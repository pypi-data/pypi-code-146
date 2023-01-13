HORIZONTAL = ["left", "center", "right"]
VERTICAL = ["top", "middle", "bottom"]


def position(*args):
    """Returns a formatted and validated position value as string

    :Examples:
        >>> from imglab import position
        >>> position("left", "bottom")
        'left,bottom'
        >>> position("bottom", "left")
        'bottom,left'
        >>> position("left")
        'left'
        >>> position("bottom")
        'bottom'

    :param args: The position with two directions or one single direction as strings
    :type args: list
    :raises ValueError: When arguments are an invalid position
    :return: A string value representing the position
    :rtype: str
    """
    if len(args) == 1 and __valid_position(args[0]):
        return args[0]
    elif len(args) == 2 and __valid_position(*args):
        return ",".join(args)
    else:
        raise ValueError("Invalid position")


def __valid_position(*directions):
    if len(directions) == 1 and __valid_direction(directions[0]):
        return True
    elif len(directions) == 2 and __valid_directions(directions[0], directions[1]):
        return True
    else:
        return False


def __valid_direction(direction):
    return direction in HORIZONTAL or direction in VERTICAL


def __valid_directions(direction_a, direction_b):
    return (direction_a in HORIZONTAL and direction_b in VERTICAL) or (
        direction_b in HORIZONTAL and direction_a in VERTICAL
    )
