import questionary

from .. import config


def confirm(message: str, default: bool = True) -> bool:
    if config.confirm:
        response = questionary.confirm(message=message, default=default).unsafe_ask()
        return response
    else:
        return default
