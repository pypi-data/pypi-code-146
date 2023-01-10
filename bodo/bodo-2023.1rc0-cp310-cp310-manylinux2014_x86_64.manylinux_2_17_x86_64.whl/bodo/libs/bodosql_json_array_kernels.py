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
        ktg__inw = 1
        afh__sjpb = {}
        kxr__epyq = ['{']
        qwv__nqmei = ''
        nfafp__ybb = ''
        zhr__nif = False
        for ewmi__phn in s:
            if ktg__inw == 1:
                if ewmi__phn.isspace():
                    continue
                elif ewmi__phn == '{':
                    ktg__inw = 2
                else:
                    return None
            elif ktg__inw == 2:
                if ewmi__phn.isspace():
                    continue
                elif ewmi__phn == '"':
                    ktg__inw = 3
                elif ewmi__phn == '}':
                    ktg__inw = 9
                else:
                    return None
            elif ktg__inw == 3:
                if zhr__nif:
                    qwv__nqmei += ewmi__phn
                    zhr__nif = False
                elif ewmi__phn == '"':
                    ktg__inw = 4
                elif ewmi__phn == '\\':
                    zhr__nif = True
                else:
                    qwv__nqmei += ewmi__phn
            elif ktg__inw == 4:
                if ewmi__phn.isspace():
                    continue
                elif ewmi__phn == ':':
                    ktg__inw = 5
                else:
                    return None
            elif ktg__inw == 5:
                if ewmi__phn.isspace():
                    continue
                if ewmi__phn in '},]':
                    return None
                else:
                    ktg__inw = 7 if ewmi__phn == '"' else 6
                    nfafp__ybb += ewmi__phn
                    if ewmi__phn in '{[':
                        kxr__epyq.append(ewmi__phn)
            elif ktg__inw == 6:
                if ewmi__phn.isspace():
                    continue
                if ewmi__phn in '{[':
                    nfafp__ybb += ewmi__phn
                    kxr__epyq.append(ewmi__phn)
                elif ewmi__phn in '}]':
                    prit__ejt = '{' if ewmi__phn == '}' else '['
                    if len(kxr__epyq) == 0 or kxr__epyq[-1] != prit__ejt:
                        return None
                    elif len(kxr__epyq) == 1:
                        afh__sjpb[qwv__nqmei] = nfafp__ybb
                        qwv__nqmei = ''
                        nfafp__ybb = ''
                        kxr__epyq.pop()
                        ktg__inw = 9
                    elif len(kxr__epyq) == 2:
                        nfafp__ybb += ewmi__phn
                        afh__sjpb[qwv__nqmei] = nfafp__ybb
                        qwv__nqmei = ''
                        nfafp__ybb = ''
                        kxr__epyq.pop()
                        ktg__inw = 8
                    else:
                        nfafp__ybb += ewmi__phn
                        kxr__epyq.pop()
                elif ewmi__phn == '"':
                    nfafp__ybb += ewmi__phn
                    ktg__inw = 7
                elif ewmi__phn == ',':
                    if len(kxr__epyq) == 1:
                        afh__sjpb[qwv__nqmei] = nfafp__ybb
                        qwv__nqmei = ''
                        nfafp__ybb = ''
                        ktg__inw = 2
                    else:
                        nfafp__ybb += ewmi__phn
                else:
                    nfafp__ybb += ewmi__phn
            elif ktg__inw == 7:
                if zhr__nif:
                    nfafp__ybb += ewmi__phn
                    zhr__nif = False
                elif ewmi__phn == '\\':
                    zhr__nif = True
                elif ewmi__phn == '"':
                    nfafp__ybb += ewmi__phn
                    ktg__inw = 6
                else:
                    nfafp__ybb += ewmi__phn
            elif ktg__inw == 8:
                if ewmi__phn.isspace():
                    continue
                elif ewmi__phn == ',':
                    ktg__inw = 2
                elif ewmi__phn == '}':
                    ktg__inw = 9
                else:
                    return None
            elif ktg__inw == 9:
                if not ewmi__phn.isspace():
                    return None
        return afh__sjpb if ktg__inw == 9 else None
    return impl


@numba.generated_jit(nopython=True)
def parse_json_util(arr):
    bodo.libs.bodosql_array_kernels.verify_string_arg(arr, 'PARSE_JSON', 's')
    dwc__ndeuw = ['arr']
    wlo__pvcl = [arr]
    dyoh__qrhh = [False]
    gmzu__zgwch = """jmap = bodo.libs.bodosql_json_array_kernels.parse_single_json_map(arg0) if arg0 is not None else None
"""
    if bodo.utils.utils.is_array_typ(arr, True):
        jmkbp__kcmkf = (
            'lengths = bodo.utils.utils.alloc_type(n, bodo.int32, (-1,))\n')
        gmzu__zgwch += 'res.append(jmap)\n'
        gmzu__zgwch += 'if jmap is None:\n'
        gmzu__zgwch += '   lengths[i] = 0\n'
        gmzu__zgwch += 'else:\n'
        gmzu__zgwch += '   lengths[i] = len(jmap)\n'
    else:
        jmkbp__kcmkf = None
        gmzu__zgwch += 'return jmap'
    zjvv__jquc = (
        'res2 = bodo.libs.map_arr_ext.pre_alloc_map_array(n, lengths, out_dtype)\n'
        )
    zjvv__jquc += 'numba.parfors.parfor.init_prange()\n'
    zjvv__jquc += 'for i in numba.parfors.parfor.internal_prange(n):\n'
    zjvv__jquc += '   if res[i] is None:\n'
    zjvv__jquc += '     bodo.libs.array_kernels.setna(res2, i)\n'
    zjvv__jquc += '   else:\n'
    zjvv__jquc += '     res2[i] = res[i]\n'
    zjvv__jquc += 'res = res2\n'
    krjwa__bmajy = bodo.StructArrayType((bodo.string_array_type, bodo.
        string_array_type), ('key', 'value'))
    asvzz__buap = bodo.utils.typing.to_nullable_type(krjwa__bmajy)
    return gen_vectorized(dwc__ndeuw, wlo__pvcl, dyoh__qrhh, gmzu__zgwch,
        asvzz__buap, prefix_code=jmkbp__kcmkf, suffix_code=zjvv__jquc,
        res_list=True, support_dict_encoding=False)
