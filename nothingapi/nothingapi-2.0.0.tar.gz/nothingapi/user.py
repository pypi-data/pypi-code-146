            
class User:
    def __init__(self, userID: int):
        self.id = userID
        
        # Profile
        self.joined_at = 0
        
        # Balance and Transactions
        self.balance = 0
        
        # Working:
        self.last_work = 0
        self.salary = 0
        
        # Inventory:
        self.inventory = []
        
        # Premium
        self.premium = False
        self.premiumStart = None
        self.premiumExpiry = None
        self.currentPlan = None
        self.nextPlan = None
        self.profileColour = None
    
    @classmethod
    def from_dict(cls, to_convert: dict):
        # Build user from dictionary
        user = cls(to_convert["id"])
        user.joined_at = to_convert["joined_at"]
        user.balance = to_convert["balance"]
        user.last_work = to_convert["last_work"]
        user.salary = to_convert["salary"]
        user.inventory = to_convert["inventory"]
        user.premium = to_convert["premium"]
        user.premiumStart = to_convert["premiumStart"]
        user.premiumExpiry = to_convert["premiumExpiry"]
        user.currentPlan = to_convert["currentPlan"]
        user.nextPlan = to_convert["nextPlan"]
        user.profileColour = to_convert["profileColour"]
        return user