"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, get_days_in_month, pd_timestamp_tz_naive_type, tz_has_transition_times
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, create_unsupported_overload, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        oypda__xhgtw = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, oypda__xhgtw)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    ubwc__xqez = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    fkof__gqi = c.pyapi.long_from_longlong(ubwc__xqez.n)
    iva__kje = c.pyapi.from_native_value(types.boolean, ubwc__xqez.
        normalize, c.env_manager)
    axzft__tezuw = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    ykgs__ekccg = c.pyapi.call_function_objargs(axzft__tezuw, (fkof__gqi,
        iva__kje))
    c.pyapi.decref(fkof__gqi)
    c.pyapi.decref(iva__kje)
    c.pyapi.decref(axzft__tezuw)
    return ykgs__ekccg


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    fkof__gqi = c.pyapi.object_getattr_string(val, 'n')
    iva__kje = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(fkof__gqi)
    normalize = c.pyapi.to_native_value(types.bool_, iva__kje).value
    ubwc__xqez = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ubwc__xqez.n = n
    ubwc__xqez.normalize = normalize
    c.pyapi.decref(fkof__gqi)
    c.pyapi.decref(iva__kje)
    reupm__xkw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ubwc__xqez._getvalue(), is_error=reupm__xkw)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        ubwc__xqez = cgutils.create_struct_proxy(typ)(context, builder)
        ubwc__xqez.n = args[0]
        ubwc__xqez.normalize = args[1]
        return ubwc__xqez._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and isinstance(rhs, PandasTimestampType):
        ontbz__qqc = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    ontbz__qqc)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=ontbz__qqc)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if (isinstance(lhs, PandasTimestampType) or lhs in [
        datetime_datetime_type, datetime_date_type]
        ) and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        oypda__xhgtw = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, oypda__xhgtw)


@box(MonthEndType)
def box_month_end(typ, val, c):
    ytzy__dktil = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    fkof__gqi = c.pyapi.long_from_longlong(ytzy__dktil.n)
    iva__kje = c.pyapi.from_native_value(types.boolean, ytzy__dktil.
        normalize, c.env_manager)
    fnw__yvv = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    ykgs__ekccg = c.pyapi.call_function_objargs(fnw__yvv, (fkof__gqi, iva__kje)
        )
    c.pyapi.decref(fkof__gqi)
    c.pyapi.decref(iva__kje)
    c.pyapi.decref(fnw__yvv)
    return ykgs__ekccg


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    fkof__gqi = c.pyapi.object_getattr_string(val, 'n')
    iva__kje = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(fkof__gqi)
    normalize = c.pyapi.to_native_value(types.bool_, iva__kje).value
    ytzy__dktil = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ytzy__dktil.n = n
    ytzy__dktil.normalize = normalize
    c.pyapi.decref(fkof__gqi)
    c.pyapi.decref(iva__kje)
    reupm__xkw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ytzy__dktil._getvalue(), is_error=reupm__xkw)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        ytzy__dktil = cgutils.create_struct_proxy(typ)(context, builder)
        ytzy__dktil.n = args[0]
        ytzy__dktil.normalize = args[1]
        return ytzy__dktil._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    return lir.Constant.literal_struct([n, normalize])


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        ytzy__dktil = get_days_in_month(year, month)
        if ytzy__dktil > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and isinstance(rhs, PandasTimestampType):
        ontbz__qqc = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    ontbz__qqc)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=ontbz__qqc)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if (isinstance(lhs, PandasTimestampType) or lhs in [
        datetime_datetime_type, datetime_date_type]) and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        oypda__xhgtw = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, oypda__xhgtw)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    ubaay__tvtw = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    istcz__lxx = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for fjgi__euq, hrop__ovbki in enumerate(date_offset_fields):
        c.builder.store(getattr(ubaay__tvtw, hrop__ovbki), c.builder.
            inttoptr(c.builder.add(c.builder.ptrtoint(istcz__lxx, lir.
            IntType(64)), lir.Constant(lir.IntType(64), 8 * fjgi__euq)),
            lir.IntType(64).as_pointer()))
    hanhe__yznjs = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    qdszk__mbut = cgutils.get_or_insert_function(c.builder.module,
        hanhe__yznjs, name='box_date_offset')
    lflq__tsm = c.builder.call(qdszk__mbut, [ubaay__tvtw.n, ubaay__tvtw.
        normalize, istcz__lxx, ubaay__tvtw.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return lflq__tsm


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    fkof__gqi = c.pyapi.object_getattr_string(val, 'n')
    iva__kje = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(fkof__gqi)
    normalize = c.pyapi.to_native_value(types.bool_, iva__kje).value
    istcz__lxx = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    hanhe__yznjs = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    lao__bwcy = cgutils.get_or_insert_function(c.builder.module,
        hanhe__yznjs, name='unbox_date_offset')
    has_kws = c.builder.call(lao__bwcy, [val, istcz__lxx])
    ubaay__tvtw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ubaay__tvtw.n = n
    ubaay__tvtw.normalize = normalize
    for fjgi__euq, hrop__ovbki in enumerate(date_offset_fields):
        setattr(ubaay__tvtw, hrop__ovbki, c.builder.load(c.builder.inttoptr
            (c.builder.add(c.builder.ptrtoint(istcz__lxx, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * fjgi__euq)), lir.IntType(64).
            as_pointer())))
    ubaay__tvtw.has_kws = has_kws
    c.pyapi.decref(fkof__gqi)
    c.pyapi.decref(iva__kje)
    reupm__xkw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ubaay__tvtw._getvalue(), is_error=reupm__xkw)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    cmhd__dgnzj = [n, normalize]
    has_kws = False
    kxg__vyx = [0] * 9 + [-1] * 9
    for fjgi__euq, hrop__ovbki in enumerate(date_offset_fields):
        if hasattr(pyval, hrop__ovbki):
            ikxgv__wdyh = context.get_constant(types.int64, getattr(pyval,
                hrop__ovbki))
            has_kws = True
        else:
            ikxgv__wdyh = context.get_constant(types.int64, kxg__vyx[fjgi__euq]
                )
        cmhd__dgnzj.append(ikxgv__wdyh)
    has_kws = context.get_constant(types.boolean, has_kws)
    cmhd__dgnzj.append(has_kws)
    return lir.Constant.literal_struct(cmhd__dgnzj)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    ehbnb__xhmwr = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for klqd__zbrq in ehbnb__xhmwr:
        if not is_overload_none(klqd__zbrq):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        ubaay__tvtw = cgutils.create_struct_proxy(typ)(context, builder)
        ubaay__tvtw.n = args[0]
        ubaay__tvtw.normalize = args[1]
        ubaay__tvtw.years = args[2]
        ubaay__tvtw.months = args[3]
        ubaay__tvtw.weeks = args[4]
        ubaay__tvtw.days = args[5]
        ubaay__tvtw.hours = args[6]
        ubaay__tvtw.minutes = args[7]
        ubaay__tvtw.seconds = args[8]
        ubaay__tvtw.microseconds = args[9]
        ubaay__tvtw.nanoseconds = args[10]
        ubaay__tvtw.year = args[11]
        ubaay__tvtw.month = args[12]
        ubaay__tvtw.day = args[13]
        ubaay__tvtw.weekday = args[14]
        ubaay__tvtw.hour = args[15]
        ubaay__tvtw.minute = args[16]
        ubaay__tvtw.second = args[17]
        ubaay__tvtw.microsecond = args[18]
        ubaay__tvtw.nanosecond = args[19]
        ubaay__tvtw.has_kws = args[20]
        return ubaay__tvtw._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        iagd__brit = -1 if dateoffset.n < 0 else 1
        for yiuhs__npi in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += iagd__brit * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += iagd__brit * dateoffset._months
            year, month, jdq__vals = calculate_month_end_date(year, month,
                day, 0)
            if day > jdq__vals:
                day = jdq__vals
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            if dateoffset._nanosecond != -1:
                nanosecond = dateoffset._nanosecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            td = pd.Timedelta(days=dateoffset._days + 7 * dateoffset._weeks,
                hours=dateoffset._hours, minutes=dateoffset._minutes,
                seconds=dateoffset._seconds, microseconds=dateoffset.
                _microseconds)
            td = td + pd.Timedelta(dateoffset._nanoseconds, unit='ns')
            if iagd__brit == -1:
                td = -td
            ts = ts + td
            if dateoffset._weekday != -1:
                qlsdg__bcun = ts.weekday()
                prk__spc = (dateoffset._weekday - qlsdg__bcun) % 7
                ts = ts + pd.Timedelta(days=prk__spc)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_tz_naive_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_tz_naive_type,
        datetime_date_type] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if (lhs in [datetime_datetime_type, datetime_date_type] or isinstance(
        lhs, PandasTimestampType)) and rhs in [date_offset_type,
        month_begin_type, month_end_type, week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    elif lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    elif lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    elif lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    else:
        return
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        oypda__xhgtw = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, oypda__xhgtw)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        ttwof__aeo = -1 if weekday is None else weekday
        return init_week(n, normalize, ttwof__aeo)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        csojl__oce = cgutils.create_struct_proxy(typ)(context, builder)
        csojl__oce.n = args[0]
        csojl__oce.normalize = args[1]
        csojl__oce.weekday = args[2]
        return csojl__oce._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        weekday = context.get_constant(types.int64, -1)
    return lir.Constant.literal_struct([n, normalize, weekday])


@box(WeekType)
def box_week(typ, val, c):
    csojl__oce = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    fkof__gqi = c.pyapi.long_from_longlong(csojl__oce.n)
    iva__kje = c.pyapi.from_native_value(types.boolean, csojl__oce.
        normalize, c.env_manager)
    kqdtq__mfj = c.pyapi.long_from_longlong(csojl__oce.weekday)
    ppnw__fpw = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    dwh__eqyai = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), 
        -1), csojl__oce.weekday)
    with c.builder.if_else(dwh__eqyai) as (hlz__vczn, bkhl__tfoo):
        with hlz__vczn:
            bfi__ikayx = c.pyapi.call_function_objargs(ppnw__fpw, (
                fkof__gqi, iva__kje, kqdtq__mfj))
            bnl__jry = c.builder.block
        with bkhl__tfoo:
            qxb__vugss = c.pyapi.call_function_objargs(ppnw__fpw, (
                fkof__gqi, iva__kje))
            zjjtf__aoxg = c.builder.block
    ykgs__ekccg = c.builder.phi(bfi__ikayx.type)
    ykgs__ekccg.add_incoming(bfi__ikayx, bnl__jry)
    ykgs__ekccg.add_incoming(qxb__vugss, zjjtf__aoxg)
    c.pyapi.decref(kqdtq__mfj)
    c.pyapi.decref(fkof__gqi)
    c.pyapi.decref(iva__kje)
    c.pyapi.decref(ppnw__fpw)
    return ykgs__ekccg


@unbox(WeekType)
def unbox_week(typ, val, c):
    fkof__gqi = c.pyapi.object_getattr_string(val, 'n')
    iva__kje = c.pyapi.object_getattr_string(val, 'normalize')
    kqdtq__mfj = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(fkof__gqi)
    normalize = c.pyapi.to_native_value(types.bool_, iva__kje).value
    gtey__otpdy = c.pyapi.make_none()
    btt__zan = c.builder.icmp_unsigned('==', kqdtq__mfj, gtey__otpdy)
    with c.builder.if_else(btt__zan) as (bkhl__tfoo, hlz__vczn):
        with hlz__vczn:
            bfi__ikayx = c.pyapi.long_as_longlong(kqdtq__mfj)
            bnl__jry = c.builder.block
        with bkhl__tfoo:
            qxb__vugss = lir.Constant(lir.IntType(64), -1)
            zjjtf__aoxg = c.builder.block
    ykgs__ekccg = c.builder.phi(bfi__ikayx.type)
    ykgs__ekccg.add_incoming(bfi__ikayx, bnl__jry)
    ykgs__ekccg.add_incoming(qxb__vugss, zjjtf__aoxg)
    csojl__oce = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    csojl__oce.n = n
    csojl__oce.normalize = normalize
    csojl__oce.weekday = ykgs__ekccg
    c.pyapi.decref(fkof__gqi)
    c.pyapi.decref(iva__kje)
    c.pyapi.decref(kqdtq__mfj)
    reupm__xkw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(csojl__oce._getvalue(), is_error=reupm__xkw)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and isinstance(rhs, PandasTimestampType):

        def impl(lhs, rhs):
            if lhs.normalize:
                wac__afyo = rhs.normalize()
            else:
                wac__afyo = rhs
            zlmwp__czk = calculate_week_date(lhs.n, lhs.weekday, wac__afyo)
            return wac__afyo + zlmwp__czk
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            if lhs.normalize:
                wac__afyo = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                wac__afyo = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            zlmwp__czk = calculate_week_date(lhs.n, lhs.weekday, wac__afyo)
            return wac__afyo + zlmwp__czk
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            zlmwp__czk = calculate_week_date(lhs.n, lhs.weekday, rhs)
            return rhs + zlmwp__czk
        return impl
    if (lhs in [datetime_datetime_type, datetime_date_type] or isinstance(
        lhs, PandasTimestampType)) and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def calculate_week_date(n, weekday, input_date_or_ts):
    pass


@overload(calculate_week_date)
def overload_calculate_week_date(n, weekday, input_date_or_ts):
    if isinstance(input_date_or_ts, PandasTimestampType
        ) and tz_has_transition_times(input_date_or_ts.tz):

        def impl_tz_aware(n, weekday, input_date_or_ts):
            if weekday == -1:
                td = pd.Timedelta(weeks=n)
            else:
                logf__bgd = input_date_or_ts.weekday()
                if weekday != logf__bgd:
                    yreu__wfb = (weekday - logf__bgd) % 7
                    if n > 0:
                        n = n - 1
                td = pd.Timedelta(weeks=n, days=yreu__wfb)
            return update_timedelta_with_transition(input_date_or_ts, td)
        return impl_tz_aware
    else:

        def impl(n, weekday, input_date_or_ts):
            if weekday == -1:
                return pd.Timedelta(weeks=n)
            logf__bgd = input_date_or_ts.weekday()
            if weekday != logf__bgd:
                yreu__wfb = (weekday - logf__bgd) % 7
                if n > 0:
                    n = n - 1
            return pd.Timedelta(weeks=n, days=yreu__wfb)
        return impl


def update_timedelta_with_transition(ts_value, timedelta):
    pass


@overload(update_timedelta_with_transition)
def overload_update_timedelta_with_transition(ts, td):
    if tz_has_transition_times(ts.tz):
        ozgz__orl = pytz.timezone(ts.tz)
        qanxg__ois = np.array(ozgz__orl._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        hwr__gze = np.array(ozgz__orl._transition_info)[:, 0]
        hwr__gze = (pd.Series(hwr__gze).dt.total_seconds() * 1000000000
            ).astype(np.int64).values

        def impl_tz_aware(ts, td):
            dihov__wwsj = ts.value
            mtxnu__sntut = dihov__wwsj + td.value
            ipor__srqb = np.searchsorted(qanxg__ois, dihov__wwsj, side='right'
                ) - 1
            nnoxg__srf = np.searchsorted(qanxg__ois, mtxnu__sntut, side='right'
                ) - 1
            yreu__wfb = hwr__gze[ipor__srqb] - hwr__gze[nnoxg__srf]
            return pd.Timedelta(td.value + yreu__wfb)
        return impl_tz_aware
    else:
        return lambda ts, td: td


date_offset_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
date_offset_unsupported = {'__call__', 'rollback', 'rollforward',
    'is_month_start', 'is_month_end', 'apply', 'apply_index', 'copy',
    'isAnchored', 'onOffset', 'is_anchored', 'is_on_offset',
    'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end'}
month_end_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_end_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
month_begin_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_begin_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
week_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos', 'rule_code'}
week_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
offsets_unsupported = {pd.tseries.offsets.BusinessDay, pd.tseries.offsets.
    BDay, pd.tseries.offsets.BusinessHour, pd.tseries.offsets.
    CustomBusinessDay, pd.tseries.offsets.CDay, pd.tseries.offsets.
    CustomBusinessHour, pd.tseries.offsets.BusinessMonthEnd, pd.tseries.
    offsets.BMonthEnd, pd.tseries.offsets.BusinessMonthBegin, pd.tseries.
    offsets.BMonthBegin, pd.tseries.offsets.CustomBusinessMonthEnd, pd.
    tseries.offsets.CBMonthEnd, pd.tseries.offsets.CustomBusinessMonthBegin,
    pd.tseries.offsets.CBMonthBegin, pd.tseries.offsets.SemiMonthEnd, pd.
    tseries.offsets.SemiMonthBegin, pd.tseries.offsets.WeekOfMonth, pd.
    tseries.offsets.LastWeekOfMonth, pd.tseries.offsets.BQuarterEnd, pd.
    tseries.offsets.BQuarterBegin, pd.tseries.offsets.QuarterEnd, pd.
    tseries.offsets.QuarterBegin, pd.tseries.offsets.BYearEnd, pd.tseries.
    offsets.BYearBegin, pd.tseries.offsets.YearEnd, pd.tseries.offsets.
    YearBegin, pd.tseries.offsets.FY5253, pd.tseries.offsets.FY5253Quarter,
    pd.tseries.offsets.Easter, pd.tseries.offsets.Tick, pd.tseries.offsets.
    Day, pd.tseries.offsets.Hour, pd.tseries.offsets.Minute, pd.tseries.
    offsets.Second, pd.tseries.offsets.Milli, pd.tseries.offsets.Micro, pd.
    tseries.offsets.Nano}
frequencies_unsupported = {pd.tseries.frequencies.to_offset}


def _install_date_offsets_unsupported():
    for blisj__cso in date_offset_unsupported_attrs:
        jkzdf__xft = 'pandas.tseries.offsets.DateOffset.' + blisj__cso
        overload_attribute(DateOffsetType, blisj__cso)(
            create_unsupported_overload(jkzdf__xft))
    for blisj__cso in date_offset_unsupported:
        jkzdf__xft = 'pandas.tseries.offsets.DateOffset.' + blisj__cso
        overload_method(DateOffsetType, blisj__cso)(create_unsupported_overload
            (jkzdf__xft))


def _install_month_begin_unsupported():
    for blisj__cso in month_begin_unsupported_attrs:
        jkzdf__xft = 'pandas.tseries.offsets.MonthBegin.' + blisj__cso
        overload_attribute(MonthBeginType, blisj__cso)(
            create_unsupported_overload(jkzdf__xft))
    for blisj__cso in month_begin_unsupported:
        jkzdf__xft = 'pandas.tseries.offsets.MonthBegin.' + blisj__cso
        overload_method(MonthBeginType, blisj__cso)(create_unsupported_overload
            (jkzdf__xft))


def _install_month_end_unsupported():
    for blisj__cso in date_offset_unsupported_attrs:
        jkzdf__xft = 'pandas.tseries.offsets.MonthEnd.' + blisj__cso
        overload_attribute(MonthEndType, blisj__cso)(
            create_unsupported_overload(jkzdf__xft))
    for blisj__cso in date_offset_unsupported:
        jkzdf__xft = 'pandas.tseries.offsets.MonthEnd.' + blisj__cso
        overload_method(MonthEndType, blisj__cso)(create_unsupported_overload
            (jkzdf__xft))


def _install_week_unsupported():
    for blisj__cso in week_unsupported_attrs:
        jkzdf__xft = 'pandas.tseries.offsets.Week.' + blisj__cso
        overload_attribute(WeekType, blisj__cso)(create_unsupported_overload
            (jkzdf__xft))
    for blisj__cso in week_unsupported:
        jkzdf__xft = 'pandas.tseries.offsets.Week.' + blisj__cso
        overload_method(WeekType, blisj__cso)(create_unsupported_overload(
            jkzdf__xft))


def _install_offsets_unsupported():
    for ikxgv__wdyh in offsets_unsupported:
        jkzdf__xft = 'pandas.tseries.offsets.' + ikxgv__wdyh.__name__
        overload(ikxgv__wdyh)(create_unsupported_overload(jkzdf__xft))


def _install_frequencies_unsupported():
    for ikxgv__wdyh in frequencies_unsupported:
        jkzdf__xft = 'pandas.tseries.frequencies.' + ikxgv__wdyh.__name__
        overload(ikxgv__wdyh)(create_unsupported_overload(jkzdf__xft))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
