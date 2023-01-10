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
    nero__hjlbt = tuple(val.columns.to_list())
    euxtx__fwqli = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        pahrw__eqiom = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        pahrw__eqiom = numba.typeof(val.index)
    acwtt__zqvi = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    tpwf__bnkwq = len(euxtx__fwqli) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(euxtx__fwqli, pahrw__eqiom, nero__hjlbt,
        acwtt__zqvi, is_table_format=tpwf__bnkwq)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    acwtt__zqvi = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        eazc__czh = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        eazc__czh = numba.typeof(val.index)
    hcrcj__sjfd = _infer_series_arr_type(val)
    if _use_dict_str_type and hcrcj__sjfd == string_array_type:
        hcrcj__sjfd = bodo.dict_str_arr_type
    return SeriesType(hcrcj__sjfd.dtype, data=hcrcj__sjfd, index=eazc__czh,
        name_typ=numba.typeof(val.name), dist=acwtt__zqvi)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    pcpd__vipjt = c.pyapi.object_getattr_string(val, 'index')
    mwmxp__niyhn = c.pyapi.to_native_value(typ.index, pcpd__vipjt).value
    c.pyapi.decref(pcpd__vipjt)
    if typ.is_table_format:
        yscf__jtt = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        yscf__jtt.parent = val
        for ujsxf__oic, cqyfe__ovhid in typ.table_type.type_to_blk.items():
            vhx__benhh = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[cqyfe__ovhid]))
            mzzt__gbb, wtplc__tgm = ListInstance.allocate_ex(c.context, c.
                builder, types.List(ujsxf__oic), vhx__benhh)
            wtplc__tgm.size = vhx__benhh
            setattr(yscf__jtt, f'block_{cqyfe__ovhid}', wtplc__tgm.value)
        jva__dtgsv = c.pyapi.call_method(val, '__len__', ())
        zyf__vux = c.pyapi.long_as_longlong(jva__dtgsv)
        c.pyapi.decref(jva__dtgsv)
        yscf__jtt.len = zyf__vux
        vjhqg__kwu = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [yscf__jtt._getvalue()])
    else:
        cvpd__jrruu = [c.context.get_constant_null(ujsxf__oic) for
            ujsxf__oic in typ.data]
        vjhqg__kwu = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            cvpd__jrruu)
    bgdf__fouy = construct_dataframe(c.context, c.builder, typ, vjhqg__kwu,
        mwmxp__niyhn, val, None)
    return NativeValue(bgdf__fouy)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        whgn__aur = df._bodo_meta['type_metadata'][1]
    else:
        whgn__aur = [None] * len(df.columns)
    qjnl__smjej = [_infer_series_arr_type(df.iloc[:, i], array_metadata=
        whgn__aur[i]) for i in range(len(df.columns))]
    qjnl__smjej = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        ujsxf__oic == string_array_type else ujsxf__oic) for ujsxf__oic in
        qjnl__smjej]
    return tuple(qjnl__smjej)


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
    azvw__iuodr, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(azvw__iuodr) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {azvw__iuodr}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        zsq__vnqu, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return zsq__vnqu, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.FloatingArray.value:
        zsq__vnqu, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return zsq__vnqu, FloatingArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        zsq__vnqu, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return zsq__vnqu, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        quuyx__qhm = typ_enum_list[1]
        ntxk__obxde = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(quuyx__qhm, ntxk__obxde)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        xzrxn__xgvu = typ_enum_list[1]
        upnv__cwx = tuple(typ_enum_list[2:2 + xzrxn__xgvu])
        nowi__htzsh = typ_enum_list[2 + xzrxn__xgvu:]
        lxfq__cybcb = []
        for i in range(xzrxn__xgvu):
            nowi__htzsh, iws__vajwc = _dtype_from_type_enum_list_recursor(
                nowi__htzsh)
            lxfq__cybcb.append(iws__vajwc)
        return nowi__htzsh, StructType(tuple(lxfq__cybcb), upnv__cwx)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        eiopt__phgd = typ_enum_list[1]
        nowi__htzsh = typ_enum_list[2:]
        return nowi__htzsh, eiopt__phgd
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        eiopt__phgd = typ_enum_list[1]
        nowi__htzsh = typ_enum_list[2:]
        return nowi__htzsh, numba.types.literal(eiopt__phgd)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        nowi__htzsh, wxvc__yzhjd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        nowi__htzsh, xwep__jmt = _dtype_from_type_enum_list_recursor(
            nowi__htzsh)
        nowi__htzsh, rchyf__hnl = _dtype_from_type_enum_list_recursor(
            nowi__htzsh)
        nowi__htzsh, rrdx__gsc = _dtype_from_type_enum_list_recursor(
            nowi__htzsh)
        nowi__htzsh, sjs__ybjci = _dtype_from_type_enum_list_recursor(
            nowi__htzsh)
        return nowi__htzsh, PDCategoricalDtype(wxvc__yzhjd, xwep__jmt,
            rchyf__hnl, rrdx__gsc, sjs__ybjci)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        nowi__htzsh, nyhao__jpcjf = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nowi__htzsh, DatetimeIndexType(nyhao__jpcjf)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        nowi__htzsh, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        nowi__htzsh, nyhao__jpcjf = _dtype_from_type_enum_list_recursor(
            nowi__htzsh)
        nowi__htzsh, rrdx__gsc = _dtype_from_type_enum_list_recursor(
            nowi__htzsh)
        return nowi__htzsh, NumericIndexType(dtype, nyhao__jpcjf, rrdx__gsc)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        nowi__htzsh, hplyh__dlcu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        nowi__htzsh, nyhao__jpcjf = _dtype_from_type_enum_list_recursor(
            nowi__htzsh)
        return nowi__htzsh, PeriodIndexType(hplyh__dlcu, nyhao__jpcjf)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        nowi__htzsh, rrdx__gsc = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        nowi__htzsh, nyhao__jpcjf = _dtype_from_type_enum_list_recursor(
            nowi__htzsh)
        return nowi__htzsh, CategoricalIndexType(rrdx__gsc, nyhao__jpcjf)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        nowi__htzsh, nyhao__jpcjf = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nowi__htzsh, RangeIndexType(nyhao__jpcjf)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        nowi__htzsh, nyhao__jpcjf = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nowi__htzsh, StringIndexType(nyhao__jpcjf)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        nowi__htzsh, nyhao__jpcjf = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nowi__htzsh, BinaryIndexType(nyhao__jpcjf)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        nowi__htzsh, nyhao__jpcjf = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nowi__htzsh, TimedeltaIndexType(nyhao__jpcjf)
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
        cig__vdil = get_overload_const_int(typ)
        if numba.types.maybe_literal(cig__vdil) == typ:
            return [SeriesDtypeEnum.LiteralType.value, cig__vdil]
    elif is_overload_constant_str(typ):
        cig__vdil = get_overload_const_str(typ)
        if numba.types.maybe_literal(cig__vdil) == typ:
            return [SeriesDtypeEnum.LiteralType.value, cig__vdil]
    elif is_overload_constant_bool(typ):
        cig__vdil = get_overload_const_bool(typ)
        if numba.types.maybe_literal(cig__vdil) == typ:
            return [SeriesDtypeEnum.LiteralType.value, cig__vdil]
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
        iwz__aun = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for ufz__jktqj in typ.names:
            iwz__aun.append(ufz__jktqj)
        for izju__vbkk in typ.data:
            iwz__aun += _dtype_to_type_enum_list_recursor(izju__vbkk)
        return iwz__aun
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        xsj__qvew = _dtype_to_type_enum_list_recursor(typ.categories)
        fqwzo__dujn = _dtype_to_type_enum_list_recursor(typ.elem_type)
        hulx__vwsm = _dtype_to_type_enum_list_recursor(typ.ordered)
        zar__sap = _dtype_to_type_enum_list_recursor(typ.data)
        ovle__zgot = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + xsj__qvew + fqwzo__dujn + hulx__vwsm + zar__sap + ovle__zgot
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                cskog__zhby = types.float64
                if isinstance(typ.data, FloatingArrayType):
                    xjfsx__uqig = FloatingArrayType(cskog__zhby)
                else:
                    xjfsx__uqig = types.Array(cskog__zhby, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                cskog__zhby = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    xjfsx__uqig = IntegerArrayType(cskog__zhby)
                else:
                    xjfsx__uqig = types.Array(cskog__zhby, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                cskog__zhby = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    xjfsx__uqig = IntegerArrayType(cskog__zhby)
                else:
                    xjfsx__uqig = types.Array(cskog__zhby, 1, 'C')
            elif typ.dtype == types.bool_:
                cskog__zhby = typ.dtype
                xjfsx__uqig = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(cskog__zhby
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(xjfsx__uqig)
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
                oaomd__utm = S._bodo_meta['type_metadata'][1]
                return dtype_to_array_type(_dtype_from_type_enum_list(
                    oaomd__utm))
        return bodo.typeof(_fix_series_arr_type(S.array))
    try:
        rai__oebg = bodo.typeof(_fix_series_arr_type(S.array))
        if rai__oebg == types.Array(types.bool_, 1, 'C'):
            rai__oebg = bodo.boolean_array
        if isinstance(rai__oebg, types.Array):
            assert rai__oebg.ndim == 1, 'invalid numpy array type in Series'
            rai__oebg = types.Array(rai__oebg.dtype, 1, 'C')
        return rai__oebg
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    ogls__cczq = cgutils.is_not_null(builder, parent_obj)
    lyxf__tyunl = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(ogls__cczq):
        tdtxw__jyh = pyapi.object_getattr_string(parent_obj, 'columns')
        jva__dtgsv = pyapi.call_method(tdtxw__jyh, '__len__', ())
        builder.store(pyapi.long_as_longlong(jva__dtgsv), lyxf__tyunl)
        pyapi.decref(jva__dtgsv)
        pyapi.decref(tdtxw__jyh)
    use_parent_obj = builder.and_(ogls__cczq, builder.icmp_unsigned('==',
        builder.load(lyxf__tyunl), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        vip__joro = df_typ.runtime_colname_typ
        context.nrt.incref(builder, vip__joro, dataframe_payload.columns)
        return pyapi.from_native_value(vip__joro, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        cqd__ginp = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        cqd__ginp = np.array(df_typ.columns, 'int64')
    else:
        cqd__ginp = df_typ.columns
    egqa__napjt = numba.typeof(cqd__ginp)
    gggd__peq = context.get_constant_generic(builder, egqa__napjt, cqd__ginp)
    lyb__ccz = pyapi.from_native_value(egqa__napjt, gggd__peq, c.env_manager)
    if (egqa__napjt == bodo.string_array_type and bodo.libs.str_arr_ext.
        use_pd_pyarrow_string_array):
        xzk__ixnec = lyb__ccz
        lyb__ccz = pyapi.call_method(lyb__ccz, 'to_numpy', ())
        pyapi.decref(xzk__ixnec)
    return lyb__ccz


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (xvfc__dhb, fwo__nof):
        with xvfc__dhb:
            pyapi.incref(obj)
            mrmkt__qdf = context.insert_const_string(c.builder.module, 'numpy')
            lxuzy__rtoto = pyapi.import_module_noblock(mrmkt__qdf)
            if df_typ.has_runtime_cols:
                bocc__ohfyc = 0
            else:
                bocc__ohfyc = len(df_typ.columns)
            nufz__rdou = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), bocc__ohfyc))
            oad__tbiz = pyapi.call_method(lxuzy__rtoto, 'arange', (nufz__rdou,)
                )
            pyapi.object_setattr_string(obj, 'columns', oad__tbiz)
            pyapi.decref(lxuzy__rtoto)
            pyapi.decref(oad__tbiz)
            pyapi.decref(nufz__rdou)
        with fwo__nof:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            rylwm__nwjlg = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            mrmkt__qdf = context.insert_const_string(c.builder.module, 'pandas'
                )
            lxuzy__rtoto = pyapi.import_module_noblock(mrmkt__qdf)
            df_obj = pyapi.call_method(lxuzy__rtoto, 'DataFrame', (pyapi.
                borrow_none(), rylwm__nwjlg))
            pyapi.decref(lxuzy__rtoto)
            pyapi.decref(rylwm__nwjlg)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    ruk__kdh = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = ruk__kdh.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        kpa__isrei = typ.table_type
        yscf__jtt = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, kpa__isrei, yscf__jtt)
        mvs__votl = box_table(kpa__isrei, yscf__jtt, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (mow__eyzkz, kkhn__lscwv):
            with mow__eyzkz:
                znbsl__tja = pyapi.object_getattr_string(mvs__votl, 'arrays')
                gxdal__krv = c.pyapi.make_none()
                if n_cols is None:
                    jva__dtgsv = pyapi.call_method(znbsl__tja, '__len__', ())
                    vhx__benhh = pyapi.long_as_longlong(jva__dtgsv)
                    pyapi.decref(jva__dtgsv)
                else:
                    vhx__benhh = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, vhx__benhh) as cejfl__lptht:
                    i = cejfl__lptht.index
                    vtb__yud = pyapi.list_getitem(znbsl__tja, i)
                    ryp__hiz = c.builder.icmp_unsigned('!=', vtb__yud,
                        gxdal__krv)
                    with builder.if_then(ryp__hiz):
                        sxpz__knx = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, sxpz__knx, vtb__yud)
                        pyapi.decref(sxpz__knx)
                pyapi.decref(znbsl__tja)
                pyapi.decref(gxdal__krv)
            with kkhn__lscwv:
                df_obj = builder.load(res)
                rylwm__nwjlg = pyapi.object_getattr_string(df_obj, 'index')
                bsrk__wwn = c.pyapi.call_method(mvs__votl, 'to_pandas', (
                    rylwm__nwjlg,))
                builder.store(bsrk__wwn, res)
                pyapi.decref(df_obj)
                pyapi.decref(rylwm__nwjlg)
        pyapi.decref(mvs__votl)
    else:
        icc__zbmhb = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        nhu__snm = typ.data
        for i, arr, hcrcj__sjfd in zip(range(n_cols), icc__zbmhb, nhu__snm):
            cjz__zqulj = cgutils.alloca_once_value(builder, arr)
            pwg__ezm = cgutils.alloca_once_value(builder, context.
                get_constant_null(hcrcj__sjfd))
            ryp__hiz = builder.not_(is_ll_eq(builder, cjz__zqulj, pwg__ezm))
            boq__oocip = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, ryp__hiz))
            with builder.if_then(boq__oocip):
                sxpz__knx = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, hcrcj__sjfd, arr)
                arr_obj = pyapi.from_native_value(hcrcj__sjfd, arr, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, sxpz__knx, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(sxpz__knx)
    df_obj = builder.load(res)
    lyb__ccz = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', lyb__ccz)
    pyapi.decref(lyb__ccz)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    gxdal__krv = pyapi.borrow_none()
    qwthp__itynt = pyapi.unserialize(pyapi.serialize_object(slice))
    hokn__iwsl = pyapi.call_function_objargs(qwthp__itynt, [gxdal__krv])
    ioti__omnl = pyapi.long_from_longlong(col_ind)
    mjhuj__kiqak = pyapi.tuple_pack([hokn__iwsl, ioti__omnl])
    dbqr__pqx = pyapi.object_getattr_string(df_obj, 'iloc')
    zyk__oujp = pyapi.object_getitem(dbqr__pqx, mjhuj__kiqak)
    zbi__stfd = pyapi.object_getattr_string(zyk__oujp, 'array')
    ahhg__sdhtl = pyapi.unserialize(pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = pyapi.call_function_objargs(ahhg__sdhtl, [zbi__stfd])
    pyapi.decref(zbi__stfd)
    pyapi.decref(ahhg__sdhtl)
    pyapi.decref(qwthp__itynt)
    pyapi.decref(hokn__iwsl)
    pyapi.decref(ioti__omnl)
    pyapi.decref(mjhuj__kiqak)
    pyapi.decref(dbqr__pqx)
    pyapi.decref(zyk__oujp)
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
        ruk__kdh = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            ruk__kdh.parent, args[1], data_typ)
        nfazz__uos = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            yscf__jtt = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            cqyfe__ovhid = df_typ.table_type.type_to_blk[data_typ]
            gts__deqv = getattr(yscf__jtt, f'block_{cqyfe__ovhid}')
            skhuv__gfxly = ListInstance(c.context, c.builder, types.List(
                data_typ), gts__deqv)
            myc__sggiz = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            skhuv__gfxly.inititem(myc__sggiz, nfazz__uos.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, nfazz__uos.value, col_ind)
        tbooa__ioxq = DataFramePayloadType(df_typ)
        pdikh__sbyw = context.nrt.meminfo_data(builder, ruk__kdh.meminfo)
        dpp__xhl = context.get_value_type(tbooa__ioxq).as_pointer()
        pdikh__sbyw = builder.bitcast(pdikh__sbyw, dpp__xhl)
        builder.store(dataframe_payload._getvalue(), pdikh__sbyw)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    zbi__stfd = c.pyapi.object_getattr_string(val, 'array')
    ahhg__sdhtl = c.pyapi.unserialize(c.pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = c.pyapi.call_function_objargs(ahhg__sdhtl, [zbi__stfd])
    nlbbc__lqby = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    rylwm__nwjlg = c.pyapi.object_getattr_string(val, 'index')
    mwmxp__niyhn = c.pyapi.to_native_value(typ.index, rylwm__nwjlg).value
    jvsz__cdt = c.pyapi.object_getattr_string(val, 'name')
    uhqf__njfxb = c.pyapi.to_native_value(typ.name_typ, jvsz__cdt).value
    ubwes__zli = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, nlbbc__lqby, mwmxp__niyhn, uhqf__njfxb)
    c.pyapi.decref(ahhg__sdhtl)
    c.pyapi.decref(zbi__stfd)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(rylwm__nwjlg)
    c.pyapi.decref(jvsz__cdt)
    return NativeValue(ubwes__zli)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        xugw__tgn = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(xugw__tgn._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    mrmkt__qdf = c.context.insert_const_string(c.builder.module, 'pandas')
    zuw__vtkg = c.pyapi.import_module_noblock(mrmkt__qdf)
    ybg__gnjc = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c
        .builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, ybg__gnjc.data)
    c.context.nrt.incref(c.builder, typ.index, ybg__gnjc.index)
    c.context.nrt.incref(c.builder, typ.name_typ, ybg__gnjc.name)
    arr_obj = c.pyapi.from_native_value(typ.data, ybg__gnjc.data, c.env_manager
        )
    rylwm__nwjlg = c.pyapi.from_native_value(typ.index, ybg__gnjc.index, c.
        env_manager)
    jvsz__cdt = c.pyapi.from_native_value(typ.name_typ, ybg__gnjc.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(zuw__vtkg, 'Series', (arr_obj, rylwm__nwjlg,
        dtype, jvsz__cdt))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(rylwm__nwjlg)
    c.pyapi.decref(jvsz__cdt)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(zuw__vtkg)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    hod__tkzna = []
    for lzu__ryk in typ_list:
        if isinstance(lzu__ryk, int) and not isinstance(lzu__ryk, bool):
            qkxi__ohah = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), lzu__ryk))
        else:
            hqd__vbau = numba.typeof(lzu__ryk)
            egkmt__wolcr = context.get_constant_generic(builder, hqd__vbau,
                lzu__ryk)
            qkxi__ohah = pyapi.from_native_value(hqd__vbau, egkmt__wolcr,
                env_manager)
        hod__tkzna.append(qkxi__ohah)
    nmbb__ttey = pyapi.list_pack(hod__tkzna)
    for val in hod__tkzna:
        pyapi.decref(val)
    return nmbb__ttey


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    uwc__xgtn = not typ.has_runtime_cols
    pcdc__elm = 2 if uwc__xgtn else 1
    gxa__kbnn = pyapi.dict_new(pcdc__elm)
    dhgbr__tkt = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    pyapi.dict_setitem_string(gxa__kbnn, 'dist', dhgbr__tkt)
    pyapi.decref(dhgbr__tkt)
    if uwc__xgtn:
        gabd__irrzg = _dtype_to_type_enum_list(typ.index)
        if gabd__irrzg != None:
            qah__vgtu = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, gabd__irrzg)
        else:
            qah__vgtu = pyapi.make_none()
        if typ.is_table_format:
            ujsxf__oic = typ.table_type
            ckr__vzkj = pyapi.list_new(lir.Constant(lir.IntType(64), len(
                typ.data)))
            for cqyfe__ovhid, dtype in ujsxf__oic.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                vhx__benhh = c.context.get_constant(types.int64, len(
                    ujsxf__oic.block_to_arr_ind[cqyfe__ovhid]))
                afx__ybd = c.context.make_constant_array(c.builder, types.
                    Array(types.int64, 1, 'C'), np.array(ujsxf__oic.
                    block_to_arr_ind[cqyfe__ovhid], dtype=np.int64))
                ynj__oyso = c.context.make_array(types.Array(types.int64, 1,
                    'C'))(c.context, c.builder, afx__ybd)
                with cgutils.for_range(c.builder, vhx__benhh) as cejfl__lptht:
                    i = cejfl__lptht.index
                    itxj__oxpd = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), ynj__oyso, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(ckr__vzkj, itxj__oxpd, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            cww__gqzs = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    nmbb__ttey = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    nmbb__ttey = pyapi.make_none()
                cww__gqzs.append(nmbb__ttey)
            ckr__vzkj = pyapi.list_pack(cww__gqzs)
            for val in cww__gqzs:
                pyapi.decref(val)
        lggwh__xhe = pyapi.list_pack([qah__vgtu, ckr__vzkj])
        pyapi.dict_setitem_string(gxa__kbnn, 'type_metadata', lggwh__xhe)
    pyapi.object_setattr_string(obj, '_bodo_meta', gxa__kbnn)
    pyapi.decref(gxa__kbnn)


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
    gxa__kbnn = pyapi.dict_new(2)
    dhgbr__tkt = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    gabd__irrzg = _dtype_to_type_enum_list(typ.index)
    if gabd__irrzg != None:
        qah__vgtu = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, gabd__irrzg)
    else:
        qah__vgtu = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            cgpih__iaize = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            cgpih__iaize = pyapi.make_none()
    else:
        cgpih__iaize = pyapi.make_none()
    ufm__auqj = pyapi.list_pack([qah__vgtu, cgpih__iaize])
    pyapi.dict_setitem_string(gxa__kbnn, 'type_metadata', ufm__auqj)
    pyapi.decref(ufm__auqj)
    pyapi.dict_setitem_string(gxa__kbnn, 'dist', dhgbr__tkt)
    pyapi.object_setattr_string(obj, '_bodo_meta', gxa__kbnn)
    pyapi.decref(gxa__kbnn)
    pyapi.decref(dhgbr__tkt)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as uim__ttz:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    nxew__dionv = numba.np.numpy_support.map_layout(val)
    apb__mtfp = not val.flags.writeable
    return types.Array(dtype, val.ndim, nxew__dionv, readonly=apb__mtfp)


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
    ota__byta = val[i]
    dogh__pca = 100
    if isinstance(ota__byta, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(ota__byta, (bytes, bytearray)):
        return binary_array_type
    elif isinstance(ota__byta, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(ota__byta, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(ota__byta))
    elif isinstance(ota__byta, (float, np.float32, np.float64)):
        return bodo.libs.float_arr_ext.FloatingArrayType(numba.typeof(
            ota__byta))
    elif isinstance(ota__byta, (dict, Dict)) and len(ota__byta.keys()
        ) <= dogh__pca and all(isinstance(dfg__ptflb, str) for dfg__ptflb in
        ota__byta.keys()):
        upnv__cwx = tuple(ota__byta.keys())
        ycm__gtc = tuple(_get_struct_value_arr_type(v) for v in ota__byta.
            values())
        return StructArrayType(ycm__gtc, upnv__cwx)
    elif isinstance(ota__byta, (dict, Dict)):
        auqs__dohwg = numba.typeof(_value_to_array(list(ota__byta.keys())))
        dftbj__idb = numba.typeof(_value_to_array(list(ota__byta.values())))
        auqs__dohwg = to_str_arr_if_dict_array(auqs__dohwg)
        dftbj__idb = to_str_arr_if_dict_array(dftbj__idb)
        return MapArrayType(auqs__dohwg, dftbj__idb)
    elif isinstance(ota__byta, tuple):
        ycm__gtc = tuple(_get_struct_value_arr_type(v) for v in ota__byta)
        return TupleArrayType(ycm__gtc)
    if isinstance(ota__byta, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.FloatingArray, pd.arrays.StringArray,
        pd.arrays.ArrowStringArray)):
        if isinstance(ota__byta, list):
            ota__byta = _value_to_array(ota__byta)
        kbox__daen = numba.typeof(ota__byta)
        kbox__daen = to_str_arr_if_dict_array(kbox__daen)
        return ArrayItemArrayType(kbox__daen)
    if isinstance(ota__byta, datetime.date):
        return datetime_date_array_type
    if isinstance(ota__byta, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(ota__byta, bodo.Time):
        return TimeArrayType(ota__byta.precision)
    if isinstance(ota__byta, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(ota__byta, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(f'Unsupported object array with first value: {ota__byta}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    lfftv__rvio = val.copy()
    lfftv__rvio.append(None)
    arr = np.array(lfftv__rvio, np.object_)
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
    hcrcj__sjfd = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        hcrcj__sjfd = to_nullable_type(hcrcj__sjfd)
    return hcrcj__sjfd
