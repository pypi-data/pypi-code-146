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
        jls__hhc = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, jls__hhc)


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
        ddwg__miiwr = args[0]
        ejpq__xhoh = signature.return_type
        lmao__styoy = cgutils.create_struct_proxy(ejpq__xhoh)(context, builder)
        lmao__styoy.obj = ddwg__miiwr
        context.nrt.incref(builder, signature.args[0], ddwg__miiwr)
        return lmao__styoy._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for ckurj__ozz in keys:
        selection.remove(ckurj__ozz)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        vjde__ifqtl = get_overload_const_int(_num_shuffle_keys)
    else:
        vjde__ifqtl = -1
    ejpq__xhoh = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=vjde__ifqtl)
    return ejpq__xhoh(obj_type, by_type, as_index_type, dropna_type,
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
        grpby, pzils__cqbxk = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(pzils__cqbxk, (tuple, list)):
                if len(set(pzils__cqbxk).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(pzils__cqbxk).difference(set(grpby.
                        df_type.columns))))
                selection = pzils__cqbxk
            else:
                if pzils__cqbxk not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(pzils__cqbxk))
                selection = pzils__cqbxk,
                series_select = True
            xit__kmmh = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(xit__kmmh, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, pzils__cqbxk = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            pzils__cqbxk):
            xit__kmmh = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(pzils__cqbxk)), {}).return_type
            return signature(xit__kmmh, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    tqjnw__gtup = arr_type == ArrayItemArrayType(string_array_type)
    bct__ikcje = arr_type.dtype
    if isinstance(bct__ikcje, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {bct__ikcje} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(bct__ikcje, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    elif func_name in ('first', 'last', 'sum', 'prod', 'min', 'max',
        'count', 'nunique', 'head') and isinstance(arr_type, (
        TupleArrayType, ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {bct__ikcje} is not supported in groupby built-in function {func_name}'
            )
    elif func_name in {'median', 'mean', 'var', 'std'} and isinstance(
        bct__ikcje, (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    elif func_name == 'boolor_agg':
        if isinstance(bct__ikcje, (Decimal128Type, types.Integer, types.
            Float, types.Boolean)):
            return bodo.boolean_array, 'ok'
        return (None,
            f'For boolor_agg, only columns of type integer, float, Decimal, or boolean type are allowed'
            )
    if not isinstance(bct__ikcje, (types.Integer, types.Float, types.Boolean)):
        if tqjnw__gtup or bct__ikcje == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(bct__ikcje, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not bct__ikcje.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {bct__ikcje} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(bct__ikcje, types.Boolean) and func_name in {'cumsum',
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
    bct__ikcje = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(bct__ikcje, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(bct__ikcje, types.Integer):
            return IntDtype(bct__ikcje)
        return bct__ikcje
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        odnfe__ntbqk = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{odnfe__ntbqk}'."
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
    for ckurj__ozz in grp.keys:
        if multi_level_names:
            ewqk__acrfe = ckurj__ozz, ''
        else:
            ewqk__acrfe = ckurj__ozz
        ticg__elpm = grp.df_type.column_index[ckurj__ozz]
        data = grp.df_type.data[ticg__elpm]
        out_columns.append(ewqk__acrfe)
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
        ngb__lovs = tuple(grp.df_type.column_index[grp.keys[fwnkk__wlz]] for
            fwnkk__wlz in range(len(grp.keys)))
        iabz__guf = tuple(grp.df_type.data[ticg__elpm] for ticg__elpm in
            ngb__lovs)
        index = MultiIndexType(iabz__guf, tuple(types.StringLiteral(
            ckurj__ozz) for ckurj__ozz in grp.keys))
    else:
        ticg__elpm = grp.df_type.column_index[grp.keys[0]]
        rms__refh = grp.df_type.data[ticg__elpm]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(rms__refh,
            types.StringLiteral(grp.keys[0]))
    hnlb__ehsj = {}
    qwt__eyegg = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        hnlb__ehsj[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        hnlb__ehsj[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        dsy__unt = dict(ascending=ascending)
        frmrz__irq = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', dsy__unt, frmrz__irq,
            package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for guuh__yag in columns:
            ticg__elpm = grp.df_type.column_index[guuh__yag]
            data = grp.df_type.data[ticg__elpm]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            phwaj__veug = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType,
                FloatingArrayType)) and isinstance(data.dtype, (types.
                Integer, types.Float)):
                phwaj__veug = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    ksbg__xgthr = SeriesType(data.dtype, data, None,
                        string_type)
                    nvflu__nweu = get_const_func_output_type(func, (
                        ksbg__xgthr,), {}, typing_context, target_context)
                    if nvflu__nweu != ArrayItemArrayType(string_array_type):
                        nvflu__nweu = dtype_to_array_type(nvflu__nweu)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=guuh__yag, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    ewo__csxza = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    tmush__gli = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    dsy__unt = dict(numeric_only=ewo__csxza, min_count=
                        tmush__gli)
                    frmrz__irq = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}', dsy__unt,
                        frmrz__irq, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    ewo__csxza = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    tmush__gli = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    dsy__unt = dict(numeric_only=ewo__csxza, min_count=
                        tmush__gli)
                    frmrz__irq = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}', dsy__unt,
                        frmrz__irq, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    ewo__csxza = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    dsy__unt = dict(numeric_only=ewo__csxza)
                    frmrz__irq = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}', dsy__unt,
                        frmrz__irq, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    ymzz__lzvwm = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    obh__nkab = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    dsy__unt = dict(axis=ymzz__lzvwm, skipna=obh__nkab)
                    frmrz__irq = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}', dsy__unt,
                        frmrz__irq, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    xnnkt__cevxc = args[0] if len(args) > 0 else kws.pop('ddof'
                        , 1)
                    dsy__unt = dict(ddof=xnnkt__cevxc)
                    frmrz__irq = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}', dsy__unt,
                        frmrz__irq, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                nvflu__nweu, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                nvflu__nweu = to_str_arr_if_dict_array(nvflu__nweu
                    ) if func_name in ('sum', 'cumsum') else nvflu__nweu
                out_data.append(nvflu__nweu)
                out_columns.append(guuh__yag)
                if func_name == 'agg':
                    haq__shrvl = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    hnlb__ehsj[guuh__yag, haq__shrvl] = guuh__yag
                else:
                    hnlb__ehsj[guuh__yag, func_name] = guuh__yag
                out_column_type.append(phwaj__veug)
            elif raise_on_any_error:
                raise BodoError(
                    f'Groupby with function {func_name} not supported. Error message: {err_msg}'
                    )
            else:
                qwt__eyegg.append(err_msg)
    if func_name == 'sum':
        gvp__dnwvb = any([(gqne__ynzou == ColumnType.NumericalColumn.value) for
            gqne__ynzou in out_column_type])
        if gvp__dnwvb:
            out_data = [gqne__ynzou for gqne__ynzou, ysb__wfhy in zip(
                out_data, out_column_type) if ysb__wfhy != ColumnType.
                NonNumericalColumn.value]
            out_columns = [gqne__ynzou for gqne__ynzou, ysb__wfhy in zip(
                out_columns, out_column_type) if ysb__wfhy != ColumnType.
                NonNumericalColumn.value]
            hnlb__ehsj = {}
            for guuh__yag in out_columns:
                if grp.as_index is False and guuh__yag in grp.keys:
                    continue
                hnlb__ehsj[guuh__yag, func_name] = guuh__yag
    jwq__iwawg = len(qwt__eyegg)
    if len(out_data) == 0:
        if jwq__iwawg == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(jwq__iwawg, ' was' if jwq__iwawg == 1 else 's were',
                ','.join(qwt__eyegg)))
    oga__lvlo = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            aze__emy = IntDtype(out_data[0].dtype)
        elif isinstance(out_data[0], FloatingArrayType):
            aze__emy = FloatDtype(out_data[0].dtype)
        else:
            aze__emy = out_data[0].dtype
        npj__wine = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        oga__lvlo = SeriesType(aze__emy, data=out_data[0], index=index,
            name_typ=npj__wine)
    return signature(oga__lvlo, *args), hnlb__ehsj


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context,
    target_context, raise_on_any_error):
    syabu__nrpho = True
    if isinstance(f_val, str):
        syabu__nrpho = False
        oywa__xmzh = f_val
    elif is_overload_constant_str(f_val):
        syabu__nrpho = False
        oywa__xmzh = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        syabu__nrpho = False
        oywa__xmzh = bodo.utils.typing.get_builtin_function_name(f_val)
    if not syabu__nrpho:
        if oywa__xmzh not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {oywa__xmzh}')
        xit__kmmh = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(xit__kmmh, (), oywa__xmzh, typing_context,
            target_context, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    else:
        if is_expr(f_val, 'make_function'):
            muccv__mikks = types.functions.MakeFunctionLiteral(f_val)
        else:
            muccv__mikks = f_val
        validate_udf('agg', muccv__mikks)
        func = get_overload_const_func(muccv__mikks, None)
        khz__ywb = func.code if hasattr(func, 'code') else func.__code__
        oywa__xmzh = khz__ywb.co_name
        xit__kmmh = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(xit__kmmh, (), 'agg', typing_context,
            target_context, muccv__mikks, raise_on_any_error=raise_on_any_error
            )[0].return_type
    return oywa__xmzh, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    mkxi__fqpkz = kws and all(isinstance(fcs__avq, types.Tuple) and len(
        fcs__avq) == 2 for fcs__avq in kws.values())
    raise_on_any_error = mkxi__fqpkz
    if is_overload_none(func) and not mkxi__fqpkz:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not mkxi__fqpkz:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    okzes__iae = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if mkxi__fqpkz or is_overload_constant_dict(func):
        if mkxi__fqpkz:
            gcl__gyt = [get_literal_value(qhx__wiq) for qhx__wiq,
                nwwif__jrf in kws.values()]
            nsl__izpem = [get_literal_value(rfyce__nljrg) for nwwif__jrf,
                rfyce__nljrg in kws.values()]
        else:
            iqej__hst = get_overload_constant_dict(func)
            gcl__gyt = tuple(iqej__hst.keys())
            nsl__izpem = tuple(iqej__hst.values())
        for aiqge__bnp in ('head', 'ngroup'):
            if aiqge__bnp in nsl__izpem:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {aiqge__bnp} cannot be mixed with other groupby operations.'
                    )
        if any(guuh__yag not in grp.selection and guuh__yag not in grp.keys for
            guuh__yag in gcl__gyt):
            raise_bodo_error(
                f'Selected column names {gcl__gyt} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            nsl__izpem)
        if mkxi__fqpkz and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        hnlb__ehsj = {}
        out_columns = []
        out_data = []
        out_column_type = []
        jaxbb__hip = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for lolyb__cbh, f_val in zip(gcl__gyt, nsl__izpem):
            if isinstance(f_val, (tuple, list)):
                ajvyb__obyy = 0
                for muccv__mikks in f_val:
                    oywa__xmzh, out_tp = get_agg_funcname_and_outtyp(grp,
                        lolyb__cbh, muccv__mikks, typing_context,
                        target_context, raise_on_any_error)
                    okzes__iae = oywa__xmzh in list_cumulative
                    if oywa__xmzh == '<lambda>' and len(f_val) > 1:
                        oywa__xmzh = '<lambda_' + str(ajvyb__obyy) + '>'
                        ajvyb__obyy += 1
                    out_columns.append((lolyb__cbh, oywa__xmzh))
                    hnlb__ehsj[lolyb__cbh, oywa__xmzh] = lolyb__cbh, oywa__xmzh
                    _append_out_type(grp, out_data, out_tp)
            else:
                oywa__xmzh, out_tp = get_agg_funcname_and_outtyp(grp,
                    lolyb__cbh, f_val, typing_context, target_context,
                    raise_on_any_error)
                okzes__iae = oywa__xmzh in list_cumulative
                if multi_level_names:
                    out_columns.append((lolyb__cbh, oywa__xmzh))
                    hnlb__ehsj[lolyb__cbh, oywa__xmzh] = lolyb__cbh, oywa__xmzh
                elif not mkxi__fqpkz:
                    out_columns.append(lolyb__cbh)
                    hnlb__ehsj[lolyb__cbh, oywa__xmzh] = lolyb__cbh
                elif mkxi__fqpkz:
                    jaxbb__hip.append(oywa__xmzh)
                _append_out_type(grp, out_data, out_tp)
        if mkxi__fqpkz:
            for fwnkk__wlz, wgfek__xgn in enumerate(kws.keys()):
                out_columns.append(wgfek__xgn)
                hnlb__ehsj[gcl__gyt[fwnkk__wlz], jaxbb__hip[fwnkk__wlz]
                    ] = wgfek__xgn
        if okzes__iae:
            index = grp.df_type.index
        else:
            index = out_tp.index
        oga__lvlo = DataFrameType(tuple(out_data), index, tuple(out_columns
            ), is_table_format=True)
        return signature(oga__lvlo, *args), hnlb__ehsj
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            qbue__rudzg = get_overload_const_list(func)
        else:
            qbue__rudzg = func.types
        if len(qbue__rudzg) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        ajvyb__obyy = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        hnlb__ehsj = {}
        sclbg__voz = grp.selection[0]
        for f_val in qbue__rudzg:
            oywa__xmzh, out_tp = get_agg_funcname_and_outtyp(grp,
                sclbg__voz, f_val, typing_context, target_context,
                raise_on_any_error)
            okzes__iae = oywa__xmzh in list_cumulative
            if oywa__xmzh == '<lambda>' and len(qbue__rudzg) > 1:
                oywa__xmzh = '<lambda_' + str(ajvyb__obyy) + '>'
                ajvyb__obyy += 1
            out_columns.append(oywa__xmzh)
            hnlb__ehsj[sclbg__voz, oywa__xmzh] = oywa__xmzh
            _append_out_type(grp, out_data, out_tp)
        if okzes__iae:
            index = grp.df_type.index
        else:
            index = out_tp.index
        oga__lvlo = DataFrameType(tuple(out_data), index, tuple(out_columns
            ), is_table_format=True)
        return signature(oga__lvlo, *args), hnlb__ehsj
    oywa__xmzh = ''
    if types.unliteral(func) == types.unicode_type:
        oywa__xmzh = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        oywa__xmzh = bodo.utils.typing.get_builtin_function_name(func)
    if oywa__xmzh:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, oywa__xmzh, typing_context, kws)
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
        ymzz__lzvwm = args[0] if len(args) > 0 else kws.pop('axis', 0)
        ewo__csxza = args[1] if len(args) > 1 else kws.pop('numeric_only', 
            False)
        obh__nkab = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        dsy__unt = dict(axis=ymzz__lzvwm, numeric_only=ewo__csxza)
        frmrz__irq = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', dsy__unt,
            frmrz__irq, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        dbiy__czlsi = args[0] if len(args) > 0 else kws.pop('periods', 1)
        jsbjj__yks = args[1] if len(args) > 1 else kws.pop('freq', None)
        ymzz__lzvwm = args[2] if len(args) > 2 else kws.pop('axis', 0)
        lnse__ycp = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        dsy__unt = dict(freq=jsbjj__yks, axis=ymzz__lzvwm, fill_value=lnse__ycp
            )
        frmrz__irq = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', dsy__unt,
            frmrz__irq, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        cryrl__tjhxn = args[0] if len(args) > 0 else kws.pop('func', None)
        yaaxi__eqjp = kws.pop('engine', None)
        idxw__xwr = kws.pop('engine_kwargs', None)
        dsy__unt = dict(engine=yaaxi__eqjp, engine_kwargs=idxw__xwr)
        frmrz__irq = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', dsy__unt, frmrz__irq,
            package_name='pandas', module_name='GroupBy')
    hnlb__ehsj = {}
    for guuh__yag in grp.selection:
        out_columns.append(guuh__yag)
        hnlb__ehsj[guuh__yag, name_operation] = guuh__yag
        ticg__elpm = grp.df_type.column_index[guuh__yag]
        data = grp.df_type.data[ticg__elpm]
        fekgw__xjfau = (name_operation if name_operation != 'transform' else
            get_literal_value(cryrl__tjhxn))
        if fekgw__xjfau in ('sum', 'cumsum'):
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
            nvflu__nweu, err_msg = get_groupby_output_dtype(data,
                get_literal_value(cryrl__tjhxn), grp.df_type.index)
            if err_msg == 'ok':
                data = nvflu__nweu
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    oga__lvlo = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        oga__lvlo = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(oga__lvlo, *args), hnlb__ehsj


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
        qpbu__nxwm = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        xte__rfqch = isinstance(qpbu__nxwm, (SeriesType,
            HeterogeneousSeriesType)
            ) and qpbu__nxwm.const_info is not None or not isinstance(
            qpbu__nxwm, (SeriesType, DataFrameType))
        if xte__rfqch:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                hcvhv__nfer = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                ngb__lovs = tuple(grp.df_type.column_index[grp.keys[
                    fwnkk__wlz]] for fwnkk__wlz in range(len(grp.keys)))
                iabz__guf = tuple(grp.df_type.data[ticg__elpm] for
                    ticg__elpm in ngb__lovs)
                hcvhv__nfer = MultiIndexType(iabz__guf, tuple(types.literal
                    (ckurj__ozz) for ckurj__ozz in grp.keys))
            else:
                ticg__elpm = grp.df_type.column_index[grp.keys[0]]
                rms__refh = grp.df_type.data[ticg__elpm]
                hcvhv__nfer = bodo.hiframes.pd_index_ext.array_type_to_index(
                    rms__refh, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            anm__bwaq = tuple(grp.df_type.data[grp.df_type.column_index[
                guuh__yag]] for guuh__yag in grp.keys)
            rlh__esza = tuple(types.literal(fcs__avq) for fcs__avq in grp.keys
                ) + get_index_name_types(qpbu__nxwm.index)
            if not grp.as_index:
                anm__bwaq = types.Array(types.int64, 1, 'C'),
                rlh__esza = (types.none,) + get_index_name_types(qpbu__nxwm
                    .index)
            hcvhv__nfer = MultiIndexType(anm__bwaq +
                get_index_data_arr_types(qpbu__nxwm.index), rlh__esza)
        if xte__rfqch:
            if isinstance(qpbu__nxwm, HeterogeneousSeriesType):
                nwwif__jrf, tkm__brla = qpbu__nxwm.const_info
                if isinstance(qpbu__nxwm.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    secq__ekbh = qpbu__nxwm.data.tuple_typ.types
                elif isinstance(qpbu__nxwm.data, types.Tuple):
                    secq__ekbh = qpbu__nxwm.data.types
                foy__yesld = tuple(to_nullable_type(dtype_to_array_type(
                    jlw__hys)) for jlw__hys in secq__ekbh)
                bwma__hkzsh = DataFrameType(out_data + foy__yesld,
                    hcvhv__nfer, out_columns + tkm__brla)
            elif isinstance(qpbu__nxwm, SeriesType):
                egcr__avrcu, tkm__brla = qpbu__nxwm.const_info
                foy__yesld = tuple(to_nullable_type(dtype_to_array_type(
                    qpbu__nxwm.dtype)) for nwwif__jrf in range(egcr__avrcu))
                bwma__hkzsh = DataFrameType(out_data + foy__yesld,
                    hcvhv__nfer, out_columns + tkm__brla)
            else:
                avcj__cqug = get_udf_out_arr_type(qpbu__nxwm)
                if not grp.as_index:
                    bwma__hkzsh = DataFrameType(out_data + (avcj__cqug,),
                        hcvhv__nfer, out_columns + ('',))
                else:
                    bwma__hkzsh = SeriesType(avcj__cqug.dtype, avcj__cqug,
                        hcvhv__nfer, None)
        elif isinstance(qpbu__nxwm, SeriesType):
            bwma__hkzsh = SeriesType(qpbu__nxwm.dtype, qpbu__nxwm.data,
                hcvhv__nfer, qpbu__nxwm.name_typ)
        else:
            bwma__hkzsh = DataFrameType(qpbu__nxwm.data, hcvhv__nfer,
                qpbu__nxwm.columns)
        aemnd__hgtj = gen_apply_pysig(len(f_args), kws.keys())
        nnkzo__fzqk = (func, *f_args) + tuple(kws.values())
        return signature(bwma__hkzsh, *nnkzo__fzqk).replace(pysig=aemnd__hgtj)

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
    xctlk__nba = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            lolyb__cbh = grp.selection[0]
            avcj__cqug = xctlk__nba.data[xctlk__nba.column_index[lolyb__cbh]]
            xeohn__vnrt = SeriesType(avcj__cqug.dtype, avcj__cqug,
                xctlk__nba.index, types.literal(lolyb__cbh))
        else:
            wbg__uvgn = tuple(xctlk__nba.data[xctlk__nba.column_index[
                guuh__yag]] for guuh__yag in grp.selection)
            xeohn__vnrt = DataFrameType(wbg__uvgn, xctlk__nba.index, tuple(
                grp.selection))
    else:
        xeohn__vnrt = xctlk__nba
    fiyz__ebcy = xeohn__vnrt,
    fiyz__ebcy += tuple(f_args)
    try:
        qpbu__nxwm = get_const_func_output_type(func, fiyz__ebcy, kws,
            typing_context, target_context)
    except Exception as xtsl__ebjj:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', xtsl__ebjj),
            getattr(xtsl__ebjj, 'loc', None))
    return qpbu__nxwm


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    fiyz__ebcy = (grp,) + f_args
    try:
        qpbu__nxwm = get_const_func_output_type(func, fiyz__ebcy, kws, self
            .context, numba.core.registry.cpu_target.target_context, False)
    except Exception as xtsl__ebjj:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', xtsl__ebjj
            ), getattr(xtsl__ebjj, 'loc', None))
    aemnd__hgtj = gen_apply_pysig(len(f_args), kws.keys())
    nnkzo__fzqk = (func, *f_args) + tuple(kws.values())
    return signature(qpbu__nxwm, *nnkzo__fzqk).replace(pysig=aemnd__hgtj)


def gen_apply_pysig(n_args, kws):
    isp__pfvd = ', '.join(f'arg{fwnkk__wlz}' for fwnkk__wlz in range(n_args))
    isp__pfvd = isp__pfvd + ', ' if isp__pfvd else ''
    epmyi__cpicq = ', '.join(f"{uxog__xcsfh} = ''" for uxog__xcsfh in kws)
    akf__idmtl = f'def apply_stub(func, {isp__pfvd}{epmyi__cpicq}):\n'
    akf__idmtl += '    pass\n'
    qracy__and = {}
    exec(akf__idmtl, {}, qracy__and)
    xau__ajy = qracy__and['apply_stub']
    return numba.core.utils.pysignature(xau__ajy)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        kgl__wjkt = types.Array(types.int64, 1, 'C')
        tvtg__pdoqb = _pivot_values.meta
        hina__rsb = len(tvtg__pdoqb)
        aube__jown = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        bgsjm__dhasb = DataFrameType((kgl__wjkt,) * hina__rsb, aube__jown,
            tuple(tvtg__pdoqb))
        return signature(bgsjm__dhasb, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    akf__idmtl = 'def impl(keys, dropna, _is_parallel):\n'
    akf__idmtl += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    akf__idmtl += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{fwnkk__wlz}])' for fwnkk__wlz in range(len(
        keys.types))))
    akf__idmtl += '    table = arr_info_list_to_table(info_list)\n'
    akf__idmtl += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    akf__idmtl += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    akf__idmtl += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    akf__idmtl += '    delete_table_decref_arrays(table)\n'
    akf__idmtl += '    ev.finalize()\n'
    akf__idmtl += '    return sort_idx, group_labels, ngroups\n'
    qracy__and = {}
    exec(akf__idmtl, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, qracy__and)
    uow__vntbp = qracy__and['impl']
    return uow__vntbp


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    jik__dhz = len(labels)
    neu__yxtwp = np.zeros(ngroups, dtype=np.int64)
    qvbgr__pfv = np.zeros(ngroups, dtype=np.int64)
    bwiid__rmwpm = 0
    zmpec__ahyl = 0
    for fwnkk__wlz in range(jik__dhz):
        rwlel__fayr = labels[fwnkk__wlz]
        if rwlel__fayr < 0:
            bwiid__rmwpm += 1
        else:
            zmpec__ahyl += 1
            if fwnkk__wlz == jik__dhz - 1 or rwlel__fayr != labels[
                fwnkk__wlz + 1]:
                neu__yxtwp[rwlel__fayr] = bwiid__rmwpm
                qvbgr__pfv[rwlel__fayr] = bwiid__rmwpm + zmpec__ahyl
                bwiid__rmwpm += zmpec__ahyl
                zmpec__ahyl = 0
    return neu__yxtwp, qvbgr__pfv


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    uow__vntbp, nwwif__jrf = gen_shuffle_dataframe(df, keys, _is_parallel)
    return uow__vntbp


def gen_shuffle_dataframe(df, keys, _is_parallel):
    egcr__avrcu = len(df.columns)
    nfz__cxm = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    akf__idmtl = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        akf__idmtl += '  return df, keys, get_null_shuffle_info()\n'
        qracy__and = {}
        exec(akf__idmtl, {'get_null_shuffle_info': get_null_shuffle_info},
            qracy__and)
        uow__vntbp = qracy__and['impl']
        return uow__vntbp
    for fwnkk__wlz in range(egcr__avrcu):
        akf__idmtl += f"""  in_arr{fwnkk__wlz} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {fwnkk__wlz})
"""
    akf__idmtl += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    akf__idmtl += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{fwnkk__wlz}])' for fwnkk__wlz in range(
        nfz__cxm)), ', '.join(f'array_to_info(in_arr{fwnkk__wlz})' for
        fwnkk__wlz in range(egcr__avrcu)), 'array_to_info(in_index_arr)')
    akf__idmtl += '  table = arr_info_list_to_table(info_list)\n'
    akf__idmtl += (
        f'  out_table = shuffle_table(table, {nfz__cxm}, _is_parallel, 1)\n')
    for fwnkk__wlz in range(nfz__cxm):
        akf__idmtl += f"""  out_key{fwnkk__wlz} = info_to_array(info_from_table(out_table, {fwnkk__wlz}), keys{fwnkk__wlz}_typ)
"""
    for fwnkk__wlz in range(egcr__avrcu):
        akf__idmtl += f"""  out_arr{fwnkk__wlz} = info_to_array(info_from_table(out_table, {fwnkk__wlz + nfz__cxm}), in_arr{fwnkk__wlz}_typ)
"""
    akf__idmtl += f"""  out_arr_index = info_to_array(info_from_table(out_table, {nfz__cxm + egcr__avrcu}), ind_arr_typ)
"""
    akf__idmtl += '  shuffle_info = get_shuffle_info(out_table)\n'
    akf__idmtl += '  delete_table(out_table)\n'
    akf__idmtl += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{fwnkk__wlz}' for fwnkk__wlz in range(
        egcr__avrcu))
    akf__idmtl += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    akf__idmtl += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    akf__idmtl += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{fwnkk__wlz}' for fwnkk__wlz in range(nfz__cxm)))
    lebd__yfpns = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    lebd__yfpns.update({f'keys{fwnkk__wlz}_typ': keys.types[fwnkk__wlz] for
        fwnkk__wlz in range(nfz__cxm)})
    lebd__yfpns.update({f'in_arr{fwnkk__wlz}_typ': df.data[fwnkk__wlz] for
        fwnkk__wlz in range(egcr__avrcu)})
    qracy__and = {}
    exec(akf__idmtl, lebd__yfpns, qracy__and)
    uow__vntbp = qracy__and['impl']
    return uow__vntbp, lebd__yfpns


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        zfau__fywgj = len(data.array_types)
        akf__idmtl = 'def impl(data, shuffle_info):\n'
        akf__idmtl += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{fwnkk__wlz}])' for fwnkk__wlz in
            range(zfau__fywgj)))
        akf__idmtl += '  table = arr_info_list_to_table(info_list)\n'
        akf__idmtl += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for fwnkk__wlz in range(zfau__fywgj):
            akf__idmtl += f"""  out_arr{fwnkk__wlz} = info_to_array(info_from_table(out_table, {fwnkk__wlz}), data._data[{fwnkk__wlz}])
"""
        akf__idmtl += '  delete_table(out_table)\n'
        akf__idmtl += '  delete_table(table)\n'
        akf__idmtl += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{fwnkk__wlz}' for fwnkk__wlz in range
            (zfau__fywgj))))
        qracy__and = {}
        exec(akf__idmtl, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, qracy__and)
        uow__vntbp = qracy__and['impl']
        return uow__vntbp
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            bma__tlgp = bodo.utils.conversion.index_to_array(data)
            xyc__jowb = reverse_shuffle(bma__tlgp, shuffle_info)
            return bodo.utils.conversion.index_from_array(xyc__jowb)
        return impl_index

    def impl_arr(data, shuffle_info):
        zhx__xslqv = [array_to_info(data)]
        oyjk__utlbk = arr_info_list_to_table(zhx__xslqv)
        ipdpe__jiokp = reverse_shuffle_table(oyjk__utlbk, shuffle_info)
        xyc__jowb = info_to_array(info_from_table(ipdpe__jiokp, 0), data)
        delete_table(ipdpe__jiokp)
        delete_table(oyjk__utlbk)
        return xyc__jowb
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    dsy__unt = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    frmrz__irq = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', dsy__unt, frmrz__irq,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    xfo__rxh = get_overload_const_bool(ascending)
    ltvz__pbwyh = grp.selection[0]
    akf__idmtl = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    lyl__inv = (
        f"lambda S: S.value_counts(ascending={xfo__rxh}, _index_name='{ltvz__pbwyh}')"
        )
    akf__idmtl += f'    return grp.apply({lyl__inv})\n'
    qracy__and = {}
    exec(akf__idmtl, {'bodo': bodo}, qracy__and)
    uow__vntbp = qracy__and['impl']
    return uow__vntbp


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
    for wcfzl__ymptj in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, wcfzl__ymptj, no_unliteral
            =True)(create_unsupported_overload(
            f'DataFrameGroupBy.{wcfzl__ymptj}'))
    for wcfzl__ymptj in groupby_unsupported:
        overload_method(DataFrameGroupByType, wcfzl__ymptj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{wcfzl__ymptj}'))
    for wcfzl__ymptj in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, wcfzl__ymptj, no_unliteral
            =True)(create_unsupported_overload(f'SeriesGroupBy.{wcfzl__ymptj}')
            )
    for wcfzl__ymptj in series_only_unsupported:
        overload_method(DataFrameGroupByType, wcfzl__ymptj, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{wcfzl__ymptj}'))
    for wcfzl__ymptj in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, wcfzl__ymptj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{wcfzl__ymptj}'))


_install_groupby_unsupported()
