from cpanlp.account.assets.asset import *
from sklearn.linear_model import LinearRegression
import random
import matplotlib.pyplot as plt
class IntangibleAsset(Asset):
    def __init__(self,account,debit, date,amortization_rate):
        super().__init__(account, debit, date)
        self.amortization_rate = amortization_rate
        self.amortization_history = []
        self.model = LinearRegression()
    def train(self):
        pass
    def predict(self, num_steps):
        pass
    
    def amortize(self, period: int):
        self.debit -= self.debit * self.amortization_rate * period
        self.amortization_history.append((period, self.debit))
    def simulate_volatility(self, volatility, num_steps):
        prices = [self.debit]
        for i in range(num_steps):
            prices.append(prices[-1] * (1 + volatility * random.uniform(-1, 1)))
        plt.plot(prices)
        plt.show()
class Goodwill(IntangibleAsset):
    def __init__(self,account,debit, date,amortization_rate):
        super().__init__(account,debit, date,amortization_rate)
        
if __name__ == '__main__':
    print(11)
    a=IntangibleAsset("a",3000,"2022-01-01",0.3)
    print(a.model)
    c=Goodwill("a",3000,"2022-01-01",0.3)
    print(c.debit)