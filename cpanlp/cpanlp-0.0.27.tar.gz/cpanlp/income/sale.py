from cpanlp.assets.accountsreceivables import *

class Sale:
    def __init__(self, customer:str,product:str, quantity:float, unit_price:float,date:str):
        self.customer=customer
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
        self.date=date
    def generate_income(self):
        return Income([self.quantity * self.unit_price],self.customer,self.date),AccountsReceivable(self.customer, [self.quantity * self.unit_price],self.date)