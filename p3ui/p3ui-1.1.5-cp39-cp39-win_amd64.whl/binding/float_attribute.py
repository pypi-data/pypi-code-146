from ..native import *


class FloatAttribute(InputFloat):

    def __init__(self, target, attribute_name):
        self.target = target
        self.attribute_name = attribute_name
        super().__init__(
            width=(1 | px, 1, 0),
            on_change=lambda value: setattr(self.target, attribute_name, value),
            value=lambda: self.value
        )

    @property
    def value(self):
        """ use model value as "truth" """
        return getattr(self.target, self.attribute_name)
