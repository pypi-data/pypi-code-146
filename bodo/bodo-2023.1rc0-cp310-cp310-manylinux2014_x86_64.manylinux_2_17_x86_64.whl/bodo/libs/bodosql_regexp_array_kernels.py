"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    itw__ywsh = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for beph__pzqxv in itw__ywsh:
        pattern = pattern.replace(beph__pzqxv, itw__ywsh[beph__pzqxv])
    return pattern


def make_flag_bitvector(flags):
    phe__xfz = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            phe__xfz = phe__xfz | re.I
    if 'm' in flags:
        phe__xfz = phe__xfz | re.M
    if 's' in flags:
        phe__xfz = phe__xfz | re.S
    return phe__xfz


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for rwpz__apwwt in range(4):
        if isinstance(args[rwpz__apwwt], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], rwpz__apwwt)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for rwpz__apwwt in range(7):
        if isinstance(args[rwpz__apwwt], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], rwpz__apwwt)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for rwpz__apwwt in range(3):
        if isinstance(args[rwpz__apwwt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], rwpz__apwwt)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for rwpz__apwwt in range(6):
        if isinstance(args[rwpz__apwwt], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], rwpz__apwwt)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for rwpz__apwwt in range(6):
        if isinstance(args[rwpz__apwwt], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                rwpz__apwwt)

    def impl(arr, pattern, position, occurrence, flags, group):
        return regexp_substr_util(arr, numba.literally(pattern), position,
            occurrence, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_count_util(arr, pattern, position, flags):
    verify_string_arg(arr, 'REGEXP_COUNT', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_COUNT', 'pattern')
    verify_int_arg(position, 'REGEXP_COUNT', 'position')
    verify_scalar_string_arg(flags, 'REGEXP_COUNT', 'flags')
    ygmml__hsyd = ['arr', 'pattern', 'position', 'flags']
    ckeff__ynmn = [arr, pattern, position, flags]
    asz__ncnce = [True] * 4
    yyjhi__cjh = bodo.utils.typing.get_overload_const_str(pattern)
    heed__xtcta = posix_to_re(yyjhi__cjh)
    eocak__zxm = bodo.utils.typing.get_overload_const_str(flags)
    qqdd__hdfhl = make_flag_bitvector(eocak__zxm)
    yplf__hsb = '\n'
    nlbn__lsuk = ''
    if bodo.utils.utils.is_array_typ(position, True):
        nlbn__lsuk += """if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    else:
        yplf__hsb += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if heed__xtcta == '':
        nlbn__lsuk += 'res[i] = 0'
    else:
        yplf__hsb += f'r = re.compile({repr(heed__xtcta)}, {qqdd__hdfhl})'
        nlbn__lsuk += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    tbkq__wma = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(ygmml__hsyd, ckeff__ynmn, asz__ncnce, nlbn__lsuk,
        tbkq__wma, prefix_code=yplf__hsb)


@numba.generated_jit(nopython=True)
def regexp_instr_util(arr, pattern, position, occurrence, option, flags, group
    ):
    verify_string_arg(arr, 'REGEXP_INSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_INSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_INSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_INSTR', 'occurrence')
    verify_int_arg(option, 'REGEXP_INSTR', 'option')
    verify_scalar_string_arg(flags, 'REGEXP_INSTR', 'flags')
    verify_int_arg(group, 'REGEXP_INSTR', 'group')
    ygmml__hsyd = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    ckeff__ynmn = [arr, pattern, position, occurrence, option, flags, group]
    asz__ncnce = [True] * 7
    yyjhi__cjh = bodo.utils.typing.get_overload_const_str(pattern)
    heed__xtcta = posix_to_re(yyjhi__cjh)
    dnn__dwss = re.compile(yyjhi__cjh).groups
    eocak__zxm = bodo.utils.typing.get_overload_const_str(flags)
    qqdd__hdfhl = make_flag_bitvector(eocak__zxm)
    yplf__hsb = '\n'
    nlbn__lsuk = ''
    if bodo.utils.utils.is_array_typ(position, True):
        nlbn__lsuk += """if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    else:
        yplf__hsb += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        nlbn__lsuk += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        yplf__hsb += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        nlbn__lsuk += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        yplf__hsb += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in eocak__zxm:
        if bodo.utils.utils.is_array_typ(group, True):
            nlbn__lsuk += f"""if not (1 <= arg6 <= {dnn__dwss}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            yplf__hsb += f"""if not (1 <= group <= {dnn__dwss}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if heed__xtcta == '':
        nlbn__lsuk += 'res[i] = 0'
    else:
        yplf__hsb += f'r = re.compile({repr(heed__xtcta)}, {qqdd__hdfhl})'
        nlbn__lsuk += 'arg0 = arg0[arg2-1:]\n'
        nlbn__lsuk += 'res[i] = 0\n'
        nlbn__lsuk += 'offset = arg2\n'
        nlbn__lsuk += 'for j in range(arg3):\n'
        nlbn__lsuk += '   match = r.search(arg0)\n'
        nlbn__lsuk += '   if match is None:\n'
        nlbn__lsuk += '      res[i] = 0\n'
        nlbn__lsuk += '      break\n'
        nlbn__lsuk += '   start, end = match.span()\n'
        nlbn__lsuk += '   if j == arg3 - 1:\n'
        if 'e' in eocak__zxm:
            nlbn__lsuk += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            nlbn__lsuk += '      res[i] = offset + match.span()[arg4]\n'
        nlbn__lsuk += '   else:\n'
        nlbn__lsuk += '      offset += end\n'
        nlbn__lsuk += '      arg0 = arg0[end:]\n'
    tbkq__wma = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(ygmml__hsyd, ckeff__ynmn, asz__ncnce, nlbn__lsuk,
        tbkq__wma, prefix_code=yplf__hsb)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    ygmml__hsyd = ['arr', 'pattern', 'flags']
    ckeff__ynmn = [arr, pattern, flags]
    asz__ncnce = [True] * 3
    yyjhi__cjh = bodo.utils.typing.get_overload_const_str(pattern)
    heed__xtcta = posix_to_re(yyjhi__cjh)
    eocak__zxm = bodo.utils.typing.get_overload_const_str(flags)
    qqdd__hdfhl = make_flag_bitvector(eocak__zxm)
    if heed__xtcta == '':
        yplf__hsb = None
        nlbn__lsuk = 'res[i] = len(arg0) == 0'
    else:
        yplf__hsb = f'r = re.compile({repr(heed__xtcta)}, {qqdd__hdfhl})'
        nlbn__lsuk = 'if r.fullmatch(arg0) is None:\n'
        nlbn__lsuk += '   res[i] = False\n'
        nlbn__lsuk += 'else:\n'
        nlbn__lsuk += '   res[i] = True\n'
    tbkq__wma = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(ygmml__hsyd, ckeff__ynmn, asz__ncnce, nlbn__lsuk,
        tbkq__wma, prefix_code=yplf__hsb)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    ygmml__hsyd = ['arr', 'pattern', 'replacement', 'position',
        'occurrence', 'flags']
    ckeff__ynmn = [arr, pattern, replacement, position, occurrence, flags]
    asz__ncnce = [True] * 6
    yyjhi__cjh = bodo.utils.typing.get_overload_const_str(pattern)
    heed__xtcta = posix_to_re(yyjhi__cjh)
    eocak__zxm = bodo.utils.typing.get_overload_const_str(flags)
    qqdd__hdfhl = make_flag_bitvector(eocak__zxm)
    yplf__hsb = '\n'
    nlbn__lsuk = ''
    if bodo.utils.utils.is_array_typ(position, True):
        nlbn__lsuk += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        yplf__hsb += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        nlbn__lsuk += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        yplf__hsb += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if heed__xtcta == '':
        nlbn__lsuk += 'res[i] = arg0'
    else:
        yplf__hsb += f'r = re.compile({repr(heed__xtcta)}, {qqdd__hdfhl})'
        nlbn__lsuk += 'result = arg0[:arg3-1]\n'
        nlbn__lsuk += 'arg0 = arg0[arg3-1:]\n'
        nlbn__lsuk += 'if arg4 == 0:\n'
        nlbn__lsuk += '   res[i] = result + r.sub(arg2, arg0)\n'
        nlbn__lsuk += 'else:\n'
        nlbn__lsuk += '   nomatch = False\n'
        nlbn__lsuk += '   for j in range(arg4 - 1):\n'
        nlbn__lsuk += '      match = r.search(arg0)\n'
        nlbn__lsuk += '      if match is None:\n'
        nlbn__lsuk += '         res[i] = result + arg0\n'
        nlbn__lsuk += '         nomatch = True\n'
        nlbn__lsuk += '         break\n'
        nlbn__lsuk += '      _, end = match.span()\n'
        nlbn__lsuk += '      result += arg0[:end]\n'
        nlbn__lsuk += '      arg0 = arg0[end:]\n'
        nlbn__lsuk += '   if nomatch == False:\n'
        nlbn__lsuk += '      result += r.sub(arg2, arg0, count=1)\n'
        nlbn__lsuk += '      res[i] = result'
    tbkq__wma = bodo.string_array_type
    return gen_vectorized(ygmml__hsyd, ckeff__ynmn, asz__ncnce, nlbn__lsuk,
        tbkq__wma, prefix_code=yplf__hsb)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    ygmml__hsyd = ['arr', 'pattern', 'position', 'occurrence', 'flags', 'group'
        ]
    ckeff__ynmn = [arr, pattern, position, occurrence, flags, group]
    asz__ncnce = [True] * 6
    yyjhi__cjh = bodo.utils.typing.get_overload_const_str(pattern)
    heed__xtcta = posix_to_re(yyjhi__cjh)
    dnn__dwss = re.compile(yyjhi__cjh).groups
    eocak__zxm = bodo.utils.typing.get_overload_const_str(flags)
    qqdd__hdfhl = make_flag_bitvector(eocak__zxm)
    yplf__hsb = '\n'
    nlbn__lsuk = ''
    if bodo.utils.utils.is_array_typ(position, True):
        nlbn__lsuk += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        yplf__hsb += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        nlbn__lsuk += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        yplf__hsb += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in eocak__zxm:
        if bodo.utils.utils.is_array_typ(group, True):
            nlbn__lsuk += f"""if not (1 <= arg5 <= {dnn__dwss}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            yplf__hsb += f"""if not (1 <= group <= {dnn__dwss}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if heed__xtcta == '':
        nlbn__lsuk += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        yplf__hsb += f'r = re.compile({repr(heed__xtcta)}, {qqdd__hdfhl})'
        if 'e' in eocak__zxm:
            nlbn__lsuk += 'matches = r.findall(arg0[arg2-1:])\n'
            nlbn__lsuk += f'if len(matches) < arg3:\n'
            nlbn__lsuk += '   bodo.libs.array_kernels.setna(res, i)\n'
            nlbn__lsuk += 'else:\n'
            if dnn__dwss == 1:
                nlbn__lsuk += '   res[i] = matches[arg3-1]\n'
            else:
                nlbn__lsuk += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            nlbn__lsuk += 'arg0 = str(arg0)[arg2-1:]\n'
            nlbn__lsuk += 'for j in range(arg3):\n'
            nlbn__lsuk += '   match = r.search(arg0)\n'
            nlbn__lsuk += '   if match is None:\n'
            nlbn__lsuk += '      bodo.libs.array_kernels.setna(res, i)\n'
            nlbn__lsuk += '      break\n'
            nlbn__lsuk += '   start, end = match.span()\n'
            nlbn__lsuk += '   if j == arg3 - 1:\n'
            nlbn__lsuk += '      res[i] = arg0[start:end]\n'
            nlbn__lsuk += '   else:\n'
            nlbn__lsuk += '      arg0 = arg0[end:]\n'
    tbkq__wma = bodo.string_array_type
    return gen_vectorized(ygmml__hsyd, ckeff__ynmn, asz__ncnce, nlbn__lsuk,
        tbkq__wma, prefix_code=yplf__hsb)
