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
    ufx__icvlc = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, ufx__icvlc, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    ufx__icvlc = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, ufx__icvlc, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            ufx__icvlc = get_type_enum(arr)
            return _isend(arr.ctypes, size, ufx__icvlc, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        ufx__icvlc = np.int32(numba_to_c_type(arr.dtype))
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            phou__jnzsd = size + 7 >> 3
            aek__xqneb = _isend(arr._data.ctypes, size, ufx__icvlc, pe, tag,
                cond)
            scsfm__per = _isend(arr._null_bitmap.ctypes, phou__jnzsd,
                sab__rlm, pe, tag, cond)
            return aek__xqneb, scsfm__per
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            nri__hdtfi = arr._data
            ufx__icvlc = get_type_enum(nri__hdtfi)
            return _isend(nri__hdtfi.ctypes, size, ufx__icvlc, pe, tag, cond)
        return impl_tz_arr
    if is_str_arr_type(arr) or arr == binary_array_type:
        ooew__diar = np.int32(numba_to_c_type(offset_type))
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            epb__tiws = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(epb__tiws, pe, tag - 1)
            phou__jnzsd = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                ooew__diar, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), epb__tiws,
                sab__rlm, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                phou__jnzsd, sab__rlm, pe, tag)
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
            ufx__icvlc = get_type_enum(arr)
            return _irecv(arr.ctypes, size, ufx__icvlc, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        ufx__icvlc = np.int32(numba_to_c_type(arr.dtype))
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            phou__jnzsd = size + 7 >> 3
            aek__xqneb = _irecv(arr._data.ctypes, size, ufx__icvlc, pe, tag,
                cond)
            scsfm__per = _irecv(arr._null_bitmap.ctypes, phou__jnzsd,
                sab__rlm, pe, tag, cond)
            return aek__xqneb, scsfm__per
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            nri__hdtfi = arr._data
            ufx__icvlc = get_type_enum(nri__hdtfi)
            return _irecv(nri__hdtfi.ctypes, size, ufx__icvlc, pe, tag, cond)
        return impl_tz_arr
    if arr in [binary_array_type, string_array_type]:
        ooew__diar = np.int32(numba_to_c_type(offset_type))
        sab__rlm = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            qpbl__jei = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            qpbl__jei = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        qrwa__fkj = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {qpbl__jei}(size, n_chars)
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
        lwe__nfez = dict()
        exec(qrwa__fkj, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            ooew__diar, 'char_typ_enum': sab__rlm}, lwe__nfez)
        impl = lwe__nfez['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    ufx__icvlc = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), ufx__icvlc)


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
        aqig__iydkk = n_pes if rank == root or allgather else 0
        keqx__cbl = np.empty(aqig__iydkk, dtype)
        c_gather_scalar(send.ctypes, keqx__cbl.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return keqx__cbl
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
        avwip__ruqsz = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], avwip__ruqsz)
        return builder.bitcast(avwip__ruqsz, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        avwip__ruqsz = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(avwip__ruqsz)
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
    mheww__hbr = types.unliteral(value)
    if isinstance(mheww__hbr, IndexValueType):
        mheww__hbr = mheww__hbr.val_typ
        zdt__xjaa = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            zdt__xjaa.append(types.int64)
            zdt__xjaa.append(bodo.datetime64ns)
            zdt__xjaa.append(bodo.timedelta64ns)
            zdt__xjaa.append(bodo.datetime_date_type)
            zdt__xjaa.append(bodo.TimeType)
        if mheww__hbr not in zdt__xjaa:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(mheww__hbr))
    typ_enum = np.int32(numba_to_c_type(mheww__hbr))

    def impl(value, reduce_op):
        qhcns__api = value_to_ptr(value)
        tiaq__yauk = value_to_ptr(value)
        _dist_reduce(qhcns__api, tiaq__yauk, reduce_op, typ_enum)
        return load_val_ptr(tiaq__yauk, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    mheww__hbr = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(mheww__hbr))
    xvex__amf = mheww__hbr(0)

    def impl(value, reduce_op):
        qhcns__api = value_to_ptr(value)
        tiaq__yauk = value_to_ptr(xvex__amf)
        _dist_exscan(qhcns__api, tiaq__yauk, reduce_op, typ_enum)
        return load_val_ptr(tiaq__yauk, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    sspff__jdf = 0
    xuc__zxtw = 0
    for i in range(len(recv_counts)):
        aeyf__sav = recv_counts[i]
        phou__jnzsd = recv_counts_nulls[i]
        ndkmf__ssu = tmp_null_bytes[sspff__jdf:sspff__jdf + phou__jnzsd]
        for xnp__zkgcu in range(aeyf__sav):
            set_bit_to(null_bitmap_ptr, xuc__zxtw, get_bit(ndkmf__ssu,
                xnp__zkgcu))
            xuc__zxtw += 1
        sspff__jdf += phou__jnzsd


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            dje__zkdba = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                dje__zkdba, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            csg__dzjcm = data.size
            recv_counts = gather_scalar(np.int32(csg__dzjcm), allgather,
                root=root)
            jxg__mgy = recv_counts.sum()
            cox__mqru = empty_like_type(jxg__mgy, data)
            gobb__sec = np.empty(1, np.int32)
            if rank == root or allgather:
                gobb__sec = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(csg__dzjcm), cox__mqru.ctypes,
                recv_counts.ctypes, gobb__sec.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return cox__mqru.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            cox__mqru = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(cox__mqru)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            cox__mqru = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(cox__mqru)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            csg__dzjcm = len(data)
            phou__jnzsd = csg__dzjcm + 7 >> 3
            recv_counts = gather_scalar(np.int32(csg__dzjcm), allgather,
                root=root)
            jxg__mgy = recv_counts.sum()
            cox__mqru = empty_like_type(jxg__mgy, data)
            gobb__sec = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            cil__uurc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                gobb__sec = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                cil__uurc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(csg__dzjcm),
                cox__mqru._days_data.ctypes, recv_counts.ctypes, gobb__sec.
                ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(csg__dzjcm),
                cox__mqru._seconds_data.ctypes, recv_counts.ctypes,
                gobb__sec.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(csg__dzjcm),
                cox__mqru._microseconds_data.ctypes, recv_counts.ctypes,
                gobb__sec.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(phou__jnzsd),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, cil__uurc.
                ctypes, sab__rlm, allgather, np.int32(root))
            copy_gathered_null_bytes(cox__mqru._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return cox__mqru
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, bodo.TimeArrayType)) or data in (boolean_array,
        datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            csg__dzjcm = len(data)
            phou__jnzsd = csg__dzjcm + 7 >> 3
            recv_counts = gather_scalar(np.int32(csg__dzjcm), allgather,
                root=root)
            jxg__mgy = recv_counts.sum()
            cox__mqru = empty_like_type(jxg__mgy, data)
            gobb__sec = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            cil__uurc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                gobb__sec = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                cil__uurc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(csg__dzjcm), cox__mqru.
                _data.ctypes, recv_counts.ctypes, gobb__sec.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(phou__jnzsd),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, cil__uurc.
                ctypes, sab__rlm, allgather, np.int32(root))
            copy_gathered_null_bytes(cox__mqru._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return cox__mqru
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        aaj__jdhl = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            ols__qrzsv = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                ols__qrzsv, aaj__jdhl)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            flwv__ezym = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            zfin__voty = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(flwv__ezym,
                zfin__voty)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            jece__ytq = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            oqen__wwag = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                oqen__wwag, jece__ytq)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        aqap__givl = np.iinfo(np.int64).max
        jzul__ksyu = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            qkdpy__qxv = data._start
            lweht__vgcfl = data._stop
            if len(data) == 0:
                qkdpy__qxv = aqap__givl
                lweht__vgcfl = jzul__ksyu
            qkdpy__qxv = bodo.libs.distributed_api.dist_reduce(qkdpy__qxv,
                np.int32(Reduce_Type.Min.value))
            lweht__vgcfl = bodo.libs.distributed_api.dist_reduce(lweht__vgcfl,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if qkdpy__qxv == aqap__givl and lweht__vgcfl == jzul__ksyu:
                qkdpy__qxv = 0
                lweht__vgcfl = 0
            xoyc__qsd = max(0, -(-(lweht__vgcfl - qkdpy__qxv) // data._step))
            if xoyc__qsd < total_len:
                lweht__vgcfl = qkdpy__qxv + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                qkdpy__qxv = 0
                lweht__vgcfl = 0
            return bodo.hiframes.pd_index_ext.init_range_index(qkdpy__qxv,
                lweht__vgcfl, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            swmt__kja = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, swmt__kja)
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
            cox__mqru = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(cox__mqru,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        lsxva__trryu = {'bodo': bodo, 'get_table_block': bodo.hiframes.
            table.get_table_block, 'ensure_column_unboxed': bodo.hiframes.
            table.ensure_column_unboxed, 'set_table_block': bodo.hiframes.
            table.set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table,
            'decode_if_dict_ary': bodo.hiframes.table.init_table}
        qrwa__fkj = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        qrwa__fkj += '  T = data\n'
        qrwa__fkj += '  T2 = init_table(T, True)\n'
        toabj__atp = bodo.hiframes.table.get_init_table_output_type(data, True)
        zuf__xhiod = (bodo.string_array_type in data.type_to_blk and bodo.
            dict_str_arr_type in data.type_to_blk)
        if zuf__xhiod:
            qrwa__fkj += (bodo.hiframes.table.
                gen_str_and_dict_enc_cols_to_one_block_fn_txt(data,
                toabj__atp, lsxva__trryu, True))
        for kfyyi__xyl, cobos__gini in data.type_to_blk.items():
            if zuf__xhiod and kfyyi__xyl in (bodo.string_array_type, bodo.
                dict_str_arr_type):
                continue
            elif kfyyi__xyl == bodo.dict_str_arr_type:
                assert bodo.string_array_type in toabj__atp.type_to_blk, 'Error in gatherv: If encoded string type is present in the input, then non-encoded string type should be present in the output'
                mxfs__mnx = toabj__atp.type_to_blk[bodo.string_array_type]
            else:
                assert kfyyi__xyl in toabj__atp.type_to_blk, 'Error in gatherv: All non-encoded string types present in the input should be present in the output'
                mxfs__mnx = toabj__atp.type_to_blk[kfyyi__xyl]
            lsxva__trryu[f'arr_inds_{cobos__gini}'] = np.array(data.
                block_to_arr_ind[cobos__gini], dtype=np.int64)
            qrwa__fkj += (
                f'  arr_list_{cobos__gini} = get_table_block(T, {cobos__gini})\n'
                )
            qrwa__fkj += f"""  out_arr_list_{cobos__gini} = alloc_list_like(arr_list_{cobos__gini}, len(arr_list_{cobos__gini}), True)
"""
            qrwa__fkj += f'  for i in range(len(arr_list_{cobos__gini})):\n'
            qrwa__fkj += (
                f'    arr_ind_{cobos__gini} = arr_inds_{cobos__gini}[i]\n')
            qrwa__fkj += f"""    ensure_column_unboxed(T, arr_list_{cobos__gini}, i, arr_ind_{cobos__gini})
"""
            qrwa__fkj += f"""    out_arr_{cobos__gini} = bodo.gatherv(arr_list_{cobos__gini}[i], allgather, warn_if_rep, root)
"""
            qrwa__fkj += (
                f'    out_arr_list_{cobos__gini}[i] = out_arr_{cobos__gini}\n')
            qrwa__fkj += (
                f'  T2 = set_table_block(T2, out_arr_list_{cobos__gini}, {mxfs__mnx})\n'
                )
        qrwa__fkj += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        qrwa__fkj += f'  T2 = set_table_len(T2, length)\n'
        qrwa__fkj += f'  return T2\n'
        lwe__nfez = {}
        exec(qrwa__fkj, lsxva__trryu, lwe__nfez)
        dnix__nlp = lwe__nfez['impl_table']
        return dnix__nlp
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        zqejr__jxh = len(data.columns)
        if zqejr__jxh == 0:
            wsjsy__ilc = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                lhr__amkp = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    lhr__amkp, wsjsy__ilc)
            return impl
        mpym__xcywg = ', '.join(f'g_data_{i}' for i in range(zqejr__jxh))
        qrwa__fkj = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            ddzk__fwab = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            mpym__xcywg = 'T2'
            qrwa__fkj += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            qrwa__fkj += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(zqejr__jxh):
                qrwa__fkj += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                qrwa__fkj += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        qrwa__fkj += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qrwa__fkj += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        qrwa__fkj += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(mpym__xcywg))
        lwe__nfez = {}
        lsxva__trryu = {'bodo': bodo,
            '__col_name_meta_value_gatherv_with_cols': ColNamesMetaType(
            data.columns)}
        exec(qrwa__fkj, lsxva__trryu, lwe__nfez)
        upugw__tor = lwe__nfez['impl_df']
        return upugw__tor
    if isinstance(data, ArrayItemArrayType):
        lqk__ssw = np.int32(numba_to_c_type(types.int32))
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pid__dvp = bodo.libs.array_item_arr_ext.get_offsets(data)
            nri__hdtfi = bodo.libs.array_item_arr_ext.get_data(data)
            nri__hdtfi = nri__hdtfi[:pid__dvp[-1]]
            msh__irqx = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            csg__dzjcm = len(data)
            zvqc__xbjwv = np.empty(csg__dzjcm, np.uint32)
            phou__jnzsd = csg__dzjcm + 7 >> 3
            for i in range(csg__dzjcm):
                zvqc__xbjwv[i] = pid__dvp[i + 1] - pid__dvp[i]
            recv_counts = gather_scalar(np.int32(csg__dzjcm), allgather,
                root=root)
            jxg__mgy = recv_counts.sum()
            gobb__sec = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            cil__uurc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                gobb__sec = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for fyohe__rtdqp in range(len(recv_counts)):
                    recv_counts_nulls[fyohe__rtdqp] = recv_counts[fyohe__rtdqp
                        ] + 7 >> 3
                cil__uurc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            oybi__dex = np.empty(jxg__mgy + 1, np.uint32)
            xtsqv__bzt = bodo.gatherv(nri__hdtfi, allgather, warn_if_rep, root)
            oexos__difo = np.empty(jxg__mgy + 7 >> 3, np.uint8)
            c_gatherv(zvqc__xbjwv.ctypes, np.int32(csg__dzjcm), oybi__dex.
                ctypes, recv_counts.ctypes, gobb__sec.ctypes, lqk__ssw,
                allgather, np.int32(root))
            c_gatherv(msh__irqx.ctypes, np.int32(phou__jnzsd),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, cil__uurc.
                ctypes, sab__rlm, allgather, np.int32(root))
            dummy_use(data)
            adum__mbzpx = np.empty(jxg__mgy + 1, np.uint64)
            convert_len_arr_to_offset(oybi__dex.ctypes, adum__mbzpx.ctypes,
                jxg__mgy)
            copy_gathered_null_bytes(oexos__difo.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                jxg__mgy, xtsqv__bzt, adum__mbzpx, oexos__difo)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        khp__qjg = data.names
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            mujtb__qjep = bodo.libs.struct_arr_ext.get_data(data)
            tupj__yvsjf = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            mkoum__exc = bodo.gatherv(mujtb__qjep, allgather=allgather,
                root=root)
            rank = bodo.libs.distributed_api.get_rank()
            csg__dzjcm = len(data)
            phou__jnzsd = csg__dzjcm + 7 >> 3
            recv_counts = gather_scalar(np.int32(csg__dzjcm), allgather,
                root=root)
            jxg__mgy = recv_counts.sum()
            ljlf__nsrp = np.empty(jxg__mgy + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            cil__uurc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                cil__uurc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(tupj__yvsjf.ctypes, np.int32(phou__jnzsd),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, cil__uurc.
                ctypes, sab__rlm, allgather, np.int32(root))
            copy_gathered_null_bytes(ljlf__nsrp.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(mkoum__exc,
                ljlf__nsrp, khp__qjg)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            cox__mqru = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(cox__mqru)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cox__mqru = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(cox__mqru)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            cox__mqru = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(cox__mqru)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cox__mqru = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            nyev__feqy = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            uag__cnod = bodo.gatherv(data.indptr, allgather, warn_if_rep, root)
            xcxdo__mepa = gather_scalar(data.shape[0], allgather, root=root)
            ubagm__cawle = xcxdo__mepa.sum()
            zqejr__jxh = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            elsyq__cvxee = np.empty(ubagm__cawle + 1, np.int64)
            nyev__feqy = nyev__feqy.astype(np.int64)
            elsyq__cvxee[0] = 0
            mfv__oafr = 1
            qsppo__per = 0
            for lmm__htw in xcxdo__mepa:
                for wxdfk__nsnb in range(lmm__htw):
                    adsm__ckcth = uag__cnod[qsppo__per + 1] - uag__cnod[
                        qsppo__per]
                    elsyq__cvxee[mfv__oafr] = elsyq__cvxee[mfv__oafr - 1
                        ] + adsm__ckcth
                    mfv__oafr += 1
                    qsppo__per += 1
                qsppo__per += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(cox__mqru,
                nyev__feqy, elsyq__cvxee, (ubagm__cawle, zqejr__jxh))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        qrwa__fkj = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        qrwa__fkj += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        lwe__nfez = {}
        exec(qrwa__fkj, {'bodo': bodo}, lwe__nfez)
        xzpna__vca = lwe__nfez['impl_tuple']
        return xzpna__vca
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as nbv__hxk:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        qrwa__fkj = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        pwqlm__voqa = ', '.join([f"'{jece__ytq}'" for jece__ytq in data.names])
        loxy__rzfft = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        qrwa__fkj += f"""  return bodosql.context_ext.init_sql_context(({pwqlm__voqa}, ), ({loxy__rzfft}, ), data.catalog)
"""
        lwe__nfez = {}
        exec(qrwa__fkj, {'bodo': bodo, 'bodosql': bodosql}, lwe__nfez)
        eqp__cehn = lwe__nfez['impl_bodosql_context']
        return eqp__cehn
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as nbv__hxk:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        qrwa__fkj = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        qrwa__fkj += f'  return data\n'
        lwe__nfez = {}
        exec(qrwa__fkj, {}, lwe__nfez)
        gvi__zxqd = lwe__nfez['impl_table_path']
        return gvi__zxqd
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    qrwa__fkj = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    qrwa__fkj += '    if random:\n'
    qrwa__fkj += '        if random_seed is None:\n'
    qrwa__fkj += '            random = 1\n'
    qrwa__fkj += '        else:\n'
    qrwa__fkj += '            random = 2\n'
    qrwa__fkj += '    if random_seed is None:\n'
    qrwa__fkj += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        hkeby__xvu = data
        zqejr__jxh = len(hkeby__xvu.columns)
        for i in range(zqejr__jxh):
            qrwa__fkj += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        qrwa__fkj += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        mpym__xcywg = ', '.join(f'data_{i}' for i in range(zqejr__jxh))
        qrwa__fkj += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(vvlm__kdwgb) for
            vvlm__kdwgb in range(zqejr__jxh))))
        qrwa__fkj += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        qrwa__fkj += '    if dests is None:\n'
        qrwa__fkj += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qrwa__fkj += '    else:\n'
        qrwa__fkj += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for pnp__iyqau in range(zqejr__jxh):
            qrwa__fkj += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(pnp__iyqau))
        qrwa__fkj += (
            '    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
            .format(zqejr__jxh))
        qrwa__fkj += '    delete_table(out_table)\n'
        qrwa__fkj += '    if parallel:\n'
        qrwa__fkj += '        delete_table(table_total)\n'
        mpym__xcywg = ', '.join('out_arr_{}'.format(i) for i in range(
            zqejr__jxh))
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        qrwa__fkj += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(mpym__xcywg, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        qrwa__fkj += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        qrwa__fkj += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        qrwa__fkj += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        qrwa__fkj += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        qrwa__fkj += '    if dests is None:\n'
        qrwa__fkj += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qrwa__fkj += '    else:\n'
        qrwa__fkj += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        qrwa__fkj += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        qrwa__fkj += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        qrwa__fkj += '    delete_table(out_table)\n'
        qrwa__fkj += '    if parallel:\n'
        qrwa__fkj += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        qrwa__fkj += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        qrwa__fkj += '    if not parallel:\n'
        qrwa__fkj += '        return data\n'
        qrwa__fkj += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        qrwa__fkj += '    if dests is None:\n'
        qrwa__fkj += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        qrwa__fkj += '    elif bodo.get_rank() not in dests:\n'
        qrwa__fkj += '        dim0_local_size = 0\n'
        qrwa__fkj += '    else:\n'
        qrwa__fkj += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        qrwa__fkj += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        qrwa__fkj += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        qrwa__fkj += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        qrwa__fkj += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        qrwa__fkj += '    if dests is None:\n'
        qrwa__fkj += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qrwa__fkj += '    else:\n'
        qrwa__fkj += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        qrwa__fkj += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        qrwa__fkj += '    delete_table(out_table)\n'
        qrwa__fkj += '    if parallel:\n'
        qrwa__fkj += '        delete_table(table_total)\n'
        qrwa__fkj += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    lwe__nfez = {}
    lsxva__trryu = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        lsxva__trryu.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(hkeby__xvu.columns)})
    exec(qrwa__fkj, lsxva__trryu, lwe__nfez)
    impl = lwe__nfez['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    qrwa__fkj = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        qrwa__fkj += '    if seed is None:\n'
        qrwa__fkj += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        qrwa__fkj += '    np.random.seed(seed)\n'
        qrwa__fkj += '    if not parallel:\n'
        qrwa__fkj += '        data = data.copy()\n'
        qrwa__fkj += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            qrwa__fkj += '        data = data[:n_samples]\n'
        qrwa__fkj += '        return data\n'
        qrwa__fkj += '    else:\n'
        qrwa__fkj += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        qrwa__fkj += '        permutation = np.arange(dim0_global_size)\n'
        qrwa__fkj += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            qrwa__fkj += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            qrwa__fkj += '        n_samples = dim0_global_size\n'
        qrwa__fkj += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        qrwa__fkj += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        qrwa__fkj += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        qrwa__fkj += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        qrwa__fkj += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        qrwa__fkj += '        return output\n'
    else:
        qrwa__fkj += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            qrwa__fkj += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            qrwa__fkj += '    output = output[:local_n_samples]\n'
        qrwa__fkj += '    return output\n'
    lwe__nfez = {}
    exec(qrwa__fkj, {'np': np, 'bodo': bodo}, lwe__nfez)
    impl = lwe__nfez['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    geo__tyu = np.empty(sendcounts_nulls.sum(), np.uint8)
    sspff__jdf = 0
    xuc__zxtw = 0
    for prybk__qnn in range(len(sendcounts)):
        aeyf__sav = sendcounts[prybk__qnn]
        phou__jnzsd = sendcounts_nulls[prybk__qnn]
        ndkmf__ssu = geo__tyu[sspff__jdf:sspff__jdf + phou__jnzsd]
        for xnp__zkgcu in range(aeyf__sav):
            set_bit_to_arr(ndkmf__ssu, xnp__zkgcu, get_bit_bitmap(
                null_bitmap_ptr, xuc__zxtw))
            xuc__zxtw += 1
        sspff__jdf += phou__jnzsd
    return geo__tyu


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    xpgid__jfubo = MPI.COMM_WORLD
    data = xpgid__jfubo.bcast(data, root)
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
    luw__qafsq = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    jnza__rsoyz = (0,) * luw__qafsq

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        ami__cmesw = np.ascontiguousarray(data)
        gwaas__grb = data.ctypes
        beuep__bjj = jnza__rsoyz
        if rank == MPI_ROOT:
            beuep__bjj = ami__cmesw.shape
        beuep__bjj = bcast_tuple(beuep__bjj)
        qqp__lvvy = get_tuple_prod(beuep__bjj[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            beuep__bjj[0])
        send_counts *= qqp__lvvy
        csg__dzjcm = send_counts[rank]
        nlg__lvwlb = np.empty(csg__dzjcm, dtype)
        gobb__sec = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(gwaas__grb, send_counts.ctypes, gobb__sec.ctypes,
            nlg__lvwlb.ctypes, np.int32(csg__dzjcm), np.int32(typ_val))
        return nlg__lvwlb.reshape((-1,) + beuep__bjj[1:])
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
        agbz__juu = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], agbz__juu)
    if isinstance(dtype, FloatingArrayType):
        agbz__juu = 'Float{}'.format(dtype.dtype.bitwidth)
        return pd.array([3.0], agbz__juu)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        jece__ytq = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=jece__ytq)
        syqdn__pict = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(syqdn__pict)
        return pd.Index(arr, name=jece__ytq)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        jece__ytq = _get_name_value_for_type(dtype.name_typ)
        khp__qjg = tuple(_get_name_value_for_type(t) for t in dtype.names_typ)
        mkenh__kuh = tuple(get_value_for_type(t) for t in dtype.array_types)
        mkenh__kuh = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in mkenh__kuh)
        val = pd.MultiIndex.from_arrays(mkenh__kuh, names=khp__qjg)
        val.name = jece__ytq
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        jece__ytq = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=jece__ytq)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        mkenh__kuh = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({jece__ytq: arr for jece__ytq, arr in zip(dtype
            .columns, mkenh__kuh)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        syqdn__pict = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(syqdn__pict[0],
            syqdn__pict[0])])
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
        lqk__ssw = np.int32(numba_to_c_type(types.int32))
        sab__rlm = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            qpbl__jei = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            qpbl__jei = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        qrwa__fkj = f"""def impl(
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
            recv_arr = {qpbl__jei}(n_loc, n_loc_char)

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
        lwe__nfez = dict()
        exec(qrwa__fkj, {'bodo': bodo, 'np': np, 'int32_typ_enum': lqk__ssw,
            'char_typ_enum': sab__rlm, 'decode_if_dict_array':
            decode_if_dict_array}, lwe__nfez)
        impl = lwe__nfez['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        lqk__ssw = np.int32(numba_to_c_type(types.int32))
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            cxfx__qsj = bodo.libs.array_item_arr_ext.get_offsets(data)
            tabhk__tse = bodo.libs.array_item_arr_ext.get_data(data)
            tabhk__tse = tabhk__tse[:cxfx__qsj[-1]]
            dyvw__zxm = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            nqboj__usdb = bcast_scalar(len(data))
            tdy__wgbue = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                tdy__wgbue[i] = cxfx__qsj[i + 1] - cxfx__qsj[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                nqboj__usdb)
            gobb__sec = bodo.ir.join.calc_disp(send_counts)
            gqd__ale = np.empty(n_pes, np.int32)
            if rank == 0:
                kshyx__byg = 0
                for i in range(n_pes):
                    vlfy__mvvqg = 0
                    for wxdfk__nsnb in range(send_counts[i]):
                        vlfy__mvvqg += tdy__wgbue[kshyx__byg]
                        kshyx__byg += 1
                    gqd__ale[i] = vlfy__mvvqg
            bcast(gqd__ale)
            lblu__dld = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                lblu__dld[i] = send_counts[i] + 7 >> 3
            cil__uurc = bodo.ir.join.calc_disp(lblu__dld)
            csg__dzjcm = send_counts[rank]
            gnphh__hkdhm = np.empty(csg__dzjcm + 1, np_offset_type)
            eyw__jir = bodo.libs.distributed_api.scatterv_impl(tabhk__tse,
                gqd__ale)
            hooak__rtmb = csg__dzjcm + 7 >> 3
            ndhlt__uaw = np.empty(hooak__rtmb, np.uint8)
            kvt__ckh = np.empty(csg__dzjcm, np.uint32)
            c_scatterv(tdy__wgbue.ctypes, send_counts.ctypes, gobb__sec.
                ctypes, kvt__ckh.ctypes, np.int32(csg__dzjcm), lqk__ssw)
            convert_len_arr_to_offset(kvt__ckh.ctypes, gnphh__hkdhm.ctypes,
                csg__dzjcm)
            rcky__rdd = get_scatter_null_bytes_buff(dyvw__zxm.ctypes,
                send_counts, lblu__dld)
            c_scatterv(rcky__rdd.ctypes, lblu__dld.ctypes, cil__uurc.ctypes,
                ndhlt__uaw.ctypes, np.int32(hooak__rtmb), sab__rlm)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                csg__dzjcm, eyw__jir, gnphh__hkdhm, ndhlt__uaw)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or data in (boolean_array, datetime_date_array_type):
        sab__rlm = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            izq__emwa = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, FloatingArrayType):
            izq__emwa = bodo.libs.float_arr_ext.init_float_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            izq__emwa = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            izq__emwa = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            izq__emwa = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            ami__cmesw = data._data
            tupj__yvsjf = data._null_bitmap
            obp__xkdz = len(ami__cmesw)
            noosc__vno = _scatterv_np(ami__cmesw, send_counts)
            nqboj__usdb = bcast_scalar(obp__xkdz)
            nmsl__cmm = len(noosc__vno) + 7 >> 3
            cqs__awjo = np.empty(nmsl__cmm, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                nqboj__usdb)
            lblu__dld = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                lblu__dld[i] = send_counts[i] + 7 >> 3
            cil__uurc = bodo.ir.join.calc_disp(lblu__dld)
            rcky__rdd = get_scatter_null_bytes_buff(tupj__yvsjf.ctypes,
                send_counts, lblu__dld)
            c_scatterv(rcky__rdd.ctypes, lblu__dld.ctypes, cil__uurc.ctypes,
                cqs__awjo.ctypes, np.int32(nmsl__cmm), sab__rlm)
            return izq__emwa(noosc__vno, cqs__awjo)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            ogpn__xsmh = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            hdbiz__zhc = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(ogpn__xsmh,
                hdbiz__zhc)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            qkdpy__qxv = data._start
            lweht__vgcfl = data._stop
            xcyz__mlvd = data._step
            jece__ytq = data._name
            jece__ytq = bcast_scalar(jece__ytq)
            qkdpy__qxv = bcast_scalar(qkdpy__qxv)
            lweht__vgcfl = bcast_scalar(lweht__vgcfl)
            xcyz__mlvd = bcast_scalar(xcyz__mlvd)
            casi__fpxx = bodo.libs.array_kernels.calc_nitems(qkdpy__qxv,
                lweht__vgcfl, xcyz__mlvd)
            chunk_start = bodo.libs.distributed_api.get_start(casi__fpxx,
                n_pes, rank)
            oaxr__xvwe = bodo.libs.distributed_api.get_node_portion(casi__fpxx,
                n_pes, rank)
            njtr__huv = qkdpy__qxv + xcyz__mlvd * chunk_start
            jgmy__bsl = qkdpy__qxv + xcyz__mlvd * (chunk_start + oaxr__xvwe)
            jgmy__bsl = min(jgmy__bsl, lweht__vgcfl)
            return bodo.hiframes.pd_index_ext.init_range_index(njtr__huv,
                jgmy__bsl, xcyz__mlvd, jece__ytq)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        swmt__kja = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            ami__cmesw = data._data
            jece__ytq = data._name
            jece__ytq = bcast_scalar(jece__ytq)
            arr = bodo.libs.distributed_api.scatterv_impl(ami__cmesw,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                jece__ytq, swmt__kja)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            ami__cmesw = data._data
            jece__ytq = data._name
            jece__ytq = bcast_scalar(jece__ytq)
            arr = bodo.libs.distributed_api.scatterv_impl(ami__cmesw,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, jece__ytq)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            cox__mqru = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            jece__ytq = bcast_scalar(data._name)
            khp__qjg = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(cox__mqru,
                khp__qjg, jece__ytq)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            jece__ytq = bodo.hiframes.pd_series_ext.get_series_name(data)
            dgcdg__uvo = bcast_scalar(jece__ytq)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            oqen__wwag = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                oqen__wwag, dgcdg__uvo)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        zqejr__jxh = len(data.columns)
        hacw__xbl = ColNamesMetaType(data.columns)
        qrwa__fkj = 'def impl_df(data, send_counts=None, warn_if_dist=True):\n'
        if data.is_table_format:
            qrwa__fkj += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            qrwa__fkj += """  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)
"""
            mpym__xcywg = 'g_table'
        else:
            for i in range(zqejr__jxh):
                qrwa__fkj += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                qrwa__fkj += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            mpym__xcywg = ', '.join(f'g_data_{i}' for i in range(zqejr__jxh))
        qrwa__fkj += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qrwa__fkj += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        qrwa__fkj += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({mpym__xcywg},), g_index, __col_name_meta_scaterv_impl)
"""
        lwe__nfez = {}
        exec(qrwa__fkj, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            hacw__xbl}, lwe__nfez)
        upugw__tor = lwe__nfez['impl_df']
        return upugw__tor
    if isinstance(data, bodo.TableType):
        qrwa__fkj = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        qrwa__fkj += '  T = data\n'
        qrwa__fkj += '  T2 = init_table(T, False)\n'
        qrwa__fkj += '  l = 0\n'
        lsxva__trryu = {}
        for ophbn__wpyhc in data.type_to_blk.values():
            lsxva__trryu[f'arr_inds_{ophbn__wpyhc}'] = np.array(data.
                block_to_arr_ind[ophbn__wpyhc], dtype=np.int64)
            qrwa__fkj += (
                f'  arr_list_{ophbn__wpyhc} = get_table_block(T, {ophbn__wpyhc})\n'
                )
            qrwa__fkj += f"""  out_arr_list_{ophbn__wpyhc} = alloc_list_like(arr_list_{ophbn__wpyhc}, len(arr_list_{ophbn__wpyhc}), False)
"""
            qrwa__fkj += f'  for i in range(len(arr_list_{ophbn__wpyhc})):\n'
            qrwa__fkj += (
                f'    arr_ind_{ophbn__wpyhc} = arr_inds_{ophbn__wpyhc}[i]\n')
            qrwa__fkj += f"""    ensure_column_unboxed(T, arr_list_{ophbn__wpyhc}, i, arr_ind_{ophbn__wpyhc})
"""
            qrwa__fkj += f"""    out_arr_{ophbn__wpyhc} = bodo.libs.distributed_api.scatterv_impl(arr_list_{ophbn__wpyhc}[i], send_counts)
"""
            qrwa__fkj += (
                f'    out_arr_list_{ophbn__wpyhc}[i] = out_arr_{ophbn__wpyhc}\n'
                )
            qrwa__fkj += f'    l = len(out_arr_{ophbn__wpyhc})\n'
            qrwa__fkj += f"""  T2 = set_table_block(T2, out_arr_list_{ophbn__wpyhc}, {ophbn__wpyhc})
"""
        qrwa__fkj += f'  T2 = set_table_len(T2, l)\n'
        qrwa__fkj += f'  return T2\n'
        lsxva__trryu.update({'bodo': bodo, 'init_table': bodo.hiframes.
            table.init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        lwe__nfez = {}
        exec(qrwa__fkj, lsxva__trryu, lwe__nfez)
        return lwe__nfez['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                tivx__dzgx = data._data
                bodo.libs.distributed_api.bcast_scalar(len(tivx__dzgx))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(tivx__dzgx)))
            else:
                xoyc__qsd = bodo.libs.distributed_api.bcast_scalar(0)
                epb__tiws = bodo.libs.distributed_api.bcast_scalar(0)
                tivx__dzgx = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    xoyc__qsd, epb__tiws)
            bodo.libs.distributed_api.bcast(tivx__dzgx)
            ogk__aqnb = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(tivx__dzgx,
                ogk__aqnb, True, data._has_deduped_local_dictionary)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            dje__zkdba = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                dje__zkdba, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        qrwa__fkj = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        qrwa__fkj += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        lwe__nfez = {}
        exec(qrwa__fkj, {'bodo': bodo}, lwe__nfez)
        xzpna__vca = lwe__nfez['impl_tuple']
        return xzpna__vca
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
        ooew__diar = np.int32(numba_to_c_type(offset_type))
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            csg__dzjcm = len(data)
            mxyt__voo = num_total_chars(data)
            assert csg__dzjcm < INT_MAX
            assert mxyt__voo < INT_MAX
            vls__fxu = get_offset_ptr(data)
            gwaas__grb = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            phou__jnzsd = csg__dzjcm + 7 >> 3
            c_bcast(vls__fxu, np.int32(csg__dzjcm + 1), ooew__diar, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(gwaas__grb, np.int32(mxyt__voo), sab__rlm, np.array([-1
                ]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(phou__jnzsd), sab__rlm, np.
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
        sab__rlm = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                lcng__kcxe = 0
                ubts__mgmfv = np.empty(0, np.uint8).ctypes
            else:
                ubts__mgmfv, lcng__kcxe = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            lcng__kcxe = bodo.libs.distributed_api.bcast_scalar(lcng__kcxe,
                root)
            if rank != root:
                qowz__muwke = np.empty(lcng__kcxe + 1, np.uint8)
                qowz__muwke[lcng__kcxe] = 0
                ubts__mgmfv = qowz__muwke.ctypes
            c_bcast(ubts__mgmfv, np.int32(lcng__kcxe), sab__rlm, np.array([
                -1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(ubts__mgmfv, lcng__kcxe)
        return impl_str
    typ_val = numba_to_c_type(val)
    qrwa__fkj = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    lwe__nfez = {}
    exec(qrwa__fkj, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, lwe__nfez)
    bwlrl__hrzso = lwe__nfez['bcast_scalar_impl']
    return bwlrl__hrzso


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple
        ), 'Internal Error: Argument to bcast tuple must be of type tuple'
    reisn__umbzk = len(val)
    qrwa__fkj = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    qrwa__fkj += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(reisn__umbzk
        )), ',' if reisn__umbzk else '')
    lwe__nfez = {}
    exec(qrwa__fkj, {'bcast_scalar': bcast_scalar}, lwe__nfez)
    qvi__hlf = lwe__nfez['bcast_tuple_impl']
    return qvi__hlf


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            csg__dzjcm = bcast_scalar(len(arr), root)
            zwrya__jxp = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(csg__dzjcm, zwrya__jxp)
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
            njtr__huv = max(arr_start, slice_index.start) - arr_start
            jgmy__bsl = max(slice_index.stop - arr_start, 0)
            return slice(njtr__huv, jgmy__bsl)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            qkdpy__qxv = slice_index.start
            xcyz__mlvd = slice_index.step
            fpr__gty = 0 if xcyz__mlvd == 1 or qkdpy__qxv > arr_start else abs(
                xcyz__mlvd - arr_start % xcyz__mlvd) % xcyz__mlvd
            njtr__huv = max(arr_start, slice_index.start
                ) - arr_start + fpr__gty
            jgmy__bsl = max(slice_index.stop - arr_start, 0)
            return slice(njtr__huv, jgmy__bsl, xcyz__mlvd)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        cnsi__hzzsk = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[cnsi__hzzsk])
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
        tfir__dth = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        sab__rlm = np.int32(numba_to_c_type(types.uint8))
        rhjvw__yccd = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            hkuq__xrep = np.int32(10)
            tag = np.int32(11)
            qgmw__oyro = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                nri__hdtfi = arr._data
                eot__dffok = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    nri__hdtfi, ind)
                iwi__ouipj = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    nri__hdtfi, ind + 1)
                length = iwi__ouipj - eot__dffok
                avwip__ruqsz = nri__hdtfi[ind]
                qgmw__oyro[0] = length
                isend(qgmw__oyro, np.int32(1), root, hkuq__xrep, True)
                isend(avwip__ruqsz, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                rhjvw__yccd, tfir__dth, 0, 1)
            xoyc__qsd = 0
            if rank == root:
                xoyc__qsd = recv(np.int64, ANY_SOURCE, hkuq__xrep)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    rhjvw__yccd, tfir__dth, xoyc__qsd, 1)
                gwaas__grb = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(gwaas__grb, np.int32(xoyc__qsd), sab__rlm, ANY_SOURCE,
                    tag)
            dummy_use(qgmw__oyro)
            xoyc__qsd = bcast_scalar(xoyc__qsd)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    rhjvw__yccd, tfir__dth, xoyc__qsd, 1)
            gwaas__grb = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(gwaas__grb, np.int32(xoyc__qsd), sab__rlm, np.array([-1
                ]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, xoyc__qsd)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        vrwhv__fhiw = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, vrwhv__fhiw)
            if arr_start <= ind < arr_start + len(arr):
                dje__zkdba = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = dje__zkdba[ind - arr_start]
                send_arr = np.full(1, data, vrwhv__fhiw)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = vrwhv__fhiw(-1)
            if rank == root:
                val = recv(vrwhv__fhiw, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            gnd__khhqv = arr.dtype.categories[max(val, 0)]
            return gnd__khhqv
        return cat_getitem_impl
    if isinstance(arr, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        jvr__rvgp = arr.tz

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
                jvr__rvgp)
        return tz_aware_getitem_impl
    ugy__agdq = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, ugy__agdq)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, ugy__agdq)[0]
        if rank == root:
            val = recv(ugy__agdq, ANY_SOURCE, tag)
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
        xslh__lrkck = np.empty(n_pes, np.int64)
        wuy__mxp = np.empty(n_pes, np.int8)
        val = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        ekhzd__ukqji = 1
        if len(A) != 0:
            val = A[-1]
            ekhzd__ukqji = 0
        allgather(xslh__lrkck, np.int64(val))
        allgather(wuy__mxp, ekhzd__ukqji)
        for i, ekhzd__ukqji in enumerate(wuy__mxp):
            if ekhzd__ukqji and i != 0:
                xslh__lrkck[i] = xslh__lrkck[i - 1]
        return xslh__lrkck
    return impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    pyek__vugv = get_type_enum(out_data)
    assert typ_enum == pyek__vugv
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
    qrwa__fkj = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        qrwa__fkj += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    qrwa__fkj += '  return\n'
    lwe__nfez = {}
    exec(qrwa__fkj, {'alltoallv': alltoallv}, lwe__nfez)
    aqur__iku = lwe__nfez['f']
    return aqur__iku


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    qkdpy__qxv = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return qkdpy__qxv, count


@numba.njit
def get_start(total_size, pes, rank):
    keqx__cbl = total_size % pes
    mie__nhmhz = (total_size - keqx__cbl) // pes
    return rank * mie__nhmhz + min(rank, keqx__cbl)


@numba.njit
def get_end(total_size, pes, rank):
    keqx__cbl = total_size % pes
    mie__nhmhz = (total_size - keqx__cbl) // pes
    return (rank + 1) * mie__nhmhz + min(rank + 1, keqx__cbl)


@numba.njit
def get_node_portion(total_size, pes, rank):
    keqx__cbl = total_size % pes
    mie__nhmhz = (total_size - keqx__cbl) // pes
    if rank < keqx__cbl:
        return mie__nhmhz + 1
    else:
        return mie__nhmhz


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    xvex__amf = in_arr.dtype(0)
    wgrnu__cxbip = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        vlfy__mvvqg = xvex__amf
        for jsgs__ufk in np.nditer(in_arr):
            vlfy__mvvqg += jsgs__ufk.item()
        akbr__euro = dist_exscan(vlfy__mvvqg, wgrnu__cxbip)
        for i in range(in_arr.size):
            akbr__euro += in_arr[i]
            out_arr[i] = akbr__euro
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    ozcy__lsp = in_arr.dtype(1)
    wgrnu__cxbip = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        vlfy__mvvqg = ozcy__lsp
        for jsgs__ufk in np.nditer(in_arr):
            vlfy__mvvqg *= jsgs__ufk.item()
        akbr__euro = dist_exscan(vlfy__mvvqg, wgrnu__cxbip)
        if get_rank() == 0:
            akbr__euro = ozcy__lsp
        for i in range(in_arr.size):
            akbr__euro *= in_arr[i]
            out_arr[i] = akbr__euro
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        ozcy__lsp = np.finfo(in_arr.dtype(1).dtype).max
    else:
        ozcy__lsp = np.iinfo(in_arr.dtype(1).dtype).max
    wgrnu__cxbip = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        vlfy__mvvqg = ozcy__lsp
        for jsgs__ufk in np.nditer(in_arr):
            vlfy__mvvqg = min(vlfy__mvvqg, jsgs__ufk.item())
        akbr__euro = dist_exscan(vlfy__mvvqg, wgrnu__cxbip)
        if get_rank() == 0:
            akbr__euro = ozcy__lsp
        for i in range(in_arr.size):
            akbr__euro = min(akbr__euro, in_arr[i])
            out_arr[i] = akbr__euro
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        ozcy__lsp = np.finfo(in_arr.dtype(1).dtype).min
    else:
        ozcy__lsp = np.iinfo(in_arr.dtype(1).dtype).min
    ozcy__lsp = in_arr.dtype(1)
    wgrnu__cxbip = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        vlfy__mvvqg = ozcy__lsp
        for jsgs__ufk in np.nditer(in_arr):
            vlfy__mvvqg = max(vlfy__mvvqg, jsgs__ufk.item())
        akbr__euro = dist_exscan(vlfy__mvvqg, wgrnu__cxbip)
        if get_rank() == 0:
            akbr__euro = ozcy__lsp
        for i in range(in_arr.size):
            akbr__euro = max(akbr__euro, in_arr[i])
            out_arr[i] = akbr__euro
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    ufx__icvlc = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), ufx__icvlc)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    nsgq__rlplr = args[0]
    if equiv_set.has_shape(nsgq__rlplr):
        return ArrayAnalysis.AnalyzeResult(shape=nsgq__rlplr, pre=[])
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
    ysy__ksndf = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for 
        i, qjii__fnzby in enumerate(args) if is_array_typ(qjii__fnzby) or
        isinstance(qjii__fnzby, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    qrwa__fkj = f"""def impl(*args):
    if {ysy__ksndf} or bodo.get_rank() == 0:
        print(*args)"""
    lwe__nfez = {}
    exec(qrwa__fkj, globals(), lwe__nfez)
    impl = lwe__nfez['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        ote__ioeta = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        qrwa__fkj = 'def f(req, cond=True):\n'
        qrwa__fkj += f'  return {ote__ioeta}\n'
        lwe__nfez = {}
        exec(qrwa__fkj, {'_wait': _wait}, lwe__nfez)
        impl = lwe__nfez['f']
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
        keqx__cbl = 1
        for a in t:
            keqx__cbl *= a
        return keqx__cbl
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    dbvp__fbsus = np.ascontiguousarray(in_arr)
    kmhfo__jbeo = get_tuple_prod(dbvp__fbsus.shape[1:])
    cgny__rkpx = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        cpev__qnwm = np.array(dest_ranks, dtype=np.int32)
    else:
        cpev__qnwm = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, dbvp__fbsus.ctypes,
        new_dim0_global_len, len(in_arr), dtype_size * cgny__rkpx, 
        dtype_size * kmhfo__jbeo, len(cpev__qnwm), cpev__qnwm.ctypes)
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
    fzsuh__aws = np.ascontiguousarray(rhs)
    gsjay__vpg = get_tuple_prod(fzsuh__aws.shape[1:])
    wlyll__rqaqm = dtype_size * gsjay__vpg
    permutation_array_index(lhs.ctypes, lhs_len, wlyll__rqaqm, fzsuh__aws.
        ctypes, fzsuh__aws.shape[0], p.ctypes, p_len, n_samples)
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
        qrwa__fkj = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        lwe__nfez = {}
        exec(qrwa__fkj, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, lwe__nfez)
        bwlrl__hrzso = lwe__nfez['bcast_scalar_impl']
        return bwlrl__hrzso
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        zqejr__jxh = len(data.columns)
        mpym__xcywg = ', '.join('g_data_{}'.format(i) for i in range(
            zqejr__jxh))
        hgczz__hyp = ColNamesMetaType(data.columns)
        qrwa__fkj = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(zqejr__jxh):
            qrwa__fkj += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            qrwa__fkj += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        qrwa__fkj += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qrwa__fkj += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        qrwa__fkj += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(mpym__xcywg))
        lwe__nfez = {}
        exec(qrwa__fkj, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            hgczz__hyp}, lwe__nfez)
        upugw__tor = lwe__nfez['impl_df']
        return upugw__tor
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            qkdpy__qxv = data._start
            lweht__vgcfl = data._stop
            xcyz__mlvd = data._step
            jece__ytq = data._name
            jece__ytq = bcast_scalar(jece__ytq, root)
            qkdpy__qxv = bcast_scalar(qkdpy__qxv, root)
            lweht__vgcfl = bcast_scalar(lweht__vgcfl, root)
            xcyz__mlvd = bcast_scalar(xcyz__mlvd, root)
            casi__fpxx = bodo.libs.array_kernels.calc_nitems(qkdpy__qxv,
                lweht__vgcfl, xcyz__mlvd)
            chunk_start = bodo.libs.distributed_api.get_start(casi__fpxx,
                n_pes, rank)
            oaxr__xvwe = bodo.libs.distributed_api.get_node_portion(casi__fpxx,
                n_pes, rank)
            njtr__huv = qkdpy__qxv + xcyz__mlvd * chunk_start
            jgmy__bsl = qkdpy__qxv + xcyz__mlvd * (chunk_start + oaxr__xvwe)
            jgmy__bsl = min(jgmy__bsl, lweht__vgcfl)
            return bodo.hiframes.pd_index_ext.init_range_index(njtr__huv,
                jgmy__bsl, xcyz__mlvd, jece__ytq)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            ami__cmesw = data._data
            jece__ytq = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(ami__cmesw,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, jece__ytq)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            jece__ytq = bodo.hiframes.pd_series_ext.get_series_name(data)
            dgcdg__uvo = bodo.libs.distributed_api.bcast_comm_impl(jece__ytq,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            oqen__wwag = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                oqen__wwag, dgcdg__uvo)
        return impl_series
    if isinstance(data, types.BaseTuple):
        qrwa__fkj = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        qrwa__fkj += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        lwe__nfez = {}
        exec(qrwa__fkj, {'bcast_comm_impl': bcast_comm_impl}, lwe__nfez)
        xzpna__vca = lwe__nfez['impl_tuple']
        return xzpna__vca
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    luw__qafsq = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    jnza__rsoyz = (0,) * luw__qafsq

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        ami__cmesw = np.ascontiguousarray(data)
        gwaas__grb = data.ctypes
        beuep__bjj = jnza__rsoyz
        if rank == root:
            beuep__bjj = ami__cmesw.shape
        beuep__bjj = bcast_tuple(beuep__bjj, root)
        qqp__lvvy = get_tuple_prod(beuep__bjj[1:])
        send_counts = beuep__bjj[0] * qqp__lvvy
        nlg__lvwlb = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(gwaas__grb, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(nlg__lvwlb.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return nlg__lvwlb.reshape((-1,) + beuep__bjj[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        xpgid__jfubo = MPI.COMM_WORLD
        vst__guhk = MPI.Get_processor_name()
        lpne__yehv = xpgid__jfubo.allgather(vst__guhk)
        node_ranks = defaultdict(list)
        for i, igvb__oirbr in enumerate(lpne__yehv):
            node_ranks[igvb__oirbr].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    xpgid__jfubo = MPI.COMM_WORLD
    loum__qzpz = xpgid__jfubo.Get_group()
    lyqr__vkb = loum__qzpz.Incl(comm_ranks)
    ivgx__iqbrg = xpgid__jfubo.Create_group(lyqr__vkb)
    return ivgx__iqbrg


def get_nodes_first_ranks():
    tqrvm__mlct = get_host_ranks()
    return np.array([fsba__yjhcp[0] for fsba__yjhcp in tqrvm__mlct.values()
        ], dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
