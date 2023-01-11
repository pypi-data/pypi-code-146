from __future__ import annotations

import copy
import importlib
import logging
import tempfile
from typing import (
    Any, Dict, Mapping, NamedTuple, Optional, Sequence, TYPE_CHECKING, Union
)

import numpy as np
import pandas as pd
import scipy.sparse as sparse
from scipy.special import logit

from truera.artifactrepo.utils.filter_utils import \
    parse_expression_to_filter_proto
from truera.client.client_utils import validate_feature_names
from truera.client.errors import NotFoundError
from truera.client.intelligence.segment import Segment
from truera.client.intelligence.segment import SegmentGroup
from truera.client.util import workspace_validation_utils
# pylint: disable=no-name-in-module
from truera.protobuf.public.data.segment_pb2 import Segment as SegmentProto
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
from truera.protobuf.public.metadata_message_types_pb2 import \
    FeatureTransformationType
from truera.protobuf.public.modelrunner.cache_entries_pb2 import \
    PartialDependenceCache
from truera.protobuf.public.qoi_pb2 import ExplanationAlgorithmType
# pylint: enable=no-name-in-module
from truera.public.feature_influence_constants import \
    get_valid_score_type_for_output_type
from truera.public.feature_influence_constants import LOGIT_CLIP_RANGE
from truera.public.feature_influence_constants import \
    SCORE_TYPE_TO_MODEL_OUTPUT
from truera.public.feature_influence_constants import VALID_MODEL_OUTPUT_TYPES
from truera.utils import filter_constants
from truera.utils.filter_utils import FilterProcessor
from truera.utils.pyspark_util import is_supported_pyspark_tree_model

if TYPE_CHECKING:
    from truera.client.nn import wrappers as base

SUPPORTED_MODEL_BACKENDS = [None, "tf1", "tf2", "pytorch"]
DEFAULT_NUM_SAMPLES = 1000


class Project:

    def __init__(
        self, name: str, score_type: str, input_type: str,
        num_default_influences: int
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.score_type = score_type
        self.data_collections: Dict[str, DataCollection] = {}
        self.models: Dict[str, Model] = {}
        self.input_type = input_type
        self.num_default_influences = num_default_influences
        self.segment_groups: Dict[str, SegmentGroup] = {}
        self.num_samples: int = DEFAULT_NUM_SAMPLES
        self.influence_algorithm: Optional[str] = None

    def set_influence_algorithm(self, algorithm: Optional[str] = None):
        has_shap = importlib.util.find_spec("shap")
        has_qii = importlib.util.find_spec("truera_qii")
        if algorithm:
            workspace_validation_utils.validate_feature_influence_algorithm_generic(
                algorithm
            )
            if (algorithm == "truera-qii" and
                not has_qii) or (algorithm == "shap" and not has_shap):
                raise ValueError(
                    f"Could not set influence algorithm to `{algorithm}` as the package is not installed!"
                )

            self.influence_algorithm = algorithm

        else:
            if self.input_type == "text" or self.input_type == "time_series_tabular":
                self.influence_algorithm = "integrated-gradients"
            elif has_qii:
                self.influence_algorithm = "truera-qii"
            elif has_shap:
                self.influence_algorithm = "shap"
            else:
                raise ValueError(
                    "Could not infer feature influence algorithm type! Must install one of `shap` or `truera-qii`."
                )

    def get_influence_algorithm(self) -> str:
        if self.influence_algorithm is None:
            self.set_influence_algorithm()
        return self.influence_algorithm

    def add_data_collection(
        self, name: str, transform_type: FeatureTransformationType
    ) -> None:
        if name in self.data_collections:
            raise ValueError(
                f"Data collection {name} already exists in project {self.name}!"
            )
        self.data_collections[name] = DataCollection(name, transform_type)

    def add_model_obj(
        self,
        model_name: str,
        model_obj,
        transform_obj,
        data_collection_name: str,
        model_output_type: str,
        model_type: Optional[str] = 'tabular',
        model_run_wrapper: Optional[base.Wrappers.ModelRunWrapper] = None,
        classification_threshold: Optional[float] = None,
        feature_transform_type:
        FeatureTransformationType = FEATURE_TRANSFORM_TYPE_NO_TRANSFORM,
        verify_model: bool = False
    ) -> None:
        if model_name in self.models:
            raise ValueError(
                f"Model {model_name} already exists in project {self.name}!"
            )
        if data_collection_name not in self.data_collections:
            raise ValueError(
                f"Data collection {data_collection_name} does not already exist in project {self.name}!"
            )
        self.models[model_name] = Model(
            model_name,
            model_obj,
            self.data_collections[data_collection_name],
            model_output_type,
            model_type,
            model_run_wrapper,
            classification_threshold=classification_threshold,
            transform_obj=transform_obj,
            feature_transform_type=feature_transform_type,
            verify_model=verify_model
        )

    def clear_train_split_from_models(self, train_split_name: str) -> None:
        for model_name, model in self.models.items():
            if model.train_split_name == train_split_name:
                self.logger.info(
                    f"Clearing train split \"{train_split_name}\" from model \"{model_name}\""
                )
                model.train_split_name = None

    def add_segment_group(
        self,
        name: str,
        segment_definitions,
        data_collection_name: str,
        data_split_name: Optional[str] = None
    ) -> None:
        segments: Dict[Segment] = {}
        for segment_name in segment_definitions:
            filter_expression = parse_expression_to_filter_proto(
                segment_definitions[segment_name]
            )
            filter_requirements = FilterProcessor.get_filter_requirements(
                filter_expression
            )
            models_in_filter = filter_requirements.model_ids_to_score_type.keys(
            ) - {filter_constants.GENERIC_MODEL_ID}
            if models_in_filter:
                models_in_dc = [
                    i for i in self.models.keys() if
                    self.models[i].data_collection.name == data_collection_name
                ]
                nonexistent_model_ids = models_in_filter - set(models_in_dc)
                if nonexistent_model_ids:
                    raise NotFoundError(
                        f"The provided `segment_definitions` contains model(s) that doesn't exist: {nonexistent_model_ids} in data collection \"{data_collection_name}\"."
                    )

            if data_collection_name and data_split_name:
                self._validate_feature_names(
                    filter_requirements.column_names,
                    data_collection_name,
                    data_split_name,
                    extra_data=True,
                    allow_label_or_model_column=True
                )
            segment_proto = SegmentProto(
                name=segment_name, filter_expression=filter_expression
            )
            segments[segment_name] = Segment(
                name=segment_name,
                project_id=self.name,
                segment_proto=segment_proto
            )
        self.segment_groups[name] = SegmentGroup(
            name=name, id=None, segments=segments, segmentation_proto=None
        )

    def get_segment_groups(self) -> Mapping[str, SegmentGroup]:
        return copy.deepcopy(self.segment_groups)

    def get_segment_group(self, name: str) -> SegmentGroup:
        self._validate_segment_group_name(name)
        return copy.deepcopy(self.segment_groups[name])

    def get_segment(
        self, segment_group_name: str, segment_name: str
    ) -> Segment:
        self._validate_segment_name(segment_group_name, segment_name)
        segment_group = self.get_segment_group(segment_group_name)
        return segment_group.segments[segment_name]

    def delete_segment_group(self, name: str) -> None:
        self._validate_segment_group_name(name)
        del self.segment_groups[name]

    def ensure_can_delete_data_collection(self, name, recursive=False):
        if name not in self.data_collections:
            raise ValueError(
                f"Cannot find the requested data collection [{name}] in the project."
            )
        if not recursive and self.data_collections[name].data_splits:
            raise ValueError(
                "Cannot delete data collection as it contains splits. Please delete the splits or pass recursive=True"
            )

        for model in self.models.values():
            if model.data_collection.name == name:
                raise ValueError(
                    f"Cannot delete this data collection as it is attached to model: {model.name}"
                )

    def ensure_can_delete_project(self, recursive=False):
        if recursive:
            return
        if self.models:
            raise ValueError(
                f"Cannot delete project as it contains one or more models. Please delete the models and data_collections or pass recursive=True."
            )
        if self.data_collections:
            raise ValueError(
                "Cannot delete project as it contains one or more data_collections. Please delete the models and data_collections or pass recursive=True."
            )

    def _validate_feature_names(
        self,
        feature_names: Sequence[str],
        data_collection_name: str,
        data_split_name: str,
        extra_data: bool = False,
        allow_label_or_model_column: bool = False
    ) -> None:
        # Need to explicitly cast to str in case some column names are numbers
        valid_names = [
            str(i) for i in list(
                self.data_collections[data_collection_name].
                data_splits[data_split_name].xs_pre.columns
            )
        ]
        if extra_data and self.data_collections[
            data_collection_name].data_splits[data_split_name].extra is not None:
            valid_names += [
                str(i) for i in list(
                    self.data_collections[data_collection_name].
                    data_splits[data_split_name].extra.columns
                )
            ]
        validate_feature_names(
            feature_names=feature_names,
            valid_feature_names=valid_names,
            score_type=self.score_type,
            allow_label_or_model_column=allow_label_or_model_column
        )

    def _validate_segment_group_name(self, name: str) -> None:
        if name not in self.segment_groups:
            raise NotFoundError(
                f"Segment group \"{name}\" does not exist in project \"{self.name}\""
            )

    def _validate_segment_name(
        self, segment_group_name: str, segment_name: str
    ) -> None:
        segment_group = self.get_segment_group(segment_group_name)
        if segment_name not in segment_group.segments:
            raise NotFoundError(
                f"Segment \"{segment_name}\" does not exist in segment group \"{segment_group_name}\""
            )


class DataCollection:

    def __init__(
        self, name: str, feature_transform_type: FeatureTransformationType
    ) -> None:
        self.name = name
        self.feature_transform_type = feature_transform_type
        self.data_splits: Dict[str, Union[DataSplit, NNDataSplit]] = {}
        self.feature_map: Optional[Dict[str, Sequence[str]]] = None
        self.base_split: Union[DataSplit, NNDataSplit] = None

    def get_default_data_split(self, data_split_name: Optional[str] = None):
        if self.base_split:
            return self.base_split
        for _, data_split in self.data_splits.items():
            if data_split.split_type in ["all", "train"]:
                return data_split
        return self.data_splits.get(data_split_name)

    def add_data_split(
        self, name: str, xs_pre: pd.DataFrame, xs_post: pd.DataFrame,
        extra: Optional[pd.DataFrame],
        ys: Optional[Union[np.ndarray, pd.Series]], split_type: str
    ) -> None:
        xs_pre = xs_pre.reset_index(drop=True)
        post_cols = set()

        if xs_post is not None:
            xs_post = xs_post.reset_index(drop=True)
            post_cols = set(xs_post.columns)
        if extra is not None:
            extra = extra.reset_index(drop=True)
        pre_cols = set(xs_pre.columns)

        for curr_split_name in self.data_splits:
            curr_split_pre_cols = set(
                self.data_splits[curr_split_name].xs_pre.columns
            )
            existing_post = self.data_splits[curr_split_name]._xs_post
            curr_split_post_cols = set()
            if existing_post is not None:
                curr_split_post_cols = set(existing_post.columns)
            if curr_split_pre_cols != pre_cols or curr_split_post_cols != post_cols:
                raise ValueError(
                    f"Split \"{name}\" doesn't match schema of existing split \"{curr_split_name}\" which is already in the data collection."
                )
            break
        if isinstance(ys, np.ndarray):
            ys = pd.Series(ys, name="ground_truth", index=xs_pre.index)
        elif isinstance(ys, pd.Series):
            ys = ys.reset_index(drop=True)
        self.data_splits[name] = DataSplit(
            name=name,
            xs_pre=xs_pre,
            xs_post=xs_post,
            extra=extra,
            ys=ys,
            split_type=split_type
        )

    def add_nn_data_split(
        self,
        name: str,
        truera_wrappers: base.WrapperCollection,
        split_type: str,
        xs_pre: Optional[pd.DataFrame] = None,
        ys: Optional[pd.DataFrame] = None,
        extra_data_df: Optional[pd.DataFrame] = None
    ) -> None:
        self.data_splits[name] = NNDataSplit(
            name, truera_wrappers, split_type, xs_pre, ys, extra_data_df
        )

    def set_feature_map(self, feature_map: Optional[Dict[str, Sequence[str]]]):
        self.feature_map = feature_map

    def set_base_split(self, data_split_name: str) -> None:
        self.validate_data_split(data_split_name)
        self.base_split = self.data_splits[data_split_name]

    def delete_data_split(self, data_split_name: str) -> None:
        self.validate_data_split(data_split_name)
        if self.base_split and self.base_split.name == data_split_name:
            self.base_split = None
        del self.data_splits[data_split_name]

    def validate_data_split(self, data_split_name: str) -> None:
        if data_split_name not in self.data_splits:
            raise ValueError(
                f"No such data split \"{data_split_name}\" in data collection \"{self.name}\"!"
            )


class DataSplit:

    def __init__(
        self, name: str, xs_pre: pd.DataFrame, xs_post: Optional[pd.DataFrame],
        extra: Optional[pd.DataFrame], ys: Union[np.ndarray,
                                                 pd.Series], split_type: str
    ) -> None:
        self.name = name
        self.xs_pre = xs_pre
        self._xs_post = xs_post
        self.extra = extra
        self.ys = ys
        self.split_type = split_type

    @property
    def has_labels(self):
        return self.ys is not None and self.ys.size > 0

    @property
    def xs_post(self):
        if self._xs_post is None:
            return self.xs_pre
        else:
            return self._xs_post


class NNDataSplit:

    def __init__(
        self,
        name: str,
        truera_wrappers: base.WrapperCollection,
        split_type: str,
        xs_pre: Optional[pd.DataFrame] = None,
        ys: Optional[pd.DataFrame] = None,
        extra_data_df: Optional[pd.DataFrame] = None
    ) -> None:
        self.name = name
        self.truera_wrappers = truera_wrappers
        self.split_type = split_type
        self.xs_pre = xs_pre
        self.ys = ys
        self.extra_data_df = extra_data_df


class Model:

    def __init__(
        self,
        name: str,
        model_obj,
        data_collection: DataCollection,
        model_output_type: str,
        model_type: str,
        model_run_wrapper: Optional[base.Wrappers.ModelRunWrapper] = None,
        classification_threshold: float = None,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        transform_obj: Optional[Any] = None,
        feature_transform_type:
        FeatureTransformationType = FEATURE_TRANSFORM_TYPE_NO_TRANSFORM,
        verify_model: bool = True
    ) -> None:
        self.name = name
        self.model_obj = model_obj
        self.transform_obj = transform_obj
        self.data_collection = data_collection
        if model_output_type not in VALID_MODEL_OUTPUT_TYPES:
            raise ValueError(
                f"{model_output_type} is not a valid model output type! Must be one of {VALID_MODEL_OUTPUT_TYPES}."
            )
        self.model_output_type = model_output_type
        self.model_type = model_type
        self.classification_threshold = classification_threshold
        self.train_split_name = train_split_name
        self.train_parameters = train_parameters
        self.feature_transform_type = feature_transform_type

        if model_type == 'rnn' or model_type == 'nlp':
            self.model_run_wrapper = model_run_wrapper
            return

        cls = self.model_obj.__class__
        module = cls.__module__
        name = cls.__name__
        if feature_transform_type == FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION:
            if module.startswith("sklearn.pipeline"):
                if len(model_obj.named_steps) > 1:
                    self.transform_obj = model_obj[:-1]
                    self.model_obj = model_obj[-1]
        if callable(self.model_obj):
            if model_output_type == "classification":

                def _base_predict_func(xs):
                    ret = self.model_obj(xs)
                    if len(ret.shape) != 2 or ret.shape[
                        1] != 2 or not isinstance(ret, pd.DataFrame):
                        raise ValueError(
                            "Provided callable classification model must return a pandas DataFrame of shape (?, 2)!"
                        )
                    return self.model_obj(xs).iloc[:, 1].to_numpy()

                self._base_predict_func = _base_predict_func
            elif model_output_type == "regression":
                self._base_predict_func = self.model_obj
        elif "xgboost.core" == module and "Booster" == name:
            from xgboost import DMatrix
            self._base_predict_func = lambda xs: self.model_obj.predict(
                DMatrix(xs), validate_features=False
            )
        elif is_supported_pyspark_tree_model(self.model_obj):
            self._base_predict_func = None
        elif model_output_type == "classification":
            if "predict_proba" in dir(self.model_obj):
                self._base_predict_func = lambda xs: self.model_obj.predict_proba(
                    xs
                )[:, 1]
            elif "predict" in dir(self.model_obj):
                self._base_predict_func = lambda xs: self.model_obj.predict(xs)
            else:
                raise ValueError(
                    "Provided model has neither predict_proba or predict function!"
                )
        elif model_output_type == "regression":
            if not hasattr(self.model_obj, "predict"):
                raise ValueError("Provided model has no predict function!")
            else:
                self._base_predict_func = self.model_obj.predict
        if verify_model:
            score = get_valid_score_type_for_output_type(model_output_type)[0]
            data = self._get_data_for_model()
            if data is not None:
                self.predict(data.iloc[:2], score)

    def _get_data_for_model(self):
        data_collection = self.data_collection
        if data_collection:
            data_split = data_collection.get_default_data_split()
            if data_split:
                return data_split.xs_post

    def transform(self, xs: pd.DataFrame) -> pd.DataFrame:
        transformed_data = xs
        if self.transform_obj and self.feature_transform_type == FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION:
            if callable(self.transform_obj):
                transformed_data = self.transform_obj(xs)
            else:
                transformed_data = self.transform_obj.transform(xs)
            if isinstance(transformed_data, pd.DataFrame):
                return transformed_data
            try:
                post_transform_features = self.transform_obj.get_feature_names_out(
                )
            except:
                raise AssertionError(
                    "Expected transform object to output a DataFrame or implement the `get_feature_names_out()` function to retrieve post features!"
                )
            if isinstance(transformed_data, sparse.csr_matrix):
                cls = self.model_obj.__class__
                module = cls.__module__
                if module.startswith("xgboost"):
                    return pd.DataFrame(
                        transformed_data.toarray(),
                        columns=post_transform_features
                    ).replace({0: np.nan})
                else:
                    return pd.DataFrame.sparse.from_spmatrix(
                        transformed_data, columns=post_transform_features
                    )
            else:
                return pd.DataFrame(
                    transformed_data, columns=post_transform_features
                )
        elif self.transform_obj is None and self.feature_transform_type == FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION:
            raise ValueError(
                "Specify transform function to use this data collection!"
            )
        else:
            return transformed_data

    def predict(self, xs: pd.DataFrame, score_type: str) -> np.ndarray:
        xs = self.transform(xs)
        if is_supported_pyspark_tree_model(self.model_obj):
            from truera_qii.shap.explainers._tree import \
                Tree as ShapTreeExplainer
            if len(xs) == 0:
                # If the xs DataFrame is empty, the ShapTreeExplainer cannot be initialized.
                # Return an empty array instead.
                return np.array([])
            ret = ShapTreeExplainer(
                model=self.model_obj,
                data=xs,
                model_output=SCORE_TYPE_TO_MODEL_OUTPUT[score_type],
                feature_perturbation="interventional"
            ).model.predict(xs)
            if ret.ndim == 2 and ret.shape[1] == 2:
                ret = ret[:, 1]
        else:
            ret = self._base_predict_func(xs)
        if score_type in ["regression", "probits"]:
            return ret
        if score_type == "logits":
            return np.clip(logit(ret), LOGIT_CLIP_RANGE[0], LOGIT_CLIP_RANGE[1])
        if score_type == "classification":
            return (ret >= self.classification_threshold).astype(int)
        raise ValueError(f"Invalid score type: {score_type}!")

    def set_classification_threshold(
        self, classification_threshold: float
    ) -> None:
        self.classification_threshold = classification_threshold

    @property
    def is_regression(self) -> bool:
        return self.model_output_type == "regression"


class Cache:

    def __init__(self):
        self._entries = {}
        self._temp_dirs = {}

    def _add_or_update(self, hash_key: NamedTuple, entry: Any) -> None:
        self._entries[hash_key] = entry

    def _get(self, hash_key: NamedTuple) -> Any:
        return self._entries.get(hash_key)

    def _get_temp_dir(
        self, hash_key: NamedTuple
    ) -> tempfile.TemporaryDirectory:
        if hash_key not in self._temp_dirs:
            self._temp_dirs[hash_key] = tempfile.TemporaryDirectory()
        return self._temp_dirs[hash_key]

    def cleanup_cache_for_model(
        self, project_name: str, model_name: str
    ) -> None:
        to_remove = []
        for hash_key in self._temp_dirs:
            if hash_key.project_name == project_name and hash_key.model_name == model_name:
                to_remove.append(hash_key)
        for hash_key in to_remove:
            del self._temp_dirs[hash_key]

        to_remove = []
        for hash_key in self._entries:
            if hash_key.project_name == project_name and hash_key.model_name == model_name:
                to_remove.append(hash_key)
        for hash_key in to_remove:
            del self._entries[hash_key]

    def cleanup_cache_for_data_split(
        self, project_name: str, data_collection_name: str, data_split_name: str
    ) -> None:
        to_remove = []
        for hash_key in self._temp_dirs:
            if hash_key.project_name == project_name and hash_key.data_collection_name == data_collection_name and hash_key.data_split_name == data_split_name:
                to_remove.append(hash_key)
        for hash_key in to_remove:
            del self._temp_dirs[hash_key]

        to_remove = []
        for hash_key in self._entries:
            if hash_key.project_name == project_name and hash_key.data_collection_name == data_collection_name and hash_key.data_split_name == data_split_name:
                to_remove.append(hash_key)
        for hash_key in to_remove:
            del self._entries[hash_key]


class QiiCache(Cache):

    def __init__(self):
        super().__init__()
        # defines the max num_sample value per project for which this cache is still valid
        self.max_num_samples_per_project = {}

    def _clean_cache_num_samples_before_add(
        self, project_name: str, requested_num_samples: int
    ):
        # update max to what was requested
        curr_max_num_samples = self.max_num_samples_per_project.get(
            project_name, requested_num_samples
        )
        self.max_num_samples_per_project[project_name] = requested_num_samples

        # if requested > old max, invalidate cache
        if requested_num_samples > curr_max_num_samples:
            for qii_hashkey in list(self._entries.keys()):
                if qii_hashkey.project_name == project_name:
                    del self._entries[qii_hashkey]

    def _clean_cache_num_samples_before_get(
        self, project_name: str, requested_num_samples: int
    ):
        # if requested > old max, invalidate cache
        if requested_num_samples > self.max_num_samples_per_project.get(
            project_name, requested_num_samples
        ):
            for qii_hashkey in list(self._entries.keys()):
                if qii_hashkey.project_name == project_name:
                    del self._entries[qii_hashkey]

    class QiiHashKey(NamedTuple):
        project_name: str
        model_name: str
        data_collection_name: str
        data_split_name: str
        hash_bg: str
        score_type: str
        algorithm: ExplanationAlgorithmType

        def __post_init__(self):
            assert self.project_name, "project_name cannot be `None` or empty string!"
            assert self.model_name, "model_name cannot be `None` or empty string!"
            assert self.data_collection_name, "data_collection_name cannot be `None` or empty string!"
            assert self.data_split_name, "data_split_name cannot be `None` or empty string!"
            assert self.hash_bg, "hash_bg cannot be `None` or empty string!"
            assert self.score_type, "score_type cannot be `None` or empty string!"

    def add_or_update_influences(
        self, influences: pd.DataFrame, project_name: str, model_name: str,
        data_collection_name: str, data_split_name: str, hash_bg: str,
        score_type: str, algorithm: ExplanationAlgorithmType, num_samples: int
    ) -> None:
        self._clean_cache_num_samples_before_add(project_name, num_samples)
        hash_key = QiiCache.QiiHashKey(
            project_name=project_name,
            model_name=model_name,
            data_collection_name=data_collection_name,
            data_split_name=data_split_name,
            hash_bg=hash_bg,
            score_type=score_type,
            algorithm=algorithm
        )
        self._add_or_update(hash_key, influences)

    def get_qiis(
        self, project_name: str, model_name: str, data_collection_name: str,
        data_split_name: str, hash_bg: str, score_type: str, num_samples: int
    ) -> Optional[pd.DataFrame]:
        self._clean_cache_num_samples_before_get(project_name, num_samples)
        hash_key = QiiCache.QiiHashKey(
            project_name=project_name,
            model_name=model_name,
            data_collection_name=data_collection_name,
            data_split_name=data_split_name,
            hash_bg=hash_bg,
            score_type=score_type,
            algorithm=ExplanationAlgorithmType.TRUERA_QII
        )
        return self._get(hash_key)

    def get_shap_values(
        self, project_name: str, model_name: str, data_collection_name: str,
        data_split_name: str, hash_bg: str, score_type: str, num_samples: int
    ) -> Optional[pd.DataFrame]:
        self._clean_cache_num_samples_before_get(project_name, num_samples)
        for algorithm in [
            ExplanationAlgorithmType.TREE_SHAP_INTERVENTIONAL,
            ExplanationAlgorithmType.KERNEL_SHAP
        ]:
            values = self._get(
                QiiCache.QiiHashKey(
                    project_name=project_name,
                    model_name=model_name,
                    data_collection_name=data_collection_name,
                    data_split_name=data_split_name,
                    hash_bg=hash_bg,
                    score_type=score_type,
                    algorithm=algorithm
                )
            )
            if values is not None:
                return values

    def get_feature_influence_by_algorithm(
        self, project_name: str, model_name: str, data_collection_name: str,
        data_split_name: str, hash_bg: str, score_type: str, num_samples: int,
        algorithm: ExplanationAlgorithmType
    ) -> Optional[pd.DataFrame]:
        self._clean_cache_num_samples_before_get(project_name, num_samples)
        return self._get(
            QiiCache.QiiHashKey(
                project_name=project_name,
                model_name=model_name,
                data_collection_name=data_collection_name,
                data_split_name=data_split_name,
                hash_bg=hash_bg,
                score_type=score_type,
                algorithm=algorithm
            )
        )

    def get_temp_dir(
        self, project_name: str, model_name: str, data_collection_name: str,
        data_split_name: str, hash_bg: str, score_type: str,
        algorithm: ExplanationAlgorithmType
    ) -> tempfile.TemporaryDirectory:
        hash_key = QiiCache.QiiHashKey(
            project_name=project_name,
            model_name=model_name,
            data_collection_name=data_collection_name,
            data_split_name=data_split_name,
            hash_bg=hash_bg,
            score_type=score_type,
            algorithm=algorithm
        )
        return self._get_temp_dir(hash_key)


class PdCache(Cache):

    class PdHashKey(NamedTuple):
        project_name: str
        model_name: str
        data_collection_name: str
        data_split_name: str
        hash_data_split: str
        score_type: str

        def __post_init__(self):
            assert self.project_name, "project_name cannot be `None` or empty string!"
            assert self.model_name, "model_name cannot be `None` or empty string!"
            assert self.data_collection_name, "data_collection_name cannot be `None` or empty string!"
            assert self.data_split_name, "data_split_name cannot be `None` or empty string!"
            assert self.hash_data_split, "hash_data_split cannot be `None` or empty string!"
            assert self.score_type, "score_type cannot be `None` or empty string!"

    def add_or_update_pds(
        self, pds: PartialDependenceCache, project_name: str, model_name: str,
        data_collection_name: str, data_split_name: str, hash_data_split: str,
        score_type: str
    ) -> None:
        hash_key = PdCache.PdHashKey(
            project_name=project_name,
            model_name=model_name,
            data_collection_name=data_collection_name,
            data_split_name=data_split_name,
            hash_data_split=hash_data_split,
            score_type=score_type
        )
        self._add_or_update(hash_key, pds)

    def get_pds(
        self, project_name: str, model_name: str, data_collection_name: str,
        data_split_name: str, hash_data_split: str, score_type: str
    ) -> pd.DataFrame:
        hash_key = PdCache.PdHashKey(
            project_name=project_name,
            model_name=model_name,
            data_collection_name=data_collection_name,
            data_split_name=data_split_name,
            hash_data_split=hash_data_split,
            score_type=score_type
        )
        return self._get(hash_key)
