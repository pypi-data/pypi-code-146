"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_bin_arr_type, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error
from bodo.utils.utils import synchronize_error_njit


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        hzz__atbpp = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(hzz__atbpp)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yhvr__pfp = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, yhvr__pfp)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        dkzg__fyt, = args
        lox__zdx = signature.return_type
        tkzng__vlwjt = cgutils.create_struct_proxy(lox__zdx)(context, builder)
        tkzng__vlwjt.obj = dkzg__fyt
        context.nrt.incref(builder, signature.args[0], dkzg__fyt)
        return tkzng__vlwjt._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not (is_str_arr_type(S.data) or S.data ==
        string_array_split_view_type or isinstance(S.data,
        ArrayItemArrayType) or is_bin_arr_type(S.data)):
        raise_bodo_error(
            'Series.str: input should be a series of string/binary or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_len_dict_impl(S_str):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(tvcna__klwi)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(tvcna__klwi, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n
        ) == -1 and S_str.stype.data == string_array_type:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(tvcna__klwi,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(tvcna__klwi, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    itidd__qjx = S_str.stype.data
    if (itidd__qjx != string_array_split_view_type and not is_str_arr_type(
        itidd__qjx)) and not isinstance(itidd__qjx, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(itidd__qjx, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(tvcna__klwi, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_get_array_impl
    if itidd__qjx == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(tvcna__klwi)
            obiub__vjf = 0
            for nggvg__bay in numba.parfors.parfor.internal_prange(n):
                yhc__eqz, yhc__eqz, qqezr__vqkkc = get_split_view_index(
                    tvcna__klwi, nggvg__bay, i)
                obiub__vjf += qqezr__vqkkc
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, obiub__vjf)
            for rpnw__rrg in numba.parfors.parfor.internal_prange(n):
                muz__ytt, zfawq__ogzm, qqezr__vqkkc = get_split_view_index(
                    tvcna__klwi, rpnw__rrg, i)
                if muz__ytt == 0:
                    bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
                    zukv__sxk = get_split_view_data_ptr(tvcna__klwi, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr, rpnw__rrg
                        )
                    zukv__sxk = get_split_view_data_ptr(tvcna__klwi,
                        zfawq__ogzm)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    rpnw__rrg, zukv__sxk, qqezr__vqkkc)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(tvcna__klwi, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(tvcna__klwi)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for rpnw__rrg in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(tvcna__klwi, rpnw__rrg) or not len(
                tvcna__klwi[rpnw__rrg]) > i >= -len(tvcna__klwi[rpnw__rrg]):
                out_arr[rpnw__rrg] = ''
                bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
            else:
                out_arr[rpnw__rrg] = tvcna__klwi[rpnw__rrg][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    itidd__qjx = S_str.stype.data
    if (itidd__qjx != string_array_split_view_type and itidd__qjx !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        itidd__qjx)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(srhur__gudzf)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for rpnw__rrg in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(srhur__gudzf, rpnw__rrg):
                out_arr[rpnw__rrg] = ''
                bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
            else:
                poxqb__tghfv = srhur__gudzf[rpnw__rrg]
                out_arr[rpnw__rrg] = sep.join(poxqb__tghfv)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_replace_dict_impl(S_str, pat, repl, n=-1, case=None, flags
            =0, regex=True):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(tvcna__klwi, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            emdb__xehki = re.compile(pat, flags)
            nxn__lfq = len(tvcna__klwi)
            out_arr = pre_alloc_string_array(nxn__lfq, -1)
            for rpnw__rrg in numba.parfors.parfor.internal_prange(nxn__lfq):
                if bodo.libs.array_kernels.isna(tvcna__klwi, rpnw__rrg):
                    out_arr[rpnw__rrg] = ''
                    bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
                    continue
                out_arr[rpnw__rrg] = emdb__xehki.sub(repl, tvcna__klwi[
                    rpnw__rrg])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(tvcna__klwi)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(nxn__lfq, -1)
        for rpnw__rrg in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(tvcna__klwi, rpnw__rrg):
                out_arr[rpnw__rrg] = ''
                bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
                continue
            out_arr[rpnw__rrg] = tvcna__klwi[rpnw__rrg].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = pd.array(S.array, 'string')._str_contains(pat, case,
            flags, na, regex)
    return out_arr


@numba.njit
def series_match_regex(S, pat, case, flags, na):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_match(pat, case, flags, na)
    return out_arr


def is_regex_unsupported(pat):
    mgzrw__azw = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(ztdnl__hxswf in pat) for ztdnl__hxswf in mgzrw__azw])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    gbajc__gwdv = re.IGNORECASE.value
    byizg__ywji = 'def impl(\n'
    byizg__ywji += (
        '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n')
    byizg__ywji += '):\n'
    byizg__ywji += '  S = S_str._obj\n'
    byizg__ywji += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    byizg__ywji += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    byizg__ywji += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    byizg__ywji += '  l = len(arr)\n'
    byizg__ywji += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                byizg__ywji += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                byizg__ywji += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            byizg__ywji += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        byizg__ywji += """  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)
"""
    else:
        byizg__ywji += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            byizg__ywji += '  upper_pat = pat.upper()\n'
        byizg__ywji += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        byizg__ywji += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        byizg__ywji += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        byizg__ywji += '      else: \n'
        if is_overload_true(case):
            byizg__ywji += '          out_arr[i] = pat in arr[i]\n'
        else:
            byizg__ywji += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    byizg__ywji += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    csjx__zvw = {}
    exec(byizg__ywji, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': gbajc__gwdv, 'get_search_regex':
        get_search_regex}, csjx__zvw)
    impl = csjx__zvw['impl']
    return impl


@overload_method(SeriesStrMethodType, 'match', inline='always',
    no_unliteral=True)
def overload_str_method_match(S_str, pat, case=True, flags=0, na=np.nan):
    not_supported_arg_check('match', 'na', na, np.nan)
    str_arg_check('match', 'pat', pat)
    int_arg_check('match', 'flags', flags)
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.match(): 'case' argument should be a constant boolean")
    gbajc__gwdv = re.IGNORECASE.value
    byizg__ywji = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    byizg__ywji += '        S = S_str._obj\n'
    byizg__ywji += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    byizg__ywji += '        l = len(arr)\n'
    byizg__ywji += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    byizg__ywji += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        byizg__ywji += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        byizg__ywji += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        byizg__ywji += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        byizg__ywji += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    byizg__ywji += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    csjx__zvw = {}
    exec(byizg__ywji, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': gbajc__gwdv, 'get_search_regex':
        get_search_regex}, csjx__zvw)
    impl = csjx__zvw['impl']
    return impl


@overload_method(SeriesStrMethodType, 'cat', no_unliteral=True)
def overload_str_method_cat(S_str, others=None, sep=None, na_rep=None, join
    ='left'):
    if not isinstance(others, DataFrameType):
        raise_bodo_error(
            "Series.str.cat(): 'others' must be a DataFrame currently")
    if not is_overload_none(sep):
        str_arg_check('cat', 'sep', sep)
    if not is_overload_constant_str(join) or get_overload_const_str(join
        ) != 'left':
        raise_bodo_error("Series.str.cat(): 'join' not supported yet")
    byizg__ywji = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    byizg__ywji += '  S = S_str._obj\n'
    byizg__ywji += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    byizg__ywji += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    byizg__ywji += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    byizg__ywji += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        byizg__ywji += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(uinmj__maobo ==
        bodo.dict_str_arr_type for uinmj__maobo in others.data):
        ijs__odtb = ', '.join(f'data{i}' for i in range(len(others.columns)))
        byizg__ywji += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {ijs__odtb}), sep)\n'
            )
    else:
        ubnnd__jdsjd = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        byizg__ywji += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        byizg__ywji += '  numba.parfors.parfor.init_prange()\n'
        byizg__ywji += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        byizg__ywji += f'      if {ubnnd__jdsjd}:\n'
        byizg__ywji += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        byizg__ywji += '          continue\n'
        wybv__crwex = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        aabka__rjb = "''" if is_overload_none(sep) else 'sep'
        byizg__ywji += (
            f'      out_arr[i] = {aabka__rjb}.join([{wybv__crwex}])\n')
    byizg__ywji += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    csjx__zvw = {}
    exec(byizg__ywji, {'bodo': bodo, 'numba': numba}, csjx__zvw)
    impl = csjx__zvw['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(tvcna__klwi, pat, flags)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        emdb__xehki = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(nxn__lfq, np.int64)
        for i in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(emdb__xehki, srhur__gudzf[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_find_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(tvcna__klwi, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(nxn__lfq, np.int64)
        for i in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = srhur__gudzf[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_rfind_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(tvcna__klwi, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(nxn__lfq, np.int64)
        for i in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = srhur__gudzf[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'index', inline='always',
    no_unliteral=True)
def overload_str_method_index(S_str, sub, start=0, end=None):
    str_arg_check('index', 'sub', sub)
    int_arg_check('index', 'start', start)
    if not is_overload_none(end):
        int_arg_check('index', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_index_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(tvcna__klwi, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(nxn__lfq, np.int64)
        numba.parfors.parfor.init_prange()
        prj__ilrfp = False
        for i in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = srhur__gudzf[i].find(sub, start, end)
                if out_arr[i] == -1:
                    prj__ilrfp = True
        wxzg__jcvfk = 'substring not found' if prj__ilrfp else ''
        synchronize_error_njit('ValueError', wxzg__jcvfk)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'rindex', inline='always',
    no_unliteral=True)
def overload_str_method_rindex(S_str, sub, start=0, end=None):
    str_arg_check('rindex', 'sub', sub)
    int_arg_check('rindex', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rindex', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_rindex_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(tvcna__klwi, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(nxn__lfq, np.int64)
        numba.parfors.parfor.init_prange()
        prj__ilrfp = False
        for i in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = srhur__gudzf[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    prj__ilrfp = True
        wxzg__jcvfk = 'substring not found' if prj__ilrfp else ''
        synchronize_error_njit('ValueError', wxzg__jcvfk)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(nxn__lfq, -1)
        for rpnw__rrg in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, rpnw__rrg):
                bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
            else:
                if stop is not None:
                    awt__zpj = srhur__gudzf[rpnw__rrg][stop:]
                else:
                    awt__zpj = ''
                out_arr[rpnw__rrg] = srhur__gudzf[rpnw__rrg][:start
                    ] + repl + awt__zpj
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
                rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
                hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(tvcna__klwi,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    rbkkj__rmm, hzz__atbpp)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            nxn__lfq = len(srhur__gudzf)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(nxn__lfq, -1
                )
            for rpnw__rrg in numba.parfors.parfor.internal_prange(nxn__lfq):
                if bodo.libs.array_kernels.isna(srhur__gudzf, rpnw__rrg):
                    bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
                else:
                    out_arr[rpnw__rrg] = srhur__gudzf[rpnw__rrg] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return impl
    elif is_overload_constant_list(repeats):
        kzor__cxl = get_overload_const_list(repeats)
        vut__lxi = all([isinstance(ufl__mlddr, int) for ufl__mlddr in
            kzor__cxl])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        vut__lxi = True
    else:
        vut__lxi = False
    if vut__lxi:

        def impl(S_str, repeats):
            S = S_str._obj
            srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            rxltk__lpdqi = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            nxn__lfq = len(srhur__gudzf)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(nxn__lfq, -1
                )
            for rpnw__rrg in numba.parfors.parfor.internal_prange(nxn__lfq):
                if bodo.libs.array_kernels.isna(srhur__gudzf, rpnw__rrg):
                    bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
                else:
                    out_arr[rpnw__rrg] = srhur__gudzf[rpnw__rrg
                        ] * rxltk__lpdqi[rpnw__rrg]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    byizg__ywji = f"""def dict_impl(S_str, width, fillchar=' '):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr, width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
def impl(S_str, width, fillchar=' '):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    numba.parfors.parfor.init_prange()
    l = len(str_arr)
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
    for j in numba.parfors.parfor.internal_prange(l):
        if bodo.libs.array_kernels.isna(str_arr, j):
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}(width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    csjx__zvw = {}
    ysq__sqh = {'bodo': bodo, 'numba': numba}
    exec(byizg__ywji, ysq__sqh, csjx__zvw)
    impl = csjx__zvw['impl']
    qppc__ovucc = csjx__zvw['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return qppc__ovucc
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for jmvy__yobkg in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(jmvy__yobkg)
        overload_method(SeriesStrMethodType, jmvy__yobkg, inline='always',
            no_unliteral=True)(impl)


_install_ljust_rjust_center()


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_pad_dict_impl(S_str, width, side='left', fillchar=' '):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(tvcna__klwi,
                    width, fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(tvcna__klwi,
                    width, fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(tvcna__klwi,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(nxn__lfq, -1)
        for rpnw__rrg in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, rpnw__rrg):
                out_arr[rpnw__rrg] = ''
                bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
            elif side == 'left':
                out_arr[rpnw__rrg] = srhur__gudzf[rpnw__rrg].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[rpnw__rrg] = srhur__gudzf[rpnw__rrg].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[rpnw__rrg] = srhur__gudzf[rpnw__rrg].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(tvcna__klwi, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(nxn__lfq, -1)
        for rpnw__rrg in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, rpnw__rrg):
                out_arr[rpnw__rrg] = ''
                bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
            else:
                out_arr[rpnw__rrg] = srhur__gudzf[rpnw__rrg].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_slice_dict_impl(S_str, start=None, stop=None, step=None):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(tvcna__klwi, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(nxn__lfq, -1)
        for rpnw__rrg in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, rpnw__rrg):
                out_arr[rpnw__rrg] = ''
                bodo.libs.array_kernels.setna(out_arr, rpnw__rrg)
            else:
                out_arr[rpnw__rrg] = srhur__gudzf[rpnw__rrg][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(tvcna__klwi,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(nxn__lfq)
        for i in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = srhur__gudzf[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
            hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(tvcna__klwi, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rbkkj__rmm, hzz__atbpp)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        srhur__gudzf = bodo.hiframes.pd_series_ext.get_series_data(S)
        hzz__atbpp = bodo.hiframes.pd_series_ext.get_series_name(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        nxn__lfq = len(srhur__gudzf)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(nxn__lfq)
        for i in numba.parfors.parfor.internal_prange(nxn__lfq):
            if bodo.libs.array_kernels.isna(srhur__gudzf, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = srhur__gudzf[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, rbkkj__rmm,
            hzz__atbpp)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    nhhqu__fbtqv, regex = _get_column_names_from_regex(pat, flags, 'extract')
    uirm__ifo = len(nhhqu__fbtqv)
    if S_str.stype.data == bodo.dict_str_arr_type:
        byizg__ywji = 'def impl(S_str, pat, flags=0, expand=True):\n'
        byizg__ywji += '  S = S_str._obj\n'
        byizg__ywji += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        byizg__ywji += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        byizg__ywji += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        byizg__ywji += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {uirm__ifo})
"""
        for i in range(uirm__ifo):
            byizg__ywji += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        byizg__ywji = 'def impl(S_str, pat, flags=0, expand=True):\n'
        byizg__ywji += '  regex = re.compile(pat, flags=flags)\n'
        byizg__ywji += '  S = S_str._obj\n'
        byizg__ywji += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        byizg__ywji += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        byizg__ywji += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        byizg__ywji += '  numba.parfors.parfor.init_prange()\n'
        byizg__ywji += '  n = len(str_arr)\n'
        for i in range(uirm__ifo):
            byizg__ywji += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        byizg__ywji += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        byizg__ywji += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(uirm__ifo):
            byizg__ywji += "          out_arr_{}[j] = ''\n".format(i)
            byizg__ywji += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        byizg__ywji += '      else:\n'
        byizg__ywji += '          m = regex.search(str_arr[j])\n'
        byizg__ywji += '          if m:\n'
        byizg__ywji += '            g = m.groups()\n'
        for i in range(uirm__ifo):
            byizg__ywji += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        byizg__ywji += '          else:\n'
        for i in range(uirm__ifo):
            byizg__ywji += "            out_arr_{}[j] = ''\n".format(i)
            byizg__ywji += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        hzz__atbpp = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        byizg__ywji += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(hzz__atbpp))
        csjx__zvw = {}
        exec(byizg__ywji, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, csjx__zvw)
        impl = csjx__zvw['impl']
        return impl
    yjz__kxyfz = ', '.join('out_arr_{}'.format(i) for i in range(uirm__ifo))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(byizg__ywji,
        nhhqu__fbtqv, yjz__kxyfz, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    nhhqu__fbtqv, yhc__eqz = _get_column_names_from_regex(pat, flags,
        'extractall')
    uirm__ifo = len(nhhqu__fbtqv)
    dhj__tqcf = isinstance(S_str.stype.index, StringIndexType)
    iaohe__srco = uirm__ifo > 1
    bqq__zlpxy = '_multi' if iaohe__srco else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        byizg__ywji = 'def impl(S_str, pat, flags=0):\n'
        byizg__ywji += '  S = S_str._obj\n'
        byizg__ywji += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        byizg__ywji += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        byizg__ywji += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        byizg__ywji += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        byizg__ywji += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        byizg__ywji += '  regex = re.compile(pat, flags=flags)\n'
        byizg__ywji += '  out_ind_arr, out_match_arr, out_arr_list = '
        byizg__ywji += f'bodo.libs.dict_arr_ext.str_extractall{bqq__zlpxy}(\n'
        byizg__ywji += f'arr, regex, {uirm__ifo}, index_arr)\n'
        for i in range(uirm__ifo):
            byizg__ywji += f'  out_arr_{i} = out_arr_list[{i}]\n'
        byizg__ywji += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        byizg__ywji += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        byizg__ywji = 'def impl(S_str, pat, flags=0):\n'
        byizg__ywji += '  regex = re.compile(pat, flags=flags)\n'
        byizg__ywji += '  S = S_str._obj\n'
        byizg__ywji += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        byizg__ywji += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        byizg__ywji += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        byizg__ywji += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        byizg__ywji += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        byizg__ywji += '  numba.parfors.parfor.init_prange()\n'
        byizg__ywji += '  n = len(str_arr)\n'
        byizg__ywji += '  out_n_l = [0]\n'
        for i in range(uirm__ifo):
            byizg__ywji += '  num_chars_{} = 0\n'.format(i)
        if dhj__tqcf:
            byizg__ywji += '  index_num_chars = 0\n'
        byizg__ywji += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if dhj__tqcf:
            byizg__ywji += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        byizg__ywji += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        byizg__ywji += '          continue\n'
        byizg__ywji += '      m = regex.findall(str_arr[i])\n'
        byizg__ywji += '      out_n_l[0] += len(m)\n'
        for i in range(uirm__ifo):
            byizg__ywji += '      l_{} = 0\n'.format(i)
        byizg__ywji += '      for s in m:\n'
        for i in range(uirm__ifo):
            byizg__ywji += '        l_{} += get_utf8_size(s{})\n'.format(i,
                '[{}]'.format(i) if uirm__ifo > 1 else '')
        for i in range(uirm__ifo):
            byizg__ywji += '      num_chars_{0} += l_{0}\n'.format(i)
        byizg__ywji += """  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)
"""
        for i in range(uirm__ifo):
            byizg__ywji += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if dhj__tqcf:
            byizg__ywji += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            byizg__ywji += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
        byizg__ywji += '  out_match_arr = np.empty(out_n, np.int64)\n'
        byizg__ywji += '  out_ind = 0\n'
        byizg__ywji += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        byizg__ywji += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        byizg__ywji += '          continue\n'
        byizg__ywji += '      m = regex.findall(str_arr[j])\n'
        byizg__ywji += '      for k, s in enumerate(m):\n'
        for i in range(uirm__ifo):
            byizg__ywji += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if uirm__ifo > 1 else ''))
        byizg__ywji += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        byizg__ywji += """        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)
"""
        byizg__ywji += '        out_ind += 1\n'
        byizg__ywji += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        byizg__ywji += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    yjz__kxyfz = ', '.join('out_arr_{}'.format(i) for i in range(uirm__ifo))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(byizg__ywji,
        nhhqu__fbtqv, yjz__kxyfz, 'out_index', extra_globals={
        'get_utf8_size': get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    qysau__pcs = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    nhhqu__fbtqv = [qysau__pcs.get(1 + i, i) for i in range(regex.groups)]
    return nhhqu__fbtqv, regex


def create_str2str_methods_overload(func_name):
    ifvn__idobn = func_name in ['lstrip', 'rstrip', 'strip']
    byizg__ywji = f"""def f({'S_str, to_strip=None' if ifvn__idobn else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if ifvn__idobn else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if ifvn__idobn else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    byizg__ywji += f"""def _dict_impl({'S_str, to_strip=None' if ifvn__idobn else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if ifvn__idobn else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    csjx__zvw = {}
    exec(byizg__ywji, {'bodo': bodo, 'numba': numba, 'num_total_chars':
        bodo.libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, csjx__zvw)
    qyr__ipj = csjx__zvw['f']
    xwxz__ieoes = csjx__zvw['_dict_impl']
    if ifvn__idobn:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return xwxz__ieoes
            return qyr__ipj
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return xwxz__ieoes
            return qyr__ipj
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    byizg__ywji = 'def dict_impl(S_str):\n'
    byizg__ywji += '    S = S_str._obj\n'
    byizg__ywji += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    byizg__ywji += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    byizg__ywji += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    byizg__ywji += (
        f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n')
    byizg__ywji += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    byizg__ywji += 'def impl(S_str):\n'
    byizg__ywji += '    S = S_str._obj\n'
    byizg__ywji += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    byizg__ywji += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    byizg__ywji += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    byizg__ywji += '    numba.parfors.parfor.init_prange()\n'
    byizg__ywji += '    l = len(str_arr)\n'
    byizg__ywji += '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    byizg__ywji += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    byizg__ywji += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    byizg__ywji += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    byizg__ywji += '        else:\n'
    byizg__ywji += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'.
        format(func_name))
    byizg__ywji += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    byizg__ywji += '      out_arr,index, name)\n'
    csjx__zvw = {}
    exec(byizg__ywji, {'bodo': bodo, 'numba': numba, 'np': np}, csjx__zvw)
    impl = csjx__zvw['impl']
    qppc__ovucc = csjx__zvw['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return qppc__ovucc
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for nptg__yupsw in bodo.hiframes.pd_series_ext.str2str_methods:
        qwcwv__voe = create_str2str_methods_overload(nptg__yupsw)
        overload_method(SeriesStrMethodType, nptg__yupsw, inline='always',
            no_unliteral=True)(qwcwv__voe)


def _install_str2bool_methods():
    for nptg__yupsw in bodo.hiframes.pd_series_ext.str2bool_methods:
        qwcwv__voe = create_str2bool_methods_overload(nptg__yupsw)
        overload_method(SeriesStrMethodType, nptg__yupsw, inline='always',
            no_unliteral=True)(qwcwv__voe)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        hzz__atbpp = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(hzz__atbpp)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yhvr__pfp = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, yhvr__pfp)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        dkzg__fyt, = args
        whze__tljdh = signature.return_type
        xumx__xkjy = cgutils.create_struct_proxy(whze__tljdh)(context, builder)
        xumx__xkjy.obj = dkzg__fyt
        context.nrt.incref(builder, signature.args[0], dkzg__fyt)
        return xumx__xkjy._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        tvcna__klwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        rbkkj__rmm = bodo.hiframes.pd_series_ext.get_series_index(S)
        hzz__atbpp = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(tvcna__klwi),
            rbkkj__rmm, hzz__atbpp)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for kylls__sdmci in unsupported_cat_attrs:
        rnzlh__mrzlm = 'Series.cat.' + kylls__sdmci
        overload_attribute(SeriesCatMethodType, kylls__sdmci)(
            create_unsupported_overload(rnzlh__mrzlm))
    for ngb__qev in unsupported_cat_methods:
        rnzlh__mrzlm = 'Series.cat.' + ngb__qev
        overload_method(SeriesCatMethodType, ngb__qev)(
            create_unsupported_overload(rnzlh__mrzlm))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for ngb__qev in unsupported_str_methods:
        rnzlh__mrzlm = 'Series.str.' + ngb__qev
        overload_method(SeriesStrMethodType, ngb__qev)(
            create_unsupported_overload(rnzlh__mrzlm))


_install_strseries_unsupported()
