from autoai_ts_libs.deps.tspy.data_structures.transforms import UnaryTransform
import autoai_ts_libs.deps.tspy


class MapObservation(UnaryTransform):
    def __init__(self, f):
        self._f = f

    def evaluate(self, time_series, start, end, inclusive_bounds):
        observations = time_series.materialize(start, end, inclusive_bounds)

        builder = autoai_ts_libs.deps.tspy.builder()
        for o in observations:
            builder.add(self._f(o))
        return builder.result()
