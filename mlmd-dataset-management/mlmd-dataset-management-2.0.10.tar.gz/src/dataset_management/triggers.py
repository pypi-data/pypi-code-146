import requests
import json
class ApiTrigger:
    def __init__(self, method=None, url=None, data=None, authorization=None) -> None:
        self.method = method
        self.url = url
        self.data = data
        self.authorization = authorization

    def execute(self):
        print("Trigger: sending request to {}".format(self.url))
        try:
            res = requests.request(self.method, self.url, data=json.dumps(self.data), headers={
            "Content-Type":"application/json", 
            # "Authorization": "Basic " + self.authorization
            })
        except Exception as e:
            print(e)
            return False
        print("Trigger: response {}".format(res.content))
        return res

    def __str__(self) -> str:
        return json.dumps({
            "method": self.method,
            "url": self.url,
            "data": self.data
        })

    @staticmethod
    def from_json_string(json_str):
        if json_str is None or json_str == '':
            return None
        obj = json.loads(json_str)
        ret = ApiTrigger()
        ret.__dict__.update(obj)
        return ret
