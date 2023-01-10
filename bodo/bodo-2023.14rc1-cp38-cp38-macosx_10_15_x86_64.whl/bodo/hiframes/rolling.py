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
        njvu__bhtt = arr.copy(dtype=types.float64)
        return signature(njvu__bhtt, *unliteral_all(args))


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
    tzm__clf = get_overload_const_str(fname)
    if tzm__clf not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (tzm__clf))
    if tzm__clf in ('median', 'min', 'max'):
        rfh__cqx = 'def kernel_func(A):\n'
        rfh__cqx += '  if np.isnan(A).sum() != 0: return np.nan\n'
        rfh__cqx += '  return np.{}(A)\n'.format(tzm__clf)
        tzipc__azce = {}
        exec(rfh__cqx, {'np': np}, tzipc__azce)
        kernel_func = register_jitable(tzipc__azce['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        tzm__clf]
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
    tzm__clf = get_overload_const_str(fname)
    if tzm__clf not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(tzm__clf))
    if tzm__clf in ('median', 'min', 'max'):
        rfh__cqx = 'def kernel_func(A):\n'
        rfh__cqx += '  arr  = dropna(A)\n'
        rfh__cqx += '  if len(arr) == 0: return np.nan\n'
        rfh__cqx += '  return np.{}(arr)\n'.format(tzm__clf)
        tzipc__azce = {}
        exec(rfh__cqx, {'np': np, 'dropna': _dropna}, tzipc__azce)
        kernel_func = register_jitable(tzipc__azce['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        tzm__clf]
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
        kxh__pyczi = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            vdes__fiav) = kxh__pyczi
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(vdes__fiav, True)
            for cvxv__ugx in range(0, halo_size):
                data = add_obs(r_recv_buff[cvxv__ugx], *data)
                sfmzu__thhsq = in_arr[N + cvxv__ugx - win]
                data = remove_obs(sfmzu__thhsq, *data)
                output[N + cvxv__ugx - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for cvxv__ugx in range(0, halo_size):
                data = add_obs(l_recv_buff[cvxv__ugx], *data)
            for cvxv__ugx in range(0, win - 1):
                data = add_obs(in_arr[cvxv__ugx], *data)
                if cvxv__ugx > offset:
                    sfmzu__thhsq = l_recv_buff[cvxv__ugx - offset - 1]
                    data = remove_obs(sfmzu__thhsq, *data)
                if cvxv__ugx >= offset:
                    output[cvxv__ugx - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    fgir__din = max(minp, 1) - 1
    fgir__din = min(fgir__din, N)
    for cvxv__ugx in range(0, fgir__din):
        data = add_obs(in_arr[cvxv__ugx], *data)
        if cvxv__ugx >= offset:
            output[cvxv__ugx - offset] = calc_out(minp, *data)
    for cvxv__ugx in range(fgir__din, N):
        val = in_arr[cvxv__ugx]
        data = add_obs(val, *data)
        if cvxv__ugx > win - 1:
            sfmzu__thhsq = in_arr[cvxv__ugx - win]
            data = remove_obs(sfmzu__thhsq, *data)
        output[cvxv__ugx - offset] = calc_out(minp, *data)
    fbd__jqii = data
    for cvxv__ugx in range(N, N + offset):
        if cvxv__ugx > win - 1:
            sfmzu__thhsq = in_arr[cvxv__ugx - win]
            data = remove_obs(sfmzu__thhsq, *data)
        output[cvxv__ugx - offset] = calc_out(minp, *data)
    return output, fbd__jqii


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
        kxh__pyczi = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            vdes__fiav) = kxh__pyczi
        if raw == False:
            dqnbb__hpb = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, tdowr__qcw, fgi__hfbz,
                ohzd__ena, uxdbw__myyd) = dqnbb__hpb
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(fgi__hfbz, tdowr__qcw, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(vdes__fiav, True)
            if raw == False:
                bodo.libs.distributed_api.wait(uxdbw__myyd, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(ohzd__ena, True)
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
            fbd__jqii = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            luu__kir = 0
            for cvxv__ugx in range(max(N - offset, 0), N):
                data = fbd__jqii[luu__kir:luu__kir + win]
                if win - np.isnan(data).sum() < minp:
                    output[cvxv__ugx] = np.nan
                else:
                    output[cvxv__ugx] = kernel_func(data)
                luu__kir += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        fbd__jqii = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        lmxeq__mlq = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx))
        luu__kir = 0
        for cvxv__ugx in range(max(N - offset, 0), N):
            data = fbd__jqii[luu__kir:luu__kir + win]
            if win - np.isnan(data).sum() < minp:
                output[cvxv__ugx] = np.nan
            else:
                output[cvxv__ugx] = kernel_func(pd.Series(data, lmxeq__mlq[
                    luu__kir:luu__kir + win]))
            luu__kir += 1
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
            fbd__jqii = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for cvxv__ugx in range(0, win - offset - 1):
                data = fbd__jqii[cvxv__ugx:cvxv__ugx + win]
                if win - np.isnan(data).sum() < minp:
                    output[cvxv__ugx] = np.nan
                else:
                    output[cvxv__ugx] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        fbd__jqii = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        lmxeq__mlq = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for cvxv__ugx in range(0, win - offset - 1):
            data = fbd__jqii[cvxv__ugx:cvxv__ugx + win]
            if win - np.isnan(data).sum() < minp:
                output[cvxv__ugx] = np.nan
            else:
                output[cvxv__ugx] = kernel_func(pd.Series(data, lmxeq__mlq[
                    cvxv__ugx:cvxv__ugx + win]))
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
        for cvxv__ugx in range(0, N):
            start = max(cvxv__ugx - win + 1 + offset, 0)
            end = min(cvxv__ugx + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[cvxv__ugx] = np.nan
            else:
                output[cvxv__ugx] = apply_func(kernel_func, data, index_arr,
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
        kxh__pyczi = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, rrt__unwuf, l_recv_req,
            vrc__dwrtp) = kxh__pyczi
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(rrt__unwuf, rrt__unwuf, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(vrc__dwrtp, True)
            num_zero_starts = 0
            for cvxv__ugx in range(0, N):
                if start[cvxv__ugx] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for fcjq__cwe in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[fcjq__cwe], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for cvxv__ugx in range(1, num_zero_starts):
                s = recv_starts[cvxv__ugx]
                sshas__qvt = end[cvxv__ugx]
                for fcjq__cwe in range(recv_starts[cvxv__ugx - 1], s):
                    data = remove_obs(l_recv_buff[fcjq__cwe], *data)
                for fcjq__cwe in range(end[cvxv__ugx - 1], sshas__qvt):
                    data = add_obs(in_arr[fcjq__cwe], *data)
                output[cvxv__ugx] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    yag__zbk = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    ycxpv__dxbw = yag__zbk[0] - win
    if left_closed:
        ycxpv__dxbw -= 1
    recv_starts[0] = halo_size
    for fcjq__cwe in range(0, halo_size):
        if l_recv_t_buff[fcjq__cwe] > ycxpv__dxbw:
            recv_starts[0] = fcjq__cwe
            break
    for cvxv__ugx in range(1, num_zero_starts):
        ycxpv__dxbw = yag__zbk[cvxv__ugx] - win
        if left_closed:
            ycxpv__dxbw -= 1
        recv_starts[cvxv__ugx] = halo_size
        for fcjq__cwe in range(recv_starts[cvxv__ugx - 1], halo_size):
            if l_recv_t_buff[fcjq__cwe] > ycxpv__dxbw:
                recv_starts[cvxv__ugx] = fcjq__cwe
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for fcjq__cwe in range(start[0], end[0]):
        data = add_obs(in_arr[fcjq__cwe], *data)
    output[0] = calc_out(minp, *data)
    for cvxv__ugx in range(1, N):
        s = start[cvxv__ugx]
        sshas__qvt = end[cvxv__ugx]
        for fcjq__cwe in range(start[cvxv__ugx - 1], s):
            data = remove_obs(in_arr[fcjq__cwe], *data)
        for fcjq__cwe in range(end[cvxv__ugx - 1], sshas__qvt):
            data = add_obs(in_arr[fcjq__cwe], *data)
        output[cvxv__ugx] = calc_out(minp, *data)
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
        kxh__pyczi = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, rrt__unwuf, l_recv_req,
            vrc__dwrtp) = kxh__pyczi
        if raw == False:
            dqnbb__hpb = _border_icomm_var(index_arr, on_arr, rank, n_pes, win)
            (l_recv_buff_idx, zhw__fhnte, fgi__hfbz, his__fuww, ohzd__ena,
                fabv__nspo) = dqnbb__hpb
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(rrt__unwuf, rrt__unwuf, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(fgi__hfbz, fgi__hfbz, rank, n_pes, True, False)
            _border_send_wait(his__fuww, his__fuww, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(vrc__dwrtp, True)
            if raw == False:
                bodo.libs.distributed_api.wait(ohzd__ena, True)
                bodo.libs.distributed_api.wait(fabv__nspo, True)
            num_zero_starts = 0
            for cvxv__ugx in range(0, N):
                if start[cvxv__ugx] != 0:
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
            for cvxv__ugx in range(0, num_zero_starts):
                yuupg__ffq = recv_starts[cvxv__ugx]
                zmu__ugwk = np.concatenate((l_recv_buff[yuupg__ffq:],
                    in_arr[:cvxv__ugx + 1]))
                if len(zmu__ugwk) - np.isnan(zmu__ugwk).sum() >= minp:
                    output[cvxv__ugx] = kernel_func(zmu__ugwk)
                else:
                    output[cvxv__ugx] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for cvxv__ugx in range(0, num_zero_starts):
            yuupg__ffq = recv_starts[cvxv__ugx]
            zmu__ugwk = np.concatenate((l_recv_buff[yuupg__ffq:], in_arr[:
                cvxv__ugx + 1]))
            grjfv__eyvxm = np.concatenate((l_recv_buff_idx[yuupg__ffq:],
                index_arr[:cvxv__ugx + 1]))
            if len(zmu__ugwk) - np.isnan(zmu__ugwk).sum() >= minp:
                output[cvxv__ugx] = kernel_func(pd.Series(zmu__ugwk,
                    grjfv__eyvxm))
            else:
                output[cvxv__ugx] = np.nan
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
    for cvxv__ugx in range(0, N):
        s = start[cvxv__ugx]
        sshas__qvt = end[cvxv__ugx]
        data = in_arr[s:sshas__qvt]
        if sshas__qvt - s - np.isnan(data).sum() >= minp:
            output[cvxv__ugx] = kernel_func(data)
        else:
            output[cvxv__ugx] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for cvxv__ugx in range(0, N):
        s = start[cvxv__ugx]
        sshas__qvt = end[cvxv__ugx]
        data = in_arr[s:sshas__qvt]
        if sshas__qvt - s - np.isnan(data).sum() >= minp:
            output[cvxv__ugx] = kernel_func(pd.Series(data, index_arr[s:
                sshas__qvt]))
        else:
            output[cvxv__ugx] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    yag__zbk = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for cvxv__ugx in range(1, N):
        bmdt__ljrp = yag__zbk[cvxv__ugx]
        ycxpv__dxbw = yag__zbk[cvxv__ugx] - win
        if left_closed:
            ycxpv__dxbw -= 1
        start[cvxv__ugx] = cvxv__ugx
        for fcjq__cwe in range(start[cvxv__ugx - 1], cvxv__ugx):
            if yag__zbk[fcjq__cwe] > ycxpv__dxbw:
                start[cvxv__ugx] = fcjq__cwe
                break
        if yag__zbk[end[cvxv__ugx - 1]] <= bmdt__ljrp:
            end[cvxv__ugx] = cvxv__ugx + 1
        else:
            end[cvxv__ugx] = end[cvxv__ugx - 1]
        if not right_closed:
            end[cvxv__ugx] -= 1
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
        yhk__wby = sum_x / nobs
        if neg_ct == 0 and yhk__wby < 0.0:
            yhk__wby = 0
        elif neg_ct == nobs and yhk__wby > 0.0:
            yhk__wby = 0
    else:
        yhk__wby = np.nan
    return yhk__wby


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        apuwp__ojgv = val - mean_x
        mean_x += apuwp__ojgv / nobs
        ssqdm_x += (nobs - 1) * apuwp__ojgv ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            apuwp__ojgv = val - mean_x
            mean_x -= apuwp__ojgv / nobs
            ssqdm_x -= (nobs + 1) * apuwp__ojgv ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    imrcs__rhvsc = 1.0
    yhk__wby = np.nan
    if nobs >= minp and nobs > imrcs__rhvsc:
        if nobs == 1:
            yhk__wby = 0.0
        else:
            yhk__wby = ssqdm_x / (nobs - imrcs__rhvsc)
            if yhk__wby < 0.0:
                yhk__wby = 0.0
    return yhk__wby


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    risy__gjo = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(risy__gjo)


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
        kxh__pyczi = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            vdes__fiav) = kxh__pyczi
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
                bodo.libs.distributed_api.wait(vdes__fiav, True)
                for cvxv__ugx in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, cvxv__ugx):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            cvxv__ugx)
                        continue
                    output[N - halo_size + cvxv__ugx] = r_recv_buff[cvxv__ugx]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False,
    default_fill_value=None):
    N = len(in_arr)
    kxgi__dioel = 1 if shift > 0 else -1
    shift = kxgi__dioel * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
        else:
            for cvxv__ugx in range(shift):
                output[cvxv__ugx
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    start = max(shift, 0)
    end = min(N, N + shift)
    for cvxv__ugx in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, cvxv__ugx - shift):
            bodo.libs.array_kernels.setna(output, cvxv__ugx)
            continue
        output[cvxv__ugx] = in_arr[cvxv__ugx - shift]
    if shift < 0:
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
        else:
            for cvxv__ugx in range(end, N):
                output[cvxv__ugx
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for cvxv__ugx in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, cvxv__ugx):
                bodo.libs.array_kernels.setna(output, cvxv__ugx)
                continue
            output[cvxv__ugx] = l_recv_buff[cvxv__ugx]


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
        kxh__pyczi = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            vdes__fiav) = kxh__pyczi
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for cvxv__ugx in range(0, halo_size):
                    rdjxl__edem = l_recv_buff[cvxv__ugx]
                    output[cvxv__ugx] = (in_arr[cvxv__ugx] - rdjxl__edem
                        ) / rdjxl__edem
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(vdes__fiav, True)
                for cvxv__ugx in range(0, halo_size):
                    rdjxl__edem = r_recv_buff[cvxv__ugx]
                    output[N - halo_size + cvxv__ugx] = (in_arr[N -
                        halo_size + cvxv__ugx] - rdjxl__edem) / rdjxl__edem
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    affa__qam = np.nan
    if arr.dtype == types.float32:
        affa__qam = np.float32('nan')

    def impl(arr):
        for cvxv__ugx in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, cvxv__ugx):
                return arr[cvxv__ugx]
        return affa__qam
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    affa__qam = np.nan
    if arr.dtype == types.float32:
        affa__qam = np.float32('nan')

    def impl(arr):
        palj__ptd = len(arr)
        for cvxv__ugx in range(len(arr)):
            luu__kir = palj__ptd - cvxv__ugx - 1
            if not bodo.libs.array_kernels.isna(arr, luu__kir):
                return arr[luu__kir]
        return affa__qam
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    kxgi__dioel = 1 if shift > 0 else -1
    shift = kxgi__dioel * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        eprd__fhsg = get_first_non_na(in_arr[:shift])
        wcpoc__xtf = get_last_non_na(in_arr[:shift])
    else:
        eprd__fhsg = get_last_non_na(in_arr[:-shift])
        wcpoc__xtf = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for cvxv__ugx in range(start, end):
        rdjxl__edem = in_arr[cvxv__ugx - shift]
        if np.isnan(rdjxl__edem):
            rdjxl__edem = eprd__fhsg
        else:
            eprd__fhsg = rdjxl__edem
        val = in_arr[cvxv__ugx]
        if np.isnan(val):
            val = wcpoc__xtf
        else:
            wcpoc__xtf = val
        output[cvxv__ugx] = val / rdjxl__edem - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    jva__rgxn = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), jva__rgxn, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), jva__rgxn, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), jva__rgxn, True)
    if send_left and rank != n_pes - 1:
        vdes__fiav = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), jva__rgxn, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        vdes__fiav)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    jva__rgxn = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for fcjq__cwe in range(-2, -N, -1):
        cer__hpq = on_arr[fcjq__cwe]
        if end - cer__hpq >= win_size:
            halo_size = -fcjq__cwe
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1), jva__rgxn
            )
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), jva__rgxn, True)
        rrt__unwuf = bodo.libs.distributed_api.isend(on_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), jva__rgxn, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), jva__rgxn)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), jva__rgxn, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        vrc__dwrtp = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), jva__rgxn, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, rrt__unwuf, l_recv_req,
        vrc__dwrtp)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    skkv__sadxh = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return skkv__sadxh != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    vpq__ewhzw = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    oijgc__majud = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        woih__zcdho, enr__beqq = roll_fixed_linear_generic_seq(oijgc__majud,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        woih__zcdho = np.empty(vpq__ewhzw, np.float64)
    bodo.libs.distributed_api.bcast(woih__zcdho)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return woih__zcdho[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    vpq__ewhzw = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    oijgc__majud = bodo.libs.distributed_api.gatherv(in_arr)
    fcz__mwpwi = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        woih__zcdho = roll_fixed_apply_seq(oijgc__majud, fcz__mwpwi, win,
            minp, center, kernel_func, raw)
    else:
        woih__zcdho = np.empty(vpq__ewhzw, np.float64)
    bodo.libs.distributed_api.bcast(woih__zcdho)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return woih__zcdho[start:end]


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
    vpq__ewhzw = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    oijgc__majud = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        woih__zcdho = alloc_shift(len(oijgc__majud), oijgc__majud, (-1,),
            fill_value=default_fill_value)
        shift_seq(oijgc__majud, shift, woih__zcdho, default_fill_value=
            default_fill_value)
        zgv__gsd = bcast_n_chars_if_str_binary_arr(woih__zcdho)
    else:
        zgv__gsd = bcast_n_chars_if_str_binary_arr(in_arr)
        woih__zcdho = alloc_shift(vpq__ewhzw, in_arr, (zgv__gsd,),
            fill_value=default_fill_value)
    bodo.libs.distributed_api.bcast(woih__zcdho)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return woih__zcdho[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    vpq__ewhzw = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    oijgc__majud = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        woih__zcdho = pct_change_seq(oijgc__majud, shift)
    else:
        woih__zcdho = alloc_pct_change(vpq__ewhzw, in_arr)
    bodo.libs.distributed_api.bcast(woih__zcdho)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return woih__zcdho[start:end]


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
        nqzg__fnehl = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        ammgl__kkeg = end - start
        nqzg__fnehl = int(ammgl__kkeg <= win_size)
    skkv__sadxh = bodo.libs.distributed_api.dist_reduce(nqzg__fnehl, np.
        int32(Reduce_Type.Sum.value))
    return skkv__sadxh != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    vpq__ewhzw = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    oijgc__majud = bodo.libs.distributed_api.gatherv(in_arr)
    jqz__kwpqs = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(jqz__kwpqs, vpq__ewhzw, win, False, True)
        woih__zcdho = roll_var_linear_generic_seq(oijgc__majud, jqz__kwpqs,
            win, minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        woih__zcdho = np.empty(vpq__ewhzw, np.float64)
    bodo.libs.distributed_api.bcast(woih__zcdho)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return woih__zcdho[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    vpq__ewhzw = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    oijgc__majud = bodo.libs.distributed_api.gatherv(in_arr)
    jqz__kwpqs = bodo.libs.distributed_api.gatherv(on_arr)
    fcz__mwpwi = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(jqz__kwpqs, vpq__ewhzw, win, False, True)
        woih__zcdho = roll_variable_apply_seq(oijgc__majud, jqz__kwpqs,
            fcz__mwpwi, win, minp, start, end, kernel_func, raw)
    else:
        woih__zcdho = np.empty(vpq__ewhzw, np.float64)
    bodo.libs.distributed_api.bcast(woih__zcdho)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return woih__zcdho[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    pdffz__fbjgi = len(arr)
    kgi__weq = pdffz__fbjgi - np.isnan(arr).sum()
    A = np.empty(kgi__weq, arr.dtype)
    ozl__xzp = 0
    for cvxv__ugx in range(pdffz__fbjgi):
        val = arr[cvxv__ugx]
        if not np.isnan(val):
            A[ozl__xzp] = val
            ozl__xzp += 1
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
