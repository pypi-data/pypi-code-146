import textwrap3


def indent(hub, data: str, level: str = 1) -> str:
    return textwrap3.indent(data, "    " * level)


def wrap(hub, data: str, width: int = 80) -> str:
    return textwrap3.wrap(data, width)
