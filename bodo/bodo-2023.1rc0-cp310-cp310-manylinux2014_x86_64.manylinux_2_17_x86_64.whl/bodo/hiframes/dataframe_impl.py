"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_getattr, models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import DatetimeIndexType, RangeIndexType, StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_tz_naive_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_castable_arr_dtype, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, parse_dtype, raise_bodo_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        uic__uan = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({uic__uan})\n')
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    cki__pusxl = 'def impl(df):\n'
    if df.has_runtime_cols:
        cki__pusxl += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        lzdr__imlw = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        cki__pusxl += f'  return {lzdr__imlw}'
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    dwga__fimb = len(df.columns)
    navdi__mijo = set(i for i in range(dwga__fimb) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in navdi__mijo else '') for i in
        range(dwga__fimb))
    cki__pusxl = 'def f(df):\n'.format()
    cki__pusxl += '    return np.stack(({},), 1)\n'.format(data_args)
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo, 'np': np}, ctum__lrkh)
    mjptj__fkmdo = ctum__lrkh['f']
    return mjptj__fkmdo


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    nlpxw__tmcy = {'dtype': dtype, 'na_value': na_value}
    bruml__fyn = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', nlpxw__tmcy, bruml__fyn,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            wfupz__jkitg = bodo.hiframes.table.compute_num_runtime_columns(t)
            return wfupz__jkitg * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@lower_getattr(DataFrameType, 'shape')
def lower_dataframe_shape(context, builder, typ, val):
    impl = overload_dataframe_shape(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            wfupz__jkitg = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), wfupz__jkitg
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), ncols)


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    cki__pusxl = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    vhte__sxiy = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    cki__pusxl += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{vhte__sxiy}), {index}, None)
"""
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if type(dtype) in bodo.libs.int_arr_ext.pd_int_dtype_classes:
        return dtype.name
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if isinstance(dtype, types.PyObject) or dtype in (object, 'object'):
        return "'object'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True, _bodo_object_typeref=None):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    nlpxw__tmcy = {'errors': errors}
    bruml__fyn = {'errors': 'raise'}
    check_unsupported_args('df.astype', nlpxw__tmcy, bruml__fyn,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    if not is_overload_bool(copy):
        raise BodoError("DataFrame.astype(): 'copy' must be a boolean value")
    extra_globals = None
    header = """def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True, _bodo_object_typeref=None):
"""
    if df.is_table_format:
        extra_globals = {}
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        yxww__mizpu = []
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        lwarr__ykm = _bodo_object_typeref.instance_type
        assert isinstance(lwarr__ykm, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        if df.is_table_format:
            for i, name in enumerate(df.columns):
                if name in lwarr__ykm.column_index:
                    idx = lwarr__ykm.column_index[name]
                    arr_typ = lwarr__ykm.data[idx]
                else:
                    arr_typ = df.data[i]
                yxww__mizpu.append(arr_typ)
        else:
            extra_globals = {}
            lpey__eobwc = {}
            for i, name in enumerate(lwarr__ykm.columns):
                arr_typ = lwarr__ykm.data[i]
                extra_globals[f'_bodo_schema{i}'] = get_castable_arr_dtype(
                    arr_typ)
                lpey__eobwc[name] = f'_bodo_schema{i}'
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {lpey__eobwc[ytzv__mwl]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if ytzv__mwl in lpey__eobwc else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, ytzv__mwl in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        eufqo__cbicn = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        if df.is_table_format:
            eufqo__cbicn = {name: dtype_to_array_type(parse_dtype(dtype)) for
                name, dtype in eufqo__cbicn.items()}
            for i, name in enumerate(df.columns):
                if name in eufqo__cbicn:
                    arr_typ = eufqo__cbicn[name]
                else:
                    arr_typ = df.data[i]
                yxww__mizpu.append(arr_typ)
        else:
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(eufqo__cbicn[ytzv__mwl])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if ytzv__mwl in eufqo__cbicn else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, ytzv__mwl in enumerate(df.columns))
    elif df.is_table_format:
        arr_typ = dtype_to_array_type(parse_dtype(dtype))
        yxww__mizpu = [arr_typ] * len(df.columns)
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    if df.is_table_format:
        hkye__giyuh = bodo.TableType(tuple(yxww__mizpu))
        extra_globals['out_table_typ'] = hkye__giyuh
        data_args = (
            'bodo.utils.table_utils.table_astype(table, out_table_typ, copy, _bodo_nan_to_str)'
            )
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    header = 'def impl(df, deep=True):\n'
    extra_globals = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        xdw__qqrow = types.none
        extra_globals = {'output_arr_typ': xdw__qqrow}
        if is_overload_false(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if deep else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        nezx__acx = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                nezx__acx.append(arr + '.copy()')
            elif is_overload_false(deep):
                nezx__acx.append(arr)
            else:
                nezx__acx.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(nezx__acx)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    nlpxw__tmcy = {'index': index, 'level': level, 'errors': errors}
    bruml__fyn = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', nlpxw__tmcy, bruml__fyn,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        ehflr__hnn = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        ehflr__hnn = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    ctn__lip = tuple([ehflr__hnn.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    drpjp__ies = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        drpjp__ies = df.copy(columns=ctn__lip)
        xdw__qqrow = types.none
        extra_globals = {'output_arr_typ': xdw__qqrow}
        if is_overload_false(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if copy else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        nezx__acx = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                nezx__acx.append(arr + '.copy()')
            elif is_overload_false(copy):
                nezx__acx.append(arr)
            else:
                nezx__acx.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(nezx__acx)
    return _gen_init_df(header, ctn__lip, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    wpm__zhtbj = not is_overload_none(items)
    wfdp__okmde = not is_overload_none(like)
    vzp__hzaf = not is_overload_none(regex)
    ftgb__hcv = wpm__zhtbj ^ wfdp__okmde ^ vzp__hzaf
    hwqk__xafr = not (wpm__zhtbj or wfdp__okmde or vzp__hzaf)
    if hwqk__xafr:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not ftgb__hcv:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        xuyrh__nntwf = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        xuyrh__nntwf = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert xuyrh__nntwf in {0, 1}
    cki__pusxl = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if xuyrh__nntwf == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if xuyrh__nntwf == 1:
        cagr__yiqw = []
        cae__ihr = []
        ynrle__vxl = []
        if wpm__zhtbj:
            if is_overload_constant_list(items):
                vdd__svd = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if wfdp__okmde:
            if is_overload_constant_str(like):
                rnkuc__eehd = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if vzp__hzaf:
            if is_overload_constant_str(regex):
                vzob__onnh = get_overload_const_str(regex)
                xfbs__ewq = re.compile(vzob__onnh)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, ytzv__mwl in enumerate(df.columns):
            if not is_overload_none(items
                ) and ytzv__mwl in vdd__svd or not is_overload_none(like
                ) and rnkuc__eehd in str(ytzv__mwl) or not is_overload_none(
                regex) and xfbs__ewq.search(str(ytzv__mwl)):
                cae__ihr.append(ytzv__mwl)
                ynrle__vxl.append(i)
        for i in ynrle__vxl:
            var_name = f'data_{i}'
            cagr__yiqw.append(var_name)
            cki__pusxl += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(cagr__yiqw)
        return _gen_init_df(cki__pusxl, cae__ihr, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    drpjp__ies = None
    if df.is_table_format:
        xdw__qqrow = types.Array(types.bool_, 1, 'C')
        drpjp__ies = DataFrameType(tuple([xdw__qqrow] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': xdw__qqrow}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    spr__cxh = is_overload_none(include)
    fgsj__mld = is_overload_none(exclude)
    qyk__lqp = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if spr__cxh and fgsj__mld:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not spr__cxh:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            spfp__zoqx = [dtype_to_array_type(parse_dtype(elem, qyk__lqp)) for
                elem in include]
        elif is_legal_input(include):
            spfp__zoqx = [dtype_to_array_type(parse_dtype(include, qyk__lqp))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        spfp__zoqx = get_nullable_and_non_nullable_types(spfp__zoqx)
        aevta__qdem = tuple(ytzv__mwl for i, ytzv__mwl in enumerate(df.
            columns) if df.data[i] in spfp__zoqx)
    else:
        aevta__qdem = df.columns
    if not fgsj__mld:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            bjak__wdtey = [dtype_to_array_type(parse_dtype(elem, qyk__lqp)) for
                elem in exclude]
        elif is_legal_input(exclude):
            bjak__wdtey = [dtype_to_array_type(parse_dtype(exclude, qyk__lqp))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        bjak__wdtey = get_nullable_and_non_nullable_types(bjak__wdtey)
        aevta__qdem = tuple(ytzv__mwl for ytzv__mwl in aevta__qdem if df.
            data[df.column_index[ytzv__mwl]] not in bjak__wdtey)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ytzv__mwl]})'
         for ytzv__mwl in aevta__qdem)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, aevta__qdem, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    drpjp__ies = None
    if df.is_table_format:
        xdw__qqrow = types.Array(types.bool_, 1, 'C')
        drpjp__ies = DataFrameType(tuple([xdw__qqrow] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': xdw__qqrow}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'~bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


def overload_dataframe_head(df, n=5):
    if df.is_table_format:
        data_args = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[:n]')
    else:
        data_args = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]'
             for i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    if df.is_table_format:
        data_args = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[m:]')
    else:
        data_args = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]'
             for i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    fleeq__acdi = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in fleeq__acdi:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.first()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    fleeq__acdi = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in fleeq__acdi:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.last()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.isin()')
    cki__pusxl = 'def impl(df, values):\n'
    ohief__wabum = {}
    lbc__eqr = False
    if isinstance(values, DataFrameType):
        lbc__eqr = True
        for i, ytzv__mwl in enumerate(df.columns):
            if ytzv__mwl in values.column_index:
                uquab__pcsa = 'val{}'.format(i)
                cki__pusxl += f"""  {uquab__pcsa} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[ytzv__mwl]})
"""
                ohief__wabum[ytzv__mwl] = uquab__pcsa
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        ohief__wabum = {ytzv__mwl: 'values' for ytzv__mwl in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        uquab__pcsa = 'data{}'.format(i)
        cki__pusxl += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(uquab__pcsa, i))
        data.append(uquab__pcsa)
    jkr__awa = ['out{}'.format(i) for i in range(len(df.columns))]
    wvmz__qjtua = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    gcbpb__ntahg = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    qot__qkmj = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, xii__mwvr) in enumerate(zip(df.columns, data)):
        if cname in ohief__wabum:
            qqagq__gndnj = ohief__wabum[cname]
            if lbc__eqr:
                cki__pusxl += wvmz__qjtua.format(xii__mwvr, qqagq__gndnj,
                    jkr__awa[i])
            else:
                cki__pusxl += gcbpb__ntahg.format(xii__mwvr, qqagq__gndnj,
                    jkr__awa[i])
        else:
            cki__pusxl += qot__qkmj.format(jkr__awa[i])
    return _gen_init_df(cki__pusxl, df.columns, ','.join(jkr__awa))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    dwga__fimb = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(dwga__fimb))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    iqogr__tkpp = [ytzv__mwl for ytzv__mwl, aoixi__dehnv in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(aoixi__dehnv
        .dtype)]
    assert len(iqogr__tkpp) != 0
    fqjnr__wgrx = ''
    if not any(aoixi__dehnv == types.float64 for aoixi__dehnv in df.data):
        fqjnr__wgrx = '.astype(np.float64)'
    uxzwa__gwnlh = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[ytzv__mwl], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[ytzv__mwl]], IntegerArrayType) or
        df.data[df.column_index[ytzv__mwl]] == boolean_array else '') for
        ytzv__mwl in iqogr__tkpp)
    dvb__ria = 'np.stack(({},), 1){}'.format(uxzwa__gwnlh, fqjnr__wgrx)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        iqogr__tkpp)))
    index = f'{generate_col_to_index_func_text(iqogr__tkpp)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(dvb__ria)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, iqogr__tkpp, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    jrsj__xblo = dict(ddof=ddof)
    rbxwc__shl = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    wtr__noewx = '1' if is_overload_none(min_periods) else 'min_periods'
    iqogr__tkpp = [ytzv__mwl for ytzv__mwl, aoixi__dehnv in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(aoixi__dehnv
        .dtype)]
    if len(iqogr__tkpp) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    fqjnr__wgrx = ''
    if not any(aoixi__dehnv == types.float64 for aoixi__dehnv in df.data):
        fqjnr__wgrx = '.astype(np.float64)'
    uxzwa__gwnlh = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[ytzv__mwl], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[ytzv__mwl]], IntegerArrayType) or
        df.data[df.column_index[ytzv__mwl]] == boolean_array else '') for
        ytzv__mwl in iqogr__tkpp)
    dvb__ria = 'np.stack(({},), 1){}'.format(uxzwa__gwnlh, fqjnr__wgrx)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        iqogr__tkpp)))
    index = f'pd.Index({iqogr__tkpp})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(dvb__ria)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        wtr__noewx)
    return _gen_init_df(header, iqogr__tkpp, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    jrsj__xblo = dict(axis=axis, level=level, numeric_only=numeric_only)
    rbxwc__shl = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    cki__pusxl = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    cki__pusxl += '  data = np.array([{}])\n'.format(data_args)
    lzdr__imlw = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    cki__pusxl += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {lzdr__imlw})\n'
        )
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo, 'np': np}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    jrsj__xblo = dict(axis=axis)
    rbxwc__shl = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    cki__pusxl = 'def impl(df, axis=0, dropna=True):\n'
    cki__pusxl += '  data = np.asarray(({},))\n'.format(data_args)
    lzdr__imlw = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    cki__pusxl += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {lzdr__imlw})\n'
        )
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo, 'np': np}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    jrsj__xblo = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    rbxwc__shl = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    jrsj__xblo = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    rbxwc__shl = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    jrsj__xblo = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    rbxwc__shl = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    jrsj__xblo = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    rbxwc__shl = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    jrsj__xblo = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    rbxwc__shl = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    jrsj__xblo = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    rbxwc__shl = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    jrsj__xblo = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    rbxwc__shl = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    jrsj__xblo = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    rbxwc__shl = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    jrsj__xblo = dict(numeric_only=numeric_only, interpolation=interpolation)
    rbxwc__shl = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    jrsj__xblo = dict(axis=axis, skipna=skipna)
    rbxwc__shl = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for bbj__ccp in df.data:
        if not (bodo.utils.utils.is_np_array_typ(bbj__ccp) and (bbj__ccp.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            bbj__ccp.dtype, (types.Number, types.Boolean))) or isinstance(
            bbj__ccp, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo.
            CategoricalArrayType)) or bbj__ccp in [bodo.boolean_array, bodo
            .datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {bbj__ccp} not supported.'
                )
        if isinstance(bbj__ccp, bodo.CategoricalArrayType
            ) and not bbj__ccp.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    jrsj__xblo = dict(axis=axis, skipna=skipna)
    rbxwc__shl = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for bbj__ccp in df.data:
        if not (bodo.utils.utils.is_np_array_typ(bbj__ccp) and (bbj__ccp.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            bbj__ccp.dtype, (types.Number, types.Boolean))) or isinstance(
            bbj__ccp, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo.
            CategoricalArrayType)) or bbj__ccp in [bodo.boolean_array, bodo
            .datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {bbj__ccp} not supported.'
                )
        if isinstance(bbj__ccp, bodo.CategoricalArrayType
            ) and not bbj__ccp.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        iqogr__tkpp = tuple(ytzv__mwl for ytzv__mwl, aoixi__dehnv in zip(df
            .columns, df.data) if bodo.utils.typing.
            _is_pandas_numeric_dtype(aoixi__dehnv.dtype))
        out_colnames = iqogr__tkpp
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            hsucl__jenpq = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[ytzv__mwl]].dtype) for ytzv__mwl in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(hsucl__jenpq, []))
    except NotImplementedError as gdcv__yywhf:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    uixj__wwuq = ''
    if func_name in ('sum', 'prod'):
        uixj__wwuq = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    cki__pusxl = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, uixj__wwuq))
    if func_name == 'quantile':
        cki__pusxl = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        cki__pusxl = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        cki__pusxl += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        cki__pusxl += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    yhy__dms = ''
    if func_name in ('min', 'max'):
        yhy__dms = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        yhy__dms = ', dtype=np.float32'
    oqge__uowk = f'bodo.libs.array_ops.array_op_{func_name}'
    nnt__supkj = ''
    if func_name in ['sum', 'prod']:
        nnt__supkj = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        nnt__supkj = 'index'
    elif func_name == 'quantile':
        nnt__supkj = 'q'
    elif func_name in ['std', 'var']:
        nnt__supkj = 'True, ddof'
    elif func_name == 'median':
        nnt__supkj = 'True'
    data_args = ', '.join(
        f'{oqge__uowk}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ytzv__mwl]}), {nnt__supkj})'
         for ytzv__mwl in out_colnames)
    cki__pusxl = ''
    if func_name in ('idxmax', 'idxmin'):
        cki__pusxl += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        cki__pusxl += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        cki__pusxl += '  data = np.asarray(({},){})\n'.format(data_args,
            yhy__dms)
    cki__pusxl += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return cki__pusxl


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    yrwyy__arten = [df_type.column_index[ytzv__mwl] for ytzv__mwl in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in yrwyy__arten)
    avs__hdmwt = '\n        '.join(f'row[{i}] = arr_{yrwyy__arten[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    nnl__xjyq = f'len(arr_{yrwyy__arten[0]})'
    tavb__zhv = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum': 'np.nansum',
        'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in tavb__zhv:
        sgrd__sznm = tavb__zhv[func_name]
        hainl__dxz = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        cki__pusxl = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {nnl__xjyq}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{hainl__dxz})
    for i in numba.parfors.parfor.internal_prange(n):
        {avs__hdmwt}
        A[i] = {sgrd__sznm}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return cki__pusxl
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    jrsj__xblo = dict(fill_method=fill_method, limit=limit, freq=freq)
    rbxwc__shl = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.pct_change()')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    jrsj__xblo = dict(axis=axis, skipna=skipna)
    rbxwc__shl = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumprod()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    jrsj__xblo = dict(skipna=skipna)
    rbxwc__shl = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumsum()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, (IntegerArrayType, FloatingArrayType)
        ) or isinstance(data, types.Array) and isinstance(data.dtype, types
        .Number) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    jrsj__xblo = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    rbxwc__shl = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    iqogr__tkpp = [ytzv__mwl for ytzv__mwl, aoixi__dehnv in zip(df.columns,
        df.data) if _is_describe_type(aoixi__dehnv)]
    if len(iqogr__tkpp) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    enaf__rhfj = sum(df.data[df.column_index[ytzv__mwl]].dtype == bodo.
        datetime64ns for ytzv__mwl in iqogr__tkpp)

    def _get_describe(col_ind):
        hrnf__vhth = df.data[col_ind].dtype == bodo.datetime64ns
        if enaf__rhfj and enaf__rhfj != len(iqogr__tkpp):
            if hrnf__vhth:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for ytzv__mwl in iqogr__tkpp:
        col_ind = df.column_index[ytzv__mwl]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[ytzv__mwl]) for
        ytzv__mwl in iqogr__tkpp)
    pec__beq = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if enaf__rhfj == len(iqogr__tkpp):
        pec__beq = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif enaf__rhfj:
        pec__beq = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({pec__beq})'
    return _gen_init_df(header, iqogr__tkpp, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    jrsj__xblo = dict(axis=axis, convert=convert, is_copy=is_copy)
    rbxwc__shl = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    jrsj__xblo = dict(freq=freq, axis=axis)
    rbxwc__shl = dict(freq=None, axis=0)
    check_unsupported_args('DataFrame.shift', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for uzvg__cdfah in df.data:
        if not is_supported_shift_array_type(uzvg__cdfah):
            raise BodoError(
                f'Dataframe.shift() column input type {uzvg__cdfah.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False, fill_value)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    jrsj__xblo = dict(axis=axis)
    rbxwc__shl = dict(axis=0)
    check_unsupported_args('DataFrame.diff', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for uzvg__cdfah in df.data:
        if not (isinstance(uzvg__cdfah, types.Array) and (isinstance(
            uzvg__cdfah.dtype, types.Number) or uzvg__cdfah.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {uzvg__cdfah.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'explode', inline='always', no_unliteral=True)
def overload_dataframe_explode(df, column, ignore_index=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.explode()')
    cijrs__dnv = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(cijrs__dnv)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        qjkg__ukaad = get_overload_const_list(column)
    else:
        qjkg__ukaad = [get_literal_value(column)]
    abu__uute = [df.column_index[ytzv__mwl] for ytzv__mwl in qjkg__ukaad]
    for i in abu__uute:
        if not isinstance(df.data[i], ArrayItemArrayType) and df.data[i
            ].dtype != string_array_split_view_type:
            raise BodoError(
                f'DataFrame.explode(): columns must have array-like entries')
    n = len(df.columns)
    header = 'def impl(df, column, ignore_index=False):\n'
    header += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    header += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    for i in range(n):
        header += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    header += (
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{abu__uute[0]})\n'
        )
    for i in range(n):
        if i in abu__uute:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.explode_no_index(data{i}, counts)\n'
                )
        else:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.repeat_kernel(data{i}, counts)\n'
                )
    header += (
        '  new_index = bodo.libs.array_kernels.repeat_kernel(index_arr, counts)\n'
        )
    data_args = ', '.join(f'out_data{i}' for i in range(n))
    index = 'bodo.utils.conversion.convert_to_index(new_index)'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    nlpxw__tmcy = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    bruml__fyn = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', nlpxw__tmcy, bruml__fyn,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    columns = tuple(ytzv__mwl for ytzv__mwl in df.columns if ytzv__mwl !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    nlpxw__tmcy = {'inplace': inplace}
    bruml__fyn = {'inplace': False}
    check_unsupported_args('query', nlpxw__tmcy, bruml__fyn, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        zoejj__qeifp = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[zoejj__qeifp]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    nlpxw__tmcy = {'subset': subset, 'keep': keep}
    bruml__fyn = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', nlpxw__tmcy, bruml__fyn,
        package_name='pandas', module_name='DataFrame')
    dwga__fimb = len(df.columns)
    cki__pusxl = "def impl(df, subset=None, keep='first'):\n"
    for i in range(dwga__fimb):
        cki__pusxl += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    ktm__doy = ', '.join(f'data_{i}' for i in range(dwga__fimb))
    ktm__doy += ',' if dwga__fimb == 1 else ''
    cki__pusxl += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({ktm__doy}))\n')
    cki__pusxl += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    cki__pusxl += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    nlpxw__tmcy = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    bruml__fyn = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    xjthr__dgn = []
    if is_overload_constant_list(subset):
        xjthr__dgn = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        xjthr__dgn = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        xjthr__dgn = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    tbrr__yhta = []
    for col_name in xjthr__dgn:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        tbrr__yhta.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', nlpxw__tmcy,
        bruml__fyn, package_name='pandas', module_name='DataFrame')
    tduk__wpi = []
    if tbrr__yhta:
        for sfgz__utmgq in tbrr__yhta:
            if isinstance(df.data[sfgz__utmgq], bodo.MapArrayType):
                tduk__wpi.append(df.columns[sfgz__utmgq])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                tduk__wpi.append(col_name)
    if tduk__wpi:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {tduk__wpi} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    dwga__fimb = len(df.columns)
    ioc__mxdi = ['data_{}'.format(i) for i in tbrr__yhta]
    xssqg__reqc = ['data_{}'.format(i) for i in range(dwga__fimb) if i not in
        tbrr__yhta]
    if ioc__mxdi:
        abfup__dkygk = len(ioc__mxdi)
    else:
        abfup__dkygk = dwga__fimb
    aod__fde = ', '.join(ioc__mxdi + xssqg__reqc)
    data_args = ', '.join('data_{}'.format(i) for i in range(dwga__fimb))
    cki__pusxl = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(dwga__fimb):
        cki__pusxl += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    cki__pusxl += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(aod__fde, index, abfup__dkygk))
    cki__pusxl += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(cki__pusxl, df.columns, data_args, 'index')


def create_dataframe_mask_where_overload(func_name):

    def overload_dataframe_mask_where(df, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
            f'DataFrame.{func_name}()')
        _validate_arguments_mask_where(f'DataFrame.{func_name}', df, cond,
            other, inplace, axis, level, errors, try_cast)
        header = """def impl(df, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False):
"""
        if func_name == 'mask':
            header += '  cond = ~cond\n'
        gen_all_false = [False]
        if cond.ndim == 1:
            cond_str = lambda i, _: 'cond'
        elif cond.ndim == 2:
            if isinstance(cond, DataFrameType):

                def cond_str(i, gen_all_false):
                    if df.columns[i] in cond.column_index:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {cond.column_index[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            pdcxh__zfkss = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                pdcxh__zfkss = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                pdcxh__zfkss = lambda i: f'other[:,{i}]'
        dwga__fimb = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {pdcxh__zfkss(i)})'
             for i in range(dwga__fimb))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        byt__vuiev = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(byt__vuiev
            )


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    jrsj__xblo = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    rbxwc__shl = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        (cond.ndim == 1 or cond.ndim == 2) and cond.dtype == types.bool_
        ) and not (isinstance(cond, DataFrameType) and cond.ndim == 2 and
        all(cond.data[i].dtype == types.bool_ for i in range(len(df.columns)))
        ):
        raise BodoError(
            f"{func_name}(): 'cond' argument must be a DataFrame, Series, 1- or 2-dimensional array of booleans"
            )
    dwga__fimb = len(df.columns)
    if hasattr(other, 'ndim') and (other.ndim != 1 or other.ndim != 2):
        if other.ndim == 2:
            if not isinstance(other, (DataFrameType, types.Array)):
                raise BodoError(
                    f"{func_name}(): 'other', if 2-dimensional, must be a DataFrame or array."
                    )
        elif other.ndim != 1:
            raise BodoError(
                f"{func_name}(): 'other' must be either 1 or 2-dimensional")
    if isinstance(other, DataFrameType):
        for i in range(dwga__fimb):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], other.data[other.
                    column_index[df.columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(dwga__fimb):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other.data)
    else:
        for i in range(dwga__fimb):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    tkzn__bucaa = ColNamesMetaType(tuple(columns))
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    cki__pusxl = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, __col_name_meta_value_gen_init_df)
"""
    ctum__lrkh = {}
    dcdg__fqccq = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba,
        '__col_name_meta_value_gen_init_df': tkzn__bucaa}
    dcdg__fqccq.update(extra_globals)
    exec(cki__pusxl, dcdg__fqccq, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        sfdw__xhox = pd.Index(lhs.columns)
        cgmky__bgxvw = pd.Index(rhs.columns)
        aci__uln, pmb__qjxyj, leg__chmxl = sfdw__xhox.join(cgmky__bgxvw,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(aci__uln), pmb__qjxyj, leg__chmxl
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        mrm__dzehk = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        dpjd__iei = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, mrm__dzehk)
        check_runtime_cols_unsupported(rhs, mrm__dzehk)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                aci__uln, pmb__qjxyj, leg__chmxl = _get_binop_columns(lhs, rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {pxa__oujc}) {mrm__dzehk}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {wos__czyr})'
                     if pxa__oujc != -1 and wos__czyr != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for pxa__oujc, wos__czyr in zip(pmb__qjxyj, leg__chmxl))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, aci__uln, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            hzapp__tli = []
            yre__rvt = []
            if op in dpjd__iei:
                for i, sjq__zjur in enumerate(lhs.data):
                    if is_common_scalar_dtype([sjq__zjur.dtype, rhs]):
                        hzapp__tli.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {mrm__dzehk} rhs'
                            )
                    else:
                        yugs__dlvrd = f'arr{i}'
                        yre__rvt.append(yugs__dlvrd)
                        hzapp__tli.append(yugs__dlvrd)
                data_args = ', '.join(hzapp__tli)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {mrm__dzehk} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(yre__rvt) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {yugs__dlvrd} = np.empty(n, dtype=np.bool_)\n' for
                    yugs__dlvrd in yre__rvt)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(yugs__dlvrd, 
                    op == operator.ne) for yugs__dlvrd in yre__rvt)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            hzapp__tli = []
            yre__rvt = []
            if op in dpjd__iei:
                for i, sjq__zjur in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, sjq__zjur.dtype]):
                        hzapp__tli.append(
                            f'lhs {mrm__dzehk} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        yugs__dlvrd = f'arr{i}'
                        yre__rvt.append(yugs__dlvrd)
                        hzapp__tli.append(yugs__dlvrd)
                data_args = ', '.join(hzapp__tli)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, mrm__dzehk) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(yre__rvt) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(yugs__dlvrd) for yugs__dlvrd in yre__rvt)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(yugs__dlvrd, 
                    op == operator.ne) for yugs__dlvrd in yre__rvt)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        byt__vuiev = create_binary_op_overload(op)
        overload(op)(byt__vuiev)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        mrm__dzehk = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, mrm__dzehk)
        check_runtime_cols_unsupported(right, mrm__dzehk)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                aci__uln, _, leg__chmxl = _get_binop_columns(left, right, True)
                cki__pusxl = 'def impl(left, right):\n'
                for i, wos__czyr in enumerate(leg__chmxl):
                    if wos__czyr == -1:
                        cki__pusxl += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    cki__pusxl += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    cki__pusxl += f"""  df_arr{i} {mrm__dzehk} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {wos__czyr})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    aci__uln)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(cki__pusxl, aci__uln, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            cki__pusxl = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                cki__pusxl += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                cki__pusxl += '  df_arr{0} {1} right\n'.format(i, mrm__dzehk)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(cki__pusxl, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        byt__vuiev = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(byt__vuiev)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            mrm__dzehk = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, mrm__dzehk)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, mrm__dzehk) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        byt__vuiev = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(byt__vuiev)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            fmvy__yjytq = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                fmvy__yjytq[i] = bodo.libs.array_kernels.isna(obj, i)
            return fmvy__yjytq
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            fmvy__yjytq = np.empty(n, np.bool_)
            for i in range(n):
                fmvy__yjytq[i] = pd.isna(obj[i])
            return fmvy__yjytq
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if isinstance(obj, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, (DataFrameType, SeriesType)):
        return lambda obj: obj.notna()
    if isinstance(obj, (types.List, types.UniTuple)) or is_array_typ(obj,
        include_index_series=True):
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    nlpxw__tmcy = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    bruml__fyn = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', nlpxw__tmcy, bruml__fyn, package_name
        ='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    nfqoz__yxsj = str(expr_node)
    return nfqoz__yxsj.startswith('(left.') or nfqoz__yxsj.startswith('(right.'
        )


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    dvy__xnm = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (dvy__xnm,))
    dlq__hgd = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        tjyjc__tug = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        ofvn__lgypz = {('NOT_NA', dlq__hgd(sjq__zjur)): sjq__zjur for
            sjq__zjur in null_set}
        xsnc__khtba, _, _ = _parse_query_expr(tjyjc__tug, env, [], [], None,
            join_cleaned_cols=ofvn__lgypz)
        cjz__ejkv = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            zrkv__uufy = pd.core.computation.ops.BinOp('&', xsnc__khtba,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = cjz__ejkv
        return zrkv__uufy

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                xbxq__yebn = set()
                bvlbj__izt = set()
                ngow__irfs = _insert_NA_cond_body(expr_node.lhs, xbxq__yebn)
                gxia__hmnv = _insert_NA_cond_body(expr_node.rhs, bvlbj__izt)
                cnn__ldf = xbxq__yebn.intersection(bvlbj__izt)
                xbxq__yebn.difference_update(cnn__ldf)
                bvlbj__izt.difference_update(cnn__ldf)
                null_set.update(cnn__ldf)
                expr_node.lhs = append_null_checks(ngow__irfs, xbxq__yebn)
                expr_node.rhs = append_null_checks(gxia__hmnv, bvlbj__izt)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            spqe__ice = expr_node.name
            yjed__chxn, col_name = spqe__ice.split('.')
            if yjed__chxn == 'left':
                dpks__tymo = left_columns
                data = left_data
            else:
                dpks__tymo = right_columns
                data = right_data
            lifvl__ufs = data[dpks__tymo.index(col_name)]
            if bodo.utils.typing.is_nullable(lifvl__ufs):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    gqkkj__eid = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        zcx__vpkvf = str(expr_node.lhs)
        fhrr__bdda = str(expr_node.rhs)
        if zcx__vpkvf.startswith('(left.') and fhrr__bdda.startswith('(left.'
            ) or zcx__vpkvf.startswith('(right.') and fhrr__bdda.startswith(
            '(right.'):
            return [], [], expr_node
        left_on = [zcx__vpkvf.split('.')[1][:-1]]
        right_on = [fhrr__bdda.split('.')[1][:-1]]
        if zcx__vpkvf.startswith('(right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        zcyg__ldr, mydfb__zqryg, sdk__apr = _extract_equal_conds(expr_node.lhs)
        kjw__gasij, plry__rue, lene__qacpz = _extract_equal_conds(expr_node.rhs
            )
        left_on = zcyg__ldr + kjw__gasij
        right_on = mydfb__zqryg + plry__rue
        if sdk__apr is None:
            return left_on, right_on, lene__qacpz
        if lene__qacpz is None:
            return left_on, right_on, sdk__apr
        expr_node.lhs = sdk__apr
        expr_node.rhs = lene__qacpz
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    dvy__xnm = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (dvy__xnm,))
    ehflr__hnn = dict()
    dlq__hgd = pd.core.computation.parsing.clean_column_name
    for name, cnr__lsc in (('left', left_columns), ('right', right_columns)):
        for sjq__zjur in cnr__lsc:
            qad__sjnwl = dlq__hgd(sjq__zjur)
            mtb__xkyxk = name, qad__sjnwl
            if mtb__xkyxk in ehflr__hnn:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{sjq__zjur}' and '{ehflr__hnn[qad__sjnwl]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            ehflr__hnn[mtb__xkyxk] = sjq__zjur
    guls__fem, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=ehflr__hnn)
    left_on, right_on, hoznj__ktk = _extract_equal_conds(guls__fem.terms)
    return left_on, right_on, _insert_NA_cond(hoznj__ktk, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    jrsj__xblo = dict(sort=sort, copy=copy, validate=validate)
    rbxwc__shl = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    pgrg__sby = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    gytng__garpv = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in pgrg__sby and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, sljqk__pxdnh = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if sljqk__pxdnh is None:
                    gytng__garpv = ''
                else:
                    gytng__garpv = str(sljqk__pxdnh)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = pgrg__sby
        right_keys = pgrg__sby
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    rifw__pbe = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        zfx__lxg = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        zfx__lxg = list(get_overload_const_list(suffixes))
    suffix_x = zfx__lxg[0]
    suffix_y = zfx__lxg[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    cki__pusxl = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    cki__pusxl += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    cki__pusxl += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    cki__pusxl += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, rifw__pbe, gytng__garpv))
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo}, ctum__lrkh)
    _impl = ctum__lrkh['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, FloatingArrayType, DecimalArrayType,
        IntervalArrayType, bodo.DatetimeArrayType, TimeArrayType)
    ifn__ajumz = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    fjj__ykr = {get_overload_const_str(jgx__jdd) for jgx__jdd in (left_on,
        right_on, on) if is_overload_constant_str(jgx__jdd)}
    for df in (left, right):
        for i, sjq__zjur in enumerate(df.data):
            if not isinstance(sjq__zjur, valid_dataframe_column_types
                ) and sjq__zjur not in ifn__ajumz:
                raise BodoError(
                    f'{name_func}(): use of column with {type(sjq__zjur)} in merge unsupported'
                    )
            if df.columns[i] in fjj__ykr and isinstance(sjq__zjur, MapArrayType
                ):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        zfx__lxg = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        zfx__lxg = list(get_overload_const_list(suffixes))
    if len(zfx__lxg) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    pgrg__sby = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        szmyh__zyy = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            szmyh__zyy = on_str not in pgrg__sby and ('left.' in on_str or 
                'right.' in on_str)
        if len(pgrg__sby) == 0 and not szmyh__zyy:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner', 'cross'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    aldb__awsbt = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            yfyn__nvxmi = left.index
            hkhgx__pwtx = isinstance(yfyn__nvxmi, StringIndexType)
            exp__wrlg = right.index
            jceba__jhpz = isinstance(exp__wrlg, StringIndexType)
        elif is_overload_true(left_index):
            yfyn__nvxmi = left.index
            hkhgx__pwtx = isinstance(yfyn__nvxmi, StringIndexType)
            exp__wrlg = right.data[right.columns.index(right_keys[0])]
            jceba__jhpz = exp__wrlg.dtype == string_type
        elif is_overload_true(right_index):
            yfyn__nvxmi = left.data[left.columns.index(left_keys[0])]
            hkhgx__pwtx = yfyn__nvxmi.dtype == string_type
            exp__wrlg = right.index
            jceba__jhpz = isinstance(exp__wrlg, StringIndexType)
        if hkhgx__pwtx and jceba__jhpz:
            return
        yfyn__nvxmi = yfyn__nvxmi.dtype
        exp__wrlg = exp__wrlg.dtype
        try:
            ziz__kuca = aldb__awsbt.resolve_function_type(operator.eq, (
                yfyn__nvxmi, exp__wrlg), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=yfyn__nvxmi, rk_dtype=exp__wrlg))
    else:
        for byydn__rwmaz, fajbb__zotas in zip(left_keys, right_keys):
            yfyn__nvxmi = left.data[left.columns.index(byydn__rwmaz)].dtype
            okhis__qcoh = left.data[left.columns.index(byydn__rwmaz)]
            exp__wrlg = right.data[right.columns.index(fajbb__zotas)].dtype
            pxp__tkj = right.data[right.columns.index(fajbb__zotas)]
            if okhis__qcoh == pxp__tkj:
                continue
            qio__aggu = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=byydn__rwmaz, lk_dtype=yfyn__nvxmi, rk=
                fajbb__zotas, rk_dtype=exp__wrlg))
            wyg__hndsp = yfyn__nvxmi == string_type
            cemjy__kov = exp__wrlg == string_type
            if wyg__hndsp ^ cemjy__kov:
                raise_bodo_error(qio__aggu)
            try:
                ziz__kuca = aldb__awsbt.resolve_function_type(operator.eq,
                    (yfyn__nvxmi, exp__wrlg), {})
            except:
                raise_bodo_error(qio__aggu)


def validate_keys(keys, df):
    icv__ive = set(keys).difference(set(df.columns))
    if len(icv__ive) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in icv__ive:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {icv__ive} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    jrsj__xblo = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    rbxwc__shl = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    cki__pusxl = "def _impl(left, other, on=None, how='left',\n"
    cki__pusxl += "    lsuffix='', rsuffix='', sort=False):\n"
    cki__pusxl += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo}, ctum__lrkh)
    _impl = ctum__lrkh['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        yub__atvig = get_overload_const_list(on)
        validate_keys(yub__atvig, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    pgrg__sby = tuple(set(left.columns) & set(other.columns))
    if len(pgrg__sby) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=pgrg__sby))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    pmnq__iat = set(left_keys) & set(right_keys)
    ndgl__mqobn = set(left_columns) & set(right_columns)
    tla__hsbmw = ndgl__mqobn - pmnq__iat
    vuev__oomw = set(left_columns) - ndgl__mqobn
    ung__oinwe = set(right_columns) - ndgl__mqobn
    mdk__ieroe = {}

    def insertOutColumn(col_name):
        if col_name in mdk__ieroe:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        mdk__ieroe[col_name] = 0
    for kejim__lrccm in pmnq__iat:
        insertOutColumn(kejim__lrccm)
    for kejim__lrccm in tla__hsbmw:
        qsq__rhemj = str(kejim__lrccm) + suffix_x
        kaaan__svdoz = str(kejim__lrccm) + suffix_y
        insertOutColumn(qsq__rhemj)
        insertOutColumn(kaaan__svdoz)
    for kejim__lrccm in vuev__oomw:
        insertOutColumn(kejim__lrccm)
    for kejim__lrccm in ung__oinwe:
        insertOutColumn(kejim__lrccm)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    raise BodoError('pandas.merge_asof() not support yet')
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    pgrg__sby = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = pgrg__sby
        right_keys = pgrg__sby
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        zfx__lxg = suffixes
    if is_overload_constant_list(suffixes):
        zfx__lxg = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        zfx__lxg = suffixes.value
    suffix_x = zfx__lxg[0]
    suffix_y = zfx__lxg[1]
    cki__pusxl = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    cki__pusxl += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    cki__pusxl += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    cki__pusxl += "    allow_exact_matches=True, direction='backward'):\n"
    cki__pusxl += '  suffix_x = suffixes[0]\n'
    cki__pusxl += '  suffix_y = suffixes[1]\n'
    cki__pusxl += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo}, ctum__lrkh)
    _impl = ctum__lrkh['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True, _bodo_num_shuffle_keys=-1):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna, _bodo_num_shuffle_keys)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True,
        _bodo_num_shuffle_keys=-1):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna, _bodo_num_shuffle_keys)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna, _num_shuffle_keys):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_bodo_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_bodo_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_bodo_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_bodo_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    if not is_overload_constant_int(_num_shuffle_keys):
        raise_bodo_error(
            f"groupby(): '_num_shuffle_keys' parameter must be a constant integer, not {_num_shuffle_keys}."
            )
    jrsj__xblo = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    gjuh__hzy = dict(sort=False, group_keys=True, squeeze=False, observed=True)
    check_unsupported_args('Dataframe.groupby', jrsj__xblo, gjuh__hzy,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    okhd__ztj = func_name == 'DataFrame.pivot_table'
    if okhd__ztj:
        if is_overload_none(index) or not is_literal_type(index):
            raise_bodo_error(
                f"DataFrame.pivot_table(): 'index' argument is required and must be constant column labels"
                )
    elif not is_overload_none(index) and not is_literal_type(index):
        raise_bodo_error(
            f"{func_name}(): if 'index' argument is provided it must be constant column labels"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise_bodo_error(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise_bodo_error(
            f"{func_name}(): if 'values' argument is provided it must be constant column labels"
            )
    afkv__yzye = get_literal_value(columns)
    if isinstance(afkv__yzye, (list, tuple)):
        if len(afkv__yzye) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {afkv__yzye}"
                )
        afkv__yzye = afkv__yzye[0]
    if afkv__yzye not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {afkv__yzye} not found in DataFrame {df}."
            )
    cykt__oqft = df.column_index[afkv__yzye]
    if is_overload_none(index):
        byxr__ggmh = []
        sgpth__emotw = []
    else:
        sgpth__emotw = get_literal_value(index)
        if not isinstance(sgpth__emotw, (list, tuple)):
            sgpth__emotw = [sgpth__emotw]
        byxr__ggmh = []
        for index in sgpth__emotw:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            byxr__ggmh.append(df.column_index[index])
    if not (all(isinstance(ytzv__mwl, int) for ytzv__mwl in sgpth__emotw) or
        all(isinstance(ytzv__mwl, str) for ytzv__mwl in sgpth__emotw)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        iedl__zmy = []
        zef__nsuaj = []
        aernn__fpnrg = byxr__ggmh + [cykt__oqft]
        for i, ytzv__mwl in enumerate(df.columns):
            if i not in aernn__fpnrg:
                iedl__zmy.append(i)
                zef__nsuaj.append(ytzv__mwl)
    else:
        zef__nsuaj = get_literal_value(values)
        if not isinstance(zef__nsuaj, (list, tuple)):
            zef__nsuaj = [zef__nsuaj]
        iedl__zmy = []
        for val in zef__nsuaj:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            iedl__zmy.append(df.column_index[val])
    lbdc__ymj = set(iedl__zmy) | set(byxr__ggmh) | {cykt__oqft}
    if len(lbdc__ymj) != len(iedl__zmy) + len(byxr__ggmh) + 1:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )

    def check_valid_index_typ(index_column):
        if isinstance(index_column, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType, bodo.
            IntervalArrayType)):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column must have scalar rows"
                )
        if isinstance(index_column, bodo.CategoricalArrayType):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column does not support categorical data"
                )
    if len(byxr__ggmh) == 0:
        index = df.index
        if isinstance(index, MultiIndexType):
            raise BodoError(
                f"{func_name}(): 'index' cannot be None with a DataFrame with a multi-index"
                )
        if not isinstance(index, RangeIndexType):
            check_valid_index_typ(index.data)
        if not is_literal_type(df.index.name_typ):
            raise BodoError(
                f"{func_name}(): If 'index' is None, the name of the DataFrame's Index must be constant at compile-time"
                )
    else:
        for wemgs__ywnn in byxr__ggmh:
            index_column = df.data[wemgs__ywnn]
            check_valid_index_typ(index_column)
    hjsq__kwqd = df.data[cykt__oqft]
    if isinstance(hjsq__kwqd, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(hjsq__kwqd, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for nddsc__vdzh in iedl__zmy:
        pxbyb__tldtw = df.data[nddsc__vdzh]
        if isinstance(pxbyb__tldtw, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or pxbyb__tldtw == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (sgpth__emotw, afkv__yzye, zef__nsuaj, byxr__ggmh, cykt__oqft,
        iedl__zmy)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (sgpth__emotw, afkv__yzye, zef__nsuaj, wemgs__ywnn, cykt__oqft, dcjzx__yio
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(sgpth__emotw) == 0:
        if is_overload_none(data.index.name_typ):
            fwge__nbjpe = None,
        else:
            fwge__nbjpe = get_literal_value(data.index.name_typ),
    else:
        fwge__nbjpe = tuple(sgpth__emotw)
    sgpth__emotw = ColNamesMetaType(fwge__nbjpe)
    zef__nsuaj = ColNamesMetaType(tuple(zef__nsuaj))
    afkv__yzye = ColNamesMetaType((afkv__yzye,))
    cki__pusxl = 'def impl(data, index=None, columns=None, values=None):\n'
    cki__pusxl += "    ev = tracing.Event('df.pivot')\n"
    cki__pusxl += f'    pivot_values = data.iloc[:, {cykt__oqft}].unique()\n'
    cki__pusxl += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(wemgs__ywnn) == 0:
        cki__pusxl += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        cki__pusxl += '        (\n'
        for eehdy__uetdl in wemgs__ywnn:
            cki__pusxl += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {eehdy__uetdl}),
"""
        cki__pusxl += '        ),\n'
    cki__pusxl += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {cykt__oqft}),),
"""
    cki__pusxl += '        (\n'
    for nddsc__vdzh in dcjzx__yio:
        cki__pusxl += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {nddsc__vdzh}),
"""
    cki__pusxl += '        ),\n'
    cki__pusxl += '        pivot_values,\n'
    cki__pusxl += '        index_lit,\n'
    cki__pusxl += '        columns_lit,\n'
    cki__pusxl += '        values_lit,\n'
    cki__pusxl += '    )\n'
    cki__pusxl += '    ev.finalize()\n'
    cki__pusxl += '    return result\n'
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo, 'index_lit': sgpth__emotw,
        'columns_lit': afkv__yzye, 'values_lit': zef__nsuaj, 'tracing':
        tracing}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@overload(pd.pivot_table, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(data, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot_table()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot_table()')
    jrsj__xblo = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    rbxwc__shl = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    (sgpth__emotw, afkv__yzye, zef__nsuaj, wemgs__ywnn, cykt__oqft, dcjzx__yio
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot_table'))
    gnxv__dccyo = sgpth__emotw
    sgpth__emotw = ColNamesMetaType(tuple(sgpth__emotw))
    zef__nsuaj = ColNamesMetaType(tuple(zef__nsuaj))
    pcx__dfsb = afkv__yzye
    afkv__yzye = ColNamesMetaType((afkv__yzye,))
    cki__pusxl = 'def impl(\n'
    cki__pusxl += '    data,\n'
    cki__pusxl += '    values=None,\n'
    cki__pusxl += '    index=None,\n'
    cki__pusxl += '    columns=None,\n'
    cki__pusxl += '    aggfunc="mean",\n'
    cki__pusxl += '    fill_value=None,\n'
    cki__pusxl += '    margins=False,\n'
    cki__pusxl += '    dropna=True,\n'
    cki__pusxl += '    margins_name="All",\n'
    cki__pusxl += '    observed=False,\n'
    cki__pusxl += '    sort=True,\n'
    cki__pusxl += '    _pivot_values=None,\n'
    cki__pusxl += '):\n'
    cki__pusxl += "    ev = tracing.Event('df.pivot_table')\n"
    rngwu__vrm = wemgs__ywnn + [cykt__oqft] + dcjzx__yio
    cki__pusxl += f'    data = data.iloc[:, {rngwu__vrm}]\n'
    boyy__fzkey = gnxv__dccyo + [pcx__dfsb]
    if not is_overload_none(_pivot_values):
        bgx__qevgz = tuple(sorted(_pivot_values.meta))
        _pivot_values = ColNamesMetaType(bgx__qevgz)
        cki__pusxl += '    pivot_values = _pivot_values_arr\n'
        cki__pusxl += (
            f'    data = data[data.iloc[:, {len(wemgs__ywnn)}].isin(pivot_values)]\n'
            )
        if all(isinstance(ytzv__mwl, str) for ytzv__mwl in bgx__qevgz):
            hidqi__lri = pd.array(bgx__qevgz, 'string')
        elif all(isinstance(ytzv__mwl, int) for ytzv__mwl in bgx__qevgz):
            hidqi__lri = np.array(bgx__qevgz, 'int64')
        else:
            raise BodoError(
                f'pivot(): pivot values selcected via pivot JIT argument must all share a common int or string type.'
                )
    else:
        hidqi__lri = None
    kgrux__vbed = is_overload_constant_str(aggfunc) and get_overload_const_str(
        aggfunc) == 'nunique'
    imr__pey = len(boyy__fzkey) if kgrux__vbed else len(gnxv__dccyo)
    cki__pusxl += f"""    data = data.groupby({boyy__fzkey!r}, as_index=False, _bodo_num_shuffle_keys={imr__pey}).agg(aggfunc)
"""
    if is_overload_none(_pivot_values):
        cki__pusxl += (
            f'    pivot_values = data.iloc[:, {len(wemgs__ywnn)}].unique()\n')
    cki__pusxl += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    cki__pusxl += '        (\n'
    for i in range(0, len(wemgs__ywnn)):
        cki__pusxl += (
            f'            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),\n'
            )
    cki__pusxl += '        ),\n'
    cki__pusxl += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(wemgs__ywnn)}),),
"""
    cki__pusxl += '        (\n'
    for i in range(len(wemgs__ywnn) + 1, len(dcjzx__yio) + len(wemgs__ywnn) + 1
        ):
        cki__pusxl += (
            f'            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),\n'
            )
    cki__pusxl += '        ),\n'
    cki__pusxl += '        pivot_values,\n'
    cki__pusxl += '        index_lit,\n'
    cki__pusxl += '        columns_lit,\n'
    cki__pusxl += '        values_lit,\n'
    cki__pusxl += '        check_duplicates=False,\n'
    cki__pusxl += f'        is_already_shuffled={not kgrux__vbed},\n'
    cki__pusxl += '        _constant_pivot_values=_constant_pivot_values,\n'
    cki__pusxl += '    )\n'
    cki__pusxl += '    ev.finalize()\n'
    cki__pusxl += '    return result\n'
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo, 'numba': numba, 'index_lit':
        sgpth__emotw, 'columns_lit': afkv__yzye, 'values_lit': zef__nsuaj,
        '_pivot_values_arr': hidqi__lri, '_constant_pivot_values':
        _pivot_values, 'tracing': tracing}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    jrsj__xblo = dict(col_level=col_level, ignore_index=ignore_index)
    rbxwc__shl = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame.")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal.")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal.")
    if not is_overload_none(var_name) and not (is_literal_type(var_name) and
        (is_scalar_type(var_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'var_name', if specified, must be a literal.")
    if value_name != 'value' and not (is_literal_type(value_name) and (
        is_scalar_type(value_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'value_name', if specified, must be a literal.")
    var_name = get_literal_value(var_name) if not is_overload_none(var_name
        ) else 'variable'
    value_name = get_literal_value(value_name
        ) if value_name != 'value' else 'value'
    smtuj__toxp = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(smtuj__toxp, (list, tuple)):
        smtuj__toxp = [smtuj__toxp]
    for ytzv__mwl in smtuj__toxp:
        if ytzv__mwl not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {ytzv__mwl} not found in {frame}."
                )
    ljpm__sbprt = [frame.column_index[i] for i in smtuj__toxp]
    if is_overload_none(value_vars):
        gsuqm__ywi = []
        udbw__yxn = []
        for i, ytzv__mwl in enumerate(frame.columns):
            if i not in ljpm__sbprt:
                gsuqm__ywi.append(i)
                udbw__yxn.append(ytzv__mwl)
    else:
        udbw__yxn = get_literal_value(value_vars)
        if not isinstance(udbw__yxn, (list, tuple)):
            udbw__yxn = [udbw__yxn]
        udbw__yxn = [v for v in udbw__yxn if v not in smtuj__toxp]
        if not udbw__yxn:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        gsuqm__ywi = []
        for val in udbw__yxn:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            gsuqm__ywi.append(frame.column_index[val])
    for ytzv__mwl in udbw__yxn:
        if ytzv__mwl not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {ytzv__mwl} not found in {frame}."
                )
    if not (all(isinstance(ytzv__mwl, int) for ytzv__mwl in udbw__yxn) or
        all(isinstance(ytzv__mwl, str) for ytzv__mwl in udbw__yxn)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    oxxa__nrup = frame.data[gsuqm__ywi[0]]
    gpng__rwco = [frame.data[i].dtype for i in gsuqm__ywi]
    gsuqm__ywi = np.array(gsuqm__ywi, dtype=np.int64)
    ljpm__sbprt = np.array(ljpm__sbprt, dtype=np.int64)
    _, ffajo__dwif = bodo.utils.typing.get_common_scalar_dtype(gpng__rwco)
    if not ffajo__dwif:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': udbw__yxn, 'val_type': oxxa__nrup}
    header = 'def impl(\n'
    header += '  frame,\n'
    header += '  id_vars=None,\n'
    header += '  value_vars=None,\n'
    header += '  var_name=None,\n'
    header += "  value_name='value',\n"
    header += '  col_level=None,\n'
    header += '  ignore_index=True,\n'
    header += '):\n'
    header += (
        '  dummy_id = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, 0)\n'
        )
    if frame.is_table_format and all(v == oxxa__nrup.dtype for v in gpng__rwco
        ):
        extra_globals['value_idxs'] = bodo.utils.typing.MetaType(tuple(
            gsuqm__ywi))
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(udbw__yxn) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {gsuqm__ywi[0]})
"""
    else:
        krkor__zumo = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in gsuqm__ywi)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({krkor__zumo},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in ljpm__sbprt:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(udbw__yxn)})\n'
            )
    dzzxm__aclb = ', '.join(f'out_id{i}' for i in ljpm__sbprt) + (', ' if 
        len(ljpm__sbprt) > 0 else '')
    data_args = dzzxm__aclb + 'var_col, val_col'
    columns = tuple(smtuj__toxp + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(udbw__yxn)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    raise BodoError(f'pandas.crosstab() not supported yet')
    jrsj__xblo = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    rbxwc__shl = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(index,
        'pandas.crosstab()')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_chunk_bounds=None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    jrsj__xblo = dict(ignore_index=ignore_index, key=key)
    rbxwc__shl = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position, _bodo_chunk_bounds)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_chunk_bounds=None, _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position, _bodo_chunk_bounds)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position, _bodo_chunk_bounds):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_bodo_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    tcsyn__kzar = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        tcsyn__kzar.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        irs__btudu = [get_overload_const_tuple(by)]
    else:
        irs__btudu = get_overload_const_list(by)
    irs__btudu = set((k, '') if (k, '') in tcsyn__kzar else k for k in
        irs__btudu)
    if len(irs__btudu.difference(tcsyn__kzar)) > 0:
        ugun__exw = list(set(get_overload_const_list(by)).difference(
            tcsyn__kzar))
        raise_bodo_error(f'sort_values(): invalid keys {ugun__exw} for by.')
    if not is_overload_none(_bodo_chunk_bounds) and len(irs__btudu) != 1:
        raise_bodo_error(
            f'sort_values(): _bodo_chunk_bounds only supported when there is a single key.'
            )
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        oebt__lyaks = get_overload_const_list(na_position)
        for na_position in oebt__lyaks:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_bodo_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    jrsj__xblo = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    rbxwc__shl = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position, None)
    return _impl


@overload_method(DataFrameType, 'rank', inline='always', no_unliteral=True)
def overload_dataframe_rank(df, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    cki__pusxl = """def impl(df, axis=0, method='average', numeric_only=None, na_option='keep', ascending=True, pct=False):
"""
    dwga__fimb = len(df.columns)
    data_args = ', '.join(
        'bodo.libs.array_kernels.rank(data_{}, method=method, na_option=na_option, ascending=ascending, pct=pct)'
        .format(i) for i in range(dwga__fimb))
    for i in range(dwga__fimb):
        cki__pusxl += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(cki__pusxl, df.columns, data_args, index)


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    jrsj__xblo = dict(limit=limit, downcast=downcast)
    rbxwc__shl = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    ehctx__uyns = not is_overload_none(value)
    qqdbs__dewja = not is_overload_none(method)
    if ehctx__uyns and qqdbs__dewja:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not ehctx__uyns and not qqdbs__dewja:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if ehctx__uyns:
        ufwk__gdfud = 'value=value'
    else:
        ufwk__gdfud = 'method=method'
    data_args = [(
        f"df['{ytzv__mwl}'].fillna({ufwk__gdfud}, inplace=inplace)" if
        isinstance(ytzv__mwl, str) else
        f'df[{ytzv__mwl}].fillna({ufwk__gdfud}, inplace=inplace)') for
        ytzv__mwl in df.columns]
    cki__pusxl = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        cki__pusxl += '  ' + '  \n'.join(data_args) + '\n'
        ctum__lrkh = {}
        exec(cki__pusxl, {}, ctum__lrkh)
        impl = ctum__lrkh['impl']
        return impl
    else:
        return _gen_init_df(cki__pusxl, df.columns, ', '.join(aoixi__dehnv +
            '.values' for aoixi__dehnv in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    jrsj__xblo = dict(col_level=col_level, col_fill=col_fill)
    rbxwc__shl = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    cki__pusxl = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    cki__pusxl += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        xxll__sdt = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            xxll__sdt)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            cki__pusxl += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            whv__zfoqv = ['m_index[{}]'.format(i) for i in range(df.index.
                nlevels)]
            data_args = whv__zfoqv + data_args
        else:
            rpznu__bmjh = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [rpznu__bmjh] + data_args
    return _gen_init_df(cki__pusxl, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    srhx__ptdp = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and srhx__ptdp == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(srhx__ptdp))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        ddvu__dvs = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        zubht__tok = get_overload_const_list(subset)
        ddvu__dvs = []
        for iltk__eptb in zubht__tok:
            if iltk__eptb not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{iltk__eptb}' not in data frame columns {df}"
                    )
            ddvu__dvs.append(df.column_index[iltk__eptb])
    dwga__fimb = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(dwga__fimb))
    cki__pusxl = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(dwga__fimb):
        cki__pusxl += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    cki__pusxl += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in ddvu__dvs)))
    cki__pusxl += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(cki__pusxl, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    jrsj__xblo = dict(index=index, level=level, errors=errors)
    rbxwc__shl = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', jrsj__xblo, rbxwc__shl,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            ivdil__wwsbu = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            ivdil__wwsbu = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            ivdil__wwsbu = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            ivdil__wwsbu = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for ytzv__mwl in ivdil__wwsbu:
        if ytzv__mwl not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(ytzv__mwl, df.columns))
    if len(set(ivdil__wwsbu)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    ctn__lip = tuple(ytzv__mwl for ytzv__mwl in df.columns if ytzv__mwl not in
        ivdil__wwsbu)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[ytzv__mwl], '.copy()' if not inplace else ''
        ) for ytzv__mwl in ctn__lip)
    cki__pusxl = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    cki__pusxl += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(cki__pusxl, ctn__lip, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sample()')
    jrsj__xblo = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    lurhn__uvm = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', jrsj__xblo, lurhn__uvm,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    dwga__fimb = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(dwga__fimb))
    gttwp__onddn = ', '.join('rhs_data_{}'.format(i) for i in range(dwga__fimb)
        )
    cki__pusxl = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    cki__pusxl += '  if (frac == 1 or n == len(df)) and not replace:\n'
    cki__pusxl += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(dwga__fimb):
        cki__pusxl += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    cki__pusxl += '  if frac is None:\n'
    cki__pusxl += '    frac_d = -1.0\n'
    cki__pusxl += '  else:\n'
    cki__pusxl += '    frac_d = frac\n'
    cki__pusxl += '  if n is None:\n'
    cki__pusxl += '    n_i = 0\n'
    cki__pusxl += '  else:\n'
    cki__pusxl += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    cki__pusxl += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({gttwp__onddn},), {index}, n_i, frac_d, replace)
"""
    cki__pusxl += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(cki__pusxl, df.columns,
        data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    nlpxw__tmcy = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    bruml__fyn = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', nlpxw__tmcy, bruml__fyn,
        package_name='pandas', module_name='DataFrame')
    kcsm__nean = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            hhpi__war = kcsm__nean + '\n'
            hhpi__war += 'Index: 0 entries\n'
            hhpi__war += 'Empty DataFrame'
            print(hhpi__war)
        return _info_impl
    else:
        cki__pusxl = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        cki__pusxl += '    ncols = df.shape[1]\n'
        cki__pusxl += f'    lines = "{kcsm__nean}\\n"\n'
        cki__pusxl += f'    lines += "{df.index}: "\n'
        cki__pusxl += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            cki__pusxl += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            cki__pusxl += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            cki__pusxl += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        cki__pusxl += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        cki__pusxl += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        cki__pusxl += '    column_width = max(space, 7)\n'
        cki__pusxl += '    column= "Column"\n'
        cki__pusxl += '    underl= "------"\n'
        cki__pusxl += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        cki__pusxl += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        cki__pusxl += '    mem_size = 0\n'
        cki__pusxl += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        cki__pusxl += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        cki__pusxl += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        jvy__lybu = dict()
        for i in range(len(df.columns)):
            cki__pusxl += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            aab__uqsz = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                aab__uqsz = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                snxex__cuhs = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                aab__uqsz = f'{snxex__cuhs[:-7]}'
            cki__pusxl += f'    col_dtype[{i}] = "{aab__uqsz}"\n'
            if aab__uqsz in jvy__lybu:
                jvy__lybu[aab__uqsz] += 1
            else:
                jvy__lybu[aab__uqsz] = 1
            cki__pusxl += f'    col_name[{i}] = "{df.columns[i]}"\n'
            cki__pusxl += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        cki__pusxl += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        cki__pusxl += '    for i in column_info:\n'
        cki__pusxl += "        lines += f'{i}\\n'\n"
        eroit__qaltd = ', '.join(f'{k}({jvy__lybu[k]})' for k in sorted(
            jvy__lybu))
        cki__pusxl += f"    lines += 'dtypes: {eroit__qaltd}\\n'\n"
        cki__pusxl += '    mem_size += df.index.nbytes\n'
        cki__pusxl += '    total_size = _sizeof_fmt(mem_size)\n'
        cki__pusxl += "    lines += f'memory usage: {total_size}'\n"
        cki__pusxl += '    print(lines)\n'
        ctum__lrkh = {}
        exec(cki__pusxl, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, ctum__lrkh)
        _info_impl = ctum__lrkh['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    cki__pusxl = 'def impl(df, index=True, deep=False):\n'
    hjun__jefto = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    qcbg__nec = is_overload_true(index)
    columns = df.columns
    if qcbg__nec:
        columns = ('Index',) + columns
    if len(columns) == 0:
        ndq__gsp = ()
    elif all(isinstance(ytzv__mwl, int) for ytzv__mwl in columns):
        ndq__gsp = np.array(columns, 'int64')
    elif all(isinstance(ytzv__mwl, str) for ytzv__mwl in columns):
        ndq__gsp = pd.array(columns, 'string')
    else:
        ndq__gsp = columns
    if df.is_table_format and len(df.columns) > 0:
        rtcv__tfuwr = int(qcbg__nec)
        wfupz__jkitg = len(columns)
        cki__pusxl += f'  nbytes_arr = np.empty({wfupz__jkitg}, np.int64)\n'
        cki__pusxl += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        cki__pusxl += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {rtcv__tfuwr})
"""
        if qcbg__nec:
            cki__pusxl += f'  nbytes_arr[0] = {hjun__jefto}\n'
        cki__pusxl += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if qcbg__nec:
            data = f'{hjun__jefto},{data}'
        else:
            vhte__sxiy = ',' if len(columns) == 1 else ''
            data = f'{data}{vhte__sxiy}'
        cki__pusxl += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        ndq__gsp}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    ehyg__diobj = 'read_excel_df{}'.format(next_label())
    setattr(types, ehyg__diobj, df_type)
    ozdr__boqen = False
    if is_overload_constant_list(parse_dates):
        ozdr__boqen = get_overload_const_list(parse_dates)
    psc__wyxy = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    cki__pusxl = f"""
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{ehyg__diobj}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{psc__wyxy}}},
            engine=engine,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates={ozdr__boqen},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    ctum__lrkh = {}
    exec(cki__pusxl, globals(), ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as gdcv__yywhf:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    cki__pusxl = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    cki__pusxl += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    cki__pusxl += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        cki__pusxl += '   fig, ax = plt.subplots()\n'
    else:
        cki__pusxl += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        cki__pusxl += '   fig.set_figwidth(figsize[0])\n'
        cki__pusxl += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        cki__pusxl += '   xlabel = x\n'
    cki__pusxl += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        cki__pusxl += '   ylabel = y\n'
    else:
        cki__pusxl += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        cki__pusxl += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        cki__pusxl += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    cki__pusxl += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            cki__pusxl += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            ius__vxp = get_overload_const_str(x)
            lfiot__ubfyv = df.columns.index(ius__vxp)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if lfiot__ubfyv != i:
                        cki__pusxl += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            cki__pusxl += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        cki__pusxl += '   ax.scatter(df[x], df[y], s=20)\n'
        cki__pusxl += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        cki__pusxl += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        cki__pusxl += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        cki__pusxl += '   ax.legend()\n'
    cki__pusxl += '   return ax\n'
    ctum__lrkh = {}
    exec(cki__pusxl, {'bodo': bodo, 'plt': plt}, ctum__lrkh)
    impl = ctum__lrkh['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for bmctj__eey in df_typ.data:
        if not (isinstance(bmctj__eey, (IntegerArrayType, FloatingArrayType
            )) or isinstance(bmctj__eey.dtype, types.Number) or bmctj__eey.
            dtype in (bodo.datetime64ns, bodo.timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        veet__stqkr = args[0]
        cxias__vke = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        fhbn__pyl = veet__stqkr
        check_runtime_cols_unsupported(veet__stqkr, 'set_df_col()')
        if isinstance(veet__stqkr, DataFrameType):
            index = veet__stqkr.index
            if len(veet__stqkr.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(veet__stqkr.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if is_overload_constant_str(val) or val == types.unicode_type:
                val = bodo.dict_str_arr_type
            elif not is_array_typ(val):
                val = dtype_to_array_type(val)
            if cxias__vke in veet__stqkr.columns:
                ctn__lip = veet__stqkr.columns
                zgdjv__tngv = veet__stqkr.columns.index(cxias__vke)
                ozj__cqpya = list(veet__stqkr.data)
                ozj__cqpya[zgdjv__tngv] = val
                ozj__cqpya = tuple(ozj__cqpya)
            else:
                ctn__lip = veet__stqkr.columns + (cxias__vke,)
                ozj__cqpya = veet__stqkr.data + (val,)
            fhbn__pyl = DataFrameType(ozj__cqpya, index, ctn__lip,
                veet__stqkr.dist, veet__stqkr.is_table_format)
        return fhbn__pyl(*args)


SetDfColInfer.prefer_literal = True


def __bodosql_replace_columns_dummy(df, col_names_to_replace,
    cols_to_replace_with):
    for i in range(len(col_names_to_replace)):
        df[col_names_to_replace[i]] = cols_to_replace_with[i]


@infer_global(__bodosql_replace_columns_dummy)
class BodoSQLReplaceColsInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 3
        assert is_overload_constant_tuple(args[1])
        assert isinstance(args[2], types.BaseTuple)
        tqwq__ggw = args[0]
        assert isinstance(tqwq__ggw, DataFrameType) and len(tqwq__ggw.columns
            ) > 0, 'Error while typechecking __bodosql_replace_columns_dummy: we should only generate a call __bodosql_replace_columns_dummy if the input dataframe'
        col_names_to_replace = get_overload_const_tuple(args[1])
        ewfbc__mwntr = args[2]
        assert len(col_names_to_replace) == len(ewfbc__mwntr
            ), 'Error while typechecking __bodosql_replace_columns_dummy: the tuple of column indicies to replace should be equal to the number of columns to replace them with'
        assert len(col_names_to_replace) <= len(tqwq__ggw.columns
            ), 'Error while typechecking __bodosql_replace_columns_dummy: The number of indicies provided should be less than or equal to the number of columns in the input dataframe'
        for col_name in col_names_to_replace:
            assert col_name in tqwq__ggw.columns, 'Error while typechecking __bodosql_replace_columns_dummy: All columns specified to be replaced should already be present in input dataframe'
        check_runtime_cols_unsupported(tqwq__ggw,
            '__bodosql_replace_columns_dummy()')
        index = tqwq__ggw.index
        ctn__lip = tqwq__ggw.columns
        ozj__cqpya = list(tqwq__ggw.data)
        for i in range(len(col_names_to_replace)):
            col_name = col_names_to_replace[i]
            swufk__yycy = ewfbc__mwntr[i]
            assert isinstance(swufk__yycy, SeriesType
                ), 'Error while typechecking __bodosql_replace_columns_dummy: the values to replace the columns with are expected to be series'
            if isinstance(swufk__yycy, SeriesType):
                swufk__yycy = swufk__yycy.data
            sfgz__utmgq = tqwq__ggw.column_index[col_name]
            ozj__cqpya[sfgz__utmgq] = swufk__yycy
        ozj__cqpya = tuple(ozj__cqpya)
        fhbn__pyl = DataFrameType(ozj__cqpya, index, ctn__lip, tqwq__ggw.
            dist, tqwq__ggw.is_table_format)
        return fhbn__pyl(*args)


BodoSQLReplaceColsInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    zwixo__ijyc = {}

    def _rewrite_membership_op(self, node, left, right):
        wokrr__por = node.op
        op = self.visit(wokrr__por)
        return op, wokrr__por, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    afrxr__damz = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in afrxr__damz:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in afrxr__damz:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing('(' + self.name + ')')

    def visit_Attribute(self, node, **kwargs):
        nue__hvm = node.attr
        value = node.value
        qoyzd__glpvl = pd.core.computation.ops.LOCAL_TAG
        if nue__hvm in ('str', 'dt'):
            try:
                emp__egjw = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as lhwdn__ozi:
                col_name = lhwdn__ozi.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            emp__egjw = str(self.visit(value))
        mtb__xkyxk = emp__egjw, nue__hvm
        if mtb__xkyxk in join_cleaned_cols:
            nue__hvm = join_cleaned_cols[mtb__xkyxk]
        name = emp__egjw + '.' + nue__hvm
        if name.startswith(qoyzd__glpvl):
            name = name[len(qoyzd__glpvl):]
        if nue__hvm in ('str', 'dt'):
            sronl__tgcns = columns[cleaned_columns.index(emp__egjw)]
            zwixo__ijyc[sronl__tgcns] = emp__egjw
            self.env.scope[name] = 0
            return self.term_type(qoyzd__glpvl + name, self.env)
        afrxr__damz.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in afrxr__damz:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        oad__xzdyv = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        cxias__vke = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(oad__xzdyv), cxias__vke))

    def op__str__(self):
        fqc__ponxa = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            vni__sgp)) for vni__sgp in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(fqc__ponxa)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(fqc__ponxa)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(fqc__ponxa))
    yuur__lqlt = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    qdi__nnh = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    ppkdr__cgei = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    oxmvn__dgda = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    cwatr__ven = pd.core.computation.ops.Term.__str__
    nlyr__ubwvl = pd.core.computation.ops.MathCall.__str__
    afjwz__bforz = pd.core.computation.ops.Op.__str__
    cjz__ejkv = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        guls__fem = pd.core.computation.expr.Expr(expr, env=env)
        wmg__uuiz = str(guls__fem)
    except pd.core.computation.ops.UndefinedVariableError as lhwdn__ozi:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == lhwdn__ozi.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {lhwdn__ozi}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            yuur__lqlt)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            qdi__nnh)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = ppkdr__cgei
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = oxmvn__dgda
        pd.core.computation.ops.Term.__str__ = cwatr__ven
        pd.core.computation.ops.MathCall.__str__ = nlyr__ubwvl
        pd.core.computation.ops.Op.__str__ = afjwz__bforz
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            cjz__ejkv)
    vqvzj__obt = pd.core.computation.parsing.clean_column_name
    zwixo__ijyc.update({ytzv__mwl: vqvzj__obt(ytzv__mwl) for ytzv__mwl in
        columns if vqvzj__obt(ytzv__mwl) in guls__fem.names})
    return guls__fem, wmg__uuiz, zwixo__ijyc


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        gkah__wds = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(gkah__wds))
        hiw__gqzae = namedtuple('Pandas', col_names)
        jsut__iockl = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], hiw__gqzae)
        super(DataFrameTupleIterator, self).__init__(name, jsut__iockl)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_tz_naive_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        bgnrj__xeqy = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        bgnrj__xeqy = [types.Array(types.int64, 1, 'C')] + bgnrj__xeqy
        krtn__nlsf = DataFrameTupleIterator(col_names, bgnrj__xeqy)
        return krtn__nlsf(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gbnt__oshsc = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            gbnt__oshsc)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    gik__lqf = args[len(args) // 2:]
    dcdcz__ydp = sig.args[len(sig.args) // 2:]
    xxnt__eodl = context.make_helper(builder, sig.return_type)
    wnav__puerb = context.get_constant(types.intp, 0)
    srdpt__kdy = cgutils.alloca_once_value(builder, wnav__puerb)
    xxnt__eodl.index = srdpt__kdy
    for i, arr in enumerate(gik__lqf):
        setattr(xxnt__eodl, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(gik__lqf, dcdcz__ydp):
        context.nrt.incref(builder, arr_typ, arr)
    res = xxnt__eodl._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    fiyc__zfofw, = sig.args
    prgy__mni, = args
    xxnt__eodl = context.make_helper(builder, fiyc__zfofw, value=prgy__mni)
    dewyo__fwy = signature(types.intp, fiyc__zfofw.array_types[1])
    ujazu__idrc = context.compile_internal(builder, lambda a: len(a),
        dewyo__fwy, [xxnt__eodl.array0])
    index = builder.load(xxnt__eodl.index)
    vyar__lwmlv = builder.icmp_signed('<', index, ujazu__idrc)
    result.set_valid(vyar__lwmlv)
    with builder.if_then(vyar__lwmlv):
        values = [index]
        for i, arr_typ in enumerate(fiyc__zfofw.array_types[1:]):
            pvf__ndj = getattr(xxnt__eodl, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                stv__dtd = signature(pd_timestamp_tz_naive_type, arr_typ,
                    types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    stv__dtd, [pvf__ndj, index])
            else:
                stv__dtd = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    stv__dtd, [pvf__ndj, index])
            values.append(val)
        value = context.make_tuple(builder, fiyc__zfofw.yield_type, values)
        result.yield_(value)
        nrfxn__brx = cgutils.increment_index(builder, index)
        builder.store(nrfxn__brx, xxnt__eodl.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    mqbmu__vlcgi = ir.Assign(rhs, lhs, expr.loc)
    hcc__jdhj = lhs
    kaefj__rdh = []
    neevy__djxk = []
    ojkx__snqxm = typ.count
    for i in range(ojkx__snqxm):
        cok__uek = ir.Var(hcc__jdhj.scope, mk_unique_var('{}_size{}'.format
            (hcc__jdhj.name, i)), hcc__jdhj.loc)
        xlwbk__juon = ir.Expr.static_getitem(lhs, i, None, hcc__jdhj.loc)
        self.calltypes[xlwbk__juon] = None
        kaefj__rdh.append(ir.Assign(xlwbk__juon, cok__uek, hcc__jdhj.loc))
        self._define(equiv_set, cok__uek, types.intp, xlwbk__juon)
        neevy__djxk.append(cok__uek)
    dbp__lea = tuple(neevy__djxk)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        dbp__lea, pre=[mqbmu__vlcgi] + kaefj__rdh)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
