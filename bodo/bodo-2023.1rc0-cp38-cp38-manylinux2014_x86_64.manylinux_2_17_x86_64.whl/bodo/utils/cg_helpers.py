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
    cdt__shsx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    vghre__fie = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    vsszt__popgs = builder.gep(null_bitmap_ptr, [cdt__shsx], inbounds=True)
    rnv__yuhva = builder.load(vsszt__popgs)
    rdn__zcwrn = lir.ArrayType(lir.IntType(8), 8)
    jfots__psk = cgutils.alloca_once_value(builder, lir.Constant(rdn__zcwrn,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    orh__gjexf = builder.load(builder.gep(jfots__psk, [lir.Constant(lir.
        IntType(64), 0), vghre__fie], inbounds=True))
    if val:
        builder.store(builder.or_(rnv__yuhva, orh__gjexf), vsszt__popgs)
    else:
        orh__gjexf = builder.xor(orh__gjexf, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(rnv__yuhva, orh__gjexf), vsszt__popgs)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    cdt__shsx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    vghre__fie = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    rnv__yuhva = builder.load(builder.gep(null_bitmap_ptr, [cdt__shsx],
        inbounds=True))
    rdn__zcwrn = lir.ArrayType(lir.IntType(8), 8)
    jfots__psk = cgutils.alloca_once_value(builder, lir.Constant(rdn__zcwrn,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    orh__gjexf = builder.load(builder.gep(jfots__psk, [lir.Constant(lir.
        IntType(64), 0), vghre__fie], inbounds=True))
    return builder.and_(rnv__yuhva, orh__gjexf)


def pyarray_check(builder, context, obj):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    jyhoy__pje = lir.FunctionType(lir.IntType(32), [sjb__tdvru])
    zymm__xsx = cgutils.get_or_insert_function(builder.module, jyhoy__pje,
        name='is_np_array')
    return builder.call(zymm__xsx, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    hmwdv__hoayr = context.get_value_type(types.intp)
    cvtbb__cwg = lir.FunctionType(lir.IntType(8).as_pointer(), [sjb__tdvru,
        hmwdv__hoayr])
    msyph__jszl = cgutils.get_or_insert_function(builder.module, cvtbb__cwg,
        name='array_getptr1')
    lynge__sjhi = lir.FunctionType(sjb__tdvru, [sjb__tdvru, lir.IntType(8).
        as_pointer()])
    jpjwv__ohd = cgutils.get_or_insert_function(builder.module, lynge__sjhi,
        name='array_getitem')
    ntiar__suto = builder.call(msyph__jszl, [arr_obj, ind])
    return builder.call(jpjwv__ohd, [arr_obj, ntiar__suto])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    hmwdv__hoayr = context.get_value_type(types.intp)
    cvtbb__cwg = lir.FunctionType(lir.IntType(8).as_pointer(), [sjb__tdvru,
        hmwdv__hoayr])
    msyph__jszl = cgutils.get_or_insert_function(builder.module, cvtbb__cwg,
        name='array_getptr1')
    gwhnx__ggqg = lir.FunctionType(lir.VoidType(), [sjb__tdvru, lir.IntType
        (8).as_pointer(), sjb__tdvru])
    czg__uuuix = cgutils.get_or_insert_function(builder.module, gwhnx__ggqg,
        name='array_setitem')
    ntiar__suto = builder.call(msyph__jszl, [arr_obj, ind])
    builder.call(czg__uuuix, [arr_obj, ntiar__suto, val_obj])


def seq_getitem(builder, context, obj, ind):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    hmwdv__hoayr = context.get_value_type(types.intp)
    iqvps__fzn = lir.FunctionType(sjb__tdvru, [sjb__tdvru, hmwdv__hoayr])
    btv__tniu = cgutils.get_or_insert_function(builder.module, iqvps__fzn,
        name='seq_getitem')
    return builder.call(btv__tniu, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    qjj__sataf = lir.FunctionType(lir.IntType(32), [sjb__tdvru, sjb__tdvru])
    kic__essnf = cgutils.get_or_insert_function(builder.module, qjj__sataf,
        name='is_na_value')
    return builder.call(kic__essnf, [val, C_NA])


def list_check(builder, context, obj):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    skp__krjz = context.get_value_type(types.int32)
    qxla__kadub = lir.FunctionType(skp__krjz, [sjb__tdvru])
    gdmu__vmykk = cgutils.get_or_insert_function(builder.module,
        qxla__kadub, name='list_check')
    return builder.call(gdmu__vmykk, [obj])


def dict_keys(builder, context, obj):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    qxla__kadub = lir.FunctionType(sjb__tdvru, [sjb__tdvru])
    gdmu__vmykk = cgutils.get_or_insert_function(builder.module,
        qxla__kadub, name='dict_keys')
    return builder.call(gdmu__vmykk, [obj])


def dict_values(builder, context, obj):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    qxla__kadub = lir.FunctionType(sjb__tdvru, [sjb__tdvru])
    gdmu__vmykk = cgutils.get_or_insert_function(builder.module,
        qxla__kadub, name='dict_values')
    return builder.call(gdmu__vmykk, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    sjb__tdvru = context.get_argument_type(types.pyobject)
    qxla__kadub = lir.FunctionType(lir.VoidType(), [sjb__tdvru, sjb__tdvru])
    gdmu__vmykk = cgutils.get_or_insert_function(builder.module,
        qxla__kadub, name='dict_merge_from_seq2')
    builder.call(gdmu__vmykk, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    qplg__exnhr = cgutils.alloca_once_value(builder, val)
    yygg__yxs = list_check(builder, context, val)
    lik__athgi = builder.icmp_unsigned('!=', yygg__yxs, lir.Constant(
        yygg__yxs.type, 0))
    with builder.if_then(lik__athgi):
        pzrf__nlawv = context.insert_const_string(builder.module, 'numpy')
        mrysb__kkkds = c.pyapi.import_module_noblock(pzrf__nlawv)
        bmk__obs = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            bmk__obs = str(typ.dtype)
        acrss__kpxs = c.pyapi.object_getattr_string(mrysb__kkkds, bmk__obs)
        tid__xnhn = builder.load(qplg__exnhr)
        ozflb__dnho = c.pyapi.call_method(mrysb__kkkds, 'asarray', (
            tid__xnhn, acrss__kpxs))
        builder.store(ozflb__dnho, qplg__exnhr)
        c.pyapi.decref(mrysb__kkkds)
        c.pyapi.decref(acrss__kpxs)
    val = builder.load(qplg__exnhr)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        zrm__ayujk = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        tjlm__ykjn, vry__pzvry = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [zrm__ayujk])
        context.nrt.decref(builder, typ, zrm__ayujk)
        return cgutils.pack_array(builder, [vry__pzvry])
    if isinstance(typ, (StructType, types.BaseTuple)):
        pzrf__nlawv = context.insert_const_string(builder.module, 'pandas')
        voaq__xjn = c.pyapi.import_module_noblock(pzrf__nlawv)
        C_NA = c.pyapi.object_getattr_string(voaq__xjn, 'NA')
        bsdq__nteo = bodo.utils.transform.get_type_alloc_counts(typ)
        akp__fthyx = context.make_tuple(builder, types.Tuple(bsdq__nteo * [
            types.int64]), bsdq__nteo * [context.get_constant(types.int64, 0)])
        meouq__rrgvh = cgutils.alloca_once_value(builder, akp__fthyx)
        syl__tvhum = 0
        gklap__cyt = typ.data if isinstance(typ, StructType) else typ.types
        for wxty__mkmd, t in enumerate(gklap__cyt):
            dya__mwq = bodo.utils.transform.get_type_alloc_counts(t)
            if dya__mwq == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    wxty__mkmd])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, wxty__mkmd)
            cmg__yvz = is_na_value(builder, context, val_obj, C_NA)
            knisf__tgxep = builder.icmp_unsigned('!=', cmg__yvz, lir.
                Constant(cmg__yvz.type, 1))
            with builder.if_then(knisf__tgxep):
                akp__fthyx = builder.load(meouq__rrgvh)
                ascg__jqj = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for wxty__mkmd in range(dya__mwq):
                    wuby__bcf = builder.extract_value(akp__fthyx, 
                        syl__tvhum + wxty__mkmd)
                    qbnl__bpa = builder.extract_value(ascg__jqj, wxty__mkmd)
                    akp__fthyx = builder.insert_value(akp__fthyx, builder.
                        add(wuby__bcf, qbnl__bpa), syl__tvhum + wxty__mkmd)
                builder.store(akp__fthyx, meouq__rrgvh)
            syl__tvhum += dya__mwq
        c.pyapi.decref(voaq__xjn)
        c.pyapi.decref(C_NA)
        return builder.load(meouq__rrgvh)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    pzrf__nlawv = context.insert_const_string(builder.module, 'pandas')
    voaq__xjn = c.pyapi.import_module_noblock(pzrf__nlawv)
    C_NA = c.pyapi.object_getattr_string(voaq__xjn, 'NA')
    bsdq__nteo = bodo.utils.transform.get_type_alloc_counts(typ)
    akp__fthyx = context.make_tuple(builder, types.Tuple(bsdq__nteo * [
        types.int64]), [n] + (bsdq__nteo - 1) * [context.get_constant(types
        .int64, 0)])
    meouq__rrgvh = cgutils.alloca_once_value(builder, akp__fthyx)
    with cgutils.for_range(builder, n) as nowwu__larg:
        tyuec__ydqpg = nowwu__larg.index
        dqp__jzy = seq_getitem(builder, context, arr_obj, tyuec__ydqpg)
        cmg__yvz = is_na_value(builder, context, dqp__jzy, C_NA)
        knisf__tgxep = builder.icmp_unsigned('!=', cmg__yvz, lir.Constant(
            cmg__yvz.type, 1))
        with builder.if_then(knisf__tgxep):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                akp__fthyx = builder.load(meouq__rrgvh)
                ascg__jqj = get_array_elem_counts(c, builder, context,
                    dqp__jzy, typ.dtype)
                for wxty__mkmd in range(bsdq__nteo - 1):
                    wuby__bcf = builder.extract_value(akp__fthyx, 
                        wxty__mkmd + 1)
                    qbnl__bpa = builder.extract_value(ascg__jqj, wxty__mkmd)
                    akp__fthyx = builder.insert_value(akp__fthyx, builder.
                        add(wuby__bcf, qbnl__bpa), wxty__mkmd + 1)
                builder.store(akp__fthyx, meouq__rrgvh)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                syl__tvhum = 1
                for wxty__mkmd, t in enumerate(typ.data):
                    dya__mwq = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if dya__mwq == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(dqp__jzy, wxty__mkmd)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(dqp__jzy, typ
                            .names[wxty__mkmd])
                    cmg__yvz = is_na_value(builder, context, val_obj, C_NA)
                    knisf__tgxep = builder.icmp_unsigned('!=', cmg__yvz,
                        lir.Constant(cmg__yvz.type, 1))
                    with builder.if_then(knisf__tgxep):
                        akp__fthyx = builder.load(meouq__rrgvh)
                        ascg__jqj = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for wxty__mkmd in range(dya__mwq):
                            wuby__bcf = builder.extract_value(akp__fthyx, 
                                syl__tvhum + wxty__mkmd)
                            qbnl__bpa = builder.extract_value(ascg__jqj,
                                wxty__mkmd)
                            akp__fthyx = builder.insert_value(akp__fthyx,
                                builder.add(wuby__bcf, qbnl__bpa), 
                                syl__tvhum + wxty__mkmd)
                        builder.store(akp__fthyx, meouq__rrgvh)
                    syl__tvhum += dya__mwq
            else:
                assert isinstance(typ, MapArrayType), typ
                akp__fthyx = builder.load(meouq__rrgvh)
                ycucd__tdg = dict_keys(builder, context, dqp__jzy)
                jpgh__srbk = dict_values(builder, context, dqp__jzy)
                bay__pysk = get_array_elem_counts(c, builder, context,
                    ycucd__tdg, typ.key_arr_type)
                emt__bmcaq = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for wxty__mkmd in range(1, emt__bmcaq + 1):
                    wuby__bcf = builder.extract_value(akp__fthyx, wxty__mkmd)
                    qbnl__bpa = builder.extract_value(bay__pysk, wxty__mkmd - 1
                        )
                    akp__fthyx = builder.insert_value(akp__fthyx, builder.
                        add(wuby__bcf, qbnl__bpa), wxty__mkmd)
                zwfv__qfb = get_array_elem_counts(c, builder, context,
                    jpgh__srbk, typ.value_arr_type)
                for wxty__mkmd in range(emt__bmcaq + 1, bsdq__nteo):
                    wuby__bcf = builder.extract_value(akp__fthyx, wxty__mkmd)
                    qbnl__bpa = builder.extract_value(zwfv__qfb, wxty__mkmd -
                        emt__bmcaq)
                    akp__fthyx = builder.insert_value(akp__fthyx, builder.
                        add(wuby__bcf, qbnl__bpa), wxty__mkmd)
                builder.store(akp__fthyx, meouq__rrgvh)
                c.pyapi.decref(ycucd__tdg)
                c.pyapi.decref(jpgh__srbk)
        c.pyapi.decref(dqp__jzy)
    c.pyapi.decref(voaq__xjn)
    c.pyapi.decref(C_NA)
    return builder.load(meouq__rrgvh)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    mqyc__ftiaf = n_elems.type.count
    assert mqyc__ftiaf >= 1
    bmps__smtx = builder.extract_value(n_elems, 0)
    if mqyc__ftiaf != 1:
        epc__crhp = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, wxty__mkmd) for wxty__mkmd in range(1, mqyc__ftiaf)])
        busx__tfisg = types.Tuple([types.int64] * (mqyc__ftiaf - 1))
    else:
        epc__crhp = context.get_dummy_value()
        busx__tfisg = types.none
    xkfy__egu = types.TypeRef(arr_type)
    sjsz__fmo = arr_type(types.int64, xkfy__egu, busx__tfisg)
    args = [bmps__smtx, context.get_dummy_value(), epc__crhp]
    jni__beqlh = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        tjlm__ykjn, xxyfv__xrz = c.pyapi.call_jit_code(jni__beqlh,
            sjsz__fmo, args)
    else:
        xxyfv__xrz = context.compile_internal(builder, jni__beqlh,
            sjsz__fmo, args)
    return xxyfv__xrz


def is_ll_eq(builder, val1, val2):
    jtydh__gnbx = val1.type.pointee
    kfrh__vcaf = val2.type.pointee
    assert jtydh__gnbx == kfrh__vcaf, 'invalid llvm value comparison'
    if isinstance(jtydh__gnbx, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(jtydh__gnbx.elements) if isinstance(jtydh__gnbx, lir.
            BaseStructType) else jtydh__gnbx.count
        trl__jmntn = lir.Constant(lir.IntType(1), 1)
        for wxty__mkmd in range(n_elems):
            vyd__kkw = lir.IntType(32)(0)
            dotew__jxnh = lir.IntType(32)(wxty__mkmd)
            nmor__sztpz = builder.gep(val1, [vyd__kkw, dotew__jxnh],
                inbounds=True)
            mngp__yop = builder.gep(val2, [vyd__kkw, dotew__jxnh], inbounds
                =True)
            trl__jmntn = builder.and_(trl__jmntn, is_ll_eq(builder,
                nmor__sztpz, mngp__yop))
        return trl__jmntn
    yveg__mgha = builder.load(val1)
    and__slir = builder.load(val2)
    if yveg__mgha.type in (lir.FloatType(), lir.DoubleType()):
        kow__xbiuw = 32 if yveg__mgha.type == lir.FloatType() else 64
        yveg__mgha = builder.bitcast(yveg__mgha, lir.IntType(kow__xbiuw))
        and__slir = builder.bitcast(and__slir, lir.IntType(kow__xbiuw))
    return builder.icmp_unsigned('==', yveg__mgha, and__slir)
