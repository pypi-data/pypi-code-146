import json


class ModernTreasuryException(Exception):
    def __init__(self, status_code, reason, url, json):
        Exception.__init__(self)
        self.reason = reason
        self.status_code = status_code
        self.url = url
        self.json = json


    def __str__(self) -> str:
        return (
            f"url: {self.url}, \n"
            f"status code: {self.status_code}, \n"
            f"reason: {self.json.get('errors', {}).get('message', 'response did not contain an error message')}, \n"
            f"payload {json.dumps(self.json)}, \n"
        )
