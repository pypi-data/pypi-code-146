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
            tkkj__oql = f'{len(self.data)} columns of types {set(self.data)}'
            ecj__jwjr = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            blgqz__lgryp = str(hash(super().__str__()))
            return (
                f'dataframe({tkkj__oql}, {self.index}, {ecj__jwjr}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols}, key_hash={blgqz__lgryp})'
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
        return {pnbo__jwfxx: i for i, pnbo__jwfxx in enumerate(self.columns)}

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
            dus__zpc = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(fmsed__fojti.unify(typingctx, lpbje__opn) if 
                fmsed__fojti != lpbje__opn else fmsed__fojti for 
                fmsed__fojti, lpbje__opn in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if dus__zpc is not None and None not in data:
                return DataFrameType(data, dus__zpc, self.columns, dist,
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
        return all(fmsed__fojti.is_precise() for fmsed__fojti in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        wum__azqi = self.columns.index(col_name)
        vep__tmkuy = tuple(list(self.data[:wum__azqi]) + [new_type] + list(
            self.data[wum__azqi + 1:]))
        return DataFrameType(vep__tmkuy, self.index, self.columns, self.
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
        dcu__cosh = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            dcu__cosh.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, dcu__cosh)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        dcu__cosh = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, dcu__cosh)


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
        aglmp__sse = 'n',
        mjad__hot = {'n': 5}
        arjzh__vyz, lqb__ssy = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, aglmp__sse, mjad__hot)
        cpvbv__sreb = lqb__ssy[0]
        if not is_overload_int(cpvbv__sreb):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        xmr__vufh = df.copy()
        return xmr__vufh(*lqb__ssy).replace(pysig=arjzh__vyz)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        zeh__mnkh = (df,) + args
        aglmp__sse = 'df', 'method', 'min_periods'
        mjad__hot = {'method': 'pearson', 'min_periods': 1}
        fzx__gnped = 'method',
        arjzh__vyz, lqb__ssy = bodo.utils.typing.fold_typing_args(func_name,
            zeh__mnkh, kws, aglmp__sse, mjad__hot, fzx__gnped)
        jlers__kph = lqb__ssy[2]
        if not is_overload_int(jlers__kph):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        ltf__fpkiq = []
        mskj__oyn = []
        for pnbo__jwfxx, kyg__vvb in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(kyg__vvb.dtype):
                ltf__fpkiq.append(pnbo__jwfxx)
                mskj__oyn.append(types.Array(types.float64, 1, 'A'))
        if len(ltf__fpkiq) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        mskj__oyn = tuple(mskj__oyn)
        ltf__fpkiq = tuple(ltf__fpkiq)
        index_typ = bodo.utils.typing.type_col_to_index(ltf__fpkiq)
        xmr__vufh = DataFrameType(mskj__oyn, index_typ, ltf__fpkiq)
        return xmr__vufh(*lqb__ssy).replace(pysig=arjzh__vyz)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        pxp__wrqr = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        gdgan__vbv = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        fqirz__nzkix = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        sdsa__pdtdo = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        jugn__jrpdl = dict(raw=gdgan__vbv, result_type=fqirz__nzkix)
        lwwo__ara = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', jugn__jrpdl, lwwo__ara,
            package_name='pandas', module_name='DataFrame')
        yrqpv__zmamv = True
        if types.unliteral(pxp__wrqr) == types.unicode_type:
            if not is_overload_constant_str(pxp__wrqr):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            yrqpv__zmamv = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        fxw__grrq = get_overload_const_int(axis)
        if yrqpv__zmamv and fxw__grrq != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif fxw__grrq not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        rfaf__mhlzm = []
        for arr_typ in df.data:
            ksig__zfd = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            enxc__jdop = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(ksig__zfd), types.int64), {}
                ).return_type
            rfaf__mhlzm.append(enxc__jdop)
        uhqr__emgsh = types.none
        qxd__frrqd = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(pnbo__jwfxx) for pnbo__jwfxx in df.columns)
            ), None)
        ehbub__bvlg = types.BaseTuple.from_types(rfaf__mhlzm)
        gnt__qefm = types.Tuple([types.bool_] * len(ehbub__bvlg))
        kqaa__net = bodo.NullableTupleType(ehbub__bvlg, gnt__qefm)
        gsjhz__yqki = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if gsjhz__yqki == types.NPDatetime('ns'):
            gsjhz__yqki = bodo.pd_timestamp_tz_naive_type
        if gsjhz__yqki == types.NPTimedelta('ns'):
            gsjhz__yqki = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(ehbub__bvlg):
            cqb__izor = HeterogeneousSeriesType(kqaa__net, qxd__frrqd,
                gsjhz__yqki)
        else:
            cqb__izor = SeriesType(ehbub__bvlg.dtype, kqaa__net, qxd__frrqd,
                gsjhz__yqki)
        ddp__taj = cqb__izor,
        if sdsa__pdtdo is not None:
            ddp__taj += tuple(sdsa__pdtdo.types)
        try:
            if not yrqpv__zmamv:
                nxz__zgsmj = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(pxp__wrqr), self.context,
                    'DataFrame.apply', axis if fxw__grrq == 1 else None)
            else:
                nxz__zgsmj = get_const_func_output_type(pxp__wrqr, ddp__taj,
                    kws, self.context, numba.core.registry.cpu_target.
                    target_context)
        except Exception as oztkh__rqfx:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                oztkh__rqfx))
        if yrqpv__zmamv:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(nxz__zgsmj, (SeriesType, HeterogeneousSeriesType)
                ) and nxz__zgsmj.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(nxz__zgsmj, HeterogeneousSeriesType):
                puk__atof, kodv__frwh = nxz__zgsmj.const_info
                if isinstance(nxz__zgsmj.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    xuok__whus = nxz__zgsmj.data.tuple_typ.types
                elif isinstance(nxz__zgsmj.data, types.Tuple):
                    xuok__whus = nxz__zgsmj.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                tbn__aqx = tuple(to_nullable_type(dtype_to_array_type(
                    iatm__pdlpy)) for iatm__pdlpy in xuok__whus)
                vjzwi__kclv = DataFrameType(tbn__aqx, df.index, kodv__frwh)
            elif isinstance(nxz__zgsmj, SeriesType):
                chnb__mzysu, kodv__frwh = nxz__zgsmj.const_info
                tbn__aqx = tuple(to_nullable_type(dtype_to_array_type(
                    nxz__zgsmj.dtype)) for puk__atof in range(chnb__mzysu))
                vjzwi__kclv = DataFrameType(tbn__aqx, df.index, kodv__frwh)
            else:
                zbxt__jlk = get_udf_out_arr_type(nxz__zgsmj)
                vjzwi__kclv = SeriesType(zbxt__jlk.dtype, zbxt__jlk, df.
                    index, None)
        else:
            vjzwi__kclv = nxz__zgsmj
        xeg__etq = ', '.join("{} = ''".format(fmsed__fojti) for
            fmsed__fojti in kws.keys())
        work__dgjdz = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {xeg__etq}):
"""
        work__dgjdz += '    pass\n'
        poti__lbr = {}
        exec(work__dgjdz, {}, poti__lbr)
        rgpwr__rha = poti__lbr['apply_stub']
        arjzh__vyz = numba.core.utils.pysignature(rgpwr__rha)
        qeerj__wbegr = (pxp__wrqr, axis, gdgan__vbv, fqirz__nzkix, sdsa__pdtdo
            ) + tuple(kws.values())
        return signature(vjzwi__kclv, *qeerj__wbegr).replace(pysig=arjzh__vyz)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        aglmp__sse = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        mjad__hot = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        fzx__gnped = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        arjzh__vyz, lqb__ssy = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, aglmp__sse, mjad__hot, fzx__gnped)
        mjk__jltg = lqb__ssy[2]
        if not is_overload_constant_str(mjk__jltg):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        lhry__mbryr = lqb__ssy[0]
        if not is_overload_none(lhry__mbryr) and not (is_overload_int(
            lhry__mbryr) or is_overload_constant_str(lhry__mbryr)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(lhry__mbryr):
            ugs__fcr = get_overload_const_str(lhry__mbryr)
            if ugs__fcr not in df.columns:
                raise BodoError(f'{func_name}: {ugs__fcr} column not found.')
        elif is_overload_int(lhry__mbryr):
            rred__sxlel = get_overload_const_int(lhry__mbryr)
            if rred__sxlel > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {rred__sxlel} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            lhry__mbryr = df.columns[lhry__mbryr]
        iahx__vgnj = lqb__ssy[1]
        if not is_overload_none(iahx__vgnj) and not (is_overload_int(
            iahx__vgnj) or is_overload_constant_str(iahx__vgnj)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(iahx__vgnj):
            wyij__mun = get_overload_const_str(iahx__vgnj)
            if wyij__mun not in df.columns:
                raise BodoError(f'{func_name}: {wyij__mun} column not found.')
        elif is_overload_int(iahx__vgnj):
            forjr__ecx = get_overload_const_int(iahx__vgnj)
            if forjr__ecx > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {forjr__ecx} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            iahx__vgnj = df.columns[iahx__vgnj]
        iiy__som = lqb__ssy[3]
        if not is_overload_none(iiy__som) and not is_tuple_like_type(iiy__som):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        bilv__piikd = lqb__ssy[10]
        if not is_overload_none(bilv__piikd) and not is_overload_constant_str(
            bilv__piikd):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        gmyw__kqy = lqb__ssy[12]
        if not is_overload_bool(gmyw__kqy):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        dfun__edp = lqb__ssy[17]
        if not is_overload_none(dfun__edp) and not is_tuple_like_type(dfun__edp
            ):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        fyu__ikry = lqb__ssy[18]
        if not is_overload_none(fyu__ikry) and not is_tuple_like_type(fyu__ikry
            ):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        ztk__azm = lqb__ssy[22]
        if not is_overload_none(ztk__azm) and not is_overload_int(ztk__azm):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        qin__yve = lqb__ssy[29]
        if not is_overload_none(qin__yve) and not is_overload_constant_str(
            qin__yve):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        uwd__ynbuq = lqb__ssy[30]
        if not is_overload_none(uwd__ynbuq) and not is_overload_constant_str(
            uwd__ynbuq):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        sjxwr__prj = types.List(types.mpl_line_2d_type)
        mjk__jltg = get_overload_const_str(mjk__jltg)
        if mjk__jltg == 'scatter':
            if is_overload_none(lhry__mbryr) and is_overload_none(iahx__vgnj):
                raise BodoError(
                    f'{func_name}: {mjk__jltg} requires an x and y column.')
            elif is_overload_none(lhry__mbryr):
                raise BodoError(
                    f'{func_name}: {mjk__jltg} x column is missing.')
            elif is_overload_none(iahx__vgnj):
                raise BodoError(
                    f'{func_name}: {mjk__jltg} y column is missing.')
            sjxwr__prj = types.mpl_path_collection_type
        elif mjk__jltg != 'line':
            raise BodoError(f'{func_name}: {mjk__jltg} plot is not supported.')
        return signature(sjxwr__prj, *lqb__ssy).replace(pysig=arjzh__vyz)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            eehmf__vpou = df.columns.index(attr)
            arr_typ = df.data[eehmf__vpou]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            vodi__obep = []
            vep__tmkuy = []
            canon__avzd = False
            for i, emqwy__vfuu in enumerate(df.columns):
                if emqwy__vfuu[0] != attr:
                    continue
                canon__avzd = True
                vodi__obep.append(emqwy__vfuu[1] if len(emqwy__vfuu) == 2 else
                    emqwy__vfuu[1:])
                vep__tmkuy.append(df.data[i])
            if canon__avzd:
                return DataFrameType(tuple(vep__tmkuy), df.index, tuple(
                    vodi__obep))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        muw__zhd = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(muw__zhd)
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
        bnif__tcvs = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], bnif__tcvs)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    tfghy__pfub = builder.module
    mdj__bkf = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    mjlu__gqex = cgutils.get_or_insert_function(tfghy__pfub, mdj__bkf, name
        ='.dtor.df.{}'.format(df_type))
    if not mjlu__gqex.is_declaration:
        return mjlu__gqex
    mjlu__gqex.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(mjlu__gqex.append_basic_block())
    orua__mekb = mjlu__gqex.args[0]
    tdli__bpunc = context.get_value_type(payload_type).as_pointer()
    etu__scc = builder.bitcast(orua__mekb, tdli__bpunc)
    payload = context.make_helper(builder, payload_type, ref=etu__scc)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        hklx__nxlv = context.get_python_api(builder)
        qsr__ltjb = hklx__nxlv.gil_ensure()
        hklx__nxlv.decref(payload.parent)
        hklx__nxlv.gil_release(qsr__ltjb)
    builder.ret_void()
    return mjlu__gqex


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    jfvri__npqv = cgutils.create_struct_proxy(payload_type)(context, builder)
    jfvri__npqv.data = data_tup
    jfvri__npqv.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        jfvri__npqv.columns = colnames
    gil__xquze = context.get_value_type(payload_type)
    ifrsg__pmzt = context.get_abi_sizeof(gil__xquze)
    zvqo__ffkbu = define_df_dtor(context, builder, df_type, payload_type)
    jdds__rzvic = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ifrsg__pmzt), zvqo__ffkbu)
    kbr__yjjh = context.nrt.meminfo_data(builder, jdds__rzvic)
    hzd__cqntk = builder.bitcast(kbr__yjjh, gil__xquze.as_pointer())
    fvaqc__skol = cgutils.create_struct_proxy(df_type)(context, builder)
    fvaqc__skol.meminfo = jdds__rzvic
    if parent is None:
        fvaqc__skol.parent = cgutils.get_null_value(fvaqc__skol.parent.type)
    else:
        fvaqc__skol.parent = parent
        jfvri__npqv.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            hklx__nxlv = context.get_python_api(builder)
            qsr__ltjb = hklx__nxlv.gil_ensure()
            hklx__nxlv.incref(parent)
            hklx__nxlv.gil_release(qsr__ltjb)
    builder.store(jfvri__npqv._getvalue(), hzd__cqntk)
    return fvaqc__skol._getvalue()


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
        ypp__terf = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        ypp__terf = [iatm__pdlpy for iatm__pdlpy in data_typ.dtype.arr_types]
    aoz__lioy = DataFrameType(tuple(ypp__terf + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        dsun__qhf = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return dsun__qhf
    sig = signature(aoz__lioy, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    chnb__mzysu = len(data_tup_typ.types)
    if chnb__mzysu == 0:
        column_names = ()
    tsagu__oupt = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(tsagu__oupt, ColNamesMetaType) and isinstance(tsagu__oupt
        .meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = tsagu__oupt.meta
    if chnb__mzysu == 1 and isinstance(data_tup_typ.types[0], TableType):
        chnb__mzysu = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == chnb__mzysu, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    ofn__hwunz = data_tup_typ.types
    if chnb__mzysu != 0 and isinstance(data_tup_typ.types[0], TableType):
        ofn__hwunz = data_tup_typ.types[0].arr_types
        is_table_format = True
    aoz__lioy = DataFrameType(ofn__hwunz, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            grfm__rxhm = cgutils.create_struct_proxy(aoz__lioy.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = grfm__rxhm.parent
        dsun__qhf = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return dsun__qhf
    sig = signature(aoz__lioy, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        fvaqc__skol = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, fvaqc__skol.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        jfvri__npqv = get_dataframe_payload(context, builder, df_typ, args[0])
        dfebg__gcic = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[dfebg__gcic]
        if df_typ.is_table_format:
            grfm__rxhm = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(jfvri__npqv.data, 0))
            odv__hvnz = df_typ.table_type.type_to_blk[arr_typ]
            tunhx__lbi = getattr(grfm__rxhm, f'block_{odv__hvnz}')
            cxyey__peb = ListInstance(context, builder, types.List(arr_typ),
                tunhx__lbi)
            btu__pyzp = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[dfebg__gcic])
            bnif__tcvs = cxyey__peb.getitem(btu__pyzp)
        else:
            bnif__tcvs = builder.extract_value(jfvri__npqv.data, dfebg__gcic)
        lmpl__cmadu = cgutils.alloca_once_value(builder, bnif__tcvs)
        wxm__gljbg = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, lmpl__cmadu, wxm__gljbg)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    jdds__rzvic = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, jdds__rzvic)
    tdli__bpunc = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, tdli__bpunc)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    aoz__lioy = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        aoz__lioy = types.Tuple([TableType(df_typ.data)])
    sig = signature(aoz__lioy, df_typ)

    def codegen(context, builder, signature, args):
        jfvri__npqv = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            jfvri__npqv.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        jfvri__npqv = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index,
            jfvri__npqv.index)
    aoz__lioy = df_typ.index
    sig = signature(aoz__lioy, df_typ)
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
        xmr__vufh = df.data[i]
        return xmr__vufh(*args)


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
        jfvri__npqv = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(jfvri__npqv.data, 0))
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
    gid__fiawc = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{gid__fiawc})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        xmr__vufh = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return xmr__vufh(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        jfvri__npqv = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, jfvri__npqv.columns)
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
    ehbub__bvlg = self.typemap[data_tup.name]
    if any(is_tuple_like_type(iatm__pdlpy) for iatm__pdlpy in ehbub__bvlg.types
        ):
        return None
    if equiv_set.has_shape(data_tup):
        tyzt__sjsux = equiv_set.get_shape(data_tup)
        if len(tyzt__sjsux) > 1:
            equiv_set.insert_equiv(*tyzt__sjsux)
        if len(tyzt__sjsux) > 0:
            qxd__frrqd = self.typemap[index.name]
            if not isinstance(qxd__frrqd, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(tyzt__sjsux[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(tyzt__sjsux[0], len(
                tyzt__sjsux)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    asjm__oskf = args[0]
    data_types = self.typemap[asjm__oskf.name].data
    if any(is_tuple_like_type(iatm__pdlpy) for iatm__pdlpy in data_types):
        return None
    if equiv_set.has_shape(asjm__oskf):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            asjm__oskf)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    asjm__oskf = args[0]
    qxd__frrqd = self.typemap[asjm__oskf.name].index
    if isinstance(qxd__frrqd, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(asjm__oskf):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            asjm__oskf)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    asjm__oskf = args[0]
    if equiv_set.has_shape(asjm__oskf):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            asjm__oskf), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    asjm__oskf = args[0]
    if equiv_set.has_shape(asjm__oskf):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            asjm__oskf)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    dfebg__gcic = get_overload_const_int(c_ind_typ)
    if df_typ.data[dfebg__gcic] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        jzacc__tnel, puk__atof, hjoi__gcjq = args
        jfvri__npqv = get_dataframe_payload(context, builder, df_typ,
            jzacc__tnel)
        if df_typ.is_table_format:
            grfm__rxhm = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(jfvri__npqv.data, 0))
            odv__hvnz = df_typ.table_type.type_to_blk[arr_typ]
            tunhx__lbi = getattr(grfm__rxhm, f'block_{odv__hvnz}')
            cxyey__peb = ListInstance(context, builder, types.List(arr_typ),
                tunhx__lbi)
            btu__pyzp = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[dfebg__gcic])
            cxyey__peb.setitem(btu__pyzp, hjoi__gcjq, True)
        else:
            bnif__tcvs = builder.extract_value(jfvri__npqv.data, dfebg__gcic)
            context.nrt.decref(builder, df_typ.data[dfebg__gcic], bnif__tcvs)
            jfvri__npqv.data = builder.insert_value(jfvri__npqv.data,
                hjoi__gcjq, dfebg__gcic)
            context.nrt.incref(builder, arr_typ, hjoi__gcjq)
        fvaqc__skol = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=jzacc__tnel)
        payload_type = DataFramePayloadType(df_typ)
        etu__scc = context.nrt.meminfo_data(builder, fvaqc__skol.meminfo)
        tdli__bpunc = context.get_value_type(payload_type).as_pointer()
        etu__scc = builder.bitcast(etu__scc, tdli__bpunc)
        builder.store(jfvri__npqv._getvalue(), etu__scc)
        return impl_ret_borrowed(context, builder, df_typ, jzacc__tnel)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        cjnzu__oxd = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        hzfh__lqyam = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=cjnzu__oxd)
        dnmo__nlm = get_dataframe_payload(context, builder, df_typ, cjnzu__oxd)
        fvaqc__skol = construct_dataframe(context, builder, signature.
            return_type, dnmo__nlm.data, index_val, hzfh__lqyam.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), dnmo__nlm.data)
        return fvaqc__skol
    aoz__lioy = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(aoz__lioy, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    chnb__mzysu = len(df_type.columns)
    azzc__fya = chnb__mzysu
    dtf__uhdhm = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    wvh__wzmx = col_name not in df_type.columns
    dfebg__gcic = chnb__mzysu
    if wvh__wzmx:
        dtf__uhdhm += arr_type,
        column_names += col_name,
        azzc__fya += 1
    else:
        dfebg__gcic = df_type.columns.index(col_name)
        dtf__uhdhm = tuple(arr_type if i == dfebg__gcic else dtf__uhdhm[i] for
            i in range(chnb__mzysu))

    def codegen(context, builder, signature, args):
        jzacc__tnel, puk__atof, hjoi__gcjq = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, jzacc__tnel)
        wwikr__btu = cgutils.create_struct_proxy(df_type)(context, builder,
            value=jzacc__tnel)
        if df_type.is_table_format:
            rgp__jccgt = df_type.table_type
            yifn__zggd = builder.extract_value(in_dataframe_payload.data, 0)
            jhe__tftj = TableType(dtf__uhdhm)
            davp__aft = set_table_data_codegen(context, builder, rgp__jccgt,
                yifn__zggd, jhe__tftj, arr_type, hjoi__gcjq, dfebg__gcic,
                wvh__wzmx)
            data_tup = context.make_tuple(builder, types.Tuple([jhe__tftj]),
                [davp__aft])
        else:
            ofn__hwunz = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != dfebg__gcic else hjoi__gcjq) for i in range(
                chnb__mzysu)]
            if wvh__wzmx:
                ofn__hwunz.append(hjoi__gcjq)
            for asjm__oskf, lgpx__ggg in zip(ofn__hwunz, dtf__uhdhm):
                context.nrt.incref(builder, lgpx__ggg, asjm__oskf)
            data_tup = context.make_tuple(builder, types.Tuple(dtf__uhdhm),
                ofn__hwunz)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        xjpkd__hbty = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, wwikr__btu.parent, None)
        if not wvh__wzmx and arr_type == df_type.data[dfebg__gcic]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            etu__scc = context.nrt.meminfo_data(builder, wwikr__btu.meminfo)
            tdli__bpunc = context.get_value_type(payload_type).as_pointer()
            etu__scc = builder.bitcast(etu__scc, tdli__bpunc)
            qcbxl__rxpuz = get_dataframe_payload(context, builder, df_type,
                xjpkd__hbty)
            builder.store(qcbxl__rxpuz._getvalue(), etu__scc)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, jhe__tftj, builder.
                    extract_value(data_tup, 0))
            else:
                for asjm__oskf, lgpx__ggg in zip(ofn__hwunz, dtf__uhdhm):
                    context.nrt.incref(builder, lgpx__ggg, asjm__oskf)
        has_parent = cgutils.is_not_null(builder, wwikr__btu.parent)
        with builder.if_then(has_parent):
            hklx__nxlv = context.get_python_api(builder)
            qsr__ltjb = hklx__nxlv.gil_ensure()
            oynz__grjm = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, hjoi__gcjq)
            pnbo__jwfxx = numba.core.pythonapi._BoxContext(context, builder,
                hklx__nxlv, oynz__grjm)
            wugjl__mvj = pnbo__jwfxx.pyapi.from_native_value(arr_type,
                hjoi__gcjq, pnbo__jwfxx.env_manager)
            if isinstance(col_name, str):
                oaroz__cnm = context.insert_const_string(builder.module,
                    col_name)
                sokm__qtpr = hklx__nxlv.string_from_string(oaroz__cnm)
            else:
                assert isinstance(col_name, int)
                sokm__qtpr = hklx__nxlv.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            hklx__nxlv.object_setitem(wwikr__btu.parent, sokm__qtpr, wugjl__mvj
                )
            hklx__nxlv.decref(wugjl__mvj)
            hklx__nxlv.decref(sokm__qtpr)
            hklx__nxlv.gil_release(qsr__ltjb)
        return xjpkd__hbty
    aoz__lioy = DataFrameType(dtf__uhdhm, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(aoz__lioy, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    chnb__mzysu = len(pyval.columns)
    ofn__hwunz = []
    for i in range(chnb__mzysu):
        zynzr__ofxp = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            wugjl__mvj = zynzr__ofxp.array
        else:
            wugjl__mvj = zynzr__ofxp.values
        ofn__hwunz.append(wugjl__mvj)
    ofn__hwunz = tuple(ofn__hwunz)
    if df_type.is_table_format:
        grfm__rxhm = context.get_constant_generic(builder, df_type.
            table_type, Table(ofn__hwunz))
        data_tup = lir.Constant.literal_struct([grfm__rxhm])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], emqwy__vfuu) for
            i, emqwy__vfuu in enumerate(ofn__hwunz)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    bbnc__cumr = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, bbnc__cumr])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    brs__xixn = context.get_constant(types.int64, -1)
    ldn__tnr = context.get_constant_null(types.voidptr)
    jdds__rzvic = lir.Constant.literal_struct([brs__xixn, ldn__tnr,
        ldn__tnr, payload, brs__xixn])
    jdds__rzvic = cgutils.global_constant(builder, '.const.meminfo',
        jdds__rzvic).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([jdds__rzvic, bbnc__cumr])


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
        dus__zpc = context.cast(builder, in_dataframe_payload.index, fromty
            .index, toty.index)
    else:
        dus__zpc = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, dus__zpc)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        vep__tmkuy = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                vep__tmkuy)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), vep__tmkuy)
    elif not fromty.is_table_format and toty.is_table_format:
        vep__tmkuy = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        vep__tmkuy = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        vep__tmkuy = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        vep__tmkuy = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, vep__tmkuy, dus__zpc,
        in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    ntj__kzox = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        nyi__qucfu = get_index_data_arr_types(toty.index)[0]
        hvvee__xul = bodo.utils.transform.get_type_alloc_counts(nyi__qucfu) - 1
        evmab__jrxyd = ', '.join('0' for puk__atof in range(hvvee__xul))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(evmab__jrxyd, ', ' if hvvee__xul == 1 else ''))
        ntj__kzox['index_arr_type'] = nyi__qucfu
    fjejc__sevge = []
    for i, arr_typ in enumerate(toty.data):
        hvvee__xul = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        evmab__jrxyd = ', '.join('0' for puk__atof in range(hvvee__xul))
        yst__yxbxd = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, evmab__jrxyd, ', ' if hvvee__xul == 1 else ''))
        fjejc__sevge.append(yst__yxbxd)
        ntj__kzox[f'arr_type{i}'] = arr_typ
    fjejc__sevge = ', '.join(fjejc__sevge)
    work__dgjdz = 'def impl():\n'
    ovvt__sfjbf = bodo.hiframes.dataframe_impl._gen_init_df(work__dgjdz,
        toty.columns, fjejc__sevge, index, ntj__kzox)
    df = context.compile_internal(builder, ovvt__sfjbf, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    ydkb__nszam = toty.table_type
    grfm__rxhm = cgutils.create_struct_proxy(ydkb__nszam)(context, builder)
    grfm__rxhm.parent = in_dataframe_payload.parent
    for iatm__pdlpy, odv__hvnz in ydkb__nszam.type_to_blk.items():
        dtt__jxm = context.get_constant(types.int64, len(ydkb__nszam.
            block_to_arr_ind[odv__hvnz]))
        puk__atof, ogd__jfew = ListInstance.allocate_ex(context, builder,
            types.List(iatm__pdlpy), dtt__jxm)
        ogd__jfew.size = dtt__jxm
        setattr(grfm__rxhm, f'block_{odv__hvnz}', ogd__jfew.value)
    for i, iatm__pdlpy in enumerate(fromty.data):
        pmd__mmii = toty.data[i]
        if iatm__pdlpy != pmd__mmii:
            cyun__tsp = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*cyun__tsp)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        bnif__tcvs = builder.extract_value(in_dataframe_payload.data, i)
        if iatm__pdlpy != pmd__mmii:
            ixib__zgftc = context.cast(builder, bnif__tcvs, iatm__pdlpy,
                pmd__mmii)
            uxsli__oonrt = False
        else:
            ixib__zgftc = bnif__tcvs
            uxsli__oonrt = True
        odv__hvnz = ydkb__nszam.type_to_blk[iatm__pdlpy]
        tunhx__lbi = getattr(grfm__rxhm, f'block_{odv__hvnz}')
        cxyey__peb = ListInstance(context, builder, types.List(iatm__pdlpy),
            tunhx__lbi)
        btu__pyzp = context.get_constant(types.int64, ydkb__nszam.
            block_offsets[i])
        cxyey__peb.setitem(btu__pyzp, ixib__zgftc, uxsli__oonrt)
    data_tup = context.make_tuple(builder, types.Tuple([ydkb__nszam]), [
        grfm__rxhm._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    ofn__hwunz = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            cyun__tsp = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*cyun__tsp)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            bnif__tcvs = builder.extract_value(in_dataframe_payload.data, i)
            ixib__zgftc = context.cast(builder, bnif__tcvs, fromty.data[i],
                toty.data[i])
            uxsli__oonrt = False
        else:
            ixib__zgftc = builder.extract_value(in_dataframe_payload.data, i)
            uxsli__oonrt = True
        if uxsli__oonrt:
            context.nrt.incref(builder, toty.data[i], ixib__zgftc)
        ofn__hwunz.append(ixib__zgftc)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), ofn__hwunz)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    rgp__jccgt = fromty.table_type
    yifn__zggd = cgutils.create_struct_proxy(rgp__jccgt)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    jhe__tftj = toty.table_type
    davp__aft = cgutils.create_struct_proxy(jhe__tftj)(context, builder)
    davp__aft.parent = in_dataframe_payload.parent
    for iatm__pdlpy, odv__hvnz in jhe__tftj.type_to_blk.items():
        dtt__jxm = context.get_constant(types.int64, len(jhe__tftj.
            block_to_arr_ind[odv__hvnz]))
        puk__atof, ogd__jfew = ListInstance.allocate_ex(context, builder,
            types.List(iatm__pdlpy), dtt__jxm)
        ogd__jfew.size = dtt__jxm
        setattr(davp__aft, f'block_{odv__hvnz}', ogd__jfew.value)
    for i in range(len(fromty.data)):
        mrc__lly = fromty.data[i]
        pmd__mmii = toty.data[i]
        if mrc__lly != pmd__mmii:
            cyun__tsp = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*cyun__tsp)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        rpnpd__miib = rgp__jccgt.type_to_blk[mrc__lly]
        hol__opxau = getattr(yifn__zggd, f'block_{rpnpd__miib}')
        zeye__zsj = ListInstance(context, builder, types.List(mrc__lly),
            hol__opxau)
        tnl__mbvt = context.get_constant(types.int64, rgp__jccgt.
            block_offsets[i])
        bnif__tcvs = zeye__zsj.getitem(tnl__mbvt)
        if mrc__lly != pmd__mmii:
            ixib__zgftc = context.cast(builder, bnif__tcvs, mrc__lly, pmd__mmii
                )
            uxsli__oonrt = False
        else:
            ixib__zgftc = bnif__tcvs
            uxsli__oonrt = True
        qshju__vaamc = jhe__tftj.type_to_blk[iatm__pdlpy]
        ogd__jfew = getattr(davp__aft, f'block_{qshju__vaamc}')
        aya__thore = ListInstance(context, builder, types.List(pmd__mmii),
            ogd__jfew)
        heg__phpyp = context.get_constant(types.int64, jhe__tftj.
            block_offsets[i])
        aya__thore.setitem(heg__phpyp, ixib__zgftc, uxsli__oonrt)
    data_tup = context.make_tuple(builder, types.Tuple([jhe__tftj]), [
        davp__aft._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    ydkb__nszam = fromty.table_type
    grfm__rxhm = cgutils.create_struct_proxy(ydkb__nszam)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    ofn__hwunz = []
    for i, iatm__pdlpy in enumerate(toty.data):
        mrc__lly = fromty.data[i]
        if iatm__pdlpy != mrc__lly:
            cyun__tsp = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*cyun__tsp)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        odv__hvnz = ydkb__nszam.type_to_blk[mrc__lly]
        tunhx__lbi = getattr(grfm__rxhm, f'block_{odv__hvnz}')
        cxyey__peb = ListInstance(context, builder, types.List(mrc__lly),
            tunhx__lbi)
        btu__pyzp = context.get_constant(types.int64, ydkb__nszam.
            block_offsets[i])
        bnif__tcvs = cxyey__peb.getitem(btu__pyzp)
        if iatm__pdlpy != mrc__lly:
            ixib__zgftc = context.cast(builder, bnif__tcvs, mrc__lly,
                iatm__pdlpy)
        else:
            ixib__zgftc = bnif__tcvs
            context.nrt.incref(builder, iatm__pdlpy, ixib__zgftc)
        ofn__hwunz.append(ixib__zgftc)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), ofn__hwunz)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    qfixy__vsvz, fjejc__sevge, index_arg = _get_df_args(data, index,
        columns, dtype, copy)
    sbpf__rquy = ColNamesMetaType(tuple(qfixy__vsvz))
    work__dgjdz = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    work__dgjdz += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(fjejc__sevge, index_arg))
    poti__lbr = {}
    exec(work__dgjdz, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': sbpf__rquy}, poti__lbr)
    dsz__xhh = poti__lbr['_init_df']
    return dsz__xhh


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    aoz__lioy = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ
        .index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(aoz__lioy, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    aoz__lioy = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ
        .index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(aoz__lioy, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    kig__gme = ''
    if not is_overload_none(dtype):
        kig__gme = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        chnb__mzysu = (len(data.types) - 1) // 2
        txhts__tidb = [iatm__pdlpy.literal_value for iatm__pdlpy in data.
            types[1:chnb__mzysu + 1]]
        data_val_types = dict(zip(txhts__tidb, data.types[chnb__mzysu + 1:]))
        ofn__hwunz = ['data[{}]'.format(i) for i in range(chnb__mzysu + 1, 
            2 * chnb__mzysu + 1)]
        data_dict = dict(zip(txhts__tidb, ofn__hwunz))
        if is_overload_none(index):
            for i, iatm__pdlpy in enumerate(data.types[chnb__mzysu + 1:]):
                if isinstance(iatm__pdlpy, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(chnb__mzysu + 1 + i))
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
        zyq__tmg = '.copy()' if copy else ''
        gbx__ucfzd = get_overload_const_list(columns)
        chnb__mzysu = len(gbx__ucfzd)
        data_val_types = {pnbo__jwfxx: data.copy(ndim=1) for pnbo__jwfxx in
            gbx__ucfzd}
        ofn__hwunz = ['data[:,{}]{}'.format(i, zyq__tmg) for i in range(
            chnb__mzysu)]
        data_dict = dict(zip(gbx__ucfzd, ofn__hwunz))
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
    fjejc__sevge = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[pnbo__jwfxx], df_len, kig__gme) for pnbo__jwfxx in
        col_names))
    if len(col_names) == 0:
        fjejc__sevge = '()'
    return col_names, fjejc__sevge, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for pnbo__jwfxx in col_names:
        if pnbo__jwfxx in data_dict and is_iterable_type(data_val_types[
            pnbo__jwfxx]):
            df_len = 'len({})'.format(data_dict[pnbo__jwfxx])
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
    if all(pnbo__jwfxx in data_dict for pnbo__jwfxx in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    wmss__crjp = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for pnbo__jwfxx in col_names:
        if pnbo__jwfxx not in data_dict:
            data_dict[pnbo__jwfxx] = wmss__crjp


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
            iatm__pdlpy = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df
                )
            return len(iatm__pdlpy)
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
        pkvlc__tyqab = idx.literal_value
        if isinstance(pkvlc__tyqab, int):
            xmr__vufh = tup.types[pkvlc__tyqab]
        elif isinstance(pkvlc__tyqab, slice):
            xmr__vufh = types.BaseTuple.from_types(tup.types[pkvlc__tyqab])
        return signature(xmr__vufh, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    napx__pgn, idx = sig.args
    idx = idx.literal_value
    tup, puk__atof = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(napx__pgn)
        if not 0 <= idx < len(napx__pgn):
            raise IndexError('cannot index at %d in %s' % (idx, napx__pgn))
        hjq__nxx = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        bwejp__mda = cgutils.unpack_tuple(builder, tup)[idx]
        hjq__nxx = context.make_tuple(builder, sig.return_type, bwejp__mda)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, hjq__nxx)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, xyoqm__efe, suffix_x,
            suffix_y, is_join, indicator, puk__atof, puk__atof) = args
        how = get_overload_const_str(xyoqm__efe)
        if how == 'cross':
            data = left_df.data + right_df.data
            columns = left_df.columns + right_df.columns
            mwxii__lfrzs = DataFrameType(data, RangeIndexType(types.none),
                columns, is_table_format=True)
            return signature(mwxii__lfrzs, *args)
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        dhgrk__xuix = {pnbo__jwfxx: i for i, pnbo__jwfxx in enumerate(left_on)}
        cqzjx__qumm = {pnbo__jwfxx: i for i, pnbo__jwfxx in enumerate(right_on)
            }
        kvlsj__alo = set(left_on) & set(right_on)
        try__olsdo = set(left_df.columns) & set(right_df.columns)
        drimt__dxlie = try__olsdo - kvlsj__alo
        hizd__afjy = '$_bodo_index_' in left_on
        yagx__vlo = '$_bodo_index_' in right_on
        yhw__hsra = how in {'left', 'outer'}
        trhi__rhazb = how in {'right', 'outer'}
        columns = []
        data = []
        if hizd__afjy or yagx__vlo:
            if hizd__afjy:
                zgqks__fjlq = bodo.utils.typing.get_index_data_arr_types(
                    left_df.index)[0]
            else:
                zgqks__fjlq = left_df.data[left_df.column_index[left_on[0]]]
            if yagx__vlo:
                zkg__aqpzo = bodo.utils.typing.get_index_data_arr_types(
                    right_df.index)[0]
            else:
                zkg__aqpzo = right_df.data[right_df.column_index[right_on[0]]]
        if hizd__afjy and not yagx__vlo and not is_join.literal_value:
            wly__dchz = right_on[0]
            if wly__dchz in left_df.column_index:
                columns.append(wly__dchz)
                if (zkg__aqpzo == bodo.dict_str_arr_type and zgqks__fjlq ==
                    bodo.string_array_type):
                    dlu__kxi = bodo.string_array_type
                else:
                    dlu__kxi = zkg__aqpzo
                data.append(dlu__kxi)
        if yagx__vlo and not hizd__afjy and not is_join.literal_value:
            vlf__uiwm = left_on[0]
            if vlf__uiwm in right_df.column_index:
                columns.append(vlf__uiwm)
                if (zgqks__fjlq == bodo.dict_str_arr_type and zkg__aqpzo ==
                    bodo.string_array_type):
                    dlu__kxi = bodo.string_array_type
                else:
                    dlu__kxi = zgqks__fjlq
                data.append(dlu__kxi)
        for mrc__lly, zynzr__ofxp in zip(left_df.data, left_df.columns):
            columns.append(str(zynzr__ofxp) + suffix_x.literal_value if 
                zynzr__ofxp in drimt__dxlie else zynzr__ofxp)
            if zynzr__ofxp in kvlsj__alo:
                if mrc__lly == bodo.dict_str_arr_type:
                    mrc__lly = right_df.data[right_df.column_index[zynzr__ofxp]
                        ]
                data.append(mrc__lly)
            else:
                if (mrc__lly == bodo.dict_str_arr_type and zynzr__ofxp in
                    dhgrk__xuix):
                    if yagx__vlo:
                        mrc__lly = zkg__aqpzo
                    else:
                        lve__uibyr = dhgrk__xuix[zynzr__ofxp]
                        pwvq__djyxl = right_on[lve__uibyr]
                        mrc__lly = right_df.data[right_df.column_index[
                            pwvq__djyxl]]
                if trhi__rhazb:
                    mrc__lly = to_nullable_type(mrc__lly)
                data.append(mrc__lly)
        for mrc__lly, zynzr__ofxp in zip(right_df.data, right_df.columns):
            if zynzr__ofxp not in kvlsj__alo:
                columns.append(str(zynzr__ofxp) + suffix_y.literal_value if
                    zynzr__ofxp in drimt__dxlie else zynzr__ofxp)
                if (mrc__lly == bodo.dict_str_arr_type and zynzr__ofxp in
                    cqzjx__qumm):
                    if hizd__afjy:
                        mrc__lly = zgqks__fjlq
                    else:
                        lve__uibyr = cqzjx__qumm[zynzr__ofxp]
                        iodq__mimxf = left_on[lve__uibyr]
                        mrc__lly = left_df.data[left_df.column_index[
                            iodq__mimxf]]
                if yhw__hsra:
                    mrc__lly = to_nullable_type(mrc__lly)
                data.append(mrc__lly)
        yby__lvxk = get_overload_const_bool(indicator)
        if yby__lvxk:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        arprt__xpz = False
        if hizd__afjy and yagx__vlo and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            arprt__xpz = True
        elif hizd__afjy and not yagx__vlo:
            index_typ = right_df.index
            arprt__xpz = True
        elif yagx__vlo and not hizd__afjy:
            index_typ = left_df.index
            arprt__xpz = True
        if arprt__xpz and isinstance(index_typ, bodo.hiframes.pd_index_ext.
            RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        mwxii__lfrzs = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(mwxii__lfrzs, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    fvaqc__skol = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return fvaqc__skol._getvalue()


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
    jugn__jrpdl = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    mjad__hot = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', jugn__jrpdl, mjad__hot,
        package_name='pandas', module_name='General')
    work__dgjdz = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        npqr__woloe = 0
        fjejc__sevge = []
        names = []
        for i, hqp__gcbiu in enumerate(objs.types):
            assert isinstance(hqp__gcbiu, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(hqp__gcbiu, 'pandas.concat()')
            if isinstance(hqp__gcbiu, SeriesType):
                names.append(str(npqr__woloe))
                npqr__woloe += 1
                fjejc__sevge.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(hqp__gcbiu.columns)
                for lif__ajram in range(len(hqp__gcbiu.data)):
                    fjejc__sevge.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, lif__ajram))
        return bodo.hiframes.dataframe_impl._gen_init_df(work__dgjdz, names,
            ', '.join(fjejc__sevge), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(iatm__pdlpy, DataFrameType) for iatm__pdlpy in
            objs.types)
        idx__uyqfb = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            idx__uyqfb.extend(df.columns)
        idx__uyqfb = list(dict.fromkeys(idx__uyqfb).keys())
        ypp__terf = {}
        for npqr__woloe, pnbo__jwfxx in enumerate(idx__uyqfb):
            for i, df in enumerate(objs.types):
                if pnbo__jwfxx in df.column_index:
                    ypp__terf[f'arr_typ{npqr__woloe}'] = df.data[df.
                        column_index[pnbo__jwfxx]]
                    break
        assert len(ypp__terf) == len(idx__uyqfb)
        mzui__roj = []
        for npqr__woloe, pnbo__jwfxx in enumerate(idx__uyqfb):
            args = []
            for i, df in enumerate(objs.types):
                if pnbo__jwfxx in df.column_index:
                    dfebg__gcic = df.column_index[pnbo__jwfxx]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, dfebg__gcic))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, npqr__woloe))
            work__dgjdz += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(npqr__woloe, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(work__dgjdz,
            idx__uyqfb, ', '.join('A{}'.format(i) for i in range(len(
            idx__uyqfb))), index, ypp__terf)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(iatm__pdlpy, SeriesType) for iatm__pdlpy in
            objs.types)
        work__dgjdz += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            work__dgjdz += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            work__dgjdz += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        work__dgjdz += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        poti__lbr = {}
        exec(work__dgjdz, {'bodo': bodo, 'np': np, 'numba': numba}, poti__lbr)
        return poti__lbr['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for npqr__woloe, pnbo__jwfxx in enumerate(df_type.columns):
            work__dgjdz += '  arrs{} = []\n'.format(npqr__woloe)
            work__dgjdz += '  for i in range(len(objs)):\n'
            work__dgjdz += '    df = objs[i]\n'
            work__dgjdz += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(npqr__woloe))
            work__dgjdz += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(npqr__woloe))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            work__dgjdz += '  arrs_index = []\n'
            work__dgjdz += '  for i in range(len(objs)):\n'
            work__dgjdz += '    df = objs[i]\n'
            work__dgjdz += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(work__dgjdz,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        work__dgjdz += '  arrs = []\n'
        work__dgjdz += '  for i in range(len(objs)):\n'
        work__dgjdz += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        work__dgjdz += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            work__dgjdz += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            work__dgjdz += '  arrs_index = []\n'
            work__dgjdz += '  for i in range(len(objs)):\n'
            work__dgjdz += '    S = objs[i]\n'
            work__dgjdz += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            work__dgjdz += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        work__dgjdz += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        poti__lbr = {}
        exec(work__dgjdz, {'bodo': bodo, 'np': np, 'numba': numba}, poti__lbr)
        return poti__lbr['impl']
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
        aoz__lioy = df.copy(index=index)
        return signature(aoz__lioy, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    rgbk__ecbh = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rgbk__ecbh._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    jugn__jrpdl = dict(index=index, name=name)
    mjad__hot = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', jugn__jrpdl, mjad__hot,
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
        ypp__terf = (types.Array(types.int64, 1, 'C'),) + df.data
        ita__xzwz = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(columns
            , ypp__terf)
        return signature(ita__xzwz, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    rgbk__ecbh = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rgbk__ecbh._getvalue()


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
    rgbk__ecbh = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rgbk__ecbh._getvalue()


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
    rgbk__ecbh = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rgbk__ecbh._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    mzai__nmdy = get_overload_const_bool(check_duplicates)
    aweq__pihs = not get_overload_const_bool(is_already_shuffled)
    jis__dnotp = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    muvp__cca = len(value_names) > 1
    yalb__pzuhk = None
    lqcq__xxdui = None
    ufroo__ssd = None
    ppzji__dayda = None
    saml__nklen = isinstance(values_tup, types.UniTuple)
    if saml__nklen:
        acjo__evd = [to_str_arr_if_dict_array(to_nullable_type(values_tup.
            dtype))]
    else:
        acjo__evd = [to_str_arr_if_dict_array(to_nullable_type(lgpx__ggg)) for
            lgpx__ggg in values_tup]
    work__dgjdz = 'def impl(\n'
    work__dgjdz += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    work__dgjdz += '):\n'
    work__dgjdz += (
        "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n")
    if aweq__pihs:
        work__dgjdz += '    if parallel:\n'
        work__dgjdz += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        arhcj__adg = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        work__dgjdz += f'        info_list = [{arhcj__adg}]\n'
        work__dgjdz += (
            '        cpp_table = arr_info_list_to_table(info_list)\n')
        work__dgjdz += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        jvkhk__rhxfd = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        vho__wovt = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        mkvsn__ejst = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        work__dgjdz += f'        index_tup = ({jvkhk__rhxfd},)\n'
        work__dgjdz += f'        columns_tup = ({vho__wovt},)\n'
        work__dgjdz += f'        values_tup = ({mkvsn__ejst},)\n'
        work__dgjdz += '        delete_table(cpp_table)\n'
        work__dgjdz += '        delete_table(out_cpp_table)\n'
        work__dgjdz += '        ev_shuffle.finalize()\n'
    work__dgjdz += '    columns_arr = columns_tup[0]\n'
    if saml__nklen:
        work__dgjdz += '    values_arrs = [arr for arr in values_tup]\n'
    work__dgjdz += """    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)
"""
    work__dgjdz += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    work__dgjdz += '        index_tup\n'
    work__dgjdz += '    )\n'
    work__dgjdz += '    n_rows = len(unique_index_arr_tup[0])\n'
    work__dgjdz += '    num_values_arrays = len(values_tup)\n'
    work__dgjdz += '    n_unique_pivots = len(pivot_values)\n'
    if saml__nklen:
        work__dgjdz += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        work__dgjdz += '    n_cols = n_unique_pivots\n'
    work__dgjdz += '    col_map = {}\n'
    work__dgjdz += '    for i in range(n_unique_pivots):\n'
    work__dgjdz += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    work__dgjdz += '            raise ValueError(\n'
    work__dgjdz += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    work__dgjdz += '            )\n'
    work__dgjdz += '        col_map[pivot_values[i]] = i\n'
    work__dgjdz += '    ev_unique.finalize()\n'
    work__dgjdz += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    ina__syn = False
    for i, qset__mpzz in enumerate(acjo__evd):
        if is_str_arr_type(qset__mpzz):
            ina__syn = True
            work__dgjdz += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            work__dgjdz += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if ina__syn:
        if mzai__nmdy:
            work__dgjdz += '    nbytes = (n_rows + 7) >> 3\n'
            work__dgjdz += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        work__dgjdz += '    for i in range(len(columns_arr)):\n'
        work__dgjdz += '        col_name = columns_arr[i]\n'
        work__dgjdz += '        pivot_idx = col_map[col_name]\n'
        work__dgjdz += '        row_idx = row_vector[i]\n'
        if mzai__nmdy:
            work__dgjdz += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            work__dgjdz += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            work__dgjdz += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            work__dgjdz += '        else:\n'
            work__dgjdz += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if saml__nklen:
            work__dgjdz += '        for j in range(num_values_arrays):\n'
            work__dgjdz += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            work__dgjdz += '            len_arr = len_arrs_0[col_idx]\n'
            work__dgjdz += '            values_arr = values_arrs[j]\n'
            work__dgjdz += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            work__dgjdz += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            work__dgjdz += '                len_arr[row_idx] = str_val_len\n'
            work__dgjdz += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, qset__mpzz in enumerate(acjo__evd):
                if is_str_arr_type(qset__mpzz):
                    work__dgjdz += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    work__dgjdz += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    work__dgjdz += f"""            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}
"""
                    work__dgjdz += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    work__dgjdz += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, qset__mpzz in enumerate(acjo__evd):
        if is_str_arr_type(qset__mpzz):
            work__dgjdz += f'    data_arrs_{i} = [\n'
            work__dgjdz += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            work__dgjdz += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            work__dgjdz += '        )\n'
            work__dgjdz += '        for i in range(n_cols)\n'
            work__dgjdz += '    ]\n'
            work__dgjdz += f'    if tracing.is_tracing():\n'
            work__dgjdz += '         for i in range(n_cols):\n'
            work__dgjdz += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            work__dgjdz += f'    data_arrs_{i} = [\n'
            work__dgjdz += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            work__dgjdz += '        for _ in range(n_cols)\n'
            work__dgjdz += '    ]\n'
    if not ina__syn and mzai__nmdy:
        work__dgjdz += '    nbytes = (n_rows + 7) >> 3\n'
        work__dgjdz += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    work__dgjdz += '    ev_alloc.finalize()\n'
    work__dgjdz += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    work__dgjdz += '    for i in range(len(columns_arr)):\n'
    work__dgjdz += '        col_name = columns_arr[i]\n'
    work__dgjdz += '        pivot_idx = col_map[col_name]\n'
    work__dgjdz += '        row_idx = row_vector[i]\n'
    if not ina__syn and mzai__nmdy:
        work__dgjdz += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        work__dgjdz += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        work__dgjdz += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        work__dgjdz += '        else:\n'
        work__dgjdz += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if saml__nklen:
        work__dgjdz += '        for j in range(num_values_arrays):\n'
        work__dgjdz += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        work__dgjdz += '            col_arr = data_arrs_0[col_idx]\n'
        work__dgjdz += '            values_arr = values_arrs[j]\n'
        work__dgjdz += """            bodo.libs.array_kernels.copy_array_element(col_arr, row_idx, values_arr, i)
"""
    else:
        for i, qset__mpzz in enumerate(acjo__evd):
            work__dgjdz += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            work__dgjdz += f"""        bodo.libs.array_kernels.copy_array_element(col_arr_{i}, row_idx, values_tup[{i}], i)
"""
    if len(index_names) == 1:
        work__dgjdz += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        yalb__pzuhk = index_names.meta[0]
    else:
        work__dgjdz += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        yalb__pzuhk = tuple(index_names.meta)
    work__dgjdz += f'    if tracing.is_tracing():\n'
    work__dgjdz += f'        index_nbytes = index.nbytes\n'
    work__dgjdz += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not jis__dnotp:
        ufroo__ssd = columns_name.meta[0]
        if muvp__cca:
            work__dgjdz += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            lqcq__xxdui = value_names.meta
            if all(isinstance(pnbo__jwfxx, str) for pnbo__jwfxx in lqcq__xxdui
                ):
                lqcq__xxdui = pd.array(lqcq__xxdui, 'string')
            elif all(isinstance(pnbo__jwfxx, int) for pnbo__jwfxx in
                lqcq__xxdui):
                lqcq__xxdui = np.array(lqcq__xxdui, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(lqcq__xxdui.dtype, pd.StringDtype):
                work__dgjdz += '    total_chars = 0\n'
                work__dgjdz += f'    for i in range({len(value_names)}):\n'
                work__dgjdz += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                work__dgjdz += '        total_chars += value_name_str_len\n'
                work__dgjdz += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                work__dgjdz += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                work__dgjdz += '    total_chars = 0\n'
                work__dgjdz += '    for i in range(len(pivot_values)):\n'
                work__dgjdz += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                work__dgjdz += '        total_chars += pivot_val_str_len\n'
                work__dgjdz += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                work__dgjdz += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            work__dgjdz += f'    for i in range({len(value_names)}):\n'
            work__dgjdz += '        for j in range(len(pivot_values)):\n'
            work__dgjdz += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            work__dgjdz += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            work__dgjdz += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            work__dgjdz += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    work__dgjdz += '    ev_fill.finalize()\n'
    ydkb__nszam = None
    if jis__dnotp:
        if muvp__cca:
            jqo__uepl = []
            for qgz__wtrwd in _constant_pivot_values.meta:
                for nll__cvy in value_names.meta:
                    jqo__uepl.append((qgz__wtrwd, nll__cvy))
            column_names = tuple(jqo__uepl)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        ppzji__dayda = ColNamesMetaType(column_names)
        nnt__jxek = []
        for lgpx__ggg in acjo__evd:
            nnt__jxek.extend([lgpx__ggg] * len(_constant_pivot_values))
        myz__pumx = tuple(nnt__jxek)
        ydkb__nszam = TableType(myz__pumx)
        work__dgjdz += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        work__dgjdz += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, lgpx__ggg in enumerate(acjo__evd):
            work__dgjdz += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {ydkb__nszam.type_to_blk[lgpx__ggg]})
"""
        work__dgjdz += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        work__dgjdz += '        (table,), index, columns_typ\n'
        work__dgjdz += '    )\n'
    else:
        bbaum__lde = ', '.join(f'data_arrs_{i}' for i in range(len(acjo__evd)))
        work__dgjdz += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({bbaum__lde},), n_rows)
"""
        work__dgjdz += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
            )
        work__dgjdz += '        (table,), index, column_index\n'
        work__dgjdz += '    )\n'
    work__dgjdz += '    ev.finalize()\n'
    work__dgjdz += '    return result\n'
    poti__lbr = {}
    tbxk__flr = {f'data_arr_typ_{i}': qset__mpzz for i, qset__mpzz in
        enumerate(acjo__evd)}
    tlnd__kbgy = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        ydkb__nszam, 'columns_typ': ppzji__dayda, 'index_names_lit':
        yalb__pzuhk, 'value_names_lit': lqcq__xxdui, 'columns_name_lit':
        ufroo__ssd, **tbxk__flr, 'tracing': tracing}
    exec(work__dgjdz, tlnd__kbgy, poti__lbr)
    impl = poti__lbr['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    okz__lvx = {}
    okz__lvx['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, wkatw__aymoh in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        feqr__nfri = None
        if isinstance(wkatw__aymoh, bodo.DatetimeArrayType):
            spty__ryv = 'datetimetz'
            bffz__aoh = 'datetime64[ns]'
            if isinstance(wkatw__aymoh.tz, int):
                fbj__eia = bodo.libs.pd_datetime_arr_ext.nanoseconds_to_offset(
                    wkatw__aymoh.tz)
            else:
                fbj__eia = pd.DatetimeTZDtype(tz=wkatw__aymoh.tz).tz
            feqr__nfri = {'timezone': pa.lib.tzinfo_to_string(fbj__eia)}
        elif isinstance(wkatw__aymoh, types.Array
            ) or wkatw__aymoh == boolean_array:
            spty__ryv = bffz__aoh = wkatw__aymoh.dtype.name
            if bffz__aoh.startswith('datetime'):
                spty__ryv = 'datetime'
        elif is_str_arr_type(wkatw__aymoh):
            spty__ryv = 'unicode'
            bffz__aoh = 'object'
        elif wkatw__aymoh == binary_array_type:
            spty__ryv = 'bytes'
            bffz__aoh = 'object'
        elif isinstance(wkatw__aymoh, DecimalArrayType):
            spty__ryv = bffz__aoh = 'object'
        elif isinstance(wkatw__aymoh, IntegerArrayType):
            vsyk__lfq = wkatw__aymoh.dtype.name
            if vsyk__lfq.startswith('int'):
                bffz__aoh = 'Int' + vsyk__lfq[3:]
            elif vsyk__lfq.startswith('uint'):
                bffz__aoh = 'UInt' + vsyk__lfq[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, wkatw__aymoh))
            spty__ryv = wkatw__aymoh.dtype.name
        elif isinstance(wkatw__aymoh, bodo.FloatingArrayType):
            vsyk__lfq = wkatw__aymoh.dtype.name
            spty__ryv = vsyk__lfq
            bffz__aoh = vsyk__lfq.capitalize()
        elif wkatw__aymoh == datetime_date_array_type:
            spty__ryv = 'datetime'
            bffz__aoh = 'object'
        elif isinstance(wkatw__aymoh, TimeArrayType):
            spty__ryv = 'datetime'
            bffz__aoh = 'object'
        elif isinstance(wkatw__aymoh, (StructArrayType, ArrayItemArrayType)):
            spty__ryv = 'object'
            bffz__aoh = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, wkatw__aymoh))
        qidd__bvbnc = {'name': col_name, 'field_name': col_name,
            'pandas_type': spty__ryv, 'numpy_type': bffz__aoh, 'metadata':
            feqr__nfri}
        okz__lvx['columns'].append(qidd__bvbnc)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            crnbn__gmzze = '__index_level_0__'
            qqco__vur = None
        else:
            crnbn__gmzze = '%s'
            qqco__vur = '%s'
        okz__lvx['index_columns'] = [crnbn__gmzze]
        okz__lvx['columns'].append({'name': qqco__vur, 'field_name':
            crnbn__gmzze, 'pandas_type': index.pandas_type_name,
            'numpy_type': index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        okz__lvx['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        okz__lvx['index_columns'] = []
    okz__lvx['pandas_version'] = pd.__version__
    return okz__lvx


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
        ytdn__haiq = []
        for uehvi__oqs in partition_cols:
            try:
                idx = df.columns.index(uehvi__oqs)
            except ValueError as ygjyd__guorp:
                raise BodoError(
                    f'Partition column {uehvi__oqs} is not in dataframe')
            ytdn__haiq.append(idx)
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
    jwdf__rvcs = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType
        )
    mphnz__gmrj = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not jwdf__rvcs)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not jwdf__rvcs or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and jwdf__rvcs and not is_overload_true(_is_parallel)
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
        lwf__cdszk = df.runtime_data_types
        sihhs__xkj = len(lwf__cdszk)
        feqr__nfri = gen_pandas_parquet_metadata([''] * sihhs__xkj,
            lwf__cdszk, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        ryp__pqp = feqr__nfri['columns'][:sihhs__xkj]
        feqr__nfri['columns'] = feqr__nfri['columns'][sihhs__xkj:]
        ryp__pqp = [json.dumps(lhry__mbryr).replace('""', '{0}') for
            lhry__mbryr in ryp__pqp]
        fgp__uqq = json.dumps(feqr__nfri)
        exr__nvab = '"columns": ['
        yls__yrn = fgp__uqq.find(exr__nvab)
        if yls__yrn == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        fjk__hxe = yls__yrn + len(exr__nvab)
        ehan__njyr = fgp__uqq[:fjk__hxe]
        fgp__uqq = fgp__uqq[fjk__hxe:]
        nur__bqj = len(feqr__nfri['columns'])
    else:
        fgp__uqq = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and jwdf__rvcs:
        fgp__uqq = fgp__uqq.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            fgp__uqq = fgp__uqq.replace('"%s"', '%s')
    if not df.is_table_format:
        fjejc__sevge = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    work__dgjdz = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        work__dgjdz += '    py_table = get_dataframe_table(df)\n'
        work__dgjdz += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        work__dgjdz += '    info_list = [{}]\n'.format(fjejc__sevge)
        work__dgjdz += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        work__dgjdz += '    columns_index = get_dataframe_column_names(df)\n'
        work__dgjdz += '    names_arr = index_to_array(columns_index)\n'
        work__dgjdz += '    col_names = array_to_info(names_arr)\n'
    else:
        work__dgjdz += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and mphnz__gmrj:
        work__dgjdz += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        bojom__oyg = True
    else:
        work__dgjdz += '    index_col = array_to_info(np.empty(0))\n'
        bojom__oyg = False
    if df.has_runtime_cols:
        work__dgjdz += '    columns_lst = []\n'
        work__dgjdz += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            work__dgjdz += f'    for _ in range(len(py_table.block_{i})):\n'
            work__dgjdz += f"""        columns_lst.append({ryp__pqp[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            work__dgjdz += '        num_cols += 1\n'
        if nur__bqj:
            work__dgjdz += "    columns_lst.append('')\n"
        work__dgjdz += '    columns_str = ", ".join(columns_lst)\n'
        work__dgjdz += ('    metadata = """' + ehan__njyr +
            '""" + columns_str + """' + fgp__uqq + '"""\n')
    else:
        work__dgjdz += '    metadata = """' + fgp__uqq + '"""\n'
    work__dgjdz += '    if compression is None:\n'
    work__dgjdz += "        compression = 'none'\n"
    work__dgjdz += '    if _bodo_timestamp_tz is None:\n'
    work__dgjdz += "        _bodo_timestamp_tz = ''\n"
    work__dgjdz += '    if df.index.name is not None:\n'
    work__dgjdz += '        name_ptr = df.index.name\n'
    work__dgjdz += '    else:\n'
    work__dgjdz += "        name_ptr = 'null'\n"
    work__dgjdz += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    rlqa__zrhs = None
    if partition_cols:
        rlqa__zrhs = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        iwife__vjovq = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in ytdn__haiq)
        if iwife__vjovq:
            work__dgjdz += '    cat_info_list = [{}]\n'.format(iwife__vjovq)
            work__dgjdz += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            work__dgjdz += '    cat_table = table\n'
        work__dgjdz += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        work__dgjdz += (
            f'    part_cols_idxs = np.array({ytdn__haiq}, dtype=np.int32)\n')
        work__dgjdz += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        work__dgjdz += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        work__dgjdz += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        work__dgjdz += (
            '                            unicode_to_utf8(compression),\n')
        work__dgjdz += '                            _is_parallel,\n'
        work__dgjdz += (
            '                            unicode_to_utf8(bucket_region),\n')
        work__dgjdz += '                            row_group_size,\n'
        work__dgjdz += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        work__dgjdz += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        work__dgjdz += '    delete_table_decref_arrays(table)\n'
        work__dgjdz += '    delete_info_decref_array(index_col)\n'
        work__dgjdz += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        work__dgjdz += '    delete_info_decref_array(col_names)\n'
        if iwife__vjovq:
            work__dgjdz += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        work__dgjdz += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        work__dgjdz += (
            '                            table, col_names, index_col,\n')
        work__dgjdz += '                            ' + str(bojom__oyg) + ',\n'
        work__dgjdz += (
            '                            unicode_to_utf8(metadata),\n')
        work__dgjdz += (
            '                            unicode_to_utf8(compression),\n')
        work__dgjdz += (
            '                            _is_parallel, 1, df.index.start,\n')
        work__dgjdz += (
            '                            df.index.stop, df.index.step,\n')
        work__dgjdz += (
            '                            unicode_to_utf8(name_ptr),\n')
        work__dgjdz += (
            '                            unicode_to_utf8(bucket_region),\n')
        work__dgjdz += '                            row_group_size,\n'
        work__dgjdz += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        work__dgjdz += '                              False,\n'
        work__dgjdz += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        work__dgjdz += '                              False)\n'
        work__dgjdz += '    delete_table_decref_arrays(table)\n'
        work__dgjdz += '    delete_info_decref_array(index_col)\n'
        work__dgjdz += '    delete_info_decref_array(col_names)\n'
    else:
        work__dgjdz += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        work__dgjdz += (
            '                            table, col_names, index_col,\n')
        work__dgjdz += '                            ' + str(bojom__oyg) + ',\n'
        work__dgjdz += (
            '                            unicode_to_utf8(metadata),\n')
        work__dgjdz += (
            '                            unicode_to_utf8(compression),\n')
        work__dgjdz += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        work__dgjdz += (
            '                            unicode_to_utf8(name_ptr),\n')
        work__dgjdz += (
            '                            unicode_to_utf8(bucket_region),\n')
        work__dgjdz += '                            row_group_size,\n'
        work__dgjdz += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        work__dgjdz += '                              False,\n'
        work__dgjdz += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        work__dgjdz += '                              False)\n'
        work__dgjdz += '    delete_table_decref_arrays(table)\n'
        work__dgjdz += '    delete_info_decref_array(index_col)\n'
        work__dgjdz += '    delete_info_decref_array(col_names)\n'
    poti__lbr = {}
    if df.has_runtime_cols:
        nqf__zipqm = None
    else:
        for zynzr__ofxp in df.columns:
            if not isinstance(zynzr__ofxp, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        nqf__zipqm = pd.array(df.columns)
    exec(work__dgjdz, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': nqf__zipqm,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': rlqa__zrhs, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, poti__lbr)
    tnrad__evo = poti__lbr['df_to_parquet']
    return tnrad__evo


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    uwsse__kmyzl = tracing.Event('to_sql_exception_guard', is_parallel=
        _is_parallel)
    iyq__afx = 'all_ok'
    oxr__jrfr, kwcky__yashf = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        jqxrp__zak = 100
        if chunksize is None:
            ykva__jyoo = jqxrp__zak
        else:
            ykva__jyoo = min(chunksize, jqxrp__zak)
        if _is_table_create:
            df = df.iloc[:ykva__jyoo, :]
        else:
            df = df.iloc[ykva__jyoo:, :]
            if len(df) == 0:
                return iyq__afx
    bjn__xzef = df.columns
    try:
        if oxr__jrfr == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            uuacd__kgdb = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            lri__zmk = bodo.typeof(df)
            orpga__eaosb = {}
            for pnbo__jwfxx, ihkm__lesu in zip(lri__zmk.columns, lri__zmk.data
                ):
                if df[pnbo__jwfxx].dtype == 'object':
                    if ihkm__lesu == datetime_date_array_type:
                        orpga__eaosb[pnbo__jwfxx] = sa.types.Date
                    elif ihkm__lesu in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not uuacd__kgdb or 
                        uuacd__kgdb == '0'):
                        orpga__eaosb[pnbo__jwfxx] = VARCHAR2(4000)
            dtype = orpga__eaosb
        try:
            yhv__yaaxs = tracing.Event('df_to_sql', is_parallel=_is_parallel)
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
            yhv__yaaxs.finalize()
        except Exception as oztkh__rqfx:
            iyq__afx = oztkh__rqfx.args[0]
            if oxr__jrfr == 'oracle' and 'ORA-12899' in iyq__afx:
                iyq__afx += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return iyq__afx
    finally:
        df.columns = bjn__xzef
        uwsse__kmyzl.finalize()


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    uwsse__kmyzl = tracing.Event('to_sql_exception_guard_encaps',
        is_parallel=_is_parallel)
    with numba.objmode(out='unicode_type'):
        rez__wwomh = tracing.Event('to_sql_exception_guard_encaps:objmode',
            is_parallel=_is_parallel)
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
        rez__wwomh.finalize()
    uwsse__kmyzl.finalize()
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
    for zynzr__ofxp in df.columns:
        if not isinstance(zynzr__ofxp, str):
            raise BodoError(
                'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
    nqf__zipqm = pd.array(df.columns)
    work__dgjdz = """def df_to_sql(
    df, name, con,
    schema=None, if_exists='fail', index=True,
    index_label=None, chunksize=None, dtype=None,
    method=None, _bodo_allow_downcasting=False,
    _is_parallel=False,
):
"""
    work__dgjdz += """    if con.startswith('iceberg'):
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
        work__dgjdz += f'        py_table = get_dataframe_table(df)\n'
        work__dgjdz += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        fjejc__sevge = ', '.join(
            f'array_to_info(get_dataframe_data(df, {i}))' for i in range(
            len(df.columns)))
        work__dgjdz += f'        info_list = [{fjejc__sevge}]\n'
        work__dgjdz += f'        table = arr_info_list_to_table(info_list)\n'
    work__dgjdz += """        col_names = array_to_info(col_names_arr)
        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names,
            if_exists, _is_parallel, pyarrow_table_schema,
            _bodo_allow_downcasting,
        )
        delete_table_decref_arrays(table)
        delete_info_decref_array(col_names)
"""
    work__dgjdz += "    elif con.startswith('snowflake'):\n"
    work__dgjdz += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        if _bodo_allow_downcasting and bodo.get_rank() == 0:
            warnings.warn('_bodo_allow_downcasting is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl', sync=False)
"""
    work__dgjdz += "        location = ''\n"
    if not is_overload_none(schema):
        work__dgjdz += '        location += \'"\' + schema + \'".\'\n'
    work__dgjdz += '        location += name\n'
    work__dgjdz += '        my_rank = bodo.get_rank()\n'
    work__dgjdz += """        with bodo.objmode(
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
    work__dgjdz += '        bodo.barrier()\n'
    work__dgjdz += '        if azure_stage_direct_upload:\n'
    work__dgjdz += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    work__dgjdz += '        if chunksize is None:\n'
    work__dgjdz += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        work__dgjdz += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        gid__fiawc = ',' if len(df.columns) == 1 else ''
        work__dgjdz += f"""            memory_usage = np.array(({data}{gid__fiawc}), np.int64).sum()
"""
    work__dgjdz += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        work__dgjdz += (
            '        columns_index = get_dataframe_column_names(df)\n')
        work__dgjdz += '        names_arr = index_to_array(columns_index)\n'
        work__dgjdz += '        col_names = array_to_info(names_arr)\n'
    else:
        work__dgjdz += '        col_names = array_to_info(col_names_arr)\n'
    work__dgjdz += '        index_col = array_to_info(np.empty(0))\n'
    work__dgjdz += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    work__dgjdz += """        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           
"""
    work__dgjdz += '        upload_threads_in_progress = []\n'
    work__dgjdz += """        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           
"""
    work__dgjdz += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    work__dgjdz += '            chunk_path = parquet_path + chunk_name\n'
    work__dgjdz += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    work__dgjdz += (
        '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n')
    work__dgjdz += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    work__dgjdz += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        work__dgjdz += (
            '            py_table_chunk = get_dataframe_table(chunk)\n')
        work__dgjdz += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        grwzx__tptd = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        work__dgjdz += (
            f'            table_chunk = arr_info_list_to_table([{grwzx__tptd}])     \n'
            )
    work__dgjdz += '            ev_to_df_table.finalize()\n'
    work__dgjdz += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
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
    work__dgjdz += '        bodo.barrier()\n'
    buyxo__eme = bodo.io.snowflake.gen_snowflake_schema(df.columns, df.data)
    work__dgjdz += f"""        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, {buyxo__eme},
                if_exists, old_creds, tmp_folder,
                azure_stage_direct_upload, old_core_site,
                old_sas_token,
            )
"""
    work__dgjdz += '        if azure_stage_direct_upload:\n'
    work__dgjdz += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    work__dgjdz += '        ev.finalize()\n'
    work__dgjdz += '    else:\n'
    work__dgjdz += (
        '        if _bodo_allow_downcasting and bodo.get_rank() == 0:\n')
    work__dgjdz += """            warnings.warn('_bodo_allow_downcasting is not supported for SQL tables.')
"""
    work__dgjdz += '        rank = bodo.libs.distributed_api.get_rank()\n'
    work__dgjdz += "        err_msg = 'unset'\n"
    work__dgjdz += '        if rank != 0:\n'
    work__dgjdz += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    work__dgjdz += '        elif rank == 0:\n'
    work__dgjdz += '            err_msg = to_sql_exception_guard_encaps(\n'
    work__dgjdz += """                          df, name, con, schema, if_exists, index, index_label,
"""
    work__dgjdz += '                          chunksize, dtype, method,\n'
    work__dgjdz += '                          True, _is_parallel,\n'
    work__dgjdz += '                      )\n'
    work__dgjdz += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    work__dgjdz += "        if_exists = 'append'\n"
    work__dgjdz += "        if _is_parallel and err_msg == 'all_ok':\n"
    work__dgjdz += '            err_msg = to_sql_exception_guard_encaps(\n'
    work__dgjdz += """                          df, name, con, schema, if_exists, index, index_label,
"""
    work__dgjdz += '                          chunksize, dtype, method,\n'
    work__dgjdz += '                          False, _is_parallel,\n'
    work__dgjdz += '                      )\n'
    work__dgjdz += "        if err_msg != 'all_ok':\n"
    work__dgjdz += "            print('err_msg=', err_msg)\n"
    work__dgjdz += (
        "            raise ValueError('error in to_sql() operation')\n")
    poti__lbr = {}
    tlnd__kbgy = globals().copy()
    tlnd__kbgy.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        nqf__zipqm, 'delete_info_decref_array': delete_info_decref_array,
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
    exec(work__dgjdz, tlnd__kbgy, poti__lbr)
    _impl = poti__lbr['df_to_sql']
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
        pjoz__jdloz = get_overload_const_str(path_or_buf)
        if pjoz__jdloz.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        kjfvh__erv = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(kjfvh__erv), unicode_to_utf8(_bodo_file_prefix)
                )
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(kjfvh__erv), unicode_to_utf8(_bodo_file_prefix)
                )
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    ffrtk__njrgz = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    zzvu__qfw = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', ffrtk__njrgz, zzvu__qfw,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    work__dgjdz = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        xib__mytle = data.data.dtype.categories
        work__dgjdz += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        xib__mytle = data.dtype.categories
        work__dgjdz += '  data_values = data\n'
    chnb__mzysu = len(xib__mytle)
    work__dgjdz += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    work__dgjdz += '  numba.parfors.parfor.init_prange()\n'
    work__dgjdz += '  n = len(data_values)\n'
    for i in range(chnb__mzysu):
        work__dgjdz += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    work__dgjdz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    work__dgjdz += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for lif__ajram in range(chnb__mzysu):
        work__dgjdz += '          data_arr_{}[i] = 0\n'.format(lif__ajram)
    work__dgjdz += '      else:\n'
    for davwl__otzr in range(chnb__mzysu):
        work__dgjdz += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            davwl__otzr)
    fjejc__sevge = ', '.join(f'data_arr_{i}' for i in range(chnb__mzysu))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(xib__mytle[0], np.datetime64):
        xib__mytle = tuple(pd.Timestamp(pnbo__jwfxx) for pnbo__jwfxx in
            xib__mytle)
    elif isinstance(xib__mytle[0], np.timedelta64):
        xib__mytle = tuple(pd.Timedelta(pnbo__jwfxx) for pnbo__jwfxx in
            xib__mytle)
    return bodo.hiframes.dataframe_impl._gen_init_df(work__dgjdz,
        xib__mytle, fjejc__sevge, index)


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
    for nuimc__ubtk in pd_unsupported:
        lyj__ran = mod_name + '.' + nuimc__ubtk.__name__
        overload(nuimc__ubtk, no_unliteral=True)(create_unsupported_overload
            (lyj__ran))


def _install_dataframe_unsupported():
    for baw__yplx in dataframe_unsupported_attrs:
        mrq__fipan = 'DataFrame.' + baw__yplx
        overload_attribute(DataFrameType, baw__yplx)(
            create_unsupported_overload(mrq__fipan))
    for lyj__ran in dataframe_unsupported:
        mrq__fipan = 'DataFrame.' + lyj__ran + '()'
        overload_method(DataFrameType, lyj__ran)(create_unsupported_overload
            (mrq__fipan))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
