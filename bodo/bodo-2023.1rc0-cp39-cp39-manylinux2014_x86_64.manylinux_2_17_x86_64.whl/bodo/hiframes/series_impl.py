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
            qlhoh__yvxjy = bodo.hiframes.pd_series_ext.get_series_data(s)
            qnrhg__eloe = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                qlhoh__yvxjy)
            return qnrhg__eloe
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
            ywt__emnif = list()
            for zmjh__sgi in range(len(S)):
                ywt__emnif.append(S.iat[zmjh__sgi])
            return ywt__emnif
        return impl_float

    def impl(S):
        ywt__emnif = list()
        for zmjh__sgi in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, zmjh__sgi):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            ywt__emnif.append(S.iat[zmjh__sgi])
        return ywt__emnif
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    otil__wgam = dict(dtype=dtype, copy=copy, na_value=na_value)
    sevi__lpn = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    otil__wgam = dict(name=name, inplace=inplace)
    sevi__lpn = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', otil__wgam, sevi__lpn,
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
        slgxw__tanvs = ', '.join(['index_arrs[{}]'.format(zmjh__sgi) for
            zmjh__sgi in range(S.index.nlevels)])
    else:
        slgxw__tanvs = '    bodo.utils.conversion.index_to_array(index)\n'
    fap__ufw = 'index' if 'index' != series_name else 'level_0'
    dekm__tyj = get_index_names(S.index, 'Series.reset_index()', fap__ufw)
    columns = [name for name in dekm__tyj]
    columns.append(series_name)
    qjyvq__slkr = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    qjyvq__slkr += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    qjyvq__slkr += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        qjyvq__slkr += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    qjyvq__slkr += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    qjyvq__slkr += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({slgxw__tanvs}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    jaljw__bxy = {}
    exec(qjyvq__slkr, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, jaljw__bxy)
    czzec__wpihw = jaljw__bxy['_impl']
    return czzec__wpihw


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        aclx__jrczi = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
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
        aclx__jrczi = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[zmjh__sgi]):
                bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
            else:
                aclx__jrczi[zmjh__sgi] = np.round(arr[zmjh__sgi], decimals)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    otil__wgam = dict(level=level, numeric_only=numeric_only)
    sevi__lpn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(level=level, numeric_only=numeric_only)
    sevi__lpn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    sevi__lpn = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', otil__wgam, sevi__lpn,
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
        qsygy__esj = bodo.hiframes.pd_series_ext.get_series_data(S)
        hbw__hgnb = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        lgzag__kosi = 0
        for zmjh__sgi in numba.parfors.parfor.internal_prange(len(qsygy__esj)):
            cfor__rnr = 0
            iqcl__tamj = bodo.libs.array_kernels.isna(qsygy__esj, zmjh__sgi)
            gkl__cra = bodo.libs.array_kernels.isna(hbw__hgnb, zmjh__sgi)
            if iqcl__tamj and not gkl__cra or not iqcl__tamj and gkl__cra:
                cfor__rnr = 1
            elif not iqcl__tamj:
                if qsygy__esj[zmjh__sgi] != hbw__hgnb[zmjh__sgi]:
                    cfor__rnr = 1
            lgzag__kosi += cfor__rnr
        return lgzag__kosi == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    otil__wgam = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    sevi__lpn = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    otil__wgam = dict(level=level)
    sevi__lpn = dict(level=None)
    check_unsupported_args('Series.mad', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    vthb__pttjd = types.float64
    ehyzl__fhsft = types.float64
    if S.dtype == types.float32:
        vthb__pttjd = types.float32
        ehyzl__fhsft = types.float32
    pweb__zmhz = vthb__pttjd(0)
    utlsc__vku = ehyzl__fhsft(0)
    nzgl__eiyvx = ehyzl__fhsft(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        rhhim__udhxv = pweb__zmhz
        lgzag__kosi = utlsc__vku
        for zmjh__sgi in numba.parfors.parfor.internal_prange(len(A)):
            cfor__rnr = pweb__zmhz
            iuhnv__ohw = utlsc__vku
            if not bodo.libs.array_kernels.isna(A, zmjh__sgi) or not skipna:
                cfor__rnr = A[zmjh__sgi]
                iuhnv__ohw = nzgl__eiyvx
            rhhim__udhxv += cfor__rnr
            lgzag__kosi += iuhnv__ohw
        utpn__fptvo = bodo.hiframes.series_kernels._mean_handle_nan(
            rhhim__udhxv, lgzag__kosi)
        kqszs__samh = pweb__zmhz
        for zmjh__sgi in numba.parfors.parfor.internal_prange(len(A)):
            cfor__rnr = pweb__zmhz
            if not bodo.libs.array_kernels.isna(A, zmjh__sgi) or not skipna:
                cfor__rnr = abs(A[zmjh__sgi] - utpn__fptvo)
            kqszs__samh += cfor__rnr
        ojosp__cen = bodo.hiframes.series_kernels._mean_handle_nan(kqszs__samh,
            lgzag__kosi)
        return ojosp__cen
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    otil__wgam = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    sevi__lpn = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(level=level, numeric_only=numeric_only)
    sevi__lpn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', otil__wgam, sevi__lpn,
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
        bnj__vuoyg = 0
        ksv__iec = 0
        lgzag__kosi = 0
        for zmjh__sgi in numba.parfors.parfor.internal_prange(len(A)):
            cfor__rnr = 0
            iuhnv__ohw = 0
            if not bodo.libs.array_kernels.isna(A, zmjh__sgi) or not skipna:
                cfor__rnr = A[zmjh__sgi]
                iuhnv__ohw = 1
            bnj__vuoyg += cfor__rnr
            ksv__iec += cfor__rnr * cfor__rnr
            lgzag__kosi += iuhnv__ohw
        diccd__nnwgy = (bodo.hiframes.series_kernels.
            _compute_var_nan_count_ddof(bnj__vuoyg, ksv__iec, lgzag__kosi,
            ddof))
        crg__dcz = bodo.hiframes.series_kernels._sem_handle_nan(diccd__nnwgy,
            lgzag__kosi)
        return crg__dcz
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    otil__wgam = dict(level=level, numeric_only=numeric_only)
    sevi__lpn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', otil__wgam, sevi__lpn,
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
        bnj__vuoyg = 0.0
        ksv__iec = 0.0
        bhpn__tgets = 0.0
        ibk__ikw = 0.0
        lgzag__kosi = 0
        for zmjh__sgi in numba.parfors.parfor.internal_prange(len(A)):
            cfor__rnr = 0.0
            iuhnv__ohw = 0
            if not bodo.libs.array_kernels.isna(A, zmjh__sgi) or not skipna:
                cfor__rnr = np.float64(A[zmjh__sgi])
                iuhnv__ohw = 1
            bnj__vuoyg += cfor__rnr
            ksv__iec += cfor__rnr ** 2
            bhpn__tgets += cfor__rnr ** 3
            ibk__ikw += cfor__rnr ** 4
            lgzag__kosi += iuhnv__ohw
        diccd__nnwgy = bodo.hiframes.series_kernels.compute_kurt(bnj__vuoyg,
            ksv__iec, bhpn__tgets, ibk__ikw, lgzag__kosi)
        return diccd__nnwgy
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    otil__wgam = dict(level=level, numeric_only=numeric_only)
    sevi__lpn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', otil__wgam, sevi__lpn,
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
        bnj__vuoyg = 0.0
        ksv__iec = 0.0
        bhpn__tgets = 0.0
        lgzag__kosi = 0
        for zmjh__sgi in numba.parfors.parfor.internal_prange(len(A)):
            cfor__rnr = 0.0
            iuhnv__ohw = 0
            if not bodo.libs.array_kernels.isna(A, zmjh__sgi) or not skipna:
                cfor__rnr = np.float64(A[zmjh__sgi])
                iuhnv__ohw = 1
            bnj__vuoyg += cfor__rnr
            ksv__iec += cfor__rnr ** 2
            bhpn__tgets += cfor__rnr ** 3
            lgzag__kosi += iuhnv__ohw
        diccd__nnwgy = bodo.hiframes.series_kernels.compute_skew(bnj__vuoyg,
            ksv__iec, bhpn__tgets, lgzag__kosi)
        return diccd__nnwgy
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    otil__wgam = dict(level=level, numeric_only=numeric_only)
    sevi__lpn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(level=level, numeric_only=numeric_only)
    sevi__lpn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', otil__wgam, sevi__lpn,
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
        qsygy__esj = bodo.hiframes.pd_series_ext.get_series_data(S)
        hbw__hgnb = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        ycst__mqebr = 0
        for zmjh__sgi in numba.parfors.parfor.internal_prange(len(qsygy__esj)):
            vua__dden = qsygy__esj[zmjh__sgi]
            ngoxr__ktquc = hbw__hgnb[zmjh__sgi]
            ycst__mqebr += vua__dden * ngoxr__ktquc
        return ycst__mqebr
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    otil__wgam = dict(skipna=skipna)
    sevi__lpn = dict(skipna=True)
    check_unsupported_args('Series.cumsum', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(skipna=skipna)
    sevi__lpn = dict(skipna=True)
    check_unsupported_args('Series.cumprod', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(skipna=skipna)
    sevi__lpn = dict(skipna=True)
    check_unsupported_args('Series.cummin', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(skipna=skipna)
    sevi__lpn = dict(skipna=True)
    check_unsupported_args('Series.cummax', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    sevi__lpn = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        axflg__ibpqb = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, axflg__ibpqb, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    otil__wgam = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    sevi__lpn = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', otil__wgam, sevi__lpn,
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
    hvhwa__qbiy = S.data

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(A)
        aclx__jrczi = bodo.utils.utils.alloc_type(n, hvhwa__qbiy, (-1,))
        for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, zmjh__sgi):
                bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                continue
            aclx__jrczi[zmjh__sgi] = np.abs(A[zmjh__sgi])
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    otil__wgam = dict(level=level)
    sevi__lpn = dict(level=None)
    check_unsupported_args('Series.count', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    otil__wgam = dict(method=method, min_periods=min_periods)
    sevi__lpn = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        uzhgb__uak = S.sum()
        jqey__fhli = other.sum()
        a = n * (S * other).sum() - uzhgb__uak * jqey__fhli
        yxt__lkz = n * (S ** 2).sum() - uzhgb__uak ** 2
        rpu__uabkr = n * (other ** 2).sum() - jqey__fhli ** 2
        return a / np.sqrt(yxt__lkz * rpu__uabkr)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    otil__wgam = dict(min_periods=min_periods)
    sevi__lpn = dict(min_periods=None)
    check_unsupported_args('Series.cov', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        uzhgb__uak = S.mean()
        jqey__fhli = other.mean()
        ydejd__wqge = ((S - uzhgb__uak) * (other - jqey__fhli)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(ydejd__wqge, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            hyu__aabv = np.sign(sum_val)
            return np.inf * hyu__aabv
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    otil__wgam = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    sevi__lpn = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        lgtn__bljdw = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            min_val = bodo.libs.array_ops.array_op_min(arr)
            return convert_val_to_timestamp(min_val.value, tz=lgtn__bljdw)
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
    otil__wgam = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    sevi__lpn = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        lgtn__bljdw = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            max_val = bodo.libs.array_ops.array_op_max(arr)
            return convert_val_to_timestamp(max_val.value, tz=lgtn__bljdw)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    otil__wgam = dict(axis=axis, skipna=skipna)
    sevi__lpn = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(axis=axis, skipna=skipna)
    sevi__lpn = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', otil__wgam, sevi__lpn,
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
    otil__wgam = dict(level=level, numeric_only=numeric_only)
    sevi__lpn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', otil__wgam, sevi__lpn,
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
        qtte__yqnq = arr[:n]
        emzh__fdyur = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(qtte__yqnq,
            emzh__fdyur, name)
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
        ytojw__ngmz = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qtte__yqnq = arr[ytojw__ngmz:]
        emzh__fdyur = index[ytojw__ngmz:]
        return bodo.hiframes.pd_series_ext.init_series(qtte__yqnq,
            emzh__fdyur, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    tcgu__oxtj = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in tcgu__oxtj:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            wye__ibewf = index[0]
            lxlwj__csp = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                wye__ibewf, False))
        else:
            lxlwj__csp = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qtte__yqnq = arr[:lxlwj__csp]
        emzh__fdyur = index[:lxlwj__csp]
        return bodo.hiframes.pd_series_ext.init_series(qtte__yqnq,
            emzh__fdyur, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    tcgu__oxtj = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in tcgu__oxtj:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            eqx__trf = index[-1]
            lxlwj__csp = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, eqx__trf,
                True))
        else:
            lxlwj__csp = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qtte__yqnq = arr[len(arr) - lxlwj__csp:]
        emzh__fdyur = index[len(arr) - lxlwj__csp:]
        return bodo.hiframes.pd_series_ext.init_series(qtte__yqnq,
            emzh__fdyur, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        nsmmr__dhvyw = bodo.utils.conversion.index_to_array(index)
        tsndu__qplg, sky__rrcoh = (bodo.libs.array_kernels.
            first_last_valid_index(arr, nsmmr__dhvyw))
        return sky__rrcoh if tsndu__qplg else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        nsmmr__dhvyw = bodo.utils.conversion.index_to_array(index)
        tsndu__qplg, sky__rrcoh = (bodo.libs.array_kernels.
            first_last_valid_index(arr, nsmmr__dhvyw, False))
        return sky__rrcoh if tsndu__qplg else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    otil__wgam = dict(keep=keep)
    sevi__lpn = dict(keep='first')
    check_unsupported_args('Series.nlargest', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        nsmmr__dhvyw = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        aclx__jrczi, rdntr__nzt = bodo.libs.array_kernels.nlargest(arr,
            nsmmr__dhvyw, n, True, bodo.hiframes.series_kernels.gt_f)
        fyeus__bubrt = bodo.utils.conversion.convert_to_index(rdntr__nzt)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
            fyeus__bubrt, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    otil__wgam = dict(keep=keep)
    sevi__lpn = dict(keep='first')
    check_unsupported_args('Series.nsmallest', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        nsmmr__dhvyw = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        aclx__jrczi, rdntr__nzt = bodo.libs.array_kernels.nlargest(arr,
            nsmmr__dhvyw, n, False, bodo.hiframes.series_kernels.lt_f)
        fyeus__bubrt = bodo.utils.conversion.convert_to_index(rdntr__nzt)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
            fyeus__bubrt, name)
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
    otil__wgam = dict(errors=errors)
    sevi__lpn = dict(errors='raise')
    check_unsupported_args('Series.astype', otil__wgam, sevi__lpn,
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
        aclx__jrczi = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    otil__wgam = dict(axis=axis, is_copy=is_copy)
    sevi__lpn = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        iqc__lsd = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[iqc__lsd], index
            [iqc__lsd], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    otil__wgam = dict(axis=axis, kind=kind, order=order)
    sevi__lpn = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pplaz__chi = S.notna().values
        if not pplaz__chi.all():
            aclx__jrczi = np.full(n, -1, np.int64)
            aclx__jrczi[pplaz__chi] = argsort(arr[pplaz__chi])
        else:
            aclx__jrczi = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    otil__wgam = dict(axis=axis, numeric_only=numeric_only)
    sevi__lpn = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', otil__wgam, sevi__lpn,
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
        aclx__jrczi = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    otil__wgam = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    sevi__lpn = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    zfyjr__kgwa = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        jszja__zop = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, zfyjr__kgwa)
        ljyuu__tsjfs = jszja__zop.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        aclx__jrczi = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            ljyuu__tsjfs, 0)
        fyeus__bubrt = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            ljyuu__tsjfs)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
            fyeus__bubrt, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    otil__wgam = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    sevi__lpn = dict(axis=0, inplace=False, kind='quicksort', ignore_index=
        False, key=None)
    check_unsupported_args('Series.sort_values', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    kcnwn__yjgj = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        jszja__zop = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, kcnwn__yjgj)
        ljyuu__tsjfs = jszja__zop.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        aclx__jrczi = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            ljyuu__tsjfs, 0)
        fyeus__bubrt = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            ljyuu__tsjfs)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
            fyeus__bubrt, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    hlr__ikmq = is_overload_true(is_nullable)
    qjyvq__slkr = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    qjyvq__slkr += '  numba.parfors.parfor.init_prange()\n'
    qjyvq__slkr += '  n = len(arr)\n'
    if hlr__ikmq:
        qjyvq__slkr += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        qjyvq__slkr += '  out_arr = np.empty(n, np.int64)\n'
    qjyvq__slkr += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    qjyvq__slkr += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if hlr__ikmq:
        qjyvq__slkr += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        qjyvq__slkr += '      out_arr[i] = -1\n'
    qjyvq__slkr += '      continue\n'
    qjyvq__slkr += '    val = arr[i]\n'
    qjyvq__slkr += '    if include_lowest and val == bins[0]:\n'
    qjyvq__slkr += '      ind = 1\n'
    qjyvq__slkr += '    else:\n'
    qjyvq__slkr += '      ind = np.searchsorted(bins, val)\n'
    qjyvq__slkr += '    if ind == 0 or ind == len(bins):\n'
    if hlr__ikmq:
        qjyvq__slkr += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        qjyvq__slkr += '      out_arr[i] = -1\n'
    qjyvq__slkr += '    else:\n'
    qjyvq__slkr += '      out_arr[i] = ind - 1\n'
    qjyvq__slkr += '  return out_arr\n'
    jaljw__bxy = {}
    exec(qjyvq__slkr, {'bodo': bodo, 'np': np, 'numba': numba}, jaljw__bxy)
    impl = jaljw__bxy['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        hyk__ejpkq, dor__bdbao = np.divmod(x, 1)
        if hyk__ejpkq == 0:
            wrfvn__gmlwk = -int(np.floor(np.log10(abs(dor__bdbao)))
                ) - 1 + precision
        else:
            wrfvn__gmlwk = precision
        return np.around(x, wrfvn__gmlwk)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        iabji__syq = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(iabji__syq)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        vvavy__ccty = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            fmu__csbht = bins.copy()
            if right and include_lowest:
                fmu__csbht[0] = fmu__csbht[0] - vvavy__ccty
            nandt__iafps = bodo.libs.interval_arr_ext.init_interval_array(
                fmu__csbht[:-1], fmu__csbht[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(nandt__iafps,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        fmu__csbht = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            fmu__csbht[0] = fmu__csbht[0] - 10.0 ** -precision
        nandt__iafps = bodo.libs.interval_arr_ext.init_interval_array(
            fmu__csbht[:-1], fmu__csbht[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(nandt__iafps,
            None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        yletc__szk = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        dmr__mdk = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        aclx__jrczi = np.zeros(nbins, np.int64)
        for zmjh__sgi in range(len(yletc__szk)):
            aclx__jrczi[dmr__mdk[zmjh__sgi]] = yletc__szk[zmjh__sgi]
        return aclx__jrczi
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
            brtk__vhepo = (max_val - min_val) * 0.001
            if right:
                bins[0] -= brtk__vhepo
            else:
                bins[-1] += brtk__vhepo
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    otil__wgam = dict(dropna=dropna)
    sevi__lpn = dict(dropna=True)
    check_unsupported_args('Series.value_counts', otil__wgam, sevi__lpn,
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
    sdcqk__ighf = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    qjyvq__slkr = 'def impl(\n'
    qjyvq__slkr += '    S,\n'
    qjyvq__slkr += '    normalize=False,\n'
    qjyvq__slkr += '    sort=True,\n'
    qjyvq__slkr += '    ascending=False,\n'
    qjyvq__slkr += '    bins=None,\n'
    qjyvq__slkr += '    dropna=True,\n'
    qjyvq__slkr += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    qjyvq__slkr += '):\n'
    qjyvq__slkr += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    qjyvq__slkr += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    qjyvq__slkr += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if sdcqk__ighf:
        qjyvq__slkr += '    right = True\n'
        qjyvq__slkr += _gen_bins_handling(bins, S.dtype)
        qjyvq__slkr += '    arr = get_bin_inds(bins, arr)\n'
    qjyvq__slkr += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    qjyvq__slkr += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    qjyvq__slkr += '    )\n'
    qjyvq__slkr += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if sdcqk__ighf:
        qjyvq__slkr += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        qjyvq__slkr += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        qjyvq__slkr += '    index = get_bin_labels(bins)\n'
    else:
        qjyvq__slkr += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        qjyvq__slkr += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        qjyvq__slkr += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        qjyvq__slkr += '    )\n'
        qjyvq__slkr += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    qjyvq__slkr += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        qjyvq__slkr += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        mpvlk__lybum = 'len(S)' if sdcqk__ighf else 'count_arr.sum()'
        qjyvq__slkr += f'    res = res / float({mpvlk__lybum})\n'
    qjyvq__slkr += '    return res\n'
    jaljw__bxy = {}
    exec(qjyvq__slkr, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, jaljw__bxy)
    impl = jaljw__bxy['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    qjyvq__slkr = ''
    if isinstance(bins, types.Integer):
        qjyvq__slkr += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        qjyvq__slkr += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            qjyvq__slkr += '    min_val = min_val.value\n'
            qjyvq__slkr += '    max_val = max_val.value\n'
        qjyvq__slkr += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            qjyvq__slkr += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        qjyvq__slkr += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return qjyvq__slkr


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    otil__wgam = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    sevi__lpn = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    qjyvq__slkr = 'def impl(\n'
    qjyvq__slkr += '    x,\n'
    qjyvq__slkr += '    bins,\n'
    qjyvq__slkr += '    right=True,\n'
    qjyvq__slkr += '    labels=None,\n'
    qjyvq__slkr += '    retbins=False,\n'
    qjyvq__slkr += '    precision=3,\n'
    qjyvq__slkr += '    include_lowest=False,\n'
    qjyvq__slkr += "    duplicates='raise',\n"
    qjyvq__slkr += '    ordered=True\n'
    qjyvq__slkr += '):\n'
    if isinstance(x, SeriesType):
        qjyvq__slkr += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        qjyvq__slkr += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        qjyvq__slkr += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        qjyvq__slkr += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    qjyvq__slkr += _gen_bins_handling(bins, x.dtype)
    qjyvq__slkr += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    qjyvq__slkr += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    qjyvq__slkr += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    qjyvq__slkr += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        qjyvq__slkr += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        qjyvq__slkr += '    return res\n'
    else:
        qjyvq__slkr += '    return out_arr\n'
    jaljw__bxy = {}
    exec(qjyvq__slkr, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, jaljw__bxy)
    impl = jaljw__bxy['impl']
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
    otil__wgam = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    sevi__lpn = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        ugxxo__wcd = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, ugxxo__wcd)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    otil__wgam = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    sevi__lpn = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', otil__wgam, sevi__lpn,
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
        lng__qlekq = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            vgdq__icm = bodo.utils.conversion.coerce_to_array(index)
            jszja__zop = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                vgdq__icm, arr), index, lng__qlekq)
            return jszja__zop.groupby(' ')['']
        return impl_index
    vgibq__ggjvy = by
    if isinstance(by, SeriesType):
        vgibq__ggjvy = by.data
    if isinstance(vgibq__ggjvy, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    yza__mwh = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        vgdq__icm = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        jszja__zop = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            vgdq__icm, arr), index, yza__mwh)
        return jszja__zop.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    otil__wgam = dict(verify_integrity=verify_integrity)
    sevi__lpn = dict(verify_integrity=False)
    check_unsupported_args('Series.append', otil__wgam, sevi__lpn,
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
            qfy__omhzr = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            aclx__jrczi = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(aclx__jrczi, A, qfy__omhzr, False)
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        aclx__jrczi = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    otil__wgam = dict(interpolation=interpolation)
    sevi__lpn = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            aclx__jrczi = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
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
        vnyz__orpp = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(vnyz__orpp, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    otil__wgam = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    sevi__lpn = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', otil__wgam, sevi__lpn,
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
        vhnej__gzl = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        vhnej__gzl = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    qjyvq__slkr = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {vhnej__gzl}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    beewa__sfjzv = dict()
    exec(qjyvq__slkr, {'bodo': bodo, 'numba': numba}, beewa__sfjzv)
    cazn__yjxvy = beewa__sfjzv['impl']
    return cazn__yjxvy


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        vhnej__gzl = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        vhnej__gzl = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    qjyvq__slkr = 'def impl(S,\n'
    qjyvq__slkr += '     value=None,\n'
    qjyvq__slkr += '    method=None,\n'
    qjyvq__slkr += '    axis=None,\n'
    qjyvq__slkr += '    inplace=False,\n'
    qjyvq__slkr += '    limit=None,\n'
    qjyvq__slkr += '   downcast=None,\n'
    qjyvq__slkr += '):\n'
    qjyvq__slkr += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    qjyvq__slkr += '    n = len(in_arr)\n'
    qjyvq__slkr += f'    out_arr = {vhnej__gzl}(n, -1)\n'
    qjyvq__slkr += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    qjyvq__slkr += '        s = in_arr[j]\n'
    qjyvq__slkr += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    qjyvq__slkr += '            s = value\n'
    qjyvq__slkr += '        out_arr[j] = s\n'
    qjyvq__slkr += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    beewa__sfjzv = dict()
    exec(qjyvq__slkr, {'bodo': bodo, 'numba': numba}, beewa__sfjzv)
    cazn__yjxvy = beewa__sfjzv['impl']
    return cazn__yjxvy


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
    skqu__vug = bodo.hiframes.pd_series_ext.get_series_data(value)
    for zmjh__sgi in numba.parfors.parfor.internal_prange(len(yxb__pgg)):
        s = yxb__pgg[zmjh__sgi]
        if bodo.libs.array_kernels.isna(yxb__pgg, zmjh__sgi
            ) and not bodo.libs.array_kernels.isna(skqu__vug, zmjh__sgi):
            s = skqu__vug[zmjh__sgi]
        yxb__pgg[zmjh__sgi] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
    for zmjh__sgi in numba.parfors.parfor.internal_prange(len(yxb__pgg)):
        s = yxb__pgg[zmjh__sgi]
        if bodo.libs.array_kernels.isna(yxb__pgg, zmjh__sgi):
            s = value
        yxb__pgg[zmjh__sgi] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    skqu__vug = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(yxb__pgg)
    aclx__jrczi = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for ukm__tghge in numba.parfors.parfor.internal_prange(n):
        s = yxb__pgg[ukm__tghge]
        if bodo.libs.array_kernels.isna(yxb__pgg, ukm__tghge
            ) and not bodo.libs.array_kernels.isna(skqu__vug, ukm__tghge):
            s = skqu__vug[ukm__tghge]
        aclx__jrczi[ukm__tghge] = s
        if bodo.libs.array_kernels.isna(yxb__pgg, ukm__tghge
            ) and bodo.libs.array_kernels.isna(skqu__vug, ukm__tghge):
            bodo.libs.array_kernels.setna(aclx__jrczi, ukm__tghge)
    return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    skqu__vug = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(yxb__pgg)
    aclx__jrczi = bodo.utils.utils.alloc_type(n, yxb__pgg.dtype, (-1,))
    for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
        s = yxb__pgg[zmjh__sgi]
        if bodo.libs.array_kernels.isna(yxb__pgg, zmjh__sgi
            ) and not bodo.libs.array_kernels.isna(skqu__vug, zmjh__sgi):
            s = skqu__vug[zmjh__sgi]
        aclx__jrczi[zmjh__sgi] = s
    return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    otil__wgam = dict(limit=limit, downcast=downcast)
    sevi__lpn = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')
    ggskd__gbny = not is_overload_none(value)
    ckdo__ygwni = not is_overload_none(method)
    if ggskd__gbny and ckdo__ygwni:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not ggskd__gbny and not ckdo__ygwni:
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
    if ckdo__ygwni:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        zmje__mqi = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(zmje__mqi)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(zmje__mqi)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    pmrf__idxh = element_type(S.data)
    ufsfy__zobjb = None
    if ggskd__gbny:
        ufsfy__zobjb = element_type(types.unliteral(value))
    if ufsfy__zobjb and not can_replace(pmrf__idxh, ufsfy__zobjb):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {ufsfy__zobjb} with series type {pmrf__idxh}'
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
        dgts__djhw = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                skqu__vug = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(yxb__pgg)
                aclx__jrczi = bodo.utils.utils.alloc_type(n, dgts__djhw, (-1,))
                for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(yxb__pgg, zmjh__sgi
                        ) and bodo.libs.array_kernels.isna(skqu__vug, zmjh__sgi
                        ):
                        bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                        continue
                    if bodo.libs.array_kernels.isna(yxb__pgg, zmjh__sgi):
                        aclx__jrczi[zmjh__sgi
                            ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                            skqu__vug[zmjh__sgi])
                        continue
                    aclx__jrczi[zmjh__sgi
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        yxb__pgg[zmjh__sgi])
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                    index, name)
            return fillna_series_impl
        if ckdo__ygwni:
            tgg__czx = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(pmrf__idxh, (types.Integer, types.Float)
                ) and pmrf__idxh not in tgg__czx:
                raise BodoError(
                    f"Series.fillna(): series of type {pmrf__idxh} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                aclx__jrczi = bodo.libs.array_kernels.ffill_bfill_arr(yxb__pgg,
                    method)
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_tz_naive_timestamp(value)
            yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(yxb__pgg)
            aclx__jrczi = bodo.utils.utils.alloc_type(n, dgts__djhw, (-1,))
            for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_tz_naive_timestamp(yxb__pgg
                    [zmjh__sgi])
                if bodo.libs.array_kernels.isna(yxb__pgg, zmjh__sgi):
                    s = value
                aclx__jrczi[zmjh__sgi] = s
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        isef__wognx = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        otil__wgam = dict(limit=limit, downcast=downcast)
        sevi__lpn = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', otil__wgam,
            sevi__lpn, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        pmrf__idxh = element_type(S.data)
        tgg__czx = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(pmrf__idxh, (types.Integer, types.Float)
            ) and pmrf__idxh not in tgg__czx:
            raise BodoError(
                f'Series.{overload_name}(): series of type {pmrf__idxh} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            aclx__jrczi = bodo.libs.array_kernels.ffill_bfill_arr(yxb__pgg,
                isef__wognx)
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        qcnwk__plw = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            qcnwk__plw)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        ptgv__ptz = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(ptgv__ptz)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        ptgv__ptz = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(ptgv__ptz)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        ptgv__ptz = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(ptgv__ptz)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    otil__wgam = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    urhov__ocqc = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', otil__wgam, urhov__ocqc,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    pmrf__idxh = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        oabzo__qzsj = element_type(to_replace.key_type)
        ufsfy__zobjb = element_type(to_replace.value_type)
    else:
        oabzo__qzsj = element_type(to_replace)
        ufsfy__zobjb = element_type(value)
    wdkf__eub = None
    if pmrf__idxh != types.unliteral(oabzo__qzsj):
        if bodo.utils.typing.equality_always_false(pmrf__idxh, types.
            unliteral(oabzo__qzsj)
            ) or not bodo.utils.typing.types_equality_exists(pmrf__idxh,
            oabzo__qzsj):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(pmrf__idxh, (types.Float, types.Integer)
            ) or pmrf__idxh == np.bool_:
            wdkf__eub = pmrf__idxh
    if not can_replace(pmrf__idxh, types.unliteral(ufsfy__zobjb)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    uuqv__idj = to_str_arr_if_dict_array(S.data)
    if isinstance(uuqv__idj, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(yxb__pgg.replace
                (to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(yxb__pgg)
        aclx__jrczi = bodo.utils.utils.alloc_type(n, uuqv__idj, (-1,))
        fdl__jdvlp = build_replace_dict(to_replace, value, wdkf__eub)
        for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(yxb__pgg, zmjh__sgi):
                bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                continue
            s = yxb__pgg[zmjh__sgi]
            if s in fdl__jdvlp:
                s = fdl__jdvlp[s]
            aclx__jrczi[zmjh__sgi] = s
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    can__yuy = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    ptqk__fgfs = is_iterable_type(to_replace)
    cwk__ikbjg = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    nlf__uzw = is_iterable_type(value)
    if can__yuy and cwk__ikbjg:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                fdl__jdvlp = {}
                fdl__jdvlp[key_dtype_conv(to_replace)] = value
                return fdl__jdvlp
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            fdl__jdvlp = {}
            fdl__jdvlp[to_replace] = value
            return fdl__jdvlp
        return impl
    if ptqk__fgfs and cwk__ikbjg:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                fdl__jdvlp = {}
                for atuxu__pvfy in to_replace:
                    fdl__jdvlp[key_dtype_conv(atuxu__pvfy)] = value
                return fdl__jdvlp
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            fdl__jdvlp = {}
            for atuxu__pvfy in to_replace:
                fdl__jdvlp[atuxu__pvfy] = value
            return fdl__jdvlp
        return impl
    if ptqk__fgfs and nlf__uzw:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                fdl__jdvlp = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for zmjh__sgi in range(len(to_replace)):
                    fdl__jdvlp[key_dtype_conv(to_replace[zmjh__sgi])] = value[
                        zmjh__sgi]
                return fdl__jdvlp
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            fdl__jdvlp = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for zmjh__sgi in range(len(to_replace)):
                fdl__jdvlp[to_replace[zmjh__sgi]] = value[zmjh__sgi]
            return fdl__jdvlp
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
            aclx__jrczi = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        aclx__jrczi = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    otil__wgam = dict(ignore_index=ignore_index)
    iwhs__btfzq = dict(ignore_index=False)
    check_unsupported_args('Series.explode', otil__wgam, iwhs__btfzq,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nsmmr__dhvyw = bodo.utils.conversion.index_to_array(index)
        aclx__jrczi, esgg__fag = bodo.libs.array_kernels.explode(arr,
            nsmmr__dhvyw)
        fyeus__bubrt = bodo.utils.conversion.index_from_array(esgg__fag)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
            fyeus__bubrt, name)
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
            ujk__eku = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                ujk__eku[zmjh__sgi] = np.argmax(a[zmjh__sgi])
            return ujk__eku
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            kavn__yvbm = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                kavn__yvbm[zmjh__sgi] = np.argmin(a[zmjh__sgi])
            return kavn__yvbm
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType) and isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            vyn__uzr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(b))
            return np.dot(arr, vyn__uzr)
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
    otil__wgam = dict(axis=axis, inplace=inplace, how=how)
    jneh__ujb = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', otil__wgam, jneh__ujb,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pplaz__chi = S.notna().values
            nsmmr__dhvyw = bodo.utils.conversion.extract_index_array(S)
            fyeus__bubrt = bodo.utils.conversion.convert_to_index(nsmmr__dhvyw
                [pplaz__chi])
            aclx__jrczi = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(yxb__pgg))
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                fyeus__bubrt, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            nsmmr__dhvyw = bodo.utils.conversion.extract_index_array(S)
            pplaz__chi = S.notna().values
            fyeus__bubrt = bodo.utils.conversion.convert_to_index(nsmmr__dhvyw
                [pplaz__chi])
            aclx__jrczi = yxb__pgg[pplaz__chi]
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                fyeus__bubrt, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    otil__wgam = dict(freq=freq, axis=axis)
    sevi__lpn = dict(freq=None, axis=0)
    check_unsupported_args('Series.shift', otil__wgam, sevi__lpn,
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
        aclx__jrczi = bodo.hiframes.rolling.shift(arr, periods, False,
            fill_value)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    otil__wgam = dict(fill_method=fill_method, limit=limit, freq=freq)
    sevi__lpn = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', otil__wgam, sevi__lpn,
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
        aclx__jrczi = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
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
            iqxv__hyf = 'None'
        else:
            iqxv__hyf = 'other'
        qjyvq__slkr = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            qjyvq__slkr += '  cond = ~cond\n'
        qjyvq__slkr += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        qjyvq__slkr += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qjyvq__slkr += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qjyvq__slkr += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {iqxv__hyf})\n'
            )
        qjyvq__slkr += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        jaljw__bxy = {}
        exec(qjyvq__slkr, {'bodo': bodo, 'np': np}, jaljw__bxy)
        impl = jaljw__bxy['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        qcnwk__plw = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(qcnwk__plw)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    otil__wgam = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    sevi__lpn = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', otil__wgam, sevi__lpn,
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
    iaem__ljfzo = is_overload_constant_nan(other)
    if not (is_default or iaem__ljfzo or is_scalar_type(other) or 
        isinstance(other, types.Array) and other.ndim >= 1 and other.ndim <=
        max_ndim or isinstance(other, SeriesType) and (isinstance(arr,
        types.Array) or arr.dtype in [bodo.string_type, bodo.bytes_type]) or
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
            jte__yak = arr.dtype.elem_type
        else:
            jte__yak = arr.dtype
        if is_iterable_type(other):
            mznh__kulao = other.dtype
        elif iaem__ljfzo:
            mznh__kulao = types.float64
        else:
            mznh__kulao = types.unliteral(other)
        if not iaem__ljfzo and not is_common_scalar_dtype([jte__yak,
            mznh__kulao]):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        otil__wgam = dict(level=level, axis=axis)
        sevi__lpn = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), otil__wgam,
            sevi__lpn, package_name='pandas', module_name='Series')
        ifmd__mbw = other == string_type or is_overload_constant_str(other)
        lgua__wjnz = is_iterable_type(other) and other.dtype == string_type
        arthl__sliwa = S.dtype == string_type and (op == operator.add and (
            ifmd__mbw or lgua__wjnz) or op == operator.mul and isinstance(
            other, types.Integer))
        fzkl__vedxq = S.dtype == bodo.timedelta64ns
        kknuj__ymal = S.dtype == bodo.datetime64ns
        dfpzx__fopg = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        flh__ljmce = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype ==
            pd_timestamp_tz_naive_type or other.dtype == bodo.datetime64ns)
        djgif__aavfc = fzkl__vedxq and (dfpzx__fopg or flh__ljmce
            ) or kknuj__ymal and dfpzx__fopg
        djgif__aavfc = djgif__aavfc and op == operator.add
        if not (isinstance(S.dtype, types.Number) or arthl__sliwa or
            djgif__aavfc):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        eqrz__eiaf = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            uuqv__idj = eqrz__eiaf.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and uuqv__idj == types.Array(types.bool_, 1, 'C'):
                uuqv__idj = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_tz_naive_timestamp(other
                    )
                n = len(arr)
                aclx__jrczi = bodo.utils.utils.alloc_type(n, uuqv__idj, (-1,))
                for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                    goki__sfv = bodo.libs.array_kernels.isna(arr, zmjh__sgi)
                    if goki__sfv:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(aclx__jrczi,
                                zmjh__sgi)
                        else:
                            aclx__jrczi[zmjh__sgi] = op(fill_value, other)
                    else:
                        aclx__jrczi[zmjh__sgi] = op(arr[zmjh__sgi], other)
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        uuqv__idj = eqrz__eiaf.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and uuqv__idj == types.Array(types.bool_, 1, 'C'):
            uuqv__idj = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            sbf__tfsk = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            aclx__jrczi = bodo.utils.utils.alloc_type(n, uuqv__idj, (-1,))
            for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                goki__sfv = bodo.libs.array_kernels.isna(arr, zmjh__sgi)
                doab__mbexv = bodo.libs.array_kernels.isna(sbf__tfsk, zmjh__sgi
                    )
                if goki__sfv and doab__mbexv:
                    bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                elif goki__sfv:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                    else:
                        aclx__jrczi[zmjh__sgi] = op(fill_value, sbf__tfsk[
                            zmjh__sgi])
                elif doab__mbexv:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                    else:
                        aclx__jrczi[zmjh__sgi] = op(arr[zmjh__sgi], fill_value)
                else:
                    aclx__jrczi[zmjh__sgi] = op(arr[zmjh__sgi], sbf__tfsk[
                        zmjh__sgi])
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
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
        eqrz__eiaf = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            uuqv__idj = eqrz__eiaf.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and uuqv__idj == types.Array(types.bool_, 1, 'C'):
                uuqv__idj = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                aclx__jrczi = bodo.utils.utils.alloc_type(n, uuqv__idj, None)
                for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                    goki__sfv = bodo.libs.array_kernels.isna(arr, zmjh__sgi)
                    if goki__sfv:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(aclx__jrczi,
                                zmjh__sgi)
                        else:
                            aclx__jrczi[zmjh__sgi] = op(other, fill_value)
                    else:
                        aclx__jrczi[zmjh__sgi] = op(other, arr[zmjh__sgi])
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        uuqv__idj = eqrz__eiaf.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and uuqv__idj == types.Array(types.bool_, 1, 'C'):
            uuqv__idj = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            sbf__tfsk = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            aclx__jrczi = bodo.utils.utils.alloc_type(n, uuqv__idj, None)
            for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                goki__sfv = bodo.libs.array_kernels.isna(arr, zmjh__sgi)
                doab__mbexv = bodo.libs.array_kernels.isna(sbf__tfsk, zmjh__sgi
                    )
                aclx__jrczi[zmjh__sgi] = op(sbf__tfsk[zmjh__sgi], arr[
                    zmjh__sgi])
                if goki__sfv and doab__mbexv:
                    bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                elif goki__sfv:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                    else:
                        aclx__jrczi[zmjh__sgi] = op(sbf__tfsk[zmjh__sgi],
                            fill_value)
                elif doab__mbexv:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                    else:
                        aclx__jrczi[zmjh__sgi] = op(fill_value, arr[zmjh__sgi])
                else:
                    aclx__jrczi[zmjh__sgi] = op(sbf__tfsk[zmjh__sgi], arr[
                        zmjh__sgi])
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
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
    for op, qzk__xir in explicit_binop_funcs_two_ways.items():
        for name in qzk__xir:
            qcnwk__plw = create_explicit_binary_op_overload(op)
            phmlz__onh = create_explicit_binary_reverse_op_overload(op)
            gtwke__vbnor = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(qcnwk__plw)
            overload_method(SeriesType, gtwke__vbnor, no_unliteral=True)(
                phmlz__onh)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        qcnwk__plw = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(qcnwk__plw)
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
                vlwkt__rpso = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                aclx__jrczi = dt64_arr_sub(arr, vlwkt__rpso)
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
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
                aclx__jrczi = np.empty(n, np.dtype('datetime64[ns]'))
                for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, zmjh__sgi):
                        bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                        continue
                    oqvvi__xkhdw = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[zmjh__sgi]))
                    xmde__iro = op(oqvvi__xkhdw, rhs)
                    aclx__jrczi[zmjh__sgi
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xmde__iro.value)
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
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
                    vlwkt__rpso = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    aclx__jrczi = op(arr, bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(vlwkt__rpso))
                    return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vlwkt__rpso = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                aclx__jrczi = op(arr, vlwkt__rpso)
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    gkmcg__dxm = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    aclx__jrczi = op(bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(gkmcg__dxm), arr)
                    return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                gkmcg__dxm = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                aclx__jrczi = op(gkmcg__dxm, arr)
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        qcnwk__plw = create_binary_op_overload(op)
        overload(op)(qcnwk__plw)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    grhlz__oyzk = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, grhlz__oyzk)
        for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, zmjh__sgi
                ) or bodo.libs.array_kernels.isna(arg2, zmjh__sgi):
                bodo.libs.array_kernels.setna(S, zmjh__sgi)
                continue
            S[zmjh__sgi
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                zmjh__sgi]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[zmjh__sgi]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                sbf__tfsk = bodo.utils.conversion.get_array_if_series_or_index(
                    other)
                op(arr, sbf__tfsk)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        qcnwk__plw = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(qcnwk__plw)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                aclx__jrczi = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        qcnwk__plw = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(qcnwk__plw)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    aclx__jrczi = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
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
                    sbf__tfsk = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    aclx__jrczi = ufunc(arr, sbf__tfsk)
                    return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    sbf__tfsk = bodo.hiframes.pd_series_ext.get_series_data(S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    aclx__jrczi = ufunc(arr, sbf__tfsk)
                    return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        qcnwk__plw = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(qcnwk__plw)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        fseh__fgrty = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        qlhoh__yvxjy = np.arange(n),
        bodo.libs.timsort.sort(fseh__fgrty, 0, n, qlhoh__yvxjy)
        return qlhoh__yvxjy[0]
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
        rga__xlgmn = get_overload_const_str(downcast)
        if rga__xlgmn in ('integer', 'signed'):
            out_dtype = types.int64
        elif rga__xlgmn == 'unsigned':
            out_dtype = types.uint64
        else:
            assert rga__xlgmn == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            yxb__pgg = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            aclx__jrczi = pd.to_numeric(yxb__pgg, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if arg_a == bodo.dict_str_arr_type:
        return (lambda arg_a, errors='raise', downcast=None: bodo.libs.
            dict_arr_ext.dict_arr_to_numeric(arg_a, errors, downcast))
    lszf__cvwi = types.Array(types.float64, 1, 'C'
        ) if out_dtype == types.float64 else IntegerArrayType(types.int64)

    def to_numeric_impl(arg_a, errors='raise', downcast=None):
        numba.parfors.parfor.init_prange()
        n = len(arg_a)
        goq__zge = bodo.utils.utils.alloc_type(n, lszf__cvwi, (-1,))
        for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg_a, zmjh__sgi):
                bodo.libs.array_kernels.setna(goq__zge, zmjh__sgi)
            else:
                bodo.libs.str_arr_ext.str_arr_item_to_numeric(goq__zge,
                    zmjh__sgi, arg_a, zmjh__sgi)
        return goq__zge
    return to_numeric_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lmq__mlvtk = if_series_to_array_type(args[0])
        if isinstance(lmq__mlvtk, types.Array) and isinstance(lmq__mlvtk.
            dtype, types.Integer):
            lmq__mlvtk = types.Array(types.float64, 1, 'C')
        return lmq__mlvtk(*args)


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
    xpqzi__dknnc = bodo.utils.utils.is_array_typ(x, True)
    tqj__rrkds = bodo.utils.utils.is_array_typ(y, True)
    qjyvq__slkr = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        qjyvq__slkr += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if xpqzi__dknnc and not bodo.utils.utils.is_array_typ(x, False):
        qjyvq__slkr += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if tqj__rrkds and not bodo.utils.utils.is_array_typ(y, False):
        qjyvq__slkr += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    qjyvq__slkr += '  n = len(condition)\n'
    owwu__gvo = x.dtype if xpqzi__dknnc else types.unliteral(x)
    tgfxk__zlsa = y.dtype if tqj__rrkds else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        owwu__gvo = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        tgfxk__zlsa = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    ppaps__rxaya = get_data(x)
    hbd__mzn = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(qlhoh__yvxjy) for
        qlhoh__yvxjy in [ppaps__rxaya, hbd__mzn])
    if hbd__mzn == types.none:
        if isinstance(owwu__gvo, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif ppaps__rxaya == hbd__mzn and not is_nullable:
        out_dtype = dtype_to_array_type(owwu__gvo)
    elif owwu__gvo == string_type or tgfxk__zlsa == string_type:
        out_dtype = bodo.string_array_type
    elif ppaps__rxaya == bytes_type or (xpqzi__dknnc and owwu__gvo ==
        bytes_type) and (hbd__mzn == bytes_type or tqj__rrkds and 
        tgfxk__zlsa == bytes_type):
        out_dtype = binary_array_type
    elif isinstance(owwu__gvo, bodo.PDCategoricalDtype):
        out_dtype = None
    elif owwu__gvo in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(owwu__gvo, 1, 'C')
    elif tgfxk__zlsa in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(tgfxk__zlsa, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(owwu__gvo), numba.np.numpy_support.
            as_dtype(tgfxk__zlsa)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(owwu__gvo, bodo.PDCategoricalDtype):
        jka__ksbtd = 'x'
    else:
        jka__ksbtd = 'out_dtype'
    qjyvq__slkr += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {jka__ksbtd}, (-1,))\n')
    if isinstance(owwu__gvo, bodo.PDCategoricalDtype):
        qjyvq__slkr += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        qjyvq__slkr += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    qjyvq__slkr += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    qjyvq__slkr += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if xpqzi__dknnc:
        qjyvq__slkr += '      if bodo.libs.array_kernels.isna(x, j):\n'
        qjyvq__slkr += '        setna(out_arr, j)\n'
        qjyvq__slkr += '        continue\n'
    if isinstance(owwu__gvo, bodo.PDCategoricalDtype):
        qjyvq__slkr += '      out_codes[j] = x_codes[j]\n'
    else:
        qjyvq__slkr += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('x[j]' if xpqzi__dknnc else 'x'))
    qjyvq__slkr += '    else:\n'
    if tqj__rrkds:
        qjyvq__slkr += '      if bodo.libs.array_kernels.isna(y, j):\n'
        qjyvq__slkr += '        setna(out_arr, j)\n'
        qjyvq__slkr += '        continue\n'
    if hbd__mzn == types.none:
        if isinstance(owwu__gvo, bodo.PDCategoricalDtype):
            qjyvq__slkr += '      out_codes[j] = -1\n'
        else:
            qjyvq__slkr += '      setna(out_arr, j)\n'
    else:
        qjyvq__slkr += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('y[j]' if tqj__rrkds else 'y'))
    qjyvq__slkr += '  return out_arr\n'
    jaljw__bxy = {}
    exec(qjyvq__slkr, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, jaljw__bxy)
    czzec__wpihw = jaljw__bxy['_impl']
    return czzec__wpihw


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
        gbai__djmzs = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(gbai__djmzs, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(gbai__djmzs):
            xuxm__ofbu = gbai__djmzs.data.dtype
        else:
            xuxm__ofbu = gbai__djmzs.dtype
        if isinstance(xuxm__ofbu, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        aql__fazt = gbai__djmzs
    else:
        lybl__mngkp = []
        for gbai__djmzs in choicelist:
            if not bodo.utils.utils.is_array_typ(gbai__djmzs, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(gbai__djmzs):
                xuxm__ofbu = gbai__djmzs.data.dtype
            else:
                xuxm__ofbu = gbai__djmzs.dtype
            if isinstance(xuxm__ofbu, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            lybl__mngkp.append(xuxm__ofbu)
        if not is_common_scalar_dtype(lybl__mngkp):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        aql__fazt = choicelist[0]
    if is_series_type(aql__fazt):
        aql__fazt = aql__fazt.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, aql__fazt.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(aql__fazt, types.Array) or isinstance(aql__fazt,
        BooleanArrayType) or isinstance(aql__fazt, IntegerArrayType) or
        isinstance(aql__fazt, FloatingArrayType) or bodo.utils.utils.
        is_array_typ(aql__fazt, False) and aql__fazt.dtype in [bodo.
        string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {aql__fazt} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    kyjjs__vgtn = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        orc__zbp = choicelist.dtype
    else:
        ojg__aroyb = False
        lybl__mngkp = []
        for gbai__djmzs in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                gbai__djmzs, 'numpy.select()')
            if is_nullable_type(gbai__djmzs):
                ojg__aroyb = True
            if is_series_type(gbai__djmzs):
                xuxm__ofbu = gbai__djmzs.data.dtype
            else:
                xuxm__ofbu = gbai__djmzs.dtype
            if isinstance(xuxm__ofbu, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            lybl__mngkp.append(xuxm__ofbu)
        uihnm__zqvj, komz__clr = get_common_scalar_dtype(lybl__mngkp)
        if not komz__clr:
            raise BodoError('Internal error in overload_np_select')
        kjj__butev = dtype_to_array_type(uihnm__zqvj)
        if ojg__aroyb:
            kjj__butev = to_nullable_type(kjj__butev)
        orc__zbp = kjj__butev
    if isinstance(orc__zbp, SeriesType):
        orc__zbp = orc__zbp.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        dkszf__omkc = True
    else:
        dkszf__omkc = False
    crmxq__ldsk = False
    goknl__mum = False
    if dkszf__omkc:
        if isinstance(orc__zbp.dtype, types.Number):
            pass
        elif orc__zbp.dtype == types.bool_:
            goknl__mum = True
        else:
            crmxq__ldsk = True
            orc__zbp = to_nullable_type(orc__zbp)
    elif default == types.none or is_overload_constant_nan(default):
        crmxq__ldsk = True
        orc__zbp = to_nullable_type(orc__zbp)
    qjyvq__slkr = 'def np_select_impl(condlist, choicelist, default=0):\n'
    qjyvq__slkr += '  if len(condlist) != len(choicelist):\n'
    qjyvq__slkr += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    qjyvq__slkr += '  output_len = len(choicelist[0])\n'
    qjyvq__slkr += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    qjyvq__slkr += '  for i in range(output_len):\n'
    if crmxq__ldsk:
        qjyvq__slkr += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif goknl__mum:
        qjyvq__slkr += '    out[i] = False\n'
    else:
        qjyvq__slkr += '    out[i] = default\n'
    if kyjjs__vgtn:
        qjyvq__slkr += '  for i in range(len(condlist) - 1, -1, -1):\n'
        qjyvq__slkr += '    cond = condlist[i]\n'
        qjyvq__slkr += '    choice = choicelist[i]\n'
        qjyvq__slkr += '    out = np.where(cond, choice, out)\n'
    else:
        for zmjh__sgi in range(len(choicelist) - 1, -1, -1):
            qjyvq__slkr += f'  cond = condlist[{zmjh__sgi}]\n'
            qjyvq__slkr += f'  choice = choicelist[{zmjh__sgi}]\n'
            qjyvq__slkr += f'  out = np.where(cond, choice, out)\n'
    qjyvq__slkr += '  return out'
    jaljw__bxy = dict()
    exec(qjyvq__slkr, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': orc__zbp}, jaljw__bxy)
    impl = jaljw__bxy['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        aclx__jrczi = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    otil__wgam = dict(subset=subset, keep=keep, inplace=inplace)
    sevi__lpn = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', otil__wgam, sevi__lpn,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        bvedc__xzcy = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (bvedc__xzcy,), nsmmr__dhvyw = bodo.libs.array_kernels.drop_duplicates(
            (bvedc__xzcy,), index, 1)
        index = bodo.utils.conversion.index_from_array(nsmmr__dhvyw)
        return bodo.hiframes.pd_series_ext.init_series(bvedc__xzcy, index, name
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
    dhuls__ydm = element_type(S.data)
    if not is_common_scalar_dtype([dhuls__ydm, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([dhuls__ydm, right]):
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
        aclx__jrczi = bodo.libs.bool_arr_ext.alloc_bool_array(n)
        for zmjh__sgi in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arr, zmjh__sgi):
                bodo.libs.array_kernels.setna(aclx__jrczi, zmjh__sgi)
                continue
            cfor__rnr = bodo.utils.conversion.box_if_dt64(arr[zmjh__sgi])
            if inclusive == 'both':
                aclx__jrczi[zmjh__sgi
                    ] = cfor__rnr <= right and cfor__rnr >= left
            else:
                aclx__jrczi[zmjh__sgi] = cfor__rnr < right and cfor__rnr > left
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi, index, name
            )
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    otil__wgam = dict(axis=axis)
    sevi__lpn = dict(axis=None)
    check_unsupported_args('Series.repeat', otil__wgam, sevi__lpn,
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
            nsmmr__dhvyw = bodo.utils.conversion.index_to_array(index)
            aclx__jrczi = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            esgg__fag = bodo.libs.array_kernels.repeat_kernel(nsmmr__dhvyw,
                repeats)
            fyeus__bubrt = bodo.utils.conversion.index_from_array(esgg__fag)
            return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
                fyeus__bubrt, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nsmmr__dhvyw = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        aclx__jrczi = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        esgg__fag = bodo.libs.array_kernels.repeat_kernel(nsmmr__dhvyw, repeats
            )
        fyeus__bubrt = bodo.utils.conversion.index_from_array(esgg__fag)
        return bodo.hiframes.pd_series_ext.init_series(aclx__jrczi,
            fyeus__bubrt, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        qlhoh__yvxjy = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(qlhoh__yvxjy)
        wbo__gdh = {}
        for zmjh__sgi in range(n):
            cfor__rnr = bodo.utils.conversion.box_if_dt64(qlhoh__yvxjy[
                zmjh__sgi])
            wbo__gdh[index[zmjh__sgi]] = cfor__rnr
        return wbo__gdh
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    zmje__mqi = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            hrfez__ytg = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(zmje__mqi)
    elif is_literal_type(name):
        hrfez__ytg = get_literal_value(name)
    else:
        raise_bodo_error(zmje__mqi)
    hrfez__ytg = 0 if hrfez__ytg is None else hrfez__ytg
    eaihn__zik = ColNamesMetaType((hrfez__ytg,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            eaihn__zik)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
