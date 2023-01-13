class Spirit:
    def __init__(self):
        self.determination = None
        self.passion = None
    def set_determination(self, determination):
        self.determination = determination
    def set_passion(self, passion):
        self.passion = passion
    def display(self):
        print(f'Determination: {self.determination}')
        print(f'Passion: {self.passion}')
class EntrepreneurialSpirit(Spirit):
    def __init__(self):
        super().__init__()
        self.vision = None
        self.risk_taking = None
        self.innovation = None
        self.perseverance = None
        self.leadership = None

    def set_vision(self, vision):
        self.vision = vision

    def set_risk_taking(self, risk_taking):
        self.risk_taking = risk_taking

    def set_innovation(self, innovation):
        self.innovation = innovation

    def set_perseverance(self, perseverance):
        self.perseverance = perseverance

    def set_leadership(self, leadership):
        self.leadership = leadership

    def display(self):
        super().display()
        print(f'Vision: {self.vision}')
        print(f'Risk Taking: {self.risk_taking}')
        print(f'Innovation: {self.innovation}')
        print(f'Perseverance: {self.perseverance}')
        print(f'Leadership: {self.leadership}')