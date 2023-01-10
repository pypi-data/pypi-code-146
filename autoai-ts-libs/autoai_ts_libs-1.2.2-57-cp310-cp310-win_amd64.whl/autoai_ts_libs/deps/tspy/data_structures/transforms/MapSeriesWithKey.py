from autoai_ts_libs.deps.tspy.data_structures.transforms import UnaryTransform


class MapSeriesWithKey(UnaryTransform):
    def __init__(self, f, key):
        self._f = f
        self._key = key

    def evaluate(self, time_series, start, end, inclusive_bounds):
        observations = time_series.materialize(start, end, inclusive_bounds)
        return self._f(observations, self._key)
