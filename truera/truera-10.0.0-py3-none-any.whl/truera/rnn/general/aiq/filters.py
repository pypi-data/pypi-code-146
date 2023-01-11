from typing import Optional, Sequence

import numpy as np

from truera.rnn.general.container import ArtifactsContainer
from truera.rnn.general.frontend.component import ComponentData
from truera.rnn.general.selection.filter_selection import FilterData
from truera.rnn.general.selection.filter_selection import FilterType
from truera.rnn.general.selection.swap_selection import SwapComparisons

from . import influences as Influences
'''
This class holds filter functions needed for filtering influences
'''


def get_swap_filter_criteria(
    aiq,
    artifacts_container: ArtifactsContainer,
    artifacts_container_compare: ArtifactsContainer,
    swap_filter_criteria: SwapComparisons,
    num_records,
    qoi_core_class,
    qoi_compare_class,
    qoi,
    pred_thresh,
    pred_thresh_compare,
    offset=0,
    qoi_timestep=0
):
    '''
    Filter based on SwapComparisons type
    '''
    input_influences, sample_filter, lengths, labels, preds = Influences.get_influences_from_qoi(
        aiq,
        qoi_core_class,
        qoi_compare_class,
        qoi,
        artifacts_container,
        num_records,
        pred_thresh,
        offset=offset,
        qoi_timestep=qoi_timestep
    )
    filter_preds = aiq.get_predictions(
        artifacts_container, num_records, offset=offset
    )

    filter_labels = aiq.get_ground_truth(
        artifacts_container, num_records, offset=offset
    )

    input_influences_compare, sample_filter_compare, lengths_compare, labels_compare, preds_compare = Influences.get_influences_from_qoi(
        aiq,
        qoi_core_class,
        qoi_compare_class,
        qoi,
        artifacts_container_compare,
        num_records,
        pred_thresh_compare,
        offset=offset,
        qoi_timestep=qoi_timestep
    )

    filter_preds_compare = aiq.get_predictions(
        artifacts_container_compare, num_records, offset=offset
    )

    filter_labels_compare = aiq.get_ground_truth(
        artifacts_container_compare, num_records, offset=offset
    )
    if qoi == 'average':
        filter_type_pred = FilterType.AVERAGE_PRED_THRESH
        filter_type_label = FilterType.AVERAGE_LABEL_THRESH
    elif qoi == 'last':
        filter_type_pred = FilterType.LAST_STEP_PRED_THRESH
        filter_type_label = FilterType.LAST_STEP_LABEL
    else:
        filter_type_pred = FilterType.LAST_STEP_PRED_THRESH
        filter_type_label = FilterType.LAST_STEP_LABEL

    swap_filter_type = SwapComparisons(swap_filter_criteria)
    if swap_filter_type == SwapComparisons.TN_TO_FP:
        predicate_pred = 1
        predicate_label = 1
        predicate_pred_compare = 0
        predicate_label_compare = 1
    elif swap_filter_type == SwapComparisons.FP_TO_TN:
        predicate_pred = 0
        predicate_label = 1
        predicate_pred_compare = 1
        predicate_label_compare = 1
    elif swap_filter_type == SwapComparisons.TN_TO_FP:
        predicate_pred = 0
        predicate_label = 0
        predicate_pred_compare = 1
        predicate_label_compare = 0
    else:
        predicate_pred = 1
        predicate_label = 0
        predicate_pred_compare = 0
        predicate_label_compare = 0

    filter_criteria_pred = get_filter_criteria(
        aiq, qoi_core_class, filter_preds, filter_labels, input_influences,
        lengths, FilterData(filter_type_pred, predicate_pred,
                            pred_thresh), artifacts_container, batch, batchsize
    )
    filter_criteria_label = get_filter_criteria(
        aiq,
        qoi_core_class,
        filter_preds,
        filter_labels,
        input_influences,
        lengths,
        FilterData(filter_type_label, predicate_label, pred_thresh),
        artifacts_container,
        num_records,
        offset=offset
    )

    filter_criteria_pred_compare = get_filter_criteria(
        aiq,
        qoi_core_class,
        qoi_compare_class,
        filter_preds_compare,
        filter_labels_compare,
        input_influences_compare,
        lengths_compare,
        FilterData(
            filter_type_pred, predicate_pred_compare, pred_thresh_compare
        ),
        artifacts_container_compare,
        num_records,
        offset=offset
    )

    filter_criteria_label_compare = get_filter_criteria(
        aiq,
        qoi_core_class,
        qoi_compare_class,
        filter_preds_compare,
        filter_labels_compare,
        input_influences_compare,
        lengths_compare,
        FilterData(
            filter_type_label, predicate_label_compare, pred_thresh_compare
        ),
        artifacts_container_compare,
        num_records,
        offset=offset
    )

    filter_criteria = np.logical_and(
        np.logical_and(filter_criteria_pred, filter_criteria_label),
        np.logical_and(
            filter_criteria_pred_compare, filter_criteria_label_compare
        )
    )
    return filter_criteria


def get_multi_filter_criteria(
    aiq,
    qoi_core_class,
    preds,
    labels,
    influences,
    seq_lengths,
    artifacts_container: ArtifactsContainer,
    num_records,
    filter_list: Optional[Sequence[ComponentData]] = None,
    offset=0
):
    filter_criteria = np.ones(len(seq_lengths), dtype=bool)
    if filter_list is None:
        filter_list = []
    for filter_component in filter_list:
        filter_criteria = np.logical_and(
            filter_criteria,
            get_filter_criteria(
                aiq,
                qoi_core_class,
                preds,
                labels,
                influences,
                seq_lengths,
                FilterData.from_component(filter_component),
                artifacts_container,
                num_records,
                offset=offset
            )
        )
    return filter_criteria


def get_filter_criteria(
    aiq,
    qoi_core_class,
    preds,
    labels,
    influences,
    seq_lengths,
    filter,
    artifacts_container: ArtifactsContainer,
    num_records,
    offset=0
):
    '''
    Filter based on prediction and/or ground truth (label) values
    '''
    if filter.lhs is None or filter.rhs is None:
        return np.ones(len(preds), dtype=bool)
    # grab filter data
    if filter.on_prediction():
        filter_data = preds[..., qoi_core_class]
    elif filter.on_label():
        filter_data = labels[..., qoi_core_class]
    elif filter.on_feature_value():
        feature = filter.lhs
        all_features = aiq.get_feature_names(artifacts_container)
        filter_data = aiq.get_data(
            artifacts_container, num_records, offset=offset
        )[..., all_features.index(str(feature).lower())]
    elif filter.on_feature_influence():
        if influences is None:
            raise ValueError("Influences needed for filter computations.")
        feature = filter.lhs
        all_features = aiq.get_feature_names(artifacts_container)
        filter_data = influences[..., all_features.index(str(feature).lower())]
    else:
        raise NotImplementedError(
            "Filter {} is not supported.".format(filter.name)
        )

    # aggregate filter data
    if filter.aggregate_average():
        filter_vals = np.array(
            [
                np.mean(filter_data[i, :seq_lengths[i]], axis=0)
                for i in range(len(seq_lengths))
            ]
        )
    elif filter.aggregate_last_step():
        filter_vals = filter_data[np.arange(len(seq_lengths)), seq_lengths - 1]
    else:
        raise NotImplementedError(
            "Aggregation type not supported for filter {}.".format(filter.name)
        )

    # perform filter operation
    if filter.is_numeric():
        filter_criteria = filter_vals >= filter.rhs if (
            filter.predicate == 0
        ) else filter_vals < filter.rhs
    else:
        filter_criteria = filter_vals == filter.rhs if (
            filter.predicate == 0
        ) else filter_vals != filter.rhs
    return filter_criteria
