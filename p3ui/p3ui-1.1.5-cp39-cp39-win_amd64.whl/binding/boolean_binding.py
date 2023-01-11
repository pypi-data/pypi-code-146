from ..native import *
from .optional_attribute import OptionalAttribute


class BooleanBinding(Row):

    def __init__(self, target, attribute_name):
        self.target = target
        self.attribute_name = attribute_name

        super().__init__(
            width=(1 | px, 1, 0),
            on_mouse_down=lambda _: self._toggle(),
            value=lambda: self.value,
            align_items=Alignment.Center,
            justify_content=Justification.Center,
            children=[Text(value=lambda: 'true' if self.value else 'false')]
        )

    def _toggle(self):
        self.value = not self.value

    @property
    def value(self):
        """ use model value as "truth" """
        return getattr(self.target, self.attribute_name)

    @value.setter
    def value(self, value):
        setattr(self.target, self.attribute_name, value)
        self.eval()


class OptionalBooleanBinding(OptionalAttribute):

    def __init__(self, target, attribute_name, default_to=True):
        super().__init__(
            target=target,
            attribute_name=attribute_name,
            children=[
                BooleanBinding(
                    target=target,
                    attribute_name=attribute_name
                )
            ],
            default_to=default_to
        )
