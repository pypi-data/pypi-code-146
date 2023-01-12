def urljoin(base: str, path: str):
    if base is None:
        raise ValueError("Undefined base URL!")

    if path is None:
        raise ValueError("Undefined path!")

    if len(base) == 0:
        if len(path) == 0:
            return ""

        return path

    if base.endswith("/"):
        base = base[:-1]

    if path.startswith("/"):
        path = path[1:]

    return str(f"{base}/{path}")


def slugify(value: str):
    """
    Converts the given value into a slug.

    :param value:
    :return: A slug
    """
    if value is None:
        return None

    value = value.strip()
    value = value.lower()
    value = value.replace(" ", "-")
    value = value.replace(".", "")
    value = value.replace("'", "")

    return value
