import math
from decimal import Decimal


def get_angle_adj_hyp(adj: float, hyp: float, unit: str = "deg") -> Decimal:
    """
    Get angle between adjacent and hypothenuse of a right triangle.
    :param adj: length of the adjacent (ankathete)
    :param hyp: length of the hypothenuse
    :param unit: "deg" or "rad"
    :return:
    """
    cos_alpha = Decimal(adj / hyp)
    angle = Decimal(math.acos(cos_alpha))
    if unit.lower() == "deg":
        angle = Decimal(math.degrees(angle))
    return angle


def get_angle_opp_hyp(opp: float, hyp: float, unit: str = "deg") -> Decimal:
    """
    Get angle between opposite and hypothenuse of a right triangle.
    :param opp: length of the opposite (Gegenkathete)
    :param hyp: length of the hypothenuse
    :param unit: "deg" or "rad"
    :return:
    """
    sin_alpha = Decimal(opp / hyp)
    angle = Decimal(math.asin(sin_alpha))
    if unit.lower() == "deg":
        angle = Decimal(math.degrees(angle))
    return angle


def get_angle_opp_adj(opp: float, adj: float, unit: str = "deg") -> Decimal:
    """
    Get angle between opposite and adjacent of a right triangle.
    :param opp: length of the opposite (Gegenkathete)
    :param adj: length of the adjacent (Ankathete)
    :param unit: "deg" or "rad"
    :return:
    """
    tan_alpha = Decimal(opp / adj)
    angle = Decimal(math.atan(tan_alpha))
    if unit.lower() == "deg":
        angle = Decimal(math.degrees(angle))
    return angle
