from typing import List
from cpanlp.assets.asset import *
from cpanlp.person.person import *
from typing import Optional

class BusinessEntity:
    def __init__(self, name:str, type:str,capital:float, employees: Optional[Employee] = None):
        self.name = name
        self.type = type
        self.name = name
        self.registration_number=""
        self.address=""
        self.capital=capital
        self.employees = employees
        self.partners = []
        self.totalsalary=sum([member.salary for member in employees])
    def add_partner(self, partner):
        self.partners.append(partner)
    def fire_employee(self, employee:Employee):
        self.employees.remove(employee)
    def hire_employee(self, employee:Employee):
        self.employees.append(employee)
    def merge(self, other_entity):
        """
        Merges the current LLC with another LLC
        """
        # Logic to merge the two LLCs
        self.employees.extend(other_entity.employees)
        self.capital += other_entity.capital
        self.name = f"{self.name}-{other_entity.name}"
    def spin_off(self, spin_off_name:str,spin_off_type:str,spin_off_capital:float, spin_off_employees: List[Employee]):
        """
        Creates a new LLC as a spin-off of the current LLC
        """
        return BusinessEntity(spin_off_name,spin_off_type,spin_off_capital, spin_off_employees)
    def increase_capital(self, amount):
        """
        Increases the capital of the LLC
        """
        self.capital += amount
    def decrease_capital(self, amount):
        """
        Decreases the capital of the LLC
        """
        if self.capital - amount < 0:
            raise ValueError("Capital can not be negative")
        self.capital -= amount
class LLC(BusinessEntity):
    def __init__(self, name:str,type:str,capital:float, employees: List[Employee], assets:List[Asset]):
        super().__init__(name,type,capital, employees)
        self.subsidiaries = []
        self.assets = assets
        
    def establish_subsidiary(self, subsidiary_name:str, subsidiary_type:str, subsidiary_capital:float,subsidiary_employees:List[Employee]):
        """
        Create a new subsidiary LLC 
        """
        subsidiary = LLC(subsidiary_name, subsidiary_type,subsidiary_capital,subsidiary_employees)
        self.subsidiaries.append(subsidiary)
        return subsidiary
class Partnership(BusinessEntity):
    def __init__(self, name,type,capital,employees,partners):
        super().__init__(name,type,capital,employees)
        self.partners = partners

    def add_partner(self, partner):
        self.partners.append(partner)

    def remove_partner(self, partner):
        self.partners.remove(partner)

    def distribute_profit(self, profit):
        """Distribute the profit among partners in a pre-agreed ratio."""
        pass
    def voting_procedure(self,proposal):
        """Conduct voting procedure for major decisions on a given proposal"""
        print(f"Proposal: {proposal}")
        for partner in self.partners:
            vote = input(f"{partner}, do you approve this proposal (yes/no)")
            if vote.lower() not in ["yes","no"]:
                print("Invalid input")
            else:
                pass
    def list_partners(self):
        """List all the partners of the partnership"""
        print(self.partners)
if __name__ == '__main__':
    partner1 = BusinessEntity("Partner Inc","partner",1000,[Employee("a",25,"22",1000,"dd"),Employee("a",25,"22",1000,"dd")])
    partner2 = BusinessEntity("Partner Co","partner",1000,[Employee("a",25,"22",1000,"dd"),Employee("a",25,"22",1000,"dd")])
    partner3 = BusinessEntity("Partner LLC","partner",1000,[Employee("a",25,"22",1000,"dd"),Employee("a",25,"22",1000,"dd")])
    partner1.add_partner(partner2)
    partner1.add_partner(partner3)
    print(len(partner1.partners))  # Output: [partner2, partner3]
    a=BusinessEntity("A","LLC",1000,[Employee("a",25,"22",1000,"dd"),Employee("a",25,"22",1000,"dd")])
    a.hire_employee(Employee("x",25,"11",111,"ss"))
    print(a.totalsalary)
def transfer_assets(self, subsidiary, assets):
        """
        Transfer assets to subsidiary
        """
        if subsidiary not in self.subsidiaries:
            raise ValueError(f"{subsidiary.name} is not a subsidiary of {self.name}")
        for asset in assets:
            if asset not in self.assets:
                raise ValueError(f"{asset} is not an asset of {self.name}")
            self.assets.remove(asset)
            subsidiary.assets.append(asset)
        return f"Assets {assets} are transferred to {subsidiary.name} successfully"