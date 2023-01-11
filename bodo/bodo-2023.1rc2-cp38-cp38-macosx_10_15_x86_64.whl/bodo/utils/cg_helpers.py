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
    tuigf__drosh = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    erhx__qmvi = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    qzkt__muf = builder.gep(null_bitmap_ptr, [tuigf__drosh], inbounds=True)
    zlqk__ntf = builder.load(qzkt__muf)
    ffkh__bou = lir.ArrayType(lir.IntType(8), 8)
    vsk__fvrjn = cgutils.alloca_once_value(builder, lir.Constant(ffkh__bou,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    ugi__eyi = builder.load(builder.gep(vsk__fvrjn, [lir.Constant(lir.
        IntType(64), 0), erhx__qmvi], inbounds=True))
    if val:
        builder.store(builder.or_(zlqk__ntf, ugi__eyi), qzkt__muf)
    else:
        ugi__eyi = builder.xor(ugi__eyi, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(zlqk__ntf, ugi__eyi), qzkt__muf)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    tuigf__drosh = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    erhx__qmvi = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    zlqk__ntf = builder.load(builder.gep(null_bitmap_ptr, [tuigf__drosh],
        inbounds=True))
    ffkh__bou = lir.ArrayType(lir.IntType(8), 8)
    vsk__fvrjn = cgutils.alloca_once_value(builder, lir.Constant(ffkh__bou,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    ugi__eyi = builder.load(builder.gep(vsk__fvrjn, [lir.Constant(lir.
        IntType(64), 0), erhx__qmvi], inbounds=True))
    return builder.and_(zlqk__ntf, ugi__eyi)


def pyarray_check(builder, context, obj):
    nbl__ntd = context.get_argument_type(types.pyobject)
    lvt__okz = lir.FunctionType(lir.IntType(32), [nbl__ntd])
    cyn__bas = cgutils.get_or_insert_function(builder.module, lvt__okz,
        name='is_np_array')
    return builder.call(cyn__bas, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    nbl__ntd = context.get_argument_type(types.pyobject)
    ssedf__eyc = context.get_value_type(types.intp)
    zbyei__akq = lir.FunctionType(lir.IntType(8).as_pointer(), [nbl__ntd,
        ssedf__eyc])
    fpy__tchif = cgutils.get_or_insert_function(builder.module, zbyei__akq,
        name='array_getptr1')
    zdu__pyr = lir.FunctionType(nbl__ntd, [nbl__ntd, lir.IntType(8).
        as_pointer()])
    afj__pruvf = cgutils.get_or_insert_function(builder.module, zdu__pyr,
        name='array_getitem')
    uipzi__zki = builder.call(fpy__tchif, [arr_obj, ind])
    return builder.call(afj__pruvf, [arr_obj, uipzi__zki])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    nbl__ntd = context.get_argument_type(types.pyobject)
    ssedf__eyc = context.get_value_type(types.intp)
    zbyei__akq = lir.FunctionType(lir.IntType(8).as_pointer(), [nbl__ntd,
        ssedf__eyc])
    fpy__tchif = cgutils.get_or_insert_function(builder.module, zbyei__akq,
        name='array_getptr1')
    caqqn__kmw = lir.FunctionType(lir.VoidType(), [nbl__ntd, lir.IntType(8)
        .as_pointer(), nbl__ntd])
    ypyio__xrlbr = cgutils.get_or_insert_function(builder.module,
        caqqn__kmw, name='array_setitem')
    uipzi__zki = builder.call(fpy__tchif, [arr_obj, ind])
    builder.call(ypyio__xrlbr, [arr_obj, uipzi__zki, val_obj])


def seq_getitem(builder, context, obj, ind):
    nbl__ntd = context.get_argument_type(types.pyobject)
    ssedf__eyc = context.get_value_type(types.intp)
    ftzb__ffdks = lir.FunctionType(nbl__ntd, [nbl__ntd, ssedf__eyc])
    cvqx__hog = cgutils.get_or_insert_function(builder.module, ftzb__ffdks,
        name='seq_getitem')
    return builder.call(cvqx__hog, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    nbl__ntd = context.get_argument_type(types.pyobject)
    mrcx__vpx = lir.FunctionType(lir.IntType(32), [nbl__ntd, nbl__ntd])
    kby__snbri = cgutils.get_or_insert_function(builder.module, mrcx__vpx,
        name='is_na_value')
    return builder.call(kby__snbri, [val, C_NA])


def list_check(builder, context, obj):
    nbl__ntd = context.get_argument_type(types.pyobject)
    dcx__pydh = context.get_value_type(types.int32)
    qhyic__vlbta = lir.FunctionType(dcx__pydh, [nbl__ntd])
    nyic__pjvg = cgutils.get_or_insert_function(builder.module,
        qhyic__vlbta, name='list_check')
    return builder.call(nyic__pjvg, [obj])


def dict_keys(builder, context, obj):
    nbl__ntd = context.get_argument_type(types.pyobject)
    qhyic__vlbta = lir.FunctionType(nbl__ntd, [nbl__ntd])
    nyic__pjvg = cgutils.get_or_insert_function(builder.module,
        qhyic__vlbta, name='dict_keys')
    return builder.call(nyic__pjvg, [obj])


def dict_values(builder, context, obj):
    nbl__ntd = context.get_argument_type(types.pyobject)
    qhyic__vlbta = lir.FunctionType(nbl__ntd, [nbl__ntd])
    nyic__pjvg = cgutils.get_or_insert_function(builder.module,
        qhyic__vlbta, name='dict_values')
    return builder.call(nyic__pjvg, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    nbl__ntd = context.get_argument_type(types.pyobject)
    qhyic__vlbta = lir.FunctionType(lir.VoidType(), [nbl__ntd, nbl__ntd])
    nyic__pjvg = cgutils.get_or_insert_function(builder.module,
        qhyic__vlbta, name='dict_merge_from_seq2')
    builder.call(nyic__pjvg, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    glh__ndm = cgutils.alloca_once_value(builder, val)
    yrjwz__kas = list_check(builder, context, val)
    ynxzb__pck = builder.icmp_unsigned('!=', yrjwz__kas, lir.Constant(
        yrjwz__kas.type, 0))
    with builder.if_then(ynxzb__pck):
        pkehk__nderk = context.insert_const_string(builder.module, 'numpy')
        fpbd__nvqcn = c.pyapi.import_module_noblock(pkehk__nderk)
        dze__iatbr = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            dze__iatbr = str(typ.dtype)
        enoz__ced = c.pyapi.object_getattr_string(fpbd__nvqcn, dze__iatbr)
        vif__valhx = builder.load(glh__ndm)
        oqhsc__bhjlt = c.pyapi.call_method(fpbd__nvqcn, 'asarray', (
            vif__valhx, enoz__ced))
        builder.store(oqhsc__bhjlt, glh__ndm)
        c.pyapi.decref(fpbd__nvqcn)
        c.pyapi.decref(enoz__ced)
    val = builder.load(glh__ndm)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        pbs__vqif = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        fsdpg__swrw, xug__ehjhz = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [pbs__vqif])
        context.nrt.decref(builder, typ, pbs__vqif)
        return cgutils.pack_array(builder, [xug__ehjhz])
    if isinstance(typ, (StructType, types.BaseTuple)):
        pkehk__nderk = context.insert_const_string(builder.module, 'pandas')
        zeap__ipp = c.pyapi.import_module_noblock(pkehk__nderk)
        C_NA = c.pyapi.object_getattr_string(zeap__ipp, 'NA')
        hhd__osx = bodo.utils.transform.get_type_alloc_counts(typ)
        knw__lcs = context.make_tuple(builder, types.Tuple(hhd__osx * [
            types.int64]), hhd__osx * [context.get_constant(types.int64, 0)])
        uiyy__kdwak = cgutils.alloca_once_value(builder, knw__lcs)
        ebfvl__voiak = 0
        kkmm__zarxf = typ.data if isinstance(typ, StructType) else typ.types
        for xam__wzg, t in enumerate(kkmm__zarxf):
            otpqd__kzec = bodo.utils.transform.get_type_alloc_counts(t)
            if otpqd__kzec == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    xam__wzg])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, xam__wzg)
            wvcgr__qlw = is_na_value(builder, context, val_obj, C_NA)
            ifnbt__bkeyj = builder.icmp_unsigned('!=', wvcgr__qlw, lir.
                Constant(wvcgr__qlw.type, 1))
            with builder.if_then(ifnbt__bkeyj):
                knw__lcs = builder.load(uiyy__kdwak)
                oeu__blek = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for xam__wzg in range(otpqd__kzec):
                    hvuv__wxkcb = builder.extract_value(knw__lcs, 
                        ebfvl__voiak + xam__wzg)
                    shbk__fpus = builder.extract_value(oeu__blek, xam__wzg)
                    knw__lcs = builder.insert_value(knw__lcs, builder.add(
                        hvuv__wxkcb, shbk__fpus), ebfvl__voiak + xam__wzg)
                builder.store(knw__lcs, uiyy__kdwak)
            ebfvl__voiak += otpqd__kzec
        c.pyapi.decref(zeap__ipp)
        c.pyapi.decref(C_NA)
        return builder.load(uiyy__kdwak)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    pkehk__nderk = context.insert_const_string(builder.module, 'pandas')
    zeap__ipp = c.pyapi.import_module_noblock(pkehk__nderk)
    C_NA = c.pyapi.object_getattr_string(zeap__ipp, 'NA')
    hhd__osx = bodo.utils.transform.get_type_alloc_counts(typ)
    knw__lcs = context.make_tuple(builder, types.Tuple(hhd__osx * [types.
        int64]), [n] + (hhd__osx - 1) * [context.get_constant(types.int64, 0)])
    uiyy__kdwak = cgutils.alloca_once_value(builder, knw__lcs)
    with cgutils.for_range(builder, n) as pdkck__cxril:
        lwib__isbd = pdkck__cxril.index
        lxmz__pnkqp = seq_getitem(builder, context, arr_obj, lwib__isbd)
        wvcgr__qlw = is_na_value(builder, context, lxmz__pnkqp, C_NA)
        ifnbt__bkeyj = builder.icmp_unsigned('!=', wvcgr__qlw, lir.Constant
            (wvcgr__qlw.type, 1))
        with builder.if_then(ifnbt__bkeyj):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                knw__lcs = builder.load(uiyy__kdwak)
                oeu__blek = get_array_elem_counts(c, builder, context,
                    lxmz__pnkqp, typ.dtype)
                for xam__wzg in range(hhd__osx - 1):
                    hvuv__wxkcb = builder.extract_value(knw__lcs, xam__wzg + 1)
                    shbk__fpus = builder.extract_value(oeu__blek, xam__wzg)
                    knw__lcs = builder.insert_value(knw__lcs, builder.add(
                        hvuv__wxkcb, shbk__fpus), xam__wzg + 1)
                builder.store(knw__lcs, uiyy__kdwak)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                ebfvl__voiak = 1
                for xam__wzg, t in enumerate(typ.data):
                    otpqd__kzec = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if otpqd__kzec == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(lxmz__pnkqp, xam__wzg)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(lxmz__pnkqp,
                            typ.names[xam__wzg])
                    wvcgr__qlw = is_na_value(builder, context, val_obj, C_NA)
                    ifnbt__bkeyj = builder.icmp_unsigned('!=', wvcgr__qlw,
                        lir.Constant(wvcgr__qlw.type, 1))
                    with builder.if_then(ifnbt__bkeyj):
                        knw__lcs = builder.load(uiyy__kdwak)
                        oeu__blek = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for xam__wzg in range(otpqd__kzec):
                            hvuv__wxkcb = builder.extract_value(knw__lcs, 
                                ebfvl__voiak + xam__wzg)
                            shbk__fpus = builder.extract_value(oeu__blek,
                                xam__wzg)
                            knw__lcs = builder.insert_value(knw__lcs,
                                builder.add(hvuv__wxkcb, shbk__fpus), 
                                ebfvl__voiak + xam__wzg)
                        builder.store(knw__lcs, uiyy__kdwak)
                    ebfvl__voiak += otpqd__kzec
            else:
                assert isinstance(typ, MapArrayType), typ
                knw__lcs = builder.load(uiyy__kdwak)
                gfhn__yzrjc = dict_keys(builder, context, lxmz__pnkqp)
                gvkv__xbxpf = dict_values(builder, context, lxmz__pnkqp)
                ctgzl__jrv = get_array_elem_counts(c, builder, context,
                    gfhn__yzrjc, typ.key_arr_type)
                bcb__icqsd = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for xam__wzg in range(1, bcb__icqsd + 1):
                    hvuv__wxkcb = builder.extract_value(knw__lcs, xam__wzg)
                    shbk__fpus = builder.extract_value(ctgzl__jrv, xam__wzg - 1
                        )
                    knw__lcs = builder.insert_value(knw__lcs, builder.add(
                        hvuv__wxkcb, shbk__fpus), xam__wzg)
                sjos__acz = get_array_elem_counts(c, builder, context,
                    gvkv__xbxpf, typ.value_arr_type)
                for xam__wzg in range(bcb__icqsd + 1, hhd__osx):
                    hvuv__wxkcb = builder.extract_value(knw__lcs, xam__wzg)
                    shbk__fpus = builder.extract_value(sjos__acz, xam__wzg -
                        bcb__icqsd)
                    knw__lcs = builder.insert_value(knw__lcs, builder.add(
                        hvuv__wxkcb, shbk__fpus), xam__wzg)
                builder.store(knw__lcs, uiyy__kdwak)
                c.pyapi.decref(gfhn__yzrjc)
                c.pyapi.decref(gvkv__xbxpf)
        c.pyapi.decref(lxmz__pnkqp)
    c.pyapi.decref(zeap__ipp)
    c.pyapi.decref(C_NA)
    return builder.load(uiyy__kdwak)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    ruese__gdz = n_elems.type.count
    assert ruese__gdz >= 1
    urjsi__gtt = builder.extract_value(n_elems, 0)
    if ruese__gdz != 1:
        hip__yoxjd = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, xam__wzg) for xam__wzg in range(1, ruese__gdz)])
        xaqel__sjdgs = types.Tuple([types.int64] * (ruese__gdz - 1))
    else:
        hip__yoxjd = context.get_dummy_value()
        xaqel__sjdgs = types.none
    dve__ifwus = types.TypeRef(arr_type)
    zoxgk__kqcvc = arr_type(types.int64, dve__ifwus, xaqel__sjdgs)
    args = [urjsi__gtt, context.get_dummy_value(), hip__yoxjd]
    yrn__soms = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        fsdpg__swrw, yxjxq__yvmkm = c.pyapi.call_jit_code(yrn__soms,
            zoxgk__kqcvc, args)
    else:
        yxjxq__yvmkm = context.compile_internal(builder, yrn__soms,
            zoxgk__kqcvc, args)
    return yxjxq__yvmkm


def is_ll_eq(builder, val1, val2):
    xjoy__bxrr = val1.type.pointee
    akypt__lym = val2.type.pointee
    assert xjoy__bxrr == akypt__lym, 'invalid llvm value comparison'
    if isinstance(xjoy__bxrr, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(xjoy__bxrr.elements) if isinstance(xjoy__bxrr, lir.
            BaseStructType) else xjoy__bxrr.count
        nkza__adlg = lir.Constant(lir.IntType(1), 1)
        for xam__wzg in range(n_elems):
            dpd__sajl = lir.IntType(32)(0)
            adaz__gvkm = lir.IntType(32)(xam__wzg)
            drkv__ssp = builder.gep(val1, [dpd__sajl, adaz__gvkm], inbounds
                =True)
            ujmq__ayt = builder.gep(val2, [dpd__sajl, adaz__gvkm], inbounds
                =True)
            nkza__adlg = builder.and_(nkza__adlg, is_ll_eq(builder,
                drkv__ssp, ujmq__ayt))
        return nkza__adlg
    ndv__fav = builder.load(val1)
    gckf__maia = builder.load(val2)
    if ndv__fav.type in (lir.FloatType(), lir.DoubleType()):
        zeklh__qbng = 32 if ndv__fav.type == lir.FloatType() else 64
        ndv__fav = builder.bitcast(ndv__fav, lir.IntType(zeklh__qbng))
        gckf__maia = builder.bitcast(gckf__maia, lir.IntType(zeklh__qbng))
    return builder.icmp_unsigned('==', ndv__fav, gckf__maia)
