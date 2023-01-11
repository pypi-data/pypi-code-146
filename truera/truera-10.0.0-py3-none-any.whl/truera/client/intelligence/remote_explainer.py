from __future__ import annotations

from collections import defaultdict
import logging
from typing import (
    Mapping, NamedTuple, Optional, Sequence, Tuple, TYPE_CHECKING, Union
)
from urllib.parse import quote

import numpy as np
import pandas as pd

from truera.client.client_utils import get_qoi_from_string
from truera.client.client_utils import get_string_from_qoi_string
from truera.client.errors import NotFoundError
from truera.client.intelligence.bias import BiasResult
from truera.client.intelligence.explainer import TabularExplainer
from truera.client.intelligence.segment import SegmentGroup
from truera.client.public.communicator.http_communicator import \
    ModelRunnerError
from truera.client.services.artifact_interaction_client import Model
from truera.client.services.artifact_interaction_client import Project
from truera.client.services.artifactrepo_client import ArtifactMetaFetchMode
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    FeatureSortMethod  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module

if TYPE_CHECKING:
    from truera.client.remote_truera_workspace import RemoteTrueraWorkspace


def catch_model_runner_errors(func):

    def wrapper(*args, **kwargs):
        explainer = args[0]
        try:
            return func(*args, **kwargs)
        except ModelRunnerError as e:
            project_name = explainer._project_name
            e.message += f"\nView the logs for this failure here: {explainer._workspace.connection_string}/p/{quote(project_name)}/t/computations"
            raise ModelRunnerError(e.message, e.job_id) from e

    return wrapper


class RemoteSplitMetadata(NamedTuple):
    split_id: str
    split_name: str


class RemoteExplainer(TabularExplainer):

    def __init__(
        self, workspace: RemoteTrueraWorkspace, project: Project, model: Model,
        data_collection_name: str, data_split_name: str,
        comparison_data_split_names: Sequence[str]
    ) -> None:
        self._logger = logging.getLogger(__name__)
        self._workspace = workspace
        self._project = project
        self._model = model
        model_meta = self._workspace.artifact_interaction_client.get_model_metadata(
            self._project.name, self._model.model_name
        )
        self._data_collection_id = model_meta["data_collection_id"]
        self._data_collection_name = data_collection_name
        self._base_data_split = None
        self._comparison_data_splits = []
        self.set_base_data_split(data_split_name)
        self.set_comparison_data_splits(comparison_data_split_names)
        self._segment = None

    @property
    def logger(self):
        return self._logger

    @property
    def _project_id(self) -> str:
        return self._project.id

    @property
    def _project_name(self) -> str:
        return self._project.name

    @property
    def _model_id(self) -> str:
        return self._model.model_id

    def _get_score_type(self) -> str:
        project_metadata = self._workspace.artifact_interaction_client.get_project_metadata(
            self._project_id
        )
        return get_string_from_qoi_string(
            project_metadata["settings"]["score_type"]
        )

    def _get_split_metadata(self, split_name: str) -> RemoteSplitMetadata:
        split_id = self._workspace.artifact_interaction_client.get_split_metadata(
            self._project.name, self._data_collection_name, split_name
        )["id"]
        return RemoteSplitMetadata(split_id=split_id, split_name=split_name)

    def set_base_data_split(self, data_split_name: str):
        if not data_split_name:
            self._base_data_split = None
            return
        self._validate_data_split(data_split_name)
        self._base_data_split = self._get_split_metadata(data_split_name)
        comparison_splits = self.get_comparison_data_splits()
        if data_split_name in comparison_splits:
            comparison_splits.remove(data_split_name)
            self.set_comparison_data_splits(comparison_splits)

    def _ensure_data_split(self):
        if not self._base_data_split:
            raise ValueError(
                "Set the current data_split using `set_base_data_split`"
            )

    def set_comparison_data_splits(
        self,
        comparison_data_splits: Optional[Sequence[str]] = None,
        use_all_data_splits: bool = False
    ):
        if not comparison_data_splits and not use_all_data_splits:
            self._comparison_data_splits = []
            return
        self._ensure_data_split()
        available_splits = self._workspace.artifact_interaction_client.get_all_datasplits_in_data_collection(
            self._project_id, self._data_collection_name
        )
        comparison_data_splits = self._validate_comparison_data_splits(
            available_splits,
            self._base_data_split.split_name,
            comparison_data_splits,
            use_all_data_splits=use_all_data_splits
        )
        self._comparison_data_splits = [
            self._get_split_metadata(split_name)
            for split_name in comparison_data_splits
        ]

    def get_base_data_split(self) -> str:
        self._ensure_data_split()
        return self._base_data_split.split_name

    def get_data_collection(self) -> str:
        return self._data_collection_name

    def get_comparison_data_splits(self) -> Sequence[str]:
        return [split.split_name for split in self._comparison_data_splits]

    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False
    ) -> pd.DataFrame:
        self._ensure_data_split()
        return self._workspace.aiq_client.get_xs(
            self._project_id,
            self._base_data_split.split_id,
            self._data_collection_id,
            start,
            stop,
            extra_data=extra_data,
            system_data=system_data,
            segment=self._segment,
            model_id=self._model_id
        ).response

    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False
    ) -> Union[pd.Series, pd.DataFrame]:
        self._ensure_data_split()
        return self._workspace.aiq_client.get_ys(
            self._project_id,
            self._base_data_split.split_id,
            self._data_collection_id,
            start,
            stop,
            system_data=system_data,
            segment=self._segment,
            model_id=self._model_id
        ).response

    @catch_model_runner_errors
    def get_ys_pred(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        *,
        system_data: bool = False,
        include_all_points: bool = False,
        score_type: Optional[str] = None,
        wait: bool = True
    ) -> Union[pd.Series, pd.DataFrame]:
        self._ensure_data_split()
        score_type_qoi = get_qoi_from_string(score_type) if score_type else None
        return self._workspace.aiq_client.get_ys_pred(
            self._project_id,
            self._model_id,
            self._base_data_split.split_id,
            start,
            stop,
            segment=self._segment,
            include_system_data=system_data,
            include_all_points=include_all_points,
            score_type=score_type_qoi,
            wait=wait
        ).response

    def get_feature_influences_for_data(
        self,
        pre_data: pd.DataFrame,
        post_data: Optional[pd.DataFrame] = None,
        ys: Optional[Union[np.ndarray, pd.Series]] = None,
        score_type: Optional[str] = None,
        comparison_post_data: Optional[pd.DataFrame] = None,
        num_internal_qii_samples: int = 1000,
        algorithm: str = "truera-qii"
    ) -> pd.DataFrame:
        raise NotImplementedError(
            "This functionality is not currently implemented for remote explainers!"
        )

    @catch_model_runner_errors
    def get_feature_influences(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,
        system_data: bool = False,
        wait: bool = True
    ) -> pd.DataFrame:
        self._ensure_data_split()
        self._validate_feature_influence_score_type(score_type)
        self._ensure_influences_background_data_split_is_set()
        return self._workspace.aiq_client.get_feature_influences(
            self._project_id,
            self._model_id,
            self._base_data_split.split_id,
            start,
            stop,
            score_type=score_type,
            segment=self._segment,
            include_system_data=system_data,
            wait=wait
        ).response

    def _get_all_feature_influences_and_algorithm_type(
        self
    ) -> Tuple[pd.DataFrame, ExplanationAlgorithmType]:
        self._ensure_data_split()
        self._ensure_influences_background_data_split_is_set()
        return self._workspace.aiq_client.get_feature_influences(
            self._project_id,
            self._model_id,
            self._base_data_split.split_id,
            start=0,
            stop=None,
            score_type=None,
            segment=None,
            include_system_data=False,
            wait=False,
            return_algorithm_type=True
        ).response

    def _get_sorted_features_metric_values(
        self,
        sort_method: FeatureSortMethod = FeatureSortMethod.ABSOLUTE_VALUE_SUM,
        wait: bool = True
    ) -> pd.Series:
        return self._workspace.aiq_client._get_sorted_features(
            self._project_id,
            self._model_id,
            self._base_data_split.split_id,
            segment=self._segment,
            sort_method=sort_method,
            wait=wait
        ).response

    @catch_model_runner_errors
    def get_global_feature_importances(
        self,
        score_type: Optional[str] = None,
        wait: bool = True
    ) -> pd.DataFrame:
        self._ensure_data_split()
        self._validate_feature_influence_score_type(score_type)
        return self._workspace.aiq_client.get_global_feature_importances(
            self._project_id,
            self._model_id,
            self._base_data_split.split_id,
            score_type=score_type,
            segment=self._segment,
            wait=wait
        ).response

    @catch_model_runner_errors
    def get_partial_dependencies(
        self,
        wait: bool = True
    ) -> Tuple[Sequence[str], Mapping[str, Sequence], Mapping[str, Sequence]]:
        self._ensure_data_split()
        return self._workspace.aiq_client.get_partial_dependencies(
            self._project_id,
            self._model_id,
            self._base_data_split.split_id,
            segment=self._segment,
            wait=wait
        ).response

    def _get_segmentations(self) -> Mapping[str, SegmentGroup]:
        return self._workspace.aiq_client.get_wrapped_segmentations(
            self._project_id
        ).response

    def set_segment(self, segment_group_name: str, segment_name: str):
        segment_groups = self._get_segmentations()
        if segment_group_name not in segment_groups:
            raise NotFoundError(
                f"Segment group \"{segment_group_name}\" does not exist in project \"{self._project.name}\""
            )
        if segment_name not in segment_groups[segment_group_name].get_segments(
        ):
            raise NotFoundError(
                f"Segment \"{segment_name}\" does not exist in segment group \"{segment_group_name}\""
            )
        self._segment = segment_groups[segment_group_name].get_segments(
        )[segment_name]

    def clear_segment(self):
        self._segment = None

    @catch_model_runner_errors
    def suggest_high_error_segments(
        self,
        num_features: int = 1,
        max_num_responses: int = 3,
        num_samples: int = 100,
        segment_type: Optional[str] = None,
        metric_types: Optional[Union[str, Sequence[str]]] = None,
        minimum_size: int = 50,
        size_exponent: float = 0.25,
        comparison_data_split_name: Optional[str] = None,
        random_state: int = 0,
    ) -> pd.DataFrame:
        score_type = self._workspace._get_score_type_for_project(
            self._project_id
        )
        metric_types, interesting_segment_type = self._validate_suggest_high_error_segments(
            segment_type, metric_types, score_type, comparison_data_split_name
        )
        data_split_id = self._base_data_split.split_id
        comparison_data_split_id = None
        comparison_model_id = None
        if comparison_data_split_name is not None:
            metadata = self._get_split_metadata(comparison_data_split_name)
            comparison_data_split_id = metadata.split_id
            comparison_model_id = self._model_id
        segment_groups = self._workspace.aiq_client.suggest_high_error_segments(
            self._project_id,
            self._model_id,
            data_split_id,
            comparison_model_id,
            comparison_data_split_id,
            interesting_segment_type,
            num_features,
            max_num_responses,
            num_samples,
            minimum_size,
            size_exponent,
            random_state,
            wait=True
        ).response.values()
        total_size = self._workspace.aiq_client.get_ys_pred(
            self._project_id,
            self._model_id,
            data_split_id,
            include_all_points=True,
            wait=True
        ).response.shape[0]
        mp = defaultdict(list)
        for curr in segment_groups:
            segment = list(curr.segments.values())[0]
            mp["representation"].append(segment.ingestable_definition())
            metrics = self._workspace.aiq_client.compute_performance(
                self._project_id,
                self._model_id,
                data_split_id,
                metric_types,
                segment,
                wait=True
            ).response
            for i, metric_type in enumerate(metric_types):
                mp[metric_type].append(metrics[i])
            segment_size = self._workspace.aiq_client.get_ys_pred(
                self._project_id,
                self._model_id,
                data_split_id,
                segment=segment,
                include_all_points=True,
                wait=True
            ).response.shape[0]
            mp["size"].append(segment_size)
            mp["size (%)"].append(100 * segment_size / total_size)
        return pd.DataFrame(data=mp)

    @catch_model_runner_errors
    def compute_fairness(
        self,
        segment_group: str,
        segment1: str,
        segment2: Optional[str] = None,
        fairness_type: Optional[str] = "DISPARATE_IMPACT_RATIO",
        threshold: Optional[float] = None,
        threshold_score_type: Optional[str] = None,
    ) -> BiasResult:
        self._ensure_data_split()
        if fairness_type not in self.list_fairness_metrics():
            raise ValueError(
                f"Unsupported fairness type {fairness_type}. Use `list_fairness_metrics()` to see a list of available options."
            )
        segmentations = self._get_segmentations()
        if segment_group not in segmentations:
            raise ValueError(f"Segment group {segment_group} does not exist.")
        segment_names = segmentations[segment_group].segments.keys()
        if segment1 not in segment_names or (
            segment2 and segment2 not in segment_names
        ):
            raise ValueError(
                f"Segments {segment1} and/or {segment2} were not found within the available segments for this segment group: {segment_names}"
            )
        if threshold_score_type not in [None, 'probits', 'logits']:
            raise ValueError(
                "Threshold score type must be None (uses default score type for model), `probits`, or `logits`."
            )
        if self._segment:
            self.logger.warning(
                "Ignoring segment that is set for this explainer. Using provided segment names for fairness computation..."
            )
        return self._workspace.aiq_client.compute_fairness(
            self._project_id,
            self._model_id,
            self._base_data_split.split_id,
            segment_group,
            segment1,
            segment2,
            fairness_type=fairness_type,
            threshold=threshold,
            threshold_score_type=threshold_score_type,
            wait=True
        ).response

    def list_fairness_metrics(self) -> Sequence[str]:
        return self._workspace.aiq_client.list_fairness_metrics()

    def rank_performance(
        self, metric_type: str, ascending: bool = False
    ) -> pd.DataFrame:
        self._validate_metric_type(metric_type)
        self._ensure_data_split()
        models_in_data_collection = self._workspace.artifact_interaction_client.get_all_models_in_project(
            project_id=self._project_id,
            data_collection_name=self.get_data_collection(),
            ar_meta_fetch_mode=ArtifactMetaFetchMode.ALL
        )["name_id_pairs"]
        ret = None
        column_names = []
        for model in models_in_data_collection:
            model_performance_df = self._compute_performance_df(
                metric_type, model_id=model["id"]
            )
            if not column_names:
                column_names = [
                    f"{metric_type} ({split_name})"
                    for split_name in model_performance_df["Split"]
                ]
                ret = pd.DataFrame([], columns=column_names)
            ret = ret.append(
                pd.DataFrame(
                    [model_performance_df[metric_type].to_list()],
                    columns=column_names
                ),
                ignore_index=True
            )
        ret.insert(
            0, "Model Name", [i["name"] for i in models_in_data_collection]
        )
        return ret.sort_values(column_names[0],
                               ascending=ascending).reset_index(drop=True)

    def _compute_performance_df(
        self,
        metric_type: str,
        compute_for_comparison_data_splits: bool = True,
        model_id: Optional[str] = None
    ) -> pd.DataFrame:
        self._ensure_data_split()
        self._validate_metric_type(metric_type)
        if model_id is None:
            model_id = self._model_id
        all_splits = [self._base_data_split]
        if compute_for_comparison_data_splits and self._comparison_data_splits:
            all_splits += self._comparison_data_splits
        split_names = []
        split_performances = []
        for split_metadata in all_splits:
            split_names.append(split_metadata.split_name)
            split_performances.append(
                self._workspace.aiq_client.compute_performance(
                    self._project_id,
                    model_id,
                    split_metadata.split_id, [metric_type],
                    segment=self._segment,
                    wait=True
                ).response[0]
            )
        return pd.DataFrame.from_dict(
            {
                "Split": split_names,
                metric_type: split_performances
            }
        )

    def _compute_model_score_instability_df(
        self,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False
    ) -> pd.DataFrame:
        self._ensure_data_split()
        if not self._comparison_data_splits:
            raise ValueError(
                "Model score drifts require comparison data splits. See `set_comparison_data_splits` for more information."
            )
        base_split_id = self._base_data_split.split_id
        base_split_name = self._base_data_split.split_name
        split_names = []
        split_drift = []
        distance_type = "DIFFERENCE_OF_MEAN" if use_difference_of_means else "NUMERICAL_WASSERSTEIN"
        for split_metadata in self._comparison_data_splits:
            split_names.append(split_metadata.split_name)
            split_drift.append(
                self._workspace.aiq_client.compute_model_score_instability(
                    self._project_id,
                    self._model_id,
                    base_split_id,
                    split_metadata.split_id,
                    score_type=score_type,
                    distance_type=distance_type,
                    segment=self._segment,
                    wait=True
                ).response
            )
        stability_data = pd.DataFrame()
        stability_data["Comparison Split"] = split_names
        stability_data["Base Split"] = base_split_name
        stability_data["Model Score Instability"] = split_drift
        return stability_data

    @catch_model_runner_errors
    def compute_feature_contributors_to_instability(
        self,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False
    ) -> pd.DataFrame:
        self._ensure_data_split()
        if not self._comparison_data_splits:
            raise ValueError(
                "Feature contributors to instability require comparison data splits. See `set_comparison_data_splits` for more information."
            )
        base_split_id = self._base_data_split.split_id
        dfs_to_concat = []
        for split_metadata in self._comparison_data_splits:
            df = self._workspace.aiq_client.compute_feature_contributors_to_instability(
                self._project_id,
                self._model_id,
                base_split_id,
                split_metadata.split_id,
                score_type=score_type,
                use_difference_of_means=use_difference_of_means,
                segment=self._segment,
                wait=True
            ).response
            df.set_index(pd.Index([split_metadata.split_name]), inplace=True)
            dfs_to_concat.append(df)
        return pd.concat(dfs_to_concat)[self.get_feature_names()]

    @catch_model_runner_errors
    def compute_estimated_performance(self,
                                      metric_type: str) -> Tuple[float, int]:
        self._ensure_data_split()
        self._validate_metric_type(metric_type)
        return self._workspace.aiq_client.compute_estimated_performance(
            self._project_id,
            self._model_id,
            self._base_data_split.split_id,
            metric_type,
            segment=self._segment,
            wait=True
        ).response

    def _ensure_influences_background_data_split_is_set(self) -> None:
        # Ensure background data split is set in metarepo. If not, set it from default value.
        background_split_id = self._workspace.cs_client.get_base_split(
            self._project.id, self._data_collection_id
        )
        if not background_split_id:
            background_split_id = self._workspace.cs_client.get_base_split(
                self._project.id,
                self._data_collection_id,
                infer_base_split_if_not_set=True
            )
            if not background_split_id:
                raise ValueError("Cannot determine background data split!")
            background_split_name = self._workspace.artifact_interaction_client.get_split_metadata_by_id(
                self._project.id, split_id=background_split_id
            )["name"]
            self.logger.warning(
                f"Background split for `data_collection` \"{self._data_collection_name}\" is currently not set. Setting it to \"{background_split_name}\""
            )
            self._workspace.cs_client.set_base_split(
                self._project.id, self._data_collection_id, background_split_id
            )

    def list_performance_metrics(self) -> Sequence[str]:
        return self._workspace.aiq_client.list_performance_metrics()

    def _validate_data_split(self, data_split_name: str) -> None:
        available_splits = self._workspace.artifact_interaction_client.get_all_datasplits_in_data_collection(
            self._project_id, self._data_collection_name
        )
        if data_split_name not in available_splits:
            raise ValueError(f"No such data split \"{data_split_name}\"!")
