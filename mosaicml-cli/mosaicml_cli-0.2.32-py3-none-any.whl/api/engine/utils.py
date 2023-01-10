""" Engine Utils """


def format_graphql(query: str) -> str:
    """Formats a graphql query into something nice

    Args:
        query: The query to format

    Returns:
        The formatted query
    """

    lines, line, indent = [], [], 0
    for char in query:
        if char.isspace() and not line:
            continue

        if char == "\n":
            lines.append('  ' * indent + ''.join(line))
            line = []
            continue

        if char == '{':
            line.append('{')
            lines.append('  ' * indent + ''.join(line))
            line = []
            indent += 1
            continue

        if char == '}':
            indent -= 1

        line.append(char)

    if line:
        lines.append(''.join(line))

    return '\n'.join(lines)
