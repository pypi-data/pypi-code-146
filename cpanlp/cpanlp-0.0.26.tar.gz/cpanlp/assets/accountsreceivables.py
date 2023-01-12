from cpanlp.assets.asset import *
from datetime import datetime
class AccountsReceivable(Asset):
    def __init__(self,account, debit, date):
        super().__init__(account, debit, date)
        self.due_dates = {}
    
    def add_receivable(self, value, due_date):
        self.debit += value
        self.due_dates[due_date] = value
        
    def reduce_receivable(self, value, due_date):
        self.debit -= value
        self.due_dates[due_date] -= value

    def check_due_date(self, date):
        total_due = 0
        date = datetime.strptime(date, "%Y-%m-%d").date()
        for d, v in self.due_dates.items():
            d = datetime.strptime(d, "%Y-%m-%d").date()
            if d <= date:
                total_due += v
        return total_due
if __name__ == '__main__':
    print(5)
