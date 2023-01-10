import datetime

import numpy as np
import pandas as pd

from autoai_ts_libs.deps.tspy.data_structures import TRS
from autoai_ts_libs.deps.tspy.data_structures.cross_language.Converters import Converters
from autoai_ts_libs.deps.tspy.data_structures.time_series.TimeSeries import TimeSeries


class JPypeConverters(Converters):
    def __init__(self, java_bridge):
        super().__init__(java_bridge)

    def bound_ts_to_df(self, bound_ts, array_index_to_col=False):
        import pandas as pd

        tt_array, value_result = self.bound_ts_to_numpy(bound_ts)

        if isinstance(value_result, dict):
            tt_col = self._determine_next_unused_col_name(
                value_result.keys(), "time_tick"
            )
            value_result[tt_col] = tt_array

            res = {}
            for k, v in value_result.items():
                # if we have a java string or a python string, we should ravel
                first = v[0]
                if isinstance(
                    first, str
                ) or self._java_bridge._tsc.java_bridge.is_instance_of_java_class(
                    first, "java.lang.String"
                ):
                    v = v.ravel()

                if array_index_to_col:
                    num_dim = v.ndim
                    if num_dim > 1:
                        v_transpose = v.transpose()
                        for i in range(num_dim):
                            val_col = self._determine_next_unused_col_name(
                                value_result.keys(), str(k) + "." + str(i)
                            )
                            res[val_col] = v_transpose[i]
                    else:
                        res[str(k)] = v
                else:
                    num_dim = v.ndim
                    if num_dim > 1:
                        res[str(k)] = v.tolist()
                    else:
                        res[str(k)] = v
            df = pd.DataFrame(
                {
                    **{
                        "time_tick": tt_array,
                    },
                    **res,
                }
            )
        else:

            # if we have a java string or a python string, we should ravel
            first = value_result[0]
            if isinstance(
                first, str
            ) or self._java_bridge._tsc.java_bridge.is_instance_of_java_class(
                first, "java.lang.String"
            ):
                value_result = value_result.ravel()

            if array_index_to_col:
                res = {}

                num_dim = value_result.ndim
                if num_dim > 1:  # check for non-string
                    value_result_transpose = value_result.transpose()
                    for i in range(num_dim):
                        res["value." + str(i)] = value_result_transpose[i]
                else:
                    res["value"] = value_result
                df = pd.DataFrame(
                    {
                        **{
                            "time_tick": tt_array,
                        },
                        **res,
                    }
                )
            else:
                df = pd.DataFrame(
                    {
                        "time_tick": tt_array,
                        "value": value_result.tolist()
                        if value_result.ndim > 1
                        else value_result,
                    }
                )
        return df

    def _determine_next_unused_col_name(self, columns, col_name):
        if col_name not in columns:
            return col_name
        else:
            i = 0
            while True:
                next_col_name = col_name + "." + str(i)
                if next_col_name not in columns:
                    return next_col_name
                else:
                    i = i + 1

    def bound_ts_to_numpy(self, bound_ts):
        if bound_ts._j_observations.isPythonBacked():
            return self._to_numpy_python(bound_ts)
        else:
            return self._to_numpy_java(bound_ts)

    def _to_numpy_values(self, bound_ts, k=None):
        import numpy as np

        # todo redundant code, we can fix this later
        if k is None:
            # if our buffer is direct, we can access it directly with no overhead
            if bound_ts._j_observations.isDirectBuffer():
                np_values = np.asarray(bound_ts._j_observations.getValueBuffer())
            else:
                if bound_ts._tsc.java_bridge.is_instance_of_java_class(
                    bound_ts._j_observations.getValueList()[0], "java.lang.String"
                ):
                    np_values = np.asarray(
                        [
                            str(bound_ts._j_observations.getValueList().get(i))
                            for i in range(
                                bound_ts._j_observations.getValueList().size()
                            )
                        ],
                        dtype="object",
                    )
                else:
                    np_values = np.asarray(
                        list(bound_ts._j_observations.getValueList()), dtype="object"
                    )

            vector_len = bound_ts._j_observations.getVectorLength()
            # if we have vectors, we need to reshape the array given the size of the vector
            if vector_len != 0:
                np_values = np_values.reshape([bound_ts.__len__(), vector_len])
        else:
            # if our buffer is direct, we can access it directly with no overhead
            if bound_ts._j_observations.isDirectBuffer(k):
                np_values = np.asarray(bound_ts._j_observations.getValueBuffer(k))
            else:
                if bound_ts._tsc.java_bridge.is_instance_of_java_class(
                    bound_ts._j_observations.getValueList(k)[0], "java.lang.String"
                ):
                    np_values = np.asarray(
                        [
                            str(bound_ts._j_observations.getValueList(k).get(i))
                            for i in range(
                                bound_ts._j_observations.getValueList(k).size()
                            )
                        ],
                        dtype="object",
                    )
                else:
                    np_values = np.asarray(
                        list(bound_ts._j_observations.getValueList(k)), dtype="object"
                    )

            vector_len = bound_ts._j_observations.getVectorLength(k)
            # if we have vectors, we need to reshape the array given the size of the vector
            if vector_len != 0:
                np_values = np_values.reshape([bound_ts.__len__(), vector_len])
        return np_values

    def _to_numpy_python(self, bound_ts):
        import numpy as np

        np_time_ticks = np.asarray(bound_ts._j_observations.getTimeTickBuffer())
        # if our underlying numpy buffer is actually a dict of buffers, we must get each buffer and return in a 2d numpy
        #  array
        if bound_ts._j_observations.bufferIsDict():
            np_values = {}
            keys = bound_ts._j_observations.getKeys()
            for k in keys:
                # if our buffer is direct, we can access it directly with no overhead
                np_values[k] = self._to_numpy_values(bound_ts, k)
        else:
            np_values = self._to_numpy_values(bound_ts)

        return np_time_ticks, np_values

    def _to_numpy_java(self, bound_ts):
        import numpy as np

        # todo this method will most likely be the slowest form of retrieval for numpy/dataframes.
        #  Look into optimizations for this
        #  Reduce times backed by java is used
        raw_iter = bound_ts._raw_iter()

        if bound_ts.__len__() == 0:
            return np.array([]), np.array([])

        time_ticks = []

        tt, val = next(raw_iter)
        time_ticks.append(tt)

        if isinstance(
            val, dict
        ) or self._java_bridge._tsc.java_bridge.is_instance_of_java_class(
            val, "java.util.HashMap"
        ):
            keys = val.keys()
            values = {k: [] for k in keys}
        else:
            values = []

        while True:
            try:
                if isinstance(
                    val, dict
                ) or bound_ts._tsc.java_bridge.is_instance_of_java_class(
                    val, "java.util.HashMap"
                ):
                    for k, v in val.items():
                        # explicitly check for Java Strings here as they will be treated by numpy as a character array
                        #  rather than an object
                        if bound_ts._tsc.java_bridge.is_instance_of_java_class(
                            v, "java.lang.String"
                        ):
                            values[k].append(str(v))
                        else:
                            values[k].append(v)
                elif isinstance(
                    val, list
                ) or bound_ts._tsc.java_bridge.is_instance_of_java_class(
                    val, "java.util.ArrayList"
                ):
                    res = []
                    for v in val:
                        # explicitly check for Java Strings here as they will be treated by numpy as a character array
                        #  rather than an object
                        if bound_ts._tsc.java_bridge.is_instance_of_java_class(
                            v, "java.lang.String"
                        ):
                            res.append(str(v))
                        else:
                            res.append(v)
                    values.append(res)
                else:
                    if bound_ts._tsc.java_bridge.is_instance_of_java_class(
                        val, "java.lang.String"
                    ):
                        values.append(str(val))
                    else:
                        values.append(val)

                tt, val = next(raw_iter)
                time_ticks.append(tt)
            except StopIteration:
                break

        if isinstance(values, dict):
            values = {k: np.array(v) for k, v in values.items()}
        else:
            values = np.array(values)
        return np.array(time_ticks), values

    def from_numpy_to_ts(self, np_array, granularity=None, start_time=None):
        pkgs = self._java_bridge.package_root.time_series.core.timeseries
        from autoai_ts_libs.deps.tspy.data_structures.cross_language.PythonObservationCollection import (
            PythonObservationCollection,
        )

        tt_nparray = np.arange(0, len(np_array))
        value_nparray = np_array
        iat = (1, 1)

        if granularity is None and start_time is None:
            observations = pkgs.BoundTimeSeries(
                PythonObservationCollection((tt_nparray, value_nparray), iat=iat)
            )
            return TimeSeries(
                self._java_bridge._tsc,
                self._java_bridge._tsc.packages.time_series.core.timeseries.TimeSeries.fromObservations(
                    observations, False, None
                ),
            )
        else:
            if granularity is None:
                granularity = datetime.timedelta(milliseconds=1)
            if start_time is None:
                start_time = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
            trs = TRS(self._java_bridge._tsc, granularity, start_time)

            # todo add trs to PythonObservationCollection
            observations = pkgs.BoundTimeSeries(
                PythonObservationCollection(
                    (tt_nparray, value_nparray), iat=iat, trs=trs
                )
            )
            return TimeSeries(
                self._java_bridge._tsc,
                self._java_bridge._tsc.packages.time_series.core.timeseries.TimeSeries.fromObservations(
                    observations, False, trs._j_trs
                ),
                trs,
            )

    def from_numpy_to_mts(self, np_array, granularity=None, start_time=None):
        import autoai_ts_libs.deps.tspy

        ts_dict = {
            i: autoai_ts_libs.deps.tspy.time_series(np_array[i], granularity, start_time)
            for i in range(len(np_array))
        }
        from autoai_ts_libs.deps.tspy.multi_time_series import _dict

        return _dict(self._java_bridge._tsc, ts_dict, granularity, start_time)

    def from_df_to_ts(
        self, df, ts_column=None, value_column=None, granularity=None, start_time=None
    ):
        import numpy as np
        import datetime

        convert_dt = False
        for c in df.columns:
            dtype_name = df[c].dtype
            if dtype_name == "datetime64[ns]":
                if c == ts_column:
                    convert_dt = True
                df[c] = df[c].apply(lambda x: int(pd.to_datetime(x).value) / 10 ** 6)

        if ts_column is None:
            tt = np.arange(len(df))
            iat = (1, 1)
        else:
            df = df.sort_values(by=[ts_column])
            tt = df[ts_column]
            iat = None

        if granularity is None and start_time is None and not convert_dt:
            trs = None
            j_trs = None
        else:
            if granularity is None or convert_dt:
                granularity = datetime.timedelta(milliseconds=1)
            if start_time is None or convert_dt:
                start_time = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
            trs = TRS(self._java_bridge._tsc, granularity, start_time)
            j_trs = trs._j_trs

        if isinstance(value_column, list):
            d = {col: df[col] for col in value_column}
        elif value_column is None:
            d = {col: df[col] for col in df.keys() if col != ts_column}
        else:
            d = df[value_column]

        from autoai_ts_libs.deps.tspy.data_structures.cross_language.PythonObservationCollection import (
            PythonObservationCollection,
        )

        observations = PythonObservationCollection((tt, d), iat=iat)
        return TimeSeries(
            self._java_bridge._tsc,
            self._java_bridge.package_root.time_series.core.timeseries.TimeSeries.fromObservations(
                observations, False, j_trs
            ),
            trs,
        )

    def from_df_observations_to_mts(
        self,
        df,
        key_column,
        ts_column=None,
        value_column=None,
        granularity=None,
        start_time=None,
    ):
        import autoai_ts_libs.deps.tspy

        grouped_df = df.groupby([key_column])
        if value_column is None:
            value_column = list(df.columns)
            value_column.remove(key_column)

            if ts_column is not None:
                value_column.remove(ts_column)

        ts_dict = {
            k: autoai_ts_libs.deps.tspy.time_series(k_df, ts_column, value_column, granularity, start_time)
            for k, k_df in grouped_df
        }
        from autoai_ts_libs.deps.tspy.multi_time_series import _dict

        return _dict(self._java_bridge._tsc, ts_dict, granularity, start_time)

    def from_df_instants_to_mts(
        self, df, key_columns=None, ts_column=None, granularity=None, start_time=None
    ):
        import autoai_ts_libs.deps.tspy

        keys = df.keys() if key_columns is None else key_columns

        # todo this is not technically the most efficient way, since we will sort each time instead of once on the df
        #  but it is a simple solution, will fix later
        ts_dict = {
            k: autoai_ts_libs.deps.tspy.time_series(df, ts_column, k, granularity, start_time)
            for k in keys
            if k != ts_column
        }
        from autoai_ts_libs.deps.tspy.multi_time_series import _dict

        return _dict(self._java_bridge._tsc, ts_dict, granularity, start_time)

    def bound_mts_to_numpy(self, bound_mts):
        return {k: v.to_numpy() for k, v in bound_mts.items()}

    def bound_mts_to_df(
        self, bound_mts, format="observations", array_index_to_col=False, key_col=None
    ):
        if format == "observations":
            return self._to_df_observations(bound_mts, array_index_to_col, key_col)
        else:
            return self._to_df_instants(bound_mts, array_index_to_col)

    def _to_df_observations(self, bound_mts, array_index_to_col=False, key_col=None):
        df_list = []
        key = "key" if key_col is None else key_col
        for k, v in bound_mts.items():
            df = v.to_df(array_index_to_col)
            key = self._determine_next_unused_col_name(df.columns, key)
            df[key] = str(k)
            df_list.append(df)
        import pandas as pd

        res = pd.concat(df_list)
        res.sort_values(by=["time_tick"], inplace=True)
        res.reset_index(inplace=True, drop=True)
        return res

    def _to_df_instants(self, bound_mts, array_index_to_col=False):
        df_dict = {}
        for k, v in bound_mts.items():
            df = v.to_df(array_index_to_col)

            for k_df in df.keys():
                if "time_tick" not in k_df:
                    to_add_key = str(k) + "." + k_df
                    cur = df[k_df]
                    cur_first = cur.iat[0]
                    # if the current is an instance of a string, we must ravel (its possible it comes from java, so
                    # check for both
                    if isinstance(
                        cur_first, str
                    ) or self._java_bridge._tsc.java_bridge.is_instance_of_java_class(
                        cur_first, "java.lang.String"
                    ):
                        cur = cur.astype(">U1").ravel()
                    df_dict[str(to_add_key)] = cur
                else:
                    df_dict[str(k_df)] = df[k_df]
        import pandas as pd

        return pd.DataFrame(df_dict)
