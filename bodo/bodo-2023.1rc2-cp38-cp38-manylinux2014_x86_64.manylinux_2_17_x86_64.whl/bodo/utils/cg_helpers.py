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
    bqg__lmjpx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    blyh__omiis = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    vha__igs = builder.gep(null_bitmap_ptr, [bqg__lmjpx], inbounds=True)
    cjif__myjbt = builder.load(vha__igs)
    ipqaz__wtqmk = lir.ArrayType(lir.IntType(8), 8)
    mzrua__wtwgz = cgutils.alloca_once_value(builder, lir.Constant(
        ipqaz__wtqmk, (1, 2, 4, 8, 16, 32, 64, 128)))
    faf__kdh = builder.load(builder.gep(mzrua__wtwgz, [lir.Constant(lir.
        IntType(64), 0), blyh__omiis], inbounds=True))
    if val:
        builder.store(builder.or_(cjif__myjbt, faf__kdh), vha__igs)
    else:
        faf__kdh = builder.xor(faf__kdh, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(cjif__myjbt, faf__kdh), vha__igs)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    bqg__lmjpx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    blyh__omiis = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    cjif__myjbt = builder.load(builder.gep(null_bitmap_ptr, [bqg__lmjpx],
        inbounds=True))
    ipqaz__wtqmk = lir.ArrayType(lir.IntType(8), 8)
    mzrua__wtwgz = cgutils.alloca_once_value(builder, lir.Constant(
        ipqaz__wtqmk, (1, 2, 4, 8, 16, 32, 64, 128)))
    faf__kdh = builder.load(builder.gep(mzrua__wtwgz, [lir.Constant(lir.
        IntType(64), 0), blyh__omiis], inbounds=True))
    return builder.and_(cjif__myjbt, faf__kdh)


def pyarray_check(builder, context, obj):
    unl__enrvk = context.get_argument_type(types.pyobject)
    lrmj__jyict = lir.FunctionType(lir.IntType(32), [unl__enrvk])
    mnfro__mnxjt = cgutils.get_or_insert_function(builder.module,
        lrmj__jyict, name='is_np_array')
    return builder.call(mnfro__mnxjt, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    unl__enrvk = context.get_argument_type(types.pyobject)
    ahb__jqw = context.get_value_type(types.intp)
    pnwrm__gtxt = lir.FunctionType(lir.IntType(8).as_pointer(), [unl__enrvk,
        ahb__jqw])
    autwv__kuohz = cgutils.get_or_insert_function(builder.module,
        pnwrm__gtxt, name='array_getptr1')
    jzsd__hbzj = lir.FunctionType(unl__enrvk, [unl__enrvk, lir.IntType(8).
        as_pointer()])
    zre__uhbs = cgutils.get_or_insert_function(builder.module, jzsd__hbzj,
        name='array_getitem')
    rjli__klx = builder.call(autwv__kuohz, [arr_obj, ind])
    return builder.call(zre__uhbs, [arr_obj, rjli__klx])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    unl__enrvk = context.get_argument_type(types.pyobject)
    ahb__jqw = context.get_value_type(types.intp)
    pnwrm__gtxt = lir.FunctionType(lir.IntType(8).as_pointer(), [unl__enrvk,
        ahb__jqw])
    autwv__kuohz = cgutils.get_or_insert_function(builder.module,
        pnwrm__gtxt, name='array_getptr1')
    gwp__bkz = lir.FunctionType(lir.VoidType(), [unl__enrvk, lir.IntType(8)
        .as_pointer(), unl__enrvk])
    mbhp__usew = cgutils.get_or_insert_function(builder.module, gwp__bkz,
        name='array_setitem')
    rjli__klx = builder.call(autwv__kuohz, [arr_obj, ind])
    builder.call(mbhp__usew, [arr_obj, rjli__klx, val_obj])


def seq_getitem(builder, context, obj, ind):
    unl__enrvk = context.get_argument_type(types.pyobject)
    ahb__jqw = context.get_value_type(types.intp)
    qtu__yfyum = lir.FunctionType(unl__enrvk, [unl__enrvk, ahb__jqw])
    atl__gdh = cgutils.get_or_insert_function(builder.module, qtu__yfyum,
        name='seq_getitem')
    return builder.call(atl__gdh, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    unl__enrvk = context.get_argument_type(types.pyobject)
    vrtx__dcva = lir.FunctionType(lir.IntType(32), [unl__enrvk, unl__enrvk])
    qksff__cljke = cgutils.get_or_insert_function(builder.module,
        vrtx__dcva, name='is_na_value')
    return builder.call(qksff__cljke, [val, C_NA])


def list_check(builder, context, obj):
    unl__enrvk = context.get_argument_type(types.pyobject)
    pou__ced = context.get_value_type(types.int32)
    kpf__kreu = lir.FunctionType(pou__ced, [unl__enrvk])
    dosi__grgr = cgutils.get_or_insert_function(builder.module, kpf__kreu,
        name='list_check')
    return builder.call(dosi__grgr, [obj])


def dict_keys(builder, context, obj):
    unl__enrvk = context.get_argument_type(types.pyobject)
    kpf__kreu = lir.FunctionType(unl__enrvk, [unl__enrvk])
    dosi__grgr = cgutils.get_or_insert_function(builder.module, kpf__kreu,
        name='dict_keys')
    return builder.call(dosi__grgr, [obj])


def dict_values(builder, context, obj):
    unl__enrvk = context.get_argument_type(types.pyobject)
    kpf__kreu = lir.FunctionType(unl__enrvk, [unl__enrvk])
    dosi__grgr = cgutils.get_or_insert_function(builder.module, kpf__kreu,
        name='dict_values')
    return builder.call(dosi__grgr, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    unl__enrvk = context.get_argument_type(types.pyobject)
    kpf__kreu = lir.FunctionType(lir.VoidType(), [unl__enrvk, unl__enrvk])
    dosi__grgr = cgutils.get_or_insert_function(builder.module, kpf__kreu,
        name='dict_merge_from_seq2')
    builder.call(dosi__grgr, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    bmtab__ywt = cgutils.alloca_once_value(builder, val)
    rdvdu__vzc = list_check(builder, context, val)
    xwo__wkve = builder.icmp_unsigned('!=', rdvdu__vzc, lir.Constant(
        rdvdu__vzc.type, 0))
    with builder.if_then(xwo__wkve):
        ekr__pvrk = context.insert_const_string(builder.module, 'numpy')
        ohb__albe = c.pyapi.import_module_noblock(ekr__pvrk)
        obcl__fmrmu = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            obcl__fmrmu = str(typ.dtype)
        tpo__fwxo = c.pyapi.object_getattr_string(ohb__albe, obcl__fmrmu)
        bcyc__hcx = builder.load(bmtab__ywt)
        plwr__mnc = c.pyapi.call_method(ohb__albe, 'asarray', (bcyc__hcx,
            tpo__fwxo))
        builder.store(plwr__mnc, bmtab__ywt)
        c.pyapi.decref(ohb__albe)
        c.pyapi.decref(tpo__fwxo)
    val = builder.load(bmtab__ywt)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        umxim__wry = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        kxdgl__qiu, rsaip__gfij = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [umxim__wry])
        context.nrt.decref(builder, typ, umxim__wry)
        return cgutils.pack_array(builder, [rsaip__gfij])
    if isinstance(typ, (StructType, types.BaseTuple)):
        ekr__pvrk = context.insert_const_string(builder.module, 'pandas')
        esche__hxkt = c.pyapi.import_module_noblock(ekr__pvrk)
        C_NA = c.pyapi.object_getattr_string(esche__hxkt, 'NA')
        lxz__kun = bodo.utils.transform.get_type_alloc_counts(typ)
        xzd__rlok = context.make_tuple(builder, types.Tuple(lxz__kun * [
            types.int64]), lxz__kun * [context.get_constant(types.int64, 0)])
        ybjg__bylv = cgutils.alloca_once_value(builder, xzd__rlok)
        qmhp__zlhu = 0
        mlfio__qzwj = typ.data if isinstance(typ, StructType) else typ.types
        for fobfp__rzjv, t in enumerate(mlfio__qzwj):
            buze__omwt = bodo.utils.transform.get_type_alloc_counts(t)
            if buze__omwt == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    fobfp__rzjv])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, fobfp__rzjv)
            vxl__mczbo = is_na_value(builder, context, val_obj, C_NA)
            xvzdo__anno = builder.icmp_unsigned('!=', vxl__mczbo, lir.
                Constant(vxl__mczbo.type, 1))
            with builder.if_then(xvzdo__anno):
                xzd__rlok = builder.load(ybjg__bylv)
                agfem__drs = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for fobfp__rzjv in range(buze__omwt):
                    asdvv__sqzgh = builder.extract_value(xzd__rlok, 
                        qmhp__zlhu + fobfp__rzjv)
                    ouuz__kvv = builder.extract_value(agfem__drs, fobfp__rzjv)
                    xzd__rlok = builder.insert_value(xzd__rlok, builder.add
                        (asdvv__sqzgh, ouuz__kvv), qmhp__zlhu + fobfp__rzjv)
                builder.store(xzd__rlok, ybjg__bylv)
            qmhp__zlhu += buze__omwt
        c.pyapi.decref(esche__hxkt)
        c.pyapi.decref(C_NA)
        return builder.load(ybjg__bylv)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    ekr__pvrk = context.insert_const_string(builder.module, 'pandas')
    esche__hxkt = c.pyapi.import_module_noblock(ekr__pvrk)
    C_NA = c.pyapi.object_getattr_string(esche__hxkt, 'NA')
    lxz__kun = bodo.utils.transform.get_type_alloc_counts(typ)
    xzd__rlok = context.make_tuple(builder, types.Tuple(lxz__kun * [types.
        int64]), [n] + (lxz__kun - 1) * [context.get_constant(types.int64, 0)])
    ybjg__bylv = cgutils.alloca_once_value(builder, xzd__rlok)
    with cgutils.for_range(builder, n) as lexw__bfoxp:
        qlq__zqgy = lexw__bfoxp.index
        fqkmc__rsct = seq_getitem(builder, context, arr_obj, qlq__zqgy)
        vxl__mczbo = is_na_value(builder, context, fqkmc__rsct, C_NA)
        xvzdo__anno = builder.icmp_unsigned('!=', vxl__mczbo, lir.Constant(
            vxl__mczbo.type, 1))
        with builder.if_then(xvzdo__anno):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                xzd__rlok = builder.load(ybjg__bylv)
                agfem__drs = get_array_elem_counts(c, builder, context,
                    fqkmc__rsct, typ.dtype)
                for fobfp__rzjv in range(lxz__kun - 1):
                    asdvv__sqzgh = builder.extract_value(xzd__rlok, 
                        fobfp__rzjv + 1)
                    ouuz__kvv = builder.extract_value(agfem__drs, fobfp__rzjv)
                    xzd__rlok = builder.insert_value(xzd__rlok, builder.add
                        (asdvv__sqzgh, ouuz__kvv), fobfp__rzjv + 1)
                builder.store(xzd__rlok, ybjg__bylv)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                qmhp__zlhu = 1
                for fobfp__rzjv, t in enumerate(typ.data):
                    buze__omwt = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if buze__omwt == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(fqkmc__rsct,
                            fobfp__rzjv)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(fqkmc__rsct,
                            typ.names[fobfp__rzjv])
                    vxl__mczbo = is_na_value(builder, context, val_obj, C_NA)
                    xvzdo__anno = builder.icmp_unsigned('!=', vxl__mczbo,
                        lir.Constant(vxl__mczbo.type, 1))
                    with builder.if_then(xvzdo__anno):
                        xzd__rlok = builder.load(ybjg__bylv)
                        agfem__drs = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for fobfp__rzjv in range(buze__omwt):
                            asdvv__sqzgh = builder.extract_value(xzd__rlok,
                                qmhp__zlhu + fobfp__rzjv)
                            ouuz__kvv = builder.extract_value(agfem__drs,
                                fobfp__rzjv)
                            xzd__rlok = builder.insert_value(xzd__rlok,
                                builder.add(asdvv__sqzgh, ouuz__kvv), 
                                qmhp__zlhu + fobfp__rzjv)
                        builder.store(xzd__rlok, ybjg__bylv)
                    qmhp__zlhu += buze__omwt
            else:
                assert isinstance(typ, MapArrayType), typ
                xzd__rlok = builder.load(ybjg__bylv)
                vttgj__izezq = dict_keys(builder, context, fqkmc__rsct)
                hnrk__fhd = dict_values(builder, context, fqkmc__rsct)
                ntsie__lpzrq = get_array_elem_counts(c, builder, context,
                    vttgj__izezq, typ.key_arr_type)
                qfckg__ngty = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for fobfp__rzjv in range(1, qfckg__ngty + 1):
                    asdvv__sqzgh = builder.extract_value(xzd__rlok, fobfp__rzjv
                        )
                    ouuz__kvv = builder.extract_value(ntsie__lpzrq, 
                        fobfp__rzjv - 1)
                    xzd__rlok = builder.insert_value(xzd__rlok, builder.add
                        (asdvv__sqzgh, ouuz__kvv), fobfp__rzjv)
                saj__ypb = get_array_elem_counts(c, builder, context,
                    hnrk__fhd, typ.value_arr_type)
                for fobfp__rzjv in range(qfckg__ngty + 1, lxz__kun):
                    asdvv__sqzgh = builder.extract_value(xzd__rlok, fobfp__rzjv
                        )
                    ouuz__kvv = builder.extract_value(saj__ypb, fobfp__rzjv -
                        qfckg__ngty)
                    xzd__rlok = builder.insert_value(xzd__rlok, builder.add
                        (asdvv__sqzgh, ouuz__kvv), fobfp__rzjv)
                builder.store(xzd__rlok, ybjg__bylv)
                c.pyapi.decref(vttgj__izezq)
                c.pyapi.decref(hnrk__fhd)
        c.pyapi.decref(fqkmc__rsct)
    c.pyapi.decref(esche__hxkt)
    c.pyapi.decref(C_NA)
    return builder.load(ybjg__bylv)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    tvoq__tlmk = n_elems.type.count
    assert tvoq__tlmk >= 1
    ryws__yfrww = builder.extract_value(n_elems, 0)
    if tvoq__tlmk != 1:
        iymbu__akduw = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, fobfp__rzjv) for fobfp__rzjv in range(1, tvoq__tlmk)])
        kszqn__dof = types.Tuple([types.int64] * (tvoq__tlmk - 1))
    else:
        iymbu__akduw = context.get_dummy_value()
        kszqn__dof = types.none
    sagj__ddh = types.TypeRef(arr_type)
    mfr__fck = arr_type(types.int64, sagj__ddh, kszqn__dof)
    args = [ryws__yfrww, context.get_dummy_value(), iymbu__akduw]
    asxy__vmf = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        kxdgl__qiu, vcaku__cgqw = c.pyapi.call_jit_code(asxy__vmf, mfr__fck,
            args)
    else:
        vcaku__cgqw = context.compile_internal(builder, asxy__vmf, mfr__fck,
            args)
    return vcaku__cgqw


def is_ll_eq(builder, val1, val2):
    klhsl__ysute = val1.type.pointee
    whc__mte = val2.type.pointee
    assert klhsl__ysute == whc__mte, 'invalid llvm value comparison'
    if isinstance(klhsl__ysute, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(klhsl__ysute.elements) if isinstance(klhsl__ysute,
            lir.BaseStructType) else klhsl__ysute.count
        fjmg__uepgg = lir.Constant(lir.IntType(1), 1)
        for fobfp__rzjv in range(n_elems):
            laqb__adig = lir.IntType(32)(0)
            wkryg__ysrpr = lir.IntType(32)(fobfp__rzjv)
            rqan__xupfg = builder.gep(val1, [laqb__adig, wkryg__ysrpr],
                inbounds=True)
            ifyoo__zegz = builder.gep(val2, [laqb__adig, wkryg__ysrpr],
                inbounds=True)
            fjmg__uepgg = builder.and_(fjmg__uepgg, is_ll_eq(builder,
                rqan__xupfg, ifyoo__zegz))
        return fjmg__uepgg
    jsr__lhe = builder.load(val1)
    rpyew__scll = builder.load(val2)
    if jsr__lhe.type in (lir.FloatType(), lir.DoubleType()):
        clswp__llsai = 32 if jsr__lhe.type == lir.FloatType() else 64
        jsr__lhe = builder.bitcast(jsr__lhe, lir.IntType(clswp__llsai))
        rpyew__scll = builder.bitcast(rpyew__scll, lir.IntType(clswp__llsai))
    return builder.icmp_unsigned('==', jsr__lhe, rpyew__scll)
