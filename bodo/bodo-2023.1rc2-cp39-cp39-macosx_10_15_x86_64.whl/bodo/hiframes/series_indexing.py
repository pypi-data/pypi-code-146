"""
Indexing support for Series objects, including loc/iloc/at/iat types.
"""
import operator
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.pd_timestamp_ext import convert_datetime64_to_timestamp, convert_numpy_timedelta64_to_pd_timedelta, integer_to_dt64, pd_timestamp_tz_naive_type
from bodo.utils.typing import BodoError, get_literal_value, get_overload_const_tuple, is_immutable_array, is_list_like_index_type, is_literal_type, is_overload_constant_str, is_overload_constant_tuple, is_scalar_type, raise_bodo_error


class SeriesIatType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        oqg__ybpur = 'SeriesIatType({})'.format(stype)
        super(SeriesIatType, self).__init__(oqg__ybpur)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 1


@register_model(SeriesIatType)
class SeriesIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jlqxw__jfw = [('obj', fe_type.stype)]
        super(SeriesIatModel, self).__init__(dmm, fe_type, jlqxw__jfw)


make_attribute_wrapper(SeriesIatType, 'obj', '_obj')


@intrinsic
def init_series_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        kwnaa__egbcb, = args
        lmvhy__wzowh = signature.return_type
        yxzs__qqzdl = cgutils.create_struct_proxy(lmvhy__wzowh)(context,
            builder)
        yxzs__qqzdl.obj = kwnaa__egbcb
        context.nrt.incref(builder, signature.args[0], kwnaa__egbcb)
        return yxzs__qqzdl._getvalue()
    return SeriesIatType(obj)(obj), codegen


@overload_attribute(SeriesType, 'iat')
def overload_series_iat(s):
    return lambda s: bodo.hiframes.series_indexing.init_series_iat(s)


@overload(operator.getitem, no_unliteral=True)
def overload_series_iat_getitem(I, idx):
    if isinstance(I, SeriesIatType):
        if not isinstance(types.unliteral(idx), types.Integer):
            raise BodoError('iAt based indexing can only have integer indexers'
                )
        if I.stype.dtype == types.NPDatetime('ns'):
            return lambda I, idx: convert_datetime64_to_timestamp(np.int64(
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx]))
        if I.stype.dtype == types.NPTimedelta('ns'):
            return lambda I, idx: convert_numpy_timedelta64_to_pd_timedelta(
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx])
        return lambda I, idx: bodo.hiframes.pd_series_ext.get_series_data(I
            ._obj)[idx]


@overload(operator.setitem, no_unliteral=True)
def overload_series_iat_setitem(I, idx, val):
    if isinstance(I, SeriesIatType):
        if not isinstance(idx, types.Integer):
            raise BodoError('iAt based indexing can only have integer indexers'
                )
        if I.stype.dtype == bodo.string_type and val is not types.none:
            raise BodoError('Series string setitem not supported yet')
        if I.stype.dtype == bodo.bytes_type and val is not types.none:
            raise BodoError('Series binary setitem not supported yet')
        if is_immutable_array(I.stype.data):
            raise BodoError(
                f'Series setitem not supported for Series with immutable array type {I.stype.data}'
                )
        if I.stype.dtype == types.NPDatetime('ns'
            ) and val == pd_timestamp_tz_naive_type:

            def impl_dt(I, idx, val):
                s = integer_to_dt64(val.value)
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx] = s
            return impl_dt
        if I.stype.dtype == types.NPDatetime('ns'
            ) and val == bodo.datetime_datetime_type:

            def impl_dt(I, idx, val):
                s = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx] = s
            return impl_dt
        if I.stype.dtype == types.NPTimedelta('ns'
            ) and val == datetime_timedelta_type:

            def impl_dt(I, idx, val):
                zeey__zqmd = (bodo.hiframes.datetime_timedelta_ext.
                    _to_nanoseconds(val))
                s = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    zeey__zqmd)
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx] = s
            return impl_dt
        if I.stype.dtype == types.NPTimedelta('ns'
            ) and val == pd_timedelta_type:

            def impl_dt(I, idx, val):
                zeey__zqmd = val.value
                s = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    zeey__zqmd)
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx] = s
            return impl_dt

        def impl(I, idx, val):
            bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx] = val
        return impl


class SeriesIlocType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        oqg__ybpur = 'SeriesIlocType({})'.format(stype)
        super(SeriesIlocType, self).__init__(oqg__ybpur)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 1


@register_model(SeriesIlocType)
class SeriesIlocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jlqxw__jfw = [('obj', fe_type.stype)]
        super(SeriesIlocModel, self).__init__(dmm, fe_type, jlqxw__jfw)


make_attribute_wrapper(SeriesIlocType, 'obj', '_obj')


@intrinsic
def init_series_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        kwnaa__egbcb, = args
        pnx__qdi = signature.return_type
        yuye__mmn = cgutils.create_struct_proxy(pnx__qdi)(context, builder)
        yuye__mmn.obj = kwnaa__egbcb
        context.nrt.incref(builder, signature.args[0], kwnaa__egbcb)
        return yuye__mmn._getvalue()
    return SeriesIlocType(obj)(obj), codegen


@overload_attribute(SeriesType, 'iloc')
def overload_series_iloc(s):
    return lambda s: bodo.hiframes.series_indexing.init_series_iloc(s)


@overload(operator.getitem, no_unliteral=True)
def overload_series_iloc_getitem(I, idx):
    if isinstance(I, SeriesIlocType):
        if I.stype.dtype == types.NPTimedelta('ns') and isinstance(idx,
            types.Integer):
            return lambda I, idx: convert_numpy_timedelta64_to_pd_timedelta(
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx])
        if isinstance(idx, types.Integer):
            return lambda I, idx: bodo.utils.conversion.box_if_dt64(bodo.
                hiframes.pd_series_ext.get_series_data(I._obj)[idx])
        if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
            Integer, types.Boolean)):

            def impl(I, idx):
                S = I._obj
                cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                ibses__wur = bodo.hiframes.pd_series_ext.get_series_data(S)[
                    cvee__zmcd]
                bqna__sdr = bodo.hiframes.pd_series_ext.get_series_index(S)[
                    cvee__zmcd]
                oqg__ybpur = bodo.hiframes.pd_series_ext.get_series_name(S)
                return bodo.hiframes.pd_series_ext.init_series(ibses__wur,
                    bqna__sdr, oqg__ybpur)
            return impl
        if isinstance(idx, types.SliceType):

            def impl_slice(I, idx):
                S = I._obj
                ibses__wur = bodo.hiframes.pd_series_ext.get_series_data(S)[idx
                    ]
                bqna__sdr = bodo.hiframes.pd_series_ext.get_series_index(S)[idx
                    ]
                oqg__ybpur = bodo.hiframes.pd_series_ext.get_series_name(S)
                return bodo.hiframes.pd_series_ext.init_series(ibses__wur,
                    bqna__sdr, oqg__ybpur)
            return impl_slice
        raise BodoError('Series.iloc[] getitem using {} not supported'.
            format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_series_iloc_setitem(I, idx, val):
    if isinstance(I, SeriesIlocType):
        if I.stype.dtype == bodo.string_type and val is not types.none:
            raise BodoError('Series string setitem not supported yet')
        if I.stype.dtype == bodo.bytes_type and val is not types.none:
            raise BodoError('Series binary setitem not supported yet')
        if is_immutable_array(I.stype.data):
            raise BodoError(
                f'Series setitem not supported for Series with immutable array type {I.stype.data}'
                )
        if isinstance(idx, types.Integer) or isinstance(idx, types.SliceType
            ) and is_scalar_type(val):
            if I.stype.dtype == types.NPDatetime('ns'
                ) and val == pd_timestamp_tz_naive_type:

                def impl_dt(I, idx, val):
                    s = integer_to_dt64(val.value)
                    bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx
                        ] = s
                return impl_dt
            if I.stype.dtype == types.NPDatetime('ns'
                ) and val == bodo.datetime_datetime_type:

                def impl_dt(I, idx, val):
                    s = (bodo.hiframes.pd_timestamp_ext.
                        datetime_datetime_to_dt64(val))
                    bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx
                        ] = s
                return impl_dt
            if I.stype.dtype == types.NPTimedelta('ns'
                ) and val == datetime_timedelta_type:

                def impl_dt(I, idx, val):
                    zeey__zqmd = (bodo.hiframes.datetime_timedelta_ext.
                        _to_nanoseconds(val))
                    s = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        zeey__zqmd)
                    bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx
                        ] = s
                return impl_dt
            if I.stype.dtype == types.NPTimedelta('ns'
                ) and val == pd_timedelta_type:

                def impl_dt(I, idx, val):
                    zeey__zqmd = val.value
                    s = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        zeey__zqmd)
                    bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx
                        ] = s
                return impl_dt

            def impl(I, idx, val):
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx] = val
            return impl
        if isinstance(idx, types.SliceType):

            def impl_slice(I, idx, val):
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[idx
                    ] = bodo.utils.conversion.coerce_to_array(val, False)
            return impl_slice
        if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
            Integer, types.Boolean)):
            if is_scalar_type(val):
                if I.stype.dtype == types.NPDatetime('ns'
                    ) and val == pd_timestamp_tz_naive_type:

                    def impl_dt(I, idx, val):
                        s = integer_to_dt64(val.value)
                        cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                        bodo.hiframes.pd_series_ext.get_series_data(I._obj)[
                            cvee__zmcd] = s
                    return impl_dt
                if I.stype.dtype == types.NPDatetime('ns'
                    ) and val == bodo.datetime_datetime_type:

                    def impl_dt(I, idx, val):
                        s = (bodo.hiframes.pd_timestamp_ext.
                            datetime_datetime_to_dt64(val))
                        cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                        bodo.hiframes.pd_series_ext.get_series_data(I._obj)[
                            cvee__zmcd] = s
                    return impl_dt
                if I.stype.dtype == types.NPTimedelta('ns'
                    ) and val == datetime_timedelta_type:

                    def impl_dt(I, idx, val):
                        zeey__zqmd = (bodo.hiframes.datetime_timedelta_ext.
                            _to_nanoseconds(val))
                        s = (bodo.hiframes.pd_timestamp_ext.
                            integer_to_timedelta64(zeey__zqmd))
                        cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                        bodo.hiframes.pd_series_ext.get_series_data(I._obj)[
                            cvee__zmcd] = s
                    return impl_dt
                if I.stype.dtype == types.NPTimedelta('ns'
                    ) and val == pd_timedelta_type:

                    def impl_dt(I, idx, val):
                        zeey__zqmd = val.value
                        s = (bodo.hiframes.pd_timestamp_ext.
                            integer_to_timedelta64(zeey__zqmd))
                        cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                        bodo.hiframes.pd_series_ext.get_series_data(I._obj)[
                            cvee__zmcd] = s
                    return impl_dt

                def impl(I, idx, val):
                    cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                    bodo.hiframes.pd_series_ext.get_series_data(I._obj)[
                        cvee__zmcd] = val
                return impl

            def impl_arr(I, idx, val):
                cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                bodo.hiframes.pd_series_ext.get_series_data(I._obj)[cvee__zmcd
                    ] = bodo.utils.conversion.coerce_to_array(val, False)
            return impl_arr
        raise BodoError('Series.iloc[] setitem using {} not supported'.
            format(idx))


class SeriesLocType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        oqg__ybpur = 'SeriesLocType({})'.format(stype)
        super(SeriesLocType, self).__init__(oqg__ybpur)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 1


@register_model(SeriesLocType)
class SeriesLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jlqxw__jfw = [('obj', fe_type.stype)]
        super(SeriesLocModel, self).__init__(dmm, fe_type, jlqxw__jfw)


make_attribute_wrapper(SeriesLocType, 'obj', '_obj')


@intrinsic
def init_series_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        kwnaa__egbcb, = args
        zzka__foh = signature.return_type
        rvpbz__gprf = cgutils.create_struct_proxy(zzka__foh)(context, builder)
        rvpbz__gprf.obj = kwnaa__egbcb
        context.nrt.incref(builder, signature.args[0], kwnaa__egbcb)
        return rvpbz__gprf._getvalue()
    return SeriesLocType(obj)(obj), codegen


@overload_attribute(SeriesType, 'loc')
def overload_series_loc(s):
    return lambda s: bodo.hiframes.series_indexing.init_series_loc(s)


@overload(operator.getitem)
def overload_series_loc_getitem(I, idx):
    if not isinstance(I, SeriesLocType):
        return
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl(I, idx):
            S = I._obj
            cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
            ibses__wur = bodo.hiframes.pd_series_ext.get_series_data(S)[
                cvee__zmcd]
            bqna__sdr = bodo.hiframes.pd_series_ext.get_series_index(S)[
                cvee__zmcd]
            oqg__ybpur = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(ibses__wur,
                bqna__sdr, oqg__ybpur)
        return impl
    if isinstance(idx, types.Integer) and isinstance(I.stype.index,
        RangeIndexType):

        def impl_range_index_int(I, idx):
            S = I._obj
            ibses__wur = bodo.hiframes.pd_series_ext.get_series_data(S)
            bqna__sdr = bodo.hiframes.pd_series_ext.get_series_index(S)
            ytsfn__fyzjl = (idx - bqna__sdr._start) // bqna__sdr._step
            return ibses__wur[ytsfn__fyzjl]
        return impl_range_index_int
    raise BodoError(
        f'Series.loc[] getitem (location-based indexing) using {idx} not supported yet'
        )


@overload(operator.setitem)
def overload_series_loc_setitem(I, idx, val):
    if not isinstance(I, SeriesLocType):
        return
    if is_immutable_array(I.stype.data):
        raise BodoError(
            f'Series setitem not supported for Series with immutable array type {I.stype.data}'
            )
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl(I, idx, val):
            S = I._obj
            S[idx] = val
        return impl
    raise BodoError(
        f'Series.loc[] setitem (location-based indexing) using {idx} not supported yet'
        )


@overload(operator.getitem)
def overload_series_getitem(S, idx):
    if isinstance(S, SeriesType) and not (isinstance(S.index,
        HeterogeneousIndexType) and is_overload_constant_tuple(S.index.data)):
        if isinstance(idx, types.Integer):
            if isinstance(S.index, NumericIndexType) and isinstance(S.index
                .dtype, types.Integer):
                raise BodoError(
                    'Indexing Series with Integer index using [] (which is label-based) not supported yet'
                    )
            if isinstance(S.index, RangeIndexType):

                def impl(S, idx):
                    ibses__wur = bodo.hiframes.pd_series_ext.get_series_data(S)
                    I = bodo.hiframes.pd_series_ext.get_series_index(S)
                    cvee__zmcd = idx * I._step + I._start
                    return bodo.utils.conversion.box_if_dt64(ibses__wur[
                        cvee__zmcd])
                return impl
            return lambda S, idx: bodo.utils.conversion.box_if_dt64(bodo.
                hiframes.pd_series_ext.get_series_data(S)[idx])
        if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
            Integer, types.Boolean)):
            if isinstance(S.index, NumericIndexType) and isinstance(S.index
                .dtype, types.Integer) and isinstance(idx.dtype, types.Integer
                ):
                raise BodoError(
                    'Indexing Series with Integer index using [] (which is label-based) not supported yet'
                    )

            def impl_arr(S, idx):
                cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                ibses__wur = bodo.hiframes.pd_series_ext.get_series_data(S)[
                    cvee__zmcd]
                bqna__sdr = bodo.hiframes.pd_series_ext.get_series_index(S)[
                    cvee__zmcd]
                oqg__ybpur = bodo.hiframes.pd_series_ext.get_series_name(S)
                return bodo.hiframes.pd_series_ext.init_series(ibses__wur,
                    bqna__sdr, oqg__ybpur)
            return impl_arr
        if isinstance(idx, types.SliceType):

            def impl_slice(S, idx):
                ibses__wur = bodo.hiframes.pd_series_ext.get_series_data(S)[idx
                    ]
                bqna__sdr = bodo.hiframes.pd_series_ext.get_series_index(S)[idx
                    ]
                oqg__ybpur = bodo.hiframes.pd_series_ext.get_series_name(S)
                return bodo.hiframes.pd_series_ext.init_series(ibses__wur,
                    bqna__sdr, oqg__ybpur)
            return impl_slice
        if idx == bodo.string_type or is_overload_constant_str(idx):
            if isinstance(S.index, bodo.hiframes.pd_index_ext.StringIndexType):

                def impl_str_getitem(S, idx):
                    aafos__wgxnk = (bodo.hiframes.pd_series_ext.
                        get_series_index(S))
                    xvoyo__lntfv = aafos__wgxnk.get_loc(idx)
                    if xvoyo__lntfv is None:
                        raise IndexError
                    else:
                        val = bodo.hiframes.pd_series_ext.get_series_data(S)[
                            bodo.utils.indexing.unoptional(xvoyo__lntfv)]
                    return val
                return impl_str_getitem
            else:
                raise BodoError(
                    f'Cannot get Series value using a string, unless the index type is also string'
                    )
        raise BodoError(f'getting Series value using {idx} not supported yet')
    elif bodo.utils.utils.is_array_typ(S) and isinstance(idx, SeriesType):
        return lambda S, idx: S[bodo.hiframes.pd_series_ext.get_series_data
            (idx)]


@overload(operator.setitem, no_unliteral=True)
def overload_series_setitem(S, idx, val):
    if isinstance(S, SeriesType):
        if S.dtype == bodo.string_type and val is not types.none and not (
            is_list_like_index_type(idx) and idx.dtype == types.bool_):
            raise BodoError('Series string setitem not supported yet')
        elif S.dtype == bodo.bytes_type:
            raise BodoError('Series binary setitem not supported yet')
        if isinstance(idx, types.Integer):
            if isinstance(S.index, NumericIndexType) and isinstance(S.index
                .dtype, types.Integer):
                raise BodoError(
                    'Indexing Series with Integer index using [] (which is label-based) not supported yet'
                    )
            if S.dtype == types.NPDatetime('ns'
                ) and val == pd_timestamp_tz_naive_type:

                def impl_dt(S, idx, val):
                    s = integer_to_dt64(val.value)
                    bodo.hiframes.pd_series_ext.get_series_data(S)[idx] = s
                return impl_dt
            if S.dtype == types.NPTimedelta('ns'
                ) and val == datetime_timedelta_type:

                def impl_dt(S, idx, val):
                    zeey__zqmd = (bodo.hiframes.datetime_timedelta_ext.
                        _to_nanoseconds(val))
                    s = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        zeey__zqmd)
                    bodo.hiframes.pd_series_ext.get_series_data(S)[idx] = s
                return impl_dt
            if S.dtype == types.NPTimedelta('ns') and val == pd_timedelta_type:

                def impl_dt(S, idx, val):
                    zeey__zqmd = val.value
                    s = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        zeey__zqmd)
                    bodo.hiframes.pd_series_ext.get_series_data(S)[idx] = s
                return impl_dt

            def impl(S, idx, val):
                bodo.hiframes.pd_series_ext.get_series_data(S)[idx] = val
            return impl
        if isinstance(idx, types.SliceType):

            def impl_slice(S, idx, val):
                bodo.hiframes.pd_series_ext.get_series_data(S)[idx
                    ] = bodo.utils.conversion.coerce_to_array(val, False)
            return impl_slice
        if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
            Integer, types.Boolean)):
            if isinstance(S.index, NumericIndexType) and isinstance(S.index
                .dtype, types.Integer) and isinstance(idx.dtype, types.Integer
                ):
                raise BodoError(
                    'Indexing Series with Integer index using [] (which is label-based) not supported yet'
                    )

            def impl_arr(S, idx, val):
                cvee__zmcd = bodo.utils.conversion.coerce_to_array(idx)
                bodo.hiframes.pd_series_ext.get_series_data(S)[cvee__zmcd
                    ] = bodo.utils.conversion.coerce_to_array(val, False)
            return impl_arr
        raise BodoError(f'Series [] setitem using {idx} not supported yet')


@overload(operator.setitem, no_unliteral=True)
def overload_array_list_setitem(A, idx, val):
    if isinstance(A, types.Array) and isinstance(idx, (types.List, SeriesType)
        ):

        def impl(A, idx, val):
            A[bodo.utils.conversion.coerce_to_array(idx)] = val
        return impl


@overload(operator.getitem, no_unliteral=True)
def overload_const_index_series_getitem(S, idx):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)) and isinstance(S
        .index, HeterogeneousIndexType) and is_overload_constant_tuple(S.
        index.data):
        ooly__hdy = get_overload_const_tuple(S.index.data)
        if isinstance(idx, types.Integer) and not any(isinstance(
            jhbw__tppbi, int) for jhbw__tppbi in ooly__hdy):
            return lambda S, idx: bodo.hiframes.pd_series_ext.get_series_data(S
                )[idx]
        if is_literal_type(idx):
            hozaf__llwkr = get_literal_value(idx)
            if hozaf__llwkr not in ooly__hdy:
                raise_bodo_error(
                    f"Series label-based getitem: '{hozaf__llwkr}' not in {ooly__hdy}"
                    )
            arr_ind = ooly__hdy.index(hozaf__llwkr)
            return lambda S, idx: bodo.hiframes.pd_series_ext.get_series_data(S
                )[arr_ind]


@lower_cast(SeriesIatType, SeriesIatType)
@lower_cast(SeriesIlocType, SeriesIlocType)
@lower_cast(SeriesLocType, SeriesLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    yxzs__qqzdl = cgutils.create_struct_proxy(fromty)(context, builder, val)
    jib__kcz = context.cast(builder, yxzs__qqzdl.obj, fromty.stype, toty.stype)
    tqvkg__bymx = cgutils.create_struct_proxy(toty)(context, builder)
    tqvkg__bymx.obj = jib__kcz
    return tqvkg__bymx._getvalue()
