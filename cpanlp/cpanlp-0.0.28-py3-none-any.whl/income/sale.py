from cpanlp.assets.accountsreceivables import *
from cpanlp.income.income import *
class Commodity:
    def __init__(self, name:str, fair_value: float, supply:float, demand:float):
        self.name = name
        self.fair_value = fair_value
        self.supply = supply
        self.demand = demand
    def get_info(self):
        print(f"Name: {self.name}")
        print(f"Fair value: {self.fair_value}")
        print(f"Supply: {self.supply}")
        print(f"Demand: {self.demand}")
    def get_market_price(self):
        if self.supply > self.demand:
            print(f"The market price of {self.name} is lower than its fair value")
        elif self.supply < self.demand:
            print(f"The market price of {self.name} is higher than its fair value")
        else:
            print(f"The market price of {self.name} is equal to its fair value")
    def get_supply_demand_gap(self):
        gap = self.demand - self.supply
        if gap > 0:
            print(f"The demand for {self.name} is higher than its supply")
        elif gap < 0:
            print(f"The supply for {self.name} is higher than its demand")
        else:
            print(f"The supply and demand for {self.name} is balanced")
    def get_price_trend(self):
        if self.supply > self.demand:
            print(f"The price of {self.name} is expected to decrease in the future")
        elif self.supply < self.demand:
            print(f"The price of {self.name} is expected to increase in the future")
        else:
            print(f"The price of {self.name} is expected to remain stable in the future")
    def get_supply_curve(self):
        print(f"The supply curve for {self.name} is as follows:")
        for price, quantity in self.supply_curve.items():
            print(f"Price: {price}, Quantity: {quantity}")
            
    def get_demand_curve(self,demand_curve):
        print(f"The demand curve for {self.name} is as follows:")
        for price, quantity in demand_curve.items():
            print(f"Price: {price}, Quantity: {quantity}")
class Sale:
    def __init__(self, customer:str,product:str, quantity:float, unit_price:float,date:str):
        self.customer=customer
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
        self.date=date
    def generate_income(self):
        a= Income([self.quantity * self.unit_price],self.customer,self.date)
        b = AccountsReceivable(self.customer, [self.quantity * self.unit_price],self.date)
        return (a,b)
if __name__ == '__main__':
    print(11)
    sales = Sale("张","apple",50,0.2,"20230101")
    (income,receivables) = sales.generate_income()
    print(income.income_list) #1000