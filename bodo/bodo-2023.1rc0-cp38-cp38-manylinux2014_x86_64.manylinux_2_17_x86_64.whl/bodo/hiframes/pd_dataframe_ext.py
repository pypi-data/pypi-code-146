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
            kyrf__rtzfr = f'{len(self.data)} columns of types {set(self.data)}'
            ymggw__jpo = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            nxkt__rqwka = str(hash(super().__str__()))
            return (
                f'dataframe({kyrf__rtzfr}, {self.index}, {ymggw__jpo}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols}, key_hash={nxkt__rqwka})'
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
        return {weog__fok: i for i, weog__fok in enumerate(self.columns)}

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
            jjx__ojw = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(kli__hlpg.unify(typingctx, iuyy__abqk) if 
                kli__hlpg != iuyy__abqk else kli__hlpg for kli__hlpg,
                iuyy__abqk in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if jjx__ojw is not None and None not in data:
                return DataFrameType(data, jjx__ojw, self.columns, dist,
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
        return all(kli__hlpg.is_precise() for kli__hlpg in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        xkoo__lkvy = self.columns.index(col_name)
        aqtyj__plo = tuple(list(self.data[:xkoo__lkvy]) + [new_type] + list
            (self.data[xkoo__lkvy + 1:]))
        return DataFrameType(aqtyj__plo, self.index, self.columns, self.
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
        ndya__rdbne = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            ndya__rdbne.append(('columns', fe_type.df_type.runtime_colname_typ)
                )
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, ndya__rdbne)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        ndya__rdbne = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, ndya__rdbne)


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
        vzklh__dqfy = 'n',
        mrg__fgs = {'n': 5}
        lfi__rvs, yzzf__hbbtl = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, vzklh__dqfy, mrg__fgs)
        zkurm__szg = yzzf__hbbtl[0]
        if not is_overload_int(zkurm__szg):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        lslkg__hzv = df.copy()
        return lslkg__hzv(*yzzf__hbbtl).replace(pysig=lfi__rvs)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        ykjvb__hily = (df,) + args
        vzklh__dqfy = 'df', 'method', 'min_periods'
        mrg__fgs = {'method': 'pearson', 'min_periods': 1}
        gzto__int = 'method',
        lfi__rvs, yzzf__hbbtl = bodo.utils.typing.fold_typing_args(func_name,
            ykjvb__hily, kws, vzklh__dqfy, mrg__fgs, gzto__int)
        krq__dowzg = yzzf__hbbtl[2]
        if not is_overload_int(krq__dowzg):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        nng__vpc = []
        iqzs__hxuk = []
        for weog__fok, rdw__wnog in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(rdw__wnog.dtype):
                nng__vpc.append(weog__fok)
                iqzs__hxuk.append(types.Array(types.float64, 1, 'A'))
        if len(nng__vpc) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        iqzs__hxuk = tuple(iqzs__hxuk)
        nng__vpc = tuple(nng__vpc)
        index_typ = bodo.utils.typing.type_col_to_index(nng__vpc)
        lslkg__hzv = DataFrameType(iqzs__hxuk, index_typ, nng__vpc)
        return lslkg__hzv(*yzzf__hbbtl).replace(pysig=lfi__rvs)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        edn__kqtd = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        bfcs__avl = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        hbx__jpk = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        eakcn__ieiky = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        jtz__fkpbf = dict(raw=bfcs__avl, result_type=hbx__jpk)
        tsdc__qjk = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', jtz__fkpbf, tsdc__qjk,
            package_name='pandas', module_name='DataFrame')
        gme__nral = True
        if types.unliteral(edn__kqtd) == types.unicode_type:
            if not is_overload_constant_str(edn__kqtd):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            gme__nral = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        lav__gqjq = get_overload_const_int(axis)
        if gme__nral and lav__gqjq != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif lav__gqjq not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        jnzv__hyn = []
        for arr_typ in df.data:
            maes__hyu = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            vcy__ncs = self.context.resolve_function_type(operator.getitem,
                (SeriesIlocType(maes__hyu), types.int64), {}).return_type
            jnzv__hyn.append(vcy__ncs)
        keulq__ygdtn = types.none
        gkws__czy = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(weog__fok) for weog__fok in df.columns)), None)
        xpvnn__ahj = types.BaseTuple.from_types(jnzv__hyn)
        hbjqi__mjlca = types.Tuple([types.bool_] * len(xpvnn__ahj))
        hpe__rqagk = bodo.NullableTupleType(xpvnn__ahj, hbjqi__mjlca)
        mve__tgeu = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if mve__tgeu == types.NPDatetime('ns'):
            mve__tgeu = bodo.pd_timestamp_tz_naive_type
        if mve__tgeu == types.NPTimedelta('ns'):
            mve__tgeu = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(xpvnn__ahj):
            hepm__xzex = HeterogeneousSeriesType(hpe__rqagk, gkws__czy,
                mve__tgeu)
        else:
            hepm__xzex = SeriesType(xpvnn__ahj.dtype, hpe__rqagk, gkws__czy,
                mve__tgeu)
        qta__zgxys = hepm__xzex,
        if eakcn__ieiky is not None:
            qta__zgxys += tuple(eakcn__ieiky.types)
        try:
            if not gme__nral:
                ghfof__uln = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(edn__kqtd), self.context,
                    'DataFrame.apply', axis if lav__gqjq == 1 else None)
            else:
                ghfof__uln = get_const_func_output_type(edn__kqtd,
                    qta__zgxys, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as xmr__ekaro:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()', xmr__ekaro)
                )
        if gme__nral:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(ghfof__uln, (SeriesType, HeterogeneousSeriesType)
                ) and ghfof__uln.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(ghfof__uln, HeterogeneousSeriesType):
                crndt__tcs, yuaxj__zyvrt = ghfof__uln.const_info
                if isinstance(ghfof__uln.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    vojou__lonw = ghfof__uln.data.tuple_typ.types
                elif isinstance(ghfof__uln.data, types.Tuple):
                    vojou__lonw = ghfof__uln.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                rkqll__qiiz = tuple(to_nullable_type(dtype_to_array_type(
                    aov__gei)) for aov__gei in vojou__lonw)
                lxgjt__uzm = DataFrameType(rkqll__qiiz, df.index, yuaxj__zyvrt)
            elif isinstance(ghfof__uln, SeriesType):
                qoao__agt, yuaxj__zyvrt = ghfof__uln.const_info
                rkqll__qiiz = tuple(to_nullable_type(dtype_to_array_type(
                    ghfof__uln.dtype)) for crndt__tcs in range(qoao__agt))
                lxgjt__uzm = DataFrameType(rkqll__qiiz, df.index, yuaxj__zyvrt)
            else:
                rokap__csxaf = get_udf_out_arr_type(ghfof__uln)
                lxgjt__uzm = SeriesType(rokap__csxaf.dtype, rokap__csxaf,
                    df.index, None)
        else:
            lxgjt__uzm = ghfof__uln
        hsb__mplp = ', '.join("{} = ''".format(kli__hlpg) for kli__hlpg in
            kws.keys())
        ikd__gdw = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {hsb__mplp}):
"""
        ikd__gdw += '    pass\n'
        loh__npi = {}
        exec(ikd__gdw, {}, loh__npi)
        cnffu__zyk = loh__npi['apply_stub']
        lfi__rvs = numba.core.utils.pysignature(cnffu__zyk)
        jfmpz__hohnh = (edn__kqtd, axis, bfcs__avl, hbx__jpk, eakcn__ieiky
            ) + tuple(kws.values())
        return signature(lxgjt__uzm, *jfmpz__hohnh).replace(pysig=lfi__rvs)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        vzklh__dqfy = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        mrg__fgs = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        gzto__int = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        lfi__rvs, yzzf__hbbtl = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, vzklh__dqfy, mrg__fgs, gzto__int)
        tcaaz__nvx = yzzf__hbbtl[2]
        if not is_overload_constant_str(tcaaz__nvx):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        witkm__scqe = yzzf__hbbtl[0]
        if not is_overload_none(witkm__scqe) and not (is_overload_int(
            witkm__scqe) or is_overload_constant_str(witkm__scqe)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(witkm__scqe):
            fqf__lqp = get_overload_const_str(witkm__scqe)
            if fqf__lqp not in df.columns:
                raise BodoError(f'{func_name}: {fqf__lqp} column not found.')
        elif is_overload_int(witkm__scqe):
            ckxyj__ttlx = get_overload_const_int(witkm__scqe)
            if ckxyj__ttlx > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {ckxyj__ttlx} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            witkm__scqe = df.columns[witkm__scqe]
        qepy__yka = yzzf__hbbtl[1]
        if not is_overload_none(qepy__yka) and not (is_overload_int(
            qepy__yka) or is_overload_constant_str(qepy__yka)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(qepy__yka):
            pxlez__zdjvh = get_overload_const_str(qepy__yka)
            if pxlez__zdjvh not in df.columns:
                raise BodoError(
                    f'{func_name}: {pxlez__zdjvh} column not found.')
        elif is_overload_int(qepy__yka):
            aatop__eiy = get_overload_const_int(qepy__yka)
            if aatop__eiy > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {aatop__eiy} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            qepy__yka = df.columns[qepy__yka]
        hmnj__pck = yzzf__hbbtl[3]
        if not is_overload_none(hmnj__pck) and not is_tuple_like_type(hmnj__pck
            ):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        svb__spee = yzzf__hbbtl[10]
        if not is_overload_none(svb__spee) and not is_overload_constant_str(
            svb__spee):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        imsjg__dnufl = yzzf__hbbtl[12]
        if not is_overload_bool(imsjg__dnufl):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        pljwo__bytc = yzzf__hbbtl[17]
        if not is_overload_none(pljwo__bytc) and not is_tuple_like_type(
            pljwo__bytc):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        wgle__lhai = yzzf__hbbtl[18]
        if not is_overload_none(wgle__lhai) and not is_tuple_like_type(
            wgle__lhai):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        uqhk__cxf = yzzf__hbbtl[22]
        if not is_overload_none(uqhk__cxf) and not is_overload_int(uqhk__cxf):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        mii__yuj = yzzf__hbbtl[29]
        if not is_overload_none(mii__yuj) and not is_overload_constant_str(
            mii__yuj):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        bakd__vcfh = yzzf__hbbtl[30]
        if not is_overload_none(bakd__vcfh) and not is_overload_constant_str(
            bakd__vcfh):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        ddkud__igty = types.List(types.mpl_line_2d_type)
        tcaaz__nvx = get_overload_const_str(tcaaz__nvx)
        if tcaaz__nvx == 'scatter':
            if is_overload_none(witkm__scqe) and is_overload_none(qepy__yka):
                raise BodoError(
                    f'{func_name}: {tcaaz__nvx} requires an x and y column.')
            elif is_overload_none(witkm__scqe):
                raise BodoError(
                    f'{func_name}: {tcaaz__nvx} x column is missing.')
            elif is_overload_none(qepy__yka):
                raise BodoError(
                    f'{func_name}: {tcaaz__nvx} y column is missing.')
            ddkud__igty = types.mpl_path_collection_type
        elif tcaaz__nvx != 'line':
            raise BodoError(f'{func_name}: {tcaaz__nvx} plot is not supported.'
                )
        return signature(ddkud__igty, *yzzf__hbbtl).replace(pysig=lfi__rvs)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            ykg__mofm = df.columns.index(attr)
            arr_typ = df.data[ykg__mofm]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            gllg__ggbeo = []
            aqtyj__plo = []
            trhe__vlp = False
            for i, myx__svu in enumerate(df.columns):
                if myx__svu[0] != attr:
                    continue
                trhe__vlp = True
                gllg__ggbeo.append(myx__svu[1] if len(myx__svu) == 2 else
                    myx__svu[1:])
                aqtyj__plo.append(df.data[i])
            if trhe__vlp:
                return DataFrameType(tuple(aqtyj__plo), df.index, tuple(
                    gllg__ggbeo))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        opief__mwd = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(opief__mwd)
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
        xrzei__qnd = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], xrzei__qnd)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    aoqgw__mcm = builder.module
    uvwf__oum = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    xfrvr__hqu = cgutils.get_or_insert_function(aoqgw__mcm, uvwf__oum, name
        ='.dtor.df.{}'.format(df_type))
    if not xfrvr__hqu.is_declaration:
        return xfrvr__hqu
    xfrvr__hqu.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(xfrvr__hqu.append_basic_block())
    opay__nritw = xfrvr__hqu.args[0]
    dgfg__pxgmh = context.get_value_type(payload_type).as_pointer()
    ivx__qdn = builder.bitcast(opay__nritw, dgfg__pxgmh)
    payload = context.make_helper(builder, payload_type, ref=ivx__qdn)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        zncu__apyw = context.get_python_api(builder)
        exha__ovakd = zncu__apyw.gil_ensure()
        zncu__apyw.decref(payload.parent)
        zncu__apyw.gil_release(exha__ovakd)
    builder.ret_void()
    return xfrvr__hqu


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    bnv__rsgvo = cgutils.create_struct_proxy(payload_type)(context, builder)
    bnv__rsgvo.data = data_tup
    bnv__rsgvo.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        bnv__rsgvo.columns = colnames
    xmrme__tifqw = context.get_value_type(payload_type)
    iafz__jyygr = context.get_abi_sizeof(xmrme__tifqw)
    ooxd__vewg = define_df_dtor(context, builder, df_type, payload_type)
    jvyrp__enoge = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, iafz__jyygr), ooxd__vewg)
    tst__scjvd = context.nrt.meminfo_data(builder, jvyrp__enoge)
    uic__fveng = builder.bitcast(tst__scjvd, xmrme__tifqw.as_pointer())
    sms__hzqkl = cgutils.create_struct_proxy(df_type)(context, builder)
    sms__hzqkl.meminfo = jvyrp__enoge
    if parent is None:
        sms__hzqkl.parent = cgutils.get_null_value(sms__hzqkl.parent.type)
    else:
        sms__hzqkl.parent = parent
        bnv__rsgvo.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            zncu__apyw = context.get_python_api(builder)
            exha__ovakd = zncu__apyw.gil_ensure()
            zncu__apyw.incref(parent)
            zncu__apyw.gil_release(exha__ovakd)
    builder.store(bnv__rsgvo._getvalue(), uic__fveng)
    return sms__hzqkl._getvalue()


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
        itich__ftwsz = [data_typ.dtype.arr_types.dtype] * len(data_typ.
            dtype.arr_types)
    else:
        itich__ftwsz = [aov__gei for aov__gei in data_typ.dtype.arr_types]
    xcszr__blz = DataFrameType(tuple(itich__ftwsz + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        eujiv__aaey = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return eujiv__aaey
    sig = signature(xcszr__blz, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    qoao__agt = len(data_tup_typ.types)
    if qoao__agt == 0:
        column_names = ()
    hlvp__keahw = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(hlvp__keahw, ColNamesMetaType) and isinstance(hlvp__keahw
        .meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = hlvp__keahw.meta
    if qoao__agt == 1 and isinstance(data_tup_typ.types[0], TableType):
        qoao__agt = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == qoao__agt, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    lnr__gez = data_tup_typ.types
    if qoao__agt != 0 and isinstance(data_tup_typ.types[0], TableType):
        lnr__gez = data_tup_typ.types[0].arr_types
        is_table_format = True
    xcszr__blz = DataFrameType(lnr__gez, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            herwd__aov = cgutils.create_struct_proxy(xcszr__blz.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = herwd__aov.parent
        eujiv__aaey = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return eujiv__aaey
    sig = signature(xcszr__blz, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        sms__hzqkl = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, sms__hzqkl.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        bnv__rsgvo = get_dataframe_payload(context, builder, df_typ, args[0])
        gazga__uvuu = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[gazga__uvuu]
        if df_typ.is_table_format:
            herwd__aov = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(bnv__rsgvo.data, 0))
            nme__srexv = df_typ.table_type.type_to_blk[arr_typ]
            iwb__nga = getattr(herwd__aov, f'block_{nme__srexv}')
            gdja__gksth = ListInstance(context, builder, types.List(arr_typ
                ), iwb__nga)
            suhb__hyl = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[gazga__uvuu])
            xrzei__qnd = gdja__gksth.getitem(suhb__hyl)
        else:
            xrzei__qnd = builder.extract_value(bnv__rsgvo.data, gazga__uvuu)
        uuwtl__wdxt = cgutils.alloca_once_value(builder, xrzei__qnd)
        eqib__exmjl = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, uuwtl__wdxt, eqib__exmjl)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    jvyrp__enoge = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, jvyrp__enoge)
    dgfg__pxgmh = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, dgfg__pxgmh)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    xcszr__blz = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        xcszr__blz = types.Tuple([TableType(df_typ.data)])
    sig = signature(xcszr__blz, df_typ)

    def codegen(context, builder, signature, args):
        bnv__rsgvo = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            bnv__rsgvo.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        bnv__rsgvo = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, bnv__rsgvo
            .index)
    xcszr__blz = df_typ.index
    sig = signature(xcszr__blz, df_typ)
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
        lslkg__hzv = df.data[i]
        return lslkg__hzv(*args)


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
        bnv__rsgvo = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(bnv__rsgvo.data, 0))
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
    eohpn__uxpcf = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{eohpn__uxpcf})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        lslkg__hzv = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return lslkg__hzv(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        bnv__rsgvo = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, bnv__rsgvo.columns)
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
    xpvnn__ahj = self.typemap[data_tup.name]
    if any(is_tuple_like_type(aov__gei) for aov__gei in xpvnn__ahj.types):
        return None
    if equiv_set.has_shape(data_tup):
        espnv__iev = equiv_set.get_shape(data_tup)
        if len(espnv__iev) > 1:
            equiv_set.insert_equiv(*espnv__iev)
        if len(espnv__iev) > 0:
            gkws__czy = self.typemap[index.name]
            if not isinstance(gkws__czy, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(espnv__iev[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(espnv__iev[0], len(
                espnv__iev)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    mytzi__bkn = args[0]
    data_types = self.typemap[mytzi__bkn.name].data
    if any(is_tuple_like_type(aov__gei) for aov__gei in data_types):
        return None
    if equiv_set.has_shape(mytzi__bkn):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mytzi__bkn)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    mytzi__bkn = args[0]
    gkws__czy = self.typemap[mytzi__bkn.name].index
    if isinstance(gkws__czy, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(mytzi__bkn):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mytzi__bkn)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    mytzi__bkn = args[0]
    if equiv_set.has_shape(mytzi__bkn):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mytzi__bkn), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    mytzi__bkn = args[0]
    if equiv_set.has_shape(mytzi__bkn):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mytzi__bkn)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    gazga__uvuu = get_overload_const_int(c_ind_typ)
    if df_typ.data[gazga__uvuu] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        vec__vkokm, crndt__tcs, zusmf__keq = args
        bnv__rsgvo = get_dataframe_payload(context, builder, df_typ, vec__vkokm
            )
        if df_typ.is_table_format:
            herwd__aov = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(bnv__rsgvo.data, 0))
            nme__srexv = df_typ.table_type.type_to_blk[arr_typ]
            iwb__nga = getattr(herwd__aov, f'block_{nme__srexv}')
            gdja__gksth = ListInstance(context, builder, types.List(arr_typ
                ), iwb__nga)
            suhb__hyl = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[gazga__uvuu])
            gdja__gksth.setitem(suhb__hyl, zusmf__keq, True)
        else:
            xrzei__qnd = builder.extract_value(bnv__rsgvo.data, gazga__uvuu)
            context.nrt.decref(builder, df_typ.data[gazga__uvuu], xrzei__qnd)
            bnv__rsgvo.data = builder.insert_value(bnv__rsgvo.data,
                zusmf__keq, gazga__uvuu)
            context.nrt.incref(builder, arr_typ, zusmf__keq)
        sms__hzqkl = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=vec__vkokm)
        payload_type = DataFramePayloadType(df_typ)
        ivx__qdn = context.nrt.meminfo_data(builder, sms__hzqkl.meminfo)
        dgfg__pxgmh = context.get_value_type(payload_type).as_pointer()
        ivx__qdn = builder.bitcast(ivx__qdn, dgfg__pxgmh)
        builder.store(bnv__rsgvo._getvalue(), ivx__qdn)
        return impl_ret_borrowed(context, builder, df_typ, vec__vkokm)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        yuxz__dzseh = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        odetk__joakh = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=yuxz__dzseh)
        ifz__ndzop = get_dataframe_payload(context, builder, df_typ,
            yuxz__dzseh)
        sms__hzqkl = construct_dataframe(context, builder, signature.
            return_type, ifz__ndzop.data, index_val, odetk__joakh.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), ifz__ndzop.data)
        return sms__hzqkl
    xcszr__blz = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(xcszr__blz, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    qoao__agt = len(df_type.columns)
    mzb__iqs = qoao__agt
    wpkh__ovcp = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    vvu__akny = col_name not in df_type.columns
    gazga__uvuu = qoao__agt
    if vvu__akny:
        wpkh__ovcp += arr_type,
        column_names += col_name,
        mzb__iqs += 1
    else:
        gazga__uvuu = df_type.columns.index(col_name)
        wpkh__ovcp = tuple(arr_type if i == gazga__uvuu else wpkh__ovcp[i] for
            i in range(qoao__agt))

    def codegen(context, builder, signature, args):
        vec__vkokm, crndt__tcs, zusmf__keq = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, vec__vkokm)
        lgs__xew = cgutils.create_struct_proxy(df_type)(context, builder,
            value=vec__vkokm)
        if df_type.is_table_format:
            yxzgz__ytrwr = df_type.table_type
            ihqsy__bms = builder.extract_value(in_dataframe_payload.data, 0)
            qpg__svmxk = TableType(wpkh__ovcp)
            rsog__ekk = set_table_data_codegen(context, builder,
                yxzgz__ytrwr, ihqsy__bms, qpg__svmxk, arr_type, zusmf__keq,
                gazga__uvuu, vvu__akny)
            data_tup = context.make_tuple(builder, types.Tuple([qpg__svmxk]
                ), [rsog__ekk])
        else:
            lnr__gez = [(builder.extract_value(in_dataframe_payload.data, i
                ) if i != gazga__uvuu else zusmf__keq) for i in range(
                qoao__agt)]
            if vvu__akny:
                lnr__gez.append(zusmf__keq)
            for mytzi__bkn, klyy__tsyzm in zip(lnr__gez, wpkh__ovcp):
                context.nrt.incref(builder, klyy__tsyzm, mytzi__bkn)
            data_tup = context.make_tuple(builder, types.Tuple(wpkh__ovcp),
                lnr__gez)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        shybn__vjnv = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, lgs__xew.parent, None)
        if not vvu__akny and arr_type == df_type.data[gazga__uvuu]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            ivx__qdn = context.nrt.meminfo_data(builder, lgs__xew.meminfo)
            dgfg__pxgmh = context.get_value_type(payload_type).as_pointer()
            ivx__qdn = builder.bitcast(ivx__qdn, dgfg__pxgmh)
            fyyme__pmgwm = get_dataframe_payload(context, builder, df_type,
                shybn__vjnv)
            builder.store(fyyme__pmgwm._getvalue(), ivx__qdn)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, qpg__svmxk, builder.
                    extract_value(data_tup, 0))
            else:
                for mytzi__bkn, klyy__tsyzm in zip(lnr__gez, wpkh__ovcp):
                    context.nrt.incref(builder, klyy__tsyzm, mytzi__bkn)
        has_parent = cgutils.is_not_null(builder, lgs__xew.parent)
        with builder.if_then(has_parent):
            zncu__apyw = context.get_python_api(builder)
            exha__ovakd = zncu__apyw.gil_ensure()
            dihn__zcz = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, zusmf__keq)
            weog__fok = numba.core.pythonapi._BoxContext(context, builder,
                zncu__apyw, dihn__zcz)
            hcj__favr = weog__fok.pyapi.from_native_value(arr_type,
                zusmf__keq, weog__fok.env_manager)
            if isinstance(col_name, str):
                jyyb__xghu = context.insert_const_string(builder.module,
                    col_name)
                cgoqx__ctja = zncu__apyw.string_from_string(jyyb__xghu)
            else:
                assert isinstance(col_name, int)
                cgoqx__ctja = zncu__apyw.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            zncu__apyw.object_setitem(lgs__xew.parent, cgoqx__ctja, hcj__favr)
            zncu__apyw.decref(hcj__favr)
            zncu__apyw.decref(cgoqx__ctja)
            zncu__apyw.gil_release(exha__ovakd)
        return shybn__vjnv
    xcszr__blz = DataFrameType(wpkh__ovcp, index_typ, column_names, df_type
        .dist, df_type.is_table_format)
    sig = signature(xcszr__blz, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    qoao__agt = len(pyval.columns)
    lnr__gez = []
    for i in range(qoao__agt):
        dsnv__zwqhf = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            hcj__favr = dsnv__zwqhf.array
        else:
            hcj__favr = dsnv__zwqhf.values
        lnr__gez.append(hcj__favr)
    lnr__gez = tuple(lnr__gez)
    if df_type.is_table_format:
        herwd__aov = context.get_constant_generic(builder, df_type.
            table_type, Table(lnr__gez))
        data_tup = lir.Constant.literal_struct([herwd__aov])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], myx__svu) for i,
            myx__svu in enumerate(lnr__gez)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    lfs__vdi = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, lfs__vdi])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    svux__cjwqq = context.get_constant(types.int64, -1)
    zfcrp__lgxsx = context.get_constant_null(types.voidptr)
    jvyrp__enoge = lir.Constant.literal_struct([svux__cjwqq, zfcrp__lgxsx,
        zfcrp__lgxsx, payload, svux__cjwqq])
    jvyrp__enoge = cgutils.global_constant(builder, '.const.meminfo',
        jvyrp__enoge).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([jvyrp__enoge, lfs__vdi])


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
        jjx__ojw = context.cast(builder, in_dataframe_payload.index, fromty
            .index, toty.index)
    else:
        jjx__ojw = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, jjx__ojw)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        aqtyj__plo = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                aqtyj__plo)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), aqtyj__plo)
    elif not fromty.is_table_format and toty.is_table_format:
        aqtyj__plo = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        aqtyj__plo = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        aqtyj__plo = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        aqtyj__plo = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, aqtyj__plo, jjx__ojw,
        in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    awmbw__iqwaj = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        ahed__pujgq = get_index_data_arr_types(toty.index)[0]
        qex__kpwkh = bodo.utils.transform.get_type_alloc_counts(ahed__pujgq
            ) - 1
        xnvn__eabv = ', '.join('0' for crndt__tcs in range(qex__kpwkh))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(xnvn__eabv, ', ' if qex__kpwkh == 1 else ''))
        awmbw__iqwaj['index_arr_type'] = ahed__pujgq
    tkvv__bbv = []
    for i, arr_typ in enumerate(toty.data):
        qex__kpwkh = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        xnvn__eabv = ', '.join('0' for crndt__tcs in range(qex__kpwkh))
        okkb__trre = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, xnvn__eabv, ', ' if qex__kpwkh == 1 else ''))
        tkvv__bbv.append(okkb__trre)
        awmbw__iqwaj[f'arr_type{i}'] = arr_typ
    tkvv__bbv = ', '.join(tkvv__bbv)
    ikd__gdw = 'def impl():\n'
    iiffc__ekaqk = bodo.hiframes.dataframe_impl._gen_init_df(ikd__gdw, toty
        .columns, tkvv__bbv, index, awmbw__iqwaj)
    df = context.compile_internal(builder, iiffc__ekaqk, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    kjb__nvvle = toty.table_type
    herwd__aov = cgutils.create_struct_proxy(kjb__nvvle)(context, builder)
    herwd__aov.parent = in_dataframe_payload.parent
    for aov__gei, nme__srexv in kjb__nvvle.type_to_blk.items():
        eehss__iuw = context.get_constant(types.int64, len(kjb__nvvle.
            block_to_arr_ind[nme__srexv]))
        crndt__tcs, iip__qdza = ListInstance.allocate_ex(context, builder,
            types.List(aov__gei), eehss__iuw)
        iip__qdza.size = eehss__iuw
        setattr(herwd__aov, f'block_{nme__srexv}', iip__qdza.value)
    for i, aov__gei in enumerate(fromty.data):
        uykfx__bisrm = toty.data[i]
        if aov__gei != uykfx__bisrm:
            hav__qkegl = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*hav__qkegl)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        xrzei__qnd = builder.extract_value(in_dataframe_payload.data, i)
        if aov__gei != uykfx__bisrm:
            ior__amr = context.cast(builder, xrzei__qnd, aov__gei, uykfx__bisrm
                )
            pyd__cty = False
        else:
            ior__amr = xrzei__qnd
            pyd__cty = True
        nme__srexv = kjb__nvvle.type_to_blk[aov__gei]
        iwb__nga = getattr(herwd__aov, f'block_{nme__srexv}')
        gdja__gksth = ListInstance(context, builder, types.List(aov__gei),
            iwb__nga)
        suhb__hyl = context.get_constant(types.int64, kjb__nvvle.
            block_offsets[i])
        gdja__gksth.setitem(suhb__hyl, ior__amr, pyd__cty)
    data_tup = context.make_tuple(builder, types.Tuple([kjb__nvvle]), [
        herwd__aov._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    lnr__gez = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            hav__qkegl = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*hav__qkegl)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            xrzei__qnd = builder.extract_value(in_dataframe_payload.data, i)
            ior__amr = context.cast(builder, xrzei__qnd, fromty.data[i],
                toty.data[i])
            pyd__cty = False
        else:
            ior__amr = builder.extract_value(in_dataframe_payload.data, i)
            pyd__cty = True
        if pyd__cty:
            context.nrt.incref(builder, toty.data[i], ior__amr)
        lnr__gez.append(ior__amr)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), lnr__gez)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    yxzgz__ytrwr = fromty.table_type
    ihqsy__bms = cgutils.create_struct_proxy(yxzgz__ytrwr)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    qpg__svmxk = toty.table_type
    rsog__ekk = cgutils.create_struct_proxy(qpg__svmxk)(context, builder)
    rsog__ekk.parent = in_dataframe_payload.parent
    for aov__gei, nme__srexv in qpg__svmxk.type_to_blk.items():
        eehss__iuw = context.get_constant(types.int64, len(qpg__svmxk.
            block_to_arr_ind[nme__srexv]))
        crndt__tcs, iip__qdza = ListInstance.allocate_ex(context, builder,
            types.List(aov__gei), eehss__iuw)
        iip__qdza.size = eehss__iuw
        setattr(rsog__ekk, f'block_{nme__srexv}', iip__qdza.value)
    for i in range(len(fromty.data)):
        qheo__hlia = fromty.data[i]
        uykfx__bisrm = toty.data[i]
        if qheo__hlia != uykfx__bisrm:
            hav__qkegl = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*hav__qkegl)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        xxc__mat = yxzgz__ytrwr.type_to_blk[qheo__hlia]
        rlu__kdh = getattr(ihqsy__bms, f'block_{xxc__mat}')
        fcjwl__jit = ListInstance(context, builder, types.List(qheo__hlia),
            rlu__kdh)
        ybi__wcx = context.get_constant(types.int64, yxzgz__ytrwr.
            block_offsets[i])
        xrzei__qnd = fcjwl__jit.getitem(ybi__wcx)
        if qheo__hlia != uykfx__bisrm:
            ior__amr = context.cast(builder, xrzei__qnd, qheo__hlia,
                uykfx__bisrm)
            pyd__cty = False
        else:
            ior__amr = xrzei__qnd
            pyd__cty = True
        mrzhw__fntsz = qpg__svmxk.type_to_blk[aov__gei]
        iip__qdza = getattr(rsog__ekk, f'block_{mrzhw__fntsz}')
        enhi__hsj = ListInstance(context, builder, types.List(uykfx__bisrm),
            iip__qdza)
        iikm__jsgjp = context.get_constant(types.int64, qpg__svmxk.
            block_offsets[i])
        enhi__hsj.setitem(iikm__jsgjp, ior__amr, pyd__cty)
    data_tup = context.make_tuple(builder, types.Tuple([qpg__svmxk]), [
        rsog__ekk._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    kjb__nvvle = fromty.table_type
    herwd__aov = cgutils.create_struct_proxy(kjb__nvvle)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    lnr__gez = []
    for i, aov__gei in enumerate(toty.data):
        qheo__hlia = fromty.data[i]
        if aov__gei != qheo__hlia:
            hav__qkegl = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*hav__qkegl)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        nme__srexv = kjb__nvvle.type_to_blk[qheo__hlia]
        iwb__nga = getattr(herwd__aov, f'block_{nme__srexv}')
        gdja__gksth = ListInstance(context, builder, types.List(qheo__hlia),
            iwb__nga)
        suhb__hyl = context.get_constant(types.int64, kjb__nvvle.
            block_offsets[i])
        xrzei__qnd = gdja__gksth.getitem(suhb__hyl)
        if aov__gei != qheo__hlia:
            ior__amr = context.cast(builder, xrzei__qnd, qheo__hlia, aov__gei)
        else:
            ior__amr = xrzei__qnd
            context.nrt.incref(builder, aov__gei, ior__amr)
        lnr__gez.append(ior__amr)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), lnr__gez)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    sksg__rtf, tkvv__bbv, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    amceh__sdqx = ColNamesMetaType(tuple(sksg__rtf))
    ikd__gdw = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    ikd__gdw += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(tkvv__bbv, index_arg))
    loh__npi = {}
    exec(ikd__gdw, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': amceh__sdqx}, loh__npi)
    moh__fce = loh__npi['_init_df']
    return moh__fce


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    xcszr__blz = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(xcszr__blz, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    xcszr__blz = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(xcszr__blz, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    opi__ydh = ''
    if not is_overload_none(dtype):
        opi__ydh = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        qoao__agt = (len(data.types) - 1) // 2
        vunlt__sky = [aov__gei.literal_value for aov__gei in data.types[1:
            qoao__agt + 1]]
        data_val_types = dict(zip(vunlt__sky, data.types[qoao__agt + 1:]))
        lnr__gez = ['data[{}]'.format(i) for i in range(qoao__agt + 1, 2 *
            qoao__agt + 1)]
        data_dict = dict(zip(vunlt__sky, lnr__gez))
        if is_overload_none(index):
            for i, aov__gei in enumerate(data.types[qoao__agt + 1:]):
                if isinstance(aov__gei, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(qoao__agt + 1 + i))
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
        mkgr__kaqz = '.copy()' if copy else ''
        jml__wsx = get_overload_const_list(columns)
        qoao__agt = len(jml__wsx)
        data_val_types = {weog__fok: data.copy(ndim=1) for weog__fok in
            jml__wsx}
        lnr__gez = ['data[:,{}]{}'.format(i, mkgr__kaqz) for i in range(
            qoao__agt)]
        data_dict = dict(zip(jml__wsx, lnr__gez))
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
    tkvv__bbv = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[weog__fok], df_len, opi__ydh) for weog__fok in
        col_names))
    if len(col_names) == 0:
        tkvv__bbv = '()'
    return col_names, tkvv__bbv, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for weog__fok in col_names:
        if weog__fok in data_dict and is_iterable_type(data_val_types[
            weog__fok]):
            df_len = 'len({})'.format(data_dict[weog__fok])
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
    if all(weog__fok in data_dict for weog__fok in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    xznk__jmz = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for weog__fok in col_names:
        if weog__fok not in data_dict:
            data_dict[weog__fok] = xznk__jmz


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
            aov__gei = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(aov__gei)
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
        lfin__rmmo = idx.literal_value
        if isinstance(lfin__rmmo, int):
            lslkg__hzv = tup.types[lfin__rmmo]
        elif isinstance(lfin__rmmo, slice):
            lslkg__hzv = types.BaseTuple.from_types(tup.types[lfin__rmmo])
        return signature(lslkg__hzv, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    bde__ifeql, idx = sig.args
    idx = idx.literal_value
    tup, crndt__tcs = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(bde__ifeql)
        if not 0 <= idx < len(bde__ifeql):
            raise IndexError('cannot index at %d in %s' % (idx, bde__ifeql))
        kvfao__rtif = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        ddyz__mvgsh = cgutils.unpack_tuple(builder, tup)[idx]
        kvfao__rtif = context.make_tuple(builder, sig.return_type, ddyz__mvgsh)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, kvfao__rtif)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, notv__vhx, suffix_x,
            suffix_y, is_join, indicator, crndt__tcs, crndt__tcs) = args
        how = get_overload_const_str(notv__vhx)
        if how == 'cross':
            data = left_df.data + right_df.data
            columns = left_df.columns + right_df.columns
            agq__rjsei = DataFrameType(data, RangeIndexType(types.none),
                columns, is_table_format=True)
            return signature(agq__rjsei, *args)
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        kbwg__ila = {weog__fok: i for i, weog__fok in enumerate(left_on)}
        zxum__uvfr = {weog__fok: i for i, weog__fok in enumerate(right_on)}
        exyg__buc = set(left_on) & set(right_on)
        cfpgq__uey = set(left_df.columns) & set(right_df.columns)
        pfgey__fip = cfpgq__uey - exyg__buc
        uppra__qdgdg = '$_bodo_index_' in left_on
        bdomf__tiks = '$_bodo_index_' in right_on
        bzqj__vcmkp = how in {'left', 'outer'}
        ljtse__efz = how in {'right', 'outer'}
        columns = []
        data = []
        if uppra__qdgdg or bdomf__tiks:
            if uppra__qdgdg:
                ekfk__dyf = bodo.utils.typing.get_index_data_arr_types(left_df
                    .index)[0]
            else:
                ekfk__dyf = left_df.data[left_df.column_index[left_on[0]]]
            if bdomf__tiks:
                rsch__otp = bodo.utils.typing.get_index_data_arr_types(right_df
                    .index)[0]
            else:
                rsch__otp = right_df.data[right_df.column_index[right_on[0]]]
        if uppra__qdgdg and not bdomf__tiks and not is_join.literal_value:
            ywobz__deeid = right_on[0]
            if ywobz__deeid in left_df.column_index:
                columns.append(ywobz__deeid)
                if (rsch__otp == bodo.dict_str_arr_type and ekfk__dyf ==
                    bodo.string_array_type):
                    ldvd__lue = bodo.string_array_type
                else:
                    ldvd__lue = rsch__otp
                data.append(ldvd__lue)
        if bdomf__tiks and not uppra__qdgdg and not is_join.literal_value:
            qxo__jza = left_on[0]
            if qxo__jza in right_df.column_index:
                columns.append(qxo__jza)
                if (ekfk__dyf == bodo.dict_str_arr_type and rsch__otp ==
                    bodo.string_array_type):
                    ldvd__lue = bodo.string_array_type
                else:
                    ldvd__lue = ekfk__dyf
                data.append(ldvd__lue)
        for qheo__hlia, dsnv__zwqhf in zip(left_df.data, left_df.columns):
            columns.append(str(dsnv__zwqhf) + suffix_x.literal_value if 
                dsnv__zwqhf in pfgey__fip else dsnv__zwqhf)
            if dsnv__zwqhf in exyg__buc:
                if qheo__hlia == bodo.dict_str_arr_type:
                    qheo__hlia = right_df.data[right_df.column_index[
                        dsnv__zwqhf]]
                data.append(qheo__hlia)
            else:
                if (qheo__hlia == bodo.dict_str_arr_type and dsnv__zwqhf in
                    kbwg__ila):
                    if bdomf__tiks:
                        qheo__hlia = rsch__otp
                    else:
                        kozhm__wgpv = kbwg__ila[dsnv__zwqhf]
                        kxtd__bqfhv = right_on[kozhm__wgpv]
                        qheo__hlia = right_df.data[right_df.column_index[
                            kxtd__bqfhv]]
                if ljtse__efz:
                    qheo__hlia = to_nullable_type(qheo__hlia)
                data.append(qheo__hlia)
        for qheo__hlia, dsnv__zwqhf in zip(right_df.data, right_df.columns):
            if dsnv__zwqhf not in exyg__buc:
                columns.append(str(dsnv__zwqhf) + suffix_y.literal_value if
                    dsnv__zwqhf in pfgey__fip else dsnv__zwqhf)
                if (qheo__hlia == bodo.dict_str_arr_type and dsnv__zwqhf in
                    zxum__uvfr):
                    if uppra__qdgdg:
                        qheo__hlia = ekfk__dyf
                    else:
                        kozhm__wgpv = zxum__uvfr[dsnv__zwqhf]
                        nmx__kueh = left_on[kozhm__wgpv]
                        qheo__hlia = left_df.data[left_df.column_index[
                            nmx__kueh]]
                if bzqj__vcmkp:
                    qheo__hlia = to_nullable_type(qheo__hlia)
                data.append(qheo__hlia)
        mrhgu__gqlig = get_overload_const_bool(indicator)
        if mrhgu__gqlig:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        vxye__fkexf = False
        if uppra__qdgdg and bdomf__tiks and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            vxye__fkexf = True
        elif uppra__qdgdg and not bdomf__tiks:
            index_typ = right_df.index
            vxye__fkexf = True
        elif bdomf__tiks and not uppra__qdgdg:
            index_typ = left_df.index
            vxye__fkexf = True
        if vxye__fkexf and isinstance(index_typ, bodo.hiframes.pd_index_ext
            .RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        agq__rjsei = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(agq__rjsei, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    sms__hzqkl = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return sms__hzqkl._getvalue()


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
    jtz__fkpbf = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    mrg__fgs = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', jtz__fkpbf, mrg__fgs,
        package_name='pandas', module_name='General')
    ikd__gdw = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        kmvu__rpsg = 0
        tkvv__bbv = []
        names = []
        for i, jnrah__cedwc in enumerate(objs.types):
            assert isinstance(jnrah__cedwc, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(jnrah__cedwc, 'pandas.concat()')
            if isinstance(jnrah__cedwc, SeriesType):
                names.append(str(kmvu__rpsg))
                kmvu__rpsg += 1
                tkvv__bbv.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(jnrah__cedwc.columns)
                for zjap__chazv in range(len(jnrah__cedwc.data)):
                    tkvv__bbv.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, zjap__chazv))
        return bodo.hiframes.dataframe_impl._gen_init_df(ikd__gdw, names,
            ', '.join(tkvv__bbv), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(aov__gei, DataFrameType) for aov__gei in objs
            .types)
        juxjd__jlbu = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            juxjd__jlbu.extend(df.columns)
        juxjd__jlbu = list(dict.fromkeys(juxjd__jlbu).keys())
        itich__ftwsz = {}
        for kmvu__rpsg, weog__fok in enumerate(juxjd__jlbu):
            for i, df in enumerate(objs.types):
                if weog__fok in df.column_index:
                    itich__ftwsz[f'arr_typ{kmvu__rpsg}'] = df.data[df.
                        column_index[weog__fok]]
                    break
        assert len(itich__ftwsz) == len(juxjd__jlbu)
        pnyt__sawaq = []
        for kmvu__rpsg, weog__fok in enumerate(juxjd__jlbu):
            args = []
            for i, df in enumerate(objs.types):
                if weog__fok in df.column_index:
                    gazga__uvuu = df.column_index[weog__fok]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, gazga__uvuu))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, kmvu__rpsg))
            ikd__gdw += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'.
                format(kmvu__rpsg, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(ikd__gdw,
            juxjd__jlbu, ', '.join('A{}'.format(i) for i in range(len(
            juxjd__jlbu))), index, itich__ftwsz)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(aov__gei, SeriesType) for aov__gei in objs.types)
        ikd__gdw += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'.
            format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            ikd__gdw += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            ikd__gdw += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        ikd__gdw += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        loh__npi = {}
        exec(ikd__gdw, {'bodo': bodo, 'np': np, 'numba': numba}, loh__npi)
        return loh__npi['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for kmvu__rpsg, weog__fok in enumerate(df_type.columns):
            ikd__gdw += '  arrs{} = []\n'.format(kmvu__rpsg)
            ikd__gdw += '  for i in range(len(objs)):\n'
            ikd__gdw += '    df = objs[i]\n'
            ikd__gdw += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(kmvu__rpsg))
            ikd__gdw += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(kmvu__rpsg))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            ikd__gdw += '  arrs_index = []\n'
            ikd__gdw += '  for i in range(len(objs)):\n'
            ikd__gdw += '    df = objs[i]\n'
            ikd__gdw += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(ikd__gdw, df_type.
            columns, ', '.join('out_arr{}'.format(i) for i in range(len(
            df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        ikd__gdw += '  arrs = []\n'
        ikd__gdw += '  for i in range(len(objs)):\n'
        ikd__gdw += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        ikd__gdw += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            ikd__gdw += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            ikd__gdw += '  arrs_index = []\n'
            ikd__gdw += '  for i in range(len(objs)):\n'
            ikd__gdw += '    S = objs[i]\n'
            ikd__gdw += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            ikd__gdw += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        ikd__gdw += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        loh__npi = {}
        exec(ikd__gdw, {'bodo': bodo, 'np': np, 'numba': numba}, loh__npi)
        return loh__npi['impl']
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
        xcszr__blz = df.copy(index=index)
        return signature(xcszr__blz, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    kwysi__jyj = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return kwysi__jyj._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    jtz__fkpbf = dict(index=index, name=name)
    mrg__fgs = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', jtz__fkpbf, mrg__fgs,
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
        itich__ftwsz = (types.Array(types.int64, 1, 'C'),) + df.data
        plhx__xlol = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, itich__ftwsz)
        return signature(plhx__xlol, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    kwysi__jyj = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return kwysi__jyj._getvalue()


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
    kwysi__jyj = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return kwysi__jyj._getvalue()


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
    kwysi__jyj = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return kwysi__jyj._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    jygqi__agmy = get_overload_const_bool(check_duplicates)
    ioq__idfzw = not get_overload_const_bool(is_already_shuffled)
    suhmc__goutg = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    godk__ixgi = len(value_names) > 1
    ippax__enrbd = None
    hgij__ryac = None
    mkkw__wii = None
    zbjb__mihve = None
    gofzg__hfq = isinstance(values_tup, types.UniTuple)
    if gofzg__hfq:
        nhpz__ipjjk = [to_str_arr_if_dict_array(to_nullable_type(values_tup
            .dtype))]
    else:
        nhpz__ipjjk = [to_str_arr_if_dict_array(to_nullable_type(
            klyy__tsyzm)) for klyy__tsyzm in values_tup]
    ikd__gdw = 'def impl(\n'
    ikd__gdw += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    ikd__gdw += '):\n'
    ikd__gdw += "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n"
    if ioq__idfzw:
        ikd__gdw += '    if parallel:\n'
        ikd__gdw += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        qrlh__czaqf = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        ikd__gdw += f'        info_list = [{qrlh__czaqf}]\n'
        ikd__gdw += '        cpp_table = arr_info_list_to_table(info_list)\n'
        ikd__gdw += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        dnqwx__frh = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        wbc__ryos = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        wolb__vkhia = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        ikd__gdw += f'        index_tup = ({dnqwx__frh},)\n'
        ikd__gdw += f'        columns_tup = ({wbc__ryos},)\n'
        ikd__gdw += f'        values_tup = ({wolb__vkhia},)\n'
        ikd__gdw += '        delete_table(cpp_table)\n'
        ikd__gdw += '        delete_table(out_cpp_table)\n'
        ikd__gdw += '        ev_shuffle.finalize()\n'
    ikd__gdw += '    columns_arr = columns_tup[0]\n'
    if gofzg__hfq:
        ikd__gdw += '    values_arrs = [arr for arr in values_tup]\n'
    ikd__gdw += (
        "    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)\n"
        )
    ikd__gdw += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    ikd__gdw += '        index_tup\n'
    ikd__gdw += '    )\n'
    ikd__gdw += '    n_rows = len(unique_index_arr_tup[0])\n'
    ikd__gdw += '    num_values_arrays = len(values_tup)\n'
    ikd__gdw += '    n_unique_pivots = len(pivot_values)\n'
    if gofzg__hfq:
        ikd__gdw += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        ikd__gdw += '    n_cols = n_unique_pivots\n'
    ikd__gdw += '    col_map = {}\n'
    ikd__gdw += '    for i in range(n_unique_pivots):\n'
    ikd__gdw += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    ikd__gdw += '            raise ValueError(\n'
    ikd__gdw += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    ikd__gdw += '            )\n'
    ikd__gdw += '        col_map[pivot_values[i]] = i\n'
    ikd__gdw += '    ev_unique.finalize()\n'
    ikd__gdw += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    upf__pbakp = False
    for i, ywlx__hlbk in enumerate(nhpz__ipjjk):
        if is_str_arr_type(ywlx__hlbk):
            upf__pbakp = True
            ikd__gdw += (
                f'    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]\n'
                )
            ikd__gdw += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if upf__pbakp:
        if jygqi__agmy:
            ikd__gdw += '    nbytes = (n_rows + 7) >> 3\n'
            ikd__gdw += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        ikd__gdw += '    for i in range(len(columns_arr)):\n'
        ikd__gdw += '        col_name = columns_arr[i]\n'
        ikd__gdw += '        pivot_idx = col_map[col_name]\n'
        ikd__gdw += '        row_idx = row_vector[i]\n'
        if jygqi__agmy:
            ikd__gdw += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            ikd__gdw += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            ikd__gdw += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            ikd__gdw += '        else:\n'
            ikd__gdw += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if gofzg__hfq:
            ikd__gdw += '        for j in range(num_values_arrays):\n'
            ikd__gdw += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            ikd__gdw += '            len_arr = len_arrs_0[col_idx]\n'
            ikd__gdw += '            values_arr = values_arrs[j]\n'
            ikd__gdw += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            ikd__gdw += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            ikd__gdw += '                len_arr[row_idx] = str_val_len\n'
            ikd__gdw += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, ywlx__hlbk in enumerate(nhpz__ipjjk):
                if is_str_arr_type(ywlx__hlbk):
                    ikd__gdw += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    ikd__gdw += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    ikd__gdw += (
                        f'            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}\n'
                        )
                    ikd__gdw += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    ikd__gdw += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, ywlx__hlbk in enumerate(nhpz__ipjjk):
        if is_str_arr_type(ywlx__hlbk):
            ikd__gdw += f'    data_arrs_{i} = [\n'
            ikd__gdw += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            ikd__gdw += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            ikd__gdw += '        )\n'
            ikd__gdw += '        for i in range(n_cols)\n'
            ikd__gdw += '    ]\n'
            ikd__gdw += f'    if tracing.is_tracing():\n'
            ikd__gdw += '         for i in range(n_cols):\n'
            ikd__gdw += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            ikd__gdw += f'    data_arrs_{i} = [\n'
            ikd__gdw += (
                f'        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})\n'
                )
            ikd__gdw += '        for _ in range(n_cols)\n'
            ikd__gdw += '    ]\n'
    if not upf__pbakp and jygqi__agmy:
        ikd__gdw += '    nbytes = (n_rows + 7) >> 3\n'
        ikd__gdw += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    ikd__gdw += '    ev_alloc.finalize()\n'
    ikd__gdw += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    ikd__gdw += '    for i in range(len(columns_arr)):\n'
    ikd__gdw += '        col_name = columns_arr[i]\n'
    ikd__gdw += '        pivot_idx = col_map[col_name]\n'
    ikd__gdw += '        row_idx = row_vector[i]\n'
    if not upf__pbakp and jygqi__agmy:
        ikd__gdw += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        ikd__gdw += (
            '        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):\n'
            )
        ikd__gdw += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        ikd__gdw += '        else:\n'
        ikd__gdw += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if gofzg__hfq:
        ikd__gdw += '        for j in range(num_values_arrays):\n'
        ikd__gdw += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        ikd__gdw += '            col_arr = data_arrs_0[col_idx]\n'
        ikd__gdw += '            values_arr = values_arrs[j]\n'
        ikd__gdw += """            bodo.libs.array_kernels.copy_array_element(col_arr, row_idx, values_arr, i)
"""
    else:
        for i, ywlx__hlbk in enumerate(nhpz__ipjjk):
            ikd__gdw += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            ikd__gdw += f"""        bodo.libs.array_kernels.copy_array_element(col_arr_{i}, row_idx, values_tup[{i}], i)
"""
    if len(index_names) == 1:
        ikd__gdw += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        ippax__enrbd = index_names.meta[0]
    else:
        ikd__gdw += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        ippax__enrbd = tuple(index_names.meta)
    ikd__gdw += f'    if tracing.is_tracing():\n'
    ikd__gdw += f'        index_nbytes = index.nbytes\n'
    ikd__gdw += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not suhmc__goutg:
        mkkw__wii = columns_name.meta[0]
        if godk__ixgi:
            ikd__gdw += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            hgij__ryac = value_names.meta
            if all(isinstance(weog__fok, str) for weog__fok in hgij__ryac):
                hgij__ryac = pd.array(hgij__ryac, 'string')
            elif all(isinstance(weog__fok, int) for weog__fok in hgij__ryac):
                hgij__ryac = np.array(hgij__ryac, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(hgij__ryac.dtype, pd.StringDtype):
                ikd__gdw += '    total_chars = 0\n'
                ikd__gdw += f'    for i in range({len(value_names)}):\n'
                ikd__gdw += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                ikd__gdw += '        total_chars += value_name_str_len\n'
                ikd__gdw += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                ikd__gdw += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                ikd__gdw += '    total_chars = 0\n'
                ikd__gdw += '    for i in range(len(pivot_values)):\n'
                ikd__gdw += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                ikd__gdw += '        total_chars += pivot_val_str_len\n'
                ikd__gdw += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                ikd__gdw += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            ikd__gdw += f'    for i in range({len(value_names)}):\n'
            ikd__gdw += '        for j in range(len(pivot_values)):\n'
            ikd__gdw += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            ikd__gdw += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            ikd__gdw += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            ikd__gdw += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    ikd__gdw += '    ev_fill.finalize()\n'
    kjb__nvvle = None
    if suhmc__goutg:
        if godk__ixgi:
            rtu__xlm = []
            for zilw__eee in _constant_pivot_values.meta:
                for hbp__eytb in value_names.meta:
                    rtu__xlm.append((zilw__eee, hbp__eytb))
            column_names = tuple(rtu__xlm)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        zbjb__mihve = ColNamesMetaType(column_names)
        oiqw__cfwmr = []
        for klyy__tsyzm in nhpz__ipjjk:
            oiqw__cfwmr.extend([klyy__tsyzm] * len(_constant_pivot_values))
        qaht__ufcj = tuple(oiqw__cfwmr)
        kjb__nvvle = TableType(qaht__ufcj)
        ikd__gdw += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        ikd__gdw += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, klyy__tsyzm in enumerate(nhpz__ipjjk):
            ikd__gdw += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {kjb__nvvle.type_to_blk[klyy__tsyzm]})
"""
        ikd__gdw += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        ikd__gdw += '        (table,), index, columns_typ\n'
        ikd__gdw += '    )\n'
    else:
        davy__duba = ', '.join(f'data_arrs_{i}' for i in range(len(
            nhpz__ipjjk)))
        ikd__gdw += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({davy__duba},), n_rows)
"""
        ikd__gdw += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
            )
        ikd__gdw += '        (table,), index, column_index\n'
        ikd__gdw += '    )\n'
    ikd__gdw += '    ev.finalize()\n'
    ikd__gdw += '    return result\n'
    loh__npi = {}
    fglle__iftiv = {f'data_arr_typ_{i}': ywlx__hlbk for i, ywlx__hlbk in
        enumerate(nhpz__ipjjk)}
    denfw__ihxym = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        kjb__nvvle, 'columns_typ': zbjb__mihve, 'index_names_lit':
        ippax__enrbd, 'value_names_lit': hgij__ryac, 'columns_name_lit':
        mkkw__wii, **fglle__iftiv, 'tracing': tracing}
    exec(ikd__gdw, denfw__ihxym, loh__npi)
    impl = loh__npi['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    jjo__faxic = {}
    jjo__faxic['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, pmnx__mji in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        dgocn__qusm = None
        if isinstance(pmnx__mji, bodo.DatetimeArrayType):
            ndz__xth = 'datetimetz'
            wysf__dhzu = 'datetime64[ns]'
            if isinstance(pmnx__mji.tz, int):
                uqspd__fub = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(pmnx__mji.tz))
            else:
                uqspd__fub = pd.DatetimeTZDtype(tz=pmnx__mji.tz).tz
            dgocn__qusm = {'timezone': pa.lib.tzinfo_to_string(uqspd__fub)}
        elif isinstance(pmnx__mji, types.Array) or pmnx__mji == boolean_array:
            ndz__xth = wysf__dhzu = pmnx__mji.dtype.name
            if wysf__dhzu.startswith('datetime'):
                ndz__xth = 'datetime'
        elif is_str_arr_type(pmnx__mji):
            ndz__xth = 'unicode'
            wysf__dhzu = 'object'
        elif pmnx__mji == binary_array_type:
            ndz__xth = 'bytes'
            wysf__dhzu = 'object'
        elif isinstance(pmnx__mji, DecimalArrayType):
            ndz__xth = wysf__dhzu = 'object'
        elif isinstance(pmnx__mji, IntegerArrayType):
            liju__jxm = pmnx__mji.dtype.name
            if liju__jxm.startswith('int'):
                wysf__dhzu = 'Int' + liju__jxm[3:]
            elif liju__jxm.startswith('uint'):
                wysf__dhzu = 'UInt' + liju__jxm[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, pmnx__mji))
            ndz__xth = pmnx__mji.dtype.name
        elif isinstance(pmnx__mji, bodo.FloatingArrayType):
            liju__jxm = pmnx__mji.dtype.name
            ndz__xth = liju__jxm
            wysf__dhzu = liju__jxm.capitalize()
        elif pmnx__mji == datetime_date_array_type:
            ndz__xth = 'datetime'
            wysf__dhzu = 'object'
        elif isinstance(pmnx__mji, TimeArrayType):
            ndz__xth = 'datetime'
            wysf__dhzu = 'object'
        elif isinstance(pmnx__mji, (StructArrayType, ArrayItemArrayType)):
            ndz__xth = 'object'
            wysf__dhzu = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, pmnx__mji))
        gvxn__wix = {'name': col_name, 'field_name': col_name,
            'pandas_type': ndz__xth, 'numpy_type': wysf__dhzu, 'metadata':
            dgocn__qusm}
        jjo__faxic['columns'].append(gvxn__wix)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            dfk__egp = '__index_level_0__'
            jvg__tegt = None
        else:
            dfk__egp = '%s'
            jvg__tegt = '%s'
        jjo__faxic['index_columns'] = [dfk__egp]
        jjo__faxic['columns'].append({'name': jvg__tegt, 'field_name':
            dfk__egp, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        jjo__faxic['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        jjo__faxic['index_columns'] = []
    jjo__faxic['pandas_version'] = pd.__version__
    return jjo__faxic


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
        cexe__zany = []
        for zeg__yshh in partition_cols:
            try:
                idx = df.columns.index(zeg__yshh)
            except ValueError as labe__hudph:
                raise BodoError(
                    f'Partition column {zeg__yshh} is not in dataframe')
            cexe__zany.append(idx)
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
    sxr__enzqy = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType
        )
    zkf__igzv = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not sxr__enzqy)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not sxr__enzqy or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and sxr__enzqy and not is_overload_true(_is_parallel)
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
        dojpd__yrme = df.runtime_data_types
        qxzhx__ercz = len(dojpd__yrme)
        dgocn__qusm = gen_pandas_parquet_metadata([''] * qxzhx__ercz,
            dojpd__yrme, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        wjh__cuuw = dgocn__qusm['columns'][:qxzhx__ercz]
        dgocn__qusm['columns'] = dgocn__qusm['columns'][qxzhx__ercz:]
        wjh__cuuw = [json.dumps(witkm__scqe).replace('""', '{0}') for
            witkm__scqe in wjh__cuuw]
        ktxrj__bmbuz = json.dumps(dgocn__qusm)
        kjxqa__dhnj = '"columns": ['
        zkb__cke = ktxrj__bmbuz.find(kjxqa__dhnj)
        if zkb__cke == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        aja__gqv = zkb__cke + len(kjxqa__dhnj)
        axfjd__fte = ktxrj__bmbuz[:aja__gqv]
        ktxrj__bmbuz = ktxrj__bmbuz[aja__gqv:]
        dkgvo__czam = len(dgocn__qusm['columns'])
    else:
        ktxrj__bmbuz = json.dumps(gen_pandas_parquet_metadata(df.columns,
            df.data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and sxr__enzqy:
        ktxrj__bmbuz = ktxrj__bmbuz.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            ktxrj__bmbuz = ktxrj__bmbuz.replace('"%s"', '%s')
    if not df.is_table_format:
        tkvv__bbv = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    ikd__gdw = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        ikd__gdw += '    py_table = get_dataframe_table(df)\n'
        ikd__gdw += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        ikd__gdw += '    info_list = [{}]\n'.format(tkvv__bbv)
        ikd__gdw += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        ikd__gdw += '    columns_index = get_dataframe_column_names(df)\n'
        ikd__gdw += '    names_arr = index_to_array(columns_index)\n'
        ikd__gdw += '    col_names = array_to_info(names_arr)\n'
    else:
        ikd__gdw += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and zkf__igzv:
        ikd__gdw += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        wlji__jue = True
    else:
        ikd__gdw += '    index_col = array_to_info(np.empty(0))\n'
        wlji__jue = False
    if df.has_runtime_cols:
        ikd__gdw += '    columns_lst = []\n'
        ikd__gdw += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            ikd__gdw += f'    for _ in range(len(py_table.block_{i})):\n'
            ikd__gdw += f"""        columns_lst.append({wjh__cuuw[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            ikd__gdw += '        num_cols += 1\n'
        if dkgvo__czam:
            ikd__gdw += "    columns_lst.append('')\n"
        ikd__gdw += '    columns_str = ", ".join(columns_lst)\n'
        ikd__gdw += ('    metadata = """' + axfjd__fte +
            '""" + columns_str + """' + ktxrj__bmbuz + '"""\n')
    else:
        ikd__gdw += '    metadata = """' + ktxrj__bmbuz + '"""\n'
    ikd__gdw += '    if compression is None:\n'
    ikd__gdw += "        compression = 'none'\n"
    ikd__gdw += '    if _bodo_timestamp_tz is None:\n'
    ikd__gdw += "        _bodo_timestamp_tz = ''\n"
    ikd__gdw += '    if df.index.name is not None:\n'
    ikd__gdw += '        name_ptr = df.index.name\n'
    ikd__gdw += '    else:\n'
    ikd__gdw += "        name_ptr = 'null'\n"
    ikd__gdw += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    fkupx__ebthz = None
    if partition_cols:
        fkupx__ebthz = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        ngwsr__dyhg = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in cexe__zany)
        if ngwsr__dyhg:
            ikd__gdw += '    cat_info_list = [{}]\n'.format(ngwsr__dyhg)
            ikd__gdw += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            ikd__gdw += '    cat_table = table\n'
        ikd__gdw += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        ikd__gdw += (
            f'    part_cols_idxs = np.array({cexe__zany}, dtype=np.int32)\n')
        ikd__gdw += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        ikd__gdw += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        ikd__gdw += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        ikd__gdw += (
            '                            unicode_to_utf8(compression),\n')
        ikd__gdw += '                            _is_parallel,\n'
        ikd__gdw += (
            '                            unicode_to_utf8(bucket_region),\n')
        ikd__gdw += '                            row_group_size,\n'
        ikd__gdw += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        ikd__gdw += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        ikd__gdw += '    delete_table_decref_arrays(table)\n'
        ikd__gdw += '    delete_info_decref_array(index_col)\n'
        ikd__gdw += '    delete_info_decref_array(col_names_no_partitions)\n'
        ikd__gdw += '    delete_info_decref_array(col_names)\n'
        if ngwsr__dyhg:
            ikd__gdw += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        ikd__gdw += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        ikd__gdw += (
            '                            table, col_names, index_col,\n')
        ikd__gdw += '                            ' + str(wlji__jue) + ',\n'
        ikd__gdw += '                            unicode_to_utf8(metadata),\n'
        ikd__gdw += (
            '                            unicode_to_utf8(compression),\n')
        ikd__gdw += (
            '                            _is_parallel, 1, df.index.start,\n')
        ikd__gdw += (
            '                            df.index.stop, df.index.step,\n')
        ikd__gdw += '                            unicode_to_utf8(name_ptr),\n'
        ikd__gdw += (
            '                            unicode_to_utf8(bucket_region),\n')
        ikd__gdw += '                            row_group_size,\n'
        ikd__gdw += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        ikd__gdw += '                              False,\n'
        ikd__gdw += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        ikd__gdw += '                              False)\n'
        ikd__gdw += '    delete_table_decref_arrays(table)\n'
        ikd__gdw += '    delete_info_decref_array(index_col)\n'
        ikd__gdw += '    delete_info_decref_array(col_names)\n'
    else:
        ikd__gdw += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        ikd__gdw += (
            '                            table, col_names, index_col,\n')
        ikd__gdw += '                            ' + str(wlji__jue) + ',\n'
        ikd__gdw += '                            unicode_to_utf8(metadata),\n'
        ikd__gdw += (
            '                            unicode_to_utf8(compression),\n')
        ikd__gdw += '                            _is_parallel, 0, 0, 0, 0,\n'
        ikd__gdw += '                            unicode_to_utf8(name_ptr),\n'
        ikd__gdw += (
            '                            unicode_to_utf8(bucket_region),\n')
        ikd__gdw += '                            row_group_size,\n'
        ikd__gdw += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        ikd__gdw += '                              False,\n'
        ikd__gdw += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        ikd__gdw += '                              False)\n'
        ikd__gdw += '    delete_table_decref_arrays(table)\n'
        ikd__gdw += '    delete_info_decref_array(index_col)\n'
        ikd__gdw += '    delete_info_decref_array(col_names)\n'
    loh__npi = {}
    if df.has_runtime_cols:
        blc__hwzvd = None
    else:
        for dsnv__zwqhf in df.columns:
            if not isinstance(dsnv__zwqhf, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        blc__hwzvd = pd.array(df.columns)
    exec(ikd__gdw, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': blc__hwzvd,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': fkupx__ebthz,
        'get_dataframe_column_names': get_dataframe_column_names,
        'fix_arr_dtype': fix_arr_dtype, 'decode_if_dict_array':
        decode_if_dict_array, 'decode_if_dict_table': decode_if_dict_table},
        loh__npi)
    gni__wsxnk = loh__npi['df_to_parquet']
    return gni__wsxnk


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    acdoz__trpu = tracing.Event('to_sql_exception_guard', is_parallel=
        _is_parallel)
    ynh__ysdvv = 'all_ok'
    nvuea__xmx, blz__xgp = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        fmi__iyet = 100
        if chunksize is None:
            casd__cns = fmi__iyet
        else:
            casd__cns = min(chunksize, fmi__iyet)
        if _is_table_create:
            df = df.iloc[:casd__cns, :]
        else:
            df = df.iloc[casd__cns:, :]
            if len(df) == 0:
                return ynh__ysdvv
    tqyy__dexm = df.columns
    try:
        if nvuea__xmx == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            azm__qrwa = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            mdt__hzgk = bodo.typeof(df)
            ghw__etqz = {}
            for weog__fok, qgkxu__ghnyr in zip(mdt__hzgk.columns, mdt__hzgk
                .data):
                if df[weog__fok].dtype == 'object':
                    if qgkxu__ghnyr == datetime_date_array_type:
                        ghw__etqz[weog__fok] = sa.types.Date
                    elif qgkxu__ghnyr in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not azm__qrwa or azm__qrwa ==
                        '0'):
                        ghw__etqz[weog__fok] = VARCHAR2(4000)
            dtype = ghw__etqz
        try:
            jwfy__zomtx = tracing.Event('df_to_sql', is_parallel=_is_parallel)
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
            jwfy__zomtx.finalize()
        except Exception as xmr__ekaro:
            ynh__ysdvv = xmr__ekaro.args[0]
            if nvuea__xmx == 'oracle' and 'ORA-12899' in ynh__ysdvv:
                ynh__ysdvv += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return ynh__ysdvv
    finally:
        df.columns = tqyy__dexm
        acdoz__trpu.finalize()


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    acdoz__trpu = tracing.Event('to_sql_exception_guard_encaps',
        is_parallel=_is_parallel)
    with numba.objmode(out='unicode_type'):
        gjwnu__cnpsn = tracing.Event('to_sql_exception_guard_encaps:objmode',
            is_parallel=_is_parallel)
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
        gjwnu__cnpsn.finalize()
    acdoz__trpu.finalize()
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
    for dsnv__zwqhf in df.columns:
        if not isinstance(dsnv__zwqhf, str):
            raise BodoError(
                'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
    blc__hwzvd = pd.array(df.columns)
    ikd__gdw = """def df_to_sql(
    df, name, con,
    schema=None, if_exists='fail', index=True,
    index_label=None, chunksize=None, dtype=None,
    method=None, _bodo_allow_downcasting=False,
    _is_parallel=False,
):
"""
    ikd__gdw += """    if con.startswith('iceberg'):
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
        ikd__gdw += f'        py_table = get_dataframe_table(df)\n'
        ikd__gdw += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        tkvv__bbv = ', '.join(f'array_to_info(get_dataframe_data(df, {i}))' for
            i in range(len(df.columns)))
        ikd__gdw += f'        info_list = [{tkvv__bbv}]\n'
        ikd__gdw += f'        table = arr_info_list_to_table(info_list)\n'
    ikd__gdw += """        col_names = array_to_info(col_names_arr)
        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names,
            if_exists, _is_parallel, pyarrow_table_schema,
            _bodo_allow_downcasting,
        )
        delete_table_decref_arrays(table)
        delete_info_decref_array(col_names)
"""
    ikd__gdw += "    elif con.startswith('snowflake'):\n"
    ikd__gdw += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        if _bodo_allow_downcasting and bodo.get_rank() == 0:
            warnings.warn('_bodo_allow_downcasting is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl', sync=False)
"""
    ikd__gdw += "        location = ''\n"
    if not is_overload_none(schema):
        ikd__gdw += '        location += \'"\' + schema + \'".\'\n'
    ikd__gdw += '        location += name\n'
    ikd__gdw += '        my_rank = bodo.get_rank()\n'
    ikd__gdw += """        with bodo.objmode(
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
    ikd__gdw += '        bodo.barrier()\n'
    ikd__gdw += '        if azure_stage_direct_upload:\n'
    ikd__gdw += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    ikd__gdw += '        if chunksize is None:\n'
    ikd__gdw += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        ikd__gdw += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        eohpn__uxpcf = ',' if len(df.columns) == 1 else ''
        ikd__gdw += (
            f'            memory_usage = np.array(({data}{eohpn__uxpcf}), np.int64).sum()\n'
            )
    ikd__gdw += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        ikd__gdw += '        columns_index = get_dataframe_column_names(df)\n'
        ikd__gdw += '        names_arr = index_to_array(columns_index)\n'
        ikd__gdw += '        col_names = array_to_info(names_arr)\n'
    else:
        ikd__gdw += '        col_names = array_to_info(col_names_arr)\n'
    ikd__gdw += '        index_col = array_to_info(np.empty(0))\n'
    ikd__gdw += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    ikd__gdw += (
        "        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           \n"
        )
    ikd__gdw += '        upload_threads_in_progress = []\n'
    ikd__gdw += (
        '        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           \n'
        )
    ikd__gdw += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    ikd__gdw += '            chunk_path = parquet_path + chunk_name\n'
    ikd__gdw += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    ikd__gdw += '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n'
    ikd__gdw += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    ikd__gdw += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        ikd__gdw += '            py_table_chunk = get_dataframe_table(chunk)\n'
        ikd__gdw += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        ezhu__irjn = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        ikd__gdw += (
            f'            table_chunk = arr_info_list_to_table([{ezhu__irjn}])     \n'
            )
    ikd__gdw += '            ev_to_df_table.finalize()\n'
    ikd__gdw += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
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
    ikd__gdw += '        bodo.barrier()\n'
    ejgxn__cltpx = bodo.io.snowflake.gen_snowflake_schema(df.columns, df.data)
    ikd__gdw += f"""        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, {ejgxn__cltpx},
                if_exists, old_creds, tmp_folder,
                azure_stage_direct_upload, old_core_site,
                old_sas_token,
            )
"""
    ikd__gdw += '        if azure_stage_direct_upload:\n'
    ikd__gdw += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    ikd__gdw += '        ev.finalize()\n'
    ikd__gdw += '    else:\n'
    ikd__gdw += (
        '        if _bodo_allow_downcasting and bodo.get_rank() == 0:\n')
    ikd__gdw += """            warnings.warn('_bodo_allow_downcasting is not supported for SQL tables.')
"""
    ikd__gdw += '        rank = bodo.libs.distributed_api.get_rank()\n'
    ikd__gdw += "        err_msg = 'unset'\n"
    ikd__gdw += '        if rank != 0:\n'
    ikd__gdw += (
        '            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          \n'
        )
    ikd__gdw += '        elif rank == 0:\n'
    ikd__gdw += '            err_msg = to_sql_exception_guard_encaps(\n'
    ikd__gdw += (
        '                          df, name, con, schema, if_exists, index, index_label,\n'
        )
    ikd__gdw += '                          chunksize, dtype, method,\n'
    ikd__gdw += '                          True, _is_parallel,\n'
    ikd__gdw += '                      )\n'
    ikd__gdw += (
        '            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          \n'
        )
    ikd__gdw += "        if_exists = 'append'\n"
    ikd__gdw += "        if _is_parallel and err_msg == 'all_ok':\n"
    ikd__gdw += '            err_msg = to_sql_exception_guard_encaps(\n'
    ikd__gdw += (
        '                          df, name, con, schema, if_exists, index, index_label,\n'
        )
    ikd__gdw += '                          chunksize, dtype, method,\n'
    ikd__gdw += '                          False, _is_parallel,\n'
    ikd__gdw += '                      )\n'
    ikd__gdw += "        if err_msg != 'all_ok':\n"
    ikd__gdw += "            print('err_msg=', err_msg)\n"
    ikd__gdw += "            raise ValueError('error in to_sql() operation')\n"
    loh__npi = {}
    denfw__ihxym = globals().copy()
    denfw__ihxym.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        blc__hwzvd, 'delete_info_decref_array': delete_info_decref_array,
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
    exec(ikd__gdw, denfw__ihxym, loh__npi)
    _impl = loh__npi['df_to_sql']
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
        spd__xsz = get_overload_const_str(path_or_buf)
        if spd__xsz.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        smid__itbyt = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(smid__itbyt), unicode_to_utf8(
                _bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(smid__itbyt), unicode_to_utf8(
                _bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    kveu__muhfv = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    qab__iedxg = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', kveu__muhfv, qab__iedxg,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    ikd__gdw = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        kvl__ksn = data.data.dtype.categories
        ikd__gdw += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        kvl__ksn = data.dtype.categories
        ikd__gdw += '  data_values = data\n'
    qoao__agt = len(kvl__ksn)
    ikd__gdw += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    ikd__gdw += '  numba.parfors.parfor.init_prange()\n'
    ikd__gdw += '  n = len(data_values)\n'
    for i in range(qoao__agt):
        ikd__gdw += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    ikd__gdw += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    ikd__gdw += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for zjap__chazv in range(qoao__agt):
        ikd__gdw += '          data_arr_{}[i] = 0\n'.format(zjap__chazv)
    ikd__gdw += '      else:\n'
    for jmnik__qesx in range(qoao__agt):
        ikd__gdw += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            jmnik__qesx)
    tkvv__bbv = ', '.join(f'data_arr_{i}' for i in range(qoao__agt))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(kvl__ksn[0], np.datetime64):
        kvl__ksn = tuple(pd.Timestamp(weog__fok) for weog__fok in kvl__ksn)
    elif isinstance(kvl__ksn[0], np.timedelta64):
        kvl__ksn = tuple(pd.Timedelta(weog__fok) for weog__fok in kvl__ksn)
    return bodo.hiframes.dataframe_impl._gen_init_df(ikd__gdw, kvl__ksn,
        tkvv__bbv, index)


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
    for izav__ofw in pd_unsupported:
        nlkpp__ygrj = mod_name + '.' + izav__ofw.__name__
        overload(izav__ofw, no_unliteral=True)(create_unsupported_overload(
            nlkpp__ygrj))


def _install_dataframe_unsupported():
    for uio__uyaf in dataframe_unsupported_attrs:
        xdjhc__dxuei = 'DataFrame.' + uio__uyaf
        overload_attribute(DataFrameType, uio__uyaf)(
            create_unsupported_overload(xdjhc__dxuei))
    for nlkpp__ygrj in dataframe_unsupported:
        xdjhc__dxuei = 'DataFrame.' + nlkpp__ygrj + '()'
        overload_method(DataFrameType, nlkpp__ygrj)(create_unsupported_overload
            (xdjhc__dxuei))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
