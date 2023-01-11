"""implementations of rolling window functions (sequential and parallel)
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, register_jitable
import bodo
from bodo.libs.distributed_api import Reduce_Type
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_func, get_overload_const_str, is_const_func_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true
from bodo.utils.utils import unliteral_all
supported_rolling_funcs = ('sum', 'mean', 'var', 'std', 'count', 'median',
    'min', 'max', 'cov', 'corr', 'apply')
unsupported_rolling_methods = ['skew', 'kurt', 'aggregate', 'quantile', 'sem']


def rolling_fixed(arr, win):
    return arr


def rolling_variable(arr, on_arr, win):
    return arr


def rolling_cov(arr, arr2, win):
    return arr


def rolling_corr(arr, arr2, win):
    return arr


@infer_global(rolling_cov)
@infer_global(rolling_corr)
class RollingCovType(AbstractTemplate):

    def generic(self, args, kws):
        arr = args[0]
        ipet__diwas = arr.copy(dtype=types.float64)
        return signature(ipet__diwas, *unliteral_all(args))


@lower_builtin(rolling_corr, types.VarArg(types.Any))
@lower_builtin(rolling_cov, types.VarArg(types.Any))
def lower_rolling_corr_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@overload(rolling_fixed, no_unliteral=True)
def overload_rolling_fixed(arr, index_arr, win, minp, center, fname, raw=
    True, parallel=False):
    assert is_overload_constant_bool(raw
        ), 'raw argument should be constant bool'
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    oqd__kix = get_overload_const_str(fname)
    if oqd__kix not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (oqd__kix))
    if oqd__kix in ('median', 'min', 'max'):
        akqq__hyq = 'def kernel_func(A):\n'
        akqq__hyq += '  if np.isnan(A).sum() != 0: return np.nan\n'
        akqq__hyq += '  return np.{}(A)\n'.format(oqd__kix)
        kixk__pocis = {}
        exec(akqq__hyq, {'np': np}, kixk__pocis)
        kernel_func = register_jitable(kixk__pocis['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        oqd__kix]
    return (lambda arr, index_arr, win, minp, center, fname, raw=True,
        parallel=False: roll_fixed_linear_generic(arr, win, minp, center,
        parallel, init_kernel, add_kernel, remove_kernel, calc_kernel))


@overload(rolling_variable, no_unliteral=True)
def overload_rolling_variable(arr, on_arr, index_arr, win, minp, center,
    fname, raw=True, parallel=False):
    assert is_overload_constant_bool(raw)
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    oqd__kix = get_overload_const_str(fname)
    if oqd__kix not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(oqd__kix))
    if oqd__kix in ('median', 'min', 'max'):
        akqq__hyq = 'def kernel_func(A):\n'
        akqq__hyq += '  arr  = dropna(A)\n'
        akqq__hyq += '  if len(arr) == 0: return np.nan\n'
        akqq__hyq += '  return np.{}(arr)\n'.format(oqd__kix)
        kixk__pocis = {}
        exec(akqq__hyq, {'np': np, 'dropna': _dropna}, kixk__pocis)
        kernel_func = register_jitable(kixk__pocis['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        oqd__kix]
    return (lambda arr, on_arr, index_arr, win, minp, center, fname, raw=
        True, parallel=False: roll_var_linear_generic(arr, on_arr, win,
        minp, center, parallel, init_kernel, add_kernel, remove_kernel,
        calc_kernel))


def _get_apply_func(f_type):
    func = get_overload_const_func(f_type, None)
    return bodo.compiler.udf_jit(func)


comm_border_tag = 22


@register_jitable
def roll_fixed_linear_generic(in_arr, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data(in_arr, win, minp, center, rank,
                n_pes, init_data, add_obs, remove_obs, calc_out)
        cpwa__voe = _border_icomm(in_arr, rank, n_pes, halo_size, True, center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            cbq__gamx) = cpwa__voe
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(cbq__gamx, True)
            for cwos__ywu in range(0, halo_size):
                data = add_obs(r_recv_buff[cwos__ywu], *data)
                zzybb__uewgt = in_arr[N + cwos__ywu - win]
                data = remove_obs(zzybb__uewgt, *data)
                output[N + cwos__ywu - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for cwos__ywu in range(0, halo_size):
                data = add_obs(l_recv_buff[cwos__ywu], *data)
            for cwos__ywu in range(0, win - 1):
                data = add_obs(in_arr[cwos__ywu], *data)
                if cwos__ywu > offset:
                    zzybb__uewgt = l_recv_buff[cwos__ywu - offset - 1]
                    data = remove_obs(zzybb__uewgt, *data)
                if cwos__ywu >= offset:
                    output[cwos__ywu - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    czgxs__frbc = max(minp, 1) - 1
    czgxs__frbc = min(czgxs__frbc, N)
    for cwos__ywu in range(0, czgxs__frbc):
        data = add_obs(in_arr[cwos__ywu], *data)
        if cwos__ywu >= offset:
            output[cwos__ywu - offset] = calc_out(minp, *data)
    for cwos__ywu in range(czgxs__frbc, N):
        val = in_arr[cwos__ywu]
        data = add_obs(val, *data)
        if cwos__ywu > win - 1:
            zzybb__uewgt = in_arr[cwos__ywu - win]
            data = remove_obs(zzybb__uewgt, *data)
        output[cwos__ywu - offset] = calc_out(minp, *data)
    iqt__vtmjd = data
    for cwos__ywu in range(N, N + offset):
        if cwos__ywu > win - 1:
            zzybb__uewgt = in_arr[cwos__ywu - win]
            data = remove_obs(zzybb__uewgt, *data)
        output[cwos__ywu - offset] = calc_out(minp, *data)
    return output, iqt__vtmjd


def roll_fixed_apply(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    pass


@overload(roll_fixed_apply, no_unliteral=True)
def overload_roll_fixed_apply(in_arr, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_fixed_apply_impl


def roll_fixed_apply_impl(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    index_arr = fix_index_arr(index_arr)
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_apply(in_arr, index_arr, win, minp,
                center, rank, n_pes, kernel_func, raw)
        cpwa__voe = _border_icomm(in_arr, rank, n_pes, halo_size, True, center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            cbq__gamx) = cpwa__voe
        if raw == False:
            xgvln__zslav = _border_icomm(index_arr, rank, n_pes, halo_size,
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, qddu__oway, ysszz__yrqt,
                gxk__ewfqd, zuyz__cdmmt) = xgvln__zslav
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(ysszz__yrqt, qddu__oway, rank, n_pes, True,
                center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(cbq__gamx, True)
            if raw == False:
                bodo.libs.distributed_api.wait(zuyz__cdmmt, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(gxk__ewfqd, True)
            recv_left_compute(output, in_arr, index_arr, win, minp, offset,
                l_recv_buff, l_recv_buff_idx, kernel_func, raw)
    return output


def recv_right_compute(output, in_arr, index_arr, N, win, minp, offset,
    r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_right_compute, no_unliteral=True)
def overload_recv_right_compute(output, in_arr, index_arr, N, win, minp,
    offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, N, win, minp, offset,
            r_recv_buff, r_recv_buff_idx, kernel_func, raw):
            iqt__vtmjd = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            taqw__qbu = 0
            for cwos__ywu in range(max(N - offset, 0), N):
                data = iqt__vtmjd[taqw__qbu:taqw__qbu + win]
                if win - np.isnan(data).sum() < minp:
                    output[cwos__ywu] = np.nan
                else:
                    output[cwos__ywu] = kernel_func(data)
                taqw__qbu += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        iqt__vtmjd = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        hqhg__xgc = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx))
        taqw__qbu = 0
        for cwos__ywu in range(max(N - offset, 0), N):
            data = iqt__vtmjd[taqw__qbu:taqw__qbu + win]
            if win - np.isnan(data).sum() < minp:
                output[cwos__ywu] = np.nan
            else:
                output[cwos__ywu] = kernel_func(pd.Series(data, hqhg__xgc[
                    taqw__qbu:taqw__qbu + win]))
            taqw__qbu += 1
    return impl_series


def recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_left_compute, no_unliteral=True)
def overload_recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, win, minp, offset, l_recv_buff,
            l_recv_buff_idx, kernel_func, raw):
            iqt__vtmjd = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for cwos__ywu in range(0, win - offset - 1):
                data = iqt__vtmjd[cwos__ywu:cwos__ywu + win]
                if win - np.isnan(data).sum() < minp:
                    output[cwos__ywu] = np.nan
                else:
                    output[cwos__ywu] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        iqt__vtmjd = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        hqhg__xgc = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for cwos__ywu in range(0, win - offset - 1):
            data = iqt__vtmjd[cwos__ywu:cwos__ywu + win]
            if win - np.isnan(data).sum() < minp:
                output[cwos__ywu] = np.nan
            else:
                output[cwos__ywu] = kernel_func(pd.Series(data, hqhg__xgc[
                    cwos__ywu:cwos__ywu + win]))
    return impl_series


def roll_fixed_apply_seq(in_arr, index_arr, win, minp, center, kernel_func,
    raw=True):
    pass


@overload(roll_fixed_apply_seq, no_unliteral=True)
def overload_roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
    kernel_func, raw=True):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"

    def roll_fixed_apply_seq_impl(in_arr, index_arr, win, minp, center,
        kernel_func, raw=True):
        N = len(in_arr)
        output = np.empty(N, dtype=np.float64)
        offset = (win - 1) // 2 if center else 0
        for cwos__ywu in range(0, N):
            start = max(cwos__ywu - win + 1 + offset, 0)
            end = min(cwos__ywu + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[cwos__ywu] = np.nan
            else:
                output[cwos__ywu] = apply_func(kernel_func, data, index_arr,
                    start, end, raw)
        return output
    return roll_fixed_apply_seq_impl


def apply_func(kernel_func, data, index_arr, start, end, raw):
    return kernel_func(data)


@overload(apply_func, no_unliteral=True)
def overload_apply_func(kernel_func, data, index_arr, start, end, raw):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"
    if is_overload_true(raw):
        return (lambda kernel_func, data, index_arr, start, end, raw:
            kernel_func(data))
    return lambda kernel_func, data, index_arr, start, end, raw: kernel_func(pd
        .Series(data, index_arr[start:end]))


def fix_index_arr(A):
    return A


@overload(fix_index_arr)
def overload_fix_index_arr(A):
    if is_overload_none(A):
        return lambda A: np.zeros(3)
    return lambda A: A


def get_offset_nanos(w):
    out = status = 0
    try:
        out = pd.tseries.frequencies.to_offset(w).nanos
    except:
        status = 1
    return out, status


def offset_to_nanos(w):
    return w


@overload(offset_to_nanos)
def overload_offset_to_nanos(w):
    if isinstance(w, types.Integer):
        return lambda w: w

    def impl(w):
        with numba.objmode(out='int64', status='int64'):
            out, status = get_offset_nanos(w)
        if status != 0:
            raise ValueError('Invalid offset value')
        return out
    return impl


@register_jitable
def roll_var_linear_generic(in_arr, on_arr_dt, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable(in_arr, on_arr, win, minp,
                rank, n_pes, init_data, add_obs, remove_obs, calc_out)
        cpwa__voe = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, ihp__bjss, l_recv_req,
            tdpoz__dwu) = cpwa__voe
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(ihp__bjss, ihp__bjss, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(tdpoz__dwu, True)
            num_zero_starts = 0
            for cwos__ywu in range(0, N):
                if start[cwos__ywu] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for wmpi__tqx in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[wmpi__tqx], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for cwos__ywu in range(1, num_zero_starts):
                s = recv_starts[cwos__ywu]
                lyknu__mmwv = end[cwos__ywu]
                for wmpi__tqx in range(recv_starts[cwos__ywu - 1], s):
                    data = remove_obs(l_recv_buff[wmpi__tqx], *data)
                for wmpi__tqx in range(end[cwos__ywu - 1], lyknu__mmwv):
                    data = add_obs(in_arr[wmpi__tqx], *data)
                output[cwos__ywu] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    krpno__vez = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    rtzh__vdlwo = krpno__vez[0] - win
    if left_closed:
        rtzh__vdlwo -= 1
    recv_starts[0] = halo_size
    for wmpi__tqx in range(0, halo_size):
        if l_recv_t_buff[wmpi__tqx] > rtzh__vdlwo:
            recv_starts[0] = wmpi__tqx
            break
    for cwos__ywu in range(1, num_zero_starts):
        rtzh__vdlwo = krpno__vez[cwos__ywu] - win
        if left_closed:
            rtzh__vdlwo -= 1
        recv_starts[cwos__ywu] = halo_size
        for wmpi__tqx in range(recv_starts[cwos__ywu - 1], halo_size):
            if l_recv_t_buff[wmpi__tqx] > rtzh__vdlwo:
                recv_starts[cwos__ywu] = wmpi__tqx
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for wmpi__tqx in range(start[0], end[0]):
        data = add_obs(in_arr[wmpi__tqx], *data)
    output[0] = calc_out(minp, *data)
    for cwos__ywu in range(1, N):
        s = start[cwos__ywu]
        lyknu__mmwv = end[cwos__ywu]
        for wmpi__tqx in range(start[cwos__ywu - 1], s):
            data = remove_obs(in_arr[wmpi__tqx], *data)
        for wmpi__tqx in range(end[cwos__ywu - 1], lyknu__mmwv):
            data = add_obs(in_arr[wmpi__tqx], *data)
        output[cwos__ywu] = calc_out(minp, *data)
    return output


def roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    pass


@overload(roll_variable_apply, no_unliteral=True)
def overload_roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_variable_apply_impl


def roll_variable_apply_impl(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    index_arr = fix_index_arr(index_arr)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable_apply(in_arr, on_arr,
                index_arr, win, minp, rank, n_pes, kernel_func, raw)
        cpwa__voe = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, ihp__bjss, l_recv_req,
            tdpoz__dwu) = cpwa__voe
        if raw == False:
            xgvln__zslav = _border_icomm_var(index_arr, on_arr, rank, n_pes,
                win)
            (l_recv_buff_idx, qraeg__blgpe, ysszz__yrqt, amzl__sgchi,
                gxk__ewfqd, ukk__zutl) = xgvln__zslav
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(ihp__bjss, ihp__bjss, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(ysszz__yrqt, ysszz__yrqt, rank, n_pes, True, 
                False)
            _border_send_wait(amzl__sgchi, amzl__sgchi, rank, n_pes, True, 
                False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(tdpoz__dwu, True)
            if raw == False:
                bodo.libs.distributed_api.wait(gxk__ewfqd, True)
                bodo.libs.distributed_api.wait(ukk__zutl, True)
            num_zero_starts = 0
            for cwos__ywu in range(0, N):
                if start[cwos__ywu] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            recv_left_var_compute(output, in_arr, index_arr,
                num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx,
                minp, kernel_func, raw)
    return output


def recv_left_var_compute(output, in_arr, index_arr, num_zero_starts,
    recv_starts, l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
    pass


@overload(recv_left_var_compute)
def overload_recv_left_var_compute(output, in_arr, index_arr,
    num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx, minp,
    kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, num_zero_starts, recv_starts,
            l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
            for cwos__ywu in range(0, num_zero_starts):
                dehkx__cdqme = recv_starts[cwos__ywu]
                ueuu__ztjh = np.concatenate((l_recv_buff[dehkx__cdqme:],
                    in_arr[:cwos__ywu + 1]))
                if len(ueuu__ztjh) - np.isnan(ueuu__ztjh).sum() >= minp:
                    output[cwos__ywu] = kernel_func(ueuu__ztjh)
                else:
                    output[cwos__ywu] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for cwos__ywu in range(0, num_zero_starts):
            dehkx__cdqme = recv_starts[cwos__ywu]
            ueuu__ztjh = np.concatenate((l_recv_buff[dehkx__cdqme:], in_arr
                [:cwos__ywu + 1]))
            ajjdy__qrsvh = np.concatenate((l_recv_buff_idx[dehkx__cdqme:],
                index_arr[:cwos__ywu + 1]))
            if len(ueuu__ztjh) - np.isnan(ueuu__ztjh).sum() >= minp:
                output[cwos__ywu] = kernel_func(pd.Series(ueuu__ztjh,
                    ajjdy__qrsvh))
            else:
                output[cwos__ywu] = np.nan
    return impl_series


def roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp, start,
    end, kernel_func, raw):
    pass


@overload(roll_variable_apply_seq)
def overload_roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):
        return roll_variable_apply_seq_impl
    return roll_variable_apply_seq_impl_series


def roll_variable_apply_seq_impl(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for cwos__ywu in range(0, N):
        s = start[cwos__ywu]
        lyknu__mmwv = end[cwos__ywu]
        data = in_arr[s:lyknu__mmwv]
        if lyknu__mmwv - s - np.isnan(data).sum() >= minp:
            output[cwos__ywu] = kernel_func(data)
        else:
            output[cwos__ywu] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for cwos__ywu in range(0, N):
        s = start[cwos__ywu]
        lyknu__mmwv = end[cwos__ywu]
        data = in_arr[s:lyknu__mmwv]
        if lyknu__mmwv - s - np.isnan(data).sum() >= minp:
            output[cwos__ywu] = kernel_func(pd.Series(data, index_arr[s:
                lyknu__mmwv]))
        else:
            output[cwos__ywu] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    krpno__vez = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for cwos__ywu in range(1, N):
        lwei__flv = krpno__vez[cwos__ywu]
        rtzh__vdlwo = krpno__vez[cwos__ywu] - win
        if left_closed:
            rtzh__vdlwo -= 1
        start[cwos__ywu] = cwos__ywu
        for wmpi__tqx in range(start[cwos__ywu - 1], cwos__ywu):
            if krpno__vez[wmpi__tqx] > rtzh__vdlwo:
                start[cwos__ywu] = wmpi__tqx
                break
        if krpno__vez[end[cwos__ywu - 1]] <= lwei__flv:
            end[cwos__ywu] = cwos__ywu + 1
        else:
            end[cwos__ywu] = end[cwos__ywu - 1]
        if not right_closed:
            end[cwos__ywu] -= 1
    return start, end


@register_jitable
def init_data_sum():
    return 0, 0.0


@register_jitable
def add_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
    return nobs, sum_x


@register_jitable
def remove_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
    return nobs, sum_x


@register_jitable
def calc_sum(minp, nobs, sum_x):
    return sum_x if nobs >= minp else np.nan


@register_jitable
def init_data_mean():
    return 0, 0.0, 0


@register_jitable
def add_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
        if val < 0:
            neg_ct += 1
    return nobs, sum_x, neg_ct


@register_jitable
def remove_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
        if val < 0:
            neg_ct -= 1
    return nobs, sum_x, neg_ct


@register_jitable
def calc_mean(minp, nobs, sum_x, neg_ct):
    if nobs >= minp:
        nava__doi = sum_x / nobs
        if neg_ct == 0 and nava__doi < 0.0:
            nava__doi = 0
        elif neg_ct == nobs and nava__doi > 0.0:
            nava__doi = 0
    else:
        nava__doi = np.nan
    return nava__doi


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        idbsp__ded = val - mean_x
        mean_x += idbsp__ded / nobs
        ssqdm_x += (nobs - 1) * idbsp__ded ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            idbsp__ded = val - mean_x
            mean_x -= idbsp__ded / nobs
            ssqdm_x -= (nobs + 1) * idbsp__ded ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    ftdk__opcr = 1.0
    nava__doi = np.nan
    if nobs >= minp and nobs > ftdk__opcr:
        if nobs == 1:
            nava__doi = 0.0
        else:
            nava__doi = ssqdm_x / (nobs - ftdk__opcr)
            if nava__doi < 0.0:
                nava__doi = 0.0
    return nava__doi


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    aqre__rnm = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(aqre__rnm)


@register_jitable
def init_data_count():
    return 0.0,


@register_jitable
def add_count(val, count_x):
    if not np.isnan(val):
        count_x += 1.0
    return count_x,


@register_jitable
def remove_count(val, count_x):
    if not np.isnan(val):
        count_x -= 1.0
    return count_x,


@register_jitable
def calc_count(minp, count_x):
    return count_x


@register_jitable
def calc_count_var(minp, count_x):
    return count_x if count_x >= minp else np.nan


linear_kernels = {'sum': (init_data_sum, add_sum, remove_sum, calc_sum),
    'mean': (init_data_mean, add_mean, remove_mean, calc_mean), 'var': (
    init_data_var, add_var, remove_var, calc_var), 'std': (init_data_var,
    add_var, remove_var, calc_std), 'count': (init_data_count, add_count,
    remove_count, calc_count)}


def shift(in_arr, shift, parallel, default_fill_value=None):
    return


@overload(shift, jit_options={'cache': True})
def shift_overload(in_arr, shift, parallel, default_fill_value=None):
    if not isinstance(parallel, types.Literal):
        return shift_impl


def shift_impl(in_arr, shift, parallel, default_fill_value=None):
    N = len(in_arr)
    in_arr = decode_if_dict_array(in_arr)
    output = alloc_shift(N, in_arr, (-1,), fill_value=default_fill_value)
    send_right = shift > 0
    send_left = shift <= 0
    is_parallel_str = False
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_shift(in_arr, shift, rank, n_pes,
                default_fill_value)
        cpwa__voe = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            cbq__gamx) = cpwa__voe
        if send_right and is_str_binary_array(in_arr):
            is_parallel_str = True
            shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
                l_recv_req, l_recv_buff, output)
    shift_seq(in_arr, shift, output, is_parallel_str, default_fill_value)
    if parallel:
        if send_right:
            if not is_str_binary_array(in_arr):
                shift_left_recv(r_send_req, l_send_req, rank, n_pes,
                    halo_size, l_recv_req, l_recv_buff, output)
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(cbq__gamx, True)
                for cwos__ywu in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, cwos__ywu):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            cwos__ywu)
                        continue
                    output[N - halo_size + cwos__ywu] = r_recv_buff[cwos__ywu]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False,
    default_fill_value=None):
    N = len(in_arr)
    qzlb__vbeaz = 1 if shift > 0 else -1
    shift = qzlb__vbeaz * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
        else:
            for cwos__ywu in range(shift):
                output[cwos__ywu
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    start = max(shift, 0)
    end = min(N, N + shift)
    for cwos__ywu in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, cwos__ywu - shift):
            bodo.libs.array_kernels.setna(output, cwos__ywu)
            continue
        output[cwos__ywu] = in_arr[cwos__ywu - shift]
    if shift < 0:
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
        else:
            for cwos__ywu in range(end, N):
                output[cwos__ywu
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for cwos__ywu in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, cwos__ywu):
                bodo.libs.array_kernels.setna(output, cwos__ywu)
                continue
            output[cwos__ywu] = l_recv_buff[cwos__ywu]


def is_str_binary_array(arr):
    return False


@overload(is_str_binary_array)
def overload_is_str_binary_array(arr):
    if arr in [bodo.string_array_type, bodo.binary_array_type]:
        return lambda arr: True
    return lambda arr: False


def is_supported_shift_array_type(arr_type):
    return isinstance(arr_type, types.Array) and (isinstance(arr_type.dtype,
        types.Number) or arr_type.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]) or isinstance(arr_type, (bodo.IntegerArrayType,
        bodo.FloatingArrayType, bodo.DecimalArrayType, bodo.DatetimeArrayType)
        ) or arr_type in (bodo.boolean_array, bodo.datetime_date_array_type,
        bodo.string_array_type, bodo.binary_array_type, bodo.dict_str_arr_type)


def pct_change():
    return


@overload(pct_change, jit_options={'cache': True})
def pct_change_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return pct_change_impl


def pct_change_impl(in_arr, shift, parallel):
    N = len(in_arr)
    send_right = shift > 0
    send_left = shift <= 0
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_pct_change(in_arr, shift, rank, n_pes)
        cpwa__voe = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            cbq__gamx) = cpwa__voe
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for cwos__ywu in range(0, halo_size):
                    rfgbz__yzbb = l_recv_buff[cwos__ywu]
                    output[cwos__ywu] = (in_arr[cwos__ywu] - rfgbz__yzbb
                        ) / rfgbz__yzbb
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(cbq__gamx, True)
                for cwos__ywu in range(0, halo_size):
                    rfgbz__yzbb = r_recv_buff[cwos__ywu]
                    output[N - halo_size + cwos__ywu] = (in_arr[N -
                        halo_size + cwos__ywu] - rfgbz__yzbb) / rfgbz__yzbb
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    mtpy__yqxjv = np.nan
    if arr.dtype == types.float32:
        mtpy__yqxjv = np.float32('nan')

    def impl(arr):
        for cwos__ywu in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, cwos__ywu):
                return arr[cwos__ywu]
        return mtpy__yqxjv
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    mtpy__yqxjv = np.nan
    if arr.dtype == types.float32:
        mtpy__yqxjv = np.float32('nan')

    def impl(arr):
        wgouu__sosq = len(arr)
        for cwos__ywu in range(len(arr)):
            taqw__qbu = wgouu__sosq - cwos__ywu - 1
            if not bodo.libs.array_kernels.isna(arr, taqw__qbu):
                return arr[taqw__qbu]
        return mtpy__yqxjv
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    qzlb__vbeaz = 1 if shift > 0 else -1
    shift = qzlb__vbeaz * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        hhd__lqmc = get_first_non_na(in_arr[:shift])
        khfd__ocuz = get_last_non_na(in_arr[:shift])
    else:
        hhd__lqmc = get_last_non_na(in_arr[:-shift])
        khfd__ocuz = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for cwos__ywu in range(start, end):
        rfgbz__yzbb = in_arr[cwos__ywu - shift]
        if np.isnan(rfgbz__yzbb):
            rfgbz__yzbb = hhd__lqmc
        else:
            hhd__lqmc = rfgbz__yzbb
        val = in_arr[cwos__ywu]
        if np.isnan(val):
            val = khfd__ocuz
        else:
            khfd__ocuz = val
        output[cwos__ywu] = val / rfgbz__yzbb - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    vflos__dap = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), vflos__dap, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), vflos__dap, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), vflos__dap, True)
    if send_left and rank != n_pes - 1:
        cbq__gamx = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), vflos__dap, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        cbq__gamx)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    vflos__dap = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for wmpi__tqx in range(-2, -N, -1):
        grg__iwuc = on_arr[wmpi__tqx]
        if end - grg__iwuc >= win_size:
            halo_size = -wmpi__tqx
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1),
            vflos__dap)
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), vflos__dap, True)
        ihp__bjss = bodo.libs.distributed_api.isend(on_arr[-halo_size:], np
            .int32(halo_size), np.int32(rank + 1), vflos__dap, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), vflos__dap)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), vflos__dap, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        tdpoz__dwu = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), vflos__dap, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, ihp__bjss, l_recv_req,
        tdpoz__dwu)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    wftb__qeokf = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return wftb__qeokf != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    pzfp__ppuz = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    qzn__jen = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        ojb__dycqn, czy__gdeon = roll_fixed_linear_generic_seq(qzn__jen,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        ojb__dycqn = np.empty(pzfp__ppuz, np.float64)
    bodo.libs.distributed_api.bcast(ojb__dycqn)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return ojb__dycqn[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    pzfp__ppuz = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    qzn__jen = bodo.libs.distributed_api.gatherv(in_arr)
    tig__ied = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        ojb__dycqn = roll_fixed_apply_seq(qzn__jen, tig__ied, win, minp,
            center, kernel_func, raw)
    else:
        ojb__dycqn = np.empty(pzfp__ppuz, np.float64)
    bodo.libs.distributed_api.bcast(ojb__dycqn)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return ojb__dycqn[start:end]


def bcast_n_chars_if_str_binary_arr(arr):
    pass


@overload(bcast_n_chars_if_str_binary_arr)
def overload_bcast_n_chars_if_str_binary_arr(arr):
    if arr in [bodo.binary_array_type, bodo.string_array_type]:

        def impl(arr):
            return bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.
                libs.str_arr_ext.num_total_chars(arr)))
        return impl
    return lambda arr: -1


@register_jitable
def _handle_small_data_shift(in_arr, shift, rank, n_pes, default_fill_value):
    N = len(in_arr)
    pzfp__ppuz = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    qzn__jen = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        ojb__dycqn = alloc_shift(len(qzn__jen), qzn__jen, (-1,), fill_value
            =default_fill_value)
        shift_seq(qzn__jen, shift, ojb__dycqn, default_fill_value=
            default_fill_value)
        bboe__rsg = bcast_n_chars_if_str_binary_arr(ojb__dycqn)
    else:
        bboe__rsg = bcast_n_chars_if_str_binary_arr(in_arr)
        ojb__dycqn = alloc_shift(pzfp__ppuz, in_arr, (bboe__rsg,),
            fill_value=default_fill_value)
    bodo.libs.distributed_api.bcast(ojb__dycqn)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return ojb__dycqn[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    pzfp__ppuz = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    qzn__jen = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        ojb__dycqn = pct_change_seq(qzn__jen, shift)
    else:
        ojb__dycqn = alloc_pct_change(pzfp__ppuz, in_arr)
    bodo.libs.distributed_api.bcast(ojb__dycqn)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return ojb__dycqn[start:end]


def cast_dt64_arr_to_int(arr):
    return arr


@infer_global(cast_dt64_arr_to_int)
class DtArrToIntType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        assert args[0] == types.Array(types.NPDatetime('ns'), 1, 'C') or args[0
            ] == types.Array(types.int64, 1, 'C')
        return signature(types.Array(types.int64, 1, 'C'), *args)


@lower_builtin(cast_dt64_arr_to_int, types.Array(types.NPDatetime('ns'), 1,
    'C'))
@lower_builtin(cast_dt64_arr_to_int, types.Array(types.int64, 1, 'C'))
def lower_cast_dt64_arr_to_int(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@register_jitable
def _is_small_for_parallel_variable(on_arr, win_size):
    if len(on_arr) < 2:
        eveas__ptr = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        rqmaj__roq = end - start
        eveas__ptr = int(rqmaj__roq <= win_size)
    wftb__qeokf = bodo.libs.distributed_api.dist_reduce(eveas__ptr, np.
        int32(Reduce_Type.Sum.value))
    return wftb__qeokf != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    pzfp__ppuz = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    qzn__jen = bodo.libs.distributed_api.gatherv(in_arr)
    qpa__ysf = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(qpa__ysf, pzfp__ppuz, win, False, True)
        ojb__dycqn = roll_var_linear_generic_seq(qzn__jen, qpa__ysf, win,
            minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        ojb__dycqn = np.empty(pzfp__ppuz, np.float64)
    bodo.libs.distributed_api.bcast(ojb__dycqn)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return ojb__dycqn[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    pzfp__ppuz = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    qzn__jen = bodo.libs.distributed_api.gatherv(in_arr)
    qpa__ysf = bodo.libs.distributed_api.gatherv(on_arr)
    tig__ied = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(qpa__ysf, pzfp__ppuz, win, False, True)
        ojb__dycqn = roll_variable_apply_seq(qzn__jen, qpa__ysf, tig__ied,
            win, minp, start, end, kernel_func, raw)
    else:
        ojb__dycqn = np.empty(pzfp__ppuz, np.float64)
    bodo.libs.distributed_api.bcast(ojb__dycqn)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return ojb__dycqn[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    ujmq__oim = len(arr)
    torh__onov = ujmq__oim - np.isnan(arr).sum()
    A = np.empty(torh__onov, arr.dtype)
    twxm__yzxqu = 0
    for cwos__ywu in range(ujmq__oim):
        val = arr[cwos__ywu]
        if not np.isnan(val):
            A[twxm__yzxqu] = val
            twxm__yzxqu += 1
    return A


def alloc_shift(n, A, s=None, fill_value=None):
    return np.empty(n, A.dtype)


@overload(alloc_shift, no_unliteral=True)
def alloc_shift_overload(n, A, s=None, fill_value=None):
    if not isinstance(A, types.Array):
        return (lambda n, A, s=None, fill_value=None: bodo.utils.utils.
            alloc_type(n, A, s))
    if isinstance(A.dtype, types.Integer) and not isinstance(fill_value,
        types.Integer):
        return lambda n, A, s=None, fill_value=None: np.empty(n, np.float64)
    return lambda n, A, s=None, fill_value=None: np.empty(n, A.dtype)


def alloc_pct_change(n, A):
    return np.empty(n, A.dtype)


@overload(alloc_pct_change, no_unliteral=True)
def alloc_pct_change_overload(n, A):
    if isinstance(A.dtype, types.Integer):
        return lambda n, A: np.empty(n, np.float64)
    return lambda n, A: bodo.utils.utils.alloc_type(n, A, (-1,))


def prep_values(A):
    return A.astype('float64')


@overload(prep_values, no_unliteral=True)
def prep_values_overload(A):
    if A == types.Array(types.float64, 1, 'C'):
        return lambda A: A
    return lambda A: A.astype(np.float64)


@register_jitable
def _validate_roll_fixed_args(win, minp):
    if win < 0:
        raise ValueError('window must be non-negative')
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if minp > win:
        raise ValueError('min_periods must be <= window')


@register_jitable
def _validate_roll_var_args(minp, center):
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if center:
        raise NotImplementedError(
            'rolling: center is not implemented for datetimelike and offset based windows'
            )
