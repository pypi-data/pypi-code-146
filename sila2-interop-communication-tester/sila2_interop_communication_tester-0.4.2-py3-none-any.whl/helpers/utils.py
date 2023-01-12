import uuid


def string_is_uuid(uuid_string: str) -> bool:
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def normalize_docstring(docstring: str) -> str:
    docstring.replace("\r\n", "\n")
    original_lines = docstring.splitlines(keepends=False)

    line_is_empty: list[bool] = [len(line.strip()) == 0 for line in original_lines]
    try:
        first_nonempty_index = line_is_empty.index(False)
    except ValueError:
        first_nonempty_index = 0
    try:
        last_nonempty_index = len(line_is_empty) - 1 - line_is_empty[::-1].index(False)
    except ValueError:
        last_nonempty_index = len(line_is_empty) - 1

    min_indent = 100
    lines = []
    for line in original_lines[first_nonempty_index : last_nonempty_index + 1]:
        line = line.rstrip()
        line = line.replace("\t", " " * 4)
        if not line:
            lines.append("")
            continue
        indent_length = len(line) - len(line.lstrip())
        if indent_length < min_indent:
            min_indent = indent_length
        lines.append(line)

    for i, line in enumerate(lines):
        lines[i] = line[min_indent:]

    return "\n".join(lines)
