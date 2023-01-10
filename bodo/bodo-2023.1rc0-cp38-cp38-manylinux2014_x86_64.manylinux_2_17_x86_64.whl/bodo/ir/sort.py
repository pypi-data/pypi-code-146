"""IR node for the data sorting"""
from collections import defaultdict
from typing import List, Set, Tuple, Union
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, mk_unique_var, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_data_to_cpp_table, sort_values_table
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, _find_used_columns, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import MetaType, is_overload_none, type_has_unknown_cats
from bodo.utils.utils import gen_getitem


class Sort(ir.Stmt):

    def __init__(self, df_in: str, df_out: str, in_vars: List[ir.Var],
        out_vars: List[ir.Var], key_inds: Tuple[int], inplace: bool, loc:
        ir.Loc, ascending_list: Union[List[bool], bool]=True, na_position:
        Union[List[str], str]='last', _bodo_chunk_bounds: Union[ir.Var,
        None]=None, is_table_format: bool=False, num_table_arrays: int=0):
        self.df_in = df_in
        self.df_out = df_out
        self.in_vars = in_vars
        self.out_vars = out_vars
        self.key_inds = key_inds
        self.inplace = inplace
        self._bodo_chunk_bounds = _bodo_chunk_bounds
        self.is_table_format = is_table_format
        self.num_table_arrays = num_table_arrays
        self.dead_var_inds: Set[int] = set()
        self.dead_key_var_inds: Set[int] = set()
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_inds)
            else:
                self.na_position_b = (False,) * len(key_inds)
        else:
            self.na_position_b = tuple([(True if tjatk__lifrp == 'last' else
                False) for tjatk__lifrp in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [aif__fiyoc for aif__fiyoc in self.in_vars if aif__fiyoc is not
            None]

    def get_live_out_vars(self):
        return [aif__fiyoc for aif__fiyoc in self.out_vars if aif__fiyoc is not
            None]

    def __repr__(self):
        eds__uwqa = ', '.join(aif__fiyoc.name for aif__fiyoc in self.
            get_live_in_vars())
        pcypg__doggk = f'{self.df_in}{{{eds__uwqa}}}'
        ruc__nmmb = ', '.join(aif__fiyoc.name for aif__fiyoc in self.
            get_live_out_vars())
        wvh__undld = f'{self.df_out}{{{ruc__nmmb}}}'
        return f'Sort (keys: {self.key_inds}): {pcypg__doggk} {wvh__undld}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    ift__fpxll = []
    for yveb__vinou in sort_node.get_live_in_vars():
        hodu__kqop = equiv_set.get_shape(yveb__vinou)
        if hodu__kqop is not None:
            ift__fpxll.append(hodu__kqop[0])
    if len(ift__fpxll) > 1:
        equiv_set.insert_equiv(*ift__fpxll)
    tvie__eefno = []
    ift__fpxll = []
    for yveb__vinou in sort_node.get_live_out_vars():
        jtp__mme = typemap[yveb__vinou.name]
        yyzal__gbswb = array_analysis._gen_shape_call(equiv_set,
            yveb__vinou, jtp__mme.ndim, None, tvie__eefno)
        equiv_set.insert_equiv(yveb__vinou, yyzal__gbswb)
        ift__fpxll.append(yyzal__gbswb[0])
        equiv_set.define(yveb__vinou, set())
    if len(ift__fpxll) > 1:
        equiv_set.insert_equiv(*ift__fpxll)
    return [], tvie__eefno


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    pxbo__dsadn = sort_node.get_live_in_vars()
    qejg__scikj = sort_node.get_live_out_vars()
    bqi__ryi = Distribution.OneD
    for yveb__vinou in pxbo__dsadn:
        bqi__ryi = Distribution(min(bqi__ryi.value, array_dists[yveb__vinou
            .name].value))
    ynq__cfq = Distribution(min(bqi__ryi.value, Distribution.OneD_Var.value))
    for yveb__vinou in qejg__scikj:
        if yveb__vinou.name in array_dists:
            ynq__cfq = Distribution(min(ynq__cfq.value, array_dists[
                yveb__vinou.name].value))
    if ynq__cfq != Distribution.OneD_Var:
        bqi__ryi = ynq__cfq
    for yveb__vinou in pxbo__dsadn:
        array_dists[yveb__vinou.name] = bqi__ryi
    for yveb__vinou in qejg__scikj:
        array_dists[yveb__vinou.name] = ynq__cfq


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for kwqd__necn, myp__uzx in enumerate(sort_node.out_vars):
        yhhh__wckh = sort_node.in_vars[kwqd__necn]
        if yhhh__wckh is not None and myp__uzx is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=myp__uzx
                .name, src=yhhh__wckh.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for yveb__vinou in sort_node.get_live_out_vars():
            definitions[yveb__vinou.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for kwqd__necn in range(len(sort_node.in_vars)):
        if sort_node.in_vars[kwqd__necn] is not None:
            sort_node.in_vars[kwqd__necn] = visit_vars_inner(sort_node.
                in_vars[kwqd__necn], callback, cbdata)
        if sort_node.out_vars[kwqd__necn] is not None:
            sort_node.out_vars[kwqd__necn] = visit_vars_inner(sort_node.
                out_vars[kwqd__necn], callback, cbdata)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = visit_vars_inner(sort_node.
            _bodo_chunk_bounds, callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        aqclu__lvbsq = sort_node.out_vars[0]
        if aqclu__lvbsq is not None and aqclu__lvbsq.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            tkzmb__ezu = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & tkzmb__ezu)
            sort_node.dead_var_inds.update(dead_cols - tkzmb__ezu)
            if len(tkzmb__ezu & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for kwqd__necn in range(1, len(sort_node.out_vars)):
            aif__fiyoc = sort_node.out_vars[kwqd__necn]
            if aif__fiyoc is not None and aif__fiyoc.name not in lives:
                sort_node.out_vars[kwqd__necn] = None
                itxuj__atw = sort_node.num_table_arrays + kwqd__necn - 1
                if itxuj__atw in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(itxuj__atw)
                else:
                    sort_node.dead_var_inds.add(itxuj__atw)
                    sort_node.in_vars[kwqd__necn] = None
    else:
        for kwqd__necn in range(len(sort_node.out_vars)):
            aif__fiyoc = sort_node.out_vars[kwqd__necn]
            if aif__fiyoc is not None and aif__fiyoc.name not in lives:
                sort_node.out_vars[kwqd__necn] = None
                if kwqd__necn in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(kwqd__necn)
                else:
                    sort_node.dead_var_inds.add(kwqd__necn)
                    sort_node.in_vars[kwqd__necn] = None
    if all(aif__fiyoc is None for aif__fiyoc in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({aif__fiyoc.name for aif__fiyoc in sort_node.
        get_live_in_vars()})
    if not sort_node.inplace:
        def_set.update({aif__fiyoc.name for aif__fiyoc in sort_node.
            get_live_out_vars()})
    if sort_node._bodo_chunk_bounds is not None:
        use_set.add(sort_node._bodo_chunk_bounds.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    pwv__wgbl = set()
    if not sort_node.inplace:
        pwv__wgbl.update({aif__fiyoc.name for aif__fiyoc in sort_node.
            get_live_out_vars()})
    return set(), pwv__wgbl


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for kwqd__necn in range(len(sort_node.in_vars)):
        if sort_node.in_vars[kwqd__necn] is not None:
            sort_node.in_vars[kwqd__necn] = replace_vars_inner(sort_node.
                in_vars[kwqd__necn], var_dict)
        if sort_node.out_vars[kwqd__necn] is not None:
            sort_node.out_vars[kwqd__necn] = replace_vars_inner(sort_node.
                out_vars[kwqd__necn], var_dict)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = replace_vars_inner(sort_node.
            _bodo_chunk_bounds, var_dict)


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    in_vars = sort_node.get_live_in_vars()
    out_vars = sort_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for aif__fiyoc in (in_vars + out_vars):
            if array_dists[aif__fiyoc.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                aif__fiyoc.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        pbhos__pebdt = []
        for aif__fiyoc in in_vars:
            nhe__kvfc = _copy_array_nodes(aif__fiyoc, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            pbhos__pebdt.append(nhe__kvfc)
        in_vars = pbhos__pebdt
    out_types = [(typemap[aif__fiyoc.name] if aif__fiyoc is not None else
        types.none) for aif__fiyoc in sort_node.out_vars]
    bttwa__hwblx, suth__xnpo = get_sort_cpp_section(sort_node, out_types,
        typemap, parallel)
    cre__jhvlb = {}
    exec(bttwa__hwblx, {}, cre__jhvlb)
    sukz__bat = cre__jhvlb['f']
    suth__xnpo.update({'bodo': bodo, 'np': np, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'sort_values_table': sort_values_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'array_to_info': array_to_info,
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    suth__xnpo.update({f'out_type{kwqd__necn}': out_types[kwqd__necn] for
        kwqd__necn in range(len(out_types))})
    xcb__pge = sort_node._bodo_chunk_bounds
    hysm__pftto = xcb__pge
    if xcb__pge is None:
        loc = sort_node.loc
        hysm__pftto = ir.Var(ir.Scope(None, loc), mk_unique_var(
            '$bounds_none'), loc)
        typemap[hysm__pftto.name] = types.none
        nodes.append(ir.Assign(ir.Const(None, loc), hysm__pftto, loc))
    lqjiv__rbona = compile_to_numba_ir(sukz__bat, suth__xnpo, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[aif__fiyoc.
        name] for aif__fiyoc in in_vars) + (typemap[hysm__pftto.name],),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(lqjiv__rbona, in_vars + [hysm__pftto])
    klzk__lcdus = lqjiv__rbona.body[-2].value.value
    nodes += lqjiv__rbona.body[:-2]
    for kwqd__necn, aif__fiyoc in enumerate(out_vars):
        gen_getitem(aif__fiyoc, klzk__lcdus, kwqd__necn, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    yqgk__kxq = lambda arr: arr.copy()
    jnf__vsipx = None
    if isinstance(typemap[var.name], TableType):
        tdozv__qteje = len(typemap[var.name].arr_types)
        jnf__vsipx = set(range(tdozv__qteje)) - dead_cols
        jnf__vsipx = MetaType(tuple(sorted(jnf__vsipx)))
        yqgk__kxq = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    lqjiv__rbona = compile_to_numba_ir(yqgk__kxq, {'bodo': bodo, 'types':
        types, '_used_columns': jnf__vsipx}, typingctx=typingctx, targetctx
        =targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(lqjiv__rbona, [var])
    nodes += lqjiv__rbona.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, typemap, parallel):
    gao__wsvh = len(sort_node.key_inds)
    yxtpp__empz = len(sort_node.in_vars)
    bvif__mpo = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + yxtpp__empz - 1 if sort_node.
        is_table_format else yxtpp__empz)
    thu__wodja, gjsg__emufa, wnmh__brxkt = _get_cpp_col_ind_mappings(sort_node
        .key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols
        )
    rxs__zue = []
    if sort_node.is_table_format:
        rxs__zue.append('arg0')
        for kwqd__necn in range(1, yxtpp__empz):
            itxuj__atw = sort_node.num_table_arrays + kwqd__necn - 1
            if itxuj__atw not in sort_node.dead_var_inds:
                rxs__zue.append(f'arg{itxuj__atw}')
    else:
        for kwqd__necn in range(n_cols):
            if kwqd__necn not in sort_node.dead_var_inds:
                rxs__zue.append(f'arg{kwqd__necn}')
    bttwa__hwblx = f"def f({', '.join(rxs__zue)}, bounds_in):\n"
    if sort_node.is_table_format:
        wbsf__gkapt = ',' if yxtpp__empz - 1 == 1 else ''
        hojpi__hsisu = []
        for kwqd__necn in range(sort_node.num_table_arrays, n_cols):
            if kwqd__necn in sort_node.dead_var_inds:
                hojpi__hsisu.append('None')
            else:
                hojpi__hsisu.append(f'arg{kwqd__necn}')
        bttwa__hwblx += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(hojpi__hsisu)}{wbsf__gkapt}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        ekw__nzur = {lvp__sjjd: kwqd__necn for kwqd__necn, lvp__sjjd in
            enumerate(thu__wodja)}
        nmhh__ovbjr = [None] * len(thu__wodja)
        for kwqd__necn in range(n_cols):
            biag__dqsp = ekw__nzur.get(kwqd__necn, -1)
            if biag__dqsp != -1:
                nmhh__ovbjr[biag__dqsp] = f'array_to_info(arg{kwqd__necn})'
        bttwa__hwblx += '  info_list_total = [{}]\n'.format(','.join(
            nmhh__ovbjr))
        bttwa__hwblx += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    bttwa__hwblx += '  vect_ascending = np.array([{}], np.int64)\n'.format(','
        .join('1' if uucj__fbizi else '0' for uucj__fbizi in sort_node.
        ascending_list))
    bttwa__hwblx += '  na_position = np.array([{}], np.int64)\n'.format(','
        .join('1' if uucj__fbizi else '0' for uucj__fbizi in sort_node.
        na_position_b))
    bttwa__hwblx += '  dead_keys = np.array([{}], np.int64)\n'.format(','.
        join('1' if kwqd__necn in wnmh__brxkt else '0' for kwqd__necn in
        range(gao__wsvh)))
    bttwa__hwblx += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    gtn__ioqv = sort_node._bodo_chunk_bounds
    kfz__kzq = '0' if gtn__ioqv is None or is_overload_none(typemap[
        gtn__ioqv.name]
        ) else 'arr_info_list_to_table([array_to_info(bounds_in)])'
    bttwa__hwblx += f"""  out_cpp_table = sort_values_table(in_cpp_table, {gao__wsvh}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {kfz__kzq}, {parallel})
"""
    if sort_node.is_table_format:
        wbsf__gkapt = ',' if bvif__mpo == 1 else ''
        vseiz__yisf = (
            f"({', '.join(f'out_type{kwqd__necn}' if not type_has_unknown_cats(out_types[kwqd__necn]) else f'arg{kwqd__necn}' for kwqd__necn in range(bvif__mpo))}{wbsf__gkapt})"
            )
        bttwa__hwblx += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {vseiz__yisf}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        ekw__nzur = {lvp__sjjd: kwqd__necn for kwqd__necn, lvp__sjjd in
            enumerate(gjsg__emufa)}
        nmhh__ovbjr = []
        for kwqd__necn in range(n_cols):
            biag__dqsp = ekw__nzur.get(kwqd__necn, -1)
            if biag__dqsp != -1:
                iter__uafb = (f'out_type{kwqd__necn}' if not
                    type_has_unknown_cats(out_types[kwqd__necn]) else
                    f'arg{kwqd__necn}')
                bttwa__hwblx += f"""  out{kwqd__necn} = info_to_array(info_from_table(out_cpp_table, {biag__dqsp}), {iter__uafb})
"""
                nmhh__ovbjr.append(f'out{kwqd__necn}')
        wbsf__gkapt = ',' if len(nmhh__ovbjr) == 1 else ''
        lkh__rcbp = f"({', '.join(nmhh__ovbjr)}{wbsf__gkapt})"
        bttwa__hwblx += f'  out_data = {lkh__rcbp}\n'
    bttwa__hwblx += '  delete_table(out_cpp_table)\n'
    bttwa__hwblx += '  delete_table(in_cpp_table)\n'
    bttwa__hwblx += f'  return out_data\n'
    return bttwa__hwblx, {'in_col_inds': MetaType(tuple(thu__wodja)),
        'out_col_inds': MetaType(tuple(gjsg__emufa))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    thu__wodja = []
    gjsg__emufa = []
    wnmh__brxkt = []
    for lvp__sjjd, kwqd__necn in enumerate(key_inds):
        thu__wodja.append(kwqd__necn)
        if kwqd__necn in dead_key_var_inds:
            wnmh__brxkt.append(lvp__sjjd)
        else:
            gjsg__emufa.append(kwqd__necn)
    for kwqd__necn in range(n_cols):
        if kwqd__necn in dead_var_inds or kwqd__necn in key_inds:
            continue
        thu__wodja.append(kwqd__necn)
        gjsg__emufa.append(kwqd__necn)
    return thu__wodja, gjsg__emufa, wnmh__brxkt


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    euat__ryu = sort_node.in_vars[0].name
    xuvtc__cwjp = sort_node.out_vars[0].name
    dsuk__gnxt, lod__spm, lfb__saa = block_use_map[euat__ryu]
    if lod__spm or lfb__saa:
        return
    kzohs__tpts, vwew__hoy, baivo__bdya = _compute_table_column_uses(
        xuvtc__cwjp, table_col_use_map, equiv_vars)
    grutl__hpljl = set(kwqd__necn for kwqd__necn in sort_node.key_inds if 
        kwqd__necn < sort_node.num_table_arrays)
    block_use_map[euat__ryu] = (dsuk__gnxt | kzohs__tpts | grutl__hpljl, 
        vwew__hoy or baivo__bdya, False)


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    tdozv__qteje = sort_node.num_table_arrays
    xuvtc__cwjp = sort_node.out_vars[0].name
    jnf__vsipx = _find_used_columns(xuvtc__cwjp, tdozv__qteje,
        column_live_map, equiv_vars)
    if jnf__vsipx is None:
        return False
    jmsj__mbn = set(range(tdozv__qteje)) - jnf__vsipx
    grutl__hpljl = set(kwqd__necn for kwqd__necn in sort_node.key_inds if 
        kwqd__necn < tdozv__qteje)
    jht__saug = sort_node.dead_key_var_inds | jmsj__mbn & grutl__hpljl
    cmkq__jwh = sort_node.dead_var_inds | jmsj__mbn - grutl__hpljl
    afm__xmja = (jht__saug != sort_node.dead_key_var_inds) | (cmkq__jwh !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = jht__saug
    sort_node.dead_var_inds = cmkq__jwh
    return afm__xmja


remove_dead_column_extensions[Sort] = sort_remove_dead_column
