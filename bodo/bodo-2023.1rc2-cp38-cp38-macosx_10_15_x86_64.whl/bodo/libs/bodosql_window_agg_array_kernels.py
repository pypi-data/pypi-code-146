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
    ppl__vwej = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        ppl__vwej += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        ppl__vwej += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        for ujzc__yuvp in range(1, len(arr_tup)):
            ppl__vwej += f"""  obs = obs | bodo.libs.array_kernels._rank_detect_ties(arr_tup[{ujzc__yuvp}]) 
"""
        ppl__vwej += '  dense = obs.cumsum()\n'
        if method == 'dense':
            ppl__vwej += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            ppl__vwej += '    dense,\n'
            ppl__vwej += '    new_dtype=np.float64,\n'
            ppl__vwej += '    copy=True,\n'
            ppl__vwej += '    nan_to_str=False,\n'
            ppl__vwej += '    from_series=True,\n'
            ppl__vwej += '  )\n'
        else:
            ppl__vwej += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            ppl__vwej += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                ppl__vwej += '  ret = count_float[dense]\n'
            elif method == 'min':
                ppl__vwej += '  ret = count_float[dense - 1] + 1\n'
            else:
                ppl__vwej += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            ppl__vwej += '  div_val = np.max(ret)\n'
        else:
            ppl__vwej += '  div_val = len(arr_tup[0])\n'
        ppl__vwej += '  for i in range(len(ret)):\n'
        ppl__vwej += '    ret[i] = ret[i] / div_val\n'
    ppl__vwej += '  return ret\n'
    znjaw__bqsz = {}
    exec(ppl__vwej, {'np': np, 'pd': pd, 'bodo': bodo}, znjaw__bqsz)
    return znjaw__bqsz['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        unhya__fabq = bodo.hiframes.pd_series_ext.get_series_data(S)
        cdbo__tzn = len(unhya__fabq)
        knh__dhn = bodo.utils.utils.alloc_type(cdbo__tzn, types.uint64, -1)
        mpr__ogvx = -1
        for ujzc__yuvp in range(cdbo__tzn):
            knh__dhn[ujzc__yuvp] = 0
            if not bodo.libs.array_kernels.isna(unhya__fabq, ujzc__yuvp):
                mpr__ogvx = ujzc__yuvp
                break
        if mpr__ogvx != -1:
            gqodh__jkot = unhya__fabq[mpr__ogvx]
            for ujzc__yuvp in range(mpr__ogvx + 1, cdbo__tzn):
                if bodo.libs.array_kernels.isna(unhya__fabq, ujzc__yuvp
                    ) or unhya__fabq[ujzc__yuvp] == gqodh__jkot:
                    knh__dhn[ujzc__yuvp] = knh__dhn[ujzc__yuvp - 1]
                else:
                    gqodh__jkot = unhya__fabq[ujzc__yuvp]
                    knh__dhn[ujzc__yuvp] = knh__dhn[ujzc__yuvp - 1] + 1
        return bodo.hiframes.pd_series_ext.init_series(knh__dhn, bodo.
            hiframes.pd_index_ext.init_range_index(0, cdbo__tzn, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    xgui__sfzb = 'res[i] = total'
    vsq__zmrk = 'constant_value = S.sum()'
    vov__lwi = 'total = 0'
    jsrdu__lsqg = 'total += elem'
    nkx__woact = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        xrtm__bwxgk = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        xrtm__bwxgk = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(xgui__sfzb, vsq__zmrk, xrtm__bwxgk, setup_block=
        vov__lwi, enter_block=jsrdu__lsqg, exit_block=nkx__woact)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    xgui__sfzb = 'res[i] = in_window'
    vsq__zmrk = 'constant_value = S.count()'
    dte__bgynn = 'res[i] = 0'
    xrtm__bwxgk = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(xgui__sfzb, vsq__zmrk, xrtm__bwxgk, empty_block=
        dte__bgynn)


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    xgui__sfzb = 'res[i] = total / in_window'
    vsq__zmrk = 'constant_value = S.mean()'
    xrtm__bwxgk = types.Array(bodo.float64, 1, 'C')
    vov__lwi = 'total = 0'
    jsrdu__lsqg = 'total += elem'
    nkx__woact = 'total -= elem'
    return gen_windowed(xgui__sfzb, vsq__zmrk, xrtm__bwxgk, setup_block=
        vov__lwi, enter_block=jsrdu__lsqg, exit_block=nkx__woact)


@numba.generated_jit(nopython=True)
def windowed_median(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_median', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    xgui__sfzb = 'res[i] = np.median(arr2)'
    vsq__zmrk = 'constant_value = S.median()'
    xrtm__bwxgk = types.Array(bodo.float64, 1, 'C')
    vov__lwi = 'arr2 = np.zeros(0, dtype=np.float64)'
    jsrdu__lsqg = 'arr2 = np.append(arr2, elem)'
    nkx__woact = 'arr2 = np.delete(arr2, np.argwhere(arr2 == elem)[0])'
    return gen_windowed(xgui__sfzb, vsq__zmrk, xrtm__bwxgk, setup_block=
        vov__lwi, enter_block=jsrdu__lsqg, exit_block=nkx__woact)


@numba.generated_jit(nopython=True)
def windowed_mode(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    if isinstance(S, bodo.SeriesType):
        xrtm__bwxgk = S.data
    else:
        xrtm__bwxgk = S
    xgui__sfzb = 'bestVal, bestCount = None, 0\n'
    xgui__sfzb += 'for key in counts:\n'
    xgui__sfzb += '   if counts[key] > bestCount:\n'
    xgui__sfzb += '      bestVal, bestCount = key, counts[key]\n'
    xgui__sfzb += 'res[i] = bestVal'
    vsq__zmrk = 'counts = {arr[0]: 0}\n'
    vsq__zmrk += 'for i in range(len(S)):\n'
    vsq__zmrk += '   if not bodo.libs.array_kernels.isna(arr, i):\n'
    vsq__zmrk += '      counts[arr[i]] = counts.get(arr[i], 0) + 1\n'
    vsq__zmrk += xgui__sfzb.replace('res[i]', 'constant_value')
    vov__lwi = 'counts = {arr[0]: 0}'
    jsrdu__lsqg = 'counts[elem] = counts.get(elem, 0) + 1'
    nkx__woact = 'counts[elem] = counts.get(elem, 0) - 1'
    return gen_windowed(xgui__sfzb, vsq__zmrk, xrtm__bwxgk, setup_block=
        vov__lwi, enter_block=jsrdu__lsqg, exit_block=nkx__woact)


@numba.generated_jit(nopython=True)
def windowed_ratio_to_report(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'ratio_to_report', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    xgui__sfzb = 'if total == 0 or bodo.libs.array_kernels.isna(arr, i):\n'
    xgui__sfzb += '   bodo.libs.array_kernels.setna(res, i)\n'
    xgui__sfzb += 'else:\n'
    xgui__sfzb += '   res[i] = arr[i] / total'
    vsq__zmrk = None
    xrtm__bwxgk = types.Array(bodo.float64, 1, 'C')
    vov__lwi = 'total = 0'
    jsrdu__lsqg = 'total += elem'
    nkx__woact = 'total -= elem'
    return gen_windowed(xgui__sfzb, vsq__zmrk, xrtm__bwxgk, setup_block=
        vov__lwi, enter_block=jsrdu__lsqg, exit_block=nkx__woact)
