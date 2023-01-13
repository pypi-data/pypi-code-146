from asset import *
class FixedAsset(Asset):
    def __init__(self, account,debit,date,purchase_price, taxes, transportation_costs, installation_costs, professional_services_costs,life_span,location):
        super().__init__(account, debit, date)
        self.purchase_price = purchase_price
        self.taxes = taxes
        self.transportation_costs = transportation_costs
        self.installation_costs = installation_costs
        self.professional_services_costs = professional_services_costs
        self.debit=self.purchase_price + self.taxes + self.transportation_costs + self.installation_costs + self.professional_services_costs
        self.location = location
        if life_span < 1:
            raise ValueError("Value must be between 0 and 1")
        self.life_span = life_span
        self.depreciation_history = []
        self.age = 0.0
        self.is_leased=False
    def __str__(self):
        return f"{self.account} ({self.debit}), Location: {self.location}"
    def depreciate(self, rate):
        if rate < 0 or rate > 1:
            raise ValueError("Value must be between 0 and 1")
        if self.age < self.life_span:
            self.depreciation_history.append(rate*self.debit)
            self.debit -= rate*self.debit
            self.age += 1
        else:
            print("Asset already reach its life span,no more depreciation.")
    def get_location(self):
        return self.location
class Land(FixedAsset):
    def __init__(self,account,debit,date,purchase_price, taxes, transportation_costs, installation_costs, professional_services_costs,life_span,location,area):
        super().__init__(self, account,debit,date,purchase_price, taxes, transportation_costs, installation_costs, professional_services_costs,life_span,location)
        self.area= area
    def zoning(self):
        # method to check zoning of land
        pass
    def rental_income(self, rental_rate):
        return self.area * rental_rate
    def appreciation(self):
        return self.market_value - self.debit
    def encumbrances(self):
        # method to check if the land has any encumbrances like mortgages, liens, etc
        pass
class RealState(FixedAsset):
    pass

if __name__ == '__main__':
    a=FixedAsset("zhang",100,"2022-02-21",22,12,12,12,12,12,"beijing")
    print(a.debit)
    print(a.location)
    print(a.likely_economic_benefit)
    a.depreciate(0.33)
    a.depreciate(0.33)
    a.depreciate(0.33)
    print(a.depreciation_history)
    print(a.debit)