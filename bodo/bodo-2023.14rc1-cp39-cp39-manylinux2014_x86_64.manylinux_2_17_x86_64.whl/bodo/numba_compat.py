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
    envd__aub = numba.core.bytecode.FunctionIdentity.from_function(func)
    sqp__uiz = numba.core.interpreter.Interpreter(envd__aub)
    zhf__bfh = numba.core.bytecode.ByteCode(func_id=envd__aub)
    func_ir = sqp__uiz.interpret(zhf__bfh)
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
        bxk__bdzq = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        bxk__bdzq.run()
    bstu__bkiv = numba.core.postproc.PostProcessor(func_ir)
    bstu__bkiv.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, ekhlb__cxa in visit_vars_extensions.items():
        if isinstance(stmt, t):
            ekhlb__cxa(stmt, callback, cbdata)
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
    xjvyn__fkgc = ['ravel', 'transpose', 'reshape']
    for jleqt__rudow in blocks.values():
        for spw__wer in jleqt__rudow.body:
            if type(spw__wer) in alias_analysis_extensions:
                ekhlb__cxa = alias_analysis_extensions[type(spw__wer)]
                ekhlb__cxa(spw__wer, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(spw__wer, ir.Assign):
                rhvg__iuepj = spw__wer.value
                yovcq__flgei = spw__wer.target.name
                if is_immutable_type(yovcq__flgei, typemap):
                    continue
                if isinstance(rhvg__iuepj, ir.Var
                    ) and yovcq__flgei != rhvg__iuepj.name:
                    _add_alias(yovcq__flgei, rhvg__iuepj.name, alias_map,
                        arg_aliases)
                if isinstance(rhvg__iuepj, ir.Expr) and (rhvg__iuepj.op ==
                    'cast' or rhvg__iuepj.op in ['getitem', 'static_getitem']):
                    _add_alias(yovcq__flgei, rhvg__iuepj.value.name,
                        alias_map, arg_aliases)
                if isinstance(rhvg__iuepj, ir.Expr
                    ) and rhvg__iuepj.op == 'inplace_binop':
                    _add_alias(yovcq__flgei, rhvg__iuepj.lhs.name,
                        alias_map, arg_aliases)
                if isinstance(rhvg__iuepj, ir.Expr
                    ) and rhvg__iuepj.op == 'getattr' and rhvg__iuepj.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(yovcq__flgei, rhvg__iuepj.value.name,
                        alias_map, arg_aliases)
                if isinstance(rhvg__iuepj, ir.Expr
                    ) and rhvg__iuepj.op == 'getattr' and rhvg__iuepj.attr not in [
                    'shape'] and rhvg__iuepj.value.name in arg_aliases:
                    _add_alias(yovcq__flgei, rhvg__iuepj.value.name,
                        alias_map, arg_aliases)
                if isinstance(rhvg__iuepj, ir.Expr
                    ) and rhvg__iuepj.op == 'getattr' and rhvg__iuepj.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(yovcq__flgei, rhvg__iuepj.value.name,
                        alias_map, arg_aliases)
                if isinstance(rhvg__iuepj, ir.Expr) and rhvg__iuepj.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(yovcq__flgei, typemap):
                    for kmw__evkcu in rhvg__iuepj.items:
                        _add_alias(yovcq__flgei, kmw__evkcu.name, alias_map,
                            arg_aliases)
                if isinstance(rhvg__iuepj, ir.Expr
                    ) and rhvg__iuepj.op == 'call':
                    onf__swyw = guard(find_callname, func_ir, rhvg__iuepj,
                        typemap)
                    if onf__swyw is None:
                        continue
                    urtab__mqpdo, xezm__hpueq = onf__swyw
                    if onf__swyw in alias_func_extensions:
                        eqn__eaiz = alias_func_extensions[onf__swyw]
                        eqn__eaiz(yovcq__flgei, rhvg__iuepj.args, alias_map,
                            arg_aliases)
                    if xezm__hpueq == 'numpy' and urtab__mqpdo in xjvyn__fkgc:
                        _add_alias(yovcq__flgei, rhvg__iuepj.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(xezm__hpueq, ir.Var
                        ) and urtab__mqpdo in xjvyn__fkgc:
                        _add_alias(yovcq__flgei, xezm__hpueq.name,
                            alias_map, arg_aliases)
    gho__nor = copy.deepcopy(alias_map)
    for kmw__evkcu in gho__nor:
        for kxo__ybttx in gho__nor[kmw__evkcu]:
            alias_map[kmw__evkcu] |= alias_map[kxo__ybttx]
        for kxo__ybttx in gho__nor[kmw__evkcu]:
            alias_map[kxo__ybttx] = alias_map[kmw__evkcu]
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
    upp__inc = compute_cfg_from_blocks(func_ir.blocks)
    ocj__ewef = compute_use_defs(func_ir.blocks)
    tybl__wsds = compute_live_map(upp__inc, func_ir.blocks, ocj__ewef.
        usemap, ocj__ewef.defmap)
    jqrgq__ctqtx = True
    while jqrgq__ctqtx:
        jqrgq__ctqtx = False
        for label, block in func_ir.blocks.items():
            lives = {kmw__evkcu.name for kmw__evkcu in block.terminator.
                list_vars()}
            for paop__axeo, bewqo__lkh in upp__inc.successors(label):
                lives |= tybl__wsds[paop__axeo]
            kloet__inj = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    yovcq__flgei = stmt.target
                    fniy__pgevk = stmt.value
                    if yovcq__flgei.name not in lives:
                        if isinstance(fniy__pgevk, ir.Expr
                            ) and fniy__pgevk.op == 'make_function':
                            continue
                        if isinstance(fniy__pgevk, ir.Expr
                            ) and fniy__pgevk.op == 'getattr':
                            continue
                        if isinstance(fniy__pgevk, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(yovcq__flgei,
                            None), types.Function):
                            continue
                        if isinstance(fniy__pgevk, ir.Expr
                            ) and fniy__pgevk.op == 'build_map':
                            continue
                        if isinstance(fniy__pgevk, ir.Expr
                            ) and fniy__pgevk.op == 'build_tuple':
                            continue
                        if isinstance(fniy__pgevk, ir.Expr
                            ) and fniy__pgevk.op == 'binop':
                            continue
                        if isinstance(fniy__pgevk, ir.Expr
                            ) and fniy__pgevk.op == 'unary':
                            continue
                        if isinstance(fniy__pgevk, ir.Expr
                            ) and fniy__pgevk.op in ('static_getitem',
                            'getitem'):
                            continue
                    if isinstance(fniy__pgevk, ir.Var
                        ) and yovcq__flgei.name == fniy__pgevk.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    elvj__cthun = analysis.ir_extension_usedefs[type(stmt)]
                    pcbfj__twzgn, nwed__sklgq = elvj__cthun(stmt)
                    lives -= nwed__sklgq
                    lives |= pcbfj__twzgn
                else:
                    lives |= {kmw__evkcu.name for kmw__evkcu in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        syxo__udj = set()
                        if isinstance(fniy__pgevk, ir.Expr):
                            syxo__udj = {kmw__evkcu.name for kmw__evkcu in
                                fniy__pgevk.list_vars()}
                        if yovcq__flgei.name not in syxo__udj:
                            lives.remove(yovcq__flgei.name)
                kloet__inj.append(stmt)
            kloet__inj.reverse()
            if len(block.body) != len(kloet__inj):
                jqrgq__ctqtx = True
            block.body = kloet__inj


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    nra__xvm = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (nra__xvm,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    ngpv__csq = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), ngpv__csq)


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
            for oof__qmsm in fnty.templates:
                self._inline_overloads.update(oof__qmsm._inline_overloads)
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
    ngpv__csq = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), ngpv__csq)
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
    qkwh__bslft, kfbbr__frwkm = self._get_impl(args, kws)
    if qkwh__bslft is None:
        return
    dvxn__siar = types.Dispatcher(qkwh__bslft)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        hbzcp__syuhi = qkwh__bslft._compiler
        flags = compiler.Flags()
        gqv__ncfe = hbzcp__syuhi.targetdescr.typing_context
        dywm__gyoqb = hbzcp__syuhi.targetdescr.target_context
        jvw__nqfc = hbzcp__syuhi.pipeline_class(gqv__ncfe, dywm__gyoqb,
            None, None, None, flags, None)
        xxmh__bekw = InlineWorker(gqv__ncfe, dywm__gyoqb, hbzcp__syuhi.
            locals, jvw__nqfc, flags, None)
        qlpig__jjuk = dvxn__siar.dispatcher.get_call_template
        oof__qmsm, scph__gdvb, hrdhp__sjuaa, kws = qlpig__jjuk(kfbbr__frwkm,
            kws)
        if hrdhp__sjuaa in self._inline_overloads:
            return self._inline_overloads[hrdhp__sjuaa]['iinfo'].signature
        ir = xxmh__bekw.run_untyped_passes(dvxn__siar.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, dywm__gyoqb, ir, hrdhp__sjuaa, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, hrdhp__sjuaa, None)
        self._inline_overloads[sig.args] = {'folded_args': hrdhp__sjuaa}
        mkssr__dhgg = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = mkssr__dhgg
        if not self._inline.is_always_inline:
            sig = dvxn__siar.get_call_type(self.context, kfbbr__frwkm, kws)
            self._compiled_overloads[sig.args] = dvxn__siar.get_overload(sig)
        brz__bqbzm = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': hrdhp__sjuaa,
            'iinfo': brz__bqbzm}
    else:
        sig = dvxn__siar.get_call_type(self.context, kfbbr__frwkm, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = dvxn__siar.get_overload(sig)
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
    trryk__jkb = [True, False]
    jgzuh__cwep = [False, True]
    bopxs__pge = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    kbt__boelp = get_local_target(context)
    aww__eec = utils.order_by_target_specificity(kbt__boelp, self.templates,
        fnkey=self.key[0])
    self._depth += 1
    for vvc__lpb in aww__eec:
        rlfe__xkl = vvc__lpb(context)
        tks__xiu = trryk__jkb if rlfe__xkl.prefer_literal else jgzuh__cwep
        tks__xiu = [True] if getattr(rlfe__xkl, '_no_unliteral', False
            ) else tks__xiu
        for thybv__gikz in tks__xiu:
            try:
                if thybv__gikz:
                    sig = rlfe__xkl.apply(args, kws)
                else:
                    prhi__wrial = tuple([_unlit_non_poison(a) for a in args])
                    ejdkx__nqgp = {trcux__xgrej: _unlit_non_poison(
                        kmw__evkcu) for trcux__xgrej, kmw__evkcu in kws.items()
                        }
                    sig = rlfe__xkl.apply(prhi__wrial, ejdkx__nqgp)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    bopxs__pge.add_error(rlfe__xkl, False, e, thybv__gikz)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = rlfe__xkl.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    oliw__vwip = getattr(rlfe__xkl, 'cases', None)
                    if oliw__vwip is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            oliw__vwip)
                    else:
                        msg = 'No match.'
                    bopxs__pge.add_error(rlfe__xkl, True, msg, thybv__gikz)
    bopxs__pge.raise_error()


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
    oof__qmsm = self.template(context)
    lvs__dct = None
    wwc__itkq = None
    ich__hux = None
    tks__xiu = [True, False] if oof__qmsm.prefer_literal else [False, True]
    tks__xiu = [True] if getattr(oof__qmsm, '_no_unliteral', False
        ) else tks__xiu
    for thybv__gikz in tks__xiu:
        if thybv__gikz:
            try:
                ich__hux = oof__qmsm.apply(args, kws)
            except Exception as pwqn__vebt:
                if isinstance(pwqn__vebt, errors.ForceLiteralArg):
                    raise pwqn__vebt
                lvs__dct = pwqn__vebt
                ich__hux = None
            else:
                break
        else:
            kmkv__ezdzc = tuple([_unlit_non_poison(a) for a in args])
            juk__zkz = {trcux__xgrej: _unlit_non_poison(kmw__evkcu) for 
                trcux__xgrej, kmw__evkcu in kws.items()}
            tdbzo__qqw = kmkv__ezdzc == args and kws == juk__zkz
            if not tdbzo__qqw and ich__hux is None:
                try:
                    ich__hux = oof__qmsm.apply(kmkv__ezdzc, juk__zkz)
                except Exception as pwqn__vebt:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        pwqn__vebt, errors.NumbaError):
                        raise pwqn__vebt
                    if isinstance(pwqn__vebt, errors.ForceLiteralArg):
                        if oof__qmsm.prefer_literal:
                            raise pwqn__vebt
                    wwc__itkq = pwqn__vebt
                else:
                    break
    if ich__hux is None and (wwc__itkq is not None or lvs__dct is not None):
        ejjhl__sdcf = '- Resolution failure for {} arguments:\n{}\n'
        gwkyq__haf = _termcolor.highlight(ejjhl__sdcf)
        if numba.core.config.DEVELOPER_MODE:
            zpmx__inm = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    muxp__kipg = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    muxp__kipg = ['']
                gbm__jpbuk = '\n{}'.format(2 * zpmx__inm)
                nhxqe__ddqt = _termcolor.reset(gbm__jpbuk + gbm__jpbuk.join
                    (_bt_as_lines(muxp__kipg)))
                return _termcolor.reset(nhxqe__ddqt)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            cbswc__xnqev = str(e)
            cbswc__xnqev = cbswc__xnqev if cbswc__xnqev else str(repr(e)
                ) + add_bt(e)
            oqo__jevb = errors.TypingError(textwrap.dedent(cbswc__xnqev))
            return gwkyq__haf.format(literalness, str(oqo__jevb))
        import bodo
        if isinstance(lvs__dct, bodo.utils.typing.BodoError):
            raise lvs__dct
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', lvs__dct) +
                nested_msg('non-literal', wwc__itkq))
        else:
            if 'missing a required argument' in lvs__dct.msg:
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
            raise errors.TypingError(msg, loc=lvs__dct.loc)
    return ich__hux


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
    urtab__mqpdo = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=urtab__mqpdo)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            vrl__bkoi = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), vrl__bkoi)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    ppn__dpxlo = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            ppn__dpxlo.append(types.Omitted(a.value))
        else:
            ppn__dpxlo.append(self.typeof_pyval(a))
    kvhz__kxae = None
    try:
        error = None
        kvhz__kxae = self.compile(tuple(ppn__dpxlo))
    except errors.ForceLiteralArg as e:
        ysh__ekfd = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if ysh__ekfd:
            snv__myz = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            rnlr__sdsna = ', '.join('Arg #{} is {}'.format(i, args[i]) for
                i in sorted(ysh__ekfd))
            raise errors.CompilerError(snv__myz.format(rnlr__sdsna))
        kfbbr__frwkm = []
        try:
            for i, kmw__evkcu in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        kfbbr__frwkm.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        kfbbr__frwkm.append(types.literal(args[i]))
                else:
                    kfbbr__frwkm.append(args[i])
            args = kfbbr__frwkm
        except (OSError, FileNotFoundError) as zah__yvs:
            error = FileNotFoundError(str(zah__yvs) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                kvhz__kxae = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        ezq__vjlb = []
        for i, jauly__xnfr in enumerate(args):
            val = jauly__xnfr.value if isinstance(jauly__xnfr, numba.core.
                dispatcher.OmittedArg) else jauly__xnfr
            try:
                otxcg__uoho = typeof(val, Purpose.argument)
            except ValueError as pnsp__knqm:
                ezq__vjlb.append((i, str(pnsp__knqm)))
            else:
                if otxcg__uoho is None:
                    ezq__vjlb.append((i,
                        f'cannot determine Numba type of value {val}'))
        if ezq__vjlb:
            bldyy__iyd = '\n'.join(f'- argument {i}: {chic__gicm}' for i,
                chic__gicm in ezq__vjlb)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{bldyy__iyd}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                qyd__wcx = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                glpkx__hgaj = False
                for pftj__hnc in qyd__wcx:
                    if pftj__hnc in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        glpkx__hgaj = True
                        break
                if not glpkx__hgaj:
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
                vrl__bkoi = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), vrl__bkoi)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return kvhz__kxae


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
    for qvvz__xrae in cres.library._codegen._engine._defined_symbols:
        if qvvz__xrae.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in qvvz__xrae and (
            'bodo_gb_udf_update_local' in qvvz__xrae or 
            'bodo_gb_udf_combine' in qvvz__xrae or 'bodo_gb_udf_eval' in
            qvvz__xrae or 'bodo_gb_apply_general_udfs' in qvvz__xrae):
            gb_agg_cfunc_addr[qvvz__xrae
                ] = cres.library.get_pointer_to_function(qvvz__xrae)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for qvvz__xrae in cres.library._codegen._engine._defined_symbols:
        if qvvz__xrae.startswith('cfunc') and ('get_join_cond_addr' not in
            qvvz__xrae or 'bodo_join_gen_cond' in qvvz__xrae):
            join_gen_cond_cfunc_addr[qvvz__xrae
                ] = cres.library.get_pointer_to_function(qvvz__xrae)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    qkwh__bslft = self._get_dispatcher_for_current_target()
    if qkwh__bslft is not self:
        return qkwh__bslft.compile(sig)
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
            xrql__kogz = self.overloads.get(tuple(args))
            if xrql__kogz is not None:
                return xrql__kogz.entry_point
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
            amiih__dub = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=amiih__dub):
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
                xijc__ytgs = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in xijc__ytgs:
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
    dxza__vhlj = self._final_module
    lalou__acuy = []
    grj__avq = 0
    for fn in dxza__vhlj.functions:
        grj__avq += 1
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
            lalou__acuy.append(fn.name)
    if grj__avq == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if lalou__acuy:
        dxza__vhlj = dxza__vhlj.clone()
        for name in lalou__acuy:
            dxza__vhlj.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = dxza__vhlj
    return dxza__vhlj


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
    for xecm__ztwtb in self.constraints:
        loc = xecm__ztwtb.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                xecm__ztwtb(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                dshng__udafr = numba.core.errors.TypingError(str(e), loc=
                    xecm__ztwtb.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(dshng__udafr, e)
                    )
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
                    dshng__udafr = numba.core.errors.TypingError(msg.format
                        (con=xecm__ztwtb, err=str(e)), loc=xecm__ztwtb.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(dshng__udafr, e))
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
    for hqkl__edn in self._failures.values():
        for mns__edkp in hqkl__edn:
            if isinstance(mns__edkp.error, ForceLiteralArg):
                raise mns__edkp.error
            if isinstance(mns__edkp.error, bodo.utils.typing.BodoError):
                raise mns__edkp.error
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
    bowct__fgeyq = False
    kloet__inj = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        ksz__btny = set()
        ccng__gech = lives & alias_set
        for kmw__evkcu in ccng__gech:
            ksz__btny |= alias_map[kmw__evkcu]
        lives_n_aliases = lives | ksz__btny | arg_aliases
        if type(stmt) in remove_dead_extensions:
            ekhlb__cxa = remove_dead_extensions[type(stmt)]
            stmt = ekhlb__cxa(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                bowct__fgeyq = True
                continue
        if isinstance(stmt, ir.Assign):
            yovcq__flgei = stmt.target
            fniy__pgevk = stmt.value
            if yovcq__flgei.name not in lives:
                if has_no_side_effect(fniy__pgevk, lives_n_aliases, call_table
                    ):
                    bowct__fgeyq = True
                    continue
                if isinstance(fniy__pgevk, ir.Expr
                    ) and fniy__pgevk.op == 'call' and call_table[fniy__pgevk
                    .func.name] == ['astype']:
                    jzkfj__ksos = guard(get_definition, func_ir,
                        fniy__pgevk.func)
                    if (jzkfj__ksos is not None and jzkfj__ksos.op ==
                        'getattr' and isinstance(typemap[jzkfj__ksos.value.
                        name], types.Array) and jzkfj__ksos.attr == 'astype'):
                        bowct__fgeyq = True
                        continue
            if saved_array_analysis and yovcq__flgei.name in lives and is_expr(
                fniy__pgevk, 'getattr'
                ) and fniy__pgevk.attr == 'shape' and is_array_typ(typemap[
                fniy__pgevk.value.name]
                ) and fniy__pgevk.value.name not in lives:
                sdzsa__jdh = {kmw__evkcu: trcux__xgrej for trcux__xgrej,
                    kmw__evkcu in func_ir.blocks.items()}
                if block in sdzsa__jdh:
                    label = sdzsa__jdh[block]
                    sda__sjdim = saved_array_analysis.get_equiv_set(label)
                    pijzk__inzm = sda__sjdim.get_equiv_set(fniy__pgevk.value)
                    if pijzk__inzm is not None:
                        for kmw__evkcu in pijzk__inzm:
                            if kmw__evkcu.endswith('#0'):
                                kmw__evkcu = kmw__evkcu[:-2]
                            if kmw__evkcu in typemap and is_array_typ(typemap
                                [kmw__evkcu]) and kmw__evkcu in lives:
                                fniy__pgevk.value = ir.Var(fniy__pgevk.
                                    value.scope, kmw__evkcu, fniy__pgevk.
                                    value.loc)
                                bowct__fgeyq = True
                                break
            if isinstance(fniy__pgevk, ir.Var
                ) and yovcq__flgei.name == fniy__pgevk.name:
                bowct__fgeyq = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                bowct__fgeyq = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            elvj__cthun = analysis.ir_extension_usedefs[type(stmt)]
            pcbfj__twzgn, nwed__sklgq = elvj__cthun(stmt)
            lives -= nwed__sklgq
            lives |= pcbfj__twzgn
        else:
            lives |= {kmw__evkcu.name for kmw__evkcu in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                syxo__udj = set()
                if isinstance(fniy__pgevk, ir.Expr):
                    syxo__udj = {kmw__evkcu.name for kmw__evkcu in
                        fniy__pgevk.list_vars()}
                if yovcq__flgei.name not in syxo__udj:
                    lives.remove(yovcq__flgei.name)
        kloet__inj.append(stmt)
    kloet__inj.reverse()
    block.body = kloet__inj
    return bowct__fgeyq


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            hxt__ypkc, = args
            if isinstance(hxt__ypkc, types.IterableType):
                dtype = hxt__ypkc.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), hxt__ypkc)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    pchvg__alggi = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (pchvg__alggi, self.dtype)
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
        except LiteralTypingError as ebr__ofx:
            return
    try:
        return literal(value)
    except LiteralTypingError as ebr__ofx:
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
        eatv__ftvs = py_func.__qualname__
    except AttributeError as ebr__ofx:
        eatv__ftvs = py_func.__name__
    ttdki__ryucp = inspect.getfile(py_func)
    for cls in self._locator_classes:
        anvi__ica = cls.from_function(py_func, ttdki__ryucp)
        if anvi__ica is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (eatv__ftvs, ttdki__ryucp))
    self._locator = anvi__ica
    czj__nri = inspect.getfile(py_func)
    gok__pmyp = os.path.splitext(os.path.basename(czj__nri))[0]
    if ttdki__ryucp.startswith('<ipython-'):
        wxec__hyiml = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', gok__pmyp, count=1)
        if wxec__hyiml == gok__pmyp:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        gok__pmyp = wxec__hyiml
    sih__nnx = '%s.%s' % (gok__pmyp, eatv__ftvs)
    njipd__buxds = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(sih__nnx, njipd__buxds
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    tsp__cbd = list(filter(lambda a: self._istuple(a.name), args))
    if len(tsp__cbd) == 2 and fn.__name__ == 'add':
        auyo__mogha = self.typemap[tsp__cbd[0].name]
        qbuf__cbg = self.typemap[tsp__cbd[1].name]
        if auyo__mogha.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                tsp__cbd[1]))
        if qbuf__cbg.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                tsp__cbd[0]))
        try:
            zkc__gngst = [equiv_set.get_shape(x) for x in tsp__cbd]
            if None in zkc__gngst:
                return None
            igxx__tmhe = sum(zkc__gngst, ())
            return ArrayAnalysis.AnalyzeResult(shape=igxx__tmhe)
        except GuardException as ebr__ofx:
            return None
    pvv__ztxv = list(filter(lambda a: self._isarray(a.name), args))
    require(len(pvv__ztxv) > 0)
    nvgnd__juzgs = [x.name for x in pvv__ztxv]
    hzv__mie = [self.typemap[x.name].ndim for x in pvv__ztxv]
    mom__nar = max(hzv__mie)
    require(mom__nar > 0)
    zkc__gngst = [equiv_set.get_shape(x) for x in pvv__ztxv]
    if any(a is None for a in zkc__gngst):
        return ArrayAnalysis.AnalyzeResult(shape=pvv__ztxv[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, pvv__ztxv))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, zkc__gngst,
        nvgnd__juzgs)


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
    ssvq__yvgfg = code_obj.code
    rsv__nlb = len(ssvq__yvgfg.co_freevars)
    ntgm__arqri = ssvq__yvgfg.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        jdyy__zbhwf, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        ntgm__arqri = [kmw__evkcu.name for kmw__evkcu in jdyy__zbhwf]
    btnm__dye = caller_ir.func_id.func.__globals__
    try:
        btnm__dye = getattr(code_obj, 'globals', btnm__dye)
    except KeyError as ebr__ofx:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    sep__vsssx = []
    for x in ntgm__arqri:
        try:
            xbz__obu = caller_ir.get_definition(x)
        except KeyError as ebr__ofx:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(xbz__obu, (ir.Const, ir.Global, ir.FreeVar)):
            val = xbz__obu.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                nra__xvm = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                btnm__dye[nra__xvm] = bodo.jit(distributed=False)(val)
                btnm__dye[nra__xvm].is_nested_func = True
                val = nra__xvm
            if isinstance(val, CPUDispatcher):
                nra__xvm = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                btnm__dye[nra__xvm] = val
                val = nra__xvm
            sep__vsssx.append(val)
        elif isinstance(xbz__obu, ir.Expr) and xbz__obu.op == 'make_function':
            bwht__ljho = convert_code_obj_to_function(xbz__obu, caller_ir)
            nra__xvm = ir_utils.mk_unique_var('nested_func').replace('.', '_')
            btnm__dye[nra__xvm] = bodo.jit(distributed=False)(bwht__ljho)
            btnm__dye[nra__xvm].is_nested_func = True
            sep__vsssx.append(nra__xvm)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    tyl__cnk = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        sep__vsssx)])
    sop__ohuzp = ','.join([('c_%d' % i) for i in range(rsv__nlb)])
    fkhuy__kcr = list(ssvq__yvgfg.co_varnames)
    bjzo__rwz = 0
    wamsh__ujkvm = ssvq__yvgfg.co_argcount
    sgvkj__gyrl = caller_ir.get_definition(code_obj.defaults)
    if sgvkj__gyrl is not None:
        if isinstance(sgvkj__gyrl, tuple):
            d = [caller_ir.get_definition(x).value for x in sgvkj__gyrl]
            zuhs__ojye = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in sgvkj__gyrl.items]
            zuhs__ojye = tuple(d)
        bjzo__rwz = len(zuhs__ojye)
    hqpa__mht = wamsh__ujkvm - bjzo__rwz
    qhth__nyg = ','.join([('%s' % fkhuy__kcr[i]) for i in range(hqpa__mht)])
    if bjzo__rwz:
        teidm__djhxc = [('%s = %s' % (fkhuy__kcr[i + hqpa__mht], zuhs__ojye
            [i])) for i in range(bjzo__rwz)]
        qhth__nyg += ', '
        qhth__nyg += ', '.join(teidm__djhxc)
    return _create_function_from_code_obj(ssvq__yvgfg, tyl__cnk, qhth__nyg,
        sop__ohuzp, btnm__dye)


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
    for icvrr__lfpv, (wbj__qkcu, wzt__cqhod) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % wzt__cqhod)
            kdag__awase = _pass_registry.get(wbj__qkcu).pass_inst
            if isinstance(kdag__awase, CompilerPass):
                self._runPass(icvrr__lfpv, kdag__awase, state)
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
                    pipeline_name, wzt__cqhod)
                lbj__zfhog = self._patch_error(msg, e)
                raise lbj__zfhog
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
    idwu__dhkfz = None
    nwed__sklgq = {}

    def lookup(var, already_seen, varonly=True):
        val = nwed__sklgq.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    jhexd__vutcr = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        yovcq__flgei = stmt.target
        fniy__pgevk = stmt.value
        nwed__sklgq[yovcq__flgei.name] = fniy__pgevk
        if isinstance(fniy__pgevk, ir.Var) and fniy__pgevk.name in nwed__sklgq:
            fniy__pgevk = lookup(fniy__pgevk, set())
        if isinstance(fniy__pgevk, ir.Expr):
            czbs__ydhmy = set(lookup(kmw__evkcu, set(), True).name for
                kmw__evkcu in fniy__pgevk.list_vars())
            if name in czbs__ydhmy:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(fniy__pgevk)]
                mhgc__nkaxu = [x for x, eamg__sgxt in args if eamg__sgxt.
                    name != name]
                args = [(x, eamg__sgxt) for x, eamg__sgxt in args if x !=
                    eamg__sgxt.name]
                qhmbs__xsqp = dict(args)
                if len(mhgc__nkaxu) == 1:
                    qhmbs__xsqp[mhgc__nkaxu[0]] = ir.Var(yovcq__flgei.scope,
                        name + '#init', yovcq__flgei.loc)
                replace_vars_inner(fniy__pgevk, qhmbs__xsqp)
                idwu__dhkfz = nodes[i:]
                break
    return idwu__dhkfz


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
        ccne__zeczi = expand_aliases({kmw__evkcu.name for kmw__evkcu in
            stmt.list_vars()}, alias_map, arg_aliases)
        sbejz__ceewo = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        ivz__kvbco = expand_aliases({kmw__evkcu.name for kmw__evkcu in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        pjwx__fhf = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(sbejz__ceewo & ivz__kvbco | pjwx__fhf & ccne__zeczi) == 0:
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
    iur__erwy = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            iur__erwy.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                iur__erwy.update(get_parfor_writes(stmt, func_ir))
    return iur__erwy


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    iur__erwy = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        iur__erwy.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        iur__erwy = {kmw__evkcu.name for kmw__evkcu in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        iur__erwy = {kmw__evkcu.name for kmw__evkcu in stmt.get_live_out_vars()
            }
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            iur__erwy.update({kmw__evkcu.name for kmw__evkcu in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        onf__swyw = guard(find_callname, func_ir, stmt.value)
        if onf__swyw in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'copy_array_element', 'bodo.libs.array_kernels'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext'), (
            'tuple_list_to_array', 'bodo.utils.utils')):
            iur__erwy.add(stmt.value.args[0].name)
        if onf__swyw == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            iur__erwy.add(stmt.value.args[1].name)
    return iur__erwy


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
        ekhlb__cxa = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        oqqfi__pzlsy = ekhlb__cxa.format(self, msg)
        self.args = oqqfi__pzlsy,
    else:
        ekhlb__cxa = _termcolor.errmsg('{0}')
        oqqfi__pzlsy = ekhlb__cxa.format(self)
        self.args = oqqfi__pzlsy,
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
        for uaa__ruz in options['distributed']:
            dist_spec[uaa__ruz] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for uaa__ruz in options['distributed_block']:
            dist_spec[uaa__ruz] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    ollv__wgchp = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, ytwn__rbopw in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(ytwn__rbopw)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    puhi__ogw = {}
    for imkzj__cqest in reversed(inspect.getmro(cls)):
        puhi__ogw.update(imkzj__cqest.__dict__)
    wnxaq__zjdkp, htngs__vwhae, gwc__altwz, lfp__qikq = {}, {}, {}, {}
    for trcux__xgrej, kmw__evkcu in puhi__ogw.items():
        if isinstance(kmw__evkcu, pytypes.FunctionType):
            wnxaq__zjdkp[trcux__xgrej] = kmw__evkcu
        elif isinstance(kmw__evkcu, property):
            htngs__vwhae[trcux__xgrej] = kmw__evkcu
        elif isinstance(kmw__evkcu, staticmethod):
            gwc__altwz[trcux__xgrej] = kmw__evkcu
        else:
            lfp__qikq[trcux__xgrej] = kmw__evkcu
    hugr__shcu = (set(wnxaq__zjdkp) | set(htngs__vwhae) | set(gwc__altwz)
        ) & set(spec)
    if hugr__shcu:
        raise NameError('name shadowing: {0}'.format(', '.join(hugr__shcu)))
    ikes__xfm = lfp__qikq.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(lfp__qikq)
    if lfp__qikq:
        msg = 'class members are not yet supported: {0}'
        euy__iehny = ', '.join(lfp__qikq.keys())
        raise TypeError(msg.format(euy__iehny))
    for trcux__xgrej, kmw__evkcu in htngs__vwhae.items():
        if kmw__evkcu.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(
                trcux__xgrej))
    jit_methods = {trcux__xgrej: bodo.jit(returns_maybe_distributed=
        ollv__wgchp)(kmw__evkcu) for trcux__xgrej, kmw__evkcu in
        wnxaq__zjdkp.items()}
    jit_props = {}
    for trcux__xgrej, kmw__evkcu in htngs__vwhae.items():
        ngpv__csq = {}
        if kmw__evkcu.fget:
            ngpv__csq['get'] = bodo.jit(kmw__evkcu.fget)
        if kmw__evkcu.fset:
            ngpv__csq['set'] = bodo.jit(kmw__evkcu.fset)
        jit_props[trcux__xgrej] = ngpv__csq
    jit_static_methods = {trcux__xgrej: bodo.jit(kmw__evkcu.__func__) for 
        trcux__xgrej, kmw__evkcu in gwc__altwz.items()}
    zvdlf__tbql = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    kfv__urug = dict(class_type=zvdlf__tbql, __doc__=ikes__xfm)
    kfv__urug.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), kfv__urug)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, zvdlf__tbql)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(zvdlf__tbql, typingctx, targetctx).register()
    as_numba_type.register(cls, zvdlf__tbql.instance_type)
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
    vtxx__ass = ','.join('{0}:{1}'.format(trcux__xgrej, kmw__evkcu) for 
        trcux__xgrej, kmw__evkcu in struct.items())
    evkh__ajx = ','.join('{0}:{1}'.format(trcux__xgrej, kmw__evkcu) for 
        trcux__xgrej, kmw__evkcu in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), vtxx__ass, evkh__ajx)
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
    brfyw__mlfho = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if brfyw__mlfho is None:
        return
    kvgw__lwsm, wkeb__mht = brfyw__mlfho
    for a in itertools.chain(kvgw__lwsm, wkeb__mht.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, kvgw__lwsm, wkeb__mht)
    except ForceLiteralArg as e:
        vbd__ovvo = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(vbd__ovvo, self.kws)
        prw__cmh = set()
        wxzcx__eytj = set()
        wxemq__wxt = {}
        for icvrr__lfpv in e.requested_args:
            pley__dunf = typeinfer.func_ir.get_definition(folded[icvrr__lfpv])
            if isinstance(pley__dunf, ir.Arg):
                prw__cmh.add(pley__dunf.index)
                if pley__dunf.index in e.file_infos:
                    wxemq__wxt[pley__dunf.index] = e.file_infos[pley__dunf.
                        index]
            else:
                wxzcx__eytj.add(icvrr__lfpv)
        if wxzcx__eytj:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif prw__cmh:
            raise ForceLiteralArg(prw__cmh, loc=self.loc, file_infos=wxemq__wxt
                )
    if sig is None:
        ebrcr__lrfpl = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in kvgw__lwsm]
        args += [('%s=%s' % (trcux__xgrej, kmw__evkcu)) for trcux__xgrej,
            kmw__evkcu in sorted(wkeb__mht.items())]
        kcmgc__dgo = ebrcr__lrfpl.format(fnty, ', '.join(map(str, args)))
        negxy__ojex = context.explain_function_type(fnty)
        msg = '\n'.join([kcmgc__dgo, negxy__ojex])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        puza__zrala = context.unify_pairs(sig.recvr, fnty.this)
        if puza__zrala is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if puza__zrala is not None and puza__zrala.is_precise():
            elge__swo = fnty.copy(this=puza__zrala)
            typeinfer.propagate_refined_type(self.func, elge__swo)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            wriqq__ptn = target.getone()
            if context.unify_pairs(wriqq__ptn, sig.return_type) == wriqq__ptn:
                sig = sig.replace(return_type=wriqq__ptn)
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
        snv__myz = '*other* must be a {} but got a {} instead'
        raise TypeError(snv__myz.format(ForceLiteralArg, type(other)))
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
    ehjtl__byhy = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for trcux__xgrej, kmw__evkcu in kwargs.items():
        tyq__ihzl = None
        try:
            wwevh__feddi = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[wwevh__feddi.name] = [kmw__evkcu]
            tyq__ihzl = get_const_value_inner(func_ir, wwevh__feddi)
            func_ir._definitions.pop(wwevh__feddi.name)
            if isinstance(tyq__ihzl, str):
                tyq__ihzl = sigutils._parse_signature_string(tyq__ihzl)
            if isinstance(tyq__ihzl, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {trcux__xgrej} is annotated as type class {tyq__ihzl}."""
                    )
            assert isinstance(tyq__ihzl, types.Type)
            if isinstance(tyq__ihzl, (types.List, types.Set)):
                tyq__ihzl = tyq__ihzl.copy(reflected=False)
            ehjtl__byhy[trcux__xgrej] = tyq__ihzl
        except BodoError as ebr__ofx:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(tyq__ihzl, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(kmw__evkcu, ir.Global):
                    msg = f'Global {kmw__evkcu.name!r} is not defined.'
                if isinstance(kmw__evkcu, ir.FreeVar):
                    msg = f'Freevar {kmw__evkcu.name!r} is not defined.'
            if isinstance(kmw__evkcu, ir.Expr) and kmw__evkcu.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=trcux__xgrej, msg=msg, loc=loc)
    for name, typ in ehjtl__byhy.items():
        self._legalize_arg_type(name, typ, loc)
    return ehjtl__byhy


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
    rqeq__wdag = inst.arg
    assert rqeq__wdag > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(rqeq__wdag)]))
    tmps = [state.make_temp() for _ in range(rqeq__wdag - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    vja__skf = ir.Global('format', format, loc=self.loc)
    self.store(value=vja__skf, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    vmyle__jbfxd = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=vmyle__jbfxd, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    rqeq__wdag = inst.arg
    assert rqeq__wdag > 0, 'invalid BUILD_STRING count'
    qpptj__bbgsw = self.get(strings[0])
    for other, pfx__crk in zip(strings[1:], tmps):
        other = self.get(other)
        rhvg__iuepj = ir.Expr.binop(operator.add, lhs=qpptj__bbgsw, rhs=
            other, loc=self.loc)
        self.store(rhvg__iuepj, pfx__crk)
        qpptj__bbgsw = self.get(pfx__crk)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    rmzdf__vtb = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, rmzdf__vtb])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    gfmp__dckl = mk_unique_var(f'{var_name}')
    stcrs__kzvqc = gfmp__dckl.replace('<', '_').replace('>', '_')
    stcrs__kzvqc = stcrs__kzvqc.replace('.', '_').replace('$', '_v')
    return stcrs__kzvqc


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
                nib__upxj = get_overload_const_str(val2)
                if nib__upxj != 'ns':
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
        ubtri__cerj = states['defmap']
        if len(ubtri__cerj) == 0:
            mglf__pla = assign.target
            numba.core.ssa._logger.debug('first assign: %s', mglf__pla)
            if mglf__pla.name not in scope.localvars:
                mglf__pla = scope.define(assign.target.name, loc=assign.loc)
        else:
            mglf__pla = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=mglf__pla, value=assign.value, loc=assign.loc
            )
        ubtri__cerj[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    iopw__ydqal = []
    for trcux__xgrej, kmw__evkcu in typing.npydecl.registry.globals:
        if trcux__xgrej == func:
            iopw__ydqal.append(kmw__evkcu)
    for trcux__xgrej, kmw__evkcu in typing.templates.builtin_registry.globals:
        if trcux__xgrej == func:
            iopw__ydqal.append(kmw__evkcu)
    if len(iopw__ydqal) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return iopw__ydqal


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    hhq__ergoe = {}
    glqj__fxn = find_topo_order(blocks)
    apaor__iqt = {}
    for label in glqj__fxn:
        block = blocks[label]
        kloet__inj = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                yovcq__flgei = stmt.target.name
                fniy__pgevk = stmt.value
                if (fniy__pgevk.op == 'getattr' and fniy__pgevk.attr in
                    arr_math and isinstance(typemap[fniy__pgevk.value.name],
                    types.npytypes.Array)):
                    fniy__pgevk = stmt.value
                    mdisi__vxgo = fniy__pgevk.value
                    hhq__ergoe[yovcq__flgei] = mdisi__vxgo
                    scope = mdisi__vxgo.scope
                    loc = mdisi__vxgo.loc
                    prt__xxli = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[prt__xxli.name] = types.misc.Module(numpy)
                    uduhw__mzoak = ir.Global('np', numpy, loc)
                    ulpm__mhwj = ir.Assign(uduhw__mzoak, prt__xxli, loc)
                    fniy__pgevk.value = prt__xxli
                    kloet__inj.append(ulpm__mhwj)
                    func_ir._definitions[prt__xxli.name] = [uduhw__mzoak]
                    func = getattr(numpy, fniy__pgevk.attr)
                    ggzf__atd = get_np_ufunc_typ_lst(func)
                    apaor__iqt[yovcq__flgei] = ggzf__atd
                if (fniy__pgevk.op == 'call' and fniy__pgevk.func.name in
                    hhq__ergoe):
                    mdisi__vxgo = hhq__ergoe[fniy__pgevk.func.name]
                    ozej__zjet = calltypes.pop(fniy__pgevk)
                    uigbd__epl = ozej__zjet.args[:len(fniy__pgevk.args)]
                    icl__zeqw = {name: typemap[kmw__evkcu.name] for name,
                        kmw__evkcu in fniy__pgevk.kws}
                    tkou__wltzr = apaor__iqt[fniy__pgevk.func.name]
                    ahrwi__exdd = None
                    for yfzs__rsud in tkou__wltzr:
                        try:
                            ahrwi__exdd = yfzs__rsud.get_call_type(typingctx,
                                [typemap[mdisi__vxgo.name]] + list(
                                uigbd__epl), icl__zeqw)
                            typemap.pop(fniy__pgevk.func.name)
                            typemap[fniy__pgevk.func.name] = yfzs__rsud
                            calltypes[fniy__pgevk] = ahrwi__exdd
                            break
                        except Exception as ebr__ofx:
                            pass
                    if ahrwi__exdd is None:
                        raise TypeError(
                            f'No valid template found for {fniy__pgevk.func.name}'
                            )
                    fniy__pgevk.args = [mdisi__vxgo] + fniy__pgevk.args
            kloet__inj.append(stmt)
        block.body = kloet__inj


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    xeu__pzd = ufunc.nin
    nseb__lgmm = ufunc.nout
    hqpa__mht = ufunc.nargs
    assert hqpa__mht == xeu__pzd + nseb__lgmm
    if len(args) < xeu__pzd:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), xeu__pzd))
    if len(args) > hqpa__mht:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), hqpa__mht))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    fhj__tape = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    lbx__tcun = max(fhj__tape)
    add__zjth = args[xeu__pzd:]
    if not all(d == lbx__tcun for d in fhj__tape[xeu__pzd:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(jtmzh__kgqc, types.ArrayCompatible) and not
        isinstance(jtmzh__kgqc, types.Bytes) for jtmzh__kgqc in add__zjth):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(jtmzh__kgqc.mutable for jtmzh__kgqc in add__zjth):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    gkfj__mkyc = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    axf__vwz = None
    if lbx__tcun > 0 and len(add__zjth) < ufunc.nout:
        axf__vwz = 'C'
        yen__wtw = [(x.layout if isinstance(x, types.ArrayCompatible) and 
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in yen__wtw and 'F' in yen__wtw:
            axf__vwz = 'F'
    return gkfj__mkyc, add__zjth, lbx__tcun, axf__vwz


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
        pddxj__lrb = 'Dict.key_type cannot be of type {}'
        raise TypingError(pddxj__lrb.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        pddxj__lrb = 'Dict.value_type cannot be of type {}'
        raise TypingError(pddxj__lrb.format(valty))
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
    bebcv__ipuva = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[bebcv__ipuva]
        return impl, args
    except KeyError as ebr__ofx:
        pass
    impl, args = self._build_impl(bebcv__ipuva, args, kws)
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
    jqrgq__ctqtx = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            ghl__due = block.body[-1]
            if isinstance(ghl__due, ir.Branch):
                if len(blocks[ghl__due.truebr].body) == 1 and len(blocks[
                    ghl__due.falsebr].body) == 1:
                    kutfh__tht = blocks[ghl__due.truebr].body[0]
                    zewa__kfmm = blocks[ghl__due.falsebr].body[0]
                    if isinstance(kutfh__tht, ir.Jump) and isinstance(
                        zewa__kfmm, ir.Jump
                        ) and kutfh__tht.target == zewa__kfmm.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(kutfh__tht
                            .target, ghl__due.loc)
                        jqrgq__ctqtx = True
                elif len(blocks[ghl__due.truebr].body) == 1:
                    kutfh__tht = blocks[ghl__due.truebr].body[0]
                    if isinstance(kutfh__tht, ir.Jump
                        ) and kutfh__tht.target == ghl__due.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(kutfh__tht
                            .target, ghl__due.loc)
                        jqrgq__ctqtx = True
                elif len(blocks[ghl__due.falsebr].body) == 1:
                    zewa__kfmm = blocks[ghl__due.falsebr].body[0]
                    if isinstance(zewa__kfmm, ir.Jump
                        ) and zewa__kfmm.target == ghl__due.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(zewa__kfmm
                            .target, ghl__due.loc)
                        jqrgq__ctqtx = True
    return jqrgq__ctqtx


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        vjqua__qbl = find_topo_order(parfor.loop_body)
    fkgjy__bhxa = vjqua__qbl[0]
    bzej__scb = {}
    _update_parfor_get_setitems(parfor.loop_body[fkgjy__bhxa].body, parfor.
        index_var, alias_map, bzej__scb, lives_n_aliases)
    evdq__qdxtc = set(bzej__scb.keys())
    for rcos__yhd in vjqua__qbl:
        if rcos__yhd == fkgjy__bhxa:
            continue
        for stmt in parfor.loop_body[rcos__yhd].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            ypnb__lslnp = set(kmw__evkcu.name for kmw__evkcu in stmt.
                list_vars())
            xkfcb__eoax = ypnb__lslnp & evdq__qdxtc
            for a in xkfcb__eoax:
                bzej__scb.pop(a, None)
    for rcos__yhd in vjqua__qbl:
        if rcos__yhd == fkgjy__bhxa:
            continue
        block = parfor.loop_body[rcos__yhd]
        omk__jywo = bzej__scb.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            omk__jywo, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    nozq__sklbo = max(blocks.keys())
    vwq__zby, ocxjg__adswz = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    egd__sxid = ir.Jump(vwq__zby, ir.Loc('parfors_dummy', -1))
    blocks[nozq__sklbo].body.append(egd__sxid)
    upp__inc = compute_cfg_from_blocks(blocks)
    ocj__ewef = compute_use_defs(blocks)
    tybl__wsds = compute_live_map(upp__inc, blocks, ocj__ewef.usemap,
        ocj__ewef.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        kloet__inj = []
        ovisw__djky = {kmw__evkcu.name for kmw__evkcu in block.terminator.
            list_vars()}
        for paop__axeo, bewqo__lkh in upp__inc.successors(label):
            ovisw__djky |= tybl__wsds[paop__axeo]
        for stmt in reversed(block.body):
            ksz__btny = ovisw__djky & alias_set
            for kmw__evkcu in ksz__btny:
                ovisw__djky |= alias_map[kmw__evkcu]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in ovisw__djky and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                onf__swyw = guard(find_callname, func_ir, stmt.value)
                if onf__swyw == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in ovisw__djky and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            ovisw__djky |= {kmw__evkcu.name for kmw__evkcu in stmt.list_vars()}
            kloet__inj.append(stmt)
        kloet__inj.reverse()
        block.body = kloet__inj
    typemap.pop(ocxjg__adswz.name)
    blocks[nozq__sklbo].body.pop()
    jqrgq__ctqtx = True
    while jqrgq__ctqtx:
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
        jqrgq__ctqtx = trim_empty_parfor_branches(parfor)
    dww__gea = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        dww__gea &= len(block.body) == 0
    if dww__gea:
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
    nyyq__buc = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                nyyq__buc += 1
                parfor = stmt
                tjale__jruf = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = tjale__jruf.scope
                loc = ir.Loc('parfors_dummy', -1)
                czash__ugyfj = ir.Var(scope, mk_unique_var('$const'), loc)
                tjale__jruf.body.append(ir.Assign(ir.Const(0, loc),
                    czash__ugyfj, loc))
                tjale__jruf.body.append(ir.Return(czash__ugyfj, loc))
                upp__inc = compute_cfg_from_blocks(parfor.loop_body)
                for qfm__yjh in upp__inc.dead_nodes():
                    del parfor.loop_body[qfm__yjh]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                tjale__jruf = parfor.loop_body[max(parfor.loop_body.keys())]
                tjale__jruf.body.pop()
                tjale__jruf.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return nyyq__buc


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    upp__inc = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != upp__inc.entry_point()
    lzja__gvdqv = list(filter(find_single_branch, blocks.keys()))
    nik__vkbae = set()
    for label in lzja__gvdqv:
        inst = blocks[label].body[0]
        lai__dtlti = upp__inc.predecessors(label)
        kyu__cruy = True
        for bviu__zmbxq, pkxh__pmre in lai__dtlti:
            block = blocks[bviu__zmbxq]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                kyu__cruy = False
        if kyu__cruy:
            nik__vkbae.add(label)
    for label in nik__vkbae:
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
            xrql__kogz = self.overloads.get(tuple(args))
            if xrql__kogz is not None:
                return xrql__kogz.entry_point
            self._pre_compile(args, return_type, flags)
            dwspj__mrzjm = self.func_ir
            amiih__dub = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=amiih__dub):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=dwspj__mrzjm, args=
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
        gok__sbecw = copy.deepcopy(flags)
        gok__sbecw.no_rewrites = True

        def compile_local(the_ir, the_flags):
            gvsqx__pmg = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return gvsqx__pmg.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        efkv__uam = compile_local(func_ir, gok__sbecw)
        gyb__dvecy = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    gyb__dvecy = compile_local(func_ir, flags)
                except Exception as ebr__ofx:
                    pass
        if gyb__dvecy is not None:
            cres = gyb__dvecy
        else:
            cres = efkv__uam
        return cres
    else:
        gvsqx__pmg = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return gvsqx__pmg.compile_ir(func_ir=func_ir, lifted=lifted,
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
    zlawc__erxgo = self.get_data_type(typ.dtype)
    uadc__qtn = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        uadc__qtn):
        elkod__dey = ary.ctypes.data
        ssu__eazlc = self.add_dynamic_addr(builder, elkod__dey, info=str(
            type(elkod__dey)))
        xzs__akyyr = self.add_dynamic_addr(builder, id(ary), info=str(type(
            ary)))
        self.global_arrays.append(ary)
    else:
        gvo__xhgsp = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            gvo__xhgsp = gvo__xhgsp.view('int64')
        val = bytearray(gvo__xhgsp.data)
        lred__wjyfx = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val
            )
        ssu__eazlc = cgutils.global_constant(builder, '.const.array.data',
            lred__wjyfx)
        ssu__eazlc.align = self.get_abi_alignment(zlawc__erxgo)
        xzs__akyyr = None
    zhaj__gsj = self.get_value_type(types.intp)
    mkxr__iuzm = [self.get_constant(types.intp, vpqr__sbxz) for vpqr__sbxz in
        ary.shape]
    emq__osjl = lir.Constant(lir.ArrayType(zhaj__gsj, len(mkxr__iuzm)),
        mkxr__iuzm)
    jjbnr__gel = [self.get_constant(types.intp, vpqr__sbxz) for vpqr__sbxz in
        ary.strides]
    uqp__hwedd = lir.Constant(lir.ArrayType(zhaj__gsj, len(jjbnr__gel)),
        jjbnr__gel)
    psvh__aji = self.get_constant(types.intp, ary.dtype.itemsize)
    ukqu__whopg = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        ukqu__whopg, psvh__aji, ssu__eazlc.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), emq__osjl, uqp__hwedd])


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
    xxor__tvwt = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    sabd__eygkd = lir.Function(module, xxor__tvwt, name='nrt_atomic_{0}'.
        format(op))
    [fnsxp__ipfoo] = sabd__eygkd.args
    pir__zvugi = sabd__eygkd.append_basic_block()
    builder = lir.IRBuilder(pir__zvugi)
    smbsh__eez = lir.Constant(_word_type, 1)
    if False:
        duxe__prj = builder.atomic_rmw(op, fnsxp__ipfoo, smbsh__eez,
            ordering=ordering)
        res = getattr(builder, op)(duxe__prj, smbsh__eez)
        builder.ret(res)
    else:
        duxe__prj = builder.load(fnsxp__ipfoo)
        qto__mvwp = getattr(builder, op)(duxe__prj, smbsh__eez)
        ozus__ipv = builder.icmp_signed('!=', duxe__prj, lir.Constant(
            duxe__prj.type, -1))
        with cgutils.if_likely(builder, ozus__ipv):
            builder.store(qto__mvwp, fnsxp__ipfoo)
        builder.ret(qto__mvwp)
    return sabd__eygkd


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
        olefw__ghaz = state.targetctx.codegen()
        state.library = olefw__ghaz.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    sqp__uiz = state.func_ir
    typemap = state.typemap
    qxeae__cgkyy = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    dqmbk__ynubn = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            sqp__uiz, typemap, qxeae__cgkyy, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            vscza__ihti = lowering.Lower(targetctx, library, fndesc,
                sqp__uiz, metadata=metadata)
            vscza__ihti.lower()
            if not flags.no_cpython_wrapper:
                vscza__ihti.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(qxeae__cgkyy, (types.Optional, types.
                        Generator)):
                        pass
                    else:
                        vscza__ihti.create_cfunc_wrapper()
            env = vscza__ihti.env
            zqqc__uaho = vscza__ihti.call_helper
            del vscza__ihti
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, zqqc__uaho, cfunc=None, env=env)
        else:
            hktwz__qjs = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(hktwz__qjs, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, zqqc__uaho, cfunc=hktwz__qjs,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        boytb__cajrr = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = boytb__cajrr - dqmbk__ynubn
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
        crjak__fdxt = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, crjak__fdxt),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            ucnmo__fmtx.do_break()
        iamt__gsq = c.builder.icmp_signed('!=', crjak__fdxt, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(iamt__gsq, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, crjak__fdxt)
                c.pyapi.decref(crjak__fdxt)
                ucnmo__fmtx.do_break()
        c.pyapi.decref(crjak__fdxt)
    sfd__elend, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(sfd__elend, likely=True) as (zqz__rzg, fepg__zunpo):
        with zqz__rzg:
            list.size = size
            its__torsv = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                its__torsv), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        its__torsv))
                    with cgutils.for_range(c.builder, size) as ucnmo__fmtx:
                        itemobj = c.pyapi.list_getitem(obj, ucnmo__fmtx.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        htk__lnts = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(htk__lnts.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            ucnmo__fmtx.do_break()
                        list.setitem(ucnmo__fmtx.index, htk__lnts.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with fepg__zunpo:
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
    aftru__qzd, gfr__iuh, bpjx__icuy, snho__ydsfb, iom__htavi = (
        compile_time_get_string_data(literal_string))
    dxza__vhlj = builder.module
    gv = context.insert_const_bytes(dxza__vhlj, aftru__qzd)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        gfr__iuh), context.get_constant(types.int32, bpjx__icuy), context.
        get_constant(types.uint32, snho__ydsfb), context.get_constant(
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
    rur__lsv = None
    if isinstance(shape, types.Integer):
        rur__lsv = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(vpqr__sbxz, (types.Integer, types.IntEnumMember)) for
            vpqr__sbxz in shape):
            rur__lsv = len(shape)
    return rur__lsv


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
            rur__lsv = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if rur__lsv == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(rur__lsv))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            nvgnd__juzgs = self._get_names(x)
            if len(nvgnd__juzgs) != 0:
                return nvgnd__juzgs[0]
            return nvgnd__juzgs
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    nvgnd__juzgs = self._get_names(obj)
    if len(nvgnd__juzgs) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(nvgnd__juzgs[0])


def get_equiv_set(self, obj):
    nvgnd__juzgs = self._get_names(obj)
    if len(nvgnd__juzgs) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(nvgnd__juzgs[0])


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
    zduo__xzoca = []
    for wloz__mqjtj in func_ir.arg_names:
        if wloz__mqjtj in typemap and isinstance(typemap[wloz__mqjtj],
            types.containers.UniTuple) and typemap[wloz__mqjtj].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(wloz__mqjtj))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for uilnq__dwyzv in func_ir.blocks.values():
        for stmt in uilnq__dwyzv.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    jqgti__tsjk = getattr(val, 'code', None)
                    if jqgti__tsjk is not None:
                        if getattr(val, 'closure', None) is not None:
                            ryzos__urr = '<creating a function from a closure>'
                            rhvg__iuepj = ''
                        else:
                            ryzos__urr = jqgti__tsjk.co_name
                            rhvg__iuepj = '(%s) ' % ryzos__urr
                    else:
                        ryzos__urr = '<could not ascertain use case>'
                        rhvg__iuepj = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (ryzos__urr, rhvg__iuepj))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                fybuz__kbv = False
                if isinstance(val, pytypes.FunctionType):
                    fybuz__kbv = val in {numba.gdb, numba.gdb_init}
                if not fybuz__kbv:
                    fybuz__kbv = getattr(val, '_name', '') == 'gdb_internal'
                if fybuz__kbv:
                    zduo__xzoca.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    lxeir__wgu = func_ir.get_definition(var)
                    zyeg__helr = guard(find_callname, func_ir, lxeir__wgu)
                    if zyeg__helr and zyeg__helr[1] == 'numpy':
                        ty = getattr(numpy, zyeg__helr[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    ifmc__rjzrt = '' if var.startswith('$'
                        ) else "'{}' ".format(var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(ifmc__rjzrt), loc=stmt.loc)
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
    if len(zduo__xzoca) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        pkwxd__ivik = '\n'.join([x.strformat() for x in zduo__xzoca])
        raise errors.UnsupportedError(msg % pkwxd__ivik)


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
    trcux__xgrej, kmw__evkcu = next(iter(val.items()))
    ksnx__xtaxd = typeof_impl(trcux__xgrej, c)
    dep__zra = typeof_impl(kmw__evkcu, c)
    if ksnx__xtaxd is None or dep__zra is None:
        raise ValueError(
            f'Cannot type dict element type {type(trcux__xgrej)}, {type(kmw__evkcu)}'
            )
    return types.DictType(ksnx__xtaxd, dep__zra)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    dgpx__eejk = cgutils.alloca_once_value(c.builder, val)
    wcgqz__ama = c.pyapi.object_hasattr_string(val, '_opaque')
    ofyz__ydlh = c.builder.icmp_unsigned('==', wcgqz__ama, lir.Constant(
        wcgqz__ama.type, 0))
    kjo__fimd = typ.key_type
    owimy__wrxki = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(kjo__fimd, owimy__wrxki)

    def copy_dict(out_dict, in_dict):
        for trcux__xgrej, kmw__evkcu in in_dict.items():
            out_dict[trcux__xgrej] = kmw__evkcu
    with c.builder.if_then(ofyz__ydlh):
        mdsac__fsqk = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        vsm__zad = c.pyapi.call_function_objargs(mdsac__fsqk, [])
        vnymc__rpr = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(vnymc__rpr, [vsm__zad, val])
        c.builder.store(vsm__zad, dgpx__eejk)
    val = c.builder.load(dgpx__eejk)
    qfc__hoapa = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    iadcg__mftfv = c.pyapi.object_type(val)
    tuh__wqvm = c.builder.icmp_unsigned('==', iadcg__mftfv, qfc__hoapa)
    with c.builder.if_else(tuh__wqvm) as (ijt__qzu, eha__mjld):
        with ijt__qzu:
            ffeq__itmj = c.pyapi.object_getattr_string(val, '_opaque')
            gbeiw__ics = types.MemInfoPointer(types.voidptr)
            htk__lnts = c.unbox(gbeiw__ics, ffeq__itmj)
            mi = htk__lnts.value
            ppn__dpxlo = gbeiw__ics, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *ppn__dpxlo)
            xizb__dfkzo = context.get_constant_null(ppn__dpxlo[1])
            args = mi, xizb__dfkzo
            tjxm__ynwuo, jucdb__tiisc = c.pyapi.call_jit_code(convert, sig,
                args)
            c.context.nrt.decref(c.builder, typ, jucdb__tiisc)
            c.pyapi.decref(ffeq__itmj)
            rhzed__owgy = c.builder.basic_block
        with eha__mjld:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", iadcg__mftfv, qfc__hoapa)
            nma__jvixl = c.builder.basic_block
    udvm__ycz = c.builder.phi(jucdb__tiisc.type)
    rsqi__jgpak = c.builder.phi(tjxm__ynwuo.type)
    udvm__ycz.add_incoming(jucdb__tiisc, rhzed__owgy)
    udvm__ycz.add_incoming(jucdb__tiisc.type(None), nma__jvixl)
    rsqi__jgpak.add_incoming(tjxm__ynwuo, rhzed__owgy)
    rsqi__jgpak.add_incoming(cgutils.true_bit, nma__jvixl)
    c.pyapi.decref(qfc__hoapa)
    c.pyapi.decref(iadcg__mftfv)
    with c.builder.if_then(ofyz__ydlh):
        c.pyapi.decref(val)
    return NativeValue(udvm__ycz, is_error=rsqi__jgpak)


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
    hyagq__tyqb = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=hyagq__tyqb, name=updatevar)
    bue__yxxyo = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=bue__yxxyo, name=res)


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
        for trcux__xgrej, kmw__evkcu in other.items():
            d[trcux__xgrej] = kmw__evkcu
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
    rhvg__iuepj = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(rhvg__iuepj, res)


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
    hvflu__gsy = PassManager(name)
    if state.func_ir is None:
        hvflu__gsy.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            hvflu__gsy.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        hvflu__gsy.add_pass(FixupArgs, 'fix up args')
    hvflu__gsy.add_pass(IRProcessing, 'processing IR')
    hvflu__gsy.add_pass(WithLifting, 'Handle with contexts')
    hvflu__gsy.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        hvflu__gsy.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        hvflu__gsy.add_pass(DeadBranchPrune, 'dead branch pruning')
        hvflu__gsy.add_pass(GenericRewrites, 'nopython rewrites')
    hvflu__gsy.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    hvflu__gsy.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        hvflu__gsy.add_pass(DeadBranchPrune, 'dead branch pruning')
    hvflu__gsy.add_pass(FindLiterallyCalls, 'find literally calls')
    hvflu__gsy.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        hvflu__gsy.add_pass(ReconstructSSA, 'ssa')
    hvflu__gsy.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    hvflu__gsy.finalize()
    return hvflu__gsy


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
    a, qydhm__iia = args
    if isinstance(a, types.List) and isinstance(qydhm__iia, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(qydhm__iia, types.List):
        return signature(qydhm__iia, types.intp, qydhm__iia)


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
        qwf__mvy, ixkx__prk = 0, 1
    else:
        qwf__mvy, ixkx__prk = 1, 0
    lft__sfiyy = ListInstance(context, builder, sig.args[qwf__mvy], args[
        qwf__mvy])
    xam__ymcg = lft__sfiyy.size
    coej__cgw = args[ixkx__prk]
    its__torsv = lir.Constant(coej__cgw.type, 0)
    coej__cgw = builder.select(cgutils.is_neg_int(builder, coej__cgw),
        its__torsv, coej__cgw)
    ukqu__whopg = builder.mul(coej__cgw, xam__ymcg)
    wfmc__umf = ListInstance.allocate(context, builder, sig.return_type,
        ukqu__whopg)
    wfmc__umf.size = ukqu__whopg
    with cgutils.for_range_slice(builder, its__torsv, ukqu__whopg,
        xam__ymcg, inc=True) as (xow__olgn, _):
        with cgutils.for_range(builder, xam__ymcg) as ucnmo__fmtx:
            value = lft__sfiyy.getitem(ucnmo__fmtx.index)
            wfmc__umf.setitem(builder.add(ucnmo__fmtx.index, xow__olgn),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, wfmc__umf.value)


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
    jcpow__hyg = first.unify(self, second)
    if jcpow__hyg is not None:
        return jcpow__hyg
    jcpow__hyg = second.unify(self, first)
    if jcpow__hyg is not None:
        return jcpow__hyg
    pwb__dgz = self.can_convert(fromty=first, toty=second)
    if pwb__dgz is not None and pwb__dgz <= Conversion.safe:
        return second
    pwb__dgz = self.can_convert(fromty=second, toty=first)
    if pwb__dgz is not None and pwb__dgz <= Conversion.safe:
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
    ukqu__whopg = payload.used
    listobj = c.pyapi.list_new(ukqu__whopg)
    sfd__elend = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(sfd__elend, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(
            ukqu__whopg.type, 0))
        with payload._iterate() as ucnmo__fmtx:
            i = c.builder.load(index)
            item = ucnmo__fmtx.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return sfd__elend, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    fztbr__rxis = h.type
    safmv__gbdlf = self.mask
    dtype = self._ty.dtype
    gqv__ncfe = context.typing_context
    fnty = gqv__ncfe.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(gqv__ncfe, (dtype, dtype), {})
    qcm__ubxol = context.get_function(fnty, sig)
    esyzm__vkuzm = ir.Constant(fztbr__rxis, 1)
    etzfp__goj = ir.Constant(fztbr__rxis, 5)
    photz__cdrp = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, safmv__gbdlf))
    if for_insert:
        jrdv__ycf = safmv__gbdlf.type(-1)
        brhw__cfokm = cgutils.alloca_once_value(builder, jrdv__ycf)
    rmtc__vzxew = builder.append_basic_block('lookup.body')
    marsp__iwqz = builder.append_basic_block('lookup.found')
    qdqkv__sdbrd = builder.append_basic_block('lookup.not_found')
    xpm__dwo = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        faev__tdlrs = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, faev__tdlrs)):
            pbj__ltb = qcm__ubxol(builder, (item, entry.key))
            with builder.if_then(pbj__ltb):
                builder.branch(marsp__iwqz)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, faev__tdlrs)):
            builder.branch(qdqkv__sdbrd)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, faev__tdlrs)):
                xtznj__rbi = builder.load(brhw__cfokm)
                xtznj__rbi = builder.select(builder.icmp_unsigned('==',
                    xtznj__rbi, jrdv__ycf), i, xtznj__rbi)
                builder.store(xtznj__rbi, brhw__cfokm)
    with cgutils.for_range(builder, ir.Constant(fztbr__rxis, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, esyzm__vkuzm)
        i = builder.and_(i, safmv__gbdlf)
        builder.store(i, index)
    builder.branch(rmtc__vzxew)
    with builder.goto_block(rmtc__vzxew):
        i = builder.load(index)
        check_entry(i)
        bviu__zmbxq = builder.load(photz__cdrp)
        bviu__zmbxq = builder.lshr(bviu__zmbxq, etzfp__goj)
        i = builder.add(esyzm__vkuzm, builder.mul(i, etzfp__goj))
        i = builder.and_(safmv__gbdlf, builder.add(i, bviu__zmbxq))
        builder.store(i, index)
        builder.store(bviu__zmbxq, photz__cdrp)
        builder.branch(rmtc__vzxew)
    with builder.goto_block(qdqkv__sdbrd):
        if for_insert:
            i = builder.load(index)
            xtznj__rbi = builder.load(brhw__cfokm)
            i = builder.select(builder.icmp_unsigned('==', xtznj__rbi,
                jrdv__ycf), i, xtznj__rbi)
            builder.store(i, index)
        builder.branch(xpm__dwo)
    with builder.goto_block(marsp__iwqz):
        builder.branch(xpm__dwo)
    builder.position_at_end(xpm__dwo)
    fybuz__kbv = builder.phi(ir.IntType(1), 'found')
    fybuz__kbv.add_incoming(cgutils.true_bit, marsp__iwqz)
    fybuz__kbv.add_incoming(cgutils.false_bit, qdqkv__sdbrd)
    return fybuz__kbv, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    xng__ydjwz = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    reuvc__tnlww = payload.used
    esyzm__vkuzm = ir.Constant(reuvc__tnlww.type, 1)
    reuvc__tnlww = payload.used = builder.add(reuvc__tnlww, esyzm__vkuzm)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, xng__ydjwz), likely=True):
        payload.fill = builder.add(payload.fill, esyzm__vkuzm)
    if do_resize:
        self.upsize(reuvc__tnlww)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    fybuz__kbv, i = payload._lookup(item, h, for_insert=True)
    ytwks__dcul = builder.not_(fybuz__kbv)
    with builder.if_then(ytwks__dcul):
        entry = payload.get_entry(i)
        xng__ydjwz = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        reuvc__tnlww = payload.used
        esyzm__vkuzm = ir.Constant(reuvc__tnlww.type, 1)
        reuvc__tnlww = payload.used = builder.add(reuvc__tnlww, esyzm__vkuzm)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, xng__ydjwz), likely=True):
            payload.fill = builder.add(payload.fill, esyzm__vkuzm)
        if do_resize:
            self.upsize(reuvc__tnlww)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    reuvc__tnlww = payload.used
    esyzm__vkuzm = ir.Constant(reuvc__tnlww.type, 1)
    reuvc__tnlww = payload.used = self._builder.sub(reuvc__tnlww, esyzm__vkuzm)
    if do_resize:
        self.downsize(reuvc__tnlww)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    zpx__ebq = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, zpx__ebq)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    ycjs__ujic = payload
    sfd__elend = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(sfd__elend), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with ycjs__ujic._iterate() as ucnmo__fmtx:
        entry = ucnmo__fmtx.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(ycjs__ujic.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as ucnmo__fmtx:
        entry = ucnmo__fmtx.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    sfd__elend = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(sfd__elend), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    sfd__elend = cgutils.alloca_once_value(builder, cgutils.true_bit)
    fztbr__rxis = context.get_value_type(types.intp)
    its__torsv = ir.Constant(fztbr__rxis, 0)
    esyzm__vkuzm = ir.Constant(fztbr__rxis, 1)
    milm__yjd = context.get_data_type(types.SetPayload(self._ty))
    dqcck__gbkt = context.get_abi_sizeof(milm__yjd)
    iftxh__rvfs = self._entrysize
    dqcck__gbkt -= iftxh__rvfs
    pzrk__rhs, hgvfn__mlyws = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(fztbr__rxis, iftxh__rvfs), ir.Constant(
        fztbr__rxis, dqcck__gbkt))
    with builder.if_then(hgvfn__mlyws, likely=False):
        builder.store(cgutils.false_bit, sfd__elend)
    with builder.if_then(builder.load(sfd__elend), likely=True):
        if realloc:
            xbf__daw = self._set.meminfo
            fnsxp__ipfoo = context.nrt.meminfo_varsize_alloc(builder,
                xbf__daw, size=pzrk__rhs)
            bpuvw__hpuz = cgutils.is_null(builder, fnsxp__ipfoo)
        else:
            bqywd__irt = _imp_dtor(context, builder.module, self._ty)
            xbf__daw = context.nrt.meminfo_new_varsize_dtor(builder,
                pzrk__rhs, builder.bitcast(bqywd__irt, cgutils.voidptr_t))
            bpuvw__hpuz = cgutils.is_null(builder, xbf__daw)
        with builder.if_else(bpuvw__hpuz, likely=False) as (vijjm__dhu,
            zqz__rzg):
            with vijjm__dhu:
                builder.store(cgutils.false_bit, sfd__elend)
            with zqz__rzg:
                if not realloc:
                    self._set.meminfo = xbf__daw
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, pzrk__rhs, 255)
                payload.used = its__torsv
                payload.fill = its__torsv
                payload.finger = its__torsv
                vpoco__pwyv = builder.sub(nentries, esyzm__vkuzm)
                payload.mask = vpoco__pwyv
    return builder.load(sfd__elend)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    sfd__elend = cgutils.alloca_once_value(builder, cgutils.true_bit)
    fztbr__rxis = context.get_value_type(types.intp)
    its__torsv = ir.Constant(fztbr__rxis, 0)
    esyzm__vkuzm = ir.Constant(fztbr__rxis, 1)
    milm__yjd = context.get_data_type(types.SetPayload(self._ty))
    dqcck__gbkt = context.get_abi_sizeof(milm__yjd)
    iftxh__rvfs = self._entrysize
    dqcck__gbkt -= iftxh__rvfs
    safmv__gbdlf = src_payload.mask
    nentries = builder.add(esyzm__vkuzm, safmv__gbdlf)
    pzrk__rhs = builder.add(ir.Constant(fztbr__rxis, dqcck__gbkt), builder.
        mul(ir.Constant(fztbr__rxis, iftxh__rvfs), nentries))
    with builder.if_then(builder.load(sfd__elend), likely=True):
        bqywd__irt = _imp_dtor(context, builder.module, self._ty)
        xbf__daw = context.nrt.meminfo_new_varsize_dtor(builder, pzrk__rhs,
            builder.bitcast(bqywd__irt, cgutils.voidptr_t))
        bpuvw__hpuz = cgutils.is_null(builder, xbf__daw)
        with builder.if_else(bpuvw__hpuz, likely=False) as (vijjm__dhu,
            zqz__rzg):
            with vijjm__dhu:
                builder.store(cgutils.false_bit, sfd__elend)
            with zqz__rzg:
                self._set.meminfo = xbf__daw
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = its__torsv
                payload.mask = safmv__gbdlf
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, iftxh__rvfs)
                with src_payload._iterate() as ucnmo__fmtx:
                    context.nrt.incref(builder, self._ty.dtype, ucnmo__fmtx
                        .entry.key)
    return builder.load(sfd__elend)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    yyloz__vhbk = context.get_value_type(types.voidptr)
    xtbbz__jarzs = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [yyloz__vhbk, xtbbz__jarzs,
        yyloz__vhbk])
    urtab__mqpdo = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=urtab__mqpdo)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        plgxp__kxns = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, plgxp__kxns)
        with payload._iterate() as ucnmo__fmtx:
            entry = ucnmo__fmtx.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    eay__fkwoj, = sig.args
    jdyy__zbhwf, = args
    yek__ayv = numba.core.imputils.call_len(context, builder, eay__fkwoj,
        jdyy__zbhwf)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, yek__ayv)
    with numba.core.imputils.for_iter(context, builder, eay__fkwoj, jdyy__zbhwf
        ) as ucnmo__fmtx:
        inst.add(ucnmo__fmtx.value)
        context.nrt.decref(builder, set_type.dtype, ucnmo__fmtx.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    eay__fkwoj = sig.args[1]
    jdyy__zbhwf = args[1]
    yek__ayv = numba.core.imputils.call_len(context, builder, eay__fkwoj,
        jdyy__zbhwf)
    if yek__ayv is not None:
        fqar__mnlx = builder.add(inst.payload.used, yek__ayv)
        inst.upsize(fqar__mnlx)
    with numba.core.imputils.for_iter(context, builder, eay__fkwoj, jdyy__zbhwf
        ) as ucnmo__fmtx:
        dtsh__mcvb = context.cast(builder, ucnmo__fmtx.value, eay__fkwoj.
            dtype, inst.dtype)
        inst.add(dtsh__mcvb)
        context.nrt.decref(builder, eay__fkwoj.dtype, ucnmo__fmtx.value)
    if yek__ayv is not None:
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
    fslby__kivy = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, fslby__kivy, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    hktwz__qjs = target_context.get_executable(library, fndesc, env)
    uzpie__eebd = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=hktwz__qjs, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return uzpie__eebd


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
        eciah__udbjc = MPI.COMM_WORLD
        if eciah__udbjc.Get_rank() == 0:
            ojd__qzx = self.get_cache_path()
            os.makedirs(ojd__qzx, exist_ok=True)
            tempfile.TemporaryFile(dir=ojd__qzx).close()
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
    sxvia__knp = cgutils.create_struct_proxy(charseq.bytes_type)
    kthe__ezca = sxvia__knp(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(kthe__ezca.nitems.type, nbytes)
    kthe__ezca.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    kthe__ezca.nitems = nbytes
    kthe__ezca.itemsize = ir.Constant(kthe__ezca.itemsize.type, 1)
    kthe__ezca.data = context.nrt.meminfo_data(builder, kthe__ezca.meminfo)
    kthe__ezca.parent = cgutils.get_null_value(kthe__ezca.parent.type)
    kthe__ezca.shape = cgutils.pack_array(builder, [kthe__ezca.nitems],
        context.get_value_type(types.intp))
    kthe__ezca.strides = cgutils.pack_array(builder, [ir.Constant(
        kthe__ezca.strides.type.element, 1)], context.get_value_type(types.
        intp))
    return kthe__ezca


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
