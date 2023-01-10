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
    avoj__puaed = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        avoj__puaed += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        avoj__puaed += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        for ikeep__avl in range(1, len(arr_tup)):
            avoj__puaed += f"""  obs = obs | bodo.libs.array_kernels._rank_detect_ties(arr_tup[{ikeep__avl}]) 
"""
        avoj__puaed += '  dense = obs.cumsum()\n'
        if method == 'dense':
            avoj__puaed += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            avoj__puaed += '    dense,\n'
            avoj__puaed += '    new_dtype=np.float64,\n'
            avoj__puaed += '    copy=True,\n'
            avoj__puaed += '    nan_to_str=False,\n'
            avoj__puaed += '    from_series=True,\n'
            avoj__puaed += '  )\n'
        else:
            avoj__puaed += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            avoj__puaed += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                avoj__puaed += '  ret = count_float[dense]\n'
            elif method == 'min':
                avoj__puaed += '  ret = count_float[dense - 1] + 1\n'
            else:
                avoj__puaed += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            avoj__puaed += '  div_val = np.max(ret)\n'
        else:
            avoj__puaed += '  div_val = len(arr_tup[0])\n'
        avoj__puaed += '  for i in range(len(ret)):\n'
        avoj__puaed += '    ret[i] = ret[i] / div_val\n'
    avoj__puaed += '  return ret\n'
    ugjqj__wto = {}
    exec(avoj__puaed, {'np': np, 'pd': pd, 'bodo': bodo}, ugjqj__wto)
    return ugjqj__wto['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        qbx__ken = bodo.hiframes.pd_series_ext.get_series_data(S)
        gcy__baaxp = len(qbx__ken)
        bid__vbii = bodo.utils.utils.alloc_type(gcy__baaxp, types.uint64, -1)
        nfbfi__hsxv = -1
        for ikeep__avl in range(gcy__baaxp):
            bid__vbii[ikeep__avl] = 0
            if not bodo.libs.array_kernels.isna(qbx__ken, ikeep__avl):
                nfbfi__hsxv = ikeep__avl
                break
        if nfbfi__hsxv != -1:
            vgkhf__gpa = qbx__ken[nfbfi__hsxv]
            for ikeep__avl in range(nfbfi__hsxv + 1, gcy__baaxp):
                if bodo.libs.array_kernels.isna(qbx__ken, ikeep__avl
                    ) or qbx__ken[ikeep__avl] == vgkhf__gpa:
                    bid__vbii[ikeep__avl] = bid__vbii[ikeep__avl - 1]
                else:
                    vgkhf__gpa = qbx__ken[ikeep__avl]
                    bid__vbii[ikeep__avl] = bid__vbii[ikeep__avl - 1] + 1
        return bodo.hiframes.pd_series_ext.init_series(bid__vbii, bodo.
            hiframes.pd_index_ext.init_range_index(0, gcy__baaxp, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    vwir__jfts = 'res[i] = total'
    xglpw__xaeje = 'constant_value = S.sum()'
    uev__ipboi = 'total = 0'
    qsocy__tjuvx = 'total += elem'
    fjx__hco = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        mzv__coip = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        mzv__coip = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(vwir__jfts, xglpw__xaeje, mzv__coip, setup_block=
        uev__ipboi, enter_block=qsocy__tjuvx, exit_block=fjx__hco)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    vwir__jfts = 'res[i] = in_window'
    xglpw__xaeje = 'constant_value = S.count()'
    zxctn__yfbig = 'res[i] = 0'
    mzv__coip = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(vwir__jfts, xglpw__xaeje, mzv__coip, empty_block=
        zxctn__yfbig)


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    vwir__jfts = 'res[i] = total / in_window'
    xglpw__xaeje = 'constant_value = S.mean()'
    mzv__coip = types.Array(bodo.float64, 1, 'C')
    uev__ipboi = 'total = 0'
    qsocy__tjuvx = 'total += elem'
    fjx__hco = 'total -= elem'
    return gen_windowed(vwir__jfts, xglpw__xaeje, mzv__coip, setup_block=
        uev__ipboi, enter_block=qsocy__tjuvx, exit_block=fjx__hco)


@numba.generated_jit(nopython=True)
def windowed_median(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_median', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    vwir__jfts = 'res[i] = np.median(arr2)'
    xglpw__xaeje = 'constant_value = S.median()'
    mzv__coip = types.Array(bodo.float64, 1, 'C')
    uev__ipboi = 'arr2 = np.zeros(0, dtype=np.float64)'
    qsocy__tjuvx = 'arr2 = np.append(arr2, elem)'
    fjx__hco = 'arr2 = np.delete(arr2, np.argwhere(arr2 == elem)[0])'
    return gen_windowed(vwir__jfts, xglpw__xaeje, mzv__coip, setup_block=
        uev__ipboi, enter_block=qsocy__tjuvx, exit_block=fjx__hco)


@numba.generated_jit(nopython=True)
def windowed_mode(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    if isinstance(S, bodo.SeriesType):
        mzv__coip = S.data
    else:
        mzv__coip = S
    vwir__jfts = 'bestVal, bestCount = None, 0\n'
    vwir__jfts += 'for key in counts:\n'
    vwir__jfts += '   if counts[key] > bestCount:\n'
    vwir__jfts += '      bestVal, bestCount = key, counts[key]\n'
    vwir__jfts += 'res[i] = bestVal'
    xglpw__xaeje = 'counts = {arr[0]: 0}\n'
    xglpw__xaeje += 'for i in range(len(S)):\n'
    xglpw__xaeje += '   if not bodo.libs.array_kernels.isna(arr, i):\n'
    xglpw__xaeje += '      counts[arr[i]] = counts.get(arr[i], 0) + 1\n'
    xglpw__xaeje += vwir__jfts.replace('res[i]', 'constant_value')
    uev__ipboi = 'counts = {arr[0]: 0}'
    qsocy__tjuvx = 'counts[elem] = counts.get(elem, 0) + 1'
    fjx__hco = 'counts[elem] = counts.get(elem, 0) - 1'
    return gen_windowed(vwir__jfts, xglpw__xaeje, mzv__coip, setup_block=
        uev__ipboi, enter_block=qsocy__tjuvx, exit_block=fjx__hco)


@numba.generated_jit(nopython=True)
def windowed_ratio_to_report(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'ratio_to_report', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    vwir__jfts = 'if total == 0 or bodo.libs.array_kernels.isna(arr, i):\n'
    vwir__jfts += '   bodo.libs.array_kernels.setna(res, i)\n'
    vwir__jfts += 'else:\n'
    vwir__jfts += '   res[i] = arr[i] / total'
    xglpw__xaeje = None
    mzv__coip = types.Array(bodo.float64, 1, 'C')
    uev__ipboi = 'total = 0'
    qsocy__tjuvx = 'total += elem'
    fjx__hco = 'total -= elem'
    return gen_windowed(vwir__jfts, xglpw__xaeje, mzv__coip, setup_block=
        uev__ipboi, enter_block=qsocy__tjuvx, exit_block=fjx__hco)
