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
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.contains',
                ['arr', 'contains'], bvnhz__vckki)

    def impl(arr, pattern):
        return contains_util(arr, pattern)
    return impl


@numba.generated_jit(nopython=True)
def contains_util(arr, pattern):
    verify_string_binary_arg(arr, 'CONTAINS', 'arr')
    verify_string_binary_arg(pattern, 'CONTAINS', 'pattern')
    rby__akq = bodo.boolean_array
    auloe__jor = ['arr', 'pattern']
    tgmr__ynnoy = [arr, pattern]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = 'res[i] = arg1 in arg0\n'
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def editdistance_no_max(s, t):
    args = [s, t]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], bvnhz__vckki)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], bvnhz__vckki)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def endswith(source, suffix):
    args = [source, suffix]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.endswith',
                ['source', 'suffix'], bvnhz__vckki)

    def impl(source, suffix):
        return endswith_util(source, suffix)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], bvnhz__vckki)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], bvnhz__vckki)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def insert(source, pos, length, inject):
    args = [source, pos, length, inject]
    for bvnhz__vckki in range(4):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.insert',
                ['source', 'pos', 'length', 'inject'], bvnhz__vckki)

    def impl(source, pos, length, inject):
        return insert_util(source, pos, length, inject)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], bvnhz__vckki)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], bvnhz__vckki)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], bvnhz__vckki)

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
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.position',
                ['substr', 'source', 'start'], bvnhz__vckki)

    def impl(substr, source, start):
        return position_util(substr, source, start)
    return impl


@numba.generated_jit(nopython=True)
def repeat(arr, repeats):
    args = [arr, repeats]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], bvnhz__vckki)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], bvnhz__vckki)

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
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], bvnhz__vckki)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], bvnhz__vckki)

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
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], bvnhz__vckki)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def startswith(source, prefix):
    args = [source, prefix]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.startswith',
                ['source', 'prefix'], bvnhz__vckki)

    def impl(source, prefix):
        return startswith_util(source, prefix)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for bvnhz__vckki in range(2):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], bvnhz__vckki)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], bvnhz__vckki)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], bvnhz__vckki)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], bvnhz__vckki)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for bvnhz__vckki in range(3):
        if isinstance(args[bvnhz__vckki], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], bvnhz__vckki)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    auloe__jor = ['arr']
    tgmr__ynnoy = [arr]
    ruwr__wmwjf = [True]
    jonh__hvgm = 'if 0 <= arg0 <= 127:\n'
    jonh__hvgm += '   res[i] = chr(arg0)\n'
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '   bodo.libs.array_kernels.setna(res, i)\n'
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    auloe__jor = ['arr', 'delim']
    tgmr__ynnoy = [arr, delim]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = 'capitalized = arg0[:1].upper()\n'
    jonh__hvgm += 'for j in range(1, len(arg0)):\n'
    jonh__hvgm += '   if arg0[j-1] in arg1:\n'
    jonh__hvgm += '      capitalized += arg0[j].upper()\n'
    jonh__hvgm += '   else:\n'
    jonh__hvgm += '      capitalized += arg0[j].lower()\n'
    jonh__hvgm += 'res[i] = capitalized'
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    auloe__jor = ['arr', 'target']
    tgmr__ynnoy = [arr, target]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = 'res[i] = arg0.find(arg1) + 1'
    rby__akq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    conx__tpz, sdqs__qjj = len(s), len(t)
    zcmz__uxhdf, tqj__qqcal = 1, 0
    arr = np.zeros((2, conx__tpz + 1), dtype=np.uint32)
    arr[0, :] = np.arange(conx__tpz + 1)
    for bvnhz__vckki in range(1, sdqs__qjj + 1):
        arr[zcmz__uxhdf, 0] = bvnhz__vckki
        for hemh__lrd in range(1, conx__tpz + 1):
            if s[hemh__lrd - 1] == t[bvnhz__vckki - 1]:
                arr[zcmz__uxhdf, hemh__lrd] = arr[tqj__qqcal, hemh__lrd - 1]
            else:
                arr[zcmz__uxhdf, hemh__lrd] = 1 + min(arr[zcmz__uxhdf, 
                    hemh__lrd - 1], arr[tqj__qqcal, hemh__lrd], arr[
                    tqj__qqcal, hemh__lrd - 1])
        zcmz__uxhdf, tqj__qqcal = tqj__qqcal, zcmz__uxhdf
    return arr[sdqs__qjj % 2, conx__tpz]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    conx__tpz, sdqs__qjj = len(s), len(t)
    if conx__tpz <= maxDistance and sdqs__qjj <= maxDistance:
        return min_edit_distance(s, t)
    zcmz__uxhdf, tqj__qqcal = 1, 0
    arr = np.zeros((2, conx__tpz + 1), dtype=np.uint32)
    arr[0, :] = np.arange(conx__tpz + 1)
    for bvnhz__vckki in range(1, sdqs__qjj + 1):
        arr[zcmz__uxhdf, 0] = bvnhz__vckki
        for hemh__lrd in range(1, conx__tpz + 1):
            if s[hemh__lrd - 1] == t[bvnhz__vckki - 1]:
                arr[zcmz__uxhdf, hemh__lrd] = arr[tqj__qqcal, hemh__lrd - 1]
            else:
                arr[zcmz__uxhdf, hemh__lrd] = 1 + min(arr[zcmz__uxhdf, 
                    hemh__lrd - 1], arr[tqj__qqcal, hemh__lrd], arr[
                    tqj__qqcal, hemh__lrd - 1])
        if (arr[zcmz__uxhdf] >= maxDistance).all():
            return maxDistance
        zcmz__uxhdf, tqj__qqcal = tqj__qqcal, zcmz__uxhdf
    return min(arr[sdqs__qjj % 2, conx__tpz], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    auloe__jor = ['s', 't']
    tgmr__ynnoy = [s, t]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    rby__akq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    auloe__jor = ['s', 't', 'maxDistance']
    tgmr__ynnoy = [s, t, maxDistance]
    ruwr__wmwjf = [True] * 3
    jonh__hvgm = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    rby__akq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def endswith_util(source, suffix):
    jbh__tvfb = verify_string_binary_arg(source, 'endswith', 'source')
    if jbh__tvfb != verify_string_binary_arg(suffix, 'endswith', 'suffix'):
        raise bodo.utils.typing.BodoError(
            'String and suffix must both be strings or both binary')
    auloe__jor = ['source', 'suffix']
    tgmr__ynnoy = [source, suffix]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = 'res[i] = arg0.endswith(arg1)'
    rby__akq = bodo.boolean_array
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    auloe__jor = ['arr', 'places']
    tgmr__ynnoy = [arr, places]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = 'prec = max(arg1, 0)\n'
    jonh__hvgm += "res[i] = format(arg0, f',.{prec}f')"
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def insert_util(arr, pos, length, inject):
    jbh__tvfb = verify_string_binary_arg(arr, 'INSERT', 'arr')
    verify_int_arg(pos, 'INSERT', 'pos')
    verify_int_arg(length, 'INSERT', 'length')
    if jbh__tvfb != verify_string_binary_arg(inject, 'INSERT', 'inject'):
        raise bodo.utils.typing.BodoError(
            'String and injected value must both be strings or both binary')
    auloe__jor = ['arr', 'pos', 'length', 'inject']
    tgmr__ynnoy = [arr, pos, length, inject]
    ruwr__wmwjf = [True] * 4
    jonh__hvgm = 'prefixIndex = max(arg1-1, 0)\n'
    jonh__hvgm += 'suffixIndex = prefixIndex + max(arg2, 0)\n'
    jonh__hvgm += 'res[i] = arg0[:prefixIndex] + arg3 + arg0[suffixIndex:]'
    rby__akq = bodo.string_array_type if jbh__tvfb else bodo.binary_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        jbh__tvfb = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        cbg__izr = "''" if jbh__tvfb else "b''"
        auloe__jor = ['arr', 'n_chars']
        tgmr__ynnoy = [arr, n_chars]
        ruwr__wmwjf = [True] * 2
        jonh__hvgm = 'if arg1 <= 0:\n'
        jonh__hvgm += f'   res[i] = {cbg__izr}\n'
        jonh__hvgm += 'else:\n'
        if func_name == 'LEFT':
            jonh__hvgm += '   res[i] = arg0[:arg1]\n'
        elif func_name == 'RIGHT':
            jonh__hvgm += '   res[i] = arg0[-arg1:]\n'
        rby__akq = (bodo.string_array_type if jbh__tvfb else bodo.
            binary_array_type)
        return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf,
            jonh__hvgm, rby__akq, may_cause_duplicate_dict_array_values=True)
    return overload_left_right_util


def _install_left_right_overload():
    for ecum__lyx, func_name in zip((left_util, right_util), ('LEFT', 'RIGHT')
        ):
        arw__rcsn = create_left_right_util_overload(func_name)
        overload(ecum__lyx)(arw__rcsn)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        uppy__pmgl = verify_string_binary_arg(pad_string, func_name,
            'pad_string')
        jbh__tvfb = verify_string_binary_arg(arr, func_name, 'arr')
        if jbh__tvfb != uppy__pmgl:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        rby__akq = (bodo.string_array_type if jbh__tvfb else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            pks__yoegs = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            pks__yoegs = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        auloe__jor = ['arr', 'length', 'pad_string']
        tgmr__ynnoy = [arr, length, pad_string]
        ruwr__wmwjf = [True] * 3
        cbg__izr = "''" if jbh__tvfb else "b''"
        jonh__hvgm = f"""                if arg1 <= 0:
                    res[i] = {cbg__izr}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {pks__yoegs}"""
        return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf,
            jonh__hvgm, rby__akq, may_cause_duplicate_dict_array_values=True)
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for ecum__lyx, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')):
        arw__rcsn = create_lpad_rpad_util_overload(func_name)
        overload(ecum__lyx)(arw__rcsn)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    auloe__jor = ['arr']
    tgmr__ynnoy = [arr]
    ruwr__wmwjf = [True]
    jonh__hvgm = 'if len(arg0) == 0:\n'
    jonh__hvgm += '   bodo.libs.array_kernels.setna(res, i)\n'
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '   res[i] = ord(arg0[0])'
    rby__akq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def position_util(substr, source, start):
    qntlv__hqgt = verify_string_binary_arg(substr, 'POSITION', 'substr')
    if qntlv__hqgt != verify_string_binary_arg(source, 'POSITION', 'source'):
        raise bodo.utils.typing.BodoError(
            'Substring and source must be both strings or both binary')
    verify_int_arg(start, 'POSITION', 'start')
    assert qntlv__hqgt, '[BE-3717] Support binary find with 3 args'
    auloe__jor = ['substr', 'source', 'start']
    tgmr__ynnoy = [substr, source, start]
    ruwr__wmwjf = [True] * 3
    jonh__hvgm = 'res[i] = arg1.find(arg0, arg2 - 1) + 1'
    rby__akq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    auloe__jor = ['arr', 'repeats']
    tgmr__ynnoy = [arr, repeats]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = 'if arg1 <= 0:\n'
    jonh__hvgm += "   res[i] = ''\n"
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '   res[i] = arg0 * arg1'
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    auloe__jor = ['arr', 'to_replace', 'replace_with']
    tgmr__ynnoy = [arr, to_replace, replace_with]
    ruwr__wmwjf = [True] * 3
    jonh__hvgm = "if arg1 == '':\n"
    jonh__hvgm += '   res[i] = arg0\n'
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '   res[i] = arg0.replace(arg1, arg2)'
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    jbh__tvfb = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    auloe__jor = ['arr']
    tgmr__ynnoy = [arr]
    ruwr__wmwjf = [True]
    jonh__hvgm = 'res[i] = arg0[::-1]'
    rby__akq = bodo.string_array_type
    rby__akq = bodo.string_array_type if jbh__tvfb else bodo.binary_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def rtrimmed_length_util(arr):
    verify_string_arg(arr, 'RTRIMMED_LENGTH', 'arr')
    auloe__jor = ['arr']
    tgmr__ynnoy = [arr]
    ruwr__wmwjf = [True]
    jonh__hvgm = "res[i] = len(arg0.rstrip(' '))"
    rby__akq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    auloe__jor = ['n_chars']
    tgmr__ynnoy = [n_chars]
    ruwr__wmwjf = [True]
    jonh__hvgm = 'if arg0 <= 0:\n'
    jonh__hvgm += "   res[i] = ''\n"
    jonh__hvgm += 'else:\n'
    jonh__hvgm += "   res[i] = ' ' * arg0"
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    auloe__jor = ['source', 'delim', 'part']
    tgmr__ynnoy = [source, delim, part]
    ruwr__wmwjf = [True] * 3
    jonh__hvgm = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    jonh__hvgm += 'if abs(arg2) > len(tokens):\n'
    jonh__hvgm += "    res[i] = ''\n"
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def startswith_util(source, prefix):
    jbh__tvfb = verify_string_binary_arg(source, 'startswith', 'source')
    if jbh__tvfb != verify_string_binary_arg(prefix, 'startswith', 'prefix'):
        raise bodo.utils.typing.BodoError(
            'String and prefix must both be strings or both binary')
    auloe__jor = ['source', 'prefix']
    tgmr__ynnoy = [source, prefix]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = 'res[i] = arg0.startswith(arg1)'
    rby__akq = bodo.boolean_array
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    auloe__jor = ['arr0', 'arr1']
    tgmr__ynnoy = [arr0, arr1]
    ruwr__wmwjf = [True] * 2
    jonh__hvgm = 'if arg0 < arg1:\n'
    jonh__hvgm += '   res[i] = -1\n'
    jonh__hvgm += 'elif arg0 > arg1:\n'
    jonh__hvgm += '   res[i] = 1\n'
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '   res[i] = 0\n'
    rby__akq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    auloe__jor = ['source', 'delim', 'part']
    tgmr__ynnoy = [source, delim, part]
    ruwr__wmwjf = [True] * 3
    jonh__hvgm = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    jonh__hvgm += '   bodo.libs.array_kernels.setna(res, i)\n'
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '   tokens = []\n'
    jonh__hvgm += "   buffer = ''\n"
    jonh__hvgm += '   for j in range(len(arg0)):\n'
    jonh__hvgm += '      if arg0[j] in arg1:\n'
    jonh__hvgm += "         if buffer != '':"
    jonh__hvgm += '            tokens.append(buffer)\n'
    jonh__hvgm += "         buffer = ''\n"
    jonh__hvgm += '      else:\n'
    jonh__hvgm += '         buffer += arg0[j]\n'
    jonh__hvgm += "   if buffer != '':\n"
    jonh__hvgm += '      tokens.append(buffer)\n'
    jonh__hvgm += '   if arg2 > len(tokens):\n'
    jonh__hvgm += '      bodo.libs.array_kernels.setna(res, i)\n'
    jonh__hvgm += '   else:\n'
    jonh__hvgm += '      res[i] = tokens[arg2-1]\n'
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    jbh__tvfb = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    rby__akq = bodo.string_array_type if jbh__tvfb else bodo.binary_array_type
    auloe__jor = ['arr', 'start', 'length']
    tgmr__ynnoy = [arr, start, length]
    ruwr__wmwjf = [True] * 3
    jonh__hvgm = 'if arg2 <= 0:\n'
    jonh__hvgm += "   res[i] = ''\n" if jbh__tvfb else "   res[i] = b''\n"
    jonh__hvgm += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    jonh__hvgm += '   res[i] = arg0[arg1:]\n'
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '   if arg1 > 0: arg1 -= 1\n'
    jonh__hvgm += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    auloe__jor = ['arr', 'delimiter', 'occurrences']
    tgmr__ynnoy = [arr, delimiter, occurrences]
    ruwr__wmwjf = [True] * 3
    jonh__hvgm = "if arg1 == '' or arg2 == 0:\n"
    jonh__hvgm += "   res[i] = ''\n"
    jonh__hvgm += 'elif arg2 >= 0:\n'
    jonh__hvgm += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    jonh__hvgm += 'else:\n'
    jonh__hvgm += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    auloe__jor = ['arr', 'source', 'target']
    tgmr__ynnoy = [arr, source, target]
    ruwr__wmwjf = [True] * 3
    jonh__hvgm = "translated = ''\n"
    jonh__hvgm += 'for char in arg0:\n'
    jonh__hvgm += '   index = arg1.find(char)\n'
    jonh__hvgm += '   if index == -1:\n'
    jonh__hvgm += '      translated += char\n'
    jonh__hvgm += '   elif index < len(arg2):\n'
    jonh__hvgm += '      translated += arg2[index]\n'
    jonh__hvgm += 'res[i] = translated'
    rby__akq = bodo.string_array_type
    return gen_vectorized(auloe__jor, tgmr__ynnoy, ruwr__wmwjf, jonh__hvgm,
        rby__akq, may_cause_duplicate_dict_array_values=True)
