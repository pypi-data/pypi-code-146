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
        llww__qxoc = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(llww__qxoc)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sbl__qyd = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, sbl__qyd)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        pskpy__idim, = args
        tts__zmd = signature.return_type
        lxse__avf = cgutils.create_struct_proxy(tts__zmd)(context, builder)
        lxse__avf.obj = pskpy__idim
        context.nrt.incref(builder, signature.args[0], pskpy__idim)
        return lxse__avf._getvalue()
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(phhx__jdndl)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(phhx__jdndl, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(phhx__jdndl,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(phhx__jdndl, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    oubz__eejj = S_str.stype.data
    if (oubz__eejj != string_array_split_view_type and not is_str_arr_type(
        oubz__eejj)) and not isinstance(oubz__eejj, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(oubz__eejj, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(phhx__jdndl, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_get_array_impl
    if oubz__eejj == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(phhx__jdndl)
            agwz__vchvj = 0
            for pyg__yvuzo in numba.parfors.parfor.internal_prange(n):
                ofxz__qaq, ofxz__qaq, qurrc__gclsv = get_split_view_index(
                    phhx__jdndl, pyg__yvuzo, i)
                agwz__vchvj += qurrc__gclsv
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, agwz__vchvj)
            for pokda__gka in numba.parfors.parfor.internal_prange(n):
                olsmi__ogv, cllq__gaher, qurrc__gclsv = get_split_view_index(
                    phhx__jdndl, pokda__gka, i)
                if olsmi__ogv == 0:
                    bodo.libs.array_kernels.setna(out_arr, pokda__gka)
                    usvr__xdgal = get_split_view_data_ptr(phhx__jdndl, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        pokda__gka)
                    usvr__xdgal = get_split_view_data_ptr(phhx__jdndl,
                        cllq__gaher)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    pokda__gka, usvr__xdgal, qurrc__gclsv)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(phhx__jdndl, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(phhx__jdndl)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for pokda__gka in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(phhx__jdndl, pokda__gka
                ) or not len(phhx__jdndl[pokda__gka]) > i >= -len(phhx__jdndl
                [pokda__gka]):
                out_arr[pokda__gka] = ''
                bodo.libs.array_kernels.setna(out_arr, pokda__gka)
            else:
                out_arr[pokda__gka] = phhx__jdndl[pokda__gka][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    oubz__eejj = S_str.stype.data
    if (oubz__eejj != string_array_split_view_type and oubz__eejj !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        oubz__eejj)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(orcgn__kpnsj)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for pokda__gka in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, pokda__gka):
                out_arr[pokda__gka] = ''
                bodo.libs.array_kernels.setna(out_arr, pokda__gka)
            else:
                noy__tfaa = orcgn__kpnsj[pokda__gka]
                out_arr[pokda__gka] = sep.join(noy__tfaa)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(phhx__jdndl, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            wmhh__tuv = re.compile(pat, flags)
            drz__dcenc = len(phhx__jdndl)
            out_arr = pre_alloc_string_array(drz__dcenc, -1)
            for pokda__gka in numba.parfors.parfor.internal_prange(drz__dcenc):
                if bodo.libs.array_kernels.isna(phhx__jdndl, pokda__gka):
                    out_arr[pokda__gka] = ''
                    bodo.libs.array_kernels.setna(out_arr, pokda__gka)
                    continue
                out_arr[pokda__gka] = wmhh__tuv.sub(repl, phhx__jdndl[
                    pokda__gka])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(phhx__jdndl)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(drz__dcenc, -1)
        for pokda__gka in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(phhx__jdndl, pokda__gka):
                out_arr[pokda__gka] = ''
                bodo.libs.array_kernels.setna(out_arr, pokda__gka)
                continue
            out_arr[pokda__gka] = phhx__jdndl[pokda__gka].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
    srfx__hhlxy = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(wnap__yiy in pat) for wnap__yiy in srfx__hhlxy])
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
    vbp__figen = re.IGNORECASE.value
    qcnys__enhb = 'def impl(\n'
    qcnys__enhb += (
        '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n')
    qcnys__enhb += '):\n'
    qcnys__enhb += '  S = S_str._obj\n'
    qcnys__enhb += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    qcnys__enhb += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    qcnys__enhb += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    qcnys__enhb += '  l = len(arr)\n'
    qcnys__enhb += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                qcnys__enhb += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                qcnys__enhb += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            qcnys__enhb += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        qcnys__enhb += """  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)
"""
    else:
        qcnys__enhb += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            qcnys__enhb += '  upper_pat = pat.upper()\n'
        qcnys__enhb += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        qcnys__enhb += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        qcnys__enhb += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        qcnys__enhb += '      else: \n'
        if is_overload_true(case):
            qcnys__enhb += '          out_arr[i] = pat in arr[i]\n'
        else:
            qcnys__enhb += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    qcnys__enhb += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zvce__pyo = {}
    exec(qcnys__enhb, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': vbp__figen, 'get_search_regex':
        get_search_regex}, zvce__pyo)
    impl = zvce__pyo['impl']
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
    vbp__figen = re.IGNORECASE.value
    qcnys__enhb = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    qcnys__enhb += '        S = S_str._obj\n'
    qcnys__enhb += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    qcnys__enhb += '        l = len(arr)\n'
    qcnys__enhb += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    qcnys__enhb += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        qcnys__enhb += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        qcnys__enhb += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        qcnys__enhb += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        qcnys__enhb += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    qcnys__enhb += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zvce__pyo = {}
    exec(qcnys__enhb, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': vbp__figen, 'get_search_regex':
        get_search_regex}, zvce__pyo)
    impl = zvce__pyo['impl']
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
    qcnys__enhb = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    qcnys__enhb += '  S = S_str._obj\n'
    qcnys__enhb += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    qcnys__enhb += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    qcnys__enhb += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    qcnys__enhb += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        qcnys__enhb += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(umopg__kmwwb ==
        bodo.dict_str_arr_type for umopg__kmwwb in others.data):
        rpql__yrqx = ', '.join(f'data{i}' for i in range(len(others.columns)))
        qcnys__enhb += f"""  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {rpql__yrqx}), sep)
"""
    else:
        onfh__tkub = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        qcnys__enhb += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        qcnys__enhb += '  numba.parfors.parfor.init_prange()\n'
        qcnys__enhb += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        qcnys__enhb += f'      if {onfh__tkub}:\n'
        qcnys__enhb += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        qcnys__enhb += '          continue\n'
        qosg__mcv = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        tcs__fem = "''" if is_overload_none(sep) else 'sep'
        qcnys__enhb += f'      out_arr[i] = {tcs__fem}.join([{qosg__mcv}])\n'
    qcnys__enhb += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zvce__pyo = {}
    exec(qcnys__enhb, {'bodo': bodo, 'numba': numba}, zvce__pyo)
    impl = zvce__pyo['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(phhx__jdndl, pat, flags)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        wmhh__tuv = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(drz__dcenc, np.int64)
        for i in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(wmhh__tuv, orcgn__kpnsj[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(phhx__jdndl, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(drz__dcenc, np.int64)
        for i in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = orcgn__kpnsj[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(phhx__jdndl, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(drz__dcenc, np.int64)
        for i in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = orcgn__kpnsj[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(phhx__jdndl, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(drz__dcenc, np.int64)
        numba.parfors.parfor.init_prange()
        skr__jbk = False
        for i in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = orcgn__kpnsj[i].find(sub, start, end)
                if out_arr[i] == -1:
                    skr__jbk = True
        ntbd__qowy = 'substring not found' if skr__jbk else ''
        synchronize_error_njit('ValueError', ntbd__qowy)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(phhx__jdndl, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(drz__dcenc, np.int64)
        numba.parfors.parfor.init_prange()
        skr__jbk = False
        for i in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = orcgn__kpnsj[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    skr__jbk = True
        ntbd__qowy = 'substring not found' if skr__jbk else ''
        synchronize_error_njit('ValueError', ntbd__qowy)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(drz__dcenc, -1)
        for pokda__gka in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, pokda__gka):
                bodo.libs.array_kernels.setna(out_arr, pokda__gka)
            else:
                if stop is not None:
                    mfkp__pgzsl = orcgn__kpnsj[pokda__gka][stop:]
                else:
                    mfkp__pgzsl = ''
                out_arr[pokda__gka] = orcgn__kpnsj[pokda__gka][:start
                    ] + repl + mfkp__pgzsl
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
                pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
                llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(phhx__jdndl,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    pbncy__rtwl, llww__qxoc)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            drz__dcenc = len(orcgn__kpnsj)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(drz__dcenc,
                -1)
            for pokda__gka in numba.parfors.parfor.internal_prange(drz__dcenc):
                if bodo.libs.array_kernels.isna(orcgn__kpnsj, pokda__gka):
                    bodo.libs.array_kernels.setna(out_arr, pokda__gka)
                else:
                    out_arr[pokda__gka] = orcgn__kpnsj[pokda__gka] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return impl
    elif is_overload_constant_list(repeats):
        ojqv__zjv = get_overload_const_list(repeats)
        rnjef__ybyq = all([isinstance(dilif__qqvx, int) for dilif__qqvx in
            ojqv__zjv])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        rnjef__ybyq = True
    else:
        rnjef__ybyq = False
    if rnjef__ybyq:

        def impl(S_str, repeats):
            S = S_str._obj
            orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            goy__pox = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            drz__dcenc = len(orcgn__kpnsj)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(drz__dcenc,
                -1)
            for pokda__gka in numba.parfors.parfor.internal_prange(drz__dcenc):
                if bodo.libs.array_kernels.isna(orcgn__kpnsj, pokda__gka):
                    bodo.libs.array_kernels.setna(out_arr, pokda__gka)
                else:
                    out_arr[pokda__gka] = orcgn__kpnsj[pokda__gka] * goy__pox[
                        pokda__gka]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    qcnys__enhb = f"""def dict_impl(S_str, width, fillchar=' '):
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
    zvce__pyo = {}
    gkkn__yricm = {'bodo': bodo, 'numba': numba}
    exec(qcnys__enhb, gkkn__yricm, zvce__pyo)
    impl = zvce__pyo['impl']
    skem__ryk = zvce__pyo['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return skem__ryk
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for uub__trxsk in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(uub__trxsk)
        overload_method(SeriesStrMethodType, uub__trxsk, inline='always',
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(phhx__jdndl,
                    width, fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(phhx__jdndl,
                    width, fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(phhx__jdndl,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(drz__dcenc, -1)
        for pokda__gka in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, pokda__gka):
                out_arr[pokda__gka] = ''
                bodo.libs.array_kernels.setna(out_arr, pokda__gka)
            elif side == 'left':
                out_arr[pokda__gka] = orcgn__kpnsj[pokda__gka].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[pokda__gka] = orcgn__kpnsj[pokda__gka].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[pokda__gka] = orcgn__kpnsj[pokda__gka].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(phhx__jdndl, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(drz__dcenc, -1)
        for pokda__gka in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, pokda__gka):
                out_arr[pokda__gka] = ''
                bodo.libs.array_kernels.setna(out_arr, pokda__gka)
            else:
                out_arr[pokda__gka] = orcgn__kpnsj[pokda__gka].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(phhx__jdndl, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(drz__dcenc, -1)
        for pokda__gka in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, pokda__gka):
                out_arr[pokda__gka] = ''
                bodo.libs.array_kernels.setna(out_arr, pokda__gka)
            else:
                out_arr[pokda__gka] = orcgn__kpnsj[pokda__gka][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(phhx__jdndl,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(drz__dcenc)
        for i in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = orcgn__kpnsj[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
            pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
            llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(phhx__jdndl, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                pbncy__rtwl, llww__qxoc)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        orcgn__kpnsj = bodo.hiframes.pd_series_ext.get_series_data(S)
        llww__qxoc = bodo.hiframes.pd_series_ext.get_series_name(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        drz__dcenc = len(orcgn__kpnsj)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(drz__dcenc)
        for i in numba.parfors.parfor.internal_prange(drz__dcenc):
            if bodo.libs.array_kernels.isna(orcgn__kpnsj, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = orcgn__kpnsj[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, pbncy__rtwl,
            llww__qxoc)
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
    dslcj__iqz, regex = _get_column_names_from_regex(pat, flags, 'extract')
    aey__fuwrb = len(dslcj__iqz)
    if S_str.stype.data == bodo.dict_str_arr_type:
        qcnys__enhb = 'def impl(S_str, pat, flags=0, expand=True):\n'
        qcnys__enhb += '  S = S_str._obj\n'
        qcnys__enhb += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qcnys__enhb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qcnys__enhb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qcnys__enhb += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {aey__fuwrb})
"""
        for i in range(aey__fuwrb):
            qcnys__enhb += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        qcnys__enhb = 'def impl(S_str, pat, flags=0, expand=True):\n'
        qcnys__enhb += '  regex = re.compile(pat, flags=flags)\n'
        qcnys__enhb += '  S = S_str._obj\n'
        qcnys__enhb += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qcnys__enhb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qcnys__enhb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qcnys__enhb += '  numba.parfors.parfor.init_prange()\n'
        qcnys__enhb += '  n = len(str_arr)\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        qcnys__enhb += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        qcnys__enhb += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += "          out_arr_{}[j] = ''\n".format(i)
            qcnys__enhb += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        qcnys__enhb += '      else:\n'
        qcnys__enhb += '          m = regex.search(str_arr[j])\n'
        qcnys__enhb += '          if m:\n'
        qcnys__enhb += '            g = m.groups()\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        qcnys__enhb += '          else:\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += "            out_arr_{}[j] = ''\n".format(i)
            qcnys__enhb += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        llww__qxoc = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        qcnys__enhb += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(llww__qxoc))
        zvce__pyo = {}
        exec(qcnys__enhb, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, zvce__pyo)
        impl = zvce__pyo['impl']
        return impl
    qik__ybzi = ', '.join('out_arr_{}'.format(i) for i in range(aey__fuwrb))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(qcnys__enhb,
        dslcj__iqz, qik__ybzi, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    dslcj__iqz, ofxz__qaq = _get_column_names_from_regex(pat, flags,
        'extractall')
    aey__fuwrb = len(dslcj__iqz)
    tpxc__wujww = isinstance(S_str.stype.index, StringIndexType)
    xnkkd__dlsx = aey__fuwrb > 1
    rjs__kou = '_multi' if xnkkd__dlsx else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        qcnys__enhb = 'def impl(S_str, pat, flags=0):\n'
        qcnys__enhb += '  S = S_str._obj\n'
        qcnys__enhb += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qcnys__enhb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qcnys__enhb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qcnys__enhb += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        qcnys__enhb += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        qcnys__enhb += '  regex = re.compile(pat, flags=flags)\n'
        qcnys__enhb += '  out_ind_arr, out_match_arr, out_arr_list = '
        qcnys__enhb += f'bodo.libs.dict_arr_ext.str_extractall{rjs__kou}(\n'
        qcnys__enhb += f'arr, regex, {aey__fuwrb}, index_arr)\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += f'  out_arr_{i} = out_arr_list[{i}]\n'
        qcnys__enhb += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        qcnys__enhb += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        qcnys__enhb = 'def impl(S_str, pat, flags=0):\n'
        qcnys__enhb += '  regex = re.compile(pat, flags=flags)\n'
        qcnys__enhb += '  S = S_str._obj\n'
        qcnys__enhb += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qcnys__enhb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qcnys__enhb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qcnys__enhb += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        qcnys__enhb += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        qcnys__enhb += '  numba.parfors.parfor.init_prange()\n'
        qcnys__enhb += '  n = len(str_arr)\n'
        qcnys__enhb += '  out_n_l = [0]\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += '  num_chars_{} = 0\n'.format(i)
        if tpxc__wujww:
            qcnys__enhb += '  index_num_chars = 0\n'
        qcnys__enhb += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if tpxc__wujww:
            qcnys__enhb += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        qcnys__enhb += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        qcnys__enhb += '          continue\n'
        qcnys__enhb += '      m = regex.findall(str_arr[i])\n'
        qcnys__enhb += '      out_n_l[0] += len(m)\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += '      l_{} = 0\n'.format(i)
        qcnys__enhb += '      for s in m:\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += '        l_{} += get_utf8_size(s{})\n'.format(i,
                '[{}]'.format(i) if aey__fuwrb > 1 else '')
        for i in range(aey__fuwrb):
            qcnys__enhb += '      num_chars_{0} += l_{0}\n'.format(i)
        qcnys__enhb += """  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)
"""
        for i in range(aey__fuwrb):
            qcnys__enhb += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if tpxc__wujww:
            qcnys__enhb += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            qcnys__enhb += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
        qcnys__enhb += '  out_match_arr = np.empty(out_n, np.int64)\n'
        qcnys__enhb += '  out_ind = 0\n'
        qcnys__enhb += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        qcnys__enhb += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        qcnys__enhb += '          continue\n'
        qcnys__enhb += '      m = regex.findall(str_arr[j])\n'
        qcnys__enhb += '      for k, s in enumerate(m):\n'
        for i in range(aey__fuwrb):
            qcnys__enhb += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if aey__fuwrb > 1 else ''))
        qcnys__enhb += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        qcnys__enhb += """        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)
"""
        qcnys__enhb += '        out_ind += 1\n'
        qcnys__enhb += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        qcnys__enhb += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    qik__ybzi = ', '.join('out_arr_{}'.format(i) for i in range(aey__fuwrb))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(qcnys__enhb,
        dslcj__iqz, qik__ybzi, 'out_index', extra_globals={'get_utf8_size':
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
    jop__yoc = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    dslcj__iqz = [jop__yoc.get(1 + i, i) for i in range(regex.groups)]
    return dslcj__iqz, regex


def create_str2str_methods_overload(func_name):
    lyfnc__fdqev = func_name in ['lstrip', 'rstrip', 'strip']
    qcnys__enhb = f"""def f({'S_str, to_strip=None' if lyfnc__fdqev else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if lyfnc__fdqev else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if lyfnc__fdqev else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    qcnys__enhb += f"""def _dict_impl({'S_str, to_strip=None' if lyfnc__fdqev else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if lyfnc__fdqev else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    zvce__pyo = {}
    exec(qcnys__enhb, {'bodo': bodo, 'numba': numba, 'num_total_chars':
        bodo.libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, zvce__pyo)
    par__arr = zvce__pyo['f']
    ymwwe__uhf = zvce__pyo['_dict_impl']
    if lyfnc__fdqev:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return ymwwe__uhf
            return par__arr
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return ymwwe__uhf
            return par__arr
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    qcnys__enhb = 'def dict_impl(S_str):\n'
    qcnys__enhb += '    S = S_str._obj\n'
    qcnys__enhb += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    qcnys__enhb += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    qcnys__enhb += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    qcnys__enhb += (
        f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n')
    qcnys__enhb += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    qcnys__enhb += 'def impl(S_str):\n'
    qcnys__enhb += '    S = S_str._obj\n'
    qcnys__enhb += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    qcnys__enhb += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    qcnys__enhb += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    qcnys__enhb += '    numba.parfors.parfor.init_prange()\n'
    qcnys__enhb += '    l = len(str_arr)\n'
    qcnys__enhb += '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    qcnys__enhb += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    qcnys__enhb += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    qcnys__enhb += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    qcnys__enhb += '        else:\n'
    qcnys__enhb += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'.
        format(func_name))
    qcnys__enhb += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    qcnys__enhb += '      out_arr,index, name)\n'
    zvce__pyo = {}
    exec(qcnys__enhb, {'bodo': bodo, 'numba': numba, 'np': np}, zvce__pyo)
    impl = zvce__pyo['impl']
    skem__ryk = zvce__pyo['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return skem__ryk
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for wvsf__hzkxf in bodo.hiframes.pd_series_ext.str2str_methods:
        zbea__txwc = create_str2str_methods_overload(wvsf__hzkxf)
        overload_method(SeriesStrMethodType, wvsf__hzkxf, inline='always',
            no_unliteral=True)(zbea__txwc)


def _install_str2bool_methods():
    for wvsf__hzkxf in bodo.hiframes.pd_series_ext.str2bool_methods:
        zbea__txwc = create_str2bool_methods_overload(wvsf__hzkxf)
        overload_method(SeriesStrMethodType, wvsf__hzkxf, inline='always',
            no_unliteral=True)(zbea__txwc)


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
        llww__qxoc = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(llww__qxoc)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sbl__qyd = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, sbl__qyd)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        pskpy__idim, = args
        yqxxf__gfv = signature.return_type
        wtul__nirb = cgutils.create_struct_proxy(yqxxf__gfv)(context, builder)
        wtul__nirb.obj = pskpy__idim
        context.nrt.incref(builder, signature.args[0], pskpy__idim)
        return wtul__nirb._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        phhx__jdndl = bodo.hiframes.pd_series_ext.get_series_data(S)
        pbncy__rtwl = bodo.hiframes.pd_series_ext.get_series_index(S)
        llww__qxoc = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(phhx__jdndl),
            pbncy__rtwl, llww__qxoc)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for aoxge__chyso in unsupported_cat_attrs:
        rnqd__mym = 'Series.cat.' + aoxge__chyso
        overload_attribute(SeriesCatMethodType, aoxge__chyso)(
            create_unsupported_overload(rnqd__mym))
    for ohad__tqz in unsupported_cat_methods:
        rnqd__mym = 'Series.cat.' + ohad__tqz
        overload_method(SeriesCatMethodType, ohad__tqz)(
            create_unsupported_overload(rnqd__mym))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for ohad__tqz in unsupported_str_methods:
        rnqd__mym = 'Series.str.' + ohad__tqz
        overload_method(SeriesStrMethodType, ohad__tqz)(
            create_unsupported_overload(rnqd__mym))


_install_strseries_unsupported()
