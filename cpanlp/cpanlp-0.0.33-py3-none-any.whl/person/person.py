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