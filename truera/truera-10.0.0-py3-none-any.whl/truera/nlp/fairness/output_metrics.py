from enum import Enum
from typing import Any, Dict, Optional, Sequence, Union

import numpy as np
import pandas as pd
from sklearn import metrics

from truera.analytics.bias_processor import BiasProcessor
from truera.analytics.bias_processor import BinaryClassificationBiasDataset
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    BiasResult  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    BiasType  # pylint: disable=no-name-in-module


def get_confusion_matrix(
    ground_truth: Union[Sequence[int], np.ndarray],
    predicted: Union[Sequence[int], np.ndarray],
    num_classes: int,
) -> Dict[str, np.ndarray]:
    '''
    Return confusion rate for given ground_truth and predicted data.
    Args:
        ground_truth: (list or np.array) list of ground truth labels, shape = [N,]
        predicted: (list or np.array) list of model predictions, shape = [N,]
        num_classes: (int) number of classes
    Return:
        confusion_matrix: (np.array) confusion matrix for the given data
    '''

    ground_truth = np.array(ground_truth).astype(np.int32)
    predicted = np.array(predicted).astype(np.int32)

    # add each class to ground_truth and predicted
    # equivalent to adding identity matrix to confusion matrix
    # guarantees [N,N] shape (N=num_classes), for confusion matrix
    all_classes = np.arange(num_classes).astype(np.int32)
    ground_truth = np.append(ground_truth, all_classes)
    predicted = np.append(predicted, all_classes)

    confusion_matrix = np.array(
        metrics.confusion_matrix(ground_truth, predicted)
    )

    # subtract identity matrix from confusion matrix
    # guarantee accurate metrics and consistent [N,N] shape
    confusion_matrix -= np.identity(num_classes, dtype="int64")
    return {"confusion_matrix": confusion_matrix}


def get_confusion_matrix_metrics(
    ground_truth: Union[list, np.ndarray],
    predicted: Union[list, np.ndarray],
    num_classes: int,
) -> Dict[str, Any]:
    '''
    Return confusion rate metrics for given ground_truth and predicted data.
    Args:
        ground_truth: (list or np.array) list of ground truth labels, shape = [N,]
        predicted: (list or np.array) list of model predictions, shape = [N,]
        num_classes: (int) number of classes
    Return:
        metrics: (dict) map containing confusion matrix metrics for the given data
    '''
    confusion_matrix = get_confusion_matrix(
        ground_truth, predicted, num_classes
    )['confusion_matrix']
    dim = len(confusion_matrix)

    true_positives = np.diag(confusion_matrix)
    false_positives = confusion_matrix.sum(axis=0) - true_positives
    false_negatives = confusion_matrix.sum(axis=1) - true_positives
    true_negatives = len(ground_truth) - (
        true_positives + false_positives + false_negatives
    )

    true_positives.astype(float)
    false_positives.astype(float)
    true_negatives.astype(float)
    false_negatives.astype(float)

    true_positive_rate = true_positives / (true_positives + false_negatives)
    false_positive_rate = false_positives / (false_positives + true_negatives)
    true_negative_rate = true_negatives / (true_negatives + false_positives)
    false_negative_rate = false_negatives / (false_negatives + true_positives)
    positive_predictive_value = true_positives / (
        true_positives + false_positives
    )
    negative_predictive_value = true_negatives / (
        true_negatives + false_negatives
    )

    if dim == 2:
        true_positive_rate = true_positive_rate[1]
        false_positive_rate = false_positive_rate[1]
        true_negative_rate = true_negative_rate[1]
        false_negative_rate = false_negative_rate[1]
        positive_predictive_value = positive_predictive_value[1]
        negative_predictive_value = negative_predictive_value[1]

    return {
        "true_positives": true_positives,
        "true_negatives": true_negatives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "true_positive_rate": true_positive_rate,
        "false_positive_rate": false_positive_rate,
        "true_negative_rate": true_negative_rate,
        "false_negative_rate": false_negative_rate,
        "positive_predictive_value": positive_predictive_value,
        "negative_predictive_value": negative_predictive_value,
    }


def get_accuracy(
    ground_truth: Union[list, np.ndarray], predicted: Union[list, np.ndarray],
    num_classes: int
) -> Dict[str, Any]:
    '''
    Return accuracy  metrics for given ground_truth and predicted data.
    Args:
        ground_truth: (list or np.array) list of ground truth labels, shape = [N,]
        predicted: (list or np.array) list of model predictions, shape = [N,]
        num_classes: (int) number of classes
    Return:
        metrics: (dict) map containing accuracy metrics for the given data
    '''
    assert (len(ground_truth) == len(predicted))
    total_correct = 0
    for i in range(len(ground_truth)):
        if ground_truth[i] == predicted[i]:
            total_correct += 1
    return {"accuracy": total_correct / len(ground_truth)}


def get_f1_score(
    ground_truth: Union[list, np.ndarray], predicted: Union[list, np.ndarray],
    num_classes: int
) -> Dict[str, Any]:
    '''
    Return f1-score metrics for given ground_truth and predicted data.
    Args:
        ground_truth: (list or np.array) list of ground truth labels, shape = [N,]
        predicted: (list or np.array) list of model predictions, shape = [N,]
        num_classes: (int) number of classes
    Return:
        metrics: (dict) map containing f1-score metrics for the given data
    '''
    confusion_matrix_rate_metrics = get_confusion_matrix_metrics(
        ground_truth, predicted, num_classes
    )
    precision = confusion_matrix_rate_metrics["positive_predictive_value"]
    recall = confusion_matrix_rate_metrics["true_positive_rate"]
    f1_score = (precision * recall) / (precision + recall)
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
    }


def disparity_wrapper(
    metric,
    segment_metrics: Dict[str, Any],
    segment_1_id: str,
    segment_2_id: str,
    get_total: Optional[bool] = False
) -> Dict[str, Any]:
    '''
    Run a given metric on given segments and calculcate disparity between the segments on said metric.
    Args:
        metric: (OutputMetrics Enum) an enum for what type of metric to run
        segment_id_1: (str) a segment_id of the one of the segments to compare 
        segment_id_2: (str) a segment_id of the one of the other segments to compare 
        segment_metrics: (dict) map from segment_id to metrics data for that segment_id
        get_total: (bool) whether or not to report the given metric for all the data (not just given segments)
    Return:
        metrics: (dict) map containing the given metric for each segment as well as the disparity between segments
    '''
    metric_name, metric_function = metric.value

    metrics = {}

    segment_1_metric = segment_metrics[segment_1_id][metric_name]
    segment_2_metric = segment_metrics[segment_2_id][metric_name]

    for key in segment_1_metric:
        metrics[f"segment_1_{key}"] = segment_1_metric[key]
        metrics[f"segment_2_{key}"] = segment_2_metric[key]
        metrics[f"{key}_disparity"] = abs(
            segment_1_metric[key] - segment_2_metric[key]
        )

        if get_total:
            total_metric = segment_metrics["total"][metric_name]
            metrics[f"total_{key}"] = total_metric[key]

    # calculcate equality of opportunity and disparate impact when calculating confusion matrix rates only if labels are binary
    if metric_name == "confusion_matrix_metrics" and len(
        segment_1_metric["true_positives"]
    ) == 2:
        metrics["equality_of_odds_positive"] = (
            1 - abs(
                segment_1_metric["true_positive_rate"] -
                segment_2_metric["true_positive_rate"]
            )
        ) / (
            1 - abs(
                segment_1_metric["false_positive_rate"] -
                segment_2_metric["false_positive_rate"]
            )
        )
        metrics["equality_of_odds_negative"] = (
            1 - abs(
                segment_1_metric["true_negative_rate"] -
                segment_2_metric["true_negative_rate"]
            )
        ) / (
            1 - abs(
                segment_1_metric["false_negative_rate"] -
                segment_2_metric["false_negative_rate"]
            )
        )
        metrics["segment_1_prob_positive"] = (
            segment_1_metric["true_positives"][1] +
            segment_1_metric["false_positives"][1]
        ) / (
            segment_1_metric["true_positives"][1] +
            segment_1_metric["false_positives"][1] +
            segment_1_metric["true_negatives"][1] +
            segment_1_metric["false_negatives"][1]
        )

        metrics["segment_2_prob_positive"] = (
            segment_2_metric["true_positives"][1] +
            segment_2_metric["false_positives"][1]
        ) / (
            segment_2_metric["true_positives"][1] +
            segment_2_metric["false_positives"][1] +
            segment_2_metric["true_negatives"][1] +
            segment_2_metric["false_negatives"][1]
        )

        metrics["disparate_impact_ratio"] = metrics[
            "segment_2_prob_positive"] / metrics["segment_1_prob_positive"]

    return metrics


def get_disp_impact(
    segment1_ds: BinaryClassificationBiasDataset,
    segment2_ds: BinaryClassificationBiasDataset,
    positive_class_favored: Optional[bool] = True
) -> BiasResult:
    processor = BiasProcessor(
        segment1_ds,
        segment2_ds,
        positive_class_favored=positive_class_favored,
        is_regression=False
    )

    disp_impact_result = processor.get_metric_from_bias_type(
        BiasType.Type.DISPARATE_IMPACT_RATIO
    )

    return disp_impact_result


class OutputMetrics(Enum):
    CONFUSION_MATRIX = ("confusion_matrix", get_confusion_matrix)
    CONFUSION_MATRIX_METRICS = (
        "confusion_matrix_metrics", get_confusion_matrix_metrics
    )
    ACCURACY = ("accuracy", get_accuracy)
    F1_SCORE = ("f1_score", get_f1_score)
