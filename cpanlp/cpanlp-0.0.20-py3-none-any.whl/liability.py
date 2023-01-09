import datetime
class Liability:
    def __init__(self, account="张三", amount=666, due_date="2025-01-01",asset=None):
        self.account = account
        self.amount = amount
        self.due_date = due_date
        self.liabilities = []
        self.asset = asset
    def __str__(self):
        return f"Liability(account='{self.account}', amount={self.amount}, due_date='{self.due_date}')"
    def add_liability(self,  account, amount, due_date):
            self.liabilities.append(Liability( account, amount, due_date))
    def pay_liability(self,  account, amount, due_date):
        for liability in self.liabilities:
            if liability.account == account:
                    liability.amount -= amount
                    break
    def is_due(self):
        """判断负债是否已到期"""
        today = datetime.date.today()
        due_date = datetime.datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return today > due_date
    def remaining_days(self):
        today = datetime.date.today()
        due_date = datetime.datetime.strptime(self.due_date, "%Y-%m-%d").date()
        if today < due_date:
            remaining_days = (due_date - today).days
            return f"债务剩余天数{remaining_days}天"
        else:
            raise ValueError("债务已经过期，无法计算剩余天数")
    def convert_to_equity(self, value):
        self.amount -= value
    def pay_off(self):
        if self.asset is not None:
            self.amount -= self.asset.debit
            self.asset = None
        else:
            raise ValueError("No asset to use for payment.")

#在上面的代码中，我们添加了一个名为 is_due 的方法，用于判断负债是否已到期。该方法使用 Python 的 datetime 模块来比较当前日期和负债的到期日期，并返回布尔值。
if __name__ == '__main__':
    print(5)