"""Увеличить отсуп каждой строки."""


def increase_indent(input_string: str) -> str:
    """Увеличить отсуп каждой строки."""
    lines = input_string.split("\n")
    lines_indent = ["    {0}".format(line) for line in lines]
    return "\n".join(lines_indent)
