import numpy as np
import pandas as pd
from ...abstract import AbstractPredictor
from ...models import DataFramePivotFields
from ...models import DefaultValues


pivot_fields = DataFramePivotFields()
defaults = DefaultValues()


class STCM(AbstractPredictor):
    """
    Spatio-temporal clustering model performing clustering
    based on coordinates and time-stamp
    """

    # SOURCE FIELDS
    _LAT_COL = pivot_fields.projected_lat
    _LON_COL = pivot_fields.projected_lon
    _UNIXTIME_COL = pivot_fields.computed_unixtime
    _FRAGM_FLAG_COL = pivot_fields.fragmentation_output
    # INTERNAL UTILITY FIELDS
    _TEMP_CLUSTER_ID = pivot_fields.clustering_output
    _PROX_DIST_COL = "proximity_distance"
    _SPATIAL_PROXIMITY_FLAG = "is_spatially_near"
    _VALID_CLUSTERS_ID = "validated_cluster_id"
    # DEFAULTS
    _NOISE_GPS_ID = defaults.noise_gps_cluster_id
    _CLUST_CANDIDS_FRAC = 1
    # CLUSTER AGGREGATES DEFAULTS
    _AGG_N_STATIONARY = "n_stationary"
    _AGG_N_TOTAL = "n_total"
    _AGG_UNIX_START = "unixtime_start"
    _AGG_UNIX_END = "unixtime_end"
    _AGG_DURATION = "duration"
    _AGG_FRAC_STAT_PTS = "frac_stationary_points"

    def __init__(
        self,
        eps: float,
        min_duration_sec: float,
    ):
        """
        Args:
        eps (float): Max distance span between 2 adjacent
            gps records to link together
        min_duration_sec (float): Minimum duration spent on site to form cluster
        """
        self.eps = eps
        self.min_duration_sec = min_duration_sec

    def __compute_adj_prox_flag(self, X: pd.DataFrame):
        _adj_shift = 1
        d_lat = X[self._LAT_COL] - X[self._LAT_COL].shift(_adj_shift)
        d_lon = X[self._LON_COL] - X[self._LON_COL].shift(_adj_shift)
        X[self._PROX_DIST_COL] = np.sqrt(d_lat**2 + d_lon**2)
        X[self._SPATIAL_PROXIMITY_FLAG] = X[self._PROX_DIST_COL] <= self.eps
        return X

    def __generate_cluster_candidates(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        NOTE: Intuition is change is based on any inverted flag change
        Function generates initial ids for potential cluster candidates
            based on adjacent flag distance and stationary point flags

        Args:
        X (pd.DataFrame): input gps

        Returns:
        pd.DataFrame: gps with expanded cluster candidate id
        """
        _adj_prox_flag_inv = ~X[self._SPATIAL_PROXIMITY_FLAG]
        _stationary_flag_inv = ~X[self._FRAGM_FLAG_COL]
        _change_flag = _adj_prox_flag_inv | _stationary_flag_inv
        X[self._TEMP_CLUSTER_ID] = np.cumsum(_change_flag)
        return X

    def __agg_clusters_candidates(self, X: pd.DataFrame) -> pd.DataFrame:
        group_cols = [self._TEMP_CLUSTER_ID]
        agg_parameters = {
            self._AGG_N_STATIONARY: (self._FRAGM_FLAG_COL, "sum"),
            self._AGG_N_TOTAL: (self._TEMP_CLUSTER_ID, "count"),
            self._AGG_UNIX_START: (self._UNIXTIME_COL, "first"),
            self._AGG_UNIX_END: (self._UNIXTIME_COL, "last"),
        }
        X_agg = X.groupby(group_cols).agg(**agg_parameters).reset_index()
        X_agg[self._AGG_DURATION] = X_agg[self._AGG_UNIX_END] - X_agg[self._AGG_UNIX_START]
        X_agg[self._AGG_FRAC_STAT_PTS] = X_agg[self._AGG_N_STATIONARY] / X_agg[self._AGG_N_TOTAL]
        return X_agg

    def __valid_clust_candidates(self, X: pd.DataFrame) -> pd.DataFrame:
        _time_constr = X[self._AGG_DURATION] >= self.min_duration_sec
        _stat_pts_constr = X[self._AGG_FRAC_STAT_PTS] >= self._CLUST_CANDIDS_FRAC
        _validation_mask = _time_constr & _stat_pts_constr
        X = X.loc[_validation_mask, :].reset_index(drop=True)
        X[self._VALID_CLUSTERS_ID] = X.index
        return X

    def __set_cluster_ids_to_input_gps(self, X_original: pd.DataFrame, cluster_ids: pd.DataFrame):
        _join_columns = [self._TEMP_CLUSTER_ID, self._VALID_CLUSTERS_ID]
        derived_cluster_ids = cluster_ids.loc[:, _join_columns]
        X_original = X_original.merge(derived_cluster_ids, how="left")
        _id_values = X_original.loc[:, self._VALID_CLUSTERS_ID]
        _id_values = _id_values.fillna(self._NOISE_GPS_ID)
        _id_values = _id_values.astype(int)
        X_original[self._VALID_CLUSTERS_ID] = _id_values
        return X_original

    def __get_cluster_ids_vector(self, X: pd.DataFrame) -> np.array:
        return X[self._VALID_CLUSTERS_ID].values

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def __validate_time_sequence(self, X: pd.DataFrame):
        time_delta = X[self._UNIXTIME_COL] - X[self._UNIXTIME_COL].shift(1)
        time_delta = time_delta.fillna(method="bfill")
        if (time_delta < 0).any():
            raise ValueError("Input gps time stamps must be ordered over time-stamp")

    def predict(self, X: pd.DataFrame) -> np.array:
        X = self._get_input_copy(X)
        self.__validate_time_sequence(X)
        X = self.__compute_adj_prox_flag(X)
        X = self.__generate_cluster_candidates(X)
        clusters = self.__agg_clusters_candidates(X)
        clusters = self.__valid_clust_candidates(clusters)
        X = self.__set_cluster_ids_to_input_gps(X, clusters)
        cluster_ids_vec = self.__get_cluster_ids_vector(X)
        return cluster_ids_vec
