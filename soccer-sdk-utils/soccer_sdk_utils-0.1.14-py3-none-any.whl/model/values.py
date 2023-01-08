import uuid


class Values:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.sw = kwargs.get("sw")
        self.tds = kwargs.get("tds")
        self.ecnl = kwargs.get("ecnl")

    def generate_id(self):
        """Generates a unique ID for the user in place"""
        self.id = str(uuid.uuid4())
