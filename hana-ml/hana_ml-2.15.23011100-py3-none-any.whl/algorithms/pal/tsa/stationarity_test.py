"""
This module contains Python wrapper for PAL stationarity test algorithm.

The following function is available:

    * :func:`stationarity_test`
"""
#pylint:disable=line-too-long, attribute-defined-outside-init, unused-variable, too-many-arguments
#pylint:disable=invalid-name, too-few-public-methods, too-many-statements, too-many-locals
#pylint:disable=bad-option-value, too-many-branches, consider-using-f-string, consider-using-f-string
import logging
import uuid
import warnings
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from hana_ml.algorithms.pal.tsa.arima import _convert_index_from_timestamp_to_int, _is_index_int
from hana_ml.algorithms.pal.pal_base import (
    ParameterTable,
    arg,
    try_drop,
    require_pal_usable,
    call_pal_auto_with_hint
)
logger = logging.getLogger(__name__)

def stationarity_test(data, key=None, endog=None, method=None,
                      mode=None, lag=None, probability=None):
    r"""
    Stationarity means that a time series has a constant mean and constant variance over time.
    For many time series models, the input data has to be stationary for reasonable analysis.

    Parameters
    ----------

    data : DataFrame
        Input data which contains at least two columns, one is ID column, the other is raw data.

    key : str, optional
        The ID (Time stamp) column. ID does not need to be in order, but must be unique and equal sampling.
        The supported data type is INTEGER.

        Defaults to the first column of data if the index column of data is not provided.
        Otherwise, defaults to the index column of data.

    endog : str, optional
        The column of series to be tested.

        Defaults to the first non-key column.

    method : str, optional
        Statistic test that used to determine stationarity. The options are "kpss" and "adf".

        Defaults "kpss".

    mode : str, optional
        Type of stationarity to determine. The options are "level", "trend" and "no".
        Note that option "no" is not applicable to "kpss".

        Defaults to "level".

    lag : int, optional
        The lag order to calculate the test statistic.

        Default value is "kpss": int(12*(data_length / 100)^0.25" ) and "adf": int(4*(data_length / 100)^(2/9)).

    probability : float, optional
        The confidence level for confirming stationarity.

        Defaults to 0.9.

    Returns
    -------
    DataFrame
        Statistics for time series, structured as follows:
            - STATS_NAME: Name of the statistics of the series.
            - STATS_VALUE: Indicates the value of corresponding stats.

    Examples
    --------

    Time series data df:

    >>> df.head(3).collect()
           TIME_STAMP  SERIES
    0      0           0.0
    1      1           1.00
    2      2           1586.00

    Perform stationarity_test():

    >>> stats = stationarity_test(df, endog='SERIES', key='TIME_STAMP',
                                  method='kpss', mode='trend', lag=5, probability=0.95)

    Outputs:

    >>> stats.head(3).collect()
         STATS_NAME     STATS_VALUE
    0    stationary     0
    1    kpss_stat      0.26801
    2    p-value        0.01
    """
    conn = data.connection_context
    require_pal_usable(conn)

    method_map = {'kpss':0, 'adf':1}
    mode_map = {'level':0, 'trend':1, 'no':2}

    method = arg('method', method, method_map)
    mode = arg('mode', mode, mode_map)
    lag = arg('lag', lag, int)
    key = arg('key', key, str)
    endog = arg('endog', endog, str)

    unique_id = str(uuid.uuid1()).replace('-', '_').upper()
    stats_tbl = '#PAL_STATIONARITY_TEST_STATS_TBL_{}_{}'.format(id, unique_id)

    cols = data.columns
    if len(cols) < 2:
        msg = ("Input data should contain at least 2 columns: " +
               "one for ID, another for raw data.")
        logger.error(msg)
        raise ValueError(msg)

    if key is not None and key not in cols:
        msg = ('Please select key from name of columns!')
        logger.error(msg)
        raise ValueError(msg)

    index = data.index
    if index is not None:
        if key is None:
            if not isinstance(index, str):
                key = cols[0]
                warn_msg = "The index of data is not a single column and key is None, so the first column of data is used as key!"
                warnings.warn(message=warn_msg)
            else:
                key = index
        else:
            if key != index:
                warn_msg = "Discrepancy between the designated key column '{}' ".format(key) +\
                "and the designated index column '{}'.".format(index)
                warnings.warn(message=warn_msg)
    else:
        if key is None:
            key = cols[0]
    cols.remove(key)

    if endog is not None:
        if endog not in cols:
            msg = ('Please select endog from name of columns!')
            logger.error(msg)
            raise ValueError(msg)
    else:
        endog = cols[0]

    data_ = data[[key] + [endog]]

    # key column type check
    is_index_int = False
    is_index_int = _is_index_int(data, key)
    if not is_index_int:
        data_= _convert_index_from_timestamp_to_int(data_, key)

    param_rows = [('METHOD', method, None, None),
                  ('MODE', mode, None, None),
                  ('LAG', lag, None, None),
                  ('PROBABILITY', None, probability, None)]

    try:
        call_pal_auto_with_hint(conn,
                                None,
                                'PAL_STATIONARITY_TEST',
                                data_,
                                ParameterTable().with_data(param_rows),
                                stats_tbl)

    except dbapi.Error as db_err:
        logger.exception(str(db_err))
        try_drop(conn, stats_tbl)
        raise
    except pyodbc.Error as db_err:
        logger.exception(str(db_err.args[1]))
        try_drop(conn, stats_tbl)
        raise
    return conn.table(stats_tbl)
