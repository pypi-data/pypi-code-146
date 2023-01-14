from cpanlp.entity.entity import *

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
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
        self.business_name = business
        self.industry = industry
        self.employees = []
    def hire_employee(self, employee):
        self.employees.append(employee)
        print(f"{employee.name} has been hired by {self.business_name}.")
    def fire_employee(self, employee):
        self.employees.remove(employee)
        print(f"{employee.name} has been fired by {self.business_name}.")
    def list_employees(self):
        for employee in self.employees:
            print(employee.name)
    def raise_funds(self, amount):
        print(f"{self.business_name} has raised ${amount} in funding.")
    def acquire_company(self, company):
        print(f"{self.business_name} has acquired {company.business_name}.")
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