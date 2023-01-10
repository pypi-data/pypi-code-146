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
    oyvgn__fxqh = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(oyvgn__fxqh)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        spbqo__gvdh = _get_map_arr_data_type(fe_type)
        fhr__ywrc = [('data', spbqo__gvdh)]
        models.StructModel.__init__(self, dmm, fe_type, fhr__ywrc)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    teqg__lida = all(isinstance(hiya__enqd, types.Array) and hiya__enqd.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for hiya__enqd in (typ.key_arr_type, typ.
        value_arr_type))
    if teqg__lida:
        peul__jwos = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        uctyc__byi = cgutils.get_or_insert_function(c.builder.module,
            peul__jwos, name='count_total_elems_list_array')
        ppgn__ejit = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            uctyc__byi, [val])])
    else:
        ppgn__ejit = get_array_elem_counts(c, c.builder, c.context, val, typ)
    spbqo__gvdh = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, spbqo__gvdh,
        ppgn__ejit, c)
    kqxh__ghgkn = _get_array_item_arr_payload(c.context, c.builder,
        spbqo__gvdh, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, kqxh__ghgkn.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, kqxh__ghgkn.offsets).data
    yukpg__bzjt = _get_struct_arr_payload(c.context, c.builder, spbqo__gvdh
        .dtype, kqxh__ghgkn.data)
    key_arr = c.builder.extract_value(yukpg__bzjt.data, 0)
    value_arr = c.builder.extract_value(yukpg__bzjt.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    harty__ayv, isolt__cizqo = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [yukpg__bzjt.null_bitmap])
    if teqg__lida:
        ovy__wzu = c.context.make_array(spbqo__gvdh.dtype.data[0])(c.
            context, c.builder, key_arr).data
        bpuc__hag = c.context.make_array(spbqo__gvdh.dtype.data[1])(c.
            context, c.builder, value_arr).data
        peul__jwos = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        cdfri__hujc = cgutils.get_or_insert_function(c.builder.module,
            peul__jwos, name='map_array_from_sequence')
        srm__mzpv = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        bqsh__tsty = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(cdfri__hujc, [val, c.builder.bitcast(ovy__wzu, lir.
            IntType(8).as_pointer()), c.builder.bitcast(bpuc__hag, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), srm__mzpv), lir.Constant(lir.IntType(
            32), bqsh__tsty)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    dcuao__zlgwz = c.context.make_helper(c.builder, typ)
    dcuao__zlgwz.data = data_arr
    shm__fykh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dcuao__zlgwz._getvalue(), is_error=shm__fykh)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    avzcg__rgsn = context.insert_const_string(builder.module, 'pandas')
    lwct__ugmry = c.pyapi.import_module_noblock(avzcg__rgsn)
    unrrx__xwq = c.pyapi.object_getattr_string(lwct__ugmry, 'NA')
    mluax__bemp = c.context.get_constant(offset_type, 0)
    builder.store(mluax__bemp, offsets_ptr)
    pwg__thcep = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as rnk__srkyq:
        bcpe__ugi = rnk__srkyq.index
        item_ind = builder.load(pwg__thcep)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [bcpe__ugi]))
        hhbsy__ytyry = seq_getitem(builder, context, val, bcpe__ugi)
        set_bitmap_bit(builder, null_bitmap_ptr, bcpe__ugi, 0)
        kwr__nznyg = is_na_value(builder, context, hhbsy__ytyry, unrrx__xwq)
        vunpc__ghglm = builder.icmp_unsigned('!=', kwr__nznyg, lir.Constant
            (kwr__nznyg.type, 1))
        with builder.if_then(vunpc__ghglm):
            set_bitmap_bit(builder, null_bitmap_ptr, bcpe__ugi, 1)
            gnz__gyrt = dict_keys(builder, context, hhbsy__ytyry)
            zzyuh__ujp = dict_values(builder, context, hhbsy__ytyry)
            n_items = bodo.utils.utils.object_length(c, gnz__gyrt)
            _unbox_array_item_array_copy_data(typ.key_arr_type, gnz__gyrt,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                zzyuh__ujp, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), pwg__thcep)
            c.pyapi.decref(gnz__gyrt)
            c.pyapi.decref(zzyuh__ujp)
        c.pyapi.decref(hhbsy__ytyry)
    builder.store(builder.trunc(builder.load(pwg__thcep), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(lwct__ugmry)
    c.pyapi.decref(unrrx__xwq)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    dcuao__zlgwz = c.context.make_helper(c.builder, typ, val)
    data_arr = dcuao__zlgwz.data
    spbqo__gvdh = _get_map_arr_data_type(typ)
    kqxh__ghgkn = _get_array_item_arr_payload(c.context, c.builder,
        spbqo__gvdh, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, kqxh__ghgkn.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, kqxh__ghgkn.offsets).data
    yukpg__bzjt = _get_struct_arr_payload(c.context, c.builder, spbqo__gvdh
        .dtype, kqxh__ghgkn.data)
    key_arr = c.builder.extract_value(yukpg__bzjt.data, 0)
    value_arr = c.builder.extract_value(yukpg__bzjt.data, 1)
    if all(isinstance(hiya__enqd, types.Array) and hiya__enqd.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type) for
        hiya__enqd in (typ.key_arr_type, typ.value_arr_type)):
        ovy__wzu = c.context.make_array(spbqo__gvdh.dtype.data[0])(c.
            context, c.builder, key_arr).data
        bpuc__hag = c.context.make_array(spbqo__gvdh.dtype.data[1])(c.
            context, c.builder, value_arr).data
        peul__jwos = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        ihivo__izb = cgutils.get_or_insert_function(c.builder.module,
            peul__jwos, name='np_array_from_map_array')
        srm__mzpv = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        bqsh__tsty = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(ihivo__izb, [kqxh__ghgkn.n_arrays, c.builder.
            bitcast(ovy__wzu, lir.IntType(8).as_pointer()), c.builder.
            bitcast(bpuc__hag, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), srm__mzpv), lir.
            Constant(lir.IntType(32), bqsh__tsty)])
    else:
        arr = _box_map_array_generic(typ, c, kqxh__ghgkn.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    avzcg__rgsn = context.insert_const_string(builder.module, 'numpy')
    idaus__djn = c.pyapi.import_module_noblock(avzcg__rgsn)
    advsb__tsg = c.pyapi.object_getattr_string(idaus__djn, 'object_')
    rvezy__zxjst = c.pyapi.long_from_longlong(n_maps)
    bjd__jdug = c.pyapi.call_method(idaus__djn, 'ndarray', (rvezy__zxjst,
        advsb__tsg))
    jbu__ndtq = c.pyapi.object_getattr_string(idaus__djn, 'nan')
    nsbk__hff = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    pwg__thcep = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as rnk__srkyq:
        rgd__pxl = rnk__srkyq.index
        pyarray_setitem(builder, context, bjd__jdug, rgd__pxl, jbu__ndtq)
        uoaz__dtzr = get_bitmap_bit(builder, null_bitmap_ptr, rgd__pxl)
        pcut__mhbws = builder.icmp_unsigned('!=', uoaz__dtzr, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(pcut__mhbws):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(rgd__pxl, lir.Constant(rgd__pxl.
                type, 1))])), builder.load(builder.gep(offsets_ptr, [
                rgd__pxl]))), lir.IntType(64))
            item_ind = builder.load(pwg__thcep)
            hhbsy__ytyry = c.pyapi.dict_new()
            fccr__acycl = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            harty__ayv, oylkp__gbini = c.pyapi.call_jit_code(fccr__acycl,
                typ.key_arr_type(typ.key_arr_type, types.int64, types.int64
                ), [key_arr, item_ind, n_items])
            harty__ayv, jpn__xtfs = c.pyapi.call_jit_code(fccr__acycl, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            oqdoa__zmoh = c.pyapi.from_native_value(typ.key_arr_type,
                oylkp__gbini, c.env_manager)
            ehjx__ybodw = c.pyapi.from_native_value(typ.value_arr_type,
                jpn__xtfs, c.env_manager)
            yiliq__cxpw = c.pyapi.call_function_objargs(nsbk__hff, (
                oqdoa__zmoh, ehjx__ybodw))
            dict_merge_from_seq2(builder, context, hhbsy__ytyry, yiliq__cxpw)
            builder.store(builder.add(item_ind, n_items), pwg__thcep)
            pyarray_setitem(builder, context, bjd__jdug, rgd__pxl, hhbsy__ytyry
                )
            c.pyapi.decref(yiliq__cxpw)
            c.pyapi.decref(oqdoa__zmoh)
            c.pyapi.decref(ehjx__ybodw)
            c.pyapi.decref(hhbsy__ytyry)
    c.pyapi.decref(nsbk__hff)
    c.pyapi.decref(idaus__djn)
    c.pyapi.decref(advsb__tsg)
    c.pyapi.decref(rvezy__zxjst)
    c.pyapi.decref(jbu__ndtq)
    return bjd__jdug


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    dcuao__zlgwz = context.make_helper(builder, sig.return_type)
    dcuao__zlgwz.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return dcuao__zlgwz._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    rxeu__kgu = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return rxeu__kgu(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    xuwv__gmol = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(xuwv__gmol)


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
    jqqqc__vgpjh = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            fswc__lafp = val.keys()
            arka__akt = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), jqqqc__vgpjh, ('key', 'value'))
            for ngmm__jjfah, wdlv__tql in enumerate(fswc__lafp):
                arka__akt[ngmm__jjfah] = bodo.libs.struct_arr_ext.init_struct((
                    wdlv__tql, val[wdlv__tql]), ('key', 'value'))
            arr._data[ind] = arka__akt
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
            wddmr__wnrsb = dict()
            bhb__eib = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            arka__akt = bodo.libs.array_item_arr_ext.get_data(arr._data)
            bapey__dod, xzmfo__tdf = bodo.libs.struct_arr_ext.get_data(
                arka__akt)
            mxu__oyaqi = bhb__eib[ind]
            jtx__goc = bhb__eib[ind + 1]
            for ngmm__jjfah in range(mxu__oyaqi, jtx__goc):
                wddmr__wnrsb[bapey__dod[ngmm__jjfah]] = xzmfo__tdf[ngmm__jjfah]
            return wddmr__wnrsb
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
