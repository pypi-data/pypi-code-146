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
        uflpw__eexx = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, uflpw__eexx)


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
    cbyga__jbjg = context.get_value_type(str_arr_split_view_payload_type)
    jqhe__lgllj = context.get_abi_sizeof(cbyga__jbjg)
    dconf__dbia = context.get_value_type(types.voidptr)
    ulg__qmbw = context.get_value_type(types.uintp)
    lcya__zce = lir.FunctionType(lir.VoidType(), [dconf__dbia, ulg__qmbw,
        dconf__dbia])
    beam__chkl = cgutils.get_or_insert_function(builder.module, lcya__zce,
        name='dtor_str_arr_split_view')
    irqq__bfsw = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jqhe__lgllj), beam__chkl)
    dxdbe__iywvx = context.nrt.meminfo_data(builder, irqq__bfsw)
    azbft__nwdc = builder.bitcast(dxdbe__iywvx, cbyga__jbjg.as_pointer())
    return irqq__bfsw, azbft__nwdc


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        yma__qwoj, kdusn__jdzqv = args
        irqq__bfsw, azbft__nwdc = construct_str_arr_split_view(context, builder
            )
        pano__nljev = _get_str_binary_arr_payload(context, builder,
            yma__qwoj, string_array_type)
        nqjn__duane = lir.FunctionType(lir.VoidType(), [azbft__nwdc.type,
            lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        zkhcw__yuah = cgutils.get_or_insert_function(builder.module,
            nqjn__duane, name='str_arr_split_view_impl')
        eovk__tkr = context.make_helper(builder, offset_arr_type,
            pano__nljev.offsets).data
        nexu__fnd = context.make_helper(builder, char_arr_type, pano__nljev
            .data).data
        lwooa__nuod = context.make_helper(builder, null_bitmap_arr_type,
            pano__nljev.null_bitmap).data
        ycij__nqvyr = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(zkhcw__yuah, [azbft__nwdc, pano__nljev.n_arrays,
            eovk__tkr, nexu__fnd, lwooa__nuod, ycij__nqvyr])
        gjoav__git = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(azbft__nwdc))
        njrq__rcwp = context.make_helper(builder, string_array_split_view_type)
        njrq__rcwp.num_items = pano__nljev.n_arrays
        njrq__rcwp.index_offsets = gjoav__git.index_offsets
        njrq__rcwp.data_offsets = gjoav__git.data_offsets
        njrq__rcwp.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [yma__qwoj])
        njrq__rcwp.null_bitmap = gjoav__git.null_bitmap
        njrq__rcwp.meminfo = irqq__bfsw
        unqw__zkctu = njrq__rcwp._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, unqw__zkctu)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    upbh__omap = context.make_helper(builder, string_array_split_view_type, val
        )
    xlwp__vlm = context.insert_const_string(builder.module, 'numpy')
    jkv__lajp = c.pyapi.import_module_noblock(xlwp__vlm)
    dtype = c.pyapi.object_getattr_string(jkv__lajp, 'object_')
    dryh__mat = builder.sext(upbh__omap.num_items, c.pyapi.longlong)
    kzsz__qvxet = c.pyapi.long_from_longlong(dryh__mat)
    vqjb__rpxmo = c.pyapi.call_method(jkv__lajp, 'ndarray', (kzsz__qvxet,
        dtype))
    sxl__aqqeg = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    hijs__lsrva = c.pyapi._get_function(sxl__aqqeg, name='array_getptr1')
    ezl__rsjdk = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    jqk__wpj = c.pyapi._get_function(ezl__rsjdk, name='array_setitem')
    tmlf__mpq = c.pyapi.object_getattr_string(jkv__lajp, 'nan')
    with cgutils.for_range(builder, upbh__omap.num_items) as otrx__mzyz:
        str_ind = otrx__mzyz.index
        yrf__hce = builder.sext(builder.load(builder.gep(upbh__omap.
            index_offsets, [str_ind])), lir.IntType(64))
        yphz__ksww = builder.sext(builder.load(builder.gep(upbh__omap.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        qsn__wif = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        iqqy__heudw = builder.gep(upbh__omap.null_bitmap, [qsn__wif])
        sojud__kippl = builder.load(iqqy__heudw)
        lgpdv__wfsu = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(sojud__kippl, lgpdv__wfsu), lir.
            Constant(lir.IntType(8), 1))
        vqpcn__sjvth = builder.sub(yphz__ksww, yrf__hce)
        vqpcn__sjvth = builder.sub(vqpcn__sjvth, vqpcn__sjvth.type(1))
        gyqv__pyffw = builder.call(hijs__lsrva, [vqjb__rpxmo, str_ind])
        vysi__gxajb = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(vysi__gxajb) as (ruzs__qpvr, owrs__iumv):
            with ruzs__qpvr:
                jel__ilcfd = c.pyapi.list_new(vqpcn__sjvth)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    jel__ilcfd), likely=True):
                    with cgutils.for_range(c.builder, vqpcn__sjvth
                        ) as otrx__mzyz:
                        jie__vtsz = builder.add(yrf__hce, otrx__mzyz.index)
                        data_start = builder.load(builder.gep(upbh__omap.
                            data_offsets, [jie__vtsz]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        abikg__rfvx = builder.load(builder.gep(upbh__omap.
                            data_offsets, [builder.add(jie__vtsz, jie__vtsz
                            .type(1))]))
                        sxf__lxxo = builder.gep(builder.extract_value(
                            upbh__omap.data, 0), [data_start])
                        btkkk__vzww = builder.sext(builder.sub(abikg__rfvx,
                            data_start), lir.IntType(64))
                        uspby__szp = c.pyapi.string_from_string_and_size(
                            sxf__lxxo, btkkk__vzww)
                        c.pyapi.list_setitem(jel__ilcfd, otrx__mzyz.index,
                            uspby__szp)
                builder.call(jqk__wpj, [vqjb__rpxmo, gyqv__pyffw, jel__ilcfd])
            with owrs__iumv:
                builder.call(jqk__wpj, [vqjb__rpxmo, gyqv__pyffw, tmlf__mpq])
    c.pyapi.decref(jkv__lajp)
    c.pyapi.decref(dtype)
    c.pyapi.decref(tmlf__mpq)
    return vqjb__rpxmo


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        oll__twad, xit__hiqr, sxf__lxxo = args
        irqq__bfsw, azbft__nwdc = construct_str_arr_split_view(context, builder
            )
        nqjn__duane = lir.FunctionType(lir.VoidType(), [azbft__nwdc.type,
            lir.IntType(64), lir.IntType(64)])
        zkhcw__yuah = cgutils.get_or_insert_function(builder.module,
            nqjn__duane, name='str_arr_split_view_alloc')
        builder.call(zkhcw__yuah, [azbft__nwdc, oll__twad, xit__hiqr])
        gjoav__git = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(azbft__nwdc))
        njrq__rcwp = context.make_helper(builder, string_array_split_view_type)
        njrq__rcwp.num_items = oll__twad
        njrq__rcwp.index_offsets = gjoav__git.index_offsets
        njrq__rcwp.data_offsets = gjoav__git.data_offsets
        njrq__rcwp.data = sxf__lxxo
        njrq__rcwp.null_bitmap = gjoav__git.null_bitmap
        context.nrt.incref(builder, data_t, sxf__lxxo)
        njrq__rcwp.meminfo = irqq__bfsw
        unqw__zkctu = njrq__rcwp._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, unqw__zkctu)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        gcnud__lei, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            gcnud__lei = builder.extract_value(gcnud__lei, 0)
        return builder.bitcast(builder.gep(gcnud__lei, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        gcnud__lei, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            gcnud__lei = builder.extract_value(gcnud__lei, 0)
        return builder.load(builder.gep(gcnud__lei, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        gcnud__lei, ind, ppm__umdiw = args
        xafw__fmz = builder.gep(gcnud__lei, [ind])
        builder.store(ppm__umdiw, xafw__fmz)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        wpgp__lkhin, ind = args
        ltddl__tjm = context.make_helper(builder, arr_ctypes_t, wpgp__lkhin)
        ekel__mwdhz = context.make_helper(builder, arr_ctypes_t)
        ekel__mwdhz.data = builder.gep(ltddl__tjm.data, [ind])
        ekel__mwdhz.meminfo = ltddl__tjm.meminfo
        dvsbs__kex = ekel__mwdhz._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, dvsbs__kex)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    gwqa__lrore = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not gwqa__lrore:
        return 0, 0, 0
    jie__vtsz = getitem_c_arr(arr._index_offsets, item_ind)
    xvc__xiacz = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    micr__wvuil = xvc__xiacz - jie__vtsz
    if str_ind >= micr__wvuil:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, jie__vtsz + str_ind)
    data_start += 1
    if jie__vtsz + str_ind == 0:
        data_start = 0
    abikg__rfvx = getitem_c_arr(arr._data_offsets, jie__vtsz + str_ind + 1)
    wkltz__eoysm = abikg__rfvx - data_start
    return 1, data_start, wkltz__eoysm


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
        pebib__homv = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            jie__vtsz = getitem_c_arr(A._index_offsets, ind)
            xvc__xiacz = getitem_c_arr(A._index_offsets, ind + 1)
            ife__zlinf = xvc__xiacz - jie__vtsz - 1
            yma__qwoj = bodo.libs.str_arr_ext.pre_alloc_string_array(ife__zlinf
                , -1)
            for auy__vni in range(ife__zlinf):
                data_start = getitem_c_arr(A._data_offsets, jie__vtsz +
                    auy__vni)
                data_start += 1
                if jie__vtsz + auy__vni == 0:
                    data_start = 0
                abikg__rfvx = getitem_c_arr(A._data_offsets, jie__vtsz +
                    auy__vni + 1)
                wkltz__eoysm = abikg__rfvx - data_start
                xafw__fmz = get_array_ctypes_ptr(A._data, data_start)
                xhjsw__lhol = bodo.libs.str_arr_ext.decode_utf8(xafw__fmz,
                    wkltz__eoysm)
                yma__qwoj[auy__vni] = xhjsw__lhol
            return yma__qwoj
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        pis__asy = offset_type.bitwidth // 8

        def _impl(A, ind):
            ife__zlinf = len(A)
            if ife__zlinf != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            oll__twad = 0
            xit__hiqr = 0
            for auy__vni in range(ife__zlinf):
                if ind[auy__vni]:
                    oll__twad += 1
                    jie__vtsz = getitem_c_arr(A._index_offsets, auy__vni)
                    xvc__xiacz = getitem_c_arr(A._index_offsets, auy__vni + 1)
                    xit__hiqr += xvc__xiacz - jie__vtsz
            vqjb__rpxmo = pre_alloc_str_arr_view(oll__twad, xit__hiqr, A._data)
            item_ind = 0
            mcptm__ygoex = 0
            for auy__vni in range(ife__zlinf):
                if ind[auy__vni]:
                    jie__vtsz = getitem_c_arr(A._index_offsets, auy__vni)
                    xvc__xiacz = getitem_c_arr(A._index_offsets, auy__vni + 1)
                    hyxbq__axq = xvc__xiacz - jie__vtsz
                    setitem_c_arr(vqjb__rpxmo._index_offsets, item_ind,
                        mcptm__ygoex)
                    xafw__fmz = get_c_arr_ptr(A._data_offsets, jie__vtsz)
                    iqbmy__qizcq = get_c_arr_ptr(vqjb__rpxmo._data_offsets,
                        mcptm__ygoex)
                    _memcpy(iqbmy__qizcq, xafw__fmz, hyxbq__axq, pis__asy)
                    gwqa__lrore = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, auy__vni)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vqjb__rpxmo.
                        _null_bitmap, item_ind, gwqa__lrore)
                    item_ind += 1
                    mcptm__ygoex += hyxbq__axq
            setitem_c_arr(vqjb__rpxmo._index_offsets, item_ind, mcptm__ygoex)
            return vqjb__rpxmo
        return _impl
