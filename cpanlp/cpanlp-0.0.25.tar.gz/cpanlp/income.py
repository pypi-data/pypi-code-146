import numpy as np
from typing import List

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
class Income:
    def __init__(self,income_list=List[float], customer="", date="2025-01-01"):
        self.income_list = income_list
        self.mean = np.mean(self.income_list)
        self.median = np.median(self.income_list)
        self.var = np.var(self.income_list)
        self.total= sum(self.income_list)
        self.customer = customer
        self.date = date
        self.goods_control=None
        self.confirm = "确认收入" if self.goods_control is None else "不能确认收入"
        self.non_cash_consideration :str=""
        self.financing_terms :str =""
    #financing_terms销售合同中存在的重大融资成分
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
class IncomeRule:
    def __init__(self, name:str, role:str):
        self.name = name
        self.role = role
    
    def is_principal(self):
        return self.role == "Principal"
    
    def is_agent(self):
        return self.role == "Agent"

class CashFlow:
    def __init__(self, amount=1000, risk="高风险", timing="短期"):
        self.amount = amount
        self.risk = risk
        self.timing = timing
    
    def __str__(self):
        return f"现金流：{self.amount}，风险水平 ：{self.risk} ，期限： {self.timing}"
    def is_positive(self):
        return self.amount > 0
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
class NonOperatingIncome:
    def __init__(self, income_type="投资所得", amount=100):
         self.income_type = income_type
         self.amount = amount
if __name__ == '__main__':
    print(1)
    cf1 = CashFlow(-1000, "中风险", "short-term")
    print(cf1)  # 输出: "Cash flow of -1000 with risk level high and timing short-term"
    print(cf1.is_positive())  # 输出: False
    control = ResidualControl("Acme Corp", "Widget Factory", 0.2)
    control.transfer_control("可读")
    print(control.owner)
    commodity = Commodity("Gold", 1000, 1000, 2000)
    commodity.get_info()
    commodity.get_price_trend()
    non_op_income = NonOperatingIncome("Investment Income", 5000)
    print(non_op_income.income_type)
    print(non_op_income.amount)
    rule1 = IncomeRule("John", "Principal")
    rule2 = IncomeRule("Jane", "Agent")
    print(rule1.is_principal())
    print(rule1.is_agent())
    print(rule2.is_principal())
    print(rule2.is_agent())
    b=ResidualControl("a","gold",0.2)
    print(b.owner)
    ww=Income(income_list=[299,222,331])
    print(ww.goods_control)
    print(ww.var)
    print(ww)
    print(ww.confirm)