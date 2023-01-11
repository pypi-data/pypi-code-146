import numpy as np

AVAILABLE_METRICS = [
    'Recall', 'Precision', 'True Positive Rate', 'Negative Prediction Value',
    'Data Volume'
]


def get_available_metric_names(include_data_volume=False):
    return AVAILABLE_METRICS[:
                            ] if include_data_volume else AVAILABLE_METRICS[:-1]


def get_threshold_from_pct(pct, pred):
    return np.percentile(pred, 100 - pct)


def cross_entropy(pred, label):
    return -np.sum(label * nd.log(pred + 1e-6)) / len(pred)


def get_precision(pred, label, class_threshold):
    denom = (pred > class_threshold).sum()
    return ((pred > class_threshold) & (label == 1)).sum() / (denom + 1e-6)


def get_tnr(pred, label, class_threshold):
    denom = (label == 0).sum()
    return ((pred < class_threshold) & (label == 0)).sum() / (denom + 1e-6)


def get_npv(pred, label, class_threshold):
    denom = (pred < class_threshold).sum()
    return ((pred < class_threshold) & (label == 0)).sum() / (denom + 1e-6)


def get_recall(pred, label, class_threshold):
    denom = (label == 1).sum()
    return ((pred > class_threshold) & (label == 1)).sum() / (denom + 1e-6)


def get_data_count(pred):
    return len(pred)


def get_stats(pred, label, class_threshold, include_data_volume=False):
    stats = [
        get_recall(pred, label, class_threshold),
        get_precision(pred, label, class_threshold),
        get_tnr(pred, label, class_threshold),
        get_npv(pred, label, class_threshold),
    ]
    if include_data_volume:
        stats.append(get_data_count(pred))
    return stats


def get_class_breakdowns(pred, label, class_threshold, above_thresh=True):
    if (above_thresh):
        thresholded = pred > class_threshold
    else:
        thresholded = pred <= class_threshold
    return thresholded.sum() / len(thresholded)
