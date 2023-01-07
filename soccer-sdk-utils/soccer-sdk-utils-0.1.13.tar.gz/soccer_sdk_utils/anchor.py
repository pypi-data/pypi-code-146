from bs4 import element


def get_href(tag: element) -> str | None:
    if tag is None:
        return None

    if tag.name != "a":
        tag = tag.find("a")

    if tag is None:
        return None

    href = tag.get("href")
    if href is None:
        return None

    href = href.strip()
    if len(href) == 0:
        return None

    return href


def get_text(tag: element) -> str | None:
    if tag is None:
        return None

    if tag.name != "a":
        tag = tag.find("a")

    if tag is None:
        return None

    text = tag.text.strip()
    if len(text) == 0:
        return None

    return text
