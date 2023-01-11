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
        hyrj__vcycx = 1
        lsb__cmzk = {}
        gss__yymhf = ['{']
        xahu__iip = ''
        ule__uutx = ''
        cznv__vrgv = False
        for qzdvy__uha in s:
            if hyrj__vcycx == 1:
                if qzdvy__uha.isspace():
                    continue
                elif qzdvy__uha == '{':
                    hyrj__vcycx = 2
                else:
                    return None
            elif hyrj__vcycx == 2:
                if qzdvy__uha.isspace():
                    continue
                elif qzdvy__uha == '"':
                    hyrj__vcycx = 3
                elif qzdvy__uha == '}':
                    hyrj__vcycx = 9
                else:
                    return None
            elif hyrj__vcycx == 3:
                if cznv__vrgv:
                    xahu__iip += qzdvy__uha
                    cznv__vrgv = False
                elif qzdvy__uha == '"':
                    hyrj__vcycx = 4
                elif qzdvy__uha == '\\':
                    cznv__vrgv = True
                else:
                    xahu__iip += qzdvy__uha
            elif hyrj__vcycx == 4:
                if qzdvy__uha.isspace():
                    continue
                elif qzdvy__uha == ':':
                    hyrj__vcycx = 5
                else:
                    return None
            elif hyrj__vcycx == 5:
                if qzdvy__uha.isspace():
                    continue
                if qzdvy__uha in '},]':
                    return None
                else:
                    hyrj__vcycx = 7 if qzdvy__uha == '"' else 6
                    ule__uutx += qzdvy__uha
                    if qzdvy__uha in '{[':
                        gss__yymhf.append(qzdvy__uha)
            elif hyrj__vcycx == 6:
                if qzdvy__uha.isspace():
                    continue
                if qzdvy__uha in '{[':
                    ule__uutx += qzdvy__uha
                    gss__yymhf.append(qzdvy__uha)
                elif qzdvy__uha in '}]':
                    uovrs__xsarl = '{' if qzdvy__uha == '}' else '['
                    if len(gss__yymhf) == 0 or gss__yymhf[-1] != uovrs__xsarl:
                        return None
                    elif len(gss__yymhf) == 1:
                        lsb__cmzk[xahu__iip] = ule__uutx
                        xahu__iip = ''
                        ule__uutx = ''
                        gss__yymhf.pop()
                        hyrj__vcycx = 9
                    elif len(gss__yymhf) == 2:
                        ule__uutx += qzdvy__uha
                        lsb__cmzk[xahu__iip] = ule__uutx
                        xahu__iip = ''
                        ule__uutx = ''
                        gss__yymhf.pop()
                        hyrj__vcycx = 8
                    else:
                        ule__uutx += qzdvy__uha
                        gss__yymhf.pop()
                elif qzdvy__uha == '"':
                    ule__uutx += qzdvy__uha
                    hyrj__vcycx = 7
                elif qzdvy__uha == ',':
                    if len(gss__yymhf) == 1:
                        lsb__cmzk[xahu__iip] = ule__uutx
                        xahu__iip = ''
                        ule__uutx = ''
                        hyrj__vcycx = 2
                    else:
                        ule__uutx += qzdvy__uha
                else:
                    ule__uutx += qzdvy__uha
            elif hyrj__vcycx == 7:
                if cznv__vrgv:
                    ule__uutx += qzdvy__uha
                    cznv__vrgv = False
                elif qzdvy__uha == '\\':
                    cznv__vrgv = True
                elif qzdvy__uha == '"':
                    ule__uutx += qzdvy__uha
                    hyrj__vcycx = 6
                else:
                    ule__uutx += qzdvy__uha
            elif hyrj__vcycx == 8:
                if qzdvy__uha.isspace():
                    continue
                elif qzdvy__uha == ',':
                    hyrj__vcycx = 2
                elif qzdvy__uha == '}':
                    hyrj__vcycx = 9
                else:
                    return None
            elif hyrj__vcycx == 9:
                if not qzdvy__uha.isspace():
                    return None
        return lsb__cmzk if hyrj__vcycx == 9 else None
    return impl


@numba.generated_jit(nopython=True)
def parse_json_util(arr):
    bodo.libs.bodosql_array_kernels.verify_string_arg(arr, 'PARSE_JSON', 's')
    gjhg__lbrpj = ['arr']
    hfzwg__zmhtv = [arr]
    azm__ttgad = [False]
    mzm__pfkuy = """jmap = bodo.libs.bodosql_json_array_kernels.parse_single_json_map(arg0) if arg0 is not None else None
"""
    if bodo.utils.utils.is_array_typ(arr, True):
        rdlo__xbqa = (
            'lengths = bodo.utils.utils.alloc_type(n, bodo.int32, (-1,))\n')
        mzm__pfkuy += 'res.append(jmap)\n'
        mzm__pfkuy += 'if jmap is None:\n'
        mzm__pfkuy += '   lengths[i] = 0\n'
        mzm__pfkuy += 'else:\n'
        mzm__pfkuy += '   lengths[i] = len(jmap)\n'
    else:
        rdlo__xbqa = None
        mzm__pfkuy += 'return jmap'
    hayxq__ejba = (
        'res2 = bodo.libs.map_arr_ext.pre_alloc_map_array(n, lengths, out_dtype)\n'
        )
    hayxq__ejba += 'numba.parfors.parfor.init_prange()\n'
    hayxq__ejba += 'for i in numba.parfors.parfor.internal_prange(n):\n'
    hayxq__ejba += '   if res[i] is None:\n'
    hayxq__ejba += '     bodo.libs.array_kernels.setna(res2, i)\n'
    hayxq__ejba += '   else:\n'
    hayxq__ejba += '     res2[i] = res[i]\n'
    hayxq__ejba += 'res = res2\n'
    fnmkq__qng = bodo.StructArrayType((bodo.string_array_type, bodo.
        string_array_type), ('key', 'value'))
    eqw__lpv = bodo.utils.typing.to_nullable_type(fnmkq__qng)
    return gen_vectorized(gjhg__lbrpj, hfzwg__zmhtv, azm__ttgad, mzm__pfkuy,
        eqw__lpv, prefix_code=rdlo__xbqa, suffix_code=hayxq__ejba, res_list
        =True, support_dict_encoding=False)
