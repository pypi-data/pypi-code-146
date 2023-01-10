import numpy as np

from autoai_ts_libs.deps.tspy.data_structures.observations.TSBuilder import TSBuilder
import sys

class NumpyTSBuilder(TSBuilder):

    def __init__(self, tsc):
        super().__init__(tsc)
        self._tsc = tsc
        self._time_ticks = [] # NDArrayList()
        self._values = [] # NDArrayList()
        self._min_iat = None
        self._max_iat = None
        self._unsorted_until_index = -1
        self._unsorted_min_time_tick = sys.maxsize
        self._max_time_tick = -sys.maxsize - 1
        self._min_time_tick = sys.maxsize

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

        self._max_time_tick = max(self._max_time_tick, time_tick)
        self._min_time_tick = min(self._min_time_tick, time_tick)
        self._time_ticks.append(time_tick)
        self._values.append(value)

        if len(self._time_ticks) >= 2:
            last = self._time_ticks[len(self._time_ticks) - 2]

            iat = time_tick - last
            if self._min_iat is None or self._max_iat is None:
                self._min_iat = iat
                self._max_iat = iat
            else:
                self._min_iat = min(self._min_iat, iat)
                self._max_iat = max(self._max_iat, iat)

            if self._min_iat < 0:
                self._unsorted_min_time_tick = min(self._unsorted_min_time_tick, time_tick)
                if self._unsorted_until_index == -1:
                    self._unsorted_until_index = len(self._time_ticks) - 1
        return self

    def result(self, granularity=None, start_time=None):
        self._enforce_sorting()

        if granularity is None and start_time is None:
            trs = None
        else:
            import datetime
            from autoai_ts_libs.deps.tspy.data_structures.observations.TRS import TRS
            if granularity is None:
                granularity = datetime.timedelta(milliseconds=1)
            if start_time is None:
                start_time = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
            trs = TRS(self._tsc, granularity, start_time)

        from autoai_ts_libs.deps.tspy.data_structures.observations.BoundTimeSeries import BoundTimeSeries
        from autoai_ts_libs.deps.tspy.data_structures.cross_language.PythonObservationCollection import PythonObservationCollection
        if trs is None:
            observations = PythonObservationCollection(
                data=(np.array(self._time_ticks), np.array(self._values)),
                iat=(self._min_iat, self._max_iat))
        else:
            observations = PythonObservationCollection(
                data=(np.array(self._time_ticks), np.array(self._values)),
                iat=(self._min_iat, self._max_iat),
                trs=trs)

        return BoundTimeSeries(
            self._tsc,
            self._tsc.packages.time_series.core.timeseries.BoundTimeSeries(observations))

    def is_empty(self):
        return self.__len__() == 0

    def add_all(self, observations):
        from autoai_ts_libs.deps.tspy.data_structures.observations.Observation import Observation
        if isinstance(observations[0], Observation):
            for o in observations:
                self.add(o)
        else:
            for o in observations:
                self.add(o[0], o[1])

        return self

    def clear(self):
        self._time_ticks = []
        self._values = []

    def __len__(self):
        return len(self._time_ticks)

    def _enforce_sorting(self):

        if self._min_iat is not None and self._min_iat < 0:
            # todo how to do without numpy or as efficient additions without a NDArrayList
            import numpy as np
            if self._unsorted_min_time_tick == sys.maxsize:
                inds = np.array(self._time_ticks).argsort()
                self._time_ticks = np.array(self._time_ticks)[inds].tolist()
                self._values = np.array(self._values)[inds].tolist()
            else:
                h = self._get_higher_index_til_unsorted(self._unsorted_min_time_tick)
                time_ticks_view = np.array(self._time_ticks[h:len(self._time_ticks)])
                values_view = np.array(self._values[h:len(self._values)])
                inds = time_ticks_view.argsort()
                self._time_ticks[h:len(self._time_ticks)] = time_ticks_view[inds].tolist()
                self._values[h:len(self._values)] = values_view[inds].tolist()

            self._unsorted_until_index = -1
            self._unsorted_min_time_tick = sys.maxsize

            self._recalculate_inter_arrival_times()

    def _recalculate_inter_arrival_times(self):
        self._min_iat = sys.maxsize
        self._max_iat = -sys.maxsize + 1

        for i in range(len(self._time_ticks) - 1):
            cur_iat = self._time_ticks[i + 1] - self._time_ticks[i]
            if cur_iat < self._min_iat:
                self._min_iat = cur_iat
            if cur_iat > self._max_iat:
                self._max_iat = cur_iat

    def _get_higher_index_til_unsorted(self, target):
        if len(self._time_ticks) == 0:
            return -1

        first = self._min_time_tick
        if target < first:
            return 0

        last = self._max_time_tick
        if target >= last:
            return -1

        offset = target - first
        l = self._get_min_index(offset)
        r = self._get_max_index(offset)

        l = max(l, 0)
        r = min(r + 1, self._unsorted_until_index)
        if r >= len(self._time_ticks):
            return -1

        result = -1
        while l <= r:
            m = int((l + r) / 2)
            if self._time_ticks[m] <= target:
                l = m + 1
            else:
                result = m
                r = m - 1
        return result

    def _get_min_index(self, offset):
        min_index = 0

        if self._max_iat is not None and self._max_iat > 0:
            min_index = int(offset / self._max_iat)
        return min_index

    def _get_max_index(self, offset):
        max_index = len(self._time_ticks) - 1

        if self._min_iat is not None and self._min_iat > 0:
            max_index = int(offset / self._min_iat)
            if offset % self._min_iat != 0:
                max_index += 1
        return max_index
