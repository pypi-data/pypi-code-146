"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.boxing
import numba.core.inline_closurecall
import numba.core.typing.listdecl
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.compiler import Compiler
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, get_definition, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
from bodo.utils.python_310_bytecode_pass import Bodo310ByteCodePass, peep_hole_call_function_ex_to_call_function_kw, peep_hole_fuse_dict_add_updates, peep_hole_fuse_tuple_adds
from bodo.utils.typing import BodoError, get_overload_const_str, is_overload_constant_str, raise_bodo_error
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    from numba.core.utils import PYVERSION
    stam__hobno = numba.core.bytecode.FunctionIdentity.from_function(func)
    vfr__umgio = numba.core.interpreter.Interpreter(stam__hobno)
    wmkv__lrqqe = numba.core.bytecode.ByteCode(func_id=stam__hobno)
    func_ir = vfr__umgio.interpret(wmkv__lrqqe)
    if PYVERSION == (3, 10):
        func_ir = peep_hole_call_function_ex_to_call_function_kw(func_ir)
        func_ir = peep_hole_fuse_dict_add_updates(func_ir)
        func_ir = peep_hole_fuse_tuple_adds(func_ir)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        udnm__liae = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        udnm__liae.run()
    dnp__zpdi = numba.core.postproc.PostProcessor(func_ir)
    dnp__zpdi.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, xpq__rdgiz in visit_vars_extensions.items():
        if isinstance(stmt, t):
            xpq__rdgiz(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    urvvy__cmyr = ['ravel', 'transpose', 'reshape']
    for dvdom__uvad in blocks.values():
        for ruq__agsmo in dvdom__uvad.body:
            if type(ruq__agsmo) in alias_analysis_extensions:
                xpq__rdgiz = alias_analysis_extensions[type(ruq__agsmo)]
                xpq__rdgiz(ruq__agsmo, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(ruq__agsmo, ir.Assign):
                dxzy__bjlyj = ruq__agsmo.value
                ybdb__btgfz = ruq__agsmo.target.name
                if is_immutable_type(ybdb__btgfz, typemap):
                    continue
                if isinstance(dxzy__bjlyj, ir.Var
                    ) and ybdb__btgfz != dxzy__bjlyj.name:
                    _add_alias(ybdb__btgfz, dxzy__bjlyj.name, alias_map,
                        arg_aliases)
                if isinstance(dxzy__bjlyj, ir.Expr) and (dxzy__bjlyj.op ==
                    'cast' or dxzy__bjlyj.op in ['getitem', 'static_getitem']):
                    _add_alias(ybdb__btgfz, dxzy__bjlyj.value.name,
                        alias_map, arg_aliases)
                if isinstance(dxzy__bjlyj, ir.Expr
                    ) and dxzy__bjlyj.op == 'inplace_binop':
                    _add_alias(ybdb__btgfz, dxzy__bjlyj.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(dxzy__bjlyj, ir.Expr
                    ) and dxzy__bjlyj.op == 'getattr' and dxzy__bjlyj.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(ybdb__btgfz, dxzy__bjlyj.value.name,
                        alias_map, arg_aliases)
                if isinstance(dxzy__bjlyj, ir.Expr
                    ) and dxzy__bjlyj.op == 'getattr' and dxzy__bjlyj.attr not in [
                    'shape'] and dxzy__bjlyj.value.name in arg_aliases:
                    _add_alias(ybdb__btgfz, dxzy__bjlyj.value.name,
                        alias_map, arg_aliases)
                if isinstance(dxzy__bjlyj, ir.Expr
                    ) and dxzy__bjlyj.op == 'getattr' and dxzy__bjlyj.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(ybdb__btgfz, dxzy__bjlyj.value.name,
                        alias_map, arg_aliases)
                if isinstance(dxzy__bjlyj, ir.Expr) and dxzy__bjlyj.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(ybdb__btgfz, typemap):
                    for pxv__lvr in dxzy__bjlyj.items:
                        _add_alias(ybdb__btgfz, pxv__lvr.name, alias_map,
                            arg_aliases)
                if isinstance(dxzy__bjlyj, ir.Expr
                    ) and dxzy__bjlyj.op == 'call':
                    rndxl__obe = guard(find_callname, func_ir, dxzy__bjlyj,
                        typemap)
                    if rndxl__obe is None:
                        continue
                    rnk__bcd, fll__tcw = rndxl__obe
                    if rndxl__obe in alias_func_extensions:
                        lnui__eetj = alias_func_extensions[rndxl__obe]
                        lnui__eetj(ybdb__btgfz, dxzy__bjlyj.args, alias_map,
                            arg_aliases)
                    if fll__tcw == 'numpy' and rnk__bcd in urvvy__cmyr:
                        _add_alias(ybdb__btgfz, dxzy__bjlyj.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(fll__tcw, ir.Var
                        ) and rnk__bcd in urvvy__cmyr:
                        _add_alias(ybdb__btgfz, fll__tcw.name, alias_map,
                            arg_aliases)
    lchk__bcd = copy.deepcopy(alias_map)
    for pxv__lvr in lchk__bcd:
        for hjyvn__cgwxe in lchk__bcd[pxv__lvr]:
            alias_map[pxv__lvr] |= alias_map[hjyvn__cgwxe]
        for hjyvn__cgwxe in lchk__bcd[pxv__lvr]:
            alias_map[hjyvn__cgwxe] = alias_map[pxv__lvr]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e6cf3e0f502f903453eb98346fc6854f87dc4ea1ac62f65c2d6aef3bf690b6c5':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
numba.parfors.array_analysis.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    fcfvb__gcea = compute_cfg_from_blocks(func_ir.blocks)
    bszok__bqq = compute_use_defs(func_ir.blocks)
    jtnx__rpmq = compute_live_map(fcfvb__gcea, func_ir.blocks, bszok__bqq.
        usemap, bszok__bqq.defmap)
    jfoh__rljdl = True
    while jfoh__rljdl:
        jfoh__rljdl = False
        for label, block in func_ir.blocks.items():
            lives = {pxv__lvr.name for pxv__lvr in block.terminator.list_vars()
                }
            for gtx__jbvix, dhku__rar in fcfvb__gcea.successors(label):
                lives |= jtnx__rpmq[gtx__jbvix]
            klgm__zvfsa = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    ybdb__btgfz = stmt.target
                    siqay__wmf = stmt.value
                    if ybdb__btgfz.name not in lives:
                        if isinstance(siqay__wmf, ir.Expr
                            ) and siqay__wmf.op == 'make_function':
                            continue
                        if isinstance(siqay__wmf, ir.Expr
                            ) and siqay__wmf.op == 'getattr':
                            continue
                        if isinstance(siqay__wmf, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(ybdb__btgfz,
                            None), types.Function):
                            continue
                        if isinstance(siqay__wmf, ir.Expr
                            ) and siqay__wmf.op == 'build_map':
                            continue
                        if isinstance(siqay__wmf, ir.Expr
                            ) and siqay__wmf.op == 'build_tuple':
                            continue
                        if isinstance(siqay__wmf, ir.Expr
                            ) and siqay__wmf.op == 'binop':
                            continue
                        if isinstance(siqay__wmf, ir.Expr
                            ) and siqay__wmf.op == 'unary':
                            continue
                        if isinstance(siqay__wmf, ir.Expr
                            ) and siqay__wmf.op in ('static_getitem', 'getitem'
                            ):
                            continue
                    if isinstance(siqay__wmf, ir.Var
                        ) and ybdb__btgfz.name == siqay__wmf.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    hoa__ghaj = analysis.ir_extension_usedefs[type(stmt)]
                    jkmuq__kpp, paxl__fqlk = hoa__ghaj(stmt)
                    lives -= paxl__fqlk
                    lives |= jkmuq__kpp
                else:
                    lives |= {pxv__lvr.name for pxv__lvr in stmt.list_vars()}
                    if isinstance(stmt, ir.Assign):
                        wlqw__agvm = set()
                        if isinstance(siqay__wmf, ir.Expr):
                            wlqw__agvm = {pxv__lvr.name for pxv__lvr in
                                siqay__wmf.list_vars()}
                        if ybdb__btgfz.name not in wlqw__agvm:
                            lives.remove(ybdb__btgfz.name)
                klgm__zvfsa.append(stmt)
            klgm__zvfsa.reverse()
            if len(block.body) != len(klgm__zvfsa):
                jfoh__rljdl = True
            block.body = klgm__zvfsa


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    srqe__pkxbr = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (srqe__pkxbr,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    wpaus__qfa = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), wpaus__qfa)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for qhaz__rnpxn in fnty.templates:
                self._inline_overloads.update(qhaz__rnpxn._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    name = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    wpaus__qfa = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), wpaus__qfa)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    vwhkt__pmb, fvr__drms = self._get_impl(args, kws)
    if vwhkt__pmb is None:
        return
    exo__dyfrr = types.Dispatcher(vwhkt__pmb)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        zmjq__zwh = vwhkt__pmb._compiler
        flags = compiler.Flags()
        ybe__ldb = zmjq__zwh.targetdescr.typing_context
        lwsuk__qog = zmjq__zwh.targetdescr.target_context
        bfp__wmvtd = zmjq__zwh.pipeline_class(ybe__ldb, lwsuk__qog, None,
            None, None, flags, None)
        ymd__sepm = InlineWorker(ybe__ldb, lwsuk__qog, zmjq__zwh.locals,
            bfp__wmvtd, flags, None)
        ibc__pwbng = exo__dyfrr.dispatcher.get_call_template
        qhaz__rnpxn, lxa__afiff, zueb__dcc, kws = ibc__pwbng(fvr__drms, kws)
        if zueb__dcc in self._inline_overloads:
            return self._inline_overloads[zueb__dcc]['iinfo'].signature
        ir = ymd__sepm.run_untyped_passes(exo__dyfrr.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, lwsuk__qog, ir, zueb__dcc, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, zueb__dcc, None)
        self._inline_overloads[sig.args] = {'folded_args': zueb__dcc}
        xmzvi__qeu = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = xmzvi__qeu
        if not self._inline.is_always_inline:
            sig = exo__dyfrr.get_call_type(self.context, fvr__drms, kws)
            self._compiled_overloads[sig.args] = exo__dyfrr.get_overload(sig)
        kytxb__cpps = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': zueb__dcc,
            'iinfo': kytxb__cpps}
    else:
        sig = exo__dyfrr.get_call_type(self.context, fvr__drms, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = exo__dyfrr.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core import utils
    iqxq__sdr = [True, False]
    azi__uklj = [False, True]
    kxs__lghy = _ResolutionFailures(context, self, args, kws, depth=self._depth
        )
    from numba.core.target_extension import get_local_target
    vooz__fef = get_local_target(context)
    ympl__rxo = utils.order_by_target_specificity(vooz__fef, self.templates,
        fnkey=self.key[0])
    self._depth += 1
    for mmog__yzqd in ympl__rxo:
        hqom__vxudk = mmog__yzqd(context)
        xafsv__bqc = iqxq__sdr if hqom__vxudk.prefer_literal else azi__uklj
        xafsv__bqc = [True] if getattr(hqom__vxudk, '_no_unliteral', False
            ) else xafsv__bqc
        for ouu__rlbu in xafsv__bqc:
            try:
                if ouu__rlbu:
                    sig = hqom__vxudk.apply(args, kws)
                else:
                    ntch__qvhvn = tuple([_unlit_non_poison(a) for a in args])
                    fuuf__qtwhc = {jap__cuf: _unlit_non_poison(pxv__lvr) for
                        jap__cuf, pxv__lvr in kws.items()}
                    sig = hqom__vxudk.apply(ntch__qvhvn, fuuf__qtwhc)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    kxs__lghy.add_error(hqom__vxudk, False, e, ouu__rlbu)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = hqom__vxudk.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    ddmp__dzkvo = getattr(hqom__vxudk, 'cases', None)
                    if ddmp__dzkvo is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            ddmp__dzkvo)
                    else:
                        msg = 'No match.'
                    kxs__lghy.add_error(hqom__vxudk, True, msg, ouu__rlbu)
    kxs__lghy.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '25f038a7216f8e6f40068ea81e11fd9af8ad25d19888f7304a549941b01b7015':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    qhaz__rnpxn = self.template(context)
    jinu__mvyi = None
    crmvg__zill = None
    bdkq__hmkmb = None
    xafsv__bqc = [True, False] if qhaz__rnpxn.prefer_literal else [False, True]
    xafsv__bqc = [True] if getattr(qhaz__rnpxn, '_no_unliteral', False
        ) else xafsv__bqc
    for ouu__rlbu in xafsv__bqc:
        if ouu__rlbu:
            try:
                bdkq__hmkmb = qhaz__rnpxn.apply(args, kws)
            except Exception as cwwim__niw:
                if isinstance(cwwim__niw, errors.ForceLiteralArg):
                    raise cwwim__niw
                jinu__mvyi = cwwim__niw
                bdkq__hmkmb = None
            else:
                break
        else:
            qhr__qbhe = tuple([_unlit_non_poison(a) for a in args])
            ial__axkk = {jap__cuf: _unlit_non_poison(pxv__lvr) for jap__cuf,
                pxv__lvr in kws.items()}
            hew__bdc = qhr__qbhe == args and kws == ial__axkk
            if not hew__bdc and bdkq__hmkmb is None:
                try:
                    bdkq__hmkmb = qhaz__rnpxn.apply(qhr__qbhe, ial__axkk)
                except Exception as cwwim__niw:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        cwwim__niw, errors.NumbaError):
                        raise cwwim__niw
                    if isinstance(cwwim__niw, errors.ForceLiteralArg):
                        if qhaz__rnpxn.prefer_literal:
                            raise cwwim__niw
                    crmvg__zill = cwwim__niw
                else:
                    break
    if bdkq__hmkmb is None and (crmvg__zill is not None or jinu__mvyi is not
        None):
        vdxzh__ydfkk = '- Resolution failure for {} arguments:\n{}\n'
        ieo__ovb = _termcolor.highlight(vdxzh__ydfkk)
        if numba.core.config.DEVELOPER_MODE:
            wefx__atvbd = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    ebefa__rre = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    ebefa__rre = ['']
                dst__nxkli = '\n{}'.format(2 * wefx__atvbd)
                ktc__njshi = _termcolor.reset(dst__nxkli + dst__nxkli.join(
                    _bt_as_lines(ebefa__rre)))
                return _termcolor.reset(ktc__njshi)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            dnhgq__pmova = str(e)
            dnhgq__pmova = dnhgq__pmova if dnhgq__pmova else str(repr(e)
                ) + add_bt(e)
            vxxnq__yfp = errors.TypingError(textwrap.dedent(dnhgq__pmova))
            return ieo__ovb.format(literalness, str(vxxnq__yfp))
        import bodo
        if isinstance(jinu__mvyi, bodo.utils.typing.BodoError):
            raise jinu__mvyi
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', jinu__mvyi) +
                nested_msg('non-literal', crmvg__zill))
        else:
            if 'missing a required argument' in jinu__mvyi.msg:
                msg = 'missing a required argument'
            else:
                msg = 'Compilation error for '
                if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                    DataFrameType):
                    msg += 'DataFrame.'
                elif isinstance(self.this, bodo.hiframes.pd_series_ext.
                    SeriesType):
                    msg += 'Series.'
                msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg, loc=jinu__mvyi.loc)
    return bdkq__hmkmb


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '502cd77c0084452e903a45a0f1f8107550bfbde7179363b57dabd617ce135f4a':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite import ir as lir
    fnty = lir.FunctionType(self.pyobj, [self.cstring, self.py_ssize_t])
    rnk__bcd = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=rnk__bcd)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            kwsvt__mse = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), kwsvt__mse)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    hahp__kdsud = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            hahp__kdsud.append(types.Omitted(a.value))
        else:
            hahp__kdsud.append(self.typeof_pyval(a))
    gypgu__veg = None
    try:
        error = None
        gypgu__veg = self.compile(tuple(hahp__kdsud))
    except errors.ForceLiteralArg as e:
        exlw__eeuo = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if exlw__eeuo:
            qcqnx__jsm = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            bnl__yneai = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(exlw__eeuo))
            raise errors.CompilerError(qcqnx__jsm.format(bnl__yneai))
        fvr__drms = []
        try:
            for i, pxv__lvr in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        fvr__drms.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        fvr__drms.append(types.literal(args[i]))
                else:
                    fvr__drms.append(args[i])
            args = fvr__drms
        except (OSError, FileNotFoundError) as bzuvy__uzik:
            error = FileNotFoundError(str(bzuvy__uzik) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                gypgu__veg = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        mecq__ikyu = []
        for i, khmwo__xxzo in enumerate(args):
            val = khmwo__xxzo.value if isinstance(khmwo__xxzo, numba.core.
                dispatcher.OmittedArg) else khmwo__xxzo
            try:
                lacr__zkkcb = typeof(val, Purpose.argument)
            except ValueError as whk__buonx:
                mecq__ikyu.append((i, str(whk__buonx)))
            else:
                if lacr__zkkcb is None:
                    mecq__ikyu.append((i,
                        f'cannot determine Numba type of value {val}'))
        if mecq__ikyu:
            djbm__nws = '\n'.join(f'- argument {i}: {gcgub__tlz}' for i,
                gcgub__tlz in mecq__ikyu)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{djbm__nws}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                gjuyv__jaek = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                qdr__nzcby = False
                for gqfc__srfo in gjuyv__jaek:
                    if gqfc__srfo in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        qdr__nzcby = True
                        break
                if not qdr__nzcby:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                kwsvt__mse = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), kwsvt__mse)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return gypgu__veg


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for ehta__zep in cres.library._codegen._engine._defined_symbols:
        if ehta__zep.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in ehta__zep and (
            'bodo_gb_udf_update_local' in ehta__zep or 
            'bodo_gb_udf_combine' in ehta__zep or 'bodo_gb_udf_eval' in
            ehta__zep or 'bodo_gb_apply_general_udfs' in ehta__zep):
            gb_agg_cfunc_addr[ehta__zep
                ] = cres.library.get_pointer_to_function(ehta__zep)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for ehta__zep in cres.library._codegen._engine._defined_symbols:
        if ehta__zep.startswith('cfunc') and ('get_join_cond_addr' not in
            ehta__zep or 'bodo_join_gen_cond' in ehta__zep):
            join_gen_cond_cfunc_addr[ehta__zep
                ] = cres.library.get_pointer_to_function(ehta__zep)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    vwhkt__pmb = self._get_dispatcher_for_current_target()
    if vwhkt__pmb is not self:
        return vwhkt__pmb.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, return_type = sigutils.normalize_signature(sig)
            sxmg__yzb = self.overloads.get(tuple(args))
            if sxmg__yzb is not None:
                return sxmg__yzb.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            cpbw__frrq = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=cpbw__frrq):
                try:
                    cres = self._compiler.compile(args, return_type)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
                if bodo.get_rank() == 0:
                    self._cache.save_overload(sig, cres)
            else:
                nvvdg__jya = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in nvvdg__jya:
                    self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    rvj__qdy = self._final_module
    lmezk__bzfcv = []
    hbvb__bqld = 0
    for fn in rvj__qdy.functions:
        hbvb__bqld += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            lmezk__bzfcv.append(fn.name)
    if hbvb__bqld == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if lmezk__bzfcv:
        rvj__qdy = rvj__qdy.clone()
        for name in lmezk__bzfcv:
            rvj__qdy.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = rvj__qdy
    return rvj__qdy


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for mjk__hca in self.constraints:
        loc = mjk__hca.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                mjk__hca(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                aoaz__wmmp = numba.core.errors.TypingError(str(e), loc=
                    mjk__hca.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(aoaz__wmmp, e))
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                from numba.core import utils
                if utils.use_old_style_errors():
                    numba.core.typeinfer._logger.debug('captured error',
                        exc_info=e)
                    msg = """Internal error at {con}.
{err}
Enable logging at debug level for details."""
                    aoaz__wmmp = numba.core.errors.TypingError(msg.format(
                        con=mjk__hca, err=str(e)), loc=mjk__hca.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(aoaz__wmmp, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = (
                        f"Unknown CAPTURED_ERRORS style: '{numba.core.config.CAPTURED_ERRORS}'."
                        )
                    assert 0, msg
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e73635eeba9ba43cb3372f395b747ae214ce73b729fb0adba0a55237a1cb063':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for jazmv__wwepj in self._failures.values():
        for pmpb__mjdf in jazmv__wwepj:
            if isinstance(pmpb__mjdf.error, ForceLiteralArg):
                raise pmpb__mjdf.error
            if isinstance(pmpb__mjdf.error, bodo.utils.typing.BodoError):
                raise pmpb__mjdf.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    lgj__pgliw = False
    klgm__zvfsa = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        ihay__wtqe = set()
        leggd__kbgse = lives & alias_set
        for pxv__lvr in leggd__kbgse:
            ihay__wtqe |= alias_map[pxv__lvr]
        lives_n_aliases = lives | ihay__wtqe | arg_aliases
        if type(stmt) in remove_dead_extensions:
            xpq__rdgiz = remove_dead_extensions[type(stmt)]
            stmt = xpq__rdgiz(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                lgj__pgliw = True
                continue
        if isinstance(stmt, ir.Assign):
            ybdb__btgfz = stmt.target
            siqay__wmf = stmt.value
            if ybdb__btgfz.name not in lives:
                if has_no_side_effect(siqay__wmf, lives_n_aliases, call_table):
                    lgj__pgliw = True
                    continue
                if isinstance(siqay__wmf, ir.Expr
                    ) and siqay__wmf.op == 'call' and call_table[siqay__wmf
                    .func.name] == ['astype']:
                    gag__vtt = guard(get_definition, func_ir, siqay__wmf.func)
                    if (gag__vtt is not None and gag__vtt.op == 'getattr' and
                        isinstance(typemap[gag__vtt.value.name], types.
                        Array) and gag__vtt.attr == 'astype'):
                        lgj__pgliw = True
                        continue
            if saved_array_analysis and ybdb__btgfz.name in lives and is_expr(
                siqay__wmf, 'getattr'
                ) and siqay__wmf.attr == 'shape' and is_array_typ(typemap[
                siqay__wmf.value.name]) and siqay__wmf.value.name not in lives:
                lea__lbn = {pxv__lvr: jap__cuf for jap__cuf, pxv__lvr in
                    func_ir.blocks.items()}
                if block in lea__lbn:
                    label = lea__lbn[block]
                    vprh__pep = saved_array_analysis.get_equiv_set(label)
                    ulykc__kyvtl = vprh__pep.get_equiv_set(siqay__wmf.value)
                    if ulykc__kyvtl is not None:
                        for pxv__lvr in ulykc__kyvtl:
                            if pxv__lvr.endswith('#0'):
                                pxv__lvr = pxv__lvr[:-2]
                            if pxv__lvr in typemap and is_array_typ(typemap
                                [pxv__lvr]) and pxv__lvr in lives:
                                siqay__wmf.value = ir.Var(siqay__wmf.value.
                                    scope, pxv__lvr, siqay__wmf.value.loc)
                                lgj__pgliw = True
                                break
            if isinstance(siqay__wmf, ir.Var
                ) and ybdb__btgfz.name == siqay__wmf.name:
                lgj__pgliw = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                lgj__pgliw = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            hoa__ghaj = analysis.ir_extension_usedefs[type(stmt)]
            jkmuq__kpp, paxl__fqlk = hoa__ghaj(stmt)
            lives -= paxl__fqlk
            lives |= jkmuq__kpp
        else:
            lives |= {pxv__lvr.name for pxv__lvr in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                wlqw__agvm = set()
                if isinstance(siqay__wmf, ir.Expr):
                    wlqw__agvm = {pxv__lvr.name for pxv__lvr in siqay__wmf.
                        list_vars()}
                if ybdb__btgfz.name not in wlqw__agvm:
                    lives.remove(ybdb__btgfz.name)
        klgm__zvfsa.append(stmt)
    klgm__zvfsa.reverse()
    block.body = klgm__zvfsa
    return lgj__pgliw


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            itjd__mug, = args
            if isinstance(itjd__mug, types.IterableType):
                dtype = itjd__mug.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), itjd__mug)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    mwzr__rxwe = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (mwzr__rxwe, self.dtype)
    super(types.Set, self).__init__(name=name)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    if isinstance(value, tuple):
        try:
            return types.Tuple([literal(x) for x in value])
        except LiteralTypingError as zaq__xvn:
            return
    try:
        return literal(value)
    except LiteralTypingError as zaq__xvn:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        hqk__ogr = py_func.__qualname__
    except AttributeError as zaq__xvn:
        hqk__ogr = py_func.__name__
    phhfd__cvn = inspect.getfile(py_func)
    for cls in self._locator_classes:
        nlyk__uzyuy = cls.from_function(py_func, phhfd__cvn)
        if nlyk__uzyuy is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (hqk__ogr, phhfd__cvn))
    self._locator = nlyk__uzyuy
    apd__snjlp = inspect.getfile(py_func)
    dkypd__qbfa = os.path.splitext(os.path.basename(apd__snjlp))[0]
    if phhfd__cvn.startswith('<ipython-'):
        nri__onuz = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', dkypd__qbfa, count=1)
        if nri__onuz == dkypd__qbfa:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        dkypd__qbfa = nri__onuz
    eozc__kujto = '%s.%s' % (dkypd__qbfa, hqk__ogr)
    zci__bvrei = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(eozc__kujto, zci__bvrei
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    doarc__zixhp = list(filter(lambda a: self._istuple(a.name), args))
    if len(doarc__zixhp) == 2 and fn.__name__ == 'add':
        tpump__wob = self.typemap[doarc__zixhp[0].name]
        ujwpf__maf = self.typemap[doarc__zixhp[1].name]
        if tpump__wob.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                doarc__zixhp[1]))
        if ujwpf__maf.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                doarc__zixhp[0]))
        try:
            cxer__kiip = [equiv_set.get_shape(x) for x in doarc__zixhp]
            if None in cxer__kiip:
                return None
            vjeg__eyv = sum(cxer__kiip, ())
            return ArrayAnalysis.AnalyzeResult(shape=vjeg__eyv)
        except GuardException as zaq__xvn:
            return None
    ayvrk__vms = list(filter(lambda a: self._isarray(a.name), args))
    require(len(ayvrk__vms) > 0)
    ukrr__qvvdm = [x.name for x in ayvrk__vms]
    tquh__prfa = [self.typemap[x.name].ndim for x in ayvrk__vms]
    wit__ycqj = max(tquh__prfa)
    require(wit__ycqj > 0)
    cxer__kiip = [equiv_set.get_shape(x) for x in ayvrk__vms]
    if any(a is None for a in cxer__kiip):
        return ArrayAnalysis.AnalyzeResult(shape=ayvrk__vms[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, ayvrk__vms))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, cxer__kiip,
        ukrr__qvvdm)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def slice_size(self, index, dsize, equiv_set, scope, stmts):
    return None, None


numba.parfors.array_analysis.ArrayAnalysis.slice_size = slice_size


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    kie__klvpj = code_obj.code
    vwyon__jxxoa = len(kie__klvpj.co_freevars)
    yulso__nnk = kie__klvpj.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        dcd__ojwo, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        yulso__nnk = [pxv__lvr.name for pxv__lvr in dcd__ojwo]
    dpywx__fcfn = caller_ir.func_id.func.__globals__
    try:
        dpywx__fcfn = getattr(code_obj, 'globals', dpywx__fcfn)
    except KeyError as zaq__xvn:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    pjsg__oxwai = []
    for x in yulso__nnk:
        try:
            nxf__dyw = caller_ir.get_definition(x)
        except KeyError as zaq__xvn:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(nxf__dyw, (ir.Const, ir.Global, ir.FreeVar)):
            val = nxf__dyw.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                srqe__pkxbr = ir_utils.mk_unique_var('nested_func').replace('.'
                    , '_')
                dpywx__fcfn[srqe__pkxbr] = bodo.jit(distributed=False)(val)
                dpywx__fcfn[srqe__pkxbr].is_nested_func = True
                val = srqe__pkxbr
            if isinstance(val, CPUDispatcher):
                srqe__pkxbr = ir_utils.mk_unique_var('nested_func').replace('.'
                    , '_')
                dpywx__fcfn[srqe__pkxbr] = val
                val = srqe__pkxbr
            pjsg__oxwai.append(val)
        elif isinstance(nxf__dyw, ir.Expr) and nxf__dyw.op == 'make_function':
            krb__ovn = convert_code_obj_to_function(nxf__dyw, caller_ir)
            srqe__pkxbr = ir_utils.mk_unique_var('nested_func').replace('.',
                '_')
            dpywx__fcfn[srqe__pkxbr] = bodo.jit(distributed=False)(krb__ovn)
            dpywx__fcfn[srqe__pkxbr].is_nested_func = True
            pjsg__oxwai.append(srqe__pkxbr)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    ojc__bubxz = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        pjsg__oxwai)])
    htn__wdi = ','.join([('c_%d' % i) for i in range(vwyon__jxxoa)])
    vcuy__kvda = list(kie__klvpj.co_varnames)
    xeqyy__pxpn = 0
    yzvjo__aub = kie__klvpj.co_argcount
    webty__lnf = caller_ir.get_definition(code_obj.defaults)
    if webty__lnf is not None:
        if isinstance(webty__lnf, tuple):
            d = [caller_ir.get_definition(x).value for x in webty__lnf]
            zbuh__dmelu = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in webty__lnf.items]
            zbuh__dmelu = tuple(d)
        xeqyy__pxpn = len(zbuh__dmelu)
    yxag__iameb = yzvjo__aub - xeqyy__pxpn
    ozidn__zjbtu = ','.join([('%s' % vcuy__kvda[i]) for i in range(
        yxag__iameb)])
    if xeqyy__pxpn:
        sxs__sany = [('%s = %s' % (vcuy__kvda[i + yxag__iameb], zbuh__dmelu
            [i])) for i in range(xeqyy__pxpn)]
        ozidn__zjbtu += ', '
        ozidn__zjbtu += ', '.join(sxs__sany)
    return _create_function_from_code_obj(kie__klvpj, ojc__bubxz,
        ozidn__zjbtu, htn__wdi, dpywx__fcfn)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b840769812418d589460e924a15477e83e7919aac8a3dcb0188ff447344aa8ac':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for jwr__rey, (xyug__uxh, kqxxd__zhc) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % kqxxd__zhc)
            rhk__ybmt = _pass_registry.get(xyug__uxh).pass_inst
            if isinstance(rhk__ybmt, CompilerPass):
                self._runPass(jwr__rey, rhk__ybmt, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, kqxxd__zhc)
                erh__pbbjm = self._patch_error(msg, e)
                raise erh__pbbjm
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '43505782e15e690fd2d7e53ea716543bec37aa0633502956864edf649e790cdb':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a57ef28c4168fdd436a5513bba4351ebc6d9fba76c5819f44046431a79b9030f':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    wjixw__fwb = None
    paxl__fqlk = {}

    def lookup(var, already_seen, varonly=True):
        val = paxl__fqlk.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    zat__vuvr = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        ybdb__btgfz = stmt.target
        siqay__wmf = stmt.value
        paxl__fqlk[ybdb__btgfz.name] = siqay__wmf
        if isinstance(siqay__wmf, ir.Var) and siqay__wmf.name in paxl__fqlk:
            siqay__wmf = lookup(siqay__wmf, set())
        if isinstance(siqay__wmf, ir.Expr):
            cbjh__oglju = set(lookup(pxv__lvr, set(), True).name for
                pxv__lvr in siqay__wmf.list_vars())
            if name in cbjh__oglju:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(siqay__wmf)]
                uizkm__bmt = [x for x, zaze__kjn in args if zaze__kjn.name !=
                    name]
                args = [(x, zaze__kjn) for x, zaze__kjn in args if x !=
                    zaze__kjn.name]
                pxdjm__nrx = dict(args)
                if len(uizkm__bmt) == 1:
                    pxdjm__nrx[uizkm__bmt[0]] = ir.Var(ybdb__btgfz.scope, 
                        name + '#init', ybdb__btgfz.loc)
                replace_vars_inner(siqay__wmf, pxdjm__nrx)
                wjixw__fwb = nodes[i:]
                break
    return wjixw__fwb


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        mmd__vwd = expand_aliases({pxv__lvr.name for pxv__lvr in stmt.
            list_vars()}, alias_map, arg_aliases)
        zrbi__fok = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        xwq__skoqb = expand_aliases({pxv__lvr.name for pxv__lvr in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        poazd__ihvvm = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(zrbi__fok & xwq__skoqb | poazd__ihvvm & mmd__vwd) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    sfc__dgx = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            sfc__dgx.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                sfc__dgx.update(get_parfor_writes(stmt, func_ir))
    return sfc__dgx


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    sfc__dgx = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        sfc__dgx.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        sfc__dgx = {pxv__lvr.name for pxv__lvr in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        sfc__dgx = {pxv__lvr.name for pxv__lvr in stmt.get_live_out_vars()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            sfc__dgx.update({pxv__lvr.name for pxv__lvr in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        rndxl__obe = guard(find_callname, func_ir, stmt.value)
        if rndxl__obe in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'copy_array_element', 'bodo.libs.array_kernels'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext'), (
            'tuple_list_to_array', 'bodo.utils.utils')):
            sfc__dgx.add(stmt.value.args[0].name)
        if rndxl__obe == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            sfc__dgx.add(stmt.value.args[1].name)
    return sfc__dgx


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        xpq__rdgiz = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        byp__cjcsf = xpq__rdgiz.format(self, msg)
        self.args = byp__cjcsf,
    else:
        xpq__rdgiz = _termcolor.errmsg('{0}')
        byp__cjcsf = xpq__rdgiz.format(self)
        self.args = byp__cjcsf,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for idezv__vjgeo in options['distributed']:
            dist_spec[idezv__vjgeo] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for idezv__vjgeo in options['distributed_block']:
            dist_spec[idezv__vjgeo] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    gim__ycnxa = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, ash__ogw in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(ash__ogw)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    kphcr__rojeb = {}
    for cwpk__jebwc in reversed(inspect.getmro(cls)):
        kphcr__rojeb.update(cwpk__jebwc.__dict__)
    fvb__kuikc, kgrxw__tej, ciev__wndf, zie__wdxal = {}, {}, {}, {}
    for jap__cuf, pxv__lvr in kphcr__rojeb.items():
        if isinstance(pxv__lvr, pytypes.FunctionType):
            fvb__kuikc[jap__cuf] = pxv__lvr
        elif isinstance(pxv__lvr, property):
            kgrxw__tej[jap__cuf] = pxv__lvr
        elif isinstance(pxv__lvr, staticmethod):
            ciev__wndf[jap__cuf] = pxv__lvr
        else:
            zie__wdxal[jap__cuf] = pxv__lvr
    phpyz__lwiuf = (set(fvb__kuikc) | set(kgrxw__tej) | set(ciev__wndf)) & set(
        spec)
    if phpyz__lwiuf:
        raise NameError('name shadowing: {0}'.format(', '.join(phpyz__lwiuf)))
    sbb__mocqq = zie__wdxal.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(zie__wdxal)
    if zie__wdxal:
        msg = 'class members are not yet supported: {0}'
        iewte__arci = ', '.join(zie__wdxal.keys())
        raise TypeError(msg.format(iewte__arci))
    for jap__cuf, pxv__lvr in kgrxw__tej.items():
        if pxv__lvr.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(jap__cuf))
    jit_methods = {jap__cuf: bodo.jit(returns_maybe_distributed=gim__ycnxa)
        (pxv__lvr) for jap__cuf, pxv__lvr in fvb__kuikc.items()}
    jit_props = {}
    for jap__cuf, pxv__lvr in kgrxw__tej.items():
        wpaus__qfa = {}
        if pxv__lvr.fget:
            wpaus__qfa['get'] = bodo.jit(pxv__lvr.fget)
        if pxv__lvr.fset:
            wpaus__qfa['set'] = bodo.jit(pxv__lvr.fset)
        jit_props[jap__cuf] = wpaus__qfa
    jit_static_methods = {jap__cuf: bodo.jit(pxv__lvr.__func__) for 
        jap__cuf, pxv__lvr in ciev__wndf.items()}
    acc__nqyul = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    wjy__ljyzb = dict(class_type=acc__nqyul, __doc__=sbb__mocqq)
    wjy__ljyzb.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), wjy__ljyzb)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, acc__nqyul)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(acc__nqyul, typingctx, targetctx).register()
    as_numba_type.register(cls, acc__nqyul.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    ryn__tpmta = ','.join('{0}:{1}'.format(jap__cuf, pxv__lvr) for jap__cuf,
        pxv__lvr in struct.items())
    okibd__yao = ','.join('{0}:{1}'.format(jap__cuf, pxv__lvr) for jap__cuf,
        pxv__lvr in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), ryn__tpmta, okibd__yao)
    super(types.misc.ClassType, self).__init__(name)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    uiv__omlfj = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if uiv__omlfj is None:
        return
    acqo__jqt, wpuij__nvrzu = uiv__omlfj
    for a in itertools.chain(acqo__jqt, wpuij__nvrzu.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, acqo__jqt, wpuij__nvrzu)
    except ForceLiteralArg as e:
        fithn__yfet = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(fithn__yfet, self.kws)
        rcza__irdcc = set()
        lfxd__bkmrt = set()
        yshlu__mxyxt = {}
        for jwr__rey in e.requested_args:
            eleml__trnw = typeinfer.func_ir.get_definition(folded[jwr__rey])
            if isinstance(eleml__trnw, ir.Arg):
                rcza__irdcc.add(eleml__trnw.index)
                if eleml__trnw.index in e.file_infos:
                    yshlu__mxyxt[eleml__trnw.index] = e.file_infos[eleml__trnw
                        .index]
            else:
                lfxd__bkmrt.add(jwr__rey)
        if lfxd__bkmrt:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif rcza__irdcc:
            raise ForceLiteralArg(rcza__irdcc, loc=self.loc, file_infos=
                yshlu__mxyxt)
    if sig is None:
        ryojk__evm = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in acqo__jqt]
        args += [('%s=%s' % (jap__cuf, pxv__lvr)) for jap__cuf, pxv__lvr in
            sorted(wpuij__nvrzu.items())]
        hsqt__etggu = ryojk__evm.format(fnty, ', '.join(map(str, args)))
        fpv__zvqh = context.explain_function_type(fnty)
        msg = '\n'.join([hsqt__etggu, fpv__zvqh])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        mkz__kqsdd = context.unify_pairs(sig.recvr, fnty.this)
        if mkz__kqsdd is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if mkz__kqsdd is not None and mkz__kqsdd.is_precise():
            cucor__loyfu = fnty.copy(this=mkz__kqsdd)
            typeinfer.propagate_refined_type(self.func, cucor__loyfu)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            pwkoh__uqnqe = target.getone()
            if context.unify_pairs(pwkoh__uqnqe, sig.return_type
                ) == pwkoh__uqnqe:
                sig = sig.replace(return_type=pwkoh__uqnqe)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        qcqnx__jsm = '*other* must be a {} but got a {} instead'
        raise TypeError(qcqnx__jsm.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args,
        file_infos={**self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    qgj__ykvee = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for jap__cuf, pxv__lvr in kwargs.items():
        avgx__osn = None
        try:
            mzkl__dvghs = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[mzkl__dvghs.name] = [pxv__lvr]
            avgx__osn = get_const_value_inner(func_ir, mzkl__dvghs)
            func_ir._definitions.pop(mzkl__dvghs.name)
            if isinstance(avgx__osn, str):
                avgx__osn = sigutils._parse_signature_string(avgx__osn)
            if isinstance(avgx__osn, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {jap__cuf} is annotated as type class {avgx__osn}."""
                    )
            assert isinstance(avgx__osn, types.Type)
            if isinstance(avgx__osn, (types.List, types.Set)):
                avgx__osn = avgx__osn.copy(reflected=False)
            qgj__ykvee[jap__cuf] = avgx__osn
        except BodoError as zaq__xvn:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(avgx__osn, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(pxv__lvr, ir.Global):
                    msg = f'Global {pxv__lvr.name!r} is not defined.'
                if isinstance(pxv__lvr, ir.FreeVar):
                    msg = f'Freevar {pxv__lvr.name!r} is not defined.'
            if isinstance(pxv__lvr, ir.Expr) and pxv__lvr.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=jap__cuf, msg=msg, loc=loc)
    for name, typ in qgj__ykvee.items():
        self._legalize_arg_type(name, typ, loc)
    return qgj__ykvee


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    flags = inst.arg
    if flags & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if flags & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    rssp__vvdhp = inst.arg
    assert rssp__vvdhp > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(rssp__vvdhp)]))
    tmps = [state.make_temp() for _ in range(rssp__vvdhp - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    xfkvs__vkn = ir.Global('format', format, loc=self.loc)
    self.store(value=xfkvs__vkn, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    tbg__cwbny = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=tbg__cwbny, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    rssp__vvdhp = inst.arg
    assert rssp__vvdhp > 0, 'invalid BUILD_STRING count'
    xqbq__fgw = self.get(strings[0])
    for other, kew__aowf in zip(strings[1:], tmps):
        other = self.get(other)
        dxzy__bjlyj = ir.Expr.binop(operator.add, lhs=xqbq__fgw, rhs=other,
            loc=self.loc)
        self.store(dxzy__bjlyj, kew__aowf)
        xqbq__fgw = self.get(kew__aowf)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    tej__ybd = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, tej__ybd])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    raonr__gge = mk_unique_var(f'{var_name}')
    fdsay__iuib = raonr__gge.replace('<', '_').replace('>', '_')
    fdsay__iuib = fdsay__iuib.replace('.', '_').replace('$', '_v')
    return fdsay__iuib


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.
        _created_inlined_var_name)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0d91aac55cd0243e58809afe9d252562f9ae2899cde1112cc01a46804e01821e':
        warnings.warn(
            'numba.core.inline_closurecall._created_inlined_var_name has changed'
            )
numba.core.inline_closurecall._created_inlined_var_name = (
    _created_inlined_var_name)


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    import bodo
    ty = classty.instance_type
    if isinstance(ty, types.NPDatetime):

        def typer(val1, val2):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(val1,
                'numpy.datetime64')
            if (val1 == bodo.hiframes.pd_timestamp_ext.
                pd_timestamp_tz_naive_type):
                if not is_overload_constant_str(val2):
                    raise_bodo_error(
                        "datetime64(): 'units' must be a 'str' specifying 'ns'"
                        )
                lneop__noxim = get_overload_const_str(val2)
                if lneop__noxim != 'ns':
                    raise BodoError("datetime64(): 'units' must be 'ns'")
                return types.NPDatetime('ns')
    else:

        def typer(val):
            if isinstance(val, (types.BaseTuple, types.Sequence)):
                fnty = self.context.resolve_value_type(np.array)
                sig = fnty.get_call_type(self.context, (val, types.DType(ty
                    )), {})
                return sig.return_type
            elif isinstance(val, (types.Number, types.Boolean, types.
                IntEnumMember)):
                return ty
            elif val == types.unicode_type:
                return ty
            elif isinstance(val, (types.NPDatetime, types.NPTimedelta)):
                if ty.bitwidth == 64:
                    return ty
                else:
                    msg = (
                        f'Cannot cast {val} to {ty} as {ty} is not 64 bits wide.'
                        )
                    raise errors.TypingError(msg)
            elif isinstance(val, types.Array
                ) and val.ndim == 0 and val.dtype == ty:
                return ty
            else:
                msg = f'Casting {val} to {ty} directly is unsupported.'
                if isinstance(val, types.Array):
                    msg += f" Try doing '<array>.astype(np.{ty})' instead"
                raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdaf0c7d0820130481bb2bd922985257b9281b670f0bafffe10e51cabf0d5081':
        warnings.warn(
            'numba.core.typing.builtins.NumberClassAttribute.resolve___call__ has changed'
            )
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        wrzy__wyrzu = states['defmap']
        if len(wrzy__wyrzu) == 0:
            xwfuh__iztxf = assign.target
            numba.core.ssa._logger.debug('first assign: %s', xwfuh__iztxf)
            if xwfuh__iztxf.name not in scope.localvars:
                xwfuh__iztxf = scope.define(assign.target.name, loc=assign.loc)
        else:
            xwfuh__iztxf = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=xwfuh__iztxf, value=assign.value, loc=
            assign.loc)
        wrzy__wyrzu[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    fxpn__emhoq = []
    for jap__cuf, pxv__lvr in typing.npydecl.registry.globals:
        if jap__cuf == func:
            fxpn__emhoq.append(pxv__lvr)
    for jap__cuf, pxv__lvr in typing.templates.builtin_registry.globals:
        if jap__cuf == func:
            fxpn__emhoq.append(pxv__lvr)
    if len(fxpn__emhoq) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return fxpn__emhoq


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    umyt__fukp = {}
    axu__atf = find_topo_order(blocks)
    fbm__htkhk = {}
    for label in axu__atf:
        block = blocks[label]
        klgm__zvfsa = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                ybdb__btgfz = stmt.target.name
                siqay__wmf = stmt.value
                if (siqay__wmf.op == 'getattr' and siqay__wmf.attr in
                    arr_math and isinstance(typemap[siqay__wmf.value.name],
                    types.npytypes.Array)):
                    siqay__wmf = stmt.value
                    pji__lwu = siqay__wmf.value
                    umyt__fukp[ybdb__btgfz] = pji__lwu
                    scope = pji__lwu.scope
                    loc = pji__lwu.loc
                    uiqzl__imbml = ir.Var(scope, mk_unique_var('$np_g_var'),
                        loc)
                    typemap[uiqzl__imbml.name] = types.misc.Module(numpy)
                    wvr__zmoaa = ir.Global('np', numpy, loc)
                    ipen__wsajt = ir.Assign(wvr__zmoaa, uiqzl__imbml, loc)
                    siqay__wmf.value = uiqzl__imbml
                    klgm__zvfsa.append(ipen__wsajt)
                    func_ir._definitions[uiqzl__imbml.name] = [wvr__zmoaa]
                    func = getattr(numpy, siqay__wmf.attr)
                    eacox__fre = get_np_ufunc_typ_lst(func)
                    fbm__htkhk[ybdb__btgfz] = eacox__fre
                if (siqay__wmf.op == 'call' and siqay__wmf.func.name in
                    umyt__fukp):
                    pji__lwu = umyt__fukp[siqay__wmf.func.name]
                    jbn__vbg = calltypes.pop(siqay__wmf)
                    snert__evxvd = jbn__vbg.args[:len(siqay__wmf.args)]
                    smxs__uled = {name: typemap[pxv__lvr.name] for name,
                        pxv__lvr in siqay__wmf.kws}
                    ftqnv__svnlx = fbm__htkhk[siqay__wmf.func.name]
                    gnrt__shqiy = None
                    for gmdpu__rkyyq in ftqnv__svnlx:
                        try:
                            gnrt__shqiy = gmdpu__rkyyq.get_call_type(typingctx,
                                [typemap[pji__lwu.name]] + list(
                                snert__evxvd), smxs__uled)
                            typemap.pop(siqay__wmf.func.name)
                            typemap[siqay__wmf.func.name] = gmdpu__rkyyq
                            calltypes[siqay__wmf] = gnrt__shqiy
                            break
                        except Exception as zaq__xvn:
                            pass
                    if gnrt__shqiy is None:
                        raise TypeError(
                            f'No valid template found for {siqay__wmf.func.name}'
                            )
                    siqay__wmf.args = [pji__lwu] + siqay__wmf.args
            klgm__zvfsa.append(stmt)
        block.body = klgm__zvfsa


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    soacy__qlu = ufunc.nin
    gbkyu__cyl = ufunc.nout
    yxag__iameb = ufunc.nargs
    assert yxag__iameb == soacy__qlu + gbkyu__cyl
    if len(args) < soacy__qlu:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), soacy__qlu)
            )
    if len(args) > yxag__iameb:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            yxag__iameb))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    kxu__kqp = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    qig__ltay = max(kxu__kqp)
    kibg__qsqsm = args[soacy__qlu:]
    if not all(d == qig__ltay for d in kxu__kqp[soacy__qlu:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(lgnr__uyrjf, types.ArrayCompatible) and not
        isinstance(lgnr__uyrjf, types.Bytes) for lgnr__uyrjf in kibg__qsqsm):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(lgnr__uyrjf.mutable for lgnr__uyrjf in kibg__qsqsm):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    vbjq__clo = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    qthl__dsdy = None
    if qig__ltay > 0 and len(kibg__qsqsm) < ufunc.nout:
        qthl__dsdy = 'C'
        sqv__cuck = [(x.layout if isinstance(x, types.ArrayCompatible) and 
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in sqv__cuck and 'F' in sqv__cuck:
            qthl__dsdy = 'F'
    return vbjq__clo, kibg__qsqsm, qig__ltay, qthl__dsdy


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        jiw__usb = 'Dict.key_type cannot be of type {}'
        raise TypingError(jiw__usb.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        jiw__usb = 'Dict.value_type cannot be of type {}'
        raise TypingError(jiw__usb.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    name = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty, valty,
        initial_value)
    super(DictType, self).__init__(name)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for i, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(i))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def _overload_template_get_impl(self, args, kws):
    smwqq__scwjx = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[smwqq__scwjx]
        return impl, args
    except KeyError as zaq__xvn:
        pass
    impl, args = self._build_impl(smwqq__scwjx, args, kws)
    return impl, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4e27d07b214ca16d6e8ed88f70d886b6b095e160d8f77f8df369dd4ed2eb3fae':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate._get_impl has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def trim_empty_parfor_branches(parfor):
    jfoh__rljdl = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            dwj__idmpg = block.body[-1]
            if isinstance(dwj__idmpg, ir.Branch):
                if len(blocks[dwj__idmpg.truebr].body) == 1 and len(blocks[
                    dwj__idmpg.falsebr].body) == 1:
                    shxxi__slpuc = blocks[dwj__idmpg.truebr].body[0]
                    aacd__cvm = blocks[dwj__idmpg.falsebr].body[0]
                    if isinstance(shxxi__slpuc, ir.Jump) and isinstance(
                        aacd__cvm, ir.Jump
                        ) and shxxi__slpuc.target == aacd__cvm.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(shxxi__slpuc
                            .target, dwj__idmpg.loc)
                        jfoh__rljdl = True
                elif len(blocks[dwj__idmpg.truebr].body) == 1:
                    shxxi__slpuc = blocks[dwj__idmpg.truebr].body[0]
                    if isinstance(shxxi__slpuc, ir.Jump
                        ) and shxxi__slpuc.target == dwj__idmpg.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(shxxi__slpuc
                            .target, dwj__idmpg.loc)
                        jfoh__rljdl = True
                elif len(blocks[dwj__idmpg.falsebr].body) == 1:
                    aacd__cvm = blocks[dwj__idmpg.falsebr].body[0]
                    if isinstance(aacd__cvm, ir.Jump
                        ) and aacd__cvm.target == dwj__idmpg.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(aacd__cvm
                            .target, dwj__idmpg.loc)
                        jfoh__rljdl = True
    return jfoh__rljdl


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        skcs__ojmm = find_topo_order(parfor.loop_body)
    hoi__apgh = skcs__ojmm[0]
    jga__jpsu = {}
    _update_parfor_get_setitems(parfor.loop_body[hoi__apgh].body, parfor.
        index_var, alias_map, jga__jpsu, lives_n_aliases)
    uikcr__yrc = set(jga__jpsu.keys())
    for ycvu__ohy in skcs__ojmm:
        if ycvu__ohy == hoi__apgh:
            continue
        for stmt in parfor.loop_body[ycvu__ohy].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            vgb__sqj = set(pxv__lvr.name for pxv__lvr in stmt.list_vars())
            eofmc__abhc = vgb__sqj & uikcr__yrc
            for a in eofmc__abhc:
                jga__jpsu.pop(a, None)
    for ycvu__ohy in skcs__ojmm:
        if ycvu__ohy == hoi__apgh:
            continue
        block = parfor.loop_body[ycvu__ohy]
        deo__hym = jga__jpsu.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            deo__hym, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    odci__icoo = max(blocks.keys())
    abq__bpsr, iqh__glxep = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    ywc__vcfa = ir.Jump(abq__bpsr, ir.Loc('parfors_dummy', -1))
    blocks[odci__icoo].body.append(ywc__vcfa)
    fcfvb__gcea = compute_cfg_from_blocks(blocks)
    bszok__bqq = compute_use_defs(blocks)
    jtnx__rpmq = compute_live_map(fcfvb__gcea, blocks, bszok__bqq.usemap,
        bszok__bqq.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        klgm__zvfsa = []
        tqt__lgt = {pxv__lvr.name for pxv__lvr in block.terminator.list_vars()}
        for gtx__jbvix, dhku__rar in fcfvb__gcea.successors(label):
            tqt__lgt |= jtnx__rpmq[gtx__jbvix]
        for stmt in reversed(block.body):
            ihay__wtqe = tqt__lgt & alias_set
            for pxv__lvr in ihay__wtqe:
                tqt__lgt |= alias_map[pxv__lvr]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in tqt__lgt and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                rndxl__obe = guard(find_callname, func_ir, stmt.value)
                if rndxl__obe == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in tqt__lgt and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            tqt__lgt |= {pxv__lvr.name for pxv__lvr in stmt.list_vars()}
            klgm__zvfsa.append(stmt)
        klgm__zvfsa.reverse()
        block.body = klgm__zvfsa
    typemap.pop(iqh__glxep.name)
    blocks[odci__icoo].body.pop()
    jfoh__rljdl = True
    while jfoh__rljdl:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        jfoh__rljdl = trim_empty_parfor_branches(parfor)
    vpu__chw = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        vpu__chw &= len(block.body) == 0
    if vpu__chw:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.parfors.parfor import Parfor
    lykml__fmdx = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                lykml__fmdx += 1
                parfor = stmt
                jxl__ruu = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = jxl__ruu.scope
                loc = ir.Loc('parfors_dummy', -1)
                dzb__imlb = ir.Var(scope, mk_unique_var('$const'), loc)
                jxl__ruu.body.append(ir.Assign(ir.Const(0, loc), dzb__imlb,
                    loc))
                jxl__ruu.body.append(ir.Return(dzb__imlb, loc))
                fcfvb__gcea = compute_cfg_from_blocks(parfor.loop_body)
                for fuxeg__vuxb in fcfvb__gcea.dead_nodes():
                    del parfor.loop_body[fuxeg__vuxb]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                jxl__ruu = parfor.loop_body[max(parfor.loop_body.keys())]
                jxl__ruu.body.pop()
                jxl__ruu.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return lykml__fmdx


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    fcfvb__gcea = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != fcfvb__gcea.entry_point()
    axbyt__ffk = list(filter(find_single_branch, blocks.keys()))
    bszej__wbqo = set()
    for label in axbyt__ffk:
        inst = blocks[label].body[0]
        xwc__mwmoa = fcfvb__gcea.predecessors(label)
        kwcaj__hvoj = True
        for ixyzo__jyflm, wnfdm__hbqpm in xwc__mwmoa:
            block = blocks[ixyzo__jyflm]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                kwcaj__hvoj = False
        if kwcaj__hvoj:
            bszej__wbqo.add(label)
    for label in bszej__wbqo:
        del blocks[label]
    merge_adjacent_blocks(blocks)
    return rename_labels(blocks)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.simplify_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0b3f2add05e5691155f08fc5945956d5cca5e068247d52cff8efb161b76388b7':
        warnings.warn('numba.core.ir_utils.simplify_CFG has changed')
numba.core.ir_utils.simplify_CFG = simplify_CFG


def _lifted_compile(self, sig):
    import numba.core.event as ev
    from numba.core import compiler, sigutils
    from numba.core.compiler_lock import global_compiler_lock
    from numba.core.ir_utils import remove_dels
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        with self._compiling_counter:
            flags = self.flags
            args, return_type = sigutils.normalize_signature(sig)
            sxmg__yzb = self.overloads.get(tuple(args))
            if sxmg__yzb is not None:
                return sxmg__yzb.entry_point
            self._pre_compile(args, return_type, flags)
            oxh__bmvw = self.func_ir
            cpbw__frrq = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=cpbw__frrq):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=oxh__bmvw, args=args,
                    return_type=return_type, flags=flags, locals=self.
                    locals, lifted=(), lifted_from=self.lifted_from,
                    is_lifted_loop=True)
                if cres.typing_error is not None and not flags.enable_pyobject:
                    raise cres.typing_error
                self.add_overload(cres)
            remove_dels(self.func_ir.blocks)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.LiftedCode.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1351ebc5d8812dc8da167b30dad30eafb2ca9bf191b49aaed6241c21e03afff1':
        warnings.warn('numba.core.dispatcher.LiftedCode.compile has changed')
numba.core.dispatcher.LiftedCode.compile = _lifted_compile


def compile_ir(typingctx, targetctx, func_ir, args, return_type, flags,
    locals, lifted=(), lifted_from=None, is_lifted_loop=False, library=None,
    pipeline_class=Compiler):
    if is_lifted_loop:
        leqhb__ildya = copy.deepcopy(flags)
        leqhb__ildya.no_rewrites = True

        def compile_local(the_ir, the_flags):
            uaf__jae = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return uaf__jae.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        srejc__nysi = compile_local(func_ir, leqhb__ildya)
        xafzj__vej = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    xafzj__vej = compile_local(func_ir, flags)
                except Exception as zaq__xvn:
                    pass
        if xafzj__vej is not None:
            cres = xafzj__vej
        else:
            cres = srejc__nysi
        return cres
    else:
        uaf__jae = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return uaf__jae.compile_ir(func_ir=func_ir, lifted=lifted,
            lifted_from=lifted_from)


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.compile_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c48ce5493f4c43326e8cbdd46f3ea038b2b9045352d9d25894244798388e5e5b':
        warnings.warn('numba.core.compiler.compile_ir has changed')
numba.core.compiler.compile_ir = compile_ir


def make_constant_array(self, builder, typ, ary):
    import math
    from llvmlite import ir as lir
    gqg__kcae = self.get_data_type(typ.dtype)
    kxllf__gtwqm = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        kxllf__gtwqm):
        bgz__icm = ary.ctypes.data
        ftr__szudw = self.add_dynamic_addr(builder, bgz__icm, info=str(type
            (bgz__icm)))
        vyq__nde = self.add_dynamic_addr(builder, id(ary), info=str(type(ary)))
        self.global_arrays.append(ary)
    else:
        ukubq__atrk = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            ukubq__atrk = ukubq__atrk.view('int64')
        val = bytearray(ukubq__atrk.data)
        mrgl__dvvx = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        ftr__szudw = cgutils.global_constant(builder, '.const.array.data',
            mrgl__dvvx)
        ftr__szudw.align = self.get_abi_alignment(gqg__kcae)
        vyq__nde = None
    soec__dzt = self.get_value_type(types.intp)
    tcfk__llk = [self.get_constant(types.intp, plh__twk) for plh__twk in
        ary.shape]
    brt__jsq = lir.Constant(lir.ArrayType(soec__dzt, len(tcfk__llk)), tcfk__llk
        )
    ksyl__tzqjr = [self.get_constant(types.intp, plh__twk) for plh__twk in
        ary.strides]
    ypen__nnloa = lir.Constant(lir.ArrayType(soec__dzt, len(ksyl__tzqjr)),
        ksyl__tzqjr)
    bsmf__hypo = self.get_constant(types.intp, ary.dtype.itemsize)
    rcf__leme = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        rcf__leme, bsmf__hypo, ftr__szudw.bitcast(self.get_value_type(types
        .CPointer(typ.dtype))), brt__jsq, ypen__nnloa])


if _check_numba_change:
    lines = inspect.getsource(numba.core.base.BaseContext.make_constant_array)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5721b5360b51f782f79bd794f7bf4d48657911ecdc05c30db22fd55f15dad821':
        warnings.warn(
            'numba.core.base.BaseContext.make_constant_array has changed')
numba.core.base.BaseContext.make_constant_array = make_constant_array


def _define_atomic_inc_dec(module, op, ordering):
    from llvmlite import ir as lir
    from numba.core.runtime.nrtdynmod import _word_type
    pmqfd__bnj = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    wbwc__khc = lir.Function(module, pmqfd__bnj, name='nrt_atomic_{0}'.
        format(op))
    [npxfq__hra] = wbwc__khc.args
    hym__nayo = wbwc__khc.append_basic_block()
    builder = lir.IRBuilder(hym__nayo)
    erco__lbtp = lir.Constant(_word_type, 1)
    if False:
        sclhx__lcqso = builder.atomic_rmw(op, npxfq__hra, erco__lbtp,
            ordering=ordering)
        res = getattr(builder, op)(sclhx__lcqso, erco__lbtp)
        builder.ret(res)
    else:
        sclhx__lcqso = builder.load(npxfq__hra)
        bfiy__tsx = getattr(builder, op)(sclhx__lcqso, erco__lbtp)
        jcvk__ltu = builder.icmp_signed('!=', sclhx__lcqso, lir.Constant(
            sclhx__lcqso.type, -1))
        with cgutils.if_likely(builder, jcvk__ltu):
            builder.store(bfiy__tsx, npxfq__hra)
        builder.ret(bfiy__tsx)
    return wbwc__khc


if _check_numba_change:
    lines = inspect.getsource(numba.core.runtime.nrtdynmod.
        _define_atomic_inc_dec)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9cc02c532b2980b6537b702f5608ea603a1ff93c6d3c785ae2cf48bace273f48':
        warnings.warn(
            'numba.core.runtime.nrtdynmod._define_atomic_inc_dec has changed')
numba.core.runtime.nrtdynmod._define_atomic_inc_dec = _define_atomic_inc_dec


def NativeLowering_run_pass(self, state):
    from llvmlite import binding as llvm
    from numba.core import funcdesc, lowering
    from numba.core.typed_passes import fallback_context
    if state.library is None:
        naa__owg = state.targetctx.codegen()
        state.library = naa__owg.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    vfr__umgio = state.func_ir
    typemap = state.typemap
    sjb__rhgbb = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    kxy__kcx = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            vfr__umgio, typemap, sjb__rhgbb, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            sneed__iehz = lowering.Lower(targetctx, library, fndesc,
                vfr__umgio, metadata=metadata)
            sneed__iehz.lower()
            if not flags.no_cpython_wrapper:
                sneed__iehz.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(sjb__rhgbb, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        sneed__iehz.create_cfunc_wrapper()
            env = sneed__iehz.env
            yuk__zwk = sneed__iehz.call_helper
            del sneed__iehz
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, yuk__zwk, cfunc=None, env=env)
        else:
            xxu__bkn = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(xxu__bkn, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, yuk__zwk, cfunc=xxu__bkn,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        vjo__djc = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = vjo__djc - kxy__kcx
        metadata['llvm_pass_timings'] = library.recorded_timings
    return True


if _check_numba_change:
    lines = inspect.getsource(numba.core.typed_passes.NativeLowering.run_pass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a777ce6ce1bb2b1cbaa3ac6c2c0e2adab69a9c23888dff5f1cbb67bfb176b5de':
        warnings.warn(
            'numba.core.typed_passes.NativeLowering.run_pass has changed')
numba.core.typed_passes.NativeLowering.run_pass = NativeLowering_run_pass


def _python_list_to_native(typ, obj, c, size, listptr, errorptr):
    from llvmlite import ir as lir
    from numba.core.boxing import _NumbaTypeHelper
    from numba.cpython import listobj

    def check_element_type(nth, itemobj, expected_typobj):
        vxvfw__nlxt = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, vxvfw__nlxt),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            oxkx__diba.do_break()
        umobj__oduft = c.builder.icmp_signed('!=', vxvfw__nlxt, expected_typobj
            )
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(umobj__oduft, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, vxvfw__nlxt)
                c.pyapi.decref(vxvfw__nlxt)
                oxkx__diba.do_break()
        c.pyapi.decref(vxvfw__nlxt)
    rlln__kgfo, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(rlln__kgfo, likely=True) as (hej__wdkg, rtwq__sqfa):
        with hej__wdkg:
            list.size = size
            vnsco__xst = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                vnsco__xst), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        vnsco__xst))
                    with cgutils.for_range(c.builder, size) as oxkx__diba:
                        itemobj = c.pyapi.list_getitem(obj, oxkx__diba.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        phflq__oqfo = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(phflq__oqfo.is_error, likely
                            =False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            oxkx__diba.do_break()
                        list.setitem(oxkx__diba.index, phflq__oqfo.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with rtwq__sqfa:
            c.builder.store(cgutils.true_bit, errorptr)
    with c.builder.if_then(c.builder.load(errorptr)):
        c.context.nrt.decref(c.builder, typ, list.value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.boxing._python_list_to_native)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f8e546df8b07adfe74a16b6aafb1d4fddbae7d3516d7944b3247cc7c9b7ea88a':
        warnings.warn('numba.core.boxing._python_list_to_native has changed')
numba.core.boxing._python_list_to_native = _python_list_to_native


def make_string_from_constant(context, builder, typ, literal_string):
    from llvmlite import ir as lir
    from numba.cpython.hashing import _Py_hash_t
    from numba.cpython.unicode import compile_time_get_string_data
    fmlcc__qyy, eswje__jks, qma__ssvyp, ycs__nhptu, wmie__udsi = (
        compile_time_get_string_data(literal_string))
    rvj__qdy = builder.module
    gv = context.insert_const_bytes(rvj__qdy, fmlcc__qyy)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        eswje__jks), context.get_constant(types.int32, qma__ssvyp), context
        .get_constant(types.uint32, ycs__nhptu), context.get_constant(
        _Py_hash_t, -1), context.get_constant_null(types.MemInfoPointer(
        types.voidptr)), context.get_constant_null(types.pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    flt__pccon = None
    if isinstance(shape, types.Integer):
        flt__pccon = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(plh__twk, (types.Integer, types.IntEnumMember)) for
            plh__twk in shape):
            flt__pccon = len(shape)
    return flt__pccon


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.parse_shape)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e62e3ff09d36df5ac9374055947d6a8be27160ce32960d3ef6cb67f89bd16429':
        warnings.warn('numba.core.typing.npydecl.parse_shape has changed')
numba.core.typing.npydecl.parse_shape = parse_shape


def _get_names(self, obj):
    if isinstance(obj, ir.Var) or isinstance(obj, str):
        name = obj if isinstance(obj, str) else obj.name
        if name not in self.typemap:
            return name,
        typ = self.typemap[name]
        if isinstance(typ, (types.BaseTuple, types.ArrayCompatible)):
            flt__pccon = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if flt__pccon == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(flt__pccon)
                    )
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            ukrr__qvvdm = self._get_names(x)
            if len(ukrr__qvvdm) != 0:
                return ukrr__qvvdm[0]
            return ukrr__qvvdm
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    ukrr__qvvdm = self._get_names(obj)
    if len(ukrr__qvvdm) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(ukrr__qvvdm[0])


def get_equiv_set(self, obj):
    ukrr__qvvdm = self._get_names(obj)
    if len(ukrr__qvvdm) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(ukrr__qvvdm[0])


if _check_numba_change:
    for name, orig, new, hash in ((
        'numba.parfors.array_analysis.ShapeEquivSet._get_names', numba.
        parfors.array_analysis.ShapeEquivSet._get_names, _get_names,
        '8c9bf136109028d5445fd0a82387b6abeb70c23b20b41e2b50c34ba5359516ee'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const',
        numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const,
        get_equiv_const,
        'bef410ca31a9e29df9ee74a4a27d339cc332564e4a237828b8a4decf625ce44e'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set', numba.
        parfors.array_analysis.ShapeEquivSet.get_equiv_set, get_equiv_set,
        'ec936d340c488461122eb74f28a28b88227cb1f1bca2b9ba3c19258cfe1eb40a')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
numba.parfors.array_analysis.ShapeEquivSet._get_names = _get_names
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const = get_equiv_const
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set = get_equiv_set


def raise_on_unsupported_feature(func_ir, typemap):
    import numpy
    itc__ppxk = []
    for vog__anlu in func_ir.arg_names:
        if vog__anlu in typemap and isinstance(typemap[vog__anlu], types.
            containers.UniTuple) and typemap[vog__anlu].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(vog__anlu))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for ndi__tklu in func_ir.blocks.values():
        for stmt in ndi__tklu.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    emc__tlkkd = getattr(val, 'code', None)
                    if emc__tlkkd is not None:
                        if getattr(val, 'closure', None) is not None:
                            upqy__bbud = '<creating a function from a closure>'
                            dxzy__bjlyj = ''
                        else:
                            upqy__bbud = emc__tlkkd.co_name
                            dxzy__bjlyj = '(%s) ' % upqy__bbud
                    else:
                        upqy__bbud = '<could not ascertain use case>'
                        dxzy__bjlyj = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (upqy__bbud, dxzy__bjlyj))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                kcch__tnbdo = False
                if isinstance(val, pytypes.FunctionType):
                    kcch__tnbdo = val in {numba.gdb, numba.gdb_init}
                if not kcch__tnbdo:
                    kcch__tnbdo = getattr(val, '_name', '') == 'gdb_internal'
                if kcch__tnbdo:
                    itc__ppxk.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    wjtym__wirb = func_ir.get_definition(var)
                    gpsij__abhf = guard(find_callname, func_ir, wjtym__wirb)
                    if gpsij__abhf and gpsij__abhf[1] == 'numpy':
                        ty = getattr(numpy, gpsij__abhf[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    tznlz__ywr = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(tznlz__ywr), loc=stmt.loc)
            if isinstance(stmt.value, ir.Global):
                ty = typemap[stmt.target.name]
                msg = (
                    "The use of a %s type, assigned to variable '%s' in globals, is not supported as globals are considered compile-time constants and there is no known way to compile a %s type as a constant."
                    )
                if isinstance(ty, types.ListType):
                    raise TypingError(msg % (ty, stmt.value.name, ty), loc=
                        stmt.loc)
            if isinstance(stmt.value, ir.Yield) and not func_ir.is_generator:
                msg = 'The use of generator expressions is unsupported.'
                raise errors.UnsupportedError(msg, loc=stmt.loc)
    if len(itc__ppxk) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        obuc__pimh = '\n'.join([x.strformat() for x in itc__ppxk])
        raise errors.UnsupportedError(msg % obuc__pimh)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.raise_on_unsupported_feature)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '237a4fe8395a40899279c718bc3754102cd2577463ef2f48daceea78d79b2d5e':
        warnings.warn(
            'numba.core.ir_utils.raise_on_unsupported_feature has changed')
numba.core.ir_utils.raise_on_unsupported_feature = raise_on_unsupported_feature
numba.core.typed_passes.raise_on_unsupported_feature = (
    raise_on_unsupported_feature)


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    jap__cuf, pxv__lvr = next(iter(val.items()))
    dtdf__vysv = typeof_impl(jap__cuf, c)
    kmzhz__hxu = typeof_impl(pxv__lvr, c)
    if dtdf__vysv is None or kmzhz__hxu is None:
        raise ValueError(
            f'Cannot type dict element type {type(jap__cuf)}, {type(pxv__lvr)}'
            )
    return types.DictType(dtdf__vysv, kmzhz__hxu)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    jstb__zkuqw = cgutils.alloca_once_value(c.builder, val)
    vzk__pokip = c.pyapi.object_hasattr_string(val, '_opaque')
    pfrsu__lsf = c.builder.icmp_unsigned('==', vzk__pokip, lir.Constant(
        vzk__pokip.type, 0))
    dmmmu__lfb = typ.key_type
    vae__svoh = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(dmmmu__lfb, vae__svoh)

    def copy_dict(out_dict, in_dict):
        for jap__cuf, pxv__lvr in in_dict.items():
            out_dict[jap__cuf] = pxv__lvr
    with c.builder.if_then(pfrsu__lsf):
        aop__lpmh = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        kngn__efjqp = c.pyapi.call_function_objargs(aop__lpmh, [])
        unj__oxerl = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(unj__oxerl, [kngn__efjqp, val])
        c.builder.store(kngn__efjqp, jstb__zkuqw)
    val = c.builder.load(jstb__zkuqw)
    viw__sdaj = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    udrx__pipr = c.pyapi.object_type(val)
    mgkt__khu = c.builder.icmp_unsigned('==', udrx__pipr, viw__sdaj)
    with c.builder.if_else(mgkt__khu) as (nhw__uztr, swub__jkpns):
        with nhw__uztr:
            tlc__wuvlr = c.pyapi.object_getattr_string(val, '_opaque')
            muudx__que = types.MemInfoPointer(types.voidptr)
            phflq__oqfo = c.unbox(muudx__que, tlc__wuvlr)
            mi = phflq__oqfo.value
            hahp__kdsud = muudx__que, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *hahp__kdsud)
            ucro__afkn = context.get_constant_null(hahp__kdsud[1])
            args = mi, ucro__afkn
            tftje__vmpbb, ptbzv__duzpn = c.pyapi.call_jit_code(convert, sig,
                args)
            c.context.nrt.decref(c.builder, typ, ptbzv__duzpn)
            c.pyapi.decref(tlc__wuvlr)
            ttp__wncrn = c.builder.basic_block
        with swub__jkpns:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", udrx__pipr, viw__sdaj)
            iwv__onm = c.builder.basic_block
    envth__xiv = c.builder.phi(ptbzv__duzpn.type)
    trba__lqdn = c.builder.phi(tftje__vmpbb.type)
    envth__xiv.add_incoming(ptbzv__duzpn, ttp__wncrn)
    envth__xiv.add_incoming(ptbzv__duzpn.type(None), iwv__onm)
    trba__lqdn.add_incoming(tftje__vmpbb, ttp__wncrn)
    trba__lqdn.add_incoming(cgutils.true_bit, iwv__onm)
    c.pyapi.decref(viw__sdaj)
    c.pyapi.decref(udrx__pipr)
    with c.builder.if_then(pfrsu__lsf):
        c.pyapi.decref(val)
    return NativeValue(envth__xiv, is_error=trba__lqdn)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype


def op_DICT_UPDATE_byteflow(self, state, inst):
    value = state.pop()
    index = inst.arg
    target = state.peek(index)
    updatevar = state.make_temp()
    res = state.make_temp()
    state.append(inst, target=target, value=value, updatevar=updatevar, res=res
        )


if _check_numba_change:
    if hasattr(numba.core.byteflow.TraceRunner, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_DICT_UPDATE has changed')
numba.core.byteflow.TraceRunner.op_DICT_UPDATE = op_DICT_UPDATE_byteflow


def op_DICT_UPDATE_interpreter(self, inst, target, value, updatevar, res):
    from numba.core import ir
    target = self.get(target)
    value = self.get(value)
    myds__pmboc = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=myds__pmboc, name=updatevar)
    fij__alh = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=fij__alh, name=res)


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_DICT_UPDATE has changed')
numba.core.interpreter.Interpreter.op_DICT_UPDATE = op_DICT_UPDATE_interpreter


@numba.extending.overload_method(numba.core.types.DictType, 'update')
def ol_dict_update(d, other):
    if not isinstance(d, numba.core.types.DictType):
        return
    if not isinstance(other, numba.core.types.DictType):
        return

    def impl(d, other):
        for jap__cuf, pxv__lvr in other.items():
            d[jap__cuf] = pxv__lvr
    return impl


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'ol_dict_update'):
        warnings.warn('numba.typed.dictobject.ol_dict_update has changed')


def op_CALL_FUNCTION_EX_byteflow(self, state, inst):
    from numba.core.utils import PYVERSION
    if inst.arg & 1 and PYVERSION != (3, 10):
        errmsg = 'CALL_FUNCTION_EX with **kwargs not supported'
        raise errors.UnsupportedError(errmsg)
    if inst.arg & 1:
        varkwarg = state.pop()
    else:
        varkwarg = None
    vararg = state.pop()
    func = state.pop()
    res = state.make_temp()
    state.append(inst, func=func, vararg=vararg, varkwarg=varkwarg, res=res)
    state.push(res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.byteflow.TraceRunner.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '349e7cfd27f5dab80fe15a7728c5f098f3f225ba8512d84331e39d01e863c6d4':
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX has changed')
numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_byteflow)


def op_CALL_FUNCTION_EX_interpreter(self, inst, func, vararg, varkwarg, res):
    func = self.get(func)
    vararg = self.get(vararg)
    if varkwarg is not None:
        varkwarg = self.get(varkwarg)
    dxzy__bjlyj = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(dxzy__bjlyj, res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.interpreter.Interpreter.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84846e5318ab7ccc8f9abaae6ab9e0ca879362648196f9d4b0ffb91cf2e01f5d':
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX has changed'
            )
numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_interpreter)


@classmethod
def ir_expr_call(cls, func, args, kws, loc, vararg=None, varkwarg=None,
    target=None):
    assert isinstance(func, ir.Var)
    assert isinstance(loc, ir.Loc)
    op = 'call'
    return cls(op=op, loc=loc, func=func, args=args, kws=kws, vararg=vararg,
        varkwarg=varkwarg, target=target)


if _check_numba_change:
    lines = inspect.getsource(ir.Expr.call)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '665601d0548d4f648d454492e542cb8aa241107a8df6bc68d0eec664c9ada738':
        warnings.warn('ir.Expr.call has changed')
ir.Expr.call = ir_expr_call


@staticmethod
def define_untyped_pipeline(state, name='untyped'):
    from numba.core.compiler_machinery import PassManager
    from numba.core.untyped_passes import DeadBranchPrune, FindLiterallyCalls, FixupArgs, GenericRewrites, InlineClosureLikes, InlineInlinables, IRProcessing, LiteralPropagationSubPipelinePass, LiteralUnroll, MakeFunctionToJitFunction, ReconstructSSA, RewriteSemanticConstants, TranslateByteCode, WithLifting
    from numba.core.utils import PYVERSION
    efl__tzkk = PassManager(name)
    if state.func_ir is None:
        efl__tzkk.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            efl__tzkk.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        efl__tzkk.add_pass(FixupArgs, 'fix up args')
    efl__tzkk.add_pass(IRProcessing, 'processing IR')
    efl__tzkk.add_pass(WithLifting, 'Handle with contexts')
    efl__tzkk.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        efl__tzkk.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        efl__tzkk.add_pass(DeadBranchPrune, 'dead branch pruning')
        efl__tzkk.add_pass(GenericRewrites, 'nopython rewrites')
    efl__tzkk.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    efl__tzkk.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        efl__tzkk.add_pass(DeadBranchPrune, 'dead branch pruning')
    efl__tzkk.add_pass(FindLiterallyCalls, 'find literally calls')
    efl__tzkk.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        efl__tzkk.add_pass(ReconstructSSA, 'ssa')
    efl__tzkk.add_pass(LiteralPropagationSubPipelinePass, 'Literal propagation'
        )
    efl__tzkk.finalize()
    return efl__tzkk


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fc5a0665658cc30588a78aca984ac2d323d5d3a45dce538cc62688530c772896':
        warnings.warn(
            'numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline has changed'
            )
numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline = (
    define_untyped_pipeline)


def mul_list_generic(self, args, kws):
    a, enyp__kwg = args
    if isinstance(a, types.List) and isinstance(enyp__kwg, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(enyp__kwg, types.List):
        return signature(enyp__kwg, types.intp, enyp__kwg)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.listdecl.MulList.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '95882385a8ffa67aa576e8169b9ee6b3197e0ad3d5def4b47fa65ce8cd0f1575':
        warnings.warn('numba.core.typing.listdecl.MulList.generic has changed')
numba.core.typing.listdecl.MulList.generic = mul_list_generic


@lower_builtin(operator.mul, types.Integer, types.List)
def list_mul(context, builder, sig, args):
    from llvmlite import ir as lir
    from numba.core.imputils import impl_ret_new_ref
    from numba.cpython.listobj import ListInstance
    if isinstance(sig.args[0], types.List):
        slvqk__bjin, caq__wbr = 0, 1
    else:
        slvqk__bjin, caq__wbr = 1, 0
    gmul__ufvka = ListInstance(context, builder, sig.args[slvqk__bjin],
        args[slvqk__bjin])
    viok__osf = gmul__ufvka.size
    avyf__fvbm = args[caq__wbr]
    vnsco__xst = lir.Constant(avyf__fvbm.type, 0)
    avyf__fvbm = builder.select(cgutils.is_neg_int(builder, avyf__fvbm),
        vnsco__xst, avyf__fvbm)
    rcf__leme = builder.mul(avyf__fvbm, viok__osf)
    yem__hjel = ListInstance.allocate(context, builder, sig.return_type,
        rcf__leme)
    yem__hjel.size = rcf__leme
    with cgutils.for_range_slice(builder, vnsco__xst, rcf__leme, viok__osf,
        inc=True) as (nsyr__baov, _):
        with cgutils.for_range(builder, viok__osf) as oxkx__diba:
            value = gmul__ufvka.getitem(oxkx__diba.index)
            yem__hjel.setitem(builder.add(oxkx__diba.index, nsyr__baov),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, yem__hjel.value)


def unify_pairs(self, first, second):
    from numba.core.typeconv import Conversion
    if first == second:
        return first
    if first is types.undefined:
        return second
    elif second is types.undefined:
        return first
    if first is types.unknown or second is types.unknown:
        return types.unknown
    qulwk__nin = first.unify(self, second)
    if qulwk__nin is not None:
        return qulwk__nin
    qulwk__nin = second.unify(self, first)
    if qulwk__nin is not None:
        return qulwk__nin
    nxvlg__rzdi = self.can_convert(fromty=first, toty=second)
    if nxvlg__rzdi is not None and nxvlg__rzdi <= Conversion.safe:
        return second
    nxvlg__rzdi = self.can_convert(fromty=second, toty=first)
    if nxvlg__rzdi is not None and nxvlg__rzdi <= Conversion.safe:
        return first
    if isinstance(first, types.Literal) or isinstance(second, types.Literal):
        first = types.unliteral(first)
        second = types.unliteral(second)
        return self.unify_pairs(first, second)
    return None


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.unify_pairs
        )
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f0eaf4cfdf1537691de26efd24d7e320f7c3f10d35e9aefe70cb946b3be0008c':
        warnings.warn(
            'numba.core.typing.context.BaseContext.unify_pairs has changed')
numba.core.typing.context.BaseContext.unify_pairs = unify_pairs


def _native_set_to_python_list(typ, payload, c):
    from llvmlite import ir
    rcf__leme = payload.used
    listobj = c.pyapi.list_new(rcf__leme)
    rlln__kgfo = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(rlln__kgfo, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(rcf__leme.
            type, 0))
        with payload._iterate() as oxkx__diba:
            i = c.builder.load(index)
            item = oxkx__diba.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return rlln__kgfo, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    rjbmr__bwdfe = h.type
    awf__xrdo = self.mask
    dtype = self._ty.dtype
    ybe__ldb = context.typing_context
    fnty = ybe__ldb.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(ybe__ldb, (dtype, dtype), {})
    ppay__bejr = context.get_function(fnty, sig)
    ynr__jrmbq = ir.Constant(rjbmr__bwdfe, 1)
    lkuo__vrlv = ir.Constant(rjbmr__bwdfe, 5)
    ltq__xyr = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, awf__xrdo))
    if for_insert:
        msws__tjsq = awf__xrdo.type(-1)
        syrg__dmebi = cgutils.alloca_once_value(builder, msws__tjsq)
    owxx__fksov = builder.append_basic_block('lookup.body')
    gesr__rnpi = builder.append_basic_block('lookup.found')
    rzxy__rupd = builder.append_basic_block('lookup.not_found')
    xlh__gxqb = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        pax__hvvs = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, pax__hvvs)):
            lmthe__zdi = ppay__bejr(builder, (item, entry.key))
            with builder.if_then(lmthe__zdi):
                builder.branch(gesr__rnpi)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, pax__hvvs)):
            builder.branch(rzxy__rupd)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, pax__hvvs)):
                ayny__hefxy = builder.load(syrg__dmebi)
                ayny__hefxy = builder.select(builder.icmp_unsigned('==',
                    ayny__hefxy, msws__tjsq), i, ayny__hefxy)
                builder.store(ayny__hefxy, syrg__dmebi)
    with cgutils.for_range(builder, ir.Constant(rjbmr__bwdfe, numba.cpython
        .setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, ynr__jrmbq)
        i = builder.and_(i, awf__xrdo)
        builder.store(i, index)
    builder.branch(owxx__fksov)
    with builder.goto_block(owxx__fksov):
        i = builder.load(index)
        check_entry(i)
        ixyzo__jyflm = builder.load(ltq__xyr)
        ixyzo__jyflm = builder.lshr(ixyzo__jyflm, lkuo__vrlv)
        i = builder.add(ynr__jrmbq, builder.mul(i, lkuo__vrlv))
        i = builder.and_(awf__xrdo, builder.add(i, ixyzo__jyflm))
        builder.store(i, index)
        builder.store(ixyzo__jyflm, ltq__xyr)
        builder.branch(owxx__fksov)
    with builder.goto_block(rzxy__rupd):
        if for_insert:
            i = builder.load(index)
            ayny__hefxy = builder.load(syrg__dmebi)
            i = builder.select(builder.icmp_unsigned('==', ayny__hefxy,
                msws__tjsq), i, ayny__hefxy)
            builder.store(i, index)
        builder.branch(xlh__gxqb)
    with builder.goto_block(gesr__rnpi):
        builder.branch(xlh__gxqb)
    builder.position_at_end(xlh__gxqb)
    kcch__tnbdo = builder.phi(ir.IntType(1), 'found')
    kcch__tnbdo.add_incoming(cgutils.true_bit, gesr__rnpi)
    kcch__tnbdo.add_incoming(cgutils.false_bit, rzxy__rupd)
    return kcch__tnbdo, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    pbx__xgbgt = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    bsnbb__nuvu = payload.used
    ynr__jrmbq = ir.Constant(bsnbb__nuvu.type, 1)
    bsnbb__nuvu = payload.used = builder.add(bsnbb__nuvu, ynr__jrmbq)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, pbx__xgbgt), likely=True):
        payload.fill = builder.add(payload.fill, ynr__jrmbq)
    if do_resize:
        self.upsize(bsnbb__nuvu)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    kcch__tnbdo, i = payload._lookup(item, h, for_insert=True)
    fkl__wubmw = builder.not_(kcch__tnbdo)
    with builder.if_then(fkl__wubmw):
        entry = payload.get_entry(i)
        pbx__xgbgt = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        bsnbb__nuvu = payload.used
        ynr__jrmbq = ir.Constant(bsnbb__nuvu.type, 1)
        bsnbb__nuvu = payload.used = builder.add(bsnbb__nuvu, ynr__jrmbq)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, pbx__xgbgt), likely=True):
            payload.fill = builder.add(payload.fill, ynr__jrmbq)
        if do_resize:
            self.upsize(bsnbb__nuvu)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    bsnbb__nuvu = payload.used
    ynr__jrmbq = ir.Constant(bsnbb__nuvu.type, 1)
    bsnbb__nuvu = payload.used = self._builder.sub(bsnbb__nuvu, ynr__jrmbq)
    if do_resize:
        self.downsize(bsnbb__nuvu)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    msm__che = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, msm__che)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    vceaw__dyfmh = payload
    rlln__kgfo = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(rlln__kgfo), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with vceaw__dyfmh._iterate() as oxkx__diba:
        entry = oxkx__diba.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(vceaw__dyfmh.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as oxkx__diba:
        entry = oxkx__diba.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    rlln__kgfo = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(rlln__kgfo), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    rlln__kgfo = cgutils.alloca_once_value(builder, cgutils.true_bit)
    rjbmr__bwdfe = context.get_value_type(types.intp)
    vnsco__xst = ir.Constant(rjbmr__bwdfe, 0)
    ynr__jrmbq = ir.Constant(rjbmr__bwdfe, 1)
    iwhe__jjubx = context.get_data_type(types.SetPayload(self._ty))
    zadz__zwe = context.get_abi_sizeof(iwhe__jjubx)
    lngt__nvq = self._entrysize
    zadz__zwe -= lngt__nvq
    gdinn__bpg, qbws__heci = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(rjbmr__bwdfe, lngt__nvq), ir.Constant(rjbmr__bwdfe,
        zadz__zwe))
    with builder.if_then(qbws__heci, likely=False):
        builder.store(cgutils.false_bit, rlln__kgfo)
    with builder.if_then(builder.load(rlln__kgfo), likely=True):
        if realloc:
            eggh__orqa = self._set.meminfo
            npxfq__hra = context.nrt.meminfo_varsize_alloc(builder,
                eggh__orqa, size=gdinn__bpg)
            qzk__rumgk = cgutils.is_null(builder, npxfq__hra)
        else:
            jrqo__diqx = _imp_dtor(context, builder.module, self._ty)
            eggh__orqa = context.nrt.meminfo_new_varsize_dtor(builder,
                gdinn__bpg, builder.bitcast(jrqo__diqx, cgutils.voidptr_t))
            qzk__rumgk = cgutils.is_null(builder, eggh__orqa)
        with builder.if_else(qzk__rumgk, likely=False) as (bnx__akmzz,
            hej__wdkg):
            with bnx__akmzz:
                builder.store(cgutils.false_bit, rlln__kgfo)
            with hej__wdkg:
                if not realloc:
                    self._set.meminfo = eggh__orqa
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, gdinn__bpg, 255)
                payload.used = vnsco__xst
                payload.fill = vnsco__xst
                payload.finger = vnsco__xst
                ner__qsjm = builder.sub(nentries, ynr__jrmbq)
                payload.mask = ner__qsjm
    return builder.load(rlln__kgfo)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    rlln__kgfo = cgutils.alloca_once_value(builder, cgutils.true_bit)
    rjbmr__bwdfe = context.get_value_type(types.intp)
    vnsco__xst = ir.Constant(rjbmr__bwdfe, 0)
    ynr__jrmbq = ir.Constant(rjbmr__bwdfe, 1)
    iwhe__jjubx = context.get_data_type(types.SetPayload(self._ty))
    zadz__zwe = context.get_abi_sizeof(iwhe__jjubx)
    lngt__nvq = self._entrysize
    zadz__zwe -= lngt__nvq
    awf__xrdo = src_payload.mask
    nentries = builder.add(ynr__jrmbq, awf__xrdo)
    gdinn__bpg = builder.add(ir.Constant(rjbmr__bwdfe, zadz__zwe), builder.
        mul(ir.Constant(rjbmr__bwdfe, lngt__nvq), nentries))
    with builder.if_then(builder.load(rlln__kgfo), likely=True):
        jrqo__diqx = _imp_dtor(context, builder.module, self._ty)
        eggh__orqa = context.nrt.meminfo_new_varsize_dtor(builder,
            gdinn__bpg, builder.bitcast(jrqo__diqx, cgutils.voidptr_t))
        qzk__rumgk = cgutils.is_null(builder, eggh__orqa)
        with builder.if_else(qzk__rumgk, likely=False) as (bnx__akmzz,
            hej__wdkg):
            with bnx__akmzz:
                builder.store(cgutils.false_bit, rlln__kgfo)
            with hej__wdkg:
                self._set.meminfo = eggh__orqa
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = vnsco__xst
                payload.mask = awf__xrdo
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, lngt__nvq)
                with src_payload._iterate() as oxkx__diba:
                    context.nrt.incref(builder, self._ty.dtype, oxkx__diba.
                        entry.key)
    return builder.load(rlln__kgfo)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    exqla__uupf = context.get_value_type(types.voidptr)
    paf__tqfo = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [exqla__uupf, paf__tqfo, exqla__uupf]
        )
    rnk__bcd = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=rnk__bcd)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        ubx__rtnty = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer()
            )
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, ubx__rtnty)
        with payload._iterate() as oxkx__diba:
            entry = oxkx__diba.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    qql__tlppf, = sig.args
    dcd__ojwo, = args
    lezis__cksx = numba.core.imputils.call_len(context, builder, qql__tlppf,
        dcd__ojwo)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, lezis__cksx)
    with numba.core.imputils.for_iter(context, builder, qql__tlppf, dcd__ojwo
        ) as oxkx__diba:
        inst.add(oxkx__diba.value)
        context.nrt.decref(builder, set_type.dtype, oxkx__diba.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    qql__tlppf = sig.args[1]
    dcd__ojwo = args[1]
    lezis__cksx = numba.core.imputils.call_len(context, builder, qql__tlppf,
        dcd__ojwo)
    if lezis__cksx is not None:
        wku__fjej = builder.add(inst.payload.used, lezis__cksx)
        inst.upsize(wku__fjej)
    with numba.core.imputils.for_iter(context, builder, qql__tlppf, dcd__ojwo
        ) as oxkx__diba:
        yhnc__ddr = context.cast(builder, oxkx__diba.value, qql__tlppf.
            dtype, inst.dtype)
        inst.add(yhnc__ddr)
        context.nrt.decref(builder, qql__tlppf.dtype, oxkx__diba.value)
    if lezis__cksx is not None:
        inst.downsize(inst.payload.used)
    return context.get_dummy_value()


if _check_numba_change:
    for name, orig, hash in ((
        'numba.core.boxing._native_set_to_python_list', numba.core.boxing.
        _native_set_to_python_list,
        'b47f3d5e582c05d80899ee73e1c009a7e5121e7a660d42cb518bb86933f3c06f'),
        ('numba.cpython.setobj._SetPayload._lookup', numba.cpython.setobj.
        _SetPayload._lookup,
        'c797b5399d7b227fe4eea3a058b3d3103f59345699388afb125ae47124bee395'),
        ('numba.cpython.setobj.SetInstance._add_entry', numba.cpython.
        setobj.SetInstance._add_entry,
        'c5ed28a5fdb453f242e41907cb792b66da2df63282c17abe0b68fc46782a7f94'),
        ('numba.cpython.setobj.SetInstance._add_key', numba.cpython.setobj.
        SetInstance._add_key,
        '324d6172638d02a361cfa0ca7f86e241e5a56a008d4ab581a305f9ae5ea4a75f'),
        ('numba.cpython.setobj.SetInstance._remove_entry', numba.cpython.
        setobj.SetInstance._remove_entry,
        '2c441b00daac61976e673c0e738e8e76982669bd2851951890dd40526fa14da1'),
        ('numba.cpython.setobj.SetInstance.pop', numba.cpython.setobj.
        SetInstance.pop,
        '1a7b7464cbe0577f2a38f3af9acfef6d4d25d049b1e216157275fbadaab41d1b'),
        ('numba.cpython.setobj.SetInstance._resize', numba.cpython.setobj.
        SetInstance._resize,
        '5ca5c2ba4f8c4bf546fde106b9c2656d4b22a16d16e163fb64c5d85ea4d88746'),
        ('numba.cpython.setobj.SetInstance._replace_payload', numba.cpython
        .setobj.SetInstance._replace_payload,
        'ada75a6c85828bff69c8469538c1979801f560a43fb726221a9c21bf208ae78d'),
        ('numba.cpython.setobj.SetInstance._allocate_payload', numba.
        cpython.setobj.SetInstance._allocate_payload,
        '2e80c419df43ebc71075b4f97fc1701c10dbc576aed248845e176b8d5829e61b'),
        ('numba.cpython.setobj.SetInstance._copy_payload', numba.cpython.
        setobj.SetInstance._copy_payload,
        '0885ac36e1eb5a0a0fc4f5d91e54b2102b69e536091fed9f2610a71d225193ec'),
        ('numba.cpython.setobj.set_constructor', numba.cpython.setobj.
        set_constructor,
        '3d521a60c3b8eaf70aa0f7267427475dfddd8f5e5053b5bfe309bb5f1891b0ce'),
        ('numba.cpython.setobj.set_update', numba.cpython.setobj.set_update,
        '965c4f7f7abcea5cbe0491b602e6d4bcb1800fa1ec39b1ffccf07e1bc56051c3')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.boxing._native_set_to_python_list = _native_set_to_python_list
numba.cpython.setobj._SetPayload._lookup = _lookup
numba.cpython.setobj.SetInstance._add_entry = _add_entry
numba.cpython.setobj.SetInstance._add_key = _add_key
numba.cpython.setobj.SetInstance._remove_entry = _remove_entry
numba.cpython.setobj.SetInstance.pop = pop
numba.cpython.setobj.SetInstance._resize = _resize
numba.cpython.setobj.SetInstance._replace_payload = _replace_payload
numba.cpython.setobj.SetInstance._allocate_payload = _allocate_payload
numba.cpython.setobj.SetInstance._copy_payload = _copy_payload


def _reduce(self):
    libdata = self.library.serialize_using_object_code()
    typeann = str(self.type_annotation)
    fndesc = self.fndesc
    fndesc.typemap = fndesc.calltypes = None
    referenced_envs = self._find_referenced_environments()
    dgv__gcfo = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, dgv__gcfo, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    xxu__bkn = target_context.get_executable(library, fndesc, env)
    lmcad__xow = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=xxu__bkn, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return lmcad__xow


if _check_numba_change:
    for name, orig, hash in (('numba.core.compiler.CompileResult._reduce',
        numba.core.compiler.CompileResult._reduce,
        '5f86eacfa5202c202b3dc200f1a7a9b6d3f9d1ec16d43a52cb2d580c34fbfa82'),
        ('numba.core.compiler.CompileResult._rebuild', numba.core.compiler.
        CompileResult._rebuild,
        '44fa9dc2255883ab49195d18c3cca8c0ad715d0dd02033bd7e2376152edc4e84')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.compiler.CompileResult._reduce = _reduce
numba.core.compiler.CompileResult._rebuild = _rebuild
if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._IPythonCacheLocator.
        get_cache_path)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'eb33b7198697b8ef78edddcf69e58973c44744ff2cb2f54d4015611ad43baed0':
        warnings.warn(
            'numba.core.caching._IPythonCacheLocator.get_cache_path has changed'
            )
if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:

    def _get_cache_path(self):
        return numba.config.CACHE_DIR
    numba.core.caching._IPythonCacheLocator.get_cache_path = _get_cache_path
if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.Bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '977423d833eeb4b8fd0c87f55dce7251c107d8d10793fe5723de6e5452da32e2':
        warnings.warn('numba.core.types.containers.Bytes has changed')
numba.core.types.containers.Bytes.slice_is_copy = True
if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheLocator.
        ensure_cache_path)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '906b6f516f76927dfbe69602c335fa151b9f33d40dfe171a9190c0d11627bc03':
        warnings.warn(
            'numba.core.caching._CacheLocator.ensure_cache_path has changed')
if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
    import tempfile

    def _ensure_cache_path(self):
        from mpi4py import MPI
        qzchy__ujbj = MPI.COMM_WORLD
        if qzchy__ujbj.Get_rank() == 0:
            ozbr__xdcg = self.get_cache_path()
            os.makedirs(ozbr__xdcg, exist_ok=True)
            tempfile.TemporaryFile(dir=ozbr__xdcg).close()
    numba.core.caching._CacheLocator.ensure_cache_path = _ensure_cache_path


def _analyze_op_call_builtins_len(self, scope, equiv_set, loc, args, kws):
    from numba.parfors.array_analysis import ArrayAnalysis
    require(len(args) == 1)
    var = args[0]
    typ = self.typemap[var.name]
    require(isinstance(typ, types.ArrayCompatible))
    require(not isinstance(typ, types.Bytes))
    shape = equiv_set._get_shape(var)
    return ArrayAnalysis.AnalyzeResult(shape=shape[0], rhs=shape[0])


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_op_call_builtins_len)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '612cbc67e8e462f25f348b2a5dd55595f4201a6af826cffcd38b16cd85fc70f7':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_op_call_builtins_len has changed'
            )
(numba.parfors.array_analysis.ArrayAnalysis._analyze_op_call_builtins_len
    ) = _analyze_op_call_builtins_len


def generic(self, args, kws):
    assert not kws
    val, = args
    if isinstance(val, (types.Buffer, types.BaseTuple)) and not isinstance(val,
        types.Bytes):
        return signature(types.intp, val)
    elif isinstance(val, types.RangeType):
        return signature(val.dtype, val)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.Len.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '88d54238ebe0896f4s69b7347105a6a68dec443036a61f9e494c1630c62b0fa76':
        warnings.warn('numba.core.typing.builtins.Len.generic has changed')
numba.core.typing.builtins.Len.generic = generic
from numba.cpython import charseq


def _make_constant_bytes(context, builder, nbytes):
    from llvmlite import ir
    rdax__fyca = cgutils.create_struct_proxy(charseq.bytes_type)
    uxm__llsxa = rdax__fyca(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(uxm__llsxa.nitems.type, nbytes)
    uxm__llsxa.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    uxm__llsxa.nitems = nbytes
    uxm__llsxa.itemsize = ir.Constant(uxm__llsxa.itemsize.type, 1)
    uxm__llsxa.data = context.nrt.meminfo_data(builder, uxm__llsxa.meminfo)
    uxm__llsxa.parent = cgutils.get_null_value(uxm__llsxa.parent.type)
    uxm__llsxa.shape = cgutils.pack_array(builder, [uxm__llsxa.nitems],
        context.get_value_type(types.intp))
    uxm__llsxa.strides = cgutils.pack_array(builder, [ir.Constant(
        uxm__llsxa.strides.type.element, 1)], context.get_value_type(types.
        intp))
    return uxm__llsxa


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
