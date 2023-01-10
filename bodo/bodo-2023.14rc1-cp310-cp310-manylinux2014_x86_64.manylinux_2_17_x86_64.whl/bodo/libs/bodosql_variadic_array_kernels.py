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
    for ovre__eln in range(len(A)):
        if isinstance(A[ovre__eln], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], 0, container_arg=ovre__eln, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    ibmge__vbi = None
    omegd__sof = []
    lan__ono = False
    for ovre__eln in range(len(A)):
        if A[ovre__eln] == bodo.none:
            omegd__sof.append(ovre__eln)
        elif not bodo.utils.utils.is_array_typ(A[ovre__eln]):
            for bdopg__skhot in range(ovre__eln + 1, len(A)):
                omegd__sof.append(bdopg__skhot)
                if bodo.utils.utils.is_array_typ(A[bdopg__skhot]):
                    ibmge__vbi = f'A[{bdopg__skhot}]'
                    lan__ono = True
            break
        else:
            lan__ono = True
    rgnhs__ese = [f'A{ovre__eln}' for ovre__eln in range(len(A)) if 
        ovre__eln not in omegd__sof]
    ldyv__jmk = [A[ovre__eln] for ovre__eln in range(len(A)) if ovre__eln
         not in omegd__sof]
    det__ztjzk = get_common_broadcasted_type(ldyv__jmk, 'COALESCE')
    thl__wsjm = lan__ono and is_str_arr_type(det__ztjzk)
    itp__oxxr = [False] * (len(A) - len(omegd__sof))
    gfalu__rokxv = False
    if thl__wsjm:
        gfalu__rokxv = True
        for bdopg__skhot, kaay__bqe in enumerate(ldyv__jmk):
            gfalu__rokxv = gfalu__rokxv and (kaay__bqe == bodo.string_type or
                kaay__bqe == bodo.dict_str_arr_type or isinstance(kaay__bqe,
                bodo.SeriesType) and kaay__bqe.data == bodo.dict_str_arr_type)
    sah__lnpi = ''
    pfbt__wvtr = True
    hpte__wjbno = False
    lkwf__ylmax = 0
    rur__yoin = None
    if gfalu__rokxv:
        rur__yoin = 'num_strings = 0\n'
        rur__yoin += 'num_chars = 0\n'
        rur__yoin += 'is_dict_global = True\n'
        for ovre__eln in range(len(A)):
            if ovre__eln in omegd__sof:
                lkwf__ylmax += 1
                continue
            elif ldyv__jmk[ovre__eln - lkwf__ylmax] != bodo.string_type:
                rur__yoin += (
                    f'old_indices{ovre__eln - lkwf__ylmax} = A{ovre__eln}._indices\n'
                    )
                rur__yoin += (
                    f'old_data{ovre__eln - lkwf__ylmax} = A{ovre__eln}._data\n'
                    )
                rur__yoin += f"""is_dict_global = is_dict_global and A{ovre__eln}._has_global_dictionary
"""
                rur__yoin += (
                    f'index_offset{ovre__eln - lkwf__ylmax} = num_strings\n')
                rur__yoin += (
                    f'num_strings += len(old_data{ovre__eln - lkwf__ylmax})\n')
                rur__yoin += f"""num_chars += bodo.libs.str_arr_ext.num_total_chars(old_data{ovre__eln - lkwf__ylmax})
"""
            else:
                rur__yoin += f'num_strings += 1\n'
                rur__yoin += (
                    f'num_chars += bodo.libs.str_ext.unicode_to_utf8_len(A{ovre__eln})\n'
                    )
    lkwf__ylmax = 0
    for ovre__eln in range(len(A)):
        if ovre__eln in omegd__sof:
            lkwf__ylmax += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[ovre__eln]):
            wyz__xqqek = 'if' if pfbt__wvtr else 'elif'
            sah__lnpi += (
                f'{wyz__xqqek} not bodo.libs.array_kernels.isna(A{ovre__eln}, i):\n'
                )
            if gfalu__rokxv:
                sah__lnpi += f"""   res[i] = old_indices{ovre__eln - lkwf__ylmax}[i] + index_offset{ovre__eln - lkwf__ylmax}
"""
            elif thl__wsjm:
                sah__lnpi += f"""   bodo.libs.str_arr_ext.get_str_arr_item_copy(res, i, A{ovre__eln}, i)
"""
            else:
                sah__lnpi += f'   res[i] = arg{ovre__eln - lkwf__ylmax}\n'
            pfbt__wvtr = False
        else:
            assert not hpte__wjbno, 'should not encounter more than one scalar due to dead column pruning'
            zsvy__csaw = ''
            if not pfbt__wvtr:
                sah__lnpi += 'else:\n'
                zsvy__csaw = '   '
            if gfalu__rokxv:
                sah__lnpi += f'{zsvy__csaw}res[i] = num_strings - 1\n'
            else:
                sah__lnpi += (
                    f'{zsvy__csaw}res[i] = arg{ovre__eln - lkwf__ylmax}\n')
            hpte__wjbno = True
            break
    if not hpte__wjbno:
        if not pfbt__wvtr:
            sah__lnpi += 'else:\n'
            sah__lnpi += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            sah__lnpi += 'bodo.libs.array_kernels.setna(res, i)'
    gwv__edf = None
    if gfalu__rokxv:
        lkwf__ylmax = 0
        gwv__edf = """dict_data = bodo.libs.str_arr_ext.pre_alloc_string_array(num_strings, num_chars)
"""
        gwv__edf += 'curr_index = 0\n'
        for ovre__eln in range(len(A)):
            if ovre__eln in omegd__sof:
                lkwf__ylmax += 1
            elif ldyv__jmk[ovre__eln - lkwf__ylmax] != bodo.string_type:
                gwv__edf += (
                    f'section_len = len(old_data{ovre__eln - lkwf__ylmax})\n')
                gwv__edf += f'for l in range(section_len):\n'
                gwv__edf += f"""    bodo.libs.str_arr_ext.get_str_arr_item_copy(dict_data, curr_index + l, old_data{ovre__eln - lkwf__ylmax}, l)
"""
                gwv__edf += f'curr_index += section_len\n'
            else:
                gwv__edf += f'dict_data[curr_index] = A{ovre__eln}\n'
                gwv__edf += f'curr_index += 1\n'
        gwv__edf += """duplicated_res = bodo.libs.dict_arr_ext.init_dict_arr(dict_data, res, is_dict_global, False)
"""
        gwv__edf += """res = bodo.libs.array.drop_duplicates_local_dictionary(duplicated_res, False)
"""
    wxt__opmio = 'A'
    pap__fgl = {f'A{ovre__eln}': f'A[{ovre__eln}]' for ovre__eln in range(
        len(A)) if ovre__eln not in omegd__sof}
    if gfalu__rokxv:
        det__ztjzk = bodo.libs.dict_arr_ext.dict_indices_arr_type
    return gen_vectorized(rgnhs__ese, ldyv__jmk, itp__oxxr, sah__lnpi,
        det__ztjzk, wxt__opmio, pap__fgl, ibmge__vbi, support_dict_encoding
        =False, prefix_code=rur__yoin, suffix_code=gwv__edf,
        alloc_array_scalars=not thl__wsjm)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for ovre__eln in range(len(A)):
        if isinstance(A[ovre__eln], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], 0, container_arg=ovre__eln, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    rgnhs__ese = [f'A{ovre__eln}' for ovre__eln in range(len(A))]
    ldyv__jmk = [A[ovre__eln] for ovre__eln in range(len(A))]
    itp__oxxr = [False] * len(A)
    sah__lnpi = ''
    for ovre__eln in range(1, len(A) - 1, 2):
        wyz__xqqek = 'if' if len(sah__lnpi) == 0 else 'elif'
        if A[ovre__eln + 1] == bodo.none:
            rhr__spvg = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[ovre__eln + 1]):
            rhr__spvg = (
                f'   if bodo.libs.array_kernels.isna({rgnhs__ese[ovre__eln + 1]}, i):\n'
                )
            rhr__spvg += f'      bodo.libs.array_kernels.setna(res, i)\n'
            rhr__spvg += f'   else:\n'
            rhr__spvg += f'      res[i] = arg{ovre__eln + 1}\n'
        else:
            rhr__spvg = f'   res[i] = arg{ovre__eln + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[ovre__eln
            ]) or A[ovre__eln] == bodo.none):
            if A[ovre__eln] == bodo.none:
                sah__lnpi += f'{wyz__xqqek} True:\n'
                sah__lnpi += rhr__spvg
                break
            else:
                sah__lnpi += f"""{wyz__xqqek} bodo.libs.array_kernels.isna({rgnhs__ese[ovre__eln]}, i):
"""
                sah__lnpi += rhr__spvg
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[ovre__eln]):
                sah__lnpi += f"""{wyz__xqqek} (bodo.libs.array_kernels.isna({rgnhs__ese[0]}, i) and bodo.libs.array_kernels.isna({rgnhs__ese[ovre__eln]}, i)) or (not bodo.libs.array_kernels.isna({rgnhs__ese[0]}, i) and not bodo.libs.array_kernels.isna({rgnhs__ese[ovre__eln]}, i) and arg0 == arg{ovre__eln}):
"""
                sah__lnpi += rhr__spvg
            elif A[ovre__eln] == bodo.none:
                sah__lnpi += (
                    f'{wyz__xqqek} bodo.libs.array_kernels.isna({rgnhs__ese[0]}, i):\n'
                    )
                sah__lnpi += rhr__spvg
            else:
                sah__lnpi += f"""{wyz__xqqek} (not bodo.libs.array_kernels.isna({rgnhs__ese[0]}, i)) and arg0 == arg{ovre__eln}:
"""
                sah__lnpi += rhr__spvg
        elif A[ovre__eln] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[ovre__eln]):
            sah__lnpi += f"""{wyz__xqqek} (not bodo.libs.array_kernels.isna({rgnhs__ese[ovre__eln]}, i)) and arg0 == arg{ovre__eln}:
"""
            sah__lnpi += rhr__spvg
        else:
            sah__lnpi += f'{wyz__xqqek} arg0 == arg{ovre__eln}:\n'
            sah__lnpi += rhr__spvg
    if len(sah__lnpi) > 0:
        sah__lnpi += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            sah__lnpi += (
                f'   if bodo.libs.array_kernels.isna({rgnhs__ese[-1]}, i):\n')
            sah__lnpi += '      bodo.libs.array_kernels.setna(res, i)\n'
            sah__lnpi += '   else:\n'
        sah__lnpi += f'      res[i] = arg{len(A) - 1}'
    else:
        sah__lnpi += '   bodo.libs.array_kernels.setna(res, i)'
    wxt__opmio = 'A'
    pap__fgl = {f'A{ovre__eln}': f'A[{ovre__eln}]' for ovre__eln in range(
        len(A))}
    if len(ldyv__jmk) % 2 == 0:
        jove__fbeum = [ldyv__jmk[0]] + ldyv__jmk[1:-1:2]
        icnbe__oobtd = ldyv__jmk[2::2] + [ldyv__jmk[-1]]
    else:
        jove__fbeum = [ldyv__jmk[0]] + ldyv__jmk[1::2]
        icnbe__oobtd = ldyv__jmk[2::2]
    rjfz__osii = get_common_broadcasted_type(jove__fbeum, 'DECODE')
    det__ztjzk = get_common_broadcasted_type(icnbe__oobtd, 'DECODE')
    if det__ztjzk == bodo.none:
        det__ztjzk = rjfz__osii
    ixzed__ckubh = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in jove__fbeum and len(ldyv__jmk) % 2 == 1
    return gen_vectorized(rgnhs__ese, ldyv__jmk, itp__oxxr, sah__lnpi,
        det__ztjzk, wxt__opmio, pap__fgl, support_dict_encoding=ixzed__ckubh)


def concat_ws(A, sep):
    return


@overload(concat_ws)
def overload_concat_ws(A, sep):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('concat_ws argument must be a tuple')
    for ovre__eln in range(len(A)):
        if isinstance(A[ovre__eln], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
                ['A', 'sep'], 0, container_arg=ovre__eln, container_length=
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
    rgnhs__ese = []
    ldyv__jmk = []
    for ovre__eln, ffqn__fwix in enumerate(A):
        jfcy__ipaal = f'A{ovre__eln}'
        verify_string_arg(ffqn__fwix, 'CONCAT_WS', jfcy__ipaal)
        rgnhs__ese.append(jfcy__ipaal)
        ldyv__jmk.append(ffqn__fwix)
    rgnhs__ese.append('sep')
    verify_string_arg(sep, 'CONCAT_WS', 'sep')
    ldyv__jmk.append(sep)
    itp__oxxr = [True] * len(rgnhs__ese)
    det__ztjzk = bodo.string_array_type
    wxt__opmio = 'A, sep'
    pap__fgl = {f'A{ovre__eln}': f'A[{ovre__eln}]' for ovre__eln in range(
        len(A))}
    sut__cfkw = ','.join([f'arg{ovre__eln}' for ovre__eln in range(len(A))])
    sah__lnpi = f'  res[i] = arg{len(A)}.join([{sut__cfkw}])\n'
    return gen_vectorized(rgnhs__ese, ldyv__jmk, itp__oxxr, sah__lnpi,
        det__ztjzk, wxt__opmio, pap__fgl)
