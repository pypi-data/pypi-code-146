"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_local_dictionary, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import DictionaryArrayType, init_dict_arr
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, alloc_int_array
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import pre_alloc_string_array, str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, check_unsupported_args, decode_if_dict_array, element_type, find_common_np_dtype, get_overload_const_bool, get_overload_const_list, get_overload_const_str, is_bin_arr_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error, to_str_arr_if_dict_array
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)
max_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Max.value)
min_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Min.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr in (boolean_array,
        datetime_date_array_type, datetime_timedelta_array_type,
        string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    if isinstance(arr, bodo.NullableTupleType):
        return lambda arr, i: arr._null_values[i]
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._indices._null_bitmap, i) or bodo.libs.array_kernels.isna(arr.
            _data, arr._indices[i])
    if isinstance(arr, DatetimeArrayType):
        return lambda arr, i: np.isnat(arr._data[i])
    assert isinstance(arr, types.Array), f'Invalid array type in isna(): {arr}'
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr, types.Array) and isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        mfdvx__eaqma = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = mfdvx__eaqma
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        mfdvx__eaqma = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = mfdvx__eaqma
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, ind, int_nan_const=0: bodo.libs.array_kernels.setna(
            arr._indices, ind)
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            vct__sbj = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            vct__sbj[ind + 1] = vct__sbj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            vct__sbj = bodo.libs.array_item_arr_ext.get_offsets(arr)
            vct__sbj[ind + 1] = vct__sbj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            vct__sbj = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            vct__sbj[ind + 1] = vct__sbj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if isinstance(arr, bodo.TimeArrayType):

        def setna_time(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_time
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def copy_array_element(out_arr, out_ind, in_arr, in_ind):
    pass


@overload(copy_array_element)
def overload_copy_array_element(out_arr, out_ind, in_arr, in_ind):
    if out_arr == bodo.string_array_type and is_str_arr_type(in_arr):

        def impl_str(out_arr, out_ind, in_arr, in_ind):
            if bodo.libs.array_kernels.isna(in_arr, in_ind):
                bodo.libs.array_kernels.setna(out_arr, out_ind)
            else:
                bodo.libs.str_arr_ext.get_str_arr_item_copy(out_arr,
                    out_ind, in_arr, in_ind)
        return impl_str
    if isinstance(out_arr, DatetimeArrayType) and isinstance(in_arr,
        DatetimeArrayType) and out_arr.tz == in_arr.tz:

        def impl_dt(out_arr, out_ind, in_arr, in_ind):
            if bodo.libs.array_kernels.isna(in_arr, in_ind):
                bodo.libs.array_kernels.setna(out_arr, out_ind)
            else:
                out_arr._data[out_ind] = in_arr._data[in_ind]
        return impl_dt

    def impl(out_arr, out_ind, in_arr, in_ind):
        if bodo.libs.array_kernels.isna(in_arr, in_ind):
            bodo.libs.array_kernels.setna(out_arr, out_ind)
        else:
            out_arr[out_ind] = in_arr[in_ind]
    return impl


def setna_tup(arr_tup, ind, int_nan_const=0):
    pass


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    yvwm__rkys = arr_tup.count
    qnlwk__knzn = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(yvwm__rkys):
        qnlwk__knzn += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    qnlwk__knzn += '  return\n'
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'setna': setna}, rdewt__vpud)
    impl = rdewt__vpud['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        zbjf__migz = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(zbjf__migz.start, zbjf__migz.stop, zbjf__migz.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        frmz__mem = 'n'
        mye__ybpn = 'n_pes'
        bens__btn = 'min_op'
    else:
        frmz__mem = 'n-1, -1, -1'
        mye__ybpn = '-1'
        bens__btn = 'max_op'
    qnlwk__knzn = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {mye__ybpn}
    for i in range({frmz__mem}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {bens__btn}))
        if possible_valid_rank != {mye__ybpn}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, rdewt__vpud)
    impl = rdewt__vpud['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    xxz__pcs = array_to_info(arr)
    _median_series_computation(res, xxz__pcs, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xxz__pcs)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    xxz__pcs = array_to_info(arr)
    _autocorr_series_computation(res, xxz__pcs, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xxz__pcs)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    xxz__pcs = array_to_info(arr)
    _compute_series_monotonicity(res, xxz__pcs, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xxz__pcs)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    ihp__kcn = res[0] > 0.5
    return ihp__kcn


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        rbbf__cgv = '-'
        pico__jhtr = 'index_arr[0] > threshhold_date'
        frmz__mem = '1, n+1'
        vkhtb__asea = 'index_arr[-i] <= threshhold_date'
        fioa__afx = 'i - 1'
    else:
        rbbf__cgv = '+'
        pico__jhtr = 'index_arr[-1] < threshhold_date'
        frmz__mem = 'n'
        vkhtb__asea = 'index_arr[i] >= threshhold_date'
        fioa__afx = 'i'
    qnlwk__knzn = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        qnlwk__knzn += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_tz_naive_type):\n'
            )
        qnlwk__knzn += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            qnlwk__knzn += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            qnlwk__knzn += """      threshhold_date = initial_date - date_offset.base + date_offset
"""
            qnlwk__knzn += '    else:\n'
            qnlwk__knzn += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            qnlwk__knzn += (
                f'    threshhold_date = initial_date {rbbf__cgv} date_offset\n'
                )
    else:
        qnlwk__knzn += f'  threshhold_date = initial_date {rbbf__cgv} offset\n'
    qnlwk__knzn += '  local_valid = 0\n'
    qnlwk__knzn += f'  n = len(index_arr)\n'
    qnlwk__knzn += f'  if n:\n'
    qnlwk__knzn += f'    if {pico__jhtr}:\n'
    qnlwk__knzn += '      loc_valid = n\n'
    qnlwk__knzn += '    else:\n'
    qnlwk__knzn += f'      for i in range({frmz__mem}):\n'
    qnlwk__knzn += f'        if {vkhtb__asea}:\n'
    qnlwk__knzn += f'          loc_valid = {fioa__afx}\n'
    qnlwk__knzn += '          break\n'
    qnlwk__knzn += '  if is_parallel:\n'
    qnlwk__knzn += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    qnlwk__knzn += '    return total_valid\n'
    qnlwk__knzn += '  else:\n'
    qnlwk__knzn += '    return loc_valid\n'
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, rdewt__vpud)
    return rdewt__vpud['impl']


def quantile(A, q):
    pass


def quantile_parallel(A, q):
    pass


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, FloatingArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    qggn__xult = numba_to_c_type(sig.args[0].dtype)
    qtp__agyv = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), qggn__xult))
    ycwo__qbu = args[0]
    foutk__xnu = sig.args[0]
    if isinstance(foutk__xnu, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        ycwo__qbu = cgutils.create_struct_proxy(foutk__xnu)(context,
            builder, ycwo__qbu).data
        foutk__xnu = types.Array(foutk__xnu.dtype, 1, 'C')
    assert foutk__xnu.ndim == 1
    arr = make_array(foutk__xnu)(context, builder, ycwo__qbu)
    mwsh__gxpq = builder.extract_value(arr.shape, 0)
    moq__gti = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        mwsh__gxpq, args[1], builder.load(qtp__agyv)]
    qwlwv__afh = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    nfz__gbmt = lir.FunctionType(lir.DoubleType(), qwlwv__afh)
    guxig__zgb = cgutils.get_or_insert_function(builder.module, nfz__gbmt,
        name='quantile_sequential')
    fif__zpiv = builder.call(guxig__zgb, moq__gti)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return fif__zpiv


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, FloatingArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    qggn__xult = numba_to_c_type(sig.args[0].dtype)
    qtp__agyv = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), qggn__xult))
    ycwo__qbu = args[0]
    foutk__xnu = sig.args[0]
    if isinstance(foutk__xnu, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        ycwo__qbu = cgutils.create_struct_proxy(foutk__xnu)(context,
            builder, ycwo__qbu).data
        foutk__xnu = types.Array(foutk__xnu.dtype, 1, 'C')
    assert foutk__xnu.ndim == 1
    arr = make_array(foutk__xnu)(context, builder, ycwo__qbu)
    mwsh__gxpq = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        svec__oyw = args[2]
    else:
        svec__oyw = mwsh__gxpq
    moq__gti = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        mwsh__gxpq, svec__oyw, args[1], builder.load(qtp__agyv)]
    qwlwv__afh = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType
        (64), lir.DoubleType(), lir.IntType(32)]
    nfz__gbmt = lir.FunctionType(lir.DoubleType(), qwlwv__afh)
    guxig__zgb = cgutils.get_or_insert_function(builder.module, nfz__gbmt,
        name='quantile_parallel')
    fif__zpiv = builder.call(guxig__zgb, moq__gti)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return fif__zpiv


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        n = len(arr)
        qil__guyd = bodo.utils.utils.alloc_type(n, np.bool_, (-1,))
        qil__guyd[0] = True
        gsg__hozf = pd.isna(arr)
        for i in range(1, len(arr)):
            if gsg__hozf[i] and gsg__hozf[i - 1]:
                qil__guyd[i] = False
            elif gsg__hozf[i] or gsg__hozf[i - 1]:
                qil__guyd[i] = True
            else:
                qil__guyd[i] = arr[i] != arr[i - 1]
        return qil__guyd
    return impl


def rank(arr, method='average', na_option='keep', ascending=True, pct=False):
    pass


@overload(rank, no_unliteral=True, inline='always')
def overload_rank(arr, method='average', na_option='keep', ascending=True,
    pct=False):
    if not is_overload_constant_str(method):
        raise_bodo_error(
            "Series.rank(): 'method' argument must be a constant string")
    method = get_overload_const_str(method)
    if not is_overload_constant_str(na_option):
        raise_bodo_error(
            "Series.rank(): 'na_option' argument must be a constant string")
    na_option = get_overload_const_str(na_option)
    if not is_overload_constant_bool(ascending):
        raise_bodo_error(
            "Series.rank(): 'ascending' argument must be a constant boolean")
    ascending = get_overload_const_bool(ascending)
    if not is_overload_constant_bool(pct):
        raise_bodo_error(
            "Series.rank(): 'pct' argument must be a constant boolean")
    pct = get_overload_const_bool(pct)
    if method == 'first' and not ascending:
        raise BodoError(
            "Series.rank(): method='first' with ascending=False is currently unsupported."
            )
    qnlwk__knzn = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    qnlwk__knzn += '  na_idxs = pd.isna(arr)\n'
    qnlwk__knzn += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    qnlwk__knzn += '  nas = sum(na_idxs)\n'
    if not ascending:
        qnlwk__knzn += '  if nas and nas < (sorter.size - 1):\n'
        qnlwk__knzn += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        qnlwk__knzn += '  else:\n'
        qnlwk__knzn += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        qnlwk__knzn += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    qnlwk__knzn += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    qnlwk__knzn += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        qnlwk__knzn += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        qnlwk__knzn += '    inv,\n'
        qnlwk__knzn += '    new_dtype=np.float64,\n'
        qnlwk__knzn += '    copy=True,\n'
        qnlwk__knzn += '    nan_to_str=False,\n'
        qnlwk__knzn += '    from_series=True,\n'
        qnlwk__knzn += '    ) + 1\n'
    else:
        qnlwk__knzn += '  arr = arr[sorter]\n'
        qnlwk__knzn += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n')
        qnlwk__knzn += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            qnlwk__knzn += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            qnlwk__knzn += '    dense,\n'
            qnlwk__knzn += '    new_dtype=np.float64,\n'
            qnlwk__knzn += '    copy=True,\n'
            qnlwk__knzn += '    nan_to_str=False,\n'
            qnlwk__knzn += '    from_series=True,\n'
            qnlwk__knzn += '  )\n'
        else:
            qnlwk__knzn += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            qnlwk__knzn += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                qnlwk__knzn += '  ret = count_float[dense]\n'
            elif method == 'min':
                qnlwk__knzn += '  ret = count_float[dense - 1] + 1\n'
            else:
                qnlwk__knzn += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                qnlwk__knzn += '  ret[na_idxs] = -1\n'
            qnlwk__knzn += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            qnlwk__knzn += '  div_val = arr.size - nas\n'
        else:
            qnlwk__knzn += '  div_val = arr.size\n'
        qnlwk__knzn += '  for i in range(len(ret)):\n'
        qnlwk__knzn += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        qnlwk__knzn += '  ret[na_idxs] = np.nan\n'
    qnlwk__knzn += '  return ret\n'
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'np': np, 'pd': pd, 'bodo': bodo}, rdewt__vpud)
    return rdewt__vpud['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    dkvj__dtf = start
    angmh__nzwgr = 2 * start + 1
    fyge__zpxjy = 2 * start + 2
    if angmh__nzwgr < n and not cmp_f(arr[angmh__nzwgr], arr[dkvj__dtf]):
        dkvj__dtf = angmh__nzwgr
    if fyge__zpxjy < n and not cmp_f(arr[fyge__zpxjy], arr[dkvj__dtf]):
        dkvj__dtf = fyge__zpxjy
    if dkvj__dtf != start:
        arr[start], arr[dkvj__dtf] = arr[dkvj__dtf], arr[start]
        ind_arr[start], ind_arr[dkvj__dtf] = ind_arr[dkvj__dtf], ind_arr[start]
        min_heapify(arr, ind_arr, n, dkvj__dtf, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        bra__mpymj = np.empty(k, A.dtype)
        klh__sbg = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                bra__mpymj[ind] = A[i]
                klh__sbg[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            bra__mpymj = bra__mpymj[:ind]
            klh__sbg = klh__sbg[:ind]
        return bra__mpymj, klh__sbg, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        ythj__klx = np.sort(A)
        cdjq__owd = index_arr[np.argsort(A)]
        cuy__rwl = pd.Series(ythj__klx).notna().values
        ythj__klx = ythj__klx[cuy__rwl]
        cdjq__owd = cdjq__owd[cuy__rwl]
        if is_largest:
            ythj__klx = ythj__klx[::-1]
            cdjq__owd = cdjq__owd[::-1]
        return np.ascontiguousarray(ythj__klx), np.ascontiguousarray(cdjq__owd)
    bra__mpymj, klh__sbg, start = select_k_nonan(A, index_arr, m, k)
    klh__sbg = klh__sbg[bra__mpymj.argsort()]
    bra__mpymj.sort()
    if not is_largest:
        bra__mpymj = np.ascontiguousarray(bra__mpymj[::-1])
        klh__sbg = np.ascontiguousarray(klh__sbg[::-1])
    for i in range(start, m):
        if cmp_f(A[i], bra__mpymj[0]):
            bra__mpymj[0] = A[i]
            klh__sbg[0] = index_arr[i]
            min_heapify(bra__mpymj, klh__sbg, k, 0, cmp_f)
    klh__sbg = klh__sbg[bra__mpymj.argsort()]
    bra__mpymj.sort()
    if is_largest:
        bra__mpymj = bra__mpymj[::-1]
        klh__sbg = klh__sbg[::-1]
    return np.ascontiguousarray(bra__mpymj), np.ascontiguousarray(klh__sbg)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    uaqci__fzf = bodo.libs.distributed_api.get_rank()
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    mfx__lovcn, kvium__pjjri = nlargest(A, I, k, is_largest, cmp_f)
    osus__zba = bodo.libs.distributed_api.gatherv(mfx__lovcn)
    jvm__sds = bodo.libs.distributed_api.gatherv(kvium__pjjri)
    if uaqci__fzf == MPI_ROOT:
        res, mhahk__htf = nlargest(osus__zba, jvm__sds, k, is_largest, cmp_f)
    else:
        res = np.empty(k, A.dtype)
        mhahk__htf = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(mhahk__htf)
    return res, mhahk__htf


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    fmtre__oeat, xaxos__pioo = mat.shape
    gboz__cwtj = np.empty((xaxos__pioo, xaxos__pioo), dtype=np.float64)
    for wzid__xqr in range(xaxos__pioo):
        for llyr__cbxwq in range(wzid__xqr + 1):
            vanqf__iav = 0
            featv__mrcif = bdp__rytd = emg__uybz = lslc__cwft = 0.0
            for i in range(fmtre__oeat):
                if np.isfinite(mat[i, wzid__xqr]) and np.isfinite(mat[i,
                    llyr__cbxwq]):
                    pcwx__vjxrt = mat[i, wzid__xqr]
                    lwm__otqe = mat[i, llyr__cbxwq]
                    vanqf__iav += 1
                    emg__uybz += pcwx__vjxrt
                    lslc__cwft += lwm__otqe
            if parallel:
                vanqf__iav = bodo.libs.distributed_api.dist_reduce(vanqf__iav,
                    sum_op)
                emg__uybz = bodo.libs.distributed_api.dist_reduce(emg__uybz,
                    sum_op)
                lslc__cwft = bodo.libs.distributed_api.dist_reduce(lslc__cwft,
                    sum_op)
            if vanqf__iav < minpv:
                gboz__cwtj[wzid__xqr, llyr__cbxwq] = gboz__cwtj[llyr__cbxwq,
                    wzid__xqr] = np.nan
            else:
                xaur__aix = emg__uybz / vanqf__iav
                aseba__hpmf = lslc__cwft / vanqf__iav
                emg__uybz = 0.0
                for i in range(fmtre__oeat):
                    if np.isfinite(mat[i, wzid__xqr]) and np.isfinite(mat[i,
                        llyr__cbxwq]):
                        pcwx__vjxrt = mat[i, wzid__xqr] - xaur__aix
                        lwm__otqe = mat[i, llyr__cbxwq] - aseba__hpmf
                        emg__uybz += pcwx__vjxrt * lwm__otqe
                        featv__mrcif += pcwx__vjxrt * pcwx__vjxrt
                        bdp__rytd += lwm__otqe * lwm__otqe
                if parallel:
                    emg__uybz = bodo.libs.distributed_api.dist_reduce(emg__uybz
                        , sum_op)
                    featv__mrcif = bodo.libs.distributed_api.dist_reduce(
                        featv__mrcif, sum_op)
                    bdp__rytd = bodo.libs.distributed_api.dist_reduce(bdp__rytd
                        , sum_op)
                wrxcy__efd = vanqf__iav - 1.0 if cov else sqrt(featv__mrcif *
                    bdp__rytd)
                if wrxcy__efd != 0.0:
                    gboz__cwtj[wzid__xqr, llyr__cbxwq] = gboz__cwtj[
                        llyr__cbxwq, wzid__xqr] = emg__uybz / wrxcy__efd
                else:
                    gboz__cwtj[wzid__xqr, llyr__cbxwq] = gboz__cwtj[
                        llyr__cbxwq, wzid__xqr] = np.nan
    return gboz__cwtj


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    cpxhd__tqqa = n != 1
    qnlwk__knzn = 'def impl(data, parallel=False):\n'
    qnlwk__knzn += '  if parallel:\n'
    zbi__cdtk = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    qnlwk__knzn += f'    cpp_table = arr_info_list_to_table([{zbi__cdtk}])\n'
    qnlwk__knzn += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    cnqfv__niw = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    qnlwk__knzn += f'    data = ({cnqfv__niw},)\n'
    qnlwk__knzn += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    qnlwk__knzn += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    qnlwk__knzn += '    bodo.libs.array.delete_table(cpp_table)\n'
    qnlwk__knzn += '  n = len(data[0])\n'
    qnlwk__knzn += '  out = np.empty(n, np.bool_)\n'
    qnlwk__knzn += '  uniqs = dict()\n'
    if cpxhd__tqqa:
        qnlwk__knzn += '  for i in range(n):\n'
        esgzh__tyeo = ', '.join(f'data[{i}][i]' for i in range(n))
        zqcz__qixgg = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        qnlwk__knzn += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({esgzh__tyeo},), ({zqcz__qixgg},))
"""
        qnlwk__knzn += '    if val in uniqs:\n'
        qnlwk__knzn += '      out[i] = True\n'
        qnlwk__knzn += '    else:\n'
        qnlwk__knzn += '      out[i] = False\n'
        qnlwk__knzn += '      uniqs[val] = 0\n'
    else:
        qnlwk__knzn += '  data = data[0]\n'
        qnlwk__knzn += '  hasna = False\n'
        qnlwk__knzn += '  for i in range(n):\n'
        qnlwk__knzn += '    if bodo.libs.array_kernels.isna(data, i):\n'
        qnlwk__knzn += '      out[i] = hasna\n'
        qnlwk__knzn += '      hasna = True\n'
        qnlwk__knzn += '    else:\n'
        qnlwk__knzn += '      val = data[i]\n'
        qnlwk__knzn += '      if val in uniqs:\n'
        qnlwk__knzn += '        out[i] = True\n'
        qnlwk__knzn += '      else:\n'
        qnlwk__knzn += '        out[i] = False\n'
        qnlwk__knzn += '        uniqs[val] = 0\n'
    qnlwk__knzn += '  if parallel:\n'
    qnlwk__knzn += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    qnlwk__knzn += '  return out\n'
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        rdewt__vpud)
    impl = rdewt__vpud['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    pass


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    yvwm__rkys = len(data)
    qnlwk__knzn = (
        'def impl(data, ind_arr, n, frac, replace, parallel=False):\n')
    qnlwk__knzn += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        yvwm__rkys)))
    qnlwk__knzn += '  table_total = arr_info_list_to_table(info_list_total)\n'
    qnlwk__knzn += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(yvwm__rkys))
    for czx__phk in range(yvwm__rkys):
        qnlwk__knzn += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(czx__phk, czx__phk, czx__phk))
    qnlwk__knzn += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(yvwm__rkys))
    qnlwk__knzn += '  delete_table(out_table)\n'
    qnlwk__knzn += '  delete_table(table_total)\n'
    qnlwk__knzn += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(yvwm__rkys)))
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, rdewt__vpud)
    impl = rdewt__vpud['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    pass


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    yvwm__rkys = len(data)
    qnlwk__knzn = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    qnlwk__knzn += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        yvwm__rkys)))
    qnlwk__knzn += '  table_total = arr_info_list_to_table(info_list_total)\n'
    qnlwk__knzn += '  keep_i = 0\n'
    qnlwk__knzn += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for czx__phk in range(yvwm__rkys):
        qnlwk__knzn += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(czx__phk, czx__phk, czx__phk))
    qnlwk__knzn += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(yvwm__rkys))
    qnlwk__knzn += '  delete_table(out_table)\n'
    qnlwk__knzn += '  delete_table(table_total)\n'
    qnlwk__knzn += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(yvwm__rkys)))
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, rdewt__vpud)
    impl = rdewt__vpud['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    pass


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        yfrx__xdb = [array_to_info(data_arr)]
        dnco__byy = arr_info_list_to_table(yfrx__xdb)
        oqgb__mrpw = 0
        kgr__ashc = drop_duplicates_table(dnco__byy, parallel, 1,
            oqgb__mrpw, False, True)
        out_arr = info_to_array(info_from_table(kgr__ashc, 0), data_arr)
        delete_table(kgr__ashc)
        delete_table(dnco__byy)
        return out_arr
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    pass


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    claxn__xswxk = len(data.types)
    pcg__tvyo = [('out' + str(i)) for i in range(claxn__xswxk)]
    wibr__pka = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    myd__dyddh = ['isna(data[{}], i)'.format(i) for i in wibr__pka]
    fwf__ktmoz = 'not ({})'.format(' or '.join(myd__dyddh))
    if not is_overload_none(thresh):
        fwf__ktmoz = '(({}) <= ({}) - thresh)'.format(' + '.join(myd__dyddh
            ), claxn__xswxk - 1)
    elif how == 'all':
        fwf__ktmoz = 'not ({})'.format(' and '.join(myd__dyddh))
    qnlwk__knzn = 'def _dropna_imp(data, how, thresh, subset):\n'
    qnlwk__knzn += '  old_len = len(data[0])\n'
    qnlwk__knzn += '  new_len = 0\n'
    qnlwk__knzn += '  for i in range(old_len):\n'
    qnlwk__knzn += '    if {}:\n'.format(fwf__ktmoz)
    qnlwk__knzn += '      new_len += 1\n'
    for i, out in enumerate(pcg__tvyo):
        if isinstance(data[i], bodo.CategoricalArrayType):
            qnlwk__knzn += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            qnlwk__knzn += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    qnlwk__knzn += '  curr_ind = 0\n'
    qnlwk__knzn += '  for i in range(old_len):\n'
    qnlwk__knzn += '    if {}:\n'.format(fwf__ktmoz)
    for i in range(claxn__xswxk):
        qnlwk__knzn += '      if isna(data[{}], i):\n'.format(i)
        qnlwk__knzn += '        setna({}, curr_ind)\n'.format(pcg__tvyo[i])
        qnlwk__knzn += '      else:\n'
        qnlwk__knzn += '        {}[curr_ind] = data[{}][i]\n'.format(pcg__tvyo
            [i], i)
    qnlwk__knzn += '      curr_ind += 1\n'
    qnlwk__knzn += '  return {}\n'.format(', '.join(pcg__tvyo))
    rdewt__vpud = {}
    ffg__izuwc = {'t{}'.format(i): zpq__hgg for i, zpq__hgg in enumerate(
        data.types)}
    ffg__izuwc.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(qnlwk__knzn, ffg__izuwc, rdewt__vpud)
    cehh__umim = rdewt__vpud['_dropna_imp']
    return cehh__umim


def get(arr, ind):
    pass


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        foutk__xnu = arr.dtype
        ltk__dme = foutk__xnu.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            hovq__pgy = init_nested_counts(ltk__dme)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                hovq__pgy = add_nested_counts(hovq__pgy, val[ind])
            out_arr = bodo.utils.utils.alloc_type(n, foutk__xnu, hovq__pgy)
            for uhxxl__mhsj in range(n):
                if bodo.libs.array_kernels.isna(arr, uhxxl__mhsj):
                    setna(out_arr, uhxxl__mhsj)
                    continue
                val = arr[uhxxl__mhsj]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(out_arr, uhxxl__mhsj)
                    continue
                out_arr[uhxxl__mhsj] = val[ind]
            return out_arr
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    hyhp__sgi = _to_readonly(arr_types.types[0])
    return all(isinstance(zpq__hgg, CategoricalArrayType) and _to_readonly(
        zpq__hgg) == hyhp__sgi for zpq__hgg in arr_types.types)


def concat(arr_list):
    pass


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        hslzm__spad = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            peaz__rgr = 0
            qii__womw = []
            for A in arr_list:
                xae__zvvn = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                qii__womw.append(bodo.libs.array_item_arr_ext.get_data(A))
                peaz__rgr += xae__zvvn
            scdi__mpj = np.empty(peaz__rgr + 1, offset_type)
            lgeky__obujs = bodo.libs.array_kernels.concat(qii__womw)
            pjteo__znold = np.empty(peaz__rgr + 7 >> 3, np.uint8)
            jbgmp__jbanw = 0
            fpxip__wdc = 0
            for A in arr_list:
                ziofs__wfgqs = bodo.libs.array_item_arr_ext.get_offsets(A)
                hpkcq__bfhc = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                xae__zvvn = len(A)
                gik__jrx = ziofs__wfgqs[xae__zvvn]
                for i in range(xae__zvvn):
                    scdi__mpj[i + jbgmp__jbanw] = ziofs__wfgqs[i] + fpxip__wdc
                    afq__tfey = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        hpkcq__bfhc, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(pjteo__znold, i +
                        jbgmp__jbanw, afq__tfey)
                jbgmp__jbanw += xae__zvvn
                fpxip__wdc += gik__jrx
            scdi__mpj[jbgmp__jbanw] = fpxip__wdc
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                peaz__rgr, lgeky__obujs, scdi__mpj, pjteo__znold)
            return out_arr
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        hxdf__pxayw = arr_list.dtype.names
        qnlwk__knzn = 'def struct_array_concat_impl(arr_list):\n'
        qnlwk__knzn += f'    n_all = 0\n'
        for i in range(len(hxdf__pxayw)):
            qnlwk__knzn += f'    concat_list{i} = []\n'
        qnlwk__knzn += '    for A in arr_list:\n'
        qnlwk__knzn += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(hxdf__pxayw)):
            qnlwk__knzn += f'        concat_list{i}.append(data_tuple[{i}])\n'
        qnlwk__knzn += '        n_all += len(A)\n'
        qnlwk__knzn += '    n_bytes = (n_all + 7) >> 3\n'
        qnlwk__knzn += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        qnlwk__knzn += '    curr_bit = 0\n'
        qnlwk__knzn += '    for A in arr_list:\n'
        qnlwk__knzn += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        qnlwk__knzn += '        for j in range(len(A)):\n'
        qnlwk__knzn += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        qnlwk__knzn += """            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)
"""
        qnlwk__knzn += '            curr_bit += 1\n'
        qnlwk__knzn += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        gls__gek = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(hxdf__pxayw))])
        qnlwk__knzn += f'        ({gls__gek},),\n'
        qnlwk__knzn += '        new_mask,\n'
        qnlwk__knzn += f'        {hxdf__pxayw},\n'
        qnlwk__knzn += '    )\n'
        rdewt__vpud = {}
        exec(qnlwk__knzn, {'bodo': bodo, 'np': np}, rdewt__vpud)
        return rdewt__vpud['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.DatetimeArrayType):
        qjom__uyqly = arr_list.dtype.tz

        def tz_aware_concat_impl(arr_list):
            kmtm__ffzn = 0
            for A in arr_list:
                kmtm__ffzn += len(A)
            rrsbv__lht = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(
                kmtm__ffzn, qjom__uyqly)
            pnzoy__izyv = 0
            for A in arr_list:
                for i in range(len(A)):
                    rrsbv__lht[i + pnzoy__izyv] = A[i]
                pnzoy__izyv += len(A)
            return rrsbv__lht
        return tz_aware_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            kmtm__ffzn = 0
            for A in arr_list:
                kmtm__ffzn += len(A)
            rrsbv__lht = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(kmtm__ffzn))
            pnzoy__izyv = 0
            for A in arr_list:
                for i in range(len(A)):
                    rrsbv__lht._data[i + pnzoy__izyv] = A._data[i]
                    afq__tfey = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(rrsbv__lht.
                        _null_bitmap, i + pnzoy__izyv, afq__tfey)
                pnzoy__izyv += len(A)
            return rrsbv__lht
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            kmtm__ffzn = 0
            for A in arr_list:
                kmtm__ffzn += len(A)
            rrsbv__lht = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(kmtm__ffzn))
            pnzoy__izyv = 0
            for A in arr_list:
                for i in range(len(A)):
                    rrsbv__lht._days_data[i + pnzoy__izyv] = A._days_data[i]
                    rrsbv__lht._seconds_data[i + pnzoy__izyv
                        ] = A._seconds_data[i]
                    rrsbv__lht._microseconds_data[i + pnzoy__izyv
                        ] = A._microseconds_data[i]
                    afq__tfey = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(rrsbv__lht.
                        _null_bitmap, i + pnzoy__izyv, afq__tfey)
                pnzoy__izyv += len(A)
            return rrsbv__lht
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        ghog__zvlp = arr_list.dtype.precision
        ixv__vxzny = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            kmtm__ffzn = 0
            for A in arr_list:
                kmtm__ffzn += len(A)
            rrsbv__lht = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                kmtm__ffzn, ghog__zvlp, ixv__vxzny)
            pnzoy__izyv = 0
            for A in arr_list:
                for i in range(len(A)):
                    rrsbv__lht._data[i + pnzoy__izyv] = A._data[i]
                    afq__tfey = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(rrsbv__lht.
                        _null_bitmap, i + pnzoy__izyv, afq__tfey)
                pnzoy__izyv += len(A)
            return rrsbv__lht
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        zpq__hgg) for zpq__hgg in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            oooda__mlbu = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    oooda__mlbu = arr_list.types[i]
                    break
        else:
            oooda__mlbu = arr_list.dtype
        if oooda__mlbu == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                tlf__ttfel = 0
                pywcp__hzekw = 0
                vxhl__vity = 0
                for A in arr_list:
                    data_arr = A._data
                    amgu__tejnx = A._indices
                    vxhl__vity += len(amgu__tejnx)
                    tlf__ttfel += len(data_arr)
                    pywcp__hzekw += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                thubo__jnhza = pre_alloc_string_array(tlf__ttfel, pywcp__hzekw)
                ivh__nss = bodo.libs.int_arr_ext.alloc_int_array(vxhl__vity,
                    np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(thubo__jnhza, -1)
                vutxy__wmha = 0
                xil__gavzt = 0
                nqeo__lfrsa = 0
                for A in arr_list:
                    data_arr = A._data
                    amgu__tejnx = A._indices
                    vxhl__vity = len(amgu__tejnx)
                    bodo.libs.str_arr_ext.set_string_array_range(thubo__jnhza,
                        data_arr, vutxy__wmha, xil__gavzt)
                    for i in range(vxhl__vity):
                        if bodo.libs.array_kernels.isna(amgu__tejnx, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            amgu__tejnx[i]):
                            bodo.libs.array_kernels.setna(ivh__nss, 
                                nqeo__lfrsa + i)
                        else:
                            ivh__nss[nqeo__lfrsa + i
                                ] = vutxy__wmha + amgu__tejnx[i]
                    vutxy__wmha += len(data_arr)
                    xil__gavzt += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                    nqeo__lfrsa += vxhl__vity
                out_arr = init_dict_arr(thubo__jnhza, ivh__nss, False, False)
                crclb__vwdh = drop_duplicates_local_dictionary(out_arr, False)
                return crclb__vwdh
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            tlf__ttfel = 0
            pywcp__hzekw = 0
            for A in arr_list:
                arr = A
                tlf__ttfel += len(arr)
                pywcp__hzekw += bodo.libs.str_arr_ext.num_total_chars(arr)
            out_arr = bodo.utils.utils.alloc_type(tlf__ttfel, oooda__mlbu,
                (pywcp__hzekw,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)
            vutxy__wmha = 0
            xil__gavzt = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(out_arr, arr,
                    vutxy__wmha, xil__gavzt)
                vutxy__wmha += len(arr)
                xil__gavzt += bodo.libs.str_arr_ext.num_total_chars(arr)
            return out_arr
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(zpq__hgg.dtype, types.Integer) for
        zpq__hgg in arr_list.types) and any(isinstance(zpq__hgg,
        IntegerArrayType) for zpq__hgg in arr_list.types):

        def impl_int_arr_list(arr_list):
            nomsp__svkcb = convert_to_nullable_tup(arr_list)
            elgfy__yuxkl = []
            zzayt__jylo = 0
            for A in nomsp__svkcb:
                elgfy__yuxkl.append(A._data)
                zzayt__jylo += len(A)
            lgeky__obujs = bodo.libs.array_kernels.concat(elgfy__yuxkl)
            pem__rkc = zzayt__jylo + 7 >> 3
            pex__pdyy = np.empty(pem__rkc, np.uint8)
            qdyj__isr = 0
            for A in nomsp__svkcb:
                majl__dssnc = A._null_bitmap
                for uhxxl__mhsj in range(len(A)):
                    afq__tfey = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        majl__dssnc, uhxxl__mhsj)
                    bodo.libs.int_arr_ext.set_bit_to_arr(pex__pdyy,
                        qdyj__isr, afq__tfey)
                    qdyj__isr += 1
            return bodo.libs.int_arr_ext.init_integer_array(lgeky__obujs,
                pex__pdyy)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(zpq__hgg.dtype == types.bool_ for zpq__hgg in
        arr_list.types) and any(zpq__hgg == boolean_array for zpq__hgg in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            nomsp__svkcb = convert_to_nullable_tup(arr_list)
            elgfy__yuxkl = []
            zzayt__jylo = 0
            for A in nomsp__svkcb:
                elgfy__yuxkl.append(A._data)
                zzayt__jylo += len(A)
            lgeky__obujs = bodo.libs.array_kernels.concat(elgfy__yuxkl)
            pem__rkc = zzayt__jylo + 7 >> 3
            pex__pdyy = np.empty(pem__rkc, np.uint8)
            qdyj__isr = 0
            for A in nomsp__svkcb:
                majl__dssnc = A._null_bitmap
                for uhxxl__mhsj in range(len(A)):
                    afq__tfey = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        majl__dssnc, uhxxl__mhsj)
                    bodo.libs.int_arr_ext.set_bit_to_arr(pex__pdyy,
                        qdyj__isr, afq__tfey)
                    qdyj__isr += 1
            return bodo.libs.bool_arr_ext.init_bool_array(lgeky__obujs,
                pex__pdyy)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, FloatingArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(zpq__hgg.dtype, types.Float) for
        zpq__hgg in arr_list.types) and any(isinstance(zpq__hgg,
        FloatingArrayType) for zpq__hgg in arr_list.types):

        def impl_float_arr_list(arr_list):
            nomsp__svkcb = convert_to_nullable_tup(arr_list)
            elgfy__yuxkl = []
            zzayt__jylo = 0
            for A in nomsp__svkcb:
                elgfy__yuxkl.append(A._data)
                zzayt__jylo += len(A)
            lgeky__obujs = bodo.libs.array_kernels.concat(elgfy__yuxkl)
            pem__rkc = zzayt__jylo + 7 >> 3
            pex__pdyy = np.empty(pem__rkc, np.uint8)
            qdyj__isr = 0
            for A in nomsp__svkcb:
                majl__dssnc = A._null_bitmap
                for uhxxl__mhsj in range(len(A)):
                    afq__tfey = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        majl__dssnc, uhxxl__mhsj)
                    bodo.libs.int_arr_ext.set_bit_to_arr(pex__pdyy,
                        qdyj__isr, afq__tfey)
                    qdyj__isr += 1
            return bodo.libs.float_arr_ext.init_float_array(lgeky__obujs,
                pex__pdyy)
        return impl_float_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            ioyd__kfp = []
            for A in arr_list:
                ioyd__kfp.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                ioyd__kfp), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        cawlj__ijxs = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        qnlwk__knzn = 'def impl(arr_list):\n'
        qnlwk__knzn += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({cawlj__ijxs}, )), arr_list[0].dtype)
"""
        mqvnl__uze = {}
        exec(qnlwk__knzn, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, mqvnl__uze)
        return mqvnl__uze['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            zzayt__jylo = 0
            for A in arr_list:
                zzayt__jylo += len(A)
            out_arr = np.empty(zzayt__jylo, dtype)
            xulya__usglg = 0
            for A in arr_list:
                n = len(A)
                out_arr[xulya__usglg:xulya__usglg + n] = A
                xulya__usglg += n
            return out_arr
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(zpq__hgg, (
        types.Array, IntegerArrayType)) and isinstance(zpq__hgg.dtype,
        types.Integer) for zpq__hgg in arr_list.types) and any(isinstance(
        zpq__hgg, types.Array) and isinstance(zpq__hgg.dtype, types.Float) for
        zpq__hgg in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            yay__himq = []
            for A in arr_list:
                yay__himq.append(A._data)
            wot__shqeh = bodo.libs.array_kernels.concat(yay__himq)
            gboz__cwtj = bodo.libs.map_arr_ext.init_map_arr(wot__shqeh)
            return gboz__cwtj
        return impl_map_arr_list
    if isinstance(arr_list, types.Tuple):
        nfk__hwup = all([(isinstance(exx__mtv, bodo.DatetimeArrayType) or 
            isinstance(exx__mtv, types.Array) and exx__mtv.dtype == bodo.
            datetime64ns) for exx__mtv in arr_list.types])
        if nfk__hwup:
            raise BodoError(
                f'Cannot concatenate the rows of Timestamp data with different timezones. Found types: {arr_list}. Please use pd.Series.tz_convert(None) to remove Timezone information.'
                )
    for exx__mtv in arr_list:
        if not isinstance(exx__mtv, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(zpq__hgg.astype(np.float64) for zpq__hgg in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    yvwm__rkys = len(arr_tup.types)
    qnlwk__knzn = 'def f(arr_tup):\n'
    qnlwk__knzn += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        yvwm__rkys)), ',' if yvwm__rkys == 1 else '')
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'np': np}, rdewt__vpud)
    gmnya__gloai = rdewt__vpud['f']
    return gmnya__gloai


def convert_to_nullable_tup(arr_tup):
    pass


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, FloatingArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple
        ), 'convert_to_nullable_tup: tuple expected'
    yvwm__rkys = len(arr_tup.types)
    qmib__zub = find_common_np_dtype(arr_tup.types)
    ltk__dme = None
    xnij__nxklu = ''
    if isinstance(qmib__zub, types.Integer):
        ltk__dme = bodo.libs.int_arr_ext.IntDtype(qmib__zub)
        xnij__nxklu = '.astype(out_dtype, False)'
    if isinstance(qmib__zub, types.Float
        ) and bodo.libs.float_arr_ext._use_nullable_float:
        ltk__dme = bodo.libs.float_arr_ext.FloatDtype(qmib__zub)
        xnij__nxklu = '.astype(out_dtype, False)'
    qnlwk__knzn = 'def f(arr_tup):\n'
    qnlwk__knzn += '  return ({}{})\n'.format(','.join(
        f'bodo.utils.conversion.coerce_to_array(arr_tup[{i}], use_nullable_array=True){xnij__nxklu}'
         for i in range(yvwm__rkys)), ',' if yvwm__rkys == 1 else '')
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'bodo': bodo, 'out_dtype': ltk__dme}, rdewt__vpud)
    tfh__lmr = rdewt__vpud['f']
    return tfh__lmr


def nunique(A, dropna):
    pass


def nunique_parallel(A, dropna):
    pass


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, xomyk__sck = build_set_seen_na(A)
        return len(s) + int(not dropna and xomyk__sck)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        qcxt__aicrp = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        twdty__kkg = len(qcxt__aicrp)
        return bodo.libs.distributed_api.dist_reduce(twdty__kkg, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    pass


def accum_func(A, func_name, parallel=False):
    pass


@overload(accum_func, no_unliteral=True)
def accum_func_overload(A, func_name, parallel=False):
    assert is_overload_constant_str(func_name
        ), 'accum_func: func_name should be const'
    prf__bcff = get_overload_const_str(func_name)
    assert prf__bcff in ('cumsum', 'cumprod', 'cummin', 'cummax'
        ), 'accum_func: invalid func_name'
    if prf__bcff == 'cumsum':
        nzpj__omwyr = A.dtype(0)
        eqcg__oyft = np.int32(Reduce_Type.Sum.value)
        vbd__ilj = np.add
    if prf__bcff == 'cumprod':
        nzpj__omwyr = A.dtype(1)
        eqcg__oyft = np.int32(Reduce_Type.Prod.value)
        vbd__ilj = np.multiply
    if prf__bcff == 'cummin':
        if isinstance(A.dtype, types.Float):
            nzpj__omwyr = np.finfo(A.dtype(1).dtype).max
        else:
            nzpj__omwyr = np.iinfo(A.dtype(1).dtype).max
        eqcg__oyft = np.int32(Reduce_Type.Min.value)
        vbd__ilj = min
    if prf__bcff == 'cummax':
        if isinstance(A.dtype, types.Float):
            nzpj__omwyr = np.finfo(A.dtype(1).dtype).min
        else:
            nzpj__omwyr = np.iinfo(A.dtype(1).dtype).min
        eqcg__oyft = np.int32(Reduce_Type.Max.value)
        vbd__ilj = max
    tum__lxqjz = A

    def impl(A, func_name, parallel=False):
        n = len(A)
        afg__ikols = nzpj__omwyr
        if parallel:
            for i in range(n):
                if not bodo.libs.array_kernels.isna(A, i):
                    afg__ikols = vbd__ilj(afg__ikols, A[i])
            afg__ikols = bodo.libs.distributed_api.dist_exscan(afg__ikols,
                eqcg__oyft)
            if bodo.get_rank() == 0:
                afg__ikols = nzpj__omwyr
        out_arr = bodo.utils.utils.alloc_type(n, tum__lxqjz, (-1,))
        for i in range(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(out_arr, i)
                continue
            afg__ikols = vbd__ilj(afg__ikols, A[i])
            out_arr[i] = afg__ikols
        return out_arr
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        ltjgj__cjyc = arr_info_list_to_table([array_to_info(A)])
        kklyt__rft = 1
        oqgb__mrpw = 0
        kgr__ashc = drop_duplicates_table(ltjgj__cjyc, parallel, kklyt__rft,
            oqgb__mrpw, dropna, True)
        out_arr = info_to_array(info_from_table(kgr__ashc, 0), A)
        delete_table(ltjgj__cjyc)
        delete_table(kgr__ashc)
        return out_arr
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    hslzm__spad = bodo.utils.typing.to_nullable_type(arr.dtype)
    skvdj__emyr = index_arr
    bwgai__xkxdn = skvdj__emyr.dtype

    def impl(arr, index_arr):
        n = len(arr)
        hovq__pgy = init_nested_counts(hslzm__spad)
        czjq__jkdlb = init_nested_counts(bwgai__xkxdn)
        for i in range(n):
            yil__wuzv = index_arr[i]
            if isna(arr, i):
                hovq__pgy = (hovq__pgy[0] + 1,) + hovq__pgy[1:]
                czjq__jkdlb = add_nested_counts(czjq__jkdlb, yil__wuzv)
                continue
            xum__qqreq = arr[i]
            if len(xum__qqreq) == 0:
                hovq__pgy = (hovq__pgy[0] + 1,) + hovq__pgy[1:]
                czjq__jkdlb = add_nested_counts(czjq__jkdlb, yil__wuzv)
                continue
            hovq__pgy = add_nested_counts(hovq__pgy, xum__qqreq)
            for abq__fanax in range(len(xum__qqreq)):
                czjq__jkdlb = add_nested_counts(czjq__jkdlb, yil__wuzv)
        out_arr = bodo.utils.utils.alloc_type(hovq__pgy[0], hslzm__spad,
            hovq__pgy[1:])
        ngr__kfhz = bodo.utils.utils.alloc_type(hovq__pgy[0], skvdj__emyr,
            czjq__jkdlb)
        fpxip__wdc = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, fpxip__wdc)
                ngr__kfhz[fpxip__wdc] = index_arr[i]
                fpxip__wdc += 1
                continue
            xum__qqreq = arr[i]
            gik__jrx = len(xum__qqreq)
            if gik__jrx == 0:
                setna(out_arr, fpxip__wdc)
                ngr__kfhz[fpxip__wdc] = index_arr[i]
                fpxip__wdc += 1
                continue
            out_arr[fpxip__wdc:fpxip__wdc + gik__jrx] = xum__qqreq
            ngr__kfhz[fpxip__wdc:fpxip__wdc + gik__jrx] = index_arr[i]
            fpxip__wdc += gik__jrx
        return out_arr, ngr__kfhz
    return impl


def explode_no_index(arr):
    pass


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    hslzm__spad = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        hovq__pgy = init_nested_counts(hslzm__spad)
        for i in range(n):
            if isna(arr, i):
                hovq__pgy = (hovq__pgy[0] + 1,) + hovq__pgy[1:]
                zao__xkme = 1
            else:
                xum__qqreq = arr[i]
                sfy__kwjr = len(xum__qqreq)
                if sfy__kwjr == 0:
                    hovq__pgy = (hovq__pgy[0] + 1,) + hovq__pgy[1:]
                    zao__xkme = 1
                    continue
                else:
                    hovq__pgy = add_nested_counts(hovq__pgy, xum__qqreq)
                    zao__xkme = sfy__kwjr
            if counts[i] != zao__xkme:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        out_arr = bodo.utils.utils.alloc_type(hovq__pgy[0], hslzm__spad,
            hovq__pgy[1:])
        fpxip__wdc = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, fpxip__wdc)
                fpxip__wdc += 1
                continue
            xum__qqreq = arr[i]
            gik__jrx = len(xum__qqreq)
            if gik__jrx == 0:
                setna(out_arr, fpxip__wdc)
                fpxip__wdc += 1
                continue
            out_arr[fpxip__wdc:fpxip__wdc + gik__jrx] = xum__qqreq
            fpxip__wdc += gik__jrx
        return out_arr
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    pass


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one or is_bin_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        vloq__uqe = 'np.empty(n, np.int64)'
        oqxar__qjtsd = 'out_arr[i] = 1'
        rzx__ijy = 'max(len(arr[i]), 1)'
    else:
        vloq__uqe = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        oqxar__qjtsd = 'bodo.libs.array_kernels.setna(out_arr, i)'
        rzx__ijy = 'len(arr[i])'
    qnlwk__knzn = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {vloq__uqe}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {oqxar__qjtsd}
        else:
            out_arr[i] = {rzx__ijy}
    return out_arr
    """
    rdewt__vpud = {}
    exec(qnlwk__knzn, {'bodo': bodo, 'numba': numba, 'np': np}, rdewt__vpud)
    impl = rdewt__vpud['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    pass


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    skvdj__emyr = index_arr
    bwgai__xkxdn = skvdj__emyr.dtype

    def impl(arr, pat, n, index_arr):
        bsku__wsp = pat is not None and len(pat) > 1
        if bsku__wsp:
            rwvdd__nzux = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        kdi__xbis = len(arr)
        tlf__ttfel = 0
        pywcp__hzekw = 0
        czjq__jkdlb = init_nested_counts(bwgai__xkxdn)
        for i in range(kdi__xbis):
            yil__wuzv = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                tlf__ttfel += 1
                czjq__jkdlb = add_nested_counts(czjq__jkdlb, yil__wuzv)
                continue
            if bsku__wsp:
                tcfj__eft = rwvdd__nzux.split(arr[i], maxsplit=n)
            else:
                tcfj__eft = arr[i].split(pat, n)
            tlf__ttfel += len(tcfj__eft)
            for s in tcfj__eft:
                czjq__jkdlb = add_nested_counts(czjq__jkdlb, yil__wuzv)
                pywcp__hzekw += bodo.libs.str_arr_ext.get_utf8_size(s)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tlf__ttfel,
            pywcp__hzekw)
        ngr__kfhz = bodo.utils.utils.alloc_type(tlf__ttfel, skvdj__emyr,
            czjq__jkdlb)
        zoqcy__dmbqb = 0
        for uhxxl__mhsj in range(kdi__xbis):
            if isna(arr, uhxxl__mhsj):
                out_arr[zoqcy__dmbqb] = ''
                bodo.libs.array_kernels.setna(out_arr, zoqcy__dmbqb)
                ngr__kfhz[zoqcy__dmbqb] = index_arr[uhxxl__mhsj]
                zoqcy__dmbqb += 1
                continue
            if bsku__wsp:
                tcfj__eft = rwvdd__nzux.split(arr[uhxxl__mhsj], maxsplit=n)
            else:
                tcfj__eft = arr[uhxxl__mhsj].split(pat, n)
            hhj__bno = len(tcfj__eft)
            out_arr[zoqcy__dmbqb:zoqcy__dmbqb + hhj__bno] = tcfj__eft
            ngr__kfhz[zoqcy__dmbqb:zoqcy__dmbqb + hhj__bno] = index_arr[
                uhxxl__mhsj]
            zoqcy__dmbqb += hhj__bno
        return out_arr, ngr__kfhz
    return impl


def gen_na_array(n, arr):
    pass


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr, use_dict_arr=False):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if not isinstance(arr, (FloatingArrayType, IntegerArrayType)
        ) and isinstance(dtype, (types.Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr, use_dict_arr=False):
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                out_arr[i] = np.nan
            return out_arr
        return impl_float
    if arr == bodo.dict_str_arr_type and is_overload_true(use_dict_arr):

        def impl_dict(n, arr, use_dict_arr=False):
            wmiw__xvn = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            gbxl__ctzdx = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(gbxl__ctzdx, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(wmiw__xvn,
                gbxl__ctzdx, True, True)
        return impl_dict
    tozxa__tqhsh = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        out_arr = bodo.utils.utils.alloc_type(n, tozxa__tqhsh, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(out_arr, i)
        return out_arr
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    pass


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.resize_and_copy()')
    ijlc__angva = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            out_arr = bodo.utils.utils.alloc_type(new_len, ijlc__angva)
            bodo.libs.str_arr_ext.str_copy_ptr(out_arr.ctypes, 0, A.ctypes,
                old_size)
            return out_arr
        return impl_char

    def impl(A, old_size, new_len):
        out_arr = bodo.utils.utils.alloc_type(new_len, ijlc__angva, (-1,))
        out_arr[:old_size] = A[:old_size]
        return out_arr
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    rndqu__yre = math.ceil((stop - start) / step)
    return int(max(rndqu__yre, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(ulrjc__iae, types.Complex) for ulrjc__iae in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            kxxm__eatow = (stop - start) / step
            rndqu__yre = math.ceil(kxxm__eatow.real)
            naueb__krwrh = math.ceil(kxxm__eatow.imag)
            ouyx__zfu = int(max(min(naueb__krwrh, rndqu__yre), 0))
            arr = np.empty(ouyx__zfu, dtype)
            for i in numba.parfors.parfor.internal_prange(ouyx__zfu):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            ouyx__zfu = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(ouyx__zfu, dtype)
            for i in numba.parfors.parfor.internal_prange(ouyx__zfu):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    pass


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        fmmp__dtfk = arr,
        if not inplace:
            fmmp__dtfk = arr.copy(),
        mzd__qabvw = bodo.libs.str_arr_ext.to_list_if_immutable_arr(fmmp__dtfk)
        afft__rvbwi = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True
            )
        bodo.libs.timsort.sort(mzd__qabvw, 0, n, afft__rvbwi)
        if not ascending:
            bodo.libs.timsort.reverseRange(mzd__qabvw, 0, n, afft__rvbwi)
        bodo.libs.str_arr_ext.cp_str_list_to_array(fmmp__dtfk, mzd__qabvw)
        return fmmp__dtfk[0]
    return impl


def overload_array_max(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    pass


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.nonzero()')
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            offset = bodo.libs.distributed_api.dist_exscan(n, Reduce_Type.
                Sum.value)
        else:
            offset = 0
        gboz__cwtj = []
        for i in range(n):
            if A[i]:
                gboz__cwtj.append(i + offset)
        return np.array(gboz__cwtj, np.int64),
    return impl


def ffill_bfill_arr(arr):
    pass


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    ijlc__angva = element_type(A)
    if ijlc__angva == types.unicode_type:
        null_value = '""'
    elif ijlc__angva == types.bool_:
        null_value = 'False'
    elif ijlc__angva == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_datetime(0))'
            )
    elif ijlc__angva == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_timedelta(0))'
            )
    else:
        null_value = '0'
    zoqcy__dmbqb = 'i'
    comw__gzyrn = False
    rfh__wrzlm = get_overload_const_str(method)
    if rfh__wrzlm in ('ffill', 'pad'):
        pmnxu__plg = 'n'
        send_right = True
    elif rfh__wrzlm in ('backfill', 'bfill'):
        pmnxu__plg = 'n-1, -1, -1'
        send_right = False
        if ijlc__angva == types.unicode_type:
            zoqcy__dmbqb = '(n - 1) - i'
            comw__gzyrn = True
    qnlwk__knzn = 'def impl(A, method, parallel=False):\n'
    qnlwk__knzn += '  A = decode_if_dict_array(A)\n'
    qnlwk__knzn += '  has_last_value = False\n'
    qnlwk__knzn += f'  last_value = {null_value}\n'
    qnlwk__knzn += '  if parallel:\n'
    qnlwk__knzn += '    rank = bodo.libs.distributed_api.get_rank()\n'
    qnlwk__knzn += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    qnlwk__knzn += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    qnlwk__knzn += '  n = len(A)\n'
    qnlwk__knzn += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    qnlwk__knzn += f'  for i in range({pmnxu__plg}):\n'
    qnlwk__knzn += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    qnlwk__knzn += (
        f'      bodo.libs.array_kernels.setna(out_arr, {zoqcy__dmbqb})\n')
    qnlwk__knzn += '      continue\n'
    qnlwk__knzn += '    s = A[i]\n'
    qnlwk__knzn += '    if bodo.libs.array_kernels.isna(A, i):\n'
    qnlwk__knzn += '      s = last_value\n'
    qnlwk__knzn += f'    out_arr[{zoqcy__dmbqb}] = s\n'
    qnlwk__knzn += '    last_value = s\n'
    qnlwk__knzn += '    has_last_value = True\n'
    if comw__gzyrn:
        qnlwk__knzn += '  return out_arr[::-1]\n'
    else:
        qnlwk__knzn += '  return out_arr\n'
    fys__kzbv = {}
    exec(qnlwk__knzn, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, fys__kzbv)
    impl = fys__kzbv['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        oglf__blhhn = 0
        bhux__mgxuq = n_pes - 1
        ujb__tzu = np.int32(rank + 1)
        sugk__axfm = np.int32(rank - 1)
        enu__mqi = len(in_arr) - 1
        jypmu__pih = -1
        sbt__tcuxh = -1
    else:
        oglf__blhhn = n_pes - 1
        bhux__mgxuq = 0
        ujb__tzu = np.int32(rank - 1)
        sugk__axfm = np.int32(rank + 1)
        enu__mqi = 0
        jypmu__pih = len(in_arr)
        sbt__tcuxh = 1
    qjk__abo = np.int32(bodo.hiframes.rolling.comm_border_tag)
    clofi__eik = np.empty(1, dtype=np.bool_)
    lzbes__ntjd = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    ezzch__jwk = np.empty(1, dtype=np.bool_)
    igxu__mjrwl = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    xhsc__jbhfa = False
    ivx__monfr = null_value
    for i in range(enu__mqi, jypmu__pih, sbt__tcuxh):
        if not isna(in_arr, i):
            xhsc__jbhfa = True
            ivx__monfr = in_arr[i]
            break
    if rank != oglf__blhhn:
        rstrc__qxiw = bodo.libs.distributed_api.irecv(clofi__eik, 1,
            sugk__axfm, qjk__abo, True)
        bodo.libs.distributed_api.wait(rstrc__qxiw, True)
        vvoyy__xqeoq = bodo.libs.distributed_api.irecv(lzbes__ntjd, 1,
            sugk__axfm, qjk__abo, True)
        bodo.libs.distributed_api.wait(vvoyy__xqeoq, True)
        epurv__kms = clofi__eik[0]
        duw__lam = lzbes__ntjd[0]
    else:
        epurv__kms = False
        duw__lam = null_value
    if xhsc__jbhfa:
        ezzch__jwk[0] = xhsc__jbhfa
        igxu__mjrwl[0] = ivx__monfr
    else:
        ezzch__jwk[0] = epurv__kms
        igxu__mjrwl[0] = duw__lam
    if rank != bhux__mgxuq:
        ywi__lrzj = bodo.libs.distributed_api.isend(ezzch__jwk, 1, ujb__tzu,
            qjk__abo, True)
        lmatn__jyt = bodo.libs.distributed_api.isend(igxu__mjrwl, 1,
            ujb__tzu, qjk__abo, True)
    return epurv__kms, duw__lam


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    kyx__jbje = {'axis': axis, 'kind': kind, 'order': order}
    jdwe__scu = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', kyx__jbje, jdwe__scu, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    pass


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    ijlc__angva = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                amgu__tejnx = A._indices
                kdi__xbis = len(amgu__tejnx)
                ivh__nss = alloc_int_array(kdi__xbis * repeats, np.int32)
                for i in range(kdi__xbis):
                    zoqcy__dmbqb = i * repeats
                    if bodo.libs.array_kernels.isna(amgu__tejnx, i):
                        for uhxxl__mhsj in range(repeats):
                            bodo.libs.array_kernels.setna(ivh__nss, 
                                zoqcy__dmbqb + uhxxl__mhsj)
                    else:
                        ivh__nss[zoqcy__dmbqb:zoqcy__dmbqb + repeats
                            ] = amgu__tejnx[i]
                return init_dict_arr(data_arr, ivh__nss, A.
                    _has_global_dictionary, A._has_deduped_local_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            kdi__xbis = len(A)
            out_arr = bodo.utils.utils.alloc_type(kdi__xbis * repeats,
                ijlc__angva, (-1,))
            for i in range(kdi__xbis):
                zoqcy__dmbqb = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for uhxxl__mhsj in range(repeats):
                        bodo.libs.array_kernels.setna(out_arr, zoqcy__dmbqb +
                            uhxxl__mhsj)
                else:
                    out_arr[zoqcy__dmbqb:zoqcy__dmbqb + repeats] = A[i]
            return out_arr
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            amgu__tejnx = A._indices
            kdi__xbis = len(amgu__tejnx)
            ivh__nss = alloc_int_array(repeats.sum(), np.int32)
            zoqcy__dmbqb = 0
            for i in range(kdi__xbis):
                egll__wkv = repeats[i]
                if egll__wkv < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(amgu__tejnx, i):
                    for uhxxl__mhsj in range(egll__wkv):
                        bodo.libs.array_kernels.setna(ivh__nss, 
                            zoqcy__dmbqb + uhxxl__mhsj)
                else:
                    ivh__nss[zoqcy__dmbqb:zoqcy__dmbqb + egll__wkv
                        ] = amgu__tejnx[i]
                zoqcy__dmbqb += egll__wkv
            return init_dict_arr(data_arr, ivh__nss, A.
                _has_global_dictionary, A._has_deduped_local_dictionary)
        return impl_dict_arr

    def impl_arr(A, repeats):
        kdi__xbis = len(A)
        out_arr = bodo.utils.utils.alloc_type(repeats.sum(), ijlc__angva, (-1,)
            )
        zoqcy__dmbqb = 0
        for i in range(kdi__xbis):
            egll__wkv = repeats[i]
            if egll__wkv < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for uhxxl__mhsj in range(egll__wkv):
                    bodo.libs.array_kernels.setna(out_arr, zoqcy__dmbqb +
                        uhxxl__mhsj)
            else:
                out_arr[zoqcy__dmbqb:zoqcy__dmbqb + egll__wkv] = A[i]
            zoqcy__dmbqb += egll__wkv
        return out_arr
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@numba.generated_jit
def repeat_like(A, dist_like_arr):
    if not bodo.utils.utils.is_array_typ(A, False
        ) or not bodo.utils.utils.is_array_typ(dist_like_arr, False):
        raise BodoError('Both A and dist_like_arr must be array-like.')

    def impl(A, dist_like_arr):
        return bodo.libs.array_kernels.repeat_kernel(A, len(dist_like_arr))
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        ytrre__konu = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(ytrre__konu, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        wmxup__espu = bodo.libs.array_kernels.concat([A1, A2])
        kinuf__otjgo = bodo.libs.array_kernels.unique(wmxup__espu)
        return pd.Series(kinuf__otjgo).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    kyx__jbje = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    jdwe__scu = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', kyx__jbje, jdwe__scu, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        ydxe__chijs = bodo.libs.array_kernels.unique(A1)
        mdf__oca = bodo.libs.array_kernels.unique(A2)
        wmxup__espu = bodo.libs.array_kernels.concat([ydxe__chijs, mdf__oca])
        wfjjd__dggc = pd.Series(wmxup__espu).sort_values().values
        return slice_array_intersect1d(wfjjd__dggc)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    cuy__rwl = arr[1:] == arr[:-1]
    return arr[:-1][cuy__rwl]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    qjk__abo = np.int32(bodo.hiframes.rolling.comm_border_tag)
    oyq__gbo = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        ndcr__cmb = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32(
            rank - 1), qjk__abo, True)
        bodo.libs.distributed_api.wait(ndcr__cmb, True)
    if rank == n_pes - 1:
        return None
    else:
        qfj__cstg = bodo.libs.distributed_api.irecv(oyq__gbo, 1, np.int32(
            rank + 1), qjk__abo, True)
        bodo.libs.distributed_api.wait(qfj__cstg, True)
        return oyq__gbo[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    cuy__rwl = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            cuy__rwl[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        myha__fyco = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == myha__fyco:
            cuy__rwl[n - 1] = True
    return cuy__rwl


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    kyx__jbje = {'assume_unique': assume_unique}
    jdwe__scu = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', kyx__jbje, jdwe__scu, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        ydxe__chijs = bodo.libs.array_kernels.unique(A1)
        mdf__oca = bodo.libs.array_kernels.unique(A2)
        cuy__rwl = calculate_mask_setdiff1d(ydxe__chijs, mdf__oca)
        return pd.Series(ydxe__chijs[cuy__rwl]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    cuy__rwl = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        cuy__rwl &= A1 != A2[i]
    return cuy__rwl


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    kyx__jbje = {'retstep': retstep, 'axis': axis}
    jdwe__scu = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', kyx__jbje, jdwe__scu, 'numpy')
    frf__dqvql = False
    if is_overload_none(dtype):
        ijlc__angva = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            frf__dqvql = True
        ijlc__angva = numba.np.numpy_support.as_dtype(dtype).type
    if frf__dqvql:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            dtks__yms = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, ijlc__angva)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = ijlc__angva(np.floor(start + i * dtks__yms))
            return out_arr
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            dtks__yms = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, ijlc__angva)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = ijlc__angva(start + i * dtks__yms)
            return out_arr
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'np.contains()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        yvwm__rkys = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                yvwm__rkys += A[i] == val
        return yvwm__rkys > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    kyx__jbje = {'axis': axis, 'out': out, 'keepdims': keepdims}
    jdwe__scu = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', kyx__jbje, jdwe__scu, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        yvwm__rkys = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                yvwm__rkys += int(bool(A[i]))
        return yvwm__rkys > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    kyx__jbje = {'axis': axis, 'out': out, 'keepdims': keepdims}
    jdwe__scu = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', kyx__jbje, jdwe__scu, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        yvwm__rkys = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                yvwm__rkys += int(bool(A[i]))
        return yvwm__rkys == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    kyx__jbje = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    jdwe__scu = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', kyx__jbje, jdwe__scu, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        jufh__jel = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            out_arr = np.empty(n, jufh__jel)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(out_arr, i)
                    continue
                out_arr[i] = np_cbrt_scalar(A[i], jufh__jel)
            return out_arr
        return impl_arr
    jufh__jel = np.promote_types(numba.np.numpy_support.as_dtype(A), numba.
        np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, jufh__jel)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    naq__znp = x < 0
    if naq__znp:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if naq__znp:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    ctort__etdqu = isinstance(tup, (types.BaseTuple, types.List))
    flo__ylqdn = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for exx__mtv in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(exx__mtv,
                'numpy.hstack()')
            ctort__etdqu = ctort__etdqu and bodo.utils.utils.is_array_typ(
                exx__mtv, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        ctort__etdqu = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif flo__ylqdn:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        bsifx__lgr = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for exx__mtv in bsifx__lgr.types:
            flo__ylqdn = flo__ylqdn and bodo.utils.utils.is_array_typ(exx__mtv,
                False)
    if not (ctort__etdqu or flo__ylqdn):
        return
    if flo__ylqdn:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    kyx__jbje = {'check_valid': check_valid, 'tol': tol}
    jdwe__scu = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', kyx__jbje,
        jdwe__scu, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        fmtre__oeat = mean.shape[0]
        vpo__cdom = size, fmtre__oeat
        flcu__mwj = np.random.standard_normal(vpo__cdom)
        cov = cov.astype(np.float64)
        rmm__qsrz, s, wvmwe__pxgqb = np.linalg.svd(cov)
        res = np.dot(flcu__mwj, np.sqrt(s).reshape(fmtre__oeat, 1) *
            wvmwe__pxgqb)
        sbhu__yaox = res + mean
        return sbhu__yaox
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, (IntegerArrayType, FloatingArrayType)) or arr in [
        boolean_array, datetime_date_array_type
        ] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            mye__ybpn = bodo.hiframes.series_kernels._get_type_max_value(arr)
            kwl__jpr = typing.builtins.IndexValue(-1, mye__ybpn)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                daizm__dio = typing.builtins.IndexValue(i, arr[i])
                kwl__jpr = min(kwl__jpr, daizm__dio)
            return kwl__jpr.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        fybcp__qyky = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            tcl__adllw = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            mye__ybpn = fybcp__qyky(len(arr.dtype.categories) + 1)
            kwl__jpr = typing.builtins.IndexValue(-1, mye__ybpn)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                daizm__dio = typing.builtins.IndexValue(i, tcl__adllw[i])
                kwl__jpr = min(kwl__jpr, daizm__dio)
            return kwl__jpr.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, (IntegerArrayType, FloatingArrayType)) or arr in [
        boolean_array, datetime_date_array_type
        ] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            mye__ybpn = bodo.hiframes.series_kernels._get_type_min_value(arr)
            kwl__jpr = typing.builtins.IndexValue(-1, mye__ybpn)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                daizm__dio = typing.builtins.IndexValue(i, arr[i])
                kwl__jpr = max(kwl__jpr, daizm__dio)
            return kwl__jpr.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        fybcp__qyky = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            tcl__adllw = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            mye__ybpn = fybcp__qyky(-1)
            kwl__jpr = typing.builtins.IndexValue(-1, mye__ybpn)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                daizm__dio = typing.builtins.IndexValue(i, tcl__adllw[i])
                kwl__jpr = max(kwl__jpr, daizm__dio)
            return kwl__jpr.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
