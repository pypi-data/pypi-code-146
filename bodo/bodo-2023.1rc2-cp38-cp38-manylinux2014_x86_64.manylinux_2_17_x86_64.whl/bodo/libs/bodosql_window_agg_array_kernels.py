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
    kyebm__cnsh = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        kyebm__cnsh += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        kyebm__cnsh += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        for agxd__waep in range(1, len(arr_tup)):
            kyebm__cnsh += f"""  obs = obs | bodo.libs.array_kernels._rank_detect_ties(arr_tup[{agxd__waep}]) 
"""
        kyebm__cnsh += '  dense = obs.cumsum()\n'
        if method == 'dense':
            kyebm__cnsh += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            kyebm__cnsh += '    dense,\n'
            kyebm__cnsh += '    new_dtype=np.float64,\n'
            kyebm__cnsh += '    copy=True,\n'
            kyebm__cnsh += '    nan_to_str=False,\n'
            kyebm__cnsh += '    from_series=True,\n'
            kyebm__cnsh += '  )\n'
        else:
            kyebm__cnsh += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            kyebm__cnsh += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                kyebm__cnsh += '  ret = count_float[dense]\n'
            elif method == 'min':
                kyebm__cnsh += '  ret = count_float[dense - 1] + 1\n'
            else:
                kyebm__cnsh += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            kyebm__cnsh += '  div_val = np.max(ret)\n'
        else:
            kyebm__cnsh += '  div_val = len(arr_tup[0])\n'
        kyebm__cnsh += '  for i in range(len(ret)):\n'
        kyebm__cnsh += '    ret[i] = ret[i] / div_val\n'
    kyebm__cnsh += '  return ret\n'
    rawlo__kwrt = {}
    exec(kyebm__cnsh, {'np': np, 'pd': pd, 'bodo': bodo}, rawlo__kwrt)
    return rawlo__kwrt['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        kyfg__wtibt = bodo.hiframes.pd_series_ext.get_series_data(S)
        kiuu__dmmwv = len(kyfg__wtibt)
        rqwz__ltwoe = bodo.utils.utils.alloc_type(kiuu__dmmwv, types.uint64, -1
            )
        rrxh__udw = -1
        for agxd__waep in range(kiuu__dmmwv):
            rqwz__ltwoe[agxd__waep] = 0
            if not bodo.libs.array_kernels.isna(kyfg__wtibt, agxd__waep):
                rrxh__udw = agxd__waep
                break
        if rrxh__udw != -1:
            lyb__ohwo = kyfg__wtibt[rrxh__udw]
            for agxd__waep in range(rrxh__udw + 1, kiuu__dmmwv):
                if bodo.libs.array_kernels.isna(kyfg__wtibt, agxd__waep
                    ) or kyfg__wtibt[agxd__waep] == lyb__ohwo:
                    rqwz__ltwoe[agxd__waep] = rqwz__ltwoe[agxd__waep - 1]
                else:
                    lyb__ohwo = kyfg__wtibt[agxd__waep]
                    rqwz__ltwoe[agxd__waep] = rqwz__ltwoe[agxd__waep - 1] + 1
        return bodo.hiframes.pd_series_ext.init_series(rqwz__ltwoe, bodo.
            hiframes.pd_index_ext.init_range_index(0, kiuu__dmmwv, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    uzceg__ucge = 'res[i] = total'
    bzppa__rfo = 'constant_value = S.sum()'
    ishy__hghi = 'total = 0'
    krtae__gdkbw = 'total += elem'
    xgba__xuan = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        rbio__aic = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        rbio__aic = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(uzceg__ucge, bzppa__rfo, rbio__aic, setup_block=
        ishy__hghi, enter_block=krtae__gdkbw, exit_block=xgba__xuan)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    uzceg__ucge = 'res[i] = in_window'
    bzppa__rfo = 'constant_value = S.count()'
    elekc__kui = 'res[i] = 0'
    rbio__aic = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(uzceg__ucge, bzppa__rfo, rbio__aic, empty_block=
        elekc__kui)


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    uzceg__ucge = 'res[i] = total / in_window'
    bzppa__rfo = 'constant_value = S.mean()'
    rbio__aic = types.Array(bodo.float64, 1, 'C')
    ishy__hghi = 'total = 0'
    krtae__gdkbw = 'total += elem'
    xgba__xuan = 'total -= elem'
    return gen_windowed(uzceg__ucge, bzppa__rfo, rbio__aic, setup_block=
        ishy__hghi, enter_block=krtae__gdkbw, exit_block=xgba__xuan)


@numba.generated_jit(nopython=True)
def windowed_median(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_median', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    uzceg__ucge = 'res[i] = np.median(arr2)'
    bzppa__rfo = 'constant_value = S.median()'
    rbio__aic = types.Array(bodo.float64, 1, 'C')
    ishy__hghi = 'arr2 = np.zeros(0, dtype=np.float64)'
    krtae__gdkbw = 'arr2 = np.append(arr2, elem)'
    xgba__xuan = 'arr2 = np.delete(arr2, np.argwhere(arr2 == elem)[0])'
    return gen_windowed(uzceg__ucge, bzppa__rfo, rbio__aic, setup_block=
        ishy__hghi, enter_block=krtae__gdkbw, exit_block=xgba__xuan)


@numba.generated_jit(nopython=True)
def windowed_mode(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    if isinstance(S, bodo.SeriesType):
        rbio__aic = S.data
    else:
        rbio__aic = S
    uzceg__ucge = 'bestVal, bestCount = None, 0\n'
    uzceg__ucge += 'for key in counts:\n'
    uzceg__ucge += '   if counts[key] > bestCount:\n'
    uzceg__ucge += '      bestVal, bestCount = key, counts[key]\n'
    uzceg__ucge += 'res[i] = bestVal'
    bzppa__rfo = 'counts = {arr[0]: 0}\n'
    bzppa__rfo += 'for i in range(len(S)):\n'
    bzppa__rfo += '   if not bodo.libs.array_kernels.isna(arr, i):\n'
    bzppa__rfo += '      counts[arr[i]] = counts.get(arr[i], 0) + 1\n'
    bzppa__rfo += uzceg__ucge.replace('res[i]', 'constant_value')
    ishy__hghi = 'counts = {arr[0]: 0}'
    krtae__gdkbw = 'counts[elem] = counts.get(elem, 0) + 1'
    xgba__xuan = 'counts[elem] = counts.get(elem, 0) - 1'
    return gen_windowed(uzceg__ucge, bzppa__rfo, rbio__aic, setup_block=
        ishy__hghi, enter_block=krtae__gdkbw, exit_block=xgba__xuan)


@numba.generated_jit(nopython=True)
def windowed_ratio_to_report(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'ratio_to_report', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    uzceg__ucge = 'if total == 0 or bodo.libs.array_kernels.isna(arr, i):\n'
    uzceg__ucge += '   bodo.libs.array_kernels.setna(res, i)\n'
    uzceg__ucge += 'else:\n'
    uzceg__ucge += '   res[i] = arr[i] / total'
    bzppa__rfo = None
    rbio__aic = types.Array(bodo.float64, 1, 'C')
    ishy__hghi = 'total = 0'
    krtae__gdkbw = 'total += elem'
    xgba__xuan = 'total -= elem'
    return gen_windowed(uzceg__ucge, bzppa__rfo, rbio__aic, setup_block=
        ishy__hghi, enter_block=krtae__gdkbw, exit_block=xgba__xuan)
