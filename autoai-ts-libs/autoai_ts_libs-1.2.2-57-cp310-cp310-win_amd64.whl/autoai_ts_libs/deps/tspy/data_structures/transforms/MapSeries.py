from autoai_ts_libs.deps.tspy.data_structures.transforms import UnaryTransform


class MapSeries(UnaryTransform):
    def __init__(self, f):
        self._f = f

    def evaluate(self, time_series, start, end, inclusive_bounds):
        observations = time_series.materialize(start, end, inclusive_bounds)
        return self._f(observations)
