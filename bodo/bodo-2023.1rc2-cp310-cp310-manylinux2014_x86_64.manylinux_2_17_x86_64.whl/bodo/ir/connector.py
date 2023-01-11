"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
import sys
from collections import defaultdict
from typing import Literal, Set, Tuple
import numba
from numba.core import ir, types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from bodo.hiframes.table import TableType
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import get_live_column_nums_block
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError
from bodo.utils.utils import debug_prints, is_array_typ


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    hvogs__dmdp = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    gwqrq__cfhj = []
    for syvtr__awy, jpkxh__jdgyn in enumerate(node.out_vars):
        jlp__yfmm = typemap[jpkxh__jdgyn.name]
        if jlp__yfmm == types.none:
            continue
        lmp__ilrmp = syvtr__awy == 0 and node.connector_typ in ('parquet',
            'sql') and not node.is_live_table
        asog__lpwr = node.connector_typ == 'sql' and syvtr__awy > 1
        if not (lmp__ilrmp or asog__lpwr):
            jfpbc__owg = array_analysis._gen_shape_call(equiv_set,
                jpkxh__jdgyn, jlp__yfmm.ndim, None, hvogs__dmdp)
            equiv_set.insert_equiv(jpkxh__jdgyn, jfpbc__owg)
            gwqrq__cfhj.append(jfpbc__owg[0])
            equiv_set.define(jpkxh__jdgyn, set())
    if len(gwqrq__cfhj) > 1:
        equiv_set.insert_equiv(*gwqrq__cfhj)
    return [], hvogs__dmdp


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        hmw__lwca = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        hmw__lwca = Distribution.OneD_Var
    else:
        hmw__lwca = Distribution.OneD
    for wlxxn__ruyrs in node.out_vars:
        if wlxxn__ruyrs.name in array_dists:
            hmw__lwca = Distribution(min(hmw__lwca.value, array_dists[
                wlxxn__ruyrs.name].value))
    for wlxxn__ruyrs in node.out_vars:
        array_dists[wlxxn__ruyrs.name] = hmw__lwca


def connector_typeinfer(node, typeinferer):
    if node.connector_typ == 'csv':
        if node.chunksize is not None:
            typeinferer.lock_type(node.out_vars[0].name, node.out_types[0],
                loc=node.loc)
        else:
            typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(
                node.out_types)), loc=node.loc)
            typeinferer.lock_type(node.out_vars[1].name, node.
                index_column_typ, loc=node.loc)
        return
    if node.connector_typ in ('parquet', 'sql'):
        typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(node.
            out_types)), loc=node.loc)
        typeinferer.lock_type(node.out_vars[1].name, node.index_column_type,
            loc=node.loc)
        if node.connector_typ == 'sql':
            if len(node.out_vars) > 2:
                typeinferer.lock_type(node.out_vars[2].name, node.
                    file_list_type, loc=node.loc)
            if len(node.out_vars) > 3:
                typeinferer.lock_type(node.out_vars[3].name, node.
                    snapshot_id_type, loc=node.loc)
        return
    for jpkxh__jdgyn, jlp__yfmm in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(jpkxh__jdgyn.name, jlp__yfmm, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    nbi__qrihl = []
    for jpkxh__jdgyn in node.out_vars:
        ftqqo__zpqpl = visit_vars_inner(jpkxh__jdgyn, callback, cbdata)
        nbi__qrihl.append(ftqqo__zpqpl)
    node.out_vars = nbi__qrihl
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for zaaj__dpco in node.filters:
            for syvtr__awy in range(len(zaaj__dpco)):
                qgni__sdxu = zaaj__dpco[syvtr__awy]
                zaaj__dpco[syvtr__awy] = qgni__sdxu[0], qgni__sdxu[1
                    ], visit_vars_inner(qgni__sdxu[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({wlxxn__ruyrs.name for wlxxn__ruyrs in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for wmgix__ifajb in node.filters:
            for wlxxn__ruyrs in wmgix__ifajb:
                if isinstance(wlxxn__ruyrs[2], ir.Var):
                    use_set.add(wlxxn__ruyrs[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    feb__rcrxk = set(wlxxn__ruyrs.name for wlxxn__ruyrs in node.out_vars)
    return set(), feb__rcrxk


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    nbi__qrihl = []
    for jpkxh__jdgyn in node.out_vars:
        ftqqo__zpqpl = replace_vars_inner(jpkxh__jdgyn, var_dict)
        nbi__qrihl.append(ftqqo__zpqpl)
    node.out_vars = nbi__qrihl
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for zaaj__dpco in node.filters:
            for syvtr__awy in range(len(zaaj__dpco)):
                qgni__sdxu = zaaj__dpco[syvtr__awy]
                zaaj__dpco[syvtr__awy] = qgni__sdxu[0], qgni__sdxu[1
                    ], replace_vars_inner(qgni__sdxu[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for jpkxh__jdgyn in node.out_vars:
        rdxuh__zhbbn = definitions[jpkxh__jdgyn.name]
        if node not in rdxuh__zhbbn:
            rdxuh__zhbbn.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        expc__wxvj = [wlxxn__ruyrs[2] for wmgix__ifajb in filters for
            wlxxn__ruyrs in wmgix__ifajb]
        ewhu__hfqeh = set()
        for qwm__kdnef in expc__wxvj:
            if isinstance(qwm__kdnef, ir.Var):
                if qwm__kdnef.name not in ewhu__hfqeh:
                    filter_vars.append(qwm__kdnef)
                ewhu__hfqeh.add(qwm__kdnef.name)
        return {wlxxn__ruyrs.name: f'f{syvtr__awy}' for syvtr__awy,
            wlxxn__ruyrs in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {syvtr__awy for syvtr__awy in used_columns if syvtr__awy <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    iipk__mrz = {}
    for syvtr__awy, ykxzf__jrl in enumerate(df_type.data):
        if isinstance(ykxzf__jrl, bodo.IntegerArrayType):
            anze__wjdkf = ykxzf__jrl.get_pandas_scalar_type_instance
            if anze__wjdkf not in iipk__mrz:
                iipk__mrz[anze__wjdkf] = []
            iipk__mrz[anze__wjdkf].append(df.columns[syvtr__awy])
    for jlp__yfmm, pmd__vtuae in iipk__mrz.items():
        df[pmd__vtuae] = df[pmd__vtuae].astype(jlp__yfmm)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    iwz__ijw = node.out_vars[0].name
    assert isinstance(typemap[iwz__ijw], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, tsqp__mghxz, ocz__ngq = get_live_column_nums_block(
            column_live_map, equiv_vars, iwz__ijw)
        if not (tsqp__mghxz or ocz__ngq):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    bioa__qvs = False
    if array_dists is not None:
        wylsv__olf = node.out_vars[0].name
        bioa__qvs = array_dists[wylsv__olf] in (Distribution.OneD,
            Distribution.OneD_Var)
        dtqj__wqsxz = node.out_vars[1].name
        assert typemap[dtqj__wqsxz
            ] == types.none or not bioa__qvs or array_dists[dtqj__wqsxz] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return bioa__qvs


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    doyh__orn = 'None'
    cqrz__wlyk = 'None'
    if filters:
        nam__qinbi = []
        puif__qtu = []
        rgz__iiyog = False
        orig_colname_map = {snywd__hwl: syvtr__awy for syvtr__awy,
            snywd__hwl in enumerate(col_names)}
        for zaaj__dpco in filters:
            vwa__xig = []
            qhm__tny = []
            for wlxxn__ruyrs in zaaj__dpco:
                if isinstance(wlxxn__ruyrs[2], ir.Var):
                    zppx__njwme, ars__zwr = determine_filter_cast(
                        original_out_types, typemap, wlxxn__ruyrs,
                        orig_colname_map, partition_names, source)
                    if wlxxn__ruyrs[1] == 'in':
                        eov__gnum = (
                            f"(ds.field('{wlxxn__ruyrs[0]}').isin({filter_map[wlxxn__ruyrs[2].name]}))"
                            )
                    else:
                        eov__gnum = (
                            f"(ds.field('{wlxxn__ruyrs[0]}'){zppx__njwme} {wlxxn__ruyrs[1]} ds.scalar({filter_map[wlxxn__ruyrs[2].name]}){ars__zwr})"
                            )
                else:
                    assert wlxxn__ruyrs[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if wlxxn__ruyrs[1] == 'is not':
                        upkjh__kly = '~'
                    else:
                        upkjh__kly = ''
                    eov__gnum = (
                        f"({upkjh__kly}ds.field('{wlxxn__ruyrs[0]}').is_null())"
                        )
                qhm__tny.append(eov__gnum)
                if not rgz__iiyog:
                    if wlxxn__ruyrs[0] in partition_names and isinstance(
                        wlxxn__ruyrs[2], ir.Var):
                        if output_dnf:
                            rcyjf__kser = (
                                f"('{wlxxn__ruyrs[0]}', '{wlxxn__ruyrs[1]}', {filter_map[wlxxn__ruyrs[2].name]})"
                                )
                        else:
                            rcyjf__kser = eov__gnum
                        vwa__xig.append(rcyjf__kser)
                    elif wlxxn__ruyrs[0] in partition_names and not isinstance(
                        wlxxn__ruyrs[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            rcyjf__kser = (
                                f"('{wlxxn__ruyrs[0]}', '{wlxxn__ruyrs[1]}', '{wlxxn__ruyrs[2]}')"
                                )
                        else:
                            rcyjf__kser = eov__gnum
                        vwa__xig.append(rcyjf__kser)
            bresd__dmpq = ''
            if vwa__xig:
                if output_dnf:
                    bresd__dmpq = ', '.join(vwa__xig)
                else:
                    bresd__dmpq = ' & '.join(vwa__xig)
            else:
                rgz__iiyog = True
            qyn__mba = ' & '.join(qhm__tny)
            if bresd__dmpq:
                if output_dnf:
                    nam__qinbi.append(f'[{bresd__dmpq}]')
                else:
                    nam__qinbi.append(f'({bresd__dmpq})')
            puif__qtu.append(f'({qyn__mba})')
        if output_dnf:
            scr__jpx = ', '.join(nam__qinbi)
        else:
            scr__jpx = ' | '.join(nam__qinbi)
        uim__uhgr = ' | '.join(puif__qtu)
        if scr__jpx and not rgz__iiyog:
            if output_dnf:
                doyh__orn = f'[{scr__jpx}]'
            else:
                doyh__orn = f'({scr__jpx})'
        cqrz__wlyk = f'({uim__uhgr})'
    return doyh__orn, cqrz__wlyk


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    kslp__antee = filter_val[0]
    dda__raz = col_types[orig_colname_map[kslp__antee]]
    mbqb__web = bodo.utils.typing.element_type(dda__raz)
    if source == 'parquet' and kslp__antee in partition_names:
        if mbqb__web == types.unicode_type:
            cqfnt__tgef = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(mbqb__web, types.Integer):
            cqfnt__tgef = f'.cast(pyarrow.{mbqb__web.name}(), safe=False)'
        else:
            cqfnt__tgef = ''
    else:
        cqfnt__tgef = ''
    oain__ohfgm = typemap[filter_val[2].name]
    if isinstance(oain__ohfgm, (types.List, types.Set)):
        cdsy__tyoc = oain__ohfgm.dtype
    elif is_array_typ(oain__ohfgm):
        cdsy__tyoc = oain__ohfgm.dtype
    else:
        cdsy__tyoc = oain__ohfgm
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(mbqb__web,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(cdsy__tyoc,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([mbqb__web, cdsy__tyoc]):
        if not bodo.utils.typing.is_safe_arrow_cast(mbqb__web, cdsy__tyoc):
            raise BodoError(
                f'Unsupported Arrow cast from {mbqb__web} to {cdsy__tyoc} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if mbqb__web == types.unicode_type and cdsy__tyoc in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif cdsy__tyoc == types.unicode_type and mbqb__web in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            if isinstance(oain__ohfgm, (types.List, types.Set)):
                uky__mvppm = 'list' if isinstance(oain__ohfgm, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {uky__mvppm} values with isin filter pushdown.'
                    )
            return cqfnt__tgef, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif mbqb__web == bodo.datetime_date_type and cdsy__tyoc in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif cdsy__tyoc == bodo.datetime_date_type and mbqb__web in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return cqfnt__tgef, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return cqfnt__tgef, ''
