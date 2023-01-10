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
        ruiq__ykc = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, ruiq__ykc)


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
        nob__fujr = args[0]
        cngx__uak = signature.return_type
        fxktp__syydo = cgutils.create_struct_proxy(cngx__uak)(context, builder)
        fxktp__syydo.obj = nob__fujr
        context.nrt.incref(builder, signature.args[0], nob__fujr)
        return fxktp__syydo._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for ssd__jtbk in keys:
        selection.remove(ssd__jtbk)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        piex__ayo = get_overload_const_int(_num_shuffle_keys)
    else:
        piex__ayo = -1
    cngx__uak = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=piex__ayo)
    return cngx__uak(obj_type, by_type, as_index_type, dropna_type,
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
        grpby, okklp__wuzz = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(okklp__wuzz, (tuple, list)):
                if len(set(okklp__wuzz).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(okklp__wuzz).difference(set(grpby.
                        df_type.columns))))
                selection = okklp__wuzz
            else:
                if okklp__wuzz not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(okklp__wuzz))
                selection = okklp__wuzz,
                series_select = True
            zrhv__fize = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(zrhv__fize, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, okklp__wuzz = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            okklp__wuzz):
            zrhv__fize = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(okklp__wuzz)), {}).return_type
            return signature(zrhv__fize, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    esuy__meseb = arr_type == ArrayItemArrayType(string_array_type)
    onodz__ghzv = arr_type.dtype
    if isinstance(onodz__ghzv, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {onodz__ghzv} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(onodz__ghzv, (
        Decimal128Type, types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    elif func_name in ('first', 'last', 'sum', 'prod', 'min', 'max',
        'count', 'nunique', 'head') and isinstance(arr_type, (
        TupleArrayType, ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {onodz__ghzv} is not supported in groupby built-in function {func_name}'
            )
    elif func_name in {'median', 'mean', 'var', 'std'} and isinstance(
        onodz__ghzv, (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    elif func_name == 'boolor_agg':
        if isinstance(onodz__ghzv, (Decimal128Type, types.Integer, types.
            Float, types.Boolean)):
            return bodo.boolean_array, 'ok'
        return (None,
            f'For boolor_agg, only columns of type integer, float, Decimal, or boolean type are allowed'
            )
    if not isinstance(onodz__ghzv, (types.Integer, types.Float, types.Boolean)
        ):
        if esuy__meseb or onodz__ghzv == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(onodz__ghzv, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not onodz__ghzv.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {onodz__ghzv} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(onodz__ghzv, types.Boolean) and func_name in {'cumsum',
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
    onodz__ghzv = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(onodz__ghzv, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(onodz__ghzv, types.Integer):
            return IntDtype(onodz__ghzv)
        return onodz__ghzv
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        poa__csgpr = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{poa__csgpr}'."
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
    for ssd__jtbk in grp.keys:
        if multi_level_names:
            nzab__njq = ssd__jtbk, ''
        else:
            nzab__njq = ssd__jtbk
        mocdt__lra = grp.df_type.column_index[ssd__jtbk]
        data = grp.df_type.data[mocdt__lra]
        out_columns.append(nzab__njq)
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
        ckmuw__rkkro = tuple(grp.df_type.column_index[grp.keys[izv__sty]] for
            izv__sty in range(len(grp.keys)))
        ajhew__ezn = tuple(grp.df_type.data[mocdt__lra] for mocdt__lra in
            ckmuw__rkkro)
        index = MultiIndexType(ajhew__ezn, tuple(types.StringLiteral(
            ssd__jtbk) for ssd__jtbk in grp.keys))
    else:
        mocdt__lra = grp.df_type.column_index[grp.keys[0]]
        uuvq__zhe = grp.df_type.data[mocdt__lra]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(uuvq__zhe,
            types.StringLiteral(grp.keys[0]))
    suja__yvunt = {}
    weq__tcpmu = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        suja__yvunt[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        suja__yvunt[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        kofw__sdxp = dict(ascending=ascending)
        awxm__yqbhi = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', kofw__sdxp,
            awxm__yqbhi, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for xpzh__apdx in columns:
            mocdt__lra = grp.df_type.column_index[xpzh__apdx]
            data = grp.df_type.data[mocdt__lra]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            fewp__xqs = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType,
                FloatingArrayType)) and isinstance(data.dtype, (types.
                Integer, types.Float)):
                fewp__xqs = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    fsi__fzm = SeriesType(data.dtype, data, None, string_type)
                    shu__zdjqr = get_const_func_output_type(func, (fsi__fzm
                        ,), {}, typing_context, target_context)
                    if shu__zdjqr != ArrayItemArrayType(string_array_type):
                        shu__zdjqr = dtype_to_array_type(shu__zdjqr)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=xpzh__apdx, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    iit__omr = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    sxoew__ymw = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    kofw__sdxp = dict(numeric_only=iit__omr, min_count=
                        sxoew__ymw)
                    awxm__yqbhi = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        kofw__sdxp, awxm__yqbhi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    iit__omr = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    sxoew__ymw = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    kofw__sdxp = dict(numeric_only=iit__omr, min_count=
                        sxoew__ymw)
                    awxm__yqbhi = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        kofw__sdxp, awxm__yqbhi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    iit__omr = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    kofw__sdxp = dict(numeric_only=iit__omr)
                    awxm__yqbhi = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        kofw__sdxp, awxm__yqbhi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    kwjd__nmcr = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    epnix__kvab = args[1] if len(args) > 1 else kws.pop(
                        'skipna', True)
                    kofw__sdxp = dict(axis=kwjd__nmcr, skipna=epnix__kvab)
                    awxm__yqbhi = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        kofw__sdxp, awxm__yqbhi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    dutfm__trd = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    kofw__sdxp = dict(ddof=dutfm__trd)
                    awxm__yqbhi = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        kofw__sdxp, awxm__yqbhi, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                shu__zdjqr, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                shu__zdjqr = to_str_arr_if_dict_array(shu__zdjqr
                    ) if func_name in ('sum', 'cumsum') else shu__zdjqr
                out_data.append(shu__zdjqr)
                out_columns.append(xpzh__apdx)
                if func_name == 'agg':
                    uda__tqvmd = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    suja__yvunt[xpzh__apdx, uda__tqvmd] = xpzh__apdx
                else:
                    suja__yvunt[xpzh__apdx, func_name] = xpzh__apdx
                out_column_type.append(fewp__xqs)
            elif raise_on_any_error:
                raise BodoError(
                    f'Groupby with function {func_name} not supported. Error message: {err_msg}'
                    )
            else:
                weq__tcpmu.append(err_msg)
    if func_name == 'sum':
        rpx__lxqwb = any([(vreik__vdibq == ColumnType.NumericalColumn.value
            ) for vreik__vdibq in out_column_type])
        if rpx__lxqwb:
            out_data = [vreik__vdibq for vreik__vdibq, aceg__pkoq in zip(
                out_data, out_column_type) if aceg__pkoq != ColumnType.
                NonNumericalColumn.value]
            out_columns = [vreik__vdibq for vreik__vdibq, aceg__pkoq in zip
                (out_columns, out_column_type) if aceg__pkoq != ColumnType.
                NonNumericalColumn.value]
            suja__yvunt = {}
            for xpzh__apdx in out_columns:
                if grp.as_index is False and xpzh__apdx in grp.keys:
                    continue
                suja__yvunt[xpzh__apdx, func_name] = xpzh__apdx
    pxg__dld = len(weq__tcpmu)
    if len(out_data) == 0:
        if pxg__dld == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(pxg__dld, ' was' if pxg__dld == 1 else 's were',
                ','.join(weq__tcpmu)))
    xsss__zsbi = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            cxkbw__vbp = IntDtype(out_data[0].dtype)
        elif isinstance(out_data[0], FloatingArrayType):
            cxkbw__vbp = FloatDtype(out_data[0].dtype)
        else:
            cxkbw__vbp = out_data[0].dtype
        nbd__rgz = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        xsss__zsbi = SeriesType(cxkbw__vbp, data=out_data[0], index=index,
            name_typ=nbd__rgz)
    return signature(xsss__zsbi, *args), suja__yvunt


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context,
    target_context, raise_on_any_error):
    gexw__lbjd = True
    if isinstance(f_val, str):
        gexw__lbjd = False
        aezq__hacwi = f_val
    elif is_overload_constant_str(f_val):
        gexw__lbjd = False
        aezq__hacwi = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        gexw__lbjd = False
        aezq__hacwi = bodo.utils.typing.get_builtin_function_name(f_val)
    if not gexw__lbjd:
        if aezq__hacwi not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {aezq__hacwi}')
        zrhv__fize = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(zrhv__fize, (), aezq__hacwi, typing_context,
            target_context, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    else:
        if is_expr(f_val, 'make_function'):
            znvqy__lywiq = types.functions.MakeFunctionLiteral(f_val)
        else:
            znvqy__lywiq = f_val
        validate_udf('agg', znvqy__lywiq)
        func = get_overload_const_func(znvqy__lywiq, None)
        hge__fzm = func.code if hasattr(func, 'code') else func.__code__
        aezq__hacwi = hge__fzm.co_name
        zrhv__fize = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(zrhv__fize, (), 'agg', typing_context,
            target_context, znvqy__lywiq, raise_on_any_error=raise_on_any_error
            )[0].return_type
    return aezq__hacwi, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    olyg__avv = kws and all(isinstance(chnc__fxxdq, types.Tuple) and len(
        chnc__fxxdq) == 2 for chnc__fxxdq in kws.values())
    raise_on_any_error = olyg__avv
    if is_overload_none(func) and not olyg__avv:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not olyg__avv:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    bgfb__bcts = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if olyg__avv or is_overload_constant_dict(func):
        if olyg__avv:
            lrd__grk = [get_literal_value(sqwn__ykr) for sqwn__ykr,
                igyvu__izyo in kws.values()]
            wkmz__enhm = [get_literal_value(padwd__ujzx) for igyvu__izyo,
                padwd__ujzx in kws.values()]
        else:
            rymg__ldv = get_overload_constant_dict(func)
            lrd__grk = tuple(rymg__ldv.keys())
            wkmz__enhm = tuple(rymg__ldv.values())
        for ots__aaagf in ('head', 'ngroup'):
            if ots__aaagf in wkmz__enhm:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {ots__aaagf} cannot be mixed with other groupby operations.'
                    )
        if any(xpzh__apdx not in grp.selection and xpzh__apdx not in grp.
            keys for xpzh__apdx in lrd__grk):
            raise_bodo_error(
                f'Selected column names {lrd__grk} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            wkmz__enhm)
        if olyg__avv and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        suja__yvunt = {}
        out_columns = []
        out_data = []
        out_column_type = []
        ecqr__ebu = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for kpr__qfez, f_val in zip(lrd__grk, wkmz__enhm):
            if isinstance(f_val, (tuple, list)):
                xpc__dko = 0
                for znvqy__lywiq in f_val:
                    aezq__hacwi, out_tp = get_agg_funcname_and_outtyp(grp,
                        kpr__qfez, znvqy__lywiq, typing_context,
                        target_context, raise_on_any_error)
                    bgfb__bcts = aezq__hacwi in list_cumulative
                    if aezq__hacwi == '<lambda>' and len(f_val) > 1:
                        aezq__hacwi = '<lambda_' + str(xpc__dko) + '>'
                        xpc__dko += 1
                    out_columns.append((kpr__qfez, aezq__hacwi))
                    suja__yvunt[kpr__qfez, aezq__hacwi
                        ] = kpr__qfez, aezq__hacwi
                    _append_out_type(grp, out_data, out_tp)
            else:
                aezq__hacwi, out_tp = get_agg_funcname_and_outtyp(grp,
                    kpr__qfez, f_val, typing_context, target_context,
                    raise_on_any_error)
                bgfb__bcts = aezq__hacwi in list_cumulative
                if multi_level_names:
                    out_columns.append((kpr__qfez, aezq__hacwi))
                    suja__yvunt[kpr__qfez, aezq__hacwi
                        ] = kpr__qfez, aezq__hacwi
                elif not olyg__avv:
                    out_columns.append(kpr__qfez)
                    suja__yvunt[kpr__qfez, aezq__hacwi] = kpr__qfez
                elif olyg__avv:
                    ecqr__ebu.append(aezq__hacwi)
                _append_out_type(grp, out_data, out_tp)
        if olyg__avv:
            for izv__sty, izzl__mbwta in enumerate(kws.keys()):
                out_columns.append(izzl__mbwta)
                suja__yvunt[lrd__grk[izv__sty], ecqr__ebu[izv__sty]
                    ] = izzl__mbwta
        if bgfb__bcts:
            index = grp.df_type.index
        else:
            index = out_tp.index
        xsss__zsbi = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(xsss__zsbi, *args), suja__yvunt
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            envqg__knke = get_overload_const_list(func)
        else:
            envqg__knke = func.types
        if len(envqg__knke) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        xpc__dko = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        suja__yvunt = {}
        hbd__zll = grp.selection[0]
        for f_val in envqg__knke:
            aezq__hacwi, out_tp = get_agg_funcname_and_outtyp(grp, hbd__zll,
                f_val, typing_context, target_context, raise_on_any_error)
            bgfb__bcts = aezq__hacwi in list_cumulative
            if aezq__hacwi == '<lambda>' and len(envqg__knke) > 1:
                aezq__hacwi = '<lambda_' + str(xpc__dko) + '>'
                xpc__dko += 1
            out_columns.append(aezq__hacwi)
            suja__yvunt[hbd__zll, aezq__hacwi] = aezq__hacwi
            _append_out_type(grp, out_data, out_tp)
        if bgfb__bcts:
            index = grp.df_type.index
        else:
            index = out_tp.index
        xsss__zsbi = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(xsss__zsbi, *args), suja__yvunt
    aezq__hacwi = ''
    if types.unliteral(func) == types.unicode_type:
        aezq__hacwi = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        aezq__hacwi = bodo.utils.typing.get_builtin_function_name(func)
    if aezq__hacwi:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, aezq__hacwi, typing_context, kws)
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
        kwjd__nmcr = args[0] if len(args) > 0 else kws.pop('axis', 0)
        iit__omr = args[1] if len(args) > 1 else kws.pop('numeric_only', False)
        epnix__kvab = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        kofw__sdxp = dict(axis=kwjd__nmcr, numeric_only=iit__omr)
        awxm__yqbhi = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', kofw__sdxp,
            awxm__yqbhi, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        qtnw__thbko = args[0] if len(args) > 0 else kws.pop('periods', 1)
        nzr__wbqo = args[1] if len(args) > 1 else kws.pop('freq', None)
        kwjd__nmcr = args[2] if len(args) > 2 else kws.pop('axis', 0)
        pgkjk__aulp = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        kofw__sdxp = dict(freq=nzr__wbqo, axis=kwjd__nmcr, fill_value=
            pgkjk__aulp)
        awxm__yqbhi = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', kofw__sdxp,
            awxm__yqbhi, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        pbdsu__mlkrd = args[0] if len(args) > 0 else kws.pop('func', None)
        hzoc__iijm = kws.pop('engine', None)
        zcn__yioi = kws.pop('engine_kwargs', None)
        kofw__sdxp = dict(engine=hzoc__iijm, engine_kwargs=zcn__yioi)
        awxm__yqbhi = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', kofw__sdxp,
            awxm__yqbhi, package_name='pandas', module_name='GroupBy')
    suja__yvunt = {}
    for xpzh__apdx in grp.selection:
        out_columns.append(xpzh__apdx)
        suja__yvunt[xpzh__apdx, name_operation] = xpzh__apdx
        mocdt__lra = grp.df_type.column_index[xpzh__apdx]
        data = grp.df_type.data[mocdt__lra]
        abpkj__evx = (name_operation if name_operation != 'transform' else
            get_literal_value(pbdsu__mlkrd))
        if abpkj__evx in ('sum', 'cumsum'):
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
            shu__zdjqr, err_msg = get_groupby_output_dtype(data,
                get_literal_value(pbdsu__mlkrd), grp.df_type.index)
            if err_msg == 'ok':
                data = shu__zdjqr
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    xsss__zsbi = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        xsss__zsbi = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(xsss__zsbi, *args), suja__yvunt


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
        bhqk__esw = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        wrh__xmux = isinstance(bhqk__esw, (SeriesType, HeterogeneousSeriesType)
            ) and bhqk__esw.const_info is not None or not isinstance(bhqk__esw,
            (SeriesType, DataFrameType))
        if wrh__xmux:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                qddu__ujlz = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                ckmuw__rkkro = tuple(grp.df_type.column_index[grp.keys[
                    izv__sty]] for izv__sty in range(len(grp.keys)))
                ajhew__ezn = tuple(grp.df_type.data[mocdt__lra] for
                    mocdt__lra in ckmuw__rkkro)
                qddu__ujlz = MultiIndexType(ajhew__ezn, tuple(types.literal
                    (ssd__jtbk) for ssd__jtbk in grp.keys))
            else:
                mocdt__lra = grp.df_type.column_index[grp.keys[0]]
                uuvq__zhe = grp.df_type.data[mocdt__lra]
                qddu__ujlz = bodo.hiframes.pd_index_ext.array_type_to_index(
                    uuvq__zhe, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            jyu__rmed = tuple(grp.df_type.data[grp.df_type.column_index[
                xpzh__apdx]] for xpzh__apdx in grp.keys)
            kil__uzrz = tuple(types.literal(chnc__fxxdq) for chnc__fxxdq in
                grp.keys) + get_index_name_types(bhqk__esw.index)
            if not grp.as_index:
                jyu__rmed = types.Array(types.int64, 1, 'C'),
                kil__uzrz = (types.none,) + get_index_name_types(bhqk__esw.
                    index)
            qddu__ujlz = MultiIndexType(jyu__rmed +
                get_index_data_arr_types(bhqk__esw.index), kil__uzrz)
        if wrh__xmux:
            if isinstance(bhqk__esw, HeterogeneousSeriesType):
                igyvu__izyo, lls__frzri = bhqk__esw.const_info
                if isinstance(bhqk__esw.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    gvll__qzgb = bhqk__esw.data.tuple_typ.types
                elif isinstance(bhqk__esw.data, types.Tuple):
                    gvll__qzgb = bhqk__esw.data.types
                voiu__slt = tuple(to_nullable_type(dtype_to_array_type(
                    jjmfo__fhw)) for jjmfo__fhw in gvll__qzgb)
                txgj__sdzo = DataFrameType(out_data + voiu__slt, qddu__ujlz,
                    out_columns + lls__frzri)
            elif isinstance(bhqk__esw, SeriesType):
                fiqvj__pwp, lls__frzri = bhqk__esw.const_info
                voiu__slt = tuple(to_nullable_type(dtype_to_array_type(
                    bhqk__esw.dtype)) for igyvu__izyo in range(fiqvj__pwp))
                txgj__sdzo = DataFrameType(out_data + voiu__slt, qddu__ujlz,
                    out_columns + lls__frzri)
            else:
                ydmgj__bxey = get_udf_out_arr_type(bhqk__esw)
                if not grp.as_index:
                    txgj__sdzo = DataFrameType(out_data + (ydmgj__bxey,),
                        qddu__ujlz, out_columns + ('',))
                else:
                    txgj__sdzo = SeriesType(ydmgj__bxey.dtype, ydmgj__bxey,
                        qddu__ujlz, None)
        elif isinstance(bhqk__esw, SeriesType):
            txgj__sdzo = SeriesType(bhqk__esw.dtype, bhqk__esw.data,
                qddu__ujlz, bhqk__esw.name_typ)
        else:
            txgj__sdzo = DataFrameType(bhqk__esw.data, qddu__ujlz,
                bhqk__esw.columns)
        nindi__ssko = gen_apply_pysig(len(f_args), kws.keys())
        xxrh__lkz = (func, *f_args) + tuple(kws.values())
        return signature(txgj__sdzo, *xxrh__lkz).replace(pysig=nindi__ssko)

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
    utlsk__bgfwh = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            kpr__qfez = grp.selection[0]
            ydmgj__bxey = utlsk__bgfwh.data[utlsk__bgfwh.column_index[
                kpr__qfez]]
            gygjn__pmuk = SeriesType(ydmgj__bxey.dtype, ydmgj__bxey,
                utlsk__bgfwh.index, types.literal(kpr__qfez))
        else:
            onp__zgqe = tuple(utlsk__bgfwh.data[utlsk__bgfwh.column_index[
                xpzh__apdx]] for xpzh__apdx in grp.selection)
            gygjn__pmuk = DataFrameType(onp__zgqe, utlsk__bgfwh.index,
                tuple(grp.selection))
    else:
        gygjn__pmuk = utlsk__bgfwh
    rqft__trf = gygjn__pmuk,
    rqft__trf += tuple(f_args)
    try:
        bhqk__esw = get_const_func_output_type(func, rqft__trf, kws,
            typing_context, target_context)
    except Exception as zkgs__ewott:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', zkgs__ewott),
            getattr(zkgs__ewott, 'loc', None))
    return bhqk__esw


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    rqft__trf = (grp,) + f_args
    try:
        bhqk__esw = get_const_func_output_type(func, rqft__trf, kws, self.
            context, numba.core.registry.cpu_target.target_context, False)
    except Exception as zkgs__ewott:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()',
            zkgs__ewott), getattr(zkgs__ewott, 'loc', None))
    nindi__ssko = gen_apply_pysig(len(f_args), kws.keys())
    xxrh__lkz = (func, *f_args) + tuple(kws.values())
    return signature(bhqk__esw, *xxrh__lkz).replace(pysig=nindi__ssko)


def gen_apply_pysig(n_args, kws):
    cew__wyvl = ', '.join(f'arg{izv__sty}' for izv__sty in range(n_args))
    cew__wyvl = cew__wyvl + ', ' if cew__wyvl else ''
    tokox__bwbk = ', '.join(f"{jec__nzscm} = ''" for jec__nzscm in kws)
    zqsxg__sbmly = f'def apply_stub(func, {cew__wyvl}{tokox__bwbk}):\n'
    zqsxg__sbmly += '    pass\n'
    tkyl__mmmp = {}
    exec(zqsxg__sbmly, {}, tkyl__mmmp)
    sla__ijayj = tkyl__mmmp['apply_stub']
    return numba.core.utils.pysignature(sla__ijayj)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        ytuhe__aueg = types.Array(types.int64, 1, 'C')
        loxos__dnz = _pivot_values.meta
        shtyr__dkmoh = len(loxos__dnz)
        bmfg__rwuyl = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        mhzfa__mprj = DataFrameType((ytuhe__aueg,) * shtyr__dkmoh,
            bmfg__rwuyl, tuple(loxos__dnz))
        return signature(mhzfa__mprj, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    zqsxg__sbmly = 'def impl(keys, dropna, _is_parallel):\n'
    zqsxg__sbmly += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    zqsxg__sbmly += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{izv__sty}])' for izv__sty in range(len(keys.
        types))))
    zqsxg__sbmly += '    table = arr_info_list_to_table(info_list)\n'
    zqsxg__sbmly += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    zqsxg__sbmly += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    zqsxg__sbmly += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    zqsxg__sbmly += '    delete_table_decref_arrays(table)\n'
    zqsxg__sbmly += '    ev.finalize()\n'
    zqsxg__sbmly += '    return sort_idx, group_labels, ngroups\n'
    tkyl__mmmp = {}
    exec(zqsxg__sbmly, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, tkyl__mmmp)
    uag__qtohf = tkyl__mmmp['impl']
    return uag__qtohf


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    nqva__ocxzr = len(labels)
    pzcl__gsx = np.zeros(ngroups, dtype=np.int64)
    tkgdp__ndbz = np.zeros(ngroups, dtype=np.int64)
    varne__lunf = 0
    kmcle__prkho = 0
    for izv__sty in range(nqva__ocxzr):
        ctoy__pce = labels[izv__sty]
        if ctoy__pce < 0:
            varne__lunf += 1
        else:
            kmcle__prkho += 1
            if izv__sty == nqva__ocxzr - 1 or ctoy__pce != labels[izv__sty + 1
                ]:
                pzcl__gsx[ctoy__pce] = varne__lunf
                tkgdp__ndbz[ctoy__pce] = varne__lunf + kmcle__prkho
                varne__lunf += kmcle__prkho
                kmcle__prkho = 0
    return pzcl__gsx, tkgdp__ndbz


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    uag__qtohf, igyvu__izyo = gen_shuffle_dataframe(df, keys, _is_parallel)
    return uag__qtohf


def gen_shuffle_dataframe(df, keys, _is_parallel):
    fiqvj__pwp = len(df.columns)
    lir__ozc = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    zqsxg__sbmly = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        zqsxg__sbmly += '  return df, keys, get_null_shuffle_info()\n'
        tkyl__mmmp = {}
        exec(zqsxg__sbmly, {'get_null_shuffle_info': get_null_shuffle_info},
            tkyl__mmmp)
        uag__qtohf = tkyl__mmmp['impl']
        return uag__qtohf
    for izv__sty in range(fiqvj__pwp):
        zqsxg__sbmly += f"""  in_arr{izv__sty} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {izv__sty})
"""
    zqsxg__sbmly += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    zqsxg__sbmly += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{izv__sty}])' for izv__sty in range(lir__ozc)),
        ', '.join(f'array_to_info(in_arr{izv__sty})' for izv__sty in range(
        fiqvj__pwp)), 'array_to_info(in_index_arr)')
    zqsxg__sbmly += '  table = arr_info_list_to_table(info_list)\n'
    zqsxg__sbmly += (
        f'  out_table = shuffle_table(table, {lir__ozc}, _is_parallel, 1)\n')
    for izv__sty in range(lir__ozc):
        zqsxg__sbmly += f"""  out_key{izv__sty} = info_to_array(info_from_table(out_table, {izv__sty}), keys{izv__sty}_typ)
"""
    for izv__sty in range(fiqvj__pwp):
        zqsxg__sbmly += f"""  out_arr{izv__sty} = info_to_array(info_from_table(out_table, {izv__sty + lir__ozc}), in_arr{izv__sty}_typ)
"""
    zqsxg__sbmly += f"""  out_arr_index = info_to_array(info_from_table(out_table, {lir__ozc + fiqvj__pwp}), ind_arr_typ)
"""
    zqsxg__sbmly += '  shuffle_info = get_shuffle_info(out_table)\n'
    zqsxg__sbmly += '  delete_table(out_table)\n'
    zqsxg__sbmly += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{izv__sty}' for izv__sty in range(fiqvj__pwp)
        )
    zqsxg__sbmly += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    zqsxg__sbmly += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    zqsxg__sbmly += '  return out_df, ({},), shuffle_info\n'.format(', '.
        join(f'out_key{izv__sty}' for izv__sty in range(lir__ozc)))
    los__jsmsy = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    los__jsmsy.update({f'keys{izv__sty}_typ': keys.types[izv__sty] for
        izv__sty in range(lir__ozc)})
    los__jsmsy.update({f'in_arr{izv__sty}_typ': df.data[izv__sty] for
        izv__sty in range(fiqvj__pwp)})
    tkyl__mmmp = {}
    exec(zqsxg__sbmly, los__jsmsy, tkyl__mmmp)
    uag__qtohf = tkyl__mmmp['impl']
    return uag__qtohf, los__jsmsy


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        pism__oxpa = len(data.array_types)
        zqsxg__sbmly = 'def impl(data, shuffle_info):\n'
        zqsxg__sbmly += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{izv__sty}])' for izv__sty in range(
            pism__oxpa)))
        zqsxg__sbmly += '  table = arr_info_list_to_table(info_list)\n'
        zqsxg__sbmly += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for izv__sty in range(pism__oxpa):
            zqsxg__sbmly += f"""  out_arr{izv__sty} = info_to_array(info_from_table(out_table, {izv__sty}), data._data[{izv__sty}])
"""
        zqsxg__sbmly += '  delete_table(out_table)\n'
        zqsxg__sbmly += '  delete_table(table)\n'
        zqsxg__sbmly += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{izv__sty}' for izv__sty in range(
            pism__oxpa))))
        tkyl__mmmp = {}
        exec(zqsxg__sbmly, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, tkyl__mmmp)
        uag__qtohf = tkyl__mmmp['impl']
        return uag__qtohf
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            qwptn__dniay = bodo.utils.conversion.index_to_array(data)
            qng__bsg = reverse_shuffle(qwptn__dniay, shuffle_info)
            return bodo.utils.conversion.index_from_array(qng__bsg)
        return impl_index

    def impl_arr(data, shuffle_info):
        ovh__uczyw = [array_to_info(data)]
        ndbkl__hdumx = arr_info_list_to_table(ovh__uczyw)
        zwahy__zjw = reverse_shuffle_table(ndbkl__hdumx, shuffle_info)
        qng__bsg = info_to_array(info_from_table(zwahy__zjw, 0), data)
        delete_table(zwahy__zjw)
        delete_table(ndbkl__hdumx)
        return qng__bsg
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    kofw__sdxp = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    awxm__yqbhi = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', kofw__sdxp, awxm__yqbhi,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    mym__xsgh = get_overload_const_bool(ascending)
    qiklu__ois = grp.selection[0]
    zqsxg__sbmly = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    vwwml__hpvh = (
        f"lambda S: S.value_counts(ascending={mym__xsgh}, _index_name='{qiklu__ois}')"
        )
    zqsxg__sbmly += f'    return grp.apply({vwwml__hpvh})\n'
    tkyl__mmmp = {}
    exec(zqsxg__sbmly, {'bodo': bodo}, tkyl__mmmp)
    uag__qtohf = tkyl__mmmp['impl']
    return uag__qtohf


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
    for xotpd__fmxlv in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, xotpd__fmxlv, no_unliteral
            =True)(create_unsupported_overload(
            f'DataFrameGroupBy.{xotpd__fmxlv}'))
    for xotpd__fmxlv in groupby_unsupported:
        overload_method(DataFrameGroupByType, xotpd__fmxlv, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{xotpd__fmxlv}'))
    for xotpd__fmxlv in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, xotpd__fmxlv, no_unliteral
            =True)(create_unsupported_overload(f'SeriesGroupBy.{xotpd__fmxlv}')
            )
    for xotpd__fmxlv in series_only_unsupported:
        overload_method(DataFrameGroupByType, xotpd__fmxlv, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{xotpd__fmxlv}'))
    for xotpd__fmxlv in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, xotpd__fmxlv, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{xotpd__fmxlv}'))


_install_groupby_unsupported()
