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
        rwer__ghv = tuple(rxacn__hrhh.name for rxacn__hrhh in self.out_vars)
        return (
            f'{rwer__ghv} = SQLReader(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_schema={self.pyarrow_schema}, is_merge_into={self.is_merge_into})'
            )


def parse_dbtype(con_str):
    gdk__ivjs = urlparse(con_str)
    db_type = gdk__ivjs.scheme
    fcz__ktrnz = gdk__ivjs.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', fcz__ktrnz
    if db_type == 'mysql+pymysql':
        return 'mysql', fcz__ktrnz
    if con_str.startswith('iceberg+glue') or gdk__ivjs.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', fcz__ktrnz
    return db_type, fcz__ktrnz


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
    ahdyq__fydc = sql_node.out_vars[0].name
    bqp__viw = sql_node.out_vars[1].name
    jld__oab = sql_node.out_vars[2].name if len(sql_node.out_vars
        ) > 2 else None
    moxzz__uikgx = sql_node.out_vars[3].name if len(sql_node.out_vars
        ) > 3 else None
    if (not sql_node.has_side_effects and ahdyq__fydc not in lives and 
        bqp__viw not in lives and jld__oab not in lives and moxzz__uikgx not in
        lives):
        return None
    if ahdyq__fydc not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
        sql_node.is_live_table = False
    if bqp__viw not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    if jld__oab not in lives:
        sql_node.file_list_live = False
        sql_node.file_list_type = types.none
    if moxzz__uikgx not in lives:
        sql_node.snapshot_id_live = False
        sql_node.snapshot_id_type = types.none
    return sql_node


def sql_distributed_run(sql_node: SqlReader, array_dists, typemap,
    calltypes, typingctx, targetctx, is_independent=False,
    meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        ddu__tebb = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        iqcnq__wbi = []
        dict_encoded_cols = []
        for mhad__mnmf in sql_node.out_used_cols:
            bbvu__maklh = sql_node.df_colnames[mhad__mnmf]
            iqcnq__wbi.append(bbvu__maklh)
            if isinstance(sql_node.out_types[mhad__mnmf], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(bbvu__maklh)
        if sql_node.index_column_name:
            iqcnq__wbi.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(sql_node.index_column_name)
        apea__kvabr = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', ddu__tebb,
            apea__kvabr, iqcnq__wbi)
        if dict_encoded_cols:
            yhgh__rkt = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', yhgh__rkt,
                apea__kvabr, dict_encoded_cols)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        qyhri__mps = set(sql_node.unsupported_columns)
        qzufj__ygflz = set(sql_node.out_used_cols)
        ooxb__pdc = qzufj__ygflz & qyhri__mps
        if ooxb__pdc:
            izksh__ppglm = sorted(ooxb__pdc)
            jiq__sjtv = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            hncs__aykn = 0
            for zgcvk__mwg in izksh__ppglm:
                while sql_node.unsupported_columns[hncs__aykn] != zgcvk__mwg:
                    hncs__aykn += 1
                jiq__sjtv.append(
                    f"Column '{sql_node.original_df_colnames[zgcvk__mwg]}' with unsupported arrow type {sql_node.unsupported_arrow_types[hncs__aykn]}"
                    )
                hncs__aykn += 1
            npx__dfnw = '\n'.join(jiq__sjtv)
            raise BodoError(npx__dfnw, loc=sql_node.loc)
    if sql_node.limit is None and (not meta_head_only_info or 
        meta_head_only_info[0] is None):
        limit = None
    elif sql_node.limit is None:
        limit = meta_head_only_info[0]
    elif not meta_head_only_info or meta_head_only_info[0] is None:
        limit = sql_node.limit
    else:
        limit = min(limit, meta_head_only_info[0])
    wvxd__dqg, riru__ptog = bodo.ir.connector.generate_filter_map(sql_node.
        filters)
    zcbo__kpp = ', '.join(wvxd__dqg.values())
    fxam__rlql = (
        f'def sql_impl(sql_request, conn, database_schema, {zcbo__kpp}):\n')
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        if sql_node.filters:
            fbnlm__ulp = []
            for hjxx__yydou in sql_node.filters:
                prmcu__qew = []
                for pbntr__xpba in hjxx__yydou:
                    mtt__noiau, uwwa__cyo = pbntr__xpba[0], pbntr__xpba[2]
                    mtt__noiau = convert_col_name(mtt__noiau, sql_node.
                        converted_colnames)
                    mtt__noiau = '\\"' + mtt__noiau + '\\"'
                    xul__usz = '{' + wvxd__dqg[pbntr__xpba[2].name
                        ] + '}' if isinstance(pbntr__xpba[2], ir.Var
                        ) else uwwa__cyo
                    if pbntr__xpba[1] in ('startswith', 'endswith'):
                        pjkn__gmuh = ['(', pbntr__xpba[1], '(', mtt__noiau,
                            ',', xul__usz, ')', ')']
                    else:
                        pjkn__gmuh = ['(', mtt__noiau, pbntr__xpba[1],
                            xul__usz, ')']
                    prmcu__qew.append(' '.join(pjkn__gmuh))
                fbnlm__ulp.append(' ( ' + ' AND '.join(prmcu__qew) + ' ) ')
            aow__arr = ' WHERE ' + ' OR '.join(fbnlm__ulp)
            for mhad__mnmf, mxwt__zdmrp in enumerate(wvxd__dqg.values()):
                fxam__rlql += (
                    f'    {mxwt__zdmrp} = get_sql_literal({mxwt__zdmrp})\n')
            fxam__rlql += f'    sql_request = f"{{sql_request}} {aow__arr}"\n'
        if sql_node.limit != limit:
            fxam__rlql += (
                f'    sql_request = f"{{sql_request}} LIMIT {limit}"\n')
    kfo__edjxc = ''
    if sql_node.db_type == 'iceberg':
        kfo__edjxc = zcbo__kpp
    fxam__rlql += f"""    (total_rows, table_var, index_var, file_list, snapshot_id) = _sql_reader_py(sql_request, conn, database_schema, {kfo__edjxc})
"""
    wgw__oyni = {}
    exec(fxam__rlql, {}, wgw__oyni)
    bvcia__fjc = wgw__oyni['sql_impl']
    vuj__msr = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        sql_node.index_column_name, sql_node.index_column_type, sql_node.
        out_used_cols, sql_node.converted_colnames, typingctx, targetctx,
        sql_node.db_type, limit, parallel, typemap, sql_node.filters,
        sql_node.pyarrow_schema, not sql_node.is_live_table, sql_node.
        is_select_query, sql_node.is_merge_into, is_independent)
    fzqig__pcuk = (types.none if sql_node.database_schema is None else
        string_type)
    wskts__forf = compile_to_numba_ir(bvcia__fjc, {'_sql_reader_py':
        vuj__msr, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type,
        fzqig__pcuk) + tuple(typemap[rxacn__hrhh.name] for rxacn__hrhh in
        riru__ptog), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        jxdbq__tfx = [sql_node.df_colnames[mhad__mnmf] for mhad__mnmf in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            jxdbq__tfx.append(sql_node.index_column_name)
        if len(jxdbq__tfx) == 0:
            ytrc__rhiu = 'COUNT(*)'
        else:
            ytrc__rhiu = escape_column_names(jxdbq__tfx, sql_node.db_type,
                sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            uadr__vrd = ('SELECT ' + ytrc__rhiu + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            uadr__vrd = ('SELECT ' + ytrc__rhiu + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        uadr__vrd = sql_node.sql_request
    replace_arg_nodes(wskts__forf, [ir.Const(uadr__vrd, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + riru__ptog)
    unsdi__njd = wskts__forf.body[:-3]
    if meta_head_only_info:
        unsdi__njd[-5].target = meta_head_only_info[1]
    unsdi__njd[-4].target = sql_node.out_vars[0]
    unsdi__njd[-3].target = sql_node.out_vars[1]
    assert sql_node.has_side_effects or not (sql_node.index_column_name is
        None and not sql_node.is_live_table
        ), 'At most one of table and index should be dead if the SQL IR node is live and has no side effects'
    if sql_node.index_column_name is None:
        unsdi__njd.pop(-3)
    elif not sql_node.is_live_table:
        unsdi__njd.pop(-4)
    if sql_node.file_list_live:
        unsdi__njd[-2].target = sql_node.out_vars[2]
    else:
        unsdi__njd.pop(-2)
    if sql_node.snapshot_id_live:
        unsdi__njd[-1].target = sql_node.out_vars[3]
    else:
        unsdi__njd.pop(-1)
    return unsdi__njd


def convert_col_name(col_name: str, converted_colnames: List[str]) ->str:
    if col_name in converted_colnames:
        return col_name.upper()
    return col_name


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type == 'snowflake':
        from bodo.io.snowflake import escape_col_name
        ytrc__rhiu = ', '.join(escape_col_name(convert_col_name(zst__iwg,
            converted_colnames)) for zst__iwg in col_names)
    elif db_type == 'oracle':
        jxdbq__tfx = []
        for zst__iwg in col_names:
            jxdbq__tfx.append(convert_col_name(zst__iwg, converted_colnames))
        ytrc__rhiu = ', '.join([f'"{zst__iwg}"' for zst__iwg in jxdbq__tfx])
    elif db_type == 'mysql':
        ytrc__rhiu = ', '.join([f'`{zst__iwg}`' for zst__iwg in col_names])
    else:
        ytrc__rhiu = ', '.join([f'"{zst__iwg}"' for zst__iwg in col_names])
    return ytrc__rhiu


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    ywusq__uxqj = types.unliteral(filter_value)
    if ywusq__uxqj == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(ywusq__uxqj, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif isinstance(ywusq__uxqj, bodo.PandasTimestampType):
        if ywusq__uxqj.tz is None:
            kjdj__leqyw = 'TIMESTAMP_NTZ'
        else:
            kjdj__leqyw = 'TIMESTAMP_TZ'

        def impl(filter_value):
            ojgfw__cktl = filter_value.nanosecond
            enljj__mpq = ''
            if ojgfw__cktl < 10:
                enljj__mpq = '00'
            elif ojgfw__cktl < 100:
                enljj__mpq = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{enljj__mpq}{ojgfw__cktl}'::{kjdj__leqyw}"
                )
        return impl
    elif ywusq__uxqj == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {ywusq__uxqj} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float, bodo.PandasTimestampType
    ffaw__cxnzh = bodo.datetime_date_type, types.unicode_type, types.bool_
    ywusq__uxqj = types.unliteral(filter_value)
    if (isinstance(ywusq__uxqj, (types.List, types.Array, bodo.
        IntegerArrayType, bodo.FloatingArrayType, bodo.DatetimeArrayType)) or
        ywusq__uxqj in (bodo.string_array_type, bodo.dict_str_arr_type,
        bodo.boolean_array, bodo.datetime_date_array_type)) and (isinstance
        (ywusq__uxqj.dtype, scalar_isinstance) or ywusq__uxqj.dtype in
        ffaw__cxnzh):

        def impl(filter_value):
            spvuo__pndb = ', '.join([_get_snowflake_sql_literal_scalar(
                zst__iwg) for zst__iwg in filter_value])
            return f'({spvuo__pndb})'
        return impl
    elif isinstance(ywusq__uxqj, scalar_isinstance
        ) or ywusq__uxqj in ffaw__cxnzh:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {ywusq__uxqj} used in filter pushdown.'
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
    except ImportError as hkuy__brv:
        ogoqg__vfpxg = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(ogoqg__vfpxg)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as hkuy__brv:
        ogoqg__vfpxg = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(ogoqg__vfpxg)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as hkuy__brv:
        ogoqg__vfpxg = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(ogoqg__vfpxg)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as hkuy__brv:
        ogoqg__vfpxg = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(ogoqg__vfpxg)


def req_limit(sql_request):
    import re
    jgb__ggxx = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    nqiw__yjy = jgb__ggxx.search(sql_request)
    if nqiw__yjy:
        return int(nqiw__yjy.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs: List[Any],
    index_column_name: Optional[str], index_column_type, out_used_cols:
    List[int], converted_colnames: List[str], typingctx, targetctx, db_type:
    str, limit: Optional[int], parallel: bool, typemap, filters: Optional[
    Any], pyarrow_schema: Optional[pa.Schema], is_dead_table: bool,
    is_select_query: bool, is_merge_into: bool, is_independent: bool):
    hfotd__ituow = next_label()
    jxdbq__tfx = [col_names[mhad__mnmf] for mhad__mnmf in out_used_cols]
    dtnc__rtr = [col_typs[mhad__mnmf] for mhad__mnmf in out_used_cols]
    if index_column_name:
        jxdbq__tfx.append(index_column_name)
        dtnc__rtr.append(index_column_type)
    zwdxy__zya = None
    xkym__bkam = None
    hqf__eevh = types.none if is_dead_table else TableType(tuple(col_typs))
    kfo__edjxc = ''
    wvxd__dqg = {}
    riru__ptog = []
    if filters and db_type == 'iceberg':
        wvxd__dqg, riru__ptog = bodo.ir.connector.generate_filter_map(filters)
        kfo__edjxc = ', '.join(wvxd__dqg.values())
    fxam__rlql = (
        f'def sql_reader_py(sql_request, conn, database_schema, {kfo__edjxc}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from an Iceberg database'
        ckyr__ncq, yjjt__gcbi = bodo.ir.connector.generate_arrow_filters(
            filters, wvxd__dqg, riru__ptog, col_names, col_names, col_typs,
            typemap, 'iceberg')
        vxcdi__qflni = -1
        if is_merge_into and col_names.index('_bodo_row_id') in out_used_cols:
            vxcdi__qflni = col_names.index('_bodo_row_id')
        selected_cols: List[int] = [pyarrow_schema.get_field_index(
            col_names[mhad__mnmf]) for mhad__mnmf in out_used_cols if 
            mhad__mnmf != vxcdi__qflni]
        ora__nsisu = {giid__czs: mhad__mnmf for mhad__mnmf, giid__czs in
            enumerate(selected_cols)}
        nullable_cols = [int(is_nullable(col_typs[mhad__mnmf])) for
            mhad__mnmf in selected_cols]
        xzlu__tcij = [mhad__mnmf for mhad__mnmf in selected_cols if 
            col_typs[mhad__mnmf] == bodo.dict_str_arr_type]
        mxthi__xklc = (
            f'dict_str_cols_arr_{hfotd__ituow}.ctypes, np.int32({len(xzlu__tcij)})'
             if xzlu__tcij else '0, 0')
        aksdp__dahi = ',' if kfo__edjxc else ''
        fxam__rlql += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{ckyr__ncq}", "{yjjt__gcbi}", ({kfo__edjxc}{aksdp__dahi}))
  out_table, total_rows, file_list, snapshot_id = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{hfotd__ituow}.ctypes,
    {len(selected_cols)},
    nullable_cols_arr_{hfotd__ituow}.ctypes,
    pyarrow_schema_{hfotd__ituow},
    {mxthi__xklc},
    {is_merge_into},
  )
"""
        if parallel:
            fxam__rlql += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            fxam__rlql += f'  local_rows = total_rows\n'
        zwdxy__zya = None
        if not is_dead_table:
            zwdxy__zya = []
            hmhyy__fuxgx = 0
            for mhad__mnmf in range(len(col_names)):
                if hmhyy__fuxgx < len(out_used_cols
                    ) and mhad__mnmf == out_used_cols[hmhyy__fuxgx]:
                    if mhad__mnmf == vxcdi__qflni:
                        zwdxy__zya.append(len(selected_cols))
                    else:
                        zwdxy__zya.append(ora__nsisu[mhad__mnmf])
                    hmhyy__fuxgx += 1
                else:
                    zwdxy__zya.append(-1)
            zwdxy__zya = np.array(zwdxy__zya, dtype=np.int64)
        if is_dead_table:
            fxam__rlql += '  table_var = None\n'
        else:
            fxam__rlql += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{hfotd__ituow}, py_table_type_{hfotd__ituow})
"""
            if len(out_used_cols) == 0:
                fxam__rlql += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        bqp__viw = 'None'
        if index_column_name is not None:
            lxcy__rwedg = len(out_used_cols) + 1 if not is_dead_table else 0
            bqp__viw = (
                f'info_to_array(info_from_table(out_table, {lxcy__rwedg}), index_col_typ)'
                )
        fxam__rlql += f'  index_var = {bqp__viw}\n'
        fxam__rlql += f'  delete_table(out_table)\n'
        fxam__rlql += f'  ev.finalize()\n'
        fxam__rlql += (
            '  return (total_rows, table_var, index_var, file_list, snapshot_id)\n'
            )
    elif db_type == 'snowflake':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from Snowflake'
        if is_select_query:
            sagvc__hftl = []
            for col_name in jxdbq__tfx:
                sbe__sjsyq = convert_col_name(col_name, converted_colnames)
                hncs__aykn = pyarrow_schema.get_field_index(sbe__sjsyq)
                if hncs__aykn < 0:
                    raise BodoError(
                        f'SQLReader Snowflake: Column {sbe__sjsyq} is not in source schema'
                        )
                sagvc__hftl.append(pyarrow_schema.field(hncs__aykn))
            pyarrow_schema = pa.schema(sagvc__hftl)
        zuf__rjs = {giid__czs: mhad__mnmf for mhad__mnmf, giid__czs in
            enumerate(out_used_cols)}
        ivo__fhpn = [zuf__rjs[mhad__mnmf] for mhad__mnmf in out_used_cols if
            col_typs[mhad__mnmf] == dict_str_arr_type]
        nullable_cols = [int(is_nullable(col_typs[mhad__mnmf])) for
            mhad__mnmf in out_used_cols]
        if index_column_name:
            nullable_cols.append(int(is_nullable(index_column_type)))
        jyq__wkwhu = np.array(ivo__fhpn, dtype=np.int32)
        uutyh__vjh = np.array(nullable_cols, dtype=np.int32)
        fxam__rlql += f"""  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = snowflake_read(
    unicode_to_utf8(sql_request),
    unicode_to_utf8(conn),
    {parallel},
    {is_independent},
    pyarrow_schema_{hfotd__ituow},
    {len(uutyh__vjh)},
    nullable_cols_array.ctypes,
    snowflake_dict_cols_array.ctypes,
    {len(jyq__wkwhu)},
    total_rows_np.ctypes,
    {is_select_query and len(jxdbq__tfx) == 0},
    {is_select_query},
  )
  check_and_propagate_cpp_exception()
"""
        fxam__rlql += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            fxam__rlql += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            fxam__rlql += f'  local_rows = total_rows\n'
        if index_column_name:
            fxam__rlql += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            fxam__rlql += '  index_var = None\n'
        if not is_dead_table:
            hncs__aykn = []
            hmhyy__fuxgx = 0
            for mhad__mnmf in range(len(col_names)):
                if hmhyy__fuxgx < len(out_used_cols
                    ) and mhad__mnmf == out_used_cols[hmhyy__fuxgx]:
                    hncs__aykn.append(hmhyy__fuxgx)
                    hmhyy__fuxgx += 1
                else:
                    hncs__aykn.append(-1)
            zwdxy__zya = np.array(hncs__aykn, dtype=np.int64)
            fxam__rlql += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{hfotd__ituow}, py_table_type_{hfotd__ituow})
"""
            if len(out_used_cols) == 0:
                if index_column_name:
                    fxam__rlql += (
                        f'  table_var = set_table_len(table_var, len(index_var))\n'
                        )
                else:
                    fxam__rlql += (
                        f'  table_var = set_table_len(table_var, local_rows)\n'
                        )
        else:
            fxam__rlql += '  table_var = None\n'
        fxam__rlql += '  delete_table(out_table)\n'
        fxam__rlql += '  ev.finalize()\n'
        fxam__rlql += (
            '  return (total_rows, table_var, index_var, None, None)\n')
    else:
        if not is_dead_table:
            fxam__rlql += f"""  type_usecols_offsets_arr_{hfotd__ituow}_2 = type_usecols_offsets_arr_{hfotd__ituow}
"""
            xkym__bkam = np.array(out_used_cols, dtype=np.int64)
        fxam__rlql += '  df_typeref_2 = df_typeref\n'
        fxam__rlql += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            fxam__rlql += '  pymysql_check()\n'
        elif db_type == 'oracle':
            fxam__rlql += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            fxam__rlql += '  psycopg2_check()\n'
        if parallel:
            fxam__rlql += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                fxam__rlql += f'  nb_row = {limit}\n'
            else:
                fxam__rlql += '  with objmode(nb_row="int64"):\n'
                fxam__rlql += f'     if rank == {MPI_ROOT}:\n'
                fxam__rlql += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                fxam__rlql += '         frame = pd.read_sql(sql_cons, conn)\n'
                fxam__rlql += '         nb_row = frame.iat[0,0]\n'
                fxam__rlql += '     else:\n'
                fxam__rlql += '         nb_row = 0\n'
                fxam__rlql += '  nb_row = bcast_scalar(nb_row)\n'
            fxam__rlql += f"""  with objmode(table_var=py_table_type_{hfotd__ituow}, index_var=index_col_typ):
"""
            fxam__rlql += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                fxam__rlql += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                fxam__rlql += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            fxam__rlql += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            fxam__rlql += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            fxam__rlql += f"""  with objmode(table_var=py_table_type_{hfotd__ituow}, index_var=index_col_typ):
"""
            fxam__rlql += '    df_ret = pd.read_sql(sql_request, conn)\n'
            fxam__rlql += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            fxam__rlql += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            fxam__rlql += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            fxam__rlql += '    index_var = None\n'
        if not is_dead_table:
            fxam__rlql += f'    arrs = []\n'
            fxam__rlql += f'    for i in range(df_ret.shape[1]):\n'
            fxam__rlql += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            fxam__rlql += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{hfotd__ituow}_2, {len(col_names)})
"""
        else:
            fxam__rlql += '    table_var = None\n'
        fxam__rlql += '  return (-1, table_var, index_var, None, None)\n'
    dqze__apftc = globals()
    dqze__apftc.update({'bodo': bodo, f'py_table_type_{hfotd__ituow}':
        hqf__eevh, 'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        dqze__apftc.update({f'table_idx_{hfotd__ituow}': zwdxy__zya,
            f'pyarrow_schema_{hfotd__ituow}': pyarrow_schema,
            'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'get_node_portion': bodo.libs.distributed_api.
            get_node_portion})
    if db_type == 'iceberg':
        dqze__apftc.update({f'selected_cols_arr_{hfotd__ituow}': np.array(
            selected_cols, np.int32), f'nullable_cols_arr_{hfotd__ituow}':
            np.array(nullable_cols, np.int32),
            f'dict_str_cols_arr_{hfotd__ituow}': np.array(xzlu__tcij, np.
            int32), f'py_table_type_{hfotd__ituow}': hqf__eevh,
            'get_filters_pyobject': bodo.io.parquet_pio.
            get_filters_pyobject, 'iceberg_read': _iceberg_pq_read})
    elif db_type == 'snowflake':
        dqze__apftc.update({'np': np, 'snowflake_read': _snowflake_read,
            'nullable_cols_array': uutyh__vjh, 'snowflake_dict_cols_array':
            jyq__wkwhu})
    else:
        dqze__apftc.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(dtnc__rtr), bodo.RangeIndexType(None),
            tuple(jxdbq__tfx)), 'Table': Table,
            f'type_usecols_offsets_arr_{hfotd__ituow}': xkym__bkam})
    wgw__oyni = {}
    exec(fxam__rlql, dqze__apftc, wgw__oyni)
    vuj__msr = wgw__oyni['sql_reader_py']
    ojlt__gzanq = numba.njit(vuj__msr)
    compiled_funcs.append(ojlt__gzanq)
    return ojlt__gzanq


parquet_predicate_type = ParquetPredicateType()
pyarrow_schema_type = PyArrowTableSchemaType()


@intrinsic
def _iceberg_pq_read(typingctx, conn_str, db_schema, sql_request_str,
    parallel, limit, dnf_filters, expr_filters, selected_cols,
    num_selected_cols, nullable_cols, pyarrow_schema, dict_encoded_cols,
    num_dict_encoded_cols, is_merge_into_cow):

    def codegen(context, builder, signature, args):
        ahvm__szgjp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(1), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(64).as_pointer()])
        uqif__qwur = cgutils.get_or_insert_function(builder.module,
            ahvm__szgjp, name='iceberg_pq_read')
        nayg__fad = cgutils.alloca_once(builder, lir.IntType(64))
        ccb__sni = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        kzlr__zxpx = cgutils.alloca_once(builder, lir.IntType(64))
        gnqjl__ijtzr = args + (nayg__fad, ccb__sni, kzlr__zxpx)
        mrd__trn = builder.call(uqif__qwur, gnqjl__ijtzr)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        and__uhdwd = builder.load(ccb__sni)
        jvx__lvxc = cgutils.create_struct_proxy(types.pyobject_of_list_type)(
            context, builder)
        pby__zcgkz = context.get_python_api(builder)
        jvx__lvxc.meminfo = pby__zcgkz.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), and__uhdwd)
        jvx__lvxc.pyobj = and__uhdwd
        pby__zcgkz.decref(and__uhdwd)
        keb__sguza = [mrd__trn, builder.load(nayg__fad), jvx__lvxc.
            _getvalue(), builder.load(kzlr__zxpx)]
        return context.make_tuple(builder, hwo__roy, keb__sguza)
    hwo__roy = types.Tuple([table_type, types.int64, types.
        pyobject_of_list_type, types.int64])
    lci__oqudu = hwo__roy(types.voidptr, types.voidptr, types.voidptr,
        types.boolean, types.int64, parquet_predicate_type,
        parquet_predicate_type, types.voidptr, types.int32, types.voidptr,
        pyarrow_schema_type, types.voidptr, types.int32, types.boolean)
    return lci__oqudu, codegen


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.boolean,
    pyarrow_schema_type, types.int64, types.voidptr, types.voidptr, types.
    int32, types.voidptr, types.boolean, types.boolean))
