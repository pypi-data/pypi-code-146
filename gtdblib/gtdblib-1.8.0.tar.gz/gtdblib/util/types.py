def is_float(s) -> bool:
    """Check if a string can be converted to a float.

    :param s: Any object to convert to a float.
    """

    try:
        float(s)
    except ValueError:
        return False

    return True
