import abc


class Converters(object, metaclass=abc.ABCMeta):
    def __init__(self, java_bridge):
        self._java_bridge = java_bridge
        self._tsc = self._java_bridge._tsc

    @abc.abstractmethod
    def from_df_to_ts(
        self, df, ts_column=None, value_column=None, granularity=None, start_time=None
    ):
        pass

    @abc.abstractmethod
    def from_numpy_to_ts(self, np_array, granularity=None, start_time=None):
        pass

    @abc.abstractmethod
    def from_df_observations_to_mts(
        self,
        df,
        key_column,
        ts_column=None,
        value_column=None,
        granularity=None,
        start_time=None,
    ):
        pass

    @abc.abstractmethod
    def from_df_instants_to_mts(
        self, df, key_columns=None, ts_column=None, granularity=None, start_time=None
    ):
        pass

    @abc.abstractmethod
    def from_numpy_to_mts(self, np_array, granularity=None, start_time=None):
        pass

    @abc.abstractmethod
    def bound_ts_to_numpy(self, bound_ts):
        pass

    @abc.abstractmethod
    def bound_ts_to_df(self, bound_ts, array_index_to_col=False):
        pass

    @abc.abstractmethod
    def bound_mts_to_numpy(self, bound_mts):
        pass

    @abc.abstractmethod
    def bound_mts_to_df(
        self, bound_mts, format="observations", array_index_to_col=False, key_col=None
    ):
        pass
