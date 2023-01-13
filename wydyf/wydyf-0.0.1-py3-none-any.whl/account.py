import os
from concurrent.futures import Future, ProcessPoolExecutor
from pathlib import Path
from typing import Optional

import pandas as pd
from rich.progress import Progress, TaskID

from .define import DEFAULT_ACCOUNT_FILEPATH, DEFAULT_PASSFILE, DEFAULT_PREFIX


def read_accounts(filepath: str | Path = DEFAULT_ACCOUNT_FILEPATH) -> dict[str, str]:
    df = pd.read_excel(filepath)
    accounts = dict(zip(df["1、您的姓名"], df["2、密码"]))
    return accounts


def set_account(name: str, password: str, prefix: str | Path = DEFAULT_PREFIX) -> None:
    prefix = Path(prefix)
    os.makedirs(name=prefix / name, exist_ok=True)
    with open(file=prefix / name / DEFAULT_PASSFILE, mode="w") as fp:
        fp.write(password)


def set_accounts(
    accounts: dict[str, str],
    prefix: str | Path = DEFAULT_PREFIX,
    progress: Optional[Progress] = None,
) -> None:
    if progress:
        task_id: TaskID = progress.add_task(
            description="Setting Up Accounts", total=len(accounts)
        )

    def callback(future: Future) -> None:
        if progress:
            progress.advance(task_id=task_id)

    with ProcessPoolExecutor() as executor:
        for name, password in accounts.items():
            future = executor.submit(
                set_account, name=name, password=password, prefix=prefix
            )
            if progress:
                future.add_done_callback(fn=callback)
