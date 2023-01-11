import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        rpje__mzf = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, rpje__mzf)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    yaj__jph = context.get_value_type(str_arr_split_view_payload_type)
    incs__gflbq = context.get_abi_sizeof(yaj__jph)
    esff__fhr = context.get_value_type(types.voidptr)
    qufa__qlzux = context.get_value_type(types.uintp)
    yiuji__seomg = lir.FunctionType(lir.VoidType(), [esff__fhr, qufa__qlzux,
        esff__fhr])
    zdonh__zgcup = cgutils.get_or_insert_function(builder.module,
        yiuji__seomg, name='dtor_str_arr_split_view')
    akqyq__axzv = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, incs__gflbq), zdonh__zgcup)
    prz__nvby = context.nrt.meminfo_data(builder, akqyq__axzv)
    cweek__ulbdt = builder.bitcast(prz__nvby, yaj__jph.as_pointer())
    return akqyq__axzv, cweek__ulbdt


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        mcwii__kiyck, bjhbl__wsqt = args
        akqyq__axzv, cweek__ulbdt = construct_str_arr_split_view(context,
            builder)
        lch__yltr = _get_str_binary_arr_payload(context, builder,
            mcwii__kiyck, string_array_type)
        kxb__phd = lir.FunctionType(lir.VoidType(), [cweek__ulbdt.type, lir
            .IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        nuwhz__ttsl = cgutils.get_or_insert_function(builder.module,
            kxb__phd, name='str_arr_split_view_impl')
        nnqky__qqyg = context.make_helper(builder, offset_arr_type,
            lch__yltr.offsets).data
        voqp__tbn = context.make_helper(builder, char_arr_type, lch__yltr.data
            ).data
        lij__vaejh = context.make_helper(builder, null_bitmap_arr_type,
            lch__yltr.null_bitmap).data
        hxgf__oncqt = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(nuwhz__ttsl, [cweek__ulbdt, lch__yltr.n_arrays,
            nnqky__qqyg, voqp__tbn, lij__vaejh, hxgf__oncqt])
        batri__mvwb = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(cweek__ulbdt))
        qgqu__vhks = context.make_helper(builder, string_array_split_view_type)
        qgqu__vhks.num_items = lch__yltr.n_arrays
        qgqu__vhks.index_offsets = batri__mvwb.index_offsets
        qgqu__vhks.data_offsets = batri__mvwb.data_offsets
        qgqu__vhks.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [
            mcwii__kiyck])
        qgqu__vhks.null_bitmap = batri__mvwb.null_bitmap
        qgqu__vhks.meminfo = akqyq__axzv
        exjf__pqkvq = qgqu__vhks._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, exjf__pqkvq)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    jglkn__aoiqx = context.make_helper(builder,
        string_array_split_view_type, val)
    nxqpr__qndhc = context.insert_const_string(builder.module, 'numpy')
    ivfx__kby = c.pyapi.import_module_noblock(nxqpr__qndhc)
    dtype = c.pyapi.object_getattr_string(ivfx__kby, 'object_')
    fgfsa__jed = builder.sext(jglkn__aoiqx.num_items, c.pyapi.longlong)
    xko__ukrg = c.pyapi.long_from_longlong(fgfsa__jed)
    jji__lwkki = c.pyapi.call_method(ivfx__kby, 'ndarray', (xko__ukrg, dtype))
    jdw__scp = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.pyobj,
        c.pyapi.py_ssize_t])
    guxlg__fmutr = c.pyapi._get_function(jdw__scp, name='array_getptr1')
    lryv__fimz = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    edqn__uatdo = c.pyapi._get_function(lryv__fimz, name='array_setitem')
    gcl__nho = c.pyapi.object_getattr_string(ivfx__kby, 'nan')
    with cgutils.for_range(builder, jglkn__aoiqx.num_items) as bhtnl__gqmin:
        str_ind = bhtnl__gqmin.index
        icws__rqiy = builder.sext(builder.load(builder.gep(jglkn__aoiqx.
            index_offsets, [str_ind])), lir.IntType(64))
        rehe__xrtt = builder.sext(builder.load(builder.gep(jglkn__aoiqx.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        ili__zqmmw = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        wfuu__zork = builder.gep(jglkn__aoiqx.null_bitmap, [ili__zqmmw])
        bpjtp__vdvjl = builder.load(wfuu__zork)
        wgvc__pbtpr = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(bpjtp__vdvjl, wgvc__pbtpr), lir.
            Constant(lir.IntType(8), 1))
        owbj__kkol = builder.sub(rehe__xrtt, icws__rqiy)
        owbj__kkol = builder.sub(owbj__kkol, owbj__kkol.type(1))
        maapm__vdurk = builder.call(guxlg__fmutr, [jji__lwkki, str_ind])
        zyp__hsrkv = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(zyp__hsrkv) as (nhcnw__ejax, uan__psbe):
            with nhcnw__ejax:
                wfdc__qxg = c.pyapi.list_new(owbj__kkol)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    wfdc__qxg), likely=True):
                    with cgutils.for_range(c.builder, owbj__kkol
                        ) as bhtnl__gqmin:
                        neur__bcqx = builder.add(icws__rqiy, bhtnl__gqmin.index
                            )
                        data_start = builder.load(builder.gep(jglkn__aoiqx.
                            data_offsets, [neur__bcqx]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        prz__msx = builder.load(builder.gep(jglkn__aoiqx.
                            data_offsets, [builder.add(neur__bcqx,
                            neur__bcqx.type(1))]))
                        ziri__pboue = builder.gep(builder.extract_value(
                            jglkn__aoiqx.data, 0), [data_start])
                        hvww__mzw = builder.sext(builder.sub(prz__msx,
                            data_start), lir.IntType(64))
                        adsnd__ammbv = c.pyapi.string_from_string_and_size(
                            ziri__pboue, hvww__mzw)
                        c.pyapi.list_setitem(wfdc__qxg, bhtnl__gqmin.index,
                            adsnd__ammbv)
                builder.call(edqn__uatdo, [jji__lwkki, maapm__vdurk, wfdc__qxg]
                    )
            with uan__psbe:
                builder.call(edqn__uatdo, [jji__lwkki, maapm__vdurk, gcl__nho])
    c.pyapi.decref(ivfx__kby)
    c.pyapi.decref(dtype)
    c.pyapi.decref(gcl__nho)
    return jji__lwkki


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        fjg__nxn, wvygm__sxe, ziri__pboue = args
        akqyq__axzv, cweek__ulbdt = construct_str_arr_split_view(context,
            builder)
        kxb__phd = lir.FunctionType(lir.VoidType(), [cweek__ulbdt.type, lir
            .IntType(64), lir.IntType(64)])
        nuwhz__ttsl = cgutils.get_or_insert_function(builder.module,
            kxb__phd, name='str_arr_split_view_alloc')
        builder.call(nuwhz__ttsl, [cweek__ulbdt, fjg__nxn, wvygm__sxe])
        batri__mvwb = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(cweek__ulbdt))
        qgqu__vhks = context.make_helper(builder, string_array_split_view_type)
        qgqu__vhks.num_items = fjg__nxn
        qgqu__vhks.index_offsets = batri__mvwb.index_offsets
        qgqu__vhks.data_offsets = batri__mvwb.data_offsets
        qgqu__vhks.data = ziri__pboue
        qgqu__vhks.null_bitmap = batri__mvwb.null_bitmap
        context.nrt.incref(builder, data_t, ziri__pboue)
        qgqu__vhks.meminfo = akqyq__axzv
        exjf__pqkvq = qgqu__vhks._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, exjf__pqkvq)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        mfdc__mydwr, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            mfdc__mydwr = builder.extract_value(mfdc__mydwr, 0)
        return builder.bitcast(builder.gep(mfdc__mydwr, [ind]), lir.IntType
            (8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        mfdc__mydwr, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            mfdc__mydwr = builder.extract_value(mfdc__mydwr, 0)
        return builder.load(builder.gep(mfdc__mydwr, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        mfdc__mydwr, ind, itif__ypm = args
        mfei__uwka = builder.gep(mfdc__mydwr, [ind])
        builder.store(itif__ypm, mfei__uwka)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        gygdm__iyf, ind = args
        utxy__qcd = context.make_helper(builder, arr_ctypes_t, gygdm__iyf)
        kacuo__lbhu = context.make_helper(builder, arr_ctypes_t)
        kacuo__lbhu.data = builder.gep(utxy__qcd.data, [ind])
        kacuo__lbhu.meminfo = utxy__qcd.meminfo
        enu__zkyb = kacuo__lbhu._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, enu__zkyb)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    ueo__ils = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not ueo__ils:
        return 0, 0, 0
    neur__bcqx = getitem_c_arr(arr._index_offsets, item_ind)
    awz__mhqzp = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    anfiq__ezfdt = awz__mhqzp - neur__bcqx
    if str_ind >= anfiq__ezfdt:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, neur__bcqx + str_ind)
    data_start += 1
    if neur__bcqx + str_ind == 0:
        data_start = 0
    prz__msx = getitem_c_arr(arr._data_offsets, neur__bcqx + str_ind + 1)
    pxp__gqdf = prz__msx - data_start
    return 1, data_start, pxp__gqdf


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        unz__mwjz = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            neur__bcqx = getitem_c_arr(A._index_offsets, ind)
            awz__mhqzp = getitem_c_arr(A._index_offsets, ind + 1)
            bzmsc__coh = awz__mhqzp - neur__bcqx - 1
            mcwii__kiyck = bodo.libs.str_arr_ext.pre_alloc_string_array(
                bzmsc__coh, -1)
            for wkld__kkpbu in range(bzmsc__coh):
                data_start = getitem_c_arr(A._data_offsets, neur__bcqx +
                    wkld__kkpbu)
                data_start += 1
                if neur__bcqx + wkld__kkpbu == 0:
                    data_start = 0
                prz__msx = getitem_c_arr(A._data_offsets, neur__bcqx +
                    wkld__kkpbu + 1)
                pxp__gqdf = prz__msx - data_start
                mfei__uwka = get_array_ctypes_ptr(A._data, data_start)
                vtrgq__chlh = bodo.libs.str_arr_ext.decode_utf8(mfei__uwka,
                    pxp__gqdf)
                mcwii__kiyck[wkld__kkpbu] = vtrgq__chlh
            return mcwii__kiyck
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        txn__tgzd = offset_type.bitwidth // 8

        def _impl(A, ind):
            bzmsc__coh = len(A)
            if bzmsc__coh != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            fjg__nxn = 0
            wvygm__sxe = 0
            for wkld__kkpbu in range(bzmsc__coh):
                if ind[wkld__kkpbu]:
                    fjg__nxn += 1
                    neur__bcqx = getitem_c_arr(A._index_offsets, wkld__kkpbu)
                    awz__mhqzp = getitem_c_arr(A._index_offsets, 
                        wkld__kkpbu + 1)
                    wvygm__sxe += awz__mhqzp - neur__bcqx
            jji__lwkki = pre_alloc_str_arr_view(fjg__nxn, wvygm__sxe, A._data)
            item_ind = 0
            hqfj__wlrq = 0
            for wkld__kkpbu in range(bzmsc__coh):
                if ind[wkld__kkpbu]:
                    neur__bcqx = getitem_c_arr(A._index_offsets, wkld__kkpbu)
                    awz__mhqzp = getitem_c_arr(A._index_offsets, 
                        wkld__kkpbu + 1)
                    qurno__bweh = awz__mhqzp - neur__bcqx
                    setitem_c_arr(jji__lwkki._index_offsets, item_ind,
                        hqfj__wlrq)
                    mfei__uwka = get_c_arr_ptr(A._data_offsets, neur__bcqx)
                    uhul__lnosr = get_c_arr_ptr(jji__lwkki._data_offsets,
                        hqfj__wlrq)
                    _memcpy(uhul__lnosr, mfei__uwka, qurno__bweh, txn__tgzd)
                    ueo__ils = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, wkld__kkpbu)
                    bodo.libs.int_arr_ext.set_bit_to_arr(jji__lwkki.
                        _null_bitmap, item_ind, ueo__ils)
                    item_ind += 1
                    hqfj__wlrq += qurno__bweh
            setitem_c_arr(jji__lwkki._index_offsets, item_ind, hqfj__wlrq)
            return jji__lwkki
        return _impl
