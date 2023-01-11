"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    jag__ammmp = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for ygqz__xrdx in jag__ammmp:
        pattern = pattern.replace(ygqz__xrdx, jag__ammmp[ygqz__xrdx])
    return pattern


def make_flag_bitvector(flags):
    vfgb__add = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            vfgb__add = vfgb__add | re.I
    if 'm' in flags:
        vfgb__add = vfgb__add | re.M
    if 's' in flags:
        vfgb__add = vfgb__add | re.S
    return vfgb__add


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for tzlmj__iyi in range(4):
        if isinstance(args[tzlmj__iyi], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], tzlmj__iyi)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for tzlmj__iyi in range(7):
        if isinstance(args[tzlmj__iyi], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], tzlmj__iyi)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for tzlmj__iyi in range(3):
        if isinstance(args[tzlmj__iyi], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], tzlmj__iyi)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for tzlmj__iyi in range(6):
        if isinstance(args[tzlmj__iyi], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], tzlmj__iyi)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for tzlmj__iyi in range(6):
        if isinstance(args[tzlmj__iyi], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                tzlmj__iyi)

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
    aebq__doun = ['arr', 'pattern', 'position', 'flags']
    krzg__eclft = [arr, pattern, position, flags]
    lyl__ibva = [True] * 4
    mzc__fre = bodo.utils.typing.get_overload_const_str(pattern)
    hmt__ocwv = posix_to_re(mzc__fre)
    bzm__yxf = bodo.utils.typing.get_overload_const_str(flags)
    daa__hep = make_flag_bitvector(bzm__yxf)
    brd__jynuo = '\n'
    sep__ndqd = ''
    if bodo.utils.utils.is_array_typ(position, True):
        sep__ndqd += """if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    else:
        brd__jynuo += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if hmt__ocwv == '':
        sep__ndqd += 'res[i] = 0'
    else:
        brd__jynuo += f'r = re.compile({repr(hmt__ocwv)}, {daa__hep})'
        sep__ndqd += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    ofhx__ixmjy = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(aebq__doun, krzg__eclft, lyl__ibva, sep__ndqd,
        ofhx__ixmjy, prefix_code=brd__jynuo)


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
    aebq__doun = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    krzg__eclft = [arr, pattern, position, occurrence, option, flags, group]
    lyl__ibva = [True] * 7
    mzc__fre = bodo.utils.typing.get_overload_const_str(pattern)
    hmt__ocwv = posix_to_re(mzc__fre)
    dri__kux = re.compile(mzc__fre).groups
    bzm__yxf = bodo.utils.typing.get_overload_const_str(flags)
    daa__hep = make_flag_bitvector(bzm__yxf)
    brd__jynuo = '\n'
    sep__ndqd = ''
    if bodo.utils.utils.is_array_typ(position, True):
        sep__ndqd += """if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    else:
        brd__jynuo += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        sep__ndqd += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        brd__jynuo += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        sep__ndqd += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        brd__jynuo += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in bzm__yxf:
        if bodo.utils.utils.is_array_typ(group, True):
            sep__ndqd += f"""if not (1 <= arg6 <= {dri__kux}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            brd__jynuo += f"""if not (1 <= group <= {dri__kux}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if hmt__ocwv == '':
        sep__ndqd += 'res[i] = 0'
    else:
        brd__jynuo += f'r = re.compile({repr(hmt__ocwv)}, {daa__hep})'
        sep__ndqd += 'arg0 = arg0[arg2-1:]\n'
        sep__ndqd += 'res[i] = 0\n'
        sep__ndqd += 'offset = arg2\n'
        sep__ndqd += 'for j in range(arg3):\n'
        sep__ndqd += '   match = r.search(arg0)\n'
        sep__ndqd += '   if match is None:\n'
        sep__ndqd += '      res[i] = 0\n'
        sep__ndqd += '      break\n'
        sep__ndqd += '   start, end = match.span()\n'
        sep__ndqd += '   if j == arg3 - 1:\n'
        if 'e' in bzm__yxf:
            sep__ndqd += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            sep__ndqd += '      res[i] = offset + match.span()[arg4]\n'
        sep__ndqd += '   else:\n'
        sep__ndqd += '      offset += end\n'
        sep__ndqd += '      arg0 = arg0[end:]\n'
    ofhx__ixmjy = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(aebq__doun, krzg__eclft, lyl__ibva, sep__ndqd,
        ofhx__ixmjy, prefix_code=brd__jynuo)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    aebq__doun = ['arr', 'pattern', 'flags']
    krzg__eclft = [arr, pattern, flags]
    lyl__ibva = [True] * 3
    mzc__fre = bodo.utils.typing.get_overload_const_str(pattern)
    hmt__ocwv = posix_to_re(mzc__fre)
    bzm__yxf = bodo.utils.typing.get_overload_const_str(flags)
    daa__hep = make_flag_bitvector(bzm__yxf)
    if hmt__ocwv == '':
        brd__jynuo = None
        sep__ndqd = 'res[i] = len(arg0) == 0'
    else:
        brd__jynuo = f'r = re.compile({repr(hmt__ocwv)}, {daa__hep})'
        sep__ndqd = 'if r.fullmatch(arg0) is None:\n'
        sep__ndqd += '   res[i] = False\n'
        sep__ndqd += 'else:\n'
        sep__ndqd += '   res[i] = True\n'
    ofhx__ixmjy = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(aebq__doun, krzg__eclft, lyl__ibva, sep__ndqd,
        ofhx__ixmjy, prefix_code=brd__jynuo)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    aebq__doun = ['arr', 'pattern', 'replacement', 'position', 'occurrence',
        'flags']
    krzg__eclft = [arr, pattern, replacement, position, occurrence, flags]
    lyl__ibva = [True] * 6
    mzc__fre = bodo.utils.typing.get_overload_const_str(pattern)
    hmt__ocwv = posix_to_re(mzc__fre)
    bzm__yxf = bodo.utils.typing.get_overload_const_str(flags)
    daa__hep = make_flag_bitvector(bzm__yxf)
    brd__jynuo = '\n'
    sep__ndqd = ''
    if bodo.utils.utils.is_array_typ(position, True):
        sep__ndqd += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        brd__jynuo += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        sep__ndqd += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        brd__jynuo += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if hmt__ocwv == '':
        sep__ndqd += 'res[i] = arg0'
    else:
        brd__jynuo += f'r = re.compile({repr(hmt__ocwv)}, {daa__hep})'
        sep__ndqd += 'result = arg0[:arg3-1]\n'
        sep__ndqd += 'arg0 = arg0[arg3-1:]\n'
        sep__ndqd += 'if arg4 == 0:\n'
        sep__ndqd += '   res[i] = result + r.sub(arg2, arg0)\n'
        sep__ndqd += 'else:\n'
        sep__ndqd += '   nomatch = False\n'
        sep__ndqd += '   for j in range(arg4 - 1):\n'
        sep__ndqd += '      match = r.search(arg0)\n'
        sep__ndqd += '      if match is None:\n'
        sep__ndqd += '         res[i] = result + arg0\n'
        sep__ndqd += '         nomatch = True\n'
        sep__ndqd += '         break\n'
        sep__ndqd += '      _, end = match.span()\n'
        sep__ndqd += '      result += arg0[:end]\n'
        sep__ndqd += '      arg0 = arg0[end:]\n'
        sep__ndqd += '   if nomatch == False:\n'
        sep__ndqd += '      result += r.sub(arg2, arg0, count=1)\n'
        sep__ndqd += '      res[i] = result'
    ofhx__ixmjy = bodo.string_array_type
    return gen_vectorized(aebq__doun, krzg__eclft, lyl__ibva, sep__ndqd,
        ofhx__ixmjy, prefix_code=brd__jynuo)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    aebq__doun = ['arr', 'pattern', 'position', 'occurrence', 'flags', 'group']
    krzg__eclft = [arr, pattern, position, occurrence, flags, group]
    lyl__ibva = [True] * 6
    mzc__fre = bodo.utils.typing.get_overload_const_str(pattern)
    hmt__ocwv = posix_to_re(mzc__fre)
    dri__kux = re.compile(mzc__fre).groups
    bzm__yxf = bodo.utils.typing.get_overload_const_str(flags)
    daa__hep = make_flag_bitvector(bzm__yxf)
    brd__jynuo = '\n'
    sep__ndqd = ''
    if bodo.utils.utils.is_array_typ(position, True):
        sep__ndqd += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        brd__jynuo += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        sep__ndqd += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        brd__jynuo += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in bzm__yxf:
        if bodo.utils.utils.is_array_typ(group, True):
            sep__ndqd += f"""if not (1 <= arg5 <= {dri__kux}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            brd__jynuo += f"""if not (1 <= group <= {dri__kux}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if hmt__ocwv == '':
        sep__ndqd += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        brd__jynuo += f'r = re.compile({repr(hmt__ocwv)}, {daa__hep})'
        if 'e' in bzm__yxf:
            sep__ndqd += 'matches = r.findall(arg0[arg2-1:])\n'
            sep__ndqd += f'if len(matches) < arg3:\n'
            sep__ndqd += '   bodo.libs.array_kernels.setna(res, i)\n'
            sep__ndqd += 'else:\n'
            if dri__kux == 1:
                sep__ndqd += '   res[i] = matches[arg3-1]\n'
            else:
                sep__ndqd += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            sep__ndqd += 'arg0 = str(arg0)[arg2-1:]\n'
            sep__ndqd += 'for j in range(arg3):\n'
            sep__ndqd += '   match = r.search(arg0)\n'
            sep__ndqd += '   if match is None:\n'
            sep__ndqd += '      bodo.libs.array_kernels.setna(res, i)\n'
            sep__ndqd += '      break\n'
            sep__ndqd += '   start, end = match.span()\n'
            sep__ndqd += '   if j == arg3 - 1:\n'
            sep__ndqd += '      res[i] = arg0[start:end]\n'
            sep__ndqd += '   else:\n'
            sep__ndqd += '      arg0 = arg0[end:]\n'
    ofhx__ixmjy = bodo.string_array_type
    return gen_vectorized(aebq__doun, krzg__eclft, lyl__ibva, sep__ndqd,
        ofhx__ixmjy, prefix_code=brd__jynuo)
