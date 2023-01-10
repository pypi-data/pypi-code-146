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
    for wbf__cklj in range(len(A)):
        if isinstance(A[wbf__cklj], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], 0, container_arg=wbf__cklj, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    gah__qen = None
    bdt__mogqz = []
    gcrnv__ifonm = False
    for wbf__cklj in range(len(A)):
        if A[wbf__cklj] == bodo.none:
            bdt__mogqz.append(wbf__cklj)
        elif not bodo.utils.utils.is_array_typ(A[wbf__cklj]):
            for fch__glzup in range(wbf__cklj + 1, len(A)):
                bdt__mogqz.append(fch__glzup)
                if bodo.utils.utils.is_array_typ(A[fch__glzup]):
                    gah__qen = f'A[{fch__glzup}]'
                    gcrnv__ifonm = True
            break
        else:
            gcrnv__ifonm = True
    gezdn__inau = [f'A{wbf__cklj}' for wbf__cklj in range(len(A)) if 
        wbf__cklj not in bdt__mogqz]
    rjlq__wmsmm = [A[wbf__cklj] for wbf__cklj in range(len(A)) if wbf__cklj
         not in bdt__mogqz]
    gjx__ozv = get_common_broadcasted_type(rjlq__wmsmm, 'COALESCE')
    stt__tdxo = gcrnv__ifonm and is_str_arr_type(gjx__ozv)
    suuy__hpko = [False] * (len(A) - len(bdt__mogqz))
    mqgh__xuhys = False
    if stt__tdxo:
        mqgh__xuhys = True
        for fch__glzup, rgj__lpalb in enumerate(rjlq__wmsmm):
            mqgh__xuhys = mqgh__xuhys and (rgj__lpalb == bodo.string_type or
                rgj__lpalb == bodo.dict_str_arr_type or isinstance(
                rgj__lpalb, bodo.SeriesType) and rgj__lpalb.data == bodo.
                dict_str_arr_type)
    yat__cao = ''
    nfiz__oshed = True
    mmxf__sdl = False
    qrtqa__hwfib = 0
    butsl__uth = None
    if mqgh__xuhys:
        butsl__uth = 'num_strings = 0\n'
        butsl__uth += 'num_chars = 0\n'
        butsl__uth += 'is_dict_global = True\n'
        for wbf__cklj in range(len(A)):
            if wbf__cklj in bdt__mogqz:
                qrtqa__hwfib += 1
                continue
            elif rjlq__wmsmm[wbf__cklj - qrtqa__hwfib] != bodo.string_type:
                butsl__uth += (
                    f'old_indices{wbf__cklj - qrtqa__hwfib} = A{wbf__cklj}._indices\n'
                    )
                butsl__uth += (
                    f'old_data{wbf__cklj - qrtqa__hwfib} = A{wbf__cklj}._data\n'
                    )
                butsl__uth += f"""is_dict_global = is_dict_global and A{wbf__cklj}._has_global_dictionary
"""
                butsl__uth += (
                    f'index_offset{wbf__cklj - qrtqa__hwfib} = num_strings\n')
                butsl__uth += (
                    f'num_strings += len(old_data{wbf__cklj - qrtqa__hwfib})\n'
                    )
                butsl__uth += f"""num_chars += bodo.libs.str_arr_ext.num_total_chars(old_data{wbf__cklj - qrtqa__hwfib})
"""
            else:
                butsl__uth += f'num_strings += 1\n'
                butsl__uth += (
                    f'num_chars += bodo.libs.str_ext.unicode_to_utf8_len(A{wbf__cklj})\n'
                    )
    qrtqa__hwfib = 0
    for wbf__cklj in range(len(A)):
        if wbf__cklj in bdt__mogqz:
            qrtqa__hwfib += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[wbf__cklj]):
            lxpgp__npai = 'if' if nfiz__oshed else 'elif'
            yat__cao += (
                f'{lxpgp__npai} not bodo.libs.array_kernels.isna(A{wbf__cklj}, i):\n'
                )
            if mqgh__xuhys:
                yat__cao += f"""   res[i] = old_indices{wbf__cklj - qrtqa__hwfib}[i] + index_offset{wbf__cklj - qrtqa__hwfib}
"""
            elif stt__tdxo:
                yat__cao += f"""   bodo.libs.str_arr_ext.get_str_arr_item_copy(res, i, A{wbf__cklj}, i)
"""
            else:
                yat__cao += f'   res[i] = arg{wbf__cklj - qrtqa__hwfib}\n'
            nfiz__oshed = False
        else:
            assert not mmxf__sdl, 'should not encounter more than one scalar due to dead column pruning'
            pvlaa__djr = ''
            if not nfiz__oshed:
                yat__cao += 'else:\n'
                pvlaa__djr = '   '
            if mqgh__xuhys:
                yat__cao += f'{pvlaa__djr}res[i] = num_strings - 1\n'
            else:
                yat__cao += (
                    f'{pvlaa__djr}res[i] = arg{wbf__cklj - qrtqa__hwfib}\n')
            mmxf__sdl = True
            break
    if not mmxf__sdl:
        if not nfiz__oshed:
            yat__cao += 'else:\n'
            yat__cao += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            yat__cao += 'bodo.libs.array_kernels.setna(res, i)'
    jlfb__vwjij = None
    if mqgh__xuhys:
        qrtqa__hwfib = 0
        jlfb__vwjij = """dict_data = bodo.libs.str_arr_ext.pre_alloc_string_array(num_strings, num_chars)
"""
        jlfb__vwjij += 'curr_index = 0\n'
        for wbf__cklj in range(len(A)):
            if wbf__cklj in bdt__mogqz:
                qrtqa__hwfib += 1
            elif rjlq__wmsmm[wbf__cklj - qrtqa__hwfib] != bodo.string_type:
                jlfb__vwjij += (
                    f'section_len = len(old_data{wbf__cklj - qrtqa__hwfib})\n')
                jlfb__vwjij += f'for l in range(section_len):\n'
                jlfb__vwjij += f"""    bodo.libs.str_arr_ext.get_str_arr_item_copy(dict_data, curr_index + l, old_data{wbf__cklj - qrtqa__hwfib}, l)
"""
                jlfb__vwjij += f'curr_index += section_len\n'
            else:
                jlfb__vwjij += f'dict_data[curr_index] = A{wbf__cklj}\n'
                jlfb__vwjij += f'curr_index += 1\n'
        jlfb__vwjij += """duplicated_res = bodo.libs.dict_arr_ext.init_dict_arr(dict_data, res, is_dict_global, False)
"""
        jlfb__vwjij += """res = bodo.libs.array.drop_duplicates_local_dictionary(duplicated_res, False)
"""
    dha__mvpb = 'A'
    sdu__zxkx = {f'A{wbf__cklj}': f'A[{wbf__cklj}]' for wbf__cklj in range(
        len(A)) if wbf__cklj not in bdt__mogqz}
    if mqgh__xuhys:
        gjx__ozv = bodo.libs.dict_arr_ext.dict_indices_arr_type
    return gen_vectorized(gezdn__inau, rjlq__wmsmm, suuy__hpko, yat__cao,
        gjx__ozv, dha__mvpb, sdu__zxkx, gah__qen, support_dict_encoding=
        False, prefix_code=butsl__uth, suffix_code=jlfb__vwjij,
        alloc_array_scalars=not stt__tdxo)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for wbf__cklj in range(len(A)):
        if isinstance(A[wbf__cklj], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], 0, container_arg=wbf__cklj, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    gezdn__inau = [f'A{wbf__cklj}' for wbf__cklj in range(len(A))]
    rjlq__wmsmm = [A[wbf__cklj] for wbf__cklj in range(len(A))]
    suuy__hpko = [False] * len(A)
    yat__cao = ''
    for wbf__cklj in range(1, len(A) - 1, 2):
        lxpgp__npai = 'if' if len(yat__cao) == 0 else 'elif'
        if A[wbf__cklj + 1] == bodo.none:
            fyv__lim = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[wbf__cklj + 1]):
            fyv__lim = (
                f'   if bodo.libs.array_kernels.isna({gezdn__inau[wbf__cklj + 1]}, i):\n'
                )
            fyv__lim += f'      bodo.libs.array_kernels.setna(res, i)\n'
            fyv__lim += f'   else:\n'
            fyv__lim += f'      res[i] = arg{wbf__cklj + 1}\n'
        else:
            fyv__lim = f'   res[i] = arg{wbf__cklj + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[wbf__cklj
            ]) or A[wbf__cklj] == bodo.none):
            if A[wbf__cklj] == bodo.none:
                yat__cao += f'{lxpgp__npai} True:\n'
                yat__cao += fyv__lim
                break
            else:
                yat__cao += f"""{lxpgp__npai} bodo.libs.array_kernels.isna({gezdn__inau[wbf__cklj]}, i):
"""
                yat__cao += fyv__lim
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[wbf__cklj]):
                yat__cao += f"""{lxpgp__npai} (bodo.libs.array_kernels.isna({gezdn__inau[0]}, i) and bodo.libs.array_kernels.isna({gezdn__inau[wbf__cklj]}, i)) or (not bodo.libs.array_kernels.isna({gezdn__inau[0]}, i) and not bodo.libs.array_kernels.isna({gezdn__inau[wbf__cklj]}, i) and arg0 == arg{wbf__cklj}):
"""
                yat__cao += fyv__lim
            elif A[wbf__cklj] == bodo.none:
                yat__cao += (
                    f'{lxpgp__npai} bodo.libs.array_kernels.isna({gezdn__inau[0]}, i):\n'
                    )
                yat__cao += fyv__lim
            else:
                yat__cao += f"""{lxpgp__npai} (not bodo.libs.array_kernels.isna({gezdn__inau[0]}, i)) and arg0 == arg{wbf__cklj}:
"""
                yat__cao += fyv__lim
        elif A[wbf__cklj] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[wbf__cklj]):
            yat__cao += f"""{lxpgp__npai} (not bodo.libs.array_kernels.isna({gezdn__inau[wbf__cklj]}, i)) and arg0 == arg{wbf__cklj}:
"""
            yat__cao += fyv__lim
        else:
            yat__cao += f'{lxpgp__npai} arg0 == arg{wbf__cklj}:\n'
            yat__cao += fyv__lim
    if len(yat__cao) > 0:
        yat__cao += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            yat__cao += (
                f'   if bodo.libs.array_kernels.isna({gezdn__inau[-1]}, i):\n')
            yat__cao += '      bodo.libs.array_kernels.setna(res, i)\n'
            yat__cao += '   else:\n'
        yat__cao += f'      res[i] = arg{len(A) - 1}'
    else:
        yat__cao += '   bodo.libs.array_kernels.setna(res, i)'
    dha__mvpb = 'A'
    sdu__zxkx = {f'A{wbf__cklj}': f'A[{wbf__cklj}]' for wbf__cklj in range(
        len(A))}
    if len(rjlq__wmsmm) % 2 == 0:
        czgia__kht = [rjlq__wmsmm[0]] + rjlq__wmsmm[1:-1:2]
        qgj__zgx = rjlq__wmsmm[2::2] + [rjlq__wmsmm[-1]]
    else:
        czgia__kht = [rjlq__wmsmm[0]] + rjlq__wmsmm[1::2]
        qgj__zgx = rjlq__wmsmm[2::2]
    rzbk__rbbq = get_common_broadcasted_type(czgia__kht, 'DECODE')
    gjx__ozv = get_common_broadcasted_type(qgj__zgx, 'DECODE')
    if gjx__ozv == bodo.none:
        gjx__ozv = rzbk__rbbq
    uvwng__etjhg = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in czgia__kht and len(rjlq__wmsmm) % 2 == 1
    return gen_vectorized(gezdn__inau, rjlq__wmsmm, suuy__hpko, yat__cao,
        gjx__ozv, dha__mvpb, sdu__zxkx, support_dict_encoding=uvwng__etjhg)


def concat_ws(A, sep):
    return


@overload(concat_ws)
def overload_concat_ws(A, sep):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('concat_ws argument must be a tuple')
    for wbf__cklj in range(len(A)):
        if isinstance(A[wbf__cklj], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
                ['A', 'sep'], 0, container_arg=wbf__cklj, container_length=
                len(A))
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
    gezdn__inau = []
    rjlq__wmsmm = []
    for wbf__cklj, oxm__ovsc in enumerate(A):
        yuifn__qjpo = f'A{wbf__cklj}'
        verify_string_arg(oxm__ovsc, 'CONCAT_WS', yuifn__qjpo)
        gezdn__inau.append(yuifn__qjpo)
        rjlq__wmsmm.append(oxm__ovsc)
    gezdn__inau.append('sep')
    verify_string_arg(sep, 'CONCAT_WS', 'sep')
    rjlq__wmsmm.append(sep)
    suuy__hpko = [True] * len(gezdn__inau)
    gjx__ozv = bodo.string_array_type
    dha__mvpb = 'A, sep'
    sdu__zxkx = {f'A{wbf__cklj}': f'A[{wbf__cklj}]' for wbf__cklj in range(
        len(A))}
    xcdn__jmjc = ','.join([f'arg{wbf__cklj}' for wbf__cklj in range(len(A))])
    yat__cao = f'  res[i] = arg{len(A)}.join([{xcdn__jmjc}])\n'
    return gen_vectorized(gezdn__inau, rjlq__wmsmm, suuy__hpko, yat__cao,
        gjx__ozv, dha__mvpb, sdu__zxkx)
