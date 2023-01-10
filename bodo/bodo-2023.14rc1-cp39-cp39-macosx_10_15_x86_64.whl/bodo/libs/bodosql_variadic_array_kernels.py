"""
Implements array kernels that are specific to BodoSQL which have a variable
number of arguments
"""
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import is_str_arr_type, raise_bodo_error


def coalesce(A):
    return


@overload(coalesce)
def overload_coalesce(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Coalesce argument must be a tuple')
    for noz__vdije in range(len(A)):
        if isinstance(A[noz__vdije], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], 0, container_arg=noz__vdije, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    ezc__gom = None
    gqy__nbhv = []
    shh__pljrq = False
    for noz__vdije in range(len(A)):
        if A[noz__vdije] == bodo.none:
            gqy__nbhv.append(noz__vdije)
        elif not bodo.utils.utils.is_array_typ(A[noz__vdije]):
            for yrzjh__kysei in range(noz__vdije + 1, len(A)):
                gqy__nbhv.append(yrzjh__kysei)
                if bodo.utils.utils.is_array_typ(A[yrzjh__kysei]):
                    ezc__gom = f'A[{yrzjh__kysei}]'
                    shh__pljrq = True
            break
        else:
            shh__pljrq = True
    izfc__vri = [f'A{noz__vdije}' for noz__vdije in range(len(A)) if 
        noz__vdije not in gqy__nbhv]
    oev__xlcmd = [A[noz__vdije] for noz__vdije in range(len(A)) if 
        noz__vdije not in gqy__nbhv]
    wwzq__kexs = get_common_broadcasted_type(oev__xlcmd, 'COALESCE')
    xpqv__zacr = shh__pljrq and is_str_arr_type(wwzq__kexs)
    pok__lces = [False] * (len(A) - len(gqy__nbhv))
    guf__urhtt = False
    if xpqv__zacr:
        guf__urhtt = True
        for yrzjh__kysei, pkr__ewz in enumerate(oev__xlcmd):
            guf__urhtt = guf__urhtt and (pkr__ewz == bodo.string_type or 
                pkr__ewz == bodo.dict_str_arr_type or isinstance(pkr__ewz,
                bodo.SeriesType) and pkr__ewz.data == bodo.dict_str_arr_type)
    iiaj__jedy = ''
    qtefh__qlsog = True
    ybb__xldgw = False
    ywjy__hdz = 0
    pqzez__mgm = None
    if guf__urhtt:
        pqzez__mgm = 'num_strings = 0\n'
        pqzez__mgm += 'num_chars = 0\n'
        pqzez__mgm += 'is_dict_global = True\n'
        for noz__vdije in range(len(A)):
            if noz__vdije in gqy__nbhv:
                ywjy__hdz += 1
                continue
            elif oev__xlcmd[noz__vdije - ywjy__hdz] != bodo.string_type:
                pqzez__mgm += (
                    f'old_indices{noz__vdije - ywjy__hdz} = A{noz__vdije}._indices\n'
                    )
                pqzez__mgm += (
                    f'old_data{noz__vdije - ywjy__hdz} = A{noz__vdije}._data\n'
                    )
                pqzez__mgm += f"""is_dict_global = is_dict_global and A{noz__vdije}._has_global_dictionary
"""
                pqzez__mgm += (
                    f'index_offset{noz__vdije - ywjy__hdz} = num_strings\n')
                pqzez__mgm += (
                    f'num_strings += len(old_data{noz__vdije - ywjy__hdz})\n')
                pqzez__mgm += f"""num_chars += bodo.libs.str_arr_ext.num_total_chars(old_data{noz__vdije - ywjy__hdz})
"""
            else:
                pqzez__mgm += f'num_strings += 1\n'
                pqzez__mgm += (
                    f'num_chars += bodo.libs.str_ext.unicode_to_utf8_len(A{noz__vdije})\n'
                    )
    ywjy__hdz = 0
    for noz__vdije in range(len(A)):
        if noz__vdije in gqy__nbhv:
            ywjy__hdz += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[noz__vdije]):
            hkt__ley = 'if' if qtefh__qlsog else 'elif'
            iiaj__jedy += (
                f'{hkt__ley} not bodo.libs.array_kernels.isna(A{noz__vdije}, i):\n'
                )
            if guf__urhtt:
                iiaj__jedy += f"""   res[i] = old_indices{noz__vdije - ywjy__hdz}[i] + index_offset{noz__vdije - ywjy__hdz}
"""
            elif xpqv__zacr:
                iiaj__jedy += f"""   bodo.libs.str_arr_ext.get_str_arr_item_copy(res, i, A{noz__vdije}, i)
"""
            else:
                iiaj__jedy += f'   res[i] = arg{noz__vdije - ywjy__hdz}\n'
            qtefh__qlsog = False
        else:
            assert not ybb__xldgw, 'should not encounter more than one scalar due to dead column pruning'
            oci__kjr = ''
            if not qtefh__qlsog:
                iiaj__jedy += 'else:\n'
                oci__kjr = '   '
            if guf__urhtt:
                iiaj__jedy += f'{oci__kjr}res[i] = num_strings - 1\n'
            else:
                iiaj__jedy += (
                    f'{oci__kjr}res[i] = arg{noz__vdije - ywjy__hdz}\n')
            ybb__xldgw = True
            break
    if not ybb__xldgw:
        if not qtefh__qlsog:
            iiaj__jedy += 'else:\n'
            iiaj__jedy += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            iiaj__jedy += 'bodo.libs.array_kernels.setna(res, i)'
    mts__khcal = None
    if guf__urhtt:
        ywjy__hdz = 0
        mts__khcal = """dict_data = bodo.libs.str_arr_ext.pre_alloc_string_array(num_strings, num_chars)
"""
        mts__khcal += 'curr_index = 0\n'
        for noz__vdije in range(len(A)):
            if noz__vdije in gqy__nbhv:
                ywjy__hdz += 1
            elif oev__xlcmd[noz__vdije - ywjy__hdz] != bodo.string_type:
                mts__khcal += (
                    f'section_len = len(old_data{noz__vdije - ywjy__hdz})\n')
                mts__khcal += f'for l in range(section_len):\n'
                mts__khcal += f"""    bodo.libs.str_arr_ext.get_str_arr_item_copy(dict_data, curr_index + l, old_data{noz__vdije - ywjy__hdz}, l)
"""
                mts__khcal += f'curr_index += section_len\n'
            else:
                mts__khcal += f'dict_data[curr_index] = A{noz__vdije}\n'
                mts__khcal += f'curr_index += 1\n'
        mts__khcal += """duplicated_res = bodo.libs.dict_arr_ext.init_dict_arr(dict_data, res, is_dict_global, False)
"""
        mts__khcal += """res = bodo.libs.array.drop_duplicates_local_dictionary(duplicated_res, False)
"""
    zpwz__ywre = 'A'
    ysszt__qxg = {f'A{noz__vdije}': f'A[{noz__vdije}]' for noz__vdije in
        range(len(A)) if noz__vdije not in gqy__nbhv}
    if guf__urhtt:
        wwzq__kexs = bodo.libs.dict_arr_ext.dict_indices_arr_type
    return gen_vectorized(izfc__vri, oev__xlcmd, pok__lces, iiaj__jedy,
        wwzq__kexs, zpwz__ywre, ysszt__qxg, ezc__gom, support_dict_encoding
        =False, prefix_code=pqzez__mgm, suffix_code=mts__khcal,
        alloc_array_scalars=not xpqv__zacr)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for noz__vdije in range(len(A)):
        if isinstance(A[noz__vdije], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], 0, container_arg=noz__vdije, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    izfc__vri = [f'A{noz__vdije}' for noz__vdije in range(len(A))]
    oev__xlcmd = [A[noz__vdije] for noz__vdije in range(len(A))]
    pok__lces = [False] * len(A)
    iiaj__jedy = ''
    for noz__vdije in range(1, len(A) - 1, 2):
        hkt__ley = 'if' if len(iiaj__jedy) == 0 else 'elif'
        if A[noz__vdije + 1] == bodo.none:
            yqol__rdfb = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[noz__vdije + 1]):
            yqol__rdfb = (
                f'   if bodo.libs.array_kernels.isna({izfc__vri[noz__vdije + 1]}, i):\n'
                )
            yqol__rdfb += f'      bodo.libs.array_kernels.setna(res, i)\n'
            yqol__rdfb += f'   else:\n'
            yqol__rdfb += f'      res[i] = arg{noz__vdije + 1}\n'
        else:
            yqol__rdfb = f'   res[i] = arg{noz__vdije + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[
            noz__vdije]) or A[noz__vdije] == bodo.none):
            if A[noz__vdije] == bodo.none:
                iiaj__jedy += f'{hkt__ley} True:\n'
                iiaj__jedy += yqol__rdfb
                break
            else:
                iiaj__jedy += f"""{hkt__ley} bodo.libs.array_kernels.isna({izfc__vri[noz__vdije]}, i):
"""
                iiaj__jedy += yqol__rdfb
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[noz__vdije]):
                iiaj__jedy += f"""{hkt__ley} (bodo.libs.array_kernels.isna({izfc__vri[0]}, i) and bodo.libs.array_kernels.isna({izfc__vri[noz__vdije]}, i)) or (not bodo.libs.array_kernels.isna({izfc__vri[0]}, i) and not bodo.libs.array_kernels.isna({izfc__vri[noz__vdije]}, i) and arg0 == arg{noz__vdije}):
"""
                iiaj__jedy += yqol__rdfb
            elif A[noz__vdije] == bodo.none:
                iiaj__jedy += (
                    f'{hkt__ley} bodo.libs.array_kernels.isna({izfc__vri[0]}, i):\n'
                    )
                iiaj__jedy += yqol__rdfb
            else:
                iiaj__jedy += f"""{hkt__ley} (not bodo.libs.array_kernels.isna({izfc__vri[0]}, i)) and arg0 == arg{noz__vdije}:
"""
                iiaj__jedy += yqol__rdfb
        elif A[noz__vdije] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[noz__vdije]):
            iiaj__jedy += f"""{hkt__ley} (not bodo.libs.array_kernels.isna({izfc__vri[noz__vdije]}, i)) and arg0 == arg{noz__vdije}:
"""
            iiaj__jedy += yqol__rdfb
        else:
            iiaj__jedy += f'{hkt__ley} arg0 == arg{noz__vdije}:\n'
            iiaj__jedy += yqol__rdfb
    if len(iiaj__jedy) > 0:
        iiaj__jedy += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            iiaj__jedy += (
                f'   if bodo.libs.array_kernels.isna({izfc__vri[-1]}, i):\n')
            iiaj__jedy += '      bodo.libs.array_kernels.setna(res, i)\n'
            iiaj__jedy += '   else:\n'
        iiaj__jedy += f'      res[i] = arg{len(A) - 1}'
    else:
        iiaj__jedy += '   bodo.libs.array_kernels.setna(res, i)'
    zpwz__ywre = 'A'
    ysszt__qxg = {f'A{noz__vdije}': f'A[{noz__vdije}]' for noz__vdije in
        range(len(A))}
    if len(oev__xlcmd) % 2 == 0:
        laqyp__dwfxm = [oev__xlcmd[0]] + oev__xlcmd[1:-1:2]
        blhtv__jorjn = oev__xlcmd[2::2] + [oev__xlcmd[-1]]
    else:
        laqyp__dwfxm = [oev__xlcmd[0]] + oev__xlcmd[1::2]
        blhtv__jorjn = oev__xlcmd[2::2]
    lai__tyyiu = get_common_broadcasted_type(laqyp__dwfxm, 'DECODE')
    wwzq__kexs = get_common_broadcasted_type(blhtv__jorjn, 'DECODE')
    if wwzq__kexs == bodo.none:
        wwzq__kexs = lai__tyyiu
    lwlvi__palr = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in laqyp__dwfxm and len(oev__xlcmd) % 2 == 1
    return gen_vectorized(izfc__vri, oev__xlcmd, pok__lces, iiaj__jedy,
        wwzq__kexs, zpwz__ywre, ysszt__qxg, support_dict_encoding=lwlvi__palr)


def concat_ws(A, sep):
    return


@overload(concat_ws)
def overload_concat_ws(A, sep):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('concat_ws argument must be a tuple')
    for noz__vdije in range(len(A)):
        if isinstance(A[noz__vdije], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
                ['A', 'sep'], 0, container_arg=noz__vdije, container_length
                =len(A))
    if isinstance(sep, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
            ['A', 'sep'], 1)

    def impl(A, sep):
        return concat_ws_util(A, sep)
    return impl


def concat_ws_util(A, sep):
    return


@overload(concat_ws_util, no_unliteral=True)
def overload_concat_ws_util(A, sep):
    if len(A) == 0:
        raise_bodo_error('Cannot concatenate 0 columns')
    izfc__vri = []
    oev__xlcmd = []
    for noz__vdije, qthvv__djr in enumerate(A):
        ykttv__xhccs = f'A{noz__vdije}'
        verify_string_arg(qthvv__djr, 'CONCAT_WS', ykttv__xhccs)
        izfc__vri.append(ykttv__xhccs)
        oev__xlcmd.append(qthvv__djr)
    izfc__vri.append('sep')
    verify_string_arg(sep, 'CONCAT_WS', 'sep')
    oev__xlcmd.append(sep)
    pok__lces = [True] * len(izfc__vri)
    wwzq__kexs = bodo.string_array_type
    zpwz__ywre = 'A, sep'
    ysszt__qxg = {f'A{noz__vdije}': f'A[{noz__vdije}]' for noz__vdije in
        range(len(A))}
    nivfr__pvtu = ','.join([f'arg{noz__vdije}' for noz__vdije in range(len(A))]
        )
    iiaj__jedy = f'  res[i] = arg{len(A)}.join([{nivfr__pvtu}])\n'
    return gen_vectorized(izfc__vri, oev__xlcmd, pok__lces, iiaj__jedy,
        wwzq__kexs, zpwz__ywre, ysszt__qxg)
