from cpanlp.assets.asset import *
from cpanlp.cas import Cas

class Inventory(Asset):
    def __init__(self, account="黄金",debit=1000.0, date="2021-05-20",net_realizable_value=1000.0):
        super().__init__(account, debit, date)
        self.net_realizable_value = net_realizable_value
        self.impairment_loss = 0
        self.CAS= Cas.INVENTORY
    def definition(self):
        return "存货是指企业在日常活动中持有以备出售的产成品或商品、处在生产过程中的在产品、在生产过程或提供劳务过程中耗用的材料和物料等。"
    def confirm(self):
        if self.likely_economic_benefit and self.is_measurable:
            return True
        return False
    def value(self):
        return min(self.debit, self.net_realizable_value)
    def recognize_impairment_loss(self):
        self.impairment_loss = max(0, self.debit - self.net_realizable_value)
if __name__ == '__main__':
    a= Inventory()
    b=a.definition()
    print(b)
    c=a.value()
    print(c)
    print(a.CAS)
