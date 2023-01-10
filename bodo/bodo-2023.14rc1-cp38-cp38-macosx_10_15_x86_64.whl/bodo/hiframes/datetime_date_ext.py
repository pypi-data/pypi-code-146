"""Numba extension support for datetime.date objects and their arrays.
"""
import datetime
import operator
import warnings
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.typing.templates import AttributeTemplate, infer_getattr
from numba.core.utils import PYVERSION
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import DatetimeDatetimeType
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type, is_overload_int, is_overload_none
ll.add_symbol('box_datetime_date_array', hdatetime_ext.box_datetime_date_array)
ll.add_symbol('unbox_datetime_date_array', hdatetime_ext.
    unbox_datetime_date_array)
ll.add_symbol('get_isocalendar', hdatetime_ext.get_isocalendar)


class DatetimeDateType(types.Type):

    def __init__(self):
        super(DatetimeDateType, self).__init__(name='DatetimeDateType()')
        self.bitwidth = 64


datetime_date_type = DatetimeDateType()


@typeof_impl.register(datetime.date)
def typeof_datetime_date(val, c):
    return datetime_date_type


register_model(DatetimeDateType)(models.IntegerModel)


@infer_getattr
class DatetimeAttribute(AttributeTemplate):
    key = DatetimeDateType

    def resolve_year(self, typ):
        return types.int64

    def resolve_month(self, typ):
        return types.int64

    def resolve_day(self, typ):
        return types.int64


@lower_getattr(DatetimeDateType, 'year')
def datetime_get_year(context, builder, typ, val):
    return builder.lshr(val, lir.Constant(lir.IntType(64), 32))


@lower_getattr(DatetimeDateType, 'month')
def datetime_get_month(context, builder, typ, val):
    return builder.and_(builder.lshr(val, lir.Constant(lir.IntType(64), 16)
        ), lir.Constant(lir.IntType(64), 65535))


@lower_getattr(DatetimeDateType, 'day')
def datetime_get_day(context, builder, typ, val):
    return builder.and_(val, lir.Constant(lir.IntType(64), 65535))


@unbox(DatetimeDateType)
def unbox_datetime_date(typ, val, c):
    xzrq__kjk = c.pyapi.object_getattr_string(val, 'year')
    avc__pobk = c.pyapi.object_getattr_string(val, 'month')
    ifpu__fqcud = c.pyapi.object_getattr_string(val, 'day')
    jbma__eet = c.pyapi.long_as_longlong(xzrq__kjk)
    unlf__cek = c.pyapi.long_as_longlong(avc__pobk)
    rkbe__pht = c.pyapi.long_as_longlong(ifpu__fqcud)
    bzf__drlhc = c.builder.add(rkbe__pht, c.builder.add(c.builder.shl(
        jbma__eet, lir.Constant(lir.IntType(64), 32)), c.builder.shl(
        unlf__cek, lir.Constant(lir.IntType(64), 16))))
    c.pyapi.decref(xzrq__kjk)
    c.pyapi.decref(avc__pobk)
    c.pyapi.decref(ifpu__fqcud)
    zsjay__yqtkt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bzf__drlhc, is_error=zsjay__yqtkt)


@lower_constant(DatetimeDateType)
def lower_constant_datetime_date(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    bzf__drlhc = builder.add(day, builder.add(builder.shl(year, lir.
        Constant(lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir
        .IntType(64), 16))))
    return bzf__drlhc


@box(DatetimeDateType)
def box_datetime_date(typ, val, c):
    xzrq__kjk = c.pyapi.long_from_longlong(c.builder.lshr(val, lir.Constant
        (lir.IntType(64), 32)))
    avc__pobk = c.pyapi.long_from_longlong(c.builder.and_(c.builder.lshr(
        val, lir.Constant(lir.IntType(64), 16)), lir.Constant(lir.IntType(
        64), 65535)))
    ifpu__fqcud = c.pyapi.long_from_longlong(c.builder.and_(val, lir.
        Constant(lir.IntType(64), 65535)))
    meja__ogpmi = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.date))
    ahr__pze = c.pyapi.call_function_objargs(meja__ogpmi, (xzrq__kjk,
        avc__pobk, ifpu__fqcud))
    c.pyapi.decref(xzrq__kjk)
    c.pyapi.decref(avc__pobk)
    c.pyapi.decref(ifpu__fqcud)
    c.pyapi.decref(meja__ogpmi)
    return ahr__pze


@type_callable(datetime.date)
def type_datetime_date(context):

    def typer(year, month, day):
        return datetime_date_type
    return typer


@lower_builtin(datetime.date, types.IntegerLiteral, types.IntegerLiteral,
    types.IntegerLiteral)
@lower_builtin(datetime.date, types.int64, types.int64, types.int64)
def impl_ctor_datetime_date(context, builder, sig, args):
    year, month, day = args
    bzf__drlhc = builder.add(day, builder.add(builder.shl(year, lir.
        Constant(lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir
        .IntType(64), 16))))
    return bzf__drlhc


@intrinsic
def cast_int_to_datetime_date(typingctx, val=None):
    assert val == types.int64

    def codegen(context, builder, signature, args):
        return args[0]
    return datetime_date_type(types.int64), codegen


@intrinsic
def cast_datetime_date_to_int(typingctx, val=None):
    assert val == datetime_date_type

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(datetime_date_type), codegen


"""
Following codes are copied from
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""
_MAXORDINAL = 3652059
_DAYS_IN_MONTH = np.array([-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 
    31], dtype=np.int64)
_DAYS_BEFORE_MONTH = np.array([-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 
    273, 304, 334], dtype=np.int64)


@register_jitable
def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


@register_jitable
def _days_before_year(year):
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


@register_jitable
def _days_in_month(year, month):
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


@register_jitable
def _days_before_month(year, month):
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


_DI400Y = _days_before_year(401)
_DI100Y = _days_before_year(101)
_DI4Y = _days_before_year(5)


@register_jitable
def _ymd2ord(year, month, day):
    vsd__ghhxj = _days_in_month(year, month)
    return _days_before_year(year) + _days_before_month(year, month) + day


@register_jitable
def _ord2ymd(n):
    n -= 1
    pmi__kbz, n = divmod(n, _DI400Y)
    year = pmi__kbz * 400 + 1
    ouhvf__uffp, n = divmod(n, _DI100Y)
    lqod__hlx, n = divmod(n, _DI4Y)
    vkz__uxgf, n = divmod(n, 365)
    year += ouhvf__uffp * 100 + lqod__hlx * 4 + vkz__uxgf
    if vkz__uxgf == 4 or ouhvf__uffp == 4:
        return year - 1, 12, 31
    wdufp__bayr = vkz__uxgf == 3 and (lqod__hlx != 24 or ouhvf__uffp == 3)
    month = n + 50 >> 5
    arb__jnu = _DAYS_BEFORE_MONTH[month] + (month > 2 and wdufp__bayr)
    if arb__jnu > n:
        month -= 1
        arb__jnu -= _DAYS_IN_MONTH[month] + (month == 2 and wdufp__bayr)
    n -= arb__jnu
    return year, month, n + 1


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@intrinsic
def get_isocalendar(typingctx, dt_year, dt_month, dt_day):

    def codegen(context, builder, sig, args):
        year = cgutils.alloca_once(builder, lir.IntType(64))
        wbtw__fvx = cgutils.alloca_once(builder, lir.IntType(64))
        hoi__zzyn = cgutils.alloca_once(builder, lir.IntType(64))
        vqfgg__evi = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir
            .IntType(64), lir.IntType(64), lir.IntType(64).as_pointer(),
            lir.IntType(64).as_pointer(), lir.IntType(64).as_pointer()])
        prkb__lxt = cgutils.get_or_insert_function(builder.module,
            vqfgg__evi, name='get_isocalendar')
        builder.call(prkb__lxt, [args[0], args[1], args[2], year, wbtw__fvx,
            hoi__zzyn])
        return cgutils.pack_array(builder, [builder.load(year), builder.
            load(wbtw__fvx), builder.load(hoi__zzyn)])
    ahr__pze = types.Tuple([types.int64, types.int64, types.int64])(types.
        int64, types.int64, types.int64), codegen
    return ahr__pze


types.datetime_date_type = datetime_date_type


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_date_type'):
        d = datetime.date.today()
    return d


@register_jitable
def fromordinal_impl(n):
    y, dzx__zmw, d = _ord2ymd(n)
    return datetime.date(y, dzx__zmw, d)


@overload_method(DatetimeDateType, 'replace')
def replace_overload(date, year=None, month=None, day=None):
    if not is_overload_none(year) and not is_overload_int(year):
        raise BodoError('date.replace(): year must be an integer')
    elif not is_overload_none(month) and not is_overload_int(month):
        raise BodoError('date.replace(): month must be an integer')
    elif not is_overload_none(day) and not is_overload_int(day):
        raise BodoError('date.replace(): day must be an integer')

    def impl(date, year=None, month=None, day=None):
        ixqw__qobcd = date.year if year is None else year
        tduwm__bypr = date.month if month is None else month
        wdxc__kiasc = date.day if day is None else day
        return datetime.date(ixqw__qobcd, tduwm__bypr, wdxc__kiasc)
    return impl


@overload_method(DatetimeDatetimeType, 'toordinal', no_unliteral=True)
@overload_method(DatetimeDateType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


@overload_method(DatetimeDatetimeType, 'weekday', no_unliteral=True)
@overload_method(DatetimeDateType, 'weekday', no_unliteral=True)
def weekday(date):

    def impl(date):
        return (date.toordinal() + 6) % 7
    return impl


@overload_method(DatetimeDateType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(date):

    def impl(date):
        year, wbtw__fvx, uxbz__gjbtq = get_isocalendar(date.year, date.
            month, date.day)
        return year, wbtw__fvx, uxbz__gjbtq
    return impl


def overload_add_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            rzz__whfb = lhs.toordinal() + rhs.days
            if 0 < rzz__whfb <= _MAXORDINAL:
                return fromordinal_impl(rzz__whfb)
            raise OverflowError('result out of range')
        return impl
    elif lhs == datetime_timedelta_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            rzz__whfb = lhs.days + rhs.toordinal()
            if 0 < rzz__whfb <= _MAXORDINAL:
                return fromordinal_impl(rzz__whfb)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + datetime.timedelta(-rhs.days)
        return impl
    elif lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            lpnyl__ode = lhs.toordinal()
            cyh__bszpn = rhs.toordinal()
            return datetime.timedelta(lpnyl__ode - cyh__bszpn)
        return impl
    if lhs == datetime_date_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            iscs__jwme = lhs
            numba.parfors.parfor.init_prange()
            n = len(iscs__jwme)
            A = alloc_datetime_date_array(n)
            for hejj__xxbha in numba.parfors.parfor.internal_prange(n):
                A[hejj__xxbha] = iscs__jwme[hejj__xxbha] - rhs
            return A
        return impl


@overload(min, no_unliteral=True)
def date_min(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def date_max(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        huo__mjrr = np.uint8(td.year // 256)
        xolss__mbd = np.uint8(td.year % 256)
        month = np.uint8(td.month)
        day = np.uint8(td.day)
        jmfw__zph = huo__mjrr, xolss__mbd, month, day
        return hash(jmfw__zph)
    return impl


@overload(bool, inline='always', no_unliteral=True)
def date_to_bool(date):
    if date != datetime_date_type:
        return

    def impl(date):
        return True
    return impl


if PYVERSION >= (3, 9):
    IsoCalendarDate = datetime.date(2011, 1, 1).isocalendar().__class__


    class IsoCalendarDateType(types.Type):

        def __init__(self):
            super(IsoCalendarDateType, self).__init__(name=
                'IsoCalendarDateType()')
    iso_calendar_date_type = DatetimeDateType()

    @typeof_impl.register(IsoCalendarDate)
    def typeof_datetime_date(val, c):
        return iso_calendar_date_type


class DatetimeDateArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeDateArrayType, self).__init__(name=
            'DatetimeDateArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_date_type

    def copy(self):
        return DatetimeDateArrayType()


datetime_date_array_type = DatetimeDateArrayType()
types.datetime_date_array_type = datetime_date_array_type
data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeDateArrayType)
class DatetimeDateArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bfb__vbt = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, bfb__vbt)


make_attribute_wrapper(DatetimeDateArrayType, 'data', '_data')
make_attribute_wrapper(DatetimeDateArrayType, 'null_bitmap', '_null_bitmap')


@overload_method(DatetimeDateArrayType, 'copy', no_unliteral=True)
def overload_datetime_date_arr_copy(A):
    return lambda A: bodo.hiframes.datetime_date_ext.init_datetime_date_array(A
        ._data.copy(), A._null_bitmap.copy())


@overload_attribute(DatetimeDateArrayType, 'dtype')
def overload_datetime_date_arr_dtype(A):
    return lambda A: np.object_


@unbox(DatetimeDateArrayType)
def unbox_datetime_date_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    lanq__qyzi = types.Array(types.intp, 1, 'C')
    tzv__rup = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        lanq__qyzi, [n])
    hgxl__fwm = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    xqyhf__syznv = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [hgxl__fwm])
    vqfgg__evi = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(8).as_pointer()])
    bng__scyb = cgutils.get_or_insert_function(c.builder.module, vqfgg__evi,
        name='unbox_datetime_date_array')
    c.builder.call(bng__scyb, [val, n, tzv__rup.data, xqyhf__syznv.data])
    jlttz__sslz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jlttz__sslz.data = tzv__rup._getvalue()
    jlttz__sslz.null_bitmap = xqyhf__syznv._getvalue()
    zsjay__yqtkt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(jlttz__sslz._getvalue(), is_error=zsjay__yqtkt)


def int_to_datetime_date_python(ia):
    return datetime.date(ia >> 32, ia >> 16 & 65535, ia & 65535)


def int_array_to_datetime_date(ia):
    return np.vectorize(int_to_datetime_date_python, otypes=[object])(ia)


@box(DatetimeDateArrayType)
def box_datetime_date_array(typ, val, c):
    iscs__jwme = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    tzv__rup = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, iscs__jwme.data)
    eoym__dlfo = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, iscs__jwme.null_bitmap).data
    n = c.builder.extract_value(tzv__rup.shape, 0)
    vqfgg__evi = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(8).as_pointer()])
    owg__ieyw = cgutils.get_or_insert_function(c.builder.module, vqfgg__evi,
        name='box_datetime_date_array')
    ixsa__lck = c.builder.call(owg__ieyw, [n, tzv__rup.data, eoym__dlfo])
    c.context.nrt.decref(c.builder, typ, val)
    return ixsa__lck


@intrinsic
def init_datetime_date_array(typingctx, data, nulls=None):
    assert data == types.Array(types.int64, 1, 'C') or data == types.Array(
        types.NPDatetime('ns'), 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        vdpv__ngtf, xzub__ylior = args
        liowy__rlzq = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        liowy__rlzq.data = vdpv__ngtf
        liowy__rlzq.null_bitmap = xzub__ylior
        context.nrt.incref(builder, signature.args[0], vdpv__ngtf)
        context.nrt.incref(builder, signature.args[1], xzub__ylior)
        return liowy__rlzq._getvalue()
    sig = datetime_date_array_type(data, nulls)
    return sig, codegen


@lower_constant(DatetimeDateArrayType)
def lower_constant_datetime_date_arr(context, builder, typ, pyval):
    n = len(pyval)
    bvkdf__vxjy = (1970 << 32) + (1 << 16) + 1
    tzv__rup = np.full(n, bvkdf__vxjy, np.int64)
    olgx__jnmix = np.empty(n + 7 >> 3, np.uint8)
    for hejj__xxbha, hjnd__zqqn in enumerate(pyval):
        fyod__ayjo = pd.isna(hjnd__zqqn)
        bodo.libs.int_arr_ext.set_bit_to_arr(olgx__jnmix, hejj__xxbha, int(
            not fyod__ayjo))
        if not fyod__ayjo:
            tzv__rup[hejj__xxbha] = (hjnd__zqqn.year << 32) + (hjnd__zqqn.
                month << 16) + hjnd__zqqn.day
    xxn__trmdy = context.get_constant_generic(builder, data_type, tzv__rup)
    czpg__enecj = context.get_constant_generic(builder, nulls_type, olgx__jnmix
        )
    return lir.Constant.literal_struct([xxn__trmdy, czpg__enecj])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_date_array(n):
    tzv__rup = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_date_array(tzv__rup, nulls)


def alloc_datetime_date_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_date_ext_alloc_datetime_date_array
    ) = alloc_datetime_date_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_date_arr_getitem(A, ind):
    if A != datetime_date_array_type:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: cast_int_to_datetime_date(A._data[ind])
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            kaeqs__gdcf, uksls__otugo = array_getitem_bool_index(A, ind)
            return init_datetime_date_array(kaeqs__gdcf, uksls__otugo)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            kaeqs__gdcf, uksls__otugo = array_getitem_int_index(A, ind)
            return init_datetime_date_array(kaeqs__gdcf, uksls__otugo)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            kaeqs__gdcf, uksls__otugo = array_getitem_slice_index(A, ind)
            return init_datetime_date_array(kaeqs__gdcf, uksls__otugo)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for DatetimeDateArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def dt_date_arr_setitem(A, idx, val):
    if A != datetime_date_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    fwv__owuwx = (
        f"setitem for DatetimeDateArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == datetime_date_type:

            def impl(A, idx, val):
                A._data[idx] = cast_datetime_date_to_int(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl
        else:
            raise BodoError(fwv__owuwx)
    if not (is_iterable_type(val) and val.dtype == bodo.datetime_date_type or
        types.unliteral(val) == datetime_date_type):
        raise BodoError(fwv__owuwx)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_int_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_arr_ind(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_bool_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_slice_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeDateArray with indexing type {idx} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_date_arr(A):
    if A == datetime_date_array_type:
        return lambda A: len(A._data)


@overload_attribute(DatetimeDateArrayType, 'shape')
def overload_datetime_date_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DatetimeDateArrayType, 'nbytes')
def datetime_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


def create_cmp_op_overload(op):

    def overload_date_cmp(lhs, rhs):
        if lhs == datetime_date_type and rhs == datetime_date_type:

            def impl(lhs, rhs):
                y, rzeja__hns = lhs.year, rhs.year
                dzx__zmw, rlu__kdzu = lhs.month, rhs.month
                d, ckxe__xldg = lhs.day, rhs.day
                return op(_cmp((y, dzx__zmw, d), (rzeja__hns, rlu__kdzu,
                    ckxe__xldg)), 0)
            return impl
    return overload_date_cmp


def create_datetime_date_cmp_op_overload(op):

    def overload_cmp(lhs, rhs):
        yidy__wghwh = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[op]} {rhs} is always {op == operator.ne} in Python. If this is unexpected there may be a bug in your code.'
            )
        warnings.warn(yidy__wghwh, bodo.utils.typing.BodoWarning)
        if op == operator.eq:
            return lambda lhs, rhs: False
        elif op == operator.ne:
            return lambda lhs, rhs: True
    return overload_cmp


def create_datetime_array_date_cmp_op_overload(op):

    def overload_arr_cmp(lhs, rhs):
        if isinstance(lhs, types.Array) and lhs.dtype == bodo.datetime64ns:
            if rhs == datetime_date_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(lhs)
                    qac__fmj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for hejj__xxbha in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, hejj__xxbha):
                            bodo.libs.array_kernels.setna(qac__fmj, hejj__xxbha
                                )
                        else:
                            qac__fmj[hejj__xxbha] = op(lhs[hejj__xxbha],
                                bodo.utils.conversion.
                                unbox_if_tz_naive_timestamp(pd.Timestamp(rhs)))
                    return qac__fmj
                return impl
            elif rhs == datetime_date_array_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(lhs)
                    qac__fmj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for hejj__xxbha in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, hejj__xxbha
                            ) or bodo.libs.array_kernels.isna(rhs, hejj__xxbha
                            ):
                            bodo.libs.array_kernels.setna(qac__fmj, hejj__xxbha
                                )
                        else:
                            qac__fmj[hejj__xxbha] = op(lhs[hejj__xxbha],
                                bodo.utils.conversion.
                                unbox_if_tz_naive_timestamp(pd.Timestamp(
                                rhs[hejj__xxbha])))
                    return qac__fmj
                return impl
        elif isinstance(rhs, types.Array) and rhs.dtype == bodo.datetime64ns:
            if lhs == datetime_date_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(rhs)
                    qac__fmj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for hejj__xxbha in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(rhs, hejj__xxbha):
                            bodo.libs.array_kernels.setna(qac__fmj, hejj__xxbha
                                )
                        else:
                            qac__fmj[hejj__xxbha] = op(bodo.utils.
                                conversion.unbox_if_tz_naive_timestamp(pd.
                                Timestamp(lhs)), rhs[hejj__xxbha])
                    return qac__fmj
                return impl
            elif lhs == datetime_date_array_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(rhs)
                    qac__fmj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for hejj__xxbha in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, hejj__xxbha
                            ) or bodo.libs.array_kernels.isna(rhs, hejj__xxbha
                            ):
                            bodo.libs.array_kernels.setna(qac__fmj, hejj__xxbha
                                )
                        else:
                            qac__fmj[hejj__xxbha] = op(bodo.utils.
                                conversion.unbox_if_tz_naive_timestamp(pd.
                                Timestamp(lhs[hejj__xxbha])), rhs[hejj__xxbha])
                    return qac__fmj
                return impl
    return overload_arr_cmp


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            czuu__omq = True
        else:
            czuu__omq = False
        if lhs == datetime_date_array_type and rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                qac__fmj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for hejj__xxbha in numba.parfors.parfor.internal_prange(n):
                    mcxz__vcsm = bodo.libs.array_kernels.isna(lhs, hejj__xxbha)
                    afnzg__ahn = bodo.libs.array_kernels.isna(rhs, hejj__xxbha)
                    if mcxz__vcsm or afnzg__ahn:
                        ulum__xorlo = czuu__omq
                    else:
                        ulum__xorlo = op(lhs[hejj__xxbha], rhs[hejj__xxbha])
                    qac__fmj[hejj__xxbha] = ulum__xorlo
                return qac__fmj
            return impl
        elif lhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                qac__fmj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for hejj__xxbha in numba.parfors.parfor.internal_prange(n):
                    nap__uvin = bodo.libs.array_kernels.isna(lhs, hejj__xxbha)
                    if nap__uvin:
                        ulum__xorlo = czuu__omq
                    else:
                        ulum__xorlo = op(lhs[hejj__xxbha], rhs)
                    qac__fmj[hejj__xxbha] = ulum__xorlo
                return qac__fmj
            return impl
        elif rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                qac__fmj = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for hejj__xxbha in numba.parfors.parfor.internal_prange(n):
                    nap__uvin = bodo.libs.array_kernels.isna(rhs, hejj__xxbha)
                    if nap__uvin:
                        ulum__xorlo = czuu__omq
                    else:
                        ulum__xorlo = op(lhs, rhs[hejj__xxbha])
                    qac__fmj[hejj__xxbha] = ulum__xorlo
                return qac__fmj
            return impl
    return overload_date_arr_cmp
