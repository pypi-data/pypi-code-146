from __future__ import annotations

import collections.abc
import dataclasses
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Set

if TYPE_CHECKING:
    from chalk.features.feature_field import Feature


__all__ = ["Filter", "before", "after", "TimeDelta"]


class Filter:
    def __init__(self, lhs: Any, operation: str, rhs: Any):
        from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature

        # Feature or other could be another feature, filter, featuretime, literal
        # Other could also be a sequence (in the case of operation = "in")
        self.operation = operation
        if isinstance(lhs, FeatureWrapper):
            lhs = unwrap_feature(lhs)
        self.lhs = lhs
        if self.operation == "in":
            if not isinstance(rhs, collections.abc.Iterable):
                raise ValueError("The RHS must be an iterable for operation='in'")
            rhs = {unwrap_feature(x) if isinstance(x, FeatureWrapper) else x for x in rhs}
        else:
            if isinstance(rhs, FeatureWrapper):
                rhs = unwrap_feature(rhs)
        self.rhs = rhs

    def __hash__(self) -> int:
        return hash((self.lhs, self.operation, self.rhs))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Filter):
            return NotImplemented
        return self.lhs == other.lhs and self.operation == other.operation and self.rhs == other.rhs

    def __and__(self, other: object):
        return Filter(self, "and", other)

    def __or__(self, other: object):
        return Filter(self, "or", other)

    def __invert__(self):
        return Filter(self, "not", None)

    def __bool__(self):
        # If the operation is == or !=, then compare the underlying filters or features
        # If x and y are features, then (x == y) is overloaded to return a Filter
        # This allows bool(x == y) to return True iff the x is y, while (x == y) is still a Filter instance
        # If either side is a FeatureWrapper
        # If either side is a Filter or a FeatureWrapper,
        if self.operation == "==":
            return self.lhs == self.rhs
        if self.operation == "!=":
            return self.lhs != self.rhs
        # Non-equality comparisons must be evaluated manually -- e.g. if x and y are Features
        # (x < y) would return a Filter, but bool(x < y) doesn't really make sense. So, raise.
        raise TypeError(f"Operation {self.operation} on a Filter is undefined")

    def referenced_features(self) -> Set[Feature]:
        from chalk.features.feature_field import Feature

        return {x for x in (self.lhs, self.rhs) if isinstance(x, Feature)}

    def __repr__(self):
        return f"Filter({self.lhs} {self.operation} {self.rhs})"


@dataclasses.dataclass(frozen=True)
class TimeDelta:
    weeks_ago: int = 0
    days_ago: int = 0
    hours_ago: int = 0
    minutes_ago: int = 0
    seconds_ago: int = 0
    milliseconds_ago: int = 0
    microseconds_ago: int = 0

    def to_std(self) -> timedelta:
        # Returning the negative inverse since the feature is defined in the past (e.g. days **ago**)
        return -timedelta(
            weeks=self.weeks_ago,
            days=self.days_ago,
            hours=self.hours_ago,
            minutes=self.minutes_ago,
            seconds=self.seconds_ago,
            milliseconds=self.milliseconds_ago,
            microseconds=self.microseconds_ago,
        )


def before(
    weeks_ago: int = 0,
    days_ago: int = 0,
    hours_ago: int = 0,
    minutes_ago: int = 0,
    seconds_ago: int = 0,
    milliseconds_ago: int = 0,
    microseconds_ago: int = 0,
) -> Any:
    from chalk.features.pseudofeatures import CHALK_TS_FEATURE

    return Filter(
        lhs=CHALK_TS_FEATURE,
        operation="<=",
        rhs=TimeDelta(
            weeks_ago=weeks_ago,
            days_ago=days_ago,
            hours_ago=hours_ago,
            minutes_ago=minutes_ago,
            seconds_ago=seconds_ago,
            milliseconds_ago=milliseconds_ago,
            microseconds_ago=microseconds_ago,
        ),
    )


def after(
    weeks_ago: int = 0,
    days_ago: int = 0,
    hours_ago: int = 0,
    minutes_ago: int = 0,
    seconds_ago: int = 0,
    milliseconds_ago: int = 0,
    microseconds_ago: int = 0,
) -> Any:
    from chalk.features.pseudofeatures import CHALK_TS_FEATURE

    return Filter(
        lhs=CHALK_TS_FEATURE,
        operation=">=",
        rhs=TimeDelta(
            weeks_ago=weeks_ago,
            days_ago=days_ago,
            hours_ago=hours_ago,
            minutes_ago=minutes_ago,
            seconds_ago=seconds_ago,
            milliseconds_ago=milliseconds_ago,
            microseconds_ago=microseconds_ago,
        ),
    )
