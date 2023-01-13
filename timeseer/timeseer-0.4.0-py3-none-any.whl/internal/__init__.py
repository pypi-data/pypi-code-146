"""Implementation details for the Timeseer Client.

Only use classes and functions defined in timeseer_client."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Protocol

import pyarrow as pa


class AugmentationStrategy(Enum):
    """AugmentationStrategy dictates what happens to filtered data points while augmenting based on event frames."""

    REMOVE = "remove values"
    HOLD_LAST = "hold last value"
    LINEAR_INTERPOLATION = "linear interpolation"
    KNN_IMPUTATION = "knn imputation"
    MEAN = "mean"


class TimeseerClientException(Exception):
    """Base class for Timeseer client exceptions.

    Use this to catch any exception that originates in the client."""


class AugmentationException(TimeseerClientException):
    """Exception raised when augmentation strategy fails."""


class UnknownAugmentationStrategyException(TimeseerClientException):
    """Raised when the augmentation strategy is not known."""


class MissingModuleException(TimeseerClientException):
    """Raised when a required Python module is not available."""

    def __init__(self, module_name: str):
        TimeseerClientException.__init__(
            self,
            f'missing Python package: "{module_name}"',
        )


class TimeoutException(TimeseerClientException):
    """Raised when a specified timeout is exceeded."""


class ProcessType(Enum):
    """ProcessType represents the process type of a time series."""

    CONTINUOUS = "CONTINUOUS"
    REGIME = "REGIME"
    BATCH = "BATCH"
    COUNTER = "COUNTER"


@dataclass
class Statistic:
    """Statistic represents a statistics that has been calculated.

    Statistics have a name and data type and contain a result that is specific per data type."""

    name: str
    data_type: str
    result: Any

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        """Create a Statistic from a data dictionary."""
        name: str = data["name"]
        data_type: str = data["dataType"]
        if data_type == "datetime":
            result: Any = datetime.fromisoformat(data["result"])
        else:
            result = data["result"]
        return Statistic(name, data_type, result)


class JSONFlightClient(Protocol):
    """Arrow Flight Client that uses JSON for actions."""

    def do_action(self, name: str, data: Any) -> Any:
        """Perform an Arrow Flight action with the given data provided as JSON."""

    def do_get(self, data: Any) -> pa.Table:
        """Return an Arrow Tabel for the given JSON-encoded ticket."""

    def do_put(self, data: Any, table: pa.Table) -> Any:
        """Do an Arrow Flight PUT request to upload an Arrow table."""
