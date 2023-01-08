

class Webcomponent:
    def __init__(self):
        self.registry = {}

    def get(self, tag):
        return self.registry.get(tag, None)

    def define(self, tag, klass):
        self.registry[tag] = klass


webcomponent = Webcomponent()
