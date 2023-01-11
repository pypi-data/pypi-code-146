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
        equu__lyve = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, equu__lyve)


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
    hbpv__nxtn = context.get_value_type(str_arr_split_view_payload_type)
    bngvc__kdnuo = context.get_abi_sizeof(hbpv__nxtn)
    erkz__jibkr = context.get_value_type(types.voidptr)
    xikb__tclkg = context.get_value_type(types.uintp)
    xftn__ijjk = lir.FunctionType(lir.VoidType(), [erkz__jibkr, xikb__tclkg,
        erkz__jibkr])
    ynm__nyl = cgutils.get_or_insert_function(builder.module, xftn__ijjk,
        name='dtor_str_arr_split_view')
    rrg__wjl = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, bngvc__kdnuo), ynm__nyl)
    zjgi__ifl = context.nrt.meminfo_data(builder, rrg__wjl)
    aicq__quk = builder.bitcast(zjgi__ifl, hbpv__nxtn.as_pointer())
    return rrg__wjl, aicq__quk


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        ubtp__emfs, zzaxt__oer = args
        rrg__wjl, aicq__quk = construct_str_arr_split_view(context, builder)
        ejh__tqr = _get_str_binary_arr_payload(context, builder, ubtp__emfs,
            string_array_type)
        kjwne__kfy = lir.FunctionType(lir.VoidType(), [aicq__quk.type, lir.
            IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        dqrko__cezrm = cgutils.get_or_insert_function(builder.module,
            kjwne__kfy, name='str_arr_split_view_impl')
        rbwg__hmajy = context.make_helper(builder, offset_arr_type,
            ejh__tqr.offsets).data
        knx__fzbdf = context.make_helper(builder, char_arr_type, ejh__tqr.data
            ).data
        nrr__dddyq = context.make_helper(builder, null_bitmap_arr_type,
            ejh__tqr.null_bitmap).data
        crwp__vck = context.get_constant(types.int8, ord(sep_typ.literal_value)
            )
        builder.call(dqrko__cezrm, [aicq__quk, ejh__tqr.n_arrays,
            rbwg__hmajy, knx__fzbdf, nrr__dddyq, crwp__vck])
        ajh__koeap = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(aicq__quk))
        hznx__kro = context.make_helper(builder, string_array_split_view_type)
        hznx__kro.num_items = ejh__tqr.n_arrays
        hznx__kro.index_offsets = ajh__koeap.index_offsets
        hznx__kro.data_offsets = ajh__koeap.data_offsets
        hznx__kro.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [ubtp__emfs])
        hznx__kro.null_bitmap = ajh__koeap.null_bitmap
        hznx__kro.meminfo = rrg__wjl
        lbmq__yeg = hznx__kro._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, lbmq__yeg)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    xmbn__iwecc = context.make_helper(builder, string_array_split_view_type,
        val)
    wnwhf__ufehv = context.insert_const_string(builder.module, 'numpy')
    uqnm__tkbr = c.pyapi.import_module_noblock(wnwhf__ufehv)
    dtype = c.pyapi.object_getattr_string(uqnm__tkbr, 'object_')
    yqsx__aof = builder.sext(xmbn__iwecc.num_items, c.pyapi.longlong)
    pkqon__mni = c.pyapi.long_from_longlong(yqsx__aof)
    alc__tbxil = c.pyapi.call_method(uqnm__tkbr, 'ndarray', (pkqon__mni, dtype)
        )
    slab__czleh = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    pfuvy__mii = c.pyapi._get_function(slab__czleh, name='array_getptr1')
    nhpzj__fphuq = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    zvfn__eaq = c.pyapi._get_function(nhpzj__fphuq, name='array_setitem')
    nkmaw__aul = c.pyapi.object_getattr_string(uqnm__tkbr, 'nan')
    with cgutils.for_range(builder, xmbn__iwecc.num_items) as mlbin__vcf:
        str_ind = mlbin__vcf.index
        xbr__mmc = builder.sext(builder.load(builder.gep(xmbn__iwecc.
            index_offsets, [str_ind])), lir.IntType(64))
        crbom__dqoi = builder.sext(builder.load(builder.gep(xmbn__iwecc.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        hocxg__dvf = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        qaz__mpymk = builder.gep(xmbn__iwecc.null_bitmap, [hocxg__dvf])
        yuxkr__qcjf = builder.load(qaz__mpymk)
        vhyo__ihm = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(yuxkr__qcjf, vhyo__ihm), lir.
            Constant(lir.IntType(8), 1))
        dgdo__czr = builder.sub(crbom__dqoi, xbr__mmc)
        dgdo__czr = builder.sub(dgdo__czr, dgdo__czr.type(1))
        nnb__yljl = builder.call(pfuvy__mii, [alc__tbxil, str_ind])
        tpr__tiu = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(tpr__tiu) as (tfnk__ljk, ztvp__lgu):
            with tfnk__ljk:
                eumg__eqrum = c.pyapi.list_new(dgdo__czr)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    eumg__eqrum), likely=True):
                    with cgutils.for_range(c.builder, dgdo__czr) as mlbin__vcf:
                        qvmvk__imw = builder.add(xbr__mmc, mlbin__vcf.index)
                        data_start = builder.load(builder.gep(xmbn__iwecc.
                            data_offsets, [qvmvk__imw]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        let__kgqez = builder.load(builder.gep(xmbn__iwecc.
                            data_offsets, [builder.add(qvmvk__imw,
                            qvmvk__imw.type(1))]))
                        ewpu__xzck = builder.gep(builder.extract_value(
                            xmbn__iwecc.data, 0), [data_start])
                        yxjb__hyj = builder.sext(builder.sub(let__kgqez,
                            data_start), lir.IntType(64))
                        vsdq__gloz = c.pyapi.string_from_string_and_size(
                            ewpu__xzck, yxjb__hyj)
                        c.pyapi.list_setitem(eumg__eqrum, mlbin__vcf.index,
                            vsdq__gloz)
                builder.call(zvfn__eaq, [alc__tbxil, nnb__yljl, eumg__eqrum])
            with ztvp__lgu:
                builder.call(zvfn__eaq, [alc__tbxil, nnb__yljl, nkmaw__aul])
    c.pyapi.decref(uqnm__tkbr)
    c.pyapi.decref(dtype)
    c.pyapi.decref(nkmaw__aul)
    return alc__tbxil


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        mbaap__hvq, gus__ugaqw, ewpu__xzck = args
        rrg__wjl, aicq__quk = construct_str_arr_split_view(context, builder)
        kjwne__kfy = lir.FunctionType(lir.VoidType(), [aicq__quk.type, lir.
            IntType(64), lir.IntType(64)])
        dqrko__cezrm = cgutils.get_or_insert_function(builder.module,
            kjwne__kfy, name='str_arr_split_view_alloc')
        builder.call(dqrko__cezrm, [aicq__quk, mbaap__hvq, gus__ugaqw])
        ajh__koeap = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(aicq__quk))
        hznx__kro = context.make_helper(builder, string_array_split_view_type)
        hznx__kro.num_items = mbaap__hvq
        hznx__kro.index_offsets = ajh__koeap.index_offsets
        hznx__kro.data_offsets = ajh__koeap.data_offsets
        hznx__kro.data = ewpu__xzck
        hznx__kro.null_bitmap = ajh__koeap.null_bitmap
        context.nrt.incref(builder, data_t, ewpu__xzck)
        hznx__kro.meminfo = rrg__wjl
        lbmq__yeg = hznx__kro._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, lbmq__yeg)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        mbkey__tcyd, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            mbkey__tcyd = builder.extract_value(mbkey__tcyd, 0)
        return builder.bitcast(builder.gep(mbkey__tcyd, [ind]), lir.IntType
            (8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        mbkey__tcyd, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            mbkey__tcyd = builder.extract_value(mbkey__tcyd, 0)
        return builder.load(builder.gep(mbkey__tcyd, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        mbkey__tcyd, ind, cgl__wxwve = args
        zwcfi__coi = builder.gep(mbkey__tcyd, [ind])
        builder.store(cgl__wxwve, zwcfi__coi)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        shu__uwa, ind = args
        vvkya__xub = context.make_helper(builder, arr_ctypes_t, shu__uwa)
        jxs__qop = context.make_helper(builder, arr_ctypes_t)
        jxs__qop.data = builder.gep(vvkya__xub.data, [ind])
        jxs__qop.meminfo = vvkya__xub.meminfo
        cpky__avdk = jxs__qop._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, cpky__avdk)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    demdb__rljb = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not demdb__rljb:
        return 0, 0, 0
    qvmvk__imw = getitem_c_arr(arr._index_offsets, item_ind)
    xxhg__sziod = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    vedvk__nhxt = xxhg__sziod - qvmvk__imw
    if str_ind >= vedvk__nhxt:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, qvmvk__imw + str_ind)
    data_start += 1
    if qvmvk__imw + str_ind == 0:
        data_start = 0
    let__kgqez = getitem_c_arr(arr._data_offsets, qvmvk__imw + str_ind + 1)
    uii__xoixj = let__kgqez - data_start
    return 1, data_start, uii__xoixj


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
        wheg__qpmtl = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            qvmvk__imw = getitem_c_arr(A._index_offsets, ind)
            xxhg__sziod = getitem_c_arr(A._index_offsets, ind + 1)
            cmt__tlht = xxhg__sziod - qvmvk__imw - 1
            ubtp__emfs = bodo.libs.str_arr_ext.pre_alloc_string_array(cmt__tlht
                , -1)
            for ols__gki in range(cmt__tlht):
                data_start = getitem_c_arr(A._data_offsets, qvmvk__imw +
                    ols__gki)
                data_start += 1
                if qvmvk__imw + ols__gki == 0:
                    data_start = 0
                let__kgqez = getitem_c_arr(A._data_offsets, qvmvk__imw +
                    ols__gki + 1)
                uii__xoixj = let__kgqez - data_start
                zwcfi__coi = get_array_ctypes_ptr(A._data, data_start)
                nnhb__amf = bodo.libs.str_arr_ext.decode_utf8(zwcfi__coi,
                    uii__xoixj)
                ubtp__emfs[ols__gki] = nnhb__amf
            return ubtp__emfs
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        tev__gzz = offset_type.bitwidth // 8

        def _impl(A, ind):
            cmt__tlht = len(A)
            if cmt__tlht != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            mbaap__hvq = 0
            gus__ugaqw = 0
            for ols__gki in range(cmt__tlht):
                if ind[ols__gki]:
                    mbaap__hvq += 1
                    qvmvk__imw = getitem_c_arr(A._index_offsets, ols__gki)
                    xxhg__sziod = getitem_c_arr(A._index_offsets, ols__gki + 1)
                    gus__ugaqw += xxhg__sziod - qvmvk__imw
            alc__tbxil = pre_alloc_str_arr_view(mbaap__hvq, gus__ugaqw, A._data
                )
            item_ind = 0
            sfds__nls = 0
            for ols__gki in range(cmt__tlht):
                if ind[ols__gki]:
                    qvmvk__imw = getitem_c_arr(A._index_offsets, ols__gki)
                    xxhg__sziod = getitem_c_arr(A._index_offsets, ols__gki + 1)
                    txbs__cdv = xxhg__sziod - qvmvk__imw
                    setitem_c_arr(alc__tbxil._index_offsets, item_ind,
                        sfds__nls)
                    zwcfi__coi = get_c_arr_ptr(A._data_offsets, qvmvk__imw)
                    fro__mvmje = get_c_arr_ptr(alc__tbxil._data_offsets,
                        sfds__nls)
                    _memcpy(fro__mvmje, zwcfi__coi, txbs__cdv, tev__gzz)
                    demdb__rljb = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, ols__gki)
                    bodo.libs.int_arr_ext.set_bit_to_arr(alc__tbxil.
                        _null_bitmap, item_ind, demdb__rljb)
                    item_ind += 1
                    sfds__nls += txbs__cdv
            setitem_c_arr(alc__tbxil._index_offsets, item_ind, sfds__nls)
            return alc__tbxil
        return _impl
