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
    vaxj__kmnv = tuple(val.columns.to_list())
    oqtx__wyy = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        ssfyu__gphp = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        ssfyu__gphp = numba.typeof(val.index)
    xkn__brf = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    mps__dgrj = len(oqtx__wyy) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(oqtx__wyy, ssfyu__gphp, vaxj__kmnv, xkn__brf,
        is_table_format=mps__dgrj)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    xkn__brf = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        kbytj__mrhc = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        kbytj__mrhc = numba.typeof(val.index)
    ogvqa__pkd = _infer_series_arr_type(val)
    if _use_dict_str_type and ogvqa__pkd == string_array_type:
        ogvqa__pkd = bodo.dict_str_arr_type
    return SeriesType(ogvqa__pkd.dtype, data=ogvqa__pkd, index=kbytj__mrhc,
        name_typ=numba.typeof(val.name), dist=xkn__brf)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    ovy__ktk = c.pyapi.object_getattr_string(val, 'index')
    pzgrr__mkgs = c.pyapi.to_native_value(typ.index, ovy__ktk).value
    c.pyapi.decref(ovy__ktk)
    if typ.is_table_format:
        cpzr__tary = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        cpzr__tary.parent = val
        for agc__scl, lpzr__bxcz in typ.table_type.type_to_blk.items():
            ofokf__owuao = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[lpzr__bxcz]))
            mfehv__hcqk, hywj__zqcxz = ListInstance.allocate_ex(c.context,
                c.builder, types.List(agc__scl), ofokf__owuao)
            hywj__zqcxz.size = ofokf__owuao
            setattr(cpzr__tary, f'block_{lpzr__bxcz}', hywj__zqcxz.value)
        yrk__pea = c.pyapi.call_method(val, '__len__', ())
        hhyy__iqgny = c.pyapi.long_as_longlong(yrk__pea)
        c.pyapi.decref(yrk__pea)
        cpzr__tary.len = hhyy__iqgny
        inwg__cfvb = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [cpzr__tary._getvalue()])
    else:
        lhrv__vld = [c.context.get_constant_null(agc__scl) for agc__scl in
            typ.data]
        inwg__cfvb = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            lhrv__vld)
    dlluq__gdjsl = construct_dataframe(c.context, c.builder, typ,
        inwg__cfvb, pzgrr__mkgs, val, None)
    return NativeValue(dlluq__gdjsl)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        khdl__qtb = df._bodo_meta['type_metadata'][1]
    else:
        khdl__qtb = [None] * len(df.columns)
    jxp__vsdpv = [_infer_series_arr_type(df.iloc[:, i], array_metadata=
        khdl__qtb[i]) for i in range(len(df.columns))]
    jxp__vsdpv = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        agc__scl == string_array_type else agc__scl) for agc__scl in jxp__vsdpv
        ]
    return tuple(jxp__vsdpv)


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
    txcje__mov, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(txcje__mov) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {txcje__mov}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        uzjii__irof, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return uzjii__irof, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.FloatingArray.value:
        uzjii__irof, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return uzjii__irof, FloatingArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        uzjii__irof, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return uzjii__irof, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        xzc__hptzt = typ_enum_list[1]
        vlhbl__dzzhf = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(xzc__hptzt, vlhbl__dzzhf)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        eplsd__yadvh = typ_enum_list[1]
        icy__tlhke = tuple(typ_enum_list[2:2 + eplsd__yadvh])
        gjljo__bjwna = typ_enum_list[2 + eplsd__yadvh:]
        bbhvl__yhpb = []
        for i in range(eplsd__yadvh):
            gjljo__bjwna, fqpqi__thmwz = _dtype_from_type_enum_list_recursor(
                gjljo__bjwna)
            bbhvl__yhpb.append(fqpqi__thmwz)
        return gjljo__bjwna, StructType(tuple(bbhvl__yhpb), icy__tlhke)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        zsqv__ngk = typ_enum_list[1]
        gjljo__bjwna = typ_enum_list[2:]
        return gjljo__bjwna, zsqv__ngk
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        zsqv__ngk = typ_enum_list[1]
        gjljo__bjwna = typ_enum_list[2:]
        return gjljo__bjwna, numba.types.literal(zsqv__ngk)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        gjljo__bjwna, qpm__sgf = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        gjljo__bjwna, xanxz__qej = _dtype_from_type_enum_list_recursor(
            gjljo__bjwna)
        gjljo__bjwna, gsp__rgnf = _dtype_from_type_enum_list_recursor(
            gjljo__bjwna)
        gjljo__bjwna, oazi__bwzr = _dtype_from_type_enum_list_recursor(
            gjljo__bjwna)
        gjljo__bjwna, fnouo__kehc = _dtype_from_type_enum_list_recursor(
            gjljo__bjwna)
        return gjljo__bjwna, PDCategoricalDtype(qpm__sgf, xanxz__qej,
            gsp__rgnf, oazi__bwzr, fnouo__kehc)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        gjljo__bjwna, ounvy__ykgo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjljo__bjwna, DatetimeIndexType(ounvy__ykgo)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        gjljo__bjwna, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        gjljo__bjwna, ounvy__ykgo = _dtype_from_type_enum_list_recursor(
            gjljo__bjwna)
        gjljo__bjwna, oazi__bwzr = _dtype_from_type_enum_list_recursor(
            gjljo__bjwna)
        return gjljo__bjwna, NumericIndexType(dtype, ounvy__ykgo, oazi__bwzr)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        gjljo__bjwna, zqpqa__tsue = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        gjljo__bjwna, ounvy__ykgo = _dtype_from_type_enum_list_recursor(
            gjljo__bjwna)
        return gjljo__bjwna, PeriodIndexType(zqpqa__tsue, ounvy__ykgo)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        gjljo__bjwna, oazi__bwzr = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        gjljo__bjwna, ounvy__ykgo = _dtype_from_type_enum_list_recursor(
            gjljo__bjwna)
        return gjljo__bjwna, CategoricalIndexType(oazi__bwzr, ounvy__ykgo)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        gjljo__bjwna, ounvy__ykgo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjljo__bjwna, RangeIndexType(ounvy__ykgo)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        gjljo__bjwna, ounvy__ykgo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjljo__bjwna, StringIndexType(ounvy__ykgo)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        gjljo__bjwna, ounvy__ykgo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjljo__bjwna, BinaryIndexType(ounvy__ykgo)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        gjljo__bjwna, ounvy__ykgo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjljo__bjwna, TimedeltaIndexType(ounvy__ykgo)
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
        ccc__qycqw = get_overload_const_int(typ)
        if numba.types.maybe_literal(ccc__qycqw) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ccc__qycqw]
    elif is_overload_constant_str(typ):
        ccc__qycqw = get_overload_const_str(typ)
        if numba.types.maybe_literal(ccc__qycqw) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ccc__qycqw]
    elif is_overload_constant_bool(typ):
        ccc__qycqw = get_overload_const_bool(typ)
        if numba.types.maybe_literal(ccc__qycqw) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ccc__qycqw]
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
        lwab__rvi = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for cph__kbv in typ.names:
            lwab__rvi.append(cph__kbv)
        for thgr__ypaej in typ.data:
            lwab__rvi += _dtype_to_type_enum_list_recursor(thgr__ypaej)
        return lwab__rvi
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        xburi__cwq = _dtype_to_type_enum_list_recursor(typ.categories)
        xqaj__nvcf = _dtype_to_type_enum_list_recursor(typ.elem_type)
        vcou__xwqzc = _dtype_to_type_enum_list_recursor(typ.ordered)
        ufwud__onhho = _dtype_to_type_enum_list_recursor(typ.data)
        tle__dhtg = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + xburi__cwq + xqaj__nvcf + vcou__xwqzc + ufwud__onhho + tle__dhtg
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                lqbtm__drjn = types.float64
                if isinstance(typ.data, FloatingArrayType):
                    gxd__pezag = FloatingArrayType(lqbtm__drjn)
                else:
                    gxd__pezag = types.Array(lqbtm__drjn, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                lqbtm__drjn = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    gxd__pezag = IntegerArrayType(lqbtm__drjn)
                else:
                    gxd__pezag = types.Array(lqbtm__drjn, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                lqbtm__drjn = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    gxd__pezag = IntegerArrayType(lqbtm__drjn)
                else:
                    gxd__pezag = types.Array(lqbtm__drjn, 1, 'C')
            elif typ.dtype == types.bool_:
                lqbtm__drjn = typ.dtype
                gxd__pezag = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(lqbtm__drjn
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(gxd__pezag)
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
                mfc__ybvul = S._bodo_meta['type_metadata'][1]
                return dtype_to_array_type(_dtype_from_type_enum_list(
                    mfc__ybvul))
        return bodo.typeof(_fix_series_arr_type(S.array))
    try:
        hgd__xtsf = bodo.typeof(_fix_series_arr_type(S.array))
        if hgd__xtsf == types.Array(types.bool_, 1, 'C'):
            hgd__xtsf = bodo.boolean_array
        if isinstance(hgd__xtsf, types.Array):
            assert hgd__xtsf.ndim == 1, 'invalid numpy array type in Series'
            hgd__xtsf = types.Array(hgd__xtsf.dtype, 1, 'C')
        return hgd__xtsf
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    mcg__ujscm = cgutils.is_not_null(builder, parent_obj)
    lkbng__ncddm = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(mcg__ujscm):
        lcz__oba = pyapi.object_getattr_string(parent_obj, 'columns')
        yrk__pea = pyapi.call_method(lcz__oba, '__len__', ())
        builder.store(pyapi.long_as_longlong(yrk__pea), lkbng__ncddm)
        pyapi.decref(yrk__pea)
        pyapi.decref(lcz__oba)
    use_parent_obj = builder.and_(mcg__ujscm, builder.icmp_unsigned('==',
        builder.load(lkbng__ncddm), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        hcg__jnh = df_typ.runtime_colname_typ
        context.nrt.incref(builder, hcg__jnh, dataframe_payload.columns)
        return pyapi.from_native_value(hcg__jnh, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        vwq__nbf = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        vwq__nbf = np.array(df_typ.columns, 'int64')
    else:
        vwq__nbf = df_typ.columns
    oqmjq__rpyn = numba.typeof(vwq__nbf)
    tgcs__zosp = context.get_constant_generic(builder, oqmjq__rpyn, vwq__nbf)
    vtecp__mynyi = pyapi.from_native_value(oqmjq__rpyn, tgcs__zosp, c.
        env_manager)
    if (oqmjq__rpyn == bodo.string_array_type and bodo.libs.str_arr_ext.
        use_pd_pyarrow_string_array):
        xddso__wtrq = vtecp__mynyi
        vtecp__mynyi = pyapi.call_method(vtecp__mynyi, 'to_numpy', ())
        pyapi.decref(xddso__wtrq)
    return vtecp__mynyi


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (wtygx__xgpf, kzeq__zrox):
        with wtygx__xgpf:
            pyapi.incref(obj)
            xsg__ebml = context.insert_const_string(c.builder.module, 'numpy')
            uudiy__omtae = pyapi.import_module_noblock(xsg__ebml)
            if df_typ.has_runtime_cols:
                mvl__juxk = 0
            else:
                mvl__juxk = len(df_typ.columns)
            xiywq__lbhj = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), mvl__juxk))
            rgdm__zyb = pyapi.call_method(uudiy__omtae, 'arange', (
                xiywq__lbhj,))
            pyapi.object_setattr_string(obj, 'columns', rgdm__zyb)
            pyapi.decref(uudiy__omtae)
            pyapi.decref(rgdm__zyb)
            pyapi.decref(xiywq__lbhj)
        with kzeq__zrox:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            hcj__hrlqt = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            xsg__ebml = context.insert_const_string(c.builder.module, 'pandas')
            uudiy__omtae = pyapi.import_module_noblock(xsg__ebml)
            df_obj = pyapi.call_method(uudiy__omtae, 'DataFrame', (pyapi.
                borrow_none(), hcj__hrlqt))
            pyapi.decref(uudiy__omtae)
            pyapi.decref(hcj__hrlqt)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    bxi__rqlk = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = bxi__rqlk.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        oso__vniq = typ.table_type
        cpzr__tary = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, oso__vniq, cpzr__tary)
        dsghg__wuv = box_table(oso__vniq, cpzr__tary, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (zawt__qndmi, wzkbd__nnz):
            with zawt__qndmi:
                mnre__wvuv = pyapi.object_getattr_string(dsghg__wuv, 'arrays')
                xicnq__fsmqo = c.pyapi.make_none()
                if n_cols is None:
                    yrk__pea = pyapi.call_method(mnre__wvuv, '__len__', ())
                    ofokf__owuao = pyapi.long_as_longlong(yrk__pea)
                    pyapi.decref(yrk__pea)
                else:
                    ofokf__owuao = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, ofokf__owuao) as mbm__blc:
                    i = mbm__blc.index
                    wgom__whx = pyapi.list_getitem(mnre__wvuv, i)
                    czs__qwuze = c.builder.icmp_unsigned('!=', wgom__whx,
                        xicnq__fsmqo)
                    with builder.if_then(czs__qwuze):
                        huxd__qyb = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, huxd__qyb, wgom__whx)
                        pyapi.decref(huxd__qyb)
                pyapi.decref(mnre__wvuv)
                pyapi.decref(xicnq__fsmqo)
            with wzkbd__nnz:
                df_obj = builder.load(res)
                hcj__hrlqt = pyapi.object_getattr_string(df_obj, 'index')
                kxu__qncma = c.pyapi.call_method(dsghg__wuv, 'to_pandas', (
                    hcj__hrlqt,))
                builder.store(kxu__qncma, res)
                pyapi.decref(df_obj)
                pyapi.decref(hcj__hrlqt)
        pyapi.decref(dsghg__wuv)
    else:
        jhru__xzj = [builder.extract_value(dataframe_payload.data, i) for i in
            range(n_cols)]
        sap__oyzx = typ.data
        for i, arr, ogvqa__pkd in zip(range(n_cols), jhru__xzj, sap__oyzx):
            astq__aup = cgutils.alloca_once_value(builder, arr)
            gmana__vpe = cgutils.alloca_once_value(builder, context.
                get_constant_null(ogvqa__pkd))
            czs__qwuze = builder.not_(is_ll_eq(builder, astq__aup, gmana__vpe))
            yevx__wlrjg = builder.or_(builder.not_(use_parent_obj), builder
                .and_(use_parent_obj, czs__qwuze))
            with builder.if_then(yevx__wlrjg):
                huxd__qyb = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, ogvqa__pkd, arr)
                arr_obj = pyapi.from_native_value(ogvqa__pkd, arr, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, huxd__qyb, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(huxd__qyb)
    df_obj = builder.load(res)
    vtecp__mynyi = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', vtecp__mynyi)
    pyapi.decref(vtecp__mynyi)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    xicnq__fsmqo = pyapi.borrow_none()
    aazu__amz = pyapi.unserialize(pyapi.serialize_object(slice))
    wof__nlzs = pyapi.call_function_objargs(aazu__amz, [xicnq__fsmqo])
    yfgep__bowa = pyapi.long_from_longlong(col_ind)
    jor__nho = pyapi.tuple_pack([wof__nlzs, yfgep__bowa])
    bpa__jmn = pyapi.object_getattr_string(df_obj, 'iloc')
    yqiwi__yvgdv = pyapi.object_getitem(bpa__jmn, jor__nho)
    ofjb__zasgx = pyapi.object_getattr_string(yqiwi__yvgdv, 'array')
    vryv__gyoal = pyapi.unserialize(pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = pyapi.call_function_objargs(vryv__gyoal, [ofjb__zasgx])
    pyapi.decref(ofjb__zasgx)
    pyapi.decref(vryv__gyoal)
    pyapi.decref(aazu__amz)
    pyapi.decref(wof__nlzs)
    pyapi.decref(yfgep__bowa)
    pyapi.decref(jor__nho)
    pyapi.decref(bpa__jmn)
    pyapi.decref(yqiwi__yvgdv)
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
        bxi__rqlk = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            bxi__rqlk.parent, args[1], data_typ)
        yuu__oprk = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            cpzr__tary = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            lpzr__bxcz = df_typ.table_type.type_to_blk[data_typ]
            bmv__ywd = getattr(cpzr__tary, f'block_{lpzr__bxcz}')
            xonzj__xhty = ListInstance(c.context, c.builder, types.List(
                data_typ), bmv__ywd)
            jph__rlp = context.get_constant(types.int64, df_typ.table_type.
                block_offsets[col_ind])
            xonzj__xhty.inititem(jph__rlp, yuu__oprk.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, yuu__oprk.value, col_ind)
        yzp__kwj = DataFramePayloadType(df_typ)
        drt__mnjz = context.nrt.meminfo_data(builder, bxi__rqlk.meminfo)
        omfp__pajcd = context.get_value_type(yzp__kwj).as_pointer()
        drt__mnjz = builder.bitcast(drt__mnjz, omfp__pajcd)
        builder.store(dataframe_payload._getvalue(), drt__mnjz)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    ofjb__zasgx = c.pyapi.object_getattr_string(val, 'array')
    vryv__gyoal = c.pyapi.unserialize(c.pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = c.pyapi.call_function_objargs(vryv__gyoal, [ofjb__zasgx])
    ioti__xhs = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    hcj__hrlqt = c.pyapi.object_getattr_string(val, 'index')
    pzgrr__mkgs = c.pyapi.to_native_value(typ.index, hcj__hrlqt).value
    bdzta__znk = c.pyapi.object_getattr_string(val, 'name')
    ocvhc__vss = c.pyapi.to_native_value(typ.name_typ, bdzta__znk).value
    nhfvv__wcphg = bodo.hiframes.pd_series_ext.construct_series(c.context,
        c.builder, typ, ioti__xhs, pzgrr__mkgs, ocvhc__vss)
    c.pyapi.decref(vryv__gyoal)
    c.pyapi.decref(ofjb__zasgx)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(hcj__hrlqt)
    c.pyapi.decref(bdzta__znk)
    return NativeValue(nhfvv__wcphg)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        xlrmu__lwa = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(xlrmu__lwa._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    xsg__ebml = c.context.insert_const_string(c.builder.module, 'pandas')
    efm__lcgzj = c.pyapi.import_module_noblock(xsg__ebml)
    epia__rrvr = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, epia__rrvr.data)
    c.context.nrt.incref(c.builder, typ.index, epia__rrvr.index)
    c.context.nrt.incref(c.builder, typ.name_typ, epia__rrvr.name)
    arr_obj = c.pyapi.from_native_value(typ.data, epia__rrvr.data, c.
        env_manager)
    hcj__hrlqt = c.pyapi.from_native_value(typ.index, epia__rrvr.index, c.
        env_manager)
    bdzta__znk = c.pyapi.from_native_value(typ.name_typ, epia__rrvr.name, c
        .env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(efm__lcgzj, 'Series', (arr_obj, hcj__hrlqt,
        dtype, bdzta__znk))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(hcj__hrlqt)
    c.pyapi.decref(bdzta__znk)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(efm__lcgzj)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    fplyb__bevzm = []
    for vjlvs__nufr in typ_list:
        if isinstance(vjlvs__nufr, int) and not isinstance(vjlvs__nufr, bool):
            xxcj__pzgrq = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), vjlvs__nufr))
        else:
            uhckp__hdd = numba.typeof(vjlvs__nufr)
            dfojj__flb = context.get_constant_generic(builder, uhckp__hdd,
                vjlvs__nufr)
            xxcj__pzgrq = pyapi.from_native_value(uhckp__hdd, dfojj__flb,
                env_manager)
        fplyb__bevzm.append(xxcj__pzgrq)
    jdw__zblz = pyapi.list_pack(fplyb__bevzm)
    for val in fplyb__bevzm:
        pyapi.decref(val)
    return jdw__zblz


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    qcla__kyh = not typ.has_runtime_cols
    mguv__scang = 2 if qcla__kyh else 1
    cyj__prh = pyapi.dict_new(mguv__scang)
    nqdg__xnm = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(cyj__prh, 'dist', nqdg__xnm)
    pyapi.decref(nqdg__xnm)
    if qcla__kyh:
        exnv__ztjv = _dtype_to_type_enum_list(typ.index)
        if exnv__ztjv != None:
            muev__fhjzm = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, exnv__ztjv)
        else:
            muev__fhjzm = pyapi.make_none()
        if typ.is_table_format:
            agc__scl = typ.table_type
            hos__awze = pyapi.list_new(lir.Constant(lir.IntType(64), len(
                typ.data)))
            for lpzr__bxcz, dtype in agc__scl.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                ofokf__owuao = c.context.get_constant(types.int64, len(
                    agc__scl.block_to_arr_ind[lpzr__bxcz]))
                pue__nxlzq = c.context.make_constant_array(c.builder, types
                    .Array(types.int64, 1, 'C'), np.array(agc__scl.
                    block_to_arr_ind[lpzr__bxcz], dtype=np.int64))
                xgsa__pgi = c.context.make_array(types.Array(types.int64, 1,
                    'C'))(c.context, c.builder, pue__nxlzq)
                with cgutils.for_range(c.builder, ofokf__owuao) as mbm__blc:
                    i = mbm__blc.index
                    fart__qrdam = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), xgsa__pgi, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(hos__awze, fart__qrdam, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            diw__knl = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    jdw__zblz = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    jdw__zblz = pyapi.make_none()
                diw__knl.append(jdw__zblz)
            hos__awze = pyapi.list_pack(diw__knl)
            for val in diw__knl:
                pyapi.decref(val)
        ibmj__nmois = pyapi.list_pack([muev__fhjzm, hos__awze])
        pyapi.dict_setitem_string(cyj__prh, 'type_metadata', ibmj__nmois)
    pyapi.object_setattr_string(obj, '_bodo_meta', cyj__prh)
    pyapi.decref(cyj__prh)


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
    cyj__prh = pyapi.dict_new(2)
    nqdg__xnm = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    exnv__ztjv = _dtype_to_type_enum_list(typ.index)
    if exnv__ztjv != None:
        muev__fhjzm = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, exnv__ztjv)
    else:
        muev__fhjzm = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            vrp__ihjzt = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            vrp__ihjzt = pyapi.make_none()
    else:
        vrp__ihjzt = pyapi.make_none()
    tqdw__qgmtt = pyapi.list_pack([muev__fhjzm, vrp__ihjzt])
    pyapi.dict_setitem_string(cyj__prh, 'type_metadata', tqdw__qgmtt)
    pyapi.decref(tqdw__qgmtt)
    pyapi.dict_setitem_string(cyj__prh, 'dist', nqdg__xnm)
    pyapi.object_setattr_string(obj, '_bodo_meta', cyj__prh)
    pyapi.decref(cyj__prh)
    pyapi.decref(nqdg__xnm)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as vejco__jihs:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    btuto__vvb = numba.np.numpy_support.map_layout(val)
    dev__hjjb = not val.flags.writeable
    return types.Array(dtype, val.ndim, btuto__vvb, readonly=dev__hjjb)


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
    lskk__ycl = val[i]
    gtlm__anetr = 100
    if isinstance(lskk__ycl, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(lskk__ycl, (bytes, bytearray)):
        return binary_array_type
    elif isinstance(lskk__ycl, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(lskk__ycl, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(lskk__ycl))
    elif isinstance(lskk__ycl, (float, np.float32, np.float64)):
        return bodo.libs.float_arr_ext.FloatingArrayType(numba.typeof(
            lskk__ycl))
    elif isinstance(lskk__ycl, (dict, Dict)) and len(lskk__ycl.keys()
        ) <= gtlm__anetr and all(isinstance(wtp__jvvq, str) for wtp__jvvq in
        lskk__ycl.keys()):
        icy__tlhke = tuple(lskk__ycl.keys())
        yqxq__zju = tuple(_get_struct_value_arr_type(v) for v in lskk__ycl.
            values())
        return StructArrayType(yqxq__zju, icy__tlhke)
    elif isinstance(lskk__ycl, (dict, Dict)):
        tdm__entmk = numba.typeof(_value_to_array(list(lskk__ycl.keys())))
        nsp__dvu = numba.typeof(_value_to_array(list(lskk__ycl.values())))
        tdm__entmk = to_str_arr_if_dict_array(tdm__entmk)
        nsp__dvu = to_str_arr_if_dict_array(nsp__dvu)
        return MapArrayType(tdm__entmk, nsp__dvu)
    elif isinstance(lskk__ycl, tuple):
        yqxq__zju = tuple(_get_struct_value_arr_type(v) for v in lskk__ycl)
        return TupleArrayType(yqxq__zju)
    if isinstance(lskk__ycl, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.FloatingArray, pd.arrays.StringArray,
        pd.arrays.ArrowStringArray)):
        if isinstance(lskk__ycl, list):
            lskk__ycl = _value_to_array(lskk__ycl)
        yqj__axjf = numba.typeof(lskk__ycl)
        yqj__axjf = to_str_arr_if_dict_array(yqj__axjf)
        return ArrayItemArrayType(yqj__axjf)
    if isinstance(lskk__ycl, datetime.date):
        return datetime_date_array_type
    if isinstance(lskk__ycl, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(lskk__ycl, bodo.Time):
        return TimeArrayType(lskk__ycl.precision)
    if isinstance(lskk__ycl, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(lskk__ycl, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(f'Unsupported object array with first value: {lskk__ycl}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    aru__yhp = val.copy()
    aru__yhp.append(None)
    arr = np.array(aru__yhp, np.object_)
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
    ogvqa__pkd = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        ogvqa__pkd = to_nullable_type(ogvqa__pkd)
    return ogvqa__pkd
