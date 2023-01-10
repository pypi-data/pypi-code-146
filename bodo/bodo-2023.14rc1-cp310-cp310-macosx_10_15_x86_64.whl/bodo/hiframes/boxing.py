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
    occfr__fcvt = tuple(val.columns.to_list())
    xkm__hlxcl = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        dep__wtllz = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        dep__wtllz = numba.typeof(val.index)
    mtmt__hberv = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    syhcf__poy = len(xkm__hlxcl) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(xkm__hlxcl, dep__wtllz, occfr__fcvt, mtmt__hberv,
        is_table_format=syhcf__poy)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    mtmt__hberv = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        gmr__hzr = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        gmr__hzr = numba.typeof(val.index)
    xqoe__vboe = _infer_series_arr_type(val)
    if _use_dict_str_type and xqoe__vboe == string_array_type:
        xqoe__vboe = bodo.dict_str_arr_type
    return SeriesType(xqoe__vboe.dtype, data=xqoe__vboe, index=gmr__hzr,
        name_typ=numba.typeof(val.name), dist=mtmt__hberv)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    mcw__zdf = c.pyapi.object_getattr_string(val, 'index')
    xaea__hrioh = c.pyapi.to_native_value(typ.index, mcw__zdf).value
    c.pyapi.decref(mcw__zdf)
    if typ.is_table_format:
        txviw__znm = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        txviw__znm.parent = val
        for eeml__ooxqs, hxdvg__ceq in typ.table_type.type_to_blk.items():
            nycm__gbegd = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[hxdvg__ceq]))
            hdio__ikkkc, dhkb__azzqj = ListInstance.allocate_ex(c.context,
                c.builder, types.List(eeml__ooxqs), nycm__gbegd)
            dhkb__azzqj.size = nycm__gbegd
            setattr(txviw__znm, f'block_{hxdvg__ceq}', dhkb__azzqj.value)
        rodlb__fff = c.pyapi.call_method(val, '__len__', ())
        gyid__vcaz = c.pyapi.long_as_longlong(rodlb__fff)
        c.pyapi.decref(rodlb__fff)
        txviw__znm.len = gyid__vcaz
        jghfe__hyulr = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [txviw__znm._getvalue()])
    else:
        yrw__zxk = [c.context.get_constant_null(eeml__ooxqs) for
            eeml__ooxqs in typ.data]
        jghfe__hyulr = c.context.make_tuple(c.builder, types.Tuple(typ.data
            ), yrw__zxk)
    wjo__bnw = construct_dataframe(c.context, c.builder, typ, jghfe__hyulr,
        xaea__hrioh, val, None)
    return NativeValue(wjo__bnw)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        yekqk__fbn = df._bodo_meta['type_metadata'][1]
    else:
        yekqk__fbn = [None] * len(df.columns)
    oeb__ecavy = [_infer_series_arr_type(df.iloc[:, i], array_metadata=
        yekqk__fbn[i]) for i in range(len(df.columns))]
    oeb__ecavy = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        eeml__ooxqs == string_array_type else eeml__ooxqs) for eeml__ooxqs in
        oeb__ecavy]
    return tuple(oeb__ecavy)


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
    uao__sonb, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(uao__sonb) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {uao__sonb}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        oun__jkz, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return oun__jkz, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.FloatingArray.value:
        oun__jkz, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return oun__jkz, FloatingArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        oun__jkz, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return oun__jkz, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        mswhb__pzgby = typ_enum_list[1]
        fny__xif = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(mswhb__pzgby, fny__xif)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        fnd__gvw = typ_enum_list[1]
        mwhj__ddwcg = tuple(typ_enum_list[2:2 + fnd__gvw])
        muiv__tdgwg = typ_enum_list[2 + fnd__gvw:]
        nvmrj__corfc = []
        for i in range(fnd__gvw):
            muiv__tdgwg, asru__lzsd = _dtype_from_type_enum_list_recursor(
                muiv__tdgwg)
            nvmrj__corfc.append(asru__lzsd)
        return muiv__tdgwg, StructType(tuple(nvmrj__corfc), mwhj__ddwcg)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        pzx__kle = typ_enum_list[1]
        muiv__tdgwg = typ_enum_list[2:]
        return muiv__tdgwg, pzx__kle
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        pzx__kle = typ_enum_list[1]
        muiv__tdgwg = typ_enum_list[2:]
        return muiv__tdgwg, numba.types.literal(pzx__kle)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        muiv__tdgwg, kszaq__pzixu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        muiv__tdgwg, bfrzq__qcvg = _dtype_from_type_enum_list_recursor(
            muiv__tdgwg)
        muiv__tdgwg, qzmum__nfopg = _dtype_from_type_enum_list_recursor(
            muiv__tdgwg)
        muiv__tdgwg, zeoj__lljjr = _dtype_from_type_enum_list_recursor(
            muiv__tdgwg)
        muiv__tdgwg, iajnu__boc = _dtype_from_type_enum_list_recursor(
            muiv__tdgwg)
        return muiv__tdgwg, PDCategoricalDtype(kszaq__pzixu, bfrzq__qcvg,
            qzmum__nfopg, zeoj__lljjr, iajnu__boc)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        muiv__tdgwg, hddbq__mnl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return muiv__tdgwg, DatetimeIndexType(hddbq__mnl)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        muiv__tdgwg, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        muiv__tdgwg, hddbq__mnl = _dtype_from_type_enum_list_recursor(
            muiv__tdgwg)
        muiv__tdgwg, zeoj__lljjr = _dtype_from_type_enum_list_recursor(
            muiv__tdgwg)
        return muiv__tdgwg, NumericIndexType(dtype, hddbq__mnl, zeoj__lljjr)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        muiv__tdgwg, wckj__xlyn = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        muiv__tdgwg, hddbq__mnl = _dtype_from_type_enum_list_recursor(
            muiv__tdgwg)
        return muiv__tdgwg, PeriodIndexType(wckj__xlyn, hddbq__mnl)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        muiv__tdgwg, zeoj__lljjr = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        muiv__tdgwg, hddbq__mnl = _dtype_from_type_enum_list_recursor(
            muiv__tdgwg)
        return muiv__tdgwg, CategoricalIndexType(zeoj__lljjr, hddbq__mnl)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        muiv__tdgwg, hddbq__mnl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return muiv__tdgwg, RangeIndexType(hddbq__mnl)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        muiv__tdgwg, hddbq__mnl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return muiv__tdgwg, StringIndexType(hddbq__mnl)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        muiv__tdgwg, hddbq__mnl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return muiv__tdgwg, BinaryIndexType(hddbq__mnl)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        muiv__tdgwg, hddbq__mnl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return muiv__tdgwg, TimedeltaIndexType(hddbq__mnl)
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
        ffayx__ntdfj = get_overload_const_int(typ)
        if numba.types.maybe_literal(ffayx__ntdfj) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ffayx__ntdfj]
    elif is_overload_constant_str(typ):
        ffayx__ntdfj = get_overload_const_str(typ)
        if numba.types.maybe_literal(ffayx__ntdfj) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ffayx__ntdfj]
    elif is_overload_constant_bool(typ):
        ffayx__ntdfj = get_overload_const_bool(typ)
        if numba.types.maybe_literal(ffayx__ntdfj) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ffayx__ntdfj]
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
        mhcpv__uke = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for gkvh__yhrcz in typ.names:
            mhcpv__uke.append(gkvh__yhrcz)
        for apeky__iphhp in typ.data:
            mhcpv__uke += _dtype_to_type_enum_list_recursor(apeky__iphhp)
        return mhcpv__uke
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        hte__kpdcb = _dtype_to_type_enum_list_recursor(typ.categories)
        bcxu__bmgrt = _dtype_to_type_enum_list_recursor(typ.elem_type)
        phq__lkzp = _dtype_to_type_enum_list_recursor(typ.ordered)
        xyzbn__coue = _dtype_to_type_enum_list_recursor(typ.data)
        rye__hhqmm = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + hte__kpdcb + bcxu__bmgrt + phq__lkzp + xyzbn__coue + rye__hhqmm
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                mmbj__adq = types.float64
                if isinstance(typ.data, FloatingArrayType):
                    hpcyx__ztn = FloatingArrayType(mmbj__adq)
                else:
                    hpcyx__ztn = types.Array(mmbj__adq, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                mmbj__adq = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    hpcyx__ztn = IntegerArrayType(mmbj__adq)
                else:
                    hpcyx__ztn = types.Array(mmbj__adq, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                mmbj__adq = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    hpcyx__ztn = IntegerArrayType(mmbj__adq)
                else:
                    hpcyx__ztn = types.Array(mmbj__adq, 1, 'C')
            elif typ.dtype == types.bool_:
                mmbj__adq = typ.dtype
                hpcyx__ztn = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(mmbj__adq
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(hpcyx__ztn)
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
                yoa__nzdm = S._bodo_meta['type_metadata'][1]
                return dtype_to_array_type(_dtype_from_type_enum_list(
                    yoa__nzdm))
        return bodo.typeof(_fix_series_arr_type(S.array))
    try:
        yld__uhlia = bodo.typeof(_fix_series_arr_type(S.array))
        if yld__uhlia == types.Array(types.bool_, 1, 'C'):
            yld__uhlia = bodo.boolean_array
        if isinstance(yld__uhlia, types.Array):
            assert yld__uhlia.ndim == 1, 'invalid numpy array type in Series'
            yld__uhlia = types.Array(yld__uhlia.dtype, 1, 'C')
        return yld__uhlia
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    ttfq__npam = cgutils.is_not_null(builder, parent_obj)
    vqy__jbo = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(ttfq__npam):
        lhkqk__liike = pyapi.object_getattr_string(parent_obj, 'columns')
        rodlb__fff = pyapi.call_method(lhkqk__liike, '__len__', ())
        builder.store(pyapi.long_as_longlong(rodlb__fff), vqy__jbo)
        pyapi.decref(rodlb__fff)
        pyapi.decref(lhkqk__liike)
    use_parent_obj = builder.and_(ttfq__npam, builder.icmp_unsigned('==',
        builder.load(vqy__jbo), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        hln__nvq = df_typ.runtime_colname_typ
        context.nrt.incref(builder, hln__nvq, dataframe_payload.columns)
        return pyapi.from_native_value(hln__nvq, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        ekgbt__orun = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        ekgbt__orun = np.array(df_typ.columns, 'int64')
    else:
        ekgbt__orun = df_typ.columns
    hapl__tgida = numba.typeof(ekgbt__orun)
    bwl__jjgam = context.get_constant_generic(builder, hapl__tgida, ekgbt__orun
        )
    hij__ziovl = pyapi.from_native_value(hapl__tgida, bwl__jjgam, c.env_manager
        )
    if (hapl__tgida == bodo.string_array_type and bodo.libs.str_arr_ext.
        use_pd_pyarrow_string_array):
        vhsr__orsbz = hij__ziovl
        hij__ziovl = pyapi.call_method(hij__ziovl, 'to_numpy', ())
        pyapi.decref(vhsr__orsbz)
    return hij__ziovl


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (dqy__sgdyi, lczp__pkxi):
        with dqy__sgdyi:
            pyapi.incref(obj)
            okh__htd = context.insert_const_string(c.builder.module, 'numpy')
            aooe__cwx = pyapi.import_module_noblock(okh__htd)
            if df_typ.has_runtime_cols:
                iqap__rvkkw = 0
            else:
                iqap__rvkkw = len(df_typ.columns)
            bzlkd__tnlh = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), iqap__rvkkw))
            rys__zjgsw = pyapi.call_method(aooe__cwx, 'arange', (bzlkd__tnlh,))
            pyapi.object_setattr_string(obj, 'columns', rys__zjgsw)
            pyapi.decref(aooe__cwx)
            pyapi.decref(rys__zjgsw)
            pyapi.decref(bzlkd__tnlh)
        with lczp__pkxi:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            eyfgg__ewhzt = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            okh__htd = context.insert_const_string(c.builder.module, 'pandas')
            aooe__cwx = pyapi.import_module_noblock(okh__htd)
            df_obj = pyapi.call_method(aooe__cwx, 'DataFrame', (pyapi.
                borrow_none(), eyfgg__ewhzt))
            pyapi.decref(aooe__cwx)
            pyapi.decref(eyfgg__ewhzt)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    cemzm__lcw = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = cemzm__lcw.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        msw__dky = typ.table_type
        txviw__znm = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, msw__dky, txviw__znm)
        vfqzd__iurgq = box_table(msw__dky, txviw__znm, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (hfh__gwevt, veq__rqqxo):
            with hfh__gwevt:
                jge__ktleq = pyapi.object_getattr_string(vfqzd__iurgq, 'arrays'
                    )
                kamqa__arsu = c.pyapi.make_none()
                if n_cols is None:
                    rodlb__fff = pyapi.call_method(jge__ktleq, '__len__', ())
                    nycm__gbegd = pyapi.long_as_longlong(rodlb__fff)
                    pyapi.decref(rodlb__fff)
                else:
                    nycm__gbegd = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, nycm__gbegd) as vure__gwu:
                    i = vure__gwu.index
                    rehl__stzt = pyapi.list_getitem(jge__ktleq, i)
                    cownb__bml = c.builder.icmp_unsigned('!=', rehl__stzt,
                        kamqa__arsu)
                    with builder.if_then(cownb__bml):
                        kcexn__mvljo = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, kcexn__mvljo, rehl__stzt)
                        pyapi.decref(kcexn__mvljo)
                pyapi.decref(jge__ktleq)
                pyapi.decref(kamqa__arsu)
            with veq__rqqxo:
                df_obj = builder.load(res)
                eyfgg__ewhzt = pyapi.object_getattr_string(df_obj, 'index')
                taiyo__lozr = c.pyapi.call_method(vfqzd__iurgq, 'to_pandas',
                    (eyfgg__ewhzt,))
                builder.store(taiyo__lozr, res)
                pyapi.decref(df_obj)
                pyapi.decref(eyfgg__ewhzt)
        pyapi.decref(vfqzd__iurgq)
    else:
        zceki__ktj = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        quzmf__aopmm = typ.data
        for i, arr, xqoe__vboe in zip(range(n_cols), zceki__ktj, quzmf__aopmm):
            eay__jio = cgutils.alloca_once_value(builder, arr)
            tptic__vggn = cgutils.alloca_once_value(builder, context.
                get_constant_null(xqoe__vboe))
            cownb__bml = builder.not_(is_ll_eq(builder, eay__jio, tptic__vggn))
            luiz__qorzt = builder.or_(builder.not_(use_parent_obj), builder
                .and_(use_parent_obj, cownb__bml))
            with builder.if_then(luiz__qorzt):
                kcexn__mvljo = pyapi.long_from_longlong(context.
                    get_constant(types.int64, i))
                context.nrt.incref(builder, xqoe__vboe, arr)
                arr_obj = pyapi.from_native_value(xqoe__vboe, arr, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, kcexn__mvljo, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(kcexn__mvljo)
    df_obj = builder.load(res)
    hij__ziovl = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', hij__ziovl)
    pyapi.decref(hij__ziovl)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    kamqa__arsu = pyapi.borrow_none()
    qlubu__efnh = pyapi.unserialize(pyapi.serialize_object(slice))
    swff__tus = pyapi.call_function_objargs(qlubu__efnh, [kamqa__arsu])
    btm__saiqx = pyapi.long_from_longlong(col_ind)
    txoew__kdlt = pyapi.tuple_pack([swff__tus, btm__saiqx])
    ima__nzzxr = pyapi.object_getattr_string(df_obj, 'iloc')
    ogej__fuaup = pyapi.object_getitem(ima__nzzxr, txoew__kdlt)
    mjp__tck = pyapi.object_getattr_string(ogej__fuaup, 'array')
    ysl__ryog = pyapi.unserialize(pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = pyapi.call_function_objargs(ysl__ryog, [mjp__tck])
    pyapi.decref(mjp__tck)
    pyapi.decref(ysl__ryog)
    pyapi.decref(qlubu__efnh)
    pyapi.decref(swff__tus)
    pyapi.decref(btm__saiqx)
    pyapi.decref(txoew__kdlt)
    pyapi.decref(ima__nzzxr)
    pyapi.decref(ogej__fuaup)
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
        cemzm__lcw = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            cemzm__lcw.parent, args[1], data_typ)
        socp__elmnx = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            txviw__znm = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            hxdvg__ceq = df_typ.table_type.type_to_blk[data_typ]
            jpyzh__bewnb = getattr(txviw__znm, f'block_{hxdvg__ceq}')
            vnoq__ywem = ListInstance(c.context, c.builder, types.List(
                data_typ), jpyzh__bewnb)
            kcg__jlop = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[col_ind])
            vnoq__ywem.inititem(kcg__jlop, socp__elmnx.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, socp__elmnx.value, col_ind)
        krgmc__mze = DataFramePayloadType(df_typ)
        eha__rah = context.nrt.meminfo_data(builder, cemzm__lcw.meminfo)
        odc__jvhvm = context.get_value_type(krgmc__mze).as_pointer()
        eha__rah = builder.bitcast(eha__rah, odc__jvhvm)
        builder.store(dataframe_payload._getvalue(), eha__rah)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    mjp__tck = c.pyapi.object_getattr_string(val, 'array')
    ysl__ryog = c.pyapi.unserialize(c.pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = c.pyapi.call_function_objargs(ysl__ryog, [mjp__tck])
    woc__nhhb = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    eyfgg__ewhzt = c.pyapi.object_getattr_string(val, 'index')
    xaea__hrioh = c.pyapi.to_native_value(typ.index, eyfgg__ewhzt).value
    agd__xdztc = c.pyapi.object_getattr_string(val, 'name')
    mqugr__jkg = c.pyapi.to_native_value(typ.name_typ, agd__xdztc).value
    wofw__urh = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, woc__nhhb, xaea__hrioh, mqugr__jkg)
    c.pyapi.decref(ysl__ryog)
    c.pyapi.decref(mjp__tck)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(eyfgg__ewhzt)
    c.pyapi.decref(agd__xdztc)
    return NativeValue(wofw__urh)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        diz__ywuc = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(diz__ywuc._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    okh__htd = c.context.insert_const_string(c.builder.module, 'pandas')
    iut__znz = c.pyapi.import_module_noblock(okh__htd)
    pitxg__kcbq = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, pitxg__kcbq.data)
    c.context.nrt.incref(c.builder, typ.index, pitxg__kcbq.index)
    c.context.nrt.incref(c.builder, typ.name_typ, pitxg__kcbq.name)
    arr_obj = c.pyapi.from_native_value(typ.data, pitxg__kcbq.data, c.
        env_manager)
    eyfgg__ewhzt = c.pyapi.from_native_value(typ.index, pitxg__kcbq.index,
        c.env_manager)
    agd__xdztc = c.pyapi.from_native_value(typ.name_typ, pitxg__kcbq.name,
        c.env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(iut__znz, 'Series', (arr_obj, eyfgg__ewhzt,
        dtype, agd__xdztc))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(eyfgg__ewhzt)
    c.pyapi.decref(agd__xdztc)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(iut__znz)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    pbupq__cxpf = []
    for qdijt__kdjq in typ_list:
        if isinstance(qdijt__kdjq, int) and not isinstance(qdijt__kdjq, bool):
            pszbe__iauu = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), qdijt__kdjq))
        else:
            yvbwm__lon = numba.typeof(qdijt__kdjq)
            gbjk__tmsat = context.get_constant_generic(builder, yvbwm__lon,
                qdijt__kdjq)
            pszbe__iauu = pyapi.from_native_value(yvbwm__lon, gbjk__tmsat,
                env_manager)
        pbupq__cxpf.append(pszbe__iauu)
    kem__ajhg = pyapi.list_pack(pbupq__cxpf)
    for val in pbupq__cxpf:
        pyapi.decref(val)
    return kem__ajhg


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    xyhy__tbkjt = not typ.has_runtime_cols
    rdkwa__yqdt = 2 if xyhy__tbkjt else 1
    juzn__wkusk = pyapi.dict_new(rdkwa__yqdt)
    rgvz__zby = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(juzn__wkusk, 'dist', rgvz__zby)
    pyapi.decref(rgvz__zby)
    if xyhy__tbkjt:
        myyfv__znsa = _dtype_to_type_enum_list(typ.index)
        if myyfv__znsa != None:
            gmh__tpe = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, myyfv__znsa)
        else:
            gmh__tpe = pyapi.make_none()
        if typ.is_table_format:
            eeml__ooxqs = typ.table_type
            oit__btz = pyapi.list_new(lir.Constant(lir.IntType(64), len(typ
                .data)))
            for hxdvg__ceq, dtype in eeml__ooxqs.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                nycm__gbegd = c.context.get_constant(types.int64, len(
                    eeml__ooxqs.block_to_arr_ind[hxdvg__ceq]))
                xoc__fgp = c.context.make_constant_array(c.builder, types.
                    Array(types.int64, 1, 'C'), np.array(eeml__ooxqs.
                    block_to_arr_ind[hxdvg__ceq], dtype=np.int64))
                gxs__ppd = c.context.make_array(types.Array(types.int64, 1,
                    'C'))(c.context, c.builder, xoc__fgp)
                with cgutils.for_range(c.builder, nycm__gbegd) as vure__gwu:
                    i = vure__gwu.index
                    fjtmm__pnhte = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), gxs__ppd, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(oit__btz, fjtmm__pnhte, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            wygd__irmd = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    kem__ajhg = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    kem__ajhg = pyapi.make_none()
                wygd__irmd.append(kem__ajhg)
            oit__btz = pyapi.list_pack(wygd__irmd)
            for val in wygd__irmd:
                pyapi.decref(val)
        pim__dkrrv = pyapi.list_pack([gmh__tpe, oit__btz])
        pyapi.dict_setitem_string(juzn__wkusk, 'type_metadata', pim__dkrrv)
    pyapi.object_setattr_string(obj, '_bodo_meta', juzn__wkusk)
    pyapi.decref(juzn__wkusk)


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
    juzn__wkusk = pyapi.dict_new(2)
    rgvz__zby = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    myyfv__znsa = _dtype_to_type_enum_list(typ.index)
    if myyfv__znsa != None:
        gmh__tpe = type_enum_list_to_py_list_obj(pyapi, context, builder, c
            .env_manager, myyfv__znsa)
    else:
        gmh__tpe = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            rug__hbhbu = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            rug__hbhbu = pyapi.make_none()
    else:
        rug__hbhbu = pyapi.make_none()
    vovi__cwgp = pyapi.list_pack([gmh__tpe, rug__hbhbu])
    pyapi.dict_setitem_string(juzn__wkusk, 'type_metadata', vovi__cwgp)
    pyapi.decref(vovi__cwgp)
    pyapi.dict_setitem_string(juzn__wkusk, 'dist', rgvz__zby)
    pyapi.object_setattr_string(obj, '_bodo_meta', juzn__wkusk)
    pyapi.decref(juzn__wkusk)
    pyapi.decref(rgvz__zby)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as sxlo__kiul:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    ympf__nxsh = numba.np.numpy_support.map_layout(val)
    uzfl__obz = not val.flags.writeable
    return types.Array(dtype, val.ndim, ympf__nxsh, readonly=uzfl__obz)


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
    qur__wgxk = val[i]
    sliaz__ltj = 100
    if isinstance(qur__wgxk, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(qur__wgxk, (bytes, bytearray)):
        return binary_array_type
    elif isinstance(qur__wgxk, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(qur__wgxk, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(qur__wgxk))
    elif isinstance(qur__wgxk, (float, np.float32, np.float64)):
        return bodo.libs.float_arr_ext.FloatingArrayType(numba.typeof(
            qur__wgxk))
    elif isinstance(qur__wgxk, (dict, Dict)) and len(qur__wgxk.keys()
        ) <= sliaz__ltj and all(isinstance(oxnbu__elion, str) for
        oxnbu__elion in qur__wgxk.keys()):
        mwhj__ddwcg = tuple(qur__wgxk.keys())
        rcdf__yvast = tuple(_get_struct_value_arr_type(v) for v in
            qur__wgxk.values())
        return StructArrayType(rcdf__yvast, mwhj__ddwcg)
    elif isinstance(qur__wgxk, (dict, Dict)):
        xmhv__jldv = numba.typeof(_value_to_array(list(qur__wgxk.keys())))
        rwd__aaic = numba.typeof(_value_to_array(list(qur__wgxk.values())))
        xmhv__jldv = to_str_arr_if_dict_array(xmhv__jldv)
        rwd__aaic = to_str_arr_if_dict_array(rwd__aaic)
        return MapArrayType(xmhv__jldv, rwd__aaic)
    elif isinstance(qur__wgxk, tuple):
        rcdf__yvast = tuple(_get_struct_value_arr_type(v) for v in qur__wgxk)
        return TupleArrayType(rcdf__yvast)
    if isinstance(qur__wgxk, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.FloatingArray, pd.arrays.StringArray,
        pd.arrays.ArrowStringArray)):
        if isinstance(qur__wgxk, list):
            qur__wgxk = _value_to_array(qur__wgxk)
        ufqlu__huk = numba.typeof(qur__wgxk)
        ufqlu__huk = to_str_arr_if_dict_array(ufqlu__huk)
        return ArrayItemArrayType(ufqlu__huk)
    if isinstance(qur__wgxk, datetime.date):
        return datetime_date_array_type
    if isinstance(qur__wgxk, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(qur__wgxk, bodo.Time):
        return TimeArrayType(qur__wgxk.precision)
    if isinstance(qur__wgxk, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(qur__wgxk, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(f'Unsupported object array with first value: {qur__wgxk}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    itxmd__ifr = val.copy()
    itxmd__ifr.append(None)
    arr = np.array(itxmd__ifr, np.object_)
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
    xqoe__vboe = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        xqoe__vboe = to_nullable_type(xqoe__vboe)
    return xqoe__vboe
