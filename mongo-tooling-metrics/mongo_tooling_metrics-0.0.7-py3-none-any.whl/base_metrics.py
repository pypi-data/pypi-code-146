from __future__ import annotations
from abc import abstractmethod
import sys
from pydantic import BaseModel
from mongo_tooling_metrics import register_hook

from mongo_tooling_metrics.errors import InvalidMetricsSetup
from mongo_tooling_metrics.lib.hooks import ExitHook
from mongo_tooling_metrics.lib.utils import should_collect_internal_metrics


class TopLevelMetrics(BaseModel):
    """Base class for a top-level metrics objects."""

    @classmethod
    @abstractmethod
    def generate_metrics(cls, *args, **kwargs) -> TopLevelMetrics:
        """Class method to generate this metrics object -- will be executed before process exit."""
        raise InvalidMetricsSetup(
            "'generate_metrics' will be used to construct the top-level metrics object and must be defined."
        )

    @staticmethod
    def should_collect_metrics() -> bool:
        """Determine whether metrics collection should even be registered or not."""
        # Default to collecting metrics on internal MongoDB virtual workstations only -- this can be overwritten.
        return should_collect_internal_metrics()

    @staticmethod
    def initialize_hooks() -> None:
        """Initialize any hooks that these metrics rely on here -- this will get called after the metrics are registered."""
        # Default to registering the ExitHook -- this can be overwritten.
        sys.exit = register_hook(ExitHook(original_fn=sys.exit))

    def is_malformed(self) -> bool:
        """Determine whether these metrics are malformed (have all expected fields/data)."""
        # Default to metrics not being malformed -- this can be overwritten.
        return False


class SubMetrics(BaseModel):
    """Base class for sub-level metrics objects."""

    @classmethod
    @abstractmethod
    def generate_metrics(cls, *args, **kwargs) -> SubMetrics:
        """Class method to generate this metrics object -- will be executed before process exit."""
        raise InvalidMetricsSetup(
            "'generate_metrics' should be used to construct the sub-metrics object and must be defined."
        )

    def is_malformed(self) -> bool:
        """Determine whether these metrics are malformed (have all expected fields/data)."""
        return False
