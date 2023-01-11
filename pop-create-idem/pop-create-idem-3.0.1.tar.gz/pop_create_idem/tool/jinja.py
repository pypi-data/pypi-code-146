import jinja2


def template(hub, data: str) -> jinja2.Template:
    """
    return a rendered template from a string the same way every time
    """
    # noinspection JinjaAutoinspect
    return jinja2.Environment(  # nosec
        autoescape=False, lstrip_blocks=True, enable_async=True
    ).from_string(data)
