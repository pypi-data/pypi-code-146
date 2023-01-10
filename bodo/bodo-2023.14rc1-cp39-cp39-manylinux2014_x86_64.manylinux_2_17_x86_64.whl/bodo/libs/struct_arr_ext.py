"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.time_ext import TimeType
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(pkz__sleg, False) for pkz__sleg in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(pkz__sleg,
                str) for pkz__sleg in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(lqvac__cbgs.dtype for lqvac__cbgs in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(pkz__sleg) for pkz__sleg in d.keys())
        data = tuple(dtype_to_array_type(lqvac__cbgs) for lqvac__cbgs in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(pkz__sleg, False) for pkz__sleg in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zhlc__duvhz = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, zhlc__duvhz)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        zhlc__duvhz = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, zhlc__duvhz)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    izt__qztwk = builder.module
    hpn__osfzl = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    ify__slkdl = cgutils.get_or_insert_function(izt__qztwk, hpn__osfzl,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not ify__slkdl.is_declaration:
        return ify__slkdl
    ify__slkdl.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(ify__slkdl.append_basic_block())
    ajkkw__xmw = ify__slkdl.args[0]
    xyz__iblg = context.get_value_type(payload_type).as_pointer()
    doxa__gzhra = builder.bitcast(ajkkw__xmw, xyz__iblg)
    lfqq__tvva = context.make_helper(builder, payload_type, ref=doxa__gzhra)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), lfqq__tvva.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        lfqq__tvva.null_bitmap)
    builder.ret_void()
    return ify__slkdl


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    rci__mzz = context.get_value_type(payload_type)
    cup__fdbe = context.get_abi_sizeof(rci__mzz)
    pwli__plt = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    zyomj__tcr = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, cup__fdbe), pwli__plt)
    vbrig__uurdf = context.nrt.meminfo_data(builder, zyomj__tcr)
    fyoq__hew = builder.bitcast(vbrig__uurdf, rci__mzz.as_pointer())
    lfqq__tvva = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    vwvjg__gys = 0
    for arr_typ in struct_arr_type.data:
        jbsg__gsymn = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        chjgt__gemqx = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(vwvjg__gys, vwvjg__gys +
            jbsg__gsymn)])
        arr = gen_allocate_array(context, builder, arr_typ, chjgt__gemqx, c)
        arrs.append(arr)
        vwvjg__gys += jbsg__gsymn
    lfqq__tvva.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    cwuk__nolz = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    zoo__ynb = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [cwuk__nolz])
    null_bitmap_ptr = zoo__ynb.data
    lfqq__tvva.null_bitmap = zoo__ynb._getvalue()
    builder.store(lfqq__tvva._getvalue(), fyoq__hew)
    return zyomj__tcr, lfqq__tvva.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    pnolm__wmofu = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        gnd__lmdag = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            gnd__lmdag)
        pnolm__wmofu.append(arr.data)
    lwsm__xvymk = cgutils.pack_array(c.builder, pnolm__wmofu
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, pnolm__wmofu)
    whx__msozi = cgutils.alloca_once_value(c.builder, lwsm__xvymk)
    jsdu__ylzo = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(pkz__sleg.dtype)) for pkz__sleg in data_typ]
    ttfim__vwt = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, jsdu__ylzo))
    cxms__pfa = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, pkz__sleg) for pkz__sleg in
        names])
    uxe__uhaf = cgutils.alloca_once_value(c.builder, cxms__pfa)
    return whx__msozi, ttfim__vwt, uxe__uhaf


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    jphv__bxx = all(isinstance(lqvac__cbgs, types.Array) and (lqvac__cbgs.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(lqvac__cbgs.dtype, TimeType)) for
        lqvac__cbgs in typ.data)
    if jphv__bxx:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        hlkou__btl = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            hlkou__btl, i) for i in range(1, hlkou__btl.type.count)], lir.
            IntType(64))
    zyomj__tcr, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if jphv__bxx:
        whx__msozi, ttfim__vwt, uxe__uhaf = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        hpn__osfzl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        ify__slkdl = cgutils.get_or_insert_function(c.builder.module,
            hpn__osfzl, name='struct_array_from_sequence')
        c.builder.call(ify__slkdl, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(whx__msozi, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(ttfim__vwt,
            lir.IntType(8).as_pointer()), c.builder.bitcast(uxe__uhaf, lir.
            IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    ytx__ffh = c.context.make_helper(c.builder, typ)
    ytx__ffh.meminfo = zyomj__tcr
    duu__uop = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ytx__ffh._getvalue(), is_error=duu__uop)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    uuow__zlyp = context.insert_const_string(builder.module, 'pandas')
    qono__gprhu = c.pyapi.import_module_noblock(uuow__zlyp)
    maf__zmdqp = c.pyapi.object_getattr_string(qono__gprhu, 'NA')
    with cgutils.for_range(builder, n_structs) as xhrud__vrx:
        hpg__igb = xhrud__vrx.index
        goec__aexfw = seq_getitem(builder, context, val, hpg__igb)
        set_bitmap_bit(builder, null_bitmap_ptr, hpg__igb, 0)
        for ghpup__xsv in range(len(typ.data)):
            arr_typ = typ.data[ghpup__xsv]
            data_arr = builder.extract_value(data_tup, ghpup__xsv)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            fhp__sar, rbl__ovgci = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, hpg__igb])
        nla__gtq = is_na_value(builder, context, goec__aexfw, maf__zmdqp)
        ymk__xmml = builder.icmp_unsigned('!=', nla__gtq, lir.Constant(
            nla__gtq.type, 1))
        with builder.if_then(ymk__xmml):
            set_bitmap_bit(builder, null_bitmap_ptr, hpg__igb, 1)
            for ghpup__xsv in range(len(typ.data)):
                arr_typ = typ.data[ghpup__xsv]
                if is_tuple_array:
                    xudqq__uzsv = c.pyapi.tuple_getitem(goec__aexfw, ghpup__xsv
                        )
                else:
                    xudqq__uzsv = c.pyapi.dict_getitem_string(goec__aexfw,
                        typ.names[ghpup__xsv])
                nla__gtq = is_na_value(builder, context, xudqq__uzsv,
                    maf__zmdqp)
                ymk__xmml = builder.icmp_unsigned('!=', nla__gtq, lir.
                    Constant(nla__gtq.type, 1))
                with builder.if_then(ymk__xmml):
                    xudqq__uzsv = to_arr_obj_if_list_obj(c, context,
                        builder, xudqq__uzsv, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        xudqq__uzsv).value
                    data_arr = builder.extract_value(data_tup, ghpup__xsv)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    fhp__sar, rbl__ovgci = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, hpg__igb, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(goec__aexfw)
    c.pyapi.decref(qono__gprhu)
    c.pyapi.decref(maf__zmdqp)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    ytx__ffh = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    vbrig__uurdf = context.nrt.meminfo_data(builder, ytx__ffh.meminfo)
    fyoq__hew = builder.bitcast(vbrig__uurdf, context.get_value_type(
        payload_type).as_pointer())
    lfqq__tvva = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(fyoq__hew))
    return lfqq__tvva


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    lfqq__tvva = _get_struct_arr_payload(c.context, c.builder, typ, val)
    fhp__sar, length = c.pyapi.call_jit_code(lambda A: len(A), types.int64(
        typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), lfqq__tvva.null_bitmap).data
    jphv__bxx = all(isinstance(lqvac__cbgs, types.Array) and (lqvac__cbgs.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(lqvac__cbgs.dtype, TimeType)) for
        lqvac__cbgs in typ.data)
    if jphv__bxx:
        whx__msozi, ttfim__vwt, uxe__uhaf = _get_C_API_ptrs(c, lfqq__tvva.
            data, typ.data, typ.names)
        hpn__osfzl = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        ske__uduwa = cgutils.get_or_insert_function(c.builder.module,
            hpn__osfzl, name='np_array_from_struct_array')
        arr = c.builder.call(ske__uduwa, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(whx__msozi, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            ttfim__vwt, lir.IntType(8).as_pointer()), c.builder.bitcast(
            uxe__uhaf, lir.IntType(8).as_pointer()), c.context.get_constant
            (types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, lfqq__tvva.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    uuow__zlyp = context.insert_const_string(builder.module, 'numpy')
    gqiu__wls = c.pyapi.import_module_noblock(uuow__zlyp)
    uqtjk__dkc = c.pyapi.object_getattr_string(gqiu__wls, 'object_')
    qdzrj__idtfk = c.pyapi.long_from_longlong(length)
    yuff__saksh = c.pyapi.call_method(gqiu__wls, 'ndarray', (qdzrj__idtfk,
        uqtjk__dkc))
    gju__yww = c.pyapi.object_getattr_string(gqiu__wls, 'nan')
    with cgutils.for_range(builder, length) as xhrud__vrx:
        hpg__igb = xhrud__vrx.index
        pyarray_setitem(builder, context, yuff__saksh, hpg__igb, gju__yww)
        dqarh__gdcrv = get_bitmap_bit(builder, null_bitmap_ptr, hpg__igb)
        dgw__agr = builder.icmp_unsigned('!=', dqarh__gdcrv, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(dgw__agr):
            if is_tuple_array:
                goec__aexfw = c.pyapi.tuple_new(len(typ.data))
            else:
                goec__aexfw = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(gju__yww)
                    c.pyapi.tuple_setitem(goec__aexfw, i, gju__yww)
                else:
                    c.pyapi.dict_setitem_string(goec__aexfw, typ.names[i],
                        gju__yww)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                fhp__sar, kwgi__ysd = c.pyapi.call_jit_code(lambda data_arr,
                    ind: not bodo.libs.array_kernels.isna(data_arr, ind),
                    types.bool_(arr_typ, types.int64), [data_arr, hpg__igb])
                with builder.if_then(kwgi__ysd):
                    fhp__sar, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, hpg__igb])
                    yfnfc__pyd = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(goec__aexfw, i, yfnfc__pyd)
                    else:
                        c.pyapi.dict_setitem_string(goec__aexfw, typ.names[
                            i], yfnfc__pyd)
                        c.pyapi.decref(yfnfc__pyd)
            pyarray_setitem(builder, context, yuff__saksh, hpg__igb,
                goec__aexfw)
            c.pyapi.decref(goec__aexfw)
    c.pyapi.decref(gqiu__wls)
    c.pyapi.decref(uqtjk__dkc)
    c.pyapi.decref(qdzrj__idtfk)
    c.pyapi.decref(gju__yww)
    return yuff__saksh


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    octv__sjhzi = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if octv__sjhzi == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for hdiy__iber in range(octv__sjhzi)])
    elif nested_counts_type.count < octv__sjhzi:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for hdiy__iber in range(
            octv__sjhzi - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(lqvac__cbgs) for lqvac__cbgs in
            names_typ.types)
    vtskn__zmkb = tuple(lqvac__cbgs.instance_type for lqvac__cbgs in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(vtskn__zmkb, names)

    def codegen(context, builder, sig, args):
        tja__ofjig, nested_counts, hdiy__iber, hdiy__iber = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        zyomj__tcr, hdiy__iber, hdiy__iber = construct_struct_array(context,
            builder, struct_arr_type, tja__ofjig, nested_counts)
        ytx__ffh = context.make_helper(builder, struct_arr_type)
        ytx__ffh.meminfo = zyomj__tcr
        return ytx__ffh._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(pkz__sleg, str) for
            pkz__sleg in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zhlc__duvhz = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, zhlc__duvhz)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        zhlc__duvhz = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, zhlc__duvhz)


def define_struct_dtor(context, builder, struct_type, payload_type):
    izt__qztwk = builder.module
    hpn__osfzl = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    ify__slkdl = cgutils.get_or_insert_function(izt__qztwk, hpn__osfzl,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not ify__slkdl.is_declaration:
        return ify__slkdl
    ify__slkdl.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(ify__slkdl.append_basic_block())
    ajkkw__xmw = ify__slkdl.args[0]
    xyz__iblg = context.get_value_type(payload_type).as_pointer()
    doxa__gzhra = builder.bitcast(ajkkw__xmw, xyz__iblg)
    lfqq__tvva = context.make_helper(builder, payload_type, ref=doxa__gzhra)
    for i in range(len(struct_type.data)):
        qjcn__ovjk = builder.extract_value(lfqq__tvva.null_bitmap, i)
        dgw__agr = builder.icmp_unsigned('==', qjcn__ovjk, lir.Constant(
            qjcn__ovjk.type, 1))
        with builder.if_then(dgw__agr):
            val = builder.extract_value(lfqq__tvva.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return ify__slkdl


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    vbrig__uurdf = context.nrt.meminfo_data(builder, struct.meminfo)
    fyoq__hew = builder.bitcast(vbrig__uurdf, context.get_value_type(
        payload_type).as_pointer())
    lfqq__tvva = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(fyoq__hew))
    return lfqq__tvva, fyoq__hew


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    uuow__zlyp = context.insert_const_string(builder.module, 'pandas')
    qono__gprhu = c.pyapi.import_module_noblock(uuow__zlyp)
    maf__zmdqp = c.pyapi.object_getattr_string(qono__gprhu, 'NA')
    nmot__tll = []
    nulls = []
    for i, lqvac__cbgs in enumerate(typ.data):
        yfnfc__pyd = c.pyapi.dict_getitem_string(val, typ.names[i])
        mfm__fqvfk = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        qbet__vpzs = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(lqvac__cbgs)))
        nla__gtq = is_na_value(builder, context, yfnfc__pyd, maf__zmdqp)
        dgw__agr = builder.icmp_unsigned('!=', nla__gtq, lir.Constant(
            nla__gtq.type, 1))
        with builder.if_then(dgw__agr):
            builder.store(context.get_constant(types.uint8, 1), mfm__fqvfk)
            field_val = c.pyapi.to_native_value(lqvac__cbgs, yfnfc__pyd).value
            builder.store(field_val, qbet__vpzs)
        nmot__tll.append(builder.load(qbet__vpzs))
        nulls.append(builder.load(mfm__fqvfk))
    c.pyapi.decref(qono__gprhu)
    c.pyapi.decref(maf__zmdqp)
    zyomj__tcr = construct_struct(context, builder, typ, nmot__tll, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = zyomj__tcr
    duu__uop = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=duu__uop)


@box(StructType)
def box_struct(typ, val, c):
    yoew__ggpts = c.pyapi.dict_new(len(typ.data))
    lfqq__tvva, hdiy__iber = _get_struct_payload(c.context, c.builder, typ, val
        )
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(yoew__ggpts, typ.names[i], c.pyapi.
            borrow_none())
        qjcn__ovjk = c.builder.extract_value(lfqq__tvva.null_bitmap, i)
        dgw__agr = c.builder.icmp_unsigned('==', qjcn__ovjk, lir.Constant(
            qjcn__ovjk.type, 1))
        with c.builder.if_then(dgw__agr):
            jrslv__tzdwh = c.builder.extract_value(lfqq__tvva.data, i)
            c.context.nrt.incref(c.builder, val_typ, jrslv__tzdwh)
            xudqq__uzsv = c.pyapi.from_native_value(val_typ, jrslv__tzdwh,
                c.env_manager)
            c.pyapi.dict_setitem_string(yoew__ggpts, typ.names[i], xudqq__uzsv)
            c.pyapi.decref(xudqq__uzsv)
    c.context.nrt.decref(c.builder, typ, val)
    return yoew__ggpts


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(lqvac__cbgs) for lqvac__cbgs in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, dxrsi__feojb = args
        payload_type = StructPayloadType(struct_type.data)
        rci__mzz = context.get_value_type(payload_type)
        cup__fdbe = context.get_abi_sizeof(rci__mzz)
        pwli__plt = define_struct_dtor(context, builder, struct_type,
            payload_type)
        zyomj__tcr = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, cup__fdbe), pwli__plt)
        vbrig__uurdf = context.nrt.meminfo_data(builder, zyomj__tcr)
        fyoq__hew = builder.bitcast(vbrig__uurdf, rci__mzz.as_pointer())
        lfqq__tvva = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        lfqq__tvva.data = data
        lfqq__tvva.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for hdiy__iber in range(len(
            data_typ.types))])
        builder.store(lfqq__tvva._getvalue(), fyoq__hew)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = zyomj__tcr
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        lfqq__tvva, hdiy__iber = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lfqq__tvva.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        lfqq__tvva, hdiy__iber = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lfqq__tvva.null_bitmap)
    sfyaf__yjver = types.UniTuple(types.int8, len(struct_typ.data))
    return sfyaf__yjver(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, hdiy__iber, val = args
        lfqq__tvva, fyoq__hew = _get_struct_payload(context, builder,
            struct_typ, struct)
        ltln__bsi = lfqq__tvva.data
        wrkf__evaam = builder.insert_value(ltln__bsi, val, field_ind)
        hrnv__omw = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, hrnv__omw, ltln__bsi)
        context.nrt.incref(builder, hrnv__omw, wrkf__evaam)
        lfqq__tvva.data = wrkf__evaam
        builder.store(lfqq__tvva._getvalue(), fyoq__hew)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    lehc__cxt = get_overload_const_str(ind)
    if lehc__cxt not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            lehc__cxt, struct))
    return struct.names.index(lehc__cxt)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    rci__mzz = context.get_value_type(payload_type)
    cup__fdbe = context.get_abi_sizeof(rci__mzz)
    pwli__plt = define_struct_dtor(context, builder, struct_type, payload_type)
    zyomj__tcr = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, cup__fdbe), pwli__plt)
    vbrig__uurdf = context.nrt.meminfo_data(builder, zyomj__tcr)
    fyoq__hew = builder.bitcast(vbrig__uurdf, rci__mzz.as_pointer())
    lfqq__tvva = cgutils.create_struct_proxy(payload_type)(context, builder)
    lfqq__tvva.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    lfqq__tvva.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(lfqq__tvva._getvalue(), fyoq__hew)
    return zyomj__tcr


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    uisl__scb = tuple(d.dtype for d in struct_arr_typ.data)
    ahy__prhtt = StructType(uisl__scb, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        mlpx__jiq, ind = args
        lfqq__tvva = _get_struct_arr_payload(context, builder,
            struct_arr_typ, mlpx__jiq)
        nmot__tll = []
        yszr__nwew = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            gnd__lmdag = builder.extract_value(lfqq__tvva.data, i)
            ucrb__wdorv = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [gnd__lmdag,
                ind])
            yszr__nwew.append(ucrb__wdorv)
            lab__ionlo = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            dgw__agr = builder.icmp_unsigned('==', ucrb__wdorv, lir.
                Constant(ucrb__wdorv.type, 1))
            with builder.if_then(dgw__agr):
                owhlj__htos = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    gnd__lmdag, ind])
                builder.store(owhlj__htos, lab__ionlo)
            nmot__tll.append(builder.load(lab__ionlo))
        if isinstance(ahy__prhtt, types.DictType):
            ikyv__mlil = [context.insert_const_string(builder.module,
                cmc__pvzg) for cmc__pvzg in struct_arr_typ.names]
            epv__grikb = cgutils.pack_array(builder, nmot__tll)
            tknm__lafny = cgutils.pack_array(builder, ikyv__mlil)

            def impl(names, vals):
                d = {}
                for i, cmc__pvzg in enumerate(names):
                    d[cmc__pvzg] = vals[i]
                return d
            ath__etiet = context.compile_internal(builder, impl, ahy__prhtt
                (types.Tuple(tuple(types.StringLiteral(cmc__pvzg) for
                cmc__pvzg in struct_arr_typ.names)), types.Tuple(uisl__scb)
                ), [tknm__lafny, epv__grikb])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                uisl__scb), epv__grikb)
            return ath__etiet
        zyomj__tcr = construct_struct(context, builder, ahy__prhtt,
            nmot__tll, yszr__nwew)
        struct = context.make_helper(builder, ahy__prhtt)
        struct.meminfo = zyomj__tcr
        return struct._getvalue()
    return ahy__prhtt(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lfqq__tvva = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lfqq__tvva.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lfqq__tvva = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lfqq__tvva.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(lqvac__cbgs) for lqvac__cbgs in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, zoo__ynb, dxrsi__feojb = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        rci__mzz = context.get_value_type(payload_type)
        cup__fdbe = context.get_abi_sizeof(rci__mzz)
        pwli__plt = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        zyomj__tcr = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, cup__fdbe), pwli__plt)
        vbrig__uurdf = context.nrt.meminfo_data(builder, zyomj__tcr)
        fyoq__hew = builder.bitcast(vbrig__uurdf, rci__mzz.as_pointer())
        lfqq__tvva = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        lfqq__tvva.data = data
        lfqq__tvva.null_bitmap = zoo__ynb
        builder.store(lfqq__tvva._getvalue(), fyoq__hew)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, zoo__ynb)
        ytx__ffh = context.make_helper(builder, struct_arr_type)
        ytx__ffh.meminfo = zyomj__tcr
        return ytx__ffh._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    if ind != bodo.boolean_array:
        ejm__gwrs = len(arr.data)
        ptwyw__pku = 'def impl(arr, ind):\n'
        ptwyw__pku += '  data = get_data(arr)\n'
        ptwyw__pku += '  null_bitmap = get_null_bitmap(arr)\n'
        if is_list_like_index_type(ind) and ind.dtype == types.bool_:
            ptwyw__pku += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
        elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.
            Integer):
            ptwyw__pku += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
        elif isinstance(ind, types.SliceType):
            ptwyw__pku += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
        else:
            raise BodoError('invalid index {} in struct array indexing'.
                format(ind))
        ptwyw__pku += (
            '  return init_struct_arr(({},), out_null_bitmap, ({},))\n'.
            format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
            i in range(ejm__gwrs)), ', '.join("'{}'".format(cmc__pvzg) for
            cmc__pvzg in arr.names)))
        cywm__mnbq = {}
        exec(ptwyw__pku, {'init_struct_arr': init_struct_arr, 'get_data':
            get_data, 'get_null_bitmap': get_null_bitmap,
            'ensure_contig_if_np': bodo.utils.conversion.
            ensure_contig_if_np, 'get_new_null_mask_bool_index': bodo.utils
            .indexing.get_new_null_mask_bool_index,
            'get_new_null_mask_int_index': bodo.utils.indexing.
            get_new_null_mask_int_index, 'get_new_null_mask_slice_index':
            bodo.utils.indexing.get_new_null_mask_slice_index}, cywm__mnbq)
        impl = cywm__mnbq['impl']
        return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        ejm__gwrs = len(arr.data)
        ptwyw__pku = 'def impl(arr, ind, val):\n'
        ptwyw__pku += '  data = get_data(arr)\n'
        ptwyw__pku += '  null_bitmap = get_null_bitmap(arr)\n'
        ptwyw__pku += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(ejm__gwrs):
            if isinstance(val, StructType):
                ptwyw__pku += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                ptwyw__pku += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                ptwyw__pku += '  else:\n'
                ptwyw__pku += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                ptwyw__pku += "  data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
        cywm__mnbq = {}
        exec(ptwyw__pku, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, cywm__mnbq)
        impl = cywm__mnbq['impl']
        return impl
    if isinstance(ind, types.SliceType):
        ejm__gwrs = len(arr.data)
        ptwyw__pku = 'def impl(arr, ind, val):\n'
        ptwyw__pku += '  data = get_data(arr)\n'
        ptwyw__pku += '  null_bitmap = get_null_bitmap(arr)\n'
        ptwyw__pku += '  val_data = get_data(val)\n'
        ptwyw__pku += '  val_null_bitmap = get_null_bitmap(val)\n'
        ptwyw__pku += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(ejm__gwrs):
            ptwyw__pku += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        cywm__mnbq = {}
        exec(ptwyw__pku, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, cywm__mnbq)
        impl = cywm__mnbq['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    ptwyw__pku = 'def impl(A):\n'
    ptwyw__pku += '  total_nbytes = 0\n'
    ptwyw__pku += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        ptwyw__pku += f'  total_nbytes += data[{i}].nbytes\n'
    ptwyw__pku += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    ptwyw__pku += '  return total_nbytes\n'
    cywm__mnbq = {}
    exec(ptwyw__pku, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, cywm__mnbq)
    impl = cywm__mnbq['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        zoo__ynb = get_null_bitmap(A)
        xasxd__pdcfn = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        jddh__bsyz = zoo__ynb.copy()
        return init_struct_arr(xasxd__pdcfn, jddh__bsyz, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(pkz__sleg.copy() for pkz__sleg in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    kowtv__jcdl = arrs.count
    ptwyw__pku = 'def f(arrs):\n'
    ptwyw__pku += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(kowtv__jcdl)))
    cywm__mnbq = {}
    exec(ptwyw__pku, {}, cywm__mnbq)
    impl = cywm__mnbq['f']
    return impl
