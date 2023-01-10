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
        pkq__ilw = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = pkq__ilw
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        pkq__ilw = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = pkq__ilw
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
            newnj__iam = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            newnj__iam[ind + 1] = newnj__iam[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            newnj__iam = bodo.libs.array_item_arr_ext.get_offsets(arr)
            newnj__iam[ind + 1] = newnj__iam[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            newnj__iam = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            newnj__iam[ind + 1] = newnj__iam[ind]
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
    krr__byae = arr_tup.count
    yke__iqx = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(krr__byae):
        yke__iqx += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    yke__iqx += '  return\n'
    rhjg__sddw = {}
    exec(yke__iqx, {'setna': setna}, rhjg__sddw)
    impl = rhjg__sddw['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        flzcx__uzcv = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(flzcx__uzcv.start, flzcx__uzcv.stop, flzcx__uzcv.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        qowy__sfrp = 'n'
        zhsjm__inhrf = 'n_pes'
        cjd__ruwty = 'min_op'
    else:
        qowy__sfrp = 'n-1, -1, -1'
        zhsjm__inhrf = '-1'
        cjd__ruwty = 'max_op'
    yke__iqx = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {zhsjm__inhrf}
    for i in range({qowy__sfrp}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {cjd__ruwty}))
        if possible_valid_rank != {zhsjm__inhrf}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    rhjg__sddw = {}
    exec(yke__iqx, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op': max_op,
        'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.box_if_dt64},
        rhjg__sddw)
    impl = rhjg__sddw['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    ouvd__lmkhy = array_to_info(arr)
    _median_series_computation(res, ouvd__lmkhy, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(ouvd__lmkhy)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    ouvd__lmkhy = array_to_info(arr)
    _autocorr_series_computation(res, ouvd__lmkhy, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(ouvd__lmkhy)


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
    ouvd__lmkhy = array_to_info(arr)
    _compute_series_monotonicity(res, ouvd__lmkhy, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(ouvd__lmkhy)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    xst__qoply = res[0] > 0.5
    return xst__qoply


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        ecd__cgy = '-'
        woh__vlfyb = 'index_arr[0] > threshhold_date'
        qowy__sfrp = '1, n+1'
        jnxfj__vtgo = 'index_arr[-i] <= threshhold_date'
        mpm__yzvn = 'i - 1'
    else:
        ecd__cgy = '+'
        woh__vlfyb = 'index_arr[-1] < threshhold_date'
        qowy__sfrp = 'n'
        jnxfj__vtgo = 'index_arr[i] >= threshhold_date'
        mpm__yzvn = 'i'
    yke__iqx = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        yke__iqx += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_tz_naive_type):\n'
            )
        yke__iqx += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            yke__iqx += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            yke__iqx += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            yke__iqx += '    else:\n'
            yke__iqx += '      threshhold_date = initial_date + date_offset\n'
        else:
            yke__iqx += (
                f'    threshhold_date = initial_date {ecd__cgy} date_offset\n')
    else:
        yke__iqx += f'  threshhold_date = initial_date {ecd__cgy} offset\n'
    yke__iqx += '  local_valid = 0\n'
    yke__iqx += f'  n = len(index_arr)\n'
    yke__iqx += f'  if n:\n'
    yke__iqx += f'    if {woh__vlfyb}:\n'
    yke__iqx += '      loc_valid = n\n'
    yke__iqx += '    else:\n'
    yke__iqx += f'      for i in range({qowy__sfrp}):\n'
    yke__iqx += f'        if {jnxfj__vtgo}:\n'
    yke__iqx += f'          loc_valid = {mpm__yzvn}\n'
    yke__iqx += '          break\n'
    yke__iqx += '  if is_parallel:\n'
    yke__iqx += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    yke__iqx += '    return total_valid\n'
    yke__iqx += '  else:\n'
    yke__iqx += '    return loc_valid\n'
    rhjg__sddw = {}
    exec(yke__iqx, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, rhjg__sddw)
    return rhjg__sddw['impl']


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
    usms__enzr = numba_to_c_type(sig.args[0].dtype)
    fyem__rxwz = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), usms__enzr))
    vzq__evrzv = args[0]
    clf__hjjs = sig.args[0]
    if isinstance(clf__hjjs, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        vzq__evrzv = cgutils.create_struct_proxy(clf__hjjs)(context,
            builder, vzq__evrzv).data
        clf__hjjs = types.Array(clf__hjjs.dtype, 1, 'C')
    assert clf__hjjs.ndim == 1
    arr = make_array(clf__hjjs)(context, builder, vzq__evrzv)
    iqgpr__pxvdh = builder.extract_value(arr.shape, 0)
    drix__fkcc = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        iqgpr__pxvdh, args[1], builder.load(fyem__rxwz)]
    rzdx__diffl = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    mtx__zwhu = lir.FunctionType(lir.DoubleType(), rzdx__diffl)
    ivb__yxt = cgutils.get_or_insert_function(builder.module, mtx__zwhu,
        name='quantile_sequential')
    dwmq__nhtpq = builder.call(ivb__yxt, drix__fkcc)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return dwmq__nhtpq


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, FloatingArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    usms__enzr = numba_to_c_type(sig.args[0].dtype)
    fyem__rxwz = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), usms__enzr))
    vzq__evrzv = args[0]
    clf__hjjs = sig.args[0]
    if isinstance(clf__hjjs, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        vzq__evrzv = cgutils.create_struct_proxy(clf__hjjs)(context,
            builder, vzq__evrzv).data
        clf__hjjs = types.Array(clf__hjjs.dtype, 1, 'C')
    assert clf__hjjs.ndim == 1
    arr = make_array(clf__hjjs)(context, builder, vzq__evrzv)
    iqgpr__pxvdh = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        otn__qqn = args[2]
    else:
        otn__qqn = iqgpr__pxvdh
    drix__fkcc = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        iqgpr__pxvdh, otn__qqn, args[1], builder.load(fyem__rxwz)]
    rzdx__diffl = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        IntType(64), lir.DoubleType(), lir.IntType(32)]
    mtx__zwhu = lir.FunctionType(lir.DoubleType(), rzdx__diffl)
    ivb__yxt = cgutils.get_or_insert_function(builder.module, mtx__zwhu,
        name='quantile_parallel')
    dwmq__nhtpq = builder.call(ivb__yxt, drix__fkcc)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return dwmq__nhtpq


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        n = len(arr)
        rrfe__ncnsr = bodo.utils.utils.alloc_type(n, np.bool_, (-1,))
        rrfe__ncnsr[0] = True
        osfhl__isebq = pd.isna(arr)
        for i in range(1, len(arr)):
            if osfhl__isebq[i] and osfhl__isebq[i - 1]:
                rrfe__ncnsr[i] = False
            elif osfhl__isebq[i] or osfhl__isebq[i - 1]:
                rrfe__ncnsr[i] = True
            else:
                rrfe__ncnsr[i] = arr[i] != arr[i - 1]
        return rrfe__ncnsr
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
    yke__iqx = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    yke__iqx += '  na_idxs = pd.isna(arr)\n'
    yke__iqx += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    yke__iqx += '  nas = sum(na_idxs)\n'
    if not ascending:
        yke__iqx += '  if nas and nas < (sorter.size - 1):\n'
        yke__iqx += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        yke__iqx += '  else:\n'
        yke__iqx += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        yke__iqx += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    yke__iqx += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    yke__iqx += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        yke__iqx += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        yke__iqx += '    inv,\n'
        yke__iqx += '    new_dtype=np.float64,\n'
        yke__iqx += '    copy=True,\n'
        yke__iqx += '    nan_to_str=False,\n'
        yke__iqx += '    from_series=True,\n'
        yke__iqx += '    ) + 1\n'
    else:
        yke__iqx += '  arr = arr[sorter]\n'
        yke__iqx += '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n'
        yke__iqx += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            yke__iqx += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            yke__iqx += '    dense,\n'
            yke__iqx += '    new_dtype=np.float64,\n'
            yke__iqx += '    copy=True,\n'
            yke__iqx += '    nan_to_str=False,\n'
            yke__iqx += '    from_series=True,\n'
            yke__iqx += '  )\n'
        else:
            yke__iqx += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            yke__iqx += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                yke__iqx += '  ret = count_float[dense]\n'
            elif method == 'min':
                yke__iqx += '  ret = count_float[dense - 1] + 1\n'
            else:
                yke__iqx += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                yke__iqx += '  ret[na_idxs] = -1\n'
            yke__iqx += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            yke__iqx += '  div_val = arr.size - nas\n'
        else:
            yke__iqx += '  div_val = arr.size\n'
        yke__iqx += '  for i in range(len(ret)):\n'
        yke__iqx += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        yke__iqx += '  ret[na_idxs] = np.nan\n'
    yke__iqx += '  return ret\n'
    rhjg__sddw = {}
    exec(yke__iqx, {'np': np, 'pd': pd, 'bodo': bodo}, rhjg__sddw)
    return rhjg__sddw['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    agoj__jfyph = start
    zrr__amw = 2 * start + 1
    ktoa__fazuf = 2 * start + 2
    if zrr__amw < n and not cmp_f(arr[zrr__amw], arr[agoj__jfyph]):
        agoj__jfyph = zrr__amw
    if ktoa__fazuf < n and not cmp_f(arr[ktoa__fazuf], arr[agoj__jfyph]):
        agoj__jfyph = ktoa__fazuf
    if agoj__jfyph != start:
        arr[start], arr[agoj__jfyph] = arr[agoj__jfyph], arr[start]
        ind_arr[start], ind_arr[agoj__jfyph] = ind_arr[agoj__jfyph], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, agoj__jfyph, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        sgmg__oes = np.empty(k, A.dtype)
        lnho__ekf = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                sgmg__oes[ind] = A[i]
                lnho__ekf[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            sgmg__oes = sgmg__oes[:ind]
            lnho__ekf = lnho__ekf[:ind]
        return sgmg__oes, lnho__ekf, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        jrdj__vwr = np.sort(A)
        vem__uas = index_arr[np.argsort(A)]
        hxrtx__xchk = pd.Series(jrdj__vwr).notna().values
        jrdj__vwr = jrdj__vwr[hxrtx__xchk]
        vem__uas = vem__uas[hxrtx__xchk]
        if is_largest:
            jrdj__vwr = jrdj__vwr[::-1]
            vem__uas = vem__uas[::-1]
        return np.ascontiguousarray(jrdj__vwr), np.ascontiguousarray(vem__uas)
    sgmg__oes, lnho__ekf, start = select_k_nonan(A, index_arr, m, k)
    lnho__ekf = lnho__ekf[sgmg__oes.argsort()]
    sgmg__oes.sort()
    if not is_largest:
        sgmg__oes = np.ascontiguousarray(sgmg__oes[::-1])
        lnho__ekf = np.ascontiguousarray(lnho__ekf[::-1])
    for i in range(start, m):
        if cmp_f(A[i], sgmg__oes[0]):
            sgmg__oes[0] = A[i]
            lnho__ekf[0] = index_arr[i]
            min_heapify(sgmg__oes, lnho__ekf, k, 0, cmp_f)
    lnho__ekf = lnho__ekf[sgmg__oes.argsort()]
    sgmg__oes.sort()
    if is_largest:
        sgmg__oes = sgmg__oes[::-1]
        lnho__ekf = lnho__ekf[::-1]
    return np.ascontiguousarray(sgmg__oes), np.ascontiguousarray(lnho__ekf)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    ljm__kxxbs = bodo.libs.distributed_api.get_rank()
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    lfp__gdgjx, dwq__efv = nlargest(A, I, k, is_largest, cmp_f)
    pew__epnbc = bodo.libs.distributed_api.gatherv(lfp__gdgjx)
    zialw__lem = bodo.libs.distributed_api.gatherv(dwq__efv)
    if ljm__kxxbs == MPI_ROOT:
        res, watj__fldi = nlargest(pew__epnbc, zialw__lem, k, is_largest, cmp_f
            )
    else:
        res = np.empty(k, A.dtype)
        watj__fldi = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(watj__fldi)
    return res, watj__fldi


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    vznf__tyios, hwtsa__otuw = mat.shape
    qlyyh__ufh = np.empty((hwtsa__otuw, hwtsa__otuw), dtype=np.float64)
    for ibpv__knneq in range(hwtsa__otuw):
        for lnyw__xso in range(ibpv__knneq + 1):
            wkmgt__osmvl = 0
            ubq__jwcgq = xja__xepzu = uma__jzpkg = qce__dkbkr = 0.0
            for i in range(vznf__tyios):
                if np.isfinite(mat[i, ibpv__knneq]) and np.isfinite(mat[i,
                    lnyw__xso]):
                    etfo__hatjj = mat[i, ibpv__knneq]
                    rywei__rke = mat[i, lnyw__xso]
                    wkmgt__osmvl += 1
                    uma__jzpkg += etfo__hatjj
                    qce__dkbkr += rywei__rke
            if parallel:
                wkmgt__osmvl = bodo.libs.distributed_api.dist_reduce(
                    wkmgt__osmvl, sum_op)
                uma__jzpkg = bodo.libs.distributed_api.dist_reduce(uma__jzpkg,
                    sum_op)
                qce__dkbkr = bodo.libs.distributed_api.dist_reduce(qce__dkbkr,
                    sum_op)
            if wkmgt__osmvl < minpv:
                qlyyh__ufh[ibpv__knneq, lnyw__xso] = qlyyh__ufh[lnyw__xso,
                    ibpv__knneq] = np.nan
            else:
                lxcx__zip = uma__jzpkg / wkmgt__osmvl
                dvq__afq = qce__dkbkr / wkmgt__osmvl
                uma__jzpkg = 0.0
                for i in range(vznf__tyios):
                    if np.isfinite(mat[i, ibpv__knneq]) and np.isfinite(mat
                        [i, lnyw__xso]):
                        etfo__hatjj = mat[i, ibpv__knneq] - lxcx__zip
                        rywei__rke = mat[i, lnyw__xso] - dvq__afq
                        uma__jzpkg += etfo__hatjj * rywei__rke
                        ubq__jwcgq += etfo__hatjj * etfo__hatjj
                        xja__xepzu += rywei__rke * rywei__rke
                if parallel:
                    uma__jzpkg = bodo.libs.distributed_api.dist_reduce(
                        uma__jzpkg, sum_op)
                    ubq__jwcgq = bodo.libs.distributed_api.dist_reduce(
                        ubq__jwcgq, sum_op)
                    xja__xepzu = bodo.libs.distributed_api.dist_reduce(
                        xja__xepzu, sum_op)
                tcidf__epcg = wkmgt__osmvl - 1.0 if cov else sqrt(
                    ubq__jwcgq * xja__xepzu)
                if tcidf__epcg != 0.0:
                    qlyyh__ufh[ibpv__knneq, lnyw__xso] = qlyyh__ufh[
                        lnyw__xso, ibpv__knneq] = uma__jzpkg / tcidf__epcg
                else:
                    qlyyh__ufh[ibpv__knneq, lnyw__xso] = qlyyh__ufh[
                        lnyw__xso, ibpv__knneq] = np.nan
    return qlyyh__ufh


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    tcp__eqb = n != 1
    yke__iqx = 'def impl(data, parallel=False):\n'
    yke__iqx += '  if parallel:\n'
    sjhy__uqek = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    yke__iqx += f'    cpp_table = arr_info_list_to_table([{sjhy__uqek}])\n'
    yke__iqx += (
        f'    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)\n'
        )
    ulf__qrf = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    yke__iqx += f'    data = ({ulf__qrf},)\n'
    yke__iqx += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    yke__iqx += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    yke__iqx += '    bodo.libs.array.delete_table(cpp_table)\n'
    yke__iqx += '  n = len(data[0])\n'
    yke__iqx += '  out = np.empty(n, np.bool_)\n'
    yke__iqx += '  uniqs = dict()\n'
    if tcp__eqb:
        yke__iqx += '  for i in range(n):\n'
        tkwt__veg = ', '.join(f'data[{i}][i]' for i in range(n))
        ovy__zttbq = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        yke__iqx += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({tkwt__veg},), ({ovy__zttbq},))
"""
        yke__iqx += '    if val in uniqs:\n'
        yke__iqx += '      out[i] = True\n'
        yke__iqx += '    else:\n'
        yke__iqx += '      out[i] = False\n'
        yke__iqx += '      uniqs[val] = 0\n'
    else:
        yke__iqx += '  data = data[0]\n'
        yke__iqx += '  hasna = False\n'
        yke__iqx += '  for i in range(n):\n'
        yke__iqx += '    if bodo.libs.array_kernels.isna(data, i):\n'
        yke__iqx += '      out[i] = hasna\n'
        yke__iqx += '      hasna = True\n'
        yke__iqx += '    else:\n'
        yke__iqx += '      val = data[i]\n'
        yke__iqx += '      if val in uniqs:\n'
        yke__iqx += '        out[i] = True\n'
        yke__iqx += '      else:\n'
        yke__iqx += '        out[i] = False\n'
        yke__iqx += '        uniqs[val] = 0\n'
    yke__iqx += '  if parallel:\n'
    yke__iqx += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    yke__iqx += '  return out\n'
    rhjg__sddw = {}
    exec(yke__iqx, {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table}, rhjg__sddw)
    impl = rhjg__sddw['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    pass


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    krr__byae = len(data)
    yke__iqx = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    yke__iqx += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        krr__byae)))
    yke__iqx += '  table_total = arr_info_list_to_table(info_list_total)\n'
    yke__iqx += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(krr__byae))
    for ynakl__mihuu in range(krr__byae):
        yke__iqx += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(ynakl__mihuu, ynakl__mihuu, ynakl__mihuu))
    yke__iqx += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(krr__byae))
    yke__iqx += '  delete_table(out_table)\n'
    yke__iqx += '  delete_table(table_total)\n'
    yke__iqx += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(krr__byae)))
    rhjg__sddw = {}
    exec(yke__iqx, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, rhjg__sddw)
    impl = rhjg__sddw['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    pass


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    krr__byae = len(data)
    yke__iqx = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    yke__iqx += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        krr__byae)))
    yke__iqx += '  table_total = arr_info_list_to_table(info_list_total)\n'
    yke__iqx += '  keep_i = 0\n'
    yke__iqx += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for ynakl__mihuu in range(krr__byae):
        yke__iqx += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(ynakl__mihuu, ynakl__mihuu, ynakl__mihuu))
    yke__iqx += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(krr__byae))
    yke__iqx += '  delete_table(out_table)\n'
    yke__iqx += '  delete_table(table_total)\n'
    yke__iqx += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(krr__byae)))
    rhjg__sddw = {}
    exec(yke__iqx, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, rhjg__sddw)
    impl = rhjg__sddw['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    pass


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        qnxk__ztbo = [array_to_info(data_arr)]
        jxil__kyc = arr_info_list_to_table(qnxk__ztbo)
        nio__tmrq = 0
        raum__ojw = drop_duplicates_table(jxil__kyc, parallel, 1, nio__tmrq,
            False, True)
        out_arr = info_to_array(info_from_table(raum__ojw, 0), data_arr)
        delete_table(raum__ojw)
        delete_table(jxil__kyc)
        return out_arr
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    pass


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    zau__qbcow = len(data.types)
    tkkf__gpi = [('out' + str(i)) for i in range(zau__qbcow)]
    mnok__lvlxh = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    xsa__dsbkx = ['isna(data[{}], i)'.format(i) for i in mnok__lvlxh]
    gplt__wmui = 'not ({})'.format(' or '.join(xsa__dsbkx))
    if not is_overload_none(thresh):
        gplt__wmui = '(({}) <= ({}) - thresh)'.format(' + '.join(xsa__dsbkx
            ), zau__qbcow - 1)
    elif how == 'all':
        gplt__wmui = 'not ({})'.format(' and '.join(xsa__dsbkx))
    yke__iqx = 'def _dropna_imp(data, how, thresh, subset):\n'
    yke__iqx += '  old_len = len(data[0])\n'
    yke__iqx += '  new_len = 0\n'
    yke__iqx += '  for i in range(old_len):\n'
    yke__iqx += '    if {}:\n'.format(gplt__wmui)
    yke__iqx += '      new_len += 1\n'
    for i, out in enumerate(tkkf__gpi):
        if isinstance(data[i], bodo.CategoricalArrayType):
            yke__iqx += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            yke__iqx += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    yke__iqx += '  curr_ind = 0\n'
    yke__iqx += '  for i in range(old_len):\n'
    yke__iqx += '    if {}:\n'.format(gplt__wmui)
    for i in range(zau__qbcow):
        yke__iqx += '      if isna(data[{}], i):\n'.format(i)
        yke__iqx += '        setna({}, curr_ind)\n'.format(tkkf__gpi[i])
        yke__iqx += '      else:\n'
        yke__iqx += '        {}[curr_ind] = data[{}][i]\n'.format(tkkf__gpi
            [i], i)
    yke__iqx += '      curr_ind += 1\n'
    yke__iqx += '  return {}\n'.format(', '.join(tkkf__gpi))
    rhjg__sddw = {}
    cyfy__blgm = {'t{}'.format(i): wirl__btsnu for i, wirl__btsnu in
        enumerate(data.types)}
    cyfy__blgm.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(yke__iqx, cyfy__blgm, rhjg__sddw)
    giha__hmag = rhjg__sddw['_dropna_imp']
    return giha__hmag


def get(arr, ind):
    pass


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        clf__hjjs = arr.dtype
        btzyn__qrc = clf__hjjs.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            jozcb__ddz = init_nested_counts(btzyn__qrc)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                jozcb__ddz = add_nested_counts(jozcb__ddz, val[ind])
            out_arr = bodo.utils.utils.alloc_type(n, clf__hjjs, jozcb__ddz)
            for hhmh__pfrg in range(n):
                if bodo.libs.array_kernels.isna(arr, hhmh__pfrg):
                    setna(out_arr, hhmh__pfrg)
                    continue
                val = arr[hhmh__pfrg]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(out_arr, hhmh__pfrg)
                    continue
                out_arr[hhmh__pfrg] = val[ind]
            return out_arr
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    ibm__awgvf = _to_readonly(arr_types.types[0])
    return all(isinstance(wirl__btsnu, CategoricalArrayType) and 
        _to_readonly(wirl__btsnu) == ibm__awgvf for wirl__btsnu in
        arr_types.types)


def concat(arr_list):
    pass


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        hjva__zxg = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            wxlt__kaint = 0
            cbhhe__ohnxl = []
            for A in arr_list:
                prmp__xdi = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                cbhhe__ohnxl.append(bodo.libs.array_item_arr_ext.get_data(A))
                wxlt__kaint += prmp__xdi
            ixk__rwt = np.empty(wxlt__kaint + 1, offset_type)
            qwwr__glq = bodo.libs.array_kernels.concat(cbhhe__ohnxl)
            vbm__tkpsa = np.empty(wxlt__kaint + 7 >> 3, np.uint8)
            qomu__rhj = 0
            jjrs__omgf = 0
            for A in arr_list:
                ybt__ckpb = bodo.libs.array_item_arr_ext.get_offsets(A)
                pzmsv__nlyxj = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                prmp__xdi = len(A)
                jzkkq__ocu = ybt__ckpb[prmp__xdi]
                for i in range(prmp__xdi):
                    ixk__rwt[i + qomu__rhj] = ybt__ckpb[i] + jjrs__omgf
                    ropj__fjnl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        pzmsv__nlyxj, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vbm__tkpsa, i +
                        qomu__rhj, ropj__fjnl)
                qomu__rhj += prmp__xdi
                jjrs__omgf += jzkkq__ocu
            ixk__rwt[qomu__rhj] = jjrs__omgf
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                wxlt__kaint, qwwr__glq, ixk__rwt, vbm__tkpsa)
            return out_arr
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        kbhm__rdzny = arr_list.dtype.names
        yke__iqx = 'def struct_array_concat_impl(arr_list):\n'
        yke__iqx += f'    n_all = 0\n'
        for i in range(len(kbhm__rdzny)):
            yke__iqx += f'    concat_list{i} = []\n'
        yke__iqx += '    for A in arr_list:\n'
        yke__iqx += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(kbhm__rdzny)):
            yke__iqx += f'        concat_list{i}.append(data_tuple[{i}])\n'
        yke__iqx += '        n_all += len(A)\n'
        yke__iqx += '    n_bytes = (n_all + 7) >> 3\n'
        yke__iqx += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        yke__iqx += '    curr_bit = 0\n'
        yke__iqx += '    for A in arr_list:\n'
        yke__iqx += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        yke__iqx += '        for j in range(len(A)):\n'
        yke__iqx += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        yke__iqx += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        yke__iqx += '            curr_bit += 1\n'
        yke__iqx += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        oimo__deo = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(kbhm__rdzny))])
        yke__iqx += f'        ({oimo__deo},),\n'
        yke__iqx += '        new_mask,\n'
        yke__iqx += f'        {kbhm__rdzny},\n'
        yke__iqx += '    )\n'
        rhjg__sddw = {}
        exec(yke__iqx, {'bodo': bodo, 'np': np}, rhjg__sddw)
        return rhjg__sddw['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.DatetimeArrayType):
        ueye__wlzsl = arr_list.dtype.tz

        def tz_aware_concat_impl(arr_list):
            awlsx__rngn = 0
            for A in arr_list:
                awlsx__rngn += len(A)
            ojjl__zrvft = (bodo.libs.pd_datetime_arr_ext.
                alloc_pd_datetime_array(awlsx__rngn, ueye__wlzsl))
            hyf__dndh = 0
            for A in arr_list:
                for i in range(len(A)):
                    ojjl__zrvft[i + hyf__dndh] = A[i]
                hyf__dndh += len(A)
            return ojjl__zrvft
        return tz_aware_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            awlsx__rngn = 0
            for A in arr_list:
                awlsx__rngn += len(A)
            ojjl__zrvft = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(awlsx__rngn))
            hyf__dndh = 0
            for A in arr_list:
                for i in range(len(A)):
                    ojjl__zrvft._data[i + hyf__dndh] = A._data[i]
                    ropj__fjnl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ojjl__zrvft.
                        _null_bitmap, i + hyf__dndh, ropj__fjnl)
                hyf__dndh += len(A)
            return ojjl__zrvft
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            awlsx__rngn = 0
            for A in arr_list:
                awlsx__rngn += len(A)
            ojjl__zrvft = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(awlsx__rngn))
            hyf__dndh = 0
            for A in arr_list:
                for i in range(len(A)):
                    ojjl__zrvft._days_data[i + hyf__dndh] = A._days_data[i]
                    ojjl__zrvft._seconds_data[i + hyf__dndh] = A._seconds_data[
                        i]
                    ojjl__zrvft._microseconds_data[i + hyf__dndh
                        ] = A._microseconds_data[i]
                    ropj__fjnl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ojjl__zrvft.
                        _null_bitmap, i + hyf__dndh, ropj__fjnl)
                hyf__dndh += len(A)
            return ojjl__zrvft
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        njfd__kwfcg = arr_list.dtype.precision
        jxi__mfwxl = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            awlsx__rngn = 0
            for A in arr_list:
                awlsx__rngn += len(A)
            ojjl__zrvft = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                awlsx__rngn, njfd__kwfcg, jxi__mfwxl)
            hyf__dndh = 0
            for A in arr_list:
                for i in range(len(A)):
                    ojjl__zrvft._data[i + hyf__dndh] = A._data[i]
                    ropj__fjnl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ojjl__zrvft.
                        _null_bitmap, i + hyf__dndh, ropj__fjnl)
                hyf__dndh += len(A)
            return ojjl__zrvft
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        wirl__btsnu) for wirl__btsnu in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            ryi__zkfzn = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    ryi__zkfzn = arr_list.types[i]
                    break
        else:
            ryi__zkfzn = arr_list.dtype
        if ryi__zkfzn == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                iixo__pyqj = 0
                mlmom__lotb = 0
                aew__iebu = 0
                for A in arr_list:
                    data_arr = A._data
                    bnb__wag = A._indices
                    aew__iebu += len(bnb__wag)
                    iixo__pyqj += len(data_arr)
                    mlmom__lotb += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                fiey__pzxk = pre_alloc_string_array(iixo__pyqj, mlmom__lotb)
                fww__mbnve = bodo.libs.int_arr_ext.alloc_int_array(aew__iebu,
                    np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(fiey__pzxk, -1)
                bulvi__bkcqn = 0
                ehmor__gcz = 0
                zjgah__tqgts = 0
                for A in arr_list:
                    data_arr = A._data
                    bnb__wag = A._indices
                    aew__iebu = len(bnb__wag)
                    bodo.libs.str_arr_ext.set_string_array_range(fiey__pzxk,
                        data_arr, bulvi__bkcqn, ehmor__gcz)
                    for i in range(aew__iebu):
                        if bodo.libs.array_kernels.isna(bnb__wag, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            bnb__wag[i]):
                            bodo.libs.array_kernels.setna(fww__mbnve, 
                                zjgah__tqgts + i)
                        else:
                            fww__mbnve[zjgah__tqgts + i
                                ] = bulvi__bkcqn + bnb__wag[i]
                    bulvi__bkcqn += len(data_arr)
                    ehmor__gcz += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                    zjgah__tqgts += aew__iebu
                out_arr = init_dict_arr(fiey__pzxk, fww__mbnve, False, False)
                ebfhh__qlq = drop_duplicates_local_dictionary(out_arr, False)
                return ebfhh__qlq
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            iixo__pyqj = 0
            mlmom__lotb = 0
            for A in arr_list:
                arr = A
                iixo__pyqj += len(arr)
                mlmom__lotb += bodo.libs.str_arr_ext.num_total_chars(arr)
            out_arr = bodo.utils.utils.alloc_type(iixo__pyqj, ryi__zkfzn, (
                mlmom__lotb,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)
            bulvi__bkcqn = 0
            ehmor__gcz = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(out_arr, arr,
                    bulvi__bkcqn, ehmor__gcz)
                bulvi__bkcqn += len(arr)
                ehmor__gcz += bodo.libs.str_arr_ext.num_total_chars(arr)
            return out_arr
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(wirl__btsnu.dtype, types.Integer) for
        wirl__btsnu in arr_list.types) and any(isinstance(wirl__btsnu,
        IntegerArrayType) for wirl__btsnu in arr_list.types):

        def impl_int_arr_list(arr_list):
            ohew__nkxlh = convert_to_nullable_tup(arr_list)
            khfa__qghl = []
            ddtsv__jnzss = 0
            for A in ohew__nkxlh:
                khfa__qghl.append(A._data)
                ddtsv__jnzss += len(A)
            qwwr__glq = bodo.libs.array_kernels.concat(khfa__qghl)
            edd__vurrx = ddtsv__jnzss + 7 >> 3
            vfcj__krarx = np.empty(edd__vurrx, np.uint8)
            cuhox__yqsn = 0
            for A in ohew__nkxlh:
                zng__hmd = A._null_bitmap
                for hhmh__pfrg in range(len(A)):
                    ropj__fjnl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        zng__hmd, hhmh__pfrg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vfcj__krarx,
                        cuhox__yqsn, ropj__fjnl)
                    cuhox__yqsn += 1
            return bodo.libs.int_arr_ext.init_integer_array(qwwr__glq,
                vfcj__krarx)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(wirl__btsnu.dtype == types.bool_ for
        wirl__btsnu in arr_list.types) and any(wirl__btsnu == boolean_array for
        wirl__btsnu in arr_list.types):

        def impl_bool_arr_list(arr_list):
            ohew__nkxlh = convert_to_nullable_tup(arr_list)
            khfa__qghl = []
            ddtsv__jnzss = 0
            for A in ohew__nkxlh:
                khfa__qghl.append(A._data)
                ddtsv__jnzss += len(A)
            qwwr__glq = bodo.libs.array_kernels.concat(khfa__qghl)
            edd__vurrx = ddtsv__jnzss + 7 >> 3
            vfcj__krarx = np.empty(edd__vurrx, np.uint8)
            cuhox__yqsn = 0
            for A in ohew__nkxlh:
                zng__hmd = A._null_bitmap
                for hhmh__pfrg in range(len(A)):
                    ropj__fjnl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        zng__hmd, hhmh__pfrg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vfcj__krarx,
                        cuhox__yqsn, ropj__fjnl)
                    cuhox__yqsn += 1
            return bodo.libs.bool_arr_ext.init_bool_array(qwwr__glq,
                vfcj__krarx)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, FloatingArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(wirl__btsnu.dtype, types.Float) for
        wirl__btsnu in arr_list.types) and any(isinstance(wirl__btsnu,
        FloatingArrayType) for wirl__btsnu in arr_list.types):

        def impl_float_arr_list(arr_list):
            ohew__nkxlh = convert_to_nullable_tup(arr_list)
            khfa__qghl = []
            ddtsv__jnzss = 0
            for A in ohew__nkxlh:
                khfa__qghl.append(A._data)
                ddtsv__jnzss += len(A)
            qwwr__glq = bodo.libs.array_kernels.concat(khfa__qghl)
            edd__vurrx = ddtsv__jnzss + 7 >> 3
            vfcj__krarx = np.empty(edd__vurrx, np.uint8)
            cuhox__yqsn = 0
            for A in ohew__nkxlh:
                zng__hmd = A._null_bitmap
                for hhmh__pfrg in range(len(A)):
                    ropj__fjnl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        zng__hmd, hhmh__pfrg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vfcj__krarx,
                        cuhox__yqsn, ropj__fjnl)
                    cuhox__yqsn += 1
            return bodo.libs.float_arr_ext.init_float_array(qwwr__glq,
                vfcj__krarx)
        return impl_float_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            vaauu__uuu = []
            for A in arr_list:
                vaauu__uuu.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                vaauu__uuu), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        bure__nhnfi = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        yke__iqx = 'def impl(arr_list):\n'
        yke__iqx += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({bure__nhnfi}, )), arr_list[0].dtype)
"""
        qmqj__scaw = {}
        exec(yke__iqx, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, qmqj__scaw)
        return qmqj__scaw['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            ddtsv__jnzss = 0
            for A in arr_list:
                ddtsv__jnzss += len(A)
            out_arr = np.empty(ddtsv__jnzss, dtype)
            emfmf__vbtdr = 0
            for A in arr_list:
                n = len(A)
                out_arr[emfmf__vbtdr:emfmf__vbtdr + n] = A
                emfmf__vbtdr += n
            return out_arr
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(wirl__btsnu,
        (types.Array, IntegerArrayType)) and isinstance(wirl__btsnu.dtype,
        types.Integer) for wirl__btsnu in arr_list.types) and any(
        isinstance(wirl__btsnu, types.Array) and isinstance(wirl__btsnu.
        dtype, types.Float) for wirl__btsnu in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            zrcf__edjf = []
            for A in arr_list:
                zrcf__edjf.append(A._data)
            ffvm__cigjo = bodo.libs.array_kernels.concat(zrcf__edjf)
            qlyyh__ufh = bodo.libs.map_arr_ext.init_map_arr(ffvm__cigjo)
            return qlyyh__ufh
        return impl_map_arr_list
    if isinstance(arr_list, types.Tuple):
        oan__oqotw = all([(isinstance(prrkc__hgoer, bodo.DatetimeArrayType) or
            isinstance(prrkc__hgoer, types.Array) and prrkc__hgoer.dtype ==
            bodo.datetime64ns) for prrkc__hgoer in arr_list.types])
        if oan__oqotw:
            raise BodoError(
                f'Cannot concatenate the rows of Timestamp data with different timezones. Found types: {arr_list}. Please use pd.Series.tz_convert(None) to remove Timezone information.'
                )
    for prrkc__hgoer in arr_list:
        if not isinstance(prrkc__hgoer, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(wirl__btsnu.astype(np.float64) for wirl__btsnu in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    krr__byae = len(arr_tup.types)
    yke__iqx = 'def f(arr_tup):\n'
    yke__iqx += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(krr__byae
        )), ',' if krr__byae == 1 else '')
    rhjg__sddw = {}
    exec(yke__iqx, {'np': np}, rhjg__sddw)
    agwr__pjlii = rhjg__sddw['f']
    return agwr__pjlii


def convert_to_nullable_tup(arr_tup):
    pass


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, FloatingArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple
        ), 'convert_to_nullable_tup: tuple expected'
    krr__byae = len(arr_tup.types)
    jsqrw__uwe = find_common_np_dtype(arr_tup.types)
    btzyn__qrc = None
    rzr__uje = ''
    if isinstance(jsqrw__uwe, types.Integer):
        btzyn__qrc = bodo.libs.int_arr_ext.IntDtype(jsqrw__uwe)
        rzr__uje = '.astype(out_dtype, False)'
    if isinstance(jsqrw__uwe, types.Float
        ) and bodo.libs.float_arr_ext._use_nullable_float:
        btzyn__qrc = bodo.libs.float_arr_ext.FloatDtype(jsqrw__uwe)
        rzr__uje = '.astype(out_dtype, False)'
    yke__iqx = 'def f(arr_tup):\n'
    yke__iqx += '  return ({}{})\n'.format(','.join(
        f'bodo.utils.conversion.coerce_to_array(arr_tup[{i}], use_nullable_array=True){rzr__uje}'
         for i in range(krr__byae)), ',' if krr__byae == 1 else '')
    rhjg__sddw = {}
    exec(yke__iqx, {'bodo': bodo, 'out_dtype': btzyn__qrc}, rhjg__sddw)
    bsj__pgx = rhjg__sddw['f']
    return bsj__pgx


def nunique(A, dropna):
    pass


def nunique_parallel(A, dropna):
    pass


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, jilg__bvuu = build_set_seen_na(A)
        return len(s) + int(not dropna and jilg__bvuu)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        wyd__mmd = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        ann__lgqgp = len(wyd__mmd)
        return bodo.libs.distributed_api.dist_reduce(ann__lgqgp, np.int32(
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
    czkfm__pyik = get_overload_const_str(func_name)
    assert czkfm__pyik in ('cumsum', 'cumprod', 'cummin', 'cummax'
        ), 'accum_func: invalid func_name'
    if czkfm__pyik == 'cumsum':
        qrhv__ojrqu = A.dtype(0)
        oavt__fxk = np.int32(Reduce_Type.Sum.value)
        axda__oez = np.add
    if czkfm__pyik == 'cumprod':
        qrhv__ojrqu = A.dtype(1)
        oavt__fxk = np.int32(Reduce_Type.Prod.value)
        axda__oez = np.multiply
    if czkfm__pyik == 'cummin':
        if isinstance(A.dtype, types.Float):
            qrhv__ojrqu = np.finfo(A.dtype(1).dtype).max
        else:
            qrhv__ojrqu = np.iinfo(A.dtype(1).dtype).max
        oavt__fxk = np.int32(Reduce_Type.Min.value)
        axda__oez = min
    if czkfm__pyik == 'cummax':
        if isinstance(A.dtype, types.Float):
            qrhv__ojrqu = np.finfo(A.dtype(1).dtype).min
        else:
            qrhv__ojrqu = np.iinfo(A.dtype(1).dtype).min
        oavt__fxk = np.int32(Reduce_Type.Max.value)
        axda__oez = max
    vrtcf__xzo = A

    def impl(A, func_name, parallel=False):
        n = len(A)
        fepsy__wlyt = qrhv__ojrqu
        if parallel:
            for i in range(n):
                if not bodo.libs.array_kernels.isna(A, i):
                    fepsy__wlyt = axda__oez(fepsy__wlyt, A[i])
            fepsy__wlyt = bodo.libs.distributed_api.dist_exscan(fepsy__wlyt,
                oavt__fxk)
            if bodo.get_rank() == 0:
                fepsy__wlyt = qrhv__ojrqu
        out_arr = bodo.utils.utils.alloc_type(n, vrtcf__xzo, (-1,))
        for i in range(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(out_arr, i)
                continue
            fepsy__wlyt = axda__oez(fepsy__wlyt, A[i])
            out_arr[i] = fepsy__wlyt
        return out_arr
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        onppc__aay = arr_info_list_to_table([array_to_info(A)])
        jzhy__ongvk = 1
        nio__tmrq = 0
        raum__ojw = drop_duplicates_table(onppc__aay, parallel, jzhy__ongvk,
            nio__tmrq, dropna, True)
        out_arr = info_to_array(info_from_table(raum__ojw, 0), A)
        delete_table(onppc__aay)
        delete_table(raum__ojw)
        return out_arr
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    hjva__zxg = bodo.utils.typing.to_nullable_type(arr.dtype)
    ixawf__avcl = index_arr
    eak__wyrb = ixawf__avcl.dtype

    def impl(arr, index_arr):
        n = len(arr)
        jozcb__ddz = init_nested_counts(hjva__zxg)
        owdt__oqa = init_nested_counts(eak__wyrb)
        for i in range(n):
            doq__yqchq = index_arr[i]
            if isna(arr, i):
                jozcb__ddz = (jozcb__ddz[0] + 1,) + jozcb__ddz[1:]
                owdt__oqa = add_nested_counts(owdt__oqa, doq__yqchq)
                continue
            zcrye__aohv = arr[i]
            if len(zcrye__aohv) == 0:
                jozcb__ddz = (jozcb__ddz[0] + 1,) + jozcb__ddz[1:]
                owdt__oqa = add_nested_counts(owdt__oqa, doq__yqchq)
                continue
            jozcb__ddz = add_nested_counts(jozcb__ddz, zcrye__aohv)
            for wyq__qkcji in range(len(zcrye__aohv)):
                owdt__oqa = add_nested_counts(owdt__oqa, doq__yqchq)
        out_arr = bodo.utils.utils.alloc_type(jozcb__ddz[0], hjva__zxg,
            jozcb__ddz[1:])
        nfak__nvact = bodo.utils.utils.alloc_type(jozcb__ddz[0],
            ixawf__avcl, owdt__oqa)
        jjrs__omgf = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, jjrs__omgf)
                nfak__nvact[jjrs__omgf] = index_arr[i]
                jjrs__omgf += 1
                continue
            zcrye__aohv = arr[i]
            jzkkq__ocu = len(zcrye__aohv)
            if jzkkq__ocu == 0:
                setna(out_arr, jjrs__omgf)
                nfak__nvact[jjrs__omgf] = index_arr[i]
                jjrs__omgf += 1
                continue
            out_arr[jjrs__omgf:jjrs__omgf + jzkkq__ocu] = zcrye__aohv
            nfak__nvact[jjrs__omgf:jjrs__omgf + jzkkq__ocu] = index_arr[i]
            jjrs__omgf += jzkkq__ocu
        return out_arr, nfak__nvact
    return impl


def explode_no_index(arr):
    pass


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    hjva__zxg = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        jozcb__ddz = init_nested_counts(hjva__zxg)
        for i in range(n):
            if isna(arr, i):
                jozcb__ddz = (jozcb__ddz[0] + 1,) + jozcb__ddz[1:]
                ovdn__xha = 1
            else:
                zcrye__aohv = arr[i]
                qvhd__lcb = len(zcrye__aohv)
                if qvhd__lcb == 0:
                    jozcb__ddz = (jozcb__ddz[0] + 1,) + jozcb__ddz[1:]
                    ovdn__xha = 1
                    continue
                else:
                    jozcb__ddz = add_nested_counts(jozcb__ddz, zcrye__aohv)
                    ovdn__xha = qvhd__lcb
            if counts[i] != ovdn__xha:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        out_arr = bodo.utils.utils.alloc_type(jozcb__ddz[0], hjva__zxg,
            jozcb__ddz[1:])
        jjrs__omgf = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, jjrs__omgf)
                jjrs__omgf += 1
                continue
            zcrye__aohv = arr[i]
            jzkkq__ocu = len(zcrye__aohv)
            if jzkkq__ocu == 0:
                setna(out_arr, jjrs__omgf)
                jjrs__omgf += 1
                continue
            out_arr[jjrs__omgf:jjrs__omgf + jzkkq__ocu] = zcrye__aohv
            jjrs__omgf += jzkkq__ocu
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
        ataig__hsr = 'np.empty(n, np.int64)'
        pyd__hyyja = 'out_arr[i] = 1'
        wghaw__xhmp = 'max(len(arr[i]), 1)'
    else:
        ataig__hsr = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        pyd__hyyja = 'bodo.libs.array_kernels.setna(out_arr, i)'
        wghaw__xhmp = 'len(arr[i])'
    yke__iqx = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {ataig__hsr}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {pyd__hyyja}
        else:
            out_arr[i] = {wghaw__xhmp}
    return out_arr
    """
    rhjg__sddw = {}
    exec(yke__iqx, {'bodo': bodo, 'numba': numba, 'np': np}, rhjg__sddw)
    impl = rhjg__sddw['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    pass


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    ixawf__avcl = index_arr
    eak__wyrb = ixawf__avcl.dtype

    def impl(arr, pat, n, index_arr):
        sjlkj__pwvi = pat is not None and len(pat) > 1
        if sjlkj__pwvi:
            twee__tix = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        scl__uyat = len(arr)
        iixo__pyqj = 0
        mlmom__lotb = 0
        owdt__oqa = init_nested_counts(eak__wyrb)
        for i in range(scl__uyat):
            doq__yqchq = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                iixo__pyqj += 1
                owdt__oqa = add_nested_counts(owdt__oqa, doq__yqchq)
                continue
            if sjlkj__pwvi:
                ymr__bdcfk = twee__tix.split(arr[i], maxsplit=n)
            else:
                ymr__bdcfk = arr[i].split(pat, n)
            iixo__pyqj += len(ymr__bdcfk)
            for s in ymr__bdcfk:
                owdt__oqa = add_nested_counts(owdt__oqa, doq__yqchq)
                mlmom__lotb += bodo.libs.str_arr_ext.get_utf8_size(s)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(iixo__pyqj,
            mlmom__lotb)
        nfak__nvact = bodo.utils.utils.alloc_type(iixo__pyqj, ixawf__avcl,
            owdt__oqa)
        exwbj__csp = 0
        for hhmh__pfrg in range(scl__uyat):
            if isna(arr, hhmh__pfrg):
                out_arr[exwbj__csp] = ''
                bodo.libs.array_kernels.setna(out_arr, exwbj__csp)
                nfak__nvact[exwbj__csp] = index_arr[hhmh__pfrg]
                exwbj__csp += 1
                continue
            if sjlkj__pwvi:
                ymr__bdcfk = twee__tix.split(arr[hhmh__pfrg], maxsplit=n)
            else:
                ymr__bdcfk = arr[hhmh__pfrg].split(pat, n)
            zohie__pczm = len(ymr__bdcfk)
            out_arr[exwbj__csp:exwbj__csp + zohie__pczm] = ymr__bdcfk
            nfak__nvact[exwbj__csp:exwbj__csp + zohie__pczm] = index_arr[
                hhmh__pfrg]
            exwbj__csp += zohie__pczm
        return out_arr, nfak__nvact
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
            rwh__cxg = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            anb__hyb = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(anb__hyb, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(rwh__cxg, anb__hyb,
                True, True)
        return impl_dict
    tnvm__dgwwx = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        out_arr = bodo.utils.utils.alloc_type(n, tnvm__dgwwx, (0,))
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
    yeyi__tqud = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            out_arr = bodo.utils.utils.alloc_type(new_len, yeyi__tqud)
            bodo.libs.str_arr_ext.str_copy_ptr(out_arr.ctypes, 0, A.ctypes,
                old_size)
            return out_arr
        return impl_char

    def impl(A, old_size, new_len):
        out_arr = bodo.utils.utils.alloc_type(new_len, yeyi__tqud, (-1,))
        out_arr[:old_size] = A[:old_size]
        return out_arr
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    qwcb__gahnx = math.ceil((stop - start) / step)
    return int(max(qwcb__gahnx, 0))


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
    if any(isinstance(gxr__ukptv, types.Complex) for gxr__ukptv in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            wyyo__ebs = (stop - start) / step
            qwcb__gahnx = math.ceil(wyyo__ebs.real)
            duyzk__gquyq = math.ceil(wyyo__ebs.imag)
            oatus__snwam = int(max(min(duyzk__gquyq, qwcb__gahnx), 0))
            arr = np.empty(oatus__snwam, dtype)
            for i in numba.parfors.parfor.internal_prange(oatus__snwam):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            oatus__snwam = bodo.libs.array_kernels.calc_nitems(start, stop,
                step)
            arr = np.empty(oatus__snwam, dtype)
            for i in numba.parfors.parfor.internal_prange(oatus__snwam):
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
        gvs__egz = arr,
        if not inplace:
            gvs__egz = arr.copy(),
        lrm__feh = bodo.libs.str_arr_ext.to_list_if_immutable_arr(gvs__egz)
        tqvh__hdfe = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(lrm__feh, 0, n, tqvh__hdfe)
        if not ascending:
            bodo.libs.timsort.reverseRange(lrm__feh, 0, n, tqvh__hdfe)
        bodo.libs.str_arr_ext.cp_str_list_to_array(gvs__egz, lrm__feh)
        return gvs__egz[0]
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
        qlyyh__ufh = []
        for i in range(n):
            if A[i]:
                qlyyh__ufh.append(i + offset)
        return np.array(qlyyh__ufh, np.int64),
    return impl


def ffill_bfill_arr(arr):
    pass


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    yeyi__tqud = element_type(A)
    if yeyi__tqud == types.unicode_type:
        null_value = '""'
    elif yeyi__tqud == types.bool_:
        null_value = 'False'
    elif yeyi__tqud == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_datetime(0))'
            )
    elif yeyi__tqud == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_timedelta(0))'
            )
    else:
        null_value = '0'
    exwbj__csp = 'i'
    gkrz__pqpj = False
    wjsq__jiz = get_overload_const_str(method)
    if wjsq__jiz in ('ffill', 'pad'):
        qubsi__likz = 'n'
        send_right = True
    elif wjsq__jiz in ('backfill', 'bfill'):
        qubsi__likz = 'n-1, -1, -1'
        send_right = False
        if yeyi__tqud == types.unicode_type:
            exwbj__csp = '(n - 1) - i'
            gkrz__pqpj = True
    yke__iqx = 'def impl(A, method, parallel=False):\n'
    yke__iqx += '  A = decode_if_dict_array(A)\n'
    yke__iqx += '  has_last_value = False\n'
    yke__iqx += f'  last_value = {null_value}\n'
    yke__iqx += '  if parallel:\n'
    yke__iqx += '    rank = bodo.libs.distributed_api.get_rank()\n'
    yke__iqx += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    yke__iqx += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    yke__iqx += '  n = len(A)\n'
    yke__iqx += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    yke__iqx += f'  for i in range({qubsi__likz}):\n'
    yke__iqx += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    yke__iqx += f'      bodo.libs.array_kernels.setna(out_arr, {exwbj__csp})\n'
    yke__iqx += '      continue\n'
    yke__iqx += '    s = A[i]\n'
    yke__iqx += '    if bodo.libs.array_kernels.isna(A, i):\n'
    yke__iqx += '      s = last_value\n'
    yke__iqx += f'    out_arr[{exwbj__csp}] = s\n'
    yke__iqx += '    last_value = s\n'
    yke__iqx += '    has_last_value = True\n'
    if gkrz__pqpj:
        yke__iqx += '  return out_arr[::-1]\n'
    else:
        yke__iqx += '  return out_arr\n'
    fqek__eqbax = {}
    exec(yke__iqx, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, fqek__eqbax)
    impl = fqek__eqbax['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        cea__yfxu = 0
        kdzpt__iuyzn = n_pes - 1
        ezgk__yxa = np.int32(rank + 1)
        gir__kjtkr = np.int32(rank - 1)
        hmw__quub = len(in_arr) - 1
        mio__nghw = -1
        jif__oatub = -1
    else:
        cea__yfxu = n_pes - 1
        kdzpt__iuyzn = 0
        ezgk__yxa = np.int32(rank - 1)
        gir__kjtkr = np.int32(rank + 1)
        hmw__quub = 0
        mio__nghw = len(in_arr)
        jif__oatub = 1
    fqjan__rqydz = np.int32(bodo.hiframes.rolling.comm_border_tag)
    hplw__uxcy = np.empty(1, dtype=np.bool_)
    mihq__msn = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    bzm__uhck = np.empty(1, dtype=np.bool_)
    uvp__dgr = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    mpcmx__nsu = False
    lumh__nlofl = null_value
    for i in range(hmw__quub, mio__nghw, jif__oatub):
        if not isna(in_arr, i):
            mpcmx__nsu = True
            lumh__nlofl = in_arr[i]
            break
    if rank != cea__yfxu:
        eno__nzi = bodo.libs.distributed_api.irecv(hplw__uxcy, 1,
            gir__kjtkr, fqjan__rqydz, True)
        bodo.libs.distributed_api.wait(eno__nzi, True)
        pjfw__lfh = bodo.libs.distributed_api.irecv(mihq__msn, 1,
            gir__kjtkr, fqjan__rqydz, True)
        bodo.libs.distributed_api.wait(pjfw__lfh, True)
        spu__jeu = hplw__uxcy[0]
        rxu__emwhw = mihq__msn[0]
    else:
        spu__jeu = False
        rxu__emwhw = null_value
    if mpcmx__nsu:
        bzm__uhck[0] = mpcmx__nsu
        uvp__dgr[0] = lumh__nlofl
    else:
        bzm__uhck[0] = spu__jeu
        uvp__dgr[0] = rxu__emwhw
    if rank != kdzpt__iuyzn:
        snd__trzz = bodo.libs.distributed_api.isend(bzm__uhck, 1, ezgk__yxa,
            fqjan__rqydz, True)
        vfs__gcde = bodo.libs.distributed_api.isend(uvp__dgr, 1, ezgk__yxa,
            fqjan__rqydz, True)
    return spu__jeu, rxu__emwhw


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    fxr__xwlk = {'axis': axis, 'kind': kind, 'order': order}
    uene__xyg = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', fxr__xwlk, uene__xyg, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    pass


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    yeyi__tqud = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                bnb__wag = A._indices
                scl__uyat = len(bnb__wag)
                fww__mbnve = alloc_int_array(scl__uyat * repeats, np.int32)
                for i in range(scl__uyat):
                    exwbj__csp = i * repeats
                    if bodo.libs.array_kernels.isna(bnb__wag, i):
                        for hhmh__pfrg in range(repeats):
                            bodo.libs.array_kernels.setna(fww__mbnve, 
                                exwbj__csp + hhmh__pfrg)
                    else:
                        fww__mbnve[exwbj__csp:exwbj__csp + repeats] = bnb__wag[
                            i]
                return init_dict_arr(data_arr, fww__mbnve, A.
                    _has_global_dictionary, A._has_deduped_local_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            scl__uyat = len(A)
            out_arr = bodo.utils.utils.alloc_type(scl__uyat * repeats,
                yeyi__tqud, (-1,))
            for i in range(scl__uyat):
                exwbj__csp = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for hhmh__pfrg in range(repeats):
                        bodo.libs.array_kernels.setna(out_arr, exwbj__csp +
                            hhmh__pfrg)
                else:
                    out_arr[exwbj__csp:exwbj__csp + repeats] = A[i]
            return out_arr
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            bnb__wag = A._indices
            scl__uyat = len(bnb__wag)
            fww__mbnve = alloc_int_array(repeats.sum(), np.int32)
            exwbj__csp = 0
            for i in range(scl__uyat):
                kft__mddz = repeats[i]
                if kft__mddz < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(bnb__wag, i):
                    for hhmh__pfrg in range(kft__mddz):
                        bodo.libs.array_kernels.setna(fww__mbnve, 
                            exwbj__csp + hhmh__pfrg)
                else:
                    fww__mbnve[exwbj__csp:exwbj__csp + kft__mddz] = bnb__wag[i]
                exwbj__csp += kft__mddz
            return init_dict_arr(data_arr, fww__mbnve, A.
                _has_global_dictionary, A._has_deduped_local_dictionary)
        return impl_dict_arr

    def impl_arr(A, repeats):
        scl__uyat = len(A)
        out_arr = bodo.utils.utils.alloc_type(repeats.sum(), yeyi__tqud, (-1,))
        exwbj__csp = 0
        for i in range(scl__uyat):
            kft__mddz = repeats[i]
            if kft__mddz < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for hhmh__pfrg in range(kft__mddz):
                    bodo.libs.array_kernels.setna(out_arr, exwbj__csp +
                        hhmh__pfrg)
            else:
                out_arr[exwbj__csp:exwbj__csp + kft__mddz] = A[i]
            exwbj__csp += kft__mddz
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
        vyxdp__kxmwa = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(vyxdp__kxmwa, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        cudc__fdav = bodo.libs.array_kernels.concat([A1, A2])
        vpts__kbq = bodo.libs.array_kernels.unique(cudc__fdav)
        return pd.Series(vpts__kbq).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    fxr__xwlk = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    uene__xyg = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', fxr__xwlk, uene__xyg, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        epxtm__opji = bodo.libs.array_kernels.unique(A1)
        duqwv__thckl = bodo.libs.array_kernels.unique(A2)
        cudc__fdav = bodo.libs.array_kernels.concat([epxtm__opji, duqwv__thckl]
            )
        hyool__ahkmc = pd.Series(cudc__fdav).sort_values().values
        return slice_array_intersect1d(hyool__ahkmc)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    hxrtx__xchk = arr[1:] == arr[:-1]
    return arr[:-1][hxrtx__xchk]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    fqjan__rqydz = np.int32(bodo.hiframes.rolling.comm_border_tag)
    qah__ufqe = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        rlxl__yfjd = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32(
            rank - 1), fqjan__rqydz, True)
        bodo.libs.distributed_api.wait(rlxl__yfjd, True)
    if rank == n_pes - 1:
        return None
    else:
        cfv__jvzu = bodo.libs.distributed_api.irecv(qah__ufqe, 1, np.int32(
            rank + 1), fqjan__rqydz, True)
        bodo.libs.distributed_api.wait(cfv__jvzu, True)
        return qah__ufqe[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    hxrtx__xchk = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            hxrtx__xchk[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        etl__zuxtm = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == etl__zuxtm:
            hxrtx__xchk[n - 1] = True
    return hxrtx__xchk


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    fxr__xwlk = {'assume_unique': assume_unique}
    uene__xyg = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', fxr__xwlk, uene__xyg, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        epxtm__opji = bodo.libs.array_kernels.unique(A1)
        duqwv__thckl = bodo.libs.array_kernels.unique(A2)
        hxrtx__xchk = calculate_mask_setdiff1d(epxtm__opji, duqwv__thckl)
        return pd.Series(epxtm__opji[hxrtx__xchk]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    hxrtx__xchk = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        hxrtx__xchk &= A1 != A2[i]
    return hxrtx__xchk


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    fxr__xwlk = {'retstep': retstep, 'axis': axis}
    uene__xyg = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', fxr__xwlk, uene__xyg, 'numpy')
    zof__imre = False
    if is_overload_none(dtype):
        yeyi__tqud = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            zof__imre = True
        yeyi__tqud = numba.np.numpy_support.as_dtype(dtype).type
    if zof__imre:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            wufq__qwmb = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, yeyi__tqud)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = yeyi__tqud(np.floor(start + i * wufq__qwmb))
            return out_arr
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            wufq__qwmb = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, yeyi__tqud)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = yeyi__tqud(start + i * wufq__qwmb)
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
        krr__byae = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                krr__byae += A[i] == val
        return krr__byae > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    fxr__xwlk = {'axis': axis, 'out': out, 'keepdims': keepdims}
    uene__xyg = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', fxr__xwlk, uene__xyg, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        krr__byae = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                krr__byae += int(bool(A[i]))
        return krr__byae > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    fxr__xwlk = {'axis': axis, 'out': out, 'keepdims': keepdims}
    uene__xyg = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', fxr__xwlk, uene__xyg, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        krr__byae = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                krr__byae += int(bool(A[i]))
        return krr__byae == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    fxr__xwlk = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    uene__xyg = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', fxr__xwlk, uene__xyg, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        cjd__mrewe = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            out_arr = np.empty(n, cjd__mrewe)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(out_arr, i)
                    continue
                out_arr[i] = np_cbrt_scalar(A[i], cjd__mrewe)
            return out_arr
        return impl_arr
    cjd__mrewe = np.promote_types(numba.np.numpy_support.as_dtype(A), numba
        .np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, cjd__mrewe)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    smeb__zbg = x < 0
    if smeb__zbg:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if smeb__zbg:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    vrnzy__xgmrt = isinstance(tup, (types.BaseTuple, types.List))
    enhnr__rnm = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for prrkc__hgoer in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                prrkc__hgoer, 'numpy.hstack()')
            vrnzy__xgmrt = vrnzy__xgmrt and bodo.utils.utils.is_array_typ(
                prrkc__hgoer, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        vrnzy__xgmrt = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif enhnr__rnm:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        hjv__mmo = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for prrkc__hgoer in hjv__mmo.types:
            enhnr__rnm = enhnr__rnm and bodo.utils.utils.is_array_typ(
                prrkc__hgoer, False)
    if not (vrnzy__xgmrt or enhnr__rnm):
        return
    if enhnr__rnm:

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
    fxr__xwlk = {'check_valid': check_valid, 'tol': tol}
    uene__xyg = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', fxr__xwlk,
        uene__xyg, 'numpy')
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
        vznf__tyios = mean.shape[0]
        rksqa__jkq = size, vznf__tyios
        neik__pxc = np.random.standard_normal(rksqa__jkq)
        cov = cov.astype(np.float64)
        gmf__qfi, s, rma__jxhh = np.linalg.svd(cov)
        res = np.dot(neik__pxc, np.sqrt(s).reshape(vznf__tyios, 1) * rma__jxhh)
        unmtr__yuf = res + mean
        return unmtr__yuf
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
            zhsjm__inhrf = bodo.hiframes.series_kernels._get_type_max_value(arr
                )
            sex__oeji = typing.builtins.IndexValue(-1, zhsjm__inhrf)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                zzdit__nfh = typing.builtins.IndexValue(i, arr[i])
                sex__oeji = min(sex__oeji, zzdit__nfh)
            return sex__oeji.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        jnus__xkpf = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            hukig__ppgh = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            zhsjm__inhrf = jnus__xkpf(len(arr.dtype.categories) + 1)
            sex__oeji = typing.builtins.IndexValue(-1, zhsjm__inhrf)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                zzdit__nfh = typing.builtins.IndexValue(i, hukig__ppgh[i])
                sex__oeji = min(sex__oeji, zzdit__nfh)
            return sex__oeji.index
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
            zhsjm__inhrf = bodo.hiframes.series_kernels._get_type_min_value(arr
                )
            sex__oeji = typing.builtins.IndexValue(-1, zhsjm__inhrf)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                zzdit__nfh = typing.builtins.IndexValue(i, arr[i])
                sex__oeji = max(sex__oeji, zzdit__nfh)
            return sex__oeji.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        jnus__xkpf = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            hukig__ppgh = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            zhsjm__inhrf = jnus__xkpf(-1)
            sex__oeji = typing.builtins.IndexValue(-1, zhsjm__inhrf)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                zzdit__nfh = typing.builtins.IndexValue(i, hukig__ppgh[i])
                sex__oeji = max(sex__oeji, zzdit__nfh)
            return sex__oeji.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
