try:
    import inflect

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def __init__(hub):
    hub.tool.format.inflect.ENGINE = inflect.engine()


def singular(hub, string: str) -> str:
    """
    if the string is a plural noun, make it singular.
    Return an empty string if it is already singular.
    """
    if (
        any(string.endswith(s) for s in ("ss", "is", "us", "as", "a"))
        or len(string) < 5
    ):
        return ""
    return hub.tool.format.inflect.ENGINE.singular_noun(string)
