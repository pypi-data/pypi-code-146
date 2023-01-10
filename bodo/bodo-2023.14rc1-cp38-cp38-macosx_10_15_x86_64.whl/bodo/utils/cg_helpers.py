"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    ber__nknyj = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    ipbv__xtmql = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    yagd__eav = builder.gep(null_bitmap_ptr, [ber__nknyj], inbounds=True)
    vnbp__tfdpm = builder.load(yagd__eav)
    mzwc__tceo = lir.ArrayType(lir.IntType(8), 8)
    kpvbi__hcsw = cgutils.alloca_once_value(builder, lir.Constant(
        mzwc__tceo, (1, 2, 4, 8, 16, 32, 64, 128)))
    agvht__oqxe = builder.load(builder.gep(kpvbi__hcsw, [lir.Constant(lir.
        IntType(64), 0), ipbv__xtmql], inbounds=True))
    if val:
        builder.store(builder.or_(vnbp__tfdpm, agvht__oqxe), yagd__eav)
    else:
        agvht__oqxe = builder.xor(agvht__oqxe, lir.Constant(lir.IntType(8), -1)
            )
        builder.store(builder.and_(vnbp__tfdpm, agvht__oqxe), yagd__eav)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    ber__nknyj = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    ipbv__xtmql = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    vnbp__tfdpm = builder.load(builder.gep(null_bitmap_ptr, [ber__nknyj],
        inbounds=True))
    mzwc__tceo = lir.ArrayType(lir.IntType(8), 8)
    kpvbi__hcsw = cgutils.alloca_once_value(builder, lir.Constant(
        mzwc__tceo, (1, 2, 4, 8, 16, 32, 64, 128)))
    agvht__oqxe = builder.load(builder.gep(kpvbi__hcsw, [lir.Constant(lir.
        IntType(64), 0), ipbv__xtmql], inbounds=True))
    return builder.and_(vnbp__tfdpm, agvht__oqxe)


def pyarray_check(builder, context, obj):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    topho__ahmm = lir.FunctionType(lir.IntType(32), [tpxvr__yeefx])
    yafx__stsl = cgutils.get_or_insert_function(builder.module, topho__ahmm,
        name='is_np_array')
    return builder.call(yafx__stsl, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    wlci__ixeho = context.get_value_type(types.intp)
    fas__pqi = lir.FunctionType(lir.IntType(8).as_pointer(), [tpxvr__yeefx,
        wlci__ixeho])
    wbl__nijl = cgutils.get_or_insert_function(builder.module, fas__pqi,
        name='array_getptr1')
    qkmau__ebwa = lir.FunctionType(tpxvr__yeefx, [tpxvr__yeefx, lir.IntType
        (8).as_pointer()])
    mrvx__lqja = cgutils.get_or_insert_function(builder.module, qkmau__ebwa,
        name='array_getitem')
    thgwc__qngb = builder.call(wbl__nijl, [arr_obj, ind])
    return builder.call(mrvx__lqja, [arr_obj, thgwc__qngb])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    wlci__ixeho = context.get_value_type(types.intp)
    fas__pqi = lir.FunctionType(lir.IntType(8).as_pointer(), [tpxvr__yeefx,
        wlci__ixeho])
    wbl__nijl = cgutils.get_or_insert_function(builder.module, fas__pqi,
        name='array_getptr1')
    jgt__tvehx = lir.FunctionType(lir.VoidType(), [tpxvr__yeefx, lir.
        IntType(8).as_pointer(), tpxvr__yeefx])
    zdz__bbiu = cgutils.get_or_insert_function(builder.module, jgt__tvehx,
        name='array_setitem')
    thgwc__qngb = builder.call(wbl__nijl, [arr_obj, ind])
    builder.call(zdz__bbiu, [arr_obj, thgwc__qngb, val_obj])


def seq_getitem(builder, context, obj, ind):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    wlci__ixeho = context.get_value_type(types.intp)
    owmh__suy = lir.FunctionType(tpxvr__yeefx, [tpxvr__yeefx, wlci__ixeho])
    xrue__ntfb = cgutils.get_or_insert_function(builder.module, owmh__suy,
        name='seq_getitem')
    return builder.call(xrue__ntfb, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    ernhl__qfkka = lir.FunctionType(lir.IntType(32), [tpxvr__yeefx,
        tpxvr__yeefx])
    byio__axl = cgutils.get_or_insert_function(builder.module, ernhl__qfkka,
        name='is_na_value')
    return builder.call(byio__axl, [val, C_NA])


def list_check(builder, context, obj):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    vbkml__rnma = context.get_value_type(types.int32)
    pjo__quwz = lir.FunctionType(vbkml__rnma, [tpxvr__yeefx])
    zoj__tgaeq = cgutils.get_or_insert_function(builder.module, pjo__quwz,
        name='list_check')
    return builder.call(zoj__tgaeq, [obj])


def dict_keys(builder, context, obj):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    pjo__quwz = lir.FunctionType(tpxvr__yeefx, [tpxvr__yeefx])
    zoj__tgaeq = cgutils.get_or_insert_function(builder.module, pjo__quwz,
        name='dict_keys')
    return builder.call(zoj__tgaeq, [obj])


def dict_values(builder, context, obj):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    pjo__quwz = lir.FunctionType(tpxvr__yeefx, [tpxvr__yeefx])
    zoj__tgaeq = cgutils.get_or_insert_function(builder.module, pjo__quwz,
        name='dict_values')
    return builder.call(zoj__tgaeq, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    tpxvr__yeefx = context.get_argument_type(types.pyobject)
    pjo__quwz = lir.FunctionType(lir.VoidType(), [tpxvr__yeefx, tpxvr__yeefx])
    zoj__tgaeq = cgutils.get_or_insert_function(builder.module, pjo__quwz,
        name='dict_merge_from_seq2')
    builder.call(zoj__tgaeq, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    ieog__wxxle = cgutils.alloca_once_value(builder, val)
    nko__ihum = list_check(builder, context, val)
    qqmuf__yei = builder.icmp_unsigned('!=', nko__ihum, lir.Constant(
        nko__ihum.type, 0))
    with builder.if_then(qqmuf__yei):
        rpdfg__uqv = context.insert_const_string(builder.module, 'numpy')
        mivyf__dxve = c.pyapi.import_module_noblock(rpdfg__uqv)
        omqh__ngb = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            omqh__ngb = str(typ.dtype)
        kpb__hhg = c.pyapi.object_getattr_string(mivyf__dxve, omqh__ngb)
        kvydv__gcpim = builder.load(ieog__wxxle)
        myt__xbmbl = c.pyapi.call_method(mivyf__dxve, 'asarray', (
            kvydv__gcpim, kpb__hhg))
        builder.store(myt__xbmbl, ieog__wxxle)
        c.pyapi.decref(mivyf__dxve)
        c.pyapi.decref(kpb__hhg)
    val = builder.load(ieog__wxxle)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        xfqo__frgxd = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        xki__jgp, tebb__mhzqq = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [xfqo__frgxd])
        context.nrt.decref(builder, typ, xfqo__frgxd)
        return cgutils.pack_array(builder, [tebb__mhzqq])
    if isinstance(typ, (StructType, types.BaseTuple)):
        rpdfg__uqv = context.insert_const_string(builder.module, 'pandas')
        pofs__jqv = c.pyapi.import_module_noblock(rpdfg__uqv)
        C_NA = c.pyapi.object_getattr_string(pofs__jqv, 'NA')
        ztu__doqv = bodo.utils.transform.get_type_alloc_counts(typ)
        olo__tied = context.make_tuple(builder, types.Tuple(ztu__doqv * [
            types.int64]), ztu__doqv * [context.get_constant(types.int64, 0)])
        lfk__ypp = cgutils.alloca_once_value(builder, olo__tied)
        jml__ymtiu = 0
        wbfe__yeld = typ.data if isinstance(typ, StructType) else typ.types
        for vlr__zwa, t in enumerate(wbfe__yeld):
            vdhtl__owpk = bodo.utils.transform.get_type_alloc_counts(t)
            if vdhtl__owpk == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    vlr__zwa])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, vlr__zwa)
            tsp__dufb = is_na_value(builder, context, val_obj, C_NA)
            rbs__dcy = builder.icmp_unsigned('!=', tsp__dufb, lir.Constant(
                tsp__dufb.type, 1))
            with builder.if_then(rbs__dcy):
                olo__tied = builder.load(lfk__ypp)
                gurgm__qsj = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for vlr__zwa in range(vdhtl__owpk):
                    vayee__motg = builder.extract_value(olo__tied, 
                        jml__ymtiu + vlr__zwa)
                    rof__uvsp = builder.extract_value(gurgm__qsj, vlr__zwa)
                    olo__tied = builder.insert_value(olo__tied, builder.add
                        (vayee__motg, rof__uvsp), jml__ymtiu + vlr__zwa)
                builder.store(olo__tied, lfk__ypp)
            jml__ymtiu += vdhtl__owpk
        c.pyapi.decref(pofs__jqv)
        c.pyapi.decref(C_NA)
        return builder.load(lfk__ypp)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    rpdfg__uqv = context.insert_const_string(builder.module, 'pandas')
    pofs__jqv = c.pyapi.import_module_noblock(rpdfg__uqv)
    C_NA = c.pyapi.object_getattr_string(pofs__jqv, 'NA')
    ztu__doqv = bodo.utils.transform.get_type_alloc_counts(typ)
    olo__tied = context.make_tuple(builder, types.Tuple(ztu__doqv * [types.
        int64]), [n] + (ztu__doqv - 1) * [context.get_constant(types.int64, 0)]
        )
    lfk__ypp = cgutils.alloca_once_value(builder, olo__tied)
    with cgutils.for_range(builder, n) as fneam__vyn:
        wfuf__wlcfz = fneam__vyn.index
        enfo__fjo = seq_getitem(builder, context, arr_obj, wfuf__wlcfz)
        tsp__dufb = is_na_value(builder, context, enfo__fjo, C_NA)
        rbs__dcy = builder.icmp_unsigned('!=', tsp__dufb, lir.Constant(
            tsp__dufb.type, 1))
        with builder.if_then(rbs__dcy):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                olo__tied = builder.load(lfk__ypp)
                gurgm__qsj = get_array_elem_counts(c, builder, context,
                    enfo__fjo, typ.dtype)
                for vlr__zwa in range(ztu__doqv - 1):
                    vayee__motg = builder.extract_value(olo__tied, vlr__zwa + 1
                        )
                    rof__uvsp = builder.extract_value(gurgm__qsj, vlr__zwa)
                    olo__tied = builder.insert_value(olo__tied, builder.add
                        (vayee__motg, rof__uvsp), vlr__zwa + 1)
                builder.store(olo__tied, lfk__ypp)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                jml__ymtiu = 1
                for vlr__zwa, t in enumerate(typ.data):
                    vdhtl__owpk = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if vdhtl__owpk == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(enfo__fjo, vlr__zwa)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(enfo__fjo,
                            typ.names[vlr__zwa])
                    tsp__dufb = is_na_value(builder, context, val_obj, C_NA)
                    rbs__dcy = builder.icmp_unsigned('!=', tsp__dufb, lir.
                        Constant(tsp__dufb.type, 1))
                    with builder.if_then(rbs__dcy):
                        olo__tied = builder.load(lfk__ypp)
                        gurgm__qsj = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for vlr__zwa in range(vdhtl__owpk):
                            vayee__motg = builder.extract_value(olo__tied, 
                                jml__ymtiu + vlr__zwa)
                            rof__uvsp = builder.extract_value(gurgm__qsj,
                                vlr__zwa)
                            olo__tied = builder.insert_value(olo__tied,
                                builder.add(vayee__motg, rof__uvsp), 
                                jml__ymtiu + vlr__zwa)
                        builder.store(olo__tied, lfk__ypp)
                    jml__ymtiu += vdhtl__owpk
            else:
                assert isinstance(typ, MapArrayType), typ
                olo__tied = builder.load(lfk__ypp)
                yaaag__ccgc = dict_keys(builder, context, enfo__fjo)
                kdo__jubew = dict_values(builder, context, enfo__fjo)
                mvj__yhkod = get_array_elem_counts(c, builder, context,
                    yaaag__ccgc, typ.key_arr_type)
                mbmk__pkb = bodo.utils.transform.get_type_alloc_counts(typ.
                    key_arr_type)
                for vlr__zwa in range(1, mbmk__pkb + 1):
                    vayee__motg = builder.extract_value(olo__tied, vlr__zwa)
                    rof__uvsp = builder.extract_value(mvj__yhkod, vlr__zwa - 1)
                    olo__tied = builder.insert_value(olo__tied, builder.add
                        (vayee__motg, rof__uvsp), vlr__zwa)
                evk__nmi = get_array_elem_counts(c, builder, context,
                    kdo__jubew, typ.value_arr_type)
                for vlr__zwa in range(mbmk__pkb + 1, ztu__doqv):
                    vayee__motg = builder.extract_value(olo__tied, vlr__zwa)
                    rof__uvsp = builder.extract_value(evk__nmi, vlr__zwa -
                        mbmk__pkb)
                    olo__tied = builder.insert_value(olo__tied, builder.add
                        (vayee__motg, rof__uvsp), vlr__zwa)
                builder.store(olo__tied, lfk__ypp)
                c.pyapi.decref(yaaag__ccgc)
                c.pyapi.decref(kdo__jubew)
        c.pyapi.decref(enfo__fjo)
    c.pyapi.decref(pofs__jqv)
    c.pyapi.decref(C_NA)
    return builder.load(lfk__ypp)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    czn__fnix = n_elems.type.count
    assert czn__fnix >= 1
    pikv__vovf = builder.extract_value(n_elems, 0)
    if czn__fnix != 1:
        epwi__itsfx = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, vlr__zwa) for vlr__zwa in range(1, czn__fnix)])
        vzk__iotj = types.Tuple([types.int64] * (czn__fnix - 1))
    else:
        epwi__itsfx = context.get_dummy_value()
        vzk__iotj = types.none
    nhaf__aqdvo = types.TypeRef(arr_type)
    ygl__zntqc = arr_type(types.int64, nhaf__aqdvo, vzk__iotj)
    args = [pikv__vovf, context.get_dummy_value(), epwi__itsfx]
    ipt__alee = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        xki__jgp, xiv__vub = c.pyapi.call_jit_code(ipt__alee, ygl__zntqc, args)
    else:
        xiv__vub = context.compile_internal(builder, ipt__alee, ygl__zntqc,
            args)
    return xiv__vub


def is_ll_eq(builder, val1, val2):
    mbw__gih = val1.type.pointee
    hwd__sye = val2.type.pointee
    assert mbw__gih == hwd__sye, 'invalid llvm value comparison'
    if isinstance(mbw__gih, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(mbw__gih.elements) if isinstance(mbw__gih, lir.
            BaseStructType) else mbw__gih.count
        dxrfp__qcc = lir.Constant(lir.IntType(1), 1)
        for vlr__zwa in range(n_elems):
            matta__gnvuh = lir.IntType(32)(0)
            hsb__cidow = lir.IntType(32)(vlr__zwa)
            zbd__iev = builder.gep(val1, [matta__gnvuh, hsb__cidow],
                inbounds=True)
            htby__vzo = builder.gep(val2, [matta__gnvuh, hsb__cidow],
                inbounds=True)
            dxrfp__qcc = builder.and_(dxrfp__qcc, is_ll_eq(builder,
                zbd__iev, htby__vzo))
        return dxrfp__qcc
    puar__mln = builder.load(val1)
    zzdhi__yel = builder.load(val2)
    if puar__mln.type in (lir.FloatType(), lir.DoubleType()):
        agiwc__yzf = 32 if puar__mln.type == lir.FloatType() else 64
        puar__mln = builder.bitcast(puar__mln, lir.IntType(agiwc__yzf))
        zzdhi__yel = builder.bitcast(zzdhi__yel, lir.IntType(agiwc__yzf))
    return builder.icmp_unsigned('==', puar__mln, zzdhi__yel)
