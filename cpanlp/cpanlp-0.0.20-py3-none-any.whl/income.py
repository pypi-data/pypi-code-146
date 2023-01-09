class Income:
    def __init__(self, amount=100, source="张老板", date="2021-05-02",control=None):
        self.amount = amount
        self.source = source
        self.date = date
        self.control = control
    def __str__(self):
        return f"Income(amount={self.amount}, source={self.source}, date={self.date})"
    def confirm(self,commodity,owner):
        if self.control.commodity == commodity:
            # 如果商品是汽车，则需要判断客户是否取得了汽车的控制权
            if self.control.owner == owner:
                # 如果客户是 Alice，则确认收入
                return True
            else:
                # 否则不能确认收入
                return False
        else:
            # 如果商品不是汽车，则直接确认收入
            return False
class Control:
    def __init__(self, commodity="苹果", owner="老白"):
        self.commodity = commodity
        self.owner = owner
    def __str__(self):
        return f"Control(commodity={self.commodity}, owner={self.owner})"
if __name__ == '__main__':
    print(1)