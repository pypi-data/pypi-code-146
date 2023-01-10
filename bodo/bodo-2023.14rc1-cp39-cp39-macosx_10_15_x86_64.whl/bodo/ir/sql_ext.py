"""
Implementation of pd.read_sql in Bodo.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
from typing import Any, List, Optional
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.table import Table, TableType
from bodo.io.helpers import PyArrowTableSchemaType, is_nullable
from bodo.io.parquet_pio import ParquetPredicateType
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception
if bodo.utils.utils.has_pyarrow():
    import llvmlite.binding as ll
    from bodo.io import arrow_cpp
    ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
    ll.add_symbol('iceberg_pq_read', arrow_cpp.iceberg_pq_read)
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request: str, connection: str, df_out,
        df_colnames, out_vars, out_types, converted_colnames: List[str],
        db_type: str, loc, unsupported_columns: List[str],
        unsupported_arrow_types: List[pa.DataType], is_select_query: bool,
        has_side_effects: bool, index_column_name: str, index_column_type,
        database_schema: Optional[str], pyarrow_schema: Optional[pa.Schema],
        is_merge_into: bool, file_list_type, snapshot_id_type):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.is_select_query = is_select_query
        self.has_side_effects = has_side_effects
        self.index_column_name = index_column_name
        self.index_column_type = index_column_type
        self.out_used_cols = list(range(len(df_colnames)))
        self.database_schema = database_schema
        self.pyarrow_schema = pyarrow_schema
        self.is_merge_into = is_merge_into
        self.is_live_table = True
        self.file_list_live = is_merge_into
        self.snapshot_id_live = is_merge_into
        if is_merge_into:
            self.file_list_type = file_list_type
            self.snapshot_id_type = snapshot_id_type
        else:
            self.file_list_type = types.none
            self.snapshot_id_type = types.none

    def __repr__(self):
        dccp__dqnrx = tuple(wsyy__yrqg.name for wsyy__yrqg in self.out_vars)
        return (
            f'{dccp__dqnrx} = SQLReader(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_schema={self.pyarrow_schema}, is_merge_into={self.is_merge_into})'
            )


def parse_dbtype(con_str):
    cgr__nyp = urlparse(con_str)
    db_type = cgr__nyp.scheme
    xlvt__vhc = cgr__nyp.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', xlvt__vhc
    if db_type == 'mysql+pymysql':
        return 'mysql', xlvt__vhc
    if con_str.startswith('iceberg+glue') or cgr__nyp.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', xlvt__vhc
    return db_type, xlvt__vhc


def remove_iceberg_prefix(con):
    import sys
    if sys.version_info.minor < 9:
        if con.startswith('iceberg+'):
            con = con[len('iceberg+'):]
        if con.startswith('iceberg://'):
            con = con[len('iceberg://'):]
    else:
        con = con.removeprefix('iceberg+').removeprefix('iceberg://')
    return con


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    vbnnl__zfqgu = sql_node.out_vars[0].name
    bcfin__nrdrd = sql_node.out_vars[1].name
    mxqvs__lhlpm = sql_node.out_vars[2].name if len(sql_node.out_vars
        ) > 2 else None
    kei__yma = sql_node.out_vars[3].name if len(sql_node.out_vars
        ) > 3 else None
    if (not sql_node.has_side_effects and vbnnl__zfqgu not in lives and 
        bcfin__nrdrd not in lives and mxqvs__lhlpm not in lives and 
        kei__yma not in lives):
        return None
    if vbnnl__zfqgu not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
        sql_node.is_live_table = False
    if bcfin__nrdrd not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    if mxqvs__lhlpm not in lives:
        sql_node.file_list_live = False
        sql_node.file_list_type = types.none
    if kei__yma not in lives:
        sql_node.snapshot_id_live = False
        sql_node.snapshot_id_type = types.none
    return sql_node


def sql_distributed_run(sql_node: SqlReader, array_dists, typemap,
    calltypes, typingctx, targetctx, is_independent=False,
    meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        shnr__ivls = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        bryis__ixzc = []
        dict_encoded_cols = []
        for ixlea__ivemv in sql_node.out_used_cols:
            rphv__rhad = sql_node.df_colnames[ixlea__ivemv]
            bryis__ixzc.append(rphv__rhad)
            if isinstance(sql_node.out_types[ixlea__ivemv], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(rphv__rhad)
        if sql_node.index_column_name:
            bryis__ixzc.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(sql_node.index_column_name)
        zxf__xtu = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', shnr__ivls,
            zxf__xtu, bryis__ixzc)
        if dict_encoded_cols:
            vefwm__nibv = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                vefwm__nibv, zxf__xtu, dict_encoded_cols)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        hbipc__yljxo = set(sql_node.unsupported_columns)
        fng__somi = set(sql_node.out_used_cols)
        xjq__bhxvh = fng__somi & hbipc__yljxo
        if xjq__bhxvh:
            ndclt__toksk = sorted(xjq__bhxvh)
            tuy__nsi = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            faw__hec = 0
            for zdzyq__crxl in ndclt__toksk:
                while sql_node.unsupported_columns[faw__hec] != zdzyq__crxl:
                    faw__hec += 1
                tuy__nsi.append(
                    f"Column '{sql_node.original_df_colnames[zdzyq__crxl]}' with unsupported arrow type {sql_node.unsupported_arrow_types[faw__hec]}"
                    )
                faw__hec += 1
            gxlc__gsv = '\n'.join(tuy__nsi)
            raise BodoError(gxlc__gsv, loc=sql_node.loc)
    if sql_node.limit is None and (not meta_head_only_info or 
        meta_head_only_info[0] is None):
        limit = None
    elif sql_node.limit is None:
        limit = meta_head_only_info[0]
    elif not meta_head_only_info or meta_head_only_info[0] is None:
        limit = sql_node.limit
    else:
        limit = min(limit, meta_head_only_info[0])
    gik__uwqs, yif__bbx = bodo.ir.connector.generate_filter_map(sql_node.
        filters)
    qlbgi__duy = ', '.join(gik__uwqs.values())
    ple__ecz = (
        f'def sql_impl(sql_request, conn, database_schema, {qlbgi__duy}):\n')
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        if sql_node.filters:
            kou__jsnv = []
            for avd__rhwvy in sql_node.filters:
                zoj__rqpfz = []
                for mdm__ppaab in avd__rhwvy:
                    igel__oxi, fmwje__rps = mdm__ppaab[0], mdm__ppaab[2]
                    igel__oxi = convert_col_name(igel__oxi, sql_node.
                        converted_colnames)
                    igel__oxi = '\\"' + igel__oxi + '\\"'
                    jxhr__zxdv = '{' + gik__uwqs[mdm__ppaab[2].name
                        ] + '}' if isinstance(mdm__ppaab[2], ir.Var
                        ) else fmwje__rps
                    if mdm__ppaab[1] in ('startswith', 'endswith'):
                        tdb__qzn = ['(', mdm__ppaab[1], '(', igel__oxi, ',',
                            jxhr__zxdv, ')', ')']
                    else:
                        tdb__qzn = ['(', igel__oxi, mdm__ppaab[1],
                            jxhr__zxdv, ')']
                    zoj__rqpfz.append(' '.join(tdb__qzn))
                kou__jsnv.append(' ( ' + ' AND '.join(zoj__rqpfz) + ' ) ')
            hcq__kdqpr = ' WHERE ' + ' OR '.join(kou__jsnv)
            for ixlea__ivemv, amcej__okq in enumerate(gik__uwqs.values()):
                ple__ecz += (
                    f'    {amcej__okq} = get_sql_literal({amcej__okq})\n')
            ple__ecz += f'    sql_request = f"{{sql_request}} {hcq__kdqpr}"\n'
        if sql_node.limit != limit:
            ple__ecz += f'    sql_request = f"{{sql_request}} LIMIT {limit}"\n'
    scxzp__apbf = ''
    if sql_node.db_type == 'iceberg':
        scxzp__apbf = qlbgi__duy
    ple__ecz += f"""    (total_rows, table_var, index_var, file_list, snapshot_id) = _sql_reader_py(sql_request, conn, database_schema, {scxzp__apbf})
"""
    trabh__dbb = {}
    exec(ple__ecz, {}, trabh__dbb)
    udd__vbm = trabh__dbb['sql_impl']
    xhx__ure = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        sql_node.index_column_name, sql_node.index_column_type, sql_node.
        out_used_cols, sql_node.converted_colnames, typingctx, targetctx,
        sql_node.db_type, limit, parallel, typemap, sql_node.filters,
        sql_node.pyarrow_schema, not sql_node.is_live_table, sql_node.
        is_select_query, sql_node.is_merge_into, is_independent)
    gcy__ufmnj = (types.none if sql_node.database_schema is None else
        string_type)
    hfuqs__jxo = compile_to_numba_ir(udd__vbm, {'_sql_reader_py': xhx__ure,
        'bcast_scalar': bcast_scalar, 'bcast': bcast, 'get_sql_literal':
        _get_snowflake_sql_literal}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=(string_type, string_type, gcy__ufmnj) + tuple(
        typemap[wsyy__yrqg.name] for wsyy__yrqg in yif__bbx), typemap=
        typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        yak__ikvet = [sql_node.df_colnames[ixlea__ivemv] for ixlea__ivemv in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            yak__ikvet.append(sql_node.index_column_name)
        if len(yak__ikvet) == 0:
            wlu__miyo = 'COUNT(*)'
        else:
            wlu__miyo = escape_column_names(yak__ikvet, sql_node.db_type,
                sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            ighc__hjtt = ('SELECT ' + wlu__miyo + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            ighc__hjtt = ('SELECT ' + wlu__miyo + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        ighc__hjtt = sql_node.sql_request
    replace_arg_nodes(hfuqs__jxo, [ir.Const(ighc__hjtt, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + yif__bbx)
    bon__epjn = hfuqs__jxo.body[:-3]
    if meta_head_only_info:
        bon__epjn[-5].target = meta_head_only_info[1]
    bon__epjn[-4].target = sql_node.out_vars[0]
    bon__epjn[-3].target = sql_node.out_vars[1]
    assert sql_node.has_side_effects or not (sql_node.index_column_name is
        None and not sql_node.is_live_table
        ), 'At most one of table and index should be dead if the SQL IR node is live and has no side effects'
    if sql_node.index_column_name is None:
        bon__epjn.pop(-3)
    elif not sql_node.is_live_table:
        bon__epjn.pop(-4)
    if sql_node.file_list_live:
        bon__epjn[-2].target = sql_node.out_vars[2]
    else:
        bon__epjn.pop(-2)
    if sql_node.snapshot_id_live:
        bon__epjn[-1].target = sql_node.out_vars[3]
    else:
        bon__epjn.pop(-1)
    return bon__epjn


def convert_col_name(col_name: str, converted_colnames: List[str]) ->str:
    if col_name in converted_colnames:
        return col_name.upper()
    return col_name


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type == 'snowflake':
        from bodo.io.snowflake import escape_col_name
        wlu__miyo = ', '.join(escape_col_name(convert_col_name(fud__ftxf,
            converted_colnames)) for fud__ftxf in col_names)
    elif db_type == 'oracle':
        yak__ikvet = []
        for fud__ftxf in col_names:
            yak__ikvet.append(convert_col_name(fud__ftxf, converted_colnames))
        wlu__miyo = ', '.join([f'"{fud__ftxf}"' for fud__ftxf in yak__ikvet])
    elif db_type == 'mysql':
        wlu__miyo = ', '.join([f'`{fud__ftxf}`' for fud__ftxf in col_names])
    else:
        wlu__miyo = ', '.join([f'"{fud__ftxf}"' for fud__ftxf in col_names])
    return wlu__miyo


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    fsney__equ = types.unliteral(filter_value)
    if fsney__equ == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(fsney__equ, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif isinstance(fsney__equ, bodo.PandasTimestampType):
        if fsney__equ.tz is None:
            zfpwh__txb = 'TIMESTAMP_NTZ'
        else:
            zfpwh__txb = 'TIMESTAMP_TZ'

        def impl(filter_value):
            zopym__yrmmf = filter_value.nanosecond
            cjh__rydmd = ''
            if zopym__yrmmf < 10:
                cjh__rydmd = '00'
            elif zopym__yrmmf < 100:
                cjh__rydmd = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{cjh__rydmd}{zopym__yrmmf}'::{zfpwh__txb}"
                )
        return impl
    elif fsney__equ == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {fsney__equ} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float, bodo.PandasTimestampType
    mhylf__kjnv = bodo.datetime_date_type, types.unicode_type, types.bool_
    fsney__equ = types.unliteral(filter_value)
    if (isinstance(fsney__equ, (types.List, types.Array, bodo.
        IntegerArrayType, bodo.FloatingArrayType, bodo.DatetimeArrayType)) or
        fsney__equ in (bodo.string_array_type, bodo.dict_str_arr_type, bodo
        .boolean_array, bodo.datetime_date_array_type)) and (isinstance(
        fsney__equ.dtype, scalar_isinstance) or fsney__equ.dtype in mhylf__kjnv
        ):

        def impl(filter_value):
            afkx__ycpaj = ', '.join([_get_snowflake_sql_literal_scalar(
                fud__ftxf) for fud__ftxf in filter_value])
            return f'({afkx__ycpaj})'
        return impl
    elif isinstance(fsney__equ, scalar_isinstance
        ) or fsney__equ in mhylf__kjnv:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {fsney__equ} used in filter pushdown.'
            )


def sql_remove_dead_column(sql_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(sql_node,
        column_live_map, equiv_vars, typemap, 'SQLReader', sql_node.
        df_colnames, require_one_column=sql_node.db_type not in ('iceberg',
        'snowflake'))


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
remove_dead_column_extensions[SqlReader] = sql_remove_dead_column
ir_extension_table_column_use[SqlReader
    ] = bodo.ir.connector.connector_table_column_use
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as wdbhf__qhz:
        qgo__jmtf = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(qgo__jmtf)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as wdbhf__qhz:
        qgo__jmtf = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(qgo__jmtf)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as wdbhf__qhz:
        qgo__jmtf = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(qgo__jmtf)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as wdbhf__qhz:
        qgo__jmtf = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(qgo__jmtf)


def req_limit(sql_request):
    import re
    xrk__xea = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    ehuds__fjut = xrk__xea.search(sql_request)
    if ehuds__fjut:
        return int(ehuds__fjut.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs: List[Any],
    index_column_name: Optional[str], index_column_type, out_used_cols:
    List[int], converted_colnames: List[str], typingctx, targetctx, db_type:
    str, limit: Optional[int], parallel: bool, typemap, filters: Optional[
    Any], pyarrow_schema: Optional[pa.Schema], is_dead_table: bool,
    is_select_query: bool, is_merge_into: bool, is_independent: bool):
    yrr__ncr = next_label()
    yak__ikvet = [col_names[ixlea__ivemv] for ixlea__ivemv in out_used_cols]
    dfeg__acyr = [col_typs[ixlea__ivemv] for ixlea__ivemv in out_used_cols]
    if index_column_name:
        yak__ikvet.append(index_column_name)
        dfeg__acyr.append(index_column_type)
    nqz__guww = None
    nvyku__bhqlq = None
    xpjel__xplc = types.none if is_dead_table else TableType(tuple(col_typs))
    scxzp__apbf = ''
    gik__uwqs = {}
    yif__bbx = []
    if filters and db_type == 'iceberg':
        gik__uwqs, yif__bbx = bodo.ir.connector.generate_filter_map(filters)
        scxzp__apbf = ', '.join(gik__uwqs.values())
    ple__ecz = (
        f'def sql_reader_py(sql_request, conn, database_schema, {scxzp__apbf}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from an Iceberg database'
        lauh__llg, qfzkt__tgxh = bodo.ir.connector.generate_arrow_filters(
            filters, gik__uwqs, yif__bbx, col_names, col_names, col_typs,
            typemap, 'iceberg')
        nvgc__mdqms = -1
        if is_merge_into and col_names.index('_bodo_row_id') in out_used_cols:
            nvgc__mdqms = col_names.index('_bodo_row_id')
        selected_cols: List[int] = [pyarrow_schema.get_field_index(
            col_names[ixlea__ivemv]) for ixlea__ivemv in out_used_cols if 
            ixlea__ivemv != nvgc__mdqms]
        dthxi__mgpj = {qab__ybu: ixlea__ivemv for ixlea__ivemv, qab__ybu in
            enumerate(selected_cols)}
        nullable_cols = [int(is_nullable(col_typs[ixlea__ivemv])) for
            ixlea__ivemv in selected_cols]
        kfjdt__fvs = [ixlea__ivemv for ixlea__ivemv in selected_cols if 
            col_typs[ixlea__ivemv] == bodo.dict_str_arr_type]
        ili__tqib = (
            f'dict_str_cols_arr_{yrr__ncr}.ctypes, np.int32({len(kfjdt__fvs)})'
             if kfjdt__fvs else '0, 0')
        vtti__aee = ',' if scxzp__apbf else ''
        ple__ecz += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{lauh__llg}", "{qfzkt__tgxh}", ({scxzp__apbf}{vtti__aee}))
  out_table, total_rows, file_list, snapshot_id = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{yrr__ncr}.ctypes,
    {len(selected_cols)},
    nullable_cols_arr_{yrr__ncr}.ctypes,
    pyarrow_schema_{yrr__ncr},
    {ili__tqib},
    {is_merge_into},
  )
"""
        if parallel:
            ple__ecz += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            ple__ecz += f'  local_rows = total_rows\n'
        nqz__guww = None
        if not is_dead_table:
            nqz__guww = []
            qim__ahyn = 0
            for ixlea__ivemv in range(len(col_names)):
                if qim__ahyn < len(out_used_cols
                    ) and ixlea__ivemv == out_used_cols[qim__ahyn]:
                    if ixlea__ivemv == nvgc__mdqms:
                        nqz__guww.append(len(selected_cols))
                    else:
                        nqz__guww.append(dthxi__mgpj[ixlea__ivemv])
                    qim__ahyn += 1
                else:
                    nqz__guww.append(-1)
            nqz__guww = np.array(nqz__guww, dtype=np.int64)
        if is_dead_table:
            ple__ecz += '  table_var = None\n'
        else:
            ple__ecz += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{yrr__ncr}, py_table_type_{yrr__ncr})
"""
            if len(out_used_cols) == 0:
                ple__ecz += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        bcfin__nrdrd = 'None'
        if index_column_name is not None:
            vkfas__ogv = len(out_used_cols) + 1 if not is_dead_table else 0
            bcfin__nrdrd = (
                f'info_to_array(info_from_table(out_table, {vkfas__ogv}), index_col_typ)'
                )
        ple__ecz += f'  index_var = {bcfin__nrdrd}\n'
        ple__ecz += f'  delete_table(out_table)\n'
        ple__ecz += f'  ev.finalize()\n'
        ple__ecz += (
            '  return (total_rows, table_var, index_var, file_list, snapshot_id)\n'
            )
    elif db_type == 'snowflake':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from Snowflake'
        if is_select_query:
            myn__hvbl = []
            for col_name in yak__ikvet:
                ruzh__fuqa = convert_col_name(col_name, converted_colnames)
                faw__hec = pyarrow_schema.get_field_index(ruzh__fuqa)
                if faw__hec < 0:
                    raise BodoError(
                        f'SQLReader Snowflake: Column {ruzh__fuqa} is not in source schema'
                        )
                myn__hvbl.append(pyarrow_schema.field(faw__hec))
            pyarrow_schema = pa.schema(myn__hvbl)
        hoca__kciq = {qab__ybu: ixlea__ivemv for ixlea__ivemv, qab__ybu in
            enumerate(out_used_cols)}
        kbg__fus = [hoca__kciq[ixlea__ivemv] for ixlea__ivemv in
            out_used_cols if col_typs[ixlea__ivemv] == dict_str_arr_type]
        nullable_cols = [int(is_nullable(col_typs[ixlea__ivemv])) for
            ixlea__ivemv in out_used_cols]
        if index_column_name:
            nullable_cols.append(int(is_nullable(index_column_type)))
        odoq__wetli = np.array(kbg__fus, dtype=np.int32)
        bjqun__sjkx = np.array(nullable_cols, dtype=np.int32)
        ple__ecz += f"""  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = snowflake_read(
    unicode_to_utf8(sql_request),
    unicode_to_utf8(conn),
    {parallel},
    {is_independent},
    pyarrow_schema_{yrr__ncr},
    {len(bjqun__sjkx)},
    nullable_cols_array.ctypes,
    snowflake_dict_cols_array.ctypes,
    {len(odoq__wetli)},
    total_rows_np.ctypes,
    {is_select_query and len(yak__ikvet) == 0},
    {is_select_query},
  )
  check_and_propagate_cpp_exception()
"""
        ple__ecz += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            ple__ecz += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            ple__ecz += f'  local_rows = total_rows\n'
        if index_column_name:
            ple__ecz += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            ple__ecz += '  index_var = None\n'
        if not is_dead_table:
            faw__hec = []
            qim__ahyn = 0
            for ixlea__ivemv in range(len(col_names)):
                if qim__ahyn < len(out_used_cols
                    ) and ixlea__ivemv == out_used_cols[qim__ahyn]:
                    faw__hec.append(qim__ahyn)
                    qim__ahyn += 1
                else:
                    faw__hec.append(-1)
            nqz__guww = np.array(faw__hec, dtype=np.int64)
            ple__ecz += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{yrr__ncr}, py_table_type_{yrr__ncr})
"""
            if len(out_used_cols) == 0:
                if index_column_name:
                    ple__ecz += (
                        f'  table_var = set_table_len(table_var, len(index_var))\n'
                        )
                else:
                    ple__ecz += (
                        f'  table_var = set_table_len(table_var, local_rows)\n'
                        )
        else:
            ple__ecz += '  table_var = None\n'
        ple__ecz += '  delete_table(out_table)\n'
        ple__ecz += '  ev.finalize()\n'
        ple__ecz += '  return (total_rows, table_var, index_var, None, None)\n'
    else:
        if not is_dead_table:
            ple__ecz += f"""  type_usecols_offsets_arr_{yrr__ncr}_2 = type_usecols_offsets_arr_{yrr__ncr}
"""
            nvyku__bhqlq = np.array(out_used_cols, dtype=np.int64)
        ple__ecz += '  df_typeref_2 = df_typeref\n'
        ple__ecz += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            ple__ecz += '  pymysql_check()\n'
        elif db_type == 'oracle':
            ple__ecz += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            ple__ecz += '  psycopg2_check()\n'
        if parallel:
            ple__ecz += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                ple__ecz += f'  nb_row = {limit}\n'
            else:
                ple__ecz += '  with objmode(nb_row="int64"):\n'
                ple__ecz += f'     if rank == {MPI_ROOT}:\n'
                ple__ecz += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                ple__ecz += '         frame = pd.read_sql(sql_cons, conn)\n'
                ple__ecz += '         nb_row = frame.iat[0,0]\n'
                ple__ecz += '     else:\n'
                ple__ecz += '         nb_row = 0\n'
                ple__ecz += '  nb_row = bcast_scalar(nb_row)\n'
            ple__ecz += f"""  with objmode(table_var=py_table_type_{yrr__ncr}, index_var=index_col_typ):
"""
            ple__ecz += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                ple__ecz += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                ple__ecz += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            ple__ecz += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            ple__ecz += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            ple__ecz += f"""  with objmode(table_var=py_table_type_{yrr__ncr}, index_var=index_col_typ):
"""
            ple__ecz += '    df_ret = pd.read_sql(sql_request, conn)\n'
            ple__ecz += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            ple__ecz += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            ple__ecz += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            ple__ecz += '    index_var = None\n'
        if not is_dead_table:
            ple__ecz += f'    arrs = []\n'
            ple__ecz += f'    for i in range(df_ret.shape[1]):\n'
            ple__ecz += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            ple__ecz += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{yrr__ncr}_2, {len(col_names)})
"""
        else:
            ple__ecz += '    table_var = None\n'
        ple__ecz += '  return (-1, table_var, index_var, None, None)\n'
    arobh__lhwaz = globals()
    arobh__lhwaz.update({'bodo': bodo, f'py_table_type_{yrr__ncr}':
        xpjel__xplc, 'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        arobh__lhwaz.update({f'table_idx_{yrr__ncr}': nqz__guww,
            f'pyarrow_schema_{yrr__ncr}': pyarrow_schema, 'unicode_to_utf8':
            unicode_to_utf8, 'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'get_node_portion': bodo.libs.distributed_api.
            get_node_portion})
    if db_type == 'iceberg':
        arobh__lhwaz.update({f'selected_cols_arr_{yrr__ncr}': np.array(
            selected_cols, np.int32), f'nullable_cols_arr_{yrr__ncr}': np.
            array(nullable_cols, np.int32), f'dict_str_cols_arr_{yrr__ncr}':
            np.array(kfjdt__fvs, np.int32), f'py_table_type_{yrr__ncr}':
            xpjel__xplc, 'get_filters_pyobject': bodo.io.parquet_pio.
            get_filters_pyobject, 'iceberg_read': _iceberg_pq_read})
    elif db_type == 'snowflake':
        arobh__lhwaz.update({'np': np, 'snowflake_read': _snowflake_read,
            'nullable_cols_array': bjqun__sjkx, 'snowflake_dict_cols_array':
            odoq__wetli})
    else:
        arobh__lhwaz.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(dfeg__acyr), bodo.RangeIndexType(None),
            tuple(yak__ikvet)), 'Table': Table,
            f'type_usecols_offsets_arr_{yrr__ncr}': nvyku__bhqlq})
    trabh__dbb = {}
    exec(ple__ecz, arobh__lhwaz, trabh__dbb)
    xhx__ure = trabh__dbb['sql_reader_py']
    mbajf__jqyfx = numba.njit(xhx__ure)
    compiled_funcs.append(mbajf__jqyfx)
    return mbajf__jqyfx


parquet_predicate_type = ParquetPredicateType()
pyarrow_schema_type = PyArrowTableSchemaType()


@intrinsic
def _iceberg_pq_read(typingctx, conn_str, db_schema, sql_request_str,
    parallel, limit, dnf_filters, expr_filters, selected_cols,
    num_selected_cols, nullable_cols, pyarrow_schema, dict_encoded_cols,
    num_dict_encoded_cols, is_merge_into_cow):

    def codegen(context, builder, signature, args):
        ahk__dvh = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(1), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(64).as_pointer()])
        mkx__ybadn = cgutils.get_or_insert_function(builder.module,
            ahk__dvh, name='iceberg_pq_read')
        xtj__qka = cgutils.alloca_once(builder, lir.IntType(64))
        rfd__mgqr = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ams__euhf = cgutils.alloca_once(builder, lir.IntType(64))
        gvyxk__mwq = args + (xtj__qka, rfd__mgqr, ams__euhf)
        rpkrw__bduvg = builder.call(mkx__ybadn, gvyxk__mwq)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        yuk__pqdp = builder.load(rfd__mgqr)
        uiht__dwiz = cgutils.create_struct_proxy(types.pyobject_of_list_type)(
            context, builder)
        shtc__ehha = context.get_python_api(builder)
        uiht__dwiz.meminfo = shtc__ehha.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), yuk__pqdp)
        uiht__dwiz.pyobj = yuk__pqdp
        shtc__ehha.decref(yuk__pqdp)
        tnjz__rfpb = [rpkrw__bduvg, builder.load(xtj__qka), uiht__dwiz.
            _getvalue(), builder.load(ams__euhf)]
        return context.make_tuple(builder, dimb__ugllo, tnjz__rfpb)
    dimb__ugllo = types.Tuple([table_type, types.int64, types.
        pyobject_of_list_type, types.int64])
    vjjt__xjwf = dimb__ugllo(types.voidptr, types.voidptr, types.voidptr,
        types.boolean, types.int64, parquet_predicate_type,
        parquet_predicate_type, types.voidptr, types.int32, types.voidptr,
        pyarrow_schema_type, types.voidptr, types.int32, types.boolean)
    return vjjt__xjwf, codegen


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.boolean,
    pyarrow_schema_type, types.int64, types.voidptr, types.voidptr, types.
    int32, types.voidptr, types.boolean, types.boolean))
