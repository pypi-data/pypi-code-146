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
    ugja__rwcqy = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    bjht__foc = []
    for boeas__wlx, qdpk__vdlj in enumerate(node.out_vars):
        dak__eymmr = typemap[qdpk__vdlj.name]
        if dak__eymmr == types.none:
            continue
        eqn__fzq = boeas__wlx == 0 and node.connector_typ in ('parquet', 'sql'
            ) and not node.is_live_table
        musaj__vgnwp = node.connector_typ == 'sql' and boeas__wlx > 1
        if not (eqn__fzq or musaj__vgnwp):
            bvtl__yjp = array_analysis._gen_shape_call(equiv_set,
                qdpk__vdlj, dak__eymmr.ndim, None, ugja__rwcqy)
            equiv_set.insert_equiv(qdpk__vdlj, bvtl__yjp)
            bjht__foc.append(bvtl__yjp[0])
            equiv_set.define(qdpk__vdlj, set())
    if len(bjht__foc) > 1:
        equiv_set.insert_equiv(*bjht__foc)
    return [], ugja__rwcqy


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        zcn__ryqav = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        zcn__ryqav = Distribution.OneD_Var
    else:
        zcn__ryqav = Distribution.OneD
    for mlhg__evcl in node.out_vars:
        if mlhg__evcl.name in array_dists:
            zcn__ryqav = Distribution(min(zcn__ryqav.value, array_dists[
                mlhg__evcl.name].value))
    for mlhg__evcl in node.out_vars:
        array_dists[mlhg__evcl.name] = zcn__ryqav


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
    for qdpk__vdlj, dak__eymmr in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(qdpk__vdlj.name, dak__eymmr, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    nrk__tyqgf = []
    for qdpk__vdlj in node.out_vars:
        nqrm__ufz = visit_vars_inner(qdpk__vdlj, callback, cbdata)
        nrk__tyqgf.append(nqrm__ufz)
    node.out_vars = nrk__tyqgf
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for ycnd__fakx in node.filters:
            for boeas__wlx in range(len(ycnd__fakx)):
                qsgk__dsqz = ycnd__fakx[boeas__wlx]
                ycnd__fakx[boeas__wlx] = qsgk__dsqz[0], qsgk__dsqz[1
                    ], visit_vars_inner(qsgk__dsqz[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({mlhg__evcl.name for mlhg__evcl in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for bcq__lfsv in node.filters:
            for mlhg__evcl in bcq__lfsv:
                if isinstance(mlhg__evcl[2], ir.Var):
                    use_set.add(mlhg__evcl[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    vip__iabg = set(mlhg__evcl.name for mlhg__evcl in node.out_vars)
    return set(), vip__iabg


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    nrk__tyqgf = []
    for qdpk__vdlj in node.out_vars:
        nqrm__ufz = replace_vars_inner(qdpk__vdlj, var_dict)
        nrk__tyqgf.append(nqrm__ufz)
    node.out_vars = nrk__tyqgf
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for ycnd__fakx in node.filters:
            for boeas__wlx in range(len(ycnd__fakx)):
                qsgk__dsqz = ycnd__fakx[boeas__wlx]
                ycnd__fakx[boeas__wlx] = qsgk__dsqz[0], qsgk__dsqz[1
                    ], replace_vars_inner(qsgk__dsqz[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for qdpk__vdlj in node.out_vars:
        ndx__mfhx = definitions[qdpk__vdlj.name]
        if node not in ndx__mfhx:
            ndx__mfhx.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        zhj__rqgp = [mlhg__evcl[2] for bcq__lfsv in filters for mlhg__evcl in
            bcq__lfsv]
        cxrvb__zgvsy = set()
        for ano__jasb in zhj__rqgp:
            if isinstance(ano__jasb, ir.Var):
                if ano__jasb.name not in cxrvb__zgvsy:
                    filter_vars.append(ano__jasb)
                cxrvb__zgvsy.add(ano__jasb.name)
        return {mlhg__evcl.name: f'f{boeas__wlx}' for boeas__wlx,
            mlhg__evcl in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {boeas__wlx for boeas__wlx in used_columns if boeas__wlx <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    ebjo__mhln = {}
    for boeas__wlx, iuqqi__lsbr in enumerate(df_type.data):
        if isinstance(iuqqi__lsbr, bodo.IntegerArrayType):
            isnv__umrzd = iuqqi__lsbr.get_pandas_scalar_type_instance
            if isnv__umrzd not in ebjo__mhln:
                ebjo__mhln[isnv__umrzd] = []
            ebjo__mhln[isnv__umrzd].append(df.columns[boeas__wlx])
    for dak__eymmr, yojc__klvci in ebjo__mhln.items():
        df[yojc__klvci] = df[yojc__klvci].astype(dak__eymmr)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    khjo__ezd = node.out_vars[0].name
    assert isinstance(typemap[khjo__ezd], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, sba__mcd, nfblf__eoruu = get_live_column_nums_block(
            column_live_map, equiv_vars, khjo__ezd)
        if not (sba__mcd or nfblf__eoruu):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    uqeq__xzhxm = False
    if array_dists is not None:
        yrqh__ftisn = node.out_vars[0].name
        uqeq__xzhxm = array_dists[yrqh__ftisn] in (Distribution.OneD,
            Distribution.OneD_Var)
        alu__wfmik = node.out_vars[1].name
        assert typemap[alu__wfmik
            ] == types.none or not uqeq__xzhxm or array_dists[alu__wfmik] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return uqeq__xzhxm


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    cqr__iwaf = 'None'
    prm__zjnia = 'None'
    if filters:
        prf__tizoj = []
        jnkob__ikpdl = []
        mlx__zhtnr = False
        orig_colname_map = {zxsvd__gbfa: boeas__wlx for boeas__wlx,
            zxsvd__gbfa in enumerate(col_names)}
        for ycnd__fakx in filters:
            ccj__vcmce = []
            tcyd__boe = []
            for mlhg__evcl in ycnd__fakx:
                if isinstance(mlhg__evcl[2], ir.Var):
                    kcrzg__umc, kso__beztu = determine_filter_cast(
                        original_out_types, typemap, mlhg__evcl,
                        orig_colname_map, partition_names, source)
                    if mlhg__evcl[1] == 'in':
                        arzv__mjig = (
                            f"(ds.field('{mlhg__evcl[0]}').isin({filter_map[mlhg__evcl[2].name]}))"
                            )
                    else:
                        arzv__mjig = (
                            f"(ds.field('{mlhg__evcl[0]}'){kcrzg__umc} {mlhg__evcl[1]} ds.scalar({filter_map[mlhg__evcl[2].name]}){kso__beztu})"
                            )
                else:
                    assert mlhg__evcl[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if mlhg__evcl[1] == 'is not':
                        uoygb__nicp = '~'
                    else:
                        uoygb__nicp = ''
                    arzv__mjig = (
                        f"({uoygb__nicp}ds.field('{mlhg__evcl[0]}').is_null())"
                        )
                tcyd__boe.append(arzv__mjig)
                if not mlx__zhtnr:
                    if mlhg__evcl[0] in partition_names and isinstance(
                        mlhg__evcl[2], ir.Var):
                        if output_dnf:
                            ofzyt__jjhnc = (
                                f"('{mlhg__evcl[0]}', '{mlhg__evcl[1]}', {filter_map[mlhg__evcl[2].name]})"
                                )
                        else:
                            ofzyt__jjhnc = arzv__mjig
                        ccj__vcmce.append(ofzyt__jjhnc)
                    elif mlhg__evcl[0] in partition_names and not isinstance(
                        mlhg__evcl[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            ofzyt__jjhnc = (
                                f"('{mlhg__evcl[0]}', '{mlhg__evcl[1]}', '{mlhg__evcl[2]}')"
                                )
                        else:
                            ofzyt__jjhnc = arzv__mjig
                        ccj__vcmce.append(ofzyt__jjhnc)
            sxye__djw = ''
            if ccj__vcmce:
                if output_dnf:
                    sxye__djw = ', '.join(ccj__vcmce)
                else:
                    sxye__djw = ' & '.join(ccj__vcmce)
            else:
                mlx__zhtnr = True
            wod__ffr = ' & '.join(tcyd__boe)
            if sxye__djw:
                if output_dnf:
                    prf__tizoj.append(f'[{sxye__djw}]')
                else:
                    prf__tizoj.append(f'({sxye__djw})')
            jnkob__ikpdl.append(f'({wod__ffr})')
        if output_dnf:
            gafh__ctshm = ', '.join(prf__tizoj)
        else:
            gafh__ctshm = ' | '.join(prf__tizoj)
        ity__idn = ' | '.join(jnkob__ikpdl)
        if gafh__ctshm and not mlx__zhtnr:
            if output_dnf:
                cqr__iwaf = f'[{gafh__ctshm}]'
            else:
                cqr__iwaf = f'({gafh__ctshm})'
        prm__zjnia = f'({ity__idn})'
    return cqr__iwaf, prm__zjnia


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    qpny__vmwp = filter_val[0]
    bbeh__ermbn = col_types[orig_colname_map[qpny__vmwp]]
    nqsl__hlit = bodo.utils.typing.element_type(bbeh__ermbn)
    if source == 'parquet' and qpny__vmwp in partition_names:
        if nqsl__hlit == types.unicode_type:
            xewi__swh = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(nqsl__hlit, types.Integer):
            xewi__swh = f'.cast(pyarrow.{nqsl__hlit.name}(), safe=False)'
        else:
            xewi__swh = ''
    else:
        xewi__swh = ''
    htowi__klj = typemap[filter_val[2].name]
    if isinstance(htowi__klj, (types.List, types.Set)):
        ebq__zbx = htowi__klj.dtype
    elif is_array_typ(htowi__klj):
        ebq__zbx = htowi__klj.dtype
    else:
        ebq__zbx = htowi__klj
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(nqsl__hlit,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ebq__zbx,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([nqsl__hlit, ebq__zbx]):
        if not bodo.utils.typing.is_safe_arrow_cast(nqsl__hlit, ebq__zbx):
            raise BodoError(
                f'Unsupported Arrow cast from {nqsl__hlit} to {ebq__zbx} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if nqsl__hlit == types.unicode_type and ebq__zbx in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif ebq__zbx == types.unicode_type and nqsl__hlit in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            if isinstance(htowi__klj, (types.List, types.Set)):
                iuqje__wae = 'list' if isinstance(htowi__klj, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {iuqje__wae} values with isin filter pushdown.'
                    )
            return xewi__swh, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif nqsl__hlit == bodo.datetime_date_type and ebq__zbx in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif ebq__zbx == bodo.datetime_date_type and nqsl__hlit in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return xewi__swh, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return xewi__swh, ''
