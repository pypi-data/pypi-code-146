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
        ejuv__hkv = [('n_arrays', types.int64), ('data', fe_type.array_type
            .dtype), ('offsets', types.Array(offset_type, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ejuv__hkv)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        ejuv__hkv = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ejuv__hkv)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    lwqe__ezms = builder.module
    cda__jern = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    btakd__wvi = cgutils.get_or_insert_function(lwqe__ezms, cda__jern, name
        ='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not btakd__wvi.is_declaration:
        return btakd__wvi
    btakd__wvi.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(btakd__wvi.append_basic_block())
    obttm__lnjcj = btakd__wvi.args[0]
    mblft__onnzy = context.get_value_type(payload_type).as_pointer()
    per__lksh = builder.bitcast(obttm__lnjcj, mblft__onnzy)
    ravzu__auz = context.make_helper(builder, payload_type, ref=per__lksh)
    context.nrt.decref(builder, array_item_type.dtype, ravzu__auz.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        ravzu__auz.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        ravzu__auz.null_bitmap)
    builder.ret_void()
    return btakd__wvi


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    lhrd__otylj = context.get_value_type(payload_type)
    cwrqt__lop = context.get_abi_sizeof(lhrd__otylj)
    ulu__jksbi = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    jrm__rdi = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, cwrqt__lop), ulu__jksbi)
    hsa__tads = context.nrt.meminfo_data(builder, jrm__rdi)
    laax__pyn = builder.bitcast(hsa__tads, lhrd__otylj.as_pointer())
    ravzu__auz = cgutils.create_struct_proxy(payload_type)(context, builder)
    ravzu__auz.n_arrays = n_arrays
    vxwn__lgze = n_elems.type.count
    lxrxd__dqn = builder.extract_value(n_elems, 0)
    zzq__glcu = cgutils.alloca_once_value(builder, lxrxd__dqn)
    qrg__dazxv = builder.icmp_signed('==', lxrxd__dqn, lir.Constant(
        lxrxd__dqn.type, -1))
    with builder.if_then(qrg__dazxv):
        builder.store(n_arrays, zzq__glcu)
    n_elems = cgutils.pack_array(builder, [builder.load(zzq__glcu)] + [
        builder.extract_value(n_elems, ebtjm__uzwyu) for ebtjm__uzwyu in
        range(1, vxwn__lgze)])
    ravzu__auz.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    xtjwo__emcdz = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    bka__abcbz = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [xtjwo__emcdz])
    offsets_ptr = bka__abcbz.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    ravzu__auz.offsets = bka__abcbz._getvalue()
    ypi__omzdb = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    xdxh__iqz = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [ypi__omzdb])
    null_bitmap_ptr = xdxh__iqz.data
    ravzu__auz.null_bitmap = xdxh__iqz._getvalue()
    builder.store(ravzu__auz._getvalue(), laax__pyn)
    return jrm__rdi, ravzu__auz.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    kupzi__vbel, ririt__vbpgj = c.pyapi.call_jit_code(copy_data, sig, [
        data_arr, item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    dnfig__murzq = context.insert_const_string(builder.module, 'pandas')
    uzha__uqt = c.pyapi.import_module_noblock(dnfig__murzq)
    fav__olcz = c.pyapi.object_getattr_string(uzha__uqt, 'NA')
    ogyzo__fajc = c.context.get_constant(offset_type, 0)
    builder.store(ogyzo__fajc, offsets_ptr)
    fzfc__sbu = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as vbt__gjoj:
        fltb__odq = vbt__gjoj.index
        item_ind = builder.load(fzfc__sbu)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [fltb__odq]))
        arr_obj = seq_getitem(builder, context, val, fltb__odq)
        set_bitmap_bit(builder, null_bitmap_ptr, fltb__odq, 0)
        nnz__gcup = is_na_value(builder, context, arr_obj, fav__olcz)
        cvcz__dul = builder.icmp_unsigned('!=', nnz__gcup, lir.Constant(
            nnz__gcup.type, 1))
        with builder.if_then(cvcz__dul):
            set_bitmap_bit(builder, null_bitmap_ptr, fltb__odq, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), fzfc__sbu)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(fzfc__sbu), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(uzha__uqt)
    c.pyapi.decref(fav__olcz)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    kxxq__fybqx = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if kxxq__fybqx:
        cda__jern = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        rat__tuget = cgutils.get_or_insert_function(c.builder.module,
            cda__jern, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(rat__tuget,
            [val])])
    else:
        rigf__cbjv = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            rigf__cbjv, ebtjm__uzwyu) for ebtjm__uzwyu in range(1,
            rigf__cbjv.type.count)])
    jrm__rdi, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if kxxq__fybqx:
        tuhp__dkpuv = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ofuge__fuiuv = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        cda__jern = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        btakd__wvi = cgutils.get_or_insert_function(c.builder.module,
            cda__jern, name='array_item_array_from_sequence')
        c.builder.call(btakd__wvi, [val, c.builder.bitcast(ofuge__fuiuv,
            lir.IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir
            .Constant(lir.IntType(32), tuhp__dkpuv)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    gbddf__xqje = c.context.make_helper(c.builder, typ)
    gbddf__xqje.meminfo = jrm__rdi
    gqn__ztyww = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gbddf__xqje._getvalue(), is_error=gqn__ztyww)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    gbddf__xqje = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    hsa__tads = context.nrt.meminfo_data(builder, gbddf__xqje.meminfo)
    laax__pyn = builder.bitcast(hsa__tads, context.get_value_type(
        payload_type).as_pointer())
    ravzu__auz = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(laax__pyn))
    return ravzu__auz


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    dnfig__murzq = context.insert_const_string(builder.module, 'numpy')
    opfs__ilfk = c.pyapi.import_module_noblock(dnfig__murzq)
    gcvwv__qgx = c.pyapi.object_getattr_string(opfs__ilfk, 'object_')
    cwnwo__qlnsa = c.pyapi.long_from_longlong(n_arrays)
    yovu__jfmqh = c.pyapi.call_method(opfs__ilfk, 'ndarray', (cwnwo__qlnsa,
        gcvwv__qgx))
    lycs__ageda = c.pyapi.object_getattr_string(opfs__ilfk, 'nan')
    fzfc__sbu = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_arrays) as vbt__gjoj:
        fltb__odq = vbt__gjoj.index
        pyarray_setitem(builder, context, yovu__jfmqh, fltb__odq, lycs__ageda)
        uqx__dqzs = get_bitmap_bit(builder, null_bitmap_ptr, fltb__odq)
        fwlw__mmea = builder.icmp_unsigned('!=', uqx__dqzs, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(fwlw__mmea):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(fltb__odq, lir.Constant(fltb__odq
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                fltb__odq]))), lir.IntType(64))
            item_ind = builder.load(fzfc__sbu)
            kupzi__vbel, glgyc__mgs = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), fzfc__sbu)
            arr_obj = c.pyapi.from_native_value(typ.dtype, glgyc__mgs, c.
                env_manager)
            pyarray_setitem(builder, context, yovu__jfmqh, fltb__odq, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(opfs__ilfk)
    c.pyapi.decref(gcvwv__qgx)
    c.pyapi.decref(cwnwo__qlnsa)
    c.pyapi.decref(lycs__ageda)
    return yovu__jfmqh


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    ravzu__auz = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = ravzu__auz.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), ravzu__auz.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), ravzu__auz.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        tuhp__dkpuv = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ofuge__fuiuv = c.context.make_helper(c.builder, typ.dtype, data_arr
            ).data
        cda__jern = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        cyl__vgl = cgutils.get_or_insert_function(c.builder.module,
            cda__jern, name='np_array_from_array_item_array')
        arr = c.builder.call(cyl__vgl, [ravzu__auz.n_arrays, c.builder.
            bitcast(ofuge__fuiuv, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), tuhp__dkpuv)])
    else:
        arr = _box_array_item_array_generic(typ, c, ravzu__auz.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    oqoih__lby, qht__bsf, arnpf__kjt = args
    valp__siw = bodo.utils.transform.get_type_alloc_counts(array_item_type.
        dtype)
    ugoab__uaxc = sig.args[1]
    if not isinstance(ugoab__uaxc, types.UniTuple):
        qht__bsf = cgutils.pack_array(builder, [lir.Constant(lir.IntType(64
            ), -1) for arnpf__kjt in range(valp__siw)])
    elif ugoab__uaxc.count < valp__siw:
        qht__bsf = cgutils.pack_array(builder, [builder.extract_value(
            qht__bsf, ebtjm__uzwyu) for ebtjm__uzwyu in range(ugoab__uaxc.
            count)] + [lir.Constant(lir.IntType(64), -1) for arnpf__kjt in
            range(valp__siw - ugoab__uaxc.count)])
    jrm__rdi, arnpf__kjt, arnpf__kjt, arnpf__kjt = construct_array_item_array(
        context, builder, array_item_type, oqoih__lby, qht__bsf)
    gbddf__xqje = context.make_helper(builder, array_item_type)
    gbddf__xqje.meminfo = jrm__rdi
    return gbddf__xqje._getvalue()


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
    n_arrays, tgsf__bmrs, bka__abcbz, xdxh__iqz = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    lhrd__otylj = context.get_value_type(payload_type)
    cwrqt__lop = context.get_abi_sizeof(lhrd__otylj)
    ulu__jksbi = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    jrm__rdi = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, cwrqt__lop), ulu__jksbi)
    hsa__tads = context.nrt.meminfo_data(builder, jrm__rdi)
    laax__pyn = builder.bitcast(hsa__tads, lhrd__otylj.as_pointer())
    ravzu__auz = cgutils.create_struct_proxy(payload_type)(context, builder)
    ravzu__auz.n_arrays = n_arrays
    ravzu__auz.data = tgsf__bmrs
    ravzu__auz.offsets = bka__abcbz
    ravzu__auz.null_bitmap = xdxh__iqz
    builder.store(ravzu__auz._getvalue(), laax__pyn)
    context.nrt.incref(builder, signature.args[1], tgsf__bmrs)
    context.nrt.incref(builder, signature.args[2], bka__abcbz)
    context.nrt.incref(builder, signature.args[3], xdxh__iqz)
    gbddf__xqje = context.make_helper(builder, array_item_type)
    gbddf__xqje.meminfo = jrm__rdi
    return gbddf__xqje._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    dnd__jkads = ArrayItemArrayType(data_type)
    sig = dnd__jkads(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ravzu__auz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            ravzu__auz.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        ravzu__auz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        ofuge__fuiuv = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, ravzu__auz.offsets).data
        bka__abcbz = builder.bitcast(ofuge__fuiuv, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(bka__abcbz, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ravzu__auz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            ravzu__auz.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ravzu__auz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            ravzu__auz.null_bitmap)
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
        ravzu__auz = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return ravzu__auz.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, yuh__bzjl = args
        gbddf__xqje = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        hsa__tads = context.nrt.meminfo_data(builder, gbddf__xqje.meminfo)
        laax__pyn = builder.bitcast(hsa__tads, context.get_value_type(
            payload_type).as_pointer())
        ravzu__auz = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(laax__pyn))
        context.nrt.decref(builder, data_typ, ravzu__auz.data)
        ravzu__auz.data = yuh__bzjl
        context.nrt.incref(builder, data_typ, yuh__bzjl)
        builder.store(ravzu__auz._getvalue(), laax__pyn)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    tgsf__bmrs = get_data(arr)
    jct__asuez = len(tgsf__bmrs)
    if jct__asuez < new_size:
        mao__gwzjn = max(2 * jct__asuez, new_size)
        yuh__bzjl = bodo.libs.array_kernels.resize_and_copy(tgsf__bmrs,
            old_size, mao__gwzjn)
        replace_data_arr(arr, yuh__bzjl)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    tgsf__bmrs = get_data(arr)
    bka__abcbz = get_offsets(arr)
    hnah__kynr = len(tgsf__bmrs)
    ebtq__xyvbo = bka__abcbz[-1]
    if hnah__kynr != ebtq__xyvbo:
        yuh__bzjl = bodo.libs.array_kernels.resize_and_copy(tgsf__bmrs,
            ebtq__xyvbo, ebtq__xyvbo)
        replace_data_arr(arr, yuh__bzjl)


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
            bka__abcbz = get_offsets(arr)
            tgsf__bmrs = get_data(arr)
            hlyds__dfbyc = bka__abcbz[ind]
            rfwn__uqyq = bka__abcbz[ind + 1]
            return tgsf__bmrs[hlyds__dfbyc:rfwn__uqyq]
        return array_item_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:
        ypmw__rqmv = arr.dtype

        def impl_bool(arr, ind):
            vkvdx__gme = len(arr)
            if vkvdx__gme != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            xdxh__iqz = get_null_bitmap(arr)
            n_arrays = 0
            ceci__lueay = init_nested_counts(ypmw__rqmv)
            for ebtjm__uzwyu in range(vkvdx__gme):
                if ind[ebtjm__uzwyu]:
                    n_arrays += 1
                    bjnbl__hwtt = arr[ebtjm__uzwyu]
                    ceci__lueay = add_nested_counts(ceci__lueay, bjnbl__hwtt)
            yovu__jfmqh = pre_alloc_array_item_array(n_arrays, ceci__lueay,
                ypmw__rqmv)
            enayb__qetux = get_null_bitmap(yovu__jfmqh)
            ijcgo__bmofz = 0
            for lax__ginii in range(vkvdx__gme):
                if ind[lax__ginii]:
                    yovu__jfmqh[ijcgo__bmofz] = arr[lax__ginii]
                    uahm__tsd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        xdxh__iqz, lax__ginii)
                    bodo.libs.int_arr_ext.set_bit_to_arr(enayb__qetux,
                        ijcgo__bmofz, uahm__tsd)
                    ijcgo__bmofz += 1
            return yovu__jfmqh
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        ypmw__rqmv = arr.dtype

        def impl_int(arr, ind):
            xdxh__iqz = get_null_bitmap(arr)
            vkvdx__gme = len(ind)
            n_arrays = vkvdx__gme
            ceci__lueay = init_nested_counts(ypmw__rqmv)
            for iibaq__gqp in range(vkvdx__gme):
                ebtjm__uzwyu = ind[iibaq__gqp]
                bjnbl__hwtt = arr[ebtjm__uzwyu]
                ceci__lueay = add_nested_counts(ceci__lueay, bjnbl__hwtt)
            yovu__jfmqh = pre_alloc_array_item_array(n_arrays, ceci__lueay,
                ypmw__rqmv)
            enayb__qetux = get_null_bitmap(yovu__jfmqh)
            for dyzf__sxula in range(vkvdx__gme):
                lax__ginii = ind[dyzf__sxula]
                yovu__jfmqh[dyzf__sxula] = arr[lax__ginii]
                uahm__tsd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(xdxh__iqz,
                    lax__ginii)
                bodo.libs.int_arr_ext.set_bit_to_arr(enayb__qetux,
                    dyzf__sxula, uahm__tsd)
            return yovu__jfmqh
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            vkvdx__gme = len(arr)
            rzh__akkkr = numba.cpython.unicode._normalize_slice(ind, vkvdx__gme
                )
            iyqqd__vmu = np.arange(rzh__akkkr.start, rzh__akkkr.stop,
                rzh__akkkr.step)
            return arr[iyqqd__vmu]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            bka__abcbz = get_offsets(A)
            xdxh__iqz = get_null_bitmap(A)
            if idx == 0:
                bka__abcbz[0] = 0
            n_items = len(val)
            vyyf__fnon = bka__abcbz[idx] + n_items
            ensure_data_capacity(A, bka__abcbz[idx], vyyf__fnon)
            tgsf__bmrs = get_data(A)
            bka__abcbz[idx + 1] = bka__abcbz[idx] + n_items
            tgsf__bmrs[bka__abcbz[idx]:bka__abcbz[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(xdxh__iqz, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            rzh__akkkr = numba.cpython.unicode._normalize_slice(idx, len(A))
            for ebtjm__uzwyu in range(rzh__akkkr.start, rzh__akkkr.stop,
                rzh__akkkr.step):
                A[ebtjm__uzwyu] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            bka__abcbz = get_offsets(A)
            xdxh__iqz = get_null_bitmap(A)
            epnw__fwzv = get_offsets(val)
            ytaq__vooeg = get_data(val)
            srjr__bfogy = get_null_bitmap(val)
            vkvdx__gme = len(A)
            rzh__akkkr = numba.cpython.unicode._normalize_slice(idx, vkvdx__gme
                )
            ywk__tdsa, alfhw__mki = rzh__akkkr.start, rzh__akkkr.stop
            assert rzh__akkkr.step == 1
            if ywk__tdsa == 0:
                bka__abcbz[ywk__tdsa] = 0
            ukd__nam = bka__abcbz[ywk__tdsa]
            vyyf__fnon = ukd__nam + len(ytaq__vooeg)
            ensure_data_capacity(A, ukd__nam, vyyf__fnon)
            tgsf__bmrs = get_data(A)
            tgsf__bmrs[ukd__nam:ukd__nam + len(ytaq__vooeg)] = ytaq__vooeg
            bka__abcbz[ywk__tdsa:alfhw__mki + 1] = epnw__fwzv + ukd__nam
            daf__jlb = 0
            for ebtjm__uzwyu in range(ywk__tdsa, alfhw__mki):
                uahm__tsd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    srjr__bfogy, daf__jlb)
                bodo.libs.int_arr_ext.set_bit_to_arr(xdxh__iqz,
                    ebtjm__uzwyu, uahm__tsd)
                daf__jlb += 1
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
