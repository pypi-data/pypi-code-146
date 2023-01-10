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
    for aks__qla in func_ir.blocks.values():
        new_body = []
        vwwxr__joat = {}
        for yccad__vzt, ukg__qrw in enumerate(aks__qla.body):
            nxrj__nqb = None
            if isinstance(ukg__qrw, ir.Assign) and isinstance(ukg__qrw.
                value, ir.Expr):
                tgrm__fqi = ukg__qrw.target.name
                if ukg__qrw.value.op == 'build_tuple':
                    nxrj__nqb = tgrm__fqi
                    vwwxr__joat[tgrm__fqi] = ukg__qrw.value.items
                elif ukg__qrw.value.op == 'binop' and ukg__qrw.value.fn == operator.add and ukg__qrw.value.lhs.name in vwwxr__joat and ukg__qrw.value.rhs.name in vwwxr__joat:
                    nxrj__nqb = tgrm__fqi
                    new_items = vwwxr__joat[ukg__qrw.value.lhs.name
                        ] + vwwxr__joat[ukg__qrw.value.rhs.name]
                    gnzez__oxo = ir.Expr.build_tuple(new_items, ukg__qrw.
                        value.loc)
                    vwwxr__joat[tgrm__fqi] = new_items
                    del vwwxr__joat[ukg__qrw.value.lhs.name]
                    del vwwxr__joat[ukg__qrw.value.rhs.name]
                    if ukg__qrw.value in func_ir._definitions[tgrm__fqi]:
                        func_ir._definitions[tgrm__fqi].remove(ukg__qrw.value)
                    func_ir._definitions[tgrm__fqi].append(gnzez__oxo)
                    ukg__qrw = ir.Assign(gnzez__oxo, ukg__qrw.target,
                        ukg__qrw.loc)
            for nigr__ldiz in ukg__qrw.list_vars():
                if (nigr__ldiz.name in vwwxr__joat and nigr__ldiz.name !=
                    nxrj__nqb):
                    del vwwxr__joat[nigr__ldiz.name]
            new_body.append(ukg__qrw)
        aks__qla.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    suyc__kuzd = keyword_expr.items.copy()
    rgrd__lpv = keyword_expr.value_indexes
    for xnq__vquhl, rtqy__ysl in rgrd__lpv.items():
        suyc__kuzd[rtqy__ysl] = xnq__vquhl, suyc__kuzd[rtqy__ysl][1]
    new_body[buildmap_idx] = None
    return suyc__kuzd


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    ufd__kpd = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    suyc__kuzd = []
    fgzhr__pvbu = buildmap_idx + 1
    while fgzhr__pvbu <= search_end:
        fdfd__hau = body[fgzhr__pvbu]
        if not (isinstance(fdfd__hau, ir.Assign) and isinstance(fdfd__hau.
            value, ir.Const)):
            raise UnsupportedError(ufd__kpd)
        irttx__kyo = fdfd__hau.target.name
        miwkl__foiw = fdfd__hau.value.value
        fgzhr__pvbu += 1
        aqt__hme = True
        while fgzhr__pvbu <= search_end and aqt__hme:
            agoq__vtyw = body[fgzhr__pvbu]
            if (isinstance(agoq__vtyw, ir.Assign) and isinstance(agoq__vtyw
                .value, ir.Expr) and agoq__vtyw.value.op == 'getattr' and 
                agoq__vtyw.value.value.name == buildmap_name and agoq__vtyw
                .value.attr == '__setitem__'):
                aqt__hme = False
            else:
                fgzhr__pvbu += 1
        if aqt__hme or fgzhr__pvbu == search_end:
            raise UnsupportedError(ufd__kpd)
        xkl__syvw = body[fgzhr__pvbu + 1]
        if not (isinstance(xkl__syvw, ir.Assign) and isinstance(xkl__syvw.
            value, ir.Expr) and xkl__syvw.value.op == 'call' and xkl__syvw.
            value.func.name == agoq__vtyw.target.name and len(xkl__syvw.
            value.args) == 2 and xkl__syvw.value.args[0].name == irttx__kyo):
            raise UnsupportedError(ufd__kpd)
        otm__sqmsq = xkl__syvw.value.args[1]
        suyc__kuzd.append((miwkl__foiw, otm__sqmsq))
        new_body[fgzhr__pvbu] = None
        new_body[fgzhr__pvbu + 1] = None
        fgzhr__pvbu += 2
    return suyc__kuzd


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    ufd__kpd = 'CALL_FUNCTION_EX with **kwargs not supported'
    fgzhr__pvbu = 0
    ihvtd__imw = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        dwjxa__qsk = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        dwjxa__qsk = vararg_stmt.target.name
    pibfu__xlrc = True
    while search_end >= fgzhr__pvbu and pibfu__xlrc:
        xtvd__tfv = body[search_end]
        if (isinstance(xtvd__tfv, ir.Assign) and xtvd__tfv.target.name ==
            dwjxa__qsk and isinstance(xtvd__tfv.value, ir.Expr) and 
            xtvd__tfv.value.op == 'build_tuple' and not xtvd__tfv.value.items):
            pibfu__xlrc = False
            new_body[search_end] = None
        else:
            if search_end == fgzhr__pvbu or not (isinstance(xtvd__tfv, ir.
                Assign) and xtvd__tfv.target.name == dwjxa__qsk and
                isinstance(xtvd__tfv.value, ir.Expr) and xtvd__tfv.value.op ==
                'binop' and xtvd__tfv.value.fn == operator.add):
                raise UnsupportedError(ufd__kpd)
            stg__duuit = xtvd__tfv.value.lhs.name
            cyey__rzqjb = xtvd__tfv.value.rhs.name
            gegq__quwyd = body[search_end - 1]
            if not (isinstance(gegq__quwyd, ir.Assign) and isinstance(
                gegq__quwyd.value, ir.Expr) and gegq__quwyd.value.op ==
                'build_tuple' and len(gegq__quwyd.value.items) == 1):
                raise UnsupportedError(ufd__kpd)
            if gegq__quwyd.target.name == stg__duuit:
                dwjxa__qsk = cyey__rzqjb
            elif gegq__quwyd.target.name == cyey__rzqjb:
                dwjxa__qsk = stg__duuit
            else:
                raise UnsupportedError(ufd__kpd)
            ihvtd__imw.append(gegq__quwyd.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            vqx__hwvy = True
            while search_end >= fgzhr__pvbu and vqx__hwvy:
                stu__abs = body[search_end]
                if isinstance(stu__abs, ir.Assign
                    ) and stu__abs.target.name == dwjxa__qsk:
                    vqx__hwvy = False
                else:
                    search_end -= 1
    if pibfu__xlrc:
        raise UnsupportedError(ufd__kpd)
    return ihvtd__imw[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    ufd__kpd = 'CALL_FUNCTION_EX with **kwargs not supported'
    for aks__qla in func_ir.blocks.values():
        wyn__jxqrd = False
        new_body = []
        for yccad__vzt, ukg__qrw in enumerate(aks__qla.body):
            if (isinstance(ukg__qrw, ir.Assign) and isinstance(ukg__qrw.
                value, ir.Expr) and ukg__qrw.value.op == 'call' and 
                ukg__qrw.value.varkwarg is not None):
                wyn__jxqrd = True
                cmu__xtls = ukg__qrw.value
                args = cmu__xtls.args
                suyc__kuzd = cmu__xtls.kws
                fqjzt__ppu = cmu__xtls.vararg
                elok__slbqg = cmu__xtls.varkwarg
                usr__rev = yccad__vzt - 1
                scgv__rjtt = usr__rev
                nklm__ejt = None
                eno__cpcm = True
                while scgv__rjtt >= 0 and eno__cpcm:
                    nklm__ejt = aks__qla.body[scgv__rjtt]
                    if isinstance(nklm__ejt, ir.Assign
                        ) and nklm__ejt.target.name == elok__slbqg.name:
                        eno__cpcm = False
                    else:
                        scgv__rjtt -= 1
                if suyc__kuzd or eno__cpcm or not (isinstance(nklm__ejt.
                    value, ir.Expr) and nklm__ejt.value.op == 'build_map'):
                    raise UnsupportedError(ufd__kpd)
                if nklm__ejt.value.items:
                    suyc__kuzd = _call_function_ex_replace_kws_small(nklm__ejt
                        .value, new_body, scgv__rjtt)
                else:
                    suyc__kuzd = _call_function_ex_replace_kws_large(aks__qla
                        .body, elok__slbqg.name, scgv__rjtt, yccad__vzt - 1,
                        new_body)
                usr__rev = scgv__rjtt
                if fqjzt__ppu is not None:
                    if args:
                        raise UnsupportedError(ufd__kpd)
                    rylnb__avrj = usr__rev
                    keysy__xyraw = None
                    eno__cpcm = True
                    while rylnb__avrj >= 0 and eno__cpcm:
                        keysy__xyraw = aks__qla.body[rylnb__avrj]
                        if isinstance(keysy__xyraw, ir.Assign
                            ) and keysy__xyraw.target.name == fqjzt__ppu.name:
                            eno__cpcm = False
                        else:
                            rylnb__avrj -= 1
                    if eno__cpcm:
                        raise UnsupportedError(ufd__kpd)
                    if isinstance(keysy__xyraw.value, ir.Expr
                        ) and keysy__xyraw.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(
                            keysy__xyraw.value, new_body, rylnb__avrj)
                    else:
                        args = _call_function_ex_replace_args_large(
                            keysy__xyraw, aks__qla.body, new_body, rylnb__avrj)
                cgr__jbq = ir.Expr.call(cmu__xtls.func, args, suyc__kuzd,
                    cmu__xtls.loc, target=cmu__xtls.target)
                if ukg__qrw.target.name in func_ir._definitions and len(func_ir
                    ._definitions[ukg__qrw.target.name]) == 1:
                    func_ir._definitions[ukg__qrw.target.name].clear()
                func_ir._definitions[ukg__qrw.target.name].append(cgr__jbq)
                ukg__qrw = ir.Assign(cgr__jbq, ukg__qrw.target, ukg__qrw.loc)
            new_body.append(ukg__qrw)
        if wyn__jxqrd:
            aks__qla.body = [chgpz__manz for chgpz__manz in new_body if 
                chgpz__manz is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for aks__qla in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        wyn__jxqrd = False
        for yccad__vzt, ukg__qrw in enumerate(aks__qla.body):
            mcxod__xwf = True
            qdkq__qbavr = None
            if isinstance(ukg__qrw, ir.Assign) and isinstance(ukg__qrw.
                value, ir.Expr):
                if ukg__qrw.value.op == 'build_map':
                    qdkq__qbavr = ukg__qrw.target.name
                    lit_old_idx[ukg__qrw.target.name] = yccad__vzt
                    lit_new_idx[ukg__qrw.target.name] = yccad__vzt
                    map_updates[ukg__qrw.target.name
                        ] = ukg__qrw.value.items.copy()
                    mcxod__xwf = False
                elif ukg__qrw.value.op == 'call' and yccad__vzt > 0:
                    vhl__adg = ukg__qrw.value.func.name
                    agoq__vtyw = aks__qla.body[yccad__vzt - 1]
                    args = ukg__qrw.value.args
                    if (isinstance(agoq__vtyw, ir.Assign) and agoq__vtyw.
                        target.name == vhl__adg and isinstance(agoq__vtyw.
                        value, ir.Expr) and agoq__vtyw.value.op ==
                        'getattr' and agoq__vtyw.value.value.name in
                        lit_old_idx):
                        qcni__mpnw = agoq__vtyw.value.value.name
                        whyx__xgz = agoq__vtyw.value.attr
                        if whyx__xgz == '__setitem__':
                            mcxod__xwf = False
                            map_updates[qcni__mpnw].append(args)
                            new_body[-1] = None
                        elif whyx__xgz == 'update' and args[0
                            ].name in lit_old_idx:
                            mcxod__xwf = False
                            map_updates[qcni__mpnw].extend(map_updates[args
                                [0].name])
                            new_body[-1] = None
                        if not mcxod__xwf:
                            lit_new_idx[qcni__mpnw] = yccad__vzt
                            func_ir._definitions[agoq__vtyw.target.name
                                ].remove(agoq__vtyw.value)
            if not (isinstance(ukg__qrw, ir.Assign) and isinstance(ukg__qrw
                .value, ir.Expr) and ukg__qrw.value.op == 'getattr' and 
                ukg__qrw.value.value.name in lit_old_idx and ukg__qrw.value
                .attr in ('__setitem__', 'update')):
                for nigr__ldiz in ukg__qrw.list_vars():
                    if (nigr__ldiz.name in lit_old_idx and nigr__ldiz.name !=
                        qdkq__qbavr):
                        _insert_build_map(func_ir, nigr__ldiz.name,
                            aks__qla.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if mcxod__xwf:
                new_body.append(ukg__qrw)
            else:
                func_ir._definitions[ukg__qrw.target.name].remove(ukg__qrw.
                    value)
                wyn__jxqrd = True
                new_body.append(None)
        frwa__azr = list(lit_old_idx.keys())
        for hakk__yyoxe in frwa__azr:
            _insert_build_map(func_ir, hakk__yyoxe, aks__qla.body, new_body,
                lit_old_idx, lit_new_idx, map_updates)
        if wyn__jxqrd:
            aks__qla.body = [chgpz__manz for chgpz__manz in new_body if 
                chgpz__manz is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    wuqk__djro = lit_old_idx[name]
    xftzc__nttk = lit_new_idx[name]
    rzm__codne = map_updates[name]
    new_body[xftzc__nttk] = _build_new_build_map(func_ir, name, old_body,
        wuqk__djro, rzm__codne)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    cwcx__sao = old_body[old_lineno]
    qblb__snsk = cwcx__sao.target
    dzd__jog = cwcx__sao.value
    ackwn__mxjj = []
    dzi__rbmjj = []
    for bhzst__rlpkn in new_items:
        mqpzi__sujw, qtdox__aayh = bhzst__rlpkn
        niksx__oghb = guard(get_definition, func_ir, mqpzi__sujw)
        if isinstance(niksx__oghb, (ir.Const, ir.Global, ir.FreeVar)):
            ackwn__mxjj.append(niksx__oghb.value)
        smfm__oah = guard(get_definition, func_ir, qtdox__aayh)
        if isinstance(smfm__oah, (ir.Const, ir.Global, ir.FreeVar)):
            dzi__rbmjj.append(smfm__oah.value)
        else:
            dzi__rbmjj.append(numba.core.interpreter._UNKNOWN_VALUE(
                qtdox__aayh.name))
    rgrd__lpv = {}
    if len(ackwn__mxjj) == len(new_items):
        zjszq__kimm = {chgpz__manz: ifbyg__vihnc for chgpz__manz,
            ifbyg__vihnc in zip(ackwn__mxjj, dzi__rbmjj)}
        for yccad__vzt, mqpzi__sujw in enumerate(ackwn__mxjj):
            rgrd__lpv[mqpzi__sujw] = yccad__vzt
    else:
        zjszq__kimm = None
    vfzqz__ltiv = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=zjszq__kimm, value_indexes=rgrd__lpv, loc=dzd__jog.loc)
    func_ir._definitions[name].append(vfzqz__ltiv)
    return ir.Assign(vfzqz__ltiv, ir.Var(qblb__snsk.scope, name, qblb__snsk
        .loc), vfzqz__ltiv.loc)
