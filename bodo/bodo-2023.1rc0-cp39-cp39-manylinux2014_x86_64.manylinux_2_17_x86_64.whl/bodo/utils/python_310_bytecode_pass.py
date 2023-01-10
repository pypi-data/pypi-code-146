"""
transforms the IR to handle bytecode issues in Python 3.10. This
should be removed once https://github.com/numba/numba/pull/7866
is included in Numba 0.56
"""
import operator
import numba
from numba.core import ir
from numba.core.compiler_machinery import FunctionPass, register_pass
from numba.core.errors import UnsupportedError
from numba.core.ir_utils import dprint_func_ir, get_definition, guard


@register_pass(mutates_CFG=False, analysis_only=False)
class Bodo310ByteCodePass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dprint_func_ir(state.func_ir,
            'starting Bodo 3.10 Bytecode optimizations pass')
        peep_hole_call_function_ex_to_call_function_kw(state.func_ir)
        peep_hole_fuse_dict_add_updates(state.func_ir)
        peep_hole_fuse_tuple_adds(state.func_ir)
        return True


def peep_hole_fuse_tuple_adds(func_ir):
    for qot__heg in func_ir.blocks.values():
        new_body = []
        zwh__knxrw = {}
        for wehda__uyz, mctk__tapyv in enumerate(qot__heg.body):
            bncn__eci = None
            if isinstance(mctk__tapyv, ir.Assign) and isinstance(mctk__tapyv
                .value, ir.Expr):
                wbdp__mvt = mctk__tapyv.target.name
                if mctk__tapyv.value.op == 'build_tuple':
                    bncn__eci = wbdp__mvt
                    zwh__knxrw[wbdp__mvt] = mctk__tapyv.value.items
                elif mctk__tapyv.value.op == 'binop' and mctk__tapyv.value.fn == operator.add and mctk__tapyv.value.lhs.name in zwh__knxrw and mctk__tapyv.value.rhs.name in zwh__knxrw:
                    bncn__eci = wbdp__mvt
                    new_items = zwh__knxrw[mctk__tapyv.value.lhs.name
                        ] + zwh__knxrw[mctk__tapyv.value.rhs.name]
                    fqin__wele = ir.Expr.build_tuple(new_items, mctk__tapyv
                        .value.loc)
                    zwh__knxrw[wbdp__mvt] = new_items
                    del zwh__knxrw[mctk__tapyv.value.lhs.name]
                    del zwh__knxrw[mctk__tapyv.value.rhs.name]
                    if mctk__tapyv.value in func_ir._definitions[wbdp__mvt]:
                        func_ir._definitions[wbdp__mvt].remove(mctk__tapyv.
                            value)
                    func_ir._definitions[wbdp__mvt].append(fqin__wele)
                    mctk__tapyv = ir.Assign(fqin__wele, mctk__tapyv.target,
                        mctk__tapyv.loc)
            for shtqc__lcpb in mctk__tapyv.list_vars():
                if (shtqc__lcpb.name in zwh__knxrw and shtqc__lcpb.name !=
                    bncn__eci):
                    del zwh__knxrw[shtqc__lcpb.name]
            new_body.append(mctk__tapyv)
        qot__heg.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    gic__zgl = keyword_expr.items.copy()
    uwh__ykoms = keyword_expr.value_indexes
    for qthxr__zgplo, kmhiu__blz in uwh__ykoms.items():
        gic__zgl[kmhiu__blz] = qthxr__zgplo, gic__zgl[kmhiu__blz][1]
    new_body[buildmap_idx] = None
    return gic__zgl


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    wkofs__cngb = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    gic__zgl = []
    njz__nlurv = buildmap_idx + 1
    while njz__nlurv <= search_end:
        ujtas__hgwe = body[njz__nlurv]
        if not (isinstance(ujtas__hgwe, ir.Assign) and isinstance(
            ujtas__hgwe.value, ir.Const)):
            raise UnsupportedError(wkofs__cngb)
        zqx__ked = ujtas__hgwe.target.name
        ewj__tuuo = ujtas__hgwe.value.value
        njz__nlurv += 1
        cbd__yuo = True
        while njz__nlurv <= search_end and cbd__yuo:
            nbnit__nylx = body[njz__nlurv]
            if (isinstance(nbnit__nylx, ir.Assign) and isinstance(
                nbnit__nylx.value, ir.Expr) and nbnit__nylx.value.op ==
                'getattr' and nbnit__nylx.value.value.name == buildmap_name and
                nbnit__nylx.value.attr == '__setitem__'):
                cbd__yuo = False
            else:
                njz__nlurv += 1
        if cbd__yuo or njz__nlurv == search_end:
            raise UnsupportedError(wkofs__cngb)
        ehr__njm = body[njz__nlurv + 1]
        if not (isinstance(ehr__njm, ir.Assign) and isinstance(ehr__njm.
            value, ir.Expr) and ehr__njm.value.op == 'call' and ehr__njm.
            value.func.name == nbnit__nylx.target.name and len(ehr__njm.
            value.args) == 2 and ehr__njm.value.args[0].name == zqx__ked):
            raise UnsupportedError(wkofs__cngb)
        gfzxc__fyuah = ehr__njm.value.args[1]
        gic__zgl.append((ewj__tuuo, gfzxc__fyuah))
        new_body[njz__nlurv] = None
        new_body[njz__nlurv + 1] = None
        njz__nlurv += 2
    return gic__zgl


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    wkofs__cngb = 'CALL_FUNCTION_EX with **kwargs not supported'
    njz__nlurv = 0
    ctigz__yute = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        duq__tpk = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        duq__tpk = vararg_stmt.target.name
    tqdqm__gia = True
    while search_end >= njz__nlurv and tqdqm__gia:
        cni__oztr = body[search_end]
        if (isinstance(cni__oztr, ir.Assign) and cni__oztr.target.name ==
            duq__tpk and isinstance(cni__oztr.value, ir.Expr) and cni__oztr
            .value.op == 'build_tuple' and not cni__oztr.value.items):
            tqdqm__gia = False
            new_body[search_end] = None
        else:
            if search_end == njz__nlurv or not (isinstance(cni__oztr, ir.
                Assign) and cni__oztr.target.name == duq__tpk and
                isinstance(cni__oztr.value, ir.Expr) and cni__oztr.value.op ==
                'binop' and cni__oztr.value.fn == operator.add):
                raise UnsupportedError(wkofs__cngb)
            ssxhk__lin = cni__oztr.value.lhs.name
            oyopa__mxwp = cni__oztr.value.rhs.name
            biqe__nouoq = body[search_end - 1]
            if not (isinstance(biqe__nouoq, ir.Assign) and isinstance(
                biqe__nouoq.value, ir.Expr) and biqe__nouoq.value.op ==
                'build_tuple' and len(biqe__nouoq.value.items) == 1):
                raise UnsupportedError(wkofs__cngb)
            if biqe__nouoq.target.name == ssxhk__lin:
                duq__tpk = oyopa__mxwp
            elif biqe__nouoq.target.name == oyopa__mxwp:
                duq__tpk = ssxhk__lin
            else:
                raise UnsupportedError(wkofs__cngb)
            ctigz__yute.append(biqe__nouoq.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            jxzy__nmkp = True
            while search_end >= njz__nlurv and jxzy__nmkp:
                hdzu__sgzly = body[search_end]
                if isinstance(hdzu__sgzly, ir.Assign
                    ) and hdzu__sgzly.target.name == duq__tpk:
                    jxzy__nmkp = False
                else:
                    search_end -= 1
    if tqdqm__gia:
        raise UnsupportedError(wkofs__cngb)
    return ctigz__yute[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    wkofs__cngb = 'CALL_FUNCTION_EX with **kwargs not supported'
    for qot__heg in func_ir.blocks.values():
        lfpb__plgbn = False
        new_body = []
        for wehda__uyz, mctk__tapyv in enumerate(qot__heg.body):
            if (isinstance(mctk__tapyv, ir.Assign) and isinstance(
                mctk__tapyv.value, ir.Expr) and mctk__tapyv.value.op ==
                'call' and mctk__tapyv.value.varkwarg is not None):
                lfpb__plgbn = True
                zka__jggs = mctk__tapyv.value
                args = zka__jggs.args
                gic__zgl = zka__jggs.kws
                zxohd__jahiz = zka__jggs.vararg
                louxw__tcc = zka__jggs.varkwarg
                ocr__bkuqo = wehda__uyz - 1
                keez__sewyh = ocr__bkuqo
                iogpv__juia = None
                suod__licl = True
                while keez__sewyh >= 0 and suod__licl:
                    iogpv__juia = qot__heg.body[keez__sewyh]
                    if isinstance(iogpv__juia, ir.Assign
                        ) and iogpv__juia.target.name == louxw__tcc.name:
                        suod__licl = False
                    else:
                        keez__sewyh -= 1
                if gic__zgl or suod__licl or not (isinstance(iogpv__juia.
                    value, ir.Expr) and iogpv__juia.value.op == 'build_map'):
                    raise UnsupportedError(wkofs__cngb)
                if iogpv__juia.value.items:
                    gic__zgl = _call_function_ex_replace_kws_small(iogpv__juia
                        .value, new_body, keez__sewyh)
                else:
                    gic__zgl = _call_function_ex_replace_kws_large(qot__heg
                        .body, louxw__tcc.name, keez__sewyh, wehda__uyz - 1,
                        new_body)
                ocr__bkuqo = keez__sewyh
                if zxohd__jahiz is not None:
                    if args:
                        raise UnsupportedError(wkofs__cngb)
                    uuoot__wwg = ocr__bkuqo
                    ivdec__ijxsg = None
                    suod__licl = True
                    while uuoot__wwg >= 0 and suod__licl:
                        ivdec__ijxsg = qot__heg.body[uuoot__wwg]
                        if isinstance(ivdec__ijxsg, ir.Assign
                            ) and ivdec__ijxsg.target.name == zxohd__jahiz.name:
                            suod__licl = False
                        else:
                            uuoot__wwg -= 1
                    if suod__licl:
                        raise UnsupportedError(wkofs__cngb)
                    if isinstance(ivdec__ijxsg.value, ir.Expr
                        ) and ivdec__ijxsg.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(
                            ivdec__ijxsg.value, new_body, uuoot__wwg)
                    else:
                        args = _call_function_ex_replace_args_large(
                            ivdec__ijxsg, qot__heg.body, new_body, uuoot__wwg)
                aid__vrfhq = ir.Expr.call(zka__jggs.func, args, gic__zgl,
                    zka__jggs.loc, target=zka__jggs.target)
                if mctk__tapyv.target.name in func_ir._definitions and len(
                    func_ir._definitions[mctk__tapyv.target.name]) == 1:
                    func_ir._definitions[mctk__tapyv.target.name].clear()
                func_ir._definitions[mctk__tapyv.target.name].append(aid__vrfhq
                    )
                mctk__tapyv = ir.Assign(aid__vrfhq, mctk__tapyv.target,
                    mctk__tapyv.loc)
            new_body.append(mctk__tapyv)
        if lfpb__plgbn:
            qot__heg.body = [pqv__bqrnt for pqv__bqrnt in new_body if 
                pqv__bqrnt is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for qot__heg in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        lfpb__plgbn = False
        for wehda__uyz, mctk__tapyv in enumerate(qot__heg.body):
            geb__unlcf = True
            iwtex__naaf = None
            if isinstance(mctk__tapyv, ir.Assign) and isinstance(mctk__tapyv
                .value, ir.Expr):
                if mctk__tapyv.value.op == 'build_map':
                    iwtex__naaf = mctk__tapyv.target.name
                    lit_old_idx[mctk__tapyv.target.name] = wehda__uyz
                    lit_new_idx[mctk__tapyv.target.name] = wehda__uyz
                    map_updates[mctk__tapyv.target.name
                        ] = mctk__tapyv.value.items.copy()
                    geb__unlcf = False
                elif mctk__tapyv.value.op == 'call' and wehda__uyz > 0:
                    fejja__sbdqx = mctk__tapyv.value.func.name
                    nbnit__nylx = qot__heg.body[wehda__uyz - 1]
                    args = mctk__tapyv.value.args
                    if (isinstance(nbnit__nylx, ir.Assign) and nbnit__nylx.
                        target.name == fejja__sbdqx and isinstance(
                        nbnit__nylx.value, ir.Expr) and nbnit__nylx.value.
                        op == 'getattr' and nbnit__nylx.value.value.name in
                        lit_old_idx):
                        jxtx__geuu = nbnit__nylx.value.value.name
                        fku__vmslv = nbnit__nylx.value.attr
                        if fku__vmslv == '__setitem__':
                            geb__unlcf = False
                            map_updates[jxtx__geuu].append(args)
                            new_body[-1] = None
                        elif fku__vmslv == 'update' and args[0
                            ].name in lit_old_idx:
                            geb__unlcf = False
                            map_updates[jxtx__geuu].extend(map_updates[args
                                [0].name])
                            new_body[-1] = None
                        if not geb__unlcf:
                            lit_new_idx[jxtx__geuu] = wehda__uyz
                            func_ir._definitions[nbnit__nylx.target.name
                                ].remove(nbnit__nylx.value)
            if not (isinstance(mctk__tapyv, ir.Assign) and isinstance(
                mctk__tapyv.value, ir.Expr) and mctk__tapyv.value.op ==
                'getattr' and mctk__tapyv.value.value.name in lit_old_idx and
                mctk__tapyv.value.attr in ('__setitem__', 'update')):
                for shtqc__lcpb in mctk__tapyv.list_vars():
                    if (shtqc__lcpb.name in lit_old_idx and shtqc__lcpb.
                        name != iwtex__naaf):
                        _insert_build_map(func_ir, shtqc__lcpb.name,
                            qot__heg.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if geb__unlcf:
                new_body.append(mctk__tapyv)
            else:
                func_ir._definitions[mctk__tapyv.target.name].remove(
                    mctk__tapyv.value)
                lfpb__plgbn = True
                new_body.append(None)
        dczt__btfa = list(lit_old_idx.keys())
        for oubg__sej in dczt__btfa:
            _insert_build_map(func_ir, oubg__sej, qot__heg.body, new_body,
                lit_old_idx, lit_new_idx, map_updates)
        if lfpb__plgbn:
            qot__heg.body = [pqv__bqrnt for pqv__bqrnt in new_body if 
                pqv__bqrnt is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    ojxmg__zarr = lit_old_idx[name]
    gywhs__pef = lit_new_idx[name]
    gpr__huhh = map_updates[name]
    new_body[gywhs__pef] = _build_new_build_map(func_ir, name, old_body,
        ojxmg__zarr, gpr__huhh)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    bae__ktg = old_body[old_lineno]
    endn__fzytf = bae__ktg.target
    sufab__qee = bae__ktg.value
    kgzzs__dgm = []
    buizz__spb = []
    for iolk__pex in new_items:
        pxz__sfedd, vdcd__npt = iolk__pex
        frvq__rol = guard(get_definition, func_ir, pxz__sfedd)
        if isinstance(frvq__rol, (ir.Const, ir.Global, ir.FreeVar)):
            kgzzs__dgm.append(frvq__rol.value)
        spti__qgmv = guard(get_definition, func_ir, vdcd__npt)
        if isinstance(spti__qgmv, (ir.Const, ir.Global, ir.FreeVar)):
            buizz__spb.append(spti__qgmv.value)
        else:
            buizz__spb.append(numba.core.interpreter._UNKNOWN_VALUE(
                vdcd__npt.name))
    uwh__ykoms = {}
    if len(kgzzs__dgm) == len(new_items):
        eal__hzyb = {pqv__bqrnt: zeqyj__gzdqs for pqv__bqrnt, zeqyj__gzdqs in
            zip(kgzzs__dgm, buizz__spb)}
        for wehda__uyz, pxz__sfedd in enumerate(kgzzs__dgm):
            uwh__ykoms[pxz__sfedd] = wehda__uyz
    else:
        eal__hzyb = None
    rfwz__uts = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=eal__hzyb, value_indexes=uwh__ykoms, loc=sufab__qee.loc)
    func_ir._definitions[name].append(rfwz__uts)
    return ir.Assign(rfwz__uts, ir.Var(endn__fzytf.scope, name, endn__fzytf
        .loc), rfwz__uts.loc)
