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
            self.na_position_b = tuple([(True if vlabe__otbya == 'last' else
                False) for vlabe__otbya in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [ypk__trk for ypk__trk in self.in_vars if ypk__trk is not None]

    def get_live_out_vars(self):
        return [ypk__trk for ypk__trk in self.out_vars if ypk__trk is not None]

    def __repr__(self):
        ykiew__sgpiy = ', '.join(ypk__trk.name for ypk__trk in self.
            get_live_in_vars())
        uezl__wpb = f'{self.df_in}{{{ykiew__sgpiy}}}'
        ooz__rgit = ', '.join(ypk__trk.name for ypk__trk in self.
            get_live_out_vars())
        ljaaq__ayybr = f'{self.df_out}{{{ooz__rgit}}}'
        return f'Sort (keys: {self.key_inds}): {uezl__wpb} {ljaaq__ayybr}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    nmdl__llb = []
    for fdo__zvn in sort_node.get_live_in_vars():
        qkpr__rjcp = equiv_set.get_shape(fdo__zvn)
        if qkpr__rjcp is not None:
            nmdl__llb.append(qkpr__rjcp[0])
    if len(nmdl__llb) > 1:
        equiv_set.insert_equiv(*nmdl__llb)
    nna__xmvob = []
    nmdl__llb = []
    for fdo__zvn in sort_node.get_live_out_vars():
        xezk__uow = typemap[fdo__zvn.name]
        nhpry__nwuf = array_analysis._gen_shape_call(equiv_set, fdo__zvn,
            xezk__uow.ndim, None, nna__xmvob)
        equiv_set.insert_equiv(fdo__zvn, nhpry__nwuf)
        nmdl__llb.append(nhpry__nwuf[0])
        equiv_set.define(fdo__zvn, set())
    if len(nmdl__llb) > 1:
        equiv_set.insert_equiv(*nmdl__llb)
    return [], nna__xmvob


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    wft__tult = sort_node.get_live_in_vars()
    czj__lsspn = sort_node.get_live_out_vars()
    akj__bmjf = Distribution.OneD
    for fdo__zvn in wft__tult:
        akj__bmjf = Distribution(min(akj__bmjf.value, array_dists[fdo__zvn.
            name].value))
    kcrrd__rfxbe = Distribution(min(akj__bmjf.value, Distribution.OneD_Var.
        value))
    for fdo__zvn in czj__lsspn:
        if fdo__zvn.name in array_dists:
            kcrrd__rfxbe = Distribution(min(kcrrd__rfxbe.value, array_dists
                [fdo__zvn.name].value))
    if kcrrd__rfxbe != Distribution.OneD_Var:
        akj__bmjf = kcrrd__rfxbe
    for fdo__zvn in wft__tult:
        array_dists[fdo__zvn.name] = akj__bmjf
    for fdo__zvn in czj__lsspn:
        array_dists[fdo__zvn.name] = kcrrd__rfxbe


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for glx__dxj, kmgf__dkf in enumerate(sort_node.out_vars):
        zqbd__oivh = sort_node.in_vars[glx__dxj]
        if zqbd__oivh is not None and kmgf__dkf is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=
                kmgf__dkf.name, src=zqbd__oivh.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for fdo__zvn in sort_node.get_live_out_vars():
            definitions[fdo__zvn.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for glx__dxj in range(len(sort_node.in_vars)):
        if sort_node.in_vars[glx__dxj] is not None:
            sort_node.in_vars[glx__dxj] = visit_vars_inner(sort_node.
                in_vars[glx__dxj], callback, cbdata)
        if sort_node.out_vars[glx__dxj] is not None:
            sort_node.out_vars[glx__dxj] = visit_vars_inner(sort_node.
                out_vars[glx__dxj], callback, cbdata)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = visit_vars_inner(sort_node.
            _bodo_chunk_bounds, callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        bjl__nhzpw = sort_node.out_vars[0]
        if bjl__nhzpw is not None and bjl__nhzpw.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            veryn__wbgt = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & veryn__wbgt)
            sort_node.dead_var_inds.update(dead_cols - veryn__wbgt)
            if len(veryn__wbgt & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for glx__dxj in range(1, len(sort_node.out_vars)):
            ypk__trk = sort_node.out_vars[glx__dxj]
            if ypk__trk is not None and ypk__trk.name not in lives:
                sort_node.out_vars[glx__dxj] = None
                uscod__vgz = sort_node.num_table_arrays + glx__dxj - 1
                if uscod__vgz in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(uscod__vgz)
                else:
                    sort_node.dead_var_inds.add(uscod__vgz)
                    sort_node.in_vars[glx__dxj] = None
    else:
        for glx__dxj in range(len(sort_node.out_vars)):
            ypk__trk = sort_node.out_vars[glx__dxj]
            if ypk__trk is not None and ypk__trk.name not in lives:
                sort_node.out_vars[glx__dxj] = None
                if glx__dxj in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(glx__dxj)
                else:
                    sort_node.dead_var_inds.add(glx__dxj)
                    sort_node.in_vars[glx__dxj] = None
    if all(ypk__trk is None for ypk__trk in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({ypk__trk.name for ypk__trk in sort_node.get_live_in_vars()}
        )
    if not sort_node.inplace:
        def_set.update({ypk__trk.name for ypk__trk in sort_node.
            get_live_out_vars()})
    if sort_node._bodo_chunk_bounds is not None:
        use_set.add(sort_node._bodo_chunk_bounds.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    pcw__zxeco = set()
    if not sort_node.inplace:
        pcw__zxeco.update({ypk__trk.name for ypk__trk in sort_node.
            get_live_out_vars()})
    return set(), pcw__zxeco


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for glx__dxj in range(len(sort_node.in_vars)):
        if sort_node.in_vars[glx__dxj] is not None:
            sort_node.in_vars[glx__dxj] = replace_vars_inner(sort_node.
                in_vars[glx__dxj], var_dict)
        if sort_node.out_vars[glx__dxj] is not None:
            sort_node.out_vars[glx__dxj] = replace_vars_inner(sort_node.
                out_vars[glx__dxj], var_dict)
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
        for ypk__trk in (in_vars + out_vars):
            if array_dists[ypk__trk.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                ypk__trk.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        glh__bbdum = []
        for ypk__trk in in_vars:
            otw__xwy = _copy_array_nodes(ypk__trk, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            glh__bbdum.append(otw__xwy)
        in_vars = glh__bbdum
    out_types = [(typemap[ypk__trk.name] if ypk__trk is not None else types
        .none) for ypk__trk in sort_node.out_vars]
    cxv__uuk, vkm__ihjx = get_sort_cpp_section(sort_node, out_types,
        typemap, parallel)
    jgtxd__vsfdl = {}
    exec(cxv__uuk, {}, jgtxd__vsfdl)
    ucy__grliq = jgtxd__vsfdl['f']
    vkm__ihjx.update({'bodo': bodo, 'np': np, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'sort_values_table': sort_values_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'array_to_info': array_to_info,
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    vkm__ihjx.update({f'out_type{glx__dxj}': out_types[glx__dxj] for
        glx__dxj in range(len(out_types))})
    gmh__uxls = sort_node._bodo_chunk_bounds
    rigr__mtia = gmh__uxls
    if gmh__uxls is None:
        loc = sort_node.loc
        rigr__mtia = ir.Var(ir.Scope(None, loc), mk_unique_var(
            '$bounds_none'), loc)
        typemap[rigr__mtia.name] = types.none
        nodes.append(ir.Assign(ir.Const(None, loc), rigr__mtia, loc))
    qhknk__uzji = compile_to_numba_ir(ucy__grliq, vkm__ihjx, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[ypk__trk.
        name] for ypk__trk in in_vars) + (typemap[rigr__mtia.name],),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(qhknk__uzji, in_vars + [rigr__mtia])
    pgk__rdyn = qhknk__uzji.body[-2].value.value
    nodes += qhknk__uzji.body[:-2]
    for glx__dxj, ypk__trk in enumerate(out_vars):
        gen_getitem(ypk__trk, pgk__rdyn, glx__dxj, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    zlthk__acar = lambda arr: arr.copy()
    rxks__wtbkz = None
    if isinstance(typemap[var.name], TableType):
        mgqc__rmy = len(typemap[var.name].arr_types)
        rxks__wtbkz = set(range(mgqc__rmy)) - dead_cols
        rxks__wtbkz = MetaType(tuple(sorted(rxks__wtbkz)))
        zlthk__acar = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    qhknk__uzji = compile_to_numba_ir(zlthk__acar, {'bodo': bodo, 'types':
        types, '_used_columns': rxks__wtbkz}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(qhknk__uzji, [var])
    nodes += qhknk__uzji.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, typemap, parallel):
    gxkyp__kzux = len(sort_node.key_inds)
    rrop__eym = len(sort_node.in_vars)
    yqcj__txy = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + rrop__eym - 1 if sort_node.
        is_table_format else rrop__eym)
    wamy__ztx, rzels__vumzz, bqlp__dzqvx = _get_cpp_col_ind_mappings(sort_node
        .key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols
        )
    tsd__ruyy = []
    if sort_node.is_table_format:
        tsd__ruyy.append('arg0')
        for glx__dxj in range(1, rrop__eym):
            uscod__vgz = sort_node.num_table_arrays + glx__dxj - 1
            if uscod__vgz not in sort_node.dead_var_inds:
                tsd__ruyy.append(f'arg{uscod__vgz}')
    else:
        for glx__dxj in range(n_cols):
            if glx__dxj not in sort_node.dead_var_inds:
                tsd__ruyy.append(f'arg{glx__dxj}')
    cxv__uuk = f"def f({', '.join(tsd__ruyy)}, bounds_in):\n"
    if sort_node.is_table_format:
        ygjh__ofg = ',' if rrop__eym - 1 == 1 else ''
        lpekp__hkdyv = []
        for glx__dxj in range(sort_node.num_table_arrays, n_cols):
            if glx__dxj in sort_node.dead_var_inds:
                lpekp__hkdyv.append('None')
            else:
                lpekp__hkdyv.append(f'arg{glx__dxj}')
        cxv__uuk += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(lpekp__hkdyv)}{ygjh__ofg}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        lgays__jetco = {hqu__qhqfl: glx__dxj for glx__dxj, hqu__qhqfl in
            enumerate(wamy__ztx)}
        qqrno__gae = [None] * len(wamy__ztx)
        for glx__dxj in range(n_cols):
            qfiu__aqnbo = lgays__jetco.get(glx__dxj, -1)
            if qfiu__aqnbo != -1:
                qqrno__gae[qfiu__aqnbo] = f'array_to_info(arg{glx__dxj})'
        cxv__uuk += '  info_list_total = [{}]\n'.format(','.join(qqrno__gae))
        cxv__uuk += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    cxv__uuk += '  vect_ascending = np.array([{}], np.int64)\n'.format(','.
        join('1' if gtmtb__bjpl else '0' for gtmtb__bjpl in sort_node.
        ascending_list))
    cxv__uuk += '  na_position = np.array([{}], np.int64)\n'.format(','.
        join('1' if gtmtb__bjpl else '0' for gtmtb__bjpl in sort_node.
        na_position_b))
    cxv__uuk += '  dead_keys = np.array([{}], np.int64)\n'.format(','.join(
        '1' if glx__dxj in bqlp__dzqvx else '0' for glx__dxj in range(
        gxkyp__kzux)))
    cxv__uuk += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    nqz__hvx = sort_node._bodo_chunk_bounds
    zmv__wvlu = '0' if nqz__hvx is None or is_overload_none(typemap[
        nqz__hvx.name]
        ) else 'arr_info_list_to_table([array_to_info(bounds_in)])'
    cxv__uuk += f"""  out_cpp_table = sort_values_table(in_cpp_table, {gxkyp__kzux}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {zmv__wvlu}, {parallel})
"""
    if sort_node.is_table_format:
        ygjh__ofg = ',' if yqcj__txy == 1 else ''
        kedg__wiom = (
            f"({', '.join(f'out_type{glx__dxj}' if not type_has_unknown_cats(out_types[glx__dxj]) else f'arg{glx__dxj}' for glx__dxj in range(yqcj__txy))}{ygjh__ofg})"
            )
        cxv__uuk += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {kedg__wiom}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        lgays__jetco = {hqu__qhqfl: glx__dxj for glx__dxj, hqu__qhqfl in
            enumerate(rzels__vumzz)}
        qqrno__gae = []
        for glx__dxj in range(n_cols):
            qfiu__aqnbo = lgays__jetco.get(glx__dxj, -1)
            if qfiu__aqnbo != -1:
                lldii__nlpwo = (f'out_type{glx__dxj}' if not
                    type_has_unknown_cats(out_types[glx__dxj]) else
                    f'arg{glx__dxj}')
                cxv__uuk += f"""  out{glx__dxj} = info_to_array(info_from_table(out_cpp_table, {qfiu__aqnbo}), {lldii__nlpwo})
"""
                qqrno__gae.append(f'out{glx__dxj}')
        ygjh__ofg = ',' if len(qqrno__gae) == 1 else ''
        fwl__qyar = f"({', '.join(qqrno__gae)}{ygjh__ofg})"
        cxv__uuk += f'  out_data = {fwl__qyar}\n'
    cxv__uuk += '  delete_table(out_cpp_table)\n'
    cxv__uuk += '  delete_table(in_cpp_table)\n'
    cxv__uuk += f'  return out_data\n'
    return cxv__uuk, {'in_col_inds': MetaType(tuple(wamy__ztx)),
        'out_col_inds': MetaType(tuple(rzels__vumzz))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    wamy__ztx = []
    rzels__vumzz = []
    bqlp__dzqvx = []
    for hqu__qhqfl, glx__dxj in enumerate(key_inds):
        wamy__ztx.append(glx__dxj)
        if glx__dxj in dead_key_var_inds:
            bqlp__dzqvx.append(hqu__qhqfl)
        else:
            rzels__vumzz.append(glx__dxj)
    for glx__dxj in range(n_cols):
        if glx__dxj in dead_var_inds or glx__dxj in key_inds:
            continue
        wamy__ztx.append(glx__dxj)
        rzels__vumzz.append(glx__dxj)
    return wamy__ztx, rzels__vumzz, bqlp__dzqvx


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    tce__anbhg = sort_node.in_vars[0].name
    lzroh__kikhj = sort_node.out_vars[0].name
    olhx__erefy, qcsw__dotub, smnhc__yvhxo = block_use_map[tce__anbhg]
    if qcsw__dotub or smnhc__yvhxo:
        return
    gqua__cain, ffz__nxvcs, ove__ykqql = _compute_table_column_uses(
        lzroh__kikhj, table_col_use_map, equiv_vars)
    hwwjs__rdoak = set(glx__dxj for glx__dxj in sort_node.key_inds if 
        glx__dxj < sort_node.num_table_arrays)
    block_use_map[tce__anbhg] = (olhx__erefy | gqua__cain | hwwjs__rdoak, 
        ffz__nxvcs or ove__ykqql, False)


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    mgqc__rmy = sort_node.num_table_arrays
    lzroh__kikhj = sort_node.out_vars[0].name
    rxks__wtbkz = _find_used_columns(lzroh__kikhj, mgqc__rmy,
        column_live_map, equiv_vars)
    if rxks__wtbkz is None:
        return False
    nfq__gqh = set(range(mgqc__rmy)) - rxks__wtbkz
    hwwjs__rdoak = set(glx__dxj for glx__dxj in sort_node.key_inds if 
        glx__dxj < mgqc__rmy)
    xme__draq = sort_node.dead_key_var_inds | nfq__gqh & hwwjs__rdoak
    bgn__rgph = sort_node.dead_var_inds | nfq__gqh - hwwjs__rdoak
    jfl__ares = (xme__draq != sort_node.dead_key_var_inds) | (bgn__rgph !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = xme__draq
    sort_node.dead_var_inds = bgn__rgph
    return jfl__ares


remove_dead_column_extensions[Sort] = sort_remove_dead_column
