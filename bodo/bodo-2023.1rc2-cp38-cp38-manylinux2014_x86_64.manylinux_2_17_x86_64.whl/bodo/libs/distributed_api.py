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
    bbnf__kiq = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, bbnf__kiq, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    bbnf__kiq = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, bbnf__kiq, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            bbnf__kiq = get_type_enum(arr)
            return _isend(arr.ctypes, size, bbnf__kiq, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        bbnf__kiq = np.int32(numba_to_c_type(arr.dtype))
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            vdi__nnqv = size + 7 >> 3
            vsca__vfotr = _isend(arr._data.ctypes, size, bbnf__kiq, pe, tag,
                cond)
            toef__pxi = _isend(arr._null_bitmap.ctypes, vdi__nnqv,
                izwun__pbv, pe, tag, cond)
            return vsca__vfotr, toef__pxi
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            zctn__rtkn = arr._data
            bbnf__kiq = get_type_enum(zctn__rtkn)
            return _isend(zctn__rtkn.ctypes, size, bbnf__kiq, pe, tag, cond)
        return impl_tz_arr
    if is_str_arr_type(arr) or arr == binary_array_type:
        rfn__lveiv = np.int32(numba_to_c_type(offset_type))
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            kjauj__hlsn = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(kjauj__hlsn, pe, tag - 1)
            vdi__nnqv = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                rfn__lveiv, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), kjauj__hlsn,
                izwun__pbv, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), vdi__nnqv,
                izwun__pbv, pe, tag)
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
            bbnf__kiq = get_type_enum(arr)
            return _irecv(arr.ctypes, size, bbnf__kiq, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        bbnf__kiq = np.int32(numba_to_c_type(arr.dtype))
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            vdi__nnqv = size + 7 >> 3
            vsca__vfotr = _irecv(arr._data.ctypes, size, bbnf__kiq, pe, tag,
                cond)
            toef__pxi = _irecv(arr._null_bitmap.ctypes, vdi__nnqv,
                izwun__pbv, pe, tag, cond)
            return vsca__vfotr, toef__pxi
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            zctn__rtkn = arr._data
            bbnf__kiq = get_type_enum(zctn__rtkn)
            return _irecv(zctn__rtkn.ctypes, size, bbnf__kiq, pe, tag, cond)
        return impl_tz_arr
    if arr in [binary_array_type, string_array_type]:
        rfn__lveiv = np.int32(numba_to_c_type(offset_type))
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            tmpa__tvv = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            tmpa__tvv = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        rzes__wmeh = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {tmpa__tvv}(size, n_chars)
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
        cycm__rujg = dict()
        exec(rzes__wmeh, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            rfn__lveiv, 'char_typ_enum': izwun__pbv}, cycm__rujg)
        impl = cycm__rujg['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    bbnf__kiq = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), bbnf__kiq)


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
        dxj__xxtmb = n_pes if rank == root or allgather else 0
        hpn__cfpj = np.empty(dxj__xxtmb, dtype)
        c_gather_scalar(send.ctypes, hpn__cfpj.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return hpn__cfpj
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
        qehns__xiryg = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], qehns__xiryg)
        return builder.bitcast(qehns__xiryg, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        qehns__xiryg = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(qehns__xiryg)
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
    jaag__utpkb = types.unliteral(value)
    if isinstance(jaag__utpkb, IndexValueType):
        jaag__utpkb = jaag__utpkb.val_typ
        yuj__upmbs = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            yuj__upmbs.append(types.int64)
            yuj__upmbs.append(bodo.datetime64ns)
            yuj__upmbs.append(bodo.timedelta64ns)
            yuj__upmbs.append(bodo.datetime_date_type)
            yuj__upmbs.append(bodo.TimeType)
        if jaag__utpkb not in yuj__upmbs:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(jaag__utpkb))
    typ_enum = np.int32(numba_to_c_type(jaag__utpkb))

    def impl(value, reduce_op):
        mtuj__omcm = value_to_ptr(value)
        wdkl__hkvhh = value_to_ptr(value)
        _dist_reduce(mtuj__omcm, wdkl__hkvhh, reduce_op, typ_enum)
        return load_val_ptr(wdkl__hkvhh, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    jaag__utpkb = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(jaag__utpkb))
    ozeuy__sdn = jaag__utpkb(0)

    def impl(value, reduce_op):
        mtuj__omcm = value_to_ptr(value)
        wdkl__hkvhh = value_to_ptr(ozeuy__sdn)
        _dist_exscan(mtuj__omcm, wdkl__hkvhh, reduce_op, typ_enum)
        return load_val_ptr(wdkl__hkvhh, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    edqo__hnuh = 0
    tmb__vkw = 0
    for i in range(len(recv_counts)):
        tvc__rnc = recv_counts[i]
        vdi__nnqv = recv_counts_nulls[i]
        tnavz__ygvz = tmp_null_bytes[edqo__hnuh:edqo__hnuh + vdi__nnqv]
        for esc__mmfz in range(tvc__rnc):
            set_bit_to(null_bitmap_ptr, tmb__vkw, get_bit(tnavz__ygvz,
                esc__mmfz))
            tmb__vkw += 1
        edqo__hnuh += vdi__nnqv


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            jzak__aedzt = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                jzak__aedzt, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            zuhn__rvo = data.size
            recv_counts = gather_scalar(np.int32(zuhn__rvo), allgather,
                root=root)
            gmqc__fcqfo = recv_counts.sum()
            zkwpr__vgtuv = empty_like_type(gmqc__fcqfo, data)
            ncb__qvmmx = np.empty(1, np.int32)
            if rank == root or allgather:
                ncb__qvmmx = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(zuhn__rvo), zkwpr__vgtuv.ctypes,
                recv_counts.ctypes, ncb__qvmmx.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return zkwpr__vgtuv.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            zkwpr__vgtuv = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.str_arr_ext.init_str_arr(zkwpr__vgtuv)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            zkwpr__vgtuv = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.binary_arr_ext.init_binary_arr(zkwpr__vgtuv)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            zuhn__rvo = len(data)
            vdi__nnqv = zuhn__rvo + 7 >> 3
            recv_counts = gather_scalar(np.int32(zuhn__rvo), allgather,
                root=root)
            gmqc__fcqfo = recv_counts.sum()
            zkwpr__vgtuv = empty_like_type(gmqc__fcqfo, data)
            ncb__qvmmx = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            ghm__yml = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                ncb__qvmmx = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                ghm__yml = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(zuhn__rvo),
                zkwpr__vgtuv._days_data.ctypes, recv_counts.ctypes,
                ncb__qvmmx.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._seconds_data.ctypes, np.int32(zuhn__rvo),
                zkwpr__vgtuv._seconds_data.ctypes, recv_counts.ctypes,
                ncb__qvmmx.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(zuhn__rvo),
                zkwpr__vgtuv._microseconds_data.ctypes, recv_counts.ctypes,
                ncb__qvmmx.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._null_bitmap.ctypes, np.int32(vdi__nnqv),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, ghm__yml.
                ctypes, izwun__pbv, allgather, np.int32(root))
            copy_gathered_null_bytes(zkwpr__vgtuv._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return zkwpr__vgtuv
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, bodo.TimeArrayType)) or data in (boolean_array,
        datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            zuhn__rvo = len(data)
            vdi__nnqv = zuhn__rvo + 7 >> 3
            recv_counts = gather_scalar(np.int32(zuhn__rvo), allgather,
                root=root)
            gmqc__fcqfo = recv_counts.sum()
            zkwpr__vgtuv = empty_like_type(gmqc__fcqfo, data)
            ncb__qvmmx = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            ghm__yml = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                ncb__qvmmx = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                ghm__yml = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(zuhn__rvo), zkwpr__vgtuv.
                _data.ctypes, recv_counts.ctypes, ncb__qvmmx.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(vdi__nnqv),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, ghm__yml.
                ctypes, izwun__pbv, allgather, np.int32(root))
            copy_gathered_null_bytes(zkwpr__vgtuv._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return zkwpr__vgtuv
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        dinjf__ebtj = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            cumys__bxf = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                cumys__bxf, dinjf__ebtj)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            wdnz__ikt = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            smqv__iha = bodo.gatherv(data._right, allgather, warn_if_rep, root)
            return bodo.libs.interval_arr_ext.init_interval_array(wdnz__ikt,
                smqv__iha)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            joe__lbziz = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            zef__dfw = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                zef__dfw, joe__lbziz)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        druv__cbaz = np.iinfo(np.int64).max
        jluv__tegf = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            gux__mzqm = data._start
            rzwp__fzxno = data._stop
            if len(data) == 0:
                gux__mzqm = druv__cbaz
                rzwp__fzxno = jluv__tegf
            gux__mzqm = bodo.libs.distributed_api.dist_reduce(gux__mzqm, np
                .int32(Reduce_Type.Min.value))
            rzwp__fzxno = bodo.libs.distributed_api.dist_reduce(rzwp__fzxno,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if gux__mzqm == druv__cbaz and rzwp__fzxno == jluv__tegf:
                gux__mzqm = 0
                rzwp__fzxno = 0
            law__lxnv = max(0, -(-(rzwp__fzxno - gux__mzqm) // data._step))
            if law__lxnv < total_len:
                rzwp__fzxno = gux__mzqm + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                gux__mzqm = 0
                rzwp__fzxno = 0
            return bodo.hiframes.pd_index_ext.init_range_index(gux__mzqm,
                rzwp__fzxno, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            tfhh__uodm = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, tfhh__uodm)
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
            zkwpr__vgtuv = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                zkwpr__vgtuv, data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        ait__gtho = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table,
            'decode_if_dict_ary': bodo.hiframes.table.init_table}
        rzes__wmeh = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        rzes__wmeh += '  T = data\n'
        rzes__wmeh += '  T2 = init_table(T, True)\n'
        mvzij__aidk = bodo.hiframes.table.get_init_table_output_type(data, True
            )
        kqz__ysqi = (bodo.string_array_type in data.type_to_blk and bodo.
            dict_str_arr_type in data.type_to_blk)
        if kqz__ysqi:
            rzes__wmeh += (bodo.hiframes.table.
                gen_str_and_dict_enc_cols_to_one_block_fn_txt(data,
                mvzij__aidk, ait__gtho, True))
        for dff__hpxh, xicq__rjafv in data.type_to_blk.items():
            if kqz__ysqi and dff__hpxh in (bodo.string_array_type, bodo.
                dict_str_arr_type):
                continue
            elif dff__hpxh == bodo.dict_str_arr_type:
                assert bodo.string_array_type in mvzij__aidk.type_to_blk, 'Error in gatherv: If encoded string type is present in the input, then non-encoded string type should be present in the output'
                lmfgn__rkf = mvzij__aidk.type_to_blk[bodo.string_array_type]
            else:
                assert dff__hpxh in mvzij__aidk.type_to_blk, 'Error in gatherv: All non-encoded string types present in the input should be present in the output'
                lmfgn__rkf = mvzij__aidk.type_to_blk[dff__hpxh]
            ait__gtho[f'arr_inds_{xicq__rjafv}'] = np.array(data.
                block_to_arr_ind[xicq__rjafv], dtype=np.int64)
            rzes__wmeh += (
                f'  arr_list_{xicq__rjafv} = get_table_block(T, {xicq__rjafv})\n'
                )
            rzes__wmeh += f"""  out_arr_list_{xicq__rjafv} = alloc_list_like(arr_list_{xicq__rjafv}, len(arr_list_{xicq__rjafv}), True)
"""
            rzes__wmeh += f'  for i in range(len(arr_list_{xicq__rjafv})):\n'
            rzes__wmeh += (
                f'    arr_ind_{xicq__rjafv} = arr_inds_{xicq__rjafv}[i]\n')
            rzes__wmeh += f"""    ensure_column_unboxed(T, arr_list_{xicq__rjafv}, i, arr_ind_{xicq__rjafv})
"""
            rzes__wmeh += f"""    out_arr_{xicq__rjafv} = bodo.gatherv(arr_list_{xicq__rjafv}[i], allgather, warn_if_rep, root)
"""
            rzes__wmeh += (
                f'    out_arr_list_{xicq__rjafv}[i] = out_arr_{xicq__rjafv}\n')
            rzes__wmeh += (
                f'  T2 = set_table_block(T2, out_arr_list_{xicq__rjafv}, {lmfgn__rkf})\n'
                )
        rzes__wmeh += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        rzes__wmeh += f'  T2 = set_table_len(T2, length)\n'
        rzes__wmeh += f'  return T2\n'
        cycm__rujg = {}
        exec(rzes__wmeh, ait__gtho, cycm__rujg)
        msxwz__wjsqc = cycm__rujg['impl_table']
        return msxwz__wjsqc
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        mzpgr__avslh = len(data.columns)
        if mzpgr__avslh == 0:
            ynclq__nyefp = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                etga__aey = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    etga__aey, ynclq__nyefp)
            return impl
        lsoln__tpo = ', '.join(f'g_data_{i}' for i in range(mzpgr__avslh))
        rzes__wmeh = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            vwycq__byesp = bodo.hiframes.pd_dataframe_ext.DataFrameType(data
                .data, data.index, data.columns, Distribution.REP, True)
            lsoln__tpo = 'T2'
            rzes__wmeh += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            rzes__wmeh += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(mzpgr__avslh):
                rzes__wmeh += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                rzes__wmeh += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        rzes__wmeh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        rzes__wmeh += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        rzes__wmeh += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(lsoln__tpo))
        cycm__rujg = {}
        ait__gtho = {'bodo': bodo,
            '__col_name_meta_value_gatherv_with_cols': ColNamesMetaType(
            data.columns)}
        exec(rzes__wmeh, ait__gtho, cycm__rujg)
        gdrd__rxz = cycm__rujg['impl_df']
        return gdrd__rxz
    if isinstance(data, ArrayItemArrayType):
        rbpch__aje = np.int32(numba_to_c_type(types.int32))
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            gwf__ndqap = bodo.libs.array_item_arr_ext.get_offsets(data)
            zctn__rtkn = bodo.libs.array_item_arr_ext.get_data(data)
            zctn__rtkn = zctn__rtkn[:gwf__ndqap[-1]]
            ilocp__zmb = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            zuhn__rvo = len(data)
            tgz__tmyf = np.empty(zuhn__rvo, np.uint32)
            vdi__nnqv = zuhn__rvo + 7 >> 3
            for i in range(zuhn__rvo):
                tgz__tmyf[i] = gwf__ndqap[i + 1] - gwf__ndqap[i]
            recv_counts = gather_scalar(np.int32(zuhn__rvo), allgather,
                root=root)
            gmqc__fcqfo = recv_counts.sum()
            ncb__qvmmx = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            ghm__yml = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                ncb__qvmmx = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for ebk__lsee in range(len(recv_counts)):
                    recv_counts_nulls[ebk__lsee] = recv_counts[ebk__lsee
                        ] + 7 >> 3
                ghm__yml = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            halr__nqbpb = np.empty(gmqc__fcqfo + 1, np.uint32)
            mrhqr__cwb = bodo.gatherv(zctn__rtkn, allgather, warn_if_rep, root)
            xzvvf__puk = np.empty(gmqc__fcqfo + 7 >> 3, np.uint8)
            c_gatherv(tgz__tmyf.ctypes, np.int32(zuhn__rvo), halr__nqbpb.
                ctypes, recv_counts.ctypes, ncb__qvmmx.ctypes, rbpch__aje,
                allgather, np.int32(root))
            c_gatherv(ilocp__zmb.ctypes, np.int32(vdi__nnqv),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, ghm__yml.
                ctypes, izwun__pbv, allgather, np.int32(root))
            dummy_use(data)
            uqh__uio = np.empty(gmqc__fcqfo + 1, np.uint64)
            convert_len_arr_to_offset(halr__nqbpb.ctypes, uqh__uio.ctypes,
                gmqc__fcqfo)
            copy_gathered_null_bytes(xzvvf__puk.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                gmqc__fcqfo, mrhqr__cwb, uqh__uio, xzvvf__puk)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        zxbrz__yxd = data.names
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            odxl__wnzj = bodo.libs.struct_arr_ext.get_data(data)
            yze__icsb = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            vks__fnwbd = bodo.gatherv(odxl__wnzj, allgather=allgather, root
                =root)
            rank = bodo.libs.distributed_api.get_rank()
            zuhn__rvo = len(data)
            vdi__nnqv = zuhn__rvo + 7 >> 3
            recv_counts = gather_scalar(np.int32(zuhn__rvo), allgather,
                root=root)
            gmqc__fcqfo = recv_counts.sum()
            erktz__eqnyk = np.empty(gmqc__fcqfo + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            ghm__yml = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                ghm__yml = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(yze__icsb.ctypes, np.int32(vdi__nnqv), tmp_null_bytes
                .ctypes, recv_counts_nulls.ctypes, ghm__yml.ctypes,
                izwun__pbv, allgather, np.int32(root))
            copy_gathered_null_bytes(erktz__eqnyk.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(vks__fnwbd,
                erktz__eqnyk, zxbrz__yxd)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            zkwpr__vgtuv = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.binary_arr_ext.init_binary_arr(zkwpr__vgtuv)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            zkwpr__vgtuv = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(zkwpr__vgtuv)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            zkwpr__vgtuv = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.map_arr_ext.init_map_arr(zkwpr__vgtuv)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            zkwpr__vgtuv = bodo.gatherv(data.data, allgather, warn_if_rep, root
                )
            ygee__vtmhv = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            cty__dle = bodo.gatherv(data.indptr, allgather, warn_if_rep, root)
            rtt__cxiaq = gather_scalar(data.shape[0], allgather, root=root)
            jlme__tkfk = rtt__cxiaq.sum()
            mzpgr__avslh = bodo.libs.distributed_api.dist_reduce(data.shape
                [1], np.int32(Reduce_Type.Max.value))
            sfftz__uxc = np.empty(jlme__tkfk + 1, np.int64)
            ygee__vtmhv = ygee__vtmhv.astype(np.int64)
            sfftz__uxc[0] = 0
            fucd__lxys = 1
            ubogc__urfp = 0
            for kbjy__mpik in rtt__cxiaq:
                for upnuk__hxdii in range(kbjy__mpik):
                    evqyx__pwe = cty__dle[ubogc__urfp + 1] - cty__dle[
                        ubogc__urfp]
                    sfftz__uxc[fucd__lxys] = sfftz__uxc[fucd__lxys - 1
                        ] + evqyx__pwe
                    fucd__lxys += 1
                    ubogc__urfp += 1
                ubogc__urfp += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(zkwpr__vgtuv,
                ygee__vtmhv, sfftz__uxc, (jlme__tkfk, mzpgr__avslh))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        rzes__wmeh = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        rzes__wmeh += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        cycm__rujg = {}
        exec(rzes__wmeh, {'bodo': bodo}, cycm__rujg)
        lodvx__hvx = cycm__rujg['impl_tuple']
        return lodvx__hvx
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as auw__pnqm:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        rzes__wmeh = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        fnktz__etfd = ', '.join([f"'{joe__lbziz}'" for joe__lbziz in data.
            names])
        bjg__xso = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        rzes__wmeh += f"""  return bodosql.context_ext.init_sql_context(({fnktz__etfd}, ), ({bjg__xso}, ), data.catalog)
"""
        cycm__rujg = {}
        exec(rzes__wmeh, {'bodo': bodo, 'bodosql': bodosql}, cycm__rujg)
        yqao__zsz = cycm__rujg['impl_bodosql_context']
        return yqao__zsz
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as auw__pnqm:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        rzes__wmeh = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        rzes__wmeh += f'  return data\n'
        cycm__rujg = {}
        exec(rzes__wmeh, {}, cycm__rujg)
        cml__neqnj = cycm__rujg['impl_table_path']
        return cml__neqnj
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    rzes__wmeh = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    rzes__wmeh += '    if random:\n'
    rzes__wmeh += '        if random_seed is None:\n'
    rzes__wmeh += '            random = 1\n'
    rzes__wmeh += '        else:\n'
    rzes__wmeh += '            random = 2\n'
    rzes__wmeh += '    if random_seed is None:\n'
    rzes__wmeh += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        fudmy__cibr = data
        mzpgr__avslh = len(fudmy__cibr.columns)
        for i in range(mzpgr__avslh):
            rzes__wmeh += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        rzes__wmeh += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        lsoln__tpo = ', '.join(f'data_{i}' for i in range(mzpgr__avslh))
        rzes__wmeh += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(gsayb__qav) for
            gsayb__qav in range(mzpgr__avslh))))
        rzes__wmeh += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        rzes__wmeh += '    if dests is None:\n'
        rzes__wmeh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        rzes__wmeh += '    else:\n'
        rzes__wmeh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for pjmka__aoivl in range(mzpgr__avslh):
            rzes__wmeh += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(pjmka__aoivl))
        rzes__wmeh += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(mzpgr__avslh))
        rzes__wmeh += '    delete_table(out_table)\n'
        rzes__wmeh += '    if parallel:\n'
        rzes__wmeh += '        delete_table(table_total)\n'
        lsoln__tpo = ', '.join('out_arr_{}'.format(i) for i in range(
            mzpgr__avslh))
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        rzes__wmeh += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(lsoln__tpo, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        rzes__wmeh += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        rzes__wmeh += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        rzes__wmeh += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        rzes__wmeh += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        rzes__wmeh += '    if dests is None:\n'
        rzes__wmeh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        rzes__wmeh += '    else:\n'
        rzes__wmeh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        rzes__wmeh += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        rzes__wmeh += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        rzes__wmeh += '    delete_table(out_table)\n'
        rzes__wmeh += '    if parallel:\n'
        rzes__wmeh += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        rzes__wmeh += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        rzes__wmeh += '    if not parallel:\n'
        rzes__wmeh += '        return data\n'
        rzes__wmeh += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        rzes__wmeh += '    if dests is None:\n'
        rzes__wmeh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        rzes__wmeh += '    elif bodo.get_rank() not in dests:\n'
        rzes__wmeh += '        dim0_local_size = 0\n'
        rzes__wmeh += '    else:\n'
        rzes__wmeh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        rzes__wmeh += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        rzes__wmeh += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        rzes__wmeh += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        rzes__wmeh += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        rzes__wmeh += '    if dests is None:\n'
        rzes__wmeh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        rzes__wmeh += '    else:\n'
        rzes__wmeh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        rzes__wmeh += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        rzes__wmeh += '    delete_table(out_table)\n'
        rzes__wmeh += '    if parallel:\n'
        rzes__wmeh += '        delete_table(table_total)\n'
        rzes__wmeh += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    cycm__rujg = {}
    ait__gtho = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.array.
        array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ait__gtho.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(fudmy__cibr.columns)})
    exec(rzes__wmeh, ait__gtho, cycm__rujg)
    impl = cycm__rujg['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    rzes__wmeh = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        rzes__wmeh += '    if seed is None:\n'
        rzes__wmeh += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        rzes__wmeh += '    np.random.seed(seed)\n'
        rzes__wmeh += '    if not parallel:\n'
        rzes__wmeh += '        data = data.copy()\n'
        rzes__wmeh += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            rzes__wmeh += '        data = data[:n_samples]\n'
        rzes__wmeh += '        return data\n'
        rzes__wmeh += '    else:\n'
        rzes__wmeh += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        rzes__wmeh += '        permutation = np.arange(dim0_global_size)\n'
        rzes__wmeh += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            rzes__wmeh += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            rzes__wmeh += '        n_samples = dim0_global_size\n'
        rzes__wmeh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        rzes__wmeh += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        rzes__wmeh += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        rzes__wmeh += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        rzes__wmeh += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        rzes__wmeh += '        return output\n'
    else:
        rzes__wmeh += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            rzes__wmeh += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            rzes__wmeh += '    output = output[:local_n_samples]\n'
        rzes__wmeh += '    return output\n'
    cycm__rujg = {}
    exec(rzes__wmeh, {'np': np, 'bodo': bodo}, cycm__rujg)
    impl = cycm__rujg['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    mfszy__kjlmi = np.empty(sendcounts_nulls.sum(), np.uint8)
    edqo__hnuh = 0
    tmb__vkw = 0
    for ndc__frjyn in range(len(sendcounts)):
        tvc__rnc = sendcounts[ndc__frjyn]
        vdi__nnqv = sendcounts_nulls[ndc__frjyn]
        tnavz__ygvz = mfszy__kjlmi[edqo__hnuh:edqo__hnuh + vdi__nnqv]
        for esc__mmfz in range(tvc__rnc):
            set_bit_to_arr(tnavz__ygvz, esc__mmfz, get_bit_bitmap(
                null_bitmap_ptr, tmb__vkw))
            tmb__vkw += 1
        edqo__hnuh += vdi__nnqv
    return mfszy__kjlmi


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    ivmt__iqut = MPI.COMM_WORLD
    data = ivmt__iqut.bcast(data, root)
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
    poho__kxmqk = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    uabs__kdzcw = (0,) * poho__kxmqk

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        fsgh__hkjw = np.ascontiguousarray(data)
        lehnn__qcyjy = data.ctypes
        jjow__boxd = uabs__kdzcw
        if rank == MPI_ROOT:
            jjow__boxd = fsgh__hkjw.shape
        jjow__boxd = bcast_tuple(jjow__boxd)
        pie__bqyzq = get_tuple_prod(jjow__boxd[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            jjow__boxd[0])
        send_counts *= pie__bqyzq
        zuhn__rvo = send_counts[rank]
        ppi__xdxr = np.empty(zuhn__rvo, dtype)
        ncb__qvmmx = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(lehnn__qcyjy, send_counts.ctypes, ncb__qvmmx.ctypes,
            ppi__xdxr.ctypes, np.int32(zuhn__rvo), np.int32(typ_val))
        return ppi__xdxr.reshape((-1,) + jjow__boxd[1:])
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
        exjv__wgiu = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], exjv__wgiu)
    if isinstance(dtype, FloatingArrayType):
        exjv__wgiu = 'Float{}'.format(dtype.dtype.bitwidth)
        return pd.array([3.0], exjv__wgiu)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        joe__lbziz = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=joe__lbziz)
        sgo__obz = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(sgo__obz)
        return pd.Index(arr, name=joe__lbziz)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        joe__lbziz = _get_name_value_for_type(dtype.name_typ)
        zxbrz__yxd = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        ldsf__zsir = tuple(get_value_for_type(t) for t in dtype.array_types)
        ldsf__zsir = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in ldsf__zsir)
        val = pd.MultiIndex.from_arrays(ldsf__zsir, names=zxbrz__yxd)
        val.name = joe__lbziz
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        joe__lbziz = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=joe__lbziz)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ldsf__zsir = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({joe__lbziz: arr for joe__lbziz, arr in zip(
            dtype.columns, ldsf__zsir)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        sgo__obz = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(sgo__obz[0], sgo__obz[0])])
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
        rbpch__aje = np.int32(numba_to_c_type(types.int32))
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            tmpa__tvv = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            tmpa__tvv = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        rzes__wmeh = f"""def impl(
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
            recv_arr = {tmpa__tvv}(n_loc, n_loc_char)

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
        cycm__rujg = dict()
        exec(rzes__wmeh, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            rbpch__aje, 'char_typ_enum': izwun__pbv, 'decode_if_dict_array':
            decode_if_dict_array}, cycm__rujg)
        impl = cycm__rujg['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        rbpch__aje = np.int32(numba_to_c_type(types.int32))
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            roz__kqhuh = bodo.libs.array_item_arr_ext.get_offsets(data)
            gazsm__xzusl = bodo.libs.array_item_arr_ext.get_data(data)
            gazsm__xzusl = gazsm__xzusl[:roz__kqhuh[-1]]
            pzx__ozyyk = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            ile__hvoj = bcast_scalar(len(data))
            yfc__svb = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                yfc__svb[i] = roz__kqhuh[i + 1] - roz__kqhuh[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                ile__hvoj)
            ncb__qvmmx = bodo.ir.join.calc_disp(send_counts)
            jjmdn__wtska = np.empty(n_pes, np.int32)
            if rank == 0:
                urj__jqyr = 0
                for i in range(n_pes):
                    avo__kyybk = 0
                    for upnuk__hxdii in range(send_counts[i]):
                        avo__kyybk += yfc__svb[urj__jqyr]
                        urj__jqyr += 1
                    jjmdn__wtska[i] = avo__kyybk
            bcast(jjmdn__wtska)
            wiv__ltqmp = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                wiv__ltqmp[i] = send_counts[i] + 7 >> 3
            ghm__yml = bodo.ir.join.calc_disp(wiv__ltqmp)
            zuhn__rvo = send_counts[rank]
            bcyjp__yjf = np.empty(zuhn__rvo + 1, np_offset_type)
            alip__wpqnn = bodo.libs.distributed_api.scatterv_impl(gazsm__xzusl,
                jjmdn__wtska)
            hcexp__ttzjr = zuhn__rvo + 7 >> 3
            hcnpt__swig = np.empty(hcexp__ttzjr, np.uint8)
            qsegs__mmuqp = np.empty(zuhn__rvo, np.uint32)
            c_scatterv(yfc__svb.ctypes, send_counts.ctypes, ncb__qvmmx.
                ctypes, qsegs__mmuqp.ctypes, np.int32(zuhn__rvo), rbpch__aje)
            convert_len_arr_to_offset(qsegs__mmuqp.ctypes, bcyjp__yjf.
                ctypes, zuhn__rvo)
            wnkjq__bxi = get_scatter_null_bytes_buff(pzx__ozyyk.ctypes,
                send_counts, wiv__ltqmp)
            c_scatterv(wnkjq__bxi.ctypes, wiv__ltqmp.ctypes, ghm__yml.
                ctypes, hcnpt__swig.ctypes, np.int32(hcexp__ttzjr), izwun__pbv)
            return bodo.libs.array_item_arr_ext.init_array_item_array(zuhn__rvo
                , alip__wpqnn, bcyjp__yjf, hcnpt__swig)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or data in (boolean_array, datetime_date_array_type):
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            gwohr__pxkrg = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, FloatingArrayType):
            gwohr__pxkrg = bodo.libs.float_arr_ext.init_float_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            gwohr__pxkrg = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            gwohr__pxkrg = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            gwohr__pxkrg = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            fsgh__hkjw = data._data
            yze__icsb = data._null_bitmap
            ttre__kfino = len(fsgh__hkjw)
            xwbb__ogim = _scatterv_np(fsgh__hkjw, send_counts)
            ile__hvoj = bcast_scalar(ttre__kfino)
            bwdr__rpvay = len(xwbb__ogim) + 7 >> 3
            byx__shwvs = np.empty(bwdr__rpvay, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                ile__hvoj)
            wiv__ltqmp = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                wiv__ltqmp[i] = send_counts[i] + 7 >> 3
            ghm__yml = bodo.ir.join.calc_disp(wiv__ltqmp)
            wnkjq__bxi = get_scatter_null_bytes_buff(yze__icsb.ctypes,
                send_counts, wiv__ltqmp)
            c_scatterv(wnkjq__bxi.ctypes, wiv__ltqmp.ctypes, ghm__yml.
                ctypes, byx__shwvs.ctypes, np.int32(bwdr__rpvay), izwun__pbv)
            return gwohr__pxkrg(xwbb__ogim, byx__shwvs)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            ekskz__ikc = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            tlrxb__arwe = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(ekskz__ikc,
                tlrxb__arwe)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            gux__mzqm = data._start
            rzwp__fzxno = data._stop
            jwdb__bew = data._step
            joe__lbziz = data._name
            joe__lbziz = bcast_scalar(joe__lbziz)
            gux__mzqm = bcast_scalar(gux__mzqm)
            rzwp__fzxno = bcast_scalar(rzwp__fzxno)
            jwdb__bew = bcast_scalar(jwdb__bew)
            kvv__fojm = bodo.libs.array_kernels.calc_nitems(gux__mzqm,
                rzwp__fzxno, jwdb__bew)
            chunk_start = bodo.libs.distributed_api.get_start(kvv__fojm,
                n_pes, rank)
            wlae__zjgiy = bodo.libs.distributed_api.get_node_portion(kvv__fojm,
                n_pes, rank)
            gou__tfgnk = gux__mzqm + jwdb__bew * chunk_start
            mizk__uhahg = gux__mzqm + jwdb__bew * (chunk_start + wlae__zjgiy)
            mizk__uhahg = min(mizk__uhahg, rzwp__fzxno)
            return bodo.hiframes.pd_index_ext.init_range_index(gou__tfgnk,
                mizk__uhahg, jwdb__bew, joe__lbziz)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        tfhh__uodm = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            fsgh__hkjw = data._data
            joe__lbziz = data._name
            joe__lbziz = bcast_scalar(joe__lbziz)
            arr = bodo.libs.distributed_api.scatterv_impl(fsgh__hkjw,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                joe__lbziz, tfhh__uodm)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            fsgh__hkjw = data._data
            joe__lbziz = data._name
            joe__lbziz = bcast_scalar(joe__lbziz)
            arr = bodo.libs.distributed_api.scatterv_impl(fsgh__hkjw,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, joe__lbziz)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            zkwpr__vgtuv = bodo.libs.distributed_api.scatterv_impl(data.
                _data, send_counts)
            joe__lbziz = bcast_scalar(data._name)
            zxbrz__yxd = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                zkwpr__vgtuv, zxbrz__yxd, joe__lbziz)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            joe__lbziz = bodo.hiframes.pd_series_ext.get_series_name(data)
            acwu__kgh = bcast_scalar(joe__lbziz)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            zef__dfw = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                zef__dfw, acwu__kgh)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        mzpgr__avslh = len(data.columns)
        amey__rxatc = ColNamesMetaType(data.columns)
        rzes__wmeh = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        if data.is_table_format:
            rzes__wmeh += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            rzes__wmeh += """  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)
"""
            lsoln__tpo = 'g_table'
        else:
            for i in range(mzpgr__avslh):
                rzes__wmeh += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                rzes__wmeh += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            lsoln__tpo = ', '.join(f'g_data_{i}' for i in range(mzpgr__avslh))
        rzes__wmeh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        rzes__wmeh += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        rzes__wmeh += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({lsoln__tpo},), g_index, __col_name_meta_scaterv_impl)
"""
        cycm__rujg = {}
        exec(rzes__wmeh, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            amey__rxatc}, cycm__rujg)
        gdrd__rxz = cycm__rujg['impl_df']
        return gdrd__rxz
    if isinstance(data, bodo.TableType):
        rzes__wmeh = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        rzes__wmeh += '  T = data\n'
        rzes__wmeh += '  T2 = init_table(T, False)\n'
        rzes__wmeh += '  l = 0\n'
        ait__gtho = {}
        for hsx__iqyy in data.type_to_blk.values():
            ait__gtho[f'arr_inds_{hsx__iqyy}'] = np.array(data.
                block_to_arr_ind[hsx__iqyy], dtype=np.int64)
            rzes__wmeh += (
                f'  arr_list_{hsx__iqyy} = get_table_block(T, {hsx__iqyy})\n')
            rzes__wmeh += f"""  out_arr_list_{hsx__iqyy} = alloc_list_like(arr_list_{hsx__iqyy}, len(arr_list_{hsx__iqyy}), False)
"""
            rzes__wmeh += f'  for i in range(len(arr_list_{hsx__iqyy})):\n'
            rzes__wmeh += (
                f'    arr_ind_{hsx__iqyy} = arr_inds_{hsx__iqyy}[i]\n')
            rzes__wmeh += f"""    ensure_column_unboxed(T, arr_list_{hsx__iqyy}, i, arr_ind_{hsx__iqyy})
"""
            rzes__wmeh += f"""    out_arr_{hsx__iqyy} = bodo.libs.distributed_api.scatterv_impl(arr_list_{hsx__iqyy}[i], send_counts)
"""
            rzes__wmeh += (
                f'    out_arr_list_{hsx__iqyy}[i] = out_arr_{hsx__iqyy}\n')
            rzes__wmeh += f'    l = len(out_arr_{hsx__iqyy})\n'
            rzes__wmeh += (
                f'  T2 = set_table_block(T2, out_arr_list_{hsx__iqyy}, {hsx__iqyy})\n'
                )
        rzes__wmeh += f'  T2 = set_table_len(T2, l)\n'
        rzes__wmeh += f'  return T2\n'
        ait__gtho.update({'bodo': bodo, 'init_table': bodo.hiframes.table.
            init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        cycm__rujg = {}
        exec(rzes__wmeh, ait__gtho, cycm__rujg)
        return cycm__rujg['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                gzg__hnta = data._data
                bodo.libs.distributed_api.bcast_scalar(len(gzg__hnta))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(gzg__hnta)))
            else:
                law__lxnv = bodo.libs.distributed_api.bcast_scalar(0)
                kjauj__hlsn = bodo.libs.distributed_api.bcast_scalar(0)
                gzg__hnta = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    law__lxnv, kjauj__hlsn)
            bodo.libs.distributed_api.bcast(gzg__hnta)
            qkmxm__tdytv = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(gzg__hnta,
                qkmxm__tdytv, True, data._has_deduped_local_dictionary)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            jzak__aedzt = bodo.libs.distributed_api.scatterv_impl(data.
                codes, send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                jzak__aedzt, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        rzes__wmeh = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        rzes__wmeh += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        cycm__rujg = {}
        exec(rzes__wmeh, {'bodo': bodo}, cycm__rujg)
        lodvx__hvx = cycm__rujg['impl_tuple']
        return lodvx__hvx
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
        rfn__lveiv = np.int32(numba_to_c_type(offset_type))
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            zuhn__rvo = len(data)
            paj__pul = num_total_chars(data)
            assert zuhn__rvo < INT_MAX
            assert paj__pul < INT_MAX
            kgtiq__hai = get_offset_ptr(data)
            lehnn__qcyjy = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            vdi__nnqv = zuhn__rvo + 7 >> 3
            c_bcast(kgtiq__hai, np.int32(zuhn__rvo + 1), rfn__lveiv, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(lehnn__qcyjy, np.int32(paj__pul), izwun__pbv, np.array(
                [-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(vdi__nnqv), izwun__pbv, np.
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
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                clf__vgph = 0
                bmvwy__artqm = np.empty(0, np.uint8).ctypes
            else:
                bmvwy__artqm, clf__vgph = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            clf__vgph = bodo.libs.distributed_api.bcast_scalar(clf__vgph, root)
            if rank != root:
                fpaw__djsxl = np.empty(clf__vgph + 1, np.uint8)
                fpaw__djsxl[clf__vgph] = 0
                bmvwy__artqm = fpaw__djsxl.ctypes
            c_bcast(bmvwy__artqm, np.int32(clf__vgph), izwun__pbv, np.array
                ([-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(bmvwy__artqm, clf__vgph)
        return impl_str
    typ_val = numba_to_c_type(val)
    rzes__wmeh = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    cycm__rujg = {}
    exec(rzes__wmeh, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, cycm__rujg)
    vyvft__snley = cycm__rujg['bcast_scalar_impl']
    return vyvft__snley


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple
        ), 'Internal Error: Argument to bcast tuple must be of type tuple'
    bro__ycs = len(val)
    rzes__wmeh = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    rzes__wmeh += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(bro__ycs)), 
        ',' if bro__ycs else '')
    cycm__rujg = {}
    exec(rzes__wmeh, {'bcast_scalar': bcast_scalar}, cycm__rujg)
    qlnfu__omus = cycm__rujg['bcast_tuple_impl']
    return qlnfu__omus


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            zuhn__rvo = bcast_scalar(len(arr), root)
            ynajy__zrh = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(zuhn__rvo, ynajy__zrh)
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
            gou__tfgnk = max(arr_start, slice_index.start) - arr_start
            mizk__uhahg = max(slice_index.stop - arr_start, 0)
            return slice(gou__tfgnk, mizk__uhahg)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            gux__mzqm = slice_index.start
            jwdb__bew = slice_index.step
            frvot__uby = 0 if jwdb__bew == 1 or gux__mzqm > arr_start else abs(
                jwdb__bew - arr_start % jwdb__bew) % jwdb__bew
            gou__tfgnk = max(arr_start, slice_index.start
                ) - arr_start + frvot__uby
            mizk__uhahg = max(slice_index.stop - arr_start, 0)
            return slice(gou__tfgnk, mizk__uhahg, jwdb__bew)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        zjw__loxuf = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[zjw__loxuf])
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
        kbbjd__xgff = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        izwun__pbv = np.int32(numba_to_c_type(types.uint8))
        ztvif__vfgjp = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            jay__naj = np.int32(10)
            tag = np.int32(11)
            gqc__dfnof = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                zctn__rtkn = arr._data
                najfr__lpx = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    zctn__rtkn, ind)
                lqmd__nnbhe = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    zctn__rtkn, ind + 1)
                length = lqmd__nnbhe - najfr__lpx
                qehns__xiryg = zctn__rtkn[ind]
                gqc__dfnof[0] = length
                isend(gqc__dfnof, np.int32(1), root, jay__naj, True)
                isend(qehns__xiryg, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                ztvif__vfgjp, kbbjd__xgff, 0, 1)
            law__lxnv = 0
            if rank == root:
                law__lxnv = recv(np.int64, ANY_SOURCE, jay__naj)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    ztvif__vfgjp, kbbjd__xgff, law__lxnv, 1)
                lehnn__qcyjy = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(lehnn__qcyjy, np.int32(law__lxnv), izwun__pbv,
                    ANY_SOURCE, tag)
            dummy_use(gqc__dfnof)
            law__lxnv = bcast_scalar(law__lxnv)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    ztvif__vfgjp, kbbjd__xgff, law__lxnv, 1)
            lehnn__qcyjy = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(lehnn__qcyjy, np.int32(law__lxnv), izwun__pbv, np.array
                ([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, law__lxnv)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        tuion__tvo = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, tuion__tvo)
            if arr_start <= ind < arr_start + len(arr):
                jzak__aedzt = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = jzak__aedzt[ind - arr_start]
                send_arr = np.full(1, data, tuion__tvo)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = tuion__tvo(-1)
            if rank == root:
                val = recv(tuion__tvo, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            huuol__ntymu = arr.dtype.categories[max(val, 0)]
            return huuol__ntymu
        return cat_getitem_impl
    if isinstance(arr, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        abdqy__qkufi = arr.tz

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
                abdqy__qkufi)
        return tz_aware_getitem_impl
    uumg__sma = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, uumg__sma)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, uumg__sma)[0]
        if rank == root:
            val = recv(uumg__sma, ANY_SOURCE, tag)
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
        agbr__zdwbw = np.empty(n_pes, np.int64)
        tyc__gaji = np.empty(n_pes, np.int8)
        val = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        nvkjr__ktxgx = 1
        if len(A) != 0:
            val = A[-1]
            nvkjr__ktxgx = 0
        allgather(agbr__zdwbw, np.int64(val))
        allgather(tyc__gaji, nvkjr__ktxgx)
        for i, nvkjr__ktxgx in enumerate(tyc__gaji):
            if nvkjr__ktxgx and i != 0:
                agbr__zdwbw[i] = agbr__zdwbw[i - 1]
        return agbr__zdwbw
    return impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    fwtm__uqsi = get_type_enum(out_data)
    assert typ_enum == fwtm__uqsi
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
    rzes__wmeh = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        rzes__wmeh += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    rzes__wmeh += '  return\n'
    cycm__rujg = {}
    exec(rzes__wmeh, {'alltoallv': alltoallv}, cycm__rujg)
    hjrhv__erhh = cycm__rujg['f']
    return hjrhv__erhh


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    gux__mzqm = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return gux__mzqm, count


@numba.njit
def get_start(total_size, pes, rank):
    hpn__cfpj = total_size % pes
    lycq__tigvb = (total_size - hpn__cfpj) // pes
    return rank * lycq__tigvb + min(rank, hpn__cfpj)


@numba.njit
def get_end(total_size, pes, rank):
    hpn__cfpj = total_size % pes
    lycq__tigvb = (total_size - hpn__cfpj) // pes
    return (rank + 1) * lycq__tigvb + min(rank + 1, hpn__cfpj)


@numba.njit
def get_node_portion(total_size, pes, rank):
    hpn__cfpj = total_size % pes
    lycq__tigvb = (total_size - hpn__cfpj) // pes
    if rank < hpn__cfpj:
        return lycq__tigvb + 1
    else:
        return lycq__tigvb


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    ozeuy__sdn = in_arr.dtype(0)
    lygwg__lsb = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        avo__kyybk = ozeuy__sdn
        for nlue__tpx in np.nditer(in_arr):
            avo__kyybk += nlue__tpx.item()
        rqpfm__oia = dist_exscan(avo__kyybk, lygwg__lsb)
        for i in range(in_arr.size):
            rqpfm__oia += in_arr[i]
            out_arr[i] = rqpfm__oia
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    jsly__yzrw = in_arr.dtype(1)
    lygwg__lsb = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        avo__kyybk = jsly__yzrw
        for nlue__tpx in np.nditer(in_arr):
            avo__kyybk *= nlue__tpx.item()
        rqpfm__oia = dist_exscan(avo__kyybk, lygwg__lsb)
        if get_rank() == 0:
            rqpfm__oia = jsly__yzrw
        for i in range(in_arr.size):
            rqpfm__oia *= in_arr[i]
            out_arr[i] = rqpfm__oia
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        jsly__yzrw = np.finfo(in_arr.dtype(1).dtype).max
    else:
        jsly__yzrw = np.iinfo(in_arr.dtype(1).dtype).max
    lygwg__lsb = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        avo__kyybk = jsly__yzrw
        for nlue__tpx in np.nditer(in_arr):
            avo__kyybk = min(avo__kyybk, nlue__tpx.item())
        rqpfm__oia = dist_exscan(avo__kyybk, lygwg__lsb)
        if get_rank() == 0:
            rqpfm__oia = jsly__yzrw
        for i in range(in_arr.size):
            rqpfm__oia = min(rqpfm__oia, in_arr[i])
            out_arr[i] = rqpfm__oia
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        jsly__yzrw = np.finfo(in_arr.dtype(1).dtype).min
    else:
        jsly__yzrw = np.iinfo(in_arr.dtype(1).dtype).min
    jsly__yzrw = in_arr.dtype(1)
    lygwg__lsb = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        avo__kyybk = jsly__yzrw
        for nlue__tpx in np.nditer(in_arr):
            avo__kyybk = max(avo__kyybk, nlue__tpx.item())
        rqpfm__oia = dist_exscan(avo__kyybk, lygwg__lsb)
        if get_rank() == 0:
            rqpfm__oia = jsly__yzrw
        for i in range(in_arr.size):
            rqpfm__oia = max(rqpfm__oia, in_arr[i])
            out_arr[i] = rqpfm__oia
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    bbnf__kiq = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), bbnf__kiq)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    vgsq__ppcx = args[0]
    if equiv_set.has_shape(vgsq__ppcx):
        return ArrayAnalysis.AnalyzeResult(shape=vgsq__ppcx, pre=[])
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
    gcstp__fru = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for 
        i, pwrlq__gbax in enumerate(args) if is_array_typ(pwrlq__gbax) or
        isinstance(pwrlq__gbax, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    rzes__wmeh = f"""def impl(*args):
    if {gcstp__fru} or bodo.get_rank() == 0:
        print(*args)"""
    cycm__rujg = {}
    exec(rzes__wmeh, globals(), cycm__rujg)
    impl = cycm__rujg['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        drak__yfr = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        rzes__wmeh = 'def f(req, cond=True):\n'
        rzes__wmeh += f'  return {drak__yfr}\n'
        cycm__rujg = {}
        exec(rzes__wmeh, {'_wait': _wait}, cycm__rujg)
        impl = cycm__rujg['f']
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
        hpn__cfpj = 1
        for a in t:
            hpn__cfpj *= a
        return hpn__cfpj
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    cqfbw__omc = np.ascontiguousarray(in_arr)
    higz__lvnr = get_tuple_prod(cqfbw__omc.shape[1:])
    diz__pdu = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        xqh__qxjpf = np.array(dest_ranks, dtype=np.int32)
    else:
        xqh__qxjpf = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, cqfbw__omc.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * diz__pdu, dtype_size * higz__lvnr, len(
        xqh__qxjpf), xqh__qxjpf.ctypes)
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
    mmufq__hld = np.ascontiguousarray(rhs)
    uoa__gtldh = get_tuple_prod(mmufq__hld.shape[1:])
    ozbe__fkwq = dtype_size * uoa__gtldh
    permutation_array_index(lhs.ctypes, lhs_len, ozbe__fkwq, mmufq__hld.
        ctypes, mmufq__hld.shape[0], p.ctypes, p_len, n_samples)
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
        rzes__wmeh = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        cycm__rujg = {}
        exec(rzes__wmeh, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, cycm__rujg)
        vyvft__snley = cycm__rujg['bcast_scalar_impl']
        return vyvft__snley
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        mzpgr__avslh = len(data.columns)
        lsoln__tpo = ', '.join('g_data_{}'.format(i) for i in range(
            mzpgr__avslh))
        fewfb__wce = ColNamesMetaType(data.columns)
        rzes__wmeh = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(mzpgr__avslh):
            rzes__wmeh += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            rzes__wmeh += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        rzes__wmeh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        rzes__wmeh += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        rzes__wmeh += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(lsoln__tpo))
        cycm__rujg = {}
        exec(rzes__wmeh, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            fewfb__wce}, cycm__rujg)
        gdrd__rxz = cycm__rujg['impl_df']
        return gdrd__rxz
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            gux__mzqm = data._start
            rzwp__fzxno = data._stop
            jwdb__bew = data._step
            joe__lbziz = data._name
            joe__lbziz = bcast_scalar(joe__lbziz, root)
            gux__mzqm = bcast_scalar(gux__mzqm, root)
            rzwp__fzxno = bcast_scalar(rzwp__fzxno, root)
            jwdb__bew = bcast_scalar(jwdb__bew, root)
            kvv__fojm = bodo.libs.array_kernels.calc_nitems(gux__mzqm,
                rzwp__fzxno, jwdb__bew)
            chunk_start = bodo.libs.distributed_api.get_start(kvv__fojm,
                n_pes, rank)
            wlae__zjgiy = bodo.libs.distributed_api.get_node_portion(kvv__fojm,
                n_pes, rank)
            gou__tfgnk = gux__mzqm + jwdb__bew * chunk_start
            mizk__uhahg = gux__mzqm + jwdb__bew * (chunk_start + wlae__zjgiy)
            mizk__uhahg = min(mizk__uhahg, rzwp__fzxno)
            return bodo.hiframes.pd_index_ext.init_range_index(gou__tfgnk,
                mizk__uhahg, jwdb__bew, joe__lbziz)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            fsgh__hkjw = data._data
            joe__lbziz = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(fsgh__hkjw,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, joe__lbziz)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            joe__lbziz = bodo.hiframes.pd_series_ext.get_series_name(data)
            acwu__kgh = bodo.libs.distributed_api.bcast_comm_impl(joe__lbziz,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            zef__dfw = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                zef__dfw, acwu__kgh)
        return impl_series
    if isinstance(data, types.BaseTuple):
        rzes__wmeh = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        rzes__wmeh += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        cycm__rujg = {}
        exec(rzes__wmeh, {'bcast_comm_impl': bcast_comm_impl}, cycm__rujg)
        lodvx__hvx = cycm__rujg['impl_tuple']
        return lodvx__hvx
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    poho__kxmqk = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    uabs__kdzcw = (0,) * poho__kxmqk

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        fsgh__hkjw = np.ascontiguousarray(data)
        lehnn__qcyjy = data.ctypes
        jjow__boxd = uabs__kdzcw
        if rank == root:
            jjow__boxd = fsgh__hkjw.shape
        jjow__boxd = bcast_tuple(jjow__boxd, root)
        pie__bqyzq = get_tuple_prod(jjow__boxd[1:])
        send_counts = jjow__boxd[0] * pie__bqyzq
        ppi__xdxr = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(lehnn__qcyjy, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(ppi__xdxr.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return ppi__xdxr.reshape((-1,) + jjow__boxd[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        ivmt__iqut = MPI.COMM_WORLD
        dposx__bnlni = MPI.Get_processor_name()
        kkun__maxox = ivmt__iqut.allgather(dposx__bnlni)
        node_ranks = defaultdict(list)
        for i, kpm__pfk in enumerate(kkun__maxox):
            node_ranks[kpm__pfk].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    ivmt__iqut = MPI.COMM_WORLD
    qmt__qzeys = ivmt__iqut.Get_group()
    otmo__cfuaz = qmt__qzeys.Incl(comm_ranks)
    hhk__vwcu = ivmt__iqut.Create_group(otmo__cfuaz)
    return hhk__vwcu


def get_nodes_first_ranks():
    tmxfz__rwbqw = get_host_ranks()
    return np.array([lysns__szg[0] for lysns__szg in tmxfz__rwbqw.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
