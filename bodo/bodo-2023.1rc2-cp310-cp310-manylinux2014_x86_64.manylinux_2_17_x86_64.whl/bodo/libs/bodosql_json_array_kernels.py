"""
Implements BodoSQL array kernels related to JSON utilities
"""
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


@numba.generated_jit(nopython=True)
def parse_json(arg):
    if isinstance(arg, types.optional):
        return bodo.libs.bodosql_array_kernel_utils.unopt_argument(
            'bodo.libs.bodosql_array_kernels.parse_json', ['arg'], 0)

    def impl(arg):
        return parse_json_util(arg)
    return impl


@numba.generated_jit(nopython=True)
def parse_single_json_map(s):

    def impl(s):
        txi__kck = 1
        onv__qfkv = {}
        caxg__szx = ['{']
        svtrl__ufm = ''
        qjxe__jhd = ''
        vkwv__mzze = False
        for henir__lbz in s:
            if txi__kck == 1:
                if henir__lbz.isspace():
                    continue
                elif henir__lbz == '{':
                    txi__kck = 2
                else:
                    return None
            elif txi__kck == 2:
                if henir__lbz.isspace():
                    continue
                elif henir__lbz == '"':
                    txi__kck = 3
                elif henir__lbz == '}':
                    txi__kck = 9
                else:
                    return None
            elif txi__kck == 3:
                if vkwv__mzze:
                    svtrl__ufm += henir__lbz
                    vkwv__mzze = False
                elif henir__lbz == '"':
                    txi__kck = 4
                elif henir__lbz == '\\':
                    vkwv__mzze = True
                else:
                    svtrl__ufm += henir__lbz
            elif txi__kck == 4:
                if henir__lbz.isspace():
                    continue
                elif henir__lbz == ':':
                    txi__kck = 5
                else:
                    return None
            elif txi__kck == 5:
                if henir__lbz.isspace():
                    continue
                if henir__lbz in '},]':
                    return None
                else:
                    txi__kck = 7 if henir__lbz == '"' else 6
                    qjxe__jhd += henir__lbz
                    if henir__lbz in '{[':
                        caxg__szx.append(henir__lbz)
            elif txi__kck == 6:
                if henir__lbz.isspace():
                    continue
                if henir__lbz in '{[':
                    qjxe__jhd += henir__lbz
                    caxg__szx.append(henir__lbz)
                elif henir__lbz in '}]':
                    qatdh__hlld = '{' if henir__lbz == '}' else '['
                    if len(caxg__szx) == 0 or caxg__szx[-1] != qatdh__hlld:
                        return None
                    elif len(caxg__szx) == 1:
                        onv__qfkv[svtrl__ufm] = qjxe__jhd
                        svtrl__ufm = ''
                        qjxe__jhd = ''
                        caxg__szx.pop()
                        txi__kck = 9
                    elif len(caxg__szx) == 2:
                        qjxe__jhd += henir__lbz
                        onv__qfkv[svtrl__ufm] = qjxe__jhd
                        svtrl__ufm = ''
                        qjxe__jhd = ''
                        caxg__szx.pop()
                        txi__kck = 8
                    else:
                        qjxe__jhd += henir__lbz
                        caxg__szx.pop()
                elif henir__lbz == '"':
                    qjxe__jhd += henir__lbz
                    txi__kck = 7
                elif henir__lbz == ',':
                    if len(caxg__szx) == 1:
                        onv__qfkv[svtrl__ufm] = qjxe__jhd
                        svtrl__ufm = ''
                        qjxe__jhd = ''
                        txi__kck = 2
                    else:
                        qjxe__jhd += henir__lbz
                else:
                    qjxe__jhd += henir__lbz
            elif txi__kck == 7:
                if vkwv__mzze:
                    qjxe__jhd += henir__lbz
                    vkwv__mzze = False
                elif henir__lbz == '\\':
                    vkwv__mzze = True
                elif henir__lbz == '"':
                    qjxe__jhd += henir__lbz
                    txi__kck = 6
                else:
                    qjxe__jhd += henir__lbz
            elif txi__kck == 8:
                if henir__lbz.isspace():
                    continue
                elif henir__lbz == ',':
                    txi__kck = 2
                elif henir__lbz == '}':
                    txi__kck = 9
                else:
                    return None
            elif txi__kck == 9:
                if not henir__lbz.isspace():
                    return None
        return onv__qfkv if txi__kck == 9 else None
    return impl


@numba.generated_jit(nopython=True)
def parse_json_util(arr):
    bodo.libs.bodosql_array_kernels.verify_string_arg(arr, 'PARSE_JSON', 's')
    obwy__uxt = ['arr']
    tcit__sjid = [arr]
    sreq__rzb = [False]
    yloor__xfvj = """jmap = bodo.libs.bodosql_json_array_kernels.parse_single_json_map(arg0) if arg0 is not None else None
"""
    if bodo.utils.utils.is_array_typ(arr, True):
        dtpy__wwf = (
            'lengths = bodo.utils.utils.alloc_type(n, bodo.int32, (-1,))\n')
        yloor__xfvj += 'res.append(jmap)\n'
        yloor__xfvj += 'if jmap is None:\n'
        yloor__xfvj += '   lengths[i] = 0\n'
        yloor__xfvj += 'else:\n'
        yloor__xfvj += '   lengths[i] = len(jmap)\n'
    else:
        dtpy__wwf = None
        yloor__xfvj += 'return jmap'
    atn__zyv = (
        'res2 = bodo.libs.map_arr_ext.pre_alloc_map_array(n, lengths, out_dtype)\n'
        )
    atn__zyv += 'numba.parfors.parfor.init_prange()\n'
    atn__zyv += 'for i in numba.parfors.parfor.internal_prange(n):\n'
    atn__zyv += '   if res[i] is None:\n'
    atn__zyv += '     bodo.libs.array_kernels.setna(res2, i)\n'
    atn__zyv += '   else:\n'
    atn__zyv += '     res2[i] = res[i]\n'
    atn__zyv += 'res = res2\n'
    xyu__sgo = bodo.StructArrayType((bodo.string_array_type, bodo.
        string_array_type), ('key', 'value'))
    sirkp__fzj = bodo.utils.typing.to_nullable_type(xyu__sgo)
    return gen_vectorized(obwy__uxt, tcit__sjid, sreq__rzb, yloor__xfvj,
        sirkp__fzj, prefix_code=dtpy__wwf, suffix_code=atn__zyv, res_list=
        True, support_dict_encoding=False)
