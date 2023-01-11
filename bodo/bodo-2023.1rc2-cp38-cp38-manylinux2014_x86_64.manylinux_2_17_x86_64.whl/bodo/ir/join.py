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
        wwhkt__taw = func.signature
        ekn__ezdm = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        gfc__udv = cgutils.get_or_insert_function(builder.module, ekn__ezdm,
            sym._literal_value)
        builder.call(gfc__udv, [context.get_constant_null(wwhkt__taw.args[0
            ]), context.get_constant_null(wwhkt__taw.args[1]), context.
            get_constant_null(wwhkt__taw.args[2]), context.
            get_constant_null(wwhkt__taw.args[3]), context.
            get_constant_null(wwhkt__taw.args[4]), context.
            get_constant_null(wwhkt__taw.args[5]), context.get_constant(
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
        uvbw__hxtj = left_df_type.columns
        culfz__eaj = right_df_type.columns
        self.left_col_names = uvbw__hxtj
        self.right_col_names = culfz__eaj
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(uvbw__hxtj) if self.is_left_table else 0
        self.n_right_table_cols = len(culfz__eaj) if self.is_right_table else 0
        imci__sfll = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        ymcy__uiupe = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(imci__sfll)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(ymcy__uiupe)
        self.left_var_map = {pdp__sse: jeluu__jjnwl for jeluu__jjnwl,
            pdp__sse in enumerate(uvbw__hxtj)}
        self.right_var_map = {pdp__sse: jeluu__jjnwl for jeluu__jjnwl,
            pdp__sse in enumerate(culfz__eaj)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = imci__sfll
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = ymcy__uiupe
        self.left_key_set = set(self.left_var_map[pdp__sse] for pdp__sse in
            left_keys)
        self.right_key_set = set(self.right_var_map[pdp__sse] for pdp__sse in
            right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[pdp__sse] for
                pdp__sse in uvbw__hxtj if f'(left.{pdp__sse})' in gen_cond_expr
                )
            self.right_cond_cols = set(self.right_var_map[pdp__sse] for
                pdp__sse in culfz__eaj if f'(right.{pdp__sse})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        othfn__zwls: int = -1
        gjuf__ytx = set(left_keys) & set(right_keys)
        ibcxy__dmmfh = set(uvbw__hxtj) & set(culfz__eaj)
        ojafu__srfl = ibcxy__dmmfh - gjuf__ytx
        onb__jnr: Dict[int, (Literal['left', 'right'], int)] = {}
        sde__vztlj: Dict[int, int] = {}
        mmh__hhou: Dict[int, int] = {}
        for jeluu__jjnwl, pdp__sse in enumerate(uvbw__hxtj):
            if pdp__sse in ojafu__srfl:
                fsb__dyim = str(pdp__sse) + suffix_left
                eybft__vfe = out_df_type.column_index[fsb__dyim]
                if (right_index and not left_index and jeluu__jjnwl in self
                    .left_key_set):
                    othfn__zwls = out_df_type.column_index[pdp__sse]
                    onb__jnr[othfn__zwls] = 'left', jeluu__jjnwl
            else:
                eybft__vfe = out_df_type.column_index[pdp__sse]
            onb__jnr[eybft__vfe] = 'left', jeluu__jjnwl
            sde__vztlj[jeluu__jjnwl] = eybft__vfe
        for jeluu__jjnwl, pdp__sse in enumerate(culfz__eaj):
            if pdp__sse not in gjuf__ytx:
                if pdp__sse in ojafu__srfl:
                    hqncv__sadpi = str(pdp__sse) + suffix_right
                    eybft__vfe = out_df_type.column_index[hqncv__sadpi]
                    if (left_index and not right_index and jeluu__jjnwl in
                        self.right_key_set):
                        othfn__zwls = out_df_type.column_index[pdp__sse]
                        onb__jnr[othfn__zwls] = 'right', jeluu__jjnwl
                else:
                    eybft__vfe = out_df_type.column_index[pdp__sse]
                onb__jnr[eybft__vfe] = 'right', jeluu__jjnwl
                mmh__hhou[jeluu__jjnwl] = eybft__vfe
        if self.left_vars[-1] is not None:
            sde__vztlj[imci__sfll] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            mmh__hhou[ymcy__uiupe] = self.n_out_table_cols
        self.out_to_input_col_map = onb__jnr
        self.left_to_output_map = sde__vztlj
        self.right_to_output_map = mmh__hhou
        self.extra_data_col_num = othfn__zwls
        if self.out_data_vars[1] is not None:
            xobgg__nqvhf = 'left' if right_index else 'right'
            if xobgg__nqvhf == 'left':
                xgkia__tzzqz = imci__sfll
            elif xobgg__nqvhf == 'right':
                xgkia__tzzqz = ymcy__uiupe
        else:
            xobgg__nqvhf = None
            xgkia__tzzqz = -1
        self.index_source = xobgg__nqvhf
        self.index_col_num = xgkia__tzzqz
        wikbk__uuqk = []
        udv__cesh = len(left_keys)
        for lkr__nqm in range(udv__cesh):
            erga__zffdb = left_keys[lkr__nqm]
            bawv__jjznc = right_keys[lkr__nqm]
            wikbk__uuqk.append(erga__zffdb == bawv__jjznc)
        self.vect_same_key = wikbk__uuqk

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
        for ibdy__hxkgu in self.left_vars:
            if ibdy__hxkgu is not None:
                vars.append(ibdy__hxkgu)
        return vars

    def get_live_right_vars(self):
        vars = []
        for ibdy__hxkgu in self.right_vars:
            if ibdy__hxkgu is not None:
                vars.append(ibdy__hxkgu)
        return vars

    def get_live_out_vars(self):
        vars = []
        for ibdy__hxkgu in self.out_data_vars:
            if ibdy__hxkgu is not None:
                vars.append(ibdy__hxkgu)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        spfw__kdkh = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[spfw__kdkh])
                spfw__kdkh += 1
            else:
                left_vars.append(None)
            start = 1
        fqdv__nceo = max(self.n_left_table_cols - 1, 0)
        for jeluu__jjnwl in range(start, len(self.left_vars)):
            if jeluu__jjnwl + fqdv__nceo in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[spfw__kdkh])
                spfw__kdkh += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        spfw__kdkh = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[spfw__kdkh])
                spfw__kdkh += 1
            else:
                right_vars.append(None)
            start = 1
        fqdv__nceo = max(self.n_right_table_cols - 1, 0)
        for jeluu__jjnwl in range(start, len(self.right_vars)):
            if jeluu__jjnwl + fqdv__nceo in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[spfw__kdkh])
                spfw__kdkh += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        wxitz__dgh = [self.has_live_out_table_var, self.has_live_out_index_var]
        spfw__kdkh = 0
        for jeluu__jjnwl in range(len(self.out_data_vars)):
            if not wxitz__dgh[jeluu__jjnwl]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[spfw__kdkh])
                spfw__kdkh += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {jeluu__jjnwl for jeluu__jjnwl in self.out_used_cols if 
            jeluu__jjnwl < self.n_out_table_cols}

    def __repr__(self):
        hzg__npca = ', '.join([f'{pdp__sse}' for pdp__sse in self.
            left_col_names])
        svdf__cyzr = f'left={{{hzg__npca}}}'
        hzg__npca = ', '.join([f'{pdp__sse}' for pdp__sse in self.
            right_col_names])
        pfp__jsy = f'right={{{hzg__npca}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, svdf__cyzr, pfp__jsy)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    mhgcv__rjtn = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    ikgh__hsqc = []
    yrji__ctr = join_node.get_live_left_vars()
    for oxh__mno in yrji__ctr:
        nybm__edvi = typemap[oxh__mno.name]
        rtkvb__nzp = equiv_set.get_shape(oxh__mno)
        if rtkvb__nzp:
            ikgh__hsqc.append(rtkvb__nzp[0])
    if len(ikgh__hsqc) > 1:
        equiv_set.insert_equiv(*ikgh__hsqc)
    ikgh__hsqc = []
    yrji__ctr = list(join_node.get_live_right_vars())
    for oxh__mno in yrji__ctr:
        nybm__edvi = typemap[oxh__mno.name]
        rtkvb__nzp = equiv_set.get_shape(oxh__mno)
        if rtkvb__nzp:
            ikgh__hsqc.append(rtkvb__nzp[0])
    if len(ikgh__hsqc) > 1:
        equiv_set.insert_equiv(*ikgh__hsqc)
    ikgh__hsqc = []
    for lxdk__yluu in join_node.get_live_out_vars():
        nybm__edvi = typemap[lxdk__yluu.name]
        bmsys__hbw = array_analysis._gen_shape_call(equiv_set, lxdk__yluu,
            nybm__edvi.ndim, None, mhgcv__rjtn)
        equiv_set.insert_equiv(lxdk__yluu, bmsys__hbw)
        ikgh__hsqc.append(bmsys__hbw[0])
        equiv_set.define(lxdk__yluu, set())
    if len(ikgh__hsqc) > 1:
        equiv_set.insert_equiv(*ikgh__hsqc)
    return [], mhgcv__rjtn


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    rkzu__lioer = Distribution.OneD
    wjg__ieb = Distribution.OneD
    for oxh__mno in join_node.get_live_left_vars():
        rkzu__lioer = Distribution(min(rkzu__lioer.value, array_dists[
            oxh__mno.name].value))
    for oxh__mno in join_node.get_live_right_vars():
        wjg__ieb = Distribution(min(wjg__ieb.value, array_dists[oxh__mno.
            name].value))
    qrdjb__kigfz = Distribution.OneD_Var
    for lxdk__yluu in join_node.get_live_out_vars():
        if lxdk__yluu.name in array_dists:
            qrdjb__kigfz = Distribution(min(qrdjb__kigfz.value, array_dists
                [lxdk__yluu.name].value))
    anpu__gdxmh = Distribution(min(qrdjb__kigfz.value, rkzu__lioer.value))
    lpmn__rpo = Distribution(min(qrdjb__kigfz.value, wjg__ieb.value))
    qrdjb__kigfz = Distribution(max(anpu__gdxmh.value, lpmn__rpo.value))
    for lxdk__yluu in join_node.get_live_out_vars():
        array_dists[lxdk__yluu.name] = qrdjb__kigfz
    if qrdjb__kigfz != Distribution.OneD_Var:
        rkzu__lioer = qrdjb__kigfz
        wjg__ieb = qrdjb__kigfz
    for oxh__mno in join_node.get_live_left_vars():
        array_dists[oxh__mno.name] = rkzu__lioer
    for oxh__mno in join_node.get_live_right_vars():
        array_dists[oxh__mno.name] = wjg__ieb
    join_node.left_dist = rkzu__lioer
    join_node.right_dist = wjg__ieb


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(ibdy__hxkgu, callback,
        cbdata) for ibdy__hxkgu in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(ibdy__hxkgu, callback,
        cbdata) for ibdy__hxkgu in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(ibdy__hxkgu,
        callback, cbdata) for ibdy__hxkgu in join_node.get_live_out_vars()])
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
        pkygx__riwo = []
        nyfej__wiip = join_node.get_out_table_var()
        if nyfej__wiip.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for pvf__ytoyr in join_node.out_to_input_col_map.keys():
            if pvf__ytoyr in join_node.out_used_cols:
                continue
            pkygx__riwo.append(pvf__ytoyr)
            if join_node.indicator_col_num == pvf__ytoyr:
                join_node.indicator_col_num = -1
                continue
            if pvf__ytoyr == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            hqlez__jejxh, pvf__ytoyr = join_node.out_to_input_col_map[
                pvf__ytoyr]
            if hqlez__jejxh == 'left':
                if (pvf__ytoyr not in join_node.left_key_set and pvf__ytoyr
                     not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(pvf__ytoyr)
                    if not join_node.is_left_table:
                        join_node.left_vars[pvf__ytoyr] = None
            elif hqlez__jejxh == 'right':
                if (pvf__ytoyr not in join_node.right_key_set and 
                    pvf__ytoyr not in join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(pvf__ytoyr)
                    if not join_node.is_right_table:
                        join_node.right_vars[pvf__ytoyr] = None
        for jeluu__jjnwl in pkygx__riwo:
            del join_node.out_to_input_col_map[jeluu__jjnwl]
        if join_node.is_left_table:
            nnl__hso = set(range(join_node.n_left_table_cols))
            bsz__zfefc = not bool(nnl__hso - join_node.left_dead_var_inds)
            if bsz__zfefc:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            nnl__hso = set(range(join_node.n_right_table_cols))
            bsz__zfefc = not bool(nnl__hso - join_node.right_dead_var_inds)
            if bsz__zfefc:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        zdr__vjpl = join_node.get_out_index_var()
        if zdr__vjpl.name not in lives:
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
    lpm__jsrxj = False
    if join_node.has_live_out_table_var:
        lefh__ftob = join_node.get_out_table_var().name
        hdq__jqpio, ydie__upml, gbqgz__nsbo = get_live_column_nums_block(
            column_live_map, equiv_vars, lefh__ftob)
        if not (ydie__upml or gbqgz__nsbo):
            hdq__jqpio = trim_extra_used_columns(hdq__jqpio, join_node.
                n_out_table_cols)
            jos__hnzx = join_node.get_out_table_used_cols()
            if len(hdq__jqpio) != len(jos__hnzx):
                lpm__jsrxj = not (join_node.is_left_table and join_node.
                    is_right_table)
                ecnp__kfhb = jos__hnzx - hdq__jqpio
                join_node.out_used_cols = join_node.out_used_cols - ecnp__kfhb
    return lpm__jsrxj


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        wmjc__ppuq = join_node.get_out_table_var()
        vsmdo__ckct, ydie__upml, gbqgz__nsbo = _compute_table_column_uses(
            wmjc__ppuq.name, table_col_use_map, equiv_vars)
    else:
        vsmdo__ckct, ydie__upml, gbqgz__nsbo = set(), False, False
    if join_node.has_live_left_table_var:
        gxo__igpy = join_node.left_vars[0].name
        bjs__flc, cjz__rbhm, zrwlr__aidfq = block_use_map[gxo__igpy]
        if not (cjz__rbhm or zrwlr__aidfq):
            ohok__ukv = set([join_node.out_to_input_col_map[jeluu__jjnwl][1
                ] for jeluu__jjnwl in vsmdo__ckct if join_node.
                out_to_input_col_map[jeluu__jjnwl][0] == 'left'])
            rxa__ecnw = set(jeluu__jjnwl for jeluu__jjnwl in join_node.
                left_key_set | join_node.left_cond_cols if jeluu__jjnwl <
                join_node.n_left_table_cols)
            if not (ydie__upml or gbqgz__nsbo):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (ohok__ukv | rxa__ecnw)
            block_use_map[gxo__igpy] = (bjs__flc | ohok__ukv | rxa__ecnw, 
                ydie__upml or gbqgz__nsbo, False)
    if join_node.has_live_right_table_var:
        sqr__rnayr = join_node.right_vars[0].name
        bjs__flc, cjz__rbhm, zrwlr__aidfq = block_use_map[sqr__rnayr]
        if not (cjz__rbhm or zrwlr__aidfq):
            ufktj__kuajq = set([join_node.out_to_input_col_map[jeluu__jjnwl
                ][1] for jeluu__jjnwl in vsmdo__ckct if join_node.
                out_to_input_col_map[jeluu__jjnwl][0] == 'right'])
            sqnz__frb = set(jeluu__jjnwl for jeluu__jjnwl in join_node.
                right_key_set | join_node.right_cond_cols if jeluu__jjnwl <
                join_node.n_right_table_cols)
            if not (ydie__upml or gbqgz__nsbo):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (ufktj__kuajq | sqnz__frb)
            block_use_map[sqr__rnayr] = (bjs__flc | ufktj__kuajq |
                sqnz__frb, ydie__upml or gbqgz__nsbo, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({kezh__nlbya.name for kezh__nlbya in join_node.
        get_live_left_vars()})
    use_set.update({kezh__nlbya.name for kezh__nlbya in join_node.
        get_live_right_vars()})
    def_set.update({kezh__nlbya.name for kezh__nlbya in join_node.
        get_live_out_vars()})
    if join_node.how == 'cross':
        use_set.add(join_node.left_len_var.name)
        use_set.add(join_node.right_len_var.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    xsvei__cnhp = set(kezh__nlbya.name for kezh__nlbya in join_node.
        get_live_out_vars())
    return set(), xsvei__cnhp


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(ibdy__hxkgu, var_dict) for
        ibdy__hxkgu in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(ibdy__hxkgu, var_dict
        ) for ibdy__hxkgu in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(ibdy__hxkgu,
        var_dict) for ibdy__hxkgu in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = replace_vars_inner(join_node.left_len_var,
            var_dict)
        join_node.right_len_var = replace_vars_inner(join_node.
            right_len_var, var_dict)


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for oxh__mno in join_node.get_live_out_vars():
        definitions[oxh__mno.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def _gen_cross_join_len(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel):
    func_text = 'def f(left_len, right_len):\n'
    soryo__mplv = 'bodo.libs.distributed_api.get_size()'
    atcn__owhyf = 'bodo.libs.distributed_api.get_rank()'
    if left_parallel:
        func_text += f"""  left_len = bodo.libs.distributed_api.get_node_portion(left_len, {soryo__mplv}, {atcn__owhyf})
"""
    if right_parallel and not left_parallel:
        func_text += f"""  right_len = bodo.libs.distributed_api.get_node_portion(right_len, {soryo__mplv}, {atcn__owhyf})
"""
    func_text += '  n_rows = left_len * right_len\n'
    func_text += '  py_table = init_table(py_table_type, False)\n'
    func_text += '  py_table = set_table_len(py_table, n_rows)\n'
    jywix__whrqo = {}
    exec(func_text, {}, jywix__whrqo)
    zdui__udgd = jywix__whrqo['f']
    glbs = {'py_table_type': out_table_type, 'init_table': bodo.hiframes.
        table.init_table, 'set_table_len': bodo.hiframes.table.
        set_table_len, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value), 'bodo': bodo}
    oigl__cunjp = [join_node.left_len_var, join_node.right_len_var]
    zofoz__dhyr = tuple(typemap[kezh__nlbya.name] for kezh__nlbya in
        oigl__cunjp)
    doz__oxnzh = compile_to_numba_ir(zdui__udgd, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=zofoz__dhyr, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(doz__oxnzh, oigl__cunjp)
    sia__fixtz = doz__oxnzh.body[:-3]
    sia__fixtz[-1].target = join_node.out_data_vars[0]
    return sia__fixtz


def _gen_cross_join_repeat(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel, left_is_dead):
    yrji__ctr = join_node.right_vars if left_is_dead else join_node.left_vars
    uzev__cdnrs = ', '.join(f't{jeluu__jjnwl}' for jeluu__jjnwl in range(
        len(yrji__ctr)) if yrji__ctr[jeluu__jjnwl] is not None)
    hpicv__ggzuw = len(join_node.right_col_names) if left_is_dead else len(
        join_node.left_col_names)
    ufken__kebs = (join_node.is_right_table if left_is_dead else join_node.
        is_left_table)
    mvkw__uwxnx = (join_node.right_dead_var_inds if left_is_dead else
        join_node.left_dead_var_inds)
    punxh__lumrz = [(f'get_table_data(t0, {jeluu__jjnwl})' if ufken__kebs else
        f't{jeluu__jjnwl}') for jeluu__jjnwl in range(hpicv__ggzuw)]
    ksj__kqn = ', '.join(
        f'bodo.libs.array_kernels.repeat_kernel({punxh__lumrz[jeluu__jjnwl]}, repeats)'
         if jeluu__jjnwl not in mvkw__uwxnx else 'None' for jeluu__jjnwl in
        range(hpicv__ggzuw))
    utyms__mxpk = len(out_table_type.arr_types)
    lmp__ofkvp = [join_node.out_to_input_col_map.get(jeluu__jjnwl, (-1, -1)
        )[1] for jeluu__jjnwl in range(utyms__mxpk)]
    soryo__mplv = 'bodo.libs.distributed_api.get_size()'
    atcn__owhyf = 'bodo.libs.distributed_api.get_rank()'
    vlpp__klstq = 'left_len' if left_is_dead else 'right_len'
    qczwz__qxg = right_parallel if left_is_dead else left_parallel
    ofb__lol = left_parallel if left_is_dead else right_parallel
    fmpv__tkdn = not qczwz__qxg and ofb__lol
    coi__eyitu = (
        f'bodo.libs.distributed_api.get_node_portion({vlpp__klstq}, {soryo__mplv}, {atcn__owhyf})'
         if fmpv__tkdn else vlpp__klstq)
    func_text = f'def f({uzev__cdnrs}, left_len, right_len):\n'
    func_text += f'  repeats = {coi__eyitu}\n'
    func_text += f'  out_data = ({ksj__kqn},)\n'
    func_text += f"""  py_table = logical_table_to_table(out_data, (), col_inds, {hpicv__ggzuw}, out_table_type, used_cols)
"""
    jywix__whrqo = {}
    exec(func_text, {}, jywix__whrqo)
    zdui__udgd = jywix__whrqo['f']
    glbs = {'out_table_type': out_table_type, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value), 'bodo': bodo, 'used_cols':
        bodo.utils.typing.MetaType(tuple(join_node.out_used_cols)),
        'col_inds': bodo.utils.typing.MetaType(tuple(lmp__ofkvp)),
        'logical_table_to_table': bodo.hiframes.table.
        logical_table_to_table, 'get_table_data': bodo.hiframes.table.
        get_table_data}
    oigl__cunjp = [kezh__nlbya for kezh__nlbya in yrji__ctr if kezh__nlbya
         is not None] + [join_node.left_len_var, join_node.right_len_var]
    zofoz__dhyr = tuple(typemap[kezh__nlbya.name] for kezh__nlbya in
        oigl__cunjp)
    doz__oxnzh = compile_to_numba_ir(zdui__udgd, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=zofoz__dhyr, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(doz__oxnzh, oigl__cunjp)
    sia__fixtz = doz__oxnzh.body[:-3]
    sia__fixtz[-1].target = join_node.out_data_vars[0]
    return sia__fixtz


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        ogt__jspon = join_node.loc.strformat()
        rwjy__yzn = [join_node.left_col_names[jeluu__jjnwl] for
            jeluu__jjnwl in sorted(set(range(len(join_node.left_col_names))
            ) - join_node.left_dead_var_inds)]
        ikh__inudk = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', ikh__inudk,
            ogt__jspon, rwjy__yzn)
        fbb__yjwki = [join_node.right_col_names[jeluu__jjnwl] for
            jeluu__jjnwl in sorted(set(range(len(join_node.right_col_names)
            )) - join_node.right_dead_var_inds)]
        ikh__inudk = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', ikh__inudk,
            ogt__jspon, fbb__yjwki)
        wbnx__ncfkm = [join_node.out_col_names[jeluu__jjnwl] for
            jeluu__jjnwl in sorted(join_node.get_out_table_used_cols())]
        ikh__inudk = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', ikh__inudk,
            ogt__jspon, wbnx__ncfkm)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    udv__cesh = len(join_node.left_keys)
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
    elif join_node.how == 'cross' and all(jeluu__jjnwl in join_node.
        left_dead_var_inds for jeluu__jjnwl in range(len(join_node.
        left_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            True)
    elif join_node.how == 'cross' and all(jeluu__jjnwl in join_node.
        right_dead_var_inds for jeluu__jjnwl in range(len(join_node.
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
    usl__jblw = set()
    qfo__gnh = set()
    left_logical_physical_map = {}
    right_logical_physical_map = {}
    left_physical_to_logical_list = []
    right_physical_to_logical_list = []
    tbqlv__vdip = 0
    bllq__wshus = 0
    zoep__ggvqu = []
    for aez__mqm, pdp__sse in enumerate(join_node.left_keys):
        wywpb__nhldy = join_node.left_var_map[pdp__sse]
        if not join_node.is_left_table:
            zoep__ggvqu.append(join_node.left_vars[wywpb__nhldy])
        wxitz__dgh = 1
        eybft__vfe = join_node.left_to_output_map[wywpb__nhldy]
        if pdp__sse == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == wywpb__nhldy):
                out_physical_to_logical_list.append(eybft__vfe)
                left_used_key_nums.add(aez__mqm)
                usl__jblw.add(wywpb__nhldy)
            else:
                wxitz__dgh = 0
        elif eybft__vfe not in join_node.out_used_cols:
            wxitz__dgh = 0
        elif wywpb__nhldy in usl__jblw:
            wxitz__dgh = 0
        else:
            left_used_key_nums.add(aez__mqm)
            usl__jblw.add(wywpb__nhldy)
            out_physical_to_logical_list.append(eybft__vfe)
        left_physical_to_logical_list.append(wywpb__nhldy)
        left_logical_physical_map[wywpb__nhldy] = tbqlv__vdip
        tbqlv__vdip += 1
        left_key_in_output.append(wxitz__dgh)
    zoep__ggvqu = tuple(zoep__ggvqu)
    yvp__bad = []
    for jeluu__jjnwl in range(len(join_node.left_col_names)):
        if (jeluu__jjnwl not in join_node.left_dead_var_inds and 
            jeluu__jjnwl not in join_node.left_key_set):
            if not join_node.is_left_table:
                kezh__nlbya = join_node.left_vars[jeluu__jjnwl]
                yvp__bad.append(kezh__nlbya)
            aoa__myiw = 1
            zdc__vxch = 1
            eybft__vfe = join_node.left_to_output_map[jeluu__jjnwl]
            if jeluu__jjnwl in join_node.left_cond_cols:
                if eybft__vfe not in join_node.out_used_cols:
                    aoa__myiw = 0
                left_key_in_output.append(aoa__myiw)
            elif jeluu__jjnwl in join_node.left_dead_var_inds:
                aoa__myiw = 0
                zdc__vxch = 0
            if aoa__myiw:
                out_physical_to_logical_list.append(eybft__vfe)
            if zdc__vxch:
                left_physical_to_logical_list.append(jeluu__jjnwl)
                left_logical_physical_map[jeluu__jjnwl] = tbqlv__vdip
                tbqlv__vdip += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            yvp__bad.append(join_node.left_vars[join_node.index_col_num])
        eybft__vfe = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(eybft__vfe)
        left_physical_to_logical_list.append(join_node.index_col_num)
    yvp__bad = tuple(yvp__bad)
    if join_node.is_left_table:
        yvp__bad = tuple(join_node.get_live_left_vars())
    umi__scakv = []
    for aez__mqm, pdp__sse in enumerate(join_node.right_keys):
        wywpb__nhldy = join_node.right_var_map[pdp__sse]
        if not join_node.is_right_table:
            umi__scakv.append(join_node.right_vars[wywpb__nhldy])
        if not join_node.vect_same_key[aez__mqm] and not join_node.is_join:
            wxitz__dgh = 1
            if wywpb__nhldy not in join_node.right_to_output_map:
                wxitz__dgh = 0
            else:
                eybft__vfe = join_node.right_to_output_map[wywpb__nhldy]
                if pdp__sse == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        wywpb__nhldy):
                        out_physical_to_logical_list.append(eybft__vfe)
                        right_used_key_nums.add(aez__mqm)
                        qfo__gnh.add(wywpb__nhldy)
                    else:
                        wxitz__dgh = 0
                elif eybft__vfe not in join_node.out_used_cols:
                    wxitz__dgh = 0
                elif wywpb__nhldy in qfo__gnh:
                    wxitz__dgh = 0
                else:
                    right_used_key_nums.add(aez__mqm)
                    qfo__gnh.add(wywpb__nhldy)
                    out_physical_to_logical_list.append(eybft__vfe)
            right_key_in_output.append(wxitz__dgh)
        right_physical_to_logical_list.append(wywpb__nhldy)
        right_logical_physical_map[wywpb__nhldy] = bllq__wshus
        bllq__wshus += 1
    umi__scakv = tuple(umi__scakv)
    zssrj__bya = []
    for jeluu__jjnwl in range(len(join_node.right_col_names)):
        if (jeluu__jjnwl not in join_node.right_dead_var_inds and 
            jeluu__jjnwl not in join_node.right_key_set):
            if not join_node.is_right_table:
                zssrj__bya.append(join_node.right_vars[jeluu__jjnwl])
            aoa__myiw = 1
            zdc__vxch = 1
            eybft__vfe = join_node.right_to_output_map[jeluu__jjnwl]
            if jeluu__jjnwl in join_node.right_cond_cols:
                if eybft__vfe not in join_node.out_used_cols:
                    aoa__myiw = 0
                right_key_in_output.append(aoa__myiw)
            elif jeluu__jjnwl in join_node.right_dead_var_inds:
                aoa__myiw = 0
                zdc__vxch = 0
            if aoa__myiw:
                out_physical_to_logical_list.append(eybft__vfe)
            if zdc__vxch:
                right_physical_to_logical_list.append(jeluu__jjnwl)
                right_logical_physical_map[jeluu__jjnwl] = bllq__wshus
                bllq__wshus += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            zssrj__bya.append(join_node.right_vars[join_node.index_col_num])
        eybft__vfe = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(eybft__vfe)
        right_physical_to_logical_list.append(join_node.index_col_num)
    zssrj__bya = tuple(zssrj__bya)
    if join_node.is_right_table:
        zssrj__bya = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    oigl__cunjp = zoep__ggvqu + umi__scakv + yvp__bad + zssrj__bya
    zofoz__dhyr = tuple(typemap[kezh__nlbya.name] for kezh__nlbya in
        oigl__cunjp)
    left_other_names = tuple('t1_c' + str(jeluu__jjnwl) for jeluu__jjnwl in
        range(len(yvp__bad)))
    right_other_names = tuple('t2_c' + str(jeluu__jjnwl) for jeluu__jjnwl in
        range(len(zssrj__bya)))
    if join_node.is_left_table:
        tqrn__mark = ()
    else:
        tqrn__mark = tuple('t1_key' + str(jeluu__jjnwl) for jeluu__jjnwl in
            range(udv__cesh))
    if join_node.is_right_table:
        dgsir__vvqi = ()
    else:
        dgsir__vvqi = tuple('t2_key' + str(jeluu__jjnwl) for jeluu__jjnwl in
            range(udv__cesh))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(tqrn__mark + dgsir__vvqi +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            skl__bdw = typemap[join_node.left_vars[0].name]
        else:
            skl__bdw = types.none
        for uiyx__solmv in left_physical_to_logical_list:
            if uiyx__solmv < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                nybm__edvi = skl__bdw.arr_types[uiyx__solmv]
            else:
                nybm__edvi = typemap[join_node.left_vars[-1].name]
            if uiyx__solmv in join_node.left_key_set:
                left_key_types.append(nybm__edvi)
            else:
                left_other_types.append(nybm__edvi)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[kezh__nlbya.name] for kezh__nlbya in
            zoep__ggvqu)
        left_other_types = tuple([typemap[pdp__sse.name] for pdp__sse in
            yvp__bad])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            skl__bdw = typemap[join_node.right_vars[0].name]
        else:
            skl__bdw = types.none
        for uiyx__solmv in right_physical_to_logical_list:
            if uiyx__solmv < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                nybm__edvi = skl__bdw.arr_types[uiyx__solmv]
            else:
                nybm__edvi = typemap[join_node.right_vars[-1].name]
            if uiyx__solmv in join_node.right_key_set:
                right_key_types.append(nybm__edvi)
            else:
                right_other_types.append(nybm__edvi)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[kezh__nlbya.name] for kezh__nlbya in
            umi__scakv)
        right_other_types = tuple([typemap[pdp__sse.name] for pdp__sse in
            zssrj__bya])
    matched_key_types = []
    for jeluu__jjnwl in range(udv__cesh):
        wfpd__khd = _match_join_key_types(left_key_types[jeluu__jjnwl],
            right_key_types[jeluu__jjnwl], loc)
        glbs[f'key_type_{jeluu__jjnwl}'] = wfpd__khd
        matched_key_types.append(wfpd__khd)
    if join_node.is_left_table:
        hoelo__ifkwt = determine_table_cast_map(matched_key_types,
            left_key_types, None, {jeluu__jjnwl: join_node.left_var_map[
            zsf__ose] for jeluu__jjnwl, zsf__ose in enumerate(join_node.
            left_keys)}, True)
        if hoelo__ifkwt:
            ztzj__lxky = False
            xxukw__sziwd = False
            axz__ylu = None
            if join_node.has_live_left_table_var:
                nzb__ror = list(typemap[join_node.left_vars[0].name].arr_types)
            else:
                nzb__ror = None
            for pvf__ytoyr, nybm__edvi in hoelo__ifkwt.items():
                if pvf__ytoyr < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    nzb__ror[pvf__ytoyr] = nybm__edvi
                    ztzj__lxky = True
                else:
                    axz__ylu = nybm__edvi
                    xxukw__sziwd = True
            if ztzj__lxky:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(nzb__ror))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if xxukw__sziwd:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = axz__ylu
    else:
        func_text += '    t1_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({tqrn__mark[jeluu__jjnwl]}, key_type_{jeluu__jjnwl})'
             if left_key_types[jeluu__jjnwl] != matched_key_types[
            jeluu__jjnwl] else f'{tqrn__mark[jeluu__jjnwl]}' for
            jeluu__jjnwl in range(udv__cesh)), ',' if udv__cesh != 0 else '')
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        hoelo__ifkwt = determine_table_cast_map(matched_key_types,
            right_key_types, None, {jeluu__jjnwl: join_node.right_var_map[
            zsf__ose] for jeluu__jjnwl, zsf__ose in enumerate(join_node.
            right_keys)}, True)
        if hoelo__ifkwt:
            ztzj__lxky = False
            xxukw__sziwd = False
            axz__ylu = None
            if join_node.has_live_right_table_var:
                nzb__ror = list(typemap[join_node.right_vars[0].name].arr_types
                    )
            else:
                nzb__ror = None
            for pvf__ytoyr, nybm__edvi in hoelo__ifkwt.items():
                if pvf__ytoyr < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    nzb__ror[pvf__ytoyr] = nybm__edvi
                    ztzj__lxky = True
                else:
                    axz__ylu = nybm__edvi
                    xxukw__sziwd = True
            if ztzj__lxky:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(nzb__ror))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if xxukw__sziwd:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = axz__ylu
    else:
        func_text += '    t2_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({dgsir__vvqi[jeluu__jjnwl]}, key_type_{jeluu__jjnwl})'
             if right_key_types[jeluu__jjnwl] != matched_key_types[
            jeluu__jjnwl] else f'{dgsir__vvqi[jeluu__jjnwl]}' for
            jeluu__jjnwl in range(udv__cesh)), ',' if udv__cesh != 0 else '')
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
        for jeluu__jjnwl in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(
                jeluu__jjnwl, jeluu__jjnwl)
        for jeluu__jjnwl in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                jeluu__jjnwl, jeluu__jjnwl)
        for jeluu__jjnwl in range(udv__cesh):
            func_text += (
                f'    t1_keys_{jeluu__jjnwl} = out_t1_keys[{jeluu__jjnwl}]\n')
        for jeluu__jjnwl in range(udv__cesh):
            func_text += (
                f'    t2_keys_{jeluu__jjnwl} = out_t2_keys[{jeluu__jjnwl}]\n')
    jywix__whrqo = {}
    exec(func_text, {}, jywix__whrqo)
    zdui__udgd = jywix__whrqo['f']
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
    doz__oxnzh = compile_to_numba_ir(zdui__udgd, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=zofoz__dhyr, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(doz__oxnzh, oigl__cunjp)
    sia__fixtz = doz__oxnzh.body[:-3]
    if join_node.has_live_out_index_var:
        sia__fixtz[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        sia__fixtz[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        sia__fixtz.pop(-1)
    elif not join_node.has_live_out_table_var:
        sia__fixtz.pop(-2)
    return sia__fixtz


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    dazn__ifj = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{dazn__ifj}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
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
    jywix__whrqo = {}
    exec(func_text, table_getitem_funcs, jywix__whrqo)
    yxz__sezns = jywix__whrqo[f'bodo_join_gen_cond{dazn__ifj}']
    rkx__apjf = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    agq__utvxm = numba.cfunc(rkx__apjf, nopython=True)(yxz__sezns)
    join_gen_cond_cfunc[agq__utvxm.native_name] = agq__utvxm
    join_gen_cond_cfunc_addr[agq__utvxm.native_name] = agq__utvxm.address
    return agq__utvxm, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    khz__efu = []
    for pdp__sse, lpj__jxv in name_to_var_map.items():
        bnx__pkv = f'({table_name}.{pdp__sse})'
        if bnx__pkv not in expr:
            continue
        fcw__vmwuk = f'getitem_{table_name}_val_{lpj__jxv}'
        if is_table_var:
            qzxi__jly = typemap[col_vars[0].name].arr_types[lpj__jxv]
        else:
            qzxi__jly = typemap[col_vars[lpj__jxv].name]
        if is_str_arr_type(qzxi__jly) or qzxi__jly == bodo.binary_array_type:
            xupk__jafz = (
                f'{fcw__vmwuk}({table_name}_table, {table_name}_ind)\n')
        else:
            xupk__jafz = (
                f'{fcw__vmwuk}({table_name}_data1, {table_name}_ind)\n')
        mwl__mmfz = logical_to_physical_ind[lpj__jxv]
        table_getitem_funcs[fcw__vmwuk
            ] = bodo.libs.array._gen_row_access_intrinsic(qzxi__jly, mwl__mmfz)
        expr = expr.replace(bnx__pkv, xupk__jafz)
        zqf__whc = f'({na_check_name}.{table_name}.{pdp__sse})'
        if zqf__whc in expr:
            aer__kdu = f'nacheck_{table_name}_val_{lpj__jxv}'
            etd__pau = f'_bodo_isna_{table_name}_val_{lpj__jxv}'
            if isinstance(qzxi__jly, (bodo.libs.int_arr_ext.
                IntegerArrayType, bodo.FloatingArrayType, bodo.TimeArrayType)
                ) or qzxi__jly in (bodo.libs.bool_arr_ext.boolean_array,
                bodo.binary_array_type, bodo.datetime_date_array_type
                ) or is_str_arr_type(qzxi__jly):
                func_text += f"""  {etd__pau} = {aer__kdu}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {etd__pau} = {aer__kdu}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[aer__kdu
                ] = bodo.libs.array._gen_row_na_check_intrinsic(qzxi__jly,
                mwl__mmfz)
            expr = expr.replace(zqf__whc, etd__pau)
        if lpj__jxv not in key_set:
            khz__efu.append(mwl__mmfz)
    return expr, func_text, khz__efu


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as ndq__mkj:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    vlwg__rgya = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[kezh__nlbya.name] in vlwg__rgya for
        kezh__nlbya in join_node.get_live_left_vars())
    if not join_node.get_live_left_vars():
        assert join_node.how == 'cross', 'cross join expected if left data is dead'
        left_parallel = join_node.left_dist in vlwg__rgya
    right_parallel = all(array_dists[kezh__nlbya.name] in vlwg__rgya for
        kezh__nlbya in join_node.get_live_right_vars())
    if not join_node.get_live_right_vars():
        assert join_node.how == 'cross', 'cross join expected if right data is dead'
        right_parallel = join_node.right_dist in vlwg__rgya
    if not left_parallel:
        assert not any(array_dists[kezh__nlbya.name] in vlwg__rgya for
            kezh__nlbya in join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[kezh__nlbya.name] in vlwg__rgya for
            kezh__nlbya in join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[kezh__nlbya.name] in vlwg__rgya for
            kezh__nlbya in join_node.get_live_out_vars())
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
    gogj__fclbk = set(left_col_nums)
    ssu__uxr = set(right_col_nums)
    wikbk__uuqk = join_node.vect_same_key
    mfup__qjqbj = []
    for jeluu__jjnwl in range(len(left_key_types)):
        if left_key_in_output[jeluu__jjnwl]:
            mfup__qjqbj.append(needs_typechange(matched_key_types[
                jeluu__jjnwl], join_node.is_right, wikbk__uuqk[jeluu__jjnwl]))
    qkn__saohh = len(left_key_types)
    dsdn__fymqx = 0
    xrb__umhqa = left_physical_to_logical_list[len(left_key_types):]
    for jeluu__jjnwl, uiyx__solmv in enumerate(xrb__umhqa):
        xar__dox = True
        if uiyx__solmv in gogj__fclbk:
            xar__dox = left_key_in_output[qkn__saohh]
            qkn__saohh += 1
        if xar__dox:
            mfup__qjqbj.append(needs_typechange(left_other_types[
                jeluu__jjnwl], join_node.is_right, False))
    for jeluu__jjnwl in range(len(right_key_types)):
        if not wikbk__uuqk[jeluu__jjnwl] and not join_node.is_join:
            if right_key_in_output[dsdn__fymqx]:
                mfup__qjqbj.append(needs_typechange(matched_key_types[
                    jeluu__jjnwl], join_node.is_left, False))
            dsdn__fymqx += 1
    bzog__atekf = right_physical_to_logical_list[len(right_key_types):]
    for jeluu__jjnwl, uiyx__solmv in enumerate(bzog__atekf):
        xar__dox = True
        if uiyx__solmv in ssu__uxr:
            xar__dox = right_key_in_output[dsdn__fymqx]
            dsdn__fymqx += 1
        if xar__dox:
            mfup__qjqbj.append(needs_typechange(right_other_types[
                jeluu__jjnwl], join_node.is_left, False))
    udv__cesh = len(left_key_types)
    func_text = '    # beginning of _gen_join_cpp_call\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            tpy__ldef = left_other_names[1:]
            nyfej__wiip = left_other_names[0]
        else:
            tpy__ldef = left_other_names
            nyfej__wiip = None
        smnou__nokd = '()' if len(tpy__ldef) == 0 else f'({tpy__ldef[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({nyfej__wiip}, {smnou__nokd}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        iyh__cbyfn = []
        for jeluu__jjnwl in range(udv__cesh):
            iyh__cbyfn.append('t1_keys[{}]'.format(jeluu__jjnwl))
        for jeluu__jjnwl in range(len(left_other_names)):
            iyh__cbyfn.append('data_left[{}]'.format(jeluu__jjnwl))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(grhki__yjccv) for grhki__yjccv in
            iyh__cbyfn))
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            fjo__rrkqz = right_other_names[1:]
            nyfej__wiip = right_other_names[0]
        else:
            fjo__rrkqz = right_other_names
            nyfej__wiip = None
        smnou__nokd = '()' if len(fjo__rrkqz) == 0 else f'({fjo__rrkqz[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({nyfej__wiip}, {smnou__nokd}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        ydq__ygd = []
        for jeluu__jjnwl in range(udv__cesh):
            ydq__ygd.append('t2_keys[{}]'.format(jeluu__jjnwl))
        for jeluu__jjnwl in range(len(right_other_names)):
            ydq__ygd.append('data_right[{}]'.format(jeluu__jjnwl))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(grhki__yjccv) for grhki__yjccv in
            ydq__ygd))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(wikbk__uuqk, dtype=np.int64)
    glbs['use_nullable_arr_type'] = np.array(mfup__qjqbj, dtype=np.int64)
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
        func_text += f"""    out_table = hash_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {udv__cesh}, {len(xrb__umhqa)}, {len(bzog__atekf)}, vect_same_key.ctypes, key_in_output.ctypes, use_nullable_arr_type.ctypes, {join_node.is_left}, {join_node.is_right}, {join_node.is_join}, {join_node.extra_data_col_num != -1}, {join_node.indicator_col_num != -1}, {join_node.is_na_equal}, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    dudud__pxgf = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {dudud__pxgf}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        spfw__kdkh = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{spfw__kdkh}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        vtzfn__jmxx = {}
        for jeluu__jjnwl, zsf__ose in enumerate(join_node.left_keys):
            if jeluu__jjnwl in left_used_key_nums:
                etkln__rowla = join_node.left_var_map[zsf__ose]
                vtzfn__jmxx[jeluu__jjnwl] = join_node.left_to_output_map[
                    etkln__rowla]
        hoelo__ifkwt = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, vtzfn__jmxx, False)
        ipsfa__hvnx = {}
        for jeluu__jjnwl, zsf__ose in enumerate(join_node.right_keys):
            if jeluu__jjnwl in right_used_key_nums:
                etkln__rowla = join_node.right_var_map[zsf__ose]
                ipsfa__hvnx[jeluu__jjnwl] = join_node.right_to_output_map[
                    etkln__rowla]
        hoelo__ifkwt.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, ipsfa__hvnx, False))
        ztzj__lxky = False
        xxukw__sziwd = False
        if join_node.has_live_out_table_var:
            nzb__ror = list(out_table_type.arr_types)
        else:
            nzb__ror = None
        for pvf__ytoyr, nybm__edvi in hoelo__ifkwt.items():
            if pvf__ytoyr < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                nzb__ror[pvf__ytoyr] = nybm__edvi
                ztzj__lxky = True
            else:
                axz__ylu = nybm__edvi
                xxukw__sziwd = True
        if ztzj__lxky:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            wpc__lsyr = bodo.TableType(tuple(nzb__ror))
            glbs['py_table_type'] = wpc__lsyr
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if xxukw__sziwd:
            glbs['index_col_type'] = axz__ylu
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
    hoelo__ifkwt: Dict[int, types.Type] = {}
    udv__cesh = len(matched_key_types)
    for jeluu__jjnwl in range(udv__cesh):
        if used_key_nums is None or jeluu__jjnwl in used_key_nums:
            if matched_key_types[jeluu__jjnwl] != key_types[jeluu__jjnwl] and (
                convert_dict_col or key_types[jeluu__jjnwl] != bodo.
                dict_str_arr_type):
                spfw__kdkh = output_map[jeluu__jjnwl]
                hoelo__ifkwt[spfw__kdkh] = matched_key_types[jeluu__jjnwl]
    return hoelo__ifkwt


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    soryo__mplv = bodo.libs.distributed_api.get_size()
    bgtns__rctkb = np.empty(soryo__mplv, left_key_arrs[0].dtype)
    qqioj__qpyyy = np.empty(soryo__mplv, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(bgtns__rctkb, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(qqioj__qpyyy, left_key_arrs[0][-1])
    bmdfs__gol = np.zeros(soryo__mplv, np.int32)
    flqra__ehvt = np.zeros(soryo__mplv, np.int32)
    powb__vdn = np.zeros(soryo__mplv, np.int32)
    xsk__vumb = right_key_arrs[0][0]
    cem__twpl = right_key_arrs[0][-1]
    fqdv__nceo = -1
    jeluu__jjnwl = 0
    while jeluu__jjnwl < soryo__mplv - 1 and qqioj__qpyyy[jeluu__jjnwl
        ] < xsk__vumb:
        jeluu__jjnwl += 1
    while jeluu__jjnwl < soryo__mplv and bgtns__rctkb[jeluu__jjnwl
        ] <= cem__twpl:
        fqdv__nceo, dpoov__cwrz = _count_overlap(right_key_arrs[0],
            bgtns__rctkb[jeluu__jjnwl], qqioj__qpyyy[jeluu__jjnwl])
        if fqdv__nceo != 0:
            fqdv__nceo -= 1
            dpoov__cwrz += 1
        bmdfs__gol[jeluu__jjnwl] = dpoov__cwrz
        flqra__ehvt[jeluu__jjnwl] = fqdv__nceo
        jeluu__jjnwl += 1
    while jeluu__jjnwl < soryo__mplv:
        bmdfs__gol[jeluu__jjnwl] = 1
        flqra__ehvt[jeluu__jjnwl] = len(right_key_arrs[0]) - 1
        jeluu__jjnwl += 1
    bodo.libs.distributed_api.alltoall(bmdfs__gol, powb__vdn, 1)
    laz__dersv = powb__vdn.sum()
    qkovx__aukbc = np.empty(laz__dersv, right_key_arrs[0].dtype)
    tcfx__jpf = alloc_arr_tup(laz__dersv, right_data)
    qqp__qawq = bodo.ir.join.calc_disp(powb__vdn)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], qkovx__aukbc,
        bmdfs__gol, powb__vdn, flqra__ehvt, qqp__qawq)
    bodo.libs.distributed_api.alltoallv_tup(right_data, tcfx__jpf,
        bmdfs__gol, powb__vdn, flqra__ehvt, qqp__qawq)
    return (qkovx__aukbc,), tcfx__jpf


@numba.njit
def _count_overlap(r_key_arr, start, end):
    dpoov__cwrz = 0
    fqdv__nceo = 0
    ntzxb__cik = 0
    while ntzxb__cik < len(r_key_arr) and r_key_arr[ntzxb__cik] < start:
        fqdv__nceo += 1
        ntzxb__cik += 1
    while ntzxb__cik < len(r_key_arr) and start <= r_key_arr[ntzxb__cik
        ] <= end:
        ntzxb__cik += 1
        dpoov__cwrz += 1
    return fqdv__nceo, dpoov__cwrz


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    kand__rioss = np.empty_like(arr)
    kand__rioss[0] = 0
    for jeluu__jjnwl in range(1, len(arr)):
        kand__rioss[jeluu__jjnwl] = kand__rioss[jeluu__jjnwl - 1] + arr[
            jeluu__jjnwl - 1]
    return kand__rioss


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    gfkce__vno = len(left_keys[0])
    qbewa__kei = len(right_keys[0])
    tzvy__tsu = alloc_arr_tup(gfkce__vno, left_keys)
    spx__gzqm = alloc_arr_tup(gfkce__vno, right_keys)
    ncv__dhii = alloc_arr_tup(gfkce__vno, data_left)
    mwpk__icrfg = alloc_arr_tup(gfkce__vno, data_right)
    lndkj__ovwan = 0
    lkelo__edosy = 0
    for lndkj__ovwan in range(gfkce__vno):
        if lkelo__edosy < 0:
            lkelo__edosy = 0
        while lkelo__edosy < qbewa__kei and getitem_arr_tup(right_keys,
            lkelo__edosy) <= getitem_arr_tup(left_keys, lndkj__ovwan):
            lkelo__edosy += 1
        lkelo__edosy -= 1
        setitem_arr_tup(tzvy__tsu, lndkj__ovwan, getitem_arr_tup(left_keys,
            lndkj__ovwan))
        setitem_arr_tup(ncv__dhii, lndkj__ovwan, getitem_arr_tup(data_left,
            lndkj__ovwan))
        if lkelo__edosy >= 0:
            setitem_arr_tup(spx__gzqm, lndkj__ovwan, getitem_arr_tup(
                right_keys, lkelo__edosy))
            setitem_arr_tup(mwpk__icrfg, lndkj__ovwan, getitem_arr_tup(
                data_right, lkelo__edosy))
        else:
            bodo.libs.array_kernels.setna_tup(spx__gzqm, lndkj__ovwan)
            bodo.libs.array_kernels.setna_tup(mwpk__icrfg, lndkj__ovwan)
    return tzvy__tsu, spx__gzqm, ncv__dhii, mwpk__icrfg
