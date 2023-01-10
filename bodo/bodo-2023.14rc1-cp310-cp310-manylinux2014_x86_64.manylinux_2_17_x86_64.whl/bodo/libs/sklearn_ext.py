"""Support scikit-learn using object mode of Numba """
import itertools
import numbers
import sys
import types as pytypes
import warnings
from itertools import combinations
import numba
import numpy as np
import pandas as pd
import sklearn.cluster
import sklearn.ensemble
import sklearn.feature_extraction
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection
import sklearn.naive_bayes
import sklearn.svm
import sklearn.utils
from mpi4py import MPI
from numba.core import types
from numba.extending import overload, overload_attribute, overload_method, register_jitable
from scipy import stats
from scipy.special import comb
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.metrics import hinge_loss, log_loss, mean_squared_error
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing._data import _handle_zeros_in_scale as sklearn_handle_zeros_in_scale
from sklearn.utils._encode import _unique
from sklearn.utils.extmath import _safe_accumulator_op as sklearn_safe_accumulator_op
from sklearn.utils.validation import _check_sample_weight, column_or_1d
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.csr_matrix_ext import CSRMatrixType
from bodo.libs.distributed_api import Reduce_Type, create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks, get_num_nodes
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, get_overload_const, get_overload_const_int, get_overload_const_str, is_overload_constant_number, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true
this_module = sys.modules[__name__]
_is_sklearn_supported_version = False
_min_sklearn_version = 1, 1, 0
_min_sklearn_ver_str = '.'.join(str(x) for x in _min_sklearn_version)
_max_sklearn_version_exclusive = 1, 2, 0
_max_sklearn_ver_str = '.'.join(str(x) for x in _max_sklearn_version_exclusive)
try:
    import re
    import sklearn
    regex = re.compile('(\\d+)\\.(\\d+)\\..*(\\d+)')
    sklearn_version = sklearn.__version__
    m = regex.match(sklearn_version)
    if m:
        ver = tuple(map(int, m.groups()))
        if (ver >= _min_sklearn_version and ver <
            _max_sklearn_version_exclusive):
            _is_sklearn_supported_version = True
except ImportError as bioba__yqqi:
    pass


def check_sklearn_version():
    if not _is_sklearn_supported_version:
        kgf__qsr = f""" Bodo supports scikit-learn version >= {_min_sklearn_ver_str} and < {_max_sklearn_ver_str}.
             Installed version is {sklearn.__version__}.
"""
        raise BodoError(kgf__qsr)


def random_forest_model_fit(m, X, y):
    gzhq__drebo = m.n_estimators
    echj__wvwkr = MPI.Get_processor_name()
    inbxq__mefo = get_host_ranks()
    pkuwh__tskh = len(inbxq__mefo)
    joef__cwkce = bodo.get_rank()
    m.n_estimators = bodo.libs.distributed_api.get_node_portion(gzhq__drebo,
        pkuwh__tskh, joef__cwkce)
    if joef__cwkce == inbxq__mefo[echj__wvwkr][0]:
        m.n_jobs = len(inbxq__mefo[echj__wvwkr])
        if m.random_state is None:
            m.random_state = np.random.RandomState()
        from sklearn.utils import parallel_backend
        with parallel_backend('threading'):
            m.fit(X, y)
        m.n_jobs = 1
    with numba.objmode(first_rank_node='int32[:]'):
        first_rank_node = get_nodes_first_ranks()
    qgvp__ayob = create_subcomm_mpi4py(first_rank_node)
    if qgvp__ayob != MPI.COMM_NULL:
        djh__dpz = 10
        irjlq__wudme = bodo.libs.distributed_api.get_node_portion(gzhq__drebo,
            pkuwh__tskh, 0)
        mmsan__cjc = irjlq__wudme // djh__dpz
        if irjlq__wudme % djh__dpz != 0:
            mmsan__cjc += 1
        gwuvd__ehzq = []
        for hlc__kqrii in range(mmsan__cjc):
            uko__vllme = qgvp__ayob.gather(m.estimators_[hlc__kqrii *
                djh__dpz:hlc__kqrii * djh__dpz + djh__dpz])
            if joef__cwkce == 0:
                gwuvd__ehzq += list(itertools.chain.from_iterable(uko__vllme))
        if joef__cwkce == 0:
            m.estimators_ = gwuvd__ehzq
    ubwg__enu = MPI.COMM_WORLD
    if joef__cwkce == 0:
        for hlc__kqrii in range(0, gzhq__drebo, 10):
            ubwg__enu.bcast(m.estimators_[hlc__kqrii:hlc__kqrii + 10])
        if isinstance(m, sklearn.ensemble.RandomForestClassifier):
            ubwg__enu.bcast(m.n_classes_)
            ubwg__enu.bcast(m.classes_)
        ubwg__enu.bcast(m.n_outputs_)
    else:
        inmem__skd = []
        for hlc__kqrii in range(0, gzhq__drebo, 10):
            inmem__skd += ubwg__enu.bcast(None)
        if isinstance(m, sklearn.ensemble.RandomForestClassifier):
            m.n_classes_ = ubwg__enu.bcast(None)
            m.classes_ = ubwg__enu.bcast(None)
        m.n_outputs_ = ubwg__enu.bcast(None)
        m.estimators_ = inmem__skd
    assert len(m.estimators_) == gzhq__drebo
    m.n_estimators = gzhq__drebo
    m.n_features_in_ = X.shape[1]


BodoRandomForestClassifierType = install_py_obj_class(types_name=
    'random_forest_classifier_type', python_type=sklearn.ensemble.
    RandomForestClassifier, module=this_module, class_name=
    'BodoRandomForestClassifierType', model_name=
    'BodoRandomForestClassifierModel')


@overload(sklearn.ensemble.RandomForestClassifier, no_unliteral=True)
def sklearn_ensemble_RandomForestClassifier_overload(n_estimators=100,
    criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf
    =1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=
    None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False,
    n_jobs=None, random_state=None, verbose=0, warm_start=False,
    class_weight=None, ccp_alpha=0.0, max_samples=None):
    check_sklearn_version()

    def _sklearn_ensemble_RandomForestClassifier_impl(n_estimators=100,
        criterion='gini', max_depth=None, min_samples_split=2,
        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=
        'auto', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=
        True, oob_score=False, n_jobs=None, random_state=None, verbose=0,
        warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None):
        with numba.objmode(m='random_forest_classifier_type'):
            if random_state is not None and get_num_nodes() > 1:
                print(
                    'With multinode, fixed random_state seed values are ignored.\n'
                    )
                random_state = None
            m = sklearn.ensemble.RandomForestClassifier(n_estimators=
                n_estimators, criterion=criterion, max_depth=max_depth,
                min_samples_split=min_samples_split, min_samples_leaf=
                min_samples_leaf, min_weight_fraction_leaf=
                min_weight_fraction_leaf, max_features=max_features,
                max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=
                min_impurity_decrease, bootstrap=bootstrap, oob_score=
                oob_score, n_jobs=1, random_state=random_state, verbose=
                verbose, warm_start=warm_start, class_weight=class_weight,
                ccp_alpha=ccp_alpha, max_samples=max_samples)
        return m
    return _sklearn_ensemble_RandomForestClassifier_impl


def parallel_predict_regression(m, X):
    check_sklearn_version()

    def _model_predict_impl(m, X):
        with numba.objmode(result='float64[:]'):
            m.n_jobs = 1
            if len(X) == 0:
                result = np.empty(0, dtype=np.float64)
            else:
                result = m.predict(X).astype(np.float64).flatten()
        return result
    return _model_predict_impl


def parallel_predict(m, X):
    check_sklearn_version()

    def _model_predict_impl(m, X):
        with numba.objmode(result='int64[:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty(0, dtype=np.int64)
            else:
                result = m.predict(X).astype(np.int64).flatten()
        return result
    return _model_predict_impl


def parallel_predict_proba(m, X):
    check_sklearn_version()

    def _model_predict_proba_impl(m, X):
        with numba.objmode(result='float64[:,:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty((0, 0), dtype=np.float64)
            else:
                result = m.predict_proba(X).astype(np.float64)
        return result
    return _model_predict_proba_impl


def parallel_predict_log_proba(m, X):
    check_sklearn_version()

    def _model_predict_log_proba_impl(m, X):
        with numba.objmode(result='float64[:,:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty((0, 0), dtype=np.float64)
            else:
                result = m.predict_log_proba(X).astype(np.float64)
        return result
    return _model_predict_log_proba_impl


def parallel_score(m, X, y, sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()

    def _model_score_impl(m, X, y, sample_weight=None, _is_data_distributed
        =False):
        with numba.objmode(result='float64[:]'):
            result = m.score(X, y, sample_weight=sample_weight)
            if _is_data_distributed:
                result = np.full(len(y), result)
            else:
                result = np.array([result])
        if _is_data_distributed:
            result = bodo.allgatherv(result)
        return result.mean()
    return _model_score_impl


@overload_method(BodoRandomForestClassifierType, 'predict', no_unliteral=True)
def overload_model_predict(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict. (Data parallelization)"""
    return parallel_predict(m, X)


@overload_method(BodoRandomForestClassifierType, 'predict_proba',
    no_unliteral=True)
def overload_rf_predict_proba(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict_proba. (Data parallelization)"""
    return parallel_predict_proba(m, X)


@overload_method(BodoRandomForestClassifierType, 'predict_log_proba',
    no_unliteral=True)
def overload_rf_predict_log_proba(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict_log_proba. (Data parallelization)"""
    return parallel_predict_log_proba(m, X)


@overload_method(BodoRandomForestClassifierType, 'score', no_unliteral=True)
def overload_model_score(m, X, y, sample_weight=None, _is_data_distributed=
    False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


def precision_recall_fscore_support_helper(MCM, average):

    def multilabel_confusion_matrix(y_true, y_pred, *, sample_weight=None,
        labels=None, samplewise=False):
        return MCM
    yni__zef = sklearn.metrics._classification.multilabel_confusion_matrix
    result = -1.0
    try:
        sklearn.metrics._classification.multilabel_confusion_matrix = (
            multilabel_confusion_matrix)
        result = (sklearn.metrics._classification.
            precision_recall_fscore_support([], [], average=average))
    finally:
        sklearn.metrics._classification.multilabel_confusion_matrix = yni__zef
    return result


@numba.njit
def precision_recall_fscore_parallel(y_true, y_pred, operation, average=
    'binary'):
    labels = bodo.libs.array_kernels.unique(y_true, parallel=True)
    labels = bodo.allgatherv(labels, False)
    labels = bodo.libs.array_kernels.sort(labels, ascending=True, inplace=False
        )
    wzk__zjntq = len(labels)
    rnlbn__vpga = np.zeros(wzk__zjntq, np.int64)
    gsqg__epmu = np.zeros(wzk__zjntq, np.int64)
    weg__czck = np.zeros(wzk__zjntq, np.int64)
    eueyq__rqnv = (bodo.hiframes.pd_categorical_ext.
        get_label_dict_from_categories(labels))
    for hlc__kqrii in range(len(y_true)):
        gsqg__epmu[eueyq__rqnv[y_true[hlc__kqrii]]] += 1
        if y_pred[hlc__kqrii] not in eueyq__rqnv:
            continue
        mkz__vxe = eueyq__rqnv[y_pred[hlc__kqrii]]
        weg__czck[mkz__vxe] += 1
        if y_true[hlc__kqrii] == y_pred[hlc__kqrii]:
            rnlbn__vpga[mkz__vxe] += 1
    rnlbn__vpga = bodo.libs.distributed_api.dist_reduce(rnlbn__vpga, np.
        int32(Reduce_Type.Sum.value))
    gsqg__epmu = bodo.libs.distributed_api.dist_reduce(gsqg__epmu, np.int32
        (Reduce_Type.Sum.value))
    weg__czck = bodo.libs.distributed_api.dist_reduce(weg__czck, np.int32(
        Reduce_Type.Sum.value))
    bbjbu__kqyxy = weg__czck - rnlbn__vpga
    vrow__vjozv = gsqg__epmu - rnlbn__vpga
    wlwwo__qlcx = rnlbn__vpga
    tnxj__zxfd = y_true.shape[0] - wlwwo__qlcx - bbjbu__kqyxy - vrow__vjozv
    with numba.objmode(result='float64[:]'):
        MCM = np.array([tnxj__zxfd, bbjbu__kqyxy, vrow__vjozv, wlwwo__qlcx]
            ).T.reshape(-1, 2, 2)
        if operation == 'precision':
            result = precision_recall_fscore_support_helper(MCM, average)[0]
        elif operation == 'recall':
            result = precision_recall_fscore_support_helper(MCM, average)[1]
        elif operation == 'f1':
            result = precision_recall_fscore_support_helper(MCM, average)[2]
        if average is not None:
            result = np.array([result])
    return result


@overload(sklearn.metrics.precision_score, no_unliteral=True)
def overload_precision_score(y_true, y_pred, labels=None, pos_label=1,
    average='binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _precision_score_impl(y_true, y_pred, labels=None,
                pos_label=1, average='binary', sample_weight=None,
                zero_division='warn', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.precision_score(y_true, y_pred,
                        labels=labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _precision_score_impl
        else:

            def _precision_score_impl(y_true, y_pred, labels=None,
                pos_label=1, average='binary', sample_weight=None,
                zero_division='warn', _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'precision', average=average)
            return _precision_score_impl
    elif is_overload_false(_is_data_distributed):

        def _precision_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.precision_score(y_true, y_pred,
                    labels=labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _precision_score_impl
    else:

        def _precision_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred,
                'precision', average=average)
            return score[0]
        return _precision_score_impl


@overload(sklearn.metrics.recall_score, no_unliteral=True)
def overload_recall_score(y_true, y_pred, labels=None, pos_label=1, average
    ='binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.recall_score(y_true, y_pred,
                        labels=labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _recall_score_impl
        else:

            def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'recall', average=average)
            return _recall_score_impl
    elif is_overload_false(_is_data_distributed):

        def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.recall_score(y_true, y_pred, labels
                    =labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _recall_score_impl
    else:

        def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred,
                'recall', average=average)
            return score[0]
        return _recall_score_impl


@overload(sklearn.metrics.f1_score, no_unliteral=True)
def overload_f1_score(y_true, y_pred, labels=None, pos_label=1, average=
    'binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.f1_score(y_true, y_pred, labels
                        =labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _f1_score_impl
        else:

            def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'f1', average=average)
            return _f1_score_impl
    elif is_overload_false(_is_data_distributed):

        def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.f1_score(y_true, y_pred, labels=
                    labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _f1_score_impl
    else:

        def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred, 'f1',
                average=average)
            return score[0]
        return _f1_score_impl


def mse_mae_dist_helper(y_true, y_pred, sample_weight, multioutput, squared,
    metric):
    if metric == 'mse':
        hizm__pte = sklearn.metrics.mean_squared_error(y_true, y_pred,
            sample_weight=sample_weight, multioutput='raw_values', squared=True
            )
    elif metric == 'mae':
        hizm__pte = sklearn.metrics.mean_absolute_error(y_true, y_pred,
            sample_weight=sample_weight, multioutput='raw_values')
    else:
        raise RuntimeError(
            f"Unrecognized metric {metric}. Must be one of 'mae' and 'mse'")
    ubwg__enu = MPI.COMM_WORLD
    sws__brwxq = ubwg__enu.Get_size()
    if sample_weight is not None:
        rlbkw__imgh = np.sum(sample_weight)
    else:
        rlbkw__imgh = np.float64(y_true.shape[0])
    fkmfl__bfeq = np.zeros(sws__brwxq, dtype=type(rlbkw__imgh))
    ubwg__enu.Allgather(rlbkw__imgh, fkmfl__bfeq)
    sal__tbik = np.zeros((sws__brwxq, *hizm__pte.shape), dtype=hizm__pte.dtype)
    ubwg__enu.Allgather(hizm__pte, sal__tbik)
    rwua__fvl = np.average(sal__tbik, weights=fkmfl__bfeq, axis=0)
    if metric == 'mse' and not squared:
        rwua__fvl = np.sqrt(rwua__fvl)
    if isinstance(multioutput, str) and multioutput == 'raw_values':
        return rwua__fvl
    elif isinstance(multioutput, str) and multioutput == 'uniform_average':
        return np.average(rwua__fvl)
    else:
        return np.average(rwua__fvl, weights=multioutput)


@overload(sklearn.metrics.mean_squared_error, no_unliteral=True)
def overload_mean_squared_error(y_true, y_pred, sample_weight=None,
    multioutput='uniform_average', squared=True, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', squared=True, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=squared, metric='mse')
                    else:
                        err = sklearn.metrics.mean_squared_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput, squared=squared)
                return err
            return _mse_impl
        else:

            def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', squared=True, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=squared, metric='mse')
                    else:
                        err = sklearn.metrics.mean_squared_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput, squared=squared)
                return err
            return _mse_impl
    elif is_overload_none(sample_weight):

        def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', squared=True, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        squared, metric='mse')
                else:
                    err = sklearn.metrics.mean_squared_error(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=
                        multioutput, squared=squared)
            return err
        return _mse_impl
    else:

        def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', squared=True, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        squared, metric='mse')
                else:
                    err = sklearn.metrics.mean_squared_error(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=
                        multioutput, squared=squared)
            return err
        return _mse_impl


@overload(sklearn.metrics.mean_absolute_error, no_unliteral=True)
def overload_mean_absolute_error(y_true, y_pred, sample_weight=None,
    multioutput='uniform_average', _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=True, metric='mae')
                    else:
                        err = sklearn.metrics.mean_absolute_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput)
                return err
            return _mae_impl
        else:

            def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=True, metric='mae')
                    else:
                        err = sklearn.metrics.mean_absolute_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput)
                return err
            return _mae_impl
    elif is_overload_none(sample_weight):

        def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        True, metric='mae')
                else:
                    err = sklearn.metrics.mean_absolute_error(y_true,
                        y_pred, sample_weight=sample_weight, multioutput=
                        multioutput)
            return err
        return _mae_impl
    else:

        def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        True, metric='mae')
                else:
                    err = sklearn.metrics.mean_absolute_error(y_true,
                        y_pred, sample_weight=sample_weight, multioutput=
                        multioutput)
            return err
        return _mae_impl


def log_loss_dist_helper(y_true, y_pred, eps, normalize, sample_weight, labels
    ):
    loss = sklearn.metrics.log_loss(y_true, y_pred, eps=eps, normalize=
        False, sample_weight=sample_weight, labels=labels)
    ubwg__enu = MPI.COMM_WORLD
    loss = ubwg__enu.allreduce(loss, op=MPI.SUM)
    if normalize:
        nvt__rbn = np.sum(sample_weight) if sample_weight is not None else len(
            y_true)
        nvt__rbn = ubwg__enu.allreduce(nvt__rbn, op=MPI.SUM)
        loss = loss / nvt__rbn
    return loss


@overload(sklearn.metrics.log_loss, no_unliteral=True)
def overload_log_loss(y_true, y_pred, eps=1e-15, normalize=True,
    sample_weight=None, labels=None, _is_data_distributed=False):
    check_sklearn_version()
    ecax__osooi = 'def _log_loss_impl(\n'
    ecax__osooi += '    y_true,\n'
    ecax__osooi += '    y_pred,\n'
    ecax__osooi += '    eps=1e-15,\n'
    ecax__osooi += '    normalize=True,\n'
    ecax__osooi += '    sample_weight=None,\n'
    ecax__osooi += '    labels=None,\n'
    ecax__osooi += '    _is_data_distributed=False,\n'
    ecax__osooi += '):\n'
    ecax__osooi += (
        '    y_true = bodo.utils.conversion.coerce_to_array(y_true)\n')
    ecax__osooi += (
        '    y_pred = bodo.utils.conversion.coerce_to_array(y_pred)\n')
    if not is_overload_none(sample_weight):
        ecax__osooi += (
            '    sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight)\n'
            )
    if not is_overload_none(labels):
        ecax__osooi += (
            '    labels = bodo.utils.conversion.coerce_to_array(labels)\n')
    if is_overload_true(_is_data_distributed) and is_overload_none(labels):
        ecax__osooi += (
            '    labels = bodo.libs.array_kernels.unique(y_true, parallel=True)\n'
            )
        ecax__osooi += '    labels = bodo.allgatherv(labels, False)\n'
    ecax__osooi += "    with numba.objmode(loss='float64'):\n"
    if is_overload_false(_is_data_distributed):
        ecax__osooi += '        loss = sklearn.metrics.log_loss(\n'
    else:
        ecax__osooi += '        loss = log_loss_dist_helper(\n'
    ecax__osooi += (
        '            y_true, y_pred, eps=eps, normalize=normalize,\n')
    ecax__osooi += '            sample_weight=sample_weight, labels=labels\n'
    ecax__osooi += '        )\n'
    ecax__osooi += '        return loss\n'
    wxn__kvxay = {}
    exec(ecax__osooi, globals(), wxn__kvxay)
    khozj__exx = wxn__kvxay['_log_loss_impl']
    return khozj__exx


@overload(sklearn.metrics.pairwise.cosine_similarity, no_unliteral=True)
def overload_metrics_cosine_similarity(X, Y=None, dense_output=True,
    _is_Y_distributed=False, _is_X_distributed=False):
    check_sklearn_version()
    kyczq__njh = {'dense_output': dense_output}
    zezmy__quuu = {'dense_output': True}
    check_unsupported_args('cosine_similarity', kyczq__njh, zezmy__quuu, 'ml')
    if is_overload_false(_is_X_distributed):
        yfvui__puhn = (
            f'metrics_cosine_similarity_type_{numba.core.ir_utils.next_label()}'
            )
        setattr(types, yfvui__puhn, X)
        ecax__osooi = 'def _metrics_cosine_similarity_impl(\n'
        ecax__osooi += """    X, Y=None, dense_output=True, _is_Y_distributed=False, _is_X_distributed=False
"""
        ecax__osooi += '):\n'
        if not is_overload_none(Y) and is_overload_true(_is_Y_distributed):
            ecax__osooi += '    Y = bodo.allgatherv(Y)\n'
        ecax__osooi += "    with numba.objmode(out='float64[:,::1]'):\n"
        ecax__osooi += (
            '        out = sklearn.metrics.pairwise.cosine_similarity(\n')
        ecax__osooi += '            X, Y, dense_output=dense_output\n'
        ecax__osooi += '        )\n'
        ecax__osooi += '    return out\n'
        wxn__kvxay = {}
        exec(ecax__osooi, globals(), wxn__kvxay)
        _metrics_cosine_similarity_impl = wxn__kvxay[
            '_metrics_cosine_similarity_impl']
    elif is_overload_none(Y):

        def _metrics_cosine_similarity_impl(X, Y=None, dense_output=True,
            _is_Y_distributed=False, _is_X_distributed=False):
            yvm__rqqo = np.sqrt((X * X).sum(axis=1)).reshape(-1, 1)
            caas__mtos = X / yvm__rqqo
            gqr__ogcfz = bodo.allgatherv(caas__mtos).T
            bidkb__ctr = np.dot(caas__mtos, gqr__ogcfz)
            return bidkb__ctr
    else:
        ecax__osooi = 'def _metrics_cosine_similarity_impl(\n'
        ecax__osooi += """    X, Y=None, dense_output=True, _is_Y_distributed=False, _is_X_distributed=False
"""
        ecax__osooi += '):\n'
        ecax__osooi += (
            '    X_norms = np.sqrt((X * X).sum(axis=1)).reshape(-1, 1)\n')
        ecax__osooi += '    X_normalized = X / X_norms\n'
        ecax__osooi += (
            '    Y_norms = np.sqrt((Y * Y).sum(axis=1)).reshape(-1, 1)\n')
        ecax__osooi += '    Y_normalized = Y / Y_norms\n'
        if is_overload_true(_is_Y_distributed):
            ecax__osooi += '    Y_normalized = bodo.allgatherv(Y_normalized)\n'
        ecax__osooi += '    Y_normalized_T = Y_normalized.T\n'
        ecax__osooi += (
            '    kernel_matrix = np.dot(X_normalized, Y_normalized_T)\n')
        ecax__osooi += '    return kernel_matrix\n'
        wxn__kvxay = {}
        exec(ecax__osooi, globals(), wxn__kvxay)
        _metrics_cosine_similarity_impl = wxn__kvxay[
            '_metrics_cosine_similarity_impl']
    return _metrics_cosine_similarity_impl


def accuracy_score_dist_helper(y_true, y_pred, normalize, sample_weight):
    score = sklearn.metrics.accuracy_score(y_true, y_pred, normalize=False,
        sample_weight=sample_weight)
    ubwg__enu = MPI.COMM_WORLD
    score = ubwg__enu.allreduce(score, op=MPI.SUM)
    if normalize:
        nvt__rbn = np.sum(sample_weight) if sample_weight is not None else len(
            y_true)
        nvt__rbn = ubwg__enu.allreduce(nvt__rbn, op=MPI.SUM)
        score = score / nvt__rbn
    return score


@overload(sklearn.metrics.accuracy_score, no_unliteral=True)
def overload_accuracy_score(y_true, y_pred, normalize=True, sample_weight=
    None, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_false(_is_data_distributed):
        if is_overload_none(sample_weight):

            def _accuracy_score_impl(y_true, y_pred, normalize=True,
                sample_weight=None, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64'):
                    score = sklearn.metrics.accuracy_score(y_true, y_pred,
                        normalize=normalize, sample_weight=sample_weight)
                return score
            return _accuracy_score_impl
        else:

            def _accuracy_score_impl(y_true, y_pred, normalize=True,
                sample_weight=None, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(score='float64'):
                    score = sklearn.metrics.accuracy_score(y_true, y_pred,
                        normalize=normalize, sample_weight=sample_weight)
                return score
            return _accuracy_score_impl
    elif is_overload_none(sample_weight):

        def _accuracy_score_impl(y_true, y_pred, normalize=True,
            sample_weight=None, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = accuracy_score_dist_helper(y_true, y_pred,
                    normalize=normalize, sample_weight=sample_weight)
            return score
        return _accuracy_score_impl
    else:

        def _accuracy_score_impl(y_true, y_pred, normalize=True,
            sample_weight=None, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(score='float64'):
                score = accuracy_score_dist_helper(y_true, y_pred,
                    normalize=normalize, sample_weight=sample_weight)
            return score
        return _accuracy_score_impl


def check_consistent_length_parallel(*arrays):
    ubwg__enu = MPI.COMM_WORLD
    svcl__foei = True
    djhb__ngkvk = [len(sjt__udl) for sjt__udl in arrays if sjt__udl is not None
        ]
    if len(np.unique(djhb__ngkvk)) > 1:
        svcl__foei = False
    svcl__foei = ubwg__enu.allreduce(svcl__foei, op=MPI.LAND)
    return svcl__foei


def r2_score_dist_helper(y_true, y_pred, sample_weight, multioutput):
    ubwg__enu = MPI.COMM_WORLD
    if y_true.ndim == 1:
        y_true = y_true.reshape((-1, 1))
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape((-1, 1))
    if not check_consistent_length_parallel(y_true, y_pred, sample_weight):
        raise ValueError(
            'y_true, y_pred and sample_weight (if not None) have inconsistent number of samples'
            )
    tgf__cjopl = y_true.shape[0]
    kwr__cmnm = ubwg__enu.allreduce(tgf__cjopl, op=MPI.SUM)
    if kwr__cmnm < 2:
        warnings.warn(
            'R^2 score is not well-defined with less than two samples.',
            UndefinedMetricWarning)
        return np.array([float('nan')])
    if sample_weight is not None:
        sample_weight = column_or_1d(sample_weight)
        jtfl__vdbq = sample_weight[:, np.newaxis]
    else:
        sample_weight = np.float64(y_true.shape[0])
        jtfl__vdbq = 1.0
    hzyo__wau = (jtfl__vdbq * (y_true - y_pred) ** 2).sum(axis=0, dtype=np.
        float64)
    uijqd__nihh = np.zeros(hzyo__wau.shape, dtype=hzyo__wau.dtype)
    ubwg__enu.Allreduce(hzyo__wau, uijqd__nihh, op=MPI.SUM)
    hasjo__xbf = np.nansum(y_true * jtfl__vdbq, axis=0, dtype=np.float64)
    orln__yuqyc = np.zeros_like(hasjo__xbf)
    ubwg__enu.Allreduce(hasjo__xbf, orln__yuqyc, op=MPI.SUM)
    eiime__owfz = np.nansum(sample_weight, dtype=np.float64)
    mvzdv__ylkvs = ubwg__enu.allreduce(eiime__owfz, op=MPI.SUM)
    pij__ogson = orln__yuqyc / mvzdv__ylkvs
    mdswy__uab = (jtfl__vdbq * (y_true - pij__ogson) ** 2).sum(axis=0,
        dtype=np.float64)
    jyuhd__obd = np.zeros(mdswy__uab.shape, dtype=mdswy__uab.dtype)
    ubwg__enu.Allreduce(mdswy__uab, jyuhd__obd, op=MPI.SUM)
    snas__mmajm = jyuhd__obd != 0
    eys__gzgo = uijqd__nihh != 0
    kame__nji = snas__mmajm & eys__gzgo
    hscnp__plybj = np.ones([y_true.shape[1] if len(y_true.shape) > 1 else 1])
    hscnp__plybj[kame__nji] = 1 - uijqd__nihh[kame__nji] / jyuhd__obd[kame__nji
        ]
    hscnp__plybj[eys__gzgo & ~snas__mmajm] = 0.0
    if isinstance(multioutput, str):
        if multioutput == 'raw_values':
            return hscnp__plybj
        elif multioutput == 'uniform_average':
            hxwtq__pwxfy = None
        elif multioutput == 'variance_weighted':
            hxwtq__pwxfy = jyuhd__obd
            if not np.any(snas__mmajm):
                if not np.any(eys__gzgo):
                    return np.array([1.0])
                else:
                    return np.array([0.0])
    else:
        hxwtq__pwxfy = multioutput
    return np.array([np.average(hscnp__plybj, weights=hxwtq__pwxfy)])


@overload(sklearn.metrics.r2_score, no_unliteral=True)
def overload_r2_score(y_true, y_pred, sample_weight=None, multioutput=
    'uniform_average', _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) not in ['raw_values', 'uniform_average',
        'variance_weighted']:
        raise BodoError(
            f"Unsupported argument {get_overload_const_str(multioutput)} specified for 'multioutput'"
            )
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _r2_score_impl(y_true, y_pred, sample_weight=None,
                multioutput='uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    if _is_data_distributed:
                        score = r2_score_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                    else:
                        score = sklearn.metrics.r2_score(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                return score
            return _r2_score_impl
        else:

            def _r2_score_impl(y_true, y_pred, sample_weight=None,
                multioutput='uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(score='float64[:]'):
                    if _is_data_distributed:
                        score = r2_score_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                    else:
                        score = sklearn.metrics.r2_score(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                return score
            return _r2_score_impl
    elif is_overload_none(sample_weight):

        def _r2_score_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                if _is_data_distributed:
                    score = r2_score_dist_helper(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
                    score = score[0]
                else:
                    score = sklearn.metrics.r2_score(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
            return score
        return _r2_score_impl
    else:

        def _r2_score_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(score='float64'):
                if _is_data_distributed:
                    score = r2_score_dist_helper(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
                    score = score[0]
                else:
                    score = sklearn.metrics.r2_score(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
            return score
        return _r2_score_impl


def confusion_matrix_dist_helper(y_true, y_pred, labels=None, sample_weight
    =None, normalize=None):
    if normalize not in ['true', 'pred', 'all', None]:
        raise ValueError(
            "normalize must be one of {'true', 'pred', 'all', None}")
    ubwg__enu = MPI.COMM_WORLD
    try:
        kesjs__yqsmr = sklearn.metrics.confusion_matrix(y_true, y_pred,
            labels=labels, sample_weight=sample_weight, normalize=None)
    except ValueError as rzx__qxqwu:
        kesjs__yqsmr = rzx__qxqwu
    uelr__usla = (isinstance(kesjs__yqsmr, ValueError) and 
        'At least one label specified must be in y_true' in kesjs__yqsmr.
        args[0])
    bbnm__lhvgg = ubwg__enu.allreduce(uelr__usla, op=MPI.LAND)
    if bbnm__lhvgg:
        raise kesjs__yqsmr
    elif uelr__usla:
        dtype = np.int64
        if sample_weight is not None and sample_weight.dtype.kind not in {'i',
            'u', 'b'}:
            dtype = np.float64
        atg__rhnar = np.zeros((labels.size, labels.size), dtype=dtype)
    else:
        atg__rhnar = kesjs__yqsmr
    eah__bnnn = np.zeros_like(atg__rhnar)
    ubwg__enu.Allreduce(atg__rhnar, eah__bnnn)
    with np.errstate(all='ignore'):
        if normalize == 'true':
            eah__bnnn = eah__bnnn / eah__bnnn.sum(axis=1, keepdims=True)
        elif normalize == 'pred':
            eah__bnnn = eah__bnnn / eah__bnnn.sum(axis=0, keepdims=True)
        elif normalize == 'all':
            eah__bnnn = eah__bnnn / eah__bnnn.sum()
        eah__bnnn = np.nan_to_num(eah__bnnn)
    return eah__bnnn


@overload(sklearn.metrics.confusion_matrix, no_unliteral=True)
def overload_confusion_matrix(y_true, y_pred, labels=None, sample_weight=
    None, normalize=None, _is_data_distributed=False):
    check_sklearn_version()
    ecax__osooi = 'def _confusion_matrix_impl(\n'
    ecax__osooi += '    y_true, y_pred, labels=None,\n'
    ecax__osooi += '    sample_weight=None, normalize=None,\n'
    ecax__osooi += '    _is_data_distributed=False,\n'
    ecax__osooi += '):\n'
    ecax__osooi += (
        '    y_true = bodo.utils.conversion.coerce_to_array(y_true)\n')
    ecax__osooi += (
        '    y_pred = bodo.utils.conversion.coerce_to_array(y_pred)\n')
    ecax__osooi += (
        '    y_true = bodo.utils.typing.decode_if_dict_array(y_true)\n')
    ecax__osooi += (
        '    y_pred = bodo.utils.typing.decode_if_dict_array(y_pred)\n')
    nflts__ejt = 'int64[:,:]', 'np.int64'
    if not is_overload_none(normalize):
        nflts__ejt = 'float64[:,:]', 'np.float64'
    if not is_overload_none(sample_weight):
        ecax__osooi += (
            '    sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight)\n'
            )
        if numba.np.numpy_support.as_dtype(sample_weight.dtype).kind not in {
            'i', 'u', 'b'}:
            nflts__ejt = 'float64[:,:]', 'np.float64'
    if not is_overload_none(labels):
        ecax__osooi += (
            '    labels = bodo.utils.conversion.coerce_to_array(labels)\n')
    elif is_overload_true(_is_data_distributed):
        ecax__osooi += (
            '    labels = bodo.libs.array_kernels.concat([y_true, y_pred])\n')
        ecax__osooi += (
            '    labels = bodo.libs.array_kernels.unique(labels, parallel=True)\n'
            )
        ecax__osooi += '    labels = bodo.allgatherv(labels, False)\n'
        ecax__osooi += """    labels = bodo.libs.array_kernels.sort(labels, ascending=True, inplace=False)
"""
    ecax__osooi += f"    with numba.objmode(cm='{nflts__ejt[0]}'):\n"
    if is_overload_false(_is_data_distributed):
        ecax__osooi += '      cm = sklearn.metrics.confusion_matrix(\n'
    else:
        ecax__osooi += '      cm = confusion_matrix_dist_helper(\n'
    ecax__osooi += '        y_true, y_pred, labels=labels,\n'
    ecax__osooi += (
        '        sample_weight=sample_weight, normalize=normalize,\n')
    ecax__osooi += f'      ).astype({nflts__ejt[1]})\n'
    ecax__osooi += '    return cm\n'
    wxn__kvxay = {}
    exec(ecax__osooi, globals(), wxn__kvxay)
    colq__rttum = wxn__kvxay['_confusion_matrix_impl']
    return colq__rttum


BodoSGDRegressorType = install_py_obj_class(types_name='sgd_regressor_type',
    python_type=sklearn.linear_model.SGDRegressor, module=this_module,
    class_name='BodoSGDRegressorType', model_name='BodoSGDRegressorModel')


@overload(sklearn.linear_model.SGDRegressor, no_unliteral=True)
def sklearn_linear_model_SGDRegressor_overload(loss='squared_error',
    penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter
    =1000, tol=0.001, shuffle=True, verbose=0, epsilon=0.1, random_state=
    None, learning_rate='invscaling', eta0=0.01, power_t=0.25,
    early_stopping=False, validation_fraction=0.1, n_iter_no_change=5,
    warm_start=False, average=False):
    check_sklearn_version()

    def _sklearn_linear_model_SGDRegressor_impl(loss='squared_error',
        penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True,
        max_iter=1000, tol=0.001, shuffle=True, verbose=0, epsilon=0.1,
        random_state=None, learning_rate='invscaling', eta0=0.01, power_t=
        0.25, early_stopping=False, validation_fraction=0.1,
        n_iter_no_change=5, warm_start=False, average=False):
        with numba.objmode(m='sgd_regressor_type'):
            m = sklearn.linear_model.SGDRegressor(loss=loss, penalty=
                penalty, alpha=alpha, l1_ratio=l1_ratio, fit_intercept=
                fit_intercept, max_iter=max_iter, tol=tol, shuffle=shuffle,
                verbose=verbose, epsilon=epsilon, random_state=random_state,
                learning_rate=learning_rate, eta0=eta0, power_t=power_t,
                early_stopping=early_stopping, validation_fraction=
                validation_fraction, n_iter_no_change=n_iter_no_change,
                warm_start=warm_start, average=average)
        return m
    return _sklearn_linear_model_SGDRegressor_impl


@overload_method(BodoSGDRegressorType, 'fit', no_unliteral=True)
def overload_sgdr_model_fit(m, X, y, coef_init=None, intercept_init=None,
    sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_true(_is_data_distributed):
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_none(coef_init):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'coef_init' is not supported for distributed data."
                )
        if not is_overload_none(intercept_init):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'intercept_init' is not supported for distributed data."
                )

        def _model_sgdr_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_regressor_type'):
                m = fit_sgd(m, X, y, _is_data_distributed)
            bodo.barrier()
            return m
        return _model_sgdr_fit_impl
    else:

        def _model_sgdr_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_regressor_type'):
                m = m.fit(X, y, coef_init, intercept_init, sample_weight)
            return m
        return _model_sgdr_fit_impl


@overload_method(BodoSGDRegressorType, 'predict', no_unliteral=True)
def overload_sgdr_model_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoSGDRegressorType, 'score', no_unliteral=True)
def overload_sgdr_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


BodoSGDClassifierType = install_py_obj_class(types_name=
    'sgd_classifier_type', python_type=sklearn.linear_model.SGDClassifier,
    module=this_module, class_name='BodoSGDClassifierType', model_name=
    'BodoSGDClassifierModel')


@overload(sklearn.linear_model.SGDClassifier, no_unliteral=True)
def sklearn_linear_model_SGDClassifier_overload(loss='hinge', penalty='l2',
    alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol=
    0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=None, random_state=
    None, learning_rate='optimal', eta0=0.0, power_t=0.5, early_stopping=
    False, validation_fraction=0.1, n_iter_no_change=5, class_weight=None,
    warm_start=False, average=False):
    check_sklearn_version()

    def _sklearn_linear_model_SGDClassifier_impl(loss='hinge', penalty='l2',
        alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol
        =0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=None,
        random_state=None, learning_rate='optimal', eta0=0.0, power_t=0.5,
        early_stopping=False, validation_fraction=0.1, n_iter_no_change=5,
        class_weight=None, warm_start=False, average=False):
        with numba.objmode(m='sgd_classifier_type'):
            m = sklearn.linear_model.SGDClassifier(loss=loss, penalty=
                penalty, alpha=alpha, l1_ratio=l1_ratio, fit_intercept=
                fit_intercept, max_iter=max_iter, tol=tol, shuffle=shuffle,
                verbose=verbose, epsilon=epsilon, n_jobs=n_jobs,
                random_state=random_state, learning_rate=learning_rate,
                eta0=eta0, power_t=power_t, early_stopping=early_stopping,
                validation_fraction=validation_fraction, n_iter_no_change=
                n_iter_no_change, class_weight=class_weight, warm_start=
                warm_start, average=average)
        return m
    return _sklearn_linear_model_SGDClassifier_impl


def fit_sgd(m, X, y, y_classes=None, _is_data_distributed=False):
    ubwg__enu = MPI.COMM_WORLD
    rli__kasv = ubwg__enu.allreduce(len(X), op=MPI.SUM)
    qok__voq = len(X) / rli__kasv
    qbjc__iqg = ubwg__enu.Get_size()
    m.n_jobs = 1
    m.early_stopping = False
    tfe__wzu = np.inf
    zbv__vjiq = 0
    if m.loss == 'hinge':
        kpc__izko = hinge_loss
    elif m.loss == 'log':
        kpc__izko = log_loss
    elif m.loss == 'squared_error':
        kpc__izko = mean_squared_error
    else:
        raise ValueError('loss {} not supported'.format(m.loss))
    wjkv__sotgk = False
    if isinstance(m, sklearn.linear_model.SGDRegressor):
        wjkv__sotgk = True
    for dlaoq__bcau in range(m.max_iter):
        if wjkv__sotgk:
            m.partial_fit(X, y)
        else:
            m.partial_fit(X, y, classes=y_classes)
        m.coef_ = m.coef_ * qok__voq
        m.coef_ = ubwg__enu.allreduce(m.coef_, op=MPI.SUM)
        m.intercept_ = m.intercept_ * qok__voq
        m.intercept_ = ubwg__enu.allreduce(m.intercept_, op=MPI.SUM)
        if wjkv__sotgk:
            y_pred = m.predict(X)
            bxuhg__exvaz = kpc__izko(y, y_pred)
        else:
            y_pred = m.decision_function(X)
            bxuhg__exvaz = kpc__izko(y, y_pred, labels=y_classes)
        zgmct__rkcq = ubwg__enu.allreduce(bxuhg__exvaz, op=MPI.SUM)
        bxuhg__exvaz = zgmct__rkcq / qbjc__iqg
        if m.tol > np.NINF and bxuhg__exvaz > tfe__wzu - m.tol * rli__kasv:
            zbv__vjiq += 1
        else:
            zbv__vjiq = 0
        if bxuhg__exvaz < tfe__wzu:
            tfe__wzu = bxuhg__exvaz
        if zbv__vjiq >= m.n_iter_no_change:
            break
    return m


@overload_method(BodoSGDClassifierType, 'fit', no_unliteral=True)
def overload_sgdc_model_fit(m, X, y, coef_init=None, intercept_init=None,
    sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()
    """
    Provide implementations for the fit function.
    In case input is replicated, we simply call sklearn,
    else we use partial_fit on each rank then use we re-compute the attributes using MPI operations.
    """
    if is_overload_true(_is_data_distributed):
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_none(coef_init):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'coef_init' is not supported for distributed data."
                )
        if not is_overload_none(intercept_init):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'intercept_init' is not supported for distributed data."
                )

        def _model_sgdc_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            y_classes = bodo.libs.array_kernels.unique(y, parallel=True)
            y_classes = bodo.allgatherv(y_classes, False)
            with numba.objmode(m='sgd_classifier_type'):
                m = fit_sgd(m, X, y, y_classes, _is_data_distributed)
            return m
        return _model_sgdc_fit_impl
    else:

        def _model_sgdc_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_classifier_type'):
                m = m.fit(X, y, coef_init, intercept_init, sample_weight)
            return m
        return _model_sgdc_fit_impl


@overload_method(BodoSGDClassifierType, 'predict', no_unliteral=True)
def overload_sgdc_model_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoSGDClassifierType, 'predict_proba', no_unliteral=True)
def overload_sgdc_model_predict_proba(m, X):
    return parallel_predict_proba(m, X)


@overload_method(BodoSGDClassifierType, 'predict_log_proba', no_unliteral=True)
def overload_sgdc_model_predict_log_proba(m, X):
    return parallel_predict_log_proba(m, X)


@overload_method(BodoSGDClassifierType, 'score', no_unliteral=True)
def overload_sgdc_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoSGDClassifierType, 'coef_')
def get_sgdc_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:,:]'):
            result = m.coef_
        return result
    return impl


BodoKMeansClusteringType = install_py_obj_class(types_name=
    'kmeans_clustering_type', python_type=sklearn.cluster.KMeans, module=
    this_module, class_name='BodoKMeansClusteringType', model_name=
    'BodoKMeansClusteringModel')


@overload(sklearn.cluster.KMeans, no_unliteral=True)
def sklearn_cluster_kmeans_overload(n_clusters=8, init='k-means++', n_init=
    10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True,
    algorithm='auto'):
    check_sklearn_version()

    def _sklearn_cluster_kmeans_impl(n_clusters=8, init='k-means++', n_init
        =10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x
        =True, algorithm='auto'):
        with numba.objmode(m='kmeans_clustering_type'):
            m = sklearn.cluster.KMeans(n_clusters=n_clusters, init=init,
                n_init=n_init, max_iter=max_iter, tol=tol, verbose=verbose,
                random_state=random_state, copy_x=copy_x, algorithm=algorithm)
        return m
    return _sklearn_cluster_kmeans_impl


def kmeans_fit_helper(m, len_X, all_X, all_sample_weight, _is_data_distributed
    ):
    ubwg__enu = MPI.COMM_WORLD
    joef__cwkce = ubwg__enu.Get_rank()
    echj__wvwkr = MPI.Get_processor_name()
    inbxq__mefo = get_host_ranks()
    rpi__mylqf = m.n_jobs if hasattr(m, 'n_jobs') else None
    ogc__oqf = m._n_threads if hasattr(m, '_n_threads') else None
    m._n_threads = len(inbxq__mefo[echj__wvwkr])
    if joef__cwkce == 0:
        m.fit(X=all_X, y=None, sample_weight=all_sample_weight)
    if joef__cwkce == 0:
        ubwg__enu.bcast(m.cluster_centers_)
        ubwg__enu.bcast(m.inertia_)
        ubwg__enu.bcast(m.n_iter_)
    else:
        m.cluster_centers_ = ubwg__enu.bcast(None)
        m.inertia_ = ubwg__enu.bcast(None)
        m.n_iter_ = ubwg__enu.bcast(None)
    if _is_data_distributed:
        jxymo__zar = ubwg__enu.allgather(len_X)
        if joef__cwkce == 0:
            ohn__hpuv = np.empty(len(jxymo__zar) + 1, dtype=int)
            np.cumsum(jxymo__zar, out=ohn__hpuv[1:])
            ohn__hpuv[0] = 0
            zkl__ubr = [m.labels_[ohn__hpuv[qzdai__pagmk]:ohn__hpuv[
                qzdai__pagmk + 1]] for qzdai__pagmk in range(len(jxymo__zar))]
            wpc__aqm = ubwg__enu.scatter(zkl__ubr)
        else:
            wpc__aqm = ubwg__enu.scatter(None)
        m.labels_ = wpc__aqm
    elif joef__cwkce == 0:
        ubwg__enu.bcast(m.labels_)
    else:
        m.labels_ = ubwg__enu.bcast(None)
    m._n_threads = ogc__oqf
    return m


@overload_method(BodoKMeansClusteringType, 'fit', no_unliteral=True)
def overload_kmeans_clustering_fit(m, X, y=None, sample_weight=None,
    _is_data_distributed=False):

    def _cluster_kmeans_fit_impl(m, X, y=None, sample_weight=None,
        _is_data_distributed=False):
        if _is_data_distributed:
            all_X = bodo.gatherv(X)
            if sample_weight is not None:
                all_sample_weight = bodo.gatherv(sample_weight)
            else:
                all_sample_weight = None
        else:
            all_X = X
            all_sample_weight = sample_weight
        with numba.objmode(m='kmeans_clustering_type'):
            m = kmeans_fit_helper(m, len(X), all_X, all_sample_weight,
                _is_data_distributed)
        return m
    return _cluster_kmeans_fit_impl


def kmeans_predict_helper(m, X, sample_weight):
    ogc__oqf = m._n_threads if hasattr(m, '_n_threads') else None
    m._n_threads = 1
    if len(X) == 0:
        preds = np.empty(0, dtype=np.int64)
    else:
        preds = m.predict(X, sample_weight).astype(np.int64).flatten()
    m._n_threads = ogc__oqf
    return preds


@overload_method(BodoKMeansClusteringType, 'predict', no_unliteral=True)
def overload_kmeans_clustering_predict(m, X, sample_weight=None):

    def _cluster_kmeans_predict(m, X, sample_weight=None):
        with numba.objmode(preds='int64[:]'):
            preds = kmeans_predict_helper(m, X, sample_weight)
        return preds
    return _cluster_kmeans_predict


@overload_method(BodoKMeansClusteringType, 'score', no_unliteral=True)
def overload_kmeans_clustering_score(m, X, y=None, sample_weight=None,
    _is_data_distributed=False):

    def _cluster_kmeans_score(m, X, y=None, sample_weight=None,
        _is_data_distributed=False):
        with numba.objmode(result='float64'):
            ogc__oqf = m._n_threads if hasattr(m, '_n_threads') else None
            m._n_threads = 1
            if len(X) == 0:
                result = 0
            else:
                result = m.score(X, y=y, sample_weight=sample_weight)
            if _is_data_distributed:
                ubwg__enu = MPI.COMM_WORLD
                result = ubwg__enu.allreduce(result, op=MPI.SUM)
            m._n_threads = ogc__oqf
        return result
    return _cluster_kmeans_score


@overload_method(BodoKMeansClusteringType, 'transform', no_unliteral=True)
def overload_kmeans_clustering_transform(m, X):

    def _cluster_kmeans_transform(m, X):
        with numba.objmode(X_new='float64[:,:]'):
            ogc__oqf = m._n_threads if hasattr(m, '_n_threads') else None
            m._n_threads = 1
            if len(X) == 0:
                X_new = np.empty((0, m.n_clusters), dtype=np.int64)
            else:
                X_new = m.transform(X).astype(np.float64)
            m._n_threads = ogc__oqf
        return X_new
    return _cluster_kmeans_transform


BodoMultinomialNBType = install_py_obj_class(types_name=
    'multinomial_nb_type', python_type=sklearn.naive_bayes.MultinomialNB,
    module=this_module, class_name='BodoMultinomialNBType', model_name=
    'BodoMultinomialNBModel')


@overload(sklearn.naive_bayes.MultinomialNB, no_unliteral=True)
def sklearn_naive_bayes_multinomialnb_overload(alpha=1.0, fit_prior=True,
    class_prior=None):
    check_sklearn_version()

    def _sklearn_naive_bayes_multinomialnb_impl(alpha=1.0, fit_prior=True,
        class_prior=None):
        with numba.objmode(m='multinomial_nb_type'):
            m = sklearn.naive_bayes.MultinomialNB(alpha=alpha, fit_prior=
                fit_prior, class_prior=class_prior)
        return m
    return _sklearn_naive_bayes_multinomialnb_impl


@overload_method(BodoMultinomialNBType, 'fit', no_unliteral=True)
def overload_multinomial_nb_model_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _naive_bayes_multinomial_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _naive_bayes_multinomial_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.naive_bayes.MultinomialNB.fit() : 'sample_weight' not supported."
                )
        ecax__osooi = 'def _model_multinomial_nb_fit_impl(\n'
        ecax__osooi += (
            '    m, X, y, sample_weight=None, _is_data_distributed=False\n')
        ecax__osooi += '):  # pragma: no cover\n'
        ecax__osooi += '    y = bodo.utils.conversion.coerce_to_ndarray(y)\n'
        if isinstance(X, DataFrameType):
            ecax__osooi += '    X = X.to_numpy()\n'
        else:
            ecax__osooi += (
                '    X = bodo.utils.conversion.coerce_to_ndarray(X)\n')
        ecax__osooi += '    my_rank = bodo.get_rank()\n'
        ecax__osooi += '    nranks = bodo.get_size()\n'
        ecax__osooi += '    total_cols = X.shape[1]\n'
        ecax__osooi += '    for i in range(nranks):\n'
        ecax__osooi += """        start = bodo.libs.distributed_api.get_start(total_cols, nranks, i)
"""
        ecax__osooi += (
            '        end = bodo.libs.distributed_api.get_end(total_cols, nranks, i)\n'
            )
        ecax__osooi += '        if i == my_rank:\n'
        ecax__osooi += (
            '            X_train = bodo.gatherv(X[:, start:end:1], root=i)\n')
        ecax__osooi += '        else:\n'
        ecax__osooi += '            bodo.gatherv(X[:, start:end:1], root=i)\n'
        ecax__osooi += '    y_train = bodo.allgatherv(y, False)\n'
        ecax__osooi += '    with numba.objmode(m="multinomial_nb_type"):\n'
        ecax__osooi += '        m = fit_multinomial_nb(\n'
        ecax__osooi += """            m, X_train, y_train, sample_weight, total_cols, _is_data_distributed
"""
        ecax__osooi += '        )\n'
        ecax__osooi += '    bodo.barrier()\n'
        ecax__osooi += '    return m\n'
        wxn__kvxay = {}
        exec(ecax__osooi, globals(), wxn__kvxay)
        fjkqq__itgo = wxn__kvxay['_model_multinomial_nb_fit_impl']
        return fjkqq__itgo


def fit_multinomial_nb(m, X_train, y_train, sample_weight=None, total_cols=
    0, _is_data_distributed=False):
    m._check_X_y(X_train, y_train)
    dlaoq__bcau, n_features = X_train.shape
    m.n_features_in_ = n_features
    lgpwu__bxiy = LabelBinarizer()
    Y = lgpwu__bxiy.fit_transform(y_train)
    m.classes_ = lgpwu__bxiy.classes_
    if Y.shape[1] == 1:
        Y = np.concatenate((1 - Y, Y), axis=1)
    if sample_weight is not None:
        Y = Y.astype(np.float64, copy=False)
        sample_weight = _check_sample_weight(sample_weight, X_train)
        sample_weight = np.atleast_2d(sample_weight)
        Y *= sample_weight.T
    class_prior = m.class_prior
    imxjg__jxwdp = Y.shape[1]
    m._init_counters(imxjg__jxwdp, n_features)
    m._count(X_train.astype('float64'), Y)
    alpha = m._check_alpha()
    m._update_class_log_prior(class_prior=class_prior)
    cor__hfdvb = m.feature_count_ + alpha
    qnu__lkd = cor__hfdvb.sum(axis=1)
    ubwg__enu = MPI.COMM_WORLD
    qbjc__iqg = ubwg__enu.Get_size()
    wivt__jqkht = np.zeros(imxjg__jxwdp)
    ubwg__enu.Allreduce(qnu__lkd, wivt__jqkht, op=MPI.SUM)
    tmer__zur = np.log(cor__hfdvb) - np.log(wivt__jqkht.reshape(-1, 1))
    uzcp__clmne = tmer__zur.T.reshape(n_features * imxjg__jxwdp)
    gwl__lvw = np.ones(qbjc__iqg) * (total_cols // qbjc__iqg)
    oiko__uet = total_cols % qbjc__iqg
    for xsnx__awyvz in range(oiko__uet):
        gwl__lvw[xsnx__awyvz] += 1
    gwl__lvw *= imxjg__jxwdp
    tyd__tmok = np.zeros(qbjc__iqg, dtype=np.int32)
    tyd__tmok[1:] = np.cumsum(gwl__lvw)[:-1]
    brtlz__pee = np.zeros((total_cols, imxjg__jxwdp), dtype=np.float64)
    ubwg__enu.Allgatherv(uzcp__clmne, [brtlz__pee, gwl__lvw, tyd__tmok, MPI
        .DOUBLE_PRECISION])
    m.feature_log_prob_ = brtlz__pee.T
    m.n_features_in_ = m.feature_log_prob_.shape[1]
    return m


@overload_method(BodoMultinomialNBType, 'predict', no_unliteral=True)
def overload_multinomial_nb_model_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoMultinomialNBType, 'score', no_unliteral=True)
def overload_multinomial_nb_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


BodoLogisticRegressionType = install_py_obj_class(types_name=
    'logistic_regression_type', python_type=sklearn.linear_model.
    LogisticRegression, module=this_module, class_name=
    'BodoLogisticRegressionType', model_name='BodoLogisticRegressionModel')


@overload(sklearn.linear_model.LogisticRegression, no_unliteral=True)
def sklearn_linear_model_logistic_regression_overload(penalty='l2', dual=
    False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1,
    class_weight=None, random_state=None, solver='lbfgs', max_iter=100,
    multi_class='auto', verbose=0, warm_start=False, n_jobs=None, l1_ratio=None
    ):
    check_sklearn_version()

    def _sklearn_linear_model_logistic_regression_impl(penalty='l2', dual=
        False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1,
        class_weight=None, random_state=None, solver='lbfgs', max_iter=100,
        multi_class='auto', verbose=0, warm_start=False, n_jobs=None,
        l1_ratio=None):
        with numba.objmode(m='logistic_regression_type'):
            m = sklearn.linear_model.LogisticRegression(penalty=penalty,
                dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                intercept_scaling=intercept_scaling, class_weight=
                class_weight, random_state=random_state, solver=solver,
                max_iter=max_iter, multi_class=multi_class, verbose=verbose,
                warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)
        return m
    return _sklearn_linear_model_logistic_regression_impl


@register_jitable
def _raise_SGD_warning(sgd_name):
    with numba.objmode:
        warnings.warn(
            f'Data is distributed so Bodo will fit model with SGD solver optimization ({sgd_name})'
            , BodoWarning)


@overload_method(BodoLogisticRegressionType, 'fit', no_unliteral=True)
def overload_logistic_regression_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _logistic_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _logistic_regression_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.LogisticRegression.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _sgdc_logistic_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDClassifier')
            with numba.objmode(clf='sgd_classifier_type'):
                if m.l1_ratio is None:
                    l1_ratio = 0.15
                else:
                    l1_ratio = m.l1_ratio
                clf = sklearn.linear_model.SGDClassifier(loss='log',
                    penalty=m.penalty, tol=m.tol, fit_intercept=m.
                    fit_intercept, class_weight=m.class_weight,
                    random_state=m.random_state, max_iter=m.max_iter,
                    verbose=m.verbose, warm_start=m.warm_start, n_jobs=m.
                    n_jobs, l1_ratio=l1_ratio)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
                m.classes_ = clf.classes_
            return m
        return _sgdc_logistic_regression_fit_impl


@overload_method(BodoLogisticRegressionType, 'predict', no_unliteral=True)
def overload_logistic_regression_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoLogisticRegressionType, 'predict_proba', no_unliteral=True
    )
def overload_logistic_regression_predict_proba(m, X):
    return parallel_predict_proba(m, X)


@overload_method(BodoLogisticRegressionType, 'predict_log_proba',
    no_unliteral=True)
def overload_logistic_regression_predict_log_proba(m, X):
    return parallel_predict_log_proba(m, X)


@overload_method(BodoLogisticRegressionType, 'score', no_unliteral=True)
def overload_logistic_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoLogisticRegressionType, 'coef_')
def get_logisticR_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:,:]'):
            result = m.coef_
        return result
    return impl


BodoLinearRegressionType = install_py_obj_class(types_name=
    'linear_regression_type', python_type=sklearn.linear_model.
    LinearRegression, module=this_module, class_name=
    'BodoLinearRegressionType', model_name='BodoLinearRegressionModel')


@overload(sklearn.linear_model.LinearRegression, no_unliteral=True)
def sklearn_linear_model_linear_regression_overload(fit_intercept=True,
    copy_X=True, n_jobs=None, positive=False):
    check_sklearn_version()

    def _sklearn_linear_model_linear_regression_impl(fit_intercept=True,
        copy_X=True, n_jobs=None, positive=False):
        with numba.objmode(m='linear_regression_type'):
            m = sklearn.linear_model.LinearRegression(fit_intercept=
                fit_intercept, copy_X=copy_X, n_jobs=n_jobs, positive=positive)
        return m
    return _sklearn_linear_model_linear_regression_impl


@overload_method(BodoLinearRegressionType, 'fit', no_unliteral=True)
def overload_linear_regression_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _linear_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _linear_regression_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.LinearRegression.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _sgdc_linear_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty=None, fit_intercept=m.
                    fit_intercept)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
            return m
        return _sgdc_linear_regression_fit_impl


@overload_method(BodoLinearRegressionType, 'predict', no_unliteral=True)
def overload_linear_regression_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoLinearRegressionType, 'score', no_unliteral=True)
def overload_linear_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoLinearRegressionType, 'coef_')
def get_lr_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.coef_
        return result
    return impl


BodoLassoType = install_py_obj_class(types_name='lasso_type', python_type=
    sklearn.linear_model.Lasso, module=this_module, class_name=
    'BodoLassoType', model_name='BodoLassoModel')


@overload(sklearn.linear_model.Lasso, no_unliteral=True)
def sklearn_linear_model_lasso_overload(alpha=1.0, fit_intercept=True,
    precompute=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=
    False, positive=False, random_state=None, selection='cyclic'):
    check_sklearn_version()

    def _sklearn_linear_model_lasso_impl(alpha=1.0, fit_intercept=True,
        precompute=False, copy_X=True, max_iter=1000, tol=0.0001,
        warm_start=False, positive=False, random_state=None, selection='cyclic'
        ):
        with numba.objmode(m='lasso_type'):
            m = sklearn.linear_model.Lasso(alpha=alpha, fit_intercept=
                fit_intercept, precompute=precompute, copy_X=copy_X,
                max_iter=max_iter, tol=tol, warm_start=warm_start, positive
                =positive, random_state=random_state, selection=selection)
        return m
    return _sklearn_linear_model_lasso_impl


@overload_method(BodoLassoType, 'fit', no_unliteral=True)
def overload_lasso_fit(m, X, y, sample_weight=None, check_input=True,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _lasso_fit_impl(m, X, y, sample_weight=None, check_input=True,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight, check_input)
            return m
        return _lasso_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.Lasso.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_true(check_input):
            raise BodoError(
                "sklearn.linear_model.Lasso.fit() : 'check_input' is not supported for distributed data."
                )

        def _sgdc_lasso_fit_impl(m, X, y, sample_weight=None, check_input=
            True, _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty='l1', alpha=m.alpha,
                    fit_intercept=m.fit_intercept, max_iter=m.max_iter, tol
                    =m.tol, warm_start=m.warm_start, random_state=m.
                    random_state)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
            return m
        return _sgdc_lasso_fit_impl


@overload_method(BodoLassoType, 'predict', no_unliteral=True)
def overload_lass_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoLassoType, 'score', no_unliteral=True)
def overload_lasso_score(m, X, y, sample_weight=None, _is_data_distributed=
    False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


BodoRidgeType = install_py_obj_class(types_name='ridge_type', python_type=
    sklearn.linear_model.Ridge, module=this_module, class_name=
    'BodoRidgeType', model_name='BodoRidgeModel')


@overload(sklearn.linear_model.Ridge, no_unliteral=True)
def sklearn_linear_model_ridge_overload(alpha=1.0, fit_intercept=True,
    copy_X=True, max_iter=None, tol=0.001, solver='auto', positive=False,
    random_state=None):
    check_sklearn_version()

    def _sklearn_linear_model_ridge_impl(alpha=1.0, fit_intercept=True,
        copy_X=True, max_iter=None, tol=0.001, solver='auto', positive=
        False, random_state=None):
        with numba.objmode(m='ridge_type'):
            m = sklearn.linear_model.Ridge(alpha=alpha, fit_intercept=
                fit_intercept, copy_X=copy_X, max_iter=max_iter, tol=tol,
                solver=solver, positive=positive, random_state=random_state)
        return m
    return _sklearn_linear_model_ridge_impl


@overload_method(BodoRidgeType, 'fit', no_unliteral=True)
def overload_ridge_fit(m, X, y, sample_weight=None, _is_data_distributed=False
    ):
    if is_overload_false(_is_data_distributed):

        def _ridge_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _ridge_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.Ridge.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _ridge_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                if m.max_iter is None:
                    max_iter = 1000
                else:
                    max_iter = m.max_iter
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty='l2', alpha=0.001,
                    fit_intercept=m.fit_intercept, max_iter=max_iter, tol=m
                    .tol, random_state=m.random_state)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
            return m
        return _ridge_fit_impl


@overload_method(BodoRidgeType, 'predict', no_unliteral=True)
def overload_linear_regression_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoRidgeType, 'score', no_unliteral=True)
def overload_linear_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoRidgeType, 'coef_')
def get_ridge_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.coef_
        return result
    return impl


BodoLinearSVCType = install_py_obj_class(types_name='linear_svc_type',
    python_type=sklearn.svm.LinearSVC, module=this_module, class_name=
    'BodoLinearSVCType', model_name='BodoLinearSVCModel')


@overload(sklearn.svm.LinearSVC, no_unliteral=True)
def sklearn_svm_linear_svc_overload(penalty='l2', loss='squared_hinge',
    dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True,
    intercept_scaling=1, class_weight=None, verbose=0, random_state=None,
    max_iter=1000):
    check_sklearn_version()

    def _sklearn_svm_linear_svc_impl(penalty='l2', loss='squared_hinge',
        dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True,
        intercept_scaling=1, class_weight=None, verbose=0, random_state=
        None, max_iter=1000):
        with numba.objmode(m='linear_svc_type'):
            m = sklearn.svm.LinearSVC(penalty=penalty, loss=loss, dual=dual,
                tol=tol, C=C, multi_class=multi_class, fit_intercept=
                fit_intercept, intercept_scaling=intercept_scaling,
                class_weight=class_weight, verbose=verbose, random_state=
                random_state, max_iter=max_iter)
        return m
    return _sklearn_svm_linear_svc_impl


@overload_method(BodoLinearSVCType, 'fit', no_unliteral=True)
def overload_linear_svc_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _svm_linear_svc_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _svm_linear_svc_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.svm.LinearSVC.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _svm_linear_svc_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDClassifier')
            with numba.objmode(clf='sgd_classifier_type'):
                clf = sklearn.linear_model.SGDClassifier(loss='hinge',
                    penalty=m.penalty, tol=m.tol, fit_intercept=m.
                    fit_intercept, class_weight=m.class_weight,
                    random_state=m.random_state, max_iter=m.max_iter,
                    verbose=m.verbose)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
                m.classes_ = clf.classes_
            return m
        return _svm_linear_svc_fit_impl


@overload_method(BodoLinearSVCType, 'predict', no_unliteral=True)
def overload_svm_linear_svc_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoLinearSVCType, 'score', no_unliteral=True)
def overload_svm_linear_svc_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


BodoPreprocessingOneHotEncoderType = install_py_obj_class(types_name=
    'preprocessing_one_hot_encoder_type', python_type=sklearn.preprocessing
    .OneHotEncoder, module=this_module, class_name=
    'BodoPreprocessingOneHotEncoderType', model_name=
    'BodoPreprocessingOneHotEncoderModel')
BodoPreprocessingOneHotEncoderCategoriesType = install_py_obj_class(types_name
    ='preprocessing_one_hot_encoder_categories_type', module=this_module,
    class_name='BodoPreprocessingOneHotEncoderCategoriesType', model_name=
    'BodoPreprocessingOneHotEncoderCategoriesModel')
BodoPreprocessingOneHotEncoderDropIdxType = install_py_obj_class(types_name
    ='preprocessing_one_hot_encoder_drop_idx_type', module=this_module,
    class_name='BodoPreprocessingOneHotEncoderDropIdxType', model_name=
    'BodoPreprocessingOneHotEncoderDropIdxModel')


@overload_attribute(BodoPreprocessingOneHotEncoderType, 'categories_')
def get_one_hot_encoder_categories_(m):

    def impl(m):
        with numba.objmode(result=
            'preprocessing_one_hot_encoder_categories_type'):
            result = m.categories_
        return result
    return impl


@overload_attribute(BodoPreprocessingOneHotEncoderType, 'drop_idx_')
def get_one_hot_encoder_drop_idx_(m):

    def impl(m):
        with numba.objmode(result='preprocessing_one_hot_encoder_drop_idx_type'
            ):
            result = m.drop_idx_
        return result
    return impl


@overload_attribute(BodoPreprocessingOneHotEncoderType, 'n_features_in_')
def get_one_hot_encoder_n_features_in_(m):

    def impl(m):
        with numba.objmode(result='int64'):
            result = m.n_features_in_
        return result
    return impl


@overload(sklearn.preprocessing.OneHotEncoder, no_unliteral=True)
def sklearn_preprocessing_one_hot_encoder_overload(categories='auto', drop=
    None, sparse=True, dtype=np.float64, handle_unknown='error',
    min_frequency=None, max_categories=None):
    check_sklearn_version()
    kyczq__njh = {'sparse': sparse, 'dtype': 'float64' if 'float64' in repr
        (dtype) else repr(dtype), 'min_frequency': min_frequency,
        'max_categories': max_categories}
    zezmy__quuu = {'sparse': False, 'dtype': 'float64', 'min_frequency':
        None, 'max_categories': None}
    check_unsupported_args('OneHotEncoder', kyczq__njh, zezmy__quuu, 'ml')

    def _sklearn_preprocessing_one_hot_encoder_impl(categories='auto', drop
        =None, sparse=True, dtype=np.float64, handle_unknown='error',
        min_frequency=None, max_categories=None):
        with numba.objmode(m='preprocessing_one_hot_encoder_type'):
            m = sklearn.preprocessing.OneHotEncoder(categories=categories,
                drop=drop, sparse=sparse, dtype=dtype, handle_unknown=
                handle_unknown, min_frequency=min_frequency, max_categories
                =max_categories)
        return m
    return _sklearn_preprocessing_one_hot_encoder_impl


def sklearn_preprocessing_one_hot_encoder_fit_dist_helper(m, X):
    ubwg__enu = MPI.COMM_WORLD
    try:
        m._validate_keywords()
        jaz__doha = m._fit(X, handle_unknown=m.handle_unknown,
            force_all_finite='allow-nan', return_counts=m._infrequent_enabled)
    except ValueError as rzx__qxqwu:
        if 'Found unknown categories' in rzx__qxqwu.args[0]:
            jaz__doha = rzx__qxqwu
        else:
            raise rzx__qxqwu
    cwl__ogcv = int(isinstance(jaz__doha, ValueError))
    wxt__ewv, rxvf__yip = ubwg__enu.allreduce((cwl__ogcv, ubwg__enu.
        Get_rank()), op=MPI.MAXLOC)
    if wxt__ewv:
        if ubwg__enu.Get_rank() == rxvf__yip:
            xsouf__vqn = jaz__doha.args[0]
        else:
            xsouf__vqn = None
        xsouf__vqn = ubwg__enu.bcast(xsouf__vqn, root=rxvf__yip)
        if cwl__ogcv:
            raise jaz__doha
        else:
            raise ValueError(xsouf__vqn)
    if m.categories == 'auto':
        jsli__sjb = m.categories_
        abc__bzx = []
        for ipyeq__gxgq in jsli__sjb:
            qywf__ndmkn = bodo.allgatherv(ipyeq__gxgq)
            mlia__dfy = _unique(qywf__ndmkn)
            abc__bzx.append(mlia__dfy)
        m.categories_ = abc__bzx
    if m._infrequent_enabled:
        m._fit_infrequent_category_mapping(jaz__doha['n_samples'],
            jaz__doha['category_counts'])
    m.drop_idx_ = m._compute_drop_idx()
    m._n_features_outs = m._compute_n_features_outs()
    return m


@overload_method(BodoPreprocessingOneHotEncoderType, 'fit', no_unliteral=True)
def overload_preprocessing_one_hot_encoder_fit(m, X, y=None,
    _is_data_distributed=False):
    ecax__osooi = 'def _preprocessing_one_hot_encoder_fit_impl(\n'
    ecax__osooi += '    m, X, y=None, _is_data_distributed=False\n'
    ecax__osooi += '):\n'
    ecax__osooi += (
        "    with numba.objmode(m='preprocessing_one_hot_encoder_type'):\n")
    ecax__osooi += """        if X.ndim == 1 and isinstance(X[0], (np.ndarray, pd.arrays.ArrowStringArray)):
"""
    ecax__osooi += '            X = np.vstack(X)\n'
    if is_overload_true(_is_data_distributed):
        ecax__osooi += (
            '        m = sklearn_preprocessing_one_hot_encoder_fit_dist_helper(m, X)\n'
            )
    else:
        ecax__osooi += '        m = m.fit(X, y)\n'
    ecax__osooi += '    return m\n'
    wxn__kvxay = {}
    exec(ecax__osooi, globals(), wxn__kvxay)
    iencu__wgin = wxn__kvxay['_preprocessing_one_hot_encoder_fit_impl']
    return iencu__wgin


@overload_method(BodoPreprocessingOneHotEncoderType, 'transform',
    no_unliteral=True)
def overload_preprocessing_one_hot_encoder_transform(m, X):

    def _preprocessing_one_hot_encoder_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            if X.ndim == 1 and isinstance(X[0], (np.ndarray, pd.arrays.
                ArrowStringArray)):
                X = np.vstack(X)
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_one_hot_encoder_transform_impl


@overload_method(BodoPreprocessingOneHotEncoderType,
    'get_feature_names_out', no_unliteral=True)
def overload_preprocessing_one_hot_encoder_get_feature_names_out(m,
    input_features=None):

    def _preprocessing_one_hot_encoder_get_feature_names_out_impl(m,
        input_features=None):
        with numba.objmode(out_features='string[:]'):
            out_features = get_feature_names_out(input_features)
        return out_features
    return _preprocessing_one_hot_encoder_get_feature_names_out_impl


BodoPreprocessingStandardScalerType = install_py_obj_class(types_name=
    'preprocessing_standard_scaler_type', python_type=sklearn.preprocessing
    .StandardScaler, module=this_module, class_name=
    'BodoPreprocessingStandardScalerType', model_name=
    'BodoPreprocessingStandardScalerModel')


@overload(sklearn.preprocessing.StandardScaler, no_unliteral=True)
def sklearn_preprocessing_standard_scaler_overload(copy=True, with_mean=
    True, with_std=True):
    check_sklearn_version()

    def _sklearn_preprocessing_standard_scaler_impl(copy=True, with_mean=
        True, with_std=True):
        with numba.objmode(m='preprocessing_standard_scaler_type'):
            m = sklearn.preprocessing.StandardScaler(copy=copy, with_mean=
                with_mean, with_std=with_std)
        return m
    return _sklearn_preprocessing_standard_scaler_impl


def sklearn_preprocessing_standard_scaler_fit_dist_helper(m, X):
    ubwg__enu = MPI.COMM_WORLD
    sws__brwxq = ubwg__enu.Get_size()
    rwjyl__siov = m.with_std
    gjkwd__iamrq = m.with_mean
    m.with_std = False
    if rwjyl__siov:
        m.with_mean = True
    m = m.fit(X)
    m.with_std = rwjyl__siov
    m.with_mean = gjkwd__iamrq
    if not isinstance(m.n_samples_seen_, numbers.Integral):
        gybe__ggqa = False
    else:
        gybe__ggqa = True
        m.n_samples_seen_ = np.repeat(m.n_samples_seen_, X.shape[1]).astype(np
            .int64, copy=False)
    qwtfm__isage = np.zeros((sws__brwxq, *m.n_samples_seen_.shape), dtype=m
        .n_samples_seen_.dtype)
    ubwg__enu.Allgather(m.n_samples_seen_, qwtfm__isage)
    civt__gxend = np.sum(qwtfm__isage, axis=0)
    m.n_samples_seen_ = civt__gxend
    if m.with_mean or m.with_std:
        bqhnh__yqiix = np.zeros((sws__brwxq, *m.mean_.shape), dtype=m.mean_
            .dtype)
        ubwg__enu.Allgather(m.mean_, bqhnh__yqiix)
        bqhnh__yqiix[np.isnan(bqhnh__yqiix)] = 0
        tfpm__dmhth = np.average(bqhnh__yqiix, axis=0, weights=qwtfm__isage)
        m.mean_ = tfpm__dmhth
    if m.with_std:
        drxkj__yel = sklearn_safe_accumulator_op(np.nansum, (X -
            tfpm__dmhth) ** 2, axis=0) / civt__gxend
        gooe__vbbpj = np.zeros_like(drxkj__yel)
        ubwg__enu.Allreduce(drxkj__yel, gooe__vbbpj, op=MPI.SUM)
        m.var_ = gooe__vbbpj
        m.scale_ = sklearn_handle_zeros_in_scale(np.sqrt(m.var_))
    gybe__ggqa = ubwg__enu.allreduce(gybe__ggqa, op=MPI.LAND)
    if gybe__ggqa:
        m.n_samples_seen_ = m.n_samples_seen_[0]
    return m


@overload_method(BodoPreprocessingStandardScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_standard_scaler_fit(m, X, y=None, sample_weight=
    None, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.preprocessing.StandardScaler.fit(): 'sample_weight' is not supported for distributed data."
                )

        def _preprocessing_standard_scaler_fit_impl(m, X, y=None,
            sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='preprocessing_standard_scaler_type'):
                m = sklearn_preprocessing_standard_scaler_fit_dist_helper(m, X)
            return m
    else:

        def _preprocessing_standard_scaler_fit_impl(m, X, y=None,
            sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='preprocessing_standard_scaler_type'):
                m = m.fit(X, y, sample_weight)
            return m
    return _preprocessing_standard_scaler_fit_impl


@overload_method(BodoPreprocessingStandardScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_standard_scaler_transform(m, X, copy=None):
    if isinstance(X, CSRMatrixType):
        types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types
            .int64)

        def _preprocessing_standard_scaler_transform_impl(m, X, copy=None):
            with numba.objmode(transformed_X='csr_matrix_float64_int64'):
                transformed_X = m.transform(X, copy=copy)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
    else:

        def _preprocessing_standard_scaler_transform_impl(m, X, copy=None):
            with numba.objmode(transformed_X='float64[:,:]'):
                transformed_X = m.transform(X, copy=copy)
            return transformed_X
    return _preprocessing_standard_scaler_transform_impl


@overload_method(BodoPreprocessingStandardScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_standard_scaler_inverse_transform(m, X, copy=None):
    if isinstance(X, CSRMatrixType):
        types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types
            .int64)

        def _preprocessing_standard_scaler_inverse_transform_impl(m, X,
            copy=None):
            with numba.objmode(inverse_transformed_X='csr_matrix_float64_int64'
                ):
                inverse_transformed_X = m.inverse_transform(X, copy=copy)
                inverse_transformed_X.indices = (inverse_transformed_X.
                    indices.astype(np.int64))
                inverse_transformed_X.indptr = (inverse_transformed_X.
                    indptr.astype(np.int64))
            return inverse_transformed_X
    else:

        def _preprocessing_standard_scaler_inverse_transform_impl(m, X,
            copy=None):
            with numba.objmode(inverse_transformed_X='float64[:,:]'):
                inverse_transformed_X = m.inverse_transform(X, copy=copy)
            return inverse_transformed_X
    return _preprocessing_standard_scaler_inverse_transform_impl


BodoPreprocessingMaxAbsScalerType = install_py_obj_class(types_name=
    'preprocessing_max_abs_scaler_type', python_type=sklearn.preprocessing.
    MaxAbsScaler, module=this_module, class_name=
    'BodoPreprocessingMaxAbsScalerType', model_name=
    'BodoPreprocessingMaxAbsScalerModel')


@overload_attribute(BodoPreprocessingMaxAbsScalerType, 'scale_')
def get_max_abs_scaler_scale_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.scale_
        return result
    return impl


@overload_attribute(BodoPreprocessingMaxAbsScalerType, 'max_abs_')
def get_max_abs_scaler_max_abs_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.max_abs_
        return result
    return impl


@overload_attribute(BodoPreprocessingMaxAbsScalerType, 'n_samples_seen_')
def get_max_abs_scaler_n_samples_seen_(m):

    def impl(m):
        with numba.objmode(result='int64'):
            result = m.n_samples_seen_
        return result
    return impl


@overload(sklearn.preprocessing.MaxAbsScaler, no_unliteral=True)
def sklearn_preprocessing_max_abs_scaler_overload(copy=True):
    check_sklearn_version()

    def _sklearn_preprocessing_max_abs_scaler_impl(copy=True):
        with numba.objmode(m='preprocessing_max_abs_scaler_type'):
            m = sklearn.preprocessing.MaxAbsScaler(copy=copy)
        return m
    return _sklearn_preprocessing_max_abs_scaler_impl


def sklearn_preprocessing_max_abs_scaler_fit_dist_helper(m, X, partial=False):
    ubwg__enu = MPI.COMM_WORLD
    sws__brwxq = ubwg__enu.Get_size()
    if hasattr(m, 'n_samples_seen_'):
        vowd__fuho = m.n_samples_seen_
    else:
        vowd__fuho = 0
    if partial:
        m = m.partial_fit(X)
    else:
        m = m.fit(X)
    civt__gxend = ubwg__enu.allreduce(m.n_samples_seen_ - vowd__fuho, op=
        MPI.SUM)
    m.n_samples_seen_ = civt__gxend + vowd__fuho
    vwoe__gykru = np.zeros((sws__brwxq, *m.max_abs_.shape), dtype=m.
        max_abs_.dtype)
    ubwg__enu.Allgather(m.max_abs_, vwoe__gykru)
    kfei__crq = np.nanmax(vwoe__gykru, axis=0)
    m.scale_ = sklearn_handle_zeros_in_scale(kfei__crq)
    m.max_abs_ = kfei__crq
    return m


@overload_method(BodoPreprocessingMaxAbsScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_max_abs_scaler_fit(m, X, y=None,
    _is_data_distributed=False):
    if _is_data_distributed:

        def _preprocessing_max_abs_scaler_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_max_abs_scaler_type'):
                m = sklearn_preprocessing_max_abs_scaler_fit_dist_helper(m,
                    X, partial=False)
            return m
    else:

        def _preprocessing_max_abs_scaler_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_max_abs_scaler_type'):
                m = m.fit(X, y)
            return m
    return _preprocessing_max_abs_scaler_fit_impl


@overload_method(BodoPreprocessingMaxAbsScalerType, 'partial_fit',
    no_unliteral=True)
def overload_preprocessing_max_abs_scaler_partial_fit(m, X, y=None,
    _is_data_distributed=False):
    if _is_data_distributed:

        def _preprocessing_max_abs_scaler_partial_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_max_abs_scaler_type'):
                m = sklearn_preprocessing_max_abs_scaler_fit_dist_helper(m,
                    X, partial=True)
            return m
    else:

        def _preprocessing_max_abs_scaler_partial_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_max_abs_scaler_type'):
                m = m.partial_fit(X, y)
            return m
    return _preprocessing_max_abs_scaler_partial_fit_impl


@overload_method(BodoPreprocessingMaxAbsScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_max_abs_scaler_transform(m, X):
    if isinstance(X, CSRMatrixType):
        types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types
            .int64)

        def _preprocessing_max_abs_scaler_transform_impl(m, X):
            with numba.objmode(transformed_X='csr_matrix_float64_int64'):
                transformed_X = m.transform(X)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
    else:

        def _preprocessing_max_abs_scaler_transform_impl(m, X):
            with numba.objmode(transformed_X='float64[:,:]'):
                transformed_X = m.transform(X)
            return transformed_X
    return _preprocessing_max_abs_scaler_transform_impl


@overload_method(BodoPreprocessingMaxAbsScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_max_abs_scaler_inverse_transform(m, X):
    if isinstance(X, CSRMatrixType):
        types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types
            .int64)

        def _preprocessing_max_abs_scaler_inverse_transform_impl(m, X):
            with numba.objmode(inverse_transformed_X='csr_matrix_float64_int64'
                ):
                inverse_transformed_X = m.inverse_transform(X)
                inverse_transformed_X.indices = (inverse_transformed_X.
                    indices.astype(np.int64))
                inverse_transformed_X.indptr = (inverse_transformed_X.
                    indptr.astype(np.int64))
            return inverse_transformed_X
    else:

        def _preprocessing_max_abs_scaler_inverse_transform_impl(m, X):
            with numba.objmode(inverse_transformed_X='float64[:,:]'):
                inverse_transformed_X = m.inverse_transform(X)
            return inverse_transformed_X
    return _preprocessing_max_abs_scaler_inverse_transform_impl


BodoModelSelectionLeavePOutType = install_py_obj_class(types_name=
    'model_selection_leave_p_out_type', python_type=sklearn.model_selection
    .LeavePOut, module=this_module, class_name=
    'BodoModelSelectionLeavePOutType', model_name=
    'BodoModelSelectionLeavePOutModel')
BodoModelSelectionLeavePOutGeneratorType = install_py_obj_class(types_name=
    'model_selection_leave_p_out_generator_type', module=this_module,
    class_name='BodoModelSelectionLeavePOutGeneratorType', model_name=
    'BodoModelSelectionLeavePOutGeneratorModel')


@overload(sklearn.model_selection.LeavePOut, no_unliteral=True)
def sklearn_model_selection_leave_p_out_overload(p):
    check_sklearn_version()

    def _sklearn_model_selection_leave_p_out_impl(p):
        with numba.objmode(m='model_selection_leave_p_out_type'):
            m = sklearn.model_selection.LeavePOut(p=p)
        return m
    return _sklearn_model_selection_leave_p_out_impl


def sklearn_model_selection_leave_p_out_generator_dist_helper(m, X):
    joef__cwkce = bodo.get_rank()
    qbjc__iqg = bodo.get_size()
    mrds__vcrhh = np.empty(qbjc__iqg, np.int64)
    bodo.libs.distributed_api.allgather(mrds__vcrhh, len(X))
    if joef__cwkce > 0:
        psg__qnp = np.sum(mrds__vcrhh[:joef__cwkce])
    else:
        psg__qnp = 0
    ejl__nytw = psg__qnp + mrds__vcrhh[joef__cwkce]
    ysx__iiita = np.sum(mrds__vcrhh)
    if ysx__iiita <= m.p:
        raise ValueError(
            f'p={m.p} must be strictly less than the number of samples={ysx__iiita}'
            )
    xlec__spg = np.arange(psg__qnp, ejl__nytw)
    for dkbd__dybz in combinations(range(ysx__iiita), m.p):
        dncex__macf = np.array(dkbd__dybz)
        dncex__macf = dncex__macf[dncex__macf >= psg__qnp]
        dncex__macf = dncex__macf[dncex__macf < ejl__nytw]
        wrbmk__ymt = np.zeros(len(X), dtype=bool)
        wrbmk__ymt[dncex__macf - psg__qnp] = True
        sjs__ree = xlec__spg[np.logical_not(wrbmk__ymt)]
        yield sjs__ree, dncex__macf


@overload_method(BodoModelSelectionLeavePOutType, 'split', no_unliteral=True)
def overload_model_selection_leave_p_out_generator(m, X, y=None, groups=
    None, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _model_selection_leave_p_out_generator_impl(m, X, y=None,
            groups=None, _is_data_distributed=False):
            with numba.objmode(gen='model_selection_leave_p_out_generator_type'
                ):
                gen = (
                    sklearn_model_selection_leave_p_out_generator_dist_helper
                    (m, X))
            return gen
    else:

        def _model_selection_leave_p_out_generator_impl(m, X, y=None,
            groups=None, _is_data_distributed=False):
            with numba.objmode(gen='model_selection_leave_p_out_generator_type'
                ):
                gen = m.split(X, y=y, groups=groups)
            return gen
    return _model_selection_leave_p_out_generator_impl


@overload_method(BodoModelSelectionLeavePOutType, 'get_n_splits',
    no_unliteral=True)
def overload_model_selection_leave_p_out_get_n_splits(m, X, y=None, groups=
    None, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _model_selection_leave_p_out_get_n_splits_impl(m, X, y=None,
            groups=None, _is_data_distributed=False):
            with numba.objmode(out='int64'):
                ysx__iiita = bodo.libs.distributed_api.dist_reduce(len(X),
                    np.int32(Reduce_Type.Sum.value))
                out = int(comb(ysx__iiita, m.p, exact=True))
            return out
    else:

        def _model_selection_leave_p_out_get_n_splits_impl(m, X, y=None,
            groups=None, _is_data_distributed=False):
            with numba.objmode(out='int64'):
                out = m.get_n_splits(X)
            return out
    return _model_selection_leave_p_out_get_n_splits_impl


BodoModelSelectionKFoldType = install_py_obj_class(types_name=
    'model_selection_kfold_type', python_type=sklearn.model_selection.KFold,
    module=this_module, class_name='BodoModelSelectionKFoldType',
    model_name='BodoModelSelectionKFoldModel')


@overload(sklearn.model_selection.KFold, no_unliteral=True)
def sklearn_model_selection_kfold_overload(n_splits=5, shuffle=False,
    random_state=None):
    check_sklearn_version()

    def _sklearn_model_selection_kfold_impl(n_splits=5, shuffle=False,
        random_state=None):
        with numba.objmode(m='model_selection_kfold_type'):
            m = sklearn.model_selection.KFold(n_splits=n_splits, shuffle=
                shuffle, random_state=random_state)
        return m
    return _sklearn_model_selection_kfold_impl


def sklearn_model_selection_kfold_generator_dist_helper(m, X, y=None,
    groups=None):
    joef__cwkce = bodo.get_rank()
    qbjc__iqg = bodo.get_size()
    mrds__vcrhh = np.empty(qbjc__iqg, np.int64)
    bodo.libs.distributed_api.allgather(mrds__vcrhh, len(X))
    if joef__cwkce > 0:
        psg__qnp = np.sum(mrds__vcrhh[:joef__cwkce])
    else:
        psg__qnp = 0
    ejl__nytw = psg__qnp + len(X)
    ysx__iiita = np.sum(mrds__vcrhh)
    if ysx__iiita < m.n_splits:
        raise ValueError(
            f'number of splits n_splits={m.n_splits} greater than the number of samples {ysx__iiita}'
            )
    ntj__ppw = np.arange(ysx__iiita)
    if m.shuffle:
        if m.random_state is None:
            tsgpa__urj = bodo.libs.distributed_api.bcast_scalar(np.random.
                randint(0, 2 ** 31))
            np.random.seed(tsgpa__urj)
        else:
            np.random.seed(m.random_state)
        np.random.shuffle(ntj__ppw)
    xlec__spg = ntj__ppw[psg__qnp:ejl__nytw]
    ouqyi__szz = np.full(m.n_splits, ysx__iiita // (qbjc__iqg * m.n_splits),
        dtype=np.int32)
    ifav__nzhd = ysx__iiita % (qbjc__iqg * m.n_splits)
    rugw__eyuw = np.full(m.n_splits, ifav__nzhd // m.n_splits, dtype=int)
    rugw__eyuw[:ifav__nzhd % m.n_splits] += 1
    oclgi__evu = np.repeat(np.arange(m.n_splits), rugw__eyuw)
    xsbi__gqyby = oclgi__evu[joef__cwkce::qbjc__iqg]
    ouqyi__szz[xsbi__gqyby] += 1
    dpdjw__lzw = 0
    for ega__gho in ouqyi__szz:
        xbkym__inu = dpdjw__lzw + ega__gho
        dncex__macf = xlec__spg[dpdjw__lzw:xbkym__inu]
        sjs__ree = np.concatenate((xlec__spg[:dpdjw__lzw], xlec__spg[
            xbkym__inu:]), axis=0)
        yield sjs__ree, dncex__macf
        dpdjw__lzw = xbkym__inu


@overload_method(BodoModelSelectionKFoldType, 'split', no_unliteral=True)
def overload_model_selection_kfold_generator(m, X, y=None, groups=None,
    _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _model_selection_kfold_generator_impl(m, X, y=None, groups=None,
            _is_data_distributed=False):
            with numba.objmode(gen='List(UniTuple(int64[:], 2))'):
                gen = list(sklearn_model_selection_kfold_generator_dist_helper
                    (m, X, y=None, groups=None))
            return gen
    else:

        def _model_selection_kfold_generator_impl(m, X, y=None, groups=None,
            _is_data_distributed=False):
            with numba.objmode(gen='List(UniTuple(int64[:], 2))'):
                gen = list(m.split(X, y=y, groups=groups))
            return gen
    return _model_selection_kfold_generator_impl


@overload_method(BodoModelSelectionKFoldType, 'get_n_splits', no_unliteral=True
    )
def overload_model_selection_kfold_get_n_splits(m, X=None, y=None, groups=
    None, _is_data_distributed=False):

    def _model_selection_kfold_get_n_splits_impl(m, X=None, y=None, groups=
        None, _is_data_distributed=False):
        with numba.objmode(out='int64'):
            out = m.n_splits
        return out
    return _model_selection_kfold_get_n_splits_impl


def get_data_slice_parallel(data, labels, len_train):
    cgny__tiyod = data[:len_train]
    tzjs__bslif = data[len_train:]
    cgny__tiyod = bodo.rebalance(cgny__tiyod)
    tzjs__bslif = bodo.rebalance(tzjs__bslif)
    magc__jshj = labels[:len_train]
    onsr__cblf = labels[len_train:]
    magc__jshj = bodo.rebalance(magc__jshj)
    onsr__cblf = bodo.rebalance(onsr__cblf)
    return cgny__tiyod, tzjs__bslif, magc__jshj, onsr__cblf


@numba.njit
def get_train_test_size(train_size, test_size):
    if train_size is None:
        train_size = -1.0
    if test_size is None:
        test_size = -1.0
    if train_size == -1.0 and test_size == -1.0:
        return 0.75, 0.25
    elif test_size == -1.0:
        return train_size, 1.0 - train_size
    elif train_size == -1.0:
        return 1.0 - test_size, test_size
    elif train_size + test_size > 1:
        raise ValueError(
            'The sum of test_size and train_size, should be in the (0, 1) range. Reduce test_size and/or train_size.'
            )
    else:
        return train_size, test_size


def set_labels_type(labels, label_type):
    return labels


@overload(set_labels_type, no_unliteral=True)
def overload_set_labels_type(labels, label_type):
    if get_overload_const_int(label_type) == 1:

        def _set_labels(labels, label_type):
            return pd.Series(labels)
        return _set_labels
    elif get_overload_const_int(label_type) == 2:

        def _set_labels(labels, label_type):
            return labels.values
        return _set_labels
    else:

        def _set_labels(labels, label_type):
            return labels
        return _set_labels


def reset_labels_type(labels, label_type):
    return labels


@overload(reset_labels_type, no_unliteral=True)
def overload_reset_labels_type(labels, label_type):
    if get_overload_const_int(label_type) == 1:

        def _reset_labels(labels, label_type):
            return labels.values
        return _reset_labels
    elif get_overload_const_int(label_type) == 2:

        def _reset_labels(labels, label_type):
            return pd.Series(labels, index=np.arange(len(labels)))
        return _reset_labels
    else:

        def _reset_labels(labels, label_type):
            return labels
        return _reset_labels


@overload(sklearn.model_selection.train_test_split, no_unliteral=True)
def overload_train_test_split(data, labels=None, train_size=None, test_size
    =None, random_state=None, shuffle=True, stratify=None,
    _is_data_distributed=False):
    check_sklearn_version()
    kyczq__njh = {'stratify': stratify}
    zezmy__quuu = {'stratify': None}
    check_unsupported_args('train_test_split', kyczq__njh, zezmy__quuu, 'ml')
    if is_overload_false(_is_data_distributed):
        yafez__erny = f'data_split_type_{numba.core.ir_utils.next_label()}'
        enz__hnp = f'labels_split_type_{numba.core.ir_utils.next_label()}'
        for ivf__bpp, ibbih__prc in ((data, yafez__erny), (labels, enz__hnp)):
            if isinstance(ivf__bpp, (DataFrameType, SeriesType)):
                unppj__uroez = ivf__bpp.copy(index=NumericIndexType(types.
                    int64))
                setattr(types, ibbih__prc, unppj__uroez)
            else:
                setattr(types, ibbih__prc, ivf__bpp)
        ecax__osooi = 'def _train_test_split_impl(\n'
        ecax__osooi += '    data,\n'
        ecax__osooi += '    labels=None,\n'
        ecax__osooi += '    train_size=None,\n'
        ecax__osooi += '    test_size=None,\n'
        ecax__osooi += '    random_state=None,\n'
        ecax__osooi += '    shuffle=True,\n'
        ecax__osooi += '    stratify=None,\n'
        ecax__osooi += '    _is_data_distributed=False,\n'
        ecax__osooi += '):  # pragma: no cover\n'
        ecax__osooi += (
            """    with numba.objmode(data_train='{}', data_test='{}', labels_train='{}', labels_test='{}'):
"""
            .format(yafez__erny, yafez__erny, enz__hnp, enz__hnp))
        ecax__osooi += """        data_train, data_test, labels_train, labels_test = sklearn.model_selection.train_test_split(
"""
        ecax__osooi += '            data,\n'
        ecax__osooi += '            labels,\n'
        ecax__osooi += '            train_size=train_size,\n'
        ecax__osooi += '            test_size=test_size,\n'
        ecax__osooi += '            random_state=random_state,\n'
        ecax__osooi += '            shuffle=shuffle,\n'
        ecax__osooi += '            stratify=stratify,\n'
        ecax__osooi += '        )\n'
        ecax__osooi += (
            '    return data_train, data_test, labels_train, labels_test\n')
        wxn__kvxay = {}
        exec(ecax__osooi, globals(), wxn__kvxay)
        _train_test_split_impl = wxn__kvxay['_train_test_split_impl']
        return _train_test_split_impl
    else:
        global get_data_slice_parallel
        if isinstance(get_data_slice_parallel, pytypes.FunctionType):
            get_data_slice_parallel = bodo.jit(get_data_slice_parallel,
                all_args_distributed_varlength=True,
                all_returns_distributed=True)
        label_type = 0
        if isinstance(data, DataFrameType) and isinstance(labels, types.Array):
            label_type = 1
        elif isinstance(data, types.Array) and isinstance(labels, SeriesType):
            label_type = 2
        if is_overload_none(random_state):
            random_state = 42

        def _train_test_split_impl(data, labels=None, train_size=None,
            test_size=None, random_state=None, shuffle=True, stratify=None,
            _is_data_distributed=False):
            if data.shape[0] != labels.shape[0]:
                raise ValueError(
                    'Found input variables with inconsistent number of samples\n'
                    )
            train_size, test_size = get_train_test_size(train_size, test_size)
            ysx__iiita = bodo.libs.distributed_api.dist_reduce(len(data),
                np.int32(Reduce_Type.Sum.value))
            len_train = int(ysx__iiita * train_size)
            exb__xqo = ysx__iiita - len_train
            if shuffle:
                labels = set_labels_type(labels, label_type)
                joef__cwkce = bodo.get_rank()
                qbjc__iqg = bodo.get_size()
                mrds__vcrhh = np.empty(qbjc__iqg, np.int64)
                bodo.libs.distributed_api.allgather(mrds__vcrhh, len(data))
                jagcq__giqv = np.cumsum(mrds__vcrhh[0:joef__cwkce + 1])
                qcgxo__grgvw = np.full(ysx__iiita, True)
                qcgxo__grgvw[:exb__xqo] = False
                np.random.seed(42)
                np.random.permutation(qcgxo__grgvw)
                if joef__cwkce:
                    dpdjw__lzw = jagcq__giqv[joef__cwkce - 1]
                else:
                    dpdjw__lzw = 0
                rqd__ndhc = jagcq__giqv[joef__cwkce]
                abhav__gmhgj = qcgxo__grgvw[dpdjw__lzw:rqd__ndhc]
                cgny__tiyod = data[abhav__gmhgj]
                tzjs__bslif = data[~abhav__gmhgj]
                magc__jshj = labels[abhav__gmhgj]
                onsr__cblf = labels[~abhav__gmhgj]
                cgny__tiyod = bodo.random_shuffle(cgny__tiyod, seed=
                    random_state, parallel=True)
                tzjs__bslif = bodo.random_shuffle(tzjs__bslif, seed=
                    random_state, parallel=True)
                magc__jshj = bodo.random_shuffle(magc__jshj, seed=
                    random_state, parallel=True)
                onsr__cblf = bodo.random_shuffle(onsr__cblf, seed=
                    random_state, parallel=True)
                magc__jshj = reset_labels_type(magc__jshj, label_type)
                onsr__cblf = reset_labels_type(onsr__cblf, label_type)
            else:
                cgny__tiyod, tzjs__bslif, magc__jshj, onsr__cblf = (
                    get_data_slice_parallel(data, labels, len_train))
            return cgny__tiyod, tzjs__bslif, magc__jshj, onsr__cblf
        return _train_test_split_impl


@overload(sklearn.utils.shuffle, no_unliteral=True)
def sklearn_utils_shuffle_overload(data, random_state=None, n_samples=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):
        yafez__erny = f'utils_shuffle_type_{numba.core.ir_utils.next_label()}'
        if isinstance(data, (DataFrameType, SeriesType)):
            bnn__iarl = data.copy(index=NumericIndexType(types.int64))
            setattr(types, yafez__erny, bnn__iarl)
        else:
            setattr(types, yafez__erny, data)
        ecax__osooi = 'def _utils_shuffle_impl(\n'
        ecax__osooi += (
            '    data, random_state=None, n_samples=None, _is_data_distributed=False\n'
            )
        ecax__osooi += '):\n'
        ecax__osooi += f"    with numba.objmode(out='{yafez__erny}'):\n"
        ecax__osooi += '        out = sklearn.utils.shuffle(\n'
        ecax__osooi += (
            '            data, random_state=random_state, n_samples=n_samples\n'
            )
        ecax__osooi += '        )\n'
        ecax__osooi += '    return out\n'
        wxn__kvxay = {}
        exec(ecax__osooi, globals(), wxn__kvxay)
        _utils_shuffle_impl = wxn__kvxay['_utils_shuffle_impl']
    else:

        def _utils_shuffle_impl(data, random_state=None, n_samples=None,
            _is_data_distributed=False):
            m = bodo.random_shuffle(data, seed=random_state, n_samples=
                n_samples, parallel=True)
            return m
    return _utils_shuffle_impl


BodoPreprocessingMinMaxScalerType = install_py_obj_class(types_name=
    'preprocessing_minmax_scaler_type', python_type=sklearn.preprocessing.
    MinMaxScaler, module=this_module, class_name=
    'BodoPreprocessingMinMaxScalerType', model_name=
    'BodoPreprocessingMinMaxScalerModel')


@overload(sklearn.preprocessing.MinMaxScaler, no_unliteral=True)
def sklearn_preprocessing_minmax_scaler_overload(feature_range=(0, 1), copy
    =True, clip=False):
    check_sklearn_version()

    def _sklearn_preprocessing_minmax_scaler_impl(feature_range=(0, 1),
        copy=True, clip=False):
        with numba.objmode(m='preprocessing_minmax_scaler_type'):
            m = sklearn.preprocessing.MinMaxScaler(feature_range=
                feature_range, copy=copy, clip=clip)
        return m
    return _sklearn_preprocessing_minmax_scaler_impl


def sklearn_preprocessing_minmax_scaler_fit_dist_helper(m, X):
    ubwg__enu = MPI.COMM_WORLD
    sws__brwxq = ubwg__enu.Get_size()
    m = m.fit(X)
    civt__gxend = ubwg__enu.allreduce(m.n_samples_seen_, op=MPI.SUM)
    m.n_samples_seen_ = civt__gxend
    won__aeqiy = np.zeros((sws__brwxq, *m.data_min_.shape), dtype=m.
        data_min_.dtype)
    ubwg__enu.Allgather(m.data_min_, won__aeqiy)
    fxg__pnszw = np.nanmin(won__aeqiy, axis=0)
    ryv__inmqk = np.zeros((sws__brwxq, *m.data_max_.shape), dtype=m.
        data_max_.dtype)
    ubwg__enu.Allgather(m.data_max_, ryv__inmqk)
    dknq__msyvm = np.nanmax(ryv__inmqk, axis=0)
    scyk__tcjd = dknq__msyvm - fxg__pnszw
    m.scale_ = (m.feature_range[1] - m.feature_range[0]
        ) / sklearn_handle_zeros_in_scale(scyk__tcjd)
    m.min_ = m.feature_range[0] - fxg__pnszw * m.scale_
    m.data_min_ = fxg__pnszw
    m.data_max_ = dknq__msyvm
    m.data_range_ = scyk__tcjd
    return m


@overload_method(BodoPreprocessingMinMaxScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_minmax_scaler_fit(m, X, y=None,
    _is_data_distributed=False):

    def _preprocessing_minmax_scaler_fit_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(m='preprocessing_minmax_scaler_type'):
            if _is_data_distributed:
                m = sklearn_preprocessing_minmax_scaler_fit_dist_helper(m, X)
            else:
                m = m.fit(X, y)
        return m
    return _preprocessing_minmax_scaler_fit_impl


@overload_method(BodoPreprocessingMinMaxScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_minmax_scaler_transform(m, X):

    def _preprocessing_minmax_scaler_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_minmax_scaler_transform_impl


@overload_method(BodoPreprocessingMinMaxScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_minmax_scaler_inverse_transform(m, X):

    def _preprocessing_minmax_scaler_inverse_transform_impl(m, X):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X)
        return inverse_transformed_X
    return _preprocessing_minmax_scaler_inverse_transform_impl


BodoPreprocessingRobustScalerType = install_py_obj_class(types_name=
    'preprocessing_robust_scaler_type', python_type=sklearn.preprocessing.
    RobustScaler, module=this_module, class_name=
    'BodoPreprocessingRobustScalerType', model_name=
    'BodoPreprocessingRobustScalerModel')


@overload_attribute(BodoPreprocessingRobustScalerType, 'with_centering')
def get_robust_scaler_with_centering(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.with_centering
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'with_scaling')
def get_robust_scaler_with_scaling(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.with_scaling
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'quantile_range')
def get_robust_scaler_quantile_range(m):
    fsep__butfi = numba.typeof((25.0, 75.0))

    def impl(m):
        with numba.objmode(result=fsep__butfi):
            result = m.quantile_range
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'unit_variance')
def get_robust_scaler_unit_variance(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.unit_variance
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'copy')
def get_robust_scaler_copy(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.copy
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'center_')
def get_robust_scaler_center_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.center_
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'scale_')
def get_robust_scaler_scale_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.scale_
        return result
    return impl


@overload(sklearn.preprocessing.RobustScaler, no_unliteral=True)
def sklearn_preprocessing_robust_scaler_overload(with_centering=True,
    with_scaling=True, quantile_range=(25.0, 75.0), copy=True,
    unit_variance=False):
    check_sklearn_version()

    def _sklearn_preprocessing_robust_scaler_impl(with_centering=True,
        with_scaling=True, quantile_range=(25.0, 75.0), copy=True,
        unit_variance=False):
        with numba.objmode(m='preprocessing_robust_scaler_type'):
            m = sklearn.preprocessing.RobustScaler(with_centering=
                with_centering, with_scaling=with_scaling, quantile_range=
                quantile_range, copy=copy, unit_variance=unit_variance)
        return m
    return _sklearn_preprocessing_robust_scaler_impl


@overload_method(BodoPreprocessingRobustScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_robust_scaler_fit(m, X, y=None,
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_true(_is_data_distributed):
        ecax__osooi = f'def preprocessing_robust_scaler_fit_impl(\n'
        ecax__osooi += f'  m, X, y=None, _is_data_distributed=False\n'
        ecax__osooi += f'):\n'
        if isinstance(X, DataFrameType):
            ecax__osooi += f'  X = X.to_numpy()\n'
        ecax__osooi += (
            f"  with numba.objmode(qrange_l='float64', qrange_r='float64'):\n")
        ecax__osooi += f'    (qrange_l, qrange_r) = m.quantile_range\n'
        ecax__osooi += f'  if not 0 <= qrange_l <= qrange_r <= 100:\n'
        ecax__osooi += f'    raise ValueError(\n'
        ecax__osooi += f"""      'Invalid quantile range provided. Ensure that 0 <= quantile_range[0] <= quantile_range[1] <= 100.'
"""
        ecax__osooi += f'    )\n'
        ecax__osooi += (
            f'  qrange_l, qrange_r = qrange_l / 100.0, qrange_r / 100.0\n')
        ecax__osooi += f'  X = bodo.utils.conversion.coerce_to_array(X)\n'
        ecax__osooi += f'  num_features = X.shape[1]\n'
        ecax__osooi += f'  if m.with_scaling:\n'
        ecax__osooi += f'    scales = np.zeros(num_features)\n'
        ecax__osooi += f'  else:\n'
        ecax__osooi += f'    scales = None\n'
        ecax__osooi += f'  if m.with_centering:\n'
        ecax__osooi += f'    centers = np.zeros(num_features)\n'
        ecax__osooi += f'  else:\n'
        ecax__osooi += f'    centers = None\n'
        ecax__osooi += f'  if m.with_scaling or m.with_centering:\n'
        ecax__osooi += f'    numba.parfors.parfor.init_prange()\n'
        ecax__osooi += f"""    for feature_idx in numba.parfors.parfor.internal_prange(num_features):
"""
        ecax__osooi += f"""      column_data = bodo.utils.conversion.ensure_contig_if_np(X[:, feature_idx])
"""
        ecax__osooi += f'      if m.with_scaling:\n'
        ecax__osooi += (
            f'        q1 = bodo.libs.array_kernels.quantile_parallel(\n')
        ecax__osooi += f'          column_data, qrange_l, 0\n'
        ecax__osooi += f'        )\n'
        ecax__osooi += (
            f'        q2 = bodo.libs.array_kernels.quantile_parallel(\n')
        ecax__osooi += f'          column_data, qrange_r, 0\n'
        ecax__osooi += f'        )\n'
        ecax__osooi += f'        scales[feature_idx] = q2 - q1\n'
        ecax__osooi += f'      if m.with_centering:\n'
        ecax__osooi += (
            f'        centers[feature_idx] = bodo.libs.array_ops.array_op_median(\n'
            )
        ecax__osooi += f'          column_data, True, True\n'
        ecax__osooi += f'        )\n'
        ecax__osooi += f'  if m.with_scaling:\n'
        ecax__osooi += (
            f'    constant_mask = scales < 10 * np.finfo(scales.dtype).eps\n')
        ecax__osooi += f'    scales[constant_mask] = 1.0\n'
        ecax__osooi += f'    if m.unit_variance:\n'
        ecax__osooi += f"      with numba.objmode(adjust='float64'):\n"
        ecax__osooi += (
            f'        adjust = stats.norm.ppf(qrange_r) - stats.norm.ppf(qrange_l)\n'
            )
        ecax__osooi += f'      scales = scales / adjust\n'
        ecax__osooi += f'  with numba.objmode():\n'
        ecax__osooi += f'    m.center_ = centers\n'
        ecax__osooi += f'    m.scale_ = scales\n'
        ecax__osooi += f'  return m\n'
        wxn__kvxay = {}
        exec(ecax__osooi, globals(), wxn__kvxay)
        _preprocessing_robust_scaler_fit_impl = wxn__kvxay[
            'preprocessing_robust_scaler_fit_impl']
        return _preprocessing_robust_scaler_fit_impl
    else:

        def _preprocessing_robust_scaler_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_robust_scaler_type'):
                m = m.fit(X, y)
            return m
        return _preprocessing_robust_scaler_fit_impl


@overload_method(BodoPreprocessingRobustScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_robust_scaler_transform(m, X):
    check_sklearn_version()

    def _preprocessing_robust_scaler_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_robust_scaler_transform_impl


@overload_method(BodoPreprocessingRobustScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_robust_scaler_inverse_transform(m, X):
    check_sklearn_version()

    def _preprocessing_robust_scaler_inverse_transform_impl(m, X):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X)
        return inverse_transformed_X
    return _preprocessing_robust_scaler_inverse_transform_impl


BodoPreprocessingLabelEncoderType = install_py_obj_class(types_name=
    'preprocessing_label_encoder_type', python_type=sklearn.preprocessing.
    LabelEncoder, module=this_module, class_name=
    'BodoPreprocessingLabelEncoderType', model_name=
    'BodoPreprocessingLabelEncoderModel')


@overload(sklearn.preprocessing.LabelEncoder, no_unliteral=True)
def sklearn_preprocessing_label_encoder_overload():
    check_sklearn_version()

    def _sklearn_preprocessing_label_encoder_impl():
        with numba.objmode(m='preprocessing_label_encoder_type'):
            m = sklearn.preprocessing.LabelEncoder()
        return m
    return _sklearn_preprocessing_label_encoder_impl


@overload_method(BodoPreprocessingLabelEncoderType, 'fit', no_unliteral=True)
def overload_preprocessing_label_encoder_fit(m, y, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _sklearn_preprocessing_label_encoder_fit_impl(m, y,
            _is_data_distributed=False):
            y = bodo.utils.typing.decode_if_dict_array(y)
            y_classes = bodo.libs.array_kernels.unique(y, parallel=True)
            y_classes = bodo.allgatherv(y_classes, False)
            y_classes = bodo.libs.array_kernels.sort(y_classes, ascending=
                True, inplace=False)
            with numba.objmode:
                m.classes_ = y_classes
            return m
        return _sklearn_preprocessing_label_encoder_fit_impl
    else:

        def _sklearn_preprocessing_label_encoder_fit_impl(m, y,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_label_encoder_type'):
                m = m.fit(y)
            return m
        return _sklearn_preprocessing_label_encoder_fit_impl


@overload_method(BodoPreprocessingLabelEncoderType, 'transform',
    no_unliteral=True)
def overload_preprocessing_label_encoder_transform(m, y,
    _is_data_distributed=False):

    def _preprocessing_label_encoder_transform_impl(m, y,
        _is_data_distributed=False):
        with numba.objmode(transformed_y='int64[:]'):
            transformed_y = m.transform(y)
        return transformed_y
    return _preprocessing_label_encoder_transform_impl


@numba.njit
def le_fit_transform(m, y):
    m = m.fit(y, _is_data_distributed=True)
    transformed_y = m.transform(y, _is_data_distributed=True)
    return transformed_y


@overload_method(BodoPreprocessingLabelEncoderType, 'fit_transform',
    no_unliteral=True)
def overload_preprocessing_label_encoder_fit_transform(m, y,
    _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _preprocessing_label_encoder_fit_transform_impl(m, y,
            _is_data_distributed=False):
            transformed_y = le_fit_transform(m, y)
            return transformed_y
        return _preprocessing_label_encoder_fit_transform_impl
    else:

        def _preprocessing_label_encoder_fit_transform_impl(m, y,
            _is_data_distributed=False):
            with numba.objmode(transformed_y='int64[:]'):
                transformed_y = m.fit_transform(y)
            return transformed_y
        return _preprocessing_label_encoder_fit_transform_impl


BodoFExtractHashingVectorizerType = install_py_obj_class(types_name=
    'f_extract_hashing_vectorizer_type', python_type=sklearn.
    feature_extraction.text.HashingVectorizer, module=this_module,
    class_name='BodoFExtractHashingVectorizerType', model_name=
    'BodoFExtractHashingVectorizerModel')


@overload(sklearn.feature_extraction.text.HashingVectorizer, no_unliteral=True)
def sklearn_hashing_vectorizer_overload(input='content', encoding='utf-8',
    decode_error='strict', strip_accents=None, lowercase=True, preprocessor
    =None, tokenizer=None, stop_words=None, token_pattern=
    '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', n_features=2 **
    20, binary=False, norm='l2', alternate_sign=True, dtype=np.float64):
    check_sklearn_version()

    def _sklearn_hashing_vectorizer_impl(input='content', encoding='utf-8',
        decode_error='strict', strip_accents=None, lowercase=True,
        preprocessor=None, tokenizer=None, stop_words=None, token_pattern=
        '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word',
        n_features=2 ** 20, binary=False, norm='l2', alternate_sign=True,
        dtype=np.float64):
        with numba.objmode(m='f_extract_hashing_vectorizer_type'):
            m = sklearn.feature_extraction.text.HashingVectorizer(input=
                input, encoding=encoding, decode_error=decode_error,
                strip_accents=strip_accents, lowercase=lowercase,
                preprocessor=preprocessor, tokenizer=tokenizer, stop_words=
                stop_words, token_pattern=token_pattern, ngram_range=
                ngram_range, analyzer=analyzer, n_features=n_features,
                binary=binary, norm=norm, alternate_sign=alternate_sign,
                dtype=dtype)
        return m
    return _sklearn_hashing_vectorizer_impl


@overload_method(BodoFExtractHashingVectorizerType, 'fit_transform',
    no_unliteral=True)
def overload_hashing_vectorizer_fit_transform(m, X, y=None,
    _is_data_distributed=False):
    types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types.int64)

    def _hashing_vectorizer_fit_transform_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(transformed_X='csr_matrix_float64_int64'):
            transformed_X = m.fit_transform(X, y)
            transformed_X.indices = transformed_X.indices.astype(np.int64)
            transformed_X.indptr = transformed_X.indptr.astype(np.int64)
        return transformed_X
    return _hashing_vectorizer_fit_transform_impl


BodoRandomForestRegressorType = install_py_obj_class(types_name=
    'random_forest_regressor_type', python_type=sklearn.ensemble.
    RandomForestRegressor, module=this_module, class_name=
    'BodoRandomForestRegressorType', model_name=
    'BodoRandomForestRegressorModel')


@overload(sklearn.ensemble.RandomForestRegressor, no_unliteral=True)
def overload_sklearn_rf_regressor(n_estimators=100, criterion=
    'squared_error', max_depth=None, min_samples_split=2, min_samples_leaf=
    1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=
    None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False,
    n_jobs=None, random_state=None, verbose=0, warm_start=False, ccp_alpha=
    0.0, max_samples=None):
    check_sklearn_version()

    def _sklearn_ensemble_RandomForestRegressor_impl(n_estimators=100,
        criterion='squared_error', max_depth=None, min_samples_split=2,
        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=
        'auto', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=
        True, oob_score=False, n_jobs=None, random_state=None, verbose=0,
        warm_start=False, ccp_alpha=0.0, max_samples=None):
        with numba.objmode(m='random_forest_regressor_type'):
            if random_state is not None and get_num_nodes() > 1:
                print(
                    'With multinode, fixed random_state seed values are ignored.\n'
                    )
                random_state = None
            m = sklearn.ensemble.RandomForestRegressor(n_estimators=
                n_estimators, criterion=criterion, max_depth=max_depth,
                min_samples_split=min_samples_split, min_samples_leaf=
                min_samples_leaf, min_weight_fraction_leaf=
                min_weight_fraction_leaf, max_features=max_features,
                max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=
                min_impurity_decrease, bootstrap=bootstrap, oob_score=
                oob_score, n_jobs=1, random_state=random_state, verbose=
                verbose, warm_start=warm_start, ccp_alpha=ccp_alpha,
                max_samples=max_samples)
        return m
    return _sklearn_ensemble_RandomForestRegressor_impl


@overload_method(BodoRandomForestRegressorType, 'predict', no_unliteral=True)
def overload_rf_regressor_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoRandomForestRegressorType, 'score', no_unliteral=True)
def overload_rf_regressor_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_method(BodoRandomForestRegressorType, 'fit', no_unliteral=True)
@overload_method(BodoRandomForestClassifierType, 'fit', no_unliteral=True)
def overload_rf_classifier_model_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    zwz__rrpks = 'RandomForestClassifier'
    if isinstance(m, BodoRandomForestRegressorType):
        zwz__rrpks = 'RandomForestRegressor'
    if not is_overload_none(sample_weight):
        raise BodoError(
            f"sklearn.ensemble.{zwz__rrpks}.fit() : 'sample_weight' is not supported for distributed data."
            )

    def _model_fit_impl(m, X, y, sample_weight=None, _is_data_distributed=False
        ):
        with numba.objmode(first_rank_node='int32[:]'):
            first_rank_node = get_nodes_first_ranks()
        if _is_data_distributed:
            pkuwh__tskh = len(first_rank_node)
            X = bodo.gatherv(X)
            y = bodo.gatherv(y)
            if pkuwh__tskh > 1:
                X = bodo.libs.distributed_api.bcast_comm(X, comm_ranks=
                    first_rank_node, nranks=pkuwh__tskh)
                y = bodo.libs.distributed_api.bcast_comm(y, comm_ranks=
                    first_rank_node, nranks=pkuwh__tskh)
        with numba.objmode:
            random_forest_model_fit(m, X, y)
        bodo.barrier()
        return m
    return _model_fit_impl


BodoFExtractCountVectorizerType = install_py_obj_class(types_name=
    'f_extract_count_vectorizer_type', python_type=sklearn.
    feature_extraction.text.CountVectorizer, module=this_module, class_name
    ='BodoFExtractCountVectorizerType', model_name=
    'BodoFExtractCountVectorizerModel')


@overload(sklearn.feature_extraction.text.CountVectorizer, no_unliteral=True)
def sklearn_count_vectorizer_overload(input='content', encoding='utf-8',
    decode_error='strict', strip_accents=None, lowercase=True, preprocessor
    =None, tokenizer=None, stop_words=None, token_pattern=
    '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', max_df=1.0,
    min_df=1, max_features=None, vocabulary=None, binary=False, dtype=np.int64
    ):
    check_sklearn_version()
    if not is_overload_constant_number(min_df) or get_overload_const(min_df
        ) != 1:
        raise BodoError(
            """sklearn.feature_extraction.text.CountVectorizer(): 'min_df' is not supported for distributed data.
"""
            )
    if not is_overload_constant_number(max_df) or get_overload_const(min_df
        ) != 1:
        raise BodoError(
            """sklearn.feature_extraction.text.CountVectorizer(): 'max_df' is not supported for distributed data.
"""
            )

    def _sklearn_count_vectorizer_impl(input='content', encoding='utf-8',
        decode_error='strict', strip_accents=None, lowercase=True,
        preprocessor=None, tokenizer=None, stop_words=None, token_pattern=
        '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', max_df=
        1.0, min_df=1, max_features=None, vocabulary=None, binary=False,
        dtype=np.int64):
        with numba.objmode(m='f_extract_count_vectorizer_type'):
            m = sklearn.feature_extraction.text.CountVectorizer(input=input,
                encoding=encoding, decode_error=decode_error, strip_accents
                =strip_accents, lowercase=lowercase, preprocessor=
                preprocessor, tokenizer=tokenizer, stop_words=stop_words,
                token_pattern=token_pattern, ngram_range=ngram_range,
                analyzer=analyzer, max_df=max_df, min_df=min_df,
                max_features=max_features, vocabulary=vocabulary, binary=
                binary, dtype=dtype)
        return m
    return _sklearn_count_vectorizer_impl


@overload_attribute(BodoFExtractCountVectorizerType, 'vocabulary_')
def get_cv_vocabulary_(m):
    types.dict_string_int = types.DictType(types.unicode_type, types.int64)

    def impl(m):
        with numba.objmode(result='dict_string_int'):
            result = m.vocabulary_
        return result
    return impl


def _cv_fit_transform_helper(m, X):
    aoyiu__yfw = False
    local_vocabulary = m.vocabulary
    if m.vocabulary is None:
        m.fit(X)
        local_vocabulary = m.vocabulary_
        aoyiu__yfw = True
    return aoyiu__yfw, local_vocabulary


@overload_method(BodoFExtractCountVectorizerType, 'fit_transform',
    no_unliteral=True)
def overload_count_vectorizer_fit_transform(m, X, y=None,
    _is_data_distributed=False):
    check_sklearn_version()
    types.csr_matrix_int64_int64 = CSRMatrixType(types.int64, types.int64)
    if is_overload_true(_is_data_distributed):
        types.dict_str_int = types.DictType(types.unicode_type, types.int64)

        def _count_vectorizer_fit_transform_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(local_vocabulary='dict_str_int', changeVoc=
                'bool_'):
                changeVoc, local_vocabulary = _cv_fit_transform_helper(m, X)
            if changeVoc:
                local_vocabulary = bodo.utils.conversion.coerce_to_array(list
                    (local_vocabulary.keys()))
                adzvu__pdlfa = bodo.libs.array_kernels.unique(local_vocabulary,
                    parallel=True)
                adzvu__pdlfa = bodo.allgatherv(adzvu__pdlfa, False)
                adzvu__pdlfa = bodo.libs.array_kernels.sort(adzvu__pdlfa,
                    ascending=True, inplace=True)
                ndy__enj = {}
                for hlc__kqrii in range(len(adzvu__pdlfa)):
                    ndy__enj[adzvu__pdlfa[hlc__kqrii]] = hlc__kqrii
            else:
                ndy__enj = local_vocabulary
            with numba.objmode(transformed_X='csr_matrix_int64_int64'):
                if changeVoc:
                    m.vocabulary = ndy__enj
                transformed_X = m.fit_transform(X, y)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
        return _count_vectorizer_fit_transform_impl
    else:

        def _count_vectorizer_fit_transform_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(transformed_X='csr_matrix_int64_int64'):
                transformed_X = m.fit_transform(X, y)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
        return _count_vectorizer_fit_transform_impl


@overload_method(BodoFExtractCountVectorizerType, 'get_feature_names_out',
    no_unliteral=True)
def overload_count_vectorizer_get_feature_names_out(m):
    check_sklearn_version()

    def impl(m):
        with numba.objmode(result=bodo.string_array_type):
            result = m.get_feature_names_out()
        return result
    return impl
