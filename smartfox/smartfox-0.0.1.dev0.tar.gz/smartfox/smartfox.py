"""SmartFox API wrapper for Python"""

import requests
from xml.etree import ElementTree

class Smartfox():
    def __init__(self, host, port=80, verify=False, scheme="http", **kwargs):
        self.host = host
        self.port = port
        self.verify = verify
        self.scheme = scheme
        
        self.valuesPath = kwargs.get("valuesPath", "values")
        self.timeout = kwargs.get("timeout", 5)
        
        
    def getValues(self):
        resp = requests.get(f"{self.scheme}://{self.host}/{self.valuesPath}", verify=self.verify)
        if resp.status_code == 200:
            return ElementTree.fromstring(resp.content)
        