"""
Implements window/aggregation array kernels that are specific to BodoSQL.
Specifically, window/aggregation array kernels that do not concern window
frames.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, raise_bodo_error


def rank_sql(arr_tup, method='average', pct=False):
    return


@overload(rank_sql, no_unliteral=True)
def overload_rank_sql(arr_tup, method='average', pct=False):
    if not is_overload_constant_str(method):
        raise_bodo_error(
            "Series.rank(): 'method' argument must be a constant string")
    method = get_overload_const_str(method)
    if not is_overload_constant_bool(pct):
        raise_bodo_error(
            "Series.rank(): 'pct' argument must be a constant boolean")
    pct = get_overload_const_bool(pct)
    ausu__ttv = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        ausu__ttv += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        ausu__ttv += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        for tqtpx__ify in range(1, len(arr_tup)):
            ausu__ttv += f"""  obs = obs | bodo.libs.array_kernels._rank_detect_ties(arr_tup[{tqtpx__ify}]) 
"""
        ausu__ttv += '  dense = obs.cumsum()\n'
        if method == 'dense':
            ausu__ttv += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            ausu__ttv += '    dense,\n'
            ausu__ttv += '    new_dtype=np.float64,\n'
            ausu__ttv += '    copy=True,\n'
            ausu__ttv += '    nan_to_str=False,\n'
            ausu__ttv += '    from_series=True,\n'
            ausu__ttv += '  )\n'
        else:
            ausu__ttv += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            ausu__ttv += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                ausu__ttv += '  ret = count_float[dense]\n'
            elif method == 'min':
                ausu__ttv += '  ret = count_float[dense - 1] + 1\n'
            else:
                ausu__ttv += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            ausu__ttv += '  div_val = np.max(ret)\n'
        else:
            ausu__ttv += '  div_val = len(arr_tup[0])\n'
        ausu__ttv += '  for i in range(len(ret)):\n'
        ausu__ttv += '    ret[i] = ret[i] / div_val\n'
    ausu__ttv += '  return ret\n'
    xluo__fvhze = {}
    exec(ausu__ttv, {'np': np, 'pd': pd, 'bodo': bodo}, xluo__fvhze)
    return xluo__fvhze['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        dhwgt__noo = bodo.hiframes.pd_series_ext.get_series_data(S)
        qqg__zcf = len(dhwgt__noo)
        hdcs__bqn = bodo.utils.utils.alloc_type(qqg__zcf, types.uint64, -1)
        dezyu__xkc = -1
        for tqtpx__ify in range(qqg__zcf):
            hdcs__bqn[tqtpx__ify] = 0
            if not bodo.libs.array_kernels.isna(dhwgt__noo, tqtpx__ify):
                dezyu__xkc = tqtpx__ify
                break
        if dezyu__xkc != -1:
            wkvjq__tqv = dhwgt__noo[dezyu__xkc]
            for tqtpx__ify in range(dezyu__xkc + 1, qqg__zcf):
                if bodo.libs.array_kernels.isna(dhwgt__noo, tqtpx__ify
                    ) or dhwgt__noo[tqtpx__ify] == wkvjq__tqv:
                    hdcs__bqn[tqtpx__ify] = hdcs__bqn[tqtpx__ify - 1]
                else:
                    wkvjq__tqv = dhwgt__noo[tqtpx__ify]
                    hdcs__bqn[tqtpx__ify] = hdcs__bqn[tqtpx__ify - 1] + 1
        return bodo.hiframes.pd_series_ext.init_series(hdcs__bqn, bodo.
            hiframes.pd_index_ext.init_range_index(0, qqg__zcf, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    ixggz__kfsaf = 'res[i] = total'
    jnwhx__rtqbd = 'constant_value = S.sum()'
    rtwm__kcmq = 'total = 0'
    fqgr__ctj = 'total += elem'
    xgil__fsiwz = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        orvc__bxqaz = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        orvc__bxqaz = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(ixggz__kfsaf, jnwhx__rtqbd, orvc__bxqaz,
        setup_block=rtwm__kcmq, enter_block=fqgr__ctj, exit_block=xgil__fsiwz)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    ixggz__kfsaf = 'res[i] = in_window'
    jnwhx__rtqbd = 'constant_value = S.count()'
    uni__zkbnr = 'res[i] = 0'
    orvc__bxqaz = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(ixggz__kfsaf, jnwhx__rtqbd, orvc__bxqaz,
        empty_block=uni__zkbnr)


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    ixggz__kfsaf = 'res[i] = total / in_window'
    jnwhx__rtqbd = 'constant_value = S.mean()'
    orvc__bxqaz = types.Array(bodo.float64, 1, 'C')
    rtwm__kcmq = 'total = 0'
    fqgr__ctj = 'total += elem'
    xgil__fsiwz = 'total -= elem'
    return gen_windowed(ixggz__kfsaf, jnwhx__rtqbd, orvc__bxqaz,
        setup_block=rtwm__kcmq, enter_block=fqgr__ctj, exit_block=xgil__fsiwz)


@numba.generated_jit(nopython=True)
def windowed_median(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_median', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    ixggz__kfsaf = 'res[i] = np.median(arr2)'
    jnwhx__rtqbd = 'constant_value = S.median()'
    orvc__bxqaz = types.Array(bodo.float64, 1, 'C')
    rtwm__kcmq = 'arr2 = np.zeros(0, dtype=np.float64)'
    fqgr__ctj = 'arr2 = np.append(arr2, elem)'
    xgil__fsiwz = 'arr2 = np.delete(arr2, np.argwhere(arr2 == elem)[0])'
    return gen_windowed(ixggz__kfsaf, jnwhx__rtqbd, orvc__bxqaz,
        setup_block=rtwm__kcmq, enter_block=fqgr__ctj, exit_block=xgil__fsiwz)


@numba.generated_jit(nopython=True)
def windowed_mode(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    if isinstance(S, bodo.SeriesType):
        orvc__bxqaz = S.data
    else:
        orvc__bxqaz = S
    ixggz__kfsaf = 'bestVal, bestCount = None, 0\n'
    ixggz__kfsaf += 'for key in counts:\n'
    ixggz__kfsaf += '   if counts[key] > bestCount:\n'
    ixggz__kfsaf += '      bestVal, bestCount = key, counts[key]\n'
    ixggz__kfsaf += 'res[i] = bestVal'
    jnwhx__rtqbd = 'counts = {arr[0]: 0}\n'
    jnwhx__rtqbd += 'for i in range(len(S)):\n'
    jnwhx__rtqbd += '   if not bodo.libs.array_kernels.isna(arr, i):\n'
    jnwhx__rtqbd += '      counts[arr[i]] = counts.get(arr[i], 0) + 1\n'
    jnwhx__rtqbd += ixggz__kfsaf.replace('res[i]', 'constant_value')
    rtwm__kcmq = 'counts = {arr[0]: 0}'
    fqgr__ctj = 'counts[elem] = counts.get(elem, 0) + 1'
    xgil__fsiwz = 'counts[elem] = counts.get(elem, 0) - 1'
    return gen_windowed(ixggz__kfsaf, jnwhx__rtqbd, orvc__bxqaz,
        setup_block=rtwm__kcmq, enter_block=fqgr__ctj, exit_block=xgil__fsiwz)


@numba.generated_jit(nopython=True)
def windowed_ratio_to_report(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'ratio_to_report', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    ixggz__kfsaf = 'if total == 0 or bodo.libs.array_kernels.isna(arr, i):\n'
    ixggz__kfsaf += '   bodo.libs.array_kernels.setna(res, i)\n'
    ixggz__kfsaf += 'else:\n'
    ixggz__kfsaf += '   res[i] = arr[i] / total'
    jnwhx__rtqbd = None
    orvc__bxqaz = types.Array(bodo.float64, 1, 'C')
    rtwm__kcmq = 'total = 0'
    fqgr__ctj = 'total += elem'
    xgil__fsiwz = 'total -= elem'
    return gen_windowed(ixggz__kfsaf, jnwhx__rtqbd, orvc__bxqaz,
        setup_block=rtwm__kcmq, enter_block=fqgr__ctj, exit_block=xgil__fsiwz)
