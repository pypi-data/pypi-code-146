import jpype
import pandas as pd
from jpype import JImplements, JOverride
import sys
import numpy as np
import autoai_ts_libs.deps.tspy


@JImplements('com.ibm.research.time_series.core.utils.ObservationCollection')
class PythonObservationCollection:
    """
    This collection assumes the data is sorted
    """

    def __init__(self, data, iat=None, indexes=None, trs=None):
        # if the data is not coming from another ObservationCollection, we must put the data into shared memory to be
        # accessed over DirectByteBuffers
        if isinstance(data, tuple) or indexes is None:
            time_ticks = data[0]
            values = data[1]

            # if the inter-arrival-times aren't known, calculate them
            if iat is None:
                self._calculate_iat(time_ticks)
            # the inter-arrival-times are known, so just use them as given
            else:
                self._min_iat = iat[0]
                self._max_iat = iat[1]

            # create a byte array which will be mapped on top of the Direct ByteBuffer
            # must multiply by 8 as we are storing Longs
            time_ticks_bytes = bytearray(8 * len(time_ticks))
            jb_time_ticks = jpype.nio.convertToDirectBuffer(time_ticks_bytes)
            # set the ByteOrder to little endian as that is the default for pandas/numpy
            jb_time_ticks.order(autoai_ts_libs.deps.tspy.ts_context.packages.java.nio.ByteOrder.LITTLE_ENDIAN)
            self._db_time_ticks = jb_time_ticks.asLongBuffer()

            # map the given time-ticks on top of the numpy array which is backed by shared memory
            # this will also set the values in the DirectByteBuffer
            self._time_ticks = np.asarray(self._db_time_ticks)
            self._time_ticks[:] = time_ticks

            # determine the backend storage for the values whether it be in DirectByteBuffers or Generic ArrayLists
            self._determine_db_values(values)

        # if the data is coming from another ObservationCollection, we must get a view on the data which is already
        # stored in DirectByteBuffers
        else:
            # set the time-ticks to the slice index's given
            self._time_ticks = data._time_ticks[indexes]

            # create a new slice DirectByteBuffer for the time-ticks which holds the information of the slice of data
            db_time_ticks = data._db_time_ticks.slice()

            # set the position for the time-ticks to the start of the slice
            db_time_ticks.position(indexes.start)

            # set the limit of the time-ticks to the current position + the size of the slice
            db_time_ticks.limit(db_time_ticks.position() + (indexes.stop - indexes.start))
            self._db_time_ticks = db_time_ticks

            self._keys = data._keys if (hasattr(data, "_keys") and data._keys is not None) else None

            # data values can either be stored in a ByteBuffer or a dictionary (coming from pandas df where each column
            # has a numpy array associated with it)
            # every point of data (whether it be from a dict or not will follow a similar pattern)
            # 1. slice the values based on the given indexes
            # 2. calculate the new position and limit of the new view
            # 3. set the position and limit of the new backend ByteBuffer view
            # 4. seed the new java utility with the old java utility

            # if the data is in a dictionary, handle each key separately and process as shown above
            if isinstance(data._values, dict):
                self._values = {}
                self._db_values = {}
                self._vector_len = {}
                j_utils = autoai_ts_libs.deps.tspy.ts_context.packages.java.util.HashMap()

                for k in data._keys:
                    # 1. slice the values based on the given indexes
                    self._values[k] = data._values[k][indexes]
                    self._vector_len[k] = data._vector_len[k]

                    # 2. calculate the new position and limit of the new view
                    position = indexes.start * self._vector_len[k] if self._vector_len[k] > 1 else indexes.start
                    length = self._vector_len[k] * (indexes.stop - indexes.start) if self._vector_len[k] > 1 else (
                            indexes.stop - indexes.start)

                    # 3. set the position and limit of the new backend ByteBuffer view
                    # if the data is in an ArrayList, that means it was a special case where the underlying data could
                    # not be handled by numpy and therefore is copied into an ArrayList
                    # Because ArrayLists don't hold information regarding the position and limit, pass that information
                    # into the java utility
                    if isinstance(data._db_values[k], autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList):
                        self._db_values[k] = data._db_values[k]
                        # 4. seed the new java utility with the old java utility
                        j_utils.put(k, self._get_j_util_generic_from_prev(data._j_util.getValueUtil(k), self._db_time_ticks,
                                                                  self._db_values[k], self._vector_len[k], position,
                                                                  position + length))
                    else:
                        self._db_values[k] = data._db_values[k].slice()
                        self._db_values[k].position(position)
                        self._db_values[k].limit(position + length)
                        # 4. seed the new java utility with the old java utility
                        j_utils.put(k, self._get_j_util_from_prev(data._j_util.getValueUtil(k), self._db_time_ticks, self._db_values[k], self._vector_len[k]))
                self._j_util = autoai_ts_libs.deps.tspy.ts_context.packages.time_series.core.utils.python.MapPythonObservationCollectionUtils(
                    self._db_time_ticks,
                    j_utils
                )
            else:
                # 1. slice the values based on the given indexes
                self._values = data._values[indexes]
                self._vector_len = data._vector_len

                # 2. calculate the new position and limit of the new view
                position = indexes.start * self._vector_len if self._vector_len > 1 else indexes.start
                length = self._vector_len * (indexes.stop - indexes.start) if self._vector_len > 1 else (
                            indexes.stop - indexes.start)

                # 3. set the position and limit of the new backend ByteBuffer view
                # if the data is in an ArrayList, that means it was a special case where the underlying data could
                # not be handled by numpy and therefore is copied into an ArrayList
                # Because ArrayLists don't hold information regarding the position and limit, pass that information
                # into the java utility
                if isinstance(data._db_values, autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList):
                    self._db_values = data._db_values # no need to change the underlying arraylist, it is just iterated on based on the position
                    # 4. seed the new java utility with the old java utility
                    self._j_util = self._get_j_util_generic_from_prev(data._j_util, self._db_time_ticks, self._db_values,
                                                              self._vector_len, position, position + length)
                else:
                    self._db_values = data._db_values.slice()
                    self._db_values.position(position)
                    self._db_values.limit(position + length)
                    # 4. seed the new java utility with the old java utility
                    self._j_util = self._get_j_util_from_prev(data._j_util, self._db_time_ticks, self._db_values, self._vector_len)

            self._min_iat = data._min_iat
            self._max_iat = data._max_iat

        # if we have values, set the min and max time-ticks
        if len(self._values) != 0:
            self._max_time_tick = self._time_ticks[len(self._time_ticks) - 1]
            self._min_time_tick = self._time_ticks[0]
        # if we do not have values, set the min and max time-ticks to default system max/min
        else:
            self._max_time_tick = -sys.maxsize - 1
            self._min_time_tick = sys.maxsize

        self._trs = trs

    def _calculate_iat(self, time_ticks):
        """Calculate the min and max inter-arrival-times given the list of time-ticks

        Parameters
        ----------
        time_ticks : list or np.ndarray
            the list of time-ticks
        """
        self._min_iat = sys.maxsize
        self._max_iat = -sys.maxsize + 1

        for i in range(len(time_ticks) - 1):
            cur_iat = time_ticks.iat[i + 1] - time_ticks.iat[i]
            if cur_iat < self._min_iat:
                self._min_iat = cur_iat
            if cur_iat > self._max_iat:
                self._max_iat = cur_iat

    def _get_j_util_from_prev(self, prev_j_util, db_time_ticks, db_values, vector_len):
        """get the new java utility from the previous java utility backed by a DirectByteBuffer

        Parameters
        ----------
        prev_j_util : PythonObservationCollectionUtils
            the previous PythonObservationCollection java utility
        db_time_ticks : DirectByteBuffer
            time-ticks in a DirectByteBuffer
        db_values : DirectByteBuffer
            values in a DirectByteBuffer
        vector_len : int
            the vector length if one exists

        Returns
        -------
        PythonObservationCollectionUtils
            a new java utility based on the old utility

        """
        if vector_len >= 1:
            return type(prev_j_util)(db_time_ticks, db_values, vector_len)
        else:
            return type(prev_j_util)(db_time_ticks, db_values)

    def _get_j_util_generic_from_prev(self, prev_j_util, db_time_ticks, db_values, vector_len, position, limit):
        """get the new java utility from the previous java utility backed by an ArrayList

        Parameters
        ----------
        prev_j_util : PythonObservationCollectionUtils
            the previous PythonObservationCollection java utility
        db_time_ticks : DirectByteBuffer
            time-ticks in a DirectByteBuffer
        db_values : ArrayList
            values in an ArrayList
        vector_len : int
            the vector length if one exists
        position : int
            the pointer to the start of the arraylist for this view
        limit : int
            the pointer to the end of the arraylist for this view

        Returns
        -------
        PythonObservationCollectionUtils
            a new java utility based on the old utility
        """
        if vector_len >= 1:
            return type(prev_j_util)(db_time_ticks, db_values, vector_len, position, limit)
        else:
            return type(prev_j_util)(db_time_ticks, db_values, position, limit)

    def _get_db_j_utils(self, pkgs, values):
        """For a collection of values, determine the underlying storage (DirectByteBuffer/ArrayList), java utility,
        underlying values (if flattened), and vector length

        Parameters
        ----------
        pkgs : java package
            pointer to the package the holds all java/python utilities in Java
        values : np.ndarray or pd.Series
            the underlying values

        Returns
        -------
        tuple
            the underlying storage (DirectByteBuffer/ArrayList), java utility, underlying values (if flattened),
            and vector length
        """

        # handling a special case where pandas dataframe contains a column containing numpy arrays
        if str(values.dtype) == 'object' and (isinstance(values, pd.Series) and isinstance(values.iat[0], np.ndarray)):
            values = np.asarray(values.tolist(), dtype=values.iat[0].dtype)

        # if the shape is greater than 1, the underlying data is stored in vectors
        if len(values.shape) > 1:

            # get the vector length
            vector_len = np.prod(np.array(values.shape[1:]))

            # create a mapping from the data type to a backend storage, utility, and corresponding number of bytes
            map_type = {
                'int8': [lambda x: x, pkgs.ByteVectorPythonObservationCollectionUtils, 1],
                'int16': [lambda x: x.asShortBuffer(), pkgs.ShortVectorPythonObservationCollectionUtils, 2],
                'int32': [lambda x: x.asIntBuffer(), pkgs.IntVectorPythonObservationCollectionUtils, 4],
                'int64': [lambda x: x.asLongBuffer(), pkgs.LongVectorPythonObservationCollectionUtils, 8],
                'float32': [lambda x: x.asFloatBuffer(), pkgs.FloatVectorPythonObservationCollectionUtils, 4],
                'float64': [lambda x: x.asDoubleBuffer(), pkgs.DoubleVectorPythonObservationCollectionUtils, 8]
            }

            # if the dtype is not a standard numpy type
            # store the values in an ArrayList
            # create a generic java utility
            dtype_name = values.dtype.name
            if dtype_name not in map_type:
                db_values = autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList(values.flatten().tolist())
                j_util = pkgs.GenericVectorPythonObservationCollectionUtils(self._db_time_ticks, db_values, vector_len)

                # flatten the data as it must be a single collection
                ret_values = values.flatten()

            # if the dtype is a standard numpy type
            # store the values in a DirectByteBuffer
            # create a specific java utility based on the numpy type
            else:
                value_bytes = bytearray(map_type[dtype_name][2] * values.size)
                jb_values = jpype.nio.convertToDirectBuffer(value_bytes)
                # set the ByteOrder to little endian as that is the default for pandas/numpy
                jb_values.order(autoai_ts_libs.deps.tspy.ts_context.packages.java.nio.ByteOrder.LITTLE_ENDIAN)
                db_values = map_type[dtype_name][0](jb_values)
                j_util = map_type[dtype_name][1](self._db_time_ticks, db_values, vector_len)

                # flatten the data as it must be a single collection
                ret_values = values.flatten()

        else:
            vector_len = 0

            # create a mapping from the data type to a backend storage, utility, and corresponding number of bytes
            map_type = {
                'int8': [lambda x: x, pkgs.BytePythonObservationCollectionUtils, 1],
                'int16': [lambda x: x.asShortBuffer(), pkgs.ShortPythonObservationCollectionUtils, 2],
                'int32': [lambda x: x.asIntBuffer(), pkgs.IntPythonObservationCollectionUtils, 4],
                'int64': [lambda x: x.asLongBuffer(), pkgs.LongPythonObservationCollectionUtils, 8],
                'float32': [lambda x: x.asFloatBuffer(), pkgs.FloatPythonObservationCollectionUtils, 4],
                'float64': [lambda x: x.asDoubleBuffer(), pkgs.DoublePythonObservationCollectionUtils, 8]
            }

            # if the dtype is not a standard numpy type
            # store the values in an ArrayList
            # create a generic java utility
            dtype_name = values.dtype.name
            if dtype_name not in map_type:
                db_values = autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList(values.tolist())
                j_util = pkgs.GenericPythonObservationCollectionUtils(self._db_time_ticks, db_values)
                ret_values = values

            # if the dtype is a standard numpy type
            # store the values in a DirectByteBuffer
            # create a specific java utility based on the numpy type
            else:
                value_bytes = bytearray(map_type[dtype_name][2] * len(values))
                jb_values = jpype.nio.convertToDirectBuffer(value_bytes)
                # set the ByteOrder to little endian as that is the default for pandas/numpy
                jb_values.order(autoai_ts_libs.deps.tspy.ts_context.packages.java.nio.ByteOrder.LITTLE_ENDIAN)
                db_values = map_type[dtype_name][0](jb_values)
                j_util = map_type[dtype_name][1](self._db_time_ticks, db_values)
                ret_values = values
        return db_values, j_util, ret_values, vector_len


    def _determine_db_values(self, values):
        """determine how the underlying values will be stored

        Parameters
        ----------
        values : dict or np.ndarray or pd.Series
            the underlying values
        """
        pkgs = autoai_ts_libs.deps.tspy.ts_context.packages.time_series.core.utils.python

        # if the values are in a dict, for each key, determine:
        # underlying storage (DirectByteBuffer/ArrayList), java utility, and vector length
        if isinstance(values, dict):
            self._db_values = {}
            self._values = {}
            self._vector_len = {}
            self._keys = autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList()
            j_utils = autoai_ts_libs.deps.tspy.ts_context.packages.java.util.HashMap()
            for k, v in values.items():
                this_values = values[k]
                # determine the underlying storage (DirectByteBuffer/ArrayList), java utility, underlying values
                # (if flattened), and vector length
                this_db_values, this_j_utils, this_values, vector_len = self._get_db_j_utils(pkgs, this_values)

                # if the values are stored in an ArrayList, no need to use numpy for the backend
                if isinstance(this_db_values, autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList):
                    self._values[k] = this_values
                # if the values are stored in a DirectByteBuffer, store the values in a numpy array
                # this will incur a single copy, then data is shared between Java/Python
                else:
                    self._values[k] = np.asarray(this_db_values)
                    self._values[k][:] = this_values
                self._db_values[k] = this_db_values
                self._vector_len[k] = vector_len
                j_utils.put(k, this_j_utils)
                self._keys.add(k)

            # set the java utility to a special Map-Like utility that contains multiple java utilities
            self._j_util = pkgs.MapPythonObservationCollectionUtils(
                self._db_time_ticks,
                j_utils
            )
        else:
            # determine the underlying storage (DirectByteBuffer/ArrayList), java utility, underlying values
            # (if flattened), and vector length
            self._db_values, self._j_util, values, vector_len = self._get_db_j_utils(pkgs, values)

            # if the values are stored in an ArrayList, no need to use numpy for the backend
            if isinstance(self._db_values, autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList):
                self._values = values
            # if the values are stored in a DirectByteBuffer, store the values in a numpy array
            # this will incur a single copy, then data is shared between Java/Python
            else:
                self._values = np.asarray(self._db_values)
                self._values[:] = values
            self._vector_len = vector_len

    def _j_observation(self, index):
        return self._j_util.getObservation(index)

    @JOverride
    def getVectorLength(self, *args):
        if len(args) == 0:
            return self._vector_len
        else:
            return self._vector_len[args[0]]

    @JOverride
    def contains(self, time_tick):
        return self.ceiling(time_tick).getTimeTick() == time_tick

    @JOverride
    def containsAll(self, time_ticks):
        for tt in time_ticks.items():
            if not self.contains(tt):
                return False
        return True

    @JOverride
    def iterator(self):
        return self._j_util.iterator()

    @JOverride
    def forEach(self, action):
        return self._j_util.forEach(action)

    @JOverride
    def parallelStream(self):
        return self._j_util.parallelStream()

    @JOverride
    def spliterator(self):
        return self._j_util.spliterator()

    @JOverride
    def stream(self):
        return self._j_util.stream()

    @JOverride
    def toArray(self, *args):
        if len(args) == 0:
            return self._j_util.toArray()
        else:
            return self._j_util.toArray(args[0])

    @JOverride
    def ceiling(self, time_tick):
        if len(self._time_ticks) == 0:
            raise Exception("cannot get ceiling of empty collection")

        result = self._get_ceiling_index(time_tick)

        if result == -1:
            return None
        else:
            return self._j_observation(result)

    @JOverride
    def floor(self, time_tick):
        if len(self._time_ticks) == 0:
            raise Exception("cannot get first observation of empty collection")

        result = self._get_floor_index(time_tick)

        if result == -1:
            return None
        else:
            return self._j_observation(result)

    @JOverride
    def headSet(self, to_time_tick, to_inclusive):
        if len(self._time_ticks) == 0:
            return PythonObservationCollection((np.array([]),np.array([])))

        if to_inclusive:
            if self._max_time_tick <= to_time_tick:
                last_index = len(self._time_ticks)
            else:
                last_index = self._get_higher_index(to_time_tick)
        else:
            last_index = self._get_lower_index(to_time_tick) + 1

        if last_index == -1:
            return PythonObservationCollection((np.array([]),np.array([])))
        else:
            return PythonObservationCollection(self, indexes=slice(0, last_index))

    @JOverride
    def tailSet(self, from_time_tick, from_inclusive):
        if len(self._time_ticks) == 0:
            return PythonObservationCollection((np.array([]),np.array([])))

        if from_inclusive:
            if self._min_time_tick >= from_time_tick:
                first_index = 0
            else:
                first_index = self._get_lower_index(from_time_tick) + 1
        else:
            first_index = self._get_higher_index(from_time_tick)

        if first_index == -1:
            return PythonObservationCollection((np.array([]),np.array([])))
        else:
            return PythonObservationCollection(self, indexes=slice(first_index, len(self._time_ticks)))

    @JOverride
    def descendingIterator(self):
        return self._j_util.descendingIterator()

    @JOverride
    def subSet(self, from_time_tick, from_inclusive, to_time_tick, to_inclusive):
        if len(self._time_ticks) == 0:
            return PythonObservationCollection((np.array([]), np.array([])))

        if from_inclusive:
            if self._min_time_tick >= from_time_tick:
                first_index = 0
            else:
                first_index = self._get_lower_index(from_time_tick) + 1
        else:
            first_index = self._get_higher_index(from_time_tick)

        if first_index == -1:
            return PythonObservationCollection((np.array([]), np.array([])))

        if to_inclusive:
            if self._max_time_tick <= to_time_tick:
                last_index = len(self._time_ticks)
            else:
                last_index = self._get_higher_index(to_time_tick)
        else:
            last_index = self._get_lower_index(to_time_tick) + 1

        if last_index == -1:
            return PythonObservationCollection((np.array([]), np.array([])))

        return PythonObservationCollection(self, indexes=slice(first_index, last_index))

    @JOverride
    def first(self):
        if len(self._time_ticks) == 0:
            raise Exception()

        return self._j_observation(0)

    @JOverride
    def last(self):
        if len(self._time_ticks) == 0:
            raise Exception()

        return self._j_observation(len(self._time_ticks) - 1)

    @JOverride
    def higher(self, time_tick):
        if len(self._time_ticks):
            raise Exception("cannot get higher of empty collection")

        result = self._get_higher_index(time_tick)

        if result == -1:
            return None
        else:
            return self._j_observation(result)

    @JOverride
    def lower(self, time_tick):
        if len(self._time_ticks):
            raise Exception("cannot get lower of empty collection")

        result = self._get_lower_index(time_tick)

        if result == -1:
            return None
        else:
            return self._j_observation(result)

    def toTimeSeriesWithoutTRS(self):
            return autoai_ts_libs.deps.tspy.ts_context.packages.time_series.core.timeseries.TimeSeries.fromObservations(self, False)

    def toTimeSeriesWithTRS(self, trs):
        if trs is None:
            return autoai_ts_libs.deps.tspy.ts_context.packages.time_series.core.timeseries.TimeSeries.fromObservations(self, False, trs)
        else:
            return autoai_ts_libs.deps.tspy.ts_context.packages.time_series.core.timeseries.TimeSeries.fromObservations(self, False, trs._j_trs)

    @JOverride
    def toTimeSeries(self, *args):
        if len(args) == 0 or self._trs is None:
            return self.toTimeSeriesWithoutTRS()
        else:
            return self.toTimeSeriesWithTRS(args[0])

    @JOverride
    def toCollection(self):
        return self._j_util.toCollection()

    @JOverride
    def toList(self):
        return self._j_util.toList()

    @JOverride
    def size(self):
        return len(self._time_ticks)

    @JOverride
    def isEmpty(self):
        return len(self._time_ticks) == 0

    @JOverride
    def getTRS(self):
        if self._trs is None:
            return None
        else:
            return self._trs._j_trs

    @JOverride
    def isPythonBacked(self):
        return True

    @JOverride
    def isDirectBuffer(self, *args):
        if len(args) == 0:
            return not isinstance(self._db_values, autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList)
        else:
            return not isinstance(self._db_values[args[0]], autoai_ts_libs.deps.tspy.ts_context.packages.java.util.ArrayList)

    @JOverride
    def bufferIsDict(self):
        return isinstance(self._db_values, dict)

    @JOverride
    def getValueBuffer(self, *args):
        if len(args) == 0:
            return self._db_values
        else:
            return self._db_values[args[0]]

    @JOverride
    def getValueList(self, *args):
        if len(args) == 0:
            return self._db_values
        else:
            return self._db_values[args[0]]

    @JOverride
    def getTimeTickBuffer(self):
        return self._db_time_ticks

    @JOverride
    def getKeys(self):
        return self._keys

    @JOverride
    def getPythonUtil(self):
        return self._j_util

    @JOverride
    def toString(self):
        if self._trs is None:
            return self._j_util.toString(None)
        else:
            return self._j_util.toString(self._trs._j_trs)

    def __str__(self):
        return str(self.toString())

    # def _value_to_str(self, i):
    #     if isinstance(self._values, dict):
    #         res = {}
    #         for k in self._keys:
    #             res[k] = self._values[k][i]
    #         return str(res)
    #     else:
    #         if self._vector_len > 1:
    #             return str(self._values[i:i+self._vector_len])
    #         else:
    #             return str(self._values[i])
    #
    # def __str__(self):
    #     return str(["Observation(" + str(self._time_ticks[i]) + ", " + self._value_to_str(i) + ")" for i in range(len(self._time_ticks))])

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

    def _get_higher_index(self, target):
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
        r = min(r + 1, len(self._time_ticks) - 1)

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

    def _get_lower_index(self, target):
        if len(self._time_ticks) == 0:
            return -1

        first = self._min_time_tick
        if target <= first:
            return -1

        last = self._max_time_tick
        if target > last:
            return len(self._time_ticks) - 1

        offset = target - first
        l = self._get_min_index(offset)
        r = self._get_max_index(offset)

        l = max(l - 1, 0)
        r = min(r, len(self._time_ticks) - 1)
        result = -1

        while l <= r:
            m = int((l + r) / 2)
            if self._time_ticks[m] < target:
                result = m
                l = m + 1
            else:
                r = m - 1
        return result

    def _get_ceiling_index(self, target):
        if len(self._time_ticks) == 0:
            return -1

        first = self._min_time_tick
        if target < first:
            return 0

        last = self._max_time_tick
        if target > last:
            return -1

        offset = target - first
        l = self._get_min_index(offset)
        r = self._get_max_index(offset)

        l = max(l, 0)
        r = min(r, len(self._time_ticks) - 1)

        result = -1
        while l <= r:
            m = int((l + r) / 2)
            if self._time_ticks[m] == target:

                while True:
                    result = m
                    m += 1
                    if m >= len(self._time_ticks) or self._time_ticks[m] != target:
                        break

            elif self._time_ticks[m] < target:
                l = m + 1

            else:
                result = m
                r = m - 1

        return result

    def _get_floor_index(self, target):
        if len(self._time_ticks) == 0:
            return -1

        first = self._min_time_tick
        if target < first:
            return -1

        last = self._max_time_tick
        if target > last:
            return len(self._time_ticks) - 1

        offset = target - first
        l = self._get_min_index(offset)
        r = self._get_max_index(offset)

        l = max(l, 0)
        r = min(r, len(self._time_ticks) - 1)

        result = -1
        while l <= r:
            m = int((l + r) / 2)
            if self._time_ticks[m] == target:

                while True:
                    result = m
                    m -= 1
                    if m >= 0 and self._time_ticks[m] == target:
                        break

            elif self._time_ticks[m] > target:
                r = m - 1
            else:
                result = m
                l = m + 1
        return result
