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
    for eft__umje in range(len(A)):
        if isinstance(A[eft__umje], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], 0, container_arg=eft__umje, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    pmhrj__lqws = None
    rndz__luadx = []
    ksfa__yhm = False
    for eft__umje in range(len(A)):
        if A[eft__umje] == bodo.none:
            rndz__luadx.append(eft__umje)
        elif not bodo.utils.utils.is_array_typ(A[eft__umje]):
            for gbhz__zzdtr in range(eft__umje + 1, len(A)):
                rndz__luadx.append(gbhz__zzdtr)
                if bodo.utils.utils.is_array_typ(A[gbhz__zzdtr]):
                    pmhrj__lqws = f'A[{gbhz__zzdtr}]'
                    ksfa__yhm = True
            break
        else:
            ksfa__yhm = True
    kcj__szk = [f'A{eft__umje}' for eft__umje in range(len(A)) if eft__umje
         not in rndz__luadx]
    rcpg__gdk = [A[eft__umje] for eft__umje in range(len(A)) if eft__umje
         not in rndz__luadx]
    ijh__uchi = get_common_broadcasted_type(rcpg__gdk, 'COALESCE')
    jze__wetel = ksfa__yhm and is_str_arr_type(ijh__uchi)
    xyxv__xsxw = [False] * (len(A) - len(rndz__luadx))
    bhb__dmq = False
    if jze__wetel:
        bhb__dmq = True
        for gbhz__zzdtr, uxe__vfsq in enumerate(rcpg__gdk):
            bhb__dmq = bhb__dmq and (uxe__vfsq == bodo.string_type or 
                uxe__vfsq == bodo.dict_str_arr_type or isinstance(uxe__vfsq,
                bodo.SeriesType) and uxe__vfsq.data == bodo.dict_str_arr_type)
    cdv__kxtrj = ''
    apnpy__huk = True
    flqw__jcrs = False
    yhqyv__gab = 0
    xgt__xzj = None
    if bhb__dmq:
        xgt__xzj = 'num_strings = 0\n'
        xgt__xzj += 'num_chars = 0\n'
        xgt__xzj += 'is_dict_global = True\n'
        for eft__umje in range(len(A)):
            if eft__umje in rndz__luadx:
                yhqyv__gab += 1
                continue
            elif rcpg__gdk[eft__umje - yhqyv__gab] != bodo.string_type:
                xgt__xzj += (
                    f'old_indices{eft__umje - yhqyv__gab} = A{eft__umje}._indices\n'
                    )
                xgt__xzj += (
                    f'old_data{eft__umje - yhqyv__gab} = A{eft__umje}._data\n')
                xgt__xzj += f"""is_dict_global = is_dict_global and A{eft__umje}._has_global_dictionary
"""
                xgt__xzj += (
                    f'index_offset{eft__umje - yhqyv__gab} = num_strings\n')
                xgt__xzj += (
                    f'num_strings += len(old_data{eft__umje - yhqyv__gab})\n')
                xgt__xzj += f"""num_chars += bodo.libs.str_arr_ext.num_total_chars(old_data{eft__umje - yhqyv__gab})
"""
            else:
                xgt__xzj += f'num_strings += 1\n'
                xgt__xzj += (
                    f'num_chars += bodo.libs.str_ext.unicode_to_utf8_len(A{eft__umje})\n'
                    )
    yhqyv__gab = 0
    for eft__umje in range(len(A)):
        if eft__umje in rndz__luadx:
            yhqyv__gab += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[eft__umje]):
            lxfoe__zwce = 'if' if apnpy__huk else 'elif'
            cdv__kxtrj += (
                f'{lxfoe__zwce} not bodo.libs.array_kernels.isna(A{eft__umje}, i):\n'
                )
            if bhb__dmq:
                cdv__kxtrj += f"""   res[i] = old_indices{eft__umje - yhqyv__gab}[i] + index_offset{eft__umje - yhqyv__gab}
"""
            elif jze__wetel:
                cdv__kxtrj += f"""   bodo.libs.str_arr_ext.get_str_arr_item_copy(res, i, A{eft__umje}, i)
"""
            else:
                cdv__kxtrj += f'   res[i] = arg{eft__umje - yhqyv__gab}\n'
            apnpy__huk = False
        else:
            assert not flqw__jcrs, 'should not encounter more than one scalar due to dead column pruning'
            omjjl__ocepq = ''
            if not apnpy__huk:
                cdv__kxtrj += 'else:\n'
                omjjl__ocepq = '   '
            if bhb__dmq:
                cdv__kxtrj += f'{omjjl__ocepq}res[i] = num_strings - 1\n'
            else:
                cdv__kxtrj += (
                    f'{omjjl__ocepq}res[i] = arg{eft__umje - yhqyv__gab}\n')
            flqw__jcrs = True
            break
    if not flqw__jcrs:
        if not apnpy__huk:
            cdv__kxtrj += 'else:\n'
            cdv__kxtrj += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            cdv__kxtrj += 'bodo.libs.array_kernels.setna(res, i)'
    dkz__gcva = None
    if bhb__dmq:
        yhqyv__gab = 0
        dkz__gcva = """dict_data = bodo.libs.str_arr_ext.pre_alloc_string_array(num_strings, num_chars)
"""
        dkz__gcva += 'curr_index = 0\n'
        for eft__umje in range(len(A)):
            if eft__umje in rndz__luadx:
                yhqyv__gab += 1
            elif rcpg__gdk[eft__umje - yhqyv__gab] != bodo.string_type:
                dkz__gcva += (
                    f'section_len = len(old_data{eft__umje - yhqyv__gab})\n')
                dkz__gcva += f'for l in range(section_len):\n'
                dkz__gcva += f"""    bodo.libs.str_arr_ext.get_str_arr_item_copy(dict_data, curr_index + l, old_data{eft__umje - yhqyv__gab}, l)
"""
                dkz__gcva += f'curr_index += section_len\n'
            else:
                dkz__gcva += f'dict_data[curr_index] = A{eft__umje}\n'
                dkz__gcva += f'curr_index += 1\n'
        dkz__gcva += """duplicated_res = bodo.libs.dict_arr_ext.init_dict_arr(dict_data, res, is_dict_global, False)
"""
        dkz__gcva += """res = bodo.libs.array.drop_duplicates_local_dictionary(duplicated_res, False)
"""
    hlm__etrny = 'A'
    ndaq__abyc = {f'A{eft__umje}': f'A[{eft__umje}]' for eft__umje in range
        (len(A)) if eft__umje not in rndz__luadx}
    if bhb__dmq:
        ijh__uchi = bodo.libs.dict_arr_ext.dict_indices_arr_type
    return gen_vectorized(kcj__szk, rcpg__gdk, xyxv__xsxw, cdv__kxtrj,
        ijh__uchi, hlm__etrny, ndaq__abyc, pmhrj__lqws,
        support_dict_encoding=False, prefix_code=xgt__xzj, suffix_code=
        dkz__gcva, alloc_array_scalars=not jze__wetel)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for eft__umje in range(len(A)):
        if isinstance(A[eft__umje], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], 0, container_arg=eft__umje, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    kcj__szk = [f'A{eft__umje}' for eft__umje in range(len(A))]
    rcpg__gdk = [A[eft__umje] for eft__umje in range(len(A))]
    xyxv__xsxw = [False] * len(A)
    cdv__kxtrj = ''
    for eft__umje in range(1, len(A) - 1, 2):
        lxfoe__zwce = 'if' if len(cdv__kxtrj) == 0 else 'elif'
        if A[eft__umje + 1] == bodo.none:
            axnh__fetvn = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[eft__umje + 1]):
            axnh__fetvn = (
                f'   if bodo.libs.array_kernels.isna({kcj__szk[eft__umje + 1]}, i):\n'
                )
            axnh__fetvn += f'      bodo.libs.array_kernels.setna(res, i)\n'
            axnh__fetvn += f'   else:\n'
            axnh__fetvn += f'      res[i] = arg{eft__umje + 1}\n'
        else:
            axnh__fetvn = f'   res[i] = arg{eft__umje + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[eft__umje
            ]) or A[eft__umje] == bodo.none):
            if A[eft__umje] == bodo.none:
                cdv__kxtrj += f'{lxfoe__zwce} True:\n'
                cdv__kxtrj += axnh__fetvn
                break
            else:
                cdv__kxtrj += f"""{lxfoe__zwce} bodo.libs.array_kernels.isna({kcj__szk[eft__umje]}, i):
"""
                cdv__kxtrj += axnh__fetvn
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[eft__umje]):
                cdv__kxtrj += f"""{lxfoe__zwce} (bodo.libs.array_kernels.isna({kcj__szk[0]}, i) and bodo.libs.array_kernels.isna({kcj__szk[eft__umje]}, i)) or (not bodo.libs.array_kernels.isna({kcj__szk[0]}, i) and not bodo.libs.array_kernels.isna({kcj__szk[eft__umje]}, i) and arg0 == arg{eft__umje}):
"""
                cdv__kxtrj += axnh__fetvn
            elif A[eft__umje] == bodo.none:
                cdv__kxtrj += (
                    f'{lxfoe__zwce} bodo.libs.array_kernels.isna({kcj__szk[0]}, i):\n'
                    )
                cdv__kxtrj += axnh__fetvn
            else:
                cdv__kxtrj += f"""{lxfoe__zwce} (not bodo.libs.array_kernels.isna({kcj__szk[0]}, i)) and arg0 == arg{eft__umje}:
"""
                cdv__kxtrj += axnh__fetvn
        elif A[eft__umje] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[eft__umje]):
            cdv__kxtrj += f"""{lxfoe__zwce} (not bodo.libs.array_kernels.isna({kcj__szk[eft__umje]}, i)) and arg0 == arg{eft__umje}:
"""
            cdv__kxtrj += axnh__fetvn
        else:
            cdv__kxtrj += f'{lxfoe__zwce} arg0 == arg{eft__umje}:\n'
            cdv__kxtrj += axnh__fetvn
    if len(cdv__kxtrj) > 0:
        cdv__kxtrj += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            cdv__kxtrj += (
                f'   if bodo.libs.array_kernels.isna({kcj__szk[-1]}, i):\n')
            cdv__kxtrj += '      bodo.libs.array_kernels.setna(res, i)\n'
            cdv__kxtrj += '   else:\n'
        cdv__kxtrj += f'      res[i] = arg{len(A) - 1}'
    else:
        cdv__kxtrj += '   bodo.libs.array_kernels.setna(res, i)'
    hlm__etrny = 'A'
    ndaq__abyc = {f'A{eft__umje}': f'A[{eft__umje}]' for eft__umje in range
        (len(A))}
    if len(rcpg__gdk) % 2 == 0:
        odg__lks = [rcpg__gdk[0]] + rcpg__gdk[1:-1:2]
        hsrg__xbds = rcpg__gdk[2::2] + [rcpg__gdk[-1]]
    else:
        odg__lks = [rcpg__gdk[0]] + rcpg__gdk[1::2]
        hsrg__xbds = rcpg__gdk[2::2]
    aokv__arlng = get_common_broadcasted_type(odg__lks, 'DECODE')
    ijh__uchi = get_common_broadcasted_type(hsrg__xbds, 'DECODE')
    if ijh__uchi == bodo.none:
        ijh__uchi = aokv__arlng
    qwfrj__qtk = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in odg__lks and len(rcpg__gdk) % 2 == 1
    return gen_vectorized(kcj__szk, rcpg__gdk, xyxv__xsxw, cdv__kxtrj,
        ijh__uchi, hlm__etrny, ndaq__abyc, support_dict_encoding=qwfrj__qtk)


def concat_ws(A, sep):
    return


@overload(concat_ws)
def overload_concat_ws(A, sep):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('concat_ws argument must be a tuple')
    for eft__umje in range(len(A)):
        if isinstance(A[eft__umje], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
                ['A', 'sep'], 0, container_arg=eft__umje, container_length=
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
    kcj__szk = []
    rcpg__gdk = []
    for eft__umje, slsf__looth in enumerate(A):
        vojwx__wkeyq = f'A{eft__umje}'
        verify_string_arg(slsf__looth, 'CONCAT_WS', vojwx__wkeyq)
        kcj__szk.append(vojwx__wkeyq)
        rcpg__gdk.append(slsf__looth)
    kcj__szk.append('sep')
    verify_string_arg(sep, 'CONCAT_WS', 'sep')
    rcpg__gdk.append(sep)
    xyxv__xsxw = [True] * len(kcj__szk)
    ijh__uchi = bodo.string_array_type
    hlm__etrny = 'A, sep'
    ndaq__abyc = {f'A{eft__umje}': f'A[{eft__umje}]' for eft__umje in range
        (len(A))}
    boq__jyy = ','.join([f'arg{eft__umje}' for eft__umje in range(len(A))])
    cdv__kxtrj = f'  res[i] = arg{len(A)}.join([{boq__jyy}])\n'
    return gen_vectorized(kcj__szk, rcpg__gdk, xyxv__xsxw, cdv__kxtrj,
        ijh__uchi, hlm__etrny, ndaq__abyc)
