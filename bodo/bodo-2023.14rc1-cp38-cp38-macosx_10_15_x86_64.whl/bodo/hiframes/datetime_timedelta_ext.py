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
        hii__aht = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, hii__aht)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    jld__dwpa = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    unlo__yfk = c.pyapi.long_from_longlong(jld__dwpa.value)
    whkhm__vre = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(whkhm__vre, (unlo__yfk,))
    c.pyapi.decref(unlo__yfk)
    c.pyapi.decref(whkhm__vre)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    unlo__yfk = c.pyapi.object_getattr_string(val, 'value')
    zgj__huv = c.pyapi.long_as_longlong(unlo__yfk)
    jld__dwpa = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jld__dwpa.value = zgj__huv
    c.pyapi.decref(unlo__yfk)
    awjuh__oex = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(jld__dwpa._getvalue(), is_error=awjuh__oex)


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
            kqg__wsxra = 1000 * microseconds
            return init_pd_timedelta(kqg__wsxra)
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
            kqg__wsxra = 1000 * microseconds
            return init_pd_timedelta(kqg__wsxra)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    dot__crl, axb__qge = pd._libs.tslibs.conversion.precision_from_unit(unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * dot__crl)
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
            pgis__gngv = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + pgis__gngv
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            qnv__bpe = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = qnv__bpe + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            wic__gvl = rhs.toordinal()
            wvkdb__suh = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            wcru__qvam = rhs.microsecond
            ojkb__zmaie = lhs.value // 1000
            sgg__fuist = lhs.nanoseconds
            jbho__dqmt = wcru__qvam + ojkb__zmaie
            kwlye__oileu = 1000000 * (wic__gvl * 86400 + wvkdb__suh
                ) + jbho__dqmt
            uoy__clh = sgg__fuist
            return compute_pd_timestamp(kwlye__oileu, uoy__clh)
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
            mlxi__goq = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            mlxi__goq = mlxi__goq + lhs
            hklh__ssbr, ypo__eis = divmod(mlxi__goq.seconds, 3600)
            fefod__bhzia, rdx__ktktt = divmod(ypo__eis, 60)
            if 0 < mlxi__goq.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(mlxi__goq
                    .days)
                return datetime.datetime(d.year, d.month, d.day, hklh__ssbr,
                    fefod__bhzia, rdx__ktktt, mlxi__goq.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            mlxi__goq = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            mlxi__goq = mlxi__goq + rhs
            hklh__ssbr, ypo__eis = divmod(mlxi__goq.seconds, 3600)
            fefod__bhzia, rdx__ktktt = divmod(ypo__eis, 60)
            if 0 < mlxi__goq.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(mlxi__goq
                    .days)
                return datetime.datetime(d.year, d.month, d.day, hklh__ssbr,
                    fefod__bhzia, rdx__ktktt, mlxi__goq.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ggm__qtq = lhs.value - rhs.value
            return pd.Timedelta(ggm__qtq)
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
            bwwyr__gracl = lhs
            numba.parfors.parfor.init_prange()
            n = len(bwwyr__gracl)
            A = alloc_datetime_timedelta_array(n)
            for wkw__tgvyb in numba.parfors.parfor.internal_prange(n):
                A[wkw__tgvyb] = bwwyr__gracl[wkw__tgvyb] - rhs
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
            wbv__fyv = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, wbv__fyv)
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
            gkpc__yitt, wbv__fyv = divmod(lhs.value, rhs.value)
            return gkpc__yitt, pd.Timedelta(wbv__fyv)
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
        hii__aht = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, hii__aht)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    jld__dwpa = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    xag__ozw = c.pyapi.long_from_longlong(jld__dwpa.days)
    xixjh__pqiha = c.pyapi.long_from_longlong(jld__dwpa.seconds)
    bextu__fqxbw = c.pyapi.long_from_longlong(jld__dwpa.microseconds)
    whkhm__vre = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(whkhm__vre, (xag__ozw, xixjh__pqiha,
        bextu__fqxbw))
    c.pyapi.decref(xag__ozw)
    c.pyapi.decref(xixjh__pqiha)
    c.pyapi.decref(bextu__fqxbw)
    c.pyapi.decref(whkhm__vre)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    xag__ozw = c.pyapi.object_getattr_string(val, 'days')
    xixjh__pqiha = c.pyapi.object_getattr_string(val, 'seconds')
    bextu__fqxbw = c.pyapi.object_getattr_string(val, 'microseconds')
    xzo__yadac = c.pyapi.long_as_longlong(xag__ozw)
    zrhhj__pebtf = c.pyapi.long_as_longlong(xixjh__pqiha)
    wql__lsb = c.pyapi.long_as_longlong(bextu__fqxbw)
    jld__dwpa = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jld__dwpa.days = xzo__yadac
    jld__dwpa.seconds = zrhhj__pebtf
    jld__dwpa.microseconds = wql__lsb
    c.pyapi.decref(xag__ozw)
    c.pyapi.decref(xixjh__pqiha)
    c.pyapi.decref(bextu__fqxbw)
    awjuh__oex = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(jld__dwpa._getvalue(), is_error=awjuh__oex)


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
    gkpc__yitt, wbv__fyv = divmod(a, b)
    wbv__fyv *= 2
    yfft__fkg = wbv__fyv > b if b > 0 else wbv__fyv < b
    if yfft__fkg or wbv__fyv == b and gkpc__yitt % 2 == 1:
        gkpc__yitt += 1
    return gkpc__yitt


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
                buges__ekv = _cmp(_getstate(lhs), _getstate(rhs))
                return op(buges__ekv, 0)
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
            gkpc__yitt, wbv__fyv = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return gkpc__yitt, datetime.timedelta(0, 0, wbv__fyv)
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
    ueov__cxant = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != ueov__cxant
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
        hii__aht = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, hii__aht)


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
    reo__vqwnh = types.Array(types.intp, 1, 'C')
    pnvz__udcue = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        reo__vqwnh, [n])
    xqnvy__ltfxx = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        reo__vqwnh, [n])
    zlx__cjs = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        reo__vqwnh, [n])
    emfl__zngep = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    gzd__uml = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types.
        Array(types.uint8, 1, 'C'), [emfl__zngep])
    qiqs__nnwgk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    uwfzb__zcoc = cgutils.get_or_insert_function(c.builder.module,
        qiqs__nnwgk, name='unbox_datetime_timedelta_array')
    c.builder.call(uwfzb__zcoc, [val, n, pnvz__udcue.data, xqnvy__ltfxx.
        data, zlx__cjs.data, gzd__uml.data])
    gmte__lgkr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gmte__lgkr.days_data = pnvz__udcue._getvalue()
    gmte__lgkr.seconds_data = xqnvy__ltfxx._getvalue()
    gmte__lgkr.microseconds_data = zlx__cjs._getvalue()
    gmte__lgkr.null_bitmap = gzd__uml._getvalue()
    awjuh__oex = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gmte__lgkr._getvalue(), is_error=awjuh__oex)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    bwwyr__gracl = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    pnvz__udcue = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, bwwyr__gracl.days_data)
    xqnvy__ltfxx = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, bwwyr__gracl.seconds_data).data
    zlx__cjs = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, bwwyr__gracl.microseconds_data).data
    dtv__tjd = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, bwwyr__gracl.null_bitmap).data
    n = c.builder.extract_value(pnvz__udcue.shape, 0)
    qiqs__nnwgk = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    ftuvw__dgpk = cgutils.get_or_insert_function(c.builder.module,
        qiqs__nnwgk, name='box_datetime_timedelta_array')
    yeptr__vxk = c.builder.call(ftuvw__dgpk, [n, pnvz__udcue.data,
        xqnvy__ltfxx, zlx__cjs, dtv__tjd])
    c.context.nrt.decref(c.builder, typ, val)
    return yeptr__vxk


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        kojhj__onw, wvsl__uyu, ulaz__ccat, vqf__cjhbh = args
        uimos__heii = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        uimos__heii.days_data = kojhj__onw
        uimos__heii.seconds_data = wvsl__uyu
        uimos__heii.microseconds_data = ulaz__ccat
        uimos__heii.null_bitmap = vqf__cjhbh
        context.nrt.incref(builder, signature.args[0], kojhj__onw)
        context.nrt.incref(builder, signature.args[1], wvsl__uyu)
        context.nrt.incref(builder, signature.args[2], ulaz__ccat)
        context.nrt.incref(builder, signature.args[3], vqf__cjhbh)
        return uimos__heii._getvalue()
    lbm__bad = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return lbm__bad, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    pnvz__udcue = np.empty(n, np.int64)
    xqnvy__ltfxx = np.empty(n, np.int64)
    zlx__cjs = np.empty(n, np.int64)
    wjpm__vde = np.empty(n + 7 >> 3, np.uint8)
    for wkw__tgvyb, s in enumerate(pyval):
        shutp__eouyi = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(wjpm__vde, wkw__tgvyb, int(not
            shutp__eouyi))
        if not shutp__eouyi:
            pnvz__udcue[wkw__tgvyb] = s.days
            xqnvy__ltfxx[wkw__tgvyb] = s.seconds
            zlx__cjs[wkw__tgvyb] = s.microseconds
    bopt__srt = context.get_constant_generic(builder, days_data_type,
        pnvz__udcue)
    ocon__lxijx = context.get_constant_generic(builder, seconds_data_type,
        xqnvy__ltfxx)
    drwqr__xjq = context.get_constant_generic(builder,
        microseconds_data_type, zlx__cjs)
    jql__vtw = context.get_constant_generic(builder, nulls_type, wjpm__vde)
    return lir.Constant.literal_struct([bopt__srt, ocon__lxijx, drwqr__xjq,
        jql__vtw])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    pnvz__udcue = np.empty(n, dtype=np.int64)
    xqnvy__ltfxx = np.empty(n, dtype=np.int64)
    zlx__cjs = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(pnvz__udcue, xqnvy__ltfxx,
        zlx__cjs, nulls)


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
            mvdgn__ibu = bodo.utils.conversion.coerce_to_array(ind)
            wwq__dlqh = A._null_bitmap
            dkwue__rrc = A._days_data[mvdgn__ibu]
            tmf__talry = A._seconds_data[mvdgn__ibu]
            ogdt__ysnec = A._microseconds_data[mvdgn__ibu]
            n = len(dkwue__rrc)
            xcmtq__zqxk = get_new_null_mask_bool_index(wwq__dlqh, ind, n)
            return init_datetime_timedelta_array(dkwue__rrc, tmf__talry,
                ogdt__ysnec, xcmtq__zqxk)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            mvdgn__ibu = bodo.utils.conversion.coerce_to_array(ind)
            wwq__dlqh = A._null_bitmap
            dkwue__rrc = A._days_data[mvdgn__ibu]
            tmf__talry = A._seconds_data[mvdgn__ibu]
            ogdt__ysnec = A._microseconds_data[mvdgn__ibu]
            n = len(dkwue__rrc)
            xcmtq__zqxk = get_new_null_mask_int_index(wwq__dlqh, mvdgn__ibu, n)
            return init_datetime_timedelta_array(dkwue__rrc, tmf__talry,
                ogdt__ysnec, xcmtq__zqxk)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            wwq__dlqh = A._null_bitmap
            dkwue__rrc = np.ascontiguousarray(A._days_data[ind])
            tmf__talry = np.ascontiguousarray(A._seconds_data[ind])
            ogdt__ysnec = np.ascontiguousarray(A._microseconds_data[ind])
            xcmtq__zqxk = get_new_null_mask_slice_index(wwq__dlqh, ind, n)
            return init_datetime_timedelta_array(dkwue__rrc, tmf__talry,
                ogdt__ysnec, xcmtq__zqxk)
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
    rtrc__obp = (
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
            raise BodoError(rtrc__obp)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(rtrc__obp)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for wkw__tgvyb in range(n):
                    A._days_data[ind[wkw__tgvyb]] = val._days
                    A._seconds_data[ind[wkw__tgvyb]] = val._seconds
                    A._microseconds_data[ind[wkw__tgvyb]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[wkw__tgvyb], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for wkw__tgvyb in range(n):
                    A._days_data[ind[wkw__tgvyb]] = val._days_data[wkw__tgvyb]
                    A._seconds_data[ind[wkw__tgvyb]] = val._seconds_data[
                        wkw__tgvyb]
                    A._microseconds_data[ind[wkw__tgvyb]
                        ] = val._microseconds_data[wkw__tgvyb]
                    javh__duf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, wkw__tgvyb)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[wkw__tgvyb], javh__duf)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for wkw__tgvyb in range(n):
                    if not bodo.libs.array_kernels.isna(ind, wkw__tgvyb
                        ) and ind[wkw__tgvyb]:
                        A._days_data[wkw__tgvyb] = val._days
                        A._seconds_data[wkw__tgvyb] = val._seconds
                        A._microseconds_data[wkw__tgvyb] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            wkw__tgvyb, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                jao__lymae = 0
                for wkw__tgvyb in range(n):
                    if not bodo.libs.array_kernels.isna(ind, wkw__tgvyb
                        ) and ind[wkw__tgvyb]:
                        A._days_data[wkw__tgvyb] = val._days_data[jao__lymae]
                        A._seconds_data[wkw__tgvyb] = val._seconds_data[
                            jao__lymae]
                        A._microseconds_data[wkw__tgvyb
                            ] = val._microseconds_data[jao__lymae]
                        javh__duf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, jao__lymae)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            wkw__tgvyb, javh__duf)
                        jao__lymae += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                jeco__kniq = numba.cpython.unicode._normalize_slice(ind, len(A)
                    )
                for wkw__tgvyb in range(jeco__kniq.start, jeco__kniq.stop,
                    jeco__kniq.step):
                    A._days_data[wkw__tgvyb] = val._days
                    A._seconds_data[wkw__tgvyb] = val._seconds
                    A._microseconds_data[wkw__tgvyb] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        wkw__tgvyb, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                zcrqx__but = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, zcrqx__but,
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
            bwwyr__gracl = arg1
            numba.parfors.parfor.init_prange()
            n = len(bwwyr__gracl)
            A = alloc_datetime_timedelta_array(n)
            for wkw__tgvyb in numba.parfors.parfor.internal_prange(n):
                A[wkw__tgvyb] = bwwyr__gracl[wkw__tgvyb] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            wfkfr__bophg = True
        else:
            wfkfr__bophg = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                qxh__yqzg = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for wkw__tgvyb in numba.parfors.parfor.internal_prange(n):
                    gqxp__iyln = bodo.libs.array_kernels.isna(lhs, wkw__tgvyb)
                    aqbh__rky = bodo.libs.array_kernels.isna(rhs, wkw__tgvyb)
                    if gqxp__iyln or aqbh__rky:
                        vloz__cavuh = wfkfr__bophg
                    else:
                        vloz__cavuh = op(lhs[wkw__tgvyb], rhs[wkw__tgvyb])
                    qxh__yqzg[wkw__tgvyb] = vloz__cavuh
                return qxh__yqzg
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                qxh__yqzg = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for wkw__tgvyb in numba.parfors.parfor.internal_prange(n):
                    javh__duf = bodo.libs.array_kernels.isna(lhs, wkw__tgvyb)
                    if javh__duf:
                        vloz__cavuh = wfkfr__bophg
                    else:
                        vloz__cavuh = op(lhs[wkw__tgvyb], rhs)
                    qxh__yqzg[wkw__tgvyb] = vloz__cavuh
                return qxh__yqzg
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                qxh__yqzg = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for wkw__tgvyb in numba.parfors.parfor.internal_prange(n):
                    javh__duf = bodo.libs.array_kernels.isna(rhs, wkw__tgvyb)
                    if javh__duf:
                        vloz__cavuh = wfkfr__bophg
                    else:
                        vloz__cavuh = op(lhs, rhs[wkw__tgvyb])
                    qxh__yqzg[wkw__tgvyb] = vloz__cavuh
                return qxh__yqzg
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for qqw__hnos in timedelta_unsupported_attrs:
        vryak__mbh = 'pandas.Timedelta.' + qqw__hnos
        overload_attribute(PDTimeDeltaType, qqw__hnos)(
            create_unsupported_overload(vryak__mbh))
    for aqzq__jvk in timedelta_unsupported_methods:
        vryak__mbh = 'pandas.Timedelta.' + aqzq__jvk
        overload_method(PDTimeDeltaType, aqzq__jvk)(create_unsupported_overload
            (vryak__mbh + '()'))


_intstall_pd_timedelta_unsupported()
