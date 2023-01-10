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
        vpl__xppiw = 'bodo' if distributed else 'bodo_seq'
        vpl__xppiw = (vpl__xppiw + '_inline' if inline_calls_pass else
            vpl__xppiw)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, vpl__xppiw
            )
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
    for kze__yta, (ste__kezg, lomp__wdnoh) in enumerate(pm.passes):
        if ste__kezg == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(kze__yta, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for kze__yta, (ste__kezg, lomp__wdnoh) in enumerate(pm.passes):
        if ste__kezg == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[kze__yta] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for kze__yta, (ste__kezg, lomp__wdnoh) in enumerate(pm.passes):
        if ste__kezg == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(kze__yta)
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
    qdvv__tynrx = guard(get_definition, func_ir, rhs.func)
    if isinstance(qdvv__tynrx, (ir.Global, ir.FreeVar, ir.Const)):
        juzr__njkt = qdvv__tynrx.value
    else:
        quxa__bmbo = guard(find_callname, func_ir, rhs)
        if not (quxa__bmbo and isinstance(quxa__bmbo[0], str) and
            isinstance(quxa__bmbo[1], str)):
            return
        func_name, func_mod = quxa__bmbo
        try:
            import importlib
            zeu__czlrn = importlib.import_module(func_mod)
            juzr__njkt = getattr(zeu__czlrn, func_name)
        except:
            return
    if isinstance(juzr__njkt, CPUDispatcher) and issubclass(juzr__njkt.
        _compiler.pipeline_class, BodoCompiler
        ) and juzr__njkt._compiler.pipeline_class != BodoCompilerUDF:
        juzr__njkt._compiler.pipeline_class = BodoCompilerUDF
        juzr__njkt.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for cccjx__mfr in block.body:
                if is_call_assign(cccjx__mfr):
                    _convert_bodo_dispatcher_to_udf(cccjx__mfr.value, state
                        .func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        aumt__jsqhp = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags, isinstance(
            state.pipeline, BodoCompilerSeq))
        aumt__jsqhp.run()
        return True


def _update_definitions(func_ir, node_list):
    bmvu__fmg = ir.Loc('', 0)
    cted__tbhu = ir.Block(ir.Scope(None, bmvu__fmg), bmvu__fmg)
    cted__tbhu.body = node_list
    build_definitions({(0): cted__tbhu}, func_ir._definitions)


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
        tla__cth = 'overload_series_' + rhs.attr
        gky__isqg = getattr(bodo.hiframes.series_impl, tla__cth)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        tla__cth = 'overload_dataframe_' + rhs.attr
        gky__isqg = getattr(bodo.hiframes.dataframe_impl, tla__cth)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    qdeg__ushk = gky__isqg(rhs_type)
    jmcm__tsp = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    liezu__kqyj = compile_func_single_block(qdeg__ushk, (rhs.value,), stmt.
        target, jmcm__tsp)
    _update_definitions(func_ir, liezu__kqyj)
    new_body += liezu__kqyj
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
        qqc__cmol = tuple(typemap[het__qpr.name] for het__qpr in rhs.args)
        vff__uixl = {vpl__xppiw: typemap[het__qpr.name] for vpl__xppiw,
            het__qpr in dict(rhs.kws).items()}
        qdeg__ushk = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*qqc__cmol, **vff__uixl)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        qqc__cmol = tuple(typemap[het__qpr.name] for het__qpr in rhs.args)
        vff__uixl = {vpl__xppiw: typemap[het__qpr.name] for vpl__xppiw,
            het__qpr in dict(rhs.kws).items()}
        qdeg__ushk = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*qqc__cmol, **vff__uixl)
    else:
        return False
    gde__qbw = replace_func(pass_info, qdeg__ushk, rhs.args, pysig=numba.
        core.utils.pysignature(qdeg__ushk), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    ayjnp__dfxr, lomp__wdnoh = inline_closure_call(func_ir, gde__qbw.glbls,
        block, len(new_body), gde__qbw.func, typingctx=typingctx, targetctx
        =targetctx, arg_typs=gde__qbw.arg_types, typemap=typemap, calltypes
        =calltypes, work_list=work_list)
    for isszy__rdby in ayjnp__dfxr.values():
        isszy__rdby.loc = rhs.loc
        update_locs(isszy__rdby.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    rmnzr__bis = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = rmnzr__bis(func_ir, typemap)
    gqh__ifu = func_ir.blocks
    work_list = list((znl__uoxnz, gqh__ifu[znl__uoxnz]) for znl__uoxnz in
        reversed(gqh__ifu.keys()))
    while work_list:
        qlx__cow, block = work_list.pop()
        new_body = []
        qpcd__isqu = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                quxa__bmbo = guard(find_callname, func_ir, rhs, typemap)
                if quxa__bmbo is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = quxa__bmbo
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    qpcd__isqu = True
                    break
            new_body.append(stmt)
        if not qpcd__isqu:
            gqh__ifu[qlx__cow].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        hsew__rnbhg = DistributedPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = hsew__rnbhg.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        boti__jly = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        hug__ews = boti__jly.run()
        appy__ucuzi = hug__ews
        if appy__ucuzi:
            appy__ucuzi = boti__jly.run()
        if appy__ucuzi:
            boti__jly.run()
        return hug__ews


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        wyfco__wkf = 0
        biy__gmyke = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            wyfco__wkf = int(os.environ[biy__gmyke])
        except:
            pass
        if wyfco__wkf > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(wyfco__wkf,
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
        jmcm__tsp = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, jmcm__tsp)
        for block in state.func_ir.blocks.values():
            new_body = []
            for cccjx__mfr in block.body:
                if type(cccjx__mfr) in distributed_run_extensions:
                    bljek__rdrz = distributed_run_extensions[type(cccjx__mfr)]
                    if isinstance(cccjx__mfr, bodo.ir.parquet_ext.ParquetReader
                        ) or isinstance(cccjx__mfr, bodo.ir.sql_ext.SqlReader
                        ) and cccjx__mfr.db_type in ('iceberg', 'snowflake'):
                        bfoqf__cnsbe = bljek__rdrz(cccjx__mfr, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx, is_independent=True,
                            meta_head_only_info=None)
                    else:
                        bfoqf__cnsbe = bljek__rdrz(cccjx__mfr, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx)
                    new_body += bfoqf__cnsbe
                elif is_call_assign(cccjx__mfr):
                    rhs = cccjx__mfr.value
                    quxa__bmbo = guard(find_callname, state.func_ir, rhs)
                    if quxa__bmbo == ('gatherv', 'bodo') or quxa__bmbo == (
                        'allgatherv', 'bodo'):
                        wmhg__hxz = state.typemap[cccjx__mfr.target.name]
                        iho__qrqgo = state.typemap[rhs.args[0].name]
                        if isinstance(iho__qrqgo, types.Array) and isinstance(
                            wmhg__hxz, types.Array):
                            ect__leyv = iho__qrqgo.copy(readonly=False)
                            uet__ajyq = wmhg__hxz.copy(readonly=False)
                            if ect__leyv == uet__ajyq:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), cccjx__mfr.target, jmcm__tsp)
                                continue
                        if (wmhg__hxz != iho__qrqgo and 
                            to_str_arr_if_dict_array(wmhg__hxz) ==
                            to_str_arr_if_dict_array(iho__qrqgo)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), cccjx__mfr.target,
                                jmcm__tsp, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            cccjx__mfr.value = rhs.args[0]
                    new_body.append(cccjx__mfr)
                else:
                    new_body.append(cccjx__mfr)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        gsah__ght = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return gsah__ght.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    iyd__par = set()
    while work_list:
        qlx__cow, block = work_list.pop()
        iyd__par.add(qlx__cow)
        for i, jgkb__tlc in enumerate(block.body):
            if isinstance(jgkb__tlc, ir.Assign):
                fhrvx__ygd = jgkb__tlc.value
                if isinstance(fhrvx__ygd, ir.Expr) and fhrvx__ygd.op == 'call':
                    qdvv__tynrx = guard(get_definition, func_ir, fhrvx__ygd
                        .func)
                    if isinstance(qdvv__tynrx, (ir.Global, ir.FreeVar)
                        ) and isinstance(qdvv__tynrx.value, CPUDispatcher
                        ) and issubclass(qdvv__tynrx.value._compiler.
                        pipeline_class, BodoCompiler):
                        pgan__lqi = qdvv__tynrx.value.py_func
                        arg_types = None
                        if typingctx:
                            sne__urkba = dict(fhrvx__ygd.kws)
                            bbnjb__oyu = tuple(typemap[het__qpr.name] for
                                het__qpr in fhrvx__ygd.args)
                            ueo__jfj = {ojh__wpvcu: typemap[het__qpr.name] for
                                ojh__wpvcu, het__qpr in sne__urkba.items()}
                            lomp__wdnoh, arg_types = (qdvv__tynrx.value.
                                fold_argument_types(bbnjb__oyu, ueo__jfj))
                        lomp__wdnoh, zbafq__let = inline_closure_call(func_ir,
                            pgan__lqi.__globals__, block, i, pgan__lqi,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((zbafq__let[ojh__wpvcu].name,
                            het__qpr) for ojh__wpvcu, het__qpr in
                            qdvv__tynrx.value.locals.items() if ojh__wpvcu in
                            zbafq__let)
                        break
    return iyd__par


def udf_jit(signature_or_function=None, **options):
    kugop__tfsph = {'comprehension': True, 'setitem': False,
        'inplace_binop': False, 'reduction': True, 'numpy': True, 'stencil':
        False, 'fusion': True}
    return numba.njit(signature_or_function, parallel=kugop__tfsph,
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
    for kze__yta, (ste__kezg, lomp__wdnoh) in enumerate(pm.passes):
        if ste__kezg == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:kze__yta + 1]
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
    ibzq__xwe = None
    jdgx__bur = None
    _locals = {}
    gfho__wjmix = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(gfho__wjmix, arg_types,
        kw_types)
    pnlu__qmfs = numba.core.compiler.Flags()
    gey__dysm = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    osgu__pro = {'nopython': True, 'boundscheck': False, 'parallel': gey__dysm}
    numba.core.registry.cpu_target.options.parse_as_flags(pnlu__qmfs, osgu__pro
        )
    qjseu__yjly = TyperCompiler(typingctx, targetctx, ibzq__xwe, args,
        jdgx__bur, pnlu__qmfs, _locals)
    return qjseu__yjly.compile_extra(func)
