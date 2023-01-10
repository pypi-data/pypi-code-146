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
        atg__tlyfi = func.signature
        ajnk__ekztm = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        qxpck__rmhww = cgutils.get_or_insert_function(builder.module,
            ajnk__ekztm, sym._literal_value)
        builder.call(qxpck__rmhww, [context.get_constant_null(atg__tlyfi.
            args[0]), context.get_constant_null(atg__tlyfi.args[1]),
            context.get_constant_null(atg__tlyfi.args[2]), context.
            get_constant_null(atg__tlyfi.args[3]), context.
            get_constant_null(atg__tlyfi.args[4]), context.
            get_constant_null(atg__tlyfi.args[5]), context.get_constant(
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
        ldwg__jko = left_df_type.columns
        pft__tae = right_df_type.columns
        self.left_col_names = ldwg__jko
        self.right_col_names = pft__tae
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(ldwg__jko) if self.is_left_table else 0
        self.n_right_table_cols = len(pft__tae) if self.is_right_table else 0
        ajlxk__tfxy = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        skbg__rsj = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(ajlxk__tfxy)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(skbg__rsj)
        self.left_var_map = {uhcej__ujo: pvrou__huj for pvrou__huj,
            uhcej__ujo in enumerate(ldwg__jko)}
        self.right_var_map = {uhcej__ujo: pvrou__huj for pvrou__huj,
            uhcej__ujo in enumerate(pft__tae)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = ajlxk__tfxy
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = skbg__rsj
        self.left_key_set = set(self.left_var_map[uhcej__ujo] for
            uhcej__ujo in left_keys)
        self.right_key_set = set(self.right_var_map[uhcej__ujo] for
            uhcej__ujo in right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[uhcej__ujo] for
                uhcej__ujo in ldwg__jko if f'(left.{uhcej__ujo})' in
                gen_cond_expr)
            self.right_cond_cols = set(self.right_var_map[uhcej__ujo] for
                uhcej__ujo in pft__tae if f'(right.{uhcej__ujo})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        koa__yuhax: int = -1
        wpe__egxf = set(left_keys) & set(right_keys)
        svdp__txjct = set(ldwg__jko) & set(pft__tae)
        wzf__dyfq = svdp__txjct - wpe__egxf
        ezi__mvkc: Dict[int, (Literal['left', 'right'], int)] = {}
        zida__faol: Dict[int, int] = {}
        pbxu__opfxw: Dict[int, int] = {}
        for pvrou__huj, uhcej__ujo in enumerate(ldwg__jko):
            if uhcej__ujo in wzf__dyfq:
                oictn__rjrz = str(uhcej__ujo) + suffix_left
                enqu__lmj = out_df_type.column_index[oictn__rjrz]
                if (right_index and not left_index and pvrou__huj in self.
                    left_key_set):
                    koa__yuhax = out_df_type.column_index[uhcej__ujo]
                    ezi__mvkc[koa__yuhax] = 'left', pvrou__huj
            else:
                enqu__lmj = out_df_type.column_index[uhcej__ujo]
            ezi__mvkc[enqu__lmj] = 'left', pvrou__huj
            zida__faol[pvrou__huj] = enqu__lmj
        for pvrou__huj, uhcej__ujo in enumerate(pft__tae):
            if uhcej__ujo not in wpe__egxf:
                if uhcej__ujo in wzf__dyfq:
                    vyrhi__vhioy = str(uhcej__ujo) + suffix_right
                    enqu__lmj = out_df_type.column_index[vyrhi__vhioy]
                    if (left_index and not right_index and pvrou__huj in
                        self.right_key_set):
                        koa__yuhax = out_df_type.column_index[uhcej__ujo]
                        ezi__mvkc[koa__yuhax] = 'right', pvrou__huj
                else:
                    enqu__lmj = out_df_type.column_index[uhcej__ujo]
                ezi__mvkc[enqu__lmj] = 'right', pvrou__huj
                pbxu__opfxw[pvrou__huj] = enqu__lmj
        if self.left_vars[-1] is not None:
            zida__faol[ajlxk__tfxy] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            pbxu__opfxw[skbg__rsj] = self.n_out_table_cols
        self.out_to_input_col_map = ezi__mvkc
        self.left_to_output_map = zida__faol
        self.right_to_output_map = pbxu__opfxw
        self.extra_data_col_num = koa__yuhax
        if self.out_data_vars[1] is not None:
            oqmxt__ldfq = 'left' if right_index else 'right'
            if oqmxt__ldfq == 'left':
                onv__orlvr = ajlxk__tfxy
            elif oqmxt__ldfq == 'right':
                onv__orlvr = skbg__rsj
        else:
            oqmxt__ldfq = None
            onv__orlvr = -1
        self.index_source = oqmxt__ldfq
        self.index_col_num = onv__orlvr
        iow__pur = []
        kyol__gzyhl = len(left_keys)
        for ntts__tylvb in range(kyol__gzyhl):
            dsan__czcc = left_keys[ntts__tylvb]
            cwo__doze = right_keys[ntts__tylvb]
            iow__pur.append(dsan__czcc == cwo__doze)
        self.vect_same_key = iow__pur

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
        for xfd__pdwku in self.left_vars:
            if xfd__pdwku is not None:
                vars.append(xfd__pdwku)
        return vars

    def get_live_right_vars(self):
        vars = []
        for xfd__pdwku in self.right_vars:
            if xfd__pdwku is not None:
                vars.append(xfd__pdwku)
        return vars

    def get_live_out_vars(self):
        vars = []
        for xfd__pdwku in self.out_data_vars:
            if xfd__pdwku is not None:
                vars.append(xfd__pdwku)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        gbygc__sbzd = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[gbygc__sbzd])
                gbygc__sbzd += 1
            else:
                left_vars.append(None)
            start = 1
        elpbh__ego = max(self.n_left_table_cols - 1, 0)
        for pvrou__huj in range(start, len(self.left_vars)):
            if pvrou__huj + elpbh__ego in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[gbygc__sbzd])
                gbygc__sbzd += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        gbygc__sbzd = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[gbygc__sbzd])
                gbygc__sbzd += 1
            else:
                right_vars.append(None)
            start = 1
        elpbh__ego = max(self.n_right_table_cols - 1, 0)
        for pvrou__huj in range(start, len(self.right_vars)):
            if pvrou__huj + elpbh__ego in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[gbygc__sbzd])
                gbygc__sbzd += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        hawmv__uro = [self.has_live_out_table_var, self.has_live_out_index_var]
        gbygc__sbzd = 0
        for pvrou__huj in range(len(self.out_data_vars)):
            if not hawmv__uro[pvrou__huj]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[gbygc__sbzd])
                gbygc__sbzd += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {pvrou__huj for pvrou__huj in self.out_used_cols if 
            pvrou__huj < self.n_out_table_cols}

    def __repr__(self):
        uhau__smp = ', '.join([f'{uhcej__ujo}' for uhcej__ujo in self.
            left_col_names])
        wgacn__mty = f'left={{{uhau__smp}}}'
        uhau__smp = ', '.join([f'{uhcej__ujo}' for uhcej__ujo in self.
            right_col_names])
        hpx__gfx = f'right={{{uhau__smp}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, wgacn__mty, hpx__gfx)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    wpdx__pic = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    lzga__gbjjz = []
    mzo__lrrf = join_node.get_live_left_vars()
    for portp__hyz in mzo__lrrf:
        opzku__qdswm = typemap[portp__hyz.name]
        abz__jdclp = equiv_set.get_shape(portp__hyz)
        if abz__jdclp:
            lzga__gbjjz.append(abz__jdclp[0])
    if len(lzga__gbjjz) > 1:
        equiv_set.insert_equiv(*lzga__gbjjz)
    lzga__gbjjz = []
    mzo__lrrf = list(join_node.get_live_right_vars())
    for portp__hyz in mzo__lrrf:
        opzku__qdswm = typemap[portp__hyz.name]
        abz__jdclp = equiv_set.get_shape(portp__hyz)
        if abz__jdclp:
            lzga__gbjjz.append(abz__jdclp[0])
    if len(lzga__gbjjz) > 1:
        equiv_set.insert_equiv(*lzga__gbjjz)
    lzga__gbjjz = []
    for ljf__fwy in join_node.get_live_out_vars():
        opzku__qdswm = typemap[ljf__fwy.name]
        cul__ycczb = array_analysis._gen_shape_call(equiv_set, ljf__fwy,
            opzku__qdswm.ndim, None, wpdx__pic)
        equiv_set.insert_equiv(ljf__fwy, cul__ycczb)
        lzga__gbjjz.append(cul__ycczb[0])
        equiv_set.define(ljf__fwy, set())
    if len(lzga__gbjjz) > 1:
        equiv_set.insert_equiv(*lzga__gbjjz)
    return [], wpdx__pic


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    tlnwp__plr = Distribution.OneD
    ykdu__qnzxb = Distribution.OneD
    for portp__hyz in join_node.get_live_left_vars():
        tlnwp__plr = Distribution(min(tlnwp__plr.value, array_dists[
            portp__hyz.name].value))
    for portp__hyz in join_node.get_live_right_vars():
        ykdu__qnzxb = Distribution(min(ykdu__qnzxb.value, array_dists[
            portp__hyz.name].value))
    ljz__mgz = Distribution.OneD_Var
    for ljf__fwy in join_node.get_live_out_vars():
        if ljf__fwy.name in array_dists:
            ljz__mgz = Distribution(min(ljz__mgz.value, array_dists[
                ljf__fwy.name].value))
    pcd__qfjod = Distribution(min(ljz__mgz.value, tlnwp__plr.value))
    sicg__azux = Distribution(min(ljz__mgz.value, ykdu__qnzxb.value))
    ljz__mgz = Distribution(max(pcd__qfjod.value, sicg__azux.value))
    for ljf__fwy in join_node.get_live_out_vars():
        array_dists[ljf__fwy.name] = ljz__mgz
    if ljz__mgz != Distribution.OneD_Var:
        tlnwp__plr = ljz__mgz
        ykdu__qnzxb = ljz__mgz
    for portp__hyz in join_node.get_live_left_vars():
        array_dists[portp__hyz.name] = tlnwp__plr
    for portp__hyz in join_node.get_live_right_vars():
        array_dists[portp__hyz.name] = ykdu__qnzxb
    join_node.left_dist = tlnwp__plr
    join_node.right_dist = ykdu__qnzxb


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(xfd__pdwku, callback,
        cbdata) for xfd__pdwku in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(xfd__pdwku, callback,
        cbdata) for xfd__pdwku in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(xfd__pdwku, callback,
        cbdata) for xfd__pdwku in join_node.get_live_out_vars()])
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
        qqie__aip = []
        vmlg__aimdc = join_node.get_out_table_var()
        if vmlg__aimdc.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for jus__xtm in join_node.out_to_input_col_map.keys():
            if jus__xtm in join_node.out_used_cols:
                continue
            qqie__aip.append(jus__xtm)
            if join_node.indicator_col_num == jus__xtm:
                join_node.indicator_col_num = -1
                continue
            if jus__xtm == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            oyqkc__wgb, jus__xtm = join_node.out_to_input_col_map[jus__xtm]
            if oyqkc__wgb == 'left':
                if (jus__xtm not in join_node.left_key_set and jus__xtm not in
                    join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(jus__xtm)
                    if not join_node.is_left_table:
                        join_node.left_vars[jus__xtm] = None
            elif oyqkc__wgb == 'right':
                if (jus__xtm not in join_node.right_key_set and jus__xtm not in
                    join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(jus__xtm)
                    if not join_node.is_right_table:
                        join_node.right_vars[jus__xtm] = None
        for pvrou__huj in qqie__aip:
            del join_node.out_to_input_col_map[pvrou__huj]
        if join_node.is_left_table:
            gem__crqc = set(range(join_node.n_left_table_cols))
            bagew__wvsx = not bool(gem__crqc - join_node.left_dead_var_inds)
            if bagew__wvsx:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            gem__crqc = set(range(join_node.n_right_table_cols))
            bagew__wvsx = not bool(gem__crqc - join_node.right_dead_var_inds)
            if bagew__wvsx:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        cewlv__xwhwd = join_node.get_out_index_var()
        if cewlv__xwhwd.name not in lives:
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
    cxkub__xdz = False
    if join_node.has_live_out_table_var:
        duqu__wgb = join_node.get_out_table_var().name
        gse__nqmd, vbt__bkz, nrfdd__nrvff = get_live_column_nums_block(
            column_live_map, equiv_vars, duqu__wgb)
        if not (vbt__bkz or nrfdd__nrvff):
            gse__nqmd = trim_extra_used_columns(gse__nqmd, join_node.
                n_out_table_cols)
            rguf__ftjpf = join_node.get_out_table_used_cols()
            if len(gse__nqmd) != len(rguf__ftjpf):
                cxkub__xdz = not (join_node.is_left_table and join_node.
                    is_right_table)
                kxcl__fhebp = rguf__ftjpf - gse__nqmd
                join_node.out_used_cols = join_node.out_used_cols - kxcl__fhebp
    return cxkub__xdz


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        ocgp__jgwql = join_node.get_out_table_var()
        slyla__zdqyv, vbt__bkz, nrfdd__nrvff = _compute_table_column_uses(
            ocgp__jgwql.name, table_col_use_map, equiv_vars)
    else:
        slyla__zdqyv, vbt__bkz, nrfdd__nrvff = set(), False, False
    if join_node.has_live_left_table_var:
        lzye__xciwq = join_node.left_vars[0].name
        bwc__fvl, pbmeq__xgeik, emu__rhpzp = block_use_map[lzye__xciwq]
        if not (pbmeq__xgeik or emu__rhpzp):
            lte__fvmcw = set([join_node.out_to_input_col_map[pvrou__huj][1] for
                pvrou__huj in slyla__zdqyv if join_node.
                out_to_input_col_map[pvrou__huj][0] == 'left'])
            zwrjf__txkc = set(pvrou__huj for pvrou__huj in join_node.
                left_key_set | join_node.left_cond_cols if pvrou__huj <
                join_node.n_left_table_cols)
            if not (vbt__bkz or nrfdd__nrvff):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (lte__fvmcw | zwrjf__txkc)
            block_use_map[lzye__xciwq] = (bwc__fvl | lte__fvmcw |
                zwrjf__txkc, vbt__bkz or nrfdd__nrvff, False)
    if join_node.has_live_right_table_var:
        xbb__kisbx = join_node.right_vars[0].name
        bwc__fvl, pbmeq__xgeik, emu__rhpzp = block_use_map[xbb__kisbx]
        if not (pbmeq__xgeik or emu__rhpzp):
            dmfis__cxem = set([join_node.out_to_input_col_map[pvrou__huj][1
                ] for pvrou__huj in slyla__zdqyv if join_node.
                out_to_input_col_map[pvrou__huj][0] == 'right'])
            pyz__yzj = set(pvrou__huj for pvrou__huj in join_node.
                right_key_set | join_node.right_cond_cols if pvrou__huj <
                join_node.n_right_table_cols)
            if not (vbt__bkz or nrfdd__nrvff):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (dmfis__cxem | pyz__yzj)
            block_use_map[xbb__kisbx] = (bwc__fvl | dmfis__cxem | pyz__yzj,
                vbt__bkz or nrfdd__nrvff, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({kag__gln.name for kag__gln in join_node.
        get_live_left_vars()})
    use_set.update({kag__gln.name for kag__gln in join_node.
        get_live_right_vars()})
    def_set.update({kag__gln.name for kag__gln in join_node.
        get_live_out_vars()})
    if join_node.how == 'cross':
        use_set.add(join_node.left_len_var.name)
        use_set.add(join_node.right_len_var.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    wnkv__rhsph = set(kag__gln.name for kag__gln in join_node.
        get_live_out_vars())
    return set(), wnkv__rhsph


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(xfd__pdwku, var_dict) for
        xfd__pdwku in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(xfd__pdwku, var_dict) for
        xfd__pdwku in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(xfd__pdwku,
        var_dict) for xfd__pdwku in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = replace_vars_inner(join_node.left_len_var,
            var_dict)
        join_node.right_len_var = replace_vars_inner(join_node.
            right_len_var, var_dict)


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for portp__hyz in join_node.get_live_out_vars():
        definitions[portp__hyz.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def _gen_cross_join_len(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel):
    func_text = 'def f(left_len, right_len):\n'
    laj__mztf = 'bodo.libs.distributed_api.get_size()'
    mnpe__nejmq = 'bodo.libs.distributed_api.get_rank()'
    if left_parallel:
        func_text += f"""  left_len = bodo.libs.distributed_api.get_node_portion(left_len, {laj__mztf}, {mnpe__nejmq})
"""
    if right_parallel and not left_parallel:
        func_text += f"""  right_len = bodo.libs.distributed_api.get_node_portion(right_len, {laj__mztf}, {mnpe__nejmq})
"""
    func_text += '  n_rows = left_len * right_len\n'
    func_text += '  py_table = init_table(py_table_type, False)\n'
    func_text += '  py_table = set_table_len(py_table, n_rows)\n'
    xleb__abu = {}
    exec(func_text, {}, xleb__abu)
    bsey__ieja = xleb__abu['f']
    glbs = {'py_table_type': out_table_type, 'init_table': bodo.hiframes.
        table.init_table, 'set_table_len': bodo.hiframes.table.
        set_table_len, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value), 'bodo': bodo}
    lqvr__eqh = [join_node.left_len_var, join_node.right_len_var]
    vjkw__risko = tuple(typemap[kag__gln.name] for kag__gln in lqvr__eqh)
    uoecq__kai = compile_to_numba_ir(bsey__ieja, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=vjkw__risko, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(uoecq__kai, lqvr__eqh)
    tta__hskvp = uoecq__kai.body[:-3]
    tta__hskvp[-1].target = join_node.out_data_vars[0]
    return tta__hskvp


def _gen_cross_join_repeat(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel, left_is_dead):
    mzo__lrrf = join_node.right_vars if left_is_dead else join_node.left_vars
    gjzu__rdlt = ', '.join(f't{pvrou__huj}' for pvrou__huj in range(len(
        mzo__lrrf)) if mzo__lrrf[pvrou__huj] is not None)
    ubrs__tvxlt = len(join_node.right_col_names) if left_is_dead else len(
        join_node.left_col_names)
    dqju__ifs = (join_node.is_right_table if left_is_dead else join_node.
        is_left_table)
    mpxm__fgpi = (join_node.right_dead_var_inds if left_is_dead else
        join_node.left_dead_var_inds)
    pzbb__uvi = [(f'get_table_data(t0, {pvrou__huj})' if dqju__ifs else
        f't{pvrou__huj}') for pvrou__huj in range(ubrs__tvxlt)]
    ypx__rzegr = ', '.join(
        f'bodo.libs.array_kernels.repeat_kernel({pzbb__uvi[pvrou__huj]}, repeats)'
         if pvrou__huj not in mpxm__fgpi else 'None' for pvrou__huj in
        range(ubrs__tvxlt))
    lppzb__vikk = len(out_table_type.arr_types)
    vaus__istmc = [join_node.out_to_input_col_map.get(pvrou__huj, (-1, -1))
        [1] for pvrou__huj in range(lppzb__vikk)]
    laj__mztf = 'bodo.libs.distributed_api.get_size()'
    mnpe__nejmq = 'bodo.libs.distributed_api.get_rank()'
    zcy__tadne = 'left_len' if left_is_dead else 'right_len'
    nplwy__wmwa = right_parallel if left_is_dead else left_parallel
    fgrpi__htx = left_parallel if left_is_dead else right_parallel
    tzp__kpr = not nplwy__wmwa and fgrpi__htx
    whc__jgowe = (
        f'bodo.libs.distributed_api.get_node_portion({zcy__tadne}, {laj__mztf}, {mnpe__nejmq})'
         if tzp__kpr else zcy__tadne)
    func_text = f'def f({gjzu__rdlt}, left_len, right_len):\n'
    func_text += f'  repeats = {whc__jgowe}\n'
    func_text += f'  out_data = ({ypx__rzegr},)\n'
    func_text += f"""  py_table = logical_table_to_table(out_data, (), col_inds, {ubrs__tvxlt}, out_table_type, used_cols)
"""
    xleb__abu = {}
    exec(func_text, {}, xleb__abu)
    bsey__ieja = xleb__abu['f']
    glbs = {'out_table_type': out_table_type, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value), 'bodo': bodo, 'used_cols':
        bodo.utils.typing.MetaType(tuple(join_node.out_used_cols)),
        'col_inds': bodo.utils.typing.MetaType(tuple(vaus__istmc)),
        'logical_table_to_table': bodo.hiframes.table.
        logical_table_to_table, 'get_table_data': bodo.hiframes.table.
        get_table_data}
    lqvr__eqh = [kag__gln for kag__gln in mzo__lrrf if kag__gln is not None
        ] + [join_node.left_len_var, join_node.right_len_var]
    vjkw__risko = tuple(typemap[kag__gln.name] for kag__gln in lqvr__eqh)
    uoecq__kai = compile_to_numba_ir(bsey__ieja, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=vjkw__risko, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(uoecq__kai, lqvr__eqh)
    tta__hskvp = uoecq__kai.body[:-3]
    tta__hskvp[-1].target = join_node.out_data_vars[0]
    return tta__hskvp


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        pbbh__qil = join_node.loc.strformat()
        ape__hfkop = [join_node.left_col_names[pvrou__huj] for pvrou__huj in
            sorted(set(range(len(join_node.left_col_names))) - join_node.
            left_dead_var_inds)]
        zfnr__rszf = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', zfnr__rszf,
            pbbh__qil, ape__hfkop)
        egkti__xftah = [join_node.right_col_names[pvrou__huj] for
            pvrou__huj in sorted(set(range(len(join_node.right_col_names))) -
            join_node.right_dead_var_inds)]
        zfnr__rszf = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', zfnr__rszf,
            pbbh__qil, egkti__xftah)
        upjaw__doyo = [join_node.out_col_names[pvrou__huj] for pvrou__huj in
            sorted(join_node.get_out_table_used_cols())]
        zfnr__rszf = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', zfnr__rszf,
            pbbh__qil, upjaw__doyo)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    kyol__gzyhl = len(join_node.left_keys)
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
    elif join_node.how == 'cross' and all(pvrou__huj in join_node.
        left_dead_var_inds for pvrou__huj in range(len(join_node.
        left_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            True)
    elif join_node.how == 'cross' and all(pvrou__huj in join_node.
        right_dead_var_inds for pvrou__huj in range(len(join_node.
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
    edcm__zba = set()
    wkl__lwlvn = set()
    left_logical_physical_map = {}
    right_logical_physical_map = {}
    left_physical_to_logical_list = []
    right_physical_to_logical_list = []
    lpi__uqoe = 0
    getf__bmjzp = 0
    ufms__khs = []
    for jmfbn__zmvz, uhcej__ujo in enumerate(join_node.left_keys):
        oyyd__vyvw = join_node.left_var_map[uhcej__ujo]
        if not join_node.is_left_table:
            ufms__khs.append(join_node.left_vars[oyyd__vyvw])
        hawmv__uro = 1
        enqu__lmj = join_node.left_to_output_map[oyyd__vyvw]
        if uhcej__ujo == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == oyyd__vyvw):
                out_physical_to_logical_list.append(enqu__lmj)
                left_used_key_nums.add(jmfbn__zmvz)
                edcm__zba.add(oyyd__vyvw)
            else:
                hawmv__uro = 0
        elif enqu__lmj not in join_node.out_used_cols:
            hawmv__uro = 0
        elif oyyd__vyvw in edcm__zba:
            hawmv__uro = 0
        else:
            left_used_key_nums.add(jmfbn__zmvz)
            edcm__zba.add(oyyd__vyvw)
            out_physical_to_logical_list.append(enqu__lmj)
        left_physical_to_logical_list.append(oyyd__vyvw)
        left_logical_physical_map[oyyd__vyvw] = lpi__uqoe
        lpi__uqoe += 1
        left_key_in_output.append(hawmv__uro)
    ufms__khs = tuple(ufms__khs)
    glkj__axoxn = []
    for pvrou__huj in range(len(join_node.left_col_names)):
        if (pvrou__huj not in join_node.left_dead_var_inds and pvrou__huj
             not in join_node.left_key_set):
            if not join_node.is_left_table:
                kag__gln = join_node.left_vars[pvrou__huj]
                glkj__axoxn.append(kag__gln)
            dam__wlrkr = 1
            hcgt__emkut = 1
            enqu__lmj = join_node.left_to_output_map[pvrou__huj]
            if pvrou__huj in join_node.left_cond_cols:
                if enqu__lmj not in join_node.out_used_cols:
                    dam__wlrkr = 0
                left_key_in_output.append(dam__wlrkr)
            elif pvrou__huj in join_node.left_dead_var_inds:
                dam__wlrkr = 0
                hcgt__emkut = 0
            if dam__wlrkr:
                out_physical_to_logical_list.append(enqu__lmj)
            if hcgt__emkut:
                left_physical_to_logical_list.append(pvrou__huj)
                left_logical_physical_map[pvrou__huj] = lpi__uqoe
                lpi__uqoe += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            glkj__axoxn.append(join_node.left_vars[join_node.index_col_num])
        enqu__lmj = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(enqu__lmj)
        left_physical_to_logical_list.append(join_node.index_col_num)
    glkj__axoxn = tuple(glkj__axoxn)
    if join_node.is_left_table:
        glkj__axoxn = tuple(join_node.get_live_left_vars())
    njx__iya = []
    for jmfbn__zmvz, uhcej__ujo in enumerate(join_node.right_keys):
        oyyd__vyvw = join_node.right_var_map[uhcej__ujo]
        if not join_node.is_right_table:
            njx__iya.append(join_node.right_vars[oyyd__vyvw])
        if not join_node.vect_same_key[jmfbn__zmvz] and not join_node.is_join:
            hawmv__uro = 1
            if oyyd__vyvw not in join_node.right_to_output_map:
                hawmv__uro = 0
            else:
                enqu__lmj = join_node.right_to_output_map[oyyd__vyvw]
                if uhcej__ujo == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        oyyd__vyvw):
                        out_physical_to_logical_list.append(enqu__lmj)
                        right_used_key_nums.add(jmfbn__zmvz)
                        wkl__lwlvn.add(oyyd__vyvw)
                    else:
                        hawmv__uro = 0
                elif enqu__lmj not in join_node.out_used_cols:
                    hawmv__uro = 0
                elif oyyd__vyvw in wkl__lwlvn:
                    hawmv__uro = 0
                else:
                    right_used_key_nums.add(jmfbn__zmvz)
                    wkl__lwlvn.add(oyyd__vyvw)
                    out_physical_to_logical_list.append(enqu__lmj)
            right_key_in_output.append(hawmv__uro)
        right_physical_to_logical_list.append(oyyd__vyvw)
        right_logical_physical_map[oyyd__vyvw] = getf__bmjzp
        getf__bmjzp += 1
    njx__iya = tuple(njx__iya)
    zhcb__sgccr = []
    for pvrou__huj in range(len(join_node.right_col_names)):
        if (pvrou__huj not in join_node.right_dead_var_inds and pvrou__huj
             not in join_node.right_key_set):
            if not join_node.is_right_table:
                zhcb__sgccr.append(join_node.right_vars[pvrou__huj])
            dam__wlrkr = 1
            hcgt__emkut = 1
            enqu__lmj = join_node.right_to_output_map[pvrou__huj]
            if pvrou__huj in join_node.right_cond_cols:
                if enqu__lmj not in join_node.out_used_cols:
                    dam__wlrkr = 0
                right_key_in_output.append(dam__wlrkr)
            elif pvrou__huj in join_node.right_dead_var_inds:
                dam__wlrkr = 0
                hcgt__emkut = 0
            if dam__wlrkr:
                out_physical_to_logical_list.append(enqu__lmj)
            if hcgt__emkut:
                right_physical_to_logical_list.append(pvrou__huj)
                right_logical_physical_map[pvrou__huj] = getf__bmjzp
                getf__bmjzp += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            zhcb__sgccr.append(join_node.right_vars[join_node.index_col_num])
        enqu__lmj = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(enqu__lmj)
        right_physical_to_logical_list.append(join_node.index_col_num)
    zhcb__sgccr = tuple(zhcb__sgccr)
    if join_node.is_right_table:
        zhcb__sgccr = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    lqvr__eqh = ufms__khs + njx__iya + glkj__axoxn + zhcb__sgccr
    vjkw__risko = tuple(typemap[kag__gln.name] for kag__gln in lqvr__eqh)
    left_other_names = tuple('t1_c' + str(pvrou__huj) for pvrou__huj in
        range(len(glkj__axoxn)))
    right_other_names = tuple('t2_c' + str(pvrou__huj) for pvrou__huj in
        range(len(zhcb__sgccr)))
    if join_node.is_left_table:
        uvwh__vfbg = ()
    else:
        uvwh__vfbg = tuple('t1_key' + str(pvrou__huj) for pvrou__huj in
            range(kyol__gzyhl))
    if join_node.is_right_table:
        dmeo__dkanv = ()
    else:
        dmeo__dkanv = tuple('t2_key' + str(pvrou__huj) for pvrou__huj in
            range(kyol__gzyhl))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(uvwh__vfbg + dmeo__dkanv +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            eaqn__rld = typemap[join_node.left_vars[0].name]
        else:
            eaqn__rld = types.none
        for nbbc__lbeur in left_physical_to_logical_list:
            if nbbc__lbeur < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                opzku__qdswm = eaqn__rld.arr_types[nbbc__lbeur]
            else:
                opzku__qdswm = typemap[join_node.left_vars[-1].name]
            if nbbc__lbeur in join_node.left_key_set:
                left_key_types.append(opzku__qdswm)
            else:
                left_other_types.append(opzku__qdswm)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[kag__gln.name] for kag__gln in ufms__khs
            )
        left_other_types = tuple([typemap[uhcej__ujo.name] for uhcej__ujo in
            glkj__axoxn])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            eaqn__rld = typemap[join_node.right_vars[0].name]
        else:
            eaqn__rld = types.none
        for nbbc__lbeur in right_physical_to_logical_list:
            if nbbc__lbeur < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                opzku__qdswm = eaqn__rld.arr_types[nbbc__lbeur]
            else:
                opzku__qdswm = typemap[join_node.right_vars[-1].name]
            if nbbc__lbeur in join_node.right_key_set:
                right_key_types.append(opzku__qdswm)
            else:
                right_other_types.append(opzku__qdswm)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[kag__gln.name] for kag__gln in njx__iya
            )
        right_other_types = tuple([typemap[uhcej__ujo.name] for uhcej__ujo in
            zhcb__sgccr])
    matched_key_types = []
    for pvrou__huj in range(kyol__gzyhl):
        reg__okz = _match_join_key_types(left_key_types[pvrou__huj],
            right_key_types[pvrou__huj], loc)
        glbs[f'key_type_{pvrou__huj}'] = reg__okz
        matched_key_types.append(reg__okz)
    if join_node.is_left_table:
        buen__tuu = determine_table_cast_map(matched_key_types,
            left_key_types, None, {pvrou__huj: join_node.left_var_map[
            mjma__pypy] for pvrou__huj, mjma__pypy in enumerate(join_node.
            left_keys)}, True)
        if buen__tuu:
            ffqwv__ngl = False
            ihahd__qylp = False
            zpfs__nvin = None
            if join_node.has_live_left_table_var:
                gxos__zsskl = list(typemap[join_node.left_vars[0].name].
                    arr_types)
            else:
                gxos__zsskl = None
            for jus__xtm, opzku__qdswm in buen__tuu.items():
                if jus__xtm < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    gxos__zsskl[jus__xtm] = opzku__qdswm
                    ffqwv__ngl = True
                else:
                    zpfs__nvin = opzku__qdswm
                    ihahd__qylp = True
            if ffqwv__ngl:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(gxos__zsskl))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if ihahd__qylp:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = zpfs__nvin
    else:
        func_text += '    t1_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({uvwh__vfbg[pvrou__huj]}, key_type_{pvrou__huj})'
             if left_key_types[pvrou__huj] != matched_key_types[pvrou__huj]
             else f'{uvwh__vfbg[pvrou__huj]}' for pvrou__huj in range(
            kyol__gzyhl)), ',' if kyol__gzyhl != 0 else '')
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        buen__tuu = determine_table_cast_map(matched_key_types,
            right_key_types, None, {pvrou__huj: join_node.right_var_map[
            mjma__pypy] for pvrou__huj, mjma__pypy in enumerate(join_node.
            right_keys)}, True)
        if buen__tuu:
            ffqwv__ngl = False
            ihahd__qylp = False
            zpfs__nvin = None
            if join_node.has_live_right_table_var:
                gxos__zsskl = list(typemap[join_node.right_vars[0].name].
                    arr_types)
            else:
                gxos__zsskl = None
            for jus__xtm, opzku__qdswm in buen__tuu.items():
                if jus__xtm < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    gxos__zsskl[jus__xtm] = opzku__qdswm
                    ffqwv__ngl = True
                else:
                    zpfs__nvin = opzku__qdswm
                    ihahd__qylp = True
            if ffqwv__ngl:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(gxos__zsskl))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if ihahd__qylp:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = zpfs__nvin
    else:
        func_text += '    t2_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({dmeo__dkanv[pvrou__huj]}, key_type_{pvrou__huj})'
             if right_key_types[pvrou__huj] != matched_key_types[pvrou__huj
            ] else f'{dmeo__dkanv[pvrou__huj]}' for pvrou__huj in range(
            kyol__gzyhl)), ',' if kyol__gzyhl != 0 else '')
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
        for pvrou__huj in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(pvrou__huj,
                pvrou__huj)
        for pvrou__huj in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                pvrou__huj, pvrou__huj)
        for pvrou__huj in range(kyol__gzyhl):
            func_text += (
                f'    t1_keys_{pvrou__huj} = out_t1_keys[{pvrou__huj}]\n')
        for pvrou__huj in range(kyol__gzyhl):
            func_text += (
                f'    t2_keys_{pvrou__huj} = out_t2_keys[{pvrou__huj}]\n')
    xleb__abu = {}
    exec(func_text, {}, xleb__abu)
    bsey__ieja = xleb__abu['f']
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
    uoecq__kai = compile_to_numba_ir(bsey__ieja, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=vjkw__risko, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(uoecq__kai, lqvr__eqh)
    tta__hskvp = uoecq__kai.body[:-3]
    if join_node.has_live_out_index_var:
        tta__hskvp[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        tta__hskvp[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        tta__hskvp.pop(-1)
    elif not join_node.has_live_out_table_var:
        tta__hskvp.pop(-2)
    return tta__hskvp


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    gtp__fwie = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{gtp__fwie}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
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
    xleb__abu = {}
    exec(func_text, table_getitem_funcs, xleb__abu)
    xtm__npyil = xleb__abu[f'bodo_join_gen_cond{gtp__fwie}']
    qalyl__eic = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    lbofc__xihh = numba.cfunc(qalyl__eic, nopython=True)(xtm__npyil)
    join_gen_cond_cfunc[lbofc__xihh.native_name] = lbofc__xihh
    join_gen_cond_cfunc_addr[lbofc__xihh.native_name] = lbofc__xihh.address
    return lbofc__xihh, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    rhn__eru = []
    for uhcej__ujo, cbbqp__oyd in name_to_var_map.items():
        ruzlf__eboy = f'({table_name}.{uhcej__ujo})'
        if ruzlf__eboy not in expr:
            continue
        dyxte__wpbfh = f'getitem_{table_name}_val_{cbbqp__oyd}'
        if is_table_var:
            emiz__fdtq = typemap[col_vars[0].name].arr_types[cbbqp__oyd]
        else:
            emiz__fdtq = typemap[col_vars[cbbqp__oyd].name]
        if is_str_arr_type(emiz__fdtq) or emiz__fdtq == bodo.binary_array_type:
            hdttn__tcdfq = (
                f'{dyxte__wpbfh}({table_name}_table, {table_name}_ind)\n')
        else:
            hdttn__tcdfq = (
                f'{dyxte__wpbfh}({table_name}_data1, {table_name}_ind)\n')
        dflsk__kum = logical_to_physical_ind[cbbqp__oyd]
        table_getitem_funcs[dyxte__wpbfh
            ] = bodo.libs.array._gen_row_access_intrinsic(emiz__fdtq,
            dflsk__kum)
        expr = expr.replace(ruzlf__eboy, hdttn__tcdfq)
        bvc__steix = f'({na_check_name}.{table_name}.{uhcej__ujo})'
        if bvc__steix in expr:
            vef__avdv = f'nacheck_{table_name}_val_{cbbqp__oyd}'
            bwmvq__umtvu = f'_bodo_isna_{table_name}_val_{cbbqp__oyd}'
            if isinstance(emiz__fdtq, (bodo.libs.int_arr_ext.
                IntegerArrayType, bodo.FloatingArrayType, bodo.TimeArrayType)
                ) or emiz__fdtq in (bodo.libs.bool_arr_ext.boolean_array,
                bodo.binary_array_type, bodo.datetime_date_array_type
                ) or is_str_arr_type(emiz__fdtq):
                func_text += f"""  {bwmvq__umtvu} = {vef__avdv}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {bwmvq__umtvu} = {vef__avdv}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[vef__avdv
                ] = bodo.libs.array._gen_row_na_check_intrinsic(emiz__fdtq,
                dflsk__kum)
            expr = expr.replace(bvc__steix, bwmvq__umtvu)
        if cbbqp__oyd not in key_set:
            rhn__eru.append(dflsk__kum)
    return expr, func_text, rhn__eru


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as fpbhr__amo:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    sip__mtx = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[kag__gln.name] in sip__mtx for kag__gln in
        join_node.get_live_left_vars())
    if not join_node.get_live_left_vars():
        assert join_node.how == 'cross', 'cross join expected if left data is dead'
        left_parallel = join_node.left_dist in sip__mtx
    right_parallel = all(array_dists[kag__gln.name] in sip__mtx for
        kag__gln in join_node.get_live_right_vars())
    if not join_node.get_live_right_vars():
        assert join_node.how == 'cross', 'cross join expected if right data is dead'
        right_parallel = join_node.right_dist in sip__mtx
    if not left_parallel:
        assert not any(array_dists[kag__gln.name] in sip__mtx for kag__gln in
            join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[kag__gln.name] in sip__mtx for kag__gln in
            join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[kag__gln.name] in sip__mtx for kag__gln in
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
    oarl__jzs = set(left_col_nums)
    jrrg__admb = set(right_col_nums)
    iow__pur = join_node.vect_same_key
    xrtrp__qzeii = []
    for pvrou__huj in range(len(left_key_types)):
        if left_key_in_output[pvrou__huj]:
            xrtrp__qzeii.append(needs_typechange(matched_key_types[
                pvrou__huj], join_node.is_right, iow__pur[pvrou__huj]))
    dlqdy__lptpl = len(left_key_types)
    coow__mgvb = 0
    spfur__rgjzj = left_physical_to_logical_list[len(left_key_types):]
    for pvrou__huj, nbbc__lbeur in enumerate(spfur__rgjzj):
        vmvfd__bisg = True
        if nbbc__lbeur in oarl__jzs:
            vmvfd__bisg = left_key_in_output[dlqdy__lptpl]
            dlqdy__lptpl += 1
        if vmvfd__bisg:
            xrtrp__qzeii.append(needs_typechange(left_other_types[
                pvrou__huj], join_node.is_right, False))
    for pvrou__huj in range(len(right_key_types)):
        if not iow__pur[pvrou__huj] and not join_node.is_join:
            if right_key_in_output[coow__mgvb]:
                xrtrp__qzeii.append(needs_typechange(matched_key_types[
                    pvrou__huj], join_node.is_left, False))
            coow__mgvb += 1
    pafb__klvm = right_physical_to_logical_list[len(right_key_types):]
    for pvrou__huj, nbbc__lbeur in enumerate(pafb__klvm):
        vmvfd__bisg = True
        if nbbc__lbeur in jrrg__admb:
            vmvfd__bisg = right_key_in_output[coow__mgvb]
            coow__mgvb += 1
        if vmvfd__bisg:
            xrtrp__qzeii.append(needs_typechange(right_other_types[
                pvrou__huj], join_node.is_left, False))
    kyol__gzyhl = len(left_key_types)
    func_text = '    # beginning of _gen_join_cpp_call\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            guzs__avdxt = left_other_names[1:]
            vmlg__aimdc = left_other_names[0]
        else:
            guzs__avdxt = left_other_names
            vmlg__aimdc = None
        kvlc__rimpr = '()' if len(guzs__avdxt) == 0 else f'({guzs__avdxt[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({vmlg__aimdc}, {kvlc__rimpr}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        jmdl__jwq = []
        for pvrou__huj in range(kyol__gzyhl):
            jmdl__jwq.append('t1_keys[{}]'.format(pvrou__huj))
        for pvrou__huj in range(len(left_other_names)):
            jmdl__jwq.append('data_left[{}]'.format(pvrou__huj))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(kyon__ibzkn) for kyon__ibzkn in
            jmdl__jwq))
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            qhku__kvewo = right_other_names[1:]
            vmlg__aimdc = right_other_names[0]
        else:
            qhku__kvewo = right_other_names
            vmlg__aimdc = None
        kvlc__rimpr = '()' if len(qhku__kvewo) == 0 else f'({qhku__kvewo[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({vmlg__aimdc}, {kvlc__rimpr}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        skq__dlxdy = []
        for pvrou__huj in range(kyol__gzyhl):
            skq__dlxdy.append('t2_keys[{}]'.format(pvrou__huj))
        for pvrou__huj in range(len(right_other_names)):
            skq__dlxdy.append('data_right[{}]'.format(pvrou__huj))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(kyon__ibzkn) for kyon__ibzkn in
            skq__dlxdy))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(iow__pur, dtype=np.int64)
    glbs['use_nullable_arr_type'] = np.array(xrtrp__qzeii, dtype=np.int64)
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
        func_text += f"""    out_table = hash_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {kyol__gzyhl}, {len(spfur__rgjzj)}, {len(pafb__klvm)}, vect_same_key.ctypes, key_in_output.ctypes, use_nullable_arr_type.ctypes, {join_node.is_left}, {join_node.is_right}, {join_node.is_join}, {join_node.extra_data_col_num != -1}, {join_node.indicator_col_num != -1}, {join_node.is_na_equal}, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    fxhft__qkvta = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {fxhft__qkvta}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        gbygc__sbzd = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{gbygc__sbzd}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        ffj__exb = {}
        for pvrou__huj, mjma__pypy in enumerate(join_node.left_keys):
            if pvrou__huj in left_used_key_nums:
                pgrqb__mmu = join_node.left_var_map[mjma__pypy]
                ffj__exb[pvrou__huj] = join_node.left_to_output_map[pgrqb__mmu]
        buen__tuu = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, ffj__exb, False)
        vnoo__kav = {}
        for pvrou__huj, mjma__pypy in enumerate(join_node.right_keys):
            if pvrou__huj in right_used_key_nums:
                pgrqb__mmu = join_node.right_var_map[mjma__pypy]
                vnoo__kav[pvrou__huj] = join_node.right_to_output_map[
                    pgrqb__mmu]
        buen__tuu.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, vnoo__kav, False))
        ffqwv__ngl = False
        ihahd__qylp = False
        if join_node.has_live_out_table_var:
            gxos__zsskl = list(out_table_type.arr_types)
        else:
            gxos__zsskl = None
        for jus__xtm, opzku__qdswm in buen__tuu.items():
            if jus__xtm < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                gxos__zsskl[jus__xtm] = opzku__qdswm
                ffqwv__ngl = True
            else:
                zpfs__nvin = opzku__qdswm
                ihahd__qylp = True
        if ffqwv__ngl:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            txlp__mpvr = bodo.TableType(tuple(gxos__zsskl))
            glbs['py_table_type'] = txlp__mpvr
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if ihahd__qylp:
            glbs['index_col_type'] = zpfs__nvin
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
    buen__tuu: Dict[int, types.Type] = {}
    kyol__gzyhl = len(matched_key_types)
    for pvrou__huj in range(kyol__gzyhl):
        if used_key_nums is None or pvrou__huj in used_key_nums:
            if matched_key_types[pvrou__huj] != key_types[pvrou__huj] and (
                convert_dict_col or key_types[pvrou__huj] != bodo.
                dict_str_arr_type):
                gbygc__sbzd = output_map[pvrou__huj]
                buen__tuu[gbygc__sbzd] = matched_key_types[pvrou__huj]
    return buen__tuu


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    laj__mztf = bodo.libs.distributed_api.get_size()
    unhn__jxqew = np.empty(laj__mztf, left_key_arrs[0].dtype)
    invho__ubo = np.empty(laj__mztf, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(unhn__jxqew, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(invho__ubo, left_key_arrs[0][-1])
    jfkq__ofngu = np.zeros(laj__mztf, np.int32)
    svjin__axi = np.zeros(laj__mztf, np.int32)
    ymnxs__tnz = np.zeros(laj__mztf, np.int32)
    tcr__qpv = right_key_arrs[0][0]
    uyd__jxif = right_key_arrs[0][-1]
    elpbh__ego = -1
    pvrou__huj = 0
    while pvrou__huj < laj__mztf - 1 and invho__ubo[pvrou__huj] < tcr__qpv:
        pvrou__huj += 1
    while pvrou__huj < laj__mztf and unhn__jxqew[pvrou__huj] <= uyd__jxif:
        elpbh__ego, klz__zml = _count_overlap(right_key_arrs[0],
            unhn__jxqew[pvrou__huj], invho__ubo[pvrou__huj])
        if elpbh__ego != 0:
            elpbh__ego -= 1
            klz__zml += 1
        jfkq__ofngu[pvrou__huj] = klz__zml
        svjin__axi[pvrou__huj] = elpbh__ego
        pvrou__huj += 1
    while pvrou__huj < laj__mztf:
        jfkq__ofngu[pvrou__huj] = 1
        svjin__axi[pvrou__huj] = len(right_key_arrs[0]) - 1
        pvrou__huj += 1
    bodo.libs.distributed_api.alltoall(jfkq__ofngu, ymnxs__tnz, 1)
    dnagv__uehah = ymnxs__tnz.sum()
    nxe__mrs = np.empty(dnagv__uehah, right_key_arrs[0].dtype)
    gaj__qaf = alloc_arr_tup(dnagv__uehah, right_data)
    zlvea__bkh = bodo.ir.join.calc_disp(ymnxs__tnz)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], nxe__mrs,
        jfkq__ofngu, ymnxs__tnz, svjin__axi, zlvea__bkh)
    bodo.libs.distributed_api.alltoallv_tup(right_data, gaj__qaf,
        jfkq__ofngu, ymnxs__tnz, svjin__axi, zlvea__bkh)
    return (nxe__mrs,), gaj__qaf


@numba.njit
def _count_overlap(r_key_arr, start, end):
    klz__zml = 0
    elpbh__ego = 0
    frep__fmxe = 0
    while frep__fmxe < len(r_key_arr) and r_key_arr[frep__fmxe] < start:
        elpbh__ego += 1
        frep__fmxe += 1
    while frep__fmxe < len(r_key_arr) and start <= r_key_arr[frep__fmxe
        ] <= end:
        frep__fmxe += 1
        klz__zml += 1
    return elpbh__ego, klz__zml


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    nsj__xkx = np.empty_like(arr)
    nsj__xkx[0] = 0
    for pvrou__huj in range(1, len(arr)):
        nsj__xkx[pvrou__huj] = nsj__xkx[pvrou__huj - 1] + arr[pvrou__huj - 1]
    return nsj__xkx


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    prsgh__lhps = len(left_keys[0])
    pem__qhjsa = len(right_keys[0])
    cohk__zhfzl = alloc_arr_tup(prsgh__lhps, left_keys)
    qqhna__ngig = alloc_arr_tup(prsgh__lhps, right_keys)
    nmdz__zblzt = alloc_arr_tup(prsgh__lhps, data_left)
    nob__tpd = alloc_arr_tup(prsgh__lhps, data_right)
    lhkg__hxk = 0
    flbc__dlhi = 0
    for lhkg__hxk in range(prsgh__lhps):
        if flbc__dlhi < 0:
            flbc__dlhi = 0
        while flbc__dlhi < pem__qhjsa and getitem_arr_tup(right_keys,
            flbc__dlhi) <= getitem_arr_tup(left_keys, lhkg__hxk):
            flbc__dlhi += 1
        flbc__dlhi -= 1
        setitem_arr_tup(cohk__zhfzl, lhkg__hxk, getitem_arr_tup(left_keys,
            lhkg__hxk))
        setitem_arr_tup(nmdz__zblzt, lhkg__hxk, getitem_arr_tup(data_left,
            lhkg__hxk))
        if flbc__dlhi >= 0:
            setitem_arr_tup(qqhna__ngig, lhkg__hxk, getitem_arr_tup(
                right_keys, flbc__dlhi))
            setitem_arr_tup(nob__tpd, lhkg__hxk, getitem_arr_tup(data_right,
                flbc__dlhi))
        else:
            bodo.libs.array_kernels.setna_tup(qqhna__ngig, lhkg__hxk)
            bodo.libs.array_kernels.setna_tup(nob__tpd, lhkg__hxk)
    return cohk__zhfzl, qqhna__ngig, nmdz__zblzt, nob__tpd
