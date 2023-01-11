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
            .utils.is_array_typ(ivv__itupz, False) for ivv__itupz in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(ivv__itupz,
                str) for ivv__itupz in names) and len(names) == len(data)
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
        return StructType(tuple(blir__djzd.dtype for blir__djzd in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(ivv__itupz) for ivv__itupz in d.keys())
        data = tuple(dtype_to_array_type(blir__djzd) for blir__djzd in d.
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
            is_array_typ(ivv__itupz, False) for ivv__itupz in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pxiop__pud = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, pxiop__pud)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        pxiop__pud = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, pxiop__pud)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    wes__oyb = builder.module
    yrds__madik = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    dgka__uigb = cgutils.get_or_insert_function(wes__oyb, yrds__madik, name
        ='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not dgka__uigb.is_declaration:
        return dgka__uigb
    dgka__uigb.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(dgka__uigb.append_basic_block())
    cgije__mfih = dgka__uigb.args[0]
    akcu__une = context.get_value_type(payload_type).as_pointer()
    ldyz__jwcr = builder.bitcast(cgije__mfih, akcu__une)
    fmszr__hwt = context.make_helper(builder, payload_type, ref=ldyz__jwcr)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), fmszr__hwt.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        fmszr__hwt.null_bitmap)
    builder.ret_void()
    return dgka__uigb


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    pyu__jikl = context.get_value_type(payload_type)
    fvejw__pte = context.get_abi_sizeof(pyu__jikl)
    llsys__pxwa = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    qsq__pbyg = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, fvejw__pte), llsys__pxwa)
    hvueu__ane = context.nrt.meminfo_data(builder, qsq__pbyg)
    rgmg__nja = builder.bitcast(hvueu__ane, pyu__jikl.as_pointer())
    fmszr__hwt = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    tog__durum = 0
    for arr_typ in struct_arr_type.data:
        edk__qdil = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        ojylk__vsqd = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(tog__durum, tog__durum +
            edk__qdil)])
        arr = gen_allocate_array(context, builder, arr_typ, ojylk__vsqd, c)
        arrs.append(arr)
        tog__durum += edk__qdil
    fmszr__hwt.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    yxvk__wif = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    undpo__pcn = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [yxvk__wif])
    null_bitmap_ptr = undpo__pcn.data
    fmszr__hwt.null_bitmap = undpo__pcn._getvalue()
    builder.store(fmszr__hwt._getvalue(), rgmg__nja)
    return qsq__pbyg, fmszr__hwt.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    ira__sqn = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        fgbda__dghv = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            fgbda__dghv)
        ira__sqn.append(arr.data)
    svmul__jbbdt = cgutils.pack_array(c.builder, ira__sqn
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, ira__sqn)
    xafx__kqapl = cgutils.alloca_once_value(c.builder, svmul__jbbdt)
    tst__zbxz = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(ivv__itupz.dtype)) for ivv__itupz in data_typ]
    ppaqp__tnwd = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c
        .builder, tst__zbxz))
    gmy__piplc = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, ivv__itupz) for ivv__itupz in
        names])
    muosa__ltwap = cgutils.alloca_once_value(c.builder, gmy__piplc)
    return xafx__kqapl, ppaqp__tnwd, muosa__ltwap


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    iozl__ezu = all(isinstance(blir__djzd, types.Array) and (blir__djzd.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(blir__djzd.dtype, TimeType)) for
        blir__djzd in typ.data)
    if iozl__ezu:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        ifhlb__beu = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ifhlb__beu, i) for i in range(1, ifhlb__beu.type.count)], lir.
            IntType(64))
    qsq__pbyg, data_tup, null_bitmap_ptr = construct_struct_array(c.context,
        c.builder, typ, n_structs, n_elems, c)
    if iozl__ezu:
        xafx__kqapl, ppaqp__tnwd, muosa__ltwap = _get_C_API_ptrs(c,
            data_tup, typ.data, typ.names)
        yrds__madik = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        dgka__uigb = cgutils.get_or_insert_function(c.builder.module,
            yrds__madik, name='struct_array_from_sequence')
        c.builder.call(dgka__uigb, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(xafx__kqapl, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(ppaqp__tnwd,
            lir.IntType(8).as_pointer()), c.builder.bitcast(muosa__ltwap,
            lir.IntType(8).as_pointer()), c.context.get_constant(types.
            bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    eijc__dsdeq = c.context.make_helper(c.builder, typ)
    eijc__dsdeq.meminfo = qsq__pbyg
    xxrdm__gia = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(eijc__dsdeq._getvalue(), is_error=xxrdm__gia)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    qnhp__okktx = context.insert_const_string(builder.module, 'pandas')
    jya__xnbxv = c.pyapi.import_module_noblock(qnhp__okktx)
    gzr__nhvyw = c.pyapi.object_getattr_string(jya__xnbxv, 'NA')
    with cgutils.for_range(builder, n_structs) as ztd__qaa:
        ypx__ktco = ztd__qaa.index
        hpzhm__lmn = seq_getitem(builder, context, val, ypx__ktco)
        set_bitmap_bit(builder, null_bitmap_ptr, ypx__ktco, 0)
        for yzzs__mdkgd in range(len(typ.data)):
            arr_typ = typ.data[yzzs__mdkgd]
            data_arr = builder.extract_value(data_tup, yzzs__mdkgd)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            xdyeu__laar, cxq__fpt = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, ypx__ktco])
        clslp__mpbvz = is_na_value(builder, context, hpzhm__lmn, gzr__nhvyw)
        bbuh__unyxk = builder.icmp_unsigned('!=', clslp__mpbvz, lir.
            Constant(clslp__mpbvz.type, 1))
        with builder.if_then(bbuh__unyxk):
            set_bitmap_bit(builder, null_bitmap_ptr, ypx__ktco, 1)
            for yzzs__mdkgd in range(len(typ.data)):
                arr_typ = typ.data[yzzs__mdkgd]
                if is_tuple_array:
                    lfg__hjz = c.pyapi.tuple_getitem(hpzhm__lmn, yzzs__mdkgd)
                else:
                    lfg__hjz = c.pyapi.dict_getitem_string(hpzhm__lmn, typ.
                        names[yzzs__mdkgd])
                clslp__mpbvz = is_na_value(builder, context, lfg__hjz,
                    gzr__nhvyw)
                bbuh__unyxk = builder.icmp_unsigned('!=', clslp__mpbvz, lir
                    .Constant(clslp__mpbvz.type, 1))
                with builder.if_then(bbuh__unyxk):
                    lfg__hjz = to_arr_obj_if_list_obj(c, context, builder,
                        lfg__hjz, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype, lfg__hjz
                        ).value
                    data_arr = builder.extract_value(data_tup, yzzs__mdkgd)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    xdyeu__laar, cxq__fpt = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, ypx__ktco, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(hpzhm__lmn)
    c.pyapi.decref(jya__xnbxv)
    c.pyapi.decref(gzr__nhvyw)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    eijc__dsdeq = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    hvueu__ane = context.nrt.meminfo_data(builder, eijc__dsdeq.meminfo)
    rgmg__nja = builder.bitcast(hvueu__ane, context.get_value_type(
        payload_type).as_pointer())
    fmszr__hwt = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(rgmg__nja))
    return fmszr__hwt


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    fmszr__hwt = _get_struct_arr_payload(c.context, c.builder, typ, val)
    xdyeu__laar, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), fmszr__hwt.null_bitmap).data
    iozl__ezu = all(isinstance(blir__djzd, types.Array) and (blir__djzd.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(blir__djzd.dtype, TimeType)) for
        blir__djzd in typ.data)
    if iozl__ezu:
        xafx__kqapl, ppaqp__tnwd, muosa__ltwap = _get_C_API_ptrs(c,
            fmszr__hwt.data, typ.data, typ.names)
        yrds__madik = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        uxxcu__jxg = cgutils.get_or_insert_function(c.builder.module,
            yrds__madik, name='np_array_from_struct_array')
        arr = c.builder.call(uxxcu__jxg, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(xafx__kqapl, lir
            .IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            ppaqp__tnwd, lir.IntType(8).as_pointer()), c.builder.bitcast(
            muosa__ltwap, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, fmszr__hwt.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    qnhp__okktx = context.insert_const_string(builder.module, 'numpy')
    vwac__utv = c.pyapi.import_module_noblock(qnhp__okktx)
    gtvl__gudts = c.pyapi.object_getattr_string(vwac__utv, 'object_')
    jqozh__ksx = c.pyapi.long_from_longlong(length)
    lwol__wyd = c.pyapi.call_method(vwac__utv, 'ndarray', (jqozh__ksx,
        gtvl__gudts))
    luq__ecjl = c.pyapi.object_getattr_string(vwac__utv, 'nan')
    with cgutils.for_range(builder, length) as ztd__qaa:
        ypx__ktco = ztd__qaa.index
        pyarray_setitem(builder, context, lwol__wyd, ypx__ktco, luq__ecjl)
        hav__nyvuw = get_bitmap_bit(builder, null_bitmap_ptr, ypx__ktco)
        ggmp__lwpqs = builder.icmp_unsigned('!=', hav__nyvuw, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(ggmp__lwpqs):
            if is_tuple_array:
                hpzhm__lmn = c.pyapi.tuple_new(len(typ.data))
            else:
                hpzhm__lmn = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(luq__ecjl)
                    c.pyapi.tuple_setitem(hpzhm__lmn, i, luq__ecjl)
                else:
                    c.pyapi.dict_setitem_string(hpzhm__lmn, typ.names[i],
                        luq__ecjl)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                xdyeu__laar, tacpz__dmy = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, ypx__ktco])
                with builder.if_then(tacpz__dmy):
                    xdyeu__laar, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, ypx__ktco])
                    oykos__enkf = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(hpzhm__lmn, i, oykos__enkf)
                    else:
                        c.pyapi.dict_setitem_string(hpzhm__lmn, typ.names[i
                            ], oykos__enkf)
                        c.pyapi.decref(oykos__enkf)
            pyarray_setitem(builder, context, lwol__wyd, ypx__ktco, hpzhm__lmn)
            c.pyapi.decref(hpzhm__lmn)
    c.pyapi.decref(vwac__utv)
    c.pyapi.decref(gtvl__gudts)
    c.pyapi.decref(jqozh__ksx)
    c.pyapi.decref(luq__ecjl)
    return lwol__wyd


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    ralst__dsft = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if ralst__dsft == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for lvfnz__wpypf in range(ralst__dsft)])
    elif nested_counts_type.count < ralst__dsft:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for lvfnz__wpypf in range(
            ralst__dsft - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(blir__djzd) for blir__djzd in
            names_typ.types)
    tqbw__gllc = tuple(blir__djzd.instance_type for blir__djzd in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(tqbw__gllc, names)

    def codegen(context, builder, sig, args):
        maph__gaq, nested_counts, lvfnz__wpypf, lvfnz__wpypf = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        qsq__pbyg, lvfnz__wpypf, lvfnz__wpypf = construct_struct_array(context,
            builder, struct_arr_type, maph__gaq, nested_counts)
        eijc__dsdeq = context.make_helper(builder, struct_arr_type)
        eijc__dsdeq.meminfo = qsq__pbyg
        return eijc__dsdeq._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(ivv__itupz, str) for
            ivv__itupz in names) and len(names) == len(data)
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
        pxiop__pud = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, pxiop__pud)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        pxiop__pud = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, pxiop__pud)


def define_struct_dtor(context, builder, struct_type, payload_type):
    wes__oyb = builder.module
    yrds__madik = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    dgka__uigb = cgutils.get_or_insert_function(wes__oyb, yrds__madik, name
        ='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not dgka__uigb.is_declaration:
        return dgka__uigb
    dgka__uigb.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(dgka__uigb.append_basic_block())
    cgije__mfih = dgka__uigb.args[0]
    akcu__une = context.get_value_type(payload_type).as_pointer()
    ldyz__jwcr = builder.bitcast(cgije__mfih, akcu__une)
    fmszr__hwt = context.make_helper(builder, payload_type, ref=ldyz__jwcr)
    for i in range(len(struct_type.data)):
        slsys__agtpc = builder.extract_value(fmszr__hwt.null_bitmap, i)
        ggmp__lwpqs = builder.icmp_unsigned('==', slsys__agtpc, lir.
            Constant(slsys__agtpc.type, 1))
        with builder.if_then(ggmp__lwpqs):
            val = builder.extract_value(fmszr__hwt.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return dgka__uigb


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    hvueu__ane = context.nrt.meminfo_data(builder, struct.meminfo)
    rgmg__nja = builder.bitcast(hvueu__ane, context.get_value_type(
        payload_type).as_pointer())
    fmszr__hwt = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(rgmg__nja))
    return fmszr__hwt, rgmg__nja


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    qnhp__okktx = context.insert_const_string(builder.module, 'pandas')
    jya__xnbxv = c.pyapi.import_module_noblock(qnhp__okktx)
    gzr__nhvyw = c.pyapi.object_getattr_string(jya__xnbxv, 'NA')
    pet__ocu = []
    nulls = []
    for i, blir__djzd in enumerate(typ.data):
        oykos__enkf = c.pyapi.dict_getitem_string(val, typ.names[i])
        lqrys__uxco = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        uzsg__yjpv = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(blir__djzd)))
        clslp__mpbvz = is_na_value(builder, context, oykos__enkf, gzr__nhvyw)
        ggmp__lwpqs = builder.icmp_unsigned('!=', clslp__mpbvz, lir.
            Constant(clslp__mpbvz.type, 1))
        with builder.if_then(ggmp__lwpqs):
            builder.store(context.get_constant(types.uint8, 1), lqrys__uxco)
            field_val = c.pyapi.to_native_value(blir__djzd, oykos__enkf).value
            builder.store(field_val, uzsg__yjpv)
        pet__ocu.append(builder.load(uzsg__yjpv))
        nulls.append(builder.load(lqrys__uxco))
    c.pyapi.decref(jya__xnbxv)
    c.pyapi.decref(gzr__nhvyw)
    qsq__pbyg = construct_struct(context, builder, typ, pet__ocu, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = qsq__pbyg
    xxrdm__gia = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=xxrdm__gia)


@box(StructType)
def box_struct(typ, val, c):
    qkx__ghc = c.pyapi.dict_new(len(typ.data))
    fmszr__hwt, lvfnz__wpypf = _get_struct_payload(c.context, c.builder,
        typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(qkx__ghc, typ.names[i], c.pyapi.
            borrow_none())
        slsys__agtpc = c.builder.extract_value(fmszr__hwt.null_bitmap, i)
        ggmp__lwpqs = c.builder.icmp_unsigned('==', slsys__agtpc, lir.
            Constant(slsys__agtpc.type, 1))
        with c.builder.if_then(ggmp__lwpqs):
            auh__buk = c.builder.extract_value(fmszr__hwt.data, i)
            c.context.nrt.incref(c.builder, val_typ, auh__buk)
            lfg__hjz = c.pyapi.from_native_value(val_typ, auh__buk, c.
                env_manager)
            c.pyapi.dict_setitem_string(qkx__ghc, typ.names[i], lfg__hjz)
            c.pyapi.decref(lfg__hjz)
    c.context.nrt.decref(c.builder, typ, val)
    return qkx__ghc


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(blir__djzd) for blir__djzd in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, xph__gea = args
        payload_type = StructPayloadType(struct_type.data)
        pyu__jikl = context.get_value_type(payload_type)
        fvejw__pte = context.get_abi_sizeof(pyu__jikl)
        llsys__pxwa = define_struct_dtor(context, builder, struct_type,
            payload_type)
        qsq__pbyg = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, fvejw__pte), llsys__pxwa)
        hvueu__ane = context.nrt.meminfo_data(builder, qsq__pbyg)
        rgmg__nja = builder.bitcast(hvueu__ane, pyu__jikl.as_pointer())
        fmszr__hwt = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        fmszr__hwt.data = data
        fmszr__hwt.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for lvfnz__wpypf in range(len(
            data_typ.types))])
        builder.store(fmszr__hwt._getvalue(), rgmg__nja)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = qsq__pbyg
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        fmszr__hwt, lvfnz__wpypf = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            fmszr__hwt.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        fmszr__hwt, lvfnz__wpypf = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            fmszr__hwt.null_bitmap)
    aov__qnu = types.UniTuple(types.int8, len(struct_typ.data))
    return aov__qnu(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, lvfnz__wpypf, val = args
        fmszr__hwt, rgmg__nja = _get_struct_payload(context, builder,
            struct_typ, struct)
        dcuh__hikr = fmszr__hwt.data
        iljq__tvwby = builder.insert_value(dcuh__hikr, val, field_ind)
        kluow__uex = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, kluow__uex, dcuh__hikr)
        context.nrt.incref(builder, kluow__uex, iljq__tvwby)
        fmszr__hwt.data = iljq__tvwby
        builder.store(fmszr__hwt._getvalue(), rgmg__nja)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    teeg__yeu = get_overload_const_str(ind)
    if teeg__yeu not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            teeg__yeu, struct))
    return struct.names.index(teeg__yeu)


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
    pyu__jikl = context.get_value_type(payload_type)
    fvejw__pte = context.get_abi_sizeof(pyu__jikl)
    llsys__pxwa = define_struct_dtor(context, builder, struct_type,
        payload_type)
    qsq__pbyg = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, fvejw__pte), llsys__pxwa)
    hvueu__ane = context.nrt.meminfo_data(builder, qsq__pbyg)
    rgmg__nja = builder.bitcast(hvueu__ane, pyu__jikl.as_pointer())
    fmszr__hwt = cgutils.create_struct_proxy(payload_type)(context, builder)
    fmszr__hwt.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    fmszr__hwt.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(fmszr__hwt._getvalue(), rgmg__nja)
    return qsq__pbyg


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    uob__rqxf = tuple(d.dtype for d in struct_arr_typ.data)
    yvv__vopor = StructType(uob__rqxf, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        ygrsb__pxs, ind = args
        fmszr__hwt = _get_struct_arr_payload(context, builder,
            struct_arr_typ, ygrsb__pxs)
        pet__ocu = []
        lmv__qcdib = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            fgbda__dghv = builder.extract_value(fmszr__hwt.data, i)
            oray__sas = context.compile_internal(builder, lambda arr, ind: 
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [
                fgbda__dghv, ind])
            lmv__qcdib.append(oray__sas)
            hym__nvxn = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            ggmp__lwpqs = builder.icmp_unsigned('==', oray__sas, lir.
                Constant(oray__sas.type, 1))
            with builder.if_then(ggmp__lwpqs):
                esoh__fzy = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    fgbda__dghv, ind])
                builder.store(esoh__fzy, hym__nvxn)
            pet__ocu.append(builder.load(hym__nvxn))
        if isinstance(yvv__vopor, types.DictType):
            kmff__noshv = [context.insert_const_string(builder.module,
                hpmkr__wilp) for hpmkr__wilp in struct_arr_typ.names]
            gmuo__icvks = cgutils.pack_array(builder, pet__ocu)
            tsypv__dycjr = cgutils.pack_array(builder, kmff__noshv)

            def impl(names, vals):
                d = {}
                for i, hpmkr__wilp in enumerate(names):
                    d[hpmkr__wilp] = vals[i]
                return d
            ibg__rzl = context.compile_internal(builder, impl, yvv__vopor(
                types.Tuple(tuple(types.StringLiteral(hpmkr__wilp) for
                hpmkr__wilp in struct_arr_typ.names)), types.Tuple(
                uob__rqxf)), [tsypv__dycjr, gmuo__icvks])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                uob__rqxf), gmuo__icvks)
            return ibg__rzl
        qsq__pbyg = construct_struct(context, builder, yvv__vopor, pet__ocu,
            lmv__qcdib)
        struct = context.make_helper(builder, yvv__vopor)
        struct.meminfo = qsq__pbyg
        return struct._getvalue()
    return yvv__vopor(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        fmszr__hwt = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            fmszr__hwt.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        fmszr__hwt = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            fmszr__hwt.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(blir__djzd) for blir__djzd in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, undpo__pcn, xph__gea = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        pyu__jikl = context.get_value_type(payload_type)
        fvejw__pte = context.get_abi_sizeof(pyu__jikl)
        llsys__pxwa = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        qsq__pbyg = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, fvejw__pte), llsys__pxwa)
        hvueu__ane = context.nrt.meminfo_data(builder, qsq__pbyg)
        rgmg__nja = builder.bitcast(hvueu__ane, pyu__jikl.as_pointer())
        fmszr__hwt = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        fmszr__hwt.data = data
        fmszr__hwt.null_bitmap = undpo__pcn
        builder.store(fmszr__hwt._getvalue(), rgmg__nja)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, undpo__pcn)
        eijc__dsdeq = context.make_helper(builder, struct_arr_type)
        eijc__dsdeq.meminfo = qsq__pbyg
        return eijc__dsdeq._getvalue()
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
        jjwu__lpaao = len(arr.data)
        qug__rjxrs = 'def impl(arr, ind):\n'
        qug__rjxrs += '  data = get_data(arr)\n'
        qug__rjxrs += '  null_bitmap = get_null_bitmap(arr)\n'
        if is_list_like_index_type(ind) and ind.dtype == types.bool_:
            qug__rjxrs += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
        elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.
            Integer):
            qug__rjxrs += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
        elif isinstance(ind, types.SliceType):
            qug__rjxrs += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
        else:
            raise BodoError('invalid index {} in struct array indexing'.
                format(ind))
        qug__rjxrs += (
            '  return init_struct_arr(({},), out_null_bitmap, ({},))\n'.
            format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
            i in range(jjwu__lpaao)), ', '.join("'{}'".format(hpmkr__wilp) for
            hpmkr__wilp in arr.names)))
        ofowg__anihn = {}
        exec(qug__rjxrs, {'init_struct_arr': init_struct_arr, 'get_data':
            get_data, 'get_null_bitmap': get_null_bitmap,
            'ensure_contig_if_np': bodo.utils.conversion.
            ensure_contig_if_np, 'get_new_null_mask_bool_index': bodo.utils
            .indexing.get_new_null_mask_bool_index,
            'get_new_null_mask_int_index': bodo.utils.indexing.
            get_new_null_mask_int_index, 'get_new_null_mask_slice_index':
            bodo.utils.indexing.get_new_null_mask_slice_index}, ofowg__anihn)
        impl = ofowg__anihn['impl']
        return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        jjwu__lpaao = len(arr.data)
        qug__rjxrs = 'def impl(arr, ind, val):\n'
        qug__rjxrs += '  data = get_data(arr)\n'
        qug__rjxrs += '  null_bitmap = get_null_bitmap(arr)\n'
        qug__rjxrs += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(jjwu__lpaao):
            if isinstance(val, StructType):
                qug__rjxrs += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                qug__rjxrs += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                qug__rjxrs += '  else:\n'
                qug__rjxrs += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                qug__rjxrs += "  data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
        ofowg__anihn = {}
        exec(qug__rjxrs, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, ofowg__anihn)
        impl = ofowg__anihn['impl']
        return impl
    if isinstance(ind, types.SliceType):
        jjwu__lpaao = len(arr.data)
        qug__rjxrs = 'def impl(arr, ind, val):\n'
        qug__rjxrs += '  data = get_data(arr)\n'
        qug__rjxrs += '  null_bitmap = get_null_bitmap(arr)\n'
        qug__rjxrs += '  val_data = get_data(val)\n'
        qug__rjxrs += '  val_null_bitmap = get_null_bitmap(val)\n'
        qug__rjxrs += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(jjwu__lpaao):
            qug__rjxrs += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        ofowg__anihn = {}
        exec(qug__rjxrs, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, ofowg__anihn)
        impl = ofowg__anihn['impl']
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
    qug__rjxrs = 'def impl(A):\n'
    qug__rjxrs += '  total_nbytes = 0\n'
    qug__rjxrs += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        qug__rjxrs += f'  total_nbytes += data[{i}].nbytes\n'
    qug__rjxrs += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    qug__rjxrs += '  return total_nbytes\n'
    ofowg__anihn = {}
    exec(qug__rjxrs, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, ofowg__anihn)
    impl = ofowg__anihn['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        undpo__pcn = get_null_bitmap(A)
        ofa__xdkz = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        fnqa__rczf = undpo__pcn.copy()
        return init_struct_arr(ofa__xdkz, fnqa__rczf, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(ivv__itupz.copy() for ivv__itupz in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    nvldj__fpq = arrs.count
    qug__rjxrs = 'def f(arrs):\n'
    qug__rjxrs += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(nvldj__fpq)))
    ofowg__anihn = {}
    exec(qug__rjxrs, {}, ofowg__anihn)
    impl = ofowg__anihn['f']
    return impl
