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
        uilc__ogg = 'bodo' if distributed else 'bodo_seq'
        uilc__ogg = uilc__ogg + '_inline' if inline_calls_pass else uilc__ogg
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, uilc__ogg)
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
    for ziapr__wqzp, (pov__tsz, ocls__vnrn) in enumerate(pm.passes):
        if pov__tsz == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(ziapr__wqzp, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for ziapr__wqzp, (pov__tsz, ocls__vnrn) in enumerate(pm.passes):
        if pov__tsz == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[ziapr__wqzp] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for ziapr__wqzp, (pov__tsz, ocls__vnrn) in enumerate(pm.passes):
        if pov__tsz == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(ziapr__wqzp)
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
    vhjfl__xsie = guard(get_definition, func_ir, rhs.func)
    if isinstance(vhjfl__xsie, (ir.Global, ir.FreeVar, ir.Const)):
        apubs__ihpd = vhjfl__xsie.value
    else:
        pmvo__kkct = guard(find_callname, func_ir, rhs)
        if not (pmvo__kkct and isinstance(pmvo__kkct[0], str) and
            isinstance(pmvo__kkct[1], str)):
            return
        func_name, func_mod = pmvo__kkct
        try:
            import importlib
            ixdas__mvmy = importlib.import_module(func_mod)
            apubs__ihpd = getattr(ixdas__mvmy, func_name)
        except:
            return
    if isinstance(apubs__ihpd, CPUDispatcher) and issubclass(apubs__ihpd.
        _compiler.pipeline_class, BodoCompiler
        ) and apubs__ihpd._compiler.pipeline_class != BodoCompilerUDF:
        apubs__ihpd._compiler.pipeline_class = BodoCompilerUDF
        apubs__ihpd.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for kfncu__gwogl in block.body:
                if is_call_assign(kfncu__gwogl):
                    _convert_bodo_dispatcher_to_udf(kfncu__gwogl.value,
                        state.func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        doq__nvwwm = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags, isinstance(state.
            pipeline, BodoCompilerSeq))
        doq__nvwwm.run()
        return True


def _update_definitions(func_ir, node_list):
    shr__msj = ir.Loc('', 0)
    sqwyf__dzr = ir.Block(ir.Scope(None, shr__msj), shr__msj)
    sqwyf__dzr.body = node_list
    build_definitions({(0): sqwyf__dzr}, func_ir._definitions)


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
        upzrj__jhfkf = 'overload_series_' + rhs.attr
        xiy__dlqqu = getattr(bodo.hiframes.series_impl, upzrj__jhfkf)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        upzrj__jhfkf = 'overload_dataframe_' + rhs.attr
        xiy__dlqqu = getattr(bodo.hiframes.dataframe_impl, upzrj__jhfkf)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    aro__mqvht = xiy__dlqqu(rhs_type)
    btnm__hgcno = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc
        )
    gvh__kbi = compile_func_single_block(aro__mqvht, (rhs.value,), stmt.
        target, btnm__hgcno)
    _update_definitions(func_ir, gvh__kbi)
    new_body += gvh__kbi
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
        bkz__qjjr = tuple(typemap[yqi__zucnr.name] for yqi__zucnr in rhs.args)
        seus__jgqp = {uilc__ogg: typemap[yqi__zucnr.name] for uilc__ogg,
            yqi__zucnr in dict(rhs.kws).items()}
        aro__mqvht = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*bkz__qjjr, **seus__jgqp)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        bkz__qjjr = tuple(typemap[yqi__zucnr.name] for yqi__zucnr in rhs.args)
        seus__jgqp = {uilc__ogg: typemap[yqi__zucnr.name] for uilc__ogg,
            yqi__zucnr in dict(rhs.kws).items()}
        aro__mqvht = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*bkz__qjjr, **seus__jgqp)
    else:
        return False
    lfckg__wpdtv = replace_func(pass_info, aro__mqvht, rhs.args, pysig=
        numba.core.utils.pysignature(aro__mqvht), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    nzonj__zsbxp, ocls__vnrn = inline_closure_call(func_ir, lfckg__wpdtv.
        glbls, block, len(new_body), lfckg__wpdtv.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=lfckg__wpdtv.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for pcyc__iigwl in nzonj__zsbxp.values():
        pcyc__iigwl.loc = rhs.loc
        update_locs(pcyc__iigwl.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    tyjov__lvhhu = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = tyjov__lvhhu(func_ir, typemap)
    zrei__zxysc = func_ir.blocks
    work_list = list((tpvkp__ebtmi, zrei__zxysc[tpvkp__ebtmi]) for
        tpvkp__ebtmi in reversed(zrei__zxysc.keys()))
    while work_list:
        kso__cez, block = work_list.pop()
        new_body = []
        iwd__zgves = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                pmvo__kkct = guard(find_callname, func_ir, rhs, typemap)
                if pmvo__kkct is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = pmvo__kkct
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    iwd__zgves = True
                    break
            new_body.append(stmt)
        if not iwd__zgves:
            zrei__zxysc[kso__cez].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        ccnl__xrivc = DistributedPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = ccnl__xrivc.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        nvzke__mnia = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        tfr__zsiwx = nvzke__mnia.run()
        nnxac__gtqf = tfr__zsiwx
        if nnxac__gtqf:
            nnxac__gtqf = nvzke__mnia.run()
        if nnxac__gtqf:
            nvzke__mnia.run()
        return tfr__zsiwx


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        jllp__ackxk = 0
        cwn__isn = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            jllp__ackxk = int(os.environ[cwn__isn])
        except:
            pass
        if jllp__ackxk > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(jllp__ackxk,
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
        btnm__hgcno = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, btnm__hgcno)
        for block in state.func_ir.blocks.values():
            new_body = []
            for kfncu__gwogl in block.body:
                if type(kfncu__gwogl) in distributed_run_extensions:
                    rlr__ddsg = distributed_run_extensions[type(kfncu__gwogl)]
                    if isinstance(kfncu__gwogl, bodo.ir.parquet_ext.
                        ParquetReader) or isinstance(kfncu__gwogl, bodo.ir.
                        sql_ext.SqlReader) and kfncu__gwogl.db_type in (
                        'iceberg', 'snowflake'):
                        cfpv__jinqi = rlr__ddsg(kfncu__gwogl, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx, is_independent=True,
                            meta_head_only_info=None)
                    else:
                        cfpv__jinqi = rlr__ddsg(kfncu__gwogl, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx)
                    new_body += cfpv__jinqi
                elif is_call_assign(kfncu__gwogl):
                    rhs = kfncu__gwogl.value
                    pmvo__kkct = guard(find_callname, state.func_ir, rhs)
                    if pmvo__kkct == ('gatherv', 'bodo') or pmvo__kkct == (
                        'allgatherv', 'bodo'):
                        uuun__ipsfo = state.typemap[kfncu__gwogl.target.name]
                        gxu__vxe = state.typemap[rhs.args[0].name]
                        if isinstance(gxu__vxe, types.Array) and isinstance(
                            uuun__ipsfo, types.Array):
                            itaz__izvfb = gxu__vxe.copy(readonly=False)
                            pfdb__qyo = uuun__ipsfo.copy(readonly=False)
                            if itaz__izvfb == pfdb__qyo:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), kfncu__gwogl.target, btnm__hgcno)
                                continue
                        if (uuun__ipsfo != gxu__vxe and 
                            to_str_arr_if_dict_array(uuun__ipsfo) ==
                            to_str_arr_if_dict_array(gxu__vxe)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), kfncu__gwogl.target,
                                btnm__hgcno, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            kfncu__gwogl.value = rhs.args[0]
                    new_body.append(kfncu__gwogl)
                else:
                    new_body.append(kfncu__gwogl)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        fwccw__eyowk = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return fwccw__eyowk.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    rijd__uyqq = set()
    while work_list:
        kso__cez, block = work_list.pop()
        rijd__uyqq.add(kso__cez)
        for i, wfljf__cfw in enumerate(block.body):
            if isinstance(wfljf__cfw, ir.Assign):
                kyghq__acfr = wfljf__cfw.value
                if isinstance(kyghq__acfr, ir.Expr
                    ) and kyghq__acfr.op == 'call':
                    vhjfl__xsie = guard(get_definition, func_ir,
                        kyghq__acfr.func)
                    if isinstance(vhjfl__xsie, (ir.Global, ir.FreeVar)
                        ) and isinstance(vhjfl__xsie.value, CPUDispatcher
                        ) and issubclass(vhjfl__xsie.value._compiler.
                        pipeline_class, BodoCompiler):
                        dttp__tuy = vhjfl__xsie.value.py_func
                        arg_types = None
                        if typingctx:
                            utac__zojow = dict(kyghq__acfr.kws)
                            jbp__ghy = tuple(typemap[yqi__zucnr.name] for
                                yqi__zucnr in kyghq__acfr.args)
                            kpvbb__eabpt = {rzcgn__rifkr: typemap[
                                yqi__zucnr.name] for rzcgn__rifkr,
                                yqi__zucnr in utac__zojow.items()}
                            ocls__vnrn, arg_types = (vhjfl__xsie.value.
                                fold_argument_types(jbp__ghy, kpvbb__eabpt))
                        ocls__vnrn, cjt__vyzka = inline_closure_call(func_ir,
                            dttp__tuy.__globals__, block, i, dttp__tuy,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((cjt__vyzka[rzcgn__rifkr].name,
                            yqi__zucnr) for rzcgn__rifkr, yqi__zucnr in
                            vhjfl__xsie.value.locals.items() if 
                            rzcgn__rifkr in cjt__vyzka)
                        break
    return rijd__uyqq


def udf_jit(signature_or_function=None, **options):
    lqe__jlqaf = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=lqe__jlqaf,
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
    for ziapr__wqzp, (pov__tsz, ocls__vnrn) in enumerate(pm.passes):
        if pov__tsz == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:ziapr__wqzp + 1]
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
    wxkme__aypo = None
    hhya__wcr = None
    _locals = {}
    dgtte__lyp = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(dgtte__lyp, arg_types,
        kw_types)
    ojwy__prq = numba.core.compiler.Flags()
    scv__bgc = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    tgzb__aflve = {'nopython': True, 'boundscheck': False, 'parallel': scv__bgc
        }
    numba.core.registry.cpu_target.options.parse_as_flags(ojwy__prq,
        tgzb__aflve)
    fduu__iuft = TyperCompiler(typingctx, targetctx, wxkme__aypo, args,
        hhya__wcr, ojwy__prq, _locals)
    return fduu__iuft.compile_extra(func)
