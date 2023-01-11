import numpy as np

from truera.public import feature_influence_constants as fi_constants


def log_loss(ys_true: np.ndarray, ys_pred: np.ndarray):
    return -(ys_true * np.log(ys_pred) + (1 - ys_true) * np.log(1 - ys_pred))


def mean_absolute_error(ys_true: np.ndarray, ys_pred: np.ndarray):
    return np.abs(ys_true - ys_pred)


SCORE_TYPE_TO_ERROR_FN = {
    fi_constants.PREDICTOR_SCORE_TYPE_LOG_LOSS: log_loss,
    fi_constants.PREDICTOR_SCORE_TYPE_MAE_CLASSIFICATION: mean_absolute_error,
    fi_constants.PREDICTOR_SCORE_TYPE_MAE_REGRESSION: mean_absolute_error
}