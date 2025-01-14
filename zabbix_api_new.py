import requests
import json
import os
url_zabbix="http://10.255.255.4:8080/api_jsonrpc.php"

class zabbix_api:
    
    def __init__(self, url=url_zabbix,login="Admin",password="zabbix",authtoken=None):
        if authtoken==None:
            self.ZABBIX_API_URL = url
            self.USERNAME = login
            r = requests.post(self.ZABBIX_API_URL,
                    json={
                        "jsonrpc": "2.0",
                        "method": "user.login",
                        "params": {
                            "username": self.USERNAME,
                            "password": password},
                        "id": 1
                    })

            print(json.dumps(r.json(), indent=4, sort_keys=True))
            if "result" in r.json():
                self.AUTHTOKEN = r.json()["result"]
            else:
                self.AUTHTOKEN = None
        else:
            self.ZABBIX_API_URL = url
            self.USERNAME = login
            self.AUTHTOKEN = authtoken
        
    def add_host(self, params):
        added = None
        response = None
        if params["type"] != "server":
            added = self.add_host_snmp(params)
        else:
            added = self.add_host_agent(params)
        
        if(added == None):
            print("failed to add host:" + params["hostname"])
            response = {
                "code": -1,
                "data": "Failed to add host.",
                "message": "Failed to add host"
            }
            added = False
        else:
            if "error" in added:
                response = added["error"]
            else:
                response = {
                    "code": 200,
                    "data": "Sucesfully added host",
                    "message": "Sucess on add host",
                }
        return response

    def add_template(self, host, template):
        self.name = host

    def get_template(self, type):
        return template[type]

    def add_host_agent(self, params, ip="horusiff.ddns.net",dns="",port=10050,templateid=10001, zabbix_type=1):
        self.name = hostname
        request_json = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": params["hostname"],
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": params["ip"],
                        "port": params["port"]
                    }
                ],
                "groups": [
                    {
                        "groupid": params["groupid"]
                    }
                ],
                "tags": [
                    {
                        "tag": "Host name",
                        "value": "Linux server"
                    }
                ],
                "templates": [
                    {
                        "templateid": "20045"
                    }
                ],
                "macros": [
                    {
                        "macro": "{$USER_ID}",
                        "value": "123321"
                    },
                    {
                        "macro": "{$USER_LOCATION}",
                        "value": "0:0:0",
                        "description": "latitude, longitude and altitude coordinates"
                    }
                ],
                "inventory_mode": 0,
                "inventory": {
                    "macaddress_a": "01234",
                    "macaddress_b": "56768"
                }
            },
            "id": 1,
            "auth": self.AUTHTOKEN
        }
        r = requests.post(self.ZABBIX_API_URL,json=request_json)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        return r.json()

    def add_host_snmp(self, params, ip="horusiff.ddns.net",port=161,dns="", zabbix_type=2):
        host_group = {
            #cameras
            "10634":"38",
            "Templates/Video surveillance":"38",
            #router
            "10637":"39",
            #servidores
            "10636":"40",
            "10644":"40",
            "10655":"40",
            "Templates/Server hardware":"40",
            "Templates/Cloud":"40",
            #switches
            "10648":"37",
            #servidors zabbix
            "Templates/Operating systems":"4",
            "10650":"4",
            #databases
            "Templates/Databases":"20",
            #application
            "Templates/Application":"19",
            "app":"19",
            #outros
            "Templates/Virtualization":"41",
            "Templates/Telephony":"41",
            "Templates/Power":"41",
            "Templates/SAN":"41",
            "Templates/Network devices":"41",
            "-":"41",
            "outros":"41"
        }
        if params["template"] in host_group:
            host_group_to_use = host_group[params["template"]]
        elif params["template_group"] in host_group:
            host_group_to_use = host_group[params["template_group"]]
        else:
            host_group_to_use = host_group["outros"]
        details = {}
        if (params["SNMP"] == "1"):
            details = {
                "version": 1,
                "bulk": 0,
                "community": params["snmp_config[comunity_security_name]"]
            }
        elif (params["SNMP"] == "2"):
            details = {
                "version": 2,
                "bulk": 0,
                "community": params["snmp_config[comunity_security_name]"]
            }
        elif (params["SNMP"] == "3"):
            details = {
                "version": 3,
                "bulk": 0,
                "securityname": params["snmp_config[comunity_security_name]"],
                "contextname": "",
                "securitylevel": 1
            }
        print(details)
        request_json = {
                "jsonrpc": "2.0",
                "method": "host.create",
                "params": {
                    "host": params["hostname"],
                    "interfaces": [
                        {
                            "type": 2,
                            "main": 1,
                            "useip": 1,
                            "ip": params["ip"],
                            "dns": "",
                            "port": params["port"],
                            "details": details
                        }
                    ],
                    "groups": [
                        {
                            "groupid": host_group_to_use
                        }
                    ],
                    "templates": [
                    {
                        "templateid": params["template"]
                    }]
                },
                "id": 1,
                "auth": self.AUTHTOKEN
            }
        print(request_json)
        r = requests.post(self.ZABBIX_API_URL,json=request_json)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        return r.json()
            
    def add_template(self, host, template):
        self.name = host

    def get_templates_to_show(self):
        templates = self.get_templates_groups()
        response = {}
        for template_id in templates:
            response[template_id["name"]] = self.get_templates(template_id["groupid"])
        return response

    def get_templates_groups(self):
        request_json = {
                "jsonrpc": "2.0",
                "method": "templategroup.get",
                "params":{

                },
                "id": 1,
                "auth": self.AUTHTOKEN
        }
        print(request_json)
        r = requests.post(self.ZABBIX_API_URL,json=request_json)
        print(r)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        return r.json()["result"]

    def get_templates(self,id):
        request_json = {
                "jsonrpc": "2.0",
                "method": "template.get",
                "params": {
                    "output":["name","templateid"],
                    "groupids": id
                    },
                "id": 1,
                "auth": self.AUTHTOKEN
        }
        print(request_json)
        r = requests.post(self.ZABBIX_API_URL,json=request_json)
        print(r)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        return r.json()["result"]

    def add_user(self,params):
        roleid_tousrgrp = {"1":"7","2":"7","3":"7",1:"7",2:"7",3:"7"}
        request_json = {
                "jsonrpc": "2.0",
                "method": "user.create",
                "params": {
                    "username": params["username"],
                    "passwd": params["password"],
                    "roleid": params["roleid"],
                    "usrgrps": [
                        {
                            "usrgrpid": roleid_tousrgrp[params["roleid"]]
                        }
                    ]
                    },
                "id": 1,
                "auth": self.AUTHTOKEN
        }
        print(request_json)
        r = requests.post(self.ZABBIX_API_URL,json=request_json)
        print(r)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        try:
            return r.json()
        except:
            try:
                return r.json()["error"]
            except:
                json_error = {"error":{"data":"Incapaz de criar usuário no zabbix"}}
                return json_error
    
    def check_token_level(self):
        request_json = {
            "jsonrpc": "2.0",
            "method": "user.checkAuthentication",
            "params": {
                "sessionid": self.AUTHTOKEN
            },
            "id": 1
        }
        r = requests.post(self.ZABBIX_API_URL,json=request_json)
        print(r)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        is_admin = False
        admin_acess = ["2","3"]
        if r.json()["result"]["roleid"] in admin_acess:
            is_admin = True
        return is_admin