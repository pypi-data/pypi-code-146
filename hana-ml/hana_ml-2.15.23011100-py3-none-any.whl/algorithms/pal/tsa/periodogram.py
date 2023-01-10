"""
This module contains Python wrapper for PAL Periodogram.

The following function is available:

    * :func:`periodogram`
"""
#pylint:disable=line-too-long, attribute-defined-outside-init, unused-variable, too-many-arguments
#pylint:disable=invalid-name, too-few-public-methods, too-many-statements, too-many-locals
#pylint:disable=too-many-branches, c-extension-no-member
import logging
import uuid
import warnings
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from hana_ml.dataframe import quotename
from hana_ml.algorithms.pal.utility import check_pal_function_exist
from hana_ml.algorithms.pal.tsa.arima import _convert_index_from_timestamp_to_int, _is_index_int
from hana_ml.algorithms.pal.pal_base import (
    ParameterTable,
    arg,
    try_drop,
    require_pal_usable,
    call_pal_auto_with_hint
)
logger = logging.getLogger(__name__)

def periodogram(data,
                key=None,
                endog=None,
                sampling_rate = None,
                num_fft = None,
                freq_range = None,
                spectrum_type = None,
                window = None,
                alpha = None,
                beta = None,
                attenuation = None,
                mode = None,
                precision = None,
                r = None):
    r"""
    Periodogram is an estimate of the spectral density of a signal.

    Parameters
    ----------

    data : DataFrame
        Input data which contains at least two columns, one is ID column, the other is raw data.

    key : str, optional
        The ID column.

        Defaults to the first column of data if the index column of data is not provided.
        Otherwise, defaults to the index column of data.

    endog : str, optional
        The column of series to be tested.

        Defaults to the first non-key column.

    sampling_rate : float, optional
        Sampling frequency of the sequence.

        Defaults to 1.0.

    num_fft : integer, optional
        Number of DFT points. If ``num_fft`` is smaller than the length of the input, the input is cropped. If it is larger, the input is padded with zeros.

        Defaults to the length of sequence.

    freq_range : {"one_sides", "two_sides"}, optional
        Indicates result frequency range.

        Defaults to "one_sides".

    spectrum_type : {"density", "spectrum"}, optional
        Indicates power spectrum scaling type.

        Defaults to "density".

    window : str, optional
        Available input window type:

        - 'none',
        - 'bartlett',
        - 'bartlett_hann',
        - 'blackman',
        - 'blackman_harris',
        - 'bohman',
        - 'chebwin',
        - 'cosine',
        - 'flattop',
        - 'gaussian',
        - 'hamming',
        - 'hann',
        - 'kaiser',
        - 'nuttall',
        - 'parzen',
        - 'tukey'

        No default value.

    alpha : float, optional
        Window parameter for Blackman and Gaussian window.
        Only valid for Blackman and Gaussian window.
        Defaults to:
        - "Blackman" : 0.16.
        - "Gaussian" : 2.5.

    beta : float, optional
        Parameter for Kaiser window.
        Only valid for Kaiser window.

        Defaults to 8.6.

    attenuation : float, optional
        Parameter for Chebwin window.
        Only valid for Chebwin window.

        Defaults to 50.0.

    mode : {'symmetric', 'periodic'}, optional
        Parameter for Flattop window.
        Only valid for Flattop window.

        Defaults to 'symmetric'.

    precision : {'none', 'octave'}, optional
        Parameter for Flattop window.
        Only valid for Flattop window.

        Defaults to 'none'.

    r : float, optional
        Parameter for Tukey window.
        Only valid for Tukey window.

        Defaults to 0.5.

    Returns
    -------
    DataFrame
        Result, structured as follows:
        - ID: ID column.
        - FREQ: Value of sample frequencies.
        - PXX: Power spectral density or power spectrum of input data.

    Examples
    --------

    Time series df:

    >>> df.collect()
       ID    X
    0   1 -2.0
    1   2  8.0
    2   3  6.0
    3   4  4.0
    4   5  1.0
    5   6  0.0
    6   7  3.0
    7   8  5.0

    Perform Periodogram function:

    >>> res = periodogram(data=df,
                          key='ID',
                          endog='X',
                          sampling_rate=100,
                          window="hamming",
                          freq_range="two_sides")

    Outputs:

    >>> res.collect()
       ID  FREQ       PXX
    0   1   0.0  0.449371
    1   2  12.5  0.072737
    2   3  25.0  0.075790
    3   4  37.5  0.006659
    4   5 -50.0  0.000960
    5   6 -37.5  0.006659
    6   7 -25.0  0.075790
    7   8 -12.5  0.072737
    """
    conn = data.connection_context
    require_pal_usable(conn)
    window_map = {'none' : 'none',
                  'bartlett' : 'bartlett',
                  'bartlett_hann' : 'bartlett_hann',
                  'blackman' : 'blackman',
                  'blackman_harris' : 'blackman_harris',
                  'bohman' : 'bohman',
                  'chebwin' : 'chebwin',
                  'cosine' : 'cosine',
                  'flattop' : 'flattop',
                  'gaussian' : 'gaussian',
                  'hamming' : 'hamming',
                  'hann' : 'hann',
                  'kaiser' : 'kaiser',
                  'nuttall' : 'nuttall',
                  'parzen' : 'parzen',
                  'tukey' : 'tukey'}
    freq_range_map = {"one_sides" : 0, "two_sides" : 1}
    spectrum_type_map = {"density" : 0, "spectrum" : 1}
    mode_map = {"symmetric" : "symmetric", "periodic" : "periodic"}
    sampling_rate = arg('sampling_rate', sampling_rate, float)
    num_fft = arg('num_fft', num_fft, int)
    freq_range = arg('freq_range', freq_range, freq_range_map)
    spectrum_type = arg('spectrum_type', spectrum_type, spectrum_type_map)
    window = arg('window', window, window_map)
    alpha = arg('alpha', alpha, float)
    beta = arg('beta', beta, float)
    attenuation = arg('attenuation', attenuation, float)
    mode = arg('mode', mode, mode_map)
    precision = arg('precision', precision, str)
    r = arg('r', r, float)

    key = arg('key', key, str)
    endog = arg('endog', endog, str)

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

    # key column type check
    is_index_int = _is_index_int(data_, key)
    if not is_index_int:
        max_ = data.select(key).max()
        min_ = data.select(key).min()
        delta = (max_ - min_) / (data.count() - 1)
        timedelta = delta.total_seconds()
        data_ = _convert_index_from_timestamp_to_int(data_, key)

    unique_id = str(uuid.uuid1()).replace('-', '_').upper()
    res_tbl = f'#PAL_PERIODOGRAM_RESULT_TBL_{unique_id}'
    param_rows = [('SAMPLING_RATE', None, sampling_rate,  None),
                  ('NUM_FFT', num_fft, None, None),
                  ('FREQ_RANGE', freq_range, None, None),
                  ('SPECTRUM_TYPE', spectrum_type, None, None),
                  ('WINDOW', None, None, window),
                  ('ALPHA', None, alpha, None),
                  ('BETA', None, beta, None),
                  ('ATTENUATION', None, attenuation, None),
                  ('MODE', None, None, mode),
                  ('PRECISION', None, None, precision),
                  ('R', None, r, None)]

    try:
        if check_pal_function_exist(conn, '%PERIODOGRAM%', like=True):
            call_pal_auto_with_hint(conn,
                                    None,
                                    'PAL_PERIODOGRAM',
                                    data_,
                                    ParameterTable().with_data(param_rows),
                                    res_tbl)
        else:
            msg = 'The version of your SAP HANA does not support periodogram!'
            logger.error(msg)
            raise ValueError(msg)
    except dbapi.Error as db_err:
        logger.exception(str(db_err))
        try_drop(conn, res_tbl)
        raise
    except pyodbc.Error as db_err:
        logger.exception(str(db_err.args[1]))
        try_drop(conn, res_tbl)
        raise
    result_df = conn.table(res_tbl)
    if not is_index_int:
        result_df = conn.sql(f"""
                              SELECT ADD_SECONDS('{min_}', ({quotename(result_df.columns[0])} - 1) * {timedelta}) AS {quotename(key)},
                              {quotename(result_df.columns[1])},
                              {quotename(result_df.columns[2])}
                              FROM ({result_df.select_statement})
                              """)
    return result_df
