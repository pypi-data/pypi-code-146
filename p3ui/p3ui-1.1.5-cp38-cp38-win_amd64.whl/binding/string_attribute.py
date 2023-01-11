from ..native import *


class StringAttribute(InputText):

    def __init__(self, target, attribute_name):
        self.target = target
        self.attribute_name = attribute_name
        super().__init__(
            width=(1 | px, 1, 0),
            on_change=self._on_change,
            value=lambda: self._value
        )
        self.eval()
        self.value = self._value

    @property
    def _value(self):
        value = getattr(self.target, self.attribute_name)
        return '' if value is None else value

    def _on_change(self, *args):
        setattr(self.target, self.attribute_name, self.value)
