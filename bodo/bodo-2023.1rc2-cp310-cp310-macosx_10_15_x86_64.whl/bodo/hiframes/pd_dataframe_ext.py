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
            fkoxf__jcquu = (
                f'{len(self.data)} columns of types {set(self.data)}')
            hqt__hanf = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            sxvtc__epdpb = str(hash(super().__str__()))
            return (
                f'dataframe({fkoxf__jcquu}, {self.index}, {hqt__hanf}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols}, key_hash={sxvtc__epdpb})'
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
        return {cvcr__koi: i for i, cvcr__koi in enumerate(self.columns)}

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
            vnon__aizen = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            data = tuple(owfom__rejrd.unify(typingctx, nklrg__pvbfl) if 
                owfom__rejrd != nklrg__pvbfl else owfom__rejrd for 
                owfom__rejrd, nklrg__pvbfl in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if vnon__aizen is not None and None not in data:
                return DataFrameType(data, vnon__aizen, self.columns, dist,
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
        return all(owfom__rejrd.is_precise() for owfom__rejrd in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        ehlud__iiu = self.columns.index(col_name)
        vvz__ays = tuple(list(self.data[:ehlud__iiu]) + [new_type] + list(
            self.data[ehlud__iiu + 1:]))
        return DataFrameType(vvz__ays, self.index, self.columns, self.dist,
            self.is_table_format)


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
        hut__svhyb = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            hut__svhyb.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, hut__svhyb)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        hut__svhyb = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, hut__svhyb)


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
        bghya__okxn = 'n',
        htt__lsx = {'n': 5}
        ouiyc__kxg, syx__kke = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, bghya__okxn, htt__lsx)
        nqxs__mlugw = syx__kke[0]
        if not is_overload_int(nqxs__mlugw):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        huup__fgx = df.copy()
        return huup__fgx(*syx__kke).replace(pysig=ouiyc__kxg)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        xbt__pbu = (df,) + args
        bghya__okxn = 'df', 'method', 'min_periods'
        htt__lsx = {'method': 'pearson', 'min_periods': 1}
        ejwa__ghwib = 'method',
        ouiyc__kxg, syx__kke = bodo.utils.typing.fold_typing_args(func_name,
            xbt__pbu, kws, bghya__okxn, htt__lsx, ejwa__ghwib)
        kcyp__gjy = syx__kke[2]
        if not is_overload_int(kcyp__gjy):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        jefmk__esjpt = []
        njw__dlbyl = []
        for cvcr__koi, xlrbl__vph in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(xlrbl__vph.dtype):
                jefmk__esjpt.append(cvcr__koi)
                njw__dlbyl.append(types.Array(types.float64, 1, 'A'))
        if len(jefmk__esjpt) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        njw__dlbyl = tuple(njw__dlbyl)
        jefmk__esjpt = tuple(jefmk__esjpt)
        index_typ = bodo.utils.typing.type_col_to_index(jefmk__esjpt)
        huup__fgx = DataFrameType(njw__dlbyl, index_typ, jefmk__esjpt)
        return huup__fgx(*syx__kke).replace(pysig=ouiyc__kxg)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        gxcs__mpq = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        zfuj__kmg = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        nvmdr__muzn = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        mob__jxje = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        wnaa__ymvhn = dict(raw=zfuj__kmg, result_type=nvmdr__muzn)
        nerl__ritck = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', wnaa__ymvhn, nerl__ritck,
            package_name='pandas', module_name='DataFrame')
        ugm__qwyqx = True
        if types.unliteral(gxcs__mpq) == types.unicode_type:
            if not is_overload_constant_str(gxcs__mpq):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            ugm__qwyqx = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        pcb__xjey = get_overload_const_int(axis)
        if ugm__qwyqx and pcb__xjey != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif pcb__xjey not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        ufd__ayl = []
        for arr_typ in df.data:
            mvnh__tsdyp = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            uqaq__ezhh = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(mvnh__tsdyp), types.int64), {}
                ).return_type
            ufd__ayl.append(uqaq__ezhh)
        hia__riyf = types.none
        whni__xrlg = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(cvcr__koi) for cvcr__koi in df.columns)), None)
        pbtr__egzq = types.BaseTuple.from_types(ufd__ayl)
        rhug__bqupy = types.Tuple([types.bool_] * len(pbtr__egzq))
        cauby__qxqen = bodo.NullableTupleType(pbtr__egzq, rhug__bqupy)
        gbdb__dfo = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if gbdb__dfo == types.NPDatetime('ns'):
            gbdb__dfo = bodo.pd_timestamp_tz_naive_type
        if gbdb__dfo == types.NPTimedelta('ns'):
            gbdb__dfo = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(pbtr__egzq):
            afvod__ndt = HeterogeneousSeriesType(cauby__qxqen, whni__xrlg,
                gbdb__dfo)
        else:
            afvod__ndt = SeriesType(pbtr__egzq.dtype, cauby__qxqen,
                whni__xrlg, gbdb__dfo)
        fzdjb__aqrj = afvod__ndt,
        if mob__jxje is not None:
            fzdjb__aqrj += tuple(mob__jxje.types)
        try:
            if not ugm__qwyqx:
                wdqq__ehzx = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(gxcs__mpq), self.context,
                    'DataFrame.apply', axis if pcb__xjey == 1 else None)
            else:
                wdqq__ehzx = get_const_func_output_type(gxcs__mpq,
                    fzdjb__aqrj, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as byute__swflb:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                byute__swflb))
        if ugm__qwyqx:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(wdqq__ehzx, (SeriesType, HeterogeneousSeriesType)
                ) and wdqq__ehzx.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(wdqq__ehzx, HeterogeneousSeriesType):
                huesb__nmst, wgw__zpzu = wdqq__ehzx.const_info
                if isinstance(wdqq__ehzx.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    gtxpc__apwh = wdqq__ehzx.data.tuple_typ.types
                elif isinstance(wdqq__ehzx.data, types.Tuple):
                    gtxpc__apwh = wdqq__ehzx.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                plvg__xhrbg = tuple(to_nullable_type(dtype_to_array_type(
                    tssga__llgq)) for tssga__llgq in gtxpc__apwh)
                ect__ivyd = DataFrameType(plvg__xhrbg, df.index, wgw__zpzu)
            elif isinstance(wdqq__ehzx, SeriesType):
                yqf__vxy, wgw__zpzu = wdqq__ehzx.const_info
                plvg__xhrbg = tuple(to_nullable_type(dtype_to_array_type(
                    wdqq__ehzx.dtype)) for huesb__nmst in range(yqf__vxy))
                ect__ivyd = DataFrameType(plvg__xhrbg, df.index, wgw__zpzu)
            else:
                ghbxz__gagx = get_udf_out_arr_type(wdqq__ehzx)
                ect__ivyd = SeriesType(ghbxz__gagx.dtype, ghbxz__gagx, df.
                    index, None)
        else:
            ect__ivyd = wdqq__ehzx
        wfl__olnua = ', '.join("{} = ''".format(owfom__rejrd) for
            owfom__rejrd in kws.keys())
        eau__ossh = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {wfl__olnua}):
"""
        eau__ossh += '    pass\n'
        rvdod__chiz = {}
        exec(eau__ossh, {}, rvdod__chiz)
        fhmuh__nav = rvdod__chiz['apply_stub']
        ouiyc__kxg = numba.core.utils.pysignature(fhmuh__nav)
        cakf__owg = (gxcs__mpq, axis, zfuj__kmg, nvmdr__muzn, mob__jxje
            ) + tuple(kws.values())
        return signature(ect__ivyd, *cakf__owg).replace(pysig=ouiyc__kxg)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        bghya__okxn = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        htt__lsx = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        ejwa__ghwib = ('subplots', 'sharex', 'sharey', 'layout',
            'use_index', 'grid', 'style', 'logx', 'logy', 'loglog', 'xlim',
            'ylim', 'rot', 'colormap', 'table', 'yerr', 'xerr',
            'sort_columns', 'secondary_y', 'colorbar', 'position',
            'stacked', 'mark_right', 'include_bool', 'backend')
        ouiyc__kxg, syx__kke = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, bghya__okxn, htt__lsx, ejwa__ghwib)
        xxy__awiep = syx__kke[2]
        if not is_overload_constant_str(xxy__awiep):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        zob__wfam = syx__kke[0]
        if not is_overload_none(zob__wfam) and not (is_overload_int(
            zob__wfam) or is_overload_constant_str(zob__wfam)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(zob__wfam):
            vzohn__qjtb = get_overload_const_str(zob__wfam)
            if vzohn__qjtb not in df.columns:
                raise BodoError(f'{func_name}: {vzohn__qjtb} column not found.'
                    )
        elif is_overload_int(zob__wfam):
            lbue__pvb = get_overload_const_int(zob__wfam)
            if lbue__pvb > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {lbue__pvb} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            zob__wfam = df.columns[zob__wfam]
        iit__boh = syx__kke[1]
        if not is_overload_none(iit__boh) and not (is_overload_int(iit__boh
            ) or is_overload_constant_str(iit__boh)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(iit__boh):
            obbv__dkur = get_overload_const_str(iit__boh)
            if obbv__dkur not in df.columns:
                raise BodoError(f'{func_name}: {obbv__dkur} column not found.')
        elif is_overload_int(iit__boh):
            lzfin__dvdul = get_overload_const_int(iit__boh)
            if lzfin__dvdul > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {lzfin__dvdul} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            iit__boh = df.columns[iit__boh]
        qtzi__wvbgv = syx__kke[3]
        if not is_overload_none(qtzi__wvbgv) and not is_tuple_like_type(
            qtzi__wvbgv):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        qoz__boymp = syx__kke[10]
        if not is_overload_none(qoz__boymp) and not is_overload_constant_str(
            qoz__boymp):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        qcgs__ydnml = syx__kke[12]
        if not is_overload_bool(qcgs__ydnml):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        xnne__cmwy = syx__kke[17]
        if not is_overload_none(xnne__cmwy) and not is_tuple_like_type(
            xnne__cmwy):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        wgbe__xke = syx__kke[18]
        if not is_overload_none(wgbe__xke) and not is_tuple_like_type(wgbe__xke
            ):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        uey__kddz = syx__kke[22]
        if not is_overload_none(uey__kddz) and not is_overload_int(uey__kddz):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        pxvsc__vjwg = syx__kke[29]
        if not is_overload_none(pxvsc__vjwg) and not is_overload_constant_str(
            pxvsc__vjwg):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        eun__rgk = syx__kke[30]
        if not is_overload_none(eun__rgk) and not is_overload_constant_str(
            eun__rgk):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        fjew__ezmln = types.List(types.mpl_line_2d_type)
        xxy__awiep = get_overload_const_str(xxy__awiep)
        if xxy__awiep == 'scatter':
            if is_overload_none(zob__wfam) and is_overload_none(iit__boh):
                raise BodoError(
                    f'{func_name}: {xxy__awiep} requires an x and y column.')
            elif is_overload_none(zob__wfam):
                raise BodoError(
                    f'{func_name}: {xxy__awiep} x column is missing.')
            elif is_overload_none(iit__boh):
                raise BodoError(
                    f'{func_name}: {xxy__awiep} y column is missing.')
            fjew__ezmln = types.mpl_path_collection_type
        elif xxy__awiep != 'line':
            raise BodoError(f'{func_name}: {xxy__awiep} plot is not supported.'
                )
        return signature(fjew__ezmln, *syx__kke).replace(pysig=ouiyc__kxg)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            dvcp__yng = df.columns.index(attr)
            arr_typ = df.data[dvcp__yng]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            vfbhw__qmsai = []
            vvz__ays = []
            okaz__ldgtr = False
            for i, fityt__ugtkb in enumerate(df.columns):
                if fityt__ugtkb[0] != attr:
                    continue
                okaz__ldgtr = True
                vfbhw__qmsai.append(fityt__ugtkb[1] if len(fityt__ugtkb) ==
                    2 else fityt__ugtkb[1:])
                vvz__ays.append(df.data[i])
            if okaz__ldgtr:
                return DataFrameType(tuple(vvz__ays), df.index, tuple(
                    vfbhw__qmsai))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        mjoup__uuza = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(mjoup__uuza)
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
        ttaf__sbku = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], ttaf__sbku)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    yumf__pxn = builder.module
    mwg__ivp = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    epjvu__ldls = cgutils.get_or_insert_function(yumf__pxn, mwg__ivp, name=
        '.dtor.df.{}'.format(df_type))
    if not epjvu__ldls.is_declaration:
        return epjvu__ldls
    epjvu__ldls.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(epjvu__ldls.append_basic_block())
    amzhy__eky = epjvu__ldls.args[0]
    hwjob__led = context.get_value_type(payload_type).as_pointer()
    ohse__igcr = builder.bitcast(amzhy__eky, hwjob__led)
    payload = context.make_helper(builder, payload_type, ref=ohse__igcr)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        frwx__yyxji = context.get_python_api(builder)
        ihycp__puf = frwx__yyxji.gil_ensure()
        frwx__yyxji.decref(payload.parent)
        frwx__yyxji.gil_release(ihycp__puf)
    builder.ret_void()
    return epjvu__ldls


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    wmmjk__dxho = cgutils.create_struct_proxy(payload_type)(context, builder)
    wmmjk__dxho.data = data_tup
    wmmjk__dxho.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        wmmjk__dxho.columns = colnames
    yryjc__udhgu = context.get_value_type(payload_type)
    rtzw__zqkiv = context.get_abi_sizeof(yryjc__udhgu)
    uhto__anq = define_df_dtor(context, builder, df_type, payload_type)
    drq__ssa = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, rtzw__zqkiv), uhto__anq)
    fuaee__jre = context.nrt.meminfo_data(builder, drq__ssa)
    sfi__orl = builder.bitcast(fuaee__jre, yryjc__udhgu.as_pointer())
    mot__wfb = cgutils.create_struct_proxy(df_type)(context, builder)
    mot__wfb.meminfo = drq__ssa
    if parent is None:
        mot__wfb.parent = cgutils.get_null_value(mot__wfb.parent.type)
    else:
        mot__wfb.parent = parent
        wmmjk__dxho.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            frwx__yyxji = context.get_python_api(builder)
            ihycp__puf = frwx__yyxji.gil_ensure()
            frwx__yyxji.incref(parent)
            frwx__yyxji.gil_release(ihycp__puf)
    builder.store(wmmjk__dxho._getvalue(), sfi__orl)
    return mot__wfb._getvalue()


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
        uof__rbt = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        uof__rbt = [tssga__llgq for tssga__llgq in data_typ.dtype.arr_types]
    jhd__udg = DataFrameType(tuple(uof__rbt + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        zqk__egjom = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return zqk__egjom
    sig = signature(jhd__udg, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    yqf__vxy = len(data_tup_typ.types)
    if yqf__vxy == 0:
        column_names = ()
    jvig__mwcr = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(jvig__mwcr, ColNamesMetaType) and isinstance(jvig__mwcr
        .meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = jvig__mwcr.meta
    if yqf__vxy == 1 and isinstance(data_tup_typ.types[0], TableType):
        yqf__vxy = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == yqf__vxy, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    dsd__knsd = data_tup_typ.types
    if yqf__vxy != 0 and isinstance(data_tup_typ.types[0], TableType):
        dsd__knsd = data_tup_typ.types[0].arr_types
        is_table_format = True
    jhd__udg = DataFrameType(dsd__knsd, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            ebjzl__gequt = cgutils.create_struct_proxy(jhd__udg.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = ebjzl__gequt.parent
        zqk__egjom = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return zqk__egjom
    sig = signature(jhd__udg, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        mot__wfb = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, mot__wfb.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        wmmjk__dxho = get_dataframe_payload(context, builder, df_typ, args[0])
        zuxav__jbdet = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[zuxav__jbdet]
        if df_typ.is_table_format:
            ebjzl__gequt = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(wmmjk__dxho.data, 0))
            qdhx__fnk = df_typ.table_type.type_to_blk[arr_typ]
            kkt__hnuz = getattr(ebjzl__gequt, f'block_{qdhx__fnk}')
            dvt__nmtun = ListInstance(context, builder, types.List(arr_typ),
                kkt__hnuz)
            gqv__bln = context.get_constant(types.int64, df_typ.table_type.
                block_offsets[zuxav__jbdet])
            ttaf__sbku = dvt__nmtun.getitem(gqv__bln)
        else:
            ttaf__sbku = builder.extract_value(wmmjk__dxho.data, zuxav__jbdet)
        uzhb__mapss = cgutils.alloca_once_value(builder, ttaf__sbku)
        agxyt__xndhu = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, uzhb__mapss, agxyt__xndhu)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    drq__ssa = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, drq__ssa)
    hwjob__led = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, hwjob__led)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    jhd__udg = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        jhd__udg = types.Tuple([TableType(df_typ.data)])
    sig = signature(jhd__udg, df_typ)

    def codegen(context, builder, signature, args):
        wmmjk__dxho = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            wmmjk__dxho.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        wmmjk__dxho = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index,
            wmmjk__dxho.index)
    jhd__udg = df_typ.index
    sig = signature(jhd__udg, df_typ)
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
        huup__fgx = df.data[i]
        return huup__fgx(*args)


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
        wmmjk__dxho = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(wmmjk__dxho.data, 0))
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
    yiem__tpeo = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{yiem__tpeo})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        huup__fgx = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return huup__fgx(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        wmmjk__dxho = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, wmmjk__dxho.columns)
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
    pbtr__egzq = self.typemap[data_tup.name]
    if any(is_tuple_like_type(tssga__llgq) for tssga__llgq in pbtr__egzq.types
        ):
        return None
    if equiv_set.has_shape(data_tup):
        mscek__fyiza = equiv_set.get_shape(data_tup)
        if len(mscek__fyiza) > 1:
            equiv_set.insert_equiv(*mscek__fyiza)
        if len(mscek__fyiza) > 0:
            whni__xrlg = self.typemap[index.name]
            if not isinstance(whni__xrlg, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(mscek__fyiza[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(mscek__fyiza[0], len(
                mscek__fyiza)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    rsrs__qywyg = args[0]
    data_types = self.typemap[rsrs__qywyg.name].data
    if any(is_tuple_like_type(tssga__llgq) for tssga__llgq in data_types):
        return None
    if equiv_set.has_shape(rsrs__qywyg):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            rsrs__qywyg)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    rsrs__qywyg = args[0]
    whni__xrlg = self.typemap[rsrs__qywyg.name].index
    if isinstance(whni__xrlg, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(rsrs__qywyg):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            rsrs__qywyg)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    rsrs__qywyg = args[0]
    if equiv_set.has_shape(rsrs__qywyg):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            rsrs__qywyg), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    rsrs__qywyg = args[0]
    if equiv_set.has_shape(rsrs__qywyg):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            rsrs__qywyg)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    zuxav__jbdet = get_overload_const_int(c_ind_typ)
    if df_typ.data[zuxav__jbdet] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        wpxjn__dzq, huesb__nmst, wru__ipnca = args
        wmmjk__dxho = get_dataframe_payload(context, builder, df_typ,
            wpxjn__dzq)
        if df_typ.is_table_format:
            ebjzl__gequt = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(wmmjk__dxho.data, 0))
            qdhx__fnk = df_typ.table_type.type_to_blk[arr_typ]
            kkt__hnuz = getattr(ebjzl__gequt, f'block_{qdhx__fnk}')
            dvt__nmtun = ListInstance(context, builder, types.List(arr_typ),
                kkt__hnuz)
            gqv__bln = context.get_constant(types.int64, df_typ.table_type.
                block_offsets[zuxav__jbdet])
            dvt__nmtun.setitem(gqv__bln, wru__ipnca, True)
        else:
            ttaf__sbku = builder.extract_value(wmmjk__dxho.data, zuxav__jbdet)
            context.nrt.decref(builder, df_typ.data[zuxav__jbdet], ttaf__sbku)
            wmmjk__dxho.data = builder.insert_value(wmmjk__dxho.data,
                wru__ipnca, zuxav__jbdet)
            context.nrt.incref(builder, arr_typ, wru__ipnca)
        mot__wfb = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=wpxjn__dzq)
        payload_type = DataFramePayloadType(df_typ)
        ohse__igcr = context.nrt.meminfo_data(builder, mot__wfb.meminfo)
        hwjob__led = context.get_value_type(payload_type).as_pointer()
        ohse__igcr = builder.bitcast(ohse__igcr, hwjob__led)
        builder.store(wmmjk__dxho._getvalue(), ohse__igcr)
        return impl_ret_borrowed(context, builder, df_typ, wpxjn__dzq)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        bsz__zhmwq = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        dvge__fqq = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=bsz__zhmwq)
        rxx__ygzfj = get_dataframe_payload(context, builder, df_typ, bsz__zhmwq
            )
        mot__wfb = construct_dataframe(context, builder, signature.
            return_type, rxx__ygzfj.data, index_val, dvge__fqq.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), rxx__ygzfj.data)
        return mot__wfb
    jhd__udg = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(jhd__udg, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    yqf__vxy = len(df_type.columns)
    zqgob__ldrw = yqf__vxy
    els__rlxk = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    bbv__dccno = col_name not in df_type.columns
    zuxav__jbdet = yqf__vxy
    if bbv__dccno:
        els__rlxk += arr_type,
        column_names += col_name,
        zqgob__ldrw += 1
    else:
        zuxav__jbdet = df_type.columns.index(col_name)
        els__rlxk = tuple(arr_type if i == zuxav__jbdet else els__rlxk[i] for
            i in range(yqf__vxy))

    def codegen(context, builder, signature, args):
        wpxjn__dzq, huesb__nmst, wru__ipnca = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, wpxjn__dzq)
        eroo__hetqa = cgutils.create_struct_proxy(df_type)(context, builder,
            value=wpxjn__dzq)
        if df_type.is_table_format:
            xuvog__ujbu = df_type.table_type
            dcdx__fvq = builder.extract_value(in_dataframe_payload.data, 0)
            nwjb__vlv = TableType(els__rlxk)
            hdwuu__yhdrx = set_table_data_codegen(context, builder,
                xuvog__ujbu, dcdx__fvq, nwjb__vlv, arr_type, wru__ipnca,
                zuxav__jbdet, bbv__dccno)
            data_tup = context.make_tuple(builder, types.Tuple([nwjb__vlv]),
                [hdwuu__yhdrx])
        else:
            dsd__knsd = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != zuxav__jbdet else wru__ipnca) for i in range(
                yqf__vxy)]
            if bbv__dccno:
                dsd__knsd.append(wru__ipnca)
            for rsrs__qywyg, vjn__ssf in zip(dsd__knsd, els__rlxk):
                context.nrt.incref(builder, vjn__ssf, rsrs__qywyg)
            data_tup = context.make_tuple(builder, types.Tuple(els__rlxk),
                dsd__knsd)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        wwaoj__xqyf = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, eroo__hetqa.parent, None)
        if not bbv__dccno and arr_type == df_type.data[zuxav__jbdet]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            ohse__igcr = context.nrt.meminfo_data(builder, eroo__hetqa.meminfo)
            hwjob__led = context.get_value_type(payload_type).as_pointer()
            ohse__igcr = builder.bitcast(ohse__igcr, hwjob__led)
            jnuw__gtsik = get_dataframe_payload(context, builder, df_type,
                wwaoj__xqyf)
            builder.store(jnuw__gtsik._getvalue(), ohse__igcr)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, nwjb__vlv, builder.
                    extract_value(data_tup, 0))
            else:
                for rsrs__qywyg, vjn__ssf in zip(dsd__knsd, els__rlxk):
                    context.nrt.incref(builder, vjn__ssf, rsrs__qywyg)
        has_parent = cgutils.is_not_null(builder, eroo__hetqa.parent)
        with builder.if_then(has_parent):
            frwx__yyxji = context.get_python_api(builder)
            ihycp__puf = frwx__yyxji.gil_ensure()
            xbbvz__gicg = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, wru__ipnca)
            cvcr__koi = numba.core.pythonapi._BoxContext(context, builder,
                frwx__yyxji, xbbvz__gicg)
            yysw__kvrm = cvcr__koi.pyapi.from_native_value(arr_type,
                wru__ipnca, cvcr__koi.env_manager)
            if isinstance(col_name, str):
                lxq__unz = context.insert_const_string(builder.module, col_name
                    )
                bww__yia = frwx__yyxji.string_from_string(lxq__unz)
            else:
                assert isinstance(col_name, int)
                bww__yia = frwx__yyxji.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            frwx__yyxji.object_setitem(eroo__hetqa.parent, bww__yia, yysw__kvrm
                )
            frwx__yyxji.decref(yysw__kvrm)
            frwx__yyxji.decref(bww__yia)
            frwx__yyxji.gil_release(ihycp__puf)
        return wwaoj__xqyf
    jhd__udg = DataFrameType(els__rlxk, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(jhd__udg, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    yqf__vxy = len(pyval.columns)
    dsd__knsd = []
    for i in range(yqf__vxy):
        chce__ehj = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            yysw__kvrm = chce__ehj.array
        else:
            yysw__kvrm = chce__ehj.values
        dsd__knsd.append(yysw__kvrm)
    dsd__knsd = tuple(dsd__knsd)
    if df_type.is_table_format:
        ebjzl__gequt = context.get_constant_generic(builder, df_type.
            table_type, Table(dsd__knsd))
        data_tup = lir.Constant.literal_struct([ebjzl__gequt])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], fityt__ugtkb) for
            i, fityt__ugtkb in enumerate(dsd__knsd)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    qihf__daaoy = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, qihf__daaoy])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    apm__vbx = context.get_constant(types.int64, -1)
    smsfe__biit = context.get_constant_null(types.voidptr)
    drq__ssa = lir.Constant.literal_struct([apm__vbx, smsfe__biit,
        smsfe__biit, payload, apm__vbx])
    drq__ssa = cgutils.global_constant(builder, '.const.meminfo', drq__ssa
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([drq__ssa, qihf__daaoy])


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
        vnon__aizen = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        vnon__aizen = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, vnon__aizen)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        vvz__ays = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                vvz__ays)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), vvz__ays)
    elif not fromty.is_table_format and toty.is_table_format:
        vvz__ays = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        vvz__ays = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        vvz__ays = _cast_df_data_keep_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    else:
        vvz__ays = _cast_df_data_keep_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, vvz__ays,
        vnon__aizen, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    bre__pqc = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        kcfn__uiecp = get_index_data_arr_types(toty.index)[0]
        nne__lokqm = bodo.utils.transform.get_type_alloc_counts(kcfn__uiecp
            ) - 1
        vgo__wrf = ', '.join('0' for huesb__nmst in range(nne__lokqm))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(vgo__wrf, ', ' if nne__lokqm == 1 else ''))
        bre__pqc['index_arr_type'] = kcfn__uiecp
    tjx__tqpd = []
    for i, arr_typ in enumerate(toty.data):
        nne__lokqm = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        vgo__wrf = ', '.join('0' for huesb__nmst in range(nne__lokqm))
        oooga__vvr = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, vgo__wrf, ', ' if nne__lokqm == 1 else ''))
        tjx__tqpd.append(oooga__vvr)
        bre__pqc[f'arr_type{i}'] = arr_typ
    tjx__tqpd = ', '.join(tjx__tqpd)
    eau__ossh = 'def impl():\n'
    etj__kvzg = bodo.hiframes.dataframe_impl._gen_init_df(eau__ossh, toty.
        columns, tjx__tqpd, index, bre__pqc)
    df = context.compile_internal(builder, etj__kvzg, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    gyf__bbpv = toty.table_type
    ebjzl__gequt = cgutils.create_struct_proxy(gyf__bbpv)(context, builder)
    ebjzl__gequt.parent = in_dataframe_payload.parent
    for tssga__llgq, qdhx__fnk in gyf__bbpv.type_to_blk.items():
        wnrls__ejj = context.get_constant(types.int64, len(gyf__bbpv.
            block_to_arr_ind[qdhx__fnk]))
        huesb__nmst, oqau__psdc = ListInstance.allocate_ex(context, builder,
            types.List(tssga__llgq), wnrls__ejj)
        oqau__psdc.size = wnrls__ejj
        setattr(ebjzl__gequt, f'block_{qdhx__fnk}', oqau__psdc.value)
    for i, tssga__llgq in enumerate(fromty.data):
        ioc__nlby = toty.data[i]
        if tssga__llgq != ioc__nlby:
            sjm__ggk = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*sjm__ggk)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ttaf__sbku = builder.extract_value(in_dataframe_payload.data, i)
        if tssga__llgq != ioc__nlby:
            gma__wudjc = context.cast(builder, ttaf__sbku, tssga__llgq,
                ioc__nlby)
            rstvw__uxona = False
        else:
            gma__wudjc = ttaf__sbku
            rstvw__uxona = True
        qdhx__fnk = gyf__bbpv.type_to_blk[tssga__llgq]
        kkt__hnuz = getattr(ebjzl__gequt, f'block_{qdhx__fnk}')
        dvt__nmtun = ListInstance(context, builder, types.List(tssga__llgq),
            kkt__hnuz)
        gqv__bln = context.get_constant(types.int64, gyf__bbpv.block_offsets[i]
            )
        dvt__nmtun.setitem(gqv__bln, gma__wudjc, rstvw__uxona)
    data_tup = context.make_tuple(builder, types.Tuple([gyf__bbpv]), [
        ebjzl__gequt._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    dsd__knsd = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            sjm__ggk = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*sjm__ggk)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            ttaf__sbku = builder.extract_value(in_dataframe_payload.data, i)
            gma__wudjc = context.cast(builder, ttaf__sbku, fromty.data[i],
                toty.data[i])
            rstvw__uxona = False
        else:
            gma__wudjc = builder.extract_value(in_dataframe_payload.data, i)
            rstvw__uxona = True
        if rstvw__uxona:
            context.nrt.incref(builder, toty.data[i], gma__wudjc)
        dsd__knsd.append(gma__wudjc)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), dsd__knsd)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    xuvog__ujbu = fromty.table_type
    dcdx__fvq = cgutils.create_struct_proxy(xuvog__ujbu)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    nwjb__vlv = toty.table_type
    hdwuu__yhdrx = cgutils.create_struct_proxy(nwjb__vlv)(context, builder)
    hdwuu__yhdrx.parent = in_dataframe_payload.parent
    for tssga__llgq, qdhx__fnk in nwjb__vlv.type_to_blk.items():
        wnrls__ejj = context.get_constant(types.int64, len(nwjb__vlv.
            block_to_arr_ind[qdhx__fnk]))
        huesb__nmst, oqau__psdc = ListInstance.allocate_ex(context, builder,
            types.List(tssga__llgq), wnrls__ejj)
        oqau__psdc.size = wnrls__ejj
        setattr(hdwuu__yhdrx, f'block_{qdhx__fnk}', oqau__psdc.value)
    for i in range(len(fromty.data)):
        qcogc__atuz = fromty.data[i]
        ioc__nlby = toty.data[i]
        if qcogc__atuz != ioc__nlby:
            sjm__ggk = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*sjm__ggk)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        prdui__qyu = xuvog__ujbu.type_to_blk[qcogc__atuz]
        okj__nlfb = getattr(dcdx__fvq, f'block_{prdui__qyu}')
        fuynr__tkdm = ListInstance(context, builder, types.List(qcogc__atuz
            ), okj__nlfb)
        kjowa__dumzx = context.get_constant(types.int64, xuvog__ujbu.
            block_offsets[i])
        ttaf__sbku = fuynr__tkdm.getitem(kjowa__dumzx)
        if qcogc__atuz != ioc__nlby:
            gma__wudjc = context.cast(builder, ttaf__sbku, qcogc__atuz,
                ioc__nlby)
            rstvw__uxona = False
        else:
            gma__wudjc = ttaf__sbku
            rstvw__uxona = True
        nvea__lcls = nwjb__vlv.type_to_blk[tssga__llgq]
        oqau__psdc = getattr(hdwuu__yhdrx, f'block_{nvea__lcls}')
        vsp__dvnd = ListInstance(context, builder, types.List(ioc__nlby),
            oqau__psdc)
        ufmpz__clw = context.get_constant(types.int64, nwjb__vlv.
            block_offsets[i])
        vsp__dvnd.setitem(ufmpz__clw, gma__wudjc, rstvw__uxona)
    data_tup = context.make_tuple(builder, types.Tuple([nwjb__vlv]), [
        hdwuu__yhdrx._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    gyf__bbpv = fromty.table_type
    ebjzl__gequt = cgutils.create_struct_proxy(gyf__bbpv)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    dsd__knsd = []
    for i, tssga__llgq in enumerate(toty.data):
        qcogc__atuz = fromty.data[i]
        if tssga__llgq != qcogc__atuz:
            sjm__ggk = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*sjm__ggk)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        qdhx__fnk = gyf__bbpv.type_to_blk[qcogc__atuz]
        kkt__hnuz = getattr(ebjzl__gequt, f'block_{qdhx__fnk}')
        dvt__nmtun = ListInstance(context, builder, types.List(qcogc__atuz),
            kkt__hnuz)
        gqv__bln = context.get_constant(types.int64, gyf__bbpv.block_offsets[i]
            )
        ttaf__sbku = dvt__nmtun.getitem(gqv__bln)
        if tssga__llgq != qcogc__atuz:
            gma__wudjc = context.cast(builder, ttaf__sbku, qcogc__atuz,
                tssga__llgq)
        else:
            gma__wudjc = ttaf__sbku
            context.nrt.incref(builder, tssga__llgq, gma__wudjc)
        dsd__knsd.append(gma__wudjc)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), dsd__knsd)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    emx__gsu, tjx__tqpd, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    kia__xco = ColNamesMetaType(tuple(emx__gsu))
    eau__ossh = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    eau__ossh += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(tjx__tqpd, index_arg))
    rvdod__chiz = {}
    exec(eau__ossh, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': kia__xco}, rvdod__chiz)
    gjk__qfjx = rvdod__chiz['_init_df']
    return gjk__qfjx


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    jhd__udg = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(jhd__udg, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    jhd__udg = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(jhd__udg, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    fighu__awgn = ''
    if not is_overload_none(dtype):
        fighu__awgn = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        yqf__vxy = (len(data.types) - 1) // 2
        qhllj__nur = [tssga__llgq.literal_value for tssga__llgq in data.
            types[1:yqf__vxy + 1]]
        data_val_types = dict(zip(qhllj__nur, data.types[yqf__vxy + 1:]))
        dsd__knsd = ['data[{}]'.format(i) for i in range(yqf__vxy + 1, 2 *
            yqf__vxy + 1)]
        data_dict = dict(zip(qhllj__nur, dsd__knsd))
        if is_overload_none(index):
            for i, tssga__llgq in enumerate(data.types[yqf__vxy + 1:]):
                if isinstance(tssga__llgq, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(yqf__vxy + 1 + i))
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
        ieqc__whghc = '.copy()' if copy else ''
        iaa__eoxj = get_overload_const_list(columns)
        yqf__vxy = len(iaa__eoxj)
        data_val_types = {cvcr__koi: data.copy(ndim=1) for cvcr__koi in
            iaa__eoxj}
        dsd__knsd = ['data[:,{}]{}'.format(i, ieqc__whghc) for i in range(
            yqf__vxy)]
        data_dict = dict(zip(iaa__eoxj, dsd__knsd))
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
    tjx__tqpd = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[cvcr__koi], df_len, fighu__awgn) for cvcr__koi in
        col_names))
    if len(col_names) == 0:
        tjx__tqpd = '()'
    return col_names, tjx__tqpd, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for cvcr__koi in col_names:
        if cvcr__koi in data_dict and is_iterable_type(data_val_types[
            cvcr__koi]):
            df_len = 'len({})'.format(data_dict[cvcr__koi])
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
    if all(cvcr__koi in data_dict for cvcr__koi in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    xxqde__cbnm = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for cvcr__koi in col_names:
        if cvcr__koi not in data_dict:
            data_dict[cvcr__koi] = xxqde__cbnm


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
            tssga__llgq = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df
                )
            return len(tssga__llgq)
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
        nxufq__qkd = idx.literal_value
        if isinstance(nxufq__qkd, int):
            huup__fgx = tup.types[nxufq__qkd]
        elif isinstance(nxufq__qkd, slice):
            huup__fgx = types.BaseTuple.from_types(tup.types[nxufq__qkd])
        return signature(huup__fgx, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    cmih__ktls, idx = sig.args
    idx = idx.literal_value
    tup, huesb__nmst = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(cmih__ktls)
        if not 0 <= idx < len(cmih__ktls):
            raise IndexError('cannot index at %d in %s' % (idx, cmih__ktls))
        dig__xjeyg = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        hnmxh__fmgjn = cgutils.unpack_tuple(builder, tup)[idx]
        dig__xjeyg = context.make_tuple(builder, sig.return_type, hnmxh__fmgjn)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, dig__xjeyg)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, qllhm__izhwr, suffix_x,
            suffix_y, is_join, indicator, huesb__nmst, huesb__nmst) = args
        how = get_overload_const_str(qllhm__izhwr)
        if how == 'cross':
            data = left_df.data + right_df.data
            columns = left_df.columns + right_df.columns
            xybt__hato = DataFrameType(data, RangeIndexType(types.none),
                columns, is_table_format=True)
            return signature(xybt__hato, *args)
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        bokut__xynl = {cvcr__koi: i for i, cvcr__koi in enumerate(left_on)}
        wagfg__luq = {cvcr__koi: i for i, cvcr__koi in enumerate(right_on)}
        knz__hkid = set(left_on) & set(right_on)
        wer__cxvkt = set(left_df.columns) & set(right_df.columns)
        gig__rrqvd = wer__cxvkt - knz__hkid
        jkvz__sqfsu = '$_bodo_index_' in left_on
        yck__gpp = '$_bodo_index_' in right_on
        wqil__ugf = how in {'left', 'outer'}
        lvqur__jpjjs = how in {'right', 'outer'}
        columns = []
        data = []
        if jkvz__sqfsu or yck__gpp:
            if jkvz__sqfsu:
                dbal__hzsm = bodo.utils.typing.get_index_data_arr_types(left_df
                    .index)[0]
            else:
                dbal__hzsm = left_df.data[left_df.column_index[left_on[0]]]
            if yck__gpp:
                qwtq__ndk = bodo.utils.typing.get_index_data_arr_types(right_df
                    .index)[0]
            else:
                qwtq__ndk = right_df.data[right_df.column_index[right_on[0]]]
        if jkvz__sqfsu and not yck__gpp and not is_join.literal_value:
            fqff__wsusn = right_on[0]
            if fqff__wsusn in left_df.column_index:
                columns.append(fqff__wsusn)
                if (qwtq__ndk == bodo.dict_str_arr_type and dbal__hzsm ==
                    bodo.string_array_type):
                    ieys__lfkr = bodo.string_array_type
                else:
                    ieys__lfkr = qwtq__ndk
                data.append(ieys__lfkr)
        if yck__gpp and not jkvz__sqfsu and not is_join.literal_value:
            jiy__ezkc = left_on[0]
            if jiy__ezkc in right_df.column_index:
                columns.append(jiy__ezkc)
                if (dbal__hzsm == bodo.dict_str_arr_type and qwtq__ndk ==
                    bodo.string_array_type):
                    ieys__lfkr = bodo.string_array_type
                else:
                    ieys__lfkr = dbal__hzsm
                data.append(ieys__lfkr)
        for qcogc__atuz, chce__ehj in zip(left_df.data, left_df.columns):
            columns.append(str(chce__ehj) + suffix_x.literal_value if 
                chce__ehj in gig__rrqvd else chce__ehj)
            if chce__ehj in knz__hkid:
                if qcogc__atuz == bodo.dict_str_arr_type:
                    qcogc__atuz = right_df.data[right_df.column_index[
                        chce__ehj]]
                data.append(qcogc__atuz)
            else:
                if (qcogc__atuz == bodo.dict_str_arr_type and chce__ehj in
                    bokut__xynl):
                    if yck__gpp:
                        qcogc__atuz = qwtq__ndk
                    else:
                        szdm__cbw = bokut__xynl[chce__ehj]
                        mkby__ijgk = right_on[szdm__cbw]
                        qcogc__atuz = right_df.data[right_df.column_index[
                            mkby__ijgk]]
                if lvqur__jpjjs:
                    qcogc__atuz = to_nullable_type(qcogc__atuz)
                data.append(qcogc__atuz)
        for qcogc__atuz, chce__ehj in zip(right_df.data, right_df.columns):
            if chce__ehj not in knz__hkid:
                columns.append(str(chce__ehj) + suffix_y.literal_value if 
                    chce__ehj in gig__rrqvd else chce__ehj)
                if (qcogc__atuz == bodo.dict_str_arr_type and chce__ehj in
                    wagfg__luq):
                    if jkvz__sqfsu:
                        qcogc__atuz = dbal__hzsm
                    else:
                        szdm__cbw = wagfg__luq[chce__ehj]
                        pbwqs__optzb = left_on[szdm__cbw]
                        qcogc__atuz = left_df.data[left_df.column_index[
                            pbwqs__optzb]]
                if wqil__ugf:
                    qcogc__atuz = to_nullable_type(qcogc__atuz)
                data.append(qcogc__atuz)
        nxgi__chg = get_overload_const_bool(indicator)
        if nxgi__chg:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        hditr__smndj = False
        if jkvz__sqfsu and yck__gpp and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            hditr__smndj = True
        elif jkvz__sqfsu and not yck__gpp:
            index_typ = right_df.index
            hditr__smndj = True
        elif yck__gpp and not jkvz__sqfsu:
            index_typ = left_df.index
            hditr__smndj = True
        if hditr__smndj and isinstance(index_typ, bodo.hiframes.
            pd_index_ext.RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        xybt__hato = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(xybt__hato, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    mot__wfb = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return mot__wfb._getvalue()


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
    wnaa__ymvhn = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    htt__lsx = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', wnaa__ymvhn, htt__lsx,
        package_name='pandas', module_name='General')
    eau__ossh = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        iho__rdlu = 0
        tjx__tqpd = []
        names = []
        for i, dzens__mxu in enumerate(objs.types):
            assert isinstance(dzens__mxu, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(dzens__mxu, 'pandas.concat()')
            if isinstance(dzens__mxu, SeriesType):
                names.append(str(iho__rdlu))
                iho__rdlu += 1
                tjx__tqpd.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(dzens__mxu.columns)
                for qiyx__dweuk in range(len(dzens__mxu.data)):
                    tjx__tqpd.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, qiyx__dweuk))
        return bodo.hiframes.dataframe_impl._gen_init_df(eau__ossh, names,
            ', '.join(tjx__tqpd), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(tssga__llgq, DataFrameType) for tssga__llgq in
            objs.types)
        oygi__asxff = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            oygi__asxff.extend(df.columns)
        oygi__asxff = list(dict.fromkeys(oygi__asxff).keys())
        uof__rbt = {}
        for iho__rdlu, cvcr__koi in enumerate(oygi__asxff):
            for i, df in enumerate(objs.types):
                if cvcr__koi in df.column_index:
                    uof__rbt[f'arr_typ{iho__rdlu}'] = df.data[df.
                        column_index[cvcr__koi]]
                    break
        assert len(uof__rbt) == len(oygi__asxff)
        aojl__lgexl = []
        for iho__rdlu, cvcr__koi in enumerate(oygi__asxff):
            args = []
            for i, df in enumerate(objs.types):
                if cvcr__koi in df.column_index:
                    zuxav__jbdet = df.column_index[cvcr__koi]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, zuxav__jbdet))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, iho__rdlu))
            eau__ossh += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(iho__rdlu, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(eau__ossh,
            oygi__asxff, ', '.join('A{}'.format(i) for i in range(len(
            oygi__asxff))), index, uof__rbt)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(tssga__llgq, SeriesType) for tssga__llgq in
            objs.types)
        eau__ossh += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            eau__ossh += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            eau__ossh += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        eau__ossh += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        rvdod__chiz = {}
        exec(eau__ossh, {'bodo': bodo, 'np': np, 'numba': numba}, rvdod__chiz)
        return rvdod__chiz['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for iho__rdlu, cvcr__koi in enumerate(df_type.columns):
            eau__ossh += '  arrs{} = []\n'.format(iho__rdlu)
            eau__ossh += '  for i in range(len(objs)):\n'
            eau__ossh += '    df = objs[i]\n'
            eau__ossh += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(iho__rdlu))
            eau__ossh += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(iho__rdlu))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            eau__ossh += '  arrs_index = []\n'
            eau__ossh += '  for i in range(len(objs)):\n'
            eau__ossh += '    df = objs[i]\n'
            eau__ossh += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(eau__ossh, df_type
            .columns, ', '.join('out_arr{}'.format(i) for i in range(len(
            df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        eau__ossh += '  arrs = []\n'
        eau__ossh += '  for i in range(len(objs)):\n'
        eau__ossh += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        eau__ossh += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            eau__ossh += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            eau__ossh += '  arrs_index = []\n'
            eau__ossh += '  for i in range(len(objs)):\n'
            eau__ossh += '    S = objs[i]\n'
            eau__ossh += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            eau__ossh += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        eau__ossh += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        rvdod__chiz = {}
        exec(eau__ossh, {'bodo': bodo, 'np': np, 'numba': numba}, rvdod__chiz)
        return rvdod__chiz['impl']
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
        jhd__udg = df.copy(index=index)
        return signature(jhd__udg, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    xcaq__rnujt = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return xcaq__rnujt._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    wnaa__ymvhn = dict(index=index, name=name)
    htt__lsx = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', wnaa__ymvhn, htt__lsx,
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
        uof__rbt = (types.Array(types.int64, 1, 'C'),) + df.data
        owtz__sawjz = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, uof__rbt)
        return signature(owtz__sawjz, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    xcaq__rnujt = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return xcaq__rnujt._getvalue()


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
    xcaq__rnujt = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return xcaq__rnujt._getvalue()


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
    xcaq__rnujt = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return xcaq__rnujt._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    rdnta__brk = get_overload_const_bool(check_duplicates)
    bpbmt__rcztb = not get_overload_const_bool(is_already_shuffled)
    qaj__xwybx = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    ksxvn__cszy = len(value_names) > 1
    jynx__iymo = None
    ewf__bsk = None
    kwtix__jnuwy = None
    igkyo__zkju = None
    jaz__uyqvm = isinstance(values_tup, types.UniTuple)
    if jaz__uyqvm:
        twx__wks = [to_str_arr_if_dict_array(to_nullable_type(values_tup.
            dtype))]
    else:
        twx__wks = [to_str_arr_if_dict_array(to_nullable_type(vjn__ssf)) for
            vjn__ssf in values_tup]
    eau__ossh = 'def impl(\n'
    eau__ossh += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    eau__ossh += '):\n'
    eau__ossh += "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n"
    if bpbmt__rcztb:
        eau__ossh += '    if parallel:\n'
        eau__ossh += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        pusx__owc = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        eau__ossh += f'        info_list = [{pusx__owc}]\n'
        eau__ossh += '        cpp_table = arr_info_list_to_table(info_list)\n'
        eau__ossh += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        qszub__pfew = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        aix__eth = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        kxhl__vng = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        eau__ossh += f'        index_tup = ({qszub__pfew},)\n'
        eau__ossh += f'        columns_tup = ({aix__eth},)\n'
        eau__ossh += f'        values_tup = ({kxhl__vng},)\n'
        eau__ossh += '        delete_table(cpp_table)\n'
        eau__ossh += '        delete_table(out_cpp_table)\n'
        eau__ossh += '        ev_shuffle.finalize()\n'
    eau__ossh += '    columns_arr = columns_tup[0]\n'
    if jaz__uyqvm:
        eau__ossh += '    values_arrs = [arr for arr in values_tup]\n'
    eau__ossh += (
        "    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)\n"
        )
    eau__ossh += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    eau__ossh += '        index_tup\n'
    eau__ossh += '    )\n'
    eau__ossh += '    n_rows = len(unique_index_arr_tup[0])\n'
    eau__ossh += '    num_values_arrays = len(values_tup)\n'
    eau__ossh += '    n_unique_pivots = len(pivot_values)\n'
    if jaz__uyqvm:
        eau__ossh += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        eau__ossh += '    n_cols = n_unique_pivots\n'
    eau__ossh += '    col_map = {}\n'
    eau__ossh += '    for i in range(n_unique_pivots):\n'
    eau__ossh += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    eau__ossh += '            raise ValueError(\n'
    eau__ossh += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    eau__ossh += '            )\n'
    eau__ossh += '        col_map[pivot_values[i]] = i\n'
    eau__ossh += '    ev_unique.finalize()\n'
    eau__ossh += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    bjkuy__mcvvo = False
    for i, qkm__dpsnp in enumerate(twx__wks):
        if is_str_arr_type(qkm__dpsnp):
            bjkuy__mcvvo = True
            eau__ossh += (
                f'    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]\n'
                )
            eau__ossh += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if bjkuy__mcvvo:
        if rdnta__brk:
            eau__ossh += '    nbytes = (n_rows + 7) >> 3\n'
            eau__ossh += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        eau__ossh += '    for i in range(len(columns_arr)):\n'
        eau__ossh += '        col_name = columns_arr[i]\n'
        eau__ossh += '        pivot_idx = col_map[col_name]\n'
        eau__ossh += '        row_idx = row_vector[i]\n'
        if rdnta__brk:
            eau__ossh += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            eau__ossh += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            eau__ossh += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            eau__ossh += '        else:\n'
            eau__ossh += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if jaz__uyqvm:
            eau__ossh += '        for j in range(num_values_arrays):\n'
            eau__ossh += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            eau__ossh += '            len_arr = len_arrs_0[col_idx]\n'
            eau__ossh += '            values_arr = values_arrs[j]\n'
            eau__ossh += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            eau__ossh += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            eau__ossh += '                len_arr[row_idx] = str_val_len\n'
            eau__ossh += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, qkm__dpsnp in enumerate(twx__wks):
                if is_str_arr_type(qkm__dpsnp):
                    eau__ossh += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    eau__ossh += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    eau__ossh += (
                        f'            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}\n'
                        )
                    eau__ossh += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    eau__ossh += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, qkm__dpsnp in enumerate(twx__wks):
        if is_str_arr_type(qkm__dpsnp):
            eau__ossh += f'    data_arrs_{i} = [\n'
            eau__ossh += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            eau__ossh += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            eau__ossh += '        )\n'
            eau__ossh += '        for i in range(n_cols)\n'
            eau__ossh += '    ]\n'
            eau__ossh += f'    if tracing.is_tracing():\n'
            eau__ossh += '         for i in range(n_cols):\n'
            eau__ossh += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            eau__ossh += f'    data_arrs_{i} = [\n'
            eau__ossh += (
                f'        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})\n'
                )
            eau__ossh += '        for _ in range(n_cols)\n'
            eau__ossh += '    ]\n'
    if not bjkuy__mcvvo and rdnta__brk:
        eau__ossh += '    nbytes = (n_rows + 7) >> 3\n'
        eau__ossh += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    eau__ossh += '    ev_alloc.finalize()\n'
    eau__ossh += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    eau__ossh += '    for i in range(len(columns_arr)):\n'
    eau__ossh += '        col_name = columns_arr[i]\n'
    eau__ossh += '        pivot_idx = col_map[col_name]\n'
    eau__ossh += '        row_idx = row_vector[i]\n'
    if not bjkuy__mcvvo and rdnta__brk:
        eau__ossh += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        eau__ossh += (
            '        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):\n'
            )
        eau__ossh += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        eau__ossh += '        else:\n'
        eau__ossh += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if jaz__uyqvm:
        eau__ossh += '        for j in range(num_values_arrays):\n'
        eau__ossh += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        eau__ossh += '            col_arr = data_arrs_0[col_idx]\n'
        eau__ossh += '            values_arr = values_arrs[j]\n'
        eau__ossh += """            bodo.libs.array_kernels.copy_array_element(col_arr, row_idx, values_arr, i)
"""
    else:
        for i, qkm__dpsnp in enumerate(twx__wks):
            eau__ossh += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            eau__ossh += f"""        bodo.libs.array_kernels.copy_array_element(col_arr_{i}, row_idx, values_tup[{i}], i)
"""
    if len(index_names) == 1:
        eau__ossh += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        jynx__iymo = index_names.meta[0]
    else:
        eau__ossh += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        jynx__iymo = tuple(index_names.meta)
    eau__ossh += f'    if tracing.is_tracing():\n'
    eau__ossh += f'        index_nbytes = index.nbytes\n'
    eau__ossh += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not qaj__xwybx:
        kwtix__jnuwy = columns_name.meta[0]
        if ksxvn__cszy:
            eau__ossh += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            ewf__bsk = value_names.meta
            if all(isinstance(cvcr__koi, str) for cvcr__koi in ewf__bsk):
                ewf__bsk = pd.array(ewf__bsk, 'string')
            elif all(isinstance(cvcr__koi, int) for cvcr__koi in ewf__bsk):
                ewf__bsk = np.array(ewf__bsk, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(ewf__bsk.dtype, pd.StringDtype):
                eau__ossh += '    total_chars = 0\n'
                eau__ossh += f'    for i in range({len(value_names)}):\n'
                eau__ossh += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                eau__ossh += '        total_chars += value_name_str_len\n'
                eau__ossh += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                eau__ossh += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                eau__ossh += '    total_chars = 0\n'
                eau__ossh += '    for i in range(len(pivot_values)):\n'
                eau__ossh += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                eau__ossh += '        total_chars += pivot_val_str_len\n'
                eau__ossh += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                eau__ossh += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            eau__ossh += f'    for i in range({len(value_names)}):\n'
            eau__ossh += '        for j in range(len(pivot_values)):\n'
            eau__ossh += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            eau__ossh += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            eau__ossh += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            eau__ossh += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    eau__ossh += '    ev_fill.finalize()\n'
    gyf__bbpv = None
    if qaj__xwybx:
        if ksxvn__cszy:
            svf__gpf = []
            for eozu__jik in _constant_pivot_values.meta:
                for rrpy__hooj in value_names.meta:
                    svf__gpf.append((eozu__jik, rrpy__hooj))
            column_names = tuple(svf__gpf)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        igkyo__zkju = ColNamesMetaType(column_names)
        brjj__qwb = []
        for vjn__ssf in twx__wks:
            brjj__qwb.extend([vjn__ssf] * len(_constant_pivot_values))
        wsqse__nmag = tuple(brjj__qwb)
        gyf__bbpv = TableType(wsqse__nmag)
        eau__ossh += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        eau__ossh += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, vjn__ssf in enumerate(twx__wks):
            eau__ossh += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {gyf__bbpv.type_to_blk[vjn__ssf]})
"""
        eau__ossh += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        eau__ossh += '        (table,), index, columns_typ\n'
        eau__ossh += '    )\n'
    else:
        snb__rlnis = ', '.join(f'data_arrs_{i}' for i in range(len(twx__wks)))
        eau__ossh += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({snb__rlnis},), n_rows)
"""
        eau__ossh += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
            )
        eau__ossh += '        (table,), index, column_index\n'
        eau__ossh += '    )\n'
    eau__ossh += '    ev.finalize()\n'
    eau__ossh += '    return result\n'
    rvdod__chiz = {}
    vpgpf__rfzh = {f'data_arr_typ_{i}': qkm__dpsnp for i, qkm__dpsnp in
        enumerate(twx__wks)}
    tek__hqn = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        gyf__bbpv, 'columns_typ': igkyo__zkju, 'index_names_lit':
        jynx__iymo, 'value_names_lit': ewf__bsk, 'columns_name_lit':
        kwtix__jnuwy, **vpgpf__rfzh, 'tracing': tracing}
    exec(eau__ossh, tek__hqn, rvdod__chiz)
    impl = rvdod__chiz['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    tnlr__ikyef = {}
    tnlr__ikyef['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, jxfb__qqn in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        ymopw__xebh = None
        if isinstance(jxfb__qqn, bodo.DatetimeArrayType):
            zeo__wvoc = 'datetimetz'
            irz__suw = 'datetime64[ns]'
            if isinstance(jxfb__qqn.tz, int):
                uhtie__cjod = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(jxfb__qqn.tz))
            else:
                uhtie__cjod = pd.DatetimeTZDtype(tz=jxfb__qqn.tz).tz
            ymopw__xebh = {'timezone': pa.lib.tzinfo_to_string(uhtie__cjod)}
        elif isinstance(jxfb__qqn, types.Array) or jxfb__qqn == boolean_array:
            zeo__wvoc = irz__suw = jxfb__qqn.dtype.name
            if irz__suw.startswith('datetime'):
                zeo__wvoc = 'datetime'
        elif is_str_arr_type(jxfb__qqn):
            zeo__wvoc = 'unicode'
            irz__suw = 'object'
        elif jxfb__qqn == binary_array_type:
            zeo__wvoc = 'bytes'
            irz__suw = 'object'
        elif isinstance(jxfb__qqn, DecimalArrayType):
            zeo__wvoc = irz__suw = 'object'
        elif isinstance(jxfb__qqn, IntegerArrayType):
            gxk__cxqhn = jxfb__qqn.dtype.name
            if gxk__cxqhn.startswith('int'):
                irz__suw = 'Int' + gxk__cxqhn[3:]
            elif gxk__cxqhn.startswith('uint'):
                irz__suw = 'UInt' + gxk__cxqhn[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, jxfb__qqn))
            zeo__wvoc = jxfb__qqn.dtype.name
        elif isinstance(jxfb__qqn, bodo.FloatingArrayType):
            gxk__cxqhn = jxfb__qqn.dtype.name
            zeo__wvoc = gxk__cxqhn
            irz__suw = gxk__cxqhn.capitalize()
        elif jxfb__qqn == datetime_date_array_type:
            zeo__wvoc = 'datetime'
            irz__suw = 'object'
        elif isinstance(jxfb__qqn, TimeArrayType):
            zeo__wvoc = 'datetime'
            irz__suw = 'object'
        elif isinstance(jxfb__qqn, (StructArrayType, ArrayItemArrayType)):
            zeo__wvoc = 'object'
            irz__suw = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, jxfb__qqn))
        fwib__poog = {'name': col_name, 'field_name': col_name,
            'pandas_type': zeo__wvoc, 'numpy_type': irz__suw, 'metadata':
            ymopw__xebh}
        tnlr__ikyef['columns'].append(fwib__poog)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            ohht__osd = '__index_level_0__'
            qwojz__pxrd = None
        else:
            ohht__osd = '%s'
            qwojz__pxrd = '%s'
        tnlr__ikyef['index_columns'] = [ohht__osd]
        tnlr__ikyef['columns'].append({'name': qwojz__pxrd, 'field_name':
            ohht__osd, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        tnlr__ikyef['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        tnlr__ikyef['index_columns'] = []
    tnlr__ikyef['pandas_version'] = pd.__version__
    return tnlr__ikyef


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
        vgl__xzbsw = []
        for pdl__gno in partition_cols:
            try:
                idx = df.columns.index(pdl__gno)
            except ValueError as mcq__gdvwa:
                raise BodoError(
                    f'Partition column {pdl__gno} is not in dataframe')
            vgl__xzbsw.append(idx)
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
    kraxc__ijfnj = isinstance(df.index, bodo.hiframes.pd_index_ext.
        RangeIndexType)
    fycog__ykdm = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not kraxc__ijfnj)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not kraxc__ijfnj or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and kraxc__ijfnj and not is_overload_true(_is_parallel)
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
        sbclz__kekdj = df.runtime_data_types
        zreid__yyd = len(sbclz__kekdj)
        ymopw__xebh = gen_pandas_parquet_metadata([''] * zreid__yyd,
            sbclz__kekdj, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        uenc__vwp = ymopw__xebh['columns'][:zreid__yyd]
        ymopw__xebh['columns'] = ymopw__xebh['columns'][zreid__yyd:]
        uenc__vwp = [json.dumps(zob__wfam).replace('""', '{0}') for
            zob__wfam in uenc__vwp]
        fpw__khdq = json.dumps(ymopw__xebh)
        spk__kcdjk = '"columns": ['
        qme__jdd = fpw__khdq.find(spk__kcdjk)
        if qme__jdd == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        jqqs__zkf = qme__jdd + len(spk__kcdjk)
        kiz__cbhv = fpw__khdq[:jqqs__zkf]
        fpw__khdq = fpw__khdq[jqqs__zkf:]
        sfbe__mvi = len(ymopw__xebh['columns'])
    else:
        fpw__khdq = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and kraxc__ijfnj:
        fpw__khdq = fpw__khdq.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            fpw__khdq = fpw__khdq.replace('"%s"', '%s')
    if not df.is_table_format:
        tjx__tqpd = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    eau__ossh = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        eau__ossh += '    py_table = get_dataframe_table(df)\n'
        eau__ossh += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        eau__ossh += '    info_list = [{}]\n'.format(tjx__tqpd)
        eau__ossh += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        eau__ossh += '    columns_index = get_dataframe_column_names(df)\n'
        eau__ossh += '    names_arr = index_to_array(columns_index)\n'
        eau__ossh += '    col_names = array_to_info(names_arr)\n'
    else:
        eau__ossh += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and fycog__ykdm:
        eau__ossh += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        bds__qav = True
    else:
        eau__ossh += '    index_col = array_to_info(np.empty(0))\n'
        bds__qav = False
    if df.has_runtime_cols:
        eau__ossh += '    columns_lst = []\n'
        eau__ossh += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            eau__ossh += f'    for _ in range(len(py_table.block_{i})):\n'
            eau__ossh += f"""        columns_lst.append({uenc__vwp[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            eau__ossh += '        num_cols += 1\n'
        if sfbe__mvi:
            eau__ossh += "    columns_lst.append('')\n"
        eau__ossh += '    columns_str = ", ".join(columns_lst)\n'
        eau__ossh += ('    metadata = """' + kiz__cbhv +
            '""" + columns_str + """' + fpw__khdq + '"""\n')
    else:
        eau__ossh += '    metadata = """' + fpw__khdq + '"""\n'
    eau__ossh += '    if compression is None:\n'
    eau__ossh += "        compression = 'none'\n"
    eau__ossh += '    if _bodo_timestamp_tz is None:\n'
    eau__ossh += "        _bodo_timestamp_tz = ''\n"
    eau__ossh += '    if df.index.name is not None:\n'
    eau__ossh += '        name_ptr = df.index.name\n'
    eau__ossh += '    else:\n'
    eau__ossh += "        name_ptr = 'null'\n"
    eau__ossh += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    qool__ljim = None
    if partition_cols:
        qool__ljim = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        pat__omni = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in vgl__xzbsw)
        if pat__omni:
            eau__ossh += '    cat_info_list = [{}]\n'.format(pat__omni)
            eau__ossh += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            eau__ossh += '    cat_table = table\n'
        eau__ossh += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        eau__ossh += (
            f'    part_cols_idxs = np.array({vgl__xzbsw}, dtype=np.int32)\n')
        eau__ossh += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        eau__ossh += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        eau__ossh += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        eau__ossh += (
            '                            unicode_to_utf8(compression),\n')
        eau__ossh += '                            _is_parallel,\n'
        eau__ossh += (
            '                            unicode_to_utf8(bucket_region),\n')
        eau__ossh += '                            row_group_size,\n'
        eau__ossh += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        eau__ossh += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        eau__ossh += '    delete_table_decref_arrays(table)\n'
        eau__ossh += '    delete_info_decref_array(index_col)\n'
        eau__ossh += '    delete_info_decref_array(col_names_no_partitions)\n'
        eau__ossh += '    delete_info_decref_array(col_names)\n'
        if pat__omni:
            eau__ossh += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        eau__ossh += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        eau__ossh += (
            '                            table, col_names, index_col,\n')
        eau__ossh += '                            ' + str(bds__qav) + ',\n'
        eau__ossh += '                            unicode_to_utf8(metadata),\n'
        eau__ossh += (
            '                            unicode_to_utf8(compression),\n')
        eau__ossh += (
            '                            _is_parallel, 1, df.index.start,\n')
        eau__ossh += (
            '                            df.index.stop, df.index.step,\n')
        eau__ossh += '                            unicode_to_utf8(name_ptr),\n'
        eau__ossh += (
            '                            unicode_to_utf8(bucket_region),\n')
        eau__ossh += '                            row_group_size,\n'
        eau__ossh += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        eau__ossh += '                              False,\n'
        eau__ossh += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        eau__ossh += '                              False)\n'
        eau__ossh += '    delete_table_decref_arrays(table)\n'
        eau__ossh += '    delete_info_decref_array(index_col)\n'
        eau__ossh += '    delete_info_decref_array(col_names)\n'
    else:
        eau__ossh += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        eau__ossh += (
            '                            table, col_names, index_col,\n')
        eau__ossh += '                            ' + str(bds__qav) + ',\n'
        eau__ossh += '                            unicode_to_utf8(metadata),\n'
        eau__ossh += (
            '                            unicode_to_utf8(compression),\n')
        eau__ossh += '                            _is_parallel, 0, 0, 0, 0,\n'
        eau__ossh += '                            unicode_to_utf8(name_ptr),\n'
        eau__ossh += (
            '                            unicode_to_utf8(bucket_region),\n')
        eau__ossh += '                            row_group_size,\n'
        eau__ossh += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        eau__ossh += '                              False,\n'
        eau__ossh += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        eau__ossh += '                              False)\n'
        eau__ossh += '    delete_table_decref_arrays(table)\n'
        eau__ossh += '    delete_info_decref_array(index_col)\n'
        eau__ossh += '    delete_info_decref_array(col_names)\n'
    rvdod__chiz = {}
    if df.has_runtime_cols:
        znogf__znpb = None
    else:
        for chce__ehj in df.columns:
            if not isinstance(chce__ehj, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        znogf__znpb = pd.array(df.columns)
    exec(eau__ossh, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': znogf__znpb,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': qool__ljim, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, rvdod__chiz)
    hkjlv__biv = rvdod__chiz['df_to_parquet']
    return hkjlv__biv


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    jqo__ddvl = tracing.Event('to_sql_exception_guard', is_parallel=
        _is_parallel)
    mgei__xufrx = 'all_ok'
    xjco__ionqs, lxgwa__bwc = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        tdn__cupkq = 100
        if chunksize is None:
            ecbi__rvs = tdn__cupkq
        else:
            ecbi__rvs = min(chunksize, tdn__cupkq)
        if _is_table_create:
            df = df.iloc[:ecbi__rvs, :]
        else:
            df = df.iloc[ecbi__rvs:, :]
            if len(df) == 0:
                return mgei__xufrx
    jqy__ybiu = df.columns
    try:
        if xjco__ionqs == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            pjli__wymj = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            ktzi__vbip = bodo.typeof(df)
            liwg__jzhfi = {}
            for cvcr__koi, vgvdz__neish in zip(ktzi__vbip.columns,
                ktzi__vbip.data):
                if df[cvcr__koi].dtype == 'object':
                    if vgvdz__neish == datetime_date_array_type:
                        liwg__jzhfi[cvcr__koi] = sa.types.Date
                    elif vgvdz__neish in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not pjli__wymj or 
                        pjli__wymj == '0'):
                        liwg__jzhfi[cvcr__koi] = VARCHAR2(4000)
            dtype = liwg__jzhfi
        try:
            cohu__pfjz = tracing.Event('df_to_sql', is_parallel=_is_parallel)
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
            cohu__pfjz.finalize()
        except Exception as byute__swflb:
            mgei__xufrx = byute__swflb.args[0]
            if xjco__ionqs == 'oracle' and 'ORA-12899' in mgei__xufrx:
                mgei__xufrx += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return mgei__xufrx
    finally:
        df.columns = jqy__ybiu
        jqo__ddvl.finalize()


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    jqo__ddvl = tracing.Event('to_sql_exception_guard_encaps', is_parallel=
        _is_parallel)
    with numba.objmode(out='unicode_type'):
        zby__tlh = tracing.Event('to_sql_exception_guard_encaps:objmode',
            is_parallel=_is_parallel)
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
        zby__tlh.finalize()
    jqo__ddvl.finalize()
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
    for chce__ehj in df.columns:
        if not isinstance(chce__ehj, str):
            raise BodoError(
                'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
    znogf__znpb = pd.array(df.columns)
    eau__ossh = """def df_to_sql(
    df, name, con,
    schema=None, if_exists='fail', index=True,
    index_label=None, chunksize=None, dtype=None,
    method=None, _bodo_allow_downcasting=False,
    _is_parallel=False,
):
"""
    eau__ossh += """    if con.startswith('iceberg'):
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
        eau__ossh += f'        py_table = get_dataframe_table(df)\n'
        eau__ossh += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        tjx__tqpd = ', '.join(f'array_to_info(get_dataframe_data(df, {i}))' for
            i in range(len(df.columns)))
        eau__ossh += f'        info_list = [{tjx__tqpd}]\n'
        eau__ossh += f'        table = arr_info_list_to_table(info_list)\n'
    eau__ossh += """        col_names = array_to_info(col_names_arr)
        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names,
            if_exists, _is_parallel, pyarrow_table_schema,
            _bodo_allow_downcasting,
        )
        delete_table_decref_arrays(table)
        delete_info_decref_array(col_names)
"""
    eau__ossh += "    elif con.startswith('snowflake'):\n"
    eau__ossh += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        if _bodo_allow_downcasting and bodo.get_rank() == 0:
            warnings.warn('_bodo_allow_downcasting is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl', sync=False)
"""
    eau__ossh += "        location = ''\n"
    if not is_overload_none(schema):
        eau__ossh += '        location += \'"\' + schema + \'".\'\n'
    eau__ossh += '        location += name\n'
    eau__ossh += '        my_rank = bodo.get_rank()\n'
    eau__ossh += """        with bodo.objmode(
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
    eau__ossh += '        bodo.barrier()\n'
    eau__ossh += '        if azure_stage_direct_upload:\n'
    eau__ossh += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    eau__ossh += '        if chunksize is None:\n'
    eau__ossh += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        eau__ossh += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        yiem__tpeo = ',' if len(df.columns) == 1 else ''
        eau__ossh += (
            f'            memory_usage = np.array(({data}{yiem__tpeo}), np.int64).sum()\n'
            )
    eau__ossh += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        eau__ossh += '        columns_index = get_dataframe_column_names(df)\n'
        eau__ossh += '        names_arr = index_to_array(columns_index)\n'
        eau__ossh += '        col_names = array_to_info(names_arr)\n'
    else:
        eau__ossh += '        col_names = array_to_info(col_names_arr)\n'
    eau__ossh += '        index_col = array_to_info(np.empty(0))\n'
    eau__ossh += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    eau__ossh += """        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           
"""
    eau__ossh += '        upload_threads_in_progress = []\n'
    eau__ossh += """        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           
"""
    eau__ossh += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    eau__ossh += '            chunk_path = parquet_path + chunk_name\n'
    eau__ossh += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    eau__ossh += (
        '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n')
    eau__ossh += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    eau__ossh += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        eau__ossh += (
            '            py_table_chunk = get_dataframe_table(chunk)\n')
        eau__ossh += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        ctjf__dip = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        eau__ossh += (
            f'            table_chunk = arr_info_list_to_table([{ctjf__dip}])     \n'
            )
    eau__ossh += '            ev_to_df_table.finalize()\n'
    eau__ossh += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
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
    eau__ossh += '        bodo.barrier()\n'
    htvv__uqa = bodo.io.snowflake.gen_snowflake_schema(df.columns, df.data)
    eau__ossh += f"""        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, {htvv__uqa},
                if_exists, old_creds, tmp_folder,
                azure_stage_direct_upload, old_core_site,
                old_sas_token,
            )
"""
    eau__ossh += '        if azure_stage_direct_upload:\n'
    eau__ossh += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    eau__ossh += '        ev.finalize()\n'
    eau__ossh += '    else:\n'
    eau__ossh += (
        '        if _bodo_allow_downcasting and bodo.get_rank() == 0:\n')
    eau__ossh += """            warnings.warn('_bodo_allow_downcasting is not supported for SQL tables.')
"""
    eau__ossh += '        rank = bodo.libs.distributed_api.get_rank()\n'
    eau__ossh += "        err_msg = 'unset'\n"
    eau__ossh += '        if rank != 0:\n'
    eau__ossh += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    eau__ossh += '        elif rank == 0:\n'
    eau__ossh += '            err_msg = to_sql_exception_guard_encaps(\n'
    eau__ossh += """                          df, name, con, schema, if_exists, index, index_label,
"""
    eau__ossh += '                          chunksize, dtype, method,\n'
    eau__ossh += '                          True, _is_parallel,\n'
    eau__ossh += '                      )\n'
    eau__ossh += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    eau__ossh += "        if_exists = 'append'\n"
    eau__ossh += "        if _is_parallel and err_msg == 'all_ok':\n"
    eau__ossh += '            err_msg = to_sql_exception_guard_encaps(\n'
    eau__ossh += """                          df, name, con, schema, if_exists, index, index_label,
"""
    eau__ossh += '                          chunksize, dtype, method,\n'
    eau__ossh += '                          False, _is_parallel,\n'
    eau__ossh += '                      )\n'
    eau__ossh += "        if err_msg != 'all_ok':\n"
    eau__ossh += "            print('err_msg=', err_msg)\n"
    eau__ossh += (
        "            raise ValueError('error in to_sql() operation')\n")
    rvdod__chiz = {}
    tek__hqn = globals().copy()
    tek__hqn.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        znogf__znpb, 'delete_info_decref_array': delete_info_decref_array,
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
    exec(eau__ossh, tek__hqn, rvdod__chiz)
    _impl = rvdod__chiz['df_to_sql']
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
        oymuj__mtk = get_overload_const_str(path_or_buf)
        if oymuj__mtk.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        fca__fpzuu = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(fca__fpzuu), unicode_to_utf8(_bodo_file_prefix)
                )
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(fca__fpzuu), unicode_to_utf8(_bodo_file_prefix)
                )
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    dhgnf__wgvj = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    nffd__bdkfs = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', dhgnf__wgvj, nffd__bdkfs,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    eau__ossh = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        ecpv__qrm = data.data.dtype.categories
        eau__ossh += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        ecpv__qrm = data.dtype.categories
        eau__ossh += '  data_values = data\n'
    yqf__vxy = len(ecpv__qrm)
    eau__ossh += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    eau__ossh += '  numba.parfors.parfor.init_prange()\n'
    eau__ossh += '  n = len(data_values)\n'
    for i in range(yqf__vxy):
        eau__ossh += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    eau__ossh += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    eau__ossh += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for qiyx__dweuk in range(yqf__vxy):
        eau__ossh += '          data_arr_{}[i] = 0\n'.format(qiyx__dweuk)
    eau__ossh += '      else:\n'
    for gyw__vfrp in range(yqf__vxy):
        eau__ossh += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            gyw__vfrp)
    tjx__tqpd = ', '.join(f'data_arr_{i}' for i in range(yqf__vxy))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(ecpv__qrm[0], np.datetime64):
        ecpv__qrm = tuple(pd.Timestamp(cvcr__koi) for cvcr__koi in ecpv__qrm)
    elif isinstance(ecpv__qrm[0], np.timedelta64):
        ecpv__qrm = tuple(pd.Timedelta(cvcr__koi) for cvcr__koi in ecpv__qrm)
    return bodo.hiframes.dataframe_impl._gen_init_df(eau__ossh, ecpv__qrm,
        tjx__tqpd, index)


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
    for zrne__fywhn in pd_unsupported:
        lqjr__idfsq = mod_name + '.' + zrne__fywhn.__name__
        overload(zrne__fywhn, no_unliteral=True)(create_unsupported_overload
            (lqjr__idfsq))


def _install_dataframe_unsupported():
    for qsskh__psi in dataframe_unsupported_attrs:
        blvxk__denu = 'DataFrame.' + qsskh__psi
        overload_attribute(DataFrameType, qsskh__psi)(
            create_unsupported_overload(blvxk__denu))
    for lqjr__idfsq in dataframe_unsupported:
        blvxk__denu = 'DataFrame.' + lqjr__idfsq + '()'
        overload_method(DataFrameType, lqjr__idfsq)(create_unsupported_overload
            (blvxk__denu))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
