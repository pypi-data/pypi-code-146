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
        ihe__fbqrc = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, ihe__fbqrc)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    kejla__ettpe = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ffq__dlv = c.pyapi.long_from_longlong(kejla__ettpe.year)
    wbp__dvh = c.pyapi.long_from_longlong(kejla__ettpe.month)
    eki__gtq = c.pyapi.long_from_longlong(kejla__ettpe.day)
    kgeb__kpr = c.pyapi.long_from_longlong(kejla__ettpe.hour)
    rljb__tkdg = c.pyapi.long_from_longlong(kejla__ettpe.minute)
    tvaw__afzyi = c.pyapi.long_from_longlong(kejla__ettpe.second)
    iry__hvvs = c.pyapi.long_from_longlong(kejla__ettpe.microsecond)
    uxda__snlgd = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    che__lohbg = c.pyapi.call_function_objargs(uxda__snlgd, (ffq__dlv,
        wbp__dvh, eki__gtq, kgeb__kpr, rljb__tkdg, tvaw__afzyi, iry__hvvs))
    c.pyapi.decref(ffq__dlv)
    c.pyapi.decref(wbp__dvh)
    c.pyapi.decref(eki__gtq)
    c.pyapi.decref(kgeb__kpr)
    c.pyapi.decref(rljb__tkdg)
    c.pyapi.decref(tvaw__afzyi)
    c.pyapi.decref(iry__hvvs)
    c.pyapi.decref(uxda__snlgd)
    return che__lohbg


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    ffq__dlv = c.pyapi.object_getattr_string(val, 'year')
    wbp__dvh = c.pyapi.object_getattr_string(val, 'month')
    eki__gtq = c.pyapi.object_getattr_string(val, 'day')
    kgeb__kpr = c.pyapi.object_getattr_string(val, 'hour')
    rljb__tkdg = c.pyapi.object_getattr_string(val, 'minute')
    tvaw__afzyi = c.pyapi.object_getattr_string(val, 'second')
    iry__hvvs = c.pyapi.object_getattr_string(val, 'microsecond')
    kejla__ettpe = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    kejla__ettpe.year = c.pyapi.long_as_longlong(ffq__dlv)
    kejla__ettpe.month = c.pyapi.long_as_longlong(wbp__dvh)
    kejla__ettpe.day = c.pyapi.long_as_longlong(eki__gtq)
    kejla__ettpe.hour = c.pyapi.long_as_longlong(kgeb__kpr)
    kejla__ettpe.minute = c.pyapi.long_as_longlong(rljb__tkdg)
    kejla__ettpe.second = c.pyapi.long_as_longlong(tvaw__afzyi)
    kejla__ettpe.microsecond = c.pyapi.long_as_longlong(iry__hvvs)
    c.pyapi.decref(ffq__dlv)
    c.pyapi.decref(wbp__dvh)
    c.pyapi.decref(eki__gtq)
    c.pyapi.decref(kgeb__kpr)
    c.pyapi.decref(rljb__tkdg)
    c.pyapi.decref(tvaw__afzyi)
    c.pyapi.decref(iry__hvvs)
    nme__xvt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(kejla__ettpe._getvalue(), is_error=nme__xvt)


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
        kejla__ettpe = cgutils.create_struct_proxy(typ)(context, builder)
        kejla__ettpe.year = args[0]
        kejla__ettpe.month = args[1]
        kejla__ettpe.day = args[2]
        kejla__ettpe.hour = args[3]
        kejla__ettpe.minute = args[4]
        kejla__ettpe.second = args[5]
        kejla__ettpe.microsecond = args[6]
        return kejla__ettpe._getvalue()
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
                y, wlzg__ndpf = lhs.year, rhs.year
                unyzf__mry, efql__cbqc = lhs.month, rhs.month
                d, zmmkb__wjiv = lhs.day, rhs.day
                tbe__hntxm, fpnnn__chnz = lhs.hour, rhs.hour
                oon__vdvn, abz__dqa = lhs.minute, rhs.minute
                rrb__cmk, zxp__qddsv = lhs.second, rhs.second
                duei__dqh, vee__ohd = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, unyzf__mry, d, tbe__hntxm, oon__vdvn,
                    rrb__cmk, duei__dqh), (wlzg__ndpf, efql__cbqc,
                    zmmkb__wjiv, fpnnn__chnz, abz__dqa, zxp__qddsv,
                    vee__ohd)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            qexz__ttnl = lhs.toordinal()
            law__sbts = rhs.toordinal()
            bpz__onjl = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            swzeo__fysps = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            iru__mezkf = datetime.timedelta(qexz__ttnl - law__sbts, 
                bpz__onjl - swzeo__fysps, lhs.microsecond - rhs.microsecond)
            return iru__mezkf
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    lbtrb__ugkzp = context.make_helper(builder, fromty, value=val)
    fio__lyj = cgutils.as_bool_bit(builder, lbtrb__ugkzp.valid)
    with builder.if_else(fio__lyj) as (rjx__nojho, mpsge__lgyz):
        with rjx__nojho:
            qtipa__jwu = context.cast(builder, lbtrb__ugkzp.data, fromty.
                type, toty)
            euz__nxqsy = builder.block
        with mpsge__lgyz:
            fksn__dxjz = numba.np.npdatetime.NAT
            lmsc__rduwm = builder.block
    che__lohbg = builder.phi(qtipa__jwu.type)
    che__lohbg.add_incoming(qtipa__jwu, euz__nxqsy)
    che__lohbg.add_incoming(fksn__dxjz, lmsc__rduwm)
    return che__lohbg
