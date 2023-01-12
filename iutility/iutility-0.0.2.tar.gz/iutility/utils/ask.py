from questionary import confirm as raw_confirm

from . import config


def confirm(message: str, default: bool = True) -> bool:
    if config.ask:
        return raw_confirm(message=message, default=default).unsafe_ask()
    else:
        return default
