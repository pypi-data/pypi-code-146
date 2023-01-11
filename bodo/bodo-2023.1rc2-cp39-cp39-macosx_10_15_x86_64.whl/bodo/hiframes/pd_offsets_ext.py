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
        bjq__hqxxu = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, bjq__hqxxu)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    arzl__rqzt = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    cmjo__git = c.pyapi.long_from_longlong(arzl__rqzt.n)
    ufdq__ecr = c.pyapi.from_native_value(types.boolean, arzl__rqzt.
        normalize, c.env_manager)
    qoou__udy = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    faz__zkehv = c.pyapi.call_function_objargs(qoou__udy, (cmjo__git,
        ufdq__ecr))
    c.pyapi.decref(cmjo__git)
    c.pyapi.decref(ufdq__ecr)
    c.pyapi.decref(qoou__udy)
    return faz__zkehv


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    cmjo__git = c.pyapi.object_getattr_string(val, 'n')
    ufdq__ecr = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(cmjo__git)
    normalize = c.pyapi.to_native_value(types.bool_, ufdq__ecr).value
    arzl__rqzt = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    arzl__rqzt.n = n
    arzl__rqzt.normalize = normalize
    c.pyapi.decref(cmjo__git)
    c.pyapi.decref(ufdq__ecr)
    sdaqn__xnqxr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(arzl__rqzt._getvalue(), is_error=sdaqn__xnqxr)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        arzl__rqzt = cgutils.create_struct_proxy(typ)(context, builder)
        arzl__rqzt.n = args[0]
        arzl__rqzt.normalize = args[1]
        return arzl__rqzt._getvalue()
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
        ujpa__qqe = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    ujpa__qqe)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=ujpa__qqe)
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
        bjq__hqxxu = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, bjq__hqxxu)


@box(MonthEndType)
def box_month_end(typ, val, c):
    azpsq__nys = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    cmjo__git = c.pyapi.long_from_longlong(azpsq__nys.n)
    ufdq__ecr = c.pyapi.from_native_value(types.boolean, azpsq__nys.
        normalize, c.env_manager)
    ota__plg = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    faz__zkehv = c.pyapi.call_function_objargs(ota__plg, (cmjo__git, ufdq__ecr)
        )
    c.pyapi.decref(cmjo__git)
    c.pyapi.decref(ufdq__ecr)
    c.pyapi.decref(ota__plg)
    return faz__zkehv


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    cmjo__git = c.pyapi.object_getattr_string(val, 'n')
    ufdq__ecr = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(cmjo__git)
    normalize = c.pyapi.to_native_value(types.bool_, ufdq__ecr).value
    azpsq__nys = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    azpsq__nys.n = n
    azpsq__nys.normalize = normalize
    c.pyapi.decref(cmjo__git)
    c.pyapi.decref(ufdq__ecr)
    sdaqn__xnqxr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(azpsq__nys._getvalue(), is_error=sdaqn__xnqxr)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        azpsq__nys = cgutils.create_struct_proxy(typ)(context, builder)
        azpsq__nys.n = args[0]
        azpsq__nys.normalize = args[1]
        return azpsq__nys._getvalue()
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
        azpsq__nys = get_days_in_month(year, month)
        if azpsq__nys > day:
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
        ujpa__qqe = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    ujpa__qqe)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=ujpa__qqe)
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
        bjq__hqxxu = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, bjq__hqxxu)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    reudd__qkud = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ihb__ccrzg = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for omciz__pjer, jfq__oopqy in enumerate(date_offset_fields):
        c.builder.store(getattr(reudd__qkud, jfq__oopqy), c.builder.
            inttoptr(c.builder.add(c.builder.ptrtoint(ihb__ccrzg, lir.
            IntType(64)), lir.Constant(lir.IntType(64), 8 * omciz__pjer)),
            lir.IntType(64).as_pointer()))
    qgo__kzjs = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    fcys__aeah = cgutils.get_or_insert_function(c.builder.module, qgo__kzjs,
        name='box_date_offset')
    uxcqc__tonh = c.builder.call(fcys__aeah, [reudd__qkud.n, reudd__qkud.
        normalize, ihb__ccrzg, reudd__qkud.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return uxcqc__tonh


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    cmjo__git = c.pyapi.object_getattr_string(val, 'n')
    ufdq__ecr = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(cmjo__git)
    normalize = c.pyapi.to_native_value(types.bool_, ufdq__ecr).value
    ihb__ccrzg = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    qgo__kzjs = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer()])
    kbmfi__ffnog = cgutils.get_or_insert_function(c.builder.module,
        qgo__kzjs, name='unbox_date_offset')
    has_kws = c.builder.call(kbmfi__ffnog, [val, ihb__ccrzg])
    reudd__qkud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    reudd__qkud.n = n
    reudd__qkud.normalize = normalize
    for omciz__pjer, jfq__oopqy in enumerate(date_offset_fields):
        setattr(reudd__qkud, jfq__oopqy, c.builder.load(c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(ihb__ccrzg, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * omciz__pjer)), lir.IntType(64
            ).as_pointer())))
    reudd__qkud.has_kws = has_kws
    c.pyapi.decref(cmjo__git)
    c.pyapi.decref(ufdq__ecr)
    sdaqn__xnqxr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(reudd__qkud._getvalue(), is_error=sdaqn__xnqxr)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    ttqd__cfn = [n, normalize]
    has_kws = False
    uhx__nnnql = [0] * 9 + [-1] * 9
    for omciz__pjer, jfq__oopqy in enumerate(date_offset_fields):
        if hasattr(pyval, jfq__oopqy):
            smcas__skbnk = context.get_constant(types.int64, getattr(pyval,
                jfq__oopqy))
            has_kws = True
        else:
            smcas__skbnk = context.get_constant(types.int64, uhx__nnnql[
                omciz__pjer])
        ttqd__cfn.append(smcas__skbnk)
    has_kws = context.get_constant(types.boolean, has_kws)
    ttqd__cfn.append(has_kws)
    return lir.Constant.literal_struct(ttqd__cfn)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    cut__stewb = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for gsbxz__wepog in cut__stewb:
        if not is_overload_none(gsbxz__wepog):
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
        reudd__qkud = cgutils.create_struct_proxy(typ)(context, builder)
        reudd__qkud.n = args[0]
        reudd__qkud.normalize = args[1]
        reudd__qkud.years = args[2]
        reudd__qkud.months = args[3]
        reudd__qkud.weeks = args[4]
        reudd__qkud.days = args[5]
        reudd__qkud.hours = args[6]
        reudd__qkud.minutes = args[7]
        reudd__qkud.seconds = args[8]
        reudd__qkud.microseconds = args[9]
        reudd__qkud.nanoseconds = args[10]
        reudd__qkud.year = args[11]
        reudd__qkud.month = args[12]
        reudd__qkud.day = args[13]
        reudd__qkud.weekday = args[14]
        reudd__qkud.hour = args[15]
        reudd__qkud.minute = args[16]
        reudd__qkud.second = args[17]
        reudd__qkud.microsecond = args[18]
        reudd__qkud.nanosecond = args[19]
        reudd__qkud.has_kws = args[20]
        return reudd__qkud._getvalue()
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
        lzmga__qxb = -1 if dateoffset.n < 0 else 1
        for yuo__keo in range(np.abs(dateoffset.n)):
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
            year += lzmga__qxb * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += lzmga__qxb * dateoffset._months
            year, month, wga__jglc = calculate_month_end_date(year, month,
                day, 0)
            if day > wga__jglc:
                day = wga__jglc
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
            if lzmga__qxb == -1:
                td = -td
            ts = ts + td
            if dateoffset._weekday != -1:
                imju__bey = ts.weekday()
                qkn__ujkfl = (dateoffset._weekday - imju__bey) % 7
                ts = ts + pd.Timedelta(days=qkn__ujkfl)
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
        bjq__hqxxu = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, bjq__hqxxu)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        tfw__dqjva = -1 if weekday is None else weekday
        return init_week(n, normalize, tfw__dqjva)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        qxi__uyo = cgutils.create_struct_proxy(typ)(context, builder)
        qxi__uyo.n = args[0]
        qxi__uyo.normalize = args[1]
        qxi__uyo.weekday = args[2]
        return qxi__uyo._getvalue()
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
    qxi__uyo = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    cmjo__git = c.pyapi.long_from_longlong(qxi__uyo.n)
    ufdq__ecr = c.pyapi.from_native_value(types.boolean, qxi__uyo.normalize,
        c.env_manager)
    gcrrt__nyas = c.pyapi.long_from_longlong(qxi__uyo.weekday)
    jjc__ismed = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    tyf__dilw = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), qxi__uyo.weekday)
    with c.builder.if_else(tyf__dilw) as (tod__uef, xxz__mkphl):
        with tod__uef:
            yvsh__gutp = c.pyapi.call_function_objargs(jjc__ismed, (
                cmjo__git, ufdq__ecr, gcrrt__nyas))
            djylz__okazb = c.builder.block
        with xxz__mkphl:
            qqf__nuff = c.pyapi.call_function_objargs(jjc__ismed, (
                cmjo__git, ufdq__ecr))
            jcw__eqgi = c.builder.block
    faz__zkehv = c.builder.phi(yvsh__gutp.type)
    faz__zkehv.add_incoming(yvsh__gutp, djylz__okazb)
    faz__zkehv.add_incoming(qqf__nuff, jcw__eqgi)
    c.pyapi.decref(gcrrt__nyas)
    c.pyapi.decref(cmjo__git)
    c.pyapi.decref(ufdq__ecr)
    c.pyapi.decref(jjc__ismed)
    return faz__zkehv


@unbox(WeekType)
def unbox_week(typ, val, c):
    cmjo__git = c.pyapi.object_getattr_string(val, 'n')
    ufdq__ecr = c.pyapi.object_getattr_string(val, 'normalize')
    gcrrt__nyas = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(cmjo__git)
    normalize = c.pyapi.to_native_value(types.bool_, ufdq__ecr).value
    whqk__fdjbx = c.pyapi.make_none()
    okkp__ltn = c.builder.icmp_unsigned('==', gcrrt__nyas, whqk__fdjbx)
    with c.builder.if_else(okkp__ltn) as (xxz__mkphl, tod__uef):
        with tod__uef:
            yvsh__gutp = c.pyapi.long_as_longlong(gcrrt__nyas)
            djylz__okazb = c.builder.block
        with xxz__mkphl:
            qqf__nuff = lir.Constant(lir.IntType(64), -1)
            jcw__eqgi = c.builder.block
    faz__zkehv = c.builder.phi(yvsh__gutp.type)
    faz__zkehv.add_incoming(yvsh__gutp, djylz__okazb)
    faz__zkehv.add_incoming(qqf__nuff, jcw__eqgi)
    qxi__uyo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qxi__uyo.n = n
    qxi__uyo.normalize = normalize
    qxi__uyo.weekday = faz__zkehv
    c.pyapi.decref(cmjo__git)
    c.pyapi.decref(ufdq__ecr)
    c.pyapi.decref(gcrrt__nyas)
    sdaqn__xnqxr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qxi__uyo._getvalue(), is_error=sdaqn__xnqxr)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and isinstance(rhs, PandasTimestampType):

        def impl(lhs, rhs):
            if lhs.normalize:
                oag__ndibe = rhs.normalize()
            else:
                oag__ndibe = rhs
            mgcm__jbc = calculate_week_date(lhs.n, lhs.weekday, oag__ndibe)
            return oag__ndibe + mgcm__jbc
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            if lhs.normalize:
                oag__ndibe = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                oag__ndibe = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            mgcm__jbc = calculate_week_date(lhs.n, lhs.weekday, oag__ndibe)
            return oag__ndibe + mgcm__jbc
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            mgcm__jbc = calculate_week_date(lhs.n, lhs.weekday, rhs)
            return rhs + mgcm__jbc
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
                jzsk__zqt = input_date_or_ts.weekday()
                if weekday != jzsk__zqt:
                    butbf__llf = (weekday - jzsk__zqt) % 7
                    if n > 0:
                        n = n - 1
                td = pd.Timedelta(weeks=n, days=butbf__llf)
            return update_timedelta_with_transition(input_date_or_ts, td)
        return impl_tz_aware
    else:

        def impl(n, weekday, input_date_or_ts):
            if weekday == -1:
                return pd.Timedelta(weeks=n)
            jzsk__zqt = input_date_or_ts.weekday()
            if weekday != jzsk__zqt:
                butbf__llf = (weekday - jzsk__zqt) % 7
                if n > 0:
                    n = n - 1
            return pd.Timedelta(weeks=n, days=butbf__llf)
        return impl


def update_timedelta_with_transition(ts_value, timedelta):
    pass


@overload(update_timedelta_with_transition)
def overload_update_timedelta_with_transition(ts, td):
    if tz_has_transition_times(ts.tz):
        bmwb__hadtm = pytz.timezone(ts.tz)
        ycn__pzlr = np.array(bmwb__hadtm._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        glex__bjxi = np.array(bmwb__hadtm._transition_info)[:, 0]
        glex__bjxi = (pd.Series(glex__bjxi).dt.total_seconds() * 1000000000
            ).astype(np.int64).values

        def impl_tz_aware(ts, td):
            blgv__icvoq = ts.value
            btkn__efe = blgv__icvoq + td.value
            aag__tcsqg = np.searchsorted(ycn__pzlr, blgv__icvoq, side='right'
                ) - 1
            blw__ulg = np.searchsorted(ycn__pzlr, btkn__efe, side='right') - 1
            butbf__llf = glex__bjxi[aag__tcsqg] - glex__bjxi[blw__ulg]
            return pd.Timedelta(td.value + butbf__llf)
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
    for pyfq__wos in date_offset_unsupported_attrs:
        tqqiw__bnrt = 'pandas.tseries.offsets.DateOffset.' + pyfq__wos
        overload_attribute(DateOffsetType, pyfq__wos)(
            create_unsupported_overload(tqqiw__bnrt))
    for pyfq__wos in date_offset_unsupported:
        tqqiw__bnrt = 'pandas.tseries.offsets.DateOffset.' + pyfq__wos
        overload_method(DateOffsetType, pyfq__wos)(create_unsupported_overload
            (tqqiw__bnrt))


def _install_month_begin_unsupported():
    for pyfq__wos in month_begin_unsupported_attrs:
        tqqiw__bnrt = 'pandas.tseries.offsets.MonthBegin.' + pyfq__wos
        overload_attribute(MonthBeginType, pyfq__wos)(
            create_unsupported_overload(tqqiw__bnrt))
    for pyfq__wos in month_begin_unsupported:
        tqqiw__bnrt = 'pandas.tseries.offsets.MonthBegin.' + pyfq__wos
        overload_method(MonthBeginType, pyfq__wos)(create_unsupported_overload
            (tqqiw__bnrt))


def _install_month_end_unsupported():
    for pyfq__wos in date_offset_unsupported_attrs:
        tqqiw__bnrt = 'pandas.tseries.offsets.MonthEnd.' + pyfq__wos
        overload_attribute(MonthEndType, pyfq__wos)(create_unsupported_overload
            (tqqiw__bnrt))
    for pyfq__wos in date_offset_unsupported:
        tqqiw__bnrt = 'pandas.tseries.offsets.MonthEnd.' + pyfq__wos
        overload_method(MonthEndType, pyfq__wos)(create_unsupported_overload
            (tqqiw__bnrt))


def _install_week_unsupported():
    for pyfq__wos in week_unsupported_attrs:
        tqqiw__bnrt = 'pandas.tseries.offsets.Week.' + pyfq__wos
        overload_attribute(WeekType, pyfq__wos)(create_unsupported_overload
            (tqqiw__bnrt))
    for pyfq__wos in week_unsupported:
        tqqiw__bnrt = 'pandas.tseries.offsets.Week.' + pyfq__wos
        overload_method(WeekType, pyfq__wos)(create_unsupported_overload(
            tqqiw__bnrt))


def _install_offsets_unsupported():
    for smcas__skbnk in offsets_unsupported:
        tqqiw__bnrt = 'pandas.tseries.offsets.' + smcas__skbnk.__name__
        overload(smcas__skbnk)(create_unsupported_overload(tqqiw__bnrt))


def _install_frequencies_unsupported():
    for smcas__skbnk in frequencies_unsupported:
        tqqiw__bnrt = 'pandas.tseries.frequencies.' + smcas__skbnk.__name__
        overload(smcas__skbnk)(create_unsupported_overload(tqqiw__bnrt))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
