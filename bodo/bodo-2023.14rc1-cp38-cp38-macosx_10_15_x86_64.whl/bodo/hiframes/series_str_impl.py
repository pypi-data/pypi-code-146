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
        jbptp__gtqc = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(jbptp__gtqc)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mbctu__oil = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, mbctu__oil)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        vvwhy__flppr, = args
        sipiw__qlj = signature.return_type
        jmcb__bvhdu = cgutils.create_struct_proxy(sipiw__qlj)(context, builder)
        jmcb__bvhdu.obj = vvwhy__flppr
        context.nrt.incref(builder, signature.args[0], vvwhy__flppr)
        return jmcb__bvhdu._getvalue()
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(txw__izkm)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(txw__izkm, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(txw__izkm,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(txw__izkm, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    tjf__yyt = S_str.stype.data
    if (tjf__yyt != string_array_split_view_type and not is_str_arr_type(
        tjf__yyt)) and not isinstance(tjf__yyt, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(tjf__yyt, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(txw__izkm, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_get_array_impl
    if tjf__yyt == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(txw__izkm)
            yqej__jml = 0
            for qviqc__prsum in numba.parfors.parfor.internal_prange(n):
                upipi__wtd, upipi__wtd, coht__ispl = get_split_view_index(
                    txw__izkm, qviqc__prsum, i)
                yqej__jml += coht__ispl
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, yqej__jml)
            for kwk__ylrar in numba.parfors.parfor.internal_prange(n):
                fce__mgzsv, pyc__oeamh, coht__ispl = get_split_view_index(
                    txw__izkm, kwk__ylrar, i)
                if fce__mgzsv == 0:
                    bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
                    xncd__nvljy = get_split_view_data_ptr(txw__izkm, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        kwk__ylrar)
                    xncd__nvljy = get_split_view_data_ptr(txw__izkm, pyc__oeamh
                        )
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    kwk__ylrar, xncd__nvljy, coht__ispl)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(txw__izkm, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(txw__izkm)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for kwk__ylrar in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(txw__izkm, kwk__ylrar) or not len(
                txw__izkm[kwk__ylrar]) > i >= -len(txw__izkm[kwk__ylrar]):
                out_arr[kwk__ylrar] = ''
                bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
            else:
                out_arr[kwk__ylrar] = txw__izkm[kwk__ylrar][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    tjf__yyt = S_str.stype.data
    if (tjf__yyt != string_array_split_view_type and tjf__yyt !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(tjf__yyt)
        ):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(yftve__gvllr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for kwk__ylrar in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(yftve__gvllr, kwk__ylrar):
                out_arr[kwk__ylrar] = ''
                bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
            else:
                cotx__kfk = yftve__gvllr[kwk__ylrar]
                out_arr[kwk__ylrar] = sep.join(cotx__kfk)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(txw__izkm, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            pid__tqu = re.compile(pat, flags)
            zjoai__waiq = len(txw__izkm)
            out_arr = pre_alloc_string_array(zjoai__waiq, -1)
            for kwk__ylrar in numba.parfors.parfor.internal_prange(zjoai__waiq
                ):
                if bodo.libs.array_kernels.isna(txw__izkm, kwk__ylrar):
                    out_arr[kwk__ylrar] = ''
                    bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
                    continue
                out_arr[kwk__ylrar] = pid__tqu.sub(repl, txw__izkm[kwk__ylrar])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(txw__izkm)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(zjoai__waiq, -1)
        for kwk__ylrar in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(txw__izkm, kwk__ylrar):
                out_arr[kwk__ylrar] = ''
                bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
                continue
            out_arr[kwk__ylrar] = txw__izkm[kwk__ylrar].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
    bkyke__duwi = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(xam__kemf in pat) for xam__kemf in bkyke__duwi])
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
    qmck__wrs = re.IGNORECASE.value
    sfww__cki = 'def impl(\n'
    sfww__cki += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    sfww__cki += '):\n'
    sfww__cki += '  S = S_str._obj\n'
    sfww__cki += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    sfww__cki += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    sfww__cki += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sfww__cki += '  l = len(arr)\n'
    sfww__cki += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                sfww__cki += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                sfww__cki += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            sfww__cki += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        sfww__cki += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        sfww__cki += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            sfww__cki += '  upper_pat = pat.upper()\n'
        sfww__cki += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        sfww__cki += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        sfww__cki += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        sfww__cki += '      else: \n'
        if is_overload_true(case):
            sfww__cki += '          out_arr[i] = pat in arr[i]\n'
        else:
            sfww__cki += '          out_arr[i] = upper_pat in arr[i].upper()\n'
    sfww__cki += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    qnl__ozz = {}
    exec(sfww__cki, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': qmck__wrs, 'get_search_regex':
        get_search_regex}, qnl__ozz)
    impl = qnl__ozz['impl']
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
    qmck__wrs = re.IGNORECASE.value
    sfww__cki = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    sfww__cki += '        S = S_str._obj\n'
    sfww__cki += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    sfww__cki += '        l = len(arr)\n'
    sfww__cki += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    sfww__cki += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        sfww__cki += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        sfww__cki += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        sfww__cki += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        sfww__cki += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    sfww__cki += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    qnl__ozz = {}
    exec(sfww__cki, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': qmck__wrs, 'get_search_regex':
        get_search_regex}, qnl__ozz)
    impl = qnl__ozz['impl']
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
    sfww__cki = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    sfww__cki += '  S = S_str._obj\n'
    sfww__cki += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    sfww__cki += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    sfww__cki += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sfww__cki += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        sfww__cki += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})\n'
            )
    if S_str.stype.data == bodo.dict_str_arr_type and all(mlira__ezme ==
        bodo.dict_str_arr_type for mlira__ezme in others.data):
        qmm__gtb = ', '.join(f'data{i}' for i in range(len(others.columns)))
        sfww__cki += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {qmm__gtb}), sep)\n'
            )
    else:
        lykt__bhcm = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        sfww__cki += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        sfww__cki += '  numba.parfors.parfor.init_prange()\n'
        sfww__cki += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        sfww__cki += f'      if {lykt__bhcm}:\n'
        sfww__cki += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        sfww__cki += '          continue\n'
        dlzht__rpp = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        vnfdi__igel = "''" if is_overload_none(sep) else 'sep'
        sfww__cki += f'      out_arr[i] = {vnfdi__igel}.join([{dlzht__rpp}])\n'
    sfww__cki += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    qnl__ozz = {}
    exec(sfww__cki, {'bodo': bodo, 'numba': numba}, qnl__ozz)
    impl = qnl__ozz['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(txw__izkm, pat, flags)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        pid__tqu = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(zjoai__waiq, np.int64)
        for i in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(pid__tqu, yftve__gvllr[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(txw__izkm, sub, start,
                end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(zjoai__waiq, np.int64)
        for i in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = yftve__gvllr[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(txw__izkm, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(zjoai__waiq, np.int64)
        for i in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = yftve__gvllr[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(txw__izkm, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(zjoai__waiq, np.int64)
        numba.parfors.parfor.init_prange()
        rtf__ugnl = False
        for i in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = yftve__gvllr[i].find(sub, start, end)
                if out_arr[i] == -1:
                    rtf__ugnl = True
        yat__lktbk = 'substring not found' if rtf__ugnl else ''
        synchronize_error_njit('ValueError', yat__lktbk)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(txw__izkm, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(zjoai__waiq, np.int64)
        numba.parfors.parfor.init_prange()
        rtf__ugnl = False
        for i in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = yftve__gvllr[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    rtf__ugnl = True
        yat__lktbk = 'substring not found' if rtf__ugnl else ''
        synchronize_error_njit('ValueError', yat__lktbk)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(zjoai__waiq, -1)
        for kwk__ylrar in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, kwk__ylrar):
                bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
            else:
                if stop is not None:
                    onf__mzij = yftve__gvllr[kwk__ylrar][stop:]
                else:
                    onf__mzij = ''
                out_arr[kwk__ylrar] = yftve__gvllr[kwk__ylrar][:start
                    ] + repl + onf__mzij
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
                ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
                jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(txw__izkm,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    ihvr__fwer, jbptp__gtqc)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            zjoai__waiq = len(yftve__gvllr)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(zjoai__waiq,
                -1)
            for kwk__ylrar in numba.parfors.parfor.internal_prange(zjoai__waiq
                ):
                if bodo.libs.array_kernels.isna(yftve__gvllr, kwk__ylrar):
                    bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
                else:
                    out_arr[kwk__ylrar] = yftve__gvllr[kwk__ylrar] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return impl
    elif is_overload_constant_list(repeats):
        swip__rzqx = get_overload_const_list(repeats)
        dslvd__ncg = all([isinstance(rqooj__mmmja, int) for rqooj__mmmja in
            swip__rzqx])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        dslvd__ncg = True
    else:
        dslvd__ncg = False
    if dslvd__ncg:

        def impl(S_str, repeats):
            S = S_str._obj
            yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            avomb__wsftl = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            zjoai__waiq = len(yftve__gvllr)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(zjoai__waiq,
                -1)
            for kwk__ylrar in numba.parfors.parfor.internal_prange(zjoai__waiq
                ):
                if bodo.libs.array_kernels.isna(yftve__gvllr, kwk__ylrar):
                    bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
                else:
                    out_arr[kwk__ylrar] = yftve__gvllr[kwk__ylrar
                        ] * avomb__wsftl[kwk__ylrar]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    sfww__cki = f"""def dict_impl(S_str, width, fillchar=' '):
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
    qnl__ozz = {}
    njsi__hnwy = {'bodo': bodo, 'numba': numba}
    exec(sfww__cki, njsi__hnwy, qnl__ozz)
    impl = qnl__ozz['impl']
    oibij__yiu = qnl__ozz['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return oibij__yiu
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for cce__hktfq in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(cce__hktfq)
        overload_method(SeriesStrMethodType, cce__hktfq, inline='always',
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(txw__izkm, width,
                    fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(txw__izkm, width,
                    fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(txw__izkm,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(zjoai__waiq, -1)
        for kwk__ylrar in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, kwk__ylrar):
                out_arr[kwk__ylrar] = ''
                bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
            elif side == 'left':
                out_arr[kwk__ylrar] = yftve__gvllr[kwk__ylrar].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[kwk__ylrar] = yftve__gvllr[kwk__ylrar].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[kwk__ylrar] = yftve__gvllr[kwk__ylrar].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(txw__izkm, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(zjoai__waiq, -1)
        for kwk__ylrar in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, kwk__ylrar):
                out_arr[kwk__ylrar] = ''
                bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
            else:
                out_arr[kwk__ylrar] = yftve__gvllr[kwk__ylrar].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(txw__izkm, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(zjoai__waiq, -1)
        for kwk__ylrar in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, kwk__ylrar):
                out_arr[kwk__ylrar] = ''
                bodo.libs.array_kernels.setna(out_arr, kwk__ylrar)
            else:
                out_arr[kwk__ylrar] = yftve__gvllr[kwk__ylrar][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(txw__izkm, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(zjoai__waiq)
        for i in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = yftve__gvllr[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
            ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
            jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(txw__izkm, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ihvr__fwer, jbptp__gtqc)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        yftve__gvllr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jbptp__gtqc = bodo.hiframes.pd_series_ext.get_series_name(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        zjoai__waiq = len(yftve__gvllr)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(zjoai__waiq)
        for i in numba.parfors.parfor.internal_prange(zjoai__waiq):
            if bodo.libs.array_kernels.isna(yftve__gvllr, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = yftve__gvllr[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ihvr__fwer,
            jbptp__gtqc)
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
    xcoe__rykri, regex = _get_column_names_from_regex(pat, flags, 'extract')
    emqug__wezuo = len(xcoe__rykri)
    if S_str.stype.data == bodo.dict_str_arr_type:
        sfww__cki = 'def impl(S_str, pat, flags=0, expand=True):\n'
        sfww__cki += '  S = S_str._obj\n'
        sfww__cki += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        sfww__cki += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sfww__cki += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sfww__cki += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {emqug__wezuo})
"""
        for i in range(emqug__wezuo):
            sfww__cki += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        sfww__cki = 'def impl(S_str, pat, flags=0, expand=True):\n'
        sfww__cki += '  regex = re.compile(pat, flags=flags)\n'
        sfww__cki += '  S = S_str._obj\n'
        sfww__cki += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        sfww__cki += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sfww__cki += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sfww__cki += '  numba.parfors.parfor.init_prange()\n'
        sfww__cki += '  n = len(str_arr)\n'
        for i in range(emqug__wezuo):
            sfww__cki += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        sfww__cki += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        sfww__cki += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(emqug__wezuo):
            sfww__cki += "          out_arr_{}[j] = ''\n".format(i)
            sfww__cki += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        sfww__cki += '      else:\n'
        sfww__cki += '          m = regex.search(str_arr[j])\n'
        sfww__cki += '          if m:\n'
        sfww__cki += '            g = m.groups()\n'
        for i in range(emqug__wezuo):
            sfww__cki += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        sfww__cki += '          else:\n'
        for i in range(emqug__wezuo):
            sfww__cki += "            out_arr_{}[j] = ''\n".format(i)
            sfww__cki += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        jbptp__gtqc = "'{}'".format(list(regex.groupindex.keys()).pop()
            ) if len(regex.groupindex.keys()) > 0 else 'name'
        sfww__cki += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(jbptp__gtqc))
        qnl__ozz = {}
        exec(sfww__cki, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, qnl__ozz)
        impl = qnl__ozz['impl']
        return impl
    dyxek__gqebt = ', '.join('out_arr_{}'.format(i) for i in range(
        emqug__wezuo))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(sfww__cki, xcoe__rykri,
        dyxek__gqebt, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    xcoe__rykri, upipi__wtd = _get_column_names_from_regex(pat, flags,
        'extractall')
    emqug__wezuo = len(xcoe__rykri)
    pfa__nbtfi = isinstance(S_str.stype.index, StringIndexType)
    pmfys__zzig = emqug__wezuo > 1
    dbzpn__imui = '_multi' if pmfys__zzig else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        sfww__cki = 'def impl(S_str, pat, flags=0):\n'
        sfww__cki += '  S = S_str._obj\n'
        sfww__cki += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        sfww__cki += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sfww__cki += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sfww__cki += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        sfww__cki += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        sfww__cki += '  regex = re.compile(pat, flags=flags)\n'
        sfww__cki += '  out_ind_arr, out_match_arr, out_arr_list = '
        sfww__cki += f'bodo.libs.dict_arr_ext.str_extractall{dbzpn__imui}(\n'
        sfww__cki += f'arr, regex, {emqug__wezuo}, index_arr)\n'
        for i in range(emqug__wezuo):
            sfww__cki += f'  out_arr_{i} = out_arr_list[{i}]\n'
        sfww__cki += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        sfww__cki += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        sfww__cki = 'def impl(S_str, pat, flags=0):\n'
        sfww__cki += '  regex = re.compile(pat, flags=flags)\n'
        sfww__cki += '  S = S_str._obj\n'
        sfww__cki += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        sfww__cki += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sfww__cki += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sfww__cki += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        sfww__cki += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        sfww__cki += '  numba.parfors.parfor.init_prange()\n'
        sfww__cki += '  n = len(str_arr)\n'
        sfww__cki += '  out_n_l = [0]\n'
        for i in range(emqug__wezuo):
            sfww__cki += '  num_chars_{} = 0\n'.format(i)
        if pfa__nbtfi:
            sfww__cki += '  index_num_chars = 0\n'
        sfww__cki += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if pfa__nbtfi:
            sfww__cki += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        sfww__cki += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        sfww__cki += '          continue\n'
        sfww__cki += '      m = regex.findall(str_arr[i])\n'
        sfww__cki += '      out_n_l[0] += len(m)\n'
        for i in range(emqug__wezuo):
            sfww__cki += '      l_{} = 0\n'.format(i)
        sfww__cki += '      for s in m:\n'
        for i in range(emqug__wezuo):
            sfww__cki += '        l_{} += get_utf8_size(s{})\n'.format(i, 
                '[{}]'.format(i) if emqug__wezuo > 1 else '')
        for i in range(emqug__wezuo):
            sfww__cki += '      num_chars_{0} += l_{0}\n'.format(i)
        sfww__cki += (
            '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
            )
        for i in range(emqug__wezuo):
            sfww__cki += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if pfa__nbtfi:
            sfww__cki += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            sfww__cki += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
        sfww__cki += '  out_match_arr = np.empty(out_n, np.int64)\n'
        sfww__cki += '  out_ind = 0\n'
        sfww__cki += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        sfww__cki += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        sfww__cki += '          continue\n'
        sfww__cki += '      m = regex.findall(str_arr[j])\n'
        sfww__cki += '      for k, s in enumerate(m):\n'
        for i in range(emqug__wezuo):
            sfww__cki += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if emqug__wezuo > 1 else ''))
        sfww__cki += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        sfww__cki += (
            '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
            )
        sfww__cki += '        out_ind += 1\n'
        sfww__cki += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        sfww__cki += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    dyxek__gqebt = ', '.join('out_arr_{}'.format(i) for i in range(
        emqug__wezuo))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(sfww__cki, xcoe__rykri,
        dyxek__gqebt, 'out_index', extra_globals={'get_utf8_size':
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
    pgtvo__kth = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    xcoe__rykri = [pgtvo__kth.get(1 + i, i) for i in range(regex.groups)]
    return xcoe__rykri, regex


def create_str2str_methods_overload(func_name):
    qfdn__ssx = func_name in ['lstrip', 'rstrip', 'strip']
    sfww__cki = f"""def f({'S_str, to_strip=None' if qfdn__ssx else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if qfdn__ssx else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if qfdn__ssx else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    sfww__cki += f"""def _dict_impl({'S_str, to_strip=None' if qfdn__ssx else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if qfdn__ssx else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    qnl__ozz = {}
    exec(sfww__cki, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo.
        libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, qnl__ozz)
    bsdmf__alhvb = qnl__ozz['f']
    cogzz__blbmp = qnl__ozz['_dict_impl']
    if qfdn__ssx:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return cogzz__blbmp
            return bsdmf__alhvb
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return cogzz__blbmp
            return bsdmf__alhvb
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    sfww__cki = 'def dict_impl(S_str):\n'
    sfww__cki += '    S = S_str._obj\n'
    sfww__cki += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    sfww__cki += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    sfww__cki += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sfww__cki += f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n'
    sfww__cki += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    sfww__cki += 'def impl(S_str):\n'
    sfww__cki += '    S = S_str._obj\n'
    sfww__cki += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    sfww__cki += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    sfww__cki += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sfww__cki += '    numba.parfors.parfor.init_prange()\n'
    sfww__cki += '    l = len(str_arr)\n'
    sfww__cki += '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    sfww__cki += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    sfww__cki += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    sfww__cki += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    sfww__cki += '        else:\n'
    sfww__cki += '            out_arr[i] = np.bool_(str_arr[i].{}())\n'.format(
        func_name)
    sfww__cki += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    sfww__cki += '      out_arr,index, name)\n'
    qnl__ozz = {}
    exec(sfww__cki, {'bodo': bodo, 'numba': numba, 'np': np}, qnl__ozz)
    impl = qnl__ozz['impl']
    oibij__yiu = qnl__ozz['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return oibij__yiu
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for mdtv__piau in bodo.hiframes.pd_series_ext.str2str_methods:
        aqwcp__aak = create_str2str_methods_overload(mdtv__piau)
        overload_method(SeriesStrMethodType, mdtv__piau, inline='always',
            no_unliteral=True)(aqwcp__aak)


def _install_str2bool_methods():
    for mdtv__piau in bodo.hiframes.pd_series_ext.str2bool_methods:
        aqwcp__aak = create_str2bool_methods_overload(mdtv__piau)
        overload_method(SeriesStrMethodType, mdtv__piau, inline='always',
            no_unliteral=True)(aqwcp__aak)


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
        jbptp__gtqc = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(jbptp__gtqc)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mbctu__oil = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, mbctu__oil)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        vvwhy__flppr, = args
        wpko__hyfq = signature.return_type
        cxrs__okwzt = cgutils.create_struct_proxy(wpko__hyfq)(context, builder)
        cxrs__okwzt.obj = vvwhy__flppr
        context.nrt.incref(builder, signature.args[0], vvwhy__flppr)
        return cxrs__okwzt._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        txw__izkm = bodo.hiframes.pd_series_ext.get_series_data(S)
        ihvr__fwer = bodo.hiframes.pd_series_ext.get_series_index(S)
        jbptp__gtqc = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(txw__izkm),
            ihvr__fwer, jbptp__gtqc)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for kwqkl__xvli in unsupported_cat_attrs:
        myu__vuvig = 'Series.cat.' + kwqkl__xvli
        overload_attribute(SeriesCatMethodType, kwqkl__xvli)(
            create_unsupported_overload(myu__vuvig))
    for dtt__gqau in unsupported_cat_methods:
        myu__vuvig = 'Series.cat.' + dtt__gqau
        overload_method(SeriesCatMethodType, dtt__gqau)(
            create_unsupported_overload(myu__vuvig))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for dtt__gqau in unsupported_str_methods:
        myu__vuvig = 'Series.str.' + dtt__gqau
        overload_method(SeriesStrMethodType, dtt__gqau)(
            create_unsupported_overload(myu__vuvig))


_install_strseries_unsupported()
