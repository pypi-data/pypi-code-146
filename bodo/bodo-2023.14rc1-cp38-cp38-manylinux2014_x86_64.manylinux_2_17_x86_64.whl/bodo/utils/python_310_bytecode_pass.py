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
    for hrjx__jbwee in func_ir.blocks.values():
        new_body = []
        vbe__slpn = {}
        for ogx__fewro, cbc__tzxv in enumerate(hrjx__jbwee.body):
            jed__mfg = None
            if isinstance(cbc__tzxv, ir.Assign) and isinstance(cbc__tzxv.
                value, ir.Expr):
                jwrf__zjg = cbc__tzxv.target.name
                if cbc__tzxv.value.op == 'build_tuple':
                    jed__mfg = jwrf__zjg
                    vbe__slpn[jwrf__zjg] = cbc__tzxv.value.items
                elif cbc__tzxv.value.op == 'binop' and cbc__tzxv.value.fn == operator.add and cbc__tzxv.value.lhs.name in vbe__slpn and cbc__tzxv.value.rhs.name in vbe__slpn:
                    jed__mfg = jwrf__zjg
                    new_items = vbe__slpn[cbc__tzxv.value.lhs.name
                        ] + vbe__slpn[cbc__tzxv.value.rhs.name]
                    cnynt__rvwjz = ir.Expr.build_tuple(new_items, cbc__tzxv
                        .value.loc)
                    vbe__slpn[jwrf__zjg] = new_items
                    del vbe__slpn[cbc__tzxv.value.lhs.name]
                    del vbe__slpn[cbc__tzxv.value.rhs.name]
                    if cbc__tzxv.value in func_ir._definitions[jwrf__zjg]:
                        func_ir._definitions[jwrf__zjg].remove(cbc__tzxv.value)
                    func_ir._definitions[jwrf__zjg].append(cnynt__rvwjz)
                    cbc__tzxv = ir.Assign(cnynt__rvwjz, cbc__tzxv.target,
                        cbc__tzxv.loc)
            for lpwp__cxsq in cbc__tzxv.list_vars():
                if (lpwp__cxsq.name in vbe__slpn and lpwp__cxsq.name !=
                    jed__mfg):
                    del vbe__slpn[lpwp__cxsq.name]
            new_body.append(cbc__tzxv)
        hrjx__jbwee.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    idl__sqe = keyword_expr.items.copy()
    lzxu__cwony = keyword_expr.value_indexes
    for dvxc__kmnzf, jhre__hkdus in lzxu__cwony.items():
        idl__sqe[jhre__hkdus] = dvxc__kmnzf, idl__sqe[jhre__hkdus][1]
    new_body[buildmap_idx] = None
    return idl__sqe


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    zlf__okasc = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    idl__sqe = []
    avdao__isqa = buildmap_idx + 1
    while avdao__isqa <= search_end:
        vyaaz__lpf = body[avdao__isqa]
        if not (isinstance(vyaaz__lpf, ir.Assign) and isinstance(vyaaz__lpf
            .value, ir.Const)):
            raise UnsupportedError(zlf__okasc)
        zta__xwoz = vyaaz__lpf.target.name
        cjjby__nxv = vyaaz__lpf.value.value
        avdao__isqa += 1
        innc__ofd = True
        while avdao__isqa <= search_end and innc__ofd:
            xdg__svaft = body[avdao__isqa]
            if (isinstance(xdg__svaft, ir.Assign) and isinstance(xdg__svaft
                .value, ir.Expr) and xdg__svaft.value.op == 'getattr' and 
                xdg__svaft.value.value.name == buildmap_name and xdg__svaft
                .value.attr == '__setitem__'):
                innc__ofd = False
            else:
                avdao__isqa += 1
        if innc__ofd or avdao__isqa == search_end:
            raise UnsupportedError(zlf__okasc)
        onc__jgpx = body[avdao__isqa + 1]
        if not (isinstance(onc__jgpx, ir.Assign) and isinstance(onc__jgpx.
            value, ir.Expr) and onc__jgpx.value.op == 'call' and onc__jgpx.
            value.func.name == xdg__svaft.target.name and len(onc__jgpx.
            value.args) == 2 and onc__jgpx.value.args[0].name == zta__xwoz):
            raise UnsupportedError(zlf__okasc)
        ciu__wkokw = onc__jgpx.value.args[1]
        idl__sqe.append((cjjby__nxv, ciu__wkokw))
        new_body[avdao__isqa] = None
        new_body[avdao__isqa + 1] = None
        avdao__isqa += 2
    return idl__sqe


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    zlf__okasc = 'CALL_FUNCTION_EX with **kwargs not supported'
    avdao__isqa = 0
    hjakc__stzt = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        rwew__reuqe = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        rwew__reuqe = vararg_stmt.target.name
    azy__hsgcq = True
    while search_end >= avdao__isqa and azy__hsgcq:
        ulidp__zrr = body[search_end]
        if (isinstance(ulidp__zrr, ir.Assign) and ulidp__zrr.target.name ==
            rwew__reuqe and isinstance(ulidp__zrr.value, ir.Expr) and 
            ulidp__zrr.value.op == 'build_tuple' and not ulidp__zrr.value.items
            ):
            azy__hsgcq = False
            new_body[search_end] = None
        else:
            if search_end == avdao__isqa or not (isinstance(ulidp__zrr, ir.
                Assign) and ulidp__zrr.target.name == rwew__reuqe and
                isinstance(ulidp__zrr.value, ir.Expr) and ulidp__zrr.value.
                op == 'binop' and ulidp__zrr.value.fn == operator.add):
                raise UnsupportedError(zlf__okasc)
            ckbq__yvy = ulidp__zrr.value.lhs.name
            zckzc__senj = ulidp__zrr.value.rhs.name
            fgx__wfp = body[search_end - 1]
            if not (isinstance(fgx__wfp, ir.Assign) and isinstance(fgx__wfp
                .value, ir.Expr) and fgx__wfp.value.op == 'build_tuple' and
                len(fgx__wfp.value.items) == 1):
                raise UnsupportedError(zlf__okasc)
            if fgx__wfp.target.name == ckbq__yvy:
                rwew__reuqe = zckzc__senj
            elif fgx__wfp.target.name == zckzc__senj:
                rwew__reuqe = ckbq__yvy
            else:
                raise UnsupportedError(zlf__okasc)
            hjakc__stzt.append(fgx__wfp.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            teag__cdd = True
            while search_end >= avdao__isqa and teag__cdd:
                cfzxo__civ = body[search_end]
                if isinstance(cfzxo__civ, ir.Assign
                    ) and cfzxo__civ.target.name == rwew__reuqe:
                    teag__cdd = False
                else:
                    search_end -= 1
    if azy__hsgcq:
        raise UnsupportedError(zlf__okasc)
    return hjakc__stzt[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    zlf__okasc = 'CALL_FUNCTION_EX with **kwargs not supported'
    for hrjx__jbwee in func_ir.blocks.values():
        pxun__wwjlo = False
        new_body = []
        for ogx__fewro, cbc__tzxv in enumerate(hrjx__jbwee.body):
            if (isinstance(cbc__tzxv, ir.Assign) and isinstance(cbc__tzxv.
                value, ir.Expr) and cbc__tzxv.value.op == 'call' and 
                cbc__tzxv.value.varkwarg is not None):
                pxun__wwjlo = True
                klmq__yhtlm = cbc__tzxv.value
                args = klmq__yhtlm.args
                idl__sqe = klmq__yhtlm.kws
                wbcz__rlu = klmq__yhtlm.vararg
                rsifw__acigu = klmq__yhtlm.varkwarg
                yfoik__krzvb = ogx__fewro - 1
                rqyhp__dgs = yfoik__krzvb
                srca__munf = None
                juqc__qjcj = True
                while rqyhp__dgs >= 0 and juqc__qjcj:
                    srca__munf = hrjx__jbwee.body[rqyhp__dgs]
                    if isinstance(srca__munf, ir.Assign
                        ) and srca__munf.target.name == rsifw__acigu.name:
                        juqc__qjcj = False
                    else:
                        rqyhp__dgs -= 1
                if idl__sqe or juqc__qjcj or not (isinstance(srca__munf.
                    value, ir.Expr) and srca__munf.value.op == 'build_map'):
                    raise UnsupportedError(zlf__okasc)
                if srca__munf.value.items:
                    idl__sqe = _call_function_ex_replace_kws_small(srca__munf
                        .value, new_body, rqyhp__dgs)
                else:
                    idl__sqe = _call_function_ex_replace_kws_large(hrjx__jbwee
                        .body, rsifw__acigu.name, rqyhp__dgs, ogx__fewro - 
                        1, new_body)
                yfoik__krzvb = rqyhp__dgs
                if wbcz__rlu is not None:
                    if args:
                        raise UnsupportedError(zlf__okasc)
                    vua__dkry = yfoik__krzvb
                    egegs__hwflm = None
                    juqc__qjcj = True
                    while vua__dkry >= 0 and juqc__qjcj:
                        egegs__hwflm = hrjx__jbwee.body[vua__dkry]
                        if isinstance(egegs__hwflm, ir.Assign
                            ) and egegs__hwflm.target.name == wbcz__rlu.name:
                            juqc__qjcj = False
                        else:
                            vua__dkry -= 1
                    if juqc__qjcj:
                        raise UnsupportedError(zlf__okasc)
                    if isinstance(egegs__hwflm.value, ir.Expr
                        ) and egegs__hwflm.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(
                            egegs__hwflm.value, new_body, vua__dkry)
                    else:
                        args = _call_function_ex_replace_args_large(
                            egegs__hwflm, hrjx__jbwee.body, new_body, vua__dkry
                            )
                aar__bawqz = ir.Expr.call(klmq__yhtlm.func, args, idl__sqe,
                    klmq__yhtlm.loc, target=klmq__yhtlm.target)
                if cbc__tzxv.target.name in func_ir._definitions and len(
                    func_ir._definitions[cbc__tzxv.target.name]) == 1:
                    func_ir._definitions[cbc__tzxv.target.name].clear()
                func_ir._definitions[cbc__tzxv.target.name].append(aar__bawqz)
                cbc__tzxv = ir.Assign(aar__bawqz, cbc__tzxv.target,
                    cbc__tzxv.loc)
            new_body.append(cbc__tzxv)
        if pxun__wwjlo:
            hrjx__jbwee.body = [ontcf__qabhr for ontcf__qabhr in new_body if
                ontcf__qabhr is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for hrjx__jbwee in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        pxun__wwjlo = False
        for ogx__fewro, cbc__tzxv in enumerate(hrjx__jbwee.body):
            ieokp__cknmk = True
            dav__zefpy = None
            if isinstance(cbc__tzxv, ir.Assign) and isinstance(cbc__tzxv.
                value, ir.Expr):
                if cbc__tzxv.value.op == 'build_map':
                    dav__zefpy = cbc__tzxv.target.name
                    lit_old_idx[cbc__tzxv.target.name] = ogx__fewro
                    lit_new_idx[cbc__tzxv.target.name] = ogx__fewro
                    map_updates[cbc__tzxv.target.name
                        ] = cbc__tzxv.value.items.copy()
                    ieokp__cknmk = False
                elif cbc__tzxv.value.op == 'call' and ogx__fewro > 0:
                    saunx__wavvn = cbc__tzxv.value.func.name
                    xdg__svaft = hrjx__jbwee.body[ogx__fewro - 1]
                    args = cbc__tzxv.value.args
                    if (isinstance(xdg__svaft, ir.Assign) and xdg__svaft.
                        target.name == saunx__wavvn and isinstance(
                        xdg__svaft.value, ir.Expr) and xdg__svaft.value.op ==
                        'getattr' and xdg__svaft.value.value.name in
                        lit_old_idx):
                        pfnzc__xuerm = xdg__svaft.value.value.name
                        njuo__xib = xdg__svaft.value.attr
                        if njuo__xib == '__setitem__':
                            ieokp__cknmk = False
                            map_updates[pfnzc__xuerm].append(args)
                            new_body[-1] = None
                        elif njuo__xib == 'update' and args[0
                            ].name in lit_old_idx:
                            ieokp__cknmk = False
                            map_updates[pfnzc__xuerm].extend(map_updates[
                                args[0].name])
                            new_body[-1] = None
                        if not ieokp__cknmk:
                            lit_new_idx[pfnzc__xuerm] = ogx__fewro
                            func_ir._definitions[xdg__svaft.target.name
                                ].remove(xdg__svaft.value)
            if not (isinstance(cbc__tzxv, ir.Assign) and isinstance(
                cbc__tzxv.value, ir.Expr) and cbc__tzxv.value.op ==
                'getattr' and cbc__tzxv.value.value.name in lit_old_idx and
                cbc__tzxv.value.attr in ('__setitem__', 'update')):
                for lpwp__cxsq in cbc__tzxv.list_vars():
                    if (lpwp__cxsq.name in lit_old_idx and lpwp__cxsq.name !=
                        dav__zefpy):
                        _insert_build_map(func_ir, lpwp__cxsq.name,
                            hrjx__jbwee.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if ieokp__cknmk:
                new_body.append(cbc__tzxv)
            else:
                func_ir._definitions[cbc__tzxv.target.name].remove(cbc__tzxv
                    .value)
                pxun__wwjlo = True
                new_body.append(None)
        bzav__jlb = list(lit_old_idx.keys())
        for qgu__thawb in bzav__jlb:
            _insert_build_map(func_ir, qgu__thawb, hrjx__jbwee.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if pxun__wwjlo:
            hrjx__jbwee.body = [ontcf__qabhr for ontcf__qabhr in new_body if
                ontcf__qabhr is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    ghu__wxlo = lit_old_idx[name]
    xhgx__ngc = lit_new_idx[name]
    wczv__thac = map_updates[name]
    new_body[xhgx__ngc] = _build_new_build_map(func_ir, name, old_body,
        ghu__wxlo, wczv__thac)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    tsml__esi = old_body[old_lineno]
    giyi__cnndp = tsml__esi.target
    tjlan__xepbd = tsml__esi.value
    eodd__pbc = []
    aggid__pdjas = []
    for nylc__acpe in new_items:
        rbjn__ykzz, ouadp__lhq = nylc__acpe
        afm__nkx = guard(get_definition, func_ir, rbjn__ykzz)
        if isinstance(afm__nkx, (ir.Const, ir.Global, ir.FreeVar)):
            eodd__pbc.append(afm__nkx.value)
        hwk__qnl = guard(get_definition, func_ir, ouadp__lhq)
        if isinstance(hwk__qnl, (ir.Const, ir.Global, ir.FreeVar)):
            aggid__pdjas.append(hwk__qnl.value)
        else:
            aggid__pdjas.append(numba.core.interpreter._UNKNOWN_VALUE(
                ouadp__lhq.name))
    lzxu__cwony = {}
    if len(eodd__pbc) == len(new_items):
        ktacw__hfqj = {ontcf__qabhr: wtrf__ebzi for ontcf__qabhr,
            wtrf__ebzi in zip(eodd__pbc, aggid__pdjas)}
        for ogx__fewro, rbjn__ykzz in enumerate(eodd__pbc):
            lzxu__cwony[rbjn__ykzz] = ogx__fewro
    else:
        ktacw__hfqj = None
    idbh__uiil = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=ktacw__hfqj, value_indexes=lzxu__cwony, loc=
        tjlan__xepbd.loc)
    func_ir._definitions[name].append(idbh__uiil)
    return ir.Assign(idbh__uiil, ir.Var(giyi__cnndp.scope, name,
        giyi__cnndp.loc), idbh__uiil.loc)
