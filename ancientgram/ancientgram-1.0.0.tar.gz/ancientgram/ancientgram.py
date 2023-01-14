import json
import requests

class Ancientgram:
    offset = None

    def __init__(self, token):
        self.token = token
        self.check_token()

    def apiRequest(self, method, params):
        resp = requests.get(url='https://api.telegram.org/bot'+self.token+"/"+method, params=params)
        data = resp.json()
        if(data['ok'] == False ):
                raise Exception({"error_code":data["error_code"], "description":data["description"]})
        return data

    def __getattr__(self, method):
        def execute(**kwargs):
            return self.apiRequest(method, kwargs)
        return execute

    def check_token(self):
        try:
            resp = requests.get(url='https://api.telegram.org/bot'+self.token+"/getMe")
            data = resp.json()
            if data["ok"] == False:
                raise Exception("Invalid token")
        except requests.exceptions.RequestException as e:
            print(e)
    
    def loop(self, handler):
        while True:
            try:
                resp = requests.get(url='https://api.telegram.org/bot'+self.token+"/getUpdates", params={'offset':self.offset, 'timeout':10})
                data = resp.json()
                if data["ok"] == True and len(data["result"])>0:
                    for update in data["result"]:
                        if "update_id" in update:
                            self.offset = update["update_id"] + 1
                            handler(update)
            except requests.exceptions.RequestException as e:
                print(e)