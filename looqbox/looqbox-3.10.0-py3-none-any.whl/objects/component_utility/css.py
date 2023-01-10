from dataclasses import dataclass


@dataclass
class Css:
    property: str
    value: str | None

    def __call__(self, value):
        new_obj = Css(self.property, value)
        return new_obj

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.property == other.property

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.property)
