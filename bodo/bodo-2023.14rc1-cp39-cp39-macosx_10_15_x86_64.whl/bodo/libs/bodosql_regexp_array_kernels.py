"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    oqd__xgiy = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for hkwpr__dyc in oqd__xgiy:
        pattern = pattern.replace(hkwpr__dyc, oqd__xgiy[hkwpr__dyc])
    return pattern


def make_flag_bitvector(flags):
    dxm__enjfo = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            dxm__enjfo = dxm__enjfo | re.I
    if 'm' in flags:
        dxm__enjfo = dxm__enjfo | re.M
    if 's' in flags:
        dxm__enjfo = dxm__enjfo | re.S
    return dxm__enjfo


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for uyw__gcaw in range(4):
        if isinstance(args[uyw__gcaw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], uyw__gcaw)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for uyw__gcaw in range(7):
        if isinstance(args[uyw__gcaw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], uyw__gcaw)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for uyw__gcaw in range(3):
        if isinstance(args[uyw__gcaw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], uyw__gcaw)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for uyw__gcaw in range(6):
        if isinstance(args[uyw__gcaw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], uyw__gcaw)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for uyw__gcaw in range(6):
        if isinstance(args[uyw__gcaw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                uyw__gcaw)

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
    hmz__wgixg = ['arr', 'pattern', 'position', 'flags']
    ztnb__kovd = [arr, pattern, position, flags]
    fqp__icbj = [True] * 4
    yvjgl__bwk = bodo.utils.typing.get_overload_const_str(pattern)
    noep__vbaz = posix_to_re(yvjgl__bwk)
    rpd__spoj = bodo.utils.typing.get_overload_const_str(flags)
    bbhw__ajwor = make_flag_bitvector(rpd__spoj)
    muu__rendy = '\n'
    nwcx__jkoih = ''
    if bodo.utils.utils.is_array_typ(position, True):
        nwcx__jkoih += """if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    else:
        muu__rendy += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if noep__vbaz == '':
        nwcx__jkoih += 'res[i] = 0'
    else:
        muu__rendy += f'r = re.compile({repr(noep__vbaz)}, {bbhw__ajwor})'
        nwcx__jkoih += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    yiwq__tnhph = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(hmz__wgixg, ztnb__kovd, fqp__icbj, nwcx__jkoih,
        yiwq__tnhph, prefix_code=muu__rendy)


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
    hmz__wgixg = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    ztnb__kovd = [arr, pattern, position, occurrence, option, flags, group]
    fqp__icbj = [True] * 7
    yvjgl__bwk = bodo.utils.typing.get_overload_const_str(pattern)
    noep__vbaz = posix_to_re(yvjgl__bwk)
    zqxkl__cozdz = re.compile(yvjgl__bwk).groups
    rpd__spoj = bodo.utils.typing.get_overload_const_str(flags)
    bbhw__ajwor = make_flag_bitvector(rpd__spoj)
    muu__rendy = '\n'
    nwcx__jkoih = ''
    if bodo.utils.utils.is_array_typ(position, True):
        nwcx__jkoih += """if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    else:
        muu__rendy += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        nwcx__jkoih += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        muu__rendy += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        nwcx__jkoih += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        muu__rendy += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in rpd__spoj:
        if bodo.utils.utils.is_array_typ(group, True):
            nwcx__jkoih += f"""if not (1 <= arg6 <= {zqxkl__cozdz}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            muu__rendy += f"""if not (1 <= group <= {zqxkl__cozdz}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if noep__vbaz == '':
        nwcx__jkoih += 'res[i] = 0'
    else:
        muu__rendy += f'r = re.compile({repr(noep__vbaz)}, {bbhw__ajwor})'
        nwcx__jkoih += 'arg0 = arg0[arg2-1:]\n'
        nwcx__jkoih += 'res[i] = 0\n'
        nwcx__jkoih += 'offset = arg2\n'
        nwcx__jkoih += 'for j in range(arg3):\n'
        nwcx__jkoih += '   match = r.search(arg0)\n'
        nwcx__jkoih += '   if match is None:\n'
        nwcx__jkoih += '      res[i] = 0\n'
        nwcx__jkoih += '      break\n'
        nwcx__jkoih += '   start, end = match.span()\n'
        nwcx__jkoih += '   if j == arg3 - 1:\n'
        if 'e' in rpd__spoj:
            nwcx__jkoih += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            nwcx__jkoih += '      res[i] = offset + match.span()[arg4]\n'
        nwcx__jkoih += '   else:\n'
        nwcx__jkoih += '      offset += end\n'
        nwcx__jkoih += '      arg0 = arg0[end:]\n'
    yiwq__tnhph = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(hmz__wgixg, ztnb__kovd, fqp__icbj, nwcx__jkoih,
        yiwq__tnhph, prefix_code=muu__rendy)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    hmz__wgixg = ['arr', 'pattern', 'flags']
    ztnb__kovd = [arr, pattern, flags]
    fqp__icbj = [True] * 3
    yvjgl__bwk = bodo.utils.typing.get_overload_const_str(pattern)
    noep__vbaz = posix_to_re(yvjgl__bwk)
    rpd__spoj = bodo.utils.typing.get_overload_const_str(flags)
    bbhw__ajwor = make_flag_bitvector(rpd__spoj)
    if noep__vbaz == '':
        muu__rendy = None
        nwcx__jkoih = 'res[i] = len(arg0) == 0'
    else:
        muu__rendy = f'r = re.compile({repr(noep__vbaz)}, {bbhw__ajwor})'
        nwcx__jkoih = 'if r.fullmatch(arg0) is None:\n'
        nwcx__jkoih += '   res[i] = False\n'
        nwcx__jkoih += 'else:\n'
        nwcx__jkoih += '   res[i] = True\n'
    yiwq__tnhph = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(hmz__wgixg, ztnb__kovd, fqp__icbj, nwcx__jkoih,
        yiwq__tnhph, prefix_code=muu__rendy)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    hmz__wgixg = ['arr', 'pattern', 'replacement', 'position', 'occurrence',
        'flags']
    ztnb__kovd = [arr, pattern, replacement, position, occurrence, flags]
    fqp__icbj = [True] * 6
    yvjgl__bwk = bodo.utils.typing.get_overload_const_str(pattern)
    noep__vbaz = posix_to_re(yvjgl__bwk)
    rpd__spoj = bodo.utils.typing.get_overload_const_str(flags)
    bbhw__ajwor = make_flag_bitvector(rpd__spoj)
    muu__rendy = '\n'
    nwcx__jkoih = ''
    if bodo.utils.utils.is_array_typ(position, True):
        nwcx__jkoih += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        muu__rendy += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        nwcx__jkoih += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        muu__rendy += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if noep__vbaz == '':
        nwcx__jkoih += 'res[i] = arg0'
    else:
        muu__rendy += f'r = re.compile({repr(noep__vbaz)}, {bbhw__ajwor})'
        nwcx__jkoih += 'result = arg0[:arg3-1]\n'
        nwcx__jkoih += 'arg0 = arg0[arg3-1:]\n'
        nwcx__jkoih += 'if arg4 == 0:\n'
        nwcx__jkoih += '   res[i] = result + r.sub(arg2, arg0)\n'
        nwcx__jkoih += 'else:\n'
        nwcx__jkoih += '   nomatch = False\n'
        nwcx__jkoih += '   for j in range(arg4 - 1):\n'
        nwcx__jkoih += '      match = r.search(arg0)\n'
        nwcx__jkoih += '      if match is None:\n'
        nwcx__jkoih += '         res[i] = result + arg0\n'
        nwcx__jkoih += '         nomatch = True\n'
        nwcx__jkoih += '         break\n'
        nwcx__jkoih += '      _, end = match.span()\n'
        nwcx__jkoih += '      result += arg0[:end]\n'
        nwcx__jkoih += '      arg0 = arg0[end:]\n'
        nwcx__jkoih += '   if nomatch == False:\n'
        nwcx__jkoih += '      result += r.sub(arg2, arg0, count=1)\n'
        nwcx__jkoih += '      res[i] = result'
    yiwq__tnhph = bodo.string_array_type
    return gen_vectorized(hmz__wgixg, ztnb__kovd, fqp__icbj, nwcx__jkoih,
        yiwq__tnhph, prefix_code=muu__rendy)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    hmz__wgixg = ['arr', 'pattern', 'position', 'occurrence', 'flags', 'group']
    ztnb__kovd = [arr, pattern, position, occurrence, flags, group]
    fqp__icbj = [True] * 6
    yvjgl__bwk = bodo.utils.typing.get_overload_const_str(pattern)
    noep__vbaz = posix_to_re(yvjgl__bwk)
    zqxkl__cozdz = re.compile(yvjgl__bwk).groups
    rpd__spoj = bodo.utils.typing.get_overload_const_str(flags)
    bbhw__ajwor = make_flag_bitvector(rpd__spoj)
    muu__rendy = '\n'
    nwcx__jkoih = ''
    if bodo.utils.utils.is_array_typ(position, True):
        nwcx__jkoih += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        muu__rendy += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        nwcx__jkoih += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        muu__rendy += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in rpd__spoj:
        if bodo.utils.utils.is_array_typ(group, True):
            nwcx__jkoih += f"""if not (1 <= arg5 <= {zqxkl__cozdz}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            muu__rendy += f"""if not (1 <= group <= {zqxkl__cozdz}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if noep__vbaz == '':
        nwcx__jkoih += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        muu__rendy += f'r = re.compile({repr(noep__vbaz)}, {bbhw__ajwor})'
        if 'e' in rpd__spoj:
            nwcx__jkoih += 'matches = r.findall(arg0[arg2-1:])\n'
            nwcx__jkoih += f'if len(matches) < arg3:\n'
            nwcx__jkoih += '   bodo.libs.array_kernels.setna(res, i)\n'
            nwcx__jkoih += 'else:\n'
            if zqxkl__cozdz == 1:
                nwcx__jkoih += '   res[i] = matches[arg3-1]\n'
            else:
                nwcx__jkoih += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            nwcx__jkoih += 'arg0 = str(arg0)[arg2-1:]\n'
            nwcx__jkoih += 'for j in range(arg3):\n'
            nwcx__jkoih += '   match = r.search(arg0)\n'
            nwcx__jkoih += '   if match is None:\n'
            nwcx__jkoih += '      bodo.libs.array_kernels.setna(res, i)\n'
            nwcx__jkoih += '      break\n'
            nwcx__jkoih += '   start, end = match.span()\n'
            nwcx__jkoih += '   if j == arg3 - 1:\n'
            nwcx__jkoih += '      res[i] = arg0[start:end]\n'
            nwcx__jkoih += '   else:\n'
            nwcx__jkoih += '      arg0 = arg0[end:]\n'
    yiwq__tnhph = bodo.string_array_type
    return gen_vectorized(hmz__wgixg, ztnb__kovd, fqp__icbj, nwcx__jkoih,
        yiwq__tnhph, prefix_code=muu__rendy)
