from ..native import *


def unit_of_length(length):
    if isinstance(length, Px):
        return px
    if isinstance(length, Em):
        return em
    if isinstance(length, Rem):
        return rem
    if isinstance(length, Percentage):
        return percent
    assert (False)


class LengthAttributeProxy:

    def __init__(self, node: Node, attribute_name: str):
        self.node = node
        self.attribute_name = attribute_name

    @property
    def unit(self):
        return unit_of_length(getattr(self.node, self.attribute_name))

    @unit.setter
    def unit(self, unit):
        setattr(self.node, self.attribute_name, getattr(self.node, self.attribute_name).value | unit)

    @property
    def value(self):
        value = getattr(self.node, self.attribute_name)
        return None if value is None else value.value

    @value.setter
    def value(self, value):
        setattr(self.node, self.attribute_name, value | self.unit)


class LengthPairAttributeProxy:

    def __init__(self, node: Node, attribute_name: str):
        self.node = node
        self.attribute_name = attribute_name

    @property
    def unit_x(self):
        return unit_of_length(getattr(self.node, self.attribute_name)[0])

    @unit_x.setter
    def unit_x(self, unit):
        pair = getattr(self.node, self.attribute_name)
        setattr(self.node, self.attribute_name, (pair[0].value | unit, pair[1]))

    @property
    def unit_y(self):
        return unit_of_length(getattr(self.node, self.attribute_name)[1])

    @unit_y.setter
    def unit_y(self, unit):
        pair = getattr(self.node, self.attribute_name)
        setattr(self.node, self.attribute_name, (pair[0], pair[1].value | unit))

    @property
    def value_x(self):
        pair = getattr(self.node, self.attribute_name)
        return None if pair is None else pair[0].value

    @value_x.setter
    def value_x(self, value):
        pair = getattr(self.node, self.attribute_name)
        setattr(self.node, self.attribute_name, (value | self.unit_x, pair[1]))

    @property
    def value_y(self):
        pair = getattr(self.node, self.attribute_name)
        return None if pair is None else pair[1].value

    @value_y.setter
    def value_y(self, value):
        pair = getattr(self.node, self.attribute_name)
        setattr(self.node, self.attribute_name, (pair[1], value | self.unit_y))
