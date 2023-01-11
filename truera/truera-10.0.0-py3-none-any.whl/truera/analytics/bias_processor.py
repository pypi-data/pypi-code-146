from enum import Enum
from enum import unique
import logging
from typing import Optional

import numpy as np
import pandas as pd
from sklearn import metrics

from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    BiasResult  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    BiasType  # pylint: disable=no-name-in-module
from truera.utils.truera_status import TruEraInternalError
from truera.utils.truera_status import TruEraInvalidArgumentError


def get_bias_dataset(
    preds_or_scores, labels, is_regression=False, positive_class_favored=True
):
    if is_regression:
        return RegressionBiasDataset(preds_or_scores, labels)
    else:
        return BinaryClassificationBiasDataset(
            preds_or_scores,
            labels,
            positive_class_favored=positive_class_favored
        )


class RegressionBiasDataset(object):

    def __init__(self, scores: pd.Series, labels: Optional[pd.Series]):
        if labels is not None and len(scores) != len(labels):
            raise TruEraInternalError(
                "Cannot calculate bias metrics from labels and scores of differing lengths."
            )
        self._scores = np.array(scores)  # y_hat
        self._labels = np.array(labels) if labels is not None else None  # y

    @property
    def scores(self):
        if self._scores is None:
            raise TruEraInternalError(
                "Scores were not provided to bias processor."
            )
        return self._scores

    @property
    def labels(self):
        if self._labels is None:
            raise TruEraInvalidArgumentError(
                "Labels were not provided to bias processor."
            )
        return self._labels

    def l1_error(self):
        return metrics.mean_absolute_error(self.labels, self.scores)

    def l2_error(self):
        return metrics.mean_squared_error(self.labels, self.scores)

    def mean_score(self):
        return np.mean(self.scores)

    def get_bias_result_from_metric(self, metric_fn_str):
        # Returns tuple of (bias_value, bias_result_type)
        if len(self.scores) == 0:
            return np.nan, BiasResult.BiasResultType.VALUE
        metric_fn = getattr(self, metric_fn_str, None)
        if metric_fn is None:
            return None, None
        return metric_fn(), BiasResult.BiasResultType.VALUE


class BinaryClassificationBiasDataset(object):

    def __init__(
        self,
        preds: pd.Series,
        labels: Optional[pd.Series],
        positive_class_favored=True
    ):
        self._preds = np.array(preds)
        self.positive_class_favored = positive_class_favored

        if labels is None:
            self._labels = None
        else:
            if len(preds) != len(labels):
                raise TruEraInternalError(
                    "Cannot calculate bias metrics from labels and predictions of differing lengths."
                )
            self._labels = np.array(labels)
            if set(np.unique(self._labels[~np.isnan(self._labels)])
                  ) > set([0, 1]):
                raise TruEraInvalidArgumentError(
                    "Bias metrics for non-binary classifications are unsupported."
                )

        # define variables for confusion matrix to avoid redundant computation
        self.num_true_positives = None
        self.num_true_negatives = None
        self.num_false_positives = None
        self.num_false_negatives = None

    @property
    def preds(self):
        if self._preds is None:
            raise TruEraInternalError(
                "Scores were not provided to bias processor."
            )
        return self._preds

    @property
    def labels(self):
        if self._labels is None:
            raise TruEraInvalidArgumentError(
                "Labels were not provided to bias processor."
            )
        return self._labels

    def _set_confusion_matrix(self):
        self.num_true_negatives, self.num_false_positives, self.num_false_negatives, self.num_true_positives = metrics.confusion_matrix(
            self.labels, self.preds
        ).ravel()

    def true_positives(self):
        if self.num_true_positives is None:
            self._set_confusion_matrix()
        return self.num_true_positives

    def true_negatives(self):
        if self.num_true_negatives is None:
            self._set_confusion_matrix()
        return self.num_true_negatives

    def false_positives(self):
        if self.num_false_positives is None:
            self._set_confusion_matrix()
        return self.num_false_positives

    def false_negatives(self):
        if self.num_false_negatives is None:
            self._set_confusion_matrix()
        return self.num_false_negatives

    def true_positive_rate(self):
        true_positives = self.true_positives()
        false_negatives = self.false_negatives()
        return true_positives / (true_positives + false_negatives)

    def false_positive_rate(self):
        false_positives = self.false_positives()
        true_negatives = self.true_negatives()
        return false_positives / (false_positives + true_negatives)

    def true_negative_rate(self):
        return 1 - self.false_positive_rate()

    def false_negative_rate(self):
        return 1 - self.true_positive_rate()

    def positive_acceptance_rate(self):
        true_positives = self.true_positives()
        false_positives = self.false_positives()
        return true_positives / (true_positives + false_positives)

    def negative_acceptance_rate(self):
        true_negatives = self.true_negatives()
        false_negatives = self.false_negatives()
        return true_negatives / (true_negatives + false_negatives)

    def positive_conditional_acceptance_rate(self):
        all_positives = self.labels.sum()
        all_pred_positives = self.preds.sum()
        return all_positives / all_pred_positives

    def negative_conditional_acceptance_rate(self):
        all_negatives = (1 - self.labels).sum()
        all_pred_negatives = (1 - self.preds).sum()
        return all_negatives / all_pred_negatives

    def selection_rate_positive(self):
        return np.sum(self.preds) / len(self.preds)

    def selection_rate(self):
        selection_rate_positive = self.selection_rate_positive()
        return selection_rate_positive if self.positive_class_favored else 1 - selection_rate_positive

    def treatment_equality_rate(self):
        false_positives = self.false_positives()
        false_negatives = self.false_negatives()
        return false_positives / false_negatives

    def equality_of_opportunity(self):
        return self.true_positive_rate(
        ) if self.positive_class_favored else self.true_negative_rate()

    def average_odds(self):
        false_positive_rate = self.false_positive_rate()
        true_positive_rate = self.true_positive_rate()
        return (false_positive_rate + true_positive_rate) / 2

    def acceptance_rate(self):
        return self.positive_acceptance_rate(
        ) if self.positive_class_favored else self.negative_acceptance_rate()

    def rejection_rate(self):
        return self.negative_acceptance_rate(
        ) if self.positive_class_favored else self.positive_acceptance_rate()

    def conditional_acceptance_rate(self):
        return self.positive_conditional_acceptance_rate(
        ) if self.positive_class_favored else self.negative_conditional_acceptance_rate(
        )

    def conditional_rejection_rate(self):
        return self.negative_conditional_acceptance_rate(
        ) if self.positive_class_favored else self.positive_conditional_acceptance_rate(
        )

    def get_bias_result_from_metric(self, metric_fn_str):
        # Returns tuple of (bias_value, bias_result_type)
        if len(self.preds) == 0:
            return np.nan, BiasResult.BiasResultType.VALUE
        metric_fn = getattr(self, metric_fn_str, None)
        if metric_fn is None:
            return None, None
        val = metric_fn()
        val_type = BiasResult.BiasResultType.VALUE if np.isfinite(
            val
        ) else BiasResult.BiasResultType.ONLY_ONE_LABEL_CLASS
        return val, val_type


@unique
class BiasAggregationType(Enum):
    DIFFERENCE = 'difference'
    RATIO = 'ratio'


class BiasProcessor(object):
    NO_LABEL_REQUIREMENT_METRICS = set(
        [
            BiasType.Type.DISPARATE_IMPACT_RATIO,
            BiasType.Type.STATISTICAL_PARITY_DIFFERENCE,
            BiasType.Type.MEAN_SCORE_DIFFERENCE
        ]
    )

    def __init__(
        self,
        segment1_dataset: pd.DataFrame,
        segment2_dataset: pd.DataFrame,
        positive_class_favored=True,
        is_regression=False
    ):
        self.logger = logging.getLogger(__name__)
        self.is_regression = is_regression
        self.positive_class_favored = positive_class_favored
        self.segment1_dataset = segment1_dataset
        self.segment2_dataset = segment2_dataset

        # maps BiasType.Type -> tuple of (metric function str, BiasAggregationType, higher_metric_is_favored)
        # note that higher_metric_is_favored is calculated with the assumption that the positive class 1 is a FAVORED outcome
        # (this is flipped later if the assumption does not hold)
        self.bias_type_to_metric_str = {
            BiasType.Type.DISPARATE_IMPACT_RATIO:
                ('selection_rate', BiasAggregationType.RATIO, True),
            BiasType.Type.STATISTICAL_PARITY_DIFFERENCE:
                ('selection_rate', BiasAggregationType.DIFFERENCE, True),
            BiasType.Type.TRUE_POSITIVE_RATIO:
                ('true_positive_rate', BiasAggregationType.RATIO, True),
            BiasType.Type.TRUE_POSITIVE_DIFFERENCE:
                ('true_positive_rate', BiasAggregationType.DIFFERENCE, True),
            BiasType.Type.FALSE_POSITIVE_RATIO:
                ('false_positive_rate', BiasAggregationType.RATIO, True),
            BiasType.Type.FALSE_POSITIVE_DIFFERENCE:
                ('false_positive_rate', BiasAggregationType.DIFFERENCE, True),
            BiasType.Type.TRUE_NEGATIVE_RATIO:
                ('true_negative_rate', BiasAggregationType.RATIO, False),
            BiasType.Type.TRUE_NEGATIVE_DIFFERENCE:
                ('true_negative_rate', BiasAggregationType.DIFFERENCE, False),
            BiasType.Type.FALSE_NEGATIVE_RATIO:
                ('false_negative_rate', BiasAggregationType.RATIO, False),
            BiasType.Type.FALSE_NEGATIVE_DIFFERENCE:
                ('false_negative_rate', BiasAggregationType.DIFFERENCE, False),
            BiasType.Type.TREATMENT_EQUALITY_DIFFERENCE:
                (
                    'treatment_equality_rate', BiasAggregationType.DIFFERENCE,
                    True
                ),
            BiasType.Type.EQUALITY_OF_OPPORTUNITY_DIFFERENCE:
                (
                    'equality_of_opportunity', BiasAggregationType.DIFFERENCE,
                    True
                ),
            BiasType.Type.EQUALITY_OF_OPPORTUNITY_RATIO:
                ('equality_of_opportunity', BiasAggregationType.RATIO, True),
            BiasType.Type.AVERAGE_ODDS_DIFFERENCE:
                ('average_odds', BiasAggregationType.DIFFERENCE, True),
            BiasType.Type.ACCEPTANCE_RATE_DIFFERENCE:
                ('acceptance_rate', BiasAggregationType.DIFFERENCE, False),
            BiasType.Type.REJECTION_RATE_DIFFERENCE:
                ('rejection_rate', BiasAggregationType.DIFFERENCE, True),
            BiasType.Type.CONDITIONAL_ACCEPTANCE_DIFFERENCE:
                (
                    'conditional_acceptance_rate',
                    BiasAggregationType.DIFFERENCE, False
                ),
            BiasType.Type.CONDITIONAL_REJECTION_DIFFERENCE:
                (
                    'conditional_rejection_rate',
                    BiasAggregationType.DIFFERENCE, True
                ),
            BiasType.Type.L1_ERROR_DIFFERENCE:
                ('l1_error', BiasAggregationType.DIFFERENCE, False),
            BiasType.Type.L2_ERROR_DIFFERENCE:
                ('l2_error', BiasAggregationType.DIFFERENCE, False),
            BiasType.Type.MEAN_SCORE_DIFFERENCE:
                ('mean_score', BiasAggregationType.DIFFERENCE, True),
        }

    def difference(self, value1, value2):
        return value1 - value2

    def ratio(self, value1, value2):
        return value1 / value2

    def get_bias_result(
        self, bias_type, metric_fn_str, aggregation_type,
        higher_metric_is_favored
    ):
        # get aggregation function
        if aggregation_type == BiasAggregationType.DIFFERENCE:
            aggregation_fn = self.difference
        elif aggregation_type == BiasAggregationType.RATIO:
            aggregation_fn = self.ratio
        else:
            raise TruEraInvalidArgumentError(
                'Unsupported bias aggregation type: {}'.
                format(aggregation_type)
            )

        # calculate bias metric per segment
        bias_result = BiasResult()
        bias_result.bias_type = bias_type
        segment1_metric, bias_result_type = self.segment1_dataset.get_bias_result_from_metric(
            metric_fn_str
        )
        if bias_result_type is None:
            raise TruEraInvalidArgumentError(
                'Unsupported bias type {} for {} model.'.format(
                    BiasType.Type.Name(bias_type),
                    'regression' if self.is_regression else 'classification'
                )
            )
        if bias_result_type != BiasResult.BiasResultType.VALUE:
            bias_result.result_type = bias_result_type
            return bias_result
        segment2_metric, bias_result_type = self.segment2_dataset.get_bias_result_from_metric(
            metric_fn_str
        )
        if bias_result_type is None:
            raise TruEraInvalidArgumentError(
                'Unsupported bias type {} for {} model.'.format(
                    BiasType.Type.Name(bias_type),
                    'regression' if self.is_regression else 'classification'
                )
            )
        aggregate_metric = aggregation_fn(segment1_metric, segment2_metric)
        bias_result.segment1_metric = segment1_metric
        bias_result.segment2_metric = segment2_metric
        bias_result.aggregate_metric = aggregate_metric
        bias_result.result_type = bias_result_type
        # determine favored segment
        if not self.positive_class_favored:
            # indicates that NEGATIVE/class 0 is favored, forcing us to flip how we interpret the metric
            if metric_fn_str not in [
                'equality_of_opportunity', 'acceptance_rate', 'rejection_rate',
                'conditional_acceptance_rate', 'conditional_rejection_rate',
                'selection_rate', 'l1_error', 'l2_error'
            ]:
                # some metrics already account for the flipped interpretation
                higher_metric_is_favored = not higher_metric_is_favored
        bias_result.segment1_favored = (
            segment1_metric > segment2_metric
        ) if higher_metric_is_favored else (segment1_metric < segment2_metric)
        return bias_result

    def get_metric_from_bias_type(self, bias_type: int):
        metric_fn_str, aggregation_type, higher_metric_is_favored = self.bias_type_to_metric_str.get(
            bias_type, (None, None, True)
        )
        if metric_fn_str is None:
            raise TruEraInvalidArgumentError(
                'Unsupported bias metric type: {}.'.format(
                    BiasType.Type.Name(bias_type)
                )
            )
        return self.get_bias_result(
            bias_type,
            metric_fn_str,
            aggregation_type,
            higher_metric_is_favored,
        )
