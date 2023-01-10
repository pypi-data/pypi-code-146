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
            self.na_position_b = tuple([(True if gfh__bmrm == 'last' else 
                False) for gfh__bmrm in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [kyma__tindn for kyma__tindn in self.in_vars if kyma__tindn
             is not None]

    def get_live_out_vars(self):
        return [kyma__tindn for kyma__tindn in self.out_vars if kyma__tindn
             is not None]

    def __repr__(self):
        taz__vhw = ', '.join(kyma__tindn.name for kyma__tindn in self.
            get_live_in_vars())
        veza__axxx = f'{self.df_in}{{{taz__vhw}}}'
        ysgku__jwx = ', '.join(kyma__tindn.name for kyma__tindn in self.
            get_live_out_vars())
        pyr__mflri = f'{self.df_out}{{{ysgku__jwx}}}'
        return f'Sort (keys: {self.key_inds}): {veza__axxx} {pyr__mflri}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    baaxf__ztja = []
    for gudw__aspv in sort_node.get_live_in_vars():
        dbwhz__tox = equiv_set.get_shape(gudw__aspv)
        if dbwhz__tox is not None:
            baaxf__ztja.append(dbwhz__tox[0])
    if len(baaxf__ztja) > 1:
        equiv_set.insert_equiv(*baaxf__ztja)
    gmn__ofpjv = []
    baaxf__ztja = []
    for gudw__aspv in sort_node.get_live_out_vars():
        noh__omauw = typemap[gudw__aspv.name]
        qqtt__zux = array_analysis._gen_shape_call(equiv_set, gudw__aspv,
            noh__omauw.ndim, None, gmn__ofpjv)
        equiv_set.insert_equiv(gudw__aspv, qqtt__zux)
        baaxf__ztja.append(qqtt__zux[0])
        equiv_set.define(gudw__aspv, set())
    if len(baaxf__ztja) > 1:
        equiv_set.insert_equiv(*baaxf__ztja)
    return [], gmn__ofpjv


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    fmnj__kjjo = sort_node.get_live_in_vars()
    ucg__ymkxl = sort_node.get_live_out_vars()
    lviza__jwg = Distribution.OneD
    for gudw__aspv in fmnj__kjjo:
        lviza__jwg = Distribution(min(lviza__jwg.value, array_dists[
            gudw__aspv.name].value))
    gvn__eunvu = Distribution(min(lviza__jwg.value, Distribution.OneD_Var.
        value))
    for gudw__aspv in ucg__ymkxl:
        if gudw__aspv.name in array_dists:
            gvn__eunvu = Distribution(min(gvn__eunvu.value, array_dists[
                gudw__aspv.name].value))
    if gvn__eunvu != Distribution.OneD_Var:
        lviza__jwg = gvn__eunvu
    for gudw__aspv in fmnj__kjjo:
        array_dists[gudw__aspv.name] = lviza__jwg
    for gudw__aspv in ucg__ymkxl:
        array_dists[gudw__aspv.name] = gvn__eunvu


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for rrkc__ohxca, cvdj__bsahj in enumerate(sort_node.out_vars):
        ultfs__ighrj = sort_node.in_vars[rrkc__ohxca]
        if ultfs__ighrj is not None and cvdj__bsahj is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=
                cvdj__bsahj.name, src=ultfs__ighrj.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for gudw__aspv in sort_node.get_live_out_vars():
            definitions[gudw__aspv.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for rrkc__ohxca in range(len(sort_node.in_vars)):
        if sort_node.in_vars[rrkc__ohxca] is not None:
            sort_node.in_vars[rrkc__ohxca] = visit_vars_inner(sort_node.
                in_vars[rrkc__ohxca], callback, cbdata)
        if sort_node.out_vars[rrkc__ohxca] is not None:
            sort_node.out_vars[rrkc__ohxca] = visit_vars_inner(sort_node.
                out_vars[rrkc__ohxca], callback, cbdata)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = visit_vars_inner(sort_node.
            _bodo_chunk_bounds, callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        fyf__kqf = sort_node.out_vars[0]
        if fyf__kqf is not None and fyf__kqf.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            wcpv__geyk = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & wcpv__geyk)
            sort_node.dead_var_inds.update(dead_cols - wcpv__geyk)
            if len(wcpv__geyk & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for rrkc__ohxca in range(1, len(sort_node.out_vars)):
            kyma__tindn = sort_node.out_vars[rrkc__ohxca]
            if kyma__tindn is not None and kyma__tindn.name not in lives:
                sort_node.out_vars[rrkc__ohxca] = None
                gqc__uvf = sort_node.num_table_arrays + rrkc__ohxca - 1
                if gqc__uvf in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(gqc__uvf)
                else:
                    sort_node.dead_var_inds.add(gqc__uvf)
                    sort_node.in_vars[rrkc__ohxca] = None
    else:
        for rrkc__ohxca in range(len(sort_node.out_vars)):
            kyma__tindn = sort_node.out_vars[rrkc__ohxca]
            if kyma__tindn is not None and kyma__tindn.name not in lives:
                sort_node.out_vars[rrkc__ohxca] = None
                if rrkc__ohxca in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(rrkc__ohxca)
                else:
                    sort_node.dead_var_inds.add(rrkc__ohxca)
                    sort_node.in_vars[rrkc__ohxca] = None
    if all(kyma__tindn is None for kyma__tindn in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({kyma__tindn.name for kyma__tindn in sort_node.
        get_live_in_vars()})
    if not sort_node.inplace:
        def_set.update({kyma__tindn.name for kyma__tindn in sort_node.
            get_live_out_vars()})
    if sort_node._bodo_chunk_bounds is not None:
        use_set.add(sort_node._bodo_chunk_bounds.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    hft__oiu = set()
    if not sort_node.inplace:
        hft__oiu.update({kyma__tindn.name for kyma__tindn in sort_node.
            get_live_out_vars()})
    return set(), hft__oiu


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for rrkc__ohxca in range(len(sort_node.in_vars)):
        if sort_node.in_vars[rrkc__ohxca] is not None:
            sort_node.in_vars[rrkc__ohxca] = replace_vars_inner(sort_node.
                in_vars[rrkc__ohxca], var_dict)
        if sort_node.out_vars[rrkc__ohxca] is not None:
            sort_node.out_vars[rrkc__ohxca] = replace_vars_inner(sort_node.
                out_vars[rrkc__ohxca], var_dict)
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
        for kyma__tindn in (in_vars + out_vars):
            if array_dists[kyma__tindn.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                kyma__tindn.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        qzi__lcw = []
        for kyma__tindn in in_vars:
            rdti__xybxa = _copy_array_nodes(kyma__tindn, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            qzi__lcw.append(rdti__xybxa)
        in_vars = qzi__lcw
    out_types = [(typemap[kyma__tindn.name] if kyma__tindn is not None else
        types.none) for kyma__tindn in sort_node.out_vars]
    urby__osir, idoi__qyuh = get_sort_cpp_section(sort_node, out_types,
        typemap, parallel)
    vwxiz__rehla = {}
    exec(urby__osir, {}, vwxiz__rehla)
    cqbcf__bqt = vwxiz__rehla['f']
    idoi__qyuh.update({'bodo': bodo, 'np': np, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'sort_values_table': sort_values_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'array_to_info': array_to_info,
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    idoi__qyuh.update({f'out_type{rrkc__ohxca}': out_types[rrkc__ohxca] for
        rrkc__ohxca in range(len(out_types))})
    hvg__cop = sort_node._bodo_chunk_bounds
    bvtf__efd = hvg__cop
    if hvg__cop is None:
        loc = sort_node.loc
        bvtf__efd = ir.Var(ir.Scope(None, loc), mk_unique_var(
            '$bounds_none'), loc)
        typemap[bvtf__efd.name] = types.none
        nodes.append(ir.Assign(ir.Const(None, loc), bvtf__efd, loc))
    obc__rszez = compile_to_numba_ir(cqbcf__bqt, idoi__qyuh, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[kyma__tindn.
        name] for kyma__tindn in in_vars) + (typemap[bvtf__efd.name],),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(obc__rszez, in_vars + [bvtf__efd])
    ihid__hghv = obc__rszez.body[-2].value.value
    nodes += obc__rszez.body[:-2]
    for rrkc__ohxca, kyma__tindn in enumerate(out_vars):
        gen_getitem(kyma__tindn, ihid__hghv, rrkc__ohxca, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    uwlyx__ctrnu = lambda arr: arr.copy()
    rile__aqo = None
    if isinstance(typemap[var.name], TableType):
        vkdl__rxao = len(typemap[var.name].arr_types)
        rile__aqo = set(range(vkdl__rxao)) - dead_cols
        rile__aqo = MetaType(tuple(sorted(rile__aqo)))
        uwlyx__ctrnu = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    obc__rszez = compile_to_numba_ir(uwlyx__ctrnu, {'bodo': bodo, 'types':
        types, '_used_columns': rile__aqo}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(obc__rszez, [var])
    nodes += obc__rszez.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, typemap, parallel):
    lhuz__xgiic = len(sort_node.key_inds)
    ctv__osbt = len(sort_node.in_vars)
    fuqm__dtlu = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + ctv__osbt - 1 if sort_node.
        is_table_format else ctv__osbt)
    ypd__zryf, rix__lgg, jssf__rwcr = _get_cpp_col_ind_mappings(sort_node.
        key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols)
    gyc__jab = []
    if sort_node.is_table_format:
        gyc__jab.append('arg0')
        for rrkc__ohxca in range(1, ctv__osbt):
            gqc__uvf = sort_node.num_table_arrays + rrkc__ohxca - 1
            if gqc__uvf not in sort_node.dead_var_inds:
                gyc__jab.append(f'arg{gqc__uvf}')
    else:
        for rrkc__ohxca in range(n_cols):
            if rrkc__ohxca not in sort_node.dead_var_inds:
                gyc__jab.append(f'arg{rrkc__ohxca}')
    urby__osir = f"def f({', '.join(gyc__jab)}, bounds_in):\n"
    if sort_node.is_table_format:
        momf__yedau = ',' if ctv__osbt - 1 == 1 else ''
        ubby__sdw = []
        for rrkc__ohxca in range(sort_node.num_table_arrays, n_cols):
            if rrkc__ohxca in sort_node.dead_var_inds:
                ubby__sdw.append('None')
            else:
                ubby__sdw.append(f'arg{rrkc__ohxca}')
        urby__osir += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(ubby__sdw)}{momf__yedau}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        rtp__tkov = {bkp__qfh: rrkc__ohxca for rrkc__ohxca, bkp__qfh in
            enumerate(ypd__zryf)}
        xfrbw__ovk = [None] * len(ypd__zryf)
        for rrkc__ohxca in range(n_cols):
            svrr__dhp = rtp__tkov.get(rrkc__ohxca, -1)
            if svrr__dhp != -1:
                xfrbw__ovk[svrr__dhp] = f'array_to_info(arg{rrkc__ohxca})'
        urby__osir += '  info_list_total = [{}]\n'.format(','.join(xfrbw__ovk))
        urby__osir += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    urby__osir += '  vect_ascending = np.array([{}], np.int64)\n'.format(','
        .join('1' if qjo__ifl else '0' for qjo__ifl in sort_node.
        ascending_list))
    urby__osir += '  na_position = np.array([{}], np.int64)\n'.format(','.
        join('1' if qjo__ifl else '0' for qjo__ifl in sort_node.na_position_b))
    urby__osir += '  dead_keys = np.array([{}], np.int64)\n'.format(','.
        join('1' if rrkc__ohxca in jssf__rwcr else '0' for rrkc__ohxca in
        range(lhuz__xgiic)))
    urby__osir += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    omydf__wnqa = sort_node._bodo_chunk_bounds
    jxt__rfu = '0' if omydf__wnqa is None or is_overload_none(typemap[
        omydf__wnqa.name]
        ) else 'arr_info_list_to_table([array_to_info(bounds_in)])'
    urby__osir += f"""  out_cpp_table = sort_values_table(in_cpp_table, {lhuz__xgiic}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {jxt__rfu}, {parallel})
"""
    if sort_node.is_table_format:
        momf__yedau = ',' if fuqm__dtlu == 1 else ''
        eisht__cgxd = (
            f"({', '.join(f'out_type{rrkc__ohxca}' if not type_has_unknown_cats(out_types[rrkc__ohxca]) else f'arg{rrkc__ohxca}' for rrkc__ohxca in range(fuqm__dtlu))}{momf__yedau})"
            )
        urby__osir += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {eisht__cgxd}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        rtp__tkov = {bkp__qfh: rrkc__ohxca for rrkc__ohxca, bkp__qfh in
            enumerate(rix__lgg)}
        xfrbw__ovk = []
        for rrkc__ohxca in range(n_cols):
            svrr__dhp = rtp__tkov.get(rrkc__ohxca, -1)
            if svrr__dhp != -1:
                ccwt__mqzt = (f'out_type{rrkc__ohxca}' if not
                    type_has_unknown_cats(out_types[rrkc__ohxca]) else
                    f'arg{rrkc__ohxca}')
                urby__osir += f"""  out{rrkc__ohxca} = info_to_array(info_from_table(out_cpp_table, {svrr__dhp}), {ccwt__mqzt})
"""
                xfrbw__ovk.append(f'out{rrkc__ohxca}')
        momf__yedau = ',' if len(xfrbw__ovk) == 1 else ''
        xfrt__lfego = f"({', '.join(xfrbw__ovk)}{momf__yedau})"
        urby__osir += f'  out_data = {xfrt__lfego}\n'
    urby__osir += '  delete_table(out_cpp_table)\n'
    urby__osir += '  delete_table(in_cpp_table)\n'
    urby__osir += f'  return out_data\n'
    return urby__osir, {'in_col_inds': MetaType(tuple(ypd__zryf)),
        'out_col_inds': MetaType(tuple(rix__lgg))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    ypd__zryf = []
    rix__lgg = []
    jssf__rwcr = []
    for bkp__qfh, rrkc__ohxca in enumerate(key_inds):
        ypd__zryf.append(rrkc__ohxca)
        if rrkc__ohxca in dead_key_var_inds:
            jssf__rwcr.append(bkp__qfh)
        else:
            rix__lgg.append(rrkc__ohxca)
    for rrkc__ohxca in range(n_cols):
        if rrkc__ohxca in dead_var_inds or rrkc__ohxca in key_inds:
            continue
        ypd__zryf.append(rrkc__ohxca)
        rix__lgg.append(rrkc__ohxca)
    return ypd__zryf, rix__lgg, jssf__rwcr


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    mldp__aqij = sort_node.in_vars[0].name
    cha__grb = sort_node.out_vars[0].name
    trx__doqpb, adie__ixh, lsw__bdutw = block_use_map[mldp__aqij]
    if adie__ixh or lsw__bdutw:
        return
    bcl__esh, vqa__kqzur, btjix__qzfs = _compute_table_column_uses(cha__grb,
        table_col_use_map, equiv_vars)
    mzoe__ztaid = set(rrkc__ohxca for rrkc__ohxca in sort_node.key_inds if 
        rrkc__ohxca < sort_node.num_table_arrays)
    block_use_map[mldp__aqij
        ] = trx__doqpb | bcl__esh | mzoe__ztaid, vqa__kqzur or btjix__qzfs, False


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    vkdl__rxao = sort_node.num_table_arrays
    cha__grb = sort_node.out_vars[0].name
    rile__aqo = _find_used_columns(cha__grb, vkdl__rxao, column_live_map,
        equiv_vars)
    if rile__aqo is None:
        return False
    sax__kix = set(range(vkdl__rxao)) - rile__aqo
    mzoe__ztaid = set(rrkc__ohxca for rrkc__ohxca in sort_node.key_inds if 
        rrkc__ohxca < vkdl__rxao)
    xkab__sijyo = sort_node.dead_key_var_inds | sax__kix & mzoe__ztaid
    keubh__apeo = sort_node.dead_var_inds | sax__kix - mzoe__ztaid
    owkq__kfgw = (xkab__sijyo != sort_node.dead_key_var_inds) | (keubh__apeo !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = xkab__sijyo
    sort_node.dead_var_inds = keubh__apeo
    return owkq__kfgw


remove_dead_column_extensions[Sort] = sort_remove_dead_column
