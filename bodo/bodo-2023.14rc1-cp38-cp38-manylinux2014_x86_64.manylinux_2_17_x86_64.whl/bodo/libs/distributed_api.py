import atexit
import datetime
import sys
import time
import warnings
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload, register_jitable
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, decode_if_dict_array, is_overload_false, is_overload_none, is_str_arr_type
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, is_array_typ, numba_to_c_type
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    bullj__gtv = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, bullj__gtv, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    bullj__gtv = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, bullj__gtv, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            bullj__gtv = get_type_enum(arr)
            return _isend(arr.ctypes, size, bullj__gtv, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        bullj__gtv = np.int32(numba_to_c_type(arr.dtype))
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            uet__nscw = size + 7 >> 3
            rxqt__swcu = _isend(arr._data.ctypes, size, bullj__gtv, pe, tag,
                cond)
            kvsh__pynt = _isend(arr._null_bitmap.ctypes, uet__nscw,
                wqg__gtnmq, pe, tag, cond)
            return rxqt__swcu, kvsh__pynt
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            jjxtq__nwzpr = arr._data
            bullj__gtv = get_type_enum(jjxtq__nwzpr)
            return _isend(jjxtq__nwzpr.ctypes, size, bullj__gtv, pe, tag, cond)
        return impl_tz_arr
    if is_str_arr_type(arr) or arr == binary_array_type:
        uomce__bhkj = np.int32(numba_to_c_type(offset_type))
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            hzfbn__tzeze = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(hzfbn__tzeze, pe, tag - 1)
            uet__nscw = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                uomce__bhkj, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), hzfbn__tzeze,
                wqg__gtnmq, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), uet__nscw,
                wqg__gtnmq, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            bullj__gtv = get_type_enum(arr)
            return _irecv(arr.ctypes, size, bullj__gtv, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        bullj__gtv = np.int32(numba_to_c_type(arr.dtype))
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            uet__nscw = size + 7 >> 3
            rxqt__swcu = _irecv(arr._data.ctypes, size, bullj__gtv, pe, tag,
                cond)
            kvsh__pynt = _irecv(arr._null_bitmap.ctypes, uet__nscw,
                wqg__gtnmq, pe, tag, cond)
            return rxqt__swcu, kvsh__pynt
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            jjxtq__nwzpr = arr._data
            bullj__gtv = get_type_enum(jjxtq__nwzpr)
            return _irecv(jjxtq__nwzpr.ctypes, size, bullj__gtv, pe, tag, cond)
        return impl_tz_arr
    if arr in [binary_array_type, string_array_type]:
        uomce__bhkj = np.int32(numba_to_c_type(offset_type))
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            hwcn__kbwde = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            hwcn__kbwde = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        cboj__fcep = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {hwcn__kbwde}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        ynw__gwwfa = dict()
        exec(cboj__fcep, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            uomce__bhkj, 'char_typ_enum': wqg__gtnmq}, ynw__gwwfa)
        impl = ynw__gwwfa['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    bullj__gtv = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), bullj__gtv)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        cnn__tskbk = n_pes if rank == root or allgather else 0
        fzfwi__kobtf = np.empty(cnn__tskbk, dtype)
        c_gather_scalar(send.ctypes, fzfwi__kobtf.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return fzfwi__kobtf
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        uoubv__qnwsc = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], uoubv__qnwsc)
        return builder.bitcast(uoubv__qnwsc, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        uoubv__qnwsc = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(uoubv__qnwsc)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    xwpa__fxm = types.unliteral(value)
    if isinstance(xwpa__fxm, IndexValueType):
        xwpa__fxm = xwpa__fxm.val_typ
        luq__dho = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            luq__dho.append(types.int64)
            luq__dho.append(bodo.datetime64ns)
            luq__dho.append(bodo.timedelta64ns)
            luq__dho.append(bodo.datetime_date_type)
            luq__dho.append(bodo.TimeType)
        if xwpa__fxm not in luq__dho:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(xwpa__fxm))
    typ_enum = np.int32(numba_to_c_type(xwpa__fxm))

    def impl(value, reduce_op):
        fucw__unw = value_to_ptr(value)
        cwstj__efnwf = value_to_ptr(value)
        _dist_reduce(fucw__unw, cwstj__efnwf, reduce_op, typ_enum)
        return load_val_ptr(cwstj__efnwf, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    xwpa__fxm = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(xwpa__fxm))
    yeltz__gbwz = xwpa__fxm(0)

    def impl(value, reduce_op):
        fucw__unw = value_to_ptr(value)
        cwstj__efnwf = value_to_ptr(yeltz__gbwz)
        _dist_exscan(fucw__unw, cwstj__efnwf, reduce_op, typ_enum)
        return load_val_ptr(cwstj__efnwf, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    pwzo__ilwsa = 0
    wvrsz__dpgcf = 0
    for i in range(len(recv_counts)):
        dllcn__jpect = recv_counts[i]
        uet__nscw = recv_counts_nulls[i]
        fiotm__pxuak = tmp_null_bytes[pwzo__ilwsa:pwzo__ilwsa + uet__nscw]
        for sae__kkkn in range(dllcn__jpect):
            set_bit_to(null_bitmap_ptr, wvrsz__dpgcf, get_bit(fiotm__pxuak,
                sae__kkkn))
            wvrsz__dpgcf += 1
        pwzo__ilwsa += uet__nscw


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            wuk__ynop = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                wuk__ynop, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            smce__nom = data.size
            recv_counts = gather_scalar(np.int32(smce__nom), allgather,
                root=root)
            eeo__hrq = recv_counts.sum()
            ilqbu__scfs = empty_like_type(eeo__hrq, data)
            oxrc__zsrs = np.empty(1, np.int32)
            if rank == root or allgather:
                oxrc__zsrs = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(smce__nom), ilqbu__scfs.ctypes,
                recv_counts.ctypes, oxrc__zsrs.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return ilqbu__scfs.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            ilqbu__scfs = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.str_arr_ext.init_str_arr(ilqbu__scfs)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            ilqbu__scfs = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.binary_arr_ext.init_binary_arr(ilqbu__scfs)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            smce__nom = len(data)
            uet__nscw = smce__nom + 7 >> 3
            recv_counts = gather_scalar(np.int32(smce__nom), allgather,
                root=root)
            eeo__hrq = recv_counts.sum()
            ilqbu__scfs = empty_like_type(eeo__hrq, data)
            oxrc__zsrs = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            cev__kdh = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                oxrc__zsrs = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                cev__kdh = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(smce__nom),
                ilqbu__scfs._days_data.ctypes, recv_counts.ctypes,
                oxrc__zsrs.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._seconds_data.ctypes, np.int32(smce__nom),
                ilqbu__scfs._seconds_data.ctypes, recv_counts.ctypes,
                oxrc__zsrs.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(smce__nom),
                ilqbu__scfs._microseconds_data.ctypes, recv_counts.ctypes,
                oxrc__zsrs.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._null_bitmap.ctypes, np.int32(uet__nscw),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, cev__kdh.
                ctypes, wqg__gtnmq, allgather, np.int32(root))
            copy_gathered_null_bytes(ilqbu__scfs._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return ilqbu__scfs
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, bodo.TimeArrayType)) or data in (boolean_array,
        datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            smce__nom = len(data)
            uet__nscw = smce__nom + 7 >> 3
            recv_counts = gather_scalar(np.int32(smce__nom), allgather,
                root=root)
            eeo__hrq = recv_counts.sum()
            ilqbu__scfs = empty_like_type(eeo__hrq, data)
            oxrc__zsrs = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            cev__kdh = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                oxrc__zsrs = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                cev__kdh = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(smce__nom), ilqbu__scfs.
                _data.ctypes, recv_counts.ctypes, oxrc__zsrs.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(uet__nscw),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, cev__kdh.
                ctypes, wqg__gtnmq, allgather, np.int32(root))
            copy_gathered_null_bytes(ilqbu__scfs._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return ilqbu__scfs
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        bzx__ulzs = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            klzek__mfvuk = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                klzek__mfvuk, bzx__ulzs)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            unmqd__vqf = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            nnoa__fqsu = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(unmqd__vqf,
                nnoa__fqsu)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            pccjj__plzbc = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            rpmhw__ebf = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rpmhw__ebf, pccjj__plzbc)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        qju__zvw = np.iinfo(np.int64).max
        xbuur__qncw = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            tzg__luewf = data._start
            oygon__fnx = data._stop
            if len(data) == 0:
                tzg__luewf = qju__zvw
                oygon__fnx = xbuur__qncw
            tzg__luewf = bodo.libs.distributed_api.dist_reduce(tzg__luewf,
                np.int32(Reduce_Type.Min.value))
            oygon__fnx = bodo.libs.distributed_api.dist_reduce(oygon__fnx,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if tzg__luewf == qju__zvw and oygon__fnx == xbuur__qncw:
                tzg__luewf = 0
                oygon__fnx = 0
            kguyx__mhbsp = max(0, -(-(oygon__fnx - tzg__luewf) // data._step))
            if kguyx__mhbsp < total_len:
                oygon__fnx = tzg__luewf + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                tzg__luewf = 0
                oygon__fnx = 0
            return bodo.hiframes.pd_index_ext.init_range_index(tzg__luewf,
                oygon__fnx, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            npr__noa = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, npr__noa)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ilqbu__scfs = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                ilqbu__scfs, data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        gnla__zcj = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table,
            'decode_if_dict_ary': bodo.hiframes.table.init_table}
        cboj__fcep = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        cboj__fcep += '  T = data\n'
        cboj__fcep += '  T2 = init_table(T, True)\n'
        gvut__vuesy = bodo.hiframes.table.get_init_table_output_type(data, True
            )
        jzb__frnk = (bodo.string_array_type in data.type_to_blk and bodo.
            dict_str_arr_type in data.type_to_blk)
        if jzb__frnk:
            cboj__fcep += (bodo.hiframes.table.
                gen_str_and_dict_enc_cols_to_one_block_fn_txt(data,
                gvut__vuesy, gnla__zcj, True))
        for loa__tyi, kzxbq__rwq in data.type_to_blk.items():
            if jzb__frnk and loa__tyi in (bodo.string_array_type, bodo.
                dict_str_arr_type):
                continue
            elif loa__tyi == bodo.dict_str_arr_type:
                assert bodo.string_array_type in gvut__vuesy.type_to_blk, 'Error in gatherv: If encoded string type is present in the input, then non-encoded string type should be present in the output'
                fgl__rpwke = gvut__vuesy.type_to_blk[bodo.string_array_type]
            else:
                assert loa__tyi in gvut__vuesy.type_to_blk, 'Error in gatherv: All non-encoded string types present in the input should be present in the output'
                fgl__rpwke = gvut__vuesy.type_to_blk[loa__tyi]
            gnla__zcj[f'arr_inds_{kzxbq__rwq}'] = np.array(data.
                block_to_arr_ind[kzxbq__rwq], dtype=np.int64)
            cboj__fcep += (
                f'  arr_list_{kzxbq__rwq} = get_table_block(T, {kzxbq__rwq})\n'
                )
            cboj__fcep += f"""  out_arr_list_{kzxbq__rwq} = alloc_list_like(arr_list_{kzxbq__rwq}, len(arr_list_{kzxbq__rwq}), True)
"""
            cboj__fcep += f'  for i in range(len(arr_list_{kzxbq__rwq})):\n'
            cboj__fcep += (
                f'    arr_ind_{kzxbq__rwq} = arr_inds_{kzxbq__rwq}[i]\n')
            cboj__fcep += f"""    ensure_column_unboxed(T, arr_list_{kzxbq__rwq}, i, arr_ind_{kzxbq__rwq})
"""
            cboj__fcep += f"""    out_arr_{kzxbq__rwq} = bodo.gatherv(arr_list_{kzxbq__rwq}[i], allgather, warn_if_rep, root)
"""
            cboj__fcep += (
                f'    out_arr_list_{kzxbq__rwq}[i] = out_arr_{kzxbq__rwq}\n')
            cboj__fcep += (
                f'  T2 = set_table_block(T2, out_arr_list_{kzxbq__rwq}, {fgl__rpwke})\n'
                )
        cboj__fcep += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        cboj__fcep += f'  T2 = set_table_len(T2, length)\n'
        cboj__fcep += f'  return T2\n'
        ynw__gwwfa = {}
        exec(cboj__fcep, gnla__zcj, ynw__gwwfa)
        wsvq__nxl = ynw__gwwfa['impl_table']
        return wsvq__nxl
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        qen__sio = len(data.columns)
        if qen__sio == 0:
            zzs__akm = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                lrqzt__tdxqi = bodo.gatherv(index, allgather, warn_if_rep, root
                    )
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    lrqzt__tdxqi, zzs__akm)
            return impl
        kkafb__tcjh = ', '.join(f'g_data_{i}' for i in range(qen__sio))
        cboj__fcep = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            ksoa__mrj = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            kkafb__tcjh = 'T2'
            cboj__fcep += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            cboj__fcep += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(qen__sio):
                cboj__fcep += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                cboj__fcep += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        cboj__fcep += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        cboj__fcep += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        cboj__fcep += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(kkafb__tcjh))
        ynw__gwwfa = {}
        gnla__zcj = {'bodo': bodo,
            '__col_name_meta_value_gatherv_with_cols': ColNamesMetaType(
            data.columns)}
        exec(cboj__fcep, gnla__zcj, ynw__gwwfa)
        ztb__qszix = ynw__gwwfa['impl_df']
        return ztb__qszix
    if isinstance(data, ArrayItemArrayType):
        dxpr__hdgv = np.int32(numba_to_c_type(types.int32))
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            bkzoi__sdyq = bodo.libs.array_item_arr_ext.get_offsets(data)
            jjxtq__nwzpr = bodo.libs.array_item_arr_ext.get_data(data)
            jjxtq__nwzpr = jjxtq__nwzpr[:bkzoi__sdyq[-1]]
            kic__xqi = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            smce__nom = len(data)
            gae__hvvxn = np.empty(smce__nom, np.uint32)
            uet__nscw = smce__nom + 7 >> 3
            for i in range(smce__nom):
                gae__hvvxn[i] = bkzoi__sdyq[i + 1] - bkzoi__sdyq[i]
            recv_counts = gather_scalar(np.int32(smce__nom), allgather,
                root=root)
            eeo__hrq = recv_counts.sum()
            oxrc__zsrs = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            cev__kdh = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                oxrc__zsrs = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for xuwno__kmdmc in range(len(recv_counts)):
                    recv_counts_nulls[xuwno__kmdmc] = recv_counts[xuwno__kmdmc
                        ] + 7 >> 3
                cev__kdh = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            muw__yurjv = np.empty(eeo__hrq + 1, np.uint32)
            zkyiu__wdi = bodo.gatherv(jjxtq__nwzpr, allgather, warn_if_rep,
                root)
            dzr__uqz = np.empty(eeo__hrq + 7 >> 3, np.uint8)
            c_gatherv(gae__hvvxn.ctypes, np.int32(smce__nom), muw__yurjv.
                ctypes, recv_counts.ctypes, oxrc__zsrs.ctypes, dxpr__hdgv,
                allgather, np.int32(root))
            c_gatherv(kic__xqi.ctypes, np.int32(uet__nscw), tmp_null_bytes.
                ctypes, recv_counts_nulls.ctypes, cev__kdh.ctypes,
                wqg__gtnmq, allgather, np.int32(root))
            dummy_use(data)
            kynmi__fpjcr = np.empty(eeo__hrq + 1, np.uint64)
            convert_len_arr_to_offset(muw__yurjv.ctypes, kynmi__fpjcr.
                ctypes, eeo__hrq)
            copy_gathered_null_bytes(dzr__uqz.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                eeo__hrq, zkyiu__wdi, kynmi__fpjcr, dzr__uqz)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        cprms__gpki = data.names
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ftns__mgvt = bodo.libs.struct_arr_ext.get_data(data)
            wcr__mxc = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            kkay__ren = bodo.gatherv(ftns__mgvt, allgather=allgather, root=root
                )
            rank = bodo.libs.distributed_api.get_rank()
            smce__nom = len(data)
            uet__nscw = smce__nom + 7 >> 3
            recv_counts = gather_scalar(np.int32(smce__nom), allgather,
                root=root)
            eeo__hrq = recv_counts.sum()
            pnyar__qwc = np.empty(eeo__hrq + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            cev__kdh = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                cev__kdh = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(wcr__mxc.ctypes, np.int32(uet__nscw), tmp_null_bytes.
                ctypes, recv_counts_nulls.ctypes, cev__kdh.ctypes,
                wqg__gtnmq, allgather, np.int32(root))
            copy_gathered_null_bytes(pnyar__qwc.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(kkay__ren,
                pnyar__qwc, cprms__gpki)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            ilqbu__scfs = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.binary_arr_ext.init_binary_arr(ilqbu__scfs)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ilqbu__scfs = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.tuple_arr_ext.init_tuple_arr(ilqbu__scfs)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            ilqbu__scfs = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.map_arr_ext.init_map_arr(ilqbu__scfs)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ilqbu__scfs = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            cuc__ias = bodo.gatherv(data.indices, allgather, warn_if_rep, root)
            rdwg__ecw = bodo.gatherv(data.indptr, allgather, warn_if_rep, root)
            kwmah__vrl = gather_scalar(data.shape[0], allgather, root=root)
            bddp__agj = kwmah__vrl.sum()
            qen__sio = bodo.libs.distributed_api.dist_reduce(data.shape[1],
                np.int32(Reduce_Type.Max.value))
            rvou__aftmb = np.empty(bddp__agj + 1, np.int64)
            cuc__ias = cuc__ias.astype(np.int64)
            rvou__aftmb[0] = 0
            ynwl__uisdd = 1
            iwu__lpzw = 0
            for hqr__cdf in kwmah__vrl:
                for yaz__cjndw in range(hqr__cdf):
                    qfen__acmm = rdwg__ecw[iwu__lpzw + 1] - rdwg__ecw[iwu__lpzw
                        ]
                    rvou__aftmb[ynwl__uisdd] = rvou__aftmb[ynwl__uisdd - 1
                        ] + qfen__acmm
                    ynwl__uisdd += 1
                    iwu__lpzw += 1
                iwu__lpzw += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(ilqbu__scfs,
                cuc__ias, rvou__aftmb, (bddp__agj, qen__sio))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        cboj__fcep = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        cboj__fcep += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        ynw__gwwfa = {}
        exec(cboj__fcep, {'bodo': bodo}, ynw__gwwfa)
        womp__milbb = ynw__gwwfa['impl_tuple']
        return womp__milbb
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as vqzuo__ntoj:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        cboj__fcep = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        fhqvn__uiu = ', '.join([f"'{pccjj__plzbc}'" for pccjj__plzbc in
            data.names])
        nwg__owu = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        cboj__fcep += f"""  return bodosql.context_ext.init_sql_context(({fhqvn__uiu}, ), ({nwg__owu}, ), data.catalog)
"""
        ynw__gwwfa = {}
        exec(cboj__fcep, {'bodo': bodo, 'bodosql': bodosql}, ynw__gwwfa)
        mkq__ribee = ynw__gwwfa['impl_bodosql_context']
        return mkq__ribee
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as vqzuo__ntoj:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        cboj__fcep = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        cboj__fcep += f'  return data\n'
        ynw__gwwfa = {}
        exec(cboj__fcep, {}, ynw__gwwfa)
        jfd__cpdpz = ynw__gwwfa['impl_table_path']
        return jfd__cpdpz
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    cboj__fcep = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    cboj__fcep += '    if random:\n'
    cboj__fcep += '        if random_seed is None:\n'
    cboj__fcep += '            random = 1\n'
    cboj__fcep += '        else:\n'
    cboj__fcep += '            random = 2\n'
    cboj__fcep += '    if random_seed is None:\n'
    cboj__fcep += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        exnyj__tis = data
        qen__sio = len(exnyj__tis.columns)
        for i in range(qen__sio):
            cboj__fcep += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        cboj__fcep += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        kkafb__tcjh = ', '.join(f'data_{i}' for i in range(qen__sio))
        cboj__fcep += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(ulkun__nqlp) for
            ulkun__nqlp in range(qen__sio))))
        cboj__fcep += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        cboj__fcep += '    if dests is None:\n'
        cboj__fcep += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        cboj__fcep += '    else:\n'
        cboj__fcep += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for pbqnl__fgnv in range(qen__sio):
            cboj__fcep += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(pbqnl__fgnv))
        cboj__fcep += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(qen__sio))
        cboj__fcep += '    delete_table(out_table)\n'
        cboj__fcep += '    if parallel:\n'
        cboj__fcep += '        delete_table(table_total)\n'
        kkafb__tcjh = ', '.join('out_arr_{}'.format(i) for i in range(qen__sio)
            )
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        cboj__fcep += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(kkafb__tcjh, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        cboj__fcep += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        cboj__fcep += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        cboj__fcep += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        cboj__fcep += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        cboj__fcep += '    if dests is None:\n'
        cboj__fcep += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        cboj__fcep += '    else:\n'
        cboj__fcep += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        cboj__fcep += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        cboj__fcep += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        cboj__fcep += '    delete_table(out_table)\n'
        cboj__fcep += '    if parallel:\n'
        cboj__fcep += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        cboj__fcep += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        cboj__fcep += '    if not parallel:\n'
        cboj__fcep += '        return data\n'
        cboj__fcep += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        cboj__fcep += '    if dests is None:\n'
        cboj__fcep += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        cboj__fcep += '    elif bodo.get_rank() not in dests:\n'
        cboj__fcep += '        dim0_local_size = 0\n'
        cboj__fcep += '    else:\n'
        cboj__fcep += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        cboj__fcep += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        cboj__fcep += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        cboj__fcep += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        cboj__fcep += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        cboj__fcep += '    if dests is None:\n'
        cboj__fcep += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        cboj__fcep += '    else:\n'
        cboj__fcep += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        cboj__fcep += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        cboj__fcep += '    delete_table(out_table)\n'
        cboj__fcep += '    if parallel:\n'
        cboj__fcep += '        delete_table(table_total)\n'
        cboj__fcep += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    ynw__gwwfa = {}
    gnla__zcj = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.array.
        array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        gnla__zcj.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(exnyj__tis.columns)})
    exec(cboj__fcep, gnla__zcj, ynw__gwwfa)
    impl = ynw__gwwfa['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    cboj__fcep = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        cboj__fcep += '    if seed is None:\n'
        cboj__fcep += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        cboj__fcep += '    np.random.seed(seed)\n'
        cboj__fcep += '    if not parallel:\n'
        cboj__fcep += '        data = data.copy()\n'
        cboj__fcep += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            cboj__fcep += '        data = data[:n_samples]\n'
        cboj__fcep += '        return data\n'
        cboj__fcep += '    else:\n'
        cboj__fcep += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        cboj__fcep += '        permutation = np.arange(dim0_global_size)\n'
        cboj__fcep += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            cboj__fcep += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            cboj__fcep += '        n_samples = dim0_global_size\n'
        cboj__fcep += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        cboj__fcep += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        cboj__fcep += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        cboj__fcep += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        cboj__fcep += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        cboj__fcep += '        return output\n'
    else:
        cboj__fcep += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            cboj__fcep += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            cboj__fcep += '    output = output[:local_n_samples]\n'
        cboj__fcep += '    return output\n'
    ynw__gwwfa = {}
    exec(cboj__fcep, {'np': np, 'bodo': bodo}, ynw__gwwfa)
    impl = ynw__gwwfa['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    obotb__zdio = np.empty(sendcounts_nulls.sum(), np.uint8)
    pwzo__ilwsa = 0
    wvrsz__dpgcf = 0
    for lccll__hibh in range(len(sendcounts)):
        dllcn__jpect = sendcounts[lccll__hibh]
        uet__nscw = sendcounts_nulls[lccll__hibh]
        fiotm__pxuak = obotb__zdio[pwzo__ilwsa:pwzo__ilwsa + uet__nscw]
        for sae__kkkn in range(dllcn__jpect):
            set_bit_to_arr(fiotm__pxuak, sae__kkkn, get_bit_bitmap(
                null_bitmap_ptr, wvrsz__dpgcf))
            wvrsz__dpgcf += 1
        pwzo__ilwsa += uet__nscw
    return obotb__zdio


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    lqclq__tvgta = MPI.COMM_WORLD
    data = lqclq__tvgta.bcast(data, root)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    dvhky__ufhk = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    ugt__vmmm = (0,) * dvhky__ufhk

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        wfgy__vctey = np.ascontiguousarray(data)
        hmv__jheep = data.ctypes
        pgh__yim = ugt__vmmm
        if rank == MPI_ROOT:
            pgh__yim = wfgy__vctey.shape
        pgh__yim = bcast_tuple(pgh__yim)
        vqk__kqwe = get_tuple_prod(pgh__yim[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes, pgh__yim[0]
            )
        send_counts *= vqk__kqwe
        smce__nom = send_counts[rank]
        uqty__wymx = np.empty(smce__nom, dtype)
        oxrc__zsrs = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(hmv__jheep, send_counts.ctypes, oxrc__zsrs.ctypes,
            uqty__wymx.ctypes, np.int32(smce__nom), np.int32(typ_val))
        return uqty__wymx.reshape((-1,) + pgh__yim[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == bodo.dict_str_arr_type:
        import pyarrow as pa
        return pa.array(['a'], type=pa.dictionary(pa.int32(), pa.string()))
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        aeknz__yvc = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], aeknz__yvc)
    if isinstance(dtype, FloatingArrayType):
        aeknz__yvc = 'Float{}'.format(dtype.dtype.bitwidth)
        return pd.array([3.0], aeknz__yvc)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        pccjj__plzbc = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=pccjj__plzbc)
        goss__ncjz = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(goss__ncjz)
        return pd.Index(arr, name=pccjj__plzbc)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        pccjj__plzbc = _get_name_value_for_type(dtype.name_typ)
        cprms__gpki = tuple(_get_name_value_for_type(t) for t in dtype.
            names_typ)
        vxh__dknyy = tuple(get_value_for_type(t) for t in dtype.array_types)
        vxh__dknyy = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in vxh__dknyy)
        val = pd.MultiIndex.from_arrays(vxh__dknyy, names=cprms__gpki)
        val.name = pccjj__plzbc
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        pccjj__plzbc = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=pccjj__plzbc)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        vxh__dknyy = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({pccjj__plzbc: arr for pccjj__plzbc, arr in zip
            (dtype.columns, vxh__dknyy)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        goss__ncjz = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(goss__ncjz[0],
            goss__ncjz[0])])
    raise BodoError(f'get_value_for_type(dtype): Missing data type {dtype}')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        warnings.warn(BodoWarning(
            "bodo.scatterv(): A non-None value for 'data' was found on a rank other than the root. This data won't be sent to any other ranks and will be overwritten with data from rank 0."
            ))
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.scatterv()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.scatterv()')
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if data in (string_array_type, binary_array_type):
        dxpr__hdgv = np.int32(numba_to_c_type(types.int32))
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            hwcn__kbwde = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            hwcn__kbwde = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        cboj__fcep = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {hwcn__kbwde}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        ynw__gwwfa = dict()
        exec(cboj__fcep, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            dxpr__hdgv, 'char_typ_enum': wqg__gtnmq, 'decode_if_dict_array':
            decode_if_dict_array}, ynw__gwwfa)
        impl = ynw__gwwfa['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        dxpr__hdgv = np.int32(numba_to_c_type(types.int32))
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            paq__dayzz = bodo.libs.array_item_arr_ext.get_offsets(data)
            pmgb__irv = bodo.libs.array_item_arr_ext.get_data(data)
            pmgb__irv = pmgb__irv[:paq__dayzz[-1]]
            ekl__fskjk = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            aytcd__mvtl = bcast_scalar(len(data))
            xiunn__xeq = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                xiunn__xeq[i] = paq__dayzz[i + 1] - paq__dayzz[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                aytcd__mvtl)
            oxrc__zsrs = bodo.ir.join.calc_disp(send_counts)
            xbuu__jntnk = np.empty(n_pes, np.int32)
            if rank == 0:
                bhfw__apmg = 0
                for i in range(n_pes):
                    adlx__mhfwj = 0
                    for yaz__cjndw in range(send_counts[i]):
                        adlx__mhfwj += xiunn__xeq[bhfw__apmg]
                        bhfw__apmg += 1
                    xbuu__jntnk[i] = adlx__mhfwj
            bcast(xbuu__jntnk)
            dur__sdtl = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                dur__sdtl[i] = send_counts[i] + 7 >> 3
            cev__kdh = bodo.ir.join.calc_disp(dur__sdtl)
            smce__nom = send_counts[rank]
            bqup__hqiz = np.empty(smce__nom + 1, np_offset_type)
            hiy__ptq = bodo.libs.distributed_api.scatterv_impl(pmgb__irv,
                xbuu__jntnk)
            wqze__hghyz = smce__nom + 7 >> 3
            pymr__coqi = np.empty(wqze__hghyz, np.uint8)
            hgen__zji = np.empty(smce__nom, np.uint32)
            c_scatterv(xiunn__xeq.ctypes, send_counts.ctypes, oxrc__zsrs.
                ctypes, hgen__zji.ctypes, np.int32(smce__nom), dxpr__hdgv)
            convert_len_arr_to_offset(hgen__zji.ctypes, bqup__hqiz.ctypes,
                smce__nom)
            sojj__xdz = get_scatter_null_bytes_buff(ekl__fskjk.ctypes,
                send_counts, dur__sdtl)
            c_scatterv(sojj__xdz.ctypes, dur__sdtl.ctypes, cev__kdh.ctypes,
                pymr__coqi.ctypes, np.int32(wqze__hghyz), wqg__gtnmq)
            return bodo.libs.array_item_arr_ext.init_array_item_array(smce__nom
                , hiy__ptq, bqup__hqiz, pymr__coqi)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or data in (boolean_array, datetime_date_array_type):
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            cgcj__ctou = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, FloatingArrayType):
            cgcj__ctou = bodo.libs.float_arr_ext.init_float_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            cgcj__ctou = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            cgcj__ctou = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            cgcj__ctou = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            wfgy__vctey = data._data
            wcr__mxc = data._null_bitmap
            zqm__dohcg = len(wfgy__vctey)
            xsvpm__yfc = _scatterv_np(wfgy__vctey, send_counts)
            aytcd__mvtl = bcast_scalar(zqm__dohcg)
            gpvht__dboo = len(xsvpm__yfc) + 7 >> 3
            ytixg__dvtfh = np.empty(gpvht__dboo, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                aytcd__mvtl)
            dur__sdtl = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                dur__sdtl[i] = send_counts[i] + 7 >> 3
            cev__kdh = bodo.ir.join.calc_disp(dur__sdtl)
            sojj__xdz = get_scatter_null_bytes_buff(wcr__mxc.ctypes,
                send_counts, dur__sdtl)
            c_scatterv(sojj__xdz.ctypes, dur__sdtl.ctypes, cev__kdh.ctypes,
                ytixg__dvtfh.ctypes, np.int32(gpvht__dboo), wqg__gtnmq)
            return cgcj__ctou(xsvpm__yfc, ytixg__dvtfh)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            bisb__ugv = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            dyk__bata = bodo.libs.distributed_api.scatterv_impl(data._right,
                send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(bisb__ugv,
                dyk__bata)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            tzg__luewf = data._start
            oygon__fnx = data._stop
            cuws__ffjah = data._step
            pccjj__plzbc = data._name
            pccjj__plzbc = bcast_scalar(pccjj__plzbc)
            tzg__luewf = bcast_scalar(tzg__luewf)
            oygon__fnx = bcast_scalar(oygon__fnx)
            cuws__ffjah = bcast_scalar(cuws__ffjah)
            euhcz__oes = bodo.libs.array_kernels.calc_nitems(tzg__luewf,
                oygon__fnx, cuws__ffjah)
            chunk_start = bodo.libs.distributed_api.get_start(euhcz__oes,
                n_pes, rank)
            dvupg__qzeq = bodo.libs.distributed_api.get_node_portion(euhcz__oes
                , n_pes, rank)
            drlhd__zpymn = tzg__luewf + cuws__ffjah * chunk_start
            uprg__qhk = tzg__luewf + cuws__ffjah * (chunk_start + dvupg__qzeq)
            uprg__qhk = min(uprg__qhk, oygon__fnx)
            return bodo.hiframes.pd_index_ext.init_range_index(drlhd__zpymn,
                uprg__qhk, cuws__ffjah, pccjj__plzbc)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        npr__noa = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            wfgy__vctey = data._data
            pccjj__plzbc = data._name
            pccjj__plzbc = bcast_scalar(pccjj__plzbc)
            arr = bodo.libs.distributed_api.scatterv_impl(wfgy__vctey,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                pccjj__plzbc, npr__noa)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            wfgy__vctey = data._data
            pccjj__plzbc = data._name
            pccjj__plzbc = bcast_scalar(pccjj__plzbc)
            arr = bodo.libs.distributed_api.scatterv_impl(wfgy__vctey,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, pccjj__plzbc)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            ilqbu__scfs = bodo.libs.distributed_api.scatterv_impl(data.
                _data, send_counts)
            pccjj__plzbc = bcast_scalar(data._name)
            cprms__gpki = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                ilqbu__scfs, cprms__gpki, pccjj__plzbc)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            pccjj__plzbc = bodo.hiframes.pd_series_ext.get_series_name(data)
            ndc__mlewb = bcast_scalar(pccjj__plzbc)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            rpmhw__ebf = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rpmhw__ebf, ndc__mlewb)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        qen__sio = len(data.columns)
        cxq__gim = ColNamesMetaType(data.columns)
        cboj__fcep = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        if data.is_table_format:
            cboj__fcep += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            cboj__fcep += """  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)
"""
            kkafb__tcjh = 'g_table'
        else:
            for i in range(qen__sio):
                cboj__fcep += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                cboj__fcep += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            kkafb__tcjh = ', '.join(f'g_data_{i}' for i in range(qen__sio))
        cboj__fcep += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        cboj__fcep += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        cboj__fcep += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({kkafb__tcjh},), g_index, __col_name_meta_scaterv_impl)
"""
        ynw__gwwfa = {}
        exec(cboj__fcep, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            cxq__gim}, ynw__gwwfa)
        ztb__qszix = ynw__gwwfa['impl_df']
        return ztb__qszix
    if isinstance(data, bodo.TableType):
        cboj__fcep = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        cboj__fcep += '  T = data\n'
        cboj__fcep += '  T2 = init_table(T, False)\n'
        cboj__fcep += '  l = 0\n'
        gnla__zcj = {}
        for nej__khdxa in data.type_to_blk.values():
            gnla__zcj[f'arr_inds_{nej__khdxa}'] = np.array(data.
                block_to_arr_ind[nej__khdxa], dtype=np.int64)
            cboj__fcep += (
                f'  arr_list_{nej__khdxa} = get_table_block(T, {nej__khdxa})\n'
                )
            cboj__fcep += f"""  out_arr_list_{nej__khdxa} = alloc_list_like(arr_list_{nej__khdxa}, len(arr_list_{nej__khdxa}), False)
"""
            cboj__fcep += f'  for i in range(len(arr_list_{nej__khdxa})):\n'
            cboj__fcep += (
                f'    arr_ind_{nej__khdxa} = arr_inds_{nej__khdxa}[i]\n')
            cboj__fcep += f"""    ensure_column_unboxed(T, arr_list_{nej__khdxa}, i, arr_ind_{nej__khdxa})
"""
            cboj__fcep += f"""    out_arr_{nej__khdxa} = bodo.libs.distributed_api.scatterv_impl(arr_list_{nej__khdxa}[i], send_counts)
"""
            cboj__fcep += (
                f'    out_arr_list_{nej__khdxa}[i] = out_arr_{nej__khdxa}\n')
            cboj__fcep += f'    l = len(out_arr_{nej__khdxa})\n'
            cboj__fcep += (
                f'  T2 = set_table_block(T2, out_arr_list_{nej__khdxa}, {nej__khdxa})\n'
                )
        cboj__fcep += f'  T2 = set_table_len(T2, l)\n'
        cboj__fcep += f'  return T2\n'
        gnla__zcj.update({'bodo': bodo, 'init_table': bodo.hiframes.table.
            init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        ynw__gwwfa = {}
        exec(cboj__fcep, gnla__zcj, ynw__gwwfa)
        return ynw__gwwfa['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                faua__cri = data._data
                bodo.libs.distributed_api.bcast_scalar(len(faua__cri))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(faua__cri)))
            else:
                kguyx__mhbsp = bodo.libs.distributed_api.bcast_scalar(0)
                hzfbn__tzeze = bodo.libs.distributed_api.bcast_scalar(0)
                faua__cri = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    kguyx__mhbsp, hzfbn__tzeze)
            bodo.libs.distributed_api.bcast(faua__cri)
            fav__sbh = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(faua__cri, fav__sbh,
                True, data._has_deduped_local_dictionary)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            wuk__ynop = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                wuk__ynop, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        cboj__fcep = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        cboj__fcep += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        ynw__gwwfa = {}
        exec(cboj__fcep, {'bodo': bodo}, ynw__gwwfa)
        womp__milbb = ynw__gwwfa['impl_tuple']
        return womp__milbb
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data, root=MPI_ROOT):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data, root=MPI_ROOT):
    if isinstance(data, types.Array):

        def bcast_impl(data, root=MPI_ROOT):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0, np.int32(root))
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data, root=MPI_ROOT):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0, np.int32(root))
            bcast(data._null_bitmap, root)
            return
        return bcast_decimal_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType)) or data in (
        boolean_array, datetime_date_array_type):

        def bcast_impl_int_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            bcast(data._null_bitmap, root)
            return
        return bcast_impl_int_arr
    if isinstance(data, DatetimeArrayType):

        def bcast_impl_tz_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            return
        return bcast_impl_tz_arr
    if is_str_arr_type(data) or data == binary_array_type:
        uomce__bhkj = np.int32(numba_to_c_type(offset_type))
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            smce__nom = len(data)
            yxbs__vklm = num_total_chars(data)
            assert smce__nom < INT_MAX
            assert yxbs__vklm < INT_MAX
            nzbr__pcs = get_offset_ptr(data)
            hmv__jheep = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            uet__nscw = smce__nom + 7 >> 3
            c_bcast(nzbr__pcs, np.int32(smce__nom + 1), uomce__bhkj, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(hmv__jheep, np.int32(yxbs__vklm), wqg__gtnmq, np.array(
                [-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(uet__nscw), wqg__gtnmq, np.
                array([-1]).ctypes, 0, np.int32(root))
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def bcast_scalar(val, root=MPI_ROOT):
    val = types.unliteral(val)
    if not (isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]):
        raise BodoError(
            f'bcast_scalar requires an argument of type Integer, Float, datetime64ns, timedelta64ns, string, None, or Bool. Found type {val}'
            )
    if val == types.none:
        return lambda val, root=MPI_ROOT: None
    if val == bodo.string_type:
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                clrph__bbgql = 0
                cxn__zmfog = np.empty(0, np.uint8).ctypes
            else:
                cxn__zmfog, clrph__bbgql = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            clrph__bbgql = bodo.libs.distributed_api.bcast_scalar(clrph__bbgql,
                root)
            if rank != root:
                zlfni__zkrl = np.empty(clrph__bbgql + 1, np.uint8)
                zlfni__zkrl[clrph__bbgql] = 0
                cxn__zmfog = zlfni__zkrl.ctypes
            c_bcast(cxn__zmfog, np.int32(clrph__bbgql), wqg__gtnmq, np.
                array([-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(cxn__zmfog, clrph__bbgql)
        return impl_str
    typ_val = numba_to_c_type(val)
    cboj__fcep = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    ynw__gwwfa = {}
    exec(cboj__fcep, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, ynw__gwwfa)
    ozlmb__npabt = ynw__gwwfa['bcast_scalar_impl']
    return ozlmb__npabt


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple
        ), 'Internal Error: Argument to bcast tuple must be of type tuple'
    mrpbd__cwdq = len(val)
    cboj__fcep = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    cboj__fcep += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(mrpbd__cwdq)
        ), ',' if mrpbd__cwdq else '')
    ynw__gwwfa = {}
    exec(cboj__fcep, {'bcast_scalar': bcast_scalar}, ynw__gwwfa)
    ikzp__skp = ynw__gwwfa['bcast_tuple_impl']
    return ikzp__skp


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            smce__nom = bcast_scalar(len(arr), root)
            tmmev__ntd = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(smce__nom, tmmev__ntd)
            return arr
        return prealloc_impl
    return lambda arr, root=MPI_ROOT: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):
    if not idx.has_step:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            drlhd__zpymn = max(arr_start, slice_index.start) - arr_start
            uprg__qhk = max(slice_index.stop - arr_start, 0)
            return slice(drlhd__zpymn, uprg__qhk)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            tzg__luewf = slice_index.start
            cuws__ffjah = slice_index.step
            quwr__yefc = (0 if cuws__ffjah == 1 or tzg__luewf > arr_start else
                abs(cuws__ffjah - arr_start % cuws__ffjah) % cuws__ffjah)
            drlhd__zpymn = max(arr_start, slice_index.start
                ) - arr_start + quwr__yefc
            uprg__qhk = max(slice_index.stop - arr_start, 0)
            return slice(drlhd__zpymn, uprg__qhk, cuws__ffjah)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        vszx__fupjr = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[vszx__fupjr])
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if is_str_arr_type(arr) or arr == bodo.binary_array_type:
        vshpg__ulyhz = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        wqg__gtnmq = np.int32(numba_to_c_type(types.uint8))
        uzo__afejw = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            khvrk__llzhm = np.int32(10)
            tag = np.int32(11)
            cit__phl = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                jjxtq__nwzpr = arr._data
                eerx__jpgi = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    jjxtq__nwzpr, ind)
                dslh__jrwv = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    jjxtq__nwzpr, ind + 1)
                length = dslh__jrwv - eerx__jpgi
                uoubv__qnwsc = jjxtq__nwzpr[ind]
                cit__phl[0] = length
                isend(cit__phl, np.int32(1), root, khvrk__llzhm, True)
                isend(uoubv__qnwsc, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(uzo__afejw
                , vshpg__ulyhz, 0, 1)
            kguyx__mhbsp = 0
            if rank == root:
                kguyx__mhbsp = recv(np.int64, ANY_SOURCE, khvrk__llzhm)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    uzo__afejw, vshpg__ulyhz, kguyx__mhbsp, 1)
                hmv__jheep = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(hmv__jheep, np.int32(kguyx__mhbsp), wqg__gtnmq,
                    ANY_SOURCE, tag)
            dummy_use(cit__phl)
            kguyx__mhbsp = bcast_scalar(kguyx__mhbsp)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    uzo__afejw, vshpg__ulyhz, kguyx__mhbsp, 1)
            hmv__jheep = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(hmv__jheep, np.int32(kguyx__mhbsp), wqg__gtnmq, np.
                array([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, kguyx__mhbsp)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        wirtx__vnji = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, wirtx__vnji)
            if arr_start <= ind < arr_start + len(arr):
                wuk__ynop = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = wuk__ynop[ind - arr_start]
                send_arr = np.full(1, data, wirtx__vnji)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = wirtx__vnji(-1)
            if rank == root:
                val = recv(wirtx__vnji, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            edwzx__pllnn = arr.dtype.categories[max(val, 0)]
            return edwzx__pllnn
        return cat_getitem_impl
    if isinstance(arr, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        frvo__arvdf = arr.tz

        def tz_aware_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                data = arr[ind - arr_start].value
                send_arr = np.full(1, data)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = 0
            if rank == root:
                val = recv(np.int64, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            return bodo.hiframes.pd_timestamp_ext.convert_val_to_timestamp(val,
                frvo__arvdf)
        return tz_aware_getitem_impl
    bhbys__ierb = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, bhbys__ierb)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, bhbys__ierb)[0]
        if rank == root:
            val = recv(bhbys__ierb, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


def get_chunk_bounds(A):
    pass


@overload(get_chunk_bounds, jit_options={'cache': True})
def get_chunk_bounds_overload(A):
    if not (isinstance(A, types.Array) and isinstance(A.dtype, types.Integer)):
        raise BodoError(
            'get_chunk_bounds() only supports Numpy int input currently.')

    def impl(A):
        n_pes = get_size()
        wbnr__ozvj = np.empty(n_pes, np.int64)
        wilm__see = np.empty(n_pes, np.int8)
        val = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        irx__dnit = 1
        if len(A) != 0:
            val = A[-1]
            irx__dnit = 0
        allgather(wbnr__ozvj, np.int64(val))
        allgather(wilm__see, irx__dnit)
        for i, irx__dnit in enumerate(wilm__see):
            if irx__dnit and i != 0:
                wbnr__ozvj[i] = wbnr__ozvj[i - 1]
        return wbnr__ozvj
    return impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    fndem__vop = get_type_enum(out_data)
    assert typ_enum == fndem__vop
    if isinstance(send_data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or send_data in (boolean_array,
        datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    cboj__fcep = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        cboj__fcep += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    cboj__fcep += '  return\n'
    ynw__gwwfa = {}
    exec(cboj__fcep, {'alltoallv': alltoallv}, ynw__gwwfa)
    jqhl__vkf = ynw__gwwfa['f']
    return jqhl__vkf


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    tzg__luewf = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return tzg__luewf, count


@numba.njit
def get_start(total_size, pes, rank):
    fzfwi__kobtf = total_size % pes
    xyed__ozag = (total_size - fzfwi__kobtf) // pes
    return rank * xyed__ozag + min(rank, fzfwi__kobtf)


@numba.njit
def get_end(total_size, pes, rank):
    fzfwi__kobtf = total_size % pes
    xyed__ozag = (total_size - fzfwi__kobtf) // pes
    return (rank + 1) * xyed__ozag + min(rank + 1, fzfwi__kobtf)


@numba.njit
def get_node_portion(total_size, pes, rank):
    fzfwi__kobtf = total_size % pes
    xyed__ozag = (total_size - fzfwi__kobtf) // pes
    if rank < fzfwi__kobtf:
        return xyed__ozag + 1
    else:
        return xyed__ozag


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    yeltz__gbwz = in_arr.dtype(0)
    nxgu__lyuzp = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        adlx__mhfwj = yeltz__gbwz
        for edtr__nvjra in np.nditer(in_arr):
            adlx__mhfwj += edtr__nvjra.item()
        dszlp__wyerl = dist_exscan(adlx__mhfwj, nxgu__lyuzp)
        for i in range(in_arr.size):
            dszlp__wyerl += in_arr[i]
            out_arr[i] = dszlp__wyerl
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    pgd__tgm = in_arr.dtype(1)
    nxgu__lyuzp = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        adlx__mhfwj = pgd__tgm
        for edtr__nvjra in np.nditer(in_arr):
            adlx__mhfwj *= edtr__nvjra.item()
        dszlp__wyerl = dist_exscan(adlx__mhfwj, nxgu__lyuzp)
        if get_rank() == 0:
            dszlp__wyerl = pgd__tgm
        for i in range(in_arr.size):
            dszlp__wyerl *= in_arr[i]
            out_arr[i] = dszlp__wyerl
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        pgd__tgm = np.finfo(in_arr.dtype(1).dtype).max
    else:
        pgd__tgm = np.iinfo(in_arr.dtype(1).dtype).max
    nxgu__lyuzp = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        adlx__mhfwj = pgd__tgm
        for edtr__nvjra in np.nditer(in_arr):
            adlx__mhfwj = min(adlx__mhfwj, edtr__nvjra.item())
        dszlp__wyerl = dist_exscan(adlx__mhfwj, nxgu__lyuzp)
        if get_rank() == 0:
            dszlp__wyerl = pgd__tgm
        for i in range(in_arr.size):
            dszlp__wyerl = min(dszlp__wyerl, in_arr[i])
            out_arr[i] = dszlp__wyerl
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        pgd__tgm = np.finfo(in_arr.dtype(1).dtype).min
    else:
        pgd__tgm = np.iinfo(in_arr.dtype(1).dtype).min
    pgd__tgm = in_arr.dtype(1)
    nxgu__lyuzp = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        adlx__mhfwj = pgd__tgm
        for edtr__nvjra in np.nditer(in_arr):
            adlx__mhfwj = max(adlx__mhfwj, edtr__nvjra.item())
        dszlp__wyerl = dist_exscan(adlx__mhfwj, nxgu__lyuzp)
        if get_rank() == 0:
            dszlp__wyerl = pgd__tgm
        for i in range(in_arr.size):
            dszlp__wyerl = max(dszlp__wyerl, in_arr[i])
            out_arr[i] = dszlp__wyerl
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    bullj__gtv = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), bullj__gtv)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ibgj__depxf = args[0]
    if equiv_set.has_shape(ibgj__depxf):
        return ArrayAnalysis.AnalyzeResult(shape=ibgj__depxf, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)
ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_rep_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
@infer_global(rep_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


def print_if_not_empty(args):
    pass


@overload(print_if_not_empty)
def overload_print_if_not_empty(*args):
    smk__yejop = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for 
        i, enx__zlxsm in enumerate(args) if is_array_typ(enx__zlxsm) or
        isinstance(enx__zlxsm, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    cboj__fcep = f"""def impl(*args):
    if {smk__yejop} or bodo.get_rank() == 0:
        print(*args)"""
    ynw__gwwfa = {}
    exec(cboj__fcep, globals(), ynw__gwwfa)
    impl = ynw__gwwfa['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        vdau__ctly = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        cboj__fcep = 'def f(req, cond=True):\n'
        cboj__fcep += f'  return {vdau__ctly}\n'
        ynw__gwwfa = {}
        exec(cboj__fcep, {'_wait': _wait}, ynw__gwwfa)
        impl = ynw__gwwfa['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        fzfwi__kobtf = 1
        for a in t:
            fzfwi__kobtf *= a
        return fzfwi__kobtf
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    reu__ebd = np.ascontiguousarray(in_arr)
    lpwrd__ekrc = get_tuple_prod(reu__ebd.shape[1:])
    hceu__dpsd = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        ftbaf__gwmi = np.array(dest_ranks, dtype=np.int32)
    else:
        ftbaf__gwmi = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, reu__ebd.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * hceu__dpsd, dtype_size * lpwrd__ekrc, len
        (ftbaf__gwmi), ftbaf__gwmi.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp, types.int64))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len,
    n_samples):
    rhea__cqpz = np.ascontiguousarray(rhs)
    rbrx__goxck = get_tuple_prod(rhea__cqpz.shape[1:])
    btuz__rrva = dtype_size * rbrx__goxck
    permutation_array_index(lhs.ctypes, lhs_len, btuz__rrva, rhea__cqpz.
        ctypes, rhea__cqpz.shape[0], p.ctypes, p_len, n_samples)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def disconnect_hdfs_njit():
    disconnect_hdfs()


@numba.njit
def call_finalize():
    finalize()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks, root=MPI_ROOT):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype, root)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks, root)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks, root=MPI_ROOT):
    return lambda data, comm_ranks, nranks, root=MPI_ROOT: bcast_comm_impl(data
        , comm_ranks, nranks, root)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks, root=MPI_ROOT):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.bcast_comm()')
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        cboj__fcep = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        ynw__gwwfa = {}
        exec(cboj__fcep, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, ynw__gwwfa)
        ozlmb__npabt = ynw__gwwfa['bcast_scalar_impl']
        return ozlmb__npabt
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        qen__sio = len(data.columns)
        kkafb__tcjh = ', '.join('g_data_{}'.format(i) for i in range(qen__sio))
        qnkn__rntgh = ColNamesMetaType(data.columns)
        cboj__fcep = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(qen__sio):
            cboj__fcep += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            cboj__fcep += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        cboj__fcep += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        cboj__fcep += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        cboj__fcep += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(kkafb__tcjh))
        ynw__gwwfa = {}
        exec(cboj__fcep, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            qnkn__rntgh}, ynw__gwwfa)
        ztb__qszix = ynw__gwwfa['impl_df']
        return ztb__qszix
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            tzg__luewf = data._start
            oygon__fnx = data._stop
            cuws__ffjah = data._step
            pccjj__plzbc = data._name
            pccjj__plzbc = bcast_scalar(pccjj__plzbc, root)
            tzg__luewf = bcast_scalar(tzg__luewf, root)
            oygon__fnx = bcast_scalar(oygon__fnx, root)
            cuws__ffjah = bcast_scalar(cuws__ffjah, root)
            euhcz__oes = bodo.libs.array_kernels.calc_nitems(tzg__luewf,
                oygon__fnx, cuws__ffjah)
            chunk_start = bodo.libs.distributed_api.get_start(euhcz__oes,
                n_pes, rank)
            dvupg__qzeq = bodo.libs.distributed_api.get_node_portion(euhcz__oes
                , n_pes, rank)
            drlhd__zpymn = tzg__luewf + cuws__ffjah * chunk_start
            uprg__qhk = tzg__luewf + cuws__ffjah * (chunk_start + dvupg__qzeq)
            uprg__qhk = min(uprg__qhk, oygon__fnx)
            return bodo.hiframes.pd_index_ext.init_range_index(drlhd__zpymn,
                uprg__qhk, cuws__ffjah, pccjj__plzbc)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            wfgy__vctey = data._data
            pccjj__plzbc = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(wfgy__vctey,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, pccjj__plzbc)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            pccjj__plzbc = bodo.hiframes.pd_series_ext.get_series_name(data)
            ndc__mlewb = bodo.libs.distributed_api.bcast_comm_impl(pccjj__plzbc
                , comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            rpmhw__ebf = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rpmhw__ebf, ndc__mlewb)
        return impl_series
    if isinstance(data, types.BaseTuple):
        cboj__fcep = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        cboj__fcep += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        ynw__gwwfa = {}
        exec(cboj__fcep, {'bcast_comm_impl': bcast_comm_impl}, ynw__gwwfa)
        womp__milbb = ynw__gwwfa['impl_tuple']
        return womp__milbb
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    dvhky__ufhk = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    ugt__vmmm = (0,) * dvhky__ufhk

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        wfgy__vctey = np.ascontiguousarray(data)
        hmv__jheep = data.ctypes
        pgh__yim = ugt__vmmm
        if rank == root:
            pgh__yim = wfgy__vctey.shape
        pgh__yim = bcast_tuple(pgh__yim, root)
        vqk__kqwe = get_tuple_prod(pgh__yim[1:])
        send_counts = pgh__yim[0] * vqk__kqwe
        uqty__wymx = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(hmv__jheep, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(uqty__wymx.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return uqty__wymx.reshape((-1,) + pgh__yim[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        lqclq__tvgta = MPI.COMM_WORLD
        ibxab__xvxvu = MPI.Get_processor_name()
        lkbfg__lsps = lqclq__tvgta.allgather(ibxab__xvxvu)
        node_ranks = defaultdict(list)
        for i, wxb__vqru in enumerate(lkbfg__lsps):
            node_ranks[wxb__vqru].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    lqclq__tvgta = MPI.COMM_WORLD
    zzz__wjkd = lqclq__tvgta.Get_group()
    srro__awxff = zzz__wjkd.Incl(comm_ranks)
    rxcb__ewq = lqclq__tvgta.Create_group(srro__awxff)
    return rxcb__ewq


def get_nodes_first_ranks():
    plqtk__txebh = get_host_ranks()
    return np.array([iaxr__jfbt[0] for iaxr__jfbt in plqtk__txebh.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
