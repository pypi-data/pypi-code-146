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
        tjsn__vbvry = func.signature
        if tjsn__vbvry == types.none(types.voidptr):
            pmxep__ozmoh = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer()])
            tuht__lfhqw = cgutils.get_or_insert_function(builder.module,
                pmxep__ozmoh, sym._literal_value)
            builder.call(tuht__lfhqw, [context.get_constant_null(
                tjsn__vbvry.args[0])])
        elif tjsn__vbvry == types.none(types.int64, types.voidptr, types.
            voidptr):
            pmxep__ozmoh = lir.FunctionType(lir.VoidType(), [lir.IntType(64
                ), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            tuht__lfhqw = cgutils.get_or_insert_function(builder.module,
                pmxep__ozmoh, sym._literal_value)
            builder.call(tuht__lfhqw, [context.get_constant(types.int64, 0),
                context.get_constant_null(tjsn__vbvry.args[1]), context.
                get_constant_null(tjsn__vbvry.args[2])])
        else:
            pmxep__ozmoh = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)
                .as_pointer()])
            tuht__lfhqw = cgutils.get_or_insert_function(builder.module,
                pmxep__ozmoh, sym._literal_value)
            builder.call(tuht__lfhqw, [context.get_constant_null(
                tjsn__vbvry.args[0]), context.get_constant_null(tjsn__vbvry
                .args[1]), context.get_constant_null(tjsn__vbvry.args[2])])
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
        tmzts__dyl = True
        lkbou__kbjo = 1
        eou__zuoq = -1
        if isinstance(rhs, ir.Expr):
            for xcp__ngo in rhs.kws:
                if func_name in list_cumulative:
                    if xcp__ngo[0] == 'skipna':
                        tmzts__dyl = guard(find_const, func_ir, xcp__ngo[1])
                        if not isinstance(tmzts__dyl, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if xcp__ngo[0] == 'dropna':
                        tmzts__dyl = guard(find_const, func_ir, xcp__ngo[1])
                        if not isinstance(tmzts__dyl, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            lkbou__kbjo = get_call_expr_arg('shift', rhs.args, dict(rhs.kws
                ), 0, 'periods', lkbou__kbjo)
            lkbou__kbjo = guard(find_const, func_ir, lkbou__kbjo)
        if func_name == 'head':
            eou__zuoq = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 
                0, 'n', 5)
            if not isinstance(eou__zuoq, int):
                eou__zuoq = guard(find_const, func_ir, eou__zuoq)
            if eou__zuoq < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = tmzts__dyl
        func.periods = lkbou__kbjo
        func.head_n = eou__zuoq
        if func_name == 'transform':
            kws = dict(rhs.kws)
            skje__zhj = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            fcog__fbn = typemap[skje__zhj.name]
            isf__fqky = None
            if isinstance(fcog__fbn, str):
                isf__fqky = fcog__fbn
            elif is_overload_constant_str(fcog__fbn):
                isf__fqky = get_overload_const_str(fcog__fbn)
            elif bodo.utils.typing.is_builtin_function(fcog__fbn):
                isf__fqky = bodo.utils.typing.get_builtin_function_name(
                    fcog__fbn)
            if isf__fqky not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {isf__fqky}')
            func.transform_func = supported_agg_funcs.index(isf__fqky)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    skje__zhj = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if skje__zhj == '':
        fcog__fbn = types.none
    else:
        fcog__fbn = typemap[skje__zhj.name]
    if is_overload_constant_dict(fcog__fbn):
        xsk__ejzcw = get_overload_constant_dict(fcog__fbn)
        oiy__qtzo = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in xsk__ejzcw.values()]
        return oiy__qtzo
    if fcog__fbn == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(fcog__fbn, types.BaseTuple) or is_overload_constant_list(
        fcog__fbn):
        oiy__qtzo = []
        jhne__nbwzw = 0
        if is_overload_constant_list(fcog__fbn):
            xhdy__izql = get_overload_const_list(fcog__fbn)
        else:
            xhdy__izql = fcog__fbn.types
        for t in xhdy__izql:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                oiy__qtzo.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(xhdy__izql) > 1:
                    func.fname = '<lambda_' + str(jhne__nbwzw) + '>'
                    jhne__nbwzw += 1
                oiy__qtzo.append(func)
        return [oiy__qtzo]
    if is_overload_constant_str(fcog__fbn):
        func_name = get_overload_const_str(fcog__fbn)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(fcog__fbn):
        func_name = bodo.utils.typing.get_builtin_function_name(fcog__fbn)
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
        jhne__nbwzw = 0
        ivd__nav = []
        for qmam__wfsqf in f_val:
            func = get_agg_func_udf(func_ir, qmam__wfsqf, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{jhne__nbwzw}>'
                jhne__nbwzw += 1
            ivd__nav.append(func)
        return ivd__nav
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
    isf__fqky = code.co_name
    return isf__fqky


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
            app__nlpzl = types.DType(args[0])
            return signature(app__nlpzl, *args)


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
        return [pdnwz__zuit for pdnwz__zuit in self.in_vars if pdnwz__zuit
             is not None]

    def get_live_out_vars(self):
        return [pdnwz__zuit for pdnwz__zuit in self.out_vars if pdnwz__zuit
             is not None]

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
        oysz__ifvjf = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        xvkzc__taw = list(get_index_data_arr_types(self.out_type.index))
        return oysz__ifvjf + xvkzc__taw

    def update_dead_col_info(self):
        for zjj__grd in self.dead_out_inds:
            self.gb_info_out.pop(zjj__grd, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for ncbz__qcvwu, lop__noiy in self.gb_info_in.copy().items():
            mzh__sknz = []
            for qmam__wfsqf, emnba__dkdb in lop__noiy:
                if emnba__dkdb not in self.dead_out_inds:
                    mzh__sknz.append((qmam__wfsqf, emnba__dkdb))
            if not mzh__sknz:
                if (ncbz__qcvwu is not None and ncbz__qcvwu not in self.
                    in_key_inds):
                    self.dead_in_inds.add(ncbz__qcvwu)
                self.gb_info_in.pop(ncbz__qcvwu)
            else:
                self.gb_info_in[ncbz__qcvwu] = mzh__sknz
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for jjcpf__upk in range(1, len(self.in_vars)):
                zjj__grd = self.n_in_table_arrays + jjcpf__upk - 1
                if zjj__grd in self.dead_in_inds:
                    self.in_vars[jjcpf__upk] = None
        else:
            for jjcpf__upk in range(len(self.in_vars)):
                if jjcpf__upk in self.dead_in_inds:
                    self.in_vars[jjcpf__upk] = None

    def __repr__(self):
        efu__ettp = ', '.join(pdnwz__zuit.name for pdnwz__zuit in self.
            get_live_in_vars())
        djaqc__vklbb = f'{self.df_in}{{{efu__ettp}}}'
        hyey__rptv = ', '.join(pdnwz__zuit.name for pdnwz__zuit in self.
            get_live_out_vars())
        elm__cdoc = f'{self.df_out}{{{hyey__rptv}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {djaqc__vklbb} {elm__cdoc}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({pdnwz__zuit.name for pdnwz__zuit in aggregate_node.
        get_live_in_vars()})
    def_set.update({pdnwz__zuit.name for pdnwz__zuit in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    eiwg__acnw = agg_node.out_vars[0]
    if eiwg__acnw is not None and eiwg__acnw.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            lvjry__ttu = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(lvjry__ttu)
        else:
            agg_node.dead_out_inds.add(0)
    for jjcpf__upk in range(1, len(agg_node.out_vars)):
        pdnwz__zuit = agg_node.out_vars[jjcpf__upk]
        if pdnwz__zuit is not None and pdnwz__zuit.name not in lives:
            agg_node.out_vars[jjcpf__upk] = None
            zjj__grd = agg_node.n_out_table_arrays + jjcpf__upk - 1
            agg_node.dead_out_inds.add(zjj__grd)
    if all(pdnwz__zuit is None for pdnwz__zuit in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    ydkc__jbva = {pdnwz__zuit.name for pdnwz__zuit in aggregate_node.
        get_live_out_vars()}
    return set(), ydkc__jbva


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for jjcpf__upk in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[jjcpf__upk] is not None:
            aggregate_node.in_vars[jjcpf__upk] = replace_vars_inner(
                aggregate_node.in_vars[jjcpf__upk], var_dict)
    for jjcpf__upk in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[jjcpf__upk] is not None:
            aggregate_node.out_vars[jjcpf__upk] = replace_vars_inner(
                aggregate_node.out_vars[jjcpf__upk], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for jjcpf__upk in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[jjcpf__upk] is not None:
            aggregate_node.in_vars[jjcpf__upk] = visit_vars_inner(
                aggregate_node.in_vars[jjcpf__upk], callback, cbdata)
    for jjcpf__upk in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[jjcpf__upk] is not None:
            aggregate_node.out_vars[jjcpf__upk] = visit_vars_inner(
                aggregate_node.out_vars[jjcpf__upk], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    opggk__vrd = []
    for qxti__uwp in aggregate_node.get_live_in_vars():
        ytge__qckh = equiv_set.get_shape(qxti__uwp)
        if ytge__qckh is not None:
            opggk__vrd.append(ytge__qckh[0])
    if len(opggk__vrd) > 1:
        equiv_set.insert_equiv(*opggk__vrd)
    ibd__xgo = []
    opggk__vrd = []
    for qxti__uwp in aggregate_node.get_live_out_vars():
        qrur__kwtu = typemap[qxti__uwp.name]
        qom__yavkp = array_analysis._gen_shape_call(equiv_set, qxti__uwp,
            qrur__kwtu.ndim, None, ibd__xgo)
        equiv_set.insert_equiv(qxti__uwp, qom__yavkp)
        opggk__vrd.append(qom__yavkp[0])
        equiv_set.define(qxti__uwp, set())
    if len(opggk__vrd) > 1:
        equiv_set.insert_equiv(*opggk__vrd)
    return [], ibd__xgo


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    fgwa__msvcc = aggregate_node.get_live_in_vars()
    hkv__cgn = aggregate_node.get_live_out_vars()
    jeoso__qihc = Distribution.OneD
    for qxti__uwp in fgwa__msvcc:
        jeoso__qihc = Distribution(min(jeoso__qihc.value, array_dists[
            qxti__uwp.name].value))
    dhwla__luofh = Distribution(min(jeoso__qihc.value, Distribution.
        OneD_Var.value))
    for qxti__uwp in hkv__cgn:
        if qxti__uwp.name in array_dists:
            dhwla__luofh = Distribution(min(dhwla__luofh.value, array_dists
                [qxti__uwp.name].value))
    if dhwla__luofh != Distribution.OneD_Var:
        jeoso__qihc = dhwla__luofh
    for qxti__uwp in fgwa__msvcc:
        array_dists[qxti__uwp.name] = jeoso__qihc
    for qxti__uwp in hkv__cgn:
        array_dists[qxti__uwp.name] = dhwla__luofh


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for qxti__uwp in agg_node.get_live_out_vars():
        definitions[qxti__uwp.name].append(agg_node)
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
    lkwl__ixy = agg_node.get_live_in_vars()
    vmdp__vsyk = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for pdnwz__zuit in (lkwl__ixy + vmdp__vsyk):
            if array_dists[pdnwz__zuit.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                pdnwz__zuit.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    oiy__qtzo = []
    func_out_types = []
    for emnba__dkdb, (ncbz__qcvwu, func) in agg_node.gb_info_out.items():
        if ncbz__qcvwu is not None:
            t = agg_node.in_col_types[ncbz__qcvwu]
            in_col_typs.append(t)
        oiy__qtzo.append(func)
        func_out_types.append(out_col_typs[emnba__dkdb])
    nrx__efvq = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for jjcpf__upk, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            nrx__efvq.update({f'in_cat_dtype_{jjcpf__upk}': in_col_typ})
    for jjcpf__upk, ppf__rtee in enumerate(out_col_typs):
        if isinstance(ppf__rtee, bodo.CategoricalArrayType):
            nrx__efvq.update({f'out_cat_dtype_{jjcpf__upk}': ppf__rtee})
    udf_func_struct = get_udf_func_struct(oiy__qtzo, in_col_typs, typingctx,
        targetctx)
    out_var_types = [(typemap[pdnwz__zuit.name] if pdnwz__zuit is not None else
        types.none) for pdnwz__zuit in agg_node.out_vars]
    dfar__yei, uhyz__haqao = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, func_out_types, parallel, udf_func_struct,
        out_var_types, typemap)
    nrx__efvq.update(uhyz__haqao)
    nrx__efvq.update({'pd': pd, 'pre_alloc_string_array':
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
            nrx__efvq.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            nrx__efvq.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    eov__evkea = {}
    exec(dfar__yei, {}, eov__evkea)
    npkv__cifju = eov__evkea['agg_top']
    nwino__yap = compile_to_numba_ir(npkv__cifju, nrx__efvq, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[pdnwz__zuit.
        name] for pdnwz__zuit in lkwl__ixy), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(nwino__yap, lkwl__ixy)
    ied__lbzxq = nwino__yap.body[-2].value.value
    vboi__txm = nwino__yap.body[:-2]
    for jjcpf__upk, pdnwz__zuit in enumerate(vmdp__vsyk):
        gen_getitem(pdnwz__zuit, ied__lbzxq, jjcpf__upk, calltypes, vboi__txm)
    return vboi__txm


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        ipw__bfol = IntDtype(t.dtype).name
        assert ipw__bfol.endswith('Dtype()')
        ipw__bfol = ipw__bfol[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{ipw__bfol}'))"
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
        gzuzr__trbzo = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {gzuzr__trbzo}_cat_dtype_{colnum})'
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
    czaz__ldwye = udf_func_struct.var_typs
    gob__fzon = len(czaz__ldwye)
    dfar__yei = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    dfar__yei += '    if is_null_pointer(in_table):\n'
    dfar__yei += '        return\n'
    dfar__yei += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in czaz__ldwye]), 
        ',' if len(czaz__ldwye) == 1 else '')
    cltu__gzb = n_keys
    bavfl__ulhd = []
    redvar_offsets = []
    kri__usf = []
    if do_combine:
        for jjcpf__upk, qmam__wfsqf in enumerate(allfuncs):
            if qmam__wfsqf.ftype != 'udf':
                cltu__gzb += qmam__wfsqf.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(cltu__gzb, cltu__gzb +
                    qmam__wfsqf.n_redvars))
                cltu__gzb += qmam__wfsqf.n_redvars
                kri__usf.append(data_in_typs_[func_idx_to_in_col[jjcpf__upk]])
                bavfl__ulhd.append(func_idx_to_in_col[jjcpf__upk] + n_keys)
    else:
        for jjcpf__upk, qmam__wfsqf in enumerate(allfuncs):
            if qmam__wfsqf.ftype != 'udf':
                cltu__gzb += qmam__wfsqf.ncols_post_shuffle
            else:
                redvar_offsets += list(range(cltu__gzb + 1, cltu__gzb + 1 +
                    qmam__wfsqf.n_redvars))
                cltu__gzb += qmam__wfsqf.n_redvars + 1
                kri__usf.append(data_in_typs_[func_idx_to_in_col[jjcpf__upk]])
                bavfl__ulhd.append(func_idx_to_in_col[jjcpf__upk] + n_keys)
    assert len(redvar_offsets) == gob__fzon
    qns__kkkml = len(kri__usf)
    zdu__biej = []
    for jjcpf__upk, t in enumerate(kri__usf):
        zdu__biej.append(_gen_dummy_alloc(t, jjcpf__upk, True))
    dfar__yei += '    data_in_dummy = ({}{})\n'.format(','.join(zdu__biej),
        ',' if len(kri__usf) == 1 else '')
    dfar__yei += """
    # initialize redvar cols
"""
    dfar__yei += '    init_vals = __init_func()\n'
    for jjcpf__upk in range(gob__fzon):
        dfar__yei += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(jjcpf__upk, redvar_offsets[jjcpf__upk], jjcpf__upk))
        dfar__yei += '    incref(redvar_arr_{})\n'.format(jjcpf__upk)
        dfar__yei += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            jjcpf__upk, jjcpf__upk)
    dfar__yei += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(jjcpf__upk) for jjcpf__upk in range(gob__fzon)]), ',' if 
        gob__fzon == 1 else '')
    dfar__yei += '\n'
    for jjcpf__upk in range(qns__kkkml):
        dfar__yei += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(jjcpf__upk, bavfl__ulhd[jjcpf__upk], jjcpf__upk))
        dfar__yei += '    incref(data_in_{})\n'.format(jjcpf__upk)
    dfar__yei += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(jjcpf__upk) for jjcpf__upk in range(qns__kkkml)]), ',' if 
        qns__kkkml == 1 else '')
    dfar__yei += '\n'
    dfar__yei += '    for i in range(len(data_in_0)):\n'
    dfar__yei += '        w_ind = row_to_group[i]\n'
    dfar__yei += '        if w_ind != -1:\n'
    dfar__yei += '            __update_redvars(redvars, data_in, w_ind, i)\n'
    eov__evkea = {}
    exec(dfar__yei, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, eov__evkea)
    return eov__evkea['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    czaz__ldwye = udf_func_struct.var_typs
    gob__fzon = len(czaz__ldwye)
    dfar__yei = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    dfar__yei += '    if is_null_pointer(in_table):\n'
    dfar__yei += '        return\n'
    dfar__yei += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in czaz__ldwye]), 
        ',' if len(czaz__ldwye) == 1 else '')
    haq__tttr = n_keys
    vfn__qzoa = n_keys
    lkuby__ofaa = []
    xyige__fpko = []
    for qmam__wfsqf in allfuncs:
        if qmam__wfsqf.ftype != 'udf':
            haq__tttr += qmam__wfsqf.ncols_pre_shuffle
            vfn__qzoa += qmam__wfsqf.ncols_post_shuffle
        else:
            lkuby__ofaa += list(range(haq__tttr, haq__tttr + qmam__wfsqf.
                n_redvars))
            xyige__fpko += list(range(vfn__qzoa + 1, vfn__qzoa + 1 +
                qmam__wfsqf.n_redvars))
            haq__tttr += qmam__wfsqf.n_redvars
            vfn__qzoa += 1 + qmam__wfsqf.n_redvars
    assert len(lkuby__ofaa) == gob__fzon
    dfar__yei += """
    # initialize redvar cols
"""
    dfar__yei += '    init_vals = __init_func()\n'
    for jjcpf__upk in range(gob__fzon):
        dfar__yei += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(jjcpf__upk, xyige__fpko[jjcpf__upk], jjcpf__upk))
        dfar__yei += '    incref(redvar_arr_{})\n'.format(jjcpf__upk)
        dfar__yei += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            jjcpf__upk, jjcpf__upk)
    dfar__yei += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(jjcpf__upk) for jjcpf__upk in range(gob__fzon)]), ',' if 
        gob__fzon == 1 else '')
    dfar__yei += '\n'
    for jjcpf__upk in range(gob__fzon):
        dfar__yei += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(jjcpf__upk, lkuby__ofaa[jjcpf__upk], jjcpf__upk))
        dfar__yei += '    incref(recv_redvar_arr_{})\n'.format(jjcpf__upk)
    dfar__yei += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(jjcpf__upk) for jjcpf__upk in range(
        gob__fzon)]), ',' if gob__fzon == 1 else '')
    dfar__yei += '\n'
    if gob__fzon:
        dfar__yei += '    for i in range(len(recv_redvar_arr_0)):\n'
        dfar__yei += '        w_ind = row_to_group[i]\n'
        dfar__yei += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    eov__evkea = {}
    exec(dfar__yei, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, eov__evkea)
    return eov__evkea['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    czaz__ldwye = udf_func_struct.var_typs
    gob__fzon = len(czaz__ldwye)
    cltu__gzb = n_keys
    redvar_offsets = []
    jgn__mnw = []
    tev__pikye = []
    for jjcpf__upk, qmam__wfsqf in enumerate(allfuncs):
        if qmam__wfsqf.ftype != 'udf':
            cltu__gzb += qmam__wfsqf.ncols_post_shuffle
        else:
            jgn__mnw.append(cltu__gzb)
            redvar_offsets += list(range(cltu__gzb + 1, cltu__gzb + 1 +
                qmam__wfsqf.n_redvars))
            cltu__gzb += 1 + qmam__wfsqf.n_redvars
            tev__pikye.append(out_data_typs_[jjcpf__upk])
    assert len(redvar_offsets) == gob__fzon
    qns__kkkml = len(tev__pikye)
    dfar__yei = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    dfar__yei += '    if is_null_pointer(table):\n'
    dfar__yei += '        return\n'
    dfar__yei += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in czaz__ldwye]), 
        ',' if len(czaz__ldwye) == 1 else '')
    dfar__yei += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        tev__pikye]), ',' if len(tev__pikye) == 1 else '')
    for jjcpf__upk in range(gob__fzon):
        dfar__yei += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(jjcpf__upk, redvar_offsets[jjcpf__upk], jjcpf__upk))
        dfar__yei += '    incref(redvar_arr_{})\n'.format(jjcpf__upk)
    dfar__yei += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(jjcpf__upk) for jjcpf__upk in range(gob__fzon)]), ',' if 
        gob__fzon == 1 else '')
    dfar__yei += '\n'
    for jjcpf__upk in range(qns__kkkml):
        dfar__yei += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(jjcpf__upk, jgn__mnw[jjcpf__upk], jjcpf__upk))
        dfar__yei += '    incref(data_out_{})\n'.format(jjcpf__upk)
    dfar__yei += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(jjcpf__upk) for jjcpf__upk in range(qns__kkkml)]), ',' if 
        qns__kkkml == 1 else '')
    dfar__yei += '\n'
    dfar__yei += '    for i in range(len(data_out_0)):\n'
    dfar__yei += '        __eval_res(redvars, data_out, i)\n'
    eov__evkea = {}
    exec(dfar__yei, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, eov__evkea)
    return eov__evkea['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    cltu__gzb = n_keys
    okyqb__tdd = []
    for jjcpf__upk, qmam__wfsqf in enumerate(allfuncs):
        if qmam__wfsqf.ftype == 'gen_udf':
            okyqb__tdd.append(cltu__gzb)
            cltu__gzb += 1
        elif qmam__wfsqf.ftype != 'udf':
            cltu__gzb += qmam__wfsqf.ncols_post_shuffle
        else:
            cltu__gzb += qmam__wfsqf.n_redvars + 1
    dfar__yei = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    dfar__yei += '    if num_groups == 0:\n'
    dfar__yei += '        return\n'
    for jjcpf__upk, func in enumerate(udf_func_struct.general_udf_funcs):
        dfar__yei += '    # col {}\n'.format(jjcpf__upk)
        dfar__yei += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(okyqb__tdd[jjcpf__upk], jjcpf__upk))
        dfar__yei += '    incref(out_col)\n'
        dfar__yei += '    for j in range(num_groups):\n'
        dfar__yei += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(jjcpf__upk, jjcpf__upk))
        dfar__yei += '        incref(in_col)\n'
        dfar__yei += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(jjcpf__upk))
    nrx__efvq = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    hhlqi__kqjmk = 0
    for jjcpf__upk, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[hhlqi__kqjmk]
        nrx__efvq['func_{}'.format(hhlqi__kqjmk)] = func
        nrx__efvq['in_col_{}_typ'.format(hhlqi__kqjmk)] = in_col_typs[
            func_idx_to_in_col[jjcpf__upk]]
        nrx__efvq['out_col_{}_typ'.format(hhlqi__kqjmk)] = out_col_typs[
            jjcpf__upk]
        hhlqi__kqjmk += 1
    eov__evkea = {}
    exec(dfar__yei, nrx__efvq, eov__evkea)
    qmam__wfsqf = eov__evkea['bodo_gb_apply_general_udfs{}'.format(
        label_suffix)]
    tmde__jdrv = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(tmde__jdrv, nopython=True)(qmam__wfsqf)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    igqgn__apq = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        cvl__xxs = []
        if agg_node.in_vars[0] is not None:
            cvl__xxs.append('arg0')
        for jjcpf__upk in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if jjcpf__upk not in agg_node.dead_in_inds:
                cvl__xxs.append(f'arg{jjcpf__upk}')
    else:
        cvl__xxs = [f'arg{jjcpf__upk}' for jjcpf__upk, pdnwz__zuit in
            enumerate(agg_node.in_vars) if pdnwz__zuit is not None]
    dfar__yei = f"def agg_top({', '.join(cvl__xxs)}):\n"
    ghq__ctfk = []
    if agg_node.is_in_table_format:
        ghq__ctfk = agg_node.in_key_inds + [ncbz__qcvwu for ncbz__qcvwu,
            eif__xww in agg_node.gb_info_out.values() if ncbz__qcvwu is not
            None]
        if agg_node.input_has_index:
            ghq__ctfk.append(agg_node.n_in_cols - 1)
        symm__mzuum = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        suk__ian = []
        for jjcpf__upk in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if jjcpf__upk in agg_node.dead_in_inds:
                suk__ian.append('None')
            else:
                suk__ian.append(f'arg{jjcpf__upk}')
        fcim__dqewj = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        dfar__yei += f"""    table = py_data_to_cpp_table({fcim__dqewj}, ({', '.join(suk__ian)}{symm__mzuum}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        ksc__rfrtp = [f'arg{jjcpf__upk}' for jjcpf__upk in agg_node.in_key_inds
            ]
        oyh__hmrgs = [f'arg{ncbz__qcvwu}' for ncbz__qcvwu, eif__xww in
            agg_node.gb_info_out.values() if ncbz__qcvwu is not None]
        oxeaq__maz = ksc__rfrtp + oyh__hmrgs
        if agg_node.input_has_index:
            oxeaq__maz.append(f'arg{len(agg_node.in_vars) - 1}')
        dfar__yei += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({wijw__ukg})' for wijw__ukg in oxeaq__maz))
        dfar__yei += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    ratpz__wgm = []
    func_idx_to_in_col = []
    gkh__ugzk = []
    tmzts__dyl = False
    hezqd__qrlav = 1
    eou__zuoq = -1
    cwg__qjo = 0
    uksa__nlt = 0
    oiy__qtzo = [func for eif__xww, func in agg_node.gb_info_out.values()]
    for ntsq__cvue, func in enumerate(oiy__qtzo):
        ratpz__wgm.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            cwg__qjo += 1
        if hasattr(func, 'skipdropna'):
            tmzts__dyl = func.skipdropna
        if func.ftype == 'shift':
            hezqd__qrlav = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            uksa__nlt = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            eou__zuoq = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(ntsq__cvue)
        if func.ftype == 'udf':
            gkh__ugzk.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            gkh__ugzk.append(0)
            do_combine = False
    ratpz__wgm.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if cwg__qjo > 0:
        if cwg__qjo != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    yppt__hxivd = []
    if udf_func_struct is not None:
        sbxu__fay = next_label()
        if udf_func_struct.regular_udfs:
            tmde__jdrv = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            dznk__fqknm = numba.cfunc(tmde__jdrv, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs, do_combine,
                func_idx_to_in_col, sbxu__fay))
            enue__aptw = numba.cfunc(tmde__jdrv, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, sbxu__fay))
            hphi__jgw = numba.cfunc('void(voidptr)', nopython=True)(gen_eval_cb
                (udf_func_struct, allfuncs, n_keys, func_out_types, sbxu__fay))
            udf_func_struct.set_regular_cfuncs(dznk__fqknm, enue__aptw,
                hphi__jgw)
            for zbrix__tchtw in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[zbrix__tchtw.native_name] = zbrix__tchtw
                gb_agg_cfunc_addr[zbrix__tchtw.native_name
                    ] = zbrix__tchtw.address
        if udf_func_struct.general_udfs:
            bjd__skzsr = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, func_out_types, func_idx_to_in_col,
                sbxu__fay)
            udf_func_struct.set_general_cfunc(bjd__skzsr)
        czaz__ldwye = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        jtl__tylcl = 0
        jjcpf__upk = 0
        for txz__fyesr, qmam__wfsqf in zip(agg_node.gb_info_out.keys(),
            allfuncs):
            if qmam__wfsqf.ftype in ('udf', 'gen_udf'):
                yppt__hxivd.append(out_col_typs[txz__fyesr])
                for sbakq__kexxj in range(jtl__tylcl, jtl__tylcl +
                    gkh__ugzk[jjcpf__upk]):
                    yppt__hxivd.append(dtype_to_array_type(czaz__ldwye[
                        sbakq__kexxj]))
                jtl__tylcl += gkh__ugzk[jjcpf__upk]
                jjcpf__upk += 1
        dfar__yei += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{jjcpf__upk}' for jjcpf__upk in range(len(yppt__hxivd)))}{',' if len(yppt__hxivd) == 1 else ''}))
"""
        dfar__yei += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(yppt__hxivd)})
"""
        if udf_func_struct.regular_udfs:
            dfar__yei += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{dznk__fqknm.native_name}')\n"
                )
            dfar__yei += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{enue__aptw.native_name}')\n"
                )
            dfar__yei += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{hphi__jgw.native_name}')\n"
                )
            dfar__yei += (
                f"    cpp_cb_update_addr = get_agg_udf_addr('{dznk__fqknm.native_name}')\n"
                )
            dfar__yei += (
                f"    cpp_cb_combine_addr = get_agg_udf_addr('{enue__aptw.native_name}')\n"
                )
            dfar__yei += (
                f"    cpp_cb_eval_addr = get_agg_udf_addr('{hphi__jgw.native_name}')\n"
                )
        else:
            dfar__yei += '    cpp_cb_update_addr = 0\n'
            dfar__yei += '    cpp_cb_combine_addr = 0\n'
            dfar__yei += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            zbrix__tchtw = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[zbrix__tchtw.native_name] = zbrix__tchtw
            gb_agg_cfunc_addr[zbrix__tchtw.native_name] = zbrix__tchtw.address
            dfar__yei += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{zbrix__tchtw.native_name}')\n"
                )
            dfar__yei += f"""    cpp_cb_general_addr = get_agg_udf_addr('{zbrix__tchtw.native_name}')
"""
        else:
            dfar__yei += '    cpp_cb_general_addr = 0\n'
    else:
        dfar__yei += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        dfar__yei += '    cpp_cb_update_addr = 0\n'
        dfar__yei += '    cpp_cb_combine_addr = 0\n'
        dfar__yei += '    cpp_cb_eval_addr = 0\n'
        dfar__yei += '    cpp_cb_general_addr = 0\n'
    dfar__yei += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(qmam__wfsqf.ftype)) for
        qmam__wfsqf in allfuncs] + ['0']))
    dfar__yei += (
        f'    func_offsets = np.array({str(ratpz__wgm)}, dtype=np.int32)\n')
    if len(gkh__ugzk) > 0:
        dfar__yei += (
            f'    udf_ncols = np.array({str(gkh__ugzk)}, dtype=np.int32)\n')
    else:
        dfar__yei += '    udf_ncols = np.array([0], np.int32)\n'
    dfar__yei += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    buodz__kovup = (agg_node._num_shuffle_keys if agg_node.
        _num_shuffle_keys != -1 else n_keys)
    dfar__yei += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {tmzts__dyl}, {hezqd__qrlav}, {uksa__nlt}, {eou__zuoq}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {buodz__kovup})
"""
    qdk__pun = []
    hvsz__kkg = 0
    if agg_node.return_key:
        tmyl__uzzka = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for jjcpf__upk in range(n_keys):
            zjj__grd = tmyl__uzzka + jjcpf__upk
            qdk__pun.append(zjj__grd if zjj__grd not in agg_node.
                dead_out_inds else -1)
            hvsz__kkg += 1
    for txz__fyesr in agg_node.gb_info_out.keys():
        qdk__pun.append(txz__fyesr)
        hvsz__kkg += 1
    ympb__lkk = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            qdk__pun.append(agg_node.n_out_cols - 1)
        else:
            ympb__lkk = True
    symm__mzuum = ',' if igqgn__apq == 1 else ''
    vjs__syh = (
        f"({', '.join(f'out_type{jjcpf__upk}' for jjcpf__upk in range(igqgn__apq))}{symm__mzuum})"
        )
    shdtv__bmt = []
    wgks__vikr = []
    for jjcpf__upk, t in enumerate(out_col_typs):
        if jjcpf__upk not in agg_node.dead_out_inds and type_has_unknown_cats(t
            ):
            if jjcpf__upk in agg_node.gb_info_out:
                ncbz__qcvwu = agg_node.gb_info_out[jjcpf__upk][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                taoy__muuyc = jjcpf__upk - tmyl__uzzka
                ncbz__qcvwu = agg_node.in_key_inds[taoy__muuyc]
            wgks__vikr.append(jjcpf__upk)
            if (agg_node.is_in_table_format and ncbz__qcvwu < agg_node.
                n_in_table_arrays):
                shdtv__bmt.append(f'get_table_data(arg0, {ncbz__qcvwu})')
            else:
                shdtv__bmt.append(f'arg{ncbz__qcvwu}')
    symm__mzuum = ',' if len(shdtv__bmt) == 1 else ''
    dfar__yei += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {vjs__syh}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(shdtv__bmt)}{symm__mzuum}), unknown_cat_out_inds)
"""
    dfar__yei += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    dfar__yei += '    delete_table_decref_arrays(table)\n'
    dfar__yei += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for jjcpf__upk in range(n_keys):
            if qdk__pun[jjcpf__upk] == -1:
                dfar__yei += (
                    f'    decref_table_array(out_table, {jjcpf__upk})\n')
    if ympb__lkk:
        urn__wfbw = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        dfar__yei += f'    decref_table_array(out_table, {urn__wfbw})\n'
    dfar__yei += '    delete_table(out_table)\n'
    dfar__yei += '    ev_clean.finalize()\n'
    dfar__yei += '    return out_data\n'
    fxe__efa = {f'out_type{jjcpf__upk}': out_var_types[jjcpf__upk] for
        jjcpf__upk in range(igqgn__apq)}
    fxe__efa['out_col_inds'] = MetaType(tuple(qdk__pun))
    fxe__efa['in_col_inds'] = MetaType(tuple(ghq__ctfk))
    fxe__efa['cpp_table_to_py_data'] = cpp_table_to_py_data
    fxe__efa['py_data_to_cpp_table'] = py_data_to_cpp_table
    fxe__efa.update({f'udf_type{jjcpf__upk}': t for jjcpf__upk, t in
        enumerate(yppt__hxivd)})
    fxe__efa['udf_dummy_col_inds'] = MetaType(tuple(range(len(yppt__hxivd))))
    fxe__efa['create_dummy_table'] = create_dummy_table
    fxe__efa['unknown_cat_out_inds'] = MetaType(tuple(wgks__vikr))
    fxe__efa['get_table_data'] = bodo.hiframes.table.get_table_data
    return dfar__yei, fxe__efa


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    irsuu__hbtk = tuple(unwrap_typeref(data_types.types[jjcpf__upk]) for
        jjcpf__upk in range(len(data_types.types)))
    kajie__kaoud = bodo.TableType(irsuu__hbtk)
    fxe__efa = {'table_type': kajie__kaoud}
    dfar__yei = 'def impl(data_types):\n'
    dfar__yei += '  py_table = init_table(table_type, False)\n'
    dfar__yei += '  py_table = set_table_len(py_table, 1)\n'
    for qrur__kwtu, eef__ccf in kajie__kaoud.type_to_blk.items():
        fxe__efa[f'typ_list_{eef__ccf}'] = types.List(qrur__kwtu)
        fxe__efa[f'typ_{eef__ccf}'] = qrur__kwtu
        hhmg__psh = len(kajie__kaoud.block_to_arr_ind[eef__ccf])
        dfar__yei += f"""  arr_list_{eef__ccf} = alloc_list_like(typ_list_{eef__ccf}, {hhmg__psh}, False)
"""
        dfar__yei += f'  for i in range(len(arr_list_{eef__ccf})):\n'
        dfar__yei += (
            f'    arr_list_{eef__ccf}[i] = alloc_type(1, typ_{eef__ccf}, (-1,))\n'
            )
        dfar__yei += (
            f'  py_table = set_table_block(py_table, arr_list_{eef__ccf}, {eef__ccf})\n'
            )
    dfar__yei += '  return py_table\n'
    fxe__efa.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    eov__evkea = {}
    exec(dfar__yei, fxe__efa, eov__evkea)
    return eov__evkea['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    fcy__azb = agg_node.in_vars[0].name
    fwab__jexv, xyxod__pvugb, fsh__qgj = block_use_map[fcy__azb]
    if xyxod__pvugb or fsh__qgj:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        qsh__vteb, nwio__nnrm, crbyy__uqk = _compute_table_column_uses(agg_node
            .out_vars[0].name, table_col_use_map, equiv_vars)
        if nwio__nnrm or crbyy__uqk:
            qsh__vteb = set(range(agg_node.n_out_table_arrays))
    else:
        qsh__vteb = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            qsh__vteb = {0}
    zvq__dca = set(jjcpf__upk for jjcpf__upk in agg_node.in_key_inds if 
        jjcpf__upk < agg_node.n_in_table_arrays)
    qbo__ipnes = set(agg_node.gb_info_out[jjcpf__upk][0] for jjcpf__upk in
        qsh__vteb if jjcpf__upk in agg_node.gb_info_out and agg_node.
        gb_info_out[jjcpf__upk][0] is not None)
    qbo__ipnes |= zvq__dca | fwab__jexv
    poah__ninm = len(set(range(agg_node.n_in_table_arrays)) - qbo__ipnes) == 0
    block_use_map[fcy__azb] = qbo__ipnes, poah__ninm, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    oxxjc__wnjd = agg_node.n_out_table_arrays
    shyis__yeb = agg_node.out_vars[0].name
    vejh__zpe = _find_used_columns(shyis__yeb, oxxjc__wnjd, column_live_map,
        equiv_vars)
    if vejh__zpe is None:
        return False
    zjqjo__fdvxs = set(range(oxxjc__wnjd)) - vejh__zpe
    enft__jjvwq = len(zjqjo__fdvxs - agg_node.dead_out_inds) != 0
    if enft__jjvwq:
        agg_node.dead_out_inds.update(zjqjo__fdvxs)
        agg_node.update_dead_col_info()
    return enft__jjvwq


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for mjh__ios in block.body:
            if is_call_assign(mjh__ios) and find_callname(f_ir, mjh__ios.value
                ) == ('len', 'builtins') and mjh__ios.value.args[0
                ].name == f_ir.arg_names[0]:
                foei__qsfq = get_definition(f_ir, mjh__ios.value.func)
                foei__qsfq.name = 'dummy_agg_count'
                foei__qsfq.value = dummy_agg_count
    gyqdl__xjnn = get_name_var_table(f_ir.blocks)
    kzr__awbj = {}
    for name, eif__xww in gyqdl__xjnn.items():
        kzr__awbj[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, kzr__awbj)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    cawud__aric = numba.core.compiler.Flags()
    cawud__aric.nrt = True
    fjl__cxlwk = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, cawud__aric)
    fjl__cxlwk.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, bozvo__iingi, calltypes, eif__xww = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    aol__kzxx = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    fsuts__mhsx = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    xpfm__kpvk = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    jusf__invjl = xpfm__kpvk(typemap, calltypes)
    pm = fsuts__mhsx(typingctx, targetctx, None, f_ir, typemap,
        bozvo__iingi, calltypes, jusf__invjl, {}, cawud__aric, None)
    gwh__cukz = numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline(
        pm)
    pm = fsuts__mhsx(typingctx, targetctx, None, f_ir, typemap,
        bozvo__iingi, calltypes, jusf__invjl, {}, cawud__aric, gwh__cukz)
    jrf__ntrc = numba.core.typed_passes.InlineOverloads()
    jrf__ntrc.run_pass(pm)
    gqjpm__jsxe = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    gqjpm__jsxe.run()
    for block in f_ir.blocks.values():
        for mjh__ios in block.body:
            if is_assign(mjh__ios) and isinstance(mjh__ios.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[mjh__ios.target.name],
                SeriesType):
                qrur__kwtu = typemap.pop(mjh__ios.target.name)
                typemap[mjh__ios.target.name] = qrur__kwtu.data
            if is_call_assign(mjh__ios) and find_callname(f_ir, mjh__ios.value
                ) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[mjh__ios.target.name].remove(mjh__ios.value)
                mjh__ios.value = mjh__ios.value.args[0]
                f_ir._definitions[mjh__ios.target.name].append(mjh__ios.value)
            if is_call_assign(mjh__ios) and find_callname(f_ir, mjh__ios.value
                ) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[mjh__ios.target.name].remove(mjh__ios.value)
                mjh__ios.value = ir.Const(False, mjh__ios.loc)
                f_ir._definitions[mjh__ios.target.name].append(mjh__ios.value)
            if is_call_assign(mjh__ios) and find_callname(f_ir, mjh__ios.value
                ) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[mjh__ios.target.name].remove(mjh__ios.value)
                mjh__ios.value = ir.Const(False, mjh__ios.loc)
                f_ir._definitions[mjh__ios.target.name].append(mjh__ios.value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    izkdz__mok = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, aol__kzxx)
    izkdz__mok.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    flcev__awmtf = numba.core.compiler.StateDict()
    flcev__awmtf.func_ir = f_ir
    flcev__awmtf.typemap = typemap
    flcev__awmtf.calltypes = calltypes
    flcev__awmtf.typingctx = typingctx
    flcev__awmtf.targetctx = targetctx
    flcev__awmtf.return_type = bozvo__iingi
    numba.core.rewrites.rewrite_registry.apply('after-inference', flcev__awmtf)
    klt__zyqkp = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        bozvo__iingi, typingctx, targetctx, aol__kzxx, cawud__aric, {})
    klt__zyqkp.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            oft__tewpw = ctypes.pythonapi.PyCell_Get
            oft__tewpw.restype = ctypes.py_object
            oft__tewpw.argtypes = ctypes.py_object,
            xsk__ejzcw = tuple(oft__tewpw(dmbdu__aec) for dmbdu__aec in closure
                )
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            xsk__ejzcw = closure.items
        assert len(code.co_freevars) == len(xsk__ejzcw)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, xsk__ejzcw
            )


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
        luj__yquzl = SeriesType(in_col_typ.dtype, to_str_arr_if_dict_array(
            in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (luj__yquzl,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        pjm__eaahv, arr_var = _rm_arg_agg_block(block, pm.typemap)
        owfc__fjk = -1
        for jjcpf__upk, mjh__ios in enumerate(pjm__eaahv):
            if isinstance(mjh__ios, numba.parfors.parfor.Parfor):
                assert owfc__fjk == -1, 'only one parfor for aggregation function'
                owfc__fjk = jjcpf__upk
        parfor = None
        if owfc__fjk != -1:
            parfor = pjm__eaahv[owfc__fjk]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = pjm__eaahv[:owfc__fjk] + parfor.init_block.body
        eval_nodes = pjm__eaahv[owfc__fjk + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for mjh__ios in init_nodes:
            if is_assign(mjh__ios) and mjh__ios.target.name in redvars:
                ind = redvars.index(mjh__ios.target.name)
                reduce_vars[ind] = mjh__ios.target
        var_types = [pm.typemap[pdnwz__zuit] for pdnwz__zuit in redvars]
        eybsm__mbzv = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        tbhsu__emis = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        iraai__jiokm = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(iraai__jiokm)
        self.all_update_funcs.append(tbhsu__emis)
        self.all_combine_funcs.append(eybsm__mbzv)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        rifhm__eyq = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        akhtb__vtlr = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        gjm__tprue = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        vbj__jkf = gen_all_eval_func(self.all_eval_funcs, self.redvar_offsets)
        return self.all_vartypes, rifhm__eyq, akhtb__vtlr, gjm__tprue, vbj__jkf


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
    wzd__wzcp = []
    for t, qmam__wfsqf in zip(in_col_types, agg_func):
        wzd__wzcp.append((t, qmam__wfsqf))
    vatc__rqnuw = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    egpvv__ngtz = GeneralUDFGenerator()
    for in_col_typ, func in wzd__wzcp:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            vatc__rqnuw.add_udf(in_col_typ, func)
        except:
            egpvv__ngtz.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = vatc__rqnuw.gen_all_func()
    general_udf_funcs = egpvv__ngtz.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    njt__xpydt = compute_use_defs(parfor.loop_body)
    xhd__fyfl = set()
    for llj__hkf in njt__xpydt.usemap.values():
        xhd__fyfl |= llj__hkf
    jnfh__fbeqq = set()
    for llj__hkf in njt__xpydt.defmap.values():
        jnfh__fbeqq |= llj__hkf
    krgp__pdeq = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    krgp__pdeq.body = eval_nodes
    peqxx__ivvcm = compute_use_defs({(0): krgp__pdeq})
    nkjn__kpfx = peqxx__ivvcm.usemap[0]
    jyvjm__mvbc = set()
    ajscv__swdxr = []
    gjwyu__dhf = []
    for mjh__ios in reversed(init_nodes):
        evkqq__kac = {pdnwz__zuit.name for pdnwz__zuit in mjh__ios.list_vars()}
        if is_assign(mjh__ios):
            pdnwz__zuit = mjh__ios.target.name
            evkqq__kac.remove(pdnwz__zuit)
            if (pdnwz__zuit in xhd__fyfl and pdnwz__zuit not in jyvjm__mvbc and
                pdnwz__zuit not in nkjn__kpfx and pdnwz__zuit not in
                jnfh__fbeqq):
                gjwyu__dhf.append(mjh__ios)
                xhd__fyfl |= evkqq__kac
                jnfh__fbeqq.add(pdnwz__zuit)
                continue
        jyvjm__mvbc |= evkqq__kac
        ajscv__swdxr.append(mjh__ios)
    gjwyu__dhf.reverse()
    ajscv__swdxr.reverse()
    bzn__dyfcu = min(parfor.loop_body.keys())
    hux__vdebb = parfor.loop_body[bzn__dyfcu]
    hux__vdebb.body = gjwyu__dhf + hux__vdebb.body
    return ajscv__swdxr


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    skaxe__phps = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    ukarz__clp = set()
    koibg__hwxjj = []
    for mjh__ios in init_nodes:
        if is_assign(mjh__ios) and isinstance(mjh__ios.value, ir.Global
            ) and isinstance(mjh__ios.value.value, pytypes.FunctionType
            ) and mjh__ios.value.value in skaxe__phps:
            ukarz__clp.add(mjh__ios.target.name)
        elif is_call_assign(mjh__ios
            ) and mjh__ios.value.func.name in ukarz__clp:
            pass
        else:
            koibg__hwxjj.append(mjh__ios)
    init_nodes = koibg__hwxjj
    nlr__fxbzp = types.Tuple(var_types)
    rmq__efk = lambda : None
    f_ir = compile_to_numba_ir(rmq__efk, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    dgqvw__dbqq = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    micj__vhvfi = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        dgqvw__dbqq, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [micj__vhvfi] + block.body
    block.body[-2].value.value = dgqvw__dbqq
    llbuz__vgg = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        nlr__fxbzp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    pwmy__hwke = numba.core.target_extension.dispatcher_registry[cpu_target](
        rmq__efk)
    pwmy__hwke.add_overload(llbuz__vgg)
    return pwmy__hwke


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    gkwyh__klo = len(update_funcs)
    lds__gkq = len(in_col_types)
    dfar__yei = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for sbakq__kexxj in range(gkwyh__klo):
        fsdro__susym = ', '.join(['redvar_arrs[{}][w_ind]'.format(
            jjcpf__upk) for jjcpf__upk in range(redvar_offsets[sbakq__kexxj
            ], redvar_offsets[sbakq__kexxj + 1])])
        if fsdro__susym:
            dfar__yei += '  {} = update_vars_{}({},  data_in[{}][i])\n'.format(
                fsdro__susym, sbakq__kexxj, fsdro__susym, 0 if lds__gkq == 
                1 else sbakq__kexxj)
    dfar__yei += '  return\n'
    nrx__efvq = {}
    for jjcpf__upk, qmam__wfsqf in enumerate(update_funcs):
        nrx__efvq['update_vars_{}'.format(jjcpf__upk)] = qmam__wfsqf
    eov__evkea = {}
    exec(dfar__yei, nrx__efvq, eov__evkea)
    bui__xds = eov__evkea['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(bui__xds)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    xyi__voltx = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = xyi__voltx, xyi__voltx, types.intp, types.intp
    vspkf__wyomp = len(redvar_offsets) - 1
    dfar__yei = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for sbakq__kexxj in range(vspkf__wyomp):
        fsdro__susym = ', '.join(['redvar_arrs[{}][w_ind]'.format(
            jjcpf__upk) for jjcpf__upk in range(redvar_offsets[sbakq__kexxj
            ], redvar_offsets[sbakq__kexxj + 1])])
        uzbzh__yscbn = ', '.join(['recv_arrs[{}][i]'.format(jjcpf__upk) for
            jjcpf__upk in range(redvar_offsets[sbakq__kexxj],
            redvar_offsets[sbakq__kexxj + 1])])
        if uzbzh__yscbn:
            dfar__yei += '  {} = combine_vars_{}({}, {})\n'.format(fsdro__susym
                , sbakq__kexxj, fsdro__susym, uzbzh__yscbn)
    dfar__yei += '  return\n'
    nrx__efvq = {}
    for jjcpf__upk, qmam__wfsqf in enumerate(combine_funcs):
        nrx__efvq['combine_vars_{}'.format(jjcpf__upk)] = qmam__wfsqf
    eov__evkea = {}
    exec(dfar__yei, nrx__efvq, eov__evkea)
    yak__yoqgf = eov__evkea['combine_all_f']
    f_ir = compile_to_numba_ir(yak__yoqgf, nrx__efvq)
    gjm__tprue = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    pwmy__hwke = numba.core.target_extension.dispatcher_registry[cpu_target](
        yak__yoqgf)
    pwmy__hwke.add_overload(gjm__tprue)
    return pwmy__hwke


def gen_all_eval_func(eval_funcs, redvar_offsets):
    vspkf__wyomp = len(redvar_offsets) - 1
    dfar__yei = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for sbakq__kexxj in range(vspkf__wyomp):
        fsdro__susym = ', '.join(['redvar_arrs[{}][j]'.format(jjcpf__upk) for
            jjcpf__upk in range(redvar_offsets[sbakq__kexxj],
            redvar_offsets[sbakq__kexxj + 1])])
        dfar__yei += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
            sbakq__kexxj, sbakq__kexxj, fsdro__susym)
    dfar__yei += '  return\n'
    nrx__efvq = {}
    for jjcpf__upk, qmam__wfsqf in enumerate(eval_funcs):
        nrx__efvq['eval_vars_{}'.format(jjcpf__upk)] = qmam__wfsqf
    eov__evkea = {}
    exec(dfar__yei, nrx__efvq, eov__evkea)
    zser__bjx = eov__evkea['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(zser__bjx)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    mpl__bvh = len(var_types)
    ugxf__ogrsh = [f'in{jjcpf__upk}' for jjcpf__upk in range(mpl__bvh)]
    nlr__fxbzp = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    vtyu__wqp = nlr__fxbzp(0)
    dfar__yei = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        ugxf__ogrsh))
    eov__evkea = {}
    exec(dfar__yei, {'_zero': vtyu__wqp}, eov__evkea)
    hojkz__rsm = eov__evkea['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(hojkz__rsm, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': vtyu__wqp}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    yqwvh__qgf = []
    for jjcpf__upk, pdnwz__zuit in enumerate(reduce_vars):
        yqwvh__qgf.append(ir.Assign(block.body[jjcpf__upk].target,
            pdnwz__zuit, pdnwz__zuit.loc))
        for vegpc__cke in pdnwz__zuit.versioned_names:
            yqwvh__qgf.append(ir.Assign(pdnwz__zuit, ir.Var(pdnwz__zuit.
                scope, vegpc__cke, pdnwz__zuit.loc), pdnwz__zuit.loc))
    block.body = block.body[:mpl__bvh] + yqwvh__qgf + eval_nodes
    iraai__jiokm = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nlr__fxbzp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    pwmy__hwke = numba.core.target_extension.dispatcher_registry[cpu_target](
        hojkz__rsm)
    pwmy__hwke.add_overload(iraai__jiokm)
    return pwmy__hwke


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    mpl__bvh = len(redvars)
    ixsmj__ytinp = [f'v{jjcpf__upk}' for jjcpf__upk in range(mpl__bvh)]
    ugxf__ogrsh = [f'in{jjcpf__upk}' for jjcpf__upk in range(mpl__bvh)]
    dfar__yei = 'def agg_combine({}):\n'.format(', '.join(ixsmj__ytinp +
        ugxf__ogrsh))
    mtn__rprn = wrap_parfor_blocks(parfor)
    ghh__rzaaz = find_topo_order(mtn__rprn)
    ghh__rzaaz = ghh__rzaaz[1:]
    unwrap_parfor_blocks(parfor)
    eaux__ken = {}
    lwbt__imgc = []
    for bwsy__amwua in ghh__rzaaz:
        rfjr__sxh = parfor.loop_body[bwsy__amwua]
        for mjh__ios in rfjr__sxh.body:
            if is_assign(mjh__ios) and mjh__ios.target.name in redvars:
                kqs__brnd = mjh__ios.target.name
                ind = redvars.index(kqs__brnd)
                if ind in lwbt__imgc:
                    continue
                if len(f_ir._definitions[kqs__brnd]) == 2:
                    var_def = f_ir._definitions[kqs__brnd][0]
                    dfar__yei += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[kqs__brnd][1]
                    dfar__yei += _match_reduce_def(var_def, f_ir, ind)
    dfar__yei += '    return {}'.format(', '.join(['v{}'.format(jjcpf__upk) for
        jjcpf__upk in range(mpl__bvh)]))
    eov__evkea = {}
    exec(dfar__yei, {}, eov__evkea)
    ohor__mpu = eov__evkea['agg_combine']
    arg_typs = tuple(2 * var_types)
    nrx__efvq = {'numba': numba, 'bodo': bodo, 'np': np}
    nrx__efvq.update(eaux__ken)
    f_ir = compile_to_numba_ir(ohor__mpu, nrx__efvq, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    nlr__fxbzp = pm.typemap[block.body[-1].value.name]
    eybsm__mbzv = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nlr__fxbzp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    pwmy__hwke = numba.core.target_extension.dispatcher_registry[cpu_target](
        ohor__mpu)
    pwmy__hwke.add_overload(eybsm__mbzv)
    return pwmy__hwke


def _match_reduce_def(var_def, f_ir, ind):
    dfar__yei = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        dfar__yei = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        tfo__zstn = guard(find_callname, f_ir, var_def)
        if tfo__zstn == ('min', 'builtins'):
            dfar__yei = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if tfo__zstn == ('max', 'builtins'):
            dfar__yei = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return dfar__yei


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    mpl__bvh = len(redvars)
    uzyyt__ipw = 1
    in_vars = []
    for jjcpf__upk in range(uzyyt__ipw):
        qtyky__qru = ir.Var(arr_var.scope, f'$input{jjcpf__upk}', arr_var.loc)
        in_vars.append(qtyky__qru)
    zcp__duwsj = parfor.loop_nests[0].index_variable
    rim__ghit = [0] * mpl__bvh
    for rfjr__sxh in parfor.loop_body.values():
        asrtu__ppci = []
        for mjh__ios in rfjr__sxh.body:
            if is_var_assign(mjh__ios
                ) and mjh__ios.value.name == zcp__duwsj.name:
                continue
            if is_getitem(mjh__ios
                ) and mjh__ios.value.value.name == arr_var.name:
                mjh__ios.value = in_vars[0]
            if is_call_assign(mjh__ios) and guard(find_callname, pm.func_ir,
                mjh__ios.value) == ('isna', 'bodo.libs.array_kernels'
                ) and mjh__ios.value.args[0].name == arr_var.name:
                mjh__ios.value = ir.Const(False, mjh__ios.target.loc)
            if is_assign(mjh__ios) and mjh__ios.target.name in redvars:
                ind = redvars.index(mjh__ios.target.name)
                rim__ghit[ind] = mjh__ios.target
            asrtu__ppci.append(mjh__ios)
        rfjr__sxh.body = asrtu__ppci
    ixsmj__ytinp = ['v{}'.format(jjcpf__upk) for jjcpf__upk in range(mpl__bvh)]
    ugxf__ogrsh = ['in{}'.format(jjcpf__upk) for jjcpf__upk in range(
        uzyyt__ipw)]
    dfar__yei = 'def agg_update({}):\n'.format(', '.join(ixsmj__ytinp +
        ugxf__ogrsh))
    dfar__yei += '    __update_redvars()\n'
    dfar__yei += '    return {}'.format(', '.join(['v{}'.format(jjcpf__upk) for
        jjcpf__upk in range(mpl__bvh)]))
    eov__evkea = {}
    exec(dfar__yei, {}, eov__evkea)
    yeg__yfk = eov__evkea['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * uzyyt__ipw)
    f_ir = compile_to_numba_ir(yeg__yfk, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    azzsv__ttuyd = f_ir.blocks.popitem()[1].body
    nlr__fxbzp = pm.typemap[azzsv__ttuyd[-1].value.name]
    mtn__rprn = wrap_parfor_blocks(parfor)
    ghh__rzaaz = find_topo_order(mtn__rprn)
    ghh__rzaaz = ghh__rzaaz[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    hux__vdebb = f_ir.blocks[ghh__rzaaz[0]]
    ssrp__kimko = f_ir.blocks[ghh__rzaaz[-1]]
    dzuh__qbt = azzsv__ttuyd[:mpl__bvh + uzyyt__ipw]
    if mpl__bvh > 1:
        mbrfi__zcwke = azzsv__ttuyd[-3:]
        assert is_assign(mbrfi__zcwke[0]) and isinstance(mbrfi__zcwke[0].
            value, ir.Expr) and mbrfi__zcwke[0].value.op == 'build_tuple'
    else:
        mbrfi__zcwke = azzsv__ttuyd[-2:]
    for jjcpf__upk in range(mpl__bvh):
        hwjmk__wkif = azzsv__ttuyd[jjcpf__upk].target
        qnhvb__nlbw = ir.Assign(hwjmk__wkif, rim__ghit[jjcpf__upk],
            hwjmk__wkif.loc)
        dzuh__qbt.append(qnhvb__nlbw)
    for jjcpf__upk in range(mpl__bvh, mpl__bvh + uzyyt__ipw):
        hwjmk__wkif = azzsv__ttuyd[jjcpf__upk].target
        qnhvb__nlbw = ir.Assign(hwjmk__wkif, in_vars[jjcpf__upk - mpl__bvh],
            hwjmk__wkif.loc)
        dzuh__qbt.append(qnhvb__nlbw)
    hux__vdebb.body = dzuh__qbt + hux__vdebb.body
    fjllp__yxu = []
    for jjcpf__upk in range(mpl__bvh):
        hwjmk__wkif = azzsv__ttuyd[jjcpf__upk].target
        qnhvb__nlbw = ir.Assign(rim__ghit[jjcpf__upk], hwjmk__wkif,
            hwjmk__wkif.loc)
        fjllp__yxu.append(qnhvb__nlbw)
    ssrp__kimko.body += fjllp__yxu + mbrfi__zcwke
    lxm__exec = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nlr__fxbzp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    pwmy__hwke = numba.core.target_extension.dispatcher_registry[cpu_target](
        yeg__yfk)
    pwmy__hwke.add_overload(lxm__exec)
    return pwmy__hwke


def _rm_arg_agg_block(block, typemap):
    pjm__eaahv = []
    arr_var = None
    for jjcpf__upk, mjh__ios in enumerate(block.body):
        if is_assign(mjh__ios) and isinstance(mjh__ios.value, ir.Arg):
            arr_var = mjh__ios.target
            aca__cezyc = typemap[arr_var.name]
            if not isinstance(aca__cezyc, types.ArrayCompatible):
                pjm__eaahv += block.body[jjcpf__upk + 1:]
                break
            grgb__wposz = block.body[jjcpf__upk + 1]
            assert is_assign(grgb__wposz) and isinstance(grgb__wposz.value,
                ir.Expr
                ) and grgb__wposz.value.op == 'getattr' and grgb__wposz.value.attr == 'shape' and grgb__wposz.value.value.name == arr_var.name
            tpat__ywktq = grgb__wposz.target
            gbas__afmg = block.body[jjcpf__upk + 2]
            assert is_assign(gbas__afmg) and isinstance(gbas__afmg.value,
                ir.Expr
                ) and gbas__afmg.value.op == 'static_getitem' and gbas__afmg.value.value.name == tpat__ywktq.name
            pjm__eaahv += block.body[jjcpf__upk + 3:]
            break
        pjm__eaahv.append(mjh__ios)
    return pjm__eaahv, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    mtn__rprn = wrap_parfor_blocks(parfor)
    ghh__rzaaz = find_topo_order(mtn__rprn)
    ghh__rzaaz = ghh__rzaaz[1:]
    unwrap_parfor_blocks(parfor)
    for bwsy__amwua in reversed(ghh__rzaaz):
        for mjh__ios in reversed(parfor.loop_body[bwsy__amwua].body):
            if isinstance(mjh__ios, ir.Assign) and (mjh__ios.target.name in
                parfor_params or mjh__ios.target.name in var_to_param):
                clbmh__bme = mjh__ios.target.name
                rhs = mjh__ios.value
                cdwgl__kwa = (clbmh__bme if clbmh__bme in parfor_params else
                    var_to_param[clbmh__bme])
                ylfy__rkwc = []
                if isinstance(rhs, ir.Var):
                    ylfy__rkwc = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    ylfy__rkwc = [pdnwz__zuit.name for pdnwz__zuit in
                        mjh__ios.value.list_vars()]
                param_uses[cdwgl__kwa].extend(ylfy__rkwc)
                for pdnwz__zuit in ylfy__rkwc:
                    var_to_param[pdnwz__zuit] = cdwgl__kwa
            if isinstance(mjh__ios, Parfor):
                get_parfor_reductions(mjh__ios, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for hpv__daqnj, ylfy__rkwc in param_uses.items():
        if hpv__daqnj in ylfy__rkwc and hpv__daqnj not in reduce_varnames:
            reduce_varnames.append(hpv__daqnj)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
