from autoai_ts_libs.deps.tspy.data_structures.cross_language.JPypeTSBuilder import JPypeTSBuilder
from autoai_ts_libs.deps.tspy.data_structures.cross_language.NumpyTSBuilder import NumpyTSBuilder
from autoai_ts_libs.deps.tspy.data_structures.observations.TSBuilder import TSBuilder
import numpy as np

class TSBuilderWrapper(TSBuilder):

    def __init__(self, tsc):
        super().__init__(tsc)
        self._builder = None

    def add(self, *args):
        if len(args) == 2:
            time_tick = args[0]
            value = args[1]
        else:
            if isinstance(args[0], tuple):
                time_tick = args[0][0]
                value = args[0][1]
            else:
                time_tick = args[0].time_tick
                value = args[0].value

        if self._builder is None:
            numpy_types = {float, int, bool, np.ndarray, str} # todo add obj str
            if type(value) in numpy_types:
                self._builder = NumpyTSBuilder(self._tsc)
            else:
                self._builder = JPypeTSBuilder(self._tsc)

        return self._builder.add(time_tick, value)

    def result(self, granularity=None, start_time=None):
        if self._builder is None:
            self._builder = JPypeTSBuilder(self._tsc)
            return self._builder.result(granularity, start_time)
        else:
            return self._builder.result(granularity, start_time)

    def clear(self):
        if self._builder is not None:
            return self._builder.clear()

    def is_empty(self):
        return self._builder is None or self._builder.is_empty()

    def add_all(self, observations):
        if len(observations) == 0:
            return self

        if self._builder is None:
            self.add(observations[0]) # this line will set the internal builder
            self._builder.add_all(observations[1:])
        else:
            self._builder.add_all(observations)
        return self
