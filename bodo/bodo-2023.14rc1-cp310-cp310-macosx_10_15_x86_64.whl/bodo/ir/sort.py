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
            self.na_position_b = tuple([(True if uakhl__qxvg == 'last' else
                False) for uakhl__qxvg in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [che__cojnh for che__cojnh in self.in_vars if che__cojnh is not
            None]

    def get_live_out_vars(self):
        return [che__cojnh for che__cojnh in self.out_vars if che__cojnh is not
            None]

    def __repr__(self):
        qrlf__voy = ', '.join(che__cojnh.name for che__cojnh in self.
            get_live_in_vars())
        cqsw__ocyjx = f'{self.df_in}{{{qrlf__voy}}}'
        qjh__jnb = ', '.join(che__cojnh.name for che__cojnh in self.
            get_live_out_vars())
        moab__orxh = f'{self.df_out}{{{qjh__jnb}}}'
        return f'Sort (keys: {self.key_inds}): {cqsw__ocyjx} {moab__orxh}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    droa__meod = []
    for pax__mke in sort_node.get_live_in_vars():
        twgw__rkg = equiv_set.get_shape(pax__mke)
        if twgw__rkg is not None:
            droa__meod.append(twgw__rkg[0])
    if len(droa__meod) > 1:
        equiv_set.insert_equiv(*droa__meod)
    now__vyh = []
    droa__meod = []
    for pax__mke in sort_node.get_live_out_vars():
        uula__spxi = typemap[pax__mke.name]
        bmrad__gqq = array_analysis._gen_shape_call(equiv_set, pax__mke,
            uula__spxi.ndim, None, now__vyh)
        equiv_set.insert_equiv(pax__mke, bmrad__gqq)
        droa__meod.append(bmrad__gqq[0])
        equiv_set.define(pax__mke, set())
    if len(droa__meod) > 1:
        equiv_set.insert_equiv(*droa__meod)
    return [], now__vyh


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    qqvgp__hmt = sort_node.get_live_in_vars()
    qtvvx__pgi = sort_node.get_live_out_vars()
    pntxf__rxvrq = Distribution.OneD
    for pax__mke in qqvgp__hmt:
        pntxf__rxvrq = Distribution(min(pntxf__rxvrq.value, array_dists[
            pax__mke.name].value))
    kdavd__moda = Distribution(min(pntxf__rxvrq.value, Distribution.
        OneD_Var.value))
    for pax__mke in qtvvx__pgi:
        if pax__mke.name in array_dists:
            kdavd__moda = Distribution(min(kdavd__moda.value, array_dists[
                pax__mke.name].value))
    if kdavd__moda != Distribution.OneD_Var:
        pntxf__rxvrq = kdavd__moda
    for pax__mke in qqvgp__hmt:
        array_dists[pax__mke.name] = pntxf__rxvrq
    for pax__mke in qtvvx__pgi:
        array_dists[pax__mke.name] = kdavd__moda


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for jvabo__huri, kcrwl__tmr in enumerate(sort_node.out_vars):
        cwmev__bvi = sort_node.in_vars[jvabo__huri]
        if cwmev__bvi is not None and kcrwl__tmr is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=
                kcrwl__tmr.name, src=cwmev__bvi.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for pax__mke in sort_node.get_live_out_vars():
            definitions[pax__mke.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for jvabo__huri in range(len(sort_node.in_vars)):
        if sort_node.in_vars[jvabo__huri] is not None:
            sort_node.in_vars[jvabo__huri] = visit_vars_inner(sort_node.
                in_vars[jvabo__huri], callback, cbdata)
        if sort_node.out_vars[jvabo__huri] is not None:
            sort_node.out_vars[jvabo__huri] = visit_vars_inner(sort_node.
                out_vars[jvabo__huri], callback, cbdata)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = visit_vars_inner(sort_node.
            _bodo_chunk_bounds, callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        czfyw__vdshe = sort_node.out_vars[0]
        if czfyw__vdshe is not None and czfyw__vdshe.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            aqr__dli = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & aqr__dli)
            sort_node.dead_var_inds.update(dead_cols - aqr__dli)
            if len(aqr__dli & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for jvabo__huri in range(1, len(sort_node.out_vars)):
            che__cojnh = sort_node.out_vars[jvabo__huri]
            if che__cojnh is not None and che__cojnh.name not in lives:
                sort_node.out_vars[jvabo__huri] = None
                kwf__steep = sort_node.num_table_arrays + jvabo__huri - 1
                if kwf__steep in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(kwf__steep)
                else:
                    sort_node.dead_var_inds.add(kwf__steep)
                    sort_node.in_vars[jvabo__huri] = None
    else:
        for jvabo__huri in range(len(sort_node.out_vars)):
            che__cojnh = sort_node.out_vars[jvabo__huri]
            if che__cojnh is not None and che__cojnh.name not in lives:
                sort_node.out_vars[jvabo__huri] = None
                if jvabo__huri in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(jvabo__huri)
                else:
                    sort_node.dead_var_inds.add(jvabo__huri)
                    sort_node.in_vars[jvabo__huri] = None
    if all(che__cojnh is None for che__cojnh in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({che__cojnh.name for che__cojnh in sort_node.
        get_live_in_vars()})
    if not sort_node.inplace:
        def_set.update({che__cojnh.name for che__cojnh in sort_node.
            get_live_out_vars()})
    if sort_node._bodo_chunk_bounds is not None:
        use_set.add(sort_node._bodo_chunk_bounds.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    pgoxt__nmo = set()
    if not sort_node.inplace:
        pgoxt__nmo.update({che__cojnh.name for che__cojnh in sort_node.
            get_live_out_vars()})
    return set(), pgoxt__nmo


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for jvabo__huri in range(len(sort_node.in_vars)):
        if sort_node.in_vars[jvabo__huri] is not None:
            sort_node.in_vars[jvabo__huri] = replace_vars_inner(sort_node.
                in_vars[jvabo__huri], var_dict)
        if sort_node.out_vars[jvabo__huri] is not None:
            sort_node.out_vars[jvabo__huri] = replace_vars_inner(sort_node.
                out_vars[jvabo__huri], var_dict)
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
        for che__cojnh in (in_vars + out_vars):
            if array_dists[che__cojnh.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                che__cojnh.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        zvhp__qexy = []
        for che__cojnh in in_vars:
            ldkbh__qjq = _copy_array_nodes(che__cojnh, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            zvhp__qexy.append(ldkbh__qjq)
        in_vars = zvhp__qexy
    out_types = [(typemap[che__cojnh.name] if che__cojnh is not None else
        types.none) for che__cojnh in sort_node.out_vars]
    ehuu__mvz, wanx__ijm = get_sort_cpp_section(sort_node, out_types,
        typemap, parallel)
    yzss__gnrp = {}
    exec(ehuu__mvz, {}, yzss__gnrp)
    vbqb__vzig = yzss__gnrp['f']
    wanx__ijm.update({'bodo': bodo, 'np': np, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'sort_values_table': sort_values_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'array_to_info': array_to_info,
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    wanx__ijm.update({f'out_type{jvabo__huri}': out_types[jvabo__huri] for
        jvabo__huri in range(len(out_types))})
    tos__wgtk = sort_node._bodo_chunk_bounds
    xuv__imvu = tos__wgtk
    if tos__wgtk is None:
        loc = sort_node.loc
        xuv__imvu = ir.Var(ir.Scope(None, loc), mk_unique_var(
            '$bounds_none'), loc)
        typemap[xuv__imvu.name] = types.none
        nodes.append(ir.Assign(ir.Const(None, loc), xuv__imvu, loc))
    bhau__jxy = compile_to_numba_ir(vbqb__vzig, wanx__ijm, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[che__cojnh.
        name] for che__cojnh in in_vars) + (typemap[xuv__imvu.name],),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(bhau__jxy, in_vars + [xuv__imvu])
    kgzod__vclhz = bhau__jxy.body[-2].value.value
    nodes += bhau__jxy.body[:-2]
    for jvabo__huri, che__cojnh in enumerate(out_vars):
        gen_getitem(che__cojnh, kgzod__vclhz, jvabo__huri, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    mzx__ktzfy = lambda arr: arr.copy()
    fedq__qoi = None
    if isinstance(typemap[var.name], TableType):
        qexuq__fhra = len(typemap[var.name].arr_types)
        fedq__qoi = set(range(qexuq__fhra)) - dead_cols
        fedq__qoi = MetaType(tuple(sorted(fedq__qoi)))
        mzx__ktzfy = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    bhau__jxy = compile_to_numba_ir(mzx__ktzfy, {'bodo': bodo, 'types':
        types, '_used_columns': fedq__qoi}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(bhau__jxy, [var])
    nodes += bhau__jxy.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, typemap, parallel):
    qrz__yckf = len(sort_node.key_inds)
    wae__wlv = len(sort_node.in_vars)
    eyqr__ypnw = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + wae__wlv - 1 if sort_node.
        is_table_format else wae__wlv)
    lylh__skbm, cxjq__aivo, nndff__bqwb = _get_cpp_col_ind_mappings(sort_node
        .key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols
        )
    qoy__qai = []
    if sort_node.is_table_format:
        qoy__qai.append('arg0')
        for jvabo__huri in range(1, wae__wlv):
            kwf__steep = sort_node.num_table_arrays + jvabo__huri - 1
            if kwf__steep not in sort_node.dead_var_inds:
                qoy__qai.append(f'arg{kwf__steep}')
    else:
        for jvabo__huri in range(n_cols):
            if jvabo__huri not in sort_node.dead_var_inds:
                qoy__qai.append(f'arg{jvabo__huri}')
    ehuu__mvz = f"def f({', '.join(qoy__qai)}, bounds_in):\n"
    if sort_node.is_table_format:
        qgghz__iso = ',' if wae__wlv - 1 == 1 else ''
        xkar__ckh = []
        for jvabo__huri in range(sort_node.num_table_arrays, n_cols):
            if jvabo__huri in sort_node.dead_var_inds:
                xkar__ckh.append('None')
            else:
                xkar__ckh.append(f'arg{jvabo__huri}')
        ehuu__mvz += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(xkar__ckh)}{qgghz__iso}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        izhz__rstl = {ihsb__pyt: jvabo__huri for jvabo__huri, ihsb__pyt in
            enumerate(lylh__skbm)}
        alepc__uwwj = [None] * len(lylh__skbm)
        for jvabo__huri in range(n_cols):
            grj__hfsyc = izhz__rstl.get(jvabo__huri, -1)
            if grj__hfsyc != -1:
                alepc__uwwj[grj__hfsyc] = f'array_to_info(arg{jvabo__huri})'
        ehuu__mvz += '  info_list_total = [{}]\n'.format(','.join(alepc__uwwj))
        ehuu__mvz += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    ehuu__mvz += '  vect_ascending = np.array([{}], np.int64)\n'.format(','
        .join('1' if ngyx__bqgo else '0' for ngyx__bqgo in sort_node.
        ascending_list))
    ehuu__mvz += '  na_position = np.array([{}], np.int64)\n'.format(','.
        join('1' if ngyx__bqgo else '0' for ngyx__bqgo in sort_node.
        na_position_b))
    ehuu__mvz += '  dead_keys = np.array([{}], np.int64)\n'.format(','.join
        ('1' if jvabo__huri in nndff__bqwb else '0' for jvabo__huri in
        range(qrz__yckf)))
    ehuu__mvz += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    rbfv__mhy = sort_node._bodo_chunk_bounds
    hbyg__qant = '0' if rbfv__mhy is None or is_overload_none(typemap[
        rbfv__mhy.name]
        ) else 'arr_info_list_to_table([array_to_info(bounds_in)])'
    ehuu__mvz += f"""  out_cpp_table = sort_values_table(in_cpp_table, {qrz__yckf}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {hbyg__qant}, {parallel})
"""
    if sort_node.is_table_format:
        qgghz__iso = ',' if eyqr__ypnw == 1 else ''
        nai__vyh = (
            f"({', '.join(f'out_type{jvabo__huri}' if not type_has_unknown_cats(out_types[jvabo__huri]) else f'arg{jvabo__huri}' for jvabo__huri in range(eyqr__ypnw))}{qgghz__iso})"
            )
        ehuu__mvz += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {nai__vyh}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        izhz__rstl = {ihsb__pyt: jvabo__huri for jvabo__huri, ihsb__pyt in
            enumerate(cxjq__aivo)}
        alepc__uwwj = []
        for jvabo__huri in range(n_cols):
            grj__hfsyc = izhz__rstl.get(jvabo__huri, -1)
            if grj__hfsyc != -1:
                uvms__uuot = (f'out_type{jvabo__huri}' if not
                    type_has_unknown_cats(out_types[jvabo__huri]) else
                    f'arg{jvabo__huri}')
                ehuu__mvz += f"""  out{jvabo__huri} = info_to_array(info_from_table(out_cpp_table, {grj__hfsyc}), {uvms__uuot})
"""
                alepc__uwwj.append(f'out{jvabo__huri}')
        qgghz__iso = ',' if len(alepc__uwwj) == 1 else ''
        looti__adfxo = f"({', '.join(alepc__uwwj)}{qgghz__iso})"
        ehuu__mvz += f'  out_data = {looti__adfxo}\n'
    ehuu__mvz += '  delete_table(out_cpp_table)\n'
    ehuu__mvz += '  delete_table(in_cpp_table)\n'
    ehuu__mvz += f'  return out_data\n'
    return ehuu__mvz, {'in_col_inds': MetaType(tuple(lylh__skbm)),
        'out_col_inds': MetaType(tuple(cxjq__aivo))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    lylh__skbm = []
    cxjq__aivo = []
    nndff__bqwb = []
    for ihsb__pyt, jvabo__huri in enumerate(key_inds):
        lylh__skbm.append(jvabo__huri)
        if jvabo__huri in dead_key_var_inds:
            nndff__bqwb.append(ihsb__pyt)
        else:
            cxjq__aivo.append(jvabo__huri)
    for jvabo__huri in range(n_cols):
        if jvabo__huri in dead_var_inds or jvabo__huri in key_inds:
            continue
        lylh__skbm.append(jvabo__huri)
        cxjq__aivo.append(jvabo__huri)
    return lylh__skbm, cxjq__aivo, nndff__bqwb


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    lhdmh__klub = sort_node.in_vars[0].name
    vpaba__vft = sort_node.out_vars[0].name
    dhb__fuor, wzsi__dgfpy, kyxx__cdu = block_use_map[lhdmh__klub]
    if wzsi__dgfpy or kyxx__cdu:
        return
    tmr__krn, ejg__lipde, irfdr__jqll = _compute_table_column_uses(vpaba__vft,
        table_col_use_map, equiv_vars)
    oemsw__olikr = set(jvabo__huri for jvabo__huri in sort_node.key_inds if
        jvabo__huri < sort_node.num_table_arrays)
    block_use_map[lhdmh__klub
        ] = dhb__fuor | tmr__krn | oemsw__olikr, ejg__lipde or irfdr__jqll, False


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    qexuq__fhra = sort_node.num_table_arrays
    vpaba__vft = sort_node.out_vars[0].name
    fedq__qoi = _find_used_columns(vpaba__vft, qexuq__fhra, column_live_map,
        equiv_vars)
    if fedq__qoi is None:
        return False
    jlvcc__nlwhv = set(range(qexuq__fhra)) - fedq__qoi
    oemsw__olikr = set(jvabo__huri for jvabo__huri in sort_node.key_inds if
        jvabo__huri < qexuq__fhra)
    vzi__hig = sort_node.dead_key_var_inds | jlvcc__nlwhv & oemsw__olikr
    rbv__yis = sort_node.dead_var_inds | jlvcc__nlwhv - oemsw__olikr
    btzif__eiehl = (vzi__hig != sort_node.dead_key_var_inds) | (rbv__yis !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = vzi__hig
    sort_node.dead_var_inds = rbv__yis
    return btzif__eiehl


remove_dead_column_extensions[Sort] = sort_remove_dead_column
