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
    yzla__oarjv = numba.core.bytecode.FunctionIdentity.from_function(func)
    sfjo__tzgja = numba.core.interpreter.Interpreter(yzla__oarjv)
    bcer__xge = numba.core.bytecode.ByteCode(func_id=yzla__oarjv)
    func_ir = sfjo__tzgja.interpret(bcer__xge)
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
        qdhz__nko = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        qdhz__nko.run()
    bwt__onio = numba.core.postproc.PostProcessor(func_ir)
    bwt__onio.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, ayc__jzagu in visit_vars_extensions.items():
        if isinstance(stmt, t):
            ayc__jzagu(stmt, callback, cbdata)
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
    mqnja__pyghk = ['ravel', 'transpose', 'reshape']
    for znx__snxii in blocks.values():
        for bcn__efs in znx__snxii.body:
            if type(bcn__efs) in alias_analysis_extensions:
                ayc__jzagu = alias_analysis_extensions[type(bcn__efs)]
                ayc__jzagu(bcn__efs, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(bcn__efs, ir.Assign):
                joog__csr = bcn__efs.value
                gnog__lsje = bcn__efs.target.name
                if is_immutable_type(gnog__lsje, typemap):
                    continue
                if isinstance(joog__csr, ir.Var
                    ) and gnog__lsje != joog__csr.name:
                    _add_alias(gnog__lsje, joog__csr.name, alias_map,
                        arg_aliases)
                if isinstance(joog__csr, ir.Expr) and (joog__csr.op ==
                    'cast' or joog__csr.op in ['getitem', 'static_getitem']):
                    _add_alias(gnog__lsje, joog__csr.value.name, alias_map,
                        arg_aliases)
                if isinstance(joog__csr, ir.Expr
                    ) and joog__csr.op == 'inplace_binop':
                    _add_alias(gnog__lsje, joog__csr.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(joog__csr, ir.Expr
                    ) and joog__csr.op == 'getattr' and joog__csr.attr in ['T',
                    'ctypes', 'flat']:
                    _add_alias(gnog__lsje, joog__csr.value.name, alias_map,
                        arg_aliases)
                if isinstance(joog__csr, ir.Expr
                    ) and joog__csr.op == 'getattr' and joog__csr.attr not in [
                    'shape'] and joog__csr.value.name in arg_aliases:
                    _add_alias(gnog__lsje, joog__csr.value.name, alias_map,
                        arg_aliases)
                if isinstance(joog__csr, ir.Expr
                    ) and joog__csr.op == 'getattr' and joog__csr.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(gnog__lsje, joog__csr.value.name, alias_map,
                        arg_aliases)
                if isinstance(joog__csr, ir.Expr) and joog__csr.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(gnog__lsje, typemap):
                    for url__mpib in joog__csr.items:
                        _add_alias(gnog__lsje, url__mpib.name, alias_map,
                            arg_aliases)
                if isinstance(joog__csr, ir.Expr) and joog__csr.op == 'call':
                    lrm__zfni = guard(find_callname, func_ir, joog__csr,
                        typemap)
                    if lrm__zfni is None:
                        continue
                    jwkw__dvm, dpvo__uwr = lrm__zfni
                    if lrm__zfni in alias_func_extensions:
                        nilka__viuss = alias_func_extensions[lrm__zfni]
                        nilka__viuss(gnog__lsje, joog__csr.args, alias_map,
                            arg_aliases)
                    if dpvo__uwr == 'numpy' and jwkw__dvm in mqnja__pyghk:
                        _add_alias(gnog__lsje, joog__csr.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(dpvo__uwr, ir.Var
                        ) and jwkw__dvm in mqnja__pyghk:
                        _add_alias(gnog__lsje, dpvo__uwr.name, alias_map,
                            arg_aliases)
    omfy__ttn = copy.deepcopy(alias_map)
    for url__mpib in omfy__ttn:
        for dqopg__vcwl in omfy__ttn[url__mpib]:
            alias_map[url__mpib] |= alias_map[dqopg__vcwl]
        for dqopg__vcwl in omfy__ttn[url__mpib]:
            alias_map[dqopg__vcwl] = alias_map[url__mpib]
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
    cph__nhcom = compute_cfg_from_blocks(func_ir.blocks)
    vtxn__hkmdc = compute_use_defs(func_ir.blocks)
    hzzcy__zgka = compute_live_map(cph__nhcom, func_ir.blocks, vtxn__hkmdc.
        usemap, vtxn__hkmdc.defmap)
    tpgm__pej = True
    while tpgm__pej:
        tpgm__pej = False
        for label, block in func_ir.blocks.items():
            lives = {url__mpib.name for url__mpib in block.terminator.
                list_vars()}
            for cvfno__gry, ydnx__hsykj in cph__nhcom.successors(label):
                lives |= hzzcy__zgka[cvfno__gry]
            rbn__jdy = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    gnog__lsje = stmt.target
                    kaits__phjfa = stmt.value
                    if gnog__lsje.name not in lives:
                        if isinstance(kaits__phjfa, ir.Expr
                            ) and kaits__phjfa.op == 'make_function':
                            continue
                        if isinstance(kaits__phjfa, ir.Expr
                            ) and kaits__phjfa.op == 'getattr':
                            continue
                        if isinstance(kaits__phjfa, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(gnog__lsje,
                            None), types.Function):
                            continue
                        if isinstance(kaits__phjfa, ir.Expr
                            ) and kaits__phjfa.op == 'build_map':
                            continue
                        if isinstance(kaits__phjfa, ir.Expr
                            ) and kaits__phjfa.op == 'build_tuple':
                            continue
                        if isinstance(kaits__phjfa, ir.Expr
                            ) and kaits__phjfa.op == 'binop':
                            continue
                        if isinstance(kaits__phjfa, ir.Expr
                            ) and kaits__phjfa.op == 'unary':
                            continue
                        if isinstance(kaits__phjfa, ir.Expr
                            ) and kaits__phjfa.op in ('static_getitem',
                            'getitem'):
                            continue
                    if isinstance(kaits__phjfa, ir.Var
                        ) and gnog__lsje.name == kaits__phjfa.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    fqx__ftes = analysis.ir_extension_usedefs[type(stmt)]
                    jht__ghjkv, qtk__cdnk = fqx__ftes(stmt)
                    lives -= qtk__cdnk
                    lives |= jht__ghjkv
                else:
                    lives |= {url__mpib.name for url__mpib in stmt.list_vars()}
                    if isinstance(stmt, ir.Assign):
                        jgn__qzps = set()
                        if isinstance(kaits__phjfa, ir.Expr):
                            jgn__qzps = {url__mpib.name for url__mpib in
                                kaits__phjfa.list_vars()}
                        if gnog__lsje.name not in jgn__qzps:
                            lives.remove(gnog__lsje.name)
                rbn__jdy.append(stmt)
            rbn__jdy.reverse()
            if len(block.body) != len(rbn__jdy):
                tpgm__pej = True
            block.body = rbn__jdy


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    bsm__eatsw = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (bsm__eatsw,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    gctcj__cmfv = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), gctcj__cmfv)


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
            for xvg__biex in fnty.templates:
                self._inline_overloads.update(xvg__biex._inline_overloads)
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
    gctcj__cmfv = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), gctcj__cmfv)
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
    munxj__ouoaq, rwm__eeylv = self._get_impl(args, kws)
    if munxj__ouoaq is None:
        return
    srs__fnuzx = types.Dispatcher(munxj__ouoaq)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        xfvs__eppr = munxj__ouoaq._compiler
        flags = compiler.Flags()
        dhmlk__fxn = xfvs__eppr.targetdescr.typing_context
        ady__cykuy = xfvs__eppr.targetdescr.target_context
        geqn__lgrz = xfvs__eppr.pipeline_class(dhmlk__fxn, ady__cykuy, None,
            None, None, flags, None)
        cndvp__txb = InlineWorker(dhmlk__fxn, ady__cykuy, xfvs__eppr.locals,
            geqn__lgrz, flags, None)
        qay__djzdm = srs__fnuzx.dispatcher.get_call_template
        xvg__biex, pcox__oupo, jvfd__atiav, kws = qay__djzdm(rwm__eeylv, kws)
        if jvfd__atiav in self._inline_overloads:
            return self._inline_overloads[jvfd__atiav]['iinfo'].signature
        ir = cndvp__txb.run_untyped_passes(srs__fnuzx.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, ady__cykuy, ir, jvfd__atiav, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, jvfd__atiav, None)
        self._inline_overloads[sig.args] = {'folded_args': jvfd__atiav}
        qiy__ffbpq = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = qiy__ffbpq
        if not self._inline.is_always_inline:
            sig = srs__fnuzx.get_call_type(self.context, rwm__eeylv, kws)
            self._compiled_overloads[sig.args] = srs__fnuzx.get_overload(sig)
        xtmc__oga = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': jvfd__atiav,
            'iinfo': xtmc__oga}
    else:
        sig = srs__fnuzx.get_call_type(self.context, rwm__eeylv, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = srs__fnuzx.get_overload(sig)
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
    rqjs__qzuaq = [True, False]
    pleg__darpl = [False, True]
    syoq__vbiv = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    okgf__zro = get_local_target(context)
    xbigc__atigq = utils.order_by_target_specificity(okgf__zro, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for dtpk__owqf in xbigc__atigq:
        gqlo__tdhc = dtpk__owqf(context)
        udmr__anv = rqjs__qzuaq if gqlo__tdhc.prefer_literal else pleg__darpl
        udmr__anv = [True] if getattr(gqlo__tdhc, '_no_unliteral', False
            ) else udmr__anv
        for zij__gzqvn in udmr__anv:
            try:
                if zij__gzqvn:
                    sig = gqlo__tdhc.apply(args, kws)
                else:
                    jkx__epf = tuple([_unlit_non_poison(a) for a in args])
                    yspfk__cun = {gmm__rih: _unlit_non_poison(url__mpib) for
                        gmm__rih, url__mpib in kws.items()}
                    sig = gqlo__tdhc.apply(jkx__epf, yspfk__cun)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    syoq__vbiv.add_error(gqlo__tdhc, False, e, zij__gzqvn)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = gqlo__tdhc.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    aowe__ehrmy = getattr(gqlo__tdhc, 'cases', None)
                    if aowe__ehrmy is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            aowe__ehrmy)
                    else:
                        msg = 'No match.'
                    syoq__vbiv.add_error(gqlo__tdhc, True, msg, zij__gzqvn)
    syoq__vbiv.raise_error()


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
    xvg__biex = self.template(context)
    fym__jjgcs = None
    ewdok__ipgbm = None
    ugbgp__gcsct = None
    udmr__anv = [True, False] if xvg__biex.prefer_literal else [False, True]
    udmr__anv = [True] if getattr(xvg__biex, '_no_unliteral', False
        ) else udmr__anv
    for zij__gzqvn in udmr__anv:
        if zij__gzqvn:
            try:
                ugbgp__gcsct = xvg__biex.apply(args, kws)
            except Exception as bmj__jtf:
                if isinstance(bmj__jtf, errors.ForceLiteralArg):
                    raise bmj__jtf
                fym__jjgcs = bmj__jtf
                ugbgp__gcsct = None
            else:
                break
        else:
            kywvz__wxiya = tuple([_unlit_non_poison(a) for a in args])
            mpl__nsiyb = {gmm__rih: _unlit_non_poison(url__mpib) for 
                gmm__rih, url__mpib in kws.items()}
            mgn__bsddt = kywvz__wxiya == args and kws == mpl__nsiyb
            if not mgn__bsddt and ugbgp__gcsct is None:
                try:
                    ugbgp__gcsct = xvg__biex.apply(kywvz__wxiya, mpl__nsiyb)
                except Exception as bmj__jtf:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(bmj__jtf
                        , errors.NumbaError):
                        raise bmj__jtf
                    if isinstance(bmj__jtf, errors.ForceLiteralArg):
                        if xvg__biex.prefer_literal:
                            raise bmj__jtf
                    ewdok__ipgbm = bmj__jtf
                else:
                    break
    if ugbgp__gcsct is None and (ewdok__ipgbm is not None or fym__jjgcs is not
        None):
        jyzz__sxs = '- Resolution failure for {} arguments:\n{}\n'
        eycex__czdq = _termcolor.highlight(jyzz__sxs)
        if numba.core.config.DEVELOPER_MODE:
            pci__hykm = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    ddq__zsxyi = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    ddq__zsxyi = ['']
                lveez__aujk = '\n{}'.format(2 * pci__hykm)
                mpyra__hroov = _termcolor.reset(lveez__aujk + lveez__aujk.
                    join(_bt_as_lines(ddq__zsxyi)))
                return _termcolor.reset(mpyra__hroov)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            mjye__cobhi = str(e)
            mjye__cobhi = mjye__cobhi if mjye__cobhi else str(repr(e)
                ) + add_bt(e)
            gan__sef = errors.TypingError(textwrap.dedent(mjye__cobhi))
            return eycex__czdq.format(literalness, str(gan__sef))
        import bodo
        if isinstance(fym__jjgcs, bodo.utils.typing.BodoError):
            raise fym__jjgcs
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', fym__jjgcs) +
                nested_msg('non-literal', ewdok__ipgbm))
        else:
            if 'missing a required argument' in fym__jjgcs.msg:
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
            raise errors.TypingError(msg, loc=fym__jjgcs.loc)
    return ugbgp__gcsct


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
    jwkw__dvm = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=jwkw__dvm)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            bgq__rpduw = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), bgq__rpduw)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    frv__kolv = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            frv__kolv.append(types.Omitted(a.value))
        else:
            frv__kolv.append(self.typeof_pyval(a))
    czdq__ruw = None
    try:
        error = None
        czdq__ruw = self.compile(tuple(frv__kolv))
    except errors.ForceLiteralArg as e:
        ljxm__sbqt = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if ljxm__sbqt:
            wdpxb__etk = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            dsbjz__mrg = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(ljxm__sbqt))
            raise errors.CompilerError(wdpxb__etk.format(dsbjz__mrg))
        rwm__eeylv = []
        try:
            for i, url__mpib in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        rwm__eeylv.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        rwm__eeylv.append(types.literal(args[i]))
                else:
                    rwm__eeylv.append(args[i])
            args = rwm__eeylv
        except (OSError, FileNotFoundError) as qva__piywf:
            error = FileNotFoundError(str(qva__piywf) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                czdq__ruw = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        vrji__nxi = []
        for i, lvkog__cndy in enumerate(args):
            val = lvkog__cndy.value if isinstance(lvkog__cndy, numba.core.
                dispatcher.OmittedArg) else lvkog__cndy
            try:
                enua__xtleu = typeof(val, Purpose.argument)
            except ValueError as kji__ehp:
                vrji__nxi.append((i, str(kji__ehp)))
            else:
                if enua__xtleu is None:
                    vrji__nxi.append((i,
                        f'cannot determine Numba type of value {val}'))
        if vrji__nxi:
            nuid__ino = '\n'.join(f'- argument {i}: {hmt__jinrm}' for i,
                hmt__jinrm in vrji__nxi)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{nuid__ino}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                vdhc__iyeim = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                fxrgn__bnm = False
                for oklp__aup in vdhc__iyeim:
                    if oklp__aup in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        fxrgn__bnm = True
                        break
                if not fxrgn__bnm:
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
                bgq__rpduw = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), bgq__rpduw)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return czdq__ruw


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
    for yswx__ywrx in cres.library._codegen._engine._defined_symbols:
        if yswx__ywrx.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in yswx__ywrx and (
            'bodo_gb_udf_update_local' in yswx__ywrx or 
            'bodo_gb_udf_combine' in yswx__ywrx or 'bodo_gb_udf_eval' in
            yswx__ywrx or 'bodo_gb_apply_general_udfs' in yswx__ywrx):
            gb_agg_cfunc_addr[yswx__ywrx
                ] = cres.library.get_pointer_to_function(yswx__ywrx)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for yswx__ywrx in cres.library._codegen._engine._defined_symbols:
        if yswx__ywrx.startswith('cfunc') and ('get_join_cond_addr' not in
            yswx__ywrx or 'bodo_join_gen_cond' in yswx__ywrx):
            join_gen_cond_cfunc_addr[yswx__ywrx
                ] = cres.library.get_pointer_to_function(yswx__ywrx)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    munxj__ouoaq = self._get_dispatcher_for_current_target()
    if munxj__ouoaq is not self:
        return munxj__ouoaq.compile(sig)
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
            yaio__azelc = self.overloads.get(tuple(args))
            if yaio__azelc is not None:
                return yaio__azelc.entry_point
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
            gzorx__nvj = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=gzorx__nvj):
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
                yri__zvmkf = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in yri__zvmkf:
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
    kjste__tbzff = self._final_module
    ykp__tlrr = []
    ezvlj__zvkr = 0
    for fn in kjste__tbzff.functions:
        ezvlj__zvkr += 1
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
            ykp__tlrr.append(fn.name)
    if ezvlj__zvkr == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if ykp__tlrr:
        kjste__tbzff = kjste__tbzff.clone()
        for name in ykp__tlrr:
            kjste__tbzff.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = kjste__tbzff
    return kjste__tbzff


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
    for aclg__ppjv in self.constraints:
        loc = aclg__ppjv.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                aclg__ppjv(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                umj__ckd = numba.core.errors.TypingError(str(e), loc=
                    aclg__ppjv.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(umj__ckd, e))
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
                    umj__ckd = numba.core.errors.TypingError(msg.format(con
                        =aclg__ppjv, err=str(e)), loc=aclg__ppjv.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(umj__ckd, e))
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
    for zmijg__klpdx in self._failures.values():
        for qod__prdt in zmijg__klpdx:
            if isinstance(qod__prdt.error, ForceLiteralArg):
                raise qod__prdt.error
            if isinstance(qod__prdt.error, bodo.utils.typing.BodoError):
                raise qod__prdt.error
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
    emks__kgtv = False
    rbn__jdy = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        vuklb__zyys = set()
        hyq__hhpr = lives & alias_set
        for url__mpib in hyq__hhpr:
            vuklb__zyys |= alias_map[url__mpib]
        lives_n_aliases = lives | vuklb__zyys | arg_aliases
        if type(stmt) in remove_dead_extensions:
            ayc__jzagu = remove_dead_extensions[type(stmt)]
            stmt = ayc__jzagu(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                emks__kgtv = True
                continue
        if isinstance(stmt, ir.Assign):
            gnog__lsje = stmt.target
            kaits__phjfa = stmt.value
            if gnog__lsje.name not in lives:
                if has_no_side_effect(kaits__phjfa, lives_n_aliases, call_table
                    ):
                    emks__kgtv = True
                    continue
                if isinstance(kaits__phjfa, ir.Expr
                    ) and kaits__phjfa.op == 'call' and call_table[kaits__phjfa
                    .func.name] == ['astype']:
                    ydoep__aho = guard(get_definition, func_ir,
                        kaits__phjfa.func)
                    if (ydoep__aho is not None and ydoep__aho.op ==
                        'getattr' and isinstance(typemap[ydoep__aho.value.
                        name], types.Array) and ydoep__aho.attr == 'astype'):
                        emks__kgtv = True
                        continue
            if saved_array_analysis and gnog__lsje.name in lives and is_expr(
                kaits__phjfa, 'getattr'
                ) and kaits__phjfa.attr == 'shape' and is_array_typ(typemap
                [kaits__phjfa.value.name]
                ) and kaits__phjfa.value.name not in lives:
                gxlu__cmb = {url__mpib: gmm__rih for gmm__rih, url__mpib in
                    func_ir.blocks.items()}
                if block in gxlu__cmb:
                    label = gxlu__cmb[block]
                    hoftj__hgcyz = saved_array_analysis.get_equiv_set(label)
                    fqff__wgge = hoftj__hgcyz.get_equiv_set(kaits__phjfa.value)
                    if fqff__wgge is not None:
                        for url__mpib in fqff__wgge:
                            if url__mpib.endswith('#0'):
                                url__mpib = url__mpib[:-2]
                            if url__mpib in typemap and is_array_typ(typemap
                                [url__mpib]) and url__mpib in lives:
                                kaits__phjfa.value = ir.Var(kaits__phjfa.
                                    value.scope, url__mpib, kaits__phjfa.
                                    value.loc)
                                emks__kgtv = True
                                break
            if isinstance(kaits__phjfa, ir.Var
                ) and gnog__lsje.name == kaits__phjfa.name:
                emks__kgtv = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                emks__kgtv = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            fqx__ftes = analysis.ir_extension_usedefs[type(stmt)]
            jht__ghjkv, qtk__cdnk = fqx__ftes(stmt)
            lives -= qtk__cdnk
            lives |= jht__ghjkv
        else:
            lives |= {url__mpib.name for url__mpib in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                jgn__qzps = set()
                if isinstance(kaits__phjfa, ir.Expr):
                    jgn__qzps = {url__mpib.name for url__mpib in
                        kaits__phjfa.list_vars()}
                if gnog__lsje.name not in jgn__qzps:
                    lives.remove(gnog__lsje.name)
        rbn__jdy.append(stmt)
    rbn__jdy.reverse()
    block.body = rbn__jdy
    return emks__kgtv


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            degt__kcrl, = args
            if isinstance(degt__kcrl, types.IterableType):
                dtype = degt__kcrl.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), degt__kcrl)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    bbxx__durs = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (bbxx__durs, self.dtype)
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
        except LiteralTypingError as rsp__kos:
            return
    try:
        return literal(value)
    except LiteralTypingError as rsp__kos:
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
        xsotr__nfxgj = py_func.__qualname__
    except AttributeError as rsp__kos:
        xsotr__nfxgj = py_func.__name__
    enea__mhg = inspect.getfile(py_func)
    for cls in self._locator_classes:
        sdvyx__ukaaj = cls.from_function(py_func, enea__mhg)
        if sdvyx__ukaaj is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (xsotr__nfxgj, enea__mhg))
    self._locator = sdvyx__ukaaj
    swmne__vdjnq = inspect.getfile(py_func)
    strk__qpvvg = os.path.splitext(os.path.basename(swmne__vdjnq))[0]
    if enea__mhg.startswith('<ipython-'):
        wzs__jik = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)', '\\1\\3',
            strk__qpvvg, count=1)
        if wzs__jik == strk__qpvvg:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        strk__qpvvg = wzs__jik
    kzr__bgnms = '%s.%s' % (strk__qpvvg, xsotr__nfxgj)
    dldlh__rwuc = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(kzr__bgnms, dldlh__rwuc
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    swt__wnlki = list(filter(lambda a: self._istuple(a.name), args))
    if len(swt__wnlki) == 2 and fn.__name__ == 'add':
        hnfl__wewgx = self.typemap[swt__wnlki[0].name]
        vcp__nnol = self.typemap[swt__wnlki[1].name]
        if hnfl__wewgx.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                swt__wnlki[1]))
        if vcp__nnol.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                swt__wnlki[0]))
        try:
            ksb__tvnv = [equiv_set.get_shape(x) for x in swt__wnlki]
            if None in ksb__tvnv:
                return None
            dfn__axk = sum(ksb__tvnv, ())
            return ArrayAnalysis.AnalyzeResult(shape=dfn__axk)
        except GuardException as rsp__kos:
            return None
    cpy__afr = list(filter(lambda a: self._isarray(a.name), args))
    require(len(cpy__afr) > 0)
    hchi__fnoyr = [x.name for x in cpy__afr]
    npvjk__sdvq = [self.typemap[x.name].ndim for x in cpy__afr]
    sfkm__abti = max(npvjk__sdvq)
    require(sfkm__abti > 0)
    ksb__tvnv = [equiv_set.get_shape(x) for x in cpy__afr]
    if any(a is None for a in ksb__tvnv):
        return ArrayAnalysis.AnalyzeResult(shape=cpy__afr[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, cpy__afr))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, ksb__tvnv,
        hchi__fnoyr)


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
    sqx__qxjon = code_obj.code
    vzh__juy = len(sqx__qxjon.co_freevars)
    ekitj__obm = sqx__qxjon.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        ika__bltky, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        ekitj__obm = [url__mpib.name for url__mpib in ika__bltky]
    ganew__rcd = caller_ir.func_id.func.__globals__
    try:
        ganew__rcd = getattr(code_obj, 'globals', ganew__rcd)
    except KeyError as rsp__kos:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    wwg__owjix = []
    for x in ekitj__obm:
        try:
            ctnd__hrd = caller_ir.get_definition(x)
        except KeyError as rsp__kos:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(ctnd__hrd, (ir.Const, ir.Global, ir.FreeVar)):
            val = ctnd__hrd.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                bsm__eatsw = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                ganew__rcd[bsm__eatsw] = bodo.jit(distributed=False)(val)
                ganew__rcd[bsm__eatsw].is_nested_func = True
                val = bsm__eatsw
            if isinstance(val, CPUDispatcher):
                bsm__eatsw = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                ganew__rcd[bsm__eatsw] = val
                val = bsm__eatsw
            wwg__owjix.append(val)
        elif isinstance(ctnd__hrd, ir.Expr
            ) and ctnd__hrd.op == 'make_function':
            dzvjh__slta = convert_code_obj_to_function(ctnd__hrd, caller_ir)
            bsm__eatsw = ir_utils.mk_unique_var('nested_func').replace('.', '_'
                )
            ganew__rcd[bsm__eatsw] = bodo.jit(distributed=False)(dzvjh__slta)
            ganew__rcd[bsm__eatsw].is_nested_func = True
            wwg__owjix.append(bsm__eatsw)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    ongxg__wqaiq = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in
        enumerate(wwg__owjix)])
    avi__lqbxi = ','.join([('c_%d' % i) for i in range(vzh__juy)])
    hxrwy__ddovy = list(sqx__qxjon.co_varnames)
    otew__vgya = 0
    qvxc__alg = sqx__qxjon.co_argcount
    mhtx__vpo = caller_ir.get_definition(code_obj.defaults)
    if mhtx__vpo is not None:
        if isinstance(mhtx__vpo, tuple):
            d = [caller_ir.get_definition(x).value for x in mhtx__vpo]
            gtx__hlyxy = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in mhtx__vpo.items]
            gtx__hlyxy = tuple(d)
        otew__vgya = len(gtx__hlyxy)
    joa__hytov = qvxc__alg - otew__vgya
    jqise__thclw = ','.join([('%s' % hxrwy__ddovy[i]) for i in range(
        joa__hytov)])
    if otew__vgya:
        ecnci__xcb = [('%s = %s' % (hxrwy__ddovy[i + joa__hytov],
            gtx__hlyxy[i])) for i in range(otew__vgya)]
        jqise__thclw += ', '
        jqise__thclw += ', '.join(ecnci__xcb)
    return _create_function_from_code_obj(sqx__qxjon, ongxg__wqaiq,
        jqise__thclw, avi__lqbxi, ganew__rcd)


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
    for zsq__dfnl, (twyyq__skt, lfwj__irzvr) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % lfwj__irzvr)
            hbkah__kqanr = _pass_registry.get(twyyq__skt).pass_inst
            if isinstance(hbkah__kqanr, CompilerPass):
                self._runPass(zsq__dfnl, hbkah__kqanr, state)
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
                    pipeline_name, lfwj__irzvr)
                dmaaf__ycp = self._patch_error(msg, e)
                raise dmaaf__ycp
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
    kdxa__mlhu = None
    qtk__cdnk = {}

    def lookup(var, already_seen, varonly=True):
        val = qtk__cdnk.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    qgk__vlwv = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        gnog__lsje = stmt.target
        kaits__phjfa = stmt.value
        qtk__cdnk[gnog__lsje.name] = kaits__phjfa
        if isinstance(kaits__phjfa, ir.Var) and kaits__phjfa.name in qtk__cdnk:
            kaits__phjfa = lookup(kaits__phjfa, set())
        if isinstance(kaits__phjfa, ir.Expr):
            wui__rhzo = set(lookup(url__mpib, set(), True).name for
                url__mpib in kaits__phjfa.list_vars())
            if name in wui__rhzo:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(kaits__phjfa)]
                pemt__iqawf = [x for x, wbm__qpd in args if wbm__qpd.name !=
                    name]
                args = [(x, wbm__qpd) for x, wbm__qpd in args if x !=
                    wbm__qpd.name]
                vdpe__laqxh = dict(args)
                if len(pemt__iqawf) == 1:
                    vdpe__laqxh[pemt__iqawf[0]] = ir.Var(gnog__lsje.scope, 
                        name + '#init', gnog__lsje.loc)
                replace_vars_inner(kaits__phjfa, vdpe__laqxh)
                kdxa__mlhu = nodes[i:]
                break
    return kdxa__mlhu


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
        dbpia__dbf = expand_aliases({url__mpib.name for url__mpib in stmt.
            list_vars()}, alias_map, arg_aliases)
        jzd__swlb = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        wjowj__iffd = expand_aliases({url__mpib.name for url__mpib in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        ftqa__fks = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(jzd__swlb & wjowj__iffd | ftqa__fks & dbpia__dbf) == 0:
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
    ynato__ogwdq = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            ynato__ogwdq.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                ynato__ogwdq.update(get_parfor_writes(stmt, func_ir))
    return ynato__ogwdq


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    ynato__ogwdq = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        ynato__ogwdq.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        ynato__ogwdq = {url__mpib.name for url__mpib in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        ynato__ogwdq = {url__mpib.name for url__mpib in stmt.
            get_live_out_vars()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            ynato__ogwdq.update({url__mpib.name for url__mpib in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        lrm__zfni = guard(find_callname, func_ir, stmt.value)
        if lrm__zfni in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'copy_array_element', 'bodo.libs.array_kernels'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext'), (
            'tuple_list_to_array', 'bodo.utils.utils')):
            ynato__ogwdq.add(stmt.value.args[0].name)
        if lrm__zfni == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            ynato__ogwdq.add(stmt.value.args[1].name)
    return ynato__ogwdq


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
        ayc__jzagu = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        rns__zangp = ayc__jzagu.format(self, msg)
        self.args = rns__zangp,
    else:
        ayc__jzagu = _termcolor.errmsg('{0}')
        rns__zangp = ayc__jzagu.format(self)
        self.args = rns__zangp,
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
        for rbjx__buccm in options['distributed']:
            dist_spec[rbjx__buccm] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for rbjx__buccm in options['distributed_block']:
            dist_spec[rbjx__buccm] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    oxk__imm = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, fblk__zuenn in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(fblk__zuenn)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    ifse__fofv = {}
    for zafoh__sosqh in reversed(inspect.getmro(cls)):
        ifse__fofv.update(zafoh__sosqh.__dict__)
    qmb__rgv, dpb__wfei, lqg__uctv, lya__eiba = {}, {}, {}, {}
    for gmm__rih, url__mpib in ifse__fofv.items():
        if isinstance(url__mpib, pytypes.FunctionType):
            qmb__rgv[gmm__rih] = url__mpib
        elif isinstance(url__mpib, property):
            dpb__wfei[gmm__rih] = url__mpib
        elif isinstance(url__mpib, staticmethod):
            lqg__uctv[gmm__rih] = url__mpib
        else:
            lya__eiba[gmm__rih] = url__mpib
    yhdz__ztrqd = (set(qmb__rgv) | set(dpb__wfei) | set(lqg__uctv)) & set(spec)
    if yhdz__ztrqd:
        raise NameError('name shadowing: {0}'.format(', '.join(yhdz__ztrqd)))
    fayk__mfdnh = lya__eiba.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(lya__eiba)
    if lya__eiba:
        msg = 'class members are not yet supported: {0}'
        fjj__ihi = ', '.join(lya__eiba.keys())
        raise TypeError(msg.format(fjj__ihi))
    for gmm__rih, url__mpib in dpb__wfei.items():
        if url__mpib.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(gmm__rih))
    jit_methods = {gmm__rih: bodo.jit(returns_maybe_distributed=oxk__imm)(
        url__mpib) for gmm__rih, url__mpib in qmb__rgv.items()}
    jit_props = {}
    for gmm__rih, url__mpib in dpb__wfei.items():
        gctcj__cmfv = {}
        if url__mpib.fget:
            gctcj__cmfv['get'] = bodo.jit(url__mpib.fget)
        if url__mpib.fset:
            gctcj__cmfv['set'] = bodo.jit(url__mpib.fset)
        jit_props[gmm__rih] = gctcj__cmfv
    jit_static_methods = {gmm__rih: bodo.jit(url__mpib.__func__) for 
        gmm__rih, url__mpib in lqg__uctv.items()}
    paix__yrjl = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    yfzc__ncgm = dict(class_type=paix__yrjl, __doc__=fayk__mfdnh)
    yfzc__ncgm.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), yfzc__ncgm)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, paix__yrjl)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(paix__yrjl, typingctx, targetctx).register()
    as_numba_type.register(cls, paix__yrjl.instance_type)
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
    bep__ylfv = ','.join('{0}:{1}'.format(gmm__rih, url__mpib) for gmm__rih,
        url__mpib in struct.items())
    zgq__tmg = ','.join('{0}:{1}'.format(gmm__rih, url__mpib) for gmm__rih,
        url__mpib in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), bep__ylfv, zgq__tmg)
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
    vpurr__uxc = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if vpurr__uxc is None:
        return
    lnsv__hmhze, txk__hsynu = vpurr__uxc
    for a in itertools.chain(lnsv__hmhze, txk__hsynu.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, lnsv__hmhze, txk__hsynu)
    except ForceLiteralArg as e:
        vhq__kxg = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(vhq__kxg, self.kws)
        zydvx__zlbt = set()
        jlgwn__kwo = set()
        eddgi__bhyt = {}
        for zsq__dfnl in e.requested_args:
            wopvf__ruxh = typeinfer.func_ir.get_definition(folded[zsq__dfnl])
            if isinstance(wopvf__ruxh, ir.Arg):
                zydvx__zlbt.add(wopvf__ruxh.index)
                if wopvf__ruxh.index in e.file_infos:
                    eddgi__bhyt[wopvf__ruxh.index] = e.file_infos[wopvf__ruxh
                        .index]
            else:
                jlgwn__kwo.add(zsq__dfnl)
        if jlgwn__kwo:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif zydvx__zlbt:
            raise ForceLiteralArg(zydvx__zlbt, loc=self.loc, file_infos=
                eddgi__bhyt)
    if sig is None:
        aay__zhonh = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in lnsv__hmhze]
        args += [('%s=%s' % (gmm__rih, url__mpib)) for gmm__rih, url__mpib in
            sorted(txk__hsynu.items())]
        nde__lzf = aay__zhonh.format(fnty, ', '.join(map(str, args)))
        gycu__sbgfc = context.explain_function_type(fnty)
        msg = '\n'.join([nde__lzf, gycu__sbgfc])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        typzw__fkc = context.unify_pairs(sig.recvr, fnty.this)
        if typzw__fkc is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if typzw__fkc is not None and typzw__fkc.is_precise():
            pahil__gyp = fnty.copy(this=typzw__fkc)
            typeinfer.propagate_refined_type(self.func, pahil__gyp)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            jfy__sde = target.getone()
            if context.unify_pairs(jfy__sde, sig.return_type) == jfy__sde:
                sig = sig.replace(return_type=jfy__sde)
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
        wdpxb__etk = '*other* must be a {} but got a {} instead'
        raise TypeError(wdpxb__etk.format(ForceLiteralArg, type(other)))
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
    virc__zpxq = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for gmm__rih, url__mpib in kwargs.items():
        wej__hggtw = None
        try:
            utxg__qhr = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var(
                'dummy'), loc)
            func_ir._definitions[utxg__qhr.name] = [url__mpib]
            wej__hggtw = get_const_value_inner(func_ir, utxg__qhr)
            func_ir._definitions.pop(utxg__qhr.name)
            if isinstance(wej__hggtw, str):
                wej__hggtw = sigutils._parse_signature_string(wej__hggtw)
            if isinstance(wej__hggtw, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {gmm__rih} is annotated as type class {wej__hggtw}."""
                    )
            assert isinstance(wej__hggtw, types.Type)
            if isinstance(wej__hggtw, (types.List, types.Set)):
                wej__hggtw = wej__hggtw.copy(reflected=False)
            virc__zpxq[gmm__rih] = wej__hggtw
        except BodoError as rsp__kos:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(wej__hggtw, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(url__mpib, ir.Global):
                    msg = f'Global {url__mpib.name!r} is not defined.'
                if isinstance(url__mpib, ir.FreeVar):
                    msg = f'Freevar {url__mpib.name!r} is not defined.'
            if isinstance(url__mpib, ir.Expr) and url__mpib.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=gmm__rih, msg=msg, loc=loc)
    for name, typ in virc__zpxq.items():
        self._legalize_arg_type(name, typ, loc)
    return virc__zpxq


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
    zhe__ghlpv = inst.arg
    assert zhe__ghlpv > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(zhe__ghlpv)]))
    tmps = [state.make_temp() for _ in range(zhe__ghlpv - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    fnn__vdf = ir.Global('format', format, loc=self.loc)
    self.store(value=fnn__vdf, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    gdbti__swref = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=gdbti__swref, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    zhe__ghlpv = inst.arg
    assert zhe__ghlpv > 0, 'invalid BUILD_STRING count'
    yezwe__iwffa = self.get(strings[0])
    for other, rre__kdmk in zip(strings[1:], tmps):
        other = self.get(other)
        joog__csr = ir.Expr.binop(operator.add, lhs=yezwe__iwffa, rhs=other,
            loc=self.loc)
        self.store(joog__csr, rre__kdmk)
        yezwe__iwffa = self.get(rre__kdmk)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    wqjro__godnh = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, wqjro__godnh])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    ueq__hwgii = mk_unique_var(f'{var_name}')
    sex__zzh = ueq__hwgii.replace('<', '_').replace('>', '_')
    sex__zzh = sex__zzh.replace('.', '_').replace('$', '_v')
    return sex__zzh


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
                xhhm__zpmf = get_overload_const_str(val2)
                if xhhm__zpmf != 'ns':
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
        qacmr__qsf = states['defmap']
        if len(qacmr__qsf) == 0:
            myzte__xzn = assign.target
            numba.core.ssa._logger.debug('first assign: %s', myzte__xzn)
            if myzte__xzn.name not in scope.localvars:
                myzte__xzn = scope.define(assign.target.name, loc=assign.loc)
        else:
            myzte__xzn = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=myzte__xzn, value=assign.value, loc=
            assign.loc)
        qacmr__qsf[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    oxui__wthz = []
    for gmm__rih, url__mpib in typing.npydecl.registry.globals:
        if gmm__rih == func:
            oxui__wthz.append(url__mpib)
    for gmm__rih, url__mpib in typing.templates.builtin_registry.globals:
        if gmm__rih == func:
            oxui__wthz.append(url__mpib)
    if len(oxui__wthz) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return oxui__wthz


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    fakw__ibuqc = {}
    lnr__xjl = find_topo_order(blocks)
    qtorv__lprsr = {}
    for label in lnr__xjl:
        block = blocks[label]
        rbn__jdy = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                gnog__lsje = stmt.target.name
                kaits__phjfa = stmt.value
                if (kaits__phjfa.op == 'getattr' and kaits__phjfa.attr in
                    arr_math and isinstance(typemap[kaits__phjfa.value.name
                    ], types.npytypes.Array)):
                    kaits__phjfa = stmt.value
                    jzim__bsrdx = kaits__phjfa.value
                    fakw__ibuqc[gnog__lsje] = jzim__bsrdx
                    scope = jzim__bsrdx.scope
                    loc = jzim__bsrdx.loc
                    yplb__cdqc = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[yplb__cdqc.name] = types.misc.Module(numpy)
                    axt__jfxeo = ir.Global('np', numpy, loc)
                    gxc__mih = ir.Assign(axt__jfxeo, yplb__cdqc, loc)
                    kaits__phjfa.value = yplb__cdqc
                    rbn__jdy.append(gxc__mih)
                    func_ir._definitions[yplb__cdqc.name] = [axt__jfxeo]
                    func = getattr(numpy, kaits__phjfa.attr)
                    tcw__yyep = get_np_ufunc_typ_lst(func)
                    qtorv__lprsr[gnog__lsje] = tcw__yyep
                if (kaits__phjfa.op == 'call' and kaits__phjfa.func.name in
                    fakw__ibuqc):
                    jzim__bsrdx = fakw__ibuqc[kaits__phjfa.func.name]
                    atx__zkxy = calltypes.pop(kaits__phjfa)
                    tssex__foqry = atx__zkxy.args[:len(kaits__phjfa.args)]
                    opxk__ztz = {name: typemap[url__mpib.name] for name,
                        url__mpib in kaits__phjfa.kws}
                    szdn__dhb = qtorv__lprsr[kaits__phjfa.func.name]
                    sdwl__jac = None
                    for bcffd__bvvqd in szdn__dhb:
                        try:
                            sdwl__jac = bcffd__bvvqd.get_call_type(typingctx,
                                [typemap[jzim__bsrdx.name]] + list(
                                tssex__foqry), opxk__ztz)
                            typemap.pop(kaits__phjfa.func.name)
                            typemap[kaits__phjfa.func.name] = bcffd__bvvqd
                            calltypes[kaits__phjfa] = sdwl__jac
                            break
                        except Exception as rsp__kos:
                            pass
                    if sdwl__jac is None:
                        raise TypeError(
                            f'No valid template found for {kaits__phjfa.func.name}'
                            )
                    kaits__phjfa.args = [jzim__bsrdx] + kaits__phjfa.args
            rbn__jdy.append(stmt)
        block.body = rbn__jdy


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    zlop__zzjuz = ufunc.nin
    rzc__spnu = ufunc.nout
    joa__hytov = ufunc.nargs
    assert joa__hytov == zlop__zzjuz + rzc__spnu
    if len(args) < zlop__zzjuz:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            zlop__zzjuz))
    if len(args) > joa__hytov:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), joa__hytov)
            )
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    xqpb__rxvu = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    wuy__lov = max(xqpb__rxvu)
    igign__cedx = args[zlop__zzjuz:]
    if not all(d == wuy__lov for d in xqpb__rxvu[zlop__zzjuz:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(haqy__cljr, types.ArrayCompatible) and not
        isinstance(haqy__cljr, types.Bytes) for haqy__cljr in igign__cedx):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(haqy__cljr.mutable for haqy__cljr in igign__cedx):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    nsx__myt = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    xqexr__kqvrf = None
    if wuy__lov > 0 and len(igign__cedx) < ufunc.nout:
        xqexr__kqvrf = 'C'
        vswin__fqahf = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in vswin__fqahf and 'F' in vswin__fqahf:
            xqexr__kqvrf = 'F'
    return nsx__myt, igign__cedx, wuy__lov, xqexr__kqvrf


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
        omcnd__rai = 'Dict.key_type cannot be of type {}'
        raise TypingError(omcnd__rai.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        omcnd__rai = 'Dict.value_type cannot be of type {}'
        raise TypingError(omcnd__rai.format(valty))
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
    kcsza__qakk = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[kcsza__qakk]
        return impl, args
    except KeyError as rsp__kos:
        pass
    impl, args = self._build_impl(kcsza__qakk, args, kws)
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
    tpgm__pej = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            pzov__bmtyv = block.body[-1]
            if isinstance(pzov__bmtyv, ir.Branch):
                if len(blocks[pzov__bmtyv.truebr].body) == 1 and len(blocks
                    [pzov__bmtyv.falsebr].body) == 1:
                    gcm__fdsfh = blocks[pzov__bmtyv.truebr].body[0]
                    hocy__hiv = blocks[pzov__bmtyv.falsebr].body[0]
                    if isinstance(gcm__fdsfh, ir.Jump) and isinstance(hocy__hiv
                        , ir.Jump) and gcm__fdsfh.target == hocy__hiv.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(gcm__fdsfh
                            .target, pzov__bmtyv.loc)
                        tpgm__pej = True
                elif len(blocks[pzov__bmtyv.truebr].body) == 1:
                    gcm__fdsfh = blocks[pzov__bmtyv.truebr].body[0]
                    if isinstance(gcm__fdsfh, ir.Jump
                        ) and gcm__fdsfh.target == pzov__bmtyv.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(gcm__fdsfh
                            .target, pzov__bmtyv.loc)
                        tpgm__pej = True
                elif len(blocks[pzov__bmtyv.falsebr].body) == 1:
                    hocy__hiv = blocks[pzov__bmtyv.falsebr].body[0]
                    if isinstance(hocy__hiv, ir.Jump
                        ) and hocy__hiv.target == pzov__bmtyv.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(hocy__hiv
                            .target, pzov__bmtyv.loc)
                        tpgm__pej = True
    return tpgm__pej


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        sejy__bsgo = find_topo_order(parfor.loop_body)
    lkm__zzcpe = sejy__bsgo[0]
    knfor__xkad = {}
    _update_parfor_get_setitems(parfor.loop_body[lkm__zzcpe].body, parfor.
        index_var, alias_map, knfor__xkad, lives_n_aliases)
    phco__sglw = set(knfor__xkad.keys())
    for eol__dwz in sejy__bsgo:
        if eol__dwz == lkm__zzcpe:
            continue
        for stmt in parfor.loop_body[eol__dwz].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            leris__tqml = set(url__mpib.name for url__mpib in stmt.list_vars())
            row__rut = leris__tqml & phco__sglw
            for a in row__rut:
                knfor__xkad.pop(a, None)
    for eol__dwz in sejy__bsgo:
        if eol__dwz == lkm__zzcpe:
            continue
        block = parfor.loop_body[eol__dwz]
        nvotk__gohh = knfor__xkad.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            nvotk__gohh, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    pdab__aorrr = max(blocks.keys())
    vbf__djn, iepyi__uploa = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    irq__puuau = ir.Jump(vbf__djn, ir.Loc('parfors_dummy', -1))
    blocks[pdab__aorrr].body.append(irq__puuau)
    cph__nhcom = compute_cfg_from_blocks(blocks)
    vtxn__hkmdc = compute_use_defs(blocks)
    hzzcy__zgka = compute_live_map(cph__nhcom, blocks, vtxn__hkmdc.usemap,
        vtxn__hkmdc.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        rbn__jdy = []
        ivb__mkyjf = {url__mpib.name for url__mpib in block.terminator.
            list_vars()}
        for cvfno__gry, ydnx__hsykj in cph__nhcom.successors(label):
            ivb__mkyjf |= hzzcy__zgka[cvfno__gry]
        for stmt in reversed(block.body):
            vuklb__zyys = ivb__mkyjf & alias_set
            for url__mpib in vuklb__zyys:
                ivb__mkyjf |= alias_map[url__mpib]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in ivb__mkyjf and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                lrm__zfni = guard(find_callname, func_ir, stmt.value)
                if lrm__zfni == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in ivb__mkyjf and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            ivb__mkyjf |= {url__mpib.name for url__mpib in stmt.list_vars()}
            rbn__jdy.append(stmt)
        rbn__jdy.reverse()
        block.body = rbn__jdy
    typemap.pop(iepyi__uploa.name)
    blocks[pdab__aorrr].body.pop()
    tpgm__pej = True
    while tpgm__pej:
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
        tpgm__pej = trim_empty_parfor_branches(parfor)
    opm__xidil = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        opm__xidil &= len(block.body) == 0
    if opm__xidil:
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
    wpl__dlb = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                wpl__dlb += 1
                parfor = stmt
                xcyhv__sfcmx = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = xcyhv__sfcmx.scope
                loc = ir.Loc('parfors_dummy', -1)
                rjudc__mima = ir.Var(scope, mk_unique_var('$const'), loc)
                xcyhv__sfcmx.body.append(ir.Assign(ir.Const(0, loc),
                    rjudc__mima, loc))
                xcyhv__sfcmx.body.append(ir.Return(rjudc__mima, loc))
                cph__nhcom = compute_cfg_from_blocks(parfor.loop_body)
                for agyfr__rvc in cph__nhcom.dead_nodes():
                    del parfor.loop_body[agyfr__rvc]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                xcyhv__sfcmx = parfor.loop_body[max(parfor.loop_body.keys())]
                xcyhv__sfcmx.body.pop()
                xcyhv__sfcmx.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return wpl__dlb


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    cph__nhcom = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != cph__nhcom.entry_point()
    tqjn__nwk = list(filter(find_single_branch, blocks.keys()))
    xio__qzuq = set()
    for label in tqjn__nwk:
        inst = blocks[label].body[0]
        ohlyy__ylu = cph__nhcom.predecessors(label)
        oka__ankx = True
        for ulhh__ogbi, wsuxx__xrg in ohlyy__ylu:
            block = blocks[ulhh__ogbi]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                oka__ankx = False
        if oka__ankx:
            xio__qzuq.add(label)
    for label in xio__qzuq:
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
            yaio__azelc = self.overloads.get(tuple(args))
            if yaio__azelc is not None:
                return yaio__azelc.entry_point
            self._pre_compile(args, return_type, flags)
            aszxd__gvkzy = self.func_ir
            gzorx__nvj = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=gzorx__nvj):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=aszxd__gvkzy, args=
                    args, return_type=return_type, flags=flags, locals=self
                    .locals, lifted=(), lifted_from=self.lifted_from,
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
        iedwy__ltyt = copy.deepcopy(flags)
        iedwy__ltyt.no_rewrites = True

        def compile_local(the_ir, the_flags):
            ysweb__rrf = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return ysweb__rrf.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        wtqba__ullrp = compile_local(func_ir, iedwy__ltyt)
        oclbg__lbupa = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    oclbg__lbupa = compile_local(func_ir, flags)
                except Exception as rsp__kos:
                    pass
        if oclbg__lbupa is not None:
            cres = oclbg__lbupa
        else:
            cres = wtqba__ullrp
        return cres
    else:
        ysweb__rrf = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return ysweb__rrf.compile_ir(func_ir=func_ir, lifted=lifted,
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
    hxaq__xlal = self.get_data_type(typ.dtype)
    wsi__wwiq = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        wsi__wwiq):
        nuvap__njnd = ary.ctypes.data
        ccv__eam = self.add_dynamic_addr(builder, nuvap__njnd, info=str(
            type(nuvap__njnd)))
        pfte__epo = self.add_dynamic_addr(builder, id(ary), info=str(type(ary))
            )
        self.global_arrays.append(ary)
    else:
        fcn__qjl = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            fcn__qjl = fcn__qjl.view('int64')
        val = bytearray(fcn__qjl.data)
        bpux__lnt = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        ccv__eam = cgutils.global_constant(builder, '.const.array.data',
            bpux__lnt)
        ccv__eam.align = self.get_abi_alignment(hxaq__xlal)
        pfte__epo = None
    ntzg__myw = self.get_value_type(types.intp)
    age__mce = [self.get_constant(types.intp, tdikw__hqzat) for
        tdikw__hqzat in ary.shape]
    bigm__nuudi = lir.Constant(lir.ArrayType(ntzg__myw, len(age__mce)),
        age__mce)
    khm__eru = [self.get_constant(types.intp, tdikw__hqzat) for
        tdikw__hqzat in ary.strides]
    inmuy__dowfj = lir.Constant(lir.ArrayType(ntzg__myw, len(khm__eru)),
        khm__eru)
    sutzn__suxwa = self.get_constant(types.intp, ary.dtype.itemsize)
    aka__letwr = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        aka__letwr, sutzn__suxwa, ccv__eam.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), bigm__nuudi, inmuy__dowfj])


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
    vosa__iffh = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    hzlb__eyz = lir.Function(module, vosa__iffh, name='nrt_atomic_{0}'.
        format(op))
    [jeyxd__vhwiy] = hzlb__eyz.args
    uppd__fzawa = hzlb__eyz.append_basic_block()
    builder = lir.IRBuilder(uppd__fzawa)
    tjwo__vyvji = lir.Constant(_word_type, 1)
    if False:
        oyr__fibu = builder.atomic_rmw(op, jeyxd__vhwiy, tjwo__vyvji,
            ordering=ordering)
        res = getattr(builder, op)(oyr__fibu, tjwo__vyvji)
        builder.ret(res)
    else:
        oyr__fibu = builder.load(jeyxd__vhwiy)
        libfd__sqseu = getattr(builder, op)(oyr__fibu, tjwo__vyvji)
        udz__czylq = builder.icmp_signed('!=', oyr__fibu, lir.Constant(
            oyr__fibu.type, -1))
        with cgutils.if_likely(builder, udz__czylq):
            builder.store(libfd__sqseu, jeyxd__vhwiy)
        builder.ret(libfd__sqseu)
    return hzlb__eyz


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
        bdzj__zfst = state.targetctx.codegen()
        state.library = bdzj__zfst.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    sfjo__tzgja = state.func_ir
    typemap = state.typemap
    yxo__lzv = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    qltad__huui = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            sfjo__tzgja, typemap, yxo__lzv, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            lkn__zhtj = lowering.Lower(targetctx, library, fndesc,
                sfjo__tzgja, metadata=metadata)
            lkn__zhtj.lower()
            if not flags.no_cpython_wrapper:
                lkn__zhtj.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(yxo__lzv, (types.Optional, types.Generator)):
                        pass
                    else:
                        lkn__zhtj.create_cfunc_wrapper()
            env = lkn__zhtj.env
            pjv__amr = lkn__zhtj.call_helper
            del lkn__zhtj
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, pjv__amr, cfunc=None, env=env)
        else:
            syqf__vktmm = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(syqf__vktmm, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, pjv__amr, cfunc=syqf__vktmm,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        uyche__zrx = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = uyche__zrx - qltad__huui
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
        xyrt__puf = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, xyrt__puf),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            egph__quj.do_break()
        elm__ryxcm = c.builder.icmp_signed('!=', xyrt__puf, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(elm__ryxcm, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, xyrt__puf)
                c.pyapi.decref(xyrt__puf)
                egph__quj.do_break()
        c.pyapi.decref(xyrt__puf)
    xpkf__yewrs, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(xpkf__yewrs, likely=True) as (osa__ljpks,
        cwhtz__swknd):
        with osa__ljpks:
            list.size = size
            xibk__adk = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                xibk__adk), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        xibk__adk))
                    with cgutils.for_range(c.builder, size) as egph__quj:
                        itemobj = c.pyapi.list_getitem(obj, egph__quj.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        sqnfo__ahj = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(sqnfo__ahj.is_error, likely=
                            False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            egph__quj.do_break()
                        list.setitem(egph__quj.index, sqnfo__ahj.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with cwhtz__swknd:
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
    ewrpd__tnppj, ywr__mzzwy, eqh__ymko, stk__hrx, lgzlg__yhs = (
        compile_time_get_string_data(literal_string))
    kjste__tbzff = builder.module
    gv = context.insert_const_bytes(kjste__tbzff, ewrpd__tnppj)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        ywr__mzzwy), context.get_constant(types.int32, eqh__ymko), context.
        get_constant(types.uint32, stk__hrx), context.get_constant(
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
    rdo__qxxw = None
    if isinstance(shape, types.Integer):
        rdo__qxxw = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(tdikw__hqzat, (types.Integer, types.IntEnumMember
            )) for tdikw__hqzat in shape):
            rdo__qxxw = len(shape)
    return rdo__qxxw


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
            rdo__qxxw = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if rdo__qxxw == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(rdo__qxxw))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            hchi__fnoyr = self._get_names(x)
            if len(hchi__fnoyr) != 0:
                return hchi__fnoyr[0]
            return hchi__fnoyr
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    hchi__fnoyr = self._get_names(obj)
    if len(hchi__fnoyr) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(hchi__fnoyr[0])


def get_equiv_set(self, obj):
    hchi__fnoyr = self._get_names(obj)
    if len(hchi__fnoyr) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(hchi__fnoyr[0])


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
    yekic__ivgky = []
    for wegz__zba in func_ir.arg_names:
        if wegz__zba in typemap and isinstance(typemap[wegz__zba], types.
            containers.UniTuple) and typemap[wegz__zba].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(wegz__zba))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for fgd__szhg in func_ir.blocks.values():
        for stmt in fgd__szhg.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    rhxy__pxa = getattr(val, 'code', None)
                    if rhxy__pxa is not None:
                        if getattr(val, 'closure', None) is not None:
                            wli__hfxp = '<creating a function from a closure>'
                            joog__csr = ''
                        else:
                            wli__hfxp = rhxy__pxa.co_name
                            joog__csr = '(%s) ' % wli__hfxp
                    else:
                        wli__hfxp = '<could not ascertain use case>'
                        joog__csr = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (wli__hfxp, joog__csr))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                rjwtz__sdd = False
                if isinstance(val, pytypes.FunctionType):
                    rjwtz__sdd = val in {numba.gdb, numba.gdb_init}
                if not rjwtz__sdd:
                    rjwtz__sdd = getattr(val, '_name', '') == 'gdb_internal'
                if rjwtz__sdd:
                    yekic__ivgky.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    pmdrp__dpw = func_ir.get_definition(var)
                    xjecf__eevpq = guard(find_callname, func_ir, pmdrp__dpw)
                    if xjecf__eevpq and xjecf__eevpq[1] == 'numpy':
                        ty = getattr(numpy, xjecf__eevpq[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    xpa__whwh = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(xpa__whwh), loc=stmt.loc)
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
    if len(yekic__ivgky) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        nkibw__ppdhp = '\n'.join([x.strformat() for x in yekic__ivgky])
        raise errors.UnsupportedError(msg % nkibw__ppdhp)


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
    gmm__rih, url__mpib = next(iter(val.items()))
    wio__wjdxk = typeof_impl(gmm__rih, c)
    szczb__rfy = typeof_impl(url__mpib, c)
    if wio__wjdxk is None or szczb__rfy is None:
        raise ValueError(
            f'Cannot type dict element type {type(gmm__rih)}, {type(url__mpib)}'
            )
    return types.DictType(wio__wjdxk, szczb__rfy)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    fvhu__pvk = cgutils.alloca_once_value(c.builder, val)
    eptw__khu = c.pyapi.object_hasattr_string(val, '_opaque')
    zrht__xsz = c.builder.icmp_unsigned('==', eptw__khu, lir.Constant(
        eptw__khu.type, 0))
    qmzvd__vbm = typ.key_type
    mqgfx__xtm = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(qmzvd__vbm, mqgfx__xtm)

    def copy_dict(out_dict, in_dict):
        for gmm__rih, url__mpib in in_dict.items():
            out_dict[gmm__rih] = url__mpib
    with c.builder.if_then(zrht__xsz):
        fdv__tah = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        hdml__dfuzq = c.pyapi.call_function_objargs(fdv__tah, [])
        yiv__fwzu = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(yiv__fwzu, [hdml__dfuzq, val])
        c.builder.store(hdml__dfuzq, fvhu__pvk)
    val = c.builder.load(fvhu__pvk)
    tael__holst = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    hclhx__uwai = c.pyapi.object_type(val)
    ibxf__mmhd = c.builder.icmp_unsigned('==', hclhx__uwai, tael__holst)
    with c.builder.if_else(ibxf__mmhd) as (mzto__xpnv, isisl__etphf):
        with mzto__xpnv:
            tpp__wbgpi = c.pyapi.object_getattr_string(val, '_opaque')
            glj__glfgb = types.MemInfoPointer(types.voidptr)
            sqnfo__ahj = c.unbox(glj__glfgb, tpp__wbgpi)
            mi = sqnfo__ahj.value
            frv__kolv = glj__glfgb, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *frv__kolv)
            xlz__kbk = context.get_constant_null(frv__kolv[1])
            args = mi, xlz__kbk
            fnzrc__shfud, gox__royf = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, gox__royf)
            c.pyapi.decref(tpp__wbgpi)
            wqwz__kecq = c.builder.basic_block
        with isisl__etphf:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", hclhx__uwai, tael__holst)
            jccf__pqp = c.builder.basic_block
    vtxdy__nzk = c.builder.phi(gox__royf.type)
    bhiz__cdqcm = c.builder.phi(fnzrc__shfud.type)
    vtxdy__nzk.add_incoming(gox__royf, wqwz__kecq)
    vtxdy__nzk.add_incoming(gox__royf.type(None), jccf__pqp)
    bhiz__cdqcm.add_incoming(fnzrc__shfud, wqwz__kecq)
    bhiz__cdqcm.add_incoming(cgutils.true_bit, jccf__pqp)
    c.pyapi.decref(tael__holst)
    c.pyapi.decref(hclhx__uwai)
    with c.builder.if_then(zrht__xsz):
        c.pyapi.decref(val)
    return NativeValue(vtxdy__nzk, is_error=bhiz__cdqcm)


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
    chae__uufyq = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=chae__uufyq, name=updatevar)
    vawq__uzbo = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=vawq__uzbo, name=res)


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
        for gmm__rih, url__mpib in other.items():
            d[gmm__rih] = url__mpib
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
    joog__csr = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(joog__csr, res)


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
    jxd__dxnq = PassManager(name)
    if state.func_ir is None:
        jxd__dxnq.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            jxd__dxnq.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        jxd__dxnq.add_pass(FixupArgs, 'fix up args')
    jxd__dxnq.add_pass(IRProcessing, 'processing IR')
    jxd__dxnq.add_pass(WithLifting, 'Handle with contexts')
    jxd__dxnq.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        jxd__dxnq.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        jxd__dxnq.add_pass(DeadBranchPrune, 'dead branch pruning')
        jxd__dxnq.add_pass(GenericRewrites, 'nopython rewrites')
    jxd__dxnq.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    jxd__dxnq.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        jxd__dxnq.add_pass(DeadBranchPrune, 'dead branch pruning')
    jxd__dxnq.add_pass(FindLiterallyCalls, 'find literally calls')
    jxd__dxnq.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        jxd__dxnq.add_pass(ReconstructSSA, 'ssa')
    jxd__dxnq.add_pass(LiteralPropagationSubPipelinePass, 'Literal propagation'
        )
    jxd__dxnq.finalize()
    return jxd__dxnq


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
    a, kzv__fxriw = args
    if isinstance(a, types.List) and isinstance(kzv__fxriw, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(kzv__fxriw, types.List):
        return signature(kzv__fxriw, types.intp, kzv__fxriw)


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
        idlo__dpyor, iqs__tdpm = 0, 1
    else:
        idlo__dpyor, iqs__tdpm = 1, 0
    joc__dzla = ListInstance(context, builder, sig.args[idlo__dpyor], args[
        idlo__dpyor])
    yxxv__yxqg = joc__dzla.size
    kwmm__vksil = args[iqs__tdpm]
    xibk__adk = lir.Constant(kwmm__vksil.type, 0)
    kwmm__vksil = builder.select(cgutils.is_neg_int(builder, kwmm__vksil),
        xibk__adk, kwmm__vksil)
    aka__letwr = builder.mul(kwmm__vksil, yxxv__yxqg)
    oerr__xky = ListInstance.allocate(context, builder, sig.return_type,
        aka__letwr)
    oerr__xky.size = aka__letwr
    with cgutils.for_range_slice(builder, xibk__adk, aka__letwr, yxxv__yxqg,
        inc=True) as (lwz__uoh, _):
        with cgutils.for_range(builder, yxxv__yxqg) as egph__quj:
            value = joc__dzla.getitem(egph__quj.index)
            oerr__xky.setitem(builder.add(egph__quj.index, lwz__uoh), value,
                incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, oerr__xky.value)


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
    uwolk__ykjls = first.unify(self, second)
    if uwolk__ykjls is not None:
        return uwolk__ykjls
    uwolk__ykjls = second.unify(self, first)
    if uwolk__ykjls is not None:
        return uwolk__ykjls
    hnhpz__bpph = self.can_convert(fromty=first, toty=second)
    if hnhpz__bpph is not None and hnhpz__bpph <= Conversion.safe:
        return second
    hnhpz__bpph = self.can_convert(fromty=second, toty=first)
    if hnhpz__bpph is not None and hnhpz__bpph <= Conversion.safe:
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
    aka__letwr = payload.used
    listobj = c.pyapi.list_new(aka__letwr)
    xpkf__yewrs = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(xpkf__yewrs, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(aka__letwr
            .type, 0))
        with payload._iterate() as egph__quj:
            i = c.builder.load(index)
            item = egph__quj.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return xpkf__yewrs, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    yutak__hwfa = h.type
    rsqe__dkort = self.mask
    dtype = self._ty.dtype
    dhmlk__fxn = context.typing_context
    fnty = dhmlk__fxn.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(dhmlk__fxn, (dtype, dtype), {})
    cqnpz__vacnf = context.get_function(fnty, sig)
    qppo__usc = ir.Constant(yutak__hwfa, 1)
    ncocw__lcgrq = ir.Constant(yutak__hwfa, 5)
    pna__esq = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, rsqe__dkort))
    if for_insert:
        dwrmo__opwi = rsqe__dkort.type(-1)
        hxul__ijg = cgutils.alloca_once_value(builder, dwrmo__opwi)
    qlx__eeai = builder.append_basic_block('lookup.body')
    udcj__vwh = builder.append_basic_block('lookup.found')
    ztkp__uqfc = builder.append_basic_block('lookup.not_found')
    rgzn__auwa = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        hha__vskea = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, hha__vskea)):
            iebw__vmu = cqnpz__vacnf(builder, (item, entry.key))
            with builder.if_then(iebw__vmu):
                builder.branch(udcj__vwh)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, hha__vskea)):
            builder.branch(ztkp__uqfc)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, hha__vskea)):
                ptmjx__pyx = builder.load(hxul__ijg)
                ptmjx__pyx = builder.select(builder.icmp_unsigned('==',
                    ptmjx__pyx, dwrmo__opwi), i, ptmjx__pyx)
                builder.store(ptmjx__pyx, hxul__ijg)
    with cgutils.for_range(builder, ir.Constant(yutak__hwfa, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, qppo__usc)
        i = builder.and_(i, rsqe__dkort)
        builder.store(i, index)
    builder.branch(qlx__eeai)
    with builder.goto_block(qlx__eeai):
        i = builder.load(index)
        check_entry(i)
        ulhh__ogbi = builder.load(pna__esq)
        ulhh__ogbi = builder.lshr(ulhh__ogbi, ncocw__lcgrq)
        i = builder.add(qppo__usc, builder.mul(i, ncocw__lcgrq))
        i = builder.and_(rsqe__dkort, builder.add(i, ulhh__ogbi))
        builder.store(i, index)
        builder.store(ulhh__ogbi, pna__esq)
        builder.branch(qlx__eeai)
    with builder.goto_block(ztkp__uqfc):
        if for_insert:
            i = builder.load(index)
            ptmjx__pyx = builder.load(hxul__ijg)
            i = builder.select(builder.icmp_unsigned('==', ptmjx__pyx,
                dwrmo__opwi), i, ptmjx__pyx)
            builder.store(i, index)
        builder.branch(rgzn__auwa)
    with builder.goto_block(udcj__vwh):
        builder.branch(rgzn__auwa)
    builder.position_at_end(rgzn__auwa)
    rjwtz__sdd = builder.phi(ir.IntType(1), 'found')
    rjwtz__sdd.add_incoming(cgutils.true_bit, udcj__vwh)
    rjwtz__sdd.add_incoming(cgutils.false_bit, ztkp__uqfc)
    return rjwtz__sdd, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    erzix__pzki = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    gfmx__cyu = payload.used
    qppo__usc = ir.Constant(gfmx__cyu.type, 1)
    gfmx__cyu = payload.used = builder.add(gfmx__cyu, qppo__usc)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, erzix__pzki), likely=True):
        payload.fill = builder.add(payload.fill, qppo__usc)
    if do_resize:
        self.upsize(gfmx__cyu)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    rjwtz__sdd, i = payload._lookup(item, h, for_insert=True)
    sgco__wbt = builder.not_(rjwtz__sdd)
    with builder.if_then(sgco__wbt):
        entry = payload.get_entry(i)
        erzix__pzki = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        gfmx__cyu = payload.used
        qppo__usc = ir.Constant(gfmx__cyu.type, 1)
        gfmx__cyu = payload.used = builder.add(gfmx__cyu, qppo__usc)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, erzix__pzki), likely=True):
            payload.fill = builder.add(payload.fill, qppo__usc)
        if do_resize:
            self.upsize(gfmx__cyu)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    gfmx__cyu = payload.used
    qppo__usc = ir.Constant(gfmx__cyu.type, 1)
    gfmx__cyu = payload.used = self._builder.sub(gfmx__cyu, qppo__usc)
    if do_resize:
        self.downsize(gfmx__cyu)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    jlizw__frax = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, jlizw__frax)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    bzx__lsvk = payload
    xpkf__yewrs = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(xpkf__yewrs), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with bzx__lsvk._iterate() as egph__quj:
        entry = egph__quj.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(bzx__lsvk.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as egph__quj:
        entry = egph__quj.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    xpkf__yewrs = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(xpkf__yewrs), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    xpkf__yewrs = cgutils.alloca_once_value(builder, cgutils.true_bit)
    yutak__hwfa = context.get_value_type(types.intp)
    xibk__adk = ir.Constant(yutak__hwfa, 0)
    qppo__usc = ir.Constant(yutak__hwfa, 1)
    auec__xdcp = context.get_data_type(types.SetPayload(self._ty))
    vvsvg__cpsxj = context.get_abi_sizeof(auec__xdcp)
    fabk__irdq = self._entrysize
    vvsvg__cpsxj -= fabk__irdq
    jzofe__nlx, vyt__qjfq = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(yutak__hwfa, fabk__irdq), ir.Constant(yutak__hwfa,
        vvsvg__cpsxj))
    with builder.if_then(vyt__qjfq, likely=False):
        builder.store(cgutils.false_bit, xpkf__yewrs)
    with builder.if_then(builder.load(xpkf__yewrs), likely=True):
        if realloc:
            cyv__vnuif = self._set.meminfo
            jeyxd__vhwiy = context.nrt.meminfo_varsize_alloc(builder,
                cyv__vnuif, size=jzofe__nlx)
            qupc__feo = cgutils.is_null(builder, jeyxd__vhwiy)
        else:
            wmy__cbqf = _imp_dtor(context, builder.module, self._ty)
            cyv__vnuif = context.nrt.meminfo_new_varsize_dtor(builder,
                jzofe__nlx, builder.bitcast(wmy__cbqf, cgutils.voidptr_t))
            qupc__feo = cgutils.is_null(builder, cyv__vnuif)
        with builder.if_else(qupc__feo, likely=False) as (ixu__smr, osa__ljpks
            ):
            with ixu__smr:
                builder.store(cgutils.false_bit, xpkf__yewrs)
            with osa__ljpks:
                if not realloc:
                    self._set.meminfo = cyv__vnuif
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, jzofe__nlx, 255)
                payload.used = xibk__adk
                payload.fill = xibk__adk
                payload.finger = xibk__adk
                cazw__njk = builder.sub(nentries, qppo__usc)
                payload.mask = cazw__njk
    return builder.load(xpkf__yewrs)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    xpkf__yewrs = cgutils.alloca_once_value(builder, cgutils.true_bit)
    yutak__hwfa = context.get_value_type(types.intp)
    xibk__adk = ir.Constant(yutak__hwfa, 0)
    qppo__usc = ir.Constant(yutak__hwfa, 1)
    auec__xdcp = context.get_data_type(types.SetPayload(self._ty))
    vvsvg__cpsxj = context.get_abi_sizeof(auec__xdcp)
    fabk__irdq = self._entrysize
    vvsvg__cpsxj -= fabk__irdq
    rsqe__dkort = src_payload.mask
    nentries = builder.add(qppo__usc, rsqe__dkort)
    jzofe__nlx = builder.add(ir.Constant(yutak__hwfa, vvsvg__cpsxj),
        builder.mul(ir.Constant(yutak__hwfa, fabk__irdq), nentries))
    with builder.if_then(builder.load(xpkf__yewrs), likely=True):
        wmy__cbqf = _imp_dtor(context, builder.module, self._ty)
        cyv__vnuif = context.nrt.meminfo_new_varsize_dtor(builder,
            jzofe__nlx, builder.bitcast(wmy__cbqf, cgutils.voidptr_t))
        qupc__feo = cgutils.is_null(builder, cyv__vnuif)
        with builder.if_else(qupc__feo, likely=False) as (ixu__smr, osa__ljpks
            ):
            with ixu__smr:
                builder.store(cgutils.false_bit, xpkf__yewrs)
            with osa__ljpks:
                self._set.meminfo = cyv__vnuif
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = xibk__adk
                payload.mask = rsqe__dkort
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, fabk__irdq)
                with src_payload._iterate() as egph__quj:
                    context.nrt.incref(builder, self._ty.dtype, egph__quj.
                        entry.key)
    return builder.load(xpkf__yewrs)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    qmu__hrsb = context.get_value_type(types.voidptr)
    hirod__bdt = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [qmu__hrsb, hirod__bdt, qmu__hrsb])
    jwkw__dvm = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=jwkw__dvm)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        ktg__amu = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, ktg__amu)
        with payload._iterate() as egph__quj:
            entry = egph__quj.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    mke__zyi, = sig.args
    ika__bltky, = args
    otaa__gvlwm = numba.core.imputils.call_len(context, builder, mke__zyi,
        ika__bltky)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, otaa__gvlwm)
    with numba.core.imputils.for_iter(context, builder, mke__zyi, ika__bltky
        ) as egph__quj:
        inst.add(egph__quj.value)
        context.nrt.decref(builder, set_type.dtype, egph__quj.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    mke__zyi = sig.args[1]
    ika__bltky = args[1]
    otaa__gvlwm = numba.core.imputils.call_len(context, builder, mke__zyi,
        ika__bltky)
    if otaa__gvlwm is not None:
        pzjm__yie = builder.add(inst.payload.used, otaa__gvlwm)
        inst.upsize(pzjm__yie)
    with numba.core.imputils.for_iter(context, builder, mke__zyi, ika__bltky
        ) as egph__quj:
        cji__tauo = context.cast(builder, egph__quj.value, mke__zyi.dtype,
            inst.dtype)
        inst.add(cji__tauo)
        context.nrt.decref(builder, mke__zyi.dtype, egph__quj.value)
    if otaa__gvlwm is not None:
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
    egv__gsa = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, egv__gsa, self.reload_init, tuple
        (referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    syqf__vktmm = target_context.get_executable(library, fndesc, env)
    rmt__sfmly = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=syqf__vktmm, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return rmt__sfmly


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
        fvd__lbkby = MPI.COMM_WORLD
        if fvd__lbkby.Get_rank() == 0:
            clh__awve = self.get_cache_path()
            os.makedirs(clh__awve, exist_ok=True)
            tempfile.TemporaryFile(dir=clh__awve).close()
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
    akoln__whpq = cgutils.create_struct_proxy(charseq.bytes_type)
    zowp__xqo = akoln__whpq(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(zowp__xqo.nitems.type, nbytes)
    zowp__xqo.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    zowp__xqo.nitems = nbytes
    zowp__xqo.itemsize = ir.Constant(zowp__xqo.itemsize.type, 1)
    zowp__xqo.data = context.nrt.meminfo_data(builder, zowp__xqo.meminfo)
    zowp__xqo.parent = cgutils.get_null_value(zowp__xqo.parent.type)
    zowp__xqo.shape = cgutils.pack_array(builder, [zowp__xqo.nitems],
        context.get_value_type(types.intp))
    zowp__xqo.strides = cgutils.pack_array(builder, [ir.Constant(zowp__xqo.
        strides.type.element, 1)], context.get_value_type(types.intp))
    return zowp__xqo


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
