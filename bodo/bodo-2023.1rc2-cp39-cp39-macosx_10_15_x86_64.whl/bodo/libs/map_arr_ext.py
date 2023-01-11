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
    dye__zneo = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(dye__zneo)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jrmsa__givus = _get_map_arr_data_type(fe_type)
        qvm__pujhu = [('data', jrmsa__givus)]
        models.StructModel.__init__(self, dmm, fe_type, qvm__pujhu)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    uoqs__etubf = all(isinstance(jjkrs__epj, types.Array) and jjkrs__epj.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for jjkrs__epj in (typ.key_arr_type, typ.
        value_arr_type))
    if uoqs__etubf:
        mvgt__kggs = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        lkt__kwemm = cgutils.get_or_insert_function(c.builder.module,
            mvgt__kggs, name='count_total_elems_list_array')
        hztov__eeh = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            lkt__kwemm, [val])])
    else:
        hztov__eeh = get_array_elem_counts(c, c.builder, c.context, val, typ)
    jrmsa__givus = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, jrmsa__givus,
        hztov__eeh, c)
    pssd__zyo = _get_array_item_arr_payload(c.context, c.builder,
        jrmsa__givus, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, pssd__zyo.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, pssd__zyo.offsets).data
    mvnrt__lofgb = _get_struct_arr_payload(c.context, c.builder,
        jrmsa__givus.dtype, pssd__zyo.data)
    key_arr = c.builder.extract_value(mvnrt__lofgb.data, 0)
    value_arr = c.builder.extract_value(mvnrt__lofgb.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    kma__fjx, myiup__qlccr = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [mvnrt__lofgb.null_bitmap])
    if uoqs__etubf:
        qudg__jaaeb = c.context.make_array(jrmsa__givus.dtype.data[0])(c.
            context, c.builder, key_arr).data
        cjogl__sdz = c.context.make_array(jrmsa__givus.dtype.data[1])(c.
            context, c.builder, value_arr).data
        mvgt__kggs = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        hmke__moc = cgutils.get_or_insert_function(c.builder.module,
            mvgt__kggs, name='map_array_from_sequence')
        vhq__hnpqt = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        dnn__mbw = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(hmke__moc, [val, c.builder.bitcast(qudg__jaaeb, lir.
            IntType(8).as_pointer()), c.builder.bitcast(cjogl__sdz, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), vhq__hnpqt), lir.Constant(lir.IntType
            (32), dnn__mbw)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    kwir__vnfe = c.context.make_helper(c.builder, typ)
    kwir__vnfe.data = data_arr
    gler__ihw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(kwir__vnfe._getvalue(), is_error=gler__ihw)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    jupe__dwev = context.insert_const_string(builder.module, 'pandas')
    timh__fjuo = c.pyapi.import_module_noblock(jupe__dwev)
    vugm__ubgb = c.pyapi.object_getattr_string(timh__fjuo, 'NA')
    fnx__dnseu = c.context.get_constant(offset_type, 0)
    builder.store(fnx__dnseu, offsets_ptr)
    kyw__tfya = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as uiewl__zsxcl:
        ecdn__addz = uiewl__zsxcl.index
        item_ind = builder.load(kyw__tfya)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [ecdn__addz]))
        mgvtd__hhq = seq_getitem(builder, context, val, ecdn__addz)
        set_bitmap_bit(builder, null_bitmap_ptr, ecdn__addz, 0)
        wscx__zsd = is_na_value(builder, context, mgvtd__hhq, vugm__ubgb)
        ufc__nzs = builder.icmp_unsigned('!=', wscx__zsd, lir.Constant(
            wscx__zsd.type, 1))
        with builder.if_then(ufc__nzs):
            set_bitmap_bit(builder, null_bitmap_ptr, ecdn__addz, 1)
            abcwb__rvz = dict_keys(builder, context, mgvtd__hhq)
            bumi__ehpz = dict_values(builder, context, mgvtd__hhq)
            n_items = bodo.utils.utils.object_length(c, abcwb__rvz)
            _unbox_array_item_array_copy_data(typ.key_arr_type, abcwb__rvz,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                bumi__ehpz, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), kyw__tfya)
            c.pyapi.decref(abcwb__rvz)
            c.pyapi.decref(bumi__ehpz)
        c.pyapi.decref(mgvtd__hhq)
    builder.store(builder.trunc(builder.load(kyw__tfya), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(timh__fjuo)
    c.pyapi.decref(vugm__ubgb)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    kwir__vnfe = c.context.make_helper(c.builder, typ, val)
    data_arr = kwir__vnfe.data
    jrmsa__givus = _get_map_arr_data_type(typ)
    pssd__zyo = _get_array_item_arr_payload(c.context, c.builder,
        jrmsa__givus, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, pssd__zyo.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, pssd__zyo.offsets).data
    mvnrt__lofgb = _get_struct_arr_payload(c.context, c.builder,
        jrmsa__givus.dtype, pssd__zyo.data)
    key_arr = c.builder.extract_value(mvnrt__lofgb.data, 0)
    value_arr = c.builder.extract_value(mvnrt__lofgb.data, 1)
    if all(isinstance(jjkrs__epj, types.Array) and jjkrs__epj.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type) for
        jjkrs__epj in (typ.key_arr_type, typ.value_arr_type)):
        qudg__jaaeb = c.context.make_array(jrmsa__givus.dtype.data[0])(c.
            context, c.builder, key_arr).data
        cjogl__sdz = c.context.make_array(jrmsa__givus.dtype.data[1])(c.
            context, c.builder, value_arr).data
        mvgt__kggs = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        xstje__xkdq = cgutils.get_or_insert_function(c.builder.module,
            mvgt__kggs, name='np_array_from_map_array')
        vhq__hnpqt = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        dnn__mbw = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(xstje__xkdq, [pssd__zyo.n_arrays, c.builder.
            bitcast(qudg__jaaeb, lir.IntType(8).as_pointer()), c.builder.
            bitcast(cjogl__sdz, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), vhq__hnpqt), lir
            .Constant(lir.IntType(32), dnn__mbw)])
    else:
        arr = _box_map_array_generic(typ, c, pssd__zyo.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    jupe__dwev = context.insert_const_string(builder.module, 'numpy')
    kzpqy__luzg = c.pyapi.import_module_noblock(jupe__dwev)
    unm__hwpu = c.pyapi.object_getattr_string(kzpqy__luzg, 'object_')
    cucmu__tyot = c.pyapi.long_from_longlong(n_maps)
    ofch__ytfta = c.pyapi.call_method(kzpqy__luzg, 'ndarray', (cucmu__tyot,
        unm__hwpu))
    apam__pueee = c.pyapi.object_getattr_string(kzpqy__luzg, 'nan')
    yhrw__whh = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    kyw__tfya = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_maps) as uiewl__zsxcl:
        aavdg__pguq = uiewl__zsxcl.index
        pyarray_setitem(builder, context, ofch__ytfta, aavdg__pguq, apam__pueee
            )
        ygl__wsxz = get_bitmap_bit(builder, null_bitmap_ptr, aavdg__pguq)
        yrh__yrom = builder.icmp_unsigned('!=', ygl__wsxz, lir.Constant(lir
            .IntType(8), 0))
        with builder.if_then(yrh__yrom):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(aavdg__pguq, lir.Constant(
                aavdg__pguq.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [aavdg__pguq]))), lir.IntType(64))
            item_ind = builder.load(kyw__tfya)
            mgvtd__hhq = c.pyapi.dict_new()
            jgnhd__twsv = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            kma__fjx, qlmqi__uxl = c.pyapi.call_jit_code(jgnhd__twsv, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            kma__fjx, syt__xrffx = c.pyapi.call_jit_code(jgnhd__twsv, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            jwfyj__ikn = c.pyapi.from_native_value(typ.key_arr_type,
                qlmqi__uxl, c.env_manager)
            jkxt__cbptx = c.pyapi.from_native_value(typ.value_arr_type,
                syt__xrffx, c.env_manager)
            sebh__rlko = c.pyapi.call_function_objargs(yhrw__whh, (
                jwfyj__ikn, jkxt__cbptx))
            dict_merge_from_seq2(builder, context, mgvtd__hhq, sebh__rlko)
            builder.store(builder.add(item_ind, n_items), kyw__tfya)
            pyarray_setitem(builder, context, ofch__ytfta, aavdg__pguq,
                mgvtd__hhq)
            c.pyapi.decref(sebh__rlko)
            c.pyapi.decref(jwfyj__ikn)
            c.pyapi.decref(jkxt__cbptx)
            c.pyapi.decref(mgvtd__hhq)
    c.pyapi.decref(yhrw__whh)
    c.pyapi.decref(kzpqy__luzg)
    c.pyapi.decref(unm__hwpu)
    c.pyapi.decref(cucmu__tyot)
    c.pyapi.decref(apam__pueee)
    return ofch__ytfta


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    kwir__vnfe = context.make_helper(builder, sig.return_type)
    kwir__vnfe.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return kwir__vnfe._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    pmhyz__uqecv = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return pmhyz__uqecv(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    bdf__jdvg = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(bdf__jdvg)


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
    utm__absh = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            tqf__bcd = val.keys()
            epfa__uxzh = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), utm__absh, ('key', 'value'))
            for bwtz__mvhu, cviuh__eipvx in enumerate(tqf__bcd):
                epfa__uxzh[bwtz__mvhu] = bodo.libs.struct_arr_ext.init_struct((
                    cviuh__eipvx, val[cviuh__eipvx]), ('key', 'value'))
            arr._data[ind] = epfa__uxzh
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
            wiyu__qjdu = dict()
            lll__ynw = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            epfa__uxzh = bodo.libs.array_item_arr_ext.get_data(arr._data)
            tncp__gpuqv, gvfoi__bnol = bodo.libs.struct_arr_ext.get_data(
                epfa__uxzh)
            izeqp__agioi = lll__ynw[ind]
            zcqa__lbbv = lll__ynw[ind + 1]
            for bwtz__mvhu in range(izeqp__agioi, zcqa__lbbv):
                wiyu__qjdu[tncp__gpuqv[bwtz__mvhu]] = gvfoi__bnol[bwtz__mvhu]
            return wiyu__qjdu
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
