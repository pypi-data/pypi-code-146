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
        meogs__utv = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = meogs__utv
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        meogs__utv = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = meogs__utv
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
            eur__wcj = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            eur__wcj[ind + 1] = eur__wcj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            eur__wcj = bodo.libs.array_item_arr_ext.get_offsets(arr)
            eur__wcj[ind + 1] = eur__wcj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            eur__wcj = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            eur__wcj[ind + 1] = eur__wcj[ind]
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
    ibaau__salr = arr_tup.count
    faptm__nbx = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(ibaau__salr):
        faptm__nbx += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    faptm__nbx += '  return\n'
    knce__yad = {}
    exec(faptm__nbx, {'setna': setna}, knce__yad)
    impl = knce__yad['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        zxu__bpyh = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(zxu__bpyh.start, zxu__bpyh.stop, zxu__bpyh.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        sutsm__rube = 'n'
        mlppn__kxd = 'n_pes'
        zuwx__itzwr = 'min_op'
    else:
        sutsm__rube = 'n-1, -1, -1'
        mlppn__kxd = '-1'
        zuwx__itzwr = 'max_op'
    faptm__nbx = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {mlppn__kxd}
    for i in range({sutsm__rube}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {zuwx__itzwr}))
        if possible_valid_rank != {mlppn__kxd}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    knce__yad = {}
    exec(faptm__nbx, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, knce__yad)
    impl = knce__yad['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    wrcyl__ydwcg = array_to_info(arr)
    _median_series_computation(res, wrcyl__ydwcg, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(wrcyl__ydwcg)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    wrcyl__ydwcg = array_to_info(arr)
    _autocorr_series_computation(res, wrcyl__ydwcg, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(wrcyl__ydwcg)


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
    wrcyl__ydwcg = array_to_info(arr)
    _compute_series_monotonicity(res, wrcyl__ydwcg, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(wrcyl__ydwcg)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    zge__jmnjz = res[0] > 0.5
    return zge__jmnjz


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        hlm__jdzke = '-'
        paz__dqn = 'index_arr[0] > threshhold_date'
        sutsm__rube = '1, n+1'
        obezn__djlp = 'index_arr[-i] <= threshhold_date'
        ing__dop = 'i - 1'
    else:
        hlm__jdzke = '+'
        paz__dqn = 'index_arr[-1] < threshhold_date'
        sutsm__rube = 'n'
        obezn__djlp = 'index_arr[i] >= threshhold_date'
        ing__dop = 'i'
    faptm__nbx = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        faptm__nbx += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_tz_naive_type):\n'
            )
        faptm__nbx += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            faptm__nbx += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            faptm__nbx += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            faptm__nbx += '    else:\n'
            faptm__nbx += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            faptm__nbx += (
                f'    threshhold_date = initial_date {hlm__jdzke} date_offset\n'
                )
    else:
        faptm__nbx += f'  threshhold_date = initial_date {hlm__jdzke} offset\n'
    faptm__nbx += '  local_valid = 0\n'
    faptm__nbx += f'  n = len(index_arr)\n'
    faptm__nbx += f'  if n:\n'
    faptm__nbx += f'    if {paz__dqn}:\n'
    faptm__nbx += '      loc_valid = n\n'
    faptm__nbx += '    else:\n'
    faptm__nbx += f'      for i in range({sutsm__rube}):\n'
    faptm__nbx += f'        if {obezn__djlp}:\n'
    faptm__nbx += f'          loc_valid = {ing__dop}\n'
    faptm__nbx += '          break\n'
    faptm__nbx += '  if is_parallel:\n'
    faptm__nbx += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    faptm__nbx += '    return total_valid\n'
    faptm__nbx += '  else:\n'
    faptm__nbx += '    return loc_valid\n'
    knce__yad = {}
    exec(faptm__nbx, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, knce__yad)
    return knce__yad['impl']


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
    bqw__hapwj = numba_to_c_type(sig.args[0].dtype)
    cqtq__zjv = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), bqw__hapwj))
    jnvp__wyhg = args[0]
    tcn__vqora = sig.args[0]
    if isinstance(tcn__vqora, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        jnvp__wyhg = cgutils.create_struct_proxy(tcn__vqora)(context,
            builder, jnvp__wyhg).data
        tcn__vqora = types.Array(tcn__vqora.dtype, 1, 'C')
    assert tcn__vqora.ndim == 1
    arr = make_array(tcn__vqora)(context, builder, jnvp__wyhg)
    vbk__gdl = builder.extract_value(arr.shape, 0)
    mdg__xzlcj = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        vbk__gdl, args[1], builder.load(cqtq__zjv)]
    few__eck = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    mtca__nzix = lir.FunctionType(lir.DoubleType(), few__eck)
    tzlkb__vqflp = cgutils.get_or_insert_function(builder.module,
        mtca__nzix, name='quantile_sequential')
    nww__mkjz = builder.call(tzlkb__vqflp, mdg__xzlcj)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return nww__mkjz


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, FloatingArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    bqw__hapwj = numba_to_c_type(sig.args[0].dtype)
    cqtq__zjv = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), bqw__hapwj))
    jnvp__wyhg = args[0]
    tcn__vqora = sig.args[0]
    if isinstance(tcn__vqora, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        jnvp__wyhg = cgutils.create_struct_proxy(tcn__vqora)(context,
            builder, jnvp__wyhg).data
        tcn__vqora = types.Array(tcn__vqora.dtype, 1, 'C')
    assert tcn__vqora.ndim == 1
    arr = make_array(tcn__vqora)(context, builder, jnvp__wyhg)
    vbk__gdl = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        tkmn__eon = args[2]
    else:
        tkmn__eon = vbk__gdl
    mdg__xzlcj = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        vbk__gdl, tkmn__eon, args[1], builder.load(cqtq__zjv)]
    few__eck = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType(
        64), lir.DoubleType(), lir.IntType(32)]
    mtca__nzix = lir.FunctionType(lir.DoubleType(), few__eck)
    tzlkb__vqflp = cgutils.get_or_insert_function(builder.module,
        mtca__nzix, name='quantile_parallel')
    nww__mkjz = builder.call(tzlkb__vqflp, mdg__xzlcj)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return nww__mkjz


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        n = len(arr)
        lxpfa__jkd = bodo.utils.utils.alloc_type(n, np.bool_, (-1,))
        lxpfa__jkd[0] = True
        edyn__rdlu = pd.isna(arr)
        for i in range(1, len(arr)):
            if edyn__rdlu[i] and edyn__rdlu[i - 1]:
                lxpfa__jkd[i] = False
            elif edyn__rdlu[i] or edyn__rdlu[i - 1]:
                lxpfa__jkd[i] = True
            else:
                lxpfa__jkd[i] = arr[i] != arr[i - 1]
        return lxpfa__jkd
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
    faptm__nbx = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    faptm__nbx += '  na_idxs = pd.isna(arr)\n'
    faptm__nbx += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    faptm__nbx += '  nas = sum(na_idxs)\n'
    if not ascending:
        faptm__nbx += '  if nas and nas < (sorter.size - 1):\n'
        faptm__nbx += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        faptm__nbx += '  else:\n'
        faptm__nbx += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        faptm__nbx += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    faptm__nbx += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    faptm__nbx += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        faptm__nbx += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        faptm__nbx += '    inv,\n'
        faptm__nbx += '    new_dtype=np.float64,\n'
        faptm__nbx += '    copy=True,\n'
        faptm__nbx += '    nan_to_str=False,\n'
        faptm__nbx += '    from_series=True,\n'
        faptm__nbx += '    ) + 1\n'
    else:
        faptm__nbx += '  arr = arr[sorter]\n'
        faptm__nbx += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n')
        faptm__nbx += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            faptm__nbx += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            faptm__nbx += '    dense,\n'
            faptm__nbx += '    new_dtype=np.float64,\n'
            faptm__nbx += '    copy=True,\n'
            faptm__nbx += '    nan_to_str=False,\n'
            faptm__nbx += '    from_series=True,\n'
            faptm__nbx += '  )\n'
        else:
            faptm__nbx += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            faptm__nbx += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                faptm__nbx += '  ret = count_float[dense]\n'
            elif method == 'min':
                faptm__nbx += '  ret = count_float[dense - 1] + 1\n'
            else:
                faptm__nbx += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                faptm__nbx += '  ret[na_idxs] = -1\n'
            faptm__nbx += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            faptm__nbx += '  div_val = arr.size - nas\n'
        else:
            faptm__nbx += '  div_val = arr.size\n'
        faptm__nbx += '  for i in range(len(ret)):\n'
        faptm__nbx += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        faptm__nbx += '  ret[na_idxs] = np.nan\n'
    faptm__nbx += '  return ret\n'
    knce__yad = {}
    exec(faptm__nbx, {'np': np, 'pd': pd, 'bodo': bodo}, knce__yad)
    return knce__yad['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    rlzi__cyxfc = start
    noo__omi = 2 * start + 1
    nrzhg__dea = 2 * start + 2
    if noo__omi < n and not cmp_f(arr[noo__omi], arr[rlzi__cyxfc]):
        rlzi__cyxfc = noo__omi
    if nrzhg__dea < n and not cmp_f(arr[nrzhg__dea], arr[rlzi__cyxfc]):
        rlzi__cyxfc = nrzhg__dea
    if rlzi__cyxfc != start:
        arr[start], arr[rlzi__cyxfc] = arr[rlzi__cyxfc], arr[start]
        ind_arr[start], ind_arr[rlzi__cyxfc] = ind_arr[rlzi__cyxfc], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, rlzi__cyxfc, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        pmaw__rnxn = np.empty(k, A.dtype)
        tbel__aedu = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                pmaw__rnxn[ind] = A[i]
                tbel__aedu[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            pmaw__rnxn = pmaw__rnxn[:ind]
            tbel__aedu = tbel__aedu[:ind]
        return pmaw__rnxn, tbel__aedu, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        yodj__mvzhd = np.sort(A)
        fsg__ggvww = index_arr[np.argsort(A)]
        bzj__dyaw = pd.Series(yodj__mvzhd).notna().values
        yodj__mvzhd = yodj__mvzhd[bzj__dyaw]
        fsg__ggvww = fsg__ggvww[bzj__dyaw]
        if is_largest:
            yodj__mvzhd = yodj__mvzhd[::-1]
            fsg__ggvww = fsg__ggvww[::-1]
        return np.ascontiguousarray(yodj__mvzhd), np.ascontiguousarray(
            fsg__ggvww)
    pmaw__rnxn, tbel__aedu, start = select_k_nonan(A, index_arr, m, k)
    tbel__aedu = tbel__aedu[pmaw__rnxn.argsort()]
    pmaw__rnxn.sort()
    if not is_largest:
        pmaw__rnxn = np.ascontiguousarray(pmaw__rnxn[::-1])
        tbel__aedu = np.ascontiguousarray(tbel__aedu[::-1])
    for i in range(start, m):
        if cmp_f(A[i], pmaw__rnxn[0]):
            pmaw__rnxn[0] = A[i]
            tbel__aedu[0] = index_arr[i]
            min_heapify(pmaw__rnxn, tbel__aedu, k, 0, cmp_f)
    tbel__aedu = tbel__aedu[pmaw__rnxn.argsort()]
    pmaw__rnxn.sort()
    if is_largest:
        pmaw__rnxn = pmaw__rnxn[::-1]
        tbel__aedu = tbel__aedu[::-1]
    return np.ascontiguousarray(pmaw__rnxn), np.ascontiguousarray(tbel__aedu)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    pjzy__drx = bodo.libs.distributed_api.get_rank()
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    zubeg__vrkgl, rmuy__gubvo = nlargest(A, I, k, is_largest, cmp_f)
    mfl__vyzyf = bodo.libs.distributed_api.gatherv(zubeg__vrkgl)
    tnv__wxyde = bodo.libs.distributed_api.gatherv(rmuy__gubvo)
    if pjzy__drx == MPI_ROOT:
        res, apxal__tbq = nlargest(mfl__vyzyf, tnv__wxyde, k, is_largest, cmp_f
            )
    else:
        res = np.empty(k, A.dtype)
        apxal__tbq = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(apxal__tbq)
    return res, apxal__tbq


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    rubfy__kdax, ixt__zbzv = mat.shape
    vxlz__xwil = np.empty((ixt__zbzv, ixt__zbzv), dtype=np.float64)
    for dsy__nwc in range(ixt__zbzv):
        for ejt__zzwja in range(dsy__nwc + 1):
            bdb__tpo = 0
            fensi__moua = kqnb__tdg = juldt__nmes = lyf__vzwt = 0.0
            for i in range(rubfy__kdax):
                if np.isfinite(mat[i, dsy__nwc]) and np.isfinite(mat[i,
                    ejt__zzwja]):
                    pdze__nedp = mat[i, dsy__nwc]
                    oial__mcxuw = mat[i, ejt__zzwja]
                    bdb__tpo += 1
                    juldt__nmes += pdze__nedp
                    lyf__vzwt += oial__mcxuw
            if parallel:
                bdb__tpo = bodo.libs.distributed_api.dist_reduce(bdb__tpo,
                    sum_op)
                juldt__nmes = bodo.libs.distributed_api.dist_reduce(juldt__nmes
                    , sum_op)
                lyf__vzwt = bodo.libs.distributed_api.dist_reduce(lyf__vzwt,
                    sum_op)
            if bdb__tpo < minpv:
                vxlz__xwil[dsy__nwc, ejt__zzwja] = vxlz__xwil[ejt__zzwja,
                    dsy__nwc] = np.nan
            else:
                nnxuh__gsxv = juldt__nmes / bdb__tpo
                osemj__bsfa = lyf__vzwt / bdb__tpo
                juldt__nmes = 0.0
                for i in range(rubfy__kdax):
                    if np.isfinite(mat[i, dsy__nwc]) and np.isfinite(mat[i,
                        ejt__zzwja]):
                        pdze__nedp = mat[i, dsy__nwc] - nnxuh__gsxv
                        oial__mcxuw = mat[i, ejt__zzwja] - osemj__bsfa
                        juldt__nmes += pdze__nedp * oial__mcxuw
                        fensi__moua += pdze__nedp * pdze__nedp
                        kqnb__tdg += oial__mcxuw * oial__mcxuw
                if parallel:
                    juldt__nmes = bodo.libs.distributed_api.dist_reduce(
                        juldt__nmes, sum_op)
                    fensi__moua = bodo.libs.distributed_api.dist_reduce(
                        fensi__moua, sum_op)
                    kqnb__tdg = bodo.libs.distributed_api.dist_reduce(kqnb__tdg
                        , sum_op)
                yizl__eta = bdb__tpo - 1.0 if cov else sqrt(fensi__moua *
                    kqnb__tdg)
                if yizl__eta != 0.0:
                    vxlz__xwil[dsy__nwc, ejt__zzwja] = vxlz__xwil[
                        ejt__zzwja, dsy__nwc] = juldt__nmes / yizl__eta
                else:
                    vxlz__xwil[dsy__nwc, ejt__zzwja] = vxlz__xwil[
                        ejt__zzwja, dsy__nwc] = np.nan
    return vxlz__xwil


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    nmd__bffk = n != 1
    faptm__nbx = 'def impl(data, parallel=False):\n'
    faptm__nbx += '  if parallel:\n'
    lqgb__drz = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    faptm__nbx += f'    cpp_table = arr_info_list_to_table([{lqgb__drz}])\n'
    faptm__nbx += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    tacdu__uwpv = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    faptm__nbx += f'    data = ({tacdu__uwpv},)\n'
    faptm__nbx += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    faptm__nbx += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    faptm__nbx += '    bodo.libs.array.delete_table(cpp_table)\n'
    faptm__nbx += '  n = len(data[0])\n'
    faptm__nbx += '  out = np.empty(n, np.bool_)\n'
    faptm__nbx += '  uniqs = dict()\n'
    if nmd__bffk:
        faptm__nbx += '  for i in range(n):\n'
        xrgy__svs = ', '.join(f'data[{i}][i]' for i in range(n))
        xyt__tikxw = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        faptm__nbx += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({xrgy__svs},), ({xyt__tikxw},))
"""
        faptm__nbx += '    if val in uniqs:\n'
        faptm__nbx += '      out[i] = True\n'
        faptm__nbx += '    else:\n'
        faptm__nbx += '      out[i] = False\n'
        faptm__nbx += '      uniqs[val] = 0\n'
    else:
        faptm__nbx += '  data = data[0]\n'
        faptm__nbx += '  hasna = False\n'
        faptm__nbx += '  for i in range(n):\n'
        faptm__nbx += '    if bodo.libs.array_kernels.isna(data, i):\n'
        faptm__nbx += '      out[i] = hasna\n'
        faptm__nbx += '      hasna = True\n'
        faptm__nbx += '    else:\n'
        faptm__nbx += '      val = data[i]\n'
        faptm__nbx += '      if val in uniqs:\n'
        faptm__nbx += '        out[i] = True\n'
        faptm__nbx += '      else:\n'
        faptm__nbx += '        out[i] = False\n'
        faptm__nbx += '        uniqs[val] = 0\n'
    faptm__nbx += '  if parallel:\n'
    faptm__nbx += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    faptm__nbx += '  return out\n'
    knce__yad = {}
    exec(faptm__nbx, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        knce__yad)
    impl = knce__yad['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    pass


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    ibaau__salr = len(data)
    faptm__nbx = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    faptm__nbx += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        ibaau__salr)))
    faptm__nbx += '  table_total = arr_info_list_to_table(info_list_total)\n'
    faptm__nbx += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(ibaau__salr))
    for tngf__mqn in range(ibaau__salr):
        faptm__nbx += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(tngf__mqn, tngf__mqn, tngf__mqn))
    faptm__nbx += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(ibaau__salr))
    faptm__nbx += '  delete_table(out_table)\n'
    faptm__nbx += '  delete_table(table_total)\n'
    faptm__nbx += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(ibaau__salr)))
    knce__yad = {}
    exec(faptm__nbx, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, knce__yad)
    impl = knce__yad['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    pass


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    ibaau__salr = len(data)
    faptm__nbx = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    faptm__nbx += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        ibaau__salr)))
    faptm__nbx += '  table_total = arr_info_list_to_table(info_list_total)\n'
    faptm__nbx += '  keep_i = 0\n'
    faptm__nbx += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for tngf__mqn in range(ibaau__salr):
        faptm__nbx += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(tngf__mqn, tngf__mqn, tngf__mqn))
    faptm__nbx += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(ibaau__salr))
    faptm__nbx += '  delete_table(out_table)\n'
    faptm__nbx += '  delete_table(table_total)\n'
    faptm__nbx += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(ibaau__salr)))
    knce__yad = {}
    exec(faptm__nbx, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, knce__yad)
    impl = knce__yad['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    pass


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        eqvk__zopih = [array_to_info(data_arr)]
        nsjyu__ayp = arr_info_list_to_table(eqvk__zopih)
        oww__feumx = 0
        crckm__zhsp = drop_duplicates_table(nsjyu__ayp, parallel, 1,
            oww__feumx, False, True)
        out_arr = info_to_array(info_from_table(crckm__zhsp, 0), data_arr)
        delete_table(crckm__zhsp)
        delete_table(nsjyu__ayp)
        return out_arr
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    pass


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    vdk__igyo = len(data.types)
    crbx__attyj = [('out' + str(i)) for i in range(vdk__igyo)]
    xrb__uhmtc = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    txo__chv = ['isna(data[{}], i)'.format(i) for i in xrb__uhmtc]
    ytogd__watrs = 'not ({})'.format(' or '.join(txo__chv))
    if not is_overload_none(thresh):
        ytogd__watrs = '(({}) <= ({}) - thresh)'.format(' + '.join(txo__chv
            ), vdk__igyo - 1)
    elif how == 'all':
        ytogd__watrs = 'not ({})'.format(' and '.join(txo__chv))
    faptm__nbx = 'def _dropna_imp(data, how, thresh, subset):\n'
    faptm__nbx += '  old_len = len(data[0])\n'
    faptm__nbx += '  new_len = 0\n'
    faptm__nbx += '  for i in range(old_len):\n'
    faptm__nbx += '    if {}:\n'.format(ytogd__watrs)
    faptm__nbx += '      new_len += 1\n'
    for i, out in enumerate(crbx__attyj):
        if isinstance(data[i], bodo.CategoricalArrayType):
            faptm__nbx += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            faptm__nbx += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    faptm__nbx += '  curr_ind = 0\n'
    faptm__nbx += '  for i in range(old_len):\n'
    faptm__nbx += '    if {}:\n'.format(ytogd__watrs)
    for i in range(vdk__igyo):
        faptm__nbx += '      if isna(data[{}], i):\n'.format(i)
        faptm__nbx += '        setna({}, curr_ind)\n'.format(crbx__attyj[i])
        faptm__nbx += '      else:\n'
        faptm__nbx += '        {}[curr_ind] = data[{}][i]\n'.format(crbx__attyj
            [i], i)
    faptm__nbx += '      curr_ind += 1\n'
    faptm__nbx += '  return {}\n'.format(', '.join(crbx__attyj))
    knce__yad = {}
    tplm__bmj = {'t{}'.format(i): htl__hje for i, htl__hje in enumerate(
        data.types)}
    tplm__bmj.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(faptm__nbx, tplm__bmj, knce__yad)
    aev__oktdb = knce__yad['_dropna_imp']
    return aev__oktdb


def get(arr, ind):
    pass


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        tcn__vqora = arr.dtype
        fud__bfv = tcn__vqora.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            jiu__zcyr = init_nested_counts(fud__bfv)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                jiu__zcyr = add_nested_counts(jiu__zcyr, val[ind])
            out_arr = bodo.utils.utils.alloc_type(n, tcn__vqora, jiu__zcyr)
            for nvv__wrxir in range(n):
                if bodo.libs.array_kernels.isna(arr, nvv__wrxir):
                    setna(out_arr, nvv__wrxir)
                    continue
                val = arr[nvv__wrxir]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(out_arr, nvv__wrxir)
                    continue
                out_arr[nvv__wrxir] = val[ind]
            return out_arr
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    hfw__zrecq = _to_readonly(arr_types.types[0])
    return all(isinstance(htl__hje, CategoricalArrayType) and _to_readonly(
        htl__hje) == hfw__zrecq for htl__hje in arr_types.types)


def concat(arr_list):
    pass


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        bsu__uunx = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            sin__web = 0
            men__rmd = []
            for A in arr_list:
                xyv__kiwvi = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                men__rmd.append(bodo.libs.array_item_arr_ext.get_data(A))
                sin__web += xyv__kiwvi
            rkbjs__xxf = np.empty(sin__web + 1, offset_type)
            jloa__wssc = bodo.libs.array_kernels.concat(men__rmd)
            osyqd__nfljh = np.empty(sin__web + 7 >> 3, np.uint8)
            pcy__pzh = 0
            vtidy__vlycu = 0
            for A in arr_list:
                hnjy__waty = bodo.libs.array_item_arr_ext.get_offsets(A)
                rrnfp__ykpo = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                xyv__kiwvi = len(A)
                geb__kyfg = hnjy__waty[xyv__kiwvi]
                for i in range(xyv__kiwvi):
                    rkbjs__xxf[i + pcy__pzh] = hnjy__waty[i] + vtidy__vlycu
                    ixjd__stmvf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        rrnfp__ykpo, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(osyqd__nfljh, i +
                        pcy__pzh, ixjd__stmvf)
                pcy__pzh += xyv__kiwvi
                vtidy__vlycu += geb__kyfg
            rkbjs__xxf[pcy__pzh] = vtidy__vlycu
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                sin__web, jloa__wssc, rkbjs__xxf, osyqd__nfljh)
            return out_arr
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        vsvx__pghx = arr_list.dtype.names
        faptm__nbx = 'def struct_array_concat_impl(arr_list):\n'
        faptm__nbx += f'    n_all = 0\n'
        for i in range(len(vsvx__pghx)):
            faptm__nbx += f'    concat_list{i} = []\n'
        faptm__nbx += '    for A in arr_list:\n'
        faptm__nbx += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(vsvx__pghx)):
            faptm__nbx += f'        concat_list{i}.append(data_tuple[{i}])\n'
        faptm__nbx += '        n_all += len(A)\n'
        faptm__nbx += '    n_bytes = (n_all + 7) >> 3\n'
        faptm__nbx += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        faptm__nbx += '    curr_bit = 0\n'
        faptm__nbx += '    for A in arr_list:\n'
        faptm__nbx += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        faptm__nbx += '        for j in range(len(A)):\n'
        faptm__nbx += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        faptm__nbx += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        faptm__nbx += '            curr_bit += 1\n'
        faptm__nbx += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        oez__nvr = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(vsvx__pghx))])
        faptm__nbx += f'        ({oez__nvr},),\n'
        faptm__nbx += '        new_mask,\n'
        faptm__nbx += f'        {vsvx__pghx},\n'
        faptm__nbx += '    )\n'
        knce__yad = {}
        exec(faptm__nbx, {'bodo': bodo, 'np': np}, knce__yad)
        return knce__yad['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.DatetimeArrayType):
        xpk__ujzq = arr_list.dtype.tz

        def tz_aware_concat_impl(arr_list):
            aat__ynl = 0
            for A in arr_list:
                aat__ynl += len(A)
            ilf__htnq = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(
                aat__ynl, xpk__ujzq)
            bnykj__bjwcr = 0
            for A in arr_list:
                for i in range(len(A)):
                    ilf__htnq[i + bnykj__bjwcr] = A[i]
                bnykj__bjwcr += len(A)
            return ilf__htnq
        return tz_aware_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            aat__ynl = 0
            for A in arr_list:
                aat__ynl += len(A)
            ilf__htnq = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(aat__ynl))
            bnykj__bjwcr = 0
            for A in arr_list:
                for i in range(len(A)):
                    ilf__htnq._data[i + bnykj__bjwcr] = A._data[i]
                    ixjd__stmvf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ilf__htnq.
                        _null_bitmap, i + bnykj__bjwcr, ixjd__stmvf)
                bnykj__bjwcr += len(A)
            return ilf__htnq
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            aat__ynl = 0
            for A in arr_list:
                aat__ynl += len(A)
            ilf__htnq = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(aat__ynl))
            bnykj__bjwcr = 0
            for A in arr_list:
                for i in range(len(A)):
                    ilf__htnq._days_data[i + bnykj__bjwcr] = A._days_data[i]
                    ilf__htnq._seconds_data[i + bnykj__bjwcr
                        ] = A._seconds_data[i]
                    ilf__htnq._microseconds_data[i + bnykj__bjwcr
                        ] = A._microseconds_data[i]
                    ixjd__stmvf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ilf__htnq.
                        _null_bitmap, i + bnykj__bjwcr, ixjd__stmvf)
                bnykj__bjwcr += len(A)
            return ilf__htnq
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        lsp__rqne = arr_list.dtype.precision
        cxbhv__kze = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            aat__ynl = 0
            for A in arr_list:
                aat__ynl += len(A)
            ilf__htnq = bodo.libs.decimal_arr_ext.alloc_decimal_array(aat__ynl,
                lsp__rqne, cxbhv__kze)
            bnykj__bjwcr = 0
            for A in arr_list:
                for i in range(len(A)):
                    ilf__htnq._data[i + bnykj__bjwcr] = A._data[i]
                    ixjd__stmvf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ilf__htnq.
                        _null_bitmap, i + bnykj__bjwcr, ixjd__stmvf)
                bnykj__bjwcr += len(A)
            return ilf__htnq
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        htl__hje) for htl__hje in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            evuee__nzpgt = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    evuee__nzpgt = arr_list.types[i]
                    break
        else:
            evuee__nzpgt = arr_list.dtype
        if evuee__nzpgt == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                wknj__xul = 0
                qee__gegvw = 0
                vggl__gyli = 0
                for A in arr_list:
                    data_arr = A._data
                    edzbn__ftxm = A._indices
                    vggl__gyli += len(edzbn__ftxm)
                    wknj__xul += len(data_arr)
                    qee__gegvw += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                vzuly__rqtk = pre_alloc_string_array(wknj__xul, qee__gegvw)
                gtfax__ibfx = bodo.libs.int_arr_ext.alloc_int_array(vggl__gyli,
                    np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(vzuly__rqtk, -1)
                cyk__jkhb = 0
                ffl__teevi = 0
                jexiy__jnbxx = 0
                for A in arr_list:
                    data_arr = A._data
                    edzbn__ftxm = A._indices
                    vggl__gyli = len(edzbn__ftxm)
                    bodo.libs.str_arr_ext.set_string_array_range(vzuly__rqtk,
                        data_arr, cyk__jkhb, ffl__teevi)
                    for i in range(vggl__gyli):
                        if bodo.libs.array_kernels.isna(edzbn__ftxm, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            edzbn__ftxm[i]):
                            bodo.libs.array_kernels.setna(gtfax__ibfx, 
                                jexiy__jnbxx + i)
                        else:
                            gtfax__ibfx[jexiy__jnbxx + i
                                ] = cyk__jkhb + edzbn__ftxm[i]
                    cyk__jkhb += len(data_arr)
                    ffl__teevi += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                    jexiy__jnbxx += vggl__gyli
                out_arr = init_dict_arr(vzuly__rqtk, gtfax__ibfx, False, False)
                ugrm__sux = drop_duplicates_local_dictionary(out_arr, False)
                return ugrm__sux
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            wknj__xul = 0
            qee__gegvw = 0
            for A in arr_list:
                arr = A
                wknj__xul += len(arr)
                qee__gegvw += bodo.libs.str_arr_ext.num_total_chars(arr)
            out_arr = bodo.utils.utils.alloc_type(wknj__xul, evuee__nzpgt,
                (qee__gegvw,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)
            cyk__jkhb = 0
            ffl__teevi = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(out_arr, arr,
                    cyk__jkhb, ffl__teevi)
                cyk__jkhb += len(arr)
                ffl__teevi += bodo.libs.str_arr_ext.num_total_chars(arr)
            return out_arr
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(htl__hje.dtype, types.Integer) for
        htl__hje in arr_list.types) and any(isinstance(htl__hje,
        IntegerArrayType) for htl__hje in arr_list.types):

        def impl_int_arr_list(arr_list):
            crpoy__brfov = convert_to_nullable_tup(arr_list)
            tpyu__ryox = []
            xeis__sfnl = 0
            for A in crpoy__brfov:
                tpyu__ryox.append(A._data)
                xeis__sfnl += len(A)
            jloa__wssc = bodo.libs.array_kernels.concat(tpyu__ryox)
            eyjd__xczrv = xeis__sfnl + 7 >> 3
            hnsj__ooz = np.empty(eyjd__xczrv, np.uint8)
            nxld__emqr = 0
            for A in crpoy__brfov:
                gbh__etp = A._null_bitmap
                for nvv__wrxir in range(len(A)):
                    ixjd__stmvf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        gbh__etp, nvv__wrxir)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hnsj__ooz,
                        nxld__emqr, ixjd__stmvf)
                    nxld__emqr += 1
            return bodo.libs.int_arr_ext.init_integer_array(jloa__wssc,
                hnsj__ooz)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(htl__hje.dtype == types.bool_ for htl__hje in
        arr_list.types) and any(htl__hje == boolean_array for htl__hje in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            crpoy__brfov = convert_to_nullable_tup(arr_list)
            tpyu__ryox = []
            xeis__sfnl = 0
            for A in crpoy__brfov:
                tpyu__ryox.append(A._data)
                xeis__sfnl += len(A)
            jloa__wssc = bodo.libs.array_kernels.concat(tpyu__ryox)
            eyjd__xczrv = xeis__sfnl + 7 >> 3
            hnsj__ooz = np.empty(eyjd__xczrv, np.uint8)
            nxld__emqr = 0
            for A in crpoy__brfov:
                gbh__etp = A._null_bitmap
                for nvv__wrxir in range(len(A)):
                    ixjd__stmvf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        gbh__etp, nvv__wrxir)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hnsj__ooz,
                        nxld__emqr, ixjd__stmvf)
                    nxld__emqr += 1
            return bodo.libs.bool_arr_ext.init_bool_array(jloa__wssc, hnsj__ooz
                )
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, FloatingArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(htl__hje.dtype, types.Float) for
        htl__hje in arr_list.types) and any(isinstance(htl__hje,
        FloatingArrayType) for htl__hje in arr_list.types):

        def impl_float_arr_list(arr_list):
            crpoy__brfov = convert_to_nullable_tup(arr_list)
            tpyu__ryox = []
            xeis__sfnl = 0
            for A in crpoy__brfov:
                tpyu__ryox.append(A._data)
                xeis__sfnl += len(A)
            jloa__wssc = bodo.libs.array_kernels.concat(tpyu__ryox)
            eyjd__xczrv = xeis__sfnl + 7 >> 3
            hnsj__ooz = np.empty(eyjd__xczrv, np.uint8)
            nxld__emqr = 0
            for A in crpoy__brfov:
                gbh__etp = A._null_bitmap
                for nvv__wrxir in range(len(A)):
                    ixjd__stmvf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        gbh__etp, nvv__wrxir)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hnsj__ooz,
                        nxld__emqr, ixjd__stmvf)
                    nxld__emqr += 1
            return bodo.libs.float_arr_ext.init_float_array(jloa__wssc,
                hnsj__ooz)
        return impl_float_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            dpqty__foa = []
            for A in arr_list:
                dpqty__foa.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                dpqty__foa), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        aba__eeh = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        faptm__nbx = 'def impl(arr_list):\n'
        faptm__nbx += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({aba__eeh}, )), arr_list[0].dtype)
"""
        hnbr__fdmik = {}
        exec(faptm__nbx, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, hnbr__fdmik)
        return hnbr__fdmik['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            xeis__sfnl = 0
            for A in arr_list:
                xeis__sfnl += len(A)
            out_arr = np.empty(xeis__sfnl, dtype)
            ekzkr__fsbeb = 0
            for A in arr_list:
                n = len(A)
                out_arr[ekzkr__fsbeb:ekzkr__fsbeb + n] = A
                ekzkr__fsbeb += n
            return out_arr
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(htl__hje, (
        types.Array, IntegerArrayType)) and isinstance(htl__hje.dtype,
        types.Integer) for htl__hje in arr_list.types) and any(isinstance(
        htl__hje, types.Array) and isinstance(htl__hje.dtype, types.Float) for
        htl__hje in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            jgpa__xtofj = []
            for A in arr_list:
                jgpa__xtofj.append(A._data)
            fwut__bvzd = bodo.libs.array_kernels.concat(jgpa__xtofj)
            vxlz__xwil = bodo.libs.map_arr_ext.init_map_arr(fwut__bvzd)
            return vxlz__xwil
        return impl_map_arr_list
    if isinstance(arr_list, types.Tuple):
        lxf__wzwp = all([(isinstance(uobrj__lfxi, bodo.DatetimeArrayType) or
            isinstance(uobrj__lfxi, types.Array) and uobrj__lfxi.dtype ==
            bodo.datetime64ns) for uobrj__lfxi in arr_list.types])
        if lxf__wzwp:
            raise BodoError(
                f'Cannot concatenate the rows of Timestamp data with different timezones. Found types: {arr_list}. Please use pd.Series.tz_convert(None) to remove Timezone information.'
                )
    for uobrj__lfxi in arr_list:
        if not isinstance(uobrj__lfxi, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(htl__hje.astype(np.float64) for htl__hje in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    ibaau__salr = len(arr_tup.types)
    faptm__nbx = 'def f(arr_tup):\n'
    faptm__nbx += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        ibaau__salr)), ',' if ibaau__salr == 1 else '')
    knce__yad = {}
    exec(faptm__nbx, {'np': np}, knce__yad)
    dds__dhv = knce__yad['f']
    return dds__dhv


def convert_to_nullable_tup(arr_tup):
    pass


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, FloatingArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple
        ), 'convert_to_nullable_tup: tuple expected'
    ibaau__salr = len(arr_tup.types)
    jkh__aqq = find_common_np_dtype(arr_tup.types)
    fud__bfv = None
    jzhx__uvlxn = ''
    if isinstance(jkh__aqq, types.Integer):
        fud__bfv = bodo.libs.int_arr_ext.IntDtype(jkh__aqq)
        jzhx__uvlxn = '.astype(out_dtype, False)'
    if isinstance(jkh__aqq, types.Float
        ) and bodo.libs.float_arr_ext._use_nullable_float:
        fud__bfv = bodo.libs.float_arr_ext.FloatDtype(jkh__aqq)
        jzhx__uvlxn = '.astype(out_dtype, False)'
    faptm__nbx = 'def f(arr_tup):\n'
    faptm__nbx += '  return ({}{})\n'.format(','.join(
        f'bodo.utils.conversion.coerce_to_array(arr_tup[{i}], use_nullable_array=True){jzhx__uvlxn}'
         for i in range(ibaau__salr)), ',' if ibaau__salr == 1 else '')
    knce__yad = {}
    exec(faptm__nbx, {'bodo': bodo, 'out_dtype': fud__bfv}, knce__yad)
    vwat__zvtc = knce__yad['f']
    return vwat__zvtc


def nunique(A, dropna):
    pass


def nunique_parallel(A, dropna):
    pass


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, jfkmu__pmuel = build_set_seen_na(A)
        return len(s) + int(not dropna and jfkmu__pmuel)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        tae__qia = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        fmlhc__mkjdg = len(tae__qia)
        return bodo.libs.distributed_api.dist_reduce(fmlhc__mkjdg, np.int32
            (sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    pass


def accum_func(A, func_name, parallel=False):
    pass


@overload(accum_func, no_unliteral=True)
def accum_func_overload(A, func_name, parallel=False):
    assert is_overload_constant_str(func_name
        ), 'accum_func: func_name should be const'
    coyp__jkraz = get_overload_const_str(func_name)
    assert coyp__jkraz in ('cumsum', 'cumprod', 'cummin', 'cummax'
        ), 'accum_func: invalid func_name'
    if coyp__jkraz == 'cumsum':
        znl__culf = A.dtype(0)
        eriq__eiwh = np.int32(Reduce_Type.Sum.value)
        fwyk__jasj = np.add
    if coyp__jkraz == 'cumprod':
        znl__culf = A.dtype(1)
        eriq__eiwh = np.int32(Reduce_Type.Prod.value)
        fwyk__jasj = np.multiply
    if coyp__jkraz == 'cummin':
        if isinstance(A.dtype, types.Float):
            znl__culf = np.finfo(A.dtype(1).dtype).max
        else:
            znl__culf = np.iinfo(A.dtype(1).dtype).max
        eriq__eiwh = np.int32(Reduce_Type.Min.value)
        fwyk__jasj = min
    if coyp__jkraz == 'cummax':
        if isinstance(A.dtype, types.Float):
            znl__culf = np.finfo(A.dtype(1).dtype).min
        else:
            znl__culf = np.iinfo(A.dtype(1).dtype).min
        eriq__eiwh = np.int32(Reduce_Type.Max.value)
        fwyk__jasj = max
    fpx__mmmvk = A

    def impl(A, func_name, parallel=False):
        n = len(A)
        ivvd__jha = znl__culf
        if parallel:
            for i in range(n):
                if not bodo.libs.array_kernels.isna(A, i):
                    ivvd__jha = fwyk__jasj(ivvd__jha, A[i])
            ivvd__jha = bodo.libs.distributed_api.dist_exscan(ivvd__jha,
                eriq__eiwh)
            if bodo.get_rank() == 0:
                ivvd__jha = znl__culf
        out_arr = bodo.utils.utils.alloc_type(n, fpx__mmmvk, (-1,))
        for i in range(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(out_arr, i)
                continue
            ivvd__jha = fwyk__jasj(ivvd__jha, A[i])
            out_arr[i] = ivvd__jha
        return out_arr
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        avflx__rahzp = arr_info_list_to_table([array_to_info(A)])
        szjt__ddesj = 1
        oww__feumx = 0
        crckm__zhsp = drop_duplicates_table(avflx__rahzp, parallel,
            szjt__ddesj, oww__feumx, dropna, True)
        out_arr = info_to_array(info_from_table(crckm__zhsp, 0), A)
        delete_table(avflx__rahzp)
        delete_table(crckm__zhsp)
        return out_arr
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    bsu__uunx = bodo.utils.typing.to_nullable_type(arr.dtype)
    efng__qwn = index_arr
    yteim__uzrvs = efng__qwn.dtype

    def impl(arr, index_arr):
        n = len(arr)
        jiu__zcyr = init_nested_counts(bsu__uunx)
        wwela__izot = init_nested_counts(yteim__uzrvs)
        for i in range(n):
            wyrjx__yybe = index_arr[i]
            if isna(arr, i):
                jiu__zcyr = (jiu__zcyr[0] + 1,) + jiu__zcyr[1:]
                wwela__izot = add_nested_counts(wwela__izot, wyrjx__yybe)
                continue
            jzi__kzkkt = arr[i]
            if len(jzi__kzkkt) == 0:
                jiu__zcyr = (jiu__zcyr[0] + 1,) + jiu__zcyr[1:]
                wwela__izot = add_nested_counts(wwela__izot, wyrjx__yybe)
                continue
            jiu__zcyr = add_nested_counts(jiu__zcyr, jzi__kzkkt)
            for afls__vpcgh in range(len(jzi__kzkkt)):
                wwela__izot = add_nested_counts(wwela__izot, wyrjx__yybe)
        out_arr = bodo.utils.utils.alloc_type(jiu__zcyr[0], bsu__uunx,
            jiu__zcyr[1:])
        febs__bbkgz = bodo.utils.utils.alloc_type(jiu__zcyr[0], efng__qwn,
            wwela__izot)
        vtidy__vlycu = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, vtidy__vlycu)
                febs__bbkgz[vtidy__vlycu] = index_arr[i]
                vtidy__vlycu += 1
                continue
            jzi__kzkkt = arr[i]
            geb__kyfg = len(jzi__kzkkt)
            if geb__kyfg == 0:
                setna(out_arr, vtidy__vlycu)
                febs__bbkgz[vtidy__vlycu] = index_arr[i]
                vtidy__vlycu += 1
                continue
            out_arr[vtidy__vlycu:vtidy__vlycu + geb__kyfg] = jzi__kzkkt
            febs__bbkgz[vtidy__vlycu:vtidy__vlycu + geb__kyfg] = index_arr[i]
            vtidy__vlycu += geb__kyfg
        return out_arr, febs__bbkgz
    return impl


def explode_no_index(arr):
    pass


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    bsu__uunx = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        jiu__zcyr = init_nested_counts(bsu__uunx)
        for i in range(n):
            if isna(arr, i):
                jiu__zcyr = (jiu__zcyr[0] + 1,) + jiu__zcyr[1:]
                ycqv__kwf = 1
            else:
                jzi__kzkkt = arr[i]
                uxlj__oucim = len(jzi__kzkkt)
                if uxlj__oucim == 0:
                    jiu__zcyr = (jiu__zcyr[0] + 1,) + jiu__zcyr[1:]
                    ycqv__kwf = 1
                    continue
                else:
                    jiu__zcyr = add_nested_counts(jiu__zcyr, jzi__kzkkt)
                    ycqv__kwf = uxlj__oucim
            if counts[i] != ycqv__kwf:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        out_arr = bodo.utils.utils.alloc_type(jiu__zcyr[0], bsu__uunx,
            jiu__zcyr[1:])
        vtidy__vlycu = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, vtidy__vlycu)
                vtidy__vlycu += 1
                continue
            jzi__kzkkt = arr[i]
            geb__kyfg = len(jzi__kzkkt)
            if geb__kyfg == 0:
                setna(out_arr, vtidy__vlycu)
                vtidy__vlycu += 1
                continue
            out_arr[vtidy__vlycu:vtidy__vlycu + geb__kyfg] = jzi__kzkkt
            vtidy__vlycu += geb__kyfg
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
        gtn__yihy = 'np.empty(n, np.int64)'
        abf__jwx = 'out_arr[i] = 1'
        tecox__xeise = 'max(len(arr[i]), 1)'
    else:
        gtn__yihy = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        abf__jwx = 'bodo.libs.array_kernels.setna(out_arr, i)'
        tecox__xeise = 'len(arr[i])'
    faptm__nbx = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {gtn__yihy}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {abf__jwx}
        else:
            out_arr[i] = {tecox__xeise}
    return out_arr
    """
    knce__yad = {}
    exec(faptm__nbx, {'bodo': bodo, 'numba': numba, 'np': np}, knce__yad)
    impl = knce__yad['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    pass


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    efng__qwn = index_arr
    yteim__uzrvs = efng__qwn.dtype

    def impl(arr, pat, n, index_arr):
        pxnfp__wsz = pat is not None and len(pat) > 1
        if pxnfp__wsz:
            ihfkv__jnem = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        pzoaz__kvjdn = len(arr)
        wknj__xul = 0
        qee__gegvw = 0
        wwela__izot = init_nested_counts(yteim__uzrvs)
        for i in range(pzoaz__kvjdn):
            wyrjx__yybe = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                wknj__xul += 1
                wwela__izot = add_nested_counts(wwela__izot, wyrjx__yybe)
                continue
            if pxnfp__wsz:
                bcy__tcz = ihfkv__jnem.split(arr[i], maxsplit=n)
            else:
                bcy__tcz = arr[i].split(pat, n)
            wknj__xul += len(bcy__tcz)
            for s in bcy__tcz:
                wwela__izot = add_nested_counts(wwela__izot, wyrjx__yybe)
                qee__gegvw += bodo.libs.str_arr_ext.get_utf8_size(s)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(wknj__xul,
            qee__gegvw)
        febs__bbkgz = bodo.utils.utils.alloc_type(wknj__xul, efng__qwn,
            wwela__izot)
        nmw__hco = 0
        for nvv__wrxir in range(pzoaz__kvjdn):
            if isna(arr, nvv__wrxir):
                out_arr[nmw__hco] = ''
                bodo.libs.array_kernels.setna(out_arr, nmw__hco)
                febs__bbkgz[nmw__hco] = index_arr[nvv__wrxir]
                nmw__hco += 1
                continue
            if pxnfp__wsz:
                bcy__tcz = ihfkv__jnem.split(arr[nvv__wrxir], maxsplit=n)
            else:
                bcy__tcz = arr[nvv__wrxir].split(pat, n)
            nczj__qdvm = len(bcy__tcz)
            out_arr[nmw__hco:nmw__hco + nczj__qdvm] = bcy__tcz
            febs__bbkgz[nmw__hco:nmw__hco + nczj__qdvm] = index_arr[nvv__wrxir]
            nmw__hco += nczj__qdvm
        return out_arr, febs__bbkgz
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
            ltv__qqz = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            kyedl__ihubx = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(kyedl__ihubx, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(ltv__qqz,
                kyedl__ihubx, True, True)
        return impl_dict
    ejlpw__orqdx = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        out_arr = bodo.utils.utils.alloc_type(n, ejlpw__orqdx, (0,))
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
    ywg__mnlg = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            out_arr = bodo.utils.utils.alloc_type(new_len, ywg__mnlg)
            bodo.libs.str_arr_ext.str_copy_ptr(out_arr.ctypes, 0, A.ctypes,
                old_size)
            return out_arr
        return impl_char

    def impl(A, old_size, new_len):
        out_arr = bodo.utils.utils.alloc_type(new_len, ywg__mnlg, (-1,))
        out_arr[:old_size] = A[:old_size]
        return out_arr
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    qklfv__cczu = math.ceil((stop - start) / step)
    return int(max(qklfv__cczu, 0))


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
    if any(isinstance(wuwe__cbfoq, types.Complex) for wuwe__cbfoq in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            zjy__rmknk = (stop - start) / step
            qklfv__cczu = math.ceil(zjy__rmknk.real)
            ypt__wke = math.ceil(zjy__rmknk.imag)
            jlcl__zhawf = int(max(min(ypt__wke, qklfv__cczu), 0))
            arr = np.empty(jlcl__zhawf, dtype)
            for i in numba.parfors.parfor.internal_prange(jlcl__zhawf):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            jlcl__zhawf = bodo.libs.array_kernels.calc_nitems(start, stop, step
                )
            arr = np.empty(jlcl__zhawf, dtype)
            for i in numba.parfors.parfor.internal_prange(jlcl__zhawf):
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
        khwq__tlym = arr,
        if not inplace:
            khwq__tlym = arr.copy(),
        ouxyt__feaq = bodo.libs.str_arr_ext.to_list_if_immutable_arr(khwq__tlym
            )
        azdd__jvs = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(ouxyt__feaq, 0, n, azdd__jvs)
        if not ascending:
            bodo.libs.timsort.reverseRange(ouxyt__feaq, 0, n, azdd__jvs)
        bodo.libs.str_arr_ext.cp_str_list_to_array(khwq__tlym, ouxyt__feaq)
        return khwq__tlym[0]
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
        vxlz__xwil = []
        for i in range(n):
            if A[i]:
                vxlz__xwil.append(i + offset)
        return np.array(vxlz__xwil, np.int64),
    return impl


def ffill_bfill_arr(arr):
    pass


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    ywg__mnlg = element_type(A)
    if ywg__mnlg == types.unicode_type:
        null_value = '""'
    elif ywg__mnlg == types.bool_:
        null_value = 'False'
    elif ywg__mnlg == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_datetime(0))'
            )
    elif ywg__mnlg == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_timedelta(0))'
            )
    else:
        null_value = '0'
    nmw__hco = 'i'
    dmuj__eohmm = False
    cjmgu__njpk = get_overload_const_str(method)
    if cjmgu__njpk in ('ffill', 'pad'):
        wygm__mkk = 'n'
        send_right = True
    elif cjmgu__njpk in ('backfill', 'bfill'):
        wygm__mkk = 'n-1, -1, -1'
        send_right = False
        if ywg__mnlg == types.unicode_type:
            nmw__hco = '(n - 1) - i'
            dmuj__eohmm = True
    faptm__nbx = 'def impl(A, method, parallel=False):\n'
    faptm__nbx += '  A = decode_if_dict_array(A)\n'
    faptm__nbx += '  has_last_value = False\n'
    faptm__nbx += f'  last_value = {null_value}\n'
    faptm__nbx += '  if parallel:\n'
    faptm__nbx += '    rank = bodo.libs.distributed_api.get_rank()\n'
    faptm__nbx += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    faptm__nbx += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    faptm__nbx += '  n = len(A)\n'
    faptm__nbx += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    faptm__nbx += f'  for i in range({wygm__mkk}):\n'
    faptm__nbx += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    faptm__nbx += f'      bodo.libs.array_kernels.setna(out_arr, {nmw__hco})\n'
    faptm__nbx += '      continue\n'
    faptm__nbx += '    s = A[i]\n'
    faptm__nbx += '    if bodo.libs.array_kernels.isna(A, i):\n'
    faptm__nbx += '      s = last_value\n'
    faptm__nbx += f'    out_arr[{nmw__hco}] = s\n'
    faptm__nbx += '    last_value = s\n'
    faptm__nbx += '    has_last_value = True\n'
    if dmuj__eohmm:
        faptm__nbx += '  return out_arr[::-1]\n'
    else:
        faptm__nbx += '  return out_arr\n'
    lier__zvubv = {}
    exec(faptm__nbx, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, lier__zvubv)
    impl = lier__zvubv['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        oyw__roo = 0
        egoew__lctrn = n_pes - 1
        xkm__qsb = np.int32(rank + 1)
        wvqgm__xrkyu = np.int32(rank - 1)
        qhjfw__tnm = len(in_arr) - 1
        kbly__qbetk = -1
        uemat__nmb = -1
    else:
        oyw__roo = n_pes - 1
        egoew__lctrn = 0
        xkm__qsb = np.int32(rank - 1)
        wvqgm__xrkyu = np.int32(rank + 1)
        qhjfw__tnm = 0
        kbly__qbetk = len(in_arr)
        uemat__nmb = 1
    myjc__iuvrt = np.int32(bodo.hiframes.rolling.comm_border_tag)
    loub__gbux = np.empty(1, dtype=np.bool_)
    fmbgb__nbe = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    jmotw__jeu = np.empty(1, dtype=np.bool_)
    lngcv__jztev = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    dvbq__bng = False
    uzqc__hcu = null_value
    for i in range(qhjfw__tnm, kbly__qbetk, uemat__nmb):
        if not isna(in_arr, i):
            dvbq__bng = True
            uzqc__hcu = in_arr[i]
            break
    if rank != oyw__roo:
        zbd__ngy = bodo.libs.distributed_api.irecv(loub__gbux, 1,
            wvqgm__xrkyu, myjc__iuvrt, True)
        bodo.libs.distributed_api.wait(zbd__ngy, True)
        viqtd__grii = bodo.libs.distributed_api.irecv(fmbgb__nbe, 1,
            wvqgm__xrkyu, myjc__iuvrt, True)
        bodo.libs.distributed_api.wait(viqtd__grii, True)
        gsdx__pncc = loub__gbux[0]
        ybvi__skdl = fmbgb__nbe[0]
    else:
        gsdx__pncc = False
        ybvi__skdl = null_value
    if dvbq__bng:
        jmotw__jeu[0] = dvbq__bng
        lngcv__jztev[0] = uzqc__hcu
    else:
        jmotw__jeu[0] = gsdx__pncc
        lngcv__jztev[0] = ybvi__skdl
    if rank != egoew__lctrn:
        xdhi__heca = bodo.libs.distributed_api.isend(jmotw__jeu, 1,
            xkm__qsb, myjc__iuvrt, True)
        orefm__oal = bodo.libs.distributed_api.isend(lngcv__jztev, 1,
            xkm__qsb, myjc__iuvrt, True)
    return gsdx__pncc, ybvi__skdl


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    znst__krkd = {'axis': axis, 'kind': kind, 'order': order}
    pzdrv__zrkm = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', znst__krkd, pzdrv__zrkm, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    pass


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    ywg__mnlg = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                edzbn__ftxm = A._indices
                pzoaz__kvjdn = len(edzbn__ftxm)
                gtfax__ibfx = alloc_int_array(pzoaz__kvjdn * repeats, np.int32)
                for i in range(pzoaz__kvjdn):
                    nmw__hco = i * repeats
                    if bodo.libs.array_kernels.isna(edzbn__ftxm, i):
                        for nvv__wrxir in range(repeats):
                            bodo.libs.array_kernels.setna(gtfax__ibfx, 
                                nmw__hco + nvv__wrxir)
                    else:
                        gtfax__ibfx[nmw__hco:nmw__hco + repeats] = edzbn__ftxm[
                            i]
                return init_dict_arr(data_arr, gtfax__ibfx, A.
                    _has_global_dictionary, A._has_deduped_local_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            pzoaz__kvjdn = len(A)
            out_arr = bodo.utils.utils.alloc_type(pzoaz__kvjdn * repeats,
                ywg__mnlg, (-1,))
            for i in range(pzoaz__kvjdn):
                nmw__hco = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for nvv__wrxir in range(repeats):
                        bodo.libs.array_kernels.setna(out_arr, nmw__hco +
                            nvv__wrxir)
                else:
                    out_arr[nmw__hco:nmw__hco + repeats] = A[i]
            return out_arr
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            edzbn__ftxm = A._indices
            pzoaz__kvjdn = len(edzbn__ftxm)
            gtfax__ibfx = alloc_int_array(repeats.sum(), np.int32)
            nmw__hco = 0
            for i in range(pzoaz__kvjdn):
                mwldn__trb = repeats[i]
                if mwldn__trb < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(edzbn__ftxm, i):
                    for nvv__wrxir in range(mwldn__trb):
                        bodo.libs.array_kernels.setna(gtfax__ibfx, nmw__hco +
                            nvv__wrxir)
                else:
                    gtfax__ibfx[nmw__hco:nmw__hco + mwldn__trb] = edzbn__ftxm[i
                        ]
                nmw__hco += mwldn__trb
            return init_dict_arr(data_arr, gtfax__ibfx, A.
                _has_global_dictionary, A._has_deduped_local_dictionary)
        return impl_dict_arr

    def impl_arr(A, repeats):
        pzoaz__kvjdn = len(A)
        out_arr = bodo.utils.utils.alloc_type(repeats.sum(), ywg__mnlg, (-1,))
        nmw__hco = 0
        for i in range(pzoaz__kvjdn):
            mwldn__trb = repeats[i]
            if mwldn__trb < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for nvv__wrxir in range(mwldn__trb):
                    bodo.libs.array_kernels.setna(out_arr, nmw__hco +
                        nvv__wrxir)
            else:
                out_arr[nmw__hco:nmw__hco + mwldn__trb] = A[i]
            nmw__hco += mwldn__trb
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
        qxi__alv = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(qxi__alv, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        gvd__naao = bodo.libs.array_kernels.concat([A1, A2])
        jnoqm__yru = bodo.libs.array_kernels.unique(gvd__naao)
        return pd.Series(jnoqm__yru).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    znst__krkd = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    pzdrv__zrkm = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', znst__krkd, pzdrv__zrkm, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        jpmuf__mgj = bodo.libs.array_kernels.unique(A1)
        nykx__jnwde = bodo.libs.array_kernels.unique(A2)
        gvd__naao = bodo.libs.array_kernels.concat([jpmuf__mgj, nykx__jnwde])
        iqec__ufroz = pd.Series(gvd__naao).sort_values().values
        return slice_array_intersect1d(iqec__ufroz)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    bzj__dyaw = arr[1:] == arr[:-1]
    return arr[:-1][bzj__dyaw]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    myjc__iuvrt = np.int32(bodo.hiframes.rolling.comm_border_tag)
    tqad__sxvkc = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        uoil__ace = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32(
            rank - 1), myjc__iuvrt, True)
        bodo.libs.distributed_api.wait(uoil__ace, True)
    if rank == n_pes - 1:
        return None
    else:
        fyr__wgv = bodo.libs.distributed_api.irecv(tqad__sxvkc, 1, np.int32
            (rank + 1), myjc__iuvrt, True)
        bodo.libs.distributed_api.wait(fyr__wgv, True)
        return tqad__sxvkc[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    bzj__dyaw = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            bzj__dyaw[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        pke__xxvly = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == pke__xxvly:
            bzj__dyaw[n - 1] = True
    return bzj__dyaw


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    znst__krkd = {'assume_unique': assume_unique}
    pzdrv__zrkm = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', znst__krkd, pzdrv__zrkm, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        jpmuf__mgj = bodo.libs.array_kernels.unique(A1)
        nykx__jnwde = bodo.libs.array_kernels.unique(A2)
        bzj__dyaw = calculate_mask_setdiff1d(jpmuf__mgj, nykx__jnwde)
        return pd.Series(jpmuf__mgj[bzj__dyaw]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    bzj__dyaw = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        bzj__dyaw &= A1 != A2[i]
    return bzj__dyaw


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    znst__krkd = {'retstep': retstep, 'axis': axis}
    pzdrv__zrkm = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', znst__krkd, pzdrv__zrkm, 'numpy')
    qdmyx__gucva = False
    if is_overload_none(dtype):
        ywg__mnlg = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            qdmyx__gucva = True
        ywg__mnlg = numba.np.numpy_support.as_dtype(dtype).type
    if qdmyx__gucva:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            kue__uqq = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, ywg__mnlg)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = ywg__mnlg(np.floor(start + i * kue__uqq))
            return out_arr
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            kue__uqq = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, ywg__mnlg)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = ywg__mnlg(start + i * kue__uqq)
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
        ibaau__salr = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                ibaau__salr += A[i] == val
        return ibaau__salr > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    znst__krkd = {'axis': axis, 'out': out, 'keepdims': keepdims}
    pzdrv__zrkm = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', znst__krkd, pzdrv__zrkm, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        ibaau__salr = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                ibaau__salr += int(bool(A[i]))
        return ibaau__salr > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    znst__krkd = {'axis': axis, 'out': out, 'keepdims': keepdims}
    pzdrv__zrkm = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', znst__krkd, pzdrv__zrkm, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        ibaau__salr = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                ibaau__salr += int(bool(A[i]))
        return ibaau__salr == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    znst__krkd = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    pzdrv__zrkm = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', znst__krkd, pzdrv__zrkm, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        rpw__qql = np.promote_types(numba.np.numpy_support.as_dtype(A.dtype
            ), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            out_arr = np.empty(n, rpw__qql)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(out_arr, i)
                    continue
                out_arr[i] = np_cbrt_scalar(A[i], rpw__qql)
            return out_arr
        return impl_arr
    rpw__qql = np.promote_types(numba.np.numpy_support.as_dtype(A), numba.
        np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, rpw__qql)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    qen__jzxk = x < 0
    if qen__jzxk:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if qen__jzxk:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    qwjr__kstdl = isinstance(tup, (types.BaseTuple, types.List))
    lmx__jygu = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for uobrj__lfxi in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                uobrj__lfxi, 'numpy.hstack()')
            qwjr__kstdl = qwjr__kstdl and bodo.utils.utils.is_array_typ(
                uobrj__lfxi, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        qwjr__kstdl = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif lmx__jygu:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        pqa__ofna = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for uobrj__lfxi in pqa__ofna.types:
            lmx__jygu = lmx__jygu and bodo.utils.utils.is_array_typ(uobrj__lfxi
                , False)
    if not (qwjr__kstdl or lmx__jygu):
        return
    if lmx__jygu:

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
    znst__krkd = {'check_valid': check_valid, 'tol': tol}
    pzdrv__zrkm = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', znst__krkd,
        pzdrv__zrkm, 'numpy')
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
        rubfy__kdax = mean.shape[0]
        tip__oez = size, rubfy__kdax
        yuzt__wvmy = np.random.standard_normal(tip__oez)
        cov = cov.astype(np.float64)
        bjdb__wrw, s, krtbr__fskl = np.linalg.svd(cov)
        res = np.dot(yuzt__wvmy, np.sqrt(s).reshape(rubfy__kdax, 1) *
            krtbr__fskl)
        henm__iyu = res + mean
        return henm__iyu
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
            mlppn__kxd = bodo.hiframes.series_kernels._get_type_max_value(arr)
            jyycp__uyf = typing.builtins.IndexValue(-1, mlppn__kxd)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                imew__opro = typing.builtins.IndexValue(i, arr[i])
                jyycp__uyf = min(jyycp__uyf, imew__opro)
            return jyycp__uyf.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        ugrnf__cxz = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            tkhzg__uuxbu = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            mlppn__kxd = ugrnf__cxz(len(arr.dtype.categories) + 1)
            jyycp__uyf = typing.builtins.IndexValue(-1, mlppn__kxd)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                imew__opro = typing.builtins.IndexValue(i, tkhzg__uuxbu[i])
                jyycp__uyf = min(jyycp__uyf, imew__opro)
            return jyycp__uyf.index
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
            mlppn__kxd = bodo.hiframes.series_kernels._get_type_min_value(arr)
            jyycp__uyf = typing.builtins.IndexValue(-1, mlppn__kxd)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                imew__opro = typing.builtins.IndexValue(i, arr[i])
                jyycp__uyf = max(jyycp__uyf, imew__opro)
            return jyycp__uyf.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        ugrnf__cxz = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            tkhzg__uuxbu = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            mlppn__kxd = ugrnf__cxz(-1)
            jyycp__uyf = typing.builtins.IndexValue(-1, mlppn__kxd)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                imew__opro = typing.builtins.IndexValue(i, tkhzg__uuxbu[i])
                jyycp__uyf = max(jyycp__uyf, imew__opro)
            return jyycp__uyf.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
