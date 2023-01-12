def relative_pos_to_absolute(relative_pos: float, det_width: int):
    """
    convert relative center of rotation to absolute
    """
    return relative_pos + (det_width - 1) / 2.0


def absolute_pos_to_relative(absolute_pos: float, det_width: int):
    """
    convert absolute center of rotation to relative
    """
    return absolute_pos - (det_width - 1) / 2.0
