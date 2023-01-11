import re
from ..native import *


class EnumAttribute(ComboBox):
    def to_dict(enum):
        return {k: v for k, v in enum.__dict__.items() if re.search("^[A-Z]", k) is not None}

    def __init__(self, enum_class, target, attribute_name):
        self.target = target
        self.attribute_name = attribute_name
        self.enum_class = enum_class
        self._dict = EnumAttribute.to_dict(enum_class)
        options = [key for key, _ in self._dict.items()]
        super().__init__(
            on_change=lambda index: setattr(self.target, self.attribute_name, self._dict[options[index]]),
            width=(4 | em, 1, 0),
            selected_index=lambda: options.index(enum_class(getattr(self.target, self.attribute_name)).name),
            options=options
        )

    @property
    def value(self):
        """
        this overrides the default one. the 'view'-value is not considered being the real value and
        can only change, if the underlying model changed.
        """
        return getattr(self.target, self.attribute_name)
