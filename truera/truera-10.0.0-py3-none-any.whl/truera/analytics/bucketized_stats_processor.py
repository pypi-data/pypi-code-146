from __future__ import annotations

from typing import Mapping, Optional, Sequence, Tuple, TYPE_CHECKING, Union

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from truera.aiq import intelligence_server_impl

from truera.analytics.pending_operations_or import PendingOperationsOr
from truera.authn.usercontext import RequestContext
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    BucketizedStatsType  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    CategoricalBucketParams  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    ModelInputSpec  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    NumericalBucketParams  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    QuantityOfInterest  # pylint: disable=no-name-in-module
from truera.utils.truera_status import TruEraInternalError
from truera.utils.truera_status import TruEraInvalidArgumentError


def compute_bucketized_stats(
    request_ctx, iss: intelligence_server_impl.IntelligenceServiceServicer,
    project_id: str, model_id: str, input_spec: ModelInputSpec, feature: str,
    bucketized_stats_type: int, numerical_bucket_params: NumericalBucketParams,
    categorical_bucket_params: CategoricalBucketParams,
    filter_series_or_operations: Optional[PendingOperationsOr[pd.Series]]
) -> PendingOperationsOr[Sequence[pd.DataFrame]]:
    is_regression = iss.artifact_metadata_client.is_regression_model(
        request_ctx, project_id, model_id
    )

    # Get scores and return early if pending operations exist.
    scores = None
    scores_or_operations = _possibly_retrieve_scores(
        request_ctx, iss, project_id, model_id, input_spec,
        bucketized_stats_type, is_regression
    )
    if scores_or_operations is not None:
        if scores_or_operations.is_operations:
            return PendingOperationsOr.from_pending_operations(
                [scores_or_operations, filter_series_or_operations]
            )
        scores = scores_or_operations.value
    if filter_series_or_operations is not None and filter_series_or_operations.is_operations:
        return filter_series_or_operations
    # Retrieve labels.
    labels = _retrieve_labels(
        request_ctx, iss, project_id, model_id, input_spec, is_regression
    )
    # Retrieve special values.
    special_values = iss.artifact_metadata_client.get_feature_special_values_for_model(
        request_ctx, project_id, model_id, feature
    )
    # Compute values of interest.
    vals = _compute_vals_of_interest(
        request_ctx, iss, project_id, model_id, bucketized_stats_type, scores,
        labels
    )
    # Retrieve feature values.
    feature_vals = _retrieve_feature_vals(
        request_ctx, iss, project_id, model_id, input_spec, feature
    )
    # Set up dataframe.
    data = pd.DataFrame.from_dict(
        {
            "feature_vals": feature_vals,
            "vals": vals,
            "counts": np.ones(len(vals)),
        }
    )
    data.index = feature_vals.index
    # Use filter if necessary.
    if filter_series_or_operations is not None:
        filter_series = filter_series_or_operations.value
        if data.shape[0] != len(filter_series):
            raise TruEraInternalError(
                "Internal error: score and filter lengths don't match!"
            )
        data = data[filter_series]
    # Bucketize.
    if iss.artifact_loader.GetIsCategoricalFeatureForModel(
        request_ctx, project_id, model_id, input_spec.split_id, feature
    ):
        return _bucketize_categorical_feature(categorical_bucket_params, data)
    else:
        return _bucketize_numerical_feature(
            numerical_bucket_params, data, special_values
        )


def get_bucketized_stats_qoi(
    bucketized_stats_type: int,
    is_regression: bool,
    always_return_score_type: bool = False
) -> Optional[QuantityOfInterest]:
    if bucketized_stats_type in [
        BucketizedStatsType.Type.CLASSIFICATION_ERROR,
        BucketizedStatsType.Type.LOG_LOSS
    ]:
        if is_regression:
            raise TruEraInvalidArgumentError(
                f"Type {BucketizedStatsType.Type.Name(bucketized_stats_type)} requires a classification model!"
            )
        return QuantityOfInterest.PROBITS_SCORE
    if bucketized_stats_type in [
        BucketizedStatsType.Type.L1_ERROR, BucketizedStatsType.Type.L2_ERROR
    ]:
        if not is_regression:
            raise TruEraInvalidArgumentError(
                f"Type {BucketizedStatsType.Type.Name(bucketized_stats_type)} requires a regression model!"
            )
        return QuantityOfInterest.REGRESSION_SCORE
    if always_return_score_type:
        return QuantityOfInterest.REGRESSION_SCORE if is_regression else QuantityOfInterest.PROBITS_SCORE


def _possibly_retrieve_scores(
    request_context: RequestContext,
    iss: intelligence_server_impl.IntelligenceServiceServicer, project_id: str,
    model_id: str, input_spec: ModelInputSpec, bucketized_stats_type: int,
    is_regression: bool
) -> Optional[PendingOperationsOr[Sequence[float]]]:
    qoi = get_bucketized_stats_qoi(bucketized_stats_type, is_regression)
    if qoi is None:
        return None

    return iss.artifact_loader.GetModelPredictions(
        request_context, project_id, model_id, input_spec, qoi=qoi
    )


def _retrieve_labels(
    request_context: RequestContext,
    iss: intelligence_server_impl.IntelligenceServiceServicer, project_id: str,
    model_id: str, input_spec: ModelInputSpec, is_regression: bool
) -> pd.Series:
    input_spec_no_filter = ModelInputSpec()
    input_spec_no_filter.CopyFrom(input_spec)
    input_spec_no_filter.ClearField("filter_expression")
    label_data = iss.artifact_loader.GetLabelsForModel(
        request_context, project_id, model_id, input_spec_no_filter
    )
    if label_data is None:
        raise TruEraInvalidArgumentError(
            "Labels are required to compute bucketized stats!"
        )
    label_data = label_data.value.iloc[:, 0]
    unique_labels = set(list(label_data.to_numpy().ravel()))
    if not is_regression and not all(
        [np.isnan(curr) or curr in [0, 1] for curr in unique_labels]
    ):
        raise TruEraInternalError("Labels must be either 0 or 1!")
    return label_data


def _compute_vals_of_interest(
    request_ctx, iss: intelligence_server_impl.IntelligenceServiceServicer,
    project_id: str, model_id: str, bucketized_stats_type: int,
    scores: pd.Series, labels: pd.Series
) -> pd.Series:
    if bucketized_stats_type == BucketizedStatsType.Type.GROUND_TRUTH:
        return labels
    elif bucketized_stats_type == BucketizedStatsType.Type.CLASSIFICATION_ERROR:
        classifications = iss.artifact_metadata_client.get_classification_scores_for_model(
            request_ctx, project_id, model_id, QuantityOfInterest.PROBITS_SCORE,
            scores
        )
        return np.abs(labels - classifications)
    elif bucketized_stats_type == BucketizedStatsType.Type.LOG_LOSS:
        return -(labels * np.log(scores) + (1 - labels) * np.log(1 - scores))
    elif bucketized_stats_type == BucketizedStatsType.Type.L1_ERROR:
        return np.abs(labels - scores)
    elif bucketized_stats_type == BucketizedStatsType.Type.L2_ERROR:
        return (labels - scores)**2
    else:
        raise TruEraInvalidArgumentError(
            f"Provided type {bucketized_stats_type} not a valid entry!"
        )


def _retrieve_feature_vals(
    request_context: RequestContext,
    iss: intelligence_server_impl.IntelligenceServiceServicer, project_id: str,
    model_id: str, input_spec: ModelInputSpec, feature: str
) -> pd.Series:
    input_spec_no_filter = ModelInputSpec()
    input_spec_no_filter.CopyFrom(input_spec)
    input_spec_no_filter.ClearField("filter_expression")
    preprocessed_data = iss.artifact_loader.GetPreprocessedDataForModel(
        request_context, project_id, model_id, input_spec_no_filter
    ).value
    if feature in preprocessed_data.columns:
        return preprocessed_data[feature]
    extra_data = iss.artifact_loader.GetExtraDataForModel(
        request_context, project_id, model_id, input_spec_no_filter
    ).value
    if extra_data is not None and feature in extra_data:
        return extra_data[feature]
    raise TruEraInvalidArgumentError(
        f"Feature \"{feature}\" not a valid (pre-transformed) feature!"
    )


def _bucketize_categorical_feature(
    categorical_bucket_params: CategoricalBucketParams, data: pd.DataFrame
) -> PendingOperationsOr[Sequence[pd.DataFrame]]:
    if not categorical_bucket_params:
        raise TruEraInvalidArgumentError(
            "categorical_bucket_params parameter not given for categoric feature!"
        )
    # The following handling of dtypes if a bit of a hack to make sure False/True maps with '0'/'1' and 42 with '42'.
    dtype = data["feature_vals"].dtype
    if dtype == bool:
        data["feature_vals"] = data["feature_vals"].astype(int).astype(str)
    elif pd.api.types.is_numeric_dtype(dtype):
        data["feature_vals"] = data["feature_vals"].astype(str)
    ret_vals = data["vals"].groupby(
        data["feature_vals"]
    ).mean().reindex(index=categorical_bucket_params.buckets)
    ret_cnts = data["counts"].groupby(
        data["feature_vals"]
    ).sum().reindex(index=categorical_bucket_params.buckets)
    ret = pd.DataFrame.from_dict({"vals": ret_vals, "counts": ret_cnts})
    return PendingOperationsOr.from_value([ret, None])


def _bucketize_numerical_feature(
    numerical_bucket_params: NumericalBucketParams, data: pd.DataFrame,
    special_values: Sequence[Union[float, int]]
) -> PendingOperationsOr[Sequence[pd.DataFrame]]:
    if not numerical_bucket_params:
        raise TruEraInvalidArgumentError(
            "numerical_bucket_params parameter not given for numeric feature!"
        )
    if numerical_bucket_params.num_buckets <= 0:
        raise TruEraInvalidArgumentError(
            "numerical_bucket_params.num_buckets parameter must be >= 1!"
        )
    data, ret_vals_special_values, ret_cnts_special_values = _process_special_values(
        special_values, data
    )
    lower_bound = numerical_bucket_params.lower_bound if numerical_bucket_params.lower_bound != -np.inf else data[
        "feature_vals"].min()
    upper_bound = numerical_bucket_params.upper_bound if numerical_bucket_params.upper_bound != np.inf else data[
        "feature_vals"].max()
    mask = (lower_bound <=
            data["feature_vals"]) & (data["feature_vals"] <= upper_bound)
    if np.sum(mask) == 0:
        ret_normal = pd.DataFrame.from_dict(
            {
                "vals": [],
                "counts": [],
                "lower_bound": [],
                "upper_bound": [],
            }
        )
        return PendingOperationsOr.from_value([ret_normal, None])
    bucket_endpoints = np.quantile(
        data["feature_vals"][mask],
        np.linspace(0, 1, numerical_bucket_params.num_buckets + 1)
    )
    bucket_endpoints = np.unique(bucket_endpoints)
    ret_vals = data["vals"].groupby(
        pd.cut(
            data["feature_vals"],
            bucket_endpoints,
            right=False,
            include_lowest=True
        )
    ).mean()
    ret_vals.index = ret_vals.index.astype(str)
    ret_cnts = data["counts"].groupby(
        pd.cut(
            data["feature_vals"],
            bucket_endpoints,
            right=False,
            include_lowest=True
        )
    ).sum()
    ret_cnts.index = ret_cnts.index.astype(str)
    ret_normal = pd.DataFrame.from_dict(
        {
            "vals":
                ret_vals,
            "counts":
                ret_cnts,
            "lower_bound":
                pd.Series(bucket_endpoints[:-1], index=ret_vals.index),
            "upper_bound":
                pd.Series(bucket_endpoints[1:], index=ret_vals.index),
        }
    )
    ret_special_values = None
    if ret_vals_special_values is not None:
        ret_special_values = pd.DataFrame.from_dict(
            {
                "vals": ret_vals_special_values,
                "counts": ret_cnts_special_values
            }
        )
    return PendingOperationsOr.from_value([ret_normal, ret_special_values])


def _process_special_values(
    special_values: Sequence[Union[float, int]], data: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    curr_vals = {}
    curr_cnts = {}
    for special_value in special_values:
        data, curr_vals, curr_cnts = _process_special_value_mask(
            data, data["feature_vals"] == special_value, str(special_value),
            curr_vals, curr_cnts
        )
    data, curr_vals, curr_cnts = _process_special_value_mask(
        data, data["feature_vals"].isna(), "NaN", curr_vals, curr_cnts
    )
    if curr_vals:
        ret_vals_special_values = pd.Series(curr_vals, name="vals")
        ret_vals_special_values.index.name = "feature_vals"
        ret_cnts_special_values = pd.Series(curr_cnts, name="counts")
        ret_cnts_special_values.index.name = "feature_vals"
    else:
        ret_vals_special_values = None
        ret_cnts_special_values = None
    return data, ret_vals_special_values, ret_cnts_special_values


def _process_special_value_mask(
    data: pd.DataFrame, mask: pd.Series, special_value_name: str,
    curr_vals: Mapping[str, float], curr_cnts: Mapping[str, float]
) -> Tuple[pd.DataFrame, Mapping[str, float], Mapping[str, float]]:
    if np.sum(mask) > 0:
        data_special_value = data[mask]
        curr_vals[special_value_name] = data_special_value["vals"].mean()
        curr_cnts[special_value_name] = data_special_value["counts"].sum()
        data = data[~mask]
    return data, curr_vals, curr_cnts
