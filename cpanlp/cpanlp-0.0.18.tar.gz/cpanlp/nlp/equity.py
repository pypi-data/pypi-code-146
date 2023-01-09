class equityaccounting:
    def __init__(self):
        self.equities = []
    
    def __str__(self):
        return "\n".join([str(equity) for equity in self.equities])
    
    def add_equity(self, name, value):
        self.equities.append(equity(name, value))
    
    def withdraw_equity(self, name, value):
        for equity in self.equities:
            if equity.name == name:
                equity.value -= value
                break
    
    def get_total_equities(self):
        return sum([equity.value for equity in self.equities])

class equity:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f"{self.name}: {self.value}"
