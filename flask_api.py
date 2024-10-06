from flask import Flask, url_for, redirect, render_template, session
from flask import request
from flask_cors import CORS
from zabbix_api_new import *
from grafana_api import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return redirect(url_for("login"))

@app.route('/login', methods = ["POST", "GET"])
def login(): 
    if request.method == "POST":
        print(request.form)
        username = request.form["username"]
        password = request.form["password"]
        zabbix_connection = zabbix_api(login = username,password = password)
        authtoken = zabbix_connection.AUTHTOKEN
        print(request.form)
        if authtoken is not None:
            session["token"] = authtoken
            session["username"] = username
        else:
            session["failed_connection"] = True
        return redirect(url_for("index"))
    else:
        if "token" in session:
            return redirect(url_for("index"))    
        else:
            return render_template("login.html")

@app.route('/index')
def index():
    print("INSIDE INDEX")
    if "token" in session:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))

@app.route('/addhosts', methods = ["POST", "GET"])
def hosts():
    print("INSIDE ADDHOSTS")
    if request.method == "POST":
        if "token" in session:
            print(request.form)
            zabbix_connection = zabbix_api(authtoken = session["token"])
            status = zabbix_connection.add_host(request.form)
            return status
        else:
            return redirect(url_for("login"))        
    else:
        if "token" in session:
            return render_template("addhosts.html")
        else:
            return redirect(url_for("login"))

@app.route('/addusers', methods = ["POST", "GET"])
def addusers():
    print("INSIDE ADDUSERS")
    if request.method == "POST":
        if "token" in session:
            print(request.form)
            import re
            pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$"
            if not (re.fullmatch(pattern, request.form["password"])):
                return redirect(url_for("addusers", status=4))
            if (request.form["password"] != request.form["password-repeat"]):
                return redirect(url_for("addusers", status=1))
            grafana_response = add_user_grafana(session["username"],request.form["password-admin"],request.form)
            print("----grafana repsonse----")
            print(grafana_response)
            if grafana_response["message"]!="User created":
                response_status = 3
                error_message = grafana_response["message"]
                return redirect(url_for("addusers",status=response_status,error=error_message))
            else:
                zabbix_connection = zabbix_api(authtoken = session["token"])
                zabbix_response = zabbix_connection.add_user(request.form)
                response_status = 0
                error_message = 0
                print("----zabbix response----")
                print(zabbix_response)
                if not("result" in zabbix_response):
                    error_message = zabbix_response["error"]["data"]
                    response_status = 2
                    return redirect(url_for("addusers",status=response_status,error=error_message))
            
                if error_message == 0:
                    return redirect(url_for("addusers",status=response_status))
                else:
                    return redirect(url_for("addusers",status=response_status,error=error_message))
                return status
        else:
            return redirect(url_for("login"))        
    else:
        if "token" in session:
            zabbix_connection = zabbix_api(authtoken = session["token"])
            is_admin = zabbix_connection.check_token_level()
            if is_admin:
                return render_template("addusers.html")
            else:
                return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))

@app.route('/templates', methods = ['POST', "GET"])
def templates():
    if request.method == "POST":
        if "token" in session:
            print(request.form)
            zabbix_connection = zabbix_api(authtoken = session["token"])
            response = zabbix_connection.get_templates_to_show()
            return response
        else:
            return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__== "__main__":
    app.secret_key = 'BAD_SECRET_KEY'

    app.run(debug=True)