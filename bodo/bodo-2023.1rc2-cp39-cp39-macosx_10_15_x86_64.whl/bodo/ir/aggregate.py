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
        sayt__mndie = func.signature
        if sayt__mndie == types.none(types.voidptr):
            bkdh__dnl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            nxw__aehh = cgutils.get_or_insert_function(builder.module,
                bkdh__dnl, sym._literal_value)
            builder.call(nxw__aehh, [context.get_constant_null(sayt__mndie.
                args[0])])
        elif sayt__mndie == types.none(types.int64, types.voidptr, types.
            voidptr):
            bkdh__dnl = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            nxw__aehh = cgutils.get_or_insert_function(builder.module,
                bkdh__dnl, sym._literal_value)
            builder.call(nxw__aehh, [context.get_constant(types.int64, 0),
                context.get_constant_null(sayt__mndie.args[1]), context.
                get_constant_null(sayt__mndie.args[2])])
        else:
            bkdh__dnl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            nxw__aehh = cgutils.get_or_insert_function(builder.module,
                bkdh__dnl, sym._literal_value)
            builder.call(nxw__aehh, [context.get_constant_null(sayt__mndie.
                args[0]), context.get_constant_null(sayt__mndie.args[1]),
                context.get_constant_null(sayt__mndie.args[2])])
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
        lty__nox = True
        poq__gdw = 1
        rirhy__gyzf = -1
        if isinstance(rhs, ir.Expr):
            for rib__nhkr in rhs.kws:
                if func_name in list_cumulative:
                    if rib__nhkr[0] == 'skipna':
                        lty__nox = guard(find_const, func_ir, rib__nhkr[1])
                        if not isinstance(lty__nox, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if rib__nhkr[0] == 'dropna':
                        lty__nox = guard(find_const, func_ir, rib__nhkr[1])
                        if not isinstance(lty__nox, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            poq__gdw = get_call_expr_arg('shift', rhs.args, dict(rhs.kws), 
                0, 'periods', poq__gdw)
            poq__gdw = guard(find_const, func_ir, poq__gdw)
        if func_name == 'head':
            rirhy__gyzf = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(rirhy__gyzf, int):
                rirhy__gyzf = guard(find_const, func_ir, rirhy__gyzf)
            if rirhy__gyzf < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = lty__nox
        func.periods = poq__gdw
        func.head_n = rirhy__gyzf
        if func_name == 'transform':
            kws = dict(rhs.kws)
            fesgn__axtxc = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            whbjp__srgf = typemap[fesgn__axtxc.name]
            yalgh__qkjan = None
            if isinstance(whbjp__srgf, str):
                yalgh__qkjan = whbjp__srgf
            elif is_overload_constant_str(whbjp__srgf):
                yalgh__qkjan = get_overload_const_str(whbjp__srgf)
            elif bodo.utils.typing.is_builtin_function(whbjp__srgf):
                yalgh__qkjan = bodo.utils.typing.get_builtin_function_name(
                    whbjp__srgf)
            if yalgh__qkjan not in bodo.ir.aggregate.supported_transform_funcs[
                :]:
                raise BodoError(
                    f'unsupported transform function {yalgh__qkjan}')
            func.transform_func = supported_agg_funcs.index(yalgh__qkjan)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    fesgn__axtxc = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if fesgn__axtxc == '':
        whbjp__srgf = types.none
    else:
        whbjp__srgf = typemap[fesgn__axtxc.name]
    if is_overload_constant_dict(whbjp__srgf):
        tszmm__rrfcq = get_overload_constant_dict(whbjp__srgf)
        jfrw__jcmjc = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in tszmm__rrfcq.values()]
        return jfrw__jcmjc
    if whbjp__srgf == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(whbjp__srgf, types.BaseTuple) or is_overload_constant_list(
        whbjp__srgf):
        jfrw__jcmjc = []
        lkx__jjzp = 0
        if is_overload_constant_list(whbjp__srgf):
            kgnn__hkfyy = get_overload_const_list(whbjp__srgf)
        else:
            kgnn__hkfyy = whbjp__srgf.types
        for t in kgnn__hkfyy:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                jfrw__jcmjc.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(kgnn__hkfyy) > 1:
                    func.fname = '<lambda_' + str(lkx__jjzp) + '>'
                    lkx__jjzp += 1
                jfrw__jcmjc.append(func)
        return [jfrw__jcmjc]
    if is_overload_constant_str(whbjp__srgf):
        func_name = get_overload_const_str(whbjp__srgf)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(whbjp__srgf):
        func_name = bodo.utils.typing.get_builtin_function_name(whbjp__srgf)
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
        lkx__jjzp = 0
        hftpq__swtw = []
        for lraw__zje in f_val:
            func = get_agg_func_udf(func_ir, lraw__zje, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{lkx__jjzp}>'
                lkx__jjzp += 1
            hftpq__swtw.append(func)
        return hftpq__swtw
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
    yalgh__qkjan = code.co_name
    return yalgh__qkjan


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
            vnzv__nfx = types.DType(args[0])
            return signature(vnzv__nfx, *args)


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
        return [kjjfo__efvi for kjjfo__efvi in self.in_vars if kjjfo__efvi
             is not None]

    def get_live_out_vars(self):
        return [kjjfo__efvi for kjjfo__efvi in self.out_vars if kjjfo__efvi
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
        zew__mdpo = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        agp__zkyab = list(get_index_data_arr_types(self.out_type.index))
        return zew__mdpo + agp__zkyab

    def update_dead_col_info(self):
        for aytc__dkeeh in self.dead_out_inds:
            self.gb_info_out.pop(aytc__dkeeh, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for xveuj__zpfnb, gtp__xkk in self.gb_info_in.copy().items():
            nssz__sriw = []
            for lraw__zje, aysh__zzdz in gtp__xkk:
                if aysh__zzdz not in self.dead_out_inds:
                    nssz__sriw.append((lraw__zje, aysh__zzdz))
            if not nssz__sriw:
                if (xveuj__zpfnb is not None and xveuj__zpfnb not in self.
                    in_key_inds):
                    self.dead_in_inds.add(xveuj__zpfnb)
                self.gb_info_in.pop(xveuj__zpfnb)
            else:
                self.gb_info_in[xveuj__zpfnb] = nssz__sriw
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for hdsib__wxwd in range(1, len(self.in_vars)):
                aytc__dkeeh = self.n_in_table_arrays + hdsib__wxwd - 1
                if aytc__dkeeh in self.dead_in_inds:
                    self.in_vars[hdsib__wxwd] = None
        else:
            for hdsib__wxwd in range(len(self.in_vars)):
                if hdsib__wxwd in self.dead_in_inds:
                    self.in_vars[hdsib__wxwd] = None

    def __repr__(self):
        tdcxe__rcy = ', '.join(kjjfo__efvi.name for kjjfo__efvi in self.
            get_live_in_vars())
        cll__hofx = f'{self.df_in}{{{tdcxe__rcy}}}'
        wvw__ymtht = ', '.join(kjjfo__efvi.name for kjjfo__efvi in self.
            get_live_out_vars())
        ksevp__sziyj = f'{self.df_out}{{{wvw__ymtht}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {cll__hofx} {ksevp__sziyj}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({kjjfo__efvi.name for kjjfo__efvi in aggregate_node.
        get_live_in_vars()})
    def_set.update({kjjfo__efvi.name for kjjfo__efvi in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    qxk__agxnq = agg_node.out_vars[0]
    if qxk__agxnq is not None and qxk__agxnq.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            dswa__ovih = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(dswa__ovih)
        else:
            agg_node.dead_out_inds.add(0)
    for hdsib__wxwd in range(1, len(agg_node.out_vars)):
        kjjfo__efvi = agg_node.out_vars[hdsib__wxwd]
        if kjjfo__efvi is not None and kjjfo__efvi.name not in lives:
            agg_node.out_vars[hdsib__wxwd] = None
            aytc__dkeeh = agg_node.n_out_table_arrays + hdsib__wxwd - 1
            agg_node.dead_out_inds.add(aytc__dkeeh)
    if all(kjjfo__efvi is None for kjjfo__efvi in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    xbp__tlv = {kjjfo__efvi.name for kjjfo__efvi in aggregate_node.
        get_live_out_vars()}
    return set(), xbp__tlv


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for hdsib__wxwd in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[hdsib__wxwd] is not None:
            aggregate_node.in_vars[hdsib__wxwd] = replace_vars_inner(
                aggregate_node.in_vars[hdsib__wxwd], var_dict)
    for hdsib__wxwd in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[hdsib__wxwd] is not None:
            aggregate_node.out_vars[hdsib__wxwd] = replace_vars_inner(
                aggregate_node.out_vars[hdsib__wxwd], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for hdsib__wxwd in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[hdsib__wxwd] is not None:
            aggregate_node.in_vars[hdsib__wxwd] = visit_vars_inner(
                aggregate_node.in_vars[hdsib__wxwd], callback, cbdata)
    for hdsib__wxwd in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[hdsib__wxwd] is not None:
            aggregate_node.out_vars[hdsib__wxwd] = visit_vars_inner(
                aggregate_node.out_vars[hdsib__wxwd], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    xls__kccmh = []
    for vhjm__zldjm in aggregate_node.get_live_in_vars():
        sxk__wvft = equiv_set.get_shape(vhjm__zldjm)
        if sxk__wvft is not None:
            xls__kccmh.append(sxk__wvft[0])
    if len(xls__kccmh) > 1:
        equiv_set.insert_equiv(*xls__kccmh)
    vjzy__rgvgy = []
    xls__kccmh = []
    for vhjm__zldjm in aggregate_node.get_live_out_vars():
        rflm__xco = typemap[vhjm__zldjm.name]
        huv__tvtwl = array_analysis._gen_shape_call(equiv_set, vhjm__zldjm,
            rflm__xco.ndim, None, vjzy__rgvgy)
        equiv_set.insert_equiv(vhjm__zldjm, huv__tvtwl)
        xls__kccmh.append(huv__tvtwl[0])
        equiv_set.define(vhjm__zldjm, set())
    if len(xls__kccmh) > 1:
        equiv_set.insert_equiv(*xls__kccmh)
    return [], vjzy__rgvgy


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    bqifg__rsr = aggregate_node.get_live_in_vars()
    thgbz__gav = aggregate_node.get_live_out_vars()
    thz__muj = Distribution.OneD
    for vhjm__zldjm in bqifg__rsr:
        thz__muj = Distribution(min(thz__muj.value, array_dists[vhjm__zldjm
            .name].value))
    rxkc__vtki = Distribution(min(thz__muj.value, Distribution.OneD_Var.value))
    for vhjm__zldjm in thgbz__gav:
        if vhjm__zldjm.name in array_dists:
            rxkc__vtki = Distribution(min(rxkc__vtki.value, array_dists[
                vhjm__zldjm.name].value))
    if rxkc__vtki != Distribution.OneD_Var:
        thz__muj = rxkc__vtki
    for vhjm__zldjm in bqifg__rsr:
        array_dists[vhjm__zldjm.name] = thz__muj
    for vhjm__zldjm in thgbz__gav:
        array_dists[vhjm__zldjm.name] = rxkc__vtki


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for vhjm__zldjm in agg_node.get_live_out_vars():
        definitions[vhjm__zldjm.name].append(agg_node)
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
    vfme__dfxv = agg_node.get_live_in_vars()
    tzx__riktp = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for kjjfo__efvi in (vfme__dfxv + tzx__riktp):
            if array_dists[kjjfo__efvi.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                kjjfo__efvi.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    jfrw__jcmjc = []
    func_out_types = []
    for aysh__zzdz, (xveuj__zpfnb, func) in agg_node.gb_info_out.items():
        if xveuj__zpfnb is not None:
            t = agg_node.in_col_types[xveuj__zpfnb]
            in_col_typs.append(t)
        jfrw__jcmjc.append(func)
        func_out_types.append(out_col_typs[aysh__zzdz])
    jyh__ehmw = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for hdsib__wxwd, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            jyh__ehmw.update({f'in_cat_dtype_{hdsib__wxwd}': in_col_typ})
    for hdsib__wxwd, daoya__mkdr in enumerate(out_col_typs):
        if isinstance(daoya__mkdr, bodo.CategoricalArrayType):
            jyh__ehmw.update({f'out_cat_dtype_{hdsib__wxwd}': daoya__mkdr})
    udf_func_struct = get_udf_func_struct(jfrw__jcmjc, in_col_typs,
        typingctx, targetctx)
    out_var_types = [(typemap[kjjfo__efvi.name] if kjjfo__efvi is not None else
        types.none) for kjjfo__efvi in agg_node.out_vars]
    hpkem__vid, unfv__vti = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, func_out_types, parallel, udf_func_struct,
        out_var_types, typemap)
    jyh__ehmw.update(unfv__vti)
    jyh__ehmw.update({'pd': pd, 'pre_alloc_string_array':
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
            jyh__ehmw.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            jyh__ehmw.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    memau__aakd = {}
    exec(hpkem__vid, {}, memau__aakd)
    zxgox__huzis = memau__aakd['agg_top']
    juxxn__azqw = compile_to_numba_ir(zxgox__huzis, jyh__ehmw, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[kjjfo__efvi.
        name] for kjjfo__efvi in vfme__dfxv), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(juxxn__azqw, vfme__dfxv)
    blfcr__emsy = juxxn__azqw.body[-2].value.value
    wwqna__tsnxn = juxxn__azqw.body[:-2]
    for hdsib__wxwd, kjjfo__efvi in enumerate(tzx__riktp):
        gen_getitem(kjjfo__efvi, blfcr__emsy, hdsib__wxwd, calltypes,
            wwqna__tsnxn)
    return wwqna__tsnxn


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        aazmk__mbvdh = IntDtype(t.dtype).name
        assert aazmk__mbvdh.endswith('Dtype()')
        aazmk__mbvdh = aazmk__mbvdh[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{aazmk__mbvdh}'))"
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
        wgiso__osu = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {wgiso__osu}_cat_dtype_{colnum})')
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
    klv__xqjux = udf_func_struct.var_typs
    ppfjw__grp = len(klv__xqjux)
    hpkem__vid = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    hpkem__vid += '    if is_null_pointer(in_table):\n'
    hpkem__vid += '        return\n'
    hpkem__vid += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in klv__xqjux]), 
        ',' if len(klv__xqjux) == 1 else '')
    vjkud__mqw = n_keys
    gzquk__cyq = []
    redvar_offsets = []
    oeu__vgq = []
    if do_combine:
        for hdsib__wxwd, lraw__zje in enumerate(allfuncs):
            if lraw__zje.ftype != 'udf':
                vjkud__mqw += lraw__zje.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(vjkud__mqw, vjkud__mqw +
                    lraw__zje.n_redvars))
                vjkud__mqw += lraw__zje.n_redvars
                oeu__vgq.append(data_in_typs_[func_idx_to_in_col[hdsib__wxwd]])
                gzquk__cyq.append(func_idx_to_in_col[hdsib__wxwd] + n_keys)
    else:
        for hdsib__wxwd, lraw__zje in enumerate(allfuncs):
            if lraw__zje.ftype != 'udf':
                vjkud__mqw += lraw__zje.ncols_post_shuffle
            else:
                redvar_offsets += list(range(vjkud__mqw + 1, vjkud__mqw + 1 +
                    lraw__zje.n_redvars))
                vjkud__mqw += lraw__zje.n_redvars + 1
                oeu__vgq.append(data_in_typs_[func_idx_to_in_col[hdsib__wxwd]])
                gzquk__cyq.append(func_idx_to_in_col[hdsib__wxwd] + n_keys)
    assert len(redvar_offsets) == ppfjw__grp
    moey__qkti = len(oeu__vgq)
    rce__fpe = []
    for hdsib__wxwd, t in enumerate(oeu__vgq):
        rce__fpe.append(_gen_dummy_alloc(t, hdsib__wxwd, True))
    hpkem__vid += '    data_in_dummy = ({}{})\n'.format(','.join(rce__fpe),
        ',' if len(oeu__vgq) == 1 else '')
    hpkem__vid += """
    # initialize redvar cols
"""
    hpkem__vid += '    init_vals = __init_func()\n'
    for hdsib__wxwd in range(ppfjw__grp):
        hpkem__vid += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(hdsib__wxwd, redvar_offsets[hdsib__wxwd], hdsib__wxwd))
        hpkem__vid += '    incref(redvar_arr_{})\n'.format(hdsib__wxwd)
        hpkem__vid += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            hdsib__wxwd, hdsib__wxwd)
    hpkem__vid += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(hdsib__wxwd) for hdsib__wxwd in range(ppfjw__grp)]), ',' if
        ppfjw__grp == 1 else '')
    hpkem__vid += '\n'
    for hdsib__wxwd in range(moey__qkti):
        hpkem__vid += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(hdsib__wxwd, gzquk__cyq[hdsib__wxwd], hdsib__wxwd))
        hpkem__vid += '    incref(data_in_{})\n'.format(hdsib__wxwd)
    hpkem__vid += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(hdsib__wxwd) for hdsib__wxwd in range(moey__qkti)]), ',' if 
        moey__qkti == 1 else '')
    hpkem__vid += '\n'
    hpkem__vid += '    for i in range(len(data_in_0)):\n'
    hpkem__vid += '        w_ind = row_to_group[i]\n'
    hpkem__vid += '        if w_ind != -1:\n'
    hpkem__vid += '            __update_redvars(redvars, data_in, w_ind, i)\n'
    memau__aakd = {}
    exec(hpkem__vid, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, memau__aakd)
    return memau__aakd['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    klv__xqjux = udf_func_struct.var_typs
    ppfjw__grp = len(klv__xqjux)
    hpkem__vid = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    hpkem__vid += '    if is_null_pointer(in_table):\n'
    hpkem__vid += '        return\n'
    hpkem__vid += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in klv__xqjux]), 
        ',' if len(klv__xqjux) == 1 else '')
    scd__lbx = n_keys
    unk__rju = n_keys
    iapi__ygieo = []
    kgu__ecp = []
    for lraw__zje in allfuncs:
        if lraw__zje.ftype != 'udf':
            scd__lbx += lraw__zje.ncols_pre_shuffle
            unk__rju += lraw__zje.ncols_post_shuffle
        else:
            iapi__ygieo += list(range(scd__lbx, scd__lbx + lraw__zje.n_redvars)
                )
            kgu__ecp += list(range(unk__rju + 1, unk__rju + 1 + lraw__zje.
                n_redvars))
            scd__lbx += lraw__zje.n_redvars
            unk__rju += 1 + lraw__zje.n_redvars
    assert len(iapi__ygieo) == ppfjw__grp
    hpkem__vid += """
    # initialize redvar cols
"""
    hpkem__vid += '    init_vals = __init_func()\n'
    for hdsib__wxwd in range(ppfjw__grp):
        hpkem__vid += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(hdsib__wxwd, kgu__ecp[hdsib__wxwd], hdsib__wxwd))
        hpkem__vid += '    incref(redvar_arr_{})\n'.format(hdsib__wxwd)
        hpkem__vid += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            hdsib__wxwd, hdsib__wxwd)
    hpkem__vid += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(hdsib__wxwd) for hdsib__wxwd in range(ppfjw__grp)]), ',' if
        ppfjw__grp == 1 else '')
    hpkem__vid += '\n'
    for hdsib__wxwd in range(ppfjw__grp):
        hpkem__vid += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(hdsib__wxwd, iapi__ygieo[hdsib__wxwd], hdsib__wxwd))
        hpkem__vid += '    incref(recv_redvar_arr_{})\n'.format(hdsib__wxwd)
    hpkem__vid += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(hdsib__wxwd) for hdsib__wxwd in range(
        ppfjw__grp)]), ',' if ppfjw__grp == 1 else '')
    hpkem__vid += '\n'
    if ppfjw__grp:
        hpkem__vid += '    for i in range(len(recv_redvar_arr_0)):\n'
        hpkem__vid += '        w_ind = row_to_group[i]\n'
        hpkem__vid += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    memau__aakd = {}
    exec(hpkem__vid, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, memau__aakd)
    return memau__aakd['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    klv__xqjux = udf_func_struct.var_typs
    ppfjw__grp = len(klv__xqjux)
    vjkud__mqw = n_keys
    redvar_offsets = []
    ailgl__klyt = []
    smdf__squgm = []
    for hdsib__wxwd, lraw__zje in enumerate(allfuncs):
        if lraw__zje.ftype != 'udf':
            vjkud__mqw += lraw__zje.ncols_post_shuffle
        else:
            ailgl__klyt.append(vjkud__mqw)
            redvar_offsets += list(range(vjkud__mqw + 1, vjkud__mqw + 1 +
                lraw__zje.n_redvars))
            vjkud__mqw += 1 + lraw__zje.n_redvars
            smdf__squgm.append(out_data_typs_[hdsib__wxwd])
    assert len(redvar_offsets) == ppfjw__grp
    moey__qkti = len(smdf__squgm)
    hpkem__vid = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    hpkem__vid += '    if is_null_pointer(table):\n'
    hpkem__vid += '        return\n'
    hpkem__vid += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in klv__xqjux]), 
        ',' if len(klv__xqjux) == 1 else '')
    hpkem__vid += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        smdf__squgm]), ',' if len(smdf__squgm) == 1 else '')
    for hdsib__wxwd in range(ppfjw__grp):
        hpkem__vid += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(hdsib__wxwd, redvar_offsets[hdsib__wxwd], hdsib__wxwd))
        hpkem__vid += '    incref(redvar_arr_{})\n'.format(hdsib__wxwd)
    hpkem__vid += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(hdsib__wxwd) for hdsib__wxwd in range(ppfjw__grp)]), ',' if
        ppfjw__grp == 1 else '')
    hpkem__vid += '\n'
    for hdsib__wxwd in range(moey__qkti):
        hpkem__vid += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(hdsib__wxwd, ailgl__klyt[hdsib__wxwd], hdsib__wxwd))
        hpkem__vid += '    incref(data_out_{})\n'.format(hdsib__wxwd)
    hpkem__vid += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(hdsib__wxwd) for hdsib__wxwd in range(moey__qkti)]), ',' if 
        moey__qkti == 1 else '')
    hpkem__vid += '\n'
    hpkem__vid += '    for i in range(len(data_out_0)):\n'
    hpkem__vid += '        __eval_res(redvars, data_out, i)\n'
    memau__aakd = {}
    exec(hpkem__vid, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, memau__aakd)
    return memau__aakd['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    vjkud__mqw = n_keys
    kbnc__mrg = []
    for hdsib__wxwd, lraw__zje in enumerate(allfuncs):
        if lraw__zje.ftype == 'gen_udf':
            kbnc__mrg.append(vjkud__mqw)
            vjkud__mqw += 1
        elif lraw__zje.ftype != 'udf':
            vjkud__mqw += lraw__zje.ncols_post_shuffle
        else:
            vjkud__mqw += lraw__zje.n_redvars + 1
    hpkem__vid = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    hpkem__vid += '    if num_groups == 0:\n'
    hpkem__vid += '        return\n'
    for hdsib__wxwd, func in enumerate(udf_func_struct.general_udf_funcs):
        hpkem__vid += '    # col {}\n'.format(hdsib__wxwd)
        hpkem__vid += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(kbnc__mrg[hdsib__wxwd], hdsib__wxwd))
        hpkem__vid += '    incref(out_col)\n'
        hpkem__vid += '    for j in range(num_groups):\n'
        hpkem__vid += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(hdsib__wxwd, hdsib__wxwd))
        hpkem__vid += '        incref(in_col)\n'
        hpkem__vid += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(hdsib__wxwd))
    jyh__ehmw = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    wqr__vnpaq = 0
    for hdsib__wxwd, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[wqr__vnpaq]
        jyh__ehmw['func_{}'.format(wqr__vnpaq)] = func
        jyh__ehmw['in_col_{}_typ'.format(wqr__vnpaq)] = in_col_typs[
            func_idx_to_in_col[hdsib__wxwd]]
        jyh__ehmw['out_col_{}_typ'.format(wqr__vnpaq)] = out_col_typs[
            hdsib__wxwd]
        wqr__vnpaq += 1
    memau__aakd = {}
    exec(hpkem__vid, jyh__ehmw, memau__aakd)
    lraw__zje = memau__aakd['bodo_gb_apply_general_udfs{}'.format(label_suffix)
        ]
    lmcad__cwrnr = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(lmcad__cwrnr, nopython=True)(lraw__zje)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    yxna__bwsa = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        tqii__sje = []
        if agg_node.in_vars[0] is not None:
            tqii__sje.append('arg0')
        for hdsib__wxwd in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if hdsib__wxwd not in agg_node.dead_in_inds:
                tqii__sje.append(f'arg{hdsib__wxwd}')
    else:
        tqii__sje = [f'arg{hdsib__wxwd}' for hdsib__wxwd, kjjfo__efvi in
            enumerate(agg_node.in_vars) if kjjfo__efvi is not None]
    hpkem__vid = f"def agg_top({', '.join(tqii__sje)}):\n"
    gxyt__tjlpz = []
    if agg_node.is_in_table_format:
        gxyt__tjlpz = agg_node.in_key_inds + [xveuj__zpfnb for xveuj__zpfnb,
            rlfoc__nwazh in agg_node.gb_info_out.values() if xveuj__zpfnb
             is not None]
        if agg_node.input_has_index:
            gxyt__tjlpz.append(agg_node.n_in_cols - 1)
        ixxh__vuyx = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        gac__txhfm = []
        for hdsib__wxwd in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if hdsib__wxwd in agg_node.dead_in_inds:
                gac__txhfm.append('None')
            else:
                gac__txhfm.append(f'arg{hdsib__wxwd}')
        yzvzd__zixuj = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        hpkem__vid += f"""    table = py_data_to_cpp_table({yzvzd__zixuj}, ({', '.join(gac__txhfm)}{ixxh__vuyx}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        mbfe__ogcd = [f'arg{hdsib__wxwd}' for hdsib__wxwd in agg_node.
            in_key_inds]
        nlgat__xlmsv = [f'arg{xveuj__zpfnb}' for xveuj__zpfnb, rlfoc__nwazh in
            agg_node.gb_info_out.values() if xveuj__zpfnb is not None]
        gwmc__xniq = mbfe__ogcd + nlgat__xlmsv
        if agg_node.input_has_index:
            gwmc__xniq.append(f'arg{len(agg_node.in_vars) - 1}')
        hpkem__vid += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({algln__kpq})' for algln__kpq in gwmc__xniq))
        hpkem__vid += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    nncu__peggi = []
    func_idx_to_in_col = []
    nmjt__bgwm = []
    lty__nox = False
    pxxix__rjdor = 1
    rirhy__gyzf = -1
    fnfba__hrr = 0
    xnoo__uphe = 0
    jfrw__jcmjc = [func for rlfoc__nwazh, func in agg_node.gb_info_out.values()
        ]
    for gxupq__ulb, func in enumerate(jfrw__jcmjc):
        nncu__peggi.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            fnfba__hrr += 1
        if hasattr(func, 'skipdropna'):
            lty__nox = func.skipdropna
        if func.ftype == 'shift':
            pxxix__rjdor = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            xnoo__uphe = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            rirhy__gyzf = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(gxupq__ulb)
        if func.ftype == 'udf':
            nmjt__bgwm.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            nmjt__bgwm.append(0)
            do_combine = False
    nncu__peggi.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if fnfba__hrr > 0:
        if fnfba__hrr != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    vum__ryes = []
    if udf_func_struct is not None:
        jqfq__evjt = next_label()
        if udf_func_struct.regular_udfs:
            lmcad__cwrnr = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            gecta__avfl = numba.cfunc(lmcad__cwrnr, nopython=True)(
                gen_update_cb(udf_func_struct, allfuncs, n_keys,
                in_col_typs, do_combine, func_idx_to_in_col, jqfq__evjt))
            agag__dyhbl = numba.cfunc(lmcad__cwrnr, nopython=True)(
                gen_combine_cb(udf_func_struct, allfuncs, n_keys, jqfq__evjt))
            ehqtu__hfy = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys,
                func_out_types, jqfq__evjt))
            udf_func_struct.set_regular_cfuncs(gecta__avfl, agag__dyhbl,
                ehqtu__hfy)
            for xrm__yflq in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[xrm__yflq.native_name] = xrm__yflq
                gb_agg_cfunc_addr[xrm__yflq.native_name] = xrm__yflq.address
        if udf_func_struct.general_udfs:
            efgmh__sgl = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, func_out_types, func_idx_to_in_col,
                jqfq__evjt)
            udf_func_struct.set_general_cfunc(efgmh__sgl)
        klv__xqjux = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        iply__oomph = 0
        hdsib__wxwd = 0
        for rju__pejhr, lraw__zje in zip(agg_node.gb_info_out.keys(), allfuncs
            ):
            if lraw__zje.ftype in ('udf', 'gen_udf'):
                vum__ryes.append(out_col_typs[rju__pejhr])
                for gwxg__mmqhl in range(iply__oomph, iply__oomph +
                    nmjt__bgwm[hdsib__wxwd]):
                    vum__ryes.append(dtype_to_array_type(klv__xqjux[
                        gwxg__mmqhl]))
                iply__oomph += nmjt__bgwm[hdsib__wxwd]
                hdsib__wxwd += 1
        hpkem__vid += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{hdsib__wxwd}' for hdsib__wxwd in range(len(vum__ryes)))}{',' if len(vum__ryes) == 1 else ''}))
"""
        hpkem__vid += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(vum__ryes)})
"""
        if udf_func_struct.regular_udfs:
            hpkem__vid += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{gecta__avfl.native_name}')\n"
                )
            hpkem__vid += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{agag__dyhbl.native_name}')\n"
                )
            hpkem__vid += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{ehqtu__hfy.native_name}')\n"
                )
            hpkem__vid += f"""    cpp_cb_update_addr = get_agg_udf_addr('{gecta__avfl.native_name}')
"""
            hpkem__vid += f"""    cpp_cb_combine_addr = get_agg_udf_addr('{agag__dyhbl.native_name}')
"""
            hpkem__vid += (
                f"    cpp_cb_eval_addr = get_agg_udf_addr('{ehqtu__hfy.native_name}')\n"
                )
        else:
            hpkem__vid += '    cpp_cb_update_addr = 0\n'
            hpkem__vid += '    cpp_cb_combine_addr = 0\n'
            hpkem__vid += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            xrm__yflq = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[xrm__yflq.native_name] = xrm__yflq
            gb_agg_cfunc_addr[xrm__yflq.native_name] = xrm__yflq.address
            hpkem__vid += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{xrm__yflq.native_name}')\n"
                )
            hpkem__vid += (
                f"    cpp_cb_general_addr = get_agg_udf_addr('{xrm__yflq.native_name}')\n"
                )
        else:
            hpkem__vid += '    cpp_cb_general_addr = 0\n'
    else:
        hpkem__vid += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        hpkem__vid += '    cpp_cb_update_addr = 0\n'
        hpkem__vid += '    cpp_cb_combine_addr = 0\n'
        hpkem__vid += '    cpp_cb_eval_addr = 0\n'
        hpkem__vid += '    cpp_cb_general_addr = 0\n'
    hpkem__vid += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(lraw__zje.ftype)) for
        lraw__zje in allfuncs] + ['0']))
    hpkem__vid += (
        f'    func_offsets = np.array({str(nncu__peggi)}, dtype=np.int32)\n')
    if len(nmjt__bgwm) > 0:
        hpkem__vid += (
            f'    udf_ncols = np.array({str(nmjt__bgwm)}, dtype=np.int32)\n')
    else:
        hpkem__vid += '    udf_ncols = np.array([0], np.int32)\n'
    hpkem__vid += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    uuow__pauau = (agg_node._num_shuffle_keys if agg_node._num_shuffle_keys !=
        -1 else n_keys)
    hpkem__vid += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {lty__nox}, {pxxix__rjdor}, {xnoo__uphe}, {rirhy__gyzf}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {uuow__pauau})
"""
    qdn__vebd = []
    fuhl__ddtqe = 0
    if agg_node.return_key:
        bept__jyl = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for hdsib__wxwd in range(n_keys):
            aytc__dkeeh = bept__jyl + hdsib__wxwd
            qdn__vebd.append(aytc__dkeeh if aytc__dkeeh not in agg_node.
                dead_out_inds else -1)
            fuhl__ddtqe += 1
    for rju__pejhr in agg_node.gb_info_out.keys():
        qdn__vebd.append(rju__pejhr)
        fuhl__ddtqe += 1
    jnjcu__tsm = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            qdn__vebd.append(agg_node.n_out_cols - 1)
        else:
            jnjcu__tsm = True
    ixxh__vuyx = ',' if yxna__bwsa == 1 else ''
    shg__iwg = (
        f"({', '.join(f'out_type{hdsib__wxwd}' for hdsib__wxwd in range(yxna__bwsa))}{ixxh__vuyx})"
        )
    xmdn__gjqma = []
    pbvch__pqvuh = []
    for hdsib__wxwd, t in enumerate(out_col_typs):
        if hdsib__wxwd not in agg_node.dead_out_inds and type_has_unknown_cats(
            t):
            if hdsib__wxwd in agg_node.gb_info_out:
                xveuj__zpfnb = agg_node.gb_info_out[hdsib__wxwd][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                maqwp__kqynr = hdsib__wxwd - bept__jyl
                xveuj__zpfnb = agg_node.in_key_inds[maqwp__kqynr]
            pbvch__pqvuh.append(hdsib__wxwd)
            if (agg_node.is_in_table_format and xveuj__zpfnb < agg_node.
                n_in_table_arrays):
                xmdn__gjqma.append(f'get_table_data(arg0, {xveuj__zpfnb})')
            else:
                xmdn__gjqma.append(f'arg{xveuj__zpfnb}')
    ixxh__vuyx = ',' if len(xmdn__gjqma) == 1 else ''
    hpkem__vid += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {shg__iwg}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(xmdn__gjqma)}{ixxh__vuyx}), unknown_cat_out_inds)
"""
    hpkem__vid += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    hpkem__vid += '    delete_table_decref_arrays(table)\n'
    hpkem__vid += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for hdsib__wxwd in range(n_keys):
            if qdn__vebd[hdsib__wxwd] == -1:
                hpkem__vid += (
                    f'    decref_table_array(out_table, {hdsib__wxwd})\n')
    if jnjcu__tsm:
        fgdg__bgc = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        hpkem__vid += f'    decref_table_array(out_table, {fgdg__bgc})\n'
    hpkem__vid += '    delete_table(out_table)\n'
    hpkem__vid += '    ev_clean.finalize()\n'
    hpkem__vid += '    return out_data\n'
    pnqk__nlhj = {f'out_type{hdsib__wxwd}': out_var_types[hdsib__wxwd] for
        hdsib__wxwd in range(yxna__bwsa)}
    pnqk__nlhj['out_col_inds'] = MetaType(tuple(qdn__vebd))
    pnqk__nlhj['in_col_inds'] = MetaType(tuple(gxyt__tjlpz))
    pnqk__nlhj['cpp_table_to_py_data'] = cpp_table_to_py_data
    pnqk__nlhj['py_data_to_cpp_table'] = py_data_to_cpp_table
    pnqk__nlhj.update({f'udf_type{hdsib__wxwd}': t for hdsib__wxwd, t in
        enumerate(vum__ryes)})
    pnqk__nlhj['udf_dummy_col_inds'] = MetaType(tuple(range(len(vum__ryes))))
    pnqk__nlhj['create_dummy_table'] = create_dummy_table
    pnqk__nlhj['unknown_cat_out_inds'] = MetaType(tuple(pbvch__pqvuh))
    pnqk__nlhj['get_table_data'] = bodo.hiframes.table.get_table_data
    return hpkem__vid, pnqk__nlhj


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    tqgg__xiscl = tuple(unwrap_typeref(data_types.types[hdsib__wxwd]) for
        hdsib__wxwd in range(len(data_types.types)))
    uozfb__bmhpb = bodo.TableType(tqgg__xiscl)
    pnqk__nlhj = {'table_type': uozfb__bmhpb}
    hpkem__vid = 'def impl(data_types):\n'
    hpkem__vid += '  py_table = init_table(table_type, False)\n'
    hpkem__vid += '  py_table = set_table_len(py_table, 1)\n'
    for rflm__xco, jghgn__vudxm in uozfb__bmhpb.type_to_blk.items():
        pnqk__nlhj[f'typ_list_{jghgn__vudxm}'] = types.List(rflm__xco)
        pnqk__nlhj[f'typ_{jghgn__vudxm}'] = rflm__xco
        ignjo__juqfh = len(uozfb__bmhpb.block_to_arr_ind[jghgn__vudxm])
        hpkem__vid += f"""  arr_list_{jghgn__vudxm} = alloc_list_like(typ_list_{jghgn__vudxm}, {ignjo__juqfh}, False)
"""
        hpkem__vid += f'  for i in range(len(arr_list_{jghgn__vudxm})):\n'
        hpkem__vid += (
            f'    arr_list_{jghgn__vudxm}[i] = alloc_type(1, typ_{jghgn__vudxm}, (-1,))\n'
            )
        hpkem__vid += f"""  py_table = set_table_block(py_table, arr_list_{jghgn__vudxm}, {jghgn__vudxm})
"""
    hpkem__vid += '  return py_table\n'
    pnqk__nlhj.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    memau__aakd = {}
    exec(hpkem__vid, pnqk__nlhj, memau__aakd)
    return memau__aakd['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    saxf__uizb = agg_node.in_vars[0].name
    thdc__jyldn, zew__zzvt, wnbj__jqgb = block_use_map[saxf__uizb]
    if zew__zzvt or wnbj__jqgb:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        jxjf__ggm, lkyw__fkbj, mrqw__hgu = _compute_table_column_uses(agg_node
            .out_vars[0].name, table_col_use_map, equiv_vars)
        if lkyw__fkbj or mrqw__hgu:
            jxjf__ggm = set(range(agg_node.n_out_table_arrays))
    else:
        jxjf__ggm = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            jxjf__ggm = {0}
    jfj__xlbbk = set(hdsib__wxwd for hdsib__wxwd in agg_node.in_key_inds if
        hdsib__wxwd < agg_node.n_in_table_arrays)
    pcru__rsnzk = set(agg_node.gb_info_out[hdsib__wxwd][0] for hdsib__wxwd in
        jxjf__ggm if hdsib__wxwd in agg_node.gb_info_out and agg_node.
        gb_info_out[hdsib__wxwd][0] is not None)
    pcru__rsnzk |= jfj__xlbbk | thdc__jyldn
    gjk__unfwi = len(set(range(agg_node.n_in_table_arrays)) - pcru__rsnzk) == 0
    block_use_map[saxf__uizb] = pcru__rsnzk, gjk__unfwi, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    snk__foznf = agg_node.n_out_table_arrays
    ludvn__fbpxp = agg_node.out_vars[0].name
    hxu__hjve = _find_used_columns(ludvn__fbpxp, snk__foznf,
        column_live_map, equiv_vars)
    if hxu__hjve is None:
        return False
    oqa__rfjt = set(range(snk__foznf)) - hxu__hjve
    zav__dkztc = len(oqa__rfjt - agg_node.dead_out_inds) != 0
    if zav__dkztc:
        agg_node.dead_out_inds.update(oqa__rfjt)
        agg_node.update_dead_col_info()
    return zav__dkztc


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for pzusf__qgtbb in block.body:
            if is_call_assign(pzusf__qgtbb) and find_callname(f_ir,
                pzusf__qgtbb.value) == ('len', 'builtins'
                ) and pzusf__qgtbb.value.args[0].name == f_ir.arg_names[0]:
                sofu__uhvu = get_definition(f_ir, pzusf__qgtbb.value.func)
                sofu__uhvu.name = 'dummy_agg_count'
                sofu__uhvu.value = dummy_agg_count
    bsld__vlml = get_name_var_table(f_ir.blocks)
    pujtl__lqj = {}
    for name, rlfoc__nwazh in bsld__vlml.items():
        pujtl__lqj[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, pujtl__lqj)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    jauly__jqp = numba.core.compiler.Flags()
    jauly__jqp.nrt = True
    jfh__jvqrl = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, jauly__jqp)
    jfh__jvqrl.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, neq__dbra, calltypes, rlfoc__nwazh = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    hvv__hfgo = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    jerug__sfyvq = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    zzy__bwe = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    byqc__zoaji = zzy__bwe(typemap, calltypes)
    pm = jerug__sfyvq(typingctx, targetctx, None, f_ir, typemap, neq__dbra,
        calltypes, byqc__zoaji, {}, jauly__jqp, None)
    hacrk__jdi = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = jerug__sfyvq(typingctx, targetctx, None, f_ir, typemap, neq__dbra,
        calltypes, byqc__zoaji, {}, jauly__jqp, hacrk__jdi)
    segbl__oavl = numba.core.typed_passes.InlineOverloads()
    segbl__oavl.run_pass(pm)
    dua__zyz = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    dua__zyz.run()
    for block in f_ir.blocks.values():
        for pzusf__qgtbb in block.body:
            if is_assign(pzusf__qgtbb) and isinstance(pzusf__qgtbb.value, (
                ir.Arg, ir.Var)) and isinstance(typemap[pzusf__qgtbb.target
                .name], SeriesType):
                rflm__xco = typemap.pop(pzusf__qgtbb.target.name)
                typemap[pzusf__qgtbb.target.name] = rflm__xco.data
            if is_call_assign(pzusf__qgtbb) and find_callname(f_ir,
                pzusf__qgtbb.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[pzusf__qgtbb.target.name].remove(pzusf__qgtbb
                    .value)
                pzusf__qgtbb.value = pzusf__qgtbb.value.args[0]
                f_ir._definitions[pzusf__qgtbb.target.name].append(pzusf__qgtbb
                    .value)
            if is_call_assign(pzusf__qgtbb) and find_callname(f_ir,
                pzusf__qgtbb.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[pzusf__qgtbb.target.name].remove(pzusf__qgtbb
                    .value)
                pzusf__qgtbb.value = ir.Const(False, pzusf__qgtbb.loc)
                f_ir._definitions[pzusf__qgtbb.target.name].append(pzusf__qgtbb
                    .value)
            if is_call_assign(pzusf__qgtbb) and find_callname(f_ir,
                pzusf__qgtbb.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[pzusf__qgtbb.target.name].remove(pzusf__qgtbb
                    .value)
                pzusf__qgtbb.value = ir.Const(False, pzusf__qgtbb.loc)
                f_ir._definitions[pzusf__qgtbb.target.name].append(pzusf__qgtbb
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    nsrj__hjx = numba.parfors.parfor.PreParforPass(f_ir, typemap, calltypes,
        typingctx, targetctx, hvv__hfgo)
    nsrj__hjx.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    dmj__xhmdm = numba.core.compiler.StateDict()
    dmj__xhmdm.func_ir = f_ir
    dmj__xhmdm.typemap = typemap
    dmj__xhmdm.calltypes = calltypes
    dmj__xhmdm.typingctx = typingctx
    dmj__xhmdm.targetctx = targetctx
    dmj__xhmdm.return_type = neq__dbra
    numba.core.rewrites.rewrite_registry.apply('after-inference', dmj__xhmdm)
    obusp__rjspy = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        neq__dbra, typingctx, targetctx, hvv__hfgo, jauly__jqp, {})
    obusp__rjspy.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            ems__iupmh = ctypes.pythonapi.PyCell_Get
            ems__iupmh.restype = ctypes.py_object
            ems__iupmh.argtypes = ctypes.py_object,
            tszmm__rrfcq = tuple(ems__iupmh(rjy__iten) for rjy__iten in closure
                )
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            tszmm__rrfcq = closure.items
        assert len(code.co_freevars) == len(tszmm__rrfcq)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks,
            tszmm__rrfcq)


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
        rofcq__ftv = SeriesType(in_col_typ.dtype, to_str_arr_if_dict_array(
            in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (rofcq__ftv,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        wphh__nnav, arr_var = _rm_arg_agg_block(block, pm.typemap)
        ekeg__jhosj = -1
        for hdsib__wxwd, pzusf__qgtbb in enumerate(wphh__nnav):
            if isinstance(pzusf__qgtbb, numba.parfors.parfor.Parfor):
                assert ekeg__jhosj == -1, 'only one parfor for aggregation function'
                ekeg__jhosj = hdsib__wxwd
        parfor = None
        if ekeg__jhosj != -1:
            parfor = wphh__nnav[ekeg__jhosj]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = wphh__nnav[:ekeg__jhosj] + parfor.init_block.body
        eval_nodes = wphh__nnav[ekeg__jhosj + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for pzusf__qgtbb in init_nodes:
            if is_assign(pzusf__qgtbb) and pzusf__qgtbb.target.name in redvars:
                ind = redvars.index(pzusf__qgtbb.target.name)
                reduce_vars[ind] = pzusf__qgtbb.target
        var_types = [pm.typemap[kjjfo__efvi] for kjjfo__efvi in redvars]
        ndz__eoj = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        bdpbk__dxhm = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        lgbx__zmypo = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(lgbx__zmypo)
        self.all_update_funcs.append(bdpbk__dxhm)
        self.all_combine_funcs.append(ndz__eoj)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        yzp__obr = gen_init_func(self.all_init_nodes, self.all_reduce_vars,
            self.all_vartypes, self.typingctx, self.targetctx)
        gpexe__fxtay = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        vegrq__ngni = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        dwrd__onqrr = gen_all_eval_func(self.all_eval_funcs, self.
            redvar_offsets)
        return (self.all_vartypes, yzp__obr, gpexe__fxtay, vegrq__ngni,
            dwrd__onqrr)


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
    tskba__wtrr = []
    for t, lraw__zje in zip(in_col_types, agg_func):
        tskba__wtrr.append((t, lraw__zje))
    unt__gcv = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    oaub__ejkb = GeneralUDFGenerator()
    for in_col_typ, func in tskba__wtrr:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            unt__gcv.add_udf(in_col_typ, func)
        except:
            oaub__ejkb.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = unt__gcv.gen_all_func()
    general_udf_funcs = oaub__ejkb.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    dsej__mcsjo = compute_use_defs(parfor.loop_body)
    sod__pahvt = set()
    for lot__vgj in dsej__mcsjo.usemap.values():
        sod__pahvt |= lot__vgj
    qqr__zxgjs = set()
    for lot__vgj in dsej__mcsjo.defmap.values():
        qqr__zxgjs |= lot__vgj
    wsp__pgnui = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    wsp__pgnui.body = eval_nodes
    zanm__ckbp = compute_use_defs({(0): wsp__pgnui})
    zlma__ojos = zanm__ckbp.usemap[0]
    gaqr__payt = set()
    kaami__ykkh = []
    hat__ycese = []
    for pzusf__qgtbb in reversed(init_nodes):
        cub__alj = {kjjfo__efvi.name for kjjfo__efvi in pzusf__qgtbb.
            list_vars()}
        if is_assign(pzusf__qgtbb):
            kjjfo__efvi = pzusf__qgtbb.target.name
            cub__alj.remove(kjjfo__efvi)
            if (kjjfo__efvi in sod__pahvt and kjjfo__efvi not in gaqr__payt and
                kjjfo__efvi not in zlma__ojos and kjjfo__efvi not in qqr__zxgjs
                ):
                hat__ycese.append(pzusf__qgtbb)
                sod__pahvt |= cub__alj
                qqr__zxgjs.add(kjjfo__efvi)
                continue
        gaqr__payt |= cub__alj
        kaami__ykkh.append(pzusf__qgtbb)
    hat__ycese.reverse()
    kaami__ykkh.reverse()
    xdf__lsggq = min(parfor.loop_body.keys())
    hja__iqk = parfor.loop_body[xdf__lsggq]
    hja__iqk.body = hat__ycese + hja__iqk.body
    return kaami__ykkh


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    pymgc__ssbow = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    bpyt__squpi = set()
    mmsb__yaurc = []
    for pzusf__qgtbb in init_nodes:
        if is_assign(pzusf__qgtbb) and isinstance(pzusf__qgtbb.value, ir.Global
            ) and isinstance(pzusf__qgtbb.value.value, pytypes.FunctionType
            ) and pzusf__qgtbb.value.value in pymgc__ssbow:
            bpyt__squpi.add(pzusf__qgtbb.target.name)
        elif is_call_assign(pzusf__qgtbb
            ) and pzusf__qgtbb.value.func.name in bpyt__squpi:
            pass
        else:
            mmsb__yaurc.append(pzusf__qgtbb)
    init_nodes = mmsb__yaurc
    ethja__rwzje = types.Tuple(var_types)
    gry__pqjei = lambda : None
    f_ir = compile_to_numba_ir(gry__pqjei, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    rruuy__hgksd = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    mdrg__oelte = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        rruuy__hgksd, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [mdrg__oelte] + block.body
    block.body[-2].value.value = rruuy__hgksd
    oqxl__mqtcf = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        ethja__rwzje, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    mcf__vvu = numba.core.target_extension.dispatcher_registry[cpu_target](
        gry__pqjei)
    mcf__vvu.add_overload(oqxl__mqtcf)
    return mcf__vvu


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    nme__qejbt = len(update_funcs)
    bodaj__iog = len(in_col_types)
    hpkem__vid = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for gwxg__mmqhl in range(nme__qejbt):
        pgs__vnl = ', '.join(['redvar_arrs[{}][w_ind]'.format(hdsib__wxwd) for
            hdsib__wxwd in range(redvar_offsets[gwxg__mmqhl],
            redvar_offsets[gwxg__mmqhl + 1])])
        if pgs__vnl:
            hpkem__vid += ('  {} = update_vars_{}({},  data_in[{}][i])\n'.
                format(pgs__vnl, gwxg__mmqhl, pgs__vnl, 0 if bodaj__iog == 
                1 else gwxg__mmqhl))
    hpkem__vid += '  return\n'
    jyh__ehmw = {}
    for hdsib__wxwd, lraw__zje in enumerate(update_funcs):
        jyh__ehmw['update_vars_{}'.format(hdsib__wxwd)] = lraw__zje
    memau__aakd = {}
    exec(hpkem__vid, jyh__ehmw, memau__aakd)
    ncgza__lwqep = memau__aakd['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(ncgza__lwqep)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    djeir__kbi = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = djeir__kbi, djeir__kbi, types.intp, types.intp
    nnklk__jglwb = len(redvar_offsets) - 1
    hpkem__vid = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for gwxg__mmqhl in range(nnklk__jglwb):
        pgs__vnl = ', '.join(['redvar_arrs[{}][w_ind]'.format(hdsib__wxwd) for
            hdsib__wxwd in range(redvar_offsets[gwxg__mmqhl],
            redvar_offsets[gwxg__mmqhl + 1])])
        mnjwf__bbrwg = ', '.join(['recv_arrs[{}][i]'.format(hdsib__wxwd) for
            hdsib__wxwd in range(redvar_offsets[gwxg__mmqhl],
            redvar_offsets[gwxg__mmqhl + 1])])
        if mnjwf__bbrwg:
            hpkem__vid += '  {} = combine_vars_{}({}, {})\n'.format(pgs__vnl,
                gwxg__mmqhl, pgs__vnl, mnjwf__bbrwg)
    hpkem__vid += '  return\n'
    jyh__ehmw = {}
    for hdsib__wxwd, lraw__zje in enumerate(combine_funcs):
        jyh__ehmw['combine_vars_{}'.format(hdsib__wxwd)] = lraw__zje
    memau__aakd = {}
    exec(hpkem__vid, jyh__ehmw, memau__aakd)
    zhajk__zagcp = memau__aakd['combine_all_f']
    f_ir = compile_to_numba_ir(zhajk__zagcp, jyh__ehmw)
    vegrq__ngni = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    mcf__vvu = numba.core.target_extension.dispatcher_registry[cpu_target](
        zhajk__zagcp)
    mcf__vvu.add_overload(vegrq__ngni)
    return mcf__vvu


def gen_all_eval_func(eval_funcs, redvar_offsets):
    nnklk__jglwb = len(redvar_offsets) - 1
    hpkem__vid = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for gwxg__mmqhl in range(nnklk__jglwb):
        pgs__vnl = ', '.join(['redvar_arrs[{}][j]'.format(hdsib__wxwd) for
            hdsib__wxwd in range(redvar_offsets[gwxg__mmqhl],
            redvar_offsets[gwxg__mmqhl + 1])])
        hpkem__vid += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
            gwxg__mmqhl, gwxg__mmqhl, pgs__vnl)
    hpkem__vid += '  return\n'
    jyh__ehmw = {}
    for hdsib__wxwd, lraw__zje in enumerate(eval_funcs):
        jyh__ehmw['eval_vars_{}'.format(hdsib__wxwd)] = lraw__zje
    memau__aakd = {}
    exec(hpkem__vid, jyh__ehmw, memau__aakd)
    dqny__pvab = memau__aakd['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(dqny__pvab)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    yff__neu = len(var_types)
    ffz__zhjt = [f'in{hdsib__wxwd}' for hdsib__wxwd in range(yff__neu)]
    ethja__rwzje = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    svd__botb = ethja__rwzje(0)
    hpkem__vid = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        ffz__zhjt))
    memau__aakd = {}
    exec(hpkem__vid, {'_zero': svd__botb}, memau__aakd)
    odf__vns = memau__aakd['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(odf__vns, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': svd__botb}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    qoh__libx = []
    for hdsib__wxwd, kjjfo__efvi in enumerate(reduce_vars):
        qoh__libx.append(ir.Assign(block.body[hdsib__wxwd].target,
            kjjfo__efvi, kjjfo__efvi.loc))
        for hazs__dykzh in kjjfo__efvi.versioned_names:
            qoh__libx.append(ir.Assign(kjjfo__efvi, ir.Var(kjjfo__efvi.
                scope, hazs__dykzh, kjjfo__efvi.loc), kjjfo__efvi.loc))
    block.body = block.body[:yff__neu] + qoh__libx + eval_nodes
    lgbx__zmypo = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ethja__rwzje, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    mcf__vvu = numba.core.target_extension.dispatcher_registry[cpu_target](
        odf__vns)
    mcf__vvu.add_overload(lgbx__zmypo)
    return mcf__vvu


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    yff__neu = len(redvars)
    mxjcc__bjkc = [f'v{hdsib__wxwd}' for hdsib__wxwd in range(yff__neu)]
    ffz__zhjt = [f'in{hdsib__wxwd}' for hdsib__wxwd in range(yff__neu)]
    hpkem__vid = 'def agg_combine({}):\n'.format(', '.join(mxjcc__bjkc +
        ffz__zhjt))
    inbsh__tvqn = wrap_parfor_blocks(parfor)
    cjs__apwa = find_topo_order(inbsh__tvqn)
    cjs__apwa = cjs__apwa[1:]
    unwrap_parfor_blocks(parfor)
    yyyww__fojd = {}
    jol__yjlwd = []
    for rfzod__nkq in cjs__apwa:
        vxf__kvct = parfor.loop_body[rfzod__nkq]
        for pzusf__qgtbb in vxf__kvct.body:
            if is_assign(pzusf__qgtbb) and pzusf__qgtbb.target.name in redvars:
                vxh__osncr = pzusf__qgtbb.target.name
                ind = redvars.index(vxh__osncr)
                if ind in jol__yjlwd:
                    continue
                if len(f_ir._definitions[vxh__osncr]) == 2:
                    var_def = f_ir._definitions[vxh__osncr][0]
                    hpkem__vid += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[vxh__osncr][1]
                    hpkem__vid += _match_reduce_def(var_def, f_ir, ind)
    hpkem__vid += '    return {}'.format(', '.join(['v{}'.format(
        hdsib__wxwd) for hdsib__wxwd in range(yff__neu)]))
    memau__aakd = {}
    exec(hpkem__vid, {}, memau__aakd)
    ywcm__wjri = memau__aakd['agg_combine']
    arg_typs = tuple(2 * var_types)
    jyh__ehmw = {'numba': numba, 'bodo': bodo, 'np': np}
    jyh__ehmw.update(yyyww__fojd)
    f_ir = compile_to_numba_ir(ywcm__wjri, jyh__ehmw, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    ethja__rwzje = pm.typemap[block.body[-1].value.name]
    ndz__eoj = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ethja__rwzje, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    mcf__vvu = numba.core.target_extension.dispatcher_registry[cpu_target](
        ywcm__wjri)
    mcf__vvu.add_overload(ndz__eoj)
    return mcf__vvu


def _match_reduce_def(var_def, f_ir, ind):
    hpkem__vid = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        hpkem__vid = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        lmtai__hqch = guard(find_callname, f_ir, var_def)
        if lmtai__hqch == ('min', 'builtins'):
            hpkem__vid = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if lmtai__hqch == ('max', 'builtins'):
            hpkem__vid = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return hpkem__vid


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    yff__neu = len(redvars)
    xxqr__omx = 1
    in_vars = []
    for hdsib__wxwd in range(xxqr__omx):
        hgjn__gylw = ir.Var(arr_var.scope, f'$input{hdsib__wxwd}', arr_var.loc)
        in_vars.append(hgjn__gylw)
    wfvb__txfva = parfor.loop_nests[0].index_variable
    lta__ctz = [0] * yff__neu
    for vxf__kvct in parfor.loop_body.values():
        rsb__tkvz = []
        for pzusf__qgtbb in vxf__kvct.body:
            if is_var_assign(pzusf__qgtbb
                ) and pzusf__qgtbb.value.name == wfvb__txfva.name:
                continue
            if is_getitem(pzusf__qgtbb
                ) and pzusf__qgtbb.value.value.name == arr_var.name:
                pzusf__qgtbb.value = in_vars[0]
            if is_call_assign(pzusf__qgtbb) and guard(find_callname, pm.
                func_ir, pzusf__qgtbb.value) == ('isna',
                'bodo.libs.array_kernels') and pzusf__qgtbb.value.args[0
                ].name == arr_var.name:
                pzusf__qgtbb.value = ir.Const(False, pzusf__qgtbb.target.loc)
            if is_assign(pzusf__qgtbb) and pzusf__qgtbb.target.name in redvars:
                ind = redvars.index(pzusf__qgtbb.target.name)
                lta__ctz[ind] = pzusf__qgtbb.target
            rsb__tkvz.append(pzusf__qgtbb)
        vxf__kvct.body = rsb__tkvz
    mxjcc__bjkc = ['v{}'.format(hdsib__wxwd) for hdsib__wxwd in range(yff__neu)
        ]
    ffz__zhjt = ['in{}'.format(hdsib__wxwd) for hdsib__wxwd in range(xxqr__omx)
        ]
    hpkem__vid = 'def agg_update({}):\n'.format(', '.join(mxjcc__bjkc +
        ffz__zhjt))
    hpkem__vid += '    __update_redvars()\n'
    hpkem__vid += '    return {}'.format(', '.join(['v{}'.format(
        hdsib__wxwd) for hdsib__wxwd in range(yff__neu)]))
    memau__aakd = {}
    exec(hpkem__vid, {}, memau__aakd)
    vmfrq__ysmgf = memau__aakd['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * xxqr__omx)
    f_ir = compile_to_numba_ir(vmfrq__ysmgf, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    amlwi__xkxd = f_ir.blocks.popitem()[1].body
    ethja__rwzje = pm.typemap[amlwi__xkxd[-1].value.name]
    inbsh__tvqn = wrap_parfor_blocks(parfor)
    cjs__apwa = find_topo_order(inbsh__tvqn)
    cjs__apwa = cjs__apwa[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    hja__iqk = f_ir.blocks[cjs__apwa[0]]
    aqly__yegia = f_ir.blocks[cjs__apwa[-1]]
    run__bwzu = amlwi__xkxd[:yff__neu + xxqr__omx]
    if yff__neu > 1:
        mka__iettx = amlwi__xkxd[-3:]
        assert is_assign(mka__iettx[0]) and isinstance(mka__iettx[0].value,
            ir.Expr) and mka__iettx[0].value.op == 'build_tuple'
    else:
        mka__iettx = amlwi__xkxd[-2:]
    for hdsib__wxwd in range(yff__neu):
        vsszi__mfbi = amlwi__xkxd[hdsib__wxwd].target
        xyrdm__zdez = ir.Assign(vsszi__mfbi, lta__ctz[hdsib__wxwd],
            vsszi__mfbi.loc)
        run__bwzu.append(xyrdm__zdez)
    for hdsib__wxwd in range(yff__neu, yff__neu + xxqr__omx):
        vsszi__mfbi = amlwi__xkxd[hdsib__wxwd].target
        xyrdm__zdez = ir.Assign(vsszi__mfbi, in_vars[hdsib__wxwd - yff__neu
            ], vsszi__mfbi.loc)
        run__bwzu.append(xyrdm__zdez)
    hja__iqk.body = run__bwzu + hja__iqk.body
    qqk__ihq = []
    for hdsib__wxwd in range(yff__neu):
        vsszi__mfbi = amlwi__xkxd[hdsib__wxwd].target
        xyrdm__zdez = ir.Assign(lta__ctz[hdsib__wxwd], vsszi__mfbi,
            vsszi__mfbi.loc)
        qqk__ihq.append(xyrdm__zdez)
    aqly__yegia.body += qqk__ihq + mka__iettx
    fgbaz__puka = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ethja__rwzje, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    mcf__vvu = numba.core.target_extension.dispatcher_registry[cpu_target](
        vmfrq__ysmgf)
    mcf__vvu.add_overload(fgbaz__puka)
    return mcf__vvu


def _rm_arg_agg_block(block, typemap):
    wphh__nnav = []
    arr_var = None
    for hdsib__wxwd, pzusf__qgtbb in enumerate(block.body):
        if is_assign(pzusf__qgtbb) and isinstance(pzusf__qgtbb.value, ir.Arg):
            arr_var = pzusf__qgtbb.target
            iirb__bcym = typemap[arr_var.name]
            if not isinstance(iirb__bcym, types.ArrayCompatible):
                wphh__nnav += block.body[hdsib__wxwd + 1:]
                break
            lej__cta = block.body[hdsib__wxwd + 1]
            assert is_assign(lej__cta) and isinstance(lej__cta.value, ir.Expr
                ) and lej__cta.value.op == 'getattr' and lej__cta.value.attr == 'shape' and lej__cta.value.value.name == arr_var.name
            uepv__kzx = lej__cta.target
            kldd__kcci = block.body[hdsib__wxwd + 2]
            assert is_assign(kldd__kcci) and isinstance(kldd__kcci.value,
                ir.Expr
                ) and kldd__kcci.value.op == 'static_getitem' and kldd__kcci.value.value.name == uepv__kzx.name
            wphh__nnav += block.body[hdsib__wxwd + 3:]
            break
        wphh__nnav.append(pzusf__qgtbb)
    return wphh__nnav, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    inbsh__tvqn = wrap_parfor_blocks(parfor)
    cjs__apwa = find_topo_order(inbsh__tvqn)
    cjs__apwa = cjs__apwa[1:]
    unwrap_parfor_blocks(parfor)
    for rfzod__nkq in reversed(cjs__apwa):
        for pzusf__qgtbb in reversed(parfor.loop_body[rfzod__nkq].body):
            if isinstance(pzusf__qgtbb, ir.Assign) and (pzusf__qgtbb.target
                .name in parfor_params or pzusf__qgtbb.target.name in
                var_to_param):
                fzjw__lzgnr = pzusf__qgtbb.target.name
                rhs = pzusf__qgtbb.value
                lfogn__wigbt = (fzjw__lzgnr if fzjw__lzgnr in parfor_params
                     else var_to_param[fzjw__lzgnr])
                sbmse__dfvpf = []
                if isinstance(rhs, ir.Var):
                    sbmse__dfvpf = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    sbmse__dfvpf = [kjjfo__efvi.name for kjjfo__efvi in
                        pzusf__qgtbb.value.list_vars()]
                param_uses[lfogn__wigbt].extend(sbmse__dfvpf)
                for kjjfo__efvi in sbmse__dfvpf:
                    var_to_param[kjjfo__efvi] = lfogn__wigbt
            if isinstance(pzusf__qgtbb, Parfor):
                get_parfor_reductions(pzusf__qgtbb, parfor_params,
                    calltypes, reduce_varnames, param_uses, var_to_param)
    for vkp__tycem, sbmse__dfvpf in param_uses.items():
        if vkp__tycem in sbmse__dfvpf and vkp__tycem not in reduce_varnames:
            reduce_varnames.append(vkp__tycem)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
