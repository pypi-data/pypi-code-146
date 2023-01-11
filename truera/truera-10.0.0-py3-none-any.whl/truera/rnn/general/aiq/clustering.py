from typing import Any, Dict, Iterable, Tuple

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.cluster import SpectralCoclustering

NUM_FEATURES_KEY = "num_features"
SUBTREE_SIZE_KEY = "subtree_size"
ID_KEY = "id"
ANCESTOR_ID_KEY = "ancestor_ids"
SUBTREE_IDXS_KEY = "subtree_idxs"
PARENT_ID_KEY = "parent_id"
FEATURE_KEY = "feature"
FEATURE_IDX_KEY = "f_idx"
X_KEY = "x"
Y_KEY = "y"


def graph_to_layout(vertices: Iterable[int], edges: Iterable[Tuple[int, int]]):
    g = nx.Graph()
    g.add_nodes_from(vertices)
    g.add_edges_from(edges)
    nodePos = nx.kamada_kawai_layout(g, center=[0, 0])

    layout_x_y = np.zeros([len(vertices), 2])
    for i in range(len(vertices)):
        layout_x_y[i] = nodePos[vertices[i]]
    return layout_x_y


class SpectralHierarchicalClusterer(object):

    def __init__(self, parent: "Tree" = None):
        self.parent = parent
        self.children = []
        self._attr_dict = {}
        self.grouping = None

    # tree building methods
    def _spawn_children(self,
                        edge_weights: np.ndarray,
                        n_clusters: int = 2) -> Iterable[np.ndarray]:
        """
        Apply spectral coclustering into n_clusters and return the cluster matrices
        """
        if (len(edge_weights) <= 1):
            self.grouping = np.array([0])
            return []
        model = SpectralCoclustering(n_clusters=n_clusters, random_state=0)
        model.fit(edge_weights)
        self.grouping = model.row_labels_
        all_child_weights = []
        for cluster_idx in range(n_clusters):
            matrix_idxs = np.where(self.grouping == cluster_idx)[0]
            child = SpectralHierarchicalClusterer(parent=self)
            child_weights = edge_weights[np.ix_(matrix_idxs, matrix_idxs)]

            self.children.append(child)
            all_child_weights.append(child_weights)
        return all_child_weights

    def build_full_binary(self, edge_weights: np.ndarray) -> None:
        """
        Recursively build a binary tree by splitting the correlation matrix on the spectral coclustering (strongest connected correlation tokens)
        """
        child_weights = self._spawn_children(edge_weights)
        for child_weight, child in zip(child_weights, self.children):
            child.build_full_binary(child_weight)

    def build_attr_dict(self, corr_idx_map: Dict) -> None:
        """
        Initialize a dictionary to hold metadata about this clusterer.

        Parameters
        ===============
        corr_idx_map: A list representing a mapping from correlation matrix id to feature id. 
            The list idx corresponds to the correlation matrix idx, and the value is the token id.
            This usually happens if the clusterer was filtered on a smaller subset of features.
        """
        self._attr_dict[NUM_FEATURES_KEY] = len(self.grouping)
        self._attr_dict[SUBTREE_SIZE_KEY] = 1
        if (ID_KEY not in self._attr_dict):
            self._attr_dict[ID_KEY] = 0
        if (ANCESTOR_ID_KEY not in self._attr_dict):
            self._attr_dict[ANCESTOR_ID_KEY] = set()
        if (SUBTREE_IDXS_KEY not in self._attr_dict):
            corr_idxs = np.arange(self._attr_dict[NUM_FEATURES_KEY])
            self._attr_dict[SUBTREE_IDXS_KEY] = np.asarray(
                [corr_idx_map[corr_idxs] for corr_idxs in corr_idxs]
            )

        for child_idx, child in enumerate(self.children):
            matrix_idxs = np.where(self.grouping == child_idx)[0]
            child._attr_dict[SUBTREE_IDXS_KEY] = self._attr_dict[
                SUBTREE_IDXS_KEY][matrix_idxs]
            child._attr_dict[ID_KEY] = self._attr_dict[
                ID_KEY] + self._attr_dict[SUBTREE_SIZE_KEY]
            child._attr_dict[PARENT_ID_KEY] = self._attr_dict[ID_KEY]
            child._attr_dict[ANCESTOR_ID_KEY] = set(
                self._attr_dict[ANCESTOR_ID_KEY]
            )
            child._attr_dict[ANCESTOR_ID_KEY].update([self._attr_dict[ID_KEY]])
            child.build_attr_dict(corr_idx_map)
            self._attr_dict[SUBTREE_SIZE_KEY] += child._attr_dict[
                SUBTREE_SIZE_KEY]

        if len(self._attr_dict[SUBTREE_IDXS_KEY]) == 1:
            self._attr_dict[FEATURE_IDX_KEY] = self._attr_dict[SUBTREE_IDXS_KEY
                                                              ][0]
            self._attr_dict[SUBTREE_SIZE_KEY] = 1

    # getters
    def get_attr_df(self, include_xy=True) -> pd.DataFrame:
        """
        Get the dictionary that holds metadata about this clusterer.
        """
        attr_df = pd.DataFrame.from_records(self._get_attr_dicts())
        if (include_xy):
            layout = graph_to_layout(*self.get_graph())
            attr_df[X_KEY] = layout[:, 0]
            attr_df[Y_KEY] = layout[:, 1]
        attr_df.set_index(ID_KEY, inplace=True)
        return attr_df

    def _get_attr_dicts(self) -> Iterable[Dict[str, Any]]:
        attr_dicts = [self._attr_dict]
        for child in self.children:
            attr_dicts += child._get_attr_dicts()
        return attr_dicts

    def get_graph(self) -> Tuple[Iterable[int], Iterable[Tuple[int, int]]]:
        nodes = [self._attr_dict[ID_KEY]]
        edges = [
            (self._attr_dict[ID_KEY], child._attr_dict[ID_KEY])
            for child in self.children
        ]
        for child in self.children:
            child_nodes, child_edges = child.get_graph()
            nodes += child_nodes
            edges += child_edges
        return nodes, edges

    @staticmethod
    def _get_correlation_matrices(
        grad_path_influences: np.ndarray,
        path_max_filter: float = 0,
        filter_top_n: int = -1
    ) -> Tuple[np.ndarray, Dict[int, int]]:
        """Gets the correlation matrices of feature to feature, using the pearson correlation on the token grad paths 

        Args:
            grad_path_influences (np.ndarray): The gradients of each record on the influence DoI
            path_max_filter (float, optional): A filter to apply to remove paths with max value in the bottom of the specified percentage. Defaults to 0.
            filter_top_n (int, optional): Only keeps the most interacting features by pearson correlation. Defaults to -1.

        Returns:
            Tuple[np.ndarray,Dict[int,int]]: 
                corrcoef (np.ndarray) - the correlation matrix 
                idx_mapping (Dict[int,int]) - a mapping of the correlation matrix indices to a feature index. 
                            usually 1:1 unless a top_n filter was applied or a token has no influence change.

        """
        assert 0 <= path_max_filter < 1

        corrcoefs = []
        idx_mappings = []

        for idx, gp_infl in enumerate(grad_path_influences):
            num_elements = gp_infl.shape[0]
            infl_path_max = np.max(np.abs(gp_infl), axis=-1)

            if path_max_filter > 0:
                elements_thresholded_low_infl_path_change = infl_path_max <= np.percentile(
                    infl_path_max, int(path_max_filter * 100)
                )
            else:
                elements_thresholded_low_infl_path_change = np.zeros(
                    infl_path_max.shape[0]
                ) != 0

            if (filter_top_n > 1 and filter_top_n < num_elements
               ) or any(elements_thresholded_low_infl_path_change):
                # Take the most interactive features. This is filtered on gradient change and not influence value.
                # High influence values will have high change, but some features may fluctuate up and down.

                # num features x 1
                most_active_paths = np.abs(gp_infl).sum(axis=-1)
                # num features x 1 (highest idx to lowest)
                most_active_paths = np.argsort(-most_active_paths, axis=-1)
                top_n_filter = most_active_paths[:filter_top_n]

                full_filter = np.intersect1d(
                    top_n_filter,
                    np.where(
                        np.
                        logical_not(elements_thresholded_low_infl_path_change)
                    )[0]
                )
                gp_infl = gp_infl[full_filter]
                idx_mappings.append(full_filter)
            else:
                idx_mappings.append(np.asarray(range(num_elements)))
            corrcoef = np.corrcoef(gp_infl)
            # All nan rows would happen when there is a feature with no variance
            # implying a linear sum through interpolation, also implying no interaction
            keep_only_interacting = np.logical_not(
                np.isnan(corrcoef).all(axis=0)
            )
            corrcoef = corrcoef[
                np.ix_(keep_only_interacting, keep_only_interacting)]
            idx_mappings[-1] = idx_mappings[-1][keep_only_interacting]

            corrcoefs.append(corrcoef)

        return corrcoefs, idx_mappings

    @staticmethod
    def interaction_dendrogram_info(
        corrs: np.ndarray,
        corr_idx_mapping,
        feature_column_names,
        num_records: int,
        offset: int = 0,
    ):
        """
        Takes records in the given artifact container from index offset to offset + num_records.
        Build a spectral coclustering-based binary tree of each record, and return a dataframe that contains
        (1) tree structure (parent, ancestors of each node)
        (2) link to original features (indexes in the original data)
        """
        clusterers = []

        for corr, corr_idx_map in zip(corrs, corr_idx_mapping):
            clusterer = SpectralHierarchicalClusterer()
            clusterer.build_full_binary(corr)
            clusterer.build_attr_dict(corr_idx_map)
            clusterers.append(clusterer)
        attr_dfs = [clusterer.get_attr_df() for clusterer in clusterers]
        return_dfs = {}
        correlation_matrices = {}
        correlation_idx_maps = {}

        for idx, features, attr_df, corr, corr_idx_map in zip(
            range(offset, offset + num_records), feature_column_names, attr_dfs,
            corrs, corr_idx_mapping
        ):
            attr_df[FEATURE_KEY] = attr_df.apply(
                lambda row: features[int(row.f_idx)]
                if row.f_idx < len(features) else np.nan,
                axis=1
            )
            return_dfs[idx] = attr_df, features
            correlation_matrices[idx] = corr
            correlation_idx_maps[idx] = corr_idx_map

        return return_dfs, correlation_matrices, correlation_idx_maps
