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
        ljs__ycc = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, ljs__ycc)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    wrhy__vsa = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    dhu__dtkfh = c.pyapi.long_from_longlong(wrhy__vsa.year)
    hnti__jqnp = c.pyapi.long_from_longlong(wrhy__vsa.month)
    yhj__utx = c.pyapi.long_from_longlong(wrhy__vsa.day)
    rpd__ffh = c.pyapi.long_from_longlong(wrhy__vsa.hour)
    xgu__oprp = c.pyapi.long_from_longlong(wrhy__vsa.minute)
    dxh__mzt = c.pyapi.long_from_longlong(wrhy__vsa.second)
    qegqz__diwki = c.pyapi.long_from_longlong(wrhy__vsa.microsecond)
    dcgu__lkj = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime)
        )
    gta__zfw = c.pyapi.call_function_objargs(dcgu__lkj, (dhu__dtkfh,
        hnti__jqnp, yhj__utx, rpd__ffh, xgu__oprp, dxh__mzt, qegqz__diwki))
    c.pyapi.decref(dhu__dtkfh)
    c.pyapi.decref(hnti__jqnp)
    c.pyapi.decref(yhj__utx)
    c.pyapi.decref(rpd__ffh)
    c.pyapi.decref(xgu__oprp)
    c.pyapi.decref(dxh__mzt)
    c.pyapi.decref(qegqz__diwki)
    c.pyapi.decref(dcgu__lkj)
    return gta__zfw


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    dhu__dtkfh = c.pyapi.object_getattr_string(val, 'year')
    hnti__jqnp = c.pyapi.object_getattr_string(val, 'month')
    yhj__utx = c.pyapi.object_getattr_string(val, 'day')
    rpd__ffh = c.pyapi.object_getattr_string(val, 'hour')
    xgu__oprp = c.pyapi.object_getattr_string(val, 'minute')
    dxh__mzt = c.pyapi.object_getattr_string(val, 'second')
    qegqz__diwki = c.pyapi.object_getattr_string(val, 'microsecond')
    wrhy__vsa = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wrhy__vsa.year = c.pyapi.long_as_longlong(dhu__dtkfh)
    wrhy__vsa.month = c.pyapi.long_as_longlong(hnti__jqnp)
    wrhy__vsa.day = c.pyapi.long_as_longlong(yhj__utx)
    wrhy__vsa.hour = c.pyapi.long_as_longlong(rpd__ffh)
    wrhy__vsa.minute = c.pyapi.long_as_longlong(xgu__oprp)
    wrhy__vsa.second = c.pyapi.long_as_longlong(dxh__mzt)
    wrhy__vsa.microsecond = c.pyapi.long_as_longlong(qegqz__diwki)
    c.pyapi.decref(dhu__dtkfh)
    c.pyapi.decref(hnti__jqnp)
    c.pyapi.decref(yhj__utx)
    c.pyapi.decref(rpd__ffh)
    c.pyapi.decref(xgu__oprp)
    c.pyapi.decref(dxh__mzt)
    c.pyapi.decref(qegqz__diwki)
    nsry__lutij = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wrhy__vsa._getvalue(), is_error=nsry__lutij)


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
        wrhy__vsa = cgutils.create_struct_proxy(typ)(context, builder)
        wrhy__vsa.year = args[0]
        wrhy__vsa.month = args[1]
        wrhy__vsa.day = args[2]
        wrhy__vsa.hour = args[3]
        wrhy__vsa.minute = args[4]
        wrhy__vsa.second = args[5]
        wrhy__vsa.microsecond = args[6]
        return wrhy__vsa._getvalue()
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
                y, fiu__xovu = lhs.year, rhs.year
                regc__utksg, zya__kooqj = lhs.month, rhs.month
                d, shn__fdj = lhs.day, rhs.day
                nvopy__ffc, fwidl__sygp = lhs.hour, rhs.hour
                vbgu__dcwc, goq__kxk = lhs.minute, rhs.minute
                gnt__zylq, wtyse__bjfv = lhs.second, rhs.second
                sxi__lccy, bzoiw__ryx = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, regc__utksg, d, nvopy__ffc, vbgu__dcwc,
                    gnt__zylq, sxi__lccy), (fiu__xovu, zya__kooqj, shn__fdj,
                    fwidl__sygp, goq__kxk, wtyse__bjfv, bzoiw__ryx)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            bqt__cgoz = lhs.toordinal()
            usm__omzmf = rhs.toordinal()
            rof__zvz = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            bie__fntp = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            meee__kavos = datetime.timedelta(bqt__cgoz - usm__omzmf, 
                rof__zvz - bie__fntp, lhs.microsecond - rhs.microsecond)
            return meee__kavos
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    fbzzu__dqlgd = context.make_helper(builder, fromty, value=val)
    unah__gnroy = cgutils.as_bool_bit(builder, fbzzu__dqlgd.valid)
    with builder.if_else(unah__gnroy) as (oaze__igdk, kimb__bqlkm):
        with oaze__igdk:
            hynvq__wmmlz = context.cast(builder, fbzzu__dqlgd.data, fromty.
                type, toty)
            rfzfk__fxf = builder.block
        with kimb__bqlkm:
            tauc__oifvf = numba.np.npdatetime.NAT
            zqx__ajb = builder.block
    gta__zfw = builder.phi(hynvq__wmmlz.type)
    gta__zfw.add_incoming(hynvq__wmmlz, rfzfk__fxf)
    gta__zfw.add_incoming(tauc__oifvf, zqx__ajb)
    return gta__zfw
