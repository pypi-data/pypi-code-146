from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any, Mapping, Optional, Sequence, Tuple, TYPE_CHECKING

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from truera.analytics.pending_operations_or import PendingOperationsOr
from truera.authn.usercontext import RequestContext
# pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.accuracy_pb2 import AccuracyEstimateConfidence
from truera.protobuf.public.aiq.accuracy_pb2 import \
    AccuracyResult as acc_result_pb
from truera.protobuf.public.aiq.accuracy_pb2 import AccuracyType
from truera.protobuf.public.aiq.accuracy_pb2 import ConfusionMatrix
from truera.protobuf.public.aiq.intelligence_service_pb2 import ModelInputSpec
from truera.protobuf.public.common_pb2 import FeatureInfluenceOptions
from truera.protobuf.public.qoi_pb2 import QuantityOfInterest
# pylint: enable=no-name-in-module
from truera.utils.accuracy_utils import ACCURACY_METRIC_MAP
from truera.utils.accuracy_utils import BINARY_CLASSIFICATION_SCORE_ACCURACIES
from truera.utils.accuracy_utils import CLASSIFICATION_SCORE_ACCURACIES
from truera.utils.accuracy_utils import confusion_matrix
from truera.utils.accuracy_utils import \
    MULTICLASS_CLASSIFICATION_SCORE_ACCURACIES
from truera.utils.accuracy_utils import PROBITS_OR_LOGITS_SCORE_ACCURACIES
from truera.utils.accuracy_utils import PROBITS_SCORE_ACCURACIES
from truera.utils.accuracy_utils import REGRESSION_SCORE_ACCURACIES
from truera.utils.accuracy_utils import SEGMENT_GENERALIZED_METRICS
from truera.utils.truera_status import TruEraInternalError
from truera.utils.truera_status import TruEraInvalidArgumentError

if TYPE_CHECKING:
    import truera.aiq.intelligence_server_impl as impl


@dataclass
class AccuracyResultTuple:
    result_type: Any
    value: float = None
    message: str = None
    interpretation: acc_result_pb.AccuracyResultType = acc_result_pb.AccuracyInterpretation.UNKNOWN


@dataclass
class AccuracyResult:
    # this needs to align to the AccuracyResponse proto defined in protocol/truera/protobuf/public/aiq/intelligence_service.proto
    result_map: Mapping[int, AccuracyResultTuple]
    # precision, recall, thresholds
    precision_recall_curve: Optional[Tuple[Any, Any, Any]] = None
    # fpr, tpr, thresholds
    roc_curve: Optional[Tuple[Any, Any, Any]] = None
    # confusion matrix
    confusion_matrix: ConfusionMatrix = ConfusionMatrix()
    # confidence of estimations
    estimate_confidence: Optional[int] = None


@dataclass
class _DataForAccuracyComputation:
    pending_operations: Optional[PendingOperationsOr[AccuracyResult]]
    labels: pd.Series
    scores_map: Mapping[int, pd.Series]


def _get_aligned_labels_preds_map(
    labels: pd.Series, preds_map: Mapping[int, pd.Series]
) -> Mapping[int, Tuple[np.ndarray, np.ndarray]]:
    return {
        qoi: _get_aligned_labels_preds(labels, preds_map[qoi])
        for qoi in preds_map
    }


def _get_aligned_labels_preds(
    labels: pd.Series, preds: pd.Series
) -> Tuple[np.ndarray, np.ndarray]:
    labels.name = "__truera_labels___"
    preds.name = "__truera_predictions__"
    joined_df = pd.merge(
        labels, preds, how="inner", left_index=True, right_index=True
    )
    return joined_df[labels.name].to_numpy(), joined_df[preds.name].to_numpy()


def _compute_accuracy_metric(
    metric: int,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    all_y_true: Optional[np.ndarray] = None,
    all_y_pred: Optional[np.ndarray] = None,
    sample_weight: Optional[np.ndarray] = None,
    num_classes: Optional[int] = None
):
    if metric not in ACCURACY_METRIC_MAP:
        raise TruEraInvalidArgumentError(
            "Metric {} is unsupported.".format(AccuracyType.Type.Name(metric))
        )
    if y_true.ndim != 1 and y_true.shape[-1] != 1:
        raise TruEraInternalError(
            f"Multiclass labels are not supported! Provided label shape: {y_true.shape}"
        )
    if y_true.size != y_pred.size:
        raise TruEraInternalError("Sizes of y_true and y_pred do not match!")
    metric_fn, interpretation = ACCURACY_METRIC_MAP[metric]
    if metric not in SEGMENT_GENERALIZED_METRICS and metric in PROBITS_OR_LOGITS_SCORE_ACCURACIES and len(
        np.unique(y_true)
    ) == 1:
        return AccuracyResultTuple(
            message="Cannot compute {}, only one class present within labels.".
            format(AccuracyType.Type.Name(metric)),
            result_type=acc_result_pb.AccuracyResultType.ONLY_ONE_LABEL_CLASS,
            interpretation=interpretation
        )
    if y_true.size <= 0:
        metric_val = np.nan
    else:
        y_true = y_true.ravel()
        y_pred = y_pred.ravel()
        kwargs = {}
        if num_classes is not None:
            kwargs["binary"] = num_classes <= 2
        if metric in SEGMENT_GENERALIZED_METRICS:
            all_y_true = None if all_y_true is None else all_y_true.ravel()
            all_y_pred = None if all_y_pred is None else all_y_pred.ravel()
            metric_val = metric_fn(
                y_true,
                y_pred,
                all_y_true,
                all_y_pred,
                sample_weight=sample_weight,
                **kwargs
            )
        else:
            metric_val = metric_fn(
                y_true, y_pred, sample_weight=sample_weight, **kwargs
            )
    return AccuracyResultTuple(
        value=metric_val,
        result_type=acc_result_pb.AccuracyResultType.VALUE,
        interpretation=interpretation
    )


def _get_qoi_types(
    metric: int, default_qoi: QuantityOfInterest, is_regression=False
) -> int:
    if is_regression != (metric in REGRESSION_SCORE_ACCURACIES):
        raise TruEraInvalidArgumentError(
            f"Accuracy type {AccuracyType.Type.Name(metric)} is not supported for a {'regression' if is_regression else 'classification'} model."
        )
    if metric in PROBITS_OR_LOGITS_SCORE_ACCURACIES:
        if default_qoi == QuantityOfInterest.CLASSIFICATION_SCORE:
            return QuantityOfInterest.PROBITS_SCORE
        return default_qoi
    if metric in PROBITS_SCORE_ACCURACIES:
        return QuantityOfInterest.PROBITS_SCORE
    if metric in CLASSIFICATION_SCORE_ACCURACIES or metric in BINARY_CLASSIFICATION_SCORE_ACCURACIES or metric in MULTICLASS_CLASSIFICATION_SCORE_ACCURACIES:
        return QuantityOfInterest.CLASSIFICATION_SCORE
    if metric in REGRESSION_SCORE_ACCURACIES:
        return QuantityOfInterest.REGRESSION_SCORE
    raise TruEraInvalidArgumentError(f'Unsupported accuracy type: {metric}')


def _retrieve_required_data(
    request_context: RequestContext,
    accuracy_types: Sequence[int],
    iss: impl.IntelligenceServiceServicer,
    project_id: str,
    model_id: str,
    input_spec: ModelInputSpec,
    default_qoi: QuantityOfInterest,
    include_confusion_matrix: bool,
    cached_predictions_only: bool,
    is_regression: bool,
    curve_qoi: Optional[int],
) -> Optional[_DataForAccuracyComputation]:
    labels_input_spec = ModelInputSpec()
    labels_input_spec.CopyFrom(input_spec)
    labels_input_spec.filter_expression.CopyFrom(
        iss._retrieve_appended_requirements_filter_expression(
            labels_input_spec,
            filter_to_available_labels=iss.SILENTLY_USE_ONLY_LABELLED_DATA,
        )
    )

    labels_or_operation = iss.artifact_loader.GetLabelsForModel(
        request_context, project_id, model_id, labels_input_spec
    )

    # If ground truth labels are missing, we cant compute accuracy.
    if labels_or_operation is None:
        return None

    qoi_types = set(
        [
            _get_qoi_types(
                accuracy_type, default_qoi, is_regression=is_regression
            ) for accuracy_type in accuracy_types
        ]
    )
    if curve_qoi is not None:
        qoi_types.add(curve_qoi)
    if not is_regression and include_confusion_matrix:
        qoi_types.add(QuantityOfInterest.CLASSIFICATION_SCORE)

    scores_map = {}
    all_operations = [labels_or_operation]
    for qoi in qoi_types:
        preds_input_spec = ModelInputSpec()
        preds_input_spec.CopyFrom(input_spec)
        preds_input_spec.filter_expression.CopyFrom(
            iss._retrieve_appended_requirements_filter_expression(
                preds_input_spec,
                filter_to_non_inf_predictions=iss.
                SILENTLY_USE_NON_INF_PREDICTIONS,
                filter_to_non_null_predictions=iss.
                SILENTLY_USE_NON_NAN_PREDICTIONS,
                qoi=qoi
            )
        )
        scores_or_operations = iss.artifact_loader.GetModelPredictions(
            request_context,
            project_id,
            model_id,
            preds_input_spec,
            qoi=qoi,
            cached_predictions_only=cached_predictions_only
        )
        if scores_or_operations is None:
            return None
        all_operations.append(scores_or_operations)
        if not scores_or_operations.is_operations:
            scores = scores_or_operations.value
            if isinstance(scores, pd.DataFrame):
                scores = scores[scores.columns[0]]
            scores_map[qoi] = scores

    if PendingOperationsOr.is_any_pending(all_operations):
        return _DataForAccuracyComputation(
            PendingOperationsOr.from_pending_operations(all_operations), None,
            None
        )
    labels = labels_or_operation.value
    if isinstance(labels, pd.DataFrame):
        labels = labels[labels.columns[0]]
    return _DataForAccuracyComputation(None, labels, scores_map)


def compute_accuracies(
    request_context: RequestContext,
    accuracy_types: Sequence[int],
    iss: impl.IntelligenceServiceServicer,
    project_id: str,
    model_id: str,
    input_spec: ModelInputSpec,
    all_input_spec: ModelInputSpec,
    default_qoi: QuantityOfInterest,
    *,
    include_precision_recall_curve: bool = False,
    include_roc_curve: bool = False,
    include_confusion_matrix: bool = False,
    cached_predictions_only: bool = False,
    is_regression: bool = False
) -> Optional[PendingOperationsOr[AccuracyResult]]:
    curve_qoi = None
    if not is_regression and (
        include_precision_recall_curve or include_roc_curve
    ):
        curve_qoi = _get_qoi_types(
            AccuracyType.Type.AUC, default_qoi, is_regression=is_regression
        )
    retrieve_required_data = lambda input_spec: _retrieve_required_data(
        request_context=request_context,
        accuracy_types=accuracy_types,
        iss=iss,
        project_id=project_id,
        model_id=model_id,
        input_spec=input_spec,
        default_qoi=default_qoi,
        include_confusion_matrix=include_confusion_matrix,
        cached_predictions_only=cached_predictions_only,
        is_regression=is_regression,
        curve_qoi=curve_qoi
    )
    use_all_data = input_spec.all_available_inputs and (
        input_spec.filter_expression is None or
        not input_spec.HasField("filter_expression")
    )
    use_segment_generalized_metric = any(
        [curr in SEGMENT_GENERALIZED_METRICS for curr in accuracy_types]
    )
    different = not use_all_data and use_segment_generalized_metric
    res_all = retrieve_required_data(
        all_input_spec if different else input_spec
    )
    if res_all is None:
        return None
    if res_all.pending_operations is not None:
        return res_all.pending_operations
    res = retrieve_required_data(input_spec) if different else res_all
    all_labels = res_all.labels
    all_scores_map = res_all.scores_map
    labels = res.labels
    scores_map = res.scores_map
    aligned_labels_preds_map = _get_aligned_labels_preds_map(labels, scores_map)

    accuracy_map = {}
    for accuracy_type in accuracy_types:
        qoi = _get_qoi_types(
            accuracy_type, default_qoi, is_regression=is_regression
        )
        all_labels_np, all_preds_np = _get_aligned_labels_preds(
            all_labels, all_scores_map[qoi]
        )
        accuracy_map[accuracy_type] = _compute_accuracy_metric(
            accuracy_type,
            aligned_labels_preds_map[qoi][0],
            aligned_labels_preds_map[qoi][1],
            all_labels_np,
            all_preds_np,
            num_classes=None
            if is_regression else 2  # TODO(MLNN-357): Support multi-class.
        )
    result = AccuracyResult(accuracy_map)
    if labels.size > 0 and not is_regression:
        if include_precision_recall_curve:
            result.precision_recall_curve = metrics.precision_recall_curve(
                *aligned_labels_preds_map[curve_qoi]
            )
        if include_roc_curve:
            result.roc_curve = metrics.roc_curve(
                *aligned_labels_preds_map[curve_qoi]
            )
        if include_confusion_matrix:
            [tn, fp, fn, tp], _ = confusion_matrix(
                *aligned_labels_preds_map[
                    QuantityOfInterest.CLASSIFICATION_SCORE]
            )
            result.confusion_matrix.true_positive_count = tp
            result.confusion_matrix.false_positive_count = fp
            result.confusion_matrix.true_negative_count = tn
            result.confusion_matrix.false_negative_count = fn

    return PendingOperationsOr.from_value(result)


def _get_importance_weights(
    intime_train_influences,
    intime_test_influences,
    oot_influences,
    test_ratio=0.05
):
    # Train discriminator to separate intime and oot
    x = pd.concat([oot_influences, intime_train_influences])
    y = np.concatenate(
        [np.zeros(len(oot_influences)),
         np.ones(len(intime_train_influences))]
    )
    train_x, test_x, train_y, test_y = train_test_split(
        x, y, test_size=test_ratio, random_state=42
    )
    discriminator = LogisticRegression(random_state=42)
    discriminator.fit(train_x, train_y)
    disc_probs = discriminator.predict_proba(test_x)[:, 1]
    disc_auc = metrics.roc_auc_score(test_y, disc_probs)
    disc_brier = metrics.brier_score_loss(test_y, disc_probs)
    disc_info = {
        'discriminator': discriminator,
        'disc_auc': disc_auc,
        'disc_brier': disc_brier
    }

    # Generate importance sampling weights
    probs = np.clip(
        discriminator.predict_proba(intime_test_influences)[:, 1], 0.01, None
    )
    is_scores = ((1 / probs) - 1) * sum(train_y) / (len(train_y) - sum(train_y))
    is_5_percentile = np.percentile(is_scores, 5)

    # Discern confidence level
    confidence_levels = [
        AccuracyEstimateConfidence.Confidence.HIGH,
        AccuracyEstimateConfidence.Confidence.MEDIUM,
        AccuracyEstimateConfidence.Confidence.LOW
    ]
    DISC_THRESH = [0.8, 0.9, 1]  # thresholds on discriminator AUC
    MIN_IS_5_THRESH = [0.1, 0.005, 0]  # thresholds on 5th %ile of weights
    confidence_index = max(
        np.digitize(disc_auc, DISC_THRESH),
        np.digitize(is_5_percentile, MIN_IS_5_THRESH)
    )
    confidence_level = confidence_levels[confidence_index]
    return is_scores, disc_info, confidence_level


def estimate_accuracies(
    request_context: RequestContext,
    accuracy_types: Sequence[int],
    iss: impl.IntelligenceServiceServicer,
    project_id: str,
    model_id: str,
    input_spec: ModelInputSpec,
    baseline_split_id: str,
    *,
    include_precision_recall_curve: bool = False,
    include_roc_curve: bool = False,
    cached_predictions_only: bool = False,
    min_baseline_influences: Optional[int] = None,
    min_estimate_influences: Optional[int] = None,
    is_regression: bool = False
) -> Optional[PendingOperationsOr[AccuracyResult]]:
    """
    Estimates projected model metrics if data is available and labels are not. 
    Uses a baseline split (with data/labels available) to create estimations. 
    For full methodology: https://www.overleaf.com/project/5f7b85d25f2af300013c23af
    """
    if min_baseline_influences is None or min_baseline_influences <= 0:
        min_baseline_influences = 1000
    if min_estimate_influences is None or min_estimate_influences <= 0:
        min_estimate_influences = min_baseline_influences // 2

    if is_regression:
        # estimations don't support regression models at the moment
        accuracy_map = {
            accuracy_type: AccuracyResultTuple(
                message="Regression models unsupported for estimated metrics",
                result_type=acc_result_pb.AccuracyResultType.
                UNSUPPORTED_MODEL_TYPE
            ) for accuracy_type in accuracy_types
        }
        return PendingOperationsOr.from_value(AccuracyResult(accuracy_map))

    baseline_too_restrictive = False
    if baseline_split_id is None:
        baseline_too_restrictive = True
    else:
        baseline_mis = ModelInputSpec(
            split_id=baseline_split_id, all_available_inputs=True
        )
        baseline_labels_df = iss.artifact_loader.GetLabelsForModel(
            request_context, project_id, model_id, baseline_mis
        )
        if baseline_labels_df is None or len(
            baseline_labels_df.value
        ) < min_baseline_influences or baseline_labels_df.value.iloc[:, 0].isna(
        ).any():
            baseline_too_restrictive = True

    if baseline_too_restrictive:
        accuracy_map = {
            accuracy_type: AccuracyResultTuple(
                message=
                "Baseline split doesn't exist, lacks labels, or is too small.",
                result_type=acc_result_pb.AccuracyResultType.
                MISSING_OR_SMALL_BASELINE
            ) for accuracy_type in accuracy_types
        }
        return PendingOperationsOr.from_value(AccuracyResult(accuracy_map))

    # Only compute preds/probs if necessary based on score types
    qois = [
        _get_qoi_types(
            accuracy_type,
            QuantityOfInterest.PROBITS_SCORE,
            is_regression=is_regression
        ) for accuracy_type in accuracy_types
    ]
    calc_classifion_scores = (QuantityOfInterest.CLASSIFICATION_SCORE in qois)
    baseline_probs = None
    baseline_preds = None

    # Need access to baseline preds, influences for baseline/estimate
    baseline_mis = ModelInputSpec(split_id=baseline_split_id)
    baseline_mis.dataset_index_range.stop = min_baseline_influences  # pylint: disable=protobuf-type-error
    quantity_of_interest = iss.GetQuantityOfInterest(
        request_context, None, project_id=project_id
    )
    baseline_influences_or_ops = iss.artifact_loader.GetModelInfluences(
        request_context, project_id, model_id, baseline_mis,
        FeatureInfluenceOptions(quantity_of_interest=quantity_of_interest)
    )
    est_influences_or_ops = iss.artifact_loader.GetModelInfluences(
        request_context, project_id, model_id, input_spec,
        FeatureInfluenceOptions(quantity_of_interest=quantity_of_interest)
    )

    baseline_probs_or_ops = iss.artifact_loader.GetModelPredictions(
        request_context,
        project_id,
        model_id,
        baseline_mis,
        qoi=QuantityOfInterest.PROBITS_SCORE,
        cached_predictions_only=cached_predictions_only
    )
    all_ops = [
        baseline_probs_or_ops, baseline_influences_or_ops, est_influences_or_ops
    ]

    # Calculate classification predictions if necessary
    if calc_classifion_scores:
        baseline_preds_or_ops = iss.artifact_loader.GetModelPredictions(
            request_context,
            project_id,
            model_id,
            baseline_mis,
            qoi=QuantityOfInterest.CLASSIFICATION_SCORE,
            cached_predictions_only=cached_predictions_only
        )
        all_ops.append(baseline_probs_or_ops)

    if any(x is None for x in all_ops):
        return None
    elif PendingOperationsOr.is_any_pending(all_ops):
        return PendingOperationsOr.from_pending_operations(all_ops)

    # Check that filter doesn't restrict size of estimation set
    if len(est_influences_or_ops.value) < min_estimate_influences:
        filter_msg = "Segment has {} datapoints, but {} are required for accuracy estimations.".format(
            len(est_influences_or_ops.value), min_estimate_influences
        )
        accuracy_map = {
            accuracy_type: AccuracyResultTuple(
                message=filter_msg,
                result_type=acc_result_pb.AccuracyResultType.
                SEGMENT_TOO_RESTRICTIVE
            ) for accuracy_type in accuracy_types
        }
        return PendingOperationsOr.from_value(AccuracyResult(accuracy_map))

    # Grab influences and generate importance sampling weights
    baseline_influences = baseline_influences_or_ops.value
    est_influences = est_influences_or_ops.value
    baseline_train_influences, baseline_test_influences, baseline_train_indices, baseline_test_indices = train_test_split(
        baseline_influences,
        np.arange(len(baseline_influences)),
        random_state=42,
        test_size=0.5
    )
    is_scores, disc_info, confidence_level = _get_importance_weights(
        baseline_train_influences, baseline_test_influences, est_influences
    )
    # Estimate metrics with importance sampling weights
    labels = baseline_labels_df.value.values[baseline_test_indices]
    baseline_probs = baseline_probs_or_ops.value.to_numpy(
    )[baseline_test_indices]
    if calc_classifion_scores:
        baseline_preds = baseline_preds_or_ops.value.to_numpy(
        )[baseline_test_indices]

    accuracy_map = {}
    for qoi, accuracy_type in zip(qois, accuracy_types):
        scores = baseline_probs if qoi != QuantityOfInterest.CLASSIFICATION_SCORE else baseline_preds
        accuracy_map[accuracy_type] = _compute_accuracy_metric(
            accuracy_type,
            labels,
            scores,
            labels,
            scores,
            sample_weight=is_scores,
            num_classes=None
            if is_regression else 2  # TODO(MLNN-357): Support multi-class.
        )

    result = AccuracyResult(accuracy_map)
    result.estimate_confidence = confidence_level
    if include_precision_recall_curve:
        result.precision_recall_curve = metrics.precision_recall_curve(
            labels, baseline_probs, sample_weight=is_scores
        )
    if include_roc_curve:
        result.roc_curve = metrics.roc_curve(
            labels, baseline_probs, sample_weight=is_scores
        )
    return PendingOperationsOr.from_value(result)
