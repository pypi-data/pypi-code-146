"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils import tracing
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero, is_str_arr_type


def array_op_any(arr, skipna=True):
    pass


@overload(array_op_any)
def overload_array_op_any(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        ychvp__ryfmd = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        ychvp__ryfmd = False
    elif A == bodo.string_array_type:
        ychvp__ryfmd = ''
    elif A == bodo.binary_array_type:
        ychvp__ryfmd = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        twcg__rfpyr = 0
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, utxs__pvhuo):
                if A[utxs__pvhuo] != ychvp__ryfmd:
                    twcg__rfpyr += 1
        return twcg__rfpyr != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        ychvp__ryfmd = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        ychvp__ryfmd = False
    elif A == bodo.string_array_type:
        ychvp__ryfmd = ''
    elif A == bodo.binary_array_type:
        ychvp__ryfmd = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        twcg__rfpyr = 0
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, utxs__pvhuo):
                if A[utxs__pvhuo] == ychvp__ryfmd:
                    twcg__rfpyr += 1
        return twcg__rfpyr == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    dud__wni = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(dud__wni.ctypes, arr,
        parallel, skipna)
    return dud__wni[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        lakli__btyey = len(arr)
        pdn__oxa = np.empty(lakli__btyey, np.bool_)
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(lakli__btyey):
            pdn__oxa[utxs__pvhuo] = bodo.libs.array_kernels.isna(arr,
                utxs__pvhuo)
        return pdn__oxa
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        twcg__rfpyr = 0
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
            numu__qysst = 0
            if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                numu__qysst = 1
            twcg__rfpyr += numu__qysst
        dud__wni = twcg__rfpyr
        return dud__wni
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    xcbve__gbahr = array_op_count(arr)
    tjxbv__zwbyy = array_op_min(arr)
    jnay__rhk = array_op_max(arr)
    zai__qck = array_op_mean(arr)
    kyru__gfuh = array_op_std(arr)
    ffkeq__hqbqn = array_op_quantile(arr, 0.25)
    uheea__pnui = array_op_quantile(arr, 0.5)
    vlv__gimw = array_op_quantile(arr, 0.75)
    return (xcbve__gbahr, zai__qck, kyru__gfuh, tjxbv__zwbyy, ffkeq__hqbqn,
        uheea__pnui, vlv__gimw, jnay__rhk)


def array_op_describe_dt_impl(arr):
    xcbve__gbahr = array_op_count(arr)
    tjxbv__zwbyy = array_op_min(arr)
    jnay__rhk = array_op_max(arr)
    zai__qck = array_op_mean(arr)
    ffkeq__hqbqn = array_op_quantile(arr, 0.25)
    uheea__pnui = array_op_quantile(arr, 0.5)
    vlv__gimw = array_op_quantile(arr, 0.75)
    return (xcbve__gbahr, zai__qck, tjxbv__zwbyy, ffkeq__hqbqn, uheea__pnui,
        vlv__gimw, jnay__rhk)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


@generated_jit(nopython=True)
def array_op_nbytes(arr):
    return array_op_nbytes_impl


def array_op_nbytes_impl(arr):
    return arr.nbytes


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = numba.cpython.builtins.get_type_max_value(np.int64)
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
                zppg__oll = uhob__diwsu
                numu__qysst = 0
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                    zppg__oll = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[utxs__pvhuo]))
                    numu__qysst = 1
                uhob__diwsu = min(uhob__diwsu, zppg__oll)
                twcg__rfpyr += numu__qysst
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(uhob__diwsu,
                twcg__rfpyr)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = numba.cpython.builtins.get_type_max_value(np.int64)
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
                zppg__oll = uhob__diwsu
                numu__qysst = 0
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                    zppg__oll = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[utxs__pvhuo])
                    numu__qysst = 1
                uhob__diwsu = min(uhob__diwsu, zppg__oll)
                twcg__rfpyr += numu__qysst
            return bodo.hiframes.pd_index_ext._dti_val_finalize(uhob__diwsu,
                twcg__rfpyr)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            abpl__xdkvw = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            uhob__diwsu = numba.cpython.builtins.get_type_max_value(np.int64)
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(
                abpl__xdkvw)):
                lmiw__qubqs = abpl__xdkvw[utxs__pvhuo]
                if lmiw__qubqs == -1:
                    continue
                uhob__diwsu = min(uhob__diwsu, lmiw__qubqs)
                twcg__rfpyr += 1
            dud__wni = bodo.hiframes.series_kernels._box_cat_val(uhob__diwsu,
                arr.dtype, twcg__rfpyr)
            return dud__wni
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = bodo.hiframes.series_kernels._get_date_max_value()
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
                zppg__oll = uhob__diwsu
                numu__qysst = 0
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                    zppg__oll = arr[utxs__pvhuo]
                    numu__qysst = 1
                uhob__diwsu = min(uhob__diwsu, zppg__oll)
                twcg__rfpyr += numu__qysst
            dud__wni = bodo.hiframes.series_kernels._sum_handle_nan(uhob__diwsu
                , twcg__rfpyr)
            return dud__wni
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        uhob__diwsu = bodo.hiframes.series_kernels._get_type_max_value(arr.
            dtype)
        twcg__rfpyr = 0
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
            zppg__oll = uhob__diwsu
            numu__qysst = 0
            if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                zppg__oll = arr[utxs__pvhuo]
                numu__qysst = 1
            uhob__diwsu = min(uhob__diwsu, zppg__oll)
            twcg__rfpyr += numu__qysst
        dud__wni = bodo.hiframes.series_kernels._sum_handle_nan(uhob__diwsu,
            twcg__rfpyr)
        return dud__wni
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = numba.cpython.builtins.get_type_min_value(np.int64)
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
                zppg__oll = uhob__diwsu
                numu__qysst = 0
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                    zppg__oll = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[utxs__pvhuo]))
                    numu__qysst = 1
                uhob__diwsu = max(uhob__diwsu, zppg__oll)
                twcg__rfpyr += numu__qysst
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(uhob__diwsu,
                twcg__rfpyr)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = numba.cpython.builtins.get_type_min_value(np.int64)
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
                zppg__oll = uhob__diwsu
                numu__qysst = 0
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                    zppg__oll = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[utxs__pvhuo])
                    numu__qysst = 1
                uhob__diwsu = max(uhob__diwsu, zppg__oll)
                twcg__rfpyr += numu__qysst
            return bodo.hiframes.pd_index_ext._dti_val_finalize(uhob__diwsu,
                twcg__rfpyr)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            abpl__xdkvw = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            uhob__diwsu = -1
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(
                abpl__xdkvw)):
                uhob__diwsu = max(uhob__diwsu, abpl__xdkvw[utxs__pvhuo])
            dud__wni = bodo.hiframes.series_kernels._box_cat_val(uhob__diwsu,
                arr.dtype, 1)
            return dud__wni
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = bodo.hiframes.series_kernels._get_date_min_value()
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
                zppg__oll = uhob__diwsu
                numu__qysst = 0
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                    zppg__oll = arr[utxs__pvhuo]
                    numu__qysst = 1
                uhob__diwsu = max(uhob__diwsu, zppg__oll)
                twcg__rfpyr += numu__qysst
            dud__wni = bodo.hiframes.series_kernels._sum_handle_nan(uhob__diwsu
                , twcg__rfpyr)
            return dud__wni
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        uhob__diwsu = bodo.hiframes.series_kernels._get_type_min_value(arr.
            dtype)
        twcg__rfpyr = 0
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
            zppg__oll = uhob__diwsu
            numu__qysst = 0
            if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                zppg__oll = arr[utxs__pvhuo]
                numu__qysst = 1
            uhob__diwsu = max(uhob__diwsu, zppg__oll)
            twcg__rfpyr += numu__qysst
        dud__wni = bodo.hiframes.series_kernels._sum_handle_nan(uhob__diwsu,
            twcg__rfpyr)
        return dud__wni
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    npsot__cpaj = types.float64
    khxh__tyg = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        npsot__cpaj = types.float32
        khxh__tyg = types.float32
    bfbdm__bzgb = npsot__cpaj(0)
    dwr__qye = khxh__tyg(0)
    ypglt__lxq = khxh__tyg(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        uhob__diwsu = bfbdm__bzgb
        twcg__rfpyr = dwr__qye
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
            zppg__oll = bfbdm__bzgb
            numu__qysst = dwr__qye
            if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                zppg__oll = arr[utxs__pvhuo]
                numu__qysst = ypglt__lxq
            uhob__diwsu += zppg__oll
            twcg__rfpyr += numu__qysst
        dud__wni = bodo.hiframes.series_kernels._mean_handle_nan(uhob__diwsu,
            twcg__rfpyr)
        return dud__wni
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        xzj__qouhv = 0.0
        xpw__ovi = 0.0
        twcg__rfpyr = 0
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
            zppg__oll = 0.0
            numu__qysst = 0
            if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo
                ) or not skipna:
                zppg__oll = arr[utxs__pvhuo]
                numu__qysst = 1
            xzj__qouhv += zppg__oll
            xpw__ovi += zppg__oll * zppg__oll
            twcg__rfpyr += numu__qysst
        dud__wni = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            xzj__qouhv, xpw__ovi, twcg__rfpyr, ddof)
        return dud__wni
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                pdn__oxa = np.empty(len(q), np.int64)
                for utxs__pvhuo in range(len(q)):
                    xow__kdo = np.float64(q[utxs__pvhuo])
                    pdn__oxa[utxs__pvhuo] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), xow__kdo)
                return pdn__oxa.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            pdn__oxa = np.empty(len(q), np.float64)
            for utxs__pvhuo in range(len(q)):
                xow__kdo = np.float64(q[utxs__pvhuo])
                pdn__oxa[utxs__pvhuo] = bodo.libs.array_kernels.quantile(arr,
                    xow__kdo)
            return pdn__oxa
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        aes__bplsx = types.intp
    elif arr.dtype == types.bool_:
        aes__bplsx = np.int64
    else:
        aes__bplsx = arr.dtype
    jatds__tza = aes__bplsx(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = jatds__tza
            lakli__btyey = len(arr)
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(
                lakli__btyey):
                zppg__oll = jatds__tza
                numu__qysst = 0
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo
                    ) or not skipna:
                    zppg__oll = arr[utxs__pvhuo]
                    numu__qysst = 1
                uhob__diwsu += zppg__oll
                twcg__rfpyr += numu__qysst
            dud__wni = bodo.hiframes.series_kernels._var_handle_mincount(
                uhob__diwsu, twcg__rfpyr, min_count)
            return dud__wni
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = jatds__tza
            lakli__btyey = len(arr)
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(
                lakli__btyey):
                zppg__oll = jatds__tza
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                    zppg__oll = arr[utxs__pvhuo]
                uhob__diwsu += zppg__oll
            return uhob__diwsu
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    vhvr__bnson = arr.dtype(1)
    if arr.dtype == types.bool_:
        vhvr__bnson = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = vhvr__bnson
            twcg__rfpyr = 0
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
                zppg__oll = vhvr__bnson
                numu__qysst = 0
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo
                    ) or not skipna:
                    zppg__oll = arr[utxs__pvhuo]
                    numu__qysst = 1
                twcg__rfpyr += numu__qysst
                uhob__diwsu *= zppg__oll
            dud__wni = bodo.hiframes.series_kernels._var_handle_mincount(
                uhob__diwsu, twcg__rfpyr, min_count)
            return dud__wni
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            uhob__diwsu = vhvr__bnson
            for utxs__pvhuo in numba.parfors.parfor.internal_prange(len(arr)):
                zppg__oll = vhvr__bnson
                if not bodo.libs.array_kernels.isna(arr, utxs__pvhuo):
                    zppg__oll = arr[utxs__pvhuo]
                uhob__diwsu *= zppg__oll
            return uhob__diwsu
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        utxs__pvhuo = bodo.libs.array_kernels._nan_argmax(arr)
        return index[utxs__pvhuo]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        utxs__pvhuo = bodo.libs.array_kernels._nan_argmin(arr)
        return index[utxs__pvhuo]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            tle__vrqbc = {}
            for svv__igkos in values:
                tle__vrqbc[bodo.utils.conversion.box_if_dt64(svv__igkos)] = 0
            return tle__vrqbc
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        lakli__btyey = len(arr)
        pdn__oxa = np.empty(lakli__btyey, np.bool_)
        for utxs__pvhuo in numba.parfors.parfor.internal_prange(lakli__btyey):
            pdn__oxa[utxs__pvhuo] = bodo.utils.conversion.box_if_dt64(arr[
                utxs__pvhuo]) in values
        return pdn__oxa
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    ickdh__txus = len(in_arr_tup) != 1
    pxuz__mmz = list(in_arr_tup.types)
    vypa__utx = 'def impl(in_arr_tup):\n'
    vypa__utx += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    vypa__utx += '  n = len(in_arr_tup[0])\n'
    if ickdh__txus:
        rqsf__vub = ', '.join([f'in_arr_tup[{utxs__pvhuo}][unused]' for
            utxs__pvhuo in range(len(in_arr_tup))])
        wexu__agfr = ', '.join(['False' for olcj__qpaao in range(len(
            in_arr_tup))])
        vypa__utx += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({rqsf__vub},), ({wexu__agfr},)): 0 for unused in range(0)}}
"""
        vypa__utx += '  map_vector = np.empty(n, np.int64)\n'
        for utxs__pvhuo, xfy__pwt in enumerate(pxuz__mmz):
            vypa__utx += f'  in_lst_{utxs__pvhuo} = []\n'
            if is_str_arr_type(xfy__pwt):
                vypa__utx += f'  total_len_{utxs__pvhuo} = 0\n'
            vypa__utx += f'  null_in_lst_{utxs__pvhuo} = []\n'
        vypa__utx += '  for i in range(n):\n'
        pycuv__qxpl = ', '.join([f'in_arr_tup[{utxs__pvhuo}][i]' for
            utxs__pvhuo in range(len(pxuz__mmz))])
        wdis__bjagp = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{utxs__pvhuo}], i)' for
            utxs__pvhuo in range(len(pxuz__mmz))])
        vypa__utx += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({pycuv__qxpl},), ({wdis__bjagp},))
"""
        vypa__utx += '    if data_val not in arr_map:\n'
        vypa__utx += '      set_val = len(arr_map)\n'
        vypa__utx += '      values_tup = data_val._data\n'
        vypa__utx += '      nulls_tup = data_val._null_values\n'
        for utxs__pvhuo, xfy__pwt in enumerate(pxuz__mmz):
            vypa__utx += (
                f'      in_lst_{utxs__pvhuo}.append(values_tup[{utxs__pvhuo}])\n'
                )
            vypa__utx += (
                f'      null_in_lst_{utxs__pvhuo}.append(nulls_tup[{utxs__pvhuo}])\n'
                )
            if is_str_arr_type(xfy__pwt):
                vypa__utx += f"""      total_len_{utxs__pvhuo}  += nulls_tup[{utxs__pvhuo}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{utxs__pvhuo}], i)
"""
        vypa__utx += '      arr_map[data_val] = len(arr_map)\n'
        vypa__utx += '    else:\n'
        vypa__utx += '      set_val = arr_map[data_val]\n'
        vypa__utx += '    map_vector[i] = set_val\n'
        vypa__utx += '  n_rows = len(arr_map)\n'
        for utxs__pvhuo, xfy__pwt in enumerate(pxuz__mmz):
            if is_str_arr_type(xfy__pwt):
                vypa__utx += f"""  out_arr_{utxs__pvhuo} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{utxs__pvhuo})
"""
            else:
                vypa__utx += f"""  out_arr_{utxs__pvhuo} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{utxs__pvhuo}], (-1,))
"""
        vypa__utx += '  for j in range(len(arr_map)):\n'
        for utxs__pvhuo in range(len(pxuz__mmz)):
            vypa__utx += f'    if null_in_lst_{utxs__pvhuo}[j]:\n'
            vypa__utx += (
                f'      bodo.libs.array_kernels.setna(out_arr_{utxs__pvhuo}, j)\n'
                )
            vypa__utx += '    else:\n'
            vypa__utx += (
                f'      out_arr_{utxs__pvhuo}[j] = in_lst_{utxs__pvhuo}[j]\n')
        vfupu__mmstk = ', '.join([f'out_arr_{utxs__pvhuo}' for utxs__pvhuo in
            range(len(pxuz__mmz))])
        vypa__utx += "  ev.add_attribute('n_map_entries', n_rows)\n"
        vypa__utx += '  ev.finalize()\n'
        vypa__utx += f'  return ({vfupu__mmstk},), map_vector\n'
    else:
        vypa__utx += '  in_arr = in_arr_tup[0]\n'
        vypa__utx += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        vypa__utx += '  map_vector = np.empty(n, np.int64)\n'
        vypa__utx += '  is_na = 0\n'
        vypa__utx += '  in_lst = []\n'
        vypa__utx += '  na_idxs = []\n'
        if is_str_arr_type(pxuz__mmz[0]):
            vypa__utx += '  total_len = 0\n'
        vypa__utx += '  for i in range(n):\n'
        vypa__utx += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        vypa__utx += '      is_na = 1\n'
        vypa__utx += '      # Always put NA in the last location.\n'
        vypa__utx += '      # We use -1 as a placeholder\n'
        vypa__utx += '      set_val = -1\n'
        vypa__utx += '      na_idxs.append(i)\n'
        vypa__utx += '    else:\n'
        vypa__utx += '      data_val = in_arr[i]\n'
        vypa__utx += '      if data_val not in arr_map:\n'
        vypa__utx += '        set_val = len(arr_map)\n'
        vypa__utx += '        in_lst.append(data_val)\n'
        if is_str_arr_type(pxuz__mmz[0]):
            vypa__utx += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        vypa__utx += '        arr_map[data_val] = len(arr_map)\n'
        vypa__utx += '      else:\n'
        vypa__utx += '        set_val = arr_map[data_val]\n'
        vypa__utx += '    map_vector[i] = set_val\n'
        vypa__utx += '  map_vector[na_idxs] = len(arr_map)\n'
        vypa__utx += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(pxuz__mmz[0]):
            vypa__utx += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            vypa__utx += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        vypa__utx += '  for j in range(len(arr_map)):\n'
        vypa__utx += '    out_arr[j] = in_lst[j]\n'
        vypa__utx += '  if is_na:\n'
        vypa__utx += '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n'
        vypa__utx += "  ev.add_attribute('n_map_entries', n_rows)\n"
        vypa__utx += '  ev.finalize()\n'
        vypa__utx += f'  return (out_arr,), map_vector\n'
    moj__axty = {}
    exec(vypa__utx, {'bodo': bodo, 'np': np, 'tracing': tracing}, moj__axty)
    impl = moj__axty['impl']
    return impl
