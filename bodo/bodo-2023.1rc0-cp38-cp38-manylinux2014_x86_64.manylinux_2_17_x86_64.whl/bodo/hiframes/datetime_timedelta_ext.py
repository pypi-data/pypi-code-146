"""Numba extension support for datetime.timedelta objects and their arrays.
"""
import datetime
import operator
from collections import namedtuple
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import get_new_null_mask_bool_index, get_new_null_mask_int_index, get_new_null_mask_slice_index, setitem_slice_index_null_bits
from bodo.utils.typing import BodoError, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_str
ll.add_symbol('box_datetime_timedelta_array', hdatetime_ext.
    box_datetime_timedelta_array)
ll.add_symbol('unbox_datetime_timedelta_array', hdatetime_ext.
    unbox_datetime_timedelta_array)


class NoInput:
    pass


_no_input = NoInput()


class NoInputType(types.Type):

    def __init__(self):
        super(NoInputType, self).__init__(name='NoInput')


register_model(NoInputType)(models.OpaqueModel)


@typeof_impl.register(NoInput)
def _typ_no_input(val, c):
    return NoInputType()


@lower_constant(NoInputType)
def constant_no_input(context, builder, ty, pyval):
    return context.get_dummy_value()


class PDTimeDeltaType(types.Type):

    def __init__(self):
        super(PDTimeDeltaType, self).__init__(name='PDTimeDeltaType()')


pd_timedelta_type = PDTimeDeltaType()
types.pd_timedelta_type = pd_timedelta_type


@typeof_impl.register(pd.Timedelta)
def typeof_pd_timedelta(val, c):
    return pd_timedelta_type


@register_model(PDTimeDeltaType)
class PDTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xjnyt__eyzbp = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, xjnyt__eyzbp)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    oehyo__ficyk = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    qfkh__vxyq = c.pyapi.long_from_longlong(oehyo__ficyk.value)
    bbx__nuwbp = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(bbx__nuwbp, (qfkh__vxyq,))
    c.pyapi.decref(qfkh__vxyq)
    c.pyapi.decref(bbx__nuwbp)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    qfkh__vxyq = c.pyapi.object_getattr_string(val, 'value')
    fxzrf__ptsi = c.pyapi.long_as_longlong(qfkh__vxyq)
    oehyo__ficyk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oehyo__ficyk.value = fxzrf__ptsi
    c.pyapi.decref(qfkh__vxyq)
    dcx__lmt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oehyo__ficyk._getvalue(), is_error=dcx__lmt)


@lower_constant(PDTimeDeltaType)
def lower_constant_pd_timedelta(context, builder, ty, pyval):
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct([value])


@overload(pd.Timedelta, no_unliteral=True)
def pd_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
    microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    if value == _no_input:

        def impl_timedelta_kw(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            days += weeks * 7
            hours += days * 24
            minutes += 60 * hours
            seconds += 60 * minutes
            milliseconds += 1000 * seconds
            microseconds += 1000 * milliseconds
            hphl__xlyx = 1000 * microseconds
            return init_pd_timedelta(hphl__xlyx)
        return impl_timedelta_kw
    if value == bodo.string_type or is_overload_constant_str(value):

        def impl_str(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            with numba.objmode(res='pd_timedelta_type'):
                res = pd.Timedelta(value)
            return res
        return impl_str
    if value == pd_timedelta_type:
        return (lambda value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0: value)
    if value == datetime_timedelta_type:

        def impl_timedelta_datetime(value=_no_input, unit='ns', days=0,
            seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
            weeks=0):
            days = value.days
            seconds = 60 * 60 * 24 * days + value.seconds
            microseconds = 1000 * 1000 * seconds + value.microseconds
            hphl__xlyx = 1000 * microseconds
            return init_pd_timedelta(hphl__xlyx)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    dutt__nrcmp, jqhzm__ytsi = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * dutt__nrcmp)
    return impl_timedelta


@intrinsic
def init_pd_timedelta(typingctx, value):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.value = args[0]
        return timedelta._getvalue()
    return PDTimeDeltaType()(value), codegen


make_attribute_wrapper(PDTimeDeltaType, 'value', '_value')


@overload_attribute(PDTimeDeltaType, 'value')
@overload_attribute(PDTimeDeltaType, 'delta')
def pd_timedelta_get_value(td):

    def impl(td):
        return td._value
    return impl


@overload_attribute(PDTimeDeltaType, 'days')
def pd_timedelta_get_days(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000 * 60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'seconds')
def pd_timedelta_get_seconds(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000) % (60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'microseconds')
def pd_timedelta_get_microseconds(td):

    def impl(td):
        return td._value // 1000 % 1000000
    return impl


@overload_attribute(PDTimeDeltaType, 'nanoseconds')
def pd_timedelta_get_nanoseconds(td):

    def impl(td):
        return td._value % 1000
    return impl


@register_jitable
def _to_hours_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60 * 60) % 24


@register_jitable
def _to_minutes_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60) % 60


@register_jitable
def _to_seconds_pd_td(td):
    return td._value // (1000 * 1000 * 1000) % 60


@register_jitable
def _to_milliseconds_pd_td(td):
    return td._value // (1000 * 1000) % 1000


@register_jitable
def _to_microseconds_pd_td(td):
    return td._value // 1000 % 1000


Components = namedtuple('Components', ['days', 'hours', 'minutes',
    'seconds', 'milliseconds', 'microseconds', 'nanoseconds'], defaults=[0,
    0, 0, 0, 0, 0, 0])


@overload_attribute(PDTimeDeltaType, 'components', no_unliteral=True)
def pd_timedelta_get_components(td):

    def impl(td):
        a = Components(td.days, _to_hours_pd_td(td), _to_minutes_pd_td(td),
            _to_seconds_pd_td(td), _to_milliseconds_pd_td(td),
            _to_microseconds_pd_td(td), td.nanoseconds)
        return a
    return impl


@overload_method(PDTimeDeltaType, '__hash__', no_unliteral=True)
def pd_td___hash__(td):

    def impl(td):
        return hash(td._value)
    return impl


@overload_method(PDTimeDeltaType, 'to_numpy', no_unliteral=True)
@overload_method(PDTimeDeltaType, 'to_timedelta64', no_unliteral=True)
def pd_td_to_numpy(td):
    from bodo.hiframes.pd_timestamp_ext import integer_to_timedelta64

    def impl(td):
        return integer_to_timedelta64(td.value)
    return impl


@overload_method(PDTimeDeltaType, 'to_pytimedelta', no_unliteral=True)
def pd_td_to_pytimedelta(td):

    def impl(td):
        return datetime.timedelta(microseconds=np.int64(td._value / 1000))
    return impl


@overload_method(PDTimeDeltaType, 'total_seconds', no_unliteral=True)
def pd_td_total_seconds(td):

    def impl(td):
        return td._value // 1000 / 10 ** 6
    return impl


def overload_add_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            val = lhs.value + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            qzahe__unb = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + qzahe__unb
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            dqj__xdqw = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = dqj__xdqw + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            dnhh__vutul = rhs.toordinal()
            iqrqe__wgc = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            akru__cpisp = rhs.microsecond
            ciycm__thdr = lhs.value // 1000
            eqsrh__tbiy = lhs.nanoseconds
            eulf__hlj = akru__cpisp + ciycm__thdr
            hmwx__pjeyk = 1000000 * (dnhh__vutul * 86400 + iqrqe__wgc
                ) + eulf__hlj
            tywpi__ede = eqsrh__tbiy
            return compute_pd_timestamp(hmwx__pjeyk, tywpi__ede)
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + rhs.to_pytimedelta()
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days + rhs.days
            s = lhs.seconds + rhs.seconds
            us = lhs.microseconds + rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            qdh__udh = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            qdh__udh = qdh__udh + lhs
            dgcd__hyp, jipd__ewf = divmod(qdh__udh.seconds, 3600)
            bzs__kwajm, xunkm__jwki = divmod(jipd__ewf, 60)
            if 0 < qdh__udh.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(qdh__udh
                    .days)
                return datetime.datetime(d.year, d.month, d.day, dgcd__hyp,
                    bzs__kwajm, xunkm__jwki, qdh__udh.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            qdh__udh = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            qdh__udh = qdh__udh + rhs
            dgcd__hyp, jipd__ewf = divmod(qdh__udh.seconds, 3600)
            bzs__kwajm, xunkm__jwki = divmod(jipd__ewf, 60)
            if 0 < qdh__udh.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(qdh__udh
                    .days)
                return datetime.datetime(d.year, d.month, d.day, dgcd__hyp,
                    bzs__kwajm, xunkm__jwki, qdh__udh.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            cul__bmopq = lhs.value - rhs.value
            return pd.Timedelta(cul__bmopq)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days - rhs.days
            s = lhs.seconds - rhs.seconds
            us = lhs.microseconds - rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            nqztg__tfbcj = lhs
            numba.parfors.parfor.init_prange()
            n = len(nqztg__tfbcj)
            A = alloc_datetime_timedelta_array(n)
            for gwcd__vrv in numba.parfors.parfor.internal_prange(n):
                A[gwcd__vrv] = nqztg__tfbcj[gwcd__vrv] - rhs
            return A
        return impl


def overload_mul_operator_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value * rhs)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(rhs.value * lhs)
        return impl
    if lhs == datetime_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            d = lhs.days * rhs
            s = lhs.seconds * rhs
            us = lhs.microseconds * rhs
            return datetime.timedelta(d, s, us)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs * rhs.days
            s = lhs * rhs.seconds
            us = lhs * rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl


def overload_floordiv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value // rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value // rhs)
        return impl


def overload_truediv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value / rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(int(lhs.value / rhs))
        return impl


def overload_mod_operator_timedeltas(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value % rhs.value)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            wymc__gzny = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, wymc__gzny)
        return impl


def pd_create_cmp_op_overload(op):

    def overload_pd_timedelta_cmp(lhs, rhs):
        if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

            def impl(lhs, rhs):
                return op(lhs.value, rhs.value)
            return impl
        if lhs == pd_timedelta_type and rhs == bodo.timedelta64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(lhs.value), rhs)
        if lhs == bodo.timedelta64ns and rhs == pd_timedelta_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(rhs.value))
    return overload_pd_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def pd_timedelta_neg(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return pd.Timedelta(-lhs.value)
        return impl


@overload(operator.pos, no_unliteral=True)
def pd_timedelta_pos(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def pd_timedelta_divmod(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            buxt__rni, wymc__gzny = divmod(lhs.value, rhs.value)
            return buxt__rni, pd.Timedelta(wymc__gzny)
        return impl


@overload(abs, no_unliteral=True)
def pd_timedelta_abs(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            if lhs.value < 0:
                return -lhs
            else:
                return lhs
        return impl


class DatetimeTimeDeltaType(types.Type):

    def __init__(self):
        super(DatetimeTimeDeltaType, self).__init__(name=
            'DatetimeTimeDeltaType()')


datetime_timedelta_type = DatetimeTimeDeltaType()


@typeof_impl.register(datetime.timedelta)
def typeof_datetime_timedelta(val, c):
    return datetime_timedelta_type


@register_model(DatetimeTimeDeltaType)
class DatetimeTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xjnyt__eyzbp = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, xjnyt__eyzbp
            )


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    oehyo__ficyk = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ork__ako = c.pyapi.long_from_longlong(oehyo__ficyk.days)
    jjeue__hxpn = c.pyapi.long_from_longlong(oehyo__ficyk.seconds)
    kzvg__onai = c.pyapi.long_from_longlong(oehyo__ficyk.microseconds)
    bbx__nuwbp = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(bbx__nuwbp, (ork__ako, jjeue__hxpn,
        kzvg__onai))
    c.pyapi.decref(ork__ako)
    c.pyapi.decref(jjeue__hxpn)
    c.pyapi.decref(kzvg__onai)
    c.pyapi.decref(bbx__nuwbp)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    ork__ako = c.pyapi.object_getattr_string(val, 'days')
    jjeue__hxpn = c.pyapi.object_getattr_string(val, 'seconds')
    kzvg__onai = c.pyapi.object_getattr_string(val, 'microseconds')
    vihks__tskx = c.pyapi.long_as_longlong(ork__ako)
    fbw__vtp = c.pyapi.long_as_longlong(jjeue__hxpn)
    siez__jce = c.pyapi.long_as_longlong(kzvg__onai)
    oehyo__ficyk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oehyo__ficyk.days = vihks__tskx
    oehyo__ficyk.seconds = fbw__vtp
    oehyo__ficyk.microseconds = siez__jce
    c.pyapi.decref(ork__ako)
    c.pyapi.decref(jjeue__hxpn)
    c.pyapi.decref(kzvg__onai)
    dcx__lmt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oehyo__ficyk._getvalue(), is_error=dcx__lmt)


@lower_constant(DatetimeTimeDeltaType)
def lower_constant_datetime_timedelta(context, builder, ty, pyval):
    days = context.get_constant(types.int64, pyval.days)
    seconds = context.get_constant(types.int64, pyval.seconds)
    microseconds = context.get_constant(types.int64, pyval.microseconds)
    return lir.Constant.literal_struct([days, seconds, microseconds])


@overload(datetime.timedelta, no_unliteral=True)
def datetime_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0):

    def impl_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
        minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        d = days
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += int(seconds)
        seconds, us = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += seconds
        return init_timedelta(d, s, us)
    return impl_timedelta


@intrinsic
def init_timedelta(typingctx, d, s, us):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.days = args[0]
        timedelta.seconds = args[1]
        timedelta.microseconds = args[2]
        return timedelta._getvalue()
    return DatetimeTimeDeltaType()(d, s, us), codegen


make_attribute_wrapper(DatetimeTimeDeltaType, 'days', '_days')
make_attribute_wrapper(DatetimeTimeDeltaType, 'seconds', '_seconds')
make_attribute_wrapper(DatetimeTimeDeltaType, 'microseconds', '_microseconds')


@overload_attribute(DatetimeTimeDeltaType, 'days')
def timedelta_get_days(td):

    def impl(td):
        return td._days
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'seconds')
def timedelta_get_seconds(td):

    def impl(td):
        return td._seconds
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'microseconds')
def timedelta_get_microseconds(td):

    def impl(td):
        return td._microseconds
    return impl


@overload_method(DatetimeTimeDeltaType, 'total_seconds', no_unliteral=True)
def total_seconds(td):

    def impl(td):
        return ((td._days * 86400 + td._seconds) * 10 ** 6 + td._microseconds
            ) / 10 ** 6
    return impl


@overload_method(DatetimeTimeDeltaType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        return hash((td._days, td._seconds, td._microseconds))
    return impl


@register_jitable
def _to_nanoseconds(td):
    return np.int64(((td._days * 86400 + td._seconds) * 1000000 + td.
        _microseconds) * 1000)


@register_jitable
def _to_microseconds(td):
    return (td._days * (24 * 3600) + td._seconds) * 1000000 + td._microseconds


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@register_jitable
def _getstate(td):
    return td._days, td._seconds, td._microseconds


@register_jitable
def _divide_and_round(a, b):
    buxt__rni, wymc__gzny = divmod(a, b)
    wymc__gzny *= 2
    ngq__zotg = wymc__gzny > b if b > 0 else wymc__gzny < b
    if ngq__zotg or wymc__gzny == b and buxt__rni % 2 == 1:
        buxt__rni += 1
    return buxt__rni


_MAXORDINAL = 3652059


def overload_floordiv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us // _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, us // rhs)
        return impl


def overload_truediv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us / _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, _divide_and_round(us, rhs))
        return impl


def create_cmp_op_overload(op):

    def overload_timedelta_cmp(lhs, rhs):
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

            def impl(lhs, rhs):
                pffq__wqz = _cmp(_getstate(lhs), _getstate(rhs))
                return op(pffq__wqz, 0)
            return impl
    return overload_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def timedelta_neg(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return datetime.timedelta(-lhs.days, -lhs.seconds, -lhs.
                microseconds)
        return impl


@overload(operator.pos, no_unliteral=True)
def timedelta_pos(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def timedelta_divmod(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            buxt__rni, wymc__gzny = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return buxt__rni, datetime.timedelta(0, 0, wymc__gzny)
        return impl


@overload(abs, no_unliteral=True)
def timedelta_abs(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            if lhs.days < 0:
                return -lhs
            else:
                return lhs
        return impl


@intrinsic
def cast_numpy_timedelta_to_int(typingctx, val=None):
    assert val in (types.NPTimedelta('ns'), types.int64)

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


@overload(bool, no_unliteral=True)
def timedelta_to_bool(timedelta):
    if timedelta != datetime_timedelta_type:
        return
    nnn__mac = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != nnn__mac
    return impl


class DatetimeTimeDeltaArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeTimeDeltaArrayType, self).__init__(name=
            'DatetimeTimeDeltaArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_timedelta_type

    def copy(self):
        return DatetimeTimeDeltaArrayType()


datetime_timedelta_array_type = DatetimeTimeDeltaArrayType()
types.datetime_timedelta_array_type = datetime_timedelta_array_type
days_data_type = types.Array(types.int64, 1, 'C')
seconds_data_type = types.Array(types.int64, 1, 'C')
microseconds_data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeTimeDeltaArrayType)
class DatetimeTimeDeltaArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xjnyt__eyzbp = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, xjnyt__eyzbp)


make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'days_data', '_days_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'seconds_data',
    '_seconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'microseconds_data',
    '_microseconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'null_bitmap',
    '_null_bitmap')


@overload_method(DatetimeTimeDeltaArrayType, 'copy', no_unliteral=True)
def overload_datetime_timedelta_arr_copy(A):
    return (lambda A: bodo.hiframes.datetime_timedelta_ext.
        init_datetime_timedelta_array(A._days_data.copy(), A._seconds_data.
        copy(), A._microseconds_data.copy(), A._null_bitmap.copy()))


@unbox(DatetimeTimeDeltaArrayType)
def unbox_datetime_timedelta_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    ktiwf__wwkt = types.Array(types.intp, 1, 'C')
    yaodc__fvp = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        ktiwf__wwkt, [n])
    jlrz__dqbq = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        ktiwf__wwkt, [n])
    aiulw__nwc = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        ktiwf__wwkt, [n])
    ave__rvgkb = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    qpq__hwk = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types.
        Array(types.uint8, 1, 'C'), [ave__rvgkb])
    ihno__mskpg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    dezdk__fhrty = cgutils.get_or_insert_function(c.builder.module,
        ihno__mskpg, name='unbox_datetime_timedelta_array')
    c.builder.call(dezdk__fhrty, [val, n, yaodc__fvp.data, jlrz__dqbq.data,
        aiulw__nwc.data, qpq__hwk.data])
    cxx__xfbgg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cxx__xfbgg.days_data = yaodc__fvp._getvalue()
    cxx__xfbgg.seconds_data = jlrz__dqbq._getvalue()
    cxx__xfbgg.microseconds_data = aiulw__nwc._getvalue()
    cxx__xfbgg.null_bitmap = qpq__hwk._getvalue()
    dcx__lmt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cxx__xfbgg._getvalue(), is_error=dcx__lmt)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    nqztg__tfbcj = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    yaodc__fvp = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, nqztg__tfbcj.days_data)
    jlrz__dqbq = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, nqztg__tfbcj.seconds_data).data
    aiulw__nwc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, nqztg__tfbcj.microseconds_data).data
    fipm__jdbqh = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, nqztg__tfbcj.null_bitmap).data
    n = c.builder.extract_value(yaodc__fvp.shape, 0)
    ihno__mskpg = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    qhk__zkvax = cgutils.get_or_insert_function(c.builder.module,
        ihno__mskpg, name='box_datetime_timedelta_array')
    smxt__eclt = c.builder.call(qhk__zkvax, [n, yaodc__fvp.data, jlrz__dqbq,
        aiulw__nwc, fipm__jdbqh])
    c.context.nrt.decref(c.builder, typ, val)
    return smxt__eclt


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        rjc__dngs, zinbb__ebjij, tyto__jtsej, qewr__isej = args
        lvigb__pmqty = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        lvigb__pmqty.days_data = rjc__dngs
        lvigb__pmqty.seconds_data = zinbb__ebjij
        lvigb__pmqty.microseconds_data = tyto__jtsej
        lvigb__pmqty.null_bitmap = qewr__isej
        context.nrt.incref(builder, signature.args[0], rjc__dngs)
        context.nrt.incref(builder, signature.args[1], zinbb__ebjij)
        context.nrt.incref(builder, signature.args[2], tyto__jtsej)
        context.nrt.incref(builder, signature.args[3], qewr__isej)
        return lvigb__pmqty._getvalue()
    osa__zpmct = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return osa__zpmct, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    yaodc__fvp = np.empty(n, np.int64)
    jlrz__dqbq = np.empty(n, np.int64)
    aiulw__nwc = np.empty(n, np.int64)
    hyqtq__nifu = np.empty(n + 7 >> 3, np.uint8)
    for gwcd__vrv, s in enumerate(pyval):
        aygr__buqgx = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(hyqtq__nifu, gwcd__vrv, int(
            not aygr__buqgx))
        if not aygr__buqgx:
            yaodc__fvp[gwcd__vrv] = s.days
            jlrz__dqbq[gwcd__vrv] = s.seconds
            aiulw__nwc[gwcd__vrv] = s.microseconds
    qen__fgbjm = context.get_constant_generic(builder, days_data_type,
        yaodc__fvp)
    suxn__uap = context.get_constant_generic(builder, seconds_data_type,
        jlrz__dqbq)
    gfi__yeik = context.get_constant_generic(builder,
        microseconds_data_type, aiulw__nwc)
    qhdi__dhr = context.get_constant_generic(builder, nulls_type, hyqtq__nifu)
    return lir.Constant.literal_struct([qen__fgbjm, suxn__uap, gfi__yeik,
        qhdi__dhr])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    yaodc__fvp = np.empty(n, dtype=np.int64)
    jlrz__dqbq = np.empty(n, dtype=np.int64)
    aiulw__nwc = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(yaodc__fvp, jlrz__dqbq, aiulw__nwc,
        nulls)


def alloc_datetime_timedelta_array_equiv(self, scope, equiv_set, loc, args, kws
    ):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_timedelta_ext_alloc_datetime_timedelta_array
    ) = alloc_datetime_timedelta_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_timedelta_arr_getitem(A, ind):
    if A != datetime_timedelta_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl_int(A, ind):
            return datetime.timedelta(days=A._days_data[ind], seconds=A.
                _seconds_data[ind], microseconds=A._microseconds_data[ind])
        return impl_int
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ftajv__clowb = bodo.utils.conversion.coerce_to_array(ind)
            yxl__bfx = A._null_bitmap
            zrae__vyus = A._days_data[ftajv__clowb]
            eqnn__ytjzn = A._seconds_data[ftajv__clowb]
            jpxzd__bxa = A._microseconds_data[ftajv__clowb]
            n = len(zrae__vyus)
            xbebq__zwq = get_new_null_mask_bool_index(yxl__bfx, ind, n)
            return init_datetime_timedelta_array(zrae__vyus, eqnn__ytjzn,
                jpxzd__bxa, xbebq__zwq)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ftajv__clowb = bodo.utils.conversion.coerce_to_array(ind)
            yxl__bfx = A._null_bitmap
            zrae__vyus = A._days_data[ftajv__clowb]
            eqnn__ytjzn = A._seconds_data[ftajv__clowb]
            jpxzd__bxa = A._microseconds_data[ftajv__clowb]
            n = len(zrae__vyus)
            xbebq__zwq = get_new_null_mask_int_index(yxl__bfx, ftajv__clowb, n)
            return init_datetime_timedelta_array(zrae__vyus, eqnn__ytjzn,
                jpxzd__bxa, xbebq__zwq)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            yxl__bfx = A._null_bitmap
            zrae__vyus = np.ascontiguousarray(A._days_data[ind])
            eqnn__ytjzn = np.ascontiguousarray(A._seconds_data[ind])
            jpxzd__bxa = np.ascontiguousarray(A._microseconds_data[ind])
            xbebq__zwq = get_new_null_mask_slice_index(yxl__bfx, ind, n)
            return init_datetime_timedelta_array(zrae__vyus, eqnn__ytjzn,
                jpxzd__bxa, xbebq__zwq)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def dt_timedelta_arr_setitem(A, ind, val):
    if A != datetime_timedelta_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    mguya__yrgss = (
        f"setitem for DatetimeTimedeltaArray with indexing type {ind} received an incorrect 'value' type {val}."
        )
    if isinstance(ind, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl(A, ind, val):
                A._days_data[ind] = val._days
                A._seconds_data[ind] = val._seconds
                A._microseconds_data[ind] = val._microseconds
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, ind, 1)
            return impl
        else:
            raise BodoError(mguya__yrgss)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(mguya__yrgss)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for gwcd__vrv in range(n):
                    A._days_data[ind[gwcd__vrv]] = val._days
                    A._seconds_data[ind[gwcd__vrv]] = val._seconds
                    A._microseconds_data[ind[gwcd__vrv]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[gwcd__vrv], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for gwcd__vrv in range(n):
                    A._days_data[ind[gwcd__vrv]] = val._days_data[gwcd__vrv]
                    A._seconds_data[ind[gwcd__vrv]] = val._seconds_data[
                        gwcd__vrv]
                    A._microseconds_data[ind[gwcd__vrv]
                        ] = val._microseconds_data[gwcd__vrv]
                    jtnlz__xoo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, gwcd__vrv)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[gwcd__vrv], jtnlz__xoo)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for gwcd__vrv in range(n):
                    if not bodo.libs.array_kernels.isna(ind, gwcd__vrv
                        ) and ind[gwcd__vrv]:
                        A._days_data[gwcd__vrv] = val._days
                        A._seconds_data[gwcd__vrv] = val._seconds
                        A._microseconds_data[gwcd__vrv] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            gwcd__vrv, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                pae__ezidt = 0
                for gwcd__vrv in range(n):
                    if not bodo.libs.array_kernels.isna(ind, gwcd__vrv
                        ) and ind[gwcd__vrv]:
                        A._days_data[gwcd__vrv] = val._days_data[pae__ezidt]
                        A._seconds_data[gwcd__vrv] = val._seconds_data[
                            pae__ezidt]
                        A._microseconds_data[gwcd__vrv
                            ] = val._microseconds_data[pae__ezidt]
                        jtnlz__xoo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, pae__ezidt)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            gwcd__vrv, jtnlz__xoo)
                        pae__ezidt += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                tfd__ufga = numba.cpython.unicode._normalize_slice(ind, len(A))
                for gwcd__vrv in range(tfd__ufga.start, tfd__ufga.stop,
                    tfd__ufga.step):
                    A._days_data[gwcd__vrv] = val._days
                    A._seconds_data[gwcd__vrv] = val._seconds
                    A._microseconds_data[gwcd__vrv] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        gwcd__vrv, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                vwty__sxxf = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, vwty__sxxf,
                    ind, n)
            return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_timedelta_arr(A):
    if A == datetime_timedelta_array_type:
        return lambda A: len(A._days_data)


@overload_attribute(DatetimeTimeDeltaArrayType, 'shape')
def overload_datetime_timedelta_arr_shape(A):
    return lambda A: (len(A._days_data),)


@overload_attribute(DatetimeTimeDeltaArrayType, 'nbytes')
def timedelta_arr_nbytes_overload(A):
    return (lambda A: A._days_data.nbytes + A._seconds_data.nbytes + A.
        _microseconds_data.nbytes + A._null_bitmap.nbytes)


def overload_datetime_timedelta_arr_sub(arg1, arg2):
    if (arg1 == datetime_timedelta_array_type and arg2 ==
        datetime_timedelta_type):

        def impl(arg1, arg2):
            nqztg__tfbcj = arg1
            numba.parfors.parfor.init_prange()
            n = len(nqztg__tfbcj)
            A = alloc_datetime_timedelta_array(n)
            for gwcd__vrv in numba.parfors.parfor.internal_prange(n):
                A[gwcd__vrv] = nqztg__tfbcj[gwcd__vrv] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            sdqe__xemm = True
        else:
            sdqe__xemm = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                aqcj__aow = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for gwcd__vrv in numba.parfors.parfor.internal_prange(n):
                    vun__qpohp = bodo.libs.array_kernels.isna(lhs, gwcd__vrv)
                    zmw__dayw = bodo.libs.array_kernels.isna(rhs, gwcd__vrv)
                    if vun__qpohp or zmw__dayw:
                        lhp__iadp = sdqe__xemm
                    else:
                        lhp__iadp = op(lhs[gwcd__vrv], rhs[gwcd__vrv])
                    aqcj__aow[gwcd__vrv] = lhp__iadp
                return aqcj__aow
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                aqcj__aow = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for gwcd__vrv in numba.parfors.parfor.internal_prange(n):
                    jtnlz__xoo = bodo.libs.array_kernels.isna(lhs, gwcd__vrv)
                    if jtnlz__xoo:
                        lhp__iadp = sdqe__xemm
                    else:
                        lhp__iadp = op(lhs[gwcd__vrv], rhs)
                    aqcj__aow[gwcd__vrv] = lhp__iadp
                return aqcj__aow
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                aqcj__aow = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for gwcd__vrv in numba.parfors.parfor.internal_prange(n):
                    jtnlz__xoo = bodo.libs.array_kernels.isna(rhs, gwcd__vrv)
                    if jtnlz__xoo:
                        lhp__iadp = sdqe__xemm
                    else:
                        lhp__iadp = op(lhs, rhs[gwcd__vrv])
                    aqcj__aow[gwcd__vrv] = lhp__iadp
                return aqcj__aow
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for kbhcr__vic in timedelta_unsupported_attrs:
        vrz__lhrhj = 'pandas.Timedelta.' + kbhcr__vic
        overload_attribute(PDTimeDeltaType, kbhcr__vic)(
            create_unsupported_overload(vrz__lhrhj))
    for ouyb__xmeg in timedelta_unsupported_methods:
        vrz__lhrhj = 'pandas.Timedelta.' + ouyb__xmeg
        overload_method(PDTimeDeltaType, ouyb__xmeg)(
            create_unsupported_overload(vrz__lhrhj + '()'))


_intstall_pd_timedelta_unsupported()
