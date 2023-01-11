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
    for txcly__jql in func_ir.blocks.values():
        new_body = []
        dgde__mtlzf = {}
        for ikii__pgxsu, fpil__njct in enumerate(txcly__jql.body):
            plcfc__ztw = None
            if isinstance(fpil__njct, ir.Assign) and isinstance(fpil__njct.
                value, ir.Expr):
                jyh__uqa = fpil__njct.target.name
                if fpil__njct.value.op == 'build_tuple':
                    plcfc__ztw = jyh__uqa
                    dgde__mtlzf[jyh__uqa] = fpil__njct.value.items
                elif fpil__njct.value.op == 'binop' and fpil__njct.value.fn == operator.add and fpil__njct.value.lhs.name in dgde__mtlzf and fpil__njct.value.rhs.name in dgde__mtlzf:
                    plcfc__ztw = jyh__uqa
                    new_items = dgde__mtlzf[fpil__njct.value.lhs.name
                        ] + dgde__mtlzf[fpil__njct.value.rhs.name]
                    yxa__grj = ir.Expr.build_tuple(new_items, fpil__njct.
                        value.loc)
                    dgde__mtlzf[jyh__uqa] = new_items
                    del dgde__mtlzf[fpil__njct.value.lhs.name]
                    del dgde__mtlzf[fpil__njct.value.rhs.name]
                    if fpil__njct.value in func_ir._definitions[jyh__uqa]:
                        func_ir._definitions[jyh__uqa].remove(fpil__njct.value)
                    func_ir._definitions[jyh__uqa].append(yxa__grj)
                    fpil__njct = ir.Assign(yxa__grj, fpil__njct.target,
                        fpil__njct.loc)
            for drs__vfgf in fpil__njct.list_vars():
                if (drs__vfgf.name in dgde__mtlzf and drs__vfgf.name !=
                    plcfc__ztw):
                    del dgde__mtlzf[drs__vfgf.name]
            new_body.append(fpil__njct)
        txcly__jql.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    gilq__cqhfb = keyword_expr.items.copy()
    vtlr__sotfm = keyword_expr.value_indexes
    for lfcx__vid, gekn__vjf in vtlr__sotfm.items():
        gilq__cqhfb[gekn__vjf] = lfcx__vid, gilq__cqhfb[gekn__vjf][1]
    new_body[buildmap_idx] = None
    return gilq__cqhfb


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    nedxv__opgnf = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    gilq__cqhfb = []
    avog__wfds = buildmap_idx + 1
    while avog__wfds <= search_end:
        atng__wrsh = body[avog__wfds]
        if not (isinstance(atng__wrsh, ir.Assign) and isinstance(atng__wrsh
            .value, ir.Const)):
            raise UnsupportedError(nedxv__opgnf)
        iemo__ezf = atng__wrsh.target.name
        ihb__bfx = atng__wrsh.value.value
        avog__wfds += 1
        hlp__oigyw = True
        while avog__wfds <= search_end and hlp__oigyw:
            ztu__wgm = body[avog__wfds]
            if (isinstance(ztu__wgm, ir.Assign) and isinstance(ztu__wgm.
                value, ir.Expr) and ztu__wgm.value.op == 'getattr' and 
                ztu__wgm.value.value.name == buildmap_name and ztu__wgm.
                value.attr == '__setitem__'):
                hlp__oigyw = False
            else:
                avog__wfds += 1
        if hlp__oigyw or avog__wfds == search_end:
            raise UnsupportedError(nedxv__opgnf)
        jmg__czncr = body[avog__wfds + 1]
        if not (isinstance(jmg__czncr, ir.Assign) and isinstance(jmg__czncr
            .value, ir.Expr) and jmg__czncr.value.op == 'call' and 
            jmg__czncr.value.func.name == ztu__wgm.target.name and len(
            jmg__czncr.value.args) == 2 and jmg__czncr.value.args[0].name ==
            iemo__ezf):
            raise UnsupportedError(nedxv__opgnf)
        gmm__fgqn = jmg__czncr.value.args[1]
        gilq__cqhfb.append((ihb__bfx, gmm__fgqn))
        new_body[avog__wfds] = None
        new_body[avog__wfds + 1] = None
        avog__wfds += 2
    return gilq__cqhfb


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    nedxv__opgnf = 'CALL_FUNCTION_EX with **kwargs not supported'
    avog__wfds = 0
    ussx__dtqe = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        cop__odh = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        cop__odh = vararg_stmt.target.name
    ftnt__xjc = True
    while search_end >= avog__wfds and ftnt__xjc:
        yuauk__pgt = body[search_end]
        if (isinstance(yuauk__pgt, ir.Assign) and yuauk__pgt.target.name ==
            cop__odh and isinstance(yuauk__pgt.value, ir.Expr) and 
            yuauk__pgt.value.op == 'build_tuple' and not yuauk__pgt.value.items
            ):
            ftnt__xjc = False
            new_body[search_end] = None
        else:
            if search_end == avog__wfds or not (isinstance(yuauk__pgt, ir.
                Assign) and yuauk__pgt.target.name == cop__odh and
                isinstance(yuauk__pgt.value, ir.Expr) and yuauk__pgt.value.
                op == 'binop' and yuauk__pgt.value.fn == operator.add):
                raise UnsupportedError(nedxv__opgnf)
            yny__onon = yuauk__pgt.value.lhs.name
            mfwd__ylq = yuauk__pgt.value.rhs.name
            xjmx__pbmyf = body[search_end - 1]
            if not (isinstance(xjmx__pbmyf, ir.Assign) and isinstance(
                xjmx__pbmyf.value, ir.Expr) and xjmx__pbmyf.value.op ==
                'build_tuple' and len(xjmx__pbmyf.value.items) == 1):
                raise UnsupportedError(nedxv__opgnf)
            if xjmx__pbmyf.target.name == yny__onon:
                cop__odh = mfwd__ylq
            elif xjmx__pbmyf.target.name == mfwd__ylq:
                cop__odh = yny__onon
            else:
                raise UnsupportedError(nedxv__opgnf)
            ussx__dtqe.append(xjmx__pbmyf.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            lwyp__ignj = True
            while search_end >= avog__wfds and lwyp__ignj:
                ckn__tjs = body[search_end]
                if isinstance(ckn__tjs, ir.Assign
                    ) and ckn__tjs.target.name == cop__odh:
                    lwyp__ignj = False
                else:
                    search_end -= 1
    if ftnt__xjc:
        raise UnsupportedError(nedxv__opgnf)
    return ussx__dtqe[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    nedxv__opgnf = 'CALL_FUNCTION_EX with **kwargs not supported'
    for txcly__jql in func_ir.blocks.values():
        exq__tdhib = False
        new_body = []
        for ikii__pgxsu, fpil__njct in enumerate(txcly__jql.body):
            if (isinstance(fpil__njct, ir.Assign) and isinstance(fpil__njct
                .value, ir.Expr) and fpil__njct.value.op == 'call' and 
                fpil__njct.value.varkwarg is not None):
                exq__tdhib = True
                wps__xtp = fpil__njct.value
                args = wps__xtp.args
                gilq__cqhfb = wps__xtp.kws
                mcxmw__osznc = wps__xtp.vararg
                nwhh__lng = wps__xtp.varkwarg
                ntek__cjq = ikii__pgxsu - 1
                osrm__exjrl = ntek__cjq
                ahkmr__fwcom = None
                yzfpn__xzeq = True
                while osrm__exjrl >= 0 and yzfpn__xzeq:
                    ahkmr__fwcom = txcly__jql.body[osrm__exjrl]
                    if isinstance(ahkmr__fwcom, ir.Assign
                        ) and ahkmr__fwcom.target.name == nwhh__lng.name:
                        yzfpn__xzeq = False
                    else:
                        osrm__exjrl -= 1
                if gilq__cqhfb or yzfpn__xzeq or not (isinstance(
                    ahkmr__fwcom.value, ir.Expr) and ahkmr__fwcom.value.op ==
                    'build_map'):
                    raise UnsupportedError(nedxv__opgnf)
                if ahkmr__fwcom.value.items:
                    gilq__cqhfb = _call_function_ex_replace_kws_small(
                        ahkmr__fwcom.value, new_body, osrm__exjrl)
                else:
                    gilq__cqhfb = _call_function_ex_replace_kws_large(
                        txcly__jql.body, nwhh__lng.name, osrm__exjrl, 
                        ikii__pgxsu - 1, new_body)
                ntek__cjq = osrm__exjrl
                if mcxmw__osznc is not None:
                    if args:
                        raise UnsupportedError(nedxv__opgnf)
                    garlv__pdru = ntek__cjq
                    lhrjx__qky = None
                    yzfpn__xzeq = True
                    while garlv__pdru >= 0 and yzfpn__xzeq:
                        lhrjx__qky = txcly__jql.body[garlv__pdru]
                        if isinstance(lhrjx__qky, ir.Assign
                            ) and lhrjx__qky.target.name == mcxmw__osznc.name:
                            yzfpn__xzeq = False
                        else:
                            garlv__pdru -= 1
                    if yzfpn__xzeq:
                        raise UnsupportedError(nedxv__opgnf)
                    if isinstance(lhrjx__qky.value, ir.Expr
                        ) and lhrjx__qky.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(lhrjx__qky
                            .value, new_body, garlv__pdru)
                    else:
                        args = _call_function_ex_replace_args_large(lhrjx__qky,
                            txcly__jql.body, new_body, garlv__pdru)
                scov__nybp = ir.Expr.call(wps__xtp.func, args, gilq__cqhfb,
                    wps__xtp.loc, target=wps__xtp.target)
                if fpil__njct.target.name in func_ir._definitions and len(
                    func_ir._definitions[fpil__njct.target.name]) == 1:
                    func_ir._definitions[fpil__njct.target.name].clear()
                func_ir._definitions[fpil__njct.target.name].append(scov__nybp)
                fpil__njct = ir.Assign(scov__nybp, fpil__njct.target,
                    fpil__njct.loc)
            new_body.append(fpil__njct)
        if exq__tdhib:
            txcly__jql.body = [kbchv__rgfe for kbchv__rgfe in new_body if 
                kbchv__rgfe is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for txcly__jql in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        exq__tdhib = False
        for ikii__pgxsu, fpil__njct in enumerate(txcly__jql.body):
            hnw__wvx = True
            bbwmo__tdox = None
            if isinstance(fpil__njct, ir.Assign) and isinstance(fpil__njct.
                value, ir.Expr):
                if fpil__njct.value.op == 'build_map':
                    bbwmo__tdox = fpil__njct.target.name
                    lit_old_idx[fpil__njct.target.name] = ikii__pgxsu
                    lit_new_idx[fpil__njct.target.name] = ikii__pgxsu
                    map_updates[fpil__njct.target.name
                        ] = fpil__njct.value.items.copy()
                    hnw__wvx = False
                elif fpil__njct.value.op == 'call' and ikii__pgxsu > 0:
                    zdlli__zpp = fpil__njct.value.func.name
                    ztu__wgm = txcly__jql.body[ikii__pgxsu - 1]
                    args = fpil__njct.value.args
                    if (isinstance(ztu__wgm, ir.Assign) and ztu__wgm.target
                        .name == zdlli__zpp and isinstance(ztu__wgm.value,
                        ir.Expr) and ztu__wgm.value.op == 'getattr' and 
                        ztu__wgm.value.value.name in lit_old_idx):
                        ydlej__evg = ztu__wgm.value.value.name
                        gvlnv__ccsm = ztu__wgm.value.attr
                        if gvlnv__ccsm == '__setitem__':
                            hnw__wvx = False
                            map_updates[ydlej__evg].append(args)
                            new_body[-1] = None
                        elif gvlnv__ccsm == 'update' and args[0
                            ].name in lit_old_idx:
                            hnw__wvx = False
                            map_updates[ydlej__evg].extend(map_updates[args
                                [0].name])
                            new_body[-1] = None
                        if not hnw__wvx:
                            lit_new_idx[ydlej__evg] = ikii__pgxsu
                            func_ir._definitions[ztu__wgm.target.name].remove(
                                ztu__wgm.value)
            if not (isinstance(fpil__njct, ir.Assign) and isinstance(
                fpil__njct.value, ir.Expr) and fpil__njct.value.op ==
                'getattr' and fpil__njct.value.value.name in lit_old_idx and
                fpil__njct.value.attr in ('__setitem__', 'update')):
                for drs__vfgf in fpil__njct.list_vars():
                    if (drs__vfgf.name in lit_old_idx and drs__vfgf.name !=
                        bbwmo__tdox):
                        _insert_build_map(func_ir, drs__vfgf.name,
                            txcly__jql.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if hnw__wvx:
                new_body.append(fpil__njct)
            else:
                func_ir._definitions[fpil__njct.target.name].remove(fpil__njct
                    .value)
                exq__tdhib = True
                new_body.append(None)
        phoj__ndzbf = list(lit_old_idx.keys())
        for sta__dyf in phoj__ndzbf:
            _insert_build_map(func_ir, sta__dyf, txcly__jql.body, new_body,
                lit_old_idx, lit_new_idx, map_updates)
        if exq__tdhib:
            txcly__jql.body = [kbchv__rgfe for kbchv__rgfe in new_body if 
                kbchv__rgfe is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    shdak__bcxe = lit_old_idx[name]
    ija__svmfi = lit_new_idx[name]
    wxr__gilsr = map_updates[name]
    new_body[ija__svmfi] = _build_new_build_map(func_ir, name, old_body,
        shdak__bcxe, wxr__gilsr)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    rjx__agl = old_body[old_lineno]
    zna__nhxz = rjx__agl.target
    vfz__plx = rjx__agl.value
    iii__ickyp = []
    upncy__chlrb = []
    for bee__bpgp in new_items:
        yywl__ouu, cqe__wfco = bee__bpgp
        lolhd__nugau = guard(get_definition, func_ir, yywl__ouu)
        if isinstance(lolhd__nugau, (ir.Const, ir.Global, ir.FreeVar)):
            iii__ickyp.append(lolhd__nugau.value)
        bfwrn__rfu = guard(get_definition, func_ir, cqe__wfco)
        if isinstance(bfwrn__rfu, (ir.Const, ir.Global, ir.FreeVar)):
            upncy__chlrb.append(bfwrn__rfu.value)
        else:
            upncy__chlrb.append(numba.core.interpreter._UNKNOWN_VALUE(
                cqe__wfco.name))
    vtlr__sotfm = {}
    if len(iii__ickyp) == len(new_items):
        rarc__vrq = {kbchv__rgfe: atyio__qhw for kbchv__rgfe, atyio__qhw in
            zip(iii__ickyp, upncy__chlrb)}
        for ikii__pgxsu, yywl__ouu in enumerate(iii__ickyp):
            vtlr__sotfm[yywl__ouu] = ikii__pgxsu
    else:
        rarc__vrq = None
    uxww__ylftu = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=rarc__vrq, value_indexes=vtlr__sotfm, loc=vfz__plx.loc)
    func_ir._definitions[name].append(uxww__ylftu)
    return ir.Assign(uxww__ylftu, ir.Var(zna__nhxz.scope, name, zna__nhxz.
        loc), uxww__ylftu.loc)
