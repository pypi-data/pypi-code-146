from itertools import chain
from typing import List

from funcy import compact

from rhino_health.lib.metrics.base_metric import MetricResponse, MetricResultDataType

AGGREGATION_METHOD = "aggregation_method"
"""@autoapi False"""
COUNT_VARIABLE_MODE = "count_variable"
"""@autoapi False"""
COUNT_VARIABLE_METRIC_NAME = "metric_name"
"""@autoapi False"""
COUNT_VARIABLE_SINGLE_VARIABLE = "single_variable"
"""@autoapi False"""


def sum_aggregation(
    metric: str, metric_results: List[MetricResultDataType], **kwargs
) -> MetricResultDataType:
    return {metric: sum([metric_result.get(metric, 0) for metric_result in metric_results])}


def weighted_average(
    metric: str, metric_results: List[MetricResultDataType], count_variable="variable", **kwargs
) -> MetricResultDataType:
    total_count = sum(
        [metric_result.get(f"{count_variable}_count", 0) for metric_result in metric_results]
    )
    return {
        metric: (
            sum(
                [
                    metric_result.get(f"{count_variable}_count", 0) * metric_result.get(metric, 0)
                    for metric_result in metric_results
                ]
            )
            / total_count
        )
    }


def standard_deviation(
    metric: str, metric_results: List[MetricResultDataType], **kwargs
) -> MetricResultDataType:
    raise NotImplementedError  # TODO


# TODO: Add support/config for >1 variable/metric return and non default var names
SUPPORTED_AGGREGATE_METRICS = {
    "mean": {
        AGGREGATION_METHOD: weighted_average,
        COUNT_VARIABLE_MODE: COUNT_VARIABLE_SINGLE_VARIABLE,
    },
    "count": {
        AGGREGATION_METHOD: sum_aggregation,
        COUNT_VARIABLE_MODE: COUNT_VARIABLE_SINGLE_VARIABLE,
    },
    "sum": {
        AGGREGATION_METHOD: sum_aggregation,
        COUNT_VARIABLE_MODE: COUNT_VARIABLE_SINGLE_VARIABLE,
    },
    "std": {
        AGGREGATION_METHOD: standard_deviation,
        COUNT_VARIABLE_MODE: COUNT_VARIABLE_SINGLE_VARIABLE,
    },
    "accuracy_score": {AGGREGATION_METHOD: weighted_average},
    "average_precision_score": {AGGREGATION_METHOD: weighted_average},
    "balanced_accuracy_score": {AGGREGATION_METHOD: weighted_average},
    "brier_score_loss": {AGGREGATION_METHOD: weighted_average},
    "cohen_kappa_score": {AGGREGATION_METHOD: weighted_average},
    "confusion_matrix": {AGGREGATION_METHOD: weighted_average},
    "dcg_score": {AGGREGATION_METHOD: weighted_average},
    "f1_score": {AGGREGATION_METHOD: weighted_average},
    "fbeta_score": {AGGREGATION_METHOD: weighted_average},
    "hamming_loss": {AGGREGATION_METHOD: weighted_average},
    "hinge_loss": {AGGREGATION_METHOD: weighted_average},
    "jaccard_score": {AGGREGATION_METHOD: weighted_average},
    "log_loss": {AGGREGATION_METHOD: weighted_average},
    "matthews_corrcoef": {AGGREGATION_METHOD: weighted_average},
    "ndcg_score": {AGGREGATION_METHOD: weighted_average},
    "precision_score": {AGGREGATION_METHOD: weighted_average},
    "recall_score": {AGGREGATION_METHOD: weighted_average},
    "top_k_accuracy_score": {AGGREGATION_METHOD: weighted_average},
    "zero_one_loss": {AGGREGATION_METHOD: weighted_average},
}
"""
A dictionary of metrics we currently support aggregating to configuration information.
See the keys for the latest list of metrics.
"""


def calculate_aggregate_metric(
    metric_configuration, metric_results: List[MetricResultDataType]
) -> MetricResultDataType:
    metric = metric_configuration.metric_name()
    if metric not in SUPPORTED_AGGREGATE_METRICS:
        raise ValueError("Unsupported metric for aggregation")
    aggregation_configuration = SUPPORTED_AGGREGATE_METRICS[metric]
    aggregation_method = aggregation_configuration.get(AGGREGATION_METHOD, weighted_average)
    count_variable_mode = aggregation_configuration.get(
        COUNT_VARIABLE_MODE, COUNT_VARIABLE_METRIC_NAME
    )
    count_variable = metric if count_variable_mode == COUNT_VARIABLE_METRIC_NAME else "variable"
    if metric_configuration.group_by is None:
        return aggregation_method(metric, metric_results, count_variable=count_variable)
    else:
        # We get the unique group names from the data to iterate over since not all sites have all groups
        groups = set(chain.from_iterable(metric_result.keys() for metric_result in metric_results))
        grouped_results = {}
        for group in groups:
            group_result = compact(
                [metric_result.get(group, None) for metric_result in metric_results]
            )
            grouped_results[group] = aggregation_method(
                metric, group_result, count_variable=count_variable
            )
        return grouped_results
