from typing import Optional, Sequence, Tuple

import networkx as nx
import numpy as np
import pandas as pd

from truera.rnn.general.selection.interaction_selection import InteractAlong
from truera.rnn.general.selection.interaction_selection import ModelGrouping
from truera.rnn.general.utils.time import TemporalData

from .processor import OverfittingProcessor


def _get_group_val(grouping, feature, index, timestep):
    if grouping is None:
        return None
    if isinstance(grouping, dict):
        grouping = grouping[feature]
    if len(grouping.shape) > 1 and grouping.shape[1] > 1:
        grouping = grouping[:, timestep]
    return grouping[index]


def _get_timestep_indices_from_num(num_timesteps, seq_length):
    '''
    Used to index into a forwards-padded (right-justified) array from a number of timesteps.
    num_timesteps = 2 would return [-1, -2]
    '''
    if num_timesteps is None or num_timesteps == 'all':
        timesteps = range(1, seq_length + 1)  # get full seq length
    else:
        timesteps = range(
            1,
            min(num_timesteps, seq_length) + 1
        )  # get max allowed seq length
    timesteps = -1 * np.array(timesteps)
    return timesteps


def _get_timestep_indices_from_index(timestep_index, seq_length):
    '''
    Used to index into a forwards-padded (right-justified) array from a single timestep index.
    Timestep 0 corresponds to index -1.
    Timestep 1 corresponds to index -2. etc. 
    2 timestep indeces from end would return [-1, -2]
    '''
    if timestep_index is None or timestep_index == 'all':
        timesteps = range(1, seq_length + 1)
    elif timestep_index < seq_length:
        timesteps = [timestep_index + 1]  # timesteps are zero-indexed
    else:
        timesteps = []  # chosen timestep does not exist for this record
    timesteps = -1 * np.array(timesteps)
    return timesteps


def input_influence_2d_dfs(
    feature_indices,
    feature_names,
    influences,
    data,
    lengths,
    index=None,
    length_thresh=None,
    length_thresh_le=False,
    timestep=None,
    grouping=None,
    sample_filter=None
):
    indices = range(len(lengths)) if index is None else [index]
    points = {f: [] for f in feature_indices}
    temporal_influences = TemporalData(influences, lengths,
                                       False).forward_pad_transform()
    temporal_data = TemporalData(data, lengths, False).forward_pad_transform()
    influences = temporal_influences.get_ndarray()
    data = temporal_data.get_ndarray()
    for i in indices:
        if sample_filter is not None and not sample_filter[i]:
            continue
        seq_length = lengths[i]
        timesteps = _get_timestep_indices_from_index(timestep, seq_length)
        if (
            not length_thresh or
            (not length_thresh_le and seq_length >= length_thresh) or
            (length_thresh_le and seq_length <= length_thresh)
        ):
            for t in timesteps:
                for f_i, feature in enumerate(feature_indices):
                    val = data[i, t, f_i]
                    inf = influences[i, t, f_i]
                    group = _get_group_val(
                        grouping, feature_names[f_i], i, seq_length + t
                    )

                    points[feature].append([val, inf, group, i])
    # TODO: filter 2D based on influence?
    dfs = {
        f:
        pd.DataFrame(points[f], columns=['vals', 'infs', 'group', 'indices'])
        for f in feature_indices
    }
    return dfs


def data_3d(
    influences,
    data,
    lengths,
    feature,
    index=None,
    length_thresh=None,
    length_thresh_le=False,
    num_timesteps=None,
    grouping=None,
    sample_filter=None
):
    '''
    outputs a list of list.
    top level list indices correspond to timestep from end.
    inside list is a list of points [val, inf, group, index]
    '''
    indexes = range(0, len(lengths)) if (index is None or
                                         index < 0) else [index]
    max_seq_length = np.max(lengths)
    steps_3d = range(max_seq_length) if (
        num_timesteps is None or num_timesteps == 'all'
    ) else range(num_timesteps)
    points = [[] for step in steps_3d]
    temporal_influences = TemporalData(influences, lengths,
                                       False).forward_pad_transform()
    temporal_data = TemporalData(data, lengths, False).forward_pad_transform()
    influences = temporal_influences.get_ndarray()
    data = temporal_data.get_ndarray()
    for i in indexes:
        if sample_filter is not None and not sample_filter[i]:
            continue
        seq_length = lengths[i]
        timesteps = _get_timestep_indices_from_num(num_timesteps, seq_length)
        if (
            not length_thresh or
            (not length_thresh_le and seq_length >= length_thresh) or
            (length_thresh_le and seq_length <= length_thresh)
        ):
            for graph_step, t in enumerate(timesteps):
                val = data[i, t, 0]
                inf = influences[i, t, 0]
                group = _get_group_val(grouping, feature, i, seq_length + t)
                points[graph_step].append([val, inf, group, i])
    return points


def density_surface(dfs_per_timestep, num_timesteps):
    num_feature_value_samples = len(list(dfs_per_timestep.values())[0])
    surface_data = np.zeros((num_feature_value_samples, num_timesteps))
    for timestep, df in dfs_per_timestep.items():
        surface_data[:, timestep] = df['fit']
    return surface_data


def convert_data_3d_to_points(data):
    points = []
    for timestep in range(len(data)):
        for item in data[timestep]:
            points.append([timestep, item[0], item[1], item[2], item[3]])
    return np.array(points)


def fit_poly_only(data, max_length, poly_order=3):
    '''
    return 3d spline coefficients
    '''
    poly_per_ts = np.zeros((max_length, poly_order + 1))
    for timestep in range(len(data)):
        x = []
        y = []
        for point in data[timestep]:
            x.append(point[0])
            y.append(point[1])
        # calculate polynomial
        if np.count_nonzero(x) > 0:  # degenerate case where x is all 0
            z = np.polyfit(x, y, poly_order)
            poly_per_ts[timestep] = z
    return poly_per_ts


def fit_data(data):
    fit_points = []
    for timestep in range(len(data)):
        x = []
        y = []
        for point in data[timestep]:
            x.append(point[0])
            y.append(point[1])
        try:
            # calculate polynomial
            z = np.polyfit(x, y, 3)
            f = np.poly1d(z)
            # calculate new x's and y's
            x_fit = np.linspace(min(x), max(x), 100)
            y_fit = f(x_fit)

            timestep_vector = np.ones_like(x_fit) * timestep
            fit_points.extend(np.stack((timestep_vector, x_fit, y_fit), axis=1))
        except:  # catch linalg errors if polyfit fails
            continue
    return fit_points


def fit(df, min_x=None, max_x=None, dim=3, num_samples=100):
    # get x and y vectors
    x = df['vals'].tolist()
    y = df['infs'].tolist()
    if (len(x) < dim):
        return None
    # calculate polynomial
    z = np.polyfit(x, y, dim)
    f = np.poly1d(z)
    # calculate new x's and y's
    min_x = min_x if min_x is not None else min(x)
    max_x = max_x if max_x is not None else max(x)
    x_fit = np.linspace(min_x, max_x, num_samples)
    y_fit = f(x_fit)
    df = pd.DataFrame(np.stack((x_fit, y_fit), axis=1), columns=['x', 'fit'])
    return df


def get_grouping(
    grouping_str: ModelGrouping, labels: np.ndarray, preds: np.ndarray,
    lengths: Sequence[int], influences: np.ndarray, vals: np.ndarray,
    features: Sequence[str]
) -> Tuple[np.ndarray, Sequence[str]]:
    """Returns an array of grouping idx per record.

    Args:
        grouping_str (ModelGrouping): The type of grrouping to do.
        labels (np.ndarray): The labels, which can be needed for grouping
        preds (np.ndarray): The preds, which can be needed for grouping
        lengths (Sequence[int]): The lengths, which can be needed for grouping
        influences (np.ndarray): The influences, which can be needed for grouping
        vals (np.ndarray): The vals, which can be needed for grouping
        features (Sequence[str]): The feature names, which can be needed for grouping

    Returns:
        Tuple[np.ndarray, Sequence[str]]: The first ndarray is the group idx per record. The list of names are the group names. 
            The groups will be integers, which correspond to the indices in the group names 
    """
    labels = labels.astype(int)
    timesteps = influences.shape[1]
    names = []
    grouping = None
    if grouping_str == ModelGrouping.OVERFITTING:
        grouping = OverfittingProcessor.rnn_density_diagnostic(
            influences, vals, lengths, features, timesteps
        )
        names = ["no", "yes"]
    elif grouping_str == ModelGrouping.PREDICTION:
        grouping = preds
        names = ['<= threshold', '> threshold']
    elif grouping_str == ModelGrouping.GROUND_TRUTH:
        grouping = labels
        names = ['<= threshold', '> threshold']
    elif grouping_str == ModelGrouping.CONFUSION_MATRIX:
        indices = {"0 0": 0, "0 1": 1, "1 0": 2, "1 1": 3}
        grouping = np.array(
            [
                indices[str(int(p)) + " " + str(int(l))]
                for p, l in zip(preds, labels)
            ]
        )
        names = [
            "true negative", "false negative", "false positive", "true positive"
        ]
    else:
        grouping = np.zeros_like(labels)
        names = ['all']

    return grouping, names


def linear_correlation(x, axis):
    if axis == InteractAlong.FEATURE_DIM.value:
        y = np.linalg.norm(x, axis=2, ord=2)
    elif axis == InteractAlong.TEMPORAL_DIM.value:
        y = np.linalg.norm(x, axis=1, ord=2)
    else:
        y = np.reshape(x, (x.shape[0], -1))
    feature_name = ["f" + str(i) for i in range(y.shape[-1])]
    return np.corrcoef(y.T), feature_name


def partial_correlation(x, axis):
    """
    Reference
        [1] https://en.wikipedia.org/wiki/Partial_correlation
        [2] https://www.cs.cmu.edu/~epxing/Class/10708-14/lectures/lecture10-NetworkLearning.pdf
    """

    if axis == InteractAlong.FEATURE_DIM.value:
        y = np.linalg.norm(x, axis=2, ord=2)
    elif axis == InteractAlong.TEMPORAL_DIM.value:
        y = np.linalg.norm(x, axis=1, ord=2)
    else:
        y = np.reshape(x, (x.shape[0], -1))
    feature_name = ["f" + str(i) for i in range(y.shape[-1])]

    cov = np.cov(y.T)
    not_PSD = False
    v, u = np.linalg.eig(cov)
    if np.min(v) < 0:
        not_PSD = True
        eps = np.abs(np.min(v))
    else:
        eps = 0

    inv_cov = np.linalg.inv(cov + np.eye(cov.shape[0]) * eps)
    R = np.ones_like(inv_cov)
    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            if i != j:
                R[i,
                  j] = -inv_cov[i, j] / np.sqrt(inv_cov[i, i] * inv_cov[j, j])

    return R, feature_name, not_PSD


def auto_correlation(x):

    def _autocorr(signal):
        """
        Definition: https://en.wikipedia.org/wiki/Autocorrelation
        Implementation Reference:
            https://www.kite.com/python/answers/how-to-calculate-autocorrelation-in-python
        """

        result = np.correlate(signal, signal, mode='full')
        return result[result.size // 2:]

    result = []
    for i in range(x.shape[-1]):
        acc = 0
        for n in range(x.shape[0]):
            acc += _autocorr(x[n, :, i])
        acc /= x.shape[0]
        acc /= acc[0]
        result.append(acc)
    return result


def sigmoid(x, alpha=1):
    return alpha / 1 + np.exp(-x)


def undirectional_graph(matrix, weight_amplify=10):
    G = nx.from_numpy_matrix(matrix)
    pos = nx.spring_layout(G, dim=2)
    edge_x, edge_y = [], []
    weight = []

    for edge in G.edges():
        i, j = edge
        if matrix[i, j] > 0:
            x0, y0 = pos[i]
            x1, y1 = pos[j]
            edge_x.append([x0, x1, None])
            edge_y.append([y0, y1, None])
            weight.append(matrix[i, j])

    node_x, node_y = [], []
    for i in range(len(pos)):
        x, y = pos[i]
        node_x.append(x)
        node_y.append(y)

    node_adj = []
    for node, adj in enumerate(G.adjacency()):
        node_adj.append(len(adj[1]))

    return edge_x, edge_y, node_x, node_y, weight, node_adj


def pairwise_influences_3d(
    influences: np.ndarray,
    data: np.ndarray,
    lengths: Sequence[int],
    grouping_feature: ModelGrouping,
    timestep_feature1: Optional[int] = None,
    timestep_feature2: Optional[int] = None,
    grouping: np.ndarray = None
) -> Sequence[Sequence[int]]:
    """Returns plot information for 3d graphing of pairwise interactions

    Args:
        influences (np.ndarray): The influences
        data (np.ndarray): The input data
        lengths (Sequence[int]): the length of input
        grouping_feature (str): The type of grouping to filter on. 
        timestep_feature1 (int, optional): The timestep of the first selected feature
        timestep_feature2 (int, optional): The timestep of the second selected feature
        grouping (np.ndarray, optional): the groupings of each record.

    Returns:
        Sequence[Sequence[int]]: The outer sequence is each point. The innter sequence is a list of metadata. The metadata ints
        are 'value of feature 1', 'value of feature 2', 'joint influence', 'group member', 'point id'
    """
    temporal_influences = TemporalData(influences, lengths,
                                       False).forward_pad_transform()
    temporal_data = TemporalData(data, lengths, False).forward_pad_transform()
    influences = temporal_influences.get_ndarray()
    data = temporal_data.get_ndarray()
    points = []
    for i in range(len(lengths)):
        seq_length = lengths[i]
        timesteps_f1 = _get_timestep_indices_from_index(
            timestep_feature1, seq_length
        )
        timesteps_f2 = _get_timestep_indices_from_index(
            timestep_feature2, seq_length
        )
        assert len(timesteps_f1) == len(timesteps_f2)
        for ti in range(len(timesteps_f1)):
            t_f1 = timesteps_f1[ti]
            t_f2 = timesteps_f2[ti]
            val1 = data[i, t_f1, 0]
            val2 = data[i, t_f2, 1]
            inf = influences[i, t_f1, 0] + influences[i, t_f2, 1]
            group = _get_group_val(
                grouping, grouping_feature, i, seq_length + t_f1
            )
            points.append([val1, val2, inf, group, i])
    return np.array(points)
