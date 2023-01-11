"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qktb__uprs = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, qktb__uprs)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        qktb__uprs = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, qktb__uprs)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    aio__ysyld = builder.module
    wqyt__tjv = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    plzbw__dqai = cgutils.get_or_insert_function(aio__ysyld, wqyt__tjv,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not plzbw__dqai.is_declaration:
        return plzbw__dqai
    plzbw__dqai.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(plzbw__dqai.append_basic_block())
    why__tmamc = plzbw__dqai.args[0]
    ctgjs__ncdkh = context.get_value_type(payload_type).as_pointer()
    wmu__qlrt = builder.bitcast(why__tmamc, ctgjs__ncdkh)
    lljw__xfxbv = context.make_helper(builder, payload_type, ref=wmu__qlrt)
    context.nrt.decref(builder, array_item_type.dtype, lljw__xfxbv.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        lljw__xfxbv.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        lljw__xfxbv.null_bitmap)
    builder.ret_void()
    return plzbw__dqai


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    myst__gpe = context.get_value_type(payload_type)
    ggyf__qahn = context.get_abi_sizeof(myst__gpe)
    rru__gvey = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    oibma__ejhbs = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ggyf__qahn), rru__gvey)
    edaz__mazi = context.nrt.meminfo_data(builder, oibma__ejhbs)
    sarff__eul = builder.bitcast(edaz__mazi, myst__gpe.as_pointer())
    lljw__xfxbv = cgutils.create_struct_proxy(payload_type)(context, builder)
    lljw__xfxbv.n_arrays = n_arrays
    ytfb__axx = n_elems.type.count
    rrj__kpku = builder.extract_value(n_elems, 0)
    qhkoj__bshz = cgutils.alloca_once_value(builder, rrj__kpku)
    yko__pwph = builder.icmp_signed('==', rrj__kpku, lir.Constant(rrj__kpku
        .type, -1))
    with builder.if_then(yko__pwph):
        builder.store(n_arrays, qhkoj__bshz)
    n_elems = cgutils.pack_array(builder, [builder.load(qhkoj__bshz)] + [
        builder.extract_value(n_elems, qpm__utovh) for qpm__utovh in range(
        1, ytfb__axx)])
    lljw__xfxbv.data = gen_allocate_array(context, builder, array_item_type
        .dtype, n_elems, c)
    rnf__kav = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    gwo__txvnm = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [rnf__kav])
    offsets_ptr = gwo__txvnm.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    lljw__xfxbv.offsets = gwo__txvnm._getvalue()
    dpfab__obxjh = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    rhzqj__aad = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [dpfab__obxjh])
    null_bitmap_ptr = rhzqj__aad.data
    lljw__xfxbv.null_bitmap = rhzqj__aad._getvalue()
    builder.store(lljw__xfxbv._getvalue(), sarff__eul)
    return oibma__ejhbs, lljw__xfxbv.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    oik__bsc, xoqag__hkyy = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    czyx__oawy = context.insert_const_string(builder.module, 'pandas')
    fsy__dqyaf = c.pyapi.import_module_noblock(czyx__oawy)
    ljve__meby = c.pyapi.object_getattr_string(fsy__dqyaf, 'NA')
    pmz__vckwk = c.context.get_constant(offset_type, 0)
    builder.store(pmz__vckwk, offsets_ptr)
    zhf__pynm = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as srkk__ypan:
        aea__dque = srkk__ypan.index
        item_ind = builder.load(zhf__pynm)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [aea__dque]))
        arr_obj = seq_getitem(builder, context, val, aea__dque)
        set_bitmap_bit(builder, null_bitmap_ptr, aea__dque, 0)
        zpvso__fdb = is_na_value(builder, context, arr_obj, ljve__meby)
        mqj__xqi = builder.icmp_unsigned('!=', zpvso__fdb, lir.Constant(
            zpvso__fdb.type, 1))
        with builder.if_then(mqj__xqi):
            set_bitmap_bit(builder, null_bitmap_ptr, aea__dque, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), zhf__pynm)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(zhf__pynm), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(fsy__dqyaf)
    c.pyapi.decref(ljve__meby)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    ppgf__cge = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if ppgf__cge:
        wqyt__tjv = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        zfauk__vpimw = cgutils.get_or_insert_function(c.builder.module,
            wqyt__tjv, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(
            zfauk__vpimw, [val])])
    else:
        vcbes__ric = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            vcbes__ric, qpm__utovh) for qpm__utovh in range(1, vcbes__ric.
            type.count)])
    oibma__ejhbs, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if ppgf__cge:
        byvgq__uckmb = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ywhtw__rcsit = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        wqyt__tjv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        plzbw__dqai = cgutils.get_or_insert_function(c.builder.module,
            wqyt__tjv, name='array_item_array_from_sequence')
        c.builder.call(plzbw__dqai, [val, c.builder.bitcast(ywhtw__rcsit,
            lir.IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir
            .Constant(lir.IntType(32), byvgq__uckmb)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    iacc__wfm = c.context.make_helper(c.builder, typ)
    iacc__wfm.meminfo = oibma__ejhbs
    odlnh__enilc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(iacc__wfm._getvalue(), is_error=odlnh__enilc)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    iacc__wfm = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    edaz__mazi = context.nrt.meminfo_data(builder, iacc__wfm.meminfo)
    sarff__eul = builder.bitcast(edaz__mazi, context.get_value_type(
        payload_type).as_pointer())
    lljw__xfxbv = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(sarff__eul))
    return lljw__xfxbv


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    czyx__oawy = context.insert_const_string(builder.module, 'numpy')
    xyrp__rog = c.pyapi.import_module_noblock(czyx__oawy)
    blj__frcs = c.pyapi.object_getattr_string(xyrp__rog, 'object_')
    vpbn__wvhbl = c.pyapi.long_from_longlong(n_arrays)
    fbq__gzo = c.pyapi.call_method(xyrp__rog, 'ndarray', (vpbn__wvhbl,
        blj__frcs))
    urtxa__nodc = c.pyapi.object_getattr_string(xyrp__rog, 'nan')
    zhf__pynm = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_arrays) as srkk__ypan:
        aea__dque = srkk__ypan.index
        pyarray_setitem(builder, context, fbq__gzo, aea__dque, urtxa__nodc)
        qkwgb__duh = get_bitmap_bit(builder, null_bitmap_ptr, aea__dque)
        ufnvc__jjon = builder.icmp_unsigned('!=', qkwgb__duh, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(ufnvc__jjon):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(aea__dque, lir.Constant(aea__dque
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                aea__dque]))), lir.IntType(64))
            item_ind = builder.load(zhf__pynm)
            oik__bsc, rfw__dbcq = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), zhf__pynm)
            arr_obj = c.pyapi.from_native_value(typ.dtype, rfw__dbcq, c.
                env_manager)
            pyarray_setitem(builder, context, fbq__gzo, aea__dque, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(xyrp__rog)
    c.pyapi.decref(blj__frcs)
    c.pyapi.decref(vpbn__wvhbl)
    c.pyapi.decref(urtxa__nodc)
    return fbq__gzo


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    lljw__xfxbv = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = lljw__xfxbv.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), lljw__xfxbv.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), lljw__xfxbv.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        byvgq__uckmb = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ywhtw__rcsit = c.context.make_helper(c.builder, typ.dtype, data_arr
            ).data
        wqyt__tjv = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        fdybt__linv = cgutils.get_or_insert_function(c.builder.module,
            wqyt__tjv, name='np_array_from_array_item_array')
        arr = c.builder.call(fdybt__linv, [lljw__xfxbv.n_arrays, c.builder.
            bitcast(ywhtw__rcsit, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), byvgq__uckmb)])
    else:
        arr = _box_array_item_array_generic(typ, c, lljw__xfxbv.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    xzst__eoxc, ptf__mlxvz, nbk__oak = args
    wbq__sjfu = bodo.utils.transform.get_type_alloc_counts(array_item_type.
        dtype)
    dms__phqb = sig.args[1]
    if not isinstance(dms__phqb, types.UniTuple):
        ptf__mlxvz = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for nbk__oak in range(wbq__sjfu)])
    elif dms__phqb.count < wbq__sjfu:
        ptf__mlxvz = cgutils.pack_array(builder, [builder.extract_value(
            ptf__mlxvz, qpm__utovh) for qpm__utovh in range(dms__phqb.count
            )] + [lir.Constant(lir.IntType(64), -1) for nbk__oak in range(
            wbq__sjfu - dms__phqb.count)])
    oibma__ejhbs, nbk__oak, nbk__oak, nbk__oak = construct_array_item_array(
        context, builder, array_item_type, xzst__eoxc, ptf__mlxvz)
    iacc__wfm = context.make_helper(builder, array_item_type)
    iacc__wfm.meminfo = oibma__ejhbs
    return iacc__wfm._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, gowlg__wdbwn, gwo__txvnm, rhzqj__aad = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    myst__gpe = context.get_value_type(payload_type)
    ggyf__qahn = context.get_abi_sizeof(myst__gpe)
    rru__gvey = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    oibma__ejhbs = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ggyf__qahn), rru__gvey)
    edaz__mazi = context.nrt.meminfo_data(builder, oibma__ejhbs)
    sarff__eul = builder.bitcast(edaz__mazi, myst__gpe.as_pointer())
    lljw__xfxbv = cgutils.create_struct_proxy(payload_type)(context, builder)
    lljw__xfxbv.n_arrays = n_arrays
    lljw__xfxbv.data = gowlg__wdbwn
    lljw__xfxbv.offsets = gwo__txvnm
    lljw__xfxbv.null_bitmap = rhzqj__aad
    builder.store(lljw__xfxbv._getvalue(), sarff__eul)
    context.nrt.incref(builder, signature.args[1], gowlg__wdbwn)
    context.nrt.incref(builder, signature.args[2], gwo__txvnm)
    context.nrt.incref(builder, signature.args[3], rhzqj__aad)
    iacc__wfm = context.make_helper(builder, array_item_type)
    iacc__wfm.meminfo = oibma__ejhbs
    return iacc__wfm._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    kxyld__nczdg = ArrayItemArrayType(data_type)
    sig = kxyld__nczdg(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lljw__xfxbv = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lljw__xfxbv.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        lljw__xfxbv = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        ywhtw__rcsit = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, lljw__xfxbv.offsets).data
        gwo__txvnm = builder.bitcast(ywhtw__rcsit, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(gwo__txvnm, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lljw__xfxbv = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lljw__xfxbv.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lljw__xfxbv = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lljw__xfxbv.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


def alias_ext_single_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_offsets',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_data',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_null_bitmap',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lljw__xfxbv = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return lljw__xfxbv.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, lbafr__wtg = args
        iacc__wfm = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        edaz__mazi = context.nrt.meminfo_data(builder, iacc__wfm.meminfo)
        sarff__eul = builder.bitcast(edaz__mazi, context.get_value_type(
            payload_type).as_pointer())
        lljw__xfxbv = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(sarff__eul))
        context.nrt.decref(builder, data_typ, lljw__xfxbv.data)
        lljw__xfxbv.data = lbafr__wtg
        context.nrt.incref(builder, data_typ, lbafr__wtg)
        builder.store(lljw__xfxbv._getvalue(), sarff__eul)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    gowlg__wdbwn = get_data(arr)
    cikg__krn = len(gowlg__wdbwn)
    if cikg__krn < new_size:
        xujh__qcs = max(2 * cikg__krn, new_size)
        lbafr__wtg = bodo.libs.array_kernels.resize_and_copy(gowlg__wdbwn,
            old_size, xujh__qcs)
        replace_data_arr(arr, lbafr__wtg)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    gowlg__wdbwn = get_data(arr)
    gwo__txvnm = get_offsets(arr)
    mvpa__khwct = len(gowlg__wdbwn)
    hclo__otfrc = gwo__txvnm[-1]
    if mvpa__khwct != hclo__otfrc:
        lbafr__wtg = bodo.libs.array_kernels.resize_and_copy(gowlg__wdbwn,
            hclo__otfrc, hclo__otfrc)
        replace_data_arr(arr, lbafr__wtg)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            gwo__txvnm = get_offsets(arr)
            gowlg__wdbwn = get_data(arr)
            fyc__qiu = gwo__txvnm[ind]
            dflp__ogk = gwo__txvnm[ind + 1]
            return gowlg__wdbwn[fyc__qiu:dflp__ogk]
        return array_item_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:
        sqtwu__mayp = arr.dtype

        def impl_bool(arr, ind):
            aud__gjjuy = len(arr)
            if aud__gjjuy != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            rhzqj__aad = get_null_bitmap(arr)
            n_arrays = 0
            qgee__lczes = init_nested_counts(sqtwu__mayp)
            for qpm__utovh in range(aud__gjjuy):
                if ind[qpm__utovh]:
                    n_arrays += 1
                    cvtb__trsdd = arr[qpm__utovh]
                    qgee__lczes = add_nested_counts(qgee__lczes, cvtb__trsdd)
            fbq__gzo = pre_alloc_array_item_array(n_arrays, qgee__lczes,
                sqtwu__mayp)
            yknp__hiiu = get_null_bitmap(fbq__gzo)
            gqe__xjm = 0
            for xuqvk__tfwy in range(aud__gjjuy):
                if ind[xuqvk__tfwy]:
                    fbq__gzo[gqe__xjm] = arr[xuqvk__tfwy]
                    mfqul__inw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        rhzqj__aad, xuqvk__tfwy)
                    bodo.libs.int_arr_ext.set_bit_to_arr(yknp__hiiu,
                        gqe__xjm, mfqul__inw)
                    gqe__xjm += 1
            return fbq__gzo
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        sqtwu__mayp = arr.dtype

        def impl_int(arr, ind):
            rhzqj__aad = get_null_bitmap(arr)
            aud__gjjuy = len(ind)
            n_arrays = aud__gjjuy
            qgee__lczes = init_nested_counts(sqtwu__mayp)
            for wlz__uovfu in range(aud__gjjuy):
                qpm__utovh = ind[wlz__uovfu]
                cvtb__trsdd = arr[qpm__utovh]
                qgee__lczes = add_nested_counts(qgee__lczes, cvtb__trsdd)
            fbq__gzo = pre_alloc_array_item_array(n_arrays, qgee__lczes,
                sqtwu__mayp)
            yknp__hiiu = get_null_bitmap(fbq__gzo)
            for tcgs__iih in range(aud__gjjuy):
                xuqvk__tfwy = ind[tcgs__iih]
                fbq__gzo[tcgs__iih] = arr[xuqvk__tfwy]
                mfqul__inw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    rhzqj__aad, xuqvk__tfwy)
                bodo.libs.int_arr_ext.set_bit_to_arr(yknp__hiiu, tcgs__iih,
                    mfqul__inw)
            return fbq__gzo
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            aud__gjjuy = len(arr)
            kan__qpvtu = numba.cpython.unicode._normalize_slice(ind, aud__gjjuy
                )
            oiwc__unj = np.arange(kan__qpvtu.start, kan__qpvtu.stop,
                kan__qpvtu.step)
            return arr[oiwc__unj]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            gwo__txvnm = get_offsets(A)
            rhzqj__aad = get_null_bitmap(A)
            if idx == 0:
                gwo__txvnm[0] = 0
            n_items = len(val)
            khsc__lep = gwo__txvnm[idx] + n_items
            ensure_data_capacity(A, gwo__txvnm[idx], khsc__lep)
            gowlg__wdbwn = get_data(A)
            gwo__txvnm[idx + 1] = gwo__txvnm[idx] + n_items
            gowlg__wdbwn[gwo__txvnm[idx]:gwo__txvnm[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(rhzqj__aad, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            kan__qpvtu = numba.cpython.unicode._normalize_slice(idx, len(A))
            for qpm__utovh in range(kan__qpvtu.start, kan__qpvtu.stop,
                kan__qpvtu.step):
                A[qpm__utovh] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            gwo__txvnm = get_offsets(A)
            rhzqj__aad = get_null_bitmap(A)
            pxni__gwo = get_offsets(val)
            cvphq__qqnlp = get_data(val)
            sjc__fcaab = get_null_bitmap(val)
            aud__gjjuy = len(A)
            kan__qpvtu = numba.cpython.unicode._normalize_slice(idx, aud__gjjuy
                )
            kpfd__faybz, sbnzi__lddy = kan__qpvtu.start, kan__qpvtu.stop
            assert kan__qpvtu.step == 1
            if kpfd__faybz == 0:
                gwo__txvnm[kpfd__faybz] = 0
            dgcrp__etl = gwo__txvnm[kpfd__faybz]
            khsc__lep = dgcrp__etl + len(cvphq__qqnlp)
            ensure_data_capacity(A, dgcrp__etl, khsc__lep)
            gowlg__wdbwn = get_data(A)
            gowlg__wdbwn[dgcrp__etl:dgcrp__etl + len(cvphq__qqnlp)
                ] = cvphq__qqnlp
            gwo__txvnm[kpfd__faybz:sbnzi__lddy + 1] = pxni__gwo + dgcrp__etl
            hsf__fie = 0
            for qpm__utovh in range(kpfd__faybz, sbnzi__lddy):
                mfqul__inw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    sjc__fcaab, hsf__fie)
                bodo.libs.int_arr_ext.set_bit_to_arr(rhzqj__aad, qpm__utovh,
                    mfqul__inw)
                hsf__fie += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
