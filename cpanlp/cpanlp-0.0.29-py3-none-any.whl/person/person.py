class Person:
    def __init__(self, name:str, age: int):
        self.name = name
        self.age = age
class Employee(Person):
    def __init__(self, name:str, age:int,emp_id:str, salary:float, department:str):
        super().__init__(name, age)
        self.emp_id = emp_id
        self.salary = salary
        self.department = department
class Partner(Person):
    def __init__(self, name:str, age:int,share: int):
        super().__init__(name, age)
        self.share = share