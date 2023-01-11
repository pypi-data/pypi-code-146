from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Optional, Sequence, Tuple, TYPE_CHECKING

from truera.protobuf.public.modeltest import modeltest_pb2

if TYPE_CHECKING:
    from truera.client.intelligence.model_tests import ModelTestDetails
    from truera.client.intelligence.model_tests import ModelTestLeaderboard
    from truera.client.intelligence.model_tests import ModelTestResults

SUPPORTED_TEST_TYPES = [
    "performance", "fairness", "stability", "feature_importance"
]


class Tester(ABC):

    TEST_TYPE_STRING_TO_MODEL_TEST_TYPE_ENUM = {
        "performance": modeltest_pb2.MODEL_TEST_TYPE_PERFORMANCE,
        "stability": modeltest_pb2.MODEL_TEST_TYPE_STABILITY,
        "fairness": modeltest_pb2.MODEL_TEST_TYPE_FAIRNESS,
        "feature_importance": modeltest_pb2.MODEL_TEST_TYPE_FEATURE_IMPORTANCE
    }

    def _validate_test_types(
        self, test_types: Optional[Sequence[str]]
    ) -> Sequence[str]:
        if test_types is None:
            return SUPPORTED_TEST_TYPES
        for curr in test_types:
            if curr not in SUPPORTED_TEST_TYPES:
                raise ValueError(
                    f"{curr} not a valid test-type! Must be one of {SUPPORTED_TEST_TYPES}"
                )
        return test_types

    @abstractmethod
    def add_performance_test(
        self,
        test_name: str,
        metric: str,
        *,
        data_split_names: Optional[Sequence[str]] = None,
        data_split_name_regex: Optional[str] = None,
        data_collection_names: Optional[Sequence[str]] = None,
        all_data_collections: bool = False,
        segments: Optional[Sequence[Tuple[str, str]]] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        warn_threshold_type: str = "ABSOLUTE",
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        fail_threshold_type: str = "ABSOLUTE",
        reference_split_name: Optional[str] = None,
        reference_model_name: Optional[str] = None,
        description: Optional[str] = None,
        overwrite: bool = False
    ) -> None:
        """Add a performance test group to the current data collection in context. To set warning condition, please provide one of [`warn_if_less_than`, `warn_if_greater_than`, `warn_if_within`, `warn_if_outside`].
        Similarly, to set fail condition please provide one of [`fail_if_less_than`, `fail_if_greater_than`, `fail_if_within`, `fail_if_outside`].

        Args:
            test_name: The name of the test.
            metric: Performance metric for the test. Must be one of the options returned by `list_performance_metrics`.
            data_split_names: List of the data splits that we want to use for the test.
            data_split_name_regex: Regex of the data split name that we want to use for the test (future data splits that match this naming pattern will automatically be included in the test).
            data_collection_names: List of the data collections for the test. If not specified, the test will only apply to the current data collection in context.
            all_data_collections: If set to `True`, the test will apply to all data collections (including future ones). Defaults to `False` which means the test will only apply to the current data collection in context (if `data_collection_names` is not specified).
            segments: List of `(segment_group_name, segment_name)` tuple to be used as filter. A test will be defined on each of the given segment filters.
            warn_if_less_than: Warn if score is less than the value specified in this argument.
            warn_if_greater_than: Warn if score is greater than the value specified in this argument.
            warn_if_within: Warn if `value[0] < score < value[1]`.
            warn_if_outside: Warn if `score < value[0] OR score > value[1]`.
            warn_threshold_type: Must be one of ["ABSOLUTE", "RELATIVE"]. Describe whether the warning threshold is defined as absolute value or relative to split in `reference_split_name`. If it's relative, the effective threshold is `score_of_reference_split * (1 + value)`. Defaults to "ABSOLUTE".
            fail_if_less_than: Fail if score is less than the value specified in this argument.
            fail_if_greater_than: Fail if score is greter than the value specified in this argument.
            fail_if_within: Fail if `value[0] < score < value[1]`.
            fail_if_outside: Fail if `score < value[0] OR score > value[1]`.
            fail_threshold_type: Must be one of ["ABSOLUTE", "RELATIVE"]. Describe whether the fail threshold is defined as absolute value or relative to split in `reference_split_name`. If it's relative, the effective threshold is `score_of_reference_split * (1 + value)`. Defaults to "ABSOLUTE".
            reference_split_name: Name of the reference split used for the "RELATIVE" threshold type. If not specified and `reference_model_name` is also not provided, the relative threshold will be calculated with respect to each models' train split (for models whose train split is not specified, then those will be treated as if no thresholds were specified).
            reference_model_name: Name of the reference model used for the "RELATIVE" threshold type.
            description: Text description of the test.
            overwrite: If set to `True`, will overwrite the thresholds for existing test specified under the given data_split_name, segment, and metric. Defaults to `False`.
        """
        pass

    @abstractmethod
    def add_stability_test(
        self,
        test_name: str,
        metric: str = "DIFFERENCE_OF_MEAN",
        *,
        comparison_data_split_names: Optional[Sequence[str]] = None,
        comparison_data_split_name_regex: Optional[str] = None,
        base_data_split_name: Optional[str] = None,
        data_collection_names: Optional[Sequence[str]] = None,
        all_data_collections: bool = False,
        segments: Optional[Sequence[Tuple[str, str]]] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        description: Optional[str] = None,
        overwrite: bool = False
    ) -> None:
        """Add a stability test to the current data collection in context. To set warning condition, please provide one of [`warn_if_less_than`, `warn_if_greater_than`, `warn_if_within`, `warn_if_outside`].
        Similarly, to set fail condition please provide one of [`fail_if_less_than`, `fail_if_greater_than`, `fail_if_within`, `fail_if_outside`].

        Args:
            test_name: The name of the test.
            metric: Stability metric for the test. Must be one ["WASSERSTEIN", "DIFFERENCE_OF_MEAN", "POPULATION_STABILITY_INDEX"]
            comparison_data_split_names: List of the data splits that we want to use for the test.
            comparison_data_split_name_regex: Regex of the data split name that we want to use for the test (future data splits that match this naming pattern will automatically be included in the test).
            base_data_split_name: Name of the reference data split to use as the comparison baseline for the test. If `None`, will be the model's train split.
            data_collection_names: List of the data collections for the test. If not specified, the test will only apply to the current data collection in context.
            all_data_collections: If set to `True`, the test will apply to all data collections (including future ones). Defaults to `False` which means the test will only apply to the current data collection in context (if `data_collection_names` is not specified).
            segments: List of `(segment_group_name, segment_name)` tuple to be used as filter. A test will be defined on each of the given segment filters.
            warn_if_less_than: Warn if score is less than the value specified in this argument.
            warn_if_greater_than: Warn if score is greater than the value specified in this argument.
            warn_if_within: Warn if `value[0] < score < value[1]`.
            warn_if_outside: Warn if `score < value[0] OR score > value[1]`.
            fail_if_less_than: Fail if score is less than the value specified in this argument.
            fail_if_greater_than: Fail if score is greter than the value specified in this argument.
            fail_if_within: Fail if `value[0] < score < value[1]`.
            fail_if_outside: Fail if `score < value[0] OR score > value[1]`.
            description: Text description of the test.
            overwrite: If set to `True`, will overwrite the thresholds for existing test specified under the given comparison_data_split_name, segment, and metric. Defaults to `False`.
        """
        pass

    @abstractmethod
    def add_fairness_test(
        self,
        test_name: str,
        metric: str = "DISPARATE_IMPACT_RATIO",
        *,
        data_split_names: Optional[Sequence[str]] = None,
        data_split_name_regex: Optional[str] = None,
        all_protected_segments: bool = False,
        protected_segments: Optional[Sequence[Tuple[str, str]]] = None,
        comparison_segments: Optional[Sequence[Tuple[str, str]]] = None,
        data_collection_names: Optional[Sequence[str]] = None,
        all_data_collections: bool = False,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        description: Optional[str] = None,
        overwrite: bool = False
    ) -> None:
        """Add a fairness test to the current data collection in context. To set warning condition, please provide one of [`warn_if_less_than`, `warn_if_greater_than`, `warn_if_within`, `warn_if_outside`].
        Similarly, to set fail condition please provide one of [`fail_if_less_than`, `fail_if_greater_than`, `fail_if_within`, `fail_if_outside`].

        Args:
            test_name: The name of the test.
            metric: Fairness metric for the test. Must be one of the options returned by `list_fairness_metrics`.
            data_split_names: List of the data splits that we want to use for the test.
            all_protected_segments: If set to `True`, the test will apply to all protected segments (including future ones). Defaults to `False` which means the test will only apply to the protected segments specified in `protected_segments`.
            protected_segments: List of `(segment_group_name, segment_name)` tuple to be used as protected segments.
            comparison_segments: List of `(segment_group_name, segment_name)` tuple to be used as comparison segments. Defaults to `None` which means the complement of the protected segment.
            data_collection_names: List of the data collections for the test. If not specified, the test will only apply to the current data collection in context.
            all_data_collections: If set to `True`, the test will apply to all data collections (including future ones). Defaults to `False` which means the test will only apply to the current data collection in context (if `data_collection_names` is not specified).
            warn_if_less_than: Warn if score is less than the value specified in this argument.
            warn_if_greater_than: Warn if score is greater than the value specified in this argument.
            warn_if_within: Warn if `value[0] < score < value[1]`.
            warn_if_outside: Warn if `score < value[0] OR score > value[1]`.
            fail_if_less_than: Fail if score is less than the value specified in this argument.
            fail_if_greater_than: Fail if score is greter than the value specified in this argument.
            fail_if_within: Fail if `value[0] < score < value[1]`.
            fail_if_outside: Fail if `score < value[0] OR score > value[1]`.
            description: Text description of the test.
            overwrite: If set to `True`, will overwrite the thresholds for existing test specified under the given data_split_name, segment, and metric. Defaults to `False`.
        """
        pass

    @abstractmethod
    def add_feature_importance_test(
        self,
        test_name: str,
        *,
        data_split_names: Optional[Sequence[str]] = None,
        data_split_name_regex: Optional[str] = None,
        min_importance_value: float,
        background_split_name: Optional[str] = None,
        score_type: Optional[str] = None,
        segments: Optional[Tuple[str, str]] = None,
        data_collection_names: Optional[Sequence[str]] = None,
        warn_if_greater_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        description: Optional[str] = None,
        overwrite: bool = False
    ) -> None:
        """Add a feature importance test to the current data collection in context. To set warning condition, please provide `warn_if_greater_than`. Similarly, to set fail condition please provide `fail_if_greater_than`.

        Args:
            test_name: The name of the test.
            data_split_names: List of the data splits that we want to use for the test.
            data_split_name_regex: Regex of the data split name that we want to use for the test (future data splits that match this naming pattern will automatically be included in the test).
            min_importance_value: Minimum global importance value of a feature.
            background_split_name: The name of the data split to be used as background data for computing feature influences. If None, this value will be inferred from the project settings. Defaults to None.
            score_type: The score type to use when computing influences. If None, this value will be inferred from the project settings. Defaults to None. For a list of valid score types, see `list_valid_score_types`.
            segments: List of `(segment_group_name, segment_name)` tuple to be used as filter. A test will be defined on each of the given segment filters.
            warn_if_greater_than: Warn if more than this number of features have global importance values lower than `min_importance_value`.
            fail_if_greater_than: Fail if more than this number of features have global importance values lower than `min_importance_value`.
            description: Text description of the test.
            overwrite: If set to `True`, will overwrite the thresholds for existing test specified under the given `data_split_name` and segment. Defaults to `False`.
        """
        pass

    @abstractmethod
    def get_model_tests(
        self, data_split_name: Optional[str] = None
    ) -> ModelTestDetails:
        """Get the details of all the model tests in the current data collection or the model tests associated with the given data split.

        Args:
            data_split_name: If provided, filters to the tests associated with this split.

        Returns:
            A `ModelTestDetails` object containing the details for each test that has been created.
            On Jupyter notebooks, this object will be displayed as a nicely formatted HTML table.
            This object also has a `pretty_print` as well as `as_json` and `as_dict` representation.
        """
        pass

    @abstractmethod
    def get_model_test_results(
        self,
        data_split_name: Optional[str] = None,
        comparison_models: Optional[Sequence[str]] = None,
        test_types: Optional[Sequence[str]] = None,
        wait: bool = True
    ) -> ModelTestResults:
        """Get the test results for the model in context.

        Args:
            data_split_name: If provided, filters to the tests associated with this split.
            comparison_models: If provided, compare the test results against this list of models.
            test_types: If provided, filter to only the given test-types. Must be a subset of ["performance", "stability", "fairness"] or None (which defaults to all). Defaults to None.
            wait: Whether to wait for test results to finish computing.

        Returns:
            A `ModelTestResults` object containing the test results for the model in context.
            On Jupyter notebooks, this object will be displayed as a nicely formatted HTML table.
            This object also has a `pretty_print` as well as `as_json` and `as_dict` representation.
        """
        pass

    @abstractmethod
    def get_model_leaderboard(
        self,
        sort_by: str = "performance",
        wait: bool = True
    ) -> ModelTestLeaderboard:
        """Get the summary of test outcomes for all models in the data collection.

        Args:
            sort_by: Rank models according to the test type specified in this arg (models with the fewest test failures will be at the top). Must be one of ["performance", "stability", "fairness"]. Defaults to "performance".
            wait: Whether to wait for test results to finish computing. Defaults to True.

        Returns:
            A `ModelTestLeaderboard` object containing the summary of test outcomes for all models in the data collection.
            On Jupyter notebooks, this object will be displayed as a nicely formatted HTML table.
            This object also has a `pretty_print` as well as `as_json` and `as_dict` representation.
        """
        pass

    @abstractmethod
    def delete_tests(
        self,
        test_name: Optional[str] = None,
        test_type: Optional[str] = None,
        data_split_name: Optional[str] = None,
        segment_group_name: Optional[str] = None,
        segment_name: Optional[str] = None,
        metric: Optional[str] = None
    ) -> None:
        """Delete tests.

        Args:
            test_name: Only delete tests with the given name.
            test_type: Only delete tests of this type. Must be one of ["performance", "stability", "fairness"] or None. If None, delete all test types. Defaults to None.
            data_split_name: Only delete tests associated with this data split. Defaults to None.
            segment_group_name: Only delete tests associated with this segment group. Defaults to None.
            segment_name: Only delete tests associated with this segment. Defaults to None.
            metric: Only delete tests associated with this metric. Defaults to None.
        """
        pass
