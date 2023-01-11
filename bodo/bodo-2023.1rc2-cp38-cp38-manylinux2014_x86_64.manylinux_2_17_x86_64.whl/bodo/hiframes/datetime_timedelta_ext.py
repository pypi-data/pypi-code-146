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
        gkei__tqzp = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, gkei__tqzp)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    skc__twvrd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ddnx__nqvfi = c.pyapi.long_from_longlong(skc__twvrd.value)
    nagy__jsm = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(nagy__jsm, (ddnx__nqvfi,))
    c.pyapi.decref(ddnx__nqvfi)
    c.pyapi.decref(nagy__jsm)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    ddnx__nqvfi = c.pyapi.object_getattr_string(val, 'value')
    den__kqy = c.pyapi.long_as_longlong(ddnx__nqvfi)
    skc__twvrd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    skc__twvrd.value = den__kqy
    c.pyapi.decref(ddnx__nqvfi)
    mwd__hzad = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(skc__twvrd._getvalue(), is_error=mwd__hzad)


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
            yrrqz__qym = 1000 * microseconds
            return init_pd_timedelta(yrrqz__qym)
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
            yrrqz__qym = 1000 * microseconds
            return init_pd_timedelta(yrrqz__qym)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    tsy__wmb, gbgy__ldc = pd._libs.tslibs.conversion.precision_from_unit(unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * tsy__wmb)
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
            xkc__pjb = (rhs.microseconds + (rhs.seconds + rhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + xkc__pjb
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ifmw__lhmn = (lhs.microseconds + (lhs.seconds + lhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = ifmw__lhmn + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            dzy__jqo = rhs.toordinal()
            ldf__jzthu = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            fzazn__rzjz = rhs.microsecond
            pzkx__eopqk = lhs.value // 1000
            zfkq__epvpq = lhs.nanoseconds
            refqc__pdayy = fzazn__rzjz + pzkx__eopqk
            pvflp__odqs = 1000000 * (dzy__jqo * 86400 + ldf__jzthu
                ) + refqc__pdayy
            odzx__lpkh = zfkq__epvpq
            return compute_pd_timestamp(pvflp__odqs, odzx__lpkh)
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
            hxzfp__fosjp = datetime.timedelta(rhs.toordinal(), hours=rhs.
                hour, minutes=rhs.minute, seconds=rhs.second, microseconds=
                rhs.microsecond)
            hxzfp__fosjp = hxzfp__fosjp + lhs
            nuxm__une, ehmgz__lzu = divmod(hxzfp__fosjp.seconds, 3600)
            thnbg__kdthl, tet__izga = divmod(ehmgz__lzu, 60)
            if 0 < hxzfp__fosjp.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(
                    hxzfp__fosjp.days)
                return datetime.datetime(d.year, d.month, d.day, nuxm__une,
                    thnbg__kdthl, tet__izga, hxzfp__fosjp.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            hxzfp__fosjp = datetime.timedelta(lhs.toordinal(), hours=lhs.
                hour, minutes=lhs.minute, seconds=lhs.second, microseconds=
                lhs.microsecond)
            hxzfp__fosjp = hxzfp__fosjp + rhs
            nuxm__une, ehmgz__lzu = divmod(hxzfp__fosjp.seconds, 3600)
            thnbg__kdthl, tet__izga = divmod(ehmgz__lzu, 60)
            if 0 < hxzfp__fosjp.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(
                    hxzfp__fosjp.days)
                return datetime.datetime(d.year, d.month, d.day, nuxm__une,
                    thnbg__kdthl, tet__izga, hxzfp__fosjp.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ztya__psw = lhs.value - rhs.value
            return pd.Timedelta(ztya__psw)
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
            brxk__obkv = lhs
            numba.parfors.parfor.init_prange()
            n = len(brxk__obkv)
            A = alloc_datetime_timedelta_array(n)
            for npr__dyu in numba.parfors.parfor.internal_prange(n):
                A[npr__dyu] = brxk__obkv[npr__dyu] - rhs
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
            mpz__rhmc = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, mpz__rhmc)
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
            etjo__ksezb, mpz__rhmc = divmod(lhs.value, rhs.value)
            return etjo__ksezb, pd.Timedelta(mpz__rhmc)
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
        gkei__tqzp = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, gkei__tqzp)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    skc__twvrd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    irwgg__ycq = c.pyapi.long_from_longlong(skc__twvrd.days)
    ttf__vgox = c.pyapi.long_from_longlong(skc__twvrd.seconds)
    zyy__qquhe = c.pyapi.long_from_longlong(skc__twvrd.microseconds)
    nagy__jsm = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(nagy__jsm, (irwgg__ycq, ttf__vgox,
        zyy__qquhe))
    c.pyapi.decref(irwgg__ycq)
    c.pyapi.decref(ttf__vgox)
    c.pyapi.decref(zyy__qquhe)
    c.pyapi.decref(nagy__jsm)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    irwgg__ycq = c.pyapi.object_getattr_string(val, 'days')
    ttf__vgox = c.pyapi.object_getattr_string(val, 'seconds')
    zyy__qquhe = c.pyapi.object_getattr_string(val, 'microseconds')
    fkmta__hlge = c.pyapi.long_as_longlong(irwgg__ycq)
    kqnnc__bpivs = c.pyapi.long_as_longlong(ttf__vgox)
    ozm__ons = c.pyapi.long_as_longlong(zyy__qquhe)
    skc__twvrd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    skc__twvrd.days = fkmta__hlge
    skc__twvrd.seconds = kqnnc__bpivs
    skc__twvrd.microseconds = ozm__ons
    c.pyapi.decref(irwgg__ycq)
    c.pyapi.decref(ttf__vgox)
    c.pyapi.decref(zyy__qquhe)
    mwd__hzad = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(skc__twvrd._getvalue(), is_error=mwd__hzad)


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
    etjo__ksezb, mpz__rhmc = divmod(a, b)
    mpz__rhmc *= 2
    exp__gjq = mpz__rhmc > b if b > 0 else mpz__rhmc < b
    if exp__gjq or mpz__rhmc == b and etjo__ksezb % 2 == 1:
        etjo__ksezb += 1
    return etjo__ksezb


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
                nkacr__teud = _cmp(_getstate(lhs), _getstate(rhs))
                return op(nkacr__teud, 0)
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
            etjo__ksezb, mpz__rhmc = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return etjo__ksezb, datetime.timedelta(0, 0, mpz__rhmc)
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
    tqpiw__mqiuo = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != tqpiw__mqiuo
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
        gkei__tqzp = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, gkei__tqzp)


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
    gsanj__tdw = types.Array(types.intp, 1, 'C')
    sfxam__edq = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        gsanj__tdw, [n])
    vss__fcp = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        gsanj__tdw, [n])
    obuy__vhi = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        gsanj__tdw, [n])
    yjhnn__inir = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    htpy__mihi = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [yjhnn__inir])
    kfr__pskw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer()])
    mzoyj__wlm = cgutils.get_or_insert_function(c.builder.module, kfr__pskw,
        name='unbox_datetime_timedelta_array')
    c.builder.call(mzoyj__wlm, [val, n, sfxam__edq.data, vss__fcp.data,
        obuy__vhi.data, htpy__mihi.data])
    binkh__pxjup = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    binkh__pxjup.days_data = sfxam__edq._getvalue()
    binkh__pxjup.seconds_data = vss__fcp._getvalue()
    binkh__pxjup.microseconds_data = obuy__vhi._getvalue()
    binkh__pxjup.null_bitmap = htpy__mihi._getvalue()
    mwd__hzad = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(binkh__pxjup._getvalue(), is_error=mwd__hzad)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    brxk__obkv = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    sfxam__edq = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, brxk__obkv.days_data)
    vss__fcp = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, brxk__obkv.seconds_data).data
    obuy__vhi = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, brxk__obkv.microseconds_data).data
    gkt__jmybz = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, brxk__obkv.null_bitmap).data
    n = c.builder.extract_value(sfxam__edq.shape, 0)
    kfr__pskw = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    mlz__zmc = cgutils.get_or_insert_function(c.builder.module, kfr__pskw,
        name='box_datetime_timedelta_array')
    nnjw__hzg = c.builder.call(mlz__zmc, [n, sfxam__edq.data, vss__fcp,
        obuy__vhi, gkt__jmybz])
    c.context.nrt.decref(c.builder, typ, val)
    return nnjw__hzg


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        yuanx__jfgn, jzm__bhin, yjg__xtd, hniqv__tjw = args
        lgkwu__nigg = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        lgkwu__nigg.days_data = yuanx__jfgn
        lgkwu__nigg.seconds_data = jzm__bhin
        lgkwu__nigg.microseconds_data = yjg__xtd
        lgkwu__nigg.null_bitmap = hniqv__tjw
        context.nrt.incref(builder, signature.args[0], yuanx__jfgn)
        context.nrt.incref(builder, signature.args[1], jzm__bhin)
        context.nrt.incref(builder, signature.args[2], yjg__xtd)
        context.nrt.incref(builder, signature.args[3], hniqv__tjw)
        return lgkwu__nigg._getvalue()
    zsq__zghgm = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return zsq__zghgm, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    sfxam__edq = np.empty(n, np.int64)
    vss__fcp = np.empty(n, np.int64)
    obuy__vhi = np.empty(n, np.int64)
    soh__wsc = np.empty(n + 7 >> 3, np.uint8)
    for npr__dyu, s in enumerate(pyval):
        lufqq__vkq = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(soh__wsc, npr__dyu, int(not
            lufqq__vkq))
        if not lufqq__vkq:
            sfxam__edq[npr__dyu] = s.days
            vss__fcp[npr__dyu] = s.seconds
            obuy__vhi[npr__dyu] = s.microseconds
    xhex__pksp = context.get_constant_generic(builder, days_data_type,
        sfxam__edq)
    jrpzc__ksqfx = context.get_constant_generic(builder, seconds_data_type,
        vss__fcp)
    iawn__nlshd = context.get_constant_generic(builder,
        microseconds_data_type, obuy__vhi)
    jpbpx__begy = context.get_constant_generic(builder, nulls_type, soh__wsc)
    return lir.Constant.literal_struct([xhex__pksp, jrpzc__ksqfx,
        iawn__nlshd, jpbpx__begy])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    sfxam__edq = np.empty(n, dtype=np.int64)
    vss__fcp = np.empty(n, dtype=np.int64)
    obuy__vhi = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(sfxam__edq, vss__fcp, obuy__vhi, nulls
        )


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
            risy__unm = bodo.utils.conversion.coerce_to_array(ind)
            cjhx__ogqu = A._null_bitmap
            ekjw__uqt = A._days_data[risy__unm]
            bfr__hkv = A._seconds_data[risy__unm]
            tldoi__xiw = A._microseconds_data[risy__unm]
            n = len(ekjw__uqt)
            urkly__egi = get_new_null_mask_bool_index(cjhx__ogqu, ind, n)
            return init_datetime_timedelta_array(ekjw__uqt, bfr__hkv,
                tldoi__xiw, urkly__egi)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            risy__unm = bodo.utils.conversion.coerce_to_array(ind)
            cjhx__ogqu = A._null_bitmap
            ekjw__uqt = A._days_data[risy__unm]
            bfr__hkv = A._seconds_data[risy__unm]
            tldoi__xiw = A._microseconds_data[risy__unm]
            n = len(ekjw__uqt)
            urkly__egi = get_new_null_mask_int_index(cjhx__ogqu, risy__unm, n)
            return init_datetime_timedelta_array(ekjw__uqt, bfr__hkv,
                tldoi__xiw, urkly__egi)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            cjhx__ogqu = A._null_bitmap
            ekjw__uqt = np.ascontiguousarray(A._days_data[ind])
            bfr__hkv = np.ascontiguousarray(A._seconds_data[ind])
            tldoi__xiw = np.ascontiguousarray(A._microseconds_data[ind])
            urkly__egi = get_new_null_mask_slice_index(cjhx__ogqu, ind, n)
            return init_datetime_timedelta_array(ekjw__uqt, bfr__hkv,
                tldoi__xiw, urkly__egi)
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
    grksy__xgu = (
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
            raise BodoError(grksy__xgu)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(grksy__xgu)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for npr__dyu in range(n):
                    A._days_data[ind[npr__dyu]] = val._days
                    A._seconds_data[ind[npr__dyu]] = val._seconds
                    A._microseconds_data[ind[npr__dyu]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[npr__dyu], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for npr__dyu in range(n):
                    A._days_data[ind[npr__dyu]] = val._days_data[npr__dyu]
                    A._seconds_data[ind[npr__dyu]] = val._seconds_data[npr__dyu
                        ]
                    A._microseconds_data[ind[npr__dyu]
                        ] = val._microseconds_data[npr__dyu]
                    abgh__wdxs = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, npr__dyu)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[npr__dyu], abgh__wdxs)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for npr__dyu in range(n):
                    if not bodo.libs.array_kernels.isna(ind, npr__dyu) and ind[
                        npr__dyu]:
                        A._days_data[npr__dyu] = val._days
                        A._seconds_data[npr__dyu] = val._seconds
                        A._microseconds_data[npr__dyu] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            npr__dyu, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                smbhw__ptie = 0
                for npr__dyu in range(n):
                    if not bodo.libs.array_kernels.isna(ind, npr__dyu) and ind[
                        npr__dyu]:
                        A._days_data[npr__dyu] = val._days_data[smbhw__ptie]
                        A._seconds_data[npr__dyu] = val._seconds_data[
                            smbhw__ptie]
                        A._microseconds_data[npr__dyu
                            ] = val._microseconds_data[smbhw__ptie]
                        abgh__wdxs = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, smbhw__ptie)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            npr__dyu, abgh__wdxs)
                        smbhw__ptie += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                pzdfr__rrj = numba.cpython.unicode._normalize_slice(ind, len(A)
                    )
                for npr__dyu in range(pzdfr__rrj.start, pzdfr__rrj.stop,
                    pzdfr__rrj.step):
                    A._days_data[npr__dyu] = val._days
                    A._seconds_data[npr__dyu] = val._seconds
                    A._microseconds_data[npr__dyu] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        npr__dyu, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                mij__mjge = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, mij__mjge, ind, n
                    )
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
            brxk__obkv = arg1
            numba.parfors.parfor.init_prange()
            n = len(brxk__obkv)
            A = alloc_datetime_timedelta_array(n)
            for npr__dyu in numba.parfors.parfor.internal_prange(n):
                A[npr__dyu] = brxk__obkv[npr__dyu] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            kdkg__jlif = True
        else:
            kdkg__jlif = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                qbh__zerkv = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for npr__dyu in numba.parfors.parfor.internal_prange(n):
                    kchwx__dqabr = bodo.libs.array_kernels.isna(lhs, npr__dyu)
                    vohhf__crz = bodo.libs.array_kernels.isna(rhs, npr__dyu)
                    if kchwx__dqabr or vohhf__crz:
                        rrjk__shdmr = kdkg__jlif
                    else:
                        rrjk__shdmr = op(lhs[npr__dyu], rhs[npr__dyu])
                    qbh__zerkv[npr__dyu] = rrjk__shdmr
                return qbh__zerkv
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                qbh__zerkv = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for npr__dyu in numba.parfors.parfor.internal_prange(n):
                    abgh__wdxs = bodo.libs.array_kernels.isna(lhs, npr__dyu)
                    if abgh__wdxs:
                        rrjk__shdmr = kdkg__jlif
                    else:
                        rrjk__shdmr = op(lhs[npr__dyu], rhs)
                    qbh__zerkv[npr__dyu] = rrjk__shdmr
                return qbh__zerkv
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                qbh__zerkv = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for npr__dyu in numba.parfors.parfor.internal_prange(n):
                    abgh__wdxs = bodo.libs.array_kernels.isna(rhs, npr__dyu)
                    if abgh__wdxs:
                        rrjk__shdmr = kdkg__jlif
                    else:
                        rrjk__shdmr = op(lhs, rhs[npr__dyu])
                    qbh__zerkv[npr__dyu] = rrjk__shdmr
                return qbh__zerkv
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for ajkqh__paj in timedelta_unsupported_attrs:
        ujab__afz = 'pandas.Timedelta.' + ajkqh__paj
        overload_attribute(PDTimeDeltaType, ajkqh__paj)(
            create_unsupported_overload(ujab__afz))
    for lxv__ndt in timedelta_unsupported_methods:
        ujab__afz = 'pandas.Timedelta.' + lxv__ndt
        overload_method(PDTimeDeltaType, lxv__ndt)(create_unsupported_overload
            (ujab__afz + '()'))


_intstall_pd_timedelta_unsupported()
