from __future__ import annotations

import logging
from typing import (
    Mapping, NamedTuple, Optional, Sequence, TYPE_CHECKING, Union
)

import pandas as pd

from truera.client.intelligence.data_profiler import DataProfiler
import truera.client.intelligence.viz as viz
from truera.client.public.auth_details import AuthDetails
from truera.client.services.artifact_interaction_client import \
    ArtifactInteractionClient
from truera.client.services.bad_data_client import BadDataClient
from truera.client.services.configuration_service_client import \
    ConfigurationServiceClient
from truera.client.services.data_quality_client import DataQualityClient
from truera.protobuf.public.common.data_kind_pb2 import \
    DataKindDescribed  # pylint: disable=no-name-in-module

if TYPE_CHECKING:
    from truera.client.remote_truera_workspace import RemoteTrueraWorkspace


class RemoteSplitMetadata(NamedTuple):
    split_id: str
    split_name: str
    data_collection_id: str


class RemoteDataProfiler(DataProfiler):

    def __init__(
        self, workspace: RemoteTrueraWorkspace,
        artifact_interaction_client: ArtifactInteractionClient,
        cs_client: ConfigurationServiceClient, connection_string: str,
        auth_details: AuthDetails, verify_cert: bool
    ) -> None:
        self._logger = logging.getLogger(__name__)
        self._workspace = workspace
        self.artifact_interaction_client = artifact_interaction_client
        self.cs_client = cs_client
        self.data_quality_client = DataQualityClient(
            connection_string=connection_string,
            auth_details=auth_details,
            use_http=True,
            verify_cert=verify_cert
        )
        self.bad_data_client = BadDataClient(
            connection_string=connection_string,
            auth_details=auth_details,
            use_http=True,
            verify_cert=verify_cert
        )

    def get_data_quality_metrics(
        self,
        feature_name: Optional[str] = None,
        metric_name: Optional[str] = None,
        comparison_data_splits: Optional[Sequence[str]] = None,
        normalize: bool = False
    ) -> Mapping[str, Union[pd.Series, pd.DataFrame]]:
        if feature_name is not None:
            self._validate_feature_name(feature_name)
        self._ensure_data_quality_constraints_are_initialized()
        split_metadata = self._get_split_metadata(
            self._workspace.data_split_name
        )
        split_names = [self._workspace.data_split_name]
        split_ids = [split_metadata.split_id]
        if comparison_data_splits:
            valid_splits = self._workspace.get_data_splits()
            missing_splits = list(
                set(comparison_data_splits) - set(valid_splits)
            )
            if missing_splits:
                raise ValueError(
                    f"Splits {missing_splits} in `comparison_data_splits` do not exist in remote. Valid splits: {valid_splits}"
                )
            for i in comparison_data_splits:
                metadata_i = self._get_split_metadata(i)
                split_ids.append(metadata_i.split_id)
                split_names.append(i)

        results = self.data_quality_client.get_data_quality_metrics_result(
            self._workspace.project.id, split_metadata.data_collection_id,
            split_ids, feature_name, metric_name, normalize
        )
        return {split_names[i]: results[i] for i in range(len(split_names))}

    def plot_data_quality_metrics(
        self,
        feature_name: str,
        metric_name: str,
        comparison_data_splits: Optional[Sequence[str]] = None,
        normalize: bool = False
    ) -> None:
        self._validate_feature_name(feature_name)
        self._ensure_data_quality_constraints_are_initialized()
        if comparison_data_splits is None:
            comparison_data_splits = []
        split_names = [self._workspace.data_split_name] + comparison_data_splits
        results = self.get_data_quality_metrics(
            feature_name, metric_name, comparison_data_splits, normalize
        )
        if normalize:
            for i in split_names:
                results[i] = results[
                    i] * 100  # make it percentage instead of fraction

        # convert to a list
        results = [results[i] for i in split_names]
        x_axis_name = "split_names"
        y_axis_name = "%" if normalize else "count"
        df = pd.DataFrame({x_axis_name: split_names, y_axis_name: results})
        viz.basic_bar_graph(
            df, x_axis_name, y_axis_name, metric_name, orientation="v"
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
        self._validate_feature_name(feature_name)
        self._ensure_data_quality_constraints_are_initialized()
        split_metadata = self._get_split_metadata(
            self._workspace.data_split_name
        )
        self.data_quality_client.update_data_quality_metric_constraint(
            self._workspace.project.id,
            split_metadata.data_collection_id,
            feature_name,
            metric_name,
            min_value=min_value,
            max_value=max_value,
            categorical_values=categorical_values
        )

    def get_data_quality_metrics_definition(
        self,
        feature_name: str,
        metric_name: Optional[str] = None,
    ) -> Union[str, Mapping[str, str]]:
        self._validate_feature_name(feature_name)
        self._ensure_data_quality_constraints_are_initialized()
        split_metadata = self._get_split_metadata(
            self._workspace.data_split_name
        )
        return self.data_quality_client.get_data_quality_metrics_definition(
            self._workspace.project.id, split_metadata.data_collection_id,
            feature_name, metric_name
        )

    def get_data_quality_rule_threshold_and_operator(
        self,
        feature_name: str,
        metric_name: Optional[str] = None
    ) -> Mapping[str, Mapping[str, str]]:
        self._validate_feature_name(feature_name)
        self._ensure_data_quality_constraints_are_initialized()
        split_metadata = self._get_split_metadata(
            self._workspace.data_split_name
        )
        return self.data_quality_client.get_data_quality_rule_threshold_and_operator(
            self._workspace.project.id, split_metadata.data_collection_id,
            feature_name, metric_name
        )

    def update_data_quality_rule_threshold_and_operator(
        self,
        feature_name: str,
        metric_name: str,
        violation_threshold: float,
        operator: str,
        treat_threshold_as_raw_count: bool = False
    ) -> None:
        self._validate_feature_name(feature_name)
        self._ensure_data_quality_constraints_are_initialized()
        split_metadata = self._get_split_metadata(
            self._workspace.data_split_name
        )
        self.data_quality_client.update_data_quality_rule_threshold_and_operator(
            self._workspace.project.id, split_metadata.data_collection_id,
            feature_name, metric_name, violation_threshold, operator,
            treat_threshold_as_raw_count
        )

    def initialize_data_quality_constraints_from_data_split(
        self, data_split_name: str, overwrite: bool = False
    ) -> None:
        self._workspace._ensure_project()
        data_collection_name = self._workspace._ensure_data_collection()
        split_metadata = self._get_split_metadata(data_split_name)
        if self.data_quality_client.check_rule_definition_exists(
            self._workspace.project.id, split_metadata.data_collection_id
        ) and not overwrite:
            raise ValueError(
                f"Data quality constraints have already been initialized for data collection \"{data_collection_name}\". Use `overwrite=True` argument to reinitialize."
            )
        self.data_quality_client.generate_rule_definition_from_split(
            self._workspace.project.id, split_metadata.data_collection_id,
            split_metadata.split_id, overwrite
        )

    def compute_feature_drift(
        self,
        comparison_data_splits: Sequence[str],
        feature_names: Optional[Sequence[str]] = None,
        distance_metrics: Optional[Sequence[str]] = None
    ) -> Mapping[str, pd.DataFrame]:
        self._workspace._ensure_project()
        self._workspace._ensure_data_collection()
        self._workspace._ensure_data_split()
        if not comparison_data_splits:
            raise ValueError(
                f"Please provide non empty `comparison_data_splits` to compute feature drift"
            )
        reference_split_metadata = self._get_split_metadata(
            self._workspace.data_split_name
        )
        results = {}
        for split_name in comparison_data_splits:
            split_metadata = self._get_split_metadata(split_name)
            results[split_name
                   ] = self._workspace.aiq_client.compute_feature_drift(
                       self._workspace.project.id,
                       reference_split_metadata.split_id,
                       reference_split_metadata.data_collection_id,
                       split_metadata.split_id,
                       split_metadata.data_collection_id,
                       distance_metrics=distance_metrics,
                       feature_names=feature_names
                   ).response
        return results

    def plot_feature_drift(
        self,
        comparison_data_splits: Sequence[str],
        distance_metric: str,
        feature_names: Optional[Sequence[str]] = None,
        minimum_score: int = 0.0
    ) -> None:
        results = self.compute_feature_drift(
            comparison_data_splits,
            feature_names=feature_names,
            distance_metrics=[distance_metric]
        )

        drift_score_per_feature = {}
        for feature_name in list(results[comparison_data_splits[0]].index):
            drift_score_per_feature[feature_name] = [
                results[i][distance_metric][feature_name]
                for i in comparison_data_splits
            ]

        x_axis_name = "Data split names"
        df = pd.DataFrame(
            {
                x_axis_name: comparison_data_splits,
                **drift_score_per_feature
            }
        )
        viz.stacked_line_chart(
            df,
            x_axis_name=x_axis_name,
            title=f"Drift From Data Split \"{self._workspace.data_split_name}\"",
            x_axis_title=x_axis_name,
            y_axis_title="Drift Scores",
            minimum_value=minimum_score
        )

    def get_schema_mismatch_rows_for_split(
        self,
        data_kind_str: str,
        data_split_name: str = None,
        *,
        feature_name: Optional[str] = None
    ) -> pd.DataFrame:
        if not data_split_name or not data_kind_str:
            raise ValueError(
                "data_split_name and data_kind_str must be populated"
            )
        self._ensure_schema_mismatch_api_constraints_are_initialized()

        split_metadata = self.artifact_interaction_client.get_split_metadata(
            project_name=self._workspace._get_current_active_project_name(),
            data_collection_name=self._workspace.
            _get_current_active_data_collection_name(),
            split_name=data_split_name
        )
        data_kind = DataKindDescribed.Value(data_kind_str.upper())
        return self.bad_data_client.get_schema_mismatch_rows(
            project_id=self._workspace.project.id,
            data_kind=data_kind,
            data_split_id=split_metadata['id'],
            feature_name=feature_name
        )

    def _ensure_schema_mismatch_api_constraints_are_initialized(self) -> None:
        self._workspace._ensure_project()
        self._workspace._ensure_data_collection()

    def _ensure_data_quality_constraints_are_initialized(self):
        project_name = self._workspace._ensure_project()
        data_collection_name = self._workspace._ensure_data_collection()
        self._workspace._ensure_data_split()
        split_metadata = self._get_split_metadata(
            self._workspace.data_split_name
        )
        if not self.data_quality_client.check_rule_definition_exists(
            self._workspace.project.id, split_metadata.data_collection_id
        ):
            raise ValueError(
                f"Data quality constraints have not been initialized for data collection \"{data_collection_name}\". "
                "Please do so by calling `initialize_data_quality_constraints_from_data_split`."
            )

    def _get_split_metadata(self, split_name: str) -> RemoteSplitMetadata:
        split_metadata = self.artifact_interaction_client.get_split_metadata(
            self._workspace._get_current_active_project_name(),
            self._workspace._get_current_active_data_collection_name(),
            split_name
        )
        return RemoteSplitMetadata(
            split_id=split_metadata["id"],
            split_name=split_name,
            data_collection_id=split_metadata["data_collection_id"]
        )

    def _validate_feature_name(self, feature_name: str) -> None:
        if not feature_name in self._get_feature_names():
            raise ValueError(
                f"Feature \"{feature_name}\" does not exist in the data collection."
            )

    def _get_feature_names(self) -> Sequence:
        return list(self._workspace.get_xs(0, 1).columns)
