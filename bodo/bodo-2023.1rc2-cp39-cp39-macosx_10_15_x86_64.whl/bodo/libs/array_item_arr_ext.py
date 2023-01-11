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
        yvfi__mkwas = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, yvfi__mkwas)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        yvfi__mkwas = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, yvfi__mkwas)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    njbr__zwbrv = builder.module
    vekzi__zna = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    rfu__bow = cgutils.get_or_insert_function(njbr__zwbrv, vekzi__zna, name
        ='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not rfu__bow.is_declaration:
        return rfu__bow
    rfu__bow.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(rfu__bow.append_basic_block())
    mbk__nqczr = rfu__bow.args[0]
    vyvx__npuzb = context.get_value_type(payload_type).as_pointer()
    vkvw__mhdag = builder.bitcast(mbk__nqczr, vyvx__npuzb)
    kfmwv__bzx = context.make_helper(builder, payload_type, ref=vkvw__mhdag)
    context.nrt.decref(builder, array_item_type.dtype, kfmwv__bzx.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        kfmwv__bzx.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        kfmwv__bzx.null_bitmap)
    builder.ret_void()
    return rfu__bow


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    qrsu__ill = context.get_value_type(payload_type)
    asnv__kgmmy = context.get_abi_sizeof(qrsu__ill)
    lqklt__iys = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    sfi__uzj = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, asnv__kgmmy), lqklt__iys)
    tcto__pxkd = context.nrt.meminfo_data(builder, sfi__uzj)
    kbsj__ctgi = builder.bitcast(tcto__pxkd, qrsu__ill.as_pointer())
    kfmwv__bzx = cgutils.create_struct_proxy(payload_type)(context, builder)
    kfmwv__bzx.n_arrays = n_arrays
    oii__untxf = n_elems.type.count
    ptyt__qzg = builder.extract_value(n_elems, 0)
    lwhw__flw = cgutils.alloca_once_value(builder, ptyt__qzg)
    rnb__ztkm = builder.icmp_signed('==', ptyt__qzg, lir.Constant(ptyt__qzg
        .type, -1))
    with builder.if_then(rnb__ztkm):
        builder.store(n_arrays, lwhw__flw)
    n_elems = cgutils.pack_array(builder, [builder.load(lwhw__flw)] + [
        builder.extract_value(n_elems, smxy__uxayn) for smxy__uxayn in
        range(1, oii__untxf)])
    kfmwv__bzx.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    xojt__hpixr = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    vpdhk__yagrb = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [xojt__hpixr])
    offsets_ptr = vpdhk__yagrb.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    kfmwv__bzx.offsets = vpdhk__yagrb._getvalue()
    kvqly__pivhu = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    sjrbg__bkub = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [kvqly__pivhu])
    null_bitmap_ptr = sjrbg__bkub.data
    kfmwv__bzx.null_bitmap = sjrbg__bkub._getvalue()
    builder.store(kfmwv__bzx._getvalue(), kbsj__ctgi)
    return sfi__uzj, kfmwv__bzx.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    vozz__jie, owb__fzf = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    cvmi__skn = context.insert_const_string(builder.module, 'pandas')
    zne__nki = c.pyapi.import_module_noblock(cvmi__skn)
    ybeti__jly = c.pyapi.object_getattr_string(zne__nki, 'NA')
    mmox__mfwzx = c.context.get_constant(offset_type, 0)
    builder.store(mmox__mfwzx, offsets_ptr)
    mdu__zpjtn = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as wgdv__bklw:
        fcv__zzcs = wgdv__bklw.index
        item_ind = builder.load(mdu__zpjtn)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [fcv__zzcs]))
        arr_obj = seq_getitem(builder, context, val, fcv__zzcs)
        set_bitmap_bit(builder, null_bitmap_ptr, fcv__zzcs, 0)
        kspmk__hyjg = is_na_value(builder, context, arr_obj, ybeti__jly)
        dxp__ncm = builder.icmp_unsigned('!=', kspmk__hyjg, lir.Constant(
            kspmk__hyjg.type, 1))
        with builder.if_then(dxp__ncm):
            set_bitmap_bit(builder, null_bitmap_ptr, fcv__zzcs, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), mdu__zpjtn)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(mdu__zpjtn), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(zne__nki)
    c.pyapi.decref(ybeti__jly)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    mqu__upj = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if mqu__upj:
        vekzi__zna = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        vjvs__oir = cgutils.get_or_insert_function(c.builder.module,
            vekzi__zna, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(vjvs__oir,
            [val])])
    else:
        dgyw__jxocu = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            dgyw__jxocu, smxy__uxayn) for smxy__uxayn in range(1,
            dgyw__jxocu.type.count)])
    sfi__uzj, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if mqu__upj:
        nsc__shewc = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        erd__uaxg = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        vekzi__zna = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        rfu__bow = cgutils.get_or_insert_function(c.builder.module,
            vekzi__zna, name='array_item_array_from_sequence')
        c.builder.call(rfu__bow, [val, c.builder.bitcast(erd__uaxg, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), nsc__shewc)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    gsj__tqmi = c.context.make_helper(c.builder, typ)
    gsj__tqmi.meminfo = sfi__uzj
    nxz__los = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gsj__tqmi._getvalue(), is_error=nxz__los)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    gsj__tqmi = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    tcto__pxkd = context.nrt.meminfo_data(builder, gsj__tqmi.meminfo)
    kbsj__ctgi = builder.bitcast(tcto__pxkd, context.get_value_type(
        payload_type).as_pointer())
    kfmwv__bzx = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(kbsj__ctgi))
    return kfmwv__bzx


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    cvmi__skn = context.insert_const_string(builder.module, 'numpy')
    hxznm__qho = c.pyapi.import_module_noblock(cvmi__skn)
    rxfed__emyu = c.pyapi.object_getattr_string(hxznm__qho, 'object_')
    kygmo__tul = c.pyapi.long_from_longlong(n_arrays)
    hcwiw__wxsxz = c.pyapi.call_method(hxznm__qho, 'ndarray', (kygmo__tul,
        rxfed__emyu))
    kmf__mzpdc = c.pyapi.object_getattr_string(hxznm__qho, 'nan')
    mdu__zpjtn = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as wgdv__bklw:
        fcv__zzcs = wgdv__bklw.index
        pyarray_setitem(builder, context, hcwiw__wxsxz, fcv__zzcs, kmf__mzpdc)
        ceqkf__kltu = get_bitmap_bit(builder, null_bitmap_ptr, fcv__zzcs)
        eveja__mbp = builder.icmp_unsigned('!=', ceqkf__kltu, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(eveja__mbp):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(fcv__zzcs, lir.Constant(fcv__zzcs
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                fcv__zzcs]))), lir.IntType(64))
            item_ind = builder.load(mdu__zpjtn)
            vozz__jie, ogdn__ftj = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), mdu__zpjtn)
            arr_obj = c.pyapi.from_native_value(typ.dtype, ogdn__ftj, c.
                env_manager)
            pyarray_setitem(builder, context, hcwiw__wxsxz, fcv__zzcs, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(hxznm__qho)
    c.pyapi.decref(rxfed__emyu)
    c.pyapi.decref(kygmo__tul)
    c.pyapi.decref(kmf__mzpdc)
    return hcwiw__wxsxz


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    kfmwv__bzx = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = kfmwv__bzx.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), kfmwv__bzx.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), kfmwv__bzx.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        nsc__shewc = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        erd__uaxg = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        vekzi__zna = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        mzn__kvst = cgutils.get_or_insert_function(c.builder.module,
            vekzi__zna, name='np_array_from_array_item_array')
        arr = c.builder.call(mzn__kvst, [kfmwv__bzx.n_arrays, c.builder.
            bitcast(erd__uaxg, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), nsc__shewc)])
    else:
        arr = _box_array_item_array_generic(typ, c, kfmwv__bzx.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    pbxvd__sil, kogur__qtq, dnhlk__zqqfu = args
    eml__sdg = bodo.utils.transform.get_type_alloc_counts(array_item_type.dtype
        )
    iris__pnud = sig.args[1]
    if not isinstance(iris__pnud, types.UniTuple):
        kogur__qtq = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for dnhlk__zqqfu in range(eml__sdg)])
    elif iris__pnud.count < eml__sdg:
        kogur__qtq = cgutils.pack_array(builder, [builder.extract_value(
            kogur__qtq, smxy__uxayn) for smxy__uxayn in range(iris__pnud.
            count)] + [lir.Constant(lir.IntType(64), -1) for dnhlk__zqqfu in
            range(eml__sdg - iris__pnud.count)])
    sfi__uzj, dnhlk__zqqfu, dnhlk__zqqfu, dnhlk__zqqfu = (
        construct_array_item_array(context, builder, array_item_type,
        pbxvd__sil, kogur__qtq))
    gsj__tqmi = context.make_helper(builder, array_item_type)
    gsj__tqmi.meminfo = sfi__uzj
    return gsj__tqmi._getvalue()


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
    n_arrays, yyuq__pcbza, vpdhk__yagrb, sjrbg__bkub = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    qrsu__ill = context.get_value_type(payload_type)
    asnv__kgmmy = context.get_abi_sizeof(qrsu__ill)
    lqklt__iys = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    sfi__uzj = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, asnv__kgmmy), lqklt__iys)
    tcto__pxkd = context.nrt.meminfo_data(builder, sfi__uzj)
    kbsj__ctgi = builder.bitcast(tcto__pxkd, qrsu__ill.as_pointer())
    kfmwv__bzx = cgutils.create_struct_proxy(payload_type)(context, builder)
    kfmwv__bzx.n_arrays = n_arrays
    kfmwv__bzx.data = yyuq__pcbza
    kfmwv__bzx.offsets = vpdhk__yagrb
    kfmwv__bzx.null_bitmap = sjrbg__bkub
    builder.store(kfmwv__bzx._getvalue(), kbsj__ctgi)
    context.nrt.incref(builder, signature.args[1], yyuq__pcbza)
    context.nrt.incref(builder, signature.args[2], vpdhk__yagrb)
    context.nrt.incref(builder, signature.args[3], sjrbg__bkub)
    gsj__tqmi = context.make_helper(builder, array_item_type)
    gsj__tqmi.meminfo = sfi__uzj
    return gsj__tqmi._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    atpd__mgoz = ArrayItemArrayType(data_type)
    sig = atpd__mgoz(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        kfmwv__bzx = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            kfmwv__bzx.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        kfmwv__bzx = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        erd__uaxg = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, kfmwv__bzx.offsets).data
        vpdhk__yagrb = builder.bitcast(erd__uaxg, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(vpdhk__yagrb, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        kfmwv__bzx = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            kfmwv__bzx.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        kfmwv__bzx = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            kfmwv__bzx.null_bitmap)
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
        kfmwv__bzx = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return kfmwv__bzx.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, ket__uauz = args
        gsj__tqmi = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        tcto__pxkd = context.nrt.meminfo_data(builder, gsj__tqmi.meminfo)
        kbsj__ctgi = builder.bitcast(tcto__pxkd, context.get_value_type(
            payload_type).as_pointer())
        kfmwv__bzx = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(kbsj__ctgi))
        context.nrt.decref(builder, data_typ, kfmwv__bzx.data)
        kfmwv__bzx.data = ket__uauz
        context.nrt.incref(builder, data_typ, ket__uauz)
        builder.store(kfmwv__bzx._getvalue(), kbsj__ctgi)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    yyuq__pcbza = get_data(arr)
    nkwso__shky = len(yyuq__pcbza)
    if nkwso__shky < new_size:
        smw__ulhqz = max(2 * nkwso__shky, new_size)
        ket__uauz = bodo.libs.array_kernels.resize_and_copy(yyuq__pcbza,
            old_size, smw__ulhqz)
        replace_data_arr(arr, ket__uauz)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    yyuq__pcbza = get_data(arr)
    vpdhk__yagrb = get_offsets(arr)
    uylbj__bpplf = len(yyuq__pcbza)
    hgqxk__svfx = vpdhk__yagrb[-1]
    if uylbj__bpplf != hgqxk__svfx:
        ket__uauz = bodo.libs.array_kernels.resize_and_copy(yyuq__pcbza,
            hgqxk__svfx, hgqxk__svfx)
        replace_data_arr(arr, ket__uauz)


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
            vpdhk__yagrb = get_offsets(arr)
            yyuq__pcbza = get_data(arr)
            rsbu__vhtz = vpdhk__yagrb[ind]
            unm__tnfx = vpdhk__yagrb[ind + 1]
            return yyuq__pcbza[rsbu__vhtz:unm__tnfx]
        return array_item_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:
        xlqj__nrh = arr.dtype

        def impl_bool(arr, ind):
            req__eczn = len(arr)
            if req__eczn != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            sjrbg__bkub = get_null_bitmap(arr)
            n_arrays = 0
            yipha__gcd = init_nested_counts(xlqj__nrh)
            for smxy__uxayn in range(req__eczn):
                if ind[smxy__uxayn]:
                    n_arrays += 1
                    kvfiu__ollxo = arr[smxy__uxayn]
                    yipha__gcd = add_nested_counts(yipha__gcd, kvfiu__ollxo)
            hcwiw__wxsxz = pre_alloc_array_item_array(n_arrays, yipha__gcd,
                xlqj__nrh)
            mkzg__jgizs = get_null_bitmap(hcwiw__wxsxz)
            qxsj__wesl = 0
            for gzttz__snf in range(req__eczn):
                if ind[gzttz__snf]:
                    hcwiw__wxsxz[qxsj__wesl] = arr[gzttz__snf]
                    azkk__aew = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        sjrbg__bkub, gzttz__snf)
                    bodo.libs.int_arr_ext.set_bit_to_arr(mkzg__jgizs,
                        qxsj__wesl, azkk__aew)
                    qxsj__wesl += 1
            return hcwiw__wxsxz
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        xlqj__nrh = arr.dtype

        def impl_int(arr, ind):
            sjrbg__bkub = get_null_bitmap(arr)
            req__eczn = len(ind)
            n_arrays = req__eczn
            yipha__gcd = init_nested_counts(xlqj__nrh)
            for mxowo__vqmty in range(req__eczn):
                smxy__uxayn = ind[mxowo__vqmty]
                kvfiu__ollxo = arr[smxy__uxayn]
                yipha__gcd = add_nested_counts(yipha__gcd, kvfiu__ollxo)
            hcwiw__wxsxz = pre_alloc_array_item_array(n_arrays, yipha__gcd,
                xlqj__nrh)
            mkzg__jgizs = get_null_bitmap(hcwiw__wxsxz)
            for nehft__aynkk in range(req__eczn):
                gzttz__snf = ind[nehft__aynkk]
                hcwiw__wxsxz[nehft__aynkk] = arr[gzttz__snf]
                azkk__aew = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    sjrbg__bkub, gzttz__snf)
                bodo.libs.int_arr_ext.set_bit_to_arr(mkzg__jgizs,
                    nehft__aynkk, azkk__aew)
            return hcwiw__wxsxz
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            req__eczn = len(arr)
            igs__vlm = numba.cpython.unicode._normalize_slice(ind, req__eczn)
            ipw__rcnv = np.arange(igs__vlm.start, igs__vlm.stop, igs__vlm.step)
            return arr[ipw__rcnv]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            vpdhk__yagrb = get_offsets(A)
            sjrbg__bkub = get_null_bitmap(A)
            if idx == 0:
                vpdhk__yagrb[0] = 0
            n_items = len(val)
            cucbp__yhun = vpdhk__yagrb[idx] + n_items
            ensure_data_capacity(A, vpdhk__yagrb[idx], cucbp__yhun)
            yyuq__pcbza = get_data(A)
            vpdhk__yagrb[idx + 1] = vpdhk__yagrb[idx] + n_items
            yyuq__pcbza[vpdhk__yagrb[idx]:vpdhk__yagrb[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(sjrbg__bkub, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            igs__vlm = numba.cpython.unicode._normalize_slice(idx, len(A))
            for smxy__uxayn in range(igs__vlm.start, igs__vlm.stop,
                igs__vlm.step):
                A[smxy__uxayn] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            vpdhk__yagrb = get_offsets(A)
            sjrbg__bkub = get_null_bitmap(A)
            ssnm__ueua = get_offsets(val)
            fngi__svwv = get_data(val)
            zapua__cowa = get_null_bitmap(val)
            req__eczn = len(A)
            igs__vlm = numba.cpython.unicode._normalize_slice(idx, req__eczn)
            wlqpo__ijr, ljac__pclxi = igs__vlm.start, igs__vlm.stop
            assert igs__vlm.step == 1
            if wlqpo__ijr == 0:
                vpdhk__yagrb[wlqpo__ijr] = 0
            pbvv__nbioh = vpdhk__yagrb[wlqpo__ijr]
            cucbp__yhun = pbvv__nbioh + len(fngi__svwv)
            ensure_data_capacity(A, pbvv__nbioh, cucbp__yhun)
            yyuq__pcbza = get_data(A)
            yyuq__pcbza[pbvv__nbioh:pbvv__nbioh + len(fngi__svwv)] = fngi__svwv
            vpdhk__yagrb[wlqpo__ijr:ljac__pclxi + 1] = ssnm__ueua + pbvv__nbioh
            liy__ntwon = 0
            for smxy__uxayn in range(wlqpo__ijr, ljac__pclxi):
                azkk__aew = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    zapua__cowa, liy__ntwon)
                bodo.libs.int_arr_ext.set_bit_to_arr(sjrbg__bkub,
                    smxy__uxayn, azkk__aew)
                liy__ntwon += 1
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
