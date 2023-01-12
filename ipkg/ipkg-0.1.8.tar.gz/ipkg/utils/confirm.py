import questionary


def confirm(message: str, default: bool = False) -> bool:
    ans = questionary.confirm(message=message, default=default).unsafe_ask()
    return ans
