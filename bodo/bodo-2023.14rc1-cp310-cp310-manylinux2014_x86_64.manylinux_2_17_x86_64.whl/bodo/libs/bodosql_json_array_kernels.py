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
        kyej__jeq = 1
        squmq__xly = {}
        xasj__qioec = ['{']
        czou__zlc = ''
        lnhxx__dzxv = ''
        ebim__oca = False
        for aevyn__cncb in s:
            if kyej__jeq == 1:
                if aevyn__cncb.isspace():
                    continue
                elif aevyn__cncb == '{':
                    kyej__jeq = 2
                else:
                    return None
            elif kyej__jeq == 2:
                if aevyn__cncb.isspace():
                    continue
                elif aevyn__cncb == '"':
                    kyej__jeq = 3
                elif aevyn__cncb == '}':
                    kyej__jeq = 9
                else:
                    return None
            elif kyej__jeq == 3:
                if ebim__oca:
                    czou__zlc += aevyn__cncb
                    ebim__oca = False
                elif aevyn__cncb == '"':
                    kyej__jeq = 4
                elif aevyn__cncb == '\\':
                    ebim__oca = True
                else:
                    czou__zlc += aevyn__cncb
            elif kyej__jeq == 4:
                if aevyn__cncb.isspace():
                    continue
                elif aevyn__cncb == ':':
                    kyej__jeq = 5
                else:
                    return None
            elif kyej__jeq == 5:
                if aevyn__cncb.isspace():
                    continue
                if aevyn__cncb in '},]':
                    return None
                else:
                    kyej__jeq = 7 if aevyn__cncb == '"' else 6
                    lnhxx__dzxv += aevyn__cncb
                    if aevyn__cncb in '{[':
                        xasj__qioec.append(aevyn__cncb)
            elif kyej__jeq == 6:
                if aevyn__cncb.isspace():
                    continue
                if aevyn__cncb in '{[':
                    lnhxx__dzxv += aevyn__cncb
                    xasj__qioec.append(aevyn__cncb)
                elif aevyn__cncb in '}]':
                    kfc__bqzuo = '{' if aevyn__cncb == '}' else '['
                    if len(xasj__qioec) == 0 or xasj__qioec[-1] != kfc__bqzuo:
                        return None
                    elif len(xasj__qioec) == 1:
                        squmq__xly[czou__zlc] = lnhxx__dzxv
                        czou__zlc = ''
                        lnhxx__dzxv = ''
                        xasj__qioec.pop()
                        kyej__jeq = 9
                    elif len(xasj__qioec) == 2:
                        lnhxx__dzxv += aevyn__cncb
                        squmq__xly[czou__zlc] = lnhxx__dzxv
                        czou__zlc = ''
                        lnhxx__dzxv = ''
                        xasj__qioec.pop()
                        kyej__jeq = 8
                    else:
                        lnhxx__dzxv += aevyn__cncb
                        xasj__qioec.pop()
                elif aevyn__cncb == '"':
                    lnhxx__dzxv += aevyn__cncb
                    kyej__jeq = 7
                elif aevyn__cncb == ',':
                    if len(xasj__qioec) == 1:
                        squmq__xly[czou__zlc] = lnhxx__dzxv
                        czou__zlc = ''
                        lnhxx__dzxv = ''
                        kyej__jeq = 2
                    else:
                        lnhxx__dzxv += aevyn__cncb
                else:
                    lnhxx__dzxv += aevyn__cncb
            elif kyej__jeq == 7:
                if ebim__oca:
                    lnhxx__dzxv += aevyn__cncb
                    ebim__oca = False
                elif aevyn__cncb == '\\':
                    ebim__oca = True
                elif aevyn__cncb == '"':
                    lnhxx__dzxv += aevyn__cncb
                    kyej__jeq = 6
                else:
                    lnhxx__dzxv += aevyn__cncb
            elif kyej__jeq == 8:
                if aevyn__cncb.isspace():
                    continue
                elif aevyn__cncb == ',':
                    kyej__jeq = 2
                elif aevyn__cncb == '}':
                    kyej__jeq = 9
                else:
                    return None
            elif kyej__jeq == 9:
                if not aevyn__cncb.isspace():
                    return None
        return squmq__xly if kyej__jeq == 9 else None
    return impl


@numba.generated_jit(nopython=True)
def parse_json_util(arr):
    bodo.libs.bodosql_array_kernels.verify_string_arg(arr, 'PARSE_JSON', 's')
    qkg__ibtm = ['arr']
    cjf__ldlq = [arr]
    egdro__ocncs = [False]
    gnhog__bbzht = """jmap = bodo.libs.bodosql_json_array_kernels.parse_single_json_map(arg0) if arg0 is not None else None
"""
    if bodo.utils.utils.is_array_typ(arr, True):
        woho__nrjsh = (
            'lengths = bodo.utils.utils.alloc_type(n, bodo.int32, (-1,))\n')
        gnhog__bbzht += 'res.append(jmap)\n'
        gnhog__bbzht += 'if jmap is None:\n'
        gnhog__bbzht += '   lengths[i] = 0\n'
        gnhog__bbzht += 'else:\n'
        gnhog__bbzht += '   lengths[i] = len(jmap)\n'
    else:
        woho__nrjsh = None
        gnhog__bbzht += 'return jmap'
    cbhjp__trfla = (
        'res2 = bodo.libs.map_arr_ext.pre_alloc_map_array(n, lengths, out_dtype)\n'
        )
    cbhjp__trfla += 'numba.parfors.parfor.init_prange()\n'
    cbhjp__trfla += 'for i in numba.parfors.parfor.internal_prange(n):\n'
    cbhjp__trfla += '   if res[i] is None:\n'
    cbhjp__trfla += '     bodo.libs.array_kernels.setna(res2, i)\n'
    cbhjp__trfla += '   else:\n'
    cbhjp__trfla += '     res2[i] = res[i]\n'
    cbhjp__trfla += 'res = res2\n'
    zmsj__yiw = bodo.StructArrayType((bodo.string_array_type, bodo.
        string_array_type), ('key', 'value'))
    vvqnr__ixtbv = bodo.utils.typing.to_nullable_type(zmsj__yiw)
    return gen_vectorized(qkg__ibtm, cjf__ldlq, egdro__ocncs, gnhog__bbzht,
        vvqnr__ixtbv, prefix_code=woho__nrjsh, suffix_code=cbhjp__trfla,
        res_list=True, support_dict_encoding=False)
