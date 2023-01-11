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
        ailx__eufdj = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(ailx__eufdj)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        uqxgq__mbkc = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, uqxgq__mbkc)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        jeaue__jqm, = args
        pfoy__pibkz = signature.return_type
        vtpk__owbq = cgutils.create_struct_proxy(pfoy__pibkz)(context, builder)
        vtpk__owbq.obj = jeaue__jqm
        context.nrt.incref(builder, signature.args[0], jeaue__jqm)
        return vtpk__owbq._getvalue()
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(byact__ydb)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(byact__ydb, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(byact__ydb,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(byact__ydb, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    ghsb__pzjle = S_str.stype.data
    if (ghsb__pzjle != string_array_split_view_type and not is_str_arr_type
        (ghsb__pzjle)) and not isinstance(ghsb__pzjle, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(ghsb__pzjle, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(byact__ydb, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_get_array_impl
    if ghsb__pzjle == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(byact__ydb)
            ckfs__svtya = 0
            for yim__oqwq in numba.parfors.parfor.internal_prange(n):
                dfs__zcddf, dfs__zcddf, vdp__xkqk = get_split_view_index(
                    byact__ydb, yim__oqwq, i)
                ckfs__svtya += vdp__xkqk
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, ckfs__svtya)
            for lvzi__fjd in numba.parfors.parfor.internal_prange(n):
                skyjp__wkt, ecd__kme, vdp__xkqk = get_split_view_index(
                    byact__ydb, lvzi__fjd, i)
                if skyjp__wkt == 0:
                    bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
                    pzbq__tvos = get_split_view_data_ptr(byact__ydb, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr, lvzi__fjd
                        )
                    pzbq__tvos = get_split_view_data_ptr(byact__ydb, ecd__kme)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    lvzi__fjd, pzbq__tvos, vdp__xkqk)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(byact__ydb, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(byact__ydb)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for lvzi__fjd in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(byact__ydb, lvzi__fjd) or not len(
                byact__ydb[lvzi__fjd]) > i >= -len(byact__ydb[lvzi__fjd]):
                out_arr[lvzi__fjd] = ''
                bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
            else:
                out_arr[lvzi__fjd] = byact__ydb[lvzi__fjd][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    ghsb__pzjle = S_str.stype.data
    if (ghsb__pzjle != string_array_split_view_type and ghsb__pzjle !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        ghsb__pzjle)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(fvt__mttja)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for lvzi__fjd in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(fvt__mttja, lvzi__fjd):
                out_arr[lvzi__fjd] = ''
                bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
            else:
                xwg__odgel = fvt__mttja[lvzi__fjd]
                out_arr[lvzi__fjd] = sep.join(xwg__odgel)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(byact__ydb, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            pvhpf__gxrv = re.compile(pat, flags)
            wbpev__ibc = len(byact__ydb)
            out_arr = pre_alloc_string_array(wbpev__ibc, -1)
            for lvzi__fjd in numba.parfors.parfor.internal_prange(wbpev__ibc):
                if bodo.libs.array_kernels.isna(byact__ydb, lvzi__fjd):
                    out_arr[lvzi__fjd] = ''
                    bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
                    continue
                out_arr[lvzi__fjd] = pvhpf__gxrv.sub(repl, byact__ydb[
                    lvzi__fjd])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(byact__ydb)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(wbpev__ibc, -1)
        for lvzi__fjd in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(byact__ydb, lvzi__fjd):
                out_arr[lvzi__fjd] = ''
                bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
                continue
            out_arr[lvzi__fjd] = byact__ydb[lvzi__fjd].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
    vill__plqq = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(rten__tytz in pat) for rten__tytz in vill__plqq])
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
    wrtnn__sjc = re.IGNORECASE.value
    otolc__ron = 'def impl(\n'
    otolc__ron += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    otolc__ron += '):\n'
    otolc__ron += '  S = S_str._obj\n'
    otolc__ron += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    otolc__ron += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    otolc__ron += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    otolc__ron += '  l = len(arr)\n'
    otolc__ron += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                otolc__ron += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                otolc__ron += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            otolc__ron += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        otolc__ron += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        otolc__ron += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            otolc__ron += '  upper_pat = pat.upper()\n'
        otolc__ron += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        otolc__ron += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        otolc__ron += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        otolc__ron += '      else: \n'
        if is_overload_true(case):
            otolc__ron += '          out_arr[i] = pat in arr[i]\n'
        else:
            otolc__ron += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    otolc__ron += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zjf__indwy = {}
    exec(otolc__ron, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': wrtnn__sjc, 'get_search_regex':
        get_search_regex}, zjf__indwy)
    impl = zjf__indwy['impl']
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
    wrtnn__sjc = re.IGNORECASE.value
    otolc__ron = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    otolc__ron += '        S = S_str._obj\n'
    otolc__ron += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    otolc__ron += '        l = len(arr)\n'
    otolc__ron += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    otolc__ron += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        otolc__ron += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        otolc__ron += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        otolc__ron += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        otolc__ron += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    otolc__ron += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zjf__indwy = {}
    exec(otolc__ron, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': wrtnn__sjc, 'get_search_regex':
        get_search_regex}, zjf__indwy)
    impl = zjf__indwy['impl']
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
    otolc__ron = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    otolc__ron += '  S = S_str._obj\n'
    otolc__ron += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    otolc__ron += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    otolc__ron += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    otolc__ron += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        otolc__ron += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(tdjj__vih == bodo
        .dict_str_arr_type for tdjj__vih in others.data):
        tnllx__bjad = ', '.join(f'data{i}' for i in range(len(others.columns)))
        otolc__ron += f"""  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {tnllx__bjad}), sep)
"""
    else:
        gdcu__pugku = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        otolc__ron += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        otolc__ron += '  numba.parfors.parfor.init_prange()\n'
        otolc__ron += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        otolc__ron += f'      if {gdcu__pugku}:\n'
        otolc__ron += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        otolc__ron += '          continue\n'
        yajo__xqaz = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        ngk__fmq = "''" if is_overload_none(sep) else 'sep'
        otolc__ron += f'      out_arr[i] = {ngk__fmq}.join([{yajo__xqaz}])\n'
    otolc__ron += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zjf__indwy = {}
    exec(otolc__ron, {'bodo': bodo, 'numba': numba}, zjf__indwy)
    impl = zjf__indwy['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(byact__ydb, pat, flags)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        pvhpf__gxrv = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(wbpev__ibc, np.int64)
        for i in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(pvhpf__gxrv, fvt__mttja[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(byact__ydb, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(wbpev__ibc, np.int64)
        for i in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = fvt__mttja[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(byact__ydb, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(wbpev__ibc, np.int64)
        for i in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = fvt__mttja[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(byact__ydb, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(wbpev__ibc, np.int64)
        numba.parfors.parfor.init_prange()
        xer__zffku = False
        for i in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = fvt__mttja[i].find(sub, start, end)
                if out_arr[i] == -1:
                    xer__zffku = True
        dsir__uxsfi = 'substring not found' if xer__zffku else ''
        synchronize_error_njit('ValueError', dsir__uxsfi)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(byact__ydb, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(wbpev__ibc, np.int64)
        numba.parfors.parfor.init_prange()
        xer__zffku = False
        for i in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = fvt__mttja[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    xer__zffku = True
        dsir__uxsfi = 'substring not found' if xer__zffku else ''
        synchronize_error_njit('ValueError', dsir__uxsfi)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(wbpev__ibc, -1)
        for lvzi__fjd in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, lvzi__fjd):
                bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
            else:
                if stop is not None:
                    kdio__laht = fvt__mttja[lvzi__fjd][stop:]
                else:
                    kdio__laht = ''
                out_arr[lvzi__fjd] = fvt__mttja[lvzi__fjd][:start
                    ] + repl + kdio__laht
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
                joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
                ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(byact__ydb,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    joyp__yquvg, ailx__eufdj)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            wbpev__ibc = len(fvt__mttja)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(wbpev__ibc,
                -1)
            for lvzi__fjd in numba.parfors.parfor.internal_prange(wbpev__ibc):
                if bodo.libs.array_kernels.isna(fvt__mttja, lvzi__fjd):
                    bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
                else:
                    out_arr[lvzi__fjd] = fvt__mttja[lvzi__fjd] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return impl
    elif is_overload_constant_list(repeats):
        anj__bjhw = get_overload_const_list(repeats)
        tqq__tjp = all([isinstance(qgvlu__lbbh, int) for qgvlu__lbbh in
            anj__bjhw])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        tqq__tjp = True
    else:
        tqq__tjp = False
    if tqq__tjp:

        def impl(S_str, repeats):
            S = S_str._obj
            fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            xraf__lbvcy = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            wbpev__ibc = len(fvt__mttja)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(wbpev__ibc,
                -1)
            for lvzi__fjd in numba.parfors.parfor.internal_prange(wbpev__ibc):
                if bodo.libs.array_kernels.isna(fvt__mttja, lvzi__fjd):
                    bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
                else:
                    out_arr[lvzi__fjd] = fvt__mttja[lvzi__fjd] * xraf__lbvcy[
                        lvzi__fjd]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    otolc__ron = f"""def dict_impl(S_str, width, fillchar=' '):
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
    zjf__indwy = {}
    rly__zre = {'bodo': bodo, 'numba': numba}
    exec(otolc__ron, rly__zre, zjf__indwy)
    impl = zjf__indwy['impl']
    omg__bexfx = zjf__indwy['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return omg__bexfx
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for uwgl__ypk in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(uwgl__ypk)
        overload_method(SeriesStrMethodType, uwgl__ypk, inline='always',
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(byact__ydb,
                    width, fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(byact__ydb,
                    width, fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(byact__ydb,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(wbpev__ibc, -1)
        for lvzi__fjd in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, lvzi__fjd):
                out_arr[lvzi__fjd] = ''
                bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
            elif side == 'left':
                out_arr[lvzi__fjd] = fvt__mttja[lvzi__fjd].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[lvzi__fjd] = fvt__mttja[lvzi__fjd].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[lvzi__fjd] = fvt__mttja[lvzi__fjd].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(byact__ydb, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(wbpev__ibc, -1)
        for lvzi__fjd in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, lvzi__fjd):
                out_arr[lvzi__fjd] = ''
                bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
            else:
                out_arr[lvzi__fjd] = fvt__mttja[lvzi__fjd].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(byact__ydb, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(wbpev__ibc, -1)
        for lvzi__fjd in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, lvzi__fjd):
                out_arr[lvzi__fjd] = ''
                bodo.libs.array_kernels.setna(out_arr, lvzi__fjd)
            else:
                out_arr[lvzi__fjd] = fvt__mttja[lvzi__fjd][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(byact__ydb, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(wbpev__ibc)
        for i in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = fvt__mttja[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
            joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(byact__ydb, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                joyp__yquvg, ailx__eufdj)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        fvt__mttja = bodo.hiframes.pd_series_ext.get_series_data(S)
        ailx__eufdj = bodo.hiframes.pd_series_ext.get_series_name(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        wbpev__ibc = len(fvt__mttja)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(wbpev__ibc)
        for i in numba.parfors.parfor.internal_prange(wbpev__ibc):
            if bodo.libs.array_kernels.isna(fvt__mttja, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = fvt__mttja[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, joyp__yquvg,
            ailx__eufdj)
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
    iqif__skag, regex = _get_column_names_from_regex(pat, flags, 'extract')
    jtsze__xyudq = len(iqif__skag)
    if S_str.stype.data == bodo.dict_str_arr_type:
        otolc__ron = 'def impl(S_str, pat, flags=0, expand=True):\n'
        otolc__ron += '  S = S_str._obj\n'
        otolc__ron += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        otolc__ron += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        otolc__ron += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        otolc__ron += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {jtsze__xyudq})
"""
        for i in range(jtsze__xyudq):
            otolc__ron += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        otolc__ron = 'def impl(S_str, pat, flags=0, expand=True):\n'
        otolc__ron += '  regex = re.compile(pat, flags=flags)\n'
        otolc__ron += '  S = S_str._obj\n'
        otolc__ron += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        otolc__ron += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        otolc__ron += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        otolc__ron += '  numba.parfors.parfor.init_prange()\n'
        otolc__ron += '  n = len(str_arr)\n'
        for i in range(jtsze__xyudq):
            otolc__ron += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        otolc__ron += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        otolc__ron += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(jtsze__xyudq):
            otolc__ron += "          out_arr_{}[j] = ''\n".format(i)
            otolc__ron += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        otolc__ron += '      else:\n'
        otolc__ron += '          m = regex.search(str_arr[j])\n'
        otolc__ron += '          if m:\n'
        otolc__ron += '            g = m.groups()\n'
        for i in range(jtsze__xyudq):
            otolc__ron += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        otolc__ron += '          else:\n'
        for i in range(jtsze__xyudq):
            otolc__ron += "            out_arr_{}[j] = ''\n".format(i)
            otolc__ron += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        ailx__eufdj = "'{}'".format(list(regex.groupindex.keys()).pop()
            ) if len(regex.groupindex.keys()) > 0 else 'name'
        otolc__ron += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(ailx__eufdj))
        zjf__indwy = {}
        exec(otolc__ron, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, zjf__indwy)
        impl = zjf__indwy['impl']
        return impl
    brpl__csk = ', '.join('out_arr_{}'.format(i) for i in range(jtsze__xyudq))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(otolc__ron, iqif__skag,
        brpl__csk, 'index', extra_globals={'get_utf8_size': get_utf8_size,
        're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    iqif__skag, dfs__zcddf = _get_column_names_from_regex(pat, flags,
        'extractall')
    jtsze__xyudq = len(iqif__skag)
    hkuo__epe = isinstance(S_str.stype.index, StringIndexType)
    ebsaw__qee = jtsze__xyudq > 1
    emfxx__pdo = '_multi' if ebsaw__qee else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        otolc__ron = 'def impl(S_str, pat, flags=0):\n'
        otolc__ron += '  S = S_str._obj\n'
        otolc__ron += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        otolc__ron += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        otolc__ron += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        otolc__ron += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        otolc__ron += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        otolc__ron += '  regex = re.compile(pat, flags=flags)\n'
        otolc__ron += '  out_ind_arr, out_match_arr, out_arr_list = '
        otolc__ron += f'bodo.libs.dict_arr_ext.str_extractall{emfxx__pdo}(\n'
        otolc__ron += f'arr, regex, {jtsze__xyudq}, index_arr)\n'
        for i in range(jtsze__xyudq):
            otolc__ron += f'  out_arr_{i} = out_arr_list[{i}]\n'
        otolc__ron += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        otolc__ron += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        otolc__ron = 'def impl(S_str, pat, flags=0):\n'
        otolc__ron += '  regex = re.compile(pat, flags=flags)\n'
        otolc__ron += '  S = S_str._obj\n'
        otolc__ron += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        otolc__ron += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        otolc__ron += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        otolc__ron += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        otolc__ron += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        otolc__ron += '  numba.parfors.parfor.init_prange()\n'
        otolc__ron += '  n = len(str_arr)\n'
        otolc__ron += '  out_n_l = [0]\n'
        for i in range(jtsze__xyudq):
            otolc__ron += '  num_chars_{} = 0\n'.format(i)
        if hkuo__epe:
            otolc__ron += '  index_num_chars = 0\n'
        otolc__ron += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if hkuo__epe:
            otolc__ron += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        otolc__ron += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        otolc__ron += '          continue\n'
        otolc__ron += '      m = regex.findall(str_arr[i])\n'
        otolc__ron += '      out_n_l[0] += len(m)\n'
        for i in range(jtsze__xyudq):
            otolc__ron += '      l_{} = 0\n'.format(i)
        otolc__ron += '      for s in m:\n'
        for i in range(jtsze__xyudq):
            otolc__ron += '        l_{} += get_utf8_size(s{})\n'.format(i, 
                '[{}]'.format(i) if jtsze__xyudq > 1 else '')
        for i in range(jtsze__xyudq):
            otolc__ron += '      num_chars_{0} += l_{0}\n'.format(i)
        otolc__ron += (
            '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
            )
        for i in range(jtsze__xyudq):
            otolc__ron += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if hkuo__epe:
            otolc__ron += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            otolc__ron += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
        otolc__ron += '  out_match_arr = np.empty(out_n, np.int64)\n'
        otolc__ron += '  out_ind = 0\n'
        otolc__ron += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        otolc__ron += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        otolc__ron += '          continue\n'
        otolc__ron += '      m = regex.findall(str_arr[j])\n'
        otolc__ron += '      for k, s in enumerate(m):\n'
        for i in range(jtsze__xyudq):
            otolc__ron += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if jtsze__xyudq > 1 else ''))
        otolc__ron += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        otolc__ron += """        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)
"""
        otolc__ron += '        out_ind += 1\n'
        otolc__ron += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        otolc__ron += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    brpl__csk = ', '.join('out_arr_{}'.format(i) for i in range(jtsze__xyudq))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(otolc__ron, iqif__skag,
        brpl__csk, 'out_index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
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
    joxxo__rerbf = dict(zip(regex.groupindex.values(), regex.groupindex.keys())
        )
    iqif__skag = [joxxo__rerbf.get(1 + i, i) for i in range(regex.groups)]
    return iqif__skag, regex


def create_str2str_methods_overload(func_name):
    dphz__vxnjy = func_name in ['lstrip', 'rstrip', 'strip']
    otolc__ron = f"""def f({'S_str, to_strip=None' if dphz__vxnjy else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if dphz__vxnjy else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if dphz__vxnjy else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    otolc__ron += f"""def _dict_impl({'S_str, to_strip=None' if dphz__vxnjy else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if dphz__vxnjy else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    zjf__indwy = {}
    exec(otolc__ron, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo
        .libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, zjf__indwy)
    dje__pgb = zjf__indwy['f']
    hnwti__eqmnx = zjf__indwy['_dict_impl']
    if dphz__vxnjy:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return hnwti__eqmnx
            return dje__pgb
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return hnwti__eqmnx
            return dje__pgb
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    otolc__ron = 'def dict_impl(S_str):\n'
    otolc__ron += '    S = S_str._obj\n'
    otolc__ron += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    otolc__ron += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    otolc__ron += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    otolc__ron += (
        f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n')
    otolc__ron += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    otolc__ron += 'def impl(S_str):\n'
    otolc__ron += '    S = S_str._obj\n'
    otolc__ron += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    otolc__ron += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    otolc__ron += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    otolc__ron += '    numba.parfors.parfor.init_prange()\n'
    otolc__ron += '    l = len(str_arr)\n'
    otolc__ron += '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    otolc__ron += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    otolc__ron += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    otolc__ron += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    otolc__ron += '        else:\n'
    otolc__ron += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'.
        format(func_name))
    otolc__ron += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    otolc__ron += '      out_arr,index, name)\n'
    zjf__indwy = {}
    exec(otolc__ron, {'bodo': bodo, 'numba': numba, 'np': np}, zjf__indwy)
    impl = zjf__indwy['impl']
    omg__bexfx = zjf__indwy['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return omg__bexfx
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for wzji__dtsmf in bodo.hiframes.pd_series_ext.str2str_methods:
        irquh__qbpw = create_str2str_methods_overload(wzji__dtsmf)
        overload_method(SeriesStrMethodType, wzji__dtsmf, inline='always',
            no_unliteral=True)(irquh__qbpw)


def _install_str2bool_methods():
    for wzji__dtsmf in bodo.hiframes.pd_series_ext.str2bool_methods:
        irquh__qbpw = create_str2bool_methods_overload(wzji__dtsmf)
        overload_method(SeriesStrMethodType, wzji__dtsmf, inline='always',
            no_unliteral=True)(irquh__qbpw)


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
        ailx__eufdj = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(ailx__eufdj)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        uqxgq__mbkc = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, uqxgq__mbkc)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        jeaue__jqm, = args
        mwj__ybur = signature.return_type
        dppdn__mvxy = cgutils.create_struct_proxy(mwj__ybur)(context, builder)
        dppdn__mvxy.obj = jeaue__jqm
        context.nrt.incref(builder, signature.args[0], jeaue__jqm)
        return dppdn__mvxy._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        byact__ydb = bodo.hiframes.pd_series_ext.get_series_data(S)
        joyp__yquvg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ailx__eufdj = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(byact__ydb),
            joyp__yquvg, ailx__eufdj)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for gtn__pzhx in unsupported_cat_attrs:
        zixw__cicy = 'Series.cat.' + gtn__pzhx
        overload_attribute(SeriesCatMethodType, gtn__pzhx)(
            create_unsupported_overload(zixw__cicy))
    for opejh__wetqd in unsupported_cat_methods:
        zixw__cicy = 'Series.cat.' + opejh__wetqd
        overload_method(SeriesCatMethodType, opejh__wetqd)(
            create_unsupported_overload(zixw__cicy))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for opejh__wetqd in unsupported_str_methods:
        zixw__cicy = 'Series.str.' + opejh__wetqd
        overload_method(SeriesStrMethodType, opejh__wetqd)(
            create_unsupported_overload(zixw__cicy))


_install_strseries_unsupported()
