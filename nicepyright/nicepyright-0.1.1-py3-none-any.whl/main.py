import asyncio
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import AsyncIterable, Dict, Tuple, List, Union

from rich.align import Align
from rich.console import Group
from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from nicepyright.definitions import DiagnosticRule, Range, SeverityLevel
from nicepyright.messages import camel_case_to_capitalized_text, parse_message


@dataclass(frozen=True)
class PyrightDiagnostic:
    file: Path
    severity: SeverityLevel
    message: str
    range_start: Range
    range_end: Range
    rule: Union[DiagnosticRule, None] = None

    @classmethod
    def from_dict(cls, d: dict):
        """Convert a dict, as per `pyright --outputjson`, to a PyrightOutput instance.

        Args:
            d: A dict, as per `pyright --outputjson`.

        Returns:
            A PyrightOutput instance.
        """
        d["file"] = Path(d["file"])
        d["severity"] = SeverityLevel[d["severity"].capitalize()]
        rng = d.pop("range")
        d["range_start"] = Range(rng["start"]["line"], rng["start"]["character"])
        d["range_end"] = Range(rng["end"]["line"], rng["end"]["character"])
        d["rule"] = DiagnosticRule[d["rule"].replace("report", "")] if "rule" in d else None
        return cls(**d)

    @property
    def code_fragment(self):
        """Return the code that caused the error.

        This is the code that is between the start and end of the error range.

        Returns:
            The code that caused the error.
        """
        file_contents = self.file.read_text()
        lines = file_contents.splitlines()
        out_lines = lines[self.range_start.line : self.range_end.line + 1]
        out_lines[0] = out_lines[0][self.range_start.character :]
        out_lines[-1] = out_lines[-1][: self.range_end.character]
        return "\n".join(out_lines)

    def get_surrounding_code(self, n_lines: int = 3) -> Tuple[str, int, int]:
        """Return the code that caused the error, with surrounding context.

        Args:
            n_lines: The number of lines of context to include before and after the error.

        Returns:
            The code that caused the error, with surrounding context.
        """
        file_contents = self.file.read_text()
        lines = file_contents.splitlines()
        start_line = max(0, self.range_start.line - n_lines)
        end_line = min(len(lines), self.range_end.line + n_lines + 1)
        out_lines = lines[start_line:end_line]
        return "\n".join(out_lines), start_line + 1, end_line

    def get_rich_syntax(
        self,
        n_context_lines: int = 3,
        # error_style: Style = Style(color="red", bold=True, underline=True),
        error_style: Style = Style(bold=True, underline=True, reverse=True),
        dimmed_style: Style = Style(dim=True),
    ) -> Syntax:
        """Return a rich Syntax instance for the code that caused the error.

        Args:
            n_context_lines: The number of lines of context to include before and after the error.

        Returns:
            A rich Syntax instance for the code that caused the error.
        """
        n_lines = len(self.file.read_text().splitlines())

        line_start = (
            1
            if self.range_start.line - n_context_lines <= 1
            else self.range_start.line - n_context_lines
        )
        line_end = (
            n_lines
            if self.range_end.line + n_context_lines >= n_lines
            else self.range_end.line + n_context_lines
        )

        syntax = Syntax(
            self.file.read_text(),
            "python",
            line_numbers=True,
            line_range=(
                line_start,
                line_end,
            ),
            highlight_lines=set(range(self.range_start.line + 1, self.range_end.line + 2)),
            background_color="default",
        )
        syntax.stylize_range(
            error_style,
            (self.range_start.line + 1, self.range_start.character),
            (self.range_end.line + 1, self.range_end.character),
        )
        syntax.stylize_range(
            dimmed_style,
            start=(line_start, 0),
            end=(self.range_end.line + 1, 0),
        )
        syntax.stylize_range(
            dimmed_style,
            start=(self.range_end.line + 2, 0),
            end=(line_end, 999999),
        )
        return syntax

    def get_parsed_message(self):
        """Return the parsed message.

        Returns:
            The parsed message.
        """
        return parse_message(self.message)

    def __rich_console__(self, console, options):
        """Render the diagnostic to the console."""
        diagnostic = self.get_parsed_message()
        diagnostic_str = diagnostic.category_text
        # con.print(diagnostic_str)

        err_class_style = {
            SeverityLevel.Error: "[bold red]",
            SeverityLevel.Warning: "[bold yellow]",
            SeverityLevel.Information: "[bold blue]",
        }[self.severity]

        if self.rule is not None:
            err_description = f" ({camel_case_to_capitalized_text(self.rule.name)})"
        else:
            err_description = ""
        err_title = f"{err_class_style}{self.severity.name.capitalize()}[/]{err_description}"

        f_path, f_name = str(self.file.relative_to(Path.cwd()).parent), self.file.name
        file_display = f"[dim]{f_path}[/]/[bold #FFFFFF]{f_name}[/]"
        err_subtitle = (
            f"{file_display} ─── "
            f"[blue]{self.range_start.line + 1}[/]:"
            f"[blue]{self.range_start.character + 1}[/]"
        )

        panel = Panel(
            Group(
                self.get_rich_syntax(),
                Padding(Text(self.message, style="bold"), (1, 2, 0, 2)),
            ),
            title=err_title,
            title_align="left",
            subtitle=err_subtitle,
            subtitle_align="left",
            padding=(1, 1),
        )
        yield Padding(panel, (1, 0))


@dataclass(frozen=True)
class PyrightOutput:
    version: str
    diagnostics: List[PyrightDiagnostic]
    time: datetime
    files_analyzed: int
    error_count: int
    warning_count: int
    information_count: int
    time_in_sec: float

    @classmethod
    def from_dict(cls, d: dict):
        """Convert a dict, as per `pyright --outputjson`, to a PyrightOutput instance.

        Args:
            d: A dict, as per `pyright --outputjson`.

        Returns:
            A PyrightOutput instance.
        """
        summary = d.pop("summary")
        d["diagnostics"] = [
            PyrightDiagnostic.from_dict(diag) for diag in d.pop("generalDiagnostics")
        ]
        d["time"] = datetime.fromtimestamp(float(d["time"]) / 1000)
        d["files_analyzed"] = int(summary["filesAnalyzed"])
        d["error_count"] = int(summary["errorCount"])
        d["warning_count"] = int(summary["warningCount"])
        d["information_count"] = int(summary["informationCount"])
        d["time_in_sec"] = float(summary["timeInSec"])
        return cls(**d)

    def by_file(self) -> Dict[Path, Tuple[PyrightDiagnostic]]:
        """Return a dict of diagnostics, grouped by file.

        Returns:
            A dict of diagnostics, grouped by file.
        """
        out = defaultdict(list)
        for diag in self.diagnostics:
            out[diag.file].append(diag)

        out_tup: Dict[Path, Tuple[PyrightDiagnostic]] = {}
        for file, diags in out.items():
            out_tup[file] = tuple(diags)
        return out_tup

    def file_info(self):

        for file, diags in self.by_file().items():
            yield Text.from_markup(
                f"[green]--------- [bold]{file}[/bold] ---------[/]",
                justify="center",
            )
            for diag in diags:
                yield diag

    def stats_panel_renderable(self):
        """Return a renderable for the stats panel."""

        s_error = "error" if self.error_count == 1 else "errors"
        s_warning = "warning" if self.warning_count == 1 else "warnings"
        s_info = "message" if self.information_count == 1 else "messages"

        count_error = self.error_count if self.error_count > 0 else "No"
        count_warning = self.warning_count if self.warning_count > 0 else "No"
        count_info = self.information_count if self.information_count > 0 else "No"

        return Panel(
            Text("\t", justify="center", end="").join(
                [
                    Text.from_markup(
                        f"[bold]{self.files_analyzed}[/] files analyzed in "
                        f"[bold]{self.time_in_sec:.3f}[/bold] seconds",
                        end="",
                    ),
                    Text.from_markup(f"[bold red]{count_error} {s_error}", end=""),
                    Text.from_markup(f"[bold yellow]{count_warning} {s_warning}", end=""),
                    Text.from_markup(f"[bold blue]{count_info} information {s_info}", end=""),
                ]
            ),
        )

    def __rich_console__(self, console, options):
        """Render the output to the console."""
        yield f"pyright {self.version}"

        yield Padding(Group(*self.file_info()), (1, 2))
        yield self.stats_panel_renderable()


async def pyright_watcher() -> AsyncIterable[PyrightOutput]:
    """Watch pyright for changes.

    Yields:
        A dict, as per `pyright --outputjson`.
    """
    proc = await asyncio.create_subprocess_exec(
        "pyright",
        "--watch",
        "--outputjson",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    assert proc.stdout is not None
    lns = []
    async for line in proc.stdout:
        assert isinstance(line, bytes)
        lns.append(line)
        if line == b"}\n":
            yield PyrightOutput.from_dict(json.loads(b"".join(lns)))
            lns = []


def watch() -> None:
    async def main() -> None:
        with Live(auto_refresh=False, screen=True) as live:
            live.update(
                Panel(
                    Align(Text("Starting pyright...", justify="center"), vertical="middle"),
                    expand=True,
                ),
                refresh=True,
            )
            async for output in pyright_watcher():
                live.update(output, refresh=True)

    asyncio.run(main())


if __name__ == "__main__":
    # y: float = "boo"
    # x: int = 4.5
    z: int = 4.5
    watch()


__all__ = (
    "pyright_watcher",
    "PyrightDiagnostic",
    "PyrightOutput",
    "watch",
)
