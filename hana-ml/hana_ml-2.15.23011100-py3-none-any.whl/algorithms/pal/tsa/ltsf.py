"""
This module contains Python wrapper for PAL LTSF algorithm.

The following class are available:

    * :class:`LTSF`
"""

#pylint: disable=too-many-lines, line-too-long, too-many-locals, too-many-arguments, too-many-branches, broad-except
#pylint: disable= c-extension-no-member, super-with-arguments, too-many-statements, invalid-name
#pylint: disable=duplicate-string-formatting-argument, too-many-instance-attributes, too-few-public-methods
import logging
import uuid
import warnings
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.dataframe import quotename
from hana_ml.algorithms.pal.tsa.arima import _convert_index_from_timestamp_to_int, _is_index_int, _get_forecast_starttime_and_timedelta
from hana_ml.algorithms.pal.utility import check_pal_function_exist
from hana_ml.algorithms.pal.pal_base import (
    PALBase,
    ParameterTable,
    pal_param_register,
    try_drop,
    ListOfStrings,
    require_pal_usable
)
from hana_ml.algorithms.pal.sqlgen import trace_sql

logger = logging.getLogger(__name__)

def _col_index_check(col, para_name, index_value, cols_name):
    # col: the name of a column
    # para_name: key, group_key
    # index_value: single only one, massive has tow columns
    # cols_name: all column names
    if col is None:
        if not isinstance(index_value, str):
            col = cols_name[0]
            warn_msg = "The index of data is not a single column and '{}' is None, so the first column of data is used as '{}'!".format(para_name, para_name)
            warnings.warn(message=warn_msg)
        else:
            col = index_value
    else:
        if col != index_value:
            warn_msg = "Discrepancy between the designated {} column '{}' ".format(para_name, col) +\
            "and the designated index {} column which is '{}'.".format(para_name, index_value)
            warnings.warn(message=warn_msg)
    return col

class LTSF(PALBase):
    r"""
    Long-Term Series Forecasting (LTSF).

    Although traditional algorithms are capable of predicting values in
    the near future, their performance will deteriorate greatly when it comes
    to long-term series forecasting. With the help of deep learning,
    this function implements a novel neural network architecture to achieve
    the state-of-the-art performance among the PAL family.

    Parameters
    ----------

    num_levels : int, optional
        Number of levels in the network architecture.
        Note that if warm_start = True in fit(), this parameter is not valid.

        Defaults to 2.

    kernel_size : int, optional
        Kernel size of Conv1d layer.
        Note that if warm_start = True in fit(), this parameter is not valid.

        Defaults to 3.

    hidden_expansion : int, optional
        Expands the input channel size of Conv1d layer.
        Note that if warm_start = True in fit(), this parameter is not valid.

        Defaults to 3.

    batch_size : int, optional
        Number of pieces of data for training in one iteration.

        Defaults to 8.

    num_epochs : int, optional
        Number of training epochs.

        Defaults to 1.

    random_seed : int, optional
        0 indicates using machine time as seed.

        Defaults to 0.

    position_encoding:  bool, optional
        Position encoding adds extra positional embeddings to the training series.

        False: Do not use.
        True: Use.

        Defaults to True.

    adjust_learning_rate: bool, optional
        Decays the learning rate to its half after every epoch.

        False: Do not use.
        True: Use.

        Defaults to True.

    learning_rate : float, optional
        Initinal learning rate for Adam optimizer.

        Defaults to 0.005.

    dropout_prob : float, optional
        Dropout probability of Dropout layer.

        Defaults to 0.05.

    Attributes
    ----------
    model_ : DataFrame

        Trained model content.

    loss_ : DataFrame

        Indicates the information of training loss either batch ID or average batch loss indicator.


    Examples
    --------

    Input dataframe is df_fit and create an instance of LTSF:

    >>> ltsf = LTSF(num_levels = 2,
                    kernel_size = 3,
                    hidden_expansion = 3,
                    batch_size = 8,
                    num_epochs = 2,
                    position_encoding = True,
                    adjust_learning_rate = True,
                    learning_rate = 0.005,
                    dropout_prob = 0.2,
                    random_seed = 1)

    Performing fit() on the given dataframe:

    >>> ltsf.fit(data=df.fit,
                 train_length=32,
                 forecast_length=16,
                 key="TIME_STAMP",
                 endog="TARGET",
                 exog=["FEAT1", "FEAT2", "FEAT3", "FEAT4"])
    >>> ltsf.loss_.collect()
        EPOCH          BATCH      LOSS
    0       1              0  1.177407
    1       1              1  0.925078
    2       1              2  0.798042
    3       1              3  0.712275
    4       1              4  0.702966
    5       1              5  0.703366
    6       1  epoch average  0.836522
    7       2              0  0.664331
    8       2              1  0.608385
    9       2              2  0.614841
    10      2              3  0.626234
    11      2              4  0.623597
    12      2              5  0.571699
    13      2  epoch average  0.618181

    Input dataframe for predict is df_predict and performing predict() on given dataframe:

    >>> result = ltsf.predict(data=df_predict)
    >>> result.collect()
       ID  FORECAST
    1   0  52.28396
    2   1  57.03466
    3   2  69.49162
    4   3  68.06987
    5   4  40.43507
    6   5  55.53528
    7   6  54.17256
    8   7  39.32336
    9   8  25.51410
    10  9 102.11331
    11 10 134.10745
    12 11  48.32333
    13 12  46.47223
    14 13  72.44048
    15 14  65.29192
    16 15  69.33713

    We also provide the continuous training which uses a parameter warm_start to control.
    The model used in the training is the attribute of model_ of a "LTSF" object.
    You could also use load_model() to load a trained model for continous training.

    >>> ltsf.num_epochs    = 1
    >>> ltsf.dropout_prob  = 0.2
    >>> ltsf.learning_rate = 0.002
    >>> ltsf.fit(df_fit,
                 key="TIME_STAMP",
                 endog="TARGET",
                 exog=["FEAT1", "FEAT2", "FEAT3", "FEAT4"],
                 warm_start=True)

    """
#pylint: disable=too-many-arguments
    def __init__(self,
                 num_levels=None,
                 kernel_size=None,
                 hidden_expansion=None,
                 batch_size=None,
                 num_epochs=None,
                 random_seed=None,
                 position_encoding=None,
                 adjust_learning_rate=None,
                 learning_rate=None,
                 dropout_prob=None):

        setattr(self, 'hanaml_parameters', pal_param_register())
        super(LTSF, self).__init__()

        self.num_levels = self._arg('num_levels', num_levels, int)
        self.kernel_size = self._arg('kernel_size', kernel_size, int)
        self.hidden_expansion = self._arg('hidden_expansion', hidden_expansion, int)
        self.batch_size = self._arg('batch_size', batch_size, int)
        self.num_epochs = self._arg('num_epochs', num_epochs, int)
        self.random_seed = self._arg('random_seed', random_seed, int)
        self.position_encoding = self._arg('position_encoding', position_encoding, bool)
        self.adjust_learning_rate = self._arg('adjust_learning_rate', adjust_learning_rate, bool)
        self.learning_rate = self._arg('learning_rate', learning_rate, float)
        self.dropout_prob = self._arg('dropout_prob', dropout_prob, float)
        self.train_length = None
        self.forecast_length = None

        self.forecast_start = None
        self.timedelta = None
        self.is_index_int = True

#pylint: disable=too-many-arguments, too-many-branches, too-many-statements
    @trace_sql
    def fit(self,
            data,
            train_length=None,
            forecast_length=None,
            key=None,
            endog=None,
            exog=None,
            warm_start=False):
        """
        Train a LTSF model with given parameters.

        Parameters
        ----------
        data : DataFrame
            Input data.

        train_length : int
            Length of training series inputted to the network.
            Note that if use warm_start mode, this parameter is not valid.

        forecast_length : int
            Length of predictions.
            Note that if use warm_start mode, this parameter is not valid.

        key : str, optional

            The timestamp column of data. The type of key column should be INTEGER,
            TIMESTAMP, DATE or SECONDDATE.

            Defaults to the first column of data if the index column of data is not provided.
            Otherwise, defaults to the index column of data.

        endog : str, optional

            The endogenous variable, i.e. target time series. The type of endog column could be
            INTEGER, DOUBLE or DECIMAL(p,s).

            Defaults to the first non-key column.

        exog : str or a list of str, optional

            An optional array of exogenous variables. The type of exog column could be
            INTEGER, DOUBLE or DECIMAL(p,s).

            Defaults to None. Please set this parameter explicitly if you have exogenous variables.

        warm_start : bool, optional
            When set to True, reuse the ``model_`` of current object to train. We provide a method called load_model to load other model.
            Otherwise, just to train a new model.

            Defaults to False.

        Returns
        -------
        A fitted object of class "LTSF".
        """
        setattr(self, 'hanaml_fit_params', pal_param_register())

        if warm_start is True:
            if self.model_ is None:
                msg = 'warm_start mode requires the model of previous fit and self.model_ should not be None!'
                logger.error(msg)
                raise ValueError(msg)

            if self.model_ and (train_length is not None or forecast_length is not None):
                warn_msg = "The value of train_length or forecast_length in the model will be used."
                warnings.warn(message=warn_msg)

            self.train_length = None
            self.forecast_length = None

        else:
            self.train_length = self._arg('train_length', train_length, int, required=True)
            self.forecast_length = self._arg('forecast_length', forecast_length, int, required=True)

        cols = data.columns
        index = data.index
        key = self._arg('key', key, str)
        if index is not None:
            key = _col_index_check(key, 'key', index, cols)
        else:
            if key is None:
                key = cols[0]

        if key is not None and key not in cols:
            msg = ("Please select key from {}!".format(cols))
            logger.error(msg)
            raise ValueError(msg)
        cols.remove(key)

        endog = self._arg('endog', endog, str)
        if endog is not None:
            if endog not in cols:
                msg = "Please select endog from {}!".format(cols)
                logger.error(msg)
                raise ValueError(msg)
        else:
            endog = cols[0]
        cols.remove(endog)

        if exog is not None:
            if isinstance(exog, str):
                exog = [exog]
            exog = self._arg('exog', exog, ListOfStrings)
            if set(exog).issubset(set(cols)) is False:
                msg = "Please select exog from {}!".format(cols)
                logger.error(msg)
                raise ValueError(msg)
        else:
            exog = []

        data_ = data[[key] + [endog] + exog]
        self.is_index_int = _is_index_int(data_, key)
        if not self.is_index_int:
            data_= _convert_index_from_timestamp_to_int(data_, key)

        conn = data.connection_context
        require_pal_usable(conn)
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        loss_tbl = '#PAL_LTSF_LOSS_TBL_{}_{}'.format(self.id, unique_id)
        model_tbl = '#PAL_LTSF_MODEL_TBL_{}_{}'.format(self.id, unique_id)
        outputs = [loss_tbl, model_tbl]
        param_rows = [
            ('TRAIN_LENGTH',         self.train_length ,                      None,   None),
            ('FORECAST_LENGTH',      self.forecast_length ,                   None,   None),
            ('NUM_LEVELS',           self.num_levels,                         None,   None),
            ('KERNEL_SIZE',          self.kernel_size,                        None,   None),
            ('HIDDEN_EXPANSION',     self.hidden_expansion,                   None,   None),
            ('BATCH_SIZE',           self.batch_size,                         None,   None),
            ('NUM_EPOCHS',           self.num_epochs,                         None,   None),
            ('POSITION_ENCODING'   , self.position_encoding,                  None,   None),
            ('ADJUST_LEARNING_RATE', self.adjust_learning_rate,               None,   None),
            ('RANDOM_SEED',          self.random_seed,                        None,   None),
            ('DROPOUT_PROB',         None,                       self.dropout_prob,   None),
            ('LEARNING_RATE',        None,                      self.learning_rate,   None)
            ]

        try:
            if check_pal_function_exist(conn, '%LTSF%', like=True):
                if warm_start is not True:
                    self._call_pal_auto(conn,
                                        'PAL_LTSF_TRAIN',
                                        data_,
                                        ParameterTable().with_data(param_rows),
                                        *outputs)
                else:
                    self._call_pal_auto(conn,
                                        'PAL_LTSF_TRAIN_CONTINUE',
                                        data_,
                                        self.model_,
                                        ParameterTable().with_data(param_rows),
                                        *outputs)
            else:
                msg = 'The version of your SAP HANA does not support LTSF!'
                logger.error(msg)
                raise ValueError(msg)
        except dbapi.Error as db_err:
            msg = str(conn.hana_version())
            logger.exception("HANA version: %s. %s", msg, str(db_err))
            try_drop(conn, outputs)
            raise
        except pyodbc.Error as db_err:
            msg = str(conn.hana_version())
            logger.exception("HANA version: %s. %s", msg, str(db_err.args[1]))
            try_drop(conn, outputs)
            raise
        #pylint: disable=attribute-defined-outside-init
        self.loss_ = conn.table(loss_tbl)
        self.model_ = conn.table(model_tbl)
        return self

    @trace_sql
    def predict(self, data, key=None, endog=None, allow_new_index=True):
        """
        Makes time series forecast based on a LTSF model. The number of rows of input predict data must be equal to the value of train_length during training and the length of predicitons is equal to the value of forecast_length.

        Parameters
        ----------

        data : DataFrame
            Input data which constains the target time series and exogenous features (optional).
            Note that the data here requires a endog column to be the input of trained model for prediction.

        key : str, optional

            Name of the ID column.

            Mandatory if ``data`` is not indexed, or the index of ``data`` contains multiple columns.

            Defaults to the single index column of ``data`` if not provided.

        endog : str, optional

            The endogenous variable (target time series), i.e. time series. The type of endog column could be
            INTEGER, DOUBLE or DECIMAL(p,s).

            Note that endog represented the input value for a LTSF model to make prediction. The length of predicitons is equal to the value of forecast_length set in the fit().

            Defaults to the first non-key column.

        allow_new_index : bool, optional

            Indicate whether a new index column is allowed in the result.
            - True: return the result with new integer or timestamp index column.
            - False: return the result with index column starting from 0.

            Defaults to True.

        Returns
        -------

        DataFrame
            Forecasted values, structured as follows:

              - ID, type INTEGER, timestamp.
              - VALUE, type DOUBLE, forecast value.
        """
        if getattr(self, 'model_', None) is None:
            msg = ('Model not initialized. Perform a fit first.')
            logger.error(msg)
            raise FitIncompleteError(msg)

        index = data.index
        cols = data.columns

        key = self._arg('key', key, str)
        index = data.index
        if index is not None:
            key = _col_index_check(key, 'key', index, cols)
        else:
            if key is None:
                key = cols[0]

        if key is not None and key not in cols:
            msg = ("Please select key from {}!".format(cols))
            logger.error(msg)
            raise ValueError(msg)
        cols.remove(key)

        endog = self._arg('endog', endog, str)
        if endog is not None:
            if endog not in cols:
                msg = "Please select endog from {}!".format(cols)
                logger.error(msg)
                raise ValueError(msg)
        else:
            endog = cols[0]
        cols.remove(endog)

        exog = cols

        data_ = data[[key] + [endog] + exog]

        self.is_index_int = _is_index_int(data_, key)
        if not self.is_index_int:
            data_= _convert_index_from_timestamp_to_int(data_, key)
        try:
            self.forecast_start, self.timedelta = _get_forecast_starttime_and_timedelta(data, key, self.is_index_int)
        except Exception as err:
            logger.warning(err)

        conn = data.connection_context
        param_rows = []

        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        result_tbl = "#PAL_LTSF_FORECAST_RESULT_TBL_{}_{}".format(self.id, unique_id)
        try:
            self._call_pal_auto(conn,
                                'PAL_LTSF_PREDICT',
                                data_,
                                self.model_,
                                ParameterTable().with_data(param_rows),
                                result_tbl)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, result_tbl)
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            try_drop(conn, result_tbl)
            raise
        result = conn.table(result_tbl)

        if allow_new_index is not True:
            return result

        if self.is_index_int is True:
            return conn.sql("""
                            SELECT ({0}+({1} * {2})) AS {5},
                            {4}
                            FROM ({3})
                            """.format(self.forecast_start,
                                       quotename(result.columns[0]),
                                       self.timedelta,
                                       result.select_statement,
                                       quotename(result.columns[1]),
                                       quotename(key)))
        # ID column is TIMESTAMP
        return conn.sql("""
                        SELECT ADD_SECONDS('{0}', {1} * {2}) AS {5},
                        {4}
                        FROM ({3})
                        """.format(self.forecast_start,
                                   quotename(result.columns[0]),
                                   self.timedelta,
                                   result.select_statement,
                                   quotename(result.columns[1]),
                                   quotename(key)))
