import datetime
import numba
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sjc__uvxgb = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, sjc__uvxgb)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    wvdon__baf = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    yvcoh__ggpw = c.pyapi.long_from_longlong(wvdon__baf.year)
    vdlyt__dwvwk = c.pyapi.long_from_longlong(wvdon__baf.month)
    kkzr__uhiy = c.pyapi.long_from_longlong(wvdon__baf.day)
    wdvth__xgi = c.pyapi.long_from_longlong(wvdon__baf.hour)
    idgp__mzfcw = c.pyapi.long_from_longlong(wvdon__baf.minute)
    nseou__tbr = c.pyapi.long_from_longlong(wvdon__baf.second)
    toywn__ile = c.pyapi.long_from_longlong(wvdon__baf.microsecond)
    ndi__xcw = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime))
    axr__xhpy = c.pyapi.call_function_objargs(ndi__xcw, (yvcoh__ggpw,
        vdlyt__dwvwk, kkzr__uhiy, wdvth__xgi, idgp__mzfcw, nseou__tbr,
        toywn__ile))
    c.pyapi.decref(yvcoh__ggpw)
    c.pyapi.decref(vdlyt__dwvwk)
    c.pyapi.decref(kkzr__uhiy)
    c.pyapi.decref(wdvth__xgi)
    c.pyapi.decref(idgp__mzfcw)
    c.pyapi.decref(nseou__tbr)
    c.pyapi.decref(toywn__ile)
    c.pyapi.decref(ndi__xcw)
    return axr__xhpy


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    yvcoh__ggpw = c.pyapi.object_getattr_string(val, 'year')
    vdlyt__dwvwk = c.pyapi.object_getattr_string(val, 'month')
    kkzr__uhiy = c.pyapi.object_getattr_string(val, 'day')
    wdvth__xgi = c.pyapi.object_getattr_string(val, 'hour')
    idgp__mzfcw = c.pyapi.object_getattr_string(val, 'minute')
    nseou__tbr = c.pyapi.object_getattr_string(val, 'second')
    toywn__ile = c.pyapi.object_getattr_string(val, 'microsecond')
    wvdon__baf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wvdon__baf.year = c.pyapi.long_as_longlong(yvcoh__ggpw)
    wvdon__baf.month = c.pyapi.long_as_longlong(vdlyt__dwvwk)
    wvdon__baf.day = c.pyapi.long_as_longlong(kkzr__uhiy)
    wvdon__baf.hour = c.pyapi.long_as_longlong(wdvth__xgi)
    wvdon__baf.minute = c.pyapi.long_as_longlong(idgp__mzfcw)
    wvdon__baf.second = c.pyapi.long_as_longlong(nseou__tbr)
    wvdon__baf.microsecond = c.pyapi.long_as_longlong(toywn__ile)
    c.pyapi.decref(yvcoh__ggpw)
    c.pyapi.decref(vdlyt__dwvwk)
    c.pyapi.decref(kkzr__uhiy)
    c.pyapi.decref(wdvth__xgi)
    c.pyapi.decref(idgp__mzfcw)
    c.pyapi.decref(nseou__tbr)
    c.pyapi.decref(toywn__ile)
    yry__cfwrb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wvdon__baf._getvalue(), is_error=yry__cfwrb)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    return lir.Constant.literal_struct([year, month, day, hour, minute,
        second, microsecond])


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        wvdon__baf = cgutils.create_struct_proxy(typ)(context, builder)
        wvdon__baf.year = args[0]
        wvdon__baf.month = args[1]
        wvdon__baf.day = args[2]
        wvdon__baf.hour = args[3]
        wvdon__baf.minute = args[4]
        wvdon__baf.second = args[5]
        wvdon__baf.microsecond = args[6]
        return wvdon__baf._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.today()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, ylsty__vzqd = lhs.year, rhs.year
                lovdc__xwxu, rqx__fizx = lhs.month, rhs.month
                d, yjxy__hhs = lhs.day, rhs.day
                ckskq__jugw, jlht__rumu = lhs.hour, rhs.hour
                hqq__zwekj, umf__aky = lhs.minute, rhs.minute
                dhvb__udke, snn__uyo = lhs.second, rhs.second
                rqjai__ixih, srsn__lkynb = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, lovdc__xwxu, d, ckskq__jugw, hqq__zwekj,
                    dhvb__udke, rqjai__ixih), (ylsty__vzqd, rqx__fizx,
                    yjxy__hhs, jlht__rumu, umf__aky, snn__uyo, srsn__lkynb)), 0
                    )
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            cxxwb__xnrcm = lhs.toordinal()
            oir__rksi = rhs.toordinal()
            jqp__rrr = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            wwd__uplww = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            qtty__ziaa = datetime.timedelta(cxxwb__xnrcm - oir__rksi, 
                jqp__rrr - wwd__uplww, lhs.microsecond - rhs.microsecond)
            return qtty__ziaa
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    xstdo__zhoa = context.make_helper(builder, fromty, value=val)
    pgqgt__dqp = cgutils.as_bool_bit(builder, xstdo__zhoa.valid)
    with builder.if_else(pgqgt__dqp) as (dgee__pqv, epag__padv):
        with dgee__pqv:
            cnq__hhpn = context.cast(builder, xstdo__zhoa.data, fromty.type,
                toty)
            fkqhc__rhcau = builder.block
        with epag__padv:
            vzd__abar = numba.np.npdatetime.NAT
            wfr__eil = builder.block
    axr__xhpy = builder.phi(cnq__hhpn.type)
    axr__xhpy.add_incoming(cnq__hhpn, fkqhc__rhcau)
    axr__xhpy.add_incoming(vzd__abar, wfr__eil)
    return axr__xhpy
