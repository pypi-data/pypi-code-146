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
        ydlzm__tsaq = tuple(buec__utz.name for buec__utz in self.out_vars)
        return (
            f'{ydlzm__tsaq} = SQLReader(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_schema={self.pyarrow_schema}, is_merge_into={self.is_merge_into})'
            )


def parse_dbtype(con_str):
    mhf__jogdm = urlparse(con_str)
    db_type = mhf__jogdm.scheme
    xwt__qixv = mhf__jogdm.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', xwt__qixv
    if db_type == 'mysql+pymysql':
        return 'mysql', xwt__qixv
    if con_str.startswith('iceberg+glue') or mhf__jogdm.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', xwt__qixv
    return db_type, xwt__qixv


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
    dxcdh__eyytn = sql_node.out_vars[0].name
    jsgw__omi = sql_node.out_vars[1].name
    omuuv__dvq = sql_node.out_vars[2].name if len(sql_node.out_vars
        ) > 2 else None
    rgmpw__laygs = sql_node.out_vars[3].name if len(sql_node.out_vars
        ) > 3 else None
    if (not sql_node.has_side_effects and dxcdh__eyytn not in lives and 
        jsgw__omi not in lives and omuuv__dvq not in lives and rgmpw__laygs
         not in lives):
        return None
    if dxcdh__eyytn not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
        sql_node.is_live_table = False
    if jsgw__omi not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    if omuuv__dvq not in lives:
        sql_node.file_list_live = False
        sql_node.file_list_type = types.none
    if rgmpw__laygs not in lives:
        sql_node.snapshot_id_live = False
        sql_node.snapshot_id_type = types.none
    return sql_node


def sql_distributed_run(sql_node: SqlReader, array_dists, typemap,
    calltypes, typingctx, targetctx, is_independent=False,
    meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        ewyvf__niamu = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        hqil__mdqqg = []
        dict_encoded_cols = []
        for vnn__fdfe in sql_node.out_used_cols:
            yta__kec = sql_node.df_colnames[vnn__fdfe]
            hqil__mdqqg.append(yta__kec)
            if isinstance(sql_node.out_types[vnn__fdfe], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(yta__kec)
        if sql_node.index_column_name:
            hqil__mdqqg.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(sql_node.index_column_name)
        ymqj__qvqbs = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', ewyvf__niamu,
            ymqj__qvqbs, hqil__mdqqg)
        if dict_encoded_cols:
            fkjfb__pczmi = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                fkjfb__pczmi, ymqj__qvqbs, dict_encoded_cols)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        zac__zmuyt = set(sql_node.unsupported_columns)
        maj__zxzz = set(sql_node.out_used_cols)
        zamt__zvj = maj__zxzz & zac__zmuyt
        if zamt__zvj:
            esrsc__quyr = sorted(zamt__zvj)
            ioy__rksv = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            als__pzi = 0
            for viavu__fee in esrsc__quyr:
                while sql_node.unsupported_columns[als__pzi] != viavu__fee:
                    als__pzi += 1
                ioy__rksv.append(
                    f"Column '{sql_node.original_df_colnames[viavu__fee]}' with unsupported arrow type {sql_node.unsupported_arrow_types[als__pzi]}"
                    )
                als__pzi += 1
            papf__csw = '\n'.join(ioy__rksv)
            raise BodoError(papf__csw, loc=sql_node.loc)
    if sql_node.limit is None and (not meta_head_only_info or 
        meta_head_only_info[0] is None):
        limit = None
    elif sql_node.limit is None:
        limit = meta_head_only_info[0]
    elif not meta_head_only_info or meta_head_only_info[0] is None:
        limit = sql_node.limit
    else:
        limit = min(limit, meta_head_only_info[0])
    debr__hbj, agg__rndli = bodo.ir.connector.generate_filter_map(sql_node.
        filters)
    cnt__pikh = ', '.join(debr__hbj.values())
    dto__isp = (
        f'def sql_impl(sql_request, conn, database_schema, {cnt__pikh}):\n')
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        if sql_node.filters:
            wzbu__acnd = []
            for bow__zrfz in sql_node.filters:
                pmk__udbl = []
                for use__scl in bow__zrfz:
                    nkdk__axr, fjv__grctf = use__scl[0], use__scl[2]
                    nkdk__axr = convert_col_name(nkdk__axr, sql_node.
                        converted_colnames)
                    nkdk__axr = '\\"' + nkdk__axr + '\\"'
                    pkxs__kzq = '{' + debr__hbj[use__scl[2].name
                        ] + '}' if isinstance(use__scl[2], ir.Var
                        ) else fjv__grctf
                    if use__scl[1] in ('startswith', 'endswith'):
                        nkvqr__naca = ['(', use__scl[1], '(', nkdk__axr,
                            ',', pkxs__kzq, ')', ')']
                    else:
                        nkvqr__naca = ['(', nkdk__axr, use__scl[1],
                            pkxs__kzq, ')']
                    pmk__udbl.append(' '.join(nkvqr__naca))
                wzbu__acnd.append(' ( ' + ' AND '.join(pmk__udbl) + ' ) ')
            ppum__swoa = ' WHERE ' + ' OR '.join(wzbu__acnd)
            for vnn__fdfe, dtarg__qyqh in enumerate(debr__hbj.values()):
                dto__isp += (
                    f'    {dtarg__qyqh} = get_sql_literal({dtarg__qyqh})\n')
            dto__isp += f'    sql_request = f"{{sql_request}} {ppum__swoa}"\n'
        if sql_node.limit != limit:
            dto__isp += f'    sql_request = f"{{sql_request}} LIMIT {limit}"\n'
    sanj__ylvr = ''
    if sql_node.db_type == 'iceberg':
        sanj__ylvr = cnt__pikh
    dto__isp += f"""    (total_rows, table_var, index_var, file_list, snapshot_id) = _sql_reader_py(sql_request, conn, database_schema, {sanj__ylvr})
"""
    bsh__kfqk = {}
    exec(dto__isp, {}, bsh__kfqk)
    jufg__mchrh = bsh__kfqk['sql_impl']
    fjunb__xfu = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.out_used_cols, sql_node.converted_colnames, typingctx,
        targetctx, sql_node.db_type, limit, parallel, typemap, sql_node.
        filters, sql_node.pyarrow_schema, not sql_node.is_live_table,
        sql_node.is_select_query, sql_node.is_merge_into, is_independent)
    yua__ylyh = types.none if sql_node.database_schema is None else string_type
    dara__vpli = compile_to_numba_ir(jufg__mchrh, {'_sql_reader_py':
        fjunb__xfu, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type, yua__ylyh) +
        tuple(typemap[buec__utz.name] for buec__utz in agg__rndli), typemap
        =typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        yriu__mwmng = [sql_node.df_colnames[vnn__fdfe] for vnn__fdfe in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            yriu__mwmng.append(sql_node.index_column_name)
        if len(yriu__mwmng) == 0:
            ofmp__vto = 'COUNT(*)'
        else:
            ofmp__vto = escape_column_names(yriu__mwmng, sql_node.db_type,
                sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            nvfb__uxh = ('SELECT ' + ofmp__vto + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            nvfb__uxh = ('SELECT ' + ofmp__vto + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        nvfb__uxh = sql_node.sql_request
    replace_arg_nodes(dara__vpli, [ir.Const(nvfb__uxh, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + agg__rndli)
    dajol__ahgfz = dara__vpli.body[:-3]
    if meta_head_only_info:
        dajol__ahgfz[-5].target = meta_head_only_info[1]
    dajol__ahgfz[-4].target = sql_node.out_vars[0]
    dajol__ahgfz[-3].target = sql_node.out_vars[1]
    assert sql_node.has_side_effects or not (sql_node.index_column_name is
        None and not sql_node.is_live_table
        ), 'At most one of table and index should be dead if the SQL IR node is live and has no side effects'
    if sql_node.index_column_name is None:
        dajol__ahgfz.pop(-3)
    elif not sql_node.is_live_table:
        dajol__ahgfz.pop(-4)
    if sql_node.file_list_live:
        dajol__ahgfz[-2].target = sql_node.out_vars[2]
    else:
        dajol__ahgfz.pop(-2)
    if sql_node.snapshot_id_live:
        dajol__ahgfz[-1].target = sql_node.out_vars[3]
    else:
        dajol__ahgfz.pop(-1)
    return dajol__ahgfz


def convert_col_name(col_name: str, converted_colnames: List[str]) ->str:
    if col_name in converted_colnames:
        return col_name.upper()
    return col_name


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type == 'snowflake':
        from bodo.io.snowflake import escape_col_name
        ofmp__vto = ', '.join(escape_col_name(convert_col_name(mba__itb,
            converted_colnames)) for mba__itb in col_names)
    elif db_type == 'oracle':
        yriu__mwmng = []
        for mba__itb in col_names:
            yriu__mwmng.append(convert_col_name(mba__itb, converted_colnames))
        ofmp__vto = ', '.join([f'"{mba__itb}"' for mba__itb in yriu__mwmng])
    elif db_type == 'mysql':
        ofmp__vto = ', '.join([f'`{mba__itb}`' for mba__itb in col_names])
    else:
        ofmp__vto = ', '.join([f'"{mba__itb}"' for mba__itb in col_names])
    return ofmp__vto


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    nmm__rjxs = types.unliteral(filter_value)
    if nmm__rjxs == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(nmm__rjxs, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif isinstance(nmm__rjxs, bodo.PandasTimestampType):
        if nmm__rjxs.tz is None:
            ybem__xmdlc = 'TIMESTAMP_NTZ'
        else:
            ybem__xmdlc = 'TIMESTAMP_TZ'

        def impl(filter_value):
            bvc__xwxhi = filter_value.nanosecond
            bui__sgyx = ''
            if bvc__xwxhi < 10:
                bui__sgyx = '00'
            elif bvc__xwxhi < 100:
                bui__sgyx = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{bui__sgyx}{bvc__xwxhi}'::{ybem__xmdlc}"
                )
        return impl
    elif nmm__rjxs == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {nmm__rjxs} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float, bodo.PandasTimestampType
    tks__mcn = bodo.datetime_date_type, types.unicode_type, types.bool_
    nmm__rjxs = types.unliteral(filter_value)
    if (isinstance(nmm__rjxs, (types.List, types.Array, bodo.
        IntegerArrayType, bodo.FloatingArrayType, bodo.DatetimeArrayType)) or
        nmm__rjxs in (bodo.string_array_type, bodo.dict_str_arr_type, bodo.
        boolean_array, bodo.datetime_date_array_type)) and (isinstance(
        nmm__rjxs.dtype, scalar_isinstance) or nmm__rjxs.dtype in tks__mcn):

        def impl(filter_value):
            akik__ezu = ', '.join([_get_snowflake_sql_literal_scalar(
                mba__itb) for mba__itb in filter_value])
            return f'({akik__ezu})'
        return impl
    elif isinstance(nmm__rjxs, scalar_isinstance) or nmm__rjxs in tks__mcn:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {nmm__rjxs} used in filter pushdown.'
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
    except ImportError as dkrhe__udhr:
        oqwg__ivzp = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(oqwg__ivzp)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as dkrhe__udhr:
        oqwg__ivzp = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(oqwg__ivzp)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as dkrhe__udhr:
        oqwg__ivzp = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(oqwg__ivzp)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as dkrhe__udhr:
        oqwg__ivzp = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(oqwg__ivzp)


def req_limit(sql_request):
    import re
    ndtgo__xdf = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    iqd__stk = ndtgo__xdf.search(sql_request)
    if iqd__stk:
        return int(iqd__stk.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs: List[Any],
    index_column_name: Optional[str], index_column_type, out_used_cols:
    List[int], converted_colnames: List[str], typingctx, targetctx, db_type:
    str, limit: Optional[int], parallel: bool, typemap, filters: Optional[
    Any], pyarrow_schema: Optional[pa.Schema], is_dead_table: bool,
    is_select_query: bool, is_merge_into: bool, is_independent: bool):
    pydmf__zvbwx = next_label()
    yriu__mwmng = [col_names[vnn__fdfe] for vnn__fdfe in out_used_cols]
    rbcq__dznw = [col_typs[vnn__fdfe] for vnn__fdfe in out_used_cols]
    if index_column_name:
        yriu__mwmng.append(index_column_name)
        rbcq__dznw.append(index_column_type)
    wwcj__eqm = None
    bder__fdxzj = None
    qvvt__fvo = types.none if is_dead_table else TableType(tuple(col_typs))
    sanj__ylvr = ''
    debr__hbj = {}
    agg__rndli = []
    if filters and db_type == 'iceberg':
        debr__hbj, agg__rndli = bodo.ir.connector.generate_filter_map(filters)
        sanj__ylvr = ', '.join(debr__hbj.values())
    dto__isp = (
        f'def sql_reader_py(sql_request, conn, database_schema, {sanj__ylvr}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from an Iceberg database'
        dbcs__yawi, pze__mca = bodo.ir.connector.generate_arrow_filters(filters
            , debr__hbj, agg__rndli, col_names, col_names, col_typs,
            typemap, 'iceberg')
        omwmu__hidu = -1
        if is_merge_into and col_names.index('_bodo_row_id') in out_used_cols:
            omwmu__hidu = col_names.index('_bodo_row_id')
        selected_cols: List[int] = [pyarrow_schema.get_field_index(
            col_names[vnn__fdfe]) for vnn__fdfe in out_used_cols if 
            vnn__fdfe != omwmu__hidu]
        thtza__krg = {avao__qlmb: vnn__fdfe for vnn__fdfe, avao__qlmb in
            enumerate(selected_cols)}
        nullable_cols = [int(is_nullable(col_typs[vnn__fdfe])) for
            vnn__fdfe in selected_cols]
        fyuob__fga = [vnn__fdfe for vnn__fdfe in selected_cols if col_typs[
            vnn__fdfe] == bodo.dict_str_arr_type]
        yxw__frww = (
            f'dict_str_cols_arr_{pydmf__zvbwx}.ctypes, np.int32({len(fyuob__fga)})'
             if fyuob__fga else '0, 0')
        atz__ihpc = ',' if sanj__ylvr else ''
        dto__isp += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{dbcs__yawi}", "{pze__mca}", ({sanj__ylvr}{atz__ihpc}))
  out_table, total_rows, file_list, snapshot_id = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{pydmf__zvbwx}.ctypes,
    {len(selected_cols)},
    nullable_cols_arr_{pydmf__zvbwx}.ctypes,
    pyarrow_schema_{pydmf__zvbwx},
    {yxw__frww},
    {is_merge_into},
  )
"""
        if parallel:
            dto__isp += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            dto__isp += f'  local_rows = total_rows\n'
        wwcj__eqm = None
        if not is_dead_table:
            wwcj__eqm = []
            ame__aqwiu = 0
            for vnn__fdfe in range(len(col_names)):
                if ame__aqwiu < len(out_used_cols
                    ) and vnn__fdfe == out_used_cols[ame__aqwiu]:
                    if vnn__fdfe == omwmu__hidu:
                        wwcj__eqm.append(len(selected_cols))
                    else:
                        wwcj__eqm.append(thtza__krg[vnn__fdfe])
                    ame__aqwiu += 1
                else:
                    wwcj__eqm.append(-1)
            wwcj__eqm = np.array(wwcj__eqm, dtype=np.int64)
        if is_dead_table:
            dto__isp += '  table_var = None\n'
        else:
            dto__isp += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{pydmf__zvbwx}, py_table_type_{pydmf__zvbwx})
"""
            if len(out_used_cols) == 0:
                dto__isp += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        jsgw__omi = 'None'
        if index_column_name is not None:
            efiu__mxv = len(out_used_cols) + 1 if not is_dead_table else 0
            jsgw__omi = (
                f'info_to_array(info_from_table(out_table, {efiu__mxv}), index_col_typ)'
                )
        dto__isp += f'  index_var = {jsgw__omi}\n'
        dto__isp += f'  delete_table(out_table)\n'
        dto__isp += f'  ev.finalize()\n'
        dto__isp += (
            '  return (total_rows, table_var, index_var, file_list, snapshot_id)\n'
            )
    elif db_type == 'snowflake':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from Snowflake'
        if is_select_query:
            sbf__lffs = []
            for col_name in yriu__mwmng:
                smspu__sakx = convert_col_name(col_name, converted_colnames)
                als__pzi = pyarrow_schema.get_field_index(smspu__sakx)
                if als__pzi < 0:
                    raise BodoError(
                        f'SQLReader Snowflake: Column {smspu__sakx} is not in source schema'
                        )
                sbf__lffs.append(pyarrow_schema.field(als__pzi))
            pyarrow_schema = pa.schema(sbf__lffs)
        blqld__vhq = {avao__qlmb: vnn__fdfe for vnn__fdfe, avao__qlmb in
            enumerate(out_used_cols)}
        vlxmi__yeot = [blqld__vhq[vnn__fdfe] for vnn__fdfe in out_used_cols if
            col_typs[vnn__fdfe] == dict_str_arr_type]
        nullable_cols = [int(is_nullable(col_typs[vnn__fdfe])) for
            vnn__fdfe in out_used_cols]
        if index_column_name:
            nullable_cols.append(int(is_nullable(index_column_type)))
        oft__akpz = np.array(vlxmi__yeot, dtype=np.int32)
        bujsm__kmtj = np.array(nullable_cols, dtype=np.int32)
        dto__isp += f"""  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = snowflake_read(
    unicode_to_utf8(sql_request),
    unicode_to_utf8(conn),
    {parallel},
    {is_independent},
    pyarrow_schema_{pydmf__zvbwx},
    {len(bujsm__kmtj)},
    nullable_cols_array.ctypes,
    snowflake_dict_cols_array.ctypes,
    {len(oft__akpz)},
    total_rows_np.ctypes,
    {is_select_query and len(yriu__mwmng) == 0},
    {is_select_query},
  )
  check_and_propagate_cpp_exception()
"""
        dto__isp += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            dto__isp += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            dto__isp += f'  local_rows = total_rows\n'
        if index_column_name:
            dto__isp += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            dto__isp += '  index_var = None\n'
        if not is_dead_table:
            als__pzi = []
            ame__aqwiu = 0
            for vnn__fdfe in range(len(col_names)):
                if ame__aqwiu < len(out_used_cols
                    ) and vnn__fdfe == out_used_cols[ame__aqwiu]:
                    als__pzi.append(ame__aqwiu)
                    ame__aqwiu += 1
                else:
                    als__pzi.append(-1)
            wwcj__eqm = np.array(als__pzi, dtype=np.int64)
            dto__isp += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{pydmf__zvbwx}, py_table_type_{pydmf__zvbwx})
"""
            if len(out_used_cols) == 0:
                if index_column_name:
                    dto__isp += (
                        f'  table_var = set_table_len(table_var, len(index_var))\n'
                        )
                else:
                    dto__isp += (
                        f'  table_var = set_table_len(table_var, local_rows)\n'
                        )
        else:
            dto__isp += '  table_var = None\n'
        dto__isp += '  delete_table(out_table)\n'
        dto__isp += '  ev.finalize()\n'
        dto__isp += '  return (total_rows, table_var, index_var, None, None)\n'
    else:
        if not is_dead_table:
            dto__isp += f"""  type_usecols_offsets_arr_{pydmf__zvbwx}_2 = type_usecols_offsets_arr_{pydmf__zvbwx}
"""
            bder__fdxzj = np.array(out_used_cols, dtype=np.int64)
        dto__isp += '  df_typeref_2 = df_typeref\n'
        dto__isp += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            dto__isp += '  pymysql_check()\n'
        elif db_type == 'oracle':
            dto__isp += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            dto__isp += '  psycopg2_check()\n'
        if parallel:
            dto__isp += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                dto__isp += f'  nb_row = {limit}\n'
            else:
                dto__isp += '  with objmode(nb_row="int64"):\n'
                dto__isp += f'     if rank == {MPI_ROOT}:\n'
                dto__isp += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                dto__isp += '         frame = pd.read_sql(sql_cons, conn)\n'
                dto__isp += '         nb_row = frame.iat[0,0]\n'
                dto__isp += '     else:\n'
                dto__isp += '         nb_row = 0\n'
                dto__isp += '  nb_row = bcast_scalar(nb_row)\n'
            dto__isp += f"""  with objmode(table_var=py_table_type_{pydmf__zvbwx}, index_var=index_col_typ):
"""
            dto__isp += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                dto__isp += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                dto__isp += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            dto__isp += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            dto__isp += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            dto__isp += f"""  with objmode(table_var=py_table_type_{pydmf__zvbwx}, index_var=index_col_typ):
"""
            dto__isp += '    df_ret = pd.read_sql(sql_request, conn)\n'
            dto__isp += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            dto__isp += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            dto__isp += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            dto__isp += '    index_var = None\n'
        if not is_dead_table:
            dto__isp += f'    arrs = []\n'
            dto__isp += f'    for i in range(df_ret.shape[1]):\n'
            dto__isp += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            dto__isp += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{pydmf__zvbwx}_2, {len(col_names)})
"""
        else:
            dto__isp += '    table_var = None\n'
        dto__isp += '  return (-1, table_var, index_var, None, None)\n'
    aem__zftxo = globals()
    aem__zftxo.update({'bodo': bodo, f'py_table_type_{pydmf__zvbwx}':
        qvvt__fvo, 'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        aem__zftxo.update({f'table_idx_{pydmf__zvbwx}': wwcj__eqm,
            f'pyarrow_schema_{pydmf__zvbwx}': pyarrow_schema,
            'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'get_node_portion': bodo.libs.distributed_api.
            get_node_portion})
    if db_type == 'iceberg':
        aem__zftxo.update({f'selected_cols_arr_{pydmf__zvbwx}': np.array(
            selected_cols, np.int32), f'nullable_cols_arr_{pydmf__zvbwx}':
            np.array(nullable_cols, np.int32),
            f'dict_str_cols_arr_{pydmf__zvbwx}': np.array(fyuob__fga, np.
            int32), f'py_table_type_{pydmf__zvbwx}': qvvt__fvo,
            'get_filters_pyobject': bodo.io.parquet_pio.
            get_filters_pyobject, 'iceberg_read': _iceberg_pq_read})
    elif db_type == 'snowflake':
        aem__zftxo.update({'np': np, 'snowflake_read': _snowflake_read,
            'nullable_cols_array': bujsm__kmtj, 'snowflake_dict_cols_array':
            oft__akpz})
    else:
        aem__zftxo.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(rbcq__dznw), bodo.RangeIndexType(None),
            tuple(yriu__mwmng)), 'Table': Table,
            f'type_usecols_offsets_arr_{pydmf__zvbwx}': bder__fdxzj})
    bsh__kfqk = {}
    exec(dto__isp, aem__zftxo, bsh__kfqk)
    fjunb__xfu = bsh__kfqk['sql_reader_py']
    puc__gmgqd = numba.njit(fjunb__xfu)
    compiled_funcs.append(puc__gmgqd)
    return puc__gmgqd


parquet_predicate_type = ParquetPredicateType()
pyarrow_schema_type = PyArrowTableSchemaType()


@intrinsic
def _iceberg_pq_read(typingctx, conn_str, db_schema, sql_request_str,
    parallel, limit, dnf_filters, expr_filters, selected_cols,
    num_selected_cols, nullable_cols, pyarrow_schema, dict_encoded_cols,
    num_dict_encoded_cols, is_merge_into_cow):

    def codegen(context, builder, signature, args):
        zljn__ykqq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(1), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(64).as_pointer()])
        zdp__bexw = cgutils.get_or_insert_function(builder.module,
            zljn__ykqq, name='iceberg_pq_read')
        zzn__nuznd = cgutils.alloca_once(builder, lir.IntType(64))
        qpju__rba = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        puv__gzej = cgutils.alloca_once(builder, lir.IntType(64))
        rarq__dosg = args + (zzn__nuznd, qpju__rba, puv__gzej)
        ffo__sbjfr = builder.call(zdp__bexw, rarq__dosg)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        zul__qans = builder.load(qpju__rba)
        whr__smw = cgutils.create_struct_proxy(types.pyobject_of_list_type)(
            context, builder)
        wzt__ryypb = context.get_python_api(builder)
        whr__smw.meminfo = wzt__ryypb.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), zul__qans)
        whr__smw.pyobj = zul__qans
        wzt__ryypb.decref(zul__qans)
        zul__tzhss = [ffo__sbjfr, builder.load(zzn__nuznd), whr__smw.
            _getvalue(), builder.load(puv__gzej)]
        return context.make_tuple(builder, sfvdi__objv, zul__tzhss)
    sfvdi__objv = types.Tuple([table_type, types.int64, types.
        pyobject_of_list_type, types.int64])
    iqqyg__cxb = sfvdi__objv(types.voidptr, types.voidptr, types.voidptr,
        types.boolean, types.int64, parquet_predicate_type,
        parquet_predicate_type, types.voidptr, types.int32, types.voidptr,
        pyarrow_schema_type, types.voidptr, types.int32, types.boolean)
    return iqqyg__cxb, codegen


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.boolean,
    pyarrow_schema_type, types.int64, types.voidptr, types.voidptr, types.
    int32, types.voidptr, types.boolean, types.boolean))
