class League:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.conference = kwargs.get("conference")

    def __repr__(self):
        return f"<League(name='{self.name}', conference='{self.conference}')>"
