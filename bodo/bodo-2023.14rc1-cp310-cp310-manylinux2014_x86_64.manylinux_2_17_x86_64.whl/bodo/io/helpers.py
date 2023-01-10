"""
File that contains some IO related helpers.
"""
import os
import threading
import uuid
import numba
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, models, register_model, typeof_impl, unbox
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.typing import BodoError, raise_bodo_error


class PyArrowTableSchemaType(types.Opaque):

    def __init__(self):
        super(PyArrowTableSchemaType, self).__init__(name=
            'PyArrowTableSchemaType')


pyarrow_table_schema_type = PyArrowTableSchemaType()
types.pyarrow_table_schema_type = pyarrow_table_schema_type
register_model(PyArrowTableSchemaType)(models.OpaqueModel)


@unbox(PyArrowTableSchemaType)
def unbox_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(PyArrowTableSchemaType)
def box_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(pa.lib.Schema)
def typeof_pyarrow_table_schema(val, c):
    return pyarrow_table_schema_type


@lower_constant(PyArrowTableSchemaType)
def lower_pyarrow_table_schema(context, builder, ty, pyval):
    wfios__ipxh = context.get_python_api(builder)
    return wfios__ipxh.unserialize(wfios__ipxh.serialize_object(pyval))


def is_nullable(typ):
    return bodo.utils.utils.is_array_typ(typ, False) and (not isinstance(
        typ, types.Array) and not isinstance(typ, bodo.DatetimeArrayType))


def pa_schema_unify_reduction(schema_a, schema_b, unused):
    return pa.unify_schemas([schema_a, schema_b])


pa_schema_unify_mpi_op = MPI.Op.Create(pa_schema_unify_reduction, commute=True)
use_nullable_pd_arr = True
_pyarrow_numba_type_map = {pa.bool_(): types.bool_, pa.int8(): types.int8,
    pa.int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.
    int64, pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32():
    types.uint32, pa.uint64(): types.uint64, pa.float32(): types.float32,
    pa.float64(): types.float64, pa.string(): string_type, pa.large_string(
    ): string_type, pa.binary(): bytes_type, pa.date32():
    datetime_date_type, pa.date64(): types.NPDatetime('ns'), pa.time32('s'):
    TimeType(0), pa.time32('ms'): TimeType(3), pa.time64('us'): TimeType(6),
    pa.time64('ns'): TimeType(9), pa.null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    nhg__kdnlv = ['ns', 'us', 'ms', 's']
    if pa_ts_typ.unit not in nhg__kdnlv:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        egi__qkrh = pa_ts_typ.to_pandas_dtype().tz
        taewy__fsbao = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            egi__qkrh)
        return bodo.DatetimeArrayType(taewy__fsbao), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        dfqk__wwco, cfzog__zym = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(dfqk__wwco), cfzog__zym
    if isinstance(pa_typ.type, pa.StructType):
        yzby__iyt = []
        lue__fre = []
        cfzog__zym = True
        for dtk__wzrnc in pa_typ.flatten():
            lue__fre.append(dtk__wzrnc.name.split('.')[-1])
            qqom__vzhiv, mjazs__bgkym = _get_numba_typ_from_pa_typ(dtk__wzrnc,
                is_index, nullable_from_metadata, category_info)
            yzby__iyt.append(qqom__vzhiv)
            cfzog__zym = cfzog__zym and mjazs__bgkym
        return StructArrayType(tuple(yzby__iyt), tuple(lue__fre)), cfzog__zym
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale), True
    if str_as_dict:
        if pa_typ.type != pa.string():
            raise BodoError(
                f'Read as dictionary used for non-string column {pa_typ}')
        return dict_str_arr_type, True
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        dnyuj__ixtl = _pyarrow_numba_type_map[pa_typ.type.index_type]
        tzhtv__ufvxu = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=dnyuj__ixtl)
        return CategoricalArrayType(tzhtv__ufvxu), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        itoj__ugff = _pyarrow_numba_type_map[pa_typ.type]
        cfzog__zym = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if itoj__ugff == datetime_date_type:
        return datetime_date_array_type, cfzog__zym
    if isinstance(itoj__ugff, TimeType):
        return TimeArrayType(itoj__ugff.precision), cfzog__zym
    if itoj__ugff == bytes_type:
        return binary_array_type, cfzog__zym
    dfqk__wwco = (string_array_type if itoj__ugff == string_type else types
        .Array(itoj__ugff, 1, 'C'))
    if itoj__ugff == types.bool_:
        dfqk__wwco = boolean_array
    bky__tyuim = (use_nullable_pd_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if bky__tyuim and not is_index and isinstance(itoj__ugff, types.Integer
        ) and pa_typ.nullable:
        dfqk__wwco = IntegerArrayType(itoj__ugff)
    if (bky__tyuim and bodo.libs.float_arr_ext._use_nullable_float and not
        is_index and isinstance(itoj__ugff, types.Float) and pa_typ.nullable):
        dfqk__wwco = FloatingArrayType(itoj__ugff)
    return dfqk__wwco, cfzog__zym


_numba_pyarrow_type_map = {types.bool_: pa.bool_(), types.int8: pa.int8(),
    types.int16: pa.int16(), types.int32: pa.int32(), types.int64: pa.int64
    (), types.uint8: pa.uint8(), types.uint16: pa.uint16(), types.uint32:
    pa.uint32(), types.uint64: pa.uint64(), types.float32: pa.float32(),
    types.float64: pa.float64(), types.NPDatetime('ns'): pa.date64()}


def is_nullable_arrow_out(numba_type: types.ArrayCompatible) ->bool:
    return is_nullable(numba_type) or isinstance(numba_type, bodo.
        DatetimeArrayType) or isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.datetime64ns


def _numba_to_pyarrow_type(numba_type: types.ArrayCompatible, is_iceberg:
    bool=False):
    if isinstance(numba_type, ArrayItemArrayType):
        wnqlz__phoi = pa.field('element', _numba_to_pyarrow_type(numba_type
            .dtype, is_iceberg)[0])
        itoj__ugff = pa.list_(wnqlz__phoi)
    elif isinstance(numba_type, StructArrayType):
        dzc__wxm = []
        for xnxf__twsi, mdtnb__pdk in zip(numba_type.names, numba_type.data):
            lzmj__syn, fvtu__uftt = _numba_to_pyarrow_type(mdtnb__pdk,
                is_iceberg)
            dzc__wxm.append(pa.field(xnxf__twsi, lzmj__syn, True))
        itoj__ugff = pa.struct(dzc__wxm)
    elif isinstance(numba_type, DecimalArrayType):
        itoj__ugff = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        tzhtv__ufvxu: PDCategoricalDtype = numba_type.dtype
        itoj__ugff = pa.dictionary(_numba_to_pyarrow_type(tzhtv__ufvxu.
            int_type, is_iceberg)[0], _numba_to_pyarrow_type(tzhtv__ufvxu.
            elem_type, is_iceberg)[0], ordered=False if tzhtv__ufvxu.
            ordered is None else tzhtv__ufvxu.ordered)
    elif numba_type == boolean_array:
        itoj__ugff = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        itoj__ugff = pa.string()
    elif numba_type == binary_array_type:
        itoj__ugff = pa.binary()
    elif numba_type == datetime_date_array_type:
        itoj__ugff = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType) or isinstance(
        numba_type, types.Array) and numba_type.dtype == bodo.datetime64ns:
        itoj__ugff = pa.timestamp('us', 'UTC') if is_iceberg else pa.timestamp(
            'ns', 'UTC')
    elif isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.timedelta64ns:
        itoj__ugff = pa.duration('ns')
    elif isinstance(numba_type, (types.Array, IntegerArrayType,
        FloatingArrayType)) and numba_type.dtype in _numba_pyarrow_type_map:
        itoj__ugff = _numba_pyarrow_type_map[numba_type.dtype]
    elif isinstance(numba_type, bodo.TimeArrayType):
        if numba_type.precision == 0:
            itoj__ugff = pa.time32('s')
        elif numba_type.precision == 3:
            itoj__ugff = pa.time32('ms')
        elif numba_type.precision == 6:
            itoj__ugff = pa.time64('us')
        elif numba_type.precision == 9:
            itoj__ugff = pa.time64('ns')
    else:
        raise BodoError(
            f'Conversion from Bodo array type {numba_type} to PyArrow type not supported yet'
            )
    return itoj__ugff, is_nullable_arrow_out(numba_type)


def numba_to_pyarrow_schema(df: DataFrameType, is_iceberg: bool=False
    ) ->pa.Schema:
    dzc__wxm = []
    for xnxf__twsi, fasc__jpcju in zip(df.columns, df.data):
        try:
            msxef__vhm, kxffe__cfq = _numba_to_pyarrow_type(fasc__jpcju,
                is_iceberg)
        except BodoError as zppyh__gmh:
            raise_bodo_error(zppyh__gmh.msg, zppyh__gmh.loc)
        dzc__wxm.append(pa.field(xnxf__twsi, msxef__vhm, kxffe__cfq))
    return pa.schema(dzc__wxm)


def update_env_vars(env_vars):
    qczh__pwb = {}
    for tlkl__tnh, jqb__sfjo in env_vars.items():
        if tlkl__tnh in os.environ:
            qczh__pwb[tlkl__tnh] = os.environ[tlkl__tnh]
        else:
            qczh__pwb[tlkl__tnh] = '__none__'
        if jqb__sfjo == '__none__':
            del os.environ[tlkl__tnh]
        else:
            os.environ[tlkl__tnh] = jqb__sfjo
    return qczh__pwb


def update_file_contents(fname: str, contents: str, is_parallel=True) ->str:
    zaj__oqi = MPI.COMM_WORLD
    oiqn__mabbs = None
    if not is_parallel or zaj__oqi.Get_rank() == 0:
        if os.path.exists(fname):
            with open(fname, 'r') as werjq__nhemu:
                oiqn__mabbs = werjq__nhemu.read()
    if is_parallel:
        oiqn__mabbs = zaj__oqi.bcast(oiqn__mabbs)
    if oiqn__mabbs is None:
        oiqn__mabbs = '__none__'
    hxnz__wpgqt = bodo.get_rank() in bodo.get_nodes_first_ranks(
        ) if is_parallel else True
    if contents == '__none__':
        if hxnz__wpgqt and os.path.exists(fname):
            os.remove(fname)
    elif hxnz__wpgqt:
        with open(fname, 'w') as werjq__nhemu:
            werjq__nhemu.write(contents)
    if is_parallel:
        zaj__oqi.Barrier()
    return oiqn__mabbs


@numba.njit
def uuid4_helper():
    with numba.objmode(out='unicode_type'):
        out = str(uuid.uuid4())
    return out


class ExceptionPropagatingThread(threading.Thread):

    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as zppyh__gmh:
            self.exc = zppyh__gmh

    def join(self, timeout=None):
        super().join(timeout)
        if self.exc:
            raise self.exc
        return self.ret


class ExceptionPropagatingThreadType(types.Opaque):

    def __init__(self):
        super(ExceptionPropagatingThreadType, self).__init__(name=
            'ExceptionPropagatingThreadType')


exception_propagating_thread_type = ExceptionPropagatingThreadType()
types.exception_propagating_thread_type = exception_propagating_thread_type
register_model(ExceptionPropagatingThreadType)(models.OpaqueModel)


@unbox(ExceptionPropagatingThreadType)
def unbox_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ExceptionPropagatingThreadType)
def box_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(ExceptionPropagatingThread)
def typeof_exception_propagating_thread(val, c):
    return exception_propagating_thread_type


def join_all_threads(thread_list):
    mtq__vzd = tracing.Event('join_all_threads', is_parallel=True)
    zaj__oqi = MPI.COMM_WORLD
    gygh__illst = None
    try:
        for vzpza__iwig in thread_list:
            if isinstance(vzpza__iwig, threading.Thread):
                vzpza__iwig.join()
    except Exception as zppyh__gmh:
        gygh__illst = zppyh__gmh
    movf__pezde = int(gygh__illst is not None)
    vasv__deise, oevyv__nljk = zaj__oqi.allreduce((movf__pezde, zaj__oqi.
        Get_rank()), op=MPI.MAXLOC)
    if vasv__deise:
        if zaj__oqi.Get_rank() == oevyv__nljk:
            ptvra__lzf = gygh__illst
        else:
            ptvra__lzf = None
        ptvra__lzf = zaj__oqi.bcast(ptvra__lzf, root=oevyv__nljk)
        if movf__pezde:
            raise gygh__illst
        else:
            raise ptvra__lzf
    mtq__vzd.finalize()
