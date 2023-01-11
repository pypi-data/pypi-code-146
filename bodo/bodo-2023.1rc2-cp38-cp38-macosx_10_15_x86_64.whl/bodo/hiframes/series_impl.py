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
            eew__wis = bodo.hiframes.pd_series_ext.get_series_data(s)
            byl__vjdvb = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(eew__wis
                )
            return byl__vjdvb
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
            exrfn__bjh = list()
            for ycf__qbufn in range(len(S)):
                exrfn__bjh.append(S.iat[ycf__qbufn])
            return exrfn__bjh
        return impl_float

    def impl(S):
        exrfn__bjh = list()
        for ycf__qbufn in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, ycf__qbufn):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            exrfn__bjh.append(S.iat[ycf__qbufn])
        return exrfn__bjh
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    bujfm__oadr = dict(dtype=dtype, copy=copy, na_value=na_value)
    lma__qqre = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    bujfm__oadr = dict(name=name, inplace=inplace)
    lma__qqre = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', bujfm__oadr, lma__qqre,
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
        cmuk__wnw = ', '.join(['index_arrs[{}]'.format(ycf__qbufn) for
            ycf__qbufn in range(S.index.nlevels)])
    else:
        cmuk__wnw = '    bodo.utils.conversion.index_to_array(index)\n'
    dbpt__bek = 'index' if 'index' != series_name else 'level_0'
    fgevk__xwsu = get_index_names(S.index, 'Series.reset_index()', dbpt__bek)
    columns = [name for name in fgevk__xwsu]
    columns.append(series_name)
    chngq__nojh = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    chngq__nojh += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    chngq__nojh += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        chngq__nojh += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    chngq__nojh += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    chngq__nojh += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({cmuk__wnw}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    mse__vch = {}
    exec(chngq__nojh, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, mse__vch)
    ituba__kcd = mse__vch['_impl']
    return ituba__kcd


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvzr__wgc = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
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
        cvzr__wgc = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[ycf__qbufn]):
                bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
            else:
                cvzr__wgc[ycf__qbufn] = np.round(arr[ycf__qbufn], decimals)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    bujfm__oadr = dict(level=level, numeric_only=numeric_only)
    lma__qqre = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(level=level, numeric_only=numeric_only)
    lma__qqre = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    lma__qqre = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', bujfm__oadr, lma__qqre,
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
        nbwz__dhq = bodo.hiframes.pd_series_ext.get_series_data(S)
        nhcc__zvsd = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        drw__wni = 0
        for ycf__qbufn in numba.parfors.parfor.internal_prange(len(nbwz__dhq)):
            fsdpq__lqikf = 0
            jyss__cbu = bodo.libs.array_kernels.isna(nbwz__dhq, ycf__qbufn)
            niz__ydnr = bodo.libs.array_kernels.isna(nhcc__zvsd, ycf__qbufn)
            if jyss__cbu and not niz__ydnr or not jyss__cbu and niz__ydnr:
                fsdpq__lqikf = 1
            elif not jyss__cbu:
                if nbwz__dhq[ycf__qbufn] != nhcc__zvsd[ycf__qbufn]:
                    fsdpq__lqikf = 1
            drw__wni += fsdpq__lqikf
        return drw__wni == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    bujfm__oadr = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    lma__qqre = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    bujfm__oadr = dict(level=level)
    lma__qqre = dict(level=None)
    check_unsupported_args('Series.mad', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    ifb__evcwv = types.float64
    bhih__alpd = types.float64
    if S.dtype == types.float32:
        ifb__evcwv = types.float32
        bhih__alpd = types.float32
    odh__ftgo = ifb__evcwv(0)
    heg__beqvb = bhih__alpd(0)
    vehzo__eqkpa = bhih__alpd(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        snypw__udjcf = odh__ftgo
        drw__wni = heg__beqvb
        for ycf__qbufn in numba.parfors.parfor.internal_prange(len(A)):
            fsdpq__lqikf = odh__ftgo
            siq__nufw = heg__beqvb
            if not bodo.libs.array_kernels.isna(A, ycf__qbufn) or not skipna:
                fsdpq__lqikf = A[ycf__qbufn]
                siq__nufw = vehzo__eqkpa
            snypw__udjcf += fsdpq__lqikf
            drw__wni += siq__nufw
        vpf__ddde = bodo.hiframes.series_kernels._mean_handle_nan(snypw__udjcf,
            drw__wni)
        cofsf__pyca = odh__ftgo
        for ycf__qbufn in numba.parfors.parfor.internal_prange(len(A)):
            fsdpq__lqikf = odh__ftgo
            if not bodo.libs.array_kernels.isna(A, ycf__qbufn) or not skipna:
                fsdpq__lqikf = abs(A[ycf__qbufn] - vpf__ddde)
            cofsf__pyca += fsdpq__lqikf
        uawnr__jvhb = bodo.hiframes.series_kernels._mean_handle_nan(cofsf__pyca
            , drw__wni)
        return uawnr__jvhb
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    bujfm__oadr = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    lma__qqre = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(level=level, numeric_only=numeric_only)
    lma__qqre = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', bujfm__oadr, lma__qqre,
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
        jmcn__mii = 0
        thwsz__njml = 0
        drw__wni = 0
        for ycf__qbufn in numba.parfors.parfor.internal_prange(len(A)):
            fsdpq__lqikf = 0
            siq__nufw = 0
            if not bodo.libs.array_kernels.isna(A, ycf__qbufn) or not skipna:
                fsdpq__lqikf = A[ycf__qbufn]
                siq__nufw = 1
            jmcn__mii += fsdpq__lqikf
            thwsz__njml += fsdpq__lqikf * fsdpq__lqikf
            drw__wni += siq__nufw
        bob__prpi = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            jmcn__mii, thwsz__njml, drw__wni, ddof)
        zgnpx__mbtd = bodo.hiframes.series_kernels._sem_handle_nan(bob__prpi,
            drw__wni)
        return zgnpx__mbtd
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    bujfm__oadr = dict(level=level, numeric_only=numeric_only)
    lma__qqre = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', bujfm__oadr, lma__qqre,
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
        jmcn__mii = 0.0
        thwsz__njml = 0.0
        ljzx__qaa = 0.0
        qmq__nwms = 0.0
        drw__wni = 0
        for ycf__qbufn in numba.parfors.parfor.internal_prange(len(A)):
            fsdpq__lqikf = 0.0
            siq__nufw = 0
            if not bodo.libs.array_kernels.isna(A, ycf__qbufn) or not skipna:
                fsdpq__lqikf = np.float64(A[ycf__qbufn])
                siq__nufw = 1
            jmcn__mii += fsdpq__lqikf
            thwsz__njml += fsdpq__lqikf ** 2
            ljzx__qaa += fsdpq__lqikf ** 3
            qmq__nwms += fsdpq__lqikf ** 4
            drw__wni += siq__nufw
        bob__prpi = bodo.hiframes.series_kernels.compute_kurt(jmcn__mii,
            thwsz__njml, ljzx__qaa, qmq__nwms, drw__wni)
        return bob__prpi
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    bujfm__oadr = dict(level=level, numeric_only=numeric_only)
    lma__qqre = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', bujfm__oadr, lma__qqre,
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
        jmcn__mii = 0.0
        thwsz__njml = 0.0
        ljzx__qaa = 0.0
        drw__wni = 0
        for ycf__qbufn in numba.parfors.parfor.internal_prange(len(A)):
            fsdpq__lqikf = 0.0
            siq__nufw = 0
            if not bodo.libs.array_kernels.isna(A, ycf__qbufn) or not skipna:
                fsdpq__lqikf = np.float64(A[ycf__qbufn])
                siq__nufw = 1
            jmcn__mii += fsdpq__lqikf
            thwsz__njml += fsdpq__lqikf ** 2
            ljzx__qaa += fsdpq__lqikf ** 3
            drw__wni += siq__nufw
        bob__prpi = bodo.hiframes.series_kernels.compute_skew(jmcn__mii,
            thwsz__njml, ljzx__qaa, drw__wni)
        return bob__prpi
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    bujfm__oadr = dict(level=level, numeric_only=numeric_only)
    lma__qqre = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(level=level, numeric_only=numeric_only)
    lma__qqre = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', bujfm__oadr, lma__qqre,
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
        nbwz__dhq = bodo.hiframes.pd_series_ext.get_series_data(S)
        nhcc__zvsd = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        nqcl__iybc = 0
        for ycf__qbufn in numba.parfors.parfor.internal_prange(len(nbwz__dhq)):
            bvyre__adzj = nbwz__dhq[ycf__qbufn]
            aeu__syz = nhcc__zvsd[ycf__qbufn]
            nqcl__iybc += bvyre__adzj * aeu__syz
        return nqcl__iybc
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    bujfm__oadr = dict(skipna=skipna)
    lma__qqre = dict(skipna=True)
    check_unsupported_args('Series.cumsum', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(skipna=skipna)
    lma__qqre = dict(skipna=True)
    check_unsupported_args('Series.cumprod', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(skipna=skipna)
    lma__qqre = dict(skipna=True)
    check_unsupported_args('Series.cummin', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(skipna=skipna)
    lma__qqre = dict(skipna=True)
    check_unsupported_args('Series.cummax', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    lma__qqre = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        ydw__rhev = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, ydw__rhev, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    bujfm__oadr = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    lma__qqre = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', bujfm__oadr, lma__qqre,
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
    npq__rdrxr = S.data

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(A)
        cvzr__wgc = bodo.utils.utils.alloc_type(n, npq__rdrxr, (-1,))
        for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, ycf__qbufn):
                bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                continue
            cvzr__wgc[ycf__qbufn] = np.abs(A[ycf__qbufn])
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    bujfm__oadr = dict(level=level)
    lma__qqre = dict(level=None)
    check_unsupported_args('Series.count', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    bujfm__oadr = dict(method=method, min_periods=min_periods)
    lma__qqre = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        hhf__xboxd = S.sum()
        qgs__avlrf = other.sum()
        a = n * (S * other).sum() - hhf__xboxd * qgs__avlrf
        xwg__qsajq = n * (S ** 2).sum() - hhf__xboxd ** 2
        vnwhi__qnsp = n * (other ** 2).sum() - qgs__avlrf ** 2
        return a / np.sqrt(xwg__qsajq * vnwhi__qnsp)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    bujfm__oadr = dict(min_periods=min_periods)
    lma__qqre = dict(min_periods=None)
    check_unsupported_args('Series.cov', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        hhf__xboxd = S.mean()
        qgs__avlrf = other.mean()
        dtww__sfl = ((S - hhf__xboxd) * (other - qgs__avlrf)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(dtww__sfl, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            giyy__ikq = np.sign(sum_val)
            return np.inf * giyy__ikq
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    bujfm__oadr = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    lma__qqre = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        kvzm__jael = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            min_val = bodo.libs.array_ops.array_op_min(arr)
            return convert_val_to_timestamp(min_val.value, tz=kvzm__jael)
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
    bujfm__oadr = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    lma__qqre = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        kvzm__jael = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            max_val = bodo.libs.array_ops.array_op_max(arr)
            return convert_val_to_timestamp(max_val.value, tz=kvzm__jael)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    bujfm__oadr = dict(axis=axis, skipna=skipna)
    lma__qqre = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(axis=axis, skipna=skipna)
    lma__qqre = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', bujfm__oadr, lma__qqre,
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
    bujfm__oadr = dict(level=level, numeric_only=numeric_only)
    lma__qqre = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', bujfm__oadr, lma__qqre,
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
        gxbwv__adtb = arr[:n]
        csxoh__tppis = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(gxbwv__adtb,
            csxoh__tppis, name)
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
        nzcw__thlcu = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        gxbwv__adtb = arr[nzcw__thlcu:]
        csxoh__tppis = index[nzcw__thlcu:]
        return bodo.hiframes.pd_series_ext.init_series(gxbwv__adtb,
            csxoh__tppis, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    wpef__dwf = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in wpef__dwf:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            spr__lwz = index[0]
            prvtv__oljj = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, spr__lwz,
                False))
        else:
            prvtv__oljj = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        gxbwv__adtb = arr[:prvtv__oljj]
        csxoh__tppis = index[:prvtv__oljj]
        return bodo.hiframes.pd_series_ext.init_series(gxbwv__adtb,
            csxoh__tppis, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    wpef__dwf = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in wpef__dwf:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            poxt__bpeie = index[-1]
            prvtv__oljj = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                poxt__bpeie, True))
        else:
            prvtv__oljj = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        gxbwv__adtb = arr[len(arr) - prvtv__oljj:]
        csxoh__tppis = index[len(arr) - prvtv__oljj:]
        return bodo.hiframes.pd_series_ext.init_series(gxbwv__adtb,
            csxoh__tppis, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fim__artcd = bodo.utils.conversion.index_to_array(index)
        yaeeh__xwnh, jrar__xzw = (bodo.libs.array_kernels.
            first_last_valid_index(arr, fim__artcd))
        return jrar__xzw if yaeeh__xwnh else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fim__artcd = bodo.utils.conversion.index_to_array(index)
        yaeeh__xwnh, jrar__xzw = (bodo.libs.array_kernels.
            first_last_valid_index(arr, fim__artcd, False))
        return jrar__xzw if yaeeh__xwnh else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    bujfm__oadr = dict(keep=keep)
    lma__qqre = dict(keep='first')
    check_unsupported_args('Series.nlargest', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fim__artcd = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvzr__wgc, xeqe__pxzpc = bodo.libs.array_kernels.nlargest(arr,
            fim__artcd, n, True, bodo.hiframes.series_kernels.gt_f)
        qvg__bxopk = bodo.utils.conversion.convert_to_index(xeqe__pxzpc)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
            qvg__bxopk, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    bujfm__oadr = dict(keep=keep)
    lma__qqre = dict(keep='first')
    check_unsupported_args('Series.nsmallest', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fim__artcd = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvzr__wgc, xeqe__pxzpc = bodo.libs.array_kernels.nlargest(arr,
            fim__artcd, n, False, bodo.hiframes.series_kernels.lt_f)
        qvg__bxopk = bodo.utils.conversion.convert_to_index(xeqe__pxzpc)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
            qvg__bxopk, name)
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
    bujfm__oadr = dict(errors=errors)
    lma__qqre = dict(errors='raise')
    check_unsupported_args('Series.astype', bujfm__oadr, lma__qqre,
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
        cvzr__wgc = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    bujfm__oadr = dict(axis=axis, is_copy=is_copy)
    lma__qqre = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        jfyp__fjxux = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[jfyp__fjxux],
            index[jfyp__fjxux], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    bujfm__oadr = dict(axis=axis, kind=kind, order=order)
    lma__qqre = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cioe__rwr = S.notna().values
        if not cioe__rwr.all():
            cvzr__wgc = np.full(n, -1, np.int64)
            cvzr__wgc[cioe__rwr] = argsort(arr[cioe__rwr])
        else:
            cvzr__wgc = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    bujfm__oadr = dict(axis=axis, numeric_only=numeric_only)
    lma__qqre = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', bujfm__oadr, lma__qqre,
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
        cvzr__wgc = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    bujfm__oadr = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    lma__qqre = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    wvnbk__ijn = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xmkq__tybrv = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, wvnbk__ijn)
        qkx__heko = xmkq__tybrv.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        cvzr__wgc = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(qkx__heko
            , 0)
        qvg__bxopk = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            qkx__heko)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
            qvg__bxopk, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    bujfm__oadr = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    lma__qqre = dict(axis=0, inplace=False, kind='quicksort', ignore_index=
        False, key=None)
    check_unsupported_args('Series.sort_values', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    omadr__pwxhl = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xmkq__tybrv = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, omadr__pwxhl)
        qkx__heko = xmkq__tybrv.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        cvzr__wgc = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(qkx__heko
            , 0)
        qvg__bxopk = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            qkx__heko)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
            qvg__bxopk, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    hvxr__cfpp = is_overload_true(is_nullable)
    chngq__nojh = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    chngq__nojh += '  numba.parfors.parfor.init_prange()\n'
    chngq__nojh += '  n = len(arr)\n'
    if hvxr__cfpp:
        chngq__nojh += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        chngq__nojh += '  out_arr = np.empty(n, np.int64)\n'
    chngq__nojh += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    chngq__nojh += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if hvxr__cfpp:
        chngq__nojh += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        chngq__nojh += '      out_arr[i] = -1\n'
    chngq__nojh += '      continue\n'
    chngq__nojh += '    val = arr[i]\n'
    chngq__nojh += '    if include_lowest and val == bins[0]:\n'
    chngq__nojh += '      ind = 1\n'
    chngq__nojh += '    else:\n'
    chngq__nojh += '      ind = np.searchsorted(bins, val)\n'
    chngq__nojh += '    if ind == 0 or ind == len(bins):\n'
    if hvxr__cfpp:
        chngq__nojh += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        chngq__nojh += '      out_arr[i] = -1\n'
    chngq__nojh += '    else:\n'
    chngq__nojh += '      out_arr[i] = ind - 1\n'
    chngq__nojh += '  return out_arr\n'
    mse__vch = {}
    exec(chngq__nojh, {'bodo': bodo, 'np': np, 'numba': numba}, mse__vch)
    impl = mse__vch['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        zhrwd__nty, qrnh__hbhv = np.divmod(x, 1)
        if zhrwd__nty == 0:
            aaf__cda = -int(np.floor(np.log10(abs(qrnh__hbhv)))
                ) - 1 + precision
        else:
            aaf__cda = precision
        return np.around(x, aaf__cda)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        fgig__asq = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(fgig__asq)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        ufru__bbno = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            nhuv__ikqgf = bins.copy()
            if right and include_lowest:
                nhuv__ikqgf[0] = nhuv__ikqgf[0] - ufru__bbno
            evke__hxgpp = bodo.libs.interval_arr_ext.init_interval_array(
                nhuv__ikqgf[:-1], nhuv__ikqgf[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(evke__hxgpp,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        nhuv__ikqgf = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            nhuv__ikqgf[0] = nhuv__ikqgf[0] - 10.0 ** -precision
        evke__hxgpp = bodo.libs.interval_arr_ext.init_interval_array(
            nhuv__ikqgf[:-1], nhuv__ikqgf[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(evke__hxgpp, None
            )
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        vta__nupj = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        xejf__heg = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        cvzr__wgc = np.zeros(nbins, np.int64)
        for ycf__qbufn in range(len(vta__nupj)):
            cvzr__wgc[xejf__heg[ycf__qbufn]] = vta__nupj[ycf__qbufn]
        return cvzr__wgc
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
            mheyp__cwzvv = (max_val - min_val) * 0.001
            if right:
                bins[0] -= mheyp__cwzvv
            else:
                bins[-1] += mheyp__cwzvv
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    bujfm__oadr = dict(dropna=dropna)
    lma__qqre = dict(dropna=True)
    check_unsupported_args('Series.value_counts', bujfm__oadr, lma__qqre,
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
    pwiwx__caryk = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    chngq__nojh = 'def impl(\n'
    chngq__nojh += '    S,\n'
    chngq__nojh += '    normalize=False,\n'
    chngq__nojh += '    sort=True,\n'
    chngq__nojh += '    ascending=False,\n'
    chngq__nojh += '    bins=None,\n'
    chngq__nojh += '    dropna=True,\n'
    chngq__nojh += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    chngq__nojh += '):\n'
    chngq__nojh += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    chngq__nojh += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    chngq__nojh += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if pwiwx__caryk:
        chngq__nojh += '    right = True\n'
        chngq__nojh += _gen_bins_handling(bins, S.dtype)
        chngq__nojh += '    arr = get_bin_inds(bins, arr)\n'
    chngq__nojh += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    chngq__nojh += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    chngq__nojh += '    )\n'
    chngq__nojh += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if pwiwx__caryk:
        chngq__nojh += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        chngq__nojh += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        chngq__nojh += '    index = get_bin_labels(bins)\n'
    else:
        chngq__nojh += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        chngq__nojh += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        chngq__nojh += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        chngq__nojh += '    )\n'
        chngq__nojh += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    chngq__nojh += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        chngq__nojh += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        vcw__kwz = 'len(S)' if pwiwx__caryk else 'count_arr.sum()'
        chngq__nojh += f'    res = res / float({vcw__kwz})\n'
    chngq__nojh += '    return res\n'
    mse__vch = {}
    exec(chngq__nojh, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, mse__vch)
    impl = mse__vch['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    chngq__nojh = ''
    if isinstance(bins, types.Integer):
        chngq__nojh += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        chngq__nojh += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            chngq__nojh += '    min_val = min_val.value\n'
            chngq__nojh += '    max_val = max_val.value\n'
        chngq__nojh += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            chngq__nojh += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        chngq__nojh += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return chngq__nojh


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    bujfm__oadr = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    lma__qqre = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    chngq__nojh = 'def impl(\n'
    chngq__nojh += '    x,\n'
    chngq__nojh += '    bins,\n'
    chngq__nojh += '    right=True,\n'
    chngq__nojh += '    labels=None,\n'
    chngq__nojh += '    retbins=False,\n'
    chngq__nojh += '    precision=3,\n'
    chngq__nojh += '    include_lowest=False,\n'
    chngq__nojh += "    duplicates='raise',\n"
    chngq__nojh += '    ordered=True\n'
    chngq__nojh += '):\n'
    if isinstance(x, SeriesType):
        chngq__nojh += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        chngq__nojh += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        chngq__nojh += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        chngq__nojh += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    chngq__nojh += _gen_bins_handling(bins, x.dtype)
    chngq__nojh += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    chngq__nojh += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    chngq__nojh += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    chngq__nojh += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        chngq__nojh += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        chngq__nojh += '    return res\n'
    else:
        chngq__nojh += '    return out_arr\n'
    mse__vch = {}
    exec(chngq__nojh, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, mse__vch)
    impl = mse__vch['impl']
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
    bujfm__oadr = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    lma__qqre = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        shvpz__nyh = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, shvpz__nyh)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    bujfm__oadr = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze
        =squeeze, observed=observed, dropna=dropna)
    lma__qqre = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', bujfm__oadr, lma__qqre,
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
        msbtr__clnu = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            ctgo__pkk = bodo.utils.conversion.coerce_to_array(index)
            xmkq__tybrv = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                ctgo__pkk, arr), index, msbtr__clnu)
            return xmkq__tybrv.groupby(' ')['']
        return impl_index
    ajpvz__usxcv = by
    if isinstance(by, SeriesType):
        ajpvz__usxcv = by.data
    if isinstance(ajpvz__usxcv, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    sleza__cgoa = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        ctgo__pkk = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        xmkq__tybrv = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            ctgo__pkk, arr), index, sleza__cgoa)
        return xmkq__tybrv.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    bujfm__oadr = dict(verify_integrity=verify_integrity)
    lma__qqre = dict(verify_integrity=False)
    check_unsupported_args('Series.append', bujfm__oadr, lma__qqre,
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
            otfec__eamkv = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            cvzr__wgc = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(cvzr__wgc, A, otfec__eamkv, False)
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index,
                name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvzr__wgc = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    bujfm__oadr = dict(interpolation=interpolation)
    lma__qqre = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            cvzr__wgc = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index,
                name)
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
        tqo__plfre = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(tqo__plfre, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    bujfm__oadr = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    lma__qqre = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', bujfm__oadr, lma__qqre,
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
        wwydr__ksvxm = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        wwydr__ksvxm = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    chngq__nojh = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {wwydr__ksvxm}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    hby__deh = dict()
    exec(chngq__nojh, {'bodo': bodo, 'numba': numba}, hby__deh)
    rohfk__rpou = hby__deh['impl']
    return rohfk__rpou


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        wwydr__ksvxm = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        wwydr__ksvxm = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    chngq__nojh = 'def impl(S,\n'
    chngq__nojh += '     value=None,\n'
    chngq__nojh += '    method=None,\n'
    chngq__nojh += '    axis=None,\n'
    chngq__nojh += '    inplace=False,\n'
    chngq__nojh += '    limit=None,\n'
    chngq__nojh += '   downcast=None,\n'
    chngq__nojh += '):\n'
    chngq__nojh += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    chngq__nojh += '    n = len(in_arr)\n'
    chngq__nojh += f'    out_arr = {wwydr__ksvxm}(n, -1)\n'
    chngq__nojh += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    chngq__nojh += '        s = in_arr[j]\n'
    chngq__nojh += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    chngq__nojh += '            s = value\n'
    chngq__nojh += '        out_arr[j] = s\n'
    chngq__nojh += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    hby__deh = dict()
    exec(chngq__nojh, {'bodo': bodo, 'numba': numba}, hby__deh)
    rohfk__rpou = hby__deh['impl']
    return rohfk__rpou


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
    nbwbr__ibhir = bodo.hiframes.pd_series_ext.get_series_data(value)
    for ycf__qbufn in numba.parfors.parfor.internal_prange(len(vmtox__yzlg)):
        s = vmtox__yzlg[ycf__qbufn]
        if bodo.libs.array_kernels.isna(vmtox__yzlg, ycf__qbufn
            ) and not bodo.libs.array_kernels.isna(nbwbr__ibhir, ycf__qbufn):
            s = nbwbr__ibhir[ycf__qbufn]
        vmtox__yzlg[ycf__qbufn] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
    for ycf__qbufn in numba.parfors.parfor.internal_prange(len(vmtox__yzlg)):
        s = vmtox__yzlg[ycf__qbufn]
        if bodo.libs.array_kernels.isna(vmtox__yzlg, ycf__qbufn):
            s = value
        vmtox__yzlg[ycf__qbufn] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    nbwbr__ibhir = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(vmtox__yzlg)
    cvzr__wgc = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for tjuw__jvae in numba.parfors.parfor.internal_prange(n):
        s = vmtox__yzlg[tjuw__jvae]
        if bodo.libs.array_kernels.isna(vmtox__yzlg, tjuw__jvae
            ) and not bodo.libs.array_kernels.isna(nbwbr__ibhir, tjuw__jvae):
            s = nbwbr__ibhir[tjuw__jvae]
        cvzr__wgc[tjuw__jvae] = s
        if bodo.libs.array_kernels.isna(vmtox__yzlg, tjuw__jvae
            ) and bodo.libs.array_kernels.isna(nbwbr__ibhir, tjuw__jvae):
            bodo.libs.array_kernels.setna(cvzr__wgc, tjuw__jvae)
    return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    nbwbr__ibhir = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(vmtox__yzlg)
    cvzr__wgc = bodo.utils.utils.alloc_type(n, vmtox__yzlg.dtype, (-1,))
    for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
        s = vmtox__yzlg[ycf__qbufn]
        if bodo.libs.array_kernels.isna(vmtox__yzlg, ycf__qbufn
            ) and not bodo.libs.array_kernels.isna(nbwbr__ibhir, ycf__qbufn):
            s = nbwbr__ibhir[ycf__qbufn]
        cvzr__wgc[ycf__qbufn] = s
    return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    bujfm__oadr = dict(limit=limit, downcast=downcast)
    lma__qqre = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')
    xjwzx__ygu = not is_overload_none(value)
    wij__epvej = not is_overload_none(method)
    if xjwzx__ygu and wij__epvej:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not xjwzx__ygu and not wij__epvej:
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
    if wij__epvej:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        cphzb__oim = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(cphzb__oim)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(cphzb__oim)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    mgbv__sdwjx = element_type(S.data)
    hymgl__jureh = None
    if xjwzx__ygu:
        hymgl__jureh = element_type(types.unliteral(value))
    if hymgl__jureh and not can_replace(mgbv__sdwjx, hymgl__jureh):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {hymgl__jureh} with series type {mgbv__sdwjx}'
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
        naz__nvh = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                nbwbr__ibhir = bodo.hiframes.pd_series_ext.get_series_data(
                    value)
                n = len(vmtox__yzlg)
                cvzr__wgc = bodo.utils.utils.alloc_type(n, naz__nvh, (-1,))
                for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(vmtox__yzlg, ycf__qbufn
                        ) and bodo.libs.array_kernels.isna(nbwbr__ibhir,
                        ycf__qbufn):
                        bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                        continue
                    if bodo.libs.array_kernels.isna(vmtox__yzlg, ycf__qbufn):
                        cvzr__wgc[ycf__qbufn
                            ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                            nbwbr__ibhir[ycf__qbufn])
                        continue
                    cvzr__wgc[ycf__qbufn
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        vmtox__yzlg[ycf__qbufn])
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                    index, name)
            return fillna_series_impl
        if wij__epvej:
            jciym__vqq = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(mgbv__sdwjx, (types.Integer, types.Float)
                ) and mgbv__sdwjx not in jciym__vqq:
                raise BodoError(
                    f"Series.fillna(): series of type {mgbv__sdwjx} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                cvzr__wgc = bodo.libs.array_kernels.ffill_bfill_arr(vmtox__yzlg
                    , method)
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_tz_naive_timestamp(value)
            vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(vmtox__yzlg)
            cvzr__wgc = bodo.utils.utils.alloc_type(n, naz__nvh, (-1,))
            for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    vmtox__yzlg[ycf__qbufn])
                if bodo.libs.array_kernels.isna(vmtox__yzlg, ycf__qbufn):
                    s = value
                cvzr__wgc[ycf__qbufn] = s
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index,
                name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        wuk__aqzvv = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        bujfm__oadr = dict(limit=limit, downcast=downcast)
        lma__qqre = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', bujfm__oadr,
            lma__qqre, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        mgbv__sdwjx = element_type(S.data)
        jciym__vqq = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(mgbv__sdwjx, (types.Integer, types.Float)
            ) and mgbv__sdwjx not in jciym__vqq:
            raise BodoError(
                f'Series.{overload_name}(): series of type {mgbv__sdwjx} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            cvzr__wgc = bodo.libs.array_kernels.ffill_bfill_arr(vmtox__yzlg,
                wuk__aqzvv)
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index,
                name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        dqyb__buey = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            dqyb__buey)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        pges__jxz = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(pges__jxz)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        pges__jxz = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(pges__jxz)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        pges__jxz = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(pges__jxz)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    bujfm__oadr = dict(inplace=inplace, limit=limit, regex=regex, method=method
        )
    vwjx__hsul = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', bujfm__oadr, vwjx__hsul,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    mgbv__sdwjx = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        gbtn__yuqs = element_type(to_replace.key_type)
        hymgl__jureh = element_type(to_replace.value_type)
    else:
        gbtn__yuqs = element_type(to_replace)
        hymgl__jureh = element_type(value)
    qwznt__hwlag = None
    if mgbv__sdwjx != types.unliteral(gbtn__yuqs):
        if bodo.utils.typing.equality_always_false(mgbv__sdwjx, types.
            unliteral(gbtn__yuqs)
            ) or not bodo.utils.typing.types_equality_exists(mgbv__sdwjx,
            gbtn__yuqs):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(mgbv__sdwjx, (types.Float, types.Integer)
            ) or mgbv__sdwjx == np.bool_:
            qwznt__hwlag = mgbv__sdwjx
    if not can_replace(mgbv__sdwjx, types.unliteral(hymgl__jureh)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    hoyp__tmf = to_str_arr_if_dict_array(S.data)
    if isinstance(hoyp__tmf, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(vmtox__yzlg.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(vmtox__yzlg)
        cvzr__wgc = bodo.utils.utils.alloc_type(n, hoyp__tmf, (-1,))
        rlvn__fbx = build_replace_dict(to_replace, value, qwznt__hwlag)
        for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(vmtox__yzlg, ycf__qbufn):
                bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                continue
            s = vmtox__yzlg[ycf__qbufn]
            if s in rlvn__fbx:
                s = rlvn__fbx[s]
            cvzr__wgc[ycf__qbufn] = s
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    sjjnr__kzk = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    fufhb__nzds = is_iterable_type(to_replace)
    xkzex__tcc = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    ykaz__unq = is_iterable_type(value)
    if sjjnr__kzk and xkzex__tcc:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                rlvn__fbx = {}
                rlvn__fbx[key_dtype_conv(to_replace)] = value
                return rlvn__fbx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            rlvn__fbx = {}
            rlvn__fbx[to_replace] = value
            return rlvn__fbx
        return impl
    if fufhb__nzds and xkzex__tcc:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                rlvn__fbx = {}
                for hnva__fzey in to_replace:
                    rlvn__fbx[key_dtype_conv(hnva__fzey)] = value
                return rlvn__fbx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            rlvn__fbx = {}
            for hnva__fzey in to_replace:
                rlvn__fbx[hnva__fzey] = value
            return rlvn__fbx
        return impl
    if fufhb__nzds and ykaz__unq:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                rlvn__fbx = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for ycf__qbufn in range(len(to_replace)):
                    rlvn__fbx[key_dtype_conv(to_replace[ycf__qbufn])] = value[
                        ycf__qbufn]
                return rlvn__fbx
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            rlvn__fbx = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for ycf__qbufn in range(len(to_replace)):
                rlvn__fbx[to_replace[ycf__qbufn]] = value[ycf__qbufn]
            return rlvn__fbx
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
            cvzr__wgc = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index,
                name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvzr__wgc = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    bujfm__oadr = dict(ignore_index=ignore_index)
    jgc__lvws = dict(ignore_index=False)
    check_unsupported_args('Series.explode', bujfm__oadr, jgc__lvws,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fim__artcd = bodo.utils.conversion.index_to_array(index)
        cvzr__wgc, fcebi__kjxeu = bodo.libs.array_kernels.explode(arr,
            fim__artcd)
        qvg__bxopk = bodo.utils.conversion.index_from_array(fcebi__kjxeu)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
            qvg__bxopk, name)
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
            ird__ewu = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                ird__ewu[ycf__qbufn] = np.argmax(a[ycf__qbufn])
            return ird__ewu
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            rvf__ygpzr = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                rvf__ygpzr[ycf__qbufn] = np.argmin(a[ycf__qbufn])
            return rvf__ygpzr
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType) and isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            fbtq__gcnr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo
                .hiframes.pd_series_ext.get_series_data(b))
            return np.dot(arr, fbtq__gcnr)
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
    bujfm__oadr = dict(axis=axis, inplace=inplace, how=how)
    mvt__zip = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', bujfm__oadr, mvt__zip,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            cioe__rwr = S.notna().values
            fim__artcd = bodo.utils.conversion.extract_index_array(S)
            qvg__bxopk = bodo.utils.conversion.convert_to_index(fim__artcd[
                cioe__rwr])
            cvzr__wgc = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(vmtox__yzlg))
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                qvg__bxopk, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            fim__artcd = bodo.utils.conversion.extract_index_array(S)
            cioe__rwr = S.notna().values
            qvg__bxopk = bodo.utils.conversion.convert_to_index(fim__artcd[
                cioe__rwr])
            cvzr__wgc = vmtox__yzlg[cioe__rwr]
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                qvg__bxopk, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    bujfm__oadr = dict(freq=freq, axis=axis)
    lma__qqre = dict(freq=None, axis=0)
    check_unsupported_args('Series.shift', bujfm__oadr, lma__qqre,
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
        cvzr__wgc = bodo.hiframes.rolling.shift(arr, periods, False, fill_value
            )
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    bujfm__oadr = dict(fill_method=fill_method, limit=limit, freq=freq)
    lma__qqre = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', bujfm__oadr, lma__qqre,
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
        cvzr__wgc = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
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
            xas__mjx = 'None'
        else:
            xas__mjx = 'other'
        chngq__nojh = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            chngq__nojh += '  cond = ~cond\n'
        chngq__nojh += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        chngq__nojh += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        chngq__nojh += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        chngq__nojh += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {xas__mjx})\n'
            )
        chngq__nojh += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        mse__vch = {}
        exec(chngq__nojh, {'bodo': bodo, 'np': np}, mse__vch)
        impl = mse__vch['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        dqyb__buey = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(dqyb__buey)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    bujfm__oadr = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    lma__qqre = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', bujfm__oadr, lma__qqre,
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
    kzcjz__iknmd = is_overload_constant_nan(other)
    if not (is_default or kzcjz__iknmd or is_scalar_type(other) or 
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
            vfbu__vlpwc = arr.dtype.elem_type
        else:
            vfbu__vlpwc = arr.dtype
        if is_iterable_type(other):
            hijgj__jbgv = other.dtype
        elif kzcjz__iknmd:
            hijgj__jbgv = types.float64
        else:
            hijgj__jbgv = types.unliteral(other)
        if not kzcjz__iknmd and not is_common_scalar_dtype([vfbu__vlpwc,
            hijgj__jbgv]):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        bujfm__oadr = dict(level=level, axis=axis)
        lma__qqre = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), bujfm__oadr,
            lma__qqre, package_name='pandas', module_name='Series')
        spqof__cgrxu = other == string_type or is_overload_constant_str(other)
        qfohk__vmdxq = is_iterable_type(other) and other.dtype == string_type
        fikgw__gbvwc = S.dtype == string_type and (op == operator.add and (
            spqof__cgrxu or qfohk__vmdxq) or op == operator.mul and
            isinstance(other, types.Integer))
        wqjo__mmnzt = S.dtype == bodo.timedelta64ns
        toxf__wou = S.dtype == bodo.datetime64ns
        tps__hrclw = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        dyhe__ywoja = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype ==
            pd_timestamp_tz_naive_type or other.dtype == bodo.datetime64ns)
        imv__myc = wqjo__mmnzt and (tps__hrclw or dyhe__ywoja
            ) or toxf__wou and tps__hrclw
        imv__myc = imv__myc and op == operator.add
        if not (isinstance(S.dtype, types.Number) or fikgw__gbvwc or imv__myc):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        jqwrt__skur = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            hoyp__tmf = jqwrt__skur.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and hoyp__tmf == types.Array(types.bool_, 1, 'C'):
                hoyp__tmf = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_tz_naive_timestamp(other
                    )
                n = len(arr)
                cvzr__wgc = bodo.utils.utils.alloc_type(n, hoyp__tmf, (-1,))
                for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                    dnmr__pes = bodo.libs.array_kernels.isna(arr, ycf__qbufn)
                    if dnmr__pes:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn
                                )
                        else:
                            cvzr__wgc[ycf__qbufn] = op(fill_value, other)
                    else:
                        cvzr__wgc[ycf__qbufn] = op(arr[ycf__qbufn], other)
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        hoyp__tmf = jqwrt__skur.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and hoyp__tmf == types.Array(types.bool_, 1, 'C'):
            hoyp__tmf = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rtcu__njby = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            cvzr__wgc = bodo.utils.utils.alloc_type(n, hoyp__tmf, (-1,))
            for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                dnmr__pes = bodo.libs.array_kernels.isna(arr, ycf__qbufn)
                tlrz__plr = bodo.libs.array_kernels.isna(rtcu__njby, ycf__qbufn
                    )
                if dnmr__pes and tlrz__plr:
                    bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                elif dnmr__pes:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                    else:
                        cvzr__wgc[ycf__qbufn] = op(fill_value, rtcu__njby[
                            ycf__qbufn])
                elif tlrz__plr:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                    else:
                        cvzr__wgc[ycf__qbufn] = op(arr[ycf__qbufn], fill_value)
                else:
                    cvzr__wgc[ycf__qbufn] = op(arr[ycf__qbufn], rtcu__njby[
                        ycf__qbufn])
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index,
                name)
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
        jqwrt__skur = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            hoyp__tmf = jqwrt__skur.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and hoyp__tmf == types.Array(types.bool_, 1, 'C'):
                hoyp__tmf = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                cvzr__wgc = bodo.utils.utils.alloc_type(n, hoyp__tmf, None)
                for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                    dnmr__pes = bodo.libs.array_kernels.isna(arr, ycf__qbufn)
                    if dnmr__pes:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn
                                )
                        else:
                            cvzr__wgc[ycf__qbufn] = op(other, fill_value)
                    else:
                        cvzr__wgc[ycf__qbufn] = op(other, arr[ycf__qbufn])
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        hoyp__tmf = jqwrt__skur.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and hoyp__tmf == types.Array(types.bool_, 1, 'C'):
            hoyp__tmf = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rtcu__njby = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            cvzr__wgc = bodo.utils.utils.alloc_type(n, hoyp__tmf, None)
            for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                dnmr__pes = bodo.libs.array_kernels.isna(arr, ycf__qbufn)
                tlrz__plr = bodo.libs.array_kernels.isna(rtcu__njby, ycf__qbufn
                    )
                cvzr__wgc[ycf__qbufn] = op(rtcu__njby[ycf__qbufn], arr[
                    ycf__qbufn])
                if dnmr__pes and tlrz__plr:
                    bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                elif dnmr__pes:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                    else:
                        cvzr__wgc[ycf__qbufn] = op(rtcu__njby[ycf__qbufn],
                            fill_value)
                elif tlrz__plr:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                    else:
                        cvzr__wgc[ycf__qbufn] = op(fill_value, arr[ycf__qbufn])
                else:
                    cvzr__wgc[ycf__qbufn] = op(rtcu__njby[ycf__qbufn], arr[
                        ycf__qbufn])
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index,
                name)
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
    for op, zehy__qvt in explicit_binop_funcs_two_ways.items():
        for name in zehy__qvt:
            dqyb__buey = create_explicit_binary_op_overload(op)
            enb__kvlpj = create_explicit_binary_reverse_op_overload(op)
            tom__oofy = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(dqyb__buey)
            overload_method(SeriesType, tom__oofy, no_unliteral=True)(
                enb__kvlpj)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        dqyb__buey = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(dqyb__buey)
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
                wolbd__ayy = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                cvzr__wgc = dt64_arr_sub(arr, wolbd__ayy)
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
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
                cvzr__wgc = np.empty(n, np.dtype('datetime64[ns]'))
                for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, ycf__qbufn):
                        bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                        continue
                    ioj__amqvc = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[ycf__qbufn]))
                    zbp__vlm = op(ioj__amqvc, rhs)
                    cvzr__wgc[ycf__qbufn
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        zbp__vlm.value)
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
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
                    wolbd__ayy = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    cvzr__wgc = op(arr, bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(wolbd__ayy))
                    return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                wolbd__ayy = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                cvzr__wgc = op(arr, wolbd__ayy)
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    pwzf__ivgil = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    cvzr__wgc = op(bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(pwzf__ivgil), arr)
                    return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                pwzf__ivgil = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                cvzr__wgc = op(pwzf__ivgil, arr)
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        dqyb__buey = create_binary_op_overload(op)
        overload(op)(dqyb__buey)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    uiuz__kqhm = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, uiuz__kqhm)
        for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, ycf__qbufn
                ) or bodo.libs.array_kernels.isna(arg2, ycf__qbufn):
                bodo.libs.array_kernels.setna(S, ycf__qbufn)
                continue
            S[ycf__qbufn
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                ycf__qbufn]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[ycf__qbufn]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                rtcu__njby = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, rtcu__njby)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        dqyb__buey = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(dqyb__buey)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                cvzr__wgc = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        dqyb__buey = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(dqyb__buey)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    cvzr__wgc = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
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
                    rtcu__njby = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    cvzr__wgc = ufunc(arr, rtcu__njby)
                    return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    rtcu__njby = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    cvzr__wgc = ufunc(arr, rtcu__njby)
                    return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        dqyb__buey = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(dqyb__buey)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        czlt__yfg = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),))
        eew__wis = np.arange(n),
        bodo.libs.timsort.sort(czlt__yfg, 0, n, eew__wis)
        return eew__wis[0]
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
        ogsd__jjod = get_overload_const_str(downcast)
        if ogsd__jjod in ('integer', 'signed'):
            out_dtype = types.int64
        elif ogsd__jjod == 'unsigned':
            out_dtype = types.uint64
        else:
            assert ogsd__jjod == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            vmtox__yzlg = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            cvzr__wgc = pd.to_numeric(vmtox__yzlg, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index,
                name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if arg_a == bodo.dict_str_arr_type:
        return (lambda arg_a, errors='raise', downcast=None: bodo.libs.
            dict_arr_ext.dict_arr_to_numeric(arg_a, errors, downcast))
    bcqi__yvmxp = types.Array(types.float64, 1, 'C'
        ) if out_dtype == types.float64 else IntegerArrayType(types.int64)

    def to_numeric_impl(arg_a, errors='raise', downcast=None):
        numba.parfors.parfor.init_prange()
        n = len(arg_a)
        ydcu__nvmco = bodo.utils.utils.alloc_type(n, bcqi__yvmxp, (-1,))
        for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg_a, ycf__qbufn):
                bodo.libs.array_kernels.setna(ydcu__nvmco, ycf__qbufn)
            else:
                bodo.libs.str_arr_ext.str_arr_item_to_numeric(ydcu__nvmco,
                    ycf__qbufn, arg_a, ycf__qbufn)
        return ydcu__nvmco
    return to_numeric_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        safit__jpkdq = if_series_to_array_type(args[0])
        if isinstance(safit__jpkdq, types.Array) and isinstance(safit__jpkdq
            .dtype, types.Integer):
            safit__jpkdq = types.Array(types.float64, 1, 'C')
        return safit__jpkdq(*args)


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
    eorl__spgve = bodo.utils.utils.is_array_typ(x, True)
    pih__wkej = bodo.utils.utils.is_array_typ(y, True)
    chngq__nojh = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        chngq__nojh += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if eorl__spgve and not bodo.utils.utils.is_array_typ(x, False):
        chngq__nojh += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if pih__wkej and not bodo.utils.utils.is_array_typ(y, False):
        chngq__nojh += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    chngq__nojh += '  n = len(condition)\n'
    aayai__brcaa = x.dtype if eorl__spgve else types.unliteral(x)
    ynaap__kmfn = y.dtype if pih__wkej else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        aayai__brcaa = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        ynaap__kmfn = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    djroj__jhdjy = get_data(x)
    sfukx__pwre = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(eew__wis) for eew__wis in
        [djroj__jhdjy, sfukx__pwre])
    if sfukx__pwre == types.none:
        if isinstance(aayai__brcaa, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif djroj__jhdjy == sfukx__pwre and not is_nullable:
        out_dtype = dtype_to_array_type(aayai__brcaa)
    elif aayai__brcaa == string_type or ynaap__kmfn == string_type:
        out_dtype = bodo.string_array_type
    elif djroj__jhdjy == bytes_type or (eorl__spgve and aayai__brcaa ==
        bytes_type) and (sfukx__pwre == bytes_type or pih__wkej and 
        ynaap__kmfn == bytes_type):
        out_dtype = binary_array_type
    elif isinstance(aayai__brcaa, bodo.PDCategoricalDtype):
        out_dtype = None
    elif aayai__brcaa in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(aayai__brcaa, 1, 'C')
    elif ynaap__kmfn in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(ynaap__kmfn, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(aayai__brcaa), numba.np.numpy_support.
            as_dtype(ynaap__kmfn)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(aayai__brcaa, bodo.PDCategoricalDtype):
        pfk__yffuk = 'x'
    else:
        pfk__yffuk = 'out_dtype'
    chngq__nojh += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {pfk__yffuk}, (-1,))\n')
    if isinstance(aayai__brcaa, bodo.PDCategoricalDtype):
        chngq__nojh += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        chngq__nojh += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    chngq__nojh += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    chngq__nojh += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if eorl__spgve:
        chngq__nojh += '      if bodo.libs.array_kernels.isna(x, j):\n'
        chngq__nojh += '        setna(out_arr, j)\n'
        chngq__nojh += '        continue\n'
    if isinstance(aayai__brcaa, bodo.PDCategoricalDtype):
        chngq__nojh += '      out_codes[j] = x_codes[j]\n'
    else:
        chngq__nojh += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('x[j]' if eorl__spgve else 'x'))
    chngq__nojh += '    else:\n'
    if pih__wkej:
        chngq__nojh += '      if bodo.libs.array_kernels.isna(y, j):\n'
        chngq__nojh += '        setna(out_arr, j)\n'
        chngq__nojh += '        continue\n'
    if sfukx__pwre == types.none:
        if isinstance(aayai__brcaa, bodo.PDCategoricalDtype):
            chngq__nojh += '      out_codes[j] = -1\n'
        else:
            chngq__nojh += '      setna(out_arr, j)\n'
    else:
        chngq__nojh += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('y[j]' if pih__wkej else 'y'))
    chngq__nojh += '  return out_arr\n'
    mse__vch = {}
    exec(chngq__nojh, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, mse__vch)
    ituba__kcd = mse__vch['_impl']
    return ituba__kcd


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
        chfp__tnp = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(chfp__tnp, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(chfp__tnp):
            zojx__npoov = chfp__tnp.data.dtype
        else:
            zojx__npoov = chfp__tnp.dtype
        if isinstance(zojx__npoov, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        ttywd__qoew = chfp__tnp
    else:
        fqw__rsabt = []
        for chfp__tnp in choicelist:
            if not bodo.utils.utils.is_array_typ(chfp__tnp, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(chfp__tnp):
                zojx__npoov = chfp__tnp.data.dtype
            else:
                zojx__npoov = chfp__tnp.dtype
            if isinstance(zojx__npoov, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            fqw__rsabt.append(zojx__npoov)
        if not is_common_scalar_dtype(fqw__rsabt):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        ttywd__qoew = choicelist[0]
    if is_series_type(ttywd__qoew):
        ttywd__qoew = ttywd__qoew.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, ttywd__qoew.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(ttywd__qoew, types.Array) or isinstance(ttywd__qoew,
        BooleanArrayType) or isinstance(ttywd__qoew, IntegerArrayType) or
        isinstance(ttywd__qoew, FloatingArrayType) or bodo.utils.utils.
        is_array_typ(ttywd__qoew, False) and ttywd__qoew.dtype in [bodo.
        string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {ttywd__qoew} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    cajeh__guub = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        kxzny__punt = choicelist.dtype
    else:
        lofh__lgl = False
        fqw__rsabt = []
        for chfp__tnp in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(chfp__tnp
                , 'numpy.select()')
            if is_nullable_type(chfp__tnp):
                lofh__lgl = True
            if is_series_type(chfp__tnp):
                zojx__npoov = chfp__tnp.data.dtype
            else:
                zojx__npoov = chfp__tnp.dtype
            if isinstance(zojx__npoov, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            fqw__rsabt.append(zojx__npoov)
        oema__lwz, tnlo__mfxo = get_common_scalar_dtype(fqw__rsabt)
        if not tnlo__mfxo:
            raise BodoError('Internal error in overload_np_select')
        wux__rdj = dtype_to_array_type(oema__lwz)
        if lofh__lgl:
            wux__rdj = to_nullable_type(wux__rdj)
        kxzny__punt = wux__rdj
    if isinstance(kxzny__punt, SeriesType):
        kxzny__punt = kxzny__punt.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        iqwdj__imgp = True
    else:
        iqwdj__imgp = False
    akvbd__tfjik = False
    oumkj__rllut = False
    if iqwdj__imgp:
        if isinstance(kxzny__punt.dtype, types.Number):
            pass
        elif kxzny__punt.dtype == types.bool_:
            oumkj__rllut = True
        else:
            akvbd__tfjik = True
            kxzny__punt = to_nullable_type(kxzny__punt)
    elif default == types.none or is_overload_constant_nan(default):
        akvbd__tfjik = True
        kxzny__punt = to_nullable_type(kxzny__punt)
    chngq__nojh = 'def np_select_impl(condlist, choicelist, default=0):\n'
    chngq__nojh += '  if len(condlist) != len(choicelist):\n'
    chngq__nojh += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    chngq__nojh += '  output_len = len(choicelist[0])\n'
    chngq__nojh += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    chngq__nojh += '  for i in range(output_len):\n'
    if akvbd__tfjik:
        chngq__nojh += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif oumkj__rllut:
        chngq__nojh += '    out[i] = False\n'
    else:
        chngq__nojh += '    out[i] = default\n'
    if cajeh__guub:
        chngq__nojh += '  for i in range(len(condlist) - 1, -1, -1):\n'
        chngq__nojh += '    cond = condlist[i]\n'
        chngq__nojh += '    choice = choicelist[i]\n'
        chngq__nojh += '    out = np.where(cond, choice, out)\n'
    else:
        for ycf__qbufn in range(len(choicelist) - 1, -1, -1):
            chngq__nojh += f'  cond = condlist[{ycf__qbufn}]\n'
            chngq__nojh += f'  choice = choicelist[{ycf__qbufn}]\n'
            chngq__nojh += f'  out = np.where(cond, choice, out)\n'
    chngq__nojh += '  return out'
    mse__vch = dict()
    exec(chngq__nojh, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': kxzny__punt}, mse__vch)
    impl = mse__vch['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cvzr__wgc = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    bujfm__oadr = dict(subset=subset, keep=keep, inplace=inplace)
    lma__qqre = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', bujfm__oadr, lma__qqre,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        akfo__hjdsv = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (akfo__hjdsv,), fim__artcd = bodo.libs.array_kernels.drop_duplicates((
            akfo__hjdsv,), index, 1)
        index = bodo.utils.conversion.index_from_array(fim__artcd)
        return bodo.hiframes.pd_series_ext.init_series(akfo__hjdsv, index, name
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
    yzm__kpsq = element_type(S.data)
    if not is_common_scalar_dtype([yzm__kpsq, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([yzm__kpsq, right]):
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
        cvzr__wgc = bodo.libs.bool_arr_ext.alloc_bool_array(n)
        for ycf__qbufn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arr, ycf__qbufn):
                bodo.libs.array_kernels.setna(cvzr__wgc, ycf__qbufn)
                continue
            fsdpq__lqikf = bodo.utils.conversion.box_if_dt64(arr[ycf__qbufn])
            if inclusive == 'both':
                cvzr__wgc[ycf__qbufn
                    ] = fsdpq__lqikf <= right and fsdpq__lqikf >= left
            else:
                cvzr__wgc[ycf__qbufn
                    ] = fsdpq__lqikf < right and fsdpq__lqikf > left
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    bujfm__oadr = dict(axis=axis)
    lma__qqre = dict(axis=None)
    check_unsupported_args('Series.repeat', bujfm__oadr, lma__qqre,
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
            fim__artcd = bodo.utils.conversion.index_to_array(index)
            cvzr__wgc = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            fcebi__kjxeu = bodo.libs.array_kernels.repeat_kernel(fim__artcd,
                repeats)
            qvg__bxopk = bodo.utils.conversion.index_from_array(fcebi__kjxeu)
            return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
                qvg__bxopk, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fim__artcd = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        cvzr__wgc = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        fcebi__kjxeu = bodo.libs.array_kernels.repeat_kernel(fim__artcd,
            repeats)
        qvg__bxopk = bodo.utils.conversion.index_from_array(fcebi__kjxeu)
        return bodo.hiframes.pd_series_ext.init_series(cvzr__wgc,
            qvg__bxopk, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        eew__wis = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(eew__wis)
        jfssh__vznc = {}
        for ycf__qbufn in range(n):
            fsdpq__lqikf = bodo.utils.conversion.box_if_dt64(eew__wis[
                ycf__qbufn])
            jfssh__vznc[index[ycf__qbufn]] = fsdpq__lqikf
        return jfssh__vznc
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    cphzb__oim = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            idln__chbzq = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(cphzb__oim)
    elif is_literal_type(name):
        idln__chbzq = get_literal_value(name)
    else:
        raise_bodo_error(cphzb__oim)
    idln__chbzq = 0 if idln__chbzq is None else idln__chbzq
    iaic__xkz = ColNamesMetaType((idln__chbzq,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            iaic__xkz)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
