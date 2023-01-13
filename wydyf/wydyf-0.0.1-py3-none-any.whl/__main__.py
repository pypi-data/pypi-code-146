from pathlib import Path

import click
import pandas as pd
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from .account import read_accounts, set_accounts
from .define import DEFAULT_PREFIX, DEFAULT_README_FILEPATH, NAME
from .feedback import process_feedback, read_feedback


@click.command(name="wydyf", context_settings={"show_default": True})
@click.option(
    "-p",
    "--prefix",
    type=click.Path(exists=False, file_okay=False, dir_okay=True, writable=True),
    default=DEFAULT_PREFIX,
)
def main(prefix: str | Path) -> None:
    prefix = Path(prefix)

    with Progress(
        TextColumn("{task.description}", style="bold bright_green"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        accounts = read_accounts()
        set_accounts(accounts=accounts, prefix=prefix, progress=progress)

        readme: str = DEFAULT_README_FILEPATH.read_text()
        feedback: pd.DataFrame = read_feedback()
        process_feedback(name=NAME, df=feedback, readme=readme, prefix=prefix)
        groups = feedback.groupby(by="志愿者")
        for raw_name, df in progress.track(
            sequence=groups, description="Processing Data"
        ):
            name: str = str(raw_name)
            process_feedback(name=name, df=df, readme=readme, prefix=prefix / name)
            df.drop(columns=["您的姓名"]).to_csv(prefix / name / f"{name}.csv")


if __name__ == "__main__":
    main()
