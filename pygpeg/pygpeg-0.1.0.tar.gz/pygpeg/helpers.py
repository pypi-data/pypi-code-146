from .symbols import Regex as re


spaces = (
    "\u0009\u0020\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006"
    "\u2007\u2008\u2009\u200A\u202F\u205F\u3000"
)

line_breaks = "\u000A\u000B\u000C\u000D\u0085\u2028\u2029"


def optional_space():
    """
    A :class:`.symbols.Regex` that provides optional space characters.
    """
    return re(f"[{spaces}]*")


def required_space():
    """
    A :class:`.symbols.Regex` that provides required space characters.
    """
    return re(f"[{spaces}]+")


def optional_line_break():
    """
    A :class:`.symbols.Regex` that provides optional line break characters.
    """
    return re(f"[{line_breaks}]*")


def required_line_break():
    """
    A :class:`.symbols.Regex` that provides required line break characters.
    """
    return re(f"[{line_breaks}]+")


def optional_whitespace():
    """
    A :class:`.symbols.Regex` that provides optional whitespace characters.
    """
    return re(f"[{spaces}{line_breaks}]*")


def required_whitespace():
    """
    A :class:`.symbols.Regex` that provides required whitespace characters.
    """
    return re(f"[{spaces}{line_breaks}]+")
