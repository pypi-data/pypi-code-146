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
    hsr__oki = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    yrop__upvra = []
    for oxyti__ltnt, azgdr__gtki in enumerate(node.out_vars):
        qrwxj__zix = typemap[azgdr__gtki.name]
        if qrwxj__zix == types.none:
            continue
        vmx__urzcw = oxyti__ltnt == 0 and node.connector_typ in ('parquet',
            'sql') and not node.is_live_table
        pgfto__khb = node.connector_typ == 'sql' and oxyti__ltnt > 1
        if not (vmx__urzcw or pgfto__khb):
            ozfyl__pxv = array_analysis._gen_shape_call(equiv_set,
                azgdr__gtki, qrwxj__zix.ndim, None, hsr__oki)
            equiv_set.insert_equiv(azgdr__gtki, ozfyl__pxv)
            yrop__upvra.append(ozfyl__pxv[0])
            equiv_set.define(azgdr__gtki, set())
    if len(yrop__upvra) > 1:
        equiv_set.insert_equiv(*yrop__upvra)
    return [], hsr__oki


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        xgsq__nlf = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        xgsq__nlf = Distribution.OneD_Var
    else:
        xgsq__nlf = Distribution.OneD
    for brsx__xhag in node.out_vars:
        if brsx__xhag.name in array_dists:
            xgsq__nlf = Distribution(min(xgsq__nlf.value, array_dists[
                brsx__xhag.name].value))
    for brsx__xhag in node.out_vars:
        array_dists[brsx__xhag.name] = xgsq__nlf


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
    for azgdr__gtki, qrwxj__zix in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(azgdr__gtki.name, qrwxj__zix, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    joub__ysw = []
    for azgdr__gtki in node.out_vars:
        mdy__smk = visit_vars_inner(azgdr__gtki, callback, cbdata)
        joub__ysw.append(mdy__smk)
    node.out_vars = joub__ysw
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for khlr__qitjt in node.filters:
            for oxyti__ltnt in range(len(khlr__qitjt)):
                pvw__rjz = khlr__qitjt[oxyti__ltnt]
                khlr__qitjt[oxyti__ltnt] = pvw__rjz[0], pvw__rjz[1
                    ], visit_vars_inner(pvw__rjz[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({brsx__xhag.name for brsx__xhag in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for jtd__gkltv in node.filters:
            for brsx__xhag in jtd__gkltv:
                if isinstance(brsx__xhag[2], ir.Var):
                    use_set.add(brsx__xhag[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    mucbk__tle = set(brsx__xhag.name for brsx__xhag in node.out_vars)
    return set(), mucbk__tle


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    joub__ysw = []
    for azgdr__gtki in node.out_vars:
        mdy__smk = replace_vars_inner(azgdr__gtki, var_dict)
        joub__ysw.append(mdy__smk)
    node.out_vars = joub__ysw
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for khlr__qitjt in node.filters:
            for oxyti__ltnt in range(len(khlr__qitjt)):
                pvw__rjz = khlr__qitjt[oxyti__ltnt]
                khlr__qitjt[oxyti__ltnt] = pvw__rjz[0], pvw__rjz[1
                    ], replace_vars_inner(pvw__rjz[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for azgdr__gtki in node.out_vars:
        qoh__efdj = definitions[azgdr__gtki.name]
        if node not in qoh__efdj:
            qoh__efdj.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        yodzc__lxmeb = [brsx__xhag[2] for jtd__gkltv in filters for
            brsx__xhag in jtd__gkltv]
        wyfwy__emvl = set()
        for tjiyf__cummw in yodzc__lxmeb:
            if isinstance(tjiyf__cummw, ir.Var):
                if tjiyf__cummw.name not in wyfwy__emvl:
                    filter_vars.append(tjiyf__cummw)
                wyfwy__emvl.add(tjiyf__cummw.name)
        return {brsx__xhag.name: f'f{oxyti__ltnt}' for oxyti__ltnt,
            brsx__xhag in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {oxyti__ltnt for oxyti__ltnt in used_columns if oxyti__ltnt <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    waid__yku = {}
    for oxyti__ltnt, rvlq__joly in enumerate(df_type.data):
        if isinstance(rvlq__joly, bodo.IntegerArrayType):
            stcb__fqve = rvlq__joly.get_pandas_scalar_type_instance
            if stcb__fqve not in waid__yku:
                waid__yku[stcb__fqve] = []
            waid__yku[stcb__fqve].append(df.columns[oxyti__ltnt])
    for qrwxj__zix, ygvpi__hmca in waid__yku.items():
        df[ygvpi__hmca] = df[ygvpi__hmca].astype(qrwxj__zix)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    ioe__kafz = node.out_vars[0].name
    assert isinstance(typemap[ioe__kafz], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, zgt__fgij, bixq__mjcp = get_live_column_nums_block(
            column_live_map, equiv_vars, ioe__kafz)
        if not (zgt__fgij or bixq__mjcp):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    ljdf__naz = False
    if array_dists is not None:
        ecws__urva = node.out_vars[0].name
        ljdf__naz = array_dists[ecws__urva] in (Distribution.OneD,
            Distribution.OneD_Var)
        cxjo__xqd = node.out_vars[1].name
        assert typemap[cxjo__xqd
            ] == types.none or not ljdf__naz or array_dists[cxjo__xqd] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return ljdf__naz


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    uvdxa__ewvef = 'None'
    yjfa__bcemx = 'None'
    if filters:
        zxj__drh = []
        dyhcp__tcjni = []
        qasx__cra = False
        orig_colname_map = {nkypk__vuf: oxyti__ltnt for oxyti__ltnt,
            nkypk__vuf in enumerate(col_names)}
        for khlr__qitjt in filters:
            nhg__twuwr = []
            vsyd__muqjm = []
            for brsx__xhag in khlr__qitjt:
                if isinstance(brsx__xhag[2], ir.Var):
                    bgrv__wmmow, bin__hrro = determine_filter_cast(
                        original_out_types, typemap, brsx__xhag,
                        orig_colname_map, partition_names, source)
                    if brsx__xhag[1] == 'in':
                        hvwio__eywhl = (
                            f"(ds.field('{brsx__xhag[0]}').isin({filter_map[brsx__xhag[2].name]}))"
                            )
                    else:
                        hvwio__eywhl = (
                            f"(ds.field('{brsx__xhag[0]}'){bgrv__wmmow} {brsx__xhag[1]} ds.scalar({filter_map[brsx__xhag[2].name]}){bin__hrro})"
                            )
                else:
                    assert brsx__xhag[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if brsx__xhag[1] == 'is not':
                        oqy__cfn = '~'
                    else:
                        oqy__cfn = ''
                    hvwio__eywhl = (
                        f"({oqy__cfn}ds.field('{brsx__xhag[0]}').is_null())")
                vsyd__muqjm.append(hvwio__eywhl)
                if not qasx__cra:
                    if brsx__xhag[0] in partition_names and isinstance(
                        brsx__xhag[2], ir.Var):
                        if output_dnf:
                            ngbb__hioq = (
                                f"('{brsx__xhag[0]}', '{brsx__xhag[1]}', {filter_map[brsx__xhag[2].name]})"
                                )
                        else:
                            ngbb__hioq = hvwio__eywhl
                        nhg__twuwr.append(ngbb__hioq)
                    elif brsx__xhag[0] in partition_names and not isinstance(
                        brsx__xhag[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            ngbb__hioq = (
                                f"('{brsx__xhag[0]}', '{brsx__xhag[1]}', '{brsx__xhag[2]}')"
                                )
                        else:
                            ngbb__hioq = hvwio__eywhl
                        nhg__twuwr.append(ngbb__hioq)
            vwe__ekml = ''
            if nhg__twuwr:
                if output_dnf:
                    vwe__ekml = ', '.join(nhg__twuwr)
                else:
                    vwe__ekml = ' & '.join(nhg__twuwr)
            else:
                qasx__cra = True
            subs__rmqp = ' & '.join(vsyd__muqjm)
            if vwe__ekml:
                if output_dnf:
                    zxj__drh.append(f'[{vwe__ekml}]')
                else:
                    zxj__drh.append(f'({vwe__ekml})')
            dyhcp__tcjni.append(f'({subs__rmqp})')
        if output_dnf:
            sevpp__boca = ', '.join(zxj__drh)
        else:
            sevpp__boca = ' | '.join(zxj__drh)
        bxg__thxa = ' | '.join(dyhcp__tcjni)
        if sevpp__boca and not qasx__cra:
            if output_dnf:
                uvdxa__ewvef = f'[{sevpp__boca}]'
            else:
                uvdxa__ewvef = f'({sevpp__boca})'
        yjfa__bcemx = f'({bxg__thxa})'
    return uvdxa__ewvef, yjfa__bcemx


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    krx__efm = filter_val[0]
    lka__eenr = col_types[orig_colname_map[krx__efm]]
    mbyi__zufv = bodo.utils.typing.element_type(lka__eenr)
    if source == 'parquet' and krx__efm in partition_names:
        if mbyi__zufv == types.unicode_type:
            acp__cre = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(mbyi__zufv, types.Integer):
            acp__cre = f'.cast(pyarrow.{mbyi__zufv.name}(), safe=False)'
        else:
            acp__cre = ''
    else:
        acp__cre = ''
    miiwp__aful = typemap[filter_val[2].name]
    if isinstance(miiwp__aful, (types.List, types.Set)):
        vrqz__skizf = miiwp__aful.dtype
    elif is_array_typ(miiwp__aful):
        vrqz__skizf = miiwp__aful.dtype
    else:
        vrqz__skizf = miiwp__aful
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(mbyi__zufv,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(vrqz__skizf,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([mbyi__zufv, vrqz__skizf]):
        if not bodo.utils.typing.is_safe_arrow_cast(mbyi__zufv, vrqz__skizf):
            raise BodoError(
                f'Unsupported Arrow cast from {mbyi__zufv} to {vrqz__skizf} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if mbyi__zufv == types.unicode_type and vrqz__skizf in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif vrqz__skizf == types.unicode_type and mbyi__zufv in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            if isinstance(miiwp__aful, (types.List, types.Set)):
                lrm__idqy = 'list' if isinstance(miiwp__aful, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {lrm__idqy} values with isin filter pushdown.'
                    )
            return acp__cre, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif mbyi__zufv == bodo.datetime_date_type and vrqz__skizf in (bodo
            .datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif vrqz__skizf == bodo.datetime_date_type and mbyi__zufv in (bodo
            .datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return acp__cre, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return acp__cre, ''
