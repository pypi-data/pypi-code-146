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
    for alwps__lyje in range(len(A)):
        if isinstance(A[alwps__lyje], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], 0, container_arg=alwps__lyje, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    yxgft__jnezl = None
    tonmc__xly = []
    knr__yyer = False
    for alwps__lyje in range(len(A)):
        if A[alwps__lyje] == bodo.none:
            tonmc__xly.append(alwps__lyje)
        elif not bodo.utils.utils.is_array_typ(A[alwps__lyje]):
            for xtd__neng in range(alwps__lyje + 1, len(A)):
                tonmc__xly.append(xtd__neng)
                if bodo.utils.utils.is_array_typ(A[xtd__neng]):
                    yxgft__jnezl = f'A[{xtd__neng}]'
                    knr__yyer = True
            break
        else:
            knr__yyer = True
    huhep__wyqw = [f'A{alwps__lyje}' for alwps__lyje in range(len(A)) if 
        alwps__lyje not in tonmc__xly]
    lngv__nut = [A[alwps__lyje] for alwps__lyje in range(len(A)) if 
        alwps__lyje not in tonmc__xly]
    hsq__wwla = get_common_broadcasted_type(lngv__nut, 'COALESCE')
    gmv__smu = knr__yyer and is_str_arr_type(hsq__wwla)
    pjys__kdn = [False] * (len(A) - len(tonmc__xly))
    nrr__lnd = False
    if gmv__smu:
        nrr__lnd = True
        for xtd__neng, jwamo__spd in enumerate(lngv__nut):
            nrr__lnd = nrr__lnd and (jwamo__spd == bodo.string_type or 
                jwamo__spd == bodo.dict_str_arr_type or isinstance(
                jwamo__spd, bodo.SeriesType) and jwamo__spd.data == bodo.
                dict_str_arr_type)
    ypzpy__pdhqa = ''
    kqgg__ydolz = True
    jxve__tmrbe = False
    gjzib__wcvbo = 0
    qscub__tqkml = None
    if nrr__lnd:
        qscub__tqkml = 'num_strings = 0\n'
        qscub__tqkml += 'num_chars = 0\n'
        qscub__tqkml += 'is_dict_global = True\n'
        for alwps__lyje in range(len(A)):
            if alwps__lyje in tonmc__xly:
                gjzib__wcvbo += 1
                continue
            elif lngv__nut[alwps__lyje - gjzib__wcvbo] != bodo.string_type:
                qscub__tqkml += f"""old_indices{alwps__lyje - gjzib__wcvbo} = A{alwps__lyje}._indices
"""
                qscub__tqkml += (
                    f'old_data{alwps__lyje - gjzib__wcvbo} = A{alwps__lyje}._data\n'
                    )
                qscub__tqkml += f"""is_dict_global = is_dict_global and A{alwps__lyje}._has_global_dictionary
"""
                qscub__tqkml += (
                    f'index_offset{alwps__lyje - gjzib__wcvbo} = num_strings\n'
                    )
                qscub__tqkml += (
                    f'num_strings += len(old_data{alwps__lyje - gjzib__wcvbo})\n'
                    )
                qscub__tqkml += f"""num_chars += bodo.libs.str_arr_ext.num_total_chars(old_data{alwps__lyje - gjzib__wcvbo})
"""
            else:
                qscub__tqkml += f'num_strings += 1\n'
                qscub__tqkml += f"""num_chars += bodo.libs.str_ext.unicode_to_utf8_len(A{alwps__lyje})
"""
    gjzib__wcvbo = 0
    for alwps__lyje in range(len(A)):
        if alwps__lyje in tonmc__xly:
            gjzib__wcvbo += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[alwps__lyje]):
            pso__tupt = 'if' if kqgg__ydolz else 'elif'
            ypzpy__pdhqa += (
                f'{pso__tupt} not bodo.libs.array_kernels.isna(A{alwps__lyje}, i):\n'
                )
            if nrr__lnd:
                ypzpy__pdhqa += f"""   res[i] = old_indices{alwps__lyje - gjzib__wcvbo}[i] + index_offset{alwps__lyje - gjzib__wcvbo}
"""
            elif gmv__smu:
                ypzpy__pdhqa += f"""   bodo.libs.str_arr_ext.get_str_arr_item_copy(res, i, A{alwps__lyje}, i)
"""
            else:
                ypzpy__pdhqa += (
                    f'   res[i] = arg{alwps__lyje - gjzib__wcvbo}\n')
            kqgg__ydolz = False
        else:
            assert not jxve__tmrbe, 'should not encounter more than one scalar due to dead column pruning'
            fys__fcul = ''
            if not kqgg__ydolz:
                ypzpy__pdhqa += 'else:\n'
                fys__fcul = '   '
            if nrr__lnd:
                ypzpy__pdhqa += f'{fys__fcul}res[i] = num_strings - 1\n'
            else:
                ypzpy__pdhqa += (
                    f'{fys__fcul}res[i] = arg{alwps__lyje - gjzib__wcvbo}\n')
            jxve__tmrbe = True
            break
    if not jxve__tmrbe:
        if not kqgg__ydolz:
            ypzpy__pdhqa += 'else:\n'
            ypzpy__pdhqa += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            ypzpy__pdhqa += 'bodo.libs.array_kernels.setna(res, i)'
    cpn__lrlqq = None
    if nrr__lnd:
        gjzib__wcvbo = 0
        cpn__lrlqq = """dict_data = bodo.libs.str_arr_ext.pre_alloc_string_array(num_strings, num_chars)
"""
        cpn__lrlqq += 'curr_index = 0\n'
        for alwps__lyje in range(len(A)):
            if alwps__lyje in tonmc__xly:
                gjzib__wcvbo += 1
            elif lngv__nut[alwps__lyje - gjzib__wcvbo] != bodo.string_type:
                cpn__lrlqq += (
                    f'section_len = len(old_data{alwps__lyje - gjzib__wcvbo})\n'
                    )
                cpn__lrlqq += f'for l in range(section_len):\n'
                cpn__lrlqq += f"""    bodo.libs.str_arr_ext.get_str_arr_item_copy(dict_data, curr_index + l, old_data{alwps__lyje - gjzib__wcvbo}, l)
"""
                cpn__lrlqq += f'curr_index += section_len\n'
            else:
                cpn__lrlqq += f'dict_data[curr_index] = A{alwps__lyje}\n'
                cpn__lrlqq += f'curr_index += 1\n'
        cpn__lrlqq += """duplicated_res = bodo.libs.dict_arr_ext.init_dict_arr(dict_data, res, is_dict_global, False)
"""
        cpn__lrlqq += """res = bodo.libs.array.drop_duplicates_local_dictionary(duplicated_res, False)
"""
    bpv__rwks = 'A'
    ffny__xtl = {f'A{alwps__lyje}': f'A[{alwps__lyje}]' for alwps__lyje in
        range(len(A)) if alwps__lyje not in tonmc__xly}
    if nrr__lnd:
        hsq__wwla = bodo.libs.dict_arr_ext.dict_indices_arr_type
    return gen_vectorized(huhep__wyqw, lngv__nut, pjys__kdn, ypzpy__pdhqa,
        hsq__wwla, bpv__rwks, ffny__xtl, yxgft__jnezl,
        support_dict_encoding=False, prefix_code=qscub__tqkml, suffix_code=
        cpn__lrlqq, alloc_array_scalars=not gmv__smu)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for alwps__lyje in range(len(A)):
        if isinstance(A[alwps__lyje], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], 0, container_arg=alwps__lyje, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    huhep__wyqw = [f'A{alwps__lyje}' for alwps__lyje in range(len(A))]
    lngv__nut = [A[alwps__lyje] for alwps__lyje in range(len(A))]
    pjys__kdn = [False] * len(A)
    ypzpy__pdhqa = ''
    for alwps__lyje in range(1, len(A) - 1, 2):
        pso__tupt = 'if' if len(ypzpy__pdhqa) == 0 else 'elif'
        if A[alwps__lyje + 1] == bodo.none:
            wmt__arhk = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[alwps__lyje + 1]):
            wmt__arhk = (
                f'   if bodo.libs.array_kernels.isna({huhep__wyqw[alwps__lyje + 1]}, i):\n'
                )
            wmt__arhk += f'      bodo.libs.array_kernels.setna(res, i)\n'
            wmt__arhk += f'   else:\n'
            wmt__arhk += f'      res[i] = arg{alwps__lyje + 1}\n'
        else:
            wmt__arhk = f'   res[i] = arg{alwps__lyje + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[
            alwps__lyje]) or A[alwps__lyje] == bodo.none):
            if A[alwps__lyje] == bodo.none:
                ypzpy__pdhqa += f'{pso__tupt} True:\n'
                ypzpy__pdhqa += wmt__arhk
                break
            else:
                ypzpy__pdhqa += f"""{pso__tupt} bodo.libs.array_kernels.isna({huhep__wyqw[alwps__lyje]}, i):
"""
                ypzpy__pdhqa += wmt__arhk
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[alwps__lyje]):
                ypzpy__pdhqa += f"""{pso__tupt} (bodo.libs.array_kernels.isna({huhep__wyqw[0]}, i) and bodo.libs.array_kernels.isna({huhep__wyqw[alwps__lyje]}, i)) or (not bodo.libs.array_kernels.isna({huhep__wyqw[0]}, i) and not bodo.libs.array_kernels.isna({huhep__wyqw[alwps__lyje]}, i) and arg0 == arg{alwps__lyje}):
"""
                ypzpy__pdhqa += wmt__arhk
            elif A[alwps__lyje] == bodo.none:
                ypzpy__pdhqa += (
                    f'{pso__tupt} bodo.libs.array_kernels.isna({huhep__wyqw[0]}, i):\n'
                    )
                ypzpy__pdhqa += wmt__arhk
            else:
                ypzpy__pdhqa += f"""{pso__tupt} (not bodo.libs.array_kernels.isna({huhep__wyqw[0]}, i)) and arg0 == arg{alwps__lyje}:
"""
                ypzpy__pdhqa += wmt__arhk
        elif A[alwps__lyje] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[alwps__lyje]):
            ypzpy__pdhqa += f"""{pso__tupt} (not bodo.libs.array_kernels.isna({huhep__wyqw[alwps__lyje]}, i)) and arg0 == arg{alwps__lyje}:
"""
            ypzpy__pdhqa += wmt__arhk
        else:
            ypzpy__pdhqa += f'{pso__tupt} arg0 == arg{alwps__lyje}:\n'
            ypzpy__pdhqa += wmt__arhk
    if len(ypzpy__pdhqa) > 0:
        ypzpy__pdhqa += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            ypzpy__pdhqa += (
                f'   if bodo.libs.array_kernels.isna({huhep__wyqw[-1]}, i):\n')
            ypzpy__pdhqa += '      bodo.libs.array_kernels.setna(res, i)\n'
            ypzpy__pdhqa += '   else:\n'
        ypzpy__pdhqa += f'      res[i] = arg{len(A) - 1}'
    else:
        ypzpy__pdhqa += '   bodo.libs.array_kernels.setna(res, i)'
    bpv__rwks = 'A'
    ffny__xtl = {f'A{alwps__lyje}': f'A[{alwps__lyje}]' for alwps__lyje in
        range(len(A))}
    if len(lngv__nut) % 2 == 0:
        mvu__mweb = [lngv__nut[0]] + lngv__nut[1:-1:2]
        mhhj__rwxai = lngv__nut[2::2] + [lngv__nut[-1]]
    else:
        mvu__mweb = [lngv__nut[0]] + lngv__nut[1::2]
        mhhj__rwxai = lngv__nut[2::2]
    ojn__jwv = get_common_broadcasted_type(mvu__mweb, 'DECODE')
    hsq__wwla = get_common_broadcasted_type(mhhj__rwxai, 'DECODE')
    if hsq__wwla == bodo.none:
        hsq__wwla = ojn__jwv
    lhqn__pccrr = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in mvu__mweb and len(lngv__nut) % 2 == 1
    return gen_vectorized(huhep__wyqw, lngv__nut, pjys__kdn, ypzpy__pdhqa,
        hsq__wwla, bpv__rwks, ffny__xtl, support_dict_encoding=lhqn__pccrr)


def concat_ws(A, sep):
    return


@overload(concat_ws)
def overload_concat_ws(A, sep):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('concat_ws argument must be a tuple')
    for alwps__lyje in range(len(A)):
        if isinstance(A[alwps__lyje], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
                ['A', 'sep'], 0, container_arg=alwps__lyje,
                container_length=len(A))
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
    huhep__wyqw = []
    lngv__nut = []
    for alwps__lyje, xira__ieabc in enumerate(A):
        zyn__ltphb = f'A{alwps__lyje}'
        verify_string_arg(xira__ieabc, 'CONCAT_WS', zyn__ltphb)
        huhep__wyqw.append(zyn__ltphb)
        lngv__nut.append(xira__ieabc)
    huhep__wyqw.append('sep')
    verify_string_arg(sep, 'CONCAT_WS', 'sep')
    lngv__nut.append(sep)
    pjys__kdn = [True] * len(huhep__wyqw)
    hsq__wwla = bodo.string_array_type
    bpv__rwks = 'A, sep'
    ffny__xtl = {f'A{alwps__lyje}': f'A[{alwps__lyje}]' for alwps__lyje in
        range(len(A))}
    bwscj__xwm = ','.join([f'arg{alwps__lyje}' for alwps__lyje in range(len
        (A))])
    ypzpy__pdhqa = f'  res[i] = arg{len(A)}.join([{bwscj__xwm}])\n'
    return gen_vectorized(huhep__wyqw, lngv__nut, pjys__kdn, ypzpy__pdhqa,
        hsq__wwla, bpv__rwks, ffny__xtl)
