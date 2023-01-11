import builtins
import keyword


def unclash(hub, string: str) -> str:
    """
    If the string name clashes with a builtin, then append an underscore
    """
    if keyword.iskeyword(string) or string in dir(builtins):
        return f"{string}_"
    return string
