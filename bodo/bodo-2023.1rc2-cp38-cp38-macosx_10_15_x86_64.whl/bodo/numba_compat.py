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
    vezq__oex = numba.core.bytecode.FunctionIdentity.from_function(func)
    irp__rflgy = numba.core.interpreter.Interpreter(vezq__oex)
    nntg__uknxx = numba.core.bytecode.ByteCode(func_id=vezq__oex)
    func_ir = irp__rflgy.interpret(nntg__uknxx)
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
        lvg__mizg = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        lvg__mizg.run()
    jqfc__boo = numba.core.postproc.PostProcessor(func_ir)
    jqfc__boo.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, tml__qtyur in visit_vars_extensions.items():
        if isinstance(stmt, t):
            tml__qtyur(stmt, callback, cbdata)
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
    znnlj__obosf = ['ravel', 'transpose', 'reshape']
    for teu__phhdt in blocks.values():
        for cvwj__xurrs in teu__phhdt.body:
            if type(cvwj__xurrs) in alias_analysis_extensions:
                tml__qtyur = alias_analysis_extensions[type(cvwj__xurrs)]
                tml__qtyur(cvwj__xurrs, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(cvwj__xurrs, ir.Assign):
                ljuck__iejrz = cvwj__xurrs.value
                ovhbh__ncq = cvwj__xurrs.target.name
                if is_immutable_type(ovhbh__ncq, typemap):
                    continue
                if isinstance(ljuck__iejrz, ir.Var
                    ) and ovhbh__ncq != ljuck__iejrz.name:
                    _add_alias(ovhbh__ncq, ljuck__iejrz.name, alias_map,
                        arg_aliases)
                if isinstance(ljuck__iejrz, ir.Expr) and (ljuck__iejrz.op ==
                    'cast' or ljuck__iejrz.op in ['getitem', 'static_getitem']
                    ):
                    _add_alias(ovhbh__ncq, ljuck__iejrz.value.name,
                        alias_map, arg_aliases)
                if isinstance(ljuck__iejrz, ir.Expr
                    ) and ljuck__iejrz.op == 'inplace_binop':
                    _add_alias(ovhbh__ncq, ljuck__iejrz.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(ljuck__iejrz, ir.Expr
                    ) and ljuck__iejrz.op == 'getattr' and ljuck__iejrz.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(ovhbh__ncq, ljuck__iejrz.value.name,
                        alias_map, arg_aliases)
                if (isinstance(ljuck__iejrz, ir.Expr) and ljuck__iejrz.op ==
                    'getattr' and ljuck__iejrz.attr not in ['shape'] and 
                    ljuck__iejrz.value.name in arg_aliases):
                    _add_alias(ovhbh__ncq, ljuck__iejrz.value.name,
                        alias_map, arg_aliases)
                if isinstance(ljuck__iejrz, ir.Expr
                    ) and ljuck__iejrz.op == 'getattr' and ljuck__iejrz.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(ovhbh__ncq, ljuck__iejrz.value.name,
                        alias_map, arg_aliases)
                if isinstance(ljuck__iejrz, ir.Expr) and ljuck__iejrz.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(ovhbh__ncq, typemap):
                    for tij__ygkm in ljuck__iejrz.items:
                        _add_alias(ovhbh__ncq, tij__ygkm.name, alias_map,
                            arg_aliases)
                if isinstance(ljuck__iejrz, ir.Expr
                    ) and ljuck__iejrz.op == 'call':
                    tddbn__syuo = guard(find_callname, func_ir,
                        ljuck__iejrz, typemap)
                    if tddbn__syuo is None:
                        continue
                    haia__ykzr, eejc__rde = tddbn__syuo
                    if tddbn__syuo in alias_func_extensions:
                        iay__bmfwb = alias_func_extensions[tddbn__syuo]
                        iay__bmfwb(ovhbh__ncq, ljuck__iejrz.args, alias_map,
                            arg_aliases)
                    if eejc__rde == 'numpy' and haia__ykzr in znnlj__obosf:
                        _add_alias(ovhbh__ncq, ljuck__iejrz.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(eejc__rde, ir.Var
                        ) and haia__ykzr in znnlj__obosf:
                        _add_alias(ovhbh__ncq, eejc__rde.name, alias_map,
                            arg_aliases)
    bjcnx__roxnq = copy.deepcopy(alias_map)
    for tij__ygkm in bjcnx__roxnq:
        for wlaad__zvtz in bjcnx__roxnq[tij__ygkm]:
            alias_map[tij__ygkm] |= alias_map[wlaad__zvtz]
        for wlaad__zvtz in bjcnx__roxnq[tij__ygkm]:
            alias_map[wlaad__zvtz] = alias_map[tij__ygkm]
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
    hkx__xasfn = compute_cfg_from_blocks(func_ir.blocks)
    lizx__icpc = compute_use_defs(func_ir.blocks)
    oetq__mluxl = compute_live_map(hkx__xasfn, func_ir.blocks, lizx__icpc.
        usemap, lizx__icpc.defmap)
    brts__jktc = True
    while brts__jktc:
        brts__jktc = False
        for label, block in func_ir.blocks.items():
            lives = {tij__ygkm.name for tij__ygkm in block.terminator.
                list_vars()}
            for xax__pxwbi, khvrn__dejzy in hkx__xasfn.successors(label):
                lives |= oetq__mluxl[xax__pxwbi]
            dqpte__larz = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    ovhbh__ncq = stmt.target
                    ydlyc__vjd = stmt.value
                    if ovhbh__ncq.name not in lives:
                        if isinstance(ydlyc__vjd, ir.Expr
                            ) and ydlyc__vjd.op == 'make_function':
                            continue
                        if isinstance(ydlyc__vjd, ir.Expr
                            ) and ydlyc__vjd.op == 'getattr':
                            continue
                        if isinstance(ydlyc__vjd, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(ovhbh__ncq,
                            None), types.Function):
                            continue
                        if isinstance(ydlyc__vjd, ir.Expr
                            ) and ydlyc__vjd.op == 'build_map':
                            continue
                        if isinstance(ydlyc__vjd, ir.Expr
                            ) and ydlyc__vjd.op == 'build_tuple':
                            continue
                        if isinstance(ydlyc__vjd, ir.Expr
                            ) and ydlyc__vjd.op == 'binop':
                            continue
                        if isinstance(ydlyc__vjd, ir.Expr
                            ) and ydlyc__vjd.op == 'unary':
                            continue
                        if isinstance(ydlyc__vjd, ir.Expr
                            ) and ydlyc__vjd.op in ('static_getitem', 'getitem'
                            ):
                            continue
                    if isinstance(ydlyc__vjd, ir.Var
                        ) and ovhbh__ncq.name == ydlyc__vjd.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    qih__efyq = analysis.ir_extension_usedefs[type(stmt)]
                    vnsgv__bjstb, uxgir__fzzu = qih__efyq(stmt)
                    lives -= uxgir__fzzu
                    lives |= vnsgv__bjstb
                else:
                    lives |= {tij__ygkm.name for tij__ygkm in stmt.list_vars()}
                    if isinstance(stmt, ir.Assign):
                        poh__uuh = set()
                        if isinstance(ydlyc__vjd, ir.Expr):
                            poh__uuh = {tij__ygkm.name for tij__ygkm in
                                ydlyc__vjd.list_vars()}
                        if ovhbh__ncq.name not in poh__uuh:
                            lives.remove(ovhbh__ncq.name)
                dqpte__larz.append(stmt)
            dqpte__larz.reverse()
            if len(block.body) != len(dqpte__larz):
                brts__jktc = True
            block.body = dqpte__larz


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    pjsw__zaa = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (pjsw__zaa,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    cnamd__fez = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), cnamd__fez)


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
            for tzr__qjdm in fnty.templates:
                self._inline_overloads.update(tzr__qjdm._inline_overloads)
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
    cnamd__fez = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), cnamd__fez)
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
    kbwtb__eck, xqd__scxnq = self._get_impl(args, kws)
    if kbwtb__eck is None:
        return
    syfo__wdla = types.Dispatcher(kbwtb__eck)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        nlgg__alj = kbwtb__eck._compiler
        flags = compiler.Flags()
        ppceh__osdw = nlgg__alj.targetdescr.typing_context
        zdr__sknq = nlgg__alj.targetdescr.target_context
        kfcku__zpmcf = nlgg__alj.pipeline_class(ppceh__osdw, zdr__sknq,
            None, None, None, flags, None)
        rlcpu__zceb = InlineWorker(ppceh__osdw, zdr__sknq, nlgg__alj.locals,
            kfcku__zpmcf, flags, None)
        erc__xzwi = syfo__wdla.dispatcher.get_call_template
        tzr__qjdm, lbs__zeksv, yic__mgjwx, kws = erc__xzwi(xqd__scxnq, kws)
        if yic__mgjwx in self._inline_overloads:
            return self._inline_overloads[yic__mgjwx]['iinfo'].signature
        ir = rlcpu__zceb.run_untyped_passes(syfo__wdla.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, zdr__sknq, ir, yic__mgjwx, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, yic__mgjwx, None)
        self._inline_overloads[sig.args] = {'folded_args': yic__mgjwx}
        izil__upp = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = izil__upp
        if not self._inline.is_always_inline:
            sig = syfo__wdla.get_call_type(self.context, xqd__scxnq, kws)
            self._compiled_overloads[sig.args] = syfo__wdla.get_overload(sig)
        dnk__xdieq = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': yic__mgjwx,
            'iinfo': dnk__xdieq}
    else:
        sig = syfo__wdla.get_call_type(self.context, xqd__scxnq, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = syfo__wdla.get_overload(sig)
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
    qnsyh__etn = [True, False]
    xtz__cfyg = [False, True]
    cctj__hmcfb = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    gtprx__rpaw = get_local_target(context)
    ejqh__xsksg = utils.order_by_target_specificity(gtprx__rpaw, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for kpscb__wgip in ejqh__xsksg:
        ygkqb__myamd = kpscb__wgip(context)
        wmizg__onon = qnsyh__etn if ygkqb__myamd.prefer_literal else xtz__cfyg
        wmizg__onon = [True] if getattr(ygkqb__myamd, '_no_unliteral', False
            ) else wmizg__onon
        for mqq__axvr in wmizg__onon:
            try:
                if mqq__axvr:
                    sig = ygkqb__myamd.apply(args, kws)
                else:
                    ozoz__mek = tuple([_unlit_non_poison(a) for a in args])
                    vren__ptvqf = {eefhl__zjfn: _unlit_non_poison(tij__ygkm
                        ) for eefhl__zjfn, tij__ygkm in kws.items()}
                    sig = ygkqb__myamd.apply(ozoz__mek, vren__ptvqf)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    cctj__hmcfb.add_error(ygkqb__myamd, False, e, mqq__axvr)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = ygkqb__myamd.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    oyb__mojka = getattr(ygkqb__myamd, 'cases', None)
                    if oyb__mojka is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            oyb__mojka)
                    else:
                        msg = 'No match.'
                    cctj__hmcfb.add_error(ygkqb__myamd, True, msg, mqq__axvr)
    cctj__hmcfb.raise_error()


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
    tzr__qjdm = self.template(context)
    bfsc__pjsaz = None
    drumr__mwwhh = None
    hlq__hxf = None
    wmizg__onon = [True, False] if tzr__qjdm.prefer_literal else [False, True]
    wmizg__onon = [True] if getattr(tzr__qjdm, '_no_unliteral', False
        ) else wmizg__onon
    for mqq__axvr in wmizg__onon:
        if mqq__axvr:
            try:
                hlq__hxf = tzr__qjdm.apply(args, kws)
            except Exception as chcw__dap:
                if isinstance(chcw__dap, errors.ForceLiteralArg):
                    raise chcw__dap
                bfsc__pjsaz = chcw__dap
                hlq__hxf = None
            else:
                break
        else:
            nac__ehsy = tuple([_unlit_non_poison(a) for a in args])
            zxjp__xls = {eefhl__zjfn: _unlit_non_poison(tij__ygkm) for 
                eefhl__zjfn, tij__ygkm in kws.items()}
            erhil__myo = nac__ehsy == args and kws == zxjp__xls
            if not erhil__myo and hlq__hxf is None:
                try:
                    hlq__hxf = tzr__qjdm.apply(nac__ehsy, zxjp__xls)
                except Exception as chcw__dap:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        chcw__dap, errors.NumbaError):
                        raise chcw__dap
                    if isinstance(chcw__dap, errors.ForceLiteralArg):
                        if tzr__qjdm.prefer_literal:
                            raise chcw__dap
                    drumr__mwwhh = chcw__dap
                else:
                    break
    if hlq__hxf is None and (drumr__mwwhh is not None or bfsc__pjsaz is not
        None):
        cgb__dwok = '- Resolution failure for {} arguments:\n{}\n'
        nitsv__zmkmj = _termcolor.highlight(cgb__dwok)
        if numba.core.config.DEVELOPER_MODE:
            yckmx__vfcb = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    ggg__irhi = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    ggg__irhi = ['']
                cdvzn__kieh = '\n{}'.format(2 * yckmx__vfcb)
                yxzy__rufk = _termcolor.reset(cdvzn__kieh + cdvzn__kieh.
                    join(_bt_as_lines(ggg__irhi)))
                return _termcolor.reset(yxzy__rufk)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            rzeag__wnhp = str(e)
            rzeag__wnhp = rzeag__wnhp if rzeag__wnhp else str(repr(e)
                ) + add_bt(e)
            gafqy__ama = errors.TypingError(textwrap.dedent(rzeag__wnhp))
            return nitsv__zmkmj.format(literalness, str(gafqy__ama))
        import bodo
        if isinstance(bfsc__pjsaz, bodo.utils.typing.BodoError):
            raise bfsc__pjsaz
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', bfsc__pjsaz) +
                nested_msg('non-literal', drumr__mwwhh))
        else:
            if 'missing a required argument' in bfsc__pjsaz.msg:
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
            raise errors.TypingError(msg, loc=bfsc__pjsaz.loc)
    return hlq__hxf


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
    haia__ykzr = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=haia__ykzr)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            ftqak__qteiv = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), ftqak__qteiv)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    hzgng__zcmqa = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            hzgng__zcmqa.append(types.Omitted(a.value))
        else:
            hzgng__zcmqa.append(self.typeof_pyval(a))
    wyocg__vuu = None
    try:
        error = None
        wyocg__vuu = self.compile(tuple(hzgng__zcmqa))
    except errors.ForceLiteralArg as e:
        nmcd__ocmyh = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if nmcd__ocmyh:
            dohj__ftvag = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            ploqu__brdfq = ', '.join('Arg #{} is {}'.format(i, args[i]) for
                i in sorted(nmcd__ocmyh))
            raise errors.CompilerError(dohj__ftvag.format(ploqu__brdfq))
        xqd__scxnq = []
        try:
            for i, tij__ygkm in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        xqd__scxnq.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        xqd__scxnq.append(types.literal(args[i]))
                else:
                    xqd__scxnq.append(args[i])
            args = xqd__scxnq
        except (OSError, FileNotFoundError) as rdsph__dxwd:
            error = FileNotFoundError(str(rdsph__dxwd) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                wyocg__vuu = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        plrq__scxrm = []
        for i, jqf__pssc in enumerate(args):
            val = jqf__pssc.value if isinstance(jqf__pssc, numba.core.
                dispatcher.OmittedArg) else jqf__pssc
            try:
                fndw__onrr = typeof(val, Purpose.argument)
            except ValueError as irkkz__olnd:
                plrq__scxrm.append((i, str(irkkz__olnd)))
            else:
                if fndw__onrr is None:
                    plrq__scxrm.append((i,
                        f'cannot determine Numba type of value {val}'))
        if plrq__scxrm:
            hvtc__uvhy = '\n'.join(f'- argument {i}: {twaft__gnk}' for i,
                twaft__gnk in plrq__scxrm)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{hvtc__uvhy}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                uxvr__eplyq = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                gxhcn__remz = False
                for skn__runv in uxvr__eplyq:
                    if skn__runv in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        gxhcn__remz = True
                        break
                if not gxhcn__remz:
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
                ftqak__qteiv = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), ftqak__qteiv)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return wyocg__vuu


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
    for dccu__humti in cres.library._codegen._engine._defined_symbols:
        if dccu__humti.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in dccu__humti and (
            'bodo_gb_udf_update_local' in dccu__humti or 
            'bodo_gb_udf_combine' in dccu__humti or 'bodo_gb_udf_eval' in
            dccu__humti or 'bodo_gb_apply_general_udfs' in dccu__humti):
            gb_agg_cfunc_addr[dccu__humti
                ] = cres.library.get_pointer_to_function(dccu__humti)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for dccu__humti in cres.library._codegen._engine._defined_symbols:
        if dccu__humti.startswith('cfunc') and ('get_join_cond_addr' not in
            dccu__humti or 'bodo_join_gen_cond' in dccu__humti):
            join_gen_cond_cfunc_addr[dccu__humti
                ] = cres.library.get_pointer_to_function(dccu__humti)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    kbwtb__eck = self._get_dispatcher_for_current_target()
    if kbwtb__eck is not self:
        return kbwtb__eck.compile(sig)
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
            xed__xtx = self.overloads.get(tuple(args))
            if xed__xtx is not None:
                return xed__xtx.entry_point
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
            clij__dro = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=clij__dro):
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
                lxv__sitn = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in lxv__sitn:
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
    qad__lxg = self._final_module
    pzwa__zwve = []
    hauxh__rwbon = 0
    for fn in qad__lxg.functions:
        hauxh__rwbon += 1
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
            pzwa__zwve.append(fn.name)
    if hauxh__rwbon == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if pzwa__zwve:
        qad__lxg = qad__lxg.clone()
        for name in pzwa__zwve:
            qad__lxg.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = qad__lxg
    return qad__lxg


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
    for hbg__kqw in self.constraints:
        loc = hbg__kqw.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                hbg__kqw(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                aglz__uvs = numba.core.errors.TypingError(str(e), loc=
                    hbg__kqw.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(aglz__uvs, e))
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
                    aglz__uvs = numba.core.errors.TypingError(msg.format(
                        con=hbg__kqw, err=str(e)), loc=hbg__kqw.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(aglz__uvs, e))
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
    for qrd__dwh in self._failures.values():
        for kqpn__svw in qrd__dwh:
            if isinstance(kqpn__svw.error, ForceLiteralArg):
                raise kqpn__svw.error
            if isinstance(kqpn__svw.error, bodo.utils.typing.BodoError):
                raise kqpn__svw.error
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
    yimz__habk = False
    dqpte__larz = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        rnpu__tvjyf = set()
        rabg__rav = lives & alias_set
        for tij__ygkm in rabg__rav:
            rnpu__tvjyf |= alias_map[tij__ygkm]
        lives_n_aliases = lives | rnpu__tvjyf | arg_aliases
        if type(stmt) in remove_dead_extensions:
            tml__qtyur = remove_dead_extensions[type(stmt)]
            stmt = tml__qtyur(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                yimz__habk = True
                continue
        if isinstance(stmt, ir.Assign):
            ovhbh__ncq = stmt.target
            ydlyc__vjd = stmt.value
            if ovhbh__ncq.name not in lives:
                if has_no_side_effect(ydlyc__vjd, lives_n_aliases, call_table):
                    yimz__habk = True
                    continue
                if isinstance(ydlyc__vjd, ir.Expr
                    ) and ydlyc__vjd.op == 'call' and call_table[ydlyc__vjd
                    .func.name] == ['astype']:
                    panki__zjo = guard(get_definition, func_ir, ydlyc__vjd.func
                        )
                    if (panki__zjo is not None and panki__zjo.op ==
                        'getattr' and isinstance(typemap[panki__zjo.value.
                        name], types.Array) and panki__zjo.attr == 'astype'):
                        yimz__habk = True
                        continue
            if saved_array_analysis and ovhbh__ncq.name in lives and is_expr(
                ydlyc__vjd, 'getattr'
                ) and ydlyc__vjd.attr == 'shape' and is_array_typ(typemap[
                ydlyc__vjd.value.name]) and ydlyc__vjd.value.name not in lives:
                hsvfx__wak = {tij__ygkm: eefhl__zjfn for eefhl__zjfn,
                    tij__ygkm in func_ir.blocks.items()}
                if block in hsvfx__wak:
                    label = hsvfx__wak[block]
                    tkb__zvvcd = saved_array_analysis.get_equiv_set(label)
                    nqlo__ppu = tkb__zvvcd.get_equiv_set(ydlyc__vjd.value)
                    if nqlo__ppu is not None:
                        for tij__ygkm in nqlo__ppu:
                            if tij__ygkm.endswith('#0'):
                                tij__ygkm = tij__ygkm[:-2]
                            if tij__ygkm in typemap and is_array_typ(typemap
                                [tij__ygkm]) and tij__ygkm in lives:
                                ydlyc__vjd.value = ir.Var(ydlyc__vjd.value.
                                    scope, tij__ygkm, ydlyc__vjd.value.loc)
                                yimz__habk = True
                                break
            if isinstance(ydlyc__vjd, ir.Var
                ) and ovhbh__ncq.name == ydlyc__vjd.name:
                yimz__habk = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                yimz__habk = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            qih__efyq = analysis.ir_extension_usedefs[type(stmt)]
            vnsgv__bjstb, uxgir__fzzu = qih__efyq(stmt)
            lives -= uxgir__fzzu
            lives |= vnsgv__bjstb
        else:
            lives |= {tij__ygkm.name for tij__ygkm in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                poh__uuh = set()
                if isinstance(ydlyc__vjd, ir.Expr):
                    poh__uuh = {tij__ygkm.name for tij__ygkm in ydlyc__vjd.
                        list_vars()}
                if ovhbh__ncq.name not in poh__uuh:
                    lives.remove(ovhbh__ncq.name)
        dqpte__larz.append(stmt)
    dqpte__larz.reverse()
    block.body = dqpte__larz
    return yimz__habk


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            cktw__nue, = args
            if isinstance(cktw__nue, types.IterableType):
                dtype = cktw__nue.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), cktw__nue)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    xgbil__hgt = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (xgbil__hgt, self.dtype)
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
        except LiteralTypingError as cbpp__zbh:
            return
    try:
        return literal(value)
    except LiteralTypingError as cbpp__zbh:
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
        kkafb__ukqan = py_func.__qualname__
    except AttributeError as cbpp__zbh:
        kkafb__ukqan = py_func.__name__
    ulzf__hih = inspect.getfile(py_func)
    for cls in self._locator_classes:
        afx__xrz = cls.from_function(py_func, ulzf__hih)
        if afx__xrz is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (kkafb__ukqan, ulzf__hih))
    self._locator = afx__xrz
    djoy__anwtm = inspect.getfile(py_func)
    mkhzv__fxye = os.path.splitext(os.path.basename(djoy__anwtm))[0]
    if ulzf__hih.startswith('<ipython-'):
        oee__dvcm = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', mkhzv__fxye, count=1)
        if oee__dvcm == mkhzv__fxye:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        mkhzv__fxye = oee__dvcm
    lhqhs__zhrq = '%s.%s' % (mkhzv__fxye, kkafb__ukqan)
    bye__xrxui = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(lhqhs__zhrq, bye__xrxui
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    aqw__ydhwt = list(filter(lambda a: self._istuple(a.name), args))
    if len(aqw__ydhwt) == 2 and fn.__name__ == 'add':
        lloya__fantp = self.typemap[aqw__ydhwt[0].name]
        fto__wsbp = self.typemap[aqw__ydhwt[1].name]
        if lloya__fantp.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                aqw__ydhwt[1]))
        if fto__wsbp.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                aqw__ydhwt[0]))
        try:
            tbya__habh = [equiv_set.get_shape(x) for x in aqw__ydhwt]
            if None in tbya__habh:
                return None
            evsx__wup = sum(tbya__habh, ())
            return ArrayAnalysis.AnalyzeResult(shape=evsx__wup)
        except GuardException as cbpp__zbh:
            return None
    wgdp__cri = list(filter(lambda a: self._isarray(a.name), args))
    require(len(wgdp__cri) > 0)
    iiqzn__ciayi = [x.name for x in wgdp__cri]
    uqjss__qcc = [self.typemap[x.name].ndim for x in wgdp__cri]
    ndwqf__ffgjm = max(uqjss__qcc)
    require(ndwqf__ffgjm > 0)
    tbya__habh = [equiv_set.get_shape(x) for x in wgdp__cri]
    if any(a is None for a in tbya__habh):
        return ArrayAnalysis.AnalyzeResult(shape=wgdp__cri[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, wgdp__cri))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, tbya__habh,
        iiqzn__ciayi)


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
    hol__fispl = code_obj.code
    wlrv__khdav = len(hol__fispl.co_freevars)
    cqrx__orrdv = hol__fispl.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        gsbq__itofi, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        cqrx__orrdv = [tij__ygkm.name for tij__ygkm in gsbq__itofi]
    dje__nxtqd = caller_ir.func_id.func.__globals__
    try:
        dje__nxtqd = getattr(code_obj, 'globals', dje__nxtqd)
    except KeyError as cbpp__zbh:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    drt__phz = []
    for x in cqrx__orrdv:
        try:
            sqw__iueo = caller_ir.get_definition(x)
        except KeyError as cbpp__zbh:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(sqw__iueo, (ir.Const, ir.Global, ir.FreeVar)):
            val = sqw__iueo.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                pjsw__zaa = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                dje__nxtqd[pjsw__zaa] = bodo.jit(distributed=False)(val)
                dje__nxtqd[pjsw__zaa].is_nested_func = True
                val = pjsw__zaa
            if isinstance(val, CPUDispatcher):
                pjsw__zaa = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                dje__nxtqd[pjsw__zaa] = val
                val = pjsw__zaa
            drt__phz.append(val)
        elif isinstance(sqw__iueo, ir.Expr
            ) and sqw__iueo.op == 'make_function':
            faqt__ldqo = convert_code_obj_to_function(sqw__iueo, caller_ir)
            pjsw__zaa = ir_utils.mk_unique_var('nested_func').replace('.', '_')
            dje__nxtqd[pjsw__zaa] = bodo.jit(distributed=False)(faqt__ldqo)
            dje__nxtqd[pjsw__zaa].is_nested_func = True
            drt__phz.append(pjsw__zaa)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    tcv__olew = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        drt__phz)])
    ptgm__fieg = ','.join([('c_%d' % i) for i in range(wlrv__khdav)])
    bqrty__ter = list(hol__fispl.co_varnames)
    qugvj__wurh = 0
    puhbz__rwukz = hol__fispl.co_argcount
    orn__ivsyh = caller_ir.get_definition(code_obj.defaults)
    if orn__ivsyh is not None:
        if isinstance(orn__ivsyh, tuple):
            d = [caller_ir.get_definition(x).value for x in orn__ivsyh]
            oke__aww = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in orn__ivsyh.items]
            oke__aww = tuple(d)
        qugvj__wurh = len(oke__aww)
    rvn__zkbm = puhbz__rwukz - qugvj__wurh
    hjpgg__uil = ','.join([('%s' % bqrty__ter[i]) for i in range(rvn__zkbm)])
    if qugvj__wurh:
        rcz__zgo = [('%s = %s' % (bqrty__ter[i + rvn__zkbm], oke__aww[i])) for
            i in range(qugvj__wurh)]
        hjpgg__uil += ', '
        hjpgg__uil += ', '.join(rcz__zgo)
    return _create_function_from_code_obj(hol__fispl, tcv__olew, hjpgg__uil,
        ptgm__fieg, dje__nxtqd)


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
    for arsvq__cvf, (oaco__fvg, abutw__bpth) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % abutw__bpth)
            fsej__insv = _pass_registry.get(oaco__fvg).pass_inst
            if isinstance(fsej__insv, CompilerPass):
                self._runPass(arsvq__cvf, fsej__insv, state)
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
                    pipeline_name, abutw__bpth)
                npdg__adj = self._patch_error(msg, e)
                raise npdg__adj
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
    adb__ziaa = None
    uxgir__fzzu = {}

    def lookup(var, already_seen, varonly=True):
        val = uxgir__fzzu.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    kefv__pvt = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        ovhbh__ncq = stmt.target
        ydlyc__vjd = stmt.value
        uxgir__fzzu[ovhbh__ncq.name] = ydlyc__vjd
        if isinstance(ydlyc__vjd, ir.Var) and ydlyc__vjd.name in uxgir__fzzu:
            ydlyc__vjd = lookup(ydlyc__vjd, set())
        if isinstance(ydlyc__vjd, ir.Expr):
            pljl__nooxc = set(lookup(tij__ygkm, set(), True).name for
                tij__ygkm in ydlyc__vjd.list_vars())
            if name in pljl__nooxc:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(ydlyc__vjd)]
                bdcg__losew = [x for x, qaawh__cji in args if qaawh__cji.
                    name != name]
                args = [(x, qaawh__cji) for x, qaawh__cji in args if x !=
                    qaawh__cji.name]
                gko__hcoh = dict(args)
                if len(bdcg__losew) == 1:
                    gko__hcoh[bdcg__losew[0]] = ir.Var(ovhbh__ncq.scope, 
                        name + '#init', ovhbh__ncq.loc)
                replace_vars_inner(ydlyc__vjd, gko__hcoh)
                adb__ziaa = nodes[i:]
                break
    return adb__ziaa


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
        gyjj__fegs = expand_aliases({tij__ygkm.name for tij__ygkm in stmt.
            list_vars()}, alias_map, arg_aliases)
        zjt__vrzqe = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        sptj__dgu = expand_aliases({tij__ygkm.name for tij__ygkm in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        uoea__jjrxm = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(zjt__vrzqe & sptj__dgu | uoea__jjrxm & gyjj__fegs) == 0:
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
    psn__dkwoy = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            psn__dkwoy.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                psn__dkwoy.update(get_parfor_writes(stmt, func_ir))
    return psn__dkwoy


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    psn__dkwoy = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        psn__dkwoy.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        psn__dkwoy = {tij__ygkm.name for tij__ygkm in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        psn__dkwoy = {tij__ygkm.name for tij__ygkm in stmt.get_live_out_vars()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            psn__dkwoy.update({tij__ygkm.name for tij__ygkm in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        tddbn__syuo = guard(find_callname, func_ir, stmt.value)
        if tddbn__syuo in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'copy_array_element', 'bodo.libs.array_kernels'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext'), (
            'tuple_list_to_array', 'bodo.utils.utils')):
            psn__dkwoy.add(stmt.value.args[0].name)
        if tddbn__syuo == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            psn__dkwoy.add(stmt.value.args[1].name)
    return psn__dkwoy


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
        tml__qtyur = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        grv__siko = tml__qtyur.format(self, msg)
        self.args = grv__siko,
    else:
        tml__qtyur = _termcolor.errmsg('{0}')
        grv__siko = tml__qtyur.format(self)
        self.args = grv__siko,
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
        for yijs__yti in options['distributed']:
            dist_spec[yijs__yti] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for yijs__yti in options['distributed_block']:
            dist_spec[yijs__yti] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    mqyy__tet = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, zmyz__jopr in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(zmyz__jopr)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    fjcc__pxma = {}
    for abmva__cfcqm in reversed(inspect.getmro(cls)):
        fjcc__pxma.update(abmva__cfcqm.__dict__)
    oxy__cbcd, ooskl__lbxkx, pftj__hgm, aew__gbu = {}, {}, {}, {}
    for eefhl__zjfn, tij__ygkm in fjcc__pxma.items():
        if isinstance(tij__ygkm, pytypes.FunctionType):
            oxy__cbcd[eefhl__zjfn] = tij__ygkm
        elif isinstance(tij__ygkm, property):
            ooskl__lbxkx[eefhl__zjfn] = tij__ygkm
        elif isinstance(tij__ygkm, staticmethod):
            pftj__hgm[eefhl__zjfn] = tij__ygkm
        else:
            aew__gbu[eefhl__zjfn] = tij__ygkm
    rdmj__fcy = (set(oxy__cbcd) | set(ooskl__lbxkx) | set(pftj__hgm)) & set(
        spec)
    if rdmj__fcy:
        raise NameError('name shadowing: {0}'.format(', '.join(rdmj__fcy)))
    gnm__gdhpm = aew__gbu.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(aew__gbu)
    if aew__gbu:
        msg = 'class members are not yet supported: {0}'
        xwyq__opeu = ', '.join(aew__gbu.keys())
        raise TypeError(msg.format(xwyq__opeu))
    for eefhl__zjfn, tij__ygkm in ooskl__lbxkx.items():
        if tij__ygkm.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(eefhl__zjfn)
                )
    jit_methods = {eefhl__zjfn: bodo.jit(returns_maybe_distributed=
        mqyy__tet)(tij__ygkm) for eefhl__zjfn, tij__ygkm in oxy__cbcd.items()}
    jit_props = {}
    for eefhl__zjfn, tij__ygkm in ooskl__lbxkx.items():
        cnamd__fez = {}
        if tij__ygkm.fget:
            cnamd__fez['get'] = bodo.jit(tij__ygkm.fget)
        if tij__ygkm.fset:
            cnamd__fez['set'] = bodo.jit(tij__ygkm.fset)
        jit_props[eefhl__zjfn] = cnamd__fez
    jit_static_methods = {eefhl__zjfn: bodo.jit(tij__ygkm.__func__) for 
        eefhl__zjfn, tij__ygkm in pftj__hgm.items()}
    gxeq__uddr = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    vjbt__mvvf = dict(class_type=gxeq__uddr, __doc__=gnm__gdhpm)
    vjbt__mvvf.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), vjbt__mvvf)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, gxeq__uddr)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(gxeq__uddr, typingctx, targetctx).register()
    as_numba_type.register(cls, gxeq__uddr.instance_type)
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
    eox__tkste = ','.join('{0}:{1}'.format(eefhl__zjfn, tij__ygkm) for 
        eefhl__zjfn, tij__ygkm in struct.items())
    quz__ncohr = ','.join('{0}:{1}'.format(eefhl__zjfn, tij__ygkm) for 
        eefhl__zjfn, tij__ygkm in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), eox__tkste, quz__ncohr)
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
    rryfd__qtvs = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if rryfd__qtvs is None:
        return
    dxuz__stwe, vbhp__mjm = rryfd__qtvs
    for a in itertools.chain(dxuz__stwe, vbhp__mjm.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, dxuz__stwe, vbhp__mjm)
    except ForceLiteralArg as e:
        kam__crdj = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(kam__crdj, self.kws)
        drsh__ctn = set()
        okrf__rlp = set()
        vto__nkdk = {}
        for arsvq__cvf in e.requested_args:
            hcp__bly = typeinfer.func_ir.get_definition(folded[arsvq__cvf])
            if isinstance(hcp__bly, ir.Arg):
                drsh__ctn.add(hcp__bly.index)
                if hcp__bly.index in e.file_infos:
                    vto__nkdk[hcp__bly.index] = e.file_infos[hcp__bly.index]
            else:
                okrf__rlp.add(arsvq__cvf)
        if okrf__rlp:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif drsh__ctn:
            raise ForceLiteralArg(drsh__ctn, loc=self.loc, file_infos=vto__nkdk
                )
    if sig is None:
        tnnz__xusgf = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in dxuz__stwe]
        args += [('%s=%s' % (eefhl__zjfn, tij__ygkm)) for eefhl__zjfn,
            tij__ygkm in sorted(vbhp__mjm.items())]
        arbfe__zuif = tnnz__xusgf.format(fnty, ', '.join(map(str, args)))
        dbeu__oggh = context.explain_function_type(fnty)
        msg = '\n'.join([arbfe__zuif, dbeu__oggh])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        ewsur__rboah = context.unify_pairs(sig.recvr, fnty.this)
        if ewsur__rboah is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if ewsur__rboah is not None and ewsur__rboah.is_precise():
            uch__ooawg = fnty.copy(this=ewsur__rboah)
            typeinfer.propagate_refined_type(self.func, uch__ooawg)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            uhw__pylay = target.getone()
            if context.unify_pairs(uhw__pylay, sig.return_type) == uhw__pylay:
                sig = sig.replace(return_type=uhw__pylay)
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
        dohj__ftvag = '*other* must be a {} but got a {} instead'
        raise TypeError(dohj__ftvag.format(ForceLiteralArg, type(other)))
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
    urhu__oasj = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for eefhl__zjfn, tij__ygkm in kwargs.items():
        psbph__agpu = None
        try:
            bri__lqir = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var(
                'dummy'), loc)
            func_ir._definitions[bri__lqir.name] = [tij__ygkm]
            psbph__agpu = get_const_value_inner(func_ir, bri__lqir)
            func_ir._definitions.pop(bri__lqir.name)
            if isinstance(psbph__agpu, str):
                psbph__agpu = sigutils._parse_signature_string(psbph__agpu)
            if isinstance(psbph__agpu, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {eefhl__zjfn} is annotated as type class {psbph__agpu}."""
                    )
            assert isinstance(psbph__agpu, types.Type)
            if isinstance(psbph__agpu, (types.List, types.Set)):
                psbph__agpu = psbph__agpu.copy(reflected=False)
            urhu__oasj[eefhl__zjfn] = psbph__agpu
        except BodoError as cbpp__zbh:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(psbph__agpu, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(tij__ygkm, ir.Global):
                    msg = f'Global {tij__ygkm.name!r} is not defined.'
                if isinstance(tij__ygkm, ir.FreeVar):
                    msg = f'Freevar {tij__ygkm.name!r} is not defined.'
            if isinstance(tij__ygkm, ir.Expr) and tij__ygkm.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=eefhl__zjfn, msg=msg, loc=loc)
    for name, typ in urhu__oasj.items():
        self._legalize_arg_type(name, typ, loc)
    return urhu__oasj


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
    jjce__rsx = inst.arg
    assert jjce__rsx > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(jjce__rsx)]))
    tmps = [state.make_temp() for _ in range(jjce__rsx - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    wddg__rumm = ir.Global('format', format, loc=self.loc)
    self.store(value=wddg__rumm, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    acap__mlb = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=acap__mlb, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    jjce__rsx = inst.arg
    assert jjce__rsx > 0, 'invalid BUILD_STRING count'
    pzwu__hlxj = self.get(strings[0])
    for other, euuzb__rhhf in zip(strings[1:], tmps):
        other = self.get(other)
        ljuck__iejrz = ir.Expr.binop(operator.add, lhs=pzwu__hlxj, rhs=
            other, loc=self.loc)
        self.store(ljuck__iejrz, euuzb__rhhf)
        pzwu__hlxj = self.get(euuzb__rhhf)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    flaqf__pwurn = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, flaqf__pwurn])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    gber__yabyc = mk_unique_var(f'{var_name}')
    zfl__uzci = gber__yabyc.replace('<', '_').replace('>', '_')
    zfl__uzci = zfl__uzci.replace('.', '_').replace('$', '_v')
    return zfl__uzci


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
                dgg__fwchu = get_overload_const_str(val2)
                if dgg__fwchu != 'ns':
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
        sqj__gqob = states['defmap']
        if len(sqj__gqob) == 0:
            umife__szmx = assign.target
            numba.core.ssa._logger.debug('first assign: %s', umife__szmx)
            if umife__szmx.name not in scope.localvars:
                umife__szmx = scope.define(assign.target.name, loc=assign.loc)
        else:
            umife__szmx = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=umife__szmx, value=assign.value, loc=
            assign.loc)
        sqj__gqob[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    zirh__trqw = []
    for eefhl__zjfn, tij__ygkm in typing.npydecl.registry.globals:
        if eefhl__zjfn == func:
            zirh__trqw.append(tij__ygkm)
    for eefhl__zjfn, tij__ygkm in typing.templates.builtin_registry.globals:
        if eefhl__zjfn == func:
            zirh__trqw.append(tij__ygkm)
    if len(zirh__trqw) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return zirh__trqw


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    uidp__mrvl = {}
    jdqwb__cgf = find_topo_order(blocks)
    kepk__ltt = {}
    for label in jdqwb__cgf:
        block = blocks[label]
        dqpte__larz = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                ovhbh__ncq = stmt.target.name
                ydlyc__vjd = stmt.value
                if (ydlyc__vjd.op == 'getattr' and ydlyc__vjd.attr in
                    arr_math and isinstance(typemap[ydlyc__vjd.value.name],
                    types.npytypes.Array)):
                    ydlyc__vjd = stmt.value
                    uejzx__dhcex = ydlyc__vjd.value
                    uidp__mrvl[ovhbh__ncq] = uejzx__dhcex
                    scope = uejzx__dhcex.scope
                    loc = uejzx__dhcex.loc
                    ohvg__kqif = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[ohvg__kqif.name] = types.misc.Module(numpy)
                    tkbbo__atq = ir.Global('np', numpy, loc)
                    fygdv__ogyy = ir.Assign(tkbbo__atq, ohvg__kqif, loc)
                    ydlyc__vjd.value = ohvg__kqif
                    dqpte__larz.append(fygdv__ogyy)
                    func_ir._definitions[ohvg__kqif.name] = [tkbbo__atq]
                    func = getattr(numpy, ydlyc__vjd.attr)
                    snbat__xlw = get_np_ufunc_typ_lst(func)
                    kepk__ltt[ovhbh__ncq] = snbat__xlw
                if (ydlyc__vjd.op == 'call' and ydlyc__vjd.func.name in
                    uidp__mrvl):
                    uejzx__dhcex = uidp__mrvl[ydlyc__vjd.func.name]
                    bmqel__aswea = calltypes.pop(ydlyc__vjd)
                    epbnp__vwp = bmqel__aswea.args[:len(ydlyc__vjd.args)]
                    hkdbw__yom = {name: typemap[tij__ygkm.name] for name,
                        tij__ygkm in ydlyc__vjd.kws}
                    yha__dur = kepk__ltt[ydlyc__vjd.func.name]
                    src__oiag = None
                    for qkbl__zozj in yha__dur:
                        try:
                            src__oiag = qkbl__zozj.get_call_type(typingctx,
                                [typemap[uejzx__dhcex.name]] + list(
                                epbnp__vwp), hkdbw__yom)
                            typemap.pop(ydlyc__vjd.func.name)
                            typemap[ydlyc__vjd.func.name] = qkbl__zozj
                            calltypes[ydlyc__vjd] = src__oiag
                            break
                        except Exception as cbpp__zbh:
                            pass
                    if src__oiag is None:
                        raise TypeError(
                            f'No valid template found for {ydlyc__vjd.func.name}'
                            )
                    ydlyc__vjd.args = [uejzx__dhcex] + ydlyc__vjd.args
            dqpte__larz.append(stmt)
        block.body = dqpte__larz


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    rvl__gqtz = ufunc.nin
    maxcl__tms = ufunc.nout
    rvn__zkbm = ufunc.nargs
    assert rvn__zkbm == rvl__gqtz + maxcl__tms
    if len(args) < rvl__gqtz:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), rvl__gqtz))
    if len(args) > rvn__zkbm:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), rvn__zkbm))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    aokog__ozdm = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    matjj__bodg = max(aokog__ozdm)
    iuk__vdsl = args[rvl__gqtz:]
    if not all(d == matjj__bodg for d in aokog__ozdm[rvl__gqtz:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(gyetv__pxjgx, types.ArrayCompatible) and not
        isinstance(gyetv__pxjgx, types.Bytes) for gyetv__pxjgx in iuk__vdsl):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(gyetv__pxjgx.mutable for gyetv__pxjgx in iuk__vdsl):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    tdjk__hnz = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    viy__qdctq = None
    if matjj__bodg > 0 and len(iuk__vdsl) < ufunc.nout:
        viy__qdctq = 'C'
        easoo__fuzf = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in easoo__fuzf and 'F' in easoo__fuzf:
            viy__qdctq = 'F'
    return tdjk__hnz, iuk__vdsl, matjj__bodg, viy__qdctq


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
        fqx__tznai = 'Dict.key_type cannot be of type {}'
        raise TypingError(fqx__tznai.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        fqx__tznai = 'Dict.value_type cannot be of type {}'
        raise TypingError(fqx__tznai.format(valty))
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
    ibq__tpzl = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[ibq__tpzl]
        return impl, args
    except KeyError as cbpp__zbh:
        pass
    impl, args = self._build_impl(ibq__tpzl, args, kws)
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
    brts__jktc = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            lruv__kxmyd = block.body[-1]
            if isinstance(lruv__kxmyd, ir.Branch):
                if len(blocks[lruv__kxmyd.truebr].body) == 1 and len(blocks
                    [lruv__kxmyd.falsebr].body) == 1:
                    fjb__zjqov = blocks[lruv__kxmyd.truebr].body[0]
                    tzcse__kjut = blocks[lruv__kxmyd.falsebr].body[0]
                    if isinstance(fjb__zjqov, ir.Jump) and isinstance(
                        tzcse__kjut, ir.Jump
                        ) and fjb__zjqov.target == tzcse__kjut.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(fjb__zjqov
                            .target, lruv__kxmyd.loc)
                        brts__jktc = True
                elif len(blocks[lruv__kxmyd.truebr].body) == 1:
                    fjb__zjqov = blocks[lruv__kxmyd.truebr].body[0]
                    if isinstance(fjb__zjqov, ir.Jump
                        ) and fjb__zjqov.target == lruv__kxmyd.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(fjb__zjqov
                            .target, lruv__kxmyd.loc)
                        brts__jktc = True
                elif len(blocks[lruv__kxmyd.falsebr].body) == 1:
                    tzcse__kjut = blocks[lruv__kxmyd.falsebr].body[0]
                    if isinstance(tzcse__kjut, ir.Jump
                        ) and tzcse__kjut.target == lruv__kxmyd.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(tzcse__kjut
                            .target, lruv__kxmyd.loc)
                        brts__jktc = True
    return brts__jktc


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        zohoo__eye = find_topo_order(parfor.loop_body)
    mvtfi__ixehu = zohoo__eye[0]
    cgd__lcftw = {}
    _update_parfor_get_setitems(parfor.loop_body[mvtfi__ixehu].body, parfor
        .index_var, alias_map, cgd__lcftw, lives_n_aliases)
    kkh__rrh = set(cgd__lcftw.keys())
    for goqk__uwi in zohoo__eye:
        if goqk__uwi == mvtfi__ixehu:
            continue
        for stmt in parfor.loop_body[goqk__uwi].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            wret__owv = set(tij__ygkm.name for tij__ygkm in stmt.list_vars())
            xcmr__qjqf = wret__owv & kkh__rrh
            for a in xcmr__qjqf:
                cgd__lcftw.pop(a, None)
    for goqk__uwi in zohoo__eye:
        if goqk__uwi == mvtfi__ixehu:
            continue
        block = parfor.loop_body[goqk__uwi]
        ebj__drca = cgd__lcftw.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            ebj__drca, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    alkjj__ckjr = max(blocks.keys())
    rsrsx__qyt, qbe__nuxbz = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    pwdy__sqfa = ir.Jump(rsrsx__qyt, ir.Loc('parfors_dummy', -1))
    blocks[alkjj__ckjr].body.append(pwdy__sqfa)
    hkx__xasfn = compute_cfg_from_blocks(blocks)
    lizx__icpc = compute_use_defs(blocks)
    oetq__mluxl = compute_live_map(hkx__xasfn, blocks, lizx__icpc.usemap,
        lizx__icpc.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        dqpte__larz = []
        pcq__pary = {tij__ygkm.name for tij__ygkm in block.terminator.
            list_vars()}
        for xax__pxwbi, khvrn__dejzy in hkx__xasfn.successors(label):
            pcq__pary |= oetq__mluxl[xax__pxwbi]
        for stmt in reversed(block.body):
            rnpu__tvjyf = pcq__pary & alias_set
            for tij__ygkm in rnpu__tvjyf:
                pcq__pary |= alias_map[tij__ygkm]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in pcq__pary and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                tddbn__syuo = guard(find_callname, func_ir, stmt.value)
                if tddbn__syuo == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in pcq__pary and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            pcq__pary |= {tij__ygkm.name for tij__ygkm in stmt.list_vars()}
            dqpte__larz.append(stmt)
        dqpte__larz.reverse()
        block.body = dqpte__larz
    typemap.pop(qbe__nuxbz.name)
    blocks[alkjj__ckjr].body.pop()
    brts__jktc = True
    while brts__jktc:
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
        brts__jktc = trim_empty_parfor_branches(parfor)
    zfof__esnt = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        zfof__esnt &= len(block.body) == 0
    if zfof__esnt:
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
    tdd__vts = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                tdd__vts += 1
                parfor = stmt
                sagm__htzec = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = sagm__htzec.scope
                loc = ir.Loc('parfors_dummy', -1)
                gen__azwd = ir.Var(scope, mk_unique_var('$const'), loc)
                sagm__htzec.body.append(ir.Assign(ir.Const(0, loc),
                    gen__azwd, loc))
                sagm__htzec.body.append(ir.Return(gen__azwd, loc))
                hkx__xasfn = compute_cfg_from_blocks(parfor.loop_body)
                for gbwd__silfu in hkx__xasfn.dead_nodes():
                    del parfor.loop_body[gbwd__silfu]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                sagm__htzec = parfor.loop_body[max(parfor.loop_body.keys())]
                sagm__htzec.body.pop()
                sagm__htzec.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return tdd__vts


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    hkx__xasfn = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != hkx__xasfn.entry_point()
    kvt__ptt = list(filter(find_single_branch, blocks.keys()))
    rfm__kund = set()
    for label in kvt__ptt:
        inst = blocks[label].body[0]
        mibp__pzs = hkx__xasfn.predecessors(label)
        jwt__osya = True
        for kgkus__edxqc, ovx__uunf in mibp__pzs:
            block = blocks[kgkus__edxqc]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                jwt__osya = False
        if jwt__osya:
            rfm__kund.add(label)
    for label in rfm__kund:
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
            xed__xtx = self.overloads.get(tuple(args))
            if xed__xtx is not None:
                return xed__xtx.entry_point
            self._pre_compile(args, return_type, flags)
            nytjz__krk = self.func_ir
            clij__dro = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=clij__dro):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=nytjz__krk, args=args,
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
        pwdgg__rbyj = copy.deepcopy(flags)
        pwdgg__rbyj.no_rewrites = True

        def compile_local(the_ir, the_flags):
            uctzw__irvx = pipeline_class(typingctx, targetctx, library,
                args, return_type, the_flags, locals)
            return uctzw__irvx.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        byt__kjutl = compile_local(func_ir, pwdgg__rbyj)
        zcfa__lmkkf = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    zcfa__lmkkf = compile_local(func_ir, flags)
                except Exception as cbpp__zbh:
                    pass
        if zcfa__lmkkf is not None:
            cres = zcfa__lmkkf
        else:
            cres = byt__kjutl
        return cres
    else:
        uctzw__irvx = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return uctzw__irvx.compile_ir(func_ir=func_ir, lifted=lifted,
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
    irt__fyom = self.get_data_type(typ.dtype)
    njqjk__niqxx = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        njqjk__niqxx):
        fudp__iqxt = ary.ctypes.data
        roppr__xjf = self.add_dynamic_addr(builder, fudp__iqxt, info=str(
            type(fudp__iqxt)))
        ewws__gedxj = self.add_dynamic_addr(builder, id(ary), info=str(type
            (ary)))
        self.global_arrays.append(ary)
    else:
        qanbw__tnrzo = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            qanbw__tnrzo = qanbw__tnrzo.view('int64')
        val = bytearray(qanbw__tnrzo.data)
        dqjxs__bctoo = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)),
            val)
        roppr__xjf = cgutils.global_constant(builder, '.const.array.data',
            dqjxs__bctoo)
        roppr__xjf.align = self.get_abi_alignment(irt__fyom)
        ewws__gedxj = None
    xqr__osrj = self.get_value_type(types.intp)
    aan__wetf = [self.get_constant(types.intp, ynfx__thgpp) for ynfx__thgpp in
        ary.shape]
    sivw__sriq = lir.Constant(lir.ArrayType(xqr__osrj, len(aan__wetf)),
        aan__wetf)
    mzhs__mfntq = [self.get_constant(types.intp, ynfx__thgpp) for
        ynfx__thgpp in ary.strides]
    yaa__smq = lir.Constant(lir.ArrayType(xqr__osrj, len(mzhs__mfntq)),
        mzhs__mfntq)
    qitw__zug = self.get_constant(types.intp, ary.dtype.itemsize)
    mtc__zhg = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        mtc__zhg, qitw__zug, roppr__xjf.bitcast(self.get_value_type(types.
        CPointer(typ.dtype))), sivw__sriq, yaa__smq])


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
    qbpzv__xdge = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    dgcn__prz = lir.Function(module, qbpzv__xdge, name='nrt_atomic_{0}'.
        format(op))
    [umgek__ith] = dgcn__prz.args
    xbl__ymmsl = dgcn__prz.append_basic_block()
    builder = lir.IRBuilder(xbl__ymmsl)
    ddsry__pahj = lir.Constant(_word_type, 1)
    if False:
        jjns__sfqtn = builder.atomic_rmw(op, umgek__ith, ddsry__pahj,
            ordering=ordering)
        res = getattr(builder, op)(jjns__sfqtn, ddsry__pahj)
        builder.ret(res)
    else:
        jjns__sfqtn = builder.load(umgek__ith)
        bsnt__gde = getattr(builder, op)(jjns__sfqtn, ddsry__pahj)
        vnhc__rec = builder.icmp_signed('!=', jjns__sfqtn, lir.Constant(
            jjns__sfqtn.type, -1))
        with cgutils.if_likely(builder, vnhc__rec):
            builder.store(bsnt__gde, umgek__ith)
        builder.ret(bsnt__gde)
    return dgcn__prz


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
        zxmyy__fzcxf = state.targetctx.codegen()
        state.library = zxmyy__fzcxf.create_library(state.func_id.func_qualname
            )
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    irp__rflgy = state.func_ir
    typemap = state.typemap
    kuwj__gci = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    kfsk__nryo = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            irp__rflgy, typemap, kuwj__gci, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            xgwgn__utj = lowering.Lower(targetctx, library, fndesc,
                irp__rflgy, metadata=metadata)
            xgwgn__utj.lower()
            if not flags.no_cpython_wrapper:
                xgwgn__utj.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(kuwj__gci, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        xgwgn__utj.create_cfunc_wrapper()
            env = xgwgn__utj.env
            syck__wqen = xgwgn__utj.call_helper
            del xgwgn__utj
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, syck__wqen, cfunc=None, env=env)
        else:
            rnom__uidn = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(rnom__uidn, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, syck__wqen, cfunc=rnom__uidn,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        jjy__wciws = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = jjy__wciws - kfsk__nryo
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
        yqq__cxc = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, yqq__cxc), likely
            =False):
            c.builder.store(cgutils.true_bit, errorptr)
            oxta__naqq.do_break()
        bzp__dnk = c.builder.icmp_signed('!=', yqq__cxc, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(bzp__dnk, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, yqq__cxc)
                c.pyapi.decref(yqq__cxc)
                oxta__naqq.do_break()
        c.pyapi.decref(yqq__cxc)
    jwovl__tiou, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(jwovl__tiou, likely=True) as (mnba__jpovh,
        axda__yhxuw):
        with mnba__jpovh:
            list.size = size
            swj__bguhv = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                swj__bguhv), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        swj__bguhv))
                    with cgutils.for_range(c.builder, size) as oxta__naqq:
                        itemobj = c.pyapi.list_getitem(obj, oxta__naqq.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        lct__coitw = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(lct__coitw.is_error, likely=
                            False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            oxta__naqq.do_break()
                        list.setitem(oxta__naqq.index, lct__coitw.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with axda__yhxuw:
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
    ixnj__jugk, hig__misa, jxdkh__gtbkj, ruqwm__exhgm, ojt__vwwm = (
        compile_time_get_string_data(literal_string))
    qad__lxg = builder.module
    gv = context.insert_const_bytes(qad__lxg, ixnj__jugk)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        hig__misa), context.get_constant(types.int32, jxdkh__gtbkj),
        context.get_constant(types.uint32, ruqwm__exhgm), context.
        get_constant(_Py_hash_t, -1), context.get_constant_null(types.
        MemInfoPointer(types.voidptr)), context.get_constant_null(types.
        pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    hlcjx__bdpi = None
    if isinstance(shape, types.Integer):
        hlcjx__bdpi = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(ynfx__thgpp, (types.Integer, types.IntEnumMember)
            ) for ynfx__thgpp in shape):
            hlcjx__bdpi = len(shape)
    return hlcjx__bdpi


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
            hlcjx__bdpi = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if hlcjx__bdpi == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    hlcjx__bdpi))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            iiqzn__ciayi = self._get_names(x)
            if len(iiqzn__ciayi) != 0:
                return iiqzn__ciayi[0]
            return iiqzn__ciayi
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    iiqzn__ciayi = self._get_names(obj)
    if len(iiqzn__ciayi) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(iiqzn__ciayi[0])


def get_equiv_set(self, obj):
    iiqzn__ciayi = self._get_names(obj)
    if len(iiqzn__ciayi) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(iiqzn__ciayi[0])


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
    ktkxe__dkvli = []
    for chs__wpms in func_ir.arg_names:
        if chs__wpms in typemap and isinstance(typemap[chs__wpms], types.
            containers.UniTuple) and typemap[chs__wpms].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(chs__wpms))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for ttpjw__soeet in func_ir.blocks.values():
        for stmt in ttpjw__soeet.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    hbszo__dqdb = getattr(val, 'code', None)
                    if hbszo__dqdb is not None:
                        if getattr(val, 'closure', None) is not None:
                            vdt__vfcid = '<creating a function from a closure>'
                            ljuck__iejrz = ''
                        else:
                            vdt__vfcid = hbszo__dqdb.co_name
                            ljuck__iejrz = '(%s) ' % vdt__vfcid
                    else:
                        vdt__vfcid = '<could not ascertain use case>'
                        ljuck__iejrz = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (vdt__vfcid, ljuck__iejrz))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                vvxt__zjxt = False
                if isinstance(val, pytypes.FunctionType):
                    vvxt__zjxt = val in {numba.gdb, numba.gdb_init}
                if not vvxt__zjxt:
                    vvxt__zjxt = getattr(val, '_name', '') == 'gdb_internal'
                if vvxt__zjxt:
                    ktkxe__dkvli.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    wsdhh__lyiod = func_ir.get_definition(var)
                    jcej__mcf = guard(find_callname, func_ir, wsdhh__lyiod)
                    if jcej__mcf and jcej__mcf[1] == 'numpy':
                        ty = getattr(numpy, jcej__mcf[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    rpwu__renc = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(rpwu__renc), loc=stmt.loc)
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
    if len(ktkxe__dkvli) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        cpu__ihohx = '\n'.join([x.strformat() for x in ktkxe__dkvli])
        raise errors.UnsupportedError(msg % cpu__ihohx)


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
    eefhl__zjfn, tij__ygkm = next(iter(val.items()))
    fied__lgjee = typeof_impl(eefhl__zjfn, c)
    vfthd__vhmop = typeof_impl(tij__ygkm, c)
    if fied__lgjee is None or vfthd__vhmop is None:
        raise ValueError(
            f'Cannot type dict element type {type(eefhl__zjfn)}, {type(tij__ygkm)}'
            )
    return types.DictType(fied__lgjee, vfthd__vhmop)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    ypd__rbh = cgutils.alloca_once_value(c.builder, val)
    xkecn__xyud = c.pyapi.object_hasattr_string(val, '_opaque')
    idb__sbgh = c.builder.icmp_unsigned('==', xkecn__xyud, lir.Constant(
        xkecn__xyud.type, 0))
    jwy__uqjpz = typ.key_type
    qgeq__wxjdm = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(jwy__uqjpz, qgeq__wxjdm)

    def copy_dict(out_dict, in_dict):
        for eefhl__zjfn, tij__ygkm in in_dict.items():
            out_dict[eefhl__zjfn] = tij__ygkm
    with c.builder.if_then(idb__sbgh):
        ltsfb__tbi = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        tel__fhm = c.pyapi.call_function_objargs(ltsfb__tbi, [])
        ypo__bxy = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(ypo__bxy, [tel__fhm, val])
        c.builder.store(tel__fhm, ypd__rbh)
    val = c.builder.load(ypd__rbh)
    zbst__uhw = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    pqzxy__usr = c.pyapi.object_type(val)
    havgj__xytlk = c.builder.icmp_unsigned('==', pqzxy__usr, zbst__uhw)
    with c.builder.if_else(havgj__xytlk) as (nsy__yfb, tsjfd__egyf):
        with nsy__yfb:
            tabhn__ycqga = c.pyapi.object_getattr_string(val, '_opaque')
            oyafb__xfjcf = types.MemInfoPointer(types.voidptr)
            lct__coitw = c.unbox(oyafb__xfjcf, tabhn__ycqga)
            mi = lct__coitw.value
            hzgng__zcmqa = oyafb__xfjcf, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *hzgng__zcmqa)
            ozv__bobzu = context.get_constant_null(hzgng__zcmqa[1])
            args = mi, ozv__bobzu
            czs__naqte, nvwrp__ecbkj = c.pyapi.call_jit_code(convert, sig, args
                )
            c.context.nrt.decref(c.builder, typ, nvwrp__ecbkj)
            c.pyapi.decref(tabhn__ycqga)
            wasfi__web = c.builder.basic_block
        with tsjfd__egyf:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", pqzxy__usr, zbst__uhw)
            jgtev__zdza = c.builder.basic_block
    bsbuj__oqfp = c.builder.phi(nvwrp__ecbkj.type)
    dyq__ydrp = c.builder.phi(czs__naqte.type)
    bsbuj__oqfp.add_incoming(nvwrp__ecbkj, wasfi__web)
    bsbuj__oqfp.add_incoming(nvwrp__ecbkj.type(None), jgtev__zdza)
    dyq__ydrp.add_incoming(czs__naqte, wasfi__web)
    dyq__ydrp.add_incoming(cgutils.true_bit, jgtev__zdza)
    c.pyapi.decref(zbst__uhw)
    c.pyapi.decref(pqzxy__usr)
    with c.builder.if_then(idb__sbgh):
        c.pyapi.decref(val)
    return NativeValue(bsbuj__oqfp, is_error=dyq__ydrp)


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
    ato__slx = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=ato__slx, name=updatevar)
    gpja__rml = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=gpja__rml, name=res)


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
        for eefhl__zjfn, tij__ygkm in other.items():
            d[eefhl__zjfn] = tij__ygkm
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
    ljuck__iejrz = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(ljuck__iejrz, res)


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
    fzphi__jmqya = PassManager(name)
    if state.func_ir is None:
        fzphi__jmqya.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            fzphi__jmqya.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        fzphi__jmqya.add_pass(FixupArgs, 'fix up args')
    fzphi__jmqya.add_pass(IRProcessing, 'processing IR')
    fzphi__jmqya.add_pass(WithLifting, 'Handle with contexts')
    fzphi__jmqya.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        fzphi__jmqya.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        fzphi__jmqya.add_pass(DeadBranchPrune, 'dead branch pruning')
        fzphi__jmqya.add_pass(GenericRewrites, 'nopython rewrites')
    fzphi__jmqya.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    fzphi__jmqya.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        fzphi__jmqya.add_pass(DeadBranchPrune, 'dead branch pruning')
    fzphi__jmqya.add_pass(FindLiterallyCalls, 'find literally calls')
    fzphi__jmqya.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        fzphi__jmqya.add_pass(ReconstructSSA, 'ssa')
    fzphi__jmqya.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    fzphi__jmqya.finalize()
    return fzphi__jmqya


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
    a, kts__jyv = args
    if isinstance(a, types.List) and isinstance(kts__jyv, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(kts__jyv, types.List):
        return signature(kts__jyv, types.intp, kts__jyv)


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
        tspxw__qpmw, sck__hocv = 0, 1
    else:
        tspxw__qpmw, sck__hocv = 1, 0
    auwwk__dry = ListInstance(context, builder, sig.args[tspxw__qpmw], args
        [tspxw__qpmw])
    dnv__pys = auwwk__dry.size
    dadw__dvvui = args[sck__hocv]
    swj__bguhv = lir.Constant(dadw__dvvui.type, 0)
    dadw__dvvui = builder.select(cgutils.is_neg_int(builder, dadw__dvvui),
        swj__bguhv, dadw__dvvui)
    mtc__zhg = builder.mul(dadw__dvvui, dnv__pys)
    pxok__wrr = ListInstance.allocate(context, builder, sig.return_type,
        mtc__zhg)
    pxok__wrr.size = mtc__zhg
    with cgutils.for_range_slice(builder, swj__bguhv, mtc__zhg, dnv__pys,
        inc=True) as (mqyrz__inl, _):
        with cgutils.for_range(builder, dnv__pys) as oxta__naqq:
            value = auwwk__dry.getitem(oxta__naqq.index)
            pxok__wrr.setitem(builder.add(oxta__naqq.index, mqyrz__inl),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, pxok__wrr.value)


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
    dam__scfr = first.unify(self, second)
    if dam__scfr is not None:
        return dam__scfr
    dam__scfr = second.unify(self, first)
    if dam__scfr is not None:
        return dam__scfr
    ofn__qrt = self.can_convert(fromty=first, toty=second)
    if ofn__qrt is not None and ofn__qrt <= Conversion.safe:
        return second
    ofn__qrt = self.can_convert(fromty=second, toty=first)
    if ofn__qrt is not None and ofn__qrt <= Conversion.safe:
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
    mtc__zhg = payload.used
    listobj = c.pyapi.list_new(mtc__zhg)
    jwovl__tiou = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(jwovl__tiou, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(mtc__zhg.
            type, 0))
        with payload._iterate() as oxta__naqq:
            i = c.builder.load(index)
            item = oxta__naqq.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return jwovl__tiou, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    yxbu__xrpzf = h.type
    emkfo__mggj = self.mask
    dtype = self._ty.dtype
    ppceh__osdw = context.typing_context
    fnty = ppceh__osdw.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(ppceh__osdw, (dtype, dtype), {})
    xwi__ryul = context.get_function(fnty, sig)
    okok__racc = ir.Constant(yxbu__xrpzf, 1)
    huug__lpa = ir.Constant(yxbu__xrpzf, 5)
    eqhfa__mwev = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, emkfo__mggj))
    if for_insert:
        dsi__zzagp = emkfo__mggj.type(-1)
        ecjn__golxh = cgutils.alloca_once_value(builder, dsi__zzagp)
    ksujg__gfx = builder.append_basic_block('lookup.body')
    psovr__fdxan = builder.append_basic_block('lookup.found')
    zwwbr__uruu = builder.append_basic_block('lookup.not_found')
    hfjxm__upxi = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        vdei__wcsnl = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, vdei__wcsnl)):
            gpwab__clch = xwi__ryul(builder, (item, entry.key))
            with builder.if_then(gpwab__clch):
                builder.branch(psovr__fdxan)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, vdei__wcsnl)):
            builder.branch(zwwbr__uruu)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, vdei__wcsnl)):
                odlz__gbs = builder.load(ecjn__golxh)
                odlz__gbs = builder.select(builder.icmp_unsigned('==',
                    odlz__gbs, dsi__zzagp), i, odlz__gbs)
                builder.store(odlz__gbs, ecjn__golxh)
    with cgutils.for_range(builder, ir.Constant(yxbu__xrpzf, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, okok__racc)
        i = builder.and_(i, emkfo__mggj)
        builder.store(i, index)
    builder.branch(ksujg__gfx)
    with builder.goto_block(ksujg__gfx):
        i = builder.load(index)
        check_entry(i)
        kgkus__edxqc = builder.load(eqhfa__mwev)
        kgkus__edxqc = builder.lshr(kgkus__edxqc, huug__lpa)
        i = builder.add(okok__racc, builder.mul(i, huug__lpa))
        i = builder.and_(emkfo__mggj, builder.add(i, kgkus__edxqc))
        builder.store(i, index)
        builder.store(kgkus__edxqc, eqhfa__mwev)
        builder.branch(ksujg__gfx)
    with builder.goto_block(zwwbr__uruu):
        if for_insert:
            i = builder.load(index)
            odlz__gbs = builder.load(ecjn__golxh)
            i = builder.select(builder.icmp_unsigned('==', odlz__gbs,
                dsi__zzagp), i, odlz__gbs)
            builder.store(i, index)
        builder.branch(hfjxm__upxi)
    with builder.goto_block(psovr__fdxan):
        builder.branch(hfjxm__upxi)
    builder.position_at_end(hfjxm__upxi)
    vvxt__zjxt = builder.phi(ir.IntType(1), 'found')
    vvxt__zjxt.add_incoming(cgutils.true_bit, psovr__fdxan)
    vvxt__zjxt.add_incoming(cgutils.false_bit, zwwbr__uruu)
    return vvxt__zjxt, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    opsp__ymffx = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    qnd__lxel = payload.used
    okok__racc = ir.Constant(qnd__lxel.type, 1)
    qnd__lxel = payload.used = builder.add(qnd__lxel, okok__racc)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, opsp__ymffx), likely=True):
        payload.fill = builder.add(payload.fill, okok__racc)
    if do_resize:
        self.upsize(qnd__lxel)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    vvxt__zjxt, i = payload._lookup(item, h, for_insert=True)
    fea__vrc = builder.not_(vvxt__zjxt)
    with builder.if_then(fea__vrc):
        entry = payload.get_entry(i)
        opsp__ymffx = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        qnd__lxel = payload.used
        okok__racc = ir.Constant(qnd__lxel.type, 1)
        qnd__lxel = payload.used = builder.add(qnd__lxel, okok__racc)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, opsp__ymffx), likely=True):
            payload.fill = builder.add(payload.fill, okok__racc)
        if do_resize:
            self.upsize(qnd__lxel)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    qnd__lxel = payload.used
    okok__racc = ir.Constant(qnd__lxel.type, 1)
    qnd__lxel = payload.used = self._builder.sub(qnd__lxel, okok__racc)
    if do_resize:
        self.downsize(qnd__lxel)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    vjfa__nhd = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, vjfa__nhd)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    brbg__cdgme = payload
    jwovl__tiou = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(jwovl__tiou), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with brbg__cdgme._iterate() as oxta__naqq:
        entry = oxta__naqq.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(brbg__cdgme.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as oxta__naqq:
        entry = oxta__naqq.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    jwovl__tiou = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(jwovl__tiou), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    jwovl__tiou = cgutils.alloca_once_value(builder, cgutils.true_bit)
    yxbu__xrpzf = context.get_value_type(types.intp)
    swj__bguhv = ir.Constant(yxbu__xrpzf, 0)
    okok__racc = ir.Constant(yxbu__xrpzf, 1)
    zjmh__ktc = context.get_data_type(types.SetPayload(self._ty))
    eqx__gxbmj = context.get_abi_sizeof(zjmh__ktc)
    fogd__vkexn = self._entrysize
    eqx__gxbmj -= fogd__vkexn
    ptwxl__sbeec, cedx__qwyo = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(yxbu__xrpzf, fogd__vkexn), ir.Constant(
        yxbu__xrpzf, eqx__gxbmj))
    with builder.if_then(cedx__qwyo, likely=False):
        builder.store(cgutils.false_bit, jwovl__tiou)
    with builder.if_then(builder.load(jwovl__tiou), likely=True):
        if realloc:
            gnola__bog = self._set.meminfo
            umgek__ith = context.nrt.meminfo_varsize_alloc(builder,
                gnola__bog, size=ptwxl__sbeec)
            xqm__fztz = cgutils.is_null(builder, umgek__ith)
        else:
            kdpe__clkdl = _imp_dtor(context, builder.module, self._ty)
            gnola__bog = context.nrt.meminfo_new_varsize_dtor(builder,
                ptwxl__sbeec, builder.bitcast(kdpe__clkdl, cgutils.voidptr_t))
            xqm__fztz = cgutils.is_null(builder, gnola__bog)
        with builder.if_else(xqm__fztz, likely=False) as (fhiqj__fujo,
            mnba__jpovh):
            with fhiqj__fujo:
                builder.store(cgutils.false_bit, jwovl__tiou)
            with mnba__jpovh:
                if not realloc:
                    self._set.meminfo = gnola__bog
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, ptwxl__sbeec, 255)
                payload.used = swj__bguhv
                payload.fill = swj__bguhv
                payload.finger = swj__bguhv
                bwzb__ktmjp = builder.sub(nentries, okok__racc)
                payload.mask = bwzb__ktmjp
    return builder.load(jwovl__tiou)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    jwovl__tiou = cgutils.alloca_once_value(builder, cgutils.true_bit)
    yxbu__xrpzf = context.get_value_type(types.intp)
    swj__bguhv = ir.Constant(yxbu__xrpzf, 0)
    okok__racc = ir.Constant(yxbu__xrpzf, 1)
    zjmh__ktc = context.get_data_type(types.SetPayload(self._ty))
    eqx__gxbmj = context.get_abi_sizeof(zjmh__ktc)
    fogd__vkexn = self._entrysize
    eqx__gxbmj -= fogd__vkexn
    emkfo__mggj = src_payload.mask
    nentries = builder.add(okok__racc, emkfo__mggj)
    ptwxl__sbeec = builder.add(ir.Constant(yxbu__xrpzf, eqx__gxbmj),
        builder.mul(ir.Constant(yxbu__xrpzf, fogd__vkexn), nentries))
    with builder.if_then(builder.load(jwovl__tiou), likely=True):
        kdpe__clkdl = _imp_dtor(context, builder.module, self._ty)
        gnola__bog = context.nrt.meminfo_new_varsize_dtor(builder,
            ptwxl__sbeec, builder.bitcast(kdpe__clkdl, cgutils.voidptr_t))
        xqm__fztz = cgutils.is_null(builder, gnola__bog)
        with builder.if_else(xqm__fztz, likely=False) as (fhiqj__fujo,
            mnba__jpovh):
            with fhiqj__fujo:
                builder.store(cgutils.false_bit, jwovl__tiou)
            with mnba__jpovh:
                self._set.meminfo = gnola__bog
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = swj__bguhv
                payload.mask = emkfo__mggj
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, fogd__vkexn)
                with src_payload._iterate() as oxta__naqq:
                    context.nrt.incref(builder, self._ty.dtype, oxta__naqq.
                        entry.key)
    return builder.load(jwovl__tiou)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    vdqf__nww = context.get_value_type(types.voidptr)
    ejft__fzed = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [vdqf__nww, ejft__fzed, vdqf__nww])
    haia__ykzr = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=haia__ykzr)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        axhj__hdzr = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer()
            )
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, axhj__hdzr)
        with payload._iterate() as oxta__naqq:
            entry = oxta__naqq.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    opegf__yzbq, = sig.args
    gsbq__itofi, = args
    exy__lirah = numba.core.imputils.call_len(context, builder, opegf__yzbq,
        gsbq__itofi)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, exy__lirah)
    with numba.core.imputils.for_iter(context, builder, opegf__yzbq,
        gsbq__itofi) as oxta__naqq:
        inst.add(oxta__naqq.value)
        context.nrt.decref(builder, set_type.dtype, oxta__naqq.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    opegf__yzbq = sig.args[1]
    gsbq__itofi = args[1]
    exy__lirah = numba.core.imputils.call_len(context, builder, opegf__yzbq,
        gsbq__itofi)
    if exy__lirah is not None:
        hko__dswuf = builder.add(inst.payload.used, exy__lirah)
        inst.upsize(hko__dswuf)
    with numba.core.imputils.for_iter(context, builder, opegf__yzbq,
        gsbq__itofi) as oxta__naqq:
        wsrlz__pjg = context.cast(builder, oxta__naqq.value, opegf__yzbq.
            dtype, inst.dtype)
        inst.add(wsrlz__pjg)
        context.nrt.decref(builder, opegf__yzbq.dtype, oxta__naqq.value)
    if exy__lirah is not None:
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
    pajcq__jpm = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, pajcq__jpm, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    rnom__uidn = target_context.get_executable(library, fndesc, env)
    sxe__zfsd = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=rnom__uidn, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return sxe__zfsd


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
        otxh__bbpwe = MPI.COMM_WORLD
        if otxh__bbpwe.Get_rank() == 0:
            sdvv__btzr = self.get_cache_path()
            os.makedirs(sdvv__btzr, exist_ok=True)
            tempfile.TemporaryFile(dir=sdvv__btzr).close()
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
    zgx__nsfr = cgutils.create_struct_proxy(charseq.bytes_type)
    knhc__dlerm = zgx__nsfr(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(knhc__dlerm.nitems.type, nbytes)
    knhc__dlerm.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    knhc__dlerm.nitems = nbytes
    knhc__dlerm.itemsize = ir.Constant(knhc__dlerm.itemsize.type, 1)
    knhc__dlerm.data = context.nrt.meminfo_data(builder, knhc__dlerm.meminfo)
    knhc__dlerm.parent = cgutils.get_null_value(knhc__dlerm.parent.type)
    knhc__dlerm.shape = cgutils.pack_array(builder, [knhc__dlerm.nitems],
        context.get_value_type(types.intp))
    knhc__dlerm.strides = cgutils.pack_array(builder, [ir.Constant(
        knhc__dlerm.strides.type.element, 1)], context.get_value_type(types
        .intp))
    return knhc__dlerm


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
