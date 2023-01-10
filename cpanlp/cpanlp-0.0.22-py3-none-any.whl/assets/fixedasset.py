from cpanlp.assets.asset import *


class FixedAsset(Asset):
    def __init__(self, account="建筑",debit=100000, date="2021-05-20",address="beijing"):
        super().__init__(account, debit, date)
        self.location = location
        
    def __str__(self):
        return f"{self.account} ({self.debit}), Location: {self.location}"
    
    def depreciate(self, rate):
        if rate < 0 or rate > 1:
            raise ValueError("Value must be between 0 and 1")
        self.debit -= rate*self.debit
        
    def get_location(self):
        return self.location
class RealState(FixedAsset):
    pass
if __name__ == '__main__':
    a=FixedAsset()