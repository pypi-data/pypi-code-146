"""Numba extension support for datetime.date objects and their arrays.
"""
import datetime
import operator
import warnings
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.typing.templates import AttributeTemplate, infer_getattr
from numba.core.utils import PYVERSION
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import DatetimeDatetimeType
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type, is_overload_int, is_overload_none
ll.add_symbol('box_datetime_date_array', hdatetime_ext.box_datetime_date_array)
ll.add_symbol('unbox_datetime_date_array', hdatetime_ext.
    unbox_datetime_date_array)
ll.add_symbol('get_isocalendar', hdatetime_ext.get_isocalendar)


class DatetimeDateType(types.Type):

    def __init__(self):
        super(DatetimeDateType, self).__init__(name='DatetimeDateType()')
        self.bitwidth = 64


datetime_date_type = DatetimeDateType()


@typeof_impl.register(datetime.date)
def typeof_datetime_date(val, c):
    return datetime_date_type


register_model(DatetimeDateType)(models.IntegerModel)


@infer_getattr
class DatetimeAttribute(AttributeTemplate):
    key = DatetimeDateType

    def resolve_year(self, typ):
        return types.int64

    def resolve_month(self, typ):
        return types.int64

    def resolve_day(self, typ):
        return types.int64


@lower_getattr(DatetimeDateType, 'year')
def datetime_get_year(context, builder, typ, val):
    return builder.lshr(val, lir.Constant(lir.IntType(64), 32))


@lower_getattr(DatetimeDateType, 'month')
def datetime_get_month(context, builder, typ, val):
    return builder.and_(builder.lshr(val, lir.Constant(lir.IntType(64), 16)
        ), lir.Constant(lir.IntType(64), 65535))


@lower_getattr(DatetimeDateType, 'day')
def datetime_get_day(context, builder, typ, val):
    return builder.and_(val, lir.Constant(lir.IntType(64), 65535))


@unbox(DatetimeDateType)
def unbox_datetime_date(typ, val, c):
    asyzm__fyytc = c.pyapi.object_getattr_string(val, 'year')
    eie__zbydf = c.pyapi.object_getattr_string(val, 'month')
    ehzk__xsy = c.pyapi.object_getattr_string(val, 'day')
    qfi__irdlv = c.pyapi.long_as_longlong(asyzm__fyytc)
    tgk__ogiug = c.pyapi.long_as_longlong(eie__zbydf)
    nlbtb__vip = c.pyapi.long_as_longlong(ehzk__xsy)
    anc__uerlt = c.builder.add(nlbtb__vip, c.builder.add(c.builder.shl(
        qfi__irdlv, lir.Constant(lir.IntType(64), 32)), c.builder.shl(
        tgk__ogiug, lir.Constant(lir.IntType(64), 16))))
    c.pyapi.decref(asyzm__fyytc)
    c.pyapi.decref(eie__zbydf)
    c.pyapi.decref(ehzk__xsy)
    stms__vpyr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(anc__uerlt, is_error=stms__vpyr)


@lower_constant(DatetimeDateType)
def lower_constant_datetime_date(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    anc__uerlt = builder.add(day, builder.add(builder.shl(year, lir.
        Constant(lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir
        .IntType(64), 16))))
    return anc__uerlt


@box(DatetimeDateType)
def box_datetime_date(typ, val, c):
    asyzm__fyytc = c.pyapi.long_from_longlong(c.builder.lshr(val, lir.
        Constant(lir.IntType(64), 32)))
    eie__zbydf = c.pyapi.long_from_longlong(c.builder.and_(c.builder.lshr(
        val, lir.Constant(lir.IntType(64), 16)), lir.Constant(lir.IntType(
        64), 65535)))
    ehzk__xsy = c.pyapi.long_from_longlong(c.builder.and_(val, lir.Constant
        (lir.IntType(64), 65535)))
    ted__xyinl = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.date))
    mgitb__wqyik = c.pyapi.call_function_objargs(ted__xyinl, (asyzm__fyytc,
        eie__zbydf, ehzk__xsy))
    c.pyapi.decref(asyzm__fyytc)
    c.pyapi.decref(eie__zbydf)
    c.pyapi.decref(ehzk__xsy)
    c.pyapi.decref(ted__xyinl)
    return mgitb__wqyik


@type_callable(datetime.date)
def type_datetime_date(context):

    def typer(year, month, day):
        return datetime_date_type
    return typer


@lower_builtin(datetime.date, types.IntegerLiteral, types.IntegerLiteral,
    types.IntegerLiteral)
@lower_builtin(datetime.date, types.int64, types.int64, types.int64)
def impl_ctor_datetime_date(context, builder, sig, args):
    year, month, day = args
    anc__uerlt = builder.add(day, builder.add(builder.shl(year, lir.
        Constant(lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir
        .IntType(64), 16))))
    return anc__uerlt


@intrinsic
def cast_int_to_datetime_date(typingctx, val=None):
    assert val == types.int64

    def codegen(context, builder, signature, args):
        return args[0]
    return datetime_date_type(types.int64), codegen


@intrinsic
def cast_datetime_date_to_int(typingctx, val=None):
    assert val == datetime_date_type

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(datetime_date_type), codegen


"""
Following codes are copied from
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""
_MAXORDINAL = 3652059
_DAYS_IN_MONTH = np.array([-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 
    31], dtype=np.int64)
_DAYS_BEFORE_MONTH = np.array([-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 
    273, 304, 334], dtype=np.int64)


@register_jitable
def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


@register_jitable
def _days_before_year(year):
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


@register_jitable
def _days_in_month(year, month):
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


@register_jitable
def _days_before_month(year, month):
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


_DI400Y = _days_before_year(401)
_DI100Y = _days_before_year(101)
_DI4Y = _days_before_year(5)


@register_jitable
def _ymd2ord(year, month, day):
    bjqx__gok = _days_in_month(year, month)
    return _days_before_year(year) + _days_before_month(year, month) + day


@register_jitable
def _ord2ymd(n):
    n -= 1
    thf__nrer, n = divmod(n, _DI400Y)
    year = thf__nrer * 400 + 1
    jel__maky, n = divmod(n, _DI100Y)
    nvmy__mbmij, n = divmod(n, _DI4Y)
    fhzuy__ojnf, n = divmod(n, 365)
    year += jel__maky * 100 + nvmy__mbmij * 4 + fhzuy__ojnf
    if fhzuy__ojnf == 4 or jel__maky == 4:
        return year - 1, 12, 31
    qcslj__nnn = fhzuy__ojnf == 3 and (nvmy__mbmij != 24 or jel__maky == 3)
    month = n + 50 >> 5
    gga__zmt = _DAYS_BEFORE_MONTH[month] + (month > 2 and qcslj__nnn)
    if gga__zmt > n:
        month -= 1
        gga__zmt -= _DAYS_IN_MONTH[month] + (month == 2 and qcslj__nnn)
    n -= gga__zmt
    return year, month, n + 1


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@intrinsic
def get_isocalendar(typingctx, dt_year, dt_month, dt_day):

    def codegen(context, builder, sig, args):
        year = cgutils.alloca_once(builder, lir.IntType(64))
        aodus__wgblb = cgutils.alloca_once(builder, lir.IntType(64))
        olzir__ygsgb = cgutils.alloca_once(builder, lir.IntType(64))
        rsmo__xtl = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir.
            IntType(64), lir.IntType(64), lir.IntType(64).as_pointer(), lir
            .IntType(64).as_pointer(), lir.IntType(64).as_pointer()])
        tbm__clu = cgutils.get_or_insert_function(builder.module, rsmo__xtl,
            name='get_isocalendar')
        builder.call(tbm__clu, [args[0], args[1], args[2], year,
            aodus__wgblb, olzir__ygsgb])
        return cgutils.pack_array(builder, [builder.load(year), builder.
            load(aodus__wgblb), builder.load(olzir__ygsgb)])
    mgitb__wqyik = types.Tuple([types.int64, types.int64, types.int64])(types
        .int64, types.int64, types.int64), codegen
    return mgitb__wqyik


types.datetime_date_type = datetime_date_type


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_date_type'):
        d = datetime.date.today()
    return d


@register_jitable
def fromordinal_impl(n):
    y, jyiw__aglwn, d = _ord2ymd(n)
    return datetime.date(y, jyiw__aglwn, d)


@overload_method(DatetimeDateType, 'replace')
def replace_overload(date, year=None, month=None, day=None):
    if not is_overload_none(year) and not is_overload_int(year):
        raise BodoError('date.replace(): year must be an integer')
    elif not is_overload_none(month) and not is_overload_int(month):
        raise BodoError('date.replace(): month must be an integer')
    elif not is_overload_none(day) and not is_overload_int(day):
        raise BodoError('date.replace(): day must be an integer')

    def impl(date, year=None, month=None, day=None):
        mrn__mmwqu = date.year if year is None else year
        vkxlj__dkan = date.month if month is None else month
        yzhba__oru = date.day if day is None else day
        return datetime.date(mrn__mmwqu, vkxlj__dkan, yzhba__oru)
    return impl


@overload_method(DatetimeDatetimeType, 'toordinal', no_unliteral=True)
@overload_method(DatetimeDateType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


@overload_method(DatetimeDatetimeType, 'weekday', no_unliteral=True)
@overload_method(DatetimeDateType, 'weekday', no_unliteral=True)
def weekday(date):

    def impl(date):
        return (date.toordinal() + 6) % 7
    return impl


@overload_method(DatetimeDateType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(date):

    def impl(date):
        year, aodus__wgblb, jrx__qcu = get_isocalendar(date.year, date.
            month, date.day)
        return year, aodus__wgblb, jrx__qcu
    return impl


def overload_add_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            tvd__wre = lhs.toordinal() + rhs.days
            if 0 < tvd__wre <= _MAXORDINAL:
                return fromordinal_impl(tvd__wre)
            raise OverflowError('result out of range')
        return impl
    elif lhs == datetime_timedelta_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            tvd__wre = lhs.days + rhs.toordinal()
            if 0 < tvd__wre <= _MAXORDINAL:
                return fromordinal_impl(tvd__wre)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + datetime.timedelta(-rhs.days)
        return impl
    elif lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            ssqk__hgtbo = lhs.toordinal()
            wbiw__mtuwd = rhs.toordinal()
            return datetime.timedelta(ssqk__hgtbo - wbiw__mtuwd)
        return impl
    if lhs == datetime_date_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            dmnzy__zdx = lhs
            numba.parfors.parfor.init_prange()
            n = len(dmnzy__zdx)
            A = alloc_datetime_date_array(n)
            for qevl__isc in numba.parfors.parfor.internal_prange(n):
                A[qevl__isc] = dmnzy__zdx[qevl__isc] - rhs
            return A
        return impl


@overload(min, no_unliteral=True)
def date_min(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def date_max(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        ihag__pndwq = np.uint8(td.year // 256)
        elde__vodku = np.uint8(td.year % 256)
        month = np.uint8(td.month)
        day = np.uint8(td.day)
        jzji__thu = ihag__pndwq, elde__vodku, month, day
        return hash(jzji__thu)
    return impl


@overload(bool, inline='always', no_unliteral=True)
def date_to_bool(date):
    if date != datetime_date_type:
        return

    def impl(date):
        return True
    return impl


if PYVERSION >= (3, 9):
    IsoCalendarDate = datetime.date(2011, 1, 1).isocalendar().__class__


    class IsoCalendarDateType(types.Type):

        def __init__(self):
            super(IsoCalendarDateType, self).__init__(name=
                'IsoCalendarDateType()')
    iso_calendar_date_type = DatetimeDateType()

    @typeof_impl.register(IsoCalendarDate)
    def typeof_datetime_date(val, c):
        return iso_calendar_date_type


class DatetimeDateArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeDateArrayType, self).__init__(name=
            'DatetimeDateArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_date_type

    def copy(self):
        return DatetimeDateArrayType()


datetime_date_array_type = DatetimeDateArrayType()
types.datetime_date_array_type = datetime_date_array_type
data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeDateArrayType)
class DatetimeDateArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ntgq__ofm = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, ntgq__ofm)


make_attribute_wrapper(DatetimeDateArrayType, 'data', '_data')
make_attribute_wrapper(DatetimeDateArrayType, 'null_bitmap', '_null_bitmap')


@overload_method(DatetimeDateArrayType, 'copy', no_unliteral=True)
def overload_datetime_date_arr_copy(A):
    return lambda A: bodo.hiframes.datetime_date_ext.init_datetime_date_array(A
        ._data.copy(), A._null_bitmap.copy())


@overload_attribute(DatetimeDateArrayType, 'dtype')
def overload_datetime_date_arr_dtype(A):
    return lambda A: np.object_


@unbox(DatetimeDateArrayType)
def unbox_datetime_date_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    dhc__bfd = types.Array(types.intp, 1, 'C')
    spydx__yfpts = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        dhc__bfd, [n])
    bikt__vbjf = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    cpet__uoa = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [bikt__vbjf])
    rsmo__xtl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer()])
    oxpit__swl = cgutils.get_or_insert_function(c.builder.module, rsmo__xtl,
        name='unbox_datetime_date_array')
    c.builder.call(oxpit__swl, [val, n, spydx__yfpts.data, cpet__uoa.data])
    dfs__sjjy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    dfs__sjjy.data = spydx__yfpts._getvalue()
    dfs__sjjy.null_bitmap = cpet__uoa._getvalue()
    stms__vpyr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dfs__sjjy._getvalue(), is_error=stms__vpyr)


def int_to_datetime_date_python(ia):
    return datetime.date(ia >> 32, ia >> 16 & 65535, ia & 65535)


def int_array_to_datetime_date(ia):
    return np.vectorize(int_to_datetime_date_python, otypes=[object])(ia)


@box(DatetimeDateArrayType)
def box_datetime_date_array(typ, val, c):
    dmnzy__zdx = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    spydx__yfpts = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, dmnzy__zdx.data)
    rtum__qum = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, dmnzy__zdx.null_bitmap).data
    n = c.builder.extract_value(spydx__yfpts.shape, 0)
    rsmo__xtl = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(8).as_pointer()])
    pewlh__lugj = cgutils.get_or_insert_function(c.builder.module,
        rsmo__xtl, name='box_datetime_date_array')
    addxt__kjjko = c.builder.call(pewlh__lugj, [n, spydx__yfpts.data,
        rtum__qum])
    c.context.nrt.decref(c.builder, typ, val)
    return addxt__kjjko


@intrinsic
def init_datetime_date_array(typingctx, data, nulls=None):
    assert data == types.Array(types.int64, 1, 'C') or data == types.Array(
        types.NPDatetime('ns'), 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        izw__mlled, ndzj__jdfn = args
        pqnm__fwkq = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        pqnm__fwkq.data = izw__mlled
        pqnm__fwkq.null_bitmap = ndzj__jdfn
        context.nrt.incref(builder, signature.args[0], izw__mlled)
        context.nrt.incref(builder, signature.args[1], ndzj__jdfn)
        return pqnm__fwkq._getvalue()
    sig = datetime_date_array_type(data, nulls)
    return sig, codegen


@lower_constant(DatetimeDateArrayType)
def lower_constant_datetime_date_arr(context, builder, typ, pyval):
    n = len(pyval)
    oyg__phj = (1970 << 32) + (1 << 16) + 1
    spydx__yfpts = np.full(n, oyg__phj, np.int64)
    cphz__atfi = np.empty(n + 7 >> 3, np.uint8)
    for qevl__isc, eqh__fxmke in enumerate(pyval):
        uonv__dck = pd.isna(eqh__fxmke)
        bodo.libs.int_arr_ext.set_bit_to_arr(cphz__atfi, qevl__isc, int(not
            uonv__dck))
        if not uonv__dck:
            spydx__yfpts[qevl__isc] = (eqh__fxmke.year << 32) + (eqh__fxmke
                .month << 16) + eqh__fxmke.day
    ghhb__kze = context.get_constant_generic(builder, data_type, spydx__yfpts)
    aff__yqcx = context.get_constant_generic(builder, nulls_type, cphz__atfi)
    return lir.Constant.literal_struct([ghhb__kze, aff__yqcx])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_date_array(n):
    spydx__yfpts = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_date_array(spydx__yfpts, nulls)


def alloc_datetime_date_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_date_ext_alloc_datetime_date_array
    ) = alloc_datetime_date_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_date_arr_getitem(A, ind):
    if A != datetime_date_array_type:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: cast_int_to_datetime_date(A._data[ind])
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            cti__xvuxe, exn__yao = array_getitem_bool_index(A, ind)
            return init_datetime_date_array(cti__xvuxe, exn__yao)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            cti__xvuxe, exn__yao = array_getitem_int_index(A, ind)
            return init_datetime_date_array(cti__xvuxe, exn__yao)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            cti__xvuxe, exn__yao = array_getitem_slice_index(A, ind)
            return init_datetime_date_array(cti__xvuxe, exn__yao)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for DatetimeDateArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def dt_date_arr_setitem(A, idx, val):
    if A != datetime_date_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    bol__qubs = (
        f"setitem for DatetimeDateArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == datetime_date_type:

            def impl(A, idx, val):
                A._data[idx] = cast_datetime_date_to_int(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl
        else:
            raise BodoError(bol__qubs)
    if not (is_iterable_type(val) and val.dtype == bodo.datetime_date_type or
        types.unliteral(val) == datetime_date_type):
        raise BodoError(bol__qubs)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_int_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_arr_ind(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_bool_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_slice_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeDateArray with indexing type {idx} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_date_arr(A):
    if A == datetime_date_array_type:
        return lambda A: len(A._data)


@overload_attribute(DatetimeDateArrayType, 'shape')
def overload_datetime_date_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DatetimeDateArrayType, 'nbytes')
def datetime_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


def create_cmp_op_overload(op):

    def overload_date_cmp(lhs, rhs):
        if lhs == datetime_date_type and rhs == datetime_date_type:

            def impl(lhs, rhs):
                y, qrm__makbm = lhs.year, rhs.year
                jyiw__aglwn, qitgn__oca = lhs.month, rhs.month
                d, pnvnx__acyw = lhs.day, rhs.day
                return op(_cmp((y, jyiw__aglwn, d), (qrm__makbm, qitgn__oca,
                    pnvnx__acyw)), 0)
            return impl
    return overload_date_cmp


def create_datetime_date_cmp_op_overload(op):

    def overload_cmp(lhs, rhs):
        dhm__ishy = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[op]} {rhs} is always {op == operator.ne} in Python. If this is unexpected there may be a bug in your code.'
            )
        warnings.warn(dhm__ishy, bodo.utils.typing.BodoWarning)
        if op == operator.eq:
            return lambda lhs, rhs: False
        elif op == operator.ne:
            return lambda lhs, rhs: True
    return overload_cmp


def create_datetime_array_date_cmp_op_overload(op):

    def overload_arr_cmp(lhs, rhs):
        if isinstance(lhs, types.Array) and lhs.dtype == bodo.datetime64ns:
            if rhs == datetime_date_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(lhs)
                    zdgt__pnq = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for qevl__isc in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, qevl__isc):
                            bodo.libs.array_kernels.setna(zdgt__pnq, qevl__isc)
                        else:
                            zdgt__pnq[qevl__isc] = op(lhs[qevl__isc], bodo.
                                utils.conversion.
                                unbox_if_tz_naive_timestamp(pd.Timestamp(rhs)))
                    return zdgt__pnq
                return impl
            elif rhs == datetime_date_array_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(lhs)
                    zdgt__pnq = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for qevl__isc in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, qevl__isc
                            ) or bodo.libs.array_kernels.isna(rhs, qevl__isc):
                            bodo.libs.array_kernels.setna(zdgt__pnq, qevl__isc)
                        else:
                            zdgt__pnq[qevl__isc] = op(lhs[qevl__isc], bodo.
                                utils.conversion.
                                unbox_if_tz_naive_timestamp(pd.Timestamp(
                                rhs[qevl__isc])))
                    return zdgt__pnq
                return impl
        elif isinstance(rhs, types.Array) and rhs.dtype == bodo.datetime64ns:
            if lhs == datetime_date_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(rhs)
                    zdgt__pnq = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for qevl__isc in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(rhs, qevl__isc):
                            bodo.libs.array_kernels.setna(zdgt__pnq, qevl__isc)
                        else:
                            zdgt__pnq[qevl__isc] = op(bodo.utils.conversion
                                .unbox_if_tz_naive_timestamp(pd.Timestamp(
                                lhs)), rhs[qevl__isc])
                    return zdgt__pnq
                return impl
            elif lhs == datetime_date_array_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(rhs)
                    zdgt__pnq = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for qevl__isc in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, qevl__isc
                            ) or bodo.libs.array_kernels.isna(rhs, qevl__isc):
                            bodo.libs.array_kernels.setna(zdgt__pnq, qevl__isc)
                        else:
                            zdgt__pnq[qevl__isc] = op(bodo.utils.conversion
                                .unbox_if_tz_naive_timestamp(pd.Timestamp(
                                lhs[qevl__isc])), rhs[qevl__isc])
                    return zdgt__pnq
                return impl
    return overload_arr_cmp


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            evglo__nctjp = True
        else:
            evglo__nctjp = False
        if lhs == datetime_date_array_type and rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                zdgt__pnq = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qevl__isc in numba.parfors.parfor.internal_prange(n):
                    qmyea__ljef = bodo.libs.array_kernels.isna(lhs, qevl__isc)
                    crcp__xxufd = bodo.libs.array_kernels.isna(rhs, qevl__isc)
                    if qmyea__ljef or crcp__xxufd:
                        ejesw__jbio = evglo__nctjp
                    else:
                        ejesw__jbio = op(lhs[qevl__isc], rhs[qevl__isc])
                    zdgt__pnq[qevl__isc] = ejesw__jbio
                return zdgt__pnq
            return impl
        elif lhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                zdgt__pnq = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qevl__isc in numba.parfors.parfor.internal_prange(n):
                    fqei__sodek = bodo.libs.array_kernels.isna(lhs, qevl__isc)
                    if fqei__sodek:
                        ejesw__jbio = evglo__nctjp
                    else:
                        ejesw__jbio = op(lhs[qevl__isc], rhs)
                    zdgt__pnq[qevl__isc] = ejesw__jbio
                return zdgt__pnq
            return impl
        elif rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                zdgt__pnq = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qevl__isc in numba.parfors.parfor.internal_prange(n):
                    fqei__sodek = bodo.libs.array_kernels.isna(rhs, qevl__isc)
                    if fqei__sodek:
                        ejesw__jbio = evglo__nctjp
                    else:
                        ejesw__jbio = op(lhs, rhs[qevl__isc])
                    zdgt__pnq[qevl__isc] = ejesw__jbio
                return zdgt__pnq
            return impl
    return overload_date_arr_cmp
