"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    hnof__ruzc = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for xyqc__vzr in hnof__ruzc:
        pattern = pattern.replace(xyqc__vzr, hnof__ruzc[xyqc__vzr])
    return pattern


def make_flag_bitvector(flags):
    ozrav__ivfoz = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            ozrav__ivfoz = ozrav__ivfoz | re.I
    if 'm' in flags:
        ozrav__ivfoz = ozrav__ivfoz | re.M
    if 's' in flags:
        ozrav__ivfoz = ozrav__ivfoz | re.S
    return ozrav__ivfoz


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for aoh__yxneq in range(4):
        if isinstance(args[aoh__yxneq], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], aoh__yxneq)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for aoh__yxneq in range(7):
        if isinstance(args[aoh__yxneq], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], aoh__yxneq)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for aoh__yxneq in range(3):
        if isinstance(args[aoh__yxneq], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], aoh__yxneq)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for aoh__yxneq in range(6):
        if isinstance(args[aoh__yxneq], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], aoh__yxneq)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for aoh__yxneq in range(6):
        if isinstance(args[aoh__yxneq], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                aoh__yxneq)

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
    ztv__msgb = ['arr', 'pattern', 'position', 'flags']
    oqems__idhsi = [arr, pattern, position, flags]
    ebk__zxi = [True] * 4
    htmvi__uca = bodo.utils.typing.get_overload_const_str(pattern)
    ibqwf__qyc = posix_to_re(htmvi__uca)
    quby__bhaba = bodo.utils.typing.get_overload_const_str(flags)
    qutr__jgz = make_flag_bitvector(quby__bhaba)
    pxebx__csc = '\n'
    giq__rdy = ''
    if bodo.utils.utils.is_array_typ(position, True):
        giq__rdy += (
            "if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')\n"
            )
    else:
        pxebx__csc += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if ibqwf__qyc == '':
        giq__rdy += 'res[i] = 0'
    else:
        pxebx__csc += f'r = re.compile({repr(ibqwf__qyc)}, {qutr__jgz})'
        giq__rdy += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    vvob__nzom = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(ztv__msgb, oqems__idhsi, ebk__zxi, giq__rdy,
        vvob__nzom, prefix_code=pxebx__csc)


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
    ztv__msgb = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    oqems__idhsi = [arr, pattern, position, occurrence, option, flags, group]
    ebk__zxi = [True] * 7
    htmvi__uca = bodo.utils.typing.get_overload_const_str(pattern)
    ibqwf__qyc = posix_to_re(htmvi__uca)
    iczww__cfpcc = re.compile(htmvi__uca).groups
    quby__bhaba = bodo.utils.typing.get_overload_const_str(flags)
    qutr__jgz = make_flag_bitvector(quby__bhaba)
    pxebx__csc = '\n'
    giq__rdy = ''
    if bodo.utils.utils.is_array_typ(position, True):
        giq__rdy += (
            "if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')\n"
            )
    else:
        pxebx__csc += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        giq__rdy += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        pxebx__csc += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        giq__rdy += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        pxebx__csc += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in quby__bhaba:
        if bodo.utils.utils.is_array_typ(group, True):
            giq__rdy += f"""if not (1 <= arg6 <= {iczww__cfpcc}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            pxebx__csc += f"""if not (1 <= group <= {iczww__cfpcc}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if ibqwf__qyc == '':
        giq__rdy += 'res[i] = 0'
    else:
        pxebx__csc += f'r = re.compile({repr(ibqwf__qyc)}, {qutr__jgz})'
        giq__rdy += 'arg0 = arg0[arg2-1:]\n'
        giq__rdy += 'res[i] = 0\n'
        giq__rdy += 'offset = arg2\n'
        giq__rdy += 'for j in range(arg3):\n'
        giq__rdy += '   match = r.search(arg0)\n'
        giq__rdy += '   if match is None:\n'
        giq__rdy += '      res[i] = 0\n'
        giq__rdy += '      break\n'
        giq__rdy += '   start, end = match.span()\n'
        giq__rdy += '   if j == arg3 - 1:\n'
        if 'e' in quby__bhaba:
            giq__rdy += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            giq__rdy += '      res[i] = offset + match.span()[arg4]\n'
        giq__rdy += '   else:\n'
        giq__rdy += '      offset += end\n'
        giq__rdy += '      arg0 = arg0[end:]\n'
    vvob__nzom = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(ztv__msgb, oqems__idhsi, ebk__zxi, giq__rdy,
        vvob__nzom, prefix_code=pxebx__csc)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    ztv__msgb = ['arr', 'pattern', 'flags']
    oqems__idhsi = [arr, pattern, flags]
    ebk__zxi = [True] * 3
    htmvi__uca = bodo.utils.typing.get_overload_const_str(pattern)
    ibqwf__qyc = posix_to_re(htmvi__uca)
    quby__bhaba = bodo.utils.typing.get_overload_const_str(flags)
    qutr__jgz = make_flag_bitvector(quby__bhaba)
    if ibqwf__qyc == '':
        pxebx__csc = None
        giq__rdy = 'res[i] = len(arg0) == 0'
    else:
        pxebx__csc = f'r = re.compile({repr(ibqwf__qyc)}, {qutr__jgz})'
        giq__rdy = 'if r.fullmatch(arg0) is None:\n'
        giq__rdy += '   res[i] = False\n'
        giq__rdy += 'else:\n'
        giq__rdy += '   res[i] = True\n'
    vvob__nzom = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(ztv__msgb, oqems__idhsi, ebk__zxi, giq__rdy,
        vvob__nzom, prefix_code=pxebx__csc)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    ztv__msgb = ['arr', 'pattern', 'replacement', 'position', 'occurrence',
        'flags']
    oqems__idhsi = [arr, pattern, replacement, position, occurrence, flags]
    ebk__zxi = [True] * 6
    htmvi__uca = bodo.utils.typing.get_overload_const_str(pattern)
    ibqwf__qyc = posix_to_re(htmvi__uca)
    quby__bhaba = bodo.utils.typing.get_overload_const_str(flags)
    qutr__jgz = make_flag_bitvector(quby__bhaba)
    pxebx__csc = '\n'
    giq__rdy = ''
    if bodo.utils.utils.is_array_typ(position, True):
        giq__rdy += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        pxebx__csc += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        giq__rdy += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        pxebx__csc += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if ibqwf__qyc == '':
        giq__rdy += 'res[i] = arg0'
    else:
        pxebx__csc += f'r = re.compile({repr(ibqwf__qyc)}, {qutr__jgz})'
        giq__rdy += 'result = arg0[:arg3-1]\n'
        giq__rdy += 'arg0 = arg0[arg3-1:]\n'
        giq__rdy += 'if arg4 == 0:\n'
        giq__rdy += '   res[i] = result + r.sub(arg2, arg0)\n'
        giq__rdy += 'else:\n'
        giq__rdy += '   nomatch = False\n'
        giq__rdy += '   for j in range(arg4 - 1):\n'
        giq__rdy += '      match = r.search(arg0)\n'
        giq__rdy += '      if match is None:\n'
        giq__rdy += '         res[i] = result + arg0\n'
        giq__rdy += '         nomatch = True\n'
        giq__rdy += '         break\n'
        giq__rdy += '      _, end = match.span()\n'
        giq__rdy += '      result += arg0[:end]\n'
        giq__rdy += '      arg0 = arg0[end:]\n'
        giq__rdy += '   if nomatch == False:\n'
        giq__rdy += '      result += r.sub(arg2, arg0, count=1)\n'
        giq__rdy += '      res[i] = result'
    vvob__nzom = bodo.string_array_type
    return gen_vectorized(ztv__msgb, oqems__idhsi, ebk__zxi, giq__rdy,
        vvob__nzom, prefix_code=pxebx__csc)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    ztv__msgb = ['arr', 'pattern', 'position', 'occurrence', 'flags', 'group']
    oqems__idhsi = [arr, pattern, position, occurrence, flags, group]
    ebk__zxi = [True] * 6
    htmvi__uca = bodo.utils.typing.get_overload_const_str(pattern)
    ibqwf__qyc = posix_to_re(htmvi__uca)
    iczww__cfpcc = re.compile(htmvi__uca).groups
    quby__bhaba = bodo.utils.typing.get_overload_const_str(flags)
    qutr__jgz = make_flag_bitvector(quby__bhaba)
    pxebx__csc = '\n'
    giq__rdy = ''
    if bodo.utils.utils.is_array_typ(position, True):
        giq__rdy += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        pxebx__csc += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        giq__rdy += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        pxebx__csc += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in quby__bhaba:
        if bodo.utils.utils.is_array_typ(group, True):
            giq__rdy += f"""if not (1 <= arg5 <= {iczww__cfpcc}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            pxebx__csc += f"""if not (1 <= group <= {iczww__cfpcc}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if ibqwf__qyc == '':
        giq__rdy += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        pxebx__csc += f'r = re.compile({repr(ibqwf__qyc)}, {qutr__jgz})'
        if 'e' in quby__bhaba:
            giq__rdy += 'matches = r.findall(arg0[arg2-1:])\n'
            giq__rdy += f'if len(matches) < arg3:\n'
            giq__rdy += '   bodo.libs.array_kernels.setna(res, i)\n'
            giq__rdy += 'else:\n'
            if iczww__cfpcc == 1:
                giq__rdy += '   res[i] = matches[arg3-1]\n'
            else:
                giq__rdy += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            giq__rdy += 'arg0 = str(arg0)[arg2-1:]\n'
            giq__rdy += 'for j in range(arg3):\n'
            giq__rdy += '   match = r.search(arg0)\n'
            giq__rdy += '   if match is None:\n'
            giq__rdy += '      bodo.libs.array_kernels.setna(res, i)\n'
            giq__rdy += '      break\n'
            giq__rdy += '   start, end = match.span()\n'
            giq__rdy += '   if j == arg3 - 1:\n'
            giq__rdy += '      res[i] = arg0[start:end]\n'
            giq__rdy += '   else:\n'
            giq__rdy += '      arg0 = arg0[end:]\n'
    vvob__nzom = bodo.string_array_type
    return gen_vectorized(ztv__msgb, oqems__idhsi, ebk__zxi, giq__rdy,
        vvob__nzom, prefix_code=pxebx__csc)
