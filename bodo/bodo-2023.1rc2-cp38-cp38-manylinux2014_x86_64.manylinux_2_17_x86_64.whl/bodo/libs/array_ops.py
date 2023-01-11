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
        ynut__uzmfg = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        ynut__uzmfg = False
    elif A == bodo.string_array_type:
        ynut__uzmfg = ''
    elif A == bodo.binary_array_type:
        ynut__uzmfg = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        hze__egmx = 0
        for ashkm__icib in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, ashkm__icib):
                if A[ashkm__icib] != ynut__uzmfg:
                    hze__egmx += 1
        return hze__egmx != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        ynut__uzmfg = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        ynut__uzmfg = False
    elif A == bodo.string_array_type:
        ynut__uzmfg = ''
    elif A == bodo.binary_array_type:
        ynut__uzmfg = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        hze__egmx = 0
        for ashkm__icib in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, ashkm__icib):
                if A[ashkm__icib] == ynut__uzmfg:
                    hze__egmx += 1
        return hze__egmx == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    cynxv__chpat = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(cynxv__chpat.ctypes,
        arr, parallel, skipna)
    return cynxv__chpat[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        yuju__bwli = len(arr)
        dgdb__wlsq = np.empty(yuju__bwli, np.bool_)
        for ashkm__icib in numba.parfors.parfor.internal_prange(yuju__bwli):
            dgdb__wlsq[ashkm__icib] = bodo.libs.array_kernels.isna(arr,
                ashkm__icib)
        return dgdb__wlsq
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        hze__egmx = 0
        for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
            zitka__xthm = 0
            if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                zitka__xthm = 1
            hze__egmx += zitka__xthm
        cynxv__chpat = hze__egmx
        return cynxv__chpat
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    rjkhx__nlpcw = array_op_count(arr)
    tio__cpgth = array_op_min(arr)
    hrl__xkz = array_op_max(arr)
    wna__lhvbr = array_op_mean(arr)
    pat__qqhu = array_op_std(arr)
    bqf__blysx = array_op_quantile(arr, 0.25)
    pvmo__kmr = array_op_quantile(arr, 0.5)
    bsrit__wdjw = array_op_quantile(arr, 0.75)
    return (rjkhx__nlpcw, wna__lhvbr, pat__qqhu, tio__cpgth, bqf__blysx,
        pvmo__kmr, bsrit__wdjw, hrl__xkz)


def array_op_describe_dt_impl(arr):
    rjkhx__nlpcw = array_op_count(arr)
    tio__cpgth = array_op_min(arr)
    hrl__xkz = array_op_max(arr)
    wna__lhvbr = array_op_mean(arr)
    bqf__blysx = array_op_quantile(arr, 0.25)
    pvmo__kmr = array_op_quantile(arr, 0.5)
    bsrit__wdjw = array_op_quantile(arr, 0.75)
    return (rjkhx__nlpcw, wna__lhvbr, tio__cpgth, bqf__blysx, pvmo__kmr,
        bsrit__wdjw, hrl__xkz)


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
            yczn__thb = numba.cpython.builtins.get_type_max_value(np.int64)
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
                cypoc__uooz = yczn__thb
                zitka__xthm = 0
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                    cypoc__uooz = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[ashkm__icib]))
                    zitka__xthm = 1
                yczn__thb = min(yczn__thb, cypoc__uooz)
                hze__egmx += zitka__xthm
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(yczn__thb,
                hze__egmx)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            yczn__thb = numba.cpython.builtins.get_type_max_value(np.int64)
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
                cypoc__uooz = yczn__thb
                zitka__xthm = 0
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                    cypoc__uooz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[ashkm__icib]))
                    zitka__xthm = 1
                yczn__thb = min(yczn__thb, cypoc__uooz)
                hze__egmx += zitka__xthm
            return bodo.hiframes.pd_index_ext._dti_val_finalize(yczn__thb,
                hze__egmx)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            gfbh__nlcxn = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            yczn__thb = numba.cpython.builtins.get_type_max_value(np.int64)
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(
                gfbh__nlcxn)):
                wpgz__gmtd = gfbh__nlcxn[ashkm__icib]
                if wpgz__gmtd == -1:
                    continue
                yczn__thb = min(yczn__thb, wpgz__gmtd)
                hze__egmx += 1
            cynxv__chpat = bodo.hiframes.series_kernels._box_cat_val(yczn__thb,
                arr.dtype, hze__egmx)
            return cynxv__chpat
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            yczn__thb = bodo.hiframes.series_kernels._get_date_max_value()
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
                cypoc__uooz = yczn__thb
                zitka__xthm = 0
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                    cypoc__uooz = arr[ashkm__icib]
                    zitka__xthm = 1
                yczn__thb = min(yczn__thb, cypoc__uooz)
                hze__egmx += zitka__xthm
            cynxv__chpat = bodo.hiframes.series_kernels._sum_handle_nan(
                yczn__thb, hze__egmx)
            return cynxv__chpat
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        yczn__thb = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype)
        hze__egmx = 0
        for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
            cypoc__uooz = yczn__thb
            zitka__xthm = 0
            if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                cypoc__uooz = arr[ashkm__icib]
                zitka__xthm = 1
            yczn__thb = min(yczn__thb, cypoc__uooz)
            hze__egmx += zitka__xthm
        cynxv__chpat = bodo.hiframes.series_kernels._sum_handle_nan(yczn__thb,
            hze__egmx)
        return cynxv__chpat
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            yczn__thb = numba.cpython.builtins.get_type_min_value(np.int64)
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
                cypoc__uooz = yczn__thb
                zitka__xthm = 0
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                    cypoc__uooz = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[ashkm__icib]))
                    zitka__xthm = 1
                yczn__thb = max(yczn__thb, cypoc__uooz)
                hze__egmx += zitka__xthm
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(yczn__thb,
                hze__egmx)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            yczn__thb = numba.cpython.builtins.get_type_min_value(np.int64)
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
                cypoc__uooz = yczn__thb
                zitka__xthm = 0
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                    cypoc__uooz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[ashkm__icib]))
                    zitka__xthm = 1
                yczn__thb = max(yczn__thb, cypoc__uooz)
                hze__egmx += zitka__xthm
            return bodo.hiframes.pd_index_ext._dti_val_finalize(yczn__thb,
                hze__egmx)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            gfbh__nlcxn = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            yczn__thb = -1
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(
                gfbh__nlcxn)):
                yczn__thb = max(yczn__thb, gfbh__nlcxn[ashkm__icib])
            cynxv__chpat = bodo.hiframes.series_kernels._box_cat_val(yczn__thb,
                arr.dtype, 1)
            return cynxv__chpat
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            yczn__thb = bodo.hiframes.series_kernels._get_date_min_value()
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
                cypoc__uooz = yczn__thb
                zitka__xthm = 0
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                    cypoc__uooz = arr[ashkm__icib]
                    zitka__xthm = 1
                yczn__thb = max(yczn__thb, cypoc__uooz)
                hze__egmx += zitka__xthm
            cynxv__chpat = bodo.hiframes.series_kernels._sum_handle_nan(
                yczn__thb, hze__egmx)
            return cynxv__chpat
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        yczn__thb = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype)
        hze__egmx = 0
        for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
            cypoc__uooz = yczn__thb
            zitka__xthm = 0
            if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                cypoc__uooz = arr[ashkm__icib]
                zitka__xthm = 1
            yczn__thb = max(yczn__thb, cypoc__uooz)
            hze__egmx += zitka__xthm
        cynxv__chpat = bodo.hiframes.series_kernels._sum_handle_nan(yczn__thb,
            hze__egmx)
        return cynxv__chpat
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
    jnqeb__tny = types.float64
    iln__xjvxk = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        jnqeb__tny = types.float32
        iln__xjvxk = types.float32
    enrn__uvxy = jnqeb__tny(0)
    wlbk__wqb = iln__xjvxk(0)
    soxfz__lmazu = iln__xjvxk(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        yczn__thb = enrn__uvxy
        hze__egmx = wlbk__wqb
        for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
            cypoc__uooz = enrn__uvxy
            zitka__xthm = wlbk__wqb
            if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                cypoc__uooz = arr[ashkm__icib]
                zitka__xthm = soxfz__lmazu
            yczn__thb += cypoc__uooz
            hze__egmx += zitka__xthm
        cynxv__chpat = bodo.hiframes.series_kernels._mean_handle_nan(yczn__thb,
            hze__egmx)
        return cynxv__chpat
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        zxg__fcv = 0.0
        lql__bhl = 0.0
        hze__egmx = 0
        for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
            cypoc__uooz = 0.0
            zitka__xthm = 0
            if not bodo.libs.array_kernels.isna(arr, ashkm__icib
                ) or not skipna:
                cypoc__uooz = arr[ashkm__icib]
                zitka__xthm = 1
            zxg__fcv += cypoc__uooz
            lql__bhl += cypoc__uooz * cypoc__uooz
            hze__egmx += zitka__xthm
        cynxv__chpat = (bodo.hiframes.series_kernels.
            _compute_var_nan_count_ddof(zxg__fcv, lql__bhl, hze__egmx, ddof))
        return cynxv__chpat
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
                dgdb__wlsq = np.empty(len(q), np.int64)
                for ashkm__icib in range(len(q)):
                    uomm__wuuk = np.float64(q[ashkm__icib])
                    dgdb__wlsq[ashkm__icib] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), uomm__wuuk)
                return dgdb__wlsq.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            dgdb__wlsq = np.empty(len(q), np.float64)
            for ashkm__icib in range(len(q)):
                uomm__wuuk = np.float64(q[ashkm__icib])
                dgdb__wlsq[ashkm__icib] = bodo.libs.array_kernels.quantile(arr,
                    uomm__wuuk)
            return dgdb__wlsq
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
        zkiv__tga = types.intp
    elif arr.dtype == types.bool_:
        zkiv__tga = np.int64
    else:
        zkiv__tga = arr.dtype
    suznn__puo = zkiv__tga(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            yczn__thb = suznn__puo
            yuju__bwli = len(arr)
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(yuju__bwli
                ):
                cypoc__uooz = suznn__puo
                zitka__xthm = 0
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib
                    ) or not skipna:
                    cypoc__uooz = arr[ashkm__icib]
                    zitka__xthm = 1
                yczn__thb += cypoc__uooz
                hze__egmx += zitka__xthm
            cynxv__chpat = bodo.hiframes.series_kernels._var_handle_mincount(
                yczn__thb, hze__egmx, min_count)
            return cynxv__chpat
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            yczn__thb = suznn__puo
            yuju__bwli = len(arr)
            for ashkm__icib in numba.parfors.parfor.internal_prange(yuju__bwli
                ):
                cypoc__uooz = suznn__puo
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                    cypoc__uooz = arr[ashkm__icib]
                yczn__thb += cypoc__uooz
            return yczn__thb
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    toj__yvsb = arr.dtype(1)
    if arr.dtype == types.bool_:
        toj__yvsb = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            yczn__thb = toj__yvsb
            hze__egmx = 0
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
                cypoc__uooz = toj__yvsb
                zitka__xthm = 0
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib
                    ) or not skipna:
                    cypoc__uooz = arr[ashkm__icib]
                    zitka__xthm = 1
                hze__egmx += zitka__xthm
                yczn__thb *= cypoc__uooz
            cynxv__chpat = bodo.hiframes.series_kernels._var_handle_mincount(
                yczn__thb, hze__egmx, min_count)
            return cynxv__chpat
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            yczn__thb = toj__yvsb
            for ashkm__icib in numba.parfors.parfor.internal_prange(len(arr)):
                cypoc__uooz = toj__yvsb
                if not bodo.libs.array_kernels.isna(arr, ashkm__icib):
                    cypoc__uooz = arr[ashkm__icib]
                yczn__thb *= cypoc__uooz
            return yczn__thb
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        ashkm__icib = bodo.libs.array_kernels._nan_argmax(arr)
        return index[ashkm__icib]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        ashkm__icib = bodo.libs.array_kernels._nan_argmin(arr)
        return index[ashkm__icib]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            jmqfm__ydr = {}
            for msz__izuw in values:
                jmqfm__ydr[bodo.utils.conversion.box_if_dt64(msz__izuw)] = 0
            return jmqfm__ydr
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
        yuju__bwli = len(arr)
        dgdb__wlsq = np.empty(yuju__bwli, np.bool_)
        for ashkm__icib in numba.parfors.parfor.internal_prange(yuju__bwli):
            dgdb__wlsq[ashkm__icib] = bodo.utils.conversion.box_if_dt64(arr
                [ashkm__icib]) in values
        return dgdb__wlsq
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    zgp__wyz = len(in_arr_tup) != 1
    fxh__aug = list(in_arr_tup.types)
    qignp__ozf = 'def impl(in_arr_tup):\n'
    qignp__ozf += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    qignp__ozf += '  n = len(in_arr_tup[0])\n'
    if zgp__wyz:
        djhdf__vcp = ', '.join([f'in_arr_tup[{ashkm__icib}][unused]' for
            ashkm__icib in range(len(in_arr_tup))])
        qbon__grh = ', '.join(['False' for qdr__pol in range(len(in_arr_tup))])
        qignp__ozf += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({djhdf__vcp},), ({qbon__grh},)): 0 for unused in range(0)}}
"""
        qignp__ozf += '  map_vector = np.empty(n, np.int64)\n'
        for ashkm__icib, uoz__jdfa in enumerate(fxh__aug):
            qignp__ozf += f'  in_lst_{ashkm__icib} = []\n'
            if is_str_arr_type(uoz__jdfa):
                qignp__ozf += f'  total_len_{ashkm__icib} = 0\n'
            qignp__ozf += f'  null_in_lst_{ashkm__icib} = []\n'
        qignp__ozf += '  for i in range(n):\n'
        hnt__gspf = ', '.join([f'in_arr_tup[{ashkm__icib}][i]' for
            ashkm__icib in range(len(fxh__aug))])
        kjpx__mds = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{ashkm__icib}], i)' for
            ashkm__icib in range(len(fxh__aug))])
        qignp__ozf += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({hnt__gspf},), ({kjpx__mds},))
"""
        qignp__ozf += '    if data_val not in arr_map:\n'
        qignp__ozf += '      set_val = len(arr_map)\n'
        qignp__ozf += '      values_tup = data_val._data\n'
        qignp__ozf += '      nulls_tup = data_val._null_values\n'
        for ashkm__icib, uoz__jdfa in enumerate(fxh__aug):
            qignp__ozf += (
                f'      in_lst_{ashkm__icib}.append(values_tup[{ashkm__icib}])\n'
                )
            qignp__ozf += (
                f'      null_in_lst_{ashkm__icib}.append(nulls_tup[{ashkm__icib}])\n'
                )
            if is_str_arr_type(uoz__jdfa):
                qignp__ozf += f"""      total_len_{ashkm__icib}  += nulls_tup[{ashkm__icib}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{ashkm__icib}], i)
"""
        qignp__ozf += '      arr_map[data_val] = len(arr_map)\n'
        qignp__ozf += '    else:\n'
        qignp__ozf += '      set_val = arr_map[data_val]\n'
        qignp__ozf += '    map_vector[i] = set_val\n'
        qignp__ozf += '  n_rows = len(arr_map)\n'
        for ashkm__icib, uoz__jdfa in enumerate(fxh__aug):
            if is_str_arr_type(uoz__jdfa):
                qignp__ozf += f"""  out_arr_{ashkm__icib} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{ashkm__icib})
"""
            else:
                qignp__ozf += f"""  out_arr_{ashkm__icib} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{ashkm__icib}], (-1,))
"""
        qignp__ozf += '  for j in range(len(arr_map)):\n'
        for ashkm__icib in range(len(fxh__aug)):
            qignp__ozf += f'    if null_in_lst_{ashkm__icib}[j]:\n'
            qignp__ozf += (
                f'      bodo.libs.array_kernels.setna(out_arr_{ashkm__icib}, j)\n'
                )
            qignp__ozf += '    else:\n'
            qignp__ozf += (
                f'      out_arr_{ashkm__icib}[j] = in_lst_{ashkm__icib}[j]\n')
        kviv__riju = ', '.join([f'out_arr_{ashkm__icib}' for ashkm__icib in
            range(len(fxh__aug))])
        qignp__ozf += "  ev.add_attribute('n_map_entries', n_rows)\n"
        qignp__ozf += '  ev.finalize()\n'
        qignp__ozf += f'  return ({kviv__riju},), map_vector\n'
    else:
        qignp__ozf += '  in_arr = in_arr_tup[0]\n'
        qignp__ozf += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        qignp__ozf += '  map_vector = np.empty(n, np.int64)\n'
        qignp__ozf += '  is_na = 0\n'
        qignp__ozf += '  in_lst = []\n'
        qignp__ozf += '  na_idxs = []\n'
        if is_str_arr_type(fxh__aug[0]):
            qignp__ozf += '  total_len = 0\n'
        qignp__ozf += '  for i in range(n):\n'
        qignp__ozf += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        qignp__ozf += '      is_na = 1\n'
        qignp__ozf += '      # Always put NA in the last location.\n'
        qignp__ozf += '      # We use -1 as a placeholder\n'
        qignp__ozf += '      set_val = -1\n'
        qignp__ozf += '      na_idxs.append(i)\n'
        qignp__ozf += '    else:\n'
        qignp__ozf += '      data_val = in_arr[i]\n'
        qignp__ozf += '      if data_val not in arr_map:\n'
        qignp__ozf += '        set_val = len(arr_map)\n'
        qignp__ozf += '        in_lst.append(data_val)\n'
        if is_str_arr_type(fxh__aug[0]):
            qignp__ozf += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        qignp__ozf += '        arr_map[data_val] = len(arr_map)\n'
        qignp__ozf += '      else:\n'
        qignp__ozf += '        set_val = arr_map[data_val]\n'
        qignp__ozf += '    map_vector[i] = set_val\n'
        qignp__ozf += '  map_vector[na_idxs] = len(arr_map)\n'
        qignp__ozf += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(fxh__aug[0]):
            qignp__ozf += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            qignp__ozf += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        qignp__ozf += '  for j in range(len(arr_map)):\n'
        qignp__ozf += '    out_arr[j] = in_lst[j]\n'
        qignp__ozf += '  if is_na:\n'
        qignp__ozf += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        qignp__ozf += "  ev.add_attribute('n_map_entries', n_rows)\n"
        qignp__ozf += '  ev.finalize()\n'
        qignp__ozf += f'  return (out_arr,), map_vector\n'
    bgrl__luetp = {}
    exec(qignp__ozf, {'bodo': bodo, 'np': np, 'tracing': tracing}, bgrl__luetp)
    impl = bgrl__luetp['impl']
    return impl
