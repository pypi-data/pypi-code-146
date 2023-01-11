"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type, is_series_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, convert_val_to_timestamp, pd_timestamp_tz_naive_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import unwrap_tz_array
from bodo.libs.str_arr_ext import StringArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.transform import is_var_size_item_array_type
from bodo.utils.typing import BodoError, ColNamesMetaType, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_common_scalar_dtype, get_index_names, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_nullable_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, is_str_arr_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    if isinstance(s.data, bodo.DatetimeArrayType):

        def impl(s):
            urros__yfp = bodo.hiframes.pd_series_ext.get_series_data(s)
            njlwz__qjut = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                urros__yfp)
            return njlwz__qjut
        return impl
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.tolist()')
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            sqacs__bkgi = list()
            for uxb__owxj in range(len(S)):
                sqacs__bkgi.append(S.iat[uxb__owxj])
            return sqacs__bkgi
        return impl_float

    def impl(S):
        sqacs__bkgi = list()
        for uxb__owxj in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, uxb__owxj):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            sqacs__bkgi.append(S.iat[uxb__owxj])
        return sqacs__bkgi
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    bnzlg__jio = dict(dtype=dtype, copy=copy, na_value=na_value)
    oesmf__egzqj = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    bnzlg__jio = dict(name=name, inplace=inplace)
    oesmf__egzqj = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        amgqr__osrl = ', '.join(['index_arrs[{}]'.format(uxb__owxj) for
            uxb__owxj in range(S.index.nlevels)])
    else:
        amgqr__osrl = '    bodo.utils.conversion.index_to_array(index)\n'
    ysa__ckyo = 'index' if 'index' != series_name else 'level_0'
    xcnc__kyh = get_index_names(S.index, 'Series.reset_index()', ysa__ckyo)
    columns = [name for name in xcnc__kyh]
    columns.append(series_name)
    aqhfn__qzmnw = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    aqhfn__qzmnw += (
        '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    aqhfn__qzmnw += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        aqhfn__qzmnw += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    aqhfn__qzmnw += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    aqhfn__qzmnw += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({amgqr__osrl}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    uhtrn__zzwqz = {}
    exec(aqhfn__qzmnw, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, uhtrn__zzwqz)
    cuy__zvsr = uhtrn__zzwqz['_impl']
    return cuy__zvsr


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.round()')

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        mdkot__hjs = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for uxb__owxj in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[uxb__owxj]):
                bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
            else:
                mdkot__hjs[uxb__owxj] = np.round(arr[uxb__owxj], decimals)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    bnzlg__jio = dict(level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sum(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sum(): skipna argument must be a boolean')
    if not is_overload_int(min_count):
        raise BodoError('Series.sum(): min_count argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sum()'
        )

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    bnzlg__jio = dict(level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.product(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.product(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.product()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    bnzlg__jio = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    oesmf__egzqj = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_any(A)
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.equals()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.equals()')
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        qrjwn__ssofm = bodo.hiframes.pd_series_ext.get_series_data(S)
        ihokh__ftbsy = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        zpu__atm = 0
        for uxb__owxj in numba.parfors.parfor.internal_prange(len(qrjwn__ssofm)
            ):
            oms__dwnni = 0
            vwceg__zqve = bodo.libs.array_kernels.isna(qrjwn__ssofm, uxb__owxj)
            edgm__edti = bodo.libs.array_kernels.isna(ihokh__ftbsy, uxb__owxj)
            if (vwceg__zqve and not edgm__edti or not vwceg__zqve and
                edgm__edti):
                oms__dwnni = 1
            elif not vwceg__zqve:
                if qrjwn__ssofm[uxb__owxj] != ihokh__ftbsy[uxb__owxj]:
                    oms__dwnni = 1
            zpu__atm += oms__dwnni
        return zpu__atm == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    bnzlg__jio = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    oesmf__egzqj = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    bnzlg__jio = dict(level=level)
    oesmf__egzqj = dict(level=None)
    check_unsupported_args('Series.mad', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    oyioe__votp = types.float64
    gwamy__dsqat = types.float64
    if S.dtype == types.float32:
        oyioe__votp = types.float32
        gwamy__dsqat = types.float32
    lgcug__nsxuq = oyioe__votp(0)
    suve__egrki = gwamy__dsqat(0)
    yspwb__qydl = gwamy__dsqat(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ehz__yjdua = lgcug__nsxuq
        zpu__atm = suve__egrki
        for uxb__owxj in numba.parfors.parfor.internal_prange(len(A)):
            oms__dwnni = lgcug__nsxuq
            abjx__wta = suve__egrki
            if not bodo.libs.array_kernels.isna(A, uxb__owxj) or not skipna:
                oms__dwnni = A[uxb__owxj]
                abjx__wta = yspwb__qydl
            ehz__yjdua += oms__dwnni
            zpu__atm += abjx__wta
        udoj__pqlyl = bodo.hiframes.series_kernels._mean_handle_nan(ehz__yjdua,
            zpu__atm)
        lfccn__crd = lgcug__nsxuq
        for uxb__owxj in numba.parfors.parfor.internal_prange(len(A)):
            oms__dwnni = lgcug__nsxuq
            if not bodo.libs.array_kernels.isna(A, uxb__owxj) or not skipna:
                oms__dwnni = abs(A[uxb__owxj] - udoj__pqlyl)
            lfccn__crd += oms__dwnni
        owu__tnedp = bodo.hiframes.series_kernels._mean_handle_nan(lfccn__crd,
            zpu__atm)
        return owu__tnedp
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    bnzlg__jio = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mean(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.mean()')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    bnzlg__jio = dict(level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sem(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sem(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.sem(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sem()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        jlxrx__esjfj = 0
        wzhot__afr = 0
        zpu__atm = 0
        for uxb__owxj in numba.parfors.parfor.internal_prange(len(A)):
            oms__dwnni = 0
            abjx__wta = 0
            if not bodo.libs.array_kernels.isna(A, uxb__owxj) or not skipna:
                oms__dwnni = A[uxb__owxj]
                abjx__wta = 1
            jlxrx__esjfj += oms__dwnni
            wzhot__afr += oms__dwnni * oms__dwnni
            zpu__atm += abjx__wta
        uycio__timmu = (bodo.hiframes.series_kernels.
            _compute_var_nan_count_ddof(jlxrx__esjfj, wzhot__afr, zpu__atm,
            ddof))
        cky__ttdi = bodo.hiframes.series_kernels._sem_handle_nan(uycio__timmu,
            zpu__atm)
        return cky__ttdi
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    bnzlg__jio = dict(level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.kurtosis(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError(
            "Series.kurtosis(): 'skipna' argument must be a boolean")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.kurtosis()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        jlxrx__esjfj = 0.0
        wzhot__afr = 0.0
        ytg__ntktx = 0.0
        zmkm__xzvhe = 0.0
        zpu__atm = 0
        for uxb__owxj in numba.parfors.parfor.internal_prange(len(A)):
            oms__dwnni = 0.0
            abjx__wta = 0
            if not bodo.libs.array_kernels.isna(A, uxb__owxj) or not skipna:
                oms__dwnni = np.float64(A[uxb__owxj])
                abjx__wta = 1
            jlxrx__esjfj += oms__dwnni
            wzhot__afr += oms__dwnni ** 2
            ytg__ntktx += oms__dwnni ** 3
            zmkm__xzvhe += oms__dwnni ** 4
            zpu__atm += abjx__wta
        uycio__timmu = bodo.hiframes.series_kernels.compute_kurt(jlxrx__esjfj,
            wzhot__afr, ytg__ntktx, zmkm__xzvhe, zpu__atm)
        return uycio__timmu
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    bnzlg__jio = dict(level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.skew()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        jlxrx__esjfj = 0.0
        wzhot__afr = 0.0
        ytg__ntktx = 0.0
        zpu__atm = 0
        for uxb__owxj in numba.parfors.parfor.internal_prange(len(A)):
            oms__dwnni = 0.0
            abjx__wta = 0
            if not bodo.libs.array_kernels.isna(A, uxb__owxj) or not skipna:
                oms__dwnni = np.float64(A[uxb__owxj])
                abjx__wta = 1
            jlxrx__esjfj += oms__dwnni
            wzhot__afr += oms__dwnni ** 2
            ytg__ntktx += oms__dwnni ** 3
            zpu__atm += abjx__wta
        uycio__timmu = bodo.hiframes.series_kernels.compute_skew(jlxrx__esjfj,
            wzhot__afr, ytg__ntktx, zpu__atm)
        return uycio__timmu
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    bnzlg__jio = dict(level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.var(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.var(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.var(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.var()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    bnzlg__jio = dict(level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.std(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.std(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.std(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.std()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.dot()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.dot()')

    def impl(S, other):
        qrjwn__ssofm = bodo.hiframes.pd_series_ext.get_series_data(S)
        ihokh__ftbsy = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        wkuz__kkyy = 0
        for uxb__owxj in numba.parfors.parfor.internal_prange(len(qrjwn__ssofm)
            ):
            vqjrj__lga = qrjwn__ssofm[uxb__owxj]
            hpse__uep = ihokh__ftbsy[uxb__owxj]
            wkuz__kkyy += vqjrj__lga * hpse__uep
        return wkuz__kkyy
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    bnzlg__jio = dict(skipna=skipna)
    oesmf__egzqj = dict(skipna=True)
    check_unsupported_args('Series.cumsum', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumsum(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumsum()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(A, 'cumsum'), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=None, skipna=True):
    bnzlg__jio = dict(skipna=skipna)
    oesmf__egzqj = dict(skipna=True)
    check_unsupported_args('Series.cumprod', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumprod(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumprod()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(A, 'cumprod'), index, name)
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=None, skipna=True):
    bnzlg__jio = dict(skipna=skipna)
    oesmf__egzqj = dict(skipna=True)
    check_unsupported_args('Series.cummin', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummin(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummin()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(arr, 'cummin'), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=None, skipna=True):
    bnzlg__jio = dict(skipna=skipna)
    oesmf__egzqj = dict(skipna=True)
    check_unsupported_args('Series.cummax', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummax(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummax()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(arr, 'cummax'), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    bnzlg__jio = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    oesmf__egzqj = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        raox__qfq = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, raox__qfq, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    bnzlg__jio = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    oesmf__egzqj = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if is_overload_none(mapper) or not is_scalar_type(mapper):
        raise BodoError(
            "Series.rename_axis(): 'mapper' is required and must be a scalar type."
            )

    def impl(S, mapper=None, index=None, columns=None, axis=None, copy=True,
        inplace=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        index = index.rename(mapper)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.abs()'
        )
    flte__xbnh = S.data

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(A)
        mdkot__hjs = bodo.utils.utils.alloc_type(n, flte__xbnh, (-1,))
        for uxb__owxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, uxb__owxj):
                bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                continue
            mdkot__hjs[uxb__owxj] = np.abs(A[uxb__owxj])
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    bnzlg__jio = dict(level=level)
    oesmf__egzqj = dict(level=None)
    check_unsupported_args('Series.count', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    bnzlg__jio = dict(method=method, min_periods=min_periods)
    oesmf__egzqj = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        mvla__efrmo = S.sum()
        myskm__vxvyb = other.sum()
        a = n * (S * other).sum() - mvla__efrmo * myskm__vxvyb
        uair__msqgz = n * (S ** 2).sum() - mvla__efrmo ** 2
        xoee__jonrc = n * (other ** 2).sum() - myskm__vxvyb ** 2
        return a / np.sqrt(uair__msqgz * xoee__jonrc)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    bnzlg__jio = dict(min_periods=min_periods)
    oesmf__egzqj = dict(min_periods=None)
    check_unsupported_args('Series.cov', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        mvla__efrmo = S.mean()
        myskm__vxvyb = other.mean()
        bdfu__pufk = ((S - mvla__efrmo) * (other - myskm__vxvyb)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(bdfu__pufk, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            mhk__vquz = np.sign(sum_val)
            return np.inf * mhk__vquz
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    bnzlg__jio = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        zou__dvx = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            min_val = bodo.libs.array_ops.array_op_min(arr)
            return convert_val_to_timestamp(min_val.value, tz=zou__dvx)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    bnzlg__jio = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        zou__dvx = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            max_val = bodo.libs.array_ops.array_op_max(arr)
            return convert_val_to_timestamp(max_val.value, tz=zou__dvx)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    bnzlg__jio = dict(axis=axis, skipna=skipna)
    oesmf__egzqj = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmin()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo.
        CategoricalArrayType)) or S.data in [bodo.boolean_array, bodo.
        datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    bnzlg__jio = dict(axis=axis, skipna=skipna)
    oesmf__egzqj = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmax()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo.
        CategoricalArrayType)) or S.data in [bodo.boolean_array, bodo.
        datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_method(SeriesType, 'infer_objects', inline='always')
def overload_series_infer_objects(S):
    return lambda S: S.copy()


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_increasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_decreasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    bnzlg__jio = dict(level=level, numeric_only=numeric_only)
    oesmf__egzqj = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.median(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.median(): skipna argument must be a boolean')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        guowg__jbz = arr[:n]
        adge__xwkbw = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(guowg__jbz,
            adge__xwkbw, name)
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        rlfyv__gqzfv = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        guowg__jbz = arr[rlfyv__gqzfv:]
        adge__xwkbw = index[rlfyv__gqzfv:]
        return bodo.hiframes.pd_series_ext.init_series(guowg__jbz,
            adge__xwkbw, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    dpt__hbocj = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in dpt__hbocj:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            sxpnx__hhwp = index[0]
            ngsg__dpf = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                sxpnx__hhwp, False))
        else:
            ngsg__dpf = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        guowg__jbz = arr[:ngsg__dpf]
        adge__xwkbw = index[:ngsg__dpf]
        return bodo.hiframes.pd_series_ext.init_series(guowg__jbz,
            adge__xwkbw, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    dpt__hbocj = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in dpt__hbocj:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            xsh__ahqom = index[-1]
            ngsg__dpf = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                xsh__ahqom, True))
        else:
            ngsg__dpf = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        guowg__jbz = arr[len(arr) - ngsg__dpf:]
        adge__xwkbw = index[len(arr) - ngsg__dpf:]
        return bodo.hiframes.pd_series_ext.init_series(guowg__jbz,
            adge__xwkbw, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        hih__yti = bodo.utils.conversion.index_to_array(index)
        gtij__rrsg, osik__klxtd = (bodo.libs.array_kernels.
            first_last_valid_index(arr, hih__yti))
        return osik__klxtd if gtij__rrsg else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        hih__yti = bodo.utils.conversion.index_to_array(index)
        gtij__rrsg, osik__klxtd = (bodo.libs.array_kernels.
            first_last_valid_index(arr, hih__yti, False))
        return osik__klxtd if gtij__rrsg else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    bnzlg__jio = dict(keep=keep)
    oesmf__egzqj = dict(keep='first')
    check_unsupported_args('Series.nlargest', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        hih__yti = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs, lfw__mcidp = bodo.libs.array_kernels.nlargest(arr,
            hih__yti, n, True, bodo.hiframes.series_kernels.gt_f)
        jti__dhrnz = bodo.utils.conversion.convert_to_index(lfw__mcidp)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
            jti__dhrnz, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    bnzlg__jio = dict(keep=keep)
    oesmf__egzqj = dict(keep='first')
    check_unsupported_args('Series.nsmallest', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        hih__yti = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs, lfw__mcidp = bodo.libs.array_kernels.nlargest(arr,
            hih__yti, n, False, bodo.hiframes.series_kernels.lt_f)
        jti__dhrnz = bodo.utils.conversion.convert_to_index(lfw__mcidp)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
            jti__dhrnz, name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
@overload_method(HeterogeneousSeriesType, 'astype', inline='always',
    no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    bnzlg__jio = dict(errors=errors)
    oesmf__egzqj = dict(errors='raise')
    check_unsupported_args('Series.astype', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.astype()')

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    bnzlg__jio = dict(axis=axis, is_copy=is_copy)
    oesmf__egzqj = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        pdoev__vmxg = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[pdoev__vmxg],
            index[pdoev__vmxg], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    bnzlg__jio = dict(axis=axis, kind=kind, order=order)
    oesmf__egzqj = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        skjf__wmejx = S.notna().values
        if not skjf__wmejx.all():
            mdkot__hjs = np.full(n, -1, np.int64)
            mdkot__hjs[skjf__wmejx] = argsort(arr[skjf__wmejx])
        else:
            mdkot__hjs = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    bnzlg__jio = dict(axis=axis, numeric_only=numeric_only)
    oesmf__egzqj = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_str(method):
        raise BodoError(
            "Series.rank(): 'method' argument must be a constant string")
    if not is_overload_constant_str(na_option):
        raise BodoError(
            "Series.rank(): 'na_option' argument must be a constant string")

    def impl(S, axis=0, method='average', numeric_only=None, na_option=
        'keep', ascending=True, pct=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    bnzlg__jio = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    oesmf__egzqj = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    uuv__jxze = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        exdt__kom = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, uuv__jxze)
        ryc__qumal = exdt__kom.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        mdkot__hjs = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            ryc__qumal, 0)
        jti__dhrnz = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            ryc__qumal)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
            jti__dhrnz, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    bnzlg__jio = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    oesmf__egzqj = dict(axis=0, inplace=False, kind='quicksort',
        ignore_index=False, key=None)
    check_unsupported_args('Series.sort_values', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    elfpm__kjdgq = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        exdt__kom = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, elfpm__kjdgq)
        ryc__qumal = exdt__kom.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        mdkot__hjs = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            ryc__qumal, 0)
        jti__dhrnz = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            ryc__qumal)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
            jti__dhrnz, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    hyqve__cwnd = is_overload_true(is_nullable)
    aqhfn__qzmnw = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    aqhfn__qzmnw += '  numba.parfors.parfor.init_prange()\n'
    aqhfn__qzmnw += '  n = len(arr)\n'
    if hyqve__cwnd:
        aqhfn__qzmnw += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        aqhfn__qzmnw += '  out_arr = np.empty(n, np.int64)\n'
    aqhfn__qzmnw += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    aqhfn__qzmnw += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if hyqve__cwnd:
        aqhfn__qzmnw += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        aqhfn__qzmnw += '      out_arr[i] = -1\n'
    aqhfn__qzmnw += '      continue\n'
    aqhfn__qzmnw += '    val = arr[i]\n'
    aqhfn__qzmnw += '    if include_lowest and val == bins[0]:\n'
    aqhfn__qzmnw += '      ind = 1\n'
    aqhfn__qzmnw += '    else:\n'
    aqhfn__qzmnw += '      ind = np.searchsorted(bins, val)\n'
    aqhfn__qzmnw += '    if ind == 0 or ind == len(bins):\n'
    if hyqve__cwnd:
        aqhfn__qzmnw += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        aqhfn__qzmnw += '      out_arr[i] = -1\n'
    aqhfn__qzmnw += '    else:\n'
    aqhfn__qzmnw += '      out_arr[i] = ind - 1\n'
    aqhfn__qzmnw += '  return out_arr\n'
    uhtrn__zzwqz = {}
    exec(aqhfn__qzmnw, {'bodo': bodo, 'np': np, 'numba': numba}, uhtrn__zzwqz)
    impl = uhtrn__zzwqz['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        mvj__rxbb, mfd__csha = np.divmod(x, 1)
        if mvj__rxbb == 0:
            xrb__tyffq = -int(np.floor(np.log10(abs(mfd__csha)))
                ) - 1 + precision
        else:
            xrb__tyffq = precision
        return np.around(x, xrb__tyffq)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        yheja__anet = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(yheja__anet)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        dkon__qfvq = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            xvtad__irpc = bins.copy()
            if right and include_lowest:
                xvtad__irpc[0] = xvtad__irpc[0] - dkon__qfvq
            glrpe__qbtf = bodo.libs.interval_arr_ext.init_interval_array(
                xvtad__irpc[:-1], xvtad__irpc[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(glrpe__qbtf,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        xvtad__irpc = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            xvtad__irpc[0] = xvtad__irpc[0] - 10.0 ** -precision
        glrpe__qbtf = bodo.libs.interval_arr_ext.init_interval_array(
            xvtad__irpc[:-1], xvtad__irpc[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(glrpe__qbtf, None
            )
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        jeqk__qoq = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        rbehe__percu = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        mdkot__hjs = np.zeros(nbins, np.int64)
        for uxb__owxj in range(len(jeqk__qoq)):
            mdkot__hjs[rbehe__percu[uxb__owxj]] = jeqk__qoq[uxb__owxj]
        return mdkot__hjs
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            plkog__pql = (max_val - min_val) * 0.001
            if right:
                bins[0] -= plkog__pql
            else:
                bins[-1] += plkog__pql
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    bnzlg__jio = dict(dropna=dropna)
    oesmf__egzqj = dict(dropna=True)
    check_unsupported_args('Series.value_counts', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            'Series.value_counts(): normalize argument must be a constant boolean'
            )
    if not is_overload_constant_bool(sort):
        raise_bodo_error(
            'Series.value_counts(): sort argument must be a constant boolean')
    if not is_overload_bool(ascending):
        raise_bodo_error(
            'Series.value_counts(): ascending argument must be a constant boolean'
            )
    pvtun__loeu = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    aqhfn__qzmnw = 'def impl(\n'
    aqhfn__qzmnw += '    S,\n'
    aqhfn__qzmnw += '    normalize=False,\n'
    aqhfn__qzmnw += '    sort=True,\n'
    aqhfn__qzmnw += '    ascending=False,\n'
    aqhfn__qzmnw += '    bins=None,\n'
    aqhfn__qzmnw += '    dropna=True,\n'
    aqhfn__qzmnw += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    aqhfn__qzmnw += '):\n'
    aqhfn__qzmnw += (
        '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    aqhfn__qzmnw += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    aqhfn__qzmnw += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if pvtun__loeu:
        aqhfn__qzmnw += '    right = True\n'
        aqhfn__qzmnw += _gen_bins_handling(bins, S.dtype)
        aqhfn__qzmnw += '    arr = get_bin_inds(bins, arr)\n'
    aqhfn__qzmnw += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    aqhfn__qzmnw += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    aqhfn__qzmnw += '    )\n'
    aqhfn__qzmnw += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if pvtun__loeu:
        aqhfn__qzmnw += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        aqhfn__qzmnw += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        aqhfn__qzmnw += '    index = get_bin_labels(bins)\n'
    else:
        aqhfn__qzmnw += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        aqhfn__qzmnw += (
            '    ind_arr = bodo.utils.conversion.coerce_to_array(\n')
        aqhfn__qzmnw += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        aqhfn__qzmnw += '    )\n'
        aqhfn__qzmnw += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    aqhfn__qzmnw += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        aqhfn__qzmnw += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        vsup__foup = 'len(S)' if pvtun__loeu else 'count_arr.sum()'
        aqhfn__qzmnw += f'    res = res / float({vsup__foup})\n'
    aqhfn__qzmnw += '    return res\n'
    uhtrn__zzwqz = {}
    exec(aqhfn__qzmnw, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, uhtrn__zzwqz)
    impl = uhtrn__zzwqz['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    aqhfn__qzmnw = ''
    if isinstance(bins, types.Integer):
        aqhfn__qzmnw += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        aqhfn__qzmnw += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            aqhfn__qzmnw += '    min_val = min_val.value\n'
            aqhfn__qzmnw += '    max_val = max_val.value\n'
        aqhfn__qzmnw += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            aqhfn__qzmnw += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        aqhfn__qzmnw += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return aqhfn__qzmnw


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    bnzlg__jio = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    oesmf__egzqj = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    aqhfn__qzmnw = 'def impl(\n'
    aqhfn__qzmnw += '    x,\n'
    aqhfn__qzmnw += '    bins,\n'
    aqhfn__qzmnw += '    right=True,\n'
    aqhfn__qzmnw += '    labels=None,\n'
    aqhfn__qzmnw += '    retbins=False,\n'
    aqhfn__qzmnw += '    precision=3,\n'
    aqhfn__qzmnw += '    include_lowest=False,\n'
    aqhfn__qzmnw += "    duplicates='raise',\n"
    aqhfn__qzmnw += '    ordered=True\n'
    aqhfn__qzmnw += '):\n'
    if isinstance(x, SeriesType):
        aqhfn__qzmnw += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        aqhfn__qzmnw += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        aqhfn__qzmnw += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        aqhfn__qzmnw += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    aqhfn__qzmnw += _gen_bins_handling(bins, x.dtype)
    aqhfn__qzmnw += (
        '    arr = get_bin_inds(bins, arr, False, include_lowest)\n')
    aqhfn__qzmnw += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    aqhfn__qzmnw += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    aqhfn__qzmnw += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        aqhfn__qzmnw += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        aqhfn__qzmnw += '    return res\n'
    else:
        aqhfn__qzmnw += '    return out_arr\n'
    uhtrn__zzwqz = {}
    exec(aqhfn__qzmnw, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, uhtrn__zzwqz)
    impl = uhtrn__zzwqz['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.unique, inline='always', no_unliteral=True)
def overload_unique(values):
    if not is_series_type(values) and not (bodo.utils.utils.is_array_typ(
        values, False) and values.ndim == 1):
        raise BodoError(
            "pd.unique(): 'values' must be either a Series or a 1-d array")
    if is_series_type(values):

        def impl(values):
            arr = bodo.hiframes.pd_series_ext.get_series_data(values)
            return bodo.allgatherv(bodo.libs.array_kernels.unique(arr), False)
        return impl
    else:
        return lambda values: bodo.allgatherv(bodo.libs.array_kernels.
            unique(values), False)


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    bnzlg__jio = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    oesmf__egzqj = dict(labels=None, retbins=False, precision=3, duplicates
        ='raise')
    check_unsupported_args('pandas.qcut', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        abp__kipeu = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, abp__kipeu)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    bnzlg__jio = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    oesmf__egzqj = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='GroupBy')
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )
        szi__ael = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            omcww__hopc = bodo.utils.conversion.coerce_to_array(index)
            exdt__kom = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                omcww__hopc, arr), index, szi__ael)
            return exdt__kom.groupby(' ')['']
        return impl_index
    eupw__yldht = by
    if isinstance(by, SeriesType):
        eupw__yldht = by.data
    if isinstance(eupw__yldht, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    mckx__ntbzs = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        omcww__hopc = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        exdt__kom = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            omcww__hopc, arr), index, mckx__ntbzs)
        return exdt__kom.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    bnzlg__jio = dict(verify_integrity=verify_integrity)
    oesmf__egzqj = dict(verify_integrity=False)
    check_unsupported_args('Series.append', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_append,
        'Series.append()')
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.isin()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(values,
        'Series.isin()')
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            ucmd__bcbl = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            mdkot__hjs = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(mdkot__hjs, A, ucmd__bcbl, False)
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    bnzlg__jio = dict(interpolation=interpolation)
    oesmf__egzqj = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            mdkot__hjs = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                index, name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        vqn__ilkie = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(vqn__ilkie, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    bnzlg__jio = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    oesmf__egzqj = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.describe()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, (IntegerArrayType, FloatingArrayType)):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        gke__maprd = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        gke__maprd = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    aqhfn__qzmnw = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {gke__maprd}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    rewq__suwdk = dict()
    exec(aqhfn__qzmnw, {'bodo': bodo, 'numba': numba}, rewq__suwdk)
    acgg__kpp = rewq__suwdk['impl']
    return acgg__kpp


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        gke__maprd = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        gke__maprd = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    aqhfn__qzmnw = 'def impl(S,\n'
    aqhfn__qzmnw += '     value=None,\n'
    aqhfn__qzmnw += '    method=None,\n'
    aqhfn__qzmnw += '    axis=None,\n'
    aqhfn__qzmnw += '    inplace=False,\n'
    aqhfn__qzmnw += '    limit=None,\n'
    aqhfn__qzmnw += '   downcast=None,\n'
    aqhfn__qzmnw += '):\n'
    aqhfn__qzmnw += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    aqhfn__qzmnw += '    n = len(in_arr)\n'
    aqhfn__qzmnw += f'    out_arr = {gke__maprd}(n, -1)\n'
    aqhfn__qzmnw += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    aqhfn__qzmnw += '        s = in_arr[j]\n'
    aqhfn__qzmnw += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    aqhfn__qzmnw += '            s = value\n'
    aqhfn__qzmnw += '        out_arr[j] = s\n'
    aqhfn__qzmnw += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    rewq__suwdk = dict()
    exec(aqhfn__qzmnw, {'bodo': bodo, 'numba': numba}, rewq__suwdk)
    acgg__kpp = rewq__suwdk['impl']
    return acgg__kpp


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
    rhpn__rgf = bodo.hiframes.pd_series_ext.get_series_data(value)
    for uxb__owxj in numba.parfors.parfor.internal_prange(len(orv__lkrr)):
        s = orv__lkrr[uxb__owxj]
        if bodo.libs.array_kernels.isna(orv__lkrr, uxb__owxj
            ) and not bodo.libs.array_kernels.isna(rhpn__rgf, uxb__owxj):
            s = rhpn__rgf[uxb__owxj]
        orv__lkrr[uxb__owxj] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
    for uxb__owxj in numba.parfors.parfor.internal_prange(len(orv__lkrr)):
        s = orv__lkrr[uxb__owxj]
        if bodo.libs.array_kernels.isna(orv__lkrr, uxb__owxj):
            s = value
        orv__lkrr[uxb__owxj] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    rhpn__rgf = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(orv__lkrr)
    mdkot__hjs = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for kmok__gyfnc in numba.parfors.parfor.internal_prange(n):
        s = orv__lkrr[kmok__gyfnc]
        if bodo.libs.array_kernels.isna(orv__lkrr, kmok__gyfnc
            ) and not bodo.libs.array_kernels.isna(rhpn__rgf, kmok__gyfnc):
            s = rhpn__rgf[kmok__gyfnc]
        mdkot__hjs[kmok__gyfnc] = s
        if bodo.libs.array_kernels.isna(orv__lkrr, kmok__gyfnc
            ) and bodo.libs.array_kernels.isna(rhpn__rgf, kmok__gyfnc):
            bodo.libs.array_kernels.setna(mdkot__hjs, kmok__gyfnc)
    return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    rhpn__rgf = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(orv__lkrr)
    mdkot__hjs = bodo.utils.utils.alloc_type(n, orv__lkrr.dtype, (-1,))
    for uxb__owxj in numba.parfors.parfor.internal_prange(n):
        s = orv__lkrr[uxb__owxj]
        if bodo.libs.array_kernels.isna(orv__lkrr, uxb__owxj
            ) and not bodo.libs.array_kernels.isna(rhpn__rgf, uxb__owxj):
            s = rhpn__rgf[uxb__owxj]
        mdkot__hjs[uxb__owxj] = s
    return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    bnzlg__jio = dict(limit=limit, downcast=downcast)
    oesmf__egzqj = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    zuunv__xbi = not is_overload_none(value)
    xvjvz__noh = not is_overload_none(method)
    if zuunv__xbi and xvjvz__noh:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not zuunv__xbi and not xvjvz__noh:
        raise BodoError(
            "Series.fillna(): Must specify one of 'value' and 'method'.")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.fillna(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet.'
            )
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "Series.fillna(): 'inplace' argument must be a constant boolean")
    if xvjvz__noh:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        wodiv__zrf = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(wodiv__zrf)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(wodiv__zrf)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    efnm__elr = element_type(S.data)
    gnyuh__kqm = None
    if zuunv__xbi:
        gnyuh__kqm = element_type(types.unliteral(value))
    if gnyuh__kqm and not can_replace(efnm__elr, gnyuh__kqm):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {gnyuh__kqm} with series type {efnm__elr}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if S.data == bodo.dict_str_arr_type:
                raise_bodo_error(
                    "Series.fillna(): 'inplace' not supported for dictionary-encoded string arrays yet."
                    )
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        fljt__wslfh = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                rhpn__rgf = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(orv__lkrr)
                mdkot__hjs = bodo.utils.utils.alloc_type(n, fljt__wslfh, (-1,))
                for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(orv__lkrr, uxb__owxj
                        ) and bodo.libs.array_kernels.isna(rhpn__rgf, uxb__owxj
                        ):
                        bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                        continue
                    if bodo.libs.array_kernels.isna(orv__lkrr, uxb__owxj):
                        mdkot__hjs[uxb__owxj
                            ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                            rhpn__rgf[uxb__owxj])
                        continue
                    mdkot__hjs[uxb__owxj
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        orv__lkrr[uxb__owxj])
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return fillna_series_impl
        if xvjvz__noh:
            hyf__ppcm = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(efnm__elr, (types.Integer, types.Float)
                ) and efnm__elr not in hyf__ppcm:
                raise BodoError(
                    f"Series.fillna(): series of type {efnm__elr} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                mdkot__hjs = bodo.libs.array_kernels.ffill_bfill_arr(orv__lkrr,
                    method)
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_tz_naive_timestamp(value)
            orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(orv__lkrr)
            mdkot__hjs = bodo.utils.utils.alloc_type(n, fljt__wslfh, (-1,))
            for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_tz_naive_timestamp(orv__lkrr
                    [uxb__owxj])
                if bodo.libs.array_kernels.isna(orv__lkrr, uxb__owxj):
                    s = value
                mdkot__hjs[uxb__owxj] = s
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        lpa__bovi = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        bnzlg__jio = dict(limit=limit, downcast=downcast)
        oesmf__egzqj = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', bnzlg__jio,
            oesmf__egzqj, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        efnm__elr = element_type(S.data)
        hyf__ppcm = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(efnm__elr, (types.Integer, types.Float)
            ) and efnm__elr not in hyf__ppcm:
            raise BodoError(
                f'Series.{overload_name}(): series of type {efnm__elr} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mdkot__hjs = bodo.libs.array_kernels.ffill_bfill_arr(orv__lkrr,
                lpa__bovi)
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        ozl__khy = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(ozl__khy)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        eec__uqucz = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(eec__uqucz)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        eec__uqucz = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(eec__uqucz)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        eec__uqucz = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(eec__uqucz)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    bnzlg__jio = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    bzr__cfwwb = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', bnzlg__jio, bzr__cfwwb,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    efnm__elr = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        gvzu__lafwa = element_type(to_replace.key_type)
        gnyuh__kqm = element_type(to_replace.value_type)
    else:
        gvzu__lafwa = element_type(to_replace)
        gnyuh__kqm = element_type(value)
    izkk__xfbz = None
    if efnm__elr != types.unliteral(gvzu__lafwa):
        if bodo.utils.typing.equality_always_false(efnm__elr, types.
            unliteral(gvzu__lafwa)
            ) or not bodo.utils.typing.types_equality_exists(efnm__elr,
            gvzu__lafwa):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(efnm__elr, (types.Float, types.Integer)
            ) or efnm__elr == np.bool_:
            izkk__xfbz = efnm__elr
    if not can_replace(efnm__elr, types.unliteral(gnyuh__kqm)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    ewdi__nvquu = to_str_arr_if_dict_array(S.data)
    if isinstance(ewdi__nvquu, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(orv__lkrr.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(orv__lkrr)
        mdkot__hjs = bodo.utils.utils.alloc_type(n, ewdi__nvquu, (-1,))
        mgnk__wfrh = build_replace_dict(to_replace, value, izkk__xfbz)
        for uxb__owxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(orv__lkrr, uxb__owxj):
                bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                continue
            s = orv__lkrr[uxb__owxj]
            if s in mgnk__wfrh:
                s = mgnk__wfrh[s]
            mdkot__hjs[uxb__owxj] = s
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    fxy__vvf = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    cxqyy__spnu = is_iterable_type(to_replace)
    eoef__qmafa = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    ojn__ojn = is_iterable_type(value)
    if fxy__vvf and eoef__qmafa:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                mgnk__wfrh = {}
                mgnk__wfrh[key_dtype_conv(to_replace)] = value
                return mgnk__wfrh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            mgnk__wfrh = {}
            mgnk__wfrh[to_replace] = value
            return mgnk__wfrh
        return impl
    if cxqyy__spnu and eoef__qmafa:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                mgnk__wfrh = {}
                for dztbh__fib in to_replace:
                    mgnk__wfrh[key_dtype_conv(dztbh__fib)] = value
                return mgnk__wfrh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            mgnk__wfrh = {}
            for dztbh__fib in to_replace:
                mgnk__wfrh[dztbh__fib] = value
            return mgnk__wfrh
        return impl
    if cxqyy__spnu and ojn__ojn:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                mgnk__wfrh = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for uxb__owxj in range(len(to_replace)):
                    mgnk__wfrh[key_dtype_conv(to_replace[uxb__owxj])] = value[
                        uxb__owxj]
                return mgnk__wfrh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            mgnk__wfrh = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for uxb__owxj in range(len(to_replace)):
                mgnk__wfrh[to_replace[uxb__owxj]] = value[uxb__owxj]
            return mgnk__wfrh
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.diff()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mdkot__hjs = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    bnzlg__jio = dict(ignore_index=ignore_index)
    lus__awud = dict(ignore_index=False)
    check_unsupported_args('Series.explode', bnzlg__jio, lus__awud,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hih__yti = bodo.utils.conversion.index_to_array(index)
        mdkot__hjs, bjfx__rfe = bodo.libs.array_kernels.explode(arr, hih__yti)
        jti__dhrnz = bodo.utils.conversion.index_from_array(bjfx__rfe)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
            jti__dhrnz, name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.digitize()')
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            gwmbx__hqxt = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                gwmbx__hqxt[uxb__owxj] = np.argmax(a[uxb__owxj])
            return gwmbx__hqxt
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            iqaq__qxpee = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                iqaq__qxpee[uxb__owxj] = np.argmin(a[uxb__owxj])
            return iqaq__qxpee
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType) and isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            iyy__vuxx = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(b))
            return np.dot(arr, iyy__vuxx)
        return impl
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            b = bodo.utils.conversion.ndarray_if_nullable_arr(b)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            a = bodo.utils.conversion.ndarray_if_nullable_arr(a)
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(b))
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False, how=None):
    bnzlg__jio = dict(axis=axis, inplace=inplace, how=how)
    wtelc__ricwo = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', bnzlg__jio, wtelc__ricwo,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            skjf__wmejx = S.notna().values
            hih__yti = bodo.utils.conversion.extract_index_array(S)
            jti__dhrnz = bodo.utils.conversion.convert_to_index(hih__yti[
                skjf__wmejx])
            mdkot__hjs = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(orv__lkrr))
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                jti__dhrnz, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            hih__yti = bodo.utils.conversion.extract_index_array(S)
            skjf__wmejx = S.notna().values
            jti__dhrnz = bodo.utils.conversion.convert_to_index(hih__yti[
                skjf__wmejx])
            mdkot__hjs = orv__lkrr[skjf__wmejx]
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                jti__dhrnz, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    bnzlg__jio = dict(freq=freq, axis=axis)
    oesmf__egzqj = dict(freq=None, axis=0)
    check_unsupported_args('Series.shift', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs = bodo.hiframes.rolling.shift(arr, periods, False,
            fill_value)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    bnzlg__jio = dict(fill_method=fill_method, limit=limit, freq=freq)
    oesmf__egzqj = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    if not is_overload_int(periods):
        raise BodoError(
            'Series.pct_change(): periods argument must be an Integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.pct_change()')

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


def create_series_mask_where_overload(func_name):

    def overload_series_mask_where(S, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
            f'Series.{func_name}()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
            f'Series.{func_name}()')
        _validate_arguments_mask_where(f'Series.{func_name}', 'Series', S,
            cond, other, inplace, axis, level, errors, try_cast)
        if is_overload_constant_nan(other):
            vldp__spgkd = 'None'
        else:
            vldp__spgkd = 'other'
        aqhfn__qzmnw = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            aqhfn__qzmnw += '  cond = ~cond\n'
        aqhfn__qzmnw += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        aqhfn__qzmnw += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        aqhfn__qzmnw += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        aqhfn__qzmnw += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {vldp__spgkd})
"""
        aqhfn__qzmnw += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        uhtrn__zzwqz = {}
        exec(aqhfn__qzmnw, {'bodo': bodo, 'np': np}, uhtrn__zzwqz)
        impl = uhtrn__zzwqz['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        ozl__khy = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(ozl__khy)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    bnzlg__jio = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    oesmf__egzqj = dict(inplace=False, level=None, errors='raise', try_cast
        =False)
    check_unsupported_args(f'{func_name}', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name=module_name)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if isinstance(S, bodo.hiframes.pd_index_ext.RangeIndexType):
        arr = types.Array(types.int64, 1, 'C')
    else:
        arr = S.data
    if isinstance(other, SeriesType):
        _validate_self_other_mask_where(func_name, module_name, arr, other.data
            )
    else:
        _validate_self_other_mask_where(func_name, module_name, arr, other)
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )


def _validate_self_other_mask_where(func_name, module_name, arr, other,
    max_ndim=1, is_default=False):
    if not (isinstance(arr, types.Array) or isinstance(arr,
        BooleanArrayType) or isinstance(arr, IntegerArrayType) or
        isinstance(arr, FloatingArrayType) or bodo.utils.utils.is_array_typ
        (arr, False) and arr.dtype in [bodo.string_type, bodo.bytes_type] or
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type
         not in [bodo.datetime64ns, bodo.timedelta64ns, bodo.
        pd_timestamp_tz_naive_type, bodo.pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() {module_name} data with type {arr} not yet supported'
            )
    bgv__olvz = is_overload_constant_nan(other)
    if not (is_default or bgv__olvz or is_scalar_type(other) or isinstance(
        other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
        isinstance(other, SeriesType) and (isinstance(arr, types.Array) or 
        arr.dtype in [bodo.string_type, bodo.bytes_type]) or 
        is_str_arr_type(other) and (arr.dtype == bodo.string_type or 
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type ==
        bodo.string_type) or isinstance(other, BinaryArrayType) and (arr.
        dtype == bodo.bytes_type or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type == bodo.bytes_type) or
        (not (isinstance(other, (StringArrayType, BinaryArrayType)) or 
        other == bodo.dict_str_arr_type) and (isinstance(arr.dtype, types.
        Integer) and (bodo.utils.utils.is_array_typ(other) and isinstance(
        other.dtype, types.Integer) or is_series_type(other) and isinstance
        (other.dtype, types.Integer))) or (bodo.utils.utils.is_array_typ(
        other) and arr.dtype == other.dtype or is_series_type(other) and 
        arr.dtype == other.dtype)) and (isinstance(arr, BooleanArrayType) or
        isinstance(arr, (IntegerArrayType, FloatingArrayType)))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, non-categorical series, 1-dim numpy array or StringArray with a matching type for {module_name}."
            )
    if not is_default:
        if isinstance(arr.dtype, bodo.PDCategoricalDtype):
            nwn__bfg = arr.dtype.elem_type
        else:
            nwn__bfg = arr.dtype
        if is_iterable_type(other):
            nmzmv__pdmm = other.dtype
        elif bgv__olvz:
            nmzmv__pdmm = types.float64
        else:
            nmzmv__pdmm = types.unliteral(other)
        if not bgv__olvz and not is_common_scalar_dtype([nwn__bfg, nmzmv__pdmm]
            ):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        bnzlg__jio = dict(level=level, axis=axis)
        oesmf__egzqj = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), bnzlg__jio,
            oesmf__egzqj, package_name='pandas', module_name='Series')
        qhcsl__lbnip = other == string_type or is_overload_constant_str(other)
        fiw__xhf = is_iterable_type(other) and other.dtype == string_type
        ynmi__tuimb = S.dtype == string_type and (op == operator.add and (
            qhcsl__lbnip or fiw__xhf) or op == operator.mul and isinstance(
            other, types.Integer))
        fkga__twhra = S.dtype == bodo.timedelta64ns
        ibqkn__llcr = S.dtype == bodo.datetime64ns
        igrw__yvyy = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        hrwvg__aghr = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype ==
            pd_timestamp_tz_naive_type or other.dtype == bodo.datetime64ns)
        luhe__zblsu = fkga__twhra and (igrw__yvyy or hrwvg__aghr
            ) or ibqkn__llcr and igrw__yvyy
        luhe__zblsu = luhe__zblsu and op == operator.add
        if not (isinstance(S.dtype, types.Number) or ynmi__tuimb or luhe__zblsu
            ):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        vrp__bst = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            ewdi__nvquu = vrp__bst.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and ewdi__nvquu == types.Array(types.bool_, 1, 'C'):
                ewdi__nvquu = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_tz_naive_timestamp(other
                    )
                n = len(arr)
                mdkot__hjs = bodo.utils.utils.alloc_type(n, ewdi__nvquu, (-1,))
                for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                    wih__ulrz = bodo.libs.array_kernels.isna(arr, uxb__owxj)
                    if wih__ulrz:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj
                                )
                        else:
                            mdkot__hjs[uxb__owxj] = op(fill_value, other)
                    else:
                        mdkot__hjs[uxb__owxj] = op(arr[uxb__owxj], other)
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        ewdi__nvquu = vrp__bst.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and ewdi__nvquu == types.Array(types.bool_, 1, 'C'):
            ewdi__nvquu = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            sxg__egka = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            mdkot__hjs = bodo.utils.utils.alloc_type(n, ewdi__nvquu, (-1,))
            for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                wih__ulrz = bodo.libs.array_kernels.isna(arr, uxb__owxj)
                zhd__nhxva = bodo.libs.array_kernels.isna(sxg__egka, uxb__owxj)
                if wih__ulrz and zhd__nhxva:
                    bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                elif wih__ulrz:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                    else:
                        mdkot__hjs[uxb__owxj] = op(fill_value, sxg__egka[
                            uxb__owxj])
                elif zhd__nhxva:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                    else:
                        mdkot__hjs[uxb__owxj] = op(arr[uxb__owxj], fill_value)
                else:
                    mdkot__hjs[uxb__owxj] = op(arr[uxb__owxj], sxg__egka[
                        uxb__owxj])
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                index, name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        vrp__bst = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            ewdi__nvquu = vrp__bst.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and ewdi__nvquu == types.Array(types.bool_, 1, 'C'):
                ewdi__nvquu = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                mdkot__hjs = bodo.utils.utils.alloc_type(n, ewdi__nvquu, None)
                for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                    wih__ulrz = bodo.libs.array_kernels.isna(arr, uxb__owxj)
                    if wih__ulrz:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj
                                )
                        else:
                            mdkot__hjs[uxb__owxj] = op(other, fill_value)
                    else:
                        mdkot__hjs[uxb__owxj] = op(other, arr[uxb__owxj])
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        ewdi__nvquu = vrp__bst.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and ewdi__nvquu == types.Array(types.bool_, 1, 'C'):
            ewdi__nvquu = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            sxg__egka = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            mdkot__hjs = bodo.utils.utils.alloc_type(n, ewdi__nvquu, None)
            for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                wih__ulrz = bodo.libs.array_kernels.isna(arr, uxb__owxj)
                zhd__nhxva = bodo.libs.array_kernels.isna(sxg__egka, uxb__owxj)
                mdkot__hjs[uxb__owxj] = op(sxg__egka[uxb__owxj], arr[uxb__owxj]
                    )
                if wih__ulrz and zhd__nhxva:
                    bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                elif wih__ulrz:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                    else:
                        mdkot__hjs[uxb__owxj] = op(sxg__egka[uxb__owxj],
                            fill_value)
                elif zhd__nhxva:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                    else:
                        mdkot__hjs[uxb__owxj] = op(fill_value, arr[uxb__owxj])
                else:
                    mdkot__hjs[uxb__owxj] = op(sxg__egka[uxb__owxj], arr[
                        uxb__owxj])
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                index, name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, rec__csz in explicit_binop_funcs_two_ways.items():
        for name in rec__csz:
            ozl__khy = create_explicit_binary_op_overload(op)
            jdtsc__mns = create_explicit_binary_reverse_op_overload(op)
            wrdy__oltr = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(ozl__khy)
            overload_method(SeriesType, wrdy__oltr, no_unliteral=True)(
                jdtsc__mns)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        ozl__khy = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(ozl__khy)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hanl__gbvdz = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                mdkot__hjs = dt64_arr_sub(arr, hanl__gbvdz)
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                mdkot__hjs = np.empty(n, np.dtype('datetime64[ns]'))
                for uxb__owxj in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, uxb__owxj):
                        bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                        continue
                    vhn__vahl = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[uxb__owxj]))
                    dbl__ukfjb = op(vhn__vahl, rhs)
                    mdkot__hjs[uxb__owxj
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        dbl__ukfjb.value)
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    hanl__gbvdz = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    mdkot__hjs = op(arr, bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(hanl__gbvdz))
                    return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hanl__gbvdz = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                mdkot__hjs = op(arr, hanl__gbvdz)
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    iwqn__qrh = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    mdkot__hjs = op(bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(iwqn__qrh), arr)
                    return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                iwqn__qrh = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                mdkot__hjs = op(iwqn__qrh, arr)
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        ozl__khy = create_binary_op_overload(op)
        overload(op)(ozl__khy)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    vxt__pyxcu = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, vxt__pyxcu)
        for uxb__owxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, uxb__owxj
                ) or bodo.libs.array_kernels.isna(arg2, uxb__owxj):
                bodo.libs.array_kernels.setna(S, uxb__owxj)
                continue
            S[uxb__owxj
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                uxb__owxj]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[uxb__owxj]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                sxg__egka = bodo.utils.conversion.get_array_if_series_or_index(
                    other)
                op(arr, sxg__egka)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        ozl__khy = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(ozl__khy)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                mdkot__hjs = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        ozl__khy = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(ozl__khy)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    mdkot__hjs = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    sxg__egka = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    mdkot__hjs = ufunc(arr, sxg__egka)
                    return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    sxg__egka = bodo.hiframes.pd_series_ext.get_series_data(S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    mdkot__hjs = ufunc(arr, sxg__egka)
                    return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        ozl__khy = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(ozl__khy)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        hobi__kswuh = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        urros__yfp = np.arange(n),
        bodo.libs.timsort.sort(hobi__kswuh, 0, n, urros__yfp)
        return urros__yfp[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        wtdqi__ynv = get_overload_const_str(downcast)
        if wtdqi__ynv in ('integer', 'signed'):
            out_dtype = types.int64
        elif wtdqi__ynv == 'unsigned':
            out_dtype = types.uint64
        else:
            assert wtdqi__ynv == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            orv__lkrr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            mdkot__hjs = pd.to_numeric(orv__lkrr, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if arg_a == bodo.dict_str_arr_type:
        return (lambda arg_a, errors='raise', downcast=None: bodo.libs.
            dict_arr_ext.dict_arr_to_numeric(arg_a, errors, downcast))
    gtfv__jlyrc = types.Array(types.float64, 1, 'C'
        ) if out_dtype == types.float64 else IntegerArrayType(types.int64)

    def to_numeric_impl(arg_a, errors='raise', downcast=None):
        numba.parfors.parfor.init_prange()
        n = len(arg_a)
        zlm__yif = bodo.utils.utils.alloc_type(n, gtfv__jlyrc, (-1,))
        for uxb__owxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg_a, uxb__owxj):
                bodo.libs.array_kernels.setna(zlm__yif, uxb__owxj)
            else:
                bodo.libs.str_arr_ext.str_arr_item_to_numeric(zlm__yif,
                    uxb__owxj, arg_a, uxb__owxj)
        return zlm__yif
    return to_numeric_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        tpmgw__ann = if_series_to_array_type(args[0])
        if isinstance(tpmgw__ann, types.Array) and isinstance(tpmgw__ann.
            dtype, types.Integer):
            tpmgw__ann = types.Array(types.float64, 1, 'C')
        return tpmgw__ann(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(y,
        'numpy.where()')
    cngxy__res = bodo.utils.utils.is_array_typ(x, True)
    aig__nvmay = bodo.utils.utils.is_array_typ(y, True)
    aqhfn__qzmnw = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        aqhfn__qzmnw += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if cngxy__res and not bodo.utils.utils.is_array_typ(x, False):
        aqhfn__qzmnw += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if aig__nvmay and not bodo.utils.utils.is_array_typ(y, False):
        aqhfn__qzmnw += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    aqhfn__qzmnw += '  n = len(condition)\n'
    eipe__kvkbc = x.dtype if cngxy__res else types.unliteral(x)
    gmo__yhvys = y.dtype if aig__nvmay else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        eipe__kvkbc = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        gmo__yhvys = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    nmnav__ogwx = get_data(x)
    hvlz__gecn = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(urros__yfp) for
        urros__yfp in [nmnav__ogwx, hvlz__gecn])
    if hvlz__gecn == types.none:
        if isinstance(eipe__kvkbc, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif nmnav__ogwx == hvlz__gecn and not is_nullable:
        out_dtype = dtype_to_array_type(eipe__kvkbc)
    elif eipe__kvkbc == string_type or gmo__yhvys == string_type:
        out_dtype = bodo.string_array_type
    elif nmnav__ogwx == bytes_type or (cngxy__res and eipe__kvkbc == bytes_type
        ) and (hvlz__gecn == bytes_type or aig__nvmay and gmo__yhvys ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(eipe__kvkbc, bodo.PDCategoricalDtype):
        out_dtype = None
    elif eipe__kvkbc in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(eipe__kvkbc, 1, 'C')
    elif gmo__yhvys in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(gmo__yhvys, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(eipe__kvkbc), numba.np.numpy_support.
            as_dtype(gmo__yhvys)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(eipe__kvkbc, bodo.PDCategoricalDtype):
        hbtky__svhfz = 'x'
    else:
        hbtky__svhfz = 'out_dtype'
    aqhfn__qzmnw += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {hbtky__svhfz}, (-1,))\n')
    if isinstance(eipe__kvkbc, bodo.PDCategoricalDtype):
        aqhfn__qzmnw += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        aqhfn__qzmnw += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    aqhfn__qzmnw += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    aqhfn__qzmnw += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if cngxy__res:
        aqhfn__qzmnw += '      if bodo.libs.array_kernels.isna(x, j):\n'
        aqhfn__qzmnw += '        setna(out_arr, j)\n'
        aqhfn__qzmnw += '        continue\n'
    if isinstance(eipe__kvkbc, bodo.PDCategoricalDtype):
        aqhfn__qzmnw += '      out_codes[j] = x_codes[j]\n'
    else:
        aqhfn__qzmnw += (
            """      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})
"""
            .format('x[j]' if cngxy__res else 'x'))
    aqhfn__qzmnw += '    else:\n'
    if aig__nvmay:
        aqhfn__qzmnw += '      if bodo.libs.array_kernels.isna(y, j):\n'
        aqhfn__qzmnw += '        setna(out_arr, j)\n'
        aqhfn__qzmnw += '        continue\n'
    if hvlz__gecn == types.none:
        if isinstance(eipe__kvkbc, bodo.PDCategoricalDtype):
            aqhfn__qzmnw += '      out_codes[j] = -1\n'
        else:
            aqhfn__qzmnw += '      setna(out_arr, j)\n'
    else:
        aqhfn__qzmnw += (
            """      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})
"""
            .format('y[j]' if aig__nvmay else 'y'))
    aqhfn__qzmnw += '  return out_arr\n'
    uhtrn__zzwqz = {}
    exec(aqhfn__qzmnw, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, uhtrn__zzwqz)
    cuy__zvsr = uhtrn__zzwqz['_impl']
    return cuy__zvsr


def _verify_np_select_arg_typs(condlist, choicelist, default):
    if isinstance(condlist, (types.List, types.UniTuple)):
        if not (bodo.utils.utils.is_np_array_typ(condlist.dtype) and 
            condlist.dtype.dtype == types.bool_):
            raise BodoError(
                "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
                )
    else:
        raise BodoError(
            "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
            )
    if not isinstance(choicelist, (types.List, types.UniTuple, types.BaseTuple)
        ):
        raise BodoError(
            "np.select(): 'choicelist' argument must be list or tuple type")
    if isinstance(choicelist, (types.List, types.UniTuple)):
        xysae__mwat = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(xysae__mwat, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(xysae__mwat):
            pwplk__imyd = xysae__mwat.data.dtype
        else:
            pwplk__imyd = xysae__mwat.dtype
        if isinstance(pwplk__imyd, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        ljdp__pzi = xysae__mwat
    else:
        wpub__zdn = []
        for xysae__mwat in choicelist:
            if not bodo.utils.utils.is_array_typ(xysae__mwat, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(xysae__mwat):
                pwplk__imyd = xysae__mwat.data.dtype
            else:
                pwplk__imyd = xysae__mwat.dtype
            if isinstance(pwplk__imyd, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            wpub__zdn.append(pwplk__imyd)
        if not is_common_scalar_dtype(wpub__zdn):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        ljdp__pzi = choicelist[0]
    if is_series_type(ljdp__pzi):
        ljdp__pzi = ljdp__pzi.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, ljdp__pzi.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(ljdp__pzi, types.Array) or isinstance(ljdp__pzi,
        BooleanArrayType) or isinstance(ljdp__pzi, IntegerArrayType) or
        isinstance(ljdp__pzi, FloatingArrayType) or bodo.utils.utils.
        is_array_typ(ljdp__pzi, False) and ljdp__pzi.dtype in [bodo.
        string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {ljdp__pzi} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    gih__hsmvz = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        rfqf__gpokd = choicelist.dtype
    else:
        grg__uau = False
        wpub__zdn = []
        for xysae__mwat in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                xysae__mwat, 'numpy.select()')
            if is_nullable_type(xysae__mwat):
                grg__uau = True
            if is_series_type(xysae__mwat):
                pwplk__imyd = xysae__mwat.data.dtype
            else:
                pwplk__imyd = xysae__mwat.dtype
            if isinstance(pwplk__imyd, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            wpub__zdn.append(pwplk__imyd)
        ikap__vvkuj, kkxkg__scp = get_common_scalar_dtype(wpub__zdn)
        if not kkxkg__scp:
            raise BodoError('Internal error in overload_np_select')
        brqf__ednrh = dtype_to_array_type(ikap__vvkuj)
        if grg__uau:
            brqf__ednrh = to_nullable_type(brqf__ednrh)
        rfqf__gpokd = brqf__ednrh
    if isinstance(rfqf__gpokd, SeriesType):
        rfqf__gpokd = rfqf__gpokd.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        cowjo__necot = True
    else:
        cowjo__necot = False
    dxkfh__mhqk = False
    xroq__uevz = False
    if cowjo__necot:
        if isinstance(rfqf__gpokd.dtype, types.Number):
            pass
        elif rfqf__gpokd.dtype == types.bool_:
            xroq__uevz = True
        else:
            dxkfh__mhqk = True
            rfqf__gpokd = to_nullable_type(rfqf__gpokd)
    elif default == types.none or is_overload_constant_nan(default):
        dxkfh__mhqk = True
        rfqf__gpokd = to_nullable_type(rfqf__gpokd)
    aqhfn__qzmnw = 'def np_select_impl(condlist, choicelist, default=0):\n'
    aqhfn__qzmnw += '  if len(condlist) != len(choicelist):\n'
    aqhfn__qzmnw += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    aqhfn__qzmnw += '  output_len = len(choicelist[0])\n'
    aqhfn__qzmnw += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    aqhfn__qzmnw += '  for i in range(output_len):\n'
    if dxkfh__mhqk:
        aqhfn__qzmnw += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif xroq__uevz:
        aqhfn__qzmnw += '    out[i] = False\n'
    else:
        aqhfn__qzmnw += '    out[i] = default\n'
    if gih__hsmvz:
        aqhfn__qzmnw += '  for i in range(len(condlist) - 1, -1, -1):\n'
        aqhfn__qzmnw += '    cond = condlist[i]\n'
        aqhfn__qzmnw += '    choice = choicelist[i]\n'
        aqhfn__qzmnw += '    out = np.where(cond, choice, out)\n'
    else:
        for uxb__owxj in range(len(choicelist) - 1, -1, -1):
            aqhfn__qzmnw += f'  cond = condlist[{uxb__owxj}]\n'
            aqhfn__qzmnw += f'  choice = choicelist[{uxb__owxj}]\n'
            aqhfn__qzmnw += f'  out = np.where(cond, choice, out)\n'
    aqhfn__qzmnw += '  return out'
    uhtrn__zzwqz = dict()
    exec(aqhfn__qzmnw, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': rfqf__gpokd}, uhtrn__zzwqz)
    impl = uhtrn__zzwqz['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mdkot__hjs = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    bnzlg__jio = dict(subset=subset, keep=keep, inplace=inplace)
    oesmf__egzqj = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', bnzlg__jio,
        oesmf__egzqj, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        gdpn__mhhei = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (gdpn__mhhei,), hih__yti = bodo.libs.array_kernels.drop_duplicates((
            gdpn__mhhei,), index, 1)
        index = bodo.utils.conversion.index_from_array(hih__yti)
        return bodo.hiframes.pd_series_ext.init_series(gdpn__mhhei, index, name
            )
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    ouwr__hxony = element_type(S.data)
    if not is_common_scalar_dtype([ouwr__hxony, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([ouwr__hxony, right]):
        raise_bodo_error(
            "Series.between(): 'right' must be compariable with the Series data"
            )
    if not is_overload_constant_str(inclusive) or get_overload_const_str(
        inclusive) not in ('both', 'neither'):
        raise_bodo_error(
            "Series.between(): 'inclusive' must be a constant string and one of ('both', 'neither')"
            )

    def impl(S, left, right, inclusive='both'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        mdkot__hjs = bodo.libs.bool_arr_ext.alloc_bool_array(n)
        for uxb__owxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arr, uxb__owxj):
                bodo.libs.array_kernels.setna(mdkot__hjs, uxb__owxj)
                continue
            oms__dwnni = bodo.utils.conversion.box_if_dt64(arr[uxb__owxj])
            if inclusive == 'both':
                mdkot__hjs[uxb__owxj
                    ] = oms__dwnni <= right and oms__dwnni >= left
            else:
                mdkot__hjs[uxb__owxj
                    ] = oms__dwnni < right and oms__dwnni > left
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    bnzlg__jio = dict(axis=axis)
    oesmf__egzqj = dict(axis=None)
    check_unsupported_args('Series.repeat', bnzlg__jio, oesmf__egzqj,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            hih__yti = bodo.utils.conversion.index_to_array(index)
            mdkot__hjs = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            bjfx__rfe = bodo.libs.array_kernels.repeat_kernel(hih__yti, repeats
                )
            jti__dhrnz = bodo.utils.conversion.index_from_array(bjfx__rfe)
            return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
                jti__dhrnz, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hih__yti = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        mdkot__hjs = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        bjfx__rfe = bodo.libs.array_kernels.repeat_kernel(hih__yti, repeats)
        jti__dhrnz = bodo.utils.conversion.index_from_array(bjfx__rfe)
        return bodo.hiframes.pd_series_ext.init_series(mdkot__hjs,
            jti__dhrnz, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        urros__yfp = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(urros__yfp)
        buzo__pyed = {}
        for uxb__owxj in range(n):
            oms__dwnni = bodo.utils.conversion.box_if_dt64(urros__yfp[
                uxb__owxj])
            buzo__pyed[index[uxb__owxj]] = oms__dwnni
        return buzo__pyed
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    wodiv__zrf = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            wdv__tmlx = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(wodiv__zrf)
    elif is_literal_type(name):
        wdv__tmlx = get_literal_value(name)
    else:
        raise_bodo_error(wodiv__zrf)
    wdv__tmlx = 0 if wdv__tmlx is None else wdv__tmlx
    zqi__ozq = ColNamesMetaType((wdv__tmlx,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            zqi__ozq)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
