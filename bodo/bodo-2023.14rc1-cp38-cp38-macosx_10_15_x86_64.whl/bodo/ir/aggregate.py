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
        vysl__qengz = func.signature
        if vysl__qengz == types.none(types.voidptr):
            uvael__ovc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            bfv__ocpy = cgutils.get_or_insert_function(builder.module,
                uvael__ovc, sym._literal_value)
            builder.call(bfv__ocpy, [context.get_constant_null(vysl__qengz.
                args[0])])
        elif vysl__qengz == types.none(types.int64, types.voidptr, types.
            voidptr):
            uvael__ovc = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            bfv__ocpy = cgutils.get_or_insert_function(builder.module,
                uvael__ovc, sym._literal_value)
            builder.call(bfv__ocpy, [context.get_constant(types.int64, 0),
                context.get_constant_null(vysl__qengz.args[1]), context.
                get_constant_null(vysl__qengz.args[2])])
        else:
            uvael__ovc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            bfv__ocpy = cgutils.get_or_insert_function(builder.module,
                uvael__ovc, sym._literal_value)
            builder.call(bfv__ocpy, [context.get_constant_null(vysl__qengz.
                args[0]), context.get_constant_null(vysl__qengz.args[1]),
                context.get_constant_null(vysl__qengz.args[2])])
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
        tzi__lvy = True
        yrmaf__hgrkg = 1
        dripl__tlkl = -1
        if isinstance(rhs, ir.Expr):
            for abyn__ajh in rhs.kws:
                if func_name in list_cumulative:
                    if abyn__ajh[0] == 'skipna':
                        tzi__lvy = guard(find_const, func_ir, abyn__ajh[1])
                        if not isinstance(tzi__lvy, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if abyn__ajh[0] == 'dropna':
                        tzi__lvy = guard(find_const, func_ir, abyn__ajh[1])
                        if not isinstance(tzi__lvy, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            yrmaf__hgrkg = get_call_expr_arg('shift', rhs.args, dict(rhs.
                kws), 0, 'periods', yrmaf__hgrkg)
            yrmaf__hgrkg = guard(find_const, func_ir, yrmaf__hgrkg)
        if func_name == 'head':
            dripl__tlkl = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(dripl__tlkl, int):
                dripl__tlkl = guard(find_const, func_ir, dripl__tlkl)
            if dripl__tlkl < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = tzi__lvy
        func.periods = yrmaf__hgrkg
        func.head_n = dripl__tlkl
        if func_name == 'transform':
            kws = dict(rhs.kws)
            fhzx__jtalu = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            xrx__yjgkd = typemap[fhzx__jtalu.name]
            rhk__mtt = None
            if isinstance(xrx__yjgkd, str):
                rhk__mtt = xrx__yjgkd
            elif is_overload_constant_str(xrx__yjgkd):
                rhk__mtt = get_overload_const_str(xrx__yjgkd)
            elif bodo.utils.typing.is_builtin_function(xrx__yjgkd):
                rhk__mtt = bodo.utils.typing.get_builtin_function_name(
                    xrx__yjgkd)
            if rhk__mtt not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {rhk__mtt}')
            func.transform_func = supported_agg_funcs.index(rhk__mtt)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    fhzx__jtalu = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if fhzx__jtalu == '':
        xrx__yjgkd = types.none
    else:
        xrx__yjgkd = typemap[fhzx__jtalu.name]
    if is_overload_constant_dict(xrx__yjgkd):
        xxsao__usmg = get_overload_constant_dict(xrx__yjgkd)
        vci__frguv = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in xxsao__usmg.values()]
        return vci__frguv
    if xrx__yjgkd == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(xrx__yjgkd, types.BaseTuple) or is_overload_constant_list(
        xrx__yjgkd):
        vci__frguv = []
        cjmc__pswly = 0
        if is_overload_constant_list(xrx__yjgkd):
            hqjyf__avf = get_overload_const_list(xrx__yjgkd)
        else:
            hqjyf__avf = xrx__yjgkd.types
        for t in hqjyf__avf:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                vci__frguv.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(hqjyf__avf) > 1:
                    func.fname = '<lambda_' + str(cjmc__pswly) + '>'
                    cjmc__pswly += 1
                vci__frguv.append(func)
        return [vci__frguv]
    if is_overload_constant_str(xrx__yjgkd):
        func_name = get_overload_const_str(xrx__yjgkd)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(xrx__yjgkd):
        func_name = bodo.utils.typing.get_builtin_function_name(xrx__yjgkd)
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
        cjmc__pswly = 0
        dgq__zbp = []
        for tywii__frrji in f_val:
            func = get_agg_func_udf(func_ir, tywii__frrji, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{cjmc__pswly}>'
                cjmc__pswly += 1
            dgq__zbp.append(func)
        return dgq__zbp
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
    rhk__mtt = code.co_name
    return rhk__mtt


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
            crp__hlo = types.DType(args[0])
            return signature(crp__hlo, *args)


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
        return [fditl__qahmi for fditl__qahmi in self.in_vars if 
            fditl__qahmi is not None]

    def get_live_out_vars(self):
        return [fditl__qahmi for fditl__qahmi in self.out_vars if 
            fditl__qahmi is not None]

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
        bknzt__fcgr = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        wamgz__fwm = list(get_index_data_arr_types(self.out_type.index))
        return bknzt__fcgr + wamgz__fwm

    def update_dead_col_info(self):
        for ucv__ymtsf in self.dead_out_inds:
            self.gb_info_out.pop(ucv__ymtsf, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for imzmy__jqw, phfjq__dag in self.gb_info_in.copy().items():
            vhyov__ovgc = []
            for tywii__frrji, qovh__hanh in phfjq__dag:
                if qovh__hanh not in self.dead_out_inds:
                    vhyov__ovgc.append((tywii__frrji, qovh__hanh))
            if not vhyov__ovgc:
                if (imzmy__jqw is not None and imzmy__jqw not in self.
                    in_key_inds):
                    self.dead_in_inds.add(imzmy__jqw)
                self.gb_info_in.pop(imzmy__jqw)
            else:
                self.gb_info_in[imzmy__jqw] = vhyov__ovgc
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for szmys__quxey in range(1, len(self.in_vars)):
                ucv__ymtsf = self.n_in_table_arrays + szmys__quxey - 1
                if ucv__ymtsf in self.dead_in_inds:
                    self.in_vars[szmys__quxey] = None
        else:
            for szmys__quxey in range(len(self.in_vars)):
                if szmys__quxey in self.dead_in_inds:
                    self.in_vars[szmys__quxey] = None

    def __repr__(self):
        dlsc__gsftf = ', '.join(fditl__qahmi.name for fditl__qahmi in self.
            get_live_in_vars())
        rvu__wmnwt = f'{self.df_in}{{{dlsc__gsftf}}}'
        pkals__lhe = ', '.join(fditl__qahmi.name for fditl__qahmi in self.
            get_live_out_vars())
        rskyj__syzeq = f'{self.df_out}{{{pkals__lhe}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {rvu__wmnwt} {rskyj__syzeq}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({fditl__qahmi.name for fditl__qahmi in aggregate_node.
        get_live_in_vars()})
    def_set.update({fditl__qahmi.name for fditl__qahmi in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    gqppj__xxnvl = agg_node.out_vars[0]
    if gqppj__xxnvl is not None and gqppj__xxnvl.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            nch__pboka = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(nch__pboka)
        else:
            agg_node.dead_out_inds.add(0)
    for szmys__quxey in range(1, len(agg_node.out_vars)):
        fditl__qahmi = agg_node.out_vars[szmys__quxey]
        if fditl__qahmi is not None and fditl__qahmi.name not in lives:
            agg_node.out_vars[szmys__quxey] = None
            ucv__ymtsf = agg_node.n_out_table_arrays + szmys__quxey - 1
            agg_node.dead_out_inds.add(ucv__ymtsf)
    if all(fditl__qahmi is None for fditl__qahmi in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    imuzu__cthk = {fditl__qahmi.name for fditl__qahmi in aggregate_node.
        get_live_out_vars()}
    return set(), imuzu__cthk


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for szmys__quxey in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[szmys__quxey] is not None:
            aggregate_node.in_vars[szmys__quxey] = replace_vars_inner(
                aggregate_node.in_vars[szmys__quxey], var_dict)
    for szmys__quxey in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[szmys__quxey] is not None:
            aggregate_node.out_vars[szmys__quxey] = replace_vars_inner(
                aggregate_node.out_vars[szmys__quxey], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for szmys__quxey in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[szmys__quxey] is not None:
            aggregate_node.in_vars[szmys__quxey] = visit_vars_inner(
                aggregate_node.in_vars[szmys__quxey], callback, cbdata)
    for szmys__quxey in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[szmys__quxey] is not None:
            aggregate_node.out_vars[szmys__quxey] = visit_vars_inner(
                aggregate_node.out_vars[szmys__quxey], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    gxu__qlo = []
    for urwx__urwpv in aggregate_node.get_live_in_vars():
        vog__agqde = equiv_set.get_shape(urwx__urwpv)
        if vog__agqde is not None:
            gxu__qlo.append(vog__agqde[0])
    if len(gxu__qlo) > 1:
        equiv_set.insert_equiv(*gxu__qlo)
    ckm__adccs = []
    gxu__qlo = []
    for urwx__urwpv in aggregate_node.get_live_out_vars():
        rapb__hoiqr = typemap[urwx__urwpv.name]
        cymdp__adcj = array_analysis._gen_shape_call(equiv_set, urwx__urwpv,
            rapb__hoiqr.ndim, None, ckm__adccs)
        equiv_set.insert_equiv(urwx__urwpv, cymdp__adcj)
        gxu__qlo.append(cymdp__adcj[0])
        equiv_set.define(urwx__urwpv, set())
    if len(gxu__qlo) > 1:
        equiv_set.insert_equiv(*gxu__qlo)
    return [], ckm__adccs


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    mwb__omt = aggregate_node.get_live_in_vars()
    zdep__atznp = aggregate_node.get_live_out_vars()
    bohw__jfcar = Distribution.OneD
    for urwx__urwpv in mwb__omt:
        bohw__jfcar = Distribution(min(bohw__jfcar.value, array_dists[
            urwx__urwpv.name].value))
    nzmx__wdtk = Distribution(min(bohw__jfcar.value, Distribution.OneD_Var.
        value))
    for urwx__urwpv in zdep__atznp:
        if urwx__urwpv.name in array_dists:
            nzmx__wdtk = Distribution(min(nzmx__wdtk.value, array_dists[
                urwx__urwpv.name].value))
    if nzmx__wdtk != Distribution.OneD_Var:
        bohw__jfcar = nzmx__wdtk
    for urwx__urwpv in mwb__omt:
        array_dists[urwx__urwpv.name] = bohw__jfcar
    for urwx__urwpv in zdep__atznp:
        array_dists[urwx__urwpv.name] = nzmx__wdtk


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for urwx__urwpv in agg_node.get_live_out_vars():
        definitions[urwx__urwpv.name].append(agg_node)
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
    sde__gbtbz = agg_node.get_live_in_vars()
    snt__wmv = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for fditl__qahmi in (sde__gbtbz + snt__wmv):
            if array_dists[fditl__qahmi.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                fditl__qahmi.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    vci__frguv = []
    func_out_types = []
    for qovh__hanh, (imzmy__jqw, func) in agg_node.gb_info_out.items():
        if imzmy__jqw is not None:
            t = agg_node.in_col_types[imzmy__jqw]
            in_col_typs.append(t)
        vci__frguv.append(func)
        func_out_types.append(out_col_typs[qovh__hanh])
    nirke__owdog = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for szmys__quxey, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            nirke__owdog.update({f'in_cat_dtype_{szmys__quxey}': in_col_typ})
    for szmys__quxey, tpeif__ucj in enumerate(out_col_typs):
        if isinstance(tpeif__ucj, bodo.CategoricalArrayType):
            nirke__owdog.update({f'out_cat_dtype_{szmys__quxey}': tpeif__ucj})
    udf_func_struct = get_udf_func_struct(vci__frguv, in_col_typs,
        typingctx, targetctx)
    out_var_types = [(typemap[fditl__qahmi.name] if fditl__qahmi is not
        None else types.none) for fditl__qahmi in agg_node.out_vars]
    sodh__qdf, lepu__stt = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, func_out_types, parallel, udf_func_struct,
        out_var_types, typemap)
    nirke__owdog.update(lepu__stt)
    nirke__owdog.update({'pd': pd, 'pre_alloc_string_array':
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
            nirke__owdog.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            nirke__owdog.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    xeo__zpng = {}
    exec(sodh__qdf, {}, xeo__zpng)
    tsuh__wjpa = xeo__zpng['agg_top']
    eeoo__uutol = compile_to_numba_ir(tsuh__wjpa, nirke__owdog, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[fditl__qahmi
        .name] for fditl__qahmi in sde__gbtbz), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(eeoo__uutol, sde__gbtbz)
    bxvc__csu = eeoo__uutol.body[-2].value.value
    ord__xeq = eeoo__uutol.body[:-2]
    for szmys__quxey, fditl__qahmi in enumerate(snt__wmv):
        gen_getitem(fditl__qahmi, bxvc__csu, szmys__quxey, calltypes, ord__xeq)
    return ord__xeq


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        dnrfg__zgt = IntDtype(t.dtype).name
        assert dnrfg__zgt.endswith('Dtype()')
        dnrfg__zgt = dnrfg__zgt[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{dnrfg__zgt}'))"
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
        orr__tqfa = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {orr__tqfa}_cat_dtype_{colnum})')
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
    pzy__cyts = udf_func_struct.var_typs
    sirs__jen = len(pzy__cyts)
    sodh__qdf = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    sodh__qdf += '    if is_null_pointer(in_table):\n'
    sodh__qdf += '        return\n'
    sodh__qdf += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in pzy__cyts]), 
        ',' if len(pzy__cyts) == 1 else '')
    bpr__hvj = n_keys
    nyty__jfto = []
    redvar_offsets = []
    rlemf__sqri = []
    if do_combine:
        for szmys__quxey, tywii__frrji in enumerate(allfuncs):
            if tywii__frrji.ftype != 'udf':
                bpr__hvj += tywii__frrji.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(bpr__hvj, bpr__hvj +
                    tywii__frrji.n_redvars))
                bpr__hvj += tywii__frrji.n_redvars
                rlemf__sqri.append(data_in_typs_[func_idx_to_in_col[
                    szmys__quxey]])
                nyty__jfto.append(func_idx_to_in_col[szmys__quxey] + n_keys)
    else:
        for szmys__quxey, tywii__frrji in enumerate(allfuncs):
            if tywii__frrji.ftype != 'udf':
                bpr__hvj += tywii__frrji.ncols_post_shuffle
            else:
                redvar_offsets += list(range(bpr__hvj + 1, bpr__hvj + 1 +
                    tywii__frrji.n_redvars))
                bpr__hvj += tywii__frrji.n_redvars + 1
                rlemf__sqri.append(data_in_typs_[func_idx_to_in_col[
                    szmys__quxey]])
                nyty__jfto.append(func_idx_to_in_col[szmys__quxey] + n_keys)
    assert len(redvar_offsets) == sirs__jen
    ise__pixva = len(rlemf__sqri)
    uujjl__cnoy = []
    for szmys__quxey, t in enumerate(rlemf__sqri):
        uujjl__cnoy.append(_gen_dummy_alloc(t, szmys__quxey, True))
    sodh__qdf += '    data_in_dummy = ({}{})\n'.format(','.join(uujjl__cnoy
        ), ',' if len(rlemf__sqri) == 1 else '')
    sodh__qdf += """
    # initialize redvar cols
"""
    sodh__qdf += '    init_vals = __init_func()\n'
    for szmys__quxey in range(sirs__jen):
        sodh__qdf += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(szmys__quxey, redvar_offsets[szmys__quxey], szmys__quxey))
        sodh__qdf += '    incref(redvar_arr_{})\n'.format(szmys__quxey)
        sodh__qdf += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            szmys__quxey, szmys__quxey)
    sodh__qdf += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(szmys__quxey) for szmys__quxey in range(sirs__jen)]), ',' if
        sirs__jen == 1 else '')
    sodh__qdf += '\n'
    for szmys__quxey in range(ise__pixva):
        sodh__qdf += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(szmys__quxey, nyty__jfto[szmys__quxey], szmys__quxey))
        sodh__qdf += '    incref(data_in_{})\n'.format(szmys__quxey)
    sodh__qdf += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(szmys__quxey) for szmys__quxey in range(ise__pixva)]), ',' if
        ise__pixva == 1 else '')
    sodh__qdf += '\n'
    sodh__qdf += '    for i in range(len(data_in_0)):\n'
    sodh__qdf += '        w_ind = row_to_group[i]\n'
    sodh__qdf += '        if w_ind != -1:\n'
    sodh__qdf += '            __update_redvars(redvars, data_in, w_ind, i)\n'
    xeo__zpng = {}
    exec(sodh__qdf, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, xeo__zpng)
    return xeo__zpng['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    pzy__cyts = udf_func_struct.var_typs
    sirs__jen = len(pzy__cyts)
    sodh__qdf = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    sodh__qdf += '    if is_null_pointer(in_table):\n'
    sodh__qdf += '        return\n'
    sodh__qdf += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in pzy__cyts]), 
        ',' if len(pzy__cyts) == 1 else '')
    ckllc__fvm = n_keys
    qpzap__chif = n_keys
    ojecc__umdkq = []
    redge__dwy = []
    for tywii__frrji in allfuncs:
        if tywii__frrji.ftype != 'udf':
            ckllc__fvm += tywii__frrji.ncols_pre_shuffle
            qpzap__chif += tywii__frrji.ncols_post_shuffle
        else:
            ojecc__umdkq += list(range(ckllc__fvm, ckllc__fvm +
                tywii__frrji.n_redvars))
            redge__dwy += list(range(qpzap__chif + 1, qpzap__chif + 1 +
                tywii__frrji.n_redvars))
            ckllc__fvm += tywii__frrji.n_redvars
            qpzap__chif += 1 + tywii__frrji.n_redvars
    assert len(ojecc__umdkq) == sirs__jen
    sodh__qdf += """
    # initialize redvar cols
"""
    sodh__qdf += '    init_vals = __init_func()\n'
    for szmys__quxey in range(sirs__jen):
        sodh__qdf += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(szmys__quxey, redge__dwy[szmys__quxey], szmys__quxey))
        sodh__qdf += '    incref(redvar_arr_{})\n'.format(szmys__quxey)
        sodh__qdf += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            szmys__quxey, szmys__quxey)
    sodh__qdf += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(szmys__quxey) for szmys__quxey in range(sirs__jen)]), ',' if
        sirs__jen == 1 else '')
    sodh__qdf += '\n'
    for szmys__quxey in range(sirs__jen):
        sodh__qdf += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(szmys__quxey, ojecc__umdkq[szmys__quxey], szmys__quxey))
        sodh__qdf += '    incref(recv_redvar_arr_{})\n'.format(szmys__quxey)
    sodh__qdf += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(szmys__quxey) for szmys__quxey in range
        (sirs__jen)]), ',' if sirs__jen == 1 else '')
    sodh__qdf += '\n'
    if sirs__jen:
        sodh__qdf += '    for i in range(len(recv_redvar_arr_0)):\n'
        sodh__qdf += '        w_ind = row_to_group[i]\n'
        sodh__qdf += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    xeo__zpng = {}
    exec(sodh__qdf, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, xeo__zpng)
    return xeo__zpng['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    pzy__cyts = udf_func_struct.var_typs
    sirs__jen = len(pzy__cyts)
    bpr__hvj = n_keys
    redvar_offsets = []
    uklw__drav = []
    aihux__kzi = []
    for szmys__quxey, tywii__frrji in enumerate(allfuncs):
        if tywii__frrji.ftype != 'udf':
            bpr__hvj += tywii__frrji.ncols_post_shuffle
        else:
            uklw__drav.append(bpr__hvj)
            redvar_offsets += list(range(bpr__hvj + 1, bpr__hvj + 1 +
                tywii__frrji.n_redvars))
            bpr__hvj += 1 + tywii__frrji.n_redvars
            aihux__kzi.append(out_data_typs_[szmys__quxey])
    assert len(redvar_offsets) == sirs__jen
    ise__pixva = len(aihux__kzi)
    sodh__qdf = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    sodh__qdf += '    if is_null_pointer(table):\n'
    sodh__qdf += '        return\n'
    sodh__qdf += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in pzy__cyts]), 
        ',' if len(pzy__cyts) == 1 else '')
    sodh__qdf += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        aihux__kzi]), ',' if len(aihux__kzi) == 1 else '')
    for szmys__quxey in range(sirs__jen):
        sodh__qdf += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(szmys__quxey, redvar_offsets[szmys__quxey], szmys__quxey))
        sodh__qdf += '    incref(redvar_arr_{})\n'.format(szmys__quxey)
    sodh__qdf += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(szmys__quxey) for szmys__quxey in range(sirs__jen)]), ',' if
        sirs__jen == 1 else '')
    sodh__qdf += '\n'
    for szmys__quxey in range(ise__pixva):
        sodh__qdf += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(szmys__quxey, uklw__drav[szmys__quxey], szmys__quxey))
        sodh__qdf += '    incref(data_out_{})\n'.format(szmys__quxey)
    sodh__qdf += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(szmys__quxey) for szmys__quxey in range(ise__pixva)]), ',' if
        ise__pixva == 1 else '')
    sodh__qdf += '\n'
    sodh__qdf += '    for i in range(len(data_out_0)):\n'
    sodh__qdf += '        __eval_res(redvars, data_out, i)\n'
    xeo__zpng = {}
    exec(sodh__qdf, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, xeo__zpng)
    return xeo__zpng['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    bpr__hvj = n_keys
    uheod__ixn = []
    for szmys__quxey, tywii__frrji in enumerate(allfuncs):
        if tywii__frrji.ftype == 'gen_udf':
            uheod__ixn.append(bpr__hvj)
            bpr__hvj += 1
        elif tywii__frrji.ftype != 'udf':
            bpr__hvj += tywii__frrji.ncols_post_shuffle
        else:
            bpr__hvj += tywii__frrji.n_redvars + 1
    sodh__qdf = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    sodh__qdf += '    if num_groups == 0:\n'
    sodh__qdf += '        return\n'
    for szmys__quxey, func in enumerate(udf_func_struct.general_udf_funcs):
        sodh__qdf += '    # col {}\n'.format(szmys__quxey)
        sodh__qdf += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(uheod__ixn[szmys__quxey], szmys__quxey))
        sodh__qdf += '    incref(out_col)\n'
        sodh__qdf += '    for j in range(num_groups):\n'
        sodh__qdf += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(szmys__quxey, szmys__quxey))
        sodh__qdf += '        incref(in_col)\n'
        sodh__qdf += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(szmys__quxey))
    nirke__owdog = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    unk__yxfk = 0
    for szmys__quxey, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[unk__yxfk]
        nirke__owdog['func_{}'.format(unk__yxfk)] = func
        nirke__owdog['in_col_{}_typ'.format(unk__yxfk)] = in_col_typs[
            func_idx_to_in_col[szmys__quxey]]
        nirke__owdog['out_col_{}_typ'.format(unk__yxfk)] = out_col_typs[
            szmys__quxey]
        unk__yxfk += 1
    xeo__zpng = {}
    exec(sodh__qdf, nirke__owdog, xeo__zpng)
    tywii__frrji = xeo__zpng['bodo_gb_apply_general_udfs{}'.format(
        label_suffix)]
    ftyqd__pxxez = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(ftyqd__pxxez, nopython=True)(tywii__frrji)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    fjcz__lych = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        wldty__vqki = []
        if agg_node.in_vars[0] is not None:
            wldty__vqki.append('arg0')
        for szmys__quxey in range(agg_node.n_in_table_arrays, agg_node.
            n_in_cols):
            if szmys__quxey not in agg_node.dead_in_inds:
                wldty__vqki.append(f'arg{szmys__quxey}')
    else:
        wldty__vqki = [f'arg{szmys__quxey}' for szmys__quxey, fditl__qahmi in
            enumerate(agg_node.in_vars) if fditl__qahmi is not None]
    sodh__qdf = f"def agg_top({', '.join(wldty__vqki)}):\n"
    rxsqe__eyfbd = []
    if agg_node.is_in_table_format:
        rxsqe__eyfbd = agg_node.in_key_inds + [imzmy__jqw for imzmy__jqw,
            eyw__hgab in agg_node.gb_info_out.values() if imzmy__jqw is not
            None]
        if agg_node.input_has_index:
            rxsqe__eyfbd.append(agg_node.n_in_cols - 1)
        igmo__dmgbe = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        zsdtk__jlzzr = []
        for szmys__quxey in range(agg_node.n_in_table_arrays, agg_node.
            n_in_cols):
            if szmys__quxey in agg_node.dead_in_inds:
                zsdtk__jlzzr.append('None')
            else:
                zsdtk__jlzzr.append(f'arg{szmys__quxey}')
        cddvz__vlfq = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        sodh__qdf += f"""    table = py_data_to_cpp_table({cddvz__vlfq}, ({', '.join(zsdtk__jlzzr)}{igmo__dmgbe}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        agndb__vlpm = [f'arg{szmys__quxey}' for szmys__quxey in agg_node.
            in_key_inds]
        zcy__vnn = [f'arg{imzmy__jqw}' for imzmy__jqw, eyw__hgab in
            agg_node.gb_info_out.values() if imzmy__jqw is not None]
        niva__zpmth = agndb__vlpm + zcy__vnn
        if agg_node.input_has_index:
            niva__zpmth.append(f'arg{len(agg_node.in_vars) - 1}')
        sodh__qdf += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({bkxvg__owxb})' for bkxvg__owxb in niva__zpmth))
        sodh__qdf += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    ekh__snhjo = []
    func_idx_to_in_col = []
    idi__muow = []
    tzi__lvy = False
    egrmv__kqljp = 1
    dripl__tlkl = -1
    hjeu__pfzw = 0
    eigok__wst = 0
    vci__frguv = [func for eyw__hgab, func in agg_node.gb_info_out.values()]
    for clmtd__qgku, func in enumerate(vci__frguv):
        ekh__snhjo.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            hjeu__pfzw += 1
        if hasattr(func, 'skipdropna'):
            tzi__lvy = func.skipdropna
        if func.ftype == 'shift':
            egrmv__kqljp = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            eigok__wst = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            dripl__tlkl = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(clmtd__qgku)
        if func.ftype == 'udf':
            idi__muow.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            idi__muow.append(0)
            do_combine = False
    ekh__snhjo.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if hjeu__pfzw > 0:
        if hjeu__pfzw != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    scf__upuen = []
    if udf_func_struct is not None:
        illc__hswe = next_label()
        if udf_func_struct.regular_udfs:
            ftyqd__pxxez = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            dbz__otf = numba.cfunc(ftyqd__pxxez, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs, do_combine,
                func_idx_to_in_col, illc__hswe))
            mezq__mlzb = numba.cfunc(ftyqd__pxxez, nopython=True)(
                gen_combine_cb(udf_func_struct, allfuncs, n_keys, illc__hswe))
            azj__xjq = numba.cfunc('void(voidptr)', nopython=True)(gen_eval_cb
                (udf_func_struct, allfuncs, n_keys, func_out_types, illc__hswe)
                )
            udf_func_struct.set_regular_cfuncs(dbz__otf, mezq__mlzb, azj__xjq)
            for odbum__azn in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[odbum__azn.native_name] = odbum__azn
                gb_agg_cfunc_addr[odbum__azn.native_name] = odbum__azn.address
        if udf_func_struct.general_udfs:
            woym__jyzk = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, func_out_types, func_idx_to_in_col,
                illc__hswe)
            udf_func_struct.set_general_cfunc(woym__jyzk)
        pzy__cyts = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        dpja__hvyo = 0
        szmys__quxey = 0
        for pgr__wbm, tywii__frrji in zip(agg_node.gb_info_out.keys(), allfuncs
            ):
            if tywii__frrji.ftype in ('udf', 'gen_udf'):
                scf__upuen.append(out_col_typs[pgr__wbm])
                for pqfgt__kzwht in range(dpja__hvyo, dpja__hvyo +
                    idi__muow[szmys__quxey]):
                    scf__upuen.append(dtype_to_array_type(pzy__cyts[
                        pqfgt__kzwht]))
                dpja__hvyo += idi__muow[szmys__quxey]
                szmys__quxey += 1
        sodh__qdf += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{szmys__quxey}' for szmys__quxey in range(len(scf__upuen)))}{',' if len(scf__upuen) == 1 else ''}))
"""
        sodh__qdf += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(scf__upuen)})
"""
        if udf_func_struct.regular_udfs:
            sodh__qdf += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{dbz__otf.native_name}')\n"
                )
            sodh__qdf += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{mezq__mlzb.native_name}')\n"
                )
            sodh__qdf += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{azj__xjq.native_name}')\n"
                )
            sodh__qdf += (
                f"    cpp_cb_update_addr = get_agg_udf_addr('{dbz__otf.native_name}')\n"
                )
            sodh__qdf += (
                f"    cpp_cb_combine_addr = get_agg_udf_addr('{mezq__mlzb.native_name}')\n"
                )
            sodh__qdf += (
                f"    cpp_cb_eval_addr = get_agg_udf_addr('{azj__xjq.native_name}')\n"
                )
        else:
            sodh__qdf += '    cpp_cb_update_addr = 0\n'
            sodh__qdf += '    cpp_cb_combine_addr = 0\n'
            sodh__qdf += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            odbum__azn = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[odbum__azn.native_name] = odbum__azn
            gb_agg_cfunc_addr[odbum__azn.native_name] = odbum__azn.address
            sodh__qdf += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{odbum__azn.native_name}')\n"
                )
            sodh__qdf += (
                f"    cpp_cb_general_addr = get_agg_udf_addr('{odbum__azn.native_name}')\n"
                )
        else:
            sodh__qdf += '    cpp_cb_general_addr = 0\n'
    else:
        sodh__qdf += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        sodh__qdf += '    cpp_cb_update_addr = 0\n'
        sodh__qdf += '    cpp_cb_combine_addr = 0\n'
        sodh__qdf += '    cpp_cb_eval_addr = 0\n'
        sodh__qdf += '    cpp_cb_general_addr = 0\n'
    sodh__qdf += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(tywii__frrji.ftype)) for
        tywii__frrji in allfuncs] + ['0']))
    sodh__qdf += (
        f'    func_offsets = np.array({str(ekh__snhjo)}, dtype=np.int32)\n')
    if len(idi__muow) > 0:
        sodh__qdf += (
            f'    udf_ncols = np.array({str(idi__muow)}, dtype=np.int32)\n')
    else:
        sodh__qdf += '    udf_ncols = np.array([0], np.int32)\n'
    sodh__qdf += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    oyw__iowkx = (agg_node._num_shuffle_keys if agg_node._num_shuffle_keys !=
        -1 else n_keys)
    sodh__qdf += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {tzi__lvy}, {egrmv__kqljp}, {eigok__wst}, {dripl__tlkl}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {oyw__iowkx})
"""
    vhzzd__idlh = []
    bwv__znys = 0
    if agg_node.return_key:
        witv__ylusv = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for szmys__quxey in range(n_keys):
            ucv__ymtsf = witv__ylusv + szmys__quxey
            vhzzd__idlh.append(ucv__ymtsf if ucv__ymtsf not in agg_node.
                dead_out_inds else -1)
            bwv__znys += 1
    for pgr__wbm in agg_node.gb_info_out.keys():
        vhzzd__idlh.append(pgr__wbm)
        bwv__znys += 1
    jtcqn__ugg = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            vhzzd__idlh.append(agg_node.n_out_cols - 1)
        else:
            jtcqn__ugg = True
    igmo__dmgbe = ',' if fjcz__lych == 1 else ''
    haxkf__jqlrp = (
        f"({', '.join(f'out_type{szmys__quxey}' for szmys__quxey in range(fjcz__lych))}{igmo__dmgbe})"
        )
    fei__vawyh = []
    nfd__cyqnk = []
    for szmys__quxey, t in enumerate(out_col_typs):
        if (szmys__quxey not in agg_node.dead_out_inds and
            type_has_unknown_cats(t)):
            if szmys__quxey in agg_node.gb_info_out:
                imzmy__jqw = agg_node.gb_info_out[szmys__quxey][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                qyprr__kiivb = szmys__quxey - witv__ylusv
                imzmy__jqw = agg_node.in_key_inds[qyprr__kiivb]
            nfd__cyqnk.append(szmys__quxey)
            if (agg_node.is_in_table_format and imzmy__jqw < agg_node.
                n_in_table_arrays):
                fei__vawyh.append(f'get_table_data(arg0, {imzmy__jqw})')
            else:
                fei__vawyh.append(f'arg{imzmy__jqw}')
    igmo__dmgbe = ',' if len(fei__vawyh) == 1 else ''
    sodh__qdf += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {haxkf__jqlrp}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(fei__vawyh)}{igmo__dmgbe}), unknown_cat_out_inds)
"""
    sodh__qdf += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    sodh__qdf += '    delete_table_decref_arrays(table)\n'
    sodh__qdf += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for szmys__quxey in range(n_keys):
            if vhzzd__idlh[szmys__quxey] == -1:
                sodh__qdf += (
                    f'    decref_table_array(out_table, {szmys__quxey})\n')
    if jtcqn__ugg:
        ixwg__ogpn = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        sodh__qdf += f'    decref_table_array(out_table, {ixwg__ogpn})\n'
    sodh__qdf += '    delete_table(out_table)\n'
    sodh__qdf += '    ev_clean.finalize()\n'
    sodh__qdf += '    return out_data\n'
    jrbu__jmgi = {f'out_type{szmys__quxey}': out_var_types[szmys__quxey] for
        szmys__quxey in range(fjcz__lych)}
    jrbu__jmgi['out_col_inds'] = MetaType(tuple(vhzzd__idlh))
    jrbu__jmgi['in_col_inds'] = MetaType(tuple(rxsqe__eyfbd))
    jrbu__jmgi['cpp_table_to_py_data'] = cpp_table_to_py_data
    jrbu__jmgi['py_data_to_cpp_table'] = py_data_to_cpp_table
    jrbu__jmgi.update({f'udf_type{szmys__quxey}': t for szmys__quxey, t in
        enumerate(scf__upuen)})
    jrbu__jmgi['udf_dummy_col_inds'] = MetaType(tuple(range(len(scf__upuen))))
    jrbu__jmgi['create_dummy_table'] = create_dummy_table
    jrbu__jmgi['unknown_cat_out_inds'] = MetaType(tuple(nfd__cyqnk))
    jrbu__jmgi['get_table_data'] = bodo.hiframes.table.get_table_data
    return sodh__qdf, jrbu__jmgi


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    dtner__eyxoa = tuple(unwrap_typeref(data_types.types[szmys__quxey]) for
        szmys__quxey in range(len(data_types.types)))
    sjwhs__vfydw = bodo.TableType(dtner__eyxoa)
    jrbu__jmgi = {'table_type': sjwhs__vfydw}
    sodh__qdf = 'def impl(data_types):\n'
    sodh__qdf += '  py_table = init_table(table_type, False)\n'
    sodh__qdf += '  py_table = set_table_len(py_table, 1)\n'
    for rapb__hoiqr, bcjoz__dmtjb in sjwhs__vfydw.type_to_blk.items():
        jrbu__jmgi[f'typ_list_{bcjoz__dmtjb}'] = types.List(rapb__hoiqr)
        jrbu__jmgi[f'typ_{bcjoz__dmtjb}'] = rapb__hoiqr
        jfo__nksz = len(sjwhs__vfydw.block_to_arr_ind[bcjoz__dmtjb])
        sodh__qdf += f"""  arr_list_{bcjoz__dmtjb} = alloc_list_like(typ_list_{bcjoz__dmtjb}, {jfo__nksz}, False)
"""
        sodh__qdf += f'  for i in range(len(arr_list_{bcjoz__dmtjb})):\n'
        sodh__qdf += (
            f'    arr_list_{bcjoz__dmtjb}[i] = alloc_type(1, typ_{bcjoz__dmtjb}, (-1,))\n'
            )
        sodh__qdf += f"""  py_table = set_table_block(py_table, arr_list_{bcjoz__dmtjb}, {bcjoz__dmtjb})
"""
    sodh__qdf += '  return py_table\n'
    jrbu__jmgi.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    xeo__zpng = {}
    exec(sodh__qdf, jrbu__jmgi, xeo__zpng)
    return xeo__zpng['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    iqkxu__hqpph = agg_node.in_vars[0].name
    xpi__ubukn, aztqi__tjzhv, xdxe__fvmxu = block_use_map[iqkxu__hqpph]
    if aztqi__tjzhv or xdxe__fvmxu:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        cirl__icbc, qfh__jpgg, tew__yzhd = _compute_table_column_uses(agg_node
            .out_vars[0].name, table_col_use_map, equiv_vars)
        if qfh__jpgg or tew__yzhd:
            cirl__icbc = set(range(agg_node.n_out_table_arrays))
    else:
        cirl__icbc = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            cirl__icbc = {0}
    xwu__vvm = set(szmys__quxey for szmys__quxey in agg_node.in_key_inds if
        szmys__quxey < agg_node.n_in_table_arrays)
    ggm__mniac = set(agg_node.gb_info_out[szmys__quxey][0] for szmys__quxey in
        cirl__icbc if szmys__quxey in agg_node.gb_info_out and agg_node.
        gb_info_out[szmys__quxey][0] is not None)
    ggm__mniac |= xwu__vvm | xpi__ubukn
    oqq__euda = len(set(range(agg_node.n_in_table_arrays)) - ggm__mniac) == 0
    block_use_map[iqkxu__hqpph] = ggm__mniac, oqq__euda, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    rtzu__cjz = agg_node.n_out_table_arrays
    jefbf__antsy = agg_node.out_vars[0].name
    vdxo__guper = _find_used_columns(jefbf__antsy, rtzu__cjz,
        column_live_map, equiv_vars)
    if vdxo__guper is None:
        return False
    mae__tifp = set(range(rtzu__cjz)) - vdxo__guper
    mjkp__zzqy = len(mae__tifp - agg_node.dead_out_inds) != 0
    if mjkp__zzqy:
        agg_node.dead_out_inds.update(mae__tifp)
        agg_node.update_dead_col_info()
    return mjkp__zzqy


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for qbwas__yxqe in block.body:
            if is_call_assign(qbwas__yxqe) and find_callname(f_ir,
                qbwas__yxqe.value) == ('len', 'builtins'
                ) and qbwas__yxqe.value.args[0].name == f_ir.arg_names[0]:
                jrwg__vzjnd = get_definition(f_ir, qbwas__yxqe.value.func)
                jrwg__vzjnd.name = 'dummy_agg_count'
                jrwg__vzjnd.value = dummy_agg_count
    gxb__bgrv = get_name_var_table(f_ir.blocks)
    psvlk__cxy = {}
    for name, eyw__hgab in gxb__bgrv.items():
        psvlk__cxy[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, psvlk__cxy)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    fif__gsw = numba.core.compiler.Flags()
    fif__gsw.nrt = True
    dpmxq__coin = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, fif__gsw)
    dpmxq__coin.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, awcb__juos, calltypes, eyw__hgab = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    oti__fbiwr = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    eul__yly = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    ryooj__whhxm = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    elb__iix = ryooj__whhxm(typemap, calltypes)
    pm = eul__yly(typingctx, targetctx, None, f_ir, typemap, awcb__juos,
        calltypes, elb__iix, {}, fif__gsw, None)
    qpgxb__frc = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = eul__yly(typingctx, targetctx, None, f_ir, typemap, awcb__juos,
        calltypes, elb__iix, {}, fif__gsw, qpgxb__frc)
    vdn__tdzlz = numba.core.typed_passes.InlineOverloads()
    vdn__tdzlz.run_pass(pm)
    nyu__tax = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    nyu__tax.run()
    for block in f_ir.blocks.values():
        for qbwas__yxqe in block.body:
            if is_assign(qbwas__yxqe) and isinstance(qbwas__yxqe.value, (ir
                .Arg, ir.Var)) and isinstance(typemap[qbwas__yxqe.target.
                name], SeriesType):
                rapb__hoiqr = typemap.pop(qbwas__yxqe.target.name)
                typemap[qbwas__yxqe.target.name] = rapb__hoiqr.data
            if is_call_assign(qbwas__yxqe) and find_callname(f_ir,
                qbwas__yxqe.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[qbwas__yxqe.target.name].remove(qbwas__yxqe
                    .value)
                qbwas__yxqe.value = qbwas__yxqe.value.args[0]
                f_ir._definitions[qbwas__yxqe.target.name].append(qbwas__yxqe
                    .value)
            if is_call_assign(qbwas__yxqe) and find_callname(f_ir,
                qbwas__yxqe.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[qbwas__yxqe.target.name].remove(qbwas__yxqe
                    .value)
                qbwas__yxqe.value = ir.Const(False, qbwas__yxqe.loc)
                f_ir._definitions[qbwas__yxqe.target.name].append(qbwas__yxqe
                    .value)
            if is_call_assign(qbwas__yxqe) and find_callname(f_ir,
                qbwas__yxqe.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[qbwas__yxqe.target.name].remove(qbwas__yxqe
                    .value)
                qbwas__yxqe.value = ir.Const(False, qbwas__yxqe.loc)
                f_ir._definitions[qbwas__yxqe.target.name].append(qbwas__yxqe
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    hdvxr__hkbv = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, oti__fbiwr)
    hdvxr__hkbv.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    xeykw__wqsc = numba.core.compiler.StateDict()
    xeykw__wqsc.func_ir = f_ir
    xeykw__wqsc.typemap = typemap
    xeykw__wqsc.calltypes = calltypes
    xeykw__wqsc.typingctx = typingctx
    xeykw__wqsc.targetctx = targetctx
    xeykw__wqsc.return_type = awcb__juos
    numba.core.rewrites.rewrite_registry.apply('after-inference', xeykw__wqsc)
    thzb__omcm = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        awcb__juos, typingctx, targetctx, oti__fbiwr, fif__gsw, {})
    thzb__omcm.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            gmsr__xwos = ctypes.pythonapi.PyCell_Get
            gmsr__xwos.restype = ctypes.py_object
            gmsr__xwos.argtypes = ctypes.py_object,
            xxsao__usmg = tuple(gmsr__xwos(dxy__izrx) for dxy__izrx in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            xxsao__usmg = closure.items
        assert len(code.co_freevars) == len(xxsao__usmg)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks,
            xxsao__usmg)


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
        ibdoz__xnjvi = SeriesType(in_col_typ.dtype,
            to_str_arr_if_dict_array(in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (ibdoz__xnjvi,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        uwm__bcth, arr_var = _rm_arg_agg_block(block, pm.typemap)
        ouwkh__evxti = -1
        for szmys__quxey, qbwas__yxqe in enumerate(uwm__bcth):
            if isinstance(qbwas__yxqe, numba.parfors.parfor.Parfor):
                assert ouwkh__evxti == -1, 'only one parfor for aggregation function'
                ouwkh__evxti = szmys__quxey
        parfor = None
        if ouwkh__evxti != -1:
            parfor = uwm__bcth[ouwkh__evxti]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = uwm__bcth[:ouwkh__evxti] + parfor.init_block.body
        eval_nodes = uwm__bcth[ouwkh__evxti + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for qbwas__yxqe in init_nodes:
            if is_assign(qbwas__yxqe) and qbwas__yxqe.target.name in redvars:
                ind = redvars.index(qbwas__yxqe.target.name)
                reduce_vars[ind] = qbwas__yxqe.target
        var_types = [pm.typemap[fditl__qahmi] for fditl__qahmi in redvars]
        fbrd__mjjnc = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        ypdul__qvwnl = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        wats__sgr = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(wats__sgr)
        self.all_update_funcs.append(ypdul__qvwnl)
        self.all_combine_funcs.append(fbrd__mjjnc)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        hlgfd__uefbv = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        zjb__dfcpr = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        ytxi__mijv = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        thqjn__aky = gen_all_eval_func(self.all_eval_funcs, self.redvar_offsets
            )
        return (self.all_vartypes, hlgfd__uefbv, zjb__dfcpr, ytxi__mijv,
            thqjn__aky)


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
    yonqe__uuva = []
    for t, tywii__frrji in zip(in_col_types, agg_func):
        yonqe__uuva.append((t, tywii__frrji))
    okr__dhcaz = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    lipd__gntv = GeneralUDFGenerator()
    for in_col_typ, func in yonqe__uuva:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            okr__dhcaz.add_udf(in_col_typ, func)
        except:
            lipd__gntv.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = okr__dhcaz.gen_all_func()
    general_udf_funcs = lipd__gntv.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    apq__oay = compute_use_defs(parfor.loop_body)
    ned__mkcl = set()
    for fejys__skezk in apq__oay.usemap.values():
        ned__mkcl |= fejys__skezk
    zka__iatxq = set()
    for fejys__skezk in apq__oay.defmap.values():
        zka__iatxq |= fejys__skezk
    lhmgf__rpqje = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    lhmgf__rpqje.body = eval_nodes
    rha__nwrx = compute_use_defs({(0): lhmgf__rpqje})
    arl__ytttk = rha__nwrx.usemap[0]
    tvw__acbg = set()
    wlwfc__zkqy = []
    dby__xht = []
    for qbwas__yxqe in reversed(init_nodes):
        euit__mvydr = {fditl__qahmi.name for fditl__qahmi in qbwas__yxqe.
            list_vars()}
        if is_assign(qbwas__yxqe):
            fditl__qahmi = qbwas__yxqe.target.name
            euit__mvydr.remove(fditl__qahmi)
            if (fditl__qahmi in ned__mkcl and fditl__qahmi not in tvw__acbg and
                fditl__qahmi not in arl__ytttk and fditl__qahmi not in
                zka__iatxq):
                dby__xht.append(qbwas__yxqe)
                ned__mkcl |= euit__mvydr
                zka__iatxq.add(fditl__qahmi)
                continue
        tvw__acbg |= euit__mvydr
        wlwfc__zkqy.append(qbwas__yxqe)
    dby__xht.reverse()
    wlwfc__zkqy.reverse()
    qwypd__gws = min(parfor.loop_body.keys())
    uap__moq = parfor.loop_body[qwypd__gws]
    uap__moq.body = dby__xht + uap__moq.body
    return wlwfc__zkqy


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    tjej__qrbf = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    cdgy__acuq = set()
    xtp__wyhb = []
    for qbwas__yxqe in init_nodes:
        if is_assign(qbwas__yxqe) and isinstance(qbwas__yxqe.value, ir.Global
            ) and isinstance(qbwas__yxqe.value.value, pytypes.FunctionType
            ) and qbwas__yxqe.value.value in tjej__qrbf:
            cdgy__acuq.add(qbwas__yxqe.target.name)
        elif is_call_assign(qbwas__yxqe
            ) and qbwas__yxqe.value.func.name in cdgy__acuq:
            pass
        else:
            xtp__wyhb.append(qbwas__yxqe)
    init_nodes = xtp__wyhb
    cfexm__vyubr = types.Tuple(var_types)
    cfp__wvd = lambda : None
    f_ir = compile_to_numba_ir(cfp__wvd, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    ugue__adrxm = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    btar__ykz = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        ugue__adrxm, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [btar__ykz] + block.body
    block.body[-2].value.value = ugue__adrxm
    bxm__rsnh = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        cfexm__vyubr, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wfm__vgi = numba.core.target_extension.dispatcher_registry[cpu_target](
        cfp__wvd)
    wfm__vgi.add_overload(bxm__rsnh)
    return wfm__vgi


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    wvvra__pshp = len(update_funcs)
    rdmvb__vpgjl = len(in_col_types)
    sodh__qdf = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for pqfgt__kzwht in range(wvvra__pshp):
        axclc__ynn = ', '.join(['redvar_arrs[{}][w_ind]'.format(
            szmys__quxey) for szmys__quxey in range(redvar_offsets[
            pqfgt__kzwht], redvar_offsets[pqfgt__kzwht + 1])])
        if axclc__ynn:
            sodh__qdf += '  {} = update_vars_{}({},  data_in[{}][i])\n'.format(
                axclc__ynn, pqfgt__kzwht, axclc__ynn, 0 if rdmvb__vpgjl == 
                1 else pqfgt__kzwht)
    sodh__qdf += '  return\n'
    nirke__owdog = {}
    for szmys__quxey, tywii__frrji in enumerate(update_funcs):
        nirke__owdog['update_vars_{}'.format(szmys__quxey)] = tywii__frrji
    xeo__zpng = {}
    exec(sodh__qdf, nirke__owdog, xeo__zpng)
    aesk__izkiu = xeo__zpng['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(aesk__izkiu)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    wacq__psj = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    arg_typs = wacq__psj, wacq__psj, types.intp, types.intp
    foejt__ovrz = len(redvar_offsets) - 1
    sodh__qdf = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for pqfgt__kzwht in range(foejt__ovrz):
        axclc__ynn = ', '.join(['redvar_arrs[{}][w_ind]'.format(
            szmys__quxey) for szmys__quxey in range(redvar_offsets[
            pqfgt__kzwht], redvar_offsets[pqfgt__kzwht + 1])])
        aaaxo__gcl = ', '.join(['recv_arrs[{}][i]'.format(szmys__quxey) for
            szmys__quxey in range(redvar_offsets[pqfgt__kzwht],
            redvar_offsets[pqfgt__kzwht + 1])])
        if aaaxo__gcl:
            sodh__qdf += '  {} = combine_vars_{}({}, {})\n'.format(axclc__ynn,
                pqfgt__kzwht, axclc__ynn, aaaxo__gcl)
    sodh__qdf += '  return\n'
    nirke__owdog = {}
    for szmys__quxey, tywii__frrji in enumerate(combine_funcs):
        nirke__owdog['combine_vars_{}'.format(szmys__quxey)] = tywii__frrji
    xeo__zpng = {}
    exec(sodh__qdf, nirke__owdog, xeo__zpng)
    cde__rkk = xeo__zpng['combine_all_f']
    f_ir = compile_to_numba_ir(cde__rkk, nirke__owdog)
    ytxi__mijv = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wfm__vgi = numba.core.target_extension.dispatcher_registry[cpu_target](
        cde__rkk)
    wfm__vgi.add_overload(ytxi__mijv)
    return wfm__vgi


def gen_all_eval_func(eval_funcs, redvar_offsets):
    foejt__ovrz = len(redvar_offsets) - 1
    sodh__qdf = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for pqfgt__kzwht in range(foejt__ovrz):
        axclc__ynn = ', '.join(['redvar_arrs[{}][j]'.format(szmys__quxey) for
            szmys__quxey in range(redvar_offsets[pqfgt__kzwht],
            redvar_offsets[pqfgt__kzwht + 1])])
        sodh__qdf += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
            pqfgt__kzwht, pqfgt__kzwht, axclc__ynn)
    sodh__qdf += '  return\n'
    nirke__owdog = {}
    for szmys__quxey, tywii__frrji in enumerate(eval_funcs):
        nirke__owdog['eval_vars_{}'.format(szmys__quxey)] = tywii__frrji
    xeo__zpng = {}
    exec(sodh__qdf, nirke__owdog, xeo__zpng)
    dtwpm__wmti = xeo__zpng['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(dtwpm__wmti)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    kwsky__ytevz = len(var_types)
    cqtcx__hfsr = [f'in{szmys__quxey}' for szmys__quxey in range(kwsky__ytevz)]
    cfexm__vyubr = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    nyrg__djzz = cfexm__vyubr(0)
    sodh__qdf = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        cqtcx__hfsr))
    xeo__zpng = {}
    exec(sodh__qdf, {'_zero': nyrg__djzz}, xeo__zpng)
    osc__slvlt = xeo__zpng['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(osc__slvlt, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': nyrg__djzz}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    sjx__tcdi = []
    for szmys__quxey, fditl__qahmi in enumerate(reduce_vars):
        sjx__tcdi.append(ir.Assign(block.body[szmys__quxey].target,
            fditl__qahmi, fditl__qahmi.loc))
        for kwzje__dxivx in fditl__qahmi.versioned_names:
            sjx__tcdi.append(ir.Assign(fditl__qahmi, ir.Var(fditl__qahmi.
                scope, kwzje__dxivx, fditl__qahmi.loc), fditl__qahmi.loc))
    block.body = block.body[:kwsky__ytevz] + sjx__tcdi + eval_nodes
    wats__sgr = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        cfexm__vyubr, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wfm__vgi = numba.core.target_extension.dispatcher_registry[cpu_target](
        osc__slvlt)
    wfm__vgi.add_overload(wats__sgr)
    return wfm__vgi


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    kwsky__ytevz = len(redvars)
    zezlj__srhha = [f'v{szmys__quxey}' for szmys__quxey in range(kwsky__ytevz)]
    cqtcx__hfsr = [f'in{szmys__quxey}' for szmys__quxey in range(kwsky__ytevz)]
    sodh__qdf = 'def agg_combine({}):\n'.format(', '.join(zezlj__srhha +
        cqtcx__hfsr))
    uig__ryc = wrap_parfor_blocks(parfor)
    oeu__vccnu = find_topo_order(uig__ryc)
    oeu__vccnu = oeu__vccnu[1:]
    unwrap_parfor_blocks(parfor)
    mjqzv__ohd = {}
    art__wzu = []
    for axe__mjcc in oeu__vccnu:
        idk__jclz = parfor.loop_body[axe__mjcc]
        for qbwas__yxqe in idk__jclz.body:
            if is_assign(qbwas__yxqe) and qbwas__yxqe.target.name in redvars:
                zbaw__cdm = qbwas__yxqe.target.name
                ind = redvars.index(zbaw__cdm)
                if ind in art__wzu:
                    continue
                if len(f_ir._definitions[zbaw__cdm]) == 2:
                    var_def = f_ir._definitions[zbaw__cdm][0]
                    sodh__qdf += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[zbaw__cdm][1]
                    sodh__qdf += _match_reduce_def(var_def, f_ir, ind)
    sodh__qdf += '    return {}'.format(', '.join(['v{}'.format(
        szmys__quxey) for szmys__quxey in range(kwsky__ytevz)]))
    xeo__zpng = {}
    exec(sodh__qdf, {}, xeo__zpng)
    wponx__yjv = xeo__zpng['agg_combine']
    arg_typs = tuple(2 * var_types)
    nirke__owdog = {'numba': numba, 'bodo': bodo, 'np': np}
    nirke__owdog.update(mjqzv__ohd)
    f_ir = compile_to_numba_ir(wponx__yjv, nirke__owdog, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=pm.
        typemap, calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    cfexm__vyubr = pm.typemap[block.body[-1].value.name]
    fbrd__mjjnc = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        cfexm__vyubr, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wfm__vgi = numba.core.target_extension.dispatcher_registry[cpu_target](
        wponx__yjv)
    wfm__vgi.add_overload(fbrd__mjjnc)
    return wfm__vgi


def _match_reduce_def(var_def, f_ir, ind):
    sodh__qdf = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        sodh__qdf = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        edthp__fmdz = guard(find_callname, f_ir, var_def)
        if edthp__fmdz == ('min', 'builtins'):
            sodh__qdf = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if edthp__fmdz == ('max', 'builtins'):
            sodh__qdf = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return sodh__qdf


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    kwsky__ytevz = len(redvars)
    mhmzf__ijgj = 1
    in_vars = []
    for szmys__quxey in range(mhmzf__ijgj):
        hro__gjj = ir.Var(arr_var.scope, f'$input{szmys__quxey}', arr_var.loc)
        in_vars.append(hro__gjj)
    crndp__wpy = parfor.loop_nests[0].index_variable
    awd__xltiv = [0] * kwsky__ytevz
    for idk__jclz in parfor.loop_body.values():
        hawp__yeeno = []
        for qbwas__yxqe in idk__jclz.body:
            if is_var_assign(qbwas__yxqe
                ) and qbwas__yxqe.value.name == crndp__wpy.name:
                continue
            if is_getitem(qbwas__yxqe
                ) and qbwas__yxqe.value.value.name == arr_var.name:
                qbwas__yxqe.value = in_vars[0]
            if is_call_assign(qbwas__yxqe) and guard(find_callname, pm.
                func_ir, qbwas__yxqe.value) == ('isna',
                'bodo.libs.array_kernels') and qbwas__yxqe.value.args[0
                ].name == arr_var.name:
                qbwas__yxqe.value = ir.Const(False, qbwas__yxqe.target.loc)
            if is_assign(qbwas__yxqe) and qbwas__yxqe.target.name in redvars:
                ind = redvars.index(qbwas__yxqe.target.name)
                awd__xltiv[ind] = qbwas__yxqe.target
            hawp__yeeno.append(qbwas__yxqe)
        idk__jclz.body = hawp__yeeno
    zezlj__srhha = ['v{}'.format(szmys__quxey) for szmys__quxey in range(
        kwsky__ytevz)]
    cqtcx__hfsr = ['in{}'.format(szmys__quxey) for szmys__quxey in range(
        mhmzf__ijgj)]
    sodh__qdf = 'def agg_update({}):\n'.format(', '.join(zezlj__srhha +
        cqtcx__hfsr))
    sodh__qdf += '    __update_redvars()\n'
    sodh__qdf += '    return {}'.format(', '.join(['v{}'.format(
        szmys__quxey) for szmys__quxey in range(kwsky__ytevz)]))
    xeo__zpng = {}
    exec(sodh__qdf, {}, xeo__zpng)
    kkce__xhan = xeo__zpng['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * mhmzf__ijgj)
    f_ir = compile_to_numba_ir(kkce__xhan, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    phfpd__dzi = f_ir.blocks.popitem()[1].body
    cfexm__vyubr = pm.typemap[phfpd__dzi[-1].value.name]
    uig__ryc = wrap_parfor_blocks(parfor)
    oeu__vccnu = find_topo_order(uig__ryc)
    oeu__vccnu = oeu__vccnu[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    uap__moq = f_ir.blocks[oeu__vccnu[0]]
    bxj__mcva = f_ir.blocks[oeu__vccnu[-1]]
    outl__ykra = phfpd__dzi[:kwsky__ytevz + mhmzf__ijgj]
    if kwsky__ytevz > 1:
        vtb__tqy = phfpd__dzi[-3:]
        assert is_assign(vtb__tqy[0]) and isinstance(vtb__tqy[0].value, ir.Expr
            ) and vtb__tqy[0].value.op == 'build_tuple'
    else:
        vtb__tqy = phfpd__dzi[-2:]
    for szmys__quxey in range(kwsky__ytevz):
        htc__wmi = phfpd__dzi[szmys__quxey].target
        arkg__vdjah = ir.Assign(htc__wmi, awd__xltiv[szmys__quxey],
            htc__wmi.loc)
        outl__ykra.append(arkg__vdjah)
    for szmys__quxey in range(kwsky__ytevz, kwsky__ytevz + mhmzf__ijgj):
        htc__wmi = phfpd__dzi[szmys__quxey].target
        arkg__vdjah = ir.Assign(htc__wmi, in_vars[szmys__quxey -
            kwsky__ytevz], htc__wmi.loc)
        outl__ykra.append(arkg__vdjah)
    uap__moq.body = outl__ykra + uap__moq.body
    tqht__pojp = []
    for szmys__quxey in range(kwsky__ytevz):
        htc__wmi = phfpd__dzi[szmys__quxey].target
        arkg__vdjah = ir.Assign(awd__xltiv[szmys__quxey], htc__wmi,
            htc__wmi.loc)
        tqht__pojp.append(arkg__vdjah)
    bxj__mcva.body += tqht__pojp + vtb__tqy
    evzea__oxa = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        cfexm__vyubr, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    wfm__vgi = numba.core.target_extension.dispatcher_registry[cpu_target](
        kkce__xhan)
    wfm__vgi.add_overload(evzea__oxa)
    return wfm__vgi


def _rm_arg_agg_block(block, typemap):
    uwm__bcth = []
    arr_var = None
    for szmys__quxey, qbwas__yxqe in enumerate(block.body):
        if is_assign(qbwas__yxqe) and isinstance(qbwas__yxqe.value, ir.Arg):
            arr_var = qbwas__yxqe.target
            ygeqb__rjvi = typemap[arr_var.name]
            if not isinstance(ygeqb__rjvi, types.ArrayCompatible):
                uwm__bcth += block.body[szmys__quxey + 1:]
                break
            glhc__vopld = block.body[szmys__quxey + 1]
            assert is_assign(glhc__vopld) and isinstance(glhc__vopld.value,
                ir.Expr
                ) and glhc__vopld.value.op == 'getattr' and glhc__vopld.value.attr == 'shape' and glhc__vopld.value.value.name == arr_var.name
            pqo__ldu = glhc__vopld.target
            wrprv__bmi = block.body[szmys__quxey + 2]
            assert is_assign(wrprv__bmi) and isinstance(wrprv__bmi.value,
                ir.Expr
                ) and wrprv__bmi.value.op == 'static_getitem' and wrprv__bmi.value.value.name == pqo__ldu.name
            uwm__bcth += block.body[szmys__quxey + 3:]
            break
        uwm__bcth.append(qbwas__yxqe)
    return uwm__bcth, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    uig__ryc = wrap_parfor_blocks(parfor)
    oeu__vccnu = find_topo_order(uig__ryc)
    oeu__vccnu = oeu__vccnu[1:]
    unwrap_parfor_blocks(parfor)
    for axe__mjcc in reversed(oeu__vccnu):
        for qbwas__yxqe in reversed(parfor.loop_body[axe__mjcc].body):
            if isinstance(qbwas__yxqe, ir.Assign) and (qbwas__yxqe.target.
                name in parfor_params or qbwas__yxqe.target.name in
                var_to_param):
                twrc__cqya = qbwas__yxqe.target.name
                rhs = qbwas__yxqe.value
                xbvme__enr = (twrc__cqya if twrc__cqya in parfor_params else
                    var_to_param[twrc__cqya])
                ymxj__kgbnb = []
                if isinstance(rhs, ir.Var):
                    ymxj__kgbnb = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    ymxj__kgbnb = [fditl__qahmi.name for fditl__qahmi in
                        qbwas__yxqe.value.list_vars()]
                param_uses[xbvme__enr].extend(ymxj__kgbnb)
                for fditl__qahmi in ymxj__kgbnb:
                    var_to_param[fditl__qahmi] = xbvme__enr
            if isinstance(qbwas__yxqe, Parfor):
                get_parfor_reductions(qbwas__yxqe, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for milbx__oytvu, ymxj__kgbnb in param_uses.items():
        if milbx__oytvu in ymxj__kgbnb and milbx__oytvu not in reduce_varnames:
            reduce_varnames.append(milbx__oytvu)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
