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
    krepv__tedxi = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, krepv__tedxi, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    krepv__tedxi = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, krepv__tedxi, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            krepv__tedxi = get_type_enum(arr)
            return _isend(arr.ctypes, size, krepv__tedxi, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        krepv__tedxi = np.int32(numba_to_c_type(arr.dtype))
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            otfe__ydb = size + 7 >> 3
            ybr__ogpl = _isend(arr._data.ctypes, size, krepv__tedxi, pe,
                tag, cond)
            xdem__udrbs = _isend(arr._null_bitmap.ctypes, otfe__ydb,
                suryp__qsxhc, pe, tag, cond)
            return ybr__ogpl, xdem__udrbs
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            zpa__jpcw = arr._data
            krepv__tedxi = get_type_enum(zpa__jpcw)
            return _isend(zpa__jpcw.ctypes, size, krepv__tedxi, pe, tag, cond)
        return impl_tz_arr
    if is_str_arr_type(arr) or arr == binary_array_type:
        rzzm__piow = np.int32(numba_to_c_type(offset_type))
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            anewi__rkq = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(anewi__rkq, pe, tag - 1)
            otfe__ydb = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                rzzm__piow, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), anewi__rkq,
                suryp__qsxhc, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), otfe__ydb,
                suryp__qsxhc, pe, tag)
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
            krepv__tedxi = get_type_enum(arr)
            return _irecv(arr.ctypes, size, krepv__tedxi, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        krepv__tedxi = np.int32(numba_to_c_type(arr.dtype))
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            otfe__ydb = size + 7 >> 3
            ybr__ogpl = _irecv(arr._data.ctypes, size, krepv__tedxi, pe,
                tag, cond)
            xdem__udrbs = _irecv(arr._null_bitmap.ctypes, otfe__ydb,
                suryp__qsxhc, pe, tag, cond)
            return ybr__ogpl, xdem__udrbs
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            zpa__jpcw = arr._data
            krepv__tedxi = get_type_enum(zpa__jpcw)
            return _irecv(zpa__jpcw.ctypes, size, krepv__tedxi, pe, tag, cond)
        return impl_tz_arr
    if arr in [binary_array_type, string_array_type]:
        rzzm__piow = np.int32(numba_to_c_type(offset_type))
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            zmp__atyt = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            zmp__atyt = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        erach__xjfk = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {zmp__atyt}(size, n_chars)
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
        lthmt__mqv = dict()
        exec(erach__xjfk, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            rzzm__piow, 'char_typ_enum': suryp__qsxhc}, lthmt__mqv)
        impl = lthmt__mqv['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    krepv__tedxi = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), krepv__tedxi)


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
        kxt__dhrk = n_pes if rank == root or allgather else 0
        bcf__ugsr = np.empty(kxt__dhrk, dtype)
        c_gather_scalar(send.ctypes, bcf__ugsr.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return bcf__ugsr
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
        ukgl__pqcgc = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], ukgl__pqcgc)
        return builder.bitcast(ukgl__pqcgc, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        ukgl__pqcgc = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(ukgl__pqcgc)
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
    kuos__kksoj = types.unliteral(value)
    if isinstance(kuos__kksoj, IndexValueType):
        kuos__kksoj = kuos__kksoj.val_typ
        auzz__brno = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            auzz__brno.append(types.int64)
            auzz__brno.append(bodo.datetime64ns)
            auzz__brno.append(bodo.timedelta64ns)
            auzz__brno.append(bodo.datetime_date_type)
            auzz__brno.append(bodo.TimeType)
        if kuos__kksoj not in auzz__brno:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(kuos__kksoj))
    typ_enum = np.int32(numba_to_c_type(kuos__kksoj))

    def impl(value, reduce_op):
        ahqle__hlxng = value_to_ptr(value)
        ayg__quj = value_to_ptr(value)
        _dist_reduce(ahqle__hlxng, ayg__quj, reduce_op, typ_enum)
        return load_val_ptr(ayg__quj, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    kuos__kksoj = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(kuos__kksoj))
    tmy__ymtku = kuos__kksoj(0)

    def impl(value, reduce_op):
        ahqle__hlxng = value_to_ptr(value)
        ayg__quj = value_to_ptr(tmy__ymtku)
        _dist_exscan(ahqle__hlxng, ayg__quj, reduce_op, typ_enum)
        return load_val_ptr(ayg__quj, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    hfv__fjqo = 0
    hvhrv__lvfg = 0
    for i in range(len(recv_counts)):
        djt__uyb = recv_counts[i]
        otfe__ydb = recv_counts_nulls[i]
        pjiq__uqp = tmp_null_bytes[hfv__fjqo:hfv__fjqo + otfe__ydb]
        for eycng__xcciq in range(djt__uyb):
            set_bit_to(null_bitmap_ptr, hvhrv__lvfg, get_bit(pjiq__uqp,
                eycng__xcciq))
            hvhrv__lvfg += 1
        hfv__fjqo += otfe__ydb


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            ipg__hnxn = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                ipg__hnxn, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            wlhro__iycig = data.size
            recv_counts = gather_scalar(np.int32(wlhro__iycig), allgather,
                root=root)
            xhfo__udmpt = recv_counts.sum()
            phhm__fof = empty_like_type(xhfo__udmpt, data)
            dav__rgi = np.empty(1, np.int32)
            if rank == root or allgather:
                dav__rgi = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(wlhro__iycig), phhm__fof.ctypes,
                recv_counts.ctypes, dav__rgi.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return phhm__fof.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            phhm__fof = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(phhm__fof)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            phhm__fof = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(phhm__fof)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            wlhro__iycig = len(data)
            otfe__ydb = wlhro__iycig + 7 >> 3
            recv_counts = gather_scalar(np.int32(wlhro__iycig), allgather,
                root=root)
            xhfo__udmpt = recv_counts.sum()
            phhm__fof = empty_like_type(xhfo__udmpt, data)
            dav__rgi = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            jhkq__azsqn = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                dav__rgi = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                jhkq__azsqn = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(wlhro__iycig),
                phhm__fof._days_data.ctypes, recv_counts.ctypes, dav__rgi.
                ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(wlhro__iycig),
                phhm__fof._seconds_data.ctypes, recv_counts.ctypes,
                dav__rgi.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(wlhro__iycig
                ), phhm__fof._microseconds_data.ctypes, recv_counts.ctypes,
                dav__rgi.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(otfe__ydb),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                jhkq__azsqn.ctypes, suryp__qsxhc, allgather, np.int32(root))
            copy_gathered_null_bytes(phhm__fof._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return phhm__fof
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, bodo.TimeArrayType)) or data in (boolean_array,
        datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            wlhro__iycig = len(data)
            otfe__ydb = wlhro__iycig + 7 >> 3
            recv_counts = gather_scalar(np.int32(wlhro__iycig), allgather,
                root=root)
            xhfo__udmpt = recv_counts.sum()
            phhm__fof = empty_like_type(xhfo__udmpt, data)
            dav__rgi = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            jhkq__azsqn = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                dav__rgi = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                jhkq__azsqn = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(wlhro__iycig), phhm__fof.
                _data.ctypes, recv_counts.ctypes, dav__rgi.ctypes, np.int32
                (typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(otfe__ydb),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                jhkq__azsqn.ctypes, suryp__qsxhc, allgather, np.int32(root))
            copy_gathered_null_bytes(phhm__fof._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return phhm__fof
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        qasrz__yjay = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            gwjz__gha = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                gwjz__gha, qasrz__yjay)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            mkye__lcmxu = bodo.gatherv(data._left, allgather, warn_if_rep, root
                )
            couln__eiiuo = bodo.gatherv(data._right, allgather, warn_if_rep,
                root)
            return bodo.libs.interval_arr_ext.init_interval_array(mkye__lcmxu,
                couln__eiiuo)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            rtija__vje = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            xaxb__vrq = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                xaxb__vrq, rtija__vje)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        udu__anqb = np.iinfo(np.int64).max
        mosn__qrdu = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cfyhl__krt = data._start
            afif__ztvs = data._stop
            if len(data) == 0:
                cfyhl__krt = udu__anqb
                afif__ztvs = mosn__qrdu
            cfyhl__krt = bodo.libs.distributed_api.dist_reduce(cfyhl__krt,
                np.int32(Reduce_Type.Min.value))
            afif__ztvs = bodo.libs.distributed_api.dist_reduce(afif__ztvs,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if cfyhl__krt == udu__anqb and afif__ztvs == mosn__qrdu:
                cfyhl__krt = 0
                afif__ztvs = 0
            zuvr__kkkvk = max(0, -(-(afif__ztvs - cfyhl__krt) // data._step))
            if zuvr__kkkvk < total_len:
                afif__ztvs = cfyhl__krt + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                cfyhl__krt = 0
                afif__ztvs = 0
            return bodo.hiframes.pd_index_ext.init_range_index(cfyhl__krt,
                afif__ztvs, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            dgtrv__cqag = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, dgtrv__cqag)
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
            phhm__fof = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(phhm__fof,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        zincv__wjaba = {'bodo': bodo, 'get_table_block': bodo.hiframes.
            table.get_table_block, 'ensure_column_unboxed': bodo.hiframes.
            table.ensure_column_unboxed, 'set_table_block': bodo.hiframes.
            table.set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table,
            'decode_if_dict_ary': bodo.hiframes.table.init_table}
        erach__xjfk = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        erach__xjfk += '  T = data\n'
        erach__xjfk += '  T2 = init_table(T, True)\n'
        jwxt__jwws = bodo.hiframes.table.get_init_table_output_type(data, True)
        nfijd__euu = (bodo.string_array_type in data.type_to_blk and bodo.
            dict_str_arr_type in data.type_to_blk)
        if nfijd__euu:
            erach__xjfk += (bodo.hiframes.table.
                gen_str_and_dict_enc_cols_to_one_block_fn_txt(data,
                jwxt__jwws, zincv__wjaba, True))
        for boj__kwn, urid__sizo in data.type_to_blk.items():
            if nfijd__euu and boj__kwn in (bodo.string_array_type, bodo.
                dict_str_arr_type):
                continue
            elif boj__kwn == bodo.dict_str_arr_type:
                assert bodo.string_array_type in jwxt__jwws.type_to_blk, 'Error in gatherv: If encoded string type is present in the input, then non-encoded string type should be present in the output'
                fgjg__ywkf = jwxt__jwws.type_to_blk[bodo.string_array_type]
            else:
                assert boj__kwn in jwxt__jwws.type_to_blk, 'Error in gatherv: All non-encoded string types present in the input should be present in the output'
                fgjg__ywkf = jwxt__jwws.type_to_blk[boj__kwn]
            zincv__wjaba[f'arr_inds_{urid__sizo}'] = np.array(data.
                block_to_arr_ind[urid__sizo], dtype=np.int64)
            erach__xjfk += (
                f'  arr_list_{urid__sizo} = get_table_block(T, {urid__sizo})\n'
                )
            erach__xjfk += f"""  out_arr_list_{urid__sizo} = alloc_list_like(arr_list_{urid__sizo}, len(arr_list_{urid__sizo}), True)
"""
            erach__xjfk += f'  for i in range(len(arr_list_{urid__sizo})):\n'
            erach__xjfk += (
                f'    arr_ind_{urid__sizo} = arr_inds_{urid__sizo}[i]\n')
            erach__xjfk += f"""    ensure_column_unboxed(T, arr_list_{urid__sizo}, i, arr_ind_{urid__sizo})
"""
            erach__xjfk += f"""    out_arr_{urid__sizo} = bodo.gatherv(arr_list_{urid__sizo}[i], allgather, warn_if_rep, root)
"""
            erach__xjfk += (
                f'    out_arr_list_{urid__sizo}[i] = out_arr_{urid__sizo}\n')
            erach__xjfk += (
                f'  T2 = set_table_block(T2, out_arr_list_{urid__sizo}, {fgjg__ywkf})\n'
                )
        erach__xjfk += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        erach__xjfk += f'  T2 = set_table_len(T2, length)\n'
        erach__xjfk += f'  return T2\n'
        lthmt__mqv = {}
        exec(erach__xjfk, zincv__wjaba, lthmt__mqv)
        jwn__gajse = lthmt__mqv['impl_table']
        return jwn__gajse
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kwawz__fpk = len(data.columns)
        if kwawz__fpk == 0:
            ftkg__vcqir = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                xkv__ujum = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    xkv__ujum, ftkg__vcqir)
            return impl
        aujhd__wme = ', '.join(f'g_data_{i}' for i in range(kwawz__fpk))
        erach__xjfk = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            trkpi__fqgtz = bodo.hiframes.pd_dataframe_ext.DataFrameType(data
                .data, data.index, data.columns, Distribution.REP, True)
            aujhd__wme = 'T2'
            erach__xjfk += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            erach__xjfk += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(kwawz__fpk):
                erach__xjfk += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                erach__xjfk += (
                    """  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)
"""
                    .format(i, i))
        erach__xjfk += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        erach__xjfk += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        erach__xjfk += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(aujhd__wme))
        lthmt__mqv = {}
        zincv__wjaba = {'bodo': bodo,
            '__col_name_meta_value_gatherv_with_cols': ColNamesMetaType(
            data.columns)}
        exec(erach__xjfk, zincv__wjaba, lthmt__mqv)
        kpoz__djav = lthmt__mqv['impl_df']
        return kpoz__djav
    if isinstance(data, ArrayItemArrayType):
        jix__tiln = np.int32(numba_to_c_type(types.int32))
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            dojb__waefc = bodo.libs.array_item_arr_ext.get_offsets(data)
            zpa__jpcw = bodo.libs.array_item_arr_ext.get_data(data)
            zpa__jpcw = zpa__jpcw[:dojb__waefc[-1]]
            pvrl__sqlrj = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            wlhro__iycig = len(data)
            vzi__dzj = np.empty(wlhro__iycig, np.uint32)
            otfe__ydb = wlhro__iycig + 7 >> 3
            for i in range(wlhro__iycig):
                vzi__dzj[i] = dojb__waefc[i + 1] - dojb__waefc[i]
            recv_counts = gather_scalar(np.int32(wlhro__iycig), allgather,
                root=root)
            xhfo__udmpt = recv_counts.sum()
            dav__rgi = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            jhkq__azsqn = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                dav__rgi = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for owkme__lvu in range(len(recv_counts)):
                    recv_counts_nulls[owkme__lvu] = recv_counts[owkme__lvu
                        ] + 7 >> 3
                jhkq__azsqn = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            zahg__qvvj = np.empty(xhfo__udmpt + 1, np.uint32)
            armfe__wae = bodo.gatherv(zpa__jpcw, allgather, warn_if_rep, root)
            kglgo__qtote = np.empty(xhfo__udmpt + 7 >> 3, np.uint8)
            c_gatherv(vzi__dzj.ctypes, np.int32(wlhro__iycig), zahg__qvvj.
                ctypes, recv_counts.ctypes, dav__rgi.ctypes, jix__tiln,
                allgather, np.int32(root))
            c_gatherv(pvrl__sqlrj.ctypes, np.int32(otfe__ydb),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                jhkq__azsqn.ctypes, suryp__qsxhc, allgather, np.int32(root))
            dummy_use(data)
            tugzp__wtqo = np.empty(xhfo__udmpt + 1, np.uint64)
            convert_len_arr_to_offset(zahg__qvvj.ctypes, tugzp__wtqo.ctypes,
                xhfo__udmpt)
            copy_gathered_null_bytes(kglgo__qtote.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                xhfo__udmpt, armfe__wae, tugzp__wtqo, kglgo__qtote)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        qgm__koghc = data.names
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            umofu__xxv = bodo.libs.struct_arr_ext.get_data(data)
            emh__jzsnz = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            qauly__rtrl = bodo.gatherv(umofu__xxv, allgather=allgather,
                root=root)
            rank = bodo.libs.distributed_api.get_rank()
            wlhro__iycig = len(data)
            otfe__ydb = wlhro__iycig + 7 >> 3
            recv_counts = gather_scalar(np.int32(wlhro__iycig), allgather,
                root=root)
            xhfo__udmpt = recv_counts.sum()
            dqfxm__aac = np.empty(xhfo__udmpt + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            jhkq__azsqn = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                jhkq__azsqn = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(emh__jzsnz.ctypes, np.int32(otfe__ydb),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                jhkq__azsqn.ctypes, suryp__qsxhc, allgather, np.int32(root))
            copy_gathered_null_bytes(dqfxm__aac.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(qauly__rtrl,
                dqfxm__aac, qgm__koghc)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            phhm__fof = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(phhm__fof)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            phhm__fof = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(phhm__fof)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            phhm__fof = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(phhm__fof)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            phhm__fof = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            xqd__uqe = bodo.gatherv(data.indices, allgather, warn_if_rep, root)
            xxsv__jhku = bodo.gatherv(data.indptr, allgather, warn_if_rep, root
                )
            elk__uthnt = gather_scalar(data.shape[0], allgather, root=root)
            qawcb__lakx = elk__uthnt.sum()
            kwawz__fpk = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            sfnu__uddke = np.empty(qawcb__lakx + 1, np.int64)
            xqd__uqe = xqd__uqe.astype(np.int64)
            sfnu__uddke[0] = 0
            ave__khw = 1
            fbbwa__cmoxm = 0
            for huphw__jpclw in elk__uthnt:
                for rkaa__vayen in range(huphw__jpclw):
                    ejh__lvmdu = xxsv__jhku[fbbwa__cmoxm + 1] - xxsv__jhku[
                        fbbwa__cmoxm]
                    sfnu__uddke[ave__khw] = sfnu__uddke[ave__khw - 1
                        ] + ejh__lvmdu
                    ave__khw += 1
                    fbbwa__cmoxm += 1
                fbbwa__cmoxm += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(phhm__fof,
                xqd__uqe, sfnu__uddke, (qawcb__lakx, kwawz__fpk))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        erach__xjfk = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        erach__xjfk += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        lthmt__mqv = {}
        exec(erach__xjfk, {'bodo': bodo}, lthmt__mqv)
        yotmq__rfj = lthmt__mqv['impl_tuple']
        return yotmq__rfj
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as jzme__hwq:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        erach__xjfk = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        ythvu__jlc = ', '.join([f"'{rtija__vje}'" for rtija__vje in data.names]
            )
        ghg__eky = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        erach__xjfk += f"""  return bodosql.context_ext.init_sql_context(({ythvu__jlc}, ), ({ghg__eky}, ), data.catalog)
"""
        lthmt__mqv = {}
        exec(erach__xjfk, {'bodo': bodo, 'bodosql': bodosql}, lthmt__mqv)
        pyq__hvua = lthmt__mqv['impl_bodosql_context']
        return pyq__hvua
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as jzme__hwq:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        erach__xjfk = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        erach__xjfk += f'  return data\n'
        lthmt__mqv = {}
        exec(erach__xjfk, {}, lthmt__mqv)
        pauh__vtpr = lthmt__mqv['impl_table_path']
        return pauh__vtpr
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    erach__xjfk = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    erach__xjfk += '    if random:\n'
    erach__xjfk += '        if random_seed is None:\n'
    erach__xjfk += '            random = 1\n'
    erach__xjfk += '        else:\n'
    erach__xjfk += '            random = 2\n'
    erach__xjfk += '    if random_seed is None:\n'
    erach__xjfk += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        jtut__qhqq = data
        kwawz__fpk = len(jtut__qhqq.columns)
        for i in range(kwawz__fpk):
            erach__xjfk += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        erach__xjfk += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        aujhd__wme = ', '.join(f'data_{i}' for i in range(kwawz__fpk))
        erach__xjfk += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(rhvn__dzpnp) for
            rhvn__dzpnp in range(kwawz__fpk))))
        erach__xjfk += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        erach__xjfk += '    if dests is None:\n'
        erach__xjfk += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        erach__xjfk += '    else:\n'
        erach__xjfk += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for vlt__dqjte in range(kwawz__fpk):
            erach__xjfk += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(vlt__dqjte))
        erach__xjfk += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(kwawz__fpk))
        erach__xjfk += '    delete_table(out_table)\n'
        erach__xjfk += '    if parallel:\n'
        erach__xjfk += '        delete_table(table_total)\n'
        aujhd__wme = ', '.join('out_arr_{}'.format(i) for i in range(
            kwawz__fpk))
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        erach__xjfk += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(aujhd__wme, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        erach__xjfk += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        erach__xjfk += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        erach__xjfk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        erach__xjfk += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        erach__xjfk += '    if dests is None:\n'
        erach__xjfk += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        erach__xjfk += '    else:\n'
        erach__xjfk += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        erach__xjfk += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        erach__xjfk += """    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)
"""
        erach__xjfk += '    delete_table(out_table)\n'
        erach__xjfk += '    if parallel:\n'
        erach__xjfk += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        erach__xjfk += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        erach__xjfk += '    if not parallel:\n'
        erach__xjfk += '        return data\n'
        erach__xjfk += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        erach__xjfk += '    if dests is None:\n'
        erach__xjfk += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        erach__xjfk += '    elif bodo.get_rank() not in dests:\n'
        erach__xjfk += '        dim0_local_size = 0\n'
        erach__xjfk += '    else:\n'
        erach__xjfk += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        erach__xjfk += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        erach__xjfk += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        erach__xjfk += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        erach__xjfk += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        erach__xjfk += '    if dests is None:\n'
        erach__xjfk += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        erach__xjfk += '    else:\n'
        erach__xjfk += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        erach__xjfk += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        erach__xjfk += '    delete_table(out_table)\n'
        erach__xjfk += '    if parallel:\n'
        erach__xjfk += '        delete_table(table_total)\n'
        erach__xjfk += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    lthmt__mqv = {}
    zincv__wjaba = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        zincv__wjaba.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(jtut__qhqq.columns)})
    exec(erach__xjfk, zincv__wjaba, lthmt__mqv)
    impl = lthmt__mqv['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    erach__xjfk = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        erach__xjfk += '    if seed is None:\n'
        erach__xjfk += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        erach__xjfk += '    np.random.seed(seed)\n'
        erach__xjfk += '    if not parallel:\n'
        erach__xjfk += '        data = data.copy()\n'
        erach__xjfk += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            erach__xjfk += '        data = data[:n_samples]\n'
        erach__xjfk += '        return data\n'
        erach__xjfk += '    else:\n'
        erach__xjfk += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        erach__xjfk += '        permutation = np.arange(dim0_global_size)\n'
        erach__xjfk += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            erach__xjfk += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            erach__xjfk += '        n_samples = dim0_global_size\n'
        erach__xjfk += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        erach__xjfk += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        erach__xjfk += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        erach__xjfk += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        erach__xjfk += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        erach__xjfk += '        return output\n'
    else:
        erach__xjfk += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            erach__xjfk += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            erach__xjfk += '    output = output[:local_n_samples]\n'
        erach__xjfk += '    return output\n'
    lthmt__mqv = {}
    exec(erach__xjfk, {'np': np, 'bodo': bodo}, lthmt__mqv)
    impl = lthmt__mqv['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    jlefo__uck = np.empty(sendcounts_nulls.sum(), np.uint8)
    hfv__fjqo = 0
    hvhrv__lvfg = 0
    for mpzao__kyms in range(len(sendcounts)):
        djt__uyb = sendcounts[mpzao__kyms]
        otfe__ydb = sendcounts_nulls[mpzao__kyms]
        pjiq__uqp = jlefo__uck[hfv__fjqo:hfv__fjqo + otfe__ydb]
        for eycng__xcciq in range(djt__uyb):
            set_bit_to_arr(pjiq__uqp, eycng__xcciq, get_bit_bitmap(
                null_bitmap_ptr, hvhrv__lvfg))
            hvhrv__lvfg += 1
        hfv__fjqo += otfe__ydb
    return jlefo__uck


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    bstf__uwj = MPI.COMM_WORLD
    data = bstf__uwj.bcast(data, root)
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
    nnzg__gbj = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    wftsk__qhyva = (0,) * nnzg__gbj

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        ktt__rqzj = np.ascontiguousarray(data)
        vfgwt__gbok = data.ctypes
        ielew__rdtw = wftsk__qhyva
        if rank == MPI_ROOT:
            ielew__rdtw = ktt__rqzj.shape
        ielew__rdtw = bcast_tuple(ielew__rdtw)
        xswdx__vhhu = get_tuple_prod(ielew__rdtw[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            ielew__rdtw[0])
        send_counts *= xswdx__vhhu
        wlhro__iycig = send_counts[rank]
        rwuap__qlu = np.empty(wlhro__iycig, dtype)
        dav__rgi = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(vfgwt__gbok, send_counts.ctypes, dav__rgi.ctypes,
            rwuap__qlu.ctypes, np.int32(wlhro__iycig), np.int32(typ_val))
        return rwuap__qlu.reshape((-1,) + ielew__rdtw[1:])
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
        cskla__bglp = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], cskla__bglp)
    if isinstance(dtype, FloatingArrayType):
        cskla__bglp = 'Float{}'.format(dtype.dtype.bitwidth)
        return pd.array([3.0], cskla__bglp)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        rtija__vje = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=rtija__vje)
        xchvr__smyrq = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(xchvr__smyrq)
        return pd.Index(arr, name=rtija__vje)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        rtija__vje = _get_name_value_for_type(dtype.name_typ)
        qgm__koghc = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        bvz__gqv = tuple(get_value_for_type(t) for t in dtype.array_types)
        bvz__gqv = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in bvz__gqv)
        val = pd.MultiIndex.from_arrays(bvz__gqv, names=qgm__koghc)
        val.name = rtija__vje
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        rtija__vje = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=rtija__vje)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        bvz__gqv = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({rtija__vje: arr for rtija__vje, arr in zip(
            dtype.columns, bvz__gqv)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        xchvr__smyrq = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(xchvr__smyrq[0],
            xchvr__smyrq[0])])
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
        jix__tiln = np.int32(numba_to_c_type(types.int32))
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            zmp__atyt = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            zmp__atyt = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        erach__xjfk = f"""def impl(
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
            recv_arr = {zmp__atyt}(n_loc, n_loc_char)

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
        lthmt__mqv = dict()
        exec(erach__xjfk, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            jix__tiln, 'char_typ_enum': suryp__qsxhc,
            'decode_if_dict_array': decode_if_dict_array}, lthmt__mqv)
        impl = lthmt__mqv['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        jix__tiln = np.int32(numba_to_c_type(types.int32))
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            eide__bhtzu = bodo.libs.array_item_arr_ext.get_offsets(data)
            yjxst__farmw = bodo.libs.array_item_arr_ext.get_data(data)
            yjxst__farmw = yjxst__farmw[:eide__bhtzu[-1]]
            zur__bmm = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            sirm__uip = bcast_scalar(len(data))
            jsvw__ujx = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                jsvw__ujx[i] = eide__bhtzu[i + 1] - eide__bhtzu[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                sirm__uip)
            dav__rgi = bodo.ir.join.calc_disp(send_counts)
            iqz__veri = np.empty(n_pes, np.int32)
            if rank == 0:
                iuffa__wenhv = 0
                for i in range(n_pes):
                    syu__fayej = 0
                    for rkaa__vayen in range(send_counts[i]):
                        syu__fayej += jsvw__ujx[iuffa__wenhv]
                        iuffa__wenhv += 1
                    iqz__veri[i] = syu__fayej
            bcast(iqz__veri)
            nqzju__yjxz = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                nqzju__yjxz[i] = send_counts[i] + 7 >> 3
            jhkq__azsqn = bodo.ir.join.calc_disp(nqzju__yjxz)
            wlhro__iycig = send_counts[rank]
            tpxvr__zcah = np.empty(wlhro__iycig + 1, np_offset_type)
            mln__aqbf = bodo.libs.distributed_api.scatterv_impl(yjxst__farmw,
                iqz__veri)
            buvsv__mfum = wlhro__iycig + 7 >> 3
            nhqqu__kmdo = np.empty(buvsv__mfum, np.uint8)
            tgx__qmspf = np.empty(wlhro__iycig, np.uint32)
            c_scatterv(jsvw__ujx.ctypes, send_counts.ctypes, dav__rgi.
                ctypes, tgx__qmspf.ctypes, np.int32(wlhro__iycig), jix__tiln)
            convert_len_arr_to_offset(tgx__qmspf.ctypes, tpxvr__zcah.ctypes,
                wlhro__iycig)
            btt__pgr = get_scatter_null_bytes_buff(zur__bmm.ctypes,
                send_counts, nqzju__yjxz)
            c_scatterv(btt__pgr.ctypes, nqzju__yjxz.ctypes, jhkq__azsqn.
                ctypes, nhqqu__kmdo.ctypes, np.int32(buvsv__mfum), suryp__qsxhc
                )
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                wlhro__iycig, mln__aqbf, tpxvr__zcah, nhqqu__kmdo)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or data in (boolean_array, datetime_date_array_type):
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            scgtw__wha = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, FloatingArrayType):
            scgtw__wha = bodo.libs.float_arr_ext.init_float_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            scgtw__wha = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            scgtw__wha = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            scgtw__wha = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            ktt__rqzj = data._data
            emh__jzsnz = data._null_bitmap
            thw__qzv = len(ktt__rqzj)
            mdgaf__klme = _scatterv_np(ktt__rqzj, send_counts)
            sirm__uip = bcast_scalar(thw__qzv)
            ryf__yvh = len(mdgaf__klme) + 7 >> 3
            liq__kihfb = np.empty(ryf__yvh, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                sirm__uip)
            nqzju__yjxz = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                nqzju__yjxz[i] = send_counts[i] + 7 >> 3
            jhkq__azsqn = bodo.ir.join.calc_disp(nqzju__yjxz)
            btt__pgr = get_scatter_null_bytes_buff(emh__jzsnz.ctypes,
                send_counts, nqzju__yjxz)
            c_scatterv(btt__pgr.ctypes, nqzju__yjxz.ctypes, jhkq__azsqn.
                ctypes, liq__kihfb.ctypes, np.int32(ryf__yvh), suryp__qsxhc)
            return scgtw__wha(mdgaf__klme, liq__kihfb)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            rnory__ztlf = bodo.libs.distributed_api.scatterv_impl(data.
                _left, send_counts)
            urbkk__qqc = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(rnory__ztlf,
                urbkk__qqc)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            cfyhl__krt = data._start
            afif__ztvs = data._stop
            fguvi__tuf = data._step
            rtija__vje = data._name
            rtija__vje = bcast_scalar(rtija__vje)
            cfyhl__krt = bcast_scalar(cfyhl__krt)
            afif__ztvs = bcast_scalar(afif__ztvs)
            fguvi__tuf = bcast_scalar(fguvi__tuf)
            mcr__gvum = bodo.libs.array_kernels.calc_nitems(cfyhl__krt,
                afif__ztvs, fguvi__tuf)
            chunk_start = bodo.libs.distributed_api.get_start(mcr__gvum,
                n_pes, rank)
            zsybl__bizyy = bodo.libs.distributed_api.get_node_portion(mcr__gvum
                , n_pes, rank)
            kgnfh__hybc = cfyhl__krt + fguvi__tuf * chunk_start
            mrb__njw = cfyhl__krt + fguvi__tuf * (chunk_start + zsybl__bizyy)
            mrb__njw = min(mrb__njw, afif__ztvs)
            return bodo.hiframes.pd_index_ext.init_range_index(kgnfh__hybc,
                mrb__njw, fguvi__tuf, rtija__vje)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        dgtrv__cqag = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            ktt__rqzj = data._data
            rtija__vje = data._name
            rtija__vje = bcast_scalar(rtija__vje)
            arr = bodo.libs.distributed_api.scatterv_impl(ktt__rqzj,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                rtija__vje, dgtrv__cqag)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            ktt__rqzj = data._data
            rtija__vje = data._name
            rtija__vje = bcast_scalar(rtija__vje)
            arr = bodo.libs.distributed_api.scatterv_impl(ktt__rqzj,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, rtija__vje)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            phhm__fof = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            rtija__vje = bcast_scalar(data._name)
            qgm__koghc = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(phhm__fof,
                qgm__koghc, rtija__vje)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            rtija__vje = bodo.hiframes.pd_series_ext.get_series_name(data)
            fqgm__bnnlc = bcast_scalar(rtija__vje)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            xaxb__vrq = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                xaxb__vrq, fqgm__bnnlc)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kwawz__fpk = len(data.columns)
        rgw__ikf = ColNamesMetaType(data.columns)
        erach__xjfk = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        if data.is_table_format:
            erach__xjfk += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            erach__xjfk += """  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)
"""
            aujhd__wme = 'g_table'
        else:
            for i in range(kwawz__fpk):
                erach__xjfk += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                erach__xjfk += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            aujhd__wme = ', '.join(f'g_data_{i}' for i in range(kwawz__fpk))
        erach__xjfk += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        erach__xjfk += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        erach__xjfk += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({aujhd__wme},), g_index, __col_name_meta_scaterv_impl)
"""
        lthmt__mqv = {}
        exec(erach__xjfk, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            rgw__ikf}, lthmt__mqv)
        kpoz__djav = lthmt__mqv['impl_df']
        return kpoz__djav
    if isinstance(data, bodo.TableType):
        erach__xjfk = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        erach__xjfk += '  T = data\n'
        erach__xjfk += '  T2 = init_table(T, False)\n'
        erach__xjfk += '  l = 0\n'
        zincv__wjaba = {}
        for ptt__giqr in data.type_to_blk.values():
            zincv__wjaba[f'arr_inds_{ptt__giqr}'] = np.array(data.
                block_to_arr_ind[ptt__giqr], dtype=np.int64)
            erach__xjfk += (
                f'  arr_list_{ptt__giqr} = get_table_block(T, {ptt__giqr})\n')
            erach__xjfk += f"""  out_arr_list_{ptt__giqr} = alloc_list_like(arr_list_{ptt__giqr}, len(arr_list_{ptt__giqr}), False)
"""
            erach__xjfk += f'  for i in range(len(arr_list_{ptt__giqr})):\n'
            erach__xjfk += (
                f'    arr_ind_{ptt__giqr} = arr_inds_{ptt__giqr}[i]\n')
            erach__xjfk += f"""    ensure_column_unboxed(T, arr_list_{ptt__giqr}, i, arr_ind_{ptt__giqr})
"""
            erach__xjfk += f"""    out_arr_{ptt__giqr} = bodo.libs.distributed_api.scatterv_impl(arr_list_{ptt__giqr}[i], send_counts)
"""
            erach__xjfk += (
                f'    out_arr_list_{ptt__giqr}[i] = out_arr_{ptt__giqr}\n')
            erach__xjfk += f'    l = len(out_arr_{ptt__giqr})\n'
            erach__xjfk += (
                f'  T2 = set_table_block(T2, out_arr_list_{ptt__giqr}, {ptt__giqr})\n'
                )
        erach__xjfk += f'  T2 = set_table_len(T2, l)\n'
        erach__xjfk += f'  return T2\n'
        zincv__wjaba.update({'bodo': bodo, 'init_table': bodo.hiframes.
            table.init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        lthmt__mqv = {}
        exec(erach__xjfk, zincv__wjaba, lthmt__mqv)
        return lthmt__mqv['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                hizt__iinqo = data._data
                bodo.libs.distributed_api.bcast_scalar(len(hizt__iinqo))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(hizt__iinqo)))
            else:
                zuvr__kkkvk = bodo.libs.distributed_api.bcast_scalar(0)
                anewi__rkq = bodo.libs.distributed_api.bcast_scalar(0)
                hizt__iinqo = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    zuvr__kkkvk, anewi__rkq)
            bodo.libs.distributed_api.bcast(hizt__iinqo)
            cizq__bxg = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(hizt__iinqo,
                cizq__bxg, True, data._has_deduped_local_dictionary)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            ipg__hnxn = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                ipg__hnxn, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        erach__xjfk = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        erach__xjfk += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        lthmt__mqv = {}
        exec(erach__xjfk, {'bodo': bodo}, lthmt__mqv)
        yotmq__rfj = lthmt__mqv['impl_tuple']
        return yotmq__rfj
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
        rzzm__piow = np.int32(numba_to_c_type(offset_type))
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            wlhro__iycig = len(data)
            bgvk__ejph = num_total_chars(data)
            assert wlhro__iycig < INT_MAX
            assert bgvk__ejph < INT_MAX
            ntcw__bwmp = get_offset_ptr(data)
            vfgwt__gbok = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            otfe__ydb = wlhro__iycig + 7 >> 3
            c_bcast(ntcw__bwmp, np.int32(wlhro__iycig + 1), rzzm__piow, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(vfgwt__gbok, np.int32(bgvk__ejph), suryp__qsxhc, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(otfe__ydb), suryp__qsxhc, np.
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
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                ddw__usobe = 0
                xufbh__urj = np.empty(0, np.uint8).ctypes
            else:
                xufbh__urj, ddw__usobe = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            ddw__usobe = bodo.libs.distributed_api.bcast_scalar(ddw__usobe,
                root)
            if rank != root:
                bli__jsk = np.empty(ddw__usobe + 1, np.uint8)
                bli__jsk[ddw__usobe] = 0
                xufbh__urj = bli__jsk.ctypes
            c_bcast(xufbh__urj, np.int32(ddw__usobe), suryp__qsxhc, np.
                array([-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(xufbh__urj, ddw__usobe)
        return impl_str
    typ_val = numba_to_c_type(val)
    erach__xjfk = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    lthmt__mqv = {}
    exec(erach__xjfk, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, lthmt__mqv)
    jis__zdqko = lthmt__mqv['bcast_scalar_impl']
    return jis__zdqko


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple
        ), 'Internal Error: Argument to bcast tuple must be of type tuple'
    czwpm__wlg = len(val)
    erach__xjfk = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    erach__xjfk += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(czwpm__wlg)),
        ',' if czwpm__wlg else '')
    lthmt__mqv = {}
    exec(erach__xjfk, {'bcast_scalar': bcast_scalar}, lthmt__mqv)
    xvy__qfqon = lthmt__mqv['bcast_tuple_impl']
    return xvy__qfqon


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            wlhro__iycig = bcast_scalar(len(arr), root)
            dqyx__zdc = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(wlhro__iycig, dqyx__zdc)
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
            kgnfh__hybc = max(arr_start, slice_index.start) - arr_start
            mrb__njw = max(slice_index.stop - arr_start, 0)
            return slice(kgnfh__hybc, mrb__njw)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            cfyhl__krt = slice_index.start
            fguvi__tuf = slice_index.step
            wzd__xfre = (0 if fguvi__tuf == 1 or cfyhl__krt > arr_start else
                abs(fguvi__tuf - arr_start % fguvi__tuf) % fguvi__tuf)
            kgnfh__hybc = max(arr_start, slice_index.start
                ) - arr_start + wzd__xfre
            mrb__njw = max(slice_index.stop - arr_start, 0)
            return slice(kgnfh__hybc, mrb__njw, fguvi__tuf)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        xso__tkzan = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[xso__tkzan])
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
        rfw__jkgl = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        suryp__qsxhc = np.int32(numba_to_c_type(types.uint8))
        wbip__bnfx = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            ktcn__lxjut = np.int32(10)
            tag = np.int32(11)
            ipfui__mtnbf = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                zpa__jpcw = arr._data
                rvhok__poitn = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    zpa__jpcw, ind)
                siz__uuw = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    zpa__jpcw, ind + 1)
                length = siz__uuw - rvhok__poitn
                ukgl__pqcgc = zpa__jpcw[ind]
                ipfui__mtnbf[0] = length
                isend(ipfui__mtnbf, np.int32(1), root, ktcn__lxjut, True)
                isend(ukgl__pqcgc, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(wbip__bnfx
                , rfw__jkgl, 0, 1)
            zuvr__kkkvk = 0
            if rank == root:
                zuvr__kkkvk = recv(np.int64, ANY_SOURCE, ktcn__lxjut)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    wbip__bnfx, rfw__jkgl, zuvr__kkkvk, 1)
                vfgwt__gbok = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(vfgwt__gbok, np.int32(zuvr__kkkvk), suryp__qsxhc,
                    ANY_SOURCE, tag)
            dummy_use(ipfui__mtnbf)
            zuvr__kkkvk = bcast_scalar(zuvr__kkkvk)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    wbip__bnfx, rfw__jkgl, zuvr__kkkvk, 1)
            vfgwt__gbok = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(vfgwt__gbok, np.int32(zuvr__kkkvk), suryp__qsxhc, np.
                array([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, zuvr__kkkvk)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        awgbg__mwued = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, awgbg__mwued)
            if arr_start <= ind < arr_start + len(arr):
                ipg__hnxn = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = ipg__hnxn[ind - arr_start]
                send_arr = np.full(1, data, awgbg__mwued)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = awgbg__mwued(-1)
            if rank == root:
                val = recv(awgbg__mwued, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            eiaix__ctgvh = arr.dtype.categories[max(val, 0)]
            return eiaix__ctgvh
        return cat_getitem_impl
    if isinstance(arr, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        mbl__zrwu = arr.tz

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
                mbl__zrwu)
        return tz_aware_getitem_impl
    sofkw__xpx = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, sofkw__xpx)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, sofkw__xpx)[0]
        if rank == root:
            val = recv(sofkw__xpx, ANY_SOURCE, tag)
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
        xfwy__uzhtn = np.empty(n_pes, np.int64)
        fsk__cznqz = np.empty(n_pes, np.int8)
        val = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        ashqz__tovkf = 1
        if len(A) != 0:
            val = A[-1]
            ashqz__tovkf = 0
        allgather(xfwy__uzhtn, np.int64(val))
        allgather(fsk__cznqz, ashqz__tovkf)
        for i, ashqz__tovkf in enumerate(fsk__cznqz):
            if ashqz__tovkf and i != 0:
                xfwy__uzhtn[i] = xfwy__uzhtn[i - 1]
        return xfwy__uzhtn
    return impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    bjy__dra = get_type_enum(out_data)
    assert typ_enum == bjy__dra
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
    erach__xjfk = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        erach__xjfk += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    erach__xjfk += '  return\n'
    lthmt__mqv = {}
    exec(erach__xjfk, {'alltoallv': alltoallv}, lthmt__mqv)
    trbb__ladzm = lthmt__mqv['f']
    return trbb__ladzm


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    cfyhl__krt = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return cfyhl__krt, count


@numba.njit
def get_start(total_size, pes, rank):
    bcf__ugsr = total_size % pes
    chx__kkq = (total_size - bcf__ugsr) // pes
    return rank * chx__kkq + min(rank, bcf__ugsr)


@numba.njit
def get_end(total_size, pes, rank):
    bcf__ugsr = total_size % pes
    chx__kkq = (total_size - bcf__ugsr) // pes
    return (rank + 1) * chx__kkq + min(rank + 1, bcf__ugsr)


@numba.njit
def get_node_portion(total_size, pes, rank):
    bcf__ugsr = total_size % pes
    chx__kkq = (total_size - bcf__ugsr) // pes
    if rank < bcf__ugsr:
        return chx__kkq + 1
    else:
        return chx__kkq


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    tmy__ymtku = in_arr.dtype(0)
    rsci__leq = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        syu__fayej = tmy__ymtku
        for glwz__wxqz in np.nditer(in_arr):
            syu__fayej += glwz__wxqz.item()
        bjmki__dvigx = dist_exscan(syu__fayej, rsci__leq)
        for i in range(in_arr.size):
            bjmki__dvigx += in_arr[i]
            out_arr[i] = bjmki__dvigx
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    lxi__gmb = in_arr.dtype(1)
    rsci__leq = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        syu__fayej = lxi__gmb
        for glwz__wxqz in np.nditer(in_arr):
            syu__fayej *= glwz__wxqz.item()
        bjmki__dvigx = dist_exscan(syu__fayej, rsci__leq)
        if get_rank() == 0:
            bjmki__dvigx = lxi__gmb
        for i in range(in_arr.size):
            bjmki__dvigx *= in_arr[i]
            out_arr[i] = bjmki__dvigx
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        lxi__gmb = np.finfo(in_arr.dtype(1).dtype).max
    else:
        lxi__gmb = np.iinfo(in_arr.dtype(1).dtype).max
    rsci__leq = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        syu__fayej = lxi__gmb
        for glwz__wxqz in np.nditer(in_arr):
            syu__fayej = min(syu__fayej, glwz__wxqz.item())
        bjmki__dvigx = dist_exscan(syu__fayej, rsci__leq)
        if get_rank() == 0:
            bjmki__dvigx = lxi__gmb
        for i in range(in_arr.size):
            bjmki__dvigx = min(bjmki__dvigx, in_arr[i])
            out_arr[i] = bjmki__dvigx
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        lxi__gmb = np.finfo(in_arr.dtype(1).dtype).min
    else:
        lxi__gmb = np.iinfo(in_arr.dtype(1).dtype).min
    lxi__gmb = in_arr.dtype(1)
    rsci__leq = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        syu__fayej = lxi__gmb
        for glwz__wxqz in np.nditer(in_arr):
            syu__fayej = max(syu__fayej, glwz__wxqz.item())
        bjmki__dvigx = dist_exscan(syu__fayej, rsci__leq)
        if get_rank() == 0:
            bjmki__dvigx = lxi__gmb
        for i in range(in_arr.size):
            bjmki__dvigx = max(bjmki__dvigx, in_arr[i])
            out_arr[i] = bjmki__dvigx
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    krepv__tedxi = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), krepv__tedxi)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    jrvex__wlep = args[0]
    if equiv_set.has_shape(jrvex__wlep):
        return ArrayAnalysis.AnalyzeResult(shape=jrvex__wlep, pre=[])
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
    cklgc__kfq = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for 
        i, rksm__yggax in enumerate(args) if is_array_typ(rksm__yggax) or
        isinstance(rksm__yggax, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    erach__xjfk = f"""def impl(*args):
    if {cklgc__kfq} or bodo.get_rank() == 0:
        print(*args)"""
    lthmt__mqv = {}
    exec(erach__xjfk, globals(), lthmt__mqv)
    impl = lthmt__mqv['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        snhz__imybr = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        erach__xjfk = 'def f(req, cond=True):\n'
        erach__xjfk += f'  return {snhz__imybr}\n'
        lthmt__mqv = {}
        exec(erach__xjfk, {'_wait': _wait}, lthmt__mqv)
        impl = lthmt__mqv['f']
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
        bcf__ugsr = 1
        for a in t:
            bcf__ugsr *= a
        return bcf__ugsr
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    yavp__cqib = np.ascontiguousarray(in_arr)
    zzpjy__zlu = get_tuple_prod(yavp__cqib.shape[1:])
    vkwl__ibmyf = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        zxib__rqrz = np.array(dest_ranks, dtype=np.int32)
    else:
        zxib__rqrz = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, yavp__cqib.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * vkwl__ibmyf, dtype_size * zzpjy__zlu, len
        (zxib__rqrz), zxib__rqrz.ctypes)
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
    lqw__mrzy = np.ascontiguousarray(rhs)
    ihqwq__bwm = get_tuple_prod(lqw__mrzy.shape[1:])
    enjqg__jkozk = dtype_size * ihqwq__bwm
    permutation_array_index(lhs.ctypes, lhs_len, enjqg__jkozk, lqw__mrzy.
        ctypes, lqw__mrzy.shape[0], p.ctypes, p_len, n_samples)
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
        erach__xjfk = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        lthmt__mqv = {}
        exec(erach__xjfk, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, lthmt__mqv)
        jis__zdqko = lthmt__mqv['bcast_scalar_impl']
        return jis__zdqko
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kwawz__fpk = len(data.columns)
        aujhd__wme = ', '.join('g_data_{}'.format(i) for i in range(kwawz__fpk)
            )
        wgr__vyinb = ColNamesMetaType(data.columns)
        erach__xjfk = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(kwawz__fpk):
            erach__xjfk += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            erach__xjfk += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        erach__xjfk += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        erach__xjfk += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        erach__xjfk += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(aujhd__wme))
        lthmt__mqv = {}
        exec(erach__xjfk, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            wgr__vyinb}, lthmt__mqv)
        kpoz__djav = lthmt__mqv['impl_df']
        return kpoz__djav
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            cfyhl__krt = data._start
            afif__ztvs = data._stop
            fguvi__tuf = data._step
            rtija__vje = data._name
            rtija__vje = bcast_scalar(rtija__vje, root)
            cfyhl__krt = bcast_scalar(cfyhl__krt, root)
            afif__ztvs = bcast_scalar(afif__ztvs, root)
            fguvi__tuf = bcast_scalar(fguvi__tuf, root)
            mcr__gvum = bodo.libs.array_kernels.calc_nitems(cfyhl__krt,
                afif__ztvs, fguvi__tuf)
            chunk_start = bodo.libs.distributed_api.get_start(mcr__gvum,
                n_pes, rank)
            zsybl__bizyy = bodo.libs.distributed_api.get_node_portion(mcr__gvum
                , n_pes, rank)
            kgnfh__hybc = cfyhl__krt + fguvi__tuf * chunk_start
            mrb__njw = cfyhl__krt + fguvi__tuf * (chunk_start + zsybl__bizyy)
            mrb__njw = min(mrb__njw, afif__ztvs)
            return bodo.hiframes.pd_index_ext.init_range_index(kgnfh__hybc,
                mrb__njw, fguvi__tuf, rtija__vje)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            ktt__rqzj = data._data
            rtija__vje = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(ktt__rqzj,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, rtija__vje)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            rtija__vje = bodo.hiframes.pd_series_ext.get_series_name(data)
            fqgm__bnnlc = bodo.libs.distributed_api.bcast_comm_impl(rtija__vje,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            xaxb__vrq = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                xaxb__vrq, fqgm__bnnlc)
        return impl_series
    if isinstance(data, types.BaseTuple):
        erach__xjfk = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        erach__xjfk += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        lthmt__mqv = {}
        exec(erach__xjfk, {'bcast_comm_impl': bcast_comm_impl}, lthmt__mqv)
        yotmq__rfj = lthmt__mqv['impl_tuple']
        return yotmq__rfj
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    nnzg__gbj = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    wftsk__qhyva = (0,) * nnzg__gbj

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        ktt__rqzj = np.ascontiguousarray(data)
        vfgwt__gbok = data.ctypes
        ielew__rdtw = wftsk__qhyva
        if rank == root:
            ielew__rdtw = ktt__rqzj.shape
        ielew__rdtw = bcast_tuple(ielew__rdtw, root)
        xswdx__vhhu = get_tuple_prod(ielew__rdtw[1:])
        send_counts = ielew__rdtw[0] * xswdx__vhhu
        rwuap__qlu = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(vfgwt__gbok, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(rwuap__qlu.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return rwuap__qlu.reshape((-1,) + ielew__rdtw[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        bstf__uwj = MPI.COMM_WORLD
        yrq__wobci = MPI.Get_processor_name()
        jcdtb__hmpny = bstf__uwj.allgather(yrq__wobci)
        node_ranks = defaultdict(list)
        for i, ibc__faebo in enumerate(jcdtb__hmpny):
            node_ranks[ibc__faebo].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    bstf__uwj = MPI.COMM_WORLD
    srf__mvytv = bstf__uwj.Get_group()
    plp__arseo = srf__mvytv.Incl(comm_ranks)
    anewh__svy = bstf__uwj.Create_group(plp__arseo)
    return anewh__svy


def get_nodes_first_ranks():
    wnfwm__fqb = get_host_ranks()
    return np.array([kogn__pwzbv[0] for kogn__pwzbv in wnfwm__fqb.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
