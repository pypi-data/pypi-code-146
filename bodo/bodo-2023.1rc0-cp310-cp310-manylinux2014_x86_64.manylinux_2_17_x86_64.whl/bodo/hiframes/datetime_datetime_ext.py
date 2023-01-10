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
        vcmi__qzazs = [('year', types.int64), ('month', types.int64), (
            'day', types.int64), ('hour', types.int64), ('minute', types.
            int64), ('second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, vcmi__qzazs)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    eby__fdf = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    musds__skume = c.pyapi.long_from_longlong(eby__fdf.year)
    xijmr__tcgqb = c.pyapi.long_from_longlong(eby__fdf.month)
    wrof__cvof = c.pyapi.long_from_longlong(eby__fdf.day)
    zeptl__iawm = c.pyapi.long_from_longlong(eby__fdf.hour)
    yhid__nwu = c.pyapi.long_from_longlong(eby__fdf.minute)
    ytt__gork = c.pyapi.long_from_longlong(eby__fdf.second)
    xtg__msnc = c.pyapi.long_from_longlong(eby__fdf.microsecond)
    ccq__xiym = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime)
        )
    qag__nrg = c.pyapi.call_function_objargs(ccq__xiym, (musds__skume,
        xijmr__tcgqb, wrof__cvof, zeptl__iawm, yhid__nwu, ytt__gork, xtg__msnc)
        )
    c.pyapi.decref(musds__skume)
    c.pyapi.decref(xijmr__tcgqb)
    c.pyapi.decref(wrof__cvof)
    c.pyapi.decref(zeptl__iawm)
    c.pyapi.decref(yhid__nwu)
    c.pyapi.decref(ytt__gork)
    c.pyapi.decref(xtg__msnc)
    c.pyapi.decref(ccq__xiym)
    return qag__nrg


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    musds__skume = c.pyapi.object_getattr_string(val, 'year')
    xijmr__tcgqb = c.pyapi.object_getattr_string(val, 'month')
    wrof__cvof = c.pyapi.object_getattr_string(val, 'day')
    zeptl__iawm = c.pyapi.object_getattr_string(val, 'hour')
    yhid__nwu = c.pyapi.object_getattr_string(val, 'minute')
    ytt__gork = c.pyapi.object_getattr_string(val, 'second')
    xtg__msnc = c.pyapi.object_getattr_string(val, 'microsecond')
    eby__fdf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    eby__fdf.year = c.pyapi.long_as_longlong(musds__skume)
    eby__fdf.month = c.pyapi.long_as_longlong(xijmr__tcgqb)
    eby__fdf.day = c.pyapi.long_as_longlong(wrof__cvof)
    eby__fdf.hour = c.pyapi.long_as_longlong(zeptl__iawm)
    eby__fdf.minute = c.pyapi.long_as_longlong(yhid__nwu)
    eby__fdf.second = c.pyapi.long_as_longlong(ytt__gork)
    eby__fdf.microsecond = c.pyapi.long_as_longlong(xtg__msnc)
    c.pyapi.decref(musds__skume)
    c.pyapi.decref(xijmr__tcgqb)
    c.pyapi.decref(wrof__cvof)
    c.pyapi.decref(zeptl__iawm)
    c.pyapi.decref(yhid__nwu)
    c.pyapi.decref(ytt__gork)
    c.pyapi.decref(xtg__msnc)
    tnzf__fxuzi = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(eby__fdf._getvalue(), is_error=tnzf__fxuzi)


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
        eby__fdf = cgutils.create_struct_proxy(typ)(context, builder)
        eby__fdf.year = args[0]
        eby__fdf.month = args[1]
        eby__fdf.day = args[2]
        eby__fdf.hour = args[3]
        eby__fdf.minute = args[4]
        eby__fdf.second = args[5]
        eby__fdf.microsecond = args[6]
        return eby__fdf._getvalue()
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
                y, dpyop__pooh = lhs.year, rhs.year
                wnop__pprfg, pso__cuwvu = lhs.month, rhs.month
                d, ftfbw__cxj = lhs.day, rhs.day
                uvut__vfpyv, rjsk__wgilq = lhs.hour, rhs.hour
                mlkrg__rve, zbcx__lcs = lhs.minute, rhs.minute
                ltra__wpq, ipolo__seac = lhs.second, rhs.second
                umet__eqjms, uswu__rgapy = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, wnop__pprfg, d, uvut__vfpyv, mlkrg__rve,
                    ltra__wpq, umet__eqjms), (dpyop__pooh, pso__cuwvu,
                    ftfbw__cxj, rjsk__wgilq, zbcx__lcs, ipolo__seac,
                    uswu__rgapy)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            ptab__iexui = lhs.toordinal()
            vggs__yclk = rhs.toordinal()
            sgqol__bay = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            qub__zcrws = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            lab__ffcr = datetime.timedelta(ptab__iexui - vggs__yclk, 
                sgqol__bay - qub__zcrws, lhs.microsecond - rhs.microsecond)
            return lab__ffcr
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    omhwb__zbw = context.make_helper(builder, fromty, value=val)
    zmz__cod = cgutils.as_bool_bit(builder, omhwb__zbw.valid)
    with builder.if_else(zmz__cod) as (xiind__zunn, jjwz__xeili):
        with xiind__zunn:
            cphe__twp = context.cast(builder, omhwb__zbw.data, fromty.type,
                toty)
            ecar__xzyqq = builder.block
        with jjwz__xeili:
            smo__fsxbt = numba.np.npdatetime.NAT
            ftqnv__qhhir = builder.block
    qag__nrg = builder.phi(cphe__twp.type)
    qag__nrg.add_incoming(cphe__twp, ecar__xzyqq)
    qag__nrg.add_incoming(smo__fsxbt, ftqnv__qhhir)
    return qag__nrg
