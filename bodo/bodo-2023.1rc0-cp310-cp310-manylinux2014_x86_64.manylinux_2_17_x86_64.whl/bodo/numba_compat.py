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
    cfz__vsc = numba.core.bytecode.FunctionIdentity.from_function(func)
    toam__jgq = numba.core.interpreter.Interpreter(cfz__vsc)
    denq__mhsan = numba.core.bytecode.ByteCode(func_id=cfz__vsc)
    func_ir = toam__jgq.interpret(denq__mhsan)
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
        nmul__xtm = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        nmul__xtm.run()
    ill__tbj = numba.core.postproc.PostProcessor(func_ir)
    ill__tbj.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, tsgmq__rbg in visit_vars_extensions.items():
        if isinstance(stmt, t):
            tsgmq__rbg(stmt, callback, cbdata)
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
    gur__nix = ['ravel', 'transpose', 'reshape']
    for omarb__awz in blocks.values():
        for nvo__uvrd in omarb__awz.body:
            if type(nvo__uvrd) in alias_analysis_extensions:
                tsgmq__rbg = alias_analysis_extensions[type(nvo__uvrd)]
                tsgmq__rbg(nvo__uvrd, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(nvo__uvrd, ir.Assign):
                hipcv__kjya = nvo__uvrd.value
                vus__ptpbi = nvo__uvrd.target.name
                if is_immutable_type(vus__ptpbi, typemap):
                    continue
                if isinstance(hipcv__kjya, ir.Var
                    ) and vus__ptpbi != hipcv__kjya.name:
                    _add_alias(vus__ptpbi, hipcv__kjya.name, alias_map,
                        arg_aliases)
                if isinstance(hipcv__kjya, ir.Expr) and (hipcv__kjya.op ==
                    'cast' or hipcv__kjya.op in ['getitem', 'static_getitem']):
                    _add_alias(vus__ptpbi, hipcv__kjya.value.name,
                        alias_map, arg_aliases)
                if isinstance(hipcv__kjya, ir.Expr
                    ) and hipcv__kjya.op == 'inplace_binop':
                    _add_alias(vus__ptpbi, hipcv__kjya.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(hipcv__kjya, ir.Expr
                    ) and hipcv__kjya.op == 'getattr' and hipcv__kjya.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(vus__ptpbi, hipcv__kjya.value.name,
                        alias_map, arg_aliases)
                if isinstance(hipcv__kjya, ir.Expr
                    ) and hipcv__kjya.op == 'getattr' and hipcv__kjya.attr not in [
                    'shape'] and hipcv__kjya.value.name in arg_aliases:
                    _add_alias(vus__ptpbi, hipcv__kjya.value.name,
                        alias_map, arg_aliases)
                if isinstance(hipcv__kjya, ir.Expr
                    ) and hipcv__kjya.op == 'getattr' and hipcv__kjya.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(vus__ptpbi, hipcv__kjya.value.name,
                        alias_map, arg_aliases)
                if isinstance(hipcv__kjya, ir.Expr) and hipcv__kjya.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(vus__ptpbi, typemap):
                    for jxplm__ekr in hipcv__kjya.items:
                        _add_alias(vus__ptpbi, jxplm__ekr.name, alias_map,
                            arg_aliases)
                if isinstance(hipcv__kjya, ir.Expr
                    ) and hipcv__kjya.op == 'call':
                    mxps__kebe = guard(find_callname, func_ir, hipcv__kjya,
                        typemap)
                    if mxps__kebe is None:
                        continue
                    vhxs__voqdj, auu__tdepr = mxps__kebe
                    if mxps__kebe in alias_func_extensions:
                        utw__dgjon = alias_func_extensions[mxps__kebe]
                        utw__dgjon(vus__ptpbi, hipcv__kjya.args, alias_map,
                            arg_aliases)
                    if auu__tdepr == 'numpy' and vhxs__voqdj in gur__nix:
                        _add_alias(vus__ptpbi, hipcv__kjya.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(auu__tdepr, ir.Var
                        ) and vhxs__voqdj in gur__nix:
                        _add_alias(vus__ptpbi, auu__tdepr.name, alias_map,
                            arg_aliases)
    haoh__myw = copy.deepcopy(alias_map)
    for jxplm__ekr in haoh__myw:
        for jmw__fmcez in haoh__myw[jxplm__ekr]:
            alias_map[jxplm__ekr] |= alias_map[jmw__fmcez]
        for jmw__fmcez in haoh__myw[jxplm__ekr]:
            alias_map[jmw__fmcez] = alias_map[jxplm__ekr]
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
    dyvcz__afpq = compute_cfg_from_blocks(func_ir.blocks)
    xgzko__vne = compute_use_defs(func_ir.blocks)
    xfxgr__goz = compute_live_map(dyvcz__afpq, func_ir.blocks, xgzko__vne.
        usemap, xgzko__vne.defmap)
    gbkl__wnhj = True
    while gbkl__wnhj:
        gbkl__wnhj = False
        for label, block in func_ir.blocks.items():
            lives = {jxplm__ekr.name for jxplm__ekr in block.terminator.
                list_vars()}
            for araxq__nzj, dfig__ial in dyvcz__afpq.successors(label):
                lives |= xfxgr__goz[araxq__nzj]
            deiw__ihyy = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    vus__ptpbi = stmt.target
                    rurqw__eyel = stmt.value
                    if vus__ptpbi.name not in lives:
                        if isinstance(rurqw__eyel, ir.Expr
                            ) and rurqw__eyel.op == 'make_function':
                            continue
                        if isinstance(rurqw__eyel, ir.Expr
                            ) and rurqw__eyel.op == 'getattr':
                            continue
                        if isinstance(rurqw__eyel, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(vus__ptpbi,
                            None), types.Function):
                            continue
                        if isinstance(rurqw__eyel, ir.Expr
                            ) and rurqw__eyel.op == 'build_map':
                            continue
                        if isinstance(rurqw__eyel, ir.Expr
                            ) and rurqw__eyel.op == 'build_tuple':
                            continue
                        if isinstance(rurqw__eyel, ir.Expr
                            ) and rurqw__eyel.op == 'binop':
                            continue
                        if isinstance(rurqw__eyel, ir.Expr
                            ) and rurqw__eyel.op == 'unary':
                            continue
                        if isinstance(rurqw__eyel, ir.Expr
                            ) and rurqw__eyel.op in ('static_getitem',
                            'getitem'):
                            continue
                    if isinstance(rurqw__eyel, ir.Var
                        ) and vus__ptpbi.name == rurqw__eyel.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    unru__nseh = analysis.ir_extension_usedefs[type(stmt)]
                    joe__qayf, ndhv__jsmgy = unru__nseh(stmt)
                    lives -= ndhv__jsmgy
                    lives |= joe__qayf
                else:
                    lives |= {jxplm__ekr.name for jxplm__ekr in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        djaev__rhz = set()
                        if isinstance(rurqw__eyel, ir.Expr):
                            djaev__rhz = {jxplm__ekr.name for jxplm__ekr in
                                rurqw__eyel.list_vars()}
                        if vus__ptpbi.name not in djaev__rhz:
                            lives.remove(vus__ptpbi.name)
                deiw__ihyy.append(stmt)
            deiw__ihyy.reverse()
            if len(block.body) != len(deiw__ihyy):
                gbkl__wnhj = True
            block.body = deiw__ihyy


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    ywbxh__toy = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (ywbxh__toy,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    giab__iwdjj = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), giab__iwdjj)


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
            for abd__rzxf in fnty.templates:
                self._inline_overloads.update(abd__rzxf._inline_overloads)
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
    giab__iwdjj = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), giab__iwdjj)
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
    stxu__okwcz, ahl__zpxt = self._get_impl(args, kws)
    if stxu__okwcz is None:
        return
    yjsvq__inthy = types.Dispatcher(stxu__okwcz)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        ytml__shzhw = stxu__okwcz._compiler
        flags = compiler.Flags()
        iqzpo__gzkqy = ytml__shzhw.targetdescr.typing_context
        jxzgc__irbun = ytml__shzhw.targetdescr.target_context
        ygq__xshj = ytml__shzhw.pipeline_class(iqzpo__gzkqy, jxzgc__irbun,
            None, None, None, flags, None)
        kexeu__zkylg = InlineWorker(iqzpo__gzkqy, jxzgc__irbun, ytml__shzhw
            .locals, ygq__xshj, flags, None)
        pet__vgji = yjsvq__inthy.dispatcher.get_call_template
        abd__rzxf, vmf__vtout, ajzjk__uyygo, kws = pet__vgji(ahl__zpxt, kws)
        if ajzjk__uyygo in self._inline_overloads:
            return self._inline_overloads[ajzjk__uyygo]['iinfo'].signature
        ir = kexeu__zkylg.run_untyped_passes(yjsvq__inthy.dispatcher.
            py_func, enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, jxzgc__irbun, ir, ajzjk__uyygo, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, ajzjk__uyygo, None)
        self._inline_overloads[sig.args] = {'folded_args': ajzjk__uyygo}
        aubi__anlte = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = aubi__anlte
        if not self._inline.is_always_inline:
            sig = yjsvq__inthy.get_call_type(self.context, ahl__zpxt, kws)
            self._compiled_overloads[sig.args] = yjsvq__inthy.get_overload(sig)
        mgz__wadii = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': ajzjk__uyygo,
            'iinfo': mgz__wadii}
    else:
        sig = yjsvq__inthy.get_call_type(self.context, ahl__zpxt, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = yjsvq__inthy.get_overload(sig)
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
    ekh__mandv = [True, False]
    dhvu__wvcp = [False, True]
    hle__jvqhl = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    lhsdj__hiqj = get_local_target(context)
    dvvw__cteqg = utils.order_by_target_specificity(lhsdj__hiqj, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for uhiju__yhnk in dvvw__cteqg:
        nocva__noc = uhiju__yhnk(context)
        llmmk__jjuj = ekh__mandv if nocva__noc.prefer_literal else dhvu__wvcp
        llmmk__jjuj = [True] if getattr(nocva__noc, '_no_unliteral', False
            ) else llmmk__jjuj
        for fqkrg__ggyh in llmmk__jjuj:
            try:
                if fqkrg__ggyh:
                    sig = nocva__noc.apply(args, kws)
                else:
                    alxdx__tbfr = tuple([_unlit_non_poison(a) for a in args])
                    dsj__vwol = {zfd__ygrjl: _unlit_non_poison(jxplm__ekr) for
                        zfd__ygrjl, jxplm__ekr in kws.items()}
                    sig = nocva__noc.apply(alxdx__tbfr, dsj__vwol)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    hle__jvqhl.add_error(nocva__noc, False, e, fqkrg__ggyh)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = nocva__noc.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    ikfi__tio = getattr(nocva__noc, 'cases', None)
                    if ikfi__tio is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            ikfi__tio)
                    else:
                        msg = 'No match.'
                    hle__jvqhl.add_error(nocva__noc, True, msg, fqkrg__ggyh)
    hle__jvqhl.raise_error()


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
    abd__rzxf = self.template(context)
    sxml__igsl = None
    xckg__clu = None
    geooa__qssz = None
    llmmk__jjuj = [True, False] if abd__rzxf.prefer_literal else [False, True]
    llmmk__jjuj = [True] if getattr(abd__rzxf, '_no_unliteral', False
        ) else llmmk__jjuj
    for fqkrg__ggyh in llmmk__jjuj:
        if fqkrg__ggyh:
            try:
                geooa__qssz = abd__rzxf.apply(args, kws)
            except Exception as gppr__zrgc:
                if isinstance(gppr__zrgc, errors.ForceLiteralArg):
                    raise gppr__zrgc
                sxml__igsl = gppr__zrgc
                geooa__qssz = None
            else:
                break
        else:
            pxro__tpcfj = tuple([_unlit_non_poison(a) for a in args])
            nxsj__jcbr = {zfd__ygrjl: _unlit_non_poison(jxplm__ekr) for 
                zfd__ygrjl, jxplm__ekr in kws.items()}
            rusjv__tsx = pxro__tpcfj == args and kws == nxsj__jcbr
            if not rusjv__tsx and geooa__qssz is None:
                try:
                    geooa__qssz = abd__rzxf.apply(pxro__tpcfj, nxsj__jcbr)
                except Exception as gppr__zrgc:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        gppr__zrgc, errors.NumbaError):
                        raise gppr__zrgc
                    if isinstance(gppr__zrgc, errors.ForceLiteralArg):
                        if abd__rzxf.prefer_literal:
                            raise gppr__zrgc
                    xckg__clu = gppr__zrgc
                else:
                    break
    if geooa__qssz is None and (xckg__clu is not None or sxml__igsl is not None
        ):
        qjh__gwuqg = '- Resolution failure for {} arguments:\n{}\n'
        afz__jmeif = _termcolor.highlight(qjh__gwuqg)
        if numba.core.config.DEVELOPER_MODE:
            kwcd__jkadn = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    mztw__zud = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    mztw__zud = ['']
                fwx__meaz = '\n{}'.format(2 * kwcd__jkadn)
                fhlp__ikbeh = _termcolor.reset(fwx__meaz + fwx__meaz.join(
                    _bt_as_lines(mztw__zud)))
                return _termcolor.reset(fhlp__ikbeh)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            fxc__omb = str(e)
            fxc__omb = fxc__omb if fxc__omb else str(repr(e)) + add_bt(e)
            jmbwe__iottt = errors.TypingError(textwrap.dedent(fxc__omb))
            return afz__jmeif.format(literalness, str(jmbwe__iottt))
        import bodo
        if isinstance(sxml__igsl, bodo.utils.typing.BodoError):
            raise sxml__igsl
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', sxml__igsl) +
                nested_msg('non-literal', xckg__clu))
        else:
            if 'missing a required argument' in sxml__igsl.msg:
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
            raise errors.TypingError(msg, loc=sxml__igsl.loc)
    return geooa__qssz


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
    vhxs__voqdj = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=vhxs__voqdj)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            odtz__qod = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), odtz__qod)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    rfphd__dob = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            rfphd__dob.append(types.Omitted(a.value))
        else:
            rfphd__dob.append(self.typeof_pyval(a))
    zxl__gboy = None
    try:
        error = None
        zxl__gboy = self.compile(tuple(rfphd__dob))
    except errors.ForceLiteralArg as e:
        smywb__jfym = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if smywb__jfym:
            ljj__gilz = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            bvoss__gxao = ', '.join('Arg #{} is {}'.format(i, args[i]) for
                i in sorted(smywb__jfym))
            raise errors.CompilerError(ljj__gilz.format(bvoss__gxao))
        ahl__zpxt = []
        try:
            for i, jxplm__ekr in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        ahl__zpxt.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        ahl__zpxt.append(types.literal(args[i]))
                else:
                    ahl__zpxt.append(args[i])
            args = ahl__zpxt
        except (OSError, FileNotFoundError) as stfya__hijok:
            error = FileNotFoundError(str(stfya__hijok) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                zxl__gboy = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        egf__exsrl = []
        for i, irc__ppfd in enumerate(args):
            val = irc__ppfd.value if isinstance(irc__ppfd, numba.core.
                dispatcher.OmittedArg) else irc__ppfd
            try:
                fqogg__adhj = typeof(val, Purpose.argument)
            except ValueError as bilkm__mhjbp:
                egf__exsrl.append((i, str(bilkm__mhjbp)))
            else:
                if fqogg__adhj is None:
                    egf__exsrl.append((i,
                        f'cannot determine Numba type of value {val}'))
        if egf__exsrl:
            txw__vggu = '\n'.join(f'- argument {i}: {lrmi__ldu}' for i,
                lrmi__ldu in egf__exsrl)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{txw__vggu}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                bdqlw__hbff = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                fesan__zgmv = False
                for ohz__ezgy in bdqlw__hbff:
                    if ohz__ezgy in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        fesan__zgmv = True
                        break
                if not fesan__zgmv:
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
                odtz__qod = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), odtz__qod)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return zxl__gboy


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
    for knbf__nmth in cres.library._codegen._engine._defined_symbols:
        if knbf__nmth.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in knbf__nmth and (
            'bodo_gb_udf_update_local' in knbf__nmth or 
            'bodo_gb_udf_combine' in knbf__nmth or 'bodo_gb_udf_eval' in
            knbf__nmth or 'bodo_gb_apply_general_udfs' in knbf__nmth):
            gb_agg_cfunc_addr[knbf__nmth
                ] = cres.library.get_pointer_to_function(knbf__nmth)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for knbf__nmth in cres.library._codegen._engine._defined_symbols:
        if knbf__nmth.startswith('cfunc') and ('get_join_cond_addr' not in
            knbf__nmth or 'bodo_join_gen_cond' in knbf__nmth):
            join_gen_cond_cfunc_addr[knbf__nmth
                ] = cres.library.get_pointer_to_function(knbf__nmth)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    stxu__okwcz = self._get_dispatcher_for_current_target()
    if stxu__okwcz is not self:
        return stxu__okwcz.compile(sig)
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
            kwzo__och = self.overloads.get(tuple(args))
            if kwzo__och is not None:
                return kwzo__och.entry_point
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
            thjwz__zoun = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=thjwz__zoun):
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
                ihwcr__xiymg = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in ihwcr__xiymg:
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
    bld__qpdld = self._final_module
    oirh__tsw = []
    xcfos__csv = 0
    for fn in bld__qpdld.functions:
        xcfos__csv += 1
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
            oirh__tsw.append(fn.name)
    if xcfos__csv == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if oirh__tsw:
        bld__qpdld = bld__qpdld.clone()
        for name in oirh__tsw:
            bld__qpdld.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = bld__qpdld
    return bld__qpdld


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
    for ixcxo__ugp in self.constraints:
        loc = ixcxo__ugp.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                ixcxo__ugp(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                cme__uon = numba.core.errors.TypingError(str(e), loc=
                    ixcxo__ugp.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(cme__uon, e))
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
                    cme__uon = numba.core.errors.TypingError(msg.format(con
                        =ixcxo__ugp, err=str(e)), loc=ixcxo__ugp.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(cme__uon, e))
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
    for mqwot__vuym in self._failures.values():
        for qjus__dvzkd in mqwot__vuym:
            if isinstance(qjus__dvzkd.error, ForceLiteralArg):
                raise qjus__dvzkd.error
            if isinstance(qjus__dvzkd.error, bodo.utils.typing.BodoError):
                raise qjus__dvzkd.error
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
    bqe__dmo = False
    deiw__ihyy = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        kxst__bnfyz = set()
        ldse__tdb = lives & alias_set
        for jxplm__ekr in ldse__tdb:
            kxst__bnfyz |= alias_map[jxplm__ekr]
        lives_n_aliases = lives | kxst__bnfyz | arg_aliases
        if type(stmt) in remove_dead_extensions:
            tsgmq__rbg = remove_dead_extensions[type(stmt)]
            stmt = tsgmq__rbg(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                bqe__dmo = True
                continue
        if isinstance(stmt, ir.Assign):
            vus__ptpbi = stmt.target
            rurqw__eyel = stmt.value
            if vus__ptpbi.name not in lives:
                if has_no_side_effect(rurqw__eyel, lives_n_aliases, call_table
                    ):
                    bqe__dmo = True
                    continue
                if isinstance(rurqw__eyel, ir.Expr
                    ) and rurqw__eyel.op == 'call' and call_table[rurqw__eyel
                    .func.name] == ['astype']:
                    fmzh__vowz = guard(get_definition, func_ir, rurqw__eyel
                        .func)
                    if (fmzh__vowz is not None and fmzh__vowz.op ==
                        'getattr' and isinstance(typemap[fmzh__vowz.value.
                        name], types.Array) and fmzh__vowz.attr == 'astype'):
                        bqe__dmo = True
                        continue
            if saved_array_analysis and vus__ptpbi.name in lives and is_expr(
                rurqw__eyel, 'getattr'
                ) and rurqw__eyel.attr == 'shape' and is_array_typ(typemap[
                rurqw__eyel.value.name]
                ) and rurqw__eyel.value.name not in lives:
                fipga__qjgm = {jxplm__ekr: zfd__ygrjl for zfd__ygrjl,
                    jxplm__ekr in func_ir.blocks.items()}
                if block in fipga__qjgm:
                    label = fipga__qjgm[block]
                    wkal__excj = saved_array_analysis.get_equiv_set(label)
                    gyrh__lxrfu = wkal__excj.get_equiv_set(rurqw__eyel.value)
                    if gyrh__lxrfu is not None:
                        for jxplm__ekr in gyrh__lxrfu:
                            if jxplm__ekr.endswith('#0'):
                                jxplm__ekr = jxplm__ekr[:-2]
                            if jxplm__ekr in typemap and is_array_typ(typemap
                                [jxplm__ekr]) and jxplm__ekr in lives:
                                rurqw__eyel.value = ir.Var(rurqw__eyel.
                                    value.scope, jxplm__ekr, rurqw__eyel.
                                    value.loc)
                                bqe__dmo = True
                                break
            if isinstance(rurqw__eyel, ir.Var
                ) and vus__ptpbi.name == rurqw__eyel.name:
                bqe__dmo = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                bqe__dmo = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            unru__nseh = analysis.ir_extension_usedefs[type(stmt)]
            joe__qayf, ndhv__jsmgy = unru__nseh(stmt)
            lives -= ndhv__jsmgy
            lives |= joe__qayf
        else:
            lives |= {jxplm__ekr.name for jxplm__ekr in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                djaev__rhz = set()
                if isinstance(rurqw__eyel, ir.Expr):
                    djaev__rhz = {jxplm__ekr.name for jxplm__ekr in
                        rurqw__eyel.list_vars()}
                if vus__ptpbi.name not in djaev__rhz:
                    lives.remove(vus__ptpbi.name)
        deiw__ihyy.append(stmt)
    deiw__ihyy.reverse()
    block.body = deiw__ihyy
    return bqe__dmo


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            yjnic__qrb, = args
            if isinstance(yjnic__qrb, types.IterableType):
                dtype = yjnic__qrb.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), yjnic__qrb)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    rdala__can = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (rdala__can, self.dtype)
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
        except LiteralTypingError as odxnv__cll:
            return
    try:
        return literal(value)
    except LiteralTypingError as odxnv__cll:
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
        ybh__cfs = py_func.__qualname__
    except AttributeError as odxnv__cll:
        ybh__cfs = py_func.__name__
    jyi__eert = inspect.getfile(py_func)
    for cls in self._locator_classes:
        sonl__ecmjp = cls.from_function(py_func, jyi__eert)
        if sonl__ecmjp is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (ybh__cfs, jyi__eert))
    self._locator = sonl__ecmjp
    dqwws__omil = inspect.getfile(py_func)
    fdjv__zqncb = os.path.splitext(os.path.basename(dqwws__omil))[0]
    if jyi__eert.startswith('<ipython-'):
        undx__aii = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', fdjv__zqncb, count=1)
        if undx__aii == fdjv__zqncb:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        fdjv__zqncb = undx__aii
    hrqqc__gaev = '%s.%s' % (fdjv__zqncb, ybh__cfs)
    bkxly__olgg = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(hrqqc__gaev, bkxly__olgg
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    mro__utp = list(filter(lambda a: self._istuple(a.name), args))
    if len(mro__utp) == 2 and fn.__name__ == 'add':
        rqtp__jnr = self.typemap[mro__utp[0].name]
        izs__thaj = self.typemap[mro__utp[1].name]
        if rqtp__jnr.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                mro__utp[1]))
        if izs__thaj.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                mro__utp[0]))
        try:
            wvh__ovmci = [equiv_set.get_shape(x) for x in mro__utp]
            if None in wvh__ovmci:
                return None
            afycb__qej = sum(wvh__ovmci, ())
            return ArrayAnalysis.AnalyzeResult(shape=afycb__qej)
        except GuardException as odxnv__cll:
            return None
    wgvkt__jvwzd = list(filter(lambda a: self._isarray(a.name), args))
    require(len(wgvkt__jvwzd) > 0)
    tkbbp__szozl = [x.name for x in wgvkt__jvwzd]
    pse__fdx = [self.typemap[x.name].ndim for x in wgvkt__jvwzd]
    mgs__qxidk = max(pse__fdx)
    require(mgs__qxidk > 0)
    wvh__ovmci = [equiv_set.get_shape(x) for x in wgvkt__jvwzd]
    if any(a is None for a in wvh__ovmci):
        return ArrayAnalysis.AnalyzeResult(shape=wgvkt__jvwzd[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, wgvkt__jvwzd))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, wvh__ovmci,
        tkbbp__szozl)


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
    wqnc__bcxke = code_obj.code
    jadq__gyxql = len(wqnc__bcxke.co_freevars)
    xacj__jqd = wqnc__bcxke.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        nqr__dyz, op = ir_utils.find_build_sequence(caller_ir, code_obj.closure
            )
        assert op == 'build_tuple'
        xacj__jqd = [jxplm__ekr.name for jxplm__ekr in nqr__dyz]
    kwdxm__ticis = caller_ir.func_id.func.__globals__
    try:
        kwdxm__ticis = getattr(code_obj, 'globals', kwdxm__ticis)
    except KeyError as odxnv__cll:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    nuln__ulva = []
    for x in xacj__jqd:
        try:
            opkv__xhhj = caller_ir.get_definition(x)
        except KeyError as odxnv__cll:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(opkv__xhhj, (ir.Const, ir.Global, ir.FreeVar)):
            val = opkv__xhhj.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                ywbxh__toy = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                kwdxm__ticis[ywbxh__toy] = bodo.jit(distributed=False)(val)
                kwdxm__ticis[ywbxh__toy].is_nested_func = True
                val = ywbxh__toy
            if isinstance(val, CPUDispatcher):
                ywbxh__toy = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                kwdxm__ticis[ywbxh__toy] = val
                val = ywbxh__toy
            nuln__ulva.append(val)
        elif isinstance(opkv__xhhj, ir.Expr
            ) and opkv__xhhj.op == 'make_function':
            maa__akqqc = convert_code_obj_to_function(opkv__xhhj, caller_ir)
            ywbxh__toy = ir_utils.mk_unique_var('nested_func').replace('.', '_'
                )
            kwdxm__ticis[ywbxh__toy] = bodo.jit(distributed=False)(maa__akqqc)
            kwdxm__ticis[ywbxh__toy].is_nested_func = True
            nuln__ulva.append(ywbxh__toy)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    owlx__eglw = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        nuln__ulva)])
    xbd__ptzh = ','.join([('c_%d' % i) for i in range(jadq__gyxql)])
    mvc__lhzt = list(wqnc__bcxke.co_varnames)
    iduqf__bbzg = 0
    yddt__jeea = wqnc__bcxke.co_argcount
    ardc__ehke = caller_ir.get_definition(code_obj.defaults)
    if ardc__ehke is not None:
        if isinstance(ardc__ehke, tuple):
            d = [caller_ir.get_definition(x).value for x in ardc__ehke]
            zjiih__ybhrd = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in ardc__ehke.items]
            zjiih__ybhrd = tuple(d)
        iduqf__bbzg = len(zjiih__ybhrd)
    qeh__umpx = yddt__jeea - iduqf__bbzg
    wcrk__spcun = ','.join([('%s' % mvc__lhzt[i]) for i in range(qeh__umpx)])
    if iduqf__bbzg:
        yuniz__rrdpy = [('%s = %s' % (mvc__lhzt[i + qeh__umpx],
            zjiih__ybhrd[i])) for i in range(iduqf__bbzg)]
        wcrk__spcun += ', '
        wcrk__spcun += ', '.join(yuniz__rrdpy)
    return _create_function_from_code_obj(wqnc__bcxke, owlx__eglw,
        wcrk__spcun, xbd__ptzh, kwdxm__ticis)


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
    for atz__iyyfr, (mpbrx__dheq, kuyd__aau) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % kuyd__aau)
            yrvg__zti = _pass_registry.get(mpbrx__dheq).pass_inst
            if isinstance(yrvg__zti, CompilerPass):
                self._runPass(atz__iyyfr, yrvg__zti, state)
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
                    pipeline_name, kuyd__aau)
                ovi__bewg = self._patch_error(msg, e)
                raise ovi__bewg
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
    hwaaw__puh = None
    ndhv__jsmgy = {}

    def lookup(var, already_seen, varonly=True):
        val = ndhv__jsmgy.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    wxnu__nfq = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        vus__ptpbi = stmt.target
        rurqw__eyel = stmt.value
        ndhv__jsmgy[vus__ptpbi.name] = rurqw__eyel
        if isinstance(rurqw__eyel, ir.Var) and rurqw__eyel.name in ndhv__jsmgy:
            rurqw__eyel = lookup(rurqw__eyel, set())
        if isinstance(rurqw__eyel, ir.Expr):
            uue__lztaw = set(lookup(jxplm__ekr, set(), True).name for
                jxplm__ekr in rurqw__eyel.list_vars())
            if name in uue__lztaw:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(rurqw__eyel)]
                oot__qjr = [x for x, qzqc__gqif in args if qzqc__gqif.name !=
                    name]
                args = [(x, qzqc__gqif) for x, qzqc__gqif in args if x !=
                    qzqc__gqif.name]
                amec__rykx = dict(args)
                if len(oot__qjr) == 1:
                    amec__rykx[oot__qjr[0]] = ir.Var(vus__ptpbi.scope, name +
                        '#init', vus__ptpbi.loc)
                replace_vars_inner(rurqw__eyel, amec__rykx)
                hwaaw__puh = nodes[i:]
                break
    return hwaaw__puh


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
        fioin__kzjqx = expand_aliases({jxplm__ekr.name for jxplm__ekr in
            stmt.list_vars()}, alias_map, arg_aliases)
        qszos__hsnz = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        wsvr__szhu = expand_aliases({jxplm__ekr.name for jxplm__ekr in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        cjrvq__hjv = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(qszos__hsnz & wsvr__szhu | cjrvq__hjv & fioin__kzjqx) == 0:
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
    hsm__ggui = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            hsm__ggui.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                hsm__ggui.update(get_parfor_writes(stmt, func_ir))
    return hsm__ggui


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    hsm__ggui = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        hsm__ggui.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        hsm__ggui = {jxplm__ekr.name for jxplm__ekr in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        hsm__ggui = {jxplm__ekr.name for jxplm__ekr in stmt.get_live_out_vars()
            }
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            hsm__ggui.update({jxplm__ekr.name for jxplm__ekr in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        mxps__kebe = guard(find_callname, func_ir, stmt.value)
        if mxps__kebe in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'copy_array_element', 'bodo.libs.array_kernels'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext'), (
            'tuple_list_to_array', 'bodo.utils.utils')):
            hsm__ggui.add(stmt.value.args[0].name)
        if mxps__kebe == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            hsm__ggui.add(stmt.value.args[1].name)
    return hsm__ggui


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
        tsgmq__rbg = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        bbnx__anrgl = tsgmq__rbg.format(self, msg)
        self.args = bbnx__anrgl,
    else:
        tsgmq__rbg = _termcolor.errmsg('{0}')
        bbnx__anrgl = tsgmq__rbg.format(self)
        self.args = bbnx__anrgl,
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
        for flelx__ren in options['distributed']:
            dist_spec[flelx__ren] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for flelx__ren in options['distributed_block']:
            dist_spec[flelx__ren] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    tkmaq__wve = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, idgw__gtfvq in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(idgw__gtfvq)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    lyidw__abb = {}
    for fum__msbzx in reversed(inspect.getmro(cls)):
        lyidw__abb.update(fum__msbzx.__dict__)
    yhjx__byc, hise__rqex, rdk__ntrw, nrow__ndnfo = {}, {}, {}, {}
    for zfd__ygrjl, jxplm__ekr in lyidw__abb.items():
        if isinstance(jxplm__ekr, pytypes.FunctionType):
            yhjx__byc[zfd__ygrjl] = jxplm__ekr
        elif isinstance(jxplm__ekr, property):
            hise__rqex[zfd__ygrjl] = jxplm__ekr
        elif isinstance(jxplm__ekr, staticmethod):
            rdk__ntrw[zfd__ygrjl] = jxplm__ekr
        else:
            nrow__ndnfo[zfd__ygrjl] = jxplm__ekr
    adp__jopmu = (set(yhjx__byc) | set(hise__rqex) | set(rdk__ntrw)) & set(spec
        )
    if adp__jopmu:
        raise NameError('name shadowing: {0}'.format(', '.join(adp__jopmu)))
    xdbj__odkqa = nrow__ndnfo.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(nrow__ndnfo)
    if nrow__ndnfo:
        msg = 'class members are not yet supported: {0}'
        syvhy__yrsjy = ', '.join(nrow__ndnfo.keys())
        raise TypeError(msg.format(syvhy__yrsjy))
    for zfd__ygrjl, jxplm__ekr in hise__rqex.items():
        if jxplm__ekr.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(zfd__ygrjl))
    jit_methods = {zfd__ygrjl: bodo.jit(returns_maybe_distributed=
        tkmaq__wve)(jxplm__ekr) for zfd__ygrjl, jxplm__ekr in yhjx__byc.items()
        }
    jit_props = {}
    for zfd__ygrjl, jxplm__ekr in hise__rqex.items():
        giab__iwdjj = {}
        if jxplm__ekr.fget:
            giab__iwdjj['get'] = bodo.jit(jxplm__ekr.fget)
        if jxplm__ekr.fset:
            giab__iwdjj['set'] = bodo.jit(jxplm__ekr.fset)
        jit_props[zfd__ygrjl] = giab__iwdjj
    jit_static_methods = {zfd__ygrjl: bodo.jit(jxplm__ekr.__func__) for 
        zfd__ygrjl, jxplm__ekr in rdk__ntrw.items()}
    rncz__bdb = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    lzrm__mha = dict(class_type=rncz__bdb, __doc__=xdbj__odkqa)
    lzrm__mha.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), lzrm__mha)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, rncz__bdb)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(rncz__bdb, typingctx, targetctx).register()
    as_numba_type.register(cls, rncz__bdb.instance_type)
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
    dcit__uxjp = ','.join('{0}:{1}'.format(zfd__ygrjl, jxplm__ekr) for 
        zfd__ygrjl, jxplm__ekr in struct.items())
    new__ufh = ','.join('{0}:{1}'.format(zfd__ygrjl, jxplm__ekr) for 
        zfd__ygrjl, jxplm__ekr in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), dcit__uxjp, new__ufh)
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
    yxno__ahsx = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if yxno__ahsx is None:
        return
    dwstv__lfj, wzx__vjqna = yxno__ahsx
    for a in itertools.chain(dwstv__lfj, wzx__vjqna.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, dwstv__lfj, wzx__vjqna)
    except ForceLiteralArg as e:
        bbc__tgz = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(bbc__tgz, self.kws)
        xcm__ymjp = set()
        inbd__parnz = set()
        omc__liw = {}
        for atz__iyyfr in e.requested_args:
            vltu__kuka = typeinfer.func_ir.get_definition(folded[atz__iyyfr])
            if isinstance(vltu__kuka, ir.Arg):
                xcm__ymjp.add(vltu__kuka.index)
                if vltu__kuka.index in e.file_infos:
                    omc__liw[vltu__kuka.index] = e.file_infos[vltu__kuka.index]
            else:
                inbd__parnz.add(atz__iyyfr)
        if inbd__parnz:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif xcm__ymjp:
            raise ForceLiteralArg(xcm__ymjp, loc=self.loc, file_infos=omc__liw)
    if sig is None:
        dpfz__rff = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in dwstv__lfj]
        args += [('%s=%s' % (zfd__ygrjl, jxplm__ekr)) for zfd__ygrjl,
            jxplm__ekr in sorted(wzx__vjqna.items())]
        mkj__fxu = dpfz__rff.format(fnty, ', '.join(map(str, args)))
        xhajh__kutze = context.explain_function_type(fnty)
        msg = '\n'.join([mkj__fxu, xhajh__kutze])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        ofzaj__fadv = context.unify_pairs(sig.recvr, fnty.this)
        if ofzaj__fadv is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if ofzaj__fadv is not None and ofzaj__fadv.is_precise():
            ajbig__ayhat = fnty.copy(this=ofzaj__fadv)
            typeinfer.propagate_refined_type(self.func, ajbig__ayhat)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            jpj__ept = target.getone()
            if context.unify_pairs(jpj__ept, sig.return_type) == jpj__ept:
                sig = sig.replace(return_type=jpj__ept)
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
        ljj__gilz = '*other* must be a {} but got a {} instead'
        raise TypeError(ljj__gilz.format(ForceLiteralArg, type(other)))
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
    lwi__knfpr = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for zfd__ygrjl, jxplm__ekr in kwargs.items():
        jncrs__fdb = None
        try:
            hpna__paiht = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[hpna__paiht.name] = [jxplm__ekr]
            jncrs__fdb = get_const_value_inner(func_ir, hpna__paiht)
            func_ir._definitions.pop(hpna__paiht.name)
            if isinstance(jncrs__fdb, str):
                jncrs__fdb = sigutils._parse_signature_string(jncrs__fdb)
            if isinstance(jncrs__fdb, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {zfd__ygrjl} is annotated as type class {jncrs__fdb}."""
                    )
            assert isinstance(jncrs__fdb, types.Type)
            if isinstance(jncrs__fdb, (types.List, types.Set)):
                jncrs__fdb = jncrs__fdb.copy(reflected=False)
            lwi__knfpr[zfd__ygrjl] = jncrs__fdb
        except BodoError as odxnv__cll:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(jncrs__fdb, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(jxplm__ekr, ir.Global):
                    msg = f'Global {jxplm__ekr.name!r} is not defined.'
                if isinstance(jxplm__ekr, ir.FreeVar):
                    msg = f'Freevar {jxplm__ekr.name!r} is not defined.'
            if isinstance(jxplm__ekr, ir.Expr) and jxplm__ekr.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=zfd__ygrjl, msg=msg, loc=loc)
    for name, typ in lwi__knfpr.items():
        self._legalize_arg_type(name, typ, loc)
    return lwi__knfpr


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
    arak__vihc = inst.arg
    assert arak__vihc > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(arak__vihc)]))
    tmps = [state.make_temp() for _ in range(arak__vihc - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    iao__svw = ir.Global('format', format, loc=self.loc)
    self.store(value=iao__svw, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    okgxa__uhxq = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=okgxa__uhxq, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    arak__vihc = inst.arg
    assert arak__vihc > 0, 'invalid BUILD_STRING count'
    lckb__xguh = self.get(strings[0])
    for other, ulka__ijxw in zip(strings[1:], tmps):
        other = self.get(other)
        hipcv__kjya = ir.Expr.binop(operator.add, lhs=lckb__xguh, rhs=other,
            loc=self.loc)
        self.store(hipcv__kjya, ulka__ijxw)
        lckb__xguh = self.get(ulka__ijxw)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    liwa__tffk = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, liwa__tffk])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    ckst__aur = mk_unique_var(f'{var_name}')
    brvdn__uqmob = ckst__aur.replace('<', '_').replace('>', '_')
    brvdn__uqmob = brvdn__uqmob.replace('.', '_').replace('$', '_v')
    return brvdn__uqmob


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
                nxpp__tavvn = get_overload_const_str(val2)
                if nxpp__tavvn != 'ns':
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
        dkpak__gbee = states['defmap']
        if len(dkpak__gbee) == 0:
            kjux__yspo = assign.target
            numba.core.ssa._logger.debug('first assign: %s', kjux__yspo)
            if kjux__yspo.name not in scope.localvars:
                kjux__yspo = scope.define(assign.target.name, loc=assign.loc)
        else:
            kjux__yspo = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=kjux__yspo, value=assign.value, loc=
            assign.loc)
        dkpak__gbee[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    sko__zdlsd = []
    for zfd__ygrjl, jxplm__ekr in typing.npydecl.registry.globals:
        if zfd__ygrjl == func:
            sko__zdlsd.append(jxplm__ekr)
    for zfd__ygrjl, jxplm__ekr in typing.templates.builtin_registry.globals:
        if zfd__ygrjl == func:
            sko__zdlsd.append(jxplm__ekr)
    if len(sko__zdlsd) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return sko__zdlsd


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    tgv__sskbd = {}
    ugau__dvzxc = find_topo_order(blocks)
    flg__azls = {}
    for label in ugau__dvzxc:
        block = blocks[label]
        deiw__ihyy = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                vus__ptpbi = stmt.target.name
                rurqw__eyel = stmt.value
                if (rurqw__eyel.op == 'getattr' and rurqw__eyel.attr in
                    arr_math and isinstance(typemap[rurqw__eyel.value.name],
                    types.npytypes.Array)):
                    rurqw__eyel = stmt.value
                    cmv__xzei = rurqw__eyel.value
                    tgv__sskbd[vus__ptpbi] = cmv__xzei
                    scope = cmv__xzei.scope
                    loc = cmv__xzei.loc
                    uhjj__cfs = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[uhjj__cfs.name] = types.misc.Module(numpy)
                    dqkz__bbwx = ir.Global('np', numpy, loc)
                    hdm__hbhba = ir.Assign(dqkz__bbwx, uhjj__cfs, loc)
                    rurqw__eyel.value = uhjj__cfs
                    deiw__ihyy.append(hdm__hbhba)
                    func_ir._definitions[uhjj__cfs.name] = [dqkz__bbwx]
                    func = getattr(numpy, rurqw__eyel.attr)
                    qbu__ynrg = get_np_ufunc_typ_lst(func)
                    flg__azls[vus__ptpbi] = qbu__ynrg
                if (rurqw__eyel.op == 'call' and rurqw__eyel.func.name in
                    tgv__sskbd):
                    cmv__xzei = tgv__sskbd[rurqw__eyel.func.name]
                    haj__fvl = calltypes.pop(rurqw__eyel)
                    irlsx__fgs = haj__fvl.args[:len(rurqw__eyel.args)]
                    sfxmy__kzml = {name: typemap[jxplm__ekr.name] for name,
                        jxplm__ekr in rurqw__eyel.kws}
                    rpei__erg = flg__azls[rurqw__eyel.func.name]
                    yijzn__wzek = None
                    for azny__sre in rpei__erg:
                        try:
                            yijzn__wzek = azny__sre.get_call_type(typingctx,
                                [typemap[cmv__xzei.name]] + list(irlsx__fgs
                                ), sfxmy__kzml)
                            typemap.pop(rurqw__eyel.func.name)
                            typemap[rurqw__eyel.func.name] = azny__sre
                            calltypes[rurqw__eyel] = yijzn__wzek
                            break
                        except Exception as odxnv__cll:
                            pass
                    if yijzn__wzek is None:
                        raise TypeError(
                            f'No valid template found for {rurqw__eyel.func.name}'
                            )
                    rurqw__eyel.args = [cmv__xzei] + rurqw__eyel.args
            deiw__ihyy.append(stmt)
        block.body = deiw__ihyy


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    rog__uups = ufunc.nin
    gvh__lnj = ufunc.nout
    qeh__umpx = ufunc.nargs
    assert qeh__umpx == rog__uups + gvh__lnj
    if len(args) < rog__uups:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), rog__uups))
    if len(args) > qeh__umpx:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), qeh__umpx))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    els__ztc = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    dym__twngq = max(els__ztc)
    qghi__ddxu = args[rog__uups:]
    if not all(d == dym__twngq for d in els__ztc[rog__uups:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(wpfmm__zgcet, types.ArrayCompatible) and not
        isinstance(wpfmm__zgcet, types.Bytes) for wpfmm__zgcet in qghi__ddxu):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(wpfmm__zgcet.mutable for wpfmm__zgcet in qghi__ddxu):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    ymykf__djua = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    inqqk__zfp = None
    if dym__twngq > 0 and len(qghi__ddxu) < ufunc.nout:
        inqqk__zfp = 'C'
        zab__azk = [(x.layout if isinstance(x, types.ArrayCompatible) and 
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in zab__azk and 'F' in zab__azk:
            inqqk__zfp = 'F'
    return ymykf__djua, qghi__ddxu, dym__twngq, inqqk__zfp


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
        spxks__znnb = 'Dict.key_type cannot be of type {}'
        raise TypingError(spxks__znnb.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        spxks__znnb = 'Dict.value_type cannot be of type {}'
        raise TypingError(spxks__znnb.format(valty))
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
    wlys__iqi = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[wlys__iqi]
        return impl, args
    except KeyError as odxnv__cll:
        pass
    impl, args = self._build_impl(wlys__iqi, args, kws)
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
    gbkl__wnhj = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            qzzsz__iyee = block.body[-1]
            if isinstance(qzzsz__iyee, ir.Branch):
                if len(blocks[qzzsz__iyee.truebr].body) == 1 and len(blocks
                    [qzzsz__iyee.falsebr].body) == 1:
                    kmxc__yhaqr = blocks[qzzsz__iyee.truebr].body[0]
                    tqt__jshwf = blocks[qzzsz__iyee.falsebr].body[0]
                    if isinstance(kmxc__yhaqr, ir.Jump) and isinstance(
                        tqt__jshwf, ir.Jump
                        ) and kmxc__yhaqr.target == tqt__jshwf.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(kmxc__yhaqr
                            .target, qzzsz__iyee.loc)
                        gbkl__wnhj = True
                elif len(blocks[qzzsz__iyee.truebr].body) == 1:
                    kmxc__yhaqr = blocks[qzzsz__iyee.truebr].body[0]
                    if isinstance(kmxc__yhaqr, ir.Jump
                        ) and kmxc__yhaqr.target == qzzsz__iyee.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(kmxc__yhaqr
                            .target, qzzsz__iyee.loc)
                        gbkl__wnhj = True
                elif len(blocks[qzzsz__iyee.falsebr].body) == 1:
                    tqt__jshwf = blocks[qzzsz__iyee.falsebr].body[0]
                    if isinstance(tqt__jshwf, ir.Jump
                        ) and tqt__jshwf.target == qzzsz__iyee.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(tqt__jshwf
                            .target, qzzsz__iyee.loc)
                        gbkl__wnhj = True
    return gbkl__wnhj


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        clsjq__qnj = find_topo_order(parfor.loop_body)
    xrrkf__wmycj = clsjq__qnj[0]
    cwt__kins = {}
    _update_parfor_get_setitems(parfor.loop_body[xrrkf__wmycj].body, parfor
        .index_var, alias_map, cwt__kins, lives_n_aliases)
    esu__ntx = set(cwt__kins.keys())
    for mmy__qrfz in clsjq__qnj:
        if mmy__qrfz == xrrkf__wmycj:
            continue
        for stmt in parfor.loop_body[mmy__qrfz].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            qjyr__bxg = set(jxplm__ekr.name for jxplm__ekr in stmt.list_vars())
            saerk__apsc = qjyr__bxg & esu__ntx
            for a in saerk__apsc:
                cwt__kins.pop(a, None)
    for mmy__qrfz in clsjq__qnj:
        if mmy__qrfz == xrrkf__wmycj:
            continue
        block = parfor.loop_body[mmy__qrfz]
        whn__yxny = cwt__kins.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            whn__yxny, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    tljq__wbxug = max(blocks.keys())
    wijcf__ylf, aogkh__yid = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    jkq__phyi = ir.Jump(wijcf__ylf, ir.Loc('parfors_dummy', -1))
    blocks[tljq__wbxug].body.append(jkq__phyi)
    dyvcz__afpq = compute_cfg_from_blocks(blocks)
    xgzko__vne = compute_use_defs(blocks)
    xfxgr__goz = compute_live_map(dyvcz__afpq, blocks, xgzko__vne.usemap,
        xgzko__vne.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        deiw__ihyy = []
        kqk__qkbxh = {jxplm__ekr.name for jxplm__ekr in block.terminator.
            list_vars()}
        for araxq__nzj, dfig__ial in dyvcz__afpq.successors(label):
            kqk__qkbxh |= xfxgr__goz[araxq__nzj]
        for stmt in reversed(block.body):
            kxst__bnfyz = kqk__qkbxh & alias_set
            for jxplm__ekr in kxst__bnfyz:
                kqk__qkbxh |= alias_map[jxplm__ekr]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in kqk__qkbxh and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                mxps__kebe = guard(find_callname, func_ir, stmt.value)
                if mxps__kebe == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in kqk__qkbxh and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            kqk__qkbxh |= {jxplm__ekr.name for jxplm__ekr in stmt.list_vars()}
            deiw__ihyy.append(stmt)
        deiw__ihyy.reverse()
        block.body = deiw__ihyy
    typemap.pop(aogkh__yid.name)
    blocks[tljq__wbxug].body.pop()
    gbkl__wnhj = True
    while gbkl__wnhj:
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
        gbkl__wnhj = trim_empty_parfor_branches(parfor)
    dgkva__yhg = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        dgkva__yhg &= len(block.body) == 0
    if dgkva__yhg:
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
    mqzk__lsr = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                mqzk__lsr += 1
                parfor = stmt
                qcihd__gywu = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = qcihd__gywu.scope
                loc = ir.Loc('parfors_dummy', -1)
                xxx__fxr = ir.Var(scope, mk_unique_var('$const'), loc)
                qcihd__gywu.body.append(ir.Assign(ir.Const(0, loc),
                    xxx__fxr, loc))
                qcihd__gywu.body.append(ir.Return(xxx__fxr, loc))
                dyvcz__afpq = compute_cfg_from_blocks(parfor.loop_body)
                for ldrr__zph in dyvcz__afpq.dead_nodes():
                    del parfor.loop_body[ldrr__zph]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                qcihd__gywu = parfor.loop_body[max(parfor.loop_body.keys())]
                qcihd__gywu.body.pop()
                qcihd__gywu.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return mqzk__lsr


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    dyvcz__afpq = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != dyvcz__afpq.entry_point()
    moxd__eqs = list(filter(find_single_branch, blocks.keys()))
    aao__powqu = set()
    for label in moxd__eqs:
        inst = blocks[label].body[0]
        otei__mmr = dyvcz__afpq.predecessors(label)
        tplb__khqwv = True
        for lxdo__fxtk, nrs__yzxuk in otei__mmr:
            block = blocks[lxdo__fxtk]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                tplb__khqwv = False
        if tplb__khqwv:
            aao__powqu.add(label)
    for label in aao__powqu:
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
            kwzo__och = self.overloads.get(tuple(args))
            if kwzo__och is not None:
                return kwzo__och.entry_point
            self._pre_compile(args, return_type, flags)
            uhbmr__zljkb = self.func_ir
            thjwz__zoun = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=thjwz__zoun):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=uhbmr__zljkb, args=
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
        ieh__ftj = copy.deepcopy(flags)
        ieh__ftj.no_rewrites = True

        def compile_local(the_ir, the_flags):
            rfqo__kyro = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return rfqo__kyro.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        tyz__wqhxu = compile_local(func_ir, ieh__ftj)
        hdexx__xttxa = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    hdexx__xttxa = compile_local(func_ir, flags)
                except Exception as odxnv__cll:
                    pass
        if hdexx__xttxa is not None:
            cres = hdexx__xttxa
        else:
            cres = tyz__wqhxu
        return cres
    else:
        rfqo__kyro = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return rfqo__kyro.compile_ir(func_ir=func_ir, lifted=lifted,
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
    pyd__can = self.get_data_type(typ.dtype)
    nkdeq__akcej = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        nkdeq__akcej):
        raib__emvy = ary.ctypes.data
        iig__rng = self.add_dynamic_addr(builder, raib__emvy, info=str(type
            (raib__emvy)))
        edoo__kvo = self.add_dynamic_addr(builder, id(ary), info=str(type(ary))
            )
        self.global_arrays.append(ary)
    else:
        aya__layo = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            aya__layo = aya__layo.view('int64')
        val = bytearray(aya__layo.data)
        pracn__zld = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        iig__rng = cgutils.global_constant(builder, '.const.array.data',
            pracn__zld)
        iig__rng.align = self.get_abi_alignment(pyd__can)
        edoo__kvo = None
    rwejj__yzve = self.get_value_type(types.intp)
    aativ__akf = [self.get_constant(types.intp, tlmm__tiu) for tlmm__tiu in
        ary.shape]
    yhdvy__mjs = lir.Constant(lir.ArrayType(rwejj__yzve, len(aativ__akf)),
        aativ__akf)
    kbob__aelj = [self.get_constant(types.intp, tlmm__tiu) for tlmm__tiu in
        ary.strides]
    gzru__exnb = lir.Constant(lir.ArrayType(rwejj__yzve, len(kbob__aelj)),
        kbob__aelj)
    riq__swcl = self.get_constant(types.intp, ary.dtype.itemsize)
    hdt__rrrf = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        hdt__rrrf, riq__swcl, iig__rng.bitcast(self.get_value_type(types.
        CPointer(typ.dtype))), yhdvy__mjs, gzru__exnb])


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
    gbqbm__hqqjp = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    ojtwc__kpi = lir.Function(module, gbqbm__hqqjp, name='nrt_atomic_{0}'.
        format(op))
    [jvmum__ucffl] = ojtwc__kpi.args
    eud__qvvof = ojtwc__kpi.append_basic_block()
    builder = lir.IRBuilder(eud__qvvof)
    cai__yapra = lir.Constant(_word_type, 1)
    if False:
        gvoa__cycc = builder.atomic_rmw(op, jvmum__ucffl, cai__yapra,
            ordering=ordering)
        res = getattr(builder, op)(gvoa__cycc, cai__yapra)
        builder.ret(res)
    else:
        gvoa__cycc = builder.load(jvmum__ucffl)
        odydt__zpv = getattr(builder, op)(gvoa__cycc, cai__yapra)
        nondr__uust = builder.icmp_signed('!=', gvoa__cycc, lir.Constant(
            gvoa__cycc.type, -1))
        with cgutils.if_likely(builder, nondr__uust):
            builder.store(odydt__zpv, jvmum__ucffl)
        builder.ret(odydt__zpv)
    return ojtwc__kpi


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
        xfz__mmvq = state.targetctx.codegen()
        state.library = xfz__mmvq.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    toam__jgq = state.func_ir
    typemap = state.typemap
    lywt__qhxvf = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    ljhlm__ghua = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            toam__jgq, typemap, lywt__qhxvf, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            ajwl__ajjw = lowering.Lower(targetctx, library, fndesc,
                toam__jgq, metadata=metadata)
            ajwl__ajjw.lower()
            if not flags.no_cpython_wrapper:
                ajwl__ajjw.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(lywt__qhxvf, (types.Optional, types.
                        Generator)):
                        pass
                    else:
                        ajwl__ajjw.create_cfunc_wrapper()
            env = ajwl__ajjw.env
            cxazq__chcci = ajwl__ajjw.call_helper
            del ajwl__ajjw
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, cxazq__chcci, cfunc=None,
                env=env)
        else:
            qzlpt__bjtb = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(qzlpt__bjtb, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, cxazq__chcci, cfunc=
                qzlpt__bjtb, env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        wxfuz__vnek = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = wxfuz__vnek - ljhlm__ghua
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
        roi__skk = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, roi__skk), likely
            =False):
            c.builder.store(cgutils.true_bit, errorptr)
            bylbl__bmdu.do_break()
        izul__nauh = c.builder.icmp_signed('!=', roi__skk, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(izul__nauh, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, roi__skk)
                c.pyapi.decref(roi__skk)
                bylbl__bmdu.do_break()
        c.pyapi.decref(roi__skk)
    cixi__rxlw, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(cixi__rxlw, likely=True) as (pyib__ztv, gvvhr__moxp
        ):
        with pyib__ztv:
            list.size = size
            wshrq__zpb = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                wshrq__zpb), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        wshrq__zpb))
                    with cgutils.for_range(c.builder, size) as bylbl__bmdu:
                        itemobj = c.pyapi.list_getitem(obj, bylbl__bmdu.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        uan__dovn = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(uan__dovn.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            bylbl__bmdu.do_break()
                        list.setitem(bylbl__bmdu.index, uan__dovn.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with gvvhr__moxp:
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
    kaw__hffyy, aoqaa__friug, pqptr__yhh, vvw__rls, snys__kuoi = (
        compile_time_get_string_data(literal_string))
    bld__qpdld = builder.module
    gv = context.insert_const_bytes(bld__qpdld, kaw__hffyy)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        aoqaa__friug), context.get_constant(types.int32, pqptr__yhh),
        context.get_constant(types.uint32, vvw__rls), context.get_constant(
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
    agck__ysysz = None
    if isinstance(shape, types.Integer):
        agck__ysysz = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(tlmm__tiu, (types.Integer, types.IntEnumMember)) for
            tlmm__tiu in shape):
            agck__ysysz = len(shape)
    return agck__ysysz


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
            agck__ysysz = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if agck__ysysz == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    agck__ysysz))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            tkbbp__szozl = self._get_names(x)
            if len(tkbbp__szozl) != 0:
                return tkbbp__szozl[0]
            return tkbbp__szozl
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    tkbbp__szozl = self._get_names(obj)
    if len(tkbbp__szozl) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(tkbbp__szozl[0])


def get_equiv_set(self, obj):
    tkbbp__szozl = self._get_names(obj)
    if len(tkbbp__szozl) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(tkbbp__szozl[0])


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
    mooes__eaiv = []
    for hpwa__uch in func_ir.arg_names:
        if hpwa__uch in typemap and isinstance(typemap[hpwa__uch], types.
            containers.UniTuple) and typemap[hpwa__uch].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(hpwa__uch))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for ezks__kmcb in func_ir.blocks.values():
        for stmt in ezks__kmcb.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    kqg__xvpik = getattr(val, 'code', None)
                    if kqg__xvpik is not None:
                        if getattr(val, 'closure', None) is not None:
                            vhhcy__uwr = '<creating a function from a closure>'
                            hipcv__kjya = ''
                        else:
                            vhhcy__uwr = kqg__xvpik.co_name
                            hipcv__kjya = '(%s) ' % vhhcy__uwr
                    else:
                        vhhcy__uwr = '<could not ascertain use case>'
                        hipcv__kjya = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (vhhcy__uwr, hipcv__kjya))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                ben__cjzmy = False
                if isinstance(val, pytypes.FunctionType):
                    ben__cjzmy = val in {numba.gdb, numba.gdb_init}
                if not ben__cjzmy:
                    ben__cjzmy = getattr(val, '_name', '') == 'gdb_internal'
                if ben__cjzmy:
                    mooes__eaiv.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    ruzi__brd = func_ir.get_definition(var)
                    pekpy__ixv = guard(find_callname, func_ir, ruzi__brd)
                    if pekpy__ixv and pekpy__ixv[1] == 'numpy':
                        ty = getattr(numpy, pekpy__ixv[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    vtt__mjzg = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(vtt__mjzg), loc=stmt.loc)
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
    if len(mooes__eaiv) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        vpz__aumcy = '\n'.join([x.strformat() for x in mooes__eaiv])
        raise errors.UnsupportedError(msg % vpz__aumcy)


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
    zfd__ygrjl, jxplm__ekr = next(iter(val.items()))
    uhhf__hxexq = typeof_impl(zfd__ygrjl, c)
    acr__wku = typeof_impl(jxplm__ekr, c)
    if uhhf__hxexq is None or acr__wku is None:
        raise ValueError(
            f'Cannot type dict element type {type(zfd__ygrjl)}, {type(jxplm__ekr)}'
            )
    return types.DictType(uhhf__hxexq, acr__wku)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    edsve__fwj = cgutils.alloca_once_value(c.builder, val)
    lypm__tfh = c.pyapi.object_hasattr_string(val, '_opaque')
    dno__ugcy = c.builder.icmp_unsigned('==', lypm__tfh, lir.Constant(
        lypm__tfh.type, 0))
    acv__xyb = typ.key_type
    fxrq__bsg = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(acv__xyb, fxrq__bsg)

    def copy_dict(out_dict, in_dict):
        for zfd__ygrjl, jxplm__ekr in in_dict.items():
            out_dict[zfd__ygrjl] = jxplm__ekr
    with c.builder.if_then(dno__ugcy):
        zzzc__fdp = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        eevdh__pel = c.pyapi.call_function_objargs(zzzc__fdp, [])
        evkoy__fug = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(evkoy__fug, [eevdh__pel, val])
        c.builder.store(eevdh__pel, edsve__fwj)
    val = c.builder.load(edsve__fwj)
    vtsb__agz = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    jki__yehrt = c.pyapi.object_type(val)
    wszm__whnfz = c.builder.icmp_unsigned('==', jki__yehrt, vtsb__agz)
    with c.builder.if_else(wszm__whnfz) as (fby__gptn, njhbp__rmp):
        with fby__gptn:
            hmb__flqsb = c.pyapi.object_getattr_string(val, '_opaque')
            miytd__piayw = types.MemInfoPointer(types.voidptr)
            uan__dovn = c.unbox(miytd__piayw, hmb__flqsb)
            mi = uan__dovn.value
            rfphd__dob = miytd__piayw, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *rfphd__dob)
            ima__lrzej = context.get_constant_null(rfphd__dob[1])
            args = mi, ima__lrzej
            jrhys__lces, qdwez__inks = c.pyapi.call_jit_code(convert, sig, args
                )
            c.context.nrt.decref(c.builder, typ, qdwez__inks)
            c.pyapi.decref(hmb__flqsb)
            furbr__qdmgb = c.builder.basic_block
        with njhbp__rmp:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", jki__yehrt, vtsb__agz)
            owiyn__zshi = c.builder.basic_block
    tssqr__zghth = c.builder.phi(qdwez__inks.type)
    viu__navov = c.builder.phi(jrhys__lces.type)
    tssqr__zghth.add_incoming(qdwez__inks, furbr__qdmgb)
    tssqr__zghth.add_incoming(qdwez__inks.type(None), owiyn__zshi)
    viu__navov.add_incoming(jrhys__lces, furbr__qdmgb)
    viu__navov.add_incoming(cgutils.true_bit, owiyn__zshi)
    c.pyapi.decref(vtsb__agz)
    c.pyapi.decref(jki__yehrt)
    with c.builder.if_then(dno__ugcy):
        c.pyapi.decref(val)
    return NativeValue(tssqr__zghth, is_error=viu__navov)


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
    zfi__zawfs = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=zfi__zawfs, name=updatevar)
    vvs__qcfv = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=vvs__qcfv, name=res)


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
        for zfd__ygrjl, jxplm__ekr in other.items():
            d[zfd__ygrjl] = jxplm__ekr
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
    hipcv__kjya = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(hipcv__kjya, res)


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
    kozr__evsos = PassManager(name)
    if state.func_ir is None:
        kozr__evsos.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            kozr__evsos.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        kozr__evsos.add_pass(FixupArgs, 'fix up args')
    kozr__evsos.add_pass(IRProcessing, 'processing IR')
    kozr__evsos.add_pass(WithLifting, 'Handle with contexts')
    kozr__evsos.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        kozr__evsos.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        kozr__evsos.add_pass(DeadBranchPrune, 'dead branch pruning')
        kozr__evsos.add_pass(GenericRewrites, 'nopython rewrites')
    kozr__evsos.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    kozr__evsos.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        kozr__evsos.add_pass(DeadBranchPrune, 'dead branch pruning')
    kozr__evsos.add_pass(FindLiterallyCalls, 'find literally calls')
    kozr__evsos.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        kozr__evsos.add_pass(ReconstructSSA, 'ssa')
    kozr__evsos.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    kozr__evsos.finalize()
    return kozr__evsos


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
    a, tsfx__vyq = args
    if isinstance(a, types.List) and isinstance(tsfx__vyq, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(tsfx__vyq, types.List):
        return signature(tsfx__vyq, types.intp, tsfx__vyq)


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
        qav__rwx, vnr__nua = 0, 1
    else:
        qav__rwx, vnr__nua = 1, 0
    tsoh__fos = ListInstance(context, builder, sig.args[qav__rwx], args[
        qav__rwx])
    born__zdmqg = tsoh__fos.size
    bun__wbp = args[vnr__nua]
    wshrq__zpb = lir.Constant(bun__wbp.type, 0)
    bun__wbp = builder.select(cgutils.is_neg_int(builder, bun__wbp),
        wshrq__zpb, bun__wbp)
    hdt__rrrf = builder.mul(bun__wbp, born__zdmqg)
    gum__nkx = ListInstance.allocate(context, builder, sig.return_type,
        hdt__rrrf)
    gum__nkx.size = hdt__rrrf
    with cgutils.for_range_slice(builder, wshrq__zpb, hdt__rrrf,
        born__zdmqg, inc=True) as (vubqj__yqa, _):
        with cgutils.for_range(builder, born__zdmqg) as bylbl__bmdu:
            value = tsoh__fos.getitem(bylbl__bmdu.index)
            gum__nkx.setitem(builder.add(bylbl__bmdu.index, vubqj__yqa),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, gum__nkx.value)


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
    xqbif__hvnx = first.unify(self, second)
    if xqbif__hvnx is not None:
        return xqbif__hvnx
    xqbif__hvnx = second.unify(self, first)
    if xqbif__hvnx is not None:
        return xqbif__hvnx
    cfoob__pko = self.can_convert(fromty=first, toty=second)
    if cfoob__pko is not None and cfoob__pko <= Conversion.safe:
        return second
    cfoob__pko = self.can_convert(fromty=second, toty=first)
    if cfoob__pko is not None and cfoob__pko <= Conversion.safe:
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
    hdt__rrrf = payload.used
    listobj = c.pyapi.list_new(hdt__rrrf)
    cixi__rxlw = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(cixi__rxlw, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(hdt__rrrf.
            type, 0))
        with payload._iterate() as bylbl__bmdu:
            i = c.builder.load(index)
            item = bylbl__bmdu.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return cixi__rxlw, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    eobvk__smqx = h.type
    cqs__nels = self.mask
    dtype = self._ty.dtype
    iqzpo__gzkqy = context.typing_context
    fnty = iqzpo__gzkqy.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(iqzpo__gzkqy, (dtype, dtype), {})
    gzro__avj = context.get_function(fnty, sig)
    kas__kcc = ir.Constant(eobvk__smqx, 1)
    nixyl__wov = ir.Constant(eobvk__smqx, 5)
    ecxo__smcvx = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, cqs__nels))
    if for_insert:
        hev__yft = cqs__nels.type(-1)
        lqvfm__yhy = cgutils.alloca_once_value(builder, hev__yft)
    stx__cih = builder.append_basic_block('lookup.body')
    wstwb__qwmk = builder.append_basic_block('lookup.found')
    xlrc__egolw = builder.append_basic_block('lookup.not_found')
    uom__kuw = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        lgvv__mdhar = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, lgvv__mdhar)):
            stff__ymvxe = gzro__avj(builder, (item, entry.key))
            with builder.if_then(stff__ymvxe):
                builder.branch(wstwb__qwmk)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, lgvv__mdhar)):
            builder.branch(xlrc__egolw)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, lgvv__mdhar)):
                ffv__nbyz = builder.load(lqvfm__yhy)
                ffv__nbyz = builder.select(builder.icmp_unsigned('==',
                    ffv__nbyz, hev__yft), i, ffv__nbyz)
                builder.store(ffv__nbyz, lqvfm__yhy)
    with cgutils.for_range(builder, ir.Constant(eobvk__smqx, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, kas__kcc)
        i = builder.and_(i, cqs__nels)
        builder.store(i, index)
    builder.branch(stx__cih)
    with builder.goto_block(stx__cih):
        i = builder.load(index)
        check_entry(i)
        lxdo__fxtk = builder.load(ecxo__smcvx)
        lxdo__fxtk = builder.lshr(lxdo__fxtk, nixyl__wov)
        i = builder.add(kas__kcc, builder.mul(i, nixyl__wov))
        i = builder.and_(cqs__nels, builder.add(i, lxdo__fxtk))
        builder.store(i, index)
        builder.store(lxdo__fxtk, ecxo__smcvx)
        builder.branch(stx__cih)
    with builder.goto_block(xlrc__egolw):
        if for_insert:
            i = builder.load(index)
            ffv__nbyz = builder.load(lqvfm__yhy)
            i = builder.select(builder.icmp_unsigned('==', ffv__nbyz,
                hev__yft), i, ffv__nbyz)
            builder.store(i, index)
        builder.branch(uom__kuw)
    with builder.goto_block(wstwb__qwmk):
        builder.branch(uom__kuw)
    builder.position_at_end(uom__kuw)
    ben__cjzmy = builder.phi(ir.IntType(1), 'found')
    ben__cjzmy.add_incoming(cgutils.true_bit, wstwb__qwmk)
    ben__cjzmy.add_incoming(cgutils.false_bit, xlrc__egolw)
    return ben__cjzmy, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    jws__xns = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    tea__srz = payload.used
    kas__kcc = ir.Constant(tea__srz.type, 1)
    tea__srz = payload.used = builder.add(tea__srz, kas__kcc)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, jws__xns), likely=True):
        payload.fill = builder.add(payload.fill, kas__kcc)
    if do_resize:
        self.upsize(tea__srz)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    ben__cjzmy, i = payload._lookup(item, h, for_insert=True)
    rik__sxd = builder.not_(ben__cjzmy)
    with builder.if_then(rik__sxd):
        entry = payload.get_entry(i)
        jws__xns = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        tea__srz = payload.used
        kas__kcc = ir.Constant(tea__srz.type, 1)
        tea__srz = payload.used = builder.add(tea__srz, kas__kcc)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, jws__xns), likely=True):
            payload.fill = builder.add(payload.fill, kas__kcc)
        if do_resize:
            self.upsize(tea__srz)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    tea__srz = payload.used
    kas__kcc = ir.Constant(tea__srz.type, 1)
    tea__srz = payload.used = self._builder.sub(tea__srz, kas__kcc)
    if do_resize:
        self.downsize(tea__srz)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    hxye__jcxi = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, hxye__jcxi)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    qjvwl__zpmtt = payload
    cixi__rxlw = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(cixi__rxlw), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with qjvwl__zpmtt._iterate() as bylbl__bmdu:
        entry = bylbl__bmdu.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(qjvwl__zpmtt.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as bylbl__bmdu:
        entry = bylbl__bmdu.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    cixi__rxlw = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(cixi__rxlw), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    cixi__rxlw = cgutils.alloca_once_value(builder, cgutils.true_bit)
    eobvk__smqx = context.get_value_type(types.intp)
    wshrq__zpb = ir.Constant(eobvk__smqx, 0)
    kas__kcc = ir.Constant(eobvk__smqx, 1)
    yxxzd__ncow = context.get_data_type(types.SetPayload(self._ty))
    scl__qdpuq = context.get_abi_sizeof(yxxzd__ncow)
    qyd__xpgt = self._entrysize
    scl__qdpuq -= qyd__xpgt
    zju__zfeug, bjmbu__gzrd = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(eobvk__smqx, qyd__xpgt), ir.Constant(
        eobvk__smqx, scl__qdpuq))
    with builder.if_then(bjmbu__gzrd, likely=False):
        builder.store(cgutils.false_bit, cixi__rxlw)
    with builder.if_then(builder.load(cixi__rxlw), likely=True):
        if realloc:
            orbba__drzl = self._set.meminfo
            jvmum__ucffl = context.nrt.meminfo_varsize_alloc(builder,
                orbba__drzl, size=zju__zfeug)
            pmrw__misiy = cgutils.is_null(builder, jvmum__ucffl)
        else:
            ohve__gdmyx = _imp_dtor(context, builder.module, self._ty)
            orbba__drzl = context.nrt.meminfo_new_varsize_dtor(builder,
                zju__zfeug, builder.bitcast(ohve__gdmyx, cgutils.voidptr_t))
            pmrw__misiy = cgutils.is_null(builder, orbba__drzl)
        with builder.if_else(pmrw__misiy, likely=False) as (llq__mqk, pyib__ztv
            ):
            with llq__mqk:
                builder.store(cgutils.false_bit, cixi__rxlw)
            with pyib__ztv:
                if not realloc:
                    self._set.meminfo = orbba__drzl
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, zju__zfeug, 255)
                payload.used = wshrq__zpb
                payload.fill = wshrq__zpb
                payload.finger = wshrq__zpb
                wfkc__rncx = builder.sub(nentries, kas__kcc)
                payload.mask = wfkc__rncx
    return builder.load(cixi__rxlw)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    cixi__rxlw = cgutils.alloca_once_value(builder, cgutils.true_bit)
    eobvk__smqx = context.get_value_type(types.intp)
    wshrq__zpb = ir.Constant(eobvk__smqx, 0)
    kas__kcc = ir.Constant(eobvk__smqx, 1)
    yxxzd__ncow = context.get_data_type(types.SetPayload(self._ty))
    scl__qdpuq = context.get_abi_sizeof(yxxzd__ncow)
    qyd__xpgt = self._entrysize
    scl__qdpuq -= qyd__xpgt
    cqs__nels = src_payload.mask
    nentries = builder.add(kas__kcc, cqs__nels)
    zju__zfeug = builder.add(ir.Constant(eobvk__smqx, scl__qdpuq), builder.
        mul(ir.Constant(eobvk__smqx, qyd__xpgt), nentries))
    with builder.if_then(builder.load(cixi__rxlw), likely=True):
        ohve__gdmyx = _imp_dtor(context, builder.module, self._ty)
        orbba__drzl = context.nrt.meminfo_new_varsize_dtor(builder,
            zju__zfeug, builder.bitcast(ohve__gdmyx, cgutils.voidptr_t))
        pmrw__misiy = cgutils.is_null(builder, orbba__drzl)
        with builder.if_else(pmrw__misiy, likely=False) as (llq__mqk, pyib__ztv
            ):
            with llq__mqk:
                builder.store(cgutils.false_bit, cixi__rxlw)
            with pyib__ztv:
                self._set.meminfo = orbba__drzl
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = wshrq__zpb
                payload.mask = cqs__nels
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, qyd__xpgt)
                with src_payload._iterate() as bylbl__bmdu:
                    context.nrt.incref(builder, self._ty.dtype, bylbl__bmdu
                        .entry.key)
    return builder.load(cixi__rxlw)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    vfele__ccjai = context.get_value_type(types.voidptr)
    wuup__mtrr = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [vfele__ccjai, wuup__mtrr,
        vfele__ccjai])
    vhxs__voqdj = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=vhxs__voqdj)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        hksf__vfxpq = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, hksf__vfxpq)
        with payload._iterate() as bylbl__bmdu:
            entry = bylbl__bmdu.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    xtor__waxx, = sig.args
    nqr__dyz, = args
    mkavr__cxedu = numba.core.imputils.call_len(context, builder,
        xtor__waxx, nqr__dyz)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, mkavr__cxedu)
    with numba.core.imputils.for_iter(context, builder, xtor__waxx, nqr__dyz
        ) as bylbl__bmdu:
        inst.add(bylbl__bmdu.value)
        context.nrt.decref(builder, set_type.dtype, bylbl__bmdu.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    xtor__waxx = sig.args[1]
    nqr__dyz = args[1]
    mkavr__cxedu = numba.core.imputils.call_len(context, builder,
        xtor__waxx, nqr__dyz)
    if mkavr__cxedu is not None:
        zmwy__jqqnl = builder.add(inst.payload.used, mkavr__cxedu)
        inst.upsize(zmwy__jqqnl)
    with numba.core.imputils.for_iter(context, builder, xtor__waxx, nqr__dyz
        ) as bylbl__bmdu:
        jknvq__weo = context.cast(builder, bylbl__bmdu.value, xtor__waxx.
            dtype, inst.dtype)
        inst.add(jknvq__weo)
        context.nrt.decref(builder, xtor__waxx.dtype, bylbl__bmdu.value)
    if mkavr__cxedu is not None:
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
    vrvl__pmys = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, vrvl__pmys, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    qzlpt__bjtb = target_context.get_executable(library, fndesc, env)
    lyxyf__xqmht = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=qzlpt__bjtb, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return lyxyf__xqmht


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
        quvl__rymp = MPI.COMM_WORLD
        if quvl__rymp.Get_rank() == 0:
            qdu__hrsnp = self.get_cache_path()
            os.makedirs(qdu__hrsnp, exist_ok=True)
            tempfile.TemporaryFile(dir=qdu__hrsnp).close()
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
    ksrom__syybn = cgutils.create_struct_proxy(charseq.bytes_type)
    fphwu__gafh = ksrom__syybn(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(fphwu__gafh.nitems.type, nbytes)
    fphwu__gafh.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    fphwu__gafh.nitems = nbytes
    fphwu__gafh.itemsize = ir.Constant(fphwu__gafh.itemsize.type, 1)
    fphwu__gafh.data = context.nrt.meminfo_data(builder, fphwu__gafh.meminfo)
    fphwu__gafh.parent = cgutils.get_null_value(fphwu__gafh.parent.type)
    fphwu__gafh.shape = cgutils.pack_array(builder, [fphwu__gafh.nitems],
        context.get_value_type(types.intp))
    fphwu__gafh.strides = cgutils.pack_array(builder, [ir.Constant(
        fphwu__gafh.strides.type.element, 1)], context.get_value_type(types
        .intp))
    return fphwu__gafh


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
