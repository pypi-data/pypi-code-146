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
            fyhnu__lca = f'{len(self.data)} columns of types {set(self.data)}'
            vdjat__jzh = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            bcic__cfvhk = str(hash(super().__str__()))
            return (
                f'dataframe({fyhnu__lca}, {self.index}, {vdjat__jzh}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols}, key_hash={bcic__cfvhk})'
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
        return {afchc__nkas: i for i, afchc__nkas in enumerate(self.columns)}

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
            lse__zlv = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(wixyh__umi.unify(typingctx, yoygh__ldaxl) if 
                wixyh__umi != yoygh__ldaxl else wixyh__umi for wixyh__umi,
                yoygh__ldaxl in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if lse__zlv is not None and None not in data:
                return DataFrameType(data, lse__zlv, self.columns, dist,
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
        return all(wixyh__umi.is_precise() for wixyh__umi in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        eexhh__uwo = self.columns.index(col_name)
        zwbg__stmjt = tuple(list(self.data[:eexhh__uwo]) + [new_type] +
            list(self.data[eexhh__uwo + 1:]))
        return DataFrameType(zwbg__stmjt, self.index, self.columns, self.
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
        itkz__vqe = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            itkz__vqe.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, itkz__vqe)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        itkz__vqe = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, itkz__vqe)


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
        izlah__czkmb = 'n',
        gfcxw__njp = {'n': 5}
        breej__zxod, ilov__lhtbk = bodo.utils.typing.fold_typing_args(func_name
            , args, kws, izlah__czkmb, gfcxw__njp)
        hzci__abqo = ilov__lhtbk[0]
        if not is_overload_int(hzci__abqo):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        fmeia__kwou = df.copy()
        return fmeia__kwou(*ilov__lhtbk).replace(pysig=breej__zxod)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        jzt__zoqnm = (df,) + args
        izlah__czkmb = 'df', 'method', 'min_periods'
        gfcxw__njp = {'method': 'pearson', 'min_periods': 1}
        qqfzd__ejwm = 'method',
        breej__zxod, ilov__lhtbk = bodo.utils.typing.fold_typing_args(func_name
            , jzt__zoqnm, kws, izlah__czkmb, gfcxw__njp, qqfzd__ejwm)
        imlpj__hmsu = ilov__lhtbk[2]
        if not is_overload_int(imlpj__hmsu):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        vyob__eccjc = []
        susem__mucyl = []
        for afchc__nkas, lqu__ldva in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(lqu__ldva.dtype):
                vyob__eccjc.append(afchc__nkas)
                susem__mucyl.append(types.Array(types.float64, 1, 'A'))
        if len(vyob__eccjc) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        susem__mucyl = tuple(susem__mucyl)
        vyob__eccjc = tuple(vyob__eccjc)
        index_typ = bodo.utils.typing.type_col_to_index(vyob__eccjc)
        fmeia__kwou = DataFrameType(susem__mucyl, index_typ, vyob__eccjc)
        return fmeia__kwou(*ilov__lhtbk).replace(pysig=breej__zxod)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        ejfer__crk = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        fat__htlg = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        irorc__jtf = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        xha__xeqj = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        nazi__eenjr = dict(raw=fat__htlg, result_type=irorc__jtf)
        puldx__ecuer = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', nazi__eenjr, puldx__ecuer,
            package_name='pandas', module_name='DataFrame')
        zuv__sad = True
        if types.unliteral(ejfer__crk) == types.unicode_type:
            if not is_overload_constant_str(ejfer__crk):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            zuv__sad = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        xejt__tab = get_overload_const_int(axis)
        if zuv__sad and xejt__tab != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif xejt__tab not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        arasw__jken = []
        for arr_typ in df.data:
            oua__vthst = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            svb__rlvln = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(oua__vthst), types.int64), {}
                ).return_type
            arasw__jken.append(svb__rlvln)
        mzezj__lch = types.none
        zmq__fwkjp = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(afchc__nkas) for afchc__nkas in df.columns)
            ), None)
        jmrm__irvas = types.BaseTuple.from_types(arasw__jken)
        kicvs__lgil = types.Tuple([types.bool_] * len(jmrm__irvas))
        znr__gdpv = bodo.NullableTupleType(jmrm__irvas, kicvs__lgil)
        ump__lqhk = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if ump__lqhk == types.NPDatetime('ns'):
            ump__lqhk = bodo.pd_timestamp_tz_naive_type
        if ump__lqhk == types.NPTimedelta('ns'):
            ump__lqhk = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(jmrm__irvas):
            qpg__bek = HeterogeneousSeriesType(znr__gdpv, zmq__fwkjp, ump__lqhk
                )
        else:
            qpg__bek = SeriesType(jmrm__irvas.dtype, znr__gdpv, zmq__fwkjp,
                ump__lqhk)
        dvfc__jrau = qpg__bek,
        if xha__xeqj is not None:
            dvfc__jrau += tuple(xha__xeqj.types)
        try:
            if not zuv__sad:
                wtq__vnkjo = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(ejfer__crk), self.context,
                    'DataFrame.apply', axis if xejt__tab == 1 else None)
            else:
                wtq__vnkjo = get_const_func_output_type(ejfer__crk,
                    dvfc__jrau, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as ygdo__rkgbk:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                ygdo__rkgbk))
        if zuv__sad:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(wtq__vnkjo, (SeriesType, HeterogeneousSeriesType)
                ) and wtq__vnkjo.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(wtq__vnkjo, HeterogeneousSeriesType):
                nlbtr__gnspa, phrt__zxhvc = wtq__vnkjo.const_info
                if isinstance(wtq__vnkjo.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    dqixh__qax = wtq__vnkjo.data.tuple_typ.types
                elif isinstance(wtq__vnkjo.data, types.Tuple):
                    dqixh__qax = wtq__vnkjo.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                mjfzt__yrhjo = tuple(to_nullable_type(dtype_to_array_type(
                    vfhs__aoud)) for vfhs__aoud in dqixh__qax)
                khydz__xqjq = DataFrameType(mjfzt__yrhjo, df.index, phrt__zxhvc
                    )
            elif isinstance(wtq__vnkjo, SeriesType):
                nbz__sklm, phrt__zxhvc = wtq__vnkjo.const_info
                mjfzt__yrhjo = tuple(to_nullable_type(dtype_to_array_type(
                    wtq__vnkjo.dtype)) for nlbtr__gnspa in range(nbz__sklm))
                khydz__xqjq = DataFrameType(mjfzt__yrhjo, df.index, phrt__zxhvc
                    )
            else:
                tau__bnbhl = get_udf_out_arr_type(wtq__vnkjo)
                khydz__xqjq = SeriesType(tau__bnbhl.dtype, tau__bnbhl, df.
                    index, None)
        else:
            khydz__xqjq = wtq__vnkjo
        pbqsv__njk = ', '.join("{} = ''".format(wixyh__umi) for wixyh__umi in
            kws.keys())
        qbgen__fdnpv = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {pbqsv__njk}):
"""
        qbgen__fdnpv += '    pass\n'
        ibr__lzd = {}
        exec(qbgen__fdnpv, {}, ibr__lzd)
        bfiyl__nix = ibr__lzd['apply_stub']
        breej__zxod = numba.core.utils.pysignature(bfiyl__nix)
        npam__xor = (ejfer__crk, axis, fat__htlg, irorc__jtf, xha__xeqj
            ) + tuple(kws.values())
        return signature(khydz__xqjq, *npam__xor).replace(pysig=breej__zxod)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        izlah__czkmb = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        gfcxw__njp = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        qqfzd__ejwm = ('subplots', 'sharex', 'sharey', 'layout',
            'use_index', 'grid', 'style', 'logx', 'logy', 'loglog', 'xlim',
            'ylim', 'rot', 'colormap', 'table', 'yerr', 'xerr',
            'sort_columns', 'secondary_y', 'colorbar', 'position',
            'stacked', 'mark_right', 'include_bool', 'backend')
        breej__zxod, ilov__lhtbk = bodo.utils.typing.fold_typing_args(func_name
            , args, kws, izlah__czkmb, gfcxw__njp, qqfzd__ejwm)
        bhb__xawo = ilov__lhtbk[2]
        if not is_overload_constant_str(bhb__xawo):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        trgj__qmhjv = ilov__lhtbk[0]
        if not is_overload_none(trgj__qmhjv) and not (is_overload_int(
            trgj__qmhjv) or is_overload_constant_str(trgj__qmhjv)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(trgj__qmhjv):
            nfbdq__yyna = get_overload_const_str(trgj__qmhjv)
            if nfbdq__yyna not in df.columns:
                raise BodoError(f'{func_name}: {nfbdq__yyna} column not found.'
                    )
        elif is_overload_int(trgj__qmhjv):
            yuqcm__abct = get_overload_const_int(trgj__qmhjv)
            if yuqcm__abct > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {yuqcm__abct} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            trgj__qmhjv = df.columns[trgj__qmhjv]
        mrac__ociz = ilov__lhtbk[1]
        if not is_overload_none(mrac__ociz) and not (is_overload_int(
            mrac__ociz) or is_overload_constant_str(mrac__ociz)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(mrac__ociz):
            dbvcg__oiinw = get_overload_const_str(mrac__ociz)
            if dbvcg__oiinw not in df.columns:
                raise BodoError(
                    f'{func_name}: {dbvcg__oiinw} column not found.')
        elif is_overload_int(mrac__ociz):
            smdtd__kmig = get_overload_const_int(mrac__ociz)
            if smdtd__kmig > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {smdtd__kmig} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            mrac__ociz = df.columns[mrac__ociz]
        knb__kfra = ilov__lhtbk[3]
        if not is_overload_none(knb__kfra) and not is_tuple_like_type(knb__kfra
            ):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        mcs__eiqp = ilov__lhtbk[10]
        if not is_overload_none(mcs__eiqp) and not is_overload_constant_str(
            mcs__eiqp):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        flal__copm = ilov__lhtbk[12]
        if not is_overload_bool(flal__copm):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        rxrzh__khyu = ilov__lhtbk[17]
        if not is_overload_none(rxrzh__khyu) and not is_tuple_like_type(
            rxrzh__khyu):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        snxo__zgo = ilov__lhtbk[18]
        if not is_overload_none(snxo__zgo) and not is_tuple_like_type(snxo__zgo
            ):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        oyoq__mzw = ilov__lhtbk[22]
        if not is_overload_none(oyoq__mzw) and not is_overload_int(oyoq__mzw):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        uzq__bwsf = ilov__lhtbk[29]
        if not is_overload_none(uzq__bwsf) and not is_overload_constant_str(
            uzq__bwsf):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        skeum__liu = ilov__lhtbk[30]
        if not is_overload_none(skeum__liu) and not is_overload_constant_str(
            skeum__liu):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        vvqx__ezyeh = types.List(types.mpl_line_2d_type)
        bhb__xawo = get_overload_const_str(bhb__xawo)
        if bhb__xawo == 'scatter':
            if is_overload_none(trgj__qmhjv) and is_overload_none(mrac__ociz):
                raise BodoError(
                    f'{func_name}: {bhb__xawo} requires an x and y column.')
            elif is_overload_none(trgj__qmhjv):
                raise BodoError(
                    f'{func_name}: {bhb__xawo} x column is missing.')
            elif is_overload_none(mrac__ociz):
                raise BodoError(
                    f'{func_name}: {bhb__xawo} y column is missing.')
            vvqx__ezyeh = types.mpl_path_collection_type
        elif bhb__xawo != 'line':
            raise BodoError(f'{func_name}: {bhb__xawo} plot is not supported.')
        return signature(vvqx__ezyeh, *ilov__lhtbk).replace(pysig=breej__zxod)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            iinak__pew = df.columns.index(attr)
            arr_typ = df.data[iinak__pew]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            gvan__lxghs = []
            zwbg__stmjt = []
            abo__euz = False
            for i, kukk__jxjop in enumerate(df.columns):
                if kukk__jxjop[0] != attr:
                    continue
                abo__euz = True
                gvan__lxghs.append(kukk__jxjop[1] if len(kukk__jxjop) == 2 else
                    kukk__jxjop[1:])
                zwbg__stmjt.append(df.data[i])
            if abo__euz:
                return DataFrameType(tuple(zwbg__stmjt), df.index, tuple(
                    gvan__lxghs))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        rthhn__cagww = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(rthhn__cagww)
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
        unuoz__iwy = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], unuoz__iwy)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    fec__luoo = builder.module
    uqkok__bdmc = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    fbu__dizz = cgutils.get_or_insert_function(fec__luoo, uqkok__bdmc, name
        ='.dtor.df.{}'.format(df_type))
    if not fbu__dizz.is_declaration:
        return fbu__dizz
    fbu__dizz.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(fbu__dizz.append_basic_block())
    rlyy__fmie = fbu__dizz.args[0]
    bbv__ybdjc = context.get_value_type(payload_type).as_pointer()
    init__vuctw = builder.bitcast(rlyy__fmie, bbv__ybdjc)
    payload = context.make_helper(builder, payload_type, ref=init__vuctw)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        hvsqg__ztwu = context.get_python_api(builder)
        mwu__wtzrd = hvsqg__ztwu.gil_ensure()
        hvsqg__ztwu.decref(payload.parent)
        hvsqg__ztwu.gil_release(mwu__wtzrd)
    builder.ret_void()
    return fbu__dizz


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    nlb__ligj = cgutils.create_struct_proxy(payload_type)(context, builder)
    nlb__ligj.data = data_tup
    nlb__ligj.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        nlb__ligj.columns = colnames
    whkmp__dmlz = context.get_value_type(payload_type)
    jjn__ala = context.get_abi_sizeof(whkmp__dmlz)
    qcn__qpi = define_df_dtor(context, builder, df_type, payload_type)
    slcz__kde = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jjn__ala), qcn__qpi)
    ibh__domdo = context.nrt.meminfo_data(builder, slcz__kde)
    wxci__uqtdf = builder.bitcast(ibh__domdo, whkmp__dmlz.as_pointer())
    yguwe__rap = cgutils.create_struct_proxy(df_type)(context, builder)
    yguwe__rap.meminfo = slcz__kde
    if parent is None:
        yguwe__rap.parent = cgutils.get_null_value(yguwe__rap.parent.type)
    else:
        yguwe__rap.parent = parent
        nlb__ligj.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            hvsqg__ztwu = context.get_python_api(builder)
            mwu__wtzrd = hvsqg__ztwu.gil_ensure()
            hvsqg__ztwu.incref(parent)
            hvsqg__ztwu.gil_release(mwu__wtzrd)
    builder.store(nlb__ligj._getvalue(), wxci__uqtdf)
    return yguwe__rap._getvalue()


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
        esr__rkgv = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        esr__rkgv = [vfhs__aoud for vfhs__aoud in data_typ.dtype.arr_types]
    iosmi__dte = DataFrameType(tuple(esr__rkgv + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        iqf__bhl = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return iqf__bhl
    sig = signature(iosmi__dte, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    nbz__sklm = len(data_tup_typ.types)
    if nbz__sklm == 0:
        column_names = ()
    mljbk__ugjbz = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(mljbk__ugjbz, ColNamesMetaType) and isinstance(
        mljbk__ugjbz.meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = mljbk__ugjbz.meta
    if nbz__sklm == 1 and isinstance(data_tup_typ.types[0], TableType):
        nbz__sklm = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == nbz__sklm, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    fkjl__wuojr = data_tup_typ.types
    if nbz__sklm != 0 and isinstance(data_tup_typ.types[0], TableType):
        fkjl__wuojr = data_tup_typ.types[0].arr_types
        is_table_format = True
    iosmi__dte = DataFrameType(fkjl__wuojr, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            qyh__kjmnp = cgutils.create_struct_proxy(iosmi__dte.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = qyh__kjmnp.parent
        iqf__bhl = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return iqf__bhl
    sig = signature(iosmi__dte, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        yguwe__rap = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, yguwe__rap.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        nlb__ligj = get_dataframe_payload(context, builder, df_typ, args[0])
        wwjp__htu = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[wwjp__htu]
        if df_typ.is_table_format:
            qyh__kjmnp = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(nlb__ligj.data, 0))
            iqvgy__kpun = df_typ.table_type.type_to_blk[arr_typ]
            mrk__bat = getattr(qyh__kjmnp, f'block_{iqvgy__kpun}')
            nnuto__snb = ListInstance(context, builder, types.List(arr_typ),
                mrk__bat)
            biggi__dgh = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[wwjp__htu])
            unuoz__iwy = nnuto__snb.getitem(biggi__dgh)
        else:
            unuoz__iwy = builder.extract_value(nlb__ligj.data, wwjp__htu)
        rdbax__dnbfy = cgutils.alloca_once_value(builder, unuoz__iwy)
        erroz__idcox = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, rdbax__dnbfy, erroz__idcox)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    slcz__kde = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, slcz__kde)
    bbv__ybdjc = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, bbv__ybdjc)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    iosmi__dte = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        iosmi__dte = types.Tuple([TableType(df_typ.data)])
    sig = signature(iosmi__dte, df_typ)

    def codegen(context, builder, signature, args):
        nlb__ligj = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            nlb__ligj.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        nlb__ligj = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, nlb__ligj.
            index)
    iosmi__dte = df_typ.index
    sig = signature(iosmi__dte, df_typ)
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
        fmeia__kwou = df.data[i]
        return fmeia__kwou(*args)


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
        nlb__ligj = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(nlb__ligj.data, 0))
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
    ukoc__idr = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{ukoc__idr})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        fmeia__kwou = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return fmeia__kwou(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        nlb__ligj = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, nlb__ligj.columns)
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
    jmrm__irvas = self.typemap[data_tup.name]
    if any(is_tuple_like_type(vfhs__aoud) for vfhs__aoud in jmrm__irvas.types):
        return None
    if equiv_set.has_shape(data_tup):
        ieo__gqd = equiv_set.get_shape(data_tup)
        if len(ieo__gqd) > 1:
            equiv_set.insert_equiv(*ieo__gqd)
        if len(ieo__gqd) > 0:
            zmq__fwkjp = self.typemap[index.name]
            if not isinstance(zmq__fwkjp, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(ieo__gqd[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(ieo__gqd[0], len(
                ieo__gqd)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    pgsbz__qfsh = args[0]
    data_types = self.typemap[pgsbz__qfsh.name].data
    if any(is_tuple_like_type(vfhs__aoud) for vfhs__aoud in data_types):
        return None
    if equiv_set.has_shape(pgsbz__qfsh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            pgsbz__qfsh)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    pgsbz__qfsh = args[0]
    zmq__fwkjp = self.typemap[pgsbz__qfsh.name].index
    if isinstance(zmq__fwkjp, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(pgsbz__qfsh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            pgsbz__qfsh)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    pgsbz__qfsh = args[0]
    if equiv_set.has_shape(pgsbz__qfsh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            pgsbz__qfsh), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    pgsbz__qfsh = args[0]
    if equiv_set.has_shape(pgsbz__qfsh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            pgsbz__qfsh)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    wwjp__htu = get_overload_const_int(c_ind_typ)
    if df_typ.data[wwjp__htu] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        fae__xynf, nlbtr__gnspa, rbjm__itd = args
        nlb__ligj = get_dataframe_payload(context, builder, df_typ, fae__xynf)
        if df_typ.is_table_format:
            qyh__kjmnp = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(nlb__ligj.data, 0))
            iqvgy__kpun = df_typ.table_type.type_to_blk[arr_typ]
            mrk__bat = getattr(qyh__kjmnp, f'block_{iqvgy__kpun}')
            nnuto__snb = ListInstance(context, builder, types.List(arr_typ),
                mrk__bat)
            biggi__dgh = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[wwjp__htu])
            nnuto__snb.setitem(biggi__dgh, rbjm__itd, True)
        else:
            unuoz__iwy = builder.extract_value(nlb__ligj.data, wwjp__htu)
            context.nrt.decref(builder, df_typ.data[wwjp__htu], unuoz__iwy)
            nlb__ligj.data = builder.insert_value(nlb__ligj.data, rbjm__itd,
                wwjp__htu)
            context.nrt.incref(builder, arr_typ, rbjm__itd)
        yguwe__rap = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=fae__xynf)
        payload_type = DataFramePayloadType(df_typ)
        init__vuctw = context.nrt.meminfo_data(builder, yguwe__rap.meminfo)
        bbv__ybdjc = context.get_value_type(payload_type).as_pointer()
        init__vuctw = builder.bitcast(init__vuctw, bbv__ybdjc)
        builder.store(nlb__ligj._getvalue(), init__vuctw)
        return impl_ret_borrowed(context, builder, df_typ, fae__xynf)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        vepot__ogbfo = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        eim__rey = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=vepot__ogbfo)
        xhblq__xxgew = get_dataframe_payload(context, builder, df_typ,
            vepot__ogbfo)
        yguwe__rap = construct_dataframe(context, builder, signature.
            return_type, xhblq__xxgew.data, index_val, eim__rey.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), xhblq__xxgew.data)
        return yguwe__rap
    iosmi__dte = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(iosmi__dte, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    nbz__sklm = len(df_type.columns)
    tlctj__dal = nbz__sklm
    gja__rbh = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    xtlg__fqc = col_name not in df_type.columns
    wwjp__htu = nbz__sklm
    if xtlg__fqc:
        gja__rbh += arr_type,
        column_names += col_name,
        tlctj__dal += 1
    else:
        wwjp__htu = df_type.columns.index(col_name)
        gja__rbh = tuple(arr_type if i == wwjp__htu else gja__rbh[i] for i in
            range(nbz__sklm))

    def codegen(context, builder, signature, args):
        fae__xynf, nlbtr__gnspa, rbjm__itd = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, fae__xynf)
        mmdn__hnu = cgutils.create_struct_proxy(df_type)(context, builder,
            value=fae__xynf)
        if df_type.is_table_format:
            skyvt__zskgv = df_type.table_type
            vfe__ywdo = builder.extract_value(in_dataframe_payload.data, 0)
            mhm__zma = TableType(gja__rbh)
            ytrt__tug = set_table_data_codegen(context, builder,
                skyvt__zskgv, vfe__ywdo, mhm__zma, arr_type, rbjm__itd,
                wwjp__htu, xtlg__fqc)
            data_tup = context.make_tuple(builder, types.Tuple([mhm__zma]),
                [ytrt__tug])
        else:
            fkjl__wuojr = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != wwjp__htu else rbjm__itd) for i in range(nbz__sklm)]
            if xtlg__fqc:
                fkjl__wuojr.append(rbjm__itd)
            for pgsbz__qfsh, ummy__ptnvk in zip(fkjl__wuojr, gja__rbh):
                context.nrt.incref(builder, ummy__ptnvk, pgsbz__qfsh)
            data_tup = context.make_tuple(builder, types.Tuple(gja__rbh),
                fkjl__wuojr)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        ovt__lpl = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, mmdn__hnu.parent, None)
        if not xtlg__fqc and arr_type == df_type.data[wwjp__htu]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            init__vuctw = context.nrt.meminfo_data(builder, mmdn__hnu.meminfo)
            bbv__ybdjc = context.get_value_type(payload_type).as_pointer()
            init__vuctw = builder.bitcast(init__vuctw, bbv__ybdjc)
            orbg__qicri = get_dataframe_payload(context, builder, df_type,
                ovt__lpl)
            builder.store(orbg__qicri._getvalue(), init__vuctw)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, mhm__zma, builder.extract_value
                    (data_tup, 0))
            else:
                for pgsbz__qfsh, ummy__ptnvk in zip(fkjl__wuojr, gja__rbh):
                    context.nrt.incref(builder, ummy__ptnvk, pgsbz__qfsh)
        has_parent = cgutils.is_not_null(builder, mmdn__hnu.parent)
        with builder.if_then(has_parent):
            hvsqg__ztwu = context.get_python_api(builder)
            mwu__wtzrd = hvsqg__ztwu.gil_ensure()
            cmh__fpgn = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, rbjm__itd)
            afchc__nkas = numba.core.pythonapi._BoxContext(context, builder,
                hvsqg__ztwu, cmh__fpgn)
            bvse__pjutd = afchc__nkas.pyapi.from_native_value(arr_type,
                rbjm__itd, afchc__nkas.env_manager)
            if isinstance(col_name, str):
                noz__xymlz = context.insert_const_string(builder.module,
                    col_name)
                axazv__gkqrt = hvsqg__ztwu.string_from_string(noz__xymlz)
            else:
                assert isinstance(col_name, int)
                axazv__gkqrt = hvsqg__ztwu.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            hvsqg__ztwu.object_setitem(mmdn__hnu.parent, axazv__gkqrt,
                bvse__pjutd)
            hvsqg__ztwu.decref(bvse__pjutd)
            hvsqg__ztwu.decref(axazv__gkqrt)
            hvsqg__ztwu.gil_release(mwu__wtzrd)
        return ovt__lpl
    iosmi__dte = DataFrameType(gja__rbh, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(iosmi__dte, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    nbz__sklm = len(pyval.columns)
    fkjl__wuojr = []
    for i in range(nbz__sklm):
        bmy__grwbq = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            bvse__pjutd = bmy__grwbq.array
        else:
            bvse__pjutd = bmy__grwbq.values
        fkjl__wuojr.append(bvse__pjutd)
    fkjl__wuojr = tuple(fkjl__wuojr)
    if df_type.is_table_format:
        qyh__kjmnp = context.get_constant_generic(builder, df_type.
            table_type, Table(fkjl__wuojr))
        data_tup = lir.Constant.literal_struct([qyh__kjmnp])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], kukk__jxjop) for
            i, kukk__jxjop in enumerate(fkjl__wuojr)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    itxo__hyyl = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, itxo__hyyl])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    bcbj__vduz = context.get_constant(types.int64, -1)
    fpq__dnbmq = context.get_constant_null(types.voidptr)
    slcz__kde = lir.Constant.literal_struct([bcbj__vduz, fpq__dnbmq,
        fpq__dnbmq, payload, bcbj__vduz])
    slcz__kde = cgutils.global_constant(builder, '.const.meminfo', slcz__kde
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([slcz__kde, itxo__hyyl])


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
        lse__zlv = context.cast(builder, in_dataframe_payload.index, fromty
            .index, toty.index)
    else:
        lse__zlv = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, lse__zlv)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        zwbg__stmjt = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                zwbg__stmjt)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), zwbg__stmjt)
    elif not fromty.is_table_format and toty.is_table_format:
        zwbg__stmjt = _cast_df_data_to_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        zwbg__stmjt = _cast_df_data_to_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        zwbg__stmjt = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        zwbg__stmjt = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, zwbg__stmjt,
        lse__zlv, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    vtz__lar = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        bqihg__cwq = get_index_data_arr_types(toty.index)[0]
        gzu__sxcs = bodo.utils.transform.get_type_alloc_counts(bqihg__cwq) - 1
        nug__qjzw = ', '.join('0' for nlbtr__gnspa in range(gzu__sxcs))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(nug__qjzw, ', ' if gzu__sxcs == 1 else ''))
        vtz__lar['index_arr_type'] = bqihg__cwq
    upvht__larf = []
    for i, arr_typ in enumerate(toty.data):
        gzu__sxcs = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        nug__qjzw = ', '.join('0' for nlbtr__gnspa in range(gzu__sxcs))
        vmwci__ofon = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'
            .format(i, nug__qjzw, ', ' if gzu__sxcs == 1 else ''))
        upvht__larf.append(vmwci__ofon)
        vtz__lar[f'arr_type{i}'] = arr_typ
    upvht__larf = ', '.join(upvht__larf)
    qbgen__fdnpv = 'def impl():\n'
    pezo__fkn = bodo.hiframes.dataframe_impl._gen_init_df(qbgen__fdnpv,
        toty.columns, upvht__larf, index, vtz__lar)
    df = context.compile_internal(builder, pezo__fkn, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    gxspo__vgw = toty.table_type
    qyh__kjmnp = cgutils.create_struct_proxy(gxspo__vgw)(context, builder)
    qyh__kjmnp.parent = in_dataframe_payload.parent
    for vfhs__aoud, iqvgy__kpun in gxspo__vgw.type_to_blk.items():
        nand__oqyi = context.get_constant(types.int64, len(gxspo__vgw.
            block_to_arr_ind[iqvgy__kpun]))
        nlbtr__gnspa, lnf__sjup = ListInstance.allocate_ex(context, builder,
            types.List(vfhs__aoud), nand__oqyi)
        lnf__sjup.size = nand__oqyi
        setattr(qyh__kjmnp, f'block_{iqvgy__kpun}', lnf__sjup.value)
    for i, vfhs__aoud in enumerate(fromty.data):
        gts__zgr = toty.data[i]
        if vfhs__aoud != gts__zgr:
            guuda__idw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*guuda__idw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        unuoz__iwy = builder.extract_value(in_dataframe_payload.data, i)
        if vfhs__aoud != gts__zgr:
            rovwq__lmy = context.cast(builder, unuoz__iwy, vfhs__aoud, gts__zgr
                )
            ell__dfvw = False
        else:
            rovwq__lmy = unuoz__iwy
            ell__dfvw = True
        iqvgy__kpun = gxspo__vgw.type_to_blk[vfhs__aoud]
        mrk__bat = getattr(qyh__kjmnp, f'block_{iqvgy__kpun}')
        nnuto__snb = ListInstance(context, builder, types.List(vfhs__aoud),
            mrk__bat)
        biggi__dgh = context.get_constant(types.int64, gxspo__vgw.
            block_offsets[i])
        nnuto__snb.setitem(biggi__dgh, rovwq__lmy, ell__dfvw)
    data_tup = context.make_tuple(builder, types.Tuple([gxspo__vgw]), [
        qyh__kjmnp._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    fkjl__wuojr = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            guuda__idw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*guuda__idw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            unuoz__iwy = builder.extract_value(in_dataframe_payload.data, i)
            rovwq__lmy = context.cast(builder, unuoz__iwy, fromty.data[i],
                toty.data[i])
            ell__dfvw = False
        else:
            rovwq__lmy = builder.extract_value(in_dataframe_payload.data, i)
            ell__dfvw = True
        if ell__dfvw:
            context.nrt.incref(builder, toty.data[i], rovwq__lmy)
        fkjl__wuojr.append(rovwq__lmy)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), fkjl__wuojr)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    skyvt__zskgv = fromty.table_type
    vfe__ywdo = cgutils.create_struct_proxy(skyvt__zskgv)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    mhm__zma = toty.table_type
    ytrt__tug = cgutils.create_struct_proxy(mhm__zma)(context, builder)
    ytrt__tug.parent = in_dataframe_payload.parent
    for vfhs__aoud, iqvgy__kpun in mhm__zma.type_to_blk.items():
        nand__oqyi = context.get_constant(types.int64, len(mhm__zma.
            block_to_arr_ind[iqvgy__kpun]))
        nlbtr__gnspa, lnf__sjup = ListInstance.allocate_ex(context, builder,
            types.List(vfhs__aoud), nand__oqyi)
        lnf__sjup.size = nand__oqyi
        setattr(ytrt__tug, f'block_{iqvgy__kpun}', lnf__sjup.value)
    for i in range(len(fromty.data)):
        xzi__vlxsq = fromty.data[i]
        gts__zgr = toty.data[i]
        if xzi__vlxsq != gts__zgr:
            guuda__idw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*guuda__idw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ete__lwnlb = skyvt__zskgv.type_to_blk[xzi__vlxsq]
        ddx__ovlbf = getattr(vfe__ywdo, f'block_{ete__lwnlb}')
        flbqo__htu = ListInstance(context, builder, types.List(xzi__vlxsq),
            ddx__ovlbf)
        bxt__jtcnk = context.get_constant(types.int64, skyvt__zskgv.
            block_offsets[i])
        unuoz__iwy = flbqo__htu.getitem(bxt__jtcnk)
        if xzi__vlxsq != gts__zgr:
            rovwq__lmy = context.cast(builder, unuoz__iwy, xzi__vlxsq, gts__zgr
                )
            ell__dfvw = False
        else:
            rovwq__lmy = unuoz__iwy
            ell__dfvw = True
        irt__ttzhy = mhm__zma.type_to_blk[vfhs__aoud]
        lnf__sjup = getattr(ytrt__tug, f'block_{irt__ttzhy}')
        jpxf__mzigo = ListInstance(context, builder, types.List(gts__zgr),
            lnf__sjup)
        nqpfd__civ = context.get_constant(types.int64, mhm__zma.
            block_offsets[i])
        jpxf__mzigo.setitem(nqpfd__civ, rovwq__lmy, ell__dfvw)
    data_tup = context.make_tuple(builder, types.Tuple([mhm__zma]), [
        ytrt__tug._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    gxspo__vgw = fromty.table_type
    qyh__kjmnp = cgutils.create_struct_proxy(gxspo__vgw)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    fkjl__wuojr = []
    for i, vfhs__aoud in enumerate(toty.data):
        xzi__vlxsq = fromty.data[i]
        if vfhs__aoud != xzi__vlxsq:
            guuda__idw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*guuda__idw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        iqvgy__kpun = gxspo__vgw.type_to_blk[xzi__vlxsq]
        mrk__bat = getattr(qyh__kjmnp, f'block_{iqvgy__kpun}')
        nnuto__snb = ListInstance(context, builder, types.List(xzi__vlxsq),
            mrk__bat)
        biggi__dgh = context.get_constant(types.int64, gxspo__vgw.
            block_offsets[i])
        unuoz__iwy = nnuto__snb.getitem(biggi__dgh)
        if vfhs__aoud != xzi__vlxsq:
            rovwq__lmy = context.cast(builder, unuoz__iwy, xzi__vlxsq,
                vfhs__aoud)
        else:
            rovwq__lmy = unuoz__iwy
            context.nrt.incref(builder, vfhs__aoud, rovwq__lmy)
        fkjl__wuojr.append(rovwq__lmy)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), fkjl__wuojr)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    dqw__onne, upvht__larf, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    ywkpn__mucb = ColNamesMetaType(tuple(dqw__onne))
    qbgen__fdnpv = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    qbgen__fdnpv += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(upvht__larf, index_arg))
    ibr__lzd = {}
    exec(qbgen__fdnpv, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': ywkpn__mucb}, ibr__lzd)
    nbn__yxozg = ibr__lzd['_init_df']
    return nbn__yxozg


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    iosmi__dte = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(iosmi__dte, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    iosmi__dte = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(iosmi__dte, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    vsr__xrwz = ''
    if not is_overload_none(dtype):
        vsr__xrwz = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        nbz__sklm = (len(data.types) - 1) // 2
        zduz__nyvus = [vfhs__aoud.literal_value for vfhs__aoud in data.
            types[1:nbz__sklm + 1]]
        data_val_types = dict(zip(zduz__nyvus, data.types[nbz__sklm + 1:]))
        fkjl__wuojr = ['data[{}]'.format(i) for i in range(nbz__sklm + 1, 2 *
            nbz__sklm + 1)]
        data_dict = dict(zip(zduz__nyvus, fkjl__wuojr))
        if is_overload_none(index):
            for i, vfhs__aoud in enumerate(data.types[nbz__sklm + 1:]):
                if isinstance(vfhs__aoud, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(nbz__sklm + 1 + i))
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
        fzkn__uqo = '.copy()' if copy else ''
        iewto__qwvo = get_overload_const_list(columns)
        nbz__sklm = len(iewto__qwvo)
        data_val_types = {afchc__nkas: data.copy(ndim=1) for afchc__nkas in
            iewto__qwvo}
        fkjl__wuojr = ['data[:,{}]{}'.format(i, fzkn__uqo) for i in range(
            nbz__sklm)]
        data_dict = dict(zip(iewto__qwvo, fkjl__wuojr))
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
    upvht__larf = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[afchc__nkas], df_len, vsr__xrwz) for afchc__nkas in
        col_names))
    if len(col_names) == 0:
        upvht__larf = '()'
    return col_names, upvht__larf, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for afchc__nkas in col_names:
        if afchc__nkas in data_dict and is_iterable_type(data_val_types[
            afchc__nkas]):
            df_len = 'len({})'.format(data_dict[afchc__nkas])
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
    if all(afchc__nkas in data_dict for afchc__nkas in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    dghao__llcnh = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len
        , dtype)
    for afchc__nkas in col_names:
        if afchc__nkas not in data_dict:
            data_dict[afchc__nkas] = dghao__llcnh


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
            vfhs__aoud = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(vfhs__aoud)
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
        zgi__tqwx = idx.literal_value
        if isinstance(zgi__tqwx, int):
            fmeia__kwou = tup.types[zgi__tqwx]
        elif isinstance(zgi__tqwx, slice):
            fmeia__kwou = types.BaseTuple.from_types(tup.types[zgi__tqwx])
        return signature(fmeia__kwou, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    xwiot__xhxfg, idx = sig.args
    idx = idx.literal_value
    tup, nlbtr__gnspa = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(xwiot__xhxfg)
        if not 0 <= idx < len(xwiot__xhxfg):
            raise IndexError('cannot index at %d in %s' % (idx, xwiot__xhxfg))
        yskt__kqtgv = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        wnjl__pgor = cgutils.unpack_tuple(builder, tup)[idx]
        yskt__kqtgv = context.make_tuple(builder, sig.return_type, wnjl__pgor)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, yskt__kqtgv)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, anw__unwmd, suffix_x,
            suffix_y, is_join, indicator, nlbtr__gnspa, nlbtr__gnspa) = args
        how = get_overload_const_str(anw__unwmd)
        if how == 'cross':
            data = left_df.data + right_df.data
            columns = left_df.columns + right_df.columns
            ohha__tbhpy = DataFrameType(data, RangeIndexType(types.none),
                columns, is_table_format=True)
            return signature(ohha__tbhpy, *args)
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        dolh__glpv = {afchc__nkas: i for i, afchc__nkas in enumerate(left_on)}
        naz__qoel = {afchc__nkas: i for i, afchc__nkas in enumerate(right_on)}
        fzkfy__qcux = set(left_on) & set(right_on)
        ioyxt__rcsm = set(left_df.columns) & set(right_df.columns)
        nembr__aqjgo = ioyxt__rcsm - fzkfy__qcux
        mkvth__gnlr = '$_bodo_index_' in left_on
        zgf__hozh = '$_bodo_index_' in right_on
        udds__adhd = how in {'left', 'outer'}
        mlel__kejkt = how in {'right', 'outer'}
        columns = []
        data = []
        if mkvth__gnlr or zgf__hozh:
            if mkvth__gnlr:
                zsyv__vbcsz = bodo.utils.typing.get_index_data_arr_types(
                    left_df.index)[0]
            else:
                zsyv__vbcsz = left_df.data[left_df.column_index[left_on[0]]]
            if zgf__hozh:
                olz__zls = bodo.utils.typing.get_index_data_arr_types(right_df
                    .index)[0]
            else:
                olz__zls = right_df.data[right_df.column_index[right_on[0]]]
        if mkvth__gnlr and not zgf__hozh and not is_join.literal_value:
            tufzn__bnm = right_on[0]
            if tufzn__bnm in left_df.column_index:
                columns.append(tufzn__bnm)
                if (olz__zls == bodo.dict_str_arr_type and zsyv__vbcsz ==
                    bodo.string_array_type):
                    tjb__zkaed = bodo.string_array_type
                else:
                    tjb__zkaed = olz__zls
                data.append(tjb__zkaed)
        if zgf__hozh and not mkvth__gnlr and not is_join.literal_value:
            obwfh__hxk = left_on[0]
            if obwfh__hxk in right_df.column_index:
                columns.append(obwfh__hxk)
                if (zsyv__vbcsz == bodo.dict_str_arr_type and olz__zls ==
                    bodo.string_array_type):
                    tjb__zkaed = bodo.string_array_type
                else:
                    tjb__zkaed = zsyv__vbcsz
                data.append(tjb__zkaed)
        for xzi__vlxsq, bmy__grwbq in zip(left_df.data, left_df.columns):
            columns.append(str(bmy__grwbq) + suffix_x.literal_value if 
                bmy__grwbq in nembr__aqjgo else bmy__grwbq)
            if bmy__grwbq in fzkfy__qcux:
                if xzi__vlxsq == bodo.dict_str_arr_type:
                    xzi__vlxsq = right_df.data[right_df.column_index[
                        bmy__grwbq]]
                data.append(xzi__vlxsq)
            else:
                if (xzi__vlxsq == bodo.dict_str_arr_type and bmy__grwbq in
                    dolh__glpv):
                    if zgf__hozh:
                        xzi__vlxsq = olz__zls
                    else:
                        zrxgs__wjc = dolh__glpv[bmy__grwbq]
                        bmia__ievb = right_on[zrxgs__wjc]
                        xzi__vlxsq = right_df.data[right_df.column_index[
                            bmia__ievb]]
                if mlel__kejkt:
                    xzi__vlxsq = to_nullable_type(xzi__vlxsq)
                data.append(xzi__vlxsq)
        for xzi__vlxsq, bmy__grwbq in zip(right_df.data, right_df.columns):
            if bmy__grwbq not in fzkfy__qcux:
                columns.append(str(bmy__grwbq) + suffix_y.literal_value if 
                    bmy__grwbq in nembr__aqjgo else bmy__grwbq)
                if (xzi__vlxsq == bodo.dict_str_arr_type and bmy__grwbq in
                    naz__qoel):
                    if mkvth__gnlr:
                        xzi__vlxsq = zsyv__vbcsz
                    else:
                        zrxgs__wjc = naz__qoel[bmy__grwbq]
                        kflga__pbais = left_on[zrxgs__wjc]
                        xzi__vlxsq = left_df.data[left_df.column_index[
                            kflga__pbais]]
                if udds__adhd:
                    xzi__vlxsq = to_nullable_type(xzi__vlxsq)
                data.append(xzi__vlxsq)
        ihvdb__vuj = get_overload_const_bool(indicator)
        if ihvdb__vuj:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        rfita__dysp = False
        if mkvth__gnlr and zgf__hozh and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            rfita__dysp = True
        elif mkvth__gnlr and not zgf__hozh:
            index_typ = right_df.index
            rfita__dysp = True
        elif zgf__hozh and not mkvth__gnlr:
            index_typ = left_df.index
            rfita__dysp = True
        if rfita__dysp and isinstance(index_typ, bodo.hiframes.pd_index_ext
            .RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        ohha__tbhpy = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(ohha__tbhpy, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    yguwe__rap = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return yguwe__rap._getvalue()


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
    nazi__eenjr = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    gfcxw__njp = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', nazi__eenjr, gfcxw__njp,
        package_name='pandas', module_name='General')
    qbgen__fdnpv = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        tiap__irsrf = 0
        upvht__larf = []
        names = []
        for i, rqdqd__bgfz in enumerate(objs.types):
            assert isinstance(rqdqd__bgfz, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(rqdqd__bgfz, 'pandas.concat()')
            if isinstance(rqdqd__bgfz, SeriesType):
                names.append(str(tiap__irsrf))
                tiap__irsrf += 1
                upvht__larf.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(rqdqd__bgfz.columns)
                for mmxl__shhew in range(len(rqdqd__bgfz.data)):
                    upvht__larf.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, mmxl__shhew))
        return bodo.hiframes.dataframe_impl._gen_init_df(qbgen__fdnpv,
            names, ', '.join(upvht__larf), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(vfhs__aoud, DataFrameType) for vfhs__aoud in
            objs.types)
        ooh__ago = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            ooh__ago.extend(df.columns)
        ooh__ago = list(dict.fromkeys(ooh__ago).keys())
        esr__rkgv = {}
        for tiap__irsrf, afchc__nkas in enumerate(ooh__ago):
            for i, df in enumerate(objs.types):
                if afchc__nkas in df.column_index:
                    esr__rkgv[f'arr_typ{tiap__irsrf}'] = df.data[df.
                        column_index[afchc__nkas]]
                    break
        assert len(esr__rkgv) == len(ooh__ago)
        oos__ejiqi = []
        for tiap__irsrf, afchc__nkas in enumerate(ooh__ago):
            args = []
            for i, df in enumerate(objs.types):
                if afchc__nkas in df.column_index:
                    wwjp__htu = df.column_index[afchc__nkas]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, wwjp__htu))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, tiap__irsrf))
            qbgen__fdnpv += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(tiap__irsrf, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(qbgen__fdnpv,
            ooh__ago, ', '.join('A{}'.format(i) for i in range(len(ooh__ago
            ))), index, esr__rkgv)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(vfhs__aoud, SeriesType) for vfhs__aoud in
            objs.types)
        qbgen__fdnpv += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            qbgen__fdnpv += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            qbgen__fdnpv += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        qbgen__fdnpv += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        ibr__lzd = {}
        exec(qbgen__fdnpv, {'bodo': bodo, 'np': np, 'numba': numba}, ibr__lzd)
        return ibr__lzd['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for tiap__irsrf, afchc__nkas in enumerate(df_type.columns):
            qbgen__fdnpv += '  arrs{} = []\n'.format(tiap__irsrf)
            qbgen__fdnpv += '  for i in range(len(objs)):\n'
            qbgen__fdnpv += '    df = objs[i]\n'
            qbgen__fdnpv += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(tiap__irsrf))
            qbgen__fdnpv += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(tiap__irsrf))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            qbgen__fdnpv += '  arrs_index = []\n'
            qbgen__fdnpv += '  for i in range(len(objs)):\n'
            qbgen__fdnpv += '    df = objs[i]\n'
            qbgen__fdnpv += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(qbgen__fdnpv,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        qbgen__fdnpv += '  arrs = []\n'
        qbgen__fdnpv += '  for i in range(len(objs)):\n'
        qbgen__fdnpv += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        qbgen__fdnpv += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            qbgen__fdnpv += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            qbgen__fdnpv += '  arrs_index = []\n'
            qbgen__fdnpv += '  for i in range(len(objs)):\n'
            qbgen__fdnpv += '    S = objs[i]\n'
            qbgen__fdnpv += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            qbgen__fdnpv += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        qbgen__fdnpv += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        ibr__lzd = {}
        exec(qbgen__fdnpv, {'bodo': bodo, 'np': np, 'numba': numba}, ibr__lzd)
        return ibr__lzd['impl']
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
        iosmi__dte = df.copy(index=index)
        return signature(iosmi__dte, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    wwv__azt = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return wwv__azt._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    nazi__eenjr = dict(index=index, name=name)
    gfcxw__njp = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', nazi__eenjr, gfcxw__njp,
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
        esr__rkgv = (types.Array(types.int64, 1, 'C'),) + df.data
        xldl__sipka = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, esr__rkgv)
        return signature(xldl__sipka, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    wwv__azt = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return wwv__azt._getvalue()


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
    wwv__azt = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return wwv__azt._getvalue()


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
    wwv__azt = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return wwv__azt._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    ylt__trm = get_overload_const_bool(check_duplicates)
    jgmrt__qojg = not get_overload_const_bool(is_already_shuffled)
    qmn__yklvy = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    gvzj__dtm = len(value_names) > 1
    oxla__ituz = None
    bvtma__yti = None
    inbbl__wfxak = None
    rstr__wib = None
    jaxh__eln = isinstance(values_tup, types.UniTuple)
    if jaxh__eln:
        bfz__mat = [to_str_arr_if_dict_array(to_nullable_type(values_tup.
            dtype))]
    else:
        bfz__mat = [to_str_arr_if_dict_array(to_nullable_type(ummy__ptnvk)) for
            ummy__ptnvk in values_tup]
    qbgen__fdnpv = 'def impl(\n'
    qbgen__fdnpv += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    qbgen__fdnpv += '):\n'
    qbgen__fdnpv += (
        "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n")
    if jgmrt__qojg:
        qbgen__fdnpv += '    if parallel:\n'
        qbgen__fdnpv += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        zidg__igga = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        qbgen__fdnpv += f'        info_list = [{zidg__igga}]\n'
        qbgen__fdnpv += (
            '        cpp_table = arr_info_list_to_table(info_list)\n')
        qbgen__fdnpv += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        qyaf__iqari = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        yqw__umxo = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        mtgm__zbjj = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        qbgen__fdnpv += f'        index_tup = ({qyaf__iqari},)\n'
        qbgen__fdnpv += f'        columns_tup = ({yqw__umxo},)\n'
        qbgen__fdnpv += f'        values_tup = ({mtgm__zbjj},)\n'
        qbgen__fdnpv += '        delete_table(cpp_table)\n'
        qbgen__fdnpv += '        delete_table(out_cpp_table)\n'
        qbgen__fdnpv += '        ev_shuffle.finalize()\n'
    qbgen__fdnpv += '    columns_arr = columns_tup[0]\n'
    if jaxh__eln:
        qbgen__fdnpv += '    values_arrs = [arr for arr in values_tup]\n'
    qbgen__fdnpv += """    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)
"""
    qbgen__fdnpv += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    qbgen__fdnpv += '        index_tup\n'
    qbgen__fdnpv += '    )\n'
    qbgen__fdnpv += '    n_rows = len(unique_index_arr_tup[0])\n'
    qbgen__fdnpv += '    num_values_arrays = len(values_tup)\n'
    qbgen__fdnpv += '    n_unique_pivots = len(pivot_values)\n'
    if jaxh__eln:
        qbgen__fdnpv += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        qbgen__fdnpv += '    n_cols = n_unique_pivots\n'
    qbgen__fdnpv += '    col_map = {}\n'
    qbgen__fdnpv += '    for i in range(n_unique_pivots):\n'
    qbgen__fdnpv += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    qbgen__fdnpv += '            raise ValueError(\n'
    qbgen__fdnpv += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    qbgen__fdnpv += '            )\n'
    qbgen__fdnpv += '        col_map[pivot_values[i]] = i\n'
    qbgen__fdnpv += '    ev_unique.finalize()\n'
    qbgen__fdnpv += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    hiia__fod = False
    for i, jzqq__sodbs in enumerate(bfz__mat):
        if is_str_arr_type(jzqq__sodbs):
            hiia__fod = True
            qbgen__fdnpv += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            qbgen__fdnpv += (
                f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n')
    if hiia__fod:
        if ylt__trm:
            qbgen__fdnpv += '    nbytes = (n_rows + 7) >> 3\n'
            qbgen__fdnpv += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        qbgen__fdnpv += '    for i in range(len(columns_arr)):\n'
        qbgen__fdnpv += '        col_name = columns_arr[i]\n'
        qbgen__fdnpv += '        pivot_idx = col_map[col_name]\n'
        qbgen__fdnpv += '        row_idx = row_vector[i]\n'
        if ylt__trm:
            qbgen__fdnpv += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            qbgen__fdnpv += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            qbgen__fdnpv += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            qbgen__fdnpv += '        else:\n'
            qbgen__fdnpv += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if jaxh__eln:
            qbgen__fdnpv += '        for j in range(num_values_arrays):\n'
            qbgen__fdnpv += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            qbgen__fdnpv += '            len_arr = len_arrs_0[col_idx]\n'
            qbgen__fdnpv += '            values_arr = values_arrs[j]\n'
            qbgen__fdnpv += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            qbgen__fdnpv += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            qbgen__fdnpv += '                len_arr[row_idx] = str_val_len\n'
            qbgen__fdnpv += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, jzqq__sodbs in enumerate(bfz__mat):
                if is_str_arr_type(jzqq__sodbs):
                    qbgen__fdnpv += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    qbgen__fdnpv += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    qbgen__fdnpv += f"""            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}
"""
                    qbgen__fdnpv += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    qbgen__fdnpv += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, jzqq__sodbs in enumerate(bfz__mat):
        if is_str_arr_type(jzqq__sodbs):
            qbgen__fdnpv += f'    data_arrs_{i} = [\n'
            qbgen__fdnpv += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            qbgen__fdnpv += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            qbgen__fdnpv += '        )\n'
            qbgen__fdnpv += '        for i in range(n_cols)\n'
            qbgen__fdnpv += '    ]\n'
            qbgen__fdnpv += f'    if tracing.is_tracing():\n'
            qbgen__fdnpv += '         for i in range(n_cols):\n'
            qbgen__fdnpv += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            qbgen__fdnpv += f'    data_arrs_{i} = [\n'
            qbgen__fdnpv += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            qbgen__fdnpv += '        for _ in range(n_cols)\n'
            qbgen__fdnpv += '    ]\n'
    if not hiia__fod and ylt__trm:
        qbgen__fdnpv += '    nbytes = (n_rows + 7) >> 3\n'
        qbgen__fdnpv += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    qbgen__fdnpv += '    ev_alloc.finalize()\n'
    qbgen__fdnpv += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    qbgen__fdnpv += '    for i in range(len(columns_arr)):\n'
    qbgen__fdnpv += '        col_name = columns_arr[i]\n'
    qbgen__fdnpv += '        pivot_idx = col_map[col_name]\n'
    qbgen__fdnpv += '        row_idx = row_vector[i]\n'
    if not hiia__fod and ylt__trm:
        qbgen__fdnpv += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        qbgen__fdnpv += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        qbgen__fdnpv += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        qbgen__fdnpv += '        else:\n'
        qbgen__fdnpv += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if jaxh__eln:
        qbgen__fdnpv += '        for j in range(num_values_arrays):\n'
        qbgen__fdnpv += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        qbgen__fdnpv += '            col_arr = data_arrs_0[col_idx]\n'
        qbgen__fdnpv += '            values_arr = values_arrs[j]\n'
        qbgen__fdnpv += """            bodo.libs.array_kernels.copy_array_element(col_arr, row_idx, values_arr, i)
"""
    else:
        for i, jzqq__sodbs in enumerate(bfz__mat):
            qbgen__fdnpv += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            qbgen__fdnpv += f"""        bodo.libs.array_kernels.copy_array_element(col_arr_{i}, row_idx, values_tup[{i}], i)
"""
    if len(index_names) == 1:
        qbgen__fdnpv += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        oxla__ituz = index_names.meta[0]
    else:
        qbgen__fdnpv += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        oxla__ituz = tuple(index_names.meta)
    qbgen__fdnpv += f'    if tracing.is_tracing():\n'
    qbgen__fdnpv += f'        index_nbytes = index.nbytes\n'
    qbgen__fdnpv += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not qmn__yklvy:
        inbbl__wfxak = columns_name.meta[0]
        if gvzj__dtm:
            qbgen__fdnpv += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            bvtma__yti = value_names.meta
            if all(isinstance(afchc__nkas, str) for afchc__nkas in bvtma__yti):
                bvtma__yti = pd.array(bvtma__yti, 'string')
            elif all(isinstance(afchc__nkas, int) for afchc__nkas in bvtma__yti
                ):
                bvtma__yti = np.array(bvtma__yti, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(bvtma__yti.dtype, pd.StringDtype):
                qbgen__fdnpv += '    total_chars = 0\n'
                qbgen__fdnpv += f'    for i in range({len(value_names)}):\n'
                qbgen__fdnpv += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                qbgen__fdnpv += '        total_chars += value_name_str_len\n'
                qbgen__fdnpv += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                qbgen__fdnpv += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                qbgen__fdnpv += '    total_chars = 0\n'
                qbgen__fdnpv += '    for i in range(len(pivot_values)):\n'
                qbgen__fdnpv += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                qbgen__fdnpv += '        total_chars += pivot_val_str_len\n'
                qbgen__fdnpv += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                qbgen__fdnpv += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            qbgen__fdnpv += f'    for i in range({len(value_names)}):\n'
            qbgen__fdnpv += '        for j in range(len(pivot_values)):\n'
            qbgen__fdnpv += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            qbgen__fdnpv += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            qbgen__fdnpv += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            qbgen__fdnpv += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    qbgen__fdnpv += '    ev_fill.finalize()\n'
    gxspo__vgw = None
    if qmn__yklvy:
        if gvzj__dtm:
            xkvp__swofx = []
            for rhpw__vuv in _constant_pivot_values.meta:
                for apz__nbeuz in value_names.meta:
                    xkvp__swofx.append((rhpw__vuv, apz__nbeuz))
            column_names = tuple(xkvp__swofx)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        rstr__wib = ColNamesMetaType(column_names)
        tgui__jcqdi = []
        for ummy__ptnvk in bfz__mat:
            tgui__jcqdi.extend([ummy__ptnvk] * len(_constant_pivot_values))
        qbkgg__vko = tuple(tgui__jcqdi)
        gxspo__vgw = TableType(qbkgg__vko)
        qbgen__fdnpv += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        qbgen__fdnpv += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, ummy__ptnvk in enumerate(bfz__mat):
            qbgen__fdnpv += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {gxspo__vgw.type_to_blk[ummy__ptnvk]})
"""
        qbgen__fdnpv += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        qbgen__fdnpv += '        (table,), index, columns_typ\n'
        qbgen__fdnpv += '    )\n'
    else:
        gtxl__plldx = ', '.join(f'data_arrs_{i}' for i in range(len(bfz__mat)))
        qbgen__fdnpv += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({gtxl__plldx},), n_rows)
"""
        qbgen__fdnpv += """    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(
"""
        qbgen__fdnpv += '        (table,), index, column_index\n'
        qbgen__fdnpv += '    )\n'
    qbgen__fdnpv += '    ev.finalize()\n'
    qbgen__fdnpv += '    return result\n'
    ibr__lzd = {}
    kdg__oyg = {f'data_arr_typ_{i}': jzqq__sodbs for i, jzqq__sodbs in
        enumerate(bfz__mat)}
    qhtsi__fyqp = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        gxspo__vgw, 'columns_typ': rstr__wib, 'index_names_lit': oxla__ituz,
        'value_names_lit': bvtma__yti, 'columns_name_lit': inbbl__wfxak, **
        kdg__oyg, 'tracing': tracing}
    exec(qbgen__fdnpv, qhtsi__fyqp, ibr__lzd)
    impl = ibr__lzd['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    oxt__urom = {}
    oxt__urom['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, dnfn__zzoni in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        ipzq__stp = None
        if isinstance(dnfn__zzoni, bodo.DatetimeArrayType):
            ssm__mhlsz = 'datetimetz'
            qopy__qsb = 'datetime64[ns]'
            if isinstance(dnfn__zzoni.tz, int):
                lxtnt__tbxu = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(dnfn__zzoni.tz))
            else:
                lxtnt__tbxu = pd.DatetimeTZDtype(tz=dnfn__zzoni.tz).tz
            ipzq__stp = {'timezone': pa.lib.tzinfo_to_string(lxtnt__tbxu)}
        elif isinstance(dnfn__zzoni, types.Array
            ) or dnfn__zzoni == boolean_array:
            ssm__mhlsz = qopy__qsb = dnfn__zzoni.dtype.name
            if qopy__qsb.startswith('datetime'):
                ssm__mhlsz = 'datetime'
        elif is_str_arr_type(dnfn__zzoni):
            ssm__mhlsz = 'unicode'
            qopy__qsb = 'object'
        elif dnfn__zzoni == binary_array_type:
            ssm__mhlsz = 'bytes'
            qopy__qsb = 'object'
        elif isinstance(dnfn__zzoni, DecimalArrayType):
            ssm__mhlsz = qopy__qsb = 'object'
        elif isinstance(dnfn__zzoni, IntegerArrayType):
            bnqb__ilu = dnfn__zzoni.dtype.name
            if bnqb__ilu.startswith('int'):
                qopy__qsb = 'Int' + bnqb__ilu[3:]
            elif bnqb__ilu.startswith('uint'):
                qopy__qsb = 'UInt' + bnqb__ilu[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, dnfn__zzoni))
            ssm__mhlsz = dnfn__zzoni.dtype.name
        elif isinstance(dnfn__zzoni, bodo.FloatingArrayType):
            bnqb__ilu = dnfn__zzoni.dtype.name
            ssm__mhlsz = bnqb__ilu
            qopy__qsb = bnqb__ilu.capitalize()
        elif dnfn__zzoni == datetime_date_array_type:
            ssm__mhlsz = 'datetime'
            qopy__qsb = 'object'
        elif isinstance(dnfn__zzoni, TimeArrayType):
            ssm__mhlsz = 'datetime'
            qopy__qsb = 'object'
        elif isinstance(dnfn__zzoni, (StructArrayType, ArrayItemArrayType)):
            ssm__mhlsz = 'object'
            qopy__qsb = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, dnfn__zzoni))
        xdbf__mhi = {'name': col_name, 'field_name': col_name,
            'pandas_type': ssm__mhlsz, 'numpy_type': qopy__qsb, 'metadata':
            ipzq__stp}
        oxt__urom['columns'].append(xdbf__mhi)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            xhb__coz = '__index_level_0__'
            ztc__gxds = None
        else:
            xhb__coz = '%s'
            ztc__gxds = '%s'
        oxt__urom['index_columns'] = [xhb__coz]
        oxt__urom['columns'].append({'name': ztc__gxds, 'field_name':
            xhb__coz, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        oxt__urom['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        oxt__urom['index_columns'] = []
    oxt__urom['pandas_version'] = pd.__version__
    return oxt__urom


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
        ywxq__mty = []
        for eeai__qxpa in partition_cols:
            try:
                idx = df.columns.index(eeai__qxpa)
            except ValueError as irp__wsudd:
                raise BodoError(
                    f'Partition column {eeai__qxpa} is not in dataframe')
            ywxq__mty.append(idx)
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
    udwjh__coni = isinstance(df.index, bodo.hiframes.pd_index_ext.
        RangeIndexType)
    xbd__hfqwo = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not udwjh__coni)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not udwjh__coni or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and udwjh__coni and not is_overload_true(_is_parallel)
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
        hitao__jtbiw = df.runtime_data_types
        lmug__cuo = len(hitao__jtbiw)
        ipzq__stp = gen_pandas_parquet_metadata([''] * lmug__cuo,
            hitao__jtbiw, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        fxlzt__zskvw = ipzq__stp['columns'][:lmug__cuo]
        ipzq__stp['columns'] = ipzq__stp['columns'][lmug__cuo:]
        fxlzt__zskvw = [json.dumps(trgj__qmhjv).replace('""', '{0}') for
            trgj__qmhjv in fxlzt__zskvw]
        eaaq__jrzqy = json.dumps(ipzq__stp)
        yzuw__eln = '"columns": ['
        crc__ulzv = eaaq__jrzqy.find(yzuw__eln)
        if crc__ulzv == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        nrzfu__ssz = crc__ulzv + len(yzuw__eln)
        slx__vgnm = eaaq__jrzqy[:nrzfu__ssz]
        eaaq__jrzqy = eaaq__jrzqy[nrzfu__ssz:]
        riq__ukmz = len(ipzq__stp['columns'])
    else:
        eaaq__jrzqy = json.dumps(gen_pandas_parquet_metadata(df.columns, df
            .data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and udwjh__coni:
        eaaq__jrzqy = eaaq__jrzqy.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            eaaq__jrzqy = eaaq__jrzqy.replace('"%s"', '%s')
    if not df.is_table_format:
        upvht__larf = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    qbgen__fdnpv = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        qbgen__fdnpv += '    py_table = get_dataframe_table(df)\n'
        qbgen__fdnpv += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        qbgen__fdnpv += '    info_list = [{}]\n'.format(upvht__larf)
        qbgen__fdnpv += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        qbgen__fdnpv += '    columns_index = get_dataframe_column_names(df)\n'
        qbgen__fdnpv += '    names_arr = index_to_array(columns_index)\n'
        qbgen__fdnpv += '    col_names = array_to_info(names_arr)\n'
    else:
        qbgen__fdnpv += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and xbd__hfqwo:
        qbgen__fdnpv += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        wyns__vprfd = True
    else:
        qbgen__fdnpv += '    index_col = array_to_info(np.empty(0))\n'
        wyns__vprfd = False
    if df.has_runtime_cols:
        qbgen__fdnpv += '    columns_lst = []\n'
        qbgen__fdnpv += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            qbgen__fdnpv += f'    for _ in range(len(py_table.block_{i})):\n'
            qbgen__fdnpv += f"""        columns_lst.append({fxlzt__zskvw[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            qbgen__fdnpv += '        num_cols += 1\n'
        if riq__ukmz:
            qbgen__fdnpv += "    columns_lst.append('')\n"
        qbgen__fdnpv += '    columns_str = ", ".join(columns_lst)\n'
        qbgen__fdnpv += ('    metadata = """' + slx__vgnm +
            '""" + columns_str + """' + eaaq__jrzqy + '"""\n')
    else:
        qbgen__fdnpv += '    metadata = """' + eaaq__jrzqy + '"""\n'
    qbgen__fdnpv += '    if compression is None:\n'
    qbgen__fdnpv += "        compression = 'none'\n"
    qbgen__fdnpv += '    if _bodo_timestamp_tz is None:\n'
    qbgen__fdnpv += "        _bodo_timestamp_tz = ''\n"
    qbgen__fdnpv += '    if df.index.name is not None:\n'
    qbgen__fdnpv += '        name_ptr = df.index.name\n'
    qbgen__fdnpv += '    else:\n'
    qbgen__fdnpv += "        name_ptr = 'null'\n"
    qbgen__fdnpv += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    pbtxy__hfhk = None
    if partition_cols:
        pbtxy__hfhk = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        txa__wwzr = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in ywxq__mty)
        if txa__wwzr:
            qbgen__fdnpv += '    cat_info_list = [{}]\n'.format(txa__wwzr)
            qbgen__fdnpv += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            qbgen__fdnpv += '    cat_table = table\n'
        qbgen__fdnpv += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        qbgen__fdnpv += (
            f'    part_cols_idxs = np.array({ywxq__mty}, dtype=np.int32)\n')
        qbgen__fdnpv += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        qbgen__fdnpv += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        qbgen__fdnpv += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        qbgen__fdnpv += (
            '                            unicode_to_utf8(compression),\n')
        qbgen__fdnpv += '                            _is_parallel,\n'
        qbgen__fdnpv += (
            '                            unicode_to_utf8(bucket_region),\n')
        qbgen__fdnpv += '                            row_group_size,\n'
        qbgen__fdnpv += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        qbgen__fdnpv += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        qbgen__fdnpv += '    delete_table_decref_arrays(table)\n'
        qbgen__fdnpv += '    delete_info_decref_array(index_col)\n'
        qbgen__fdnpv += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        qbgen__fdnpv += '    delete_info_decref_array(col_names)\n'
        if txa__wwzr:
            qbgen__fdnpv += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        qbgen__fdnpv += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        qbgen__fdnpv += (
            '                            table, col_names, index_col,\n')
        qbgen__fdnpv += '                            ' + str(wyns__vprfd
            ) + ',\n'
        qbgen__fdnpv += (
            '                            unicode_to_utf8(metadata),\n')
        qbgen__fdnpv += (
            '                            unicode_to_utf8(compression),\n')
        qbgen__fdnpv += (
            '                            _is_parallel, 1, df.index.start,\n')
        qbgen__fdnpv += (
            '                            df.index.stop, df.index.step,\n')
        qbgen__fdnpv += (
            '                            unicode_to_utf8(name_ptr),\n')
        qbgen__fdnpv += (
            '                            unicode_to_utf8(bucket_region),\n')
        qbgen__fdnpv += '                            row_group_size,\n'
        qbgen__fdnpv += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        qbgen__fdnpv += '                              False,\n'
        qbgen__fdnpv += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        qbgen__fdnpv += '                              False)\n'
        qbgen__fdnpv += '    delete_table_decref_arrays(table)\n'
        qbgen__fdnpv += '    delete_info_decref_array(index_col)\n'
        qbgen__fdnpv += '    delete_info_decref_array(col_names)\n'
    else:
        qbgen__fdnpv += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        qbgen__fdnpv += (
            '                            table, col_names, index_col,\n')
        qbgen__fdnpv += '                            ' + str(wyns__vprfd
            ) + ',\n'
        qbgen__fdnpv += (
            '                            unicode_to_utf8(metadata),\n')
        qbgen__fdnpv += (
            '                            unicode_to_utf8(compression),\n')
        qbgen__fdnpv += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        qbgen__fdnpv += (
            '                            unicode_to_utf8(name_ptr),\n')
        qbgen__fdnpv += (
            '                            unicode_to_utf8(bucket_region),\n')
        qbgen__fdnpv += '                            row_group_size,\n'
        qbgen__fdnpv += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        qbgen__fdnpv += '                              False,\n'
        qbgen__fdnpv += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        qbgen__fdnpv += '                              False)\n'
        qbgen__fdnpv += '    delete_table_decref_arrays(table)\n'
        qbgen__fdnpv += '    delete_info_decref_array(index_col)\n'
        qbgen__fdnpv += '    delete_info_decref_array(col_names)\n'
    ibr__lzd = {}
    if df.has_runtime_cols:
        xszpy__ultak = None
    else:
        for bmy__grwbq in df.columns:
            if not isinstance(bmy__grwbq, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        xszpy__ultak = pd.array(df.columns)
    exec(qbgen__fdnpv, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': xszpy__ultak,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': pbtxy__hfhk, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, ibr__lzd)
    laon__jxgd = ibr__lzd['df_to_parquet']
    return laon__jxgd


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    otw__ipd = tracing.Event('to_sql_exception_guard', is_parallel=_is_parallel
        )
    vja__hxb = 'all_ok'
    lfvg__vim, fdioc__ich = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        fct__rfsq = 100
        if chunksize is None:
            evrqp__xfvnr = fct__rfsq
        else:
            evrqp__xfvnr = min(chunksize, fct__rfsq)
        if _is_table_create:
            df = df.iloc[:evrqp__xfvnr, :]
        else:
            df = df.iloc[evrqp__xfvnr:, :]
            if len(df) == 0:
                return vja__hxb
    xiyma__etfo = df.columns
    try:
        if lfvg__vim == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            yzyp__gyse = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            pqdup__big = bodo.typeof(df)
            qmq__jbi = {}
            for afchc__nkas, yyj__xmjex in zip(pqdup__big.columns,
                pqdup__big.data):
                if df[afchc__nkas].dtype == 'object':
                    if yyj__xmjex == datetime_date_array_type:
                        qmq__jbi[afchc__nkas] = sa.types.Date
                    elif yyj__xmjex in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not yzyp__gyse or 
                        yzyp__gyse == '0'):
                        qmq__jbi[afchc__nkas] = VARCHAR2(4000)
            dtype = qmq__jbi
        try:
            uvi__pstw = tracing.Event('df_to_sql', is_parallel=_is_parallel)
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
            uvi__pstw.finalize()
        except Exception as ygdo__rkgbk:
            vja__hxb = ygdo__rkgbk.args[0]
            if lfvg__vim == 'oracle' and 'ORA-12899' in vja__hxb:
                vja__hxb += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return vja__hxb
    finally:
        df.columns = xiyma__etfo
        otw__ipd.finalize()


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    otw__ipd = tracing.Event('to_sql_exception_guard_encaps', is_parallel=
        _is_parallel)
    with numba.objmode(out='unicode_type'):
        jcex__pkdey = tracing.Event('to_sql_exception_guard_encaps:objmode',
            is_parallel=_is_parallel)
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
        jcex__pkdey.finalize()
    otw__ipd.finalize()
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
    for bmy__grwbq in df.columns:
        if not isinstance(bmy__grwbq, str):
            raise BodoError(
                'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
    xszpy__ultak = pd.array(df.columns)
    qbgen__fdnpv = """def df_to_sql(
    df, name, con,
    schema=None, if_exists='fail', index=True,
    index_label=None, chunksize=None, dtype=None,
    method=None, _bodo_allow_downcasting=False,
    _is_parallel=False,
):
"""
    qbgen__fdnpv += """    if con.startswith('iceberg'):
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
        qbgen__fdnpv += f'        py_table = get_dataframe_table(df)\n'
        qbgen__fdnpv += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        upvht__larf = ', '.join(
            f'array_to_info(get_dataframe_data(df, {i}))' for i in range(
            len(df.columns)))
        qbgen__fdnpv += f'        info_list = [{upvht__larf}]\n'
        qbgen__fdnpv += f'        table = arr_info_list_to_table(info_list)\n'
    qbgen__fdnpv += """        col_names = array_to_info(col_names_arr)
        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names,
            if_exists, _is_parallel, pyarrow_table_schema,
            _bodo_allow_downcasting,
        )
        delete_table_decref_arrays(table)
        delete_info_decref_array(col_names)
"""
    qbgen__fdnpv += "    elif con.startswith('snowflake'):\n"
    qbgen__fdnpv += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        if _bodo_allow_downcasting and bodo.get_rank() == 0:
            warnings.warn('_bodo_allow_downcasting is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl', sync=False)
"""
    qbgen__fdnpv += "        location = ''\n"
    if not is_overload_none(schema):
        qbgen__fdnpv += '        location += \'"\' + schema + \'".\'\n'
    qbgen__fdnpv += '        location += name\n'
    qbgen__fdnpv += '        my_rank = bodo.get_rank()\n'
    qbgen__fdnpv += """        with bodo.objmode(
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
    qbgen__fdnpv += '        bodo.barrier()\n'
    qbgen__fdnpv += '        if azure_stage_direct_upload:\n'
    qbgen__fdnpv += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    qbgen__fdnpv += '        if chunksize is None:\n'
    qbgen__fdnpv += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        qbgen__fdnpv += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        ukoc__idr = ',' if len(df.columns) == 1 else ''
        qbgen__fdnpv += f"""            memory_usage = np.array(({data}{ukoc__idr}), np.int64).sum()
"""
    qbgen__fdnpv += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        qbgen__fdnpv += (
            '        columns_index = get_dataframe_column_names(df)\n')
        qbgen__fdnpv += '        names_arr = index_to_array(columns_index)\n'
        qbgen__fdnpv += '        col_names = array_to_info(names_arr)\n'
    else:
        qbgen__fdnpv += '        col_names = array_to_info(col_names_arr)\n'
    qbgen__fdnpv += '        index_col = array_to_info(np.empty(0))\n'
    qbgen__fdnpv += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    qbgen__fdnpv += """        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           
"""
    qbgen__fdnpv += '        upload_threads_in_progress = []\n'
    qbgen__fdnpv += """        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           
"""
    qbgen__fdnpv += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    qbgen__fdnpv += '            chunk_path = parquet_path + chunk_name\n'
    qbgen__fdnpv += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    qbgen__fdnpv += (
        '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n')
    qbgen__fdnpv += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    qbgen__fdnpv += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        qbgen__fdnpv += (
            '            py_table_chunk = get_dataframe_table(chunk)\n')
        qbgen__fdnpv += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        dizn__ynfgl = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        qbgen__fdnpv += (
            f'            table_chunk = arr_info_list_to_table([{dizn__ynfgl}])     \n'
            )
    qbgen__fdnpv += '            ev_to_df_table.finalize()\n'
    qbgen__fdnpv += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
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
    qbgen__fdnpv += '        bodo.barrier()\n'
    bxxya__gmhh = bodo.io.snowflake.gen_snowflake_schema(df.columns, df.data)
    qbgen__fdnpv += f"""        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, {bxxya__gmhh},
                if_exists, old_creds, tmp_folder,
                azure_stage_direct_upload, old_core_site,
                old_sas_token,
            )
"""
    qbgen__fdnpv += '        if azure_stage_direct_upload:\n'
    qbgen__fdnpv += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    qbgen__fdnpv += '        ev.finalize()\n'
    qbgen__fdnpv += '    else:\n'
    qbgen__fdnpv += (
        '        if _bodo_allow_downcasting and bodo.get_rank() == 0:\n')
    qbgen__fdnpv += """            warnings.warn('_bodo_allow_downcasting is not supported for SQL tables.')
"""
    qbgen__fdnpv += '        rank = bodo.libs.distributed_api.get_rank()\n'
    qbgen__fdnpv += "        err_msg = 'unset'\n"
    qbgen__fdnpv += '        if rank != 0:\n'
    qbgen__fdnpv += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    qbgen__fdnpv += '        elif rank == 0:\n'
    qbgen__fdnpv += '            err_msg = to_sql_exception_guard_encaps(\n'
    qbgen__fdnpv += """                          df, name, con, schema, if_exists, index, index_label,
"""
    qbgen__fdnpv += '                          chunksize, dtype, method,\n'
    qbgen__fdnpv += '                          True, _is_parallel,\n'
    qbgen__fdnpv += '                      )\n'
    qbgen__fdnpv += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    qbgen__fdnpv += "        if_exists = 'append'\n"
    qbgen__fdnpv += "        if _is_parallel and err_msg == 'all_ok':\n"
    qbgen__fdnpv += '            err_msg = to_sql_exception_guard_encaps(\n'
    qbgen__fdnpv += """                          df, name, con, schema, if_exists, index, index_label,
"""
    qbgen__fdnpv += '                          chunksize, dtype, method,\n'
    qbgen__fdnpv += '                          False, _is_parallel,\n'
    qbgen__fdnpv += '                      )\n'
    qbgen__fdnpv += "        if err_msg != 'all_ok':\n"
    qbgen__fdnpv += "            print('err_msg=', err_msg)\n"
    qbgen__fdnpv += (
        "            raise ValueError('error in to_sql() operation')\n")
    ibr__lzd = {}
    qhtsi__fyqp = globals().copy()
    qhtsi__fyqp.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        xszpy__ultak, 'delete_info_decref_array': delete_info_decref_array,
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
    exec(qbgen__fdnpv, qhtsi__fyqp, ibr__lzd)
    _impl = ibr__lzd['df_to_sql']
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
        fcwk__ieda = get_overload_const_str(path_or_buf)
        if fcwk__ieda.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        acyxr__pxzo = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(acyxr__pxzo), unicode_to_utf8(
                _bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(acyxr__pxzo), unicode_to_utf8(
                _bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    niacr__ajtb = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    vsdo__mtvvg = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', niacr__ajtb, vsdo__mtvvg,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    qbgen__fdnpv = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        cyid__owmze = data.data.dtype.categories
        qbgen__fdnpv += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        cyid__owmze = data.dtype.categories
        qbgen__fdnpv += '  data_values = data\n'
    nbz__sklm = len(cyid__owmze)
    qbgen__fdnpv += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    qbgen__fdnpv += '  numba.parfors.parfor.init_prange()\n'
    qbgen__fdnpv += '  n = len(data_values)\n'
    for i in range(nbz__sklm):
        qbgen__fdnpv += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    qbgen__fdnpv += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    qbgen__fdnpv += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for mmxl__shhew in range(nbz__sklm):
        qbgen__fdnpv += '          data_arr_{}[i] = 0\n'.format(mmxl__shhew)
    qbgen__fdnpv += '      else:\n'
    for grucn__uro in range(nbz__sklm):
        qbgen__fdnpv += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            grucn__uro)
    upvht__larf = ', '.join(f'data_arr_{i}' for i in range(nbz__sklm))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(cyid__owmze[0], np.datetime64):
        cyid__owmze = tuple(pd.Timestamp(afchc__nkas) for afchc__nkas in
            cyid__owmze)
    elif isinstance(cyid__owmze[0], np.timedelta64):
        cyid__owmze = tuple(pd.Timedelta(afchc__nkas) for afchc__nkas in
            cyid__owmze)
    return bodo.hiframes.dataframe_impl._gen_init_df(qbgen__fdnpv,
        cyid__owmze, upvht__larf, index)


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
    for zvllo__lxg in pd_unsupported:
        slvs__vuzp = mod_name + '.' + zvllo__lxg.__name__
        overload(zvllo__lxg, no_unliteral=True)(create_unsupported_overload
            (slvs__vuzp))


def _install_dataframe_unsupported():
    for miw__kly in dataframe_unsupported_attrs:
        wde__epzrr = 'DataFrame.' + miw__kly
        overload_attribute(DataFrameType, miw__kly)(create_unsupported_overload
            (wde__epzrr))
    for slvs__vuzp in dataframe_unsupported:
        wde__epzrr = 'DataFrame.' + slvs__vuzp + '()'
        overload_method(DataFrameType, slvs__vuzp)(create_unsupported_overload
            (wde__epzrr))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
