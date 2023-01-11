from typing import Mapping, Optional, Sequence, Union

import pandas as pd

from truera.client.ingestion_client import Table
from truera.client.intelligence.data_profiler import DataProfiler
from truera.client.public.communicator.http_communicator import \
    NotSupportedError


class LocalDataProfiler(DataProfiler):

    def __init__(self):
        pass

    def get_data_quality_metrics(
        self,
        feature_name: Optional[str] = None,
        metric_name: Optional[str] = None,
        comparison_data_splits: Optional[Sequence[str]] = None,
        normalize: bool = False
    ) -> Mapping[str, Union[pd.Series, pd.DataFrame]]:
        raise NotSupportedError(
            "Data quality operations currently are not supported in local projects."
        )

    def plot_data_quality_metrics(
        self,
        feature_name: str,
        metric_name: str,
        comparison_data_splits: Optional[Sequence[str]] = None,
        normalize: bool = False
    ) -> None:
        raise NotSupportedError(
            "Data quality operations currently are not supported in local projects."
        )

    def get_data_quality_metrics_definition(
        self,
        feature_name: str,
        metric_name: Optional[str] = None,
    ) -> Union[str, Mapping[str, str]]:
        raise NotSupportedError(
            "Data quality operations currently are not supported in local projects."
        )

    def update_data_quality_metric_constraint(
        self,
        feature_name: str,
        metric_name: str,
        *,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        categorical_values: Optional[Sequence] = None
    ) -> None:
        raise NotSupportedError(
            "Data quality operations currently are not supported in local projects."
        )

    def get_data_quality_rule_threshold_and_operator(
        self,
        feature_name: str,
        metric_name: Optional[str] = None
    ) -> Mapping[str, Mapping[str, str]]:
        raise NotSupportedError(
            "Data quality operations currently are not supported in local projects."
        )

    def update_data_quality_rule_threshold_and_operator(
        self,
        feature_name: str,
        metric_name: str,
        violation_threshold: float,
        operator: str,
        treat_threshold_as_raw_count: bool = False
    ) -> None:
        raise NotSupportedError(
            "Data quality operations currently are not supported in local projects."
        )

    def initialize_data_quality_constraints_from_data_split(
        self, data_split_name: str, overwrite: bool = False
    ) -> None:
        raise NotSupportedError(
            "Data quality operations currently are not supported in local projects."
        )

    def compute_feature_drift(
        self,
        comparison_data_splits: Sequence[str],
        feature_names: Optional[Sequence[str]] = None,
        distance_metrics: Optional[Sequence[str]] = None
    ) -> Mapping[str, pd.DataFrame]:
        raise NotSupportedError(
            "Data drift functionalities currently are not supported in local projects."
        )

    def plot_feature_drift(
        self,
        comparison_data_splits: Sequence[str],
        distance_metric: str,
        feature_names: Optional[Sequence[str]] = None,
        minimum_score: int = 0.0
    ) -> None:
        raise NotSupportedError(
            "Data drift functionalities currently are not supported in local projects."
        )

    def get_schema_mismatch_rows_for_split(
        self,
        data_kind_str: str,
        data_split_name: str = None,
        *,
        feature_name: Optional[str] = None
    ) -> pd.DataFrame:
        raise NotSupportedError(
            "Schema mismatch functionalities currently are not supported in local projects."
        )
