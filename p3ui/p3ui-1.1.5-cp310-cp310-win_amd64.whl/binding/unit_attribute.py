from ..native import *


class UnitAttribute(ComboBox):
    UnitToIndex = {px: 0, em: 1, rem: 2, percent: 3}
    IndexToUnit = [px, em, rem, percent]

    def __init__(self, target, attribute_name, percentage=True):
        self.target = target
        self.attribute_name = attribute_name
        options = ['px', 'em', 'rem']
        if percentage:
            options.append('%')
        super().__init__(
            on_change=lambda index: setattr(self.target, self.attribute_name, UnitAttribute.IndexToUnit[index]),
            width=(4 | em, 0, 0),
            selected_index=lambda: UnitAttribute.UnitToIndex[self.value],
            options=options
        )

    @property
    def value(self):
        # this overrides the property from the input. the 'view'-value is not considered being the real value and
        # can only change, if the underlying model changed.
        return getattr(self.target, self.attribute_name)
