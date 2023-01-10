from autoai_ts_libs.deps.tspy.data_structures.transforms import UnaryTransform
import autoai_ts_libs.deps.tspy
import numpy as np

class Map(UnaryTransform):
    def __init__(self, f):
        self._f = f

    def _result_is_numpy(self, resulting_value):
        numpy_types = {float, int, bool, np.ndarray, str, np.int8, np.int16, np.int32, np.int64, np.float32,
                       np.float64}
        return type(resulting_value) in numpy_types

    def evaluate(self, time_series, start, end, inclusive_bounds):
        observations = time_series.materialize(start, end, inclusive_bounds)

        if len(observations) == 0:
            return autoai_ts_libs.deps.tspy.observations()

        iter_observations = observations._raw_iter()
        tt, val = next(iter_observations)
        current_result = self._f(val)

        if self._result_is_numpy(current_result):

            if observations._j_observations.isPythonBacked():
                result_tt = observations._j_observations.getTimeTickBuffer()
                result_values = []
                while True:
                    try:
                        result_values.append(current_result)
                        tt, val = next(iter_observations)
                        current_result = self._f(val)
                    except StopIteration:
                        break
                return autoai_ts_libs.deps.tspy.observations(np.asarray(result_tt), np.asarray(result_values))
            else:
                result_tt = []
                result_values = []
                while True:
                    try:
                        result_tt.append(tt)
                        result_values.append(current_result)
                        tt, val = next(iter_observations)
                        current_result = self._f(val)
                    except StopIteration:
                        break
                return autoai_ts_libs.deps.tspy.observations(np.asarray(result_tt), np.asarray(result_values))
        else:
            builder = autoai_ts_libs.deps.tspy.builder()
            for o in observations:
                builder.add(o.time_tick, self._f(o.value))
            return builder.result()
