"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.utils.typing import BodoError
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_map_arr_data_type(map_type):
    gnynt__tlpkv = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(gnynt__tlpkv)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        tsuz__elvo = _get_map_arr_data_type(fe_type)
        ias__othow = [('data', tsuz__elvo)]
        models.StructModel.__init__(self, dmm, fe_type, ias__othow)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    hoh__wph = all(isinstance(pse__dpf, types.Array) and pse__dpf.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        pse__dpf in (typ.key_arr_type, typ.value_arr_type))
    if hoh__wph:
        tar__uzzuh = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        cxvu__ngfwy = cgutils.get_or_insert_function(c.builder.module,
            tar__uzzuh, name='count_total_elems_list_array')
        nrmnw__nie = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            cxvu__ngfwy, [val])])
    else:
        nrmnw__nie = get_array_elem_counts(c, c.builder, c.context, val, typ)
    tsuz__elvo = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, tsuz__elvo,
        nrmnw__nie, c)
    hgcfb__bwu = _get_array_item_arr_payload(c.context, c.builder,
        tsuz__elvo, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, hgcfb__bwu.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, hgcfb__bwu.offsets).data
    bqgry__rdo = _get_struct_arr_payload(c.context, c.builder, tsuz__elvo.
        dtype, hgcfb__bwu.data)
    key_arr = c.builder.extract_value(bqgry__rdo.data, 0)
    value_arr = c.builder.extract_value(bqgry__rdo.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    xzbm__fps, croac__njr = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [bqgry__rdo.null_bitmap])
    if hoh__wph:
        kaax__chc = c.context.make_array(tsuz__elvo.dtype.data[0])(c.
            context, c.builder, key_arr).data
        tdy__bsu = c.context.make_array(tsuz__elvo.dtype.data[1])(c.context,
            c.builder, value_arr).data
        tar__uzzuh = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        ovi__znfgd = cgutils.get_or_insert_function(c.builder.module,
            tar__uzzuh, name='map_array_from_sequence')
        wymj__oon = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        dbpvi__pyq = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(ovi__znfgd, [val, c.builder.bitcast(kaax__chc, lir.
            IntType(8).as_pointer()), c.builder.bitcast(tdy__bsu, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), wymj__oon), lir.Constant(lir.IntType(
            32), dbpvi__pyq)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    nmn__jpgm = c.context.make_helper(c.builder, typ)
    nmn__jpgm.data = data_arr
    tmdg__svm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nmn__jpgm._getvalue(), is_error=tmdg__svm)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    rpk__hbe = context.insert_const_string(builder.module, 'pandas')
    zyzb__lavf = c.pyapi.import_module_noblock(rpk__hbe)
    wdsd__wakzu = c.pyapi.object_getattr_string(zyzb__lavf, 'NA')
    awyui__rmy = c.context.get_constant(offset_type, 0)
    builder.store(awyui__rmy, offsets_ptr)
    qsg__alrc = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as tdnp__pvf:
        wvhq__mde = tdnp__pvf.index
        item_ind = builder.load(qsg__alrc)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [wvhq__mde]))
        nuos__oig = seq_getitem(builder, context, val, wvhq__mde)
        set_bitmap_bit(builder, null_bitmap_ptr, wvhq__mde, 0)
        ubqeg__azois = is_na_value(builder, context, nuos__oig, wdsd__wakzu)
        egnw__yzv = builder.icmp_unsigned('!=', ubqeg__azois, lir.Constant(
            ubqeg__azois.type, 1))
        with builder.if_then(egnw__yzv):
            set_bitmap_bit(builder, null_bitmap_ptr, wvhq__mde, 1)
            fydk__cch = dict_keys(builder, context, nuos__oig)
            xpf__hwvx = dict_values(builder, context, nuos__oig)
            n_items = bodo.utils.utils.object_length(c, fydk__cch)
            _unbox_array_item_array_copy_data(typ.key_arr_type, fydk__cch,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type, xpf__hwvx,
                c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), qsg__alrc)
            c.pyapi.decref(fydk__cch)
            c.pyapi.decref(xpf__hwvx)
        c.pyapi.decref(nuos__oig)
    builder.store(builder.trunc(builder.load(qsg__alrc), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(zyzb__lavf)
    c.pyapi.decref(wdsd__wakzu)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    nmn__jpgm = c.context.make_helper(c.builder, typ, val)
    data_arr = nmn__jpgm.data
    tsuz__elvo = _get_map_arr_data_type(typ)
    hgcfb__bwu = _get_array_item_arr_payload(c.context, c.builder,
        tsuz__elvo, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, hgcfb__bwu.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, hgcfb__bwu.offsets).data
    bqgry__rdo = _get_struct_arr_payload(c.context, c.builder, tsuz__elvo.
        dtype, hgcfb__bwu.data)
    key_arr = c.builder.extract_value(bqgry__rdo.data, 0)
    value_arr = c.builder.extract_value(bqgry__rdo.data, 1)
    if all(isinstance(pse__dpf, types.Array) and pse__dpf.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type) for pse__dpf in
        (typ.key_arr_type, typ.value_arr_type)):
        kaax__chc = c.context.make_array(tsuz__elvo.dtype.data[0])(c.
            context, c.builder, key_arr).data
        tdy__bsu = c.context.make_array(tsuz__elvo.dtype.data[1])(c.context,
            c.builder, value_arr).data
        tar__uzzuh = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        dzbm__mevp = cgutils.get_or_insert_function(c.builder.module,
            tar__uzzuh, name='np_array_from_map_array')
        wymj__oon = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        dbpvi__pyq = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(dzbm__mevp, [hgcfb__bwu.n_arrays, c.builder.
            bitcast(kaax__chc, lir.IntType(8).as_pointer()), c.builder.
            bitcast(tdy__bsu, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), wymj__oon), lir.
            Constant(lir.IntType(32), dbpvi__pyq)])
    else:
        arr = _box_map_array_generic(typ, c, hgcfb__bwu.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    rpk__hbe = context.insert_const_string(builder.module, 'numpy')
    fkuch__wfc = c.pyapi.import_module_noblock(rpk__hbe)
    efsh__irjq = c.pyapi.object_getattr_string(fkuch__wfc, 'object_')
    nqlrj__vznz = c.pyapi.long_from_longlong(n_maps)
    quy__ubyyy = c.pyapi.call_method(fkuch__wfc, 'ndarray', (nqlrj__vznz,
        efsh__irjq))
    djug__dqgq = c.pyapi.object_getattr_string(fkuch__wfc, 'nan')
    ymnz__apc = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    qsg__alrc = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_maps) as tdnp__pvf:
        xwov__mdnq = tdnp__pvf.index
        pyarray_setitem(builder, context, quy__ubyyy, xwov__mdnq, djug__dqgq)
        kgtg__drxr = get_bitmap_bit(builder, null_bitmap_ptr, xwov__mdnq)
        wpc__hreqv = builder.icmp_unsigned('!=', kgtg__drxr, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(wpc__hreqv):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(xwov__mdnq, lir.Constant(
                xwov__mdnq.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [xwov__mdnq]))), lir.IntType(64))
            item_ind = builder.load(qsg__alrc)
            nuos__oig = c.pyapi.dict_new()
            ilkmf__ibk = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            xzbm__fps, jmhcr__olofu = c.pyapi.call_jit_code(ilkmf__ibk, typ
                .key_arr_type(typ.key_arr_type, types.int64, types.int64),
                [key_arr, item_ind, n_items])
            xzbm__fps, daw__elv = c.pyapi.call_jit_code(ilkmf__ibk, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            vwhf__tdh = c.pyapi.from_native_value(typ.key_arr_type,
                jmhcr__olofu, c.env_manager)
            hxbta__dqq = c.pyapi.from_native_value(typ.value_arr_type,
                daw__elv, c.env_manager)
            vuxji__daadb = c.pyapi.call_function_objargs(ymnz__apc, (
                vwhf__tdh, hxbta__dqq))
            dict_merge_from_seq2(builder, context, nuos__oig, vuxji__daadb)
            builder.store(builder.add(item_ind, n_items), qsg__alrc)
            pyarray_setitem(builder, context, quy__ubyyy, xwov__mdnq, nuos__oig
                )
            c.pyapi.decref(vuxji__daadb)
            c.pyapi.decref(vwhf__tdh)
            c.pyapi.decref(hxbta__dqq)
            c.pyapi.decref(nuos__oig)
    c.pyapi.decref(ymnz__apc)
    c.pyapi.decref(fkuch__wfc)
    c.pyapi.decref(efsh__irjq)
    c.pyapi.decref(nqlrj__vznz)
    c.pyapi.decref(djug__dqgq)
    return quy__ubyyy


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    nmn__jpgm = context.make_helper(builder, sig.return_type)
    nmn__jpgm.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return nmn__jpgm._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    ywb__yxe = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return ywb__yxe(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    zuiv__pngdy = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(zuiv__pngdy)


def pre_alloc_map_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_map_arr_ext_pre_alloc_map_array
    ) = pre_alloc_map_array_equiv


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(MapArrayType, 'copy')
def overload_map_arr_copy(A):
    return lambda A: init_map_arr(A._data.copy())


@overload(operator.setitem, no_unliteral=True)
def map_arr_setitem(arr, ind, val):
    if not isinstance(arr, MapArrayType):
        return
    hyh__qzxn = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            hmqt__rkog = val.keys()
            svxja__zslwq = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), hyh__qzxn, ('key', 'value'))
            for nnm__qaltp, xvrbm__erx in enumerate(hmqt__rkog):
                svxja__zslwq[nnm__qaltp
                    ] = bodo.libs.struct_arr_ext.init_struct((xvrbm__erx,
                    val[xvrbm__erx]), ('key', 'value'))
            arr._data[ind] = svxja__zslwq
        return map_arr_setitem_impl
    raise BodoError(
        'operator.setitem with MapArrays is only supported with an integer index.'
        )


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            ochj__nzzfw = dict()
            ugak__aea = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            svxja__zslwq = bodo.libs.array_item_arr_ext.get_data(arr._data)
            xzlw__nle, inpz__dulpu = bodo.libs.struct_arr_ext.get_data(
                svxja__zslwq)
            nco__zlrv = ugak__aea[ind]
            bru__fav = ugak__aea[ind + 1]
            for nnm__qaltp in range(nco__zlrv, bru__fav):
                ochj__nzzfw[xzlw__nle[nnm__qaltp]] = inpz__dulpu[nnm__qaltp]
            return ochj__nzzfw
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
