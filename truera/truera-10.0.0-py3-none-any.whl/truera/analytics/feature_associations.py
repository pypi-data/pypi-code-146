import logging
import math
import os
import string
import threading

import networkx as nx
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import entropy
from sklearn.metrics.cluster import contingency_matrix

from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    FeatureAssociationsGraphResponse  # pylint: disable=no-name-in-module
from truera.utils import file_utils

_CACHE_FILENAME_PREFIX = "feature_associations"
_NUM_CHARS_FOR_RANDOM_PLACEHOLDER = 20
_CENTRAL_NODE_EDGE_WEIGHT = 0.001


class FeatureAssociations:

    def __init__(self, cache_directory):
        self._logger = logging.getLogger(__name__)
        self._cache_directory = cache_directory
        self._lock = threading.Lock()

    def compute_feature_associations_graph(
        self, xs, cache_key_map, special_value=None, seed=0
    ):
        # pylint: disable=no-member
        cache_key = ",".join(
            ["{}={}".format(k, v) for k, v in cache_key_map.items()]
        )
        # TODO(davidkurokawa): Currently this only allows us to compute/retrieve one feature association at a time.
        with self._lock:
            ret = self._retrieve_from_cache(cache_key)
            if ret is not None:
                return ret
            np.random.seed(seed)
            xs = xs.copy()
            FeatureAssociations._convert_to_categorical_columns(
                xs, special_value
            )
            symmetric_uncertainty_matrix = FeatureAssociations._compute_symmetric_uncertainty_matrix(
                xs
            )
            visualization_node_placements = FeatureAssociations._compute_force_directed_graph(
                symmetric_uncertainty_matrix.values, list(xs)
            )
            ret = FeatureAssociationsGraphResponse()
            FeatureAssociations._df_to_float_table(
                symmetric_uncertainty_matrix, ret.feature_associations
            )
            FeatureAssociations._df_to_float_table(
                visualization_node_placements, ret.visualization_node_placements
            )
            self._insert_in_cache(cache_key, ret)
        return ret

    def _cache_key_to_full_path(self, cache_key):
        cache_filename = _CACHE_FILENAME_PREFIX + "_" + cache_key
        return file_utils.join_path(self._cache_directory, cache_filename)

    def _retrieve_from_cache(self, cache_key):
        cache_full_path = self._cache_key_to_full_path(cache_key)
        if os.path.exists(cache_full_path):
            ret = FeatureAssociationsGraphResponse()
            with open(cache_full_path, "rb") as f:
                ret.ParseFromString(f.read())
            return ret

    def _insert_in_cache(self, cache_key, cache_entry):
        cache_filename = self._cache_key_to_full_path(cache_key)
        os.makedirs(os.path.dirname(cache_filename), exist_ok=True)
        with open(cache_filename, "wb") as f:
            f.write(cache_entry.SerializeToString())

    @staticmethod
    def _df_to_float_table(df, float_table, set_row_labels=True):
        if set_row_labels:
            float_table.row_labels.extend(df.index)
        for col in list(df):
            float_table.column_value_map[col].values.extend(df[col])

    @staticmethod
    def _convert_to_categorical_columns(xs, special_value, num_bins=20):
        # Fill null in categorical columns.
        cat_cols = list(xs.dtypes[xs.dtypes == "object"].index)
        replacement_value = res = "".join(
            np.random.choice(
                list(string.ascii_letters), _NUM_CHARS_FOR_RANDOM_PLACEHOLDER
            )
        )
        for cat_col in cat_cols:
            xs[cat_col].fillna(replacement_value, inplace=True)
        # Convert numerical columns to categorical columns.
        num_cols = list(xs.dtypes[xs.dtypes != "object"].index)
        for num_col in num_cols:
            null_mask = (xs[num_col] == special_value) | (xs[num_col].isna())
            unique = np.unique(xs[num_col])
            if len(unique) <= 2:
                quantiles = np.sort(unique)
                quantiles = quantiles.astype(np.float32)
                quantiles = np.unique(quantiles)
            else:
                quantiles = xs[num_col].quantile(
                    np.arange(0, 1, 1 / num_bins)[1:]
                )
                quantiles = quantiles.astype(np.float32)
                quantiles = quantiles.unique()
            quantiles = np.insert(quantiles, 0, -np.inf)
            quantiles = np.insert(quantiles, len(quantiles), np.inf)
            xs[num_col] = pd.cut(xs[num_col], labels=False, bins=quantiles)
            xs[num_col][null_mask] = -1

    # This function is largely copied from sklearn.metrics.mutual_info_score but uses more precision.
    @staticmethod
    def _compute_mutual_information(a, b):
        a = a.values.astype(np.str)
        b = b.values.astype(np.str)
        contingency = contingency_matrix(a, b, sparse=True)
        nza, nzb, nz_val = sparse.find(contingency)
        contingency_sum = contingency.sum()
        pi = np.ravel(contingency.sum(axis=1))
        pj = np.ravel(contingency.sum(axis=0))
        log_contingency_nm = np.log(nz_val)
        contingency_nm = nz_val / contingency_sum
        outer = pi.take(nza).astype(np.int64, copy=False) * pj.take(nzb).astype(
            np.int64, copy=False
        )
        log_outer = -np.log(outer) + np.log(pi.sum()) + np.log(pj.sum())
        mi = contingency_nm * (
            log_contingency_nm - np.log(contingency_sum)
        ) + contingency_nm * log_outer
        return mi.sum()

    @staticmethod
    def _compute_entropy(x):
        p = x.value_counts().values
        p = p / np.sum(p)
        return entropy(p)

    @staticmethod
    def _compute_symmetric_uncertainty(a, b):
        ha = FeatureAssociations._compute_entropy(a)
        hb = FeatureAssociations._compute_entropy(b)
        if ha == 0 and hb == 0:
            return 1
        mi = FeatureAssociations._compute_mutual_information(a, b)
        return max(0, 2 * mi / (ha + hb))

    @staticmethod
    def _compute_symmetric_uncertainty_matrix(df):
        arr = df.values
        features = list(df)
        num_features = len(features)
        ret = np.zeros((num_features, num_features))
        for r in range(num_features):
            ret[r, r] = 1
            for c in range(r + 1, num_features):
                su = FeatureAssociations._compute_symmetric_uncertainty(
                    df[features[r]], df[features[c]]
                )
                ret[r, c] = su
                ret[c, r] = su
        return pd.DataFrame(data=ret, index=features, columns=features)

    @staticmethod
    def _compute_force_directed_graph(
        adjacency_matrix, features, num_iterations=10000
    ):
        g = nx.Graph()
        num_features = len(features)
        central_node = "".join(
            np.random.choice(
                list(string.ascii_letters), _NUM_CHARS_FOR_RANDOM_PLACEHOLDER
            )
        )
        for r in range(num_features):
            for c in range(r + 1, num_features):
                g.add_weighted_edges_from(
                    [(features[r], features[c], adjacency_matrix[r, c])]
                )
                g.add_weighted_edges_from(
                    [(features[r], central_node, _CENTRAL_NODE_EDGE_WEIGHT)]
                )
        positions = nx.drawing.layout.spring_layout(
            g, iterations=num_iterations
        )
        positions.pop(central_node)
        return pd.DataFrame.from_dict(
            positions, orient="index", columns=["x", "y"]
        )
