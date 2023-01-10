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
        apxac__gdhhj = 1
        cehv__bxrv = {}
        sgxo__gok = ['{']
        oqlr__qpd = ''
        dxj__jtthu = ''
        fgf__bte = False
        for ydsv__xvrh in s:
            if apxac__gdhhj == 1:
                if ydsv__xvrh.isspace():
                    continue
                elif ydsv__xvrh == '{':
                    apxac__gdhhj = 2
                else:
                    return None
            elif apxac__gdhhj == 2:
                if ydsv__xvrh.isspace():
                    continue
                elif ydsv__xvrh == '"':
                    apxac__gdhhj = 3
                elif ydsv__xvrh == '}':
                    apxac__gdhhj = 9
                else:
                    return None
            elif apxac__gdhhj == 3:
                if fgf__bte:
                    oqlr__qpd += ydsv__xvrh
                    fgf__bte = False
                elif ydsv__xvrh == '"':
                    apxac__gdhhj = 4
                elif ydsv__xvrh == '\\':
                    fgf__bte = True
                else:
                    oqlr__qpd += ydsv__xvrh
            elif apxac__gdhhj == 4:
                if ydsv__xvrh.isspace():
                    continue
                elif ydsv__xvrh == ':':
                    apxac__gdhhj = 5
                else:
                    return None
            elif apxac__gdhhj == 5:
                if ydsv__xvrh.isspace():
                    continue
                if ydsv__xvrh in '},]':
                    return None
                else:
                    apxac__gdhhj = 7 if ydsv__xvrh == '"' else 6
                    dxj__jtthu += ydsv__xvrh
                    if ydsv__xvrh in '{[':
                        sgxo__gok.append(ydsv__xvrh)
            elif apxac__gdhhj == 6:
                if ydsv__xvrh.isspace():
                    continue
                if ydsv__xvrh in '{[':
                    dxj__jtthu += ydsv__xvrh
                    sgxo__gok.append(ydsv__xvrh)
                elif ydsv__xvrh in '}]':
                    huv__jfyt = '{' if ydsv__xvrh == '}' else '['
                    if len(sgxo__gok) == 0 or sgxo__gok[-1] != huv__jfyt:
                        return None
                    elif len(sgxo__gok) == 1:
                        cehv__bxrv[oqlr__qpd] = dxj__jtthu
                        oqlr__qpd = ''
                        dxj__jtthu = ''
                        sgxo__gok.pop()
                        apxac__gdhhj = 9
                    elif len(sgxo__gok) == 2:
                        dxj__jtthu += ydsv__xvrh
                        cehv__bxrv[oqlr__qpd] = dxj__jtthu
                        oqlr__qpd = ''
                        dxj__jtthu = ''
                        sgxo__gok.pop()
                        apxac__gdhhj = 8
                    else:
                        dxj__jtthu += ydsv__xvrh
                        sgxo__gok.pop()
                elif ydsv__xvrh == '"':
                    dxj__jtthu += ydsv__xvrh
                    apxac__gdhhj = 7
                elif ydsv__xvrh == ',':
                    if len(sgxo__gok) == 1:
                        cehv__bxrv[oqlr__qpd] = dxj__jtthu
                        oqlr__qpd = ''
                        dxj__jtthu = ''
                        apxac__gdhhj = 2
                    else:
                        dxj__jtthu += ydsv__xvrh
                else:
                    dxj__jtthu += ydsv__xvrh
            elif apxac__gdhhj == 7:
                if fgf__bte:
                    dxj__jtthu += ydsv__xvrh
                    fgf__bte = False
                elif ydsv__xvrh == '\\':
                    fgf__bte = True
                elif ydsv__xvrh == '"':
                    dxj__jtthu += ydsv__xvrh
                    apxac__gdhhj = 6
                else:
                    dxj__jtthu += ydsv__xvrh
            elif apxac__gdhhj == 8:
                if ydsv__xvrh.isspace():
                    continue
                elif ydsv__xvrh == ',':
                    apxac__gdhhj = 2
                elif ydsv__xvrh == '}':
                    apxac__gdhhj = 9
                else:
                    return None
            elif apxac__gdhhj == 9:
                if not ydsv__xvrh.isspace():
                    return None
        return cehv__bxrv if apxac__gdhhj == 9 else None
    return impl


@numba.generated_jit(nopython=True)
def parse_json_util(arr):
    bodo.libs.bodosql_array_kernels.verify_string_arg(arr, 'PARSE_JSON', 's')
    ikhg__uridh = ['arr']
    euu__fie = [arr]
    ave__wue = [False]
    qgd__pbzaq = """jmap = bodo.libs.bodosql_json_array_kernels.parse_single_json_map(arg0) if arg0 is not None else None
"""
    if bodo.utils.utils.is_array_typ(arr, True):
        jkyxm__uvgwf = (
            'lengths = bodo.utils.utils.alloc_type(n, bodo.int32, (-1,))\n')
        qgd__pbzaq += 'res.append(jmap)\n'
        qgd__pbzaq += 'if jmap is None:\n'
        qgd__pbzaq += '   lengths[i] = 0\n'
        qgd__pbzaq += 'else:\n'
        qgd__pbzaq += '   lengths[i] = len(jmap)\n'
    else:
        jkyxm__uvgwf = None
        qgd__pbzaq += 'return jmap'
    vgse__nvchh = (
        'res2 = bodo.libs.map_arr_ext.pre_alloc_map_array(n, lengths, out_dtype)\n'
        )
    vgse__nvchh += 'numba.parfors.parfor.init_prange()\n'
    vgse__nvchh += 'for i in numba.parfors.parfor.internal_prange(n):\n'
    vgse__nvchh += '   if res[i] is None:\n'
    vgse__nvchh += '     bodo.libs.array_kernels.setna(res2, i)\n'
    vgse__nvchh += '   else:\n'
    vgse__nvchh += '     res2[i] = res[i]\n'
    vgse__nvchh += 'res = res2\n'
    hrd__rfevg = bodo.StructArrayType((bodo.string_array_type, bodo.
        string_array_type), ('key', 'value'))
    srjc__fvpg = bodo.utils.typing.to_nullable_type(hrd__rfevg)
    return gen_vectorized(ikhg__uridh, euu__fie, ave__wue, qgd__pbzaq,
        srjc__fvpg, prefix_code=jkyxm__uvgwf, suffix_code=vgse__nvchh,
        res_list=True, support_dict_encoding=False)
