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
        byzv__pgep = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, byzv__pgep)


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
        int__bhv = args[0]
        hno__hfgel = signature.return_type
        pcck__wavz = cgutils.create_struct_proxy(hno__hfgel)(context, builder)
        pcck__wavz.obj = int__bhv
        context.nrt.incref(builder, signature.args[0], int__bhv)
        return pcck__wavz._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for hluzi__cyry in keys:
        selection.remove(hluzi__cyry)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        xlxuj__wios = get_overload_const_int(_num_shuffle_keys)
    else:
        xlxuj__wios = -1
    hno__hfgel = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=xlxuj__wios)
    return hno__hfgel(obj_type, by_type, as_index_type, dropna_type,
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
        grpby, pirdp__wmgg = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(pirdp__wmgg, (tuple, list)):
                if len(set(pirdp__wmgg).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(pirdp__wmgg).difference(set(grpby.
                        df_type.columns))))
                selection = pirdp__wmgg
            else:
                if pirdp__wmgg not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(pirdp__wmgg))
                selection = pirdp__wmgg,
                series_select = True
            bsot__zfwml = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(bsot__zfwml, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, pirdp__wmgg = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            pirdp__wmgg):
            bsot__zfwml = StaticGetItemDataFrameGroupBy.generic(self, (
                grpby, get_literal_value(pirdp__wmgg)), {}).return_type
            return signature(bsot__zfwml, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    igfi__uylsb = arr_type == ArrayItemArrayType(string_array_type)
    qhksi__rvj = arr_type.dtype
    if isinstance(qhksi__rvj, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {qhksi__rvj} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(qhksi__rvj, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    elif func_name in ('first', 'last', 'sum', 'prod', 'min', 'max',
        'count', 'nunique', 'head') and isinstance(arr_type, (
        TupleArrayType, ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {qhksi__rvj} is not supported in groupby built-in function {func_name}'
            )
    elif func_name in {'median', 'mean', 'var', 'std'} and isinstance(
        qhksi__rvj, (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    elif func_name == 'boolor_agg':
        if isinstance(qhksi__rvj, (Decimal128Type, types.Integer, types.
            Float, types.Boolean)):
            return bodo.boolean_array, 'ok'
        return (None,
            f'For boolor_agg, only columns of type integer, float, Decimal, or boolean type are allowed'
            )
    if not isinstance(qhksi__rvj, (types.Integer, types.Float, types.Boolean)):
        if igfi__uylsb or qhksi__rvj == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(qhksi__rvj, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not qhksi__rvj.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {qhksi__rvj} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(qhksi__rvj, types.Boolean) and func_name in {'cumsum',
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
    qhksi__rvj = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(qhksi__rvj, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(qhksi__rvj, types.Integer):
            return IntDtype(qhksi__rvj)
        return qhksi__rvj
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        avf__zqv = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{avf__zqv}'."
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
    for hluzi__cyry in grp.keys:
        if multi_level_names:
            pkjij__qix = hluzi__cyry, ''
        else:
            pkjij__qix = hluzi__cyry
        emvl__otpa = grp.df_type.column_index[hluzi__cyry]
        data = grp.df_type.data[emvl__otpa]
        out_columns.append(pkjij__qix)
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
        lxvrs__pmqsg = tuple(grp.df_type.column_index[grp.keys[bhr__kmeur]] for
            bhr__kmeur in range(len(grp.keys)))
        jqf__pmdq = tuple(grp.df_type.data[emvl__otpa] for emvl__otpa in
            lxvrs__pmqsg)
        index = MultiIndexType(jqf__pmdq, tuple(types.StringLiteral(
            hluzi__cyry) for hluzi__cyry in grp.keys))
    else:
        emvl__otpa = grp.df_type.column_index[grp.keys[0]]
        aagg__hkuod = grp.df_type.data[emvl__otpa]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(aagg__hkuod,
            types.StringLiteral(grp.keys[0]))
    jid__rykqj = {}
    xyzqt__kieg = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        jid__rykqj[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        jid__rykqj[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        fmd__skvux = dict(ascending=ascending)
        nex__eesd = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', fmd__skvux,
            nex__eesd, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for nmsb__qgqla in columns:
            emvl__otpa = grp.df_type.column_index[nmsb__qgqla]
            data = grp.df_type.data[emvl__otpa]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            jqzl__xlc = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType,
                FloatingArrayType)) and isinstance(data.dtype, (types.
                Integer, types.Float)):
                jqzl__xlc = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    tdlw__dlwr = SeriesType(data.dtype, data, None, string_type
                        )
                    xfw__qzy = get_const_func_output_type(func, (tdlw__dlwr
                        ,), {}, typing_context, target_context)
                    if xfw__qzy != ArrayItemArrayType(string_array_type):
                        xfw__qzy = dtype_to_array_type(xfw__qzy)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=nmsb__qgqla, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    rvnw__nzwbq = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    fczk__ejmld = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    fmd__skvux = dict(numeric_only=rvnw__nzwbq, min_count=
                        fczk__ejmld)
                    nex__eesd = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        fmd__skvux, nex__eesd, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    rvnw__nzwbq = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    fczk__ejmld = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    fmd__skvux = dict(numeric_only=rvnw__nzwbq, min_count=
                        fczk__ejmld)
                    nex__eesd = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        fmd__skvux, nex__eesd, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    rvnw__nzwbq = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    fmd__skvux = dict(numeric_only=rvnw__nzwbq)
                    nex__eesd = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        fmd__skvux, nex__eesd, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    sypr__zud = args[0] if len(args) > 0 else kws.pop('axis', 0
                        )
                    erjws__uhqqi = args[1] if len(args) > 1 else kws.pop(
                        'skipna', True)
                    fmd__skvux = dict(axis=sypr__zud, skipna=erjws__uhqqi)
                    nex__eesd = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        fmd__skvux, nex__eesd, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    hopnb__aucbz = args[0] if len(args) > 0 else kws.pop('ddof'
                        , 1)
                    fmd__skvux = dict(ddof=hopnb__aucbz)
                    nex__eesd = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        fmd__skvux, nex__eesd, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                xfw__qzy, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                xfw__qzy = to_str_arr_if_dict_array(xfw__qzy) if func_name in (
                    'sum', 'cumsum') else xfw__qzy
                out_data.append(xfw__qzy)
                out_columns.append(nmsb__qgqla)
                if func_name == 'agg':
                    dgjp__flx = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    jid__rykqj[nmsb__qgqla, dgjp__flx] = nmsb__qgqla
                else:
                    jid__rykqj[nmsb__qgqla, func_name] = nmsb__qgqla
                out_column_type.append(jqzl__xlc)
            elif raise_on_any_error:
                raise BodoError(
                    f'Groupby with function {func_name} not supported. Error message: {err_msg}'
                    )
            else:
                xyzqt__kieg.append(err_msg)
    if func_name == 'sum':
        rdtv__mrffk = any([(klap__hacic == ColumnType.NumericalColumn.value
            ) for klap__hacic in out_column_type])
        if rdtv__mrffk:
            out_data = [klap__hacic for klap__hacic, zwv__ghcbv in zip(
                out_data, out_column_type) if zwv__ghcbv != ColumnType.
                NonNumericalColumn.value]
            out_columns = [klap__hacic for klap__hacic, zwv__ghcbv in zip(
                out_columns, out_column_type) if zwv__ghcbv != ColumnType.
                NonNumericalColumn.value]
            jid__rykqj = {}
            for nmsb__qgqla in out_columns:
                if grp.as_index is False and nmsb__qgqla in grp.keys:
                    continue
                jid__rykqj[nmsb__qgqla, func_name] = nmsb__qgqla
    keff__jpy = len(xyzqt__kieg)
    if len(out_data) == 0:
        if keff__jpy == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(keff__jpy, ' was' if keff__jpy == 1 else 's were',
                ','.join(xyzqt__kieg)))
    cnlgd__qqm = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            qfmx__ughss = IntDtype(out_data[0].dtype)
        elif isinstance(out_data[0], FloatingArrayType):
            qfmx__ughss = FloatDtype(out_data[0].dtype)
        else:
            qfmx__ughss = out_data[0].dtype
        lwzr__wcmm = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        cnlgd__qqm = SeriesType(qfmx__ughss, data=out_data[0], index=index,
            name_typ=lwzr__wcmm)
    return signature(cnlgd__qqm, *args), jid__rykqj


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context,
    target_context, raise_on_any_error):
    odghh__cglum = True
    if isinstance(f_val, str):
        odghh__cglum = False
        essiz__ztif = f_val
    elif is_overload_constant_str(f_val):
        odghh__cglum = False
        essiz__ztif = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        odghh__cglum = False
        essiz__ztif = bodo.utils.typing.get_builtin_function_name(f_val)
    if not odghh__cglum:
        if essiz__ztif not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {essiz__ztif}')
        bsot__zfwml = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(bsot__zfwml, (), essiz__ztif, typing_context,
            target_context, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    else:
        if is_expr(f_val, 'make_function'):
            mye__cog = types.functions.MakeFunctionLiteral(f_val)
        else:
            mye__cog = f_val
        validate_udf('agg', mye__cog)
        func = get_overload_const_func(mye__cog, None)
        yqcwy__gvk = func.code if hasattr(func, 'code') else func.__code__
        essiz__ztif = yqcwy__gvk.co_name
        bsot__zfwml = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(bsot__zfwml, (), 'agg', typing_context,
            target_context, mye__cog, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    return essiz__ztif, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    laktq__kfzzo = kws and all(isinstance(ztow__cyxb, types.Tuple) and len(
        ztow__cyxb) == 2 for ztow__cyxb in kws.values())
    raise_on_any_error = laktq__kfzzo
    if is_overload_none(func) and not laktq__kfzzo:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not laktq__kfzzo:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    tggk__kac = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if laktq__kfzzo or is_overload_constant_dict(func):
        if laktq__kfzzo:
            utrgy__huu = [get_literal_value(efcw__nvn) for efcw__nvn,
                cczlx__aiznu in kws.values()]
            qcti__djho = [get_literal_value(cldb__lksym) for cczlx__aiznu,
                cldb__lksym in kws.values()]
        else:
            zpems__ebi = get_overload_constant_dict(func)
            utrgy__huu = tuple(zpems__ebi.keys())
            qcti__djho = tuple(zpems__ebi.values())
        for fnhl__mbg in ('head', 'ngroup'):
            if fnhl__mbg in qcti__djho:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {fnhl__mbg} cannot be mixed with other groupby operations.'
                    )
        if any(nmsb__qgqla not in grp.selection and nmsb__qgqla not in grp.
            keys for nmsb__qgqla in utrgy__huu):
            raise_bodo_error(
                f'Selected column names {utrgy__huu} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            qcti__djho)
        if laktq__kfzzo and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        jid__rykqj = {}
        out_columns = []
        out_data = []
        out_column_type = []
        jru__mqqy = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for yfe__vmlty, f_val in zip(utrgy__huu, qcti__djho):
            if isinstance(f_val, (tuple, list)):
                bzju__qosbe = 0
                for mye__cog in f_val:
                    essiz__ztif, out_tp = get_agg_funcname_and_outtyp(grp,
                        yfe__vmlty, mye__cog, typing_context,
                        target_context, raise_on_any_error)
                    tggk__kac = essiz__ztif in list_cumulative
                    if essiz__ztif == '<lambda>' and len(f_val) > 1:
                        essiz__ztif = '<lambda_' + str(bzju__qosbe) + '>'
                        bzju__qosbe += 1
                    out_columns.append((yfe__vmlty, essiz__ztif))
                    jid__rykqj[yfe__vmlty, essiz__ztif
                        ] = yfe__vmlty, essiz__ztif
                    _append_out_type(grp, out_data, out_tp)
            else:
                essiz__ztif, out_tp = get_agg_funcname_and_outtyp(grp,
                    yfe__vmlty, f_val, typing_context, target_context,
                    raise_on_any_error)
                tggk__kac = essiz__ztif in list_cumulative
                if multi_level_names:
                    out_columns.append((yfe__vmlty, essiz__ztif))
                    jid__rykqj[yfe__vmlty, essiz__ztif
                        ] = yfe__vmlty, essiz__ztif
                elif not laktq__kfzzo:
                    out_columns.append(yfe__vmlty)
                    jid__rykqj[yfe__vmlty, essiz__ztif] = yfe__vmlty
                elif laktq__kfzzo:
                    jru__mqqy.append(essiz__ztif)
                _append_out_type(grp, out_data, out_tp)
        if laktq__kfzzo:
            for bhr__kmeur, porq__aeg in enumerate(kws.keys()):
                out_columns.append(porq__aeg)
                jid__rykqj[utrgy__huu[bhr__kmeur], jru__mqqy[bhr__kmeur]
                    ] = porq__aeg
        if tggk__kac:
            index = grp.df_type.index
        else:
            index = out_tp.index
        cnlgd__qqm = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(cnlgd__qqm, *args), jid__rykqj
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            qlats__vlbb = get_overload_const_list(func)
        else:
            qlats__vlbb = func.types
        if len(qlats__vlbb) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        bzju__qosbe = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        jid__rykqj = {}
        gfmrm__avapq = grp.selection[0]
        for f_val in qlats__vlbb:
            essiz__ztif, out_tp = get_agg_funcname_and_outtyp(grp,
                gfmrm__avapq, f_val, typing_context, target_context,
                raise_on_any_error)
            tggk__kac = essiz__ztif in list_cumulative
            if essiz__ztif == '<lambda>' and len(qlats__vlbb) > 1:
                essiz__ztif = '<lambda_' + str(bzju__qosbe) + '>'
                bzju__qosbe += 1
            out_columns.append(essiz__ztif)
            jid__rykqj[gfmrm__avapq, essiz__ztif] = essiz__ztif
            _append_out_type(grp, out_data, out_tp)
        if tggk__kac:
            index = grp.df_type.index
        else:
            index = out_tp.index
        cnlgd__qqm = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(cnlgd__qqm, *args), jid__rykqj
    essiz__ztif = ''
    if types.unliteral(func) == types.unicode_type:
        essiz__ztif = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        essiz__ztif = bodo.utils.typing.get_builtin_function_name(func)
    if essiz__ztif:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, essiz__ztif, typing_context, kws)
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
        sypr__zud = args[0] if len(args) > 0 else kws.pop('axis', 0)
        rvnw__nzwbq = args[1] if len(args) > 1 else kws.pop('numeric_only',
            False)
        erjws__uhqqi = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        fmd__skvux = dict(axis=sypr__zud, numeric_only=rvnw__nzwbq)
        nex__eesd = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', fmd__skvux,
            nex__eesd, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        rwo__kpwwp = args[0] if len(args) > 0 else kws.pop('periods', 1)
        dbry__duyk = args[1] if len(args) > 1 else kws.pop('freq', None)
        sypr__zud = args[2] if len(args) > 2 else kws.pop('axis', 0)
        cya__kccrh = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        fmd__skvux = dict(freq=dbry__duyk, axis=sypr__zud, fill_value=
            cya__kccrh)
        nex__eesd = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', fmd__skvux,
            nex__eesd, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        bquu__gzc = args[0] if len(args) > 0 else kws.pop('func', None)
        cjgys__udssd = kws.pop('engine', None)
        secg__dskkb = kws.pop('engine_kwargs', None)
        fmd__skvux = dict(engine=cjgys__udssd, engine_kwargs=secg__dskkb)
        nex__eesd = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', fmd__skvux, nex__eesd,
            package_name='pandas', module_name='GroupBy')
    jid__rykqj = {}
    for nmsb__qgqla in grp.selection:
        out_columns.append(nmsb__qgqla)
        jid__rykqj[nmsb__qgqla, name_operation] = nmsb__qgqla
        emvl__otpa = grp.df_type.column_index[nmsb__qgqla]
        data = grp.df_type.data[emvl__otpa]
        ysmrd__hgd = (name_operation if name_operation != 'transform' else
            get_literal_value(bquu__gzc))
        if ysmrd__hgd in ('sum', 'cumsum'):
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
            xfw__qzy, err_msg = get_groupby_output_dtype(data,
                get_literal_value(bquu__gzc), grp.df_type.index)
            if err_msg == 'ok':
                data = xfw__qzy
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    cnlgd__qqm = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        cnlgd__qqm = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(cnlgd__qqm, *args), jid__rykqj


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
        ktrwe__wslp = _get_groupby_apply_udf_out_type(func, grp, f_args,
            kws, self.context, numba.core.registry.cpu_target.target_context)
        eyqks__ugg = isinstance(ktrwe__wslp, (SeriesType,
            HeterogeneousSeriesType)
            ) and ktrwe__wslp.const_info is not None or not isinstance(
            ktrwe__wslp, (SeriesType, DataFrameType))
        if eyqks__ugg:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                nmu__gxv = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                lxvrs__pmqsg = tuple(grp.df_type.column_index[grp.keys[
                    bhr__kmeur]] for bhr__kmeur in range(len(grp.keys)))
                jqf__pmdq = tuple(grp.df_type.data[emvl__otpa] for
                    emvl__otpa in lxvrs__pmqsg)
                nmu__gxv = MultiIndexType(jqf__pmdq, tuple(types.literal(
                    hluzi__cyry) for hluzi__cyry in grp.keys))
            else:
                emvl__otpa = grp.df_type.column_index[grp.keys[0]]
                aagg__hkuod = grp.df_type.data[emvl__otpa]
                nmu__gxv = bodo.hiframes.pd_index_ext.array_type_to_index(
                    aagg__hkuod, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            vmi__gehnn = tuple(grp.df_type.data[grp.df_type.column_index[
                nmsb__qgqla]] for nmsb__qgqla in grp.keys)
            vhlh__fwk = tuple(types.literal(ztow__cyxb) for ztow__cyxb in
                grp.keys) + get_index_name_types(ktrwe__wslp.index)
            if not grp.as_index:
                vmi__gehnn = types.Array(types.int64, 1, 'C'),
                vhlh__fwk = (types.none,) + get_index_name_types(ktrwe__wslp
                    .index)
            nmu__gxv = MultiIndexType(vmi__gehnn + get_index_data_arr_types
                (ktrwe__wslp.index), vhlh__fwk)
        if eyqks__ugg:
            if isinstance(ktrwe__wslp, HeterogeneousSeriesType):
                cczlx__aiznu, cvd__buc = ktrwe__wslp.const_info
                if isinstance(ktrwe__wslp.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    hoz__hwlkn = ktrwe__wslp.data.tuple_typ.types
                elif isinstance(ktrwe__wslp.data, types.Tuple):
                    hoz__hwlkn = ktrwe__wslp.data.types
                mfmd__hgrun = tuple(to_nullable_type(dtype_to_array_type(
                    iax__tebjw)) for iax__tebjw in hoz__hwlkn)
                ebmj__kclig = DataFrameType(out_data + mfmd__hgrun,
                    nmu__gxv, out_columns + cvd__buc)
            elif isinstance(ktrwe__wslp, SeriesType):
                eya__nfzr, cvd__buc = ktrwe__wslp.const_info
                mfmd__hgrun = tuple(to_nullable_type(dtype_to_array_type(
                    ktrwe__wslp.dtype)) for cczlx__aiznu in range(eya__nfzr))
                ebmj__kclig = DataFrameType(out_data + mfmd__hgrun,
                    nmu__gxv, out_columns + cvd__buc)
            else:
                qftkd__offhn = get_udf_out_arr_type(ktrwe__wslp)
                if not grp.as_index:
                    ebmj__kclig = DataFrameType(out_data + (qftkd__offhn,),
                        nmu__gxv, out_columns + ('',))
                else:
                    ebmj__kclig = SeriesType(qftkd__offhn.dtype,
                        qftkd__offhn, nmu__gxv, None)
        elif isinstance(ktrwe__wslp, SeriesType):
            ebmj__kclig = SeriesType(ktrwe__wslp.dtype, ktrwe__wslp.data,
                nmu__gxv, ktrwe__wslp.name_typ)
        else:
            ebmj__kclig = DataFrameType(ktrwe__wslp.data, nmu__gxv,
                ktrwe__wslp.columns)
        iuuc__cci = gen_apply_pysig(len(f_args), kws.keys())
        izhcb__jtiyi = (func, *f_args) + tuple(kws.values())
        return signature(ebmj__kclig, *izhcb__jtiyi).replace(pysig=iuuc__cci)

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
    jcuix__yirj = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            yfe__vmlty = grp.selection[0]
            qftkd__offhn = jcuix__yirj.data[jcuix__yirj.column_index[
                yfe__vmlty]]
            omrox__hqtco = SeriesType(qftkd__offhn.dtype, qftkd__offhn,
                jcuix__yirj.index, types.literal(yfe__vmlty))
        else:
            gfbbg__mus = tuple(jcuix__yirj.data[jcuix__yirj.column_index[
                nmsb__qgqla]] for nmsb__qgqla in grp.selection)
            omrox__hqtco = DataFrameType(gfbbg__mus, jcuix__yirj.index,
                tuple(grp.selection))
    else:
        omrox__hqtco = jcuix__yirj
    drde__siq = omrox__hqtco,
    drde__siq += tuple(f_args)
    try:
        ktrwe__wslp = get_const_func_output_type(func, drde__siq, kws,
            typing_context, target_context)
    except Exception as adk__vyyd:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', adk__vyyd),
            getattr(adk__vyyd, 'loc', None))
    return ktrwe__wslp


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    drde__siq = (grp,) + f_args
    try:
        ktrwe__wslp = get_const_func_output_type(func, drde__siq, kws, self
            .context, numba.core.registry.cpu_target.target_context, False)
    except Exception as adk__vyyd:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', adk__vyyd),
            getattr(adk__vyyd, 'loc', None))
    iuuc__cci = gen_apply_pysig(len(f_args), kws.keys())
    izhcb__jtiyi = (func, *f_args) + tuple(kws.values())
    return signature(ktrwe__wslp, *izhcb__jtiyi).replace(pysig=iuuc__cci)


def gen_apply_pysig(n_args, kws):
    ahvf__rks = ', '.join(f'arg{bhr__kmeur}' for bhr__kmeur in range(n_args))
    ahvf__rks = ahvf__rks + ', ' if ahvf__rks else ''
    snkk__jei = ', '.join(f"{wco__oxdg} = ''" for wco__oxdg in kws)
    fqxu__nfonk = f'def apply_stub(func, {ahvf__rks}{snkk__jei}):\n'
    fqxu__nfonk += '    pass\n'
    yyar__oruzh = {}
    exec(fqxu__nfonk, {}, yyar__oruzh)
    wxur__xtrol = yyar__oruzh['apply_stub']
    return numba.core.utils.pysignature(wxur__xtrol)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        hlvf__zwv = types.Array(types.int64, 1, 'C')
        vxh__uzmp = _pivot_values.meta
        xyll__hft = len(vxh__uzmp)
        qgtk__brksw = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        tdfv__haj = DataFrameType((hlvf__zwv,) * xyll__hft, qgtk__brksw,
            tuple(vxh__uzmp))
        return signature(tdfv__haj, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    fqxu__nfonk = 'def impl(keys, dropna, _is_parallel):\n'
    fqxu__nfonk += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    fqxu__nfonk += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{bhr__kmeur}])' for bhr__kmeur in range(len(
        keys.types))))
    fqxu__nfonk += '    table = arr_info_list_to_table(info_list)\n'
    fqxu__nfonk += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    fqxu__nfonk += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    fqxu__nfonk += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    fqxu__nfonk += '    delete_table_decref_arrays(table)\n'
    fqxu__nfonk += '    ev.finalize()\n'
    fqxu__nfonk += '    return sort_idx, group_labels, ngroups\n'
    yyar__oruzh = {}
    exec(fqxu__nfonk, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, yyar__oruzh)
    ian__lsnk = yyar__oruzh['impl']
    return ian__lsnk


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    qocjh__lzf = len(labels)
    buht__ldn = np.zeros(ngroups, dtype=np.int64)
    yvfn__bcq = np.zeros(ngroups, dtype=np.int64)
    szdp__rgzrg = 0
    jsy__sbh = 0
    for bhr__kmeur in range(qocjh__lzf):
        necav__qzbk = labels[bhr__kmeur]
        if necav__qzbk < 0:
            szdp__rgzrg += 1
        else:
            jsy__sbh += 1
            if bhr__kmeur == qocjh__lzf - 1 or necav__qzbk != labels[
                bhr__kmeur + 1]:
                buht__ldn[necav__qzbk] = szdp__rgzrg
                yvfn__bcq[necav__qzbk] = szdp__rgzrg + jsy__sbh
                szdp__rgzrg += jsy__sbh
                jsy__sbh = 0
    return buht__ldn, yvfn__bcq


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    ian__lsnk, cczlx__aiznu = gen_shuffle_dataframe(df, keys, _is_parallel)
    return ian__lsnk


def gen_shuffle_dataframe(df, keys, _is_parallel):
    eya__nfzr = len(df.columns)
    glzs__hix = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    fqxu__nfonk = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        fqxu__nfonk += '  return df, keys, get_null_shuffle_info()\n'
        yyar__oruzh = {}
        exec(fqxu__nfonk, {'get_null_shuffle_info': get_null_shuffle_info},
            yyar__oruzh)
        ian__lsnk = yyar__oruzh['impl']
        return ian__lsnk
    for bhr__kmeur in range(eya__nfzr):
        fqxu__nfonk += f"""  in_arr{bhr__kmeur} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bhr__kmeur})
"""
    fqxu__nfonk += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    fqxu__nfonk += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{bhr__kmeur}])' for bhr__kmeur in range(
        glzs__hix)), ', '.join(f'array_to_info(in_arr{bhr__kmeur})' for
        bhr__kmeur in range(eya__nfzr)), 'array_to_info(in_index_arr)')
    fqxu__nfonk += '  table = arr_info_list_to_table(info_list)\n'
    fqxu__nfonk += (
        f'  out_table = shuffle_table(table, {glzs__hix}, _is_parallel, 1)\n')
    for bhr__kmeur in range(glzs__hix):
        fqxu__nfonk += f"""  out_key{bhr__kmeur} = info_to_array(info_from_table(out_table, {bhr__kmeur}), keys{bhr__kmeur}_typ)
"""
    for bhr__kmeur in range(eya__nfzr):
        fqxu__nfonk += f"""  out_arr{bhr__kmeur} = info_to_array(info_from_table(out_table, {bhr__kmeur + glzs__hix}), in_arr{bhr__kmeur}_typ)
"""
    fqxu__nfonk += f"""  out_arr_index = info_to_array(info_from_table(out_table, {glzs__hix + eya__nfzr}), ind_arr_typ)
"""
    fqxu__nfonk += '  shuffle_info = get_shuffle_info(out_table)\n'
    fqxu__nfonk += '  delete_table(out_table)\n'
    fqxu__nfonk += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{bhr__kmeur}' for bhr__kmeur in range(
        eya__nfzr))
    fqxu__nfonk += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    fqxu__nfonk += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    fqxu__nfonk += '  return out_df, ({},), shuffle_info\n'.format(', '.
        join(f'out_key{bhr__kmeur}' for bhr__kmeur in range(glzs__hix)))
    wkzg__riar = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    wkzg__riar.update({f'keys{bhr__kmeur}_typ': keys.types[bhr__kmeur] for
        bhr__kmeur in range(glzs__hix)})
    wkzg__riar.update({f'in_arr{bhr__kmeur}_typ': df.data[bhr__kmeur] for
        bhr__kmeur in range(eya__nfzr)})
    yyar__oruzh = {}
    exec(fqxu__nfonk, wkzg__riar, yyar__oruzh)
    ian__lsnk = yyar__oruzh['impl']
    return ian__lsnk, wkzg__riar


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        lqo__vpx = len(data.array_types)
        fqxu__nfonk = 'def impl(data, shuffle_info):\n'
        fqxu__nfonk += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{bhr__kmeur}])' for bhr__kmeur in
            range(lqo__vpx)))
        fqxu__nfonk += '  table = arr_info_list_to_table(info_list)\n'
        fqxu__nfonk += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for bhr__kmeur in range(lqo__vpx):
            fqxu__nfonk += f"""  out_arr{bhr__kmeur} = info_to_array(info_from_table(out_table, {bhr__kmeur}), data._data[{bhr__kmeur}])
"""
        fqxu__nfonk += '  delete_table(out_table)\n'
        fqxu__nfonk += '  delete_table(table)\n'
        fqxu__nfonk += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{bhr__kmeur}' for bhr__kmeur in range
            (lqo__vpx))))
        yyar__oruzh = {}
        exec(fqxu__nfonk, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, yyar__oruzh)
        ian__lsnk = yyar__oruzh['impl']
        return ian__lsnk
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            dkdw__ytk = bodo.utils.conversion.index_to_array(data)
            ypl__jwa = reverse_shuffle(dkdw__ytk, shuffle_info)
            return bodo.utils.conversion.index_from_array(ypl__jwa)
        return impl_index

    def impl_arr(data, shuffle_info):
        mvfvj__hsw = [array_to_info(data)]
        aaoj__oiewg = arr_info_list_to_table(mvfvj__hsw)
        dbh__rkb = reverse_shuffle_table(aaoj__oiewg, shuffle_info)
        ypl__jwa = info_to_array(info_from_table(dbh__rkb, 0), data)
        delete_table(dbh__rkb)
        delete_table(aaoj__oiewg)
        return ypl__jwa
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    fmd__skvux = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    nex__eesd = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', fmd__skvux, nex__eesd,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    rdthf__kkie = get_overload_const_bool(ascending)
    droy__xejs = grp.selection[0]
    fqxu__nfonk = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    whuwc__tmk = (
        f"lambda S: S.value_counts(ascending={rdthf__kkie}, _index_name='{droy__xejs}')"
        )
    fqxu__nfonk += f'    return grp.apply({whuwc__tmk})\n'
    yyar__oruzh = {}
    exec(fqxu__nfonk, {'bodo': bodo}, yyar__oruzh)
    ian__lsnk = yyar__oruzh['impl']
    return ian__lsnk


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
    for cxfmb__dcfqw in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, cxfmb__dcfqw, no_unliteral
            =True)(create_unsupported_overload(
            f'DataFrameGroupBy.{cxfmb__dcfqw}'))
    for cxfmb__dcfqw in groupby_unsupported:
        overload_method(DataFrameGroupByType, cxfmb__dcfqw, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{cxfmb__dcfqw}'))
    for cxfmb__dcfqw in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, cxfmb__dcfqw, no_unliteral
            =True)(create_unsupported_overload(f'SeriesGroupBy.{cxfmb__dcfqw}')
            )
    for cxfmb__dcfqw in series_only_unsupported:
        overload_method(DataFrameGroupByType, cxfmb__dcfqw, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{cxfmb__dcfqw}'))
    for cxfmb__dcfqw in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, cxfmb__dcfqw, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{cxfmb__dcfqw}'))


_install_groupby_unsupported()
