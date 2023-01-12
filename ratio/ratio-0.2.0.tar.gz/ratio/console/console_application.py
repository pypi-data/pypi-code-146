from ratio.console._create_argument_parser import _create_argument_parser
from ratio.console._create_rich_console import _create_rich_console
from ratio.application.application import Application


class ConsoleApplication(Application):
    def __init__(self) -> None:
        super().__init__()


def run_console_application(arguments: list[str]) -> None:
    parser = _create_argument_parser()
    parsed = parser.parse_args(arguments)

    if parsed.command not in []:
        raise NotImplementedError

    # Set up application environment
    console = _create_rich_console()
    console.print("[bold]ratio {command}[/bold]")
