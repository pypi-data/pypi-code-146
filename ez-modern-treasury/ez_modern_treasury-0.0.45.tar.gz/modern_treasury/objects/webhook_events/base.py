from decimal import Decimal


class Data:
    def __init__(self, json_data):
        self.json_data = json_data

    @property
    def amount(self):
        return Decimal(self.json_data.get("amount")) / 100

    @property
    def status(self):
        return self.json_data.get("status")

    @property
    def error_message(self):
        return self.json_data.get("error", {}).get("message", {})


class Event:
    def __init__(self, json_data: dict):
        self.json_data = json_data
