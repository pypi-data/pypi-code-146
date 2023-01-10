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
    onos__ouiy = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(onos__ouiy)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qcj__hdfhd = _get_map_arr_data_type(fe_type)
        dhful__patjv = [('data', qcj__hdfhd)]
        models.StructModel.__init__(self, dmm, fe_type, dhful__patjv)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    vvfw__ygy = all(isinstance(pvowk__eefoe, types.Array) and pvowk__eefoe.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for pvowk__eefoe in (typ.key_arr_type, typ.
        value_arr_type))
    if vvfw__ygy:
        lwe__ykaab = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        nty__fii = cgutils.get_or_insert_function(c.builder.module,
            lwe__ykaab, name='count_total_elems_list_array')
        bgaj__ymaqg = cgutils.pack_array(c.builder, [n_maps, c.builder.call
            (nty__fii, [val])])
    else:
        bgaj__ymaqg = get_array_elem_counts(c, c.builder, c.context, val, typ)
    qcj__hdfhd = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, qcj__hdfhd,
        bgaj__ymaqg, c)
    kznc__molp = _get_array_item_arr_payload(c.context, c.builder,
        qcj__hdfhd, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, kznc__molp.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, kznc__molp.offsets).data
    rysq__sogid = _get_struct_arr_payload(c.context, c.builder, qcj__hdfhd.
        dtype, kznc__molp.data)
    key_arr = c.builder.extract_value(rysq__sogid.data, 0)
    value_arr = c.builder.extract_value(rysq__sogid.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    odjcl__qkg, lmxgm__lgrc = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [rysq__sogid.null_bitmap])
    if vvfw__ygy:
        zkna__oidew = c.context.make_array(qcj__hdfhd.dtype.data[0])(c.
            context, c.builder, key_arr).data
        yozhw__ysejx = c.context.make_array(qcj__hdfhd.dtype.data[1])(c.
            context, c.builder, value_arr).data
        lwe__ykaab = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        fxmgd__birb = cgutils.get_or_insert_function(c.builder.module,
            lwe__ykaab, name='map_array_from_sequence')
        npx__con = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        jesq__bfe = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(fxmgd__birb, [val, c.builder.bitcast(zkna__oidew,
            lir.IntType(8).as_pointer()), c.builder.bitcast(yozhw__ysejx,
            lir.IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir
            .Constant(lir.IntType(32), npx__con), lir.Constant(lir.IntType(
            32), jesq__bfe)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    pivk__ryi = c.context.make_helper(c.builder, typ)
    pivk__ryi.data = data_arr
    nej__ylwtx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(pivk__ryi._getvalue(), is_error=nej__ylwtx)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    tbok__sqoji = context.insert_const_string(builder.module, 'pandas')
    mtfkt__wfm = c.pyapi.import_module_noblock(tbok__sqoji)
    xczxi__vqoil = c.pyapi.object_getattr_string(mtfkt__wfm, 'NA')
    jboj__fnew = c.context.get_constant(offset_type, 0)
    builder.store(jboj__fnew, offsets_ptr)
    abolz__psp = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as fdi__hjjl:
        fhkyg__jtuna = fdi__hjjl.index
        item_ind = builder.load(abolz__psp)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [fhkyg__jtuna]))
        uzfcm__mrdz = seq_getitem(builder, context, val, fhkyg__jtuna)
        set_bitmap_bit(builder, null_bitmap_ptr, fhkyg__jtuna, 0)
        uuuev__ccepp = is_na_value(builder, context, uzfcm__mrdz, xczxi__vqoil)
        rsjhd__luoqy = builder.icmp_unsigned('!=', uuuev__ccepp, lir.
            Constant(uuuev__ccepp.type, 1))
        with builder.if_then(rsjhd__luoqy):
            set_bitmap_bit(builder, null_bitmap_ptr, fhkyg__jtuna, 1)
            gvqo__fvo = dict_keys(builder, context, uzfcm__mrdz)
            gpqfc__ajd = dict_values(builder, context, uzfcm__mrdz)
            n_items = bodo.utils.utils.object_length(c, gvqo__fvo)
            _unbox_array_item_array_copy_data(typ.key_arr_type, gvqo__fvo,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                gpqfc__ajd, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), abolz__psp)
            c.pyapi.decref(gvqo__fvo)
            c.pyapi.decref(gpqfc__ajd)
        c.pyapi.decref(uzfcm__mrdz)
    builder.store(builder.trunc(builder.load(abolz__psp), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(mtfkt__wfm)
    c.pyapi.decref(xczxi__vqoil)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    pivk__ryi = c.context.make_helper(c.builder, typ, val)
    data_arr = pivk__ryi.data
    qcj__hdfhd = _get_map_arr_data_type(typ)
    kznc__molp = _get_array_item_arr_payload(c.context, c.builder,
        qcj__hdfhd, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, kznc__molp.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, kznc__molp.offsets).data
    rysq__sogid = _get_struct_arr_payload(c.context, c.builder, qcj__hdfhd.
        dtype, kznc__molp.data)
    key_arr = c.builder.extract_value(rysq__sogid.data, 0)
    value_arr = c.builder.extract_value(rysq__sogid.data, 1)
    if all(isinstance(pvowk__eefoe, types.Array) and pvowk__eefoe.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        pvowk__eefoe in (typ.key_arr_type, typ.value_arr_type)):
        zkna__oidew = c.context.make_array(qcj__hdfhd.dtype.data[0])(c.
            context, c.builder, key_arr).data
        yozhw__ysejx = c.context.make_array(qcj__hdfhd.dtype.data[1])(c.
            context, c.builder, value_arr).data
        lwe__ykaab = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        ezg__ygun = cgutils.get_or_insert_function(c.builder.module,
            lwe__ykaab, name='np_array_from_map_array')
        npx__con = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        jesq__bfe = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(ezg__ygun, [kznc__molp.n_arrays, c.builder.
            bitcast(zkna__oidew, lir.IntType(8).as_pointer()), c.builder.
            bitcast(yozhw__ysejx, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), npx__con), lir.
            Constant(lir.IntType(32), jesq__bfe)])
    else:
        arr = _box_map_array_generic(typ, c, kznc__molp.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    tbok__sqoji = context.insert_const_string(builder.module, 'numpy')
    xrq__tcqhe = c.pyapi.import_module_noblock(tbok__sqoji)
    olo__trc = c.pyapi.object_getattr_string(xrq__tcqhe, 'object_')
    ezk__kvf = c.pyapi.long_from_longlong(n_maps)
    ukrln__hfnvt = c.pyapi.call_method(xrq__tcqhe, 'ndarray', (ezk__kvf,
        olo__trc))
    mkeu__bak = c.pyapi.object_getattr_string(xrq__tcqhe, 'nan')
    ota__lywx = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    abolz__psp = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as fdi__hjjl:
        jyi__yev = fdi__hjjl.index
        pyarray_setitem(builder, context, ukrln__hfnvt, jyi__yev, mkeu__bak)
        qex__nrk = get_bitmap_bit(builder, null_bitmap_ptr, jyi__yev)
        ypfh__jtj = builder.icmp_unsigned('!=', qex__nrk, lir.Constant(lir.
            IntType(8), 0))
        with builder.if_then(ypfh__jtj):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(jyi__yev, lir.Constant(jyi__yev.
                type, 1))])), builder.load(builder.gep(offsets_ptr, [
                jyi__yev]))), lir.IntType(64))
            item_ind = builder.load(abolz__psp)
            uzfcm__mrdz = c.pyapi.dict_new()
            crpv__zbnul = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            odjcl__qkg, ebze__fhkl = c.pyapi.call_jit_code(crpv__zbnul, typ
                .key_arr_type(typ.key_arr_type, types.int64, types.int64),
                [key_arr, item_ind, n_items])
            odjcl__qkg, lykp__grc = c.pyapi.call_jit_code(crpv__zbnul, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            vtrta__kagnz = c.pyapi.from_native_value(typ.key_arr_type,
                ebze__fhkl, c.env_manager)
            ucft__gacax = c.pyapi.from_native_value(typ.value_arr_type,
                lykp__grc, c.env_manager)
            hsg__hya = c.pyapi.call_function_objargs(ota__lywx, (
                vtrta__kagnz, ucft__gacax))
            dict_merge_from_seq2(builder, context, uzfcm__mrdz, hsg__hya)
            builder.store(builder.add(item_ind, n_items), abolz__psp)
            pyarray_setitem(builder, context, ukrln__hfnvt, jyi__yev,
                uzfcm__mrdz)
            c.pyapi.decref(hsg__hya)
            c.pyapi.decref(vtrta__kagnz)
            c.pyapi.decref(ucft__gacax)
            c.pyapi.decref(uzfcm__mrdz)
    c.pyapi.decref(ota__lywx)
    c.pyapi.decref(xrq__tcqhe)
    c.pyapi.decref(olo__trc)
    c.pyapi.decref(ezk__kvf)
    c.pyapi.decref(mkeu__bak)
    return ukrln__hfnvt


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    pivk__ryi = context.make_helper(builder, sig.return_type)
    pivk__ryi.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return pivk__ryi._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    qnx__fxee = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return qnx__fxee(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    pwz__wnr = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(num_maps
        , nested_counts, struct_typ)
    return init_map_arr(pwz__wnr)


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
    wrutr__lrdg = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            ulqwd__wqa = val.keys()
            iwcfv__tfh = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), wrutr__lrdg, ('key', 'value'))
            for ncqg__ile, rwx__qxck in enumerate(ulqwd__wqa):
                iwcfv__tfh[ncqg__ile] = bodo.libs.struct_arr_ext.init_struct((
                    rwx__qxck, val[rwx__qxck]), ('key', 'value'))
            arr._data[ind] = iwcfv__tfh
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
            wggu__zaep = dict()
            ibgyw__rdd = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            iwcfv__tfh = bodo.libs.array_item_arr_ext.get_data(arr._data)
            ytyc__bij, lscib__dknah = bodo.libs.struct_arr_ext.get_data(
                iwcfv__tfh)
            ebk__hhpw = ibgyw__rdd[ind]
            kvx__psqh = ibgyw__rdd[ind + 1]
            for ncqg__ile in range(ebk__hhpw, kvx__psqh):
                wggu__zaep[ytyc__bij[ncqg__ile]] = lscib__dknah[ncqg__ile]
            return wggu__zaep
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
