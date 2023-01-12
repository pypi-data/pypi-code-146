class Stakeholder:
    def __init__(self, name: str, interests: str):
        self.name = name
        self.interests = interests
        self.contact_info = ""
        self.concern=""
        self.suggest=""
class Media(Stakeholder):
    def __init__(self, name: str, interests: str):
        super().__init__(name, interests)
        self.media_type = ""
        self.publish=""
class Public(Stakeholder):
    def __init__(self, name: str, interests: str):
        super().__init__(name, interests)
        self.voice=""

if __name__ == '__main__':
    customer = Stakeholder("Jane", "product quality and customer service")
    b=Media("xinhua","合作")
