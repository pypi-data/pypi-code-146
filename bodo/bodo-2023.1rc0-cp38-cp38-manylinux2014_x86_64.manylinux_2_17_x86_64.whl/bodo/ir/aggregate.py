"""IR node for the groupby"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, decref_table_array, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, py_data_to_cpp_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, _find_used_columns, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, list_cumulative, to_str_arr_if_dict_array, type_has_unknown_cats, unwrap_typeref
from bodo.utils.utils import gen_getitem, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        arjl__cdqe = func.signature
        if arjl__cdqe == types.none(types.voidptr):
            gqcki__tusj = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            jwcgi__imr = cgutils.get_or_insert_function(builder.module,
                gqcki__tusj, sym._literal_value)
            builder.call(jwcgi__imr, [context.get_constant_null(arjl__cdqe.
                args[0])])
        elif arjl__cdqe == types.none(types.int64, types.voidptr, types.voidptr
            ):
            gqcki__tusj = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            jwcgi__imr = cgutils.get_or_insert_function(builder.module,
                gqcki__tusj, sym._literal_value)
            builder.call(jwcgi__imr, [context.get_constant(types.int64, 0),
                context.get_constant_null(arjl__cdqe.args[1]), context.
                get_constant_null(arjl__cdqe.args[2])])
        else:
            gqcki__tusj = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            jwcgi__imr = cgutils.get_or_insert_function(builder.module,
                gqcki__tusj, sym._literal_value)
            builder.call(jwcgi__imr, [context.get_constant_null(arjl__cdqe.
                args[0]), context.get_constant_null(arjl__cdqe.args[1]),
                context.get_constant_null(arjl__cdqe.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'ngroup', 'head', 'transform', 'size',
    'shift', 'sum', 'count', 'nunique', 'median', 'cumsum', 'cumprod',
    'cummin', 'cummax', 'mean', 'min', 'max', 'prod', 'first', 'last',
    'idxmin', 'idxmax', 'var', 'std', 'boolor_agg', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last', 'boolor_agg'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        hgbpv__iav = True
        jgu__qox = 1
        vtn__xcv = -1
        if isinstance(rhs, ir.Expr):
            for pdp__sjmiy in rhs.kws:
                if func_name in list_cumulative:
                    if pdp__sjmiy[0] == 'skipna':
                        hgbpv__iav = guard(find_const, func_ir, pdp__sjmiy[1])
                        if not isinstance(hgbpv__iav, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if pdp__sjmiy[0] == 'dropna':
                        hgbpv__iav = guard(find_const, func_ir, pdp__sjmiy[1])
                        if not isinstance(hgbpv__iav, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            jgu__qox = get_call_expr_arg('shift', rhs.args, dict(rhs.kws), 
                0, 'periods', jgu__qox)
            jgu__qox = guard(find_const, func_ir, jgu__qox)
        if func_name == 'head':
            vtn__xcv = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 0,
                'n', 5)
            if not isinstance(vtn__xcv, int):
                vtn__xcv = guard(find_const, func_ir, vtn__xcv)
            if vtn__xcv < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = hgbpv__iav
        func.periods = jgu__qox
        func.head_n = vtn__xcv
        if func_name == 'transform':
            kws = dict(rhs.kws)
            pyko__fhxry = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            dhhnj__qyjo = typemap[pyko__fhxry.name]
            eyrd__jluwu = None
            if isinstance(dhhnj__qyjo, str):
                eyrd__jluwu = dhhnj__qyjo
            elif is_overload_constant_str(dhhnj__qyjo):
                eyrd__jluwu = get_overload_const_str(dhhnj__qyjo)
            elif bodo.utils.typing.is_builtin_function(dhhnj__qyjo):
                eyrd__jluwu = bodo.utils.typing.get_builtin_function_name(
                    dhhnj__qyjo)
            if eyrd__jluwu not in bodo.ir.aggregate.supported_transform_funcs[:
                ]:
                raise BodoError(f'unsupported transform function {eyrd__jluwu}'
                    )
            func.transform_func = supported_agg_funcs.index(eyrd__jluwu)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    pyko__fhxry = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if pyko__fhxry == '':
        dhhnj__qyjo = types.none
    else:
        dhhnj__qyjo = typemap[pyko__fhxry.name]
    if is_overload_constant_dict(dhhnj__qyjo):
        meyk__hwbmk = get_overload_constant_dict(dhhnj__qyjo)
        tjwp__nauxi = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in meyk__hwbmk.values()]
        return tjwp__nauxi
    if dhhnj__qyjo == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(dhhnj__qyjo, types.BaseTuple) or is_overload_constant_list(
        dhhnj__qyjo):
        tjwp__nauxi = []
        osjr__stzcq = 0
        if is_overload_constant_list(dhhnj__qyjo):
            njojr__kdxr = get_overload_const_list(dhhnj__qyjo)
        else:
            njojr__kdxr = dhhnj__qyjo.types
        for t in njojr__kdxr:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                tjwp__nauxi.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(njojr__kdxr) > 1:
                    func.fname = '<lambda_' + str(osjr__stzcq) + '>'
                    osjr__stzcq += 1
                tjwp__nauxi.append(func)
        return [tjwp__nauxi]
    if is_overload_constant_str(dhhnj__qyjo):
        func_name = get_overload_const_str(dhhnj__qyjo)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(dhhnj__qyjo):
        func_name = bodo.utils.typing.get_builtin_function_name(dhhnj__qyjo)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        osjr__stzcq = 0
        xihpr__jpk = []
        for gfawd__lyj in f_val:
            func = get_agg_func_udf(func_ir, gfawd__lyj, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{osjr__stzcq}>'
                osjr__stzcq += 1
            xihpr__jpk.append(func)
        return xihpr__jpk
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    eyrd__jluwu = code.co_name
    return eyrd__jluwu


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            qlxy__tqg = types.DType(args[0])
            return signature(qlxy__tqg, *args)


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_vars, in_vars, in_key_inds, df_in_type, out_type,
        input_has_index, same_index, return_key, loc, func_name, dropna,
        _num_shuffle_keys):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_vars = out_vars
        self.in_vars = in_vars
        self.in_key_inds = in_key_inds
        self.df_in_type = df_in_type
        self.out_type = out_type
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self._num_shuffle_keys = _num_shuffle_keys
        self.dead_in_inds = set()
        self.dead_out_inds = set()

    def get_live_in_vars(self):
        return [slc__jqx for slc__jqx in self.in_vars if slc__jqx is not None]

    def get_live_out_vars(self):
        return [slc__jqx for slc__jqx in self.out_vars if slc__jqx is not None]

    @property
    def is_in_table_format(self):
        return self.df_in_type.is_table_format

    @property
    def n_in_table_arrays(self):
        return len(self.df_in_type.columns
            ) if self.df_in_type.is_table_format else 1

    @property
    def n_in_cols(self):
        return self.n_in_table_arrays + len(self.in_vars) - 1

    @property
    def in_col_types(self):
        return list(self.df_in_type.data) + list(get_index_data_arr_types(
            self.df_in_type.index))

    @property
    def is_output_table(self):
        return not isinstance(self.out_type, SeriesType)

    @property
    def n_out_table_arrays(self):
        return len(self.out_type.table_type.arr_types) if not isinstance(self
            .out_type, SeriesType) else 1

    @property
    def n_out_cols(self):
        return self.n_out_table_arrays + len(self.out_vars) - 1

    @property
    def out_col_types(self):
        ofm__mnnan = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        kvdwa__uwqfo = list(get_index_data_arr_types(self.out_type.index))
        return ofm__mnnan + kvdwa__uwqfo

    def update_dead_col_info(self):
        for efm__pdp in self.dead_out_inds:
            self.gb_info_out.pop(efm__pdp, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for xpecd__skqh, zyls__ycx in self.gb_info_in.copy().items():
            xso__jwwko = []
            for gfawd__lyj, tgt__uhv in zyls__ycx:
                if tgt__uhv not in self.dead_out_inds:
                    xso__jwwko.append((gfawd__lyj, tgt__uhv))
            if not xso__jwwko:
                if (xpecd__skqh is not None and xpecd__skqh not in self.
                    in_key_inds):
                    self.dead_in_inds.add(xpecd__skqh)
                self.gb_info_in.pop(xpecd__skqh)
            else:
                self.gb_info_in[xpecd__skqh] = xso__jwwko
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for jbp__lixid in range(1, len(self.in_vars)):
                efm__pdp = self.n_in_table_arrays + jbp__lixid - 1
                if efm__pdp in self.dead_in_inds:
                    self.in_vars[jbp__lixid] = None
        else:
            for jbp__lixid in range(len(self.in_vars)):
                if jbp__lixid in self.dead_in_inds:
                    self.in_vars[jbp__lixid] = None

    def __repr__(self):
        oaf__kbf = ', '.join(slc__jqx.name for slc__jqx in self.
            get_live_in_vars())
        mlwx__cndf = f'{self.df_in}{{{oaf__kbf}}}'
        wcxv__gnpby = ', '.join(slc__jqx.name for slc__jqx in self.
            get_live_out_vars())
        arnab__secl = f'{self.df_out}{{{wcxv__gnpby}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {mlwx__cndf} {arnab__secl}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({slc__jqx.name for slc__jqx in aggregate_node.
        get_live_in_vars()})
    def_set.update({slc__jqx.name for slc__jqx in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    opyw__ecnx = agg_node.out_vars[0]
    if opyw__ecnx is not None and opyw__ecnx.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            hqno__dqo = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(hqno__dqo)
        else:
            agg_node.dead_out_inds.add(0)
    for jbp__lixid in range(1, len(agg_node.out_vars)):
        slc__jqx = agg_node.out_vars[jbp__lixid]
        if slc__jqx is not None and slc__jqx.name not in lives:
            agg_node.out_vars[jbp__lixid] = None
            efm__pdp = agg_node.n_out_table_arrays + jbp__lixid - 1
            agg_node.dead_out_inds.add(efm__pdp)
    if all(slc__jqx is None for slc__jqx in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    fozy__doi = {slc__jqx.name for slc__jqx in aggregate_node.
        get_live_out_vars()}
    return set(), fozy__doi


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for jbp__lixid in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[jbp__lixid] is not None:
            aggregate_node.in_vars[jbp__lixid] = replace_vars_inner(
                aggregate_node.in_vars[jbp__lixid], var_dict)
    for jbp__lixid in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[jbp__lixid] is not None:
            aggregate_node.out_vars[jbp__lixid] = replace_vars_inner(
                aggregate_node.out_vars[jbp__lixid], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for jbp__lixid in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[jbp__lixid] is not None:
            aggregate_node.in_vars[jbp__lixid] = visit_vars_inner(
                aggregate_node.in_vars[jbp__lixid], callback, cbdata)
    for jbp__lixid in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[jbp__lixid] is not None:
            aggregate_node.out_vars[jbp__lixid] = visit_vars_inner(
                aggregate_node.out_vars[jbp__lixid], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    nogym__zkvo = []
    for ebmp__cnen in aggregate_node.get_live_in_vars():
        fbe__necge = equiv_set.get_shape(ebmp__cnen)
        if fbe__necge is not None:
            nogym__zkvo.append(fbe__necge[0])
    if len(nogym__zkvo) > 1:
        equiv_set.insert_equiv(*nogym__zkvo)
    hybbk__vud = []
    nogym__zkvo = []
    for ebmp__cnen in aggregate_node.get_live_out_vars():
        symt__nmo = typemap[ebmp__cnen.name]
        hzwmk__ztmv = array_analysis._gen_shape_call(equiv_set, ebmp__cnen,
            symt__nmo.ndim, None, hybbk__vud)
        equiv_set.insert_equiv(ebmp__cnen, hzwmk__ztmv)
        nogym__zkvo.append(hzwmk__ztmv[0])
        equiv_set.define(ebmp__cnen, set())
    if len(nogym__zkvo) > 1:
        equiv_set.insert_equiv(*nogym__zkvo)
    return [], hybbk__vud


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    hsz__bimz = aggregate_node.get_live_in_vars()
    yke__porg = aggregate_node.get_live_out_vars()
    eecw__myh = Distribution.OneD
    for ebmp__cnen in hsz__bimz:
        eecw__myh = Distribution(min(eecw__myh.value, array_dists[
            ebmp__cnen.name].value))
    eapd__wksg = Distribution(min(eecw__myh.value, Distribution.OneD_Var.value)
        )
    for ebmp__cnen in yke__porg:
        if ebmp__cnen.name in array_dists:
            eapd__wksg = Distribution(min(eapd__wksg.value, array_dists[
                ebmp__cnen.name].value))
    if eapd__wksg != Distribution.OneD_Var:
        eecw__myh = eapd__wksg
    for ebmp__cnen in hsz__bimz:
        array_dists[ebmp__cnen.name] = eecw__myh
    for ebmp__cnen in yke__porg:
        array_dists[ebmp__cnen.name] = eapd__wksg


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ebmp__cnen in agg_node.get_live_out_vars():
        definitions[ebmp__cnen.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    rnf__wrveq = agg_node.get_live_in_vars()
    phv__gggvq = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for slc__jqx in (rnf__wrveq + phv__gggvq):
            if array_dists[slc__jqx.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                slc__jqx.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    tjwp__nauxi = []
    func_out_types = []
    for tgt__uhv, (xpecd__skqh, func) in agg_node.gb_info_out.items():
        if xpecd__skqh is not None:
            t = agg_node.in_col_types[xpecd__skqh]
            in_col_typs.append(t)
        tjwp__nauxi.append(func)
        func_out_types.append(out_col_typs[tgt__uhv])
    izbo__utjbz = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for jbp__lixid, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            izbo__utjbz.update({f'in_cat_dtype_{jbp__lixid}': in_col_typ})
    for jbp__lixid, qlhxf__xvew in enumerate(out_col_typs):
        if isinstance(qlhxf__xvew, bodo.CategoricalArrayType):
            izbo__utjbz.update({f'out_cat_dtype_{jbp__lixid}': qlhxf__xvew})
    udf_func_struct = get_udf_func_struct(tjwp__nauxi, in_col_typs,
        typingctx, targetctx)
    out_var_types = [(typemap[slc__jqx.name] if slc__jqx is not None else
        types.none) for slc__jqx in agg_node.out_vars]
    sbf__dqxl, mtr__yogll = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, func_out_types, parallel, udf_func_struct,
        out_var_types, typemap)
    izbo__utjbz.update(mtr__yogll)
    izbo__utjbz.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'decref_table_array': decref_table_array, 'decode_if_dict_array':
        decode_if_dict_array, 'set_table_data': bodo.hiframes.table.
        set_table_data, 'get_table_data': bodo.hiframes.table.
        get_table_data, 'out_typs': out_col_typs})
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            izbo__utjbz.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            izbo__utjbz.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    iwj__ulgj = {}
    exec(sbf__dqxl, {}, iwj__ulgj)
    oryxv__aey = iwj__ulgj['agg_top']
    ltnf__jgk = compile_to_numba_ir(oryxv__aey, izbo__utjbz, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[slc__jqx.
        name] for slc__jqx in rnf__wrveq), typemap=typemap, calltypes=calltypes
        ).blocks.popitem()[1]
    replace_arg_nodes(ltnf__jgk, rnf__wrveq)
    easew__lstgo = ltnf__jgk.body[-2].value.value
    fupep__wiv = ltnf__jgk.body[:-2]
    for jbp__lixid, slc__jqx in enumerate(phv__gggvq):
        gen_getitem(slc__jqx, easew__lstgo, jbp__lixid, calltypes, fupep__wiv)
    return fupep__wiv


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        mjvuv__cmc = IntDtype(t.dtype).name
        assert mjvuv__cmc.endswith('Dtype()')
        mjvuv__cmc = mjvuv__cmc[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{mjvuv__cmc}'))"
            )
    elif isinstance(t, FloatingArrayType):
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1.0], dtype='{t.dtype}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif t == bodo.dict_str_arr_type:
        return (
            'bodo.libs.dict_arr_ext.init_dict_arr(pre_alloc_string_array(1, 1), bodo.libs.int_arr_ext.alloc_int_array(1, np.int32), False, False)'
            )
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        gydh__jwroy = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {gydh__jwroy}_cat_dtype_{colnum})'
            )
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    do_combine, func_idx_to_in_col, label_suffix):
    spp__hpe = udf_func_struct.var_typs
    fuh__dke = len(spp__hpe)
    sbf__dqxl = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    sbf__dqxl += '    if is_null_pointer(in_table):\n'
    sbf__dqxl += '        return\n'
    sbf__dqxl += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in spp__hpe]), ',' if
        len(spp__hpe) == 1 else '')
    eisr__xytb = n_keys
    rqt__naz = []
    redvar_offsets = []
    edus__dhf = []
    if do_combine:
        for jbp__lixid, gfawd__lyj in enumerate(allfuncs):
            if gfawd__lyj.ftype != 'udf':
                eisr__xytb += gfawd__lyj.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(eisr__xytb, eisr__xytb +
                    gfawd__lyj.n_redvars))
                eisr__xytb += gfawd__lyj.n_redvars
                edus__dhf.append(data_in_typs_[func_idx_to_in_col[jbp__lixid]])
                rqt__naz.append(func_idx_to_in_col[jbp__lixid] + n_keys)
    else:
        for jbp__lixid, gfawd__lyj in enumerate(allfuncs):
            if gfawd__lyj.ftype != 'udf':
                eisr__xytb += gfawd__lyj.ncols_post_shuffle
            else:
                redvar_offsets += list(range(eisr__xytb + 1, eisr__xytb + 1 +
                    gfawd__lyj.n_redvars))
                eisr__xytb += gfawd__lyj.n_redvars + 1
                edus__dhf.append(data_in_typs_[func_idx_to_in_col[jbp__lixid]])
                rqt__naz.append(func_idx_to_in_col[jbp__lixid] + n_keys)
    assert len(redvar_offsets) == fuh__dke
    msiud__eukxs = len(edus__dhf)
    pkkh__lneae = []
    for jbp__lixid, t in enumerate(edus__dhf):
        pkkh__lneae.append(_gen_dummy_alloc(t, jbp__lixid, True))
    sbf__dqxl += '    data_in_dummy = ({}{})\n'.format(','.join(pkkh__lneae
        ), ',' if len(edus__dhf) == 1 else '')
    sbf__dqxl += """
    # initialize redvar cols
"""
    sbf__dqxl += '    init_vals = __init_func()\n'
    for jbp__lixid in range(fuh__dke):
        sbf__dqxl += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(jbp__lixid, redvar_offsets[jbp__lixid], jbp__lixid))
        sbf__dqxl += '    incref(redvar_arr_{})\n'.format(jbp__lixid)
        sbf__dqxl += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            jbp__lixid, jbp__lixid)
    sbf__dqxl += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(jbp__lixid) for jbp__lixid in range(fuh__dke)]), ',' if 
        fuh__dke == 1 else '')
    sbf__dqxl += '\n'
    for jbp__lixid in range(msiud__eukxs):
        sbf__dqxl += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(jbp__lixid, rqt__naz[jbp__lixid], jbp__lixid))
        sbf__dqxl += '    incref(data_in_{})\n'.format(jbp__lixid)
    sbf__dqxl += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(jbp__lixid) for jbp__lixid in range(msiud__eukxs)]), ',' if 
        msiud__eukxs == 1 else '')
    sbf__dqxl += '\n'
    sbf__dqxl += '    for i in range(len(data_in_0)):\n'
    sbf__dqxl += '        w_ind = row_to_group[i]\n'
    sbf__dqxl += '        if w_ind != -1:\n'
    sbf__dqxl += '            __update_redvars(redvars, data_in, w_ind, i)\n'
    iwj__ulgj = {}
    exec(sbf__dqxl, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, iwj__ulgj)
    return iwj__ulgj['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    spp__hpe = udf_func_struct.var_typs
    fuh__dke = len(spp__hpe)
    sbf__dqxl = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    sbf__dqxl += '    if is_null_pointer(in_table):\n'
    sbf__dqxl += '        return\n'
    sbf__dqxl += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in spp__hpe]), ',' if
        len(spp__hpe) == 1 else '')
    jvsx__hefct = n_keys
    xkk__ebqq = n_keys
    wrhf__nso = []
    wnxxd__ugwr = []
    for gfawd__lyj in allfuncs:
        if gfawd__lyj.ftype != 'udf':
            jvsx__hefct += gfawd__lyj.ncols_pre_shuffle
            xkk__ebqq += gfawd__lyj.ncols_post_shuffle
        else:
            wrhf__nso += list(range(jvsx__hefct, jvsx__hefct + gfawd__lyj.
                n_redvars))
            wnxxd__ugwr += list(range(xkk__ebqq + 1, xkk__ebqq + 1 +
                gfawd__lyj.n_redvars))
            jvsx__hefct += gfawd__lyj.n_redvars
            xkk__ebqq += 1 + gfawd__lyj.n_redvars
    assert len(wrhf__nso) == fuh__dke
    sbf__dqxl += """
    # initialize redvar cols
"""
    sbf__dqxl += '    init_vals = __init_func()\n'
    for jbp__lixid in range(fuh__dke):
        sbf__dqxl += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(jbp__lixid, wnxxd__ugwr[jbp__lixid], jbp__lixid))
        sbf__dqxl += '    incref(redvar_arr_{})\n'.format(jbp__lixid)
        sbf__dqxl += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            jbp__lixid, jbp__lixid)
    sbf__dqxl += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(jbp__lixid) for jbp__lixid in range(fuh__dke)]), ',' if 
        fuh__dke == 1 else '')
    sbf__dqxl += '\n'
    for jbp__lixid in range(fuh__dke):
        sbf__dqxl += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(jbp__lixid, wrhf__nso[jbp__lixid], jbp__lixid))
        sbf__dqxl += '    incref(recv_redvar_arr_{})\n'.format(jbp__lixid)
    sbf__dqxl += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(jbp__lixid) for jbp__lixid in range(
        fuh__dke)]), ',' if fuh__dke == 1 else '')
    sbf__dqxl += '\n'
    if fuh__dke:
        sbf__dqxl += '    for i in range(len(recv_redvar_arr_0)):\n'
        sbf__dqxl += '        w_ind = row_to_group[i]\n'
        sbf__dqxl += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    iwj__ulgj = {}
    exec(sbf__dqxl, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, iwj__ulgj)
    return iwj__ulgj['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    spp__hpe = udf_func_struct.var_typs
    fuh__dke = len(spp__hpe)
    eisr__xytb = n_keys
    redvar_offsets = []
    feu__pmwn = []
    dzc__rse = []
    for jbp__lixid, gfawd__lyj in enumerate(allfuncs):
        if gfawd__lyj.ftype != 'udf':
            eisr__xytb += gfawd__lyj.ncols_post_shuffle
        else:
            feu__pmwn.append(eisr__xytb)
            redvar_offsets += list(range(eisr__xytb + 1, eisr__xytb + 1 +
                gfawd__lyj.n_redvars))
            eisr__xytb += 1 + gfawd__lyj.n_redvars
            dzc__rse.append(out_data_typs_[jbp__lixid])
    assert len(redvar_offsets) == fuh__dke
    msiud__eukxs = len(dzc__rse)
    sbf__dqxl = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    sbf__dqxl += '    if is_null_pointer(table):\n'
    sbf__dqxl += '        return\n'
    sbf__dqxl += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in spp__hpe]), ',' if
        len(spp__hpe) == 1 else '')
    sbf__dqxl += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in dzc__rse]
        ), ',' if len(dzc__rse) == 1 else '')
    for jbp__lixid in range(fuh__dke):
        sbf__dqxl += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(jbp__lixid, redvar_offsets[jbp__lixid], jbp__lixid))
        sbf__dqxl += '    incref(redvar_arr_{})\n'.format(jbp__lixid)
    sbf__dqxl += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(jbp__lixid) for jbp__lixid in range(fuh__dke)]), ',' if 
        fuh__dke == 1 else '')
    sbf__dqxl += '\n'
    for jbp__lixid in range(msiud__eukxs):
        sbf__dqxl += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(jbp__lixid, feu__pmwn[jbp__lixid], jbp__lixid))
        sbf__dqxl += '    incref(data_out_{})\n'.format(jbp__lixid)
    sbf__dqxl += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(jbp__lixid) for jbp__lixid in range(msiud__eukxs)]), ',' if 
        msiud__eukxs == 1 else '')
    sbf__dqxl += '\n'
    sbf__dqxl += '    for i in range(len(data_out_0)):\n'
    sbf__dqxl += '        __eval_res(redvars, data_out, i)\n'
    iwj__ulgj = {}
    exec(sbf__dqxl, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, iwj__ulgj)
    return iwj__ulgj['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    eisr__xytb = n_keys
    ojlyv__rmhbu = []
    for jbp__lixid, gfawd__lyj in enumerate(allfuncs):
        if gfawd__lyj.ftype == 'gen_udf':
            ojlyv__rmhbu.append(eisr__xytb)
            eisr__xytb += 1
        elif gfawd__lyj.ftype != 'udf':
            eisr__xytb += gfawd__lyj.ncols_post_shuffle
        else:
            eisr__xytb += gfawd__lyj.n_redvars + 1
    sbf__dqxl = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    sbf__dqxl += '    if num_groups == 0:\n'
    sbf__dqxl += '        return\n'
    for jbp__lixid, func in enumerate(udf_func_struct.general_udf_funcs):
        sbf__dqxl += '    # col {}\n'.format(jbp__lixid)
        sbf__dqxl += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(ojlyv__rmhbu[jbp__lixid], jbp__lixid))
        sbf__dqxl += '    incref(out_col)\n'
        sbf__dqxl += '    for j in range(num_groups):\n'
        sbf__dqxl += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(jbp__lixid, jbp__lixid))
        sbf__dqxl += '        incref(in_col)\n'
        sbf__dqxl += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(jbp__lixid))
    izbo__utjbz = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    iday__uma = 0
    for jbp__lixid, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[iday__uma]
        izbo__utjbz['func_{}'.format(iday__uma)] = func
        izbo__utjbz['in_col_{}_typ'.format(iday__uma)] = in_col_typs[
            func_idx_to_in_col[jbp__lixid]]
        izbo__utjbz['out_col_{}_typ'.format(iday__uma)] = out_col_typs[
            jbp__lixid]
        iday__uma += 1
    iwj__ulgj = {}
    exec(sbf__dqxl, izbo__utjbz, iwj__ulgj)
    gfawd__lyj = iwj__ulgj['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    tog__gcug = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(tog__gcug, nopython=True)(gfawd__lyj)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    szlbd__hon = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        fiiw__xnm = []
        if agg_node.in_vars[0] is not None:
            fiiw__xnm.append('arg0')
        for jbp__lixid in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if jbp__lixid not in agg_node.dead_in_inds:
                fiiw__xnm.append(f'arg{jbp__lixid}')
    else:
        fiiw__xnm = [f'arg{jbp__lixid}' for jbp__lixid, slc__jqx in
            enumerate(agg_node.in_vars) if slc__jqx is not None]
    sbf__dqxl = f"def agg_top({', '.join(fiiw__xnm)}):\n"
    juy__yvo = []
    if agg_node.is_in_table_format:
        juy__yvo = agg_node.in_key_inds + [xpecd__skqh for xpecd__skqh,
            aydc__siq in agg_node.gb_info_out.values() if xpecd__skqh is not
            None]
        if agg_node.input_has_index:
            juy__yvo.append(agg_node.n_in_cols - 1)
        eehu__ehsp = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        dbght__hxqoz = []
        for jbp__lixid in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if jbp__lixid in agg_node.dead_in_inds:
                dbght__hxqoz.append('None')
            else:
                dbght__hxqoz.append(f'arg{jbp__lixid}')
        hlb__yorb = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        sbf__dqxl += f"""    table = py_data_to_cpp_table({hlb__yorb}, ({', '.join(dbght__hxqoz)}{eehu__ehsp}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        krtjg__satur = [f'arg{jbp__lixid}' for jbp__lixid in agg_node.
            in_key_inds]
        epyp__ztym = [f'arg{xpecd__skqh}' for xpecd__skqh, aydc__siq in
            agg_node.gb_info_out.values() if xpecd__skqh is not None]
        wdaw__tpbr = krtjg__satur + epyp__ztym
        if agg_node.input_has_index:
            wdaw__tpbr.append(f'arg{len(agg_node.in_vars) - 1}')
        sbf__dqxl += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({qtipm__tgn})' for qtipm__tgn in wdaw__tpbr))
        sbf__dqxl += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    pauk__gpo = []
    func_idx_to_in_col = []
    uxssr__txei = []
    hgbpv__iav = False
    lelyp__blnwg = 1
    vtn__xcv = -1
    bcn__ilul = 0
    wgv__gmrg = 0
    tjwp__nauxi = [func for aydc__siq, func in agg_node.gb_info_out.values()]
    for dls__nadzy, func in enumerate(tjwp__nauxi):
        pauk__gpo.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            bcn__ilul += 1
        if hasattr(func, 'skipdropna'):
            hgbpv__iav = func.skipdropna
        if func.ftype == 'shift':
            lelyp__blnwg = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            wgv__gmrg = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            vtn__xcv = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(dls__nadzy)
        if func.ftype == 'udf':
            uxssr__txei.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            uxssr__txei.append(0)
            do_combine = False
    pauk__gpo.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if bcn__ilul > 0:
        if bcn__ilul != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    hnh__xehrk = []
    if udf_func_struct is not None:
        zll__cga = next_label()
        if udf_func_struct.regular_udfs:
            tog__gcug = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            fec__lprn = numba.cfunc(tog__gcug, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs, do_combine,
                func_idx_to_in_col, zll__cga))
            boaxl__ghvq = numba.cfunc(tog__gcug, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, zll__cga))
            htzsb__rlryc = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys,
                func_out_types, zll__cga))
            udf_func_struct.set_regular_cfuncs(fec__lprn, boaxl__ghvq,
                htzsb__rlryc)
            for oec__wzqcr in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[oec__wzqcr.native_name] = oec__wzqcr
                gb_agg_cfunc_addr[oec__wzqcr.native_name] = oec__wzqcr.address
        if udf_func_struct.general_udfs:
            jsdte__zrmj = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, func_out_types, func_idx_to_in_col,
                zll__cga)
            udf_func_struct.set_general_cfunc(jsdte__zrmj)
        spp__hpe = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        kvu__rjgip = 0
        jbp__lixid = 0
        for brfqz__ucg, gfawd__lyj in zip(agg_node.gb_info_out.keys(), allfuncs
            ):
            if gfawd__lyj.ftype in ('udf', 'gen_udf'):
                hnh__xehrk.append(out_col_typs[brfqz__ucg])
                for dzt__gywy in range(kvu__rjgip, kvu__rjgip + uxssr__txei
                    [jbp__lixid]):
                    hnh__xehrk.append(dtype_to_array_type(spp__hpe[dzt__gywy]))
                kvu__rjgip += uxssr__txei[jbp__lixid]
                jbp__lixid += 1
        sbf__dqxl += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{jbp__lixid}' for jbp__lixid in range(len(hnh__xehrk)))}{',' if len(hnh__xehrk) == 1 else ''}))
"""
        sbf__dqxl += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(hnh__xehrk)})
"""
        if udf_func_struct.regular_udfs:
            sbf__dqxl += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{fec__lprn.native_name}')\n"
                )
            sbf__dqxl += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{boaxl__ghvq.native_name}')\n"
                )
            sbf__dqxl += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{htzsb__rlryc.native_name}')\n"
                )
            sbf__dqxl += (
                f"    cpp_cb_update_addr = get_agg_udf_addr('{fec__lprn.native_name}')\n"
                )
            sbf__dqxl += f"""    cpp_cb_combine_addr = get_agg_udf_addr('{boaxl__ghvq.native_name}')
"""
            sbf__dqxl += (
                f"    cpp_cb_eval_addr = get_agg_udf_addr('{htzsb__rlryc.native_name}')\n"
                )
        else:
            sbf__dqxl += '    cpp_cb_update_addr = 0\n'
            sbf__dqxl += '    cpp_cb_combine_addr = 0\n'
            sbf__dqxl += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            oec__wzqcr = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[oec__wzqcr.native_name] = oec__wzqcr
            gb_agg_cfunc_addr[oec__wzqcr.native_name] = oec__wzqcr.address
            sbf__dqxl += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{oec__wzqcr.native_name}')\n"
                )
            sbf__dqxl += (
                f"    cpp_cb_general_addr = get_agg_udf_addr('{oec__wzqcr.native_name}')\n"
                )
        else:
            sbf__dqxl += '    cpp_cb_general_addr = 0\n'
    else:
        sbf__dqxl += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        sbf__dqxl += '    cpp_cb_update_addr = 0\n'
        sbf__dqxl += '    cpp_cb_combine_addr = 0\n'
        sbf__dqxl += '    cpp_cb_eval_addr = 0\n'
        sbf__dqxl += '    cpp_cb_general_addr = 0\n'
    sbf__dqxl += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(gfawd__lyj.ftype)) for
        gfawd__lyj in allfuncs] + ['0']))
    sbf__dqxl += (
        f'    func_offsets = np.array({str(pauk__gpo)}, dtype=np.int32)\n')
    if len(uxssr__txei) > 0:
        sbf__dqxl += (
            f'    udf_ncols = np.array({str(uxssr__txei)}, dtype=np.int32)\n')
    else:
        sbf__dqxl += '    udf_ncols = np.array([0], np.int32)\n'
    sbf__dqxl += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    hasl__wzpm = (agg_node._num_shuffle_keys if agg_node._num_shuffle_keys !=
        -1 else n_keys)
    sbf__dqxl += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {hgbpv__iav}, {lelyp__blnwg}, {wgv__gmrg}, {vtn__xcv}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {hasl__wzpm})
"""
    eetr__csc = []
    ealjr__mixtt = 0
    if agg_node.return_key:
        jxgdu__vkxn = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for jbp__lixid in range(n_keys):
            efm__pdp = jxgdu__vkxn + jbp__lixid
            eetr__csc.append(efm__pdp if efm__pdp not in agg_node.
                dead_out_inds else -1)
            ealjr__mixtt += 1
    for brfqz__ucg in agg_node.gb_info_out.keys():
        eetr__csc.append(brfqz__ucg)
        ealjr__mixtt += 1
    viapu__yfihy = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            eetr__csc.append(agg_node.n_out_cols - 1)
        else:
            viapu__yfihy = True
    eehu__ehsp = ',' if szlbd__hon == 1 else ''
    ypcl__plh = (
        f"({', '.join(f'out_type{jbp__lixid}' for jbp__lixid in range(szlbd__hon))}{eehu__ehsp})"
        )
    env__wdobc = []
    yley__nqqg = []
    for jbp__lixid, t in enumerate(out_col_typs):
        if jbp__lixid not in agg_node.dead_out_inds and type_has_unknown_cats(t
            ):
            if jbp__lixid in agg_node.gb_info_out:
                xpecd__skqh = agg_node.gb_info_out[jbp__lixid][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                lco__ppo = jbp__lixid - jxgdu__vkxn
                xpecd__skqh = agg_node.in_key_inds[lco__ppo]
            yley__nqqg.append(jbp__lixid)
            if (agg_node.is_in_table_format and xpecd__skqh < agg_node.
                n_in_table_arrays):
                env__wdobc.append(f'get_table_data(arg0, {xpecd__skqh})')
            else:
                env__wdobc.append(f'arg{xpecd__skqh}')
    eehu__ehsp = ',' if len(env__wdobc) == 1 else ''
    sbf__dqxl += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {ypcl__plh}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(env__wdobc)}{eehu__ehsp}), unknown_cat_out_inds)
"""
    sbf__dqxl += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    sbf__dqxl += '    delete_table_decref_arrays(table)\n'
    sbf__dqxl += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for jbp__lixid in range(n_keys):
            if eetr__csc[jbp__lixid] == -1:
                sbf__dqxl += (
                    f'    decref_table_array(out_table, {jbp__lixid})\n')
    if viapu__yfihy:
        pwxb__kotl = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        sbf__dqxl += f'    decref_table_array(out_table, {pwxb__kotl})\n'
    sbf__dqxl += '    delete_table(out_table)\n'
    sbf__dqxl += '    ev_clean.finalize()\n'
    sbf__dqxl += '    return out_data\n'
    ujpzt__vay = {f'out_type{jbp__lixid}': out_var_types[jbp__lixid] for
        jbp__lixid in range(szlbd__hon)}
    ujpzt__vay['out_col_inds'] = MetaType(tuple(eetr__csc))
    ujpzt__vay['in_col_inds'] = MetaType(tuple(juy__yvo))
    ujpzt__vay['cpp_table_to_py_data'] = cpp_table_to_py_data
    ujpzt__vay['py_data_to_cpp_table'] = py_data_to_cpp_table
    ujpzt__vay.update({f'udf_type{jbp__lixid}': t for jbp__lixid, t in
        enumerate(hnh__xehrk)})
    ujpzt__vay['udf_dummy_col_inds'] = MetaType(tuple(range(len(hnh__xehrk))))
    ujpzt__vay['create_dummy_table'] = create_dummy_table
    ujpzt__vay['unknown_cat_out_inds'] = MetaType(tuple(yley__nqqg))
    ujpzt__vay['get_table_data'] = bodo.hiframes.table.get_table_data
    return sbf__dqxl, ujpzt__vay


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    bid__zper = tuple(unwrap_typeref(data_types.types[jbp__lixid]) for
        jbp__lixid in range(len(data_types.types)))
    rmtd__yvrmh = bodo.TableType(bid__zper)
    ujpzt__vay = {'table_type': rmtd__yvrmh}
    sbf__dqxl = 'def impl(data_types):\n'
    sbf__dqxl += '  py_table = init_table(table_type, False)\n'
    sbf__dqxl += '  py_table = set_table_len(py_table, 1)\n'
    for symt__nmo, yqgr__phbjp in rmtd__yvrmh.type_to_blk.items():
        ujpzt__vay[f'typ_list_{yqgr__phbjp}'] = types.List(symt__nmo)
        ujpzt__vay[f'typ_{yqgr__phbjp}'] = symt__nmo
        abage__ocdw = len(rmtd__yvrmh.block_to_arr_ind[yqgr__phbjp])
        sbf__dqxl += f"""  arr_list_{yqgr__phbjp} = alloc_list_like(typ_list_{yqgr__phbjp}, {abage__ocdw}, False)
"""
        sbf__dqxl += f'  for i in range(len(arr_list_{yqgr__phbjp})):\n'
        sbf__dqxl += (
            f'    arr_list_{yqgr__phbjp}[i] = alloc_type(1, typ_{yqgr__phbjp}, (-1,))\n'
            )
        sbf__dqxl += f"""  py_table = set_table_block(py_table, arr_list_{yqgr__phbjp}, {yqgr__phbjp})
"""
    sbf__dqxl += '  return py_table\n'
    ujpzt__vay.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    iwj__ulgj = {}
    exec(sbf__dqxl, ujpzt__vay, iwj__ulgj)
    return iwj__ulgj['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    ontj__eaq = agg_node.in_vars[0].name
    pryp__hudw, hhdmr__hyb, qifak__ggkd = block_use_map[ontj__eaq]
    if hhdmr__hyb or qifak__ggkd:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        avjtx__mxt, mbgwl__elsbr, onfvc__gzv = _compute_table_column_uses(
            agg_node.out_vars[0].name, table_col_use_map, equiv_vars)
        if mbgwl__elsbr or onfvc__gzv:
            avjtx__mxt = set(range(agg_node.n_out_table_arrays))
    else:
        avjtx__mxt = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            avjtx__mxt = {0}
    jvigz__hdcd = set(jbp__lixid for jbp__lixid in agg_node.in_key_inds if 
        jbp__lixid < agg_node.n_in_table_arrays)
    xop__yjbbe = set(agg_node.gb_info_out[jbp__lixid][0] for jbp__lixid in
        avjtx__mxt if jbp__lixid in agg_node.gb_info_out and agg_node.
        gb_info_out[jbp__lixid][0] is not None)
    xop__yjbbe |= jvigz__hdcd | pryp__hudw
    cep__orlz = len(set(range(agg_node.n_in_table_arrays)) - xop__yjbbe) == 0
    block_use_map[ontj__eaq] = xop__yjbbe, cep__orlz, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    twz__qkpi = agg_node.n_out_table_arrays
    flep__teq = agg_node.out_vars[0].name
    yjk__jbu = _find_used_columns(flep__teq, twz__qkpi, column_live_map,
        equiv_vars)
    if yjk__jbu is None:
        return False
    xpjrh__rmlhk = set(range(twz__qkpi)) - yjk__jbu
    ygusu__htj = len(xpjrh__rmlhk - agg_node.dead_out_inds) != 0
    if ygusu__htj:
        agg_node.dead_out_inds.update(xpjrh__rmlhk)
        agg_node.update_dead_col_info()
    return ygusu__htj


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for awv__aynqw in block.body:
            if is_call_assign(awv__aynqw) and find_callname(f_ir,
                awv__aynqw.value) == ('len', 'builtins'
                ) and awv__aynqw.value.args[0].name == f_ir.arg_names[0]:
                jvicj__xrxw = get_definition(f_ir, awv__aynqw.value.func)
                jvicj__xrxw.name = 'dummy_agg_count'
                jvicj__xrxw.value = dummy_agg_count
    jrud__tyoa = get_name_var_table(f_ir.blocks)
    exe__duf = {}
    for name, aydc__siq in jrud__tyoa.items():
        exe__duf[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, exe__duf)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    tbf__ddy = numba.core.compiler.Flags()
    tbf__ddy.nrt = True
    rjo__xtjqr = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, tbf__ddy)
    rjo__xtjqr.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, kvc__yiwel, calltypes, aydc__siq = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    zjca__mvocy = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    vjfh__hcm = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    hodbe__eqr = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    rul__vbq = hodbe__eqr(typemap, calltypes)
    pm = vjfh__hcm(typingctx, targetctx, None, f_ir, typemap, kvc__yiwel,
        calltypes, rul__vbq, {}, tbf__ddy, None)
    dive__txg = numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline(
        pm)
    pm = vjfh__hcm(typingctx, targetctx, None, f_ir, typemap, kvc__yiwel,
        calltypes, rul__vbq, {}, tbf__ddy, dive__txg)
    jnlfm__tvm = numba.core.typed_passes.InlineOverloads()
    jnlfm__tvm.run_pass(pm)
    dux__pdt = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    dux__pdt.run()
    for block in f_ir.blocks.values():
        for awv__aynqw in block.body:
            if is_assign(awv__aynqw) and isinstance(awv__aynqw.value, (ir.
                Arg, ir.Var)) and isinstance(typemap[awv__aynqw.target.name
                ], SeriesType):
                symt__nmo = typemap.pop(awv__aynqw.target.name)
                typemap[awv__aynqw.target.name] = symt__nmo.data
            if is_call_assign(awv__aynqw) and find_callname(f_ir,
                awv__aynqw.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[awv__aynqw.target.name].remove(awv__aynqw
                    .value)
                awv__aynqw.value = awv__aynqw.value.args[0]
                f_ir._definitions[awv__aynqw.target.name].append(awv__aynqw
                    .value)
            if is_call_assign(awv__aynqw) and find_callname(f_ir,
                awv__aynqw.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[awv__aynqw.target.name].remove(awv__aynqw
                    .value)
                awv__aynqw.value = ir.Const(False, awv__aynqw.loc)
                f_ir._definitions[awv__aynqw.target.name].append(awv__aynqw
                    .value)
            if is_call_assign(awv__aynqw) and find_callname(f_ir,
                awv__aynqw.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[awv__aynqw.target.name].remove(awv__aynqw
                    .value)
                awv__aynqw.value = ir.Const(False, awv__aynqw.loc)
                f_ir._definitions[awv__aynqw.target.name].append(awv__aynqw
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    fizx__fneir = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, zjca__mvocy)
    fizx__fneir.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    smz__plp = numba.core.compiler.StateDict()
    smz__plp.func_ir = f_ir
    smz__plp.typemap = typemap
    smz__plp.calltypes = calltypes
    smz__plp.typingctx = typingctx
    smz__plp.targetctx = targetctx
    smz__plp.return_type = kvc__yiwel
    numba.core.rewrites.rewrite_registry.apply('after-inference', smz__plp)
    tbrcn__cum = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        kvc__yiwel, typingctx, targetctx, zjca__mvocy, tbf__ddy, {})
    tbrcn__cum.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            nuphu__fyoc = ctypes.pythonapi.PyCell_Get
            nuphu__fyoc.restype = ctypes.py_object
            nuphu__fyoc.argtypes = ctypes.py_object,
            meyk__hwbmk = tuple(nuphu__fyoc(uabje__swi) for uabje__swi in
                closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            meyk__hwbmk = closure.items
        assert len(code.co_freevars) == len(meyk__hwbmk)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks,
            meyk__hwbmk)


class RegularUDFGenerator:

    def __init__(self, in_col_types, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        qepq__gevzj = SeriesType(in_col_typ.dtype, to_str_arr_if_dict_array
            (in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (qepq__gevzj,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        iffi__fwwsb, arr_var = _rm_arg_agg_block(block, pm.typemap)
        gtzab__dvxmp = -1
        for jbp__lixid, awv__aynqw in enumerate(iffi__fwwsb):
            if isinstance(awv__aynqw, numba.parfors.parfor.Parfor):
                assert gtzab__dvxmp == -1, 'only one parfor for aggregation function'
                gtzab__dvxmp = jbp__lixid
        parfor = None
        if gtzab__dvxmp != -1:
            parfor = iffi__fwwsb[gtzab__dvxmp]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = iffi__fwwsb[:gtzab__dvxmp] + parfor.init_block.body
        eval_nodes = iffi__fwwsb[gtzab__dvxmp + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for awv__aynqw in init_nodes:
            if is_assign(awv__aynqw) and awv__aynqw.target.name in redvars:
                ind = redvars.index(awv__aynqw.target.name)
                reduce_vars[ind] = awv__aynqw.target
        var_types = [pm.typemap[slc__jqx] for slc__jqx in redvars]
        osbik__fjzxz = gen_combine_func(f_ir, parfor, redvars,
            var_to_redvar, var_types, arr_var, pm, self.typingctx, self.
            targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        zqqnd__dzkzf = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        wipx__hljmx = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(wipx__hljmx)
        self.all_update_funcs.append(zqqnd__dzkzf)
        self.all_combine_funcs.append(osbik__fjzxz)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        qvf__phm = gen_init_func(self.all_init_nodes, self.all_reduce_vars,
            self.all_vartypes, self.typingctx, self.targetctx)
        inl__oqa = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        fmcf__bwx = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        kkk__gnspt = gen_all_eval_func(self.all_eval_funcs, self.redvar_offsets
            )
        return self.all_vartypes, qvf__phm, inl__oqa, fmcf__bwx, kkk__gnspt


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, in_col_types, typingctx, targetctx):
    jhce__tylk = []
    for t, gfawd__lyj in zip(in_col_types, agg_func):
        jhce__tylk.append((t, gfawd__lyj))
    hbsm__qqk = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    qskjo__kagl = GeneralUDFGenerator()
    for in_col_typ, func in jhce__tylk:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            hbsm__qqk.add_udf(in_col_typ, func)
        except:
            qskjo__kagl.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = hbsm__qqk.gen_all_func()
    general_udf_funcs = qskjo__kagl.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    lfgl__efnvg = compute_use_defs(parfor.loop_body)
    nnbz__str = set()
    for fpr__bwqhs in lfgl__efnvg.usemap.values():
        nnbz__str |= fpr__bwqhs
    kuq__ywkc = set()
    for fpr__bwqhs in lfgl__efnvg.defmap.values():
        kuq__ywkc |= fpr__bwqhs
    hpg__ubvs = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    hpg__ubvs.body = eval_nodes
    pvasz__yzaha = compute_use_defs({(0): hpg__ubvs})
    uja__lmcof = pvasz__yzaha.usemap[0]
    hdipm__gpd = set()
    mpej__dmof = []
    eny__ozh = []
    for awv__aynqw in reversed(init_nodes):
        qotzc__ndqnq = {slc__jqx.name for slc__jqx in awv__aynqw.list_vars()}
        if is_assign(awv__aynqw):
            slc__jqx = awv__aynqw.target.name
            qotzc__ndqnq.remove(slc__jqx)
            if (slc__jqx in nnbz__str and slc__jqx not in hdipm__gpd and 
                slc__jqx not in uja__lmcof and slc__jqx not in kuq__ywkc):
                eny__ozh.append(awv__aynqw)
                nnbz__str |= qotzc__ndqnq
                kuq__ywkc.add(slc__jqx)
                continue
        hdipm__gpd |= qotzc__ndqnq
        mpej__dmof.append(awv__aynqw)
    eny__ozh.reverse()
    mpej__dmof.reverse()
    rwnvj__ndm = min(parfor.loop_body.keys())
    vtpyf__hzjpy = parfor.loop_body[rwnvj__ndm]
    vtpyf__hzjpy.body = eny__ozh + vtpyf__hzjpy.body
    return mpej__dmof


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    gwwte__xzc = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    lsnpb__gvih = set()
    oyhrx__isoht = []
    for awv__aynqw in init_nodes:
        if is_assign(awv__aynqw) and isinstance(awv__aynqw.value, ir.Global
            ) and isinstance(awv__aynqw.value.value, pytypes.FunctionType
            ) and awv__aynqw.value.value in gwwte__xzc:
            lsnpb__gvih.add(awv__aynqw.target.name)
        elif is_call_assign(awv__aynqw
            ) and awv__aynqw.value.func.name in lsnpb__gvih:
            pass
        else:
            oyhrx__isoht.append(awv__aynqw)
    init_nodes = oyhrx__isoht
    pfgg__yrzz = types.Tuple(var_types)
    sefb__oprsn = lambda : None
    f_ir = compile_to_numba_ir(sefb__oprsn, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    qxvk__wfaox = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    mqgql__bpc = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        qxvk__wfaox, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [mqgql__bpc] + block.body
    block.body[-2].value.value = qxvk__wfaox
    tsci__wnm = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        pfgg__yrzz, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vqmff__koaox = numba.core.target_extension.dispatcher_registry[cpu_target](
        sefb__oprsn)
    vqmff__koaox.add_overload(tsci__wnm)
    return vqmff__koaox


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    oxw__gskkv = len(update_funcs)
    ixmz__ggt = len(in_col_types)
    sbf__dqxl = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for dzt__gywy in range(oxw__gskkv):
        qdwhk__nxjm = ', '.join(['redvar_arrs[{}][w_ind]'.format(jbp__lixid
            ) for jbp__lixid in range(redvar_offsets[dzt__gywy],
            redvar_offsets[dzt__gywy + 1])])
        if qdwhk__nxjm:
            sbf__dqxl += '  {} = update_vars_{}({},  data_in[{}][i])\n'.format(
                qdwhk__nxjm, dzt__gywy, qdwhk__nxjm, 0 if ixmz__ggt == 1 else
                dzt__gywy)
    sbf__dqxl += '  return\n'
    izbo__utjbz = {}
    for jbp__lixid, gfawd__lyj in enumerate(update_funcs):
        izbo__utjbz['update_vars_{}'.format(jbp__lixid)] = gfawd__lyj
    iwj__ulgj = {}
    exec(sbf__dqxl, izbo__utjbz, iwj__ulgj)
    xtmns__lha = iwj__ulgj['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(xtmns__lha)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    cjvp__dmqk = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = cjvp__dmqk, cjvp__dmqk, types.intp, types.intp
    aqrgt__tpjl = len(redvar_offsets) - 1
    sbf__dqxl = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for dzt__gywy in range(aqrgt__tpjl):
        qdwhk__nxjm = ', '.join(['redvar_arrs[{}][w_ind]'.format(jbp__lixid
            ) for jbp__lixid in range(redvar_offsets[dzt__gywy],
            redvar_offsets[dzt__gywy + 1])])
        kyvfw__foec = ', '.join(['recv_arrs[{}][i]'.format(jbp__lixid) for
            jbp__lixid in range(redvar_offsets[dzt__gywy], redvar_offsets[
            dzt__gywy + 1])])
        if kyvfw__foec:
            sbf__dqxl += '  {} = combine_vars_{}({}, {})\n'.format(qdwhk__nxjm,
                dzt__gywy, qdwhk__nxjm, kyvfw__foec)
    sbf__dqxl += '  return\n'
    izbo__utjbz = {}
    for jbp__lixid, gfawd__lyj in enumerate(combine_funcs):
        izbo__utjbz['combine_vars_{}'.format(jbp__lixid)] = gfawd__lyj
    iwj__ulgj = {}
    exec(sbf__dqxl, izbo__utjbz, iwj__ulgj)
    agst__tccku = iwj__ulgj['combine_all_f']
    f_ir = compile_to_numba_ir(agst__tccku, izbo__utjbz)
    fmcf__bwx = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vqmff__koaox = numba.core.target_extension.dispatcher_registry[cpu_target](
        agst__tccku)
    vqmff__koaox.add_overload(fmcf__bwx)
    return vqmff__koaox


def gen_all_eval_func(eval_funcs, redvar_offsets):
    aqrgt__tpjl = len(redvar_offsets) - 1
    sbf__dqxl = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for dzt__gywy in range(aqrgt__tpjl):
        qdwhk__nxjm = ', '.join(['redvar_arrs[{}][j]'.format(jbp__lixid) for
            jbp__lixid in range(redvar_offsets[dzt__gywy], redvar_offsets[
            dzt__gywy + 1])])
        sbf__dqxl += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(dzt__gywy,
            dzt__gywy, qdwhk__nxjm)
    sbf__dqxl += '  return\n'
    izbo__utjbz = {}
    for jbp__lixid, gfawd__lyj in enumerate(eval_funcs):
        izbo__utjbz['eval_vars_{}'.format(jbp__lixid)] = gfawd__lyj
    iwj__ulgj = {}
    exec(sbf__dqxl, izbo__utjbz, iwj__ulgj)
    oigzj__wrob = iwj__ulgj['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(oigzj__wrob)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    gly__jqlga = len(var_types)
    ecxem__lmc = [f'in{jbp__lixid}' for jbp__lixid in range(gly__jqlga)]
    pfgg__yrzz = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    bre__zhmfc = pfgg__yrzz(0)
    sbf__dqxl = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        ecxem__lmc))
    iwj__ulgj = {}
    exec(sbf__dqxl, {'_zero': bre__zhmfc}, iwj__ulgj)
    xcs__kzod = iwj__ulgj['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(xcs__kzod, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': bre__zhmfc}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    insbu__wpni = []
    for jbp__lixid, slc__jqx in enumerate(reduce_vars):
        insbu__wpni.append(ir.Assign(block.body[jbp__lixid].target,
            slc__jqx, slc__jqx.loc))
        for rywx__urrf in slc__jqx.versioned_names:
            insbu__wpni.append(ir.Assign(slc__jqx, ir.Var(slc__jqx.scope,
                rywx__urrf, slc__jqx.loc), slc__jqx.loc))
    block.body = block.body[:gly__jqlga] + insbu__wpni + eval_nodes
    wipx__hljmx = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        pfgg__yrzz, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vqmff__koaox = numba.core.target_extension.dispatcher_registry[cpu_target](
        xcs__kzod)
    vqmff__koaox.add_overload(wipx__hljmx)
    return vqmff__koaox


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    gly__jqlga = len(redvars)
    gic__hvqzp = [f'v{jbp__lixid}' for jbp__lixid in range(gly__jqlga)]
    ecxem__lmc = [f'in{jbp__lixid}' for jbp__lixid in range(gly__jqlga)]
    sbf__dqxl = 'def agg_combine({}):\n'.format(', '.join(gic__hvqzp +
        ecxem__lmc))
    zdgkt__xwwuu = wrap_parfor_blocks(parfor)
    gow__twjen = find_topo_order(zdgkt__xwwuu)
    gow__twjen = gow__twjen[1:]
    unwrap_parfor_blocks(parfor)
    hxqd__kcio = {}
    wxc__sokx = []
    for cisv__zzuzf in gow__twjen:
        ksm__nsgcg = parfor.loop_body[cisv__zzuzf]
        for awv__aynqw in ksm__nsgcg.body:
            if is_assign(awv__aynqw) and awv__aynqw.target.name in redvars:
                wsy__qfqpg = awv__aynqw.target.name
                ind = redvars.index(wsy__qfqpg)
                if ind in wxc__sokx:
                    continue
                if len(f_ir._definitions[wsy__qfqpg]) == 2:
                    var_def = f_ir._definitions[wsy__qfqpg][0]
                    sbf__dqxl += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[wsy__qfqpg][1]
                    sbf__dqxl += _match_reduce_def(var_def, f_ir, ind)
    sbf__dqxl += '    return {}'.format(', '.join(['v{}'.format(jbp__lixid) for
        jbp__lixid in range(gly__jqlga)]))
    iwj__ulgj = {}
    exec(sbf__dqxl, {}, iwj__ulgj)
    wvr__rdgs = iwj__ulgj['agg_combine']
    arg_typs = tuple(2 * var_types)
    izbo__utjbz = {'numba': numba, 'bodo': bodo, 'np': np}
    izbo__utjbz.update(hxqd__kcio)
    f_ir = compile_to_numba_ir(wvr__rdgs, izbo__utjbz, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    pfgg__yrzz = pm.typemap[block.body[-1].value.name]
    osbik__fjzxz = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        pfgg__yrzz, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vqmff__koaox = numba.core.target_extension.dispatcher_registry[cpu_target](
        wvr__rdgs)
    vqmff__koaox.add_overload(osbik__fjzxz)
    return vqmff__koaox


def _match_reduce_def(var_def, f_ir, ind):
    sbf__dqxl = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        sbf__dqxl = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        ejbm__zhz = guard(find_callname, f_ir, var_def)
        if ejbm__zhz == ('min', 'builtins'):
            sbf__dqxl = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if ejbm__zhz == ('max', 'builtins'):
            sbf__dqxl = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return sbf__dqxl


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    gly__jqlga = len(redvars)
    zhw__yodni = 1
    in_vars = []
    for jbp__lixid in range(zhw__yodni):
        rvmxt__gmmja = ir.Var(arr_var.scope, f'$input{jbp__lixid}', arr_var.loc
            )
        in_vars.append(rvmxt__gmmja)
    ubbzp__miunj = parfor.loop_nests[0].index_variable
    wspd__chtav = [0] * gly__jqlga
    for ksm__nsgcg in parfor.loop_body.values():
        jfv__xtzc = []
        for awv__aynqw in ksm__nsgcg.body:
            if is_var_assign(awv__aynqw
                ) and awv__aynqw.value.name == ubbzp__miunj.name:
                continue
            if is_getitem(awv__aynqw
                ) and awv__aynqw.value.value.name == arr_var.name:
                awv__aynqw.value = in_vars[0]
            if is_call_assign(awv__aynqw) and guard(find_callname, pm.
                func_ir, awv__aynqw.value) == ('isna',
                'bodo.libs.array_kernels') and awv__aynqw.value.args[0
                ].name == arr_var.name:
                awv__aynqw.value = ir.Const(False, awv__aynqw.target.loc)
            if is_assign(awv__aynqw) and awv__aynqw.target.name in redvars:
                ind = redvars.index(awv__aynqw.target.name)
                wspd__chtav[ind] = awv__aynqw.target
            jfv__xtzc.append(awv__aynqw)
        ksm__nsgcg.body = jfv__xtzc
    gic__hvqzp = ['v{}'.format(jbp__lixid) for jbp__lixid in range(gly__jqlga)]
    ecxem__lmc = ['in{}'.format(jbp__lixid) for jbp__lixid in range(zhw__yodni)
        ]
    sbf__dqxl = 'def agg_update({}):\n'.format(', '.join(gic__hvqzp +
        ecxem__lmc))
    sbf__dqxl += '    __update_redvars()\n'
    sbf__dqxl += '    return {}'.format(', '.join(['v{}'.format(jbp__lixid) for
        jbp__lixid in range(gly__jqlga)]))
    iwj__ulgj = {}
    exec(sbf__dqxl, {}, iwj__ulgj)
    yhgpd__seoc = iwj__ulgj['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * zhw__yodni)
    f_ir = compile_to_numba_ir(yhgpd__seoc, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    nhwvo__niq = f_ir.blocks.popitem()[1].body
    pfgg__yrzz = pm.typemap[nhwvo__niq[-1].value.name]
    zdgkt__xwwuu = wrap_parfor_blocks(parfor)
    gow__twjen = find_topo_order(zdgkt__xwwuu)
    gow__twjen = gow__twjen[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    vtpyf__hzjpy = f_ir.blocks[gow__twjen[0]]
    vudrh__wglj = f_ir.blocks[gow__twjen[-1]]
    lkatb__nyaa = nhwvo__niq[:gly__jqlga + zhw__yodni]
    if gly__jqlga > 1:
        ijnxd__zqilb = nhwvo__niq[-3:]
        assert is_assign(ijnxd__zqilb[0]) and isinstance(ijnxd__zqilb[0].
            value, ir.Expr) and ijnxd__zqilb[0].value.op == 'build_tuple'
    else:
        ijnxd__zqilb = nhwvo__niq[-2:]
    for jbp__lixid in range(gly__jqlga):
        lwwt__igdnq = nhwvo__niq[jbp__lixid].target
        ildpx__dhyd = ir.Assign(lwwt__igdnq, wspd__chtav[jbp__lixid],
            lwwt__igdnq.loc)
        lkatb__nyaa.append(ildpx__dhyd)
    for jbp__lixid in range(gly__jqlga, gly__jqlga + zhw__yodni):
        lwwt__igdnq = nhwvo__niq[jbp__lixid].target
        ildpx__dhyd = ir.Assign(lwwt__igdnq, in_vars[jbp__lixid -
            gly__jqlga], lwwt__igdnq.loc)
        lkatb__nyaa.append(ildpx__dhyd)
    vtpyf__hzjpy.body = lkatb__nyaa + vtpyf__hzjpy.body
    uii__ywyp = []
    for jbp__lixid in range(gly__jqlga):
        lwwt__igdnq = nhwvo__niq[jbp__lixid].target
        ildpx__dhyd = ir.Assign(wspd__chtav[jbp__lixid], lwwt__igdnq,
            lwwt__igdnq.loc)
        uii__ywyp.append(ildpx__dhyd)
    vudrh__wglj.body += uii__ywyp + ijnxd__zqilb
    jrwgi__cvib = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        pfgg__yrzz, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vqmff__koaox = numba.core.target_extension.dispatcher_registry[cpu_target](
        yhgpd__seoc)
    vqmff__koaox.add_overload(jrwgi__cvib)
    return vqmff__koaox


def _rm_arg_agg_block(block, typemap):
    iffi__fwwsb = []
    arr_var = None
    for jbp__lixid, awv__aynqw in enumerate(block.body):
        if is_assign(awv__aynqw) and isinstance(awv__aynqw.value, ir.Arg):
            arr_var = awv__aynqw.target
            ekwt__vrp = typemap[arr_var.name]
            if not isinstance(ekwt__vrp, types.ArrayCompatible):
                iffi__fwwsb += block.body[jbp__lixid + 1:]
                break
            ppr__jvzg = block.body[jbp__lixid + 1]
            assert is_assign(ppr__jvzg) and isinstance(ppr__jvzg.value, ir.Expr
                ) and ppr__jvzg.value.op == 'getattr' and ppr__jvzg.value.attr == 'shape' and ppr__jvzg.value.value.name == arr_var.name
            qnygt__twha = ppr__jvzg.target
            xytd__qqn = block.body[jbp__lixid + 2]
            assert is_assign(xytd__qqn) and isinstance(xytd__qqn.value, ir.Expr
                ) and xytd__qqn.value.op == 'static_getitem' and xytd__qqn.value.value.name == qnygt__twha.name
            iffi__fwwsb += block.body[jbp__lixid + 3:]
            break
        iffi__fwwsb.append(awv__aynqw)
    return iffi__fwwsb, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    zdgkt__xwwuu = wrap_parfor_blocks(parfor)
    gow__twjen = find_topo_order(zdgkt__xwwuu)
    gow__twjen = gow__twjen[1:]
    unwrap_parfor_blocks(parfor)
    for cisv__zzuzf in reversed(gow__twjen):
        for awv__aynqw in reversed(parfor.loop_body[cisv__zzuzf].body):
            if isinstance(awv__aynqw, ir.Assign) and (awv__aynqw.target.
                name in parfor_params or awv__aynqw.target.name in var_to_param
                ):
                ybe__ztte = awv__aynqw.target.name
                rhs = awv__aynqw.value
                bribs__yfng = (ybe__ztte if ybe__ztte in parfor_params else
                    var_to_param[ybe__ztte])
                xacj__hhn = []
                if isinstance(rhs, ir.Var):
                    xacj__hhn = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    xacj__hhn = [slc__jqx.name for slc__jqx in awv__aynqw.
                        value.list_vars()]
                param_uses[bribs__yfng].extend(xacj__hhn)
                for slc__jqx in xacj__hhn:
                    var_to_param[slc__jqx] = bribs__yfng
            if isinstance(awv__aynqw, Parfor):
                get_parfor_reductions(awv__aynqw, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for njgcy__imgz, xacj__hhn in param_uses.items():
        if njgcy__imgz in xacj__hhn and njgcy__imgz not in reduce_varnames:
            reduce_varnames.append(njgcy__imgz)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
