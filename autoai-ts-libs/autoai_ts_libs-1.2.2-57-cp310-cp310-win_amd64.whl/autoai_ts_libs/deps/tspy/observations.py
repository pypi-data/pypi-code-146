"""
main entry-point for creation of :class:`~autoai_ts_libs.deps.tspy.data_structures.observations.ObservationCollection.ObservationCollection`
"""
from autoai_ts_libs.deps.tspy import _get_context
from autoai_ts_libs.deps.tspy._others import builder

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
from autoai_ts_libs.deps.tspy.data_structures import BoundTimeSeries
import autoai_ts_libs.deps.tspy.dtypes
import numpy as np
import sys

def _numpy_array(tsc, *args, **kwargs):
    # todo this is a pretty unsafe method but it gives the user an extremely fast way of creating a bound-time-series
    #  For instance a user may give time-ticks out of order, or give time-ticks with an incorrect period (should we
    #  safeguard against this or opt for performance and just document). Should we add a parameter to optionally sort?
    #  Keeping this as is with no safeguards and only documentation to opt for performance is also an OK route as we
    #  provide very safe ways for users to create BoundTimeSeries through the TSBuilder as well as TimeSeries through
    #  the time_series entry point.
    period = kwargs.get('period', 1)
    sort = kwargs.get('sort', False)

    if len(args) == 2:
        values = args[1]
        time_ticks = args[0]
    elif len(args) == 1:
        values = args[0]
        time_ticks = kwargs.get('time_ticks', np.arange(0, len(values) * period, period))
    else:
        values = kwargs['values']
        time_ticks = kwargs.get('time_ticks', np.arange(0, len(values)*period, period))

    if sort:
        inds = time_ticks.argsort()
        time_ticks[:] = time_ticks[inds]
        values[:] = values[inds]

    if ('time_ticks' in kwargs or len(args) == 2) and 'period' not in kwargs:
        min_iat = sys.maxsize
        max_iat = -sys.maxsize + 1

        for i in range(len(time_ticks) - 1):
            cur_iat = time_ticks[i + 1] - time_ticks[i]
            if cur_iat < min_iat:
                min_iat = cur_iat
            if cur_iat > max_iat:
                max_iat = cur_iat
        iat = (min_iat, max_iat)
    else:
        iat = (period, period)
    util = tsc.packages.time_series.core.timeseries
    from autoai_ts_libs.deps.tspy.data_structures.cross_language.PythonObservationCollection import PythonObservationCollection
    py_obs_coll = PythonObservationCollection((time_ticks, values), iat=iat)
    return BoundTimeSeries(tsc, util.BoundTimeSeries(py_obs_coll), py_obs_coll)

def _empty(tsc):
    """creates an empty observation-collection

    Returns
    -------
    :class:`~autoai_ts_libs.deps.tspy.data_structures.observations.BoundTimeSeries.BoundTimeSeries`
        a new observation-collection
    """
    return BoundTimeSeries(tsc)

def _of(*observations):
    """creates a collection of observations

    Parameters
    ----------
    observations : varargs
        a variable number of observations

    Returns
    -------
    :class:`~autoai_ts_libs.deps.tspy.data_structures.observations.BoundTimeSeries.BoundTimeSeries`
        a new observation-collection
    """
    ts_builder = builder()
    for obs in observations:
        ts_builder.add(obs)
    # todo not sure why this was added, need to ask tuan
      # if isinstance(obs, autoai_ts_libs.deps.tspy.dtypes.Observation):
      #   ts_builder.add(obs)
      # elif isinstance(obs, tuple):
      #   for ob in obs:
      #     ts_builder.add(ob)
    return ts_builder.result()

def observations(*args, **kwargs):
    """returns an :class:`.ObservationCollection`

    Parameters
    ----------
    observations : varargs
        either empty or a variable number of observations

    Returns
    -------
    :class:`~autoai_ts_libs.deps.tspy.data_structures.observations.BoundTimeSeries.BoundTimeSeries`
        a new observation-collection
    """
    tsc = _get_context()

    if 'values' in kwargs or isinstance(args[0], np.ndarray):
        return _numpy_array(tsc, *args, **kwargs)
    elif len(args) > 0:
        return _of(*args)
    else:
        return _empty(tsc)
