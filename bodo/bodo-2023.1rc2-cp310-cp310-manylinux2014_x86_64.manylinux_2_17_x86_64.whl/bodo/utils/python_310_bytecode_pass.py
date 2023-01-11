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
    for cfrpv__zoklk in func_ir.blocks.values():
        new_body = []
        her__jso = {}
        for ywck__btvfm, ormer__ecdym in enumerate(cfrpv__zoklk.body):
            agpm__ihhit = None
            if isinstance(ormer__ecdym, ir.Assign) and isinstance(ormer__ecdym
                .value, ir.Expr):
                exqg__ytxq = ormer__ecdym.target.name
                if ormer__ecdym.value.op == 'build_tuple':
                    agpm__ihhit = exqg__ytxq
                    her__jso[exqg__ytxq] = ormer__ecdym.value.items
                elif ormer__ecdym.value.op == 'binop' and ormer__ecdym.value.fn == operator.add and ormer__ecdym.value.lhs.name in her__jso and ormer__ecdym.value.rhs.name in her__jso:
                    agpm__ihhit = exqg__ytxq
                    new_items = her__jso[ormer__ecdym.value.lhs.name
                        ] + her__jso[ormer__ecdym.value.rhs.name]
                    mxdpi__stxe = ir.Expr.build_tuple(new_items,
                        ormer__ecdym.value.loc)
                    her__jso[exqg__ytxq] = new_items
                    del her__jso[ormer__ecdym.value.lhs.name]
                    del her__jso[ormer__ecdym.value.rhs.name]
                    if ormer__ecdym.value in func_ir._definitions[exqg__ytxq]:
                        func_ir._definitions[exqg__ytxq].remove(ormer__ecdym
                            .value)
                    func_ir._definitions[exqg__ytxq].append(mxdpi__stxe)
                    ormer__ecdym = ir.Assign(mxdpi__stxe, ormer__ecdym.
                        target, ormer__ecdym.loc)
            for txty__bmb in ormer__ecdym.list_vars():
                if (txty__bmb.name in her__jso and txty__bmb.name !=
                    agpm__ihhit):
                    del her__jso[txty__bmb.name]
            new_body.append(ormer__ecdym)
        cfrpv__zoklk.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    jssjt__vlipq = keyword_expr.items.copy()
    udble__wct = keyword_expr.value_indexes
    for gpdty__qwy, kbihb__txn in udble__wct.items():
        jssjt__vlipq[kbihb__txn] = gpdty__qwy, jssjt__vlipq[kbihb__txn][1]
    new_body[buildmap_idx] = None
    return jssjt__vlipq


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    vnzsl__lnlqp = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    jssjt__vlipq = []
    lixon__nguh = buildmap_idx + 1
    while lixon__nguh <= search_end:
        nrvjo__knbvk = body[lixon__nguh]
        if not (isinstance(nrvjo__knbvk, ir.Assign) and isinstance(
            nrvjo__knbvk.value, ir.Const)):
            raise UnsupportedError(vnzsl__lnlqp)
        xbmxn__bdxr = nrvjo__knbvk.target.name
        xod__ofk = nrvjo__knbvk.value.value
        lixon__nguh += 1
        itr__gmlih = True
        while lixon__nguh <= search_end and itr__gmlih:
            fdzh__ecv = body[lixon__nguh]
            if (isinstance(fdzh__ecv, ir.Assign) and isinstance(fdzh__ecv.
                value, ir.Expr) and fdzh__ecv.value.op == 'getattr' and 
                fdzh__ecv.value.value.name == buildmap_name and fdzh__ecv.
                value.attr == '__setitem__'):
                itr__gmlih = False
            else:
                lixon__nguh += 1
        if itr__gmlih or lixon__nguh == search_end:
            raise UnsupportedError(vnzsl__lnlqp)
        pwm__udqyp = body[lixon__nguh + 1]
        if not (isinstance(pwm__udqyp, ir.Assign) and isinstance(pwm__udqyp
            .value, ir.Expr) and pwm__udqyp.value.op == 'call' and 
            pwm__udqyp.value.func.name == fdzh__ecv.target.name and len(
            pwm__udqyp.value.args) == 2 and pwm__udqyp.value.args[0].name ==
            xbmxn__bdxr):
            raise UnsupportedError(vnzsl__lnlqp)
        ezmz__kie = pwm__udqyp.value.args[1]
        jssjt__vlipq.append((xod__ofk, ezmz__kie))
        new_body[lixon__nguh] = None
        new_body[lixon__nguh + 1] = None
        lixon__nguh += 2
    return jssjt__vlipq


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    vnzsl__lnlqp = 'CALL_FUNCTION_EX with **kwargs not supported'
    lixon__nguh = 0
    hbtbs__kpj = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        ixp__gdr = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        ixp__gdr = vararg_stmt.target.name
    tiw__wnhot = True
    while search_end >= lixon__nguh and tiw__wnhot:
        olvae__tybi = body[search_end]
        if (isinstance(olvae__tybi, ir.Assign) and olvae__tybi.target.name ==
            ixp__gdr and isinstance(olvae__tybi.value, ir.Expr) and 
            olvae__tybi.value.op == 'build_tuple' and not olvae__tybi.value
            .items):
            tiw__wnhot = False
            new_body[search_end] = None
        else:
            if search_end == lixon__nguh or not (isinstance(olvae__tybi, ir
                .Assign) and olvae__tybi.target.name == ixp__gdr and
                isinstance(olvae__tybi.value, ir.Expr) and olvae__tybi.
                value.op == 'binop' and olvae__tybi.value.fn == operator.add):
                raise UnsupportedError(vnzsl__lnlqp)
            bqp__djm = olvae__tybi.value.lhs.name
            klq__ogug = olvae__tybi.value.rhs.name
            njdh__zbjlx = body[search_end - 1]
            if not (isinstance(njdh__zbjlx, ir.Assign) and isinstance(
                njdh__zbjlx.value, ir.Expr) and njdh__zbjlx.value.op ==
                'build_tuple' and len(njdh__zbjlx.value.items) == 1):
                raise UnsupportedError(vnzsl__lnlqp)
            if njdh__zbjlx.target.name == bqp__djm:
                ixp__gdr = klq__ogug
            elif njdh__zbjlx.target.name == klq__ogug:
                ixp__gdr = bqp__djm
            else:
                raise UnsupportedError(vnzsl__lnlqp)
            hbtbs__kpj.append(njdh__zbjlx.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            ntw__osy = True
            while search_end >= lixon__nguh and ntw__osy:
                razca__jlpss = body[search_end]
                if isinstance(razca__jlpss, ir.Assign
                    ) and razca__jlpss.target.name == ixp__gdr:
                    ntw__osy = False
                else:
                    search_end -= 1
    if tiw__wnhot:
        raise UnsupportedError(vnzsl__lnlqp)
    return hbtbs__kpj[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    vnzsl__lnlqp = 'CALL_FUNCTION_EX with **kwargs not supported'
    for cfrpv__zoklk in func_ir.blocks.values():
        lttk__rtvn = False
        new_body = []
        for ywck__btvfm, ormer__ecdym in enumerate(cfrpv__zoklk.body):
            if (isinstance(ormer__ecdym, ir.Assign) and isinstance(
                ormer__ecdym.value, ir.Expr) and ormer__ecdym.value.op ==
                'call' and ormer__ecdym.value.varkwarg is not None):
                lttk__rtvn = True
                dkn__iwc = ormer__ecdym.value
                args = dkn__iwc.args
                jssjt__vlipq = dkn__iwc.kws
                sznu__jbfgl = dkn__iwc.vararg
                podrg__qlycb = dkn__iwc.varkwarg
                ffju__rdjd = ywck__btvfm - 1
                ipz__ephlw = ffju__rdjd
                irl__vuzkh = None
                tymr__rwjt = True
                while ipz__ephlw >= 0 and tymr__rwjt:
                    irl__vuzkh = cfrpv__zoklk.body[ipz__ephlw]
                    if isinstance(irl__vuzkh, ir.Assign
                        ) and irl__vuzkh.target.name == podrg__qlycb.name:
                        tymr__rwjt = False
                    else:
                        ipz__ephlw -= 1
                if jssjt__vlipq or tymr__rwjt or not (isinstance(irl__vuzkh
                    .value, ir.Expr) and irl__vuzkh.value.op == 'build_map'):
                    raise UnsupportedError(vnzsl__lnlqp)
                if irl__vuzkh.value.items:
                    jssjt__vlipq = _call_function_ex_replace_kws_small(
                        irl__vuzkh.value, new_body, ipz__ephlw)
                else:
                    jssjt__vlipq = _call_function_ex_replace_kws_large(
                        cfrpv__zoklk.body, podrg__qlycb.name, ipz__ephlw, 
                        ywck__btvfm - 1, new_body)
                ffju__rdjd = ipz__ephlw
                if sznu__jbfgl is not None:
                    if args:
                        raise UnsupportedError(vnzsl__lnlqp)
                    hal__zgfuj = ffju__rdjd
                    fqq__zaty = None
                    tymr__rwjt = True
                    while hal__zgfuj >= 0 and tymr__rwjt:
                        fqq__zaty = cfrpv__zoklk.body[hal__zgfuj]
                        if isinstance(fqq__zaty, ir.Assign
                            ) and fqq__zaty.target.name == sznu__jbfgl.name:
                            tymr__rwjt = False
                        else:
                            hal__zgfuj -= 1
                    if tymr__rwjt:
                        raise UnsupportedError(vnzsl__lnlqp)
                    if isinstance(fqq__zaty.value, ir.Expr
                        ) and fqq__zaty.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(fqq__zaty
                            .value, new_body, hal__zgfuj)
                    else:
                        args = _call_function_ex_replace_args_large(fqq__zaty,
                            cfrpv__zoklk.body, new_body, hal__zgfuj)
                jvrr__nscam = ir.Expr.call(dkn__iwc.func, args,
                    jssjt__vlipq, dkn__iwc.loc, target=dkn__iwc.target)
                if ormer__ecdym.target.name in func_ir._definitions and len(
                    func_ir._definitions[ormer__ecdym.target.name]) == 1:
                    func_ir._definitions[ormer__ecdym.target.name].clear()
                func_ir._definitions[ormer__ecdym.target.name].append(
                    jvrr__nscam)
                ormer__ecdym = ir.Assign(jvrr__nscam, ormer__ecdym.target,
                    ormer__ecdym.loc)
            new_body.append(ormer__ecdym)
        if lttk__rtvn:
            cfrpv__zoklk.body = [mrpuy__jdl for mrpuy__jdl in new_body if 
                mrpuy__jdl is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for cfrpv__zoklk in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        lttk__rtvn = False
        for ywck__btvfm, ormer__ecdym in enumerate(cfrpv__zoklk.body):
            utwv__uwf = True
            dfqk__pkxdg = None
            if isinstance(ormer__ecdym, ir.Assign) and isinstance(ormer__ecdym
                .value, ir.Expr):
                if ormer__ecdym.value.op == 'build_map':
                    dfqk__pkxdg = ormer__ecdym.target.name
                    lit_old_idx[ormer__ecdym.target.name] = ywck__btvfm
                    lit_new_idx[ormer__ecdym.target.name] = ywck__btvfm
                    map_updates[ormer__ecdym.target.name
                        ] = ormer__ecdym.value.items.copy()
                    utwv__uwf = False
                elif ormer__ecdym.value.op == 'call' and ywck__btvfm > 0:
                    sodec__aupt = ormer__ecdym.value.func.name
                    fdzh__ecv = cfrpv__zoklk.body[ywck__btvfm - 1]
                    args = ormer__ecdym.value.args
                    if (isinstance(fdzh__ecv, ir.Assign) and fdzh__ecv.
                        target.name == sodec__aupt and isinstance(fdzh__ecv
                        .value, ir.Expr) and fdzh__ecv.value.op ==
                        'getattr' and fdzh__ecv.value.value.name in lit_old_idx
                        ):
                        arjh__xuje = fdzh__ecv.value.value.name
                        yzdc__grzg = fdzh__ecv.value.attr
                        if yzdc__grzg == '__setitem__':
                            utwv__uwf = False
                            map_updates[arjh__xuje].append(args)
                            new_body[-1] = None
                        elif yzdc__grzg == 'update' and args[0
                            ].name in lit_old_idx:
                            utwv__uwf = False
                            map_updates[arjh__xuje].extend(map_updates[args
                                [0].name])
                            new_body[-1] = None
                        if not utwv__uwf:
                            lit_new_idx[arjh__xuje] = ywck__btvfm
                            func_ir._definitions[fdzh__ecv.target.name].remove(
                                fdzh__ecv.value)
            if not (isinstance(ormer__ecdym, ir.Assign) and isinstance(
                ormer__ecdym.value, ir.Expr) and ormer__ecdym.value.op ==
                'getattr' and ormer__ecdym.value.value.name in lit_old_idx and
                ormer__ecdym.value.attr in ('__setitem__', 'update')):
                for txty__bmb in ormer__ecdym.list_vars():
                    if (txty__bmb.name in lit_old_idx and txty__bmb.name !=
                        dfqk__pkxdg):
                        _insert_build_map(func_ir, txty__bmb.name,
                            cfrpv__zoklk.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if utwv__uwf:
                new_body.append(ormer__ecdym)
            else:
                func_ir._definitions[ormer__ecdym.target.name].remove(
                    ormer__ecdym.value)
                lttk__rtvn = True
                new_body.append(None)
        nblto__qmz = list(lit_old_idx.keys())
        for ppn__ohxc in nblto__qmz:
            _insert_build_map(func_ir, ppn__ohxc, cfrpv__zoklk.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if lttk__rtvn:
            cfrpv__zoklk.body = [mrpuy__jdl for mrpuy__jdl in new_body if 
                mrpuy__jdl is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    woh__zupr = lit_old_idx[name]
    nqzm__bqb = lit_new_idx[name]
    zjy__gljny = map_updates[name]
    new_body[nqzm__bqb] = _build_new_build_map(func_ir, name, old_body,
        woh__zupr, zjy__gljny)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    acure__naf = old_body[old_lineno]
    uch__icdny = acure__naf.target
    njhlm__dltgc = acure__naf.value
    ocdy__fiw = []
    ysmpv__psnmo = []
    for lqsen__orx in new_items:
        ukxak__vfbnu, wfxy__raf = lqsen__orx
        jhmsa__iuml = guard(get_definition, func_ir, ukxak__vfbnu)
        if isinstance(jhmsa__iuml, (ir.Const, ir.Global, ir.FreeVar)):
            ocdy__fiw.append(jhmsa__iuml.value)
        ufq__xorzw = guard(get_definition, func_ir, wfxy__raf)
        if isinstance(ufq__xorzw, (ir.Const, ir.Global, ir.FreeVar)):
            ysmpv__psnmo.append(ufq__xorzw.value)
        else:
            ysmpv__psnmo.append(numba.core.interpreter._UNKNOWN_VALUE(
                wfxy__raf.name))
    udble__wct = {}
    if len(ocdy__fiw) == len(new_items):
        ivhb__wqpo = {mrpuy__jdl: flmxh__owy for mrpuy__jdl, flmxh__owy in
            zip(ocdy__fiw, ysmpv__psnmo)}
        for ywck__btvfm, ukxak__vfbnu in enumerate(ocdy__fiw):
            udble__wct[ukxak__vfbnu] = ywck__btvfm
    else:
        ivhb__wqpo = None
    sqkm__qtiil = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=ivhb__wqpo, value_indexes=udble__wct, loc=
        njhlm__dltgc.loc)
    func_ir._definitions[name].append(sqkm__qtiil)
    return ir.Assign(sqkm__qtiil, ir.Var(uch__icdny.scope, name, uch__icdny
        .loc), sqkm__qtiil.loc)
