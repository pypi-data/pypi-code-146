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
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.contains',
                ['arr', 'contains'], tsxx__lxagw)

    def impl(arr, pattern):
        return contains_util(arr, pattern)
    return impl


@numba.generated_jit(nopython=True)
def contains_util(arr, pattern):
    verify_string_binary_arg(arr, 'CONTAINS', 'arr')
    verify_string_binary_arg(pattern, 'CONTAINS', 'pattern')
    ckqnb__onu = bodo.boolean_array
    rojv__mxeqd = ['arr', 'pattern']
    duji__kfbxn = [arr, pattern]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = 'res[i] = arg1 in arg0\n'
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def editdistance_no_max(s, t):
    args = [s, t]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], tsxx__lxagw)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], tsxx__lxagw)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def endswith(source, suffix):
    args = [source, suffix]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.endswith',
                ['source', 'suffix'], tsxx__lxagw)

    def impl(source, suffix):
        return endswith_util(source, suffix)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], tsxx__lxagw)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], tsxx__lxagw)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def insert(source, pos, length, inject):
    args = [source, pos, length, inject]
    for tsxx__lxagw in range(4):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.insert',
                ['source', 'pos', 'length', 'inject'], tsxx__lxagw)

    def impl(source, pos, length, inject):
        return insert_util(source, pos, length, inject)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], tsxx__lxagw)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], tsxx__lxagw)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], tsxx__lxagw)

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
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.position',
                ['substr', 'source', 'start'], tsxx__lxagw)

    def impl(substr, source, start):
        return position_util(substr, source, start)
    return impl


@numba.generated_jit(nopython=True)
def repeat(arr, repeats):
    args = [arr, repeats]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], tsxx__lxagw)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], tsxx__lxagw)

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
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], tsxx__lxagw)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], tsxx__lxagw)

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
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], tsxx__lxagw)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def startswith(source, prefix):
    args = [source, prefix]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.startswith',
                ['source', 'prefix'], tsxx__lxagw)

    def impl(source, prefix):
        return startswith_util(source, prefix)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for tsxx__lxagw in range(2):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], tsxx__lxagw)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], tsxx__lxagw)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], tsxx__lxagw)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], tsxx__lxagw)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for tsxx__lxagw in range(3):
        if isinstance(args[tsxx__lxagw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], tsxx__lxagw)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    rojv__mxeqd = ['arr']
    duji__kfbxn = [arr]
    ysohi__xzui = [True]
    crtwc__hcksc = 'if 0 <= arg0 <= 127:\n'
    crtwc__hcksc += '   res[i] = chr(arg0)\n'
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '   bodo.libs.array_kernels.setna(res, i)\n'
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    rojv__mxeqd = ['arr', 'delim']
    duji__kfbxn = [arr, delim]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = 'capitalized = arg0[:1].upper()\n'
    crtwc__hcksc += 'for j in range(1, len(arg0)):\n'
    crtwc__hcksc += '   if arg0[j-1] in arg1:\n'
    crtwc__hcksc += '      capitalized += arg0[j].upper()\n'
    crtwc__hcksc += '   else:\n'
    crtwc__hcksc += '      capitalized += arg0[j].lower()\n'
    crtwc__hcksc += 'res[i] = capitalized'
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    rojv__mxeqd = ['arr', 'target']
    duji__kfbxn = [arr, target]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = 'res[i] = arg0.find(arg1) + 1'
    ckqnb__onu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    shd__cupwb, papg__khf = len(s), len(t)
    nnn__jqq, qyhn__ubmkn = 1, 0
    arr = np.zeros((2, shd__cupwb + 1), dtype=np.uint32)
    arr[0, :] = np.arange(shd__cupwb + 1)
    for tsxx__lxagw in range(1, papg__khf + 1):
        arr[nnn__jqq, 0] = tsxx__lxagw
        for gdgxa__yecfi in range(1, shd__cupwb + 1):
            if s[gdgxa__yecfi - 1] == t[tsxx__lxagw - 1]:
                arr[nnn__jqq, gdgxa__yecfi] = arr[qyhn__ubmkn, gdgxa__yecfi - 1
                    ]
            else:
                arr[nnn__jqq, gdgxa__yecfi] = 1 + min(arr[nnn__jqq, 
                    gdgxa__yecfi - 1], arr[qyhn__ubmkn, gdgxa__yecfi], arr[
                    qyhn__ubmkn, gdgxa__yecfi - 1])
        nnn__jqq, qyhn__ubmkn = qyhn__ubmkn, nnn__jqq
    return arr[papg__khf % 2, shd__cupwb]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    shd__cupwb, papg__khf = len(s), len(t)
    if shd__cupwb <= maxDistance and papg__khf <= maxDistance:
        return min_edit_distance(s, t)
    nnn__jqq, qyhn__ubmkn = 1, 0
    arr = np.zeros((2, shd__cupwb + 1), dtype=np.uint32)
    arr[0, :] = np.arange(shd__cupwb + 1)
    for tsxx__lxagw in range(1, papg__khf + 1):
        arr[nnn__jqq, 0] = tsxx__lxagw
        for gdgxa__yecfi in range(1, shd__cupwb + 1):
            if s[gdgxa__yecfi - 1] == t[tsxx__lxagw - 1]:
                arr[nnn__jqq, gdgxa__yecfi] = arr[qyhn__ubmkn, gdgxa__yecfi - 1
                    ]
            else:
                arr[nnn__jqq, gdgxa__yecfi] = 1 + min(arr[nnn__jqq, 
                    gdgxa__yecfi - 1], arr[qyhn__ubmkn, gdgxa__yecfi], arr[
                    qyhn__ubmkn, gdgxa__yecfi - 1])
        if (arr[nnn__jqq] >= maxDistance).all():
            return maxDistance
        nnn__jqq, qyhn__ubmkn = qyhn__ubmkn, nnn__jqq
    return min(arr[papg__khf % 2, shd__cupwb], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    rojv__mxeqd = ['s', 't']
    duji__kfbxn = [s, t]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    ckqnb__onu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    rojv__mxeqd = ['s', 't', 'maxDistance']
    duji__kfbxn = [s, t, maxDistance]
    ysohi__xzui = [True] * 3
    crtwc__hcksc = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    ckqnb__onu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def endswith_util(source, suffix):
    bqg__spo = verify_string_binary_arg(source, 'endswith', 'source')
    if bqg__spo != verify_string_binary_arg(suffix, 'endswith', 'suffix'):
        raise bodo.utils.typing.BodoError(
            'String and suffix must both be strings or both binary')
    rojv__mxeqd = ['source', 'suffix']
    duji__kfbxn = [source, suffix]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = 'res[i] = arg0.endswith(arg1)'
    ckqnb__onu = bodo.boolean_array
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    rojv__mxeqd = ['arr', 'places']
    duji__kfbxn = [arr, places]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = 'prec = max(arg1, 0)\n'
    crtwc__hcksc += "res[i] = format(arg0, f',.{prec}f')"
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def insert_util(arr, pos, length, inject):
    bqg__spo = verify_string_binary_arg(arr, 'INSERT', 'arr')
    verify_int_arg(pos, 'INSERT', 'pos')
    verify_int_arg(length, 'INSERT', 'length')
    if bqg__spo != verify_string_binary_arg(inject, 'INSERT', 'inject'):
        raise bodo.utils.typing.BodoError(
            'String and injected value must both be strings or both binary')
    rojv__mxeqd = ['arr', 'pos', 'length', 'inject']
    duji__kfbxn = [arr, pos, length, inject]
    ysohi__xzui = [True] * 4
    crtwc__hcksc = 'prefixIndex = max(arg1-1, 0)\n'
    crtwc__hcksc += 'suffixIndex = prefixIndex + max(arg2, 0)\n'
    crtwc__hcksc += 'res[i] = arg0[:prefixIndex] + arg3 + arg0[suffixIndex:]'
    ckqnb__onu = bodo.string_array_type if bqg__spo else bodo.binary_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        bqg__spo = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        tqjs__vsvba = "''" if bqg__spo else "b''"
        rojv__mxeqd = ['arr', 'n_chars']
        duji__kfbxn = [arr, n_chars]
        ysohi__xzui = [True] * 2
        crtwc__hcksc = 'if arg1 <= 0:\n'
        crtwc__hcksc += f'   res[i] = {tqjs__vsvba}\n'
        crtwc__hcksc += 'else:\n'
        if func_name == 'LEFT':
            crtwc__hcksc += '   res[i] = arg0[:arg1]\n'
        elif func_name == 'RIGHT':
            crtwc__hcksc += '   res[i] = arg0[-arg1:]\n'
        ckqnb__onu = (bodo.string_array_type if bqg__spo else bodo.
            binary_array_type)
        return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
            crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values
            =True)
    return overload_left_right_util


def _install_left_right_overload():
    for ekh__ghy, func_name in zip((left_util, right_util), ('LEFT', 'RIGHT')):
        otp__uoih = create_left_right_util_overload(func_name)
        overload(ekh__ghy)(otp__uoih)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        btlvi__nsrud = verify_string_binary_arg(pad_string, func_name,
            'pad_string')
        bqg__spo = verify_string_binary_arg(arr, func_name, 'arr')
        if bqg__spo != btlvi__nsrud:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        ckqnb__onu = (bodo.string_array_type if bqg__spo else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            nkc__ztmsp = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            nkc__ztmsp = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        rojv__mxeqd = ['arr', 'length', 'pad_string']
        duji__kfbxn = [arr, length, pad_string]
        ysohi__xzui = [True] * 3
        tqjs__vsvba = "''" if bqg__spo else "b''"
        crtwc__hcksc = f"""                if arg1 <= 0:
                    res[i] = {tqjs__vsvba}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {nkc__ztmsp}"""
        return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
            crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values
            =True)
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for ekh__ghy, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')):
        otp__uoih = create_lpad_rpad_util_overload(func_name)
        overload(ekh__ghy)(otp__uoih)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    rojv__mxeqd = ['arr']
    duji__kfbxn = [arr]
    ysohi__xzui = [True]
    crtwc__hcksc = 'if len(arg0) == 0:\n'
    crtwc__hcksc += '   bodo.libs.array_kernels.setna(res, i)\n'
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '   res[i] = ord(arg0[0])'
    ckqnb__onu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def position_util(substr, source, start):
    zjt__vujy = verify_string_binary_arg(substr, 'POSITION', 'substr')
    if zjt__vujy != verify_string_binary_arg(source, 'POSITION', 'source'):
        raise bodo.utils.typing.BodoError(
            'Substring and source must be both strings or both binary')
    verify_int_arg(start, 'POSITION', 'start')
    assert zjt__vujy, '[BE-3717] Support binary find with 3 args'
    rojv__mxeqd = ['substr', 'source', 'start']
    duji__kfbxn = [substr, source, start]
    ysohi__xzui = [True] * 3
    crtwc__hcksc = 'res[i] = arg1.find(arg0, arg2 - 1) + 1'
    ckqnb__onu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    rojv__mxeqd = ['arr', 'repeats']
    duji__kfbxn = [arr, repeats]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = 'if arg1 <= 0:\n'
    crtwc__hcksc += "   res[i] = ''\n"
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '   res[i] = arg0 * arg1'
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    rojv__mxeqd = ['arr', 'to_replace', 'replace_with']
    duji__kfbxn = [arr, to_replace, replace_with]
    ysohi__xzui = [True] * 3
    crtwc__hcksc = "if arg1 == '':\n"
    crtwc__hcksc += '   res[i] = arg0\n'
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '   res[i] = arg0.replace(arg1, arg2)'
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    bqg__spo = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    rojv__mxeqd = ['arr']
    duji__kfbxn = [arr]
    ysohi__xzui = [True]
    crtwc__hcksc = 'res[i] = arg0[::-1]'
    ckqnb__onu = bodo.string_array_type
    ckqnb__onu = bodo.string_array_type if bqg__spo else bodo.binary_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def rtrimmed_length_util(arr):
    verify_string_arg(arr, 'RTRIMMED_LENGTH', 'arr')
    rojv__mxeqd = ['arr']
    duji__kfbxn = [arr]
    ysohi__xzui = [True]
    crtwc__hcksc = "res[i] = len(arg0.rstrip(' '))"
    ckqnb__onu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    rojv__mxeqd = ['n_chars']
    duji__kfbxn = [n_chars]
    ysohi__xzui = [True]
    crtwc__hcksc = 'if arg0 <= 0:\n'
    crtwc__hcksc += "   res[i] = ''\n"
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += "   res[i] = ' ' * arg0"
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    rojv__mxeqd = ['source', 'delim', 'part']
    duji__kfbxn = [source, delim, part]
    ysohi__xzui = [True] * 3
    crtwc__hcksc = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    crtwc__hcksc += 'if abs(arg2) > len(tokens):\n'
    crtwc__hcksc += "    res[i] = ''\n"
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def startswith_util(source, prefix):
    bqg__spo = verify_string_binary_arg(source, 'startswith', 'source')
    if bqg__spo != verify_string_binary_arg(prefix, 'startswith', 'prefix'):
        raise bodo.utils.typing.BodoError(
            'String and prefix must both be strings or both binary')
    rojv__mxeqd = ['source', 'prefix']
    duji__kfbxn = [source, prefix]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = 'res[i] = arg0.startswith(arg1)'
    ckqnb__onu = bodo.boolean_array
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    rojv__mxeqd = ['arr0', 'arr1']
    duji__kfbxn = [arr0, arr1]
    ysohi__xzui = [True] * 2
    crtwc__hcksc = 'if arg0 < arg1:\n'
    crtwc__hcksc += '   res[i] = -1\n'
    crtwc__hcksc += 'elif arg0 > arg1:\n'
    crtwc__hcksc += '   res[i] = 1\n'
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '   res[i] = 0\n'
    ckqnb__onu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    rojv__mxeqd = ['source', 'delim', 'part']
    duji__kfbxn = [source, delim, part]
    ysohi__xzui = [True] * 3
    crtwc__hcksc = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    crtwc__hcksc += '   bodo.libs.array_kernels.setna(res, i)\n'
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '   tokens = []\n'
    crtwc__hcksc += "   buffer = ''\n"
    crtwc__hcksc += '   for j in range(len(arg0)):\n'
    crtwc__hcksc += '      if arg0[j] in arg1:\n'
    crtwc__hcksc += "         if buffer != '':"
    crtwc__hcksc += '            tokens.append(buffer)\n'
    crtwc__hcksc += "         buffer = ''\n"
    crtwc__hcksc += '      else:\n'
    crtwc__hcksc += '         buffer += arg0[j]\n'
    crtwc__hcksc += "   if buffer != '':\n"
    crtwc__hcksc += '      tokens.append(buffer)\n'
    crtwc__hcksc += '   if arg2 > len(tokens):\n'
    crtwc__hcksc += '      bodo.libs.array_kernels.setna(res, i)\n'
    crtwc__hcksc += '   else:\n'
    crtwc__hcksc += '      res[i] = tokens[arg2-1]\n'
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    bqg__spo = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    ckqnb__onu = bodo.string_array_type if bqg__spo else bodo.binary_array_type
    rojv__mxeqd = ['arr', 'start', 'length']
    duji__kfbxn = [arr, start, length]
    ysohi__xzui = [True] * 3
    crtwc__hcksc = 'if arg2 <= 0:\n'
    crtwc__hcksc += "   res[i] = ''\n" if bqg__spo else "   res[i] = b''\n"
    crtwc__hcksc += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    crtwc__hcksc += '   res[i] = arg0[arg1:]\n'
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '   if arg1 > 0: arg1 -= 1\n'
    crtwc__hcksc += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    rojv__mxeqd = ['arr', 'delimiter', 'occurrences']
    duji__kfbxn = [arr, delimiter, occurrences]
    ysohi__xzui = [True] * 3
    crtwc__hcksc = "if arg1 == '' or arg2 == 0:\n"
    crtwc__hcksc += "   res[i] = ''\n"
    crtwc__hcksc += 'elif arg2 >= 0:\n'
    crtwc__hcksc += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    crtwc__hcksc += 'else:\n'
    crtwc__hcksc += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    rojv__mxeqd = ['arr', 'source', 'target']
    duji__kfbxn = [arr, source, target]
    ysohi__xzui = [True] * 3
    crtwc__hcksc = "translated = ''\n"
    crtwc__hcksc += 'for char in arg0:\n'
    crtwc__hcksc += '   index = arg1.find(char)\n'
    crtwc__hcksc += '   if index == -1:\n'
    crtwc__hcksc += '      translated += char\n'
    crtwc__hcksc += '   elif index < len(arg2):\n'
    crtwc__hcksc += '      translated += arg2[index]\n'
    crtwc__hcksc += 'res[i] = translated'
    ckqnb__onu = bodo.string_array_type
    return gen_vectorized(rojv__mxeqd, duji__kfbxn, ysohi__xzui,
        crtwc__hcksc, ckqnb__onu, may_cause_duplicate_dict_array_values=True)
