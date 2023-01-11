"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
import time
from functools import cached_property
from typing import Optional, Sequence
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.cpython.listobj import ListInstance
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.hiframes.table import Table, TableType, decode_if_dict_table, get_table_data, set_table_data_codegen
from bodo.hiframes.time_ext import TimeArrayType
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_table_to_cpp_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.conversion import fix_arr_dtype, index_to_array
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_str_arr_type, is_tuple_like_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr, types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data: Optional[Sequence['types.Array']]=None, index=
        None, columns: Optional[Sequence[str]]=None, dist=None,
        is_table_format=False):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        self.is_table_format = is_table_format
        if columns is None:
            assert is_table_format, 'Determining columns at runtime is only supported for DataFrame with table format'
            self.table_type = TableType(tuple(data[:-1]), True)
        else:
            self.table_type = TableType(data) if is_table_format else None
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist}, {is_table_format}, {self.has_runtime_cols})'
            )

    def __str__(self):
        if not self.has_runtime_cols and len(self.columns) > 20:
            fjqo__dtl = f'{len(self.data)} columns of types {set(self.data)}'
            kjlux__ghs = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            pnth__xhqm = str(hash(super().__str__()))
            return (
                f'dataframe({fjqo__dtl}, {self.index}, {kjlux__ghs}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols}, key_hash={pnth__xhqm})'
                )
        return super().__str__()

    def copy(self, data=None, index=None, columns=None, dist=None,
        is_table_format=None):
        if data is None:
            data = self.data
        if columns is None:
            columns = self.columns
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if is_table_format is None:
            is_table_format = self.is_table_format
        return DataFrameType(data, index, columns, dist, is_table_format)

    @property
    def has_runtime_cols(self):
        return self.columns is None

    @cached_property
    def column_index(self):
        return {epzhw__jytyl: i for i, epzhw__jytyl in enumerate(self.columns)}

    @property
    def runtime_colname_typ(self):
        return self.data[-1] if self.has_runtime_cols else None

    @property
    def runtime_data_types(self):
        return self.data[:-1] if self.has_runtime_cols else self.data

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return (self.data, self.index, self.columns, self.dist, self.
            is_table_format)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if (isinstance(other, DataFrameType) and len(other.data) == len(
            self.data) and other.columns == self.columns and other.
            has_runtime_cols == self.has_runtime_cols):
            ndhds__xsxef = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            data = tuple(nsdb__qju.unify(typingctx, cstgb__asiz) if 
                nsdb__qju != cstgb__asiz else nsdb__qju for nsdb__qju,
                cstgb__asiz in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if ndhds__xsxef is not None and None not in data:
                return DataFrameType(data, ndhds__xsxef, self.columns, dist,
                    self.is_table_format)
        if isinstance(other, DataFrameType) and len(self.data
            ) == 0 and not self.has_runtime_cols:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist and self.has_runtime_cols == other.
            has_runtime_cols):
            return Conversion.safe

    def is_precise(self):
        return all(nsdb__qju.is_precise() for nsdb__qju in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        amf__uay = self.columns.index(col_name)
        zey__pkooj = tuple(list(self.data[:amf__uay]) + [new_type] + list(
            self.data[amf__uay + 1:]))
        return DataFrameType(zey__pkooj, self.index, self.columns, self.
            dist, self.is_table_format)


def check_runtime_cols_unsupported(df, func_name):
    if isinstance(df, DataFrameType) and df.has_runtime_cols:
        raise BodoError(
            f'{func_name} on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information.'
            )


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        data_typ = types.Tuple(fe_type.df_type.data)
        if fe_type.df_type.is_table_format:
            data_typ = types.Tuple([fe_type.df_type.table_type])
        xdju__oexkz = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            xdju__oexkz.append(('columns', fe_type.df_type.runtime_colname_typ)
                )
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, xdju__oexkz)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        xdju__oexkz = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, xdju__oexkz)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        djj__ozj = 'n',
        xkw__wfftr = {'n': 5}
        cvhlg__ocda, son__lbty = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, djj__ozj, xkw__wfftr)
        swtbp__duify = son__lbty[0]
        if not is_overload_int(swtbp__duify):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        vqmsn__cwfa = df.copy()
        return vqmsn__cwfa(*son__lbty).replace(pysig=cvhlg__ocda)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        eafdj__cyd = (df,) + args
        djj__ozj = 'df', 'method', 'min_periods'
        xkw__wfftr = {'method': 'pearson', 'min_periods': 1}
        xdi__pokj = 'method',
        cvhlg__ocda, son__lbty = bodo.utils.typing.fold_typing_args(func_name,
            eafdj__cyd, kws, djj__ozj, xkw__wfftr, xdi__pokj)
        zmbuu__oabh = son__lbty[2]
        if not is_overload_int(zmbuu__oabh):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        aqos__uhd = []
        pha__lzsok = []
        for epzhw__jytyl, niws__dppbs in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(niws__dppbs.dtype):
                aqos__uhd.append(epzhw__jytyl)
                pha__lzsok.append(types.Array(types.float64, 1, 'A'))
        if len(aqos__uhd) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        pha__lzsok = tuple(pha__lzsok)
        aqos__uhd = tuple(aqos__uhd)
        index_typ = bodo.utils.typing.type_col_to_index(aqos__uhd)
        vqmsn__cwfa = DataFrameType(pha__lzsok, index_typ, aqos__uhd)
        return vqmsn__cwfa(*son__lbty).replace(pysig=cvhlg__ocda)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        sfu__efg = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        ysq__slvbf = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        eis__qffi = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        izcoh__tkkr = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        ave__gqhe = dict(raw=ysq__slvbf, result_type=eis__qffi)
        wqrsi__uhfhn = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', ave__gqhe, wqrsi__uhfhn,
            package_name='pandas', module_name='DataFrame')
        qymxm__iaesm = True
        if types.unliteral(sfu__efg) == types.unicode_type:
            if not is_overload_constant_str(sfu__efg):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            qymxm__iaesm = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        juyvz__yjrzu = get_overload_const_int(axis)
        if qymxm__iaesm and juyvz__yjrzu != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif juyvz__yjrzu not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        lfq__rrm = []
        for arr_typ in df.data:
            phvu__gdyyv = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            bjs__dit = self.context.resolve_function_type(operator.getitem,
                (SeriesIlocType(phvu__gdyyv), types.int64), {}).return_type
            lfq__rrm.append(bjs__dit)
        gdjeh__pjjiz = types.none
        yuz__lri = HeterogeneousIndexType(types.BaseTuple.from_types(tuple(
            types.literal(epzhw__jytyl) for epzhw__jytyl in df.columns)), None)
        wpk__whba = types.BaseTuple.from_types(lfq__rrm)
        fmcem__rrkb = types.Tuple([types.bool_] * len(wpk__whba))
        zggy__ziz = bodo.NullableTupleType(wpk__whba, fmcem__rrkb)
        yrbla__wftns = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if yrbla__wftns == types.NPDatetime('ns'):
            yrbla__wftns = bodo.pd_timestamp_tz_naive_type
        if yrbla__wftns == types.NPTimedelta('ns'):
            yrbla__wftns = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(wpk__whba):
            dqsmb__ase = HeterogeneousSeriesType(zggy__ziz, yuz__lri,
                yrbla__wftns)
        else:
            dqsmb__ase = SeriesType(wpk__whba.dtype, zggy__ziz, yuz__lri,
                yrbla__wftns)
        kva__rvnug = dqsmb__ase,
        if izcoh__tkkr is not None:
            kva__rvnug += tuple(izcoh__tkkr.types)
        try:
            if not qymxm__iaesm:
                hehmo__cmwp = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(sfu__efg), self.context,
                    'DataFrame.apply', axis if juyvz__yjrzu == 1 else None)
            else:
                hehmo__cmwp = get_const_func_output_type(sfu__efg,
                    kva__rvnug, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as fscbo__yaktc:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                fscbo__yaktc))
        if qymxm__iaesm:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(hehmo__cmwp, (SeriesType, HeterogeneousSeriesType)
                ) and hehmo__cmwp.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(hehmo__cmwp, HeterogeneousSeriesType):
                pzkb__ynha, mzmh__izrb = hehmo__cmwp.const_info
                if isinstance(hehmo__cmwp.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    tikzo__onzdx = hehmo__cmwp.data.tuple_typ.types
                elif isinstance(hehmo__cmwp.data, types.Tuple):
                    tikzo__onzdx = hehmo__cmwp.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                qqmpg__ylek = tuple(to_nullable_type(dtype_to_array_type(
                    dodiu__ykmjy)) for dodiu__ykmjy in tikzo__onzdx)
                eilh__ges = DataFrameType(qqmpg__ylek, df.index, mzmh__izrb)
            elif isinstance(hehmo__cmwp, SeriesType):
                xfnk__ejfl, mzmh__izrb = hehmo__cmwp.const_info
                qqmpg__ylek = tuple(to_nullable_type(dtype_to_array_type(
                    hehmo__cmwp.dtype)) for pzkb__ynha in range(xfnk__ejfl))
                eilh__ges = DataFrameType(qqmpg__ylek, df.index, mzmh__izrb)
            else:
                bgpyd__xxcvg = get_udf_out_arr_type(hehmo__cmwp)
                eilh__ges = SeriesType(bgpyd__xxcvg.dtype, bgpyd__xxcvg, df
                    .index, None)
        else:
            eilh__ges = hehmo__cmwp
        arzy__imjew = ', '.join("{} = ''".format(nsdb__qju) for nsdb__qju in
            kws.keys())
        epq__mwl = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {arzy__imjew}):
"""
        epq__mwl += '    pass\n'
        nvyr__gligm = {}
        exec(epq__mwl, {}, nvyr__gligm)
        huzd__vrbqw = nvyr__gligm['apply_stub']
        cvhlg__ocda = numba.core.utils.pysignature(huzd__vrbqw)
        wyl__pfg = (sfu__efg, axis, ysq__slvbf, eis__qffi, izcoh__tkkr
            ) + tuple(kws.values())
        return signature(eilh__ges, *wyl__pfg).replace(pysig=cvhlg__ocda)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        djj__ozj = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots', 'sharex',
            'sharey', 'layout', 'use_index', 'title', 'grid', 'legend',
            'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks', 'xlim',
            'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr', 'xerr',
            'secondary_y', 'sort_columns', 'xlabel', 'ylabel', 'position',
            'stacked', 'mark_right', 'include_bool', 'backend')
        xkw__wfftr = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        xdi__pokj = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        cvhlg__ocda, son__lbty = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, djj__ozj, xkw__wfftr, xdi__pokj)
        rauly__ytvft = son__lbty[2]
        if not is_overload_constant_str(rauly__ytvft):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        cjif__ltf = son__lbty[0]
        if not is_overload_none(cjif__ltf) and not (is_overload_int(
            cjif__ltf) or is_overload_constant_str(cjif__ltf)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(cjif__ltf):
            dcus__vythp = get_overload_const_str(cjif__ltf)
            if dcus__vythp not in df.columns:
                raise BodoError(f'{func_name}: {dcus__vythp} column not found.'
                    )
        elif is_overload_int(cjif__ltf):
            wcy__uqgnf = get_overload_const_int(cjif__ltf)
            if wcy__uqgnf > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {wcy__uqgnf} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            cjif__ltf = df.columns[cjif__ltf]
        remnq__ytvqe = son__lbty[1]
        if not is_overload_none(remnq__ytvqe) and not (is_overload_int(
            remnq__ytvqe) or is_overload_constant_str(remnq__ytvqe)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(remnq__ytvqe):
            oor__pxfks = get_overload_const_str(remnq__ytvqe)
            if oor__pxfks not in df.columns:
                raise BodoError(f'{func_name}: {oor__pxfks} column not found.')
        elif is_overload_int(remnq__ytvqe):
            ymvl__agcb = get_overload_const_int(remnq__ytvqe)
            if ymvl__agcb > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {ymvl__agcb} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            remnq__ytvqe = df.columns[remnq__ytvqe]
        hngxy__yyf = son__lbty[3]
        if not is_overload_none(hngxy__yyf) and not is_tuple_like_type(
            hngxy__yyf):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        dhcn__xiq = son__lbty[10]
        if not is_overload_none(dhcn__xiq) and not is_overload_constant_str(
            dhcn__xiq):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        uxnk__xgn = son__lbty[12]
        if not is_overload_bool(uxnk__xgn):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        qut__als = son__lbty[17]
        if not is_overload_none(qut__als) and not is_tuple_like_type(qut__als):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        uba__wkyfq = son__lbty[18]
        if not is_overload_none(uba__wkyfq) and not is_tuple_like_type(
            uba__wkyfq):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        vqy__rzltr = son__lbty[22]
        if not is_overload_none(vqy__rzltr) and not is_overload_int(vqy__rzltr
            ):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        mfcv__mywre = son__lbty[29]
        if not is_overload_none(mfcv__mywre) and not is_overload_constant_str(
            mfcv__mywre):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        jolj__pgz = son__lbty[30]
        if not is_overload_none(jolj__pgz) and not is_overload_constant_str(
            jolj__pgz):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        iya__bybok = types.List(types.mpl_line_2d_type)
        rauly__ytvft = get_overload_const_str(rauly__ytvft)
        if rauly__ytvft == 'scatter':
            if is_overload_none(cjif__ltf) and is_overload_none(remnq__ytvqe):
                raise BodoError(
                    f'{func_name}: {rauly__ytvft} requires an x and y column.')
            elif is_overload_none(cjif__ltf):
                raise BodoError(
                    f'{func_name}: {rauly__ytvft} x column is missing.')
            elif is_overload_none(remnq__ytvqe):
                raise BodoError(
                    f'{func_name}: {rauly__ytvft} y column is missing.')
            iya__bybok = types.mpl_path_collection_type
        elif rauly__ytvft != 'line':
            raise BodoError(
                f'{func_name}: {rauly__ytvft} plot is not supported.')
        return signature(iya__bybok, *son__lbty).replace(pysig=cvhlg__ocda)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            czsy__sjn = df.columns.index(attr)
            arr_typ = df.data[czsy__sjn]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            cwnv__wtjcs = []
            zey__pkooj = []
            huszi__bbzn = False
            for i, druof__tdfd in enumerate(df.columns):
                if druof__tdfd[0] != attr:
                    continue
                huszi__bbzn = True
                cwnv__wtjcs.append(druof__tdfd[1] if len(druof__tdfd) == 2 else
                    druof__tdfd[1:])
                zey__pkooj.append(df.data[i])
            if huszi__bbzn:
                return DataFrameType(tuple(zey__pkooj), df.index, tuple(
                    cwnv__wtjcs))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        kpon__okkb = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(kpon__okkb)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    if df_type.is_table_format:
        context.nrt.decref(builder, df_type.table_type, builder.
            extract_value(payload.data, 0))
        context.nrt.decref(builder, df_type.index, payload.index)
        if df_type.has_runtime_cols:
            context.nrt.decref(builder, df_type.data[-1], payload.columns)
        return
    for i in range(len(df_type.data)):
        fgo__ssfnw = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], fgo__ssfnw)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    nykif__dfsxm = builder.module
    afs__bupy = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    fit__vcxz = cgutils.get_or_insert_function(nykif__dfsxm, afs__bupy,
        name='.dtor.df.{}'.format(df_type))
    if not fit__vcxz.is_declaration:
        return fit__vcxz
    fit__vcxz.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(fit__vcxz.append_basic_block())
    vybqa__jyhvx = fit__vcxz.args[0]
    jodk__mry = context.get_value_type(payload_type).as_pointer()
    dcutk__tig = builder.bitcast(vybqa__jyhvx, jodk__mry)
    payload = context.make_helper(builder, payload_type, ref=dcutk__tig)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        mjf__gcvf = context.get_python_api(builder)
        aqle__iuted = mjf__gcvf.gil_ensure()
        mjf__gcvf.decref(payload.parent)
        mjf__gcvf.gil_release(aqle__iuted)
    builder.ret_void()
    return fit__vcxz


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    rgqaa__dzp = cgutils.create_struct_proxy(payload_type)(context, builder)
    rgqaa__dzp.data = data_tup
    rgqaa__dzp.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        rgqaa__dzp.columns = colnames
    lyo__xvz = context.get_value_type(payload_type)
    onf__qnp = context.get_abi_sizeof(lyo__xvz)
    dqkln__iao = define_df_dtor(context, builder, df_type, payload_type)
    vpr__rxkp = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, onf__qnp), dqkln__iao)
    zprab__mwauf = context.nrt.meminfo_data(builder, vpr__rxkp)
    vsbui__zuaw = builder.bitcast(zprab__mwauf, lyo__xvz.as_pointer())
    wwhw__blt = cgutils.create_struct_proxy(df_type)(context, builder)
    wwhw__blt.meminfo = vpr__rxkp
    if parent is None:
        wwhw__blt.parent = cgutils.get_null_value(wwhw__blt.parent.type)
    else:
        wwhw__blt.parent = parent
        rgqaa__dzp.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            mjf__gcvf = context.get_python_api(builder)
            aqle__iuted = mjf__gcvf.gil_ensure()
            mjf__gcvf.incref(parent)
            mjf__gcvf.gil_release(aqle__iuted)
    builder.store(rgqaa__dzp._getvalue(), vsbui__zuaw)
    return wwhw__blt._getvalue()


@intrinsic
def init_runtime_cols_dataframe(typingctx, data_typ, index_typ,
    colnames_index_typ=None):
    assert isinstance(data_typ, types.BaseTuple) and isinstance(data_typ.
        dtype, TableType
        ) and data_typ.dtype.has_runtime_cols, 'init_runtime_cols_dataframe must be called with a table that determines columns at runtime.'
    assert bodo.hiframes.pd_index_ext.is_pd_index_type(colnames_index_typ
        ) or isinstance(colnames_index_typ, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType), 'Column names must be an index'
    if isinstance(data_typ.dtype.arr_types, types.UniTuple):
        isd__rpxzh = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        isd__rpxzh = [dodiu__ykmjy for dodiu__ykmjy in data_typ.dtype.arr_types
            ]
    maiu__ttqog = DataFrameType(tuple(isd__rpxzh + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        uvdj__ybdos = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return uvdj__ybdos
    sig = signature(maiu__ttqog, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    xfnk__ejfl = len(data_tup_typ.types)
    if xfnk__ejfl == 0:
        column_names = ()
    rvkvz__frw = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(rvkvz__frw, ColNamesMetaType) and isinstance(rvkvz__frw
        .meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = rvkvz__frw.meta
    if xfnk__ejfl == 1 and isinstance(data_tup_typ.types[0], TableType):
        xfnk__ejfl = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == xfnk__ejfl, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    xgag__tivcd = data_tup_typ.types
    if xfnk__ejfl != 0 and isinstance(data_tup_typ.types[0], TableType):
        xgag__tivcd = data_tup_typ.types[0].arr_types
        is_table_format = True
    maiu__ttqog = DataFrameType(xgag__tivcd, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            ybm__kmue = cgutils.create_struct_proxy(maiu__ttqog.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = ybm__kmue.parent
        uvdj__ybdos = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return uvdj__ybdos
    sig = signature(maiu__ttqog, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        wwhw__blt = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, wwhw__blt.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        rgqaa__dzp = get_dataframe_payload(context, builder, df_typ, args[0])
        plygj__tbox = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[plygj__tbox]
        if df_typ.is_table_format:
            ybm__kmue = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(rgqaa__dzp.data, 0))
            zug__edv = df_typ.table_type.type_to_blk[arr_typ]
            ojrkc__ytbw = getattr(ybm__kmue, f'block_{zug__edv}')
            lpgo__gsklj = ListInstance(context, builder, types.List(arr_typ
                ), ojrkc__ytbw)
            asoib__upyb = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[plygj__tbox])
            fgo__ssfnw = lpgo__gsklj.getitem(asoib__upyb)
        else:
            fgo__ssfnw = builder.extract_value(rgqaa__dzp.data, plygj__tbox)
        vridw__xohg = cgutils.alloca_once_value(builder, fgo__ssfnw)
        kpf__zothp = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, vridw__xohg, kpf__zothp)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    vpr__rxkp = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, vpr__rxkp)
    jodk__mry = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, jodk__mry)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    maiu__ttqog = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        maiu__ttqog = types.Tuple([TableType(df_typ.data)])
    sig = signature(maiu__ttqog, df_typ)

    def codegen(context, builder, signature, args):
        rgqaa__dzp = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            rgqaa__dzp.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        rgqaa__dzp = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, rgqaa__dzp
            .index)
    maiu__ttqog = df_typ.index
    sig = signature(maiu__ttqog, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if not is_overload_constant_int(args[1]):
            raise_bodo_error(
                'Selecting a DataFrame column requires a constant column label'
                )
        df = args[0]
        check_runtime_cols_unsupported(df, 'get_dataframe_data')
        i = get_overload_const_int(args[1])
        vqmsn__cwfa = df.data[i]
        return vqmsn__cwfa(*args)


GetDataFrameDataInfer.prefer_literal = True


def get_dataframe_data_impl(df, i):
    if df.is_table_format:

        def _impl(df, i):
            if has_parent(df) and _column_needs_unboxing(df, i):
                bodo.hiframes.boxing.unbox_dataframe_column(df, i)
            return get_table_data(_get_dataframe_data(df)[0], i)
        return _impl

    def _impl(df, i):
        if has_parent(df) and _column_needs_unboxing(df, i):
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@intrinsic
def get_dataframe_table(typingctx, df_typ=None):
    assert df_typ.is_table_format, 'get_dataframe_table() expects table format'

    def codegen(context, builder, signature, args):
        rgqaa__dzp = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(rgqaa__dzp.data, 0))
    return df_typ.table_type(df_typ), codegen


def get_dataframe_all_data(df):
    return df.data


def get_dataframe_all_data_impl(df):
    if df.is_table_format:

        def _impl(df):
            return get_dataframe_table(df)
        return _impl
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for i in
        range(len(df.columns)))
    zxf__iid = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{zxf__iid})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        vqmsn__cwfa = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return vqmsn__cwfa(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        rgqaa__dzp = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, rgqaa__dzp.columns)
    return df_typ.runtime_colname_typ(df_typ), codegen


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_table',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_all_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    wpk__whba = self.typemap[data_tup.name]
    if any(is_tuple_like_type(dodiu__ykmjy) for dodiu__ykmjy in wpk__whba.types
        ):
        return None
    if equiv_set.has_shape(data_tup):
        ouz__nlame = equiv_set.get_shape(data_tup)
        if len(ouz__nlame) > 1:
            equiv_set.insert_equiv(*ouz__nlame)
        if len(ouz__nlame) > 0:
            yuz__lri = self.typemap[index.name]
            if not isinstance(yuz__lri, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(ouz__nlame[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(ouz__nlame[0], len(
                ouz__nlame)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    fliw__axxxu = args[0]
    data_types = self.typemap[fliw__axxxu.name].data
    if any(is_tuple_like_type(dodiu__ykmjy) for dodiu__ykmjy in data_types):
        return None
    if equiv_set.has_shape(fliw__axxxu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            fliw__axxxu)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    fliw__axxxu = args[0]
    yuz__lri = self.typemap[fliw__axxxu.name].index
    if isinstance(yuz__lri, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(fliw__axxxu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            fliw__axxxu)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    fliw__axxxu = args[0]
    if equiv_set.has_shape(fliw__axxxu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            fliw__axxxu), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    fliw__axxxu = args[0]
    if equiv_set.has_shape(fliw__axxxu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            fliw__axxxu)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    plygj__tbox = get_overload_const_int(c_ind_typ)
    if df_typ.data[plygj__tbox] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        qow__xte, pzkb__ynha, jby__wdlr = args
        rgqaa__dzp = get_dataframe_payload(context, builder, df_typ, qow__xte)
        if df_typ.is_table_format:
            ybm__kmue = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(rgqaa__dzp.data, 0))
            zug__edv = df_typ.table_type.type_to_blk[arr_typ]
            ojrkc__ytbw = getattr(ybm__kmue, f'block_{zug__edv}')
            lpgo__gsklj = ListInstance(context, builder, types.List(arr_typ
                ), ojrkc__ytbw)
            asoib__upyb = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[plygj__tbox])
            lpgo__gsklj.setitem(asoib__upyb, jby__wdlr, True)
        else:
            fgo__ssfnw = builder.extract_value(rgqaa__dzp.data, plygj__tbox)
            context.nrt.decref(builder, df_typ.data[plygj__tbox], fgo__ssfnw)
            rgqaa__dzp.data = builder.insert_value(rgqaa__dzp.data,
                jby__wdlr, plygj__tbox)
            context.nrt.incref(builder, arr_typ, jby__wdlr)
        wwhw__blt = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=qow__xte)
        payload_type = DataFramePayloadType(df_typ)
        dcutk__tig = context.nrt.meminfo_data(builder, wwhw__blt.meminfo)
        jodk__mry = context.get_value_type(payload_type).as_pointer()
        dcutk__tig = builder.bitcast(dcutk__tig, jodk__mry)
        builder.store(rgqaa__dzp._getvalue(), dcutk__tig)
        return impl_ret_borrowed(context, builder, df_typ, qow__xte)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        seu__vfwy = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        fmxs__pye = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=seu__vfwy)
        bxdxu__xvxn = get_dataframe_payload(context, builder, df_typ, seu__vfwy
            )
        wwhw__blt = construct_dataframe(context, builder, signature.
            return_type, bxdxu__xvxn.data, index_val, fmxs__pye.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), bxdxu__xvxn.data)
        return wwhw__blt
    maiu__ttqog = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(maiu__ttqog, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    xfnk__ejfl = len(df_type.columns)
    ioocj__ebyyl = xfnk__ejfl
    zipji__znses = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    homo__yqcd = col_name not in df_type.columns
    plygj__tbox = xfnk__ejfl
    if homo__yqcd:
        zipji__znses += arr_type,
        column_names += col_name,
        ioocj__ebyyl += 1
    else:
        plygj__tbox = df_type.columns.index(col_name)
        zipji__znses = tuple(arr_type if i == plygj__tbox else zipji__znses
            [i] for i in range(xfnk__ejfl))

    def codegen(context, builder, signature, args):
        qow__xte, pzkb__ynha, jby__wdlr = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, qow__xte)
        ortf__upjpj = cgutils.create_struct_proxy(df_type)(context, builder,
            value=qow__xte)
        if df_type.is_table_format:
            oxvu__edmb = df_type.table_type
            jeh__lty = builder.extract_value(in_dataframe_payload.data, 0)
            yyrbj__rffcb = TableType(zipji__znses)
            jbxhm__kai = set_table_data_codegen(context, builder,
                oxvu__edmb, jeh__lty, yyrbj__rffcb, arr_type, jby__wdlr,
                plygj__tbox, homo__yqcd)
            data_tup = context.make_tuple(builder, types.Tuple([
                yyrbj__rffcb]), [jbxhm__kai])
        else:
            xgag__tivcd = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != plygj__tbox else jby__wdlr) for i in range(
                xfnk__ejfl)]
            if homo__yqcd:
                xgag__tivcd.append(jby__wdlr)
            for fliw__axxxu, mzf__iceei in zip(xgag__tivcd, zipji__znses):
                context.nrt.incref(builder, mzf__iceei, fliw__axxxu)
            data_tup = context.make_tuple(builder, types.Tuple(zipji__znses
                ), xgag__tivcd)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        zzo__rllog = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, ortf__upjpj.parent, None)
        if not homo__yqcd and arr_type == df_type.data[plygj__tbox]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            dcutk__tig = context.nrt.meminfo_data(builder, ortf__upjpj.meminfo)
            jodk__mry = context.get_value_type(payload_type).as_pointer()
            dcutk__tig = builder.bitcast(dcutk__tig, jodk__mry)
            znr__lunqg = get_dataframe_payload(context, builder, df_type,
                zzo__rllog)
            builder.store(znr__lunqg._getvalue(), dcutk__tig)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, yyrbj__rffcb, builder.
                    extract_value(data_tup, 0))
            else:
                for fliw__axxxu, mzf__iceei in zip(xgag__tivcd, zipji__znses):
                    context.nrt.incref(builder, mzf__iceei, fliw__axxxu)
        has_parent = cgutils.is_not_null(builder, ortf__upjpj.parent)
        with builder.if_then(has_parent):
            mjf__gcvf = context.get_python_api(builder)
            aqle__iuted = mjf__gcvf.gil_ensure()
            hxsib__eqke = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, jby__wdlr)
            epzhw__jytyl = numba.core.pythonapi._BoxContext(context,
                builder, mjf__gcvf, hxsib__eqke)
            emqxc__xnh = epzhw__jytyl.pyapi.from_native_value(arr_type,
                jby__wdlr, epzhw__jytyl.env_manager)
            if isinstance(col_name, str):
                lsfhf__bynv = context.insert_const_string(builder.module,
                    col_name)
                cjcci__esn = mjf__gcvf.string_from_string(lsfhf__bynv)
            else:
                assert isinstance(col_name, int)
                cjcci__esn = mjf__gcvf.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            mjf__gcvf.object_setitem(ortf__upjpj.parent, cjcci__esn, emqxc__xnh
                )
            mjf__gcvf.decref(emqxc__xnh)
            mjf__gcvf.decref(cjcci__esn)
            mjf__gcvf.gil_release(aqle__iuted)
        return zzo__rllog
    maiu__ttqog = DataFrameType(zipji__znses, index_typ, column_names,
        df_type.dist, df_type.is_table_format)
    sig = signature(maiu__ttqog, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    xfnk__ejfl = len(pyval.columns)
    xgag__tivcd = []
    for i in range(xfnk__ejfl):
        hyvnc__yrk = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            emqxc__xnh = hyvnc__yrk.array
        else:
            emqxc__xnh = hyvnc__yrk.values
        xgag__tivcd.append(emqxc__xnh)
    xgag__tivcd = tuple(xgag__tivcd)
    if df_type.is_table_format:
        ybm__kmue = context.get_constant_generic(builder, df_type.
            table_type, Table(xgag__tivcd))
        data_tup = lir.Constant.literal_struct([ybm__kmue])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], druof__tdfd) for
            i, druof__tdfd in enumerate(xgag__tivcd)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    amdra__pgi = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, amdra__pgi])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    nxc__kpbk = context.get_constant(types.int64, -1)
    dnfcu__ghxef = context.get_constant_null(types.voidptr)
    vpr__rxkp = lir.Constant.literal_struct([nxc__kpbk, dnfcu__ghxef,
        dnfcu__ghxef, payload, nxc__kpbk])
    vpr__rxkp = cgutils.global_constant(builder, '.const.meminfo', vpr__rxkp
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([vpr__rxkp, amdra__pgi])


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.is_table_format == toty.
        is_table_format and fromty.dist != toty.dist and fromty.
        has_runtime_cols == toty.has_runtime_cols):
        return val
    if not fromty.has_runtime_cols and not toty.has_runtime_cols and len(fromty
        .data) == 0 and len(toty.columns):
        return _cast_empty_df(context, builder, toty)
    if len(fromty.data) != len(toty.data) or fromty.data != toty.data and any(
        context.typing_context.unify_pairs(fromty.data[i], toty.data[i]) is
        None for i in range(len(fromty.data))
        ) or fromty.has_runtime_cols != toty.has_runtime_cols:
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    in_dataframe_payload = get_dataframe_payload(context, builder, fromty, val)
    if isinstance(fromty.index, RangeIndexType) and isinstance(toty.index,
        NumericIndexType):
        ndhds__xsxef = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        ndhds__xsxef = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, ndhds__xsxef)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        zey__pkooj = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                zey__pkooj)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), zey__pkooj)
    elif not fromty.is_table_format and toty.is_table_format:
        zey__pkooj = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        zey__pkooj = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        zey__pkooj = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        zey__pkooj = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, zey__pkooj,
        ndhds__xsxef, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    ekr__vujal = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        covyx__nmqa = get_index_data_arr_types(toty.index)[0]
        ecz__njxm = bodo.utils.transform.get_type_alloc_counts(covyx__nmqa) - 1
        oltix__oyy = ', '.join('0' for pzkb__ynha in range(ecz__njxm))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(oltix__oyy, ', ' if ecz__njxm == 1 else ''))
        ekr__vujal['index_arr_type'] = covyx__nmqa
    mzvy__lcvnj = []
    for i, arr_typ in enumerate(toty.data):
        ecz__njxm = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        oltix__oyy = ', '.join('0' for pzkb__ynha in range(ecz__njxm))
        hjmy__tsvhv = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'
            .format(i, oltix__oyy, ', ' if ecz__njxm == 1 else ''))
        mzvy__lcvnj.append(hjmy__tsvhv)
        ekr__vujal[f'arr_type{i}'] = arr_typ
    mzvy__lcvnj = ', '.join(mzvy__lcvnj)
    epq__mwl = 'def impl():\n'
    tcf__pfwdn = bodo.hiframes.dataframe_impl._gen_init_df(epq__mwl, toty.
        columns, mzvy__lcvnj, index, ekr__vujal)
    df = context.compile_internal(builder, tcf__pfwdn, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    geiq__wfi = toty.table_type
    ybm__kmue = cgutils.create_struct_proxy(geiq__wfi)(context, builder)
    ybm__kmue.parent = in_dataframe_payload.parent
    for dodiu__ykmjy, zug__edv in geiq__wfi.type_to_blk.items():
        dvkus__thpq = context.get_constant(types.int64, len(geiq__wfi.
            block_to_arr_ind[zug__edv]))
        pzkb__ynha, wzs__tcluh = ListInstance.allocate_ex(context, builder,
            types.List(dodiu__ykmjy), dvkus__thpq)
        wzs__tcluh.size = dvkus__thpq
        setattr(ybm__kmue, f'block_{zug__edv}', wzs__tcluh.value)
    for i, dodiu__ykmjy in enumerate(fromty.data):
        mzn__ozg = toty.data[i]
        if dodiu__ykmjy != mzn__ozg:
            lffq__uyru = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lffq__uyru)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        fgo__ssfnw = builder.extract_value(in_dataframe_payload.data, i)
        if dodiu__ykmjy != mzn__ozg:
            wir__cxsv = context.cast(builder, fgo__ssfnw, dodiu__ykmjy,
                mzn__ozg)
            xegp__efk = False
        else:
            wir__cxsv = fgo__ssfnw
            xegp__efk = True
        zug__edv = geiq__wfi.type_to_blk[dodiu__ykmjy]
        ojrkc__ytbw = getattr(ybm__kmue, f'block_{zug__edv}')
        lpgo__gsklj = ListInstance(context, builder, types.List(
            dodiu__ykmjy), ojrkc__ytbw)
        asoib__upyb = context.get_constant(types.int64, geiq__wfi.
            block_offsets[i])
        lpgo__gsklj.setitem(asoib__upyb, wir__cxsv, xegp__efk)
    data_tup = context.make_tuple(builder, types.Tuple([geiq__wfi]), [
        ybm__kmue._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    xgag__tivcd = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            lffq__uyru = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lffq__uyru)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            fgo__ssfnw = builder.extract_value(in_dataframe_payload.data, i)
            wir__cxsv = context.cast(builder, fgo__ssfnw, fromty.data[i],
                toty.data[i])
            xegp__efk = False
        else:
            wir__cxsv = builder.extract_value(in_dataframe_payload.data, i)
            xegp__efk = True
        if xegp__efk:
            context.nrt.incref(builder, toty.data[i], wir__cxsv)
        xgag__tivcd.append(wir__cxsv)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), xgag__tivcd)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    oxvu__edmb = fromty.table_type
    jeh__lty = cgutils.create_struct_proxy(oxvu__edmb)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    yyrbj__rffcb = toty.table_type
    jbxhm__kai = cgutils.create_struct_proxy(yyrbj__rffcb)(context, builder)
    jbxhm__kai.parent = in_dataframe_payload.parent
    for dodiu__ykmjy, zug__edv in yyrbj__rffcb.type_to_blk.items():
        dvkus__thpq = context.get_constant(types.int64, len(yyrbj__rffcb.
            block_to_arr_ind[zug__edv]))
        pzkb__ynha, wzs__tcluh = ListInstance.allocate_ex(context, builder,
            types.List(dodiu__ykmjy), dvkus__thpq)
        wzs__tcluh.size = dvkus__thpq
        setattr(jbxhm__kai, f'block_{zug__edv}', wzs__tcluh.value)
    for i in range(len(fromty.data)):
        arux__pfqfs = fromty.data[i]
        mzn__ozg = toty.data[i]
        if arux__pfqfs != mzn__ozg:
            lffq__uyru = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lffq__uyru)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        tqh__yyf = oxvu__edmb.type_to_blk[arux__pfqfs]
        vwabw__hur = getattr(jeh__lty, f'block_{tqh__yyf}')
        lrjh__gvlh = ListInstance(context, builder, types.List(arux__pfqfs),
            vwabw__hur)
        jhpof__tjd = context.get_constant(types.int64, oxvu__edmb.
            block_offsets[i])
        fgo__ssfnw = lrjh__gvlh.getitem(jhpof__tjd)
        if arux__pfqfs != mzn__ozg:
            wir__cxsv = context.cast(builder, fgo__ssfnw, arux__pfqfs, mzn__ozg
                )
            xegp__efk = False
        else:
            wir__cxsv = fgo__ssfnw
            xegp__efk = True
        hsf__zcx = yyrbj__rffcb.type_to_blk[dodiu__ykmjy]
        wzs__tcluh = getattr(jbxhm__kai, f'block_{hsf__zcx}')
        hka__gely = ListInstance(context, builder, types.List(mzn__ozg),
            wzs__tcluh)
        wqfah__ihdy = context.get_constant(types.int64, yyrbj__rffcb.
            block_offsets[i])
        hka__gely.setitem(wqfah__ihdy, wir__cxsv, xegp__efk)
    data_tup = context.make_tuple(builder, types.Tuple([yyrbj__rffcb]), [
        jbxhm__kai._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    geiq__wfi = fromty.table_type
    ybm__kmue = cgutils.create_struct_proxy(geiq__wfi)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    xgag__tivcd = []
    for i, dodiu__ykmjy in enumerate(toty.data):
        arux__pfqfs = fromty.data[i]
        if dodiu__ykmjy != arux__pfqfs:
            lffq__uyru = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lffq__uyru)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        zug__edv = geiq__wfi.type_to_blk[arux__pfqfs]
        ojrkc__ytbw = getattr(ybm__kmue, f'block_{zug__edv}')
        lpgo__gsklj = ListInstance(context, builder, types.List(arux__pfqfs
            ), ojrkc__ytbw)
        asoib__upyb = context.get_constant(types.int64, geiq__wfi.
            block_offsets[i])
        fgo__ssfnw = lpgo__gsklj.getitem(asoib__upyb)
        if dodiu__ykmjy != arux__pfqfs:
            wir__cxsv = context.cast(builder, fgo__ssfnw, arux__pfqfs,
                dodiu__ykmjy)
        else:
            wir__cxsv = fgo__ssfnw
            context.nrt.incref(builder, dodiu__ykmjy, wir__cxsv)
        xgag__tivcd.append(wir__cxsv)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), xgag__tivcd)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    viiym__xntpq, mzvy__lcvnj, index_arg = _get_df_args(data, index,
        columns, dtype, copy)
    fgvx__sdj = ColNamesMetaType(tuple(viiym__xntpq))
    epq__mwl = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    epq__mwl += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(mzvy__lcvnj, index_arg))
    nvyr__gligm = {}
    exec(epq__mwl, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': fgvx__sdj}, nvyr__gligm)
    xbri__zjfin = nvyr__gligm['_init_df']
    return xbri__zjfin


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    maiu__ttqog = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(maiu__ttqog, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    maiu__ttqog = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(maiu__ttqog, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    wuu__wjmib = ''
    if not is_overload_none(dtype):
        wuu__wjmib = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        xfnk__ejfl = (len(data.types) - 1) // 2
        jiaqt__bgu = [dodiu__ykmjy.literal_value for dodiu__ykmjy in data.
            types[1:xfnk__ejfl + 1]]
        data_val_types = dict(zip(jiaqt__bgu, data.types[xfnk__ejfl + 1:]))
        xgag__tivcd = ['data[{}]'.format(i) for i in range(xfnk__ejfl + 1, 
            2 * xfnk__ejfl + 1)]
        data_dict = dict(zip(jiaqt__bgu, xgag__tivcd))
        if is_overload_none(index):
            for i, dodiu__ykmjy in enumerate(data.types[xfnk__ejfl + 1:]):
                if isinstance(dodiu__ykmjy, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(xfnk__ejfl + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        becpb__tjoj = '.copy()' if copy else ''
        lvd__htly = get_overload_const_list(columns)
        xfnk__ejfl = len(lvd__htly)
        data_val_types = {epzhw__jytyl: data.copy(ndim=1) for epzhw__jytyl in
            lvd__htly}
        xgag__tivcd = ['data[:,{}]{}'.format(i, becpb__tjoj) for i in range
            (xfnk__ejfl)]
        data_dict = dict(zip(lvd__htly, xgag__tivcd))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    mzvy__lcvnj = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[epzhw__jytyl], df_len, wuu__wjmib) for
        epzhw__jytyl in col_names))
    if len(col_names) == 0:
        mzvy__lcvnj = '()'
    return col_names, mzvy__lcvnj, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for epzhw__jytyl in col_names:
        if epzhw__jytyl in data_dict and is_iterable_type(data_val_types[
            epzhw__jytyl]):
            df_len = 'len({})'.format(data_dict[epzhw__jytyl])
            break
    if df_len == '0':
        if not index_is_none:
            df_len = f'len({index_arg})'
        elif data_dict:
            raise BodoError(
                'Internal Error: Unable to determine length of DataFrame Index. If this is unexpected, please try passing an index value.'
                )
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(epzhw__jytyl in data_dict for epzhw__jytyl in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    hdihm__zqk = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for epzhw__jytyl in col_names:
        if epzhw__jytyl not in data_dict:
            data_dict[epzhw__jytyl] = hdihm__zqk


@infer_global(len)
class LenTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        if isinstance(args[0], (DataFrameType, bodo.TableType)):
            return types.int64(*args)


@lower_builtin(len, DataFrameType)
def table_len_lower(context, builder, sig, args):
    impl = df_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if df.has_runtime_cols:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            dodiu__ykmjy = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(
                df)
            return len(dodiu__ykmjy)
        return impl
    if len(df.columns) == 0:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
        return impl

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        cck__xrrfp = idx.literal_value
        if isinstance(cck__xrrfp, int):
            vqmsn__cwfa = tup.types[cck__xrrfp]
        elif isinstance(cck__xrrfp, slice):
            vqmsn__cwfa = types.BaseTuple.from_types(tup.types[cck__xrrfp])
        return signature(vqmsn__cwfa, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    zmzw__qdlvx, idx = sig.args
    idx = idx.literal_value
    tup, pzkb__ynha = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(zmzw__qdlvx)
        if not 0 <= idx < len(zmzw__qdlvx):
            raise IndexError('cannot index at %d in %s' % (idx, zmzw__qdlvx))
        wdyf__njq = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        hhsf__grrqu = cgutils.unpack_tuple(builder, tup)[idx]
        wdyf__njq = context.make_tuple(builder, sig.return_type, hhsf__grrqu)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, wdyf__njq)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, bcc__euzsw, suffix_x,
            suffix_y, is_join, indicator, pzkb__ynha, pzkb__ynha) = args
        how = get_overload_const_str(bcc__euzsw)
        if how == 'cross':
            data = left_df.data + right_df.data
            columns = left_df.columns + right_df.columns
            hfhok__fhch = DataFrameType(data, RangeIndexType(types.none),
                columns, is_table_format=True)
            return signature(hfhok__fhch, *args)
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        asjns__nue = {epzhw__jytyl: i for i, epzhw__jytyl in enumerate(left_on)
            }
        yetco__pnhv = {epzhw__jytyl: i for i, epzhw__jytyl in enumerate(
            right_on)}
        tiza__vvfy = set(left_on) & set(right_on)
        sca__imhee = set(left_df.columns) & set(right_df.columns)
        xqtv__dfit = sca__imhee - tiza__vvfy
        oxkbq__xwjg = '$_bodo_index_' in left_on
        ucda__lepbw = '$_bodo_index_' in right_on
        kkj__nvk = how in {'left', 'outer'}
        myau__evrw = how in {'right', 'outer'}
        columns = []
        data = []
        if oxkbq__xwjg or ucda__lepbw:
            if oxkbq__xwjg:
                jmrjd__khcyo = bodo.utils.typing.get_index_data_arr_types(
                    left_df.index)[0]
            else:
                jmrjd__khcyo = left_df.data[left_df.column_index[left_on[0]]]
            if ucda__lepbw:
                ufv__msz = bodo.utils.typing.get_index_data_arr_types(right_df
                    .index)[0]
            else:
                ufv__msz = right_df.data[right_df.column_index[right_on[0]]]
        if oxkbq__xwjg and not ucda__lepbw and not is_join.literal_value:
            blap__krjbp = right_on[0]
            if blap__krjbp in left_df.column_index:
                columns.append(blap__krjbp)
                if (ufv__msz == bodo.dict_str_arr_type and jmrjd__khcyo ==
                    bodo.string_array_type):
                    bfko__wlr = bodo.string_array_type
                else:
                    bfko__wlr = ufv__msz
                data.append(bfko__wlr)
        if ucda__lepbw and not oxkbq__xwjg and not is_join.literal_value:
            jaer__qeq = left_on[0]
            if jaer__qeq in right_df.column_index:
                columns.append(jaer__qeq)
                if (jmrjd__khcyo == bodo.dict_str_arr_type and ufv__msz ==
                    bodo.string_array_type):
                    bfko__wlr = bodo.string_array_type
                else:
                    bfko__wlr = jmrjd__khcyo
                data.append(bfko__wlr)
        for arux__pfqfs, hyvnc__yrk in zip(left_df.data, left_df.columns):
            columns.append(str(hyvnc__yrk) + suffix_x.literal_value if 
                hyvnc__yrk in xqtv__dfit else hyvnc__yrk)
            if hyvnc__yrk in tiza__vvfy:
                if arux__pfqfs == bodo.dict_str_arr_type:
                    arux__pfqfs = right_df.data[right_df.column_index[
                        hyvnc__yrk]]
                data.append(arux__pfqfs)
            else:
                if (arux__pfqfs == bodo.dict_str_arr_type and hyvnc__yrk in
                    asjns__nue):
                    if ucda__lepbw:
                        arux__pfqfs = ufv__msz
                    else:
                        lan__lfd = asjns__nue[hyvnc__yrk]
                        wrj__vupu = right_on[lan__lfd]
                        arux__pfqfs = right_df.data[right_df.column_index[
                            wrj__vupu]]
                if myau__evrw:
                    arux__pfqfs = to_nullable_type(arux__pfqfs)
                data.append(arux__pfqfs)
        for arux__pfqfs, hyvnc__yrk in zip(right_df.data, right_df.columns):
            if hyvnc__yrk not in tiza__vvfy:
                columns.append(str(hyvnc__yrk) + suffix_y.literal_value if 
                    hyvnc__yrk in xqtv__dfit else hyvnc__yrk)
                if (arux__pfqfs == bodo.dict_str_arr_type and hyvnc__yrk in
                    yetco__pnhv):
                    if oxkbq__xwjg:
                        arux__pfqfs = jmrjd__khcyo
                    else:
                        lan__lfd = yetco__pnhv[hyvnc__yrk]
                        xygfn__poj = left_on[lan__lfd]
                        arux__pfqfs = left_df.data[left_df.column_index[
                            xygfn__poj]]
                if kkj__nvk:
                    arux__pfqfs = to_nullable_type(arux__pfqfs)
                data.append(arux__pfqfs)
        nau__scxd = get_overload_const_bool(indicator)
        if nau__scxd:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        jih__afrsn = False
        if oxkbq__xwjg and ucda__lepbw and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            jih__afrsn = True
        elif oxkbq__xwjg and not ucda__lepbw:
            index_typ = right_df.index
            jih__afrsn = True
        elif ucda__lepbw and not oxkbq__xwjg:
            index_typ = left_df.index
            jih__afrsn = True
        if jih__afrsn and isinstance(index_typ, bodo.hiframes.pd_index_ext.
            RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        hfhok__fhch = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(hfhok__fhch, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    wwhw__blt = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return wwhw__blt._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    if not is_overload_constant_int(axis):
        raise BodoError("pd.concat(): 'axis' should be a constant integer")
    if not is_overload_constant_bool(ignore_index):
        raise BodoError(
            "pd.concat(): 'ignore_index' should be a constant boolean")
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    ave__gqhe = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    xkw__wfftr = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', ave__gqhe, xkw__wfftr,
        package_name='pandas', module_name='General')
    epq__mwl = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        gmp__xpdhc = 0
        mzvy__lcvnj = []
        names = []
        for i, xcbkp__tjr in enumerate(objs.types):
            assert isinstance(xcbkp__tjr, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(xcbkp__tjr, 'pandas.concat()')
            if isinstance(xcbkp__tjr, SeriesType):
                names.append(str(gmp__xpdhc))
                gmp__xpdhc += 1
                mzvy__lcvnj.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(xcbkp__tjr.columns)
                for mlup__plp in range(len(xcbkp__tjr.data)):
                    mzvy__lcvnj.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, mlup__plp))
        return bodo.hiframes.dataframe_impl._gen_init_df(epq__mwl, names,
            ', '.join(mzvy__lcvnj), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(dodiu__ykmjy, DataFrameType) for dodiu__ykmjy in
            objs.types)
        nze__ftg = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            nze__ftg.extend(df.columns)
        nze__ftg = list(dict.fromkeys(nze__ftg).keys())
        isd__rpxzh = {}
        for gmp__xpdhc, epzhw__jytyl in enumerate(nze__ftg):
            for i, df in enumerate(objs.types):
                if epzhw__jytyl in df.column_index:
                    isd__rpxzh[f'arr_typ{gmp__xpdhc}'] = df.data[df.
                        column_index[epzhw__jytyl]]
                    break
        assert len(isd__rpxzh) == len(nze__ftg)
        hoez__rhd = []
        for gmp__xpdhc, epzhw__jytyl in enumerate(nze__ftg):
            args = []
            for i, df in enumerate(objs.types):
                if epzhw__jytyl in df.column_index:
                    plygj__tbox = df.column_index[epzhw__jytyl]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, plygj__tbox))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, gmp__xpdhc))
            epq__mwl += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'.
                format(gmp__xpdhc, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(epq__mwl, nze__ftg,
            ', '.join('A{}'.format(i) for i in range(len(nze__ftg))), index,
            isd__rpxzh)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(dodiu__ykmjy, SeriesType) for dodiu__ykmjy in
            objs.types)
        epq__mwl += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'.
            format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            epq__mwl += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            epq__mwl += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        epq__mwl += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        nvyr__gligm = {}
        exec(epq__mwl, {'bodo': bodo, 'np': np, 'numba': numba}, nvyr__gligm)
        return nvyr__gligm['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for gmp__xpdhc, epzhw__jytyl in enumerate(df_type.columns):
            epq__mwl += '  arrs{} = []\n'.format(gmp__xpdhc)
            epq__mwl += '  for i in range(len(objs)):\n'
            epq__mwl += '    df = objs[i]\n'
            epq__mwl += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(gmp__xpdhc))
            epq__mwl += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(gmp__xpdhc))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            epq__mwl += '  arrs_index = []\n'
            epq__mwl += '  for i in range(len(objs)):\n'
            epq__mwl += '    df = objs[i]\n'
            epq__mwl += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(epq__mwl, df_type.
            columns, ', '.join('out_arr{}'.format(i) for i in range(len(
            df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        epq__mwl += '  arrs = []\n'
        epq__mwl += '  for i in range(len(objs)):\n'
        epq__mwl += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        epq__mwl += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            epq__mwl += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            epq__mwl += '  arrs_index = []\n'
            epq__mwl += '  for i in range(len(objs)):\n'
            epq__mwl += '    S = objs[i]\n'
            epq__mwl += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            epq__mwl += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        epq__mwl += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        nvyr__gligm = {}
        exec(epq__mwl, {'bodo': bodo, 'np': np, 'numba': numba}, nvyr__gligm)
        return nvyr__gligm['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position,
    _bodo_chunk_bounds):
    pass


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df = args[0]
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        maiu__ttqog = df.copy(index=index)
        return signature(maiu__ttqog, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    gsg__lrv = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return gsg__lrv._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    ave__gqhe = dict(index=index, name=name)
    xkw__wfftr = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', ave__gqhe, xkw__wfftr,
        package_name='pandas', module_name='DataFrame')

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        isd__rpxzh = (types.Array(types.int64, 1, 'C'),) + df.data
        zew__wkw = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(columns,
            isd__rpxzh)
        return signature(zew__wkw, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    gsg__lrv = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return gsg__lrv._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    gsg__lrv = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return gsg__lrv._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    gsg__lrv = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return gsg__lrv._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    jwk__wiq = get_overload_const_bool(check_duplicates)
    wus__pzmd = not get_overload_const_bool(is_already_shuffled)
    ltcb__hspro = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    ysyz__daqwj = len(value_names) > 1
    ajive__uikb = None
    nmjrc__akc = None
    yqtt__olafc = None
    ohy__ffla = None
    zou__xum = isinstance(values_tup, types.UniTuple)
    if zou__xum:
        cii__wkeoc = [to_str_arr_if_dict_array(to_nullable_type(values_tup.
            dtype))]
    else:
        cii__wkeoc = [to_str_arr_if_dict_array(to_nullable_type(mzf__iceei)
            ) for mzf__iceei in values_tup]
    epq__mwl = 'def impl(\n'
    epq__mwl += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    epq__mwl += '):\n'
    epq__mwl += "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n"
    if wus__pzmd:
        epq__mwl += '    if parallel:\n'
        epq__mwl += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        has__dorac = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        epq__mwl += f'        info_list = [{has__dorac}]\n'
        epq__mwl += '        cpp_table = arr_info_list_to_table(info_list)\n'
        epq__mwl += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        jnpy__qzsh = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        diymy__ipjg = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        ymm__qam = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        epq__mwl += f'        index_tup = ({jnpy__qzsh},)\n'
        epq__mwl += f'        columns_tup = ({diymy__ipjg},)\n'
        epq__mwl += f'        values_tup = ({ymm__qam},)\n'
        epq__mwl += '        delete_table(cpp_table)\n'
        epq__mwl += '        delete_table(out_cpp_table)\n'
        epq__mwl += '        ev_shuffle.finalize()\n'
    epq__mwl += '    columns_arr = columns_tup[0]\n'
    if zou__xum:
        epq__mwl += '    values_arrs = [arr for arr in values_tup]\n'
    epq__mwl += (
        "    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)\n"
        )
    epq__mwl += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    epq__mwl += '        index_tup\n'
    epq__mwl += '    )\n'
    epq__mwl += '    n_rows = len(unique_index_arr_tup[0])\n'
    epq__mwl += '    num_values_arrays = len(values_tup)\n'
    epq__mwl += '    n_unique_pivots = len(pivot_values)\n'
    if zou__xum:
        epq__mwl += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        epq__mwl += '    n_cols = n_unique_pivots\n'
    epq__mwl += '    col_map = {}\n'
    epq__mwl += '    for i in range(n_unique_pivots):\n'
    epq__mwl += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    epq__mwl += '            raise ValueError(\n'
    epq__mwl += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    epq__mwl += '            )\n'
    epq__mwl += '        col_map[pivot_values[i]] = i\n'
    epq__mwl += '    ev_unique.finalize()\n'
    epq__mwl += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    nmqw__xhbjl = False
    for i, ecx__dxg in enumerate(cii__wkeoc):
        if is_str_arr_type(ecx__dxg):
            nmqw__xhbjl = True
            epq__mwl += (
                f'    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]\n'
                )
            epq__mwl += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if nmqw__xhbjl:
        if jwk__wiq:
            epq__mwl += '    nbytes = (n_rows + 7) >> 3\n'
            epq__mwl += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        epq__mwl += '    for i in range(len(columns_arr)):\n'
        epq__mwl += '        col_name = columns_arr[i]\n'
        epq__mwl += '        pivot_idx = col_map[col_name]\n'
        epq__mwl += '        row_idx = row_vector[i]\n'
        if jwk__wiq:
            epq__mwl += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            epq__mwl += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            epq__mwl += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            epq__mwl += '        else:\n'
            epq__mwl += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if zou__xum:
            epq__mwl += '        for j in range(num_values_arrays):\n'
            epq__mwl += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            epq__mwl += '            len_arr = len_arrs_0[col_idx]\n'
            epq__mwl += '            values_arr = values_arrs[j]\n'
            epq__mwl += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            epq__mwl += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            epq__mwl += '                len_arr[row_idx] = str_val_len\n'
            epq__mwl += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, ecx__dxg in enumerate(cii__wkeoc):
                if is_str_arr_type(ecx__dxg):
                    epq__mwl += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    epq__mwl += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    epq__mwl += (
                        f'            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}\n'
                        )
                    epq__mwl += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    epq__mwl += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, ecx__dxg in enumerate(cii__wkeoc):
        if is_str_arr_type(ecx__dxg):
            epq__mwl += f'    data_arrs_{i} = [\n'
            epq__mwl += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            epq__mwl += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            epq__mwl += '        )\n'
            epq__mwl += '        for i in range(n_cols)\n'
            epq__mwl += '    ]\n'
            epq__mwl += f'    if tracing.is_tracing():\n'
            epq__mwl += '         for i in range(n_cols):\n'
            epq__mwl += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            epq__mwl += f'    data_arrs_{i} = [\n'
            epq__mwl += (
                f'        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})\n'
                )
            epq__mwl += '        for _ in range(n_cols)\n'
            epq__mwl += '    ]\n'
    if not nmqw__xhbjl and jwk__wiq:
        epq__mwl += '    nbytes = (n_rows + 7) >> 3\n'
        epq__mwl += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    epq__mwl += '    ev_alloc.finalize()\n'
    epq__mwl += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    epq__mwl += '    for i in range(len(columns_arr)):\n'
    epq__mwl += '        col_name = columns_arr[i]\n'
    epq__mwl += '        pivot_idx = col_map[col_name]\n'
    epq__mwl += '        row_idx = row_vector[i]\n'
    if not nmqw__xhbjl and jwk__wiq:
        epq__mwl += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        epq__mwl += (
            '        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):\n'
            )
        epq__mwl += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        epq__mwl += '        else:\n'
        epq__mwl += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if zou__xum:
        epq__mwl += '        for j in range(num_values_arrays):\n'
        epq__mwl += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        epq__mwl += '            col_arr = data_arrs_0[col_idx]\n'
        epq__mwl += '            values_arr = values_arrs[j]\n'
        epq__mwl += """            bodo.libs.array_kernels.copy_array_element(col_arr, row_idx, values_arr, i)
"""
    else:
        for i, ecx__dxg in enumerate(cii__wkeoc):
            epq__mwl += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            epq__mwl += f"""        bodo.libs.array_kernels.copy_array_element(col_arr_{i}, row_idx, values_tup[{i}], i)
"""
    if len(index_names) == 1:
        epq__mwl += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        ajive__uikb = index_names.meta[0]
    else:
        epq__mwl += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        ajive__uikb = tuple(index_names.meta)
    epq__mwl += f'    if tracing.is_tracing():\n'
    epq__mwl += f'        index_nbytes = index.nbytes\n'
    epq__mwl += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not ltcb__hspro:
        yqtt__olafc = columns_name.meta[0]
        if ysyz__daqwj:
            epq__mwl += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            nmjrc__akc = value_names.meta
            if all(isinstance(epzhw__jytyl, str) for epzhw__jytyl in nmjrc__akc
                ):
                nmjrc__akc = pd.array(nmjrc__akc, 'string')
            elif all(isinstance(epzhw__jytyl, int) for epzhw__jytyl in
                nmjrc__akc):
                nmjrc__akc = np.array(nmjrc__akc, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(nmjrc__akc.dtype, pd.StringDtype):
                epq__mwl += '    total_chars = 0\n'
                epq__mwl += f'    for i in range({len(value_names)}):\n'
                epq__mwl += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                epq__mwl += '        total_chars += value_name_str_len\n'
                epq__mwl += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                epq__mwl += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                epq__mwl += '    total_chars = 0\n'
                epq__mwl += '    for i in range(len(pivot_values)):\n'
                epq__mwl += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                epq__mwl += '        total_chars += pivot_val_str_len\n'
                epq__mwl += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                epq__mwl += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            epq__mwl += f'    for i in range({len(value_names)}):\n'
            epq__mwl += '        for j in range(len(pivot_values)):\n'
            epq__mwl += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            epq__mwl += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            epq__mwl += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            epq__mwl += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    epq__mwl += '    ev_fill.finalize()\n'
    geiq__wfi = None
    if ltcb__hspro:
        if ysyz__daqwj:
            oey__eycn = []
            for bkbxi__cckl in _constant_pivot_values.meta:
                for kxo__xarug in value_names.meta:
                    oey__eycn.append((bkbxi__cckl, kxo__xarug))
            column_names = tuple(oey__eycn)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        ohy__ffla = ColNamesMetaType(column_names)
        dqi__sadb = []
        for mzf__iceei in cii__wkeoc:
            dqi__sadb.extend([mzf__iceei] * len(_constant_pivot_values))
        pqh__aju = tuple(dqi__sadb)
        geiq__wfi = TableType(pqh__aju)
        epq__mwl += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        epq__mwl += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, mzf__iceei in enumerate(cii__wkeoc):
            epq__mwl += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {geiq__wfi.type_to_blk[mzf__iceei]})
"""
        epq__mwl += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        epq__mwl += '        (table,), index, columns_typ\n'
        epq__mwl += '    )\n'
    else:
        olljl__vhli = ', '.join(f'data_arrs_{i}' for i in range(len(
            cii__wkeoc)))
        epq__mwl += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({olljl__vhli},), n_rows)
"""
        epq__mwl += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
            )
        epq__mwl += '        (table,), index, column_index\n'
        epq__mwl += '    )\n'
    epq__mwl += '    ev.finalize()\n'
    epq__mwl += '    return result\n'
    nvyr__gligm = {}
    nceep__yvwch = {f'data_arr_typ_{i}': ecx__dxg for i, ecx__dxg in
        enumerate(cii__wkeoc)}
    hnkmz__keu = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        geiq__wfi, 'columns_typ': ohy__ffla, 'index_names_lit': ajive__uikb,
        'value_names_lit': nmjrc__akc, 'columns_name_lit': yqtt__olafc, **
        nceep__yvwch, 'tracing': tracing}
    exec(epq__mwl, hnkmz__keu, nvyr__gligm)
    impl = nvyr__gligm['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    phmy__gaoh = {}
    phmy__gaoh['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, ubqv__cyn in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        smynt__msv = None
        if isinstance(ubqv__cyn, bodo.DatetimeArrayType):
            eeh__oveu = 'datetimetz'
            qfti__bru = 'datetime64[ns]'
            if isinstance(ubqv__cyn.tz, int):
                ihe__wfgi = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(ubqv__cyn.tz))
            else:
                ihe__wfgi = pd.DatetimeTZDtype(tz=ubqv__cyn.tz).tz
            smynt__msv = {'timezone': pa.lib.tzinfo_to_string(ihe__wfgi)}
        elif isinstance(ubqv__cyn, types.Array) or ubqv__cyn == boolean_array:
            eeh__oveu = qfti__bru = ubqv__cyn.dtype.name
            if qfti__bru.startswith('datetime'):
                eeh__oveu = 'datetime'
        elif is_str_arr_type(ubqv__cyn):
            eeh__oveu = 'unicode'
            qfti__bru = 'object'
        elif ubqv__cyn == binary_array_type:
            eeh__oveu = 'bytes'
            qfti__bru = 'object'
        elif isinstance(ubqv__cyn, DecimalArrayType):
            eeh__oveu = qfti__bru = 'object'
        elif isinstance(ubqv__cyn, IntegerArrayType):
            fkolp__khz = ubqv__cyn.dtype.name
            if fkolp__khz.startswith('int'):
                qfti__bru = 'Int' + fkolp__khz[3:]
            elif fkolp__khz.startswith('uint'):
                qfti__bru = 'UInt' + fkolp__khz[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, ubqv__cyn))
            eeh__oveu = ubqv__cyn.dtype.name
        elif isinstance(ubqv__cyn, bodo.FloatingArrayType):
            fkolp__khz = ubqv__cyn.dtype.name
            eeh__oveu = fkolp__khz
            qfti__bru = fkolp__khz.capitalize()
        elif ubqv__cyn == datetime_date_array_type:
            eeh__oveu = 'datetime'
            qfti__bru = 'object'
        elif isinstance(ubqv__cyn, TimeArrayType):
            eeh__oveu = 'datetime'
            qfti__bru = 'object'
        elif isinstance(ubqv__cyn, (StructArrayType, ArrayItemArrayType)):
            eeh__oveu = 'object'
            qfti__bru = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, ubqv__cyn))
        bpwx__tazfl = {'name': col_name, 'field_name': col_name,
            'pandas_type': eeh__oveu, 'numpy_type': qfti__bru, 'metadata':
            smynt__msv}
        phmy__gaoh['columns'].append(bpwx__tazfl)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            vvcl__uyn = '__index_level_0__'
            nlbs__cfst = None
        else:
            vvcl__uyn = '%s'
            nlbs__cfst = '%s'
        phmy__gaoh['index_columns'] = [vvcl__uyn]
        phmy__gaoh['columns'].append({'name': nlbs__cfst, 'field_name':
            vvcl__uyn, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        phmy__gaoh['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        phmy__gaoh['index_columns'] = []
    phmy__gaoh['pandas_version'] = pd.__version__
    return phmy__gaoh


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, path, engine='auto', compression='snappy',
    index=None, partition_cols=None, storage_options=None, row_group_size=-
    1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
    check_unsupported_args('DataFrame.to_parquet', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if df.has_runtime_cols and not is_overload_none(partition_cols):
        raise BodoError(
            f"DataFrame.to_parquet(): Providing 'partition_cols' on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information."
            )
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        anuk__chsw = []
        for sbjl__tjqg in partition_cols:
            try:
                idx = df.columns.index(sbjl__tjqg)
            except ValueError as chx__glx:
                raise BodoError(
                    f'Partition column {sbjl__tjqg} is not in dataframe')
            anuk__chsw.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    if not is_overload_none(_bodo_timestamp_tz) and (not
        is_overload_constant_str(_bodo_timestamp_tz) or not
        get_overload_const_str(_bodo_timestamp_tz)):
        raise BodoError(
            'to_parquet(): _bodo_timestamp_tz must be None or a constant string'
            )
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    bblj__tvds = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType
        )
    hyii__gxfl = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not bblj__tvds)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not bblj__tvds or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and bblj__tvds and not is_overload_true(_is_parallel)
    if df.has_runtime_cols:
        if isinstance(df.runtime_colname_typ, MultiIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): Not supported with MultiIndex runtime column names. Please return the DataFrame to regular Python to update typing information.'
                )
        if not isinstance(df.runtime_colname_typ, bodo.hiframes.
            pd_index_ext.StringIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): parquet must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
        ucmr__dgz = df.runtime_data_types
        oygf__ghf = len(ucmr__dgz)
        smynt__msv = gen_pandas_parquet_metadata([''] * oygf__ghf,
            ucmr__dgz, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        dqg__xqk = smynt__msv['columns'][:oygf__ghf]
        smynt__msv['columns'] = smynt__msv['columns'][oygf__ghf:]
        dqg__xqk = [json.dumps(cjif__ltf).replace('""', '{0}') for
            cjif__ltf in dqg__xqk]
        lkuhv__sdg = json.dumps(smynt__msv)
        qcmco__erey = '"columns": ['
        youog__jggo = lkuhv__sdg.find(qcmco__erey)
        if youog__jggo == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        naxm__xwz = youog__jggo + len(qcmco__erey)
        jlz__owylw = lkuhv__sdg[:naxm__xwz]
        lkuhv__sdg = lkuhv__sdg[naxm__xwz:]
        amgi__hjg = len(smynt__msv['columns'])
    else:
        lkuhv__sdg = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and bblj__tvds:
        lkuhv__sdg = lkuhv__sdg.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            lkuhv__sdg = lkuhv__sdg.replace('"%s"', '%s')
    if not df.is_table_format:
        mzvy__lcvnj = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    epq__mwl = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        epq__mwl += '    py_table = get_dataframe_table(df)\n'
        epq__mwl += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        epq__mwl += '    info_list = [{}]\n'.format(mzvy__lcvnj)
        epq__mwl += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        epq__mwl += '    columns_index = get_dataframe_column_names(df)\n'
        epq__mwl += '    names_arr = index_to_array(columns_index)\n'
        epq__mwl += '    col_names = array_to_info(names_arr)\n'
    else:
        epq__mwl += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and hyii__gxfl:
        epq__mwl += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        deo__aoe = True
    else:
        epq__mwl += '    index_col = array_to_info(np.empty(0))\n'
        deo__aoe = False
    if df.has_runtime_cols:
        epq__mwl += '    columns_lst = []\n'
        epq__mwl += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            epq__mwl += f'    for _ in range(len(py_table.block_{i})):\n'
            epq__mwl += f"""        columns_lst.append({dqg__xqk[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            epq__mwl += '        num_cols += 1\n'
        if amgi__hjg:
            epq__mwl += "    columns_lst.append('')\n"
        epq__mwl += '    columns_str = ", ".join(columns_lst)\n'
        epq__mwl += ('    metadata = """' + jlz__owylw +
            '""" + columns_str + """' + lkuhv__sdg + '"""\n')
    else:
        epq__mwl += '    metadata = """' + lkuhv__sdg + '"""\n'
    epq__mwl += '    if compression is None:\n'
    epq__mwl += "        compression = 'none'\n"
    epq__mwl += '    if _bodo_timestamp_tz is None:\n'
    epq__mwl += "        _bodo_timestamp_tz = ''\n"
    epq__mwl += '    if df.index.name is not None:\n'
    epq__mwl += '        name_ptr = df.index.name\n'
    epq__mwl += '    else:\n'
    epq__mwl += "        name_ptr = 'null'\n"
    epq__mwl += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    qkw__uht = None
    if partition_cols:
        qkw__uht = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        idbyb__huvs = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in anuk__chsw)
        if idbyb__huvs:
            epq__mwl += '    cat_info_list = [{}]\n'.format(idbyb__huvs)
            epq__mwl += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            epq__mwl += '    cat_table = table\n'
        epq__mwl += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        epq__mwl += (
            f'    part_cols_idxs = np.array({anuk__chsw}, dtype=np.int32)\n')
        epq__mwl += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        epq__mwl += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        epq__mwl += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        epq__mwl += (
            '                            unicode_to_utf8(compression),\n')
        epq__mwl += '                            _is_parallel,\n'
        epq__mwl += (
            '                            unicode_to_utf8(bucket_region),\n')
        epq__mwl += '                            row_group_size,\n'
        epq__mwl += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        epq__mwl += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        epq__mwl += '    delete_table_decref_arrays(table)\n'
        epq__mwl += '    delete_info_decref_array(index_col)\n'
        epq__mwl += '    delete_info_decref_array(col_names_no_partitions)\n'
        epq__mwl += '    delete_info_decref_array(col_names)\n'
        if idbyb__huvs:
            epq__mwl += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        epq__mwl += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        epq__mwl += (
            '                            table, col_names, index_col,\n')
        epq__mwl += '                            ' + str(deo__aoe) + ',\n'
        epq__mwl += '                            unicode_to_utf8(metadata),\n'
        epq__mwl += (
            '                            unicode_to_utf8(compression),\n')
        epq__mwl += (
            '                            _is_parallel, 1, df.index.start,\n')
        epq__mwl += (
            '                            df.index.stop, df.index.step,\n')
        epq__mwl += '                            unicode_to_utf8(name_ptr),\n'
        epq__mwl += (
            '                            unicode_to_utf8(bucket_region),\n')
        epq__mwl += '                            row_group_size,\n'
        epq__mwl += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        epq__mwl += '                              False,\n'
        epq__mwl += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        epq__mwl += '                              False)\n'
        epq__mwl += '    delete_table_decref_arrays(table)\n'
        epq__mwl += '    delete_info_decref_array(index_col)\n'
        epq__mwl += '    delete_info_decref_array(col_names)\n'
    else:
        epq__mwl += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        epq__mwl += (
            '                            table, col_names, index_col,\n')
        epq__mwl += '                            ' + str(deo__aoe) + ',\n'
        epq__mwl += '                            unicode_to_utf8(metadata),\n'
        epq__mwl += (
            '                            unicode_to_utf8(compression),\n')
        epq__mwl += '                            _is_parallel, 0, 0, 0, 0,\n'
        epq__mwl += '                            unicode_to_utf8(name_ptr),\n'
        epq__mwl += (
            '                            unicode_to_utf8(bucket_region),\n')
        epq__mwl += '                            row_group_size,\n'
        epq__mwl += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        epq__mwl += '                              False,\n'
        epq__mwl += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        epq__mwl += '                              False)\n'
        epq__mwl += '    delete_table_decref_arrays(table)\n'
        epq__mwl += '    delete_info_decref_array(index_col)\n'
        epq__mwl += '    delete_info_decref_array(col_names)\n'
    nvyr__gligm = {}
    if df.has_runtime_cols:
        ysc__avl = None
    else:
        for hyvnc__yrk in df.columns:
            if not isinstance(hyvnc__yrk, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        ysc__avl = pd.array(df.columns)
    exec(epq__mwl, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': ysc__avl,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': qkw__uht, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, nvyr__gligm)
    kwm__vih = nvyr__gligm['df_to_parquet']
    return kwm__vih


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    rgsjy__ndvhz = tracing.Event('to_sql_exception_guard', is_parallel=
        _is_parallel)
    duk__aqv = 'all_ok'
    tajt__ypx, zpl__ewajh = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        ubbzs__cahj = 100
        if chunksize is None:
            hduso__hql = ubbzs__cahj
        else:
            hduso__hql = min(chunksize, ubbzs__cahj)
        if _is_table_create:
            df = df.iloc[:hduso__hql, :]
        else:
            df = df.iloc[hduso__hql:, :]
            if len(df) == 0:
                return duk__aqv
    nju__bagc = df.columns
    try:
        if tajt__ypx == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            janml__eas = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            gyr__rbuk = bodo.typeof(df)
            uunat__rwxej = {}
            for epzhw__jytyl, dekld__qrfk in zip(gyr__rbuk.columns,
                gyr__rbuk.data):
                if df[epzhw__jytyl].dtype == 'object':
                    if dekld__qrfk == datetime_date_array_type:
                        uunat__rwxej[epzhw__jytyl] = sa.types.Date
                    elif dekld__qrfk in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not janml__eas or 
                        janml__eas == '0'):
                        uunat__rwxej[epzhw__jytyl] = VARCHAR2(4000)
            dtype = uunat__rwxej
        try:
            ecfih__csry = tracing.Event('df_to_sql', is_parallel=_is_parallel)
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
            ecfih__csry.finalize()
        except Exception as fscbo__yaktc:
            duk__aqv = fscbo__yaktc.args[0]
            if tajt__ypx == 'oracle' and 'ORA-12899' in duk__aqv:
                duk__aqv += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return duk__aqv
    finally:
        df.columns = nju__bagc
        rgsjy__ndvhz.finalize()


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    rgsjy__ndvhz = tracing.Event('to_sql_exception_guard_encaps',
        is_parallel=_is_parallel)
    with numba.objmode(out='unicode_type'):
        jdb__ddh = tracing.Event('to_sql_exception_guard_encaps:objmode',
            is_parallel=_is_parallel)
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
        jdb__ddh.finalize()
    rgsjy__ndvhz.finalize()
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _bodo_allow_downcasting=False, _is_parallel=False):
    import warnings
    check_runtime_cols_unsupported(df, 'DataFrame.to_sql()')
    df: DataFrameType = df
    assert df.columns is not None and df.data is not None
    if is_overload_none(schema):
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'DataFrame.to_sql(): schema argument is recommended to avoid permission issues when writing the table.'
                ))
    if not (is_overload_none(chunksize) or isinstance(chunksize, types.Integer)
        ):
        raise BodoError(
            "DataFrame.to_sql(): 'chunksize' argument must be an integer if provided."
            )
    from bodo.io.helpers import exception_propagating_thread_type
    from bodo.io.parquet_pio import parquet_write_table_cpp
    from bodo.io.snowflake import snowflake_connector_cursor_python_type
    for hyvnc__yrk in df.columns:
        if not isinstance(hyvnc__yrk, str):
            raise BodoError(
                'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
    ysc__avl = pd.array(df.columns)
    epq__mwl = """def df_to_sql(
    df, name, con,
    schema=None, if_exists='fail', index=True,
    index_label=None, chunksize=None, dtype=None,
    method=None, _bodo_allow_downcasting=False,
    _is_parallel=False,
):
"""
    epq__mwl += """    if con.startswith('iceberg'):
        con_str = bodo.io.iceberg.format_iceberg_conn_njit(con)
        if schema is None:
            raise ValueError('DataFrame.to_sql(): schema must be provided when writing to an Iceberg table.')
        if chunksize is not None:
            raise ValueError('DataFrame.to_sql(): chunksize not supported for Iceberg tables.')
        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Iceberg tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Iceberg tables.')
"""
    if df.is_table_format:
        epq__mwl += f'        py_table = get_dataframe_table(df)\n'
        epq__mwl += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        mzvy__lcvnj = ', '.join(
            f'array_to_info(get_dataframe_data(df, {i}))' for i in range(
            len(df.columns)))
        epq__mwl += f'        info_list = [{mzvy__lcvnj}]\n'
        epq__mwl += f'        table = arr_info_list_to_table(info_list)\n'
    epq__mwl += """        col_names = array_to_info(col_names_arr)
        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names,
            if_exists, _is_parallel, pyarrow_table_schema,
            _bodo_allow_downcasting,
        )
        delete_table_decref_arrays(table)
        delete_info_decref_array(col_names)
"""
    epq__mwl += "    elif con.startswith('snowflake'):\n"
    epq__mwl += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        if _bodo_allow_downcasting and bodo.get_rank() == 0:
            warnings.warn('_bodo_allow_downcasting is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl', sync=False)
"""
    epq__mwl += "        location = ''\n"
    if not is_overload_none(schema):
        epq__mwl += '        location += \'"\' + schema + \'".\'\n'
    epq__mwl += '        location += name\n'
    epq__mwl += '        my_rank = bodo.get_rank()\n'
    epq__mwl += """        with bodo.objmode(
            cursor='snowflake_connector_cursor_type',
            tmp_folder='temporary_directory_type',
            stage_name='unicode_type',
            parquet_path='unicode_type',
            upload_using_snowflake_put='boolean',
            old_creds='DictType(unicode_type, unicode_type)',
            azure_stage_direct_upload='boolean',
            old_core_site='unicode_type',
            old_sas_token='unicode_type',
        ):
            (
                cursor, tmp_folder, stage_name, parquet_path, upload_using_snowflake_put, old_creds, azure_stage_direct_upload, old_core_site, old_sas_token,
            ) = bodo.io.snowflake.connect_and_get_upload_info(con)
"""
    epq__mwl += '        bodo.barrier()\n'
    epq__mwl += '        if azure_stage_direct_upload:\n'
    epq__mwl += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    epq__mwl += '        if chunksize is None:\n'
    epq__mwl += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        epq__mwl += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        zxf__iid = ',' if len(df.columns) == 1 else ''
        epq__mwl += (
            f'            memory_usage = np.array(({data}{zxf__iid}), np.int64).sum()\n'
            )
    epq__mwl += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        epq__mwl += '        columns_index = get_dataframe_column_names(df)\n'
        epq__mwl += '        names_arr = index_to_array(columns_index)\n'
        epq__mwl += '        col_names = array_to_info(names_arr)\n'
    else:
        epq__mwl += '        col_names = array_to_info(col_names_arr)\n'
    epq__mwl += '        index_col = array_to_info(np.empty(0))\n'
    epq__mwl += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    epq__mwl += (
        "        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           \n"
        )
    epq__mwl += '        upload_threads_in_progress = []\n'
    epq__mwl += (
        '        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           \n'
        )
    epq__mwl += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    epq__mwl += '            chunk_path = parquet_path + chunk_name\n'
    epq__mwl += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    epq__mwl += '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n'
    epq__mwl += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    epq__mwl += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        epq__mwl += '            py_table_chunk = get_dataframe_table(chunk)\n'
        epq__mwl += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        qbxk__xqa = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        epq__mwl += (
            f'            table_chunk = arr_info_list_to_table([{qbxk__xqa}])     \n'
            )
    epq__mwl += '            ev_to_df_table.finalize()\n'
    epq__mwl += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
            ev_pq_write_cpp.add_attribute('chunk_start', i)
            ev_pq_write_cpp.add_attribute('chunk_end', i + len(chunk))
            ev_pq_write_cpp.add_attribute('chunk_size', len(chunk))
            ev_pq_write_cpp.add_attribute('chunk_path', chunk_path)
            parquet_write_table_cpp(
                unicode_to_utf8(chunk_path),
                table_chunk, col_names, index_col,
                False,
                unicode_to_utf8('null'),
                unicode_to_utf8(bodo.io.snowflake.SF_WRITE_PARQUET_COMPRESSION),
                False,
                0,
                0, 0, 0,
                unicode_to_utf8('null'),
                unicode_to_utf8(bucket_region),
                chunksize,
                unicode_to_utf8('null'),
                True,
                unicode_to_utf8('UTC'),
                True,
            )
            ev_pq_write_cpp.finalize()
            delete_table_decref_arrays(table_chunk)
            if upload_using_snowflake_put:
                with bodo.objmode(upload_thread='types.optional(exception_propagating_thread_type)'):
                    upload_thread = bodo.io.snowflake.do_upload_and_cleanup(
                        cursor, chunk_idx, chunk_path, stage_name,
                    )
                if bodo.io.snowflake.SF_WRITE_OVERLAP_UPLOAD:
                    upload_threads_in_progress.append(upload_thread)
        delete_info_decref_array(index_col)
        delete_info_decref_array(col_names)
        if bodo.io.snowflake.SF_WRITE_OVERLAP_UPLOAD:
            with bodo.objmode():
                bodo.io.helpers.join_all_threads(upload_threads_in_progress)
        ev_upload_df.finalize()
"""
    epq__mwl += '        bodo.barrier()\n'
    aujjo__hjyoi = bodo.io.snowflake.gen_snowflake_schema(df.columns, df.data)
    epq__mwl += f"""        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, {aujjo__hjyoi},
                if_exists, old_creds, tmp_folder,
                azure_stage_direct_upload, old_core_site,
                old_sas_token,
            )
"""
    epq__mwl += '        if azure_stage_direct_upload:\n'
    epq__mwl += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    epq__mwl += '        ev.finalize()\n'
    epq__mwl += '    else:\n'
    epq__mwl += (
        '        if _bodo_allow_downcasting and bodo.get_rank() == 0:\n')
    epq__mwl += """            warnings.warn('_bodo_allow_downcasting is not supported for SQL tables.')
"""
    epq__mwl += '        rank = bodo.libs.distributed_api.get_rank()\n'
    epq__mwl += "        err_msg = 'unset'\n"
    epq__mwl += '        if rank != 0:\n'
    epq__mwl += (
        '            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          \n'
        )
    epq__mwl += '        elif rank == 0:\n'
    epq__mwl += '            err_msg = to_sql_exception_guard_encaps(\n'
    epq__mwl += (
        '                          df, name, con, schema, if_exists, index, index_label,\n'
        )
    epq__mwl += '                          chunksize, dtype, method,\n'
    epq__mwl += '                          True, _is_parallel,\n'
    epq__mwl += '                      )\n'
    epq__mwl += (
        '            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          \n'
        )
    epq__mwl += "        if_exists = 'append'\n"
    epq__mwl += "        if _is_parallel and err_msg == 'all_ok':\n"
    epq__mwl += '            err_msg = to_sql_exception_guard_encaps(\n'
    epq__mwl += (
        '                          df, name, con, schema, if_exists, index, index_label,\n'
        )
    epq__mwl += '                          chunksize, dtype, method,\n'
    epq__mwl += '                          False, _is_parallel,\n'
    epq__mwl += '                      )\n'
    epq__mwl += "        if err_msg != 'all_ok':\n"
    epq__mwl += "            print('err_msg=', err_msg)\n"
    epq__mwl += "            raise ValueError('error in to_sql() operation')\n"
    nvyr__gligm = {}
    hnkmz__keu = globals().copy()
    hnkmz__keu.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        ysc__avl, 'delete_info_decref_array': delete_info_decref_array,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'get_dataframe_column_names': get_dataframe_column_names,
        'get_dataframe_data': get_dataframe_data, 'get_dataframe_table':
        get_dataframe_table, 'index_to_array': index_to_array, 'np': np,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'pyarrow_table_schema': bodo.io.helpers.
        numba_to_pyarrow_schema(df, is_iceberg=True), 'time': time,
        'to_sql_exception_guard_encaps': to_sql_exception_guard_encaps,
        'tracing': tracing, 'unicode_to_utf8': unicode_to_utf8, 'warnings':
        warnings})
    exec(epq__mwl, hnkmz__keu, nvyr__gligm)
    _impl = nvyr__gligm['df_to_sql']
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=
    None, _bodo_file_prefix='part-'):
    check_runtime_cols_unsupported(df, 'DataFrame.to_csv()')
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None}, package_name='pandas', module_name='IO')
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        cgyw__ytxyh = get_overload_const_str(path_or_buf)
        if cgyw__ytxyh.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if not (is_overload_none(columns) or isinstance(columns, (types.List,
        types.Tuple))):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must be list a or tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None, _bodo_file_prefix=
            'part-'):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None, _bodo_file_prefix='part-'):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D, _bodo_file_prefix)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='records', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=True, compression='infer', index=True,
    indent=None, storage_options=None, _bodo_file_prefix='part-'):
    check_runtime_cols_unsupported(df, 'DataFrame.to_json()')
    check_unsupported_args('DataFrame.to_json', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='records', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=True, compression='infer', index=
            True, indent=None, storage_options=None, _bodo_file_prefix='part-'
            ):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent,
                    storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='records', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=True, compression='infer', index=True,
        indent=None, storage_options=None, _bodo_file_prefix='part-'):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent, storage_options)
        egzj__saki = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(egzj__saki), unicode_to_utf8(_bodo_file_prefix)
                )
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(egzj__saki), unicode_to_utf8(_bodo_file_prefix)
                )
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    xqds__ioc = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    yqb__ith = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', xqds__ioc, yqb__ith,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    epq__mwl = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        avwff__rvn = data.data.dtype.categories
        epq__mwl += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        avwff__rvn = data.dtype.categories
        epq__mwl += '  data_values = data\n'
    xfnk__ejfl = len(avwff__rvn)
    epq__mwl += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    epq__mwl += '  numba.parfors.parfor.init_prange()\n'
    epq__mwl += '  n = len(data_values)\n'
    for i in range(xfnk__ejfl):
        epq__mwl += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    epq__mwl += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    epq__mwl += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for mlup__plp in range(xfnk__ejfl):
        epq__mwl += '          data_arr_{}[i] = 0\n'.format(mlup__plp)
    epq__mwl += '      else:\n'
    for qzhkf__qlahk in range(xfnk__ejfl):
        epq__mwl += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            qzhkf__qlahk)
    mzvy__lcvnj = ', '.join(f'data_arr_{i}' for i in range(xfnk__ejfl))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(avwff__rvn[0], np.datetime64):
        avwff__rvn = tuple(pd.Timestamp(epzhw__jytyl) for epzhw__jytyl in
            avwff__rvn)
    elif isinstance(avwff__rvn[0], np.timedelta64):
        avwff__rvn = tuple(pd.Timedelta(epzhw__jytyl) for epzhw__jytyl in
            avwff__rvn)
    return bodo.hiframes.dataframe_impl._gen_init_df(epq__mwl, avwff__rvn,
        mzvy__lcvnj, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelFile, pd.read_html, pd.read_xml, pd.read_hdf,
    pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_query, pd.read_gbq, pd.read_stata, pd.ExcelWriter, pd.
    json_normalize, pd.merge_ordered, pd.factorize, pd.wide_to_long, pd.
    bdate_range, pd.period_range, pd.infer_freq, pd.interval_range, pd.eval,
    pd.test, pd.Grouper)
pd_util_unsupported = pd.util.hash_array, pd.util.hash_pandas_object
dataframe_unsupported = ['set_flags', 'convert_dtypes', 'bool', '__iter__',
    'items', 'iteritems', 'keys', 'iterrows', 'lookup', 'pop', 'xs', 'get',
    'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow', 'dot',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'lt', 'gt', 'le', 'ge', 'ne', 'eq', 'combine', 'combine_first',
    'subtract', 'divide', 'multiply', 'applymap', 'agg', 'aggregate',
    'transform', 'expanding', 'ewm', 'all', 'any', 'clip', 'corrwith',
    'cummax', 'cummin', 'eval', 'kurt', 'kurtosis', 'mad', 'mode', 'round',
    'sem', 'skew', 'value_counts', 'add_prefix', 'add_suffix', 'align',
    'at_time', 'between_time', 'equals', 'reindex', 'reindex_like',
    'rename_axis', 'set_axis', 'truncate', 'backfill', 'bfill', 'ffill',
    'interpolate', 'pad', 'droplevel', 'reorder_levels', 'nlargest',
    'nsmallest', 'swaplevel', 'stack', 'unstack', 'swapaxes', 'squeeze',
    'to_xarray', 'T', 'transpose', 'compare', 'update', 'asfreq', 'asof',
    'slice_shift', 'tshift', 'first_valid_index', 'last_valid_index',
    'resample', 'to_period', 'to_timestamp', 'tz_convert', 'tz_localize',
    'boxplot', 'hist', 'from_dict', 'from_records', 'to_pickle', 'to_hdf',
    'to_dict', 'to_excel', 'to_html', 'to_feather', 'to_latex', 'to_stata',
    'to_gbq', 'to_records', 'to_clipboard', 'to_markdown', 'to_xml']
dataframe_unsupported_attrs = ['at', 'attrs', 'axes', 'flags', 'style',
    'sparse']


def _install_pd_unsupported(mod_name, pd_unsupported):
    for vjjdn__xldt in pd_unsupported:
        onptd__jdn = mod_name + '.' + vjjdn__xldt.__name__
        overload(vjjdn__xldt, no_unliteral=True)(create_unsupported_overload
            (onptd__jdn))


def _install_dataframe_unsupported():
    for tstno__ihpfi in dataframe_unsupported_attrs:
        bud__bui = 'DataFrame.' + tstno__ihpfi
        overload_attribute(DataFrameType, tstno__ihpfi)(
            create_unsupported_overload(bud__bui))
    for onptd__jdn in dataframe_unsupported:
        bud__bui = 'DataFrame.' + onptd__jdn + '()'
        overload_method(DataFrameType, onptd__jdn)(create_unsupported_overload
            (bud__bui))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
