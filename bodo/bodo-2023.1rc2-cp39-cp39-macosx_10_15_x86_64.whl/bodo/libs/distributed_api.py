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
    jlzv__jxhd = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, jlzv__jxhd, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    jlzv__jxhd = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, jlzv__jxhd, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            jlzv__jxhd = get_type_enum(arr)
            return _isend(arr.ctypes, size, jlzv__jxhd, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        jlzv__jxhd = np.int32(numba_to_c_type(arr.dtype))
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            are__ghvv = size + 7 >> 3
            myuco__yknc = _isend(arr._data.ctypes, size, jlzv__jxhd, pe,
                tag, cond)
            gzy__bbyd = _isend(arr._null_bitmap.ctypes, are__ghvv,
                hlliz__zniq, pe, tag, cond)
            return myuco__yknc, gzy__bbyd
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            qrb__rnb = arr._data
            jlzv__jxhd = get_type_enum(qrb__rnb)
            return _isend(qrb__rnb.ctypes, size, jlzv__jxhd, pe, tag, cond)
        return impl_tz_arr
    if is_str_arr_type(arr) or arr == binary_array_type:
        byxu__dys = np.int32(numba_to_c_type(offset_type))
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            yljb__pbauc = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(yljb__pbauc, pe, tag - 1)
            are__ghvv = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                byxu__dys, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), yljb__pbauc,
                hlliz__zniq, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), are__ghvv,
                hlliz__zniq, pe, tag)
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
            jlzv__jxhd = get_type_enum(arr)
            return _irecv(arr.ctypes, size, jlzv__jxhd, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        jlzv__jxhd = np.int32(numba_to_c_type(arr.dtype))
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            are__ghvv = size + 7 >> 3
            myuco__yknc = _irecv(arr._data.ctypes, size, jlzv__jxhd, pe,
                tag, cond)
            gzy__bbyd = _irecv(arr._null_bitmap.ctypes, are__ghvv,
                hlliz__zniq, pe, tag, cond)
            return myuco__yknc, gzy__bbyd
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            qrb__rnb = arr._data
            jlzv__jxhd = get_type_enum(qrb__rnb)
            return _irecv(qrb__rnb.ctypes, size, jlzv__jxhd, pe, tag, cond)
        return impl_tz_arr
    if arr in [binary_array_type, string_array_type]:
        byxu__dys = np.int32(numba_to_c_type(offset_type))
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            zcuua__nqyu = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            zcuua__nqyu = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        vtwoi__yit = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {zcuua__nqyu}(size, n_chars)
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
        hcctx__yian = dict()
        exec(vtwoi__yit, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            byxu__dys, 'char_typ_enum': hlliz__zniq}, hcctx__yian)
        impl = hcctx__yian['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    jlzv__jxhd = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), jlzv__jxhd)


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
        pmy__qhd = n_pes if rank == root or allgather else 0
        lcrwl__rofpq = np.empty(pmy__qhd, dtype)
        c_gather_scalar(send.ctypes, lcrwl__rofpq.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return lcrwl__rofpq
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
        krvv__glf = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], krvv__glf)
        return builder.bitcast(krvv__glf, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        krvv__glf = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(krvv__glf)
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
    fkz__lpce = types.unliteral(value)
    if isinstance(fkz__lpce, IndexValueType):
        fkz__lpce = fkz__lpce.val_typ
        rme__kci = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            rme__kci.append(types.int64)
            rme__kci.append(bodo.datetime64ns)
            rme__kci.append(bodo.timedelta64ns)
            rme__kci.append(bodo.datetime_date_type)
            rme__kci.append(bodo.TimeType)
        if fkz__lpce not in rme__kci:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(fkz__lpce))
    typ_enum = np.int32(numba_to_c_type(fkz__lpce))

    def impl(value, reduce_op):
        xgu__umzlt = value_to_ptr(value)
        koqyp__smrn = value_to_ptr(value)
        _dist_reduce(xgu__umzlt, koqyp__smrn, reduce_op, typ_enum)
        return load_val_ptr(koqyp__smrn, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    fkz__lpce = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(fkz__lpce))
    uxvxa__cdh = fkz__lpce(0)

    def impl(value, reduce_op):
        xgu__umzlt = value_to_ptr(value)
        koqyp__smrn = value_to_ptr(uxvxa__cdh)
        _dist_exscan(xgu__umzlt, koqyp__smrn, reduce_op, typ_enum)
        return load_val_ptr(koqyp__smrn, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    veqhd__cjm = 0
    rbn__wojf = 0
    for i in range(len(recv_counts)):
        kyy__vdn = recv_counts[i]
        are__ghvv = recv_counts_nulls[i]
        fqh__ztcye = tmp_null_bytes[veqhd__cjm:veqhd__cjm + are__ghvv]
        for uytuz__dof in range(kyy__vdn):
            set_bit_to(null_bitmap_ptr, rbn__wojf, get_bit(fqh__ztcye,
                uytuz__dof))
            rbn__wojf += 1
        veqhd__cjm += are__ghvv


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            kynbj__qpkaj = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                kynbj__qpkaj, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            vymfd__oywrj = data.size
            recv_counts = gather_scalar(np.int32(vymfd__oywrj), allgather,
                root=root)
            ouvvy__wmp = recv_counts.sum()
            opc__vxex = empty_like_type(ouvvy__wmp, data)
            kdvzq__wlxgi = np.empty(1, np.int32)
            if rank == root or allgather:
                kdvzq__wlxgi = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(vymfd__oywrj), opc__vxex.ctypes,
                recv_counts.ctypes, kdvzq__wlxgi.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return opc__vxex.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            opc__vxex = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(opc__vxex)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            opc__vxex = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(opc__vxex)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            vymfd__oywrj = len(data)
            are__ghvv = vymfd__oywrj + 7 >> 3
            recv_counts = gather_scalar(np.int32(vymfd__oywrj), allgather,
                root=root)
            ouvvy__wmp = recv_counts.sum()
            opc__vxex = empty_like_type(ouvvy__wmp, data)
            kdvzq__wlxgi = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            gfmx__rrism = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                kdvzq__wlxgi = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                gfmx__rrism = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(vymfd__oywrj),
                opc__vxex._days_data.ctypes, recv_counts.ctypes,
                kdvzq__wlxgi.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._seconds_data.ctypes, np.int32(vymfd__oywrj),
                opc__vxex._seconds_data.ctypes, recv_counts.ctypes,
                kdvzq__wlxgi.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(vymfd__oywrj
                ), opc__vxex._microseconds_data.ctypes, recv_counts.ctypes,
                kdvzq__wlxgi.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(are__ghvv),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                gfmx__rrism.ctypes, hlliz__zniq, allgather, np.int32(root))
            copy_gathered_null_bytes(opc__vxex._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return opc__vxex
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, bodo.TimeArrayType)) or data in (boolean_array,
        datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            vymfd__oywrj = len(data)
            are__ghvv = vymfd__oywrj + 7 >> 3
            recv_counts = gather_scalar(np.int32(vymfd__oywrj), allgather,
                root=root)
            ouvvy__wmp = recv_counts.sum()
            opc__vxex = empty_like_type(ouvvy__wmp, data)
            kdvzq__wlxgi = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            gfmx__rrism = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                kdvzq__wlxgi = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                gfmx__rrism = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(vymfd__oywrj), opc__vxex.
                _data.ctypes, recv_counts.ctypes, kdvzq__wlxgi.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(are__ghvv),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                gfmx__rrism.ctypes, hlliz__zniq, allgather, np.int32(root))
            copy_gathered_null_bytes(opc__vxex._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return opc__vxex
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        umsci__kdnmn = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            oce__krhb = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                oce__krhb, umsci__kdnmn)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            mac__lnora = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            omt__cyt = bodo.gatherv(data._right, allgather, warn_if_rep, root)
            return bodo.libs.interval_arr_ext.init_interval_array(mac__lnora,
                omt__cyt)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            dpd__nkzmu = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            anvq__akhrx = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                anvq__akhrx, dpd__nkzmu)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        edivd__rmn = np.iinfo(np.int64).max
        aoc__cjqi = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            xzign__ouv = data._start
            azglg__mmog = data._stop
            if len(data) == 0:
                xzign__ouv = edivd__rmn
                azglg__mmog = aoc__cjqi
            xzign__ouv = bodo.libs.distributed_api.dist_reduce(xzign__ouv,
                np.int32(Reduce_Type.Min.value))
            azglg__mmog = bodo.libs.distributed_api.dist_reduce(azglg__mmog,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if xzign__ouv == edivd__rmn and azglg__mmog == aoc__cjqi:
                xzign__ouv = 0
                azglg__mmog = 0
            oqrh__pqxc = max(0, -(-(azglg__mmog - xzign__ouv) // data._step))
            if oqrh__pqxc < total_len:
                azglg__mmog = xzign__ouv + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                xzign__ouv = 0
                azglg__mmog = 0
            return bodo.hiframes.pd_index_ext.init_range_index(xzign__ouv,
                azglg__mmog, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            gho__fwbtu = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, gho__fwbtu)
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
            opc__vxex = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(opc__vxex,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        aasa__mkg = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table,
            'decode_if_dict_ary': bodo.hiframes.table.init_table}
        vtwoi__yit = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        vtwoi__yit += '  T = data\n'
        vtwoi__yit += '  T2 = init_table(T, True)\n'
        hsesf__cimrx = bodo.hiframes.table.get_init_table_output_type(data,
            True)
        qmc__tomv = (bodo.string_array_type in data.type_to_blk and bodo.
            dict_str_arr_type in data.type_to_blk)
        if qmc__tomv:
            vtwoi__yit += (bodo.hiframes.table.
                gen_str_and_dict_enc_cols_to_one_block_fn_txt(data,
                hsesf__cimrx, aasa__mkg, True))
        for lays__ddhw, mtf__yciz in data.type_to_blk.items():
            if qmc__tomv and lays__ddhw in (bodo.string_array_type, bodo.
                dict_str_arr_type):
                continue
            elif lays__ddhw == bodo.dict_str_arr_type:
                assert bodo.string_array_type in hsesf__cimrx.type_to_blk, 'Error in gatherv: If encoded string type is present in the input, then non-encoded string type should be present in the output'
                ufzbh__pijo = hsesf__cimrx.type_to_blk[bodo.string_array_type]
            else:
                assert lays__ddhw in hsesf__cimrx.type_to_blk, 'Error in gatherv: All non-encoded string types present in the input should be present in the output'
                ufzbh__pijo = hsesf__cimrx.type_to_blk[lays__ddhw]
            aasa__mkg[f'arr_inds_{mtf__yciz}'] = np.array(data.
                block_to_arr_ind[mtf__yciz], dtype=np.int64)
            vtwoi__yit += (
                f'  arr_list_{mtf__yciz} = get_table_block(T, {mtf__yciz})\n')
            vtwoi__yit += f"""  out_arr_list_{mtf__yciz} = alloc_list_like(arr_list_{mtf__yciz}, len(arr_list_{mtf__yciz}), True)
"""
            vtwoi__yit += f'  for i in range(len(arr_list_{mtf__yciz})):\n'
            vtwoi__yit += (
                f'    arr_ind_{mtf__yciz} = arr_inds_{mtf__yciz}[i]\n')
            vtwoi__yit += f"""    ensure_column_unboxed(T, arr_list_{mtf__yciz}, i, arr_ind_{mtf__yciz})
"""
            vtwoi__yit += f"""    out_arr_{mtf__yciz} = bodo.gatherv(arr_list_{mtf__yciz}[i], allgather, warn_if_rep, root)
"""
            vtwoi__yit += (
                f'    out_arr_list_{mtf__yciz}[i] = out_arr_{mtf__yciz}\n')
            vtwoi__yit += (
                f'  T2 = set_table_block(T2, out_arr_list_{mtf__yciz}, {ufzbh__pijo})\n'
                )
        vtwoi__yit += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        vtwoi__yit += f'  T2 = set_table_len(T2, length)\n'
        vtwoi__yit += f'  return T2\n'
        hcctx__yian = {}
        exec(vtwoi__yit, aasa__mkg, hcctx__yian)
        lhqvk__ziiu = hcctx__yian['impl_table']
        return lhqvk__ziiu
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        xwaa__sbxkf = len(data.columns)
        if xwaa__sbxkf == 0:
            ihsqh__usm = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                smly__kjjss = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    smly__kjjss, ihsqh__usm)
            return impl
        zgq__rwkjp = ', '.join(f'g_data_{i}' for i in range(xwaa__sbxkf))
        vtwoi__yit = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            byjdl__saz = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            zgq__rwkjp = 'T2'
            vtwoi__yit += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            vtwoi__yit += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(xwaa__sbxkf):
                vtwoi__yit += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                vtwoi__yit += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        vtwoi__yit += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        vtwoi__yit += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        vtwoi__yit += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(zgq__rwkjp))
        hcctx__yian = {}
        aasa__mkg = {'bodo': bodo,
            '__col_name_meta_value_gatherv_with_cols': ColNamesMetaType(
            data.columns)}
        exec(vtwoi__yit, aasa__mkg, hcctx__yian)
        wcuy__rxl = hcctx__yian['impl_df']
        return wcuy__rxl
    if isinstance(data, ArrayItemArrayType):
        sfmbv__ldwa = np.int32(numba_to_c_type(types.int32))
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            eaks__lablc = bodo.libs.array_item_arr_ext.get_offsets(data)
            qrb__rnb = bodo.libs.array_item_arr_ext.get_data(data)
            qrb__rnb = qrb__rnb[:eaks__lablc[-1]]
            grs__imug = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            vymfd__oywrj = len(data)
            hop__svknf = np.empty(vymfd__oywrj, np.uint32)
            are__ghvv = vymfd__oywrj + 7 >> 3
            for i in range(vymfd__oywrj):
                hop__svknf[i] = eaks__lablc[i + 1] - eaks__lablc[i]
            recv_counts = gather_scalar(np.int32(vymfd__oywrj), allgather,
                root=root)
            ouvvy__wmp = recv_counts.sum()
            kdvzq__wlxgi = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            gfmx__rrism = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                kdvzq__wlxgi = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for uixt__lshxv in range(len(recv_counts)):
                    recv_counts_nulls[uixt__lshxv] = recv_counts[uixt__lshxv
                        ] + 7 >> 3
                gfmx__rrism = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            azxy__htuiu = np.empty(ouvvy__wmp + 1, np.uint32)
            qptum__cbim = bodo.gatherv(qrb__rnb, allgather, warn_if_rep, root)
            its__nyhiq = np.empty(ouvvy__wmp + 7 >> 3, np.uint8)
            c_gatherv(hop__svknf.ctypes, np.int32(vymfd__oywrj),
                azxy__htuiu.ctypes, recv_counts.ctypes, kdvzq__wlxgi.ctypes,
                sfmbv__ldwa, allgather, np.int32(root))
            c_gatherv(grs__imug.ctypes, np.int32(are__ghvv), tmp_null_bytes
                .ctypes, recv_counts_nulls.ctypes, gfmx__rrism.ctypes,
                hlliz__zniq, allgather, np.int32(root))
            dummy_use(data)
            tzl__mtjst = np.empty(ouvvy__wmp + 1, np.uint64)
            convert_len_arr_to_offset(azxy__htuiu.ctypes, tzl__mtjst.ctypes,
                ouvvy__wmp)
            copy_gathered_null_bytes(its__nyhiq.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                ouvvy__wmp, qptum__cbim, tzl__mtjst, its__nyhiq)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        mwwy__cmi = data.names
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            gbkqw__pgscl = bodo.libs.struct_arr_ext.get_data(data)
            zlca__yrcqm = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            nwn__nusaw = bodo.gatherv(gbkqw__pgscl, allgather=allgather,
                root=root)
            rank = bodo.libs.distributed_api.get_rank()
            vymfd__oywrj = len(data)
            are__ghvv = vymfd__oywrj + 7 >> 3
            recv_counts = gather_scalar(np.int32(vymfd__oywrj), allgather,
                root=root)
            ouvvy__wmp = recv_counts.sum()
            pvqq__pwqsj = np.empty(ouvvy__wmp + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            gfmx__rrism = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                gfmx__rrism = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(zlca__yrcqm.ctypes, np.int32(are__ghvv),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                gfmx__rrism.ctypes, hlliz__zniq, allgather, np.int32(root))
            copy_gathered_null_bytes(pvqq__pwqsj.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(nwn__nusaw,
                pvqq__pwqsj, mwwy__cmi)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            opc__vxex = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(opc__vxex)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            opc__vxex = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(opc__vxex)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            opc__vxex = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(opc__vxex)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            opc__vxex = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            lfm__azs = bodo.gatherv(data.indices, allgather, warn_if_rep, root)
            vnhf__vsp = bodo.gatherv(data.indptr, allgather, warn_if_rep, root)
            vdaf__nso = gather_scalar(data.shape[0], allgather, root=root)
            ufbxa__nsoo = vdaf__nso.sum()
            xwaa__sbxkf = bodo.libs.distributed_api.dist_reduce(data.shape[
                1], np.int32(Reduce_Type.Max.value))
            muwa__sziy = np.empty(ufbxa__nsoo + 1, np.int64)
            lfm__azs = lfm__azs.astype(np.int64)
            muwa__sziy[0] = 0
            jgvxq__onood = 1
            ovpf__nui = 0
            for manc__puej in vdaf__nso:
                for apjtm__avzuf in range(manc__puej):
                    zwc__wkeep = vnhf__vsp[ovpf__nui + 1] - vnhf__vsp[ovpf__nui
                        ]
                    muwa__sziy[jgvxq__onood] = muwa__sziy[jgvxq__onood - 1
                        ] + zwc__wkeep
                    jgvxq__onood += 1
                    ovpf__nui += 1
                ovpf__nui += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(opc__vxex,
                lfm__azs, muwa__sziy, (ufbxa__nsoo, xwaa__sbxkf))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        vtwoi__yit = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        vtwoi__yit += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        hcctx__yian = {}
        exec(vtwoi__yit, {'bodo': bodo}, hcctx__yian)
        asvbw__welpa = hcctx__yian['impl_tuple']
        return asvbw__welpa
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as zgwqf__gchp:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        vtwoi__yit = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        yiyq__squk = ', '.join([f"'{dpd__nkzmu}'" for dpd__nkzmu in data.names]
            )
        rzax__xmyu = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        vtwoi__yit += f"""  return bodosql.context_ext.init_sql_context(({yiyq__squk}, ), ({rzax__xmyu}, ), data.catalog)
"""
        hcctx__yian = {}
        exec(vtwoi__yit, {'bodo': bodo, 'bodosql': bodosql}, hcctx__yian)
        ttc__tqlhc = hcctx__yian['impl_bodosql_context']
        return ttc__tqlhc
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as zgwqf__gchp:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        vtwoi__yit = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        vtwoi__yit += f'  return data\n'
        hcctx__yian = {}
        exec(vtwoi__yit, {}, hcctx__yian)
        ecwz__fgkp = hcctx__yian['impl_table_path']
        return ecwz__fgkp
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    vtwoi__yit = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    vtwoi__yit += '    if random:\n'
    vtwoi__yit += '        if random_seed is None:\n'
    vtwoi__yit += '            random = 1\n'
    vtwoi__yit += '        else:\n'
    vtwoi__yit += '            random = 2\n'
    vtwoi__yit += '    if random_seed is None:\n'
    vtwoi__yit += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        zqrri__bzp = data
        xwaa__sbxkf = len(zqrri__bzp.columns)
        for i in range(xwaa__sbxkf):
            vtwoi__yit += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        vtwoi__yit += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        zgq__rwkjp = ', '.join(f'data_{i}' for i in range(xwaa__sbxkf))
        vtwoi__yit += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(whu__rqo) for
            whu__rqo in range(xwaa__sbxkf))))
        vtwoi__yit += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        vtwoi__yit += '    if dests is None:\n'
        vtwoi__yit += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        vtwoi__yit += '    else:\n'
        vtwoi__yit += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for zalk__ekk in range(xwaa__sbxkf):
            vtwoi__yit += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(zalk__ekk))
        vtwoi__yit += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(xwaa__sbxkf))
        vtwoi__yit += '    delete_table(out_table)\n'
        vtwoi__yit += '    if parallel:\n'
        vtwoi__yit += '        delete_table(table_total)\n'
        zgq__rwkjp = ', '.join('out_arr_{}'.format(i) for i in range(
            xwaa__sbxkf))
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        vtwoi__yit += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(zgq__rwkjp, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        vtwoi__yit += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        vtwoi__yit += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        vtwoi__yit += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        vtwoi__yit += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        vtwoi__yit += '    if dests is None:\n'
        vtwoi__yit += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        vtwoi__yit += '    else:\n'
        vtwoi__yit += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        vtwoi__yit += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        vtwoi__yit += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        vtwoi__yit += '    delete_table(out_table)\n'
        vtwoi__yit += '    if parallel:\n'
        vtwoi__yit += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        vtwoi__yit += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        vtwoi__yit += '    if not parallel:\n'
        vtwoi__yit += '        return data\n'
        vtwoi__yit += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        vtwoi__yit += '    if dests is None:\n'
        vtwoi__yit += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        vtwoi__yit += '    elif bodo.get_rank() not in dests:\n'
        vtwoi__yit += '        dim0_local_size = 0\n'
        vtwoi__yit += '    else:\n'
        vtwoi__yit += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        vtwoi__yit += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        vtwoi__yit += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        vtwoi__yit += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        vtwoi__yit += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        vtwoi__yit += '    if dests is None:\n'
        vtwoi__yit += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        vtwoi__yit += '    else:\n'
        vtwoi__yit += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        vtwoi__yit += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        vtwoi__yit += '    delete_table(out_table)\n'
        vtwoi__yit += '    if parallel:\n'
        vtwoi__yit += '        delete_table(table_total)\n'
        vtwoi__yit += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    hcctx__yian = {}
    aasa__mkg = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.array.
        array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        aasa__mkg.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(zqrri__bzp.columns)})
    exec(vtwoi__yit, aasa__mkg, hcctx__yian)
    impl = hcctx__yian['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    vtwoi__yit = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        vtwoi__yit += '    if seed is None:\n'
        vtwoi__yit += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        vtwoi__yit += '    np.random.seed(seed)\n'
        vtwoi__yit += '    if not parallel:\n'
        vtwoi__yit += '        data = data.copy()\n'
        vtwoi__yit += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            vtwoi__yit += '        data = data[:n_samples]\n'
        vtwoi__yit += '        return data\n'
        vtwoi__yit += '    else:\n'
        vtwoi__yit += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        vtwoi__yit += '        permutation = np.arange(dim0_global_size)\n'
        vtwoi__yit += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            vtwoi__yit += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            vtwoi__yit += '        n_samples = dim0_global_size\n'
        vtwoi__yit += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        vtwoi__yit += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        vtwoi__yit += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        vtwoi__yit += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        vtwoi__yit += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        vtwoi__yit += '        return output\n'
    else:
        vtwoi__yit += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            vtwoi__yit += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            vtwoi__yit += '    output = output[:local_n_samples]\n'
        vtwoi__yit += '    return output\n'
    hcctx__yian = {}
    exec(vtwoi__yit, {'np': np, 'bodo': bodo}, hcctx__yian)
    impl = hcctx__yian['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    mmo__olm = np.empty(sendcounts_nulls.sum(), np.uint8)
    veqhd__cjm = 0
    rbn__wojf = 0
    for wip__pmdts in range(len(sendcounts)):
        kyy__vdn = sendcounts[wip__pmdts]
        are__ghvv = sendcounts_nulls[wip__pmdts]
        fqh__ztcye = mmo__olm[veqhd__cjm:veqhd__cjm + are__ghvv]
        for uytuz__dof in range(kyy__vdn):
            set_bit_to_arr(fqh__ztcye, uytuz__dof, get_bit_bitmap(
                null_bitmap_ptr, rbn__wojf))
            rbn__wojf += 1
        veqhd__cjm += are__ghvv
    return mmo__olm


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    xnwzv__pfd = MPI.COMM_WORLD
    data = xnwzv__pfd.bcast(data, root)
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
    yip__fpx = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    oxgru__ojrgn = (0,) * yip__fpx

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        djjw__suzp = np.ascontiguousarray(data)
        xzbp__laly = data.ctypes
        xlek__lehlo = oxgru__ojrgn
        if rank == MPI_ROOT:
            xlek__lehlo = djjw__suzp.shape
        xlek__lehlo = bcast_tuple(xlek__lehlo)
        aey__xqocs = get_tuple_prod(xlek__lehlo[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            xlek__lehlo[0])
        send_counts *= aey__xqocs
        vymfd__oywrj = send_counts[rank]
        cphw__oky = np.empty(vymfd__oywrj, dtype)
        kdvzq__wlxgi = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(xzbp__laly, send_counts.ctypes, kdvzq__wlxgi.ctypes,
            cphw__oky.ctypes, np.int32(vymfd__oywrj), np.int32(typ_val))
        return cphw__oky.reshape((-1,) + xlek__lehlo[1:])
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
        ukqw__gys = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], ukqw__gys)
    if isinstance(dtype, FloatingArrayType):
        ukqw__gys = 'Float{}'.format(dtype.dtype.bitwidth)
        return pd.array([3.0], ukqw__gys)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        dpd__nkzmu = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=dpd__nkzmu)
        hhd__ffsn = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(hhd__ffsn)
        return pd.Index(arr, name=dpd__nkzmu)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        dpd__nkzmu = _get_name_value_for_type(dtype.name_typ)
        mwwy__cmi = tuple(_get_name_value_for_type(t) for t in dtype.names_typ)
        bqk__ncnbc = tuple(get_value_for_type(t) for t in dtype.array_types)
        bqk__ncnbc = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in bqk__ncnbc)
        val = pd.MultiIndex.from_arrays(bqk__ncnbc, names=mwwy__cmi)
        val.name = dpd__nkzmu
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        dpd__nkzmu = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=dpd__nkzmu)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        bqk__ncnbc = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({dpd__nkzmu: arr for dpd__nkzmu, arr in zip(
            dtype.columns, bqk__ncnbc)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        hhd__ffsn = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(hhd__ffsn[0], hhd__ffsn
            [0])])
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
        sfmbv__ldwa = np.int32(numba_to_c_type(types.int32))
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            zcuua__nqyu = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            zcuua__nqyu = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        vtwoi__yit = f"""def impl(
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
            recv_arr = {zcuua__nqyu}(n_loc, n_loc_char)

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
        hcctx__yian = dict()
        exec(vtwoi__yit, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            sfmbv__ldwa, 'char_typ_enum': hlliz__zniq,
            'decode_if_dict_array': decode_if_dict_array}, hcctx__yian)
        impl = hcctx__yian['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        sfmbv__ldwa = np.int32(numba_to_c_type(types.int32))
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            etlly__gjwrx = bodo.libs.array_item_arr_ext.get_offsets(data)
            nfgi__qgrh = bodo.libs.array_item_arr_ext.get_data(data)
            nfgi__qgrh = nfgi__qgrh[:etlly__gjwrx[-1]]
            wtlgk__izdbb = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            wswi__hhiz = bcast_scalar(len(data))
            vjm__zygtf = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                vjm__zygtf[i] = etlly__gjwrx[i + 1] - etlly__gjwrx[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                wswi__hhiz)
            kdvzq__wlxgi = bodo.ir.join.calc_disp(send_counts)
            pmfh__msldw = np.empty(n_pes, np.int32)
            if rank == 0:
                etjqf__xnn = 0
                for i in range(n_pes):
                    xry__sbebv = 0
                    for apjtm__avzuf in range(send_counts[i]):
                        xry__sbebv += vjm__zygtf[etjqf__xnn]
                        etjqf__xnn += 1
                    pmfh__msldw[i] = xry__sbebv
            bcast(pmfh__msldw)
            odyr__lvhbt = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                odyr__lvhbt[i] = send_counts[i] + 7 >> 3
            gfmx__rrism = bodo.ir.join.calc_disp(odyr__lvhbt)
            vymfd__oywrj = send_counts[rank]
            elull__srhb = np.empty(vymfd__oywrj + 1, np_offset_type)
            rqa__tsujn = bodo.libs.distributed_api.scatterv_impl(nfgi__qgrh,
                pmfh__msldw)
            zpc__wbg = vymfd__oywrj + 7 >> 3
            mick__lvar = np.empty(zpc__wbg, np.uint8)
            iwps__wpwm = np.empty(vymfd__oywrj, np.uint32)
            c_scatterv(vjm__zygtf.ctypes, send_counts.ctypes, kdvzq__wlxgi.
                ctypes, iwps__wpwm.ctypes, np.int32(vymfd__oywrj), sfmbv__ldwa)
            convert_len_arr_to_offset(iwps__wpwm.ctypes, elull__srhb.ctypes,
                vymfd__oywrj)
            mivsh__gib = get_scatter_null_bytes_buff(wtlgk__izdbb.ctypes,
                send_counts, odyr__lvhbt)
            c_scatterv(mivsh__gib.ctypes, odyr__lvhbt.ctypes, gfmx__rrism.
                ctypes, mick__lvar.ctypes, np.int32(zpc__wbg), hlliz__zniq)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                vymfd__oywrj, rqa__tsujn, elull__srhb, mick__lvar)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or data in (boolean_array, datetime_date_array_type):
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            ush__bns = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, FloatingArrayType):
            ush__bns = bodo.libs.float_arr_ext.init_float_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            ush__bns = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            ush__bns = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            ush__bns = bodo.hiframes.datetime_date_ext.init_datetime_date_array

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            djjw__suzp = data._data
            zlca__yrcqm = data._null_bitmap
            pflc__pqo = len(djjw__suzp)
            tltm__ewk = _scatterv_np(djjw__suzp, send_counts)
            wswi__hhiz = bcast_scalar(pflc__pqo)
            aak__cknq = len(tltm__ewk) + 7 >> 3
            nwtc__nnw = np.empty(aak__cknq, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                wswi__hhiz)
            odyr__lvhbt = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                odyr__lvhbt[i] = send_counts[i] + 7 >> 3
            gfmx__rrism = bodo.ir.join.calc_disp(odyr__lvhbt)
            mivsh__gib = get_scatter_null_bytes_buff(zlca__yrcqm.ctypes,
                send_counts, odyr__lvhbt)
            c_scatterv(mivsh__gib.ctypes, odyr__lvhbt.ctypes, gfmx__rrism.
                ctypes, nwtc__nnw.ctypes, np.int32(aak__cknq), hlliz__zniq)
            return ush__bns(tltm__ewk, nwtc__nnw)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            kacin__bys = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            ewf__nzpmb = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(kacin__bys,
                ewf__nzpmb)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            xzign__ouv = data._start
            azglg__mmog = data._stop
            ulqet__nreww = data._step
            dpd__nkzmu = data._name
            dpd__nkzmu = bcast_scalar(dpd__nkzmu)
            xzign__ouv = bcast_scalar(xzign__ouv)
            azglg__mmog = bcast_scalar(azglg__mmog)
            ulqet__nreww = bcast_scalar(ulqet__nreww)
            rllol__ljggl = bodo.libs.array_kernels.calc_nitems(xzign__ouv,
                azglg__mmog, ulqet__nreww)
            chunk_start = bodo.libs.distributed_api.get_start(rllol__ljggl,
                n_pes, rank)
            ybg__wxrl = bodo.libs.distributed_api.get_node_portion(rllol__ljggl
                , n_pes, rank)
            kvvr__ekdjq = xzign__ouv + ulqet__nreww * chunk_start
            xwb__srui = xzign__ouv + ulqet__nreww * (chunk_start + ybg__wxrl)
            xwb__srui = min(xwb__srui, azglg__mmog)
            return bodo.hiframes.pd_index_ext.init_range_index(kvvr__ekdjq,
                xwb__srui, ulqet__nreww, dpd__nkzmu)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        gho__fwbtu = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            djjw__suzp = data._data
            dpd__nkzmu = data._name
            dpd__nkzmu = bcast_scalar(dpd__nkzmu)
            arr = bodo.libs.distributed_api.scatterv_impl(djjw__suzp,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                dpd__nkzmu, gho__fwbtu)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            djjw__suzp = data._data
            dpd__nkzmu = data._name
            dpd__nkzmu = bcast_scalar(dpd__nkzmu)
            arr = bodo.libs.distributed_api.scatterv_impl(djjw__suzp,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, dpd__nkzmu)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            opc__vxex = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            dpd__nkzmu = bcast_scalar(data._name)
            mwwy__cmi = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(opc__vxex,
                mwwy__cmi, dpd__nkzmu)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            dpd__nkzmu = bodo.hiframes.pd_series_ext.get_series_name(data)
            meq__hsbnx = bcast_scalar(dpd__nkzmu)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            anvq__akhrx = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                anvq__akhrx, meq__hsbnx)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        xwaa__sbxkf = len(data.columns)
        oubln__qof = ColNamesMetaType(data.columns)
        vtwoi__yit = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        if data.is_table_format:
            vtwoi__yit += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            vtwoi__yit += """  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)
"""
            zgq__rwkjp = 'g_table'
        else:
            for i in range(xwaa__sbxkf):
                vtwoi__yit += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                vtwoi__yit += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            zgq__rwkjp = ', '.join(f'g_data_{i}' for i in range(xwaa__sbxkf))
        vtwoi__yit += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        vtwoi__yit += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        vtwoi__yit += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({zgq__rwkjp},), g_index, __col_name_meta_scaterv_impl)
"""
        hcctx__yian = {}
        exec(vtwoi__yit, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            oubln__qof}, hcctx__yian)
        wcuy__rxl = hcctx__yian['impl_df']
        return wcuy__rxl
    if isinstance(data, bodo.TableType):
        vtwoi__yit = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        vtwoi__yit += '  T = data\n'
        vtwoi__yit += '  T2 = init_table(T, False)\n'
        vtwoi__yit += '  l = 0\n'
        aasa__mkg = {}
        for glg__tjyl in data.type_to_blk.values():
            aasa__mkg[f'arr_inds_{glg__tjyl}'] = np.array(data.
                block_to_arr_ind[glg__tjyl], dtype=np.int64)
            vtwoi__yit += (
                f'  arr_list_{glg__tjyl} = get_table_block(T, {glg__tjyl})\n')
            vtwoi__yit += f"""  out_arr_list_{glg__tjyl} = alloc_list_like(arr_list_{glg__tjyl}, len(arr_list_{glg__tjyl}), False)
"""
            vtwoi__yit += f'  for i in range(len(arr_list_{glg__tjyl})):\n'
            vtwoi__yit += (
                f'    arr_ind_{glg__tjyl} = arr_inds_{glg__tjyl}[i]\n')
            vtwoi__yit += f"""    ensure_column_unboxed(T, arr_list_{glg__tjyl}, i, arr_ind_{glg__tjyl})
"""
            vtwoi__yit += f"""    out_arr_{glg__tjyl} = bodo.libs.distributed_api.scatterv_impl(arr_list_{glg__tjyl}[i], send_counts)
"""
            vtwoi__yit += (
                f'    out_arr_list_{glg__tjyl}[i] = out_arr_{glg__tjyl}\n')
            vtwoi__yit += f'    l = len(out_arr_{glg__tjyl})\n'
            vtwoi__yit += (
                f'  T2 = set_table_block(T2, out_arr_list_{glg__tjyl}, {glg__tjyl})\n'
                )
        vtwoi__yit += f'  T2 = set_table_len(T2, l)\n'
        vtwoi__yit += f'  return T2\n'
        aasa__mkg.update({'bodo': bodo, 'init_table': bodo.hiframes.table.
            init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        hcctx__yian = {}
        exec(vtwoi__yit, aasa__mkg, hcctx__yian)
        return hcctx__yian['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                nqzh__yhigo = data._data
                bodo.libs.distributed_api.bcast_scalar(len(nqzh__yhigo))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(nqzh__yhigo)))
            else:
                oqrh__pqxc = bodo.libs.distributed_api.bcast_scalar(0)
                yljb__pbauc = bodo.libs.distributed_api.bcast_scalar(0)
                nqzh__yhigo = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    oqrh__pqxc, yljb__pbauc)
            bodo.libs.distributed_api.bcast(nqzh__yhigo)
            sqfvu__iboko = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(nqzh__yhigo,
                sqfvu__iboko, True, data._has_deduped_local_dictionary)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            kynbj__qpkaj = bodo.libs.distributed_api.scatterv_impl(data.
                codes, send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                kynbj__qpkaj, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        vtwoi__yit = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        vtwoi__yit += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        hcctx__yian = {}
        exec(vtwoi__yit, {'bodo': bodo}, hcctx__yian)
        asvbw__welpa = hcctx__yian['impl_tuple']
        return asvbw__welpa
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
        byxu__dys = np.int32(numba_to_c_type(offset_type))
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            vymfd__oywrj = len(data)
            wcqwb__bdpng = num_total_chars(data)
            assert vymfd__oywrj < INT_MAX
            assert wcqwb__bdpng < INT_MAX
            rhpcx__giido = get_offset_ptr(data)
            xzbp__laly = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            are__ghvv = vymfd__oywrj + 7 >> 3
            c_bcast(rhpcx__giido, np.int32(vymfd__oywrj + 1), byxu__dys, np
                .array([-1]).ctypes, 0, np.int32(root))
            c_bcast(xzbp__laly, np.int32(wcqwb__bdpng), hlliz__zniq, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(are__ghvv), hlliz__zniq, np.
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
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                vecy__auo = 0
                hids__gogwc = np.empty(0, np.uint8).ctypes
            else:
                hids__gogwc, vecy__auo = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            vecy__auo = bodo.libs.distributed_api.bcast_scalar(vecy__auo, root)
            if rank != root:
                xpd__cdtv = np.empty(vecy__auo + 1, np.uint8)
                xpd__cdtv[vecy__auo] = 0
                hids__gogwc = xpd__cdtv.ctypes
            c_bcast(hids__gogwc, np.int32(vecy__auo), hlliz__zniq, np.array
                ([-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(hids__gogwc, vecy__auo)
        return impl_str
    typ_val = numba_to_c_type(val)
    vtwoi__yit = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    hcctx__yian = {}
    exec(vtwoi__yit, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, hcctx__yian)
    ebzmd__olpu = hcctx__yian['bcast_scalar_impl']
    return ebzmd__olpu


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple
        ), 'Internal Error: Argument to bcast tuple must be of type tuple'
    mizbi__jhtwk = len(val)
    vtwoi__yit = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    vtwoi__yit += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(mizbi__jhtwk
        )), ',' if mizbi__jhtwk else '')
    hcctx__yian = {}
    exec(vtwoi__yit, {'bcast_scalar': bcast_scalar}, hcctx__yian)
    kbfl__cntzq = hcctx__yian['bcast_tuple_impl']
    return kbfl__cntzq


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            vymfd__oywrj = bcast_scalar(len(arr), root)
            ekw__eai = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(vymfd__oywrj, ekw__eai)
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
            kvvr__ekdjq = max(arr_start, slice_index.start) - arr_start
            xwb__srui = max(slice_index.stop - arr_start, 0)
            return slice(kvvr__ekdjq, xwb__srui)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            xzign__ouv = slice_index.start
            ulqet__nreww = slice_index.step
            sed__qmuz = (0 if ulqet__nreww == 1 or xzign__ouv > arr_start else
                abs(ulqet__nreww - arr_start % ulqet__nreww) % ulqet__nreww)
            kvvr__ekdjq = max(arr_start, slice_index.start
                ) - arr_start + sed__qmuz
            xwb__srui = max(slice_index.stop - arr_start, 0)
            return slice(kvvr__ekdjq, xwb__srui, ulqet__nreww)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        yij__pwmsz = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[yij__pwmsz])
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
        oxw__qqhf = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        hlliz__zniq = np.int32(numba_to_c_type(types.uint8))
        zowqc__prsdm = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            bvwf__sddve = np.int32(10)
            tag = np.int32(11)
            pos__sec = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                qrb__rnb = arr._data
                vzr__fviba = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    qrb__rnb, ind)
                xkwg__coacq = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    qrb__rnb, ind + 1)
                length = xkwg__coacq - vzr__fviba
                krvv__glf = qrb__rnb[ind]
                pos__sec[0] = length
                isend(pos__sec, np.int32(1), root, bvwf__sddve, True)
                isend(krvv__glf, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                zowqc__prsdm, oxw__qqhf, 0, 1)
            oqrh__pqxc = 0
            if rank == root:
                oqrh__pqxc = recv(np.int64, ANY_SOURCE, bvwf__sddve)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    zowqc__prsdm, oxw__qqhf, oqrh__pqxc, 1)
                xzbp__laly = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(xzbp__laly, np.int32(oqrh__pqxc), hlliz__zniq,
                    ANY_SOURCE, tag)
            dummy_use(pos__sec)
            oqrh__pqxc = bcast_scalar(oqrh__pqxc)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    zowqc__prsdm, oxw__qqhf, oqrh__pqxc, 1)
            xzbp__laly = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(xzbp__laly, np.int32(oqrh__pqxc), hlliz__zniq, np.array
                ([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, oqrh__pqxc)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        fbooy__divy = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, fbooy__divy)
            if arr_start <= ind < arr_start + len(arr):
                kynbj__qpkaj = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = kynbj__qpkaj[ind - arr_start]
                send_arr = np.full(1, data, fbooy__divy)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = fbooy__divy(-1)
            if rank == root:
                val = recv(fbooy__divy, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            pul__tmpd = arr.dtype.categories[max(val, 0)]
            return pul__tmpd
        return cat_getitem_impl
    if isinstance(arr, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        edlji__mkox = arr.tz

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
                edlji__mkox)
        return tz_aware_getitem_impl
    usha__hqx = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, usha__hqx)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, usha__hqx)[0]
        if rank == root:
            val = recv(usha__hqx, ANY_SOURCE, tag)
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
        voeo__jwum = np.empty(n_pes, np.int64)
        wxp__oqne = np.empty(n_pes, np.int8)
        val = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        sbn__hwxz = 1
        if len(A) != 0:
            val = A[-1]
            sbn__hwxz = 0
        allgather(voeo__jwum, np.int64(val))
        allgather(wxp__oqne, sbn__hwxz)
        for i, sbn__hwxz in enumerate(wxp__oqne):
            if sbn__hwxz and i != 0:
                voeo__jwum[i] = voeo__jwum[i - 1]
        return voeo__jwum
    return impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    simv__lyq = get_type_enum(out_data)
    assert typ_enum == simv__lyq
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
    vtwoi__yit = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        vtwoi__yit += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    vtwoi__yit += '  return\n'
    hcctx__yian = {}
    exec(vtwoi__yit, {'alltoallv': alltoallv}, hcctx__yian)
    zxf__sxg = hcctx__yian['f']
    return zxf__sxg


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    xzign__ouv = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return xzign__ouv, count


@numba.njit
def get_start(total_size, pes, rank):
    lcrwl__rofpq = total_size % pes
    odqq__ncjjy = (total_size - lcrwl__rofpq) // pes
    return rank * odqq__ncjjy + min(rank, lcrwl__rofpq)


@numba.njit
def get_end(total_size, pes, rank):
    lcrwl__rofpq = total_size % pes
    odqq__ncjjy = (total_size - lcrwl__rofpq) // pes
    return (rank + 1) * odqq__ncjjy + min(rank + 1, lcrwl__rofpq)


@numba.njit
def get_node_portion(total_size, pes, rank):
    lcrwl__rofpq = total_size % pes
    odqq__ncjjy = (total_size - lcrwl__rofpq) // pes
    if rank < lcrwl__rofpq:
        return odqq__ncjjy + 1
    else:
        return odqq__ncjjy


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    uxvxa__cdh = in_arr.dtype(0)
    slgdz__pxwlo = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        xry__sbebv = uxvxa__cdh
        for yrf__drfsj in np.nditer(in_arr):
            xry__sbebv += yrf__drfsj.item()
        wtb__ojq = dist_exscan(xry__sbebv, slgdz__pxwlo)
        for i in range(in_arr.size):
            wtb__ojq += in_arr[i]
            out_arr[i] = wtb__ojq
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    qapz__ttut = in_arr.dtype(1)
    slgdz__pxwlo = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        xry__sbebv = qapz__ttut
        for yrf__drfsj in np.nditer(in_arr):
            xry__sbebv *= yrf__drfsj.item()
        wtb__ojq = dist_exscan(xry__sbebv, slgdz__pxwlo)
        if get_rank() == 0:
            wtb__ojq = qapz__ttut
        for i in range(in_arr.size):
            wtb__ojq *= in_arr[i]
            out_arr[i] = wtb__ojq
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        qapz__ttut = np.finfo(in_arr.dtype(1).dtype).max
    else:
        qapz__ttut = np.iinfo(in_arr.dtype(1).dtype).max
    slgdz__pxwlo = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        xry__sbebv = qapz__ttut
        for yrf__drfsj in np.nditer(in_arr):
            xry__sbebv = min(xry__sbebv, yrf__drfsj.item())
        wtb__ojq = dist_exscan(xry__sbebv, slgdz__pxwlo)
        if get_rank() == 0:
            wtb__ojq = qapz__ttut
        for i in range(in_arr.size):
            wtb__ojq = min(wtb__ojq, in_arr[i])
            out_arr[i] = wtb__ojq
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        qapz__ttut = np.finfo(in_arr.dtype(1).dtype).min
    else:
        qapz__ttut = np.iinfo(in_arr.dtype(1).dtype).min
    qapz__ttut = in_arr.dtype(1)
    slgdz__pxwlo = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        xry__sbebv = qapz__ttut
        for yrf__drfsj in np.nditer(in_arr):
            xry__sbebv = max(xry__sbebv, yrf__drfsj.item())
        wtb__ojq = dist_exscan(xry__sbebv, slgdz__pxwlo)
        if get_rank() == 0:
            wtb__ojq = qapz__ttut
        for i in range(in_arr.size):
            wtb__ojq = max(wtb__ojq, in_arr[i])
            out_arr[i] = wtb__ojq
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    jlzv__jxhd = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), jlzv__jxhd)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    kxa__pjd = args[0]
    if equiv_set.has_shape(kxa__pjd):
        return ArrayAnalysis.AnalyzeResult(shape=kxa__pjd, pre=[])
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
    dui__byxoo = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for 
        i, cdmj__lhlqw in enumerate(args) if is_array_typ(cdmj__lhlqw) or
        isinstance(cdmj__lhlqw, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    vtwoi__yit = f"""def impl(*args):
    if {dui__byxoo} or bodo.get_rank() == 0:
        print(*args)"""
    hcctx__yian = {}
    exec(vtwoi__yit, globals(), hcctx__yian)
    impl = hcctx__yian['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        bdrkm__djux = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        vtwoi__yit = 'def f(req, cond=True):\n'
        vtwoi__yit += f'  return {bdrkm__djux}\n'
        hcctx__yian = {}
        exec(vtwoi__yit, {'_wait': _wait}, hcctx__yian)
        impl = hcctx__yian['f']
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
        lcrwl__rofpq = 1
        for a in t:
            lcrwl__rofpq *= a
        return lcrwl__rofpq
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    oae__nyoo = np.ascontiguousarray(in_arr)
    fpu__rbox = get_tuple_prod(oae__nyoo.shape[1:])
    kdg__aipkd = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        kra__lzzkv = np.array(dest_ranks, dtype=np.int32)
    else:
        kra__lzzkv = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, oae__nyoo.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * kdg__aipkd, dtype_size * fpu__rbox, len(
        kra__lzzkv), kra__lzzkv.ctypes)
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
    kfnpi__dhk = np.ascontiguousarray(rhs)
    ssmhr__ltmc = get_tuple_prod(kfnpi__dhk.shape[1:])
    yfurf__vysre = dtype_size * ssmhr__ltmc
    permutation_array_index(lhs.ctypes, lhs_len, yfurf__vysre, kfnpi__dhk.
        ctypes, kfnpi__dhk.shape[0], p.ctypes, p_len, n_samples)
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
        vtwoi__yit = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        hcctx__yian = {}
        exec(vtwoi__yit, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, hcctx__yian)
        ebzmd__olpu = hcctx__yian['bcast_scalar_impl']
        return ebzmd__olpu
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        xwaa__sbxkf = len(data.columns)
        zgq__rwkjp = ', '.join('g_data_{}'.format(i) for i in range(
            xwaa__sbxkf))
        pxoq__tfp = ColNamesMetaType(data.columns)
        vtwoi__yit = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(xwaa__sbxkf):
            vtwoi__yit += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            vtwoi__yit += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        vtwoi__yit += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        vtwoi__yit += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        vtwoi__yit += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(zgq__rwkjp))
        hcctx__yian = {}
        exec(vtwoi__yit, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            pxoq__tfp}, hcctx__yian)
        wcuy__rxl = hcctx__yian['impl_df']
        return wcuy__rxl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            xzign__ouv = data._start
            azglg__mmog = data._stop
            ulqet__nreww = data._step
            dpd__nkzmu = data._name
            dpd__nkzmu = bcast_scalar(dpd__nkzmu, root)
            xzign__ouv = bcast_scalar(xzign__ouv, root)
            azglg__mmog = bcast_scalar(azglg__mmog, root)
            ulqet__nreww = bcast_scalar(ulqet__nreww, root)
            rllol__ljggl = bodo.libs.array_kernels.calc_nitems(xzign__ouv,
                azglg__mmog, ulqet__nreww)
            chunk_start = bodo.libs.distributed_api.get_start(rllol__ljggl,
                n_pes, rank)
            ybg__wxrl = bodo.libs.distributed_api.get_node_portion(rllol__ljggl
                , n_pes, rank)
            kvvr__ekdjq = xzign__ouv + ulqet__nreww * chunk_start
            xwb__srui = xzign__ouv + ulqet__nreww * (chunk_start + ybg__wxrl)
            xwb__srui = min(xwb__srui, azglg__mmog)
            return bodo.hiframes.pd_index_ext.init_range_index(kvvr__ekdjq,
                xwb__srui, ulqet__nreww, dpd__nkzmu)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            djjw__suzp = data._data
            dpd__nkzmu = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(djjw__suzp,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, dpd__nkzmu)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            dpd__nkzmu = bodo.hiframes.pd_series_ext.get_series_name(data)
            meq__hsbnx = bodo.libs.distributed_api.bcast_comm_impl(dpd__nkzmu,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            anvq__akhrx = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                anvq__akhrx, meq__hsbnx)
        return impl_series
    if isinstance(data, types.BaseTuple):
        vtwoi__yit = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        vtwoi__yit += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        hcctx__yian = {}
        exec(vtwoi__yit, {'bcast_comm_impl': bcast_comm_impl}, hcctx__yian)
        asvbw__welpa = hcctx__yian['impl_tuple']
        return asvbw__welpa
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    yip__fpx = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    oxgru__ojrgn = (0,) * yip__fpx

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        djjw__suzp = np.ascontiguousarray(data)
        xzbp__laly = data.ctypes
        xlek__lehlo = oxgru__ojrgn
        if rank == root:
            xlek__lehlo = djjw__suzp.shape
        xlek__lehlo = bcast_tuple(xlek__lehlo, root)
        aey__xqocs = get_tuple_prod(xlek__lehlo[1:])
        send_counts = xlek__lehlo[0] * aey__xqocs
        cphw__oky = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(xzbp__laly, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(cphw__oky.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return cphw__oky.reshape((-1,) + xlek__lehlo[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        xnwzv__pfd = MPI.COMM_WORLD
        giktg__ynjgq = MPI.Get_processor_name()
        lew__kyaxz = xnwzv__pfd.allgather(giktg__ynjgq)
        node_ranks = defaultdict(list)
        for i, qzxzk__bwvv in enumerate(lew__kyaxz):
            node_ranks[qzxzk__bwvv].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    xnwzv__pfd = MPI.COMM_WORLD
    avpn__xwr = xnwzv__pfd.Get_group()
    rqm__efjh = avpn__xwr.Incl(comm_ranks)
    tygcj__uhen = xnwzv__pfd.Create_group(rqm__efjh)
    return tygcj__uhen


def get_nodes_first_ranks():
    hazai__usgi = get_host_ranks()
    return np.array([kyyqi__bwqi[0] for kyyqi__bwqi in hazai__usgi.values()
        ], dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
