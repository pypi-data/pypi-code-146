from __future__ import annotations

from collections import defaultdict
from copy import copy
from dataclasses import dataclass
import hashlib
import logging
from typing import Mapping, Optional, Sequence, Tuple, TYPE_CHECKING, Union
import uuid

import numpy as np
import pandas as pd

from truera.client.errors import NotFoundError
from truera.client.intelligence.explainer import TabularExplainer
import truera.client.intelligence.metrics_util as metrics_util
from truera.client.local.intelligence.local_explanation_processor import \
    LocalExplanationProcessor
from truera.client.local.local_artifacts import DataCollection
from truera.client.local.local_artifacts import DataSplit
from truera.client.local.local_artifacts import Model
from truera.client.local.local_artifacts import PdCache
from truera.client.local.local_artifacts import Project
from truera.client.local.local_artifacts import QiiCache
from truera.client.truera_workspace_utils import ExplainerQiiCacheKey
from truera.client.util import workspace_validation_utils
from truera.client.util.absolute_progress_bar import AbsoluteProgressBar
from truera.partial_dependence_plot.partial_dependence_plot import \
    PartialDependencePlotComputer
from truera.partial_dependence_plot.partial_dependence_representation_converter import \
    convert_PartialDependenceCache_to_tuple
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    FeatureSortMethod  # pylint: disable=no-name-in-module
from truera.protobuf.public.data.filter_pb2 import \
    FilterExpression  # pylint: disable=no-name-in-module
from truera.protobuf.public.data.segment_pb2 import \
    InterestingSegment  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION  # pylint: disable=no-name-in-module
from truera.protobuf.public.modelrunner.cache_entries_pb2 import \
    PartialDependenceCache  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.public import feature_influence_constants as fi_constants
from truera.public.processors.feature_sort_processor import \
    FeatureSortProcessor
from truera.public.processors.interesting_segments_processor import \
    InterestingSegmentsProcessor
from truera.utils import filter_constants
from truera.utils.filter_utils import FilterProcessor

if TYPE_CHECKING:
    from truera.client.local.local_truera_workspace import LocalTrueraWorkspace


@dataclass(eq=True, frozen=True)
class SegmentContext:
    segment_group_name: str
    segment_name: str


class LocalExplainer(TabularExplainer):

    def __init__(
        self, workspace: LocalTrueraWorkspace, project_obj: Project,
        model: Model, data_collection: DataCollection, data_split: str,
        comparison_data_splits: Sequence[str]
    ) -> None:
        self._base_data_split = None
        self._comparison_data_splits = []
        self._workspace = workspace
        self._project_obj = project_obj
        self._classification_performance_metrics = metrics_util.LOCAL_CLASSIFICATION_METRICS
        self._regression_performance_metrics = metrics_util.LOCAL_REGRESSION_METRICS
        self._model = model
        self._data_collection = data_collection
        self.set_base_data_split(data_split)
        self.set_comparison_data_splits(comparison_data_splits)
        self._qii_cache: QiiCache = self._workspace.qii_cache
        self._pd_cache: PdCache = self._workspace.pd_cache
        self._logger = logging.getLogger(__name__)
        self._segment_context = SegmentContext(
            segment_group_name=None, segment_name=None
        )

    @property
    def logger(self):
        return self._logger

    def _get_score_type(self) -> str:
        return self._project_obj.score_type

    def _ensure_feature_map_if_needed(
        self
    ) -> Optional[Mapping[str, Sequence[str]]]:
        if self._data_collection.feature_map is not None:
            return self._data_collection.feature_map
        data_splits = list(self._data_collection.data_splits.values())
        if not data_splits:
            return None
        pre_cols = sorted(list(data_splits[0].xs_pre.columns))
        post_cols = sorted(list(data_splits[0].xs_post.columns))
        if pre_cols != post_cols:
            raise ValueError(
                f"Pre-transform data columns do not match post-transform data columns. Please provide a feature map which provides a mapping between pre- and post-features while adding the data collection via `add_data_collection`. Pre-transform features: {pre_cols} Post-transform features: {post_cols}"
            )
        return None

    def set_base_data_split(self, data_split_name: str):
        if not data_split_name:
            self._base_data_split = None
            return
        self._validate_data_split(data_split_name)
        self._base_data_split = self._data_collection.data_splits[
            data_split_name]
        comparison_splits = self.get_comparison_data_splits()
        if data_split_name in comparison_splits:
            comparison_splits.remove(data_split_name)
            self.set_comparison_data_splits(comparison_splits)

    def get_base_data_split(self) -> str:
        self._ensure_data_split()
        return self._base_data_split.name

    def get_data_collection(self) -> str:
        return self._data_collection.name

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
        available_splits = list(self._data_collection.data_splits.keys())
        comparison_data_splits = self._validate_comparison_data_splits(
            available_splits,
            self._base_data_split.name,
            comparison_data_splits,
            use_all_data_splits=use_all_data_splits
        )
        self._comparison_data_splits = [
            self._data_collection.data_splits[split_name]
            for split_name in comparison_data_splits
        ]

    def get_comparison_data_splits(self) -> Sequence[str]:
        return [split.name for split in self._comparison_data_splits]

    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False
    ) -> pd.DataFrame:
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        if system_data:
            raise ValueError("`system_data` is not supported in local!")
        start, stop = self._convert_start_stop(start, stop)
        if not isinstance(self._base_data_split.xs_pre, pd.DataFrame):
            raise TypeError(
                f"Data must be of type pandas.DataFrame. Found {type(self._base_data_split.xs_pre)}."
            )
        data = self._base_data_split.xs_pre.iloc[start:stop, :]
        if extra_data and self._base_data_split.extra is not None:
            data = pd.concat(
                [data, self._base_data_split.extra.iloc[start:stop, :]], axis=1
            )
        if self._check_current_active_segment():
            row_selector = self._get_row_selector_for_segment(
                segment_group_name=self._segment_context.segment_group_name,
                segment_name=self._segment_context.segment_name,
                data_split=self._base_data_split,
                start=start,
                stop=stop
            )
            data = data[row_selector]
        return data

    def _get_xs_post(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None
    ) -> pd.DataFrame:
        self._ensure_data_split()
        return self._get_xs_post_for_split(self._base_data_split, start, stop)

    def _get_xs_post_for_split(
        self,
        data_split: DataSplit,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        ignore_segment: bool = False
    ) -> pd.DataFrame:
        self._ensure_feature_map_if_needed()
        start, stop = self._convert_start_stop(start, stop)
        data = data_split.xs_post
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                f"Data must be of type pandas.DataFrame. Found {type(data)}."
            )
        data = data.iloc[start:stop, :]
        if not ignore_segment and self._check_current_active_segment():
            row_selector = self._get_row_selector_for_segment(
                segment_group_name=self._segment_context.segment_group_name,
                segment_name=self._segment_context.segment_name,
                data_split=data_split,
                start=start,
                stop=stop
            )
            data = data[row_selector]
        return data

    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False
    ) -> pd.Series:
        self._ensure_data_split()
        if system_data:
            raise ValueError("`system_data` is not supported in local!")
        return self._get_ys_for_split(self._base_data_split, start, stop)

    def _get_ys_for_split(
        self,
        data_split: DataSplit,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        ignore_segment: bool = False
    ) -> pd.Series:
        start, stop = self._convert_start_stop(start, stop)
        data = data_split.ys
        if isinstance(data, pd.Series):
            data = data.iloc[start:stop]
        elif data is None:
            raise NotFoundError("Labels were not found for this data split.")
        else:
            raise TypeError(
                f"Labels must be of type pandas.Series. Found {type(data)}."
            )
        data = data.iloc[start:stop]
        if not ignore_segment and self._check_current_active_segment():
            row_selector = self._get_row_selector_for_segment(
                segment_group_name=self._segment_context.segment_group_name,
                segment_name=self._segment_context.segment_name,
                data_split=data_split,
                start=start,
                stop=stop
            )
            data = data[row_selector]
        return data

    def get_ys_pred(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False,
        wait: bool = True
    ) -> pd.Series:
        return self._get_ys_pred(
            start, stop, self._project_obj.score_type, wait
        )

    def _get_ys_pred(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,
        wait: bool = True,
    ) -> pd.Series:
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        start, stop = self._convert_start_stop(start, stop)
        if not wait:
            raise ValueError("For local computations `wait` must be `True`!")
        return pd.Series(
            self._model.predict(
                self._get_xs_post(start, stop),
                score_type,
            ),
            index=self.get_xs(start, stop).index
        )

    def _get_row_selector_for_segment(
        self,
        segment_group_name: str,
        segment_name: str,
        data_split: DataSplit,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        model_id: Optional[str] = None
    ) -> pd.Series:
        segment = self._project_obj.get_segment(
            segment_group_name=segment_group_name, segment_name=segment_name
        )
        return self._get_row_selector_for_filter_expression(
            segment._segment_proto.filter_expression, data_split, start, stop,
            model_id
        )

    def _get_row_selector_for_filter_expression(
        self,
        filter_expression: FilterExpression,
        data_split: DataSplit,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        model_id: Optional[str] = None
    ) -> pd.Series:
        start, stop = self._convert_start_stop(start, stop)
        data = data_split.xs_pre.iloc[start:stop, :]
        if data_split.extra is not None:
            data = pd.concat(
                [data, data_split.extra.iloc[start:stop, :]], axis=1
            )
        filter_requirements = FilterProcessor.get_filter_requirements(
            filter_expression
        )
        nonexistent_model_ids = filter_requirements.model_ids_to_score_type.keys(
        ) - self._project_obj.models.keys() - {
            filter_constants.GENERIC_MODEL_ID
        }
        if nonexistent_model_ids:
            raise ValueError(
                f"The provided `segment_definitions` contains model(s) that doesn't exist: {nonexistent_model_ids}."
            )
        if filter_requirements.requires_ground_truth:
            if not data_split.has_labels:
                index = data_split.ys.iloc[start:stop, 0].index if isinstance(
                    data_split.ys, pd.DataFrame
                ) else pd.Series(data_split.ys).iloc[start:stop].index
                data[filter_constants.FILTER_GROUND_TRUTH_NAME
                    ] = pd.Series(np.nan, index=index)
            else:
                data[filter_constants.FILTER_GROUND_TRUTH_NAME
                    ] = data_split.ys.iloc[start:stop, 0] if isinstance(
                        data_split.ys, pd.DataFrame
                    ) else pd.Series(data_split.ys).iloc[start:stop]
        for requested_model_id, qois in filter_requirements.model_ids_to_score_type.items(
        ):
            real_model_id = requested_model_id if requested_model_id != filter_constants.GENERIC_MODEL_ID else model_id
            for qoi in qois:
                model_output_score_type = fi_constants.QOI_TO_SCORE_TYPE[qoi]
                model_output_column_name = filter_constants.get_filter_column_name_for_model_output(
                    qoi, real_model_id
                )
                if real_model_id:
                    data[model_output_column_name] = self._project_obj.models[
                        real_model_id].predict(
                            data_split.xs_post.iloc[start:stop, :],
                            model_output_score_type
                        )
                else:
                    data[model_output_column_name] = self._model.predict(
                        data_split.xs_post.iloc[start:stop, :],
                        model_output_score_type
                    )

        return FilterProcessor.filter(
            data.rename(columns={i: str(i) for i in data.columns}),
            filter_expression
        )

    def _hash_data_split(self, bg: pd.DataFrame) -> str:
        return hashlib.sha256(pd.util.hash_pandas_object(bg).values).hexdigest()

    def get_all_computed_feature_influences(
        self,
        bg: Optional[pd.DataFrame] = None
    ) -> Mapping[ExplainerQiiCacheKey, pd.DataFrame]:
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        bg = bg if bg is not None else self.get_influences_background_data_split_or_set_from_default(
        ).xs_post
        hash_bg = self._hash_data_split(bg)
        ret = {}
        all_score_types = fi_constants.ALL_REGRESSION_SCORE_TYPES if self._get_output_type(
        ) == "regression" else fi_constants.ALL_CLASSIFICATION_SCORE_TYPES
        for algorithm in [
            ExplanationAlgorithmType.TRUERA_QII,
            ExplanationAlgorithmType.KERNEL_SHAP,
            ExplanationAlgorithmType.TREE_SHAP_PATH_DEPENDENT,
            ExplanationAlgorithmType.TREE_SHAP_INTERVENTIONAL
        ]:
            for score_type in all_score_types:
                computed_qiis = self._qii_cache.get_feature_influence_by_algorithm(
                    project_name=self._project_obj.name,
                    model_name=self._model.name,
                    data_collection_name=self._data_collection.name,
                    data_split_name=self._base_data_split.name,
                    hash_bg=hash_bg,
                    score_type=score_type,
                    num_samples=self._project_obj.num_samples,
                    algorithm=algorithm
                )
                if computed_qiis is not None:
                    ret[ExplainerQiiCacheKey(score_type, algorithm)
                       ] = computed_qiis.iloc[:, 1:]
        return ret

    def _get_feature_influences_nonbase_split(
        self,
        split_name,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        force_compute: bool = False,
        score_type: Optional[str] = None,
        wait: bool = True
    ) -> pd.DataFrame:
        initial_base_split = self.get_base_data_split()
        initial_comparison_splits = self.get_comparison_data_splits()
        try:
            self.set_base_data_split(split_name)
            return self.get_feature_influences(
                start, stop, score_type, wait, force_compute
            )
        finally:
            self.set_base_data_split(initial_base_split)
            self.set_comparison_data_splits(initial_comparison_splits)

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
        algorithm_enum = LocalExplanationProcessor.validate_feature_influence_algorithm(
            algorithm
        )
        self._validate_feature_influence_score_type(score_type)
        workspace_validation_utils.validate_split_for_dataframe(
            self._logger,
            pre_data=pre_data,
            post_data=None if self._data_collection.feature_transform_type
            == FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION else post_data,
            label_data=ys,
            pre_to_post_feature_map=self._data_collection.feature_map,
            output_type=self._get_output_type()
        )
        feature_map = self._ensure_feature_map_if_needed()
        if score_type is None:
            score_type = self._project_obj.score_type
        if comparison_post_data is None:
            comparison_post_data = self.get_influences_background_data_split_or_set_from_default(
            ).xs_post
        elif not isinstance(comparison_post_data, pd.DataFrame):
            raise ValueError(
                "`comparison_post_data` must be of type `pandas.DataFrame`!"
            )
        comparison_post_data = self._model.transform(comparison_post_data)
        return LocalExplanationProcessor(
            model=self._model,
            score_type=score_type,
            comparison_data=comparison_post_data,
            feature_map=feature_map,
            num_internal_qii_samples=num_internal_qii_samples,
            logger=self._logger
        ).get_feature_influences_for_data(
            pre_data, post_data, ys, algorithm=algorithm_enum
        )

    def get_feature_influences(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,
        wait: bool = True,
        force_compute: bool = False,
        system_data: bool = False
    ) -> pd.DataFrame:
        self._ensure_data_split()
        self._validate_feature_influence_score_type(score_type)
        self._ensure_feature_map_if_needed()
        if not wait:
            raise ValueError("For local computations `wait` must be `True`!")
        if score_type is None:
            score_type = self._project_obj.score_type
        if stop is None:
            stop = self._project_obj.num_default_influences
        start, stop = self._convert_start_stop(start, stop)
        xs_pre = self.get_xs(start, stop)
        xs_post = self._get_xs_post(start, stop)
        hash_xs = pd.util.hash_pandas_object(xs_pre).to_numpy().reshape(-1, 1)
        bg = self.get_influences_background_data_split_or_set_from_default(
        ).xs_post
        hash_bg = self._hash_data_split(bg)
        use_qii = self._project_obj.get_influence_algorithm() == "truera-qii"
        cache_query_fn = self._qii_cache.get_qiis if use_qii else self._qii_cache.get_shap_values
        computed_qiis = cache_query_fn(
            project_name=self._project_obj.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=self._base_data_split.name,
            hash_bg=hash_bg,
            score_type=score_type,
            num_samples=self._project_obj.num_samples
        )
        if (computed_qiis
            is not None) and (computed_qiis.shape[0] >= stop) and np.all(
                computed_qiis.iloc[start:stop,
                                   0].to_numpy().reshape(-1, 1) == hash_xs
            ) and (not force_compute):
            return computed_qiis.iloc[start:stop, 1:]
        ys = None
        pre_cols = list(xs_pre.columns)
        if score_type in fi_constants.MODEL_ERROR_SCORE_TYPES:
            ys = self.get_ys(start, stop).to_numpy().ravel()

        processor = LocalExplanationProcessor(
            model=self._model,
            score_type=score_type,
            comparison_data=bg,
            feature_map=self._ensure_feature_map_if_needed(),
            num_internal_qii_samples=self._project_obj.num_samples,
            logger=self._logger
        )
        qiis, algorithm = processor.get_feature_influences_for_data_infer_algorithm(
            pre_data=xs_pre, post_data=xs_post, ys=ys, use_qii=use_qii
        )
        new_hash_bg = self._hash_data_split(
            self.get_influences_background_data_split_or_set_from_default().
            xs_post
        )
        if new_hash_bg != hash_bg:
            raise AssertionError(
                "Aborting because data split has been modified! Please call `get_feature_influences` again."
            )
        computed_qiis = pd.DataFrame(
            data=np.concatenate([hash_xs, qiis.to_numpy()], axis=1),
            columns=["hash_xs"] + list(qiis.columns)
        )
        self._qii_cache.add_or_update_influences(
            influences=computed_qiis,
            project_name=self._project_obj.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=self._base_data_split.name,
            hash_bg=hash_bg,
            score_type=score_type,
            algorithm=algorithm,
            num_samples=self._project_obj.num_samples
        )
        return computed_qiis.iloc[start:stop, 1:]

    def _get_sorted_features_metric_values(
        self,
        sort_method: FeatureSortMethod = FeatureSortMethod.ABSOLUTE_VALUE_SUM,
        wait: bool = True
    ) -> pd.Series:
        return FeatureSortProcessor.get_feature_sort_values(
            self.get_xs(),
            self.get_feature_influences(wait=wait),
            sort_methods=[sort_method]
        )

    def get_global_feature_importances(
        self,
        score_type: Optional[str] = None,
        wait: bool = True
    ) -> pd.DataFrame:
        infs = self.get_feature_influences(score_type=score_type, wait=wait)
        aggregated_infs = infs.abs().mean()
        if aggregated_infs.sum() > 0:
            aggregated_infs /= aggregated_infs.sum()
        aggregated_infs = aggregated_infs.to_frame().T
        return aggregated_infs

    def get_partial_dependencies(
        self,
        num_points: int = 100,
        num_samples: int = 1000,
        wait: bool = True,
        force_compute: bool = False
    ) -> Tuple[Sequence[str], Mapping[str, Sequence], Mapping[str, Sequence]]:
        pds = self._get_partial_dependencies_as_proto(
            num_points, num_samples, wait, force_compute
        )
        return convert_PartialDependenceCache_to_tuple(pds)

    def _get_partial_dependencies_as_proto(
        self,
        num_points: int = 100,
        num_samples: int = 1000,
        wait: bool = True,
        force_compute: bool = False
    ) -> PartialDependenceCache:
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        if not wait:
            raise ValueError("For local computations `wait` must be `True`!")
        score_type = self._project_obj.score_type
        pre_df = self.get_xs()
        post_df = self._get_xs_post()
        hash_data_split = self._hash_data_split(post_df)
        computed_pds = self._pd_cache.get_pds(
            project_name=self._project_obj.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=self._base_data_split.name,
            hash_data_split=hash_data_split,
            score_type=score_type
        )
        if (computed_pds is not None) and (not force_compute):
            return computed_pds
        ys = self.get_ys() if self._base_data_split.has_labels else None
        model_func = LocalExplanationProcessor.get_explainer_scorer_from_score_type(
            self._model, score_type, has_labels=ys is not None and len(ys) > 0
        )
        computer = PartialDependencePlotComputer()
        with AbsoluteProgressBar() as progress_bar:
            pds = computer.compute_partial_dependence_plot(
                pre_df=pre_df,
                post_df=post_df,
                transform_if_possible_func=lambda xs: xs,
                pre_transform_column_names=list(pre_df.columns),
                post_transform_column_names=list(post_df.columns),
                feature_map=self._data_collection.feature_map,
                model_func=model_func,
                num_points=num_points,
                num_samples=num_samples,
                report_progress_func=progress_bar.set_percentage,
            )
        new_hash_data_split = self._hash_data_split(self._get_xs_post())
        if new_hash_data_split != hash_data_split:
            raise AssertionError(
                "Aborting because data split has been modified! Please call `get_partial_dependencies` again."
            )
        self._pd_cache.add_or_update_pds(
            pds=pds,
            project_name=self._project_obj.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=self._base_data_split.name,
            hash_data_split=hash_data_split,
            score_type=score_type
        )
        return pds

    def set_segment(self, segment_group_name: str, segment_name: str):
        self._project_obj._validate_segment_name(
            segment_group_name, segment_name
        )
        self._segment_context = SegmentContext(
            segment_group_name=segment_group_name, segment_name=segment_name
        )

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
        metric_types, interesting_segment_type = self._validate_suggest_high_error_segments(
            segment_type, metric_types, self._project_obj.score_type,
            comparison_data_split_name
        )
        score_type = self._project_obj.score_type
        if interesting_segment_type == InterestingSegment.Type.LOW_CLASSIFICATION_ACCURACY:
            score_type = "classification"
        all_xs = [self.get_xs()]
        all_ys = [self.get_ys()]
        all_ys_pred = [self._get_ys_pred(score_type=score_type)]
        if comparison_data_split_name is not None:
            comparison_explainer = copy(self)
            comparison_explainer.set_base_data_split(comparison_data_split_name)
            all_xs.append(comparison_explainer.get_xs())
            all_ys.append(comparison_explainer.get_ys())
            all_ys_pred.append(
                comparison_explainer._get_ys_pred(score_type=score_type)
            )
        pointwise_metrics = InterestingSegmentsProcessor.validate_and_get_pointwise_metrics(
            interesting_segment_type, all_ys, all_ys_pred
        )
        segments = InterestingSegmentsProcessor.find_interesting_segments(
            self.logger, all_xs, pointwise_metrics,
            InterestingSegmentsProcessor.pointwise_metrics_aggregator(
                minimum_size, size_exponent
            ), num_features, num_samples, random_state
        )
        stringify = lambda segment: FilterProcessor.stringify_filter(
            segment.filter_expression, ingestable=True
        )
        mp = defaultdict(list)
        total_size = all_ys_pred[0].shape[0]
        for segment in segments["segments"][:max_num_responses]:
            mp["representation"].append(stringify(segment))
            metrics = [
                self._compute_performance_df(
                    metric_type,
                    compute_for_comparison_data_splits=False,
                    overriding_filter_expression=segment.filter_expression
                )[metric_type][0] for metric_type in metric_types
            ]
            for i, metric_type in enumerate(metric_types):
                mp[metric_type].append(metrics[i])
            segment_size = np.sum(
                self._get_row_selector_for_filter_expression(
                    segment.filter_expression, self._base_data_split
                )
            )
            mp["size"].append(segment_size)
            mp["size (%)"].append(100 * segment_size / total_size)
        return pd.DataFrame(data=mp)

    def clear_segment(self):
        self._segment_context = SegmentContext(
            segment_group_name=None, segment_name=None
        )

    def compute_fairness(
        self,
        segment_group: str,
        segment1: str,
        segment2: Optional[str] = None,
        fairness_type: Optional[str] = 'DISPARATE_IMPACT_RATIO',
        threshold: Optional[float] = None,
        threshold_score_type: Optional[str] = None,
    ):
        raise NotImplementedError(
            "This functionality is not implemented locally!"
        )

    def list_fairness_metrics(self) -> Sequence[str]:
        raise NotImplementedError(
            "This functionality is not implemented locally!"
        )

    def list_performance_metrics(self) -> Sequence[str]:
        return list(self._regression_performance_metrics.keys()
                   ) if self._model.is_regression else list(
                       self._classification_performance_metrics.keys()
                   )

    def rank_performance(
        self, metric_type: str, ascending: bool = False
    ) -> pd.DataFrame:
        self._validate_metric_type(metric_type)
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        models_in_data_collection = self._workspace.get_models(
            data_collection_name=self._data_collection.name
        )
        ret = None
        column_names = []
        for model_name in models_in_data_collection:
            model_performance_df = self._compute_performance_df(
                metric_type, model=self._project_obj.models[model_name]
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
        ret.insert(0, "Model Name", models_in_data_collection)
        return ret.sort_values(column_names[0],
                               ascending=ascending).reset_index(drop=True)

    def _compute_performance_df(
        self,
        metric_type: str,
        compute_for_comparison_data_splits: bool = True,
        overriding_filter_expression: Optional[FilterExpression] = None,
        model: Optional[Model] = None
    ) -> pd.DataFrame:
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        if model is None:
            model = self._model
        allowable_performance_metrics = self.list_performance_metrics()
        score_type = self._project_obj.score_type
        if metric_type not in allowable_performance_metrics:
            raise ValueError(
                f"Unsupported performance metric {metric_type}. Available metrics: {allowable_performance_metrics}"
            )
        if not model.is_regression and metric_type not in metrics_util.THRESHOLD_INDEPENDENT_CLASSIFICATION_METRICS:
            score_type = "classification"
        metric_fn = self._regression_performance_metrics[
            metric_type
        ] if model.is_regression else self._classification_performance_metrics[
            metric_type]
        data_splits_to_consider = [self._base_data_split]
        if compute_for_comparison_data_splits and self._comparison_data_splits:
            data_splits_to_consider += self._comparison_data_splits
        split_names = []
        split_performances = []
        for split in data_splits_to_consider:
            split_names.append(split.name)
            all_ys_true = self._get_ys_for_split(split, ignore_segment=True)
            all_ys_pred = model.predict(
                self._get_xs_post_for_split(split, ignore_segment=True),
                score_type
            )
            row_selector = None
            if overriding_filter_expression is not None:
                row_selector = self._get_row_selector_for_filter_expression(
                    overriding_filter_expression, split
                )
            elif self._check_current_active_segment():
                row_selector = self._get_row_selector_for_segment(
                    segment_group_name=self._segment_context.segment_group_name,
                    segment_name=self._segment_context.segment_name,
                    data_split=split
                )
            if row_selector is not None:
                ys_true = all_ys_true[row_selector]
                ys_pred = all_ys_pred[row_selector]
            else:
                ys_true = all_ys_true
                ys_pred = all_ys_pred
            if metric_type == "SEGMENT_GENERALIZED_AUC":
                metric_val = metric_fn(
                    ys_true, ys_pred, all_ys_true, all_ys_pred
                )
            else:
                metric_val = metric_fn(ys_true, ys_pred)
            split_performances.append(metric_val)
        return pd.DataFrame.from_dict(
            {
                "Split": split_names,
                metric_type: split_performances
            }
        )

    def _validate_instability_score_type(
        self, score_type: Optional[str]
    ) -> str:
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        if score_type is None:
            return self._project_obj.score_type
        if self._model.is_regression:
            if score_type not in fi_constants.ALL_REGRESSION_SCORE_TYPES:
                raise ValueError(
                    f"Invalid score type {score_type} was provided. Valid influence score types for this model: {fi_constants.ALL_REGRESSION_SCORE_TYPES}"
                )
            return score_type
        if score_type not in fi_constants.ALL_CLASSIFICATION_SCORE_TYPES:
            raise ValueError(
                f"Invalid score type {score_type} was provided. Valid influence score types for this model: {fi_constants.ALL_CLASSIFICATION_SCORE_TYPES}"
            )
        return score_type

    def _compute_model_score_instability_df(
        self,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False
    ) -> pd.DataFrame:
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        if not self._comparison_data_splits:
            raise ValueError(
                "Model score drifts require comparison data splits. See `set_comparison_data_splits` for more information."
            )
        score_type = self._validate_instability_score_type(score_type)
        base_split_name = self._base_data_split.name
        base_ys_pred = self._model.predict(
            self._get_xs_post_for_split(self._base_data_split), score_type
        )
        split_names = []
        split_drift = []
        for split in self._comparison_data_splits:
            split_names.append(split.name)
            ys_pred = self._model.predict(
                self._get_xs_post_for_split(split), score_type
            )
            distribution_processor = metrics_util.DistributionProcessor(
                base_ys_pred, ys_pred
            )
            split_drift.append(
                distribution_processor.difference_of_means(
                ) if use_difference_of_means else distribution_processor.
                wasserstein_distance()
            )
        stability_data = pd.DataFrame()
        stability_data["Comparison Split"] = split_names
        stability_data["Base Split"] = base_split_name
        stability_data["Model Score Instability"] = split_drift
        return stability_data

    def compute_feature_contributors_to_instability(
        self,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False
    ) -> pd.DataFrame:
        self._ensure_data_split()
        self._ensure_feature_map_if_needed()
        if not self._comparison_data_splits:
            raise ValueError(
                "Feature contributors to instability require comparison data splits. See `set_comparison_data_splits` for more information."
            )
        score_type = self._validate_instability_score_type(score_type)
        base_influences = self.get_feature_influences(score_type=score_type)
        feature_contributors = []
        split_names = []
        for split in self._comparison_data_splits:
            split_names.append(split.name)
            split_contributor_row = {}
            compare_influences = self._get_feature_influences_nonbase_split(
                split.name, score_type=score_type
            )
            for feature_col in base_influences.columns:
                distribution_processor = metrics_util.DistributionProcessor(
                    base_influences[feature_col],
                    compare_influences[feature_col]
                )
                split_contributor_row[
                    feature_col
                ] = distribution_processor.difference_of_means(
                ) if use_difference_of_means else distribution_processor.wasserstein_distance(
                )
            split_contributor_row = pd.Series(split_contributor_row)
            total_contribution = split_contributor_row.abs().sum()
            if total_contribution != 0:
                split_contributor_row /= total_contribution
            feature_contributors.append(split_contributor_row.to_frame().T)
        resp = pd.concat(feature_contributors)
        resp.set_index(pd.Index(split_names), inplace=True)
        return resp

    def compute_estimated_performance(self,
                                      metric_type: str) -> Tuple[float, str]:
        raise NotImplementedError(
            "This functionality is not implemented locally!"
        )

    def get_influences_background_data_split_or_set_from_default(
        self
    ) -> DataSplit:
        # Returns background split for compute influences if it has already been set in the data_collection.
        # Otherwise set influences background split from default and return it.
        if self._data_collection.base_split is not None:
            return self._data_collection.base_split
        background_split = self._data_collection.get_default_data_split(
            self.get_base_data_split()
        )
        if not background_split:
            raise ValueError("Cannot determine background data split!")
        self.logger.warning(
            f"Background split for `data_collection` \"{self._data_collection.name}\" is currently not set. Setting it to \"{background_split.name}\""
        )
        self._data_collection.set_base_split(background_split.name)
        return self._data_collection.get_default_data_split()

    def _convert_start_stop(self, start: Optional[int], stop: Optional[int]):
        if start is None:
            start = 0
        max_length = self._base_data_split.xs_pre.shape[0]
        if stop is None or stop > max_length:
            stop = max_length
        if start >= stop:
            raise ValueError("`start` must be less than `stop`!")
        return start, stop

    def _add_feature_influences_from_cache(
        self, data_split_name: str, qiis: np.ndarray, num_samples: int,
        explanation_algorithm_type: ExplanationAlgorithmType
    ):
        xs = self.get_xs(0, self._project_obj.num_default_influences)
        cols = list(xs.columns)
        hash_xs = pd.util.hash_pandas_object(xs).to_numpy().reshape(-1, 1)
        bg = self.get_influences_background_data_split_or_set_from_default(
        ).xs_post
        hash_bg = self._hash_data_split(bg)
        computed_qiis = pd.DataFrame(
            data=np.concatenate([hash_xs, qiis], axis=1),
            columns=["hash_xs"] + cols
        )
        self._qii_cache.add_or_update_influences(
            influences=computed_qiis,
            project_name=self._project_obj.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=data_split_name,
            hash_bg=hash_bg,
            score_type=self._project_obj.score_type,
            algorithm=explanation_algorithm_type,
            num_samples=num_samples
        )

    def _validate_data_split(self, data_split_name: str) -> None:
        if data_split_name not in self._data_collection.data_splits.keys():
            raise ValueError(f"No such data split \"{data_split_name}\"!")

    def _check_current_active_segment(self) -> bool:
        if self._segment_context.segment_name:
            try:
                self._project_obj._validate_segment_name(
                    self._segment_context.segment_group_name,
                    self._segment_context.segment_name
                )
            except NotFoundError:
                self.logger.warning(
                    f"Segment {self._segment_context.segment_name} no longer exists. Unsetting segment in explainer."
                )
                self.clear_segment()
                return False
            return True
        return False
