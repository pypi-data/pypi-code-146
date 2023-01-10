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
        stx__alrh = func.signature
        tidvu__vvscl = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        negn__dewvg = cgutils.get_or_insert_function(builder.module,
            tidvu__vvscl, sym._literal_value)
        builder.call(negn__dewvg, [context.get_constant_null(stx__alrh.args
            [0]), context.get_constant_null(stx__alrh.args[1]), context.
            get_constant_null(stx__alrh.args[2]), context.get_constant_null
            (stx__alrh.args[3]), context.get_constant_null(stx__alrh.args[4
            ]), context.get_constant_null(stx__alrh.args[5]), context.
            get_constant(types.int64, 0), context.get_constant(types.int64, 0)]
            )
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
        zro__zphe = left_df_type.columns
        weml__hoqi = right_df_type.columns
        self.left_col_names = zro__zphe
        self.right_col_names = weml__hoqi
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(zro__zphe) if self.is_left_table else 0
        self.n_right_table_cols = len(weml__hoqi) if self.is_right_table else 0
        dpx__gzsax = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        tzz__exooi = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(dpx__gzsax)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(tzz__exooi)
        self.left_var_map = {jufvi__fhp: mmu__mssuk for mmu__mssuk,
            jufvi__fhp in enumerate(zro__zphe)}
        self.right_var_map = {jufvi__fhp: mmu__mssuk for mmu__mssuk,
            jufvi__fhp in enumerate(weml__hoqi)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = dpx__gzsax
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = tzz__exooi
        self.left_key_set = set(self.left_var_map[jufvi__fhp] for
            jufvi__fhp in left_keys)
        self.right_key_set = set(self.right_var_map[jufvi__fhp] for
            jufvi__fhp in right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[jufvi__fhp] for
                jufvi__fhp in zro__zphe if f'(left.{jufvi__fhp})' in
                gen_cond_expr)
            self.right_cond_cols = set(self.right_var_map[jufvi__fhp] for
                jufvi__fhp in weml__hoqi if f'(right.{jufvi__fhp})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        vzf__amx: int = -1
        mvmqq__lvby = set(left_keys) & set(right_keys)
        ohjuh__tjgwc = set(zro__zphe) & set(weml__hoqi)
        wlap__izph = ohjuh__tjgwc - mvmqq__lvby
        cponr__zzct: Dict[int, (Literal['left', 'right'], int)] = {}
        qkkmd__bvwgv: Dict[int, int] = {}
        tqbp__orrce: Dict[int, int] = {}
        for mmu__mssuk, jufvi__fhp in enumerate(zro__zphe):
            if jufvi__fhp in wlap__izph:
                xed__wppa = str(jufvi__fhp) + suffix_left
                ncst__nkmv = out_df_type.column_index[xed__wppa]
                if (right_index and not left_index and mmu__mssuk in self.
                    left_key_set):
                    vzf__amx = out_df_type.column_index[jufvi__fhp]
                    cponr__zzct[vzf__amx] = 'left', mmu__mssuk
            else:
                ncst__nkmv = out_df_type.column_index[jufvi__fhp]
            cponr__zzct[ncst__nkmv] = 'left', mmu__mssuk
            qkkmd__bvwgv[mmu__mssuk] = ncst__nkmv
        for mmu__mssuk, jufvi__fhp in enumerate(weml__hoqi):
            if jufvi__fhp not in mvmqq__lvby:
                if jufvi__fhp in wlap__izph:
                    inzyf__rjktq = str(jufvi__fhp) + suffix_right
                    ncst__nkmv = out_df_type.column_index[inzyf__rjktq]
                    if (left_index and not right_index and mmu__mssuk in
                        self.right_key_set):
                        vzf__amx = out_df_type.column_index[jufvi__fhp]
                        cponr__zzct[vzf__amx] = 'right', mmu__mssuk
                else:
                    ncst__nkmv = out_df_type.column_index[jufvi__fhp]
                cponr__zzct[ncst__nkmv] = 'right', mmu__mssuk
                tqbp__orrce[mmu__mssuk] = ncst__nkmv
        if self.left_vars[-1] is not None:
            qkkmd__bvwgv[dpx__gzsax] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            tqbp__orrce[tzz__exooi] = self.n_out_table_cols
        self.out_to_input_col_map = cponr__zzct
        self.left_to_output_map = qkkmd__bvwgv
        self.right_to_output_map = tqbp__orrce
        self.extra_data_col_num = vzf__amx
        if self.out_data_vars[1] is not None:
            ptrty__amv = 'left' if right_index else 'right'
            if ptrty__amv == 'left':
                havm__yii = dpx__gzsax
            elif ptrty__amv == 'right':
                havm__yii = tzz__exooi
        else:
            ptrty__amv = None
            havm__yii = -1
        self.index_source = ptrty__amv
        self.index_col_num = havm__yii
        nxy__irv = []
        muz__ngyp = len(left_keys)
        for elnbb__oih in range(muz__ngyp):
            heh__tvo = left_keys[elnbb__oih]
            tbm__kdg = right_keys[elnbb__oih]
            nxy__irv.append(heh__tvo == tbm__kdg)
        self.vect_same_key = nxy__irv

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
        for dqgm__pfpkx in self.left_vars:
            if dqgm__pfpkx is not None:
                vars.append(dqgm__pfpkx)
        return vars

    def get_live_right_vars(self):
        vars = []
        for dqgm__pfpkx in self.right_vars:
            if dqgm__pfpkx is not None:
                vars.append(dqgm__pfpkx)
        return vars

    def get_live_out_vars(self):
        vars = []
        for dqgm__pfpkx in self.out_data_vars:
            if dqgm__pfpkx is not None:
                vars.append(dqgm__pfpkx)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        pxxt__ktr = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[pxxt__ktr])
                pxxt__ktr += 1
            else:
                left_vars.append(None)
            start = 1
        biw__nvr = max(self.n_left_table_cols - 1, 0)
        for mmu__mssuk in range(start, len(self.left_vars)):
            if mmu__mssuk + biw__nvr in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[pxxt__ktr])
                pxxt__ktr += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        pxxt__ktr = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[pxxt__ktr])
                pxxt__ktr += 1
            else:
                right_vars.append(None)
            start = 1
        biw__nvr = max(self.n_right_table_cols - 1, 0)
        for mmu__mssuk in range(start, len(self.right_vars)):
            if mmu__mssuk + biw__nvr in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[pxxt__ktr])
                pxxt__ktr += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        pdum__irwdp = [self.has_live_out_table_var, self.has_live_out_index_var
            ]
        pxxt__ktr = 0
        for mmu__mssuk in range(len(self.out_data_vars)):
            if not pdum__irwdp[mmu__mssuk]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[pxxt__ktr])
                pxxt__ktr += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {mmu__mssuk for mmu__mssuk in self.out_used_cols if 
            mmu__mssuk < self.n_out_table_cols}

    def __repr__(self):
        phc__vjmfs = ', '.join([f'{jufvi__fhp}' for jufvi__fhp in self.
            left_col_names])
        jxj__enl = f'left={{{phc__vjmfs}}}'
        phc__vjmfs = ', '.join([f'{jufvi__fhp}' for jufvi__fhp in self.
            right_col_names])
        bmi__pgo = f'right={{{phc__vjmfs}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, jxj__enl, bmi__pgo)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    pao__xxvxm = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    gwxr__brov = []
    iumtz__qalhm = join_node.get_live_left_vars()
    for cbky__rzid in iumtz__qalhm:
        atuj__xzvte = typemap[cbky__rzid.name]
        hst__rwwn = equiv_set.get_shape(cbky__rzid)
        if hst__rwwn:
            gwxr__brov.append(hst__rwwn[0])
    if len(gwxr__brov) > 1:
        equiv_set.insert_equiv(*gwxr__brov)
    gwxr__brov = []
    iumtz__qalhm = list(join_node.get_live_right_vars())
    for cbky__rzid in iumtz__qalhm:
        atuj__xzvte = typemap[cbky__rzid.name]
        hst__rwwn = equiv_set.get_shape(cbky__rzid)
        if hst__rwwn:
            gwxr__brov.append(hst__rwwn[0])
    if len(gwxr__brov) > 1:
        equiv_set.insert_equiv(*gwxr__brov)
    gwxr__brov = []
    for obgde__ziv in join_node.get_live_out_vars():
        atuj__xzvte = typemap[obgde__ziv.name]
        johf__glr = array_analysis._gen_shape_call(equiv_set, obgde__ziv,
            atuj__xzvte.ndim, None, pao__xxvxm)
        equiv_set.insert_equiv(obgde__ziv, johf__glr)
        gwxr__brov.append(johf__glr[0])
        equiv_set.define(obgde__ziv, set())
    if len(gwxr__brov) > 1:
        equiv_set.insert_equiv(*gwxr__brov)
    return [], pao__xxvxm


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    oayq__cbuyc = Distribution.OneD
    hwzdf__iryu = Distribution.OneD
    for cbky__rzid in join_node.get_live_left_vars():
        oayq__cbuyc = Distribution(min(oayq__cbuyc.value, array_dists[
            cbky__rzid.name].value))
    for cbky__rzid in join_node.get_live_right_vars():
        hwzdf__iryu = Distribution(min(hwzdf__iryu.value, array_dists[
            cbky__rzid.name].value))
    hwckg__hxv = Distribution.OneD_Var
    for obgde__ziv in join_node.get_live_out_vars():
        if obgde__ziv.name in array_dists:
            hwckg__hxv = Distribution(min(hwckg__hxv.value, array_dists[
                obgde__ziv.name].value))
    bjkt__tlw = Distribution(min(hwckg__hxv.value, oayq__cbuyc.value))
    phf__lwvm = Distribution(min(hwckg__hxv.value, hwzdf__iryu.value))
    hwckg__hxv = Distribution(max(bjkt__tlw.value, phf__lwvm.value))
    for obgde__ziv in join_node.get_live_out_vars():
        array_dists[obgde__ziv.name] = hwckg__hxv
    if hwckg__hxv != Distribution.OneD_Var:
        oayq__cbuyc = hwckg__hxv
        hwzdf__iryu = hwckg__hxv
    for cbky__rzid in join_node.get_live_left_vars():
        array_dists[cbky__rzid.name] = oayq__cbuyc
    for cbky__rzid in join_node.get_live_right_vars():
        array_dists[cbky__rzid.name] = hwzdf__iryu
    join_node.left_dist = oayq__cbuyc
    join_node.right_dist = hwzdf__iryu


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(dqgm__pfpkx, callback,
        cbdata) for dqgm__pfpkx in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(dqgm__pfpkx, callback,
        cbdata) for dqgm__pfpkx in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(dqgm__pfpkx,
        callback, cbdata) for dqgm__pfpkx in join_node.get_live_out_vars()])
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
        ieioz__nxxpq = []
        nqwsu__hhusd = join_node.get_out_table_var()
        if nqwsu__hhusd.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for uxe__qsi in join_node.out_to_input_col_map.keys():
            if uxe__qsi in join_node.out_used_cols:
                continue
            ieioz__nxxpq.append(uxe__qsi)
            if join_node.indicator_col_num == uxe__qsi:
                join_node.indicator_col_num = -1
                continue
            if uxe__qsi == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            gusoz__tuvan, uxe__qsi = join_node.out_to_input_col_map[uxe__qsi]
            if gusoz__tuvan == 'left':
                if (uxe__qsi not in join_node.left_key_set and uxe__qsi not in
                    join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(uxe__qsi)
                    if not join_node.is_left_table:
                        join_node.left_vars[uxe__qsi] = None
            elif gusoz__tuvan == 'right':
                if (uxe__qsi not in join_node.right_key_set and uxe__qsi not in
                    join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(uxe__qsi)
                    if not join_node.is_right_table:
                        join_node.right_vars[uxe__qsi] = None
        for mmu__mssuk in ieioz__nxxpq:
            del join_node.out_to_input_col_map[mmu__mssuk]
        if join_node.is_left_table:
            ejdw__sijkk = set(range(join_node.n_left_table_cols))
            hogl__keqg = not bool(ejdw__sijkk - join_node.left_dead_var_inds)
            if hogl__keqg:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            ejdw__sijkk = set(range(join_node.n_right_table_cols))
            hogl__keqg = not bool(ejdw__sijkk - join_node.right_dead_var_inds)
            if hogl__keqg:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        rszn__ruvhh = join_node.get_out_index_var()
        if rszn__ruvhh.name not in lives:
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
    ruy__pwzw = False
    if join_node.has_live_out_table_var:
        zfznd__nfok = join_node.get_out_table_var().name
        iwkxf__bhmue, zjwb__icdy, xjn__knsw = get_live_column_nums_block(
            column_live_map, equiv_vars, zfznd__nfok)
        if not (zjwb__icdy or xjn__knsw):
            iwkxf__bhmue = trim_extra_used_columns(iwkxf__bhmue, join_node.
                n_out_table_cols)
            snb__gmor = join_node.get_out_table_used_cols()
            if len(iwkxf__bhmue) != len(snb__gmor):
                ruy__pwzw = not (join_node.is_left_table and join_node.
                    is_right_table)
                dxyp__mdgac = snb__gmor - iwkxf__bhmue
                join_node.out_used_cols = join_node.out_used_cols - dxyp__mdgac
    return ruy__pwzw


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        ycflp__gbega = join_node.get_out_table_var()
        koeb__dpyf, zjwb__icdy, xjn__knsw = _compute_table_column_uses(
            ycflp__gbega.name, table_col_use_map, equiv_vars)
    else:
        koeb__dpyf, zjwb__icdy, xjn__knsw = set(), False, False
    if join_node.has_live_left_table_var:
        iuomi__gyjp = join_node.left_vars[0].name
        bihzq__kyu, imis__mzt, cpnbo__bmwd = block_use_map[iuomi__gyjp]
        if not (imis__mzt or cpnbo__bmwd):
            fnay__lcn = set([join_node.out_to_input_col_map[mmu__mssuk][1] for
                mmu__mssuk in koeb__dpyf if join_node.out_to_input_col_map[
                mmu__mssuk][0] == 'left'])
            myjpb__azfe = set(mmu__mssuk for mmu__mssuk in join_node.
                left_key_set | join_node.left_cond_cols if mmu__mssuk <
                join_node.n_left_table_cols)
            if not (zjwb__icdy or xjn__knsw):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (fnay__lcn | myjpb__azfe)
            block_use_map[iuomi__gyjp] = (bihzq__kyu | fnay__lcn |
                myjpb__azfe, zjwb__icdy or xjn__knsw, False)
    if join_node.has_live_right_table_var:
        rlryg__wayed = join_node.right_vars[0].name
        bihzq__kyu, imis__mzt, cpnbo__bmwd = block_use_map[rlryg__wayed]
        if not (imis__mzt or cpnbo__bmwd):
            bqhr__efv = set([join_node.out_to_input_col_map[mmu__mssuk][1] for
                mmu__mssuk in koeb__dpyf if join_node.out_to_input_col_map[
                mmu__mssuk][0] == 'right'])
            ehu__auuti = set(mmu__mssuk for mmu__mssuk in join_node.
                right_key_set | join_node.right_cond_cols if mmu__mssuk <
                join_node.n_right_table_cols)
            if not (zjwb__icdy or xjn__knsw):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (bqhr__efv | ehu__auuti)
            block_use_map[rlryg__wayed] = (bihzq__kyu | bqhr__efv |
                ehu__auuti, zjwb__icdy or xjn__knsw, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({jvmya__ukmtm.name for jvmya__ukmtm in join_node.
        get_live_left_vars()})
    use_set.update({jvmya__ukmtm.name for jvmya__ukmtm in join_node.
        get_live_right_vars()})
    def_set.update({jvmya__ukmtm.name for jvmya__ukmtm in join_node.
        get_live_out_vars()})
    if join_node.how == 'cross':
        use_set.add(join_node.left_len_var.name)
        use_set.add(join_node.right_len_var.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    pqpfq__uyyp = set(jvmya__ukmtm.name for jvmya__ukmtm in join_node.
        get_live_out_vars())
    return set(), pqpfq__uyyp


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(dqgm__pfpkx, var_dict) for
        dqgm__pfpkx in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(dqgm__pfpkx, var_dict
        ) for dqgm__pfpkx in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(dqgm__pfpkx,
        var_dict) for dqgm__pfpkx in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = replace_vars_inner(join_node.left_len_var,
            var_dict)
        join_node.right_len_var = replace_vars_inner(join_node.
            right_len_var, var_dict)


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for cbky__rzid in join_node.get_live_out_vars():
        definitions[cbky__rzid.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def _gen_cross_join_len(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel):
    func_text = 'def f(left_len, right_len):\n'
    gxznu__hukok = 'bodo.libs.distributed_api.get_size()'
    aydof__zhed = 'bodo.libs.distributed_api.get_rank()'
    if left_parallel:
        func_text += f"""  left_len = bodo.libs.distributed_api.get_node_portion(left_len, {gxznu__hukok}, {aydof__zhed})
"""
    if right_parallel and not left_parallel:
        func_text += f"""  right_len = bodo.libs.distributed_api.get_node_portion(right_len, {gxznu__hukok}, {aydof__zhed})
"""
    func_text += '  n_rows = left_len * right_len\n'
    func_text += '  py_table = init_table(py_table_type, False)\n'
    func_text += '  py_table = set_table_len(py_table, n_rows)\n'
    jnwb__wkq = {}
    exec(func_text, {}, jnwb__wkq)
    doemq__hjbze = jnwb__wkq['f']
    glbs = {'py_table_type': out_table_type, 'init_table': bodo.hiframes.
        table.init_table, 'set_table_len': bodo.hiframes.table.
        set_table_len, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value), 'bodo': bodo}
    uqnkb__xpu = [join_node.left_len_var, join_node.right_len_var]
    lri__vxs = tuple(typemap[jvmya__ukmtm.name] for jvmya__ukmtm in uqnkb__xpu)
    knd__pqsy = compile_to_numba_ir(doemq__hjbze, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=lri__vxs, typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(knd__pqsy, uqnkb__xpu)
    iznd__kwoky = knd__pqsy.body[:-3]
    iznd__kwoky[-1].target = join_node.out_data_vars[0]
    return iznd__kwoky


def _gen_cross_join_repeat(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel, left_is_dead):
    iumtz__qalhm = (join_node.right_vars if left_is_dead else join_node.
        left_vars)
    frdn__tribn = ', '.join(f't{mmu__mssuk}' for mmu__mssuk in range(len(
        iumtz__qalhm)) if iumtz__qalhm[mmu__mssuk] is not None)
    ykw__ezpg = len(join_node.right_col_names) if left_is_dead else len(
        join_node.left_col_names)
    ceo__zmjg = (join_node.is_right_table if left_is_dead else join_node.
        is_left_table)
    eyin__sifm = (join_node.right_dead_var_inds if left_is_dead else
        join_node.left_dead_var_inds)
    lik__qbz = [(f'get_table_data(t0, {mmu__mssuk})' if ceo__zmjg else
        f't{mmu__mssuk}') for mmu__mssuk in range(ykw__ezpg)]
    hnjq__mebkl = ', '.join(
        f'bodo.libs.array_kernels.repeat_kernel({lik__qbz[mmu__mssuk]}, repeats)'
         if mmu__mssuk not in eyin__sifm else 'None' for mmu__mssuk in
        range(ykw__ezpg))
    emymn__gweum = len(out_table_type.arr_types)
    ewazh__gdvql = [join_node.out_to_input_col_map.get(mmu__mssuk, (-1, -1)
        )[1] for mmu__mssuk in range(emymn__gweum)]
    gxznu__hukok = 'bodo.libs.distributed_api.get_size()'
    aydof__zhed = 'bodo.libs.distributed_api.get_rank()'
    szqf__apjb = 'left_len' if left_is_dead else 'right_len'
    iaexg__foex = right_parallel if left_is_dead else left_parallel
    hjfyd__efxuu = left_parallel if left_is_dead else right_parallel
    ivc__ksxc = not iaexg__foex and hjfyd__efxuu
    qge__smbdr = (
        f'bodo.libs.distributed_api.get_node_portion({szqf__apjb}, {gxznu__hukok}, {aydof__zhed})'
         if ivc__ksxc else szqf__apjb)
    func_text = f'def f({frdn__tribn}, left_len, right_len):\n'
    func_text += f'  repeats = {qge__smbdr}\n'
    func_text += f'  out_data = ({hnjq__mebkl},)\n'
    func_text += f"""  py_table = logical_table_to_table(out_data, (), col_inds, {ykw__ezpg}, out_table_type, used_cols)
"""
    jnwb__wkq = {}
    exec(func_text, {}, jnwb__wkq)
    doemq__hjbze = jnwb__wkq['f']
    glbs = {'out_table_type': out_table_type, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value), 'bodo': bodo, 'used_cols':
        bodo.utils.typing.MetaType(tuple(join_node.out_used_cols)),
        'col_inds': bodo.utils.typing.MetaType(tuple(ewazh__gdvql)),
        'logical_table_to_table': bodo.hiframes.table.
        logical_table_to_table, 'get_table_data': bodo.hiframes.table.
        get_table_data}
    uqnkb__xpu = [jvmya__ukmtm for jvmya__ukmtm in iumtz__qalhm if 
        jvmya__ukmtm is not None] + [join_node.left_len_var, join_node.
        right_len_var]
    lri__vxs = tuple(typemap[jvmya__ukmtm.name] for jvmya__ukmtm in uqnkb__xpu)
    knd__pqsy = compile_to_numba_ir(doemq__hjbze, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=lri__vxs, typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(knd__pqsy, uqnkb__xpu)
    iznd__kwoky = knd__pqsy.body[:-3]
    iznd__kwoky[-1].target = join_node.out_data_vars[0]
    return iznd__kwoky


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        ouzt__bbek = join_node.loc.strformat()
        qynh__njwb = [join_node.left_col_names[mmu__mssuk] for mmu__mssuk in
            sorted(set(range(len(join_node.left_col_names))) - join_node.
            left_dead_var_inds)]
        xssk__eargh = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', xssk__eargh,
            ouzt__bbek, qynh__njwb)
        vdl__gdgje = [join_node.right_col_names[mmu__mssuk] for mmu__mssuk in
            sorted(set(range(len(join_node.right_col_names))) - join_node.
            right_dead_var_inds)]
        xssk__eargh = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', xssk__eargh,
            ouzt__bbek, vdl__gdgje)
        vpsh__syp = [join_node.out_col_names[mmu__mssuk] for mmu__mssuk in
            sorted(join_node.get_out_table_used_cols())]
        xssk__eargh = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', xssk__eargh,
            ouzt__bbek, vpsh__syp)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    muz__ngyp = len(join_node.left_keys)
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
    elif join_node.how == 'cross' and all(mmu__mssuk in join_node.
        left_dead_var_inds for mmu__mssuk in range(len(join_node.
        left_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            True)
    elif join_node.how == 'cross' and all(mmu__mssuk in join_node.
        right_dead_var_inds for mmu__mssuk in range(len(join_node.
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
    zly__lomfm = set()
    mpvn__ruxp = set()
    left_logical_physical_map = {}
    right_logical_physical_map = {}
    left_physical_to_logical_list = []
    right_physical_to_logical_list = []
    pbxq__mum = 0
    ieqs__sgndj = 0
    ciha__zfolx = []
    for gvg__sknz, jufvi__fhp in enumerate(join_node.left_keys):
        avqu__pnx = join_node.left_var_map[jufvi__fhp]
        if not join_node.is_left_table:
            ciha__zfolx.append(join_node.left_vars[avqu__pnx])
        pdum__irwdp = 1
        ncst__nkmv = join_node.left_to_output_map[avqu__pnx]
        if jufvi__fhp == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == avqu__pnx):
                out_physical_to_logical_list.append(ncst__nkmv)
                left_used_key_nums.add(gvg__sknz)
                zly__lomfm.add(avqu__pnx)
            else:
                pdum__irwdp = 0
        elif ncst__nkmv not in join_node.out_used_cols:
            pdum__irwdp = 0
        elif avqu__pnx in zly__lomfm:
            pdum__irwdp = 0
        else:
            left_used_key_nums.add(gvg__sknz)
            zly__lomfm.add(avqu__pnx)
            out_physical_to_logical_list.append(ncst__nkmv)
        left_physical_to_logical_list.append(avqu__pnx)
        left_logical_physical_map[avqu__pnx] = pbxq__mum
        pbxq__mum += 1
        left_key_in_output.append(pdum__irwdp)
    ciha__zfolx = tuple(ciha__zfolx)
    gias__snncs = []
    for mmu__mssuk in range(len(join_node.left_col_names)):
        if (mmu__mssuk not in join_node.left_dead_var_inds and mmu__mssuk
             not in join_node.left_key_set):
            if not join_node.is_left_table:
                jvmya__ukmtm = join_node.left_vars[mmu__mssuk]
                gias__snncs.append(jvmya__ukmtm)
            lbjcr__mpw = 1
            rcbr__tids = 1
            ncst__nkmv = join_node.left_to_output_map[mmu__mssuk]
            if mmu__mssuk in join_node.left_cond_cols:
                if ncst__nkmv not in join_node.out_used_cols:
                    lbjcr__mpw = 0
                left_key_in_output.append(lbjcr__mpw)
            elif mmu__mssuk in join_node.left_dead_var_inds:
                lbjcr__mpw = 0
                rcbr__tids = 0
            if lbjcr__mpw:
                out_physical_to_logical_list.append(ncst__nkmv)
            if rcbr__tids:
                left_physical_to_logical_list.append(mmu__mssuk)
                left_logical_physical_map[mmu__mssuk] = pbxq__mum
                pbxq__mum += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            gias__snncs.append(join_node.left_vars[join_node.index_col_num])
        ncst__nkmv = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(ncst__nkmv)
        left_physical_to_logical_list.append(join_node.index_col_num)
    gias__snncs = tuple(gias__snncs)
    if join_node.is_left_table:
        gias__snncs = tuple(join_node.get_live_left_vars())
    tje__aqcga = []
    for gvg__sknz, jufvi__fhp in enumerate(join_node.right_keys):
        avqu__pnx = join_node.right_var_map[jufvi__fhp]
        if not join_node.is_right_table:
            tje__aqcga.append(join_node.right_vars[avqu__pnx])
        if not join_node.vect_same_key[gvg__sknz] and not join_node.is_join:
            pdum__irwdp = 1
            if avqu__pnx not in join_node.right_to_output_map:
                pdum__irwdp = 0
            else:
                ncst__nkmv = join_node.right_to_output_map[avqu__pnx]
                if jufvi__fhp == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        avqu__pnx):
                        out_physical_to_logical_list.append(ncst__nkmv)
                        right_used_key_nums.add(gvg__sknz)
                        mpvn__ruxp.add(avqu__pnx)
                    else:
                        pdum__irwdp = 0
                elif ncst__nkmv not in join_node.out_used_cols:
                    pdum__irwdp = 0
                elif avqu__pnx in mpvn__ruxp:
                    pdum__irwdp = 0
                else:
                    right_used_key_nums.add(gvg__sknz)
                    mpvn__ruxp.add(avqu__pnx)
                    out_physical_to_logical_list.append(ncst__nkmv)
            right_key_in_output.append(pdum__irwdp)
        right_physical_to_logical_list.append(avqu__pnx)
        right_logical_physical_map[avqu__pnx] = ieqs__sgndj
        ieqs__sgndj += 1
    tje__aqcga = tuple(tje__aqcga)
    myrob__ugg = []
    for mmu__mssuk in range(len(join_node.right_col_names)):
        if (mmu__mssuk not in join_node.right_dead_var_inds and mmu__mssuk
             not in join_node.right_key_set):
            if not join_node.is_right_table:
                myrob__ugg.append(join_node.right_vars[mmu__mssuk])
            lbjcr__mpw = 1
            rcbr__tids = 1
            ncst__nkmv = join_node.right_to_output_map[mmu__mssuk]
            if mmu__mssuk in join_node.right_cond_cols:
                if ncst__nkmv not in join_node.out_used_cols:
                    lbjcr__mpw = 0
                right_key_in_output.append(lbjcr__mpw)
            elif mmu__mssuk in join_node.right_dead_var_inds:
                lbjcr__mpw = 0
                rcbr__tids = 0
            if lbjcr__mpw:
                out_physical_to_logical_list.append(ncst__nkmv)
            if rcbr__tids:
                right_physical_to_logical_list.append(mmu__mssuk)
                right_logical_physical_map[mmu__mssuk] = ieqs__sgndj
                ieqs__sgndj += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            myrob__ugg.append(join_node.right_vars[join_node.index_col_num])
        ncst__nkmv = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(ncst__nkmv)
        right_physical_to_logical_list.append(join_node.index_col_num)
    myrob__ugg = tuple(myrob__ugg)
    if join_node.is_right_table:
        myrob__ugg = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    uqnkb__xpu = ciha__zfolx + tje__aqcga + gias__snncs + myrob__ugg
    lri__vxs = tuple(typemap[jvmya__ukmtm.name] for jvmya__ukmtm in uqnkb__xpu)
    left_other_names = tuple('t1_c' + str(mmu__mssuk) for mmu__mssuk in
        range(len(gias__snncs)))
    right_other_names = tuple('t2_c' + str(mmu__mssuk) for mmu__mssuk in
        range(len(myrob__ugg)))
    if join_node.is_left_table:
        rowg__wmaw = ()
    else:
        rowg__wmaw = tuple('t1_key' + str(mmu__mssuk) for mmu__mssuk in
            range(muz__ngyp))
    if join_node.is_right_table:
        qnft__iqi = ()
    else:
        qnft__iqi = tuple('t2_key' + str(mmu__mssuk) for mmu__mssuk in
            range(muz__ngyp))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(rowg__wmaw + qnft__iqi +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            fpj__npvar = typemap[join_node.left_vars[0].name]
        else:
            fpj__npvar = types.none
        for dosuo__ustma in left_physical_to_logical_list:
            if dosuo__ustma < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                atuj__xzvte = fpj__npvar.arr_types[dosuo__ustma]
            else:
                atuj__xzvte = typemap[join_node.left_vars[-1].name]
            if dosuo__ustma in join_node.left_key_set:
                left_key_types.append(atuj__xzvte)
            else:
                left_other_types.append(atuj__xzvte)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[jvmya__ukmtm.name] for jvmya__ukmtm in
            ciha__zfolx)
        left_other_types = tuple([typemap[jufvi__fhp.name] for jufvi__fhp in
            gias__snncs])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            fpj__npvar = typemap[join_node.right_vars[0].name]
        else:
            fpj__npvar = types.none
        for dosuo__ustma in right_physical_to_logical_list:
            if dosuo__ustma < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                atuj__xzvte = fpj__npvar.arr_types[dosuo__ustma]
            else:
                atuj__xzvte = typemap[join_node.right_vars[-1].name]
            if dosuo__ustma in join_node.right_key_set:
                right_key_types.append(atuj__xzvte)
            else:
                right_other_types.append(atuj__xzvte)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[jvmya__ukmtm.name] for jvmya__ukmtm in
            tje__aqcga)
        right_other_types = tuple([typemap[jufvi__fhp.name] for jufvi__fhp in
            myrob__ugg])
    matched_key_types = []
    for mmu__mssuk in range(muz__ngyp):
        zwp__eioqh = _match_join_key_types(left_key_types[mmu__mssuk],
            right_key_types[mmu__mssuk], loc)
        glbs[f'key_type_{mmu__mssuk}'] = zwp__eioqh
        matched_key_types.append(zwp__eioqh)
    if join_node.is_left_table:
        raow__lcv = determine_table_cast_map(matched_key_types,
            left_key_types, None, {mmu__mssuk: join_node.left_var_map[
            sops__iqqg] for mmu__mssuk, sops__iqqg in enumerate(join_node.
            left_keys)}, True)
        if raow__lcv:
            dmbhj__ewydh = False
            rsfi__aer = False
            ijk__runoz = None
            if join_node.has_live_left_table_var:
                lco__twkt = list(typemap[join_node.left_vars[0].name].arr_types
                    )
            else:
                lco__twkt = None
            for uxe__qsi, atuj__xzvte in raow__lcv.items():
                if uxe__qsi < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    lco__twkt[uxe__qsi] = atuj__xzvte
                    dmbhj__ewydh = True
                else:
                    ijk__runoz = atuj__xzvte
                    rsfi__aer = True
            if dmbhj__ewydh:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(lco__twkt))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if rsfi__aer:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = ijk__runoz
    else:
        func_text += '    t1_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({rowg__wmaw[mmu__mssuk]}, key_type_{mmu__mssuk})'
             if left_key_types[mmu__mssuk] != matched_key_types[mmu__mssuk]
             else f'{rowg__wmaw[mmu__mssuk]}' for mmu__mssuk in range(
            muz__ngyp)), ',' if muz__ngyp != 0 else '')
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        raow__lcv = determine_table_cast_map(matched_key_types,
            right_key_types, None, {mmu__mssuk: join_node.right_var_map[
            sops__iqqg] for mmu__mssuk, sops__iqqg in enumerate(join_node.
            right_keys)}, True)
        if raow__lcv:
            dmbhj__ewydh = False
            rsfi__aer = False
            ijk__runoz = None
            if join_node.has_live_right_table_var:
                lco__twkt = list(typemap[join_node.right_vars[0].name].
                    arr_types)
            else:
                lco__twkt = None
            for uxe__qsi, atuj__xzvte in raow__lcv.items():
                if uxe__qsi < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    lco__twkt[uxe__qsi] = atuj__xzvte
                    dmbhj__ewydh = True
                else:
                    ijk__runoz = atuj__xzvte
                    rsfi__aer = True
            if dmbhj__ewydh:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(lco__twkt))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if rsfi__aer:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = ijk__runoz
    else:
        func_text += '    t2_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({qnft__iqi[mmu__mssuk]}, key_type_{mmu__mssuk})'
             if right_key_types[mmu__mssuk] != matched_key_types[mmu__mssuk
            ] else f'{qnft__iqi[mmu__mssuk]}' for mmu__mssuk in range(
            muz__ngyp)), ',' if muz__ngyp != 0 else '')
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
        for mmu__mssuk in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(mmu__mssuk,
                mmu__mssuk)
        for mmu__mssuk in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                mmu__mssuk, mmu__mssuk)
        for mmu__mssuk in range(muz__ngyp):
            func_text += (
                f'    t1_keys_{mmu__mssuk} = out_t1_keys[{mmu__mssuk}]\n')
        for mmu__mssuk in range(muz__ngyp):
            func_text += (
                f'    t2_keys_{mmu__mssuk} = out_t2_keys[{mmu__mssuk}]\n')
    jnwb__wkq = {}
    exec(func_text, {}, jnwb__wkq)
    doemq__hjbze = jnwb__wkq['f']
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
    knd__pqsy = compile_to_numba_ir(doemq__hjbze, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=lri__vxs, typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(knd__pqsy, uqnkb__xpu)
    iznd__kwoky = knd__pqsy.body[:-3]
    if join_node.has_live_out_index_var:
        iznd__kwoky[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        iznd__kwoky[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        iznd__kwoky.pop(-1)
    elif not join_node.has_live_out_table_var:
        iznd__kwoky.pop(-2)
    return iznd__kwoky


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    xldt__jlam = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{xldt__jlam}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
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
    jnwb__wkq = {}
    exec(func_text, table_getitem_funcs, jnwb__wkq)
    ceogz__sefhh = jnwb__wkq[f'bodo_join_gen_cond{xldt__jlam}']
    fcmdv__zal = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    uuxud__eah = numba.cfunc(fcmdv__zal, nopython=True)(ceogz__sefhh)
    join_gen_cond_cfunc[uuxud__eah.native_name] = uuxud__eah
    join_gen_cond_cfunc_addr[uuxud__eah.native_name] = uuxud__eah.address
    return uuxud__eah, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    vrk__ifv = []
    for jufvi__fhp, itrlf__hfkw in name_to_var_map.items():
        anmcc__qukif = f'({table_name}.{jufvi__fhp})'
        if anmcc__qukif not in expr:
            continue
        jlbqx__jbsf = f'getitem_{table_name}_val_{itrlf__hfkw}'
        if is_table_var:
            nlrzb__psmu = typemap[col_vars[0].name].arr_types[itrlf__hfkw]
        else:
            nlrzb__psmu = typemap[col_vars[itrlf__hfkw].name]
        if is_str_arr_type(nlrzb__psmu
            ) or nlrzb__psmu == bodo.binary_array_type:
            tdyx__jdj = (
                f'{jlbqx__jbsf}({table_name}_table, {table_name}_ind)\n')
        else:
            tdyx__jdj = (
                f'{jlbqx__jbsf}({table_name}_data1, {table_name}_ind)\n')
        alg__pqcb = logical_to_physical_ind[itrlf__hfkw]
        table_getitem_funcs[jlbqx__jbsf
            ] = bodo.libs.array._gen_row_access_intrinsic(nlrzb__psmu,
            alg__pqcb)
        expr = expr.replace(anmcc__qukif, tdyx__jdj)
        rxzd__vda = f'({na_check_name}.{table_name}.{jufvi__fhp})'
        if rxzd__vda in expr:
            rmuvf__suk = f'nacheck_{table_name}_val_{itrlf__hfkw}'
            rdz__uvko = f'_bodo_isna_{table_name}_val_{itrlf__hfkw}'
            if isinstance(nlrzb__psmu, (bodo.libs.int_arr_ext.
                IntegerArrayType, bodo.FloatingArrayType, bodo.TimeArrayType)
                ) or nlrzb__psmu in (bodo.libs.bool_arr_ext.boolean_array,
                bodo.binary_array_type, bodo.datetime_date_array_type
                ) or is_str_arr_type(nlrzb__psmu):
                func_text += f"""  {rdz__uvko} = {rmuvf__suk}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {rdz__uvko} = {rmuvf__suk}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[rmuvf__suk
                ] = bodo.libs.array._gen_row_na_check_intrinsic(nlrzb__psmu,
                alg__pqcb)
            expr = expr.replace(rxzd__vda, rdz__uvko)
        if itrlf__hfkw not in key_set:
            vrk__ifv.append(alg__pqcb)
    return expr, func_text, vrk__ifv


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as nxpyi__gulve:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    jpfj__oslq = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[jvmya__ukmtm.name] in jpfj__oslq for
        jvmya__ukmtm in join_node.get_live_left_vars())
    if not join_node.get_live_left_vars():
        assert join_node.how == 'cross', 'cross join expected if left data is dead'
        left_parallel = join_node.left_dist in jpfj__oslq
    right_parallel = all(array_dists[jvmya__ukmtm.name] in jpfj__oslq for
        jvmya__ukmtm in join_node.get_live_right_vars())
    if not join_node.get_live_right_vars():
        assert join_node.how == 'cross', 'cross join expected if right data is dead'
        right_parallel = join_node.right_dist in jpfj__oslq
    if not left_parallel:
        assert not any(array_dists[jvmya__ukmtm.name] in jpfj__oslq for
            jvmya__ukmtm in join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[jvmya__ukmtm.name] in jpfj__oslq for
            jvmya__ukmtm in join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[jvmya__ukmtm.name] in jpfj__oslq for
            jvmya__ukmtm in join_node.get_live_out_vars())
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
    zynt__twu = set(left_col_nums)
    avbx__tua = set(right_col_nums)
    nxy__irv = join_node.vect_same_key
    jyrch__wgdxl = []
    for mmu__mssuk in range(len(left_key_types)):
        if left_key_in_output[mmu__mssuk]:
            jyrch__wgdxl.append(needs_typechange(matched_key_types[
                mmu__mssuk], join_node.is_right, nxy__irv[mmu__mssuk]))
    cdjg__fzy = len(left_key_types)
    orc__dvh = 0
    vdmcd__rljmd = left_physical_to_logical_list[len(left_key_types):]
    for mmu__mssuk, dosuo__ustma in enumerate(vdmcd__rljmd):
        ycmk__jzkvr = True
        if dosuo__ustma in zynt__twu:
            ycmk__jzkvr = left_key_in_output[cdjg__fzy]
            cdjg__fzy += 1
        if ycmk__jzkvr:
            jyrch__wgdxl.append(needs_typechange(left_other_types[
                mmu__mssuk], join_node.is_right, False))
    for mmu__mssuk in range(len(right_key_types)):
        if not nxy__irv[mmu__mssuk] and not join_node.is_join:
            if right_key_in_output[orc__dvh]:
                jyrch__wgdxl.append(needs_typechange(matched_key_types[
                    mmu__mssuk], join_node.is_left, False))
            orc__dvh += 1
    nxxsr__rcdg = right_physical_to_logical_list[len(right_key_types):]
    for mmu__mssuk, dosuo__ustma in enumerate(nxxsr__rcdg):
        ycmk__jzkvr = True
        if dosuo__ustma in avbx__tua:
            ycmk__jzkvr = right_key_in_output[orc__dvh]
            orc__dvh += 1
        if ycmk__jzkvr:
            jyrch__wgdxl.append(needs_typechange(right_other_types[
                mmu__mssuk], join_node.is_left, False))
    muz__ngyp = len(left_key_types)
    func_text = '    # beginning of _gen_join_cpp_call\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            rrr__igp = left_other_names[1:]
            nqwsu__hhusd = left_other_names[0]
        else:
            rrr__igp = left_other_names
            nqwsu__hhusd = None
        qfk__vxjdi = '()' if len(rrr__igp) == 0 else f'({rrr__igp[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({nqwsu__hhusd}, {qfk__vxjdi}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        eze__cvrsa = []
        for mmu__mssuk in range(muz__ngyp):
            eze__cvrsa.append('t1_keys[{}]'.format(mmu__mssuk))
        for mmu__mssuk in range(len(left_other_names)):
            eze__cvrsa.append('data_left[{}]'.format(mmu__mssuk))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(nvzl__nfehy) for nvzl__nfehy in
            eze__cvrsa))
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            pfa__ddez = right_other_names[1:]
            nqwsu__hhusd = right_other_names[0]
        else:
            pfa__ddez = right_other_names
            nqwsu__hhusd = None
        qfk__vxjdi = '()' if len(pfa__ddez) == 0 else f'({pfa__ddez[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({nqwsu__hhusd}, {qfk__vxjdi}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        rta__tlxs = []
        for mmu__mssuk in range(muz__ngyp):
            rta__tlxs.append('t2_keys[{}]'.format(mmu__mssuk))
        for mmu__mssuk in range(len(right_other_names)):
            rta__tlxs.append('data_right[{}]'.format(mmu__mssuk))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(nvzl__nfehy) for nvzl__nfehy in
            rta__tlxs))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(nxy__irv, dtype=np.int64)
    glbs['use_nullable_arr_type'] = np.array(jyrch__wgdxl, dtype=np.int64)
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
        func_text += f"""    out_table = hash_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {muz__ngyp}, {len(vdmcd__rljmd)}, {len(nxxsr__rcdg)}, vect_same_key.ctypes, key_in_output.ctypes, use_nullable_arr_type.ctypes, {join_node.is_left}, {join_node.is_right}, {join_node.is_join}, {join_node.extra_data_col_num != -1}, {join_node.indicator_col_num != -1}, {join_node.is_na_equal}, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    urma__lshq = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {urma__lshq}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        pxxt__ktr = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{pxxt__ktr}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        fdnlt__bpa = {}
        for mmu__mssuk, sops__iqqg in enumerate(join_node.left_keys):
            if mmu__mssuk in left_used_key_nums:
                gbmj__xwpp = join_node.left_var_map[sops__iqqg]
                fdnlt__bpa[mmu__mssuk] = join_node.left_to_output_map[
                    gbmj__xwpp]
        raow__lcv = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, fdnlt__bpa, False)
        gfxhb__fnetr = {}
        for mmu__mssuk, sops__iqqg in enumerate(join_node.right_keys):
            if mmu__mssuk in right_used_key_nums:
                gbmj__xwpp = join_node.right_var_map[sops__iqqg]
                gfxhb__fnetr[mmu__mssuk] = join_node.right_to_output_map[
                    gbmj__xwpp]
        raow__lcv.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, gfxhb__fnetr, False))
        dmbhj__ewydh = False
        rsfi__aer = False
        if join_node.has_live_out_table_var:
            lco__twkt = list(out_table_type.arr_types)
        else:
            lco__twkt = None
        for uxe__qsi, atuj__xzvte in raow__lcv.items():
            if uxe__qsi < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                lco__twkt[uxe__qsi] = atuj__xzvte
                dmbhj__ewydh = True
            else:
                ijk__runoz = atuj__xzvte
                rsfi__aer = True
        if dmbhj__ewydh:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            lnbh__oalhn = bodo.TableType(tuple(lco__twkt))
            glbs['py_table_type'] = lnbh__oalhn
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if rsfi__aer:
            glbs['index_col_type'] = ijk__runoz
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
    raow__lcv: Dict[int, types.Type] = {}
    muz__ngyp = len(matched_key_types)
    for mmu__mssuk in range(muz__ngyp):
        if used_key_nums is None or mmu__mssuk in used_key_nums:
            if matched_key_types[mmu__mssuk] != key_types[mmu__mssuk] and (
                convert_dict_col or key_types[mmu__mssuk] != bodo.
                dict_str_arr_type):
                pxxt__ktr = output_map[mmu__mssuk]
                raow__lcv[pxxt__ktr] = matched_key_types[mmu__mssuk]
    return raow__lcv


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    gxznu__hukok = bodo.libs.distributed_api.get_size()
    efwy__sdaci = np.empty(gxznu__hukok, left_key_arrs[0].dtype)
    vph__uyi = np.empty(gxznu__hukok, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(efwy__sdaci, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(vph__uyi, left_key_arrs[0][-1])
    hapug__gwa = np.zeros(gxznu__hukok, np.int32)
    jmed__wgtu = np.zeros(gxznu__hukok, np.int32)
    xpepa__dewlo = np.zeros(gxznu__hukok, np.int32)
    mfqey__udv = right_key_arrs[0][0]
    dfjz__jtmqt = right_key_arrs[0][-1]
    biw__nvr = -1
    mmu__mssuk = 0
    while mmu__mssuk < gxznu__hukok - 1 and vph__uyi[mmu__mssuk] < mfqey__udv:
        mmu__mssuk += 1
    while mmu__mssuk < gxznu__hukok and efwy__sdaci[mmu__mssuk] <= dfjz__jtmqt:
        biw__nvr, ycpz__wjw = _count_overlap(right_key_arrs[0], efwy__sdaci
            [mmu__mssuk], vph__uyi[mmu__mssuk])
        if biw__nvr != 0:
            biw__nvr -= 1
            ycpz__wjw += 1
        hapug__gwa[mmu__mssuk] = ycpz__wjw
        jmed__wgtu[mmu__mssuk] = biw__nvr
        mmu__mssuk += 1
    while mmu__mssuk < gxznu__hukok:
        hapug__gwa[mmu__mssuk] = 1
        jmed__wgtu[mmu__mssuk] = len(right_key_arrs[0]) - 1
        mmu__mssuk += 1
    bodo.libs.distributed_api.alltoall(hapug__gwa, xpepa__dewlo, 1)
    spu__uukw = xpepa__dewlo.sum()
    clrx__vnpmn = np.empty(spu__uukw, right_key_arrs[0].dtype)
    efk__ubl = alloc_arr_tup(spu__uukw, right_data)
    ylcb__kdtb = bodo.ir.join.calc_disp(xpepa__dewlo)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], clrx__vnpmn,
        hapug__gwa, xpepa__dewlo, jmed__wgtu, ylcb__kdtb)
    bodo.libs.distributed_api.alltoallv_tup(right_data, efk__ubl,
        hapug__gwa, xpepa__dewlo, jmed__wgtu, ylcb__kdtb)
    return (clrx__vnpmn,), efk__ubl


@numba.njit
def _count_overlap(r_key_arr, start, end):
    ycpz__wjw = 0
    biw__nvr = 0
    pzly__koryq = 0
    while pzly__koryq < len(r_key_arr) and r_key_arr[pzly__koryq] < start:
        biw__nvr += 1
        pzly__koryq += 1
    while pzly__koryq < len(r_key_arr) and start <= r_key_arr[pzly__koryq
        ] <= end:
        pzly__koryq += 1
        ycpz__wjw += 1
    return biw__nvr, ycpz__wjw


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    lllq__nlunc = np.empty_like(arr)
    lllq__nlunc[0] = 0
    for mmu__mssuk in range(1, len(arr)):
        lllq__nlunc[mmu__mssuk] = lllq__nlunc[mmu__mssuk - 1] + arr[
            mmu__mssuk - 1]
    return lllq__nlunc


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    uahp__pvoul = len(left_keys[0])
    ysfs__oyo = len(right_keys[0])
    hcxn__rkz = alloc_arr_tup(uahp__pvoul, left_keys)
    icnw__oiw = alloc_arr_tup(uahp__pvoul, right_keys)
    lvge__pjs = alloc_arr_tup(uahp__pvoul, data_left)
    vvyt__tqdxz = alloc_arr_tup(uahp__pvoul, data_right)
    zaciy__orefs = 0
    qxz__wsaau = 0
    for zaciy__orefs in range(uahp__pvoul):
        if qxz__wsaau < 0:
            qxz__wsaau = 0
        while qxz__wsaau < ysfs__oyo and getitem_arr_tup(right_keys, qxz__wsaau
            ) <= getitem_arr_tup(left_keys, zaciy__orefs):
            qxz__wsaau += 1
        qxz__wsaau -= 1
        setitem_arr_tup(hcxn__rkz, zaciy__orefs, getitem_arr_tup(left_keys,
            zaciy__orefs))
        setitem_arr_tup(lvge__pjs, zaciy__orefs, getitem_arr_tup(data_left,
            zaciy__orefs))
        if qxz__wsaau >= 0:
            setitem_arr_tup(icnw__oiw, zaciy__orefs, getitem_arr_tup(
                right_keys, qxz__wsaau))
            setitem_arr_tup(vvyt__tqdxz, zaciy__orefs, getitem_arr_tup(
                data_right, qxz__wsaau))
        else:
            bodo.libs.array_kernels.setna_tup(icnw__oiw, zaciy__orefs)
            bodo.libs.array_kernels.setna_tup(vvyt__tqdxz, zaciy__orefs)
    return hcxn__rkz, icnw__oiw, lvge__pjs, vvyt__tqdxz
