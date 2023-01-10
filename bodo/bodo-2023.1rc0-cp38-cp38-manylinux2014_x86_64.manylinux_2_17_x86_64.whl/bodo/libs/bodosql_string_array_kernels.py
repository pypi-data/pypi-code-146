"""
Implements string array kernels that are specific to BodoSQL
"""
import numba
import numpy as np
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


@numba.generated_jit(nopython=True)
def char(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.char_util',
            ['arr'], 0)

    def impl(arr):
        return char_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def contains(arr, pattern):
    args = [arr, pattern]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.contains',
                ['arr', 'contains'], oih__nkf)

    def impl(arr, pattern):
        return contains_util(arr, pattern)
    return impl


@numba.generated_jit(nopython=True)
def contains_util(arr, pattern):
    verify_string_binary_arg(arr, 'CONTAINS', 'arr')
    verify_string_binary_arg(pattern, 'CONTAINS', 'pattern')
    mbo__pdki = bodo.boolean_array
    urn__zlg = ['arr', 'pattern']
    nhrt__yzeb = [arr, pattern]
    ded__ovd = [True] * 2
    guwb__oijzq = 'res[i] = arg1 in arg0\n'
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def editdistance_no_max(s, t):
    args = [s, t]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], oih__nkf)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], oih__nkf)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def endswith(source, suffix):
    args = [source, suffix]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.endswith',
                ['source', 'suffix'], oih__nkf)

    def impl(source, suffix):
        return endswith_util(source, suffix)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], oih__nkf)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], oih__nkf)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def insert(source, pos, length, inject):
    args = [source, pos, length, inject]
    for oih__nkf in range(4):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.insert',
                ['source', 'pos', 'length', 'inject'], oih__nkf)

    def impl(source, pos, length, inject):
        return insert_util(source, pos, length, inject)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], oih__nkf)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], oih__nkf)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], oih__nkf)

    def impl(arr, length, padstr):
        return lpad_util(arr, length, padstr)
    return impl


@numba.generated_jit(nopython=True)
def ord_ascii(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.ord_ascii_util',
            ['arr'], 0)

    def impl(arr):
        return ord_ascii_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def position(substr, source, start):
    args = [substr, source, start]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.position',
                ['substr', 'source', 'start'], oih__nkf)

    def impl(substr, source, start):
        return position_util(substr, source, start)
    return impl


@numba.generated_jit(nopython=True)
def repeat(arr, repeats):
    args = [arr, repeats]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], oih__nkf)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], oih__nkf)

    def impl(arr, to_replace, replace_with):
        return replace_util(arr, to_replace, replace_with)
    return impl


@numba.generated_jit(nopython=True)
def reverse(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.reverse_util',
            ['arr'], 0)

    def impl(arr):
        return reverse_util(arr)
    return impl


def right(arr, n_chars):
    return


@overload(right)
def overload_right(arr, n_chars):
    args = [arr, n_chars]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], oih__nkf)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], oih__nkf)

    def impl(arr, length, padstr):
        return rpad_util(arr, length, padstr)
    return impl


@numba.generated_jit(nopython=True)
def rtrimmed_length(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.rtrimmed_length_util', ['arr'], 0)

    def impl(arr):
        return rtrimmed_length_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def space(n_chars):
    if isinstance(n_chars, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.space_util',
            ['n_chars'], 0)

    def impl(n_chars):
        return space_util(n_chars)
    return impl


@numba.generated_jit(nopython=True)
def split_part(source, delim, part):
    args = [source, delim, part]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], oih__nkf)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def startswith(source, prefix):
    args = [source, prefix]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.startswith',
                ['source', 'prefix'], oih__nkf)

    def impl(source, prefix):
        return startswith_util(source, prefix)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for oih__nkf in range(2):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], oih__nkf)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], oih__nkf)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], oih__nkf)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], oih__nkf)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for oih__nkf in range(3):
        if isinstance(args[oih__nkf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], oih__nkf)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    urn__zlg = ['arr']
    nhrt__yzeb = [arr]
    ded__ovd = [True]
    guwb__oijzq = 'if 0 <= arg0 <= 127:\n'
    guwb__oijzq += '   res[i] = chr(arg0)\n'
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '   bodo.libs.array_kernels.setna(res, i)\n'
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    urn__zlg = ['arr', 'delim']
    nhrt__yzeb = [arr, delim]
    ded__ovd = [True] * 2
    guwb__oijzq = 'capitalized = arg0[:1].upper()\n'
    guwb__oijzq += 'for j in range(1, len(arg0)):\n'
    guwb__oijzq += '   if arg0[j-1] in arg1:\n'
    guwb__oijzq += '      capitalized += arg0[j].upper()\n'
    guwb__oijzq += '   else:\n'
    guwb__oijzq += '      capitalized += arg0[j].lower()\n'
    guwb__oijzq += 'res[i] = capitalized'
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    urn__zlg = ['arr', 'target']
    nhrt__yzeb = [arr, target]
    ded__ovd = [True] * 2
    guwb__oijzq = 'res[i] = arg0.find(arg1) + 1'
    mbo__pdki = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    hyl__cpo, hww__mjgf = len(s), len(t)
    lapm__tynh, kds__lrh = 1, 0
    arr = np.zeros((2, hyl__cpo + 1), dtype=np.uint32)
    arr[0, :] = np.arange(hyl__cpo + 1)
    for oih__nkf in range(1, hww__mjgf + 1):
        arr[lapm__tynh, 0] = oih__nkf
        for zmym__xdsk in range(1, hyl__cpo + 1):
            if s[zmym__xdsk - 1] == t[oih__nkf - 1]:
                arr[lapm__tynh, zmym__xdsk] = arr[kds__lrh, zmym__xdsk - 1]
            else:
                arr[lapm__tynh, zmym__xdsk] = 1 + min(arr[lapm__tynh, 
                    zmym__xdsk - 1], arr[kds__lrh, zmym__xdsk], arr[
                    kds__lrh, zmym__xdsk - 1])
        lapm__tynh, kds__lrh = kds__lrh, lapm__tynh
    return arr[hww__mjgf % 2, hyl__cpo]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    hyl__cpo, hww__mjgf = len(s), len(t)
    if hyl__cpo <= maxDistance and hww__mjgf <= maxDistance:
        return min_edit_distance(s, t)
    lapm__tynh, kds__lrh = 1, 0
    arr = np.zeros((2, hyl__cpo + 1), dtype=np.uint32)
    arr[0, :] = np.arange(hyl__cpo + 1)
    for oih__nkf in range(1, hww__mjgf + 1):
        arr[lapm__tynh, 0] = oih__nkf
        for zmym__xdsk in range(1, hyl__cpo + 1):
            if s[zmym__xdsk - 1] == t[oih__nkf - 1]:
                arr[lapm__tynh, zmym__xdsk] = arr[kds__lrh, zmym__xdsk - 1]
            else:
                arr[lapm__tynh, zmym__xdsk] = 1 + min(arr[lapm__tynh, 
                    zmym__xdsk - 1], arr[kds__lrh, zmym__xdsk], arr[
                    kds__lrh, zmym__xdsk - 1])
        if (arr[lapm__tynh] >= maxDistance).all():
            return maxDistance
        lapm__tynh, kds__lrh = kds__lrh, lapm__tynh
    return min(arr[hww__mjgf % 2, hyl__cpo], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    urn__zlg = ['s', 't']
    nhrt__yzeb = [s, t]
    ded__ovd = [True] * 2
    guwb__oijzq = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    mbo__pdki = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    urn__zlg = ['s', 't', 'maxDistance']
    nhrt__yzeb = [s, t, maxDistance]
    ded__ovd = [True] * 3
    guwb__oijzq = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    mbo__pdki = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def endswith_util(source, suffix):
    gxh__pbfr = verify_string_binary_arg(source, 'endswith', 'source')
    if gxh__pbfr != verify_string_binary_arg(suffix, 'endswith', 'suffix'):
        raise bodo.utils.typing.BodoError(
            'String and suffix must both be strings or both binary')
    urn__zlg = ['source', 'suffix']
    nhrt__yzeb = [source, suffix]
    ded__ovd = [True] * 2
    guwb__oijzq = 'res[i] = arg0.endswith(arg1)'
    mbo__pdki = bodo.boolean_array
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    urn__zlg = ['arr', 'places']
    nhrt__yzeb = [arr, places]
    ded__ovd = [True] * 2
    guwb__oijzq = 'prec = max(arg1, 0)\n'
    guwb__oijzq += "res[i] = format(arg0, f',.{prec}f')"
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def insert_util(arr, pos, length, inject):
    gxh__pbfr = verify_string_binary_arg(arr, 'INSERT', 'arr')
    verify_int_arg(pos, 'INSERT', 'pos')
    verify_int_arg(length, 'INSERT', 'length')
    if gxh__pbfr != verify_string_binary_arg(inject, 'INSERT', 'inject'):
        raise bodo.utils.typing.BodoError(
            'String and injected value must both be strings or both binary')
    urn__zlg = ['arr', 'pos', 'length', 'inject']
    nhrt__yzeb = [arr, pos, length, inject]
    ded__ovd = [True] * 4
    guwb__oijzq = 'prefixIndex = max(arg1-1, 0)\n'
    guwb__oijzq += 'suffixIndex = prefixIndex + max(arg2, 0)\n'
    guwb__oijzq += 'res[i] = arg0[:prefixIndex] + arg3 + arg0[suffixIndex:]'
    mbo__pdki = bodo.string_array_type if gxh__pbfr else bodo.binary_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        gxh__pbfr = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        onav__mdjvi = "''" if gxh__pbfr else "b''"
        urn__zlg = ['arr', 'n_chars']
        nhrt__yzeb = [arr, n_chars]
        ded__ovd = [True] * 2
        guwb__oijzq = 'if arg1 <= 0:\n'
        guwb__oijzq += f'   res[i] = {onav__mdjvi}\n'
        guwb__oijzq += 'else:\n'
        if func_name == 'LEFT':
            guwb__oijzq += '   res[i] = arg0[:arg1]\n'
        elif func_name == 'RIGHT':
            guwb__oijzq += '   res[i] = arg0[-arg1:]\n'
        mbo__pdki = (bodo.string_array_type if gxh__pbfr else bodo.
            binary_array_type)
        return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
            mbo__pdki, may_cause_duplicate_dict_array_values=True)
    return overload_left_right_util


def _install_left_right_overload():
    for krqmu__gkmtq, func_name in zip((left_util, right_util), ('LEFT',
        'RIGHT')):
        ejhr__vcqj = create_left_right_util_overload(func_name)
        overload(krqmu__gkmtq)(ejhr__vcqj)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        fxu__yzt = verify_string_binary_arg(pad_string, func_name, 'pad_string'
            )
        gxh__pbfr = verify_string_binary_arg(arr, func_name, 'arr')
        if gxh__pbfr != fxu__yzt:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        mbo__pdki = (bodo.string_array_type if gxh__pbfr else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            rsoy__qtpb = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            rsoy__qtpb = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        urn__zlg = ['arr', 'length', 'pad_string']
        nhrt__yzeb = [arr, length, pad_string]
        ded__ovd = [True] * 3
        onav__mdjvi = "''" if gxh__pbfr else "b''"
        guwb__oijzq = f"""                if arg1 <= 0:
                    res[i] = {onav__mdjvi}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {rsoy__qtpb}"""
        return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
            mbo__pdki, may_cause_duplicate_dict_array_values=True)
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for krqmu__gkmtq, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')
        ):
        ejhr__vcqj = create_lpad_rpad_util_overload(func_name)
        overload(krqmu__gkmtq)(ejhr__vcqj)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    urn__zlg = ['arr']
    nhrt__yzeb = [arr]
    ded__ovd = [True]
    guwb__oijzq = 'if len(arg0) == 0:\n'
    guwb__oijzq += '   bodo.libs.array_kernels.setna(res, i)\n'
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '   res[i] = ord(arg0[0])'
    mbo__pdki = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def position_util(substr, source, start):
    iwgbc__zlc = verify_string_binary_arg(substr, 'POSITION', 'substr')
    if iwgbc__zlc != verify_string_binary_arg(source, 'POSITION', 'source'):
        raise bodo.utils.typing.BodoError(
            'Substring and source must be both strings or both binary')
    verify_int_arg(start, 'POSITION', 'start')
    assert iwgbc__zlc, '[BE-3717] Support binary find with 3 args'
    urn__zlg = ['substr', 'source', 'start']
    nhrt__yzeb = [substr, source, start]
    ded__ovd = [True] * 3
    guwb__oijzq = 'res[i] = arg1.find(arg0, arg2 - 1) + 1'
    mbo__pdki = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    urn__zlg = ['arr', 'repeats']
    nhrt__yzeb = [arr, repeats]
    ded__ovd = [True] * 2
    guwb__oijzq = 'if arg1 <= 0:\n'
    guwb__oijzq += "   res[i] = ''\n"
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '   res[i] = arg0 * arg1'
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    urn__zlg = ['arr', 'to_replace', 'replace_with']
    nhrt__yzeb = [arr, to_replace, replace_with]
    ded__ovd = [True] * 3
    guwb__oijzq = "if arg1 == '':\n"
    guwb__oijzq += '   res[i] = arg0\n'
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '   res[i] = arg0.replace(arg1, arg2)'
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    gxh__pbfr = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    urn__zlg = ['arr']
    nhrt__yzeb = [arr]
    ded__ovd = [True]
    guwb__oijzq = 'res[i] = arg0[::-1]'
    mbo__pdki = bodo.string_array_type
    mbo__pdki = bodo.string_array_type if gxh__pbfr else bodo.binary_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def rtrimmed_length_util(arr):
    verify_string_arg(arr, 'RTRIMMED_LENGTH', 'arr')
    urn__zlg = ['arr']
    nhrt__yzeb = [arr]
    ded__ovd = [True]
    guwb__oijzq = "res[i] = len(arg0.rstrip(' '))"
    mbo__pdki = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    urn__zlg = ['n_chars']
    nhrt__yzeb = [n_chars]
    ded__ovd = [True]
    guwb__oijzq = 'if arg0 <= 0:\n'
    guwb__oijzq += "   res[i] = ''\n"
    guwb__oijzq += 'else:\n'
    guwb__oijzq += "   res[i] = ' ' * arg0"
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    urn__zlg = ['source', 'delim', 'part']
    nhrt__yzeb = [source, delim, part]
    ded__ovd = [True] * 3
    guwb__oijzq = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    guwb__oijzq += 'if abs(arg2) > len(tokens):\n'
    guwb__oijzq += "    res[i] = ''\n"
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def startswith_util(source, prefix):
    gxh__pbfr = verify_string_binary_arg(source, 'startswith', 'source')
    if gxh__pbfr != verify_string_binary_arg(prefix, 'startswith', 'prefix'):
        raise bodo.utils.typing.BodoError(
            'String and prefix must both be strings or both binary')
    urn__zlg = ['source', 'prefix']
    nhrt__yzeb = [source, prefix]
    ded__ovd = [True] * 2
    guwb__oijzq = 'res[i] = arg0.startswith(arg1)'
    mbo__pdki = bodo.boolean_array
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    urn__zlg = ['arr0', 'arr1']
    nhrt__yzeb = [arr0, arr1]
    ded__ovd = [True] * 2
    guwb__oijzq = 'if arg0 < arg1:\n'
    guwb__oijzq += '   res[i] = -1\n'
    guwb__oijzq += 'elif arg0 > arg1:\n'
    guwb__oijzq += '   res[i] = 1\n'
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '   res[i] = 0\n'
    mbo__pdki = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    urn__zlg = ['source', 'delim', 'part']
    nhrt__yzeb = [source, delim, part]
    ded__ovd = [True] * 3
    guwb__oijzq = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    guwb__oijzq += '   bodo.libs.array_kernels.setna(res, i)\n'
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '   tokens = []\n'
    guwb__oijzq += "   buffer = ''\n"
    guwb__oijzq += '   for j in range(len(arg0)):\n'
    guwb__oijzq += '      if arg0[j] in arg1:\n'
    guwb__oijzq += "         if buffer != '':"
    guwb__oijzq += '            tokens.append(buffer)\n'
    guwb__oijzq += "         buffer = ''\n"
    guwb__oijzq += '      else:\n'
    guwb__oijzq += '         buffer += arg0[j]\n'
    guwb__oijzq += "   if buffer != '':\n"
    guwb__oijzq += '      tokens.append(buffer)\n'
    guwb__oijzq += '   if arg2 > len(tokens):\n'
    guwb__oijzq += '      bodo.libs.array_kernels.setna(res, i)\n'
    guwb__oijzq += '   else:\n'
    guwb__oijzq += '      res[i] = tokens[arg2-1]\n'
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    gxh__pbfr = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    mbo__pdki = bodo.string_array_type if gxh__pbfr else bodo.binary_array_type
    urn__zlg = ['arr', 'start', 'length']
    nhrt__yzeb = [arr, start, length]
    ded__ovd = [True] * 3
    guwb__oijzq = 'if arg2 <= 0:\n'
    guwb__oijzq += "   res[i] = ''\n" if gxh__pbfr else "   res[i] = b''\n"
    guwb__oijzq += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    guwb__oijzq += '   res[i] = arg0[arg1:]\n'
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '   if arg1 > 0: arg1 -= 1\n'
    guwb__oijzq += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    urn__zlg = ['arr', 'delimiter', 'occurrences']
    nhrt__yzeb = [arr, delimiter, occurrences]
    ded__ovd = [True] * 3
    guwb__oijzq = "if arg1 == '' or arg2 == 0:\n"
    guwb__oijzq += "   res[i] = ''\n"
    guwb__oijzq += 'elif arg2 >= 0:\n'
    guwb__oijzq += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    guwb__oijzq += 'else:\n'
    guwb__oijzq += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    urn__zlg = ['arr', 'source', 'target']
    nhrt__yzeb = [arr, source, target]
    ded__ovd = [True] * 3
    guwb__oijzq = "translated = ''\n"
    guwb__oijzq += 'for char in arg0:\n'
    guwb__oijzq += '   index = arg1.find(char)\n'
    guwb__oijzq += '   if index == -1:\n'
    guwb__oijzq += '      translated += char\n'
    guwb__oijzq += '   elif index < len(arg2):\n'
    guwb__oijzq += '      translated += arg2[index]\n'
    guwb__oijzq += 'res[i] = translated'
    mbo__pdki = bodo.string_array_type
    return gen_vectorized(urn__zlg, nhrt__yzeb, ded__ovd, guwb__oijzq,
        mbo__pdki, may_cause_duplicate_dict_array_values=True)
