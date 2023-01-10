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
        hrqo__qnmu = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({hrqo__qnmu})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    fwih__bfoke = 'def impl(df):\n'
    if df.has_runtime_cols:
        fwih__bfoke += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        htp__prtpn = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        fwih__bfoke += f'  return {htp__prtpn}'
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo}, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
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
    bkyvw__zhagt = len(df.columns)
    pozda__dcu = set(i for i in range(bkyvw__zhagt) if isinstance(df.data[i
        ], IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in pozda__dcu else '') for i in
        range(bkyvw__zhagt))
    fwih__bfoke = 'def f(df):\n'.format()
    fwih__bfoke += '    return np.stack(({},), 1)\n'.format(data_args)
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo, 'np': np}, oeiz__fpxd)
    dil__rckbx = oeiz__fpxd['f']
    return dil__rckbx


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
    rbway__vuecn = {'dtype': dtype, 'na_value': na_value}
    bjxj__cnb = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', rbway__vuecn, bjxj__cnb,
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
            yrqoe__busp = bodo.hiframes.table.compute_num_runtime_columns(t)
            return yrqoe__busp * len(t)
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
            yrqoe__busp = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), yrqoe__busp
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), ncols)


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    fwih__bfoke = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    irhq__kdbkr = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    fwih__bfoke += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{irhq__kdbkr}), {index}, None)
"""
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo}, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
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
    rbway__vuecn = {'errors': errors}
    bjxj__cnb = {'errors': 'raise'}
    check_unsupported_args('df.astype', rbway__vuecn, bjxj__cnb,
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
        eeelm__myg = []
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        qwfko__ijfhr = _bodo_object_typeref.instance_type
        assert isinstance(qwfko__ijfhr, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        if df.is_table_format:
            for i, name in enumerate(df.columns):
                if name in qwfko__ijfhr.column_index:
                    idx = qwfko__ijfhr.column_index[name]
                    arr_typ = qwfko__ijfhr.data[idx]
                else:
                    arr_typ = df.data[i]
                eeelm__myg.append(arr_typ)
        else:
            extra_globals = {}
            cjun__lcnvl = {}
            for i, name in enumerate(qwfko__ijfhr.columns):
                arr_typ = qwfko__ijfhr.data[i]
                extra_globals[f'_bodo_schema{i}'] = get_castable_arr_dtype(
                    arr_typ)
                cjun__lcnvl[name] = f'_bodo_schema{i}'
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {cjun__lcnvl[nacja__xokax]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if nacja__xokax in cjun__lcnvl else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, nacja__xokax in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        puo__ffkv = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        if df.is_table_format:
            puo__ffkv = {name: dtype_to_array_type(parse_dtype(dtype)) for 
                name, dtype in puo__ffkv.items()}
            for i, name in enumerate(df.columns):
                if name in puo__ffkv:
                    arr_typ = puo__ffkv[name]
                else:
                    arr_typ = df.data[i]
                eeelm__myg.append(arr_typ)
        else:
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(puo__ffkv[nacja__xokax])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if nacja__xokax in puo__ffkv else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, nacja__xokax in enumerate(df.columns))
    elif df.is_table_format:
        arr_typ = dtype_to_array_type(parse_dtype(dtype))
        eeelm__myg = [arr_typ] * len(df.columns)
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    if df.is_table_format:
        ktrw__hjggz = bodo.TableType(tuple(eeelm__myg))
        extra_globals['out_table_typ'] = ktrw__hjggz
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
        njows__kjnqj = types.none
        extra_globals = {'output_arr_typ': njows__kjnqj}
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
        xowp__fqevv = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                xowp__fqevv.append(arr + '.copy()')
            elif is_overload_false(deep):
                xowp__fqevv.append(arr)
            else:
                xowp__fqevv.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(xowp__fqevv)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    rbway__vuecn = {'index': index, 'level': level, 'errors': errors}
    bjxj__cnb = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', rbway__vuecn, bjxj__cnb,
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
        qyfk__wlfx = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        qyfk__wlfx = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    dgfg__tcbu = tuple([qyfk__wlfx.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    hsuds__hgt = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        hsuds__hgt = df.copy(columns=dgfg__tcbu)
        njows__kjnqj = types.none
        extra_globals = {'output_arr_typ': njows__kjnqj}
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
        xowp__fqevv = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                xowp__fqevv.append(arr + '.copy()')
            elif is_overload_false(copy):
                xowp__fqevv.append(arr)
            else:
                xowp__fqevv.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(xowp__fqevv)
    return _gen_init_df(header, dgfg__tcbu, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    oprox__pfxsd = not is_overload_none(items)
    dfehi__eeptb = not is_overload_none(like)
    one__uzuu = not is_overload_none(regex)
    vywaw__ymxw = oprox__pfxsd ^ dfehi__eeptb ^ one__uzuu
    qrm__fiepb = not (oprox__pfxsd or dfehi__eeptb or one__uzuu)
    if qrm__fiepb:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not vywaw__ymxw:
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
        xzzg__czi = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        xzzg__czi = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert xzzg__czi in {0, 1}
    fwih__bfoke = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if xzzg__czi == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if xzzg__czi == 1:
        ghvvs__yym = []
        ucz__vtvuh = []
        kmk__jym = []
        if oprox__pfxsd:
            if is_overload_constant_list(items):
                yxet__lcxlc = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if dfehi__eeptb:
            if is_overload_constant_str(like):
                tvso__alah = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if one__uzuu:
            if is_overload_constant_str(regex):
                lkm__sfdy = get_overload_const_str(regex)
                gwnwi__xon = re.compile(lkm__sfdy)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, nacja__xokax in enumerate(df.columns):
            if not is_overload_none(items
                ) and nacja__xokax in yxet__lcxlc or not is_overload_none(like
                ) and tvso__alah in str(nacja__xokax) or not is_overload_none(
                regex) and gwnwi__xon.search(str(nacja__xokax)):
                ucz__vtvuh.append(nacja__xokax)
                kmk__jym.append(i)
        for i in kmk__jym:
            var_name = f'data_{i}'
            ghvvs__yym.append(var_name)
            fwih__bfoke += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(ghvvs__yym)
        return _gen_init_df(fwih__bfoke, ucz__vtvuh, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    hsuds__hgt = None
    if df.is_table_format:
        njows__kjnqj = types.Array(types.bool_, 1, 'C')
        hsuds__hgt = DataFrameType(tuple([njows__kjnqj] * len(df.data)), df
            .index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': njows__kjnqj}
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
    hau__glkpt = is_overload_none(include)
    otzfs__tagze = is_overload_none(exclude)
    arihx__mjsph = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if hau__glkpt and otzfs__tagze:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not hau__glkpt:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            iyqid__aunn = [dtype_to_array_type(parse_dtype(elem,
                arihx__mjsph)) for elem in include]
        elif is_legal_input(include):
            iyqid__aunn = [dtype_to_array_type(parse_dtype(include,
                arihx__mjsph))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        iyqid__aunn = get_nullable_and_non_nullable_types(iyqid__aunn)
        cvwa__gock = tuple(nacja__xokax for i, nacja__xokax in enumerate(df
            .columns) if df.data[i] in iyqid__aunn)
    else:
        cvwa__gock = df.columns
    if not otzfs__tagze:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            jtffj__tgzph = [dtype_to_array_type(parse_dtype(elem,
                arihx__mjsph)) for elem in exclude]
        elif is_legal_input(exclude):
            jtffj__tgzph = [dtype_to_array_type(parse_dtype(exclude,
                arihx__mjsph))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        jtffj__tgzph = get_nullable_and_non_nullable_types(jtffj__tgzph)
        cvwa__gock = tuple(nacja__xokax for nacja__xokax in cvwa__gock if 
            df.data[df.column_index[nacja__xokax]] not in jtffj__tgzph)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[nacja__xokax]})'
         for nacja__xokax in cvwa__gock)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, cvwa__gock, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    hsuds__hgt = None
    if df.is_table_format:
        njows__kjnqj = types.Array(types.bool_, 1, 'C')
        hsuds__hgt = DataFrameType(tuple([njows__kjnqj] * len(df.data)), df
            .index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': njows__kjnqj}
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
    uvwk__bintw = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in uvwk__bintw:
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
    uvwk__bintw = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in uvwk__bintw:
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
    fwih__bfoke = 'def impl(df, values):\n'
    gmwut__elxv = {}
    sll__nbbp = False
    if isinstance(values, DataFrameType):
        sll__nbbp = True
        for i, nacja__xokax in enumerate(df.columns):
            if nacja__xokax in values.column_index:
                tgbx__nxtl = 'val{}'.format(i)
                fwih__bfoke += f"""  {tgbx__nxtl} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[nacja__xokax]})
"""
                gmwut__elxv[nacja__xokax] = tgbx__nxtl
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        gmwut__elxv = {nacja__xokax: 'values' for nacja__xokax in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        tgbx__nxtl = 'data{}'.format(i)
        fwih__bfoke += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(tgbx__nxtl, i))
        data.append(tgbx__nxtl)
    vxs__lizw = ['out{}'.format(i) for i in range(len(df.columns))]
    rirf__mhbjh = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    hff__zps = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    ypl__byoq = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, mfoi__ycv) in enumerate(zip(df.columns, data)):
        if cname in gmwut__elxv:
            dzh__czdx = gmwut__elxv[cname]
            if sll__nbbp:
                fwih__bfoke += rirf__mhbjh.format(mfoi__ycv, dzh__czdx,
                    vxs__lizw[i])
            else:
                fwih__bfoke += hff__zps.format(mfoi__ycv, dzh__czdx,
                    vxs__lizw[i])
        else:
            fwih__bfoke += ypl__byoq.format(vxs__lizw[i])
    return _gen_init_df(fwih__bfoke, df.columns, ','.join(vxs__lizw))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    bkyvw__zhagt = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(bkyvw__zhagt))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    biolu__ybb = [nacja__xokax for nacja__xokax, xjvus__vjv in zip(df.
        columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype(
        xjvus__vjv.dtype)]
    assert len(biolu__ybb) != 0
    myk__tyu = ''
    if not any(xjvus__vjv == types.float64 for xjvus__vjv in df.data):
        myk__tyu = '.astype(np.float64)'
    likem__asq = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[nacja__xokax], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[nacja__xokax]], IntegerArrayType
        ) or df.data[df.column_index[nacja__xokax]] == boolean_array else
        '') for nacja__xokax in biolu__ybb)
    wrm__wrazf = 'np.stack(({},), 1){}'.format(likem__asq, myk__tyu)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(biolu__ybb))
        )
    index = f'{generate_col_to_index_func_text(biolu__ybb)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(wrm__wrazf)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, biolu__ybb, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    bobbd__oxyz = dict(ddof=ddof)
    qpsl__yjq = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    nexo__bub = '1' if is_overload_none(min_periods) else 'min_periods'
    biolu__ybb = [nacja__xokax for nacja__xokax, xjvus__vjv in zip(df.
        columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype(
        xjvus__vjv.dtype)]
    if len(biolu__ybb) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    myk__tyu = ''
    if not any(xjvus__vjv == types.float64 for xjvus__vjv in df.data):
        myk__tyu = '.astype(np.float64)'
    likem__asq = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[nacja__xokax], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[nacja__xokax]], IntegerArrayType
        ) or df.data[df.column_index[nacja__xokax]] == boolean_array else
        '') for nacja__xokax in biolu__ybb)
    wrm__wrazf = 'np.stack(({},), 1){}'.format(likem__asq, myk__tyu)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(biolu__ybb))
        )
    index = f'pd.Index({biolu__ybb})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(wrm__wrazf)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        nexo__bub)
    return _gen_init_df(header, biolu__ybb, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    bobbd__oxyz = dict(axis=axis, level=level, numeric_only=numeric_only)
    qpsl__yjq = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    fwih__bfoke = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    fwih__bfoke += '  data = np.array([{}])\n'.format(data_args)
    htp__prtpn = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    fwih__bfoke += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {htp__prtpn})\n'
        )
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo, 'np': np}, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    bobbd__oxyz = dict(axis=axis)
    qpsl__yjq = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    fwih__bfoke = 'def impl(df, axis=0, dropna=True):\n'
    fwih__bfoke += '  data = np.asarray(({},))\n'.format(data_args)
    htp__prtpn = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    fwih__bfoke += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {htp__prtpn})\n'
        )
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo, 'np': np}, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    bobbd__oxyz = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    qpsl__yjq = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    bobbd__oxyz = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    qpsl__yjq = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    bobbd__oxyz = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    qpsl__yjq = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    bobbd__oxyz = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    qpsl__yjq = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    bobbd__oxyz = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    qpsl__yjq = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    bobbd__oxyz = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    qpsl__yjq = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    bobbd__oxyz = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    qpsl__yjq = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    bobbd__oxyz = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    qpsl__yjq = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    bobbd__oxyz = dict(numeric_only=numeric_only, interpolation=interpolation)
    qpsl__yjq = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    bobbd__oxyz = dict(axis=axis, skipna=skipna)
    qpsl__yjq = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for dsn__qezy in df.data:
        if not (bodo.utils.utils.is_np_array_typ(dsn__qezy) and (dsn__qezy.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            dsn__qezy.dtype, (types.Number, types.Boolean))) or isinstance(
            dsn__qezy, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo
            .CategoricalArrayType)) or dsn__qezy in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {dsn__qezy} not supported.'
                )
        if isinstance(dsn__qezy, bodo.CategoricalArrayType
            ) and not dsn__qezy.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    bobbd__oxyz = dict(axis=axis, skipna=skipna)
    qpsl__yjq = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for dsn__qezy in df.data:
        if not (bodo.utils.utils.is_np_array_typ(dsn__qezy) and (dsn__qezy.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            dsn__qezy.dtype, (types.Number, types.Boolean))) or isinstance(
            dsn__qezy, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo
            .CategoricalArrayType)) or dsn__qezy in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {dsn__qezy} not supported.'
                )
        if isinstance(dsn__qezy, bodo.CategoricalArrayType
            ) and not dsn__qezy.dtype.ordered:
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
        biolu__ybb = tuple(nacja__xokax for nacja__xokax, xjvus__vjv in zip
            (df.columns, df.data) if bodo.utils.typing.
            _is_pandas_numeric_dtype(xjvus__vjv.dtype))
        out_colnames = biolu__ybb
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            dox__slj = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[nacja__xokax]].dtype) for nacja__xokax in
                out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(dox__slj, []))
    except NotImplementedError as gubv__ibtrr:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    zibyo__ret = ''
    if func_name in ('sum', 'prod'):
        zibyo__ret = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    fwih__bfoke = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, zibyo__ret))
    if func_name == 'quantile':
        fwih__bfoke = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        fwih__bfoke = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        fwih__bfoke += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        fwih__bfoke += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        oeiz__fpxd)
    impl = oeiz__fpxd['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    boain__njix = ''
    if func_name in ('min', 'max'):
        boain__njix = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        boain__njix = ', dtype=np.float32'
    rvsk__rdpi = f'bodo.libs.array_ops.array_op_{func_name}'
    upf__wru = ''
    if func_name in ['sum', 'prod']:
        upf__wru = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        upf__wru = 'index'
    elif func_name == 'quantile':
        upf__wru = 'q'
    elif func_name in ['std', 'var']:
        upf__wru = 'True, ddof'
    elif func_name == 'median':
        upf__wru = 'True'
    data_args = ', '.join(
        f'{rvsk__rdpi}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[nacja__xokax]}), {upf__wru})'
         for nacja__xokax in out_colnames)
    fwih__bfoke = ''
    if func_name in ('idxmax', 'idxmin'):
        fwih__bfoke += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        fwih__bfoke += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        fwih__bfoke += '  data = np.asarray(({},){})\n'.format(data_args,
            boain__njix)
    fwih__bfoke += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return fwih__bfoke


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    oafuz__ixwks = [df_type.column_index[nacja__xokax] for nacja__xokax in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in oafuz__ixwks)
    gstl__mrkre = '\n        '.join(f'row[{i}] = arr_{oafuz__ixwks[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    eaiw__ztj = f'len(arr_{oafuz__ixwks[0]})'
    mpoc__aqjiv = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in mpoc__aqjiv:
        rnanb__afw = mpoc__aqjiv[func_name]
        oggtu__tjh = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        fwih__bfoke = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {eaiw__ztj}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{oggtu__tjh})
    for i in numba.parfors.parfor.internal_prange(n):
        {gstl__mrkre}
        A[i] = {rnanb__afw}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return fwih__bfoke
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    bobbd__oxyz = dict(fill_method=fill_method, limit=limit, freq=freq)
    qpsl__yjq = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', bobbd__oxyz, qpsl__yjq,
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
    bobbd__oxyz = dict(axis=axis, skipna=skipna)
    qpsl__yjq = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', bobbd__oxyz, qpsl__yjq,
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
    bobbd__oxyz = dict(skipna=skipna)
    qpsl__yjq = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', bobbd__oxyz, qpsl__yjq,
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
    bobbd__oxyz = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    qpsl__yjq = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    biolu__ybb = [nacja__xokax for nacja__xokax, xjvus__vjv in zip(df.
        columns, df.data) if _is_describe_type(xjvus__vjv)]
    if len(biolu__ybb) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    cno__lhucl = sum(df.data[df.column_index[nacja__xokax]].dtype == bodo.
        datetime64ns for nacja__xokax in biolu__ybb)

    def _get_describe(col_ind):
        vcjyu__vowel = df.data[col_ind].dtype == bodo.datetime64ns
        if cno__lhucl and cno__lhucl != len(biolu__ybb):
            if vcjyu__vowel:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for nacja__xokax in biolu__ybb:
        col_ind = df.column_index[nacja__xokax]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[nacja__xokax]) for
        nacja__xokax in biolu__ybb)
    qfi__dom = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if cno__lhucl == len(biolu__ybb):
        qfi__dom = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif cno__lhucl:
        qfi__dom = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({qfi__dom})'
    return _gen_init_df(header, biolu__ybb, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    bobbd__oxyz = dict(axis=axis, convert=convert, is_copy=is_copy)
    qpsl__yjq = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', bobbd__oxyz, qpsl__yjq,
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
    bobbd__oxyz = dict(freq=freq, axis=axis)
    qpsl__yjq = dict(freq=None, axis=0)
    check_unsupported_args('DataFrame.shift', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for jgp__qih in df.data:
        if not is_supported_shift_array_type(jgp__qih):
            raise BodoError(
                f'Dataframe.shift() column input type {jgp__qih.dtype} not supported yet.'
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
    bobbd__oxyz = dict(axis=axis)
    qpsl__yjq = dict(axis=0)
    check_unsupported_args('DataFrame.diff', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for jgp__qih in df.data:
        if not (isinstance(jgp__qih, types.Array) and (isinstance(jgp__qih.
            dtype, types.Number) or jgp__qih.dtype == bodo.datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {jgp__qih.dtype} not supported.'
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
    bxdrr__fiki = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(bxdrr__fiki)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        xrnq__trtdu = get_overload_const_list(column)
    else:
        xrnq__trtdu = [get_literal_value(column)]
    izw__hglfr = [df.column_index[nacja__xokax] for nacja__xokax in xrnq__trtdu
        ]
    for i in izw__hglfr:
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
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{izw__hglfr[0]})\n'
        )
    for i in range(n):
        if i in izw__hglfr:
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
    rbway__vuecn = {'inplace': inplace, 'append': append,
        'verify_integrity': verify_integrity}
    bjxj__cnb = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', rbway__vuecn, bjxj__cnb,
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
    columns = tuple(nacja__xokax for nacja__xokax in df.columns if 
        nacja__xokax != col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    rbway__vuecn = {'inplace': inplace}
    bjxj__cnb = {'inplace': False}
    check_unsupported_args('query', rbway__vuecn, bjxj__cnb, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        hrspc__uzvl = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[hrspc__uzvl]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    rbway__vuecn = {'subset': subset, 'keep': keep}
    bjxj__cnb = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', rbway__vuecn, bjxj__cnb,
        package_name='pandas', module_name='DataFrame')
    bkyvw__zhagt = len(df.columns)
    fwih__bfoke = "def impl(df, subset=None, keep='first'):\n"
    for i in range(bkyvw__zhagt):
        fwih__bfoke += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    xstr__lpjav = ', '.join(f'data_{i}' for i in range(bkyvw__zhagt))
    xstr__lpjav += ',' if bkyvw__zhagt == 1 else ''
    fwih__bfoke += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({xstr__lpjav}))\n'
        )
    fwih__bfoke += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    fwih__bfoke += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo}, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    rbway__vuecn = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    bjxj__cnb = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    fzdf__nnha = []
    if is_overload_constant_list(subset):
        fzdf__nnha = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        fzdf__nnha = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        fzdf__nnha = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    qtk__vxs = []
    for col_name in fzdf__nnha:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        qtk__vxs.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', rbway__vuecn,
        bjxj__cnb, package_name='pandas', module_name='DataFrame')
    cjjq__uvsl = []
    if qtk__vxs:
        for usetq__zsst in qtk__vxs:
            if isinstance(df.data[usetq__zsst], bodo.MapArrayType):
                cjjq__uvsl.append(df.columns[usetq__zsst])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                cjjq__uvsl.append(col_name)
    if cjjq__uvsl:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {cjjq__uvsl} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    bkyvw__zhagt = len(df.columns)
    sob__fit = ['data_{}'.format(i) for i in qtk__vxs]
    qxdm__fvh = ['data_{}'.format(i) for i in range(bkyvw__zhagt) if i not in
        qtk__vxs]
    if sob__fit:
        gtu__npl = len(sob__fit)
    else:
        gtu__npl = bkyvw__zhagt
    huvea__ftxik = ', '.join(sob__fit + qxdm__fvh)
    data_args = ', '.join('data_{}'.format(i) for i in range(bkyvw__zhagt))
    fwih__bfoke = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(bkyvw__zhagt):
        fwih__bfoke += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    fwih__bfoke += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(huvea__ftxik, index, gtu__npl))
    fwih__bfoke += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(fwih__bfoke, df.columns, data_args, 'index')


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
            uxjxj__kbwg = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                uxjxj__kbwg = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                uxjxj__kbwg = lambda i: f'other[:,{i}]'
        bkyvw__zhagt = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {uxjxj__kbwg(i)})'
             for i in range(bkyvw__zhagt))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        miek__gfvpe = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(
            miek__gfvpe)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    bobbd__oxyz = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    qpsl__yjq = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', bobbd__oxyz, qpsl__yjq,
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
    bkyvw__zhagt = len(df.columns)
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
        for i in range(bkyvw__zhagt):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], other.data[other.
                    column_index[df.columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(bkyvw__zhagt):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other.data)
    else:
        for i in range(bkyvw__zhagt):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    fdxil__yun = ColNamesMetaType(tuple(columns))
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    fwih__bfoke = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, __col_name_meta_value_gen_init_df)
"""
    oeiz__fpxd = {}
    our__hxm = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba,
        '__col_name_meta_value_gen_init_df': fdxil__yun}
    our__hxm.update(extra_globals)
    exec(fwih__bfoke, our__hxm, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        ctmjf__chz = pd.Index(lhs.columns)
        wcrv__ebfzs = pd.Index(rhs.columns)
        sxp__roe, ragx__ynan, qmc__djt = ctmjf__chz.join(wcrv__ebfzs, how=
            'left' if is_inplace else 'outer', level=None, return_indexers=True
            )
        return tuple(sxp__roe), ragx__ynan, qmc__djt
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        jmxi__aje = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        lka__eepl = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, jmxi__aje)
        check_runtime_cols_unsupported(rhs, jmxi__aje)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                sxp__roe, ragx__ynan, qmc__djt = _get_binop_columns(lhs, rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {jvztc__khwuo}) {jmxi__aje}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {lemp__edh})'
                     if jvztc__khwuo != -1 and lemp__edh != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for jvztc__khwuo, lemp__edh in zip(ragx__ynan, qmc__djt))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, sxp__roe, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            oftyn__pxtd = []
            rqr__witgw = []
            if op in lka__eepl:
                for i, gss__fuijl in enumerate(lhs.data):
                    if is_common_scalar_dtype([gss__fuijl.dtype, rhs]):
                        oftyn__pxtd.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {jmxi__aje} rhs'
                            )
                    else:
                        luet__batxw = f'arr{i}'
                        rqr__witgw.append(luet__batxw)
                        oftyn__pxtd.append(luet__batxw)
                data_args = ', '.join(oftyn__pxtd)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {jmxi__aje} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(rqr__witgw) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {luet__batxw} = np.empty(n, dtype=np.bool_)\n' for
                    luet__batxw in rqr__witgw)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(luet__batxw, 
                    op == operator.ne) for luet__batxw in rqr__witgw)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            oftyn__pxtd = []
            rqr__witgw = []
            if op in lka__eepl:
                for i, gss__fuijl in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, gss__fuijl.dtype]):
                        oftyn__pxtd.append(
                            f'lhs {jmxi__aje} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        luet__batxw = f'arr{i}'
                        rqr__witgw.append(luet__batxw)
                        oftyn__pxtd.append(luet__batxw)
                data_args = ', '.join(oftyn__pxtd)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, jmxi__aje) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(rqr__witgw) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(luet__batxw) for luet__batxw in rqr__witgw)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(luet__batxw, 
                    op == operator.ne) for luet__batxw in rqr__witgw)
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
        miek__gfvpe = create_binary_op_overload(op)
        overload(op)(miek__gfvpe)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        jmxi__aje = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, jmxi__aje)
        check_runtime_cols_unsupported(right, jmxi__aje)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                sxp__roe, _, qmc__djt = _get_binop_columns(left, right, True)
                fwih__bfoke = 'def impl(left, right):\n'
                for i, lemp__edh in enumerate(qmc__djt):
                    if lemp__edh == -1:
                        fwih__bfoke += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    fwih__bfoke += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    fwih__bfoke += f"""  df_arr{i} {jmxi__aje} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {lemp__edh})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    sxp__roe)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(fwih__bfoke, sxp__roe, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            fwih__bfoke = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                fwih__bfoke += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                fwih__bfoke += '  df_arr{0} {1} right\n'.format(i, jmxi__aje)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(fwih__bfoke, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        miek__gfvpe = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(miek__gfvpe)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            jmxi__aje = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, jmxi__aje)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, jmxi__aje) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        miek__gfvpe = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(miek__gfvpe)


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
            wjdix__mlit = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                wjdix__mlit[i] = bodo.libs.array_kernels.isna(obj, i)
            return wjdix__mlit
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
            wjdix__mlit = np.empty(n, np.bool_)
            for i in range(n):
                wjdix__mlit[i] = pd.isna(obj[i])
            return wjdix__mlit
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
    rbway__vuecn = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    bjxj__cnb = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', rbway__vuecn, bjxj__cnb, package_name
        ='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    gto__vlsd = str(expr_node)
    return gto__vlsd.startswith('(left.') or gto__vlsd.startswith('(right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    feoyj__oanlm = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (feoyj__oanlm,))
    vojz__qllps = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        dfr__fjqca = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        epa__ehe = {('NOT_NA', vojz__qllps(gss__fuijl)): gss__fuijl for
            gss__fuijl in null_set}
        zseq__lryl, _, _ = _parse_query_expr(dfr__fjqca, env, [], [], None,
            join_cleaned_cols=epa__ehe)
        fxu__tfl = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            qjb__qbsfq = pd.core.computation.ops.BinOp('&', zseq__lryl,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = fxu__tfl
        return qjb__qbsfq

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                xqi__gyo = set()
                zqnz__zoao = set()
                rxhg__azaij = _insert_NA_cond_body(expr_node.lhs, xqi__gyo)
                afn__fssa = _insert_NA_cond_body(expr_node.rhs, zqnz__zoao)
                qyi__czlmb = xqi__gyo.intersection(zqnz__zoao)
                xqi__gyo.difference_update(qyi__czlmb)
                zqnz__zoao.difference_update(qyi__czlmb)
                null_set.update(qyi__czlmb)
                expr_node.lhs = append_null_checks(rxhg__azaij, xqi__gyo)
                expr_node.rhs = append_null_checks(afn__fssa, zqnz__zoao)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            jff__ffke = expr_node.name
            hptc__gasb, col_name = jff__ffke.split('.')
            if hptc__gasb == 'left':
                cgf__fkbjs = left_columns
                data = left_data
            else:
                cgf__fkbjs = right_columns
                data = right_data
            nyph__bosi = data[cgf__fkbjs.index(col_name)]
            if bodo.utils.typing.is_nullable(nyph__bosi):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    tmkx__tjx = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        xxf__ujckr = str(expr_node.lhs)
        ibkfn__wvrwr = str(expr_node.rhs)
        if xxf__ujckr.startswith('(left.') and ibkfn__wvrwr.startswith('(left.'
            ) or xxf__ujckr.startswith('(right.') and ibkfn__wvrwr.startswith(
            '(right.'):
            return [], [], expr_node
        left_on = [xxf__ujckr.split('.')[1][:-1]]
        right_on = [ibkfn__wvrwr.split('.')[1][:-1]]
        if xxf__ujckr.startswith('(right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        ahs__aisas, zwb__aeuvm, ponv__ssrp = _extract_equal_conds(expr_node.lhs
            )
        hxmb__svkwr, udp__aoben, ncjp__dgh = _extract_equal_conds(expr_node.rhs
            )
        left_on = ahs__aisas + hxmb__svkwr
        right_on = zwb__aeuvm + udp__aoben
        if ponv__ssrp is None:
            return left_on, right_on, ncjp__dgh
        if ncjp__dgh is None:
            return left_on, right_on, ponv__ssrp
        expr_node.lhs = ponv__ssrp
        expr_node.rhs = ncjp__dgh
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    feoyj__oanlm = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (feoyj__oanlm,))
    qyfk__wlfx = dict()
    vojz__qllps = pd.core.computation.parsing.clean_column_name
    for name, xtv__eujs in (('left', left_columns), ('right', right_columns)):
        for gss__fuijl in xtv__eujs:
            qrb__pzf = vojz__qllps(gss__fuijl)
            bfd__aisle = name, qrb__pzf
            if bfd__aisle in qyfk__wlfx:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{gss__fuijl}' and '{qyfk__wlfx[qrb__pzf]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            qyfk__wlfx[bfd__aisle] = gss__fuijl
    hxye__qlcr, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=qyfk__wlfx)
    left_on, right_on, ewaz__jsp = _extract_equal_conds(hxye__qlcr.terms)
    return left_on, right_on, _insert_NA_cond(ewaz__jsp, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    bobbd__oxyz = dict(sort=sort, copy=copy, validate=validate)
    qpsl__yjq = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    dha__lbu = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    zyey__ephn = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in dha__lbu and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, uqj__rkehu = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if uqj__rkehu is None:
                    zyey__ephn = ''
                else:
                    zyey__ephn = str(uqj__rkehu)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = dha__lbu
        right_keys = dha__lbu
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
    xojtt__rvab = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        xtufy__oso = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        xtufy__oso = list(get_overload_const_list(suffixes))
    suffix_x = xtufy__oso[0]
    suffix_y = xtufy__oso[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    fwih__bfoke = (
        "def _impl(left, right, how='inner', on=None, left_on=None,\n")
    fwih__bfoke += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    fwih__bfoke += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    fwih__bfoke += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, xojtt__rvab, zyey__ephn))
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo}, oeiz__fpxd)
    _impl = oeiz__fpxd['_impl']
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
    qhtb__sgs = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    tnsn__lay = {get_overload_const_str(nexbl__qyd) for nexbl__qyd in (
        left_on, right_on, on) if is_overload_constant_str(nexbl__qyd)}
    for df in (left, right):
        for i, gss__fuijl in enumerate(df.data):
            if not isinstance(gss__fuijl, valid_dataframe_column_types
                ) and gss__fuijl not in qhtb__sgs:
                raise BodoError(
                    f'{name_func}(): use of column with {type(gss__fuijl)} in merge unsupported'
                    )
            if df.columns[i] in tnsn__lay and isinstance(gss__fuijl,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        xtufy__oso = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        xtufy__oso = list(get_overload_const_list(suffixes))
    if len(xtufy__oso) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    dha__lbu = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        gxx__cvd = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            gxx__cvd = on_str not in dha__lbu and ('left.' in on_str or 
                'right.' in on_str)
        if len(dha__lbu) == 0 and not gxx__cvd:
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
    bpuuh__ihugk = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            vzo__csnxk = left.index
            opp__hhd = isinstance(vzo__csnxk, StringIndexType)
            lotz__orzxw = right.index
            emvlf__tjz = isinstance(lotz__orzxw, StringIndexType)
        elif is_overload_true(left_index):
            vzo__csnxk = left.index
            opp__hhd = isinstance(vzo__csnxk, StringIndexType)
            lotz__orzxw = right.data[right.columns.index(right_keys[0])]
            emvlf__tjz = lotz__orzxw.dtype == string_type
        elif is_overload_true(right_index):
            vzo__csnxk = left.data[left.columns.index(left_keys[0])]
            opp__hhd = vzo__csnxk.dtype == string_type
            lotz__orzxw = right.index
            emvlf__tjz = isinstance(lotz__orzxw, StringIndexType)
        if opp__hhd and emvlf__tjz:
            return
        vzo__csnxk = vzo__csnxk.dtype
        lotz__orzxw = lotz__orzxw.dtype
        try:
            ktf__abkoa = bpuuh__ihugk.resolve_function_type(operator.eq, (
                vzo__csnxk, lotz__orzxw), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=vzo__csnxk, rk_dtype=lotz__orzxw))
    else:
        for turo__ren, zwks__iuwy in zip(left_keys, right_keys):
            vzo__csnxk = left.data[left.columns.index(turo__ren)].dtype
            nxwib__scdsd = left.data[left.columns.index(turo__ren)]
            lotz__orzxw = right.data[right.columns.index(zwks__iuwy)].dtype
            ugd__grwxs = right.data[right.columns.index(zwks__iuwy)]
            if nxwib__scdsd == ugd__grwxs:
                continue
            jfix__wfhi = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=turo__ren, lk_dtype=vzo__csnxk, rk=zwks__iuwy,
                rk_dtype=lotz__orzxw))
            nlybv__whqp = vzo__csnxk == string_type
            rqwn__lho = lotz__orzxw == string_type
            if nlybv__whqp ^ rqwn__lho:
                raise_bodo_error(jfix__wfhi)
            try:
                ktf__abkoa = bpuuh__ihugk.resolve_function_type(operator.eq,
                    (vzo__csnxk, lotz__orzxw), {})
            except:
                raise_bodo_error(jfix__wfhi)


def validate_keys(keys, df):
    ftas__thb = set(keys).difference(set(df.columns))
    if len(ftas__thb) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in ftas__thb:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {ftas__thb} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    bobbd__oxyz = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    qpsl__yjq = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', bobbd__oxyz, qpsl__yjq,
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
    fwih__bfoke = "def _impl(left, other, on=None, how='left',\n"
    fwih__bfoke += "    lsuffix='', rsuffix='', sort=False):\n"
    fwih__bfoke += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo}, oeiz__fpxd)
    _impl = oeiz__fpxd['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        iuibu__dsad = get_overload_const_list(on)
        validate_keys(iuibu__dsad, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    dha__lbu = tuple(set(left.columns) & set(other.columns))
    if len(dha__lbu) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=dha__lbu))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    csxj__weg = set(left_keys) & set(right_keys)
    cae__fte = set(left_columns) & set(right_columns)
    wju__taa = cae__fte - csxj__weg
    kzue__fqlf = set(left_columns) - cae__fte
    vef__zvgv = set(right_columns) - cae__fte
    qeiwy__jut = {}

    def insertOutColumn(col_name):
        if col_name in qeiwy__jut:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        qeiwy__jut[col_name] = 0
    for uszwv__qgf in csxj__weg:
        insertOutColumn(uszwv__qgf)
    for uszwv__qgf in wju__taa:
        gqpw__gqzs = str(uszwv__qgf) + suffix_x
        bjwck__sro = str(uszwv__qgf) + suffix_y
        insertOutColumn(gqpw__gqzs)
        insertOutColumn(bjwck__sro)
    for uszwv__qgf in kzue__fqlf:
        insertOutColumn(uszwv__qgf)
    for uszwv__qgf in vef__zvgv:
        insertOutColumn(uszwv__qgf)
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
    dha__lbu = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = dha__lbu
        right_keys = dha__lbu
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
        xtufy__oso = suffixes
    if is_overload_constant_list(suffixes):
        xtufy__oso = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        xtufy__oso = suffixes.value
    suffix_x = xtufy__oso[0]
    suffix_y = xtufy__oso[1]
    fwih__bfoke = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    fwih__bfoke += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    fwih__bfoke += (
        "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n")
    fwih__bfoke += "    allow_exact_matches=True, direction='backward'):\n"
    fwih__bfoke += '  suffix_x = suffixes[0]\n'
    fwih__bfoke += '  suffix_y = suffixes[1]\n'
    fwih__bfoke += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo}, oeiz__fpxd)
    _impl = oeiz__fpxd['_impl']
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
    bobbd__oxyz = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    rpkyc__dds = dict(sort=False, group_keys=True, squeeze=False, observed=True
        )
    check_unsupported_args('Dataframe.groupby', bobbd__oxyz, rpkyc__dds,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    egnh__aoxx = func_name == 'DataFrame.pivot_table'
    if egnh__aoxx:
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
    auqpd__pznw = get_literal_value(columns)
    if isinstance(auqpd__pznw, (list, tuple)):
        if len(auqpd__pznw) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {auqpd__pznw}"
                )
        auqpd__pznw = auqpd__pznw[0]
    if auqpd__pznw not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {auqpd__pznw} not found in DataFrame {df}."
            )
    lcg__wsm = df.column_index[auqpd__pznw]
    if is_overload_none(index):
        jfxp__ipjxp = []
        gsq__jatk = []
    else:
        gsq__jatk = get_literal_value(index)
        if not isinstance(gsq__jatk, (list, tuple)):
            gsq__jatk = [gsq__jatk]
        jfxp__ipjxp = []
        for index in gsq__jatk:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            jfxp__ipjxp.append(df.column_index[index])
    if not (all(isinstance(nacja__xokax, int) for nacja__xokax in gsq__jatk
        ) or all(isinstance(nacja__xokax, str) for nacja__xokax in gsq__jatk)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        dxm__cpjio = []
        lrgvz__qbhnh = []
        cuqnj__wwfg = jfxp__ipjxp + [lcg__wsm]
        for i, nacja__xokax in enumerate(df.columns):
            if i not in cuqnj__wwfg:
                dxm__cpjio.append(i)
                lrgvz__qbhnh.append(nacja__xokax)
    else:
        lrgvz__qbhnh = get_literal_value(values)
        if not isinstance(lrgvz__qbhnh, (list, tuple)):
            lrgvz__qbhnh = [lrgvz__qbhnh]
        dxm__cpjio = []
        for val in lrgvz__qbhnh:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            dxm__cpjio.append(df.column_index[val])
    eudu__ealn = set(dxm__cpjio) | set(jfxp__ipjxp) | {lcg__wsm}
    if len(eudu__ealn) != len(dxm__cpjio) + len(jfxp__ipjxp) + 1:
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
    if len(jfxp__ipjxp) == 0:
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
        for flt__uvyvz in jfxp__ipjxp:
            index_column = df.data[flt__uvyvz]
            check_valid_index_typ(index_column)
    ftrz__lkmdd = df.data[lcg__wsm]
    if isinstance(ftrz__lkmdd, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(ftrz__lkmdd, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for lok__grdt in dxm__cpjio:
        iwmix__tsa = df.data[lok__grdt]
        if isinstance(iwmix__tsa, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or iwmix__tsa == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (gsq__jatk, auqpd__pznw, lrgvz__qbhnh, jfxp__ipjxp, lcg__wsm,
        dxm__cpjio)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (gsq__jatk, auqpd__pznw, lrgvz__qbhnh, flt__uvyvz, lcg__wsm, qovm__vsxzn
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(gsq__jatk) == 0:
        if is_overload_none(data.index.name_typ):
            dce__qszwf = None,
        else:
            dce__qszwf = get_literal_value(data.index.name_typ),
    else:
        dce__qszwf = tuple(gsq__jatk)
    gsq__jatk = ColNamesMetaType(dce__qszwf)
    lrgvz__qbhnh = ColNamesMetaType(tuple(lrgvz__qbhnh))
    auqpd__pznw = ColNamesMetaType((auqpd__pznw,))
    fwih__bfoke = 'def impl(data, index=None, columns=None, values=None):\n'
    fwih__bfoke += "    ev = tracing.Event('df.pivot')\n"
    fwih__bfoke += f'    pivot_values = data.iloc[:, {lcg__wsm}].unique()\n'
    fwih__bfoke += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(flt__uvyvz) == 0:
        fwih__bfoke += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        fwih__bfoke += '        (\n'
        for lfl__bwf in flt__uvyvz:
            fwih__bfoke += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {lfl__bwf}),
"""
        fwih__bfoke += '        ),\n'
    fwih__bfoke += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {lcg__wsm}),),
"""
    fwih__bfoke += '        (\n'
    for lok__grdt in qovm__vsxzn:
        fwih__bfoke += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {lok__grdt}),
"""
    fwih__bfoke += '        ),\n'
    fwih__bfoke += '        pivot_values,\n'
    fwih__bfoke += '        index_lit,\n'
    fwih__bfoke += '        columns_lit,\n'
    fwih__bfoke += '        values_lit,\n'
    fwih__bfoke += '    )\n'
    fwih__bfoke += '    ev.finalize()\n'
    fwih__bfoke += '    return result\n'
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo, 'index_lit': gsq__jatk, 'columns_lit':
        auqpd__pznw, 'values_lit': lrgvz__qbhnh, 'tracing': tracing},
        oeiz__fpxd)
    impl = oeiz__fpxd['impl']
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
    bobbd__oxyz = dict(fill_value=fill_value, margins=margins, dropna=
        dropna, margins_name=margins_name, observed=observed, sort=sort)
    qpsl__yjq = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    (gsq__jatk, auqpd__pznw, lrgvz__qbhnh, flt__uvyvz, lcg__wsm, qovm__vsxzn
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot_table'))
    voocc__mvumt = gsq__jatk
    gsq__jatk = ColNamesMetaType(tuple(gsq__jatk))
    lrgvz__qbhnh = ColNamesMetaType(tuple(lrgvz__qbhnh))
    qkauo__knre = auqpd__pznw
    auqpd__pznw = ColNamesMetaType((auqpd__pznw,))
    fwih__bfoke = 'def impl(\n'
    fwih__bfoke += '    data,\n'
    fwih__bfoke += '    values=None,\n'
    fwih__bfoke += '    index=None,\n'
    fwih__bfoke += '    columns=None,\n'
    fwih__bfoke += '    aggfunc="mean",\n'
    fwih__bfoke += '    fill_value=None,\n'
    fwih__bfoke += '    margins=False,\n'
    fwih__bfoke += '    dropna=True,\n'
    fwih__bfoke += '    margins_name="All",\n'
    fwih__bfoke += '    observed=False,\n'
    fwih__bfoke += '    sort=True,\n'
    fwih__bfoke += '    _pivot_values=None,\n'
    fwih__bfoke += '):\n'
    fwih__bfoke += "    ev = tracing.Event('df.pivot_table')\n"
    klvu__zxmo = flt__uvyvz + [lcg__wsm] + qovm__vsxzn
    fwih__bfoke += f'    data = data.iloc[:, {klvu__zxmo}]\n'
    enbu__tni = voocc__mvumt + [qkauo__knre]
    if not is_overload_none(_pivot_values):
        fgn__uaj = tuple(sorted(_pivot_values.meta))
        _pivot_values = ColNamesMetaType(fgn__uaj)
        fwih__bfoke += '    pivot_values = _pivot_values_arr\n'
        fwih__bfoke += (
            f'    data = data[data.iloc[:, {len(flt__uvyvz)}].isin(pivot_values)]\n'
            )
        if all(isinstance(nacja__xokax, str) for nacja__xokax in fgn__uaj):
            pkbxf__iuql = pd.array(fgn__uaj, 'string')
        elif all(isinstance(nacja__xokax, int) for nacja__xokax in fgn__uaj):
            pkbxf__iuql = np.array(fgn__uaj, 'int64')
        else:
            raise BodoError(
                f'pivot(): pivot values selcected via pivot JIT argument must all share a common int or string type.'
                )
    else:
        pkbxf__iuql = None
    bvdkr__gkzxc = is_overload_constant_str(aggfunc
        ) and get_overload_const_str(aggfunc) == 'nunique'
    yybt__jgtc = len(enbu__tni) if bvdkr__gkzxc else len(voocc__mvumt)
    fwih__bfoke += f"""    data = data.groupby({enbu__tni!r}, as_index=False, _bodo_num_shuffle_keys={yybt__jgtc}).agg(aggfunc)
"""
    if is_overload_none(_pivot_values):
        fwih__bfoke += (
            f'    pivot_values = data.iloc[:, {len(flt__uvyvz)}].unique()\n')
    fwih__bfoke += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    fwih__bfoke += '        (\n'
    for i in range(0, len(flt__uvyvz)):
        fwih__bfoke += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
    fwih__bfoke += '        ),\n'
    fwih__bfoke += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(flt__uvyvz)}),),
"""
    fwih__bfoke += '        (\n'
    for i in range(len(flt__uvyvz) + 1, len(qovm__vsxzn) + len(flt__uvyvz) + 1
        ):
        fwih__bfoke += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
    fwih__bfoke += '        ),\n'
    fwih__bfoke += '        pivot_values,\n'
    fwih__bfoke += '        index_lit,\n'
    fwih__bfoke += '        columns_lit,\n'
    fwih__bfoke += '        values_lit,\n'
    fwih__bfoke += '        check_duplicates=False,\n'
    fwih__bfoke += f'        is_already_shuffled={not bvdkr__gkzxc},\n'
    fwih__bfoke += '        _constant_pivot_values=_constant_pivot_values,\n'
    fwih__bfoke += '    )\n'
    fwih__bfoke += '    ev.finalize()\n'
    fwih__bfoke += '    return result\n'
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo, 'numba': numba, 'index_lit': gsq__jatk,
        'columns_lit': auqpd__pznw, 'values_lit': lrgvz__qbhnh,
        '_pivot_values_arr': pkbxf__iuql, '_constant_pivot_values':
        _pivot_values, 'tracing': tracing}, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
    return impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    bobbd__oxyz = dict(col_level=col_level, ignore_index=ignore_index)
    qpsl__yjq = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', bobbd__oxyz, qpsl__yjq,
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
    lgap__defkf = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(lgap__defkf, (list, tuple)):
        lgap__defkf = [lgap__defkf]
    for nacja__xokax in lgap__defkf:
        if nacja__xokax not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {nacja__xokax} not found in {frame}."
                )
    iph__rfc = [frame.column_index[i] for i in lgap__defkf]
    if is_overload_none(value_vars):
        ifr__lbfg = []
        amc__lzmor = []
        for i, nacja__xokax in enumerate(frame.columns):
            if i not in iph__rfc:
                ifr__lbfg.append(i)
                amc__lzmor.append(nacja__xokax)
    else:
        amc__lzmor = get_literal_value(value_vars)
        if not isinstance(amc__lzmor, (list, tuple)):
            amc__lzmor = [amc__lzmor]
        amc__lzmor = [v for v in amc__lzmor if v not in lgap__defkf]
        if not amc__lzmor:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        ifr__lbfg = []
        for val in amc__lzmor:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            ifr__lbfg.append(frame.column_index[val])
    for nacja__xokax in amc__lzmor:
        if nacja__xokax not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {nacja__xokax} not found in {frame}."
                )
    if not (all(isinstance(nacja__xokax, int) for nacja__xokax in
        amc__lzmor) or all(isinstance(nacja__xokax, str) for nacja__xokax in
        amc__lzmor)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    cquh__vwyk = frame.data[ifr__lbfg[0]]
    tayh__onwtv = [frame.data[i].dtype for i in ifr__lbfg]
    ifr__lbfg = np.array(ifr__lbfg, dtype=np.int64)
    iph__rfc = np.array(iph__rfc, dtype=np.int64)
    _, vstv__tqjb = bodo.utils.typing.get_common_scalar_dtype(tayh__onwtv)
    if not vstv__tqjb:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': amc__lzmor, 'val_type': cquh__vwyk}
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
    if frame.is_table_format and all(v == cquh__vwyk.dtype for v in tayh__onwtv
        ):
        extra_globals['value_idxs'] = bodo.utils.typing.MetaType(tuple(
            ifr__lbfg))
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(amc__lzmor) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {ifr__lbfg[0]})
"""
    else:
        yxqww__iqw = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in ifr__lbfg)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({yxqww__iqw},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in iph__rfc:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(amc__lzmor)})\n'
            )
    gtn__jos = ', '.join(f'out_id{i}' for i in iph__rfc) + (', ' if len(
        iph__rfc) > 0 else '')
    data_args = gtn__jos + 'var_col, val_col'
    columns = tuple(lgap__defkf + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(amc__lzmor)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    raise BodoError(f'pandas.crosstab() not supported yet')
    bobbd__oxyz = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    qpsl__yjq = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', bobbd__oxyz, qpsl__yjq,
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
    bobbd__oxyz = dict(ignore_index=ignore_index, key=key)
    qpsl__yjq = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', bobbd__oxyz, qpsl__yjq,
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
    yxsaa__dly = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        yxsaa__dly.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        hgf__mtmh = [get_overload_const_tuple(by)]
    else:
        hgf__mtmh = get_overload_const_list(by)
    hgf__mtmh = set((k, '') if (k, '') in yxsaa__dly else k for k in hgf__mtmh)
    if len(hgf__mtmh.difference(yxsaa__dly)) > 0:
        yxp__wtegg = list(set(get_overload_const_list(by)).difference(
            yxsaa__dly))
        raise_bodo_error(f'sort_values(): invalid keys {yxp__wtegg} for by.')
    if not is_overload_none(_bodo_chunk_bounds) and len(hgf__mtmh) != 1:
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
        qfsl__kec = get_overload_const_list(na_position)
        for na_position in qfsl__kec:
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
    bobbd__oxyz = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    qpsl__yjq = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', bobbd__oxyz, qpsl__yjq,
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
    fwih__bfoke = """def impl(df, axis=0, method='average', numeric_only=None, na_option='keep', ascending=True, pct=False):
"""
    bkyvw__zhagt = len(df.columns)
    data_args = ', '.join(
        'bodo.libs.array_kernels.rank(data_{}, method=method, na_option=na_option, ascending=ascending, pct=pct)'
        .format(i) for i in range(bkyvw__zhagt))
    for i in range(bkyvw__zhagt):
        fwih__bfoke += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(fwih__bfoke, df.columns, data_args, index)


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    bobbd__oxyz = dict(limit=limit, downcast=downcast)
    qpsl__yjq = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', bobbd__oxyz, qpsl__yjq,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    goz__qgjb = not is_overload_none(value)
    unc__twjz = not is_overload_none(method)
    if goz__qgjb and unc__twjz:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not goz__qgjb and not unc__twjz:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if goz__qgjb:
        zeabk__dloin = 'value=value'
    else:
        zeabk__dloin = 'method=method'
    data_args = [(
        f"df['{nacja__xokax}'].fillna({zeabk__dloin}, inplace=inplace)" if
        isinstance(nacja__xokax, str) else
        f'df[{nacja__xokax}].fillna({zeabk__dloin}, inplace=inplace)') for
        nacja__xokax in df.columns]
    fwih__bfoke = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        fwih__bfoke += '  ' + '  \n'.join(data_args) + '\n'
        oeiz__fpxd = {}
        exec(fwih__bfoke, {}, oeiz__fpxd)
        impl = oeiz__fpxd['impl']
        return impl
    else:
        return _gen_init_df(fwih__bfoke, df.columns, ', '.join(xjvus__vjv +
            '.values' for xjvus__vjv in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    bobbd__oxyz = dict(col_level=col_level, col_fill=col_fill)
    qpsl__yjq = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', bobbd__oxyz, qpsl__yjq,
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
    fwih__bfoke = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    fwih__bfoke += (
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
        rqp__mqfm = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            rqp__mqfm)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            fwih__bfoke += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            ari__haml = ['m_index[{}]'.format(i) for i in range(df.index.
                nlevels)]
            data_args = ari__haml + data_args
        else:
            nacg__bow = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [nacg__bow] + data_args
    return _gen_init_df(fwih__bfoke, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    inftm__mrr = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and inftm__mrr == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(inftm__mrr))


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
        bloo__znxwr = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        okefi__yfg = get_overload_const_list(subset)
        bloo__znxwr = []
        for muru__nrws in okefi__yfg:
            if muru__nrws not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{muru__nrws}' not in data frame columns {df}"
                    )
            bloo__znxwr.append(df.column_index[muru__nrws])
    bkyvw__zhagt = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(bkyvw__zhagt))
    fwih__bfoke = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(bkyvw__zhagt):
        fwih__bfoke += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    fwih__bfoke += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in bloo__znxwr)))
    fwih__bfoke += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(fwih__bfoke, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    bobbd__oxyz = dict(index=index, level=level, errors=errors)
    qpsl__yjq = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', bobbd__oxyz, qpsl__yjq,
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
            bnb__ilanz = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            bnb__ilanz = get_overload_const_list(labels)
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
            bnb__ilanz = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            bnb__ilanz = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for nacja__xokax in bnb__ilanz:
        if nacja__xokax not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(nacja__xokax, df.columns))
    if len(set(bnb__ilanz)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    dgfg__tcbu = tuple(nacja__xokax for nacja__xokax in df.columns if 
        nacja__xokax not in bnb__ilanz)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[nacja__xokax], '.copy()' if not inplace else
        '') for nacja__xokax in dgfg__tcbu)
    fwih__bfoke = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    fwih__bfoke += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(fwih__bfoke, dgfg__tcbu, data_args, index)


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
    bobbd__oxyz = dict(random_state=random_state, weights=weights, axis=
        axis, ignore_index=ignore_index)
    jztpf__svhf = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', bobbd__oxyz, jztpf__svhf,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    bkyvw__zhagt = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(bkyvw__zhagt))
    yntg__kuz = ', '.join('rhs_data_{}'.format(i) for i in range(bkyvw__zhagt))
    fwih__bfoke = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    fwih__bfoke += '  if (frac == 1 or n == len(df)) and not replace:\n'
    fwih__bfoke += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(bkyvw__zhagt):
        fwih__bfoke += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    fwih__bfoke += '  if frac is None:\n'
    fwih__bfoke += '    frac_d = -1.0\n'
    fwih__bfoke += '  else:\n'
    fwih__bfoke += '    frac_d = frac\n'
    fwih__bfoke += '  if n is None:\n'
    fwih__bfoke += '    n_i = 0\n'
    fwih__bfoke += '  else:\n'
    fwih__bfoke += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    fwih__bfoke += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({yntg__kuz},), {index}, n_i, frac_d, replace)
"""
    fwih__bfoke += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(fwih__bfoke, df.
        columns, data_args, 'index')


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
    rbway__vuecn = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    bjxj__cnb = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', rbway__vuecn, bjxj__cnb,
        package_name='pandas', module_name='DataFrame')
    tof__gluc = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            djz__lun = tof__gluc + '\n'
            djz__lun += 'Index: 0 entries\n'
            djz__lun += 'Empty DataFrame'
            print(djz__lun)
        return _info_impl
    else:
        fwih__bfoke = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        fwih__bfoke += '    ncols = df.shape[1]\n'
        fwih__bfoke += f'    lines = "{tof__gluc}\\n"\n'
        fwih__bfoke += f'    lines += "{df.index}: "\n'
        fwih__bfoke += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            fwih__bfoke += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            fwih__bfoke += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            fwih__bfoke += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        fwih__bfoke += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        fwih__bfoke += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        fwih__bfoke += '    column_width = max(space, 7)\n'
        fwih__bfoke += '    column= "Column"\n'
        fwih__bfoke += '    underl= "------"\n'
        fwih__bfoke += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        fwih__bfoke += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        fwih__bfoke += '    mem_size = 0\n'
        fwih__bfoke += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        fwih__bfoke += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        fwih__bfoke += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        jref__yvby = dict()
        for i in range(len(df.columns)):
            fwih__bfoke += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            qww__fhtoh = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                qww__fhtoh = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                bnjgk__tedd = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                qww__fhtoh = f'{bnjgk__tedd[:-7]}'
            fwih__bfoke += f'    col_dtype[{i}] = "{qww__fhtoh}"\n'
            if qww__fhtoh in jref__yvby:
                jref__yvby[qww__fhtoh] += 1
            else:
                jref__yvby[qww__fhtoh] = 1
            fwih__bfoke += f'    col_name[{i}] = "{df.columns[i]}"\n'
            fwih__bfoke += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        fwih__bfoke += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        fwih__bfoke += '    for i in column_info:\n'
        fwih__bfoke += "        lines += f'{i}\\n'\n"
        sox__hpb = ', '.join(f'{k}({jref__yvby[k]})' for k in sorted(
            jref__yvby))
        fwih__bfoke += f"    lines += 'dtypes: {sox__hpb}\\n'\n"
        fwih__bfoke += '    mem_size += df.index.nbytes\n'
        fwih__bfoke += '    total_size = _sizeof_fmt(mem_size)\n'
        fwih__bfoke += "    lines += f'memory usage: {total_size}'\n"
        fwih__bfoke += '    print(lines)\n'
        oeiz__fpxd = {}
        exec(fwih__bfoke, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, oeiz__fpxd)
        _info_impl = oeiz__fpxd['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    fwih__bfoke = 'def impl(df, index=True, deep=False):\n'
    gssq__nrp = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes'
    hfhq__ckjcg = is_overload_true(index)
    columns = df.columns
    if hfhq__ckjcg:
        columns = ('Index',) + columns
    if len(columns) == 0:
        klaap__rbe = ()
    elif all(isinstance(nacja__xokax, int) for nacja__xokax in columns):
        klaap__rbe = np.array(columns, 'int64')
    elif all(isinstance(nacja__xokax, str) for nacja__xokax in columns):
        klaap__rbe = pd.array(columns, 'string')
    else:
        klaap__rbe = columns
    if df.is_table_format and len(df.columns) > 0:
        dkis__lhwnr = int(hfhq__ckjcg)
        yrqoe__busp = len(columns)
        fwih__bfoke += f'  nbytes_arr = np.empty({yrqoe__busp}, np.int64)\n'
        fwih__bfoke += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        fwih__bfoke += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {dkis__lhwnr})
"""
        if hfhq__ckjcg:
            fwih__bfoke += f'  nbytes_arr[0] = {gssq__nrp}\n'
        fwih__bfoke += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if hfhq__ckjcg:
            data = f'{gssq__nrp},{data}'
        else:
            irhq__kdbkr = ',' if len(columns) == 1 else ''
            data = f'{data}{irhq__kdbkr}'
        fwih__bfoke += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        klaap__rbe}, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
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
    fel__kcszw = 'read_excel_df{}'.format(next_label())
    setattr(types, fel__kcszw, df_type)
    kxn__adtfb = False
    if is_overload_constant_list(parse_dates):
        kxn__adtfb = get_overload_const_list(parse_dates)
    zvbg__scu = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    fwih__bfoke = f"""
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
    with numba.objmode(df="{fel__kcszw}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{zvbg__scu}}},
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
            parse_dates={kxn__adtfb},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    oeiz__fpxd = {}
    exec(fwih__bfoke, globals(), oeiz__fpxd)
    impl = oeiz__fpxd['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as gubv__ibtrr:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    fwih__bfoke = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    fwih__bfoke += (
        '    ylabel=None, title=None, legend=True, fontsize=None, \n')
    fwih__bfoke += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        fwih__bfoke += '   fig, ax = plt.subplots()\n'
    else:
        fwih__bfoke += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        fwih__bfoke += '   fig.set_figwidth(figsize[0])\n'
        fwih__bfoke += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        fwih__bfoke += '   xlabel = x\n'
    fwih__bfoke += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        fwih__bfoke += '   ylabel = y\n'
    else:
        fwih__bfoke += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        fwih__bfoke += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        fwih__bfoke += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    fwih__bfoke += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            fwih__bfoke += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            bxrb__ijzrj = get_overload_const_str(x)
            skyc__dug = df.columns.index(bxrb__ijzrj)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if skyc__dug != i:
                        fwih__bfoke += f"""   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])
"""
        else:
            fwih__bfoke += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        fwih__bfoke += '   ax.scatter(df[x], df[y], s=20)\n'
        fwih__bfoke += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        fwih__bfoke += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        fwih__bfoke += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        fwih__bfoke += '   ax.legend()\n'
    fwih__bfoke += '   return ax\n'
    oeiz__fpxd = {}
    exec(fwih__bfoke, {'bodo': bodo, 'plt': plt}, oeiz__fpxd)
    impl = oeiz__fpxd['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for uqklu__leo in df_typ.data:
        if not (isinstance(uqklu__leo, (IntegerArrayType, FloatingArrayType
            )) or isinstance(uqklu__leo.dtype, types.Number) or uqklu__leo.
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
        qdulj__kse = args[0]
        ckak__jvq = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        bxye__mbu = qdulj__kse
        check_runtime_cols_unsupported(qdulj__kse, 'set_df_col()')
        if isinstance(qdulj__kse, DataFrameType):
            index = qdulj__kse.index
            if len(qdulj__kse.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(qdulj__kse.columns) == 0:
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
            if ckak__jvq in qdulj__kse.columns:
                dgfg__tcbu = qdulj__kse.columns
                rtmr__kvlkk = qdulj__kse.columns.index(ckak__jvq)
                vkyae__gmnmu = list(qdulj__kse.data)
                vkyae__gmnmu[rtmr__kvlkk] = val
                vkyae__gmnmu = tuple(vkyae__gmnmu)
            else:
                dgfg__tcbu = qdulj__kse.columns + (ckak__jvq,)
                vkyae__gmnmu = qdulj__kse.data + (val,)
            bxye__mbu = DataFrameType(vkyae__gmnmu, index, dgfg__tcbu,
                qdulj__kse.dist, qdulj__kse.is_table_format)
        return bxye__mbu(*args)


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
        cdgmt__qjdpl = args[0]
        assert isinstance(cdgmt__qjdpl, DataFrameType) and len(cdgmt__qjdpl
            .columns
            ) > 0, 'Error while typechecking __bodosql_replace_columns_dummy: we should only generate a call __bodosql_replace_columns_dummy if the input dataframe'
        col_names_to_replace = get_overload_const_tuple(args[1])
        djnwm__fjj = args[2]
        assert len(col_names_to_replace) == len(djnwm__fjj
            ), 'Error while typechecking __bodosql_replace_columns_dummy: the tuple of column indicies to replace should be equal to the number of columns to replace them with'
        assert len(col_names_to_replace) <= len(cdgmt__qjdpl.columns
            ), 'Error while typechecking __bodosql_replace_columns_dummy: The number of indicies provided should be less than or equal to the number of columns in the input dataframe'
        for col_name in col_names_to_replace:
            assert col_name in cdgmt__qjdpl.columns, 'Error while typechecking __bodosql_replace_columns_dummy: All columns specified to be replaced should already be present in input dataframe'
        check_runtime_cols_unsupported(cdgmt__qjdpl,
            '__bodosql_replace_columns_dummy()')
        index = cdgmt__qjdpl.index
        dgfg__tcbu = cdgmt__qjdpl.columns
        vkyae__gmnmu = list(cdgmt__qjdpl.data)
        for i in range(len(col_names_to_replace)):
            col_name = col_names_to_replace[i]
            yfv__ztvnr = djnwm__fjj[i]
            assert isinstance(yfv__ztvnr, SeriesType
                ), 'Error while typechecking __bodosql_replace_columns_dummy: the values to replace the columns with are expected to be series'
            if isinstance(yfv__ztvnr, SeriesType):
                yfv__ztvnr = yfv__ztvnr.data
            usetq__zsst = cdgmt__qjdpl.column_index[col_name]
            vkyae__gmnmu[usetq__zsst] = yfv__ztvnr
        vkyae__gmnmu = tuple(vkyae__gmnmu)
        bxye__mbu = DataFrameType(vkyae__gmnmu, index, dgfg__tcbu,
            cdgmt__qjdpl.dist, cdgmt__qjdpl.is_table_format)
        return bxye__mbu(*args)


BodoSQLReplaceColsInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    apo__rdde = {}

    def _rewrite_membership_op(self, node, left, right):
        kzkoe__wazaf = node.op
        op = self.visit(kzkoe__wazaf)
        return op, kzkoe__wazaf, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    mniu__zfk = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in mniu__zfk:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in mniu__zfk:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing('(' + self.name + ')')

    def visit_Attribute(self, node, **kwargs):
        mkv__gcz = node.attr
        value = node.value
        dorjz__pdk = pd.core.computation.ops.LOCAL_TAG
        if mkv__gcz in ('str', 'dt'):
            try:
                musrd__qeafb = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as arx__nhnzs:
                col_name = arx__nhnzs.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            musrd__qeafb = str(self.visit(value))
        bfd__aisle = musrd__qeafb, mkv__gcz
        if bfd__aisle in join_cleaned_cols:
            mkv__gcz = join_cleaned_cols[bfd__aisle]
        name = musrd__qeafb + '.' + mkv__gcz
        if name.startswith(dorjz__pdk):
            name = name[len(dorjz__pdk):]
        if mkv__gcz in ('str', 'dt'):
            fsio__oklc = columns[cleaned_columns.index(musrd__qeafb)]
            apo__rdde[fsio__oklc] = musrd__qeafb
            self.env.scope[name] = 0
            return self.term_type(dorjz__pdk + name, self.env)
        mniu__zfk.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in mniu__zfk:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        golnl__lpj = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        ckak__jvq = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(golnl__lpj), ckak__jvq))

    def op__str__(self):
        fgjf__denp = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            mvat__ilav)) for mvat__ilav in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(fgjf__denp)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(fgjf__denp)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(fgjf__denp))
    tiykw__nssnh = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    pmh__hztof = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    juuu__vgon = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    kwod__bxir = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    czxoc__ejx = pd.core.computation.ops.Term.__str__
    wilwr__dyonc = pd.core.computation.ops.MathCall.__str__
    xct__ykq = pd.core.computation.ops.Op.__str__
    fxu__tfl = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
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
        hxye__qlcr = pd.core.computation.expr.Expr(expr, env=env)
        smrmu__wem = str(hxye__qlcr)
    except pd.core.computation.ops.UndefinedVariableError as arx__nhnzs:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == arx__nhnzs.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {arx__nhnzs}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            tiykw__nssnh)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            pmh__hztof)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = juuu__vgon
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = kwod__bxir
        pd.core.computation.ops.Term.__str__ = czxoc__ejx
        pd.core.computation.ops.MathCall.__str__ = wilwr__dyonc
        pd.core.computation.ops.Op.__str__ = xct__ykq
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = fxu__tfl
    urqmg__txogq = pd.core.computation.parsing.clean_column_name
    apo__rdde.update({nacja__xokax: urqmg__txogq(nacja__xokax) for
        nacja__xokax in columns if urqmg__txogq(nacja__xokax) in hxye__qlcr
        .names})
    return hxye__qlcr, smrmu__wem, apo__rdde


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        gmxt__udqpg = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(gmxt__udqpg))
        cix__qkfhy = namedtuple('Pandas', col_names)
        aeavi__ypzol = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], cix__qkfhy)
        super(DataFrameTupleIterator, self).__init__(name, aeavi__ypzol)

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
        rie__enzn = [if_series_to_array_type(a) for a in args[len(args) // 2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        rie__enzn = [types.Array(types.int64, 1, 'C')] + rie__enzn
        wxwh__dkr = DataFrameTupleIterator(col_names, rie__enzn)
        return wxwh__dkr(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jvtb__cyzr = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            jvtb__cyzr)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    xkewz__xqam = args[len(args) // 2:]
    ihsos__ncd = sig.args[len(sig.args) // 2:]
    xco__ilv = context.make_helper(builder, sig.return_type)
    iipdn__zfc = context.get_constant(types.intp, 0)
    dzo__qsg = cgutils.alloca_once_value(builder, iipdn__zfc)
    xco__ilv.index = dzo__qsg
    for i, arr in enumerate(xkewz__xqam):
        setattr(xco__ilv, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(xkewz__xqam, ihsos__ncd):
        context.nrt.incref(builder, arr_typ, arr)
    res = xco__ilv._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    hcmi__pipj, = sig.args
    ovye__atw, = args
    xco__ilv = context.make_helper(builder, hcmi__pipj, value=ovye__atw)
    riiz__nqc = signature(types.intp, hcmi__pipj.array_types[1])
    zaslh__cayr = context.compile_internal(builder, lambda a: len(a),
        riiz__nqc, [xco__ilv.array0])
    index = builder.load(xco__ilv.index)
    owuge__ksqg = builder.icmp_signed('<', index, zaslh__cayr)
    result.set_valid(owuge__ksqg)
    with builder.if_then(owuge__ksqg):
        values = [index]
        for i, arr_typ in enumerate(hcmi__pipj.array_types[1:]):
            xdd__rnoom = getattr(xco__ilv, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                lvzyj__pkc = signature(pd_timestamp_tz_naive_type, arr_typ,
                    types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    lvzyj__pkc, [xdd__rnoom, index])
            else:
                lvzyj__pkc = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    lvzyj__pkc, [xdd__rnoom, index])
            values.append(val)
        value = context.make_tuple(builder, hcmi__pipj.yield_type, values)
        result.yield_(value)
        jem__kknu = cgutils.increment_index(builder, index)
        builder.store(jem__kknu, xco__ilv.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    ymqnv__bnxs = ir.Assign(rhs, lhs, expr.loc)
    brn__hidpd = lhs
    qexnv__sjlcd = []
    niyz__kux = []
    cwgzp__citu = typ.count
    for i in range(cwgzp__citu):
        avwu__zptks = ir.Var(brn__hidpd.scope, mk_unique_var('{}_size{}'.
            format(brn__hidpd.name, i)), brn__hidpd.loc)
        nsrjd__okwgj = ir.Expr.static_getitem(lhs, i, None, brn__hidpd.loc)
        self.calltypes[nsrjd__okwgj] = None
        qexnv__sjlcd.append(ir.Assign(nsrjd__okwgj, avwu__zptks, brn__hidpd
            .loc))
        self._define(equiv_set, avwu__zptks, types.intp, nsrjd__okwgj)
        niyz__kux.append(avwu__zptks)
    jpdm__xrna = tuple(niyz__kux)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        jpdm__xrna, pre=[ymqnv__bnxs] + qexnv__sjlcd)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
