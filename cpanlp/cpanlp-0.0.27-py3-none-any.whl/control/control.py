class ResidualControl:
    def __init__(self, owner:str, asset:str, percentage:float):
        self.owner = owner
        self.asset = asset
        if percentage < 0 or percentage > 1:
            raise ValueError("Value must be between 0 and 1")
        self.percentage = percentage
    def transfer_control(self, new_owner):
        self.owner = new_owner
class Control:
    def __init__(self, owner="",commodity=""):
        self.commodity = commodity
        self.owner = owner
    def __str__(self):
        return f"Control(commodity={self.commodity}, owner={self.owner})"
    def transfer_control(self, new_owner:str):
        self.owner = new_owner