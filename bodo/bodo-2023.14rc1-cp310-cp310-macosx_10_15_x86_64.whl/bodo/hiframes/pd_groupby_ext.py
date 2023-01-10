"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_null_shuffle_info, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.float_arr_ext import FloatDtype, FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_bool, get_overload_const_func, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, to_nullable_type, to_numeric_index_if_range_index, to_str_arr_if_dict_array
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False, _num_shuffle_keys=-1):
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        self._num_shuffle_keys = _num_shuffle_keys
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select}, {_num_shuffle_keys})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select, self._num_shuffle_keys)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jonhk__qfg = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, jonhk__qfg)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_bodo_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type, dropna_type,
    _num_shuffle_keys):

    def codegen(context, builder, signature, args):
        faa__lgnh = args[0]
        xtas__cdq = signature.return_type
        qtsaj__mpv = cgutils.create_struct_proxy(xtas__cdq)(context, builder)
        qtsaj__mpv.obj = faa__lgnh
        context.nrt.incref(builder, signature.args[0], faa__lgnh)
        return qtsaj__mpv._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for lers__gtr in keys:
        selection.remove(lers__gtr)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        jloi__ibujc = get_overload_const_int(_num_shuffle_keys)
    else:
        jloi__ibujc = -1
    xtas__cdq = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=jloi__ibujc)
    return xtas__cdq(obj_type, by_type, as_index_type, dropna_type,
        _num_shuffle_keys), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
@lower_builtin('groupby.agg', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, nvcug__ukhns = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(nvcug__ukhns, (tuple, list)):
                if len(set(nvcug__ukhns).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(nvcug__ukhns).difference(set(grpby.
                        df_type.columns))))
                selection = nvcug__ukhns
            else:
                if nvcug__ukhns not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(nvcug__ukhns))
                selection = nvcug__ukhns,
                series_select = True
            cmyr__ujgpp = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(cmyr__ujgpp, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, nvcug__ukhns = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            nvcug__ukhns):
            cmyr__ujgpp = StaticGetItemDataFrameGroupBy.generic(self, (
                grpby, get_literal_value(nvcug__ukhns)), {}).return_type
            return signature(cmyr__ujgpp, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    zchs__fratq = arr_type == ArrayItemArrayType(string_array_type)
    mlu__ork = arr_type.dtype
    if isinstance(mlu__ork, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {mlu__ork} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(mlu__ork, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    elif func_name in ('first', 'last', 'sum', 'prod', 'min', 'max',
        'count', 'nunique', 'head') and isinstance(arr_type, (
        TupleArrayType, ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {mlu__ork} is not supported in groupby built-in function {func_name}'
            )
    elif func_name in {'median', 'mean', 'var', 'std'} and isinstance(mlu__ork,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    elif func_name == 'boolor_agg':
        if isinstance(mlu__ork, (Decimal128Type, types.Integer, types.Float,
            types.Boolean)):
            return bodo.boolean_array, 'ok'
        return (None,
            f'For boolor_agg, only columns of type integer, float, Decimal, or boolean type are allowed'
            )
    if not isinstance(mlu__ork, (types.Integer, types.Float, types.Boolean)):
        if zchs__fratq or mlu__ork == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(mlu__ork, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not mlu__ork.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {mlu__ork} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(mlu__ork, types.Boolean) and func_name in {'cumsum',
        'mean', 'sum', 'std', 'var'}:
        if func_name in {'sum'}:
            return to_nullable_type(dtype_to_array_type(types.int64)), 'ok'
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    elif func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    elif func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    mlu__ork = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(mlu__ork, (types
            .Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(mlu__ork, types.Integer):
            return IntDtype(mlu__ork)
        return mlu__ork
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        cmo__sqln = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{cmo__sqln}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for lers__gtr in grp.keys:
        if multi_level_names:
            msq__uvnt = lers__gtr, ''
        else:
            msq__uvnt = lers__gtr
        dlrw__vbb = grp.df_type.column_index[lers__gtr]
        data = grp.df_type.data[dlrw__vbb]
        out_columns.append(msq__uvnt)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None, raise_on_any_error=False):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if func_name in ('head', 'ngroup'):
        grp.as_index = True
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif func_name in ('head', 'ngroup'):
        if grp.df_type.index == index:
            index = NumericIndexType(types.int64, types.none)
        else:
            index = grp.df_type.index
    elif len(grp.keys) > 1:
        lhnl__xtzu = tuple(grp.df_type.column_index[grp.keys[ydnh__nzmtt]] for
            ydnh__nzmtt in range(len(grp.keys)))
        slwht__zod = tuple(grp.df_type.data[dlrw__vbb] for dlrw__vbb in
            lhnl__xtzu)
        index = MultiIndexType(slwht__zod, tuple(types.StringLiteral(
            lers__gtr) for lers__gtr in grp.keys))
    else:
        dlrw__vbb = grp.df_type.column_index[grp.keys[0]]
        txmke__upkbz = grp.df_type.data[dlrw__vbb]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(txmke__upkbz,
            types.StringLiteral(grp.keys[0]))
    wlhwd__hnc = {}
    llk__udy = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        wlhwd__hnc[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        wlhwd__hnc[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        hqgxq__iwh = dict(ascending=ascending)
        zsuxt__atvcn = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', hqgxq__iwh,
            zsuxt__atvcn, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for wxlgv__wqod in columns:
            dlrw__vbb = grp.df_type.column_index[wxlgv__wqod]
            data = grp.df_type.data[dlrw__vbb]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            gzkkw__klf = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType,
                FloatingArrayType)) and isinstance(data.dtype, (types.
                Integer, types.Float)):
                gzkkw__klf = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    yecod__klo = SeriesType(data.dtype, data, None, string_type
                        )
                    isul__efcvm = get_const_func_output_type(func, (
                        yecod__klo,), {}, typing_context, target_context)
                    if isul__efcvm != ArrayItemArrayType(string_array_type):
                        isul__efcvm = dtype_to_array_type(isul__efcvm)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=wxlgv__wqod, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    ckank__ieyc = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    tmpix__zmfh = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    hqgxq__iwh = dict(numeric_only=ckank__ieyc, min_count=
                        tmpix__zmfh)
                    zsuxt__atvcn = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hqgxq__iwh, zsuxt__atvcn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    ckank__ieyc = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    tmpix__zmfh = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    hqgxq__iwh = dict(numeric_only=ckank__ieyc, min_count=
                        tmpix__zmfh)
                    zsuxt__atvcn = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hqgxq__iwh, zsuxt__atvcn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    ckank__ieyc = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    hqgxq__iwh = dict(numeric_only=ckank__ieyc)
                    zsuxt__atvcn = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hqgxq__iwh, zsuxt__atvcn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    ltaep__ktsn = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    ngo__rdbyz = args[1] if len(args) > 1 else kws.pop('skipna'
                        , True)
                    hqgxq__iwh = dict(axis=ltaep__ktsn, skipna=ngo__rdbyz)
                    zsuxt__atvcn = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hqgxq__iwh, zsuxt__atvcn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    gkov__gknvy = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    hqgxq__iwh = dict(ddof=gkov__gknvy)
                    zsuxt__atvcn = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        hqgxq__iwh, zsuxt__atvcn, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                isul__efcvm, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                isul__efcvm = to_str_arr_if_dict_array(isul__efcvm
                    ) if func_name in ('sum', 'cumsum') else isul__efcvm
                out_data.append(isul__efcvm)
                out_columns.append(wxlgv__wqod)
                if func_name == 'agg':
                    vjvq__sjxdf = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    wlhwd__hnc[wxlgv__wqod, vjvq__sjxdf] = wxlgv__wqod
                else:
                    wlhwd__hnc[wxlgv__wqod, func_name] = wxlgv__wqod
                out_column_type.append(gzkkw__klf)
            elif raise_on_any_error:
                raise BodoError(
                    f'Groupby with function {func_name} not supported. Error message: {err_msg}'
                    )
            else:
                llk__udy.append(err_msg)
    if func_name == 'sum':
        snv__birc = any([(fdo__qjd == ColumnType.NumericalColumn.value) for
            fdo__qjd in out_column_type])
        if snv__birc:
            out_data = [fdo__qjd for fdo__qjd, rga__uywi in zip(out_data,
                out_column_type) if rga__uywi != ColumnType.
                NonNumericalColumn.value]
            out_columns = [fdo__qjd for fdo__qjd, rga__uywi in zip(
                out_columns, out_column_type) if rga__uywi != ColumnType.
                NonNumericalColumn.value]
            wlhwd__hnc = {}
            for wxlgv__wqod in out_columns:
                if grp.as_index is False and wxlgv__wqod in grp.keys:
                    continue
                wlhwd__hnc[wxlgv__wqod, func_name] = wxlgv__wqod
    xba__kxy = len(llk__udy)
    if len(out_data) == 0:
        if xba__kxy == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(xba__kxy, ' was' if xba__kxy == 1 else 's were',
                ','.join(llk__udy)))
    uqcv__fwszl = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            rbq__oip = IntDtype(out_data[0].dtype)
        elif isinstance(out_data[0], FloatingArrayType):
            rbq__oip = FloatDtype(out_data[0].dtype)
        else:
            rbq__oip = out_data[0].dtype
        qeooa__yhsyr = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        uqcv__fwszl = SeriesType(rbq__oip, data=out_data[0], index=index,
            name_typ=qeooa__yhsyr)
    return signature(uqcv__fwszl, *args), wlhwd__hnc


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context,
    target_context, raise_on_any_error):
    lfiw__rdfbx = True
    if isinstance(f_val, str):
        lfiw__rdfbx = False
        mquup__dfvi = f_val
    elif is_overload_constant_str(f_val):
        lfiw__rdfbx = False
        mquup__dfvi = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        lfiw__rdfbx = False
        mquup__dfvi = bodo.utils.typing.get_builtin_function_name(f_val)
    if not lfiw__rdfbx:
        if mquup__dfvi not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {mquup__dfvi}')
        cmyr__ujgpp = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(cmyr__ujgpp, (), mquup__dfvi, typing_context,
            target_context, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    else:
        if is_expr(f_val, 'make_function'):
            tnmtk__ypd = types.functions.MakeFunctionLiteral(f_val)
        else:
            tnmtk__ypd = f_val
        validate_udf('agg', tnmtk__ypd)
        func = get_overload_const_func(tnmtk__ypd, None)
        hab__gbxut = func.code if hasattr(func, 'code') else func.__code__
        mquup__dfvi = hab__gbxut.co_name
        cmyr__ujgpp = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(cmyr__ujgpp, (), 'agg', typing_context,
            target_context, tnmtk__ypd, raise_on_any_error=raise_on_any_error)[
            0].return_type
    return mquup__dfvi, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    moyet__pefn = kws and all(isinstance(ypoqx__clxbt, types.Tuple) and len
        (ypoqx__clxbt) == 2 for ypoqx__clxbt in kws.values())
    raise_on_any_error = moyet__pefn
    if is_overload_none(func) and not moyet__pefn:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not moyet__pefn:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    tqih__dzhno = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if moyet__pefn or is_overload_constant_dict(func):
        if moyet__pefn:
            mncrr__wfq = [get_literal_value(xbxaz__dye) for xbxaz__dye,
                meffp__fddjo in kws.values()]
            iwsw__sqtp = [get_literal_value(vtuqa__eohrt) for meffp__fddjo,
                vtuqa__eohrt in kws.values()]
        else:
            zvmh__cvl = get_overload_constant_dict(func)
            mncrr__wfq = tuple(zvmh__cvl.keys())
            iwsw__sqtp = tuple(zvmh__cvl.values())
        for bpv__arb in ('head', 'ngroup'):
            if bpv__arb in iwsw__sqtp:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {bpv__arb} cannot be mixed with other groupby operations.'
                    )
        if any(wxlgv__wqod not in grp.selection and wxlgv__wqod not in grp.
            keys for wxlgv__wqod in mncrr__wfq):
            raise_bodo_error(
                f'Selected column names {mncrr__wfq} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            iwsw__sqtp)
        if moyet__pefn and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        wlhwd__hnc = {}
        out_columns = []
        out_data = []
        out_column_type = []
        bhv__syyj = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for bnr__xii, f_val in zip(mncrr__wfq, iwsw__sqtp):
            if isinstance(f_val, (tuple, list)):
                quu__vgxw = 0
                for tnmtk__ypd in f_val:
                    mquup__dfvi, out_tp = get_agg_funcname_and_outtyp(grp,
                        bnr__xii, tnmtk__ypd, typing_context,
                        target_context, raise_on_any_error)
                    tqih__dzhno = mquup__dfvi in list_cumulative
                    if mquup__dfvi == '<lambda>' and len(f_val) > 1:
                        mquup__dfvi = '<lambda_' + str(quu__vgxw) + '>'
                        quu__vgxw += 1
                    out_columns.append((bnr__xii, mquup__dfvi))
                    wlhwd__hnc[bnr__xii, mquup__dfvi] = bnr__xii, mquup__dfvi
                    _append_out_type(grp, out_data, out_tp)
            else:
                mquup__dfvi, out_tp = get_agg_funcname_and_outtyp(grp,
                    bnr__xii, f_val, typing_context, target_context,
                    raise_on_any_error)
                tqih__dzhno = mquup__dfvi in list_cumulative
                if multi_level_names:
                    out_columns.append((bnr__xii, mquup__dfvi))
                    wlhwd__hnc[bnr__xii, mquup__dfvi] = bnr__xii, mquup__dfvi
                elif not moyet__pefn:
                    out_columns.append(bnr__xii)
                    wlhwd__hnc[bnr__xii, mquup__dfvi] = bnr__xii
                elif moyet__pefn:
                    bhv__syyj.append(mquup__dfvi)
                _append_out_type(grp, out_data, out_tp)
        if moyet__pefn:
            for ydnh__nzmtt, comp__gllsd in enumerate(kws.keys()):
                out_columns.append(comp__gllsd)
                wlhwd__hnc[mncrr__wfq[ydnh__nzmtt], bhv__syyj[ydnh__nzmtt]
                    ] = comp__gllsd
        if tqih__dzhno:
            index = grp.df_type.index
        else:
            index = out_tp.index
        uqcv__fwszl = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(uqcv__fwszl, *args), wlhwd__hnc
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            bfbsv__jngm = get_overload_const_list(func)
        else:
            bfbsv__jngm = func.types
        if len(bfbsv__jngm) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        quu__vgxw = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        wlhwd__hnc = {}
        fdk__fkoug = grp.selection[0]
        for f_val in bfbsv__jngm:
            mquup__dfvi, out_tp = get_agg_funcname_and_outtyp(grp,
                fdk__fkoug, f_val, typing_context, target_context,
                raise_on_any_error)
            tqih__dzhno = mquup__dfvi in list_cumulative
            if mquup__dfvi == '<lambda>' and len(bfbsv__jngm) > 1:
                mquup__dfvi = '<lambda_' + str(quu__vgxw) + '>'
                quu__vgxw += 1
            out_columns.append(mquup__dfvi)
            wlhwd__hnc[fdk__fkoug, mquup__dfvi] = mquup__dfvi
            _append_out_type(grp, out_data, out_tp)
        if tqih__dzhno:
            index = grp.df_type.index
        else:
            index = out_tp.index
        uqcv__fwszl = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(uqcv__fwszl, *args), wlhwd__hnc
    mquup__dfvi = ''
    if types.unliteral(func) == types.unicode_type:
        mquup__dfvi = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        mquup__dfvi = bodo.utils.typing.get_builtin_function_name(func)
    if mquup__dfvi:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, mquup__dfvi, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = to_numeric_index_if_range_index(grp.df_type.index)
    if isinstance(index, MultiIndexType):
        raise_bodo_error(
            f'Groupby.{name_operation}: MultiIndex input not supported for groupby operations that use input Index'
            )
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        ltaep__ktsn = args[0] if len(args) > 0 else kws.pop('axis', 0)
        ckank__ieyc = args[1] if len(args) > 1 else kws.pop('numeric_only',
            False)
        ngo__rdbyz = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        hqgxq__iwh = dict(axis=ltaep__ktsn, numeric_only=ckank__ieyc)
        zsuxt__atvcn = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', hqgxq__iwh,
            zsuxt__atvcn, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        nndh__drna = args[0] if len(args) > 0 else kws.pop('periods', 1)
        rky__xew = args[1] if len(args) > 1 else kws.pop('freq', None)
        ltaep__ktsn = args[2] if len(args) > 2 else kws.pop('axis', 0)
        lch__ojz = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        hqgxq__iwh = dict(freq=rky__xew, axis=ltaep__ktsn, fill_value=lch__ojz)
        zsuxt__atvcn = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', hqgxq__iwh,
            zsuxt__atvcn, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        vdvgt__zia = args[0] if len(args) > 0 else kws.pop('func', None)
        foy__wro = kws.pop('engine', None)
        lyl__gxtau = kws.pop('engine_kwargs', None)
        hqgxq__iwh = dict(engine=foy__wro, engine_kwargs=lyl__gxtau)
        zsuxt__atvcn = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', hqgxq__iwh,
            zsuxt__atvcn, package_name='pandas', module_name='GroupBy')
    wlhwd__hnc = {}
    for wxlgv__wqod in grp.selection:
        out_columns.append(wxlgv__wqod)
        wlhwd__hnc[wxlgv__wqod, name_operation] = wxlgv__wqod
        dlrw__vbb = grp.df_type.column_index[wxlgv__wqod]
        data = grp.df_type.data[dlrw__vbb]
        tiwtx__mwg = (name_operation if name_operation != 'transform' else
            get_literal_value(vdvgt__zia))
        if tiwtx__mwg in ('sum', 'cumsum'):
            data = to_str_arr_if_dict_array(data)
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            isul__efcvm, err_msg = get_groupby_output_dtype(data,
                get_literal_value(vdvgt__zia), grp.df_type.index)
            if err_msg == 'ok':
                data = isul__efcvm
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    uqcv__fwszl = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        uqcv__fwszl = SeriesType(out_data[0].dtype, data=out_data[0], index
            =index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(uqcv__fwszl, *args), wlhwd__hnc


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameGroupByType
    _attr_set = None

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.head', no_unliteral=True)
    def resolve_head(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'head', self.context, numba.core.
            registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.ngroup', no_unliteral=True)
    def resolve_ngroup(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'ngroup', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        hbwt__pucve = _get_groupby_apply_udf_out_type(func, grp, f_args,
            kws, self.context, numba.core.registry.cpu_target.target_context)
        pvtht__xpnsy = isinstance(hbwt__pucve, (SeriesType,
            HeterogeneousSeriesType)
            ) and hbwt__pucve.const_info is not None or not isinstance(
            hbwt__pucve, (SeriesType, DataFrameType))
        if pvtht__xpnsy:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                ftnhw__avfbr = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                lhnl__xtzu = tuple(grp.df_type.column_index[grp.keys[
                    ydnh__nzmtt]] for ydnh__nzmtt in range(len(grp.keys)))
                slwht__zod = tuple(grp.df_type.data[dlrw__vbb] for
                    dlrw__vbb in lhnl__xtzu)
                ftnhw__avfbr = MultiIndexType(slwht__zod, tuple(types.
                    literal(lers__gtr) for lers__gtr in grp.keys))
            else:
                dlrw__vbb = grp.df_type.column_index[grp.keys[0]]
                txmke__upkbz = grp.df_type.data[dlrw__vbb]
                ftnhw__avfbr = bodo.hiframes.pd_index_ext.array_type_to_index(
                    txmke__upkbz, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            egwm__jmv = tuple(grp.df_type.data[grp.df_type.column_index[
                wxlgv__wqod]] for wxlgv__wqod in grp.keys)
            san__uelf = tuple(types.literal(ypoqx__clxbt) for ypoqx__clxbt in
                grp.keys) + get_index_name_types(hbwt__pucve.index)
            if not grp.as_index:
                egwm__jmv = types.Array(types.int64, 1, 'C'),
                san__uelf = (types.none,) + get_index_name_types(hbwt__pucve
                    .index)
            ftnhw__avfbr = MultiIndexType(egwm__jmv +
                get_index_data_arr_types(hbwt__pucve.index), san__uelf)
        if pvtht__xpnsy:
            if isinstance(hbwt__pucve, HeterogeneousSeriesType):
                meffp__fddjo, imzyy__gsq = hbwt__pucve.const_info
                if isinstance(hbwt__pucve.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    mypff__ssk = hbwt__pucve.data.tuple_typ.types
                elif isinstance(hbwt__pucve.data, types.Tuple):
                    mypff__ssk = hbwt__pucve.data.types
                ofsm__vcbc = tuple(to_nullable_type(dtype_to_array_type(
                    vhp__ohzq)) for vhp__ohzq in mypff__ssk)
                pfl__tvz = DataFrameType(out_data + ofsm__vcbc,
                    ftnhw__avfbr, out_columns + imzyy__gsq)
            elif isinstance(hbwt__pucve, SeriesType):
                pxwi__qniyy, imzyy__gsq = hbwt__pucve.const_info
                ofsm__vcbc = tuple(to_nullable_type(dtype_to_array_type(
                    hbwt__pucve.dtype)) for meffp__fddjo in range(pxwi__qniyy))
                pfl__tvz = DataFrameType(out_data + ofsm__vcbc,
                    ftnhw__avfbr, out_columns + imzyy__gsq)
            else:
                fdt__jgaqb = get_udf_out_arr_type(hbwt__pucve)
                if not grp.as_index:
                    pfl__tvz = DataFrameType(out_data + (fdt__jgaqb,),
                        ftnhw__avfbr, out_columns + ('',))
                else:
                    pfl__tvz = SeriesType(fdt__jgaqb.dtype, fdt__jgaqb,
                        ftnhw__avfbr, None)
        elif isinstance(hbwt__pucve, SeriesType):
            pfl__tvz = SeriesType(hbwt__pucve.dtype, hbwt__pucve.data,
                ftnhw__avfbr, hbwt__pucve.name_typ)
        else:
            pfl__tvz = DataFrameType(hbwt__pucve.data, ftnhw__avfbr,
                hbwt__pucve.columns)
        nsc__aybb = gen_apply_pysig(len(f_args), kws.keys())
        gww__ggd = (func, *f_args) + tuple(kws.values())
        return signature(pfl__tvz, *gww__ggd).replace(pysig=nsc__aybb)

    def generic_resolve(self, grpby, attr):
        if self._is_existing_attr(attr):
            return
        if attr not in grpby.df_type.columns:
            raise_bodo_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True, _num_shuffle_keys=
            grpby._num_shuffle_keys)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    iom__tpky = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            bnr__xii = grp.selection[0]
            fdt__jgaqb = iom__tpky.data[iom__tpky.column_index[bnr__xii]]
            jfro__qkwmg = SeriesType(fdt__jgaqb.dtype, fdt__jgaqb,
                iom__tpky.index, types.literal(bnr__xii))
        else:
            jqydc__uhlqi = tuple(iom__tpky.data[iom__tpky.column_index[
                wxlgv__wqod]] for wxlgv__wqod in grp.selection)
            jfro__qkwmg = DataFrameType(jqydc__uhlqi, iom__tpky.index,
                tuple(grp.selection))
    else:
        jfro__qkwmg = iom__tpky
    pat__kceyi = jfro__qkwmg,
    pat__kceyi += tuple(f_args)
    try:
        hbwt__pucve = get_const_func_output_type(func, pat__kceyi, kws,
            typing_context, target_context)
    except Exception as kiqs__dvvcs:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', kiqs__dvvcs),
            getattr(kiqs__dvvcs, 'loc', None))
    return hbwt__pucve


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    pat__kceyi = (grp,) + f_args
    try:
        hbwt__pucve = get_const_func_output_type(func, pat__kceyi, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as kiqs__dvvcs:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()',
            kiqs__dvvcs), getattr(kiqs__dvvcs, 'loc', None))
    nsc__aybb = gen_apply_pysig(len(f_args), kws.keys())
    gww__ggd = (func, *f_args) + tuple(kws.values())
    return signature(hbwt__pucve, *gww__ggd).replace(pysig=nsc__aybb)


def gen_apply_pysig(n_args, kws):
    gbj__ecoj = ', '.join(f'arg{ydnh__nzmtt}' for ydnh__nzmtt in range(n_args))
    gbj__ecoj = gbj__ecoj + ', ' if gbj__ecoj else ''
    xya__euhv = ', '.join(f"{zbmgg__finb} = ''" for zbmgg__finb in kws)
    utzmt__hpj = f'def apply_stub(func, {gbj__ecoj}{xya__euhv}):\n'
    utzmt__hpj += '    pass\n'
    xeojb__mkbl = {}
    exec(utzmt__hpj, {}, xeojb__mkbl)
    hofy__toozw = xeojb__mkbl['apply_stub']
    return numba.core.utils.pysignature(hofy__toozw)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        pslh__rws = types.Array(types.int64, 1, 'C')
        mop__jsu = _pivot_values.meta
        bzcxs__hfody = len(mop__jsu)
        tbmfz__yalu = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        bowt__ocrp = DataFrameType((pslh__rws,) * bzcxs__hfody, tbmfz__yalu,
            tuple(mop__jsu))
        return signature(bowt__ocrp, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    utzmt__hpj = 'def impl(keys, dropna, _is_parallel):\n'
    utzmt__hpj += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    utzmt__hpj += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{ydnh__nzmtt}])' for ydnh__nzmtt in range(len(
        keys.types))))
    utzmt__hpj += '    table = arr_info_list_to_table(info_list)\n'
    utzmt__hpj += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    utzmt__hpj += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    utzmt__hpj += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    utzmt__hpj += '    delete_table_decref_arrays(table)\n'
    utzmt__hpj += '    ev.finalize()\n'
    utzmt__hpj += '    return sort_idx, group_labels, ngroups\n'
    xeojb__mkbl = {}
    exec(utzmt__hpj, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, xeojb__mkbl)
    bcz__ufgjr = xeojb__mkbl['impl']
    return bcz__ufgjr


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    pbvmz__kaqke = len(labels)
    fcjaf__jnnju = np.zeros(ngroups, dtype=np.int64)
    kptna__max = np.zeros(ngroups, dtype=np.int64)
    drur__ijy = 0
    gvc__mrad = 0
    for ydnh__nzmtt in range(pbvmz__kaqke):
        qyku__gtlf = labels[ydnh__nzmtt]
        if qyku__gtlf < 0:
            drur__ijy += 1
        else:
            gvc__mrad += 1
            if ydnh__nzmtt == pbvmz__kaqke - 1 or qyku__gtlf != labels[
                ydnh__nzmtt + 1]:
                fcjaf__jnnju[qyku__gtlf] = drur__ijy
                kptna__max[qyku__gtlf] = drur__ijy + gvc__mrad
                drur__ijy += gvc__mrad
                gvc__mrad = 0
    return fcjaf__jnnju, kptna__max


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    bcz__ufgjr, meffp__fddjo = gen_shuffle_dataframe(df, keys, _is_parallel)
    return bcz__ufgjr


def gen_shuffle_dataframe(df, keys, _is_parallel):
    pxwi__qniyy = len(df.columns)
    xay__bjtxi = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    utzmt__hpj = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        utzmt__hpj += '  return df, keys, get_null_shuffle_info()\n'
        xeojb__mkbl = {}
        exec(utzmt__hpj, {'get_null_shuffle_info': get_null_shuffle_info},
            xeojb__mkbl)
        bcz__ufgjr = xeojb__mkbl['impl']
        return bcz__ufgjr
    for ydnh__nzmtt in range(pxwi__qniyy):
        utzmt__hpj += f"""  in_arr{ydnh__nzmtt} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ydnh__nzmtt})
"""
    utzmt__hpj += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    utzmt__hpj += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{ydnh__nzmtt}])' for ydnh__nzmtt in range(
        xay__bjtxi)), ', '.join(f'array_to_info(in_arr{ydnh__nzmtt})' for
        ydnh__nzmtt in range(pxwi__qniyy)), 'array_to_info(in_index_arr)')
    utzmt__hpj += '  table = arr_info_list_to_table(info_list)\n'
    utzmt__hpj += (
        f'  out_table = shuffle_table(table, {xay__bjtxi}, _is_parallel, 1)\n')
    for ydnh__nzmtt in range(xay__bjtxi):
        utzmt__hpj += f"""  out_key{ydnh__nzmtt} = info_to_array(info_from_table(out_table, {ydnh__nzmtt}), keys{ydnh__nzmtt}_typ)
"""
    for ydnh__nzmtt in range(pxwi__qniyy):
        utzmt__hpj += f"""  out_arr{ydnh__nzmtt} = info_to_array(info_from_table(out_table, {ydnh__nzmtt + xay__bjtxi}), in_arr{ydnh__nzmtt}_typ)
"""
    utzmt__hpj += f"""  out_arr_index = info_to_array(info_from_table(out_table, {xay__bjtxi + pxwi__qniyy}), ind_arr_typ)
"""
    utzmt__hpj += '  shuffle_info = get_shuffle_info(out_table)\n'
    utzmt__hpj += '  delete_table(out_table)\n'
    utzmt__hpj += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{ydnh__nzmtt}' for ydnh__nzmtt in range(
        pxwi__qniyy))
    utzmt__hpj += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    utzmt__hpj += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    utzmt__hpj += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{ydnh__nzmtt}' for ydnh__nzmtt in range(xay__bjtxi)))
    zje__ssvgj = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    zje__ssvgj.update({f'keys{ydnh__nzmtt}_typ': keys.types[ydnh__nzmtt] for
        ydnh__nzmtt in range(xay__bjtxi)})
    zje__ssvgj.update({f'in_arr{ydnh__nzmtt}_typ': df.data[ydnh__nzmtt] for
        ydnh__nzmtt in range(pxwi__qniyy)})
    xeojb__mkbl = {}
    exec(utzmt__hpj, zje__ssvgj, xeojb__mkbl)
    bcz__ufgjr = xeojb__mkbl['impl']
    return bcz__ufgjr, zje__ssvgj


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        bmnsd__iamgc = len(data.array_types)
        utzmt__hpj = 'def impl(data, shuffle_info):\n'
        utzmt__hpj += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{ydnh__nzmtt}])' for ydnh__nzmtt in
            range(bmnsd__iamgc)))
        utzmt__hpj += '  table = arr_info_list_to_table(info_list)\n'
        utzmt__hpj += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for ydnh__nzmtt in range(bmnsd__iamgc):
            utzmt__hpj += f"""  out_arr{ydnh__nzmtt} = info_to_array(info_from_table(out_table, {ydnh__nzmtt}), data._data[{ydnh__nzmtt}])
"""
        utzmt__hpj += '  delete_table(out_table)\n'
        utzmt__hpj += '  delete_table(table)\n'
        utzmt__hpj += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{ydnh__nzmtt}' for ydnh__nzmtt in
            range(bmnsd__iamgc))))
        xeojb__mkbl = {}
        exec(utzmt__hpj, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, xeojb__mkbl)
        bcz__ufgjr = xeojb__mkbl['impl']
        return bcz__ufgjr
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            bum__oozxs = bodo.utils.conversion.index_to_array(data)
            suzoi__epbc = reverse_shuffle(bum__oozxs, shuffle_info)
            return bodo.utils.conversion.index_from_array(suzoi__epbc)
        return impl_index

    def impl_arr(data, shuffle_info):
        vfe__wmqr = [array_to_info(data)]
        usoc__mmm = arr_info_list_to_table(vfe__wmqr)
        ztfvc__fwsyr = reverse_shuffle_table(usoc__mmm, shuffle_info)
        suzoi__epbc = info_to_array(info_from_table(ztfvc__fwsyr, 0), data)
        delete_table(ztfvc__fwsyr)
        delete_table(usoc__mmm)
        return suzoi__epbc
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    hqgxq__iwh = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    zsuxt__atvcn = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', hqgxq__iwh, zsuxt__atvcn,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    boi__xmtt = get_overload_const_bool(ascending)
    nibu__idlr = grp.selection[0]
    utzmt__hpj = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    jnvl__tso = (
        f"lambda S: S.value_counts(ascending={boi__xmtt}, _index_name='{nibu__idlr}')"
        )
    utzmt__hpj += f'    return grp.apply({jnvl__tso})\n'
    xeojb__mkbl = {}
    exec(utzmt__hpj, {'bodo': bodo}, xeojb__mkbl)
    bcz__ufgjr = xeojb__mkbl['impl']
    return bcz__ufgjr


groupby_unsupported_attr = {'groups', 'indices'}
groupby_unsupported = {'__iter__', 'get_group', 'all', 'any', 'bfill',
    'backfill', 'cumcount', 'cummax', 'cummin', 'cumprod', 'ffill', 'nth',
    'ohlc', 'pad', 'rank', 'pct_change', 'sem', 'tail', 'corr', 'cov',
    'describe', 'diff', 'fillna', 'filter', 'hist', 'mad', 'plot',
    'quantile', 'resample', 'sample', 'skew', 'take', 'tshift'}
series_only_unsupported_attrs = {'is_monotonic_increasing',
    'is_monotonic_decreasing'}
series_only_unsupported = {'nlargest', 'nsmallest', 'unique'}
dataframe_only_unsupported = {'corrwith', 'boxplot'}


def _install_groupby_unsupported():
    for yph__owp in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, yph__owp, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{yph__owp}'))
    for yph__owp in groupby_unsupported:
        overload_method(DataFrameGroupByType, yph__owp, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{yph__owp}'))
    for yph__owp in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, yph__owp, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{yph__owp}'))
    for yph__owp in series_only_unsupported:
        overload_method(DataFrameGroupByType, yph__owp, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{yph__owp}'))
    for yph__owp in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, yph__owp, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{yph__owp}'))


_install_groupby_unsupported()
