"""
This module supports to run PAL functions in a pipeline manner.
"""

#pylint: disable=invalid-name
#pylint: disable=eval-used
#pylint: disable=unused-variable
#pylint: disable=line-too-long
#pylint: disable=too-many-locals
#pylint: disable=too-many-branches
#pylint: disable=consider-using-f-string
#pylint: disable=protected-access
#pylint: disable=consider-iterating-dictionary
#pylint: disable=too-many-instance-attributes

import json
import logging
import re
import uuid
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from hana_ml.ml_base import ListOfStrings
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.algorithms.pal.pal_base import (
    PALBase,
    ParameterTable,
    try_drop
)
from hana_ml.algorithms.pal.sqlgen import trace_sql
from hana_ml.algorithms.pal.utility import mlflow_autologging
from hana_ml.visualizers.digraph import Digraph
from hana_ml.algorithms.pal.neural_network import MLPClassifier, MLPRegressor
from hana_ml.algorithms.pal.svm import SVC, SVR
from hana_ml.algorithms.pal.tsa.auto_arima import AutoARIMA
from hana_ml.algorithms.pal.tsa.exponential_smoothing import (
    AutoExponentialSmoothing,
    SingleExponentialSmoothing,
    DoubleExponentialSmoothing,
    TripleExponentialSmoothing,
    BrownExponentialSmoothing
)
from hana_ml.algorithms.pal.tsa.additive_model_forecast import AdditiveModelForecast
from hana_ml.algorithms.pal.tsa.bsts import BSTS
from hana_ml.algorithms.pal.tsa.outlier_detection import OutlierDetectionTS

logger = logging.getLogger(__name__)#pylint: disable=invalid-name

class Pipeline(PALBase): #pylint: disable=useless-object-inheritance
    """
    Pipeline construction to run transformers and estimators sequentially.

    Parameters
    ----------

    step : list
        List of (name, transform) tuples that are chained. The last object should be an estimator.
    """
    def __init__(self, steps):
        super(Pipeline, self).__init__()
        self.steps = steps
        self.nodes = []
        self.pipeline = None
        self.predict_info_ = None
        self.info_ = None
        self.use_pal_pipeline_fit = None
        self._is_autologging = False
        self._autologging_model_storage_schema = None
        self._autologging_model_storage_meta = None
        self.is_exported = False
        self.registered_model_name = None
        self.report = None

    def enable_mlflow_autologging(self, schema=None, meta=None, is_exported=False, registered_model_name=None):
        """
        It will enable mlflow autologging. Only works for fit function.

        Parameters
        ----------
        schema : str, optional
            Define the model storage schema for mlflow autologging.

            Defaults to the current schema.
        meta : str, optional
            Define the model storage meta table for mlflow autologging.

            Defaults to 'HANAML_MLFLOW_MODEL_STORAGE'.
        is_exported : bool, optional
            Determine whether export the HANA model to mlflow.

            Defaults to False.
        registered_model_name : str, optional
            MLFlow registered_model_name.
        """
        self._is_autologging = True
        self._autologging_model_storage_schema = schema
        self._autologging_model_storage_meta = meta
        self.is_exported = is_exported
        self.registered_model_name = registered_model_name

    def disable_mlflow_autologging(self):
        """
        It will disable mlflow autologging.
        """
        self._is_autologging = False

    def fit_transform(self, data, fit_params=None):
        """
        Fit all the transforms one after the other and transform the
        data, then fit the transformed data using the final estimator.

        Parameters
        ----------

        data : DataFrame
            SAP HANA DataFrame to be transformed in the pipeline.
        fit_params : dict
            The parameters corresponding to the transformers/estimator name
            where each parameter name is prefixed such that parameter p for step s has key s__p.

        Returns
        -------

        DataFrame
            Transformed SAP HANA DataFrame.

        Examples
        --------

        >>> my_pipeline = Pipeline([
                ('pca', PCA(scaling=True, scores=True)),
                ('imputer', Imputer(strategy='mean'))
                ])
        >>> fit_params = {'pca__key': 'ID', 'pca__label': 'CLASS'}
        >>> my_pipeline.fit_transform(data=train_data, fit_params=fit_params)

        """
        data_ = data
        count = 0
        if fit_params is None:
            fit_params = {}
        for step in self.steps:
            fit_param_str = ''
            m_fit_params = {}
            for param_key, param_val in fit_params.items():
                if "__" not in param_key:
                    raise ValueError("The parameter name format incorrect. The parameter name is prefixed such that parameter p for step s has key s__p.")
                step_marker, param_name = param_key.split("__")
                if step[0] in step_marker:
                    m_fit_params[param_name] = param_val
                    fit_param_str = fit_param_str + ",\n" + param_name + "="
                    if isinstance(param_val, str):
                        fit_param_str = fit_param_str + "'{}'".format(param_val)
                    else:
                        fit_param_str = fit_param_str + str(param_val)
            data_ = step[1].fit_transform(data_, **m_fit_params)
            self.nodes.append((step[0],
                               "{}.fit_transform(data={}{})".format(_get_obj(step[1]),
                                                                    repr(data_),
                                                                    fit_param_str),
                               [str(count)],
                               [str(count + 1)]))
            count = count + 1
        return data_

    @mlflow_autologging(logtype='pal_fit')
    @trace_sql
    def fit(self, data,
            key=None,
            features=None,
            label=None,
            fit_params=None,
            categorical_variable=None,
            generate_json_pipeline=False,
            use_pal_pipeline_fit=True,
            endog=None,
            exog=None,
            model_table_name=None):
        """
        Fit all the transforms one after the other and transform the
        data, then fit the transformed data using the final estimator.

        Parameters
        ----------
        data : DataFrame
            SAP HANA DataFrame to be transformed in the pipeline.
        key : str, optional
            Name of the ID column.

            If ``key`` is not provided, then:

                - if ``data`` is indexed by a single column, then ``key`` defaults
                  to that index column;

                - otherwise, it is assumed that ``data`` contains no ID column.

        features : list of str, optional
            Names of the feature columns.

            If ``features`` is not provided, it defaults to all non-ID, non-label columns.

        label : str, optional
            Name of the dependent variable.

            Defaults to the name of the last non-ID column.
        fit_params : dict, optional
            Parameters corresponding to the transformers/estimator name
            where each parameter name is prefixed such that parameter p for step s has key s__p.
        categorical_variable : str or list of str, optional
            Specify INTEGER column(s) that should be be treated as categorical data.
            Other INTEGER columns will be treated as continuous.
        generate_json_pipeline : bool, optional
            Help generate json formatted pipeline.

            Defaults to False.
        use_pal_pipeline_fit : bool, optional
            Use PAL's pipeline fit function instead of the original chain execution.

            Defaults to True.
        endog : str, optional
            Specifies the endogenous variable in time-series data.
            Please use ``endog`` instead of ``label`` if ``data`` is time-series data.

            Defaults to the name of 1st non-key column in ``data``.
        exog : ListOfStrings or str, optional
            Specifies the exogenous variables in time-series data.
            Please use ``exog`` instead of ``features`` if ``data`` is time-series data.

            Defaults to

              - the list of names of all non-key, non-endog columns in ``data`` if final estimator
                is not ExponentialSmoothing based
              - [] otherwise.
        model_table_name : str, optional
            Specifies the HANA model table name instead of the generated temporary table.

            Defaults to None.

        Returns
        -------
        DataFrame
            Transformed SAP HANA DataFrame.

        Examples
        --------

        >>> my_pipeline = Pipeline([
            ('pca', PCA(scaling=True, scores=True)),
            ('imputer', Imputer(strategy='mean')),
            ('hgbt', HybridGradientBoostingClassifier(
            n_estimators=4, split_threshold=0, learning_rate=0.5, fold_num=5,
            max_depth=6, cross_validation_range=cv_range))
            ])
        >>> fit_params = {'pca__key': 'ID',
                          'pca__label': 'CLASS',
                          'hgbt__key': 'ID',
                          'hgbt__label': 'CLASS',
                          'hgbt__categorical_variable': 'CLASS'}
        >>> hgbt_model = my_pipeline.fit(data=train_data, fit_params=fit_params)
        """
        self.use_pal_pipeline_fit = use_pal_pipeline_fit
        expsm_estimators = [SingleExponentialSmoothing, DoubleExponentialSmoothing,
                            TripleExponentialSmoothing, BrownExponentialSmoothing,
                            AutoExponentialSmoothing]
        ts_estimators = [AutoARIMA, AdditiveModelForecast, BSTS] + expsm_estimators
        type_ts = any(isinstance(self.steps[-1][1], ts_est) for ts_est in ts_estimators)
        if type_ts:
            features, label = exog, endog
        expsm_flag = isinstance(self.steps[-1][1], tuple(expsm_estimators))
        features = [] if expsm_flag else features
        if not use_pal_pipeline_fit:
            data_ = data.rearrange(key=key, features=features, label=label,
                                   type_ts=type_ts)
        else:
            data_ = data
        conn = data_.connection_context
        count = 0
        if fit_params is None:
            fit_params = {}
        obj = None
        for step in self.steps:
            fit_param_str = ''
            m_fit_params = {}
            for param_key, param_val in fit_params.items():
                if "__" not in param_key:
                    raise ValueError("The parameter name format incorrect. The parameter name is prefixed such that parameter p for step s has key s__p.")
                step_marker, param_name = param_key.split("__")
                if step[0] in step_marker:
                    m_fit_params[param_name] = param_val
                    fit_param_str = fit_param_str + ",\n" + param_name + "="
                    if isinstance(param_val, str):
                        fit_param_str = fit_param_str + "'{}'".format(param_val)
                    else:
                        fit_param_str = fit_param_str + str(param_val)
            obj = step[1]
            if count < len(self.steps) - 1:
                if use_pal_pipeline_fit:
                    obj.disable_hana_execution()
                if not isinstance(obj, OutlierDetectionTS):
                    data_ = obj.fit_transform(data_, **m_fit_params)
                    self.nodes.append((step[0],
                                       "{}.fit_transform(data={}{})".format(_get_obj(obj),
                                                                            repr(data_),
                                                                            fit_param_str),
                                       [str(count)],
                                       [str(count + 1)]))
                else:
                    data_ = obj.fit_predict(data_, **m_fit_params)
                    self.nodes.append((step[0],
                                       "{}.fit_predict(data={}{})".format(_get_obj(obj),
                                                                            repr(data_),
                                                                            fit_param_str),
                                       [str(count)],
                                       [str(count + 1)]))
            else:
                if use_pal_pipeline_fit:
                    obj.disable_hana_execution()
                if expsm_flag:
                    obj.fit_predict(data_, **m_fit_params)
                else:
                    obj.fit(data_, **m_fit_params)
                fit_func = 'fit_predict' if expsm_flag else 'fit'
                self.nodes.append((step[0],
                                   "{}.{}(data={}{})".format(_get_obj(obj),
                                                             fit_func,
                                                             repr(data_),
                                                             fit_param_str),
                                   [str(count)],
                                   [str(count + 1)]))
            count = count + 1
        if generate_json_pipeline and not use_pal_pipeline_fit:
            self.generate_json_pipeline()
        if use_pal_pipeline_fit:
            self.generate_json_pipeline()
            categorical_variable = self._arg('categorical_variable',
                                             categorical_variable,
                                             ListOfStrings)
            pipeline_param = [('HAS_ID', key is not None, None, None)]
            if categorical_variable is not None:
                pipeline_param.extend([('CATEGORICAL_VARIABLE', None, None, var) for var in categorical_variable])
            if isinstance(self.pipeline, dict):
                pipeline = json.dumps(self.pipeline)
            else:
                pipeline = self.pipeline
            pipeline_param.extend([('PIPELINE', None, None, pipeline)])
            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            outputs = ['MODEL', 'INFO']
            outputs = ['#PAL_PIPELINE_{}_TBL_{}_{}'.format(name, self.id, unique_id) for name in outputs]
            if model_table_name:
                outputs[0] = model_table_name
            model_tbl, info_tbl = outputs
            try:
                self._call_pal_auto(conn,
                                    'PAL_PIPELINE_FIT',
                                    data.rearrange(key=key, features=features,
                                                   label=label, type_ts=type_ts),
                                    ParameterTable().with_data(pipeline_param),
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
            self.info_ = conn.table(info_tbl)
        return self

    def predict(self, data, key=None, features=None, model=None):
        r"""
        Predict function for AutoML.

        Parameters
        ----------
        data :  DataFrame
            Data to be predicted.

        key : str, optional

            Name of the ID column.

            Mandatory if ``data`` is not indexed, or is indexed by multiple columns.

            Defaults to the index of ``data`` if ``data`` is indexed by a single column.

        features : list of str, optional

            Names of the feature columns.

            If ``features`` is not provided, it defaults to all non-ID columns.

        model : DataFrame, optional
            The model to be used for prediction.

            Defaults to the fitted model (model\_).

        Returns
        -------
        DataFrame
            Predicted result, structured as follows:

              - 1st column: Data type and name same as the 1st column of ``data``.
              - 2nd column: SCORE, predicted values(for regression) or class labels(for classification).
        """
        conn = data.connection_context
        if model is None:
            if getattr(self, 'model_', None) is None:
                msg = ('Model not initialized. Perform a fit first.')
                logger.error(msg)
                raise FitIncompleteError(msg)
            if isinstance(self.model_, (list, tuple)):
                model = self.model_[0]
            else:
                model = self.model_

        data_ = data.rearrange(key=key, features=features)

        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        outputs = ['RESULT', 'INFO']
        outputs = ['#PAL_PIPELINE_{}_RESULT_TBL_{}_{}'.format(name, self.id, unique_id)
                   for name in outputs]
        result_tbl, info_tbl = outputs
        param_rows = []
        try:
            self._call_pal_auto(conn,
                                'PAL_PIPELINE_PREDICT',
                                data_,
                                model,
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
        result_df = conn.table(result_tbl)
        self.predict_info_ = conn.table(info_tbl)
        return result_df

    def fit_predict(self, data, apply_data=None, fit_params=None, predict_params=None):
        """
        Fit all the transforms one after the other and transform the
        data, then fit_predict the transformed data using the last estimator.

        Parameters
        ----------
        data : DataFrame
            SAP HANA DataFrame to be transformed in the pipeline.
        apply_data : DataFrame
            SAP HANA DataFrame to be predicted in the pipeline.
        fit_params : dict, optional
            Parameters corresponding to the transformers/estimator name
            where each parameter name is prefixed such that parameter p for step s has key s__p.
        predict_params : dict, optional
            Parameters corresponding to the predictor name
            where each parameter name is prefixed such that parameter p for step s has key s__p.

        Returns
        -------
        DataFrame
            Transformed SAP HANA DataFrame.

        Examples
        --------

        >>> my_pipeline = Pipeline([
            ('pca', PCA(scaling=True, scores=True)),
            ('imputer', Imputer(strategy='mean')),
            ('hgbt', HybridGradientBoostingClassifier(
            n_estimators=4, split_threshold=0, learning_rate=0.5, fold_num=5,
            max_depth=6, cross_validation_range=cv_range))
            ])
        >>> fit_params = {'pca__key': 'ID',
                          'pca__label': 'CLASS',
                          'hgbt__key': 'ID',
                          'hgbt__label': 'CLASS',
                          'hgbt__categorical_variable': 'CLASS'}
        >>> hgbt_model = my_pipeline.fit_predict(data=train_data, apply_data=test_data, fit_params=fit_params)
        """
        data_ = data
        if apply_data:
            apply_data_ = apply_data
        count = 0
        if fit_params is None:
            fit_params = {}
        if predict_params is None:
            predict_params = {}
        for step in self.steps:
            fit_param_str = ''
            m_fit_params = {}
            m_predict_params = {}
            for param_key, param_val in fit_params.items():
                if "__" not in param_key:
                    raise ValueError("The parameter name format incorrect. The parameter name is prefixed such that parameter p for step s has key s__p.")
                step_marker, param_name = param_key.split("__")
                if step[0] in step_marker:
                    m_fit_params[param_name] = param_val
                    fit_param_str = fit_param_str + ",\n" + param_name + "="
                    if isinstance(param_val, str):
                        fit_param_str = fit_param_str + "'{}'".format(param_val)
                    else:
                        fit_param_str = fit_param_str + str(param_val)
            predit_param_str = ''
            for param_key, param_val in predict_params.items():
                if "__" not in param_key:
                    raise ValueError("The parameter name format incorrect. The parameter name is prefixed such that parameter p for step s has key s__p.")
                step_marker, param_name = param_key.split("__")
                if step[0] in step_marker:
                    m_predict_params[param_name] = param_val
                    predit_param_str = predit_param_str + ",\n" + param_name + "="
                    if isinstance(param_val, str):
                        predit_param_str = predit_param_str + "'{}'".format(param_val)
                    else:
                        predit_param_str = predit_param_str + str(param_val)
            if count < len(self.steps) - 1:
                data_ = step[1].fit_transform(data_, **m_fit_params)
                apply_data_ = step[1].fit_transform(apply_data_, **m_predict_params)
                self.nodes.append((step[0],
                                   "{}\n.fit_transform(data={}{})".format(_get_obj(step[1]),
                                                                          repr(data_),
                                                                          fit_param_str),
                                   [str(count)],
                                   [str(count + 1)]))
            else:
                expsm_estimators = [SingleExponentialSmoothing, DoubleExponentialSmoothing,
                                    TripleExponentialSmoothing, BrownExponentialSmoothing,
                                    AutoExponentialSmoothing]
                expsm_flag = isinstance(step[1], tuple(expsm_estimators))
                if expsm_flag:
                    m_fit_predict_params = m_fit_params
                    m_fit_predict_params.update(m_predict_params)
                    data_ = step[1].fit_predict(data_, **m_fit_predict_params)
                    fit_predict_param_str = fit_param_str + ", " + predit_param_str[2:]
                    self.nodes.append((step[0],
                                      "{}\n.fit_predict(data={}{})".format(_get_obj(step[1]),
                                                                           repr(data_),
                                                                           fit_predict_param_str),
                                      [str(count)],
                                      [str(count + 1)]))
                else:
                    if apply_data:
                        data_ = step[1].fit(data_, **m_fit_params).predict(apply_data_, **m_predict_params)
                    else:
                        data_ = step[1].fit(data_, **m_fit_params).predict(**m_predict_params)
                    if apply_data:
                        apply_param_str = repr(apply_data_) + ", " + predit_param_str[2:]
                    else:
                        apply_param_str = predit_param_str[2:]
                    self.nodes.append((step[0],
                                      "{}\n.fit(data={}{})\n.predict({})".format(_get_obj(step[1]),
                                                                                 repr(data_),
                                                                                 fit_param_str,
                                                                                 apply_param_str),
                                      [str(count)],
                                      [str(count + 1)]))
            count = count + 1
        return data_

    def plot(self, name="my_pipeline", iframe_height=450):
        """
        Plot pipeline.
        """
        digraph = Digraph(name)
        node = []
        for elem in self.nodes:
            node.append(digraph.add_python_node(elem[0],
                                                elem[1],
                                                in_ports=elem[2],
                                                out_ports=elem[3]))
        for node_x in range(0, len(node) - 1):
            digraph.add_edge(node[node_x].out_ports[0],
                             node[node_x + 1].in_ports[0])
        digraph.build()
        digraph.generate_notebook_iframe(iframe_height)

    def generate_json_pipeline(self):
        """
        Generate the json formatted pipeline for auto-ml's pipeline_fit function.
        """
        inputs = "ROWDATA"
        uni_mlp_mapping = {"HIDDEN_LAYER_ACTIVE_FUNC": "ACTIVATION",
                           "HIDDEN_LAYER_ACTIVE_FUNC_VALUES": "ACTIVATION_OPTIONS",
                           "HIDDEN_LAYER_SIZE_VALUES": "HIDDEN_LAYER_SIZE_OPTIONS",
                           "MAX_ITERATION": "MAX_ITER",
                           "MINI_BATCH_SIZE": "BATCH_SIZE",
                           "MINI_BATCH_SIZE_VALUES": "BATCH_SIZE_VALUES",
                           "MINI_BATCH_SIZE_RANGE": "BATCH_SIZE_RANGE",
                           "MOMENTUM_FACTOR": "MOMENTUM",
                           "MOMENTUM_FACTOR_VALUES": "MOMENTUM_VALUES",
                           "MOMENTUM_FACTOR_RANGE": "MOMENTUM_RANGE",
                           "OUTPUT_LAYER_ACTIVE_FUNC": "OUTPUT_ACTIVATION",
                           "OUTPUT_LAYER_ACTIVE_FUNC_VALUES": "OUTPUT_ACTIVATION_OPTIONS"}
        uni_svm_mapping = { "ERROR_TOL": "TOL"}
        for step in self.steps:
            new_inputs = {}
            params = {}
            try:
                fit_args = step[1].get_parameters()["fit"]
            except KeyError:
                fit_args = {}
            for args in fit_args:
                arg_key = args[0]
                if self.use_pal_pipeline_fit:
                    if args[0] == 'HAS_ID':
                        continue
                    if args[0] == 'CATEGORICAL_VARIABLE':
                        continue
                    if args[0] == 'KEY':
                        continue
                    if args[0] == 'DEPENDENT_VARIABLE':
                        continue
                    if args[0] == 'LABEL':
                        continue
                    if isinstance(step[1], (MLPClassifier, MLPRegressor)):
                        if args[0] in uni_mlp_mapping.keys():
                            arg_key = uni_mlp_mapping[args[0]]
                    if isinstance(step[1], (SVC, SVR)):
                        if args[0] in uni_svm_mapping.keys():
                            arg_key = uni_svm_mapping[args[0]]
                params[arg_key] = args[1]
            new_inputs["args"] = params
            new_inputs["inputs"] = {"data": inputs}
            inputs = {}
            if self.use_pal_pipeline_fit:
                inputs[step[1].op_name] = new_inputs
            else:
                inputs[step[0]] = new_inputs
        self.pipeline = json.dumps(inputs)
        return self.pipeline

def _get_obj(obj):
    tmp_mem = []
    for key, val in obj.hanaml_parameters.items():
        if val is not None:
            tmp_mem.append("{}={}".format(key, val))
    return "{}({})".format(re.findall('\'([^$]*)\'', str(obj.__class__))[0], ",\n".join(tmp_mem))
