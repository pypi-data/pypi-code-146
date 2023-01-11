"""DatetimeArray extension for Pandas DatetimeArray with timezone support."""
import operator
import numba
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoArrayIterator, BodoError, get_literal_value, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str


class PandasDatetimeTZDtype(types.Type):

    def __init__(self, tz):
        if isinstance(tz, (pytz._FixedOffset, pytz.tzinfo.BaseTzInfo)):
            tz = get_pytz_type_info(tz)
        if not isinstance(tz, (int, str)):
            raise BodoError(
                'Timezone must be either a valid pytz type with a zone or a fixed offset'
                )
        self.tz = tz
        super(PandasDatetimeTZDtype, self).__init__(name=
            f'PandasDatetimeTZDtype[{tz}]')


register_model(PandasDatetimeTZDtype)(models.OpaqueModel)


@lower_constant(PandasDatetimeTZDtype)
def lower_constant_pd_datetime_tz_dtype(context, builder, typ, pyval):
    return context.get_dummy_value()


@box(PandasDatetimeTZDtype)
def box_pd_datetime_tzdtype(typ, val, c):
    moq__gswb = c.context.insert_const_string(c.builder.module, 'pandas')
    joteh__xrhr = c.pyapi.import_module_noblock(moq__gswb)
    kvj__bvoej = c.context.get_constant_generic(c.builder, types.
        unicode_type, 'ns')
    lrrmk__cvbtm = c.pyapi.from_native_value(types.unicode_type, kvj__bvoej,
        c.env_manager)
    if isinstance(typ.tz, str):
        kpyzi__ugs = c.context.get_constant_generic(c.builder, types.
            unicode_type, typ.tz)
        luucj__awczd = c.pyapi.from_native_value(types.unicode_type,
            kpyzi__ugs, c.env_manager)
    else:
        gcq__sws = nanoseconds_to_offset(typ.tz)
        luucj__awczd = c.pyapi.unserialize(c.pyapi.serialize_object(gcq__sws))
    xwwd__ubs = c.pyapi.call_method(joteh__xrhr, 'DatetimeTZDtype', (
        lrrmk__cvbtm, luucj__awczd))
    c.pyapi.decref(lrrmk__cvbtm)
    c.pyapi.decref(luucj__awczd)
    c.pyapi.decref(joteh__xrhr)
    c.context.nrt.decref(c.builder, typ, val)
    return xwwd__ubs


@unbox(PandasDatetimeTZDtype)
def unbox_pd_datetime_tzdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


@typeof_impl.register(pd.DatetimeTZDtype)
def typeof_pd_int_dtype(val, c):
    return PandasDatetimeTZDtype(val.tz)


def get_pytz_type_info(pytz_type):
    if isinstance(pytz_type, pytz._FixedOffset):
        kten__ntzt = pd.Timedelta(pytz_type._offset).value
    else:
        kten__ntzt = pytz_type.zone
        if kten__ntzt not in pytz.all_timezones_set:
            raise BodoError(
                'Unsupported timezone type. Timezones must be a fixedOffset or contain a zone found in pytz.all_timezones'
                )
    return kten__ntzt


def nanoseconds_to_offset(nanoseconds):
    kqd__imc = nanoseconds // (60 * 1000 * 1000 * 1000)
    return pytz.FixedOffset(kqd__imc)


class DatetimeArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, tz):
        if isinstance(tz, (pytz._FixedOffset, pytz.tzinfo.BaseTzInfo)):
            tz = get_pytz_type_info(tz)
        if not isinstance(tz, (int, str)):
            raise BodoError(
                'Timezone must be either a valid pytz type with a zone or a fixed offset'
                )
        self.tz = tz
        self._data_array_type = types.Array(types.NPDatetime('ns'), 1, 'C')
        self._dtype = PandasDatetimeTZDtype(tz)
        super(DatetimeArrayType, self).__init__(name=
            f'PandasDatetimeArray[{tz}]')

    @property
    def data_array_type(self):
        return self._data_array_type

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self._dtype

    def copy(self):
        return DatetimeArrayType(self.tz)


@register_model(DatetimeArrayType)
class PandasDatetimeArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ewkba__yayac = [('data', fe_type.data_array_type)]
        models.StructModel.__init__(self, dmm, fe_type, ewkba__yayac)


make_attribute_wrapper(DatetimeArrayType, 'data', '_data')


@typeof_impl.register(pd.arrays.DatetimeArray)
def typeof_pd_datetime_array(val, c):
    if val.tz is None:
        raise BodoError(
            "Cannot support timezone naive pd.arrays.DatetimeArray. Please convert to a numpy array with .astype('datetime64[ns]')."
            )
    if val.dtype.unit != 'ns':
        raise BodoError("Timezone-aware datetime data requires 'ns' units")
    return DatetimeArrayType(val.dtype.tz)


@unbox(DatetimeArrayType)
def unbox_pd_datetime_array(typ, val, c):
    gfz__ujz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cuqb__tihmw = c.pyapi.string_from_constant_string('datetime64[ns]')
    crci__dge = c.pyapi.call_method(val, 'to_numpy', (cuqb__tihmw,))
    gfz__ujz.data = c.unbox(typ.data_array_type, crci__dge).value
    c.pyapi.decref(crci__dge)
    oet__xvvmn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gfz__ujz._getvalue(), is_error=oet__xvvmn)


@box(DatetimeArrayType)
def box_pd_datetime_array(typ, val, c):
    gfz__ujz = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    c.context.nrt.incref(c.builder, typ.data_array_type, gfz__ujz.data)
    vgeo__sfk = c.pyapi.from_native_value(typ.data_array_type, gfz__ujz.
        data, c.env_manager)
    kvj__bvoej = c.context.get_constant_generic(c.builder, types.
        unicode_type, 'ns')
    lrrmk__cvbtm = c.pyapi.from_native_value(types.unicode_type, kvj__bvoej,
        c.env_manager)
    if isinstance(typ.tz, str):
        kpyzi__ugs = c.context.get_constant_generic(c.builder, types.
            unicode_type, typ.tz)
        luucj__awczd = c.pyapi.from_native_value(types.unicode_type,
            kpyzi__ugs, c.env_manager)
    else:
        gcq__sws = nanoseconds_to_offset(typ.tz)
        luucj__awczd = c.pyapi.unserialize(c.pyapi.serialize_object(gcq__sws))
    moq__gswb = c.context.insert_const_string(c.builder.module, 'pandas')
    joteh__xrhr = c.pyapi.import_module_noblock(moq__gswb)
    xixdx__xmawo = c.pyapi.call_method(joteh__xrhr, 'DatetimeTZDtype', (
        lrrmk__cvbtm, luucj__awczd))
    zggk__vscyh = c.pyapi.object_getattr_string(joteh__xrhr, 'arrays')
    xwwd__ubs = c.pyapi.call_method(zggk__vscyh, 'DatetimeArray', (
        vgeo__sfk, xixdx__xmawo))
    c.pyapi.decref(vgeo__sfk)
    c.pyapi.decref(lrrmk__cvbtm)
    c.pyapi.decref(luucj__awczd)
    c.pyapi.decref(joteh__xrhr)
    c.pyapi.decref(xixdx__xmawo)
    c.pyapi.decref(zggk__vscyh)
    c.context.nrt.decref(c.builder, typ, val)
    return xwwd__ubs


@intrinsic
def init_pandas_datetime_array(typingctx, data, tz):

    def codegen(context, builder, sig, args):
        data, tz = args
        jea__fph = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        jea__fph.data = data
        context.nrt.incref(builder, sig.args[0], data)
        return jea__fph._getvalue()
    if is_overload_constant_str(tz) or is_overload_constant_int(tz):
        kpyzi__ugs = get_literal_value(tz)
    else:
        raise BodoError('tz must be a constant string or Fixed Offset')
    ksaaf__zbs = DatetimeArrayType(kpyzi__ugs)
    sig = ksaaf__zbs(ksaaf__zbs.data_array_type, tz)
    return sig, codegen


@numba.njit(no_cpython_wrapper=True)
def alloc_pd_datetime_array(n, tz):
    uciw__ngc = np.empty(n, dtype='datetime64[ns]')
    return init_pandas_datetime_array(uciw__ngc, tz)


def alloc_pd_datetime_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_pd_datetime_arr_ext_alloc_pd_datetime_array
    ) = alloc_pd_datetime_array_equiv


@overload(len, no_unliteral=True)
def overload_pd_datetime_arr_len(A):
    if isinstance(A, DatetimeArrayType):
        return lambda A: len(A._data)


@lower_constant(DatetimeArrayType)
def lower_constant_pd_datetime_arr(context, builder, typ, pyval):
    ehp__thi = context.get_constant_generic(builder, typ.data_array_type,
        pyval.to_numpy('datetime64[ns]'))
    opr__ihv = lir.Constant.literal_struct([ehp__thi])
    return opr__ihv


@overload_attribute(DatetimeArrayType, 'shape')
def overload_pd_datetime_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DatetimeArrayType, 'nbytes')
def overload_pd_datetime_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(DatetimeArrayType, 'tz_convert', no_unliteral=True)
def overload_pd_datetime_tz_convert(A, tz):
    if tz == types.none:

        def impl(A, tz):
            return A._data.copy()
        return impl
    else:

        def impl(A, tz):
            return init_pandas_datetime_array(A._data.copy(), tz)
    return impl


@overload_method(DatetimeArrayType, 'copy', no_unliteral=True)
def overload_pd_datetime_tz_convert(A):
    tz = A.tz

    def impl(A):
        return init_pandas_datetime_array(A._data.copy(), tz)
    return impl


@overload_attribute(DatetimeArrayType, 'dtype', no_unliteral=True)
def overload_pd_datetime_dtype(A):
    tz = A.tz
    dtype = pd.DatetimeTZDtype('ns', tz)

    def impl(A):
        return dtype
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_getitem(A, ind):
    if not isinstance(A, DatetimeArrayType):
        return
    tz = A.tz
    if isinstance(ind, types.Integer):

        def impl(A, ind):
            return bodo.hiframes.pd_timestamp_ext.convert_val_to_timestamp(bodo
                .hiframes.pd_timestamp_ext.dt64_to_integer(A._data[ind]), tz)
        return impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            jfeub__qmi = ensure_contig_if_np(A._data[ind])
            return init_pandas_datetime_array(jfeub__qmi, tz)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl_int_arr(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            jfeub__qmi = ensure_contig_if_np(A._data[ind])
            return init_pandas_datetime_array(jfeub__qmi, tz)
        return impl_int_arr
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            jfeub__qmi = ensure_contig_if_np(A._data[ind])
            return init_pandas_datetime_array(jfeub__qmi, tz)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            'operator.getitem with DatetimeArrayType is only supported with an integer index, int arr, boolean array, or slice.'
            )


@overload(operator.setitem, no_unliteral=True)
def overload_getitem(A, ind, val):
    if not isinstance(A, DatetimeArrayType):
        return
    tz = A.tz
    if isinstance(ind, types.Integer):
        if not isinstance(val, bodo.PandasTimestampType):
            raise BodoError(
                'operator.setitem with DatetimeArrayType requires a Timestamp value'
                )
        if val.tz != tz:
            raise BodoError(
                'operator.setitem with DatetimeArrayType requires the Timestamp value to share the same timezone'
                )

        def impl(A, ind, val):
            A._data[ind] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val
                .value)
        return impl
    raise BodoError(
        'operator.setitem with DatetimeArrayType is only supported with an integer index'
        )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def unwrap_tz_array(A):
    if isinstance(A, DatetimeArrayType):
        return lambda A: A._data
    return lambda A: A


def unwrap_tz_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ohbwf__mije = args[0]
    if equiv_set.has_shape(ohbwf__mije):
        return ArrayAnalysis.AnalyzeResult(shape=ohbwf__mije, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_pd_datetime_arr_ext_unwrap_tz_array
    ) = unwrap_tz_array_equiv


def create_cmp_op_overload_arr(op):
    from bodo.hiframes.pd_timestamp_ext import PandasTimestampType

    def overload_datetime_arr_cmp(lhs, rhs):
        if not (isinstance(lhs, DatetimeArrayType) or isinstance(rhs,
            DatetimeArrayType)):
            return
        if isinstance(lhs, DatetimeArrayType) and (isinstance(rhs,
            PandasTimestampType) or rhs == bodo.datetime_date_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                ntnz__rzox = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for pvq__uml in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, pvq__uml):
                        bodo.libs.array_kernels.setna(ntnz__rzox, pvq__uml)
                    else:
                        ntnz__rzox[pvq__uml] = op(lhs[pvq__uml], rhs)
                return ntnz__rzox
            return impl
        elif (isinstance(lhs, PandasTimestampType) or lhs == bodo.
            datetime_date_type) and isinstance(rhs, DatetimeArrayType):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                ntnz__rzox = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for pvq__uml in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, pvq__uml):
                        bodo.libs.array_kernels.setna(ntnz__rzox, pvq__uml)
                    else:
                        ntnz__rzox[pvq__uml] = op(lhs, rhs[pvq__uml])
                return ntnz__rzox
            return impl
        elif (isinstance(lhs, DatetimeArrayType) or lhs == bodo.
            datetime_date_array_type) and (isinstance(rhs,
            DatetimeArrayType) or rhs == bodo.datetime_date_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                ntnz__rzox = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for pvq__uml in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, pvq__uml
                        ) or bodo.libs.array_kernels.isna(rhs, pvq__uml):
                        bodo.libs.array_kernels.setna(ntnz__rzox, pvq__uml)
                    else:
                        ntnz__rzox[pvq__uml] = op(lhs[pvq__uml], rhs[pvq__uml])
                return ntnz__rzox
            return impl
        elif isinstance(lhs, DatetimeArrayType) and (isinstance(rhs, types.
            Array) and rhs.dtype == bodo.datetime64ns):
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[op]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {lhs.tz} and argument 1 is timezone-naive. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        elif (isinstance(lhs, types.Array) and lhs.dtype == bodo.datetime64ns
            ) and isinstance(rhs, DatetimeArrayType):
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[op]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 is timezone-naive and argument 1 has timezone {rhs.tz}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
    return overload_datetime_arr_cmp


def overload_add_operator_datetime_arr(lhs, rhs):
    if isinstance(lhs, DatetimeArrayType):
        if rhs == bodo.week_type:
            gcdv__zah = lhs.tz

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                ntnz__rzox = (bodo.libs.pd_datetime_arr_ext.
                    alloc_pd_datetime_array(n, gcdv__zah))
                for pvq__uml in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, pvq__uml):
                        bodo.libs.array_kernels.setna(ntnz__rzox, pvq__uml)
                    else:
                        ntnz__rzox[pvq__uml] = lhs[pvq__uml] + rhs
                return ntnz__rzox
            return impl
        else:
            raise BodoError(
                f'add operator not supported between Timezone-aware timestamp and {rhs}. Please convert to timezone naive with ts.tz_convert(None)'
                )
    elif lhs == bodo.week_type:
        gcdv__zah = rhs.tz

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            n = len(rhs)
            ntnz__rzox = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(
                n, gcdv__zah)
            for pvq__uml in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(rhs, pvq__uml):
                    bodo.libs.array_kernels.setna(ntnz__rzox, pvq__uml)
                else:
                    ntnz__rzox[pvq__uml] = lhs + rhs[pvq__uml]
            return ntnz__rzox
        return impl
    else:
        raise BodoError(
            f'add operator not supported between {lhs} and Timezone-aware timestamp. Please convert to timezone naive with ts.tz_convert(None)'
            )


@register_jitable
def convert_months_offset_to_days(curr_year, curr_month, curr_day, num_months):
    lfpg__qmkme = curr_month + num_months - 1
    gxrtf__ildg = lfpg__qmkme % 12 + 1
    jiz__cernv = lfpg__qmkme // 12
    nlrco__icogc = curr_year + jiz__cernv
    pjgfb__kkvw = bodo.hiframes.pd_timestamp_ext.get_days_in_month(nlrco__icogc
        , gxrtf__ildg)
    idchs__noqhi = min(pjgfb__kkvw, curr_day)
    yurfq__urvr = pd.Timestamp(year=curr_year, month=curr_month, day=curr_day)
    xfvg__xcy = pd.Timestamp(year=nlrco__icogc, month=gxrtf__ildg, day=
        idchs__noqhi)
    return xfvg__xcy - yurfq__urvr
