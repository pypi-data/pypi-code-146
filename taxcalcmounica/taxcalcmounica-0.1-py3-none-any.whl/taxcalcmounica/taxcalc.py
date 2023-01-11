class Totalamt:
    def __init__(self,amount,percent) -> None:
        self.amount=amount
        self.percent=percent
    
    def calc_amt(amount, percent):
        return (amount * percent) / 100
  
class Amount:
    def __init__(self,total_income):
        self.total_income=total_income
    
    def calc_income_tax(self):
    
        if self.total_income <= 250000:
            return 0
        elif self.total_income <= 500000:
            return Totalamt.calc_amt(self.total_income - 
                            250000, 5)
        elif self.total_income <= 750000:
            return Totalamt.calc_amt(self.total_income - 
                            500000, 10) + 12500
        elif self.total_income <= 1000000:
            return Totalamt.calc_amt(self.total_income - 
                            750000, 15) + 37500
        elif self.total_income <= 1250000:
            return Totalamt.calc_amt(self.total_income - 
                            1000000, 20) + 75000
        elif self.total_income <= 1500000:
            return Totalamt.calc_amt(self.total_income - 
                            1250000, 25) + 125000
        else:
            return Totalamt.calc_amt(self.total_income - 
                            1500000, 30) + 187500


def result(total_income):
    total_income = float(input("What's your annual income?\n> "))
    tax = Amount(total_income)
    Z=tax.calc_income_tax()
    print(f"Tax applicable for ₹{total_income} is ₹{Z}")
