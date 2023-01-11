from guide_bot.elements.Element_curved import GeometryCurved
from guide_bot.elements.Element_elliptic import GeometryElliptic
from guide_bot.elements.Element_gap import GeometryGap
from guide_bot.elements.Element_kink import GeometryKink
from guide_bot.elements.Element_slit import GeometrySlit
from guide_bot.elements.Element_straight import GeometryStraight
from guide_bot.elements.Element_wolter_EH import GeometryWolter_EH
from guide_bot.elements.Element_wolter_PH import GeometryWolter_PH


def geometry_register(element_type):
    element_type = element_type.lower()
    if element_type == "curved":
        return GeometryCurved
    elif element_type == "elliptic":
        return GeometryElliptic
    elif element_type == "gap":
        return GeometryGap
    elif element_type == "kink":
        return GeometryKink
    elif element_type == "slit":
        return GeometrySlit
    elif element_type == "straight":
        return GeometryStraight
    elif element_type == "wolter_eh":
        return GeometryWolter_EH
    elif element_type == "wolter_ph":
        return GeometryWolter_PH
    else:
        raise ValueError("element_type '" + element_type + "'not found in register.")