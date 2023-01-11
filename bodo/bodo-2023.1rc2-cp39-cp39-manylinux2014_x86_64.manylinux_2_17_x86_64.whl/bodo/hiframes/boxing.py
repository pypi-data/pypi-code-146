"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.ir_utils import GuardException, guard
from numba.core.typing import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, check_runtime_cols_unsupported, construct_dataframe
from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.float_arr_ext import FloatDtype, FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type, string_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
ll.add_symbol('is_np_array', hstr_ext.is_np_array)
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
TABLE_FORMAT_THRESHOLD = 20
_use_dict_str_type = False


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    bracp__kescl = tuple(val.columns.to_list())
    nwr__kvt = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        qqbg__aznd = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        qqbg__aznd = numba.typeof(val.index)
    rzolt__bzfhq = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    yywd__gdlp = len(nwr__kvt) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(nwr__kvt, qqbg__aznd, bracp__kescl, rzolt__bzfhq,
        is_table_format=yywd__gdlp)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    rzolt__bzfhq = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        wbme__jajyd = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        wbme__jajyd = numba.typeof(val.index)
    nmq__cas = _infer_series_arr_type(val)
    if _use_dict_str_type and nmq__cas == string_array_type:
        nmq__cas = bodo.dict_str_arr_type
    return SeriesType(nmq__cas.dtype, data=nmq__cas, index=wbme__jajyd,
        name_typ=numba.typeof(val.name), dist=rzolt__bzfhq)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    gwc__hgh = c.pyapi.object_getattr_string(val, 'index')
    hkpvc__vakjq = c.pyapi.to_native_value(typ.index, gwc__hgh).value
    c.pyapi.decref(gwc__hgh)
    if typ.is_table_format:
        quel__ofnqt = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        quel__ofnqt.parent = val
        for gqja__lyqqz, dxk__ospp in typ.table_type.type_to_blk.items():
            okl__gkl = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[dxk__ospp]))
            htc__ogu, tfzk__qma = ListInstance.allocate_ex(c.context, c.
                builder, types.List(gqja__lyqqz), okl__gkl)
            tfzk__qma.size = okl__gkl
            setattr(quel__ofnqt, f'block_{dxk__ospp}', tfzk__qma.value)
        rufyp__iywe = c.pyapi.call_method(val, '__len__', ())
        hugm__plxb = c.pyapi.long_as_longlong(rufyp__iywe)
        c.pyapi.decref(rufyp__iywe)
        quel__ofnqt.len = hugm__plxb
        wqzi__gvy = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [quel__ofnqt._getvalue()])
    else:
        hcfmq__sdlz = [c.context.get_constant_null(gqja__lyqqz) for
            gqja__lyqqz in typ.data]
        wqzi__gvy = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            hcfmq__sdlz)
    jhv__wvni = construct_dataframe(c.context, c.builder, typ, wqzi__gvy,
        hkpvc__vakjq, val, None)
    return NativeValue(jhv__wvni)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        otsg__hhrky = df._bodo_meta['type_metadata'][1]
    else:
        otsg__hhrky = [None] * len(df.columns)
    tpxb__zgz = [_infer_series_arr_type(df.iloc[:, i], array_metadata=
        otsg__hhrky[i]) for i in range(len(df.columns))]
    tpxb__zgz = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        gqja__lyqqz == string_array_type else gqja__lyqqz) for gqja__lyqqz in
        tpxb__zgz]
    return tuple(tpxb__zgz)


class SeriesDtypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Datime_Date = 13
    NP_Datetime64ns = 14
    NP_Timedelta64ns = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 21
    ARRAY = 22
    PD_nullable_Int8 = 23
    PD_nullable_UInt8 = 24
    PD_nullable_Int16 = 25
    PD_nullable_UInt16 = 26
    PD_nullable_Int32 = 27
    PD_nullable_UInt32 = 28
    PD_nullable_Int64 = 29
    PD_nullable_UInt64 = 30
    PD_nullable_bool = 31
    CategoricalType = 32
    NoneType = 33
    Literal = 34
    IntegerArray = 35
    RangeIndexType = 36
    DatetimeIndexType = 37
    NumericIndexType = 38
    PeriodIndexType = 39
    IntervalIndexType = 40
    CategoricalIndexType = 41
    StringIndexType = 42
    BinaryIndexType = 43
    TimedeltaIndexType = 44
    LiteralType = 45
    PD_nullable_Float32 = 46
    PD_nullable_Float64 = 47
    FloatingArray = 48


_one_to_one_type_to_enum_map = {types.int8: SeriesDtypeEnum.Int8.value,
    types.uint8: SeriesDtypeEnum.UInt8.value, types.int32: SeriesDtypeEnum.
    Int32.value, types.uint32: SeriesDtypeEnum.UInt32.value, types.int64:
    SeriesDtypeEnum.Int64.value, types.uint64: SeriesDtypeEnum.UInt64.value,
    types.float32: SeriesDtypeEnum.Float32.value, types.float64:
    SeriesDtypeEnum.Float64.value, types.NPDatetime('ns'): SeriesDtypeEnum.
    NP_Datetime64ns.value, types.NPTimedelta('ns'): SeriesDtypeEnum.
    NP_Timedelta64ns.value, types.bool_: SeriesDtypeEnum.Bool.value, types.
    int16: SeriesDtypeEnum.Int16.value, types.uint16: SeriesDtypeEnum.
    UInt16.value, types.Integer('int128', 128): SeriesDtypeEnum.Int128.
    value, bodo.hiframes.datetime_date_ext.datetime_date_type:
    SeriesDtypeEnum.Datime_Date.value, IntDtype(types.int8):
    SeriesDtypeEnum.PD_nullable_Int8.value, IntDtype(types.uint8):
    SeriesDtypeEnum.PD_nullable_UInt8.value, IntDtype(types.int16):
    SeriesDtypeEnum.PD_nullable_Int16.value, IntDtype(types.uint16):
    SeriesDtypeEnum.PD_nullable_UInt16.value, IntDtype(types.int32):
    SeriesDtypeEnum.PD_nullable_Int32.value, IntDtype(types.uint32):
    SeriesDtypeEnum.PD_nullable_UInt32.value, IntDtype(types.int64):
    SeriesDtypeEnum.PD_nullable_Int64.value, IntDtype(types.uint64):
    SeriesDtypeEnum.PD_nullable_UInt64.value, FloatDtype(types.float32):
    SeriesDtypeEnum.PD_nullable_Float32.value, FloatDtype(types.float64):
    SeriesDtypeEnum.PD_nullable_Float64.value, bytes_type: SeriesDtypeEnum.
    BINARY.value, string_type: SeriesDtypeEnum.STRING.value, bodo.bool_:
    SeriesDtypeEnum.Bool.value, types.none: SeriesDtypeEnum.NoneType.value}
_one_to_one_enum_to_type_map = {SeriesDtypeEnum.Int8.value: types.int8,
    SeriesDtypeEnum.UInt8.value: types.uint8, SeriesDtypeEnum.Int32.value:
    types.int32, SeriesDtypeEnum.UInt32.value: types.uint32,
    SeriesDtypeEnum.Int64.value: types.int64, SeriesDtypeEnum.UInt64.value:
    types.uint64, SeriesDtypeEnum.Float32.value: types.float32,
    SeriesDtypeEnum.Float64.value: types.float64, SeriesDtypeEnum.
    NP_Datetime64ns.value: types.NPDatetime('ns'), SeriesDtypeEnum.
    NP_Timedelta64ns.value: types.NPTimedelta('ns'), SeriesDtypeEnum.Int16.
    value: types.int16, SeriesDtypeEnum.UInt16.value: types.uint16,
    SeriesDtypeEnum.Int128.value: types.Integer('int128', 128),
    SeriesDtypeEnum.Datime_Date.value: bodo.hiframes.datetime_date_ext.
    datetime_date_type, SeriesDtypeEnum.PD_nullable_Int8.value: IntDtype(
    types.int8), SeriesDtypeEnum.PD_nullable_UInt8.value: IntDtype(types.
    uint8), SeriesDtypeEnum.PD_nullable_Int16.value: IntDtype(types.int16),
    SeriesDtypeEnum.PD_nullable_UInt16.value: IntDtype(types.uint16),
    SeriesDtypeEnum.PD_nullable_Int32.value: IntDtype(types.int32),
    SeriesDtypeEnum.PD_nullable_UInt32.value: IntDtype(types.uint32),
    SeriesDtypeEnum.PD_nullable_Int64.value: IntDtype(types.int64),
    SeriesDtypeEnum.PD_nullable_UInt64.value: IntDtype(types.uint64),
    SeriesDtypeEnum.PD_nullable_Float32.value: FloatDtype(types.float32),
    SeriesDtypeEnum.PD_nullable_Float64.value: FloatDtype(types.float64),
    SeriesDtypeEnum.BINARY.value: bytes_type, SeriesDtypeEnum.STRING.value:
    string_type, SeriesDtypeEnum.Bool.value: bodo.bool_, SeriesDtypeEnum.
    NoneType.value: types.none}


def _dtype_from_type_enum_list(typ_enum_list):
    gwv__rse, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(gwv__rse) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {gwv__rse}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        fxkws__kiy, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return fxkws__kiy, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.FloatingArray.value:
        fxkws__kiy, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return fxkws__kiy, FloatingArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        fxkws__kiy, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return fxkws__kiy, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        osmps__oyzle = typ_enum_list[1]
        akxt__sxwnc = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(osmps__oyzle, akxt__sxwnc)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        iozla__tucyn = typ_enum_list[1]
        odxvt__dmgq = tuple(typ_enum_list[2:2 + iozla__tucyn])
        dhdkm__xajaz = typ_enum_list[2 + iozla__tucyn:]
        ilpz__pignv = []
        for i in range(iozla__tucyn):
            dhdkm__xajaz, spcwz__kkve = _dtype_from_type_enum_list_recursor(
                dhdkm__xajaz)
            ilpz__pignv.append(spcwz__kkve)
        return dhdkm__xajaz, StructType(tuple(ilpz__pignv), odxvt__dmgq)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        erjmp__ixzpy = typ_enum_list[1]
        dhdkm__xajaz = typ_enum_list[2:]
        return dhdkm__xajaz, erjmp__ixzpy
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        erjmp__ixzpy = typ_enum_list[1]
        dhdkm__xajaz = typ_enum_list[2:]
        return dhdkm__xajaz, numba.types.literal(erjmp__ixzpy)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        dhdkm__xajaz, ykyg__ewzep = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        dhdkm__xajaz, vikmq__irddy = _dtype_from_type_enum_list_recursor(
            dhdkm__xajaz)
        dhdkm__xajaz, ukyb__iqhc = _dtype_from_type_enum_list_recursor(
            dhdkm__xajaz)
        dhdkm__xajaz, fzfb__pren = _dtype_from_type_enum_list_recursor(
            dhdkm__xajaz)
        dhdkm__xajaz, spkt__doel = _dtype_from_type_enum_list_recursor(
            dhdkm__xajaz)
        return dhdkm__xajaz, PDCategoricalDtype(ykyg__ewzep, vikmq__irddy,
            ukyb__iqhc, fzfb__pren, spkt__doel)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        dhdkm__xajaz, kjou__ogo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return dhdkm__xajaz, DatetimeIndexType(kjou__ogo)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        dhdkm__xajaz, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        dhdkm__xajaz, kjou__ogo = _dtype_from_type_enum_list_recursor(
            dhdkm__xajaz)
        dhdkm__xajaz, fzfb__pren = _dtype_from_type_enum_list_recursor(
            dhdkm__xajaz)
        return dhdkm__xajaz, NumericIndexType(dtype, kjou__ogo, fzfb__pren)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        dhdkm__xajaz, tovf__pah = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        dhdkm__xajaz, kjou__ogo = _dtype_from_type_enum_list_recursor(
            dhdkm__xajaz)
        return dhdkm__xajaz, PeriodIndexType(tovf__pah, kjou__ogo)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        dhdkm__xajaz, fzfb__pren = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        dhdkm__xajaz, kjou__ogo = _dtype_from_type_enum_list_recursor(
            dhdkm__xajaz)
        return dhdkm__xajaz, CategoricalIndexType(fzfb__pren, kjou__ogo)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        dhdkm__xajaz, kjou__ogo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return dhdkm__xajaz, RangeIndexType(kjou__ogo)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        dhdkm__xajaz, kjou__ogo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return dhdkm__xajaz, StringIndexType(kjou__ogo)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        dhdkm__xajaz, kjou__ogo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return dhdkm__xajaz, BinaryIndexType(kjou__ogo)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        dhdkm__xajaz, kjou__ogo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return dhdkm__xajaz, TimedeltaIndexType(kjou__ogo)
    else:
        raise_bodo_error(
            f'Unexpected Internal Error while converting typing metadata: unable to infer dtype for type enum {typ_enum_list[0]}. Please file the error here: https://github.com/Bodo-inc/Feedback'
            )


def _dtype_to_type_enum_list(typ):
    return guard(_dtype_to_type_enum_list_recursor, typ)


def _dtype_to_type_enum_list_recursor(typ, upcast_numeric_index=True):
    if typ.__hash__ and typ in _one_to_one_type_to_enum_map:
        return [_one_to_one_type_to_enum_map[typ]]
    if isinstance(typ, (dict, int, list, tuple, str, bool, bytes, float)):
        return [SeriesDtypeEnum.Literal.value, typ]
    elif typ is None:
        return [SeriesDtypeEnum.Literal.value, typ]
    elif is_overload_constant_int(typ):
        jqpj__ami = get_overload_const_int(typ)
        if numba.types.maybe_literal(jqpj__ami) == typ:
            return [SeriesDtypeEnum.LiteralType.value, jqpj__ami]
    elif is_overload_constant_str(typ):
        jqpj__ami = get_overload_const_str(typ)
        if numba.types.maybe_literal(jqpj__ami) == typ:
            return [SeriesDtypeEnum.LiteralType.value, jqpj__ami]
    elif is_overload_constant_bool(typ):
        jqpj__ami = get_overload_const_bool(typ)
        if numba.types.maybe_literal(jqpj__ami) == typ:
            return [SeriesDtypeEnum.LiteralType.value, jqpj__ami]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, FloatingArrayType):
        return [SeriesDtypeEnum.FloatingArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        ygtt__igqb = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for ihm__sogec in typ.names:
            ygtt__igqb.append(ihm__sogec)
        for qfbrn__whxsh in typ.data:
            ygtt__igqb += _dtype_to_type_enum_list_recursor(qfbrn__whxsh)
        return ygtt__igqb
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        dvt__kifl = _dtype_to_type_enum_list_recursor(typ.categories)
        ico__aaqkk = _dtype_to_type_enum_list_recursor(typ.elem_type)
        qyvjg__wad = _dtype_to_type_enum_list_recursor(typ.ordered)
        tij__vmjm = _dtype_to_type_enum_list_recursor(typ.data)
        blngb__mea = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + dvt__kifl + ico__aaqkk + qyvjg__wad + tij__vmjm + blngb__mea
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                ihb__jyy = types.float64
                if isinstance(typ.data, FloatingArrayType):
                    drmy__rcul = FloatingArrayType(ihb__jyy)
                else:
                    drmy__rcul = types.Array(ihb__jyy, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                ihb__jyy = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    drmy__rcul = IntegerArrayType(ihb__jyy)
                else:
                    drmy__rcul = types.Array(ihb__jyy, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                ihb__jyy = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    drmy__rcul = IntegerArrayType(ihb__jyy)
                else:
                    drmy__rcul = types.Array(ihb__jyy, 1, 'C')
            elif typ.dtype == types.bool_:
                ihb__jyy = typ.dtype
                drmy__rcul = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(ihb__jyy
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(drmy__rcul)
        else:
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(typ.dtype
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(typ.data)
    elif isinstance(typ, PeriodIndexType):
        return [SeriesDtypeEnum.PeriodIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.freq
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, CategoricalIndexType):
        return [SeriesDtypeEnum.CategoricalIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.data
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, RangeIndexType):
        return [SeriesDtypeEnum.RangeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, StringIndexType):
        return [SeriesDtypeEnum.StringIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, BinaryIndexType):
        return [SeriesDtypeEnum.BinaryIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, TimedeltaIndexType):
        return [SeriesDtypeEnum.TimedeltaIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    else:
        raise GuardException('Unable to convert type')


def _is_wrapper_pd_arr(arr):
    if isinstance(arr, pd.arrays.StringArray):
        return False
    return isinstance(arr, (pd.arrays.PandasArray, pd.arrays.TimedeltaArray)
        ) or isinstance(arr, pd.arrays.DatetimeArray) and arr.tz is None


def unwrap_pd_arr(arr):
    if _is_wrapper_pd_arr(arr):
        return np.ascontiguousarray(arr._ndarray)
    return arr


def _fix_series_arr_type(pd_arr):
    if _is_wrapper_pd_arr(pd_arr):
        return pd_arr._ndarray
    return pd_arr


def _infer_series_arr_type(S, array_metadata=None):
    if S.dtype == np.dtype('O'):
        if len(S.array) == 0 or S.isna().sum() == len(S):
            if array_metadata is not None:
                return _dtype_from_type_enum_list(array_metadata)
            elif hasattr(S, '_bodo_meta'
                ) and S._bodo_meta is not None and 'type_metadata' in S._bodo_meta and S._bodo_meta[
                'type_metadata'][1] is not None:
                yey__xlhov = S._bodo_meta['type_metadata'][1]
                return dtype_to_array_type(_dtype_from_type_enum_list(
                    yey__xlhov))
        return bodo.typeof(_fix_series_arr_type(S.array))
    try:
        pxp__czqan = bodo.typeof(_fix_series_arr_type(S.array))
        if pxp__czqan == types.Array(types.bool_, 1, 'C'):
            pxp__czqan = bodo.boolean_array
        if isinstance(pxp__czqan, types.Array):
            assert pxp__czqan.ndim == 1, 'invalid numpy array type in Series'
            pxp__czqan = types.Array(pxp__czqan.dtype, 1, 'C')
        return pxp__czqan
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    oepnx__sxsfh = cgutils.is_not_null(builder, parent_obj)
    kgbwn__qmfdg = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(oepnx__sxsfh):
        tnqmt__kxrd = pyapi.object_getattr_string(parent_obj, 'columns')
        rufyp__iywe = pyapi.call_method(tnqmt__kxrd, '__len__', ())
        builder.store(pyapi.long_as_longlong(rufyp__iywe), kgbwn__qmfdg)
        pyapi.decref(rufyp__iywe)
        pyapi.decref(tnqmt__kxrd)
    use_parent_obj = builder.and_(oepnx__sxsfh, builder.icmp_unsigned('==',
        builder.load(kgbwn__qmfdg), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        osoyq__xlss = df_typ.runtime_colname_typ
        context.nrt.incref(builder, osoyq__xlss, dataframe_payload.columns)
        return pyapi.from_native_value(osoyq__xlss, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        gqaog__qnntm = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        gqaog__qnntm = np.array(df_typ.columns, 'int64')
    else:
        gqaog__qnntm = df_typ.columns
    gfzq__qcwc = numba.typeof(gqaog__qnntm)
    hzq__qlc = context.get_constant_generic(builder, gfzq__qcwc, gqaog__qnntm)
    wxvlq__kyrl = pyapi.from_native_value(gfzq__qcwc, hzq__qlc, c.env_manager)
    if (gfzq__qcwc == bodo.string_array_type and bodo.libs.str_arr_ext.
        use_pd_pyarrow_string_array):
        off__cpr = wxvlq__kyrl
        wxvlq__kyrl = pyapi.call_method(wxvlq__kyrl, 'to_numpy', ())
        pyapi.decref(off__cpr)
    return wxvlq__kyrl


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (dmvy__ndipn, iybpq__ihk):
        with dmvy__ndipn:
            pyapi.incref(obj)
            suje__wsei = context.insert_const_string(c.builder.module, 'numpy')
            jlgdt__wkxn = pyapi.import_module_noblock(suje__wsei)
            if df_typ.has_runtime_cols:
                iizkk__tha = 0
            else:
                iizkk__tha = len(df_typ.columns)
            fupog__wew = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), iizkk__tha))
            vab__ydfdd = pyapi.call_method(jlgdt__wkxn, 'arange', (fupog__wew,)
                )
            pyapi.object_setattr_string(obj, 'columns', vab__ydfdd)
            pyapi.decref(jlgdt__wkxn)
            pyapi.decref(vab__ydfdd)
            pyapi.decref(fupog__wew)
        with iybpq__ihk:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            jbq__iliqr = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            suje__wsei = context.insert_const_string(c.builder.module, 'pandas'
                )
            jlgdt__wkxn = pyapi.import_module_noblock(suje__wsei)
            df_obj = pyapi.call_method(jlgdt__wkxn, 'DataFrame', (pyapi.
                borrow_none(), jbq__iliqr))
            pyapi.decref(jlgdt__wkxn)
            pyapi.decref(jbq__iliqr)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    muvir__yol = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = muvir__yol.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        ynnrg__reyfu = typ.table_type
        quel__ofnqt = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, ynnrg__reyfu, quel__ofnqt)
        vpb__rff = box_table(ynnrg__reyfu, quel__ofnqt, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (vig__uwzng, rzc__sueb):
            with vig__uwzng:
                wzc__qte = pyapi.object_getattr_string(vpb__rff, 'arrays')
                uaq__fogd = c.pyapi.make_none()
                if n_cols is None:
                    rufyp__iywe = pyapi.call_method(wzc__qte, '__len__', ())
                    okl__gkl = pyapi.long_as_longlong(rufyp__iywe)
                    pyapi.decref(rufyp__iywe)
                else:
                    okl__gkl = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, okl__gkl) as fbtox__hapbt:
                    i = fbtox__hapbt.index
                    gmm__dlgl = pyapi.list_getitem(wzc__qte, i)
                    owtv__njbq = c.builder.icmp_unsigned('!=', gmm__dlgl,
                        uaq__fogd)
                    with builder.if_then(owtv__njbq):
                        vfta__xej = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, vfta__xej, gmm__dlgl)
                        pyapi.decref(vfta__xej)
                pyapi.decref(wzc__qte)
                pyapi.decref(uaq__fogd)
            with rzc__sueb:
                df_obj = builder.load(res)
                jbq__iliqr = pyapi.object_getattr_string(df_obj, 'index')
                sfprw__ziw = c.pyapi.call_method(vpb__rff, 'to_pandas', (
                    jbq__iliqr,))
                builder.store(sfprw__ziw, res)
                pyapi.decref(df_obj)
                pyapi.decref(jbq__iliqr)
        pyapi.decref(vpb__rff)
    else:
        qblvb__dgz = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        lmypq__yjfiq = typ.data
        for i, arr, nmq__cas in zip(range(n_cols), qblvb__dgz, lmypq__yjfiq):
            jhd__fzza = cgutils.alloca_once_value(builder, arr)
            sjxva__vcxoe = cgutils.alloca_once_value(builder, context.
                get_constant_null(nmq__cas))
            owtv__njbq = builder.not_(is_ll_eq(builder, jhd__fzza,
                sjxva__vcxoe))
            chf__fjcv = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, owtv__njbq))
            with builder.if_then(chf__fjcv):
                vfta__xej = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, nmq__cas, arr)
                arr_obj = pyapi.from_native_value(nmq__cas, arr, c.env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, vfta__xej, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(vfta__xej)
    df_obj = builder.load(res)
    wxvlq__kyrl = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', wxvlq__kyrl)
    pyapi.decref(wxvlq__kyrl)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    uaq__fogd = pyapi.borrow_none()
    mgif__uax = pyapi.unserialize(pyapi.serialize_object(slice))
    cfiuo__pvwwy = pyapi.call_function_objargs(mgif__uax, [uaq__fogd])
    jkzd__ppcj = pyapi.long_from_longlong(col_ind)
    ngvc__suky = pyapi.tuple_pack([cfiuo__pvwwy, jkzd__ppcj])
    czky__nkxfo = pyapi.object_getattr_string(df_obj, 'iloc')
    qcman__pmmdp = pyapi.object_getitem(czky__nkxfo, ngvc__suky)
    mat__ndt = pyapi.object_getattr_string(qcman__pmmdp, 'array')
    vnm__qqtdu = pyapi.unserialize(pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = pyapi.call_function_objargs(vnm__qqtdu, [mat__ndt])
    pyapi.decref(mat__ndt)
    pyapi.decref(vnm__qqtdu)
    pyapi.decref(mgif__uax)
    pyapi.decref(cfiuo__pvwwy)
    pyapi.decref(jkzd__ppcj)
    pyapi.decref(ngvc__suky)
    pyapi.decref(czky__nkxfo)
    pyapi.decref(qcman__pmmdp)
    return arr_obj


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        df_typ = sig.args[0]
        col_ind = get_overload_const_int(sig.args[1])
        data_typ = df_typ.data[col_ind]
        muvir__yol = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            muvir__yol.parent, args[1], data_typ)
        swr__qjok = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            quel__ofnqt = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            dxk__ospp = df_typ.table_type.type_to_blk[data_typ]
            piliq__kqi = getattr(quel__ofnqt, f'block_{dxk__ospp}')
            bjejk__qazlm = ListInstance(c.context, c.builder, types.List(
                data_typ), piliq__kqi)
            ziih__kchp = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            bjejk__qazlm.inititem(ziih__kchp, swr__qjok.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, swr__qjok.value, col_ind)
        fyvsr__fva = DataFramePayloadType(df_typ)
        qeat__ukibf = context.nrt.meminfo_data(builder, muvir__yol.meminfo)
        nnvb__lqse = context.get_value_type(fyvsr__fva).as_pointer()
        qeat__ukibf = builder.bitcast(qeat__ukibf, nnvb__lqse)
        builder.store(dataframe_payload._getvalue(), qeat__ukibf)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    mat__ndt = c.pyapi.object_getattr_string(val, 'array')
    vnm__qqtdu = c.pyapi.unserialize(c.pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = c.pyapi.call_function_objargs(vnm__qqtdu, [mat__ndt])
    jqy__wdj = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    jbq__iliqr = c.pyapi.object_getattr_string(val, 'index')
    hkpvc__vakjq = c.pyapi.to_native_value(typ.index, jbq__iliqr).value
    kvn__qpuy = c.pyapi.object_getattr_string(val, 'name')
    aihmk__vmpav = c.pyapi.to_native_value(typ.name_typ, kvn__qpuy).value
    yow__itcz = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, jqy__wdj, hkpvc__vakjq, aihmk__vmpav)
    c.pyapi.decref(vnm__qqtdu)
    c.pyapi.decref(mat__ndt)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(jbq__iliqr)
    c.pyapi.decref(kvn__qpuy)
    return NativeValue(yow__itcz)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        jwvki__psf = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(jwvki__psf._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    suje__wsei = c.context.insert_const_string(c.builder.module, 'pandas')
    ljrtw__mfm = c.pyapi.import_module_noblock(suje__wsei)
    iibnx__rjhg = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, iibnx__rjhg.data)
    c.context.nrt.incref(c.builder, typ.index, iibnx__rjhg.index)
    c.context.nrt.incref(c.builder, typ.name_typ, iibnx__rjhg.name)
    arr_obj = c.pyapi.from_native_value(typ.data, iibnx__rjhg.data, c.
        env_manager)
    jbq__iliqr = c.pyapi.from_native_value(typ.index, iibnx__rjhg.index, c.
        env_manager)
    kvn__qpuy = c.pyapi.from_native_value(typ.name_typ, iibnx__rjhg.name, c
        .env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(ljrtw__mfm, 'Series', (arr_obj, jbq__iliqr,
        dtype, kvn__qpuy))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(jbq__iliqr)
    c.pyapi.decref(kvn__qpuy)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(ljrtw__mfm)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    fbldu__gacuq = []
    for dnwcr__mrnb in typ_list:
        if isinstance(dnwcr__mrnb, int) and not isinstance(dnwcr__mrnb, bool):
            gmdtb__nxh = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), dnwcr__mrnb))
        else:
            yfeq__cklh = numba.typeof(dnwcr__mrnb)
            wqk__wxe = context.get_constant_generic(builder, yfeq__cklh,
                dnwcr__mrnb)
            gmdtb__nxh = pyapi.from_native_value(yfeq__cklh, wqk__wxe,
                env_manager)
        fbldu__gacuq.append(gmdtb__nxh)
    ggy__bfmy = pyapi.list_pack(fbldu__gacuq)
    for val in fbldu__gacuq:
        pyapi.decref(val)
    return ggy__bfmy


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    wwm__slbq = not typ.has_runtime_cols
    unlr__grs = 2 if wwm__slbq else 1
    yksvs__fkt = pyapi.dict_new(unlr__grs)
    uahv__fjru = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    pyapi.dict_setitem_string(yksvs__fkt, 'dist', uahv__fjru)
    pyapi.decref(uahv__fjru)
    if wwm__slbq:
        bopid__boup = _dtype_to_type_enum_list(typ.index)
        if bopid__boup != None:
            kskbk__wlmi = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, bopid__boup)
        else:
            kskbk__wlmi = pyapi.make_none()
        if typ.is_table_format:
            gqja__lyqqz = typ.table_type
            ntc__vtapx = pyapi.list_new(lir.Constant(lir.IntType(64), len(
                typ.data)))
            for dxk__ospp, dtype in gqja__lyqqz.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                okl__gkl = c.context.get_constant(types.int64, len(
                    gqja__lyqqz.block_to_arr_ind[dxk__ospp]))
                tirr__nnxzp = c.context.make_constant_array(c.builder,
                    types.Array(types.int64, 1, 'C'), np.array(gqja__lyqqz.
                    block_to_arr_ind[dxk__ospp], dtype=np.int64))
                kzjo__rjolq = c.context.make_array(types.Array(types.int64,
                    1, 'C'))(c.context, c.builder, tirr__nnxzp)
                with cgutils.for_range(c.builder, okl__gkl) as fbtox__hapbt:
                    i = fbtox__hapbt.index
                    loq__uxr = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), kzjo__rjolq, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(ntc__vtapx, loq__uxr, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            hyz__ipij = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    ggy__bfmy = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    ggy__bfmy = pyapi.make_none()
                hyz__ipij.append(ggy__bfmy)
            ntc__vtapx = pyapi.list_pack(hyz__ipij)
            for val in hyz__ipij:
                pyapi.decref(val)
        xjzn__amdnt = pyapi.list_pack([kskbk__wlmi, ntc__vtapx])
        pyapi.dict_setitem_string(yksvs__fkt, 'type_metadata', xjzn__amdnt)
    pyapi.object_setattr_string(obj, '_bodo_meta', yksvs__fkt)
    pyapi.decref(yksvs__fkt)


def get_series_dtype_handle_null_int_and_hetrogenous(series_typ):
    if isinstance(series_typ, HeterogeneousSeriesType):
        return None
    if isinstance(series_typ.dtype, types.Number) and isinstance(series_typ
        .data, IntegerArrayType):
        return IntDtype(series_typ.dtype)
    if isinstance(series_typ.dtype, types.Float) and isinstance(series_typ.
        data, FloatingArrayType):
        return FloatDtype(series_typ.dtype)
    return series_typ.dtype


def _set_bodo_meta_series(obj, c, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    yksvs__fkt = pyapi.dict_new(2)
    uahv__fjru = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    bopid__boup = _dtype_to_type_enum_list(typ.index)
    if bopid__boup != None:
        kskbk__wlmi = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, bopid__boup)
    else:
        kskbk__wlmi = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            dyalt__aprg = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            dyalt__aprg = pyapi.make_none()
    else:
        dyalt__aprg = pyapi.make_none()
    nvnd__ehj = pyapi.list_pack([kskbk__wlmi, dyalt__aprg])
    pyapi.dict_setitem_string(yksvs__fkt, 'type_metadata', nvnd__ehj)
    pyapi.decref(nvnd__ehj)
    pyapi.dict_setitem_string(yksvs__fkt, 'dist', uahv__fjru)
    pyapi.object_setattr_string(obj, '_bodo_meta', yksvs__fkt)
    pyapi.decref(yksvs__fkt)
    pyapi.decref(uahv__fjru)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as jjgjg__oox:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    vvog__dya = numba.np.numpy_support.map_layout(val)
    zhwik__gafa = not val.flags.writeable
    return types.Array(dtype, val.ndim, vvog__dya, readonly=zhwik__gafa)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    tde__typ = val[i]
    dzdc__sbv = 100
    if isinstance(tde__typ, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(tde__typ, (bytes, bytearray)):
        return binary_array_type
    elif isinstance(tde__typ, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(tde__typ, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(tde__typ))
    elif isinstance(tde__typ, (float, np.float32, np.float64)):
        return bodo.libs.float_arr_ext.FloatingArrayType(numba.typeof(tde__typ)
            )
    elif isinstance(tde__typ, (dict, Dict)) and len(tde__typ.keys()
        ) <= dzdc__sbv and all(isinstance(nwr__fkhyw, str) for nwr__fkhyw in
        tde__typ.keys()):
        odxvt__dmgq = tuple(tde__typ.keys())
        pdxk__cugu = tuple(_get_struct_value_arr_type(v) for v in tde__typ.
            values())
        return StructArrayType(pdxk__cugu, odxvt__dmgq)
    elif isinstance(tde__typ, (dict, Dict)):
        gxcp__eoas = numba.typeof(_value_to_array(list(tde__typ.keys())))
        drojj__hilm = numba.typeof(_value_to_array(list(tde__typ.values())))
        gxcp__eoas = to_str_arr_if_dict_array(gxcp__eoas)
        drojj__hilm = to_str_arr_if_dict_array(drojj__hilm)
        return MapArrayType(gxcp__eoas, drojj__hilm)
    elif isinstance(tde__typ, tuple):
        pdxk__cugu = tuple(_get_struct_value_arr_type(v) for v in tde__typ)
        return TupleArrayType(pdxk__cugu)
    if isinstance(tde__typ, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.FloatingArray, pd.arrays.StringArray,
        pd.arrays.ArrowStringArray)):
        if isinstance(tde__typ, list):
            tde__typ = _value_to_array(tde__typ)
        vvpyd__ozjji = numba.typeof(tde__typ)
        vvpyd__ozjji = to_str_arr_if_dict_array(vvpyd__ozjji)
        return ArrayItemArrayType(vvpyd__ozjji)
    if isinstance(tde__typ, datetime.date):
        return datetime_date_array_type
    if isinstance(tde__typ, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(tde__typ, bodo.Time):
        return TimeArrayType(tde__typ.precision)
    if isinstance(tde__typ, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(tde__typ, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(f'Unsupported object array with first value: {tde__typ}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    dynwu__yjic = val.copy()
    dynwu__yjic.append(None)
    arr = np.array(dynwu__yjic, np.object_)
    if len(val) and isinstance(val[0], float):
        arr = np.array(val, np.float64)
    return arr


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    nmq__cas = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        nmq__cas = to_nullable_type(nmq__cas)
    return nmq__cas
