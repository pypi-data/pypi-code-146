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
    asvsp__uea = context.get_python_api(builder)
    return asvsp__uea.unserialize(asvsp__uea.serialize_object(pyval))


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
    yrhzj__fetv = ['ns', 'us', 'ms', 's']
    if pa_ts_typ.unit not in yrhzj__fetv:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        pov__urfc = pa_ts_typ.to_pandas_dtype().tz
        ibakq__lwqsu = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            pov__urfc)
        return bodo.DatetimeArrayType(ibakq__lwqsu), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        metb__uvrx, ijh__nniw = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(metb__uvrx), ijh__nniw
    if isinstance(pa_typ.type, pa.StructType):
        nmz__kfqc = []
        gjd__wzt = []
        ijh__nniw = True
        for hmsxp__tfpgm in pa_typ.flatten():
            gjd__wzt.append(hmsxp__tfpgm.name.split('.')[-1])
            ile__oyddn, focb__yult = _get_numba_typ_from_pa_typ(hmsxp__tfpgm,
                is_index, nullable_from_metadata, category_info)
            nmz__kfqc.append(ile__oyddn)
            ijh__nniw = ijh__nniw and focb__yult
        return StructArrayType(tuple(nmz__kfqc), tuple(gjd__wzt)), ijh__nniw
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
        rms__owolk = _pyarrow_numba_type_map[pa_typ.type.index_type]
        ishag__imdvy = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=rms__owolk)
        return CategoricalArrayType(ishag__imdvy), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        yxf__xts = _pyarrow_numba_type_map[pa_typ.type]
        ijh__nniw = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if yxf__xts == datetime_date_type:
        return datetime_date_array_type, ijh__nniw
    if isinstance(yxf__xts, TimeType):
        return TimeArrayType(yxf__xts.precision), ijh__nniw
    if yxf__xts == bytes_type:
        return binary_array_type, ijh__nniw
    metb__uvrx = string_array_type if yxf__xts == string_type else types.Array(
        yxf__xts, 1, 'C')
    if yxf__xts == types.bool_:
        metb__uvrx = boolean_array
    ldbj__cpmfa = (use_nullable_pd_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if ldbj__cpmfa and not is_index and isinstance(yxf__xts, types.Integer
        ) and pa_typ.nullable:
        metb__uvrx = IntegerArrayType(yxf__xts)
    if (ldbj__cpmfa and bodo.libs.float_arr_ext._use_nullable_float and not
        is_index and isinstance(yxf__xts, types.Float) and pa_typ.nullable):
        metb__uvrx = FloatingArrayType(yxf__xts)
    return metb__uvrx, ijh__nniw


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
        pscgp__innh = pa.field('element', _numba_to_pyarrow_type(numba_type
            .dtype, is_iceberg)[0])
        yxf__xts = pa.list_(pscgp__innh)
    elif isinstance(numba_type, StructArrayType):
        jzhf__hrq = []
        for joim__wgj, cfe__dhxoe in zip(numba_type.names, numba_type.data):
            wbg__jsm, bti__vxwgm = _numba_to_pyarrow_type(cfe__dhxoe,
                is_iceberg)
            jzhf__hrq.append(pa.field(joim__wgj, wbg__jsm, True))
        yxf__xts = pa.struct(jzhf__hrq)
    elif isinstance(numba_type, DecimalArrayType):
        yxf__xts = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        ishag__imdvy: PDCategoricalDtype = numba_type.dtype
        yxf__xts = pa.dictionary(_numba_to_pyarrow_type(ishag__imdvy.
            int_type, is_iceberg)[0], _numba_to_pyarrow_type(ishag__imdvy.
            elem_type, is_iceberg)[0], ordered=False if ishag__imdvy.
            ordered is None else ishag__imdvy.ordered)
    elif numba_type == boolean_array:
        yxf__xts = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        yxf__xts = pa.string()
    elif numba_type == binary_array_type:
        yxf__xts = pa.binary()
    elif numba_type == datetime_date_array_type:
        yxf__xts = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType) or isinstance(
        numba_type, types.Array) and numba_type.dtype == bodo.datetime64ns:
        yxf__xts = pa.timestamp('us', 'UTC') if is_iceberg else pa.timestamp(
            'ns', 'UTC')
    elif isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.timedelta64ns:
        yxf__xts = pa.duration('ns')
    elif isinstance(numba_type, (types.Array, IntegerArrayType,
        FloatingArrayType)) and numba_type.dtype in _numba_pyarrow_type_map:
        yxf__xts = _numba_pyarrow_type_map[numba_type.dtype]
    elif isinstance(numba_type, bodo.TimeArrayType):
        if numba_type.precision == 0:
            yxf__xts = pa.time32('s')
        elif numba_type.precision == 3:
            yxf__xts = pa.time32('ms')
        elif numba_type.precision == 6:
            yxf__xts = pa.time64('us')
        elif numba_type.precision == 9:
            yxf__xts = pa.time64('ns')
    else:
        raise BodoError(
            f'Conversion from Bodo array type {numba_type} to PyArrow type not supported yet'
            )
    return yxf__xts, is_nullable_arrow_out(numba_type)


def numba_to_pyarrow_schema(df: DataFrameType, is_iceberg: bool=False
    ) ->pa.Schema:
    jzhf__hrq = []
    for joim__wgj, lqm__lcih in zip(df.columns, df.data):
        try:
            otrbl__lredd, bgr__suwea = _numba_to_pyarrow_type(lqm__lcih,
                is_iceberg)
        except BodoError as ewu__dhno:
            raise_bodo_error(ewu__dhno.msg, ewu__dhno.loc)
        jzhf__hrq.append(pa.field(joim__wgj, otrbl__lredd, bgr__suwea))
    return pa.schema(jzhf__hrq)


def update_env_vars(env_vars):
    jpoo__sulam = {}
    for wnvap__jhy, gma__uzl in env_vars.items():
        if wnvap__jhy in os.environ:
            jpoo__sulam[wnvap__jhy] = os.environ[wnvap__jhy]
        else:
            jpoo__sulam[wnvap__jhy] = '__none__'
        if gma__uzl == '__none__':
            del os.environ[wnvap__jhy]
        else:
            os.environ[wnvap__jhy] = gma__uzl
    return jpoo__sulam


def update_file_contents(fname: str, contents: str, is_parallel=True) ->str:
    vwyp__excj = MPI.COMM_WORLD
    sqgda__nuv = None
    if not is_parallel or vwyp__excj.Get_rank() == 0:
        if os.path.exists(fname):
            with open(fname, 'r') as tbzq__oohfl:
                sqgda__nuv = tbzq__oohfl.read()
    if is_parallel:
        sqgda__nuv = vwyp__excj.bcast(sqgda__nuv)
    if sqgda__nuv is None:
        sqgda__nuv = '__none__'
    fbl__xsigo = bodo.get_rank() in bodo.get_nodes_first_ranks(
        ) if is_parallel else True
    if contents == '__none__':
        if fbl__xsigo and os.path.exists(fname):
            os.remove(fname)
    elif fbl__xsigo:
        with open(fname, 'w') as tbzq__oohfl:
            tbzq__oohfl.write(contents)
    if is_parallel:
        vwyp__excj.Barrier()
    return sqgda__nuv


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
        except BaseException as ewu__dhno:
            self.exc = ewu__dhno

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
    idqk__dwtn = tracing.Event('join_all_threads', is_parallel=True)
    vwyp__excj = MPI.COMM_WORLD
    ehbi__dbp = None
    try:
        for datr__jkvts in thread_list:
            if isinstance(datr__jkvts, threading.Thread):
                datr__jkvts.join()
    except Exception as ewu__dhno:
        ehbi__dbp = ewu__dhno
    haoi__teq = int(ehbi__dbp is not None)
    pkcgk__livz, sucb__pch = vwyp__excj.allreduce((haoi__teq, vwyp__excj.
        Get_rank()), op=MPI.MAXLOC)
    if pkcgk__livz:
        if vwyp__excj.Get_rank() == sucb__pch:
            dqwy__xyc = ehbi__dbp
        else:
            dqwy__xyc = None
        dqwy__xyc = vwyp__excj.bcast(dqwy__xyc, root=sucb__pch)
        if haoi__teq:
            raise ehbi__dbp
        else:
            raise dqwy__xyc
    idqk__dwtn.finalize()
