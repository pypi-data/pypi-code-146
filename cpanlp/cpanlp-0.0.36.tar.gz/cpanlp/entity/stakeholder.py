from cpanlp.entity.entity import *
class Stakeholder:
    def __init__(self, name, interests):
        self.name = name
        self.interests = interests
        self.contact_info = ""
        self.concern=""
        self.suggest=""
class Government(Stakeholder):
    def __init__(self, name, interests, government_type):
        super().__init__(name, interests)
        self.government_type = government_type
    def regulate_company(self, company):
        # Code to regulate the company
        pass
    def make_policy(self, policy):
        # Code to make a policy
        pass
class Media(Stakeholder):
    def __init__(self, name, interests):
        super().__init__(name, interests)
        self.media_type = ""
        self.publish=""
class Public(Stakeholder):
    def __init__(self, name, interests):
        super().__init__(name, interests)
        self.voice=""
class RatingAgency(Stakeholder):
    def __init__(self, name, interests):
        super().__init__(name, interests)
        self.ratings = {}
    def assign_rating(self, company, rating):
        self.ratings[company.name] = rating
class Bank(Stakeholder):
    def __init__(self, name, interests):
        super().__init__(name, interests)
        self.loans = {}
    def grant_loan(self, company, amount):
        self.loans[company.name] = amount
        
if __name__ == '__main__':
    customer = Stakeholder("Jane", "product quality and customer service")
    b=Media("xinhua","合作")
    agency = RatingAgency("Moody's","makemoney")
    agency.assign_rating(LLC("huawei","technology",10000),"A")
    print(agency.ratings)

