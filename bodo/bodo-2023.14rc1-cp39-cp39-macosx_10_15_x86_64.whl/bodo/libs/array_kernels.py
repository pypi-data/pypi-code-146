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
        qskiv__znwq = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = qskiv__znwq
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        qskiv__znwq = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = qskiv__znwq
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
            wipxu__ucf = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            wipxu__ucf[ind + 1] = wipxu__ucf[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            wipxu__ucf = bodo.libs.array_item_arr_ext.get_offsets(arr)
            wipxu__ucf[ind + 1] = wipxu__ucf[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            wipxu__ucf = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            wipxu__ucf[ind + 1] = wipxu__ucf[ind]
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
    zcz__azc = arr_tup.count
    vdbf__babxq = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(zcz__azc):
        vdbf__babxq += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    vdbf__babxq += '  return\n'
    jkle__vzos = {}
    exec(vdbf__babxq, {'setna': setna}, jkle__vzos)
    impl = jkle__vzos['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        mob__eebb = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(mob__eebb.start, mob__eebb.stop, mob__eebb.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        zdpob__xac = 'n'
        tdw__lnl = 'n_pes'
        zhp__fiqmv = 'min_op'
    else:
        zdpob__xac = 'n-1, -1, -1'
        tdw__lnl = '-1'
        zhp__fiqmv = 'max_op'
    vdbf__babxq = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {tdw__lnl}
    for i in range({zdpob__xac}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {zhp__fiqmv}))
        if possible_valid_rank != {tdw__lnl}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    jkle__vzos = {}
    exec(vdbf__babxq, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, jkle__vzos)
    impl = jkle__vzos['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    bwhm__kskz = array_to_info(arr)
    _median_series_computation(res, bwhm__kskz, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(bwhm__kskz)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    bwhm__kskz = array_to_info(arr)
    _autocorr_series_computation(res, bwhm__kskz, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(bwhm__kskz)


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
    bwhm__kskz = array_to_info(arr)
    _compute_series_monotonicity(res, bwhm__kskz, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(bwhm__kskz)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    rhwwn__qodi = res[0] > 0.5
    return rhwwn__qodi


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        dufgf__fdkq = '-'
        pxhq__uizzo = 'index_arr[0] > threshhold_date'
        zdpob__xac = '1, n+1'
        ytzp__qrwui = 'index_arr[-i] <= threshhold_date'
        bulqx__rzh = 'i - 1'
    else:
        dufgf__fdkq = '+'
        pxhq__uizzo = 'index_arr[-1] < threshhold_date'
        zdpob__xac = 'n'
        ytzp__qrwui = 'index_arr[i] >= threshhold_date'
        bulqx__rzh = 'i'
    vdbf__babxq = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        vdbf__babxq += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_tz_naive_type):\n'
            )
        vdbf__babxq += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            vdbf__babxq += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            vdbf__babxq += """      threshhold_date = initial_date - date_offset.base + date_offset
"""
            vdbf__babxq += '    else:\n'
            vdbf__babxq += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            vdbf__babxq += (
                f'    threshhold_date = initial_date {dufgf__fdkq} date_offset\n'
                )
    else:
        vdbf__babxq += (
            f'  threshhold_date = initial_date {dufgf__fdkq} offset\n')
    vdbf__babxq += '  local_valid = 0\n'
    vdbf__babxq += f'  n = len(index_arr)\n'
    vdbf__babxq += f'  if n:\n'
    vdbf__babxq += f'    if {pxhq__uizzo}:\n'
    vdbf__babxq += '      loc_valid = n\n'
    vdbf__babxq += '    else:\n'
    vdbf__babxq += f'      for i in range({zdpob__xac}):\n'
    vdbf__babxq += f'        if {ytzp__qrwui}:\n'
    vdbf__babxq += f'          loc_valid = {bulqx__rzh}\n'
    vdbf__babxq += '          break\n'
    vdbf__babxq += '  if is_parallel:\n'
    vdbf__babxq += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    vdbf__babxq += '    return total_valid\n'
    vdbf__babxq += '  else:\n'
    vdbf__babxq += '    return loc_valid\n'
    jkle__vzos = {}
    exec(vdbf__babxq, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, jkle__vzos)
    return jkle__vzos['impl']


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
    yak__eko = numba_to_c_type(sig.args[0].dtype)
    qnub__omo = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), yak__eko))
    gyjc__rea = args[0]
    jhcn__oaljm = sig.args[0]
    if isinstance(jhcn__oaljm, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        gyjc__rea = cgutils.create_struct_proxy(jhcn__oaljm)(context,
            builder, gyjc__rea).data
        jhcn__oaljm = types.Array(jhcn__oaljm.dtype, 1, 'C')
    assert jhcn__oaljm.ndim == 1
    arr = make_array(jhcn__oaljm)(context, builder, gyjc__rea)
    ixhk__dfo = builder.extract_value(arr.shape, 0)
    nzhxt__uyb = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        ixhk__dfo, args[1], builder.load(qnub__omo)]
    wlwme__hauu = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    awva__ditf = lir.FunctionType(lir.DoubleType(), wlwme__hauu)
    ibbaw__lfatf = cgutils.get_or_insert_function(builder.module,
        awva__ditf, name='quantile_sequential')
    husb__dwl = builder.call(ibbaw__lfatf, nzhxt__uyb)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return husb__dwl


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, FloatingArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    yak__eko = numba_to_c_type(sig.args[0].dtype)
    qnub__omo = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), yak__eko))
    gyjc__rea = args[0]
    jhcn__oaljm = sig.args[0]
    if isinstance(jhcn__oaljm, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        gyjc__rea = cgutils.create_struct_proxy(jhcn__oaljm)(context,
            builder, gyjc__rea).data
        jhcn__oaljm = types.Array(jhcn__oaljm.dtype, 1, 'C')
    assert jhcn__oaljm.ndim == 1
    arr = make_array(jhcn__oaljm)(context, builder, gyjc__rea)
    ixhk__dfo = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        woar__yhvqo = args[2]
    else:
        woar__yhvqo = ixhk__dfo
    nzhxt__uyb = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        ixhk__dfo, woar__yhvqo, args[1], builder.load(qnub__omo)]
    wlwme__hauu = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        IntType(64), lir.DoubleType(), lir.IntType(32)]
    awva__ditf = lir.FunctionType(lir.DoubleType(), wlwme__hauu)
    ibbaw__lfatf = cgutils.get_or_insert_function(builder.module,
        awva__ditf, name='quantile_parallel')
    husb__dwl = builder.call(ibbaw__lfatf, nzhxt__uyb)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return husb__dwl


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        n = len(arr)
        nyzzs__bwmf = bodo.utils.utils.alloc_type(n, np.bool_, (-1,))
        nyzzs__bwmf[0] = True
        umze__gkle = pd.isna(arr)
        for i in range(1, len(arr)):
            if umze__gkle[i] and umze__gkle[i - 1]:
                nyzzs__bwmf[i] = False
            elif umze__gkle[i] or umze__gkle[i - 1]:
                nyzzs__bwmf[i] = True
            else:
                nyzzs__bwmf[i] = arr[i] != arr[i - 1]
        return nyzzs__bwmf
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
    vdbf__babxq = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    vdbf__babxq += '  na_idxs = pd.isna(arr)\n'
    vdbf__babxq += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    vdbf__babxq += '  nas = sum(na_idxs)\n'
    if not ascending:
        vdbf__babxq += '  if nas and nas < (sorter.size - 1):\n'
        vdbf__babxq += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        vdbf__babxq += '  else:\n'
        vdbf__babxq += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        vdbf__babxq += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    vdbf__babxq += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    vdbf__babxq += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        vdbf__babxq += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        vdbf__babxq += '    inv,\n'
        vdbf__babxq += '    new_dtype=np.float64,\n'
        vdbf__babxq += '    copy=True,\n'
        vdbf__babxq += '    nan_to_str=False,\n'
        vdbf__babxq += '    from_series=True,\n'
        vdbf__babxq += '    ) + 1\n'
    else:
        vdbf__babxq += '  arr = arr[sorter]\n'
        vdbf__babxq += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n')
        vdbf__babxq += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            vdbf__babxq += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            vdbf__babxq += '    dense,\n'
            vdbf__babxq += '    new_dtype=np.float64,\n'
            vdbf__babxq += '    copy=True,\n'
            vdbf__babxq += '    nan_to_str=False,\n'
            vdbf__babxq += '    from_series=True,\n'
            vdbf__babxq += '  )\n'
        else:
            vdbf__babxq += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            vdbf__babxq += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                vdbf__babxq += '  ret = count_float[dense]\n'
            elif method == 'min':
                vdbf__babxq += '  ret = count_float[dense - 1] + 1\n'
            else:
                vdbf__babxq += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                vdbf__babxq += '  ret[na_idxs] = -1\n'
            vdbf__babxq += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            vdbf__babxq += '  div_val = arr.size - nas\n'
        else:
            vdbf__babxq += '  div_val = arr.size\n'
        vdbf__babxq += '  for i in range(len(ret)):\n'
        vdbf__babxq += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        vdbf__babxq += '  ret[na_idxs] = np.nan\n'
    vdbf__babxq += '  return ret\n'
    jkle__vzos = {}
    exec(vdbf__babxq, {'np': np, 'pd': pd, 'bodo': bodo}, jkle__vzos)
    return jkle__vzos['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    ahyx__cbmr = start
    aeyi__mbm = 2 * start + 1
    vxu__qzbc = 2 * start + 2
    if aeyi__mbm < n and not cmp_f(arr[aeyi__mbm], arr[ahyx__cbmr]):
        ahyx__cbmr = aeyi__mbm
    if vxu__qzbc < n and not cmp_f(arr[vxu__qzbc], arr[ahyx__cbmr]):
        ahyx__cbmr = vxu__qzbc
    if ahyx__cbmr != start:
        arr[start], arr[ahyx__cbmr] = arr[ahyx__cbmr], arr[start]
        ind_arr[start], ind_arr[ahyx__cbmr] = ind_arr[ahyx__cbmr], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, ahyx__cbmr, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        slp__pnx = np.empty(k, A.dtype)
        czra__ieph = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                slp__pnx[ind] = A[i]
                czra__ieph[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            slp__pnx = slp__pnx[:ind]
            czra__ieph = czra__ieph[:ind]
        return slp__pnx, czra__ieph, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        xkrk__tep = np.sort(A)
        jme__ygjla = index_arr[np.argsort(A)]
        qsee__ddo = pd.Series(xkrk__tep).notna().values
        xkrk__tep = xkrk__tep[qsee__ddo]
        jme__ygjla = jme__ygjla[qsee__ddo]
        if is_largest:
            xkrk__tep = xkrk__tep[::-1]
            jme__ygjla = jme__ygjla[::-1]
        return np.ascontiguousarray(xkrk__tep), np.ascontiguousarray(jme__ygjla
            )
    slp__pnx, czra__ieph, start = select_k_nonan(A, index_arr, m, k)
    czra__ieph = czra__ieph[slp__pnx.argsort()]
    slp__pnx.sort()
    if not is_largest:
        slp__pnx = np.ascontiguousarray(slp__pnx[::-1])
        czra__ieph = np.ascontiguousarray(czra__ieph[::-1])
    for i in range(start, m):
        if cmp_f(A[i], slp__pnx[0]):
            slp__pnx[0] = A[i]
            czra__ieph[0] = index_arr[i]
            min_heapify(slp__pnx, czra__ieph, k, 0, cmp_f)
    czra__ieph = czra__ieph[slp__pnx.argsort()]
    slp__pnx.sort()
    if is_largest:
        slp__pnx = slp__pnx[::-1]
        czra__ieph = czra__ieph[::-1]
    return np.ascontiguousarray(slp__pnx), np.ascontiguousarray(czra__ieph)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    bjyng__tvlrz = bodo.libs.distributed_api.get_rank()
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    vgvgd__lis, hrpmd__mkreo = nlargest(A, I, k, is_largest, cmp_f)
    fzew__hdeqd = bodo.libs.distributed_api.gatherv(vgvgd__lis)
    xndnm__lcwwg = bodo.libs.distributed_api.gatherv(hrpmd__mkreo)
    if bjyng__tvlrz == MPI_ROOT:
        res, invbi__fasz = nlargest(fzew__hdeqd, xndnm__lcwwg, k,
            is_largest, cmp_f)
    else:
        res = np.empty(k, A.dtype)
        invbi__fasz = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(invbi__fasz)
    return res, invbi__fasz


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    odued__oapoe, yvd__mrek = mat.shape
    jdp__mfp = np.empty((yvd__mrek, yvd__mrek), dtype=np.float64)
    for dvav__oghw in range(yvd__mrek):
        for ywjrg__eam in range(dvav__oghw + 1):
            jgxks__fkcfx = 0
            yal__jum = mlfcv__zjacw = ezjt__vhbov = mxcy__fkf = 0.0
            for i in range(odued__oapoe):
                if np.isfinite(mat[i, dvav__oghw]) and np.isfinite(mat[i,
                    ywjrg__eam]):
                    jsp__tfgl = mat[i, dvav__oghw]
                    ljn__ara = mat[i, ywjrg__eam]
                    jgxks__fkcfx += 1
                    ezjt__vhbov += jsp__tfgl
                    mxcy__fkf += ljn__ara
            if parallel:
                jgxks__fkcfx = bodo.libs.distributed_api.dist_reduce(
                    jgxks__fkcfx, sum_op)
                ezjt__vhbov = bodo.libs.distributed_api.dist_reduce(ezjt__vhbov
                    , sum_op)
                mxcy__fkf = bodo.libs.distributed_api.dist_reduce(mxcy__fkf,
                    sum_op)
            if jgxks__fkcfx < minpv:
                jdp__mfp[dvav__oghw, ywjrg__eam] = jdp__mfp[ywjrg__eam,
                    dvav__oghw] = np.nan
            else:
                lyn__eihif = ezjt__vhbov / jgxks__fkcfx
                upgy__kthd = mxcy__fkf / jgxks__fkcfx
                ezjt__vhbov = 0.0
                for i in range(odued__oapoe):
                    if np.isfinite(mat[i, dvav__oghw]) and np.isfinite(mat[
                        i, ywjrg__eam]):
                        jsp__tfgl = mat[i, dvav__oghw] - lyn__eihif
                        ljn__ara = mat[i, ywjrg__eam] - upgy__kthd
                        ezjt__vhbov += jsp__tfgl * ljn__ara
                        yal__jum += jsp__tfgl * jsp__tfgl
                        mlfcv__zjacw += ljn__ara * ljn__ara
                if parallel:
                    ezjt__vhbov = bodo.libs.distributed_api.dist_reduce(
                        ezjt__vhbov, sum_op)
                    yal__jum = bodo.libs.distributed_api.dist_reduce(yal__jum,
                        sum_op)
                    mlfcv__zjacw = bodo.libs.distributed_api.dist_reduce(
                        mlfcv__zjacw, sum_op)
                exxj__hid = jgxks__fkcfx - 1.0 if cov else sqrt(yal__jum *
                    mlfcv__zjacw)
                if exxj__hid != 0.0:
                    jdp__mfp[dvav__oghw, ywjrg__eam] = jdp__mfp[ywjrg__eam,
                        dvav__oghw] = ezjt__vhbov / exxj__hid
                else:
                    jdp__mfp[dvav__oghw, ywjrg__eam] = jdp__mfp[ywjrg__eam,
                        dvav__oghw] = np.nan
    return jdp__mfp


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    uulka__bmgm = n != 1
    vdbf__babxq = 'def impl(data, parallel=False):\n'
    vdbf__babxq += '  if parallel:\n'
    tmf__einl = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    vdbf__babxq += f'    cpp_table = arr_info_list_to_table([{tmf__einl}])\n'
    vdbf__babxq += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    fgcid__mix = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    vdbf__babxq += f'    data = ({fgcid__mix},)\n'
    vdbf__babxq += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    vdbf__babxq += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    vdbf__babxq += '    bodo.libs.array.delete_table(cpp_table)\n'
    vdbf__babxq += '  n = len(data[0])\n'
    vdbf__babxq += '  out = np.empty(n, np.bool_)\n'
    vdbf__babxq += '  uniqs = dict()\n'
    if uulka__bmgm:
        vdbf__babxq += '  for i in range(n):\n'
        kdh__nqfo = ', '.join(f'data[{i}][i]' for i in range(n))
        vqfys__iorz = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        vdbf__babxq += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({kdh__nqfo},), ({vqfys__iorz},))
"""
        vdbf__babxq += '    if val in uniqs:\n'
        vdbf__babxq += '      out[i] = True\n'
        vdbf__babxq += '    else:\n'
        vdbf__babxq += '      out[i] = False\n'
        vdbf__babxq += '      uniqs[val] = 0\n'
    else:
        vdbf__babxq += '  data = data[0]\n'
        vdbf__babxq += '  hasna = False\n'
        vdbf__babxq += '  for i in range(n):\n'
        vdbf__babxq += '    if bodo.libs.array_kernels.isna(data, i):\n'
        vdbf__babxq += '      out[i] = hasna\n'
        vdbf__babxq += '      hasna = True\n'
        vdbf__babxq += '    else:\n'
        vdbf__babxq += '      val = data[i]\n'
        vdbf__babxq += '      if val in uniqs:\n'
        vdbf__babxq += '        out[i] = True\n'
        vdbf__babxq += '      else:\n'
        vdbf__babxq += '        out[i] = False\n'
        vdbf__babxq += '        uniqs[val] = 0\n'
    vdbf__babxq += '  if parallel:\n'
    vdbf__babxq += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    vdbf__babxq += '  return out\n'
    jkle__vzos = {}
    exec(vdbf__babxq, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        jkle__vzos)
    impl = jkle__vzos['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    pass


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    zcz__azc = len(data)
    vdbf__babxq = (
        'def impl(data, ind_arr, n, frac, replace, parallel=False):\n')
    vdbf__babxq += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(zcz__azc))
        )
    vdbf__babxq += '  table_total = arr_info_list_to_table(info_list_total)\n'
    vdbf__babxq += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(zcz__azc))
    for absd__ujzk in range(zcz__azc):
        vdbf__babxq += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(absd__ujzk, absd__ujzk, absd__ujzk))
    vdbf__babxq += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(zcz__azc))
    vdbf__babxq += '  delete_table(out_table)\n'
    vdbf__babxq += '  delete_table(table_total)\n'
    vdbf__babxq += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(zcz__azc)))
    jkle__vzos = {}
    exec(vdbf__babxq, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, jkle__vzos)
    impl = jkle__vzos['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    pass


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    zcz__azc = len(data)
    vdbf__babxq = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    vdbf__babxq += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(zcz__azc))
        )
    vdbf__babxq += '  table_total = arr_info_list_to_table(info_list_total)\n'
    vdbf__babxq += '  keep_i = 0\n'
    vdbf__babxq += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for absd__ujzk in range(zcz__azc):
        vdbf__babxq += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(absd__ujzk, absd__ujzk, absd__ujzk))
    vdbf__babxq += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(zcz__azc))
    vdbf__babxq += '  delete_table(out_table)\n'
    vdbf__babxq += '  delete_table(table_total)\n'
    vdbf__babxq += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(zcz__azc)))
    jkle__vzos = {}
    exec(vdbf__babxq, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, jkle__vzos)
    impl = jkle__vzos['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    pass


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        hpkp__pubva = [array_to_info(data_arr)]
        kirg__fako = arr_info_list_to_table(hpkp__pubva)
        aeqmb__bbn = 0
        uej__eazyp = drop_duplicates_table(kirg__fako, parallel, 1,
            aeqmb__bbn, False, True)
        out_arr = info_to_array(info_from_table(uej__eazyp, 0), data_arr)
        delete_table(uej__eazyp)
        delete_table(kirg__fako)
        return out_arr
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    pass


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    dom__nqcuu = len(data.types)
    jcy__yhjp = [('out' + str(i)) for i in range(dom__nqcuu)]
    hvlsr__pew = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    ylsdo__fze = ['isna(data[{}], i)'.format(i) for i in hvlsr__pew]
    yezoi__cjk = 'not ({})'.format(' or '.join(ylsdo__fze))
    if not is_overload_none(thresh):
        yezoi__cjk = '(({}) <= ({}) - thresh)'.format(' + '.join(ylsdo__fze
            ), dom__nqcuu - 1)
    elif how == 'all':
        yezoi__cjk = 'not ({})'.format(' and '.join(ylsdo__fze))
    vdbf__babxq = 'def _dropna_imp(data, how, thresh, subset):\n'
    vdbf__babxq += '  old_len = len(data[0])\n'
    vdbf__babxq += '  new_len = 0\n'
    vdbf__babxq += '  for i in range(old_len):\n'
    vdbf__babxq += '    if {}:\n'.format(yezoi__cjk)
    vdbf__babxq += '      new_len += 1\n'
    for i, out in enumerate(jcy__yhjp):
        if isinstance(data[i], bodo.CategoricalArrayType):
            vdbf__babxq += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            vdbf__babxq += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    vdbf__babxq += '  curr_ind = 0\n'
    vdbf__babxq += '  for i in range(old_len):\n'
    vdbf__babxq += '    if {}:\n'.format(yezoi__cjk)
    for i in range(dom__nqcuu):
        vdbf__babxq += '      if isna(data[{}], i):\n'.format(i)
        vdbf__babxq += '        setna({}, curr_ind)\n'.format(jcy__yhjp[i])
        vdbf__babxq += '      else:\n'
        vdbf__babxq += '        {}[curr_ind] = data[{}][i]\n'.format(jcy__yhjp
            [i], i)
    vdbf__babxq += '      curr_ind += 1\n'
    vdbf__babxq += '  return {}\n'.format(', '.join(jcy__yhjp))
    jkle__vzos = {}
    khs__pjioo = {'t{}'.format(i): kgro__bcuvt for i, kgro__bcuvt in
        enumerate(data.types)}
    khs__pjioo.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(vdbf__babxq, khs__pjioo, jkle__vzos)
    jso__crzns = jkle__vzos['_dropna_imp']
    return jso__crzns


def get(arr, ind):
    pass


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        jhcn__oaljm = arr.dtype
        eqpx__faxn = jhcn__oaljm.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            qekkw__ocm = init_nested_counts(eqpx__faxn)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                qekkw__ocm = add_nested_counts(qekkw__ocm, val[ind])
            out_arr = bodo.utils.utils.alloc_type(n, jhcn__oaljm, qekkw__ocm)
            for lowu__ndo in range(n):
                if bodo.libs.array_kernels.isna(arr, lowu__ndo):
                    setna(out_arr, lowu__ndo)
                    continue
                val = arr[lowu__ndo]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(out_arr, lowu__ndo)
                    continue
                out_arr[lowu__ndo] = val[ind]
            return out_arr
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    frgji__qsn = _to_readonly(arr_types.types[0])
    return all(isinstance(kgro__bcuvt, CategoricalArrayType) and 
        _to_readonly(kgro__bcuvt) == frgji__qsn for kgro__bcuvt in
        arr_types.types)


def concat(arr_list):
    pass


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        utje__syg = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            hwyi__toxpi = 0
            ldsfp__tvk = []
            for A in arr_list:
                ttnl__xmct = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                ldsfp__tvk.append(bodo.libs.array_item_arr_ext.get_data(A))
                hwyi__toxpi += ttnl__xmct
            veg__rem = np.empty(hwyi__toxpi + 1, offset_type)
            zifq__vepw = bodo.libs.array_kernels.concat(ldsfp__tvk)
            fhs__knlkp = np.empty(hwyi__toxpi + 7 >> 3, np.uint8)
            jodnh__kwp = 0
            zhp__sju = 0
            for A in arr_list:
                wyunk__tbdel = bodo.libs.array_item_arr_ext.get_offsets(A)
                yyxl__prv = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                ttnl__xmct = len(A)
                hil__nzey = wyunk__tbdel[ttnl__xmct]
                for i in range(ttnl__xmct):
                    veg__rem[i + jodnh__kwp] = wyunk__tbdel[i] + zhp__sju
                    vwb__atr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        yyxl__prv, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(fhs__knlkp, i +
                        jodnh__kwp, vwb__atr)
                jodnh__kwp += ttnl__xmct
                zhp__sju += hil__nzey
            veg__rem[jodnh__kwp] = zhp__sju
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                hwyi__toxpi, zifq__vepw, veg__rem, fhs__knlkp)
            return out_arr
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        gls__ptop = arr_list.dtype.names
        vdbf__babxq = 'def struct_array_concat_impl(arr_list):\n'
        vdbf__babxq += f'    n_all = 0\n'
        for i in range(len(gls__ptop)):
            vdbf__babxq += f'    concat_list{i} = []\n'
        vdbf__babxq += '    for A in arr_list:\n'
        vdbf__babxq += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(gls__ptop)):
            vdbf__babxq += f'        concat_list{i}.append(data_tuple[{i}])\n'
        vdbf__babxq += '        n_all += len(A)\n'
        vdbf__babxq += '    n_bytes = (n_all + 7) >> 3\n'
        vdbf__babxq += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        vdbf__babxq += '    curr_bit = 0\n'
        vdbf__babxq += '    for A in arr_list:\n'
        vdbf__babxq += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        vdbf__babxq += '        for j in range(len(A)):\n'
        vdbf__babxq += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        vdbf__babxq += """            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)
"""
        vdbf__babxq += '            curr_bit += 1\n'
        vdbf__babxq += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        fcps__btn = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(gls__ptop))])
        vdbf__babxq += f'        ({fcps__btn},),\n'
        vdbf__babxq += '        new_mask,\n'
        vdbf__babxq += f'        {gls__ptop},\n'
        vdbf__babxq += '    )\n'
        jkle__vzos = {}
        exec(vdbf__babxq, {'bodo': bodo, 'np': np}, jkle__vzos)
        return jkle__vzos['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.DatetimeArrayType):
        ebn__yefk = arr_list.dtype.tz

        def tz_aware_concat_impl(arr_list):
            gyjkh__sdmvy = 0
            for A in arr_list:
                gyjkh__sdmvy += len(A)
            innw__zlnp = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(
                gyjkh__sdmvy, ebn__yefk)
            zvgj__gvjfm = 0
            for A in arr_list:
                for i in range(len(A)):
                    innw__zlnp[i + zvgj__gvjfm] = A[i]
                zvgj__gvjfm += len(A)
            return innw__zlnp
        return tz_aware_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            gyjkh__sdmvy = 0
            for A in arr_list:
                gyjkh__sdmvy += len(A)
            innw__zlnp = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(gyjkh__sdmvy))
            zvgj__gvjfm = 0
            for A in arr_list:
                for i in range(len(A)):
                    innw__zlnp._data[i + zvgj__gvjfm] = A._data[i]
                    vwb__atr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(innw__zlnp.
                        _null_bitmap, i + zvgj__gvjfm, vwb__atr)
                zvgj__gvjfm += len(A)
            return innw__zlnp
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            gyjkh__sdmvy = 0
            for A in arr_list:
                gyjkh__sdmvy += len(A)
            innw__zlnp = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(gyjkh__sdmvy))
            zvgj__gvjfm = 0
            for A in arr_list:
                for i in range(len(A)):
                    innw__zlnp._days_data[i + zvgj__gvjfm] = A._days_data[i]
                    innw__zlnp._seconds_data[i + zvgj__gvjfm
                        ] = A._seconds_data[i]
                    innw__zlnp._microseconds_data[i + zvgj__gvjfm
                        ] = A._microseconds_data[i]
                    vwb__atr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(innw__zlnp.
                        _null_bitmap, i + zvgj__gvjfm, vwb__atr)
                zvgj__gvjfm += len(A)
            return innw__zlnp
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        uyzy__dtync = arr_list.dtype.precision
        vif__wqaw = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            gyjkh__sdmvy = 0
            for A in arr_list:
                gyjkh__sdmvy += len(A)
            innw__zlnp = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                gyjkh__sdmvy, uyzy__dtync, vif__wqaw)
            zvgj__gvjfm = 0
            for A in arr_list:
                for i in range(len(A)):
                    innw__zlnp._data[i + zvgj__gvjfm] = A._data[i]
                    vwb__atr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(innw__zlnp.
                        _null_bitmap, i + zvgj__gvjfm, vwb__atr)
                zvgj__gvjfm += len(A)
            return innw__zlnp
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        kgro__bcuvt) for kgro__bcuvt in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            favmc__jwtw = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    favmc__jwtw = arr_list.types[i]
                    break
        else:
            favmc__jwtw = arr_list.dtype
        if favmc__jwtw == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                iht__jnf = 0
                asb__auma = 0
                wcsl__fco = 0
                for A in arr_list:
                    data_arr = A._data
                    gztg__cmyoj = A._indices
                    wcsl__fco += len(gztg__cmyoj)
                    iht__jnf += len(data_arr)
                    asb__auma += bodo.libs.str_arr_ext.num_total_chars(data_arr
                        )
                lbwfp__xkvn = pre_alloc_string_array(iht__jnf, asb__auma)
                potdr__tscib = bodo.libs.int_arr_ext.alloc_int_array(wcsl__fco,
                    np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(lbwfp__xkvn, -1)
                ghnxi__rsh = 0
                cls__hjhf = 0
                fas__eno = 0
                for A in arr_list:
                    data_arr = A._data
                    gztg__cmyoj = A._indices
                    wcsl__fco = len(gztg__cmyoj)
                    bodo.libs.str_arr_ext.set_string_array_range(lbwfp__xkvn,
                        data_arr, ghnxi__rsh, cls__hjhf)
                    for i in range(wcsl__fco):
                        if bodo.libs.array_kernels.isna(gztg__cmyoj, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            gztg__cmyoj[i]):
                            bodo.libs.array_kernels.setna(potdr__tscib, 
                                fas__eno + i)
                        else:
                            potdr__tscib[fas__eno + i
                                ] = ghnxi__rsh + gztg__cmyoj[i]
                    ghnxi__rsh += len(data_arr)
                    cls__hjhf += bodo.libs.str_arr_ext.num_total_chars(data_arr
                        )
                    fas__eno += wcsl__fco
                out_arr = init_dict_arr(lbwfp__xkvn, potdr__tscib, False, False
                    )
                ghy__iet = drop_duplicates_local_dictionary(out_arr, False)
                return ghy__iet
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            iht__jnf = 0
            asb__auma = 0
            for A in arr_list:
                arr = A
                iht__jnf += len(arr)
                asb__auma += bodo.libs.str_arr_ext.num_total_chars(arr)
            out_arr = bodo.utils.utils.alloc_type(iht__jnf, favmc__jwtw, (
                asb__auma,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)
            ghnxi__rsh = 0
            cls__hjhf = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(out_arr, arr,
                    ghnxi__rsh, cls__hjhf)
                ghnxi__rsh += len(arr)
                cls__hjhf += bodo.libs.str_arr_ext.num_total_chars(arr)
            return out_arr
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(kgro__bcuvt.dtype, types.Integer) for
        kgro__bcuvt in arr_list.types) and any(isinstance(kgro__bcuvt,
        IntegerArrayType) for kgro__bcuvt in arr_list.types):

        def impl_int_arr_list(arr_list):
            eex__lono = convert_to_nullable_tup(arr_list)
            pcqf__fbct = []
            fyg__ajeh = 0
            for A in eex__lono:
                pcqf__fbct.append(A._data)
                fyg__ajeh += len(A)
            zifq__vepw = bodo.libs.array_kernels.concat(pcqf__fbct)
            fhsgk__vacr = fyg__ajeh + 7 >> 3
            temfn__tyepv = np.empty(fhsgk__vacr, np.uint8)
            fna__yzexv = 0
            for A in eex__lono:
                ktirk__qpru = A._null_bitmap
                for lowu__ndo in range(len(A)):
                    vwb__atr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        ktirk__qpru, lowu__ndo)
                    bodo.libs.int_arr_ext.set_bit_to_arr(temfn__tyepv,
                        fna__yzexv, vwb__atr)
                    fna__yzexv += 1
            return bodo.libs.int_arr_ext.init_integer_array(zifq__vepw,
                temfn__tyepv)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(kgro__bcuvt.dtype == types.bool_ for
        kgro__bcuvt in arr_list.types) and any(kgro__bcuvt == boolean_array for
        kgro__bcuvt in arr_list.types):

        def impl_bool_arr_list(arr_list):
            eex__lono = convert_to_nullable_tup(arr_list)
            pcqf__fbct = []
            fyg__ajeh = 0
            for A in eex__lono:
                pcqf__fbct.append(A._data)
                fyg__ajeh += len(A)
            zifq__vepw = bodo.libs.array_kernels.concat(pcqf__fbct)
            fhsgk__vacr = fyg__ajeh + 7 >> 3
            temfn__tyepv = np.empty(fhsgk__vacr, np.uint8)
            fna__yzexv = 0
            for A in eex__lono:
                ktirk__qpru = A._null_bitmap
                for lowu__ndo in range(len(A)):
                    vwb__atr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        ktirk__qpru, lowu__ndo)
                    bodo.libs.int_arr_ext.set_bit_to_arr(temfn__tyepv,
                        fna__yzexv, vwb__atr)
                    fna__yzexv += 1
            return bodo.libs.bool_arr_ext.init_bool_array(zifq__vepw,
                temfn__tyepv)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, FloatingArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(kgro__bcuvt.dtype, types.Float) for
        kgro__bcuvt in arr_list.types) and any(isinstance(kgro__bcuvt,
        FloatingArrayType) for kgro__bcuvt in arr_list.types):

        def impl_float_arr_list(arr_list):
            eex__lono = convert_to_nullable_tup(arr_list)
            pcqf__fbct = []
            fyg__ajeh = 0
            for A in eex__lono:
                pcqf__fbct.append(A._data)
                fyg__ajeh += len(A)
            zifq__vepw = bodo.libs.array_kernels.concat(pcqf__fbct)
            fhsgk__vacr = fyg__ajeh + 7 >> 3
            temfn__tyepv = np.empty(fhsgk__vacr, np.uint8)
            fna__yzexv = 0
            for A in eex__lono:
                ktirk__qpru = A._null_bitmap
                for lowu__ndo in range(len(A)):
                    vwb__atr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        ktirk__qpru, lowu__ndo)
                    bodo.libs.int_arr_ext.set_bit_to_arr(temfn__tyepv,
                        fna__yzexv, vwb__atr)
                    fna__yzexv += 1
            return bodo.libs.float_arr_ext.init_float_array(zifq__vepw,
                temfn__tyepv)
        return impl_float_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            wqtiz__wzfi = []
            for A in arr_list:
                wqtiz__wzfi.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                wqtiz__wzfi), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        sajcq__wypu = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        vdbf__babxq = 'def impl(arr_list):\n'
        vdbf__babxq += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({sajcq__wypu}, )), arr_list[0].dtype)
"""
        gmoh__unl = {}
        exec(vdbf__babxq, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, gmoh__unl)
        return gmoh__unl['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            fyg__ajeh = 0
            for A in arr_list:
                fyg__ajeh += len(A)
            out_arr = np.empty(fyg__ajeh, dtype)
            tamxw__cih = 0
            for A in arr_list:
                n = len(A)
                out_arr[tamxw__cih:tamxw__cih + n] = A
                tamxw__cih += n
            return out_arr
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(kgro__bcuvt,
        (types.Array, IntegerArrayType)) and isinstance(kgro__bcuvt.dtype,
        types.Integer) for kgro__bcuvt in arr_list.types) and any(
        isinstance(kgro__bcuvt, types.Array) and isinstance(kgro__bcuvt.
        dtype, types.Float) for kgro__bcuvt in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            xhqwl__ybjr = []
            for A in arr_list:
                xhqwl__ybjr.append(A._data)
            hzxsv__nwqxb = bodo.libs.array_kernels.concat(xhqwl__ybjr)
            jdp__mfp = bodo.libs.map_arr_ext.init_map_arr(hzxsv__nwqxb)
            return jdp__mfp
        return impl_map_arr_list
    if isinstance(arr_list, types.Tuple):
        ved__siy = all([(isinstance(ensdf__abkcz, bodo.DatetimeArrayType) or
            isinstance(ensdf__abkcz, types.Array) and ensdf__abkcz.dtype ==
            bodo.datetime64ns) for ensdf__abkcz in arr_list.types])
        if ved__siy:
            raise BodoError(
                f'Cannot concatenate the rows of Timestamp data with different timezones. Found types: {arr_list}. Please use pd.Series.tz_convert(None) to remove Timezone information.'
                )
    for ensdf__abkcz in arr_list:
        if not isinstance(ensdf__abkcz, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(kgro__bcuvt.astype(np.float64) for kgro__bcuvt in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    zcz__azc = len(arr_tup.types)
    vdbf__babxq = 'def f(arr_tup):\n'
    vdbf__babxq += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(zcz__azc)
        ), ',' if zcz__azc == 1 else '')
    jkle__vzos = {}
    exec(vdbf__babxq, {'np': np}, jkle__vzos)
    vflrm__bagmt = jkle__vzos['f']
    return vflrm__bagmt


def convert_to_nullable_tup(arr_tup):
    pass


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, FloatingArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple
        ), 'convert_to_nullable_tup: tuple expected'
    zcz__azc = len(arr_tup.types)
    rcvyx__tjc = find_common_np_dtype(arr_tup.types)
    eqpx__faxn = None
    umti__fjo = ''
    if isinstance(rcvyx__tjc, types.Integer):
        eqpx__faxn = bodo.libs.int_arr_ext.IntDtype(rcvyx__tjc)
        umti__fjo = '.astype(out_dtype, False)'
    if isinstance(rcvyx__tjc, types.Float
        ) and bodo.libs.float_arr_ext._use_nullable_float:
        eqpx__faxn = bodo.libs.float_arr_ext.FloatDtype(rcvyx__tjc)
        umti__fjo = '.astype(out_dtype, False)'
    vdbf__babxq = 'def f(arr_tup):\n'
    vdbf__babxq += '  return ({}{})\n'.format(','.join(
        f'bodo.utils.conversion.coerce_to_array(arr_tup[{i}], use_nullable_array=True){umti__fjo}'
         for i in range(zcz__azc)), ',' if zcz__azc == 1 else '')
    jkle__vzos = {}
    exec(vdbf__babxq, {'bodo': bodo, 'out_dtype': eqpx__faxn}, jkle__vzos)
    jmxws__sce = jkle__vzos['f']
    return jmxws__sce


def nunique(A, dropna):
    pass


def nunique_parallel(A, dropna):
    pass


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, bmnn__lgjlh = build_set_seen_na(A)
        return len(s) + int(not dropna and bmnn__lgjlh)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        ayun__sdeqg = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        hlvw__uknl = len(ayun__sdeqg)
        return bodo.libs.distributed_api.dist_reduce(hlvw__uknl, np.int32(
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
    cmv__ozlhs = get_overload_const_str(func_name)
    assert cmv__ozlhs in ('cumsum', 'cumprod', 'cummin', 'cummax'
        ), 'accum_func: invalid func_name'
    if cmv__ozlhs == 'cumsum':
        pijs__mxia = A.dtype(0)
        lypj__olqya = np.int32(Reduce_Type.Sum.value)
        pwbcu__vpym = np.add
    if cmv__ozlhs == 'cumprod':
        pijs__mxia = A.dtype(1)
        lypj__olqya = np.int32(Reduce_Type.Prod.value)
        pwbcu__vpym = np.multiply
    if cmv__ozlhs == 'cummin':
        if isinstance(A.dtype, types.Float):
            pijs__mxia = np.finfo(A.dtype(1).dtype).max
        else:
            pijs__mxia = np.iinfo(A.dtype(1).dtype).max
        lypj__olqya = np.int32(Reduce_Type.Min.value)
        pwbcu__vpym = min
    if cmv__ozlhs == 'cummax':
        if isinstance(A.dtype, types.Float):
            pijs__mxia = np.finfo(A.dtype(1).dtype).min
        else:
            pijs__mxia = np.iinfo(A.dtype(1).dtype).min
        lypj__olqya = np.int32(Reduce_Type.Max.value)
        pwbcu__vpym = max
    reqh__ump = A

    def impl(A, func_name, parallel=False):
        n = len(A)
        owtn__wamvk = pijs__mxia
        if parallel:
            for i in range(n):
                if not bodo.libs.array_kernels.isna(A, i):
                    owtn__wamvk = pwbcu__vpym(owtn__wamvk, A[i])
            owtn__wamvk = bodo.libs.distributed_api.dist_exscan(owtn__wamvk,
                lypj__olqya)
            if bodo.get_rank() == 0:
                owtn__wamvk = pijs__mxia
        out_arr = bodo.utils.utils.alloc_type(n, reqh__ump, (-1,))
        for i in range(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(out_arr, i)
                continue
            owtn__wamvk = pwbcu__vpym(owtn__wamvk, A[i])
            out_arr[i] = owtn__wamvk
        return out_arr
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        whxh__men = arr_info_list_to_table([array_to_info(A)])
        ycza__sij = 1
        aeqmb__bbn = 0
        uej__eazyp = drop_duplicates_table(whxh__men, parallel, ycza__sij,
            aeqmb__bbn, dropna, True)
        out_arr = info_to_array(info_from_table(uej__eazyp, 0), A)
        delete_table(whxh__men)
        delete_table(uej__eazyp)
        return out_arr
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    utje__syg = bodo.utils.typing.to_nullable_type(arr.dtype)
    eiydu__gxqji = index_arr
    mrmu__doxs = eiydu__gxqji.dtype

    def impl(arr, index_arr):
        n = len(arr)
        qekkw__ocm = init_nested_counts(utje__syg)
        dwl__qcg = init_nested_counts(mrmu__doxs)
        for i in range(n):
            lmlj__ixztf = index_arr[i]
            if isna(arr, i):
                qekkw__ocm = (qekkw__ocm[0] + 1,) + qekkw__ocm[1:]
                dwl__qcg = add_nested_counts(dwl__qcg, lmlj__ixztf)
                continue
            yppk__iaby = arr[i]
            if len(yppk__iaby) == 0:
                qekkw__ocm = (qekkw__ocm[0] + 1,) + qekkw__ocm[1:]
                dwl__qcg = add_nested_counts(dwl__qcg, lmlj__ixztf)
                continue
            qekkw__ocm = add_nested_counts(qekkw__ocm, yppk__iaby)
            for lngow__qucfd in range(len(yppk__iaby)):
                dwl__qcg = add_nested_counts(dwl__qcg, lmlj__ixztf)
        out_arr = bodo.utils.utils.alloc_type(qekkw__ocm[0], utje__syg,
            qekkw__ocm[1:])
        dlqga__chegl = bodo.utils.utils.alloc_type(qekkw__ocm[0],
            eiydu__gxqji, dwl__qcg)
        zhp__sju = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, zhp__sju)
                dlqga__chegl[zhp__sju] = index_arr[i]
                zhp__sju += 1
                continue
            yppk__iaby = arr[i]
            hil__nzey = len(yppk__iaby)
            if hil__nzey == 0:
                setna(out_arr, zhp__sju)
                dlqga__chegl[zhp__sju] = index_arr[i]
                zhp__sju += 1
                continue
            out_arr[zhp__sju:zhp__sju + hil__nzey] = yppk__iaby
            dlqga__chegl[zhp__sju:zhp__sju + hil__nzey] = index_arr[i]
            zhp__sju += hil__nzey
        return out_arr, dlqga__chegl
    return impl


def explode_no_index(arr):
    pass


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    utje__syg = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        qekkw__ocm = init_nested_counts(utje__syg)
        for i in range(n):
            if isna(arr, i):
                qekkw__ocm = (qekkw__ocm[0] + 1,) + qekkw__ocm[1:]
                qqinj__szzfz = 1
            else:
                yppk__iaby = arr[i]
                vmoqt__qcu = len(yppk__iaby)
                if vmoqt__qcu == 0:
                    qekkw__ocm = (qekkw__ocm[0] + 1,) + qekkw__ocm[1:]
                    qqinj__szzfz = 1
                    continue
                else:
                    qekkw__ocm = add_nested_counts(qekkw__ocm, yppk__iaby)
                    qqinj__szzfz = vmoqt__qcu
            if counts[i] != qqinj__szzfz:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        out_arr = bodo.utils.utils.alloc_type(qekkw__ocm[0], utje__syg,
            qekkw__ocm[1:])
        zhp__sju = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, zhp__sju)
                zhp__sju += 1
                continue
            yppk__iaby = arr[i]
            hil__nzey = len(yppk__iaby)
            if hil__nzey == 0:
                setna(out_arr, zhp__sju)
                zhp__sju += 1
                continue
            out_arr[zhp__sju:zhp__sju + hil__nzey] = yppk__iaby
            zhp__sju += hil__nzey
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
        aklko__ixiyl = 'np.empty(n, np.int64)'
        vywa__qdir = 'out_arr[i] = 1'
        otm__rrah = 'max(len(arr[i]), 1)'
    else:
        aklko__ixiyl = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        vywa__qdir = 'bodo.libs.array_kernels.setna(out_arr, i)'
        otm__rrah = 'len(arr[i])'
    vdbf__babxq = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {aklko__ixiyl}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {vywa__qdir}
        else:
            out_arr[i] = {otm__rrah}
    return out_arr
    """
    jkle__vzos = {}
    exec(vdbf__babxq, {'bodo': bodo, 'numba': numba, 'np': np}, jkle__vzos)
    impl = jkle__vzos['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    pass


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    eiydu__gxqji = index_arr
    mrmu__doxs = eiydu__gxqji.dtype

    def impl(arr, pat, n, index_arr):
        egzq__jdxs = pat is not None and len(pat) > 1
        if egzq__jdxs:
            ptit__mmez = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        dqgvq__idun = len(arr)
        iht__jnf = 0
        asb__auma = 0
        dwl__qcg = init_nested_counts(mrmu__doxs)
        for i in range(dqgvq__idun):
            lmlj__ixztf = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                iht__jnf += 1
                dwl__qcg = add_nested_counts(dwl__qcg, lmlj__ixztf)
                continue
            if egzq__jdxs:
                lda__pfilk = ptit__mmez.split(arr[i], maxsplit=n)
            else:
                lda__pfilk = arr[i].split(pat, n)
            iht__jnf += len(lda__pfilk)
            for s in lda__pfilk:
                dwl__qcg = add_nested_counts(dwl__qcg, lmlj__ixztf)
                asb__auma += bodo.libs.str_arr_ext.get_utf8_size(s)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(iht__jnf,
            asb__auma)
        dlqga__chegl = bodo.utils.utils.alloc_type(iht__jnf, eiydu__gxqji,
            dwl__qcg)
        cqf__ubq = 0
        for lowu__ndo in range(dqgvq__idun):
            if isna(arr, lowu__ndo):
                out_arr[cqf__ubq] = ''
                bodo.libs.array_kernels.setna(out_arr, cqf__ubq)
                dlqga__chegl[cqf__ubq] = index_arr[lowu__ndo]
                cqf__ubq += 1
                continue
            if egzq__jdxs:
                lda__pfilk = ptit__mmez.split(arr[lowu__ndo], maxsplit=n)
            else:
                lda__pfilk = arr[lowu__ndo].split(pat, n)
            ekq__afq = len(lda__pfilk)
            out_arr[cqf__ubq:cqf__ubq + ekq__afq] = lda__pfilk
            dlqga__chegl[cqf__ubq:cqf__ubq + ekq__afq] = index_arr[lowu__ndo]
            cqf__ubq += ekq__afq
        return out_arr, dlqga__chegl
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
            zgji__pnkvr = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            juf__woscl = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(juf__woscl, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(zgji__pnkvr,
                juf__woscl, True, True)
        return impl_dict
    clg__ljsno = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        out_arr = bodo.utils.utils.alloc_type(n, clg__ljsno, (0,))
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
    nipf__iyq = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            out_arr = bodo.utils.utils.alloc_type(new_len, nipf__iyq)
            bodo.libs.str_arr_ext.str_copy_ptr(out_arr.ctypes, 0, A.ctypes,
                old_size)
            return out_arr
        return impl_char

    def impl(A, old_size, new_len):
        out_arr = bodo.utils.utils.alloc_type(new_len, nipf__iyq, (-1,))
        out_arr[:old_size] = A[:old_size]
        return out_arr
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    dtj__cdr = math.ceil((stop - start) / step)
    return int(max(dtj__cdr, 0))


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
    if any(isinstance(iqtek__wsz, types.Complex) for iqtek__wsz in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            ofy__lbdkg = (stop - start) / step
            dtj__cdr = math.ceil(ofy__lbdkg.real)
            xzavs__hpbv = math.ceil(ofy__lbdkg.imag)
            yjc__olclc = int(max(min(xzavs__hpbv, dtj__cdr), 0))
            arr = np.empty(yjc__olclc, dtype)
            for i in numba.parfors.parfor.internal_prange(yjc__olclc):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            yjc__olclc = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(yjc__olclc, dtype)
            for i in numba.parfors.parfor.internal_prange(yjc__olclc):
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
        xpom__nrd = arr,
        if not inplace:
            xpom__nrd = arr.copy(),
        twaae__pss = bodo.libs.str_arr_ext.to_list_if_immutable_arr(xpom__nrd)
        hbvov__bvbks = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data,
            True)
        bodo.libs.timsort.sort(twaae__pss, 0, n, hbvov__bvbks)
        if not ascending:
            bodo.libs.timsort.reverseRange(twaae__pss, 0, n, hbvov__bvbks)
        bodo.libs.str_arr_ext.cp_str_list_to_array(xpom__nrd, twaae__pss)
        return xpom__nrd[0]
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
        jdp__mfp = []
        for i in range(n):
            if A[i]:
                jdp__mfp.append(i + offset)
        return np.array(jdp__mfp, np.int64),
    return impl


def ffill_bfill_arr(arr):
    pass


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    nipf__iyq = element_type(A)
    if nipf__iyq == types.unicode_type:
        null_value = '""'
    elif nipf__iyq == types.bool_:
        null_value = 'False'
    elif nipf__iyq == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_datetime(0))'
            )
    elif nipf__iyq == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_timedelta(0))'
            )
    else:
        null_value = '0'
    cqf__ubq = 'i'
    lndjz__rxfaf = False
    xrij__efgf = get_overload_const_str(method)
    if xrij__efgf in ('ffill', 'pad'):
        dbucc__ohcst = 'n'
        send_right = True
    elif xrij__efgf in ('backfill', 'bfill'):
        dbucc__ohcst = 'n-1, -1, -1'
        send_right = False
        if nipf__iyq == types.unicode_type:
            cqf__ubq = '(n - 1) - i'
            lndjz__rxfaf = True
    vdbf__babxq = 'def impl(A, method, parallel=False):\n'
    vdbf__babxq += '  A = decode_if_dict_array(A)\n'
    vdbf__babxq += '  has_last_value = False\n'
    vdbf__babxq += f'  last_value = {null_value}\n'
    vdbf__babxq += '  if parallel:\n'
    vdbf__babxq += '    rank = bodo.libs.distributed_api.get_rank()\n'
    vdbf__babxq += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    vdbf__babxq += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    vdbf__babxq += '  n = len(A)\n'
    vdbf__babxq += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    vdbf__babxq += f'  for i in range({dbucc__ohcst}):\n'
    vdbf__babxq += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    vdbf__babxq += (
        f'      bodo.libs.array_kernels.setna(out_arr, {cqf__ubq})\n')
    vdbf__babxq += '      continue\n'
    vdbf__babxq += '    s = A[i]\n'
    vdbf__babxq += '    if bodo.libs.array_kernels.isna(A, i):\n'
    vdbf__babxq += '      s = last_value\n'
    vdbf__babxq += f'    out_arr[{cqf__ubq}] = s\n'
    vdbf__babxq += '    last_value = s\n'
    vdbf__babxq += '    has_last_value = True\n'
    if lndjz__rxfaf:
        vdbf__babxq += '  return out_arr[::-1]\n'
    else:
        vdbf__babxq += '  return out_arr\n'
    iabcx__vav = {}
    exec(vdbf__babxq, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, iabcx__vav)
    impl = iabcx__vav['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        olwt__ial = 0
        rer__pfak = n_pes - 1
        nbq__fwlvk = np.int32(rank + 1)
        wuim__gvw = np.int32(rank - 1)
        uca__bnx = len(in_arr) - 1
        dci__zdje = -1
        oacp__blor = -1
    else:
        olwt__ial = n_pes - 1
        rer__pfak = 0
        nbq__fwlvk = np.int32(rank - 1)
        wuim__gvw = np.int32(rank + 1)
        uca__bnx = 0
        dci__zdje = len(in_arr)
        oacp__blor = 1
    kyg__zeqp = np.int32(bodo.hiframes.rolling.comm_border_tag)
    jmn__rdfd = np.empty(1, dtype=np.bool_)
    mxiuu__bkm = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    yjq__xibu = np.empty(1, dtype=np.bool_)
    eplci__yrn = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    ncx__rjnhn = False
    ottlb__rfho = null_value
    for i in range(uca__bnx, dci__zdje, oacp__blor):
        if not isna(in_arr, i):
            ncx__rjnhn = True
            ottlb__rfho = in_arr[i]
            break
    if rank != olwt__ial:
        zlqo__qujwu = bodo.libs.distributed_api.irecv(jmn__rdfd, 1,
            wuim__gvw, kyg__zeqp, True)
        bodo.libs.distributed_api.wait(zlqo__qujwu, True)
        zshm__hpw = bodo.libs.distributed_api.irecv(mxiuu__bkm, 1,
            wuim__gvw, kyg__zeqp, True)
        bodo.libs.distributed_api.wait(zshm__hpw, True)
        cway__yjib = jmn__rdfd[0]
        khv__emx = mxiuu__bkm[0]
    else:
        cway__yjib = False
        khv__emx = null_value
    if ncx__rjnhn:
        yjq__xibu[0] = ncx__rjnhn
        eplci__yrn[0] = ottlb__rfho
    else:
        yjq__xibu[0] = cway__yjib
        eplci__yrn[0] = khv__emx
    if rank != rer__pfak:
        vwsv__xnnyq = bodo.libs.distributed_api.isend(yjq__xibu, 1,
            nbq__fwlvk, kyg__zeqp, True)
        wcwlo__sgxaj = bodo.libs.distributed_api.isend(eplci__yrn, 1,
            nbq__fwlvk, kyg__zeqp, True)
    return cway__yjib, khv__emx


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    yluxu__eqght = {'axis': axis, 'kind': kind, 'order': order}
    skm__abbow = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', yluxu__eqght, skm__abbow, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    pass


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    nipf__iyq = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                gztg__cmyoj = A._indices
                dqgvq__idun = len(gztg__cmyoj)
                potdr__tscib = alloc_int_array(dqgvq__idun * repeats, np.int32)
                for i in range(dqgvq__idun):
                    cqf__ubq = i * repeats
                    if bodo.libs.array_kernels.isna(gztg__cmyoj, i):
                        for lowu__ndo in range(repeats):
                            bodo.libs.array_kernels.setna(potdr__tscib, 
                                cqf__ubq + lowu__ndo)
                    else:
                        potdr__tscib[cqf__ubq:cqf__ubq + repeats
                            ] = gztg__cmyoj[i]
                return init_dict_arr(data_arr, potdr__tscib, A.
                    _has_global_dictionary, A._has_deduped_local_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            dqgvq__idun = len(A)
            out_arr = bodo.utils.utils.alloc_type(dqgvq__idun * repeats,
                nipf__iyq, (-1,))
            for i in range(dqgvq__idun):
                cqf__ubq = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for lowu__ndo in range(repeats):
                        bodo.libs.array_kernels.setna(out_arr, cqf__ubq +
                            lowu__ndo)
                else:
                    out_arr[cqf__ubq:cqf__ubq + repeats] = A[i]
            return out_arr
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            gztg__cmyoj = A._indices
            dqgvq__idun = len(gztg__cmyoj)
            potdr__tscib = alloc_int_array(repeats.sum(), np.int32)
            cqf__ubq = 0
            for i in range(dqgvq__idun):
                zddh__kfj = repeats[i]
                if zddh__kfj < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(gztg__cmyoj, i):
                    for lowu__ndo in range(zddh__kfj):
                        bodo.libs.array_kernels.setna(potdr__tscib, 
                            cqf__ubq + lowu__ndo)
                else:
                    potdr__tscib[cqf__ubq:cqf__ubq + zddh__kfj] = gztg__cmyoj[i
                        ]
                cqf__ubq += zddh__kfj
            return init_dict_arr(data_arr, potdr__tscib, A.
                _has_global_dictionary, A._has_deduped_local_dictionary)
        return impl_dict_arr

    def impl_arr(A, repeats):
        dqgvq__idun = len(A)
        out_arr = bodo.utils.utils.alloc_type(repeats.sum(), nipf__iyq, (-1,))
        cqf__ubq = 0
        for i in range(dqgvq__idun):
            zddh__kfj = repeats[i]
            if zddh__kfj < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for lowu__ndo in range(zddh__kfj):
                    bodo.libs.array_kernels.setna(out_arr, cqf__ubq + lowu__ndo
                        )
            else:
                out_arr[cqf__ubq:cqf__ubq + zddh__kfj] = A[i]
            cqf__ubq += zddh__kfj
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
        oko__onib = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(oko__onib, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        aof__tygv = bodo.libs.array_kernels.concat([A1, A2])
        vewmz__brg = bodo.libs.array_kernels.unique(aof__tygv)
        return pd.Series(vewmz__brg).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    yluxu__eqght = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    skm__abbow = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', yluxu__eqght, skm__abbow, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        oyr__xsvef = bodo.libs.array_kernels.unique(A1)
        fza__dujvq = bodo.libs.array_kernels.unique(A2)
        aof__tygv = bodo.libs.array_kernels.concat([oyr__xsvef, fza__dujvq])
        iqjrq__rfjyh = pd.Series(aof__tygv).sort_values().values
        return slice_array_intersect1d(iqjrq__rfjyh)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    qsee__ddo = arr[1:] == arr[:-1]
    return arr[:-1][qsee__ddo]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    kyg__zeqp = np.int32(bodo.hiframes.rolling.comm_border_tag)
    frlbj__oxiw = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        hkf__iap = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32(
            rank - 1), kyg__zeqp, True)
        bodo.libs.distributed_api.wait(hkf__iap, True)
    if rank == n_pes - 1:
        return None
    else:
        tzkbs__rdc = bodo.libs.distributed_api.irecv(frlbj__oxiw, 1, np.
            int32(rank + 1), kyg__zeqp, True)
        bodo.libs.distributed_api.wait(tzkbs__rdc, True)
        return frlbj__oxiw[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    qsee__ddo = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            qsee__ddo[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        jndo__coe = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == jndo__coe:
            qsee__ddo[n - 1] = True
    return qsee__ddo


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    yluxu__eqght = {'assume_unique': assume_unique}
    skm__abbow = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', yluxu__eqght, skm__abbow, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        oyr__xsvef = bodo.libs.array_kernels.unique(A1)
        fza__dujvq = bodo.libs.array_kernels.unique(A2)
        qsee__ddo = calculate_mask_setdiff1d(oyr__xsvef, fza__dujvq)
        return pd.Series(oyr__xsvef[qsee__ddo]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    qsee__ddo = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        qsee__ddo &= A1 != A2[i]
    return qsee__ddo


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    yluxu__eqght = {'retstep': retstep, 'axis': axis}
    skm__abbow = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', yluxu__eqght, skm__abbow, 'numpy')
    toj__wvmys = False
    if is_overload_none(dtype):
        nipf__iyq = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            toj__wvmys = True
        nipf__iyq = numba.np.numpy_support.as_dtype(dtype).type
    if toj__wvmys:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            mft__egnu = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, nipf__iyq)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = nipf__iyq(np.floor(start + i * mft__egnu))
            return out_arr
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            mft__egnu = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, nipf__iyq)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = nipf__iyq(start + i * mft__egnu)
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
        zcz__azc = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                zcz__azc += A[i] == val
        return zcz__azc > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    yluxu__eqght = {'axis': axis, 'out': out, 'keepdims': keepdims}
    skm__abbow = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', yluxu__eqght, skm__abbow, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        zcz__azc = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                zcz__azc += int(bool(A[i]))
        return zcz__azc > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    yluxu__eqght = {'axis': axis, 'out': out, 'keepdims': keepdims}
    skm__abbow = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', yluxu__eqght, skm__abbow, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        zcz__azc = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                zcz__azc += int(bool(A[i]))
        return zcz__azc == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    yluxu__eqght = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    skm__abbow = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', yluxu__eqght, skm__abbow, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        yduyz__jdcrj = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            out_arr = np.empty(n, yduyz__jdcrj)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(out_arr, i)
                    continue
                out_arr[i] = np_cbrt_scalar(A[i], yduyz__jdcrj)
            return out_arr
        return impl_arr
    yduyz__jdcrj = np.promote_types(numba.np.numpy_support.as_dtype(A),
        numba.np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, yduyz__jdcrj)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    uatk__wxu = x < 0
    if uatk__wxu:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if uatk__wxu:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    tnd__fzxn = isinstance(tup, (types.BaseTuple, types.List))
    sfof__tjx = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for ensdf__abkcz in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                ensdf__abkcz, 'numpy.hstack()')
            tnd__fzxn = tnd__fzxn and bodo.utils.utils.is_array_typ(
                ensdf__abkcz, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        tnd__fzxn = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif sfof__tjx:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        whie__tvc = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for ensdf__abkcz in whie__tvc.types:
            sfof__tjx = sfof__tjx and bodo.utils.utils.is_array_typ(
                ensdf__abkcz, False)
    if not (tnd__fzxn or sfof__tjx):
        return
    if sfof__tjx:

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
    yluxu__eqght = {'check_valid': check_valid, 'tol': tol}
    skm__abbow = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', yluxu__eqght,
        skm__abbow, 'numpy')
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
        odued__oapoe = mean.shape[0]
        yldy__csi = size, odued__oapoe
        czxxc__uywg = np.random.standard_normal(yldy__csi)
        cov = cov.astype(np.float64)
        ncn__ileyl, s, erk__vbwb = np.linalg.svd(cov)
        res = np.dot(czxxc__uywg, np.sqrt(s).reshape(odued__oapoe, 1) *
            erk__vbwb)
        nac__ejs = res + mean
        return nac__ejs
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
            tdw__lnl = bodo.hiframes.series_kernels._get_type_max_value(arr)
            xrf__xwkx = typing.builtins.IndexValue(-1, tdw__lnl)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                amhf__uzho = typing.builtins.IndexValue(i, arr[i])
                xrf__xwkx = min(xrf__xwkx, amhf__uzho)
            return xrf__xwkx.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        mpshj__tfrb = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            tfywc__cfoeo = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            tdw__lnl = mpshj__tfrb(len(arr.dtype.categories) + 1)
            xrf__xwkx = typing.builtins.IndexValue(-1, tdw__lnl)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                amhf__uzho = typing.builtins.IndexValue(i, tfywc__cfoeo[i])
                xrf__xwkx = min(xrf__xwkx, amhf__uzho)
            return xrf__xwkx.index
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
            tdw__lnl = bodo.hiframes.series_kernels._get_type_min_value(arr)
            xrf__xwkx = typing.builtins.IndexValue(-1, tdw__lnl)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                amhf__uzho = typing.builtins.IndexValue(i, arr[i])
                xrf__xwkx = max(xrf__xwkx, amhf__uzho)
            return xrf__xwkx.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        mpshj__tfrb = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            tfywc__cfoeo = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            tdw__lnl = mpshj__tfrb(-1)
            xrf__xwkx = typing.builtins.IndexValue(-1, tdw__lnl)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                amhf__uzho = typing.builtins.IndexValue(i, tfywc__cfoeo[i])
                xrf__xwkx = max(xrf__xwkx, amhf__uzho)
            return xrf__xwkx.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
