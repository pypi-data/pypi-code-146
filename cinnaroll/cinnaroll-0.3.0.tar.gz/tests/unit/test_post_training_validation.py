from typing import Any, Dict

import pytest

from cinnaroll_internal.post_training_validation import (
    find_metrics_post_training_errors,
    MetricsError,
)
from tests.unit import utils


class TestPostTrainingValidation:
    @pytest.mark.parametrize(
        "metrics,expected_outcome",
        [
            ({}, []),
            (
                {"dataset": "mnist_extended", "f1": 0.7, "accuracy": 0.9},
                [],
            ),
            (
                {"dataset": "mnist_extended", "f1": None},
                [
                    MetricsError(
                        "All values in the metrics dictionary must be floats."
                    ),
                    MetricsError(
                        "Values in the metrics dictionary cannot be None or empty strings."
                    ),
                ],
            ),
            (
                {"dataset": "mnist_extended", "f1": [0, 1, 2]},
                [
                    MetricsError(
                        "All values in the metrics dictionary must be floats, "
                        "except for optional 'dataset' key value which must be string."
                    )
                ],
            ),
            (
                {"dataset": "mnist_extended", "f1": (0.3,)},
                [
                    MetricsError(
                        "All values in the metrics dictionary must be floats, "
                        "except for optional 'dataset' key value which must be string."
                    )
                ],
            ),
            (
                {"dataset": "mnist_extended", "f1": {"test": 0.5, "train": 0.7}},
                [
                    MetricsError(
                        "All values in the metrics dictionary must be floats, "
                        "except for optional 'dataset' key value which must be string."
                    )
                ],
            ),
            (
                ["zaba", "pies"],
                [MetricsError("Object passed as metrics must be a dictionary.")],
            ),
            (
                {"dataset": "mnist_extended", 2: "zaba"},
                [MetricsError("All keys in the metrics dictionary must be strings.")],
            ),
        ],
    )
    def test_find_metrics_post_training_errors(
        self, metrics: Dict[str, Any], expected_outcome: Any
    ) -> None:
        utils.assert_list_exceptions_type_equality(
            expected_outcome, find_metrics_post_training_errors(metrics)
        )
