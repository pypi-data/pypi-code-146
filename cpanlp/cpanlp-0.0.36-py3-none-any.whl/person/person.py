from cpanlp.entity.entity import *
import math
import numpy as np
import pandas as pd
def calculate_beta(portfolio):
    # Load historical data for each stock in the portfolio
    stocks_data = {}
    for stock in portfolio:
        data = pd.read_csv(stock + ".csv")
        stocks_data[stock] = data
    # Calculate the daily returns for each stock
    returns = {}
    for stock, data in stocks_data.items():
        returns[stock] = data["Adj Close"].pct_change()
    # Calculate the covariance matrix between the returns of all stocks
    cov_matrix = np.cov(list(returns.values()))
    # Calculate the beta value of the portfolio
    beta = cov_matrix[0][1] / np.var(returns["market"])
    return beta
def log_utility(good_utility, price, consumer_income):
    return math.log(good_utility - price / consumer_income)
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
class Investor(Person):
    def __init__(self,name, age, portfolio, expected_return, risk_preference):
        super().__init__(name, age)
        self.portfolio = portfolio
        self.expected_return = expected_return
        self.risk_preference = risk_preference
    def calculate_risk_neutrality(self):
        # Code to calculate the beta value of the portfolio
        beta = calculate_beta(self.portfolio)
        return beta
class Employee(Person):
    def __init__(self, name, age,emp_id, salary, department):
        super().__init__(name, age)
        self.emp_id = emp_id
        self.salary = salary
        self.department = department
class Partner(Person):
    def __init__(self, name, age,share):
        super().__init__(name, age)
        self.share = share
class Entrepreneur(Person):
    def __init__(self, name, age,business, industry):
        super().__init__(name, age)
        self.business = business
        self.industry = industry
        self.employees = []
    def hire_employee(self, employee):
        self.employees.append(employee)
        print(f"{employee.name} has been hired by {self.business}.")
    def fire_employee(self, employee):
        self.employees.remove(employee)
        print(f"{employee.name} has been fired by {self.business}.")
    def list_employees(self):
        for employee in self.employees:
            print(employee.name)
    def raise_funds(self, amount):
        print(f"{self.business} has raised ${amount} in funding.")
    def acquire_company(self, company):
        print(f"{self.business} has acquired {company.name}.")
class Auditor(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
class Consumer(Person):
    def __init__(self, name, age, utility_function):
        super().__init__(name, age)
        self.utility_function = utility_function
    def calculate_utility(self, goods, prices, income):
        """
        Calculates the total utility for a consumer given a set of goods, their prices, and the consumer's income
        """
        total_utility = 0
        for i in range(len(goods)):
            total_utility += self.utility_function(goods[i], prices[i], income)
        return total_utility
if __name__ == '__main__':
    # Create an Entrepreneur
    john = Entrepreneur("John Smith",30, "Acme Inc", "Technology")
    # Hire employees
    employee1 = Employee("zhang",19,1333,2000,"accounting")
    employee2 = Employee("zhang12",29,233,2000,"accounting")
    john.hire_employee(employee1)
    john.hire_employee(employee2)
    # List employees
    john.list_employees()
    # Raise funds
    john.raise_funds(1000000)
    # Acquire company
    company = LLC("deloitte","auditor",20000)
    john.acquire_company(company)