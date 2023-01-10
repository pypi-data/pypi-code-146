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
        eev__jcjyo = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, eev__jcjyo)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    uswf__hpjmn = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    vgi__suzn = c.pyapi.long_from_longlong(uswf__hpjmn.n)
    dtys__xdwuk = c.pyapi.from_native_value(types.boolean, uswf__hpjmn.
        normalize, c.env_manager)
    zwa__rng = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    wcgav__iqfn = c.pyapi.call_function_objargs(zwa__rng, (vgi__suzn,
        dtys__xdwuk))
    c.pyapi.decref(vgi__suzn)
    c.pyapi.decref(dtys__xdwuk)
    c.pyapi.decref(zwa__rng)
    return wcgav__iqfn


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    vgi__suzn = c.pyapi.object_getattr_string(val, 'n')
    dtys__xdwuk = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(vgi__suzn)
    normalize = c.pyapi.to_native_value(types.bool_, dtys__xdwuk).value
    uswf__hpjmn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    uswf__hpjmn.n = n
    uswf__hpjmn.normalize = normalize
    c.pyapi.decref(vgi__suzn)
    c.pyapi.decref(dtys__xdwuk)
    wom__hea = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uswf__hpjmn._getvalue(), is_error=wom__hea)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        uswf__hpjmn = cgutils.create_struct_proxy(typ)(context, builder)
        uswf__hpjmn.n = args[0]
        uswf__hpjmn.normalize = args[1]
        return uswf__hpjmn._getvalue()
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
        uwfr__hllj = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    uwfr__hllj)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=uwfr__hllj)
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
        eev__jcjyo = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, eev__jcjyo)


@box(MonthEndType)
def box_month_end(typ, val, c):
    rnkhw__ttih = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    vgi__suzn = c.pyapi.long_from_longlong(rnkhw__ttih.n)
    dtys__xdwuk = c.pyapi.from_native_value(types.boolean, rnkhw__ttih.
        normalize, c.env_manager)
    tyl__lkye = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    wcgav__iqfn = c.pyapi.call_function_objargs(tyl__lkye, (vgi__suzn,
        dtys__xdwuk))
    c.pyapi.decref(vgi__suzn)
    c.pyapi.decref(dtys__xdwuk)
    c.pyapi.decref(tyl__lkye)
    return wcgav__iqfn


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    vgi__suzn = c.pyapi.object_getattr_string(val, 'n')
    dtys__xdwuk = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(vgi__suzn)
    normalize = c.pyapi.to_native_value(types.bool_, dtys__xdwuk).value
    rnkhw__ttih = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rnkhw__ttih.n = n
    rnkhw__ttih.normalize = normalize
    c.pyapi.decref(vgi__suzn)
    c.pyapi.decref(dtys__xdwuk)
    wom__hea = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rnkhw__ttih._getvalue(), is_error=wom__hea)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        rnkhw__ttih = cgutils.create_struct_proxy(typ)(context, builder)
        rnkhw__ttih.n = args[0]
        rnkhw__ttih.normalize = args[1]
        return rnkhw__ttih._getvalue()
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
        rnkhw__ttih = get_days_in_month(year, month)
        if rnkhw__ttih > day:
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
        uwfr__hllj = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    uwfr__hllj)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=uwfr__hllj)
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
        eev__jcjyo = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, eev__jcjyo)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    rmt__gyan = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    dxaa__erysf = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for mot__rhx, pnfng__kihfr in enumerate(date_offset_fields):
        c.builder.store(getattr(rmt__gyan, pnfng__kihfr), c.builder.
            inttoptr(c.builder.add(c.builder.ptrtoint(dxaa__erysf, lir.
            IntType(64)), lir.Constant(lir.IntType(64), 8 * mot__rhx)), lir
            .IntType(64).as_pointer()))
    rsbdu__nmh = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    himrf__tglx = cgutils.get_or_insert_function(c.builder.module,
        rsbdu__nmh, name='box_date_offset')
    iqs__emsgv = c.builder.call(himrf__tglx, [rmt__gyan.n, rmt__gyan.
        normalize, dxaa__erysf, rmt__gyan.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return iqs__emsgv


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    vgi__suzn = c.pyapi.object_getattr_string(val, 'n')
    dtys__xdwuk = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(vgi__suzn)
    normalize = c.pyapi.to_native_value(types.bool_, dtys__xdwuk).value
    dxaa__erysf = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    rsbdu__nmh = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    ush__wvhu = cgutils.get_or_insert_function(c.builder.module, rsbdu__nmh,
        name='unbox_date_offset')
    has_kws = c.builder.call(ush__wvhu, [val, dxaa__erysf])
    rmt__gyan = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rmt__gyan.n = n
    rmt__gyan.normalize = normalize
    for mot__rhx, pnfng__kihfr in enumerate(date_offset_fields):
        setattr(rmt__gyan, pnfng__kihfr, c.builder.load(c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(dxaa__erysf, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * mot__rhx)), lir.IntType(64).
            as_pointer())))
    rmt__gyan.has_kws = has_kws
    c.pyapi.decref(vgi__suzn)
    c.pyapi.decref(dtys__xdwuk)
    wom__hea = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rmt__gyan._getvalue(), is_error=wom__hea)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    wmti__oql = [n, normalize]
    has_kws = False
    xhh__tgqhx = [0] * 9 + [-1] * 9
    for mot__rhx, pnfng__kihfr in enumerate(date_offset_fields):
        if hasattr(pyval, pnfng__kihfr):
            ercqm__igbx = context.get_constant(types.int64, getattr(pyval,
                pnfng__kihfr))
            has_kws = True
        else:
            ercqm__igbx = context.get_constant(types.int64, xhh__tgqhx[
                mot__rhx])
        wmti__oql.append(ercqm__igbx)
    has_kws = context.get_constant(types.boolean, has_kws)
    wmti__oql.append(has_kws)
    return lir.Constant.literal_struct(wmti__oql)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    keoh__ivegg = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for xbfm__xmjb in keoh__ivegg:
        if not is_overload_none(xbfm__xmjb):
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
        rmt__gyan = cgutils.create_struct_proxy(typ)(context, builder)
        rmt__gyan.n = args[0]
        rmt__gyan.normalize = args[1]
        rmt__gyan.years = args[2]
        rmt__gyan.months = args[3]
        rmt__gyan.weeks = args[4]
        rmt__gyan.days = args[5]
        rmt__gyan.hours = args[6]
        rmt__gyan.minutes = args[7]
        rmt__gyan.seconds = args[8]
        rmt__gyan.microseconds = args[9]
        rmt__gyan.nanoseconds = args[10]
        rmt__gyan.year = args[11]
        rmt__gyan.month = args[12]
        rmt__gyan.day = args[13]
        rmt__gyan.weekday = args[14]
        rmt__gyan.hour = args[15]
        rmt__gyan.minute = args[16]
        rmt__gyan.second = args[17]
        rmt__gyan.microsecond = args[18]
        rmt__gyan.nanosecond = args[19]
        rmt__gyan.has_kws = args[20]
        return rmt__gyan._getvalue()
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
        hmnu__nrfbz = -1 if dateoffset.n < 0 else 1
        for qtes__nxfgv in range(np.abs(dateoffset.n)):
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
            year += hmnu__nrfbz * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += hmnu__nrfbz * dateoffset._months
            year, month, eqpf__dwqvz = calculate_month_end_date(year, month,
                day, 0)
            if day > eqpf__dwqvz:
                day = eqpf__dwqvz
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
            if hmnu__nrfbz == -1:
                td = -td
            ts = ts + td
            if dateoffset._weekday != -1:
                vfnmc__bwo = ts.weekday()
                jsas__ktq = (dateoffset._weekday - vfnmc__bwo) % 7
                ts = ts + pd.Timedelta(days=jsas__ktq)
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
        eev__jcjyo = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, eev__jcjyo)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        vbpuw__nkivl = -1 if weekday is None else weekday
        return init_week(n, normalize, vbpuw__nkivl)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        nzl__wzoi = cgutils.create_struct_proxy(typ)(context, builder)
        nzl__wzoi.n = args[0]
        nzl__wzoi.normalize = args[1]
        nzl__wzoi.weekday = args[2]
        return nzl__wzoi._getvalue()
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
    nzl__wzoi = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    vgi__suzn = c.pyapi.long_from_longlong(nzl__wzoi.n)
    dtys__xdwuk = c.pyapi.from_native_value(types.boolean, nzl__wzoi.
        normalize, c.env_manager)
    nmn__uptga = c.pyapi.long_from_longlong(nzl__wzoi.weekday)
    xsuw__cba = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    ype__nrhl = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), nzl__wzoi.weekday)
    with c.builder.if_else(ype__nrhl) as (tsqmg__xmyyq, ahtb__jhgv):
        with tsqmg__xmyyq:
            rsqr__zrhyc = c.pyapi.call_function_objargs(xsuw__cba, (
                vgi__suzn, dtys__xdwuk, nmn__uptga))
            mrjvd__ejgxj = c.builder.block
        with ahtb__jhgv:
            frga__mhwn = c.pyapi.call_function_objargs(xsuw__cba, (
                vgi__suzn, dtys__xdwuk))
            xzrn__axnz = c.builder.block
    wcgav__iqfn = c.builder.phi(rsqr__zrhyc.type)
    wcgav__iqfn.add_incoming(rsqr__zrhyc, mrjvd__ejgxj)
    wcgav__iqfn.add_incoming(frga__mhwn, xzrn__axnz)
    c.pyapi.decref(nmn__uptga)
    c.pyapi.decref(vgi__suzn)
    c.pyapi.decref(dtys__xdwuk)
    c.pyapi.decref(xsuw__cba)
    return wcgav__iqfn


@unbox(WeekType)
def unbox_week(typ, val, c):
    vgi__suzn = c.pyapi.object_getattr_string(val, 'n')
    dtys__xdwuk = c.pyapi.object_getattr_string(val, 'normalize')
    nmn__uptga = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(vgi__suzn)
    normalize = c.pyapi.to_native_value(types.bool_, dtys__xdwuk).value
    ypcjp__tsly = c.pyapi.make_none()
    uwajv__heaha = c.builder.icmp_unsigned('==', nmn__uptga, ypcjp__tsly)
    with c.builder.if_else(uwajv__heaha) as (ahtb__jhgv, tsqmg__xmyyq):
        with tsqmg__xmyyq:
            rsqr__zrhyc = c.pyapi.long_as_longlong(nmn__uptga)
            mrjvd__ejgxj = c.builder.block
        with ahtb__jhgv:
            frga__mhwn = lir.Constant(lir.IntType(64), -1)
            xzrn__axnz = c.builder.block
    wcgav__iqfn = c.builder.phi(rsqr__zrhyc.type)
    wcgav__iqfn.add_incoming(rsqr__zrhyc, mrjvd__ejgxj)
    wcgav__iqfn.add_incoming(frga__mhwn, xzrn__axnz)
    nzl__wzoi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nzl__wzoi.n = n
    nzl__wzoi.normalize = normalize
    nzl__wzoi.weekday = wcgav__iqfn
    c.pyapi.decref(vgi__suzn)
    c.pyapi.decref(dtys__xdwuk)
    c.pyapi.decref(nmn__uptga)
    wom__hea = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nzl__wzoi._getvalue(), is_error=wom__hea)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and isinstance(rhs, PandasTimestampType):

        def impl(lhs, rhs):
            if lhs.normalize:
                bybpi__fzk = rhs.normalize()
            else:
                bybpi__fzk = rhs
            npspu__fjr = calculate_week_date(lhs.n, lhs.weekday, bybpi__fzk)
            return bybpi__fzk + npspu__fjr
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            if lhs.normalize:
                bybpi__fzk = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                bybpi__fzk = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            npspu__fjr = calculate_week_date(lhs.n, lhs.weekday, bybpi__fzk)
            return bybpi__fzk + npspu__fjr
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            npspu__fjr = calculate_week_date(lhs.n, lhs.weekday, rhs)
            return rhs + npspu__fjr
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
                sool__xlmun = input_date_or_ts.weekday()
                if weekday != sool__xlmun:
                    zhrwu__abfc = (weekday - sool__xlmun) % 7
                    if n > 0:
                        n = n - 1
                td = pd.Timedelta(weeks=n, days=zhrwu__abfc)
            return update_timedelta_with_transition(input_date_or_ts, td)
        return impl_tz_aware
    else:

        def impl(n, weekday, input_date_or_ts):
            if weekday == -1:
                return pd.Timedelta(weeks=n)
            sool__xlmun = input_date_or_ts.weekday()
            if weekday != sool__xlmun:
                zhrwu__abfc = (weekday - sool__xlmun) % 7
                if n > 0:
                    n = n - 1
            return pd.Timedelta(weeks=n, days=zhrwu__abfc)
        return impl


def update_timedelta_with_transition(ts_value, timedelta):
    pass


@overload(update_timedelta_with_transition)
def overload_update_timedelta_with_transition(ts, td):
    if tz_has_transition_times(ts.tz):
        cln__wky = pytz.timezone(ts.tz)
        bnbm__evgw = np.array(cln__wky._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        wyc__etn = np.array(cln__wky._transition_info)[:, 0]
        wyc__etn = (pd.Series(wyc__etn).dt.total_seconds() * 1000000000
            ).astype(np.int64).values

        def impl_tz_aware(ts, td):
            kxeq__jsht = ts.value
            jsyn__yyw = kxeq__jsht + td.value
            vybt__ptnep = np.searchsorted(bnbm__evgw, kxeq__jsht, side='right'
                ) - 1
            jnzzi__fvkp = np.searchsorted(bnbm__evgw, jsyn__yyw, side='right'
                ) - 1
            zhrwu__abfc = wyc__etn[vybt__ptnep] - wyc__etn[jnzzi__fvkp]
            return pd.Timedelta(td.value + zhrwu__abfc)
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
    for kdke__who in date_offset_unsupported_attrs:
        qkss__hvka = 'pandas.tseries.offsets.DateOffset.' + kdke__who
        overload_attribute(DateOffsetType, kdke__who)(
            create_unsupported_overload(qkss__hvka))
    for kdke__who in date_offset_unsupported:
        qkss__hvka = 'pandas.tseries.offsets.DateOffset.' + kdke__who
        overload_method(DateOffsetType, kdke__who)(create_unsupported_overload
            (qkss__hvka))


def _install_month_begin_unsupported():
    for kdke__who in month_begin_unsupported_attrs:
        qkss__hvka = 'pandas.tseries.offsets.MonthBegin.' + kdke__who
        overload_attribute(MonthBeginType, kdke__who)(
            create_unsupported_overload(qkss__hvka))
    for kdke__who in month_begin_unsupported:
        qkss__hvka = 'pandas.tseries.offsets.MonthBegin.' + kdke__who
        overload_method(MonthBeginType, kdke__who)(create_unsupported_overload
            (qkss__hvka))


def _install_month_end_unsupported():
    for kdke__who in date_offset_unsupported_attrs:
        qkss__hvka = 'pandas.tseries.offsets.MonthEnd.' + kdke__who
        overload_attribute(MonthEndType, kdke__who)(create_unsupported_overload
            (qkss__hvka))
    for kdke__who in date_offset_unsupported:
        qkss__hvka = 'pandas.tseries.offsets.MonthEnd.' + kdke__who
        overload_method(MonthEndType, kdke__who)(create_unsupported_overload
            (qkss__hvka))


def _install_week_unsupported():
    for kdke__who in week_unsupported_attrs:
        qkss__hvka = 'pandas.tseries.offsets.Week.' + kdke__who
        overload_attribute(WeekType, kdke__who)(create_unsupported_overload
            (qkss__hvka))
    for kdke__who in week_unsupported:
        qkss__hvka = 'pandas.tseries.offsets.Week.' + kdke__who
        overload_method(WeekType, kdke__who)(create_unsupported_overload(
            qkss__hvka))


def _install_offsets_unsupported():
    for ercqm__igbx in offsets_unsupported:
        qkss__hvka = 'pandas.tseries.offsets.' + ercqm__igbx.__name__
        overload(ercqm__igbx)(create_unsupported_overload(qkss__hvka))


def _install_frequencies_unsupported():
    for ercqm__igbx in frequencies_unsupported:
        qkss__hvka = 'pandas.tseries.frequencies.' + ercqm__igbx.__name__
        overload(ercqm__igbx)(create_unsupported_overload(qkss__hvka))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
