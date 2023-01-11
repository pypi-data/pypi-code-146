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
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.contains',
                ['arr', 'contains'], lxkbi__fgizo)

    def impl(arr, pattern):
        return contains_util(arr, pattern)
    return impl


@numba.generated_jit(nopython=True)
def contains_util(arr, pattern):
    verify_string_binary_arg(arr, 'CONTAINS', 'arr')
    verify_string_binary_arg(pattern, 'CONTAINS', 'pattern')
    jdw__vgo = bodo.boolean_array
    xnx__tzh = ['arr', 'pattern']
    pfl__ubzwr = [arr, pattern]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = 'res[i] = arg1 in arg0\n'
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def editdistance_no_max(s, t):
    args = [s, t]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], lxkbi__fgizo)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], lxkbi__fgizo)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def endswith(source, suffix):
    args = [source, suffix]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.endswith',
                ['source', 'suffix'], lxkbi__fgizo)

    def impl(source, suffix):
        return endswith_util(source, suffix)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], lxkbi__fgizo)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], lxkbi__fgizo)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def insert(source, pos, length, inject):
    args = [source, pos, length, inject]
    for lxkbi__fgizo in range(4):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.insert',
                ['source', 'pos', 'length', 'inject'], lxkbi__fgizo)

    def impl(source, pos, length, inject):
        return insert_util(source, pos, length, inject)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], lxkbi__fgizo)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], lxkbi__fgizo)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], lxkbi__fgizo)

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
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.position',
                ['substr', 'source', 'start'], lxkbi__fgizo)

    def impl(substr, source, start):
        return position_util(substr, source, start)
    return impl


@numba.generated_jit(nopython=True)
def repeat(arr, repeats):
    args = [arr, repeats]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], lxkbi__fgizo)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], lxkbi__fgizo)

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
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], lxkbi__fgizo)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], lxkbi__fgizo)

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
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], lxkbi__fgizo)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def startswith(source, prefix):
    args = [source, prefix]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.startswith',
                ['source', 'prefix'], lxkbi__fgizo)

    def impl(source, prefix):
        return startswith_util(source, prefix)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for lxkbi__fgizo in range(2):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], lxkbi__fgizo)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], lxkbi__fgizo)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], lxkbi__fgizo)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], lxkbi__fgizo)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for lxkbi__fgizo in range(3):
        if isinstance(args[lxkbi__fgizo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], lxkbi__fgizo)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    xnx__tzh = ['arr']
    pfl__ubzwr = [arr]
    ltaca__gfir = [True]
    gxxar__rfygv = 'if 0 <= arg0 <= 127:\n'
    gxxar__rfygv += '   res[i] = chr(arg0)\n'
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '   bodo.libs.array_kernels.setna(res, i)\n'
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    xnx__tzh = ['arr', 'delim']
    pfl__ubzwr = [arr, delim]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = 'capitalized = arg0[:1].upper()\n'
    gxxar__rfygv += 'for j in range(1, len(arg0)):\n'
    gxxar__rfygv += '   if arg0[j-1] in arg1:\n'
    gxxar__rfygv += '      capitalized += arg0[j].upper()\n'
    gxxar__rfygv += '   else:\n'
    gxxar__rfygv += '      capitalized += arg0[j].lower()\n'
    gxxar__rfygv += 'res[i] = capitalized'
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    xnx__tzh = ['arr', 'target']
    pfl__ubzwr = [arr, target]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = 'res[i] = arg0.find(arg1) + 1'
    jdw__vgo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    mmnsc__wbsy, jwpu__ondt = len(s), len(t)
    dcffb__tjkm, povnr__vtey = 1, 0
    arr = np.zeros((2, mmnsc__wbsy + 1), dtype=np.uint32)
    arr[0, :] = np.arange(mmnsc__wbsy + 1)
    for lxkbi__fgizo in range(1, jwpu__ondt + 1):
        arr[dcffb__tjkm, 0] = lxkbi__fgizo
        for wwxzk__cqk in range(1, mmnsc__wbsy + 1):
            if s[wwxzk__cqk - 1] == t[lxkbi__fgizo - 1]:
                arr[dcffb__tjkm, wwxzk__cqk] = arr[povnr__vtey, wwxzk__cqk - 1]
            else:
                arr[dcffb__tjkm, wwxzk__cqk] = 1 + min(arr[dcffb__tjkm, 
                    wwxzk__cqk - 1], arr[povnr__vtey, wwxzk__cqk], arr[
                    povnr__vtey, wwxzk__cqk - 1])
        dcffb__tjkm, povnr__vtey = povnr__vtey, dcffb__tjkm
    return arr[jwpu__ondt % 2, mmnsc__wbsy]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    mmnsc__wbsy, jwpu__ondt = len(s), len(t)
    if mmnsc__wbsy <= maxDistance and jwpu__ondt <= maxDistance:
        return min_edit_distance(s, t)
    dcffb__tjkm, povnr__vtey = 1, 0
    arr = np.zeros((2, mmnsc__wbsy + 1), dtype=np.uint32)
    arr[0, :] = np.arange(mmnsc__wbsy + 1)
    for lxkbi__fgizo in range(1, jwpu__ondt + 1):
        arr[dcffb__tjkm, 0] = lxkbi__fgizo
        for wwxzk__cqk in range(1, mmnsc__wbsy + 1):
            if s[wwxzk__cqk - 1] == t[lxkbi__fgizo - 1]:
                arr[dcffb__tjkm, wwxzk__cqk] = arr[povnr__vtey, wwxzk__cqk - 1]
            else:
                arr[dcffb__tjkm, wwxzk__cqk] = 1 + min(arr[dcffb__tjkm, 
                    wwxzk__cqk - 1], arr[povnr__vtey, wwxzk__cqk], arr[
                    povnr__vtey, wwxzk__cqk - 1])
        if (arr[dcffb__tjkm] >= maxDistance).all():
            return maxDistance
        dcffb__tjkm, povnr__vtey = povnr__vtey, dcffb__tjkm
    return min(arr[jwpu__ondt % 2, mmnsc__wbsy], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    xnx__tzh = ['s', 't']
    pfl__ubzwr = [s, t]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    jdw__vgo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    xnx__tzh = ['s', 't', 'maxDistance']
    pfl__ubzwr = [s, t, maxDistance]
    ltaca__gfir = [True] * 3
    gxxar__rfygv = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    jdw__vgo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def endswith_util(source, suffix):
    sqmkm__vxtd = verify_string_binary_arg(source, 'endswith', 'source')
    if sqmkm__vxtd != verify_string_binary_arg(suffix, 'endswith', 'suffix'):
        raise bodo.utils.typing.BodoError(
            'String and suffix must both be strings or both binary')
    xnx__tzh = ['source', 'suffix']
    pfl__ubzwr = [source, suffix]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = 'res[i] = arg0.endswith(arg1)'
    jdw__vgo = bodo.boolean_array
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    xnx__tzh = ['arr', 'places']
    pfl__ubzwr = [arr, places]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = 'prec = max(arg1, 0)\n'
    gxxar__rfygv += "res[i] = format(arg0, f',.{prec}f')"
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def insert_util(arr, pos, length, inject):
    sqmkm__vxtd = verify_string_binary_arg(arr, 'INSERT', 'arr')
    verify_int_arg(pos, 'INSERT', 'pos')
    verify_int_arg(length, 'INSERT', 'length')
    if sqmkm__vxtd != verify_string_binary_arg(inject, 'INSERT', 'inject'):
        raise bodo.utils.typing.BodoError(
            'String and injected value must both be strings or both binary')
    xnx__tzh = ['arr', 'pos', 'length', 'inject']
    pfl__ubzwr = [arr, pos, length, inject]
    ltaca__gfir = [True] * 4
    gxxar__rfygv = 'prefixIndex = max(arg1-1, 0)\n'
    gxxar__rfygv += 'suffixIndex = prefixIndex + max(arg2, 0)\n'
    gxxar__rfygv += 'res[i] = arg0[:prefixIndex] + arg3 + arg0[suffixIndex:]'
    jdw__vgo = (bodo.string_array_type if sqmkm__vxtd else bodo.
        binary_array_type)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        sqmkm__vxtd = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        uzfn__ano = "''" if sqmkm__vxtd else "b''"
        xnx__tzh = ['arr', 'n_chars']
        pfl__ubzwr = [arr, n_chars]
        ltaca__gfir = [True] * 2
        gxxar__rfygv = 'if arg1 <= 0:\n'
        gxxar__rfygv += f'   res[i] = {uzfn__ano}\n'
        gxxar__rfygv += 'else:\n'
        if func_name == 'LEFT':
            gxxar__rfygv += '   res[i] = arg0[:arg1]\n'
        elif func_name == 'RIGHT':
            gxxar__rfygv += '   res[i] = arg0[-arg1:]\n'
        jdw__vgo = (bodo.string_array_type if sqmkm__vxtd else bodo.
            binary_array_type)
        return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir,
            gxxar__rfygv, jdw__vgo, may_cause_duplicate_dict_array_values=True)
    return overload_left_right_util


def _install_left_right_overload():
    for zfpgt__cpo, func_name in zip((left_util, right_util), ('LEFT', 'RIGHT')
        ):
        clu__vrc = create_left_right_util_overload(func_name)
        overload(zfpgt__cpo)(clu__vrc)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        bdlsu__chrch = verify_string_binary_arg(pad_string, func_name,
            'pad_string')
        sqmkm__vxtd = verify_string_binary_arg(arr, func_name, 'arr')
        if sqmkm__vxtd != bdlsu__chrch:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        jdw__vgo = (bodo.string_array_type if sqmkm__vxtd else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            ocnis__olgul = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            ocnis__olgul = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        xnx__tzh = ['arr', 'length', 'pad_string']
        pfl__ubzwr = [arr, length, pad_string]
        ltaca__gfir = [True] * 3
        uzfn__ano = "''" if sqmkm__vxtd else "b''"
        gxxar__rfygv = f"""                if arg1 <= 0:
                    res[i] = {uzfn__ano}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {ocnis__olgul}"""
        return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir,
            gxxar__rfygv, jdw__vgo, may_cause_duplicate_dict_array_values=True)
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for zfpgt__cpo, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')):
        clu__vrc = create_lpad_rpad_util_overload(func_name)
        overload(zfpgt__cpo)(clu__vrc)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    xnx__tzh = ['arr']
    pfl__ubzwr = [arr]
    ltaca__gfir = [True]
    gxxar__rfygv = 'if len(arg0) == 0:\n'
    gxxar__rfygv += '   bodo.libs.array_kernels.setna(res, i)\n'
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '   res[i] = ord(arg0[0])'
    jdw__vgo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def position_util(substr, source, start):
    njfxm__yut = verify_string_binary_arg(substr, 'POSITION', 'substr')
    if njfxm__yut != verify_string_binary_arg(source, 'POSITION', 'source'):
        raise bodo.utils.typing.BodoError(
            'Substring and source must be both strings or both binary')
    verify_int_arg(start, 'POSITION', 'start')
    assert njfxm__yut, '[BE-3717] Support binary find with 3 args'
    xnx__tzh = ['substr', 'source', 'start']
    pfl__ubzwr = [substr, source, start]
    ltaca__gfir = [True] * 3
    gxxar__rfygv = 'res[i] = arg1.find(arg0, arg2 - 1) + 1'
    jdw__vgo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    xnx__tzh = ['arr', 'repeats']
    pfl__ubzwr = [arr, repeats]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = 'if arg1 <= 0:\n'
    gxxar__rfygv += "   res[i] = ''\n"
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '   res[i] = arg0 * arg1'
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    xnx__tzh = ['arr', 'to_replace', 'replace_with']
    pfl__ubzwr = [arr, to_replace, replace_with]
    ltaca__gfir = [True] * 3
    gxxar__rfygv = "if arg1 == '':\n"
    gxxar__rfygv += '   res[i] = arg0\n'
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '   res[i] = arg0.replace(arg1, arg2)'
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    sqmkm__vxtd = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    xnx__tzh = ['arr']
    pfl__ubzwr = [arr]
    ltaca__gfir = [True]
    gxxar__rfygv = 'res[i] = arg0[::-1]'
    jdw__vgo = bodo.string_array_type
    jdw__vgo = (bodo.string_array_type if sqmkm__vxtd else bodo.
        binary_array_type)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def rtrimmed_length_util(arr):
    verify_string_arg(arr, 'RTRIMMED_LENGTH', 'arr')
    xnx__tzh = ['arr']
    pfl__ubzwr = [arr]
    ltaca__gfir = [True]
    gxxar__rfygv = "res[i] = len(arg0.rstrip(' '))"
    jdw__vgo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    xnx__tzh = ['n_chars']
    pfl__ubzwr = [n_chars]
    ltaca__gfir = [True]
    gxxar__rfygv = 'if arg0 <= 0:\n'
    gxxar__rfygv += "   res[i] = ''\n"
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += "   res[i] = ' ' * arg0"
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    xnx__tzh = ['source', 'delim', 'part']
    pfl__ubzwr = [source, delim, part]
    ltaca__gfir = [True] * 3
    gxxar__rfygv = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    gxxar__rfygv += 'if abs(arg2) > len(tokens):\n'
    gxxar__rfygv += "    res[i] = ''\n"
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def startswith_util(source, prefix):
    sqmkm__vxtd = verify_string_binary_arg(source, 'startswith', 'source')
    if sqmkm__vxtd != verify_string_binary_arg(prefix, 'startswith', 'prefix'):
        raise bodo.utils.typing.BodoError(
            'String and prefix must both be strings or both binary')
    xnx__tzh = ['source', 'prefix']
    pfl__ubzwr = [source, prefix]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = 'res[i] = arg0.startswith(arg1)'
    jdw__vgo = bodo.boolean_array
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    xnx__tzh = ['arr0', 'arr1']
    pfl__ubzwr = [arr0, arr1]
    ltaca__gfir = [True] * 2
    gxxar__rfygv = 'if arg0 < arg1:\n'
    gxxar__rfygv += '   res[i] = -1\n'
    gxxar__rfygv += 'elif arg0 > arg1:\n'
    gxxar__rfygv += '   res[i] = 1\n'
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '   res[i] = 0\n'
    jdw__vgo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    xnx__tzh = ['source', 'delim', 'part']
    pfl__ubzwr = [source, delim, part]
    ltaca__gfir = [True] * 3
    gxxar__rfygv = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    gxxar__rfygv += '   bodo.libs.array_kernels.setna(res, i)\n'
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '   tokens = []\n'
    gxxar__rfygv += "   buffer = ''\n"
    gxxar__rfygv += '   for j in range(len(arg0)):\n'
    gxxar__rfygv += '      if arg0[j] in arg1:\n'
    gxxar__rfygv += "         if buffer != '':"
    gxxar__rfygv += '            tokens.append(buffer)\n'
    gxxar__rfygv += "         buffer = ''\n"
    gxxar__rfygv += '      else:\n'
    gxxar__rfygv += '         buffer += arg0[j]\n'
    gxxar__rfygv += "   if buffer != '':\n"
    gxxar__rfygv += '      tokens.append(buffer)\n'
    gxxar__rfygv += '   if arg2 > len(tokens):\n'
    gxxar__rfygv += '      bodo.libs.array_kernels.setna(res, i)\n'
    gxxar__rfygv += '   else:\n'
    gxxar__rfygv += '      res[i] = tokens[arg2-1]\n'
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    sqmkm__vxtd = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    jdw__vgo = (bodo.string_array_type if sqmkm__vxtd else bodo.
        binary_array_type)
    xnx__tzh = ['arr', 'start', 'length']
    pfl__ubzwr = [arr, start, length]
    ltaca__gfir = [True] * 3
    gxxar__rfygv = 'if arg2 <= 0:\n'
    gxxar__rfygv += "   res[i] = ''\n" if sqmkm__vxtd else "   res[i] = b''\n"
    gxxar__rfygv += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    gxxar__rfygv += '   res[i] = arg0[arg1:]\n'
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '   if arg1 > 0: arg1 -= 1\n'
    gxxar__rfygv += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    xnx__tzh = ['arr', 'delimiter', 'occurrences']
    pfl__ubzwr = [arr, delimiter, occurrences]
    ltaca__gfir = [True] * 3
    gxxar__rfygv = "if arg1 == '' or arg2 == 0:\n"
    gxxar__rfygv += "   res[i] = ''\n"
    gxxar__rfygv += 'elif arg2 >= 0:\n'
    gxxar__rfygv += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    gxxar__rfygv += 'else:\n'
    gxxar__rfygv += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    xnx__tzh = ['arr', 'source', 'target']
    pfl__ubzwr = [arr, source, target]
    ltaca__gfir = [True] * 3
    gxxar__rfygv = "translated = ''\n"
    gxxar__rfygv += 'for char in arg0:\n'
    gxxar__rfygv += '   index = arg1.find(char)\n'
    gxxar__rfygv += '   if index == -1:\n'
    gxxar__rfygv += '      translated += char\n'
    gxxar__rfygv += '   elif index < len(arg2):\n'
    gxxar__rfygv += '      translated += arg2[index]\n'
    gxxar__rfygv += 'res[i] = translated'
    jdw__vgo = bodo.string_array_type
    return gen_vectorized(xnx__tzh, pfl__ubzwr, ltaca__gfir, gxxar__rfygv,
        jdw__vgo, may_cause_duplicate_dict_array_values=True)
