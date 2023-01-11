from __future__ import annotations

import itertools
import logging
from typing import Any, Mapping, Optional, Sequence, TYPE_CHECKING, Union

import numpy as np
import pandas as pd

from truera.client.client_utils import get_input_data_format_from_string
from truera.client.client_utils import STR_TO_EXPLANATION_ALGORITHM_TYPE
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.protobuf.public.aiq import intelligence_service_pb2 as is_pb
# pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.accuracy_pb2 import AccuracyType
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_PRE_POST_DATA
from truera.protobuf.public.metadata_message_types_pb2 import \
    FeatureTransformationType
from truera.protobuf.public.metadata_message_types_pb2 import InputDataFormat
from truera.protobuf.public.qoi_pb2 import ExplanationAlgorithmType
# pylint: enable=no-name-in-module
from truera.protobuf.public.util import split_mode_pb2 as sm_pb
from truera.public.artifact_repo_lib import \
    ensure_valid_identifier as check_identifier
import truera.public.feature_influence_constants as fi_constants

if TYPE_CHECKING:
    from truera.client.ingestion_client import Table

VALID_SPLIT_TYPES = [
    "all", "train", "test", "validate", "oot", "prod", "custom"
]


def validate_influence_type_str_for_virtual_model_upload(
    provided_influence_type: str, project_influence_type: str
) -> ExplanationAlgorithmType:
    use_shap = project_influence_type != "truera-qii"

    # allow algorithm to be inferred if QII.
    if not use_shap and provided_influence_type is None:
        return ExplanationAlgorithmType.TRUERA_QII
    if provided_influence_type not in STR_TO_EXPLANATION_ALGORITHM_TYPE:
        raise ValueError(
            f"Expected `influence_type` to be one of {list(STR_TO_EXPLANATION_ALGORITHM_TYPE.keys())}!"
        )
    if use_shap and not "shap" in provided_influence_type:
        raise ValueError(
            "Influence type of project is set to shap. Provided feature influences must be calculated using one of \"kernel-shap\",  \"tree-shap-path-dependent\", \"tree-shap-interventional\"!"
        )
    elif not use_shap and provided_influence_type != "truera-qii":
        raise ValueError(
            "Influence type of project is set to truera-qii. Provided feature influences must be calculated using \"truera-qii\"."
        )
    return STR_TO_EXPLANATION_ALGORITHM_TYPE[provided_influence_type]


def verify_label_values_for_classification(ys: Union[pd.Series, np.ndarray]):
    if not np.isin(ys, [0, 1]).all():
        raise ValueError(
            "Classification models require label data to be binary!"
        )


def verify_label_values_for_regression(ys: Union[pd.Series, np.ndarray]):
    if not pd.api.types.is_numeric_dtype(ys):
        raise ValueError("Regression models require label data to be numeric!")


def is_nlp_project(input_type: str) -> bool:
    return get_input_data_format_from_string(input_type) == InputDataFormat.TEXT


def is_rnn_project(input_type: str) -> bool:
    return get_input_data_format_from_string(
        input_type
    ) == InputDataFormat.TIME_SERIES_TABULAR


def is_nontabular_project(input_type: str) -> bool:
    return is_nlp_project(input_type) or is_rnn_project(input_type)


def is_tabular_project(input_type: str) -> bool:
    # legacy projects can have UNKNOWN input data types, so this safeguards against that.
    return not is_nontabular_project(input_type)


def _assert_dataframe_columns_are_strings(df: pd.DataFrame, df_name: str):
    for col in df.columns:
        if not isinstance(col, str):
            raise ValueError(
                f"Found column name {col} in `{df_name}` of type {type(col)} but expected `str`!"
            )


def _assert_is_dataframe(df: Any, df_name: str):
    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"`{df_name}` must be of type `pandas.DataFrame`!")


def _assert_df_shape_matches_pre(
    df: pd.DataFrame, df_name: str, pre_data: pd.DataFrame
):
    if len(pre_data) != len(df):
        raise ValueError(
            f"`pre_data` and `{df_name}` must have the same number of rows! `pre_data` has {len(pre_data)} but `{df_name}` has {len(df)}."
        )


def _assert_labels_are_single_dim(
    label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]],
    id_column_name: Optional[str]
):
    expected_label_cols = 1 + (1 if id_column_name is not None else 0)
    if label_data is not None and (
        label_data.ndim > expected_label_cols and
        label_data.shape[1] != expected_label_cols
    ):
        raise ValueError(
            f"`label_data` has {label_data.shape[1]} columns! Pass in a one-dimensional np.ndarray, a pd.Series or a single-column pd.DataFrame."
        )


def ensure_valid_identifier(artifact_name: str):
    check_identifier(
        to_check=artifact_name,
        context=None,
        ignore_empty=False,
        logger=None,
        raise_value_error=True
    )


def validate_split_against_data_collection_feature_transform(
    feature_transform_type: FeatureTransformationType,
    post_data: Optional[Union[pd.DataFrame, Table, str]] = None
):
    if feature_transform_type == FEATURE_TRANSFORM_TYPE_PRE_POST_DATA and post_data is None:
        raise ValueError(
            "Cannot add a split without post data when feature transform is set to have pre-/post- transform data."
        )
    elif feature_transform_type in [
        FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION,
        FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
    ] and post_data is not None:
        raise ValueError(
            "Cannot add a split with post data when there is no feature transform or it is being done with a model transform function."
        )


def validate_model_threshold(threshold: float, score_type: str) -> float:
    if score_type == "regression":
        return None
    if score_type == "probits" or score_type == "classification":
        if threshold is None:
            return 0.5
        if threshold > 1 or threshold < 0:
            raise ValueError(
                f"Thresholds for score type {score_type} must be between 0 and 1. Provided threshold: {threshold}"
            )
        return threshold
    if score_type == "logits":
        return 0 if threshold is None else threshold
    raise ValueError(
        f"Attempted to set threshold for unrecognized score type {score_type}."
    )


def is_feature_map_identity_transform(
    pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]]
) -> bool:
    if pre_to_post_feature_map is None:
        return True
    return all(
        len(v) == 1 and k == v[0] for k, v in pre_to_post_feature_map.items()
    )


def get_feature_transform_type_from_feature_map(
    pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]],
    provide_transform_with_model: Optional[bool]
):
    if pre_to_post_feature_map:
        if provide_transform_with_model:
            return FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION
        elif provide_transform_with_model == False:
            return FEATURE_TRANSFORM_TYPE_PRE_POST_DATA
        elif is_feature_map_identity_transform(
            pre_to_post_feature_map
        ) and provide_transform_with_model is None:
            return FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
        else:
            raise ValueError(
                "Must use `provide_transform_with_model` to specify how feature mapping will be done in this data collection."
            )
    elif not provide_transform_with_model:
        return FEATURE_TRANSFORM_TYPE_NO_TRANSFORM
    else:
        raise ValueError(
            "Must specify `pre_to_post_feature_map` if transforms are provided with models!"
        )


def validate_split_with_feature_map(
    logger: logging.Logger, feature_map: Mapping[str, Sequence[str]],
    pre_data: pd.DataFrame, post_data: Optional[pd.DataFrame]
):
    pre_features_from_map = set(feature_map.keys())
    pre_features_from_data = set(pre_data.columns)
    post_features_from_map = set(
        itertools.chain.from_iterable(feature_map.values())
    )
    if pre_features_from_map != pre_features_from_data:
        missing_cols = sorted(
            list(pre_features_from_map - pre_features_from_data)
        )
        added_cols = sorted(
            list(pre_features_from_data - pre_features_from_map)
        )
        raise ValueError(
            f"`pre_data` does not match existing feature map! Missing columns: {missing_cols} \nAdditional columns: {added_cols}"
        )
    if post_features_from_map:
        if post_data is None:
            logger.warning(
                "Feature map detected, but post-transformed data is not provided with this split. Make sure that uploaded models contain a transform function to perform the feature mapping!"
            )
        else:
            post_features_from_data = set(post_data.columns)
            missing_cols = sorted(
                list(post_features_from_map - post_features_from_data)
            )
            added_cols = sorted(
                list(post_features_from_data - post_features_from_map)
            )
            if missing_cols or added_cols:
                raise ValueError(
                    f"`post_data` does not match existing feature map! Missing columns: {missing_cols} \nAdditional columns: {added_cols}"
                )


def validate_split_for_dataframe(
    logger: logging.Logger,
    *,
    pre_data: Optional[pd.DataFrame],
    post_data: Optional[pd.DataFrame] = None,
    label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
    label_col_name: Optional[str] = None,
    extra_data_df: Optional[pd.DataFrame] = None,
    pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]] = None,
    output_type: str = "classification",
    id_column_name: Optional[str] = None,
    timestamp_col_name: Optional[str] = None,
    prediction_col_name: Optional[str] = None,
    split_mode=sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED,
    model_set_in_context: bool = False
):
    # verify types and length of rows
    if pre_data is not None:
        _assert_is_dataframe(pre_data, "pre_data")
        _assert_dataframe_columns_are_strings(pre_data, "pre_data")

    if post_data is not None:
        _assert_is_dataframe(post_data, "post_data")
        _assert_dataframe_columns_are_strings(post_data, "post_data")
        _assert_df_shape_matches_pre(post_data, "post_data", pre_data)

    if split_mode != sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED:
        if label_data is not None:
            _assert_df_shape_matches_pre(label_data, "label_data", pre_data)

    if extra_data_df is not None:
        _assert_dataframe_columns_are_strings(extra_data_df, "extra_data_df")
        _assert_df_shape_matches_pre(extra_data_df, "extra_data_df", pre_data)

    _assert_labels_are_single_dim(label_data, id_column_name)

    # verify presence of special cols
    if isinstance(pre_data, pd.DataFrame):
        # devnote: we could consider applying this check to tables too.
        pre_data_columns = pre_data.columns
        if id_column_name:
            if id_column_name not in pre_data_columns:
                raise ValueError(
                    f"Provided `id_column_name` \"{id_column_name}\" not found in `pre_data`!"
                )
            if post_data is not None and id_column_name not in post_data.columns:
                raise ValueError(
                    f"Provided `id_column_name` \"{id_column_name}\" not found in `post_data`!"
                )
            if label_data is not None:
                if not isinstance(label_data, pd.DataFrame):
                    raise ValueError(
                        f"Expected ID column {id_column_name} to be present in `label_data`, but found type {type(label_data)}! Pass in a pd.DataFrame with the ID column present."
                    )
                if id_column_name not in label_data.columns:
                    raise ValueError(
                        f"Provided `id_column_name` \"{id_column_name}\" not found in `label_data`!"
                    )
        if label_col_name and label_col_name not in pre_data_columns:
            raise ValueError(
                f"Provided `label_col_name` \"{label_col_name}\" not found in `pre_data`!"
            )
        if prediction_col_name:
            if prediction_col_name not in pre_data_columns:
                raise ValueError(
                    f"Provided `prediction_column_name` \"{prediction_col_name}\" not found in `pre_data`!"
                )
            if not model_set_in_context:
                raise ValueError(
                    "Must set model in workspace context prior to uploading predictions alongside a split!"
                )
        num_pre_cols = len(pre_data_columns) - bool(prediction_col_name) - bool(
            label_col_name
        ) - bool(id_column_name)
        if num_pre_cols <= 0 and split_mode != sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED:
            raise ValueError(
                "Provided `pre_data` DataFrame does not have any non-label or non-prediction columns!"
            )
    # verify against feature map
    if pre_to_post_feature_map:
        pre_data_dropping_cols = pre_data
        post_data_dropping_cols = post_data
        if id_column_name:
            pre_data_dropping_cols = pre_data_dropping_cols.drop(
                columns=[id_column_name]
            )
            if post_data_dropping_cols is not None:
                post_data_dropping_cols = post_data_dropping_cols.drop(
                    columns=[id_column_name]
                )
        if timestamp_col_name:
            pre_data_dropping_cols = pre_data_dropping_cols.drop(
                columns=[timestamp_col_name]
            )
        validate_split_with_feature_map(
            logger, pre_to_post_feature_map, pre_data_dropping_cols,
            post_data_dropping_cols
        )

    # verify label values
    label_verification_fn = verify_label_values_for_classification if output_type == "classification" else verify_label_values_for_regression
    label_data_to_verify = label_data
    if label_col_name:
        label_data_to_verify = pre_data[label_col_name]
    elif isinstance(
        label_data, pd.DataFrame
    ) and id_column_name in label_data.columns:
        col_to_index = [c for c in label_data.columns if c != id_column_name][0]
        label_data_to_verify = label_data_to_verify[col_to_index]
    if label_data_to_verify is not None:
        label_verification_fn(label_data_to_verify)

    if isinstance(label_data, pd.DataFrame):
        _assert_dataframe_columns_are_strings(label_data, "label_data")


def validate_feature_influence_algorithm_generic(algorithm: str):
    if algorithm not in ["truera-qii", "shap", "integrated-gradients"]:
        raise ValueError(
            f"`algorithm` must be one of {['truera-qii', 'shap']}, but given \"{algorithm}\"!"
        )


def validate_feature_influence_score_type(is_regression: bool, score_type: str):
    if score_type is None:
        return  # use default score type
    if is_regression:
        if score_type not in fi_constants.ALL_REGRESSION_SCORE_TYPES:
            raise ValueError(
                f"Invalid score type \"{score_type}\" was provided. Valid influence score types for this model: {fi_constants.ALL_REGRESSION_SCORE_TYPES}"
            )
        return
    if score_type not in fi_constants.ALL_CLASSIFICATION_SCORE_TYPES:
        raise ValueError(
            f"Invalid score type \"{score_type}\" was provided. Valid influence score types for this model: {fi_constants.ALL_CLASSIFICATION_SCORE_TYPES}"
        )


def validate_performance_metrics(
    performance_metrics: Sequence[str], valid_performance_metrics: Sequence[str]
) -> Sequence[AccuracyType.Type]:
    ret = []
    for curr in performance_metrics:
        if curr not in valid_performance_metrics:
            raise ValueError(
                f"Metric {curr} not a valid performance metric! Must be one of {valid_performance_metrics}"
            )
        ret.append(AccuracyType.Type.Value(curr))
    return ret


def get_score_type_from_default(
    provided_score_type: Optional[str], default_score_type: str
) -> str:
    if not provided_score_type:
        return default_score_type

    for (project_type, valid_score_types) in [
        ("regression", fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION),
        ("classification", fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION)
    ]:
        if default_score_type in valid_score_types and provided_score_type not in valid_score_types:
            raise ValueError(
                f"Cannot ingest predictions of score type {provided_score_type} for {project_type} project!"
            )
    return provided_score_type


def validate_add_feature_influence(
    feature_influence_data: pd.DataFrame,
    aiq_split_metadata: is_pb.SplitMetaData,
    data_splits: Optional[Sequence[str]] = None,
    data_collection_name: Optional[str] = None,
    background_data_split_name: Optional[str] = None,
    id_col_name: Optional[str] = None,
    timestamp_col_name: Optional[str] = None,
    influence_type: Optional[str] = None,
    project_influence_type: Optional[str] = None
) -> bool:
    if not isinstance(feature_influence_data, pd.DataFrame):
        raise ValueError(
            f"`feature_influence_data` is type {type(feature_influence_data)}, expected pd.DataFrame!"
        )

    temp_feature_influence_data = feature_influence_data.drop(
        [id_col_name, timestamp_col_name], axis="columns", errors="ignore"
    )

    if background_data_split_name and background_data_split_name not in data_splits:
        raise ValueError(
            f"Split \"{background_data_split_name}\" does not exist in data collection {data_collection_name}"
        )
    # TODO(AB#6731): Validate influence data against data collection schema instead of pulling split data
    split_cols = set(aiq_split_metadata.ordered_column_names.values)
    fi_cols = set(temp_feature_influence_data.columns)
    if split_cols != fi_cols:
        raise ValueError(
            f"`feature_influence_data` columns do not match split data columns! Missing columns: "
            f"{split_cols - fi_cols}. Additional columns: {fi_cols - split_cols}."
        )
    if not all(
        [
            pd.api.types.is_float_dtype(dtype)
            for dtype in temp_feature_influence_data.dtypes
        ]
    ):
        raise ValueError(
            f"`feature_influence_data` columns must have float dtype!"
        )

    explanation_algorithm_type = validate_influence_type_str_for_virtual_model_upload(
        influence_type, project_influence_type
    )

    if id_col_name or timestamp_col_name:
        if explanation_algorithm_type != ExplanationAlgorithmType.TRUERA_QII:
            raise ValueError(
                f"Uploading non-QII influences is not supported for splits with ID or timestamp columns."
            )

    if id_col_name and id_col_name not in feature_influence_data.columns:
        raise ValueError(
            f"Invalid `id_col_name`: {id_col_name}. Column does not exist."
        )

    if timestamp_col_name and timestamp_col_name not in feature_influence_data.columns:
        raise ValueError(
            f"Invalid `timestamp_col_name`: {timestamp_col_name}. Column does not exist."
        )

    if id_col_name and timestamp_col_name:
        # converting to datetime so that if any error/exceptions would happen here
        try:
            pd.to_datetime(feature_influence_data[timestamp_col_name])
        except Exception as exc:
            raise ValueError(
                f"`timestamp_col_name` column must have valid datetime format. Could not convert column to datetime; "
                f"error: {exc}"
            )
        return True

    return False


def validate_add_data_split_generic(
    data_split_name: str,
    *,
    post_data: Optional[Union[pd.DataFrame, Table, str]] = None,
    label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
    feature_influence_data: Optional[pd.DataFrame] = None,
    label_col_name: Optional[str] = None,
    split_type: Optional[str] = "all",
    background_split_name: Optional[str] = None,
    input_type: Optional[str] = None,
    data_splits: Optional[Sequence[str]] = None,
    feature_transform_type: Optional[FeatureTransformationType] = None
):
    if is_nontabular_project(input_type):
        raise ValueError(
            "For `time_series_tabular` or `nlp` projects, use `add_nn_data_split` instead."
        )

    if data_split_name in data_splits:
        raise AlreadyExistsError(
            f"Data split \"{data_split_name}\" already exists!"
        )
    ensure_valid_identifier(data_split_name)
    if split_type not in VALID_SPLIT_TYPES:
        raise ValueError(
            f"Provided `split_type` \"{split_type}\" is not valid! Must be one of {VALID_SPLIT_TYPES}"
        )
    if label_col_name and label_data is not None:
        raise ValueError(
            f"`label_data` and `label_col_name` both given, but at most one is allowed!"
        )
    if feature_influence_data is not None and not background_split_name:
        raise ValueError(
            f"Must specify `background_split_name` for feature influence data"
        )
    if background_split_name:
        if background_split_name == data_split_name:
            raise ValueError(
                f"`background_split_name` cannot be same as `data_split_name`. Please ensure background split exists."
            )
        if background_split_name not in data_splits:
            raise ValueError(
                f"Background split \"{background_split_name}\" does not exist. Available splits: {data_splits}"
            )
    validate_split_against_data_collection_feature_transform(
        feature_transform_type, post_data=post_data
    )
