"""
This module contains Python wrapper for PAL ARIMA algorithm.

The following class are available:

    * :class:`ARIMA`
"""
#pylint: disable=too-many-instance-attributes, too-few-public-methods, invalid-name, too-many-statements
#pylint: disable=too-many-lines, line-too-long, too-many-arguments, too-many-branches, attribute-defined-outside-init
#pylint: disable=simplifiable-if-statement, too-many-locals, bare-except, consider-using-dict-items
#pylint: disable=consider-using-f-string, super-with-arguments, unnecessary-pass, c-extension-no-member
#pylint: disable=broad-except, use-a-generator, no-self-use, too-many-return-statements, duplicate-string-formatting-argument
import logging
import uuid
import warnings
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from hana_ml.dataframe import quotename
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.algorithms.pal.sqlgen import trace_sql
from hana_ml.algorithms.pal.utility import check_pal_function_exist
from hana_ml.algorithms.pal.pal_base import (
    PALBase,
    arg,
    ParameterTable,
    ListOfStrings,
    TupleOfIntegers,
    pal_param_register,
    try_drop,
    require_pal_usable,
    execute_logged
)

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

def _categorical_variable_update(input_cate_var):
    if isinstance(input_cate_var, str):
        input_cate_var = [input_cate_var]
    input_cate_var = arg('categorical_variable', input_cate_var, ListOfStrings)
    return input_cate_var

def _convert_index_from_timestamp_to_int(data, key=None):
    if key is None:
        if data.index is None:
            key = data.columns[0]
        else:
            key = data.index
    return data.add_id(key + '(INT)', ref_col=key).deselect(key)

def _is_index_int(data, key=None):
    if key is None:
        if data.index is None:
            key = data.columns[0]
        else:
            key = data.index
    try:
        if not 'INT' in data.get_table_structure()[key].upper():
            return False
    except Exception as err:
        logger.warning(err)
        pass
    return True

def _get_forecast_starttime_and_timedelta(data, key=None, is_index_int=True):
    if key is None:
        if data.index is None:
            key = data.columns[0]
        else:
            key = data.index
    max_ = data.select(key).max()
    min_ = data.select(key).min()
    delta = (max_ - min_) / (data.count() - 1)
    if is_index_int:
        return max_ + delta, delta
    return max_ + delta, delta.total_seconds()

def _params_check(input_dict, param_map):
    update_params = {}
    if not input_dict or input_dict is None:
        return update_params

    for parm in input_dict:
        if parm in ['show_explainer', 'allow_new_index']:
            val = input_dict.get(parm)
            if val is not None:
                arg('{}'.format(parm), val, bool)
        elif parm ==  'categorical_variable':
            pass
        elif parm == 'order':
            order_tuple = input_dict.get('order')
            if order_tuple is not None:
                if len(order_tuple) != 3:
                    msg = ('order must contain exactly 3 integers for regression order, ' +
                           'differentiation order and moving average order!')
                    logger.error(msg)
                    raise ValueError(msg)
                for each in order_tuple:
                    arg('order', each, int)
                update_params['ORDER'] = (order_tuple, TupleOfIntegers)
        elif parm == 'seasonal_order':
            seasonal_order_tuple = input_dict.get('seasonal_order')
            if seasonal_order_tuple is not None:
                if len(seasonal_order_tuple) != 4:
                    msg = ('seasonal_order must contain exactly 4 integers for regression order, ' +
                           'differentiation order, moving average order for seasonal part' +
                           'and seasonal period.')
                    logger.error(msg)
                    raise ValueError(msg)
                for each in seasonal_order_tuple:
                    arg('order', each, int)
                if seasonal_order_tuple[3] <= 1:
                    msg = 's in seasonal_order(P,D,Q,s) must be larger than 1!'
                    logger.error(msg)
                    raise ValueError(msg)
                update_params['SEASONAL_ORDER'] = (seasonal_order_tuple, TupleOfIntegers)
        else:
            if parm in param_map.keys():
                parm_val = input_dict[parm]
                arg_map = param_map[parm]
                if arg_map[1] == ListOfStrings and isinstance(parm_val, str):
                    parm_val = [parm_val]
                if len(arg_map) == 2:
                    update_params[arg_map[0]] = (arg(parm, parm_val, arg_map[1]), arg_map[1])
                else:
                    update_params[arg_map[0]] = (arg(parm, parm_val, arg_map[2]), arg_map[1])
            else:
                err_msg = f"'{parm}' is not a valid parameter name for initializing an ARIMA model!"
                logger.error(err_msg)
                raise KeyError(err_msg)

        if input_dict.get('order') and input_dict.get('seasonal_order') and input_dict.get('include_mean'):
            if input_dict['order'][1] + input_dict['seasonal_order'][1] > 1:
                msg = ('include_mean is only valid when the sum of differentiation order ' +
                       'seasonal_period is not larger than 1.')
                logger.error(msg)
                raise ValueError(msg)

    return update_params

def _delete_none_key_in_dict(input_dict):
    for key in list(input_dict.keys()) :
        if input_dict[key] is None:
            del input_dict[key]
    return input_dict

class _ARIMABase(PALBase):
    __init_param_dict = {'order' : ('ORDER', TupleOfIntegers),
                         'seasonal_order' : ('SEASONAL_ORDER', TupleOfIntegers),
                         'method' : ('METHOD', int, {'css':0, 'mle':1, 'css-mle':2}),
                         'include_mean' : ('INCLUDE_MEAN', bool),
                         'forecast_method'  : ('FORECAST_METHOD', int, {'formula_forecast':0, 'innovations_algorithm':1}),
                         'output_fitted'  : ('OUTPUT_FITTED', bool),
                         'thread_ratio' : ('THREAD_RATIO', float),
                         'background_size' : ('BACKGROUND_SIZE', int),
                         'solver' : ('SOLVER', int, {'bfgs':0, 'l-bfgs':1, 'l-bfgs-b':2})}

    __predict_param_dict = {'forecast_method' : ('FORECAST_METHOD', int, {'formula_forecast':0,
                                                                          'innovations_algorithm':1,
                                                                          'truncation_algorithm':2}),
                            'forecast_length' : ('FORECAST_LENGTH', int),
                            'thread_ratio' : ('THREAD_RATIO', float),
                            'top_k_attributions' : ('TOP_K_ATTRIBUTIONS', int),
                            'trend_mod' : ('TREND_MOD', float),
                            'trend_width' : ('TREND_WIDTH', float),
                            'seasonal_width' : ('SEASONAL_WIDTH', float)}

    def __init__(self,
                 order=None,
                 seasonal_order=None,
                 method=None,
                 include_mean=None,
                 forecast_method=None,
                 output_fitted=None,
                 thread_ratio=None,
                 background_size=None,
                 solver=None,
                 massive=False,
                 group_params=None):

        setattr(self, 'hanaml_parameters', pal_param_register())
        super(_ARIMABase, self).__init__()

        init_params = {'order' : order,
                       'seasonal_order' : seasonal_order,
                       'method' : method,
                       'include_mean' : include_mean,
                       'forecast_method' : forecast_method,
                       'output_fitted' : output_fitted,
                       'thread_ratio' : thread_ratio,
                       'background_size' : background_size,
                       'solver' : solver}
        init_params = _delete_none_key_in_dict(init_params)
        self.init_params = init_params
        self.__pal_params = {}

        self.massive = self._arg('massive', massive, bool)
        if self.massive is not True:
            self.__pal_params = _params_check(input_dict=self.init_params,
                                              param_map=self.__init_param_dict)

        else: # massive mode
            group_params = arg('group_params', group_params, dict)
            group_params = {} if group_params is None else group_params
            for group in group_params:
                self._arg('Parameters with group_key ' + str(group), group_params[group], dict)
            self.group_params = group_params

            for group in self.group_params:
                self.__pal_params[group] = _params_check(input_dict=self.group_params[group],
                                                         param_map=self.__init_param_dict)
            if self.init_params:
                special_group_name = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
                self.__pal_params[special_group_name] = _params_check(input_dict=self.init_params,
                                                                      param_map=self.__init_param_dict)

        self.forecast_start = None
        self.timedelta = None
        self.is_index_int = True
        self.group_key_type = None
        self.data_groups = None
        self.explainer_ = None

    def __map_param(self, name, value, typ):
        tpl = ()
        if typ in [int, bool]:
            tpl = (name, value, None, None)
        elif typ == float:
            tpl = (name, None, value, None)
        #elif typ in [str, ListOfStrings]:
        #    tpl = (name, None, None, value)
        return tpl

    @trace_sql
    def _fit(self, data, endog, group_params, group_key_type, categorical_variable):
        setattr(self, 'hanaml_fit_params', pal_param_register())
        conn = data.connection_context
        require_pal_usable(conn)
        self.conn_context = conn
        param_rows = []

        if self.massive is not True:
            for name in self.__pal_params:
                value, typ = self.__pal_params[name]
                if name == 'ORDER':
                    order_list = ['P', 'D', 'Q']
                    for i in range(0,3):
                        tpl = [(order_list[i], value[i], None, None)]
                        param_rows.extend(tpl)
                elif name == 'SEASONAL_ORDER':
                    s_order_list = ['SEASONAL_P', 'SEASONAL_D', 'SEASONAL_Q', 'SEASONAL_PERIOD']
                    for i in range(0,4):
                        tpl = [(s_order_list[i], value[i], None, None)]
                        param_rows.extend(tpl)
                else:
                    tpl = [self.__map_param(name, value, typ)]
                    param_rows.extend(tpl)

            tpl = [('DEPENDENT_VARIABLE', None, None, endog)]
            param_rows.extend(tpl)

            categorical_variable = _categorical_variable_update(categorical_variable)
            if categorical_variable:
                param_rows.extend([('CATEGORICAL_VARIABLE', None, None, var) for var in categorical_variable])

            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            outputs = ['MODEL', 'FIT']
            outputs = ['#PAL_ARIMA_{}_TBL_{}_{}'.format(name, self.id, unique_id)
                       for name in outputs]
            model_tbl, fit_tbl = outputs
            try:
                self._call_pal_auto(conn,
                                    'PAL_ARIMA',
                                    data,
                                    ParameterTable().with_data(param_rows),
                                    *outputs)
            except dbapi.Error as db_err:
                logger.exception(str(db_err))
                try_drop(conn, outputs)
                raise
            except pyodbc.Error as db_err:
                logger.exception(str(db_err.args[1]))
                try_drop(conn, outputs)
                raise
            self.model_ = conn.table(model_tbl)
            self.fitted_ = conn.table(fit_tbl)
        else: # massive mode
            special_group_name = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
            if 'INT' not in group_key_type:
                categorical_variable = _categorical_variable_update(categorical_variable)
                if categorical_variable is not None:
                    param_rows.extend([(special_group_name, 'CATEGORICAL_VARIABLE', None, None, var) for var in categorical_variable])

            if 'INT' in group_key_type:
                warn_msg = "If the type of group_key is INTEGER, only parameters in group_params are valid!"
                warnings.warn(message=warn_msg)

            # for each group, only categorical_variable could be set in this algorithm fit()
            for group in group_params:
                if group in ['PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID']:
                    continue
                group_val = int(group) if 'INT' in group_key_type else group
                group_categorical_variable = None
                if group_params[group].get('categorical_variable') is not None:
                    group_categorical_variable = group_params[group]['categorical_variable']
                group_categorical_variable = _categorical_variable_update(group_categorical_variable)
                if group_categorical_variable:
                    param_rows.extend([(group_val, 'CATEGORICAL_VARIABLE', None, None, var) for var in group_categorical_variable])

            for group in self.__pal_params:
                is_special_group = False
                if group in ['PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID']:
                    group_val = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
                    is_special_group = True
                else:
                    group_val = int(group) if 'INT' in group_key_type else group
                if 'INT' in group_key_type and is_special_group is True:
                    continue
                for name in self.__pal_params[group]:
                    value, typ = self.__pal_params[group][name]
                    if name == 'ORDER':
                        order_list = ['P', 'D', 'Q']
                        for i in range(0,3):
                            tpl = [(group_val, order_list[i], value[i], None, None)]
                            param_rows.extend(tpl)
                    elif name == 'SEASONAL_ORDER':
                        s_order_list = ['SEASONAL_P', 'SEASONAL_D', 'SEASONAL_Q', 'SEASONAL_PERIOD']
                        for i in range(0,4):
                            tpl = [(group_val, s_order_list[i], value[i], None, None)]
                            param_rows.extend(tpl)
                    else:
                        tpl = [tuple([group_val] + list(self.__map_param(name, value, typ)))]
                        param_rows.extend(tpl)

            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            outputs = ['MODEL', 'FIT', 'ERROR']
            outputs = ['#PAL_ARIMA_{}_TBL_{}_{}'.format(name, self.id, unique_id)
                       for name in outputs]
            model_tbl, fit_tbl, errormsg_tbl = outputs
            if not param_rows:
                param_rows = [('1', 'PLACE_HOLDER', None, None, 'place_holder')]

            try:
                if check_pal_function_exist(conn, '%MASSIVE_ARIMA%', like=True) or self._disable_hana_execution:
                    self._call_pal_auto(conn,
                                        'PAL_MASSIVE_ARIMA',
                                        data,
                                        ParameterTable(itype=group_key_type).with_data(param_rows),
                                        *outputs)
                else:
                    msg = 'The version of your SAP HANA does not support massive ARIMA!'
                    logger.error(msg)
                    raise ValueError(msg)
            except dbapi.Error as db_err:
                logger.exception(str(db_err))
                try_drop(conn, outputs)
                raise
            except pyodbc.Error as db_err:
                logger.exception(str(db_err.args[1]))
                try_drop(conn, outputs)
                raise
            self.model_ = conn.table(model_tbl)
            self.fitted_ = conn.table(fit_tbl)

            self.error_msg_ = None
            if self.massive is True:
                if not self._disable_hana_execution:
                    self.error_msg_ = conn.table(errormsg_tbl)
                    if not self.error_msg_.collect().empty:
                        row = self.error_msg_.count()
                        for i in range(1, row+1):
                            warn_msg = "For group_key '{}',".format(self.error_msg_.collect()['GROUP_ID'][i-1]) +\
                                       " the error message is '{}'.".format(self.error_msg_.collect()['ERROR_MESSAGE'][i-1]) +\
                                       "More information could be seen in the attribute error_msg_!"
                            warnings.warn(message=warn_msg)

    def set_conn(self, connection_context):
        """
        Set connection context for an ARIMA instance.

        Parameters
        ----------
        connection_context : ConnectionContext
            The connection to the SAP HANA system.

        Returns
        -------
        None.

        """
        self.conn_context = connection_context

    @trace_sql
    def _predict(self,
                 data,
                 group_params,
                 predict_params,
                 group_key_type):

        conn = self.conn_context

        show_explainer = False
        if predict_params.get('show_explainer'):
            show_explainer = predict_params['show_explainer']

        __pal_predict_params = {}
        param_rows = []

        if self.massive is not True:
            __pal_predict_params = _params_check(input_dict=predict_params,
                                                 param_map=self.__predict_param_dict)
            for name in __pal_predict_params:
                value, typ = __pal_predict_params[name]
                if isinstance(value, (list, tuple)):
                    for val in value:
                        tpl = [self.__map_param(name, val, typ)]
                        param_rows.extend(tpl)
                else:
                    tpl = [self.__map_param(name, value, typ)]
                    param_rows.extend(tpl)

            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            result_tbl = "#PAL_ARIMA_FORECAST_RESULT_TBL_{}_{}".format(self.id, unique_id)
            decompose_tbl = "#PAL_ARIMA_FORECAST_DECOMPOSITION_TBL_{}_{}".format(self.id, unique_id)

            if show_explainer is not True:
                try:
                    self._call_pal_auto(conn,
                                        'PAL_ARIMA_FORECAST',
                                        data,
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
            else: # explain
                try:
                    if check_pal_function_exist(conn, 'ARIMAEXPLAIN%', like=True) or self._disable_hana_execution:
                        self._call_pal_auto(conn,
                                            'PAL_ARIMA_EXPLAIN',
                                            data,
                                            self.model_,
                                            ParameterTable().with_data(param_rows),
                                            result_tbl,
                                            decompose_tbl)
                    else:
                        msg = 'The version of SAP HANA does not support ARIMA explainer. Please set show_explainer=False!'
                        logger.error(msg)
                        raise ValueError(msg)
                except dbapi.Error as db_err:
                    logger.exception(str(db_err))
                    try_drop(conn, result_tbl)
                    try_drop(conn, decompose_tbl)
                    raise
                except pyodbc.Error as db_err:
                    logger.exception(str(db_err.args[1]))
                    try_drop(conn, result_tbl)
                    try_drop(conn, decompose_tbl)
                    raise


            if show_explainer is True:
                self.explainer_ = conn.table(decompose_tbl)
            return conn.table(result_tbl)

        #massive mode
        special_group_name = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
        general_params = {}
        general_params = _params_check(input_dict=predict_params,
                                       param_map=self.__predict_param_dict)

        if 'INT' in group_key_type and general_params:
            warn_msg = "If the type of group_key is INTEGER, only parameters in group_params are valid!"
            warnings.warn(message=warn_msg)

        if general_params:
            __pal_predict_params[special_group_name] = general_params

        # for each group, only categorical_variable could be set in this algorithm fit()
        group_params = {} if group_params is None else group_params
        for group in group_params:
            if group in ['PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID']:
                continue
            group_val = int(group) if 'INT' in group_key_type else group
            each_group_params = {}
            each_group_params = _params_check(input_dict=group_params[group],
                                              param_map=self.__predict_param_dict)
            if each_group_params:
                __pal_predict_params[group] = each_group_params

        for group in __pal_predict_params:
            is_special_group = False
            if group in ['PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID']:
                group_val = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
                is_special_group = True
            else:
                group_val = int(group) if 'INT' in group_key_type else group
            if 'INT' in group_key_type and is_special_group is True:
                continue
            if __pal_predict_params[group]:
                for name in __pal_predict_params[group]:
                    value, typ = __pal_predict_params[group][name]
                    if isinstance(value, (list, tuple)):
                        for val in value:
                            tpl = [tuple([group_val] + list(self.__map_param(name, val, typ)))]
                            param_rows.extend(tpl)
                    else:
                        tpl = [tuple([group_val] + list(self.__map_param(name, value, typ)))]
                        param_rows.extend(tpl)

        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        result_tbl = "#PAL_ARIMA_FORECAST_RESULT_TBL_{}_{}".format(self.id, unique_id)
        decompose_tbl = "#PAL_ARIMA_FORECAST_DECOMPOSITION_TBL_{}_{}".format(self.id, unique_id)
        errormsg_tbl = '#PAL_ARIMA_FORECAST_ERROR_TBL_{}_{}'.format(self.id, unique_id)

        if not param_rows:
            param_rows = [('1', 'PLACE_HOLDER', None, None, 'place_holder')]

        try:
            if check_pal_function_exist(conn, '%MASSIVE_ARIMA%', like=True) or self._disable_hana_execution:
                if show_explainer is True:
                    self._call_pal_auto(conn,
                                        'PAL_MASSIVE_ARIMA_EXPLAIN',
                                        data,
                                        self.model_,
                                        ParameterTable(itype=group_key_type).with_data(param_rows),
                                        result_tbl,
                                        decompose_tbl,
                                        errormsg_tbl)
                else:
                    self._call_pal_auto(conn,
                                        'PAL_MASSIVE_ARIMA_FORECAST',
                                        data,
                                        self.model_,
                                        ParameterTable(itype=group_key_type).with_data(param_rows),
                                        result_tbl,
                                        errormsg_tbl)
            else:
                msg = 'The version of SAP HANA does not support massive ARIMA!'
                logger.error(msg)
                raise ValueError(msg)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, result_tbl)
            try_drop(conn, errormsg_tbl)
            if show_explainer is True:
                try_drop(conn, decompose_tbl)
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            try_drop(conn, result_tbl)
            try_drop(conn, errormsg_tbl)
            if show_explainer is True:
                try_drop(conn, decompose_tbl)
            raise

        if show_explainer is True:
            if not self._disable_hana_execution:
                self.explainer_ = conn.table(decompose_tbl)
                err_msg = conn.table(errormsg_tbl)
                if not err_msg.collect().empty:
                    row = err_msg.count()
                    for i in range(1, row+1):
                        warn_msg = "For group_key '{}',".format(err_msg.collect()['GROUP_ID'][i-1]) +\
                                   " the error message is '{}'.".format(err_msg.collect()['ERROR_MESSAGE'][i-1]) +\
                                   "More information could be seen in the 2nd return Dataframe!"
                        warnings.warn(message=warn_msg)

            return conn.table(result_tbl), self.explainer_, err_msg
        # show_explainer is False
        return conn.table(result_tbl), conn.table(errormsg_tbl)

class ARIMA(_ARIMABase):
    r"""
    Autoregressive Integrated Moving Average ARIMA(p, d, q) model.

    .. note::
        PAL ARIMA algorithm contains four functions: ARIMA, SARIMA, ARIMAX and SARIMA depending on \n
        whether seasonal information and external (intervention) data are provided.

    Parameters
    ----------

    order : (p, d, q), tuple of int, optional
        - p: value of the auto regression order.
        - d: value of the differentiation order.
        - q: value of the moving average order.

        Defaults to (0, 0, 0).

    seasonal_order : (P, D, Q, s), tuple of int, optional
        - P: value of the auto regression order for the seasonal part.
        - D: value of the differentiation order for the seasonal part.
        - Q: value of the moving average order for the seasonal part.
        - s: value of the seasonal period.

        Defaults to (0, 0, 0, 0).

    method : {'css', 'mle', 'css-mle'}, optional
        - 'css': use the conditional sum of squares.
        - 'mle': use the maximized likelihood estimation.
        - 'css-mle': use css to approximate starting values first and then mle to fit.

        Defaults to 'css-mle'.

    include_mean : bool, optional
        ARIMA model includes a constant part if True.
        Valid only when d + D <= 1 (d is defined in ``order`` and D is defined in ``seasonal_order``).

        Defaults to True if d + D = 0 else False.

    forecast_method : {'formula_forecast', 'innovations_algorithm'}, optional

        - 'formula_forecast': compute future series via formula.
        - 'innovations_algorithm': apply innovations algorithm to compute future series,
          which requires more original information to be stored.

        Store information for the subsequent forecast method.

        Defaults to 'innovations_algorithm'.

    output_fitted : bool, optional
        Output fitted result and residuals if True.

        Defaults to True.

    thread_ratio : float, optional
        Controls the proportion of available threads to use.
        The ratio of available threads.

            - 0: single thread.
            - 0~1: percentage.
            - Others: heuristically determined.

        Defaults to -1.

    background_size : int, optional
        Indicates the number of data points used in ARIMA model explanation in the predict function.
        If you want to use the ARIMA with explanation, you must set ``background_size`` to be a positive value or -1(auto mode)
        when initializing an ARIMA instance the and then set ``show_explainer=True`` in the predict function.

        Defaults to None(no model explanation).

    solver : int, optional
        Optimization solver. options are 'bfgs', 'l-bfgs', 'l-bfgs-b'.

        Defaults to 'l-bfgs'.

    massive : bool, optional
        Specifies whether or not to activate massive mode.

        For parameter setting in massive mode, you could use both
        group_params (please see the example below) or the original parameters.
        Using original parameters will apply for all groups. However, if you define some parameters of a group,
        the value of all original parameter setting will be not applicable to such group.

        An example is as follows:

        .. only:: latex

            >>> ar = ARIMA(order=(1,0,0),
                           background_size=5,
                           massive=True,
                           group_params={'Group_1':{'output_fitted':False},
                                         'Group_2':{'output_fitted':True}})

        .. raw:: html

            <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                src="../_static/arima_init_example1.html" width="100%" height="100%">
            </iframe>


        In this example, as a parameter 'output_fitted' is set in group_params for Group_1 & Group_2,
        parameter setting of 'background_size' is not applicable to Group_1 & Group_2.

        Defaults to False.

    group_params : dict, optional
        If massive mode is activated (``massive`` is True), input data is divided into different
        groups with different parameters applied.

        An example with group_params is as follows:

        .. only:: latex

            >>> ar = ARIMA(massive=True,
               group_params={'Group_1':{'background_size':5},
                             'Group_2':{'output_fitted':False}})

        .. raw:: html

            <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                src="../_static/arima_init_example2.html" width="100%" height="100%">
            </iframe>

        Valid only when ``massive`` is True and defaults to None.

    References
    ----------
    Forecasted values of ARIMAX model can be locally interpreted(explained),
    please see:

    #. :ref:`Local Interpretability<local_interpretability-label>`
    #. :ref:`Explaining the Forecasted Values<arima_explain-label>`

    Attributes
    ----------

    model_ : DataFrame

        Model content.

    fitted_ : DateFrame

        Fitted values and residuals.

    explainer_ : DataFrame

        The with explanations with decomposition of trend, seasonal, transitory, irregular
        and reason code of exogenous variables.
        The attribute only appear when setting ``background_size`` when initializing an ARIMA instance
        and ``show_explainer=True`` in the predict function.

    error_msg_ :  DataFrame

        Error message and only valid if ``massive=True`` when create an 'ARIMA' instance.

    Examples
    --------

    ARIMA example:

    Input dataframe df for ARIMA:

    >>> df.head(5).collect()
       TIMESTAMP              Y
    0          1   -0.636126431
    1          2    3.092508651
    2          3    -0.73733556
    3          4   -3.142190983
    4          5    2.088819813

    Create an ARIMA instance:

    >>> arima = ARIMA(order=(0, 0, 1), seasonal_order=(1, 0, 0, 4), method='mle', thread_ratio=1.0)

    Perform fit on the given data:

    >>> arima.fit(data=df)

    Show the output:

    >>> arima.head(5).model_.collect()
       KEY      VALUE
    0    p          0
    1   AR
    2    d          0
    3    q          1
    4   MA  -0.141073

    >>> arima.fitted_.head(3).collect().set_index('TIMESTAMP')
       TIMESTAMP     FITTED    RESIDUALS
    0          1   0.023374    -0.659500
    1          2   0.114596     2.977913
    2          3  -0.396567    -0.340769

    Perform predict on the model:

    >>> result = arima.predict(forecast_method='innovations_algorithm', forecast_length=10)

    Show the output:

    >>> result.head(3).collect()
      TIMESTAMP   FORECAST           SE        LO80        HI80         LO95        HI95
    0         0   1.557783     1.302436   -0.111357    3.226922    -0.994945    4.110511
    1         1   3.765987     1.315333    2.080320    5.451654     1.187983    6.343992
    2         2  -0.565599     1.315333   -2.251266    1.120068    -3.143603    2.012406

    If you want to see the decomposed result of predict result, you could set ``background_size``
    when initializing an ARIMA instance and set ``show_explainer`` = True in the predict():

    >>> arima = ARIMA(order=(0, 0, 1),
                      seasonal_order=(1, 0, 0, 4),
                      method='mle',
                      thread_ratio=1.0,
                      background_size=10)
    >>> result = arima.predict(forecast_method='innovations_algorithm',
                               forecast_length=3,
                               allow_new_index=False,
                               show_explainer=True)

    Show the explainer\_ of arima instance:

    >>> arima.explainer_.head(3).collect()
      ID     TREND SEASONAL TRANSITORY IRREGULAR                                          EXOGENOUS
    0  0  1.179043     None       None      None  [{"attr":"X","val":-0.49871412549199997,"pct":...
    1  1  1.252138     None       None      None  [{"attr":"X","val":-0.27390052549199997,"pct":...
    2  2  1.362164     None       None      None  [{"attr":"X","val":-0.19046313238292013,"pct":...

    ARIMAX example:

    Input dataframe df for ARIMAX:

    >>> df.head(5).collect()
       ID                   Y                   X
    0   1                 1.2                 0.8
    1   2    1.34845613096197                 1.2
    2   3    1.32261090809898    1.34845613096197
    3   4    1.38095306748554    1.32261090809898
    4   5    1.54066648969168    1.38095306748554

    Create an ARIMAX instance:

    >>> arimax = ARIMA(order=(1, 0, 1), method='mle', thread_ratio=1.0)

    Perform fit on the given data:

    >>> arimax.fit(data=df, endog='Y')

    Show the output:

    >>> arimax.model_.collect().head(5)
       KEY      VALUE
    0    p          1
    1   AR   0.302207
    2    d          0
    3    q          1
    4   MA   0.291575

    >>> arimax.fitted_.head(3).collect().set_index('TIMESTAMP')
      TIMESTAMP     FITTED    RESIDUALS
    0         1   1.182363     0.017637
    1         2   1.416213    -0.067757
    2         3   1.453572    -0.130961

    Perform predict on the ARIMAX model:

    Input dataframe df2 for ARIMAX predict:

    >>> df2.head(5).collect()
      TIMESTAMP          X
    0         1   0.800000
    1         2   1.200000
    2         3   1.348456
    3         4   1.322611
    4         5   1.380953

    >>> result = arimax.predict(df2, forecast_method='innovations_algorithm', forecast_length=5)

    Show the output:

    >>> result.head(3).collect()
       TIMESTAMP   FORECAST          SE        LO80         HI80        LO95        HI95
    0          0   1.195952    0.093510    1.076114     1.315791    1.012675    1.379229
    1          1   1.411284    0.108753    1.271912     1.550657    1.198132    1.624436
    2          2   1.491856    0.110040    1.350835     1.632878    1.276182    1.707530

    """
    def fit(self,
            data,
            key=None,
            endog=None,
            exog=None,
            group_key=None,
            group_params=None,
            categorical_variable=None):
        """
        Generates ARIMA models with given parameters.

        Parameters
        ----------

        data : DataFrame

            Input data which at least have two columns: key and endog.

            We also support ARIMAX which needs external data (exogenous variables).

        key : str, optional

            The timestamp column of data. The type of key column should be INTEGER,
            TIMESTAMP, DATE or SECONDDATE.

            In massive mode, defaults to the first-non group key column of data if the index columns of data is not provided.
            Otherwise, defaults to the second of index columns of data and the first column of index columns is group_key.

        endog : str, optional

            The endogenous variable, i.e. time series. The type of endog column could be
            INTEGER, DOUBLE or DECIMAL(p,s).

            In single mode, defaults to the first non-ID column.
            In massive mode, defaults to the first non group_key, non key column.

        exog : str or a list of str, optional

            An optional array of exogenous variables. The type of exog column could be
            INTEGER, DOUBLE or DECIMAL(p,s).

            Valid only for ARIMAX.

            Defaults to None. Please set this parameter explicitly if you have exogenous variables.

        group_key : str, optional
            The column of group_key. Data type can be INT or NVARCHAR/VARCHAR.
            If data type is INT, only parameters set in the group_params are valid.

            This parameter is only valid when ``massive`` is True in class instance initialization.

            Defaults to the first column of data if the index columns of data is not provided.
            Otherwise, defaults to the first column of index columns.

        group_params : dict, optional
            If massive mode is activated (``massive`` is True in class instance initialization),
            input data is divided into different groups with different parameters applied.

            An example with ``group_params`` is as follows:

            .. only:: latex

                >>> ar = ARIMA(massive=True,
                               group_params={'Group_1':{'background_size':5},
                                             'Group_2':{'output_fitted':False}})
                >>> ar.fit(data=train_df,
                           group_params={'Group_1':{'categorical_variable':'AA'},
                                         'Group_2':{'categorical_variable':'BB'}))

            .. raw:: html

                <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                    src="../_static/arima_fit_example.html" width="100%" height="100%">
                </iframe>

            Valid only when ``massive`` is True in class instance initialization(i.e. `self.massive` is True).

            Defaults to None.

        categorical_variable : str or ist of str, optional
            Specifies INTEGER columns specified that should be be treated as categorical.

            Other INTEGER columns will be treated as continuous.

            Defaults to None.

        Returns
        -------
        A fitted object of "ARIMA".
        """
        setattr(self, 'hanaml_fit_params', pal_param_register())
        if data is None:
            msg = ('The data for fit cannot be None!')
            logger.error(msg)
            raise ValueError(msg)

        group_params = {} if group_params is None else group_params
        if group_params:
            for group in group_params:
                self._arg('Parameters with group_key ' + str(group),
                          group_params[group], dict)

        cols = data.columns
        index = data.index
        group_id = []
        group_key_type = None
        if self.massive is True:
            group_key = self._arg('group_key', group_key, str)
            if index is not None:
                group_key = _col_index_check(group_key, 'group_key', index[0], cols)
            else:
                if group_key is None:
                    group_key = cols[0]

            if group_key is not None and group_key not in cols:
                msg = ("Please select group_key from {}!".format(cols))
                logger.error(msg)
                raise ValueError(msg)
            data_groups = list(data[[group_key]].collect()[group_key].drop_duplicates())
            # for predict when data is None
            self.data_groups = data_groups
            param_keys = list(group_params.keys())
            if not self._disable_hana_execution:
                gid_type = data[[group_key]].dtypes()[0]
                if not all([(int(ky) if 'INT' in gid_type[1] else ky) in data_groups for ky in param_keys]):
                    msg = 'Invalid group key identified in group parameters!'
                    logger.error(msg)
                    raise ValueError(msg)
            else:
                gid_type = {tp[0]:(tp[0], tp[1], tp[2]) for tp in data.dtypes()}[group_key]

            if 'INT' in gid_type[1]:
                group_key_type = gid_type[1]
            elif 'VARCHAR' in gid_type[1]:
                group_key_type = gid_type[1] + '({})'.format(gid_type[2])
            group_id = [group_key]
            cols.remove(group_key)

            key = self._arg('key', key, str)
            if index is not None:
                key = _col_index_check(key, 'key', index[1], cols)
            else:
                if key is None:
                    key = cols[0]

        else: # single mode
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

        if self.massive is not True:
            data_ = data[[key] + [endog] + exog]
            self.is_index_int = _is_index_int(data_, key)
            if not self.is_index_int:
                data_= _convert_index_from_timestamp_to_int(data_, key)
            try:
                self.forecast_start, self.timedelta = _get_forecast_starttime_and_timedelta(data, key, self.is_index_int)
            except Exception as err:
                logger.warning(err)

        else: # massive mode
            self.is_index_int = _is_index_int(data, key)
            data_ = data[group_id + [key] + [endog] + exog]
            recomb_data = None
            self.forecast_start = {}
            self.timedelta = {}
            group_count = {}
            for group in data_groups:
                group_val = group if 'INT' in group_key_type else "'{}'".format(group)
                group_data = data_.filter("{}={}".format(quotename(data_.dtypes()[0][0]),
                                                         group_val)).sort(data_.dtypes()[0][0])
                group_count[group] = group_data.count()
                try:
                    self.forecast_start[group], self.timedelta[group] =\
                    _get_forecast_starttime_and_timedelta(group_data,
                                                          key,
                                                          self.is_index_int)
                except Exception as err:
                    logger.warning(err)
                    pass
                if self.is_index_int is False:
                    group_data = _convert_index_from_timestamp_to_int(group_data, key)
                if recomb_data is None:
                    recomb_data = group_data
                else:
                    recomb_data = recomb_data.union(group_data)

            if not self._disable_hana_execution:
                if self.is_index_int is True:
                    data_ = recomb_data[group_id + [key] + [endog] + exog]
                else:
                    data_ = recomb_data[group_id + [key+'(INT)'] + [endog] + exog]

        self.fit_data = data_
        super(ARIMA, self)._fit(data_, endog, group_params, group_key_type, categorical_variable)

        return self

    def predict(self,
                data=None,
                key=None,
                group_key=None,
                group_params=None,
                forecast_method=None,
                forecast_length=None,
                allow_new_index=False,
                show_explainer=False,
                thread_ratio=None,
                top_k_attributions=None,
                trend_mod=None,
                trend_width=None,
                seasonal_width=None):
        r"""

        Makes time series forecast based on the estimated ARIMA model.

        Parameters
        ----------

        data : DataFrame, optional

            Index and exogenous variables for forecast. For ARIMAX only.

            Defaults to None.

        key : str, optional

            The timestamp column of data. The data type of key column should be
            INTEGER, TIMESTAMP, DATE or SECONDDATE. For ARIMAX only.

            In massive mode, defaults to the first-non group key column of data if the index columns of data is not provided.
            Otherwise, defaults to the second of index columns of data and the first column of index columns is group_key.

        group_key : str, optional
            The column of group_key. Data type can be INT or NVARCHAR/VARCHAR.
            If data type is INT, only parameters set in the group_params are valid.

            This parameter is only valid when ``massive`` is True.

            Defaults to the first column of data if the index columns of data is not provided.
            Otherwise, defaults to the first column of index columns.

        group_params : dict, optional
            If massive mode is activated (``massive`` is True in class instance initialization),
            input data is divided into different groups with different parameters applied.

            An example with ``group_params`` is as follows:

            .. only:: latex

                >>> ar = ARIMA(massive=True,
                               group_params={'Group_1':{'background_size':5},
                                             'Group_2':{'output_fitted':False}})
                >>> ar.fit(data=train_df,
                           group_params={'Group_1':{'categorical_variable':'AA'},
                                         'Group_2':{'categorical_variable':'BB'}))
                >>> ar.predict(data=pred_df,
                               group_params={'Group_1':{'forecast_method':'formula_forecast'}})

            .. raw:: html

                <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                    src="../_static/arima_predict_example.html" width="100%" height="100%">
                </iframe>

            Valid only when `self.massive` is True.

            Defaults to None.

        forecast_method : {'formula_forecast', 'innovations_algorithm', 'truncation_algorithm'}, optional
            Specify the forecast method.

              - 'formula_forecast': forecast via formula.
              - 'innovations_algorithm': apply innovations algorithm to forecast.
              - 'truncation_algorithm': a forecast method much faster than innovations algorithm when
                the AR representation of ARIMA model can be truncated to finite order

            Defaults to 'innovations_algorithm' if, in class initialization, the parameter ``forecast_method``
            is not set, or set as 'inovations_algorithm'; otherwise defaults to 'formula_forecast'.

        forecast_length : int, optional

            Number of points to forecast.

            Valid only when ``data`` is None.

            In ARIMAX, the forecast length is the same as the length of the input data.

            Defaults to None.

        allow_new_index : bool, optional

            Indicate whether a new index column is allowed in the result.

              - True: return the result with new integer or timestamp index column.
              - False: return the result with index column starting from 0.

            Defaults to False.

        show_explainer : bool, optional
            Indicate whether to invoke the ARIMA with explanations function in the predict.
            Only valid when ``background_size`` is set when initializing an ARIMA instance.

            If true, the contributions of trend, seasonal, transitory irregular and exogenous are
            shown in a attribute called explainer\_ of arima/auto arima instance.

            Defaults to False.

        thread_ratio : float, optional
            Controls the proportion of available threads to use.
            The ratio of available threads.

                - 0: single thread
                - 0~1: percentage
                - Others: heuristically determined

            Defaults to -1. Valid only when ``show_explainer`` is True.

        top_k_attributions : int, optional

            Specifies the number of attributes with the largest contribution that will be output.
            0-contributed attributes will not be output
            Valid only when ``show_explainer`` is True.

            Defaults to 10.

        trend_mod : double, optional

            The real AR roots with inverse modulus larger than TREND_MOD will be integrated into trend component.
            Valid only when ``show_explainer`` is True.
            Cannot be smaller than 0.

            Defaults to 0.4.

        trend_width : double, optional

            Specifies the bandwidth of spectrum of trend component in unit of rad.
            Valid only when ``show_explainer`` is True. Cannot be smaller than 0.

            Defaults to 0.035.

        seasonal_width : double, optional

            Specifies the bandwidth of spectrum of seasonal component in unit of rad.
            Valid only when ``show_explainer`` is True. Cannot be smaller than 0.

            Defaults to 0.035.

        Returns
        -------

        DataFrame
            Forecasted values, structured as follows:

              - ID, type INTEGER or TIMESTAMP.
              - FORECAST, type DOUBLE, forecast value.
              - SE, type DOUBLE, standard error.
              - LO80, type DOUBLE, low 80% value.
              - HI80, type DOUBLE, high 80% value.
              - LO95, type DOUBLE, low 95% value.
              - HI95, type DOUBLE, high 95% value.

        """
        if getattr(self, 'model_', None) is None:
            raise FitIncompleteError("Model not initialized. Perform a fit first!")

        group_params = arg('group_params', group_params, dict)
        group_params = {} if group_params is None else group_params
        if group_params:
            for group in group_params:
                self._arg('Parameters with group_key ' + str(group),
                          group_params[group], dict)

        predict_params = {'forecast_method' : forecast_method,
                          'forecast_length' : forecast_length,
                          'thread_ratio' : thread_ratio,
                          'top_k_attributions' : top_k_attributions,
                          'trend_mod' : trend_mod,
                          'trend_width' : trend_width,
                          'seasonal_width' : seasonal_width,
                          'show_explainer' : show_explainer,
                          'allow_new_index' : allow_new_index}
        predict_params = _delete_none_key_in_dict(predict_params)

        arg('allow_new_index', allow_new_index, bool)
        arg('show_explainer', show_explainer, bool)
        if predict_params.get('show_explainer') is None:
            predict_params.update({'show_explainer':False})
        if predict_params.get('allow_new_index') is None:
            predict_params.update({'allow_new_index':False})

        # validate key
        key = self._arg('key', key, str)

        if ((key is not None) and (data is not None) and (key not in data.columns)):
            msg = 'Please select key from {}!'.format(data.columns)
            logger.error(msg)
            raise ValueError(msg)

        data_ = data
        group_key_type = None
        # prepare the data, which could be empty or combination of key(must be the first column) and external data.
        if data is None:
            data_groups = self.data_groups
            self.predict_data = None
            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            data_name = "#PAL_ARIMA_PREDICT_DATA_{}".format(unique_id)
            with self.conn_context.connection.cursor() as cur:
                if self.massive is not True:
                    execute_logged(cur,
                                   'CREATE LOCAL TEMPORARY COLUMN TABLE {} ("TIMESTAMP" INTEGER, "Y" DOUBLE)'.format(data_name),
                                   self.conn_context.sql_tracer,
                                   self.conn_context)
                else:# massive mode
                    if self.group_key_type is not None:
                        group_key_type = self.group_key_type
                    else:
                        group_key_type = 'NVARCHAR(100)'
                    execute_logged(cur,
                                   'CREATE LOCAL TEMPORARY COLUMN TABLE {} ("GROUP_ID" {}, "TIMESTAMP" INTEGER, "Y" DOUBLE)'.format(data_name, group_key_type),
                                   self.conn_context.sql_tracer,
                                   self.conn_context)
            if not self.conn_context.connection.getautocommit():
                self.conn_context.connection.commit()
            data_ = self.conn_context.table(data_name)
            # for default key value
            if key is None:
                key = 'TIMESTAMP'
            if group_key is None:
                group_key = 'GROUP_ID'
        else: #  data is not None
            index = data.index
            cols = data.columns
            group_id = []
            if self.massive is True:
                group_key = self._arg('group_key', group_key, str)
                if index is not None:
                    group_key = _col_index_check(group_key, 'group_key', index[0], cols)
                else:
                    if group_key is None:
                        group_key = cols[0]
                if group_key is not None and group_key not in cols:
                    msg = ("Please select group_key from from '{}'!".format(cols))
                    logger.error(msg)
                    raise ValueError(msg)
                data_groups = list(data[[group_key]].collect()[group_key].drop_duplicates())

                param_keys = list(group_params.keys())
                if not self._disable_hana_execution:
                    gid_type = data[[group_key]].dtypes()[0]
                    if not all([(int(ky) if 'INT' in gid_type[1] else ky) in data_groups for ky in param_keys]):
                        msg = 'Invalid group key identified in group parameters!'
                        logger.error(msg)
                        raise ValueError(msg)
                else:
                    gid_type = {tp[0]:(tp[0], tp[1], tp[2]) for tp in data.dtypes()}[group_key]

                if 'INT' in gid_type[1]:
                    group_key_type = gid_type[1]
                elif 'VARCHAR' in gid_type[1]:
                    group_key_type = gid_type[1] + '({})'.format(gid_type[2])
                group_id = [group_key]
                cols.remove(group_key)

                key = self._arg('key', key, str)
                if index is not None:
                    key = _col_index_check(key, 'key', index[1], cols)
                else:
                    if key is None:
                        key = cols[0]
            else:
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

            exog = cols

            is_index_int = _is_index_int(data, key)
            if not is_index_int:
                data_ = _convert_index_from_timestamp_to_int(data, key)
            if is_index_int:
                data_ = data[group_id + [key] + exog]
            else:
                data_ = data_[group_id + [key + '(INT)'] + exog]
            self.predict_data = data_

        if self.massive is not True:
            result = super(ARIMA, self)._predict(data_,
                                                 group_params,
                                                 predict_params,
                                                 group_key_type)
            if not allow_new_index:
                return result

            # Note that if model_storage is used, self.in_index_int would be None, so allow_new_index is useless.
            # allow_new_index is True, to divide into two category: TIMESTAP and INTERGER
            if self.is_index_int is True: # INTERGER
                if show_explainer: # need update, as original result is not from next integer ID
                    explainer = self.explainer_
                    update_explainer = self.conn_context.sql("""
                                         SELECT {0} + {1} AS {8},
                                         {3},
                                         {4},
                                         {5},
                                         {6},
                                         {7}
                                         FROM ({2})
                                         """.format(self.forecast_start,
                                                    quotename(explainer.columns[0]),
                                                    explainer.select_statement,
                                                    quotename(explainer.columns[1]),
                                                    quotename(explainer.columns[2]),
                                                    quotename(explainer.columns[3]),
                                                    quotename(explainer.columns[4]),
                                                    quotename(explainer.columns[5]),
                                                    quotename(key)))
                    self.explainer_ = update_explainer

                return self.conn_context.sql("""
                                            SELECT {0} + {1} AS {9},
                                            {3},
                                            {4},
                                            {5},
                                            {6},
                                            {7},
                                            {8}
                                            FROM ({2})
                                            """.format(self.forecast_start,
                                                       quotename(result.columns[0]),
                                                       result.select_statement,
                                                       quotename(result.columns[1]),
                                                       quotename(result.columns[2]),
                                                       quotename(result.columns[3]),
                                                       quotename(result.columns[4]),
                                                       quotename(result.columns[5]),
                                                       quotename(result.columns[6]),
                                                       quotename(key)))
            # ID column is TIMESTAMP
            if show_explainer is True:
                explainer = self.explainer_
                update_explainer = self.conn_context.sql("""
                                                         SELECT ADD_SECONDS('{0}', {1} * {2}) AS {9},
                                                         {4},
                                                         {5},
                                                         {6},
                                                         {7},
                                                         {8}
                                                         FROM ({3})
                                                         """.format(self.forecast_start,
                                                                    quotename(explainer.columns[0]),
                                                                    self.timedelta,
                                                                    explainer.select_statement,
                                                                    quotename(explainer.columns[1]),
                                                                    quotename(explainer.columns[2]),
                                                                    quotename(explainer.columns[3]),
                                                                    quotename(explainer.columns[4]),
                                                                    quotename(explainer.columns[5]),
                                                                    quotename(key)))
                self.explainer_ = update_explainer

            return self.conn_context.sql("""
                                        SELECT ADD_SECONDS('{0}', {1} * {2}) AS {10},
                                        {4},
                                        {5},
                                        {6},
                                        {7},
                                        {8},
                                        {9}
                                        FROM ({3})
                                        """.format(self.forecast_start,
                                                   quotename(result.columns[0]),
                                                   self.timedelta,
                                                   result.select_statement,
                                                   quotename(result.columns[1]),
                                                   quotename(result.columns[2]),
                                                   quotename(result.columns[3]),
                                                   quotename(result.columns[4]),
                                                   quotename(result.columns[5]),
                                                   quotename(result.columns[6]),
                                                   quotename(key)))
        # massive mode
        if show_explainer:
            result, decomposed, error_msg = super(ARIMA, self)._predict(data_,
                                                                        group_params,
                                                                        predict_params,
                                                                        group_key_type)
        else:
            result, error_msg = super(ARIMA, self)._predict(data_,
                                                            group_params,
                                                            predict_params,
                                                            group_key_type)

        if not allow_new_index:
            if show_explainer:
                return result, decomposed, error_msg
            return result, error_msg
        # allow_new_index is True
        if self.is_index_int:
            if show_explainer:
                comb_exp = None
                for group in data_groups:
                    group_val = int(group) if 'INT' in group_key_type else "'{}'".format(group)

                    if self.predict_data is None:
                        group_exp = decomposed.filter('GROUP_ID={}'.format(group_val)).sort('TIMESTAMP')
                    else:
                        group_exp = decomposed.filter('GROUP_ID={}'.format(group_val)).sort(key)

                    sql_statement_exp = """
                                         SELECT {0},
                                         {1} + {2} AS {9},
                                         {4},
                                         {5},
                                         {6},
                                         {7},
                                         {8}
                                         FROM ({3})
                                         """.format(quotename(decomposed.columns[0]),
                                                    self.forecast_start[group],
                                                    quotename(decomposed.columns[1]),
                                                    group_exp.select_statement,
                                                    quotename(decomposed.columns[2]),
                                                    quotename(decomposed.columns[3]),
                                                    quotename(decomposed.columns[4]),
                                                    quotename(decomposed.columns[5]),
                                                    quotename(decomposed.columns[6]),
                                                    quotename(key))
                    group_exp = self.conn_context.sql(sql_statement_exp)
                    if comb_exp is None:
                        comb_exp = group_exp
                    else:
                        comb_exp = group_exp.union(comb_exp)
            comb_res = None
            for group in data_groups:
                group_val = int(group) if 'INT' in group_key_type else "'{}'".format(group)
                if self.predict_data is None:
                    group_res = result.filter('GROUP_ID={}'.format(group_val)).sort('TIMESTAMP')
                else:
                    group_res = result.filter('GROUP_ID={}'.format(group_val)).sort(key)
                sql_statement_res = """
                                    SELECT {0},
                                    {1} + {2} AS {10},
                                    {4},
                                    {5},
                                    {6},
                                    {7},
                                    {8},
                                    {9}
                                    FROM ({3})
                                    """.format(quotename(result.columns[0]),
                                               self.forecast_start[group],
                                               quotename(result.columns[1]),
                                               group_res.select_statement,
                                               quotename(result.columns[2]),
                                               quotename(result.columns[3]),
                                               quotename(result.columns[4]),
                                               quotename(result.columns[5]),
                                               quotename(result.columns[6]),
                                               quotename(result.columns[7]),
                                               quotename(key))
                group_res = self.conn_context.sql(sql_statement_res)

                if comb_res is None:
                    comb_res = group_res
                else:
                    comb_res = group_res.union(comb_res)

            result = comb_res.sort(['GROUP_ID', key])
            if show_explainer:
                self.explainer_ = comb_exp.sort(['GROUP_ID', key])
                decomposed = comb_exp.sort(['GROUP_ID', key])
                return result, decomposed, error_msg
            # show_explainer is False
            self.explainer_ = None
            return result, error_msg

        # ID column is TIMESTAMP
        comb_res = None
        for group in data_groups:
            group_val = int(group) if 'INT' in group_key_type else "'{}'".format(group)
            group_res = result.filter('GROUP_ID={}'.format(group_val)).sort(key+'(INT)')
            sql_statement_res = """
                                SELECT {0},
                                ADD_SECONDS('{1}', {2} * {3}) AS {11},
                                {5},
                                {6},
                                {7},
                                {8},
                                {9},
                                {10}
                                FROM ({4})
                                """.format(quotename(result.columns[0]),
                                           self.forecast_start[group],
                                           quotename(result.columns[1]),
                                           self.timedelta[group],
                                           group_res.select_statement,
                                           quotename(result.columns[2]),
                                           quotename(result.columns[3]),
                                           quotename(result.columns[4]),
                                           quotename(result.columns[5]),
                                           quotename(result.columns[6]),
                                           quotename(result.columns[7]),
                                           quotename(key))

            group_res = self.conn_context.sql(sql_statement_res)
            if comb_res is None:
                comb_res = group_res
            else:
                comb_res = group_res.union(comb_res)

        if show_explainer:
            comb_exp = None
            for group in data_groups:
                group_val = int(group) if 'INT' in group_key_type else "'{}'".format(group)
                group_exp = decomposed.filter('GROUP_ID={}'.format(group_val)).sort(key+'(INT)')
                sql_statement_exp = """
                                    SELECT {0},
                                    ADD_SECONDS('{1}', {2} * {3}) AS {10},
                                    {5},
                                    {6},
                                    {7},
                                    {8},
                                    {9}
                                    FROM ({4})
                                    """.format(quotename(decomposed.columns[0]),
                                               self.forecast_start[group],
                                               quotename(decomposed.columns[1]),
                                               self.timedelta[group],
                                               group_exp.select_statement,
                                               quotename(decomposed.columns[2]),
                                               quotename(decomposed.columns[3]),
                                               quotename(decomposed.columns[4]),
                                               quotename(decomposed.columns[5]),
                                               quotename(decomposed.columns[6]),
                                               quotename(key))

                group_exp = self.conn_context.sql(sql_statement_exp)
                if comb_exp is None:
                    comb_exp = group_exp
                else:
                    comb_exp = group_exp.union(comb_exp)

        result = comb_res.sort(['GROUP_ID', key])
        if show_explainer:
            self.explainer_ = comb_exp.sort(['GROUP_ID', key])
            decomposed = comb_exp.sort(['GROUP_ID', key])
            return result, decomposed, error_msg
        # show_explainer is False
        self.explainer_ = None
        return result, error_msg
