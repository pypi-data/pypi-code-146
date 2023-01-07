from typing import Optional, Union

from rhino_health.lib.metrics.base_metric import BaseMetric
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class AccuracyScore(BaseMetric):
    """
    Calculates the `Accuracy Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score>`_

    Examples
    --------
    >>> accuracy_score_configuration = AccuracyScore(
    ...   y_true = 'first_binary_column',
    ...   y_pred = 'second_binary_column',
    ...   normalize = False,
    ...   sample_weight = [ 0.1, 0.2, 1, 0, ..... ],
    ... )
    >>> my_cohort.get_metric(accuracy_score_configuration)
    """

    y_true: FilterVariableTypeOrColumnName
    y_pred: FilterVariableTypeOrColumnName
    normalize: Optional[bool] = True
    sample_weight: Optional[list] = None

    def metric_name(self):
        return "accuracy_score"


class AveragePrecisionScore(BaseMetric):
    """
    Calculates the `Average Precision Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html#sklearn.metrics.average_precision_score>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_score: FilterVariableTypeOrColumnName
    average: Optional[str] = "macro"
    pos_label: Optional[Union[int, str]] = 1
    sample_weight: Optional[list] = None

    def metric_name(self):
        return "average_precision_score"


class BalancedAccuracyScore(BaseMetric):
    """
    Calculates the `Balanced Accuracy Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html#sklearn.metrics.balanced_accuracy_score>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_pred: FilterVariableTypeOrColumnName
    sample_weight: Optional[list] = None
    adjusted: Optional[bool] = False

    def metric_name(self):
        return "balanced_accuracy_score"


class BrierScoreLoss(BaseMetric):
    """
    Calculates the `Brier Score Loss <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html#sklearn.metrics.brier_score_loss>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_prob: FilterVariableTypeOrColumnName
    sample_weight: Optional[list] = None
    pos_label: Optional[Union[int, str]] = None

    def metric_name(self):
        return "brier_score_loss"


class CohenKappaScore(BaseMetric):
    """
    Calculates the `Cohen Kappa Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html#sklearn.metrics.cohen_kappa_score>`_
    """

    y1: FilterVariableTypeOrColumnName
    y2: FilterVariableTypeOrColumnName
    labels: Optional[list] = None
    weights: Optional[str] = None
    sample_weight: Optional[list] = None

    def metric_name(self):
        return "cohen_kappa_score"


class ConfusionMatrix(BaseMetric):
    """
    Calculates the `Confusion Matrix <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html#sklearn.metrics.confusion_matrix>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_pred: FilterVariableTypeOrColumnName
    labels: Optional[list] = None
    sample_weight: Optional[list] = None
    normalize: Optional[bool] = True

    def metric_name(self):
        return "confusion_matrix"


class DCGScore(BaseMetric):
    """
    Calculates the `DCG Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.dcg_score.html#sklearn.metrics.dcg_score>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_score: FilterVariableTypeOrColumnName
    k: Optional[int] = None
    log_base: Optional[int] = 2
    sample_weight: Optional[list] = None
    ignore_ties: Optional[bool] = False

    def metric_name(self):
        return "dcg_score"


class WeightedScore(BaseMetric):
    """@autoapi False"""

    y_true: FilterVariableTypeOrColumnName
    """@autoapi True """
    y_pred: FilterVariableTypeOrColumnName
    """@autoapi True"""
    average: Optional[str] = "binary"
    """@autoapi True"""
    labels: Optional[list] = None
    """@autoapi True"""
    pos_label: Optional[Union[int, str]] = 1
    """@autoapi True"""
    sample_weight: Optional[list] = None
    """@autoapi True"""


class F1Score(WeightedScore):
    """
    Calculates the `F1 Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score>`_
    """

    def metric_name(self):
        return "f1_score"


class FBetaScore(WeightedScore):
    """
    Calculates the `F Beta Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.fbeta_score.html#sklearn.metrics.fbeta_score>`_
    """

    def metric_name(self):
        return "fbeta_score"


class HammingLossMetric(BaseMetric):
    """
    Calculates the `Hamming Loss Metric <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.hamming_loss.html#sklearn.metrics.hamming_loss>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_pred: FilterVariableTypeOrColumnName
    sample_weight: Optional[list] = None

    def metric_name(self):
        return "hamming_loss"


class HingeLossMetric(BaseMetric):
    """
    Calculates the `Hinge Loss Metric <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.hinge_loss.html#sklearn.metrics.hinge_loss>`_
    """

    y_true: FilterVariableTypeOrColumnName
    pred_decision: FilterVariableTypeOrColumnName
    labels: Optional[list] = None
    sample_weight: Optional[list] = None

    def metric_name(self):
        return "hinge_loss"


class JaccardScore(WeightedScore):
    """
    Calculates the `Jaccard Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html#sklearn.metrics.jaccard_score>`_
    """

    def metric_name(self):
        return "jaccard_score"


class LogLoss(BaseMetric):
    """
    Calculates the `Log Loss <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html#sklearn.metrics.log_loss>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_pred: FilterVariableTypeOrColumnName
    eps: Optional[float] = None
    normalize: Optional[bool] = True
    sample_weight: Optional[list] = None
    labels: Optional[list] = None

    def metric_name(self):
        return "log_loss"


class MatthewsCorrelationCoefficient(BaseMetric):
    """
    Calculates the `Matthews Correlation Coefficient <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.matthews_corrcoef.html#sklearn.metrics.matthews_corrcoef>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_pred: FilterVariableTypeOrColumnName
    sample_weight: Optional[list] = None

    def metric_name(self):
        return "matthews_corrcoef"


class NDCGScore(BaseMetric):
    """
    Calculates the `NDCG Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html#sklearn.metrics.ndcg_score>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_score: FilterVariableTypeOrColumnName
    k: Optional[int] = None
    sample_weight: Optional[list] = None
    ignore_ties: Optional[bool] = False

    def metric_name(self):
        return "ndcg_score"


class PrecisionScore(WeightedScore):
    """
    Calculates the `Precision Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html#sklearn.metrics.precision_score>`_
    """

    def metric_name(self):
        return "precision_score"


class RecallScore(WeightedScore):
    """
    Calculates the `Recall Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score>`_
    """

    def metric_name(self):
        return "recall_score"


class TopKAccuracyScore(BaseMetric):
    """
    Calculates the `Top K Accuracy Score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.top_k_accuracy_score.html#sklearn.metrics.top_k_accuracy_score>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_score: FilterVariableTypeOrColumnName
    k: Optional[int] = 2
    normalize: Optional[bool] = True
    sample_weight: Optional[list] = None
    labels: Optional[list] = None

    def metric_name(self):
        return "top_k_accuracy_score"


class ZeroOneLoss(BaseMetric):
    """
    Calculates the `Zero One Loss <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.zero_one_loss.html#sklearn.metrics.zero_one_loss>`_
    """

    y_true: FilterVariableTypeOrColumnName
    y_score: FilterVariableTypeOrColumnName
    normalize: Optional[bool] = True
    sample_weight: Optional[list] = None

    def metric_name(self):
        return "zero_one_loss"
