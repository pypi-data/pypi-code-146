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
            self.na_position_b = tuple([(True if szxld__vwivr == 'last' else
                False) for szxld__vwivr in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [tgmvs__hoylp for tgmvs__hoylp in self.in_vars if 
            tgmvs__hoylp is not None]

    def get_live_out_vars(self):
        return [tgmvs__hoylp for tgmvs__hoylp in self.out_vars if 
            tgmvs__hoylp is not None]

    def __repr__(self):
        ocj__pqzj = ', '.join(tgmvs__hoylp.name for tgmvs__hoylp in self.
            get_live_in_vars())
        zymh__haha = f'{self.df_in}{{{ocj__pqzj}}}'
        iruw__cro = ', '.join(tgmvs__hoylp.name for tgmvs__hoylp in self.
            get_live_out_vars())
        apflr__xjub = f'{self.df_out}{{{iruw__cro}}}'
        return f'Sort (keys: {self.key_inds}): {zymh__haha} {apflr__xjub}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    ukrr__jkek = []
    for yglbp__cxuuj in sort_node.get_live_in_vars():
        mfg__trb = equiv_set.get_shape(yglbp__cxuuj)
        if mfg__trb is not None:
            ukrr__jkek.append(mfg__trb[0])
    if len(ukrr__jkek) > 1:
        equiv_set.insert_equiv(*ukrr__jkek)
    uzkae__pkmw = []
    ukrr__jkek = []
    for yglbp__cxuuj in sort_node.get_live_out_vars():
        jioc__wvtyb = typemap[yglbp__cxuuj.name]
        czxzl__uookj = array_analysis._gen_shape_call(equiv_set,
            yglbp__cxuuj, jioc__wvtyb.ndim, None, uzkae__pkmw)
        equiv_set.insert_equiv(yglbp__cxuuj, czxzl__uookj)
        ukrr__jkek.append(czxzl__uookj[0])
        equiv_set.define(yglbp__cxuuj, set())
    if len(ukrr__jkek) > 1:
        equiv_set.insert_equiv(*ukrr__jkek)
    return [], uzkae__pkmw


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    knjn__jeb = sort_node.get_live_in_vars()
    lmza__gjjr = sort_node.get_live_out_vars()
    tsr__oiif = Distribution.OneD
    for yglbp__cxuuj in knjn__jeb:
        tsr__oiif = Distribution(min(tsr__oiif.value, array_dists[
            yglbp__cxuuj.name].value))
    qpa__wkyl = Distribution(min(tsr__oiif.value, Distribution.OneD_Var.value))
    for yglbp__cxuuj in lmza__gjjr:
        if yglbp__cxuuj.name in array_dists:
            qpa__wkyl = Distribution(min(qpa__wkyl.value, array_dists[
                yglbp__cxuuj.name].value))
    if qpa__wkyl != Distribution.OneD_Var:
        tsr__oiif = qpa__wkyl
    for yglbp__cxuuj in knjn__jeb:
        array_dists[yglbp__cxuuj.name] = tsr__oiif
    for yglbp__cxuuj in lmza__gjjr:
        array_dists[yglbp__cxuuj.name] = qpa__wkyl


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for gdl__cnmhn, gji__hcdi in enumerate(sort_node.out_vars):
        cifnb__foiho = sort_node.in_vars[gdl__cnmhn]
        if cifnb__foiho is not None and gji__hcdi is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=
                gji__hcdi.name, src=cifnb__foiho.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for yglbp__cxuuj in sort_node.get_live_out_vars():
            definitions[yglbp__cxuuj.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for gdl__cnmhn in range(len(sort_node.in_vars)):
        if sort_node.in_vars[gdl__cnmhn] is not None:
            sort_node.in_vars[gdl__cnmhn] = visit_vars_inner(sort_node.
                in_vars[gdl__cnmhn], callback, cbdata)
        if sort_node.out_vars[gdl__cnmhn] is not None:
            sort_node.out_vars[gdl__cnmhn] = visit_vars_inner(sort_node.
                out_vars[gdl__cnmhn], callback, cbdata)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = visit_vars_inner(sort_node.
            _bodo_chunk_bounds, callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        isbpc__fti = sort_node.out_vars[0]
        if isbpc__fti is not None and isbpc__fti.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            jfk__gteqg = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & jfk__gteqg)
            sort_node.dead_var_inds.update(dead_cols - jfk__gteqg)
            if len(jfk__gteqg & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for gdl__cnmhn in range(1, len(sort_node.out_vars)):
            tgmvs__hoylp = sort_node.out_vars[gdl__cnmhn]
            if tgmvs__hoylp is not None and tgmvs__hoylp.name not in lives:
                sort_node.out_vars[gdl__cnmhn] = None
                acp__oxw = sort_node.num_table_arrays + gdl__cnmhn - 1
                if acp__oxw in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(acp__oxw)
                else:
                    sort_node.dead_var_inds.add(acp__oxw)
                    sort_node.in_vars[gdl__cnmhn] = None
    else:
        for gdl__cnmhn in range(len(sort_node.out_vars)):
            tgmvs__hoylp = sort_node.out_vars[gdl__cnmhn]
            if tgmvs__hoylp is not None and tgmvs__hoylp.name not in lives:
                sort_node.out_vars[gdl__cnmhn] = None
                if gdl__cnmhn in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(gdl__cnmhn)
                else:
                    sort_node.dead_var_inds.add(gdl__cnmhn)
                    sort_node.in_vars[gdl__cnmhn] = None
    if all(tgmvs__hoylp is None for tgmvs__hoylp in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({tgmvs__hoylp.name for tgmvs__hoylp in sort_node.
        get_live_in_vars()})
    if not sort_node.inplace:
        def_set.update({tgmvs__hoylp.name for tgmvs__hoylp in sort_node.
            get_live_out_vars()})
    if sort_node._bodo_chunk_bounds is not None:
        use_set.add(sort_node._bodo_chunk_bounds.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    rgw__rxrwm = set()
    if not sort_node.inplace:
        rgw__rxrwm.update({tgmvs__hoylp.name for tgmvs__hoylp in sort_node.
            get_live_out_vars()})
    return set(), rgw__rxrwm


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for gdl__cnmhn in range(len(sort_node.in_vars)):
        if sort_node.in_vars[gdl__cnmhn] is not None:
            sort_node.in_vars[gdl__cnmhn] = replace_vars_inner(sort_node.
                in_vars[gdl__cnmhn], var_dict)
        if sort_node.out_vars[gdl__cnmhn] is not None:
            sort_node.out_vars[gdl__cnmhn] = replace_vars_inner(sort_node.
                out_vars[gdl__cnmhn], var_dict)
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
        for tgmvs__hoylp in (in_vars + out_vars):
            if array_dists[tgmvs__hoylp.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                tgmvs__hoylp.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        tuta__jmjdf = []
        for tgmvs__hoylp in in_vars:
            yzm__cvwd = _copy_array_nodes(tgmvs__hoylp, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            tuta__jmjdf.append(yzm__cvwd)
        in_vars = tuta__jmjdf
    out_types = [(typemap[tgmvs__hoylp.name] if tgmvs__hoylp is not None else
        types.none) for tgmvs__hoylp in sort_node.out_vars]
    ecp__rrpq, btb__fvzzq = get_sort_cpp_section(sort_node, out_types,
        typemap, parallel)
    vgb__dkns = {}
    exec(ecp__rrpq, {}, vgb__dkns)
    tzrsw__mhpxl = vgb__dkns['f']
    btb__fvzzq.update({'bodo': bodo, 'np': np, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'sort_values_table': sort_values_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'array_to_info': array_to_info,
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    btb__fvzzq.update({f'out_type{gdl__cnmhn}': out_types[gdl__cnmhn] for
        gdl__cnmhn in range(len(out_types))})
    cbi__znskt = sort_node._bodo_chunk_bounds
    vkitp__ykd = cbi__znskt
    if cbi__znskt is None:
        loc = sort_node.loc
        vkitp__ykd = ir.Var(ir.Scope(None, loc), mk_unique_var(
            '$bounds_none'), loc)
        typemap[vkitp__ykd.name] = types.none
        nodes.append(ir.Assign(ir.Const(None, loc), vkitp__ykd, loc))
    oembr__nslcu = compile_to_numba_ir(tzrsw__mhpxl, btb__fvzzq, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[tgmvs__hoylp
        .name] for tgmvs__hoylp in in_vars) + (typemap[vkitp__ykd.name],),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(oembr__nslcu, in_vars + [vkitp__ykd])
    yyv__blrrk = oembr__nslcu.body[-2].value.value
    nodes += oembr__nslcu.body[:-2]
    for gdl__cnmhn, tgmvs__hoylp in enumerate(out_vars):
        gen_getitem(tgmvs__hoylp, yyv__blrrk, gdl__cnmhn, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    vuhtt__kub = lambda arr: arr.copy()
    yia__dyjd = None
    if isinstance(typemap[var.name], TableType):
        mjqt__yyw = len(typemap[var.name].arr_types)
        yia__dyjd = set(range(mjqt__yyw)) - dead_cols
        yia__dyjd = MetaType(tuple(sorted(yia__dyjd)))
        vuhtt__kub = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    oembr__nslcu = compile_to_numba_ir(vuhtt__kub, {'bodo': bodo, 'types':
        types, '_used_columns': yia__dyjd}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(oembr__nslcu, [var])
    nodes += oembr__nslcu.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, typemap, parallel):
    fwx__ont = len(sort_node.key_inds)
    ruwm__pdt = len(sort_node.in_vars)
    orqlg__sya = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + ruwm__pdt - 1 if sort_node.
        is_table_format else ruwm__pdt)
    xby__duuv, dkbv__euh, kecl__ckej = _get_cpp_col_ind_mappings(sort_node.
        key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols)
    nfuvv__otnf = []
    if sort_node.is_table_format:
        nfuvv__otnf.append('arg0')
        for gdl__cnmhn in range(1, ruwm__pdt):
            acp__oxw = sort_node.num_table_arrays + gdl__cnmhn - 1
            if acp__oxw not in sort_node.dead_var_inds:
                nfuvv__otnf.append(f'arg{acp__oxw}')
    else:
        for gdl__cnmhn in range(n_cols):
            if gdl__cnmhn not in sort_node.dead_var_inds:
                nfuvv__otnf.append(f'arg{gdl__cnmhn}')
    ecp__rrpq = f"def f({', '.join(nfuvv__otnf)}, bounds_in):\n"
    if sort_node.is_table_format:
        gem__kpsez = ',' if ruwm__pdt - 1 == 1 else ''
        xffx__pbybt = []
        for gdl__cnmhn in range(sort_node.num_table_arrays, n_cols):
            if gdl__cnmhn in sort_node.dead_var_inds:
                xffx__pbybt.append('None')
            else:
                xffx__pbybt.append(f'arg{gdl__cnmhn}')
        ecp__rrpq += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(xffx__pbybt)}{gem__kpsez}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        xaqcc__tqp = {ozv__bgb: gdl__cnmhn for gdl__cnmhn, ozv__bgb in
            enumerate(xby__duuv)}
        lwka__dgg = [None] * len(xby__duuv)
        for gdl__cnmhn in range(n_cols):
            aqc__awvn = xaqcc__tqp.get(gdl__cnmhn, -1)
            if aqc__awvn != -1:
                lwka__dgg[aqc__awvn] = f'array_to_info(arg{gdl__cnmhn})'
        ecp__rrpq += '  info_list_total = [{}]\n'.format(','.join(lwka__dgg))
        ecp__rrpq += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    ecp__rrpq += '  vect_ascending = np.array([{}], np.int64)\n'.format(','
        .join('1' if qee__ubz else '0' for qee__ubz in sort_node.
        ascending_list))
    ecp__rrpq += '  na_position = np.array([{}], np.int64)\n'.format(','.
        join('1' if qee__ubz else '0' for qee__ubz in sort_node.na_position_b))
    ecp__rrpq += '  dead_keys = np.array([{}], np.int64)\n'.format(','.join
        ('1' if gdl__cnmhn in kecl__ckej else '0' for gdl__cnmhn in range(
        fwx__ont)))
    ecp__rrpq += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    eoms__idnq = sort_node._bodo_chunk_bounds
    fdkq__mhkln = '0' if eoms__idnq is None or is_overload_none(typemap[
        eoms__idnq.name]
        ) else 'arr_info_list_to_table([array_to_info(bounds_in)])'
    ecp__rrpq += f"""  out_cpp_table = sort_values_table(in_cpp_table, {fwx__ont}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {fdkq__mhkln}, {parallel})
"""
    if sort_node.is_table_format:
        gem__kpsez = ',' if orqlg__sya == 1 else ''
        wjhd__oukaz = (
            f"({', '.join(f'out_type{gdl__cnmhn}' if not type_has_unknown_cats(out_types[gdl__cnmhn]) else f'arg{gdl__cnmhn}' for gdl__cnmhn in range(orqlg__sya))}{gem__kpsez})"
            )
        ecp__rrpq += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {wjhd__oukaz}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        xaqcc__tqp = {ozv__bgb: gdl__cnmhn for gdl__cnmhn, ozv__bgb in
            enumerate(dkbv__euh)}
        lwka__dgg = []
        for gdl__cnmhn in range(n_cols):
            aqc__awvn = xaqcc__tqp.get(gdl__cnmhn, -1)
            if aqc__awvn != -1:
                hux__zqg = (f'out_type{gdl__cnmhn}' if not
                    type_has_unknown_cats(out_types[gdl__cnmhn]) else
                    f'arg{gdl__cnmhn}')
                ecp__rrpq += f"""  out{gdl__cnmhn} = info_to_array(info_from_table(out_cpp_table, {aqc__awvn}), {hux__zqg})
"""
                lwka__dgg.append(f'out{gdl__cnmhn}')
        gem__kpsez = ',' if len(lwka__dgg) == 1 else ''
        dvqne__bymn = f"({', '.join(lwka__dgg)}{gem__kpsez})"
        ecp__rrpq += f'  out_data = {dvqne__bymn}\n'
    ecp__rrpq += '  delete_table(out_cpp_table)\n'
    ecp__rrpq += '  delete_table(in_cpp_table)\n'
    ecp__rrpq += f'  return out_data\n'
    return ecp__rrpq, {'in_col_inds': MetaType(tuple(xby__duuv)),
        'out_col_inds': MetaType(tuple(dkbv__euh))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    xby__duuv = []
    dkbv__euh = []
    kecl__ckej = []
    for ozv__bgb, gdl__cnmhn in enumerate(key_inds):
        xby__duuv.append(gdl__cnmhn)
        if gdl__cnmhn in dead_key_var_inds:
            kecl__ckej.append(ozv__bgb)
        else:
            dkbv__euh.append(gdl__cnmhn)
    for gdl__cnmhn in range(n_cols):
        if gdl__cnmhn in dead_var_inds or gdl__cnmhn in key_inds:
            continue
        xby__duuv.append(gdl__cnmhn)
        dkbv__euh.append(gdl__cnmhn)
    return xby__duuv, dkbv__euh, kecl__ckej


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    pvd__ilt = sort_node.in_vars[0].name
    iujc__iax = sort_node.out_vars[0].name
    tgsnd__pknh, blip__wjwp, kpn__vos = block_use_map[pvd__ilt]
    if blip__wjwp or kpn__vos:
        return
    xjt__tew, oigm__evwe, weuia__wpbmf = _compute_table_column_uses(iujc__iax,
        table_col_use_map, equiv_vars)
    yjjq__ygw = set(gdl__cnmhn for gdl__cnmhn in sort_node.key_inds if 
        gdl__cnmhn < sort_node.num_table_arrays)
    block_use_map[pvd__ilt
        ] = tgsnd__pknh | xjt__tew | yjjq__ygw, oigm__evwe or weuia__wpbmf, False


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    mjqt__yyw = sort_node.num_table_arrays
    iujc__iax = sort_node.out_vars[0].name
    yia__dyjd = _find_used_columns(iujc__iax, mjqt__yyw, column_live_map,
        equiv_vars)
    if yia__dyjd is None:
        return False
    vije__zwxx = set(range(mjqt__yyw)) - yia__dyjd
    yjjq__ygw = set(gdl__cnmhn for gdl__cnmhn in sort_node.key_inds if 
        gdl__cnmhn < mjqt__yyw)
    lltx__ypyf = sort_node.dead_key_var_inds | vije__zwxx & yjjq__ygw
    zwuil__phwo = sort_node.dead_var_inds | vije__zwxx - yjjq__ygw
    xwz__yrpf = (lltx__ypyf != sort_node.dead_key_var_inds) | (zwuil__phwo !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = lltx__ypyf
    sort_node.dead_var_inds = zwuil__phwo
    return xwz__yrpf


remove_dead_column_extensions[Sort] = sort_remove_dead_column
