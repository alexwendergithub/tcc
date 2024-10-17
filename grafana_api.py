import requests
import json
import os

def add_user_grafana(username,password,new_user):
    grafana_url = os.getenv("URL_GRAFANA","10.18.0.24")+":3000"
    isAdmin=False
    if(new_user["roleid"]!=1 and new_user["roleid"]!="1"):
        isAdmin = True
    base_url = "http://{}:{}@{}".format(username, password, grafana_url)
    data = {
    "name":new_user["username"],
    "email":new_user["email"],
    "login":new_user["username"],
    "password":new_user["password"],
    "OrgId": 1,
    }

    resp = requests.post(base_url + "/api/admin/users", json=data, verify=False)
    data = resp.json()
    if isAdmin == True:
        print("test")
        print(data['id'])
        add_admin_grafana_users(base_url,data["id"])
    return data

def add_admin_grafana_users(base_url,user_id):
    resp = requests.patch(base_url + "/api/orgs/1/users/{}".format(user_id), json={"id":user_id,"role": "Admin",}, verify=False)
    print(resp.json())