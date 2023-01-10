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
    qiv__igce = context.get_python_api(builder)
    return qiv__igce.unserialize(qiv__igce.serialize_object(pyval))


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
    mqwz__yxa = ['ns', 'us', 'ms', 's']
    if pa_ts_typ.unit not in mqwz__yxa:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        vtryt__vng = pa_ts_typ.to_pandas_dtype().tz
        ayjbt__zwfkx = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            vtryt__vng)
        return bodo.DatetimeArrayType(ayjbt__zwfkx), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        cpot__xnvic, udljm__ujedc = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(cpot__xnvic), udljm__ujedc
    if isinstance(pa_typ.type, pa.StructType):
        dxra__bzlfo = []
        chxpj__hljuf = []
        udljm__ujedc = True
        for tkagw__fdis in pa_typ.flatten():
            chxpj__hljuf.append(tkagw__fdis.name.split('.')[-1])
            vmvhz__gha, qgjbo__hwz = _get_numba_typ_from_pa_typ(tkagw__fdis,
                is_index, nullable_from_metadata, category_info)
            dxra__bzlfo.append(vmvhz__gha)
            udljm__ujedc = udljm__ujedc and qgjbo__hwz
        return StructArrayType(tuple(dxra__bzlfo), tuple(chxpj__hljuf)
            ), udljm__ujedc
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
        uqchp__mqyy = _pyarrow_numba_type_map[pa_typ.type.index_type]
        ltvdj__nhr = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=uqchp__mqyy)
        return CategoricalArrayType(ltvdj__nhr), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        uysrd__yqrc = _pyarrow_numba_type_map[pa_typ.type]
        udljm__ujedc = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if uysrd__yqrc == datetime_date_type:
        return datetime_date_array_type, udljm__ujedc
    if isinstance(uysrd__yqrc, TimeType):
        return TimeArrayType(uysrd__yqrc.precision), udljm__ujedc
    if uysrd__yqrc == bytes_type:
        return binary_array_type, udljm__ujedc
    cpot__xnvic = (string_array_type if uysrd__yqrc == string_type else
        types.Array(uysrd__yqrc, 1, 'C'))
    if uysrd__yqrc == types.bool_:
        cpot__xnvic = boolean_array
    toau__gop = (use_nullable_pd_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if toau__gop and not is_index and isinstance(uysrd__yqrc, types.Integer
        ) and pa_typ.nullable:
        cpot__xnvic = IntegerArrayType(uysrd__yqrc)
    if (toau__gop and bodo.libs.float_arr_ext._use_nullable_float and not
        is_index and isinstance(uysrd__yqrc, types.Float) and pa_typ.nullable):
        cpot__xnvic = FloatingArrayType(uysrd__yqrc)
    return cpot__xnvic, udljm__ujedc


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
        ovgrr__nev = pa.field('element', _numba_to_pyarrow_type(numba_type.
            dtype, is_iceberg)[0])
        uysrd__yqrc = pa.list_(ovgrr__nev)
    elif isinstance(numba_type, StructArrayType):
        ett__zau = []
        for gqx__rhm, jgbf__sxl in zip(numba_type.names, numba_type.data):
            lxnau__mzpcl, ktv__leg = _numba_to_pyarrow_type(jgbf__sxl,
                is_iceberg)
            ett__zau.append(pa.field(gqx__rhm, lxnau__mzpcl, True))
        uysrd__yqrc = pa.struct(ett__zau)
    elif isinstance(numba_type, DecimalArrayType):
        uysrd__yqrc = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        ltvdj__nhr: PDCategoricalDtype = numba_type.dtype
        uysrd__yqrc = pa.dictionary(_numba_to_pyarrow_type(ltvdj__nhr.
            int_type, is_iceberg)[0], _numba_to_pyarrow_type(ltvdj__nhr.
            elem_type, is_iceberg)[0], ordered=False if ltvdj__nhr.ordered is
            None else ltvdj__nhr.ordered)
    elif numba_type == boolean_array:
        uysrd__yqrc = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        uysrd__yqrc = pa.string()
    elif numba_type == binary_array_type:
        uysrd__yqrc = pa.binary()
    elif numba_type == datetime_date_array_type:
        uysrd__yqrc = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType) or isinstance(
        numba_type, types.Array) and numba_type.dtype == bodo.datetime64ns:
        uysrd__yqrc = pa.timestamp('us', 'UTC'
            ) if is_iceberg else pa.timestamp('ns', 'UTC')
    elif isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.timedelta64ns:
        uysrd__yqrc = pa.duration('ns')
    elif isinstance(numba_type, (types.Array, IntegerArrayType,
        FloatingArrayType)) and numba_type.dtype in _numba_pyarrow_type_map:
        uysrd__yqrc = _numba_pyarrow_type_map[numba_type.dtype]
    elif isinstance(numba_type, bodo.TimeArrayType):
        if numba_type.precision == 0:
            uysrd__yqrc = pa.time32('s')
        elif numba_type.precision == 3:
            uysrd__yqrc = pa.time32('ms')
        elif numba_type.precision == 6:
            uysrd__yqrc = pa.time64('us')
        elif numba_type.precision == 9:
            uysrd__yqrc = pa.time64('ns')
    else:
        raise BodoError(
            f'Conversion from Bodo array type {numba_type} to PyArrow type not supported yet'
            )
    return uysrd__yqrc, is_nullable_arrow_out(numba_type)


def numba_to_pyarrow_schema(df: DataFrameType, is_iceberg: bool=False
    ) ->pa.Schema:
    ett__zau = []
    for gqx__rhm, shshj__fksj in zip(df.columns, df.data):
        try:
            wpoi__klvrd, vyas__znf = _numba_to_pyarrow_type(shshj__fksj,
                is_iceberg)
        except BodoError as aog__kaqdc:
            raise_bodo_error(aog__kaqdc.msg, aog__kaqdc.loc)
        ett__zau.append(pa.field(gqx__rhm, wpoi__klvrd, vyas__znf))
    return pa.schema(ett__zau)


def update_env_vars(env_vars):
    ikyj__llel = {}
    for mshk__wdc, hpvxv__jrbv in env_vars.items():
        if mshk__wdc in os.environ:
            ikyj__llel[mshk__wdc] = os.environ[mshk__wdc]
        else:
            ikyj__llel[mshk__wdc] = '__none__'
        if hpvxv__jrbv == '__none__':
            del os.environ[mshk__wdc]
        else:
            os.environ[mshk__wdc] = hpvxv__jrbv
    return ikyj__llel


def update_file_contents(fname: str, contents: str, is_parallel=True) ->str:
    mctw__gvhj = MPI.COMM_WORLD
    uwi__dwd = None
    if not is_parallel or mctw__gvhj.Get_rank() == 0:
        if os.path.exists(fname):
            with open(fname, 'r') as cozt__izwn:
                uwi__dwd = cozt__izwn.read()
    if is_parallel:
        uwi__dwd = mctw__gvhj.bcast(uwi__dwd)
    if uwi__dwd is None:
        uwi__dwd = '__none__'
    edu__fij = bodo.get_rank() in bodo.get_nodes_first_ranks(
        ) if is_parallel else True
    if contents == '__none__':
        if edu__fij and os.path.exists(fname):
            os.remove(fname)
    elif edu__fij:
        with open(fname, 'w') as cozt__izwn:
            cozt__izwn.write(contents)
    if is_parallel:
        mctw__gvhj.Barrier()
    return uwi__dwd


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
        except BaseException as aog__kaqdc:
            self.exc = aog__kaqdc

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
    rzuv__bgqo = tracing.Event('join_all_threads', is_parallel=True)
    mctw__gvhj = MPI.COMM_WORLD
    tgw__kvi = None
    try:
        for qhg__nonn in thread_list:
            if isinstance(qhg__nonn, threading.Thread):
                qhg__nonn.join()
    except Exception as aog__kaqdc:
        tgw__kvi = aog__kaqdc
    fwjo__nhcrj = int(tgw__kvi is not None)
    zkvd__huohi, qbr__wify = mctw__gvhj.allreduce((fwjo__nhcrj, mctw__gvhj.
        Get_rank()), op=MPI.MAXLOC)
    if zkvd__huohi:
        if mctw__gvhj.Get_rank() == qbr__wify:
            ykcyf__nlog = tgw__kvi
        else:
            ykcyf__nlog = None
        ykcyf__nlog = mctw__gvhj.bcast(ykcyf__nlog, root=qbr__wify)
        if fwjo__nhcrj:
            raise tgw__kvi
        else:
            raise ykcyf__nlog
    rzuv__bgqo.finalize()
