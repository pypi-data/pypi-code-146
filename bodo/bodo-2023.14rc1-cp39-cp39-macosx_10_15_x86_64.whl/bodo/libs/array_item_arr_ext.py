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
        yudeu__wasy = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, yudeu__wasy)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        yudeu__wasy = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, yudeu__wasy)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    afdm__rpxm = builder.module
    gqyvl__fvxls = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    hzpl__nbry = cgutils.get_or_insert_function(afdm__rpxm, gqyvl__fvxls,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not hzpl__nbry.is_declaration:
        return hzpl__nbry
    hzpl__nbry.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(hzpl__nbry.append_basic_block())
    fcjn__zcfkd = hzpl__nbry.args[0]
    lqb__coidc = context.get_value_type(payload_type).as_pointer()
    koxa__czk = builder.bitcast(fcjn__zcfkd, lqb__coidc)
    tew__nbdz = context.make_helper(builder, payload_type, ref=koxa__czk)
    context.nrt.decref(builder, array_item_type.dtype, tew__nbdz.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), tew__nbdz
        .offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), tew__nbdz
        .null_bitmap)
    builder.ret_void()
    return hzpl__nbry


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    epvcc__noeay = context.get_value_type(payload_type)
    tywjb__gdf = context.get_abi_sizeof(epvcc__noeay)
    fekr__nubjz = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    zlr__xrq = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, tywjb__gdf), fekr__nubjz)
    ilkdu__pfc = context.nrt.meminfo_data(builder, zlr__xrq)
    yxmv__ksyoi = builder.bitcast(ilkdu__pfc, epvcc__noeay.as_pointer())
    tew__nbdz = cgutils.create_struct_proxy(payload_type)(context, builder)
    tew__nbdz.n_arrays = n_arrays
    ocago__cogl = n_elems.type.count
    ymlk__fmvhr = builder.extract_value(n_elems, 0)
    qrooc__nll = cgutils.alloca_once_value(builder, ymlk__fmvhr)
    ped__vce = builder.icmp_signed('==', ymlk__fmvhr, lir.Constant(
        ymlk__fmvhr.type, -1))
    with builder.if_then(ped__vce):
        builder.store(n_arrays, qrooc__nll)
    n_elems = cgutils.pack_array(builder, [builder.load(qrooc__nll)] + [
        builder.extract_value(n_elems, bnqu__zhqua) for bnqu__zhqua in
        range(1, ocago__cogl)])
    tew__nbdz.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    huwjv__kzjp = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    jwv__vhs = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [huwjv__kzjp])
    offsets_ptr = jwv__vhs.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    tew__nbdz.offsets = jwv__vhs._getvalue()
    cab__rag = builder.udiv(builder.add(n_arrays, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    trnax__uygm = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [cab__rag])
    null_bitmap_ptr = trnax__uygm.data
    tew__nbdz.null_bitmap = trnax__uygm._getvalue()
    builder.store(tew__nbdz._getvalue(), yxmv__ksyoi)
    return zlr__xrq, tew__nbdz.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    sxd__vxjh, psv__wxiq = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    ilpi__rfzq = context.insert_const_string(builder.module, 'pandas')
    ltqdb__jmul = c.pyapi.import_module_noblock(ilpi__rfzq)
    hkeky__cpb = c.pyapi.object_getattr_string(ltqdb__jmul, 'NA')
    siwzi__wwc = c.context.get_constant(offset_type, 0)
    builder.store(siwzi__wwc, offsets_ptr)
    jdf__hav = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as xpfey__zym:
        gqfg__jryq = xpfey__zym.index
        item_ind = builder.load(jdf__hav)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [gqfg__jryq]))
        arr_obj = seq_getitem(builder, context, val, gqfg__jryq)
        set_bitmap_bit(builder, null_bitmap_ptr, gqfg__jryq, 0)
        zhqk__hhxz = is_na_value(builder, context, arr_obj, hkeky__cpb)
        oijrx__czchd = builder.icmp_unsigned('!=', zhqk__hhxz, lir.Constant
            (zhqk__hhxz.type, 1))
        with builder.if_then(oijrx__czchd):
            set_bitmap_bit(builder, null_bitmap_ptr, gqfg__jryq, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), jdf__hav)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(jdf__hav), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(ltqdb__jmul)
    c.pyapi.decref(hkeky__cpb)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    gnzx__yjrk = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if gnzx__yjrk:
        gqyvl__fvxls = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        qnvuw__yrd = cgutils.get_or_insert_function(c.builder.module,
            gqyvl__fvxls, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(qnvuw__yrd,
            [val])])
    else:
        tqhp__lgjn = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            tqhp__lgjn, bnqu__zhqua) for bnqu__zhqua in range(1, tqhp__lgjn
            .type.count)])
    zlr__xrq, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if gnzx__yjrk:
        nkg__wnwi = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ildqj__qkab = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        gqyvl__fvxls = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        hzpl__nbry = cgutils.get_or_insert_function(c.builder.module,
            gqyvl__fvxls, name='array_item_array_from_sequence')
        c.builder.call(hzpl__nbry, [val, c.builder.bitcast(ildqj__qkab, lir
            .IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), nkg__wnwi)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    bmlo__obla = c.context.make_helper(c.builder, typ)
    bmlo__obla.meminfo = zlr__xrq
    cqm__lpplq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bmlo__obla._getvalue(), is_error=cqm__lpplq)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    bmlo__obla = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    ilkdu__pfc = context.nrt.meminfo_data(builder, bmlo__obla.meminfo)
    yxmv__ksyoi = builder.bitcast(ilkdu__pfc, context.get_value_type(
        payload_type).as_pointer())
    tew__nbdz = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(yxmv__ksyoi))
    return tew__nbdz


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    ilpi__rfzq = context.insert_const_string(builder.module, 'numpy')
    gzzg__kicin = c.pyapi.import_module_noblock(ilpi__rfzq)
    hhvo__hwa = c.pyapi.object_getattr_string(gzzg__kicin, 'object_')
    wwo__gvbt = c.pyapi.long_from_longlong(n_arrays)
    eqdbb__ayhb = c.pyapi.call_method(gzzg__kicin, 'ndarray', (wwo__gvbt,
        hhvo__hwa))
    pkof__czhg = c.pyapi.object_getattr_string(gzzg__kicin, 'nan')
    jdf__hav = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType(
        64), 0))
    with cgutils.for_range(builder, n_arrays) as xpfey__zym:
        gqfg__jryq = xpfey__zym.index
        pyarray_setitem(builder, context, eqdbb__ayhb, gqfg__jryq, pkof__czhg)
        haue__awid = get_bitmap_bit(builder, null_bitmap_ptr, gqfg__jryq)
        lnazp__bmlh = builder.icmp_unsigned('!=', haue__awid, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(lnazp__bmlh):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(gqfg__jryq, lir.Constant(
                gqfg__jryq.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [gqfg__jryq]))), lir.IntType(64))
            item_ind = builder.load(jdf__hav)
            sxd__vxjh, cjxw__emhv = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), jdf__hav)
            arr_obj = c.pyapi.from_native_value(typ.dtype, cjxw__emhv, c.
                env_manager)
            pyarray_setitem(builder, context, eqdbb__ayhb, gqfg__jryq, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(gzzg__kicin)
    c.pyapi.decref(hhvo__hwa)
    c.pyapi.decref(wwo__gvbt)
    c.pyapi.decref(pkof__czhg)
    return eqdbb__ayhb


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    tew__nbdz = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = tew__nbdz.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), tew__nbdz.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), tew__nbdz.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        nkg__wnwi = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ildqj__qkab = c.context.make_helper(c.builder, typ.dtype, data_arr
            ).data
        gqyvl__fvxls = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        avysy__hrbfc = cgutils.get_or_insert_function(c.builder.module,
            gqyvl__fvxls, name='np_array_from_array_item_array')
        arr = c.builder.call(avysy__hrbfc, [tew__nbdz.n_arrays, c.builder.
            bitcast(ildqj__qkab, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), nkg__wnwi)])
    else:
        arr = _box_array_item_array_generic(typ, c, tew__nbdz.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    zoa__julj, kagqb__vkl, rei__jyshx = args
    trov__gvxj = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    uqh__gah = sig.args[1]
    if not isinstance(uqh__gah, types.UniTuple):
        kagqb__vkl = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for rei__jyshx in range(trov__gvxj)])
    elif uqh__gah.count < trov__gvxj:
        kagqb__vkl = cgutils.pack_array(builder, [builder.extract_value(
            kagqb__vkl, bnqu__zhqua) for bnqu__zhqua in range(uqh__gah.
            count)] + [lir.Constant(lir.IntType(64), -1) for rei__jyshx in
            range(trov__gvxj - uqh__gah.count)])
    zlr__xrq, rei__jyshx, rei__jyshx, rei__jyshx = construct_array_item_array(
        context, builder, array_item_type, zoa__julj, kagqb__vkl)
    bmlo__obla = context.make_helper(builder, array_item_type)
    bmlo__obla.meminfo = zlr__xrq
    return bmlo__obla._getvalue()


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
    n_arrays, jjzcf__nni, jwv__vhs, trnax__uygm = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    epvcc__noeay = context.get_value_type(payload_type)
    tywjb__gdf = context.get_abi_sizeof(epvcc__noeay)
    fekr__nubjz = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    zlr__xrq = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, tywjb__gdf), fekr__nubjz)
    ilkdu__pfc = context.nrt.meminfo_data(builder, zlr__xrq)
    yxmv__ksyoi = builder.bitcast(ilkdu__pfc, epvcc__noeay.as_pointer())
    tew__nbdz = cgutils.create_struct_proxy(payload_type)(context, builder)
    tew__nbdz.n_arrays = n_arrays
    tew__nbdz.data = jjzcf__nni
    tew__nbdz.offsets = jwv__vhs
    tew__nbdz.null_bitmap = trnax__uygm
    builder.store(tew__nbdz._getvalue(), yxmv__ksyoi)
    context.nrt.incref(builder, signature.args[1], jjzcf__nni)
    context.nrt.incref(builder, signature.args[2], jwv__vhs)
    context.nrt.incref(builder, signature.args[3], trnax__uygm)
    bmlo__obla = context.make_helper(builder, array_item_type)
    bmlo__obla.meminfo = zlr__xrq
    return bmlo__obla._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    elsew__nbkf = ArrayItemArrayType(data_type)
    sig = elsew__nbkf(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tew__nbdz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tew__nbdz.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        tew__nbdz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        ildqj__qkab = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, tew__nbdz.offsets).data
        jwv__vhs = builder.bitcast(ildqj__qkab, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(jwv__vhs, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tew__nbdz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tew__nbdz.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tew__nbdz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tew__nbdz.null_bitmap)
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
        tew__nbdz = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return tew__nbdz.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, lue__odxqh = args
        bmlo__obla = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        ilkdu__pfc = context.nrt.meminfo_data(builder, bmlo__obla.meminfo)
        yxmv__ksyoi = builder.bitcast(ilkdu__pfc, context.get_value_type(
            payload_type).as_pointer())
        tew__nbdz = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(yxmv__ksyoi))
        context.nrt.decref(builder, data_typ, tew__nbdz.data)
        tew__nbdz.data = lue__odxqh
        context.nrt.incref(builder, data_typ, lue__odxqh)
        builder.store(tew__nbdz._getvalue(), yxmv__ksyoi)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    jjzcf__nni = get_data(arr)
    fij__wpacf = len(jjzcf__nni)
    if fij__wpacf < new_size:
        cumw__lqz = max(2 * fij__wpacf, new_size)
        lue__odxqh = bodo.libs.array_kernels.resize_and_copy(jjzcf__nni,
            old_size, cumw__lqz)
        replace_data_arr(arr, lue__odxqh)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    jjzcf__nni = get_data(arr)
    jwv__vhs = get_offsets(arr)
    jeyus__ynl = len(jjzcf__nni)
    xzila__fqnix = jwv__vhs[-1]
    if jeyus__ynl != xzila__fqnix:
        lue__odxqh = bodo.libs.array_kernels.resize_and_copy(jjzcf__nni,
            xzila__fqnix, xzila__fqnix)
        replace_data_arr(arr, lue__odxqh)


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
            jwv__vhs = get_offsets(arr)
            jjzcf__nni = get_data(arr)
            mjg__pxrq = jwv__vhs[ind]
            oqh__hrqzi = jwv__vhs[ind + 1]
            return jjzcf__nni[mjg__pxrq:oqh__hrqzi]
        return array_item_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:
        sucq__sgn = arr.dtype

        def impl_bool(arr, ind):
            jni__bvp = len(arr)
            if jni__bvp != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            trnax__uygm = get_null_bitmap(arr)
            n_arrays = 0
            ekeqq__euja = init_nested_counts(sucq__sgn)
            for bnqu__zhqua in range(jni__bvp):
                if ind[bnqu__zhqua]:
                    n_arrays += 1
                    uthjw__xfn = arr[bnqu__zhqua]
                    ekeqq__euja = add_nested_counts(ekeqq__euja, uthjw__xfn)
            eqdbb__ayhb = pre_alloc_array_item_array(n_arrays, ekeqq__euja,
                sucq__sgn)
            jigdr__fdyy = get_null_bitmap(eqdbb__ayhb)
            zddc__ahfzt = 0
            for fcxbr__bhhem in range(jni__bvp):
                if ind[fcxbr__bhhem]:
                    eqdbb__ayhb[zddc__ahfzt] = arr[fcxbr__bhhem]
                    hfa__axem = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        trnax__uygm, fcxbr__bhhem)
                    bodo.libs.int_arr_ext.set_bit_to_arr(jigdr__fdyy,
                        zddc__ahfzt, hfa__axem)
                    zddc__ahfzt += 1
            return eqdbb__ayhb
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        sucq__sgn = arr.dtype

        def impl_int(arr, ind):
            trnax__uygm = get_null_bitmap(arr)
            jni__bvp = len(ind)
            n_arrays = jni__bvp
            ekeqq__euja = init_nested_counts(sucq__sgn)
            for hyfg__dzxk in range(jni__bvp):
                bnqu__zhqua = ind[hyfg__dzxk]
                uthjw__xfn = arr[bnqu__zhqua]
                ekeqq__euja = add_nested_counts(ekeqq__euja, uthjw__xfn)
            eqdbb__ayhb = pre_alloc_array_item_array(n_arrays, ekeqq__euja,
                sucq__sgn)
            jigdr__fdyy = get_null_bitmap(eqdbb__ayhb)
            for eej__gkpzs in range(jni__bvp):
                fcxbr__bhhem = ind[eej__gkpzs]
                eqdbb__ayhb[eej__gkpzs] = arr[fcxbr__bhhem]
                hfa__axem = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    trnax__uygm, fcxbr__bhhem)
                bodo.libs.int_arr_ext.set_bit_to_arr(jigdr__fdyy,
                    eej__gkpzs, hfa__axem)
            return eqdbb__ayhb
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            jni__bvp = len(arr)
            ntpxp__ytb = numba.cpython.unicode._normalize_slice(ind, jni__bvp)
            wlu__svan = np.arange(ntpxp__ytb.start, ntpxp__ytb.stop,
                ntpxp__ytb.step)
            return arr[wlu__svan]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            jwv__vhs = get_offsets(A)
            trnax__uygm = get_null_bitmap(A)
            if idx == 0:
                jwv__vhs[0] = 0
            n_items = len(val)
            efza__vxh = jwv__vhs[idx] + n_items
            ensure_data_capacity(A, jwv__vhs[idx], efza__vxh)
            jjzcf__nni = get_data(A)
            jwv__vhs[idx + 1] = jwv__vhs[idx] + n_items
            jjzcf__nni[jwv__vhs[idx]:jwv__vhs[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(trnax__uygm, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            ntpxp__ytb = numba.cpython.unicode._normalize_slice(idx, len(A))
            for bnqu__zhqua in range(ntpxp__ytb.start, ntpxp__ytb.stop,
                ntpxp__ytb.step):
                A[bnqu__zhqua] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            jwv__vhs = get_offsets(A)
            trnax__uygm = get_null_bitmap(A)
            tbhmx__sidpc = get_offsets(val)
            axzp__pbjob = get_data(val)
            zvq__xsexd = get_null_bitmap(val)
            jni__bvp = len(A)
            ntpxp__ytb = numba.cpython.unicode._normalize_slice(idx, jni__bvp)
            gzah__lvhj, frdx__hmvo = ntpxp__ytb.start, ntpxp__ytb.stop
            assert ntpxp__ytb.step == 1
            if gzah__lvhj == 0:
                jwv__vhs[gzah__lvhj] = 0
            set__aind = jwv__vhs[gzah__lvhj]
            efza__vxh = set__aind + len(axzp__pbjob)
            ensure_data_capacity(A, set__aind, efza__vxh)
            jjzcf__nni = get_data(A)
            jjzcf__nni[set__aind:set__aind + len(axzp__pbjob)] = axzp__pbjob
            jwv__vhs[gzah__lvhj:frdx__hmvo + 1] = tbhmx__sidpc + set__aind
            foe__cuimo = 0
            for bnqu__zhqua in range(gzah__lvhj, frdx__hmvo):
                hfa__axem = bodo.libs.int_arr_ext.get_bit_bitmap_arr(zvq__xsexd
                    , foe__cuimo)
                bodo.libs.int_arr_ext.set_bit_to_arr(trnax__uygm,
                    bnqu__zhqua, hfa__axem)
                foe__cuimo += 1
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
