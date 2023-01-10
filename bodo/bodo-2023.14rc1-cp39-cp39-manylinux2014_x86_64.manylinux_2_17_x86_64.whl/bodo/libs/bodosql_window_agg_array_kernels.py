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
    zyl__txgz = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        zyl__txgz += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        zyl__txgz += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        for vbvt__brv in range(1, len(arr_tup)):
            zyl__txgz += f"""  obs = obs | bodo.libs.array_kernels._rank_detect_ties(arr_tup[{vbvt__brv}]) 
"""
        zyl__txgz += '  dense = obs.cumsum()\n'
        if method == 'dense':
            zyl__txgz += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            zyl__txgz += '    dense,\n'
            zyl__txgz += '    new_dtype=np.float64,\n'
            zyl__txgz += '    copy=True,\n'
            zyl__txgz += '    nan_to_str=False,\n'
            zyl__txgz += '    from_series=True,\n'
            zyl__txgz += '  )\n'
        else:
            zyl__txgz += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            zyl__txgz += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                zyl__txgz += '  ret = count_float[dense]\n'
            elif method == 'min':
                zyl__txgz += '  ret = count_float[dense - 1] + 1\n'
            else:
                zyl__txgz += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            zyl__txgz += '  div_val = np.max(ret)\n'
        else:
            zyl__txgz += '  div_val = len(arr_tup[0])\n'
        zyl__txgz += '  for i in range(len(ret)):\n'
        zyl__txgz += '    ret[i] = ret[i] / div_val\n'
    zyl__txgz += '  return ret\n'
    qvcc__ery = {}
    exec(zyl__txgz, {'np': np, 'pd': pd, 'bodo': bodo}, qvcc__ery)
    return qvcc__ery['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        xusu__rvkb = bodo.hiframes.pd_series_ext.get_series_data(S)
        ntefl__kdefz = len(xusu__rvkb)
        xykb__ygm = bodo.utils.utils.alloc_type(ntefl__kdefz, types.uint64, -1)
        yrwye__cbq = -1
        for vbvt__brv in range(ntefl__kdefz):
            xykb__ygm[vbvt__brv] = 0
            if not bodo.libs.array_kernels.isna(xusu__rvkb, vbvt__brv):
                yrwye__cbq = vbvt__brv
                break
        if yrwye__cbq != -1:
            zqjr__upp = xusu__rvkb[yrwye__cbq]
            for vbvt__brv in range(yrwye__cbq + 1, ntefl__kdefz):
                if bodo.libs.array_kernels.isna(xusu__rvkb, vbvt__brv
                    ) or xusu__rvkb[vbvt__brv] == zqjr__upp:
                    xykb__ygm[vbvt__brv] = xykb__ygm[vbvt__brv - 1]
                else:
                    zqjr__upp = xusu__rvkb[vbvt__brv]
                    xykb__ygm[vbvt__brv] = xykb__ygm[vbvt__brv - 1] + 1
        return bodo.hiframes.pd_series_ext.init_series(xykb__ygm, bodo.
            hiframes.pd_index_ext.init_range_index(0, ntefl__kdefz, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    kxc__lijhw = 'res[i] = total'
    dev__uykyg = 'constant_value = S.sum()'
    smb__blzyt = 'total = 0'
    vroxr__vaay = 'total += elem'
    uxwab__xfl = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        ekb__uqn = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        ekb__uqn = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(kxc__lijhw, dev__uykyg, ekb__uqn, setup_block=
        smb__blzyt, enter_block=vroxr__vaay, exit_block=uxwab__xfl)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    kxc__lijhw = 'res[i] = in_window'
    dev__uykyg = 'constant_value = S.count()'
    ptyt__vtgjb = 'res[i] = 0'
    ekb__uqn = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(kxc__lijhw, dev__uykyg, ekb__uqn, empty_block=
        ptyt__vtgjb)


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    kxc__lijhw = 'res[i] = total / in_window'
    dev__uykyg = 'constant_value = S.mean()'
    ekb__uqn = types.Array(bodo.float64, 1, 'C')
    smb__blzyt = 'total = 0'
    vroxr__vaay = 'total += elem'
    uxwab__xfl = 'total -= elem'
    return gen_windowed(kxc__lijhw, dev__uykyg, ekb__uqn, setup_block=
        smb__blzyt, enter_block=vroxr__vaay, exit_block=uxwab__xfl)


@numba.generated_jit(nopython=True)
def windowed_median(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_median', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    kxc__lijhw = 'res[i] = np.median(arr2)'
    dev__uykyg = 'constant_value = S.median()'
    ekb__uqn = types.Array(bodo.float64, 1, 'C')
    smb__blzyt = 'arr2 = np.zeros(0, dtype=np.float64)'
    vroxr__vaay = 'arr2 = np.append(arr2, elem)'
    uxwab__xfl = 'arr2 = np.delete(arr2, np.argwhere(arr2 == elem)[0])'
    return gen_windowed(kxc__lijhw, dev__uykyg, ekb__uqn, setup_block=
        smb__blzyt, enter_block=vroxr__vaay, exit_block=uxwab__xfl)


@numba.generated_jit(nopython=True)
def windowed_mode(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    if isinstance(S, bodo.SeriesType):
        ekb__uqn = S.data
    else:
        ekb__uqn = S
    kxc__lijhw = 'bestVal, bestCount = None, 0\n'
    kxc__lijhw += 'for key in counts:\n'
    kxc__lijhw += '   if counts[key] > bestCount:\n'
    kxc__lijhw += '      bestVal, bestCount = key, counts[key]\n'
    kxc__lijhw += 'res[i] = bestVal'
    dev__uykyg = 'counts = {arr[0]: 0}\n'
    dev__uykyg += 'for i in range(len(S)):\n'
    dev__uykyg += '   if not bodo.libs.array_kernels.isna(arr, i):\n'
    dev__uykyg += '      counts[arr[i]] = counts.get(arr[i], 0) + 1\n'
    dev__uykyg += kxc__lijhw.replace('res[i]', 'constant_value')
    smb__blzyt = 'counts = {arr[0]: 0}'
    vroxr__vaay = 'counts[elem] = counts.get(elem, 0) + 1'
    uxwab__xfl = 'counts[elem] = counts.get(elem, 0) - 1'
    return gen_windowed(kxc__lijhw, dev__uykyg, ekb__uqn, setup_block=
        smb__blzyt, enter_block=vroxr__vaay, exit_block=uxwab__xfl)


@numba.generated_jit(nopython=True)
def windowed_ratio_to_report(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'ratio_to_report', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    kxc__lijhw = 'if total == 0 or bodo.libs.array_kernels.isna(arr, i):\n'
    kxc__lijhw += '   bodo.libs.array_kernels.setna(res, i)\n'
    kxc__lijhw += 'else:\n'
    kxc__lijhw += '   res[i] = arr[i] / total'
    dev__uykyg = None
    ekb__uqn = types.Array(bodo.float64, 1, 'C')
    smb__blzyt = 'total = 0'
    vroxr__vaay = 'total += elem'
    uxwab__xfl = 'total -= elem'
    return gen_windowed(kxc__lijhw, dev__uykyg, ekb__uqn, setup_block=
        smb__blzyt, enter_block=vroxr__vaay, exit_block=uxwab__xfl)
