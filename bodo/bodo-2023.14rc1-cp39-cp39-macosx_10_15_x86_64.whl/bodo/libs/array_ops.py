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
        dqcwx__goyok = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        dqcwx__goyok = False
    elif A == bodo.string_array_type:
        dqcwx__goyok = ''
    elif A == bodo.binary_array_type:
        dqcwx__goyok = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        zmn__olhu = 0
        for hsp__qrx in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, hsp__qrx):
                if A[hsp__qrx] != dqcwx__goyok:
                    zmn__olhu += 1
        return zmn__olhu != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        dqcwx__goyok = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        dqcwx__goyok = False
    elif A == bodo.string_array_type:
        dqcwx__goyok = ''
    elif A == bodo.binary_array_type:
        dqcwx__goyok = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        zmn__olhu = 0
        for hsp__qrx in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, hsp__qrx):
                if A[hsp__qrx] == dqcwx__goyok:
                    zmn__olhu += 1
        return zmn__olhu == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    jon__mnkad = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(jon__mnkad.ctypes,
        arr, parallel, skipna)
    return jon__mnkad[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ggdg__qkag = len(arr)
        oxefo__zyfe = np.empty(ggdg__qkag, np.bool_)
        for hsp__qrx in numba.parfors.parfor.internal_prange(ggdg__qkag):
            oxefo__zyfe[hsp__qrx] = bodo.libs.array_kernels.isna(arr, hsp__qrx)
        return oxefo__zyfe
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        zmn__olhu = 0
        for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
            zjc__cwyte = 0
            if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                zjc__cwyte = 1
            zmn__olhu += zjc__cwyte
        jon__mnkad = zmn__olhu
        return jon__mnkad
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    xtur__woxt = array_op_count(arr)
    onxh__xrldh = array_op_min(arr)
    mkoph__slzrj = array_op_max(arr)
    cgo__vmeu = array_op_mean(arr)
    xyt__fed = array_op_std(arr)
    tocx__ejjqc = array_op_quantile(arr, 0.25)
    kuit__ryry = array_op_quantile(arr, 0.5)
    wkmeo__pfni = array_op_quantile(arr, 0.75)
    return (xtur__woxt, cgo__vmeu, xyt__fed, onxh__xrldh, tocx__ejjqc,
        kuit__ryry, wkmeo__pfni, mkoph__slzrj)


def array_op_describe_dt_impl(arr):
    xtur__woxt = array_op_count(arr)
    onxh__xrldh = array_op_min(arr)
    mkoph__slzrj = array_op_max(arr)
    cgo__vmeu = array_op_mean(arr)
    tocx__ejjqc = array_op_quantile(arr, 0.25)
    kuit__ryry = array_op_quantile(arr, 0.5)
    wkmeo__pfni = array_op_quantile(arr, 0.75)
    return (xtur__woxt, cgo__vmeu, onxh__xrldh, tocx__ejjqc, kuit__ryry,
        wkmeo__pfni, mkoph__slzrj)


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
            pulrz__vzuac = numba.cpython.builtins.get_type_max_value(np.int64)
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
                kpxbk__uyb = pulrz__vzuac
                zjc__cwyte = 0
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                    kpxbk__uyb = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[hsp__qrx]))
                    zjc__cwyte = 1
                pulrz__vzuac = min(pulrz__vzuac, kpxbk__uyb)
                zmn__olhu += zjc__cwyte
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(pulrz__vzuac,
                zmn__olhu)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = numba.cpython.builtins.get_type_max_value(np.int64)
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
                kpxbk__uyb = pulrz__vzuac
                zjc__cwyte = 0
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                    kpxbk__uyb = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[hsp__qrx]))
                    zjc__cwyte = 1
                pulrz__vzuac = min(pulrz__vzuac, kpxbk__uyb)
                zmn__olhu += zjc__cwyte
            return bodo.hiframes.pd_index_ext._dti_val_finalize(pulrz__vzuac,
                zmn__olhu)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            mbkm__sphe = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = numba.cpython.builtins.get_type_max_value(np.int64)
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(
                mbkm__sphe)):
                wrp__pvy = mbkm__sphe[hsp__qrx]
                if wrp__pvy == -1:
                    continue
                pulrz__vzuac = min(pulrz__vzuac, wrp__pvy)
                zmn__olhu += 1
            jon__mnkad = bodo.hiframes.series_kernels._box_cat_val(pulrz__vzuac
                , arr.dtype, zmn__olhu)
            return jon__mnkad
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = bodo.hiframes.series_kernels._get_date_max_value()
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
                kpxbk__uyb = pulrz__vzuac
                zjc__cwyte = 0
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                    kpxbk__uyb = arr[hsp__qrx]
                    zjc__cwyte = 1
                pulrz__vzuac = min(pulrz__vzuac, kpxbk__uyb)
                zmn__olhu += zjc__cwyte
            jon__mnkad = bodo.hiframes.series_kernels._sum_handle_nan(
                pulrz__vzuac, zmn__olhu)
            return jon__mnkad
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        pulrz__vzuac = bodo.hiframes.series_kernels._get_type_max_value(arr
            .dtype)
        zmn__olhu = 0
        for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
            kpxbk__uyb = pulrz__vzuac
            zjc__cwyte = 0
            if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                kpxbk__uyb = arr[hsp__qrx]
                zjc__cwyte = 1
            pulrz__vzuac = min(pulrz__vzuac, kpxbk__uyb)
            zmn__olhu += zjc__cwyte
        jon__mnkad = bodo.hiframes.series_kernels._sum_handle_nan(pulrz__vzuac,
            zmn__olhu)
        return jon__mnkad
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = numba.cpython.builtins.get_type_min_value(np.int64)
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
                kpxbk__uyb = pulrz__vzuac
                zjc__cwyte = 0
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                    kpxbk__uyb = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[hsp__qrx]))
                    zjc__cwyte = 1
                pulrz__vzuac = max(pulrz__vzuac, kpxbk__uyb)
                zmn__olhu += zjc__cwyte
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(pulrz__vzuac,
                zmn__olhu)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = numba.cpython.builtins.get_type_min_value(np.int64)
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
                kpxbk__uyb = pulrz__vzuac
                zjc__cwyte = 0
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                    kpxbk__uyb = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[hsp__qrx]))
                    zjc__cwyte = 1
                pulrz__vzuac = max(pulrz__vzuac, kpxbk__uyb)
                zmn__olhu += zjc__cwyte
            return bodo.hiframes.pd_index_ext._dti_val_finalize(pulrz__vzuac,
                zmn__olhu)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            mbkm__sphe = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = -1
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(
                mbkm__sphe)):
                pulrz__vzuac = max(pulrz__vzuac, mbkm__sphe[hsp__qrx])
            jon__mnkad = bodo.hiframes.series_kernels._box_cat_val(pulrz__vzuac
                , arr.dtype, 1)
            return jon__mnkad
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = bodo.hiframes.series_kernels._get_date_min_value()
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
                kpxbk__uyb = pulrz__vzuac
                zjc__cwyte = 0
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                    kpxbk__uyb = arr[hsp__qrx]
                    zjc__cwyte = 1
                pulrz__vzuac = max(pulrz__vzuac, kpxbk__uyb)
                zmn__olhu += zjc__cwyte
            jon__mnkad = bodo.hiframes.series_kernels._sum_handle_nan(
                pulrz__vzuac, zmn__olhu)
            return jon__mnkad
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        pulrz__vzuac = bodo.hiframes.series_kernels._get_type_min_value(arr
            .dtype)
        zmn__olhu = 0
        for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
            kpxbk__uyb = pulrz__vzuac
            zjc__cwyte = 0
            if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                kpxbk__uyb = arr[hsp__qrx]
                zjc__cwyte = 1
            pulrz__vzuac = max(pulrz__vzuac, kpxbk__uyb)
            zmn__olhu += zjc__cwyte
        jon__mnkad = bodo.hiframes.series_kernels._sum_handle_nan(pulrz__vzuac,
            zmn__olhu)
        return jon__mnkad
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
    tmn__exkb = types.float64
    ptiy__jgeg = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        tmn__exkb = types.float32
        ptiy__jgeg = types.float32
    efao__zqej = tmn__exkb(0)
    zeg__fzncp = ptiy__jgeg(0)
    yjmrn__dme = ptiy__jgeg(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        pulrz__vzuac = efao__zqej
        zmn__olhu = zeg__fzncp
        for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
            kpxbk__uyb = efao__zqej
            zjc__cwyte = zeg__fzncp
            if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                kpxbk__uyb = arr[hsp__qrx]
                zjc__cwyte = yjmrn__dme
            pulrz__vzuac += kpxbk__uyb
            zmn__olhu += zjc__cwyte
        jon__mnkad = bodo.hiframes.series_kernels._mean_handle_nan(pulrz__vzuac
            , zmn__olhu)
        return jon__mnkad
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        lvwdz__nri = 0.0
        qbmo__aankd = 0.0
        zmn__olhu = 0
        for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
            kpxbk__uyb = 0.0
            zjc__cwyte = 0
            if not bodo.libs.array_kernels.isna(arr, hsp__qrx) or not skipna:
                kpxbk__uyb = arr[hsp__qrx]
                zjc__cwyte = 1
            lvwdz__nri += kpxbk__uyb
            qbmo__aankd += kpxbk__uyb * kpxbk__uyb
            zmn__olhu += zjc__cwyte
        jon__mnkad = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            lvwdz__nri, qbmo__aankd, zmn__olhu, ddof)
        return jon__mnkad
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
                oxefo__zyfe = np.empty(len(q), np.int64)
                for hsp__qrx in range(len(q)):
                    odhj__kkz = np.float64(q[hsp__qrx])
                    oxefo__zyfe[hsp__qrx] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), odhj__kkz)
                return oxefo__zyfe.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            oxefo__zyfe = np.empty(len(q), np.float64)
            for hsp__qrx in range(len(q)):
                odhj__kkz = np.float64(q[hsp__qrx])
                oxefo__zyfe[hsp__qrx] = bodo.libs.array_kernels.quantile(arr,
                    odhj__kkz)
            return oxefo__zyfe
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
        weref__ggugz = types.intp
    elif arr.dtype == types.bool_:
        weref__ggugz = np.int64
    else:
        weref__ggugz = arr.dtype
    omk__sfsf = weref__ggugz(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = omk__sfsf
            ggdg__qkag = len(arr)
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(ggdg__qkag):
                kpxbk__uyb = omk__sfsf
                zjc__cwyte = 0
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx
                    ) or not skipna:
                    kpxbk__uyb = arr[hsp__qrx]
                    zjc__cwyte = 1
                pulrz__vzuac += kpxbk__uyb
                zmn__olhu += zjc__cwyte
            jon__mnkad = bodo.hiframes.series_kernels._var_handle_mincount(
                pulrz__vzuac, zmn__olhu, min_count)
            return jon__mnkad
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = omk__sfsf
            ggdg__qkag = len(arr)
            for hsp__qrx in numba.parfors.parfor.internal_prange(ggdg__qkag):
                kpxbk__uyb = omk__sfsf
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                    kpxbk__uyb = arr[hsp__qrx]
                pulrz__vzuac += kpxbk__uyb
            return pulrz__vzuac
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    jvlfa__ikemg = arr.dtype(1)
    if arr.dtype == types.bool_:
        jvlfa__ikemg = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = jvlfa__ikemg
            zmn__olhu = 0
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
                kpxbk__uyb = jvlfa__ikemg
                zjc__cwyte = 0
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx
                    ) or not skipna:
                    kpxbk__uyb = arr[hsp__qrx]
                    zjc__cwyte = 1
                zmn__olhu += zjc__cwyte
                pulrz__vzuac *= kpxbk__uyb
            jon__mnkad = bodo.hiframes.series_kernels._var_handle_mincount(
                pulrz__vzuac, zmn__olhu, min_count)
            return jon__mnkad
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            pulrz__vzuac = jvlfa__ikemg
            for hsp__qrx in numba.parfors.parfor.internal_prange(len(arr)):
                kpxbk__uyb = jvlfa__ikemg
                if not bodo.libs.array_kernels.isna(arr, hsp__qrx):
                    kpxbk__uyb = arr[hsp__qrx]
                pulrz__vzuac *= kpxbk__uyb
            return pulrz__vzuac
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        hsp__qrx = bodo.libs.array_kernels._nan_argmax(arr)
        return index[hsp__qrx]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        hsp__qrx = bodo.libs.array_kernels._nan_argmin(arr)
        return index[hsp__qrx]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            xuis__imz = {}
            for erzd__sqkr in values:
                xuis__imz[bodo.utils.conversion.box_if_dt64(erzd__sqkr)] = 0
            return xuis__imz
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
        ggdg__qkag = len(arr)
        oxefo__zyfe = np.empty(ggdg__qkag, np.bool_)
        for hsp__qrx in numba.parfors.parfor.internal_prange(ggdg__qkag):
            oxefo__zyfe[hsp__qrx] = bodo.utils.conversion.box_if_dt64(arr[
                hsp__qrx]) in values
        return oxefo__zyfe
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    bbz__sxr = len(in_arr_tup) != 1
    pldo__sykjt = list(in_arr_tup.types)
    codo__qcrz = 'def impl(in_arr_tup):\n'
    codo__qcrz += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    codo__qcrz += '  n = len(in_arr_tup[0])\n'
    if bbz__sxr:
        wqnv__szd = ', '.join([f'in_arr_tup[{hsp__qrx}][unused]' for
            hsp__qrx in range(len(in_arr_tup))])
        mdb__phj = ', '.join(['False' for frwrz__belv in range(len(
            in_arr_tup))])
        codo__qcrz += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({wqnv__szd},), ({mdb__phj},)): 0 for unused in range(0)}}
"""
        codo__qcrz += '  map_vector = np.empty(n, np.int64)\n'
        for hsp__qrx, enb__xgwdq in enumerate(pldo__sykjt):
            codo__qcrz += f'  in_lst_{hsp__qrx} = []\n'
            if is_str_arr_type(enb__xgwdq):
                codo__qcrz += f'  total_len_{hsp__qrx} = 0\n'
            codo__qcrz += f'  null_in_lst_{hsp__qrx} = []\n'
        codo__qcrz += '  for i in range(n):\n'
        yrv__oack = ', '.join([f'in_arr_tup[{hsp__qrx}][i]' for hsp__qrx in
            range(len(pldo__sykjt))])
        mnryk__dokfr = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{hsp__qrx}], i)' for
            hsp__qrx in range(len(pldo__sykjt))])
        codo__qcrz += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({yrv__oack},), ({mnryk__dokfr},))
"""
        codo__qcrz += '    if data_val not in arr_map:\n'
        codo__qcrz += '      set_val = len(arr_map)\n'
        codo__qcrz += '      values_tup = data_val._data\n'
        codo__qcrz += '      nulls_tup = data_val._null_values\n'
        for hsp__qrx, enb__xgwdq in enumerate(pldo__sykjt):
            codo__qcrz += (
                f'      in_lst_{hsp__qrx}.append(values_tup[{hsp__qrx}])\n')
            codo__qcrz += (
                f'      null_in_lst_{hsp__qrx}.append(nulls_tup[{hsp__qrx}])\n'
                )
            if is_str_arr_type(enb__xgwdq):
                codo__qcrz += f"""      total_len_{hsp__qrx}  += nulls_tup[{hsp__qrx}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{hsp__qrx}], i)
"""
        codo__qcrz += '      arr_map[data_val] = len(arr_map)\n'
        codo__qcrz += '    else:\n'
        codo__qcrz += '      set_val = arr_map[data_val]\n'
        codo__qcrz += '    map_vector[i] = set_val\n'
        codo__qcrz += '  n_rows = len(arr_map)\n'
        for hsp__qrx, enb__xgwdq in enumerate(pldo__sykjt):
            if is_str_arr_type(enb__xgwdq):
                codo__qcrz += f"""  out_arr_{hsp__qrx} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{hsp__qrx})
"""
            else:
                codo__qcrz += f"""  out_arr_{hsp__qrx} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{hsp__qrx}], (-1,))
"""
        codo__qcrz += '  for j in range(len(arr_map)):\n'
        for hsp__qrx in range(len(pldo__sykjt)):
            codo__qcrz += f'    if null_in_lst_{hsp__qrx}[j]:\n'
            codo__qcrz += (
                f'      bodo.libs.array_kernels.setna(out_arr_{hsp__qrx}, j)\n'
                )
            codo__qcrz += '    else:\n'
            codo__qcrz += (
                f'      out_arr_{hsp__qrx}[j] = in_lst_{hsp__qrx}[j]\n')
        fkd__nzng = ', '.join([f'out_arr_{hsp__qrx}' for hsp__qrx in range(
            len(pldo__sykjt))])
        codo__qcrz += "  ev.add_attribute('n_map_entries', n_rows)\n"
        codo__qcrz += '  ev.finalize()\n'
        codo__qcrz += f'  return ({fkd__nzng},), map_vector\n'
    else:
        codo__qcrz += '  in_arr = in_arr_tup[0]\n'
        codo__qcrz += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        codo__qcrz += '  map_vector = np.empty(n, np.int64)\n'
        codo__qcrz += '  is_na = 0\n'
        codo__qcrz += '  in_lst = []\n'
        codo__qcrz += '  na_idxs = []\n'
        if is_str_arr_type(pldo__sykjt[0]):
            codo__qcrz += '  total_len = 0\n'
        codo__qcrz += '  for i in range(n):\n'
        codo__qcrz += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        codo__qcrz += '      is_na = 1\n'
        codo__qcrz += '      # Always put NA in the last location.\n'
        codo__qcrz += '      # We use -1 as a placeholder\n'
        codo__qcrz += '      set_val = -1\n'
        codo__qcrz += '      na_idxs.append(i)\n'
        codo__qcrz += '    else:\n'
        codo__qcrz += '      data_val = in_arr[i]\n'
        codo__qcrz += '      if data_val not in arr_map:\n'
        codo__qcrz += '        set_val = len(arr_map)\n'
        codo__qcrz += '        in_lst.append(data_val)\n'
        if is_str_arr_type(pldo__sykjt[0]):
            codo__qcrz += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        codo__qcrz += '        arr_map[data_val] = len(arr_map)\n'
        codo__qcrz += '      else:\n'
        codo__qcrz += '        set_val = arr_map[data_val]\n'
        codo__qcrz += '    map_vector[i] = set_val\n'
        codo__qcrz += '  map_vector[na_idxs] = len(arr_map)\n'
        codo__qcrz += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(pldo__sykjt[0]):
            codo__qcrz += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            codo__qcrz += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        codo__qcrz += '  for j in range(len(arr_map)):\n'
        codo__qcrz += '    out_arr[j] = in_lst[j]\n'
        codo__qcrz += '  if is_na:\n'
        codo__qcrz += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        codo__qcrz += "  ev.add_attribute('n_map_entries', n_rows)\n"
        codo__qcrz += '  ev.finalize()\n'
        codo__qcrz += f'  return (out_arr,), map_vector\n'
    zdag__uhrk = {}
    exec(codo__qcrz, {'bodo': bodo, 'np': np, 'tracing': tracing}, zdag__uhrk)
    impl = zdag__uhrk['impl']
    return impl
