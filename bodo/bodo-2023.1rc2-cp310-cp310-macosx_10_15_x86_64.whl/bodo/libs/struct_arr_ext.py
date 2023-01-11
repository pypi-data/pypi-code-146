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
            .utils.is_array_typ(wttb__nsteh, False) for wttb__nsteh in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(wttb__nsteh,
                str) for wttb__nsteh in names) and len(names) == len(data)
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
        return StructType(tuple(cxvi__pengl.dtype for cxvi__pengl in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(wttb__nsteh) for wttb__nsteh in d.keys())
        data = tuple(dtype_to_array_type(cxvi__pengl) for cxvi__pengl in d.
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
            is_array_typ(wttb__nsteh, False) for wttb__nsteh in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ijikr__tlzh = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ijikr__tlzh)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        ijikr__tlzh = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ijikr__tlzh)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    gvcyw__zrb = builder.module
    hvkdk__qwhpv = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    guxlc__lyhkp = cgutils.get_or_insert_function(gvcyw__zrb, hvkdk__qwhpv,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not guxlc__lyhkp.is_declaration:
        return guxlc__lyhkp
    guxlc__lyhkp.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(guxlc__lyhkp.append_basic_block())
    foynj__lpkux = guxlc__lyhkp.args[0]
    syrfl__tdtyn = context.get_value_type(payload_type).as_pointer()
    ebhjf__vfi = builder.bitcast(foynj__lpkux, syrfl__tdtyn)
    nyti__cvkp = context.make_helper(builder, payload_type, ref=ebhjf__vfi)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), nyti__cvkp.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        nyti__cvkp.null_bitmap)
    builder.ret_void()
    return guxlc__lyhkp


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    enb__fzm = context.get_value_type(payload_type)
    pawlp__xdxde = context.get_abi_sizeof(enb__fzm)
    tuj__pgtfo = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    rue__bsmj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, pawlp__xdxde), tuj__pgtfo)
    gtjtq__lkw = context.nrt.meminfo_data(builder, rue__bsmj)
    oevkp__jmtsv = builder.bitcast(gtjtq__lkw, enb__fzm.as_pointer())
    nyti__cvkp = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    ewwi__pwn = 0
    for arr_typ in struct_arr_type.data:
        vffo__rpirg = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        sqfz__ces = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(ewwi__pwn, ewwi__pwn +
            vffo__rpirg)])
        arr = gen_allocate_array(context, builder, arr_typ, sqfz__ces, c)
        arrs.append(arr)
        ewwi__pwn += vffo__rpirg
    nyti__cvkp.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    lig__bma = builder.udiv(builder.add(n_structs, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    bqc__cwrg = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [lig__bma])
    null_bitmap_ptr = bqc__cwrg.data
    nyti__cvkp.null_bitmap = bqc__cwrg._getvalue()
    builder.store(nyti__cvkp._getvalue(), oevkp__jmtsv)
    return rue__bsmj, nyti__cvkp.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    upefy__gzylk = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        uiexl__tyesx = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            uiexl__tyesx)
        upefy__gzylk.append(arr.data)
    cuvq__uhi = cgutils.pack_array(c.builder, upefy__gzylk
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, upefy__gzylk)
    muh__ikka = cgutils.alloca_once_value(c.builder, cuvq__uhi)
    vfdjh__xltk = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(wttb__nsteh.dtype)) for wttb__nsteh in data_typ]
    jxaeu__hpj = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, vfdjh__xltk))
    hfudl__ngsb = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, wttb__nsteh) for wttb__nsteh in
        names])
    mzdgg__jmiw = cgutils.alloca_once_value(c.builder, hfudl__ngsb)
    return muh__ikka, jxaeu__hpj, mzdgg__jmiw


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    pqx__qwve = all(isinstance(cxvi__pengl, types.Array) and (cxvi__pengl.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(cxvi__pengl.dtype, TimeType)) for
        cxvi__pengl in typ.data)
    if pqx__qwve:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        uyj__ntseq = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            uyj__ntseq, i) for i in range(1, uyj__ntseq.type.count)], lir.
            IntType(64))
    rue__bsmj, data_tup, null_bitmap_ptr = construct_struct_array(c.context,
        c.builder, typ, n_structs, n_elems, c)
    if pqx__qwve:
        muh__ikka, jxaeu__hpj, mzdgg__jmiw = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        hvkdk__qwhpv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        guxlc__lyhkp = cgutils.get_or_insert_function(c.builder.module,
            hvkdk__qwhpv, name='struct_array_from_sequence')
        c.builder.call(guxlc__lyhkp, [val, c.context.get_constant(types.
            int32, len(typ.data)), c.builder.bitcast(muh__ikka, lir.IntType
            (8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            jxaeu__hpj, lir.IntType(8).as_pointer()), c.builder.bitcast(
            mzdgg__jmiw, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    crmor__zag = c.context.make_helper(c.builder, typ)
    crmor__zag.meminfo = rue__bsmj
    eken__yitu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(crmor__zag._getvalue(), is_error=eken__yitu)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    wnz__bpiso = context.insert_const_string(builder.module, 'pandas')
    gztc__dguj = c.pyapi.import_module_noblock(wnz__bpiso)
    moo__mobnu = c.pyapi.object_getattr_string(gztc__dguj, 'NA')
    with cgutils.for_range(builder, n_structs) as ntrg__jrgv:
        xbbgw__gya = ntrg__jrgv.index
        ioxtt__uylun = seq_getitem(builder, context, val, xbbgw__gya)
        set_bitmap_bit(builder, null_bitmap_ptr, xbbgw__gya, 0)
        for vrvo__fvho in range(len(typ.data)):
            arr_typ = typ.data[vrvo__fvho]
            data_arr = builder.extract_value(data_tup, vrvo__fvho)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            jbbwm__wdo, tvqud__cia = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, xbbgw__gya])
        iethq__sxbx = is_na_value(builder, context, ioxtt__uylun, moo__mobnu)
        vqz__ksw = builder.icmp_unsigned('!=', iethq__sxbx, lir.Constant(
            iethq__sxbx.type, 1))
        with builder.if_then(vqz__ksw):
            set_bitmap_bit(builder, null_bitmap_ptr, xbbgw__gya, 1)
            for vrvo__fvho in range(len(typ.data)):
                arr_typ = typ.data[vrvo__fvho]
                if is_tuple_array:
                    dvjge__yxi = c.pyapi.tuple_getitem(ioxtt__uylun, vrvo__fvho
                        )
                else:
                    dvjge__yxi = c.pyapi.dict_getitem_string(ioxtt__uylun,
                        typ.names[vrvo__fvho])
                iethq__sxbx = is_na_value(builder, context, dvjge__yxi,
                    moo__mobnu)
                vqz__ksw = builder.icmp_unsigned('!=', iethq__sxbx, lir.
                    Constant(iethq__sxbx.type, 1))
                with builder.if_then(vqz__ksw):
                    dvjge__yxi = to_arr_obj_if_list_obj(c, context, builder,
                        dvjge__yxi, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        dvjge__yxi).value
                    data_arr = builder.extract_value(data_tup, vrvo__fvho)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    jbbwm__wdo, tvqud__cia = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, xbbgw__gya, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(ioxtt__uylun)
    c.pyapi.decref(gztc__dguj)
    c.pyapi.decref(moo__mobnu)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    crmor__zag = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    gtjtq__lkw = context.nrt.meminfo_data(builder, crmor__zag.meminfo)
    oevkp__jmtsv = builder.bitcast(gtjtq__lkw, context.get_value_type(
        payload_type).as_pointer())
    nyti__cvkp = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(oevkp__jmtsv))
    return nyti__cvkp


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    nyti__cvkp = _get_struct_arr_payload(c.context, c.builder, typ, val)
    jbbwm__wdo, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), nyti__cvkp.null_bitmap).data
    pqx__qwve = all(isinstance(cxvi__pengl, types.Array) and (cxvi__pengl.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(cxvi__pengl.dtype, TimeType)) for
        cxvi__pengl in typ.data)
    if pqx__qwve:
        muh__ikka, jxaeu__hpj, mzdgg__jmiw = _get_C_API_ptrs(c, nyti__cvkp.
            data, typ.data, typ.names)
        hvkdk__qwhpv = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        gxbqa__vrec = cgutils.get_or_insert_function(c.builder.module,
            hvkdk__qwhpv, name='np_array_from_struct_array')
        arr = c.builder.call(gxbqa__vrec, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(muh__ikka, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            jxaeu__hpj, lir.IntType(8).as_pointer()), c.builder.bitcast(
            mzdgg__jmiw, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, nyti__cvkp.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    wnz__bpiso = context.insert_const_string(builder.module, 'numpy')
    gnotb__ruo = c.pyapi.import_module_noblock(wnz__bpiso)
    iwr__cdxa = c.pyapi.object_getattr_string(gnotb__ruo, 'object_')
    cnfcy__kui = c.pyapi.long_from_longlong(length)
    acsp__jeqd = c.pyapi.call_method(gnotb__ruo, 'ndarray', (cnfcy__kui,
        iwr__cdxa))
    npb__surx = c.pyapi.object_getattr_string(gnotb__ruo, 'nan')
    with cgutils.for_range(builder, length) as ntrg__jrgv:
        xbbgw__gya = ntrg__jrgv.index
        pyarray_setitem(builder, context, acsp__jeqd, xbbgw__gya, npb__surx)
        fbrrh__oivid = get_bitmap_bit(builder, null_bitmap_ptr, xbbgw__gya)
        jwj__evou = builder.icmp_unsigned('!=', fbrrh__oivid, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(jwj__evou):
            if is_tuple_array:
                ioxtt__uylun = c.pyapi.tuple_new(len(typ.data))
            else:
                ioxtt__uylun = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(npb__surx)
                    c.pyapi.tuple_setitem(ioxtt__uylun, i, npb__surx)
                else:
                    c.pyapi.dict_setitem_string(ioxtt__uylun, typ.names[i],
                        npb__surx)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                jbbwm__wdo, jvf__dvx = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, xbbgw__gya])
                with builder.if_then(jvf__dvx):
                    jbbwm__wdo, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, xbbgw__gya])
                    yxnby__refu = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(ioxtt__uylun, i, yxnby__refu)
                    else:
                        c.pyapi.dict_setitem_string(ioxtt__uylun, typ.names
                            [i], yxnby__refu)
                        c.pyapi.decref(yxnby__refu)
            pyarray_setitem(builder, context, acsp__jeqd, xbbgw__gya,
                ioxtt__uylun)
            c.pyapi.decref(ioxtt__uylun)
    c.pyapi.decref(gnotb__ruo)
    c.pyapi.decref(iwr__cdxa)
    c.pyapi.decref(cnfcy__kui)
    c.pyapi.decref(npb__surx)
    return acsp__jeqd


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    slay__lekl = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if slay__lekl == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for gturz__rijk in range(slay__lekl)])
    elif nested_counts_type.count < slay__lekl:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for gturz__rijk in range(
            slay__lekl - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(cxvi__pengl) for cxvi__pengl in
            names_typ.types)
    gvbk__xffo = tuple(cxvi__pengl.instance_type for cxvi__pengl in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(gvbk__xffo, names)

    def codegen(context, builder, sig, args):
        qxcz__dttw, nested_counts, gturz__rijk, gturz__rijk = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        rue__bsmj, gturz__rijk, gturz__rijk = construct_struct_array(context,
            builder, struct_arr_type, qxcz__dttw, nested_counts)
        crmor__zag = context.make_helper(builder, struct_arr_type)
        crmor__zag.meminfo = rue__bsmj
        return crmor__zag._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(wttb__nsteh, str
            ) for wttb__nsteh in names) and len(names) == len(data)
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
        ijikr__tlzh = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, ijikr__tlzh)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        ijikr__tlzh = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ijikr__tlzh)


def define_struct_dtor(context, builder, struct_type, payload_type):
    gvcyw__zrb = builder.module
    hvkdk__qwhpv = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    guxlc__lyhkp = cgutils.get_or_insert_function(gvcyw__zrb, hvkdk__qwhpv,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not guxlc__lyhkp.is_declaration:
        return guxlc__lyhkp
    guxlc__lyhkp.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(guxlc__lyhkp.append_basic_block())
    foynj__lpkux = guxlc__lyhkp.args[0]
    syrfl__tdtyn = context.get_value_type(payload_type).as_pointer()
    ebhjf__vfi = builder.bitcast(foynj__lpkux, syrfl__tdtyn)
    nyti__cvkp = context.make_helper(builder, payload_type, ref=ebhjf__vfi)
    for i in range(len(struct_type.data)):
        tab__pwezq = builder.extract_value(nyti__cvkp.null_bitmap, i)
        jwj__evou = builder.icmp_unsigned('==', tab__pwezq, lir.Constant(
            tab__pwezq.type, 1))
        with builder.if_then(jwj__evou):
            val = builder.extract_value(nyti__cvkp.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return guxlc__lyhkp


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    gtjtq__lkw = context.nrt.meminfo_data(builder, struct.meminfo)
    oevkp__jmtsv = builder.bitcast(gtjtq__lkw, context.get_value_type(
        payload_type).as_pointer())
    nyti__cvkp = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(oevkp__jmtsv))
    return nyti__cvkp, oevkp__jmtsv


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    wnz__bpiso = context.insert_const_string(builder.module, 'pandas')
    gztc__dguj = c.pyapi.import_module_noblock(wnz__bpiso)
    moo__mobnu = c.pyapi.object_getattr_string(gztc__dguj, 'NA')
    dfu__ujdj = []
    nulls = []
    for i, cxvi__pengl in enumerate(typ.data):
        yxnby__refu = c.pyapi.dict_getitem_string(val, typ.names[i])
        jkisj__zqg = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        sdkv__aykpv = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(cxvi__pengl)))
        iethq__sxbx = is_na_value(builder, context, yxnby__refu, moo__mobnu)
        jwj__evou = builder.icmp_unsigned('!=', iethq__sxbx, lir.Constant(
            iethq__sxbx.type, 1))
        with builder.if_then(jwj__evou):
            builder.store(context.get_constant(types.uint8, 1), jkisj__zqg)
            field_val = c.pyapi.to_native_value(cxvi__pengl, yxnby__refu).value
            builder.store(field_val, sdkv__aykpv)
        dfu__ujdj.append(builder.load(sdkv__aykpv))
        nulls.append(builder.load(jkisj__zqg))
    c.pyapi.decref(gztc__dguj)
    c.pyapi.decref(moo__mobnu)
    rue__bsmj = construct_struct(context, builder, typ, dfu__ujdj, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = rue__bsmj
    eken__yitu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=eken__yitu)


@box(StructType)
def box_struct(typ, val, c):
    nmj__fnx = c.pyapi.dict_new(len(typ.data))
    nyti__cvkp, gturz__rijk = _get_struct_payload(c.context, c.builder, typ,
        val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(nmj__fnx, typ.names[i], c.pyapi.
            borrow_none())
        tab__pwezq = c.builder.extract_value(nyti__cvkp.null_bitmap, i)
        jwj__evou = c.builder.icmp_unsigned('==', tab__pwezq, lir.Constant(
            tab__pwezq.type, 1))
        with c.builder.if_then(jwj__evou):
            gsljf__cgsk = c.builder.extract_value(nyti__cvkp.data, i)
            c.context.nrt.incref(c.builder, val_typ, gsljf__cgsk)
            dvjge__yxi = c.pyapi.from_native_value(val_typ, gsljf__cgsk, c.
                env_manager)
            c.pyapi.dict_setitem_string(nmj__fnx, typ.names[i], dvjge__yxi)
            c.pyapi.decref(dvjge__yxi)
    c.context.nrt.decref(c.builder, typ, val)
    return nmj__fnx


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(cxvi__pengl) for cxvi__pengl in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, utbpk__wlggn = args
        payload_type = StructPayloadType(struct_type.data)
        enb__fzm = context.get_value_type(payload_type)
        pawlp__xdxde = context.get_abi_sizeof(enb__fzm)
        tuj__pgtfo = define_struct_dtor(context, builder, struct_type,
            payload_type)
        rue__bsmj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, pawlp__xdxde), tuj__pgtfo)
        gtjtq__lkw = context.nrt.meminfo_data(builder, rue__bsmj)
        oevkp__jmtsv = builder.bitcast(gtjtq__lkw, enb__fzm.as_pointer())
        nyti__cvkp = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        nyti__cvkp.data = data
        nyti__cvkp.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for gturz__rijk in range(len(
            data_typ.types))])
        builder.store(nyti__cvkp._getvalue(), oevkp__jmtsv)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = rue__bsmj
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        nyti__cvkp, gturz__rijk = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            nyti__cvkp.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        nyti__cvkp, gturz__rijk = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            nyti__cvkp.null_bitmap)
    leglx__jwx = types.UniTuple(types.int8, len(struct_typ.data))
    return leglx__jwx(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, gturz__rijk, val = args
        nyti__cvkp, oevkp__jmtsv = _get_struct_payload(context, builder,
            struct_typ, struct)
        trs__dnxv = nyti__cvkp.data
        zwqkw__xyxp = builder.insert_value(trs__dnxv, val, field_ind)
        glg__vgptm = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, glg__vgptm, trs__dnxv)
        context.nrt.incref(builder, glg__vgptm, zwqkw__xyxp)
        nyti__cvkp.data = zwqkw__xyxp
        builder.store(nyti__cvkp._getvalue(), oevkp__jmtsv)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    bnksh__ordf = get_overload_const_str(ind)
    if bnksh__ordf not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            bnksh__ordf, struct))
    return struct.names.index(bnksh__ordf)


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
    enb__fzm = context.get_value_type(payload_type)
    pawlp__xdxde = context.get_abi_sizeof(enb__fzm)
    tuj__pgtfo = define_struct_dtor(context, builder, struct_type, payload_type
        )
    rue__bsmj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, pawlp__xdxde), tuj__pgtfo)
    gtjtq__lkw = context.nrt.meminfo_data(builder, rue__bsmj)
    oevkp__jmtsv = builder.bitcast(gtjtq__lkw, enb__fzm.as_pointer())
    nyti__cvkp = cgutils.create_struct_proxy(payload_type)(context, builder)
    nyti__cvkp.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    nyti__cvkp.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(nyti__cvkp._getvalue(), oevkp__jmtsv)
    return rue__bsmj


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    hpfjj__iugte = tuple(d.dtype for d in struct_arr_typ.data)
    ictw__bkcs = StructType(hpfjj__iugte, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        mfoee__gkg, ind = args
        nyti__cvkp = _get_struct_arr_payload(context, builder,
            struct_arr_typ, mfoee__gkg)
        dfu__ujdj = []
        zsts__wsv = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            uiexl__tyesx = builder.extract_value(nyti__cvkp.data, i)
            gcx__ulg = context.compile_internal(builder, lambda arr, ind: 
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [
                uiexl__tyesx, ind])
            zsts__wsv.append(gcx__ulg)
            xepi__lhnak = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            jwj__evou = builder.icmp_unsigned('==', gcx__ulg, lir.Constant(
                gcx__ulg.type, 1))
            with builder.if_then(jwj__evou):
                bzbr__odxza = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    uiexl__tyesx, ind])
                builder.store(bzbr__odxza, xepi__lhnak)
            dfu__ujdj.append(builder.load(xepi__lhnak))
        if isinstance(ictw__bkcs, types.DictType):
            dhfec__ium = [context.insert_const_string(builder.module,
                wtn__pbwdq) for wtn__pbwdq in struct_arr_typ.names]
            ujax__zfsy = cgutils.pack_array(builder, dfu__ujdj)
            vqjx__xtcsd = cgutils.pack_array(builder, dhfec__ium)

            def impl(names, vals):
                d = {}
                for i, wtn__pbwdq in enumerate(names):
                    d[wtn__pbwdq] = vals[i]
                return d
            qfs__pglvl = context.compile_internal(builder, impl, ictw__bkcs
                (types.Tuple(tuple(types.StringLiteral(wtn__pbwdq) for
                wtn__pbwdq in struct_arr_typ.names)), types.Tuple(
                hpfjj__iugte)), [vqjx__xtcsd, ujax__zfsy])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                hpfjj__iugte), ujax__zfsy)
            return qfs__pglvl
        rue__bsmj = construct_struct(context, builder, ictw__bkcs,
            dfu__ujdj, zsts__wsv)
        struct = context.make_helper(builder, ictw__bkcs)
        struct.meminfo = rue__bsmj
        return struct._getvalue()
    return ictw__bkcs(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        nyti__cvkp = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            nyti__cvkp.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        nyti__cvkp = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            nyti__cvkp.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(cxvi__pengl) for cxvi__pengl in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, bqc__cwrg, utbpk__wlggn = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        enb__fzm = context.get_value_type(payload_type)
        pawlp__xdxde = context.get_abi_sizeof(enb__fzm)
        tuj__pgtfo = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        rue__bsmj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, pawlp__xdxde), tuj__pgtfo)
        gtjtq__lkw = context.nrt.meminfo_data(builder, rue__bsmj)
        oevkp__jmtsv = builder.bitcast(gtjtq__lkw, enb__fzm.as_pointer())
        nyti__cvkp = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        nyti__cvkp.data = data
        nyti__cvkp.null_bitmap = bqc__cwrg
        builder.store(nyti__cvkp._getvalue(), oevkp__jmtsv)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, bqc__cwrg)
        crmor__zag = context.make_helper(builder, struct_arr_type)
        crmor__zag.meminfo = rue__bsmj
        return crmor__zag._getvalue()
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
        kucpz__svzfj = len(arr.data)
        idxu__vqht = 'def impl(arr, ind):\n'
        idxu__vqht += '  data = get_data(arr)\n'
        idxu__vqht += '  null_bitmap = get_null_bitmap(arr)\n'
        if is_list_like_index_type(ind) and ind.dtype == types.bool_:
            idxu__vqht += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
        elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.
            Integer):
            idxu__vqht += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
        elif isinstance(ind, types.SliceType):
            idxu__vqht += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
        else:
            raise BodoError('invalid index {} in struct array indexing'.
                format(ind))
        idxu__vqht += (
            '  return init_struct_arr(({},), out_null_bitmap, ({},))\n'.
            format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
            i in range(kucpz__svzfj)), ', '.join("'{}'".format(wtn__pbwdq) for
            wtn__pbwdq in arr.names)))
        rjqr__znggy = {}
        exec(idxu__vqht, {'init_struct_arr': init_struct_arr, 'get_data':
            get_data, 'get_null_bitmap': get_null_bitmap,
            'ensure_contig_if_np': bodo.utils.conversion.
            ensure_contig_if_np, 'get_new_null_mask_bool_index': bodo.utils
            .indexing.get_new_null_mask_bool_index,
            'get_new_null_mask_int_index': bodo.utils.indexing.
            get_new_null_mask_int_index, 'get_new_null_mask_slice_index':
            bodo.utils.indexing.get_new_null_mask_slice_index}, rjqr__znggy)
        impl = rjqr__znggy['impl']
        return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        kucpz__svzfj = len(arr.data)
        idxu__vqht = 'def impl(arr, ind, val):\n'
        idxu__vqht += '  data = get_data(arr)\n'
        idxu__vqht += '  null_bitmap = get_null_bitmap(arr)\n'
        idxu__vqht += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(kucpz__svzfj):
            if isinstance(val, StructType):
                idxu__vqht += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                idxu__vqht += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                idxu__vqht += '  else:\n'
                idxu__vqht += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                idxu__vqht += "  data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
        rjqr__znggy = {}
        exec(idxu__vqht, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, rjqr__znggy)
        impl = rjqr__znggy['impl']
        return impl
    if isinstance(ind, types.SliceType):
        kucpz__svzfj = len(arr.data)
        idxu__vqht = 'def impl(arr, ind, val):\n'
        idxu__vqht += '  data = get_data(arr)\n'
        idxu__vqht += '  null_bitmap = get_null_bitmap(arr)\n'
        idxu__vqht += '  val_data = get_data(val)\n'
        idxu__vqht += '  val_null_bitmap = get_null_bitmap(val)\n'
        idxu__vqht += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(kucpz__svzfj):
            idxu__vqht += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        rjqr__znggy = {}
        exec(idxu__vqht, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, rjqr__znggy)
        impl = rjqr__znggy['impl']
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
    idxu__vqht = 'def impl(A):\n'
    idxu__vqht += '  total_nbytes = 0\n'
    idxu__vqht += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        idxu__vqht += f'  total_nbytes += data[{i}].nbytes\n'
    idxu__vqht += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    idxu__vqht += '  return total_nbytes\n'
    rjqr__znggy = {}
    exec(idxu__vqht, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, rjqr__znggy)
    impl = rjqr__znggy['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        bqc__cwrg = get_null_bitmap(A)
        nmcv__saxbk = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        yac__lkxe = bqc__cwrg.copy()
        return init_struct_arr(nmcv__saxbk, yac__lkxe, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(wttb__nsteh.copy() for wttb__nsteh in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    llpoz__abtii = arrs.count
    idxu__vqht = 'def f(arrs):\n'
    idxu__vqht += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(llpoz__abtii)))
    rjqr__znggy = {}
    exec(idxu__vqht, {}, rjqr__znggy)
    impl = rjqr__znggy['f']
    return impl
