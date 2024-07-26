'''import os
import sys

from pyzabbix import ZabbixAPI, ZabbixAPIException

class zabbix_api:

    self.templates = {
        "switch": 11111,
        "router": 22222,
        "impressora": 33333,
        "servidor": 44444,
        "outro": 55555
    }
    
    def __init__(self, ip="127.0.0.1",login="Admin",password="zabbix"):
        self.zabbix_ip = "http://"+ip+"/zabbix"
        self.zabbix = ZabbixAPI(self.zabbix_ip)
        self.zabbix.login(login, passwd)

    def add_host(self, host):
        self.name = new_name

    def add_template(self, host, template):
        self.name = new_name

    def add_host_agent(self, hostname="zabbix_agent", ip="127.0.0.1",dns="",port=10050,templateid=10001 zabbix_type=2):
        try:
                # print ("Add Item: " + row['key'])
                host = self.zapi.host.create(
                    host= hostname,
                    status= 1,
                    interfaces=[{
                        "type": 1,
                        "main": "1",
                        "useip": 1,
                        "ip": ip,
                        "dns": dns,
                        "port": port
                    }],
                    groups=[{
                        "groupid": 2
                    }],
                    templates=[{
                        "templateid": templateid
                    }]
                )
        except:
                print("failed to add host")
        return host

    def add_host_snmp(self, hostname, ip="127.0.0.1",port=161,dns="" zabbix_type=2):
        try:
                host = self.zapi.host.create(
                    host= hostname,
                    status= 1,
                    interfaces=[{
                        "type": 2,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": dns,
                        "port": port,
                        "details": {
                            "version": 3,
                            "bulk": 0,
                            "securityname": "mysecurityname",
                            "contextname": "",
                            "securitylevel": 1
                        }
                        }],
                    groups=[{
                        "groupid": 4
                    }],
                    id="1"
                )
        except:
                print("failed to add host")
        return host

    def add_template(self, host, template):
        self.name = new_name
'''