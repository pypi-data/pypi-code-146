from typing import List


class ConnectionResponse:
    def __init__(self, json):
       self.json = json
    
    @property
    def id(self):
        return self.json.get("id")

    @property
    def object(self):
        return self.json.get("object")

    @property
    def live_mode(self):
        return self.json.get("live_mode")

    @property
    def vendor_id(self):
        return self.json.get("vendor_id")
        
    @property
    def vendor_name(self):
        return self.json.get("vendor_name")

    @property
    def vendor_customer_id(self):
        return self.json.get("vendor_customer_id")

    @property
    def discarded_at(self):
        return self.json.get("discarded_at")
