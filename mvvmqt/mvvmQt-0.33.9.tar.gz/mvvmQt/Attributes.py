class Attribute:
    def __init__(self, key, value, dom, twoWay=False):
        self.key = key
        self.value = value
        self.dom = dom
        self.twoWay = twoWay

    def toDict(self):
        return {self.key: self.value}