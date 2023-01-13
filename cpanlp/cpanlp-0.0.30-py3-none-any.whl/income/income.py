import numpy as np
from typing import List
from cpanlp.assets.accountsreceivables import *
from cpanlp.control.control import *

class Commodity:
    def __init__(self, commodity:str, fair_value: float, supply:float, demand:float):
        self.name = commodity
        self.fair_value = fair_value
        self.supply = supply
        self.demand = demand
        self.supply_curve = {}
        self.demand_curve = {}
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
class Sale(Commodity):
    def __init__(self, customer:str,product:str, quantity:float, unit_price:float,date:str):
        self.supply=0
        self.demand=0
        self.name=product
        self.fair_value=unit_price
        self.customer=customer
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
        self.date=date
        self.supply_curve = {1:3,1:4}
        self.demand_curve = {1:3,1:4}
class Income(Sale,CommodityControl):
    def __init__(self, credit:float,customer:str,product:str, date):
        super().__init__(customer,product,0,0,date)
        self.credit=credit
        self.income_list =[3,2]
        self.income_list = np.array(self.income_list)
        self.mean = np.mean(self.income_list)
        self.median = np.median(self.income_list)
        self.var = np.var(self.income_list)
        self.total= sum(self.income_list)
        self.goods_control=None
        self.confirm = "确认收入" if self.goods_control is None else "不能确认收入"
        self.non_cash_consideration :str=""
        self.financing_terms :str =""
    #销售合同中存在的重大融资成分
    def __str__(self):
        return f"Income(income_list={self.income_list}, customer={self.customer}, date={self.date})"
    def recognize_revenue(self,product_info: dict = {'current_payment_obligation': True,'ownership_transferred': False,'physical_transfer': False,'risk_and_reward_transferred': False,'accepted_by_customer': False,'other_indicators_of_control': False}): 
         #确认销售收入
 # 企业就该商品享有现时收款权利，即客户就该商品负有现时付款义务
        if product_info['current_payment_obligation']:
            return True# 企业已将该商品的法定所有权转移给客户，即客户已拥有该商品的法定所有权
        elif product_info['ownership_transferred']:
            return True# 企业已将该商品实物转移给客户，即客户已实物占有该商品
        elif product_info['physical_transfer']:
            return True# 企业已将该商品所有权上的主要风险和报酬转移给客户，即客户已取得该商品所有权上的主要风险和报酬
        elif product_info['risk_and_reward_transferred']:
            return True# 客户已接受该商品
        elif product_info['accepted_by_customer']:
            return True# 其他表明客户已取得商品控制权的迹象
        elif product_info['other_indicators_of_control']:
            return True# 其他情况均不确认销售收入
        else:
            return False
    def confirm_income(self,amount):
        self.credit += amount
    def evaluate_contract(self,contract: dict = {'milestone1': ('Milestone 1', 'time-based', 100),'milestone2': ('Milestone 2', 'point-in-time', 200)}):
        """评估合同，并返回各单项履约义务的类型
    """
        # 创建字典，用于存储各单项履约义务的类型
        milestones_type = {}
        # 遍历合同中的单项履约义务
        for milestone_name, milestone in contract.items():
            # 确定履约义务的类型
            if milestone[1] == 'time-based':
                milestones_type[milestone_name] = 'time-based'
            else:
                milestones_type[milestone_name] = 'point-in-time'
        # 返回字典
        return milestones_type
    def generate_income(self,sale:Sale):
        a= Income(sale.quantity * sale.unit_price,sale.customer,sale.product,sale.date)
        b = AccountsReceivable(sale.customer, [sale.quantity * sale.unit_price],
    self.date)
        return (a,b)
class IncomeRule:
    def __init__(self, name:str, role:str):
        self.name = name
        self.role = role
    def is_principal(self):
        return self.role == "Principal"
    def is_agent(self):
        return self.role == "Agent"
class NonOperatingIncome:
    def __init__(self, income_type="投资所得", amount=100):
         self.income_type = income_type
         self.amount = amount
if __name__ == '__main__':
    sale1=Sale("zhang","apple",19,0.2,"2022-02-01")
    hin=Income(23,"zhang","pingguo","2022-02-02")
    sale1.get_supply_curve()
    incom=Income(11,"张","apple","2022-02-01")
    incom.get_market_price()
    print(incom.customer)
    incom.evaluate_contract()