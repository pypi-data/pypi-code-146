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
        etm__nrksl = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        etm__nrksl = False
    elif A == bodo.string_array_type:
        etm__nrksl = ''
    elif A == bodo.binary_array_type:
        etm__nrksl = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        zla__axda = 0
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, rlxnk__uzcnf):
                if A[rlxnk__uzcnf] != etm__nrksl:
                    zla__axda += 1
        return zla__axda != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        etm__nrksl = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        etm__nrksl = False
    elif A == bodo.string_array_type:
        etm__nrksl = ''
    elif A == bodo.binary_array_type:
        etm__nrksl = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        zla__axda = 0
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, rlxnk__uzcnf):
                if A[rlxnk__uzcnf] == etm__nrksl:
                    zla__axda += 1
        return zla__axda == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    rnn__qjqo = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(rnn__qjqo.ctypes, arr,
        parallel, skipna)
    return rnn__qjqo[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        lnso__bqlh = len(arr)
        xcpk__yfzur = np.empty(lnso__bqlh, np.bool_)
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(lnso__bqlh):
            xcpk__yfzur[rlxnk__uzcnf] = bodo.libs.array_kernels.isna(arr,
                rlxnk__uzcnf)
        return xcpk__yfzur
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        zla__axda = 0
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
            xjd__qeagl = 0
            if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                xjd__qeagl = 1
            zla__axda += xjd__qeagl
        rnn__qjqo = zla__axda
        return rnn__qjqo
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    fca__fhf = array_op_count(arr)
    dwxao__pvn = array_op_min(arr)
    yule__cwbma = array_op_max(arr)
    ghbpn__ixbvy = array_op_mean(arr)
    enjca__vcaci = array_op_std(arr)
    hxs__hgnt = array_op_quantile(arr, 0.25)
    tfptq__sua = array_op_quantile(arr, 0.5)
    mmtzt__bzckc = array_op_quantile(arr, 0.75)
    return (fca__fhf, ghbpn__ixbvy, enjca__vcaci, dwxao__pvn, hxs__hgnt,
        tfptq__sua, mmtzt__bzckc, yule__cwbma)


def array_op_describe_dt_impl(arr):
    fca__fhf = array_op_count(arr)
    dwxao__pvn = array_op_min(arr)
    yule__cwbma = array_op_max(arr)
    ghbpn__ixbvy = array_op_mean(arr)
    hxs__hgnt = array_op_quantile(arr, 0.25)
    tfptq__sua = array_op_quantile(arr, 0.5)
    mmtzt__bzckc = array_op_quantile(arr, 0.75)
    return (fca__fhf, ghbpn__ixbvy, dwxao__pvn, hxs__hgnt, tfptq__sua,
        mmtzt__bzckc, yule__cwbma)


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
            ilnbr__ryov = numba.cpython.builtins.get_type_max_value(np.int64)
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
                vflmv__vxzs = ilnbr__ryov
                xjd__qeagl = 0
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                    vflmv__vxzs = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[rlxnk__uzcnf]))
                    xjd__qeagl = 1
                ilnbr__ryov = min(ilnbr__ryov, vflmv__vxzs)
                zla__axda += xjd__qeagl
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(ilnbr__ryov,
                zla__axda)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = numba.cpython.builtins.get_type_max_value(np.int64)
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
                vflmv__vxzs = ilnbr__ryov
                xjd__qeagl = 0
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                    vflmv__vxzs = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[rlxnk__uzcnf]))
                    xjd__qeagl = 1
                ilnbr__ryov = min(ilnbr__ryov, vflmv__vxzs)
                zla__axda += xjd__qeagl
            return bodo.hiframes.pd_index_ext._dti_val_finalize(ilnbr__ryov,
                zla__axda)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            tyehc__vndjy = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = numba.cpython.builtins.get_type_max_value(np.int64)
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(
                tyehc__vndjy)):
                fnzts__gfu = tyehc__vndjy[rlxnk__uzcnf]
                if fnzts__gfu == -1:
                    continue
                ilnbr__ryov = min(ilnbr__ryov, fnzts__gfu)
                zla__axda += 1
            rnn__qjqo = bodo.hiframes.series_kernels._box_cat_val(ilnbr__ryov,
                arr.dtype, zla__axda)
            return rnn__qjqo
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = bodo.hiframes.series_kernels._get_date_max_value()
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
                vflmv__vxzs = ilnbr__ryov
                xjd__qeagl = 0
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                    vflmv__vxzs = arr[rlxnk__uzcnf]
                    xjd__qeagl = 1
                ilnbr__ryov = min(ilnbr__ryov, vflmv__vxzs)
                zla__axda += xjd__qeagl
            rnn__qjqo = bodo.hiframes.series_kernels._sum_handle_nan(
                ilnbr__ryov, zla__axda)
            return rnn__qjqo
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ilnbr__ryov = bodo.hiframes.series_kernels._get_type_max_value(arr.
            dtype)
        zla__axda = 0
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
            vflmv__vxzs = ilnbr__ryov
            xjd__qeagl = 0
            if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                vflmv__vxzs = arr[rlxnk__uzcnf]
                xjd__qeagl = 1
            ilnbr__ryov = min(ilnbr__ryov, vflmv__vxzs)
            zla__axda += xjd__qeagl
        rnn__qjqo = bodo.hiframes.series_kernels._sum_handle_nan(ilnbr__ryov,
            zla__axda)
        return rnn__qjqo
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = numba.cpython.builtins.get_type_min_value(np.int64)
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
                vflmv__vxzs = ilnbr__ryov
                xjd__qeagl = 0
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                    vflmv__vxzs = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[rlxnk__uzcnf]))
                    xjd__qeagl = 1
                ilnbr__ryov = max(ilnbr__ryov, vflmv__vxzs)
                zla__axda += xjd__qeagl
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(ilnbr__ryov,
                zla__axda)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = numba.cpython.builtins.get_type_min_value(np.int64)
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
                vflmv__vxzs = ilnbr__ryov
                xjd__qeagl = 0
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                    vflmv__vxzs = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[rlxnk__uzcnf]))
                    xjd__qeagl = 1
                ilnbr__ryov = max(ilnbr__ryov, vflmv__vxzs)
                zla__axda += xjd__qeagl
            return bodo.hiframes.pd_index_ext._dti_val_finalize(ilnbr__ryov,
                zla__axda)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            tyehc__vndjy = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = -1
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(
                tyehc__vndjy)):
                ilnbr__ryov = max(ilnbr__ryov, tyehc__vndjy[rlxnk__uzcnf])
            rnn__qjqo = bodo.hiframes.series_kernels._box_cat_val(ilnbr__ryov,
                arr.dtype, 1)
            return rnn__qjqo
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = bodo.hiframes.series_kernels._get_date_min_value()
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
                vflmv__vxzs = ilnbr__ryov
                xjd__qeagl = 0
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                    vflmv__vxzs = arr[rlxnk__uzcnf]
                    xjd__qeagl = 1
                ilnbr__ryov = max(ilnbr__ryov, vflmv__vxzs)
                zla__axda += xjd__qeagl
            rnn__qjqo = bodo.hiframes.series_kernels._sum_handle_nan(
                ilnbr__ryov, zla__axda)
            return rnn__qjqo
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ilnbr__ryov = bodo.hiframes.series_kernels._get_type_min_value(arr.
            dtype)
        zla__axda = 0
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
            vflmv__vxzs = ilnbr__ryov
            xjd__qeagl = 0
            if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                vflmv__vxzs = arr[rlxnk__uzcnf]
                xjd__qeagl = 1
            ilnbr__ryov = max(ilnbr__ryov, vflmv__vxzs)
            zla__axda += xjd__qeagl
        rnn__qjqo = bodo.hiframes.series_kernels._sum_handle_nan(ilnbr__ryov,
            zla__axda)
        return rnn__qjqo
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
    axuj__oel = types.float64
    lches__qttud = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        axuj__oel = types.float32
        lches__qttud = types.float32
    ihvqm__jgy = axuj__oel(0)
    afc__yusu = lches__qttud(0)
    rjq__umuh = lches__qttud(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ilnbr__ryov = ihvqm__jgy
        zla__axda = afc__yusu
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
            vflmv__vxzs = ihvqm__jgy
            xjd__qeagl = afc__yusu
            if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                vflmv__vxzs = arr[rlxnk__uzcnf]
                xjd__qeagl = rjq__umuh
            ilnbr__ryov += vflmv__vxzs
            zla__axda += xjd__qeagl
        rnn__qjqo = bodo.hiframes.series_kernels._mean_handle_nan(ilnbr__ryov,
            zla__axda)
        return rnn__qjqo
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        iijik__gptdn = 0.0
        tlyp__oem = 0.0
        zla__axda = 0
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
            vflmv__vxzs = 0.0
            xjd__qeagl = 0
            if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf
                ) or not skipna:
                vflmv__vxzs = arr[rlxnk__uzcnf]
                xjd__qeagl = 1
            iijik__gptdn += vflmv__vxzs
            tlyp__oem += vflmv__vxzs * vflmv__vxzs
            zla__axda += xjd__qeagl
        rnn__qjqo = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            iijik__gptdn, tlyp__oem, zla__axda, ddof)
        return rnn__qjqo
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
                xcpk__yfzur = np.empty(len(q), np.int64)
                for rlxnk__uzcnf in range(len(q)):
                    rxk__vuaol = np.float64(q[rlxnk__uzcnf])
                    xcpk__yfzur[rlxnk__uzcnf
                        ] = bodo.libs.array_kernels.quantile(arr.view(np.
                        int64), rxk__vuaol)
                return xcpk__yfzur.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            xcpk__yfzur = np.empty(len(q), np.float64)
            for rlxnk__uzcnf in range(len(q)):
                rxk__vuaol = np.float64(q[rlxnk__uzcnf])
                xcpk__yfzur[rlxnk__uzcnf] = bodo.libs.array_kernels.quantile(
                    arr, rxk__vuaol)
            return xcpk__yfzur
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
        tde__nwulz = types.intp
    elif arr.dtype == types.bool_:
        tde__nwulz = np.int64
    else:
        tde__nwulz = arr.dtype
    ltq__emwx = tde__nwulz(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = ltq__emwx
            lnso__bqlh = len(arr)
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(lnso__bqlh
                ):
                vflmv__vxzs = ltq__emwx
                xjd__qeagl = 0
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf
                    ) or not skipna:
                    vflmv__vxzs = arr[rlxnk__uzcnf]
                    xjd__qeagl = 1
                ilnbr__ryov += vflmv__vxzs
                zla__axda += xjd__qeagl
            rnn__qjqo = bodo.hiframes.series_kernels._var_handle_mincount(
                ilnbr__ryov, zla__axda, min_count)
            return rnn__qjqo
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = ltq__emwx
            lnso__bqlh = len(arr)
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(lnso__bqlh
                ):
                vflmv__vxzs = ltq__emwx
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                    vflmv__vxzs = arr[rlxnk__uzcnf]
                ilnbr__ryov += vflmv__vxzs
            return ilnbr__ryov
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    wekqn__srm = arr.dtype(1)
    if arr.dtype == types.bool_:
        wekqn__srm = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = wekqn__srm
            zla__axda = 0
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
                vflmv__vxzs = wekqn__srm
                xjd__qeagl = 0
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf
                    ) or not skipna:
                    vflmv__vxzs = arr[rlxnk__uzcnf]
                    xjd__qeagl = 1
                zla__axda += xjd__qeagl
                ilnbr__ryov *= vflmv__vxzs
            rnn__qjqo = bodo.hiframes.series_kernels._var_handle_mincount(
                ilnbr__ryov, zla__axda, min_count)
            return rnn__qjqo
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            ilnbr__ryov = wekqn__srm
            for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(len(arr)):
                vflmv__vxzs = wekqn__srm
                if not bodo.libs.array_kernels.isna(arr, rlxnk__uzcnf):
                    vflmv__vxzs = arr[rlxnk__uzcnf]
                ilnbr__ryov *= vflmv__vxzs
            return ilnbr__ryov
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        rlxnk__uzcnf = bodo.libs.array_kernels._nan_argmax(arr)
        return index[rlxnk__uzcnf]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        rlxnk__uzcnf = bodo.libs.array_kernels._nan_argmin(arr)
        return index[rlxnk__uzcnf]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            wsiaq__ybefz = {}
            for mtspt__xvmlx in values:
                wsiaq__ybefz[bodo.utils.conversion.box_if_dt64(mtspt__xvmlx)
                    ] = 0
            return wsiaq__ybefz
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
        lnso__bqlh = len(arr)
        xcpk__yfzur = np.empty(lnso__bqlh, np.bool_)
        for rlxnk__uzcnf in numba.parfors.parfor.internal_prange(lnso__bqlh):
            xcpk__yfzur[rlxnk__uzcnf] = bodo.utils.conversion.box_if_dt64(arr
                [rlxnk__uzcnf]) in values
        return xcpk__yfzur
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    hiro__itqq = len(in_arr_tup) != 1
    dbo__udfz = list(in_arr_tup.types)
    rjde__kzg = 'def impl(in_arr_tup):\n'
    rjde__kzg += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    rjde__kzg += '  n = len(in_arr_tup[0])\n'
    if hiro__itqq:
        cfc__god = ', '.join([f'in_arr_tup[{rlxnk__uzcnf}][unused]' for
            rlxnk__uzcnf in range(len(in_arr_tup))])
        ujiu__dap = ', '.join(['False' for rut__kud in range(len(in_arr_tup))])
        rjde__kzg += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({cfc__god},), ({ujiu__dap},)): 0 for unused in range(0)}}
"""
        rjde__kzg += '  map_vector = np.empty(n, np.int64)\n'
        for rlxnk__uzcnf, uuj__mwvx in enumerate(dbo__udfz):
            rjde__kzg += f'  in_lst_{rlxnk__uzcnf} = []\n'
            if is_str_arr_type(uuj__mwvx):
                rjde__kzg += f'  total_len_{rlxnk__uzcnf} = 0\n'
            rjde__kzg += f'  null_in_lst_{rlxnk__uzcnf} = []\n'
        rjde__kzg += '  for i in range(n):\n'
        okum__odxa = ', '.join([f'in_arr_tup[{rlxnk__uzcnf}][i]' for
            rlxnk__uzcnf in range(len(dbo__udfz))])
        naho__kckeb = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{rlxnk__uzcnf}], i)' for
            rlxnk__uzcnf in range(len(dbo__udfz))])
        rjde__kzg += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({okum__odxa},), ({naho__kckeb},))
"""
        rjde__kzg += '    if data_val not in arr_map:\n'
        rjde__kzg += '      set_val = len(arr_map)\n'
        rjde__kzg += '      values_tup = data_val._data\n'
        rjde__kzg += '      nulls_tup = data_val._null_values\n'
        for rlxnk__uzcnf, uuj__mwvx in enumerate(dbo__udfz):
            rjde__kzg += (
                f'      in_lst_{rlxnk__uzcnf}.append(values_tup[{rlxnk__uzcnf}])\n'
                )
            rjde__kzg += (
                f'      null_in_lst_{rlxnk__uzcnf}.append(nulls_tup[{rlxnk__uzcnf}])\n'
                )
            if is_str_arr_type(uuj__mwvx):
                rjde__kzg += f"""      total_len_{rlxnk__uzcnf}  += nulls_tup[{rlxnk__uzcnf}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{rlxnk__uzcnf}], i)
"""
        rjde__kzg += '      arr_map[data_val] = len(arr_map)\n'
        rjde__kzg += '    else:\n'
        rjde__kzg += '      set_val = arr_map[data_val]\n'
        rjde__kzg += '    map_vector[i] = set_val\n'
        rjde__kzg += '  n_rows = len(arr_map)\n'
        for rlxnk__uzcnf, uuj__mwvx in enumerate(dbo__udfz):
            if is_str_arr_type(uuj__mwvx):
                rjde__kzg += f"""  out_arr_{rlxnk__uzcnf} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{rlxnk__uzcnf})
"""
            else:
                rjde__kzg += f"""  out_arr_{rlxnk__uzcnf} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{rlxnk__uzcnf}], (-1,))
"""
        rjde__kzg += '  for j in range(len(arr_map)):\n'
        for rlxnk__uzcnf in range(len(dbo__udfz)):
            rjde__kzg += f'    if null_in_lst_{rlxnk__uzcnf}[j]:\n'
            rjde__kzg += (
                f'      bodo.libs.array_kernels.setna(out_arr_{rlxnk__uzcnf}, j)\n'
                )
            rjde__kzg += '    else:\n'
            rjde__kzg += (
                f'      out_arr_{rlxnk__uzcnf}[j] = in_lst_{rlxnk__uzcnf}[j]\n'
                )
        zwoa__wewb = ', '.join([f'out_arr_{rlxnk__uzcnf}' for rlxnk__uzcnf in
            range(len(dbo__udfz))])
        rjde__kzg += "  ev.add_attribute('n_map_entries', n_rows)\n"
        rjde__kzg += '  ev.finalize()\n'
        rjde__kzg += f'  return ({zwoa__wewb},), map_vector\n'
    else:
        rjde__kzg += '  in_arr = in_arr_tup[0]\n'
        rjde__kzg += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        rjde__kzg += '  map_vector = np.empty(n, np.int64)\n'
        rjde__kzg += '  is_na = 0\n'
        rjde__kzg += '  in_lst = []\n'
        rjde__kzg += '  na_idxs = []\n'
        if is_str_arr_type(dbo__udfz[0]):
            rjde__kzg += '  total_len = 0\n'
        rjde__kzg += '  for i in range(n):\n'
        rjde__kzg += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        rjde__kzg += '      is_na = 1\n'
        rjde__kzg += '      # Always put NA in the last location.\n'
        rjde__kzg += '      # We use -1 as a placeholder\n'
        rjde__kzg += '      set_val = -1\n'
        rjde__kzg += '      na_idxs.append(i)\n'
        rjde__kzg += '    else:\n'
        rjde__kzg += '      data_val = in_arr[i]\n'
        rjde__kzg += '      if data_val not in arr_map:\n'
        rjde__kzg += '        set_val = len(arr_map)\n'
        rjde__kzg += '        in_lst.append(data_val)\n'
        if is_str_arr_type(dbo__udfz[0]):
            rjde__kzg += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        rjde__kzg += '        arr_map[data_val] = len(arr_map)\n'
        rjde__kzg += '      else:\n'
        rjde__kzg += '        set_val = arr_map[data_val]\n'
        rjde__kzg += '    map_vector[i] = set_val\n'
        rjde__kzg += '  map_vector[na_idxs] = len(arr_map)\n'
        rjde__kzg += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(dbo__udfz[0]):
            rjde__kzg += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            rjde__kzg += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        rjde__kzg += '  for j in range(len(arr_map)):\n'
        rjde__kzg += '    out_arr[j] = in_lst[j]\n'
        rjde__kzg += '  if is_na:\n'
        rjde__kzg += '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n'
        rjde__kzg += "  ev.add_attribute('n_map_entries', n_rows)\n"
        rjde__kzg += '  ev.finalize()\n'
        rjde__kzg += f'  return (out_arr,), map_vector\n'
    vedx__zoqr = {}
    exec(rjde__kzg, {'bodo': bodo, 'np': np, 'tracing': tracing}, vedx__zoqr)
    impl = vedx__zoqr['impl']
    return impl
