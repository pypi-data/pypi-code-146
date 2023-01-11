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
        xpvn__wei = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(xpvn__wei)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        anyx__nfifd = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, anyx__nfifd)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        oqcn__lgd, = args
        bphy__cbaf = signature.return_type
        qhkx__bujdt = cgutils.create_struct_proxy(bphy__cbaf)(context, builder)
        qhkx__bujdt.obj = oqcn__lgd
        context.nrt.incref(builder, signature.args[0], oqcn__lgd)
        return qhkx__bujdt._getvalue()
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(iul__mak)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(iul__mak, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(iul__mak, pat
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(iul__mak, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    yhuzh__jmhrp = S_str.stype.data
    if (yhuzh__jmhrp != string_array_split_view_type and not
        is_str_arr_type(yhuzh__jmhrp)) and not isinstance(yhuzh__jmhrp,
        ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(yhuzh__jmhrp, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(iul__mak, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_get_array_impl
    if yhuzh__jmhrp == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(iul__mak)
            jqz__oyodz = 0
            for fin__rnq in numba.parfors.parfor.internal_prange(n):
                lkgqy__zqij, lkgqy__zqij, kjka__zqnue = get_split_view_index(
                    iul__mak, fin__rnq, i)
                jqz__oyodz += kjka__zqnue
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, jqz__oyodz)
            for hcw__ljizy in numba.parfors.parfor.internal_prange(n):
                bgb__jngw, tpqv__sipl, kjka__zqnue = get_split_view_index(
                    iul__mak, hcw__ljizy, i)
                if bgb__jngw == 0:
                    bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
                    bxbr__kcln = get_split_view_data_ptr(iul__mak, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        hcw__ljizy)
                    bxbr__kcln = get_split_view_data_ptr(iul__mak, tpqv__sipl)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    hcw__ljizy, bxbr__kcln, kjka__zqnue)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(iul__mak, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(iul__mak)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for hcw__ljizy in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(iul__mak, hcw__ljizy) or not len(
                iul__mak[hcw__ljizy]) > i >= -len(iul__mak[hcw__ljizy]):
                out_arr[hcw__ljizy] = ''
                bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
            else:
                out_arr[hcw__ljizy] = iul__mak[hcw__ljizy][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    yhuzh__jmhrp = S_str.stype.data
    if (yhuzh__jmhrp != string_array_split_view_type and yhuzh__jmhrp !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        yhuzh__jmhrp)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(sgmx__hjtr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for hcw__ljizy in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, hcw__ljizy):
                out_arr[hcw__ljizy] = ''
                bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
            else:
                fqtmr__trq = sgmx__hjtr[hcw__ljizy]
                out_arr[hcw__ljizy] = sep.join(fqtmr__trq)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(iul__mak, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            bvzkd__qdqb = re.compile(pat, flags)
            egli__iab = len(iul__mak)
            out_arr = pre_alloc_string_array(egli__iab, -1)
            for hcw__ljizy in numba.parfors.parfor.internal_prange(egli__iab):
                if bodo.libs.array_kernels.isna(iul__mak, hcw__ljizy):
                    out_arr[hcw__ljizy] = ''
                    bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
                    continue
                out_arr[hcw__ljizy] = bvzkd__qdqb.sub(repl, iul__mak[
                    hcw__ljizy])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(iul__mak)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(egli__iab, -1)
        for hcw__ljizy in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(iul__mak, hcw__ljizy):
                out_arr[hcw__ljizy] = ''
                bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
                continue
            out_arr[hcw__ljizy] = iul__mak[hcw__ljizy].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
    ozk__tmfp = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(pnf__ccy in pat) for pnf__ccy in ozk__tmfp])
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
    xoxg__lll = re.IGNORECASE.value
    xuvdl__lrvw = 'def impl(\n'
    xuvdl__lrvw += (
        '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n')
    xuvdl__lrvw += '):\n'
    xuvdl__lrvw += '  S = S_str._obj\n'
    xuvdl__lrvw += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    xuvdl__lrvw += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    xuvdl__lrvw += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    xuvdl__lrvw += '  l = len(arr)\n'
    xuvdl__lrvw += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                xuvdl__lrvw += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                xuvdl__lrvw += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            xuvdl__lrvw += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        xuvdl__lrvw += """  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)
"""
    else:
        xuvdl__lrvw += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            xuvdl__lrvw += '  upper_pat = pat.upper()\n'
        xuvdl__lrvw += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        xuvdl__lrvw += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        xuvdl__lrvw += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        xuvdl__lrvw += '      else: \n'
        if is_overload_true(case):
            xuvdl__lrvw += '          out_arr[i] = pat in arr[i]\n'
        else:
            xuvdl__lrvw += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    xuvdl__lrvw += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    rbvv__dud = {}
    exec(xuvdl__lrvw, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': xoxg__lll, 'get_search_regex':
        get_search_regex}, rbvv__dud)
    impl = rbvv__dud['impl']
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
    xoxg__lll = re.IGNORECASE.value
    xuvdl__lrvw = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    xuvdl__lrvw += '        S = S_str._obj\n'
    xuvdl__lrvw += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    xuvdl__lrvw += '        l = len(arr)\n'
    xuvdl__lrvw += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    xuvdl__lrvw += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        xuvdl__lrvw += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        xuvdl__lrvw += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        xuvdl__lrvw += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        xuvdl__lrvw += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    xuvdl__lrvw += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    rbvv__dud = {}
    exec(xuvdl__lrvw, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': xoxg__lll, 'get_search_regex':
        get_search_regex}, rbvv__dud)
    impl = rbvv__dud['impl']
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
    xuvdl__lrvw = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    xuvdl__lrvw += '  S = S_str._obj\n'
    xuvdl__lrvw += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    xuvdl__lrvw += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    xuvdl__lrvw += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    xuvdl__lrvw += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        xuvdl__lrvw += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(zyw__opi == bodo.
        dict_str_arr_type for zyw__opi in others.data):
        viqiz__iol = ', '.join(f'data{i}' for i in range(len(others.columns)))
        xuvdl__lrvw += f"""  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {viqiz__iol}), sep)
"""
    else:
        xrdia__btcxl = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        xuvdl__lrvw += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        xuvdl__lrvw += '  numba.parfors.parfor.init_prange()\n'
        xuvdl__lrvw += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        xuvdl__lrvw += f'      if {xrdia__btcxl}:\n'
        xuvdl__lrvw += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        xuvdl__lrvw += '          continue\n'
        srze__ozg = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        befot__oslmu = "''" if is_overload_none(sep) else 'sep'
        xuvdl__lrvw += (
            f'      out_arr[i] = {befot__oslmu}.join([{srze__ozg}])\n')
    xuvdl__lrvw += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    rbvv__dud = {}
    exec(xuvdl__lrvw, {'bodo': bodo, 'numba': numba}, rbvv__dud)
    impl = rbvv__dud['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(iul__mak, pat, flags)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        bvzkd__qdqb = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(egli__iab, np.int64)
        for i in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(bvzkd__qdqb, sgmx__hjtr[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(iul__mak, sub, start, end
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(egli__iab, np.int64)
        for i in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = sgmx__hjtr[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(iul__mak, sub, start,
                end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(egli__iab, np.int64)
        for i in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = sgmx__hjtr[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(iul__mak, sub, start,
                end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(egli__iab, np.int64)
        numba.parfors.parfor.init_prange()
        takmp__mcp = False
        for i in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = sgmx__hjtr[i].find(sub, start, end)
                if out_arr[i] == -1:
                    takmp__mcp = True
        osoe__blnxc = 'substring not found' if takmp__mcp else ''
        synchronize_error_njit('ValueError', osoe__blnxc)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(iul__mak, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(egli__iab, np.int64)
        numba.parfors.parfor.init_prange()
        takmp__mcp = False
        for i in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = sgmx__hjtr[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    takmp__mcp = True
        osoe__blnxc = 'substring not found' if takmp__mcp else ''
        synchronize_error_njit('ValueError', osoe__blnxc)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(egli__iab, -1)
        for hcw__ljizy in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, hcw__ljizy):
                bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
            else:
                if stop is not None:
                    vkoji__uamut = sgmx__hjtr[hcw__ljizy][stop:]
                else:
                    vkoji__uamut = ''
                out_arr[hcw__ljizy] = sgmx__hjtr[hcw__ljizy][:start
                    ] + repl + vkoji__uamut
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
                fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
                xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(iul__mak,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    fsw__bkna, xpvn__wei)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            egli__iab = len(sgmx__hjtr)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(egli__iab,
                -1)
            for hcw__ljizy in numba.parfors.parfor.internal_prange(egli__iab):
                if bodo.libs.array_kernels.isna(sgmx__hjtr, hcw__ljizy):
                    bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
                else:
                    out_arr[hcw__ljizy] = sgmx__hjtr[hcw__ljizy] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return impl
    elif is_overload_constant_list(repeats):
        igr__uxyy = get_overload_const_list(repeats)
        kuie__wawk = all([isinstance(aclxa__pch, int) for aclxa__pch in
            igr__uxyy])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        kuie__wawk = True
    else:
        kuie__wawk = False
    if kuie__wawk:

        def impl(S_str, repeats):
            S = S_str._obj
            sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            idln__ypet = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            egli__iab = len(sgmx__hjtr)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(egli__iab,
                -1)
            for hcw__ljizy in numba.parfors.parfor.internal_prange(egli__iab):
                if bodo.libs.array_kernels.isna(sgmx__hjtr, hcw__ljizy):
                    bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
                else:
                    out_arr[hcw__ljizy] = sgmx__hjtr[hcw__ljizy] * idln__ypet[
                        hcw__ljizy]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    xuvdl__lrvw = f"""def dict_impl(S_str, width, fillchar=' '):
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
    rbvv__dud = {}
    ntkn__beqm = {'bodo': bodo, 'numba': numba}
    exec(xuvdl__lrvw, ntkn__beqm, rbvv__dud)
    impl = rbvv__dud['impl']
    fithw__uce = rbvv__dud['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return fithw__uce
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for uhe__pnmi in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(uhe__pnmi)
        overload_method(SeriesStrMethodType, uhe__pnmi, inline='always',
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(iul__mak, width,
                    fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(iul__mak, width,
                    fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(iul__mak, width,
                    fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(egli__iab, -1)
        for hcw__ljizy in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, hcw__ljizy):
                out_arr[hcw__ljizy] = ''
                bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
            elif side == 'left':
                out_arr[hcw__ljizy] = sgmx__hjtr[hcw__ljizy].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[hcw__ljizy] = sgmx__hjtr[hcw__ljizy].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[hcw__ljizy] = sgmx__hjtr[hcw__ljizy].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(iul__mak, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(egli__iab, -1)
        for hcw__ljizy in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, hcw__ljizy):
                out_arr[hcw__ljizy] = ''
                bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
            else:
                out_arr[hcw__ljizy] = sgmx__hjtr[hcw__ljizy].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(iul__mak, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(egli__iab, -1)
        for hcw__ljizy in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, hcw__ljizy):
                out_arr[hcw__ljizy] = ''
                bodo.libs.array_kernels.setna(out_arr, hcw__ljizy)
            else:
                out_arr[hcw__ljizy] = sgmx__hjtr[hcw__ljizy][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(iul__mak, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(egli__iab)
        for i in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = sgmx__hjtr[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
            fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(iul__mak, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                fsw__bkna, xpvn__wei)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        sgmx__hjtr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xpvn__wei = bodo.hiframes.pd_series_ext.get_series_name(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        egli__iab = len(sgmx__hjtr)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(egli__iab)
        for i in numba.parfors.parfor.internal_prange(egli__iab):
            if bodo.libs.array_kernels.isna(sgmx__hjtr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = sgmx__hjtr[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, fsw__bkna,
            xpvn__wei)
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
    xgjzs__kspo, regex = _get_column_names_from_regex(pat, flags, 'extract')
    pipvv__mikqm = len(xgjzs__kspo)
    if S_str.stype.data == bodo.dict_str_arr_type:
        xuvdl__lrvw = 'def impl(S_str, pat, flags=0, expand=True):\n'
        xuvdl__lrvw += '  S = S_str._obj\n'
        xuvdl__lrvw += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xuvdl__lrvw += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xuvdl__lrvw += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        xuvdl__lrvw += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {pipvv__mikqm})
"""
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        xuvdl__lrvw = 'def impl(S_str, pat, flags=0, expand=True):\n'
        xuvdl__lrvw += '  regex = re.compile(pat, flags=flags)\n'
        xuvdl__lrvw += '  S = S_str._obj\n'
        xuvdl__lrvw += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xuvdl__lrvw += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xuvdl__lrvw += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        xuvdl__lrvw += '  numba.parfors.parfor.init_prange()\n'
        xuvdl__lrvw += '  n = len(str_arr)\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        xuvdl__lrvw += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        xuvdl__lrvw += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += "          out_arr_{}[j] = ''\n".format(i)
            xuvdl__lrvw += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        xuvdl__lrvw += '      else:\n'
        xuvdl__lrvw += '          m = regex.search(str_arr[j])\n'
        xuvdl__lrvw += '          if m:\n'
        xuvdl__lrvw += '            g = m.groups()\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        xuvdl__lrvw += '          else:\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += "            out_arr_{}[j] = ''\n".format(i)
            xuvdl__lrvw += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        xpvn__wei = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        xuvdl__lrvw += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(xpvn__wei))
        rbvv__dud = {}
        exec(xuvdl__lrvw, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, rbvv__dud)
        impl = rbvv__dud['impl']
        return impl
    rzwq__hcgp = ', '.join('out_arr_{}'.format(i) for i in range(pipvv__mikqm))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(xuvdl__lrvw,
        xgjzs__kspo, rzwq__hcgp, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    xgjzs__kspo, lkgqy__zqij = _get_column_names_from_regex(pat, flags,
        'extractall')
    pipvv__mikqm = len(xgjzs__kspo)
    gaxp__wta = isinstance(S_str.stype.index, StringIndexType)
    htc__khx = pipvv__mikqm > 1
    gzetv__aeul = '_multi' if htc__khx else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        xuvdl__lrvw = 'def impl(S_str, pat, flags=0):\n'
        xuvdl__lrvw += '  S = S_str._obj\n'
        xuvdl__lrvw += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xuvdl__lrvw += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xuvdl__lrvw += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        xuvdl__lrvw += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        xuvdl__lrvw += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        xuvdl__lrvw += '  regex = re.compile(pat, flags=flags)\n'
        xuvdl__lrvw += '  out_ind_arr, out_match_arr, out_arr_list = '
        xuvdl__lrvw += f'bodo.libs.dict_arr_ext.str_extractall{gzetv__aeul}(\n'
        xuvdl__lrvw += f'arr, regex, {pipvv__mikqm}, index_arr)\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += f'  out_arr_{i} = out_arr_list[{i}]\n'
        xuvdl__lrvw += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        xuvdl__lrvw += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        xuvdl__lrvw = 'def impl(S_str, pat, flags=0):\n'
        xuvdl__lrvw += '  regex = re.compile(pat, flags=flags)\n'
        xuvdl__lrvw += '  S = S_str._obj\n'
        xuvdl__lrvw += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        xuvdl__lrvw += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        xuvdl__lrvw += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        xuvdl__lrvw += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        xuvdl__lrvw += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        xuvdl__lrvw += '  numba.parfors.parfor.init_prange()\n'
        xuvdl__lrvw += '  n = len(str_arr)\n'
        xuvdl__lrvw += '  out_n_l = [0]\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += '  num_chars_{} = 0\n'.format(i)
        if gaxp__wta:
            xuvdl__lrvw += '  index_num_chars = 0\n'
        xuvdl__lrvw += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if gaxp__wta:
            xuvdl__lrvw += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        xuvdl__lrvw += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        xuvdl__lrvw += '          continue\n'
        xuvdl__lrvw += '      m = regex.findall(str_arr[i])\n'
        xuvdl__lrvw += '      out_n_l[0] += len(m)\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += '      l_{} = 0\n'.format(i)
        xuvdl__lrvw += '      for s in m:\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += '        l_{} += get_utf8_size(s{})\n'.format(i,
                '[{}]'.format(i) if pipvv__mikqm > 1 else '')
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += '      num_chars_{0} += l_{0}\n'.format(i)
        xuvdl__lrvw += """  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)
"""
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if gaxp__wta:
            xuvdl__lrvw += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            xuvdl__lrvw += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
        xuvdl__lrvw += '  out_match_arr = np.empty(out_n, np.int64)\n'
        xuvdl__lrvw += '  out_ind = 0\n'
        xuvdl__lrvw += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        xuvdl__lrvw += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        xuvdl__lrvw += '          continue\n'
        xuvdl__lrvw += '      m = regex.findall(str_arr[j])\n'
        xuvdl__lrvw += '      for k, s in enumerate(m):\n'
        for i in range(pipvv__mikqm):
            xuvdl__lrvw += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if pipvv__mikqm > 1 else ''))
        xuvdl__lrvw += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        xuvdl__lrvw += """        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)
"""
        xuvdl__lrvw += '        out_ind += 1\n'
        xuvdl__lrvw += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        xuvdl__lrvw += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    rzwq__hcgp = ', '.join('out_arr_{}'.format(i) for i in range(pipvv__mikqm))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(xuvdl__lrvw,
        xgjzs__kspo, rzwq__hcgp, 'out_index', extra_globals={
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
    vunb__hnx = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    xgjzs__kspo = [vunb__hnx.get(1 + i, i) for i in range(regex.groups)]
    return xgjzs__kspo, regex


def create_str2str_methods_overload(func_name):
    uokmf__pdw = func_name in ['lstrip', 'rstrip', 'strip']
    xuvdl__lrvw = f"""def f({'S_str, to_strip=None' if uokmf__pdw else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if uokmf__pdw else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if uokmf__pdw else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    xuvdl__lrvw += f"""def _dict_impl({'S_str, to_strip=None' if uokmf__pdw else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if uokmf__pdw else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    rbvv__dud = {}
    exec(xuvdl__lrvw, {'bodo': bodo, 'numba': numba, 'num_total_chars':
        bodo.libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, rbvv__dud)
    shifp__miyd = rbvv__dud['f']
    fgax__rnji = rbvv__dud['_dict_impl']
    if uokmf__pdw:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return fgax__rnji
            return shifp__miyd
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return fgax__rnji
            return shifp__miyd
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    xuvdl__lrvw = 'def dict_impl(S_str):\n'
    xuvdl__lrvw += '    S = S_str._obj\n'
    xuvdl__lrvw += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    xuvdl__lrvw += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    xuvdl__lrvw += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    xuvdl__lrvw += (
        f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n')
    xuvdl__lrvw += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xuvdl__lrvw += 'def impl(S_str):\n'
    xuvdl__lrvw += '    S = S_str._obj\n'
    xuvdl__lrvw += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    xuvdl__lrvw += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    xuvdl__lrvw += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    xuvdl__lrvw += '    numba.parfors.parfor.init_prange()\n'
    xuvdl__lrvw += '    l = len(str_arr)\n'
    xuvdl__lrvw += '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    xuvdl__lrvw += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    xuvdl__lrvw += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    xuvdl__lrvw += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    xuvdl__lrvw += '        else:\n'
    xuvdl__lrvw += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'.
        format(func_name))
    xuvdl__lrvw += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    xuvdl__lrvw += '      out_arr,index, name)\n'
    rbvv__dud = {}
    exec(xuvdl__lrvw, {'bodo': bodo, 'numba': numba, 'np': np}, rbvv__dud)
    impl = rbvv__dud['impl']
    fithw__uce = rbvv__dud['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return fithw__uce
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for vdi__nmh in bodo.hiframes.pd_series_ext.str2str_methods:
        oblb__wxi = create_str2str_methods_overload(vdi__nmh)
        overload_method(SeriesStrMethodType, vdi__nmh, inline='always',
            no_unliteral=True)(oblb__wxi)


def _install_str2bool_methods():
    for vdi__nmh in bodo.hiframes.pd_series_ext.str2bool_methods:
        oblb__wxi = create_str2bool_methods_overload(vdi__nmh)
        overload_method(SeriesStrMethodType, vdi__nmh, inline='always',
            no_unliteral=True)(oblb__wxi)


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
        xpvn__wei = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(xpvn__wei)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        anyx__nfifd = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, anyx__nfifd)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        oqcn__lgd, = args
        bijpt__zkwxj = signature.return_type
        nmdtp__kxv = cgutils.create_struct_proxy(bijpt__zkwxj)(context, builder
            )
        nmdtp__kxv.obj = oqcn__lgd
        context.nrt.incref(builder, signature.args[0], oqcn__lgd)
        return nmdtp__kxv._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        iul__mak = bodo.hiframes.pd_series_ext.get_series_data(S)
        fsw__bkna = bodo.hiframes.pd_series_ext.get_series_index(S)
        xpvn__wei = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(iul__mak),
            fsw__bkna, xpvn__wei)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for knmdn__rmb in unsupported_cat_attrs:
        zch__fbl = 'Series.cat.' + knmdn__rmb
        overload_attribute(SeriesCatMethodType, knmdn__rmb)(
            create_unsupported_overload(zch__fbl))
    for hdk__tiqe in unsupported_cat_methods:
        zch__fbl = 'Series.cat.' + hdk__tiqe
        overload_method(SeriesCatMethodType, hdk__tiqe)(
            create_unsupported_overload(zch__fbl))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for hdk__tiqe in unsupported_str_methods:
        zch__fbl = 'Series.str.' + hdk__tiqe
        overload_method(SeriesStrMethodType, hdk__tiqe)(
            create_unsupported_overload(zch__fbl))


_install_strseries_unsupported()
