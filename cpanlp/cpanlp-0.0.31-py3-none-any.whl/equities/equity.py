import datetime
from typing import List

class Equity:
    def __init__(self, account:str, value:float):
        self.account = account
        self.value = value
        self.equities: List[Equity] = []
    def __str__(self):
        return f"{self.account}: {self.value}"
    def add_equity(self, account, value):
        self.equities.append(Equity(account, value))
    def withdraw_equity(self, account, value):
        for equity in self.equities:
            if equity.account == account:
                equity.value -= value
                break
    def get_total_equities(self):
        return sum([equity.value for equity in self.equities])
if __name__ == '__main__':
    a=Equity("张老板",1000)
    print(a)
    a.add_equity("liu",1000)
    print(a.equities[0])