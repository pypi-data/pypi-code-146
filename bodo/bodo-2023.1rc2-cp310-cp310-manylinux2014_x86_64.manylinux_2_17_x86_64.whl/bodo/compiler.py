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
        gyfdi__lbc = 'bodo' if distributed else 'bodo_seq'
        gyfdi__lbc = (gyfdi__lbc + '_inline' if inline_calls_pass else
            gyfdi__lbc)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, gyfdi__lbc
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
    for mah__lmnh, (ftu__xkto, qmjf__oma) in enumerate(pm.passes):
        if ftu__xkto == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(mah__lmnh, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for mah__lmnh, (ftu__xkto, qmjf__oma) in enumerate(pm.passes):
        if ftu__xkto == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[mah__lmnh] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for mah__lmnh, (ftu__xkto, qmjf__oma) in enumerate(pm.passes):
        if ftu__xkto == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(mah__lmnh)
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
    kig__eyw = guard(get_definition, func_ir, rhs.func)
    if isinstance(kig__eyw, (ir.Global, ir.FreeVar, ir.Const)):
        rkgt__vytc = kig__eyw.value
    else:
        opy__yxby = guard(find_callname, func_ir, rhs)
        if not (opy__yxby and isinstance(opy__yxby[0], str) and isinstance(
            opy__yxby[1], str)):
            return
        func_name, func_mod = opy__yxby
        try:
            import importlib
            aaw__xjpbb = importlib.import_module(func_mod)
            rkgt__vytc = getattr(aaw__xjpbb, func_name)
        except:
            return
    if isinstance(rkgt__vytc, CPUDispatcher) and issubclass(rkgt__vytc.
        _compiler.pipeline_class, BodoCompiler
        ) and rkgt__vytc._compiler.pipeline_class != BodoCompilerUDF:
        rkgt__vytc._compiler.pipeline_class = BodoCompilerUDF
        rkgt__vytc.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for ovr__gqn in block.body:
                if is_call_assign(ovr__gqn):
                    _convert_bodo_dispatcher_to_udf(ovr__gqn.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        stc__ulpvb = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags, isinstance(state.
            pipeline, BodoCompilerSeq))
        stc__ulpvb.run()
        return True


def _update_definitions(func_ir, node_list):
    yksh__swmje = ir.Loc('', 0)
    pkul__ialy = ir.Block(ir.Scope(None, yksh__swmje), yksh__swmje)
    pkul__ialy.body = node_list
    build_definitions({(0): pkul__ialy}, func_ir._definitions)


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
        ubkaf__jls = 'overload_series_' + rhs.attr
        xabaj__aekqj = getattr(bodo.hiframes.series_impl, ubkaf__jls)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        ubkaf__jls = 'overload_dataframe_' + rhs.attr
        xabaj__aekqj = getattr(bodo.hiframes.dataframe_impl, ubkaf__jls)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    ihaba__owwe = xabaj__aekqj(rhs_type)
    objjp__ynthe = TypingInfo(typingctx, targetctx, typemap, calltypes,
        stmt.loc)
    trax__fov = compile_func_single_block(ihaba__owwe, (rhs.value,), stmt.
        target, objjp__ynthe)
    _update_definitions(func_ir, trax__fov)
    new_body += trax__fov
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
        uyyea__xqhc = tuple(typemap[kqnn__dgy.name] for kqnn__dgy in rhs.args)
        kgqo__yme = {gyfdi__lbc: typemap[kqnn__dgy.name] for gyfdi__lbc,
            kqnn__dgy in dict(rhs.kws).items()}
        ihaba__owwe = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*uyyea__xqhc, **kgqo__yme)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        uyyea__xqhc = tuple(typemap[kqnn__dgy.name] for kqnn__dgy in rhs.args)
        kgqo__yme = {gyfdi__lbc: typemap[kqnn__dgy.name] for gyfdi__lbc,
            kqnn__dgy in dict(rhs.kws).items()}
        ihaba__owwe = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*uyyea__xqhc, **kgqo__yme)
    else:
        return False
    gebm__jxqo = replace_func(pass_info, ihaba__owwe, rhs.args, pysig=numba
        .core.utils.pysignature(ihaba__owwe), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    qkphw__oppgp, qmjf__oma = inline_closure_call(func_ir, gebm__jxqo.glbls,
        block, len(new_body), gebm__jxqo.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=gebm__jxqo.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for zoiop__oddux in qkphw__oppgp.values():
        zoiop__oddux.loc = rhs.loc
        update_locs(zoiop__oddux.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    gdq__nst = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = gdq__nst(func_ir, typemap)
    hymx__qnu = func_ir.blocks
    work_list = list((lcerl__aeop, hymx__qnu[lcerl__aeop]) for lcerl__aeop in
        reversed(hymx__qnu.keys()))
    while work_list:
        nkwd__wiom, block = work_list.pop()
        new_body = []
        btej__uum = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                opy__yxby = guard(find_callname, func_ir, rhs, typemap)
                if opy__yxby is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = opy__yxby
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    btej__uum = True
                    break
            new_body.append(stmt)
        if not btej__uum:
            hymx__qnu[nkwd__wiom].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        vajd__gtnle = DistributedPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = vajd__gtnle.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        resh__ubaks = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        cump__mlvtf = resh__ubaks.run()
        caw__seyrd = cump__mlvtf
        if caw__seyrd:
            caw__seyrd = resh__ubaks.run()
        if caw__seyrd:
            resh__ubaks.run()
        return cump__mlvtf


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        yzcfd__cwu = 0
        nvnk__jdzki = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            yzcfd__cwu = int(os.environ[nvnk__jdzki])
        except:
            pass
        if yzcfd__cwu > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(yzcfd__cwu,
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
        objjp__ynthe = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, objjp__ynthe)
        for block in state.func_ir.blocks.values():
            new_body = []
            for ovr__gqn in block.body:
                if type(ovr__gqn) in distributed_run_extensions:
                    ghi__ddgw = distributed_run_extensions[type(ovr__gqn)]
                    if isinstance(ovr__gqn, bodo.ir.parquet_ext.ParquetReader
                        ) or isinstance(ovr__gqn, bodo.ir.sql_ext.SqlReader
                        ) and ovr__gqn.db_type in ('iceberg', 'snowflake'):
                        offr__zht = ghi__ddgw(ovr__gqn, None, state.typemap,
                            state.calltypes, state.typingctx, state.
                            targetctx, is_independent=True,
                            meta_head_only_info=None)
                    else:
                        offr__zht = ghi__ddgw(ovr__gqn, None, state.typemap,
                            state.calltypes, state.typingctx, state.targetctx)
                    new_body += offr__zht
                elif is_call_assign(ovr__gqn):
                    rhs = ovr__gqn.value
                    opy__yxby = guard(find_callname, state.func_ir, rhs)
                    if opy__yxby == ('gatherv', 'bodo') or opy__yxby == (
                        'allgatherv', 'bodo'):
                        lwtn__ljcqp = state.typemap[ovr__gqn.target.name]
                        mqg__koxks = state.typemap[rhs.args[0].name]
                        if isinstance(mqg__koxks, types.Array) and isinstance(
                            lwtn__ljcqp, types.Array):
                            efhce__ubz = mqg__koxks.copy(readonly=False)
                            acv__ipbat = lwtn__ljcqp.copy(readonly=False)
                            if efhce__ubz == acv__ipbat:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), ovr__gqn.target, objjp__ynthe)
                                continue
                        if (lwtn__ljcqp != mqg__koxks and 
                            to_str_arr_if_dict_array(lwtn__ljcqp) ==
                            to_str_arr_if_dict_array(mqg__koxks)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), ovr__gqn.target,
                                objjp__ynthe, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            ovr__gqn.value = rhs.args[0]
                    new_body.append(ovr__gqn)
                else:
                    new_body.append(ovr__gqn)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        uls__ffmcu = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return uls__ffmcu.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    hmq__cjz = set()
    while work_list:
        nkwd__wiom, block = work_list.pop()
        hmq__cjz.add(nkwd__wiom)
        for i, asf__ymjm in enumerate(block.body):
            if isinstance(asf__ymjm, ir.Assign):
                gqlnq__ouj = asf__ymjm.value
                if isinstance(gqlnq__ouj, ir.Expr) and gqlnq__ouj.op == 'call':
                    kig__eyw = guard(get_definition, func_ir, gqlnq__ouj.func)
                    if isinstance(kig__eyw, (ir.Global, ir.FreeVar)
                        ) and isinstance(kig__eyw.value, CPUDispatcher
                        ) and issubclass(kig__eyw.value._compiler.
                        pipeline_class, BodoCompiler):
                        fbk__mef = kig__eyw.value.py_func
                        arg_types = None
                        if typingctx:
                            uvgyr__dkc = dict(gqlnq__ouj.kws)
                            vwrg__llwya = tuple(typemap[kqnn__dgy.name] for
                                kqnn__dgy in gqlnq__ouj.args)
                            qajx__btg = {hrwe__effo: typemap[kqnn__dgy.name
                                ] for hrwe__effo, kqnn__dgy in uvgyr__dkc.
                                items()}
                            qmjf__oma, arg_types = (kig__eyw.value.
                                fold_argument_types(vwrg__llwya, qajx__btg))
                        qmjf__oma, dqte__mnf = inline_closure_call(func_ir,
                            fbk__mef.__globals__, block, i, fbk__mef,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((dqte__mnf[hrwe__effo].name,
                            kqnn__dgy) for hrwe__effo, kqnn__dgy in
                            kig__eyw.value.locals.items() if hrwe__effo in
                            dqte__mnf)
                        break
    return hmq__cjz


def udf_jit(signature_or_function=None, **options):
    kru__oai = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=kru__oai,
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
    for mah__lmnh, (ftu__xkto, qmjf__oma) in enumerate(pm.passes):
        if ftu__xkto == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:mah__lmnh + 1]
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
    hfn__kbgg = None
    nnh__gami = None
    _locals = {}
    dyb__qayg = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(dyb__qayg, arg_types,
        kw_types)
    mbx__erjgw = numba.core.compiler.Flags()
    ddtt__nhx = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    jgx__hlxg = {'nopython': True, 'boundscheck': False, 'parallel': ddtt__nhx}
    numba.core.registry.cpu_target.options.parse_as_flags(mbx__erjgw, jgx__hlxg
        )
    yvwi__djg = TyperCompiler(typingctx, targetctx, hfn__kbgg, args,
        nnh__gami, mbx__erjgw, _locals)
    return yvwi__djg.compile_extra(func)
