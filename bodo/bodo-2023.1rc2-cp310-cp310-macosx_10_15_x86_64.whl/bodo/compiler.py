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
        vkk__qmqse = 'bodo' if distributed else 'bodo_seq'
        vkk__qmqse = (vkk__qmqse + '_inline' if inline_calls_pass else
            vkk__qmqse)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, vkk__qmqse
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
    for flo__qmlhl, (rwybj__eygpe, gefz__dbt) in enumerate(pm.passes):
        if rwybj__eygpe == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(flo__qmlhl, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for flo__qmlhl, (rwybj__eygpe, gefz__dbt) in enumerate(pm.passes):
        if rwybj__eygpe == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[flo__qmlhl] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for flo__qmlhl, (rwybj__eygpe, gefz__dbt) in enumerate(pm.passes):
        if rwybj__eygpe == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(flo__qmlhl)
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
    rrtp__wam = guard(get_definition, func_ir, rhs.func)
    if isinstance(rrtp__wam, (ir.Global, ir.FreeVar, ir.Const)):
        ubua__rsucg = rrtp__wam.value
    else:
        cbffi__ulon = guard(find_callname, func_ir, rhs)
        if not (cbffi__ulon and isinstance(cbffi__ulon[0], str) and
            isinstance(cbffi__ulon[1], str)):
            return
        func_name, func_mod = cbffi__ulon
        try:
            import importlib
            vmsf__yot = importlib.import_module(func_mod)
            ubua__rsucg = getattr(vmsf__yot, func_name)
        except:
            return
    if isinstance(ubua__rsucg, CPUDispatcher) and issubclass(ubua__rsucg.
        _compiler.pipeline_class, BodoCompiler
        ) and ubua__rsucg._compiler.pipeline_class != BodoCompilerUDF:
        ubua__rsucg._compiler.pipeline_class = BodoCompilerUDF
        ubua__rsucg.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for kqb__nhoeu in block.body:
                if is_call_assign(kqb__nhoeu):
                    _convert_bodo_dispatcher_to_udf(kqb__nhoeu.value, state
                        .func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        znzg__buqhh = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags, isinstance(
            state.pipeline, BodoCompilerSeq))
        znzg__buqhh.run()
        return True


def _update_definitions(func_ir, node_list):
    ynu__ida = ir.Loc('', 0)
    iakg__rgyz = ir.Block(ir.Scope(None, ynu__ida), ynu__ida)
    iakg__rgyz.body = node_list
    build_definitions({(0): iakg__rgyz}, func_ir._definitions)


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
        kmjx__vlvok = 'overload_series_' + rhs.attr
        nqc__uki = getattr(bodo.hiframes.series_impl, kmjx__vlvok)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        kmjx__vlvok = 'overload_dataframe_' + rhs.attr
        nqc__uki = getattr(bodo.hiframes.dataframe_impl, kmjx__vlvok)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    yiq__jagus = nqc__uki(rhs_type)
    exbyz__nyujq = TypingInfo(typingctx, targetctx, typemap, calltypes,
        stmt.loc)
    pampr__csgtb = compile_func_single_block(yiq__jagus, (rhs.value,), stmt
        .target, exbyz__nyujq)
    _update_definitions(func_ir, pampr__csgtb)
    new_body += pampr__csgtb
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
        vckma__ldnw = tuple(typemap[tuvl__tqyqj.name] for tuvl__tqyqj in
            rhs.args)
        fmyl__ctpll = {vkk__qmqse: typemap[tuvl__tqyqj.name] for vkk__qmqse,
            tuvl__tqyqj in dict(rhs.kws).items()}
        yiq__jagus = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*vckma__ldnw, **fmyl__ctpll)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        vckma__ldnw = tuple(typemap[tuvl__tqyqj.name] for tuvl__tqyqj in
            rhs.args)
        fmyl__ctpll = {vkk__qmqse: typemap[tuvl__tqyqj.name] for vkk__qmqse,
            tuvl__tqyqj in dict(rhs.kws).items()}
        yiq__jagus = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*vckma__ldnw, **fmyl__ctpll)
    else:
        return False
    tcuei__gnzp = replace_func(pass_info, yiq__jagus, rhs.args, pysig=numba
        .core.utils.pysignature(yiq__jagus), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    jzb__ssgk, gefz__dbt = inline_closure_call(func_ir, tcuei__gnzp.glbls,
        block, len(new_body), tcuei__gnzp.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=tcuei__gnzp.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for bvaxu__uehiq in jzb__ssgk.values():
        bvaxu__uehiq.loc = rhs.loc
        update_locs(bvaxu__uehiq.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    naxes__ptgi = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = naxes__ptgi(func_ir, typemap)
    tuwxc__rnqo = func_ir.blocks
    work_list = list((mev__mxykb, tuwxc__rnqo[mev__mxykb]) for mev__mxykb in
        reversed(tuwxc__rnqo.keys()))
    while work_list:
        ejasg__uxmg, block = work_list.pop()
        new_body = []
        eye__hkp = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                cbffi__ulon = guard(find_callname, func_ir, rhs, typemap)
                if cbffi__ulon is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = cbffi__ulon
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    eye__hkp = True
                    break
            new_body.append(stmt)
        if not eye__hkp:
            tuwxc__rnqo[ejasg__uxmg].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        baj__qem = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = baj__qem.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        ucmvw__xeuc = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        tde__llgjl = ucmvw__xeuc.run()
        ronwh__flqcp = tde__llgjl
        if ronwh__flqcp:
            ronwh__flqcp = ucmvw__xeuc.run()
        if ronwh__flqcp:
            ucmvw__xeuc.run()
        return tde__llgjl


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        iwykd__ewsm = 0
        zih__uin = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            iwykd__ewsm = int(os.environ[zih__uin])
        except:
            pass
        if iwykd__ewsm > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(iwykd__ewsm,
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
        exbyz__nyujq = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, exbyz__nyujq)
        for block in state.func_ir.blocks.values():
            new_body = []
            for kqb__nhoeu in block.body:
                if type(kqb__nhoeu) in distributed_run_extensions:
                    lve__rbdi = distributed_run_extensions[type(kqb__nhoeu)]
                    if isinstance(kqb__nhoeu, bodo.ir.parquet_ext.ParquetReader
                        ) or isinstance(kqb__nhoeu, bodo.ir.sql_ext.SqlReader
                        ) and kqb__nhoeu.db_type in ('iceberg', 'snowflake'):
                        xip__wuhe = lve__rbdi(kqb__nhoeu, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx, is_independent=True,
                            meta_head_only_info=None)
                    else:
                        xip__wuhe = lve__rbdi(kqb__nhoeu, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx)
                    new_body += xip__wuhe
                elif is_call_assign(kqb__nhoeu):
                    rhs = kqb__nhoeu.value
                    cbffi__ulon = guard(find_callname, state.func_ir, rhs)
                    if cbffi__ulon == ('gatherv', 'bodo') or cbffi__ulon == (
                        'allgatherv', 'bodo'):
                        xatae__idaxo = state.typemap[kqb__nhoeu.target.name]
                        kwqt__ihqz = state.typemap[rhs.args[0].name]
                        if isinstance(kwqt__ihqz, types.Array) and isinstance(
                            xatae__idaxo, types.Array):
                            wnse__ozp = kwqt__ihqz.copy(readonly=False)
                            ctlwk__erlt = xatae__idaxo.copy(readonly=False)
                            if wnse__ozp == ctlwk__erlt:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), kqb__nhoeu.target, exbyz__nyujq)
                                continue
                        if (xatae__idaxo != kwqt__ihqz and 
                            to_str_arr_if_dict_array(xatae__idaxo) ==
                            to_str_arr_if_dict_array(kwqt__ihqz)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), kqb__nhoeu.target,
                                exbyz__nyujq, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            kqb__nhoeu.value = rhs.args[0]
                    new_body.append(kqb__nhoeu)
                else:
                    new_body.append(kqb__nhoeu)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        ebs__hnlxp = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return ebs__hnlxp.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    yxkf__dikh = set()
    while work_list:
        ejasg__uxmg, block = work_list.pop()
        yxkf__dikh.add(ejasg__uxmg)
        for i, dbkh__wxd in enumerate(block.body):
            if isinstance(dbkh__wxd, ir.Assign):
                ivb__vtf = dbkh__wxd.value
                if isinstance(ivb__vtf, ir.Expr) and ivb__vtf.op == 'call':
                    rrtp__wam = guard(get_definition, func_ir, ivb__vtf.func)
                    if isinstance(rrtp__wam, (ir.Global, ir.FreeVar)
                        ) and isinstance(rrtp__wam.value, CPUDispatcher
                        ) and issubclass(rrtp__wam.value._compiler.
                        pipeline_class, BodoCompiler):
                        neyv__fin = rrtp__wam.value.py_func
                        arg_types = None
                        if typingctx:
                            byz__tcz = dict(ivb__vtf.kws)
                            olwud__qmn = tuple(typemap[tuvl__tqyqj.name] for
                                tuvl__tqyqj in ivb__vtf.args)
                            rvkqm__vnf = {aazv__byr: typemap[tuvl__tqyqj.
                                name] for aazv__byr, tuvl__tqyqj in
                                byz__tcz.items()}
                            gefz__dbt, arg_types = (rrtp__wam.value.
                                fold_argument_types(olwud__qmn, rvkqm__vnf))
                        gefz__dbt, uevc__mly = inline_closure_call(func_ir,
                            neyv__fin.__globals__, block, i, neyv__fin,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((uevc__mly[aazv__byr].name,
                            tuvl__tqyqj) for aazv__byr, tuvl__tqyqj in
                            rrtp__wam.value.locals.items() if aazv__byr in
                            uevc__mly)
                        break
    return yxkf__dikh


def udf_jit(signature_or_function=None, **options):
    ngk__amk = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=ngk__amk,
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
    for flo__qmlhl, (rwybj__eygpe, gefz__dbt) in enumerate(pm.passes):
        if rwybj__eygpe == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:flo__qmlhl + 1]
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
    nba__wzt = None
    ffndn__cual = None
    _locals = {}
    blpx__oct = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(blpx__oct, arg_types,
        kw_types)
    rmq__oqh = numba.core.compiler.Flags()
    ncli__luc = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    jvf__gngsm = {'nopython': True, 'boundscheck': False, 'parallel': ncli__luc
        }
    numba.core.registry.cpu_target.options.parse_as_flags(rmq__oqh, jvf__gngsm)
    ygvhs__rpul = TyperCompiler(typingctx, targetctx, nba__wzt, args,
        ffndn__cual, rmq__oqh, _locals)
    return ygvhs__rpul.compile_extra(func)
