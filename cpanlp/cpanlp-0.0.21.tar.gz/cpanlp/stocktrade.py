class stocktrade:
    def __init__(self, balance):
        self.balance = balance

    def buy(self, price, num_shares):
        total_cost = price * num_shares
        if total_cost > self.balance:
            print("Insufficient funds")
            return
        self.balance -= total_cost
        print(f"Bought {num_shares} shares at {price} for a total cost of {total_cost}")

    def sell(self, price, num_shares):
        total_revenue = price * num_shares
        self.balance += total_revenue
        print(f"Sold {num_shares} shares at {price} for a total revenue of {total_revenue}")