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
        bzwp__zxpe = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, bzwp__zxpe)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        bzwp__zxpe = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, bzwp__zxpe)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    zaqi__hga = builder.module
    feafh__vigux = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    xmiok__tuoky = cgutils.get_or_insert_function(zaqi__hga, feafh__vigux,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not xmiok__tuoky.is_declaration:
        return xmiok__tuoky
    xmiok__tuoky.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(xmiok__tuoky.append_basic_block())
    yam__kegw = xmiok__tuoky.args[0]
    xkqb__gfl = context.get_value_type(payload_type).as_pointer()
    frhg__qsueg = builder.bitcast(yam__kegw, xkqb__gfl)
    pdm__bdow = context.make_helper(builder, payload_type, ref=frhg__qsueg)
    context.nrt.decref(builder, array_item_type.dtype, pdm__bdow.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), pdm__bdow
        .offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), pdm__bdow
        .null_bitmap)
    builder.ret_void()
    return xmiok__tuoky


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    eky__ygq = context.get_value_type(payload_type)
    mcp__ojf = context.get_abi_sizeof(eky__ygq)
    qnils__amri = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    weqkf__uvhg = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, mcp__ojf), qnils__amri)
    wyo__umj = context.nrt.meminfo_data(builder, weqkf__uvhg)
    zsri__rkub = builder.bitcast(wyo__umj, eky__ygq.as_pointer())
    pdm__bdow = cgutils.create_struct_proxy(payload_type)(context, builder)
    pdm__bdow.n_arrays = n_arrays
    fciw__gfbcd = n_elems.type.count
    duesj__sxgp = builder.extract_value(n_elems, 0)
    zemlf__yuxdp = cgutils.alloca_once_value(builder, duesj__sxgp)
    mos__xqwxi = builder.icmp_signed('==', duesj__sxgp, lir.Constant(
        duesj__sxgp.type, -1))
    with builder.if_then(mos__xqwxi):
        builder.store(n_arrays, zemlf__yuxdp)
    n_elems = cgutils.pack_array(builder, [builder.load(zemlf__yuxdp)] + [
        builder.extract_value(n_elems, rqz__krabd) for rqz__krabd in range(
        1, fciw__gfbcd)])
    pdm__bdow.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    xqn__wrtka = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    nzdzk__mnz = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [xqn__wrtka])
    offsets_ptr = nzdzk__mnz.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    pdm__bdow.offsets = nzdzk__mnz._getvalue()
    hna__lanep = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    tjdnw__jxjvz = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [hna__lanep])
    null_bitmap_ptr = tjdnw__jxjvz.data
    pdm__bdow.null_bitmap = tjdnw__jxjvz._getvalue()
    builder.store(pdm__bdow._getvalue(), zsri__rkub)
    return weqkf__uvhg, pdm__bdow.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    vsbs__rul, tfur__lxzt = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    thn__afg = context.insert_const_string(builder.module, 'pandas')
    ftuh__ovaa = c.pyapi.import_module_noblock(thn__afg)
    tuta__sbdi = c.pyapi.object_getattr_string(ftuh__ovaa, 'NA')
    zkkx__lbs = c.context.get_constant(offset_type, 0)
    builder.store(zkkx__lbs, offsets_ptr)
    qms__joiu = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as eskrs__jir:
        hblx__gskzd = eskrs__jir.index
        item_ind = builder.load(qms__joiu)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [hblx__gskzd]))
        arr_obj = seq_getitem(builder, context, val, hblx__gskzd)
        set_bitmap_bit(builder, null_bitmap_ptr, hblx__gskzd, 0)
        llhui__ulib = is_na_value(builder, context, arr_obj, tuta__sbdi)
        lfl__eha = builder.icmp_unsigned('!=', llhui__ulib, lir.Constant(
            llhui__ulib.type, 1))
        with builder.if_then(lfl__eha):
            set_bitmap_bit(builder, null_bitmap_ptr, hblx__gskzd, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), qms__joiu)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(qms__joiu), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(ftuh__ovaa)
    c.pyapi.decref(tuta__sbdi)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    vand__hnpn = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if vand__hnpn:
        feafh__vigux = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        fes__qerao = cgutils.get_or_insert_function(c.builder.module,
            feafh__vigux, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(fes__qerao,
            [val])])
    else:
        rxf__laya = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            rxf__laya, rqz__krabd) for rqz__krabd in range(1, rxf__laya.
            type.count)])
    weqkf__uvhg, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if vand__hnpn:
        wpwr__xfl = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        quisl__ljp = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        feafh__vigux = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        xmiok__tuoky = cgutils.get_or_insert_function(c.builder.module,
            feafh__vigux, name='array_item_array_from_sequence')
        c.builder.call(xmiok__tuoky, [val, c.builder.bitcast(quisl__ljp,
            lir.IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir
            .Constant(lir.IntType(32), wpwr__xfl)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    gmeqb__mvoye = c.context.make_helper(c.builder, typ)
    gmeqb__mvoye.meminfo = weqkf__uvhg
    hrlhd__lghgn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gmeqb__mvoye._getvalue(), is_error=hrlhd__lghgn)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    gmeqb__mvoye = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    wyo__umj = context.nrt.meminfo_data(builder, gmeqb__mvoye.meminfo)
    zsri__rkub = builder.bitcast(wyo__umj, context.get_value_type(
        payload_type).as_pointer())
    pdm__bdow = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(zsri__rkub))
    return pdm__bdow


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    thn__afg = context.insert_const_string(builder.module, 'numpy')
    hguwj__mypl = c.pyapi.import_module_noblock(thn__afg)
    lja__cwjwq = c.pyapi.object_getattr_string(hguwj__mypl, 'object_')
    mtz__zkad = c.pyapi.long_from_longlong(n_arrays)
    fhzd__kzk = c.pyapi.call_method(hguwj__mypl, 'ndarray', (mtz__zkad,
        lja__cwjwq))
    gzer__rfnmf = c.pyapi.object_getattr_string(hguwj__mypl, 'nan')
    qms__joiu = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_arrays) as eskrs__jir:
        hblx__gskzd = eskrs__jir.index
        pyarray_setitem(builder, context, fhzd__kzk, hblx__gskzd, gzer__rfnmf)
        prfa__xpb = get_bitmap_bit(builder, null_bitmap_ptr, hblx__gskzd)
        nboh__kujws = builder.icmp_unsigned('!=', prfa__xpb, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(nboh__kujws):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(hblx__gskzd, lir.Constant(
                hblx__gskzd.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [hblx__gskzd]))), lir.IntType(64))
            item_ind = builder.load(qms__joiu)
            vsbs__rul, yxs__rps = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), qms__joiu)
            arr_obj = c.pyapi.from_native_value(typ.dtype, yxs__rps, c.
                env_manager)
            pyarray_setitem(builder, context, fhzd__kzk, hblx__gskzd, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(hguwj__mypl)
    c.pyapi.decref(lja__cwjwq)
    c.pyapi.decref(mtz__zkad)
    c.pyapi.decref(gzer__rfnmf)
    return fhzd__kzk


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    pdm__bdow = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = pdm__bdow.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), pdm__bdow.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), pdm__bdow.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        wpwr__xfl = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        quisl__ljp = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        feafh__vigux = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        ale__ruqc = cgutils.get_or_insert_function(c.builder.module,
            feafh__vigux, name='np_array_from_array_item_array')
        arr = c.builder.call(ale__ruqc, [pdm__bdow.n_arrays, c.builder.
            bitcast(quisl__ljp, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), wpwr__xfl)])
    else:
        arr = _box_array_item_array_generic(typ, c, pdm__bdow.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    sjvtq__uubki, qfn__qmolk, nsofb__uikx = args
    fqcq__jjgc = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    ewcrl__feq = sig.args[1]
    if not isinstance(ewcrl__feq, types.UniTuple):
        qfn__qmolk = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for nsofb__uikx in range(fqcq__jjgc)])
    elif ewcrl__feq.count < fqcq__jjgc:
        qfn__qmolk = cgutils.pack_array(builder, [builder.extract_value(
            qfn__qmolk, rqz__krabd) for rqz__krabd in range(ewcrl__feq.
            count)] + [lir.Constant(lir.IntType(64), -1) for nsofb__uikx in
            range(fqcq__jjgc - ewcrl__feq.count)])
    weqkf__uvhg, nsofb__uikx, nsofb__uikx, nsofb__uikx = (
        construct_array_item_array(context, builder, array_item_type,
        sjvtq__uubki, qfn__qmolk))
    gmeqb__mvoye = context.make_helper(builder, array_item_type)
    gmeqb__mvoye.meminfo = weqkf__uvhg
    return gmeqb__mvoye._getvalue()


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
    n_arrays, cgv__kdjld, nzdzk__mnz, tjdnw__jxjvz = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    eky__ygq = context.get_value_type(payload_type)
    mcp__ojf = context.get_abi_sizeof(eky__ygq)
    qnils__amri = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    weqkf__uvhg = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, mcp__ojf), qnils__amri)
    wyo__umj = context.nrt.meminfo_data(builder, weqkf__uvhg)
    zsri__rkub = builder.bitcast(wyo__umj, eky__ygq.as_pointer())
    pdm__bdow = cgutils.create_struct_proxy(payload_type)(context, builder)
    pdm__bdow.n_arrays = n_arrays
    pdm__bdow.data = cgv__kdjld
    pdm__bdow.offsets = nzdzk__mnz
    pdm__bdow.null_bitmap = tjdnw__jxjvz
    builder.store(pdm__bdow._getvalue(), zsri__rkub)
    context.nrt.incref(builder, signature.args[1], cgv__kdjld)
    context.nrt.incref(builder, signature.args[2], nzdzk__mnz)
    context.nrt.incref(builder, signature.args[3], tjdnw__jxjvz)
    gmeqb__mvoye = context.make_helper(builder, array_item_type)
    gmeqb__mvoye.meminfo = weqkf__uvhg
    return gmeqb__mvoye._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    nym__rub = ArrayItemArrayType(data_type)
    sig = nym__rub(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        pdm__bdow = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            pdm__bdow.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        pdm__bdow = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        quisl__ljp = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, pdm__bdow.offsets).data
        nzdzk__mnz = builder.bitcast(quisl__ljp, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(nzdzk__mnz, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        pdm__bdow = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            pdm__bdow.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        pdm__bdow = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            pdm__bdow.null_bitmap)
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
        pdm__bdow = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return pdm__bdow.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, mljrj__eaujp = args
        gmeqb__mvoye = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        wyo__umj = context.nrt.meminfo_data(builder, gmeqb__mvoye.meminfo)
        zsri__rkub = builder.bitcast(wyo__umj, context.get_value_type(
            payload_type).as_pointer())
        pdm__bdow = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(zsri__rkub))
        context.nrt.decref(builder, data_typ, pdm__bdow.data)
        pdm__bdow.data = mljrj__eaujp
        context.nrt.incref(builder, data_typ, mljrj__eaujp)
        builder.store(pdm__bdow._getvalue(), zsri__rkub)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    cgv__kdjld = get_data(arr)
    mmhk__lubfw = len(cgv__kdjld)
    if mmhk__lubfw < new_size:
        jgro__bsnjx = max(2 * mmhk__lubfw, new_size)
        mljrj__eaujp = bodo.libs.array_kernels.resize_and_copy(cgv__kdjld,
            old_size, jgro__bsnjx)
        replace_data_arr(arr, mljrj__eaujp)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    cgv__kdjld = get_data(arr)
    nzdzk__mnz = get_offsets(arr)
    rgwvx__vem = len(cgv__kdjld)
    phre__wvkrf = nzdzk__mnz[-1]
    if rgwvx__vem != phre__wvkrf:
        mljrj__eaujp = bodo.libs.array_kernels.resize_and_copy(cgv__kdjld,
            phre__wvkrf, phre__wvkrf)
        replace_data_arr(arr, mljrj__eaujp)


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
            nzdzk__mnz = get_offsets(arr)
            cgv__kdjld = get_data(arr)
            tlqv__erkiq = nzdzk__mnz[ind]
            qhd__kkzg = nzdzk__mnz[ind + 1]
            return cgv__kdjld[tlqv__erkiq:qhd__kkzg]
        return array_item_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:
        zbsj__kpfee = arr.dtype

        def impl_bool(arr, ind):
            lzc__hhjp = len(arr)
            if lzc__hhjp != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            tjdnw__jxjvz = get_null_bitmap(arr)
            n_arrays = 0
            spqi__ukklv = init_nested_counts(zbsj__kpfee)
            for rqz__krabd in range(lzc__hhjp):
                if ind[rqz__krabd]:
                    n_arrays += 1
                    lqqh__efsm = arr[rqz__krabd]
                    spqi__ukklv = add_nested_counts(spqi__ukklv, lqqh__efsm)
            fhzd__kzk = pre_alloc_array_item_array(n_arrays, spqi__ukklv,
                zbsj__kpfee)
            vysxq__mkdo = get_null_bitmap(fhzd__kzk)
            azi__jtp = 0
            for uzab__whd in range(lzc__hhjp):
                if ind[uzab__whd]:
                    fhzd__kzk[azi__jtp] = arr[uzab__whd]
                    lhtt__zpp = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        tjdnw__jxjvz, uzab__whd)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vysxq__mkdo,
                        azi__jtp, lhtt__zpp)
                    azi__jtp += 1
            return fhzd__kzk
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        zbsj__kpfee = arr.dtype

        def impl_int(arr, ind):
            tjdnw__jxjvz = get_null_bitmap(arr)
            lzc__hhjp = len(ind)
            n_arrays = lzc__hhjp
            spqi__ukklv = init_nested_counts(zbsj__kpfee)
            for ffhi__irkyp in range(lzc__hhjp):
                rqz__krabd = ind[ffhi__irkyp]
                lqqh__efsm = arr[rqz__krabd]
                spqi__ukklv = add_nested_counts(spqi__ukklv, lqqh__efsm)
            fhzd__kzk = pre_alloc_array_item_array(n_arrays, spqi__ukklv,
                zbsj__kpfee)
            vysxq__mkdo = get_null_bitmap(fhzd__kzk)
            for ovo__iyb in range(lzc__hhjp):
                uzab__whd = ind[ovo__iyb]
                fhzd__kzk[ovo__iyb] = arr[uzab__whd]
                lhtt__zpp = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    tjdnw__jxjvz, uzab__whd)
                bodo.libs.int_arr_ext.set_bit_to_arr(vysxq__mkdo, ovo__iyb,
                    lhtt__zpp)
            return fhzd__kzk
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            lzc__hhjp = len(arr)
            kvrfl__qkiml = numba.cpython.unicode._normalize_slice(ind,
                lzc__hhjp)
            ertl__zax = np.arange(kvrfl__qkiml.start, kvrfl__qkiml.stop,
                kvrfl__qkiml.step)
            return arr[ertl__zax]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            nzdzk__mnz = get_offsets(A)
            tjdnw__jxjvz = get_null_bitmap(A)
            if idx == 0:
                nzdzk__mnz[0] = 0
            n_items = len(val)
            tqtws__ustw = nzdzk__mnz[idx] + n_items
            ensure_data_capacity(A, nzdzk__mnz[idx], tqtws__ustw)
            cgv__kdjld = get_data(A)
            nzdzk__mnz[idx + 1] = nzdzk__mnz[idx] + n_items
            cgv__kdjld[nzdzk__mnz[idx]:nzdzk__mnz[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(tjdnw__jxjvz, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            kvrfl__qkiml = numba.cpython.unicode._normalize_slice(idx, len(A))
            for rqz__krabd in range(kvrfl__qkiml.start, kvrfl__qkiml.stop,
                kvrfl__qkiml.step):
                A[rqz__krabd] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            nzdzk__mnz = get_offsets(A)
            tjdnw__jxjvz = get_null_bitmap(A)
            biy__clcxi = get_offsets(val)
            yutv__zmn = get_data(val)
            lbpo__fuzc = get_null_bitmap(val)
            lzc__hhjp = len(A)
            kvrfl__qkiml = numba.cpython.unicode._normalize_slice(idx,
                lzc__hhjp)
            mhfr__iejq, zbko__pfqzq = kvrfl__qkiml.start, kvrfl__qkiml.stop
            assert kvrfl__qkiml.step == 1
            if mhfr__iejq == 0:
                nzdzk__mnz[mhfr__iejq] = 0
            atg__tyiz = nzdzk__mnz[mhfr__iejq]
            tqtws__ustw = atg__tyiz + len(yutv__zmn)
            ensure_data_capacity(A, atg__tyiz, tqtws__ustw)
            cgv__kdjld = get_data(A)
            cgv__kdjld[atg__tyiz:atg__tyiz + len(yutv__zmn)] = yutv__zmn
            nzdzk__mnz[mhfr__iejq:zbko__pfqzq + 1] = biy__clcxi + atg__tyiz
            gsqxz__dghc = 0
            for rqz__krabd in range(mhfr__iejq, zbko__pfqzq):
                lhtt__zpp = bodo.libs.int_arr_ext.get_bit_bitmap_arr(lbpo__fuzc
                    , gsqxz__dghc)
                bodo.libs.int_arr_ext.set_bit_to_arr(tjdnw__jxjvz,
                    rqz__krabd, lhtt__zpp)
                gsqxz__dghc += 1
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
