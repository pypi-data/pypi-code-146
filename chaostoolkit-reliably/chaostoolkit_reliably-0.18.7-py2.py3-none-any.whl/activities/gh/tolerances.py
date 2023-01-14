from typing import List, Optional, Union, cast

from boltons import statsutils
from chaoslib.exceptions import InvalidActivity
from logzero import logger

from chaosreliably import parse_duration

__all__ = ["ratio_under", "ratio_above", "percentile_under"]


def ratio_under(target: float, value: float = 0.0) -> bool:
    """
    Validates the ratio returned by a probe is strictly below the `target`.
    """
    logger.debug(f"Verify that ratio is below: {target}")
    return value < target


def ratio_above(target: float, value: float = 0.0) -> bool:
    """
    Validates the ratio returned by a probe is strictly greater than the
    `target`.
    """
    logger.debug(f"Verify that ratio is above: {target}")
    return value > target


def percentile_under(
    percentile: float,
    duration: str = "1d",
    value: Optional[List[Union[int, float]]] = None,
) -> bool:
    """
    Computes that the values under `percentile` are below the given duration.

    For instance, for PR durations, this could be helpful to understand that
    99% of them were closed in less than the given duration.

    ```python
    v = pr_duration("chaostoolkit/chaostoolkit", "master", window=None)
    p = percentile_under(0.99, duration="1d", value=v)
    ```
    """
    if not (0.0 <= percentile <= 1.0):
        raise InvalidActivity(
            "`percentile` of the `percentile_under` tolerance "
            "must be below 0 and 99"
        )

    if not value:
        return True

    d = parse_duration(duration).total_seconds()
    s = statsutils.Stats(value)
    q = cast(float, s.get_quantile(percentile))

    logger.debug(f"Stats summary:\n{s.describe(format='text')}")

    return q <= d
