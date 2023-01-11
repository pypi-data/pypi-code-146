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
        ciu__jyglj = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, ciu__jyglj)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    lqy__zejo = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    stadr__piydt = c.pyapi.long_from_longlong(lqy__zejo.year)
    lunk__oowzb = c.pyapi.long_from_longlong(lqy__zejo.month)
    ijg__bvbn = c.pyapi.long_from_longlong(lqy__zejo.day)
    wykgb__eidqj = c.pyapi.long_from_longlong(lqy__zejo.hour)
    lwzkc__tgpj = c.pyapi.long_from_longlong(lqy__zejo.minute)
    xqcwn__krmgq = c.pyapi.long_from_longlong(lqy__zejo.second)
    ikjt__mivg = c.pyapi.long_from_longlong(lqy__zejo.microsecond)
    osvm__ogtgf = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    julmt__zsc = c.pyapi.call_function_objargs(osvm__ogtgf, (stadr__piydt,
        lunk__oowzb, ijg__bvbn, wykgb__eidqj, lwzkc__tgpj, xqcwn__krmgq,
        ikjt__mivg))
    c.pyapi.decref(stadr__piydt)
    c.pyapi.decref(lunk__oowzb)
    c.pyapi.decref(ijg__bvbn)
    c.pyapi.decref(wykgb__eidqj)
    c.pyapi.decref(lwzkc__tgpj)
    c.pyapi.decref(xqcwn__krmgq)
    c.pyapi.decref(ikjt__mivg)
    c.pyapi.decref(osvm__ogtgf)
    return julmt__zsc


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    stadr__piydt = c.pyapi.object_getattr_string(val, 'year')
    lunk__oowzb = c.pyapi.object_getattr_string(val, 'month')
    ijg__bvbn = c.pyapi.object_getattr_string(val, 'day')
    wykgb__eidqj = c.pyapi.object_getattr_string(val, 'hour')
    lwzkc__tgpj = c.pyapi.object_getattr_string(val, 'minute')
    xqcwn__krmgq = c.pyapi.object_getattr_string(val, 'second')
    ikjt__mivg = c.pyapi.object_getattr_string(val, 'microsecond')
    lqy__zejo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lqy__zejo.year = c.pyapi.long_as_longlong(stadr__piydt)
    lqy__zejo.month = c.pyapi.long_as_longlong(lunk__oowzb)
    lqy__zejo.day = c.pyapi.long_as_longlong(ijg__bvbn)
    lqy__zejo.hour = c.pyapi.long_as_longlong(wykgb__eidqj)
    lqy__zejo.minute = c.pyapi.long_as_longlong(lwzkc__tgpj)
    lqy__zejo.second = c.pyapi.long_as_longlong(xqcwn__krmgq)
    lqy__zejo.microsecond = c.pyapi.long_as_longlong(ikjt__mivg)
    c.pyapi.decref(stadr__piydt)
    c.pyapi.decref(lunk__oowzb)
    c.pyapi.decref(ijg__bvbn)
    c.pyapi.decref(wykgb__eidqj)
    c.pyapi.decref(lwzkc__tgpj)
    c.pyapi.decref(xqcwn__krmgq)
    c.pyapi.decref(ikjt__mivg)
    ybxc__zgz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lqy__zejo._getvalue(), is_error=ybxc__zgz)


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
        lqy__zejo = cgutils.create_struct_proxy(typ)(context, builder)
        lqy__zejo.year = args[0]
        lqy__zejo.month = args[1]
        lqy__zejo.day = args[2]
        lqy__zejo.hour = args[3]
        lqy__zejo.minute = args[4]
        lqy__zejo.second = args[5]
        lqy__zejo.microsecond = args[6]
        return lqy__zejo._getvalue()
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
                y, uoayf__abw = lhs.year, rhs.year
                fnsrp__qdj, chhn__xxb = lhs.month, rhs.month
                d, yzixv__sgzn = lhs.day, rhs.day
                ujg__hbrc, aimr__nvl = lhs.hour, rhs.hour
                iywly__riw, vocve__aabl = lhs.minute, rhs.minute
                oddhb__emq, mvvx__paxin = lhs.second, rhs.second
                paizx__bwfep, lqddu__wwjsq = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, fnsrp__qdj, d, ujg__hbrc, iywly__riw,
                    oddhb__emq, paizx__bwfep), (uoayf__abw, chhn__xxb,
                    yzixv__sgzn, aimr__nvl, vocve__aabl, mvvx__paxin,
                    lqddu__wwjsq)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            mmy__ljao = lhs.toordinal()
            ysdyi__sbdui = rhs.toordinal()
            vap__fphvl = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            epq__dyds = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            iat__jlqpu = datetime.timedelta(mmy__ljao - ysdyi__sbdui, 
                vap__fphvl - epq__dyds, lhs.microsecond - rhs.microsecond)
            return iat__jlqpu
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    vwb__rgcvi = context.make_helper(builder, fromty, value=val)
    tjsya__buudb = cgutils.as_bool_bit(builder, vwb__rgcvi.valid)
    with builder.if_else(tjsya__buudb) as (zuoue__zrwro, vqr__drxy):
        with zuoue__zrwro:
            onz__bqj = context.cast(builder, vwb__rgcvi.data, fromty.type, toty
                )
            dcg__ubj = builder.block
        with vqr__drxy:
            xbvd__svuq = numba.np.npdatetime.NAT
            teq__mpsy = builder.block
    julmt__zsc = builder.phi(onz__bqj.type)
    julmt__zsc.add_incoming(onz__bqj, dcg__ubj)
    julmt__zsc.add_incoming(xbvd__svuq, teq__mpsy)
    return julmt__zsc
