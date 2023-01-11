from ..native import *


class ColorAttribute(ColorEdit):

    def __init__(self, target, attribute_name):
        self.target = target
        self.attribute_name = attribute_name
        super().__init__(
            show_inputs=False,
            on_change=lambda value: setattr(self.target, attribute_name, value),
            value=lambda: self.value
        )

    @property
    def value(self):
        """ use model value as "truth" """
        return getattr(self.target, self.attribute_name)
