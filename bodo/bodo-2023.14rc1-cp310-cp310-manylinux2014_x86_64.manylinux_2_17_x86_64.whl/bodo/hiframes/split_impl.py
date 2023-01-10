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
        clql__pyrve = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, clql__pyrve)


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
    nxb__ugb = context.get_value_type(str_arr_split_view_payload_type)
    luy__pmecf = context.get_abi_sizeof(nxb__ugb)
    mswj__ypf = context.get_value_type(types.voidptr)
    ysxmz__bal = context.get_value_type(types.uintp)
    otq__tnl = lir.FunctionType(lir.VoidType(), [mswj__ypf, ysxmz__bal,
        mswj__ypf])
    ntx__acp = cgutils.get_or_insert_function(builder.module, otq__tnl,
        name='dtor_str_arr_split_view')
    immhu__fny = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, luy__pmecf), ntx__acp)
    wemyi__ocsk = context.nrt.meminfo_data(builder, immhu__fny)
    rdmm__qxin = builder.bitcast(wemyi__ocsk, nxb__ugb.as_pointer())
    return immhu__fny, rdmm__qxin


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        qzb__fzxj, fsuf__ovn = args
        immhu__fny, rdmm__qxin = construct_str_arr_split_view(context, builder)
        bjv__cgl = _get_str_binary_arr_payload(context, builder, qzb__fzxj,
            string_array_type)
        lxe__gwjbt = lir.FunctionType(lir.VoidType(), [rdmm__qxin.type, lir
            .IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        fkyy__stab = cgutils.get_or_insert_function(builder.module,
            lxe__gwjbt, name='str_arr_split_view_impl')
        ikl__iudd = context.make_helper(builder, offset_arr_type, bjv__cgl.
            offsets).data
        cfy__mjt = context.make_helper(builder, char_arr_type, bjv__cgl.data
            ).data
        qxen__loue = context.make_helper(builder, null_bitmap_arr_type,
            bjv__cgl.null_bitmap).data
        tozr__uonr = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(fkyy__stab, [rdmm__qxin, bjv__cgl.n_arrays, ikl__iudd,
            cfy__mjt, qxen__loue, tozr__uonr])
        nhir__rrun = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(rdmm__qxin))
        okpb__utn = context.make_helper(builder, string_array_split_view_type)
        okpb__utn.num_items = bjv__cgl.n_arrays
        okpb__utn.index_offsets = nhir__rrun.index_offsets
        okpb__utn.data_offsets = nhir__rrun.data_offsets
        okpb__utn.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [qzb__fzxj])
        okpb__utn.null_bitmap = nhir__rrun.null_bitmap
        okpb__utn.meminfo = immhu__fny
        obmod__juv = okpb__utn._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, obmod__juv)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    agm__pfw = context.make_helper(builder, string_array_split_view_type, val)
    ofhel__dpfvp = context.insert_const_string(builder.module, 'numpy')
    dnfj__yoq = c.pyapi.import_module_noblock(ofhel__dpfvp)
    dtype = c.pyapi.object_getattr_string(dnfj__yoq, 'object_')
    jjii__yoock = builder.sext(agm__pfw.num_items, c.pyapi.longlong)
    gjy__nsri = c.pyapi.long_from_longlong(jjii__yoock)
    rcqhh__neuk = c.pyapi.call_method(dnfj__yoq, 'ndarray', (gjy__nsri, dtype))
    mor__uwa = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.pyobj,
        c.pyapi.py_ssize_t])
    rke__pdd = c.pyapi._get_function(mor__uwa, name='array_getptr1')
    xvm__wpk = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.IntType
        (8).as_pointer(), c.pyapi.pyobj])
    joyc__yitri = c.pyapi._get_function(xvm__wpk, name='array_setitem')
    mniij__bikgb = c.pyapi.object_getattr_string(dnfj__yoq, 'nan')
    with cgutils.for_range(builder, agm__pfw.num_items) as yak__azvl:
        str_ind = yak__azvl.index
        jql__qtyfw = builder.sext(builder.load(builder.gep(agm__pfw.
            index_offsets, [str_ind])), lir.IntType(64))
        urn__dgi = builder.sext(builder.load(builder.gep(agm__pfw.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        jjoos__jbrca = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        rhw__zjkp = builder.gep(agm__pfw.null_bitmap, [jjoos__jbrca])
        wdt__ohv = builder.load(rhw__zjkp)
        ydfv__uwrcb = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(wdt__ohv, ydfv__uwrcb), lir.
            Constant(lir.IntType(8), 1))
        pav__ntdmn = builder.sub(urn__dgi, jql__qtyfw)
        pav__ntdmn = builder.sub(pav__ntdmn, pav__ntdmn.type(1))
        gkiy__kvl = builder.call(rke__pdd, [rcqhh__neuk, str_ind])
        yzb__glbzk = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(yzb__glbzk) as (ueo__dvdo, moct__pzazf):
            with ueo__dvdo:
                eabk__xrmjq = c.pyapi.list_new(pav__ntdmn)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    eabk__xrmjq), likely=True):
                    with cgutils.for_range(c.builder, pav__ntdmn) as yak__azvl:
                        jti__hdddp = builder.add(jql__qtyfw, yak__azvl.index)
                        data_start = builder.load(builder.gep(agm__pfw.
                            data_offsets, [jti__hdddp]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        arf__ehr = builder.load(builder.gep(agm__pfw.
                            data_offsets, [builder.add(jti__hdddp,
                            jti__hdddp.type(1))]))
                        khrtd__xjz = builder.gep(builder.extract_value(
                            agm__pfw.data, 0), [data_start])
                        ovhe__hxc = builder.sext(builder.sub(arf__ehr,
                            data_start), lir.IntType(64))
                        pkur__zean = c.pyapi.string_from_string_and_size(
                            khrtd__xjz, ovhe__hxc)
                        c.pyapi.list_setitem(eabk__xrmjq, yak__azvl.index,
                            pkur__zean)
                builder.call(joyc__yitri, [rcqhh__neuk, gkiy__kvl, eabk__xrmjq]
                    )
            with moct__pzazf:
                builder.call(joyc__yitri, [rcqhh__neuk, gkiy__kvl,
                    mniij__bikgb])
    c.pyapi.decref(dnfj__yoq)
    c.pyapi.decref(dtype)
    c.pyapi.decref(mniij__bikgb)
    return rcqhh__neuk


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        blzs__hvcpl, jmkvq__qkh, khrtd__xjz = args
        immhu__fny, rdmm__qxin = construct_str_arr_split_view(context, builder)
        lxe__gwjbt = lir.FunctionType(lir.VoidType(), [rdmm__qxin.type, lir
            .IntType(64), lir.IntType(64)])
        fkyy__stab = cgutils.get_or_insert_function(builder.module,
            lxe__gwjbt, name='str_arr_split_view_alloc')
        builder.call(fkyy__stab, [rdmm__qxin, blzs__hvcpl, jmkvq__qkh])
        nhir__rrun = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(rdmm__qxin))
        okpb__utn = context.make_helper(builder, string_array_split_view_type)
        okpb__utn.num_items = blzs__hvcpl
        okpb__utn.index_offsets = nhir__rrun.index_offsets
        okpb__utn.data_offsets = nhir__rrun.data_offsets
        okpb__utn.data = khrtd__xjz
        okpb__utn.null_bitmap = nhir__rrun.null_bitmap
        context.nrt.incref(builder, data_t, khrtd__xjz)
        okpb__utn.meminfo = immhu__fny
        obmod__juv = okpb__utn._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, obmod__juv)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        mriam__akl, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            mriam__akl = builder.extract_value(mriam__akl, 0)
        return builder.bitcast(builder.gep(mriam__akl, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        mriam__akl, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            mriam__akl = builder.extract_value(mriam__akl, 0)
        return builder.load(builder.gep(mriam__akl, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        mriam__akl, ind, ordhz__cyeqg = args
        yvpd__kodr = builder.gep(mriam__akl, [ind])
        builder.store(ordhz__cyeqg, yvpd__kodr)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        nain__yur, ind = args
        yrbwq__hsrua = context.make_helper(builder, arr_ctypes_t, nain__yur)
        hbps__fia = context.make_helper(builder, arr_ctypes_t)
        hbps__fia.data = builder.gep(yrbwq__hsrua.data, [ind])
        hbps__fia.meminfo = yrbwq__hsrua.meminfo
        yyc__lll = hbps__fia._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, yyc__lll)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    cgx__jca = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not cgx__jca:
        return 0, 0, 0
    jti__hdddp = getitem_c_arr(arr._index_offsets, item_ind)
    hip__pqsj = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    uzn__nut = hip__pqsj - jti__hdddp
    if str_ind >= uzn__nut:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, jti__hdddp + str_ind)
    data_start += 1
    if jti__hdddp + str_ind == 0:
        data_start = 0
    arf__ehr = getitem_c_arr(arr._data_offsets, jti__hdddp + str_ind + 1)
    rogyo__gdpaa = arf__ehr - data_start
    return 1, data_start, rogyo__gdpaa


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
        iplmv__wsg = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            jti__hdddp = getitem_c_arr(A._index_offsets, ind)
            hip__pqsj = getitem_c_arr(A._index_offsets, ind + 1)
            dbnx__owibo = hip__pqsj - jti__hdddp - 1
            qzb__fzxj = bodo.libs.str_arr_ext.pre_alloc_string_array(
                dbnx__owibo, -1)
            for emi__rtyfd in range(dbnx__owibo):
                data_start = getitem_c_arr(A._data_offsets, jti__hdddp +
                    emi__rtyfd)
                data_start += 1
                if jti__hdddp + emi__rtyfd == 0:
                    data_start = 0
                arf__ehr = getitem_c_arr(A._data_offsets, jti__hdddp +
                    emi__rtyfd + 1)
                rogyo__gdpaa = arf__ehr - data_start
                yvpd__kodr = get_array_ctypes_ptr(A._data, data_start)
                wos__mkh = bodo.libs.str_arr_ext.decode_utf8(yvpd__kodr,
                    rogyo__gdpaa)
                qzb__fzxj[emi__rtyfd] = wos__mkh
            return qzb__fzxj
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        vnsu__szx = offset_type.bitwidth // 8

        def _impl(A, ind):
            dbnx__owibo = len(A)
            if dbnx__owibo != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            blzs__hvcpl = 0
            jmkvq__qkh = 0
            for emi__rtyfd in range(dbnx__owibo):
                if ind[emi__rtyfd]:
                    blzs__hvcpl += 1
                    jti__hdddp = getitem_c_arr(A._index_offsets, emi__rtyfd)
                    hip__pqsj = getitem_c_arr(A._index_offsets, emi__rtyfd + 1)
                    jmkvq__qkh += hip__pqsj - jti__hdddp
            rcqhh__neuk = pre_alloc_str_arr_view(blzs__hvcpl, jmkvq__qkh, A
                ._data)
            item_ind = 0
            xmxkh__vhrfz = 0
            for emi__rtyfd in range(dbnx__owibo):
                if ind[emi__rtyfd]:
                    jti__hdddp = getitem_c_arr(A._index_offsets, emi__rtyfd)
                    hip__pqsj = getitem_c_arr(A._index_offsets, emi__rtyfd + 1)
                    bxp__quz = hip__pqsj - jti__hdddp
                    setitem_c_arr(rcqhh__neuk._index_offsets, item_ind,
                        xmxkh__vhrfz)
                    yvpd__kodr = get_c_arr_ptr(A._data_offsets, jti__hdddp)
                    gxed__xcv = get_c_arr_ptr(rcqhh__neuk._data_offsets,
                        xmxkh__vhrfz)
                    _memcpy(gxed__xcv, yvpd__kodr, bxp__quz, vnsu__szx)
                    cgx__jca = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, emi__rtyfd)
                    bodo.libs.int_arr_ext.set_bit_to_arr(rcqhh__neuk.
                        _null_bitmap, item_ind, cgx__jca)
                    item_ind += 1
                    xmxkh__vhrfz += bxp__quz
            setitem_c_arr(rcqhh__neuk._index_offsets, item_ind, xmxkh__vhrfz)
            return rcqhh__neuk
        return _impl
