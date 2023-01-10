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
        plfrh__cxu = arr.copy(dtype=types.float64)
        return signature(plfrh__cxu, *unliteral_all(args))


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
    ryrfg__esy = get_overload_const_str(fname)
    if ryrfg__esy not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (ryrfg__esy))
    if ryrfg__esy in ('median', 'min', 'max'):
        zng__jte = 'def kernel_func(A):\n'
        zng__jte += '  if np.isnan(A).sum() != 0: return np.nan\n'
        zng__jte += '  return np.{}(A)\n'.format(ryrfg__esy)
        dkpdx__iwlu = {}
        exec(zng__jte, {'np': np}, dkpdx__iwlu)
        kernel_func = register_jitable(dkpdx__iwlu['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        ryrfg__esy]
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
    ryrfg__esy = get_overload_const_str(fname)
    if ryrfg__esy not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(ryrfg__esy))
    if ryrfg__esy in ('median', 'min', 'max'):
        zng__jte = 'def kernel_func(A):\n'
        zng__jte += '  arr  = dropna(A)\n'
        zng__jte += '  if len(arr) == 0: return np.nan\n'
        zng__jte += '  return np.{}(arr)\n'.format(ryrfg__esy)
        dkpdx__iwlu = {}
        exec(zng__jte, {'np': np, 'dropna': _dropna}, dkpdx__iwlu)
        kernel_func = register_jitable(dkpdx__iwlu['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        ryrfg__esy]
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
        ssnph__rgqs = _border_icomm(in_arr, rank, n_pes, halo_size, True,
            center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req, amb__aoe
            ) = ssnph__rgqs
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(amb__aoe, True)
            for oizfi__lqh in range(0, halo_size):
                data = add_obs(r_recv_buff[oizfi__lqh], *data)
                tyzvj__coezd = in_arr[N + oizfi__lqh - win]
                data = remove_obs(tyzvj__coezd, *data)
                output[N + oizfi__lqh - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for oizfi__lqh in range(0, halo_size):
                data = add_obs(l_recv_buff[oizfi__lqh], *data)
            for oizfi__lqh in range(0, win - 1):
                data = add_obs(in_arr[oizfi__lqh], *data)
                if oizfi__lqh > offset:
                    tyzvj__coezd = l_recv_buff[oizfi__lqh - offset - 1]
                    data = remove_obs(tyzvj__coezd, *data)
                if oizfi__lqh >= offset:
                    output[oizfi__lqh - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    pnpx__uyrnk = max(minp, 1) - 1
    pnpx__uyrnk = min(pnpx__uyrnk, N)
    for oizfi__lqh in range(0, pnpx__uyrnk):
        data = add_obs(in_arr[oizfi__lqh], *data)
        if oizfi__lqh >= offset:
            output[oizfi__lqh - offset] = calc_out(minp, *data)
    for oizfi__lqh in range(pnpx__uyrnk, N):
        val = in_arr[oizfi__lqh]
        data = add_obs(val, *data)
        if oizfi__lqh > win - 1:
            tyzvj__coezd = in_arr[oizfi__lqh - win]
            data = remove_obs(tyzvj__coezd, *data)
        output[oizfi__lqh - offset] = calc_out(minp, *data)
    fiyvs__yltsv = data
    for oizfi__lqh in range(N, N + offset):
        if oizfi__lqh > win - 1:
            tyzvj__coezd = in_arr[oizfi__lqh - win]
            data = remove_obs(tyzvj__coezd, *data)
        output[oizfi__lqh - offset] = calc_out(minp, *data)
    return output, fiyvs__yltsv


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
        ssnph__rgqs = _border_icomm(in_arr, rank, n_pes, halo_size, True,
            center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req, amb__aoe
            ) = ssnph__rgqs
        if raw == False:
            oknk__kksmw = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, eddb__xzhzz, bdcbx__nveh,
                lvuyd__txg, knuqu__grmn) = oknk__kksmw
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(bdcbx__nveh, eddb__xzhzz, rank, n_pes, True,
                center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(amb__aoe, True)
            if raw == False:
                bodo.libs.distributed_api.wait(knuqu__grmn, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(lvuyd__txg, True)
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
            fiyvs__yltsv = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            ejh__ykdsx = 0
            for oizfi__lqh in range(max(N - offset, 0), N):
                data = fiyvs__yltsv[ejh__ykdsx:ejh__ykdsx + win]
                if win - np.isnan(data).sum() < minp:
                    output[oizfi__lqh] = np.nan
                else:
                    output[oizfi__lqh] = kernel_func(data)
                ejh__ykdsx += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        fiyvs__yltsv = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        iglcd__nkle = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx)
            )
        ejh__ykdsx = 0
        for oizfi__lqh in range(max(N - offset, 0), N):
            data = fiyvs__yltsv[ejh__ykdsx:ejh__ykdsx + win]
            if win - np.isnan(data).sum() < minp:
                output[oizfi__lqh] = np.nan
            else:
                output[oizfi__lqh] = kernel_func(pd.Series(data,
                    iglcd__nkle[ejh__ykdsx:ejh__ykdsx + win]))
            ejh__ykdsx += 1
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
            fiyvs__yltsv = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for oizfi__lqh in range(0, win - offset - 1):
                data = fiyvs__yltsv[oizfi__lqh:oizfi__lqh + win]
                if win - np.isnan(data).sum() < minp:
                    output[oizfi__lqh] = np.nan
                else:
                    output[oizfi__lqh] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        fiyvs__yltsv = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        iglcd__nkle = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for oizfi__lqh in range(0, win - offset - 1):
            data = fiyvs__yltsv[oizfi__lqh:oizfi__lqh + win]
            if win - np.isnan(data).sum() < minp:
                output[oizfi__lqh] = np.nan
            else:
                output[oizfi__lqh] = kernel_func(pd.Series(data,
                    iglcd__nkle[oizfi__lqh:oizfi__lqh + win]))
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
        for oizfi__lqh in range(0, N):
            start = max(oizfi__lqh - win + 1 + offset, 0)
            end = min(oizfi__lqh + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[oizfi__lqh] = np.nan
            else:
                output[oizfi__lqh] = apply_func(kernel_func, data,
                    index_arr, start, end, raw)
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
        ssnph__rgqs = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, xlzj__sneby, l_recv_req,
            szi__ggcmj) = ssnph__rgqs
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(xlzj__sneby, xlzj__sneby, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(szi__ggcmj, True)
            num_zero_starts = 0
            for oizfi__lqh in range(0, N):
                if start[oizfi__lqh] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for vbba__bfg in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[vbba__bfg], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for oizfi__lqh in range(1, num_zero_starts):
                s = recv_starts[oizfi__lqh]
                icsv__rybgf = end[oizfi__lqh]
                for vbba__bfg in range(recv_starts[oizfi__lqh - 1], s):
                    data = remove_obs(l_recv_buff[vbba__bfg], *data)
                for vbba__bfg in range(end[oizfi__lqh - 1], icsv__rybgf):
                    data = add_obs(in_arr[vbba__bfg], *data)
                output[oizfi__lqh] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    yzfa__nubmw = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    drwq__phdu = yzfa__nubmw[0] - win
    if left_closed:
        drwq__phdu -= 1
    recv_starts[0] = halo_size
    for vbba__bfg in range(0, halo_size):
        if l_recv_t_buff[vbba__bfg] > drwq__phdu:
            recv_starts[0] = vbba__bfg
            break
    for oizfi__lqh in range(1, num_zero_starts):
        drwq__phdu = yzfa__nubmw[oizfi__lqh] - win
        if left_closed:
            drwq__phdu -= 1
        recv_starts[oizfi__lqh] = halo_size
        for vbba__bfg in range(recv_starts[oizfi__lqh - 1], halo_size):
            if l_recv_t_buff[vbba__bfg] > drwq__phdu:
                recv_starts[oizfi__lqh] = vbba__bfg
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for vbba__bfg in range(start[0], end[0]):
        data = add_obs(in_arr[vbba__bfg], *data)
    output[0] = calc_out(minp, *data)
    for oizfi__lqh in range(1, N):
        s = start[oizfi__lqh]
        icsv__rybgf = end[oizfi__lqh]
        for vbba__bfg in range(start[oizfi__lqh - 1], s):
            data = remove_obs(in_arr[vbba__bfg], *data)
        for vbba__bfg in range(end[oizfi__lqh - 1], icsv__rybgf):
            data = add_obs(in_arr[vbba__bfg], *data)
        output[oizfi__lqh] = calc_out(minp, *data)
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
        ssnph__rgqs = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, xlzj__sneby, l_recv_req,
            szi__ggcmj) = ssnph__rgqs
        if raw == False:
            oknk__kksmw = _border_icomm_var(index_arr, on_arr, rank, n_pes, win
                )
            (l_recv_buff_idx, tmb__wioch, bdcbx__nveh, gaz__fwbk,
                lvuyd__txg, anle__urrsr) = oknk__kksmw
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(xlzj__sneby, xlzj__sneby, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(bdcbx__nveh, bdcbx__nveh, rank, n_pes, True, 
                False)
            _border_send_wait(gaz__fwbk, gaz__fwbk, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(szi__ggcmj, True)
            if raw == False:
                bodo.libs.distributed_api.wait(lvuyd__txg, True)
                bodo.libs.distributed_api.wait(anle__urrsr, True)
            num_zero_starts = 0
            for oizfi__lqh in range(0, N):
                if start[oizfi__lqh] != 0:
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
            for oizfi__lqh in range(0, num_zero_starts):
                ehri__vezh = recv_starts[oizfi__lqh]
                him__itxwt = np.concatenate((l_recv_buff[ehri__vezh:],
                    in_arr[:oizfi__lqh + 1]))
                if len(him__itxwt) - np.isnan(him__itxwt).sum() >= minp:
                    output[oizfi__lqh] = kernel_func(him__itxwt)
                else:
                    output[oizfi__lqh] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for oizfi__lqh in range(0, num_zero_starts):
            ehri__vezh = recv_starts[oizfi__lqh]
            him__itxwt = np.concatenate((l_recv_buff[ehri__vezh:], in_arr[:
                oizfi__lqh + 1]))
            oior__mdpo = np.concatenate((l_recv_buff_idx[ehri__vezh:],
                index_arr[:oizfi__lqh + 1]))
            if len(him__itxwt) - np.isnan(him__itxwt).sum() >= minp:
                output[oizfi__lqh] = kernel_func(pd.Series(him__itxwt,
                    oior__mdpo))
            else:
                output[oizfi__lqh] = np.nan
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
    for oizfi__lqh in range(0, N):
        s = start[oizfi__lqh]
        icsv__rybgf = end[oizfi__lqh]
        data = in_arr[s:icsv__rybgf]
        if icsv__rybgf - s - np.isnan(data).sum() >= minp:
            output[oizfi__lqh] = kernel_func(data)
        else:
            output[oizfi__lqh] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for oizfi__lqh in range(0, N):
        s = start[oizfi__lqh]
        icsv__rybgf = end[oizfi__lqh]
        data = in_arr[s:icsv__rybgf]
        if icsv__rybgf - s - np.isnan(data).sum() >= minp:
            output[oizfi__lqh] = kernel_func(pd.Series(data, index_arr[s:
                icsv__rybgf]))
        else:
            output[oizfi__lqh] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    yzfa__nubmw = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for oizfi__lqh in range(1, N):
        vnpx__morjq = yzfa__nubmw[oizfi__lqh]
        drwq__phdu = yzfa__nubmw[oizfi__lqh] - win
        if left_closed:
            drwq__phdu -= 1
        start[oizfi__lqh] = oizfi__lqh
        for vbba__bfg in range(start[oizfi__lqh - 1], oizfi__lqh):
            if yzfa__nubmw[vbba__bfg] > drwq__phdu:
                start[oizfi__lqh] = vbba__bfg
                break
        if yzfa__nubmw[end[oizfi__lqh - 1]] <= vnpx__morjq:
            end[oizfi__lqh] = oizfi__lqh + 1
        else:
            end[oizfi__lqh] = end[oizfi__lqh - 1]
        if not right_closed:
            end[oizfi__lqh] -= 1
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
        emxa__cup = sum_x / nobs
        if neg_ct == 0 and emxa__cup < 0.0:
            emxa__cup = 0
        elif neg_ct == nobs and emxa__cup > 0.0:
            emxa__cup = 0
    else:
        emxa__cup = np.nan
    return emxa__cup


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        wjywj__irpdy = val - mean_x
        mean_x += wjywj__irpdy / nobs
        ssqdm_x += (nobs - 1) * wjywj__irpdy ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            wjywj__irpdy = val - mean_x
            mean_x -= wjywj__irpdy / nobs
            ssqdm_x -= (nobs + 1) * wjywj__irpdy ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    thk__rjsry = 1.0
    emxa__cup = np.nan
    if nobs >= minp and nobs > thk__rjsry:
        if nobs == 1:
            emxa__cup = 0.0
        else:
            emxa__cup = ssqdm_x / (nobs - thk__rjsry)
            if emxa__cup < 0.0:
                emxa__cup = 0.0
    return emxa__cup


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    mbxgn__gmye = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(mbxgn__gmye)


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
        ssnph__rgqs = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req, amb__aoe
            ) = ssnph__rgqs
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
                bodo.libs.distributed_api.wait(amb__aoe, True)
                for oizfi__lqh in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, oizfi__lqh):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            oizfi__lqh)
                        continue
                    output[N - halo_size + oizfi__lqh] = r_recv_buff[oizfi__lqh
                        ]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False,
    default_fill_value=None):
    N = len(in_arr)
    bauzx__vdfae = 1 if shift > 0 else -1
    shift = bauzx__vdfae * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
        else:
            for oizfi__lqh in range(shift):
                output[oizfi__lqh
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    start = max(shift, 0)
    end = min(N, N + shift)
    for oizfi__lqh in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, oizfi__lqh - shift):
            bodo.libs.array_kernels.setna(output, oizfi__lqh)
            continue
        output[oizfi__lqh] = in_arr[oizfi__lqh - shift]
    if shift < 0:
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
        else:
            for oizfi__lqh in range(end, N):
                output[oizfi__lqh
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for oizfi__lqh in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, oizfi__lqh):
                bodo.libs.array_kernels.setna(output, oizfi__lqh)
                continue
            output[oizfi__lqh] = l_recv_buff[oizfi__lqh]


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
        ssnph__rgqs = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req, amb__aoe
            ) = ssnph__rgqs
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for oizfi__lqh in range(0, halo_size):
                    ayhs__hcyey = l_recv_buff[oizfi__lqh]
                    output[oizfi__lqh] = (in_arr[oizfi__lqh] - ayhs__hcyey
                        ) / ayhs__hcyey
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(amb__aoe, True)
                for oizfi__lqh in range(0, halo_size):
                    ayhs__hcyey = r_recv_buff[oizfi__lqh]
                    output[N - halo_size + oizfi__lqh] = (in_arr[N -
                        halo_size + oizfi__lqh] - ayhs__hcyey) / ayhs__hcyey
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    zzz__ooss = np.nan
    if arr.dtype == types.float32:
        zzz__ooss = np.float32('nan')

    def impl(arr):
        for oizfi__lqh in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, oizfi__lqh):
                return arr[oizfi__lqh]
        return zzz__ooss
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    zzz__ooss = np.nan
    if arr.dtype == types.float32:
        zzz__ooss = np.float32('nan')

    def impl(arr):
        pmte__glufu = len(arr)
        for oizfi__lqh in range(len(arr)):
            ejh__ykdsx = pmte__glufu - oizfi__lqh - 1
            if not bodo.libs.array_kernels.isna(arr, ejh__ykdsx):
                return arr[ejh__ykdsx]
        return zzz__ooss
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    bauzx__vdfae = 1 if shift > 0 else -1
    shift = bauzx__vdfae * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        hoasm__nga = get_first_non_na(in_arr[:shift])
        vhvjm__qdf = get_last_non_na(in_arr[:shift])
    else:
        hoasm__nga = get_last_non_na(in_arr[:-shift])
        vhvjm__qdf = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for oizfi__lqh in range(start, end):
        ayhs__hcyey = in_arr[oizfi__lqh - shift]
        if np.isnan(ayhs__hcyey):
            ayhs__hcyey = hoasm__nga
        else:
            hoasm__nga = ayhs__hcyey
        val = in_arr[oizfi__lqh]
        if np.isnan(val):
            val = vhvjm__qdf
        else:
            vhvjm__qdf = val
        output[oizfi__lqh] = val / ayhs__hcyey - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    flqxy__qitl = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), flqxy__qitl, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), flqxy__qitl, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), flqxy__qitl, True)
    if send_left and rank != n_pes - 1:
        amb__aoe = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), flqxy__qitl, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        amb__aoe)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    flqxy__qitl = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for vbba__bfg in range(-2, -N, -1):
        rjudp__nflir = on_arr[vbba__bfg]
        if end - rjudp__nflir >= win_size:
            halo_size = -vbba__bfg
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1),
            flqxy__qitl)
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), flqxy__qitl, True)
        xlzj__sneby = bodo.libs.distributed_api.isend(on_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), flqxy__qitl, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), flqxy__qitl)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), flqxy__qitl, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        szi__ggcmj = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), flqxy__qitl, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, xlzj__sneby, l_recv_req,
        szi__ggcmj)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    qfuf__xbs = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return qfuf__xbs != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    wlyv__nmd = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32
        (Reduce_Type.Sum.value))
    ayus__kuy = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        xslo__oki, tch__par = roll_fixed_linear_generic_seq(ayus__kuy, win,
            minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        xslo__oki = np.empty(wlyv__nmd, np.float64)
    bodo.libs.distributed_api.bcast(xslo__oki)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xslo__oki[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    wlyv__nmd = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32
        (Reduce_Type.Sum.value))
    ayus__kuy = bodo.libs.distributed_api.gatherv(in_arr)
    rkb__klea = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        xslo__oki = roll_fixed_apply_seq(ayus__kuy, rkb__klea, win, minp,
            center, kernel_func, raw)
    else:
        xslo__oki = np.empty(wlyv__nmd, np.float64)
    bodo.libs.distributed_api.bcast(xslo__oki)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xslo__oki[start:end]


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
    wlyv__nmd = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32
        (Reduce_Type.Sum.value))
    ayus__kuy = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        xslo__oki = alloc_shift(len(ayus__kuy), ayus__kuy, (-1,),
            fill_value=default_fill_value)
        shift_seq(ayus__kuy, shift, xslo__oki, default_fill_value=
            default_fill_value)
        dws__pmno = bcast_n_chars_if_str_binary_arr(xslo__oki)
    else:
        dws__pmno = bcast_n_chars_if_str_binary_arr(in_arr)
        xslo__oki = alloc_shift(wlyv__nmd, in_arr, (dws__pmno,), fill_value
            =default_fill_value)
    bodo.libs.distributed_api.bcast(xslo__oki)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xslo__oki[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    wlyv__nmd = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ayus__kuy = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        xslo__oki = pct_change_seq(ayus__kuy, shift)
    else:
        xslo__oki = alloc_pct_change(wlyv__nmd, in_arr)
    bodo.libs.distributed_api.bcast(xslo__oki)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xslo__oki[start:end]


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
        yip__czpt = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        idm__fkur = end - start
        yip__czpt = int(idm__fkur <= win_size)
    qfuf__xbs = bodo.libs.distributed_api.dist_reduce(yip__czpt, np.int32(
        Reduce_Type.Sum.value))
    return qfuf__xbs != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    wlyv__nmd = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ayus__kuy = bodo.libs.distributed_api.gatherv(in_arr)
    pze__vpcy = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(pze__vpcy, wlyv__nmd, win, False, True)
        xslo__oki = roll_var_linear_generic_seq(ayus__kuy, pze__vpcy, win,
            minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        xslo__oki = np.empty(wlyv__nmd, np.float64)
    bodo.libs.distributed_api.bcast(xslo__oki)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xslo__oki[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    wlyv__nmd = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ayus__kuy = bodo.libs.distributed_api.gatherv(in_arr)
    pze__vpcy = bodo.libs.distributed_api.gatherv(on_arr)
    rkb__klea = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(pze__vpcy, wlyv__nmd, win, False, True)
        xslo__oki = roll_variable_apply_seq(ayus__kuy, pze__vpcy, rkb__klea,
            win, minp, start, end, kernel_func, raw)
    else:
        xslo__oki = np.empty(wlyv__nmd, np.float64)
    bodo.libs.distributed_api.bcast(xslo__oki)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xslo__oki[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    wjv__cosc = len(arr)
    svre__bpat = wjv__cosc - np.isnan(arr).sum()
    A = np.empty(svre__bpat, arr.dtype)
    jbvjt__creon = 0
    for oizfi__lqh in range(wjv__cosc):
        val = arr[oizfi__lqh]
        if not np.isnan(val):
            A[jbvjt__creon] = val
            jbvjt__creon += 1
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
