from flask import Flask, url_for, redirect, render_template, session
from flask import request
from flask_cors import CORS
from zabbix_api_new import *

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
        #zabbix_connection = zabbix_api(login = username,password = password)
        #authtoken = zabbix_connection.AUTHTOKEN
        authtoken = "hehe"
        print(request.form)
        if authtoken is not None:
            session["token"] = authtoken
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__== "__main__":
    app.secret_key = 'BAD_SECRET_KEY'

    app.run(debug=True)