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
        yuhaf__czp = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, yuhaf__czp)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    nyqr__dxjbd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ncnow__wogqm = c.pyapi.long_from_longlong(nyqr__dxjbd.n)
    xfxlq__xdab = c.pyapi.from_native_value(types.boolean, nyqr__dxjbd.
        normalize, c.env_manager)
    negra__zkn = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    uocbv__ghl = c.pyapi.call_function_objargs(negra__zkn, (ncnow__wogqm,
        xfxlq__xdab))
    c.pyapi.decref(ncnow__wogqm)
    c.pyapi.decref(xfxlq__xdab)
    c.pyapi.decref(negra__zkn)
    return uocbv__ghl


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    ncnow__wogqm = c.pyapi.object_getattr_string(val, 'n')
    xfxlq__xdab = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(ncnow__wogqm)
    normalize = c.pyapi.to_native_value(types.bool_, xfxlq__xdab).value
    nyqr__dxjbd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nyqr__dxjbd.n = n
    nyqr__dxjbd.normalize = normalize
    c.pyapi.decref(ncnow__wogqm)
    c.pyapi.decref(xfxlq__xdab)
    bxc__bkfuo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nyqr__dxjbd._getvalue(), is_error=bxc__bkfuo)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        nyqr__dxjbd = cgutils.create_struct_proxy(typ)(context, builder)
        nyqr__dxjbd.n = args[0]
        nyqr__dxjbd.normalize = args[1]
        return nyqr__dxjbd._getvalue()
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
        vej__qoc = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    vej__qoc)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=vej__qoc)
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
        yuhaf__czp = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, yuhaf__czp)


@box(MonthEndType)
def box_month_end(typ, val, c):
    azao__jiw = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ncnow__wogqm = c.pyapi.long_from_longlong(azao__jiw.n)
    xfxlq__xdab = c.pyapi.from_native_value(types.boolean, azao__jiw.
        normalize, c.env_manager)
    oicvl__migit = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    uocbv__ghl = c.pyapi.call_function_objargs(oicvl__migit, (ncnow__wogqm,
        xfxlq__xdab))
    c.pyapi.decref(ncnow__wogqm)
    c.pyapi.decref(xfxlq__xdab)
    c.pyapi.decref(oicvl__migit)
    return uocbv__ghl


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    ncnow__wogqm = c.pyapi.object_getattr_string(val, 'n')
    xfxlq__xdab = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(ncnow__wogqm)
    normalize = c.pyapi.to_native_value(types.bool_, xfxlq__xdab).value
    azao__jiw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    azao__jiw.n = n
    azao__jiw.normalize = normalize
    c.pyapi.decref(ncnow__wogqm)
    c.pyapi.decref(xfxlq__xdab)
    bxc__bkfuo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(azao__jiw._getvalue(), is_error=bxc__bkfuo)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        azao__jiw = cgutils.create_struct_proxy(typ)(context, builder)
        azao__jiw.n = args[0]
        azao__jiw.normalize = args[1]
        return azao__jiw._getvalue()
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
        azao__jiw = get_days_in_month(year, month)
        if azao__jiw > day:
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
        vej__qoc = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    vej__qoc)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=vej__qoc)
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
        yuhaf__czp = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, yuhaf__czp)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    gsqi__qhp = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    gqr__lbs = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for diygv__vql, iejme__fmt in enumerate(date_offset_fields):
        c.builder.store(getattr(gsqi__qhp, iejme__fmt), c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(gqr__lbs, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * diygv__vql)), lir.IntType(64)
            .as_pointer()))
    qfjnr__zuho = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    tdnvm__onu = cgutils.get_or_insert_function(c.builder.module,
        qfjnr__zuho, name='box_date_offset')
    bvr__vkgt = c.builder.call(tdnvm__onu, [gsqi__qhp.n, gsqi__qhp.
        normalize, gqr__lbs, gsqi__qhp.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return bvr__vkgt


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    ncnow__wogqm = c.pyapi.object_getattr_string(val, 'n')
    xfxlq__xdab = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(ncnow__wogqm)
    normalize = c.pyapi.to_native_value(types.bool_, xfxlq__xdab).value
    gqr__lbs = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    qfjnr__zuho = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    otflq__umo = cgutils.get_or_insert_function(c.builder.module,
        qfjnr__zuho, name='unbox_date_offset')
    has_kws = c.builder.call(otflq__umo, [val, gqr__lbs])
    gsqi__qhp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gsqi__qhp.n = n
    gsqi__qhp.normalize = normalize
    for diygv__vql, iejme__fmt in enumerate(date_offset_fields):
        setattr(gsqi__qhp, iejme__fmt, c.builder.load(c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(gqr__lbs, lir.IntType(64)), lir.
            Constant(lir.IntType(64), 8 * diygv__vql)), lir.IntType(64).
            as_pointer())))
    gsqi__qhp.has_kws = has_kws
    c.pyapi.decref(ncnow__wogqm)
    c.pyapi.decref(xfxlq__xdab)
    bxc__bkfuo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gsqi__qhp._getvalue(), is_error=bxc__bkfuo)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    ocn__ctqy = [n, normalize]
    has_kws = False
    tkgp__zpna = [0] * 9 + [-1] * 9
    for diygv__vql, iejme__fmt in enumerate(date_offset_fields):
        if hasattr(pyval, iejme__fmt):
            jbz__nmf = context.get_constant(types.int64, getattr(pyval,
                iejme__fmt))
            has_kws = True
        else:
            jbz__nmf = context.get_constant(types.int64, tkgp__zpna[diygv__vql]
                )
        ocn__ctqy.append(jbz__nmf)
    has_kws = context.get_constant(types.boolean, has_kws)
    ocn__ctqy.append(has_kws)
    return lir.Constant.literal_struct(ocn__ctqy)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    vjs__xsn = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for boug__vft in vjs__xsn:
        if not is_overload_none(boug__vft):
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
        gsqi__qhp = cgutils.create_struct_proxy(typ)(context, builder)
        gsqi__qhp.n = args[0]
        gsqi__qhp.normalize = args[1]
        gsqi__qhp.years = args[2]
        gsqi__qhp.months = args[3]
        gsqi__qhp.weeks = args[4]
        gsqi__qhp.days = args[5]
        gsqi__qhp.hours = args[6]
        gsqi__qhp.minutes = args[7]
        gsqi__qhp.seconds = args[8]
        gsqi__qhp.microseconds = args[9]
        gsqi__qhp.nanoseconds = args[10]
        gsqi__qhp.year = args[11]
        gsqi__qhp.month = args[12]
        gsqi__qhp.day = args[13]
        gsqi__qhp.weekday = args[14]
        gsqi__qhp.hour = args[15]
        gsqi__qhp.minute = args[16]
        gsqi__qhp.second = args[17]
        gsqi__qhp.microsecond = args[18]
        gsqi__qhp.nanosecond = args[19]
        gsqi__qhp.has_kws = args[20]
        return gsqi__qhp._getvalue()
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
        vvm__tnodh = -1 if dateoffset.n < 0 else 1
        for qutbz__cuwxw in range(np.abs(dateoffset.n)):
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
            year += vvm__tnodh * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += vvm__tnodh * dateoffset._months
            year, month, bfpto__cbswo = calculate_month_end_date(year,
                month, day, 0)
            if day > bfpto__cbswo:
                day = bfpto__cbswo
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
            if vvm__tnodh == -1:
                td = -td
            ts = ts + td
            if dateoffset._weekday != -1:
                sltg__mbka = ts.weekday()
                epjx__gcg = (dateoffset._weekday - sltg__mbka) % 7
                ts = ts + pd.Timedelta(days=epjx__gcg)
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
        yuhaf__czp = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, yuhaf__czp)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        caxo__xgiyy = -1 if weekday is None else weekday
        return init_week(n, normalize, caxo__xgiyy)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        mah__vfxl = cgutils.create_struct_proxy(typ)(context, builder)
        mah__vfxl.n = args[0]
        mah__vfxl.normalize = args[1]
        mah__vfxl.weekday = args[2]
        return mah__vfxl._getvalue()
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
    mah__vfxl = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ncnow__wogqm = c.pyapi.long_from_longlong(mah__vfxl.n)
    xfxlq__xdab = c.pyapi.from_native_value(types.boolean, mah__vfxl.
        normalize, c.env_manager)
    noeen__oldqr = c.pyapi.long_from_longlong(mah__vfxl.weekday)
    lig__lzblg = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    omu__erm = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -1
        ), mah__vfxl.weekday)
    with c.builder.if_else(omu__erm) as (mcd__wpukm, lyj__gyefw):
        with mcd__wpukm:
            ofsim__xvad = c.pyapi.call_function_objargs(lig__lzblg, (
                ncnow__wogqm, xfxlq__xdab, noeen__oldqr))
            jyjai__aledw = c.builder.block
        with lyj__gyefw:
            armt__wtaa = c.pyapi.call_function_objargs(lig__lzblg, (
                ncnow__wogqm, xfxlq__xdab))
            oluzh__mjnhp = c.builder.block
    uocbv__ghl = c.builder.phi(ofsim__xvad.type)
    uocbv__ghl.add_incoming(ofsim__xvad, jyjai__aledw)
    uocbv__ghl.add_incoming(armt__wtaa, oluzh__mjnhp)
    c.pyapi.decref(noeen__oldqr)
    c.pyapi.decref(ncnow__wogqm)
    c.pyapi.decref(xfxlq__xdab)
    c.pyapi.decref(lig__lzblg)
    return uocbv__ghl


@unbox(WeekType)
def unbox_week(typ, val, c):
    ncnow__wogqm = c.pyapi.object_getattr_string(val, 'n')
    xfxlq__xdab = c.pyapi.object_getattr_string(val, 'normalize')
    noeen__oldqr = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(ncnow__wogqm)
    normalize = c.pyapi.to_native_value(types.bool_, xfxlq__xdab).value
    ixie__hlihz = c.pyapi.make_none()
    cvp__xwh = c.builder.icmp_unsigned('==', noeen__oldqr, ixie__hlihz)
    with c.builder.if_else(cvp__xwh) as (lyj__gyefw, mcd__wpukm):
        with mcd__wpukm:
            ofsim__xvad = c.pyapi.long_as_longlong(noeen__oldqr)
            jyjai__aledw = c.builder.block
        with lyj__gyefw:
            armt__wtaa = lir.Constant(lir.IntType(64), -1)
            oluzh__mjnhp = c.builder.block
    uocbv__ghl = c.builder.phi(ofsim__xvad.type)
    uocbv__ghl.add_incoming(ofsim__xvad, jyjai__aledw)
    uocbv__ghl.add_incoming(armt__wtaa, oluzh__mjnhp)
    mah__vfxl = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mah__vfxl.n = n
    mah__vfxl.normalize = normalize
    mah__vfxl.weekday = uocbv__ghl
    c.pyapi.decref(ncnow__wogqm)
    c.pyapi.decref(xfxlq__xdab)
    c.pyapi.decref(noeen__oldqr)
    bxc__bkfuo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mah__vfxl._getvalue(), is_error=bxc__bkfuo)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and isinstance(rhs, PandasTimestampType):

        def impl(lhs, rhs):
            if lhs.normalize:
                iyzf__ojs = rhs.normalize()
            else:
                iyzf__ojs = rhs
            tex__dqxx = calculate_week_date(lhs.n, lhs.weekday, iyzf__ojs)
            return iyzf__ojs + tex__dqxx
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            if lhs.normalize:
                iyzf__ojs = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                iyzf__ojs = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            tex__dqxx = calculate_week_date(lhs.n, lhs.weekday, iyzf__ojs)
            return iyzf__ojs + tex__dqxx
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            tex__dqxx = calculate_week_date(lhs.n, lhs.weekday, rhs)
            return rhs + tex__dqxx
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
                vxw__nru = input_date_or_ts.weekday()
                if weekday != vxw__nru:
                    ryor__nip = (weekday - vxw__nru) % 7
                    if n > 0:
                        n = n - 1
                td = pd.Timedelta(weeks=n, days=ryor__nip)
            return update_timedelta_with_transition(input_date_or_ts, td)
        return impl_tz_aware
    else:

        def impl(n, weekday, input_date_or_ts):
            if weekday == -1:
                return pd.Timedelta(weeks=n)
            vxw__nru = input_date_or_ts.weekday()
            if weekday != vxw__nru:
                ryor__nip = (weekday - vxw__nru) % 7
                if n > 0:
                    n = n - 1
            return pd.Timedelta(weeks=n, days=ryor__nip)
        return impl


def update_timedelta_with_transition(ts_value, timedelta):
    pass


@overload(update_timedelta_with_transition)
def overload_update_timedelta_with_transition(ts, td):
    if tz_has_transition_times(ts.tz):
        vudyi__duqck = pytz.timezone(ts.tz)
        bqhzf__xnvik = np.array(vudyi__duqck._utc_transition_times, dtype=
            'M8[ns]').view('i8')
        vfqk__vfwn = np.array(vudyi__duqck._transition_info)[:, 0]
        vfqk__vfwn = (pd.Series(vfqk__vfwn).dt.total_seconds() * 1000000000
            ).astype(np.int64).values

        def impl_tz_aware(ts, td):
            scbp__ykpn = ts.value
            fce__ppeh = scbp__ykpn + td.value
            huhc__nlmgh = np.searchsorted(bqhzf__xnvik, scbp__ykpn, side=
                'right') - 1
            dlk__uvral = np.searchsorted(bqhzf__xnvik, fce__ppeh, side='right'
                ) - 1
            ryor__nip = vfqk__vfwn[huhc__nlmgh] - vfqk__vfwn[dlk__uvral]
            return pd.Timedelta(td.value + ryor__nip)
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
    for lrtih__vuffn in date_offset_unsupported_attrs:
        orei__lbdi = 'pandas.tseries.offsets.DateOffset.' + lrtih__vuffn
        overload_attribute(DateOffsetType, lrtih__vuffn)(
            create_unsupported_overload(orei__lbdi))
    for lrtih__vuffn in date_offset_unsupported:
        orei__lbdi = 'pandas.tseries.offsets.DateOffset.' + lrtih__vuffn
        overload_method(DateOffsetType, lrtih__vuffn)(
            create_unsupported_overload(orei__lbdi))


def _install_month_begin_unsupported():
    for lrtih__vuffn in month_begin_unsupported_attrs:
        orei__lbdi = 'pandas.tseries.offsets.MonthBegin.' + lrtih__vuffn
        overload_attribute(MonthBeginType, lrtih__vuffn)(
            create_unsupported_overload(orei__lbdi))
    for lrtih__vuffn in month_begin_unsupported:
        orei__lbdi = 'pandas.tseries.offsets.MonthBegin.' + lrtih__vuffn
        overload_method(MonthBeginType, lrtih__vuffn)(
            create_unsupported_overload(orei__lbdi))


def _install_month_end_unsupported():
    for lrtih__vuffn in date_offset_unsupported_attrs:
        orei__lbdi = 'pandas.tseries.offsets.MonthEnd.' + lrtih__vuffn
        overload_attribute(MonthEndType, lrtih__vuffn)(
            create_unsupported_overload(orei__lbdi))
    for lrtih__vuffn in date_offset_unsupported:
        orei__lbdi = 'pandas.tseries.offsets.MonthEnd.' + lrtih__vuffn
        overload_method(MonthEndType, lrtih__vuffn)(create_unsupported_overload
            (orei__lbdi))


def _install_week_unsupported():
    for lrtih__vuffn in week_unsupported_attrs:
        orei__lbdi = 'pandas.tseries.offsets.Week.' + lrtih__vuffn
        overload_attribute(WeekType, lrtih__vuffn)(create_unsupported_overload
            (orei__lbdi))
    for lrtih__vuffn in week_unsupported:
        orei__lbdi = 'pandas.tseries.offsets.Week.' + lrtih__vuffn
        overload_method(WeekType, lrtih__vuffn)(create_unsupported_overload
            (orei__lbdi))


def _install_offsets_unsupported():
    for jbz__nmf in offsets_unsupported:
        orei__lbdi = 'pandas.tseries.offsets.' + jbz__nmf.__name__
        overload(jbz__nmf)(create_unsupported_overload(orei__lbdi))


def _install_frequencies_unsupported():
    for jbz__nmf in frequencies_unsupported:
        orei__lbdi = 'pandas.tseries.frequencies.' + jbz__nmf.__name__
        overload(jbz__nmf)(create_unsupported_overload(orei__lbdi))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
