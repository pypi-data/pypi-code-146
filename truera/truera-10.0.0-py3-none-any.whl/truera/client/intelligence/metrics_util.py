import numpy as np
from scipy import stats
from sklearn import metrics

from truera.utils.accuracy_utils import false_negative_rate
from truera.utils.accuracy_utils import false_positive_rate
from truera.utils.accuracy_utils import gini_score
from truera.utils.accuracy_utils import mean_squared_log_error
from truera.utils.accuracy_utils import negative_predictive_value
from truera.utils.accuracy_utils import rmse_score
from truera.utils.accuracy_utils import segment_generalized_roc_auc_score
from truera.utils.accuracy_utils import true_negative_rate
from truera.utils.accuracy_utils import true_positive_rate

LOCAL_CLASSIFICATION_METRICS = {
    # TODO: generalize these metrics to segment level.
    'AUC': metrics.roc_auc_score,
    'SEGMENT_GENERALIZED_AUC': segment_generalized_roc_auc_score,
    'GINI': gini_score,
    'LOG_LOSS': metrics.log_loss,
    'CLASSIFICATION_ACCURACY': metrics.accuracy_score,
    'PRECISION': metrics.precision_score,
    'RECALL': metrics.recall_score,
    'F1': metrics.f1_score,
    'TRUE_POSITIVE_RATE': true_positive_rate,
    'FALSE_POSITIVE_RATE': false_positive_rate,
    'TRUE_NEGATIVE_RATE': true_negative_rate,
    'FALSE_NEGATIVE_RATE': false_negative_rate,
    'NEGATIVE_PREDICTIVE_VALUE': negative_predictive_value,
    'MATTHEWS_CORRCOEF': metrics.matthews_corrcoef,
    'JACCARD_INDEX': metrics.jaccard_score,
}

THRESHOLD_INDEPENDENT_CLASSIFICATION_METRICS = [
    'AUC', 'GINI', 'LOG_LOSS', 'SEGMENT_GENERALIZED_AUC'
]

LOCAL_REGRESSION_METRICS = {
    'RMSE': rmse_score,
    'MSE': metrics.mean_squared_error,
    'MAE': metrics.mean_absolute_error,
    'MSLE': mean_squared_log_error,
    'R_SQUARED': metrics.r2_score,
    'EXPLAINED_VARIANCE': metrics.explained_variance_score,
}


class DistributionProcessor(object):

    def __init__(
        self, base_distribution: np.ndarray, compare_distribution: np.ndarray
    ):
        self.base_distribution = base_distribution
        self.compare_distribution = compare_distribution

    def difference_of_means(self):
        return self.compare_distribution.mean() - self.base_distribution.mean()

    def wasserstein_distance(self):
        return stats.wasserstein_distance(
            self.base_distribution, self.compare_distribution
        )
