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
        pzv__psk = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, pzv__psk)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    lper__fxeqi = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    blg__ehoq = c.pyapi.long_from_longlong(lper__fxeqi.value)
    qrjc__tsvnx = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(qrjc__tsvnx, (blg__ehoq,))
    c.pyapi.decref(blg__ehoq)
    c.pyapi.decref(qrjc__tsvnx)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    blg__ehoq = c.pyapi.object_getattr_string(val, 'value')
    evo__dawe = c.pyapi.long_as_longlong(blg__ehoq)
    lper__fxeqi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lper__fxeqi.value = evo__dawe
    c.pyapi.decref(blg__ehoq)
    cid__edx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lper__fxeqi._getvalue(), is_error=cid__edx)


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
            qnr__apggo = 1000 * microseconds
            return init_pd_timedelta(qnr__apggo)
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
            qnr__apggo = 1000 * microseconds
            return init_pd_timedelta(qnr__apggo)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    wlp__uupq, zubaq__aqkl = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * wlp__uupq)
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
            bpf__log = (rhs.microseconds + (rhs.seconds + rhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + bpf__log
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            asp__lkl = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = asp__lkl + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            vit__rbuu = rhs.toordinal()
            ewhc__xab = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            lzgn__guvph = rhs.microsecond
            fbs__vmjpj = lhs.value // 1000
            zxkxn__sdlz = lhs.nanoseconds
            mfqor__wtxxc = lzgn__guvph + fbs__vmjpj
            wrnx__uwp = 1000000 * (vit__rbuu * 86400 + ewhc__xab
                ) + mfqor__wtxxc
            sdqsr__bwzai = zxkxn__sdlz
            return compute_pd_timestamp(wrnx__uwp, sdqsr__bwzai)
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
            fvv__zbf = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            fvv__zbf = fvv__zbf + lhs
            qdar__pxbze, aga__qvs = divmod(fvv__zbf.seconds, 3600)
            oooe__llgki, lrz__ate = divmod(aga__qvs, 60)
            if 0 < fvv__zbf.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(fvv__zbf
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    qdar__pxbze, oooe__llgki, lrz__ate, fvv__zbf.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            fvv__zbf = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            fvv__zbf = fvv__zbf + rhs
            qdar__pxbze, aga__qvs = divmod(fvv__zbf.seconds, 3600)
            oooe__llgki, lrz__ate = divmod(aga__qvs, 60)
            if 0 < fvv__zbf.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(fvv__zbf
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    qdar__pxbze, oooe__llgki, lrz__ate, fvv__zbf.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ommtj__yjdda = lhs.value - rhs.value
            return pd.Timedelta(ommtj__yjdda)
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
            ytrzx__qvy = lhs
            numba.parfors.parfor.init_prange()
            n = len(ytrzx__qvy)
            A = alloc_datetime_timedelta_array(n)
            for ykod__rau in numba.parfors.parfor.internal_prange(n):
                A[ykod__rau] = ytrzx__qvy[ykod__rau] - rhs
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
            wfurt__gpd = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, wfurt__gpd)
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
            whdf__vxafn, wfurt__gpd = divmod(lhs.value, rhs.value)
            return whdf__vxafn, pd.Timedelta(wfurt__gpd)
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
        pzv__psk = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, pzv__psk)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    lper__fxeqi = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    cayl__ruca = c.pyapi.long_from_longlong(lper__fxeqi.days)
    ruzjj__olsdn = c.pyapi.long_from_longlong(lper__fxeqi.seconds)
    ganf__xmh = c.pyapi.long_from_longlong(lper__fxeqi.microseconds)
    qrjc__tsvnx = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(qrjc__tsvnx, (cayl__ruca,
        ruzjj__olsdn, ganf__xmh))
    c.pyapi.decref(cayl__ruca)
    c.pyapi.decref(ruzjj__olsdn)
    c.pyapi.decref(ganf__xmh)
    c.pyapi.decref(qrjc__tsvnx)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    cayl__ruca = c.pyapi.object_getattr_string(val, 'days')
    ruzjj__olsdn = c.pyapi.object_getattr_string(val, 'seconds')
    ganf__xmh = c.pyapi.object_getattr_string(val, 'microseconds')
    nxkb__lehl = c.pyapi.long_as_longlong(cayl__ruca)
    hcm__ehk = c.pyapi.long_as_longlong(ruzjj__olsdn)
    qagi__rkar = c.pyapi.long_as_longlong(ganf__xmh)
    lper__fxeqi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lper__fxeqi.days = nxkb__lehl
    lper__fxeqi.seconds = hcm__ehk
    lper__fxeqi.microseconds = qagi__rkar
    c.pyapi.decref(cayl__ruca)
    c.pyapi.decref(ruzjj__olsdn)
    c.pyapi.decref(ganf__xmh)
    cid__edx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lper__fxeqi._getvalue(), is_error=cid__edx)


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
    whdf__vxafn, wfurt__gpd = divmod(a, b)
    wfurt__gpd *= 2
    lpax__ykig = wfurt__gpd > b if b > 0 else wfurt__gpd < b
    if lpax__ykig or wfurt__gpd == b and whdf__vxafn % 2 == 1:
        whdf__vxafn += 1
    return whdf__vxafn


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
                nqqt__zowc = _cmp(_getstate(lhs), _getstate(rhs))
                return op(nqqt__zowc, 0)
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
            whdf__vxafn, wfurt__gpd = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return whdf__vxafn, datetime.timedelta(0, 0, wfurt__gpd)
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
    ettw__dnius = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != ettw__dnius
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
        pzv__psk = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, pzv__psk)


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
    miwm__njce = types.Array(types.intp, 1, 'C')
    mvuk__jglp = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        miwm__njce, [n])
    nyc__ttl = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        miwm__njce, [n])
    tmgc__qzrc = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        miwm__njce, [n])
    fow__vmq = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64),
        7)), lir.Constant(lir.IntType(64), 8))
    pxu__laj = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types.
        Array(types.uint8, 1, 'C'), [fow__vmq])
    pghbv__grt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    rfdes__egcm = cgutils.get_or_insert_function(c.builder.module,
        pghbv__grt, name='unbox_datetime_timedelta_array')
    c.builder.call(rfdes__egcm, [val, n, mvuk__jglp.data, nyc__ttl.data,
        tmgc__qzrc.data, pxu__laj.data])
    hyux__tzk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hyux__tzk.days_data = mvuk__jglp._getvalue()
    hyux__tzk.seconds_data = nyc__ttl._getvalue()
    hyux__tzk.microseconds_data = tmgc__qzrc._getvalue()
    hyux__tzk.null_bitmap = pxu__laj._getvalue()
    cid__edx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hyux__tzk._getvalue(), is_error=cid__edx)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    ytrzx__qvy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    mvuk__jglp = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, ytrzx__qvy.days_data)
    nyc__ttl = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, ytrzx__qvy.seconds_data).data
    tmgc__qzrc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, ytrzx__qvy.microseconds_data).data
    zedrr__hcohr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, ytrzx__qvy.null_bitmap).data
    n = c.builder.extract_value(mvuk__jglp.shape, 0)
    pghbv__grt = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    dnsy__nfl = cgutils.get_or_insert_function(c.builder.module, pghbv__grt,
        name='box_datetime_timedelta_array')
    iqqj__afq = c.builder.call(dnsy__nfl, [n, mvuk__jglp.data, nyc__ttl,
        tmgc__qzrc, zedrr__hcohr])
    c.context.nrt.decref(c.builder, typ, val)
    return iqqj__afq


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        ytk__ndd, fju__qri, fkqjx__pseve, tmet__bvwd = args
        bgps__ywjbu = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        bgps__ywjbu.days_data = ytk__ndd
        bgps__ywjbu.seconds_data = fju__qri
        bgps__ywjbu.microseconds_data = fkqjx__pseve
        bgps__ywjbu.null_bitmap = tmet__bvwd
        context.nrt.incref(builder, signature.args[0], ytk__ndd)
        context.nrt.incref(builder, signature.args[1], fju__qri)
        context.nrt.incref(builder, signature.args[2], fkqjx__pseve)
        context.nrt.incref(builder, signature.args[3], tmet__bvwd)
        return bgps__ywjbu._getvalue()
    fqg__wvcsq = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return fqg__wvcsq, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    mvuk__jglp = np.empty(n, np.int64)
    nyc__ttl = np.empty(n, np.int64)
    tmgc__qzrc = np.empty(n, np.int64)
    brz__vvij = np.empty(n + 7 >> 3, np.uint8)
    for ykod__rau, s in enumerate(pyval):
        clp__vhlfu = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(brz__vvij, ykod__rau, int(not
            clp__vhlfu))
        if not clp__vhlfu:
            mvuk__jglp[ykod__rau] = s.days
            nyc__ttl[ykod__rau] = s.seconds
            tmgc__qzrc[ykod__rau] = s.microseconds
    wpbpg__npo = context.get_constant_generic(builder, days_data_type,
        mvuk__jglp)
    jeq__repiy = context.get_constant_generic(builder, seconds_data_type,
        nyc__ttl)
    qgr__wqpe = context.get_constant_generic(builder,
        microseconds_data_type, tmgc__qzrc)
    qecl__hrqkd = context.get_constant_generic(builder, nulls_type, brz__vvij)
    return lir.Constant.literal_struct([wpbpg__npo, jeq__repiy, qgr__wqpe,
        qecl__hrqkd])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    mvuk__jglp = np.empty(n, dtype=np.int64)
    nyc__ttl = np.empty(n, dtype=np.int64)
    tmgc__qzrc = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(mvuk__jglp, nyc__ttl, tmgc__qzrc,
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
            dox__oecsb = bodo.utils.conversion.coerce_to_array(ind)
            fmsm__nbdqp = A._null_bitmap
            xblsq__dpi = A._days_data[dox__oecsb]
            iosjo__wag = A._seconds_data[dox__oecsb]
            ojg__woloz = A._microseconds_data[dox__oecsb]
            n = len(xblsq__dpi)
            dnoz__sphgi = get_new_null_mask_bool_index(fmsm__nbdqp, ind, n)
            return init_datetime_timedelta_array(xblsq__dpi, iosjo__wag,
                ojg__woloz, dnoz__sphgi)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            dox__oecsb = bodo.utils.conversion.coerce_to_array(ind)
            fmsm__nbdqp = A._null_bitmap
            xblsq__dpi = A._days_data[dox__oecsb]
            iosjo__wag = A._seconds_data[dox__oecsb]
            ojg__woloz = A._microseconds_data[dox__oecsb]
            n = len(xblsq__dpi)
            dnoz__sphgi = get_new_null_mask_int_index(fmsm__nbdqp,
                dox__oecsb, n)
            return init_datetime_timedelta_array(xblsq__dpi, iosjo__wag,
                ojg__woloz, dnoz__sphgi)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            fmsm__nbdqp = A._null_bitmap
            xblsq__dpi = np.ascontiguousarray(A._days_data[ind])
            iosjo__wag = np.ascontiguousarray(A._seconds_data[ind])
            ojg__woloz = np.ascontiguousarray(A._microseconds_data[ind])
            dnoz__sphgi = get_new_null_mask_slice_index(fmsm__nbdqp, ind, n)
            return init_datetime_timedelta_array(xblsq__dpi, iosjo__wag,
                ojg__woloz, dnoz__sphgi)
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
    ahoqt__ehvs = (
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
            raise BodoError(ahoqt__ehvs)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(ahoqt__ehvs)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for ykod__rau in range(n):
                    A._days_data[ind[ykod__rau]] = val._days
                    A._seconds_data[ind[ykod__rau]] = val._seconds
                    A._microseconds_data[ind[ykod__rau]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[ykod__rau], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for ykod__rau in range(n):
                    A._days_data[ind[ykod__rau]] = val._days_data[ykod__rau]
                    A._seconds_data[ind[ykod__rau]] = val._seconds_data[
                        ykod__rau]
                    A._microseconds_data[ind[ykod__rau]
                        ] = val._microseconds_data[ykod__rau]
                    osia__lno = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, ykod__rau)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[ykod__rau], osia__lno)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for ykod__rau in range(n):
                    if not bodo.libs.array_kernels.isna(ind, ykod__rau
                        ) and ind[ykod__rau]:
                        A._days_data[ykod__rau] = val._days
                        A._seconds_data[ykod__rau] = val._seconds
                        A._microseconds_data[ykod__rau] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            ykod__rau, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                jjx__qszyy = 0
                for ykod__rau in range(n):
                    if not bodo.libs.array_kernels.isna(ind, ykod__rau
                        ) and ind[ykod__rau]:
                        A._days_data[ykod__rau] = val._days_data[jjx__qszyy]
                        A._seconds_data[ykod__rau] = val._seconds_data[
                            jjx__qszyy]
                        A._microseconds_data[ykod__rau
                            ] = val._microseconds_data[jjx__qszyy]
                        osia__lno = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, jjx__qszyy)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            ykod__rau, osia__lno)
                        jjx__qszyy += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                kuhit__zli = numba.cpython.unicode._normalize_slice(ind, len(A)
                    )
                for ykod__rau in range(kuhit__zli.start, kuhit__zli.stop,
                    kuhit__zli.step):
                    A._days_data[ykod__rau] = val._days
                    A._seconds_data[ykod__rau] = val._seconds
                    A._microseconds_data[ykod__rau] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ykod__rau, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                ewzwf__cee = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, ewzwf__cee,
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
            ytrzx__qvy = arg1
            numba.parfors.parfor.init_prange()
            n = len(ytrzx__qvy)
            A = alloc_datetime_timedelta_array(n)
            for ykod__rau in numba.parfors.parfor.internal_prange(n):
                A[ykod__rau] = ytrzx__qvy[ykod__rau] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            wwvd__tcf = True
        else:
            wwvd__tcf = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                sqq__bcc = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for ykod__rau in numba.parfors.parfor.internal_prange(n):
                    pjlz__hfg = bodo.libs.array_kernels.isna(lhs, ykod__rau)
                    xnrcv__vtpmp = bodo.libs.array_kernels.isna(rhs, ykod__rau)
                    if pjlz__hfg or xnrcv__vtpmp:
                        vjaqq__zvdtm = wwvd__tcf
                    else:
                        vjaqq__zvdtm = op(lhs[ykod__rau], rhs[ykod__rau])
                    sqq__bcc[ykod__rau] = vjaqq__zvdtm
                return sqq__bcc
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                sqq__bcc = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for ykod__rau in numba.parfors.parfor.internal_prange(n):
                    osia__lno = bodo.libs.array_kernels.isna(lhs, ykod__rau)
                    if osia__lno:
                        vjaqq__zvdtm = wwvd__tcf
                    else:
                        vjaqq__zvdtm = op(lhs[ykod__rau], rhs)
                    sqq__bcc[ykod__rau] = vjaqq__zvdtm
                return sqq__bcc
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                sqq__bcc = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for ykod__rau in numba.parfors.parfor.internal_prange(n):
                    osia__lno = bodo.libs.array_kernels.isna(rhs, ykod__rau)
                    if osia__lno:
                        vjaqq__zvdtm = wwvd__tcf
                    else:
                        vjaqq__zvdtm = op(lhs, rhs[ykod__rau])
                    sqq__bcc[ykod__rau] = vjaqq__zvdtm
                return sqq__bcc
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for gsygp__noum in timedelta_unsupported_attrs:
        qmt__oobb = 'pandas.Timedelta.' + gsygp__noum
        overload_attribute(PDTimeDeltaType, gsygp__noum)(
            create_unsupported_overload(qmt__oobb))
    for tyrpk__ykzv in timedelta_unsupported_methods:
        qmt__oobb = 'pandas.Timedelta.' + tyrpk__ykzv
        overload_method(PDTimeDeltaType, tyrpk__ykzv)(
            create_unsupported_overload(qmt__oobb + '()'))


_intstall_pd_timedelta_unsupported()
