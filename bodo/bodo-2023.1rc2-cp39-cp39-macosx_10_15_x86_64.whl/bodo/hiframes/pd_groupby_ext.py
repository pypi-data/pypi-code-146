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
        hqsw__faa = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, hqsw__faa)


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
        pozi__wbn = args[0]
        joxp__rwyek = signature.return_type
        sxdq__xuyuy = cgutils.create_struct_proxy(joxp__rwyek)(context, builder
            )
        sxdq__xuyuy.obj = pozi__wbn
        context.nrt.incref(builder, signature.args[0], pozi__wbn)
        return sxdq__xuyuy._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for txqm__fjnvy in keys:
        selection.remove(txqm__fjnvy)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        jix__fgf = get_overload_const_int(_num_shuffle_keys)
    else:
        jix__fgf = -1
    joxp__rwyek = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=jix__fgf)
    return joxp__rwyek(obj_type, by_type, as_index_type, dropna_type,
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
        grpby, ugf__nzfag = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(ugf__nzfag, (tuple, list)):
                if len(set(ugf__nzfag).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(ugf__nzfag).difference(set(grpby.
                        df_type.columns))))
                selection = ugf__nzfag
            else:
                if ugf__nzfag not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(ugf__nzfag))
                selection = ugf__nzfag,
                series_select = True
            qzfix__nflml = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(qzfix__nflml, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, ugf__nzfag = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            ugf__nzfag):
            qzfix__nflml = StaticGetItemDataFrameGroupBy.generic(self, (
                grpby, get_literal_value(ugf__nzfag)), {}).return_type
            return signature(qzfix__nflml, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    tta__ptib = arr_type == ArrayItemArrayType(string_array_type)
    pmsct__pruee = arr_type.dtype
    if isinstance(pmsct__pruee, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {pmsct__pruee} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(pmsct__pruee, (
        Decimal128Type, types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    elif func_name in ('first', 'last', 'sum', 'prod', 'min', 'max',
        'count', 'nunique', 'head') and isinstance(arr_type, (
        TupleArrayType, ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {pmsct__pruee} is not supported in groupby built-in function {func_name}'
            )
    elif func_name in {'median', 'mean', 'var', 'std'} and isinstance(
        pmsct__pruee, (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    elif func_name == 'boolor_agg':
        if isinstance(pmsct__pruee, (Decimal128Type, types.Integer, types.
            Float, types.Boolean)):
            return bodo.boolean_array, 'ok'
        return (None,
            f'For boolor_agg, only columns of type integer, float, Decimal, or boolean type are allowed'
            )
    if not isinstance(pmsct__pruee, (types.Integer, types.Float, types.Boolean)
        ):
        if tta__ptib or pmsct__pruee == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(pmsct__pruee, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not pmsct__pruee.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {pmsct__pruee} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(pmsct__pruee, types.Boolean) and func_name in {'cumsum',
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
    pmsct__pruee = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(pmsct__pruee, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(pmsct__pruee, types.Integer):
            return IntDtype(pmsct__pruee)
        return pmsct__pruee
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        zjivs__tko = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{zjivs__tko}'."
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
    for txqm__fjnvy in grp.keys:
        if multi_level_names:
            oiu__ykmzn = txqm__fjnvy, ''
        else:
            oiu__ykmzn = txqm__fjnvy
        doli__wllg = grp.df_type.column_index[txqm__fjnvy]
        data = grp.df_type.data[doli__wllg]
        out_columns.append(oiu__ykmzn)
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
        dqv__xqznn = tuple(grp.df_type.column_index[grp.keys[umy__bcaep]] for
            umy__bcaep in range(len(grp.keys)))
        ovun__zuz = tuple(grp.df_type.data[doli__wllg] for doli__wllg in
            dqv__xqznn)
        index = MultiIndexType(ovun__zuz, tuple(types.StringLiteral(
            txqm__fjnvy) for txqm__fjnvy in grp.keys))
    else:
        doli__wllg = grp.df_type.column_index[grp.keys[0]]
        smb__btxjz = grp.df_type.data[doli__wllg]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(smb__btxjz,
            types.StringLiteral(grp.keys[0]))
    kpo__pqvj = {}
    klgi__ajo = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        kpo__pqvj[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        kpo__pqvj[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        vsxfq__tcxeu = dict(ascending=ascending)
        irvi__kklt = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', vsxfq__tcxeu,
            irvi__kklt, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for disbi__dskb in columns:
            doli__wllg = grp.df_type.column_index[disbi__dskb]
            data = grp.df_type.data[doli__wllg]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            bryl__yqb = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType,
                FloatingArrayType)) and isinstance(data.dtype, (types.
                Integer, types.Float)):
                bryl__yqb = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    hwm__qggt = SeriesType(data.dtype, data, None, string_type)
                    kuyk__nophv = get_const_func_output_type(func, (
                        hwm__qggt,), {}, typing_context, target_context)
                    if kuyk__nophv != ArrayItemArrayType(string_array_type):
                        kuyk__nophv = dtype_to_array_type(kuyk__nophv)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=disbi__dskb, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    tjv__wpgvx = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    ouu__rrpd = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    vsxfq__tcxeu = dict(numeric_only=tjv__wpgvx, min_count=
                        ouu__rrpd)
                    irvi__kklt = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vsxfq__tcxeu, irvi__kklt, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    tjv__wpgvx = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    ouu__rrpd = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    vsxfq__tcxeu = dict(numeric_only=tjv__wpgvx, min_count=
                        ouu__rrpd)
                    irvi__kklt = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vsxfq__tcxeu, irvi__kklt, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    tjv__wpgvx = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    vsxfq__tcxeu = dict(numeric_only=tjv__wpgvx)
                    irvi__kklt = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vsxfq__tcxeu, irvi__kklt, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    onjw__cfk = args[0] if len(args) > 0 else kws.pop('axis', 0
                        )
                    lvc__qcet = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    vsxfq__tcxeu = dict(axis=onjw__cfk, skipna=lvc__qcet)
                    irvi__kklt = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vsxfq__tcxeu, irvi__kklt, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    nudf__vha = args[0] if len(args) > 0 else kws.pop('ddof', 1
                        )
                    vsxfq__tcxeu = dict(ddof=nudf__vha)
                    irvi__kklt = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vsxfq__tcxeu, irvi__kklt, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                kuyk__nophv, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                kuyk__nophv = to_str_arr_if_dict_array(kuyk__nophv
                    ) if func_name in ('sum', 'cumsum') else kuyk__nophv
                out_data.append(kuyk__nophv)
                out_columns.append(disbi__dskb)
                if func_name == 'agg':
                    qchz__tmh = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    kpo__pqvj[disbi__dskb, qchz__tmh] = disbi__dskb
                else:
                    kpo__pqvj[disbi__dskb, func_name] = disbi__dskb
                out_column_type.append(bryl__yqb)
            elif raise_on_any_error:
                raise BodoError(
                    f'Groupby with function {func_name} not supported. Error message: {err_msg}'
                    )
            else:
                klgi__ajo.append(err_msg)
    if func_name == 'sum':
        fwnw__bnj = any([(mwtb__uljoc == ColumnType.NumericalColumn.value) for
            mwtb__uljoc in out_column_type])
        if fwnw__bnj:
            out_data = [mwtb__uljoc for mwtb__uljoc, xzks__czn in zip(
                out_data, out_column_type) if xzks__czn != ColumnType.
                NonNumericalColumn.value]
            out_columns = [mwtb__uljoc for mwtb__uljoc, xzks__czn in zip(
                out_columns, out_column_type) if xzks__czn != ColumnType.
                NonNumericalColumn.value]
            kpo__pqvj = {}
            for disbi__dskb in out_columns:
                if grp.as_index is False and disbi__dskb in grp.keys:
                    continue
                kpo__pqvj[disbi__dskb, func_name] = disbi__dskb
    jtkiq__szz = len(klgi__ajo)
    if len(out_data) == 0:
        if jtkiq__szz == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(jtkiq__szz, ' was' if jtkiq__szz == 1 else 's were',
                ','.join(klgi__ajo)))
    slo__pzuzq = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            uyu__keigc = IntDtype(out_data[0].dtype)
        elif isinstance(out_data[0], FloatingArrayType):
            uyu__keigc = FloatDtype(out_data[0].dtype)
        else:
            uyu__keigc = out_data[0].dtype
        fjhc__vixdu = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        slo__pzuzq = SeriesType(uyu__keigc, data=out_data[0], index=index,
            name_typ=fjhc__vixdu)
    return signature(slo__pzuzq, *args), kpo__pqvj


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context,
    target_context, raise_on_any_error):
    npwnn__tru = True
    if isinstance(f_val, str):
        npwnn__tru = False
        gtgb__mjyu = f_val
    elif is_overload_constant_str(f_val):
        npwnn__tru = False
        gtgb__mjyu = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        npwnn__tru = False
        gtgb__mjyu = bodo.utils.typing.get_builtin_function_name(f_val)
    if not npwnn__tru:
        if gtgb__mjyu not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {gtgb__mjyu}')
        qzfix__nflml = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(qzfix__nflml, (), gtgb__mjyu, typing_context,
            target_context, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    else:
        if is_expr(f_val, 'make_function'):
            qrpld__ldhp = types.functions.MakeFunctionLiteral(f_val)
        else:
            qrpld__ldhp = f_val
        validate_udf('agg', qrpld__ldhp)
        func = get_overload_const_func(qrpld__ldhp, None)
        nhvsx__oraqb = func.code if hasattr(func, 'code') else func.__code__
        gtgb__mjyu = nhvsx__oraqb.co_name
        qzfix__nflml = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(qzfix__nflml, (), 'agg', typing_context,
            target_context, qrpld__ldhp, raise_on_any_error=raise_on_any_error
            )[0].return_type
    return gtgb__mjyu, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    jsamj__ebvo = kws and all(isinstance(vvef__esod, types.Tuple) and len(
        vvef__esod) == 2 for vvef__esod in kws.values())
    raise_on_any_error = jsamj__ebvo
    if is_overload_none(func) and not jsamj__ebvo:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not jsamj__ebvo:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    zvv__rnql = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if jsamj__ebvo or is_overload_constant_dict(func):
        if jsamj__ebvo:
            yjqv__ltae = [get_literal_value(prs__gobp) for prs__gobp,
                vvsh__hrqu in kws.values()]
            gcol__eybs = [get_literal_value(eww__wnui) for vvsh__hrqu,
                eww__wnui in kws.values()]
        else:
            pii__elu = get_overload_constant_dict(func)
            yjqv__ltae = tuple(pii__elu.keys())
            gcol__eybs = tuple(pii__elu.values())
        for vlx__rjpou in ('head', 'ngroup'):
            if vlx__rjpou in gcol__eybs:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {vlx__rjpou} cannot be mixed with other groupby operations.'
                    )
        if any(disbi__dskb not in grp.selection and disbi__dskb not in grp.
            keys for disbi__dskb in yjqv__ltae):
            raise_bodo_error(
                f'Selected column names {yjqv__ltae} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            gcol__eybs)
        if jsamj__ebvo and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        kpo__pqvj = {}
        out_columns = []
        out_data = []
        out_column_type = []
        oqycm__gck = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for tjxj__egkrt, f_val in zip(yjqv__ltae, gcol__eybs):
            if isinstance(f_val, (tuple, list)):
                dsp__erhch = 0
                for qrpld__ldhp in f_val:
                    gtgb__mjyu, out_tp = get_agg_funcname_and_outtyp(grp,
                        tjxj__egkrt, qrpld__ldhp, typing_context,
                        target_context, raise_on_any_error)
                    zvv__rnql = gtgb__mjyu in list_cumulative
                    if gtgb__mjyu == '<lambda>' and len(f_val) > 1:
                        gtgb__mjyu = '<lambda_' + str(dsp__erhch) + '>'
                        dsp__erhch += 1
                    out_columns.append((tjxj__egkrt, gtgb__mjyu))
                    kpo__pqvj[tjxj__egkrt, gtgb__mjyu
                        ] = tjxj__egkrt, gtgb__mjyu
                    _append_out_type(grp, out_data, out_tp)
            else:
                gtgb__mjyu, out_tp = get_agg_funcname_and_outtyp(grp,
                    tjxj__egkrt, f_val, typing_context, target_context,
                    raise_on_any_error)
                zvv__rnql = gtgb__mjyu in list_cumulative
                if multi_level_names:
                    out_columns.append((tjxj__egkrt, gtgb__mjyu))
                    kpo__pqvj[tjxj__egkrt, gtgb__mjyu
                        ] = tjxj__egkrt, gtgb__mjyu
                elif not jsamj__ebvo:
                    out_columns.append(tjxj__egkrt)
                    kpo__pqvj[tjxj__egkrt, gtgb__mjyu] = tjxj__egkrt
                elif jsamj__ebvo:
                    oqycm__gck.append(gtgb__mjyu)
                _append_out_type(grp, out_data, out_tp)
        if jsamj__ebvo:
            for umy__bcaep, phuys__kjq in enumerate(kws.keys()):
                out_columns.append(phuys__kjq)
                kpo__pqvj[yjqv__ltae[umy__bcaep], oqycm__gck[umy__bcaep]
                    ] = phuys__kjq
        if zvv__rnql:
            index = grp.df_type.index
        else:
            index = out_tp.index
        slo__pzuzq = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(slo__pzuzq, *args), kpo__pqvj
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            psi__aqq = get_overload_const_list(func)
        else:
            psi__aqq = func.types
        if len(psi__aqq) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        dsp__erhch = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        kpo__pqvj = {}
        dxk__uyjba = grp.selection[0]
        for f_val in psi__aqq:
            gtgb__mjyu, out_tp = get_agg_funcname_and_outtyp(grp,
                dxk__uyjba, f_val, typing_context, target_context,
                raise_on_any_error)
            zvv__rnql = gtgb__mjyu in list_cumulative
            if gtgb__mjyu == '<lambda>' and len(psi__aqq) > 1:
                gtgb__mjyu = '<lambda_' + str(dsp__erhch) + '>'
                dsp__erhch += 1
            out_columns.append(gtgb__mjyu)
            kpo__pqvj[dxk__uyjba, gtgb__mjyu] = gtgb__mjyu
            _append_out_type(grp, out_data, out_tp)
        if zvv__rnql:
            index = grp.df_type.index
        else:
            index = out_tp.index
        slo__pzuzq = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(slo__pzuzq, *args), kpo__pqvj
    gtgb__mjyu = ''
    if types.unliteral(func) == types.unicode_type:
        gtgb__mjyu = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        gtgb__mjyu = bodo.utils.typing.get_builtin_function_name(func)
    if gtgb__mjyu:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, gtgb__mjyu, typing_context, kws)
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
        onjw__cfk = args[0] if len(args) > 0 else kws.pop('axis', 0)
        tjv__wpgvx = args[1] if len(args) > 1 else kws.pop('numeric_only', 
            False)
        lvc__qcet = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        vsxfq__tcxeu = dict(axis=onjw__cfk, numeric_only=tjv__wpgvx)
        irvi__kklt = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', vsxfq__tcxeu,
            irvi__kklt, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        qsis__nch = args[0] if len(args) > 0 else kws.pop('periods', 1)
        mja__gwwha = args[1] if len(args) > 1 else kws.pop('freq', None)
        onjw__cfk = args[2] if len(args) > 2 else kws.pop('axis', 0)
        tosum__nlvl = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        vsxfq__tcxeu = dict(freq=mja__gwwha, axis=onjw__cfk, fill_value=
            tosum__nlvl)
        irvi__kklt = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', vsxfq__tcxeu,
            irvi__kklt, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        aqlcb__fpmq = args[0] if len(args) > 0 else kws.pop('func', None)
        ksq__nloty = kws.pop('engine', None)
        mqrrs__cxkmv = kws.pop('engine_kwargs', None)
        vsxfq__tcxeu = dict(engine=ksq__nloty, engine_kwargs=mqrrs__cxkmv)
        irvi__kklt = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', vsxfq__tcxeu,
            irvi__kklt, package_name='pandas', module_name='GroupBy')
    kpo__pqvj = {}
    for disbi__dskb in grp.selection:
        out_columns.append(disbi__dskb)
        kpo__pqvj[disbi__dskb, name_operation] = disbi__dskb
        doli__wllg = grp.df_type.column_index[disbi__dskb]
        data = grp.df_type.data[doli__wllg]
        jfz__wjsc = (name_operation if name_operation != 'transform' else
            get_literal_value(aqlcb__fpmq))
        if jfz__wjsc in ('sum', 'cumsum'):
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
            kuyk__nophv, err_msg = get_groupby_output_dtype(data,
                get_literal_value(aqlcb__fpmq), grp.df_type.index)
            if err_msg == 'ok':
                data = kuyk__nophv
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    slo__pzuzq = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        slo__pzuzq = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(slo__pzuzq, *args), kpo__pqvj


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
        doyeu__afdz = _get_groupby_apply_udf_out_type(func, grp, f_args,
            kws, self.context, numba.core.registry.cpu_target.target_context)
        zdvf__gsyzr = isinstance(doyeu__afdz, (SeriesType,
            HeterogeneousSeriesType)
            ) and doyeu__afdz.const_info is not None or not isinstance(
            doyeu__afdz, (SeriesType, DataFrameType))
        if zdvf__gsyzr:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                ctxm__vpbn = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                dqv__xqznn = tuple(grp.df_type.column_index[grp.keys[
                    umy__bcaep]] for umy__bcaep in range(len(grp.keys)))
                ovun__zuz = tuple(grp.df_type.data[doli__wllg] for
                    doli__wllg in dqv__xqznn)
                ctxm__vpbn = MultiIndexType(ovun__zuz, tuple(types.literal(
                    txqm__fjnvy) for txqm__fjnvy in grp.keys))
            else:
                doli__wllg = grp.df_type.column_index[grp.keys[0]]
                smb__btxjz = grp.df_type.data[doli__wllg]
                ctxm__vpbn = bodo.hiframes.pd_index_ext.array_type_to_index(
                    smb__btxjz, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            jyc__ruker = tuple(grp.df_type.data[grp.df_type.column_index[
                disbi__dskb]] for disbi__dskb in grp.keys)
            uoa__dxuaa = tuple(types.literal(vvef__esod) for vvef__esod in
                grp.keys) + get_index_name_types(doyeu__afdz.index)
            if not grp.as_index:
                jyc__ruker = types.Array(types.int64, 1, 'C'),
                uoa__dxuaa = (types.none,) + get_index_name_types(doyeu__afdz
                    .index)
            ctxm__vpbn = MultiIndexType(jyc__ruker +
                get_index_data_arr_types(doyeu__afdz.index), uoa__dxuaa)
        if zdvf__gsyzr:
            if isinstance(doyeu__afdz, HeterogeneousSeriesType):
                vvsh__hrqu, zvv__byee = doyeu__afdz.const_info
                if isinstance(doyeu__afdz.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    nnsoc__gdxtv = doyeu__afdz.data.tuple_typ.types
                elif isinstance(doyeu__afdz.data, types.Tuple):
                    nnsoc__gdxtv = doyeu__afdz.data.types
                rmfrf__grmhl = tuple(to_nullable_type(dtype_to_array_type(
                    cqhtz__igq)) for cqhtz__igq in nnsoc__gdxtv)
                nisf__jbo = DataFrameType(out_data + rmfrf__grmhl,
                    ctxm__vpbn, out_columns + zvv__byee)
            elif isinstance(doyeu__afdz, SeriesType):
                emsoz__wzljy, zvv__byee = doyeu__afdz.const_info
                rmfrf__grmhl = tuple(to_nullable_type(dtype_to_array_type(
                    doyeu__afdz.dtype)) for vvsh__hrqu in range(emsoz__wzljy))
                nisf__jbo = DataFrameType(out_data + rmfrf__grmhl,
                    ctxm__vpbn, out_columns + zvv__byee)
            else:
                sspf__msmb = get_udf_out_arr_type(doyeu__afdz)
                if not grp.as_index:
                    nisf__jbo = DataFrameType(out_data + (sspf__msmb,),
                        ctxm__vpbn, out_columns + ('',))
                else:
                    nisf__jbo = SeriesType(sspf__msmb.dtype, sspf__msmb,
                        ctxm__vpbn, None)
        elif isinstance(doyeu__afdz, SeriesType):
            nisf__jbo = SeriesType(doyeu__afdz.dtype, doyeu__afdz.data,
                ctxm__vpbn, doyeu__afdz.name_typ)
        else:
            nisf__jbo = DataFrameType(doyeu__afdz.data, ctxm__vpbn,
                doyeu__afdz.columns)
        qwo__fsyhl = gen_apply_pysig(len(f_args), kws.keys())
        ghutb__putt = (func, *f_args) + tuple(kws.values())
        return signature(nisf__jbo, *ghutb__putt).replace(pysig=qwo__fsyhl)

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
    oio__kkwm = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            tjxj__egkrt = grp.selection[0]
            sspf__msmb = oio__kkwm.data[oio__kkwm.column_index[tjxj__egkrt]]
            zcaqp__gmn = SeriesType(sspf__msmb.dtype, sspf__msmb, oio__kkwm
                .index, types.literal(tjxj__egkrt))
        else:
            hkk__wdjb = tuple(oio__kkwm.data[oio__kkwm.column_index[
                disbi__dskb]] for disbi__dskb in grp.selection)
            zcaqp__gmn = DataFrameType(hkk__wdjb, oio__kkwm.index, tuple(
                grp.selection))
    else:
        zcaqp__gmn = oio__kkwm
    gac__miidb = zcaqp__gmn,
    gac__miidb += tuple(f_args)
    try:
        doyeu__afdz = get_const_func_output_type(func, gac__miidb, kws,
            typing_context, target_context)
    except Exception as ldw__uosed:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', ldw__uosed),
            getattr(ldw__uosed, 'loc', None))
    return doyeu__afdz


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    gac__miidb = (grp,) + f_args
    try:
        doyeu__afdz = get_const_func_output_type(func, gac__miidb, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as ldw__uosed:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', ldw__uosed
            ), getattr(ldw__uosed, 'loc', None))
    qwo__fsyhl = gen_apply_pysig(len(f_args), kws.keys())
    ghutb__putt = (func, *f_args) + tuple(kws.values())
    return signature(doyeu__afdz, *ghutb__putt).replace(pysig=qwo__fsyhl)


def gen_apply_pysig(n_args, kws):
    yolyu__wcai = ', '.join(f'arg{umy__bcaep}' for umy__bcaep in range(n_args))
    yolyu__wcai = yolyu__wcai + ', ' if yolyu__wcai else ''
    jzr__tjfmm = ', '.join(f"{oef__iboic} = ''" for oef__iboic in kws)
    mdz__aqk = f'def apply_stub(func, {yolyu__wcai}{jzr__tjfmm}):\n'
    mdz__aqk += '    pass\n'
    abcg__vqpdj = {}
    exec(mdz__aqk, {}, abcg__vqpdj)
    fhjus__syp = abcg__vqpdj['apply_stub']
    return numba.core.utils.pysignature(fhjus__syp)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        ywez__ryh = types.Array(types.int64, 1, 'C')
        vyb__sed = _pivot_values.meta
        znh__cssl = len(vyb__sed)
        jaig__omthz = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        reib__klqjc = DataFrameType((ywez__ryh,) * znh__cssl, jaig__omthz,
            tuple(vyb__sed))
        return signature(reib__klqjc, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    mdz__aqk = 'def impl(keys, dropna, _is_parallel):\n'
    mdz__aqk += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    mdz__aqk += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{umy__bcaep}])' for umy__bcaep in range(len(
        keys.types))))
    mdz__aqk += '    table = arr_info_list_to_table(info_list)\n'
    mdz__aqk += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    mdz__aqk += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    mdz__aqk += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    mdz__aqk += '    delete_table_decref_arrays(table)\n'
    mdz__aqk += '    ev.finalize()\n'
    mdz__aqk += '    return sort_idx, group_labels, ngroups\n'
    abcg__vqpdj = {}
    exec(mdz__aqk, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, abcg__vqpdj)
    johw__baow = abcg__vqpdj['impl']
    return johw__baow


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    ijsny__mto = len(labels)
    tqkjv__yligv = np.zeros(ngroups, dtype=np.int64)
    vpoe__fgvvg = np.zeros(ngroups, dtype=np.int64)
    zappt__pwqfe = 0
    rncz__bdl = 0
    for umy__bcaep in range(ijsny__mto):
        kvsb__eabs = labels[umy__bcaep]
        if kvsb__eabs < 0:
            zappt__pwqfe += 1
        else:
            rncz__bdl += 1
            if umy__bcaep == ijsny__mto - 1 or kvsb__eabs != labels[
                umy__bcaep + 1]:
                tqkjv__yligv[kvsb__eabs] = zappt__pwqfe
                vpoe__fgvvg[kvsb__eabs] = zappt__pwqfe + rncz__bdl
                zappt__pwqfe += rncz__bdl
                rncz__bdl = 0
    return tqkjv__yligv, vpoe__fgvvg


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    johw__baow, vvsh__hrqu = gen_shuffle_dataframe(df, keys, _is_parallel)
    return johw__baow


def gen_shuffle_dataframe(df, keys, _is_parallel):
    emsoz__wzljy = len(df.columns)
    mlugq__ufzoc = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    mdz__aqk = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        mdz__aqk += '  return df, keys, get_null_shuffle_info()\n'
        abcg__vqpdj = {}
        exec(mdz__aqk, {'get_null_shuffle_info': get_null_shuffle_info},
            abcg__vqpdj)
        johw__baow = abcg__vqpdj['impl']
        return johw__baow
    for umy__bcaep in range(emsoz__wzljy):
        mdz__aqk += f"""  in_arr{umy__bcaep} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {umy__bcaep})
"""
    mdz__aqk += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    mdz__aqk += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{umy__bcaep}])' for umy__bcaep in range(
        mlugq__ufzoc)), ', '.join(f'array_to_info(in_arr{umy__bcaep})' for
        umy__bcaep in range(emsoz__wzljy)), 'array_to_info(in_index_arr)')
    mdz__aqk += '  table = arr_info_list_to_table(info_list)\n'
    mdz__aqk += (
        f'  out_table = shuffle_table(table, {mlugq__ufzoc}, _is_parallel, 1)\n'
        )
    for umy__bcaep in range(mlugq__ufzoc):
        mdz__aqk += f"""  out_key{umy__bcaep} = info_to_array(info_from_table(out_table, {umy__bcaep}), keys{umy__bcaep}_typ)
"""
    for umy__bcaep in range(emsoz__wzljy):
        mdz__aqk += f"""  out_arr{umy__bcaep} = info_to_array(info_from_table(out_table, {umy__bcaep + mlugq__ufzoc}), in_arr{umy__bcaep}_typ)
"""
    mdz__aqk += f"""  out_arr_index = info_to_array(info_from_table(out_table, {mlugq__ufzoc + emsoz__wzljy}), ind_arr_typ)
"""
    mdz__aqk += '  shuffle_info = get_shuffle_info(out_table)\n'
    mdz__aqk += '  delete_table(out_table)\n'
    mdz__aqk += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{umy__bcaep}' for umy__bcaep in range(
        emsoz__wzljy))
    mdz__aqk += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    mdz__aqk += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    mdz__aqk += '  return out_df, ({},), shuffle_info\n'.format(', '.join(
        f'out_key{umy__bcaep}' for umy__bcaep in range(mlugq__ufzoc)))
    tjx__rng = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    tjx__rng.update({f'keys{umy__bcaep}_typ': keys.types[umy__bcaep] for
        umy__bcaep in range(mlugq__ufzoc)})
    tjx__rng.update({f'in_arr{umy__bcaep}_typ': df.data[umy__bcaep] for
        umy__bcaep in range(emsoz__wzljy)})
    abcg__vqpdj = {}
    exec(mdz__aqk, tjx__rng, abcg__vqpdj)
    johw__baow = abcg__vqpdj['impl']
    return johw__baow, tjx__rng


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        pis__zll = len(data.array_types)
        mdz__aqk = 'def impl(data, shuffle_info):\n'
        mdz__aqk += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{umy__bcaep}])' for umy__bcaep in
            range(pis__zll)))
        mdz__aqk += '  table = arr_info_list_to_table(info_list)\n'
        mdz__aqk += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for umy__bcaep in range(pis__zll):
            mdz__aqk += f"""  out_arr{umy__bcaep} = info_to_array(info_from_table(out_table, {umy__bcaep}), data._data[{umy__bcaep}])
"""
        mdz__aqk += '  delete_table(out_table)\n'
        mdz__aqk += '  delete_table(table)\n'
        mdz__aqk += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{umy__bcaep}' for umy__bcaep in range
            (pis__zll))))
        abcg__vqpdj = {}
        exec(mdz__aqk, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, abcg__vqpdj)
        johw__baow = abcg__vqpdj['impl']
        return johw__baow
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            ncxo__yshhg = bodo.utils.conversion.index_to_array(data)
            nyvj__hri = reverse_shuffle(ncxo__yshhg, shuffle_info)
            return bodo.utils.conversion.index_from_array(nyvj__hri)
        return impl_index

    def impl_arr(data, shuffle_info):
        hqfmr__uoa = [array_to_info(data)]
        polkb__mif = arr_info_list_to_table(hqfmr__uoa)
        kefqh__mmr = reverse_shuffle_table(polkb__mif, shuffle_info)
        nyvj__hri = info_to_array(info_from_table(kefqh__mmr, 0), data)
        delete_table(kefqh__mmr)
        delete_table(polkb__mif)
        return nyvj__hri
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    vsxfq__tcxeu = dict(normalize=normalize, sort=sort, bins=bins, dropna=
        dropna)
    irvi__kklt = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', vsxfq__tcxeu, irvi__kklt,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    cls__gxxsh = get_overload_const_bool(ascending)
    num__auaem = grp.selection[0]
    mdz__aqk = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    vxupm__bdgg = (
        f"lambda S: S.value_counts(ascending={cls__gxxsh}, _index_name='{num__auaem}')"
        )
    mdz__aqk += f'    return grp.apply({vxupm__bdgg})\n'
    abcg__vqpdj = {}
    exec(mdz__aqk, {'bodo': bodo}, abcg__vqpdj)
    johw__baow = abcg__vqpdj['impl']
    return johw__baow


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
    for bic__jkdn in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, bic__jkdn, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{bic__jkdn}'))
    for bic__jkdn in groupby_unsupported:
        overload_method(DataFrameGroupByType, bic__jkdn, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{bic__jkdn}'))
    for bic__jkdn in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, bic__jkdn, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{bic__jkdn}'))
    for bic__jkdn in series_only_unsupported:
        overload_method(DataFrameGroupByType, bic__jkdn, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{bic__jkdn}'))
    for bic__jkdn in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, bic__jkdn, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{bic__jkdn}'))


_install_groupby_unsupported()
