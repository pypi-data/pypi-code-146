"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils, types
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, IRLegalization, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
import bodo.io
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
import bodo.utils
import bodo.utils.table_utils
import bodo.utils.typing
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.table_column_del_pass import TableColumnDelPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        odhx__lcneg = 'bodo' if distributed else 'bodo_seq'
        odhx__lcneg = (odhx__lcneg + '_inline' if inline_calls_pass else
            odhx__lcneg)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state,
            odhx__lcneg)
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        add_pass_before(pm, BodoTableColumnDelPass, IRLegalization)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for nydqk__xfx, (vngun__rjfkf, gmiid__jwfaz) in enumerate(pm.passes):
        if vngun__rjfkf == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(nydqk__xfx, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for nydqk__xfx, (vngun__rjfkf, gmiid__jwfaz) in enumerate(pm.passes):
        if vngun__rjfkf == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[nydqk__xfx] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for nydqk__xfx, (vngun__rjfkf, gmiid__jwfaz) in enumerate(pm.passes):
        if vngun__rjfkf == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(nydqk__xfx)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    wvs__vtfkt = guard(get_definition, func_ir, rhs.func)
    if isinstance(wvs__vtfkt, (ir.Global, ir.FreeVar, ir.Const)):
        qaltz__ntj = wvs__vtfkt.value
    else:
        fleje__ammhi = guard(find_callname, func_ir, rhs)
        if not (fleje__ammhi and isinstance(fleje__ammhi[0], str) and
            isinstance(fleje__ammhi[1], str)):
            return
        func_name, func_mod = fleje__ammhi
        try:
            import importlib
            mps__bsm = importlib.import_module(func_mod)
            qaltz__ntj = getattr(mps__bsm, func_name)
        except:
            return
    if isinstance(qaltz__ntj, CPUDispatcher) and issubclass(qaltz__ntj.
        _compiler.pipeline_class, BodoCompiler
        ) and qaltz__ntj._compiler.pipeline_class != BodoCompilerUDF:
        qaltz__ntj._compiler.pipeline_class = BodoCompilerUDF
        qaltz__ntj.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for pxcmx__quzzr in block.body:
                if is_call_assign(pxcmx__quzzr):
                    _convert_bodo_dispatcher_to_udf(pxcmx__quzzr.value,
                        state.func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        tpkc__nmd = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags, isinstance(state.
            pipeline, BodoCompilerSeq))
        tpkc__nmd.run()
        return True


def _update_definitions(func_ir, node_list):
    jyusk__vml = ir.Loc('', 0)
    mwvtl__eskog = ir.Block(ir.Scope(None, jyusk__vml), jyusk__vml)
    mwvtl__eskog.body = node_list
    build_definitions({(0): mwvtl__eskog}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine',
    'bfill', 'ffill', 'pad', 'backfill', 'mask', 'where'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query',
    'rolling', 'mask', 'where'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        wqs__aiep = 'overload_series_' + rhs.attr
        jvg__wwuup = getattr(bodo.hiframes.series_impl, wqs__aiep)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        wqs__aiep = 'overload_dataframe_' + rhs.attr
        jvg__wwuup = getattr(bodo.hiframes.dataframe_impl, wqs__aiep)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    yrsje__lne = jvg__wwuup(rhs_type)
    upv__ery = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    ywhqw__nudh = compile_func_single_block(yrsje__lne, (rhs.value,), stmt.
        target, upv__ery)
    _update_definitions(func_ir, ywhqw__nudh)
    new_body += ywhqw__nudh
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        wnimr__qmf = tuple(typemap[bvw__dcpgy.name] for bvw__dcpgy in rhs.args)
        kkr__uvozd = {odhx__lcneg: typemap[bvw__dcpgy.name] for odhx__lcneg,
            bvw__dcpgy in dict(rhs.kws).items()}
        yrsje__lne = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*wnimr__qmf, **kkr__uvozd)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        wnimr__qmf = tuple(typemap[bvw__dcpgy.name] for bvw__dcpgy in rhs.args)
        kkr__uvozd = {odhx__lcneg: typemap[bvw__dcpgy.name] for odhx__lcneg,
            bvw__dcpgy in dict(rhs.kws).items()}
        yrsje__lne = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*wnimr__qmf, **kkr__uvozd)
    else:
        return False
    tlsh__uinu = replace_func(pass_info, yrsje__lne, rhs.args, pysig=numba.
        core.utils.pysignature(yrsje__lne), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    ixor__clph, gmiid__jwfaz = inline_closure_call(func_ir, tlsh__uinu.
        glbls, block, len(new_body), tlsh__uinu.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=tlsh__uinu.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for asfzq__iscyt in ixor__clph.values():
        asfzq__iscyt.loc = rhs.loc
        update_locs(asfzq__iscyt.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    inopa__zqth = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = inopa__zqth(func_ir, typemap)
    yomk__thc = func_ir.blocks
    work_list = list((xlnwo__fzwa, yomk__thc[xlnwo__fzwa]) for xlnwo__fzwa in
        reversed(yomk__thc.keys()))
    while work_list:
        klqbf__tqp, block = work_list.pop()
        new_body = []
        anv__ziv = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                fleje__ammhi = guard(find_callname, func_ir, rhs, typemap)
                if fleje__ammhi is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = fleje__ammhi
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    anv__ziv = True
                    break
            new_body.append(stmt)
        if not anv__ziv:
            yomk__thc[klqbf__tqp].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        wufb__zul = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = wufb__zul.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        xeov__yec = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        fute__rwk = xeov__yec.run()
        ise__ouztn = fute__rwk
        if ise__ouztn:
            ise__ouztn = xeov__yec.run()
        if ise__ouztn:
            xeov__yec.run()
        return fute__rwk


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        dcvpj__cntl = 0
        gkmeu__ewaxk = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            dcvpj__cntl = int(os.environ[gkmeu__ewaxk])
        except:
            pass
        if dcvpj__cntl > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(dcvpj__cntl,
                state.metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        from bodo.transforms.table_column_del_pass import remove_dead_table_columns
        from bodo.utils.transform import compile_func_single_block
        from bodo.utils.typing import decode_if_dict_array, to_str_arr_if_dict_array
        state.func_ir._definitions = build_definitions(state.func_ir.blocks)
        upv__ery = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, upv__ery)
        for block in state.func_ir.blocks.values():
            new_body = []
            for pxcmx__quzzr in block.body:
                if type(pxcmx__quzzr) in distributed_run_extensions:
                    div__nwr = distributed_run_extensions[type(pxcmx__quzzr)]
                    if isinstance(pxcmx__quzzr, bodo.ir.parquet_ext.
                        ParquetReader) or isinstance(pxcmx__quzzr, bodo.ir.
                        sql_ext.SqlReader) and pxcmx__quzzr.db_type in (
                        'iceberg', 'snowflake'):
                        kowot__vcv = div__nwr(pxcmx__quzzr, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx, is_independent=True,
                            meta_head_only_info=None)
                    else:
                        kowot__vcv = div__nwr(pxcmx__quzzr, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx)
                    new_body += kowot__vcv
                elif is_call_assign(pxcmx__quzzr):
                    rhs = pxcmx__quzzr.value
                    fleje__ammhi = guard(find_callname, state.func_ir, rhs)
                    if fleje__ammhi == ('gatherv', 'bodo') or fleje__ammhi == (
                        'allgatherv', 'bodo'):
                        aih__yskdo = state.typemap[pxcmx__quzzr.target.name]
                        jzs__lgj = state.typemap[rhs.args[0].name]
                        if isinstance(jzs__lgj, types.Array) and isinstance(
                            aih__yskdo, types.Array):
                            wagbc__myw = jzs__lgj.copy(readonly=False)
                            hxeso__qgx = aih__yskdo.copy(readonly=False)
                            if wagbc__myw == hxeso__qgx:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), pxcmx__quzzr.target, upv__ery)
                                continue
                        if aih__yskdo != jzs__lgj and to_str_arr_if_dict_array(
                            aih__yskdo) == to_str_arr_if_dict_array(jzs__lgj):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), pxcmx__quzzr.target,
                                upv__ery, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            pxcmx__quzzr.value = rhs.args[0]
                    new_body.append(pxcmx__quzzr)
                else:
                    new_body.append(pxcmx__quzzr)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        pkfo__gpbug = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return pkfo__gpbug.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    mjcky__iwth = set()
    while work_list:
        klqbf__tqp, block = work_list.pop()
        mjcky__iwth.add(klqbf__tqp)
        for i, psjv__oih in enumerate(block.body):
            if isinstance(psjv__oih, ir.Assign):
                wmxqd__popqb = psjv__oih.value
                if isinstance(wmxqd__popqb, ir.Expr
                    ) and wmxqd__popqb.op == 'call':
                    wvs__vtfkt = guard(get_definition, func_ir,
                        wmxqd__popqb.func)
                    if isinstance(wvs__vtfkt, (ir.Global, ir.FreeVar)
                        ) and isinstance(wvs__vtfkt.value, CPUDispatcher
                        ) and issubclass(wvs__vtfkt.value._compiler.
                        pipeline_class, BodoCompiler):
                        ewffl__khtwm = wvs__vtfkt.value.py_func
                        arg_types = None
                        if typingctx:
                            wjgi__lgosh = dict(wmxqd__popqb.kws)
                            who__gllu = tuple(typemap[bvw__dcpgy.name] for
                                bvw__dcpgy in wmxqd__popqb.args)
                            spt__ugohr = {vyfm__bpjue: typemap[bvw__dcpgy.
                                name] for vyfm__bpjue, bvw__dcpgy in
                                wjgi__lgosh.items()}
                            gmiid__jwfaz, arg_types = (wvs__vtfkt.value.
                                fold_argument_types(who__gllu, spt__ugohr))
                        gmiid__jwfaz, yczj__koqss = inline_closure_call(func_ir
                            , ewffl__khtwm.__globals__, block, i,
                            ewffl__khtwm, typingctx=typingctx, targetctx=
                            targetctx, arg_typs=arg_types, typemap=typemap,
                            calltypes=calltypes, work_list=work_list)
                        _locals.update((yczj__koqss[vyfm__bpjue].name,
                            bvw__dcpgy) for vyfm__bpjue, bvw__dcpgy in
                            wvs__vtfkt.value.locals.items() if vyfm__bpjue in
                            yczj__koqss)
                        break
    return mjcky__iwth


def udf_jit(signature_or_function=None, **options):
    vok__kfvl = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=vok__kfvl,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for nydqk__xfx, (vngun__rjfkf, gmiid__jwfaz) in enumerate(pm.passes):
        if vngun__rjfkf == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:nydqk__xfx + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    gjx__yhi = None
    wjxgx__yozp = None
    _locals = {}
    koiwk__eth = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(koiwk__eth, arg_types,
        kw_types)
    wclj__nrtz = numba.core.compiler.Flags()
    yhjo__tjfho = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    ixjs__mft = {'nopython': True, 'boundscheck': False, 'parallel':
        yhjo__tjfho}
    numba.core.registry.cpu_target.options.parse_as_flags(wclj__nrtz, ixjs__mft
        )
    rkr__mpu = TyperCompiler(typingctx, targetctx, gjx__yhi, args,
        wjxgx__yozp, wclj__nrtz, _locals)
    return rkr__mpu.compile_extra(func)
