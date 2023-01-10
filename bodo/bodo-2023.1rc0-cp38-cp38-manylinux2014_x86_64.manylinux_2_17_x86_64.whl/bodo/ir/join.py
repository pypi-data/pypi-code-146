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
        bybau__jdf = func.signature
        kdul__axgh = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        xgl__moq = cgutils.get_or_insert_function(builder.module,
            kdul__axgh, sym._literal_value)
        builder.call(xgl__moq, [context.get_constant_null(bybau__jdf.args[0
            ]), context.get_constant_null(bybau__jdf.args[1]), context.
            get_constant_null(bybau__jdf.args[2]), context.
            get_constant_null(bybau__jdf.args[3]), context.
            get_constant_null(bybau__jdf.args[4]), context.
            get_constant_null(bybau__jdf.args[5]), context.get_constant(
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
        mmhy__sfco = left_df_type.columns
        irra__vdv = right_df_type.columns
        self.left_col_names = mmhy__sfco
        self.right_col_names = irra__vdv
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(mmhy__sfco) if self.is_left_table else 0
        self.n_right_table_cols = len(irra__vdv) if self.is_right_table else 0
        dvgab__ync = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        ygl__pjvu = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(dvgab__ync)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(ygl__pjvu)
        self.left_var_map = {pgy__nhbla: yiqe__opj for yiqe__opj,
            pgy__nhbla in enumerate(mmhy__sfco)}
        self.right_var_map = {pgy__nhbla: yiqe__opj for yiqe__opj,
            pgy__nhbla in enumerate(irra__vdv)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = dvgab__ync
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = ygl__pjvu
        self.left_key_set = set(self.left_var_map[pgy__nhbla] for
            pgy__nhbla in left_keys)
        self.right_key_set = set(self.right_var_map[pgy__nhbla] for
            pgy__nhbla in right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[pgy__nhbla] for
                pgy__nhbla in mmhy__sfco if f'(left.{pgy__nhbla})' in
                gen_cond_expr)
            self.right_cond_cols = set(self.right_var_map[pgy__nhbla] for
                pgy__nhbla in irra__vdv if f'(right.{pgy__nhbla})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        povy__tckqt: int = -1
        vzvgc__maq = set(left_keys) & set(right_keys)
        rhyc__wht = set(mmhy__sfco) & set(irra__vdv)
        kyxfo__yxv = rhyc__wht - vzvgc__maq
        wmsnp__qhsq: Dict[int, (Literal['left', 'right'], int)] = {}
        oygd__drnx: Dict[int, int] = {}
        lyp__fjq: Dict[int, int] = {}
        for yiqe__opj, pgy__nhbla in enumerate(mmhy__sfco):
            if pgy__nhbla in kyxfo__yxv:
                chcbs__nie = str(pgy__nhbla) + suffix_left
                cvati__ikhsb = out_df_type.column_index[chcbs__nie]
                if (right_index and not left_index and yiqe__opj in self.
                    left_key_set):
                    povy__tckqt = out_df_type.column_index[pgy__nhbla]
                    wmsnp__qhsq[povy__tckqt] = 'left', yiqe__opj
            else:
                cvati__ikhsb = out_df_type.column_index[pgy__nhbla]
            wmsnp__qhsq[cvati__ikhsb] = 'left', yiqe__opj
            oygd__drnx[yiqe__opj] = cvati__ikhsb
        for yiqe__opj, pgy__nhbla in enumerate(irra__vdv):
            if pgy__nhbla not in vzvgc__maq:
                if pgy__nhbla in kyxfo__yxv:
                    jtsq__obju = str(pgy__nhbla) + suffix_right
                    cvati__ikhsb = out_df_type.column_index[jtsq__obju]
                    if (left_index and not right_index and yiqe__opj in
                        self.right_key_set):
                        povy__tckqt = out_df_type.column_index[pgy__nhbla]
                        wmsnp__qhsq[povy__tckqt] = 'right', yiqe__opj
                else:
                    cvati__ikhsb = out_df_type.column_index[pgy__nhbla]
                wmsnp__qhsq[cvati__ikhsb] = 'right', yiqe__opj
                lyp__fjq[yiqe__opj] = cvati__ikhsb
        if self.left_vars[-1] is not None:
            oygd__drnx[dvgab__ync] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            lyp__fjq[ygl__pjvu] = self.n_out_table_cols
        self.out_to_input_col_map = wmsnp__qhsq
        self.left_to_output_map = oygd__drnx
        self.right_to_output_map = lyp__fjq
        self.extra_data_col_num = povy__tckqt
        if self.out_data_vars[1] is not None:
            rwptn__gstzg = 'left' if right_index else 'right'
            if rwptn__gstzg == 'left':
                ptbl__cmg = dvgab__ync
            elif rwptn__gstzg == 'right':
                ptbl__cmg = ygl__pjvu
        else:
            rwptn__gstzg = None
            ptbl__cmg = -1
        self.index_source = rwptn__gstzg
        self.index_col_num = ptbl__cmg
        dla__quok = []
        hee__ofa = len(left_keys)
        for tkd__dkljg in range(hee__ofa):
            eulrg__eydn = left_keys[tkd__dkljg]
            saga__qteo = right_keys[tkd__dkljg]
            dla__quok.append(eulrg__eydn == saga__qteo)
        self.vect_same_key = dla__quok

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
        for tcpq__qdds in self.left_vars:
            if tcpq__qdds is not None:
                vars.append(tcpq__qdds)
        return vars

    def get_live_right_vars(self):
        vars = []
        for tcpq__qdds in self.right_vars:
            if tcpq__qdds is not None:
                vars.append(tcpq__qdds)
        return vars

    def get_live_out_vars(self):
        vars = []
        for tcpq__qdds in self.out_data_vars:
            if tcpq__qdds is not None:
                vars.append(tcpq__qdds)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        pjmy__ytx = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[pjmy__ytx])
                pjmy__ytx += 1
            else:
                left_vars.append(None)
            start = 1
        syaxr__jwvbz = max(self.n_left_table_cols - 1, 0)
        for yiqe__opj in range(start, len(self.left_vars)):
            if yiqe__opj + syaxr__jwvbz in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[pjmy__ytx])
                pjmy__ytx += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        pjmy__ytx = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[pjmy__ytx])
                pjmy__ytx += 1
            else:
                right_vars.append(None)
            start = 1
        syaxr__jwvbz = max(self.n_right_table_cols - 1, 0)
        for yiqe__opj in range(start, len(self.right_vars)):
            if yiqe__opj + syaxr__jwvbz in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[pjmy__ytx])
                pjmy__ytx += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        nax__miesj = [self.has_live_out_table_var, self.has_live_out_index_var]
        pjmy__ytx = 0
        for yiqe__opj in range(len(self.out_data_vars)):
            if not nax__miesj[yiqe__opj]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[pjmy__ytx])
                pjmy__ytx += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {yiqe__opj for yiqe__opj in self.out_used_cols if yiqe__opj <
            self.n_out_table_cols}

    def __repr__(self):
        vzpyc__pdr = ', '.join([f'{pgy__nhbla}' for pgy__nhbla in self.
            left_col_names])
        gopb__kwfo = f'left={{{vzpyc__pdr}}}'
        vzpyc__pdr = ', '.join([f'{pgy__nhbla}' for pgy__nhbla in self.
            right_col_names])
        syc__vpn = f'right={{{vzpyc__pdr}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, gopb__kwfo, syc__vpn)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    scbom__ocfeo = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    gosqh__jka = []
    ngam__ypblm = join_node.get_live_left_vars()
    for vrwfs__rvy in ngam__ypblm:
        sgu__wcf = typemap[vrwfs__rvy.name]
        echm__kjm = equiv_set.get_shape(vrwfs__rvy)
        if echm__kjm:
            gosqh__jka.append(echm__kjm[0])
    if len(gosqh__jka) > 1:
        equiv_set.insert_equiv(*gosqh__jka)
    gosqh__jka = []
    ngam__ypblm = list(join_node.get_live_right_vars())
    for vrwfs__rvy in ngam__ypblm:
        sgu__wcf = typemap[vrwfs__rvy.name]
        echm__kjm = equiv_set.get_shape(vrwfs__rvy)
        if echm__kjm:
            gosqh__jka.append(echm__kjm[0])
    if len(gosqh__jka) > 1:
        equiv_set.insert_equiv(*gosqh__jka)
    gosqh__jka = []
    for qea__ymoog in join_node.get_live_out_vars():
        sgu__wcf = typemap[qea__ymoog.name]
        roeo__gzk = array_analysis._gen_shape_call(equiv_set, qea__ymoog,
            sgu__wcf.ndim, None, scbom__ocfeo)
        equiv_set.insert_equiv(qea__ymoog, roeo__gzk)
        gosqh__jka.append(roeo__gzk[0])
        equiv_set.define(qea__ymoog, set())
    if len(gosqh__jka) > 1:
        equiv_set.insert_equiv(*gosqh__jka)
    return [], scbom__ocfeo


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    znfj__hkryb = Distribution.OneD
    zoiyv__qim = Distribution.OneD
    for vrwfs__rvy in join_node.get_live_left_vars():
        znfj__hkryb = Distribution(min(znfj__hkryb.value, array_dists[
            vrwfs__rvy.name].value))
    for vrwfs__rvy in join_node.get_live_right_vars():
        zoiyv__qim = Distribution(min(zoiyv__qim.value, array_dists[
            vrwfs__rvy.name].value))
    ygihl__efki = Distribution.OneD_Var
    for qea__ymoog in join_node.get_live_out_vars():
        if qea__ymoog.name in array_dists:
            ygihl__efki = Distribution(min(ygihl__efki.value, array_dists[
                qea__ymoog.name].value))
    anqei__hau = Distribution(min(ygihl__efki.value, znfj__hkryb.value))
    itom__smc = Distribution(min(ygihl__efki.value, zoiyv__qim.value))
    ygihl__efki = Distribution(max(anqei__hau.value, itom__smc.value))
    for qea__ymoog in join_node.get_live_out_vars():
        array_dists[qea__ymoog.name] = ygihl__efki
    if ygihl__efki != Distribution.OneD_Var:
        znfj__hkryb = ygihl__efki
        zoiyv__qim = ygihl__efki
    for vrwfs__rvy in join_node.get_live_left_vars():
        array_dists[vrwfs__rvy.name] = znfj__hkryb
    for vrwfs__rvy in join_node.get_live_right_vars():
        array_dists[vrwfs__rvy.name] = zoiyv__qim
    join_node.left_dist = znfj__hkryb
    join_node.right_dist = zoiyv__qim


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(tcpq__qdds, callback,
        cbdata) for tcpq__qdds in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(tcpq__qdds, callback,
        cbdata) for tcpq__qdds in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(tcpq__qdds, callback,
        cbdata) for tcpq__qdds in join_node.get_live_out_vars()])
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
        gxfbb__vtn = []
        doi__lclmw = join_node.get_out_table_var()
        if doi__lclmw.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for vvo__mfqga in join_node.out_to_input_col_map.keys():
            if vvo__mfqga in join_node.out_used_cols:
                continue
            gxfbb__vtn.append(vvo__mfqga)
            if join_node.indicator_col_num == vvo__mfqga:
                join_node.indicator_col_num = -1
                continue
            if vvo__mfqga == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            ubn__miez, vvo__mfqga = join_node.out_to_input_col_map[vvo__mfqga]
            if ubn__miez == 'left':
                if (vvo__mfqga not in join_node.left_key_set and vvo__mfqga
                     not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(vvo__mfqga)
                    if not join_node.is_left_table:
                        join_node.left_vars[vvo__mfqga] = None
            elif ubn__miez == 'right':
                if (vvo__mfqga not in join_node.right_key_set and 
                    vvo__mfqga not in join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(vvo__mfqga)
                    if not join_node.is_right_table:
                        join_node.right_vars[vvo__mfqga] = None
        for yiqe__opj in gxfbb__vtn:
            del join_node.out_to_input_col_map[yiqe__opj]
        if join_node.is_left_table:
            hbv__dbyu = set(range(join_node.n_left_table_cols))
            rqyj__ftn = not bool(hbv__dbyu - join_node.left_dead_var_inds)
            if rqyj__ftn:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            hbv__dbyu = set(range(join_node.n_right_table_cols))
            rqyj__ftn = not bool(hbv__dbyu - join_node.right_dead_var_inds)
            if rqyj__ftn:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        zale__frlg = join_node.get_out_index_var()
        if zale__frlg.name not in lives:
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
    kjbom__nfqof = False
    if join_node.has_live_out_table_var:
        gbb__jao = join_node.get_out_table_var().name
        cac__utbxl, xld__arssy, ziouz__xxe = get_live_column_nums_block(
            column_live_map, equiv_vars, gbb__jao)
        if not (xld__arssy or ziouz__xxe):
            cac__utbxl = trim_extra_used_columns(cac__utbxl, join_node.
                n_out_table_cols)
            okw__zyguo = join_node.get_out_table_used_cols()
            if len(cac__utbxl) != len(okw__zyguo):
                kjbom__nfqof = not (join_node.is_left_table and join_node.
                    is_right_table)
                asq__woyfj = okw__zyguo - cac__utbxl
                join_node.out_used_cols = join_node.out_used_cols - asq__woyfj
    return kjbom__nfqof


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        pnfso__slbp = join_node.get_out_table_var()
        qwxqz__hmyfa, xld__arssy, ziouz__xxe = _compute_table_column_uses(
            pnfso__slbp.name, table_col_use_map, equiv_vars)
    else:
        qwxqz__hmyfa, xld__arssy, ziouz__xxe = set(), False, False
    if join_node.has_live_left_table_var:
        fgz__zsokx = join_node.left_vars[0].name
        lbxnm__jdy, ilsnd__rnx, vtg__ejgpo = block_use_map[fgz__zsokx]
        if not (ilsnd__rnx or vtg__ejgpo):
            zmske__wodvd = set([join_node.out_to_input_col_map[yiqe__opj][1
                ] for yiqe__opj in qwxqz__hmyfa if join_node.
                out_to_input_col_map[yiqe__opj][0] == 'left'])
            axsn__vpk = set(yiqe__opj for yiqe__opj in join_node.
                left_key_set | join_node.left_cond_cols if yiqe__opj <
                join_node.n_left_table_cols)
            if not (xld__arssy or ziouz__xxe):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (zmske__wodvd | axsn__vpk)
            block_use_map[fgz__zsokx] = (lbxnm__jdy | zmske__wodvd |
                axsn__vpk, xld__arssy or ziouz__xxe, False)
    if join_node.has_live_right_table_var:
        gga__phyia = join_node.right_vars[0].name
        lbxnm__jdy, ilsnd__rnx, vtg__ejgpo = block_use_map[gga__phyia]
        if not (ilsnd__rnx or vtg__ejgpo):
            mqto__hyijf = set([join_node.out_to_input_col_map[yiqe__opj][1] for
                yiqe__opj in qwxqz__hmyfa if join_node.out_to_input_col_map
                [yiqe__opj][0] == 'right'])
            tti__wiy = set(yiqe__opj for yiqe__opj in join_node.
                right_key_set | join_node.right_cond_cols if yiqe__opj <
                join_node.n_right_table_cols)
            if not (xld__arssy or ziouz__xxe):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (mqto__hyijf | tti__wiy)
            block_use_map[gga__phyia] = (lbxnm__jdy | mqto__hyijf |
                tti__wiy, xld__arssy or ziouz__xxe, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({czzr__kmd.name for czzr__kmd in join_node.
        get_live_left_vars()})
    use_set.update({czzr__kmd.name for czzr__kmd in join_node.
        get_live_right_vars()})
    def_set.update({czzr__kmd.name for czzr__kmd in join_node.
        get_live_out_vars()})
    if join_node.how == 'cross':
        use_set.add(join_node.left_len_var.name)
        use_set.add(join_node.right_len_var.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    isl__yfewc = set(czzr__kmd.name for czzr__kmd in join_node.
        get_live_out_vars())
    return set(), isl__yfewc


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(tcpq__qdds, var_dict) for
        tcpq__qdds in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(tcpq__qdds, var_dict) for
        tcpq__qdds in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(tcpq__qdds,
        var_dict) for tcpq__qdds in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = replace_vars_inner(join_node.left_len_var,
            var_dict)
        join_node.right_len_var = replace_vars_inner(join_node.
            right_len_var, var_dict)


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for vrwfs__rvy in join_node.get_live_out_vars():
        definitions[vrwfs__rvy.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def _gen_cross_join_len(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel):
    func_text = 'def f(left_len, right_len):\n'
    bxhx__bpa = 'bodo.libs.distributed_api.get_size()'
    pfv__hoqvl = 'bodo.libs.distributed_api.get_rank()'
    if left_parallel:
        func_text += f"""  left_len = bodo.libs.distributed_api.get_node_portion(left_len, {bxhx__bpa}, {pfv__hoqvl})
"""
    if right_parallel and not left_parallel:
        func_text += f"""  right_len = bodo.libs.distributed_api.get_node_portion(right_len, {bxhx__bpa}, {pfv__hoqvl})
"""
    func_text += '  n_rows = left_len * right_len\n'
    func_text += '  py_table = init_table(py_table_type, False)\n'
    func_text += '  py_table = set_table_len(py_table, n_rows)\n'
    darz__apib = {}
    exec(func_text, {}, darz__apib)
    poed__jiv = darz__apib['f']
    glbs = {'py_table_type': out_table_type, 'init_table': bodo.hiframes.
        table.init_table, 'set_table_len': bodo.hiframes.table.
        set_table_len, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value), 'bodo': bodo}
    euce__rzbjt = [join_node.left_len_var, join_node.right_len_var]
    pcrl__hdl = tuple(typemap[czzr__kmd.name] for czzr__kmd in euce__rzbjt)
    avafd__rldv = compile_to_numba_ir(poed__jiv, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=pcrl__hdl, typemap=typemap, calltypes
        =calltypes).blocks.popitem()[1]
    replace_arg_nodes(avafd__rldv, euce__rzbjt)
    rhyc__xwfuh = avafd__rldv.body[:-3]
    rhyc__xwfuh[-1].target = join_node.out_data_vars[0]
    return rhyc__xwfuh


def _gen_cross_join_repeat(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel, left_is_dead):
    ngam__ypblm = join_node.right_vars if left_is_dead else join_node.left_vars
    vbbmz__ozej = ', '.join(f't{yiqe__opj}' for yiqe__opj in range(len(
        ngam__ypblm)) if ngam__ypblm[yiqe__opj] is not None)
    pfpeo__ptoe = len(join_node.right_col_names) if left_is_dead else len(
        join_node.left_col_names)
    uxb__rpva = (join_node.is_right_table if left_is_dead else join_node.
        is_left_table)
    ngetr__dnaqs = (join_node.right_dead_var_inds if left_is_dead else
        join_node.left_dead_var_inds)
    ygkpc__pmuoz = [(f'get_table_data(t0, {yiqe__opj})' if uxb__rpva else
        f't{yiqe__opj}') for yiqe__opj in range(pfpeo__ptoe)]
    sbxih__ompiy = ', '.join(
        f'bodo.libs.array_kernels.repeat_kernel({ygkpc__pmuoz[yiqe__opj]}, repeats)'
         if yiqe__opj not in ngetr__dnaqs else 'None' for yiqe__opj in
        range(pfpeo__ptoe))
    qyxao__otvrh = len(out_table_type.arr_types)
    zfe__vlj = [join_node.out_to_input_col_map.get(yiqe__opj, (-1, -1))[1] for
        yiqe__opj in range(qyxao__otvrh)]
    bxhx__bpa = 'bodo.libs.distributed_api.get_size()'
    pfv__hoqvl = 'bodo.libs.distributed_api.get_rank()'
    hkrb__bbuy = 'left_len' if left_is_dead else 'right_len'
    aee__bydh = right_parallel if left_is_dead else left_parallel
    hrjc__dwnd = left_parallel if left_is_dead else right_parallel
    kqga__ycb = not aee__bydh and hrjc__dwnd
    xzht__ditb = (
        f'bodo.libs.distributed_api.get_node_portion({hkrb__bbuy}, {bxhx__bpa}, {pfv__hoqvl})'
         if kqga__ycb else hkrb__bbuy)
    func_text = f'def f({vbbmz__ozej}, left_len, right_len):\n'
    func_text += f'  repeats = {xzht__ditb}\n'
    func_text += f'  out_data = ({sbxih__ompiy},)\n'
    func_text += f"""  py_table = logical_table_to_table(out_data, (), col_inds, {pfpeo__ptoe}, out_table_type, used_cols)
"""
    darz__apib = {}
    exec(func_text, {}, darz__apib)
    poed__jiv = darz__apib['f']
    glbs = {'out_table_type': out_table_type, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value), 'bodo': bodo, 'used_cols':
        bodo.utils.typing.MetaType(tuple(join_node.out_used_cols)),
        'col_inds': bodo.utils.typing.MetaType(tuple(zfe__vlj)),
        'logical_table_to_table': bodo.hiframes.table.
        logical_table_to_table, 'get_table_data': bodo.hiframes.table.
        get_table_data}
    euce__rzbjt = [czzr__kmd for czzr__kmd in ngam__ypblm if czzr__kmd is not
        None] + [join_node.left_len_var, join_node.right_len_var]
    pcrl__hdl = tuple(typemap[czzr__kmd.name] for czzr__kmd in euce__rzbjt)
    avafd__rldv = compile_to_numba_ir(poed__jiv, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=pcrl__hdl, typemap=typemap, calltypes
        =calltypes).blocks.popitem()[1]
    replace_arg_nodes(avafd__rldv, euce__rzbjt)
    rhyc__xwfuh = avafd__rldv.body[:-3]
    rhyc__xwfuh[-1].target = join_node.out_data_vars[0]
    return rhyc__xwfuh


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        lagc__dwc = join_node.loc.strformat()
        zypx__sbeuc = [join_node.left_col_names[yiqe__opj] for yiqe__opj in
            sorted(set(range(len(join_node.left_col_names))) - join_node.
            left_dead_var_inds)]
        uikrb__dbm = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', uikrb__dbm,
            lagc__dwc, zypx__sbeuc)
        frq__vegyh = [join_node.right_col_names[yiqe__opj] for yiqe__opj in
            sorted(set(range(len(join_node.right_col_names))) - join_node.
            right_dead_var_inds)]
        uikrb__dbm = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', uikrb__dbm,
            lagc__dwc, frq__vegyh)
        ibxg__iucx = [join_node.out_col_names[yiqe__opj] for yiqe__opj in
            sorted(join_node.get_out_table_used_cols())]
        uikrb__dbm = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', uikrb__dbm,
            lagc__dwc, ibxg__iucx)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    hee__ofa = len(join_node.left_keys)
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
    elif join_node.how == 'cross' and all(yiqe__opj in join_node.
        left_dead_var_inds for yiqe__opj in range(len(join_node.
        left_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            True)
    elif join_node.how == 'cross' and all(yiqe__opj in join_node.
        right_dead_var_inds for yiqe__opj in range(len(join_node.
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
    mdg__iea = set()
    alol__lxmj = set()
    left_logical_physical_map = {}
    right_logical_physical_map = {}
    left_physical_to_logical_list = []
    right_physical_to_logical_list = []
    psbcq__scm = 0
    dkia__zcipe = 0
    vqj__nqk = []
    for kffw__nedw, pgy__nhbla in enumerate(join_node.left_keys):
        nadnt__wby = join_node.left_var_map[pgy__nhbla]
        if not join_node.is_left_table:
            vqj__nqk.append(join_node.left_vars[nadnt__wby])
        nax__miesj = 1
        cvati__ikhsb = join_node.left_to_output_map[nadnt__wby]
        if pgy__nhbla == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == nadnt__wby):
                out_physical_to_logical_list.append(cvati__ikhsb)
                left_used_key_nums.add(kffw__nedw)
                mdg__iea.add(nadnt__wby)
            else:
                nax__miesj = 0
        elif cvati__ikhsb not in join_node.out_used_cols:
            nax__miesj = 0
        elif nadnt__wby in mdg__iea:
            nax__miesj = 0
        else:
            left_used_key_nums.add(kffw__nedw)
            mdg__iea.add(nadnt__wby)
            out_physical_to_logical_list.append(cvati__ikhsb)
        left_physical_to_logical_list.append(nadnt__wby)
        left_logical_physical_map[nadnt__wby] = psbcq__scm
        psbcq__scm += 1
        left_key_in_output.append(nax__miesj)
    vqj__nqk = tuple(vqj__nqk)
    teos__kovy = []
    for yiqe__opj in range(len(join_node.left_col_names)):
        if (yiqe__opj not in join_node.left_dead_var_inds and yiqe__opj not in
            join_node.left_key_set):
            if not join_node.is_left_table:
                czzr__kmd = join_node.left_vars[yiqe__opj]
                teos__kovy.append(czzr__kmd)
            sekn__qgx = 1
            cwwgt__mjp = 1
            cvati__ikhsb = join_node.left_to_output_map[yiqe__opj]
            if yiqe__opj in join_node.left_cond_cols:
                if cvati__ikhsb not in join_node.out_used_cols:
                    sekn__qgx = 0
                left_key_in_output.append(sekn__qgx)
            elif yiqe__opj in join_node.left_dead_var_inds:
                sekn__qgx = 0
                cwwgt__mjp = 0
            if sekn__qgx:
                out_physical_to_logical_list.append(cvati__ikhsb)
            if cwwgt__mjp:
                left_physical_to_logical_list.append(yiqe__opj)
                left_logical_physical_map[yiqe__opj] = psbcq__scm
                psbcq__scm += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            teos__kovy.append(join_node.left_vars[join_node.index_col_num])
        cvati__ikhsb = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(cvati__ikhsb)
        left_physical_to_logical_list.append(join_node.index_col_num)
    teos__kovy = tuple(teos__kovy)
    if join_node.is_left_table:
        teos__kovy = tuple(join_node.get_live_left_vars())
    cipy__rpcjh = []
    for kffw__nedw, pgy__nhbla in enumerate(join_node.right_keys):
        nadnt__wby = join_node.right_var_map[pgy__nhbla]
        if not join_node.is_right_table:
            cipy__rpcjh.append(join_node.right_vars[nadnt__wby])
        if not join_node.vect_same_key[kffw__nedw] and not join_node.is_join:
            nax__miesj = 1
            if nadnt__wby not in join_node.right_to_output_map:
                nax__miesj = 0
            else:
                cvati__ikhsb = join_node.right_to_output_map[nadnt__wby]
                if pgy__nhbla == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        nadnt__wby):
                        out_physical_to_logical_list.append(cvati__ikhsb)
                        right_used_key_nums.add(kffw__nedw)
                        alol__lxmj.add(nadnt__wby)
                    else:
                        nax__miesj = 0
                elif cvati__ikhsb not in join_node.out_used_cols:
                    nax__miesj = 0
                elif nadnt__wby in alol__lxmj:
                    nax__miesj = 0
                else:
                    right_used_key_nums.add(kffw__nedw)
                    alol__lxmj.add(nadnt__wby)
                    out_physical_to_logical_list.append(cvati__ikhsb)
            right_key_in_output.append(nax__miesj)
        right_physical_to_logical_list.append(nadnt__wby)
        right_logical_physical_map[nadnt__wby] = dkia__zcipe
        dkia__zcipe += 1
    cipy__rpcjh = tuple(cipy__rpcjh)
    btpu__fio = []
    for yiqe__opj in range(len(join_node.right_col_names)):
        if (yiqe__opj not in join_node.right_dead_var_inds and yiqe__opj not in
            join_node.right_key_set):
            if not join_node.is_right_table:
                btpu__fio.append(join_node.right_vars[yiqe__opj])
            sekn__qgx = 1
            cwwgt__mjp = 1
            cvati__ikhsb = join_node.right_to_output_map[yiqe__opj]
            if yiqe__opj in join_node.right_cond_cols:
                if cvati__ikhsb not in join_node.out_used_cols:
                    sekn__qgx = 0
                right_key_in_output.append(sekn__qgx)
            elif yiqe__opj in join_node.right_dead_var_inds:
                sekn__qgx = 0
                cwwgt__mjp = 0
            if sekn__qgx:
                out_physical_to_logical_list.append(cvati__ikhsb)
            if cwwgt__mjp:
                right_physical_to_logical_list.append(yiqe__opj)
                right_logical_physical_map[yiqe__opj] = dkia__zcipe
                dkia__zcipe += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            btpu__fio.append(join_node.right_vars[join_node.index_col_num])
        cvati__ikhsb = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(cvati__ikhsb)
        right_physical_to_logical_list.append(join_node.index_col_num)
    btpu__fio = tuple(btpu__fio)
    if join_node.is_right_table:
        btpu__fio = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    euce__rzbjt = vqj__nqk + cipy__rpcjh + teos__kovy + btpu__fio
    pcrl__hdl = tuple(typemap[czzr__kmd.name] for czzr__kmd in euce__rzbjt)
    left_other_names = tuple('t1_c' + str(yiqe__opj) for yiqe__opj in range
        (len(teos__kovy)))
    right_other_names = tuple('t2_c' + str(yiqe__opj) for yiqe__opj in
        range(len(btpu__fio)))
    if join_node.is_left_table:
        suga__ojqye = ()
    else:
        suga__ojqye = tuple('t1_key' + str(yiqe__opj) for yiqe__opj in
            range(hee__ofa))
    if join_node.is_right_table:
        plxnb__mrge = ()
    else:
        plxnb__mrge = tuple('t2_key' + str(yiqe__opj) for yiqe__opj in
            range(hee__ofa))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(suga__ojqye + plxnb__mrge +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            lfkdv__rms = typemap[join_node.left_vars[0].name]
        else:
            lfkdv__rms = types.none
        for qjaf__yqfdx in left_physical_to_logical_list:
            if qjaf__yqfdx < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                sgu__wcf = lfkdv__rms.arr_types[qjaf__yqfdx]
            else:
                sgu__wcf = typemap[join_node.left_vars[-1].name]
            if qjaf__yqfdx in join_node.left_key_set:
                left_key_types.append(sgu__wcf)
            else:
                left_other_types.append(sgu__wcf)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[czzr__kmd.name] for czzr__kmd in
            vqj__nqk)
        left_other_types = tuple([typemap[pgy__nhbla.name] for pgy__nhbla in
            teos__kovy])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            lfkdv__rms = typemap[join_node.right_vars[0].name]
        else:
            lfkdv__rms = types.none
        for qjaf__yqfdx in right_physical_to_logical_list:
            if qjaf__yqfdx < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                sgu__wcf = lfkdv__rms.arr_types[qjaf__yqfdx]
            else:
                sgu__wcf = typemap[join_node.right_vars[-1].name]
            if qjaf__yqfdx in join_node.right_key_set:
                right_key_types.append(sgu__wcf)
            else:
                right_other_types.append(sgu__wcf)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[czzr__kmd.name] for czzr__kmd in
            cipy__rpcjh)
        right_other_types = tuple([typemap[pgy__nhbla.name] for pgy__nhbla in
            btpu__fio])
    matched_key_types = []
    for yiqe__opj in range(hee__ofa):
        ewlia__wwwv = _match_join_key_types(left_key_types[yiqe__opj],
            right_key_types[yiqe__opj], loc)
        glbs[f'key_type_{yiqe__opj}'] = ewlia__wwwv
        matched_key_types.append(ewlia__wwwv)
    if join_node.is_left_table:
        lze__kxu = determine_table_cast_map(matched_key_types,
            left_key_types, None, {yiqe__opj: join_node.left_var_map[
            maocm__iba] for yiqe__opj, maocm__iba in enumerate(join_node.
            left_keys)}, True)
        if lze__kxu:
            ntyy__oxkz = False
            rwnwj__hoct = False
            tpryg__skv = None
            if join_node.has_live_left_table_var:
                qqxd__hze = list(typemap[join_node.left_vars[0].name].arr_types
                    )
            else:
                qqxd__hze = None
            for vvo__mfqga, sgu__wcf in lze__kxu.items():
                if vvo__mfqga < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    qqxd__hze[vvo__mfqga] = sgu__wcf
                    ntyy__oxkz = True
                else:
                    tpryg__skv = sgu__wcf
                    rwnwj__hoct = True
            if ntyy__oxkz:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(qqxd__hze))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if rwnwj__hoct:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = tpryg__skv
    else:
        func_text += '    t1_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({suga__ojqye[yiqe__opj]}, key_type_{yiqe__opj})'
             if left_key_types[yiqe__opj] != matched_key_types[yiqe__opj] else
            f'{suga__ojqye[yiqe__opj]}' for yiqe__opj in range(hee__ofa)), 
            ',' if hee__ofa != 0 else '')
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        lze__kxu = determine_table_cast_map(matched_key_types,
            right_key_types, None, {yiqe__opj: join_node.right_var_map[
            maocm__iba] for yiqe__opj, maocm__iba in enumerate(join_node.
            right_keys)}, True)
        if lze__kxu:
            ntyy__oxkz = False
            rwnwj__hoct = False
            tpryg__skv = None
            if join_node.has_live_right_table_var:
                qqxd__hze = list(typemap[join_node.right_vars[0].name].
                    arr_types)
            else:
                qqxd__hze = None
            for vvo__mfqga, sgu__wcf in lze__kxu.items():
                if vvo__mfqga < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    qqxd__hze[vvo__mfqga] = sgu__wcf
                    ntyy__oxkz = True
                else:
                    tpryg__skv = sgu__wcf
                    rwnwj__hoct = True
            if ntyy__oxkz:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(qqxd__hze))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if rwnwj__hoct:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = tpryg__skv
    else:
        func_text += '    t2_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({plxnb__mrge[yiqe__opj]}, key_type_{yiqe__opj})'
             if right_key_types[yiqe__opj] != matched_key_types[yiqe__opj] else
            f'{plxnb__mrge[yiqe__opj]}' for yiqe__opj in range(hee__ofa)), 
            ',' if hee__ofa != 0 else '')
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
        for yiqe__opj in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(yiqe__opj,
                yiqe__opj)
        for yiqe__opj in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(yiqe__opj
                , yiqe__opj)
        for yiqe__opj in range(hee__ofa):
            func_text += (
                f'    t1_keys_{yiqe__opj} = out_t1_keys[{yiqe__opj}]\n')
        for yiqe__opj in range(hee__ofa):
            func_text += (
                f'    t2_keys_{yiqe__opj} = out_t2_keys[{yiqe__opj}]\n')
    darz__apib = {}
    exec(func_text, {}, darz__apib)
    poed__jiv = darz__apib['f']
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
    avafd__rldv = compile_to_numba_ir(poed__jiv, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=pcrl__hdl, typemap=typemap, calltypes
        =calltypes).blocks.popitem()[1]
    replace_arg_nodes(avafd__rldv, euce__rzbjt)
    rhyc__xwfuh = avafd__rldv.body[:-3]
    if join_node.has_live_out_index_var:
        rhyc__xwfuh[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        rhyc__xwfuh[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        rhyc__xwfuh.pop(-1)
    elif not join_node.has_live_out_table_var:
        rhyc__xwfuh.pop(-2)
    return rhyc__xwfuh


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    vqnlo__hpqq = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{vqnlo__hpqq}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
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
    darz__apib = {}
    exec(func_text, table_getitem_funcs, darz__apib)
    zua__cdht = darz__apib[f'bodo_join_gen_cond{vqnlo__hpqq}']
    jlzw__eiv = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    gxo__hzz = numba.cfunc(jlzw__eiv, nopython=True)(zua__cdht)
    join_gen_cond_cfunc[gxo__hzz.native_name] = gxo__hzz
    join_gen_cond_cfunc_addr[gxo__hzz.native_name] = gxo__hzz.address
    return gxo__hzz, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    kzui__jarrm = []
    for pgy__nhbla, midpl__cavi in name_to_var_map.items():
        scbcb__mrt = f'({table_name}.{pgy__nhbla})'
        if scbcb__mrt not in expr:
            continue
        yzbr__pec = f'getitem_{table_name}_val_{midpl__cavi}'
        if is_table_var:
            mehoz__ykk = typemap[col_vars[0].name].arr_types[midpl__cavi]
        else:
            mehoz__ykk = typemap[col_vars[midpl__cavi].name]
        if is_str_arr_type(mehoz__ykk) or mehoz__ykk == bodo.binary_array_type:
            ttmxn__sijhp = (
                f'{yzbr__pec}({table_name}_table, {table_name}_ind)\n')
        else:
            ttmxn__sijhp = (
                f'{yzbr__pec}({table_name}_data1, {table_name}_ind)\n')
        bpwq__jppp = logical_to_physical_ind[midpl__cavi]
        table_getitem_funcs[yzbr__pec
            ] = bodo.libs.array._gen_row_access_intrinsic(mehoz__ykk,
            bpwq__jppp)
        expr = expr.replace(scbcb__mrt, ttmxn__sijhp)
        qie__vfhma = f'({na_check_name}.{table_name}.{pgy__nhbla})'
        if qie__vfhma in expr:
            vxd__clytk = f'nacheck_{table_name}_val_{midpl__cavi}'
            tuh__dcmit = f'_bodo_isna_{table_name}_val_{midpl__cavi}'
            if isinstance(mehoz__ykk, (bodo.libs.int_arr_ext.
                IntegerArrayType, bodo.FloatingArrayType, bodo.TimeArrayType)
                ) or mehoz__ykk in (bodo.libs.bool_arr_ext.boolean_array,
                bodo.binary_array_type, bodo.datetime_date_array_type
                ) or is_str_arr_type(mehoz__ykk):
                func_text += f"""  {tuh__dcmit} = {vxd__clytk}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {tuh__dcmit} = {vxd__clytk}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[vxd__clytk
                ] = bodo.libs.array._gen_row_na_check_intrinsic(mehoz__ykk,
                bpwq__jppp)
            expr = expr.replace(qie__vfhma, tuh__dcmit)
        if midpl__cavi not in key_set:
            kzui__jarrm.append(bpwq__jppp)
    return expr, func_text, kzui__jarrm


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as sei__eog:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    pfvl__mxx = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[czzr__kmd.name] in pfvl__mxx for
        czzr__kmd in join_node.get_live_left_vars())
    if not join_node.get_live_left_vars():
        assert join_node.how == 'cross', 'cross join expected if left data is dead'
        left_parallel = join_node.left_dist in pfvl__mxx
    right_parallel = all(array_dists[czzr__kmd.name] in pfvl__mxx for
        czzr__kmd in join_node.get_live_right_vars())
    if not join_node.get_live_right_vars():
        assert join_node.how == 'cross', 'cross join expected if right data is dead'
        right_parallel = join_node.right_dist in pfvl__mxx
    if not left_parallel:
        assert not any(array_dists[czzr__kmd.name] in pfvl__mxx for
            czzr__kmd in join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[czzr__kmd.name] in pfvl__mxx for
            czzr__kmd in join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[czzr__kmd.name] in pfvl__mxx for czzr__kmd in
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
    lcqjf__vwup = set(left_col_nums)
    oqeuq__pbrn = set(right_col_nums)
    dla__quok = join_node.vect_same_key
    wnfk__ddpzx = []
    for yiqe__opj in range(len(left_key_types)):
        if left_key_in_output[yiqe__opj]:
            wnfk__ddpzx.append(needs_typechange(matched_key_types[yiqe__opj
                ], join_node.is_right, dla__quok[yiqe__opj]))
    caq__pdrq = len(left_key_types)
    ulyo__ltysi = 0
    bxpi__tfwtu = left_physical_to_logical_list[len(left_key_types):]
    for yiqe__opj, qjaf__yqfdx in enumerate(bxpi__tfwtu):
        ynm__lkyr = True
        if qjaf__yqfdx in lcqjf__vwup:
            ynm__lkyr = left_key_in_output[caq__pdrq]
            caq__pdrq += 1
        if ynm__lkyr:
            wnfk__ddpzx.append(needs_typechange(left_other_types[yiqe__opj],
                join_node.is_right, False))
    for yiqe__opj in range(len(right_key_types)):
        if not dla__quok[yiqe__opj] and not join_node.is_join:
            if right_key_in_output[ulyo__ltysi]:
                wnfk__ddpzx.append(needs_typechange(matched_key_types[
                    yiqe__opj], join_node.is_left, False))
            ulyo__ltysi += 1
    inheo__nnbsh = right_physical_to_logical_list[len(right_key_types):]
    for yiqe__opj, qjaf__yqfdx in enumerate(inheo__nnbsh):
        ynm__lkyr = True
        if qjaf__yqfdx in oqeuq__pbrn:
            ynm__lkyr = right_key_in_output[ulyo__ltysi]
            ulyo__ltysi += 1
        if ynm__lkyr:
            wnfk__ddpzx.append(needs_typechange(right_other_types[yiqe__opj
                ], join_node.is_left, False))
    hee__ofa = len(left_key_types)
    func_text = '    # beginning of _gen_join_cpp_call\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            day__ldan = left_other_names[1:]
            doi__lclmw = left_other_names[0]
        else:
            day__ldan = left_other_names
            doi__lclmw = None
        lyjtk__yuosh = '()' if len(day__ldan) == 0 else f'({day__ldan[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({doi__lclmw}, {lyjtk__yuosh}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        jxzh__uujqi = []
        for yiqe__opj in range(hee__ofa):
            jxzh__uujqi.append('t1_keys[{}]'.format(yiqe__opj))
        for yiqe__opj in range(len(left_other_names)):
            jxzh__uujqi.append('data_left[{}]'.format(yiqe__opj))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(zdr__jfmq) for zdr__jfmq in jxzh__uujqi)
            )
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            uytu__vjxu = right_other_names[1:]
            doi__lclmw = right_other_names[0]
        else:
            uytu__vjxu = right_other_names
            doi__lclmw = None
        lyjtk__yuosh = '()' if len(uytu__vjxu) == 0 else f'({uytu__vjxu[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({doi__lclmw}, {lyjtk__yuosh}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        etix__zma = []
        for yiqe__opj in range(hee__ofa):
            etix__zma.append('t2_keys[{}]'.format(yiqe__opj))
        for yiqe__opj in range(len(right_other_names)):
            etix__zma.append('data_right[{}]'.format(yiqe__opj))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(zdr__jfmq) for zdr__jfmq in etix__zma))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(dla__quok, dtype=np.int64)
    glbs['use_nullable_arr_type'] = np.array(wnfk__ddpzx, dtype=np.int64)
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
        func_text += f"""    out_table = hash_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {hee__ofa}, {len(bxpi__tfwtu)}, {len(inheo__nnbsh)}, vect_same_key.ctypes, key_in_output.ctypes, use_nullable_arr_type.ctypes, {join_node.is_left}, {join_node.is_right}, {join_node.is_join}, {join_node.extra_data_col_num != -1}, {join_node.indicator_col_num != -1}, {join_node.is_na_equal}, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    qyk__odlus = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {qyk__odlus}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        pjmy__ytx = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{pjmy__ytx}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        wjoen__oioqg = {}
        for yiqe__opj, maocm__iba in enumerate(join_node.left_keys):
            if yiqe__opj in left_used_key_nums:
                tbv__cinv = join_node.left_var_map[maocm__iba]
                wjoen__oioqg[yiqe__opj] = join_node.left_to_output_map[
                    tbv__cinv]
        lze__kxu = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, wjoen__oioqg, False)
        jjua__ganfe = {}
        for yiqe__opj, maocm__iba in enumerate(join_node.right_keys):
            if yiqe__opj in right_used_key_nums:
                tbv__cinv = join_node.right_var_map[maocm__iba]
                jjua__ganfe[yiqe__opj] = join_node.right_to_output_map[
                    tbv__cinv]
        lze__kxu.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, jjua__ganfe, False))
        ntyy__oxkz = False
        rwnwj__hoct = False
        if join_node.has_live_out_table_var:
            qqxd__hze = list(out_table_type.arr_types)
        else:
            qqxd__hze = None
        for vvo__mfqga, sgu__wcf in lze__kxu.items():
            if vvo__mfqga < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                qqxd__hze[vvo__mfqga] = sgu__wcf
                ntyy__oxkz = True
            else:
                tpryg__skv = sgu__wcf
                rwnwj__hoct = True
        if ntyy__oxkz:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            vsv__evjmk = bodo.TableType(tuple(qqxd__hze))
            glbs['py_table_type'] = vsv__evjmk
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if rwnwj__hoct:
            glbs['index_col_type'] = tpryg__skv
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
    lze__kxu: Dict[int, types.Type] = {}
    hee__ofa = len(matched_key_types)
    for yiqe__opj in range(hee__ofa):
        if used_key_nums is None or yiqe__opj in used_key_nums:
            if matched_key_types[yiqe__opj] != key_types[yiqe__opj] and (
                convert_dict_col or key_types[yiqe__opj] != bodo.
                dict_str_arr_type):
                pjmy__ytx = output_map[yiqe__opj]
                lze__kxu[pjmy__ytx] = matched_key_types[yiqe__opj]
    return lze__kxu


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    bxhx__bpa = bodo.libs.distributed_api.get_size()
    lktt__fnsg = np.empty(bxhx__bpa, left_key_arrs[0].dtype)
    aisv__kej = np.empty(bxhx__bpa, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(lktt__fnsg, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(aisv__kej, left_key_arrs[0][-1])
    crkpq__galpz = np.zeros(bxhx__bpa, np.int32)
    wsaby__reyo = np.zeros(bxhx__bpa, np.int32)
    cggxb__lipc = np.zeros(bxhx__bpa, np.int32)
    gzxh__dpsi = right_key_arrs[0][0]
    auj__sjgj = right_key_arrs[0][-1]
    syaxr__jwvbz = -1
    yiqe__opj = 0
    while yiqe__opj < bxhx__bpa - 1 and aisv__kej[yiqe__opj] < gzxh__dpsi:
        yiqe__opj += 1
    while yiqe__opj < bxhx__bpa and lktt__fnsg[yiqe__opj] <= auj__sjgj:
        syaxr__jwvbz, xjrk__bbe = _count_overlap(right_key_arrs[0],
            lktt__fnsg[yiqe__opj], aisv__kej[yiqe__opj])
        if syaxr__jwvbz != 0:
            syaxr__jwvbz -= 1
            xjrk__bbe += 1
        crkpq__galpz[yiqe__opj] = xjrk__bbe
        wsaby__reyo[yiqe__opj] = syaxr__jwvbz
        yiqe__opj += 1
    while yiqe__opj < bxhx__bpa:
        crkpq__galpz[yiqe__opj] = 1
        wsaby__reyo[yiqe__opj] = len(right_key_arrs[0]) - 1
        yiqe__opj += 1
    bodo.libs.distributed_api.alltoall(crkpq__galpz, cggxb__lipc, 1)
    weaco__nznw = cggxb__lipc.sum()
    pkbl__kzuqe = np.empty(weaco__nznw, right_key_arrs[0].dtype)
    roqvi__adfj = alloc_arr_tup(weaco__nznw, right_data)
    zbjqu__sie = bodo.ir.join.calc_disp(cggxb__lipc)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], pkbl__kzuqe,
        crkpq__galpz, cggxb__lipc, wsaby__reyo, zbjqu__sie)
    bodo.libs.distributed_api.alltoallv_tup(right_data, roqvi__adfj,
        crkpq__galpz, cggxb__lipc, wsaby__reyo, zbjqu__sie)
    return (pkbl__kzuqe,), roqvi__adfj


@numba.njit
def _count_overlap(r_key_arr, start, end):
    xjrk__bbe = 0
    syaxr__jwvbz = 0
    jarty__rrndq = 0
    while jarty__rrndq < len(r_key_arr) and r_key_arr[jarty__rrndq] < start:
        syaxr__jwvbz += 1
        jarty__rrndq += 1
    while jarty__rrndq < len(r_key_arr) and start <= r_key_arr[jarty__rrndq
        ] <= end:
        jarty__rrndq += 1
        xjrk__bbe += 1
    return syaxr__jwvbz, xjrk__bbe


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    ddjdw__uln = np.empty_like(arr)
    ddjdw__uln[0] = 0
    for yiqe__opj in range(1, len(arr)):
        ddjdw__uln[yiqe__opj] = ddjdw__uln[yiqe__opj - 1] + arr[yiqe__opj - 1]
    return ddjdw__uln


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    uncj__ilxg = len(left_keys[0])
    uym__moxc = len(right_keys[0])
    yzl__zgk = alloc_arr_tup(uncj__ilxg, left_keys)
    vjts__xhxh = alloc_arr_tup(uncj__ilxg, right_keys)
    eju__apyu = alloc_arr_tup(uncj__ilxg, data_left)
    lnu__lheh = alloc_arr_tup(uncj__ilxg, data_right)
    oox__amsdt = 0
    hhoel__lsetm = 0
    for oox__amsdt in range(uncj__ilxg):
        if hhoel__lsetm < 0:
            hhoel__lsetm = 0
        while hhoel__lsetm < uym__moxc and getitem_arr_tup(right_keys,
            hhoel__lsetm) <= getitem_arr_tup(left_keys, oox__amsdt):
            hhoel__lsetm += 1
        hhoel__lsetm -= 1
        setitem_arr_tup(yzl__zgk, oox__amsdt, getitem_arr_tup(left_keys,
            oox__amsdt))
        setitem_arr_tup(eju__apyu, oox__amsdt, getitem_arr_tup(data_left,
            oox__amsdt))
        if hhoel__lsetm >= 0:
            setitem_arr_tup(vjts__xhxh, oox__amsdt, getitem_arr_tup(
                right_keys, hhoel__lsetm))
            setitem_arr_tup(lnu__lheh, oox__amsdt, getitem_arr_tup(
                data_right, hhoel__lsetm))
        else:
            bodo.libs.array_kernels.setna_tup(vjts__xhxh, oox__amsdt)
            bodo.libs.array_kernels.setna_tup(lnu__lheh, oox__amsdt)
    return yzl__zgk, vjts__xhxh, eju__apyu, lnu__lheh
