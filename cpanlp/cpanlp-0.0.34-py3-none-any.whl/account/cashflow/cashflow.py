class CashFlow:
    def __init__(self, amount, risk, timing):
        self.amount = amount
        self.risk = risk
        self.timing = timing
    def __str__(self):
        return f"现金流：{self.amount}，风险水平 ：{self.risk} ，期限： {self.timing}"
    def is_positive(self):
        return self.amount > 0
if __name__ == '__main__':
    print(11)