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
    ymsk__eakv = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    koz__squuu = []
    for tbjmo__vef, njuor__srrt in enumerate(node.out_vars):
        rkp__zdbuq = typemap[njuor__srrt.name]
        if rkp__zdbuq == types.none:
            continue
        etfm__nqd = tbjmo__vef == 0 and node.connector_typ in ('parquet', 'sql'
            ) and not node.is_live_table
        qsrd__ozup = node.connector_typ == 'sql' and tbjmo__vef > 1
        if not (etfm__nqd or qsrd__ozup):
            rwcar__ggfq = array_analysis._gen_shape_call(equiv_set,
                njuor__srrt, rkp__zdbuq.ndim, None, ymsk__eakv)
            equiv_set.insert_equiv(njuor__srrt, rwcar__ggfq)
            koz__squuu.append(rwcar__ggfq[0])
            equiv_set.define(njuor__srrt, set())
    if len(koz__squuu) > 1:
        equiv_set.insert_equiv(*koz__squuu)
    return [], ymsk__eakv


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        yzqq__ltccp = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        yzqq__ltccp = Distribution.OneD_Var
    else:
        yzqq__ltccp = Distribution.OneD
    for web__lbkrv in node.out_vars:
        if web__lbkrv.name in array_dists:
            yzqq__ltccp = Distribution(min(yzqq__ltccp.value, array_dists[
                web__lbkrv.name].value))
    for web__lbkrv in node.out_vars:
        array_dists[web__lbkrv.name] = yzqq__ltccp


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
    for njuor__srrt, rkp__zdbuq in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(njuor__srrt.name, rkp__zdbuq, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    hheg__gujrf = []
    for njuor__srrt in node.out_vars:
        cdghj__bljia = visit_vars_inner(njuor__srrt, callback, cbdata)
        hheg__gujrf.append(cdghj__bljia)
    node.out_vars = hheg__gujrf
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for vjfnp__nhh in node.filters:
            for tbjmo__vef in range(len(vjfnp__nhh)):
                stm__qeyuk = vjfnp__nhh[tbjmo__vef]
                vjfnp__nhh[tbjmo__vef] = stm__qeyuk[0], stm__qeyuk[1
                    ], visit_vars_inner(stm__qeyuk[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({web__lbkrv.name for web__lbkrv in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for bjyu__julla in node.filters:
            for web__lbkrv in bjyu__julla:
                if isinstance(web__lbkrv[2], ir.Var):
                    use_set.add(web__lbkrv[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    kiaa__dumu = set(web__lbkrv.name for web__lbkrv in node.out_vars)
    return set(), kiaa__dumu


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    hheg__gujrf = []
    for njuor__srrt in node.out_vars:
        cdghj__bljia = replace_vars_inner(njuor__srrt, var_dict)
        hheg__gujrf.append(cdghj__bljia)
    node.out_vars = hheg__gujrf
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for vjfnp__nhh in node.filters:
            for tbjmo__vef in range(len(vjfnp__nhh)):
                stm__qeyuk = vjfnp__nhh[tbjmo__vef]
                vjfnp__nhh[tbjmo__vef] = stm__qeyuk[0], stm__qeyuk[1
                    ], replace_vars_inner(stm__qeyuk[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for njuor__srrt in node.out_vars:
        npcj__svxec = definitions[njuor__srrt.name]
        if node not in npcj__svxec:
            npcj__svxec.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        ciw__iia = [web__lbkrv[2] for bjyu__julla in filters for web__lbkrv in
            bjyu__julla]
        ytg__magyq = set()
        for schd__flzg in ciw__iia:
            if isinstance(schd__flzg, ir.Var):
                if schd__flzg.name not in ytg__magyq:
                    filter_vars.append(schd__flzg)
                ytg__magyq.add(schd__flzg.name)
        return {web__lbkrv.name: f'f{tbjmo__vef}' for tbjmo__vef,
            web__lbkrv in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {tbjmo__vef for tbjmo__vef in used_columns if tbjmo__vef <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    svfn__mqyh = {}
    for tbjmo__vef, ldgz__cdezm in enumerate(df_type.data):
        if isinstance(ldgz__cdezm, bodo.IntegerArrayType):
            rpb__hof = ldgz__cdezm.get_pandas_scalar_type_instance
            if rpb__hof not in svfn__mqyh:
                svfn__mqyh[rpb__hof] = []
            svfn__mqyh[rpb__hof].append(df.columns[tbjmo__vef])
    for rkp__zdbuq, lcrrm__yku in svfn__mqyh.items():
        df[lcrrm__yku] = df[lcrrm__yku].astype(rkp__zdbuq)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    ijz__uuo = node.out_vars[0].name
    assert isinstance(typemap[ijz__uuo], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, mhu__lxtt, mex__efrw = get_live_column_nums_block(
            column_live_map, equiv_vars, ijz__uuo)
        if not (mhu__lxtt or mex__efrw):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    crzn__zmnjf = False
    if array_dists is not None:
        ugwx__jus = node.out_vars[0].name
        crzn__zmnjf = array_dists[ugwx__jus] in (Distribution.OneD,
            Distribution.OneD_Var)
        klj__omb = node.out_vars[1].name
        assert typemap[klj__omb
            ] == types.none or not crzn__zmnjf or array_dists[klj__omb] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return crzn__zmnjf


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    afok__dgyp = 'None'
    wpvs__luq = 'None'
    if filters:
        ofie__vdjfj = []
        qlwp__mrvi = []
        pekpa__skb = False
        orig_colname_map = {dpebv__hxy: tbjmo__vef for tbjmo__vef,
            dpebv__hxy in enumerate(col_names)}
        for vjfnp__nhh in filters:
            szk__nlzk = []
            qmp__flmap = []
            for web__lbkrv in vjfnp__nhh:
                if isinstance(web__lbkrv[2], ir.Var):
                    ttefr__biv, heb__jtraz = determine_filter_cast(
                        original_out_types, typemap, web__lbkrv,
                        orig_colname_map, partition_names, source)
                    if web__lbkrv[1] == 'in':
                        hci__ffysl = (
                            f"(ds.field('{web__lbkrv[0]}').isin({filter_map[web__lbkrv[2].name]}))"
                            )
                    else:
                        hci__ffysl = (
                            f"(ds.field('{web__lbkrv[0]}'){ttefr__biv} {web__lbkrv[1]} ds.scalar({filter_map[web__lbkrv[2].name]}){heb__jtraz})"
                            )
                else:
                    assert web__lbkrv[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if web__lbkrv[1] == 'is not':
                        uwfz__dxo = '~'
                    else:
                        uwfz__dxo = ''
                    hci__ffysl = (
                        f"({uwfz__dxo}ds.field('{web__lbkrv[0]}').is_null())")
                qmp__flmap.append(hci__ffysl)
                if not pekpa__skb:
                    if web__lbkrv[0] in partition_names and isinstance(
                        web__lbkrv[2], ir.Var):
                        if output_dnf:
                            wetl__huzlv = (
                                f"('{web__lbkrv[0]}', '{web__lbkrv[1]}', {filter_map[web__lbkrv[2].name]})"
                                )
                        else:
                            wetl__huzlv = hci__ffysl
                        szk__nlzk.append(wetl__huzlv)
                    elif web__lbkrv[0] in partition_names and not isinstance(
                        web__lbkrv[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            wetl__huzlv = (
                                f"('{web__lbkrv[0]}', '{web__lbkrv[1]}', '{web__lbkrv[2]}')"
                                )
                        else:
                            wetl__huzlv = hci__ffysl
                        szk__nlzk.append(wetl__huzlv)
            qdvg__pssr = ''
            if szk__nlzk:
                if output_dnf:
                    qdvg__pssr = ', '.join(szk__nlzk)
                else:
                    qdvg__pssr = ' & '.join(szk__nlzk)
            else:
                pekpa__skb = True
            hxf__ksp = ' & '.join(qmp__flmap)
            if qdvg__pssr:
                if output_dnf:
                    ofie__vdjfj.append(f'[{qdvg__pssr}]')
                else:
                    ofie__vdjfj.append(f'({qdvg__pssr})')
            qlwp__mrvi.append(f'({hxf__ksp})')
        if output_dnf:
            rvet__qit = ', '.join(ofie__vdjfj)
        else:
            rvet__qit = ' | '.join(ofie__vdjfj)
        njnp__mkec = ' | '.join(qlwp__mrvi)
        if rvet__qit and not pekpa__skb:
            if output_dnf:
                afok__dgyp = f'[{rvet__qit}]'
            else:
                afok__dgyp = f'({rvet__qit})'
        wpvs__luq = f'({njnp__mkec})'
    return afok__dgyp, wpvs__luq


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    tanq__mqpi = filter_val[0]
    lzl__szb = col_types[orig_colname_map[tanq__mqpi]]
    rhf__ywksa = bodo.utils.typing.element_type(lzl__szb)
    if source == 'parquet' and tanq__mqpi in partition_names:
        if rhf__ywksa == types.unicode_type:
            vlj__jxbkg = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(rhf__ywksa, types.Integer):
            vlj__jxbkg = f'.cast(pyarrow.{rhf__ywksa.name}(), safe=False)'
        else:
            vlj__jxbkg = ''
    else:
        vlj__jxbkg = ''
    iwn__qmu = typemap[filter_val[2].name]
    if isinstance(iwn__qmu, (types.List, types.Set)):
        acvcg__lxh = iwn__qmu.dtype
    elif is_array_typ(iwn__qmu):
        acvcg__lxh = iwn__qmu.dtype
    else:
        acvcg__lxh = iwn__qmu
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhf__ywksa,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(acvcg__lxh,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([rhf__ywksa, acvcg__lxh]):
        if not bodo.utils.typing.is_safe_arrow_cast(rhf__ywksa, acvcg__lxh):
            raise BodoError(
                f'Unsupported Arrow cast from {rhf__ywksa} to {acvcg__lxh} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if rhf__ywksa == types.unicode_type and acvcg__lxh in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif acvcg__lxh == types.unicode_type and rhf__ywksa in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            if isinstance(iwn__qmu, (types.List, types.Set)):
                yyuie__pxz = 'list' if isinstance(iwn__qmu, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {yyuie__pxz} values with isin filter pushdown.'
                    )
            return vlj__jxbkg, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif rhf__ywksa == bodo.datetime_date_type and acvcg__lxh in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif acvcg__lxh == bodo.datetime_date_type and rhf__ywksa in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return vlj__jxbkg, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return vlj__jxbkg, ''
