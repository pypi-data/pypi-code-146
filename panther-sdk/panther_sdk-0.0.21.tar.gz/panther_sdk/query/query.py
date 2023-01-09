# Copyright (C) 2022 Panther Labs, Inc.
#
# The Panther SaaS is licensed under the terms of the Panther Enterprise Subscription
# Agreement available at https://panther.com/enterprise-subscription-agreement/.
# All intellectual property rights in and to the Panther SaaS, including any and all
# rights to access the Panther SaaS, are governed by the Panther Enterprise Subscription Agreement.

# coding=utf-8
# *** WARNING: generated file
import typing
import functools
import dataclasses

from panther_core import PantherEvent

"""
The query module provides classes representing Panther datalake queries
"""

from .. import _utilities

__all__ = [
    "CronSchedule",
    "CronScheduleOverrides",
    "IntervalSchedule",
    "IntervalScheduleOverrides",
    "Query",
    "QueryOverrides",
    "DatalakeAthena",
    "DatalakeSnowflake",
]


DatalakeAthena = "athena"
DatalakeSnowflake = "snowflake"


class DefaultOverrides:
    pass


def overridable(cls: typing.Callable) -> typing.Callable:
    @functools.wraps(cls)
    def wrapper(
        *args: typing.Any,
        overrides: typing.Optional[
            typing.Union[
                "CronScheduleOverrides",
                "IntervalScheduleOverrides",
                "QueryOverrides",
                DefaultOverrides,
            ]
        ] = DefaultOverrides(),
        **kwargs: typing.Any,
    ) -> typing.Any:
        if overrides:  # overrides can be None
            for key, val in overrides.__dict__.items():
                kwargs[key] = val or kwargs.get(key)
        return cls(*args, **kwargs)

    return wrapper


@dataclasses.dataclass
class CronScheduleOverrides:
    """Overrides dataclass for CronSchedule. All arguments are marked optional.

    - expression -- Defines how often queries using this schedule run
    - timeout_minutes -- Defines the timeout applied to queries with this schedule
    """

    expression: typing.Optional[str] = None

    timeout_minutes: typing.Optional[int] = None


@dataclasses.dataclass(frozen=True)
class CronSchedule(_utilities.SDKNode):
    """Cron expression based schedule definition for a query (https://docs.panther.com/data-analytics/scheduled-queries)

    - expression -- Defines how often queries using this schedule run (required)
    - timeout_minutes -- Defines the timeout applied to queries with this schedule (required)
    """

    # required
    expression: str

    # required
    timeout_minutes: int

    # internal private methods
    def _typename(self) -> str:
        return "CronSchedule"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["expression", "timeout_minutes"]


@dataclasses.dataclass
class IntervalScheduleOverrides:
    """Overrides dataclass for IntervalSchedule. All arguments are marked optional.

    - rate_minutes -- Defines how often queries using this schedule run
    - timeout_minutes -- Defines the timeout applied to queries with this schedule
    """

    rate_minutes: typing.Optional[int] = None

    timeout_minutes: typing.Optional[int] = None


@dataclasses.dataclass(frozen=True)
class IntervalSchedule(_utilities.SDKNode):
    """Interval based schedule definition for a query (https://docs.panther.com/data-analytics/scheduled-queries)

    - rate_minutes -- Defines how often queries using this schedule run (required)
    - timeout_minutes -- Defines the timeout applied to queries with this schedule (required)
    """

    # required
    rate_minutes: int

    # required
    timeout_minutes: int

    # internal private methods
    def _typename(self) -> str:
        return "IntervalSchedule"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["rate_minutes", "timeout_minutes"]


@dataclasses.dataclass
class QueryOverrides:
    """Overrides dataclass for Query. All arguments are marked optional.

    - name -- Unique name for the query
    - sql -- SQL statement
    - default_database -- Default database for the query
    - description -- Short description for the query
    - enabled -- Whether the query is enabled or not
    - schedule -- Schedule attached to the query
    - tags -- Tags for the query
    """

    name: typing.Optional[str] = None

    sql: typing.Optional[str] = None

    default_database: typing.Optional[str] = None

    description: typing.Optional[str] = None

    enabled: typing.Optional[bool] = None

    schedule: typing.Optional[typing.Union[IntervalSchedule, CronSchedule]] = None

    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None


@dataclasses.dataclass(frozen=True)
class Query(_utilities.SDKNode):
    """A saved or scheduled query (https://docs.panther.com/data-analytics/scheduled-queries)

    - name -- Unique name for the query (required)
    - sql -- SQL statement (required)
    - default_database -- Default database for the query (optional, default: "")
    - description -- Short description for the query (optional, default: "")
    - enabled -- Whether the query is enabled or not (optional, default: True)
    - schedule -- Schedule attached to the query (optional, default: None)
    - tags -- Tags for the query (optional, default: None)
    """

    # required
    name: str

    # required
    sql: str

    # optional
    default_database: str = ""

    # optional
    description: str = ""

    # optional
    enabled: bool = True

    # optional
    schedule: typing.Optional[typing.Union[IntervalSchedule, CronSchedule]] = None

    # optional
    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    # internal private methods
    def _typename(self) -> str:
        return "Query"

    def _output_key(self) -> str:
        return "sdk-node:query"

    def _fields(self) -> typing.List[str]:
        return [
            "name",
            "sql",
            "default_database",
            "description",
            "enabled",
            "schedule",
            "tags",
        ]
