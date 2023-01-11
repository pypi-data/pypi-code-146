from typing import Optional, Sequence

import numpy as np

from truera.rnn.general.aiq import filters as Filters
from truera.rnn.general.aiq.aiq import AIQ
from truera.rnn.general.container import ArtifactsContainer
from truera.rnn.general.frontend.component import ComponentData
from truera.rnn.general.selection.filter_selection import FilterData
from truera.rnn.general.selection.interaction_selection import \
    InfluenceAggregationMethod
from truera.rnn.general.selection.swap_selection import SwapComparisons
from truera.rnn.general.utils.errors import FilterError
from truera.rnn.general.utils.time import TemporalData
'''
Class to hold most influence manipulation methods like generating QoIs
'''


def get_compare_influences_from_qoi(
    aiq: AIQ,
    qoi_core_class: int,
    qoi_compare_class: int,
    qoi: str,
    artifacts_container: ArtifactsContainer,
    num_records: int,
    offset: int = 0,
    pred_thresh: float = 0.5,
    from_layer: str = 'input',
    qoi_timestep: int = 0,
    neuron: Optional[int] = None,
    artifacts_container_compare: Optional[ArtifactsContainer] = None,
    pred_thresh_compare: float = 0.5,
    feature_index: Optional[int] = None
) -> Sequence[np.ndarray]:
    """
    Get influences when comparing between different class outputs
    Args:
        aiq (AIQ): an AIQ class that helps get influence information.
        qoi_core_class (int): The main class to get influences from.
        qoi_compare_class (int): A comparitive class to subtract from the main qoi_core_class. This gets a difference of classes explanation.
        qoi (str): The type of qoi. Options are ['last', 'average','timestep','first default (prediction), 'first default (ground truth)']. These reference the timestep outputs.
        artifacts_container (ArtifactsContainer): An ArtifactsContainer object that helps locate metadata.
        num_records (int): The number of records to return.
        offset (int): The offset to start the num_records.
        pred_thresh (float): A threshold to use for filters. Defaults to 0.5
        from_layer (str): The layer of attributions to get. Options are ['input','internal']
        qoi_timestep (int): If the qoi is 'timestep', this helps specify the timestep output
        neuron (int or None): If from_layer is 'internal', this specifies the specific neuron index.
        artifacts_container_compare (ArtifactsContainer or None): An ArtifactsContainer object that helps locate metadata of a compare artifact. 
        pred_thresh_compare(float or None): A threshold to use for filters on a compare artifact. Defaults to 0.5
        feature_index (int or None): The feature influences to return. If none, then all features will be returned.

    Returns:
        influences (np.ndarray): An array of influences of the original influences minus the compare influences.
        sample_filter (np.ndarray): The records that pass the filter for the original data and the compare data.
        input_lengths (np.ndarray): The input lengths of the records.
        grouping_labels (np.ndarray): The labels exceeding the threshold. Used for grouping purposes in other functions.
        grouping_preds (np.ndarray): The predictions exceeding the threshold. Used for grouping purposes in other functions.
    """
    influences, sample_filter, lengths, grouping_labels, grouping_preds = get_influences_from_qoi(
        aiq,
        qoi_core_class,
        qoi_compare_class,
        qoi,
        artifacts_container,
        num_records,
        offset=0,
        pred_thresh=pred_thresh,
        from_layer=from_layer,
        qoi_timestep=qoi_timestep,
        neuron=neuron,
        feature_index=feature_index
    )

    if (artifacts_container_compare is None):
        return influences, sample_filter, lengths, grouping_labels, grouping_preds
    else:
        influences_compare, sample_filter_compare, _, _, _ = get_influences_from_qoi(
            aiq,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            artifacts_container_compare,
            num_records,
            offset=offset,
            pred_thresh=pred_thresh_compare,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            neuron=neuron,
            feature_index=feature_index
        )
        return influences - influences_compare, np.logical_and(
            sample_filter, sample_filter_compare
        ), lengths, grouping_labels, grouping_preds


def get_influences_from_qoi(
    aiq: AIQ,
    qoi_core_class: int,
    qoi_compare_class: int,
    qoi: str,
    artifacts_container: ArtifactsContainer,
    num_records: int,
    offset: int = 0,
    pred_thresh: float = 0.5,
    from_layer: str = 'input',
    qoi_timestep: int = 0,
    neuron: Optional[int] = None,
    feature_index: Optional[int] = None
) -> Sequence[np.ndarray]:
    """
    Construct simple QoIs that gradients are not necessary. ex: sums or multiplication/division by constant. This supports average QoI or timestep QoI
    Args:
        aiq (AIQ): an AIQ class that helps get influence information.
        qoi_core_class (int): The main class to get influences from.
        qoi_compare_class (int): A comparitive class to subtract from the main qoi_core_class. This gets a difference of classes explanation.
        qoi (str): The type of qoi. Options are ['last', 'average','timestep','first default (prediction), 'first default (ground truth)']. These reference the timestep outputs.
        artifacts_container (ArtifactsContainer): An ArtifactsContainer object that helps locate metadata.
        num_records (int): The number of records to return.
        offset (int): The offset to start the num_records.
        pred_thresh (float): A threshold to use for filters. Defaults to 0.5
        from_layer (str): The layer of attributions to get. Options are ['input','internal']
        qoi_timestep (int): If the qoi is 'timestep', this helps specify the timestep output
        neuron (int or None): If from_layer is 'internal', this specifies the specific neuron index.
        feature_index (int or None): The feature influences to return. If none, then all features will be returned.

    Returns:
        influences (np.ndarray): An array of influences.
        sample_filter (np.ndarray): The records that pass the filter for 'first default' qois, as not all records will have this event.
        input_lengths (np.ndarray): The input lengths of the records.
        grouping_labels (np.ndarray): The labels exceeding the threshold. Used for grouping purposes in other functions.
        grouping_preds (np.ndarray): The predictions exceeding the threshold. Used for grouping purposes in other functions.
    """
    sample_filter = None
    if neuron is None:
        layer = 'input' if from_layer == 'input' else 'outer'
        all_influences = aiq.get_influences_per_timestep(
            layer,
            artifacts_container,
            num_records,
            offset=offset,
            feature_index=feature_index
        )
        influences = all_influences[..., qoi_core_class]
        if (
            isinstance(qoi_compare_class, int) and qoi_compare_class >= 0 and
            qoi_compare_class != qoi_core_class
        ):
            influences = influences - all_influences[..., qoi_compare_class]
    else:
        if (neuron > 0):
            influences = aiq.get_influences_per_timestep(
                'inner',
                artifacts_container,
                num_records,
                offset=offset,
                class_index=neuron,
                feature_index=feature_index
            )
        else:
            influences = np.moveaxis(
                aiq.get_influences_per_timestep(
                    'inner',
                    artifacts_container,
                    num_records,
                    offset=offset,
                    feature_index=feature_index
                ), -1, -2
            )

    input_lengths = aiq.get_lengths(
        artifacts_container, num_records, offset=offset
    )
    output_lengths = input_lengths.copy()

    # If input timesteps and output timesteps sizes do not match, for now we will assume non variable lengths
    if influences.shape[1] != influences.shape[-1]:
        output_lengths = [influences.shape[-1]] * len(output_lengths)

    preds = aiq.get_predictions(
        artifacts_container,
        num_records,
        offset=offset,
        class_index=qoi_core_class
    )
    labels = aiq.get_ground_truth(
        artifacts_container, num_records, class_index=qoi_core_class
    )
    for i in range(len(output_lengths)):
        preds[i, ..., output_lengths[i]:] = 0
        labels[i, ..., output_lengths[i]:] = 0
        influences[i, ..., output_lengths[i]:] = 0
    if qoi == 'average':
        preds = np.array(
            [np.sum(p, axis=-1) / l for p, l in zip(preds, output_lengths)]
        )
        labels = np.array(
            [np.sum(p, axis=-1) / l for p, l in zip(labels, output_lengths)]
        )
        influences = np.array(
            [
                np.sum(p, axis=-1) / l
                for p, l in zip(influences, output_lengths)
            ]
        )

    elif qoi == 'last':
        preds = np.array([p[l - 1] for p, l in zip(preds, output_lengths)])
        labels = np.array([g[l - 1] for g, l in zip(labels, output_lengths)])
        influences = np.array(
            [p[..., l - 1] for p, l in zip(influences, output_lengths)]
        )
    elif qoi == 'timestep':
        preds = preds[:, qoi_timestep]
        labels = labels[:, qoi_timestep]
        influences = influences[..., qoi_timestep]
    # 'first default (ground_truth)', 'first default (prediction)'
    elif 'first default' in qoi:
        if 'prediction' in qoi:
            seqs = (preds > pred_thresh)
        elif 'ground_truth' in qoi:
            seqs = labels > 0
        output_lengths = np.array(
            [
                l + 1 if seqs[i, l] else 0
                for i, l in enumerate(seqs.argmax(axis=1))
            ]
        )
        prior_timestep = output_lengths - 1

        # b x t x f x t
        first_default_influences = np.array(
            [
                a[..., l - 1] if l > 0 else np.zeros_like(a[..., 0])
                for l, a in zip(output_lengths, influences)
            ]
        )
        prior_influences = np.array(
            [
                a[..., l - 1] if l > 0 else np.zeros_like(a[..., 0])
                for l, a in zip(prior_timestep, influences)
            ]
        )
        influences = first_default_influences - prior_influences

        labels = np.array(
            [p[l - 1] if l > 0 else 0 for l, p in zip(output_lengths, labels)]
        )
        preds = np.array(
            [p[l - 1] if l > 0 else 0 for l, p in zip(output_lengths, preds)]
        )
        sample_filter = output_lengths > 0

    grouping_preds = preds > pred_thresh
    grouping_labels = labels > 0
    return influences, sample_filter, input_lengths, grouping_labels, grouping_preds


def _get_top_feature_idx(seq, sort: InfluenceAggregationMethod, top_n):
    '''
    Applies different norms to the features and returns the sorted order of features and the aggregation values
    '''
    if sort == InfluenceAggregationMethod.MEAN_ABS:  # absolute influence with mean correction
        agg_seq = np.abs(seq - np.expand_dims(seq.mean(1), axis=1)).mean(1)
    elif sort == InfluenceAggregationMethod.VAR:  # influence variance
        agg_seq = seq.var(1)
    else:
        agg_seq = seq.mean(1)
    sorted_index = np.argsort(agg_seq)

    # reverse order if not looking at least influential
    if sort != InfluenceAggregationMethod.MIN_VALUE:
        sorted_index = sorted_index[::-1]
    if top_n:
        sorted_index = sorted_index[:top_n]

    return sorted_index, agg_seq


def get_influences_alongside_filter(
    aiq: AIQ,
    artifacts_container: ArtifactsContainer,
    num_records: int,
    offset: int = 0,
    qoi_core_class: int = 0,
    qoi_compare_class: int = 0,
    qoi: str = 'last',
    from_layer: str = 'input',
    qoi_timestep: int = 0,
    pred_thresh: float = 0.5,
    filter_list: Optional[Sequence[ComponentData]] = None,
    artifacts_container_compare: Optional[ArtifactsContainer] = None,
    pred_thresh_compare: float = 0.5,
    swap_compare_filter: int = SwapComparisons.NONE.value,
    feature_index: Optional[int] = None
) -> Sequence[np.ndarray]:
    """
    Get influences when comparing between different class outputs
    Args:
        aiq (AIQ): an AIQ class that helps get influence information.
        artifacts_container (ArtifactsContainer): An ArtifactsContainer object that helps locate metadata.
        num_records (int): The number of records to return.
        offset (int): The offset to start the num_records.
        qoi_core_class (int): The main class to get influences from.
        qoi_compare_class (int): A comparitive class to subtract from the main qoi_core_class. This gets a difference of classes explanation.
        qoi (str): The type of qoi. Options are ['last', 'average','timestep','first default (prediction), 'first default (ground truth)']. These reference the timestep outputs.
        from_layer (str): The layer of attributions to get. Options are ['input','internal']
        qoi_timestep (int): If the qoi is 'timestep', this helps specify the timestep output
        pred_thresh (float): A threshold to use for filters. Defaults to 0.5
        filter_list (list of dash filter components): Filters to apply to the data.
        artifacts_container_compare (ArtifactsContainer or None): An ArtifactsContainer object that helps locate metadata of a compare artifact. 
        pred_thresh_compare(float or None): A threshold to use for filters on a compare artifact. Defaults to 0.5
        swap_compare_filter=SwapComparisons.NONE.value,
        feature_index (int or None): The feature influences to return. If none, then all features will be returned.

    Returns:
        influences (np.ndarray): An array of influences of the original influences minus the compare influences.
        sample_filter (np.ndarray): The records that pass the filter for the original data and the compare data.
        input_lengths (np.ndarray): The input lengths of the records.
        grouping_labels (np.ndarray): The labels exceeding the threshold. Used for grouping purposes in other functions.
        grouping_preds (np.ndarray): The predictions exceeding the threshold. Used for grouping purposes in other functions.
    """
    influences, sample_filter, lengths, grouping_labels, grouping_preds = get_compare_influences_from_qoi(
        aiq,
        qoi_core_class,
        qoi_compare_class,
        qoi,
        artifacts_container,
        num_records,
        offset=offset,
        pred_thresh=pred_thresh,
        from_layer=from_layer,
        qoi_timestep=qoi_timestep,
        artifacts_container_compare=artifacts_container_compare,
        pred_thresh_compare=pred_thresh_compare,
        feature_index=feature_index
    )
    data = aiq.get_data(
        artifacts_container,
        num_records,
        offset=offset,
        feature_index=feature_index
    )
    preds = aiq.get_predictions(artifacts_container, num_records, offset=offset)
    labels = aiq.get_ground_truth(
        artifacts_container, num_records, offset=offset
    )
    seq_lengths = aiq.get_lengths(
        artifacts_container, num_records, offset=offset
    )
    filter_criteria = Filters.get_multi_filter_criteria(
        aiq,
        qoi_core_class,
        preds,
        labels,
        influences,
        seq_lengths,
        artifacts_container,
        num_records,
        filter_list=filter_list,
        offset=offset
    )

    if (
        artifacts_container_compare is not None and
        SwapComparisons(swap_compare_filter) != SwapComparisons.NONE
    ):
        swap_filter_criteria = Filters.get_swap_filter_criteria(
            aiq,
            artifacts_container,
            artifacts_container_compare,
            swap_compare_filter,
            num_records,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            pred_thresh,
            pred_thresh_compare,
            offset=offset,
            qoi_timestep=qoi_timestep
        )
        filter_criteria = np.logical_and(filter_criteria, swap_filter_criteria)

    if sample_filter is not None:
        filter_criteria = np.logical_and(filter_criteria, sample_filter)

    return influences, filter_criteria, lengths, data, grouping_labels, grouping_preds


def get_all_influences(
    aiq,
    artifacts_container: ArtifactsContainer,
    num_records,
    offset=0,
    qoi_core_class=0,
    qoi_compare_class=0,
    qoi='average',
    from_layer='internal',
    qoi_timestep=0,
    pred_thresh=0.5,
    filter_list: Optional[Sequence[ComponentData]] = None,
    artifacts_container_compare=None,
    pred_thresh_compare=0.5,
    swap_compare_filter=SwapComparisons.NONE.value
):
    '''
    Gets the influences as a TemporalData structure
    '''
    influences, filter_criteria, seq_lengths, _, _, _ = get_influences_alongside_filter(
        aiq,
        artifacts_container,
        num_records,
        offset=offset,
        qoi_core_class=qoi_core_class,
        qoi_compare_class=qoi_compare_class,
        qoi=qoi,
        from_layer=from_layer,
        qoi_timestep=qoi_timestep,
        pred_thresh=pred_thresh,
        filter_list=filter_list,
        artifacts_container_compare=artifacts_container_compare,
        pred_thresh_compare=pred_thresh_compare,
        swap_compare_filter=swap_compare_filter
    )
    influences = np.array([a for f, a in zip(filter_criteria, influences) if f])
    seq_lengths = np.array(
        [s for f, s in zip(filter_criteria, seq_lengths) if f]
    )
    if len(influences) == 0:
        raise FilterError
    temporal_data = TemporalData(influences, seq_lengths, False)
    return temporal_data


def global_influences(
    aiq,
    top_n,
    artifacts_container: ArtifactsContainer,
    num_records,
    offset=0,
    sort: InfluenceAggregationMethod = InfluenceAggregationMethod.MEAN_ABS,
    qoi_core_class=0,
    qoi_compare_class=0,
    qoi='average',
    from_layer='internal',
    qoi_timestep=0,
    pred_thresh=0.5,
    filter_list: Optional[Sequence[ComponentData]] = None,
    artifacts_container_compare=None,
    pred_thresh_compare=0.5,
    swap_compare_filter=SwapComparisons.NONE.value
):
    '''
    Gets the global influence metrics from the model. 
    '''
    temporal_data = get_all_influences(
        aiq,
        artifacts_container,
        num_records,
        offset=offset,
        qoi_core_class=qoi_core_class,
        qoi_compare_class=qoi_compare_class,
        qoi=qoi,
        from_layer=from_layer,
        qoi_timestep=qoi_timestep,
        pred_thresh=pred_thresh,
        filter_list=filter_list,
        artifacts_container_compare=artifacts_container_compare,
        pred_thresh_compare=pred_thresh_compare,
        swap_compare_filter=swap_compare_filter
    )
    if temporal_data is None:
        raise FilterError
    seq = temporal_data.mean_over_timestep().T
    sorted_index, agg_seq = _get_top_feature_idx(seq, sort, top_n)
    return seq, sorted_index, agg_seq
