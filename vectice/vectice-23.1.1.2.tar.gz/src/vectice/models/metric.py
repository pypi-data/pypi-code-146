from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Metric:
    """Define a metric for a model or a dataset.

    :param key: the key to identify the metric
    :param value: the value of the metric
    :param timestamp: the timestamp of the metric. Corresponds to the metric creation time if not explicitly passed.
    :param name: the name of the metric
    """

    key: str
    value: int | float
    timestamp: datetime | str = datetime.now(timezone.utc).isoformat()
    name: str | None = None

    def __post_init__(self):
        if not (isinstance(self.value, int) or isinstance(self.value, float)):
            raise TypeError(
                f"Metric '{self.key}' value must have type float or integer, not {type(self.value).__name__}."
            )

    def __repr__(self) -> str:
        return f"Metric(key='{self.key}', value={self.value})"
