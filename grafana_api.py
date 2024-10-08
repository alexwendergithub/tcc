import requests
import json
import os

def add_user_grafana(username,password,new_user):
    grafana_url = os.getenv("URL_GRAFANA","10.18.0.24")+":3000"

    base_url = "http://{}:{}@{}".format(username, password, grafana_url)

    data = {
    "name":new_user["username"],
    "email":new_user["email"],
    "login":new_user["username"],
    "password":new_user["password"],
    "OrgId": 1

    }

    resp = requests.post(base_url + "/api/admin/users", json=data, verify=False)
    data = resp.json()
    return data