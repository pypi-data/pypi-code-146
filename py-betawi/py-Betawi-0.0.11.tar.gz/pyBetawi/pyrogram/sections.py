n = "\n"
w = " "


def bold(x): return f"<b>{x}:</b> "
def bold_ul(x): return f"<b>--{x}:</b>-- "


def mono(x): return f"<code>{x}</code>{n}"


def section(
    title: str,
    body: dict,
    indent: int = 2,
    underline: bool = False,
) -> str:
    text = (bold_ul(title) + n) if underline else bold(title) + n

    for key, value in body.items():
        text += (
            indent * w
            + bold(key)
            + ((value[0] + n) if isinstance(value, list) else mono(value))
        )
    return text
