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
        sfe__flnad = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = sfe__flnad
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        sfe__flnad = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = sfe__flnad
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
            vnxjv__jxo = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            vnxjv__jxo[ind + 1] = vnxjv__jxo[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            vnxjv__jxo = bodo.libs.array_item_arr_ext.get_offsets(arr)
            vnxjv__jxo[ind + 1] = vnxjv__jxo[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            vnxjv__jxo = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            vnxjv__jxo[ind + 1] = vnxjv__jxo[ind]
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
    gowd__bap = arr_tup.count
    cwte__dzt = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(gowd__bap):
        cwte__dzt += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    cwte__dzt += '  return\n'
    qqi__nqw = {}
    exec(cwte__dzt, {'setna': setna}, qqi__nqw)
    impl = qqi__nqw['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        xqoxn__bvui = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(xqoxn__bvui.start, xqoxn__bvui.stop, xqoxn__bvui.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        tklob__enot = 'n'
        tessy__xuh = 'n_pes'
        htv__wztd = 'min_op'
    else:
        tklob__enot = 'n-1, -1, -1'
        tessy__xuh = '-1'
        htv__wztd = 'max_op'
    cwte__dzt = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {tessy__xuh}
    for i in range({tklob__enot}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {htv__wztd}))
        if possible_valid_rank != {tessy__xuh}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    qqi__nqw = {}
    exec(cwte__dzt, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op': max_op,
        'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.box_if_dt64},
        qqi__nqw)
    impl = qqi__nqw['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    lbm__yxeet = array_to_info(arr)
    _median_series_computation(res, lbm__yxeet, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lbm__yxeet)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    lbm__yxeet = array_to_info(arr)
    _autocorr_series_computation(res, lbm__yxeet, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lbm__yxeet)


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
    lbm__yxeet = array_to_info(arr)
    _compute_series_monotonicity(res, lbm__yxeet, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lbm__yxeet)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    kvkq__ulw = res[0] > 0.5
    return kvkq__ulw


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        qxf__jnsb = '-'
        yzdw__maoc = 'index_arr[0] > threshhold_date'
        tklob__enot = '1, n+1'
        kcqk__erz = 'index_arr[-i] <= threshhold_date'
        afl__feudg = 'i - 1'
    else:
        qxf__jnsb = '+'
        yzdw__maoc = 'index_arr[-1] < threshhold_date'
        tklob__enot = 'n'
        kcqk__erz = 'index_arr[i] >= threshhold_date'
        afl__feudg = 'i'
    cwte__dzt = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        cwte__dzt += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_tz_naive_type):\n'
            )
        cwte__dzt += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            cwte__dzt += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            cwte__dzt += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            cwte__dzt += '    else:\n'
            cwte__dzt += '      threshhold_date = initial_date + date_offset\n'
        else:
            cwte__dzt += (
                f'    threshhold_date = initial_date {qxf__jnsb} date_offset\n'
                )
    else:
        cwte__dzt += f'  threshhold_date = initial_date {qxf__jnsb} offset\n'
    cwte__dzt += '  local_valid = 0\n'
    cwte__dzt += f'  n = len(index_arr)\n'
    cwte__dzt += f'  if n:\n'
    cwte__dzt += f'    if {yzdw__maoc}:\n'
    cwte__dzt += '      loc_valid = n\n'
    cwte__dzt += '    else:\n'
    cwte__dzt += f'      for i in range({tklob__enot}):\n'
    cwte__dzt += f'        if {kcqk__erz}:\n'
    cwte__dzt += f'          loc_valid = {afl__feudg}\n'
    cwte__dzt += '          break\n'
    cwte__dzt += '  if is_parallel:\n'
    cwte__dzt += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    cwte__dzt += '    return total_valid\n'
    cwte__dzt += '  else:\n'
    cwte__dzt += '    return loc_valid\n'
    qqi__nqw = {}
    exec(cwte__dzt, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, qqi__nqw)
    return qqi__nqw['impl']


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
    lgft__jglxg = numba_to_c_type(sig.args[0].dtype)
    amt__pplb = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), lgft__jglxg))
    mvcm__mlk = args[0]
    cbp__joztp = sig.args[0]
    if isinstance(cbp__joztp, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        mvcm__mlk = cgutils.create_struct_proxy(cbp__joztp)(context,
            builder, mvcm__mlk).data
        cbp__joztp = types.Array(cbp__joztp.dtype, 1, 'C')
    assert cbp__joztp.ndim == 1
    arr = make_array(cbp__joztp)(context, builder, mvcm__mlk)
    fxpls__wwsah = builder.extract_value(arr.shape, 0)
    vlb__hxzn = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        fxpls__wwsah, args[1], builder.load(amt__pplb)]
    dwss__wrwdn = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    whs__tia = lir.FunctionType(lir.DoubleType(), dwss__wrwdn)
    remzo__xcqk = cgutils.get_or_insert_function(builder.module, whs__tia,
        name='quantile_sequential')
    jtfbp__edt = builder.call(remzo__xcqk, vlb__hxzn)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return jtfbp__edt


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, FloatingArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    lgft__jglxg = numba_to_c_type(sig.args[0].dtype)
    amt__pplb = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), lgft__jglxg))
    mvcm__mlk = args[0]
    cbp__joztp = sig.args[0]
    if isinstance(cbp__joztp, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        mvcm__mlk = cgutils.create_struct_proxy(cbp__joztp)(context,
            builder, mvcm__mlk).data
        cbp__joztp = types.Array(cbp__joztp.dtype, 1, 'C')
    assert cbp__joztp.ndim == 1
    arr = make_array(cbp__joztp)(context, builder, mvcm__mlk)
    fxpls__wwsah = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        bkebk__iuffz = args[2]
    else:
        bkebk__iuffz = fxpls__wwsah
    vlb__hxzn = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        fxpls__wwsah, bkebk__iuffz, args[1], builder.load(amt__pplb)]
    dwss__wrwdn = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        IntType(64), lir.DoubleType(), lir.IntType(32)]
    whs__tia = lir.FunctionType(lir.DoubleType(), dwss__wrwdn)
    remzo__xcqk = cgutils.get_or_insert_function(builder.module, whs__tia,
        name='quantile_parallel')
    jtfbp__edt = builder.call(remzo__xcqk, vlb__hxzn)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return jtfbp__edt


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        n = len(arr)
        jguj__qiivz = bodo.utils.utils.alloc_type(n, np.bool_, (-1,))
        jguj__qiivz[0] = True
        rds__stdvi = pd.isna(arr)
        for i in range(1, len(arr)):
            if rds__stdvi[i] and rds__stdvi[i - 1]:
                jguj__qiivz[i] = False
            elif rds__stdvi[i] or rds__stdvi[i - 1]:
                jguj__qiivz[i] = True
            else:
                jguj__qiivz[i] = arr[i] != arr[i - 1]
        return jguj__qiivz
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
    cwte__dzt = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    cwte__dzt += '  na_idxs = pd.isna(arr)\n'
    cwte__dzt += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    cwte__dzt += '  nas = sum(na_idxs)\n'
    if not ascending:
        cwte__dzt += '  if nas and nas < (sorter.size - 1):\n'
        cwte__dzt += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        cwte__dzt += '  else:\n'
        cwte__dzt += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        cwte__dzt += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    cwte__dzt += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    cwte__dzt += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        cwte__dzt += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        cwte__dzt += '    inv,\n'
        cwte__dzt += '    new_dtype=np.float64,\n'
        cwte__dzt += '    copy=True,\n'
        cwte__dzt += '    nan_to_str=False,\n'
        cwte__dzt += '    from_series=True,\n'
        cwte__dzt += '    ) + 1\n'
    else:
        cwte__dzt += '  arr = arr[sorter]\n'
        cwte__dzt += '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n'
        cwte__dzt += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            cwte__dzt += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            cwte__dzt += '    dense,\n'
            cwte__dzt += '    new_dtype=np.float64,\n'
            cwte__dzt += '    copy=True,\n'
            cwte__dzt += '    nan_to_str=False,\n'
            cwte__dzt += '    from_series=True,\n'
            cwte__dzt += '  )\n'
        else:
            cwte__dzt += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            cwte__dzt += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                cwte__dzt += '  ret = count_float[dense]\n'
            elif method == 'min':
                cwte__dzt += '  ret = count_float[dense - 1] + 1\n'
            else:
                cwte__dzt += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                cwte__dzt += '  ret[na_idxs] = -1\n'
            cwte__dzt += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            cwte__dzt += '  div_val = arr.size - nas\n'
        else:
            cwte__dzt += '  div_val = arr.size\n'
        cwte__dzt += '  for i in range(len(ret)):\n'
        cwte__dzt += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        cwte__dzt += '  ret[na_idxs] = np.nan\n'
    cwte__dzt += '  return ret\n'
    qqi__nqw = {}
    exec(cwte__dzt, {'np': np, 'pd': pd, 'bodo': bodo}, qqi__nqw)
    return qqi__nqw['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    ibbm__dsj = start
    jenpo__dkp = 2 * start + 1
    ylze__hdbfh = 2 * start + 2
    if jenpo__dkp < n and not cmp_f(arr[jenpo__dkp], arr[ibbm__dsj]):
        ibbm__dsj = jenpo__dkp
    if ylze__hdbfh < n and not cmp_f(arr[ylze__hdbfh], arr[ibbm__dsj]):
        ibbm__dsj = ylze__hdbfh
    if ibbm__dsj != start:
        arr[start], arr[ibbm__dsj] = arr[ibbm__dsj], arr[start]
        ind_arr[start], ind_arr[ibbm__dsj] = ind_arr[ibbm__dsj], ind_arr[start]
        min_heapify(arr, ind_arr, n, ibbm__dsj, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        bur__aqe = np.empty(k, A.dtype)
        gsff__qjzj = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                bur__aqe[ind] = A[i]
                gsff__qjzj[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            bur__aqe = bur__aqe[:ind]
            gsff__qjzj = gsff__qjzj[:ind]
        return bur__aqe, gsff__qjzj, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        nedyi__unlp = np.sort(A)
        fxu__cwbwa = index_arr[np.argsort(A)]
        akcff__mgmfu = pd.Series(nedyi__unlp).notna().values
        nedyi__unlp = nedyi__unlp[akcff__mgmfu]
        fxu__cwbwa = fxu__cwbwa[akcff__mgmfu]
        if is_largest:
            nedyi__unlp = nedyi__unlp[::-1]
            fxu__cwbwa = fxu__cwbwa[::-1]
        return np.ascontiguousarray(nedyi__unlp), np.ascontiguousarray(
            fxu__cwbwa)
    bur__aqe, gsff__qjzj, start = select_k_nonan(A, index_arr, m, k)
    gsff__qjzj = gsff__qjzj[bur__aqe.argsort()]
    bur__aqe.sort()
    if not is_largest:
        bur__aqe = np.ascontiguousarray(bur__aqe[::-1])
        gsff__qjzj = np.ascontiguousarray(gsff__qjzj[::-1])
    for i in range(start, m):
        if cmp_f(A[i], bur__aqe[0]):
            bur__aqe[0] = A[i]
            gsff__qjzj[0] = index_arr[i]
            min_heapify(bur__aqe, gsff__qjzj, k, 0, cmp_f)
    gsff__qjzj = gsff__qjzj[bur__aqe.argsort()]
    bur__aqe.sort()
    if is_largest:
        bur__aqe = bur__aqe[::-1]
        gsff__qjzj = gsff__qjzj[::-1]
    return np.ascontiguousarray(bur__aqe), np.ascontiguousarray(gsff__qjzj)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    xru__grfbh = bodo.libs.distributed_api.get_rank()
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    upk__nuu, eavt__bqsl = nlargest(A, I, k, is_largest, cmp_f)
    ixr__hrtfe = bodo.libs.distributed_api.gatherv(upk__nuu)
    vgn__kjh = bodo.libs.distributed_api.gatherv(eavt__bqsl)
    if xru__grfbh == MPI_ROOT:
        res, nlhj__pxbxc = nlargest(ixr__hrtfe, vgn__kjh, k, is_largest, cmp_f)
    else:
        res = np.empty(k, A.dtype)
        nlhj__pxbxc = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(nlhj__pxbxc)
    return res, nlhj__pxbxc


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    vtxdl__grjzt, wwzlj__fae = mat.shape
    xkyll__ijlfm = np.empty((wwzlj__fae, wwzlj__fae), dtype=np.float64)
    for dcmmk__tgjmd in range(wwzlj__fae):
        for lqylg__lspts in range(dcmmk__tgjmd + 1):
            hwkzs__kcphi = 0
            qbgbk__mxc = smqd__uwmc = vuv__flbj = nefg__zaoya = 0.0
            for i in range(vtxdl__grjzt):
                if np.isfinite(mat[i, dcmmk__tgjmd]) and np.isfinite(mat[i,
                    lqylg__lspts]):
                    hnw__yyf = mat[i, dcmmk__tgjmd]
                    dio__hetik = mat[i, lqylg__lspts]
                    hwkzs__kcphi += 1
                    vuv__flbj += hnw__yyf
                    nefg__zaoya += dio__hetik
            if parallel:
                hwkzs__kcphi = bodo.libs.distributed_api.dist_reduce(
                    hwkzs__kcphi, sum_op)
                vuv__flbj = bodo.libs.distributed_api.dist_reduce(vuv__flbj,
                    sum_op)
                nefg__zaoya = bodo.libs.distributed_api.dist_reduce(nefg__zaoya
                    , sum_op)
            if hwkzs__kcphi < minpv:
                xkyll__ijlfm[dcmmk__tgjmd, lqylg__lspts] = xkyll__ijlfm[
                    lqylg__lspts, dcmmk__tgjmd] = np.nan
            else:
                pvpw__faptz = vuv__flbj / hwkzs__kcphi
                kics__feva = nefg__zaoya / hwkzs__kcphi
                vuv__flbj = 0.0
                for i in range(vtxdl__grjzt):
                    if np.isfinite(mat[i, dcmmk__tgjmd]) and np.isfinite(mat
                        [i, lqylg__lspts]):
                        hnw__yyf = mat[i, dcmmk__tgjmd] - pvpw__faptz
                        dio__hetik = mat[i, lqylg__lspts] - kics__feva
                        vuv__flbj += hnw__yyf * dio__hetik
                        qbgbk__mxc += hnw__yyf * hnw__yyf
                        smqd__uwmc += dio__hetik * dio__hetik
                if parallel:
                    vuv__flbj = bodo.libs.distributed_api.dist_reduce(vuv__flbj
                        , sum_op)
                    qbgbk__mxc = bodo.libs.distributed_api.dist_reduce(
                        qbgbk__mxc, sum_op)
                    smqd__uwmc = bodo.libs.distributed_api.dist_reduce(
                        smqd__uwmc, sum_op)
                gyxff__ilvhy = hwkzs__kcphi - 1.0 if cov else sqrt(
                    qbgbk__mxc * smqd__uwmc)
                if gyxff__ilvhy != 0.0:
                    xkyll__ijlfm[dcmmk__tgjmd, lqylg__lspts] = xkyll__ijlfm[
                        lqylg__lspts, dcmmk__tgjmd] = vuv__flbj / gyxff__ilvhy
                else:
                    xkyll__ijlfm[dcmmk__tgjmd, lqylg__lspts] = xkyll__ijlfm[
                        lqylg__lspts, dcmmk__tgjmd] = np.nan
    return xkyll__ijlfm


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    jqw__flk = n != 1
    cwte__dzt = 'def impl(data, parallel=False):\n'
    cwte__dzt += '  if parallel:\n'
    rkgz__ohj = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    cwte__dzt += f'    cpp_table = arr_info_list_to_table([{rkgz__ohj}])\n'
    cwte__dzt += (
        f'    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)\n'
        )
    kqlv__mshy = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    cwte__dzt += f'    data = ({kqlv__mshy},)\n'
    cwte__dzt += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    cwte__dzt += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    cwte__dzt += '    bodo.libs.array.delete_table(cpp_table)\n'
    cwte__dzt += '  n = len(data[0])\n'
    cwte__dzt += '  out = np.empty(n, np.bool_)\n'
    cwte__dzt += '  uniqs = dict()\n'
    if jqw__flk:
        cwte__dzt += '  for i in range(n):\n'
        mdk__unmem = ', '.join(f'data[{i}][i]' for i in range(n))
        qsrep__fhx = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        cwte__dzt += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({mdk__unmem},), ({qsrep__fhx},))
"""
        cwte__dzt += '    if val in uniqs:\n'
        cwte__dzt += '      out[i] = True\n'
        cwte__dzt += '    else:\n'
        cwte__dzt += '      out[i] = False\n'
        cwte__dzt += '      uniqs[val] = 0\n'
    else:
        cwte__dzt += '  data = data[0]\n'
        cwte__dzt += '  hasna = False\n'
        cwte__dzt += '  for i in range(n):\n'
        cwte__dzt += '    if bodo.libs.array_kernels.isna(data, i):\n'
        cwte__dzt += '      out[i] = hasna\n'
        cwte__dzt += '      hasna = True\n'
        cwte__dzt += '    else:\n'
        cwte__dzt += '      val = data[i]\n'
        cwte__dzt += '      if val in uniqs:\n'
        cwte__dzt += '        out[i] = True\n'
        cwte__dzt += '      else:\n'
        cwte__dzt += '        out[i] = False\n'
        cwte__dzt += '        uniqs[val] = 0\n'
    cwte__dzt += '  if parallel:\n'
    cwte__dzt += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    cwte__dzt += '  return out\n'
    qqi__nqw = {}
    exec(cwte__dzt, {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table}, qqi__nqw)
    impl = qqi__nqw['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    pass


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    gowd__bap = len(data)
    cwte__dzt = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    cwte__dzt += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        gowd__bap)))
    cwte__dzt += '  table_total = arr_info_list_to_table(info_list_total)\n'
    cwte__dzt += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(gowd__bap))
    for ddub__zzq in range(gowd__bap):
        cwte__dzt += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(ddub__zzq, ddub__zzq, ddub__zzq))
    cwte__dzt += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(gowd__bap))
    cwte__dzt += '  delete_table(out_table)\n'
    cwte__dzt += '  delete_table(table_total)\n'
    cwte__dzt += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(gowd__bap)))
    qqi__nqw = {}
    exec(cwte__dzt, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, qqi__nqw)
    impl = qqi__nqw['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    pass


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    gowd__bap = len(data)
    cwte__dzt = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    cwte__dzt += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        gowd__bap)))
    cwte__dzt += '  table_total = arr_info_list_to_table(info_list_total)\n'
    cwte__dzt += '  keep_i = 0\n'
    cwte__dzt += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for ddub__zzq in range(gowd__bap):
        cwte__dzt += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(ddub__zzq, ddub__zzq, ddub__zzq))
    cwte__dzt += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(gowd__bap))
    cwte__dzt += '  delete_table(out_table)\n'
    cwte__dzt += '  delete_table(table_total)\n'
    cwte__dzt += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(gowd__bap)))
    qqi__nqw = {}
    exec(cwte__dzt, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, qqi__nqw)
    impl = qqi__nqw['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    pass


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        qol__iiric = [array_to_info(data_arr)]
        bzgl__vbdh = arr_info_list_to_table(qol__iiric)
        bace__crcfv = 0
        cdqa__zho = drop_duplicates_table(bzgl__vbdh, parallel, 1,
            bace__crcfv, False, True)
        out_arr = info_to_array(info_from_table(cdqa__zho, 0), data_arr)
        delete_table(cdqa__zho)
        delete_table(bzgl__vbdh)
        return out_arr
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    pass


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    ddrbc__srn = len(data.types)
    phb__whnee = [('out' + str(i)) for i in range(ddrbc__srn)]
    tesrs__dbx = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    wrxjz__cdy = ['isna(data[{}], i)'.format(i) for i in tesrs__dbx]
    cojhg__apm = 'not ({})'.format(' or '.join(wrxjz__cdy))
    if not is_overload_none(thresh):
        cojhg__apm = '(({}) <= ({}) - thresh)'.format(' + '.join(wrxjz__cdy
            ), ddrbc__srn - 1)
    elif how == 'all':
        cojhg__apm = 'not ({})'.format(' and '.join(wrxjz__cdy))
    cwte__dzt = 'def _dropna_imp(data, how, thresh, subset):\n'
    cwte__dzt += '  old_len = len(data[0])\n'
    cwte__dzt += '  new_len = 0\n'
    cwte__dzt += '  for i in range(old_len):\n'
    cwte__dzt += '    if {}:\n'.format(cojhg__apm)
    cwte__dzt += '      new_len += 1\n'
    for i, out in enumerate(phb__whnee):
        if isinstance(data[i], bodo.CategoricalArrayType):
            cwte__dzt += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            cwte__dzt += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    cwte__dzt += '  curr_ind = 0\n'
    cwte__dzt += '  for i in range(old_len):\n'
    cwte__dzt += '    if {}:\n'.format(cojhg__apm)
    for i in range(ddrbc__srn):
        cwte__dzt += '      if isna(data[{}], i):\n'.format(i)
        cwte__dzt += '        setna({}, curr_ind)\n'.format(phb__whnee[i])
        cwte__dzt += '      else:\n'
        cwte__dzt += '        {}[curr_ind] = data[{}][i]\n'.format(phb__whnee
            [i], i)
    cwte__dzt += '      curr_ind += 1\n'
    cwte__dzt += '  return {}\n'.format(', '.join(phb__whnee))
    qqi__nqw = {}
    ujbl__bnmmv = {'t{}'.format(i): odgu__yyf for i, odgu__yyf in enumerate
        (data.types)}
    ujbl__bnmmv.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(cwte__dzt, ujbl__bnmmv, qqi__nqw)
    minnn__jutc = qqi__nqw['_dropna_imp']
    return minnn__jutc


def get(arr, ind):
    pass


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        cbp__joztp = arr.dtype
        nlrzz__ccer = cbp__joztp.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            ujey__qiftl = init_nested_counts(nlrzz__ccer)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                ujey__qiftl = add_nested_counts(ujey__qiftl, val[ind])
            out_arr = bodo.utils.utils.alloc_type(n, cbp__joztp, ujey__qiftl)
            for iime__pnvb in range(n):
                if bodo.libs.array_kernels.isna(arr, iime__pnvb):
                    setna(out_arr, iime__pnvb)
                    continue
                val = arr[iime__pnvb]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(out_arr, iime__pnvb)
                    continue
                out_arr[iime__pnvb] = val[ind]
            return out_arr
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    bcf__tnpp = _to_readonly(arr_types.types[0])
    return all(isinstance(odgu__yyf, CategoricalArrayType) and _to_readonly
        (odgu__yyf) == bcf__tnpp for odgu__yyf in arr_types.types)


def concat(arr_list):
    pass


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        zcm__euwla = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            bvgz__bsyv = 0
            jzp__rlcur = []
            for A in arr_list:
                kmv__ivfhf = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                jzp__rlcur.append(bodo.libs.array_item_arr_ext.get_data(A))
                bvgz__bsyv += kmv__ivfhf
            tmwy__qxjb = np.empty(bvgz__bsyv + 1, offset_type)
            kvgu__ereiz = bodo.libs.array_kernels.concat(jzp__rlcur)
            dvfzb__gwejo = np.empty(bvgz__bsyv + 7 >> 3, np.uint8)
            qkdph__aymhr = 0
            akey__fjq = 0
            for A in arr_list:
                clotb__nyv = bodo.libs.array_item_arr_ext.get_offsets(A)
                gakiz__ngmxb = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                kmv__ivfhf = len(A)
                cmmde__jopg = clotb__nyv[kmv__ivfhf]
                for i in range(kmv__ivfhf):
                    tmwy__qxjb[i + qkdph__aymhr] = clotb__nyv[i] + akey__fjq
                    feftg__egru = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        gakiz__ngmxb, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(dvfzb__gwejo, i +
                        qkdph__aymhr, feftg__egru)
                qkdph__aymhr += kmv__ivfhf
                akey__fjq += cmmde__jopg
            tmwy__qxjb[qkdph__aymhr] = akey__fjq
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                bvgz__bsyv, kvgu__ereiz, tmwy__qxjb, dvfzb__gwejo)
            return out_arr
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        klkq__brt = arr_list.dtype.names
        cwte__dzt = 'def struct_array_concat_impl(arr_list):\n'
        cwte__dzt += f'    n_all = 0\n'
        for i in range(len(klkq__brt)):
            cwte__dzt += f'    concat_list{i} = []\n'
        cwte__dzt += '    for A in arr_list:\n'
        cwte__dzt += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(klkq__brt)):
            cwte__dzt += f'        concat_list{i}.append(data_tuple[{i}])\n'
        cwte__dzt += '        n_all += len(A)\n'
        cwte__dzt += '    n_bytes = (n_all + 7) >> 3\n'
        cwte__dzt += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        cwte__dzt += '    curr_bit = 0\n'
        cwte__dzt += '    for A in arr_list:\n'
        cwte__dzt += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        cwte__dzt += '        for j in range(len(A)):\n'
        cwte__dzt += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        cwte__dzt += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        cwte__dzt += '            curr_bit += 1\n'
        cwte__dzt += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        daf__rwt = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(klkq__brt))])
        cwte__dzt += f'        ({daf__rwt},),\n'
        cwte__dzt += '        new_mask,\n'
        cwte__dzt += f'        {klkq__brt},\n'
        cwte__dzt += '    )\n'
        qqi__nqw = {}
        exec(cwte__dzt, {'bodo': bodo, 'np': np}, qqi__nqw)
        return qqi__nqw['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.DatetimeArrayType):
        zozex__hejt = arr_list.dtype.tz

        def tz_aware_concat_impl(arr_list):
            afpsd__ykmni = 0
            for A in arr_list:
                afpsd__ykmni += len(A)
            dmg__jylhm = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(
                afpsd__ykmni, zozex__hejt)
            pqspr__qcbqm = 0
            for A in arr_list:
                for i in range(len(A)):
                    dmg__jylhm[i + pqspr__qcbqm] = A[i]
                pqspr__qcbqm += len(A)
            return dmg__jylhm
        return tz_aware_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            afpsd__ykmni = 0
            for A in arr_list:
                afpsd__ykmni += len(A)
            dmg__jylhm = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(afpsd__ykmni))
            pqspr__qcbqm = 0
            for A in arr_list:
                for i in range(len(A)):
                    dmg__jylhm._data[i + pqspr__qcbqm] = A._data[i]
                    feftg__egru = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(dmg__jylhm.
                        _null_bitmap, i + pqspr__qcbqm, feftg__egru)
                pqspr__qcbqm += len(A)
            return dmg__jylhm
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            afpsd__ykmni = 0
            for A in arr_list:
                afpsd__ykmni += len(A)
            dmg__jylhm = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(afpsd__ykmni))
            pqspr__qcbqm = 0
            for A in arr_list:
                for i in range(len(A)):
                    dmg__jylhm._days_data[i + pqspr__qcbqm] = A._days_data[i]
                    dmg__jylhm._seconds_data[i + pqspr__qcbqm
                        ] = A._seconds_data[i]
                    dmg__jylhm._microseconds_data[i + pqspr__qcbqm
                        ] = A._microseconds_data[i]
                    feftg__egru = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(dmg__jylhm.
                        _null_bitmap, i + pqspr__qcbqm, feftg__egru)
                pqspr__qcbqm += len(A)
            return dmg__jylhm
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        wkw__irhr = arr_list.dtype.precision
        zywnu__tpxg = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            afpsd__ykmni = 0
            for A in arr_list:
                afpsd__ykmni += len(A)
            dmg__jylhm = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                afpsd__ykmni, wkw__irhr, zywnu__tpxg)
            pqspr__qcbqm = 0
            for A in arr_list:
                for i in range(len(A)):
                    dmg__jylhm._data[i + pqspr__qcbqm] = A._data[i]
                    feftg__egru = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(dmg__jylhm.
                        _null_bitmap, i + pqspr__qcbqm, feftg__egru)
                pqspr__qcbqm += len(A)
            return dmg__jylhm
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        odgu__yyf) for odgu__yyf in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            rqza__iwuqg = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    rqza__iwuqg = arr_list.types[i]
                    break
        else:
            rqza__iwuqg = arr_list.dtype
        if rqza__iwuqg == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                rmlq__wnf = 0
                eypxm__sie = 0
                zrep__tkbya = 0
                for A in arr_list:
                    data_arr = A._data
                    pzvui__nlkhz = A._indices
                    zrep__tkbya += len(pzvui__nlkhz)
                    rmlq__wnf += len(data_arr)
                    eypxm__sie += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                edwfn__llzc = pre_alloc_string_array(rmlq__wnf, eypxm__sie)
                ishq__ccyeb = bodo.libs.int_arr_ext.alloc_int_array(zrep__tkbya
                    , np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(edwfn__llzc, -1)
                rnigo__ljqp = 0
                qla__gayxx = 0
                fdcgg__ezdej = 0
                for A in arr_list:
                    data_arr = A._data
                    pzvui__nlkhz = A._indices
                    zrep__tkbya = len(pzvui__nlkhz)
                    bodo.libs.str_arr_ext.set_string_array_range(edwfn__llzc,
                        data_arr, rnigo__ljqp, qla__gayxx)
                    for i in range(zrep__tkbya):
                        if bodo.libs.array_kernels.isna(pzvui__nlkhz, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            pzvui__nlkhz[i]):
                            bodo.libs.array_kernels.setna(ishq__ccyeb, 
                                fdcgg__ezdej + i)
                        else:
                            ishq__ccyeb[fdcgg__ezdej + i
                                ] = rnigo__ljqp + pzvui__nlkhz[i]
                    rnigo__ljqp += len(data_arr)
                    qla__gayxx += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                    fdcgg__ezdej += zrep__tkbya
                out_arr = init_dict_arr(edwfn__llzc, ishq__ccyeb, False, False)
                dho__yiw = drop_duplicates_local_dictionary(out_arr, False)
                return dho__yiw
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            rmlq__wnf = 0
            eypxm__sie = 0
            for A in arr_list:
                arr = A
                rmlq__wnf += len(arr)
                eypxm__sie += bodo.libs.str_arr_ext.num_total_chars(arr)
            out_arr = bodo.utils.utils.alloc_type(rmlq__wnf, rqza__iwuqg, (
                eypxm__sie,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)
            rnigo__ljqp = 0
            qla__gayxx = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(out_arr, arr,
                    rnigo__ljqp, qla__gayxx)
                rnigo__ljqp += len(arr)
                qla__gayxx += bodo.libs.str_arr_ext.num_total_chars(arr)
            return out_arr
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(odgu__yyf.dtype, types.Integer) for
        odgu__yyf in arr_list.types) and any(isinstance(odgu__yyf,
        IntegerArrayType) for odgu__yyf in arr_list.types):

        def impl_int_arr_list(arr_list):
            mcfmh__rpb = convert_to_nullable_tup(arr_list)
            ncoea__paam = []
            qwb__sne = 0
            for A in mcfmh__rpb:
                ncoea__paam.append(A._data)
                qwb__sne += len(A)
            kvgu__ereiz = bodo.libs.array_kernels.concat(ncoea__paam)
            wfm__ypaw = qwb__sne + 7 >> 3
            azb__wxhu = np.empty(wfm__ypaw, np.uint8)
            swna__bmpr = 0
            for A in mcfmh__rpb:
                dasa__vnn = A._null_bitmap
                for iime__pnvb in range(len(A)):
                    feftg__egru = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        dasa__vnn, iime__pnvb)
                    bodo.libs.int_arr_ext.set_bit_to_arr(azb__wxhu,
                        swna__bmpr, feftg__egru)
                    swna__bmpr += 1
            return bodo.libs.int_arr_ext.init_integer_array(kvgu__ereiz,
                azb__wxhu)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(odgu__yyf.dtype == types.bool_ for odgu__yyf in
        arr_list.types) and any(odgu__yyf == boolean_array for odgu__yyf in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            mcfmh__rpb = convert_to_nullable_tup(arr_list)
            ncoea__paam = []
            qwb__sne = 0
            for A in mcfmh__rpb:
                ncoea__paam.append(A._data)
                qwb__sne += len(A)
            kvgu__ereiz = bodo.libs.array_kernels.concat(ncoea__paam)
            wfm__ypaw = qwb__sne + 7 >> 3
            azb__wxhu = np.empty(wfm__ypaw, np.uint8)
            swna__bmpr = 0
            for A in mcfmh__rpb:
                dasa__vnn = A._null_bitmap
                for iime__pnvb in range(len(A)):
                    feftg__egru = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        dasa__vnn, iime__pnvb)
                    bodo.libs.int_arr_ext.set_bit_to_arr(azb__wxhu,
                        swna__bmpr, feftg__egru)
                    swna__bmpr += 1
            return bodo.libs.bool_arr_ext.init_bool_array(kvgu__ereiz,
                azb__wxhu)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, FloatingArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(odgu__yyf.dtype, types.Float) for
        odgu__yyf in arr_list.types) and any(isinstance(odgu__yyf,
        FloatingArrayType) for odgu__yyf in arr_list.types):

        def impl_float_arr_list(arr_list):
            mcfmh__rpb = convert_to_nullable_tup(arr_list)
            ncoea__paam = []
            qwb__sne = 0
            for A in mcfmh__rpb:
                ncoea__paam.append(A._data)
                qwb__sne += len(A)
            kvgu__ereiz = bodo.libs.array_kernels.concat(ncoea__paam)
            wfm__ypaw = qwb__sne + 7 >> 3
            azb__wxhu = np.empty(wfm__ypaw, np.uint8)
            swna__bmpr = 0
            for A in mcfmh__rpb:
                dasa__vnn = A._null_bitmap
                for iime__pnvb in range(len(A)):
                    feftg__egru = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        dasa__vnn, iime__pnvb)
                    bodo.libs.int_arr_ext.set_bit_to_arr(azb__wxhu,
                        swna__bmpr, feftg__egru)
                    swna__bmpr += 1
            return bodo.libs.float_arr_ext.init_float_array(kvgu__ereiz,
                azb__wxhu)
        return impl_float_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            jxf__wdwuz = []
            for A in arr_list:
                jxf__wdwuz.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                jxf__wdwuz), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        efdss__dtrux = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        cwte__dzt = 'def impl(arr_list):\n'
        cwte__dzt += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({efdss__dtrux}, )), arr_list[0].dtype)
"""
        lshoj__zitq = {}
        exec(cwte__dzt, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, lshoj__zitq)
        return lshoj__zitq['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            qwb__sne = 0
            for A in arr_list:
                qwb__sne += len(A)
            out_arr = np.empty(qwb__sne, dtype)
            ryx__styg = 0
            for A in arr_list:
                n = len(A)
                out_arr[ryx__styg:ryx__styg + n] = A
                ryx__styg += n
            return out_arr
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(odgu__yyf,
        (types.Array, IntegerArrayType)) and isinstance(odgu__yyf.dtype,
        types.Integer) for odgu__yyf in arr_list.types) and any(isinstance(
        odgu__yyf, types.Array) and isinstance(odgu__yyf.dtype, types.Float
        ) for odgu__yyf in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            vwyf__inlzw = []
            for A in arr_list:
                vwyf__inlzw.append(A._data)
            zvloz__kzplc = bodo.libs.array_kernels.concat(vwyf__inlzw)
            xkyll__ijlfm = bodo.libs.map_arr_ext.init_map_arr(zvloz__kzplc)
            return xkyll__ijlfm
        return impl_map_arr_list
    if isinstance(arr_list, types.Tuple):
        jia__sowbm = all([(isinstance(laytl__gyjq, bodo.DatetimeArrayType) or
            isinstance(laytl__gyjq, types.Array) and laytl__gyjq.dtype ==
            bodo.datetime64ns) for laytl__gyjq in arr_list.types])
        if jia__sowbm:
            raise BodoError(
                f'Cannot concatenate the rows of Timestamp data with different timezones. Found types: {arr_list}. Please use pd.Series.tz_convert(None) to remove Timezone information.'
                )
    for laytl__gyjq in arr_list:
        if not isinstance(laytl__gyjq, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(odgu__yyf.astype(np.float64) for odgu__yyf in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    gowd__bap = len(arr_tup.types)
    cwte__dzt = 'def f(arr_tup):\n'
    cwte__dzt += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(gowd__bap
        )), ',' if gowd__bap == 1 else '')
    qqi__nqw = {}
    exec(cwte__dzt, {'np': np}, qqi__nqw)
    hkt__khp = qqi__nqw['f']
    return hkt__khp


def convert_to_nullable_tup(arr_tup):
    pass


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, FloatingArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple
        ), 'convert_to_nullable_tup: tuple expected'
    gowd__bap = len(arr_tup.types)
    mfcc__txbf = find_common_np_dtype(arr_tup.types)
    nlrzz__ccer = None
    qrtp__iku = ''
    if isinstance(mfcc__txbf, types.Integer):
        nlrzz__ccer = bodo.libs.int_arr_ext.IntDtype(mfcc__txbf)
        qrtp__iku = '.astype(out_dtype, False)'
    if isinstance(mfcc__txbf, types.Float
        ) and bodo.libs.float_arr_ext._use_nullable_float:
        nlrzz__ccer = bodo.libs.float_arr_ext.FloatDtype(mfcc__txbf)
        qrtp__iku = '.astype(out_dtype, False)'
    cwte__dzt = 'def f(arr_tup):\n'
    cwte__dzt += '  return ({}{})\n'.format(','.join(
        f'bodo.utils.conversion.coerce_to_array(arr_tup[{i}], use_nullable_array=True){qrtp__iku}'
         for i in range(gowd__bap)), ',' if gowd__bap == 1 else '')
    qqi__nqw = {}
    exec(cwte__dzt, {'bodo': bodo, 'out_dtype': nlrzz__ccer}, qqi__nqw)
    qngu__biz = qqi__nqw['f']
    return qngu__biz


def nunique(A, dropna):
    pass


def nunique_parallel(A, dropna):
    pass


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, lzdy__hds = build_set_seen_na(A)
        return len(s) + int(not dropna and lzdy__hds)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        vzy__kax = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        muop__xkur = len(vzy__kax)
        return bodo.libs.distributed_api.dist_reduce(muop__xkur, np.int32(
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
    auac__kbjsv = get_overload_const_str(func_name)
    assert auac__kbjsv in ('cumsum', 'cumprod', 'cummin', 'cummax'
        ), 'accum_func: invalid func_name'
    if auac__kbjsv == 'cumsum':
        lit__cmr = A.dtype(0)
        tkzmw__jgmak = np.int32(Reduce_Type.Sum.value)
        vjuv__sjiqx = np.add
    if auac__kbjsv == 'cumprod':
        lit__cmr = A.dtype(1)
        tkzmw__jgmak = np.int32(Reduce_Type.Prod.value)
        vjuv__sjiqx = np.multiply
    if auac__kbjsv == 'cummin':
        if isinstance(A.dtype, types.Float):
            lit__cmr = np.finfo(A.dtype(1).dtype).max
        else:
            lit__cmr = np.iinfo(A.dtype(1).dtype).max
        tkzmw__jgmak = np.int32(Reduce_Type.Min.value)
        vjuv__sjiqx = min
    if auac__kbjsv == 'cummax':
        if isinstance(A.dtype, types.Float):
            lit__cmr = np.finfo(A.dtype(1).dtype).min
        else:
            lit__cmr = np.iinfo(A.dtype(1).dtype).min
        tkzmw__jgmak = np.int32(Reduce_Type.Max.value)
        vjuv__sjiqx = max
    jkpwi__icck = A

    def impl(A, func_name, parallel=False):
        n = len(A)
        idamc__uubkk = lit__cmr
        if parallel:
            for i in range(n):
                if not bodo.libs.array_kernels.isna(A, i):
                    idamc__uubkk = vjuv__sjiqx(idamc__uubkk, A[i])
            idamc__uubkk = bodo.libs.distributed_api.dist_exscan(idamc__uubkk,
                tkzmw__jgmak)
            if bodo.get_rank() == 0:
                idamc__uubkk = lit__cmr
        out_arr = bodo.utils.utils.alloc_type(n, jkpwi__icck, (-1,))
        for i in range(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(out_arr, i)
                continue
            idamc__uubkk = vjuv__sjiqx(idamc__uubkk, A[i])
            out_arr[i] = idamc__uubkk
        return out_arr
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        qlvjb__hkkd = arr_info_list_to_table([array_to_info(A)])
        sit__shha = 1
        bace__crcfv = 0
        cdqa__zho = drop_duplicates_table(qlvjb__hkkd, parallel, sit__shha,
            bace__crcfv, dropna, True)
        out_arr = info_to_array(info_from_table(cdqa__zho, 0), A)
        delete_table(qlvjb__hkkd)
        delete_table(cdqa__zho)
        return out_arr
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    zcm__euwla = bodo.utils.typing.to_nullable_type(arr.dtype)
    mzo__hukht = index_arr
    uvh__buy = mzo__hukht.dtype

    def impl(arr, index_arr):
        n = len(arr)
        ujey__qiftl = init_nested_counts(zcm__euwla)
        mnmux__wbfw = init_nested_counts(uvh__buy)
        for i in range(n):
            yhdaz__ufmw = index_arr[i]
            if isna(arr, i):
                ujey__qiftl = (ujey__qiftl[0] + 1,) + ujey__qiftl[1:]
                mnmux__wbfw = add_nested_counts(mnmux__wbfw, yhdaz__ufmw)
                continue
            esuyc__vvc = arr[i]
            if len(esuyc__vvc) == 0:
                ujey__qiftl = (ujey__qiftl[0] + 1,) + ujey__qiftl[1:]
                mnmux__wbfw = add_nested_counts(mnmux__wbfw, yhdaz__ufmw)
                continue
            ujey__qiftl = add_nested_counts(ujey__qiftl, esuyc__vvc)
            for xnseo__dwxx in range(len(esuyc__vvc)):
                mnmux__wbfw = add_nested_counts(mnmux__wbfw, yhdaz__ufmw)
        out_arr = bodo.utils.utils.alloc_type(ujey__qiftl[0], zcm__euwla,
            ujey__qiftl[1:])
        jypi__mjvxk = bodo.utils.utils.alloc_type(ujey__qiftl[0],
            mzo__hukht, mnmux__wbfw)
        akey__fjq = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, akey__fjq)
                jypi__mjvxk[akey__fjq] = index_arr[i]
                akey__fjq += 1
                continue
            esuyc__vvc = arr[i]
            cmmde__jopg = len(esuyc__vvc)
            if cmmde__jopg == 0:
                setna(out_arr, akey__fjq)
                jypi__mjvxk[akey__fjq] = index_arr[i]
                akey__fjq += 1
                continue
            out_arr[akey__fjq:akey__fjq + cmmde__jopg] = esuyc__vvc
            jypi__mjvxk[akey__fjq:akey__fjq + cmmde__jopg] = index_arr[i]
            akey__fjq += cmmde__jopg
        return out_arr, jypi__mjvxk
    return impl


def explode_no_index(arr):
    pass


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    zcm__euwla = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        ujey__qiftl = init_nested_counts(zcm__euwla)
        for i in range(n):
            if isna(arr, i):
                ujey__qiftl = (ujey__qiftl[0] + 1,) + ujey__qiftl[1:]
                ndvxd__ctb = 1
            else:
                esuyc__vvc = arr[i]
                vayjn__kcc = len(esuyc__vvc)
                if vayjn__kcc == 0:
                    ujey__qiftl = (ujey__qiftl[0] + 1,) + ujey__qiftl[1:]
                    ndvxd__ctb = 1
                    continue
                else:
                    ujey__qiftl = add_nested_counts(ujey__qiftl, esuyc__vvc)
                    ndvxd__ctb = vayjn__kcc
            if counts[i] != ndvxd__ctb:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        out_arr = bodo.utils.utils.alloc_type(ujey__qiftl[0], zcm__euwla,
            ujey__qiftl[1:])
        akey__fjq = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, akey__fjq)
                akey__fjq += 1
                continue
            esuyc__vvc = arr[i]
            cmmde__jopg = len(esuyc__vvc)
            if cmmde__jopg == 0:
                setna(out_arr, akey__fjq)
                akey__fjq += 1
                continue
            out_arr[akey__fjq:akey__fjq + cmmde__jopg] = esuyc__vvc
            akey__fjq += cmmde__jopg
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
        htfdz__mmxfq = 'np.empty(n, np.int64)'
        aixf__vgo = 'out_arr[i] = 1'
        kclxg__lxtei = 'max(len(arr[i]), 1)'
    else:
        htfdz__mmxfq = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        aixf__vgo = 'bodo.libs.array_kernels.setna(out_arr, i)'
        kclxg__lxtei = 'len(arr[i])'
    cwte__dzt = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {htfdz__mmxfq}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {aixf__vgo}
        else:
            out_arr[i] = {kclxg__lxtei}
    return out_arr
    """
    qqi__nqw = {}
    exec(cwte__dzt, {'bodo': bodo, 'numba': numba, 'np': np}, qqi__nqw)
    impl = qqi__nqw['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    pass


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    mzo__hukht = index_arr
    uvh__buy = mzo__hukht.dtype

    def impl(arr, pat, n, index_arr):
        vtit__wcbyw = pat is not None and len(pat) > 1
        if vtit__wcbyw:
            qqc__viy = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        uqgj__vqxz = len(arr)
        rmlq__wnf = 0
        eypxm__sie = 0
        mnmux__wbfw = init_nested_counts(uvh__buy)
        for i in range(uqgj__vqxz):
            yhdaz__ufmw = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                rmlq__wnf += 1
                mnmux__wbfw = add_nested_counts(mnmux__wbfw, yhdaz__ufmw)
                continue
            if vtit__wcbyw:
                irr__ieg = qqc__viy.split(arr[i], maxsplit=n)
            else:
                irr__ieg = arr[i].split(pat, n)
            rmlq__wnf += len(irr__ieg)
            for s in irr__ieg:
                mnmux__wbfw = add_nested_counts(mnmux__wbfw, yhdaz__ufmw)
                eypxm__sie += bodo.libs.str_arr_ext.get_utf8_size(s)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(rmlq__wnf,
            eypxm__sie)
        jypi__mjvxk = bodo.utils.utils.alloc_type(rmlq__wnf, mzo__hukht,
            mnmux__wbfw)
        jebxk__iygy = 0
        for iime__pnvb in range(uqgj__vqxz):
            if isna(arr, iime__pnvb):
                out_arr[jebxk__iygy] = ''
                bodo.libs.array_kernels.setna(out_arr, jebxk__iygy)
                jypi__mjvxk[jebxk__iygy] = index_arr[iime__pnvb]
                jebxk__iygy += 1
                continue
            if vtit__wcbyw:
                irr__ieg = qqc__viy.split(arr[iime__pnvb], maxsplit=n)
            else:
                irr__ieg = arr[iime__pnvb].split(pat, n)
            hel__khbxx = len(irr__ieg)
            out_arr[jebxk__iygy:jebxk__iygy + hel__khbxx] = irr__ieg
            jypi__mjvxk[jebxk__iygy:jebxk__iygy + hel__khbxx] = index_arr[
                iime__pnvb]
            jebxk__iygy += hel__khbxx
        return out_arr, jypi__mjvxk
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
            opxl__rmutt = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            vwxr__ercc = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(vwxr__ercc, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(opxl__rmutt,
                vwxr__ercc, True, True)
        return impl_dict
    pkbit__sjve = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        out_arr = bodo.utils.utils.alloc_type(n, pkbit__sjve, (0,))
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
    uugg__kkmn = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            out_arr = bodo.utils.utils.alloc_type(new_len, uugg__kkmn)
            bodo.libs.str_arr_ext.str_copy_ptr(out_arr.ctypes, 0, A.ctypes,
                old_size)
            return out_arr
        return impl_char

    def impl(A, old_size, new_len):
        out_arr = bodo.utils.utils.alloc_type(new_len, uugg__kkmn, (-1,))
        out_arr[:old_size] = A[:old_size]
        return out_arr
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    coosm__yhn = math.ceil((stop - start) / step)
    return int(max(coosm__yhn, 0))


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
    if any(isinstance(ldbsl__nghi, types.Complex) for ldbsl__nghi in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            loki__zwr = (stop - start) / step
            coosm__yhn = math.ceil(loki__zwr.real)
            jdgmk__myhh = math.ceil(loki__zwr.imag)
            mscyf__kvi = int(max(min(jdgmk__myhh, coosm__yhn), 0))
            arr = np.empty(mscyf__kvi, dtype)
            for i in numba.parfors.parfor.internal_prange(mscyf__kvi):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            mscyf__kvi = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(mscyf__kvi, dtype)
            for i in numba.parfors.parfor.internal_prange(mscyf__kvi):
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
        lrqq__cip = arr,
        if not inplace:
            lrqq__cip = arr.copy(),
        zlqgc__yirz = bodo.libs.str_arr_ext.to_list_if_immutable_arr(lrqq__cip)
        jfesd__xvsm = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True
            )
        bodo.libs.timsort.sort(zlqgc__yirz, 0, n, jfesd__xvsm)
        if not ascending:
            bodo.libs.timsort.reverseRange(zlqgc__yirz, 0, n, jfesd__xvsm)
        bodo.libs.str_arr_ext.cp_str_list_to_array(lrqq__cip, zlqgc__yirz)
        return lrqq__cip[0]
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
        xkyll__ijlfm = []
        for i in range(n):
            if A[i]:
                xkyll__ijlfm.append(i + offset)
        return np.array(xkyll__ijlfm, np.int64),
    return impl


def ffill_bfill_arr(arr):
    pass


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    uugg__kkmn = element_type(A)
    if uugg__kkmn == types.unicode_type:
        null_value = '""'
    elif uugg__kkmn == types.bool_:
        null_value = 'False'
    elif uugg__kkmn == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_datetime(0))'
            )
    elif uugg__kkmn == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_timedelta(0))'
            )
    else:
        null_value = '0'
    jebxk__iygy = 'i'
    evvj__egxo = False
    bkt__yacp = get_overload_const_str(method)
    if bkt__yacp in ('ffill', 'pad'):
        vtz__ltefx = 'n'
        send_right = True
    elif bkt__yacp in ('backfill', 'bfill'):
        vtz__ltefx = 'n-1, -1, -1'
        send_right = False
        if uugg__kkmn == types.unicode_type:
            jebxk__iygy = '(n - 1) - i'
            evvj__egxo = True
    cwte__dzt = 'def impl(A, method, parallel=False):\n'
    cwte__dzt += '  A = decode_if_dict_array(A)\n'
    cwte__dzt += '  has_last_value = False\n'
    cwte__dzt += f'  last_value = {null_value}\n'
    cwte__dzt += '  if parallel:\n'
    cwte__dzt += '    rank = bodo.libs.distributed_api.get_rank()\n'
    cwte__dzt += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    cwte__dzt += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    cwte__dzt += '  n = len(A)\n'
    cwte__dzt += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    cwte__dzt += f'  for i in range({vtz__ltefx}):\n'
    cwte__dzt += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    cwte__dzt += (
        f'      bodo.libs.array_kernels.setna(out_arr, {jebxk__iygy})\n')
    cwte__dzt += '      continue\n'
    cwte__dzt += '    s = A[i]\n'
    cwte__dzt += '    if bodo.libs.array_kernels.isna(A, i):\n'
    cwte__dzt += '      s = last_value\n'
    cwte__dzt += f'    out_arr[{jebxk__iygy}] = s\n'
    cwte__dzt += '    last_value = s\n'
    cwte__dzt += '    has_last_value = True\n'
    if evvj__egxo:
        cwte__dzt += '  return out_arr[::-1]\n'
    else:
        cwte__dzt += '  return out_arr\n'
    owiuo__witf = {}
    exec(cwte__dzt, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, owiuo__witf)
    impl = owiuo__witf['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        izxrn__arhit = 0
        zadx__rwju = n_pes - 1
        omqop__hzih = np.int32(rank + 1)
        sjthf__rpj = np.int32(rank - 1)
        qifo__pxiph = len(in_arr) - 1
        zyzrp__lvcj = -1
        agd__xto = -1
    else:
        izxrn__arhit = n_pes - 1
        zadx__rwju = 0
        omqop__hzih = np.int32(rank - 1)
        sjthf__rpj = np.int32(rank + 1)
        qifo__pxiph = 0
        zyzrp__lvcj = len(in_arr)
        agd__xto = 1
    yob__tbno = np.int32(bodo.hiframes.rolling.comm_border_tag)
    bdpw__gqdzw = np.empty(1, dtype=np.bool_)
    ycswt__kovk = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    atr__jbx = np.empty(1, dtype=np.bool_)
    lmxa__coroc = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    icvd__lcw = False
    zfik__bvk = null_value
    for i in range(qifo__pxiph, zyzrp__lvcj, agd__xto):
        if not isna(in_arr, i):
            icvd__lcw = True
            zfik__bvk = in_arr[i]
            break
    if rank != izxrn__arhit:
        wlt__zrl = bodo.libs.distributed_api.irecv(bdpw__gqdzw, 1,
            sjthf__rpj, yob__tbno, True)
        bodo.libs.distributed_api.wait(wlt__zrl, True)
        jkl__qqpfr = bodo.libs.distributed_api.irecv(ycswt__kovk, 1,
            sjthf__rpj, yob__tbno, True)
        bodo.libs.distributed_api.wait(jkl__qqpfr, True)
        agx__jqsw = bdpw__gqdzw[0]
        kaoe__btr = ycswt__kovk[0]
    else:
        agx__jqsw = False
        kaoe__btr = null_value
    if icvd__lcw:
        atr__jbx[0] = icvd__lcw
        lmxa__coroc[0] = zfik__bvk
    else:
        atr__jbx[0] = agx__jqsw
        lmxa__coroc[0] = kaoe__btr
    if rank != zadx__rwju:
        gvzpc__pnj = bodo.libs.distributed_api.isend(atr__jbx, 1,
            omqop__hzih, yob__tbno, True)
        ilprg__rlau = bodo.libs.distributed_api.isend(lmxa__coroc, 1,
            omqop__hzih, yob__tbno, True)
    return agx__jqsw, kaoe__btr


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    iyiuu__okjb = {'axis': axis, 'kind': kind, 'order': order}
    vvx__tekzx = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', iyiuu__okjb, vvx__tekzx, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    pass


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    uugg__kkmn = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                pzvui__nlkhz = A._indices
                uqgj__vqxz = len(pzvui__nlkhz)
                ishq__ccyeb = alloc_int_array(uqgj__vqxz * repeats, np.int32)
                for i in range(uqgj__vqxz):
                    jebxk__iygy = i * repeats
                    if bodo.libs.array_kernels.isna(pzvui__nlkhz, i):
                        for iime__pnvb in range(repeats):
                            bodo.libs.array_kernels.setna(ishq__ccyeb, 
                                jebxk__iygy + iime__pnvb)
                    else:
                        ishq__ccyeb[jebxk__iygy:jebxk__iygy + repeats
                            ] = pzvui__nlkhz[i]
                return init_dict_arr(data_arr, ishq__ccyeb, A.
                    _has_global_dictionary, A._has_deduped_local_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            uqgj__vqxz = len(A)
            out_arr = bodo.utils.utils.alloc_type(uqgj__vqxz * repeats,
                uugg__kkmn, (-1,))
            for i in range(uqgj__vqxz):
                jebxk__iygy = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for iime__pnvb in range(repeats):
                        bodo.libs.array_kernels.setna(out_arr, jebxk__iygy +
                            iime__pnvb)
                else:
                    out_arr[jebxk__iygy:jebxk__iygy + repeats] = A[i]
            return out_arr
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            pzvui__nlkhz = A._indices
            uqgj__vqxz = len(pzvui__nlkhz)
            ishq__ccyeb = alloc_int_array(repeats.sum(), np.int32)
            jebxk__iygy = 0
            for i in range(uqgj__vqxz):
                qzgy__ftk = repeats[i]
                if qzgy__ftk < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(pzvui__nlkhz, i):
                    for iime__pnvb in range(qzgy__ftk):
                        bodo.libs.array_kernels.setna(ishq__ccyeb, 
                            jebxk__iygy + iime__pnvb)
                else:
                    ishq__ccyeb[jebxk__iygy:jebxk__iygy + qzgy__ftk
                        ] = pzvui__nlkhz[i]
                jebxk__iygy += qzgy__ftk
            return init_dict_arr(data_arr, ishq__ccyeb, A.
                _has_global_dictionary, A._has_deduped_local_dictionary)
        return impl_dict_arr

    def impl_arr(A, repeats):
        uqgj__vqxz = len(A)
        out_arr = bodo.utils.utils.alloc_type(repeats.sum(), uugg__kkmn, (-1,))
        jebxk__iygy = 0
        for i in range(uqgj__vqxz):
            qzgy__ftk = repeats[i]
            if qzgy__ftk < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for iime__pnvb in range(qzgy__ftk):
                    bodo.libs.array_kernels.setna(out_arr, jebxk__iygy +
                        iime__pnvb)
            else:
                out_arr[jebxk__iygy:jebxk__iygy + qzgy__ftk] = A[i]
            jebxk__iygy += qzgy__ftk
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
        pnj__zeyvd = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(pnj__zeyvd, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        vpqn__rxvj = bodo.libs.array_kernels.concat([A1, A2])
        hdy__znakw = bodo.libs.array_kernels.unique(vpqn__rxvj)
        return pd.Series(hdy__znakw).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    iyiuu__okjb = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    vvx__tekzx = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', iyiuu__okjb, vvx__tekzx, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        skr__lbs = bodo.libs.array_kernels.unique(A1)
        pmxx__txi = bodo.libs.array_kernels.unique(A2)
        vpqn__rxvj = bodo.libs.array_kernels.concat([skr__lbs, pmxx__txi])
        bspeu__xui = pd.Series(vpqn__rxvj).sort_values().values
        return slice_array_intersect1d(bspeu__xui)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    akcff__mgmfu = arr[1:] == arr[:-1]
    return arr[:-1][akcff__mgmfu]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    yob__tbno = np.int32(bodo.hiframes.rolling.comm_border_tag)
    pwujy__wxl = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        bwuh__kdv = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32(
            rank - 1), yob__tbno, True)
        bodo.libs.distributed_api.wait(bwuh__kdv, True)
    if rank == n_pes - 1:
        return None
    else:
        jdxls__nmb = bodo.libs.distributed_api.irecv(pwujy__wxl, 1, np.
            int32(rank + 1), yob__tbno, True)
        bodo.libs.distributed_api.wait(jdxls__nmb, True)
        return pwujy__wxl[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    akcff__mgmfu = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            akcff__mgmfu[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        ohk__liqav = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == ohk__liqav:
            akcff__mgmfu[n - 1] = True
    return akcff__mgmfu


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    iyiuu__okjb = {'assume_unique': assume_unique}
    vvx__tekzx = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', iyiuu__okjb, vvx__tekzx, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        skr__lbs = bodo.libs.array_kernels.unique(A1)
        pmxx__txi = bodo.libs.array_kernels.unique(A2)
        akcff__mgmfu = calculate_mask_setdiff1d(skr__lbs, pmxx__txi)
        return pd.Series(skr__lbs[akcff__mgmfu]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    akcff__mgmfu = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        akcff__mgmfu &= A1 != A2[i]
    return akcff__mgmfu


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    iyiuu__okjb = {'retstep': retstep, 'axis': axis}
    vvx__tekzx = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', iyiuu__okjb, vvx__tekzx, 'numpy')
    sch__viddw = False
    if is_overload_none(dtype):
        uugg__kkmn = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            sch__viddw = True
        uugg__kkmn = numba.np.numpy_support.as_dtype(dtype).type
    if sch__viddw:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            aqze__wrf = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, uugg__kkmn)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = uugg__kkmn(np.floor(start + i * aqze__wrf))
            return out_arr
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            aqze__wrf = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, uugg__kkmn)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = uugg__kkmn(start + i * aqze__wrf)
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
        gowd__bap = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                gowd__bap += A[i] == val
        return gowd__bap > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    iyiuu__okjb = {'axis': axis, 'out': out, 'keepdims': keepdims}
    vvx__tekzx = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', iyiuu__okjb, vvx__tekzx, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        gowd__bap = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                gowd__bap += int(bool(A[i]))
        return gowd__bap > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    iyiuu__okjb = {'axis': axis, 'out': out, 'keepdims': keepdims}
    vvx__tekzx = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', iyiuu__okjb, vvx__tekzx, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        gowd__bap = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                gowd__bap += int(bool(A[i]))
        return gowd__bap == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    iyiuu__okjb = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    vvx__tekzx = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', iyiuu__okjb, vvx__tekzx, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        dnp__kpi = np.promote_types(numba.np.numpy_support.as_dtype(A.dtype
            ), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            out_arr = np.empty(n, dnp__kpi)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(out_arr, i)
                    continue
                out_arr[i] = np_cbrt_scalar(A[i], dnp__kpi)
            return out_arr
        return impl_arr
    dnp__kpi = np.promote_types(numba.np.numpy_support.as_dtype(A), numba.
        np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, dnp__kpi)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    oycpn__crsp = x < 0
    if oycpn__crsp:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if oycpn__crsp:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    cynv__jcnr = isinstance(tup, (types.BaseTuple, types.List))
    uszzc__wdwl = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for laytl__gyjq in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                laytl__gyjq, 'numpy.hstack()')
            cynv__jcnr = cynv__jcnr and bodo.utils.utils.is_array_typ(
                laytl__gyjq, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        cynv__jcnr = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif uszzc__wdwl:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        pljx__uysl = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for laytl__gyjq in pljx__uysl.types:
            uszzc__wdwl = uszzc__wdwl and bodo.utils.utils.is_array_typ(
                laytl__gyjq, False)
    if not (cynv__jcnr or uszzc__wdwl):
        return
    if uszzc__wdwl:

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
    iyiuu__okjb = {'check_valid': check_valid, 'tol': tol}
    vvx__tekzx = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', iyiuu__okjb,
        vvx__tekzx, 'numpy')
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
        vtxdl__grjzt = mean.shape[0]
        gqcy__pip = size, vtxdl__grjzt
        nihpy__hzgz = np.random.standard_normal(gqcy__pip)
        cov = cov.astype(np.float64)
        otqr__eqqxq, s, jfd__jlcos = np.linalg.svd(cov)
        res = np.dot(nihpy__hzgz, np.sqrt(s).reshape(vtxdl__grjzt, 1) *
            jfd__jlcos)
        gwzg__nfawa = res + mean
        return gwzg__nfawa
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
            tessy__xuh = bodo.hiframes.series_kernels._get_type_max_value(arr)
            wtmbe__olf = typing.builtins.IndexValue(-1, tessy__xuh)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                upp__sgt = typing.builtins.IndexValue(i, arr[i])
                wtmbe__olf = min(wtmbe__olf, upp__sgt)
            return wtmbe__olf.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        jvkz__trwi = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            sbyw__hnvxi = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            tessy__xuh = jvkz__trwi(len(arr.dtype.categories) + 1)
            wtmbe__olf = typing.builtins.IndexValue(-1, tessy__xuh)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                upp__sgt = typing.builtins.IndexValue(i, sbyw__hnvxi[i])
                wtmbe__olf = min(wtmbe__olf, upp__sgt)
            return wtmbe__olf.index
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
            tessy__xuh = bodo.hiframes.series_kernels._get_type_min_value(arr)
            wtmbe__olf = typing.builtins.IndexValue(-1, tessy__xuh)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                upp__sgt = typing.builtins.IndexValue(i, arr[i])
                wtmbe__olf = max(wtmbe__olf, upp__sgt)
            return wtmbe__olf.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        jvkz__trwi = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            sbyw__hnvxi = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            tessy__xuh = jvkz__trwi(-1)
            wtmbe__olf = typing.builtins.IndexValue(-1, tessy__xuh)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                upp__sgt = typing.builtins.IndexValue(i, sbyw__hnvxi[i])
                wtmbe__olf = max(wtmbe__olf, upp__sgt)
            return wtmbe__olf.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
