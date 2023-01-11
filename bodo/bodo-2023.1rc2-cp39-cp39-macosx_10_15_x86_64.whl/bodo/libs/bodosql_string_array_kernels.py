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
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.contains',
                ['arr', 'contains'], nmja__slhfy)

    def impl(arr, pattern):
        return contains_util(arr, pattern)
    return impl


@numba.generated_jit(nopython=True)
def contains_util(arr, pattern):
    verify_string_binary_arg(arr, 'CONTAINS', 'arr')
    verify_string_binary_arg(pattern, 'CONTAINS', 'pattern')
    ltk__ebkq = bodo.boolean_array
    zwzoy__gtdm = ['arr', 'pattern']
    scrrw__nsp = [arr, pattern]
    gccv__wsrjv = [True] * 2
    reybt__hseim = 'res[i] = arg1 in arg0\n'
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def editdistance_no_max(s, t):
    args = [s, t]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], nmja__slhfy)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], nmja__slhfy)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def endswith(source, suffix):
    args = [source, suffix]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.endswith',
                ['source', 'suffix'], nmja__slhfy)

    def impl(source, suffix):
        return endswith_util(source, suffix)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], nmja__slhfy)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], nmja__slhfy)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def insert(source, pos, length, inject):
    args = [source, pos, length, inject]
    for nmja__slhfy in range(4):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.insert',
                ['source', 'pos', 'length', 'inject'], nmja__slhfy)

    def impl(source, pos, length, inject):
        return insert_util(source, pos, length, inject)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], nmja__slhfy)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], nmja__slhfy)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], nmja__slhfy)

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
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.position',
                ['substr', 'source', 'start'], nmja__slhfy)

    def impl(substr, source, start):
        return position_util(substr, source, start)
    return impl


@numba.generated_jit(nopython=True)
def repeat(arr, repeats):
    args = [arr, repeats]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], nmja__slhfy)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], nmja__slhfy)

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
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], nmja__slhfy)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], nmja__slhfy)

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
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], nmja__slhfy)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def startswith(source, prefix):
    args = [source, prefix]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.startswith',
                ['source', 'prefix'], nmja__slhfy)

    def impl(source, prefix):
        return startswith_util(source, prefix)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for nmja__slhfy in range(2):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], nmja__slhfy)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], nmja__slhfy)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], nmja__slhfy)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], nmja__slhfy)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for nmja__slhfy in range(3):
        if isinstance(args[nmja__slhfy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], nmja__slhfy)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    zwzoy__gtdm = ['arr']
    scrrw__nsp = [arr]
    gccv__wsrjv = [True]
    reybt__hseim = 'if 0 <= arg0 <= 127:\n'
    reybt__hseim += '   res[i] = chr(arg0)\n'
    reybt__hseim += 'else:\n'
    reybt__hseim += '   bodo.libs.array_kernels.setna(res, i)\n'
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    zwzoy__gtdm = ['arr', 'delim']
    scrrw__nsp = [arr, delim]
    gccv__wsrjv = [True] * 2
    reybt__hseim = 'capitalized = arg0[:1].upper()\n'
    reybt__hseim += 'for j in range(1, len(arg0)):\n'
    reybt__hseim += '   if arg0[j-1] in arg1:\n'
    reybt__hseim += '      capitalized += arg0[j].upper()\n'
    reybt__hseim += '   else:\n'
    reybt__hseim += '      capitalized += arg0[j].lower()\n'
    reybt__hseim += 'res[i] = capitalized'
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    zwzoy__gtdm = ['arr', 'target']
    scrrw__nsp = [arr, target]
    gccv__wsrjv = [True] * 2
    reybt__hseim = 'res[i] = arg0.find(arg1) + 1'
    ltk__ebkq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    tjoes__ocotr, clfy__tdlbr = len(s), len(t)
    ndpme__lomjc, bvw__bcck = 1, 0
    arr = np.zeros((2, tjoes__ocotr + 1), dtype=np.uint32)
    arr[0, :] = np.arange(tjoes__ocotr + 1)
    for nmja__slhfy in range(1, clfy__tdlbr + 1):
        arr[ndpme__lomjc, 0] = nmja__slhfy
        for mwbgb__wixk in range(1, tjoes__ocotr + 1):
            if s[mwbgb__wixk - 1] == t[nmja__slhfy - 1]:
                arr[ndpme__lomjc, mwbgb__wixk] = arr[bvw__bcck, mwbgb__wixk - 1
                    ]
            else:
                arr[ndpme__lomjc, mwbgb__wixk] = 1 + min(arr[ndpme__lomjc, 
                    mwbgb__wixk - 1], arr[bvw__bcck, mwbgb__wixk], arr[
                    bvw__bcck, mwbgb__wixk - 1])
        ndpme__lomjc, bvw__bcck = bvw__bcck, ndpme__lomjc
    return arr[clfy__tdlbr % 2, tjoes__ocotr]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    tjoes__ocotr, clfy__tdlbr = len(s), len(t)
    if tjoes__ocotr <= maxDistance and clfy__tdlbr <= maxDistance:
        return min_edit_distance(s, t)
    ndpme__lomjc, bvw__bcck = 1, 0
    arr = np.zeros((2, tjoes__ocotr + 1), dtype=np.uint32)
    arr[0, :] = np.arange(tjoes__ocotr + 1)
    for nmja__slhfy in range(1, clfy__tdlbr + 1):
        arr[ndpme__lomjc, 0] = nmja__slhfy
        for mwbgb__wixk in range(1, tjoes__ocotr + 1):
            if s[mwbgb__wixk - 1] == t[nmja__slhfy - 1]:
                arr[ndpme__lomjc, mwbgb__wixk] = arr[bvw__bcck, mwbgb__wixk - 1
                    ]
            else:
                arr[ndpme__lomjc, mwbgb__wixk] = 1 + min(arr[ndpme__lomjc, 
                    mwbgb__wixk - 1], arr[bvw__bcck, mwbgb__wixk], arr[
                    bvw__bcck, mwbgb__wixk - 1])
        if (arr[ndpme__lomjc] >= maxDistance).all():
            return maxDistance
        ndpme__lomjc, bvw__bcck = bvw__bcck, ndpme__lomjc
    return min(arr[clfy__tdlbr % 2, tjoes__ocotr], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    zwzoy__gtdm = ['s', 't']
    scrrw__nsp = [s, t]
    gccv__wsrjv = [True] * 2
    reybt__hseim = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    ltk__ebkq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    zwzoy__gtdm = ['s', 't', 'maxDistance']
    scrrw__nsp = [s, t, maxDistance]
    gccv__wsrjv = [True] * 3
    reybt__hseim = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    ltk__ebkq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def endswith_util(source, suffix):
    bwkd__idp = verify_string_binary_arg(source, 'endswith', 'source')
    if bwkd__idp != verify_string_binary_arg(suffix, 'endswith', 'suffix'):
        raise bodo.utils.typing.BodoError(
            'String and suffix must both be strings or both binary')
    zwzoy__gtdm = ['source', 'suffix']
    scrrw__nsp = [source, suffix]
    gccv__wsrjv = [True] * 2
    reybt__hseim = 'res[i] = arg0.endswith(arg1)'
    ltk__ebkq = bodo.boolean_array
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    zwzoy__gtdm = ['arr', 'places']
    scrrw__nsp = [arr, places]
    gccv__wsrjv = [True] * 2
    reybt__hseim = 'prec = max(arg1, 0)\n'
    reybt__hseim += "res[i] = format(arg0, f',.{prec}f')"
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def insert_util(arr, pos, length, inject):
    bwkd__idp = verify_string_binary_arg(arr, 'INSERT', 'arr')
    verify_int_arg(pos, 'INSERT', 'pos')
    verify_int_arg(length, 'INSERT', 'length')
    if bwkd__idp != verify_string_binary_arg(inject, 'INSERT', 'inject'):
        raise bodo.utils.typing.BodoError(
            'String and injected value must both be strings or both binary')
    zwzoy__gtdm = ['arr', 'pos', 'length', 'inject']
    scrrw__nsp = [arr, pos, length, inject]
    gccv__wsrjv = [True] * 4
    reybt__hseim = 'prefixIndex = max(arg1-1, 0)\n'
    reybt__hseim += 'suffixIndex = prefixIndex + max(arg2, 0)\n'
    reybt__hseim += 'res[i] = arg0[:prefixIndex] + arg3 + arg0[suffixIndex:]'
    ltk__ebkq = bodo.string_array_type if bwkd__idp else bodo.binary_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        bwkd__idp = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        gnu__nhxv = "''" if bwkd__idp else "b''"
        zwzoy__gtdm = ['arr', 'n_chars']
        scrrw__nsp = [arr, n_chars]
        gccv__wsrjv = [True] * 2
        reybt__hseim = 'if arg1 <= 0:\n'
        reybt__hseim += f'   res[i] = {gnu__nhxv}\n'
        reybt__hseim += 'else:\n'
        if func_name == 'LEFT':
            reybt__hseim += '   res[i] = arg0[:arg1]\n'
        elif func_name == 'RIGHT':
            reybt__hseim += '   res[i] = arg0[-arg1:]\n'
        ltk__ebkq = (bodo.string_array_type if bwkd__idp else bodo.
            binary_array_type)
        return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
            reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True
            )
    return overload_left_right_util


def _install_left_right_overload():
    for mtjn__zgpbw, func_name in zip((left_util, right_util), ('LEFT',
        'RIGHT')):
        djah__nwtr = create_left_right_util_overload(func_name)
        overload(mtjn__zgpbw)(djah__nwtr)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        xxo__daads = verify_string_binary_arg(pad_string, func_name,
            'pad_string')
        bwkd__idp = verify_string_binary_arg(arr, func_name, 'arr')
        if bwkd__idp != xxo__daads:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        ltk__ebkq = (bodo.string_array_type if bwkd__idp else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            dskp__crf = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            dskp__crf = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        zwzoy__gtdm = ['arr', 'length', 'pad_string']
        scrrw__nsp = [arr, length, pad_string]
        gccv__wsrjv = [True] * 3
        gnu__nhxv = "''" if bwkd__idp else "b''"
        reybt__hseim = f"""                if arg1 <= 0:
                    res[i] = {gnu__nhxv}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {dskp__crf}"""
        return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
            reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True
            )
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for mtjn__zgpbw, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')
        ):
        djah__nwtr = create_lpad_rpad_util_overload(func_name)
        overload(mtjn__zgpbw)(djah__nwtr)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    zwzoy__gtdm = ['arr']
    scrrw__nsp = [arr]
    gccv__wsrjv = [True]
    reybt__hseim = 'if len(arg0) == 0:\n'
    reybt__hseim += '   bodo.libs.array_kernels.setna(res, i)\n'
    reybt__hseim += 'else:\n'
    reybt__hseim += '   res[i] = ord(arg0[0])'
    ltk__ebkq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def position_util(substr, source, start):
    vimcp__gkof = verify_string_binary_arg(substr, 'POSITION', 'substr')
    if vimcp__gkof != verify_string_binary_arg(source, 'POSITION', 'source'):
        raise bodo.utils.typing.BodoError(
            'Substring and source must be both strings or both binary')
    verify_int_arg(start, 'POSITION', 'start')
    assert vimcp__gkof, '[BE-3717] Support binary find with 3 args'
    zwzoy__gtdm = ['substr', 'source', 'start']
    scrrw__nsp = [substr, source, start]
    gccv__wsrjv = [True] * 3
    reybt__hseim = 'res[i] = arg1.find(arg0, arg2 - 1) + 1'
    ltk__ebkq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    zwzoy__gtdm = ['arr', 'repeats']
    scrrw__nsp = [arr, repeats]
    gccv__wsrjv = [True] * 2
    reybt__hseim = 'if arg1 <= 0:\n'
    reybt__hseim += "   res[i] = ''\n"
    reybt__hseim += 'else:\n'
    reybt__hseim += '   res[i] = arg0 * arg1'
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    zwzoy__gtdm = ['arr', 'to_replace', 'replace_with']
    scrrw__nsp = [arr, to_replace, replace_with]
    gccv__wsrjv = [True] * 3
    reybt__hseim = "if arg1 == '':\n"
    reybt__hseim += '   res[i] = arg0\n'
    reybt__hseim += 'else:\n'
    reybt__hseim += '   res[i] = arg0.replace(arg1, arg2)'
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    bwkd__idp = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    zwzoy__gtdm = ['arr']
    scrrw__nsp = [arr]
    gccv__wsrjv = [True]
    reybt__hseim = 'res[i] = arg0[::-1]'
    ltk__ebkq = bodo.string_array_type
    ltk__ebkq = bodo.string_array_type if bwkd__idp else bodo.binary_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def rtrimmed_length_util(arr):
    verify_string_arg(arr, 'RTRIMMED_LENGTH', 'arr')
    zwzoy__gtdm = ['arr']
    scrrw__nsp = [arr]
    gccv__wsrjv = [True]
    reybt__hseim = "res[i] = len(arg0.rstrip(' '))"
    ltk__ebkq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    zwzoy__gtdm = ['n_chars']
    scrrw__nsp = [n_chars]
    gccv__wsrjv = [True]
    reybt__hseim = 'if arg0 <= 0:\n'
    reybt__hseim += "   res[i] = ''\n"
    reybt__hseim += 'else:\n'
    reybt__hseim += "   res[i] = ' ' * arg0"
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    zwzoy__gtdm = ['source', 'delim', 'part']
    scrrw__nsp = [source, delim, part]
    gccv__wsrjv = [True] * 3
    reybt__hseim = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    reybt__hseim += 'if abs(arg2) > len(tokens):\n'
    reybt__hseim += "    res[i] = ''\n"
    reybt__hseim += 'else:\n'
    reybt__hseim += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def startswith_util(source, prefix):
    bwkd__idp = verify_string_binary_arg(source, 'startswith', 'source')
    if bwkd__idp != verify_string_binary_arg(prefix, 'startswith', 'prefix'):
        raise bodo.utils.typing.BodoError(
            'String and prefix must both be strings or both binary')
    zwzoy__gtdm = ['source', 'prefix']
    scrrw__nsp = [source, prefix]
    gccv__wsrjv = [True] * 2
    reybt__hseim = 'res[i] = arg0.startswith(arg1)'
    ltk__ebkq = bodo.boolean_array
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    zwzoy__gtdm = ['arr0', 'arr1']
    scrrw__nsp = [arr0, arr1]
    gccv__wsrjv = [True] * 2
    reybt__hseim = 'if arg0 < arg1:\n'
    reybt__hseim += '   res[i] = -1\n'
    reybt__hseim += 'elif arg0 > arg1:\n'
    reybt__hseim += '   res[i] = 1\n'
    reybt__hseim += 'else:\n'
    reybt__hseim += '   res[i] = 0\n'
    ltk__ebkq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    zwzoy__gtdm = ['source', 'delim', 'part']
    scrrw__nsp = [source, delim, part]
    gccv__wsrjv = [True] * 3
    reybt__hseim = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    reybt__hseim += '   bodo.libs.array_kernels.setna(res, i)\n'
    reybt__hseim += 'else:\n'
    reybt__hseim += '   tokens = []\n'
    reybt__hseim += "   buffer = ''\n"
    reybt__hseim += '   for j in range(len(arg0)):\n'
    reybt__hseim += '      if arg0[j] in arg1:\n'
    reybt__hseim += "         if buffer != '':"
    reybt__hseim += '            tokens.append(buffer)\n'
    reybt__hseim += "         buffer = ''\n"
    reybt__hseim += '      else:\n'
    reybt__hseim += '         buffer += arg0[j]\n'
    reybt__hseim += "   if buffer != '':\n"
    reybt__hseim += '      tokens.append(buffer)\n'
    reybt__hseim += '   if arg2 > len(tokens):\n'
    reybt__hseim += '      bodo.libs.array_kernels.setna(res, i)\n'
    reybt__hseim += '   else:\n'
    reybt__hseim += '      res[i] = tokens[arg2-1]\n'
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    bwkd__idp = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    ltk__ebkq = bodo.string_array_type if bwkd__idp else bodo.binary_array_type
    zwzoy__gtdm = ['arr', 'start', 'length']
    scrrw__nsp = [arr, start, length]
    gccv__wsrjv = [True] * 3
    reybt__hseim = 'if arg2 <= 0:\n'
    reybt__hseim += "   res[i] = ''\n" if bwkd__idp else "   res[i] = b''\n"
    reybt__hseim += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    reybt__hseim += '   res[i] = arg0[arg1:]\n'
    reybt__hseim += 'else:\n'
    reybt__hseim += '   if arg1 > 0: arg1 -= 1\n'
    reybt__hseim += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    zwzoy__gtdm = ['arr', 'delimiter', 'occurrences']
    scrrw__nsp = [arr, delimiter, occurrences]
    gccv__wsrjv = [True] * 3
    reybt__hseim = "if arg1 == '' or arg2 == 0:\n"
    reybt__hseim += "   res[i] = ''\n"
    reybt__hseim += 'elif arg2 >= 0:\n'
    reybt__hseim += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    reybt__hseim += 'else:\n'
    reybt__hseim += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    zwzoy__gtdm = ['arr', 'source', 'target']
    scrrw__nsp = [arr, source, target]
    gccv__wsrjv = [True] * 3
    reybt__hseim = "translated = ''\n"
    reybt__hseim += 'for char in arg0:\n'
    reybt__hseim += '   index = arg1.find(char)\n'
    reybt__hseim += '   if index == -1:\n'
    reybt__hseim += '      translated += char\n'
    reybt__hseim += '   elif index < len(arg2):\n'
    reybt__hseim += '      translated += arg2[index]\n'
    reybt__hseim += 'res[i] = translated'
    ltk__ebkq = bodo.string_array_type
    return gen_vectorized(zwzoy__gtdm, scrrw__nsp, gccv__wsrjv,
        reybt__hseim, ltk__ebkq, may_cause_duplicate_dict_array_values=True)
