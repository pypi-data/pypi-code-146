import json


class Response:
    def __init__(self, status, data):
        self.status = str(status)
        self.raw_data = data

    @property
    def data(self):
        return str.encode(json.dumps(self.raw_data))
