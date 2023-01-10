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
        rhyhc__geiuv = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        rhyhc__geiuv = False
    elif A == bodo.string_array_type:
        rhyhc__geiuv = ''
    elif A == bodo.binary_array_type:
        rhyhc__geiuv = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        hxp__vjonh = 0
        for reu__dzbpx in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, reu__dzbpx):
                if A[reu__dzbpx] != rhyhc__geiuv:
                    hxp__vjonh += 1
        return hxp__vjonh != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        rhyhc__geiuv = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        rhyhc__geiuv = False
    elif A == bodo.string_array_type:
        rhyhc__geiuv = ''
    elif A == bodo.binary_array_type:
        rhyhc__geiuv = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        hxp__vjonh = 0
        for reu__dzbpx in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, reu__dzbpx):
                if A[reu__dzbpx] == rhyhc__geiuv:
                    hxp__vjonh += 1
        return hxp__vjonh == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    zsigh__nwy = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(zsigh__nwy.ctypes,
        arr, parallel, skipna)
    return zsigh__nwy[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        xmrjr__cia = len(arr)
        fztky__ybnq = np.empty(xmrjr__cia, np.bool_)
        for reu__dzbpx in numba.parfors.parfor.internal_prange(xmrjr__cia):
            fztky__ybnq[reu__dzbpx] = bodo.libs.array_kernels.isna(arr,
                reu__dzbpx)
        return fztky__ybnq
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        hxp__vjonh = 0
        for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
            wic__mmyzl = 0
            if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                wic__mmyzl = 1
            hxp__vjonh += wic__mmyzl
        zsigh__nwy = hxp__vjonh
        return zsigh__nwy
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    pymcy__oxa = array_op_count(arr)
    innu__qgby = array_op_min(arr)
    ikce__tqjt = array_op_max(arr)
    wtjau__artr = array_op_mean(arr)
    gfx__jik = array_op_std(arr)
    ggj__reepl = array_op_quantile(arr, 0.25)
    vzy__ium = array_op_quantile(arr, 0.5)
    pvyc__jfw = array_op_quantile(arr, 0.75)
    return (pymcy__oxa, wtjau__artr, gfx__jik, innu__qgby, ggj__reepl,
        vzy__ium, pvyc__jfw, ikce__tqjt)


def array_op_describe_dt_impl(arr):
    pymcy__oxa = array_op_count(arr)
    innu__qgby = array_op_min(arr)
    ikce__tqjt = array_op_max(arr)
    wtjau__artr = array_op_mean(arr)
    ggj__reepl = array_op_quantile(arr, 0.25)
    vzy__ium = array_op_quantile(arr, 0.5)
    pvyc__jfw = array_op_quantile(arr, 0.75)
    return (pymcy__oxa, wtjau__artr, innu__qgby, ggj__reepl, vzy__ium,
        pvyc__jfw, ikce__tqjt)


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
            kbfs__xnyu = numba.cpython.builtins.get_type_max_value(np.int64)
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
                qqkf__exigh = kbfs__xnyu
                wic__mmyzl = 0
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                    qqkf__exigh = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[reu__dzbpx]))
                    wic__mmyzl = 1
                kbfs__xnyu = min(kbfs__xnyu, qqkf__exigh)
                hxp__vjonh += wic__mmyzl
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(kbfs__xnyu,
                hxp__vjonh)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = numba.cpython.builtins.get_type_max_value(np.int64)
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
                qqkf__exigh = kbfs__xnyu
                wic__mmyzl = 0
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                    qqkf__exigh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[reu__dzbpx]))
                    wic__mmyzl = 1
                kbfs__xnyu = min(kbfs__xnyu, qqkf__exigh)
                hxp__vjonh += wic__mmyzl
            return bodo.hiframes.pd_index_ext._dti_val_finalize(kbfs__xnyu,
                hxp__vjonh)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            ddhs__joj = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = numba.cpython.builtins.get_type_max_value(np.int64)
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(
                ddhs__joj)):
                xks__bkh = ddhs__joj[reu__dzbpx]
                if xks__bkh == -1:
                    continue
                kbfs__xnyu = min(kbfs__xnyu, xks__bkh)
                hxp__vjonh += 1
            zsigh__nwy = bodo.hiframes.series_kernels._box_cat_val(kbfs__xnyu,
                arr.dtype, hxp__vjonh)
            return zsigh__nwy
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = bodo.hiframes.series_kernels._get_date_max_value()
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
                qqkf__exigh = kbfs__xnyu
                wic__mmyzl = 0
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                    qqkf__exigh = arr[reu__dzbpx]
                    wic__mmyzl = 1
                kbfs__xnyu = min(kbfs__xnyu, qqkf__exigh)
                hxp__vjonh += wic__mmyzl
            zsigh__nwy = bodo.hiframes.series_kernels._sum_handle_nan(
                kbfs__xnyu, hxp__vjonh)
            return zsigh__nwy
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kbfs__xnyu = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype
            )
        hxp__vjonh = 0
        for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
            qqkf__exigh = kbfs__xnyu
            wic__mmyzl = 0
            if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                qqkf__exigh = arr[reu__dzbpx]
                wic__mmyzl = 1
            kbfs__xnyu = min(kbfs__xnyu, qqkf__exigh)
            hxp__vjonh += wic__mmyzl
        zsigh__nwy = bodo.hiframes.series_kernels._sum_handle_nan(kbfs__xnyu,
            hxp__vjonh)
        return zsigh__nwy
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = numba.cpython.builtins.get_type_min_value(np.int64)
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
                qqkf__exigh = kbfs__xnyu
                wic__mmyzl = 0
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                    qqkf__exigh = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[reu__dzbpx]))
                    wic__mmyzl = 1
                kbfs__xnyu = max(kbfs__xnyu, qqkf__exigh)
                hxp__vjonh += wic__mmyzl
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(kbfs__xnyu,
                hxp__vjonh)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = numba.cpython.builtins.get_type_min_value(np.int64)
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
                qqkf__exigh = kbfs__xnyu
                wic__mmyzl = 0
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                    qqkf__exigh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[reu__dzbpx]))
                    wic__mmyzl = 1
                kbfs__xnyu = max(kbfs__xnyu, qqkf__exigh)
                hxp__vjonh += wic__mmyzl
            return bodo.hiframes.pd_index_ext._dti_val_finalize(kbfs__xnyu,
                hxp__vjonh)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            ddhs__joj = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = -1
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(
                ddhs__joj)):
                kbfs__xnyu = max(kbfs__xnyu, ddhs__joj[reu__dzbpx])
            zsigh__nwy = bodo.hiframes.series_kernels._box_cat_val(kbfs__xnyu,
                arr.dtype, 1)
            return zsigh__nwy
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = bodo.hiframes.series_kernels._get_date_min_value()
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
                qqkf__exigh = kbfs__xnyu
                wic__mmyzl = 0
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                    qqkf__exigh = arr[reu__dzbpx]
                    wic__mmyzl = 1
                kbfs__xnyu = max(kbfs__xnyu, qqkf__exigh)
                hxp__vjonh += wic__mmyzl
            zsigh__nwy = bodo.hiframes.series_kernels._sum_handle_nan(
                kbfs__xnyu, hxp__vjonh)
            return zsigh__nwy
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kbfs__xnyu = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype
            )
        hxp__vjonh = 0
        for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
            qqkf__exigh = kbfs__xnyu
            wic__mmyzl = 0
            if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                qqkf__exigh = arr[reu__dzbpx]
                wic__mmyzl = 1
            kbfs__xnyu = max(kbfs__xnyu, qqkf__exigh)
            hxp__vjonh += wic__mmyzl
        zsigh__nwy = bodo.hiframes.series_kernels._sum_handle_nan(kbfs__xnyu,
            hxp__vjonh)
        return zsigh__nwy
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
    kqbr__orhv = types.float64
    erg__siy = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        kqbr__orhv = types.float32
        erg__siy = types.float32
    qzap__vxpg = kqbr__orhv(0)
    ygqyv__aer = erg__siy(0)
    mhesi__pjf = erg__siy(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kbfs__xnyu = qzap__vxpg
        hxp__vjonh = ygqyv__aer
        for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
            qqkf__exigh = qzap__vxpg
            wic__mmyzl = ygqyv__aer
            if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                qqkf__exigh = arr[reu__dzbpx]
                wic__mmyzl = mhesi__pjf
            kbfs__xnyu += qqkf__exigh
            hxp__vjonh += wic__mmyzl
        zsigh__nwy = bodo.hiframes.series_kernels._mean_handle_nan(kbfs__xnyu,
            hxp__vjonh)
        return zsigh__nwy
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        wudpu__dfng = 0.0
        pbjeb__iaayr = 0.0
        hxp__vjonh = 0
        for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
            qqkf__exigh = 0.0
            wic__mmyzl = 0
            if not bodo.libs.array_kernels.isna(arr, reu__dzbpx) or not skipna:
                qqkf__exigh = arr[reu__dzbpx]
                wic__mmyzl = 1
            wudpu__dfng += qqkf__exigh
            pbjeb__iaayr += qqkf__exigh * qqkf__exigh
            hxp__vjonh += wic__mmyzl
        zsigh__nwy = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            wudpu__dfng, pbjeb__iaayr, hxp__vjonh, ddof)
        return zsigh__nwy
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
                fztky__ybnq = np.empty(len(q), np.int64)
                for reu__dzbpx in range(len(q)):
                    bexz__ehin = np.float64(q[reu__dzbpx])
                    fztky__ybnq[reu__dzbpx] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), bexz__ehin)
                return fztky__ybnq.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            fztky__ybnq = np.empty(len(q), np.float64)
            for reu__dzbpx in range(len(q)):
                bexz__ehin = np.float64(q[reu__dzbpx])
                fztky__ybnq[reu__dzbpx] = bodo.libs.array_kernels.quantile(arr,
                    bexz__ehin)
            return fztky__ybnq
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
        ssg__hfdue = types.intp
    elif arr.dtype == types.bool_:
        ssg__hfdue = np.int64
    else:
        ssg__hfdue = arr.dtype
    ousd__evexs = ssg__hfdue(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = ousd__evexs
            xmrjr__cia = len(arr)
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(xmrjr__cia):
                qqkf__exigh = ousd__evexs
                wic__mmyzl = 0
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx
                    ) or not skipna:
                    qqkf__exigh = arr[reu__dzbpx]
                    wic__mmyzl = 1
                kbfs__xnyu += qqkf__exigh
                hxp__vjonh += wic__mmyzl
            zsigh__nwy = bodo.hiframes.series_kernels._var_handle_mincount(
                kbfs__xnyu, hxp__vjonh, min_count)
            return zsigh__nwy
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = ousd__evexs
            xmrjr__cia = len(arr)
            for reu__dzbpx in numba.parfors.parfor.internal_prange(xmrjr__cia):
                qqkf__exigh = ousd__evexs
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                    qqkf__exigh = arr[reu__dzbpx]
                kbfs__xnyu += qqkf__exigh
            return kbfs__xnyu
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    bwrhx__rmvlg = arr.dtype(1)
    if arr.dtype == types.bool_:
        bwrhx__rmvlg = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = bwrhx__rmvlg
            hxp__vjonh = 0
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
                qqkf__exigh = bwrhx__rmvlg
                wic__mmyzl = 0
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx
                    ) or not skipna:
                    qqkf__exigh = arr[reu__dzbpx]
                    wic__mmyzl = 1
                hxp__vjonh += wic__mmyzl
                kbfs__xnyu *= qqkf__exigh
            zsigh__nwy = bodo.hiframes.series_kernels._var_handle_mincount(
                kbfs__xnyu, hxp__vjonh, min_count)
            return zsigh__nwy
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            kbfs__xnyu = bwrhx__rmvlg
            for reu__dzbpx in numba.parfors.parfor.internal_prange(len(arr)):
                qqkf__exigh = bwrhx__rmvlg
                if not bodo.libs.array_kernels.isna(arr, reu__dzbpx):
                    qqkf__exigh = arr[reu__dzbpx]
                kbfs__xnyu *= qqkf__exigh
            return kbfs__xnyu
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        reu__dzbpx = bodo.libs.array_kernels._nan_argmax(arr)
        return index[reu__dzbpx]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        reu__dzbpx = bodo.libs.array_kernels._nan_argmin(arr)
        return index[reu__dzbpx]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            thy__hnbqn = {}
            for jao__odysd in values:
                thy__hnbqn[bodo.utils.conversion.box_if_dt64(jao__odysd)] = 0
            return thy__hnbqn
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
        xmrjr__cia = len(arr)
        fztky__ybnq = np.empty(xmrjr__cia, np.bool_)
        for reu__dzbpx in numba.parfors.parfor.internal_prange(xmrjr__cia):
            fztky__ybnq[reu__dzbpx] = bodo.utils.conversion.box_if_dt64(arr
                [reu__dzbpx]) in values
        return fztky__ybnq
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    xshfx__mocfr = len(in_arr_tup) != 1
    xorf__sffd = list(in_arr_tup.types)
    jbng__xci = 'def impl(in_arr_tup):\n'
    jbng__xci += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    jbng__xci += '  n = len(in_arr_tup[0])\n'
    if xshfx__mocfr:
        mqxnx__jzy = ', '.join([f'in_arr_tup[{reu__dzbpx}][unused]' for
            reu__dzbpx in range(len(in_arr_tup))])
        ejt__zlb = ', '.join(['False' for ehbah__bjx in range(len(in_arr_tup))]
            )
        jbng__xci += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({mqxnx__jzy},), ({ejt__zlb},)): 0 for unused in range(0)}}
"""
        jbng__xci += '  map_vector = np.empty(n, np.int64)\n'
        for reu__dzbpx, ktmc__lhjau in enumerate(xorf__sffd):
            jbng__xci += f'  in_lst_{reu__dzbpx} = []\n'
            if is_str_arr_type(ktmc__lhjau):
                jbng__xci += f'  total_len_{reu__dzbpx} = 0\n'
            jbng__xci += f'  null_in_lst_{reu__dzbpx} = []\n'
        jbng__xci += '  for i in range(n):\n'
        uwdw__xgwsc = ', '.join([f'in_arr_tup[{reu__dzbpx}][i]' for
            reu__dzbpx in range(len(xorf__sffd))])
        bbryn__mqef = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{reu__dzbpx}], i)' for
            reu__dzbpx in range(len(xorf__sffd))])
        jbng__xci += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({uwdw__xgwsc},), ({bbryn__mqef},))
"""
        jbng__xci += '    if data_val not in arr_map:\n'
        jbng__xci += '      set_val = len(arr_map)\n'
        jbng__xci += '      values_tup = data_val._data\n'
        jbng__xci += '      nulls_tup = data_val._null_values\n'
        for reu__dzbpx, ktmc__lhjau in enumerate(xorf__sffd):
            jbng__xci += (
                f'      in_lst_{reu__dzbpx}.append(values_tup[{reu__dzbpx}])\n'
                )
            jbng__xci += (
                f'      null_in_lst_{reu__dzbpx}.append(nulls_tup[{reu__dzbpx}])\n'
                )
            if is_str_arr_type(ktmc__lhjau):
                jbng__xci += f"""      total_len_{reu__dzbpx}  += nulls_tup[{reu__dzbpx}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{reu__dzbpx}], i)
"""
        jbng__xci += '      arr_map[data_val] = len(arr_map)\n'
        jbng__xci += '    else:\n'
        jbng__xci += '      set_val = arr_map[data_val]\n'
        jbng__xci += '    map_vector[i] = set_val\n'
        jbng__xci += '  n_rows = len(arr_map)\n'
        for reu__dzbpx, ktmc__lhjau in enumerate(xorf__sffd):
            if is_str_arr_type(ktmc__lhjau):
                jbng__xci += f"""  out_arr_{reu__dzbpx} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{reu__dzbpx})
"""
            else:
                jbng__xci += f"""  out_arr_{reu__dzbpx} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{reu__dzbpx}], (-1,))
"""
        jbng__xci += '  for j in range(len(arr_map)):\n'
        for reu__dzbpx in range(len(xorf__sffd)):
            jbng__xci += f'    if null_in_lst_{reu__dzbpx}[j]:\n'
            jbng__xci += (
                f'      bodo.libs.array_kernels.setna(out_arr_{reu__dzbpx}, j)\n'
                )
            jbng__xci += '    else:\n'
            jbng__xci += (
                f'      out_arr_{reu__dzbpx}[j] = in_lst_{reu__dzbpx}[j]\n')
        yvpue__ysi = ', '.join([f'out_arr_{reu__dzbpx}' for reu__dzbpx in
            range(len(xorf__sffd))])
        jbng__xci += "  ev.add_attribute('n_map_entries', n_rows)\n"
        jbng__xci += '  ev.finalize()\n'
        jbng__xci += f'  return ({yvpue__ysi},), map_vector\n'
    else:
        jbng__xci += '  in_arr = in_arr_tup[0]\n'
        jbng__xci += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        jbng__xci += '  map_vector = np.empty(n, np.int64)\n'
        jbng__xci += '  is_na = 0\n'
        jbng__xci += '  in_lst = []\n'
        jbng__xci += '  na_idxs = []\n'
        if is_str_arr_type(xorf__sffd[0]):
            jbng__xci += '  total_len = 0\n'
        jbng__xci += '  for i in range(n):\n'
        jbng__xci += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        jbng__xci += '      is_na = 1\n'
        jbng__xci += '      # Always put NA in the last location.\n'
        jbng__xci += '      # We use -1 as a placeholder\n'
        jbng__xci += '      set_val = -1\n'
        jbng__xci += '      na_idxs.append(i)\n'
        jbng__xci += '    else:\n'
        jbng__xci += '      data_val = in_arr[i]\n'
        jbng__xci += '      if data_val not in arr_map:\n'
        jbng__xci += '        set_val = len(arr_map)\n'
        jbng__xci += '        in_lst.append(data_val)\n'
        if is_str_arr_type(xorf__sffd[0]):
            jbng__xci += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        jbng__xci += '        arr_map[data_val] = len(arr_map)\n'
        jbng__xci += '      else:\n'
        jbng__xci += '        set_val = arr_map[data_val]\n'
        jbng__xci += '    map_vector[i] = set_val\n'
        jbng__xci += '  map_vector[na_idxs] = len(arr_map)\n'
        jbng__xci += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(xorf__sffd[0]):
            jbng__xci += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            jbng__xci += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        jbng__xci += '  for j in range(len(arr_map)):\n'
        jbng__xci += '    out_arr[j] = in_lst[j]\n'
        jbng__xci += '  if is_na:\n'
        jbng__xci += '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n'
        jbng__xci += "  ev.add_attribute('n_map_entries', n_rows)\n"
        jbng__xci += '  ev.finalize()\n'
        jbng__xci += f'  return (out_arr,), map_vector\n'
    igtdt__xfmx = {}
    exec(jbng__xci, {'bodo': bodo, 'np': np, 'tracing': tracing}, igtdt__xfmx)
    impl = igtdt__xfmx['impl']
    return impl
