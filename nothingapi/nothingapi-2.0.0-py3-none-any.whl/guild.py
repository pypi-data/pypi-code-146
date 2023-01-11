class Guild:
    def __init__(self, guildID: int):
        self.id = guildID
        
        # Statistics and Leaderboard
        self.totalValue = 0
        self.leaderboard = []
        self.last_updated = 0
    
    @classmethod
    def from_dict(cls, convert: dict):
        # Build guild from dictionary
        guild = cls(convert["id"])
        guild.total_value = convert["total_value"]
        guild.leaderboard = convert["leaderboard"]
        guild.last_updated = convert["last_updated"]
        return guild