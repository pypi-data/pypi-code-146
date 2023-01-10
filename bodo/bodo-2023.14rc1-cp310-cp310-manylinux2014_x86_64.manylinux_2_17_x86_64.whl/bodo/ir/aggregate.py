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
        uqml__yoma = func.signature
        if uqml__yoma == types.none(types.voidptr):
            frohy__ssnsp = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer()])
            dzra__majs = cgutils.get_or_insert_function(builder.module,
                frohy__ssnsp, sym._literal_value)
            builder.call(dzra__majs, [context.get_constant_null(uqml__yoma.
                args[0])])
        elif uqml__yoma == types.none(types.int64, types.voidptr, types.voidptr
            ):
            frohy__ssnsp = lir.FunctionType(lir.VoidType(), [lir.IntType(64
                ), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            dzra__majs = cgutils.get_or_insert_function(builder.module,
                frohy__ssnsp, sym._literal_value)
            builder.call(dzra__majs, [context.get_constant(types.int64, 0),
                context.get_constant_null(uqml__yoma.args[1]), context.
                get_constant_null(uqml__yoma.args[2])])
        else:
            frohy__ssnsp = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)
                .as_pointer()])
            dzra__majs = cgutils.get_or_insert_function(builder.module,
                frohy__ssnsp, sym._literal_value)
            builder.call(dzra__majs, [context.get_constant_null(uqml__yoma.
                args[0]), context.get_constant_null(uqml__yoma.args[1]),
                context.get_constant_null(uqml__yoma.args[2])])
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
        jun__ffws = True
        rjkvm__xsc = 1
        xds__ggi = -1
        if isinstance(rhs, ir.Expr):
            for zfgy__nua in rhs.kws:
                if func_name in list_cumulative:
                    if zfgy__nua[0] == 'skipna':
                        jun__ffws = guard(find_const, func_ir, zfgy__nua[1])
                        if not isinstance(jun__ffws, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if zfgy__nua[0] == 'dropna':
                        jun__ffws = guard(find_const, func_ir, zfgy__nua[1])
                        if not isinstance(jun__ffws, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            rjkvm__xsc = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', rjkvm__xsc)
            rjkvm__xsc = guard(find_const, func_ir, rjkvm__xsc)
        if func_name == 'head':
            xds__ggi = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 0,
                'n', 5)
            if not isinstance(xds__ggi, int):
                xds__ggi = guard(find_const, func_ir, xds__ggi)
            if xds__ggi < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = jun__ffws
        func.periods = rjkvm__xsc
        func.head_n = xds__ggi
        if func_name == 'transform':
            kws = dict(rhs.kws)
            hjb__aik = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            dpxh__ikkqg = typemap[hjb__aik.name]
            qvs__qrst = None
            if isinstance(dpxh__ikkqg, str):
                qvs__qrst = dpxh__ikkqg
            elif is_overload_constant_str(dpxh__ikkqg):
                qvs__qrst = get_overload_const_str(dpxh__ikkqg)
            elif bodo.utils.typing.is_builtin_function(dpxh__ikkqg):
                qvs__qrst = bodo.utils.typing.get_builtin_function_name(
                    dpxh__ikkqg)
            if qvs__qrst not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {qvs__qrst}')
            func.transform_func = supported_agg_funcs.index(qvs__qrst)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    hjb__aik = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if hjb__aik == '':
        dpxh__ikkqg = types.none
    else:
        dpxh__ikkqg = typemap[hjb__aik.name]
    if is_overload_constant_dict(dpxh__ikkqg):
        rim__osvr = get_overload_constant_dict(dpxh__ikkqg)
        sktw__jecg = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in rim__osvr.values()]
        return sktw__jecg
    if dpxh__ikkqg == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(dpxh__ikkqg, types.BaseTuple) or is_overload_constant_list(
        dpxh__ikkqg):
        sktw__jecg = []
        ylgl__cyzh = 0
        if is_overload_constant_list(dpxh__ikkqg):
            imb__yazqq = get_overload_const_list(dpxh__ikkqg)
        else:
            imb__yazqq = dpxh__ikkqg.types
        for t in imb__yazqq:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                sktw__jecg.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(imb__yazqq) > 1:
                    func.fname = '<lambda_' + str(ylgl__cyzh) + '>'
                    ylgl__cyzh += 1
                sktw__jecg.append(func)
        return [sktw__jecg]
    if is_overload_constant_str(dpxh__ikkqg):
        func_name = get_overload_const_str(dpxh__ikkqg)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(dpxh__ikkqg):
        func_name = bodo.utils.typing.get_builtin_function_name(dpxh__ikkqg)
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
        ylgl__cyzh = 0
        jocx__iaaz = []
        for ohtf__lyzj in f_val:
            func = get_agg_func_udf(func_ir, ohtf__lyzj, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{ylgl__cyzh}>'
                ylgl__cyzh += 1
            jocx__iaaz.append(func)
        return jocx__iaaz
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
    qvs__qrst = code.co_name
    return qvs__qrst


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
            iff__hswwt = types.DType(args[0])
            return signature(iff__hswwt, *args)


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
        return [gqsh__rkccx for gqsh__rkccx in self.in_vars if gqsh__rkccx
             is not None]

    def get_live_out_vars(self):
        return [gqsh__rkccx for gqsh__rkccx in self.out_vars if gqsh__rkccx
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
        snehv__thpp = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        dzxh__mxrax = list(get_index_data_arr_types(self.out_type.index))
        return snehv__thpp + dzxh__mxrax

    def update_dead_col_info(self):
        for bvo__vuyd in self.dead_out_inds:
            self.gb_info_out.pop(bvo__vuyd, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for otilq__pvvgq, dvnm__nflct in self.gb_info_in.copy().items():
            gary__cic = []
            for ohtf__lyzj, fysy__piqw in dvnm__nflct:
                if fysy__piqw not in self.dead_out_inds:
                    gary__cic.append((ohtf__lyzj, fysy__piqw))
            if not gary__cic:
                if (otilq__pvvgq is not None and otilq__pvvgq not in self.
                    in_key_inds):
                    self.dead_in_inds.add(otilq__pvvgq)
                self.gb_info_in.pop(otilq__pvvgq)
            else:
                self.gb_info_in[otilq__pvvgq] = gary__cic
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for nzuew__ywu in range(1, len(self.in_vars)):
                bvo__vuyd = self.n_in_table_arrays + nzuew__ywu - 1
                if bvo__vuyd in self.dead_in_inds:
                    self.in_vars[nzuew__ywu] = None
        else:
            for nzuew__ywu in range(len(self.in_vars)):
                if nzuew__ywu in self.dead_in_inds:
                    self.in_vars[nzuew__ywu] = None

    def __repr__(self):
        uttt__zoi = ', '.join(gqsh__rkccx.name for gqsh__rkccx in self.
            get_live_in_vars())
        ffisp__kpc = f'{self.df_in}{{{uttt__zoi}}}'
        ybue__lmr = ', '.join(gqsh__rkccx.name for gqsh__rkccx in self.
            get_live_out_vars())
        rpq__rkjtn = f'{self.df_out}{{{ybue__lmr}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {ffisp__kpc} {rpq__rkjtn}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({gqsh__rkccx.name for gqsh__rkccx in aggregate_node.
        get_live_in_vars()})
    def_set.update({gqsh__rkccx.name for gqsh__rkccx in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    tsc__gkf = agg_node.out_vars[0]
    if tsc__gkf is not None and tsc__gkf.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            qmbzo__ycozm = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(qmbzo__ycozm)
        else:
            agg_node.dead_out_inds.add(0)
    for nzuew__ywu in range(1, len(agg_node.out_vars)):
        gqsh__rkccx = agg_node.out_vars[nzuew__ywu]
        if gqsh__rkccx is not None and gqsh__rkccx.name not in lives:
            agg_node.out_vars[nzuew__ywu] = None
            bvo__vuyd = agg_node.n_out_table_arrays + nzuew__ywu - 1
            agg_node.dead_out_inds.add(bvo__vuyd)
    if all(gqsh__rkccx is None for gqsh__rkccx in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    ran__fwbv = {gqsh__rkccx.name for gqsh__rkccx in aggregate_node.
        get_live_out_vars()}
    return set(), ran__fwbv


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for nzuew__ywu in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[nzuew__ywu] is not None:
            aggregate_node.in_vars[nzuew__ywu] = replace_vars_inner(
                aggregate_node.in_vars[nzuew__ywu], var_dict)
    for nzuew__ywu in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[nzuew__ywu] is not None:
            aggregate_node.out_vars[nzuew__ywu] = replace_vars_inner(
                aggregate_node.out_vars[nzuew__ywu], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for nzuew__ywu in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[nzuew__ywu] is not None:
            aggregate_node.in_vars[nzuew__ywu] = visit_vars_inner(
                aggregate_node.in_vars[nzuew__ywu], callback, cbdata)
    for nzuew__ywu in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[nzuew__ywu] is not None:
            aggregate_node.out_vars[nzuew__ywu] = visit_vars_inner(
                aggregate_node.out_vars[nzuew__ywu], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    tcet__dfncj = []
    for skytn__hcyri in aggregate_node.get_live_in_vars():
        fcys__erejp = equiv_set.get_shape(skytn__hcyri)
        if fcys__erejp is not None:
            tcet__dfncj.append(fcys__erejp[0])
    if len(tcet__dfncj) > 1:
        equiv_set.insert_equiv(*tcet__dfncj)
    njn__qsu = []
    tcet__dfncj = []
    for skytn__hcyri in aggregate_node.get_live_out_vars():
        okk__vpvrj = typemap[skytn__hcyri.name]
        zlk__cgqlj = array_analysis._gen_shape_call(equiv_set, skytn__hcyri,
            okk__vpvrj.ndim, None, njn__qsu)
        equiv_set.insert_equiv(skytn__hcyri, zlk__cgqlj)
        tcet__dfncj.append(zlk__cgqlj[0])
        equiv_set.define(skytn__hcyri, set())
    if len(tcet__dfncj) > 1:
        equiv_set.insert_equiv(*tcet__dfncj)
    return [], njn__qsu


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    jxvac__fod = aggregate_node.get_live_in_vars()
    uczxl__jxiws = aggregate_node.get_live_out_vars()
    dxs__xjob = Distribution.OneD
    for skytn__hcyri in jxvac__fod:
        dxs__xjob = Distribution(min(dxs__xjob.value, array_dists[
            skytn__hcyri.name].value))
    sdhw__hzb = Distribution(min(dxs__xjob.value, Distribution.OneD_Var.value))
    for skytn__hcyri in uczxl__jxiws:
        if skytn__hcyri.name in array_dists:
            sdhw__hzb = Distribution(min(sdhw__hzb.value, array_dists[
                skytn__hcyri.name].value))
    if sdhw__hzb != Distribution.OneD_Var:
        dxs__xjob = sdhw__hzb
    for skytn__hcyri in jxvac__fod:
        array_dists[skytn__hcyri.name] = dxs__xjob
    for skytn__hcyri in uczxl__jxiws:
        array_dists[skytn__hcyri.name] = sdhw__hzb


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for skytn__hcyri in agg_node.get_live_out_vars():
        definitions[skytn__hcyri.name].append(agg_node)
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
    fwbgu__lsu = agg_node.get_live_in_vars()
    rmdw__fqpf = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for gqsh__rkccx in (fwbgu__lsu + rmdw__fqpf):
            if array_dists[gqsh__rkccx.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                gqsh__rkccx.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    sktw__jecg = []
    func_out_types = []
    for fysy__piqw, (otilq__pvvgq, func) in agg_node.gb_info_out.items():
        if otilq__pvvgq is not None:
            t = agg_node.in_col_types[otilq__pvvgq]
            in_col_typs.append(t)
        sktw__jecg.append(func)
        func_out_types.append(out_col_typs[fysy__piqw])
    cazx__rdz = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for nzuew__ywu, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            cazx__rdz.update({f'in_cat_dtype_{nzuew__ywu}': in_col_typ})
    for nzuew__ywu, xhqip__sleel in enumerate(out_col_typs):
        if isinstance(xhqip__sleel, bodo.CategoricalArrayType):
            cazx__rdz.update({f'out_cat_dtype_{nzuew__ywu}': xhqip__sleel})
    udf_func_struct = get_udf_func_struct(sktw__jecg, in_col_typs,
        typingctx, targetctx)
    out_var_types = [(typemap[gqsh__rkccx.name] if gqsh__rkccx is not None else
        types.none) for gqsh__rkccx in agg_node.out_vars]
    dqr__ebl, ofjzq__lugwc = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, func_out_types, parallel, udf_func_struct,
        out_var_types, typemap)
    cazx__rdz.update(ofjzq__lugwc)
    cazx__rdz.update({'pd': pd, 'pre_alloc_string_array':
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
            cazx__rdz.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            cazx__rdz.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    nytuy__msz = {}
    exec(dqr__ebl, {}, nytuy__msz)
    wxb__brs = nytuy__msz['agg_top']
    tphzq__dktrk = compile_to_numba_ir(wxb__brs, cazx__rdz, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[gqsh__rkccx.
        name] for gqsh__rkccx in fwbgu__lsu), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(tphzq__dktrk, fwbgu__lsu)
    ilea__ijq = tphzq__dktrk.body[-2].value.value
    bhah__cdvh = tphzq__dktrk.body[:-2]
    for nzuew__ywu, gqsh__rkccx in enumerate(rmdw__fqpf):
        gen_getitem(gqsh__rkccx, ilea__ijq, nzuew__ywu, calltypes, bhah__cdvh)
    return bhah__cdvh


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        yyu__nwyt = IntDtype(t.dtype).name
        assert yyu__nwyt.endswith('Dtype()')
        yyu__nwyt = yyu__nwyt[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{yyu__nwyt}'))"
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
        uxn__voh = 'in' if is_input else 'out'
        return f'bodo.utils.utils.alloc_type(1, {uxn__voh}_cat_dtype_{colnum})'
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
    esz__svlo = udf_func_struct.var_typs
    nos__qzt = len(esz__svlo)
    dqr__ebl = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    dqr__ebl += '    if is_null_pointer(in_table):\n'
    dqr__ebl += '        return\n'
    dqr__ebl += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in esz__svlo]), 
        ',' if len(esz__svlo) == 1 else '')
    damsp__jza = n_keys
    wexd__vjl = []
    redvar_offsets = []
    fmv__uiy = []
    if do_combine:
        for nzuew__ywu, ohtf__lyzj in enumerate(allfuncs):
            if ohtf__lyzj.ftype != 'udf':
                damsp__jza += ohtf__lyzj.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(damsp__jza, damsp__jza +
                    ohtf__lyzj.n_redvars))
                damsp__jza += ohtf__lyzj.n_redvars
                fmv__uiy.append(data_in_typs_[func_idx_to_in_col[nzuew__ywu]])
                wexd__vjl.append(func_idx_to_in_col[nzuew__ywu] + n_keys)
    else:
        for nzuew__ywu, ohtf__lyzj in enumerate(allfuncs):
            if ohtf__lyzj.ftype != 'udf':
                damsp__jza += ohtf__lyzj.ncols_post_shuffle
            else:
                redvar_offsets += list(range(damsp__jza + 1, damsp__jza + 1 +
                    ohtf__lyzj.n_redvars))
                damsp__jza += ohtf__lyzj.n_redvars + 1
                fmv__uiy.append(data_in_typs_[func_idx_to_in_col[nzuew__ywu]])
                wexd__vjl.append(func_idx_to_in_col[nzuew__ywu] + n_keys)
    assert len(redvar_offsets) == nos__qzt
    wge__wshh = len(fmv__uiy)
    logbq__qldz = []
    for nzuew__ywu, t in enumerate(fmv__uiy):
        logbq__qldz.append(_gen_dummy_alloc(t, nzuew__ywu, True))
    dqr__ebl += '    data_in_dummy = ({}{})\n'.format(','.join(logbq__qldz),
        ',' if len(fmv__uiy) == 1 else '')
    dqr__ebl += """
    # initialize redvar cols
"""
    dqr__ebl += '    init_vals = __init_func()\n'
    for nzuew__ywu in range(nos__qzt):
        dqr__ebl += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(nzuew__ywu, redvar_offsets[nzuew__ywu], nzuew__ywu))
        dqr__ebl += '    incref(redvar_arr_{})\n'.format(nzuew__ywu)
        dqr__ebl += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(nzuew__ywu
            , nzuew__ywu)
    dqr__ebl += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(nzuew__ywu) for nzuew__ywu in range(nos__qzt)]), ',' if 
        nos__qzt == 1 else '')
    dqr__ebl += '\n'
    for nzuew__ywu in range(wge__wshh):
        dqr__ebl += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(nzuew__ywu, wexd__vjl[nzuew__ywu], nzuew__ywu))
        dqr__ebl += '    incref(data_in_{})\n'.format(nzuew__ywu)
    dqr__ebl += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(nzuew__ywu) for nzuew__ywu in range(wge__wshh)]), ',' if 
        wge__wshh == 1 else '')
    dqr__ebl += '\n'
    dqr__ebl += '    for i in range(len(data_in_0)):\n'
    dqr__ebl += '        w_ind = row_to_group[i]\n'
    dqr__ebl += '        if w_ind != -1:\n'
    dqr__ebl += '            __update_redvars(redvars, data_in, w_ind, i)\n'
    nytuy__msz = {}
    exec(dqr__ebl, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, nytuy__msz)
    return nytuy__msz['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    esz__svlo = udf_func_struct.var_typs
    nos__qzt = len(esz__svlo)
    dqr__ebl = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    dqr__ebl += '    if is_null_pointer(in_table):\n'
    dqr__ebl += '        return\n'
    dqr__ebl += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in esz__svlo]), 
        ',' if len(esz__svlo) == 1 else '')
    ziwyu__fix = n_keys
    inbzd__prnz = n_keys
    rov__fhy = []
    azono__bcm = []
    for ohtf__lyzj in allfuncs:
        if ohtf__lyzj.ftype != 'udf':
            ziwyu__fix += ohtf__lyzj.ncols_pre_shuffle
            inbzd__prnz += ohtf__lyzj.ncols_post_shuffle
        else:
            rov__fhy += list(range(ziwyu__fix, ziwyu__fix + ohtf__lyzj.
                n_redvars))
            azono__bcm += list(range(inbzd__prnz + 1, inbzd__prnz + 1 +
                ohtf__lyzj.n_redvars))
            ziwyu__fix += ohtf__lyzj.n_redvars
            inbzd__prnz += 1 + ohtf__lyzj.n_redvars
    assert len(rov__fhy) == nos__qzt
    dqr__ebl += """
    # initialize redvar cols
"""
    dqr__ebl += '    init_vals = __init_func()\n'
    for nzuew__ywu in range(nos__qzt):
        dqr__ebl += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(nzuew__ywu, azono__bcm[nzuew__ywu], nzuew__ywu))
        dqr__ebl += '    incref(redvar_arr_{})\n'.format(nzuew__ywu)
        dqr__ebl += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(nzuew__ywu
            , nzuew__ywu)
    dqr__ebl += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(nzuew__ywu) for nzuew__ywu in range(nos__qzt)]), ',' if 
        nos__qzt == 1 else '')
    dqr__ebl += '\n'
    for nzuew__ywu in range(nos__qzt):
        dqr__ebl += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(nzuew__ywu, rov__fhy[nzuew__ywu], nzuew__ywu))
        dqr__ebl += '    incref(recv_redvar_arr_{})\n'.format(nzuew__ywu)
    dqr__ebl += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(nzuew__ywu) for nzuew__ywu in range(
        nos__qzt)]), ',' if nos__qzt == 1 else '')
    dqr__ebl += '\n'
    if nos__qzt:
        dqr__ebl += '    for i in range(len(recv_redvar_arr_0)):\n'
        dqr__ebl += '        w_ind = row_to_group[i]\n'
        dqr__ebl += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    nytuy__msz = {}
    exec(dqr__ebl, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, nytuy__msz)
    return nytuy__msz['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    esz__svlo = udf_func_struct.var_typs
    nos__qzt = len(esz__svlo)
    damsp__jza = n_keys
    redvar_offsets = []
    bgk__aolf = []
    fvpgs__xasx = []
    for nzuew__ywu, ohtf__lyzj in enumerate(allfuncs):
        if ohtf__lyzj.ftype != 'udf':
            damsp__jza += ohtf__lyzj.ncols_post_shuffle
        else:
            bgk__aolf.append(damsp__jza)
            redvar_offsets += list(range(damsp__jza + 1, damsp__jza + 1 +
                ohtf__lyzj.n_redvars))
            damsp__jza += 1 + ohtf__lyzj.n_redvars
            fvpgs__xasx.append(out_data_typs_[nzuew__ywu])
    assert len(redvar_offsets) == nos__qzt
    wge__wshh = len(fvpgs__xasx)
    dqr__ebl = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    dqr__ebl += '    if is_null_pointer(table):\n'
    dqr__ebl += '        return\n'
    dqr__ebl += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in esz__svlo]), 
        ',' if len(esz__svlo) == 1 else '')
    dqr__ebl += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        fvpgs__xasx]), ',' if len(fvpgs__xasx) == 1 else '')
    for nzuew__ywu in range(nos__qzt):
        dqr__ebl += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(nzuew__ywu, redvar_offsets[nzuew__ywu], nzuew__ywu))
        dqr__ebl += '    incref(redvar_arr_{})\n'.format(nzuew__ywu)
    dqr__ebl += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(nzuew__ywu) for nzuew__ywu in range(nos__qzt)]), ',' if 
        nos__qzt == 1 else '')
    dqr__ebl += '\n'
    for nzuew__ywu in range(wge__wshh):
        dqr__ebl += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(nzuew__ywu, bgk__aolf[nzuew__ywu], nzuew__ywu))
        dqr__ebl += '    incref(data_out_{})\n'.format(nzuew__ywu)
    dqr__ebl += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(nzuew__ywu) for nzuew__ywu in range(wge__wshh)]), ',' if 
        wge__wshh == 1 else '')
    dqr__ebl += '\n'
    dqr__ebl += '    for i in range(len(data_out_0)):\n'
    dqr__ebl += '        __eval_res(redvars, data_out, i)\n'
    nytuy__msz = {}
    exec(dqr__ebl, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, nytuy__msz)
    return nytuy__msz['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    damsp__jza = n_keys
    sodp__bcgv = []
    for nzuew__ywu, ohtf__lyzj in enumerate(allfuncs):
        if ohtf__lyzj.ftype == 'gen_udf':
            sodp__bcgv.append(damsp__jza)
            damsp__jza += 1
        elif ohtf__lyzj.ftype != 'udf':
            damsp__jza += ohtf__lyzj.ncols_post_shuffle
        else:
            damsp__jza += ohtf__lyzj.n_redvars + 1
    dqr__ebl = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    dqr__ebl += '    if num_groups == 0:\n'
    dqr__ebl += '        return\n'
    for nzuew__ywu, func in enumerate(udf_func_struct.general_udf_funcs):
        dqr__ebl += '    # col {}\n'.format(nzuew__ywu)
        dqr__ebl += (
            '    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)\n'
            .format(sodp__bcgv[nzuew__ywu], nzuew__ywu))
        dqr__ebl += '    incref(out_col)\n'
        dqr__ebl += '    for j in range(num_groups):\n'
        dqr__ebl += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(nzuew__ywu, nzuew__ywu))
        dqr__ebl += '        incref(in_col)\n'
        dqr__ebl += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(nzuew__ywu))
    cazx__rdz = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    rmzd__zinfd = 0
    for nzuew__ywu, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[rmzd__zinfd]
        cazx__rdz['func_{}'.format(rmzd__zinfd)] = func
        cazx__rdz['in_col_{}_typ'.format(rmzd__zinfd)] = in_col_typs[
            func_idx_to_in_col[nzuew__ywu]]
        cazx__rdz['out_col_{}_typ'.format(rmzd__zinfd)] = out_col_typs[
            nzuew__ywu]
        rmzd__zinfd += 1
    nytuy__msz = {}
    exec(dqr__ebl, cazx__rdz, nytuy__msz)
    ohtf__lyzj = nytuy__msz['bodo_gb_apply_general_udfs{}'.format(label_suffix)
        ]
    pokpt__cvduk = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(pokpt__cvduk, nopython=True)(ohtf__lyzj)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    okhn__ccacc = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        uwfq__gtj = []
        if agg_node.in_vars[0] is not None:
            uwfq__gtj.append('arg0')
        for nzuew__ywu in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if nzuew__ywu not in agg_node.dead_in_inds:
                uwfq__gtj.append(f'arg{nzuew__ywu}')
    else:
        uwfq__gtj = [f'arg{nzuew__ywu}' for nzuew__ywu, gqsh__rkccx in
            enumerate(agg_node.in_vars) if gqsh__rkccx is not None]
    dqr__ebl = f"def agg_top({', '.join(uwfq__gtj)}):\n"
    xnkar__lykc = []
    if agg_node.is_in_table_format:
        xnkar__lykc = agg_node.in_key_inds + [otilq__pvvgq for otilq__pvvgq,
            jjmz__rin in agg_node.gb_info_out.values() if otilq__pvvgq is not
            None]
        if agg_node.input_has_index:
            xnkar__lykc.append(agg_node.n_in_cols - 1)
        vjgvd__knyzh = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        xtfhq__ayoeo = []
        for nzuew__ywu in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if nzuew__ywu in agg_node.dead_in_inds:
                xtfhq__ayoeo.append('None')
            else:
                xtfhq__ayoeo.append(f'arg{nzuew__ywu}')
        zkrgu__grb = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        dqr__ebl += f"""    table = py_data_to_cpp_table({zkrgu__grb}, ({', '.join(xtfhq__ayoeo)}{vjgvd__knyzh}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        sna__weyn = [f'arg{nzuew__ywu}' for nzuew__ywu in agg_node.in_key_inds]
        thas__rda = [f'arg{otilq__pvvgq}' for otilq__pvvgq, jjmz__rin in
            agg_node.gb_info_out.values() if otilq__pvvgq is not None]
        fbdgc__kizls = sna__weyn + thas__rda
        if agg_node.input_has_index:
            fbdgc__kizls.append(f'arg{len(agg_node.in_vars) - 1}')
        dqr__ebl += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({smp__bkjk})' for smp__bkjk in fbdgc__kizls))
        dqr__ebl += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    ybv__acfd = []
    func_idx_to_in_col = []
    yhu__ssrh = []
    jun__ffws = False
    agqrj__uvpp = 1
    xds__ggi = -1
    nnhsu__grasl = 0
    wqgxr__excv = 0
    sktw__jecg = [func for jjmz__rin, func in agg_node.gb_info_out.values()]
    for awl__mpnfs, func in enumerate(sktw__jecg):
        ybv__acfd.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            nnhsu__grasl += 1
        if hasattr(func, 'skipdropna'):
            jun__ffws = func.skipdropna
        if func.ftype == 'shift':
            agqrj__uvpp = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            wqgxr__excv = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            xds__ggi = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(awl__mpnfs)
        if func.ftype == 'udf':
            yhu__ssrh.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            yhu__ssrh.append(0)
            do_combine = False
    ybv__acfd.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if nnhsu__grasl > 0:
        if nnhsu__grasl != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    tznt__ycrlu = []
    if udf_func_struct is not None:
        romqf__dupp = next_label()
        if udf_func_struct.regular_udfs:
            pokpt__cvduk = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            xwb__xrs = numba.cfunc(pokpt__cvduk, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs, do_combine,
                func_idx_to_in_col, romqf__dupp))
            zno__sca = numba.cfunc(pokpt__cvduk, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, romqf__dupp))
            ofpc__knb = numba.cfunc('void(voidptr)', nopython=True)(gen_eval_cb
                (udf_func_struct, allfuncs, n_keys, func_out_types,
                romqf__dupp))
            udf_func_struct.set_regular_cfuncs(xwb__xrs, zno__sca, ofpc__knb)
            for jnaom__gctq in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[jnaom__gctq.native_name] = jnaom__gctq
                gb_agg_cfunc_addr[jnaom__gctq.native_name
                    ] = jnaom__gctq.address
        if udf_func_struct.general_udfs:
            rdzf__ravgl = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, func_out_types, func_idx_to_in_col,
                romqf__dupp)
            udf_func_struct.set_general_cfunc(rdzf__ravgl)
        esz__svlo = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        bayg__nuhh = 0
        nzuew__ywu = 0
        for howy__nor, ohtf__lyzj in zip(agg_node.gb_info_out.keys(), allfuncs
            ):
            if ohtf__lyzj.ftype in ('udf', 'gen_udf'):
                tznt__ycrlu.append(out_col_typs[howy__nor])
                for pws__ndlzm in range(bayg__nuhh, bayg__nuhh + yhu__ssrh[
                    nzuew__ywu]):
                    tznt__ycrlu.append(dtype_to_array_type(esz__svlo[
                        pws__ndlzm]))
                bayg__nuhh += yhu__ssrh[nzuew__ywu]
                nzuew__ywu += 1
        dqr__ebl += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{nzuew__ywu}' for nzuew__ywu in range(len(tznt__ycrlu)))}{',' if len(tznt__ycrlu) == 1 else ''}))
"""
        dqr__ebl += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(tznt__ycrlu)})
"""
        if udf_func_struct.regular_udfs:
            dqr__ebl += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{xwb__xrs.native_name}')\n"
                )
            dqr__ebl += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{zno__sca.native_name}')\n"
                )
            dqr__ebl += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{ofpc__knb.native_name}')\n"
                )
            dqr__ebl += (
                f"    cpp_cb_update_addr = get_agg_udf_addr('{xwb__xrs.native_name}')\n"
                )
            dqr__ebl += (
                f"    cpp_cb_combine_addr = get_agg_udf_addr('{zno__sca.native_name}')\n"
                )
            dqr__ebl += (
                f"    cpp_cb_eval_addr = get_agg_udf_addr('{ofpc__knb.native_name}')\n"
                )
        else:
            dqr__ebl += '    cpp_cb_update_addr = 0\n'
            dqr__ebl += '    cpp_cb_combine_addr = 0\n'
            dqr__ebl += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            jnaom__gctq = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[jnaom__gctq.native_name] = jnaom__gctq
            gb_agg_cfunc_addr[jnaom__gctq.native_name] = jnaom__gctq.address
            dqr__ebl += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{jnaom__gctq.native_name}')\n"
                )
            dqr__ebl += (
                f"    cpp_cb_general_addr = get_agg_udf_addr('{jnaom__gctq.native_name}')\n"
                )
        else:
            dqr__ebl += '    cpp_cb_general_addr = 0\n'
    else:
        dqr__ebl += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        dqr__ebl += '    cpp_cb_update_addr = 0\n'
        dqr__ebl += '    cpp_cb_combine_addr = 0\n'
        dqr__ebl += '    cpp_cb_eval_addr = 0\n'
        dqr__ebl += '    cpp_cb_general_addr = 0\n'
    dqr__ebl += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(ohtf__lyzj.ftype)) for
        ohtf__lyzj in allfuncs] + ['0']))
    dqr__ebl += (
        f'    func_offsets = np.array({str(ybv__acfd)}, dtype=np.int32)\n')
    if len(yhu__ssrh) > 0:
        dqr__ebl += (
            f'    udf_ncols = np.array({str(yhu__ssrh)}, dtype=np.int32)\n')
    else:
        dqr__ebl += '    udf_ncols = np.array([0], np.int32)\n'
    dqr__ebl += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    wduq__gkkgm = (agg_node._num_shuffle_keys if agg_node._num_shuffle_keys !=
        -1 else n_keys)
    dqr__ebl += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {jun__ffws}, {agqrj__uvpp}, {wqgxr__excv}, {xds__ggi}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {wduq__gkkgm})
"""
    wbhc__axisy = []
    iial__aocc = 0
    if agg_node.return_key:
        iopoz__fkmw = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for nzuew__ywu in range(n_keys):
            bvo__vuyd = iopoz__fkmw + nzuew__ywu
            wbhc__axisy.append(bvo__vuyd if bvo__vuyd not in agg_node.
                dead_out_inds else -1)
            iial__aocc += 1
    for howy__nor in agg_node.gb_info_out.keys():
        wbhc__axisy.append(howy__nor)
        iial__aocc += 1
    fsyl__kcns = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            wbhc__axisy.append(agg_node.n_out_cols - 1)
        else:
            fsyl__kcns = True
    vjgvd__knyzh = ',' if okhn__ccacc == 1 else ''
    vizw__leo = (
        f"({', '.join(f'out_type{nzuew__ywu}' for nzuew__ywu in range(okhn__ccacc))}{vjgvd__knyzh})"
        )
    aja__dbx = []
    ujsa__frlp = []
    for nzuew__ywu, t in enumerate(out_col_typs):
        if nzuew__ywu not in agg_node.dead_out_inds and type_has_unknown_cats(t
            ):
            if nzuew__ywu in agg_node.gb_info_out:
                otilq__pvvgq = agg_node.gb_info_out[nzuew__ywu][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                hhal__ytgd = nzuew__ywu - iopoz__fkmw
                otilq__pvvgq = agg_node.in_key_inds[hhal__ytgd]
            ujsa__frlp.append(nzuew__ywu)
            if (agg_node.is_in_table_format and otilq__pvvgq < agg_node.
                n_in_table_arrays):
                aja__dbx.append(f'get_table_data(arg0, {otilq__pvvgq})')
            else:
                aja__dbx.append(f'arg{otilq__pvvgq}')
    vjgvd__knyzh = ',' if len(aja__dbx) == 1 else ''
    dqr__ebl += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {vizw__leo}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(aja__dbx)}{vjgvd__knyzh}), unknown_cat_out_inds)
"""
    dqr__ebl += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    dqr__ebl += '    delete_table_decref_arrays(table)\n'
    dqr__ebl += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for nzuew__ywu in range(n_keys):
            if wbhc__axisy[nzuew__ywu] == -1:
                dqr__ebl += (
                    f'    decref_table_array(out_table, {nzuew__ywu})\n')
    if fsyl__kcns:
        bso__qgfe = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        dqr__ebl += f'    decref_table_array(out_table, {bso__qgfe})\n'
    dqr__ebl += '    delete_table(out_table)\n'
    dqr__ebl += '    ev_clean.finalize()\n'
    dqr__ebl += '    return out_data\n'
    nzna__llls = {f'out_type{nzuew__ywu}': out_var_types[nzuew__ywu] for
        nzuew__ywu in range(okhn__ccacc)}
    nzna__llls['out_col_inds'] = MetaType(tuple(wbhc__axisy))
    nzna__llls['in_col_inds'] = MetaType(tuple(xnkar__lykc))
    nzna__llls['cpp_table_to_py_data'] = cpp_table_to_py_data
    nzna__llls['py_data_to_cpp_table'] = py_data_to_cpp_table
    nzna__llls.update({f'udf_type{nzuew__ywu}': t for nzuew__ywu, t in
        enumerate(tznt__ycrlu)})
    nzna__llls['udf_dummy_col_inds'] = MetaType(tuple(range(len(tznt__ycrlu))))
    nzna__llls['create_dummy_table'] = create_dummy_table
    nzna__llls['unknown_cat_out_inds'] = MetaType(tuple(ujsa__frlp))
    nzna__llls['get_table_data'] = bodo.hiframes.table.get_table_data
    return dqr__ebl, nzna__llls


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    kkh__sxwmz = tuple(unwrap_typeref(data_types.types[nzuew__ywu]) for
        nzuew__ywu in range(len(data_types.types)))
    udqnk__nuyrm = bodo.TableType(kkh__sxwmz)
    nzna__llls = {'table_type': udqnk__nuyrm}
    dqr__ebl = 'def impl(data_types):\n'
    dqr__ebl += '  py_table = init_table(table_type, False)\n'
    dqr__ebl += '  py_table = set_table_len(py_table, 1)\n'
    for okk__vpvrj, dlkj__puw in udqnk__nuyrm.type_to_blk.items():
        nzna__llls[f'typ_list_{dlkj__puw}'] = types.List(okk__vpvrj)
        nzna__llls[f'typ_{dlkj__puw}'] = okk__vpvrj
        nej__kms = len(udqnk__nuyrm.block_to_arr_ind[dlkj__puw])
        dqr__ebl += f"""  arr_list_{dlkj__puw} = alloc_list_like(typ_list_{dlkj__puw}, {nej__kms}, False)
"""
        dqr__ebl += f'  for i in range(len(arr_list_{dlkj__puw})):\n'
        dqr__ebl += (
            f'    arr_list_{dlkj__puw}[i] = alloc_type(1, typ_{dlkj__puw}, (-1,))\n'
            )
        dqr__ebl += (
            f'  py_table = set_table_block(py_table, arr_list_{dlkj__puw}, {dlkj__puw})\n'
            )
    dqr__ebl += '  return py_table\n'
    nzna__llls.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    nytuy__msz = {}
    exec(dqr__ebl, nzna__llls, nytuy__msz)
    return nytuy__msz['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    pqixq__ttgfu = agg_node.in_vars[0].name
    ubag__fwai, kxh__gncyd, tzx__nlh = block_use_map[pqixq__ttgfu]
    if kxh__gncyd or tzx__nlh:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        qmutb__sfmk, djnnu__lvxdp, ensgp__hwei = _compute_table_column_uses(
            agg_node.out_vars[0].name, table_col_use_map, equiv_vars)
        if djnnu__lvxdp or ensgp__hwei:
            qmutb__sfmk = set(range(agg_node.n_out_table_arrays))
    else:
        qmutb__sfmk = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            qmutb__sfmk = {0}
    onzvf__sneu = set(nzuew__ywu for nzuew__ywu in agg_node.in_key_inds if 
        nzuew__ywu < agg_node.n_in_table_arrays)
    dnzce__byv = set(agg_node.gb_info_out[nzuew__ywu][0] for nzuew__ywu in
        qmutb__sfmk if nzuew__ywu in agg_node.gb_info_out and agg_node.
        gb_info_out[nzuew__ywu][0] is not None)
    dnzce__byv |= onzvf__sneu | ubag__fwai
    ykwu__pkdjd = len(set(range(agg_node.n_in_table_arrays)) - dnzce__byv) == 0
    block_use_map[pqixq__ttgfu] = dnzce__byv, ykwu__pkdjd, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    bwrry__wksoi = agg_node.n_out_table_arrays
    kfzoo__jwzco = agg_node.out_vars[0].name
    mxwpy__qkk = _find_used_columns(kfzoo__jwzco, bwrry__wksoi,
        column_live_map, equiv_vars)
    if mxwpy__qkk is None:
        return False
    ntej__skwzg = set(range(bwrry__wksoi)) - mxwpy__qkk
    dqlk__wha = len(ntej__skwzg - agg_node.dead_out_inds) != 0
    if dqlk__wha:
        agg_node.dead_out_inds.update(ntej__skwzg)
        agg_node.update_dead_col_info()
    return dqlk__wha


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for euy__hpu in block.body:
            if is_call_assign(euy__hpu) and find_callname(f_ir, euy__hpu.value
                ) == ('len', 'builtins') and euy__hpu.value.args[0
                ].name == f_ir.arg_names[0]:
                fjfvj__idn = get_definition(f_ir, euy__hpu.value.func)
                fjfvj__idn.name = 'dummy_agg_count'
                fjfvj__idn.value = dummy_agg_count
    ktze__zfpx = get_name_var_table(f_ir.blocks)
    gygxd__kka = {}
    for name, jjmz__rin in ktze__zfpx.items():
        gygxd__kka[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, gygxd__kka)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    xciw__moxc = numba.core.compiler.Flags()
    xciw__moxc.nrt = True
    qdiqu__flyx = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, xciw__moxc)
    qdiqu__flyx.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, ijdj__tqab, calltypes, jjmz__rin = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    uycr__sbr = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    mhwn__uehcp = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    hnlxc__ffssj = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    lul__kuk = hnlxc__ffssj(typemap, calltypes)
    pm = mhwn__uehcp(typingctx, targetctx, None, f_ir, typemap, ijdj__tqab,
        calltypes, lul__kuk, {}, xciw__moxc, None)
    jnfw__kbu = numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline(
        pm)
    pm = mhwn__uehcp(typingctx, targetctx, None, f_ir, typemap, ijdj__tqab,
        calltypes, lul__kuk, {}, xciw__moxc, jnfw__kbu)
    rxqvq__evur = numba.core.typed_passes.InlineOverloads()
    rxqvq__evur.run_pass(pm)
    arjjm__dstdk = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    arjjm__dstdk.run()
    for block in f_ir.blocks.values():
        for euy__hpu in block.body:
            if is_assign(euy__hpu) and isinstance(euy__hpu.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[euy__hpu.target.name],
                SeriesType):
                okk__vpvrj = typemap.pop(euy__hpu.target.name)
                typemap[euy__hpu.target.name] = okk__vpvrj.data
            if is_call_assign(euy__hpu) and find_callname(f_ir, euy__hpu.value
                ) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[euy__hpu.target.name].remove(euy__hpu.value)
                euy__hpu.value = euy__hpu.value.args[0]
                f_ir._definitions[euy__hpu.target.name].append(euy__hpu.value)
            if is_call_assign(euy__hpu) and find_callname(f_ir, euy__hpu.value
                ) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[euy__hpu.target.name].remove(euy__hpu.value)
                euy__hpu.value = ir.Const(False, euy__hpu.loc)
                f_ir._definitions[euy__hpu.target.name].append(euy__hpu.value)
            if is_call_assign(euy__hpu) and find_callname(f_ir, euy__hpu.value
                ) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[euy__hpu.target.name].remove(euy__hpu.value)
                euy__hpu.value = ir.Const(False, euy__hpu.loc)
                f_ir._definitions[euy__hpu.target.name].append(euy__hpu.value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    zxvh__aonju = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, uycr__sbr)
    zxvh__aonju.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    xak__fsb = numba.core.compiler.StateDict()
    xak__fsb.func_ir = f_ir
    xak__fsb.typemap = typemap
    xak__fsb.calltypes = calltypes
    xak__fsb.typingctx = typingctx
    xak__fsb.targetctx = targetctx
    xak__fsb.return_type = ijdj__tqab
    numba.core.rewrites.rewrite_registry.apply('after-inference', xak__fsb)
    kke__yeht = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        ijdj__tqab, typingctx, targetctx, uycr__sbr, xciw__moxc, {})
    kke__yeht.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            xug__lcy = ctypes.pythonapi.PyCell_Get
            xug__lcy.restype = ctypes.py_object
            xug__lcy.argtypes = ctypes.py_object,
            rim__osvr = tuple(xug__lcy(bdzkz__azn) for bdzkz__azn in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            rim__osvr = closure.items
        assert len(code.co_freevars) == len(rim__osvr)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, rim__osvr)


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
        cbxq__ssu = SeriesType(in_col_typ.dtype, to_str_arr_if_dict_array(
            in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (cbxq__ssu,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        rdj__ymij, arr_var = _rm_arg_agg_block(block, pm.typemap)
        mcq__tkci = -1
        for nzuew__ywu, euy__hpu in enumerate(rdj__ymij):
            if isinstance(euy__hpu, numba.parfors.parfor.Parfor):
                assert mcq__tkci == -1, 'only one parfor for aggregation function'
                mcq__tkci = nzuew__ywu
        parfor = None
        if mcq__tkci != -1:
            parfor = rdj__ymij[mcq__tkci]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = rdj__ymij[:mcq__tkci] + parfor.init_block.body
        eval_nodes = rdj__ymij[mcq__tkci + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for euy__hpu in init_nodes:
            if is_assign(euy__hpu) and euy__hpu.target.name in redvars:
                ind = redvars.index(euy__hpu.target.name)
                reduce_vars[ind] = euy__hpu.target
        var_types = [pm.typemap[gqsh__rkccx] for gqsh__rkccx in redvars]
        jwigz__ici = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        bokne__hfj = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        prf__wftu = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(prf__wftu)
        self.all_update_funcs.append(bokne__hfj)
        self.all_combine_funcs.append(jwigz__ici)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        fzs__lsown = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        aetr__hlja = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        rypg__bomh = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        vrspn__akjt = gen_all_eval_func(self.all_eval_funcs, self.
            redvar_offsets)
        return (self.all_vartypes, fzs__lsown, aetr__hlja, rypg__bomh,
            vrspn__akjt)


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
    lgvck__teu = []
    for t, ohtf__lyzj in zip(in_col_types, agg_func):
        lgvck__teu.append((t, ohtf__lyzj))
    pgif__mwo = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    jpnh__dai = GeneralUDFGenerator()
    for in_col_typ, func in lgvck__teu:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            pgif__mwo.add_udf(in_col_typ, func)
        except:
            jpnh__dai.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = pgif__mwo.gen_all_func()
    general_udf_funcs = jpnh__dai.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    ewczu__tli = compute_use_defs(parfor.loop_body)
    cyb__sgfh = set()
    for cjys__zudnr in ewczu__tli.usemap.values():
        cyb__sgfh |= cjys__zudnr
    ndfi__urzn = set()
    for cjys__zudnr in ewczu__tli.defmap.values():
        ndfi__urzn |= cjys__zudnr
    uclps__blxsg = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    uclps__blxsg.body = eval_nodes
    hopfm__qnhy = compute_use_defs({(0): uclps__blxsg})
    zmovl__who = hopfm__qnhy.usemap[0]
    ynp__twnfb = set()
    xijtl__mgghi = []
    vhp__rlqz = []
    for euy__hpu in reversed(init_nodes):
        jyv__xxlh = {gqsh__rkccx.name for gqsh__rkccx in euy__hpu.list_vars()}
        if is_assign(euy__hpu):
            gqsh__rkccx = euy__hpu.target.name
            jyv__xxlh.remove(gqsh__rkccx)
            if (gqsh__rkccx in cyb__sgfh and gqsh__rkccx not in ynp__twnfb and
                gqsh__rkccx not in zmovl__who and gqsh__rkccx not in ndfi__urzn
                ):
                vhp__rlqz.append(euy__hpu)
                cyb__sgfh |= jyv__xxlh
                ndfi__urzn.add(gqsh__rkccx)
                continue
        ynp__twnfb |= jyv__xxlh
        xijtl__mgghi.append(euy__hpu)
    vhp__rlqz.reverse()
    xijtl__mgghi.reverse()
    vtt__juzx = min(parfor.loop_body.keys())
    ddnmf__fjy = parfor.loop_body[vtt__juzx]
    ddnmf__fjy.body = vhp__rlqz + ddnmf__fjy.body
    return xijtl__mgghi


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    iik__pwt = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    ztk__lau = set()
    efyhk__qsi = []
    for euy__hpu in init_nodes:
        if is_assign(euy__hpu) and isinstance(euy__hpu.value, ir.Global
            ) and isinstance(euy__hpu.value.value, pytypes.FunctionType
            ) and euy__hpu.value.value in iik__pwt:
            ztk__lau.add(euy__hpu.target.name)
        elif is_call_assign(euy__hpu) and euy__hpu.value.func.name in ztk__lau:
            pass
        else:
            efyhk__qsi.append(euy__hpu)
    init_nodes = efyhk__qsi
    nhl__andgp = types.Tuple(var_types)
    iedrh__xjic = lambda : None
    f_ir = compile_to_numba_ir(iedrh__xjic, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    dem__vcaw = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    kuf__lkylb = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc), dem__vcaw,
        loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [kuf__lkylb] + block.body
    block.body[-2].value.value = dem__vcaw
    bgxxv__lxb = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        nhl__andgp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kaynp__nhaog = numba.core.target_extension.dispatcher_registry[cpu_target](
        iedrh__xjic)
    kaynp__nhaog.add_overload(bgxxv__lxb)
    return kaynp__nhaog


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    jqzbr__rxbwr = len(update_funcs)
    tmbc__komrd = len(in_col_types)
    dqr__ebl = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for pws__ndlzm in range(jqzbr__rxbwr):
        fmq__rcd = ', '.join(['redvar_arrs[{}][w_ind]'.format(nzuew__ywu) for
            nzuew__ywu in range(redvar_offsets[pws__ndlzm], redvar_offsets[
            pws__ndlzm + 1])])
        if fmq__rcd:
            dqr__ebl += '  {} = update_vars_{}({},  data_in[{}][i])\n'.format(
                fmq__rcd, pws__ndlzm, fmq__rcd, 0 if tmbc__komrd == 1 else
                pws__ndlzm)
    dqr__ebl += '  return\n'
    cazx__rdz = {}
    for nzuew__ywu, ohtf__lyzj in enumerate(update_funcs):
        cazx__rdz['update_vars_{}'.format(nzuew__ywu)] = ohtf__lyzj
    nytuy__msz = {}
    exec(dqr__ebl, cazx__rdz, nytuy__msz)
    jaud__pctoj = nytuy__msz['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(jaud__pctoj)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    ltzc__hrgx = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = ltzc__hrgx, ltzc__hrgx, types.intp, types.intp
    vhn__cfxe = len(redvar_offsets) - 1
    dqr__ebl = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for pws__ndlzm in range(vhn__cfxe):
        fmq__rcd = ', '.join(['redvar_arrs[{}][w_ind]'.format(nzuew__ywu) for
            nzuew__ywu in range(redvar_offsets[pws__ndlzm], redvar_offsets[
            pws__ndlzm + 1])])
        hhsd__ohr = ', '.join(['recv_arrs[{}][i]'.format(nzuew__ywu) for
            nzuew__ywu in range(redvar_offsets[pws__ndlzm], redvar_offsets[
            pws__ndlzm + 1])])
        if hhsd__ohr:
            dqr__ebl += '  {} = combine_vars_{}({}, {})\n'.format(fmq__rcd,
                pws__ndlzm, fmq__rcd, hhsd__ohr)
    dqr__ebl += '  return\n'
    cazx__rdz = {}
    for nzuew__ywu, ohtf__lyzj in enumerate(combine_funcs):
        cazx__rdz['combine_vars_{}'.format(nzuew__ywu)] = ohtf__lyzj
    nytuy__msz = {}
    exec(dqr__ebl, cazx__rdz, nytuy__msz)
    pwq__xemi = nytuy__msz['combine_all_f']
    f_ir = compile_to_numba_ir(pwq__xemi, cazx__rdz)
    rypg__bomh = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kaynp__nhaog = numba.core.target_extension.dispatcher_registry[cpu_target](
        pwq__xemi)
    kaynp__nhaog.add_overload(rypg__bomh)
    return kaynp__nhaog


def gen_all_eval_func(eval_funcs, redvar_offsets):
    vhn__cfxe = len(redvar_offsets) - 1
    dqr__ebl = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for pws__ndlzm in range(vhn__cfxe):
        fmq__rcd = ', '.join(['redvar_arrs[{}][j]'.format(nzuew__ywu) for
            nzuew__ywu in range(redvar_offsets[pws__ndlzm], redvar_offsets[
            pws__ndlzm + 1])])
        dqr__ebl += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(pws__ndlzm,
            pws__ndlzm, fmq__rcd)
    dqr__ebl += '  return\n'
    cazx__rdz = {}
    for nzuew__ywu, ohtf__lyzj in enumerate(eval_funcs):
        cazx__rdz['eval_vars_{}'.format(nzuew__ywu)] = ohtf__lyzj
    nytuy__msz = {}
    exec(dqr__ebl, cazx__rdz, nytuy__msz)
    pgjzx__fhb = nytuy__msz['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(pgjzx__fhb)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    ujpp__morhz = len(var_types)
    fucza__wch = [f'in{nzuew__ywu}' for nzuew__ywu in range(ujpp__morhz)]
    nhl__andgp = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    plfuk__sflu = nhl__andgp(0)
    dqr__ebl = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        fucza__wch))
    nytuy__msz = {}
    exec(dqr__ebl, {'_zero': plfuk__sflu}, nytuy__msz)
    bhkcc__uvudo = nytuy__msz['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(bhkcc__uvudo, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': plfuk__sflu}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    whid__htipm = []
    for nzuew__ywu, gqsh__rkccx in enumerate(reduce_vars):
        whid__htipm.append(ir.Assign(block.body[nzuew__ywu].target,
            gqsh__rkccx, gqsh__rkccx.loc))
        for bhjsv__ndfc in gqsh__rkccx.versioned_names:
            whid__htipm.append(ir.Assign(gqsh__rkccx, ir.Var(gqsh__rkccx.
                scope, bhjsv__ndfc, gqsh__rkccx.loc), gqsh__rkccx.loc))
    block.body = block.body[:ujpp__morhz] + whid__htipm + eval_nodes
    prf__wftu = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nhl__andgp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kaynp__nhaog = numba.core.target_extension.dispatcher_registry[cpu_target](
        bhkcc__uvudo)
    kaynp__nhaog.add_overload(prf__wftu)
    return kaynp__nhaog


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    ujpp__morhz = len(redvars)
    pgn__gfwg = [f'v{nzuew__ywu}' for nzuew__ywu in range(ujpp__morhz)]
    fucza__wch = [f'in{nzuew__ywu}' for nzuew__ywu in range(ujpp__morhz)]
    dqr__ebl = 'def agg_combine({}):\n'.format(', '.join(pgn__gfwg +
        fucza__wch))
    lrmb__wfa = wrap_parfor_blocks(parfor)
    kre__xcu = find_topo_order(lrmb__wfa)
    kre__xcu = kre__xcu[1:]
    unwrap_parfor_blocks(parfor)
    facrh__bpn = {}
    qdd__spy = []
    for zngnd__cmlsd in kre__xcu:
        howma__fkq = parfor.loop_body[zngnd__cmlsd]
        for euy__hpu in howma__fkq.body:
            if is_assign(euy__hpu) and euy__hpu.target.name in redvars:
                liha__dipxn = euy__hpu.target.name
                ind = redvars.index(liha__dipxn)
                if ind in qdd__spy:
                    continue
                if len(f_ir._definitions[liha__dipxn]) == 2:
                    var_def = f_ir._definitions[liha__dipxn][0]
                    dqr__ebl += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[liha__dipxn][1]
                    dqr__ebl += _match_reduce_def(var_def, f_ir, ind)
    dqr__ebl += '    return {}'.format(', '.join(['v{}'.format(nzuew__ywu) for
        nzuew__ywu in range(ujpp__morhz)]))
    nytuy__msz = {}
    exec(dqr__ebl, {}, nytuy__msz)
    ueb__glu = nytuy__msz['agg_combine']
    arg_typs = tuple(2 * var_types)
    cazx__rdz = {'numba': numba, 'bodo': bodo, 'np': np}
    cazx__rdz.update(facrh__bpn)
    f_ir = compile_to_numba_ir(ueb__glu, cazx__rdz, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    nhl__andgp = pm.typemap[block.body[-1].value.name]
    jwigz__ici = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nhl__andgp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kaynp__nhaog = numba.core.target_extension.dispatcher_registry[cpu_target](
        ueb__glu)
    kaynp__nhaog.add_overload(jwigz__ici)
    return kaynp__nhaog


def _match_reduce_def(var_def, f_ir, ind):
    dqr__ebl = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        dqr__ebl = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        qymqz__kluxn = guard(find_callname, f_ir, var_def)
        if qymqz__kluxn == ('min', 'builtins'):
            dqr__ebl = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if qymqz__kluxn == ('max', 'builtins'):
            dqr__ebl = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return dqr__ebl


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    ujpp__morhz = len(redvars)
    zxlnr__qpg = 1
    in_vars = []
    for nzuew__ywu in range(zxlnr__qpg):
        nymyo__vap = ir.Var(arr_var.scope, f'$input{nzuew__ywu}', arr_var.loc)
        in_vars.append(nymyo__vap)
    otvag__nwytb = parfor.loop_nests[0].index_variable
    mbfu__bmlkg = [0] * ujpp__morhz
    for howma__fkq in parfor.loop_body.values():
        wvtiy__uhlsp = []
        for euy__hpu in howma__fkq.body:
            if is_var_assign(euy__hpu
                ) and euy__hpu.value.name == otvag__nwytb.name:
                continue
            if is_getitem(euy__hpu
                ) and euy__hpu.value.value.name == arr_var.name:
                euy__hpu.value = in_vars[0]
            if is_call_assign(euy__hpu) and guard(find_callname, pm.func_ir,
                euy__hpu.value) == ('isna', 'bodo.libs.array_kernels'
                ) and euy__hpu.value.args[0].name == arr_var.name:
                euy__hpu.value = ir.Const(False, euy__hpu.target.loc)
            if is_assign(euy__hpu) and euy__hpu.target.name in redvars:
                ind = redvars.index(euy__hpu.target.name)
                mbfu__bmlkg[ind] = euy__hpu.target
            wvtiy__uhlsp.append(euy__hpu)
        howma__fkq.body = wvtiy__uhlsp
    pgn__gfwg = ['v{}'.format(nzuew__ywu) for nzuew__ywu in range(ujpp__morhz)]
    fucza__wch = ['in{}'.format(nzuew__ywu) for nzuew__ywu in range(zxlnr__qpg)
        ]
    dqr__ebl = 'def agg_update({}):\n'.format(', '.join(pgn__gfwg + fucza__wch)
        )
    dqr__ebl += '    __update_redvars()\n'
    dqr__ebl += '    return {}'.format(', '.join(['v{}'.format(nzuew__ywu) for
        nzuew__ywu in range(ujpp__morhz)]))
    nytuy__msz = {}
    exec(dqr__ebl, {}, nytuy__msz)
    omgfs__yvdd = nytuy__msz['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * zxlnr__qpg)
    f_ir = compile_to_numba_ir(omgfs__yvdd, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    nlt__hwme = f_ir.blocks.popitem()[1].body
    nhl__andgp = pm.typemap[nlt__hwme[-1].value.name]
    lrmb__wfa = wrap_parfor_blocks(parfor)
    kre__xcu = find_topo_order(lrmb__wfa)
    kre__xcu = kre__xcu[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    ddnmf__fjy = f_ir.blocks[kre__xcu[0]]
    ikv__jbqjc = f_ir.blocks[kre__xcu[-1]]
    oxxu__tyo = nlt__hwme[:ujpp__morhz + zxlnr__qpg]
    if ujpp__morhz > 1:
        eox__pdevg = nlt__hwme[-3:]
        assert is_assign(eox__pdevg[0]) and isinstance(eox__pdevg[0].value,
            ir.Expr) and eox__pdevg[0].value.op == 'build_tuple'
    else:
        eox__pdevg = nlt__hwme[-2:]
    for nzuew__ywu in range(ujpp__morhz):
        hcbss__bvf = nlt__hwme[nzuew__ywu].target
        ngkn__wlbe = ir.Assign(hcbss__bvf, mbfu__bmlkg[nzuew__ywu],
            hcbss__bvf.loc)
        oxxu__tyo.append(ngkn__wlbe)
    for nzuew__ywu in range(ujpp__morhz, ujpp__morhz + zxlnr__qpg):
        hcbss__bvf = nlt__hwme[nzuew__ywu].target
        ngkn__wlbe = ir.Assign(hcbss__bvf, in_vars[nzuew__ywu - ujpp__morhz
            ], hcbss__bvf.loc)
        oxxu__tyo.append(ngkn__wlbe)
    ddnmf__fjy.body = oxxu__tyo + ddnmf__fjy.body
    tswhs__knl = []
    for nzuew__ywu in range(ujpp__morhz):
        hcbss__bvf = nlt__hwme[nzuew__ywu].target
        ngkn__wlbe = ir.Assign(mbfu__bmlkg[nzuew__ywu], hcbss__bvf,
            hcbss__bvf.loc)
        tswhs__knl.append(ngkn__wlbe)
    ikv__jbqjc.body += tswhs__knl + eox__pdevg
    kcz__nwnp = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        nhl__andgp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    kaynp__nhaog = numba.core.target_extension.dispatcher_registry[cpu_target](
        omgfs__yvdd)
    kaynp__nhaog.add_overload(kcz__nwnp)
    return kaynp__nhaog


def _rm_arg_agg_block(block, typemap):
    rdj__ymij = []
    arr_var = None
    for nzuew__ywu, euy__hpu in enumerate(block.body):
        if is_assign(euy__hpu) and isinstance(euy__hpu.value, ir.Arg):
            arr_var = euy__hpu.target
            pjbu__gakv = typemap[arr_var.name]
            if not isinstance(pjbu__gakv, types.ArrayCompatible):
                rdj__ymij += block.body[nzuew__ywu + 1:]
                break
            huw__alvl = block.body[nzuew__ywu + 1]
            assert is_assign(huw__alvl) and isinstance(huw__alvl.value, ir.Expr
                ) and huw__alvl.value.op == 'getattr' and huw__alvl.value.attr == 'shape' and huw__alvl.value.value.name == arr_var.name
            nulyd__bmor = huw__alvl.target
            mwqp__avenn = block.body[nzuew__ywu + 2]
            assert is_assign(mwqp__avenn) and isinstance(mwqp__avenn.value,
                ir.Expr
                ) and mwqp__avenn.value.op == 'static_getitem' and mwqp__avenn.value.value.name == nulyd__bmor.name
            rdj__ymij += block.body[nzuew__ywu + 3:]
            break
        rdj__ymij.append(euy__hpu)
    return rdj__ymij, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    lrmb__wfa = wrap_parfor_blocks(parfor)
    kre__xcu = find_topo_order(lrmb__wfa)
    kre__xcu = kre__xcu[1:]
    unwrap_parfor_blocks(parfor)
    for zngnd__cmlsd in reversed(kre__xcu):
        for euy__hpu in reversed(parfor.loop_body[zngnd__cmlsd].body):
            if isinstance(euy__hpu, ir.Assign) and (euy__hpu.target.name in
                parfor_params or euy__hpu.target.name in var_to_param):
                seswe__pcz = euy__hpu.target.name
                rhs = euy__hpu.value
                ecxjt__trdvt = (seswe__pcz if seswe__pcz in parfor_params else
                    var_to_param[seswe__pcz])
                zjz__jzwq = []
                if isinstance(rhs, ir.Var):
                    zjz__jzwq = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    zjz__jzwq = [gqsh__rkccx.name for gqsh__rkccx in
                        euy__hpu.value.list_vars()]
                param_uses[ecxjt__trdvt].extend(zjz__jzwq)
                for gqsh__rkccx in zjz__jzwq:
                    var_to_param[gqsh__rkccx] = ecxjt__trdvt
            if isinstance(euy__hpu, Parfor):
                get_parfor_reductions(euy__hpu, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for heh__bfda, zjz__jzwq in param_uses.items():
        if heh__bfda in zjz__jzwq and heh__bfda not in reduce_varnames:
            reduce_varnames.append(heh__bfda)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
