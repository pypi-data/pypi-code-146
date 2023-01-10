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
    jvvb__ynr = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    msb__zyizz = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    cfepp__idwvf = builder.gep(null_bitmap_ptr, [jvvb__ynr], inbounds=True)
    flp__lvcky = builder.load(cfepp__idwvf)
    gbxyd__cfp = lir.ArrayType(lir.IntType(8), 8)
    avmtv__ggtam = cgutils.alloca_once_value(builder, lir.Constant(
        gbxyd__cfp, (1, 2, 4, 8, 16, 32, 64, 128)))
    vhqz__jmmnj = builder.load(builder.gep(avmtv__ggtam, [lir.Constant(lir.
        IntType(64), 0), msb__zyizz], inbounds=True))
    if val:
        builder.store(builder.or_(flp__lvcky, vhqz__jmmnj), cfepp__idwvf)
    else:
        vhqz__jmmnj = builder.xor(vhqz__jmmnj, lir.Constant(lir.IntType(8), -1)
            )
        builder.store(builder.and_(flp__lvcky, vhqz__jmmnj), cfepp__idwvf)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    jvvb__ynr = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    msb__zyizz = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    flp__lvcky = builder.load(builder.gep(null_bitmap_ptr, [jvvb__ynr],
        inbounds=True))
    gbxyd__cfp = lir.ArrayType(lir.IntType(8), 8)
    avmtv__ggtam = cgutils.alloca_once_value(builder, lir.Constant(
        gbxyd__cfp, (1, 2, 4, 8, 16, 32, 64, 128)))
    vhqz__jmmnj = builder.load(builder.gep(avmtv__ggtam, [lir.Constant(lir.
        IntType(64), 0), msb__zyizz], inbounds=True))
    return builder.and_(flp__lvcky, vhqz__jmmnj)


def pyarray_check(builder, context, obj):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    cad__mjfu = lir.FunctionType(lir.IntType(32), [fhteb__ltxf])
    kbjqb__dkzo = cgutils.get_or_insert_function(builder.module, cad__mjfu,
        name='is_np_array')
    return builder.call(kbjqb__dkzo, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    fbkbd__wlp = context.get_value_type(types.intp)
    rnpk__eoka = lir.FunctionType(lir.IntType(8).as_pointer(), [fhteb__ltxf,
        fbkbd__wlp])
    wzwt__nomgd = cgutils.get_or_insert_function(builder.module, rnpk__eoka,
        name='array_getptr1')
    row__pkn = lir.FunctionType(fhteb__ltxf, [fhteb__ltxf, lir.IntType(8).
        as_pointer()])
    sjm__yjmj = cgutils.get_or_insert_function(builder.module, row__pkn,
        name='array_getitem')
    yst__jzep = builder.call(wzwt__nomgd, [arr_obj, ind])
    return builder.call(sjm__yjmj, [arr_obj, yst__jzep])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    fbkbd__wlp = context.get_value_type(types.intp)
    rnpk__eoka = lir.FunctionType(lir.IntType(8).as_pointer(), [fhteb__ltxf,
        fbkbd__wlp])
    wzwt__nomgd = cgutils.get_or_insert_function(builder.module, rnpk__eoka,
        name='array_getptr1')
    fsk__qxi = lir.FunctionType(lir.VoidType(), [fhteb__ltxf, lir.IntType(8
        ).as_pointer(), fhteb__ltxf])
    dsyo__lfm = cgutils.get_or_insert_function(builder.module, fsk__qxi,
        name='array_setitem')
    yst__jzep = builder.call(wzwt__nomgd, [arr_obj, ind])
    builder.call(dsyo__lfm, [arr_obj, yst__jzep, val_obj])


def seq_getitem(builder, context, obj, ind):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    fbkbd__wlp = context.get_value_type(types.intp)
    zxjph__gmxnf = lir.FunctionType(fhteb__ltxf, [fhteb__ltxf, fbkbd__wlp])
    osgt__jlok = cgutils.get_or_insert_function(builder.module,
        zxjph__gmxnf, name='seq_getitem')
    return builder.call(osgt__jlok, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    xwdou__pev = lir.FunctionType(lir.IntType(32), [fhteb__ltxf, fhteb__ltxf])
    bme__oiu = cgutils.get_or_insert_function(builder.module, xwdou__pev,
        name='is_na_value')
    return builder.call(bme__oiu, [val, C_NA])


def list_check(builder, context, obj):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    vres__khynt = context.get_value_type(types.int32)
    rchz__mkem = lir.FunctionType(vres__khynt, [fhteb__ltxf])
    cyece__wlj = cgutils.get_or_insert_function(builder.module, rchz__mkem,
        name='list_check')
    return builder.call(cyece__wlj, [obj])


def dict_keys(builder, context, obj):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    rchz__mkem = lir.FunctionType(fhteb__ltxf, [fhteb__ltxf])
    cyece__wlj = cgutils.get_or_insert_function(builder.module, rchz__mkem,
        name='dict_keys')
    return builder.call(cyece__wlj, [obj])


def dict_values(builder, context, obj):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    rchz__mkem = lir.FunctionType(fhteb__ltxf, [fhteb__ltxf])
    cyece__wlj = cgutils.get_or_insert_function(builder.module, rchz__mkem,
        name='dict_values')
    return builder.call(cyece__wlj, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    fhteb__ltxf = context.get_argument_type(types.pyobject)
    rchz__mkem = lir.FunctionType(lir.VoidType(), [fhteb__ltxf, fhteb__ltxf])
    cyece__wlj = cgutils.get_or_insert_function(builder.module, rchz__mkem,
        name='dict_merge_from_seq2')
    builder.call(cyece__wlj, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    rhup__huw = cgutils.alloca_once_value(builder, val)
    kne__znlyh = list_check(builder, context, val)
    zpgd__kqjba = builder.icmp_unsigned('!=', kne__znlyh, lir.Constant(
        kne__znlyh.type, 0))
    with builder.if_then(zpgd__kqjba):
        ohyn__okwkd = context.insert_const_string(builder.module, 'numpy')
        afkp__miur = c.pyapi.import_module_noblock(ohyn__okwkd)
        hba__bsfdo = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            hba__bsfdo = str(typ.dtype)
        fbj__rppwu = c.pyapi.object_getattr_string(afkp__miur, hba__bsfdo)
        cux__drven = builder.load(rhup__huw)
        lbkg__xbtaj = c.pyapi.call_method(afkp__miur, 'asarray', (
            cux__drven, fbj__rppwu))
        builder.store(lbkg__xbtaj, rhup__huw)
        c.pyapi.decref(afkp__miur)
        c.pyapi.decref(fbj__rppwu)
    val = builder.load(rhup__huw)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        muhfl__neugu = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        fvau__ghsmv, zlxzh__acm = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [muhfl__neugu])
        context.nrt.decref(builder, typ, muhfl__neugu)
        return cgutils.pack_array(builder, [zlxzh__acm])
    if isinstance(typ, (StructType, types.BaseTuple)):
        ohyn__okwkd = context.insert_const_string(builder.module, 'pandas')
        hrewg__arna = c.pyapi.import_module_noblock(ohyn__okwkd)
        C_NA = c.pyapi.object_getattr_string(hrewg__arna, 'NA')
        bvklo__gfx = bodo.utils.transform.get_type_alloc_counts(typ)
        gyst__aean = context.make_tuple(builder, types.Tuple(bvklo__gfx * [
            types.int64]), bvklo__gfx * [context.get_constant(types.int64, 0)])
        maobv__pawyz = cgutils.alloca_once_value(builder, gyst__aean)
        nad__utz = 0
        audp__spk = typ.data if isinstance(typ, StructType) else typ.types
        for nercf__lcjkv, t in enumerate(audp__spk):
            yznii__gfb = bodo.utils.transform.get_type_alloc_counts(t)
            if yznii__gfb == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    nercf__lcjkv])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, nercf__lcjkv)
            qxxo__bazvx = is_na_value(builder, context, val_obj, C_NA)
            nkup__fbz = builder.icmp_unsigned('!=', qxxo__bazvx, lir.
                Constant(qxxo__bazvx.type, 1))
            with builder.if_then(nkup__fbz):
                gyst__aean = builder.load(maobv__pawyz)
                jumm__zcuz = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for nercf__lcjkv in range(yznii__gfb):
                    nnqm__ool = builder.extract_value(gyst__aean, nad__utz +
                        nercf__lcjkv)
                    cxqxa__ffx = builder.extract_value(jumm__zcuz, nercf__lcjkv
                        )
                    gyst__aean = builder.insert_value(gyst__aean, builder.
                        add(nnqm__ool, cxqxa__ffx), nad__utz + nercf__lcjkv)
                builder.store(gyst__aean, maobv__pawyz)
            nad__utz += yznii__gfb
        c.pyapi.decref(hrewg__arna)
        c.pyapi.decref(C_NA)
        return builder.load(maobv__pawyz)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    ohyn__okwkd = context.insert_const_string(builder.module, 'pandas')
    hrewg__arna = c.pyapi.import_module_noblock(ohyn__okwkd)
    C_NA = c.pyapi.object_getattr_string(hrewg__arna, 'NA')
    bvklo__gfx = bodo.utils.transform.get_type_alloc_counts(typ)
    gyst__aean = context.make_tuple(builder, types.Tuple(bvklo__gfx * [
        types.int64]), [n] + (bvklo__gfx - 1) * [context.get_constant(types
        .int64, 0)])
    maobv__pawyz = cgutils.alloca_once_value(builder, gyst__aean)
    with cgutils.for_range(builder, n) as nyjep__kdvc:
        fxbv__uapw = nyjep__kdvc.index
        sar__wbxd = seq_getitem(builder, context, arr_obj, fxbv__uapw)
        qxxo__bazvx = is_na_value(builder, context, sar__wbxd, C_NA)
        nkup__fbz = builder.icmp_unsigned('!=', qxxo__bazvx, lir.Constant(
            qxxo__bazvx.type, 1))
        with builder.if_then(nkup__fbz):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                gyst__aean = builder.load(maobv__pawyz)
                jumm__zcuz = get_array_elem_counts(c, builder, context,
                    sar__wbxd, typ.dtype)
                for nercf__lcjkv in range(bvklo__gfx - 1):
                    nnqm__ool = builder.extract_value(gyst__aean, 
                        nercf__lcjkv + 1)
                    cxqxa__ffx = builder.extract_value(jumm__zcuz, nercf__lcjkv
                        )
                    gyst__aean = builder.insert_value(gyst__aean, builder.
                        add(nnqm__ool, cxqxa__ffx), nercf__lcjkv + 1)
                builder.store(gyst__aean, maobv__pawyz)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                nad__utz = 1
                for nercf__lcjkv, t in enumerate(typ.data):
                    yznii__gfb = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if yznii__gfb == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(sar__wbxd, nercf__lcjkv
                            )
                    else:
                        val_obj = c.pyapi.dict_getitem_string(sar__wbxd,
                            typ.names[nercf__lcjkv])
                    qxxo__bazvx = is_na_value(builder, context, val_obj, C_NA)
                    nkup__fbz = builder.icmp_unsigned('!=', qxxo__bazvx,
                        lir.Constant(qxxo__bazvx.type, 1))
                    with builder.if_then(nkup__fbz):
                        gyst__aean = builder.load(maobv__pawyz)
                        jumm__zcuz = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for nercf__lcjkv in range(yznii__gfb):
                            nnqm__ool = builder.extract_value(gyst__aean, 
                                nad__utz + nercf__lcjkv)
                            cxqxa__ffx = builder.extract_value(jumm__zcuz,
                                nercf__lcjkv)
                            gyst__aean = builder.insert_value(gyst__aean,
                                builder.add(nnqm__ool, cxqxa__ffx), 
                                nad__utz + nercf__lcjkv)
                        builder.store(gyst__aean, maobv__pawyz)
                    nad__utz += yznii__gfb
            else:
                assert isinstance(typ, MapArrayType), typ
                gyst__aean = builder.load(maobv__pawyz)
                thax__vccm = dict_keys(builder, context, sar__wbxd)
                jnqp__iqna = dict_values(builder, context, sar__wbxd)
                gbmd__ifpgf = get_array_elem_counts(c, builder, context,
                    thax__vccm, typ.key_arr_type)
                demgp__hynh = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for nercf__lcjkv in range(1, demgp__hynh + 1):
                    nnqm__ool = builder.extract_value(gyst__aean, nercf__lcjkv)
                    cxqxa__ffx = builder.extract_value(gbmd__ifpgf, 
                        nercf__lcjkv - 1)
                    gyst__aean = builder.insert_value(gyst__aean, builder.
                        add(nnqm__ool, cxqxa__ffx), nercf__lcjkv)
                nyzdq__egkf = get_array_elem_counts(c, builder, context,
                    jnqp__iqna, typ.value_arr_type)
                for nercf__lcjkv in range(demgp__hynh + 1, bvklo__gfx):
                    nnqm__ool = builder.extract_value(gyst__aean, nercf__lcjkv)
                    cxqxa__ffx = builder.extract_value(nyzdq__egkf, 
                        nercf__lcjkv - demgp__hynh)
                    gyst__aean = builder.insert_value(gyst__aean, builder.
                        add(nnqm__ool, cxqxa__ffx), nercf__lcjkv)
                builder.store(gyst__aean, maobv__pawyz)
                c.pyapi.decref(thax__vccm)
                c.pyapi.decref(jnqp__iqna)
        c.pyapi.decref(sar__wbxd)
    c.pyapi.decref(hrewg__arna)
    c.pyapi.decref(C_NA)
    return builder.load(maobv__pawyz)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    prj__amt = n_elems.type.count
    assert prj__amt >= 1
    utaj__rrh = builder.extract_value(n_elems, 0)
    if prj__amt != 1:
        slcjm__sgu = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, nercf__lcjkv) for nercf__lcjkv in range(1, prj__amt)])
        ggzh__ldye = types.Tuple([types.int64] * (prj__amt - 1))
    else:
        slcjm__sgu = context.get_dummy_value()
        ggzh__ldye = types.none
    qel__fmtnd = types.TypeRef(arr_type)
    tma__ssbb = arr_type(types.int64, qel__fmtnd, ggzh__ldye)
    args = [utaj__rrh, context.get_dummy_value(), slcjm__sgu]
    jirrj__jssfo = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        fvau__ghsmv, fek__dftm = c.pyapi.call_jit_code(jirrj__jssfo,
            tma__ssbb, args)
    else:
        fek__dftm = context.compile_internal(builder, jirrj__jssfo,
            tma__ssbb, args)
    return fek__dftm


def is_ll_eq(builder, val1, val2):
    kqq__hlb = val1.type.pointee
    evmbj__kiv = val2.type.pointee
    assert kqq__hlb == evmbj__kiv, 'invalid llvm value comparison'
    if isinstance(kqq__hlb, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(kqq__hlb.elements) if isinstance(kqq__hlb, lir.
            BaseStructType) else kqq__hlb.count
        fgm__tunxe = lir.Constant(lir.IntType(1), 1)
        for nercf__lcjkv in range(n_elems):
            vwoae__lhu = lir.IntType(32)(0)
            ybe__qfton = lir.IntType(32)(nercf__lcjkv)
            fytfb__rzro = builder.gep(val1, [vwoae__lhu, ybe__qfton],
                inbounds=True)
            yuqop__hmjn = builder.gep(val2, [vwoae__lhu, ybe__qfton],
                inbounds=True)
            fgm__tunxe = builder.and_(fgm__tunxe, is_ll_eq(builder,
                fytfb__rzro, yuqop__hmjn))
        return fgm__tunxe
    sod__dytgs = builder.load(val1)
    ojn__uutog = builder.load(val2)
    if sod__dytgs.type in (lir.FloatType(), lir.DoubleType()):
        wlz__todky = 32 if sod__dytgs.type == lir.FloatType() else 64
        sod__dytgs = builder.bitcast(sod__dytgs, lir.IntType(wlz__todky))
        ojn__uutog = builder.bitcast(ojn__uutog, lir.IntType(wlz__todky))
    return builder.icmp_unsigned('==', sod__dytgs, ojn__uutog)
