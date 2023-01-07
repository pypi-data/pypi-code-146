def slugify(value: str | None) -> str | None:
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


def urljoin(base: str | None, path: str | None) -> str:
    """
    Joins the given base URL and path.
    Args:
        base:
        path:

    Returns: Joined URL
    """
    if base is None:
        raise ValueError("Undefined base URL!")

    if path is None:
        raise ValueError("Undefined path!")

    if len(base) == 0:
        if len(path) == 0:
            return ""
        else:
            return path

    if base.endswith("/"):
        base = base[:-1]

    if path.startswith("/"):
        path = path[1:]

    return str(f"{base}/{path}")

def get_href_from_anchor(anchor):
    if anchor is None:
        return None

    if anchor.name != "a":
        anchor = anchor.find("a")

    if anchor is None:
        return None

    href = anchor.get("href")
    if href is None:
        return None

    href = href.strip()
    if len(href) == 0:
        return None

    return href


def get_text_from_anchor(anchor):
    if anchor is None:
        return None

    if anchor.name != "a":
        anchor = anchor.find("a")

    if anchor is None:
        return None

    text = anchor.text.strip()
    if len(text) == 0:
        return None

    return text
