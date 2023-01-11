import rich.console
import rich.theme


def _create_rich_console() -> rich.console.Console:
    theme = rich.theme.Theme({"error": "white on red"})
    return rich.console.Console(theme=theme)
