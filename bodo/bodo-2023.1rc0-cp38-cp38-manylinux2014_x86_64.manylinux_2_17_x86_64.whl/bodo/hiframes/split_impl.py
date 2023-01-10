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
        rikay__fiiq = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, rikay__fiiq)


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
    oow__gkhza = context.get_value_type(str_arr_split_view_payload_type)
    nqjez__wab = context.get_abi_sizeof(oow__gkhza)
    zct__jpm = context.get_value_type(types.voidptr)
    wksx__tdcqc = context.get_value_type(types.uintp)
    lxdqq__ics = lir.FunctionType(lir.VoidType(), [zct__jpm, wksx__tdcqc,
        zct__jpm])
    urvqb__vwk = cgutils.get_or_insert_function(builder.module, lxdqq__ics,
        name='dtor_str_arr_split_view')
    fmlts__urbmj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, nqjez__wab), urvqb__vwk)
    kdsi__jym = context.nrt.meminfo_data(builder, fmlts__urbmj)
    ikj__blxme = builder.bitcast(kdsi__jym, oow__gkhza.as_pointer())
    return fmlts__urbmj, ikj__blxme


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        oebw__sjtdj, kthl__eoydi = args
        fmlts__urbmj, ikj__blxme = construct_str_arr_split_view(context,
            builder)
        seos__wkn = _get_str_binary_arr_payload(context, builder,
            oebw__sjtdj, string_array_type)
        urj__jkvhk = lir.FunctionType(lir.VoidType(), [ikj__blxme.type, lir
            .IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        raqo__ckdnd = cgutils.get_or_insert_function(builder.module,
            urj__jkvhk, name='str_arr_split_view_impl')
        bajr__wrg = context.make_helper(builder, offset_arr_type, seos__wkn
            .offsets).data
        thn__ktvu = context.make_helper(builder, char_arr_type, seos__wkn.data
            ).data
        sgl__yvlcm = context.make_helper(builder, null_bitmap_arr_type,
            seos__wkn.null_bitmap).data
        rzr__yevjb = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(raqo__ckdnd, [ikj__blxme, seos__wkn.n_arrays,
            bajr__wrg, thn__ktvu, sgl__yvlcm, rzr__yevjb])
        sau__set = cgutils.create_struct_proxy(str_arr_split_view_payload_type
            )(context, builder, value=builder.load(ikj__blxme))
        foxvd__yawp = context.make_helper(builder, string_array_split_view_type
            )
        foxvd__yawp.num_items = seos__wkn.n_arrays
        foxvd__yawp.index_offsets = sau__set.index_offsets
        foxvd__yawp.data_offsets = sau__set.data_offsets
        foxvd__yawp.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [oebw__sjtdj]
            )
        foxvd__yawp.null_bitmap = sau__set.null_bitmap
        foxvd__yawp.meminfo = fmlts__urbmj
        oaix__rpdr = foxvd__yawp._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, oaix__rpdr)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    mhdkv__oybca = context.make_helper(builder,
        string_array_split_view_type, val)
    keih__gdsmu = context.insert_const_string(builder.module, 'numpy')
    xjv__ctntw = c.pyapi.import_module_noblock(keih__gdsmu)
    dtype = c.pyapi.object_getattr_string(xjv__ctntw, 'object_')
    tpqq__jipx = builder.sext(mhdkv__oybca.num_items, c.pyapi.longlong)
    xyjze__rehf = c.pyapi.long_from_longlong(tpqq__jipx)
    vbjij__hgcq = c.pyapi.call_method(xjv__ctntw, 'ndarray', (xyjze__rehf,
        dtype))
    kcztt__foo = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    vyam__qypsy = c.pyapi._get_function(kcztt__foo, name='array_getptr1')
    gvl__moq = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.IntType
        (8).as_pointer(), c.pyapi.pyobj])
    ehpb__romu = c.pyapi._get_function(gvl__moq, name='array_setitem')
    jcosx__gnmu = c.pyapi.object_getattr_string(xjv__ctntw, 'nan')
    with cgutils.for_range(builder, mhdkv__oybca.num_items) as yve__stnm:
        str_ind = yve__stnm.index
        ors__zqrax = builder.sext(builder.load(builder.gep(mhdkv__oybca.
            index_offsets, [str_ind])), lir.IntType(64))
        ulo__zale = builder.sext(builder.load(builder.gep(mhdkv__oybca.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        iqtt__xwaye = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        yxmyn__scx = builder.gep(mhdkv__oybca.null_bitmap, [iqtt__xwaye])
        deh__hrb = builder.load(yxmyn__scx)
        dbm__igeie = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(deh__hrb, dbm__igeie), lir.Constant
            (lir.IntType(8), 1))
        cspq__ifx = builder.sub(ulo__zale, ors__zqrax)
        cspq__ifx = builder.sub(cspq__ifx, cspq__ifx.type(1))
        zedn__zdbqo = builder.call(vyam__qypsy, [vbjij__hgcq, str_ind])
        gbi__sanjl = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(gbi__sanjl) as (ngm__jlb, vbaq__tmm):
            with ngm__jlb:
                doj__bdwk = c.pyapi.list_new(cspq__ifx)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    doj__bdwk), likely=True):
                    with cgutils.for_range(c.builder, cspq__ifx) as yve__stnm:
                        edtu__khaa = builder.add(ors__zqrax, yve__stnm.index)
                        data_start = builder.load(builder.gep(mhdkv__oybca.
                            data_offsets, [edtu__khaa]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        emez__dom = builder.load(builder.gep(mhdkv__oybca.
                            data_offsets, [builder.add(edtu__khaa,
                            edtu__khaa.type(1))]))
                        mpzf__wnl = builder.gep(builder.extract_value(
                            mhdkv__oybca.data, 0), [data_start])
                        nxu__bflvc = builder.sext(builder.sub(emez__dom,
                            data_start), lir.IntType(64))
                        jud__gslr = c.pyapi.string_from_string_and_size(
                            mpzf__wnl, nxu__bflvc)
                        c.pyapi.list_setitem(doj__bdwk, yve__stnm.index,
                            jud__gslr)
                builder.call(ehpb__romu, [vbjij__hgcq, zedn__zdbqo, doj__bdwk])
            with vbaq__tmm:
                builder.call(ehpb__romu, [vbjij__hgcq, zedn__zdbqo,
                    jcosx__gnmu])
    c.pyapi.decref(xjv__ctntw)
    c.pyapi.decref(dtype)
    c.pyapi.decref(jcosx__gnmu)
    return vbjij__hgcq


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        mzc__vjiln, dqdy__vtpfn, mpzf__wnl = args
        fmlts__urbmj, ikj__blxme = construct_str_arr_split_view(context,
            builder)
        urj__jkvhk = lir.FunctionType(lir.VoidType(), [ikj__blxme.type, lir
            .IntType(64), lir.IntType(64)])
        raqo__ckdnd = cgutils.get_or_insert_function(builder.module,
            urj__jkvhk, name='str_arr_split_view_alloc')
        builder.call(raqo__ckdnd, [ikj__blxme, mzc__vjiln, dqdy__vtpfn])
        sau__set = cgutils.create_struct_proxy(str_arr_split_view_payload_type
            )(context, builder, value=builder.load(ikj__blxme))
        foxvd__yawp = context.make_helper(builder, string_array_split_view_type
            )
        foxvd__yawp.num_items = mzc__vjiln
        foxvd__yawp.index_offsets = sau__set.index_offsets
        foxvd__yawp.data_offsets = sau__set.data_offsets
        foxvd__yawp.data = mpzf__wnl
        foxvd__yawp.null_bitmap = sau__set.null_bitmap
        context.nrt.incref(builder, data_t, mpzf__wnl)
        foxvd__yawp.meminfo = fmlts__urbmj
        oaix__rpdr = foxvd__yawp._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, oaix__rpdr)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        wagji__ejzsa, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            wagji__ejzsa = builder.extract_value(wagji__ejzsa, 0)
        return builder.bitcast(builder.gep(wagji__ejzsa, [ind]), lir.
            IntType(8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        wagji__ejzsa, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            wagji__ejzsa = builder.extract_value(wagji__ejzsa, 0)
        return builder.load(builder.gep(wagji__ejzsa, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        wagji__ejzsa, ind, ghtb__bojxe = args
        qtpy__tttb = builder.gep(wagji__ejzsa, [ind])
        builder.store(ghtb__bojxe, qtpy__tttb)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        aexn__tsksv, ind = args
        mgc__yucnl = context.make_helper(builder, arr_ctypes_t, aexn__tsksv)
        pzyd__grf = context.make_helper(builder, arr_ctypes_t)
        pzyd__grf.data = builder.gep(mgc__yucnl.data, [ind])
        pzyd__grf.meminfo = mgc__yucnl.meminfo
        rqome__bnd = pzyd__grf._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, rqome__bnd)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    dyf__qvupr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not dyf__qvupr:
        return 0, 0, 0
    edtu__khaa = getitem_c_arr(arr._index_offsets, item_ind)
    uohg__utpqp = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    xzn__rraj = uohg__utpqp - edtu__khaa
    if str_ind >= xzn__rraj:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, edtu__khaa + str_ind)
    data_start += 1
    if edtu__khaa + str_ind == 0:
        data_start = 0
    emez__dom = getitem_c_arr(arr._data_offsets, edtu__khaa + str_ind + 1)
    kzagt__efo = emez__dom - data_start
    return 1, data_start, kzagt__efo


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
        bjs__ujol = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            edtu__khaa = getitem_c_arr(A._index_offsets, ind)
            uohg__utpqp = getitem_c_arr(A._index_offsets, ind + 1)
            ggpp__yxwz = uohg__utpqp - edtu__khaa - 1
            oebw__sjtdj = bodo.libs.str_arr_ext.pre_alloc_string_array(
                ggpp__yxwz, -1)
            for fjgx__kywe in range(ggpp__yxwz):
                data_start = getitem_c_arr(A._data_offsets, edtu__khaa +
                    fjgx__kywe)
                data_start += 1
                if edtu__khaa + fjgx__kywe == 0:
                    data_start = 0
                emez__dom = getitem_c_arr(A._data_offsets, edtu__khaa +
                    fjgx__kywe + 1)
                kzagt__efo = emez__dom - data_start
                qtpy__tttb = get_array_ctypes_ptr(A._data, data_start)
                tnqjk__tfg = bodo.libs.str_arr_ext.decode_utf8(qtpy__tttb,
                    kzagt__efo)
                oebw__sjtdj[fjgx__kywe] = tnqjk__tfg
            return oebw__sjtdj
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        udcc__qxrvj = offset_type.bitwidth // 8

        def _impl(A, ind):
            ggpp__yxwz = len(A)
            if ggpp__yxwz != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            mzc__vjiln = 0
            dqdy__vtpfn = 0
            for fjgx__kywe in range(ggpp__yxwz):
                if ind[fjgx__kywe]:
                    mzc__vjiln += 1
                    edtu__khaa = getitem_c_arr(A._index_offsets, fjgx__kywe)
                    uohg__utpqp = getitem_c_arr(A._index_offsets, 
                        fjgx__kywe + 1)
                    dqdy__vtpfn += uohg__utpqp - edtu__khaa
            vbjij__hgcq = pre_alloc_str_arr_view(mzc__vjiln, dqdy__vtpfn, A
                ._data)
            item_ind = 0
            ffm__xrgf = 0
            for fjgx__kywe in range(ggpp__yxwz):
                if ind[fjgx__kywe]:
                    edtu__khaa = getitem_c_arr(A._index_offsets, fjgx__kywe)
                    uohg__utpqp = getitem_c_arr(A._index_offsets, 
                        fjgx__kywe + 1)
                    domb__sxxi = uohg__utpqp - edtu__khaa
                    setitem_c_arr(vbjij__hgcq._index_offsets, item_ind,
                        ffm__xrgf)
                    qtpy__tttb = get_c_arr_ptr(A._data_offsets, edtu__khaa)
                    qljzp__ppxhi = get_c_arr_ptr(vbjij__hgcq._data_offsets,
                        ffm__xrgf)
                    _memcpy(qljzp__ppxhi, qtpy__tttb, domb__sxxi, udcc__qxrvj)
                    dyf__qvupr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, fjgx__kywe)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vbjij__hgcq.
                        _null_bitmap, item_ind, dyf__qvupr)
                    item_ind += 1
                    ffm__xrgf += domb__sxxi
            setitem_c_arr(vbjij__hgcq._index_offsets, item_ind, ffm__xrgf)
            return vbjij__hgcq
        return _impl
