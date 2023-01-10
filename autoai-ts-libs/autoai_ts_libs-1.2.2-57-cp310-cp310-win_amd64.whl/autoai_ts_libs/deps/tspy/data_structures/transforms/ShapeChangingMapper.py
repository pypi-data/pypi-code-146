from autoai_ts_libs.deps.tspy.data_structures.transforms import UnaryTransform
import numpy as np
import autoai_ts_libs.deps.tspy
import abc

class ShapeChangingMapper(UnaryTransform, metaclass=abc.ABCMeta):
    def __init__(self, f):
        self._f = f

    @abc.abstractmethod
    def result_is_numpy(self, input_before_apply, input_after_apply, types_set):
        pass

    @abc.abstractmethod
    def handle_input_numpy(self, tts_reference, values_reference, tt, input_before_apply, input_after_apply):
        pass

    @abc.abstractmethod
    def handle_input_object(self, builder_reference, tt, input_before_apply, input_after_apply):
        pass

    @abc.abstractmethod
    def apply_lambda(self, value):
        pass

    def evaluate(self, time_series, start, end, inclusive_bounds):
        observations = time_series.materialize(start, end, inclusive_bounds)

        if len(observations) == 0:
            return autoai_ts_libs.deps.tspy.observations()

        iter_observations = observations._raw_iter()
        tt, val = next(iter_observations)
        current_result = self._f(val)

        numpy_types = {float, int, bool, np.ndarray, str, np.int8, np.int16, np.int32, np.int64, np.float32,
                       np.float64}

        if self.result_is_numpy(val, current_result, numpy_types):
            result_tt = []
            result_values = []

            while True:
                try:
                    self.handle_input_numpy(result_tt, result_values, tt, val, current_result)
                    tt, val = next(iter_observations)
                    current_result = self.apply_lambda(val)
                except StopIteration:
                    break

            return autoai_ts_libs.deps.tspy.observations(np.asarray(result_tt), np.asarray(result_values))

        else:
            builder = autoai_ts_libs.deps.tspy.builder()
            for o in observations:
                output = self.apply_lambda(o.value)
                self.handle_input_object(builder, o.time_tick, o.value, output)
            return builder.result()
