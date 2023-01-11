import numpy as np


def get_accuracy_group_name_dict(num_classes: int):
    """return the name of accuracy groups keyed by (target, pred) tuple"""
    accuracy_group_name_dict = {}
    if num_classes == 2:
        accuracy_group_name_dict[(0, 0)] = 'True Negative'
        accuracy_group_name_dict[(1, 0)] = 'False Negative'
        accuracy_group_name_dict[(0, 1)] = 'False Positive'
        accuracy_group_name_dict[(1, 1)] = 'True Positive'
    else:
        for c1 in range(num_classes):
            for c2 in range(num_classes):
                accuracy_group_name_dict[(c1, c2)] = '{}_as_{}'.format(c1, c2)
    return accuracy_group_name_dict


def get_filter_from_group_name(pred, label, group):
    """
    get indices of various accuracy-based groups based on group name
    """
    if '_as_' not in group:
        if group == 'False Negative':
            return (pred == 0) & (label == 1)
        elif group == 'False Positive':
            return (pred == 1) & (label == 0)
        elif group == 'True Negative':
            return (pred == 0) & (label == 0)
        elif group == 'True Positive':
            return (pred == 1) & (label == 1)
        elif group == 'All':
            return np.ones(len(pred), dtype=bool)
    else:
        target_class = int(group.split('_as_')[0])
        pred_class = int(group.split('_as_')[1])
        return (pred == pred_class) & (label == target_class)