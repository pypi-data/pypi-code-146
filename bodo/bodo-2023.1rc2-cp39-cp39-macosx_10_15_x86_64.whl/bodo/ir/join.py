"""IR node for the join and merge"""
from collections import defaultdict
from typing import Dict, List, Literal, Optional, Set, Tuple, Union
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic
import bodo
from bodo.hiframes.table import TableType
from bodo.ir.connector import trim_extra_used_columns
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, cross_join_table, delete_table, hash_join_table, py_data_to_cpp_table
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, get_live_column_nums_block, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import INDEX_SENTINEL, BodoError, MetaType, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, is_str_arr_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        jnuw__vxqi = func.signature
        ppetn__gmiir = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        rfck__mkie = cgutils.get_or_insert_function(builder.module,
            ppetn__gmiir, sym._literal_value)
        builder.call(rfck__mkie, [context.get_constant_null(jnuw__vxqi.args
            [0]), context.get_constant_null(jnuw__vxqi.args[1]), context.
            get_constant_null(jnuw__vxqi.args[2]), context.
            get_constant_null(jnuw__vxqi.args[3]), context.
            get_constant_null(jnuw__vxqi.args[4]), context.
            get_constant_null(jnuw__vxqi.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


HOW_OPTIONS = Literal['inner', 'left', 'right', 'outer', 'asof', 'cross']


class Join(ir.Stmt):

    def __init__(self, left_keys: Union[List[str], str], right_keys: Union[
        List[str], str], out_data_vars: List[ir.Var], out_df_type: bodo.
        DataFrameType, left_vars: List[ir.Var], left_df_type: bodo.
        DataFrameType, right_vars: List[ir.Var], right_df_type: bodo.
        DataFrameType, how: HOW_OPTIONS, suffix_left: str, suffix_right:
        str, loc: ir.Loc, is_left: bool, is_right: bool, is_join: bool,
        left_index: bool, right_index: bool, indicator_col_num: int,
        is_na_equal: bool, gen_cond_expr: str, left_len_var: ir.Var,
        right_len_var: ir.Var):
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.out_col_names = out_df_type.columns
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator_col_num = indicator_col_num
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.left_len_var = left_len_var
        self.right_len_var = right_len_var
        self.n_out_table_cols = len(self.out_col_names)
        self.out_used_cols = set(range(self.n_out_table_cols))
        if self.out_data_vars[1] is not None:
            self.out_used_cols.add(self.n_out_table_cols)
        oycje__vskw = left_df_type.columns
        zuexr__xdwno = right_df_type.columns
        self.left_col_names = oycje__vskw
        self.right_col_names = zuexr__xdwno
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(oycje__vskw) if self.is_left_table else 0
        self.n_right_table_cols = len(zuexr__xdwno
            ) if self.is_right_table else 0
        oam__zse = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        mbkp__rxqw = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(oam__zse)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(mbkp__rxqw)
        self.left_var_map = {wzc__ndbv: ispc__nljk for ispc__nljk,
            wzc__ndbv in enumerate(oycje__vskw)}
        self.right_var_map = {wzc__ndbv: ispc__nljk for ispc__nljk,
            wzc__ndbv in enumerate(zuexr__xdwno)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = oam__zse
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = mbkp__rxqw
        self.left_key_set = set(self.left_var_map[wzc__ndbv] for wzc__ndbv in
            left_keys)
        self.right_key_set = set(self.right_var_map[wzc__ndbv] for
            wzc__ndbv in right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[wzc__ndbv] for
                wzc__ndbv in oycje__vskw if f'(left.{wzc__ndbv})' in
                gen_cond_expr)
            self.right_cond_cols = set(self.right_var_map[wzc__ndbv] for
                wzc__ndbv in zuexr__xdwno if f'(right.{wzc__ndbv})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        gbyly__gupz: int = -1
        hgqes__apsz = set(left_keys) & set(right_keys)
        gwhv__csxy = set(oycje__vskw) & set(zuexr__xdwno)
        dopfl__dsyta = gwhv__csxy - hgqes__apsz
        kua__wzjq: Dict[int, (Literal['left', 'right'], int)] = {}
        ggbog__uvh: Dict[int, int] = {}
        zhx__qwd: Dict[int, int] = {}
        for ispc__nljk, wzc__ndbv in enumerate(oycje__vskw):
            if wzc__ndbv in dopfl__dsyta:
                cstcv__sulk = str(wzc__ndbv) + suffix_left
                tcp__skkx = out_df_type.column_index[cstcv__sulk]
                if (right_index and not left_index and ispc__nljk in self.
                    left_key_set):
                    gbyly__gupz = out_df_type.column_index[wzc__ndbv]
                    kua__wzjq[gbyly__gupz] = 'left', ispc__nljk
            else:
                tcp__skkx = out_df_type.column_index[wzc__ndbv]
            kua__wzjq[tcp__skkx] = 'left', ispc__nljk
            ggbog__uvh[ispc__nljk] = tcp__skkx
        for ispc__nljk, wzc__ndbv in enumerate(zuexr__xdwno):
            if wzc__ndbv not in hgqes__apsz:
                if wzc__ndbv in dopfl__dsyta:
                    mds__kndw = str(wzc__ndbv) + suffix_right
                    tcp__skkx = out_df_type.column_index[mds__kndw]
                    if (left_index and not right_index and ispc__nljk in
                        self.right_key_set):
                        gbyly__gupz = out_df_type.column_index[wzc__ndbv]
                        kua__wzjq[gbyly__gupz] = 'right', ispc__nljk
                else:
                    tcp__skkx = out_df_type.column_index[wzc__ndbv]
                kua__wzjq[tcp__skkx] = 'right', ispc__nljk
                zhx__qwd[ispc__nljk] = tcp__skkx
        if self.left_vars[-1] is not None:
            ggbog__uvh[oam__zse] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            zhx__qwd[mbkp__rxqw] = self.n_out_table_cols
        self.out_to_input_col_map = kua__wzjq
        self.left_to_output_map = ggbog__uvh
        self.right_to_output_map = zhx__qwd
        self.extra_data_col_num = gbyly__gupz
        if self.out_data_vars[1] is not None:
            ojfh__nggm = 'left' if right_index else 'right'
            if ojfh__nggm == 'left':
                tylxz__clojf = oam__zse
            elif ojfh__nggm == 'right':
                tylxz__clojf = mbkp__rxqw
        else:
            ojfh__nggm = None
            tylxz__clojf = -1
        self.index_source = ojfh__nggm
        self.index_col_num = tylxz__clojf
        yhj__fwvyi = []
        and__epa = len(left_keys)
        for ocjus__rsllu in range(and__epa):
            rmljr__eybpq = left_keys[ocjus__rsllu]
            qtx__ygb = right_keys[ocjus__rsllu]
            yhj__fwvyi.append(rmljr__eybpq == qtx__ygb)
        self.vect_same_key = yhj__fwvyi

    @property
    def has_live_left_table_var(self):
        return self.is_left_table and self.left_vars[0] is not None

    @property
    def has_live_right_table_var(self):
        return self.is_right_table and self.right_vars[0] is not None

    @property
    def has_live_out_table_var(self):
        return self.out_data_vars[0] is not None

    @property
    def has_live_out_index_var(self):
        return self.out_data_vars[1] is not None

    def get_out_table_var(self):
        return self.out_data_vars[0]

    def get_out_index_var(self):
        return self.out_data_vars[1]

    def get_live_left_vars(self):
        vars = []
        for ekiv__irizq in self.left_vars:
            if ekiv__irizq is not None:
                vars.append(ekiv__irizq)
        return vars

    def get_live_right_vars(self):
        vars = []
        for ekiv__irizq in self.right_vars:
            if ekiv__irizq is not None:
                vars.append(ekiv__irizq)
        return vars

    def get_live_out_vars(self):
        vars = []
        for ekiv__irizq in self.out_data_vars:
            if ekiv__irizq is not None:
                vars.append(ekiv__irizq)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        fghj__hgv = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[fghj__hgv])
                fghj__hgv += 1
            else:
                left_vars.append(None)
            start = 1
        fph__pgcpp = max(self.n_left_table_cols - 1, 0)
        for ispc__nljk in range(start, len(self.left_vars)):
            if ispc__nljk + fph__pgcpp in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[fghj__hgv])
                fghj__hgv += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        fghj__hgv = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[fghj__hgv])
                fghj__hgv += 1
            else:
                right_vars.append(None)
            start = 1
        fph__pgcpp = max(self.n_right_table_cols - 1, 0)
        for ispc__nljk in range(start, len(self.right_vars)):
            if ispc__nljk + fph__pgcpp in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[fghj__hgv])
                fghj__hgv += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        dgap__ryyiu = [self.has_live_out_table_var, self.has_live_out_index_var
            ]
        fghj__hgv = 0
        for ispc__nljk in range(len(self.out_data_vars)):
            if not dgap__ryyiu[ispc__nljk]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[fghj__hgv])
                fghj__hgv += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {ispc__nljk for ispc__nljk in self.out_used_cols if 
            ispc__nljk < self.n_out_table_cols}

    def __repr__(self):
        cund__yqt = ', '.join([f'{wzc__ndbv}' for wzc__ndbv in self.
            left_col_names])
        dooj__gqt = f'left={{{cund__yqt}}}'
        cund__yqt = ', '.join([f'{wzc__ndbv}' for wzc__ndbv in self.
            right_col_names])
        yiq__wbh = f'right={{{cund__yqt}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, dooj__gqt, yiq__wbh)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    clnq__xusu = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    pukr__nnfpr = []
    jipv__rib = join_node.get_live_left_vars()
    for yinzy__mpcvj in jipv__rib:
        stjrm__cjr = typemap[yinzy__mpcvj.name]
        kbwl__rwo = equiv_set.get_shape(yinzy__mpcvj)
        if kbwl__rwo:
            pukr__nnfpr.append(kbwl__rwo[0])
    if len(pukr__nnfpr) > 1:
        equiv_set.insert_equiv(*pukr__nnfpr)
    pukr__nnfpr = []
    jipv__rib = list(join_node.get_live_right_vars())
    for yinzy__mpcvj in jipv__rib:
        stjrm__cjr = typemap[yinzy__mpcvj.name]
        kbwl__rwo = equiv_set.get_shape(yinzy__mpcvj)
        if kbwl__rwo:
            pukr__nnfpr.append(kbwl__rwo[0])
    if len(pukr__nnfpr) > 1:
        equiv_set.insert_equiv(*pukr__nnfpr)
    pukr__nnfpr = []
    for krb__mbio in join_node.get_live_out_vars():
        stjrm__cjr = typemap[krb__mbio.name]
        gufl__zptiq = array_analysis._gen_shape_call(equiv_set, krb__mbio,
            stjrm__cjr.ndim, None, clnq__xusu)
        equiv_set.insert_equiv(krb__mbio, gufl__zptiq)
        pukr__nnfpr.append(gufl__zptiq[0])
        equiv_set.define(krb__mbio, set())
    if len(pukr__nnfpr) > 1:
        equiv_set.insert_equiv(*pukr__nnfpr)
    return [], clnq__xusu


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    jtwb__svgw = Distribution.OneD
    rxl__wauz = Distribution.OneD
    for yinzy__mpcvj in join_node.get_live_left_vars():
        jtwb__svgw = Distribution(min(jtwb__svgw.value, array_dists[
            yinzy__mpcvj.name].value))
    for yinzy__mpcvj in join_node.get_live_right_vars():
        rxl__wauz = Distribution(min(rxl__wauz.value, array_dists[
            yinzy__mpcvj.name].value))
    abqg__grze = Distribution.OneD_Var
    for krb__mbio in join_node.get_live_out_vars():
        if krb__mbio.name in array_dists:
            abqg__grze = Distribution(min(abqg__grze.value, array_dists[
                krb__mbio.name].value))
    ybv__mvrl = Distribution(min(abqg__grze.value, jtwb__svgw.value))
    hibtx__hpyf = Distribution(min(abqg__grze.value, rxl__wauz.value))
    abqg__grze = Distribution(max(ybv__mvrl.value, hibtx__hpyf.value))
    for krb__mbio in join_node.get_live_out_vars():
        array_dists[krb__mbio.name] = abqg__grze
    if abqg__grze != Distribution.OneD_Var:
        jtwb__svgw = abqg__grze
        rxl__wauz = abqg__grze
    for yinzy__mpcvj in join_node.get_live_left_vars():
        array_dists[yinzy__mpcvj.name] = jtwb__svgw
    for yinzy__mpcvj in join_node.get_live_right_vars():
        array_dists[yinzy__mpcvj.name] = rxl__wauz
    join_node.left_dist = jtwb__svgw
    join_node.right_dist = rxl__wauz


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(ekiv__irizq, callback,
        cbdata) for ekiv__irizq in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(ekiv__irizq, callback,
        cbdata) for ekiv__irizq in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(ekiv__irizq,
        callback, cbdata) for ekiv__irizq in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = visit_vars_inner(join_node.left_len_var,
            callback, cbdata)
        join_node.right_len_var = visit_vars_inner(join_node.right_len_var,
            callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def _is_cross_join_len(join_node):
    return (join_node.how == 'cross' and not join_node.out_used_cols and
        join_node.has_live_out_table_var and not join_node.
        has_live_out_index_var)


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if join_node.has_live_out_table_var:
        iuli__rmk = []
        gbj__ruto = join_node.get_out_table_var()
        if gbj__ruto.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for axpd__nswg in join_node.out_to_input_col_map.keys():
            if axpd__nswg in join_node.out_used_cols:
                continue
            iuli__rmk.append(axpd__nswg)
            if join_node.indicator_col_num == axpd__nswg:
                join_node.indicator_col_num = -1
                continue
            if axpd__nswg == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            cjsfh__cjgj, axpd__nswg = join_node.out_to_input_col_map[axpd__nswg
                ]
            if cjsfh__cjgj == 'left':
                if (axpd__nswg not in join_node.left_key_set and axpd__nswg
                     not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(axpd__nswg)
                    if not join_node.is_left_table:
                        join_node.left_vars[axpd__nswg] = None
            elif cjsfh__cjgj == 'right':
                if (axpd__nswg not in join_node.right_key_set and 
                    axpd__nswg not in join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(axpd__nswg)
                    if not join_node.is_right_table:
                        join_node.right_vars[axpd__nswg] = None
        for ispc__nljk in iuli__rmk:
            del join_node.out_to_input_col_map[ispc__nljk]
        if join_node.is_left_table:
            ofpn__oiow = set(range(join_node.n_left_table_cols))
            gdut__hpif = not bool(ofpn__oiow - join_node.left_dead_var_inds)
            if gdut__hpif:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            ofpn__oiow = set(range(join_node.n_right_table_cols))
            gdut__hpif = not bool(ofpn__oiow - join_node.right_dead_var_inds)
            if gdut__hpif:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        auhl__mbeur = join_node.get_out_index_var()
        if auhl__mbeur.name not in lives:
            join_node.out_data_vars[1] = None
            join_node.out_used_cols.remove(join_node.n_out_table_cols)
            if join_node.index_source == 'left':
                if (join_node.index_col_num not in join_node.left_key_set and
                    join_node.index_col_num not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(join_node.index_col_num)
                    join_node.left_vars[-1] = None
            elif join_node.index_col_num not in join_node.right_key_set and join_node.index_col_num not in join_node.right_cond_cols:
                join_node.right_dead_var_inds.add(join_node.index_col_num)
                join_node.right_vars[-1] = None
    if not (join_node.has_live_out_table_var or join_node.
        has_live_out_index_var):
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_remove_dead_column(join_node, column_live_map, equiv_vars, typemap):
    pezhw__xpyab = False
    if join_node.has_live_out_table_var:
        yokf__zvprn = join_node.get_out_table_var().name
        szs__mcye, emm__rwcz, roqoj__gssjx = get_live_column_nums_block(
            column_live_map, equiv_vars, yokf__zvprn)
        if not (emm__rwcz or roqoj__gssjx):
            szs__mcye = trim_extra_used_columns(szs__mcye, join_node.
                n_out_table_cols)
            ewvry__olw = join_node.get_out_table_used_cols()
            if len(szs__mcye) != len(ewvry__olw):
                pezhw__xpyab = not (join_node.is_left_table and join_node.
                    is_right_table)
                bkmef__kio = ewvry__olw - szs__mcye
                join_node.out_used_cols = join_node.out_used_cols - bkmef__kio
    return pezhw__xpyab


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        zzqha__hdql = join_node.get_out_table_var()
        jjgim__jkb, emm__rwcz, roqoj__gssjx = _compute_table_column_uses(
            zzqha__hdql.name, table_col_use_map, equiv_vars)
    else:
        jjgim__jkb, emm__rwcz, roqoj__gssjx = set(), False, False
    if join_node.has_live_left_table_var:
        beh__tbgc = join_node.left_vars[0].name
        weze__nks, hmp__jii, tgxa__tgp = block_use_map[beh__tbgc]
        if not (hmp__jii or tgxa__tgp):
            ida__htv = set([join_node.out_to_input_col_map[ispc__nljk][1] for
                ispc__nljk in jjgim__jkb if join_node.out_to_input_col_map[
                ispc__nljk][0] == 'left'])
            aek__xbdo = set(ispc__nljk for ispc__nljk in join_node.
                left_key_set | join_node.left_cond_cols if ispc__nljk <
                join_node.n_left_table_cols)
            if not (emm__rwcz or roqoj__gssjx):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (ida__htv | aek__xbdo)
            block_use_map[beh__tbgc] = (weze__nks | ida__htv | aek__xbdo, 
                emm__rwcz or roqoj__gssjx, False)
    if join_node.has_live_right_table_var:
        vmx__ykc = join_node.right_vars[0].name
        weze__nks, hmp__jii, tgxa__tgp = block_use_map[vmx__ykc]
        if not (hmp__jii or tgxa__tgp):
            lfga__yrzmm = set([join_node.out_to_input_col_map[ispc__nljk][1
                ] for ispc__nljk in jjgim__jkb if join_node.
                out_to_input_col_map[ispc__nljk][0] == 'right'])
            kdknh__bfxg = set(ispc__nljk for ispc__nljk in join_node.
                right_key_set | join_node.right_cond_cols if ispc__nljk <
                join_node.n_right_table_cols)
            if not (emm__rwcz or roqoj__gssjx):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (lfga__yrzmm | kdknh__bfxg)
            block_use_map[vmx__ykc] = (weze__nks | lfga__yrzmm |
                kdknh__bfxg, emm__rwcz or roqoj__gssjx, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({gifx__jpz.name for gifx__jpz in join_node.
        get_live_left_vars()})
    use_set.update({gifx__jpz.name for gifx__jpz in join_node.
        get_live_right_vars()})
    def_set.update({gifx__jpz.name for gifx__jpz in join_node.
        get_live_out_vars()})
    if join_node.how == 'cross':
        use_set.add(join_node.left_len_var.name)
        use_set.add(join_node.right_len_var.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    dcy__ffftm = set(gifx__jpz.name for gifx__jpz in join_node.
        get_live_out_vars())
    return set(), dcy__ffftm


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(ekiv__irizq, var_dict) for
        ekiv__irizq in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(ekiv__irizq, var_dict
        ) for ekiv__irizq in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(ekiv__irizq,
        var_dict) for ekiv__irizq in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = replace_vars_inner(join_node.left_len_var,
            var_dict)
        join_node.right_len_var = replace_vars_inner(join_node.
            right_len_var, var_dict)


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for yinzy__mpcvj in join_node.get_live_out_vars():
        definitions[yinzy__mpcvj.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def _gen_cross_join_len(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel):
    func_text = 'def f(left_len, right_len):\n'
    jem__ddlcr = 'bodo.libs.distributed_api.get_size()'
    nkexx__nydzx = 'bodo.libs.distributed_api.get_rank()'
    if left_parallel:
        func_text += f"""  left_len = bodo.libs.distributed_api.get_node_portion(left_len, {jem__ddlcr}, {nkexx__nydzx})
"""
    if right_parallel and not left_parallel:
        func_text += f"""  right_len = bodo.libs.distributed_api.get_node_portion(right_len, {jem__ddlcr}, {nkexx__nydzx})
"""
    func_text += '  n_rows = left_len * right_len\n'
    func_text += '  py_table = init_table(py_table_type, False)\n'
    func_text += '  py_table = set_table_len(py_table, n_rows)\n'
    gxhr__xpus = {}
    exec(func_text, {}, gxhr__xpus)
    pgmb__vdta = gxhr__xpus['f']
    glbs = {'py_table_type': out_table_type, 'init_table': bodo.hiframes.
        table.init_table, 'set_table_len': bodo.hiframes.table.
        set_table_len, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value), 'bodo': bodo}
    dty__wdryc = [join_node.left_len_var, join_node.right_len_var]
    wkr__yewx = tuple(typemap[gifx__jpz.name] for gifx__jpz in dty__wdryc)
    ydtw__jlyxa = compile_to_numba_ir(pgmb__vdta, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=wkr__yewx, typemap=typemap, calltypes
        =calltypes).blocks.popitem()[1]
    replace_arg_nodes(ydtw__jlyxa, dty__wdryc)
    omb__yhlj = ydtw__jlyxa.body[:-3]
    omb__yhlj[-1].target = join_node.out_data_vars[0]
    return omb__yhlj


def _gen_cross_join_repeat(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel, left_is_dead):
    jipv__rib = join_node.right_vars if left_is_dead else join_node.left_vars
    unkrr__zphog = ', '.join(f't{ispc__nljk}' for ispc__nljk in range(len(
        jipv__rib)) if jipv__rib[ispc__nljk] is not None)
    shi__fwk = len(join_node.right_col_names) if left_is_dead else len(
        join_node.left_col_names)
    yjex__wff = (join_node.is_right_table if left_is_dead else join_node.
        is_left_table)
    ufz__bjp = (join_node.right_dead_var_inds if left_is_dead else
        join_node.left_dead_var_inds)
    ihu__sdcfe = [(f'get_table_data(t0, {ispc__nljk})' if yjex__wff else
        f't{ispc__nljk}') for ispc__nljk in range(shi__fwk)]
    kck__mtm = ', '.join(
        f'bodo.libs.array_kernels.repeat_kernel({ihu__sdcfe[ispc__nljk]}, repeats)'
         if ispc__nljk not in ufz__bjp else 'None' for ispc__nljk in range(
        shi__fwk))
    hlent__kyei = len(out_table_type.arr_types)
    ouqv__vwimj = [join_node.out_to_input_col_map.get(ispc__nljk, (-1, -1))
        [1] for ispc__nljk in range(hlent__kyei)]
    jem__ddlcr = 'bodo.libs.distributed_api.get_size()'
    nkexx__nydzx = 'bodo.libs.distributed_api.get_rank()'
    gtz__oiecz = 'left_len' if left_is_dead else 'right_len'
    brdp__uvlv = right_parallel if left_is_dead else left_parallel
    losc__qxfa = left_parallel if left_is_dead else right_parallel
    gasg__ungen = not brdp__uvlv and losc__qxfa
    vsd__bpc = (
        f'bodo.libs.distributed_api.get_node_portion({gtz__oiecz}, {jem__ddlcr}, {nkexx__nydzx})'
         if gasg__ungen else gtz__oiecz)
    func_text = f'def f({unkrr__zphog}, left_len, right_len):\n'
    func_text += f'  repeats = {vsd__bpc}\n'
    func_text += f'  out_data = ({kck__mtm},)\n'
    func_text += f"""  py_table = logical_table_to_table(out_data, (), col_inds, {shi__fwk}, out_table_type, used_cols)
"""
    gxhr__xpus = {}
    exec(func_text, {}, gxhr__xpus)
    pgmb__vdta = gxhr__xpus['f']
    glbs = {'out_table_type': out_table_type, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value), 'bodo': bodo, 'used_cols':
        bodo.utils.typing.MetaType(tuple(join_node.out_used_cols)),
        'col_inds': bodo.utils.typing.MetaType(tuple(ouqv__vwimj)),
        'logical_table_to_table': bodo.hiframes.table.
        logical_table_to_table, 'get_table_data': bodo.hiframes.table.
        get_table_data}
    dty__wdryc = [gifx__jpz for gifx__jpz in jipv__rib if gifx__jpz is not None
        ] + [join_node.left_len_var, join_node.right_len_var]
    wkr__yewx = tuple(typemap[gifx__jpz.name] for gifx__jpz in dty__wdryc)
    ydtw__jlyxa = compile_to_numba_ir(pgmb__vdta, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=wkr__yewx, typemap=typemap, calltypes
        =calltypes).blocks.popitem()[1]
    replace_arg_nodes(ydtw__jlyxa, dty__wdryc)
    omb__yhlj = ydtw__jlyxa.body[:-3]
    omb__yhlj[-1].target = join_node.out_data_vars[0]
    return omb__yhlj


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        lsa__yeza = join_node.loc.strformat()
        qtco__lstn = [join_node.left_col_names[ispc__nljk] for ispc__nljk in
            sorted(set(range(len(join_node.left_col_names))) - join_node.
            left_dead_var_inds)]
        lwqmd__ekw = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', lwqmd__ekw,
            lsa__yeza, qtco__lstn)
        ooluz__xljd = [join_node.right_col_names[ispc__nljk] for ispc__nljk in
            sorted(set(range(len(join_node.right_col_names))) - join_node.
            right_dead_var_inds)]
        lwqmd__ekw = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', lwqmd__ekw,
            lsa__yeza, ooluz__xljd)
        ssgdz__lny = [join_node.out_col_names[ispc__nljk] for ispc__nljk in
            sorted(join_node.get_out_table_used_cols())]
        lwqmd__ekw = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', lwqmd__ekw,
            lsa__yeza, ssgdz__lny)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    and__epa = len(join_node.left_keys)
    out_physical_to_logical_list = []
    if join_node.has_live_out_table_var:
        out_table_type = typemap[join_node.get_out_table_var().name]
    else:
        out_table_type = types.none
    if join_node.has_live_out_index_var:
        index_col_type = typemap[join_node.get_out_index_var().name]
    else:
        index_col_type = types.none
    if _is_cross_join_len(join_node):
        return _gen_cross_join_len(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel)
    elif join_node.how == 'cross' and all(ispc__nljk in join_node.
        left_dead_var_inds for ispc__nljk in range(len(join_node.
        left_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            True)
    elif join_node.how == 'cross' and all(ispc__nljk in join_node.
        right_dead_var_inds for ispc__nljk in range(len(join_node.
        right_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            False)
    if join_node.extra_data_col_num != -1:
        out_physical_to_logical_list.append(join_node.extra_data_col_num)
    left_key_in_output = []
    right_key_in_output = []
    left_used_key_nums = set()
    right_used_key_nums = set()
    ttxtt__ubxx = set()
    gthwb__awo = set()
    left_logical_physical_map = {}
    right_logical_physical_map = {}
    left_physical_to_logical_list = []
    right_physical_to_logical_list = []
    crflb__dmxcr = 0
    xssl__lrult = 0
    wpt__jronq = []
    for vqlx__aao, wzc__ndbv in enumerate(join_node.left_keys):
        ipl__kps = join_node.left_var_map[wzc__ndbv]
        if not join_node.is_left_table:
            wpt__jronq.append(join_node.left_vars[ipl__kps])
        dgap__ryyiu = 1
        tcp__skkx = join_node.left_to_output_map[ipl__kps]
        if wzc__ndbv == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == ipl__kps):
                out_physical_to_logical_list.append(tcp__skkx)
                left_used_key_nums.add(vqlx__aao)
                ttxtt__ubxx.add(ipl__kps)
            else:
                dgap__ryyiu = 0
        elif tcp__skkx not in join_node.out_used_cols:
            dgap__ryyiu = 0
        elif ipl__kps in ttxtt__ubxx:
            dgap__ryyiu = 0
        else:
            left_used_key_nums.add(vqlx__aao)
            ttxtt__ubxx.add(ipl__kps)
            out_physical_to_logical_list.append(tcp__skkx)
        left_physical_to_logical_list.append(ipl__kps)
        left_logical_physical_map[ipl__kps] = crflb__dmxcr
        crflb__dmxcr += 1
        left_key_in_output.append(dgap__ryyiu)
    wpt__jronq = tuple(wpt__jronq)
    ohjni__eercx = []
    for ispc__nljk in range(len(join_node.left_col_names)):
        if (ispc__nljk not in join_node.left_dead_var_inds and ispc__nljk
             not in join_node.left_key_set):
            if not join_node.is_left_table:
                gifx__jpz = join_node.left_vars[ispc__nljk]
                ohjni__eercx.append(gifx__jpz)
            ymf__bvoi = 1
            rzsel__ngi = 1
            tcp__skkx = join_node.left_to_output_map[ispc__nljk]
            if ispc__nljk in join_node.left_cond_cols:
                if tcp__skkx not in join_node.out_used_cols:
                    ymf__bvoi = 0
                left_key_in_output.append(ymf__bvoi)
            elif ispc__nljk in join_node.left_dead_var_inds:
                ymf__bvoi = 0
                rzsel__ngi = 0
            if ymf__bvoi:
                out_physical_to_logical_list.append(tcp__skkx)
            if rzsel__ngi:
                left_physical_to_logical_list.append(ispc__nljk)
                left_logical_physical_map[ispc__nljk] = crflb__dmxcr
                crflb__dmxcr += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            ohjni__eercx.append(join_node.left_vars[join_node.index_col_num])
        tcp__skkx = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(tcp__skkx)
        left_physical_to_logical_list.append(join_node.index_col_num)
    ohjni__eercx = tuple(ohjni__eercx)
    if join_node.is_left_table:
        ohjni__eercx = tuple(join_node.get_live_left_vars())
    nbvyq__hyk = []
    for vqlx__aao, wzc__ndbv in enumerate(join_node.right_keys):
        ipl__kps = join_node.right_var_map[wzc__ndbv]
        if not join_node.is_right_table:
            nbvyq__hyk.append(join_node.right_vars[ipl__kps])
        if not join_node.vect_same_key[vqlx__aao] and not join_node.is_join:
            dgap__ryyiu = 1
            if ipl__kps not in join_node.right_to_output_map:
                dgap__ryyiu = 0
            else:
                tcp__skkx = join_node.right_to_output_map[ipl__kps]
                if wzc__ndbv == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        ipl__kps):
                        out_physical_to_logical_list.append(tcp__skkx)
                        right_used_key_nums.add(vqlx__aao)
                        gthwb__awo.add(ipl__kps)
                    else:
                        dgap__ryyiu = 0
                elif tcp__skkx not in join_node.out_used_cols:
                    dgap__ryyiu = 0
                elif ipl__kps in gthwb__awo:
                    dgap__ryyiu = 0
                else:
                    right_used_key_nums.add(vqlx__aao)
                    gthwb__awo.add(ipl__kps)
                    out_physical_to_logical_list.append(tcp__skkx)
            right_key_in_output.append(dgap__ryyiu)
        right_physical_to_logical_list.append(ipl__kps)
        right_logical_physical_map[ipl__kps] = xssl__lrult
        xssl__lrult += 1
    nbvyq__hyk = tuple(nbvyq__hyk)
    svtk__npcs = []
    for ispc__nljk in range(len(join_node.right_col_names)):
        if (ispc__nljk not in join_node.right_dead_var_inds and ispc__nljk
             not in join_node.right_key_set):
            if not join_node.is_right_table:
                svtk__npcs.append(join_node.right_vars[ispc__nljk])
            ymf__bvoi = 1
            rzsel__ngi = 1
            tcp__skkx = join_node.right_to_output_map[ispc__nljk]
            if ispc__nljk in join_node.right_cond_cols:
                if tcp__skkx not in join_node.out_used_cols:
                    ymf__bvoi = 0
                right_key_in_output.append(ymf__bvoi)
            elif ispc__nljk in join_node.right_dead_var_inds:
                ymf__bvoi = 0
                rzsel__ngi = 0
            if ymf__bvoi:
                out_physical_to_logical_list.append(tcp__skkx)
            if rzsel__ngi:
                right_physical_to_logical_list.append(ispc__nljk)
                right_logical_physical_map[ispc__nljk] = xssl__lrult
                xssl__lrult += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            svtk__npcs.append(join_node.right_vars[join_node.index_col_num])
        tcp__skkx = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(tcp__skkx)
        right_physical_to_logical_list.append(join_node.index_col_num)
    svtk__npcs = tuple(svtk__npcs)
    if join_node.is_right_table:
        svtk__npcs = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    dty__wdryc = wpt__jronq + nbvyq__hyk + ohjni__eercx + svtk__npcs
    wkr__yewx = tuple(typemap[gifx__jpz.name] for gifx__jpz in dty__wdryc)
    left_other_names = tuple('t1_c' + str(ispc__nljk) for ispc__nljk in
        range(len(ohjni__eercx)))
    right_other_names = tuple('t2_c' + str(ispc__nljk) for ispc__nljk in
        range(len(svtk__npcs)))
    if join_node.is_left_table:
        dwgj__qtwff = ()
    else:
        dwgj__qtwff = tuple('t1_key' + str(ispc__nljk) for ispc__nljk in
            range(and__epa))
    if join_node.is_right_table:
        xhoq__odmq = ()
    else:
        xhoq__odmq = tuple('t2_key' + str(ispc__nljk) for ispc__nljk in
            range(and__epa))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(dwgj__qtwff + xhoq__odmq +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            keeqp__wmyoq = typemap[join_node.left_vars[0].name]
        else:
            keeqp__wmyoq = types.none
        for uzcw__qoaa in left_physical_to_logical_list:
            if uzcw__qoaa < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                stjrm__cjr = keeqp__wmyoq.arr_types[uzcw__qoaa]
            else:
                stjrm__cjr = typemap[join_node.left_vars[-1].name]
            if uzcw__qoaa in join_node.left_key_set:
                left_key_types.append(stjrm__cjr)
            else:
                left_other_types.append(stjrm__cjr)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[gifx__jpz.name] for gifx__jpz in
            wpt__jronq)
        left_other_types = tuple([typemap[wzc__ndbv.name] for wzc__ndbv in
            ohjni__eercx])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            keeqp__wmyoq = typemap[join_node.right_vars[0].name]
        else:
            keeqp__wmyoq = types.none
        for uzcw__qoaa in right_physical_to_logical_list:
            if uzcw__qoaa < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                stjrm__cjr = keeqp__wmyoq.arr_types[uzcw__qoaa]
            else:
                stjrm__cjr = typemap[join_node.right_vars[-1].name]
            if uzcw__qoaa in join_node.right_key_set:
                right_key_types.append(stjrm__cjr)
            else:
                right_other_types.append(stjrm__cjr)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[gifx__jpz.name] for gifx__jpz in
            nbvyq__hyk)
        right_other_types = tuple([typemap[wzc__ndbv.name] for wzc__ndbv in
            svtk__npcs])
    matched_key_types = []
    for ispc__nljk in range(and__epa):
        subfi__imvbt = _match_join_key_types(left_key_types[ispc__nljk],
            right_key_types[ispc__nljk], loc)
        glbs[f'key_type_{ispc__nljk}'] = subfi__imvbt
        matched_key_types.append(subfi__imvbt)
    if join_node.is_left_table:
        yiqp__cdulq = determine_table_cast_map(matched_key_types,
            left_key_types, None, {ispc__nljk: join_node.left_var_map[
            rrxmh__hgrpl] for ispc__nljk, rrxmh__hgrpl in enumerate(
            join_node.left_keys)}, True)
        if yiqp__cdulq:
            zwbeq__xsk = False
            qcmbn__dfe = False
            yxs__gnli = None
            if join_node.has_live_left_table_var:
                gwjq__ejv = list(typemap[join_node.left_vars[0].name].arr_types
                    )
            else:
                gwjq__ejv = None
            for axpd__nswg, stjrm__cjr in yiqp__cdulq.items():
                if axpd__nswg < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    gwjq__ejv[axpd__nswg] = stjrm__cjr
                    zwbeq__xsk = True
                else:
                    yxs__gnli = stjrm__cjr
                    qcmbn__dfe = True
            if zwbeq__xsk:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(gwjq__ejv))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if qcmbn__dfe:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = yxs__gnli
    else:
        func_text += '    t1_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({dwgj__qtwff[ispc__nljk]}, key_type_{ispc__nljk})'
             if left_key_types[ispc__nljk] != matched_key_types[ispc__nljk]
             else f'{dwgj__qtwff[ispc__nljk]}' for ispc__nljk in range(
            and__epa)), ',' if and__epa != 0 else '')
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        yiqp__cdulq = determine_table_cast_map(matched_key_types,
            right_key_types, None, {ispc__nljk: join_node.right_var_map[
            rrxmh__hgrpl] for ispc__nljk, rrxmh__hgrpl in enumerate(
            join_node.right_keys)}, True)
        if yiqp__cdulq:
            zwbeq__xsk = False
            qcmbn__dfe = False
            yxs__gnli = None
            if join_node.has_live_right_table_var:
                gwjq__ejv = list(typemap[join_node.right_vars[0].name].
                    arr_types)
            else:
                gwjq__ejv = None
            for axpd__nswg, stjrm__cjr in yiqp__cdulq.items():
                if axpd__nswg < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    gwjq__ejv[axpd__nswg] = stjrm__cjr
                    zwbeq__xsk = True
                else:
                    yxs__gnli = stjrm__cjr
                    qcmbn__dfe = True
            if zwbeq__xsk:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(gwjq__ejv))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if qcmbn__dfe:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = yxs__gnli
    else:
        func_text += '    t2_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({xhoq__odmq[ispc__nljk]}, key_type_{ispc__nljk})'
             if right_key_types[ispc__nljk] != matched_key_types[ispc__nljk
            ] else f'{xhoq__odmq[ispc__nljk]}' for ispc__nljk in range(
            and__epa)), ',' if and__epa != 0 else '')
        func_text += '    data_right = ({}{})\n'.format(','.join(
            right_other_names), ',' if len(right_other_names) != 0 else '')
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap,
        left_logical_physical_map, right_logical_physical_map))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel, 'pd.merge_asof requires both left and right to be replicated or distributed'
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_join_cpp_call(join_node, left_key_types,
            right_key_types, matched_key_types, left_other_names,
            right_other_names, left_other_types, right_other_types,
            left_key_in_output, right_key_in_output, left_parallel,
            right_parallel, glbs, out_physical_to_logical_list,
            out_table_type, index_col_type, join_node.
            get_out_table_used_cols(), left_used_key_nums,
            right_used_key_nums, general_cond_cfunc, left_col_nums,
            right_col_nums, left_physical_to_logical_list,
            right_physical_to_logical_list)
    if join_node.how == 'asof':
        for ispc__nljk in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(ispc__nljk,
                ispc__nljk)
        for ispc__nljk in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                ispc__nljk, ispc__nljk)
        for ispc__nljk in range(and__epa):
            func_text += (
                f'    t1_keys_{ispc__nljk} = out_t1_keys[{ispc__nljk}]\n')
        for ispc__nljk in range(and__epa):
            func_text += (
                f'    t2_keys_{ispc__nljk} = out_t2_keys[{ispc__nljk}]\n')
    gxhr__xpus = {}
    exec(func_text, {}, gxhr__xpus)
    pgmb__vdta = gxhr__xpus['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'cross_join_table': cross_join_table, 'hash_join_table':
        hash_join_table, 'delete_table': delete_table,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr, 'key_in_output': np.array
        (left_key_in_output + right_key_in_output, dtype=np.bool_),
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    ydtw__jlyxa = compile_to_numba_ir(pgmb__vdta, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=wkr__yewx, typemap=typemap, calltypes
        =calltypes).blocks.popitem()[1]
    replace_arg_nodes(ydtw__jlyxa, dty__wdryc)
    omb__yhlj = ydtw__jlyxa.body[:-3]
    if join_node.has_live_out_index_var:
        omb__yhlj[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        omb__yhlj[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        omb__yhlj.pop(-1)
    elif not join_node.has_live_out_table_var:
        omb__yhlj.pop(-2)
    return omb__yhlj


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    gmu__yrtd = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{gmu__yrtd}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        left_logical_physical_map, join_node.left_var_map, typemap,
        join_node.left_vars, table_getitem_funcs, func_text, 'left',
        join_node.left_key_set, na_check_name, join_node.is_left_table)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        right_logical_physical_map, join_node.right_var_map, typemap,
        join_node.right_vars, table_getitem_funcs, func_text, 'right',
        join_node.right_key_set, na_check_name, join_node.is_right_table)
    expr = expr.replace(' & ', ' and ').replace(' | ', ' or ')
    func_text += f'  return {expr}'
    gxhr__xpus = {}
    exec(func_text, table_getitem_funcs, gxhr__xpus)
    ndqb__xnjr = gxhr__xpus[f'bodo_join_gen_cond{gmu__yrtd}']
    heien__tuhk = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    lwg__cpwq = numba.cfunc(heien__tuhk, nopython=True)(ndqb__xnjr)
    join_gen_cond_cfunc[lwg__cpwq.native_name] = lwg__cpwq
    join_gen_cond_cfunc_addr[lwg__cpwq.native_name] = lwg__cpwq.address
    return lwg__cpwq, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    jsz__qwhu = []
    for wzc__ndbv, yutzy__bqp in name_to_var_map.items():
        ugl__qizxy = f'({table_name}.{wzc__ndbv})'
        if ugl__qizxy not in expr:
            continue
        gimof__bnz = f'getitem_{table_name}_val_{yutzy__bqp}'
        if is_table_var:
            vks__egk = typemap[col_vars[0].name].arr_types[yutzy__bqp]
        else:
            vks__egk = typemap[col_vars[yutzy__bqp].name]
        if is_str_arr_type(vks__egk) or vks__egk == bodo.binary_array_type:
            egjn__vlkb = (
                f'{gimof__bnz}({table_name}_table, {table_name}_ind)\n')
        else:
            egjn__vlkb = (
                f'{gimof__bnz}({table_name}_data1, {table_name}_ind)\n')
        ekgw__qtlpg = logical_to_physical_ind[yutzy__bqp]
        table_getitem_funcs[gimof__bnz
            ] = bodo.libs.array._gen_row_access_intrinsic(vks__egk, ekgw__qtlpg
            )
        expr = expr.replace(ugl__qizxy, egjn__vlkb)
        xnz__idsk = f'({na_check_name}.{table_name}.{wzc__ndbv})'
        if xnz__idsk in expr:
            avwu__ihotz = f'nacheck_{table_name}_val_{yutzy__bqp}'
            pytz__vag = f'_bodo_isna_{table_name}_val_{yutzy__bqp}'
            if isinstance(vks__egk, (bodo.libs.int_arr_ext.IntegerArrayType,
                bodo.FloatingArrayType, bodo.TimeArrayType)) or vks__egk in (
                bodo.libs.bool_arr_ext.boolean_array, bodo.
                binary_array_type, bodo.datetime_date_array_type
                ) or is_str_arr_type(vks__egk):
                func_text += f"""  {pytz__vag} = {avwu__ihotz}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {pytz__vag} = {avwu__ihotz}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[avwu__ihotz
                ] = bodo.libs.array._gen_row_na_check_intrinsic(vks__egk,
                ekgw__qtlpg)
            expr = expr.replace(xnz__idsk, pytz__vag)
        if yutzy__bqp not in key_set:
            jsz__qwhu.append(ekgw__qtlpg)
    return expr, func_text, jsz__qwhu


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as buv__ofkg:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    cvh__pwmg = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[gifx__jpz.name] in cvh__pwmg for
        gifx__jpz in join_node.get_live_left_vars())
    if not join_node.get_live_left_vars():
        assert join_node.how == 'cross', 'cross join expected if left data is dead'
        left_parallel = join_node.left_dist in cvh__pwmg
    right_parallel = all(array_dists[gifx__jpz.name] in cvh__pwmg for
        gifx__jpz in join_node.get_live_right_vars())
    if not join_node.get_live_right_vars():
        assert join_node.how == 'cross', 'cross join expected if right data is dead'
        right_parallel = join_node.right_dist in cvh__pwmg
    if not left_parallel:
        assert not any(array_dists[gifx__jpz.name] in cvh__pwmg for
            gifx__jpz in join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[gifx__jpz.name] in cvh__pwmg for
            gifx__jpz in join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[gifx__jpz.name] in cvh__pwmg for gifx__jpz in
            join_node.get_live_out_vars())
    return left_parallel, right_parallel


def _gen_join_cpp_call(join_node, left_key_types, right_key_types,
    matched_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, left_key_in_output,
    right_key_in_output, left_parallel, right_parallel, glbs,
    out_physical_to_logical_list, out_table_type, index_col_type,
    out_table_used_cols, left_used_key_nums, right_used_key_nums,
    general_cond_cfunc, left_col_nums, right_col_nums,
    left_physical_to_logical_list, right_physical_to_logical_list):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    ios__eplr = set(left_col_nums)
    cmq__imzm = set(right_col_nums)
    yhj__fwvyi = join_node.vect_same_key
    hvyc__ixqpc = []
    for ispc__nljk in range(len(left_key_types)):
        if left_key_in_output[ispc__nljk]:
            hvyc__ixqpc.append(needs_typechange(matched_key_types[
                ispc__nljk], join_node.is_right, yhj__fwvyi[ispc__nljk]))
    wixo__nmu = len(left_key_types)
    laq__vyyub = 0
    zlht__edt = left_physical_to_logical_list[len(left_key_types):]
    for ispc__nljk, uzcw__qoaa in enumerate(zlht__edt):
        lixh__flkwk = True
        if uzcw__qoaa in ios__eplr:
            lixh__flkwk = left_key_in_output[wixo__nmu]
            wixo__nmu += 1
        if lixh__flkwk:
            hvyc__ixqpc.append(needs_typechange(left_other_types[ispc__nljk
                ], join_node.is_right, False))
    for ispc__nljk in range(len(right_key_types)):
        if not yhj__fwvyi[ispc__nljk] and not join_node.is_join:
            if right_key_in_output[laq__vyyub]:
                hvyc__ixqpc.append(needs_typechange(matched_key_types[
                    ispc__nljk], join_node.is_left, False))
            laq__vyyub += 1
    nfalk__vbzf = right_physical_to_logical_list[len(right_key_types):]
    for ispc__nljk, uzcw__qoaa in enumerate(nfalk__vbzf):
        lixh__flkwk = True
        if uzcw__qoaa in cmq__imzm:
            lixh__flkwk = right_key_in_output[laq__vyyub]
            laq__vyyub += 1
        if lixh__flkwk:
            hvyc__ixqpc.append(needs_typechange(right_other_types[
                ispc__nljk], join_node.is_left, False))
    and__epa = len(left_key_types)
    func_text = '    # beginning of _gen_join_cpp_call\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            xwnzv__vqicg = left_other_names[1:]
            gbj__ruto = left_other_names[0]
        else:
            xwnzv__vqicg = left_other_names
            gbj__ruto = None
        lmhv__ndxg = '()' if len(xwnzv__vqicg
            ) == 0 else f'({xwnzv__vqicg[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({gbj__ruto}, {lmhv__ndxg}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        xrc__esu = []
        for ispc__nljk in range(and__epa):
            xrc__esu.append('t1_keys[{}]'.format(ispc__nljk))
        for ispc__nljk in range(len(left_other_names)):
            xrc__esu.append('data_left[{}]'.format(ispc__nljk))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(xkt__xwljq) for xkt__xwljq in xrc__esu))
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            qmq__phajx = right_other_names[1:]
            gbj__ruto = right_other_names[0]
        else:
            qmq__phajx = right_other_names
            gbj__ruto = None
        lmhv__ndxg = '()' if len(qmq__phajx) == 0 else f'({qmq__phajx[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({gbj__ruto}, {lmhv__ndxg}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        flef__ygjm = []
        for ispc__nljk in range(and__epa):
            flef__ygjm.append('t2_keys[{}]'.format(ispc__nljk))
        for ispc__nljk in range(len(right_other_names)):
            flef__ygjm.append('data_right[{}]'.format(ispc__nljk))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(xkt__xwljq) for xkt__xwljq in
            flef__ygjm))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(yhj__fwvyi, dtype=np.int64)
    glbs['use_nullable_arr_type'] = np.array(hvyc__ixqpc, dtype=np.int64)
    glbs['left_table_cond_columns'] = np.array(left_col_nums if len(
        left_col_nums) > 0 else [-1], dtype=np.int64)
    glbs['right_table_cond_columns'] = np.array(right_col_nums if len(
        right_col_nums) > 0 else [-1], dtype=np.int64)
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    if join_node.how == 'cross' or not join_node.left_keys:
        func_text += f"""    out_table = cross_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {join_node.is_left}, {join_node.is_right}, key_in_output.ctypes, use_nullable_arr_type.ctypes, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    else:
        func_text += f"""    out_table = hash_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {and__epa}, {len(zlht__edt)}, {len(nfalk__vbzf)}, vect_same_key.ctypes, key_in_output.ctypes, use_nullable_arr_type.ctypes, {join_node.is_left}, {join_node.is_right}, {join_node.is_join}, {join_node.extra_data_col_num != -1}, {join_node.indicator_col_num != -1}, {join_node.is_na_equal}, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    fuf__bxn = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {fuf__bxn}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        fghj__hgv = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{fghj__hgv}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        kcp__kdtq = {}
        for ispc__nljk, rrxmh__hgrpl in enumerate(join_node.left_keys):
            if ispc__nljk in left_used_key_nums:
                eixb__izqjn = join_node.left_var_map[rrxmh__hgrpl]
                kcp__kdtq[ispc__nljk] = join_node.left_to_output_map[
                    eixb__izqjn]
        yiqp__cdulq = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, kcp__kdtq, False)
        lzni__cahr = {}
        for ispc__nljk, rrxmh__hgrpl in enumerate(join_node.right_keys):
            if ispc__nljk in right_used_key_nums:
                eixb__izqjn = join_node.right_var_map[rrxmh__hgrpl]
                lzni__cahr[ispc__nljk] = join_node.right_to_output_map[
                    eixb__izqjn]
        yiqp__cdulq.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, lzni__cahr, False))
        zwbeq__xsk = False
        qcmbn__dfe = False
        if join_node.has_live_out_table_var:
            gwjq__ejv = list(out_table_type.arr_types)
        else:
            gwjq__ejv = None
        for axpd__nswg, stjrm__cjr in yiqp__cdulq.items():
            if axpd__nswg < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                gwjq__ejv[axpd__nswg] = stjrm__cjr
                zwbeq__xsk = True
            else:
                yxs__gnli = stjrm__cjr
                qcmbn__dfe = True
        if zwbeq__xsk:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            gvlf__mkai = bodo.TableType(tuple(gwjq__ejv))
            glbs['py_table_type'] = gvlf__mkai
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if qcmbn__dfe:
            glbs['index_col_type'] = yxs__gnli
            glbs['index_cast_type'] = index_col_type
            func_text += (
                f'    index_var = bodo.utils.utils.astype(index_var, index_cast_type)\n'
                )
    func_text += f'    out_table = T\n'
    func_text += f'    out_index = index_var\n'
    return func_text


def determine_table_cast_map(matched_key_types: List[types.Type], key_types:
    List[types.Type], used_key_nums: Optional[Set[int]], output_map: Dict[
    int, int], convert_dict_col: bool):
    yiqp__cdulq: Dict[int, types.Type] = {}
    and__epa = len(matched_key_types)
    for ispc__nljk in range(and__epa):
        if used_key_nums is None or ispc__nljk in used_key_nums:
            if matched_key_types[ispc__nljk] != key_types[ispc__nljk] and (
                convert_dict_col or key_types[ispc__nljk] != bodo.
                dict_str_arr_type):
                fghj__hgv = output_map[ispc__nljk]
                yiqp__cdulq[fghj__hgv] = matched_key_types[ispc__nljk]
    return yiqp__cdulq


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    jem__ddlcr = bodo.libs.distributed_api.get_size()
    rdrv__zgi = np.empty(jem__ddlcr, left_key_arrs[0].dtype)
    rlz__cexxr = np.empty(jem__ddlcr, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(rdrv__zgi, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(rlz__cexxr, left_key_arrs[0][-1])
    zjim__xcyx = np.zeros(jem__ddlcr, np.int32)
    zmqy__bcum = np.zeros(jem__ddlcr, np.int32)
    tul__uqin = np.zeros(jem__ddlcr, np.int32)
    ybk__rosh = right_key_arrs[0][0]
    yoha__srsvo = right_key_arrs[0][-1]
    fph__pgcpp = -1
    ispc__nljk = 0
    while ispc__nljk < jem__ddlcr - 1 and rlz__cexxr[ispc__nljk] < ybk__rosh:
        ispc__nljk += 1
    while ispc__nljk < jem__ddlcr and rdrv__zgi[ispc__nljk] <= yoha__srsvo:
        fph__pgcpp, ewe__cym = _count_overlap(right_key_arrs[0], rdrv__zgi[
            ispc__nljk], rlz__cexxr[ispc__nljk])
        if fph__pgcpp != 0:
            fph__pgcpp -= 1
            ewe__cym += 1
        zjim__xcyx[ispc__nljk] = ewe__cym
        zmqy__bcum[ispc__nljk] = fph__pgcpp
        ispc__nljk += 1
    while ispc__nljk < jem__ddlcr:
        zjim__xcyx[ispc__nljk] = 1
        zmqy__bcum[ispc__nljk] = len(right_key_arrs[0]) - 1
        ispc__nljk += 1
    bodo.libs.distributed_api.alltoall(zjim__xcyx, tul__uqin, 1)
    ygghz__omvva = tul__uqin.sum()
    ijac__wsg = np.empty(ygghz__omvva, right_key_arrs[0].dtype)
    bihta__cwu = alloc_arr_tup(ygghz__omvva, right_data)
    mmhxe__ehde = bodo.ir.join.calc_disp(tul__uqin)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], ijac__wsg,
        zjim__xcyx, tul__uqin, zmqy__bcum, mmhxe__ehde)
    bodo.libs.distributed_api.alltoallv_tup(right_data, bihta__cwu,
        zjim__xcyx, tul__uqin, zmqy__bcum, mmhxe__ehde)
    return (ijac__wsg,), bihta__cwu


@numba.njit
def _count_overlap(r_key_arr, start, end):
    ewe__cym = 0
    fph__pgcpp = 0
    tmk__wcfs = 0
    while tmk__wcfs < len(r_key_arr) and r_key_arr[tmk__wcfs] < start:
        fph__pgcpp += 1
        tmk__wcfs += 1
    while tmk__wcfs < len(r_key_arr) and start <= r_key_arr[tmk__wcfs] <= end:
        tmk__wcfs += 1
        ewe__cym += 1
    return fph__pgcpp, ewe__cym


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    efiey__quea = np.empty_like(arr)
    efiey__quea[0] = 0
    for ispc__nljk in range(1, len(arr)):
        efiey__quea[ispc__nljk] = efiey__quea[ispc__nljk - 1] + arr[
            ispc__nljk - 1]
    return efiey__quea


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    agwdc__dduhz = len(left_keys[0])
    sdcsa__ajs = len(right_keys[0])
    qqafx__tglc = alloc_arr_tup(agwdc__dduhz, left_keys)
    cvg__afhsa = alloc_arr_tup(agwdc__dduhz, right_keys)
    sgwth__rgdh = alloc_arr_tup(agwdc__dduhz, data_left)
    oewt__auict = alloc_arr_tup(agwdc__dduhz, data_right)
    auqsa__ioyv = 0
    hnvkt__lphjm = 0
    for auqsa__ioyv in range(agwdc__dduhz):
        if hnvkt__lphjm < 0:
            hnvkt__lphjm = 0
        while hnvkt__lphjm < sdcsa__ajs and getitem_arr_tup(right_keys,
            hnvkt__lphjm) <= getitem_arr_tup(left_keys, auqsa__ioyv):
            hnvkt__lphjm += 1
        hnvkt__lphjm -= 1
        setitem_arr_tup(qqafx__tglc, auqsa__ioyv, getitem_arr_tup(left_keys,
            auqsa__ioyv))
        setitem_arr_tup(sgwth__rgdh, auqsa__ioyv, getitem_arr_tup(data_left,
            auqsa__ioyv))
        if hnvkt__lphjm >= 0:
            setitem_arr_tup(cvg__afhsa, auqsa__ioyv, getitem_arr_tup(
                right_keys, hnvkt__lphjm))
            setitem_arr_tup(oewt__auict, auqsa__ioyv, getitem_arr_tup(
                data_right, hnvkt__lphjm))
        else:
            bodo.libs.array_kernels.setna_tup(cvg__afhsa, auqsa__ioyv)
            bodo.libs.array_kernels.setna_tup(oewt__auict, auqsa__ioyv)
    return qqafx__tglc, cvg__afhsa, sgwth__rgdh, oewt__auict
