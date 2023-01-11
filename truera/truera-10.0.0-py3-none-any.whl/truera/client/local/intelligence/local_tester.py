from __future__ import annotations

from typing import Optional, Sequence, TYPE_CHECKING

from truera.client.intelligence.tester import Tester
from truera.client.public.communicator.http_communicator import \
    NotSupportedError

if TYPE_CHECKING:
    from truera.client.intelligence.model_tests import ModelTestDetails
    from truera.client.intelligence.model_tests import ModelTestLeaderboard
    from truera.client.intelligence.model_tests import ModelTestResults


# AB#6631: Implement this class out.
class LocalTester(Tester):

    def add_performance_test(self, *args, **kwargs):
        raise NotSupportedError(
            "Model tester operations currently are not supported in local projects."
        )

    def add_stability_test(self, *args, **kwargs):
        raise NotSupportedError(
            "Model tester operations currently are not supported in local projects."
        )

    def add_fairness_test(self, *args, **kwargs):
        raise NotSupportedError(
            "Model tester operations currently are not supported in local projects."
        )

    def add_feature_importance_test(self, *args, **kwargs):
        raise NotSupportedError(
            "Model tester operations currently are not supported in local projects."
        )

    def get_model_tests(
        self, data_split_name: Optional[str] = None
    ) -> ModelTestDetails:
        raise NotSupportedError(
            "Model tester operations currently are not supported in local projects."
        )

    def get_model_test_results(
        self,
        data_split_name: Optional[str] = None,
        comparison_models: Optional[Sequence[str]] = None,
        test_types: Optional[Sequence[str]] = None,
        wait: bool = True
    ) -> ModelTestResults:
        raise NotSupportedError(
            "Model tester operations currently are not supported in local projects."
        )

    def get_model_leaderboard(
        self,
        sort_by: str = "performance",
        wait: bool = True
    ) -> ModelTestLeaderboard:
        raise NotSupportedError(
            "Model tester operations currently are not supported in local projects."
        )

    def delete_tests(self, *args, **kwargs):
        raise NotSupportedError(
            "Model tester operations currently are not supported in local projects."
        )
