import requests

class EndpointClient:

    def __init__(self, base_url = None):
        
        if base_url is None:
            self.base_url = "http://localhost:6030"
        else:
            self.base_url = base_url

        self.headers = {'Content-Type': 'application/json'}

    def predict_record(self, endpoint, query):
        url = self.base_url + endpoint
        response = requests.post(url, headers= self.headers, json=query)
        return response.json()
    
    def predict_records(self, endpoint, queries):
        url = self.base_url + endpoint
        response = requests.post(url, headers= self.headers, json=queries)
        return response.json()