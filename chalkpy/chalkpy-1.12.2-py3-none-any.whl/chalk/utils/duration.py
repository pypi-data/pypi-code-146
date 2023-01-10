import re
from datetime import timedelta
from re import Pattern
from typing import Literal, Mapping, Optional, Tuple, Union

# Duration is used to describe time periods in
# natural langauge. To specify using natural
# language, write the count of the unit you would
# like, followed by the representation of the unit.
#
# Chalk support the following units:
# | Signifier | Meaning  |
# | --------- | -------- |
# | w         | Weeks    |
# | d         | Days     |
# | h         | Hours    |
# | m         | Minutes  |
# | s         | Seconds  |
#
# As well as the special keyword "infinity"
#
# Examples
# | Signifier   | Meaning                           |
# | ----------- | --------------------------------- |
# | "10h"       | 10 hours                          |
# | "1w 2m"     | 1 week and 2 minutes              |
# | "1h 10m 2s" | 1 hour, 10 minutes, and 2 seconds |
# | "infinity"  | Unbounded time duration           |
#
# Read more at https://docs.chalk.ai/docs/duration
Duration = Union[str, timedelta]

# A schedule defined using the unix-cron
# string format (* * * * *).
# Values are given in the order below:
#
# | Field        | Values |
# | ------------ | ------ |
# | Minute       | 0-59   |
# | Hour         | 0-23   |
# | Day of Month | 1-31   |
# | Month        | 1-12   |
# | Day of Week  | 0-6    |
CronTab = str
ScheduleOptions = Optional[Union[CronTab, Duration, Literal[True]]]


def timedelta_to_duration(t: timedelta) -> Duration:
    s = ""
    if t.days > 0:
        s += f"{t.days}d"
    if t.seconds > 0:
        if len(s) > 0:
            s += " "
        s += f"{t.seconds}s"
    return s


_kwarg_to_regex: Mapping[str, Pattern] = {
    k: re.compile(f"(([0-9]+?){v})")
    for k, v in dict(
        weeks="w",
        days="d",
        hours="h",
        minutes="m",
        seconds="s",
    ).items()
}


def parse_chalk_duration(s: str) -> timedelta:
    def parse(regex: Pattern) -> Tuple[int, str]:
        matched = regex.search(s)
        if matched is None:
            return 0, ""

        return int(matched.groups()[1]), matched.groups()[0]

    parsed_values = {k: parse(unit) for k, unit in _kwarg_to_regex.items()}

    # Check for remaining unparsed input
    remainder = s
    for v in parsed_values.values():
        remainder = remainder.replace(v[1], "", 1)
    remainder = remainder.strip()

    if remainder != "":
        raise ValueError(f"Unparsed portion of duration: '{remainder}' for input: '{s}'")

    return timedelta(**{k: v[0] for k, v in parsed_values.items()})
