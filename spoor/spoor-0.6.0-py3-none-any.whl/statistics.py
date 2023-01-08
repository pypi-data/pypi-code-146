from collections import UserList
from dataclasses import dataclass

from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table


@dataclass
class FuncCall:
    name: str
    called: bool = False
    call_count: int = 0

    def __rich_console__(
        self,
        console: Console,
        options: ConsoleOptions,
    ):
        # TODO: add hash column?
        # TODO: add id column?
        color = "yellow"
        calls = ""
        if self.called:
            color = "green"
            calls = f" ({self.call_count} calls)"

        highlight = options.highlight
        console._highlight = False
        yield f"[{color}]• {self.name}[/]{calls}"
        console._highlight = highlight


class TopCalls(UserList):
    def __rich_console__(
        self,
        console: Console,
        options: ConsoleOptions,
    ) -> RenderResult:
        # TODO: add hash column?
        # TODO: add id column?
        table = Table("#", "Name", "Called", "Call count")
        for index, entry in enumerate(self.data, start=1):
            call_count = entry[1]
            table.add_row(
                f"{index}",
                f"[bold magenta]{entry[0]}[/]",
                "[green]yes[/]" if call_count else "[yellow]no[/]",
                f"{call_count}",
            )
        yield table


if __name__ == "__main__":
    import rich

    fc = FuncCall()
    rich.print(fc)
    print(fc)
