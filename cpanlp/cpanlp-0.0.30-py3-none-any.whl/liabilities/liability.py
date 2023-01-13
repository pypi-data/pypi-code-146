import datetime
class Liability:
    def __init__(self,rate :float, account="", credit=0.0, due_date="2025-01-01"):
        self.account = account
        self.credit = credit
        self.due_date = due_date
        self.liabilities = []
        self.asset = None
        self.rate=rate
        today = datetime.date.today()
        due_date = datetime.datetime.strptime(self.due_date, "%Y-%m-%d").date()
        if today < due_date:
            self.remaining_days = (due_date - today).days
        else:
            raise ValueError("债务已经过期，无法计算剩余天数")
    def make_payment(self, amount):
        self.credit -= amount
        print(f"{self.account} has made a payment of {amount}, and the remaining debt is {self.credit}.")
    def __str__(self):
        return f"Liability(account='{self.account}', amount={self.credit}, due_date='{self.due_date}')"
    def add_liability(self, rate: float, account:str, credit: float, due_date:str):
            self.liabilities.append(Liability(rate,account,credit,due_date))
    def pay_liability(self,  account, amount):
        for liability in self.liabilities:
            if liability.account == account:
                    liability.amount -= amount
                    break
    def convert_to_equity(self, value):
        self.credit -= value
    def pay_off(self):
        if self.asset is not None:
            self.credit -= self.asset.debit
            self.asset = None
        else:
            raise ValueError("No asset to use for payment.")
class PonziScheme:
    def __init__(self, promise:str):
        self.promise = promise
        self.victims = []
    def add_victim(self, victim:str):
        self.victims.append(victim)
    def get_info(self):
        print(f"Promise: {self.promise}")
        print(f"Number of victims: {len(self.victims)}")
#在上面的代码中，我们添加了一个名为 is_due 的方法，用于判断负债是否已到期。该方法使用 Python 的 datetime 模块来比较当前日期和负债的到期日期，并返回布尔值。
if __name__ == '__main__':
    print(5)
    a=Liability(0.2,"a",10000,"2025-01-01")
    print(a.remaining_days)