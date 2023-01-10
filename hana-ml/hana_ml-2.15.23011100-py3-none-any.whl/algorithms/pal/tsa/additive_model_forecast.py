"""
This module contains Python wrapper for PAL Additive Model Forecast algorithm.

The following class are available:

    * :class:`AdditiveModelForecast`
"""
#pylint: disable=too-many-instance-attributes, too-few-public-methods, too-many-nested-blocks
#pylint: disable=too-many-lines, line-too-long, invalid-name, too-many-branches
#pylint: disable=too-many-arguments, too-many-locals, attribute-defined-outside-init
#pylint: disable=super-with-arguments, c-extension-no-member, consider-using-dict-items
#pylint: disable=no-self-use, too-many-statements, consider-using-f-string, use-a-generator
import logging
import uuid
import warnings
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.algorithms.pal.sqlgen import HolidayTable, trace_sql
from hana_ml.algorithms.pal.utility import check_pal_function_exist
from hana_ml.algorithms.pal.tsa.arima import _categorical_variable_update
from hana_ml.algorithms.pal.tsa.arima import _delete_none_key_in_dict, _col_index_check
from hana_ml.algorithms.pal.tsa.auto_arima import _validate_og
from hana_ml.algorithms.pal.pal_base import (
    arg,
    PALBase,
    ParameterTable,
    ListOfStrings,
    pal_param_register,
    try_drop,
    require_pal_usable
)
logger = logging.getLogger(__name__)

def _params_check(input_dict, param_map):
    update_params = {}
    if not input_dict or input_dict is None:
        return update_params

    for parm in input_dict:
        if parm in ['categorical_variable', 'show_explainer']:
            pass
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
                err_msg = "'{}' is not a valid parameter name for initializing an AdditiveModelForecast model!".format(parm)
                logger.error(err_msg)
                raise KeyError(err_msg)

        growth_val = input_dict.get('growth')
        logistic_growth_capacity_val =  input_dict.get('logistic_growth_capacity')
        if growth_val == 'logistic' and logistic_growth_capacity_val is None:
            msg = "logistic_growth_capacity is mandatory when growth is 'logistic'!"
            logger.error(msg)
            raise ValueError(msg)

    return update_params

def _delete_none_key_in_dict(input_dict):
    for key in list(input_dict.keys()) :
        if input_dict[key] is None:
            del input_dict[key]
    return input_dict

def _categorical_variable_update(input_cate_var):
    if isinstance(input_cate_var, str):
        input_cate_var = [input_cate_var]
    input_cate_var = arg('categorical_variable', input_cate_var, ListOfStrings)
    return input_cate_var

class _AdditiveModelForecastBase(PALBase):
    __init_param_dict = {'growth' : ('GROWTH', str),
                         'logistic_growth_capacity' : ('CAP', float),
                         'seasonality_mode'  : ('SEASONALITY_MODE', str),
                         'seasonality'  : ('SEASONALITY', ListOfStrings),
                         'num_changepoints' : ('NUM_CHANGEPOINTS', int),
                         'changepoint_range' : ('CHANGEPOINT_RANGE', float),
                         'regressor' : ('REGRESSOR', ListOfStrings),
                         'changepoints' : ('CHANGE_POINT', ListOfStrings),
                         'yearly_seasonality' : ('YEARLY_SEASONALITY', int, {'auto': -1, 'false': 0, 'true': 1}),
                         'weekly_seasonality' : ('WEEKLY_SEASONALITY', int, {'auto': -1, 'false': 0, 'true': 1}),
                         'daily_seasonality' : ('DAILY_SEASONALITY', int, {'auto': -1, 'false': 0, 'true': 1}),
                         'seasonality_prior_scale' : ('SEASONALITY_PRIOR_SCALE', float),
                         'holiday_prior_scale' : ('HOLIDAYS_PRIOR_SCALE', float),
                         'changepoint_prior_scale' : ('CHANGEPOINT_PRIOR_SCALE', float)}

    __predict_param_dict = {'logistic_growth_capacity' : ('CAP', float),
                            'interval_width' : ('INTERVAL_WIDTH', float),
                            'uncertainty_samples' : ('UNCERTAINTY_SAMPLES', int),
                            'show_explainer' : ('EXPLAINER', bool),
                            'decompose_seasonality' : ('EXPLAIN_SEASONALITY', bool),
                            'decompose_holiday' : ('EXPLAIN_HOLIDAY', bool)}
    op_name = 'AMTSA'
    def __init__(self,
                 growth=None,
                 logistic_growth_capacity=None,
                 seasonality_mode=None,
                 seasonality=None,
                 num_changepoints=None,
                 changepoint_range=None,
                 regressor=None,
                 changepoints=None,
                 yearly_seasonality=None,
                 weekly_seasonality=None,
                 daily_seasonality=None,
                 seasonality_prior_scale=None,
                 holiday_prior_scale=None,
                 changepoint_prior_scale=None,
                 massive=False,
                 group_params=None):
        super(_AdditiveModelForecastBase, self).__init__()
        setattr(self, 'hanaml_parameters', pal_param_register())

        init_params = {'growth' : growth,
                       'logistic_growth_capacity' : logistic_growth_capacity,
                       'seasonality_mode' : seasonality_mode,
                       'seasonality' : seasonality,
                       'num_changepoints' : num_changepoints,
                       'changepoint_range' : changepoint_range,
                       'regressor' : regressor,
                       'changepoints' : changepoints,
                       'yearly_seasonality' : yearly_seasonality,
                       'weekly_seasonality' : weekly_seasonality,
                       'daily_seasonality' : daily_seasonality,
                       'seasonality_prior_scale' : seasonality_prior_scale,
                       'holiday_prior_scale' : holiday_prior_scale,
                       'changepoint_prior_scale' : changepoint_prior_scale}

        init_params = _delete_none_key_in_dict(init_params)
        self.init_params = init_params
        self.__pal_params = {}

        self.massive = self._arg('massive', massive, bool)
        if self.massive is not True:
            self.__pal_params = _params_check(input_dict=self.init_params,
                                              param_map=self.__init_param_dict)
        else: # massive mode
            group_params = self._arg('group_params', group_params, dict)
            group_params = {} if group_params is None else group_params
            for group in group_params:
                self._arg('Parameters with group_key ' + str(group), group_params[group], dict)
            self.group_params = group_params

            for group in self.group_params:
                self.__pal_params[group] = _params_check(input_dict=self.group_params[group],
                                                         param_map=self.__init_param_dict)
            if init_params:
                special_group_name = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
                self.__pal_params[special_group_name] = _params_check(input_dict=self.init_params,
                                                                      param_map=self.__init_param_dict)

    def __map_param(self, name, value, typ):
        tpl = ()
        if typ in [int, bool]:
            tpl = (name, value, None, None)
        elif typ == float:
            tpl = (name, None, value, None)
        elif typ in [str, ListOfStrings]:
            tpl = (name, None, None, value)
        return tpl

    @trace_sql
    def _fit(self, data, holiday, group_params, categorical_variable, group_key_type):
        conn = data.connection_context
        require_pal_usable(conn)
        param_rows = []

        if self.massive is not True:
            for name in self.__pal_params:
                value, typ = self.__pal_params[name]
                if isinstance(value, (list, tuple)):
                    for val in value:
                        tpl = [self.__map_param(name, val, typ)]
                        param_rows.extend(tpl)
                else:
                    tpl = [self.__map_param(name, value, typ)]
                    param_rows.extend(tpl)

            categorical_variable = _categorical_variable_update(categorical_variable)
            if categorical_variable:
                param_rows.extend([('CATEGORICAL_VARIABLE', None, None, var) for var in categorical_variable])

        else: # massive mode
            special_group_name = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
            if 'INT' not in group_key_type:
                categorical_variable = _categorical_variable_update(categorical_variable)
                if categorical_variable is not None:
                    param_rows.extend([(special_group_name, 'CATEGORICAL_VARIABLE', None, None, var) for var in categorical_variable])

            if 'INT' in group_key_type and self.init_params:
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
                if self.__pal_params[group]:
                    for name in self.__pal_params[group]:
                        value, typ = self.__pal_params[group][name]
                        if isinstance(value, (list, tuple)):
                            for val in value:
                                tpl = [tuple([group_val] + list(self.__map_param(name, val, typ)))]
                                param_rows.extend(tpl)
                        else:
                            tpl = [tuple([group_val] + list(self.__map_param(name, value, typ)))]
                            param_rows.extend(tpl)

        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        if holiday is None:
            holiday = HolidayTable()
        if self.massive is not True:
            model_tbl = '#PAL_ADDITIVE_MODEL_FORECAST_MODEL_TBL_{}_{}'.format(self.id, unique_id)
            outputs = [model_tbl]
            try:
                self._call_pal_auto(conn,
                                    'PAL_ADDITIVE_MODEL_ANALYSIS',
                                    data,
                                    holiday,
                                    ParameterTable().with_data(param_rows),
                                    *outputs)
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
        else:
            if not param_rows:
                param_rows = [('1', 'PLACE_HOLDER', None, None, 'place_holder')]

            model_tbl = '#PAL_MASSIVE_ADDITIVE_MODEL_FORECAST_MODEL_TBL_{}_{}'.format(self.id, unique_id)
            errormsg_tbl = '#PAL_MASSIVE_ADDITIVE_MODEL_FORECAST_ERROR_TBL_{}_{}'.format(self.id, unique_id)
            outputs = [model_tbl, errormsg_tbl]
            try:
                if check_pal_function_exist(conn, '%MASSIVE_ADDITIVE_MODEL%', like=True) or self._disable_hana_execution:
                    self._call_pal_auto(conn,
                                        'PAL_MASSIVE_ADDITIVE_MODEL_ANALYSIS',
                                        data,
                                        holiday,
                                        ParameterTable(itype=group_key_type).with_data(param_rows),
                                        *outputs)
                else:
                    msg = 'The version of your SAP HANA does not support massive AdditiveModelForecast!'
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

        self.model_ = conn.table(model_tbl)
        self.error_msg_ = None
        if self.massive is True:
            if not self._disable_hana_execution:
                self.error_msg_ = conn.table(errormsg_tbl)
                if not self.error_msg_.collect().empty:
                    row = self.error_msg_.count()
                    for i in range(1, row+1):
                        warn_msg = "For group_key '{}',".format(self.error_msg_.collect()['GROUP_ID'][i-1]) +\
                                   " the error message is '{}'.".format(self.error_msg_.collect()['MESSAGE'][i-1]) +\
                                   "More information could be seen in the attribute error_msg_!"
                        warnings.warn(message=warn_msg)

        return self

    @trace_sql
    def _predict(self,
                 data,
                 group_params,
                 predict_params,
                 group_key_type):

        conn = data.connection_context

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
        else: # massive mode
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

        show_explainer = False
        if predict_params.get('show_explainer'):
            show_explainer = predict_params['show_explainer']

        if self.massive is not True:
            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            result_tbl = "#PAL_ADDITIVE_MODEL_FORECAST_RESULT_TBL_{}_{}".format(self.id, unique_id)
            decompose_tbl = "#PAL_ADDITIVE_MODEL_FORECAST_DECOMPOSITION_TBL_{}_{}".format(self.id, unique_id)
            try:
                if show_explainer is not True:
                    self._call_pal_auto(conn,
                                        'PAL_ADDITIVE_MODEL_PREDICT',
                                        data,
                                        self.model_,
                                        ParameterTable().with_data(param_rows),
                                        result_tbl)
                else:
                    if check_pal_function_exist(conn, 'ADDITIVE_MODEL_EXPLAIN%', like=True) or self._disable_hana_execution:
                        self._call_pal_auto(conn,
                                            'PAL_ADDITIVE_MODEL_EXPLAIN',
                                            data,
                                            self.model_,
                                            ParameterTable().with_data(param_rows),
                                            result_tbl,
                                            decompose_tbl)
                    else:
                        msg = 'The version of SAP HANA does not support additive_model_forecast explainer. Please set show_explainer=False!'
                        logger.error(msg)
                        raise ValueError(msg)
            except dbapi.Error as db_err:
                msg = str(conn.hana_version())
                logger.exception("HANA version: %s. %s", msg, str(db_err))
                try_drop(conn, result_tbl)
                raise
            except pyodbc.Error as db_err:
                msg = str(conn.hana_version())
                logger.exception("HANA version: %s. %s", msg, str(db_err.args[1]))
                try_drop(conn, result_tbl)
                raise
            self.explainer_ = None
            if show_explainer is True:
                self.explainer_ = conn.table(decompose_tbl)
            return conn.table(result_tbl)

        # massive mode
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        result_tbl = "#PAL_MASSIVE_AMF_PREDICT_RESULT_TBL_{}_{}".format(self.id, unique_id)
        decompose_tbl = "#PAL_MASSIVE_AMF_PREDICT_DECOMPOSITION_TBL_{}_{}".format(self.id, unique_id)
        errormsg_tbl = "#PAL_MASSIVE_AMF_PREDICT_ERROR_TBL_{}_{}".format(self.id, unique_id)
        if not param_rows:
            param_rows = [('1', 'PLACE_HOLDER', None, None, 'place_holder')]
        try:
            if check_pal_function_exist(conn, 'MASSIVE_ADDITIVE_MODEL%', like=True) or self._disable_hana_execution:
                self._call_pal_auto(conn,
                                    'PAL_MASSIVE_ADDITIVE_MODEL_PREDICT',
                                    data,
                                    self.model_,
                                    ParameterTable(itype=group_key_type).with_data(param_rows),
                                    result_tbl,
                                    decompose_tbl,
                                    errormsg_tbl)
            else:
                msg = 'The version of SAP HANA does not support massive AdditiveModelForecast!'
                logger.error(msg)
                raise ValueError(msg)
        except dbapi.Error as db_err:
            msg = str(conn.hana_version())
            logger.exception("HANA version: %s. %s", msg, str(db_err))
            try_drop(conn, result_tbl)
            raise
        except pyodbc.Error as db_err:
            msg = str(conn.hana_version())
            logger.exception("HANA version: %s. %s", msg, str(db_err.args[1]))
            try_drop(conn, result_tbl)
            raise

        if not self._disable_hana_execution:
            self.explainer_ = conn.table(decompose_tbl)
            err_msg = conn.table(errormsg_tbl)
            if not err_msg.collect().empty:
                row = err_msg.count()
                for i in range(1, row+1):
                    warn_msg = "For group_key '{}',".format(err_msg.collect()['GROUP_ID'][i-1]) +\
                               " the error message is '{}'.".format(err_msg.collect()['MESSAGE'][i-1]) +\
                               "More information could be seen in the 2nd return Dataframe!"
                    warnings.warn(message=warn_msg)

        return conn.table(result_tbl), self.explainer_, err_msg

class AdditiveModelForecast(_AdditiveModelForecastBase):
    r"""
    Additive Model Forecast use a decomposable time series model with three main components: trend,
    seasonality, and holidays or event.

    Note that this function is a new function in SAP HANA SPS05 and Cloud.

    Parameters
    ----------

    growth : {'linear', 'logistic'}, optional

        Specify a trend, which could be either linear or logistic.

        Defaults to 'linear'.

    logistic_growth_capacity: float, optional

        Specify the carrying capacity for logistic growth.
        Mandatory and valid only when ``growth`` is 'logistic'.

        No default value.
    seasonality_mode : {'additive', 'multiplicative'}, optional

        Mode for seasonality, either additive or multiplicative.

        Defaults to 'additive'.
    seasonality : str or list of str, optional
        Add seasonality to model, is a json format, include:

          - NAME
          - PERIOD
          - FOURIER_ORDER
          - PRIOR_SCALE, optional
          - MODE, optional

        Each str is json format such as
        '{ "NAME": "MONTHLY", "PERIOD":30, "FOURIER_ORDER":5 }'.
        A seasonality parameter must include NAME, PERIOD, and FOURIER_ORDER elements.
        PRIOR_SCALE and MODE elements are optional.
        FOURIER_ORDER determines how quickly the seasonality can change.
        PRIOR_SCALE controls the amount of regularization.
        No seasonality will be added to the model if this parameter is not provided.

        No default value.

    num_changepoints : int, optional

        Number of potential changepoints.
        Not effective if ``changepoints`` is provided.

        Defaults to 25 if not provided.

    changepoint_range : float, optional

        Proportion of history in which trend changepoints will be estimated.

        Not effective if ``changepoints`` is provided.

        Defaults to 0.8.

    regressor : list of str, optional
        Specify the regressor, include:

          - NAME
          - PRIOR_SCALE
          - STANDARDIZE
          - MODE: "additive" or 'multiplicative'.

        Each str is json format such as
        '{ "NAME": "X1", "PRIOR_SCALE":4, "MODE": "additive" }'.
        PRIOR_SCALE controls for the amount of regularization;
        STANDARDIZE specifies whether or not the regressor is standardized.
        No default value.

    changepoints : list of str, optional,

        Specify a list of changepoints in the format of timestamp,
        such as ['2019-01-01 00:00:00, '2019-02-04 00:00:00']

        No default value.

    yearly_seasonality : {'auto', 'false', 'true'}, optional

        Specify whether or not to fit yearly seasonality.

        'false' and 'true' simply corresponds to their logical meaning,
        while 'auto' means automatically determined from the input data.

        Defaults to 'auto'.

    weekly_seasonality : {'auto', 'false', 'true'}, optional

        Specify whether or not to fit the weekly seasonality.

        'auto' means automatically determined from input data.

        Defaults to 'auto'.

    daily_seasonality : {'auto', 'false', 'true'}, optional

        Specify whether or not to fit the daily seasonality.

        'auto' means automatically determined from input data.

        Defaults to 'auto'.

    seasonality_prior_scale : float, optional

        Parameter modulating the strength of the seasonality model.

        Defaults to 10 if not provided.

    holiday_prior_scale : float, optional

        Parameter modulating the strength of the holiday components model.

        Defaults to 10 if not provided.

    changepoint_prior_scale : float, optional

        Parameter modulating the flexibility of the automatic changepoint selection.

        Defaults to 0.05 if not provided.

    massive : bool, optional
        Specifies whether or not to activate massive mode.

        For parameter setting in massive mode, you could use both
        group_params (please see the example below) or the original parameters.
        Using original parameters will apply for all groups.
        However, if you define some parameters of a group,
        the value of all original parameter setting will be not applicable to such group.

        An example is as follows:

        .. only:: latex

            >>> amf = AdditiveModelForecast(massive=True,
                                            changepoint_prior_scale=0.06,
                                            group_params={'Group_1': {'seasonality_mode':'additive'}})

        .. raw:: html

            <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                src="../_static/amf_init_example1.html" width="100%" height="100%">
            </iframe>

        In this example, as 'seasonality_mode' is set in group_params for Group_1,
        parameter setting of 'changepoint_prior_scale' is not applicable to Group_1.

        Defaults to False.

    group_params : dict, optional
        If massive mode is activated (``massive`` is True), input data is divided into different
        groups with different parameters applied.

        An example with group_params is as follows:

        .. only:: latex

            >>> amf = AdditiveModelForecast(massive=True,
                                            group_params={'Group_1': {'seasonality_mode':'additive'},
                                                          'Group_2': {'seasonality_mode':'multiplicative'}})

        .. raw:: html

            <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                src="../_static/amf_init_example2.html" width="100%" height="100%">
            </iframe>

        Valid only when ``massive`` is True and defaults to None.

    References
    ----------
    :ref:`Seasonalities in Additive Model Forecast<amf_season-label>`

    Attributes
    ----------

    model_ : DataFrame

        Model content.

    explainer_ : DataFrame

        The decomposition of trend, seasonal, holiday and exogenous variables.

          - In non-massive mode, only contains value when ``show_explainer=True`` in the predict function.
          - In massive mode, this attribute always contains value.

    error_msg_ :  DataFrame

        Error message and only valid if ``massive=True`` when creating an 'AdditiveModelForecast' instance.

    Examples
    --------

    Input dataframe df_fit:

    >>> df_fit.head(5).collect()
            ts         y
    2007-12-10  9.590761
    2007-12-11  8.519590
    2007-12-12  8.183677
    2007-12-13  8.072467
    2007-12-14  7.893572

    Create an Additive Model Forecast model:

    >>> amf = additive_model_forecast.AdditiveModelForecast(growth='linear')

    Perform fit on the given data:

    >>> amf.fit(data=df_fit)

    Expected output:

    >>> amf.model_.collect()
       ROW_INDEX                                      MODEL_CONTENT
    0          0  {"GROWTH":"linear","FLOOR":0.0,"SEASONALITY_MO...

    Perform predict on the model:

    Input dataframe df_predict for prediction:

    >>> df_predict.head(5).collect()
                ts    y
    0   2008-03-09  0.0
    1   2008-03-10  0.0
    2   2008-03-11  0.0
    3   2008-03-12  0.0
    4   2008-03-13  0.0

    >>> result = amf.predict(data=df2)

    Expected output:

    >>> result.collect()
                ts      YHAT  YHAT_LOWER  YHAT_UPPER
    0   2008-03-09  7.676880    6.930349    8.461546
    1   2008-03-10  8.147574    7.387315    8.969112
    2   2008-03-11  7.410452    6.630115    8.195562
    3   2008-03-12  7.198807    6.412776    7.977391
    4   2008-03-13  7.087702    6.310826    7.837083

    If you want to see the decomposed result of predict result, you could set show_explainer = True:

    >>> result = amf.predict(df_predict,
                             show_explainer=True,
                             decompose_seasonality=False,
                             decompose_holiday=False)

    Show the ``explainer_``:

    >>> amf.explainer_.head(5).collect()
                ts     TREND                                SEASONAL HOLIDAY EXOGENOUS
    0   2008-03-09  7.432172   {"seasonalities":0.24470822257259804}      {}        {}
    1   2008-03-10  7.390030     {"seasonalities":0.757544365973254}      {}        {}
    2   2008-03-11  7.347887   {"seasonalities":0.06256440574150749}      {}        {}
    3   2008-03-12  7.305745  {"seasonalities":-0.10693834906369426}      {}        {}
    4   2008-03-13  7.263603  {"seasonalities":-0.17590059499681369}      {}        {}

    """
    def fit(self,
            data,
            key=None,
            endog=None,
            exog=None,
            holiday=None,
            group_key=None,
            group_params=None,
            categorical_variable=None):
        r"""
        Additive model forecast fit function.

        Parameters
        ----------

        data : DataFrame

            Input data. The structure is as follows.

            - The first column: index (ID), type TIMESTAMP, SECONDDATE or DATE.
            - The second column: raw data, type INTEGER or DECIMAL(p,s).
            - Other columns: external data, type INTEGER, DOUBLE or DECIMAL(p,s).

        key : str, optional

            The timestamp column of data. The type of key column is TIMESTAMP, SECONDDATE, or DATE.

            In single mode, defaults to the first column of data if the index column of data is
            not provided; otherwise, defaults to the index column of data.

            In massive mode, defaults to the first-non group key column of data if the index columns
            of data is not provided; otherwise, defaults to the second of index columns of data and
            the first column of index columns is group_key.

        endog : str, optional

            The endogenous variable, i.e. time series. The type of endog column is
            INTEGER, DOUBLE, or DECIMAL(p, s).

            - In single mode, defaults to the first non-key column.
            - In massive mode, defaults to the first non group_key, non key column.

        exog : str or a list of str, optional

            An optional array of exogenous variables. The type of exog column is INTEGER, DOUBLE, or DECIMAL(p, s).

            Defaults to None. Please set this parameter explicitly if you have exogenous variables.

        holiday : DataFrame, optional

            Input holiday data. The structure is as follows.

            - 1st column : timestamp/key, TIMESTAMP, SECONDDATE, DATE
            - 2nd column : holiday name, VARCHAR, NVARCHAR
            - 3rd column : lower window of holiday, less than 0, INTEGER, optional
            - 4th column : upper window of holiday, greater than 0, INTEGER, optional

            if ``massive`` is True, the structure of input holiday data is as follows:

            - 1st column: group_key, INTEGER, VRACHAR or NVARCHAR
            - 2nd column: timestamp/key, TIMESTAMP, SECONDDATE, DATE
            - 3rd column : holiday name, VARCHAR, NVARCHAR
            - 4th column : lower window of holiday, less than 0, INTEGER, optional
            - 3th column : upper window of holiday, greater than 0, INTEGER, optional

            Defaults to None.

        group_key : str, optional
            The column of group_key. Data type can be INT or NVARCHAR/VARCHAR.
            If data type is INT, only parameters set in the group_params are valid.

            This parameter is only valid when `self.massive` is True.

            Defaults to the first column of data if the index columns of data is not provided.
            Otherwise, defaults to the first column of index columns.

        group_params : dict, optional
            If massive mode is activated (``massive`` is True), input data is divided into different
            groups with different parameters applied.

            An example with group_params is as follows:

            .. raw:: html

                <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                    src="../_static/amf_fit_example.html" width="100%" height="100%">
                </iframe>

            Valid only when `self.massive` is True.

            Defaults to None.

        categorical_variable : str or ist of str, optional

            Specifies INTEGER columns specified that should be be treated as categorical.

            Other INTEGER columns will be treated as continuous.

            Defaults to None.

        Returns
        -------
        A fitted object of class "AdditiveModelForecast".
        """
        setattr(self, 'hanaml_fit_params', pal_param_register())

        group_params = {} if group_params is None else group_params
        if group_params:
            for group in group_params:
                self._arg('Parameters with group_key ' + str(group),
                          group_params[group], dict)
        group_key_type = None
        group_id = []
        key = self._arg('key', key, str)
        endog = self._arg('endog', endog, str)
        if isinstance(exog, str):
            exog = [exog]
        exog = self._arg('exog', exog, ListOfStrings)
        if self.massive is True:
            cols = data.columns
            group_key = self._arg('group_key', group_key, str)
            index = data.index
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
            if index is not None:
                key = _col_index_check(key, 'key', index[1], cols)
            else:
                if key is None:
                    key = cols[0]
            endog, exog = _validate_og(key, endog, exog, cols)
            data_ = data[group_id + [key] + [endog] + exog]
        else: # single mode
            if not self._disable_hana_execution:
                cols = data.columns
                index = data.index
                if index is not None:
                    key = _col_index_check(key, 'key', index, cols)
                else:
                    if key is None:
                        key = cols[0]
                endog, exog = _validate_og(key, endog, exog, cols)
                data_ = data[[key] + [endog] + exog]
            else:
                data_ = data
        self.fit_data = data_
        super(AdditiveModelForecast, self)._fit(data_, holiday, group_params, categorical_variable, group_key_type)
        return self

    def predict(self,
                data,
                key=None,
                exog=None,
                group_key=None,
                group_params=None,
                logistic_growth_capacity=None,
                interval_width=None,
                uncertainty_samples=None,
                show_explainer=False,
                decompose_seasonality=None,
                decompose_holiday=None):
        """
        Makes time series forecast based on the estimated Additive Model Forecast model.

        Parameters
        ----------

        data : DataFrame, optional

            Index and exogenous variables for forecast.
            The structure is as follows.

              - First column: Index (ID), type TIMESTAMP, SECONDDATE or DATE.
              - Second column: Placeholder column for forecast values, type DOUBLE or DECIMAL(p,s).
              - Other columns : external data, type INTEGER, DOUBLE or DECIMAL(p,s).

            if massive is True, the structure of data is as follows:

              - First column: Group_key, type INTEGER, VRACHAR or NVARCHAR.
              - Second column: Index (ID), type TIMESTAMP, SECONDDATE or DATE.
              - Third column : Placeholder column for forecast values, type DOUBLE or DECIMAL(p,s).
              - Other columns: external data, type INTEGER, DOUBLE or DECIMAL(p,s).

        key : str, optional

            The timestamp column of data. The data type of key column should be
            TIMESTAMP, DATE or SECONDDATE.

            In single mode, defaults to the first column of data if the index column of data is not provided.
            Otherwise, defaults to the index column of data.

            In massive mode, defaults to the first-non group key column of data
            if the index columns of data is not provided; otherwise, defaults to
            the second of index columns of data and the first column of index columns is group_key.

        group_key : str, optional
            The column of group_key. Data type can be INT or NVARCHAR/VARCHAR.
            If data type is INT, only parameters set in the group_params are valid.

            This parameter is only valid when ``massive`` is True.

            Defaults to the first column of data if the index columns of data is not provided.
            Otherwise, defaults to the first column of index columns.

        group_params : dict, optional
            If massive mode is activated (``massive`` is True), input data is divided into different
            groups with different parameters applied.

            An example with ``group_params`` is as follows:

            .. only:: latex

                >>> amf = AdditiveModelForecast(massive=True)
                >>> res = amf.fit(data=train_df).predict(group_params={'Group_1': {'interval_width':0.5},
                                                                       'Group_2': {'interval_width':0.6}})

            .. raw:: html

                <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                    src="../_static/amf_predict_example.html" width="100%" height="100%">
                </iframe>

            Valid only when ``massive`` is True and defaults to None.

        logistic_growth_capacity: float, optional

            specify the carrying capacity for logistic growth.
            Mandatory and valid only when ``growth`` is 'logistic'.

            Defaults to None.
        interval_width : float, optional

            Width of the uncertainty intervals.

            Defaults to 0.8.

        uncertainty_samples : int, optional

            Number of simulated draws used to estimate uncertainty intervals.

            Defaults to 1000.

        show_explainer : bool, optional
            Indicate whether to invoke the AdditiveModelForecast with explanations function in the predict.
            If true, the contributions of trend, seasonal, holiday and exogenous variables are
            shown in a attribute called ``explainer_`` of the AdditiveModelForecast instance.

            Defaults to False.

        decompose_seasonality : bool, optional
            Specify whether or not seasonal component will be decomposed.
            Valid only when ``show_explainer`` is True.

            Defaults to False.

        decompose_holiday : bool, optional
            Specify whether or not holiday component will be decomposed.
            Valid only when ``show_explainer`` is True.

            Defaults to False.

        Returns
        -------

        DataFrame 1
            Forecasted values, structured as follows:

            - ID, type timestamp.
            - YHAT, type DOUBLE, forecast value.
            - YHAT_LOWER, type DOUBLE, lower bound of confidence region.
            - YHAT_UPPER, type DOUBLE, higher bound of confidence region.

        DataFrame 2
            The decomposition of trend, seasonal, holiday and exogenous variables.
            Only available in the massive mode.

        DataFrame 3
            Error message for each group.
            Only available in the massive mode.

        """
        if getattr(self, 'model_', None) is None:
            raise FitIncompleteError("Model not initialized. Perform a fit first.")

        group_params = {} if group_params is None else group_params
        if group_params:
            for group in group_params:
                self._arg('Parameters with group_key ' + str(group),
                          group_params[group], dict)

        predict_params = {'logistic_growth_capacity' : logistic_growth_capacity,
                          'interval_width' : interval_width,
                          'uncertainty_samples' : uncertainty_samples,
                          'show_explainer' : show_explainer,
                          'decompose_seasonality' : decompose_seasonality if show_explainer is True else None,
                          'decompose_holiday' : decompose_holiday if show_explainer is True else None}

        predict_params = _delete_none_key_in_dict(predict_params)

        index = data.index
        cols = data.columns
        group_key_type = None
        group_id = []
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
            msg = "Please select key from {}!".format(cols)
            logger.error(msg)
            raise ValueError(msg)
        cols.remove(key)
        exog = cols
        data_ = data[group_id + [key] + exog]
        self.predict_data = data_

        return super(AdditiveModelForecast, self)._predict(data_,
                                                           group_params,
                                                           predict_params,
                                                           group_key_type)
