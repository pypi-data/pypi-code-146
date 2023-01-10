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
            tewgo__qsx = bodo.hiframes.pd_series_ext.get_series_data(s)
            ceti__hwyb = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                tewgo__qsx)
            return ceti__hwyb
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
            mab__atxsk = list()
            for nhuyr__safl in range(len(S)):
                mab__atxsk.append(S.iat[nhuyr__safl])
            return mab__atxsk
        return impl_float

    def impl(S):
        mab__atxsk = list()
        for nhuyr__safl in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, nhuyr__safl):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            mab__atxsk.append(S.iat[nhuyr__safl])
        return mab__atxsk
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    msu__cuyrl = dict(dtype=dtype, copy=copy, na_value=na_value)
    ava__kma = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    msu__cuyrl = dict(name=name, inplace=inplace)
    ava__kma = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', msu__cuyrl, ava__kma,
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
        kds__vqir = ', '.join(['index_arrs[{}]'.format(nhuyr__safl) for
            nhuyr__safl in range(S.index.nlevels)])
    else:
        kds__vqir = '    bodo.utils.conversion.index_to_array(index)\n'
    gzz__iow = 'index' if 'index' != series_name else 'level_0'
    hui__ttltf = get_index_names(S.index, 'Series.reset_index()', gzz__iow)
    columns = [name for name in hui__ttltf]
    columns.append(series_name)
    mbds__arjnf = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    mbds__arjnf += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    mbds__arjnf += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        mbds__arjnf += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    mbds__arjnf += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    mbds__arjnf += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({kds__vqir}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    ugf__sfq = {}
    exec(mbds__arjnf, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, ugf__sfq)
    yretj__sxsrv = ugf__sfq['_impl']
    return yretj__sxsrv


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        uyezw__qkqjs = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
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
        uyezw__qkqjs = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[nhuyr__safl]):
                bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl)
            else:
                uyezw__qkqjs[nhuyr__safl] = np.round(arr[nhuyr__safl], decimals
                    )
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    msu__cuyrl = dict(level=level, numeric_only=numeric_only)
    ava__kma = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
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
    msu__cuyrl = dict(level=level, numeric_only=numeric_only)
    ava__kma = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', msu__cuyrl, ava__kma,
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
    msu__cuyrl = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    ava__kma = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
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
        naza__jng = bodo.hiframes.pd_series_ext.get_series_data(S)
        ftbuu__skgrk = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        grn__qwp = 0
        for nhuyr__safl in numba.parfors.parfor.internal_prange(len(naza__jng)
            ):
            ikzkj__zxb = 0
            dnp__hmni = bodo.libs.array_kernels.isna(naza__jng, nhuyr__safl)
            nrfn__khr = bodo.libs.array_kernels.isna(ftbuu__skgrk, nhuyr__safl)
            if dnp__hmni and not nrfn__khr or not dnp__hmni and nrfn__khr:
                ikzkj__zxb = 1
            elif not dnp__hmni:
                if naza__jng[nhuyr__safl] != ftbuu__skgrk[nhuyr__safl]:
                    ikzkj__zxb = 1
            grn__qwp += ikzkj__zxb
        return grn__qwp == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    msu__cuyrl = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    ava__kma = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    msu__cuyrl = dict(level=level)
    ava__kma = dict(level=None)
    check_unsupported_args('Series.mad', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    jul__kml = types.float64
    bbos__jdea = types.float64
    if S.dtype == types.float32:
        jul__kml = types.float32
        bbos__jdea = types.float32
    gypx__jouw = jul__kml(0)
    qknb__qqd = bbos__jdea(0)
    jncud__iiu = bbos__jdea(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        bodu__zfijm = gypx__jouw
        grn__qwp = qknb__qqd
        for nhuyr__safl in numba.parfors.parfor.internal_prange(len(A)):
            ikzkj__zxb = gypx__jouw
            rclrh__hsswq = qknb__qqd
            if not bodo.libs.array_kernels.isna(A, nhuyr__safl) or not skipna:
                ikzkj__zxb = A[nhuyr__safl]
                rclrh__hsswq = jncud__iiu
            bodu__zfijm += ikzkj__zxb
            grn__qwp += rclrh__hsswq
        taii__ptxy = bodo.hiframes.series_kernels._mean_handle_nan(bodu__zfijm,
            grn__qwp)
        ppwiv__xnyq = gypx__jouw
        for nhuyr__safl in numba.parfors.parfor.internal_prange(len(A)):
            ikzkj__zxb = gypx__jouw
            if not bodo.libs.array_kernels.isna(A, nhuyr__safl) or not skipna:
                ikzkj__zxb = abs(A[nhuyr__safl] - taii__ptxy)
            ppwiv__xnyq += ikzkj__zxb
        oujea__xmw = bodo.hiframes.series_kernels._mean_handle_nan(ppwiv__xnyq,
            grn__qwp)
        return oujea__xmw
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    msu__cuyrl = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    ava__kma = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', msu__cuyrl, ava__kma,
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
    msu__cuyrl = dict(level=level, numeric_only=numeric_only)
    ava__kma = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
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
        btpyc__rtfk = 0
        tmm__igld = 0
        grn__qwp = 0
        for nhuyr__safl in numba.parfors.parfor.internal_prange(len(A)):
            ikzkj__zxb = 0
            rclrh__hsswq = 0
            if not bodo.libs.array_kernels.isna(A, nhuyr__safl) or not skipna:
                ikzkj__zxb = A[nhuyr__safl]
                rclrh__hsswq = 1
            btpyc__rtfk += ikzkj__zxb
            tmm__igld += ikzkj__zxb * ikzkj__zxb
            grn__qwp += rclrh__hsswq
        nqhm__gupny = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            btpyc__rtfk, tmm__igld, grn__qwp, ddof)
        xjq__pptp = bodo.hiframes.series_kernels._sem_handle_nan(nqhm__gupny,
            grn__qwp)
        return xjq__pptp
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    msu__cuyrl = dict(level=level, numeric_only=numeric_only)
    ava__kma = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', msu__cuyrl, ava__kma,
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
        btpyc__rtfk = 0.0
        tmm__igld = 0.0
        bkuwi__mzzgo = 0.0
        yjue__cihg = 0.0
        grn__qwp = 0
        for nhuyr__safl in numba.parfors.parfor.internal_prange(len(A)):
            ikzkj__zxb = 0.0
            rclrh__hsswq = 0
            if not bodo.libs.array_kernels.isna(A, nhuyr__safl) or not skipna:
                ikzkj__zxb = np.float64(A[nhuyr__safl])
                rclrh__hsswq = 1
            btpyc__rtfk += ikzkj__zxb
            tmm__igld += ikzkj__zxb ** 2
            bkuwi__mzzgo += ikzkj__zxb ** 3
            yjue__cihg += ikzkj__zxb ** 4
            grn__qwp += rclrh__hsswq
        nqhm__gupny = bodo.hiframes.series_kernels.compute_kurt(btpyc__rtfk,
            tmm__igld, bkuwi__mzzgo, yjue__cihg, grn__qwp)
        return nqhm__gupny
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    msu__cuyrl = dict(level=level, numeric_only=numeric_only)
    ava__kma = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', msu__cuyrl, ava__kma,
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
        btpyc__rtfk = 0.0
        tmm__igld = 0.0
        bkuwi__mzzgo = 0.0
        grn__qwp = 0
        for nhuyr__safl in numba.parfors.parfor.internal_prange(len(A)):
            ikzkj__zxb = 0.0
            rclrh__hsswq = 0
            if not bodo.libs.array_kernels.isna(A, nhuyr__safl) or not skipna:
                ikzkj__zxb = np.float64(A[nhuyr__safl])
                rclrh__hsswq = 1
            btpyc__rtfk += ikzkj__zxb
            tmm__igld += ikzkj__zxb ** 2
            bkuwi__mzzgo += ikzkj__zxb ** 3
            grn__qwp += rclrh__hsswq
        nqhm__gupny = bodo.hiframes.series_kernels.compute_skew(btpyc__rtfk,
            tmm__igld, bkuwi__mzzgo, grn__qwp)
        return nqhm__gupny
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    msu__cuyrl = dict(level=level, numeric_only=numeric_only)
    ava__kma = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
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
    msu__cuyrl = dict(level=level, numeric_only=numeric_only)
    ava__kma = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
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
        naza__jng = bodo.hiframes.pd_series_ext.get_series_data(S)
        ftbuu__skgrk = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        zxweu__ayd = 0
        for nhuyr__safl in numba.parfors.parfor.internal_prange(len(naza__jng)
            ):
            ljhfs__ohvh = naza__jng[nhuyr__safl]
            exj__foprd = ftbuu__skgrk[nhuyr__safl]
            zxweu__ayd += ljhfs__ohvh * exj__foprd
        return zxweu__ayd
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    msu__cuyrl = dict(skipna=skipna)
    ava__kma = dict(skipna=True)
    check_unsupported_args('Series.cumsum', msu__cuyrl, ava__kma,
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
    msu__cuyrl = dict(skipna=skipna)
    ava__kma = dict(skipna=True)
    check_unsupported_args('Series.cumprod', msu__cuyrl, ava__kma,
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
    msu__cuyrl = dict(skipna=skipna)
    ava__kma = dict(skipna=True)
    check_unsupported_args('Series.cummin', msu__cuyrl, ava__kma,
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
    msu__cuyrl = dict(skipna=skipna)
    ava__kma = dict(skipna=True)
    check_unsupported_args('Series.cummax', msu__cuyrl, ava__kma,
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
    msu__cuyrl = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    ava__kma = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        zbi__ymtns = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, zbi__ymtns, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    msu__cuyrl = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    ava__kma = dict(index=None, columns=None, axis=None, copy=True, inplace
        =False)
    check_unsupported_args('Series.rename_axis', msu__cuyrl, ava__kma,
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
    azvmc__esjis = S.data

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(A)
        uyezw__qkqjs = bodo.utils.utils.alloc_type(n, azvmc__esjis, (-1,))
        for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, nhuyr__safl):
                bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl)
                continue
            uyezw__qkqjs[nhuyr__safl] = np.abs(A[nhuyr__safl])
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    msu__cuyrl = dict(level=level)
    ava__kma = dict(level=None)
    check_unsupported_args('Series.count', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    msu__cuyrl = dict(method=method, min_periods=min_periods)
    ava__kma = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        hyigw__gjh = S.sum()
        zav__mwf = other.sum()
        a = n * (S * other).sum() - hyigw__gjh * zav__mwf
        ixheo__ftg = n * (S ** 2).sum() - hyigw__gjh ** 2
        kxx__qotkx = n * (other ** 2).sum() - zav__mwf ** 2
        return a / np.sqrt(ixheo__ftg * kxx__qotkx)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    msu__cuyrl = dict(min_periods=min_periods)
    ava__kma = dict(min_periods=None)
    check_unsupported_args('Series.cov', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        hyigw__gjh = S.mean()
        zav__mwf = other.mean()
        xvk__vsu = ((S - hyigw__gjh) * (other - zav__mwf)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(xvk__vsu, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            ttl__gze = np.sign(sum_val)
            return np.inf * ttl__gze
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    msu__cuyrl = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    ava__kma = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        huopp__zkwe = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            min_val = bodo.libs.array_ops.array_op_min(arr)
            return convert_val_to_timestamp(min_val.value, tz=huopp__zkwe)
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
    msu__cuyrl = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    ava__kma = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        huopp__zkwe = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            max_val = bodo.libs.array_ops.array_op_max(arr)
            return convert_val_to_timestamp(max_val.value, tz=huopp__zkwe)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    msu__cuyrl = dict(axis=axis, skipna=skipna)
    ava__kma = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', msu__cuyrl, ava__kma,
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
    msu__cuyrl = dict(axis=axis, skipna=skipna)
    ava__kma = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', msu__cuyrl, ava__kma,
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
    msu__cuyrl = dict(level=level, numeric_only=numeric_only)
    ava__kma = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', msu__cuyrl, ava__kma,
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
        ueonl__bysq = arr[:n]
        rnswv__fur = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(ueonl__bysq,
            rnswv__fur, name)
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
        fvxsv__vray = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ueonl__bysq = arr[fvxsv__vray:]
        rnswv__fur = index[fvxsv__vray:]
        return bodo.hiframes.pd_series_ext.init_series(ueonl__bysq,
            rnswv__fur, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    aff__ahiiy = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in aff__ahiiy:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            tygr__rrg = index[0]
            lxa__soddx = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, tygr__rrg,
                False))
        else:
            lxa__soddx = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ueonl__bysq = arr[:lxa__soddx]
        rnswv__fur = index[:lxa__soddx]
        return bodo.hiframes.pd_series_ext.init_series(ueonl__bysq,
            rnswv__fur, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    aff__ahiiy = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in aff__ahiiy:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            ysk__rrvl = index[-1]
            lxa__soddx = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, ysk__rrvl,
                True))
        else:
            lxa__soddx = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ueonl__bysq = arr[len(arr) - lxa__soddx:]
        rnswv__fur = index[len(arr) - lxa__soddx:]
        return bodo.hiframes.pd_series_ext.init_series(ueonl__bysq,
            rnswv__fur, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        gyfbm__ael = bodo.utils.conversion.index_to_array(index)
        miw__tvw, zspsn__jyc = bodo.libs.array_kernels.first_last_valid_index(
            arr, gyfbm__ael)
        return zspsn__jyc if miw__tvw else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        gyfbm__ael = bodo.utils.conversion.index_to_array(index)
        miw__tvw, zspsn__jyc = bodo.libs.array_kernels.first_last_valid_index(
            arr, gyfbm__ael, False)
        return zspsn__jyc if miw__tvw else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    msu__cuyrl = dict(keep=keep)
    ava__kma = dict(keep='first')
    check_unsupported_args('Series.nlargest', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        gyfbm__ael = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        uyezw__qkqjs, xcjde__ors = bodo.libs.array_kernels.nlargest(arr,
            gyfbm__ael, n, True, bodo.hiframes.series_kernels.gt_f)
        mfj__fuiyd = bodo.utils.conversion.convert_to_index(xcjde__ors)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
            mfj__fuiyd, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    msu__cuyrl = dict(keep=keep)
    ava__kma = dict(keep='first')
    check_unsupported_args('Series.nsmallest', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        gyfbm__ael = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        uyezw__qkqjs, xcjde__ors = bodo.libs.array_kernels.nlargest(arr,
            gyfbm__ael, n, False, bodo.hiframes.series_kernels.lt_f)
        mfj__fuiyd = bodo.utils.conversion.convert_to_index(xcjde__ors)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
            mfj__fuiyd, name)
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
    msu__cuyrl = dict(errors=errors)
    ava__kma = dict(errors='raise')
    check_unsupported_args('Series.astype', msu__cuyrl, ava__kma,
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
        uyezw__qkqjs = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    msu__cuyrl = dict(axis=axis, is_copy=is_copy)
    ava__kma = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        tpowx__otqqq = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[tpowx__otqqq],
            index[tpowx__otqqq], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    msu__cuyrl = dict(axis=axis, kind=kind, order=order)
    ava__kma = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nrscd__jhb = S.notna().values
        if not nrscd__jhb.all():
            uyezw__qkqjs = np.full(n, -1, np.int64)
            uyezw__qkqjs[nrscd__jhb] = argsort(arr[nrscd__jhb])
        else:
            uyezw__qkqjs = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    msu__cuyrl = dict(axis=axis, numeric_only=numeric_only)
    ava__kma = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', msu__cuyrl, ava__kma,
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
        uyezw__qkqjs = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    msu__cuyrl = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    ava__kma = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    tsk__uerq = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        byn__nkxm = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, tsk__uerq)
        mqe__boaja = byn__nkxm.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        uyezw__qkqjs = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            mqe__boaja, 0)
        mfj__fuiyd = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            mqe__boaja)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
            mfj__fuiyd, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    msu__cuyrl = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    ava__kma = dict(axis=0, inplace=False, kind='quicksort', ignore_index=
        False, key=None)
    check_unsupported_args('Series.sort_values', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    uzob__eomid = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        byn__nkxm = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, uzob__eomid)
        mqe__boaja = byn__nkxm.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        uyezw__qkqjs = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            mqe__boaja, 0)
        mfj__fuiyd = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            mqe__boaja)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
            mfj__fuiyd, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    hfdth__dtjcb = is_overload_true(is_nullable)
    mbds__arjnf = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    mbds__arjnf += '  numba.parfors.parfor.init_prange()\n'
    mbds__arjnf += '  n = len(arr)\n'
    if hfdth__dtjcb:
        mbds__arjnf += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        mbds__arjnf += '  out_arr = np.empty(n, np.int64)\n'
    mbds__arjnf += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    mbds__arjnf += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if hfdth__dtjcb:
        mbds__arjnf += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        mbds__arjnf += '      out_arr[i] = -1\n'
    mbds__arjnf += '      continue\n'
    mbds__arjnf += '    val = arr[i]\n'
    mbds__arjnf += '    if include_lowest and val == bins[0]:\n'
    mbds__arjnf += '      ind = 1\n'
    mbds__arjnf += '    else:\n'
    mbds__arjnf += '      ind = np.searchsorted(bins, val)\n'
    mbds__arjnf += '    if ind == 0 or ind == len(bins):\n'
    if hfdth__dtjcb:
        mbds__arjnf += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        mbds__arjnf += '      out_arr[i] = -1\n'
    mbds__arjnf += '    else:\n'
    mbds__arjnf += '      out_arr[i] = ind - 1\n'
    mbds__arjnf += '  return out_arr\n'
    ugf__sfq = {}
    exec(mbds__arjnf, {'bodo': bodo, 'np': np, 'numba': numba}, ugf__sfq)
    impl = ugf__sfq['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        idvcj__vpugi, xfcrr__godhb = np.divmod(x, 1)
        if idvcj__vpugi == 0:
            tfh__oapyn = -int(np.floor(np.log10(abs(xfcrr__godhb)))
                ) - 1 + precision
        else:
            tfh__oapyn = precision
        return np.around(x, tfh__oapyn)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        sihsu__avsi = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(sihsu__avsi)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        ekza__tvmgs = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            cxa__tsfyu = bins.copy()
            if right and include_lowest:
                cxa__tsfyu[0] = cxa__tsfyu[0] - ekza__tvmgs
            flx__lhty = bodo.libs.interval_arr_ext.init_interval_array(
                cxa__tsfyu[:-1], cxa__tsfyu[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(flx__lhty,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        cxa__tsfyu = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            cxa__tsfyu[0] = cxa__tsfyu[0] - 10.0 ** -precision
        flx__lhty = bodo.libs.interval_arr_ext.init_interval_array(cxa__tsfyu
            [:-1], cxa__tsfyu[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(flx__lhty, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        ndi__eiu = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        cex__eyma = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        uyezw__qkqjs = np.zeros(nbins, np.int64)
        for nhuyr__safl in range(len(ndi__eiu)):
            uyezw__qkqjs[cex__eyma[nhuyr__safl]] = ndi__eiu[nhuyr__safl]
        return uyezw__qkqjs
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
            heebp__gib = (max_val - min_val) * 0.001
            if right:
                bins[0] -= heebp__gib
            else:
                bins[-1] += heebp__gib
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    msu__cuyrl = dict(dropna=dropna)
    ava__kma = dict(dropna=True)
    check_unsupported_args('Series.value_counts', msu__cuyrl, ava__kma,
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
    voiq__upsrv = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    mbds__arjnf = 'def impl(\n'
    mbds__arjnf += '    S,\n'
    mbds__arjnf += '    normalize=False,\n'
    mbds__arjnf += '    sort=True,\n'
    mbds__arjnf += '    ascending=False,\n'
    mbds__arjnf += '    bins=None,\n'
    mbds__arjnf += '    dropna=True,\n'
    mbds__arjnf += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    mbds__arjnf += '):\n'
    mbds__arjnf += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    mbds__arjnf += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    mbds__arjnf += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if voiq__upsrv:
        mbds__arjnf += '    right = True\n'
        mbds__arjnf += _gen_bins_handling(bins, S.dtype)
        mbds__arjnf += '    arr = get_bin_inds(bins, arr)\n'
    mbds__arjnf += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    mbds__arjnf += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    mbds__arjnf += '    )\n'
    mbds__arjnf += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if voiq__upsrv:
        mbds__arjnf += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        mbds__arjnf += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        mbds__arjnf += '    index = get_bin_labels(bins)\n'
    else:
        mbds__arjnf += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        mbds__arjnf += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        mbds__arjnf += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        mbds__arjnf += '    )\n'
        mbds__arjnf += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    mbds__arjnf += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        mbds__arjnf += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        xzb__neu = 'len(S)' if voiq__upsrv else 'count_arr.sum()'
        mbds__arjnf += f'    res = res / float({xzb__neu})\n'
    mbds__arjnf += '    return res\n'
    ugf__sfq = {}
    exec(mbds__arjnf, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, ugf__sfq)
    impl = ugf__sfq['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    mbds__arjnf = ''
    if isinstance(bins, types.Integer):
        mbds__arjnf += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        mbds__arjnf += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            mbds__arjnf += '    min_val = min_val.value\n'
            mbds__arjnf += '    max_val = max_val.value\n'
        mbds__arjnf += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            mbds__arjnf += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        mbds__arjnf += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return mbds__arjnf


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    msu__cuyrl = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    ava__kma = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', msu__cuyrl, ava__kma, package_name
        ='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    mbds__arjnf = 'def impl(\n'
    mbds__arjnf += '    x,\n'
    mbds__arjnf += '    bins,\n'
    mbds__arjnf += '    right=True,\n'
    mbds__arjnf += '    labels=None,\n'
    mbds__arjnf += '    retbins=False,\n'
    mbds__arjnf += '    precision=3,\n'
    mbds__arjnf += '    include_lowest=False,\n'
    mbds__arjnf += "    duplicates='raise',\n"
    mbds__arjnf += '    ordered=True\n'
    mbds__arjnf += '):\n'
    if isinstance(x, SeriesType):
        mbds__arjnf += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        mbds__arjnf += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        mbds__arjnf += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        mbds__arjnf += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    mbds__arjnf += _gen_bins_handling(bins, x.dtype)
    mbds__arjnf += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    mbds__arjnf += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    mbds__arjnf += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    mbds__arjnf += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        mbds__arjnf += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        mbds__arjnf += '    return res\n'
    else:
        mbds__arjnf += '    return out_arr\n'
    ugf__sfq = {}
    exec(mbds__arjnf, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, ugf__sfq)
    impl = ugf__sfq['impl']
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
    msu__cuyrl = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    ava__kma = dict(labels=None, retbins=False, precision=3, duplicates='raise'
        )
    check_unsupported_args('pandas.qcut', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        bzet__wxnnv = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, bzet__wxnnv)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    msu__cuyrl = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    ava__kma = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', msu__cuyrl, ava__kma,
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
        gjfw__bizc = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            mkct__qjqj = bodo.utils.conversion.coerce_to_array(index)
            byn__nkxm = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                mkct__qjqj, arr), index, gjfw__bizc)
            return byn__nkxm.groupby(' ')['']
        return impl_index
    tndh__erfkk = by
    if isinstance(by, SeriesType):
        tndh__erfkk = by.data
    if isinstance(tndh__erfkk, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    xgl__ujop = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        mkct__qjqj = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        byn__nkxm = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            mkct__qjqj, arr), index, xgl__ujop)
        return byn__nkxm.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    msu__cuyrl = dict(verify_integrity=verify_integrity)
    ava__kma = dict(verify_integrity=False)
    check_unsupported_args('Series.append', msu__cuyrl, ava__kma,
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
            hmk__lqv = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            uyezw__qkqjs = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(uyezw__qkqjs, A, hmk__lqv, False)
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        uyezw__qkqjs = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    msu__cuyrl = dict(interpolation=interpolation)
    ava__kma = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            uyezw__qkqjs = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
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
        ias__voub = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(ias__voub, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    msu__cuyrl = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    ava__kma = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', msu__cuyrl, ava__kma,
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
        sxdr__piqos = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        sxdr__piqos = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    mbds__arjnf = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {sxdr__piqos}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    cvjt__wqror = dict()
    exec(mbds__arjnf, {'bodo': bodo, 'numba': numba}, cvjt__wqror)
    lzg__seshr = cvjt__wqror['impl']
    return lzg__seshr


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        sxdr__piqos = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        sxdr__piqos = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    mbds__arjnf = 'def impl(S,\n'
    mbds__arjnf += '     value=None,\n'
    mbds__arjnf += '    method=None,\n'
    mbds__arjnf += '    axis=None,\n'
    mbds__arjnf += '    inplace=False,\n'
    mbds__arjnf += '    limit=None,\n'
    mbds__arjnf += '   downcast=None,\n'
    mbds__arjnf += '):\n'
    mbds__arjnf += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    mbds__arjnf += '    n = len(in_arr)\n'
    mbds__arjnf += f'    out_arr = {sxdr__piqos}(n, -1)\n'
    mbds__arjnf += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    mbds__arjnf += '        s = in_arr[j]\n'
    mbds__arjnf += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    mbds__arjnf += '            s = value\n'
    mbds__arjnf += '        out_arr[j] = s\n'
    mbds__arjnf += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    cvjt__wqror = dict()
    exec(mbds__arjnf, {'bodo': bodo, 'numba': numba}, cvjt__wqror)
    lzg__seshr = cvjt__wqror['impl']
    return lzg__seshr


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
    hbq__wqqhh = bodo.hiframes.pd_series_ext.get_series_data(value)
    for nhuyr__safl in numba.parfors.parfor.internal_prange(len(gaozn__seqae)):
        s = gaozn__seqae[nhuyr__safl]
        if bodo.libs.array_kernels.isna(gaozn__seqae, nhuyr__safl
            ) and not bodo.libs.array_kernels.isna(hbq__wqqhh, nhuyr__safl):
            s = hbq__wqqhh[nhuyr__safl]
        gaozn__seqae[nhuyr__safl] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
    for nhuyr__safl in numba.parfors.parfor.internal_prange(len(gaozn__seqae)):
        s = gaozn__seqae[nhuyr__safl]
        if bodo.libs.array_kernels.isna(gaozn__seqae, nhuyr__safl):
            s = value
        gaozn__seqae[nhuyr__safl] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    hbq__wqqhh = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(gaozn__seqae)
    uyezw__qkqjs = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for yakb__untef in numba.parfors.parfor.internal_prange(n):
        s = gaozn__seqae[yakb__untef]
        if bodo.libs.array_kernels.isna(gaozn__seqae, yakb__untef
            ) and not bodo.libs.array_kernels.isna(hbq__wqqhh, yakb__untef):
            s = hbq__wqqhh[yakb__untef]
        uyezw__qkqjs[yakb__untef] = s
        if bodo.libs.array_kernels.isna(gaozn__seqae, yakb__untef
            ) and bodo.libs.array_kernels.isna(hbq__wqqhh, yakb__untef):
            bodo.libs.array_kernels.setna(uyezw__qkqjs, yakb__untef)
    return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    hbq__wqqhh = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(gaozn__seqae)
    uyezw__qkqjs = bodo.utils.utils.alloc_type(n, gaozn__seqae.dtype, (-1,))
    for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
        s = gaozn__seqae[nhuyr__safl]
        if bodo.libs.array_kernels.isna(gaozn__seqae, nhuyr__safl
            ) and not bodo.libs.array_kernels.isna(hbq__wqqhh, nhuyr__safl):
            s = hbq__wqqhh[nhuyr__safl]
        uyezw__qkqjs[nhuyr__safl] = s
    return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    msu__cuyrl = dict(limit=limit, downcast=downcast)
    ava__kma = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')
    ukilq__bsew = not is_overload_none(value)
    yhchc__ptmp = not is_overload_none(method)
    if ukilq__bsew and yhchc__ptmp:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not ukilq__bsew and not yhchc__ptmp:
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
    if yhchc__ptmp:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        cbu__iuu = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(cbu__iuu)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(cbu__iuu)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    ovvz__nuilf = element_type(S.data)
    bft__mocgt = None
    if ukilq__bsew:
        bft__mocgt = element_type(types.unliteral(value))
    if bft__mocgt and not can_replace(ovvz__nuilf, bft__mocgt):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {bft__mocgt} with series type {ovvz__nuilf}'
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
        rxjwq__ujd = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                hbq__wqqhh = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(gaozn__seqae)
                uyezw__qkqjs = bodo.utils.utils.alloc_type(n, rxjwq__ujd, (-1,)
                    )
                for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(gaozn__seqae, nhuyr__safl
                        ) and bodo.libs.array_kernels.isna(hbq__wqqhh,
                        nhuyr__safl):
                        bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl
                            )
                        continue
                    if bodo.libs.array_kernels.isna(gaozn__seqae, nhuyr__safl):
                        uyezw__qkqjs[nhuyr__safl
                            ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                            hbq__wqqhh[nhuyr__safl])
                        continue
                    uyezw__qkqjs[nhuyr__safl
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        gaozn__seqae[nhuyr__safl])
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                    index, name)
            return fillna_series_impl
        if yhchc__ptmp:
            kbn__ruh = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(ovvz__nuilf, (types.Integer, types.Float)
                ) and ovvz__nuilf not in kbn__ruh:
                raise BodoError(
                    f"Series.fillna(): series of type {ovvz__nuilf} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                uyezw__qkqjs = bodo.libs.array_kernels.ffill_bfill_arr(
                    gaozn__seqae, method)
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_tz_naive_timestamp(value)
            gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(gaozn__seqae)
            uyezw__qkqjs = bodo.utils.utils.alloc_type(n, rxjwq__ujd, (-1,))
            for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    gaozn__seqae[nhuyr__safl])
                if bodo.libs.array_kernels.isna(gaozn__seqae, nhuyr__safl):
                    s = value
                uyezw__qkqjs[nhuyr__safl] = s
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        oug__hey = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        msu__cuyrl = dict(limit=limit, downcast=downcast)
        ava__kma = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', msu__cuyrl,
            ava__kma, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        ovvz__nuilf = element_type(S.data)
        kbn__ruh = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(ovvz__nuilf, (types.Integer, types.Float)
            ) and ovvz__nuilf not in kbn__ruh:
            raise BodoError(
                f'Series.{overload_name}(): series of type {ovvz__nuilf} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            uyezw__qkqjs = bodo.libs.array_kernels.ffill_bfill_arr(gaozn__seqae
                , oug__hey)
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        cxrp__mtjj = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            cxrp__mtjj)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        uwwy__gom = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(uwwy__gom)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        uwwy__gom = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(uwwy__gom)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        uwwy__gom = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(uwwy__gom)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    msu__cuyrl = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    vmkqz__btsy = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', msu__cuyrl, vmkqz__btsy,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    ovvz__nuilf = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        klx__uasn = element_type(to_replace.key_type)
        bft__mocgt = element_type(to_replace.value_type)
    else:
        klx__uasn = element_type(to_replace)
        bft__mocgt = element_type(value)
    ehdcg__zhbxw = None
    if ovvz__nuilf != types.unliteral(klx__uasn):
        if bodo.utils.typing.equality_always_false(ovvz__nuilf, types.
            unliteral(klx__uasn)
            ) or not bodo.utils.typing.types_equality_exists(ovvz__nuilf,
            klx__uasn):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(ovvz__nuilf, (types.Float, types.Integer)
            ) or ovvz__nuilf == np.bool_:
            ehdcg__zhbxw = ovvz__nuilf
    if not can_replace(ovvz__nuilf, types.unliteral(bft__mocgt)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    gwzbw__jcw = to_str_arr_if_dict_array(S.data)
    if isinstance(gwzbw__jcw, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(gaozn__seqae.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(gaozn__seqae)
        uyezw__qkqjs = bodo.utils.utils.alloc_type(n, gwzbw__jcw, (-1,))
        zcn__ghe = build_replace_dict(to_replace, value, ehdcg__zhbxw)
        for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(gaozn__seqae, nhuyr__safl):
                bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl)
                continue
            s = gaozn__seqae[nhuyr__safl]
            if s in zcn__ghe:
                s = zcn__ghe[s]
            uyezw__qkqjs[nhuyr__safl] = s
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    snlar__qkoo = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    fkfg__dlz = is_iterable_type(to_replace)
    ofw__ktwvd = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    jfuy__dzvsg = is_iterable_type(value)
    if snlar__qkoo and ofw__ktwvd:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                zcn__ghe = {}
                zcn__ghe[key_dtype_conv(to_replace)] = value
                return zcn__ghe
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            zcn__ghe = {}
            zcn__ghe[to_replace] = value
            return zcn__ghe
        return impl
    if fkfg__dlz and ofw__ktwvd:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                zcn__ghe = {}
                for exk__zvp in to_replace:
                    zcn__ghe[key_dtype_conv(exk__zvp)] = value
                return zcn__ghe
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            zcn__ghe = {}
            for exk__zvp in to_replace:
                zcn__ghe[exk__zvp] = value
            return zcn__ghe
        return impl
    if fkfg__dlz and jfuy__dzvsg:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                zcn__ghe = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for nhuyr__safl in range(len(to_replace)):
                    zcn__ghe[key_dtype_conv(to_replace[nhuyr__safl])] = value[
                        nhuyr__safl]
                return zcn__ghe
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            zcn__ghe = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for nhuyr__safl in range(len(to_replace)):
                zcn__ghe[to_replace[nhuyr__safl]] = value[nhuyr__safl]
            return zcn__ghe
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
            uyezw__qkqjs = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo
                .hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        uyezw__qkqjs = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    msu__cuyrl = dict(ignore_index=ignore_index)
    ohh__dml = dict(ignore_index=False)
    check_unsupported_args('Series.explode', msu__cuyrl, ohh__dml,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        gyfbm__ael = bodo.utils.conversion.index_to_array(index)
        uyezw__qkqjs, ymqfb__fjxrs = bodo.libs.array_kernels.explode(arr,
            gyfbm__ael)
        mfj__fuiyd = bodo.utils.conversion.index_from_array(ymqfb__fjxrs)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
            mfj__fuiyd, name)
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
            tue__ykv = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                tue__ykv[nhuyr__safl] = np.argmax(a[nhuyr__safl])
            return tue__ykv
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            zaaqf__kdbx = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                zaaqf__kdbx[nhuyr__safl] = np.argmin(a[nhuyr__safl])
            return zaaqf__kdbx
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType) and isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            cnjr__lxmne = bodo.utils.conversion.ndarray_if_nullable_arr(bodo
                .hiframes.pd_series_ext.get_series_data(b))
            return np.dot(arr, cnjr__lxmne)
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
    msu__cuyrl = dict(axis=axis, inplace=inplace, how=how)
    imrep__hqgsx = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', msu__cuyrl, imrep__hqgsx,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            nrscd__jhb = S.notna().values
            gyfbm__ael = bodo.utils.conversion.extract_index_array(S)
            mfj__fuiyd = bodo.utils.conversion.convert_to_index(gyfbm__ael[
                nrscd__jhb])
            uyezw__qkqjs = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(gaozn__seqae))
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                mfj__fuiyd, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            gyfbm__ael = bodo.utils.conversion.extract_index_array(S)
            nrscd__jhb = S.notna().values
            mfj__fuiyd = bodo.utils.conversion.convert_to_index(gyfbm__ael[
                nrscd__jhb])
            uyezw__qkqjs = gaozn__seqae[nrscd__jhb]
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                mfj__fuiyd, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    msu__cuyrl = dict(freq=freq, axis=axis)
    ava__kma = dict(freq=None, axis=0)
    check_unsupported_args('Series.shift', msu__cuyrl, ava__kma,
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
        uyezw__qkqjs = bodo.hiframes.rolling.shift(arr, periods, False,
            fill_value)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    msu__cuyrl = dict(fill_method=fill_method, limit=limit, freq=freq)
    ava__kma = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', msu__cuyrl, ava__kma,
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
        uyezw__qkqjs = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
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
            dfh__fiyxg = 'None'
        else:
            dfh__fiyxg = 'other'
        mbds__arjnf = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            mbds__arjnf += '  cond = ~cond\n'
        mbds__arjnf += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        mbds__arjnf += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        mbds__arjnf += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        mbds__arjnf += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {dfh__fiyxg})
"""
        mbds__arjnf += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        ugf__sfq = {}
        exec(mbds__arjnf, {'bodo': bodo, 'np': np}, ugf__sfq)
        impl = ugf__sfq['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        cxrp__mtjj = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(cxrp__mtjj)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    msu__cuyrl = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    ava__kma = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', msu__cuyrl, ava__kma,
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
    ftpmf__qdt = is_overload_constant_nan(other)
    if not (is_default or ftpmf__qdt or is_scalar_type(other) or isinstance
        (other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
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
            kqodb__joxjy = arr.dtype.elem_type
        else:
            kqodb__joxjy = arr.dtype
        if is_iterable_type(other):
            rkedm__xwglr = other.dtype
        elif ftpmf__qdt:
            rkedm__xwglr = types.float64
        else:
            rkedm__xwglr = types.unliteral(other)
        if not ftpmf__qdt and not is_common_scalar_dtype([kqodb__joxjy,
            rkedm__xwglr]):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        msu__cuyrl = dict(level=level, axis=axis)
        ava__kma = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), msu__cuyrl,
            ava__kma, package_name='pandas', module_name='Series')
        zbaf__ocmd = other == string_type or is_overload_constant_str(other)
        fuxrw__wav = is_iterable_type(other) and other.dtype == string_type
        nwo__ukeb = S.dtype == string_type and (op == operator.add and (
            zbaf__ocmd or fuxrw__wav) or op == operator.mul and isinstance(
            other, types.Integer))
        cvtbq__cbith = S.dtype == bodo.timedelta64ns
        qxyen__rpdz = S.dtype == bodo.datetime64ns
        zyr__dnkh = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        xpvwg__kspbz = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype ==
            pd_timestamp_tz_naive_type or other.dtype == bodo.datetime64ns)
        qimc__bjw = cvtbq__cbith and (zyr__dnkh or xpvwg__kspbz
            ) or qxyen__rpdz and zyr__dnkh
        qimc__bjw = qimc__bjw and op == operator.add
        if not (isinstance(S.dtype, types.Number) or nwo__ukeb or qimc__bjw):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        arx__hnapl = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            gwzbw__jcw = arx__hnapl.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and gwzbw__jcw == types.Array(types.bool_, 1, 'C'):
                gwzbw__jcw = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_tz_naive_timestamp(other
                    )
                n = len(arr)
                uyezw__qkqjs = bodo.utils.utils.alloc_type(n, gwzbw__jcw, (-1,)
                    )
                for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                    xfzwj__mshnm = bodo.libs.array_kernels.isna(arr,
                        nhuyr__safl)
                    if xfzwj__mshnm:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(uyezw__qkqjs,
                                nhuyr__safl)
                        else:
                            uyezw__qkqjs[nhuyr__safl] = op(fill_value, other)
                    else:
                        uyezw__qkqjs[nhuyr__safl] = op(arr[nhuyr__safl], other)
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        gwzbw__jcw = arx__hnapl.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and gwzbw__jcw == types.Array(types.bool_, 1, 'C'):
            gwzbw__jcw = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rro__csa = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            uyezw__qkqjs = bodo.utils.utils.alloc_type(n, gwzbw__jcw, (-1,))
            for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                xfzwj__mshnm = bodo.libs.array_kernels.isna(arr, nhuyr__safl)
                hftd__hham = bodo.libs.array_kernels.isna(rro__csa, nhuyr__safl
                    )
                if xfzwj__mshnm and hftd__hham:
                    bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl)
                elif xfzwj__mshnm:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl
                            )
                    else:
                        uyezw__qkqjs[nhuyr__safl] = op(fill_value, rro__csa
                            [nhuyr__safl])
                elif hftd__hham:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl
                            )
                    else:
                        uyezw__qkqjs[nhuyr__safl] = op(arr[nhuyr__safl],
                            fill_value)
                else:
                    uyezw__qkqjs[nhuyr__safl] = op(arr[nhuyr__safl],
                        rro__csa[nhuyr__safl])
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
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
        arx__hnapl = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            gwzbw__jcw = arx__hnapl.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and gwzbw__jcw == types.Array(types.bool_, 1, 'C'):
                gwzbw__jcw = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                uyezw__qkqjs = bodo.utils.utils.alloc_type(n, gwzbw__jcw, None)
                for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                    xfzwj__mshnm = bodo.libs.array_kernels.isna(arr,
                        nhuyr__safl)
                    if xfzwj__mshnm:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(uyezw__qkqjs,
                                nhuyr__safl)
                        else:
                            uyezw__qkqjs[nhuyr__safl] = op(other, fill_value)
                    else:
                        uyezw__qkqjs[nhuyr__safl] = op(other, arr[nhuyr__safl])
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        gwzbw__jcw = arx__hnapl.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and gwzbw__jcw == types.Array(types.bool_, 1, 'C'):
            gwzbw__jcw = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rro__csa = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            uyezw__qkqjs = bodo.utils.utils.alloc_type(n, gwzbw__jcw, None)
            for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                xfzwj__mshnm = bodo.libs.array_kernels.isna(arr, nhuyr__safl)
                hftd__hham = bodo.libs.array_kernels.isna(rro__csa, nhuyr__safl
                    )
                uyezw__qkqjs[nhuyr__safl] = op(rro__csa[nhuyr__safl], arr[
                    nhuyr__safl])
                if xfzwj__mshnm and hftd__hham:
                    bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl)
                elif xfzwj__mshnm:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl
                            )
                    else:
                        uyezw__qkqjs[nhuyr__safl] = op(rro__csa[nhuyr__safl
                            ], fill_value)
                elif hftd__hham:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl
                            )
                    else:
                        uyezw__qkqjs[nhuyr__safl] = op(fill_value, arr[
                            nhuyr__safl])
                else:
                    uyezw__qkqjs[nhuyr__safl] = op(rro__csa[nhuyr__safl],
                        arr[nhuyr__safl])
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
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
    for op, xsygu__vsrd in explicit_binop_funcs_two_ways.items():
        for name in xsygu__vsrd:
            cxrp__mtjj = create_explicit_binary_op_overload(op)
            mhrq__dprfz = create_explicit_binary_reverse_op_overload(op)
            uclz__rdfuh = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(cxrp__mtjj)
            overload_method(SeriesType, uclz__rdfuh, no_unliteral=True)(
                mhrq__dprfz)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        cxrp__mtjj = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(cxrp__mtjj)
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
                lmenx__dfj = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                uyezw__qkqjs = dt64_arr_sub(arr, lmenx__dfj)
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
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
                uyezw__qkqjs = np.empty(n, np.dtype('datetime64[ns]'))
                for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, nhuyr__safl):
                        bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl
                            )
                        continue
                    blrsj__mchy = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[nhuyr__safl]))
                    kslfk__necd = op(blrsj__mchy, rhs)
                    uyezw__qkqjs[nhuyr__safl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        kslfk__necd.value)
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
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
                    lmenx__dfj = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    uyezw__qkqjs = op(arr, bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(lmenx__dfj))
                    return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs
                        , index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lmenx__dfj = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                uyezw__qkqjs = op(arr, lmenx__dfj)
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    hxan__rinr = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    uyezw__qkqjs = op(bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(hxan__rinr), arr)
                    return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs
                        , index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                hxan__rinr = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                uyezw__qkqjs = op(hxan__rinr, arr)
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        cxrp__mtjj = create_binary_op_overload(op)
        overload(op)(cxrp__mtjj)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    qnydb__pzywa = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, qnydb__pzywa)
        for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, nhuyr__safl
                ) or bodo.libs.array_kernels.isna(arg2, nhuyr__safl):
                bodo.libs.array_kernels.setna(S, nhuyr__safl)
                continue
            S[nhuyr__safl
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                nhuyr__safl]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[nhuyr__safl]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                rro__csa = bodo.utils.conversion.get_array_if_series_or_index(
                    other)
                op(arr, rro__csa)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        cxrp__mtjj = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(cxrp__mtjj)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                uyezw__qkqjs = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        cxrp__mtjj = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(cxrp__mtjj)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    uyezw__qkqjs = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs
                        , index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    rro__csa = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    uyezw__qkqjs = ufunc(arr, rro__csa)
                    return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs
                        , index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    rro__csa = bodo.hiframes.pd_series_ext.get_series_data(S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    uyezw__qkqjs = ufunc(arr, rro__csa)
                    return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs
                        , index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        cxrp__mtjj = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(cxrp__mtjj)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        ggyy__lnvej = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        tewgo__qsx = np.arange(n),
        bodo.libs.timsort.sort(ggyy__lnvej, 0, n, tewgo__qsx)
        return tewgo__qsx[0]
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
        uqja__omuaj = get_overload_const_str(downcast)
        if uqja__omuaj in ('integer', 'signed'):
            out_dtype = types.int64
        elif uqja__omuaj == 'unsigned':
            out_dtype = types.uint64
        else:
            assert uqja__omuaj == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            gaozn__seqae = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            uyezw__qkqjs = pd.to_numeric(gaozn__seqae, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if arg_a == bodo.dict_str_arr_type:
        return (lambda arg_a, errors='raise', downcast=None: bodo.libs.
            dict_arr_ext.dict_arr_to_numeric(arg_a, errors, downcast))
    qwb__mhlju = types.Array(types.float64, 1, 'C'
        ) if out_dtype == types.float64 else IntegerArrayType(types.int64)

    def to_numeric_impl(arg_a, errors='raise', downcast=None):
        numba.parfors.parfor.init_prange()
        n = len(arg_a)
        ozbq__vwuxa = bodo.utils.utils.alloc_type(n, qwb__mhlju, (-1,))
        for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg_a, nhuyr__safl):
                bodo.libs.array_kernels.setna(ozbq__vwuxa, nhuyr__safl)
            else:
                bodo.libs.str_arr_ext.str_arr_item_to_numeric(ozbq__vwuxa,
                    nhuyr__safl, arg_a, nhuyr__safl)
        return ozbq__vwuxa
    return to_numeric_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        gwk__jgxvw = if_series_to_array_type(args[0])
        if isinstance(gwk__jgxvw, types.Array) and isinstance(gwk__jgxvw.
            dtype, types.Integer):
            gwk__jgxvw = types.Array(types.float64, 1, 'C')
        return gwk__jgxvw(*args)


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
    lhr__cvp = bodo.utils.utils.is_array_typ(x, True)
    bsy__ijmh = bodo.utils.utils.is_array_typ(y, True)
    mbds__arjnf = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        mbds__arjnf += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if lhr__cvp and not bodo.utils.utils.is_array_typ(x, False):
        mbds__arjnf += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if bsy__ijmh and not bodo.utils.utils.is_array_typ(y, False):
        mbds__arjnf += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    mbds__arjnf += '  n = len(condition)\n'
    kcjse__olcwv = x.dtype if lhr__cvp else types.unliteral(x)
    aqau__vkdhy = y.dtype if bsy__ijmh else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        kcjse__olcwv = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        aqau__vkdhy = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    tdgxw__xjeuu = get_data(x)
    qjw__hrgj = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(tewgo__qsx) for
        tewgo__qsx in [tdgxw__xjeuu, qjw__hrgj])
    if qjw__hrgj == types.none:
        if isinstance(kcjse__olcwv, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif tdgxw__xjeuu == qjw__hrgj and not is_nullable:
        out_dtype = dtype_to_array_type(kcjse__olcwv)
    elif kcjse__olcwv == string_type or aqau__vkdhy == string_type:
        out_dtype = bodo.string_array_type
    elif tdgxw__xjeuu == bytes_type or (lhr__cvp and kcjse__olcwv == bytes_type
        ) and (qjw__hrgj == bytes_type or bsy__ijmh and aqau__vkdhy ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(kcjse__olcwv, bodo.PDCategoricalDtype):
        out_dtype = None
    elif kcjse__olcwv in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(kcjse__olcwv, 1, 'C')
    elif aqau__vkdhy in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(aqau__vkdhy, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(kcjse__olcwv), numba.np.numpy_support.
            as_dtype(aqau__vkdhy)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(kcjse__olcwv, bodo.PDCategoricalDtype):
        ywqqu__ddmz = 'x'
    else:
        ywqqu__ddmz = 'out_dtype'
    mbds__arjnf += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {ywqqu__ddmz}, (-1,))\n')
    if isinstance(kcjse__olcwv, bodo.PDCategoricalDtype):
        mbds__arjnf += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        mbds__arjnf += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    mbds__arjnf += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    mbds__arjnf += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if lhr__cvp:
        mbds__arjnf += '      if bodo.libs.array_kernels.isna(x, j):\n'
        mbds__arjnf += '        setna(out_arr, j)\n'
        mbds__arjnf += '        continue\n'
    if isinstance(kcjse__olcwv, bodo.PDCategoricalDtype):
        mbds__arjnf += '      out_codes[j] = x_codes[j]\n'
    else:
        mbds__arjnf += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('x[j]' if lhr__cvp else 'x'))
    mbds__arjnf += '    else:\n'
    if bsy__ijmh:
        mbds__arjnf += '      if bodo.libs.array_kernels.isna(y, j):\n'
        mbds__arjnf += '        setna(out_arr, j)\n'
        mbds__arjnf += '        continue\n'
    if qjw__hrgj == types.none:
        if isinstance(kcjse__olcwv, bodo.PDCategoricalDtype):
            mbds__arjnf += '      out_codes[j] = -1\n'
        else:
            mbds__arjnf += '      setna(out_arr, j)\n'
    else:
        mbds__arjnf += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('y[j]' if bsy__ijmh else 'y'))
    mbds__arjnf += '  return out_arr\n'
    ugf__sfq = {}
    exec(mbds__arjnf, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, ugf__sfq)
    yretj__sxsrv = ugf__sfq['_impl']
    return yretj__sxsrv


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
        qxx__ikz = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(qxx__ikz, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(qxx__ikz):
            whzxc__fhmyf = qxx__ikz.data.dtype
        else:
            whzxc__fhmyf = qxx__ikz.dtype
        if isinstance(whzxc__fhmyf, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        vvfbf__drhw = qxx__ikz
    else:
        fjrw__gvq = []
        for qxx__ikz in choicelist:
            if not bodo.utils.utils.is_array_typ(qxx__ikz, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(qxx__ikz):
                whzxc__fhmyf = qxx__ikz.data.dtype
            else:
                whzxc__fhmyf = qxx__ikz.dtype
            if isinstance(whzxc__fhmyf, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            fjrw__gvq.append(whzxc__fhmyf)
        if not is_common_scalar_dtype(fjrw__gvq):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        vvfbf__drhw = choicelist[0]
    if is_series_type(vvfbf__drhw):
        vvfbf__drhw = vvfbf__drhw.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, vvfbf__drhw.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(vvfbf__drhw, types.Array) or isinstance(vvfbf__drhw,
        BooleanArrayType) or isinstance(vvfbf__drhw, IntegerArrayType) or
        isinstance(vvfbf__drhw, FloatingArrayType) or bodo.utils.utils.
        is_array_typ(vvfbf__drhw, False) and vvfbf__drhw.dtype in [bodo.
        string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {vvfbf__drhw} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    skg__ikgnd = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        hjc__mvdup = choicelist.dtype
    else:
        ekp__zxzxk = False
        fjrw__gvq = []
        for qxx__ikz in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(qxx__ikz,
                'numpy.select()')
            if is_nullable_type(qxx__ikz):
                ekp__zxzxk = True
            if is_series_type(qxx__ikz):
                whzxc__fhmyf = qxx__ikz.data.dtype
            else:
                whzxc__fhmyf = qxx__ikz.dtype
            if isinstance(whzxc__fhmyf, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            fjrw__gvq.append(whzxc__fhmyf)
        uuwvf__omaow, brjqx__ibb = get_common_scalar_dtype(fjrw__gvq)
        if not brjqx__ibb:
            raise BodoError('Internal error in overload_np_select')
        lwzg__ysx = dtype_to_array_type(uuwvf__omaow)
        if ekp__zxzxk:
            lwzg__ysx = to_nullable_type(lwzg__ysx)
        hjc__mvdup = lwzg__ysx
    if isinstance(hjc__mvdup, SeriesType):
        hjc__mvdup = hjc__mvdup.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        wtbts__fdwvt = True
    else:
        wtbts__fdwvt = False
    rovss__emxh = False
    mtlx__wubnj = False
    if wtbts__fdwvt:
        if isinstance(hjc__mvdup.dtype, types.Number):
            pass
        elif hjc__mvdup.dtype == types.bool_:
            mtlx__wubnj = True
        else:
            rovss__emxh = True
            hjc__mvdup = to_nullable_type(hjc__mvdup)
    elif default == types.none or is_overload_constant_nan(default):
        rovss__emxh = True
        hjc__mvdup = to_nullable_type(hjc__mvdup)
    mbds__arjnf = 'def np_select_impl(condlist, choicelist, default=0):\n'
    mbds__arjnf += '  if len(condlist) != len(choicelist):\n'
    mbds__arjnf += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    mbds__arjnf += '  output_len = len(choicelist[0])\n'
    mbds__arjnf += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    mbds__arjnf += '  for i in range(output_len):\n'
    if rovss__emxh:
        mbds__arjnf += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif mtlx__wubnj:
        mbds__arjnf += '    out[i] = False\n'
    else:
        mbds__arjnf += '    out[i] = default\n'
    if skg__ikgnd:
        mbds__arjnf += '  for i in range(len(condlist) - 1, -1, -1):\n'
        mbds__arjnf += '    cond = condlist[i]\n'
        mbds__arjnf += '    choice = choicelist[i]\n'
        mbds__arjnf += '    out = np.where(cond, choice, out)\n'
    else:
        for nhuyr__safl in range(len(choicelist) - 1, -1, -1):
            mbds__arjnf += f'  cond = condlist[{nhuyr__safl}]\n'
            mbds__arjnf += f'  choice = choicelist[{nhuyr__safl}]\n'
            mbds__arjnf += f'  out = np.where(cond, choice, out)\n'
    mbds__arjnf += '  return out'
    ugf__sfq = dict()
    exec(mbds__arjnf, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': hjc__mvdup}, ugf__sfq)
    impl = ugf__sfq['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        uyezw__qkqjs = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    msu__cuyrl = dict(subset=subset, keep=keep, inplace=inplace)
    ava__kma = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', msu__cuyrl, ava__kma,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        wge__izoj = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (wge__izoj,), gyfbm__ael = bodo.libs.array_kernels.drop_duplicates((
            wge__izoj,), index, 1)
        index = bodo.utils.conversion.index_from_array(gyfbm__ael)
        return bodo.hiframes.pd_series_ext.init_series(wge__izoj, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    lhsn__neswm = element_type(S.data)
    if not is_common_scalar_dtype([lhsn__neswm, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([lhsn__neswm, right]):
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
        uyezw__qkqjs = bodo.libs.bool_arr_ext.alloc_bool_array(n)
        for nhuyr__safl in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arr, nhuyr__safl):
                bodo.libs.array_kernels.setna(uyezw__qkqjs, nhuyr__safl)
                continue
            ikzkj__zxb = bodo.utils.conversion.box_if_dt64(arr[nhuyr__safl])
            if inclusive == 'both':
                uyezw__qkqjs[nhuyr__safl
                    ] = ikzkj__zxb <= right and ikzkj__zxb >= left
            else:
                uyezw__qkqjs[nhuyr__safl
                    ] = ikzkj__zxb < right and ikzkj__zxb > left
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs, index,
            name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    msu__cuyrl = dict(axis=axis)
    ava__kma = dict(axis=None)
    check_unsupported_args('Series.repeat', msu__cuyrl, ava__kma,
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
            gyfbm__ael = bodo.utils.conversion.index_to_array(index)
            uyezw__qkqjs = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            ymqfb__fjxrs = bodo.libs.array_kernels.repeat_kernel(gyfbm__ael,
                repeats)
            mfj__fuiyd = bodo.utils.conversion.index_from_array(ymqfb__fjxrs)
            return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
                mfj__fuiyd, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        gyfbm__ael = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        uyezw__qkqjs = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        ymqfb__fjxrs = bodo.libs.array_kernels.repeat_kernel(gyfbm__ael,
            repeats)
        mfj__fuiyd = bodo.utils.conversion.index_from_array(ymqfb__fjxrs)
        return bodo.hiframes.pd_series_ext.init_series(uyezw__qkqjs,
            mfj__fuiyd, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        tewgo__qsx = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(tewgo__qsx)
        wuky__sxaon = {}
        for nhuyr__safl in range(n):
            ikzkj__zxb = bodo.utils.conversion.box_if_dt64(tewgo__qsx[
                nhuyr__safl])
            wuky__sxaon[index[nhuyr__safl]] = ikzkj__zxb
        return wuky__sxaon
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    cbu__iuu = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            ywazp__mfw = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(cbu__iuu)
    elif is_literal_type(name):
        ywazp__mfw = get_literal_value(name)
    else:
        raise_bodo_error(cbu__iuu)
    ywazp__mfw = 0 if ywazp__mfw is None else ywazp__mfw
    mjvl__huvas = ColNamesMetaType((ywazp__mfw,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            mjvl__huvas)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
