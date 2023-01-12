from typing import List
from cpanlp.assets.asset import *
from cpanlp.person.person import *
from typing import Optional

class BusinessEntity:
    def __init__(self, name:str, type:str,capital:float):
        self.name = name
        self.type = type
        self.name = name
        self.registration_number=""
        self.address=""
        self.capital=capital
        self.employees: Optional[Employee] = None
        self.assets:Optional[Asset] = None
        self.partners = []
    def add_partner(self, partner):
        self.partners.append(partner)
    def fire_employee(self, employee:Employee):
        self.employees.discard(employee)
    def hire_employee(self, employee:Employee):
        self.employees.append(employee)
    def totalsalary(self):
        return 0.0 if self.employees is None else sum([member.salary for member in self.employees])
    def merge(self, other_entity):
        """
        Merges the current LLC with another LLC
        """
        # Logic to merge the two LLCs
        self.employees.extend(other_entity.employees)
        self.capital += other_entity.capital
        self.name = f"{self.name}-{other_entity.name}"
    def spin_off(self, spin_off_name:str,spin_off_type:str,spin_off_capital:float):
        """
        Creates a new LLC as a spin-off of the current LLC
        """
        return BusinessEntity(spin_off_name,spin_off_type,spin_off_capital)
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
    def __init__(self, name:str,type:str,capital:float):
        super().__init__(name,type,capital)
        self.subsidiaries = []
        
    def establish_subsidiary(self, subsidiary_name:str, subsidiary_type:str, subsidiary_capital:float):
        """
        Create a new subsidiary LLC 
        """
        subsidiary = LLC(subsidiary_name, subsidiary_type,subsidiary_capital)
        self.subsidiaries.append(subsidiary)
        return subsidiary
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
class Partnership(BusinessEntity):
    def __init__(self, name,type,capital):
        super().__init__(name,type,capital)
        self.partners = []
    def add_partner(self, partner):
        self.partners.append(partner)
    def remove_partner(self, partner):
        self.partners.discard(partner)
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
    partner1 = BusinessEntity("Partner Inc","partner",10)
    partner2 = BusinessEntity("Partner Co","partner",100)
    partner3 = BusinessEntity("Partner LLC","partner",1000)
    partner1.add_partner(partner2)
    partner1.add_partner(partner3)
    print(len(partner1.partners))  # Output: [partner2, partner3]
    a=BusinessEntity("A","LLC",1000)
    a.employees=[Employee("a",25,"22",1000,"dd"),Employee("a",25,"22",1000,"dd")]
    a.hire_employee(Employee("x",25,"11",111,"ss"))
    b=LLC("Partner Inc","partner",10)
    print(b.subsidiaries)
    print(a.totalsalary())