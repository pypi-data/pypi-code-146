#  /************** Begin Copyright - Do not add comments here **************
#   * Licensed Materials - Property of IBM
#   *
#   *   OCO Source Materials
#   *
#   *   (C) Copyright IBM Corp. 2020, All Rights Reserved
#   *
#   * The source code for this program is not published or other-
#   * wise divested of its trade secrets, irrespective of what has
#   * been deposited with the U.S. Copyright Office.
#   ***************************** End Copyright ****************************/


class Observation:
    """
    Basic storage unit for a single time-series observation

    .. todo::
        Ask Josh to provide other supported types for `time_tick`

    Attributes
    ----------
    time_tick : int
        the time-tick associated with this observation
    value : any
        the value associated with this observation

    Examples
    --------
    create a simple observation

    >>> import autoai_ts_libs.deps.tspy
    >>> obs = autoai_ts_libs.deps.tspy.observation(1,1)
    >>> obs
    TimeStamp: 1     Value: 1
    """

    def __init__(self, tsc, time_tick=-1, value=None, contains_java=True):
        self._tsc = tsc
        self._time_tick = time_tick
        self._value = value
        self._contains_java = contains_java
        if self._contains_java or not self._tsc.java_bridge_is_default:
            self._insert_java()

    def __call__(self, timestamp, value):
        return Observation(self._tsc, timestamp, value)

    @property
    def time_tick(self):
        """
        Returns
        -------
        int
            the time-tick associated with this observation

        .. todo::
            Ask Josh ...

        """
        return self._time_tick

    @property
    def value(self):
        """
        Returns
        -------
        any
            the value associated with this observation
        """
        return self._value

    def _insert_java(self):
        if type(self._value) is list:
            j_value = self._tsc.java_bridge.convert_to_java_list(self._value)
        elif type(self._value) is tuple:
            j_value = self._tsc.packages.time_series.core.utils.Pair(
                self._value[0], self._value[1]
            )
        elif type(self._value) is dict:
            j_value = self._tsc.java_bridge.convert_to_java_map(self._value)
        else:
            j_value = self._tsc.java_bridge.cast_to_j_if_necessary(self._value)
        try:
            self._j_observation = (
                self._tsc.packages.time_series.core.observation.Observation(
                    self._time_tick, j_value
                )
            )
            self._contains_java = True
        except Exception:
            msg = "Not supportted type for `value`"
            raise TypeError(msg) from None

    def _to_human_readable_str(self, j_trs):
        return self._j_observation.toString(j_trs)

    def __str__(self):
        if self._contains_java:
            return str(self._j_observation.toString())
        else:
            return "Observation(" + str(self.time_tick) + ", " + str(self.value) + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.time_tick is other.time_tick and self.value is other.value
