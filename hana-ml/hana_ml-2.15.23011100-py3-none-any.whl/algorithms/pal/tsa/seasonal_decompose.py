"""
This module contains Python wrapper for PAL seasonality test algorithm.

The following function is available:

    * :func:`seasonal_decompose`
"""
#pylint:disable=line-too-long, too-many-locals, unused-argument
#pylint:disable=invalid-name, too-many-arguments, too-few-public-methods, too-many-statements
#pylint: disable=too-many-branches, c-extension-no-member
import logging
import uuid
import warnings


try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from hana_ml.algorithms.pal.tsa.arima import _convert_index_from_timestamp_to_int, _is_index_int
from hana_ml.dataframe import quotename
from hana_ml.algorithms.pal.pal_base import (
    ParameterTable,
    arg,
    try_drop,
    require_pal_usable,
    call_pal_auto_with_hint
)
logger = logging.getLogger(__name__)

def seasonal_decompose(data,
                       key=None,
                       endog=None,
                       alpha=None,
                       thread_ratio=None,
                       model=None,
                       decompose_type=None,
                       extrapolation=None,
                       smooth_width=None,
                       auxiliary_normalitytest=None,
                       periods=None):
    """
    seasonal_decompose function is to decompose a time series into three components: trend, seasonality and random noise.

    Parameters
    ----------
    data : DataFrame
        Input data. At least two columns, one is ID column, the other is raw data.

    key : str, optional
        The ID column.

        Defaults to the first column of data if the index column of data is not provided.
        Otherwise, defaults to the index column of data.

    endog : str, optional
        The column of series to be decomposed.

        Defaults to the first non-ID column.

    alpha : float, optional
        The criterion for the autocorrelation coefficient.
        The value range is (0, 1). A larger value indicates stricter requirement for seasonality.

        Defaults to 0.2.

    thread_ratio : float, optional
        Controls the proportion of available threads to use.
        The ratio of available threads.

            - 0: single thread.
            - 0~1: percentage.
            - Others: heuristically determined.

        Defaults to -1.

    decompose_type : {'additive', 'multiplicative', 'auto'}, optional
        Specifies decompose type.
          - 'additive': Additive decomposition model
          - 'multiplicative': Multiplicative decomposition model
          - 'auto': Decomposition model automatically determined from input data

        Defaults to 'auto'.

    extrapolation : bool, optional
       Specifies whether to extrapolate the endpoints.
       Set to True when there is an end-point issue.

       Defaults to False.

    smooth_width : int, optional
       Specifies the width of the moving average applied to non-seasonal data.
       0 indicates linear fitting to extract trends.
       Can not be larger than half of the data length.

       Defaults to 0.

    auxiliary_normalitytest : bool, optional
       Specifies whether to use normality test to identify model types.

       Defaults to False.

    periods : int, optional
       Length of the periods.
       When this parameter is specified between 2 and half of the series length, autocorrelation value is calculated for this number of periods and the result is compared to ``alpha`` parameter.

       If correlation value is equal to or higher than ``alpha``, decomposition is executed with the value of ``periods``. Otherwise, decomposition is executed with no seasonality. For other value of ``periods``, decomposition is also executed with no seasonality.

       Defaults to None.

    Returns
    -------

    DataFrame
        Statistics for time series, structured as follows:
            - STAT_NAME: includes type (additive or multiplicative), period (number of seasonality),
              acf (autocorrelation coefficient).
            - STAT_VALUE: value of stats above.

        Seasonal decomposition table, structured as follows:
            - ID : index/time stamp.
            - SEASONAL: seasonality component.
            - TREND: trend component.
            - RANDOM: white noise component.


    Examples
    --------

    Time series data df:

    >>> df.collect().head(3)
       TIME_STAMP   SERIES
    0           1     10.0
    1           2      7.0
    2           3     17.0

    Perform seasonal_decompose function:

    >>> stats, decompose = seasonal_decompose(data, endog='SERIES', alpha=0.2, thread_ratio=0.5)

    Outputs:

    >>> stats.collect()
        STAT_NAME       STAT_VALUE
    0        type   multiplicative
    1      period                4
    2         acf         0.501947

    >>> decompose.collect().head(3)
        ID    SEASONAL      TREND        RANDOM
    0    1    1.252660     10.125      0.788445
    1    2    0.349952     14.000      1.428769
    2    3    0.748851     16.875      1.345271

    """
    seasonal_decompose_map = {'additive': 1, 'multiplicity' : 2,
                              'multiplicative': 2,
                              'none' : None, 'auto': 0}
    conn = data.connection_context
    require_pal_usable(conn)
    alpha = arg('alpha', alpha, float)
    thread_ratio = arg('thread_ratio', thread_ratio, float)
    decompose_type = arg('decompose_type', decompose_type, seasonal_decompose_map)
    extrapolation = arg('extrapolation', extrapolation, bool)
    smooth_width = arg('smooth_width', smooth_width, int)
    auxiliary_normalitytest = arg('auxiliary_normalitytest', auxiliary_normalitytest, bool)
    periods = arg('periods', periods, int)

    key = arg('key', key, str)
    endog = arg('endog', endog, str)

    cols = data.columns
    if len(cols) < 2:
        msg = ("Input data should contain at least 2 columns: " +
               "one for ID, another for raw data.")
        logger.error(msg)
        raise ValueError(msg)

    if key is not None and key not in cols:
        msg = 'Please select key from name of columns!'
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
                warn_msg = f"Discrepancy between the designated key column '{key}' and the designated index column '{index}'"
                warnings.warn(message=warn_msg)
    else:
        if key is None:
            key = cols[0]
    cols.remove(key)

    if endog is not None:
        if endog not in cols:
            msg = 'Please select endog from name of columns!'
            logger.error(msg)
            raise ValueError(msg)
    else:
        endog = cols[0]

    data_ = data[[key] + [endog]]

    unique_id = str(uuid.uuid1()).replace('-', '_').upper()
    outputs = ['STATS', 'DECOMPOSE',]
    outputs = [f'#PAL_SEASONAL_DECOMPOSE_{name}_TBL_{unique_id}' for name in outputs]
    stats_tbl, decompose_tbl = outputs
    param_rows = [('ALPHA', None, alpha, None),
                  ('THREAD_RATIO', None, thread_ratio, None),
                  ('DECOMPOSE_TYPE', decompose_type, None, None),
                  ('EXTRAPOLATION', extrapolation, None, None),
                  ('SMOOTH_WIDTH', smooth_width, None, None),
                  ('AUXILIARY_NORMALITYTEST', auxiliary_normalitytest, None, None),
                  ('PERIODS', periods, None, None)]

    is_index_int = _is_index_int(data_, key)
    if not is_index_int:
        max_ = data.select(key).max()
        min_ = data.select(key).min()
        delta = (max_ - min_) / (data.count() - 1)
        timedelta = delta.total_seconds()
        data_ = _convert_index_from_timestamp_to_int(data_, key)
    try:
        call_pal_auto_with_hint(conn,
                                None,
                                'PAL_SEASONALITY_TEST',
                                data_,
                                ParameterTable().with_data(param_rows),
                                *outputs)

    except dbapi.Error as db_err:
        logger.exception(str(db_err))
        try_drop(conn, stats_tbl)
        try_drop(conn, decompose_tbl)
        raise
    except pyodbc.Error as db_err:
        logger.exception(str(db_err.args[1]))
        try_drop(conn, stats_tbl)
        try_drop(conn, decompose_tbl)
        raise
    decompose_df = conn.table(decompose_tbl)
    if not is_index_int:
        decompose_df = conn.sql(f"""
                                SELECT ADD_SECONDS('{min_}', ({quotename(decompose_df.columns[0])} - 1) * {timedelta}) AS {quotename(key)},
                                {quotename(decompose_df.columns[1])},
                                {quotename(decompose_df.columns[2])},
                                {quotename(decompose_df.columns[3])}
                                FROM ({decompose_df.select_statement})
                                """)
    return conn.table(stats_tbl), decompose_df
