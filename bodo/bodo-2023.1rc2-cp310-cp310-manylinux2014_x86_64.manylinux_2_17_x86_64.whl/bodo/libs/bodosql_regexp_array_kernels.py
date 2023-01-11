"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    eefe__rhe = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for pmpbz__uoc in eefe__rhe:
        pattern = pattern.replace(pmpbz__uoc, eefe__rhe[pmpbz__uoc])
    return pattern


def make_flag_bitvector(flags):
    iev__iptm = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            iev__iptm = iev__iptm | re.I
    if 'm' in flags:
        iev__iptm = iev__iptm | re.M
    if 's' in flags:
        iev__iptm = iev__iptm | re.S
    return iev__iptm


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for ihr__wjbnd in range(4):
        if isinstance(args[ihr__wjbnd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], ihr__wjbnd)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for ihr__wjbnd in range(7):
        if isinstance(args[ihr__wjbnd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], ihr__wjbnd)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for ihr__wjbnd in range(3):
        if isinstance(args[ihr__wjbnd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], ihr__wjbnd)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for ihr__wjbnd in range(6):
        if isinstance(args[ihr__wjbnd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], ihr__wjbnd)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for ihr__wjbnd in range(6):
        if isinstance(args[ihr__wjbnd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                ihr__wjbnd)

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
    rtei__qiul = ['arr', 'pattern', 'position', 'flags']
    mjix__lpht = [arr, pattern, position, flags]
    acff__xlbde = [True] * 4
    hch__dllic = bodo.utils.typing.get_overload_const_str(pattern)
    icyac__mcij = posix_to_re(hch__dllic)
    jzynt__tdb = bodo.utils.typing.get_overload_const_str(flags)
    xoadf__uum = make_flag_bitvector(jzynt__tdb)
    yoqi__csjpv = '\n'
    vrqn__pgscj = ''
    if bodo.utils.utils.is_array_typ(position, True):
        vrqn__pgscj += """if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    else:
        yoqi__csjpv += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if icyac__mcij == '':
        vrqn__pgscj += 'res[i] = 0'
    else:
        yoqi__csjpv += f'r = re.compile({repr(icyac__mcij)}, {xoadf__uum})'
        vrqn__pgscj += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    wfwa__fsliw = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rtei__qiul, mjix__lpht, acff__xlbde, vrqn__pgscj,
        wfwa__fsliw, prefix_code=yoqi__csjpv)


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
    rtei__qiul = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    mjix__lpht = [arr, pattern, position, occurrence, option, flags, group]
    acff__xlbde = [True] * 7
    hch__dllic = bodo.utils.typing.get_overload_const_str(pattern)
    icyac__mcij = posix_to_re(hch__dllic)
    lbu__vqk = re.compile(hch__dllic).groups
    jzynt__tdb = bodo.utils.typing.get_overload_const_str(flags)
    xoadf__uum = make_flag_bitvector(jzynt__tdb)
    yoqi__csjpv = '\n'
    vrqn__pgscj = ''
    if bodo.utils.utils.is_array_typ(position, True):
        vrqn__pgscj += """if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    else:
        yoqi__csjpv += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        vrqn__pgscj += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        yoqi__csjpv += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        vrqn__pgscj += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        yoqi__csjpv += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in jzynt__tdb:
        if bodo.utils.utils.is_array_typ(group, True):
            vrqn__pgscj += f"""if not (1 <= arg6 <= {lbu__vqk}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            yoqi__csjpv += f"""if not (1 <= group <= {lbu__vqk}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if icyac__mcij == '':
        vrqn__pgscj += 'res[i] = 0'
    else:
        yoqi__csjpv += f'r = re.compile({repr(icyac__mcij)}, {xoadf__uum})'
        vrqn__pgscj += 'arg0 = arg0[arg2-1:]\n'
        vrqn__pgscj += 'res[i] = 0\n'
        vrqn__pgscj += 'offset = arg2\n'
        vrqn__pgscj += 'for j in range(arg3):\n'
        vrqn__pgscj += '   match = r.search(arg0)\n'
        vrqn__pgscj += '   if match is None:\n'
        vrqn__pgscj += '      res[i] = 0\n'
        vrqn__pgscj += '      break\n'
        vrqn__pgscj += '   start, end = match.span()\n'
        vrqn__pgscj += '   if j == arg3 - 1:\n'
        if 'e' in jzynt__tdb:
            vrqn__pgscj += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            vrqn__pgscj += '      res[i] = offset + match.span()[arg4]\n'
        vrqn__pgscj += '   else:\n'
        vrqn__pgscj += '      offset += end\n'
        vrqn__pgscj += '      arg0 = arg0[end:]\n'
    wfwa__fsliw = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(rtei__qiul, mjix__lpht, acff__xlbde, vrqn__pgscj,
        wfwa__fsliw, prefix_code=yoqi__csjpv)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    rtei__qiul = ['arr', 'pattern', 'flags']
    mjix__lpht = [arr, pattern, flags]
    acff__xlbde = [True] * 3
    hch__dllic = bodo.utils.typing.get_overload_const_str(pattern)
    icyac__mcij = posix_to_re(hch__dllic)
    jzynt__tdb = bodo.utils.typing.get_overload_const_str(flags)
    xoadf__uum = make_flag_bitvector(jzynt__tdb)
    if icyac__mcij == '':
        yoqi__csjpv = None
        vrqn__pgscj = 'res[i] = len(arg0) == 0'
    else:
        yoqi__csjpv = f'r = re.compile({repr(icyac__mcij)}, {xoadf__uum})'
        vrqn__pgscj = 'if r.fullmatch(arg0) is None:\n'
        vrqn__pgscj += '   res[i] = False\n'
        vrqn__pgscj += 'else:\n'
        vrqn__pgscj += '   res[i] = True\n'
    wfwa__fsliw = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(rtei__qiul, mjix__lpht, acff__xlbde, vrqn__pgscj,
        wfwa__fsliw, prefix_code=yoqi__csjpv)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    rtei__qiul = ['arr', 'pattern', 'replacement', 'position', 'occurrence',
        'flags']
    mjix__lpht = [arr, pattern, replacement, position, occurrence, flags]
    acff__xlbde = [True] * 6
    hch__dllic = bodo.utils.typing.get_overload_const_str(pattern)
    icyac__mcij = posix_to_re(hch__dllic)
    jzynt__tdb = bodo.utils.typing.get_overload_const_str(flags)
    xoadf__uum = make_flag_bitvector(jzynt__tdb)
    yoqi__csjpv = '\n'
    vrqn__pgscj = ''
    if bodo.utils.utils.is_array_typ(position, True):
        vrqn__pgscj += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        yoqi__csjpv += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        vrqn__pgscj += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        yoqi__csjpv += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if icyac__mcij == '':
        vrqn__pgscj += 'res[i] = arg0'
    else:
        yoqi__csjpv += f'r = re.compile({repr(icyac__mcij)}, {xoadf__uum})'
        vrqn__pgscj += 'result = arg0[:arg3-1]\n'
        vrqn__pgscj += 'arg0 = arg0[arg3-1:]\n'
        vrqn__pgscj += 'if arg4 == 0:\n'
        vrqn__pgscj += '   res[i] = result + r.sub(arg2, arg0)\n'
        vrqn__pgscj += 'else:\n'
        vrqn__pgscj += '   nomatch = False\n'
        vrqn__pgscj += '   for j in range(arg4 - 1):\n'
        vrqn__pgscj += '      match = r.search(arg0)\n'
        vrqn__pgscj += '      if match is None:\n'
        vrqn__pgscj += '         res[i] = result + arg0\n'
        vrqn__pgscj += '         nomatch = True\n'
        vrqn__pgscj += '         break\n'
        vrqn__pgscj += '      _, end = match.span()\n'
        vrqn__pgscj += '      result += arg0[:end]\n'
        vrqn__pgscj += '      arg0 = arg0[end:]\n'
        vrqn__pgscj += '   if nomatch == False:\n'
        vrqn__pgscj += '      result += r.sub(arg2, arg0, count=1)\n'
        vrqn__pgscj += '      res[i] = result'
    wfwa__fsliw = bodo.string_array_type
    return gen_vectorized(rtei__qiul, mjix__lpht, acff__xlbde, vrqn__pgscj,
        wfwa__fsliw, prefix_code=yoqi__csjpv)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    rtei__qiul = ['arr', 'pattern', 'position', 'occurrence', 'flags', 'group']
    mjix__lpht = [arr, pattern, position, occurrence, flags, group]
    acff__xlbde = [True] * 6
    hch__dllic = bodo.utils.typing.get_overload_const_str(pattern)
    icyac__mcij = posix_to_re(hch__dllic)
    lbu__vqk = re.compile(hch__dllic).groups
    jzynt__tdb = bodo.utils.typing.get_overload_const_str(flags)
    xoadf__uum = make_flag_bitvector(jzynt__tdb)
    yoqi__csjpv = '\n'
    vrqn__pgscj = ''
    if bodo.utils.utils.is_array_typ(position, True):
        vrqn__pgscj += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        yoqi__csjpv += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        vrqn__pgscj += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        yoqi__csjpv += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in jzynt__tdb:
        if bodo.utils.utils.is_array_typ(group, True):
            vrqn__pgscj += f"""if not (1 <= arg5 <= {lbu__vqk}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            yoqi__csjpv += f"""if not (1 <= group <= {lbu__vqk}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if icyac__mcij == '':
        vrqn__pgscj += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        yoqi__csjpv += f'r = re.compile({repr(icyac__mcij)}, {xoadf__uum})'
        if 'e' in jzynt__tdb:
            vrqn__pgscj += 'matches = r.findall(arg0[arg2-1:])\n'
            vrqn__pgscj += f'if len(matches) < arg3:\n'
            vrqn__pgscj += '   bodo.libs.array_kernels.setna(res, i)\n'
            vrqn__pgscj += 'else:\n'
            if lbu__vqk == 1:
                vrqn__pgscj += '   res[i] = matches[arg3-1]\n'
            else:
                vrqn__pgscj += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            vrqn__pgscj += 'arg0 = str(arg0)[arg2-1:]\n'
            vrqn__pgscj += 'for j in range(arg3):\n'
            vrqn__pgscj += '   match = r.search(arg0)\n'
            vrqn__pgscj += '   if match is None:\n'
            vrqn__pgscj += '      bodo.libs.array_kernels.setna(res, i)\n'
            vrqn__pgscj += '      break\n'
            vrqn__pgscj += '   start, end = match.span()\n'
            vrqn__pgscj += '   if j == arg3 - 1:\n'
            vrqn__pgscj += '      res[i] = arg0[start:end]\n'
            vrqn__pgscj += '   else:\n'
            vrqn__pgscj += '      arg0 = arg0[end:]\n'
    wfwa__fsliw = bodo.string_array_type
    return gen_vectorized(rtei__qiul, mjix__lpht, acff__xlbde, vrqn__pgscj,
        wfwa__fsliw, prefix_code=yoqi__csjpv)
