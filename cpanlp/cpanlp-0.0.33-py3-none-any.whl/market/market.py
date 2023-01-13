from cpanlp.income.income import *
from cpanlp.entity.entity import *
class Market:
    def __init__(self,commodity,participants):
        self.commodity = commodity
        self.participants = participants
class PerfectlyCompetitiveMarket(Market):
    def __init__(self, commodity, participants):
        super().__init__(commodity, participants)
        self.equilibrium_price = None
        self.equilibrium_quantity = None

    def calculate_equilibrium(self):
        # Code to calculate equilibrium price and quantity
        pass
class MonopolyMarket(Market):
    def __init__(self, commodity, businessentity):
        super().__init__(commodity, [])
        self.businessentity=businessentity
        self.profit_maximizing_price = None
        self.profit_maximizing_quantity = None
        self.market_demand = None
        self.total_cost = None
if __name__ == '__main__':
    commodity=Commodity("苹果",5,30,10)
    llc=BusinessEntity("科技公司","小企业",3000)
    llc1=BusinessEntity("科技公司2","小企业2",3000)
    a= Market(commodity,[llc,llc1])
    print(a.commodity.demand)