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
    jwt__wsh = tuple(val.columns.to_list())
    bogit__tww = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        juh__sbn = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        juh__sbn = numba.typeof(val.index)
    uqrgh__cdtx = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    pejf__gpkf = len(bogit__tww) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(bogit__tww, juh__sbn, jwt__wsh, uqrgh__cdtx,
        is_table_format=pejf__gpkf)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    uqrgh__cdtx = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        ltj__taxd = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        ltj__taxd = numba.typeof(val.index)
    ampk__ohgzh = _infer_series_arr_type(val)
    if _use_dict_str_type and ampk__ohgzh == string_array_type:
        ampk__ohgzh = bodo.dict_str_arr_type
    return SeriesType(ampk__ohgzh.dtype, data=ampk__ohgzh, index=ltj__taxd,
        name_typ=numba.typeof(val.name), dist=uqrgh__cdtx)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    eqhg__tmw = c.pyapi.object_getattr_string(val, 'index')
    pmohf__rfbqw = c.pyapi.to_native_value(typ.index, eqhg__tmw).value
    c.pyapi.decref(eqhg__tmw)
    if typ.is_table_format:
        mqhy__xln = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        mqhy__xln.parent = val
        for oygaz__ook, zvaa__wslkk in typ.table_type.type_to_blk.items():
            nqs__cogt = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[zvaa__wslkk]))
            awakx__nyak, gsrh__gnyje = ListInstance.allocate_ex(c.context,
                c.builder, types.List(oygaz__ook), nqs__cogt)
            gsrh__gnyje.size = nqs__cogt
            setattr(mqhy__xln, f'block_{zvaa__wslkk}', gsrh__gnyje.value)
        zof__cpun = c.pyapi.call_method(val, '__len__', ())
        uabcc__siid = c.pyapi.long_as_longlong(zof__cpun)
        c.pyapi.decref(zof__cpun)
        mqhy__xln.len = uabcc__siid
        gwaup__okq = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [mqhy__xln._getvalue()])
    else:
        nroo__hlid = [c.context.get_constant_null(oygaz__ook) for
            oygaz__ook in typ.data]
        gwaup__okq = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            nroo__hlid)
    qhehx__qvyd = construct_dataframe(c.context, c.builder, typ, gwaup__okq,
        pmohf__rfbqw, val, None)
    return NativeValue(qhehx__qvyd)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        nwmhg__tgbgd = df._bodo_meta['type_metadata'][1]
    else:
        nwmhg__tgbgd = [None] * len(df.columns)
    yixb__eay = [_infer_series_arr_type(df.iloc[:, i], array_metadata=
        nwmhg__tgbgd[i]) for i in range(len(df.columns))]
    yixb__eay = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        oygaz__ook == string_array_type else oygaz__ook) for oygaz__ook in
        yixb__eay]
    return tuple(yixb__eay)


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
    wsrhe__gfycm, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(wsrhe__gfycm) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {wsrhe__gfycm}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        bftjp__idf, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return bftjp__idf, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.FloatingArray.value:
        bftjp__idf, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return bftjp__idf, FloatingArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        bftjp__idf, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return bftjp__idf, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        bpqhi__oihe = typ_enum_list[1]
        rcy__pxshv = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(bpqhi__oihe, rcy__pxshv)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        vjey__jrh = typ_enum_list[1]
        sdw__psio = tuple(typ_enum_list[2:2 + vjey__jrh])
        zuffk__gch = typ_enum_list[2 + vjey__jrh:]
        cck__lsqm = []
        for i in range(vjey__jrh):
            zuffk__gch, tit__clbc = _dtype_from_type_enum_list_recursor(
                zuffk__gch)
            cck__lsqm.append(tit__clbc)
        return zuffk__gch, StructType(tuple(cck__lsqm), sdw__psio)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        yylvy__futd = typ_enum_list[1]
        zuffk__gch = typ_enum_list[2:]
        return zuffk__gch, yylvy__futd
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        yylvy__futd = typ_enum_list[1]
        zuffk__gch = typ_enum_list[2:]
        return zuffk__gch, numba.types.literal(yylvy__futd)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        zuffk__gch, ndrpm__pgj = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        zuffk__gch, jtgw__bla = _dtype_from_type_enum_list_recursor(zuffk__gch)
        zuffk__gch, wrps__greyu = _dtype_from_type_enum_list_recursor(
            zuffk__gch)
        zuffk__gch, wrt__fiju = _dtype_from_type_enum_list_recursor(zuffk__gch)
        zuffk__gch, zejaf__sray = _dtype_from_type_enum_list_recursor(
            zuffk__gch)
        return zuffk__gch, PDCategoricalDtype(ndrpm__pgj, jtgw__bla,
            wrps__greyu, wrt__fiju, zejaf__sray)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        zuffk__gch, tyh__rbxq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return zuffk__gch, DatetimeIndexType(tyh__rbxq)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        zuffk__gch, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        zuffk__gch, tyh__rbxq = _dtype_from_type_enum_list_recursor(zuffk__gch)
        zuffk__gch, wrt__fiju = _dtype_from_type_enum_list_recursor(zuffk__gch)
        return zuffk__gch, NumericIndexType(dtype, tyh__rbxq, wrt__fiju)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        zuffk__gch, pkw__etoz = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        zuffk__gch, tyh__rbxq = _dtype_from_type_enum_list_recursor(zuffk__gch)
        return zuffk__gch, PeriodIndexType(pkw__etoz, tyh__rbxq)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        zuffk__gch, wrt__fiju = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        zuffk__gch, tyh__rbxq = _dtype_from_type_enum_list_recursor(zuffk__gch)
        return zuffk__gch, CategoricalIndexType(wrt__fiju, tyh__rbxq)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        zuffk__gch, tyh__rbxq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return zuffk__gch, RangeIndexType(tyh__rbxq)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        zuffk__gch, tyh__rbxq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return zuffk__gch, StringIndexType(tyh__rbxq)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        zuffk__gch, tyh__rbxq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return zuffk__gch, BinaryIndexType(tyh__rbxq)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        zuffk__gch, tyh__rbxq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return zuffk__gch, TimedeltaIndexType(tyh__rbxq)
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
        rqj__pdjje = get_overload_const_int(typ)
        if numba.types.maybe_literal(rqj__pdjje) == typ:
            return [SeriesDtypeEnum.LiteralType.value, rqj__pdjje]
    elif is_overload_constant_str(typ):
        rqj__pdjje = get_overload_const_str(typ)
        if numba.types.maybe_literal(rqj__pdjje) == typ:
            return [SeriesDtypeEnum.LiteralType.value, rqj__pdjje]
    elif is_overload_constant_bool(typ):
        rqj__pdjje = get_overload_const_bool(typ)
        if numba.types.maybe_literal(rqj__pdjje) == typ:
            return [SeriesDtypeEnum.LiteralType.value, rqj__pdjje]
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
        fqf__kwsro = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for banqt__tjgqj in typ.names:
            fqf__kwsro.append(banqt__tjgqj)
        for htcux__kcx in typ.data:
            fqf__kwsro += _dtype_to_type_enum_list_recursor(htcux__kcx)
        return fqf__kwsro
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        lpdl__hnckz = _dtype_to_type_enum_list_recursor(typ.categories)
        yirul__gcydd = _dtype_to_type_enum_list_recursor(typ.elem_type)
        psct__enql = _dtype_to_type_enum_list_recursor(typ.ordered)
        jixwh__glqog = _dtype_to_type_enum_list_recursor(typ.data)
        pbh__fmaoy = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + lpdl__hnckz + yirul__gcydd + psct__enql + jixwh__glqog + pbh__fmaoy
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                hcvse__poobr = types.float64
                if isinstance(typ.data, FloatingArrayType):
                    fxzjs__yuzou = FloatingArrayType(hcvse__poobr)
                else:
                    fxzjs__yuzou = types.Array(hcvse__poobr, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                hcvse__poobr = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    fxzjs__yuzou = IntegerArrayType(hcvse__poobr)
                else:
                    fxzjs__yuzou = types.Array(hcvse__poobr, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                hcvse__poobr = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    fxzjs__yuzou = IntegerArrayType(hcvse__poobr)
                else:
                    fxzjs__yuzou = types.Array(hcvse__poobr, 1, 'C')
            elif typ.dtype == types.bool_:
                hcvse__poobr = typ.dtype
                fxzjs__yuzou = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(hcvse__poobr
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(fxzjs__yuzou)
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
                ezpo__gpdr = S._bodo_meta['type_metadata'][1]
                return dtype_to_array_type(_dtype_from_type_enum_list(
                    ezpo__gpdr))
        return bodo.typeof(_fix_series_arr_type(S.array))
    try:
        aqnn__mrwlu = bodo.typeof(_fix_series_arr_type(S.array))
        if aqnn__mrwlu == types.Array(types.bool_, 1, 'C'):
            aqnn__mrwlu = bodo.boolean_array
        if isinstance(aqnn__mrwlu, types.Array):
            assert aqnn__mrwlu.ndim == 1, 'invalid numpy array type in Series'
            aqnn__mrwlu = types.Array(aqnn__mrwlu.dtype, 1, 'C')
        return aqnn__mrwlu
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    qhpe__jqwmi = cgutils.is_not_null(builder, parent_obj)
    mmywi__usnp = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(qhpe__jqwmi):
        ztem__rwrub = pyapi.object_getattr_string(parent_obj, 'columns')
        zof__cpun = pyapi.call_method(ztem__rwrub, '__len__', ())
        builder.store(pyapi.long_as_longlong(zof__cpun), mmywi__usnp)
        pyapi.decref(zof__cpun)
        pyapi.decref(ztem__rwrub)
    use_parent_obj = builder.and_(qhpe__jqwmi, builder.icmp_unsigned('==',
        builder.load(mmywi__usnp), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        nbs__muxm = df_typ.runtime_colname_typ
        context.nrt.incref(builder, nbs__muxm, dataframe_payload.columns)
        return pyapi.from_native_value(nbs__muxm, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        nupp__vmklu = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        nupp__vmklu = np.array(df_typ.columns, 'int64')
    else:
        nupp__vmklu = df_typ.columns
    upl__ihrd = numba.typeof(nupp__vmklu)
    yphlq__ttsn = context.get_constant_generic(builder, upl__ihrd, nupp__vmklu)
    nnqhd__tsv = pyapi.from_native_value(upl__ihrd, yphlq__ttsn, c.env_manager)
    if (upl__ihrd == bodo.string_array_type and bodo.libs.str_arr_ext.
        use_pd_pyarrow_string_array):
        tvakj__uqug = nnqhd__tsv
        nnqhd__tsv = pyapi.call_method(nnqhd__tsv, 'to_numpy', ())
        pyapi.decref(tvakj__uqug)
    return nnqhd__tsv


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (ulv__rzzej, lrlg__piwe):
        with ulv__rzzej:
            pyapi.incref(obj)
            ujr__mqr = context.insert_const_string(c.builder.module, 'numpy')
            lit__hls = pyapi.import_module_noblock(ujr__mqr)
            if df_typ.has_runtime_cols:
                mffsx__mwe = 0
            else:
                mffsx__mwe = len(df_typ.columns)
            zppo__rdq = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), mffsx__mwe))
            opp__poe = pyapi.call_method(lit__hls, 'arange', (zppo__rdq,))
            pyapi.object_setattr_string(obj, 'columns', opp__poe)
            pyapi.decref(lit__hls)
            pyapi.decref(opp__poe)
            pyapi.decref(zppo__rdq)
        with lrlg__piwe:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            xrlg__eske = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            ujr__mqr = context.insert_const_string(c.builder.module, 'pandas')
            lit__hls = pyapi.import_module_noblock(ujr__mqr)
            df_obj = pyapi.call_method(lit__hls, 'DataFrame', (pyapi.
                borrow_none(), xrlg__eske))
            pyapi.decref(lit__hls)
            pyapi.decref(xrlg__eske)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    yaa__bse = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = yaa__bse.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        lyesc__rwsz = typ.table_type
        mqhy__xln = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, lyesc__rwsz, mqhy__xln)
        ofs__oek = box_table(lyesc__rwsz, mqhy__xln, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (bomjt__mecce, aab__ezbrr):
            with bomjt__mecce:
                zqye__xle = pyapi.object_getattr_string(ofs__oek, 'arrays')
                xnrba__abea = c.pyapi.make_none()
                if n_cols is None:
                    zof__cpun = pyapi.call_method(zqye__xle, '__len__', ())
                    nqs__cogt = pyapi.long_as_longlong(zof__cpun)
                    pyapi.decref(zof__cpun)
                else:
                    nqs__cogt = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, nqs__cogt) as nxy__zdnzn:
                    i = nxy__zdnzn.index
                    jts__ljgno = pyapi.list_getitem(zqye__xle, i)
                    ftlx__zivqd = c.builder.icmp_unsigned('!=', jts__ljgno,
                        xnrba__abea)
                    with builder.if_then(ftlx__zivqd):
                        usw__dpu = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, usw__dpu, jts__ljgno)
                        pyapi.decref(usw__dpu)
                pyapi.decref(zqye__xle)
                pyapi.decref(xnrba__abea)
            with aab__ezbrr:
                df_obj = builder.load(res)
                xrlg__eske = pyapi.object_getattr_string(df_obj, 'index')
                dsv__wvlvt = c.pyapi.call_method(ofs__oek, 'to_pandas', (
                    xrlg__eske,))
                builder.store(dsv__wvlvt, res)
                pyapi.decref(df_obj)
                pyapi.decref(xrlg__eske)
        pyapi.decref(ofs__oek)
    else:
        zmijs__jgvt = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        rwutt__qseyx = typ.data
        for i, arr, ampk__ohgzh in zip(range(n_cols), zmijs__jgvt, rwutt__qseyx
            ):
            wdxq__vpqh = cgutils.alloca_once_value(builder, arr)
            rhh__zcq = cgutils.alloca_once_value(builder, context.
                get_constant_null(ampk__ohgzh))
            ftlx__zivqd = builder.not_(is_ll_eq(builder, wdxq__vpqh, rhh__zcq))
            varl__smny = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, ftlx__zivqd))
            with builder.if_then(varl__smny):
                usw__dpu = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, ampk__ohgzh, arr)
                arr_obj = pyapi.from_native_value(ampk__ohgzh, arr, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, usw__dpu, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(usw__dpu)
    df_obj = builder.load(res)
    nnqhd__tsv = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', nnqhd__tsv)
    pyapi.decref(nnqhd__tsv)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    xnrba__abea = pyapi.borrow_none()
    abzo__qorhp = pyapi.unserialize(pyapi.serialize_object(slice))
    cuz__dmcze = pyapi.call_function_objargs(abzo__qorhp, [xnrba__abea])
    per__udkkf = pyapi.long_from_longlong(col_ind)
    hoicl__bele = pyapi.tuple_pack([cuz__dmcze, per__udkkf])
    krfq__zpys = pyapi.object_getattr_string(df_obj, 'iloc')
    xpfi__jizmv = pyapi.object_getitem(krfq__zpys, hoicl__bele)
    cdyci__blmdn = pyapi.object_getattr_string(xpfi__jizmv, 'array')
    hicr__syun = pyapi.unserialize(pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = pyapi.call_function_objargs(hicr__syun, [cdyci__blmdn])
    pyapi.decref(cdyci__blmdn)
    pyapi.decref(hicr__syun)
    pyapi.decref(abzo__qorhp)
    pyapi.decref(cuz__dmcze)
    pyapi.decref(per__udkkf)
    pyapi.decref(hoicl__bele)
    pyapi.decref(krfq__zpys)
    pyapi.decref(xpfi__jizmv)
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
        yaa__bse = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            yaa__bse.parent, args[1], data_typ)
        aymhd__pgz = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            mqhy__xln = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            zvaa__wslkk = df_typ.table_type.type_to_blk[data_typ]
            tqnv__edufl = getattr(mqhy__xln, f'block_{zvaa__wslkk}')
            bhf__gyttq = ListInstance(c.context, c.builder, types.List(
                data_typ), tqnv__edufl)
            gfc__gdz = context.get_constant(types.int64, df_typ.table_type.
                block_offsets[col_ind])
            bhf__gyttq.inititem(gfc__gdz, aymhd__pgz.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, aymhd__pgz.value, col_ind)
        njbwv__pek = DataFramePayloadType(df_typ)
        otuiq__zqn = context.nrt.meminfo_data(builder, yaa__bse.meminfo)
        lsuuf__zhbz = context.get_value_type(njbwv__pek).as_pointer()
        otuiq__zqn = builder.bitcast(otuiq__zqn, lsuuf__zhbz)
        builder.store(dataframe_payload._getvalue(), otuiq__zqn)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    cdyci__blmdn = c.pyapi.object_getattr_string(val, 'array')
    hicr__syun = c.pyapi.unserialize(c.pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = c.pyapi.call_function_objargs(hicr__syun, [cdyci__blmdn])
    oey__jana = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    xrlg__eske = c.pyapi.object_getattr_string(val, 'index')
    pmohf__rfbqw = c.pyapi.to_native_value(typ.index, xrlg__eske).value
    sipu__kpltg = c.pyapi.object_getattr_string(val, 'name')
    kxja__hjx = c.pyapi.to_native_value(typ.name_typ, sipu__kpltg).value
    ifp__hxvmi = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, oey__jana, pmohf__rfbqw, kxja__hjx)
    c.pyapi.decref(hicr__syun)
    c.pyapi.decref(cdyci__blmdn)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(xrlg__eske)
    c.pyapi.decref(sipu__kpltg)
    return NativeValue(ifp__hxvmi)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        rqm__egvo = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(rqm__egvo._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    ujr__mqr = c.context.insert_const_string(c.builder.module, 'pandas')
    ezmub__iaekv = c.pyapi.import_module_noblock(ujr__mqr)
    juwv__smtw = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, juwv__smtw.data)
    c.context.nrt.incref(c.builder, typ.index, juwv__smtw.index)
    c.context.nrt.incref(c.builder, typ.name_typ, juwv__smtw.name)
    arr_obj = c.pyapi.from_native_value(typ.data, juwv__smtw.data, c.
        env_manager)
    xrlg__eske = c.pyapi.from_native_value(typ.index, juwv__smtw.index, c.
        env_manager)
    sipu__kpltg = c.pyapi.from_native_value(typ.name_typ, juwv__smtw.name,
        c.env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(ezmub__iaekv, 'Series', (arr_obj, xrlg__eske,
        dtype, sipu__kpltg))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(xrlg__eske)
    c.pyapi.decref(sipu__kpltg)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(ezmub__iaekv)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    xsihc__tkrb = []
    for mjo__ypjb in typ_list:
        if isinstance(mjo__ypjb, int) and not isinstance(mjo__ypjb, bool):
            eosxl__ntn = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), mjo__ypjb))
        else:
            oftwl__laqnp = numba.typeof(mjo__ypjb)
            slwm__nhnhh = context.get_constant_generic(builder,
                oftwl__laqnp, mjo__ypjb)
            eosxl__ntn = pyapi.from_native_value(oftwl__laqnp, slwm__nhnhh,
                env_manager)
        xsihc__tkrb.append(eosxl__ntn)
    crbp__xqm = pyapi.list_pack(xsihc__tkrb)
    for val in xsihc__tkrb:
        pyapi.decref(val)
    return crbp__xqm


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    eweq__ryfzf = not typ.has_runtime_cols
    bhi__prsix = 2 if eweq__ryfzf else 1
    nuzs__tmjq = pyapi.dict_new(bhi__prsix)
    zcd__cjpl = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(nuzs__tmjq, 'dist', zcd__cjpl)
    pyapi.decref(zcd__cjpl)
    if eweq__ryfzf:
        hnnls__sshv = _dtype_to_type_enum_list(typ.index)
        if hnnls__sshv != None:
            tfi__mcmzg = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, hnnls__sshv)
        else:
            tfi__mcmzg = pyapi.make_none()
        if typ.is_table_format:
            oygaz__ook = typ.table_type
            kpo__wick = pyapi.list_new(lir.Constant(lir.IntType(64), len(
                typ.data)))
            for zvaa__wslkk, dtype in oygaz__ook.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                nqs__cogt = c.context.get_constant(types.int64, len(
                    oygaz__ook.block_to_arr_ind[zvaa__wslkk]))
                cfuoh__rwxzy = c.context.make_constant_array(c.builder,
                    types.Array(types.int64, 1, 'C'), np.array(oygaz__ook.
                    block_to_arr_ind[zvaa__wslkk], dtype=np.int64))
                sngvb__xvjpb = c.context.make_array(types.Array(types.int64,
                    1, 'C'))(c.context, c.builder, cfuoh__rwxzy)
                with cgutils.for_range(c.builder, nqs__cogt) as nxy__zdnzn:
                    i = nxy__zdnzn.index
                    vwobw__sqn = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), sngvb__xvjpb, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(kpo__wick, vwobw__sqn, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            vgadp__piu = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    crbp__xqm = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    crbp__xqm = pyapi.make_none()
                vgadp__piu.append(crbp__xqm)
            kpo__wick = pyapi.list_pack(vgadp__piu)
            for val in vgadp__piu:
                pyapi.decref(val)
        eff__dohu = pyapi.list_pack([tfi__mcmzg, kpo__wick])
        pyapi.dict_setitem_string(nuzs__tmjq, 'type_metadata', eff__dohu)
    pyapi.object_setattr_string(obj, '_bodo_meta', nuzs__tmjq)
    pyapi.decref(nuzs__tmjq)


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
    nuzs__tmjq = pyapi.dict_new(2)
    zcd__cjpl = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    hnnls__sshv = _dtype_to_type_enum_list(typ.index)
    if hnnls__sshv != None:
        tfi__mcmzg = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, hnnls__sshv)
    else:
        tfi__mcmzg = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            wgfa__eno = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            wgfa__eno = pyapi.make_none()
    else:
        wgfa__eno = pyapi.make_none()
    bevrd__mxmkx = pyapi.list_pack([tfi__mcmzg, wgfa__eno])
    pyapi.dict_setitem_string(nuzs__tmjq, 'type_metadata', bevrd__mxmkx)
    pyapi.decref(bevrd__mxmkx)
    pyapi.dict_setitem_string(nuzs__tmjq, 'dist', zcd__cjpl)
    pyapi.object_setattr_string(obj, '_bodo_meta', nuzs__tmjq)
    pyapi.decref(nuzs__tmjq)
    pyapi.decref(zcd__cjpl)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as eqng__arls:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    pdzqy__wkla = numba.np.numpy_support.map_layout(val)
    kjdn__wwm = not val.flags.writeable
    return types.Array(dtype, val.ndim, pdzqy__wkla, readonly=kjdn__wwm)


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
    foq__gbyak = val[i]
    only__rpxhy = 100
    if isinstance(foq__gbyak, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(foq__gbyak, (bytes, bytearray)):
        return binary_array_type
    elif isinstance(foq__gbyak, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(foq__gbyak, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(foq__gbyak))
    elif isinstance(foq__gbyak, (float, np.float32, np.float64)):
        return bodo.libs.float_arr_ext.FloatingArrayType(numba.typeof(
            foq__gbyak))
    elif isinstance(foq__gbyak, (dict, Dict)) and len(foq__gbyak.keys()
        ) <= only__rpxhy and all(isinstance(nor__ajgwz, str) for nor__ajgwz in
        foq__gbyak.keys()):
        sdw__psio = tuple(foq__gbyak.keys())
        wyad__xvfx = tuple(_get_struct_value_arr_type(v) for v in
            foq__gbyak.values())
        return StructArrayType(wyad__xvfx, sdw__psio)
    elif isinstance(foq__gbyak, (dict, Dict)):
        nrqex__xgudd = numba.typeof(_value_to_array(list(foq__gbyak.keys())))
        kirh__sgw = numba.typeof(_value_to_array(list(foq__gbyak.values())))
        nrqex__xgudd = to_str_arr_if_dict_array(nrqex__xgudd)
        kirh__sgw = to_str_arr_if_dict_array(kirh__sgw)
        return MapArrayType(nrqex__xgudd, kirh__sgw)
    elif isinstance(foq__gbyak, tuple):
        wyad__xvfx = tuple(_get_struct_value_arr_type(v) for v in foq__gbyak)
        return TupleArrayType(wyad__xvfx)
    if isinstance(foq__gbyak, (list, np.ndarray, pd.arrays.BooleanArray, pd
        .arrays.IntegerArray, pd.arrays.FloatingArray, pd.arrays.
        StringArray, pd.arrays.ArrowStringArray)):
        if isinstance(foq__gbyak, list):
            foq__gbyak = _value_to_array(foq__gbyak)
        ecng__xwm = numba.typeof(foq__gbyak)
        ecng__xwm = to_str_arr_if_dict_array(ecng__xwm)
        return ArrayItemArrayType(ecng__xwm)
    if isinstance(foq__gbyak, datetime.date):
        return datetime_date_array_type
    if isinstance(foq__gbyak, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(foq__gbyak, bodo.Time):
        return TimeArrayType(foq__gbyak.precision)
    if isinstance(foq__gbyak, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(foq__gbyak, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(f'Unsupported object array with first value: {foq__gbyak}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    dulg__fdb = val.copy()
    dulg__fdb.append(None)
    arr = np.array(dulg__fdb, np.object_)
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
    ampk__ohgzh = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        ampk__ohgzh = to_nullable_type(ampk__ohgzh)
    return ampk__ohgzh
