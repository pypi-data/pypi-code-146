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
            vhlcw__mqhw = bodo.hiframes.pd_series_ext.get_series_data(s)
            iudf__zvp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                vhlcw__mqhw)
            return iudf__zvp
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
            beqdx__fsfm = list()
            for cvohh__cxj in range(len(S)):
                beqdx__fsfm.append(S.iat[cvohh__cxj])
            return beqdx__fsfm
        return impl_float

    def impl(S):
        beqdx__fsfm = list()
        for cvohh__cxj in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, cvohh__cxj):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            beqdx__fsfm.append(S.iat[cvohh__cxj])
        return beqdx__fsfm
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    xgi__cfu = dict(dtype=dtype, copy=copy, na_value=na_value)
    svn__bqe = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    xgi__cfu = dict(name=name, inplace=inplace)
    svn__bqe = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', xgi__cfu, svn__bqe,
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
        xvfj__rncw = ', '.join(['index_arrs[{}]'.format(cvohh__cxj) for
            cvohh__cxj in range(S.index.nlevels)])
    else:
        xvfj__rncw = '    bodo.utils.conversion.index_to_array(index)\n'
    kqpg__aiac = 'index' if 'index' != series_name else 'level_0'
    yqmnw__zikgn = get_index_names(S.index, 'Series.reset_index()', kqpg__aiac)
    columns = [name for name in yqmnw__zikgn]
    columns.append(series_name)
    iuxtm__gjbi = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    iuxtm__gjbi += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    iuxtm__gjbi += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        iuxtm__gjbi += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    iuxtm__gjbi += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    iuxtm__gjbi += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({xvfj__rncw}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    liszm__hwjm = {}
    exec(iuxtm__gjbi, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, liszm__hwjm)
    rvflv__hvya = liszm__hwjm['_impl']
    return rvflv__hvya


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ckdiz__dqde = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
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
        ckdiz__dqde = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[cvohh__cxj]):
                bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
            else:
                ckdiz__dqde[cvohh__cxj] = np.round(arr[cvohh__cxj], decimals)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    xgi__cfu = dict(level=level, numeric_only=numeric_only)
    svn__bqe = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
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
    xgi__cfu = dict(level=level, numeric_only=numeric_only)
    svn__bqe = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', xgi__cfu, svn__bqe,
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
    xgi__cfu = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level)
    svn__bqe = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
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
        qqky__bsb = bodo.hiframes.pd_series_ext.get_series_data(S)
        yyo__udkez = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        wim__olbqp = 0
        for cvohh__cxj in numba.parfors.parfor.internal_prange(len(qqky__bsb)):
            zemnu__epf = 0
            orv__mhjtb = bodo.libs.array_kernels.isna(qqky__bsb, cvohh__cxj)
            wms__jybhl = bodo.libs.array_kernels.isna(yyo__udkez, cvohh__cxj)
            if orv__mhjtb and not wms__jybhl or not orv__mhjtb and wms__jybhl:
                zemnu__epf = 1
            elif not orv__mhjtb:
                if qqky__bsb[cvohh__cxj] != yyo__udkez[cvohh__cxj]:
                    zemnu__epf = 1
            wim__olbqp += zemnu__epf
        return wim__olbqp == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    xgi__cfu = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level)
    svn__bqe = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    xgi__cfu = dict(level=level)
    svn__bqe = dict(level=None)
    check_unsupported_args('Series.mad', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    upec__jsw = types.float64
    zalyn__ausd = types.float64
    if S.dtype == types.float32:
        upec__jsw = types.float32
        zalyn__ausd = types.float32
    gif__fwp = upec__jsw(0)
    zolbz__zgok = zalyn__ausd(0)
    bkhkg__suw = zalyn__ausd(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        kwnkr__mso = gif__fwp
        wim__olbqp = zolbz__zgok
        for cvohh__cxj in numba.parfors.parfor.internal_prange(len(A)):
            zemnu__epf = gif__fwp
            ufvzr__jzeug = zolbz__zgok
            if not bodo.libs.array_kernels.isna(A, cvohh__cxj) or not skipna:
                zemnu__epf = A[cvohh__cxj]
                ufvzr__jzeug = bkhkg__suw
            kwnkr__mso += zemnu__epf
            wim__olbqp += ufvzr__jzeug
        xtoaj__ahs = bodo.hiframes.series_kernels._mean_handle_nan(kwnkr__mso,
            wim__olbqp)
        qgj__szrf = gif__fwp
        for cvohh__cxj in numba.parfors.parfor.internal_prange(len(A)):
            zemnu__epf = gif__fwp
            if not bodo.libs.array_kernels.isna(A, cvohh__cxj) or not skipna:
                zemnu__epf = abs(A[cvohh__cxj] - xtoaj__ahs)
            qgj__szrf += zemnu__epf
        emih__xnifh = bodo.hiframes.series_kernels._mean_handle_nan(qgj__szrf,
            wim__olbqp)
        return emih__xnifh
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    xgi__cfu = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    svn__bqe = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
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
    xgi__cfu = dict(level=level, numeric_only=numeric_only)
    svn__bqe = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
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
        pfoaa__qunz = 0
        xekgo__fplzs = 0
        wim__olbqp = 0
        for cvohh__cxj in numba.parfors.parfor.internal_prange(len(A)):
            zemnu__epf = 0
            ufvzr__jzeug = 0
            if not bodo.libs.array_kernels.isna(A, cvohh__cxj) or not skipna:
                zemnu__epf = A[cvohh__cxj]
                ufvzr__jzeug = 1
            pfoaa__qunz += zemnu__epf
            xekgo__fplzs += zemnu__epf * zemnu__epf
            wim__olbqp += ufvzr__jzeug
        vfhil__pxoz = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            pfoaa__qunz, xekgo__fplzs, wim__olbqp, ddof)
        ayov__gwaix = bodo.hiframes.series_kernels._sem_handle_nan(vfhil__pxoz,
            wim__olbqp)
        return ayov__gwaix
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    xgi__cfu = dict(level=level, numeric_only=numeric_only)
    svn__bqe = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', xgi__cfu, svn__bqe,
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
        pfoaa__qunz = 0.0
        xekgo__fplzs = 0.0
        iec__hffzi = 0.0
        vnbxk__yavg = 0.0
        wim__olbqp = 0
        for cvohh__cxj in numba.parfors.parfor.internal_prange(len(A)):
            zemnu__epf = 0.0
            ufvzr__jzeug = 0
            if not bodo.libs.array_kernels.isna(A, cvohh__cxj) or not skipna:
                zemnu__epf = np.float64(A[cvohh__cxj])
                ufvzr__jzeug = 1
            pfoaa__qunz += zemnu__epf
            xekgo__fplzs += zemnu__epf ** 2
            iec__hffzi += zemnu__epf ** 3
            vnbxk__yavg += zemnu__epf ** 4
            wim__olbqp += ufvzr__jzeug
        vfhil__pxoz = bodo.hiframes.series_kernels.compute_kurt(pfoaa__qunz,
            xekgo__fplzs, iec__hffzi, vnbxk__yavg, wim__olbqp)
        return vfhil__pxoz
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    xgi__cfu = dict(level=level, numeric_only=numeric_only)
    svn__bqe = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.skew()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        pfoaa__qunz = 0.0
        xekgo__fplzs = 0.0
        iec__hffzi = 0.0
        wim__olbqp = 0
        for cvohh__cxj in numba.parfors.parfor.internal_prange(len(A)):
            zemnu__epf = 0.0
            ufvzr__jzeug = 0
            if not bodo.libs.array_kernels.isna(A, cvohh__cxj) or not skipna:
                zemnu__epf = np.float64(A[cvohh__cxj])
                ufvzr__jzeug = 1
            pfoaa__qunz += zemnu__epf
            xekgo__fplzs += zemnu__epf ** 2
            iec__hffzi += zemnu__epf ** 3
            wim__olbqp += ufvzr__jzeug
        vfhil__pxoz = bodo.hiframes.series_kernels.compute_skew(pfoaa__qunz,
            xekgo__fplzs, iec__hffzi, wim__olbqp)
        return vfhil__pxoz
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    xgi__cfu = dict(level=level, numeric_only=numeric_only)
    svn__bqe = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
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
    xgi__cfu = dict(level=level, numeric_only=numeric_only)
    svn__bqe = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
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
        qqky__bsb = bodo.hiframes.pd_series_ext.get_series_data(S)
        yyo__udkez = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        oki__jlqs = 0
        for cvohh__cxj in numba.parfors.parfor.internal_prange(len(qqky__bsb)):
            nfw__woh = qqky__bsb[cvohh__cxj]
            rilq__qgmt = yyo__udkez[cvohh__cxj]
            oki__jlqs += nfw__woh * rilq__qgmt
        return oki__jlqs
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    xgi__cfu = dict(skipna=skipna)
    svn__bqe = dict(skipna=True)
    check_unsupported_args('Series.cumsum', xgi__cfu, svn__bqe,
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
    xgi__cfu = dict(skipna=skipna)
    svn__bqe = dict(skipna=True)
    check_unsupported_args('Series.cumprod', xgi__cfu, svn__bqe,
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
    xgi__cfu = dict(skipna=skipna)
    svn__bqe = dict(skipna=True)
    check_unsupported_args('Series.cummin', xgi__cfu, svn__bqe,
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
    xgi__cfu = dict(skipna=skipna)
    svn__bqe = dict(skipna=True)
    check_unsupported_args('Series.cummax', xgi__cfu, svn__bqe,
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
    xgi__cfu = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    svn__bqe = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        chbhu__cvhb = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, chbhu__cvhb, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    xgi__cfu = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    svn__bqe = dict(index=None, columns=None, axis=None, copy=True, inplace
        =False)
    check_unsupported_args('Series.rename_axis', xgi__cfu, svn__bqe,
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
    ezc__jla = S.data

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(A)
        ckdiz__dqde = bodo.utils.utils.alloc_type(n, ezc__jla, (-1,))
        for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, cvohh__cxj):
                bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                continue
            ckdiz__dqde[cvohh__cxj] = np.abs(A[cvohh__cxj])
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    xgi__cfu = dict(level=level)
    svn__bqe = dict(level=None)
    check_unsupported_args('Series.count', xgi__cfu, svn__bqe, package_name
        ='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    xgi__cfu = dict(method=method, min_periods=min_periods)
    svn__bqe = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        scoai__gsb = S.sum()
        wlgty__dklok = other.sum()
        a = n * (S * other).sum() - scoai__gsb * wlgty__dklok
        jer__yyrhh = n * (S ** 2).sum() - scoai__gsb ** 2
        vbbr__webk = n * (other ** 2).sum() - wlgty__dklok ** 2
        return a / np.sqrt(jer__yyrhh * vbbr__webk)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    xgi__cfu = dict(min_periods=min_periods)
    svn__bqe = dict(min_periods=None)
    check_unsupported_args('Series.cov', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        scoai__gsb = S.mean()
        wlgty__dklok = other.mean()
        vvb__bxdm = ((S - scoai__gsb) * (other - wlgty__dklok)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(vvb__bxdm, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            mcz__byxbj = np.sign(sum_val)
            return np.inf * mcz__byxbj
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    xgi__cfu = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    svn__bqe = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        jkhh__arxsv = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            min_val = bodo.libs.array_ops.array_op_min(arr)
            return convert_val_to_timestamp(min_val.value, tz=jkhh__arxsv)
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
    xgi__cfu = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    svn__bqe = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        jkhh__arxsv = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            max_val = bodo.libs.array_ops.array_op_max(arr)
            return convert_val_to_timestamp(max_val.value, tz=jkhh__arxsv)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    xgi__cfu = dict(axis=axis, skipna=skipna)
    svn__bqe = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', xgi__cfu, svn__bqe,
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
    xgi__cfu = dict(axis=axis, skipna=skipna)
    svn__bqe = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', xgi__cfu, svn__bqe,
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
    xgi__cfu = dict(level=level, numeric_only=numeric_only)
    svn__bqe = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', xgi__cfu, svn__bqe,
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
        annd__huo = arr[:n]
        fcwd__gklan = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(annd__huo,
            fcwd__gklan, name)
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
        czr__mtzkl = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        annd__huo = arr[czr__mtzkl:]
        fcwd__gklan = index[czr__mtzkl:]
        return bodo.hiframes.pd_series_ext.init_series(annd__huo,
            fcwd__gklan, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    yzy__xkwn = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in yzy__xkwn:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            cgars__iap = index[0]
            sasce__imqm = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                cgars__iap, False))
        else:
            sasce__imqm = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        annd__huo = arr[:sasce__imqm]
        fcwd__gklan = index[:sasce__imqm]
        return bodo.hiframes.pd_series_ext.init_series(annd__huo,
            fcwd__gklan, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    yzy__xkwn = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in yzy__xkwn:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            zarg__dij = index[-1]
            sasce__imqm = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, zarg__dij,
                True))
        else:
            sasce__imqm = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        annd__huo = arr[len(arr) - sasce__imqm:]
        fcwd__gklan = index[len(arr) - sasce__imqm:]
        return bodo.hiframes.pd_series_ext.init_series(annd__huo,
            fcwd__gklan, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        bocv__ixvg = bodo.utils.conversion.index_to_array(index)
        ole__dpq, yqt__gqeqm = bodo.libs.array_kernels.first_last_valid_index(
            arr, bocv__ixvg)
        return yqt__gqeqm if ole__dpq else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        bocv__ixvg = bodo.utils.conversion.index_to_array(index)
        ole__dpq, yqt__gqeqm = bodo.libs.array_kernels.first_last_valid_index(
            arr, bocv__ixvg, False)
        return yqt__gqeqm if ole__dpq else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    xgi__cfu = dict(keep=keep)
    svn__bqe = dict(keep='first')
    check_unsupported_args('Series.nlargest', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        bocv__ixvg = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ckdiz__dqde, pfx__ydgk = bodo.libs.array_kernels.nlargest(arr,
            bocv__ixvg, n, True, bodo.hiframes.series_kernels.gt_f)
        iiwej__plfsl = bodo.utils.conversion.convert_to_index(pfx__ydgk)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
            iiwej__plfsl, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    xgi__cfu = dict(keep=keep)
    svn__bqe = dict(keep='first')
    check_unsupported_args('Series.nsmallest', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        bocv__ixvg = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ckdiz__dqde, pfx__ydgk = bodo.libs.array_kernels.nlargest(arr,
            bocv__ixvg, n, False, bodo.hiframes.series_kernels.lt_f)
        iiwej__plfsl = bodo.utils.conversion.convert_to_index(pfx__ydgk)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
            iiwej__plfsl, name)
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
    xgi__cfu = dict(errors=errors)
    svn__bqe = dict(errors='raise')
    check_unsupported_args('Series.astype', xgi__cfu, svn__bqe,
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
        ckdiz__dqde = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    xgi__cfu = dict(axis=axis, is_copy=is_copy)
    svn__bqe = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        cqqt__uvt = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[cqqt__uvt],
            index[cqqt__uvt], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    xgi__cfu = dict(axis=axis, kind=kind, order=order)
    svn__bqe = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mnzdn__jte = S.notna().values
        if not mnzdn__jte.all():
            ckdiz__dqde = np.full(n, -1, np.int64)
            ckdiz__dqde[mnzdn__jte] = argsort(arr[mnzdn__jte])
        else:
            ckdiz__dqde = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    xgi__cfu = dict(axis=axis, numeric_only=numeric_only)
    svn__bqe = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='Series')
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
        ckdiz__dqde = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    xgi__cfu = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    svn__bqe = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    ksxq__dxa = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        oag__nigmv = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ksxq__dxa)
        bxpb__rvrs = oag__nigmv.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        ckdiz__dqde = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            bxpb__rvrs, 0)
        iiwej__plfsl = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            bxpb__rvrs)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
            iiwej__plfsl, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    xgi__cfu = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    svn__bqe = dict(axis=0, inplace=False, kind='quicksort', ignore_index=
        False, key=None)
    check_unsupported_args('Series.sort_values', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    wubu__hsqgu = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        oag__nigmv = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, wubu__hsqgu)
        bxpb__rvrs = oag__nigmv.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        ckdiz__dqde = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            bxpb__rvrs, 0)
        iiwej__plfsl = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            bxpb__rvrs)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
            iiwej__plfsl, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    mopap__ikw = is_overload_true(is_nullable)
    iuxtm__gjbi = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    iuxtm__gjbi += '  numba.parfors.parfor.init_prange()\n'
    iuxtm__gjbi += '  n = len(arr)\n'
    if mopap__ikw:
        iuxtm__gjbi += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        iuxtm__gjbi += '  out_arr = np.empty(n, np.int64)\n'
    iuxtm__gjbi += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    iuxtm__gjbi += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if mopap__ikw:
        iuxtm__gjbi += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        iuxtm__gjbi += '      out_arr[i] = -1\n'
    iuxtm__gjbi += '      continue\n'
    iuxtm__gjbi += '    val = arr[i]\n'
    iuxtm__gjbi += '    if include_lowest and val == bins[0]:\n'
    iuxtm__gjbi += '      ind = 1\n'
    iuxtm__gjbi += '    else:\n'
    iuxtm__gjbi += '      ind = np.searchsorted(bins, val)\n'
    iuxtm__gjbi += '    if ind == 0 or ind == len(bins):\n'
    if mopap__ikw:
        iuxtm__gjbi += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        iuxtm__gjbi += '      out_arr[i] = -1\n'
    iuxtm__gjbi += '    else:\n'
    iuxtm__gjbi += '      out_arr[i] = ind - 1\n'
    iuxtm__gjbi += '  return out_arr\n'
    liszm__hwjm = {}
    exec(iuxtm__gjbi, {'bodo': bodo, 'np': np, 'numba': numba}, liszm__hwjm)
    impl = liszm__hwjm['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        xicff__qxvg, nnm__jppzm = np.divmod(x, 1)
        if xicff__qxvg == 0:
            kcgy__rde = -int(np.floor(np.log10(abs(nnm__jppzm)))
                ) - 1 + precision
        else:
            kcgy__rde = precision
        return np.around(x, kcgy__rde)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        azb__dlgd = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(azb__dlgd)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        smgn__ojvt = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            vzfhr__agmc = bins.copy()
            if right and include_lowest:
                vzfhr__agmc[0] = vzfhr__agmc[0] - smgn__ojvt
            jqs__vgah = bodo.libs.interval_arr_ext.init_interval_array(
                vzfhr__agmc[:-1], vzfhr__agmc[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(jqs__vgah,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        vzfhr__agmc = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            vzfhr__agmc[0] = vzfhr__agmc[0] - 10.0 ** -precision
        jqs__vgah = bodo.libs.interval_arr_ext.init_interval_array(vzfhr__agmc
            [:-1], vzfhr__agmc[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(jqs__vgah, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        cxsnh__frd = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        pye__spss = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        ckdiz__dqde = np.zeros(nbins, np.int64)
        for cvohh__cxj in range(len(cxsnh__frd)):
            ckdiz__dqde[pye__spss[cvohh__cxj]] = cxsnh__frd[cvohh__cxj]
        return ckdiz__dqde
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
            rjgq__clo = (max_val - min_val) * 0.001
            if right:
                bins[0] -= rjgq__clo
            else:
                bins[-1] += rjgq__clo
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    xgi__cfu = dict(dropna=dropna)
    svn__bqe = dict(dropna=True)
    check_unsupported_args('Series.value_counts', xgi__cfu, svn__bqe,
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
    mbuhi__uqmxw = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    iuxtm__gjbi = 'def impl(\n'
    iuxtm__gjbi += '    S,\n'
    iuxtm__gjbi += '    normalize=False,\n'
    iuxtm__gjbi += '    sort=True,\n'
    iuxtm__gjbi += '    ascending=False,\n'
    iuxtm__gjbi += '    bins=None,\n'
    iuxtm__gjbi += '    dropna=True,\n'
    iuxtm__gjbi += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    iuxtm__gjbi += '):\n'
    iuxtm__gjbi += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    iuxtm__gjbi += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    iuxtm__gjbi += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if mbuhi__uqmxw:
        iuxtm__gjbi += '    right = True\n'
        iuxtm__gjbi += _gen_bins_handling(bins, S.dtype)
        iuxtm__gjbi += '    arr = get_bin_inds(bins, arr)\n'
    iuxtm__gjbi += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    iuxtm__gjbi += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    iuxtm__gjbi += '    )\n'
    iuxtm__gjbi += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if mbuhi__uqmxw:
        iuxtm__gjbi += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        iuxtm__gjbi += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        iuxtm__gjbi += '    index = get_bin_labels(bins)\n'
    else:
        iuxtm__gjbi += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        iuxtm__gjbi += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        iuxtm__gjbi += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        iuxtm__gjbi += '    )\n'
        iuxtm__gjbi += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    iuxtm__gjbi += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        iuxtm__gjbi += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        zvlmd__vqz = 'len(S)' if mbuhi__uqmxw else 'count_arr.sum()'
        iuxtm__gjbi += f'    res = res / float({zvlmd__vqz})\n'
    iuxtm__gjbi += '    return res\n'
    liszm__hwjm = {}
    exec(iuxtm__gjbi, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, liszm__hwjm)
    impl = liszm__hwjm['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    iuxtm__gjbi = ''
    if isinstance(bins, types.Integer):
        iuxtm__gjbi += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        iuxtm__gjbi += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            iuxtm__gjbi += '    min_val = min_val.value\n'
            iuxtm__gjbi += '    max_val = max_val.value\n'
        iuxtm__gjbi += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            iuxtm__gjbi += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        iuxtm__gjbi += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return iuxtm__gjbi


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    xgi__cfu = dict(right=right, labels=labels, retbins=retbins, precision=
        precision, duplicates=duplicates, ordered=ordered)
    svn__bqe = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    iuxtm__gjbi = 'def impl(\n'
    iuxtm__gjbi += '    x,\n'
    iuxtm__gjbi += '    bins,\n'
    iuxtm__gjbi += '    right=True,\n'
    iuxtm__gjbi += '    labels=None,\n'
    iuxtm__gjbi += '    retbins=False,\n'
    iuxtm__gjbi += '    precision=3,\n'
    iuxtm__gjbi += '    include_lowest=False,\n'
    iuxtm__gjbi += "    duplicates='raise',\n"
    iuxtm__gjbi += '    ordered=True\n'
    iuxtm__gjbi += '):\n'
    if isinstance(x, SeriesType):
        iuxtm__gjbi += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        iuxtm__gjbi += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        iuxtm__gjbi += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        iuxtm__gjbi += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    iuxtm__gjbi += _gen_bins_handling(bins, x.dtype)
    iuxtm__gjbi += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    iuxtm__gjbi += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    iuxtm__gjbi += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    iuxtm__gjbi += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        iuxtm__gjbi += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        iuxtm__gjbi += '    return res\n'
    else:
        iuxtm__gjbi += '    return out_arr\n'
    liszm__hwjm = {}
    exec(iuxtm__gjbi, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, liszm__hwjm)
    impl = liszm__hwjm['impl']
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
    xgi__cfu = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    svn__bqe = dict(labels=None, retbins=False, precision=3, duplicates='raise'
        )
    check_unsupported_args('pandas.qcut', xgi__cfu, svn__bqe, package_name=
        'pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        shm__aens = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, shm__aens)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    xgi__cfu = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    svn__bqe = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', xgi__cfu, svn__bqe,
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
        lptr__mpgyk = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            vmkry__kbgg = bodo.utils.conversion.coerce_to_array(index)
            oag__nigmv = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                vmkry__kbgg, arr), index, lptr__mpgyk)
            return oag__nigmv.groupby(' ')['']
        return impl_index
    sjcaq__dkepg = by
    if isinstance(by, SeriesType):
        sjcaq__dkepg = by.data
    if isinstance(sjcaq__dkepg, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    uxa__vie = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        vmkry__kbgg = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        oag__nigmv = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            vmkry__kbgg, arr), index, uxa__vie)
        return oag__nigmv.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    xgi__cfu = dict(verify_integrity=verify_integrity)
    svn__bqe = dict(verify_integrity=False)
    check_unsupported_args('Series.append', xgi__cfu, svn__bqe,
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
            upc__rjybn = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            ckdiz__dqde = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(ckdiz__dqde, A, upc__rjybn, False)
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ckdiz__dqde = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    xgi__cfu = dict(interpolation=interpolation)
    svn__bqe = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            ckdiz__dqde = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
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
        nsdtt__mwbt = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(nsdtt__mwbt, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    xgi__cfu = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    svn__bqe = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', xgi__cfu, svn__bqe,
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
        fckje__qzity = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        fckje__qzity = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    iuxtm__gjbi = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {fckje__qzity}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    uxdu__eao = dict()
    exec(iuxtm__gjbi, {'bodo': bodo, 'numba': numba}, uxdu__eao)
    tro__jtlua = uxdu__eao['impl']
    return tro__jtlua


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        fckje__qzity = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        fckje__qzity = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    iuxtm__gjbi = 'def impl(S,\n'
    iuxtm__gjbi += '     value=None,\n'
    iuxtm__gjbi += '    method=None,\n'
    iuxtm__gjbi += '    axis=None,\n'
    iuxtm__gjbi += '    inplace=False,\n'
    iuxtm__gjbi += '    limit=None,\n'
    iuxtm__gjbi += '   downcast=None,\n'
    iuxtm__gjbi += '):\n'
    iuxtm__gjbi += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    iuxtm__gjbi += '    n = len(in_arr)\n'
    iuxtm__gjbi += f'    out_arr = {fckje__qzity}(n, -1)\n'
    iuxtm__gjbi += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    iuxtm__gjbi += '        s = in_arr[j]\n'
    iuxtm__gjbi += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    iuxtm__gjbi += '            s = value\n'
    iuxtm__gjbi += '        out_arr[j] = s\n'
    iuxtm__gjbi += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    uxdu__eao = dict()
    exec(iuxtm__gjbi, {'bodo': bodo, 'numba': numba}, uxdu__eao)
    tro__jtlua = uxdu__eao['impl']
    return tro__jtlua


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
    ouzp__zzjih = bodo.hiframes.pd_series_ext.get_series_data(value)
    for cvohh__cxj in numba.parfors.parfor.internal_prange(len(adynm__hsui)):
        s = adynm__hsui[cvohh__cxj]
        if bodo.libs.array_kernels.isna(adynm__hsui, cvohh__cxj
            ) and not bodo.libs.array_kernels.isna(ouzp__zzjih, cvohh__cxj):
            s = ouzp__zzjih[cvohh__cxj]
        adynm__hsui[cvohh__cxj] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
    for cvohh__cxj in numba.parfors.parfor.internal_prange(len(adynm__hsui)):
        s = adynm__hsui[cvohh__cxj]
        if bodo.libs.array_kernels.isna(adynm__hsui, cvohh__cxj):
            s = value
        adynm__hsui[cvohh__cxj] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    ouzp__zzjih = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(adynm__hsui)
    ckdiz__dqde = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for rmxi__cikc in numba.parfors.parfor.internal_prange(n):
        s = adynm__hsui[rmxi__cikc]
        if bodo.libs.array_kernels.isna(adynm__hsui, rmxi__cikc
            ) and not bodo.libs.array_kernels.isna(ouzp__zzjih, rmxi__cikc):
            s = ouzp__zzjih[rmxi__cikc]
        ckdiz__dqde[rmxi__cikc] = s
        if bodo.libs.array_kernels.isna(adynm__hsui, rmxi__cikc
            ) and bodo.libs.array_kernels.isna(ouzp__zzjih, rmxi__cikc):
            bodo.libs.array_kernels.setna(ckdiz__dqde, rmxi__cikc)
    return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    ouzp__zzjih = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(adynm__hsui)
    ckdiz__dqde = bodo.utils.utils.alloc_type(n, adynm__hsui.dtype, (-1,))
    for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
        s = adynm__hsui[cvohh__cxj]
        if bodo.libs.array_kernels.isna(adynm__hsui, cvohh__cxj
            ) and not bodo.libs.array_kernels.isna(ouzp__zzjih, cvohh__cxj):
            s = ouzp__zzjih[cvohh__cxj]
        ckdiz__dqde[cvohh__cxj] = s
    return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    xgi__cfu = dict(limit=limit, downcast=downcast)
    svn__bqe = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')
    sepe__iibfd = not is_overload_none(value)
    znlh__tkye = not is_overload_none(method)
    if sepe__iibfd and znlh__tkye:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not sepe__iibfd and not znlh__tkye:
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
    if znlh__tkye:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        kge__kgbu = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(kge__kgbu)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(kge__kgbu)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    mzav__ufg = element_type(S.data)
    dqggq__kazyl = None
    if sepe__iibfd:
        dqggq__kazyl = element_type(types.unliteral(value))
    if dqggq__kazyl and not can_replace(mzav__ufg, dqggq__kazyl):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {dqggq__kazyl} with series type {mzav__ufg}'
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
        afex__fupw = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ouzp__zzjih = bodo.hiframes.pd_series_ext.get_series_data(value
                    )
                n = len(adynm__hsui)
                ckdiz__dqde = bodo.utils.utils.alloc_type(n, afex__fupw, (-1,))
                for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(adynm__hsui, cvohh__cxj
                        ) and bodo.libs.array_kernels.isna(ouzp__zzjih,
                        cvohh__cxj):
                        bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                        continue
                    if bodo.libs.array_kernels.isna(adynm__hsui, cvohh__cxj):
                        ckdiz__dqde[cvohh__cxj
                            ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                            ouzp__zzjih[cvohh__cxj])
                        continue
                    ckdiz__dqde[cvohh__cxj
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        adynm__hsui[cvohh__cxj])
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                    index, name)
            return fillna_series_impl
        if znlh__tkye:
            rxf__qdgm = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(mzav__ufg, (types.Integer, types.Float)
                ) and mzav__ufg not in rxf__qdgm:
                raise BodoError(
                    f"Series.fillna(): series of type {mzav__ufg} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ckdiz__dqde = bodo.libs.array_kernels.ffill_bfill_arr(
                    adynm__hsui, method)
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_tz_naive_timestamp(value)
            adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(adynm__hsui)
            ckdiz__dqde = bodo.utils.utils.alloc_type(n, afex__fupw, (-1,))
            for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    adynm__hsui[cvohh__cxj])
                if bodo.libs.array_kernels.isna(adynm__hsui, cvohh__cxj):
                    s = value
                ckdiz__dqde[cvohh__cxj] = s
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        murz__cptyh = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        xgi__cfu = dict(limit=limit, downcast=downcast)
        svn__bqe = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', xgi__cfu,
            svn__bqe, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        mzav__ufg = element_type(S.data)
        rxf__qdgm = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(mzav__ufg, (types.Integer, types.Float)
            ) and mzav__ufg not in rxf__qdgm:
            raise BodoError(
                f'Series.{overload_name}(): series of type {mzav__ufg} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ckdiz__dqde = bodo.libs.array_kernels.ffill_bfill_arr(adynm__hsui,
                murz__cptyh)
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        bhc__cvz = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(bhc__cvz)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        yngzd__dbnjl = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(yngzd__dbnjl)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        yngzd__dbnjl = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(yngzd__dbnjl)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        yngzd__dbnjl = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(yngzd__dbnjl)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    xgi__cfu = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    pmiak__qthnd = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', xgi__cfu, pmiak__qthnd,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    mzav__ufg = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        lihg__lbb = element_type(to_replace.key_type)
        dqggq__kazyl = element_type(to_replace.value_type)
    else:
        lihg__lbb = element_type(to_replace)
        dqggq__kazyl = element_type(value)
    zze__dwd = None
    if mzav__ufg != types.unliteral(lihg__lbb):
        if bodo.utils.typing.equality_always_false(mzav__ufg, types.
            unliteral(lihg__lbb)
            ) or not bodo.utils.typing.types_equality_exists(mzav__ufg,
            lihg__lbb):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(mzav__ufg, (types.Float, types.Integer)
            ) or mzav__ufg == np.bool_:
            zze__dwd = mzav__ufg
    if not can_replace(mzav__ufg, types.unliteral(dqggq__kazyl)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    ucjrn__abl = to_str_arr_if_dict_array(S.data)
    if isinstance(ucjrn__abl, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(adynm__hsui.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(adynm__hsui)
        ckdiz__dqde = bodo.utils.utils.alloc_type(n, ucjrn__abl, (-1,))
        vvp__zzqc = build_replace_dict(to_replace, value, zze__dwd)
        for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(adynm__hsui, cvohh__cxj):
                bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                continue
            s = adynm__hsui[cvohh__cxj]
            if s in vvp__zzqc:
                s = vvp__zzqc[s]
            ckdiz__dqde[cvohh__cxj] = s
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    zxvtv__iyz = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    kzp__frwuh = is_iterable_type(to_replace)
    zcjyp__fndn = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    alca__cgc = is_iterable_type(value)
    if zxvtv__iyz and zcjyp__fndn:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vvp__zzqc = {}
                vvp__zzqc[key_dtype_conv(to_replace)] = value
                return vvp__zzqc
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vvp__zzqc = {}
            vvp__zzqc[to_replace] = value
            return vvp__zzqc
        return impl
    if kzp__frwuh and zcjyp__fndn:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vvp__zzqc = {}
                for uar__mqfk in to_replace:
                    vvp__zzqc[key_dtype_conv(uar__mqfk)] = value
                return vvp__zzqc
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vvp__zzqc = {}
            for uar__mqfk in to_replace:
                vvp__zzqc[uar__mqfk] = value
            return vvp__zzqc
        return impl
    if kzp__frwuh and alca__cgc:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vvp__zzqc = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for cvohh__cxj in range(len(to_replace)):
                    vvp__zzqc[key_dtype_conv(to_replace[cvohh__cxj])] = value[
                        cvohh__cxj]
                return vvp__zzqc
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vvp__zzqc = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for cvohh__cxj in range(len(to_replace)):
                vvp__zzqc[to_replace[cvohh__cxj]] = value[cvohh__cxj]
            return vvp__zzqc
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
            ckdiz__dqde = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ckdiz__dqde = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    xgi__cfu = dict(ignore_index=ignore_index)
    ytz__lccee = dict(ignore_index=False)
    check_unsupported_args('Series.explode', xgi__cfu, ytz__lccee,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        bocv__ixvg = bodo.utils.conversion.index_to_array(index)
        ckdiz__dqde, oxw__vvpr = bodo.libs.array_kernels.explode(arr,
            bocv__ixvg)
        iiwej__plfsl = bodo.utils.conversion.index_from_array(oxw__vvpr)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
            iiwej__plfsl, name)
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
            vyg__ycwk = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                vyg__ycwk[cvohh__cxj] = np.argmax(a[cvohh__cxj])
            return vyg__ycwk
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            brzj__jta = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                brzj__jta[cvohh__cxj] = np.argmin(a[cvohh__cxj])
            return brzj__jta
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType) and isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            ykyoj__fqoej = bodo.utils.conversion.ndarray_if_nullable_arr(bodo
                .hiframes.pd_series_ext.get_series_data(b))
            return np.dot(arr, ykyoj__fqoej)
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
    xgi__cfu = dict(axis=axis, inplace=inplace, how=how)
    qmdfb__iks = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', xgi__cfu, qmdfb__iks,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mnzdn__jte = S.notna().values
            bocv__ixvg = bodo.utils.conversion.extract_index_array(S)
            iiwej__plfsl = bodo.utils.conversion.convert_to_index(bocv__ixvg
                [mnzdn__jte])
            ckdiz__dqde = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(adynm__hsui))
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                iiwej__plfsl, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            bocv__ixvg = bodo.utils.conversion.extract_index_array(S)
            mnzdn__jte = S.notna().values
            iiwej__plfsl = bodo.utils.conversion.convert_to_index(bocv__ixvg
                [mnzdn__jte])
            ckdiz__dqde = adynm__hsui[mnzdn__jte]
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                iiwej__plfsl, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    xgi__cfu = dict(freq=freq, axis=axis)
    svn__bqe = dict(freq=None, axis=0)
    check_unsupported_args('Series.shift', xgi__cfu, svn__bqe, package_name
        ='pandas', module_name='Series')
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
        ckdiz__dqde = bodo.hiframes.rolling.shift(arr, periods, False,
            fill_value)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    xgi__cfu = dict(fill_method=fill_method, limit=limit, freq=freq)
    svn__bqe = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', xgi__cfu, svn__bqe,
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
        ckdiz__dqde = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
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
            pucu__bsdx = 'None'
        else:
            pucu__bsdx = 'other'
        iuxtm__gjbi = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            iuxtm__gjbi += '  cond = ~cond\n'
        iuxtm__gjbi += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        iuxtm__gjbi += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        iuxtm__gjbi += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        iuxtm__gjbi += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {pucu__bsdx})
"""
        iuxtm__gjbi += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        liszm__hwjm = {}
        exec(iuxtm__gjbi, {'bodo': bodo, 'np': np}, liszm__hwjm)
        impl = liszm__hwjm['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        bhc__cvz = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(bhc__cvz)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    xgi__cfu = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    svn__bqe = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', xgi__cfu, svn__bqe, package_name
        ='pandas', module_name=module_name)
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
    ylj__rcd = is_overload_constant_nan(other)
    if not (is_default or ylj__rcd or is_scalar_type(other) or isinstance(
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
            urbg__dlioy = arr.dtype.elem_type
        else:
            urbg__dlioy = arr.dtype
        if is_iterable_type(other):
            brafa__uxuyl = other.dtype
        elif ylj__rcd:
            brafa__uxuyl = types.float64
        else:
            brafa__uxuyl = types.unliteral(other)
        if not ylj__rcd and not is_common_scalar_dtype([urbg__dlioy,
            brafa__uxuyl]):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        xgi__cfu = dict(level=level, axis=axis)
        svn__bqe = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), xgi__cfu,
            svn__bqe, package_name='pandas', module_name='Series')
        wvr__tjmc = other == string_type or is_overload_constant_str(other)
        fvyw__akbo = is_iterable_type(other) and other.dtype == string_type
        rcv__hvx = S.dtype == string_type and (op == operator.add and (
            wvr__tjmc or fvyw__akbo) or op == operator.mul and isinstance(
            other, types.Integer))
        mxv__vxsfl = S.dtype == bodo.timedelta64ns
        fnni__kqoq = S.dtype == bodo.datetime64ns
        ynahd__vzo = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        acuxs__auhdj = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype ==
            pd_timestamp_tz_naive_type or other.dtype == bodo.datetime64ns)
        pteha__hqwye = mxv__vxsfl and (ynahd__vzo or acuxs__auhdj
            ) or fnni__kqoq and ynahd__vzo
        pteha__hqwye = pteha__hqwye and op == operator.add
        if not (isinstance(S.dtype, types.Number) or rcv__hvx or pteha__hqwye):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        ldhxo__nmbu = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            ucjrn__abl = ldhxo__nmbu.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and ucjrn__abl == types.Array(types.bool_, 1, 'C'):
                ucjrn__abl = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_tz_naive_timestamp(other
                    )
                n = len(arr)
                ckdiz__dqde = bodo.utils.utils.alloc_type(n, ucjrn__abl, (-1,))
                for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                    nuwi__xeino = bodo.libs.array_kernels.isna(arr, cvohh__cxj)
                    if nuwi__xeino:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(ckdiz__dqde,
                                cvohh__cxj)
                        else:
                            ckdiz__dqde[cvohh__cxj] = op(fill_value, other)
                    else:
                        ckdiz__dqde[cvohh__cxj] = op(arr[cvohh__cxj], other)
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        ucjrn__abl = ldhxo__nmbu.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and ucjrn__abl == types.Array(types.bool_, 1, 'C'):
            ucjrn__abl = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            iiwlv__sdanc = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            ckdiz__dqde = bodo.utils.utils.alloc_type(n, ucjrn__abl, (-1,))
            for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                nuwi__xeino = bodo.libs.array_kernels.isna(arr, cvohh__cxj)
                tyk__lvi = bodo.libs.array_kernels.isna(iiwlv__sdanc,
                    cvohh__cxj)
                if nuwi__xeino and tyk__lvi:
                    bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                elif nuwi__xeino:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                    else:
                        ckdiz__dqde[cvohh__cxj] = op(fill_value,
                            iiwlv__sdanc[cvohh__cxj])
                elif tyk__lvi:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                    else:
                        ckdiz__dqde[cvohh__cxj] = op(arr[cvohh__cxj],
                            fill_value)
                else:
                    ckdiz__dqde[cvohh__cxj] = op(arr[cvohh__cxj],
                        iiwlv__sdanc[cvohh__cxj])
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
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
        ldhxo__nmbu = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            ucjrn__abl = ldhxo__nmbu.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and ucjrn__abl == types.Array(types.bool_, 1, 'C'):
                ucjrn__abl = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                ckdiz__dqde = bodo.utils.utils.alloc_type(n, ucjrn__abl, None)
                for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                    nuwi__xeino = bodo.libs.array_kernels.isna(arr, cvohh__cxj)
                    if nuwi__xeino:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(ckdiz__dqde,
                                cvohh__cxj)
                        else:
                            ckdiz__dqde[cvohh__cxj] = op(other, fill_value)
                    else:
                        ckdiz__dqde[cvohh__cxj] = op(other, arr[cvohh__cxj])
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        ucjrn__abl = ldhxo__nmbu.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and ucjrn__abl == types.Array(types.bool_, 1, 'C'):
            ucjrn__abl = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            iiwlv__sdanc = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            ckdiz__dqde = bodo.utils.utils.alloc_type(n, ucjrn__abl, None)
            for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                nuwi__xeino = bodo.libs.array_kernels.isna(arr, cvohh__cxj)
                tyk__lvi = bodo.libs.array_kernels.isna(iiwlv__sdanc,
                    cvohh__cxj)
                ckdiz__dqde[cvohh__cxj] = op(iiwlv__sdanc[cvohh__cxj], arr[
                    cvohh__cxj])
                if nuwi__xeino and tyk__lvi:
                    bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                elif nuwi__xeino:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                    else:
                        ckdiz__dqde[cvohh__cxj] = op(iiwlv__sdanc[
                            cvohh__cxj], fill_value)
                elif tyk__lvi:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                    else:
                        ckdiz__dqde[cvohh__cxj] = op(fill_value, arr[
                            cvohh__cxj])
                else:
                    ckdiz__dqde[cvohh__cxj] = op(iiwlv__sdanc[cvohh__cxj],
                        arr[cvohh__cxj])
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
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
    for op, qesu__lgw in explicit_binop_funcs_two_ways.items():
        for name in qesu__lgw:
            bhc__cvz = create_explicit_binary_op_overload(op)
            qmt__hmrd = create_explicit_binary_reverse_op_overload(op)
            eqcu__mah = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(bhc__cvz)
            overload_method(SeriesType, eqcu__mah, no_unliteral=True)(qmt__hmrd
                )
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        bhc__cvz = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(bhc__cvz)
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
                fbex__pnov = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                ckdiz__dqde = dt64_arr_sub(arr, fbex__pnov)
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
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
                ckdiz__dqde = np.empty(n, np.dtype('datetime64[ns]'))
                for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, cvohh__cxj):
                        bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                        continue
                    hsf__ngfio = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[cvohh__cxj]))
                    cngt__wckr = op(hsf__ngfio, rhs)
                    ckdiz__dqde[cvohh__cxj
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        cngt__wckr.value)
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
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
                    fbex__pnov = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    ckdiz__dqde = op(arr, bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(fbex__pnov))
                    return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                fbex__pnov = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                ckdiz__dqde = op(arr, fbex__pnov)
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    uflk__zxel = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    ckdiz__dqde = op(bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(uflk__zxel), arr)
                    return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                uflk__zxel = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                ckdiz__dqde = op(uflk__zxel, arr)
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        bhc__cvz = create_binary_op_overload(op)
        overload(op)(bhc__cvz)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    lffvj__vzlx = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, lffvj__vzlx)
        for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, cvohh__cxj
                ) or bodo.libs.array_kernels.isna(arg2, cvohh__cxj):
                bodo.libs.array_kernels.setna(S, cvohh__cxj)
                continue
            S[cvohh__cxj
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                cvohh__cxj]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[cvohh__cxj]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                iiwlv__sdanc = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, iiwlv__sdanc)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        bhc__cvz = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(bhc__cvz)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ckdiz__dqde = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        bhc__cvz = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(bhc__cvz)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    ckdiz__dqde = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
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
                    iiwlv__sdanc = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    ckdiz__dqde = ufunc(arr, iiwlv__sdanc)
                    return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    iiwlv__sdanc = bodo.hiframes.pd_series_ext.get_series_data(
                        S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    ckdiz__dqde = ufunc(arr, iiwlv__sdanc)
                    return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        bhc__cvz = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(bhc__cvz)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        bwoj__bptdw = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        vhlcw__mqhw = np.arange(n),
        bodo.libs.timsort.sort(bwoj__bptdw, 0, n, vhlcw__mqhw)
        return vhlcw__mqhw[0]
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
        dufj__nym = get_overload_const_str(downcast)
        if dufj__nym in ('integer', 'signed'):
            out_dtype = types.int64
        elif dufj__nym == 'unsigned':
            out_dtype = types.uint64
        else:
            assert dufj__nym == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            adynm__hsui = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ckdiz__dqde = pd.to_numeric(adynm__hsui, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if arg_a == bodo.dict_str_arr_type:
        return (lambda arg_a, errors='raise', downcast=None: bodo.libs.
            dict_arr_ext.dict_arr_to_numeric(arg_a, errors, downcast))
    glcd__ylw = types.Array(types.float64, 1, 'C'
        ) if out_dtype == types.float64 else IntegerArrayType(types.int64)

    def to_numeric_impl(arg_a, errors='raise', downcast=None):
        numba.parfors.parfor.init_prange()
        n = len(arg_a)
        tclv__imyvw = bodo.utils.utils.alloc_type(n, glcd__ylw, (-1,))
        for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg_a, cvohh__cxj):
                bodo.libs.array_kernels.setna(tclv__imyvw, cvohh__cxj)
            else:
                bodo.libs.str_arr_ext.str_arr_item_to_numeric(tclv__imyvw,
                    cvohh__cxj, arg_a, cvohh__cxj)
        return tclv__imyvw
    return to_numeric_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        yuks__vfcn = if_series_to_array_type(args[0])
        if isinstance(yuks__vfcn, types.Array) and isinstance(yuks__vfcn.
            dtype, types.Integer):
            yuks__vfcn = types.Array(types.float64, 1, 'C')
        return yuks__vfcn(*args)


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
    wgsvc__mdid = bodo.utils.utils.is_array_typ(x, True)
    bbqp__txv = bodo.utils.utils.is_array_typ(y, True)
    iuxtm__gjbi = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        iuxtm__gjbi += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if wgsvc__mdid and not bodo.utils.utils.is_array_typ(x, False):
        iuxtm__gjbi += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if bbqp__txv and not bodo.utils.utils.is_array_typ(y, False):
        iuxtm__gjbi += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    iuxtm__gjbi += '  n = len(condition)\n'
    nfr__yahp = x.dtype if wgsvc__mdid else types.unliteral(x)
    kwja__prvo = y.dtype if bbqp__txv else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        nfr__yahp = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        kwja__prvo = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    ebcwt__qjisc = get_data(x)
    ftl__vaoao = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(vhlcw__mqhw) for
        vhlcw__mqhw in [ebcwt__qjisc, ftl__vaoao])
    if ftl__vaoao == types.none:
        if isinstance(nfr__yahp, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif ebcwt__qjisc == ftl__vaoao and not is_nullable:
        out_dtype = dtype_to_array_type(nfr__yahp)
    elif nfr__yahp == string_type or kwja__prvo == string_type:
        out_dtype = bodo.string_array_type
    elif ebcwt__qjisc == bytes_type or (wgsvc__mdid and nfr__yahp == bytes_type
        ) and (ftl__vaoao == bytes_type or bbqp__txv and kwja__prvo ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(nfr__yahp, bodo.PDCategoricalDtype):
        out_dtype = None
    elif nfr__yahp in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(nfr__yahp, 1, 'C')
    elif kwja__prvo in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(kwja__prvo, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(nfr__yahp), numba.np.numpy_support.
            as_dtype(kwja__prvo)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(nfr__yahp, bodo.PDCategoricalDtype):
        ikp__jpa = 'x'
    else:
        ikp__jpa = 'out_dtype'
    iuxtm__gjbi += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {ikp__jpa}, (-1,))\n')
    if isinstance(nfr__yahp, bodo.PDCategoricalDtype):
        iuxtm__gjbi += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        iuxtm__gjbi += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    iuxtm__gjbi += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    iuxtm__gjbi += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if wgsvc__mdid:
        iuxtm__gjbi += '      if bodo.libs.array_kernels.isna(x, j):\n'
        iuxtm__gjbi += '        setna(out_arr, j)\n'
        iuxtm__gjbi += '        continue\n'
    if isinstance(nfr__yahp, bodo.PDCategoricalDtype):
        iuxtm__gjbi += '      out_codes[j] = x_codes[j]\n'
    else:
        iuxtm__gjbi += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('x[j]' if wgsvc__mdid else 'x'))
    iuxtm__gjbi += '    else:\n'
    if bbqp__txv:
        iuxtm__gjbi += '      if bodo.libs.array_kernels.isna(y, j):\n'
        iuxtm__gjbi += '        setna(out_arr, j)\n'
        iuxtm__gjbi += '        continue\n'
    if ftl__vaoao == types.none:
        if isinstance(nfr__yahp, bodo.PDCategoricalDtype):
            iuxtm__gjbi += '      out_codes[j] = -1\n'
        else:
            iuxtm__gjbi += '      setna(out_arr, j)\n'
    else:
        iuxtm__gjbi += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('y[j]' if bbqp__txv else 'y'))
    iuxtm__gjbi += '  return out_arr\n'
    liszm__hwjm = {}
    exec(iuxtm__gjbi, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, liszm__hwjm)
    rvflv__hvya = liszm__hwjm['_impl']
    return rvflv__hvya


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
        ycquq__tvdsl = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(ycquq__tvdsl, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(ycquq__tvdsl):
            zyk__wqs = ycquq__tvdsl.data.dtype
        else:
            zyk__wqs = ycquq__tvdsl.dtype
        if isinstance(zyk__wqs, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        npje__vdi = ycquq__tvdsl
    else:
        zwkb__cmfk = []
        for ycquq__tvdsl in choicelist:
            if not bodo.utils.utils.is_array_typ(ycquq__tvdsl, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(ycquq__tvdsl):
                zyk__wqs = ycquq__tvdsl.data.dtype
            else:
                zyk__wqs = ycquq__tvdsl.dtype
            if isinstance(zyk__wqs, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            zwkb__cmfk.append(zyk__wqs)
        if not is_common_scalar_dtype(zwkb__cmfk):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        npje__vdi = choicelist[0]
    if is_series_type(npje__vdi):
        npje__vdi = npje__vdi.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, npje__vdi.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(npje__vdi, types.Array) or isinstance(npje__vdi,
        BooleanArrayType) or isinstance(npje__vdi, IntegerArrayType) or
        isinstance(npje__vdi, FloatingArrayType) or bodo.utils.utils.
        is_array_typ(npje__vdi, False) and npje__vdi.dtype in [bodo.
        string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {npje__vdi} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    ymr__blpcm = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        lld__eitiy = choicelist.dtype
    else:
        jrjmb__ocrzh = False
        zwkb__cmfk = []
        for ycquq__tvdsl in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                ycquq__tvdsl, 'numpy.select()')
            if is_nullable_type(ycquq__tvdsl):
                jrjmb__ocrzh = True
            if is_series_type(ycquq__tvdsl):
                zyk__wqs = ycquq__tvdsl.data.dtype
            else:
                zyk__wqs = ycquq__tvdsl.dtype
            if isinstance(zyk__wqs, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            zwkb__cmfk.append(zyk__wqs)
        rpdv__bkkod, aoe__nct = get_common_scalar_dtype(zwkb__cmfk)
        if not aoe__nct:
            raise BodoError('Internal error in overload_np_select')
        bte__jvycl = dtype_to_array_type(rpdv__bkkod)
        if jrjmb__ocrzh:
            bte__jvycl = to_nullable_type(bte__jvycl)
        lld__eitiy = bte__jvycl
    if isinstance(lld__eitiy, SeriesType):
        lld__eitiy = lld__eitiy.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        dismt__rmve = True
    else:
        dismt__rmve = False
    nvr__ock = False
    eux__dqdk = False
    if dismt__rmve:
        if isinstance(lld__eitiy.dtype, types.Number):
            pass
        elif lld__eitiy.dtype == types.bool_:
            eux__dqdk = True
        else:
            nvr__ock = True
            lld__eitiy = to_nullable_type(lld__eitiy)
    elif default == types.none or is_overload_constant_nan(default):
        nvr__ock = True
        lld__eitiy = to_nullable_type(lld__eitiy)
    iuxtm__gjbi = 'def np_select_impl(condlist, choicelist, default=0):\n'
    iuxtm__gjbi += '  if len(condlist) != len(choicelist):\n'
    iuxtm__gjbi += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    iuxtm__gjbi += '  output_len = len(choicelist[0])\n'
    iuxtm__gjbi += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    iuxtm__gjbi += '  for i in range(output_len):\n'
    if nvr__ock:
        iuxtm__gjbi += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif eux__dqdk:
        iuxtm__gjbi += '    out[i] = False\n'
    else:
        iuxtm__gjbi += '    out[i] = default\n'
    if ymr__blpcm:
        iuxtm__gjbi += '  for i in range(len(condlist) - 1, -1, -1):\n'
        iuxtm__gjbi += '    cond = condlist[i]\n'
        iuxtm__gjbi += '    choice = choicelist[i]\n'
        iuxtm__gjbi += '    out = np.where(cond, choice, out)\n'
    else:
        for cvohh__cxj in range(len(choicelist) - 1, -1, -1):
            iuxtm__gjbi += f'  cond = condlist[{cvohh__cxj}]\n'
            iuxtm__gjbi += f'  choice = choicelist[{cvohh__cxj}]\n'
            iuxtm__gjbi += f'  out = np.where(cond, choice, out)\n'
    iuxtm__gjbi += '  return out'
    liszm__hwjm = dict()
    exec(iuxtm__gjbi, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': lld__eitiy}, liszm__hwjm)
    impl = liszm__hwjm['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ckdiz__dqde = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    xgi__cfu = dict(subset=subset, keep=keep, inplace=inplace)
    svn__bqe = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', xgi__cfu, svn__bqe,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        hainm__ktfof = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (hainm__ktfof,), bocv__ixvg = bodo.libs.array_kernels.drop_duplicates((
            hainm__ktfof,), index, 1)
        index = bodo.utils.conversion.index_from_array(bocv__ixvg)
        return bodo.hiframes.pd_series_ext.init_series(hainm__ktfof, index,
            name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    srtyp__xkuyu = element_type(S.data)
    if not is_common_scalar_dtype([srtyp__xkuyu, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([srtyp__xkuyu, right]):
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
        ckdiz__dqde = bodo.libs.bool_arr_ext.alloc_bool_array(n)
        for cvohh__cxj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arr, cvohh__cxj):
                bodo.libs.array_kernels.setna(ckdiz__dqde, cvohh__cxj)
                continue
            zemnu__epf = bodo.utils.conversion.box_if_dt64(arr[cvohh__cxj])
            if inclusive == 'both':
                ckdiz__dqde[cvohh__cxj
                    ] = zemnu__epf <= right and zemnu__epf >= left
            else:
                ckdiz__dqde[cvohh__cxj
                    ] = zemnu__epf < right and zemnu__epf > left
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde, index, name
            )
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    xgi__cfu = dict(axis=axis)
    svn__bqe = dict(axis=None)
    check_unsupported_args('Series.repeat', xgi__cfu, svn__bqe,
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
            bocv__ixvg = bodo.utils.conversion.index_to_array(index)
            ckdiz__dqde = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            oxw__vvpr = bodo.libs.array_kernels.repeat_kernel(bocv__ixvg,
                repeats)
            iiwej__plfsl = bodo.utils.conversion.index_from_array(oxw__vvpr)
            return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
                iiwej__plfsl, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        bocv__ixvg = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        ckdiz__dqde = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        oxw__vvpr = bodo.libs.array_kernels.repeat_kernel(bocv__ixvg, repeats)
        iiwej__plfsl = bodo.utils.conversion.index_from_array(oxw__vvpr)
        return bodo.hiframes.pd_series_ext.init_series(ckdiz__dqde,
            iiwej__plfsl, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        vhlcw__mqhw = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(vhlcw__mqhw)
        uvba__yow = {}
        for cvohh__cxj in range(n):
            zemnu__epf = bodo.utils.conversion.box_if_dt64(vhlcw__mqhw[
                cvohh__cxj])
            uvba__yow[index[cvohh__cxj]] = zemnu__epf
        return uvba__yow
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    kge__kgbu = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            zbk__blci = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(kge__kgbu)
    elif is_literal_type(name):
        zbk__blci = get_literal_value(name)
    else:
        raise_bodo_error(kge__kgbu)
    zbk__blci = 0 if zbk__blci is None else zbk__blci
    ilmyg__tulpf = ColNamesMetaType((zbk__blci,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            ilmyg__tulpf)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
