import requests
import json

class zabbix_api:

    templates = {
        "switch": 11111,
        "router": 22222,
        "impressora": 33333,
        "servidor": 44444,
        "outro": 55555
    }
    
    def __init__(self, url="http://horusiff.ddns.net/api_jsonrpc.php",login="Admin",password="x9v4c1l4um!",authtoken=None):
        if authtoken==None:
            self.ZABBIX_API_URL = url
            self.USERNAME = login
            r = requests.post(self.ZABBIX_API_URL,
                    json={
                        "jsonrpc": "2.0",
                        "method": "user.login",
                        "params": {
                            "user": self.USERNAME,
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
                        "dns": params["dns"],
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
                            "dns": params["dns"],
                            "port": params["port"],
                            "details": {
                                "version": 3,
                                "bulk": 0,
                                "securityname": "mysecurityname",
                                "contextname": "",
                                "securitylevel": 1
                            }
                        }
                    ],
                    "groups": [
                        {
                            "groupid": "4"
                        }
                    ]
                },
                "id": 1,
                "auth": self.AUTHTOKEN
            }
        r = requests.post(self.ZABBIX_API_URL,json=request_json)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        return r.json()
            
    def add_template(self, host, template):
        self.name = host

    def get_templates(self):
        request_json = {
                "jsonrpc": "2.0",
                "method": "template.get",
                "params": {
                    "output": "extend"
                },
                "id": 1,
                "auth": self.AUTHTOKEN
        }
        r = requests.post(self.ZABBIX_API_URL,json=request_json)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        return r.json()
