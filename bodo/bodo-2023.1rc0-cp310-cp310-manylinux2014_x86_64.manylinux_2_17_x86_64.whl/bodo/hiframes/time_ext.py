"""Numba extension support for time objects and their arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
_nanos_per_micro = 1000
_nanos_per_milli = 1000 * _nanos_per_micro
_nanos_per_second = 1000 * _nanos_per_milli
_nanos_per_minute = 60 * _nanos_per_second
_nanos_per_hour = 60 * _nanos_per_minute


class Time:

    def __init__(self, hour=0, minute=0, second=0, millisecond=0,
        microsecond=0, nanosecond=0, precision=9):
        self.precision = precision
        assert all(np.issubdtype(type(val), np.integer) or pd.api.types.
            is_int64_dtype(val) for val in (hour, minute, second,
            millisecond, microsecond, nanosecond)
            ), 'All time components must be integers'
        self.value = np.int64(hour * _nanos_per_hour + minute *
            _nanos_per_minute + second * _nanos_per_second + millisecond *
            _nanos_per_milli + microsecond * _nanos_per_micro + nanosecond)

    def __repr__(self):
        return (
            f'Time(hour={self.hour}, minute={self.minute}, second={self.second}, millisecond={self.millisecond}, microsecond={self.microsecond}, nanosecond={self.nanosecond}, precision={self.precision})'
            )

    def __str__(self):
        return (
            f'{self.hour}:{self.minute}:{self.second}.{self.microsecond}{self.nanosecond}'
            )

    def __eq__(self, other):
        if not isinstance(other, Time):
            return False
        return self.value == other.value and self.precision == other.precision

    def _check_can_compare(self, other):
        if isinstance(other, Time):
            if self.precision != other.precision:
                raise TypeError(
                    f'Cannot compare times with different precisions: {self} and {other}'
                    )
        else:
            raise TypeError('Cannot compare Time with non-Time type')

    def __lt__(self, other):
        self._check_can_compare(other)
        return self.value < other.value

    def __le__(self, other):
        self._check_can_compare(other)
        return self.value <= other.value

    def __int__(self):
        if self.precision == 9:
            return self.value
        if self.precision == 6:
            return self.value // _nanos_per_micro
        if self.precision == 3:
            return self.value // _nanos_per_milli
        if self.precision == 0:
            return self.value // _nanos_per_second
        raise BodoError(f'Unsupported precision: {self.precision}')

    def __hash__(self):
        return hash((self.value, self.precision))

    @property
    def hour(self):
        return self.value // _nanos_per_hour

    @property
    def minute(self):
        return self.value % _nanos_per_hour // _nanos_per_minute

    @property
    def second(self):
        return self.value % _nanos_per_minute // _nanos_per_second

    @property
    def millisecond(self):
        return self.value % _nanos_per_second // _nanos_per_milli

    @property
    def microsecond(self):
        return self.value % _nanos_per_milli // _nanos_per_micro

    @property
    def nanosecond(self):
        return self.value % _nanos_per_micro


def time_from_str(time_str, precision=9):
    hour = 0
    minute = 0
    second = 0
    millisecond = 0
    microsecond = 0
    nanosecond = 0
    hour = int(time_str[:2])
    assert time_str[2] == ':', 'Invalid time string'
    minute = int(time_str[3:5])
    assert time_str[5] == ':', 'Invalid time string'
    second = int(time_str[6:8])
    if len(time_str) > 8:
        assert time_str[8] == '.', 'Invalid time string'
        millisecond = int(time_str[9:12])
        if len(time_str) > 12:
            microsecond = int(time_str[12:15])
            if len(time_str) > 15:
                nanosecond = int(time_str[15:18])
    return Time(hour, minute, second, millisecond, microsecond, nanosecond,
        precision=precision)


@overload(time_from_str)
def overload_time_from_str(time_str, precision=9):
    return time_from_str


ll.add_symbol('box_time_array', hdatetime_ext.box_time_array)
ll.add_symbol('unbox_time_array', hdatetime_ext.unbox_time_array)


class TimeType(types.Type):

    def __init__(self, precision):
        assert isinstance(precision, int
            ) and precision >= 0 and precision <= 9, 'precision must be an integer between 0 and 9'
        self.precision = precision
        super(TimeType, self).__init__(name=f'TimeType({precision})')
        self.bitwidth = 64


@typeof_impl.register(Time)
def typeof_time(val, c):
    return TimeType(val.precision)


@overload(Time)
def overload_time(hour=0, min=0, second=0, millisecond=0, microsecond=0,
    nanosecond=0, precision=9):
    if isinstance(hour, types.Integer) or isinstance(hour, types.IntegerLiteral
        ) or hour == 0:

        def impl(hour=0, min=0, second=0, millisecond=0, microsecond=0,
            nanosecond=0, precision=9):
            return cast_int_to_time(_nanos_per_hour * hour + 
                _nanos_per_minute * min + _nanos_per_second * second + 
                _nanos_per_milli * millisecond + _nanos_per_micro *
                microsecond + nanosecond, precision)
    else:
        raise TypeError(f'Invalid type for Time: {type(hour)}')
    return impl


register_model(TimeType)(models.IntegerModel)


@overload_attribute(TimeType, 'hour')
def time_hour_attribute(val):
    return lambda val: cast_time_to_int(val) // _nanos_per_hour


@overload_attribute(TimeType, 'minute')
def time_minute_attribute(val):
    return lambda val: cast_time_to_int(val
        ) % _nanos_per_hour // _nanos_per_minute


@overload_attribute(TimeType, 'second')
def time_second_attribute(val):
    return lambda val: cast_time_to_int(val
        ) % _nanos_per_minute // _nanos_per_second


@overload_attribute(TimeType, 'millisecond')
def time_millisecond_attribute(val):
    return lambda val: cast_time_to_int(val
        ) % _nanos_per_second // _nanos_per_milli


@overload_attribute(TimeType, 'microsecond')
def time_microsecond_attribute(val):
    return lambda val: cast_time_to_int(val
        ) % _nanos_per_milli // _nanos_per_micro


@overload_attribute(TimeType, 'nanosecond')
def time_nanosecond_attribute(val):
    return lambda val: cast_time_to_int(val) % _nanos_per_micro


def _to_nanos_codegen(c, hour_ll, minute_ll, second_ll, millisecond_ll,
    microsecond_ll, nanosecond_ll):
    return c.builder.add(nanosecond_ll, c.builder.add(c.builder.mul(
        microsecond_ll, lir.Constant(lir.IntType(64), _nanos_per_micro)), c
        .builder.add(c.builder.mul(millisecond_ll, lir.Constant(lir.IntType
        (64), _nanos_per_milli)), c.builder.add(c.builder.mul(second_ll,
        lir.Constant(lir.IntType(64), _nanos_per_second)), c.builder.add(c.
        builder.mul(minute_ll, lir.Constant(lir.IntType(64),
        _nanos_per_minute)), c.builder.mul(hour_ll, lir.Constant(lir.
        IntType(64), _nanos_per_hour)))))))


def _from_nanos_codegen(c, val):
    zikl__dxah = c.pyapi.long_from_longlong(c.builder.udiv(val, lir.
        Constant(lir.IntType(64), _nanos_per_hour)))
    dnne__twd = c.pyapi.long_from_longlong(c.builder.udiv(c.builder.urem(
        val, lir.Constant(lir.IntType(64), _nanos_per_hour)), lir.Constant(
        lir.IntType(64), _nanos_per_minute)))
    jwot__zrlkp = c.pyapi.long_from_longlong(c.builder.udiv(c.builder.urem(
        val, lir.Constant(lir.IntType(64), _nanos_per_minute)), lir.
        Constant(lir.IntType(64), _nanos_per_second)))
    olyof__uzw = c.pyapi.long_from_longlong(c.builder.udiv(c.builder.urem(
        val, lir.Constant(lir.IntType(64), _nanos_per_second)), lir.
        Constant(lir.IntType(64), _nanos_per_milli)))
    bpwi__curn = c.pyapi.long_from_longlong(c.builder.udiv(c.builder.urem(
        val, lir.Constant(lir.IntType(64), _nanos_per_milli)), lir.Constant
        (lir.IntType(64), _nanos_per_micro)))
    ptiw__ofze = c.pyapi.long_from_longlong(c.builder.urem(val, lir.
        Constant(lir.IntType(64), _nanos_per_micro)))
    return (zikl__dxah, dnne__twd, jwot__zrlkp, olyof__uzw, bpwi__curn,
        ptiw__ofze)


@unbox(TimeType)
def unbox_time(typ, val, c):
    zikl__dxah = c.pyapi.object_getattr_string(val, 'hour')
    dnne__twd = c.pyapi.object_getattr_string(val, 'minute')
    jwot__zrlkp = c.pyapi.object_getattr_string(val, 'second')
    olyof__uzw = c.pyapi.object_getattr_string(val, 'millisecond')
    bpwi__curn = c.pyapi.object_getattr_string(val, 'microsecond')
    ptiw__ofze = c.pyapi.object_getattr_string(val, 'nanosecond')
    hour_ll = c.pyapi.long_as_longlong(zikl__dxah)
    minute_ll = c.pyapi.long_as_longlong(dnne__twd)
    second_ll = c.pyapi.long_as_longlong(jwot__zrlkp)
    millisecond_ll = c.pyapi.long_as_longlong(olyof__uzw)
    microsecond_ll = c.pyapi.long_as_longlong(bpwi__curn)
    nanosecond_ll = c.pyapi.long_as_longlong(ptiw__ofze)
    xrv__qef = _to_nanos_codegen(c, hour_ll, minute_ll, second_ll,
        millisecond_ll, microsecond_ll, nanosecond_ll)
    c.pyapi.decref(zikl__dxah)
    c.pyapi.decref(dnne__twd)
    c.pyapi.decref(jwot__zrlkp)
    c.pyapi.decref(olyof__uzw)
    c.pyapi.decref(bpwi__curn)
    c.pyapi.decref(ptiw__ofze)
    zgs__eogtz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xrv__qef, is_error=zgs__eogtz)


@lower_constant(TimeType)
def lower_constant_time(context, builder, ty, pyval):
    hour_ll = context.get_constant(types.int64, pyval.hour)
    minute_ll = context.get_constant(types.int64, pyval.minute)
    second_ll = context.get_constant(types.int64, pyval.second)
    millisecond_ll = context.get_constant(types.int64, pyval.millisecond)
    microsecond_ll = context.get_constant(types.int64, pyval.microsecond)
    nanosecond_ll = context.get_constant(types.int64, pyval.nanosecond)
    xrv__qef = _to_nanos_codegen(context, hour_ll, minute_ll, second_ll,
        millisecond_ll, microsecond_ll, nanosecond_ll)
    return xrv__qef


@box(TimeType)
def box_time(typ, val, c):
    (zikl__dxah, dnne__twd, jwot__zrlkp, olyof__uzw, bpwi__curn, ptiw__ofze
        ) = _from_nanos_codegen(c, val)
    dmrr__erggw = c.pyapi.unserialize(c.pyapi.serialize_object(Time))
    utgma__wdu = c.pyapi.call_function_objargs(dmrr__erggw, (zikl__dxah,
        dnne__twd, jwot__zrlkp, olyof__uzw, bpwi__curn, ptiw__ofze, c.pyapi
        .long_from_longlong(lir.Constant(lir.IntType(64), typ.precision))))
    c.pyapi.decref(zikl__dxah)
    c.pyapi.decref(dnne__twd)
    c.pyapi.decref(jwot__zrlkp)
    c.pyapi.decref(olyof__uzw)
    c.pyapi.decref(bpwi__curn)
    c.pyapi.decref(ptiw__ofze)
    c.pyapi.decref(dmrr__erggw)
    return utgma__wdu


@lower_builtin(Time, types.int64, types.int64, types.int64, types.int64,
    types.int64, types.int64)
def impl_ctor_time(context, builder, sig, args):
    (hour_ll, minute_ll, second_ll, millisecond_ll, microsecond_ll,
        nanosecond_ll) = args
    xrv__qef = _to_nanos_codegen(context, hour_ll, minute_ll, second_ll,
        millisecond_ll, microsecond_ll, nanosecond_ll)
    return xrv__qef


@intrinsic
def cast_int_to_time(typingctx, val, precision):
    assert types.unliteral(val) == types.int64, 'val must be int64'
    assert isinstance(precision, types.IntegerLiteral
        ), 'precision must be an integer literal'

    def codegen(context, builder, signature, args):
        return args[0]
    return TimeType(precision.literal_value)(types.int64, types.int64), codegen


@intrinsic
def cast_time_to_int(typingctx, val):
    assert isinstance(val, TimeType), 'val must be Time'

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


class TimeArrayType(types.ArrayCompatible):

    def __init__(self, precision):
        assert isinstance(precision, int
            ) and precision >= 0 and precision <= 9, 'precision must be an integer between 0 and 9'
        self.precision = precision
        super(TimeArrayType, self).__init__(name=f'TimeArrayType({precision})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return TimeType(self.precision)

    def copy(self):
        return TimeArrayType(self.precision)


data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(TimeArrayType)
class TimeArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        doac__ldktr = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, doac__ldktr)


make_attribute_wrapper(TimeArrayType, 'data', '_data')
make_attribute_wrapper(TimeArrayType, 'null_bitmap', '_null_bitmap')


@overload_method(TimeArrayType, 'copy', no_unliteral=True)
def overload_time_arr_copy(A):
    precision = A.precision
    """Copy a TimeArrayType by copying the underlying data and null bitmap"""
    return lambda A: bodo.hiframes.time_ext.init_time_array(A._data.copy(),
        A._null_bitmap.copy(), precision)


@overload_attribute(TimeArrayType, 'dtype')
def overload_time_arr_dtype(A):
    return lambda A: np.object_


@unbox(TimeArrayType)
def unbox_time_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    fslqf__oypdj = types.Array(types.intp, 1, 'C')
    yitj__vsw = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        fslqf__oypdj, [n])
    qttu__ith = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    xdb__eho = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types.
        Array(types.uint8, 1, 'C'), [qttu__ith])
    srq__hzr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer(
        ), lir.IntType(64), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer()])
    tlrj__wcdze = cgutils.get_or_insert_function(c.builder.module, srq__hzr,
        name='unbox_time_array')
    c.builder.call(tlrj__wcdze, [val, n, yitj__vsw.data, xdb__eho.data])
    cjycb__punhp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cjycb__punhp.data = yitj__vsw._getvalue()
    cjycb__punhp.null_bitmap = xdb__eho._getvalue()
    zgs__eogtz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cjycb__punhp._getvalue(), is_error=zgs__eogtz)


@box(TimeArrayType)
def box_time_array(typ, val, c):
    ppuf__qzse = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    yitj__vsw = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, ppuf__qzse.data)
    dygoz__hnj = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, ppuf__qzse.null_bitmap).data
    n = c.builder.extract_value(yitj__vsw.shape, 0)
    srq__hzr = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8)])
    aqurf__arvmy = cgutils.get_or_insert_function(c.builder.module,
        srq__hzr, name='box_time_array')
    nzm__qpsbr = c.builder.call(aqurf__arvmy, [n, yitj__vsw.data,
        dygoz__hnj, lir.Constant(lir.IntType(8), typ.precision)])
    c.context.nrt.decref(c.builder, typ, val)
    return nzm__qpsbr


@intrinsic
def init_time_array(typingctx, data, nulls, precision):
    assert data == types.Array(types.int64, 1, 'C'
        ), 'data must be an array of int64'
    assert nulls == types.Array(types.uint8, 1, 'C'
        ), 'nulls must be an array of uint8'
    assert isinstance(precision, types.IntegerLiteral
        ), 'precision must be an integer literal'

    def codegen(context, builder, signature, args):
        crc__wsg, bahf__ttpy, pxtg__ohvfm = args
        mhp__zgmqc = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        mhp__zgmqc.data = crc__wsg
        mhp__zgmqc.null_bitmap = bahf__ttpy
        context.nrt.incref(builder, signature.args[0], crc__wsg)
        context.nrt.incref(builder, signature.args[1], bahf__ttpy)
        return mhp__zgmqc._getvalue()
    sig = TimeArrayType(precision.literal_value)(data, nulls, precision)
    return sig, codegen


@lower_constant(TimeArrayType)
def lower_constant_time_arr(context, builder, typ, pyval):
    n = len(pyval)
    yitj__vsw = np.full(n, 0, np.int64)
    zkc__fuwcc = np.empty(n + 7 >> 3, np.uint8)
    for unwpr__dpct, ihz__ucan in enumerate(pyval):
        gfnbx__nev = pd.isna(ihz__ucan)
        bodo.libs.int_arr_ext.set_bit_to_arr(zkc__fuwcc, unwpr__dpct, int(
            not gfnbx__nev))
        if not gfnbx__nev:
            yitj__vsw[unwpr__dpct] = (ihz__ucan.hour * _nanos_per_hour + 
                ihz__ucan.minute * _nanos_per_minute + ihz__ucan.second *
                _nanos_per_second + ihz__ucan.millisecond *
                _nanos_per_milli + ihz__ucan.microsecond * _nanos_per_micro +
                ihz__ucan.nanosecond)
    twurj__hzy = context.get_constant_generic(builder, data_type, yitj__vsw)
    wmosl__vjlbn = context.get_constant_generic(builder, nulls_type, zkc__fuwcc
        )
    return lir.Constant.literal_struct([twurj__hzy, wmosl__vjlbn])


@numba.njit(no_cpython_wrapper=True)
def alloc_time_array(n, precision):
    yitj__vsw = np.empty(n, dtype=np.int64)
    nulls = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_time_array(yitj__vsw, nulls, precision)


def alloc_time_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws, 'alloc_time_array() takes two arguments'
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_time_ext_alloc_time_array = (
    alloc_time_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def time_arr_getitem(A, ind):
    if not isinstance(A, TimeArrayType):
        return
    precision = A.precision
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: cast_int_to_time(A._data[ind], precision)
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            adkj__dzxu, tccu__nssw = array_getitem_bool_index(A, ind)
            return init_time_array(adkj__dzxu, tccu__nssw, precision)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            adkj__dzxu, tccu__nssw = array_getitem_int_index(A, ind)
            return init_time_array(adkj__dzxu, tccu__nssw, precision)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            adkj__dzxu, tccu__nssw = array_getitem_slice_index(A, ind)
            return init_time_array(adkj__dzxu, tccu__nssw, precision)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for TimeArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def time_arr_setitem(A, idx, val):
    if not isinstance(A, TimeArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    ddnh__xfgi = (
        f"setitem for TimeArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if isinstance(types.unliteral(val), TimeType):

            def impl(A, idx, val):
                A._data[idx] = cast_time_to_int(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl
        else:
            raise BodoError(ddnh__xfgi)
    if not (is_iterable_type(val) and isinstance(val.dtype, TimeType) or
        isinstance(types.unliteral(val), TimeType)):
        raise BodoError(ddnh__xfgi)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):
        if isinstance(types.unliteral(val), TimeType):
            return lambda A, idx, val: array_setitem_int_index(A, idx,
                cast_time_to_int(val))

        def impl_arr_ind(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if isinstance(types.unliteral(val), TimeType):
            return lambda A, idx, val: array_setitem_bool_index(A, idx,
                cast_time_to_int(val))

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):
        if isinstance(types.unliteral(val), TimeType):
            return lambda A, idx, val: array_setitem_slice_index(A, idx,
                cast_time_to_int(val))

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for TimeArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_len_time_arr(A):
    if isinstance(A, TimeArrayType):
        return lambda A: len(A._data)


@overload_attribute(TimeArrayType, 'shape')
def overload_time_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(TimeArrayType, 'nbytes')
def time_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


def create_cmp_op_overload(op):

    def overload_time_cmp(lhs, rhs):
        if isinstance(lhs, TimeType) and isinstance(rhs, TimeType):

            def impl(lhs, rhs):
                snbdq__cztey = cast_time_to_int(lhs)
                dwjd__iak = cast_time_to_int(rhs)
                return op(0 if snbdq__cztey == dwjd__iak else 1 if 
                    snbdq__cztey > dwjd__iak else -1, 0)
            return impl
    return overload_time_cmp
