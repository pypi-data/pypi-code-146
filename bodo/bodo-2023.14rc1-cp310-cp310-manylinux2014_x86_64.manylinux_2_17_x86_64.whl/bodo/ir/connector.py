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
    bgzh__ipo = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    pqnvh__hbvfu = []
    for lck__svpar, nbcu__lobk in enumerate(node.out_vars):
        wpqg__pya = typemap[nbcu__lobk.name]
        if wpqg__pya == types.none:
            continue
        ezkzp__amzw = lck__svpar == 0 and node.connector_typ in ('parquet',
            'sql') and not node.is_live_table
        jydu__dcgmv = node.connector_typ == 'sql' and lck__svpar > 1
        if not (ezkzp__amzw or jydu__dcgmv):
            rlzb__kwupr = array_analysis._gen_shape_call(equiv_set,
                nbcu__lobk, wpqg__pya.ndim, None, bgzh__ipo)
            equiv_set.insert_equiv(nbcu__lobk, rlzb__kwupr)
            pqnvh__hbvfu.append(rlzb__kwupr[0])
            equiv_set.define(nbcu__lobk, set())
    if len(pqnvh__hbvfu) > 1:
        equiv_set.insert_equiv(*pqnvh__hbvfu)
    return [], bgzh__ipo


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        mcwxp__sdza = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        mcwxp__sdza = Distribution.OneD_Var
    else:
        mcwxp__sdza = Distribution.OneD
    for ymhmb__mduf in node.out_vars:
        if ymhmb__mduf.name in array_dists:
            mcwxp__sdza = Distribution(min(mcwxp__sdza.value, array_dists[
                ymhmb__mduf.name].value))
    for ymhmb__mduf in node.out_vars:
        array_dists[ymhmb__mduf.name] = mcwxp__sdza


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
    for nbcu__lobk, wpqg__pya in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(nbcu__lobk.name, wpqg__pya, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    hqp__tpp = []
    for nbcu__lobk in node.out_vars:
        hbfdi__sxmzf = visit_vars_inner(nbcu__lobk, callback, cbdata)
        hqp__tpp.append(hbfdi__sxmzf)
    node.out_vars = hqp__tpp
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for xuid__sgunr in node.filters:
            for lck__svpar in range(len(xuid__sgunr)):
                ztero__ywvmc = xuid__sgunr[lck__svpar]
                xuid__sgunr[lck__svpar] = ztero__ywvmc[0], ztero__ywvmc[1
                    ], visit_vars_inner(ztero__ywvmc[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({ymhmb__mduf.name for ymhmb__mduf in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for duxik__nad in node.filters:
            for ymhmb__mduf in duxik__nad:
                if isinstance(ymhmb__mduf[2], ir.Var):
                    use_set.add(ymhmb__mduf[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    vnolg__zqvxj = set(ymhmb__mduf.name for ymhmb__mduf in node.out_vars)
    return set(), vnolg__zqvxj


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    hqp__tpp = []
    for nbcu__lobk in node.out_vars:
        hbfdi__sxmzf = replace_vars_inner(nbcu__lobk, var_dict)
        hqp__tpp.append(hbfdi__sxmzf)
    node.out_vars = hqp__tpp
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for xuid__sgunr in node.filters:
            for lck__svpar in range(len(xuid__sgunr)):
                ztero__ywvmc = xuid__sgunr[lck__svpar]
                xuid__sgunr[lck__svpar] = ztero__ywvmc[0], ztero__ywvmc[1
                    ], replace_vars_inner(ztero__ywvmc[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for nbcu__lobk in node.out_vars:
        emkp__jdr = definitions[nbcu__lobk.name]
        if node not in emkp__jdr:
            emkp__jdr.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        likmy__xwb = [ymhmb__mduf[2] for duxik__nad in filters for
            ymhmb__mduf in duxik__nad]
        fpn__oos = set()
        for ige__qzu in likmy__xwb:
            if isinstance(ige__qzu, ir.Var):
                if ige__qzu.name not in fpn__oos:
                    filter_vars.append(ige__qzu)
                fpn__oos.add(ige__qzu.name)
        return {ymhmb__mduf.name: f'f{lck__svpar}' for lck__svpar,
            ymhmb__mduf in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {lck__svpar for lck__svpar in used_columns if lck__svpar <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    pjbyr__odjmg = {}
    for lck__svpar, xlzy__vvzn in enumerate(df_type.data):
        if isinstance(xlzy__vvzn, bodo.IntegerArrayType):
            jdry__noax = xlzy__vvzn.get_pandas_scalar_type_instance
            if jdry__noax not in pjbyr__odjmg:
                pjbyr__odjmg[jdry__noax] = []
            pjbyr__odjmg[jdry__noax].append(df.columns[lck__svpar])
    for wpqg__pya, chnmz__rumy in pjbyr__odjmg.items():
        df[chnmz__rumy] = df[chnmz__rumy].astype(wpqg__pya)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    ovtf__gzlq = node.out_vars[0].name
    assert isinstance(typemap[ovtf__gzlq], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, nrv__npwmq, cadim__uecdz = get_live_column_nums_block(
            column_live_map, equiv_vars, ovtf__gzlq)
        if not (nrv__npwmq or cadim__uecdz):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    nyx__qnmb = False
    if array_dists is not None:
        obeil__ztyty = node.out_vars[0].name
        nyx__qnmb = array_dists[obeil__ztyty] in (Distribution.OneD,
            Distribution.OneD_Var)
        moh__wdvfd = node.out_vars[1].name
        assert typemap[moh__wdvfd
            ] == types.none or not nyx__qnmb or array_dists[moh__wdvfd] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return nyx__qnmb


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    emcb__adhxs = 'None'
    bem__ieavr = 'None'
    if filters:
        zdae__kekd = []
        mnu__jved = []
        vikas__brk = False
        orig_colname_map = {xoqd__ppia: lck__svpar for lck__svpar,
            xoqd__ppia in enumerate(col_names)}
        for xuid__sgunr in filters:
            vyjjg__krenn = []
            vbnoz__otnu = []
            for ymhmb__mduf in xuid__sgunr:
                if isinstance(ymhmb__mduf[2], ir.Var):
                    qepan__ygvj, efor__zxpzr = determine_filter_cast(
                        original_out_types, typemap, ymhmb__mduf,
                        orig_colname_map, partition_names, source)
                    if ymhmb__mduf[1] == 'in':
                        rpvby__orsd = (
                            f"(ds.field('{ymhmb__mduf[0]}').isin({filter_map[ymhmb__mduf[2].name]}))"
                            )
                    else:
                        rpvby__orsd = (
                            f"(ds.field('{ymhmb__mduf[0]}'){qepan__ygvj} {ymhmb__mduf[1]} ds.scalar({filter_map[ymhmb__mduf[2].name]}){efor__zxpzr})"
                            )
                else:
                    assert ymhmb__mduf[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if ymhmb__mduf[1] == 'is not':
                        wqul__orsg = '~'
                    else:
                        wqul__orsg = ''
                    rpvby__orsd = (
                        f"({wqul__orsg}ds.field('{ymhmb__mduf[0]}').is_null())"
                        )
                vbnoz__otnu.append(rpvby__orsd)
                if not vikas__brk:
                    if ymhmb__mduf[0] in partition_names and isinstance(
                        ymhmb__mduf[2], ir.Var):
                        if output_dnf:
                            mqean__cerh = (
                                f"('{ymhmb__mduf[0]}', '{ymhmb__mduf[1]}', {filter_map[ymhmb__mduf[2].name]})"
                                )
                        else:
                            mqean__cerh = rpvby__orsd
                        vyjjg__krenn.append(mqean__cerh)
                    elif ymhmb__mduf[0] in partition_names and not isinstance(
                        ymhmb__mduf[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            mqean__cerh = (
                                f"('{ymhmb__mduf[0]}', '{ymhmb__mduf[1]}', '{ymhmb__mduf[2]}')"
                                )
                        else:
                            mqean__cerh = rpvby__orsd
                        vyjjg__krenn.append(mqean__cerh)
            pyocg__oimb = ''
            if vyjjg__krenn:
                if output_dnf:
                    pyocg__oimb = ', '.join(vyjjg__krenn)
                else:
                    pyocg__oimb = ' & '.join(vyjjg__krenn)
            else:
                vikas__brk = True
            dnu__fev = ' & '.join(vbnoz__otnu)
            if pyocg__oimb:
                if output_dnf:
                    zdae__kekd.append(f'[{pyocg__oimb}]')
                else:
                    zdae__kekd.append(f'({pyocg__oimb})')
            mnu__jved.append(f'({dnu__fev})')
        if output_dnf:
            gdaa__cfe = ', '.join(zdae__kekd)
        else:
            gdaa__cfe = ' | '.join(zdae__kekd)
        ccmyh__vmr = ' | '.join(mnu__jved)
        if gdaa__cfe and not vikas__brk:
            if output_dnf:
                emcb__adhxs = f'[{gdaa__cfe}]'
            else:
                emcb__adhxs = f'({gdaa__cfe})'
        bem__ieavr = f'({ccmyh__vmr})'
    return emcb__adhxs, bem__ieavr


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    bqow__sei = filter_val[0]
    xfyd__lkee = col_types[orig_colname_map[bqow__sei]]
    ycec__kfcdx = bodo.utils.typing.element_type(xfyd__lkee)
    if source == 'parquet' and bqow__sei in partition_names:
        if ycec__kfcdx == types.unicode_type:
            ekgxe__zjmw = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(ycec__kfcdx, types.Integer):
            ekgxe__zjmw = f'.cast(pyarrow.{ycec__kfcdx.name}(), safe=False)'
        else:
            ekgxe__zjmw = ''
    else:
        ekgxe__zjmw = ''
    iwf__erwn = typemap[filter_val[2].name]
    if isinstance(iwf__erwn, (types.List, types.Set)):
        mruw__dex = iwf__erwn.dtype
    elif is_array_typ(iwf__erwn):
        mruw__dex = iwf__erwn.dtype
    else:
        mruw__dex = iwf__erwn
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ycec__kfcdx,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(mruw__dex,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([ycec__kfcdx, mruw__dex]):
        if not bodo.utils.typing.is_safe_arrow_cast(ycec__kfcdx, mruw__dex):
            raise BodoError(
                f'Unsupported Arrow cast from {ycec__kfcdx} to {mruw__dex} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if ycec__kfcdx == types.unicode_type and mruw__dex in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif mruw__dex == types.unicode_type and ycec__kfcdx in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            if isinstance(iwf__erwn, (types.List, types.Set)):
                mpnuj__iqc = 'list' if isinstance(iwf__erwn, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {mpnuj__iqc} values with isin filter pushdown.'
                    )
            return ekgxe__zjmw, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif ycec__kfcdx == bodo.datetime_date_type and mruw__dex in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif mruw__dex == bodo.datetime_date_type and ycec__kfcdx in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ekgxe__zjmw, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return ekgxe__zjmw, ''
