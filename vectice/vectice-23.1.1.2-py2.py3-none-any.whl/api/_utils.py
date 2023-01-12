from __future__ import annotations

import os
from datetime import datetime

from dotenv import dotenv_values, find_dotenv


def read_nodejs_date(date_as_string: str | None) -> datetime | None:
    if date_as_string is None:
        return None
    return datetime.strptime(date_as_string, "%Y-%m-%dT%H:%M:%S.%f%z")


def calculate_duration(endDate: datetime, startDateNodeJsFormat: str) -> int:
    # format sample : 2021-06-20T11:04:16.249Z
    startDate = read_nodejs_date(startDateNodeJsFormat)
    if startDate is None:
        raise RuntimeError("Invalid date format for value: " + startDateNodeJsFormat)
    duration = endDate - startDate
    return int(duration.total_seconds())


def read_env(*args: str) -> list[str | None]:
    """
    Read configurations in the order: .vectice file > .env file > environment variables.
    As usual, System variables always take precedence over dotenv files
    And as expected, dotenv file take precedence over dotvectice files.
    """
    if len(args) == 0:
        raise ValueError("At least one argument must be provided to read.")
    config: dict[str, str | None] = {
        **dotenv_values(find_dotenv(".vectice")),
        **dotenv_values(find_dotenv(".env")),
        **os.environ,
    }
    return [config.get(key) for key in args]
