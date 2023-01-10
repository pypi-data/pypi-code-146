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
        yja__iku = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, yja__iku)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    valpx__rgmie = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    bec__sfpqh = c.pyapi.long_from_longlong(valpx__rgmie.n)
    knin__xqlgm = c.pyapi.from_native_value(types.boolean, valpx__rgmie.
        normalize, c.env_manager)
    mklq__psji = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    sth__damg = c.pyapi.call_function_objargs(mklq__psji, (bec__sfpqh,
        knin__xqlgm))
    c.pyapi.decref(bec__sfpqh)
    c.pyapi.decref(knin__xqlgm)
    c.pyapi.decref(mklq__psji)
    return sth__damg


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    bec__sfpqh = c.pyapi.object_getattr_string(val, 'n')
    knin__xqlgm = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(bec__sfpqh)
    normalize = c.pyapi.to_native_value(types.bool_, knin__xqlgm).value
    valpx__rgmie = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    valpx__rgmie.n = n
    valpx__rgmie.normalize = normalize
    c.pyapi.decref(bec__sfpqh)
    c.pyapi.decref(knin__xqlgm)
    bnio__naluh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(valpx__rgmie._getvalue(), is_error=bnio__naluh)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        valpx__rgmie = cgutils.create_struct_proxy(typ)(context, builder)
        valpx__rgmie.n = args[0]
        valpx__rgmie.normalize = args[1]
        return valpx__rgmie._getvalue()
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
        qbo__nvkux = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    qbo__nvkux)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=qbo__nvkux)
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
        yja__iku = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, yja__iku)


@box(MonthEndType)
def box_month_end(typ, val, c):
    hdlu__gigiq = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    bec__sfpqh = c.pyapi.long_from_longlong(hdlu__gigiq.n)
    knin__xqlgm = c.pyapi.from_native_value(types.boolean, hdlu__gigiq.
        normalize, c.env_manager)
    euodk__tplm = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    sth__damg = c.pyapi.call_function_objargs(euodk__tplm, (bec__sfpqh,
        knin__xqlgm))
    c.pyapi.decref(bec__sfpqh)
    c.pyapi.decref(knin__xqlgm)
    c.pyapi.decref(euodk__tplm)
    return sth__damg


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    bec__sfpqh = c.pyapi.object_getattr_string(val, 'n')
    knin__xqlgm = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(bec__sfpqh)
    normalize = c.pyapi.to_native_value(types.bool_, knin__xqlgm).value
    hdlu__gigiq = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hdlu__gigiq.n = n
    hdlu__gigiq.normalize = normalize
    c.pyapi.decref(bec__sfpqh)
    c.pyapi.decref(knin__xqlgm)
    bnio__naluh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hdlu__gigiq._getvalue(), is_error=bnio__naluh)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        hdlu__gigiq = cgutils.create_struct_proxy(typ)(context, builder)
        hdlu__gigiq.n = args[0]
        hdlu__gigiq.normalize = args[1]
        return hdlu__gigiq._getvalue()
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
        hdlu__gigiq = get_days_in_month(year, month)
        if hdlu__gigiq > day:
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
        qbo__nvkux = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    qbo__nvkux)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=qbo__nvkux)
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
        yja__iku = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, yja__iku)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    acz__bwerm = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    volq__evqw = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for kjqri__hyd, igk__rxsp in enumerate(date_offset_fields):
        c.builder.store(getattr(acz__bwerm, igk__rxsp), c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(volq__evqw, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * kjqri__hyd)), lir.IntType(64)
            .as_pointer()))
    ldt__qnt = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    cppg__qqh = cgutils.get_or_insert_function(c.builder.module, ldt__qnt,
        name='box_date_offset')
    tvmm__wbb = c.builder.call(cppg__qqh, [acz__bwerm.n, acz__bwerm.
        normalize, volq__evqw, acz__bwerm.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return tvmm__wbb


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    bec__sfpqh = c.pyapi.object_getattr_string(val, 'n')
    knin__xqlgm = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(bec__sfpqh)
    normalize = c.pyapi.to_native_value(types.bool_, knin__xqlgm).value
    volq__evqw = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    ldt__qnt = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer(
        ), lir.IntType(64).as_pointer()])
    nnaj__gmhmo = cgutils.get_or_insert_function(c.builder.module, ldt__qnt,
        name='unbox_date_offset')
    has_kws = c.builder.call(nnaj__gmhmo, [val, volq__evqw])
    acz__bwerm = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    acz__bwerm.n = n
    acz__bwerm.normalize = normalize
    for kjqri__hyd, igk__rxsp in enumerate(date_offset_fields):
        setattr(acz__bwerm, igk__rxsp, c.builder.load(c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(volq__evqw, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * kjqri__hyd)), lir.IntType(64)
            .as_pointer())))
    acz__bwerm.has_kws = has_kws
    c.pyapi.decref(bec__sfpqh)
    c.pyapi.decref(knin__xqlgm)
    bnio__naluh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(acz__bwerm._getvalue(), is_error=bnio__naluh)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    scb__ecdpv = [n, normalize]
    has_kws = False
    sksf__qxcb = [0] * 9 + [-1] * 9
    for kjqri__hyd, igk__rxsp in enumerate(date_offset_fields):
        if hasattr(pyval, igk__rxsp):
            wsjj__cfxda = context.get_constant(types.int64, getattr(pyval,
                igk__rxsp))
            has_kws = True
        else:
            wsjj__cfxda = context.get_constant(types.int64, sksf__qxcb[
                kjqri__hyd])
        scb__ecdpv.append(wsjj__cfxda)
    has_kws = context.get_constant(types.boolean, has_kws)
    scb__ecdpv.append(has_kws)
    return lir.Constant.literal_struct(scb__ecdpv)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    usguu__sbx = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for dcv__axc in usguu__sbx:
        if not is_overload_none(dcv__axc):
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
        acz__bwerm = cgutils.create_struct_proxy(typ)(context, builder)
        acz__bwerm.n = args[0]
        acz__bwerm.normalize = args[1]
        acz__bwerm.years = args[2]
        acz__bwerm.months = args[3]
        acz__bwerm.weeks = args[4]
        acz__bwerm.days = args[5]
        acz__bwerm.hours = args[6]
        acz__bwerm.minutes = args[7]
        acz__bwerm.seconds = args[8]
        acz__bwerm.microseconds = args[9]
        acz__bwerm.nanoseconds = args[10]
        acz__bwerm.year = args[11]
        acz__bwerm.month = args[12]
        acz__bwerm.day = args[13]
        acz__bwerm.weekday = args[14]
        acz__bwerm.hour = args[15]
        acz__bwerm.minute = args[16]
        acz__bwerm.second = args[17]
        acz__bwerm.microsecond = args[18]
        acz__bwerm.nanosecond = args[19]
        acz__bwerm.has_kws = args[20]
        return acz__bwerm._getvalue()
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
        arhi__tyxch = -1 if dateoffset.n < 0 else 1
        for islna__skfu in range(np.abs(dateoffset.n)):
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
            year += arhi__tyxch * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += arhi__tyxch * dateoffset._months
            year, month, osjwi__oqioy = calculate_month_end_date(year,
                month, day, 0)
            if day > osjwi__oqioy:
                day = osjwi__oqioy
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
            if arhi__tyxch == -1:
                td = -td
            ts = ts + td
            if dateoffset._weekday != -1:
                rnw__uqhqr = ts.weekday()
                kpvnr__szr = (dateoffset._weekday - rnw__uqhqr) % 7
                ts = ts + pd.Timedelta(days=kpvnr__szr)
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
        yja__iku = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, yja__iku)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        izxru__gdrg = -1 if weekday is None else weekday
        return init_week(n, normalize, izxru__gdrg)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        zhkmv__nykfa = cgutils.create_struct_proxy(typ)(context, builder)
        zhkmv__nykfa.n = args[0]
        zhkmv__nykfa.normalize = args[1]
        zhkmv__nykfa.weekday = args[2]
        return zhkmv__nykfa._getvalue()
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
    zhkmv__nykfa = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    bec__sfpqh = c.pyapi.long_from_longlong(zhkmv__nykfa.n)
    knin__xqlgm = c.pyapi.from_native_value(types.boolean, zhkmv__nykfa.
        normalize, c.env_manager)
    galfl__zdra = c.pyapi.long_from_longlong(zhkmv__nykfa.weekday)
    vfv__hglp = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    cpv__auqaa = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), 
        -1), zhkmv__nykfa.weekday)
    with c.builder.if_else(cpv__auqaa) as (ddqta__iifxq, knb__ion):
        with ddqta__iifxq:
            cdybn__tgj = c.pyapi.call_function_objargs(vfv__hglp, (
                bec__sfpqh, knin__xqlgm, galfl__zdra))
            ven__lhwd = c.builder.block
        with knb__ion:
            vqd__wxoud = c.pyapi.call_function_objargs(vfv__hglp, (
                bec__sfpqh, knin__xqlgm))
            atfgw__oinx = c.builder.block
    sth__damg = c.builder.phi(cdybn__tgj.type)
    sth__damg.add_incoming(cdybn__tgj, ven__lhwd)
    sth__damg.add_incoming(vqd__wxoud, atfgw__oinx)
    c.pyapi.decref(galfl__zdra)
    c.pyapi.decref(bec__sfpqh)
    c.pyapi.decref(knin__xqlgm)
    c.pyapi.decref(vfv__hglp)
    return sth__damg


@unbox(WeekType)
def unbox_week(typ, val, c):
    bec__sfpqh = c.pyapi.object_getattr_string(val, 'n')
    knin__xqlgm = c.pyapi.object_getattr_string(val, 'normalize')
    galfl__zdra = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(bec__sfpqh)
    normalize = c.pyapi.to_native_value(types.bool_, knin__xqlgm).value
    hjqj__btviq = c.pyapi.make_none()
    xtlay__acc = c.builder.icmp_unsigned('==', galfl__zdra, hjqj__btviq)
    with c.builder.if_else(xtlay__acc) as (knb__ion, ddqta__iifxq):
        with ddqta__iifxq:
            cdybn__tgj = c.pyapi.long_as_longlong(galfl__zdra)
            ven__lhwd = c.builder.block
        with knb__ion:
            vqd__wxoud = lir.Constant(lir.IntType(64), -1)
            atfgw__oinx = c.builder.block
    sth__damg = c.builder.phi(cdybn__tgj.type)
    sth__damg.add_incoming(cdybn__tgj, ven__lhwd)
    sth__damg.add_incoming(vqd__wxoud, atfgw__oinx)
    zhkmv__nykfa = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zhkmv__nykfa.n = n
    zhkmv__nykfa.normalize = normalize
    zhkmv__nykfa.weekday = sth__damg
    c.pyapi.decref(bec__sfpqh)
    c.pyapi.decref(knin__xqlgm)
    c.pyapi.decref(galfl__zdra)
    bnio__naluh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zhkmv__nykfa._getvalue(), is_error=bnio__naluh)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and isinstance(rhs, PandasTimestampType):

        def impl(lhs, rhs):
            if lhs.normalize:
                gov__wiqv = rhs.normalize()
            else:
                gov__wiqv = rhs
            asxfk__uos = calculate_week_date(lhs.n, lhs.weekday, gov__wiqv)
            return gov__wiqv + asxfk__uos
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            if lhs.normalize:
                gov__wiqv = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                gov__wiqv = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            asxfk__uos = calculate_week_date(lhs.n, lhs.weekday, gov__wiqv)
            return gov__wiqv + asxfk__uos
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            asxfk__uos = calculate_week_date(lhs.n, lhs.weekday, rhs)
            return rhs + asxfk__uos
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
                hgv__bwzu = input_date_or_ts.weekday()
                if weekday != hgv__bwzu:
                    pxf__vaq = (weekday - hgv__bwzu) % 7
                    if n > 0:
                        n = n - 1
                td = pd.Timedelta(weeks=n, days=pxf__vaq)
            return update_timedelta_with_transition(input_date_or_ts, td)
        return impl_tz_aware
    else:

        def impl(n, weekday, input_date_or_ts):
            if weekday == -1:
                return pd.Timedelta(weeks=n)
            hgv__bwzu = input_date_or_ts.weekday()
            if weekday != hgv__bwzu:
                pxf__vaq = (weekday - hgv__bwzu) % 7
                if n > 0:
                    n = n - 1
            return pd.Timedelta(weeks=n, days=pxf__vaq)
        return impl


def update_timedelta_with_transition(ts_value, timedelta):
    pass


@overload(update_timedelta_with_transition)
def overload_update_timedelta_with_transition(ts, td):
    if tz_has_transition_times(ts.tz):
        zut__mdb = pytz.timezone(ts.tz)
        dal__nqqg = np.array(zut__mdb._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        haqeb__nll = np.array(zut__mdb._transition_info)[:, 0]
        haqeb__nll = (pd.Series(haqeb__nll).dt.total_seconds() * 1000000000
            ).astype(np.int64).values

        def impl_tz_aware(ts, td):
            qhk__imz = ts.value
            nqx__rbwo = qhk__imz + td.value
            nlkd__cvzq = np.searchsorted(dal__nqqg, qhk__imz, side='right') - 1
            oidt__ejxd = np.searchsorted(dal__nqqg, nqx__rbwo, side='right'
                ) - 1
            pxf__vaq = haqeb__nll[nlkd__cvzq] - haqeb__nll[oidt__ejxd]
            return pd.Timedelta(td.value + pxf__vaq)
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
    for kerso__icvcn in date_offset_unsupported_attrs:
        oxf__ovsnm = 'pandas.tseries.offsets.DateOffset.' + kerso__icvcn
        overload_attribute(DateOffsetType, kerso__icvcn)(
            create_unsupported_overload(oxf__ovsnm))
    for kerso__icvcn in date_offset_unsupported:
        oxf__ovsnm = 'pandas.tseries.offsets.DateOffset.' + kerso__icvcn
        overload_method(DateOffsetType, kerso__icvcn)(
            create_unsupported_overload(oxf__ovsnm))


def _install_month_begin_unsupported():
    for kerso__icvcn in month_begin_unsupported_attrs:
        oxf__ovsnm = 'pandas.tseries.offsets.MonthBegin.' + kerso__icvcn
        overload_attribute(MonthBeginType, kerso__icvcn)(
            create_unsupported_overload(oxf__ovsnm))
    for kerso__icvcn in month_begin_unsupported:
        oxf__ovsnm = 'pandas.tseries.offsets.MonthBegin.' + kerso__icvcn
        overload_method(MonthBeginType, kerso__icvcn)(
            create_unsupported_overload(oxf__ovsnm))


def _install_month_end_unsupported():
    for kerso__icvcn in date_offset_unsupported_attrs:
        oxf__ovsnm = 'pandas.tseries.offsets.MonthEnd.' + kerso__icvcn
        overload_attribute(MonthEndType, kerso__icvcn)(
            create_unsupported_overload(oxf__ovsnm))
    for kerso__icvcn in date_offset_unsupported:
        oxf__ovsnm = 'pandas.tseries.offsets.MonthEnd.' + kerso__icvcn
        overload_method(MonthEndType, kerso__icvcn)(create_unsupported_overload
            (oxf__ovsnm))


def _install_week_unsupported():
    for kerso__icvcn in week_unsupported_attrs:
        oxf__ovsnm = 'pandas.tseries.offsets.Week.' + kerso__icvcn
        overload_attribute(WeekType, kerso__icvcn)(create_unsupported_overload
            (oxf__ovsnm))
    for kerso__icvcn in week_unsupported:
        oxf__ovsnm = 'pandas.tseries.offsets.Week.' + kerso__icvcn
        overload_method(WeekType, kerso__icvcn)(create_unsupported_overload
            (oxf__ovsnm))


def _install_offsets_unsupported():
    for wsjj__cfxda in offsets_unsupported:
        oxf__ovsnm = 'pandas.tseries.offsets.' + wsjj__cfxda.__name__
        overload(wsjj__cfxda)(create_unsupported_overload(oxf__ovsnm))


def _install_frequencies_unsupported():
    for wsjj__cfxda in frequencies_unsupported:
        oxf__ovsnm = 'pandas.tseries.frequencies.' + wsjj__cfxda.__name__
        overload(wsjj__cfxda)(create_unsupported_overload(oxf__ovsnm))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
