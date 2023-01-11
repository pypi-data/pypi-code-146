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
        ayyl__grb = tuple(cmj__aiabu.name for cmj__aiabu in self.out_vars)
        return (
            f'{ayyl__grb} = SQLReader(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_schema={self.pyarrow_schema}, is_merge_into={self.is_merge_into})'
            )


def parse_dbtype(con_str):
    lxd__rrq = urlparse(con_str)
    db_type = lxd__rrq.scheme
    vet__aczh = lxd__rrq.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', vet__aczh
    if db_type == 'mysql+pymysql':
        return 'mysql', vet__aczh
    if con_str.startswith('iceberg+glue') or lxd__rrq.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', vet__aczh
    return db_type, vet__aczh


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
    cogu__oggtp = sql_node.out_vars[0].name
    emdr__uhxx = sql_node.out_vars[1].name
    jpsv__nlzxe = sql_node.out_vars[2].name if len(sql_node.out_vars
        ) > 2 else None
    jin__ovhgu = sql_node.out_vars[3].name if len(sql_node.out_vars
        ) > 3 else None
    if (not sql_node.has_side_effects and cogu__oggtp not in lives and 
        emdr__uhxx not in lives and jpsv__nlzxe not in lives and jin__ovhgu
         not in lives):
        return None
    if cogu__oggtp not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
        sql_node.is_live_table = False
    if emdr__uhxx not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    if jpsv__nlzxe not in lives:
        sql_node.file_list_live = False
        sql_node.file_list_type = types.none
    if jin__ovhgu not in lives:
        sql_node.snapshot_id_live = False
        sql_node.snapshot_id_type = types.none
    return sql_node


def sql_distributed_run(sql_node: SqlReader, array_dists, typemap,
    calltypes, typingctx, targetctx, is_independent=False,
    meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        livnu__fkf = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        ujfwu__zhvkk = []
        dict_encoded_cols = []
        for bkaa__paa in sql_node.out_used_cols:
            ubts__aczqo = sql_node.df_colnames[bkaa__paa]
            ujfwu__zhvkk.append(ubts__aczqo)
            if isinstance(sql_node.out_types[bkaa__paa], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(ubts__aczqo)
        if sql_node.index_column_name:
            ujfwu__zhvkk.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(sql_node.index_column_name)
        mkw__nzw = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', livnu__fkf,
            mkw__nzw, ujfwu__zhvkk)
        if dict_encoded_cols:
            vqncj__nub = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', vqncj__nub,
                mkw__nzw, dict_encoded_cols)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        daau__tnu = set(sql_node.unsupported_columns)
        npi__ihzs = set(sql_node.out_used_cols)
        nepya__wblej = npi__ihzs & daau__tnu
        if nepya__wblej:
            nxghk__puvw = sorted(nepya__wblej)
            kxh__dvfnq = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            sixsu__qcsyh = 0
            for cir__thtgj in nxghk__puvw:
                while sql_node.unsupported_columns[sixsu__qcsyh] != cir__thtgj:
                    sixsu__qcsyh += 1
                kxh__dvfnq.append(
                    f"Column '{sql_node.original_df_colnames[cir__thtgj]}' with unsupported arrow type {sql_node.unsupported_arrow_types[sixsu__qcsyh]}"
                    )
                sixsu__qcsyh += 1
            hyeya__pttjc = '\n'.join(kxh__dvfnq)
            raise BodoError(hyeya__pttjc, loc=sql_node.loc)
    if sql_node.limit is None and (not meta_head_only_info or 
        meta_head_only_info[0] is None):
        limit = None
    elif sql_node.limit is None:
        limit = meta_head_only_info[0]
    elif not meta_head_only_info or meta_head_only_info[0] is None:
        limit = sql_node.limit
    else:
        limit = min(limit, meta_head_only_info[0])
    lsu__djmf, uyi__ydpn = bodo.ir.connector.generate_filter_map(sql_node.
        filters)
    isjf__cywcc = ', '.join(lsu__djmf.values())
    urf__ucim = (
        f'def sql_impl(sql_request, conn, database_schema, {isjf__cywcc}):\n')
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        if sql_node.filters:
            zfets__ned = []
            for jcq__wxklh in sql_node.filters:
                eud__wpb = []
                for yktk__swvgf in jcq__wxklh:
                    mcpp__lsr, zzel__mgnb = yktk__swvgf[0], yktk__swvgf[2]
                    mcpp__lsr = convert_col_name(mcpp__lsr, sql_node.
                        converted_colnames)
                    mcpp__lsr = '\\"' + mcpp__lsr + '\\"'
                    wul__uey = '{' + lsu__djmf[yktk__swvgf[2].name
                        ] + '}' if isinstance(yktk__swvgf[2], ir.Var
                        ) else zzel__mgnb
                    if yktk__swvgf[1] in ('startswith', 'endswith'):
                        bkhs__bds = ['(', yktk__swvgf[1], '(', mcpp__lsr,
                            ',', wul__uey, ')', ')']
                    else:
                        bkhs__bds = ['(', mcpp__lsr, yktk__swvgf[1],
                            wul__uey, ')']
                    eud__wpb.append(' '.join(bkhs__bds))
                zfets__ned.append(' ( ' + ' AND '.join(eud__wpb) + ' ) ')
            hietc__knnv = ' WHERE ' + ' OR '.join(zfets__ned)
            for bkaa__paa, vywah__zvh in enumerate(lsu__djmf.values()):
                urf__ucim += (
                    f'    {vywah__zvh} = get_sql_literal({vywah__zvh})\n')
            urf__ucim += (
                f'    sql_request = f"{{sql_request}} {hietc__knnv}"\n')
        if sql_node.limit != limit:
            urf__ucim += (
                f'    sql_request = f"{{sql_request}} LIMIT {limit}"\n')
    suzh__dzfl = ''
    if sql_node.db_type == 'iceberg':
        suzh__dzfl = isjf__cywcc
    urf__ucim += f"""    (total_rows, table_var, index_var, file_list, snapshot_id) = _sql_reader_py(sql_request, conn, database_schema, {suzh__dzfl})
"""
    gyx__lnvi = {}
    exec(urf__ucim, {}, gyx__lnvi)
    lhl__pcimv = gyx__lnvi['sql_impl']
    klyj__xupzw = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.out_used_cols, sql_node.converted_colnames, typingctx,
        targetctx, sql_node.db_type, limit, parallel, typemap, sql_node.
        filters, sql_node.pyarrow_schema, not sql_node.is_live_table,
        sql_node.is_select_query, sql_node.is_merge_into, is_independent)
    dnpem__jvjds = (types.none if sql_node.database_schema is None else
        string_type)
    xoz__lxvf = compile_to_numba_ir(lhl__pcimv, {'_sql_reader_py':
        klyj__xupzw, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type,
        dnpem__jvjds) + tuple(typemap[cmj__aiabu.name] for cmj__aiabu in
        uyi__ydpn), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        rbfb__tgbhl = [sql_node.df_colnames[bkaa__paa] for bkaa__paa in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            rbfb__tgbhl.append(sql_node.index_column_name)
        if len(rbfb__tgbhl) == 0:
            dve__qkbq = 'COUNT(*)'
        else:
            dve__qkbq = escape_column_names(rbfb__tgbhl, sql_node.db_type,
                sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            wuv__wderu = ('SELECT ' + dve__qkbq + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            wuv__wderu = ('SELECT ' + dve__qkbq + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        wuv__wderu = sql_node.sql_request
    replace_arg_nodes(xoz__lxvf, [ir.Const(wuv__wderu, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + uyi__ydpn)
    tlwjf__amico = xoz__lxvf.body[:-3]
    if meta_head_only_info:
        tlwjf__amico[-5].target = meta_head_only_info[1]
    tlwjf__amico[-4].target = sql_node.out_vars[0]
    tlwjf__amico[-3].target = sql_node.out_vars[1]
    assert sql_node.has_side_effects or not (sql_node.index_column_name is
        None and not sql_node.is_live_table
        ), 'At most one of table and index should be dead if the SQL IR node is live and has no side effects'
    if sql_node.index_column_name is None:
        tlwjf__amico.pop(-3)
    elif not sql_node.is_live_table:
        tlwjf__amico.pop(-4)
    if sql_node.file_list_live:
        tlwjf__amico[-2].target = sql_node.out_vars[2]
    else:
        tlwjf__amico.pop(-2)
    if sql_node.snapshot_id_live:
        tlwjf__amico[-1].target = sql_node.out_vars[3]
    else:
        tlwjf__amico.pop(-1)
    return tlwjf__amico


def convert_col_name(col_name: str, converted_colnames: List[str]) ->str:
    if col_name in converted_colnames:
        return col_name.upper()
    return col_name


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type == 'snowflake':
        from bodo.io.snowflake import escape_col_name
        dve__qkbq = ', '.join(escape_col_name(convert_col_name(rshlt__vrlm,
            converted_colnames)) for rshlt__vrlm in col_names)
    elif db_type == 'oracle':
        rbfb__tgbhl = []
        for rshlt__vrlm in col_names:
            rbfb__tgbhl.append(convert_col_name(rshlt__vrlm,
                converted_colnames))
        dve__qkbq = ', '.join([f'"{rshlt__vrlm}"' for rshlt__vrlm in
            rbfb__tgbhl])
    elif db_type == 'mysql':
        dve__qkbq = ', '.join([f'`{rshlt__vrlm}`' for rshlt__vrlm in col_names]
            )
    else:
        dve__qkbq = ', '.join([f'"{rshlt__vrlm}"' for rshlt__vrlm in col_names]
            )
    return dve__qkbq


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    ydq__qyejj = types.unliteral(filter_value)
    if ydq__qyejj == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(ydq__qyejj, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif isinstance(ydq__qyejj, bodo.PandasTimestampType):
        if ydq__qyejj.tz is None:
            lhhy__bvekn = 'TIMESTAMP_NTZ'
        else:
            lhhy__bvekn = 'TIMESTAMP_TZ'

        def impl(filter_value):
            awuik__ibm = filter_value.nanosecond
            piy__jveab = ''
            if awuik__ibm < 10:
                piy__jveab = '00'
            elif awuik__ibm < 100:
                piy__jveab = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{piy__jveab}{awuik__ibm}'::{lhhy__bvekn}"
                )
        return impl
    elif ydq__qyejj == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {ydq__qyejj} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float, bodo.PandasTimestampType
    oos__wkpt = bodo.datetime_date_type, types.unicode_type, types.bool_
    ydq__qyejj = types.unliteral(filter_value)
    if (isinstance(ydq__qyejj, (types.List, types.Array, bodo.
        IntegerArrayType, bodo.FloatingArrayType, bodo.DatetimeArrayType)) or
        ydq__qyejj in (bodo.string_array_type, bodo.dict_str_arr_type, bodo
        .boolean_array, bodo.datetime_date_array_type)) and (isinstance(
        ydq__qyejj.dtype, scalar_isinstance) or ydq__qyejj.dtype in oos__wkpt):

        def impl(filter_value):
            hvqkl__vope = ', '.join([_get_snowflake_sql_literal_scalar(
                rshlt__vrlm) for rshlt__vrlm in filter_value])
            return f'({hvqkl__vope})'
        return impl
    elif isinstance(ydq__qyejj, scalar_isinstance) or ydq__qyejj in oos__wkpt:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {ydq__qyejj} used in filter pushdown.'
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
    except ImportError as srfdp__wzjwi:
        nuhsj__qzxro = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(nuhsj__qzxro)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as srfdp__wzjwi:
        nuhsj__qzxro = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(nuhsj__qzxro)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as srfdp__wzjwi:
        nuhsj__qzxro = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(nuhsj__qzxro)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as srfdp__wzjwi:
        nuhsj__qzxro = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(nuhsj__qzxro)


def req_limit(sql_request):
    import re
    iao__ryt = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    actd__sva = iao__ryt.search(sql_request)
    if actd__sva:
        return int(actd__sva.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs: List[Any],
    index_column_name: Optional[str], index_column_type, out_used_cols:
    List[int], converted_colnames: List[str], typingctx, targetctx, db_type:
    str, limit: Optional[int], parallel: bool, typemap, filters: Optional[
    Any], pyarrow_schema: Optional[pa.Schema], is_dead_table: bool,
    is_select_query: bool, is_merge_into: bool, is_independent: bool):
    zrxw__wxz = next_label()
    rbfb__tgbhl = [col_names[bkaa__paa] for bkaa__paa in out_used_cols]
    tkz__uurpm = [col_typs[bkaa__paa] for bkaa__paa in out_used_cols]
    if index_column_name:
        rbfb__tgbhl.append(index_column_name)
        tkz__uurpm.append(index_column_type)
    blkyx__vwd = None
    pdkka__wizp = None
    bocj__opp = types.none if is_dead_table else TableType(tuple(col_typs))
    suzh__dzfl = ''
    lsu__djmf = {}
    uyi__ydpn = []
    if filters and db_type == 'iceberg':
        lsu__djmf, uyi__ydpn = bodo.ir.connector.generate_filter_map(filters)
        suzh__dzfl = ', '.join(lsu__djmf.values())
    urf__ucim = (
        f'def sql_reader_py(sql_request, conn, database_schema, {suzh__dzfl}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from an Iceberg database'
        momq__tsxn, zrj__pbdb = bodo.ir.connector.generate_arrow_filters(
            filters, lsu__djmf, uyi__ydpn, col_names, col_names, col_typs,
            typemap, 'iceberg')
        ubnso__fgsn = -1
        if is_merge_into and col_names.index('_bodo_row_id') in out_used_cols:
            ubnso__fgsn = col_names.index('_bodo_row_id')
        selected_cols: List[int] = [pyarrow_schema.get_field_index(
            col_names[bkaa__paa]) for bkaa__paa in out_used_cols if 
            bkaa__paa != ubnso__fgsn]
        xvh__ussdb = {gcan__rrweb: bkaa__paa for bkaa__paa, gcan__rrweb in
            enumerate(selected_cols)}
        nullable_cols = [int(is_nullable(col_typs[bkaa__paa])) for
            bkaa__paa in selected_cols]
        azq__vdu = [bkaa__paa for bkaa__paa in selected_cols if col_typs[
            bkaa__paa] == bodo.dict_str_arr_type]
        ogaod__tedvb = (
            f'dict_str_cols_arr_{zrxw__wxz}.ctypes, np.int32({len(azq__vdu)})'
             if azq__vdu else '0, 0')
        zcu__nwne = ',' if suzh__dzfl else ''
        urf__ucim += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{momq__tsxn}", "{zrj__pbdb}", ({suzh__dzfl}{zcu__nwne}))
  out_table, total_rows, file_list, snapshot_id = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{zrxw__wxz}.ctypes,
    {len(selected_cols)},
    nullable_cols_arr_{zrxw__wxz}.ctypes,
    pyarrow_schema_{zrxw__wxz},
    {ogaod__tedvb},
    {is_merge_into},
  )
"""
        if parallel:
            urf__ucim += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            urf__ucim += f'  local_rows = total_rows\n'
        blkyx__vwd = None
        if not is_dead_table:
            blkyx__vwd = []
            jqfqh__bgo = 0
            for bkaa__paa in range(len(col_names)):
                if jqfqh__bgo < len(out_used_cols
                    ) and bkaa__paa == out_used_cols[jqfqh__bgo]:
                    if bkaa__paa == ubnso__fgsn:
                        blkyx__vwd.append(len(selected_cols))
                    else:
                        blkyx__vwd.append(xvh__ussdb[bkaa__paa])
                    jqfqh__bgo += 1
                else:
                    blkyx__vwd.append(-1)
            blkyx__vwd = np.array(blkyx__vwd, dtype=np.int64)
        if is_dead_table:
            urf__ucim += '  table_var = None\n'
        else:
            urf__ucim += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{zrxw__wxz}, py_table_type_{zrxw__wxz})
"""
            if len(out_used_cols) == 0:
                urf__ucim += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        emdr__uhxx = 'None'
        if index_column_name is not None:
            hvx__twqkn = len(out_used_cols) + 1 if not is_dead_table else 0
            emdr__uhxx = (
                f'info_to_array(info_from_table(out_table, {hvx__twqkn}), index_col_typ)'
                )
        urf__ucim += f'  index_var = {emdr__uhxx}\n'
        urf__ucim += f'  delete_table(out_table)\n'
        urf__ucim += f'  ev.finalize()\n'
        urf__ucim += (
            '  return (total_rows, table_var, index_var, file_list, snapshot_id)\n'
            )
    elif db_type == 'snowflake':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from Snowflake'
        if is_select_query:
            gpgxk__xtcvr = []
            for col_name in rbfb__tgbhl:
                hrm__szlu = convert_col_name(col_name, converted_colnames)
                sixsu__qcsyh = pyarrow_schema.get_field_index(hrm__szlu)
                if sixsu__qcsyh < 0:
                    raise BodoError(
                        f'SQLReader Snowflake: Column {hrm__szlu} is not in source schema'
                        )
                gpgxk__xtcvr.append(pyarrow_schema.field(sixsu__qcsyh))
            pyarrow_schema = pa.schema(gpgxk__xtcvr)
        bma__vshwu = {gcan__rrweb: bkaa__paa for bkaa__paa, gcan__rrweb in
            enumerate(out_used_cols)}
        dfnf__nysgi = [bma__vshwu[bkaa__paa] for bkaa__paa in out_used_cols if
            col_typs[bkaa__paa] == dict_str_arr_type]
        nullable_cols = [int(is_nullable(col_typs[bkaa__paa])) for
            bkaa__paa in out_used_cols]
        if index_column_name:
            nullable_cols.append(int(is_nullable(index_column_type)))
        sue__lwr = np.array(dfnf__nysgi, dtype=np.int32)
        wvl__xbobt = np.array(nullable_cols, dtype=np.int32)
        urf__ucim += f"""  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = snowflake_read(
    unicode_to_utf8(sql_request),
    unicode_to_utf8(conn),
    {parallel},
    {is_independent},
    pyarrow_schema_{zrxw__wxz},
    {len(wvl__xbobt)},
    nullable_cols_array.ctypes,
    snowflake_dict_cols_array.ctypes,
    {len(sue__lwr)},
    total_rows_np.ctypes,
    {is_select_query and len(rbfb__tgbhl) == 0},
    {is_select_query},
  )
  check_and_propagate_cpp_exception()
"""
        urf__ucim += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            urf__ucim += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            urf__ucim += f'  local_rows = total_rows\n'
        if index_column_name:
            urf__ucim += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            urf__ucim += '  index_var = None\n'
        if not is_dead_table:
            sixsu__qcsyh = []
            jqfqh__bgo = 0
            for bkaa__paa in range(len(col_names)):
                if jqfqh__bgo < len(out_used_cols
                    ) and bkaa__paa == out_used_cols[jqfqh__bgo]:
                    sixsu__qcsyh.append(jqfqh__bgo)
                    jqfqh__bgo += 1
                else:
                    sixsu__qcsyh.append(-1)
            blkyx__vwd = np.array(sixsu__qcsyh, dtype=np.int64)
            urf__ucim += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{zrxw__wxz}, py_table_type_{zrxw__wxz})
"""
            if len(out_used_cols) == 0:
                if index_column_name:
                    urf__ucim += (
                        f'  table_var = set_table_len(table_var, len(index_var))\n'
                        )
                else:
                    urf__ucim += (
                        f'  table_var = set_table_len(table_var, local_rows)\n'
                        )
        else:
            urf__ucim += '  table_var = None\n'
        urf__ucim += '  delete_table(out_table)\n'
        urf__ucim += '  ev.finalize()\n'
        urf__ucim += (
            '  return (total_rows, table_var, index_var, None, None)\n')
    else:
        if not is_dead_table:
            urf__ucim += f"""  type_usecols_offsets_arr_{zrxw__wxz}_2 = type_usecols_offsets_arr_{zrxw__wxz}
"""
            pdkka__wizp = np.array(out_used_cols, dtype=np.int64)
        urf__ucim += '  df_typeref_2 = df_typeref\n'
        urf__ucim += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            urf__ucim += '  pymysql_check()\n'
        elif db_type == 'oracle':
            urf__ucim += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            urf__ucim += '  psycopg2_check()\n'
        if parallel:
            urf__ucim += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                urf__ucim += f'  nb_row = {limit}\n'
            else:
                urf__ucim += '  with objmode(nb_row="int64"):\n'
                urf__ucim += f'     if rank == {MPI_ROOT}:\n'
                urf__ucim += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                urf__ucim += '         frame = pd.read_sql(sql_cons, conn)\n'
                urf__ucim += '         nb_row = frame.iat[0,0]\n'
                urf__ucim += '     else:\n'
                urf__ucim += '         nb_row = 0\n'
                urf__ucim += '  nb_row = bcast_scalar(nb_row)\n'
            urf__ucim += f"""  with objmode(table_var=py_table_type_{zrxw__wxz}, index_var=index_col_typ):
"""
            urf__ucim += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                urf__ucim += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                urf__ucim += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            urf__ucim += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            urf__ucim += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            urf__ucim += f"""  with objmode(table_var=py_table_type_{zrxw__wxz}, index_var=index_col_typ):
"""
            urf__ucim += '    df_ret = pd.read_sql(sql_request, conn)\n'
            urf__ucim += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            urf__ucim += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            urf__ucim += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            urf__ucim += '    index_var = None\n'
        if not is_dead_table:
            urf__ucim += f'    arrs = []\n'
            urf__ucim += f'    for i in range(df_ret.shape[1]):\n'
            urf__ucim += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            urf__ucim += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{zrxw__wxz}_2, {len(col_names)})
"""
        else:
            urf__ucim += '    table_var = None\n'
        urf__ucim += '  return (-1, table_var, index_var, None, None)\n'
    sob__knjl = globals()
    sob__knjl.update({'bodo': bodo, f'py_table_type_{zrxw__wxz}': bocj__opp,
        'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        sob__knjl.update({f'table_idx_{zrxw__wxz}': blkyx__vwd,
            f'pyarrow_schema_{zrxw__wxz}': pyarrow_schema,
            'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'get_node_portion': bodo.libs.distributed_api.
            get_node_portion})
    if db_type == 'iceberg':
        sob__knjl.update({f'selected_cols_arr_{zrxw__wxz}': np.array(
            selected_cols, np.int32), f'nullable_cols_arr_{zrxw__wxz}': np.
            array(nullable_cols, np.int32),
            f'dict_str_cols_arr_{zrxw__wxz}': np.array(azq__vdu, np.int32),
            f'py_table_type_{zrxw__wxz}': bocj__opp, 'get_filters_pyobject':
            bodo.io.parquet_pio.get_filters_pyobject, 'iceberg_read':
            _iceberg_pq_read})
    elif db_type == 'snowflake':
        sob__knjl.update({'np': np, 'snowflake_read': _snowflake_read,
            'nullable_cols_array': wvl__xbobt, 'snowflake_dict_cols_array':
            sue__lwr})
    else:
        sob__knjl.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(tkz__uurpm), bodo.RangeIndexType(None),
            tuple(rbfb__tgbhl)), 'Table': Table,
            f'type_usecols_offsets_arr_{zrxw__wxz}': pdkka__wizp})
    gyx__lnvi = {}
    exec(urf__ucim, sob__knjl, gyx__lnvi)
    klyj__xupzw = gyx__lnvi['sql_reader_py']
    ekg__ubem = numba.njit(klyj__xupzw)
    compiled_funcs.append(ekg__ubem)
    return ekg__ubem


parquet_predicate_type = ParquetPredicateType()
pyarrow_schema_type = PyArrowTableSchemaType()


@intrinsic
def _iceberg_pq_read(typingctx, conn_str, db_schema, sql_request_str,
    parallel, limit, dnf_filters, expr_filters, selected_cols,
    num_selected_cols, nullable_cols, pyarrow_schema, dict_encoded_cols,
    num_dict_encoded_cols, is_merge_into_cow):

    def codegen(context, builder, signature, args):
        bow__blbwk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(1), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(64).as_pointer()])
        gtzpw__ugny = cgutils.get_or_insert_function(builder.module,
            bow__blbwk, name='iceberg_pq_read')
        qzdfn__ohm = cgutils.alloca_once(builder, lir.IntType(64))
        chwg__fjue = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        mdy__ntm = cgutils.alloca_once(builder, lir.IntType(64))
        gvfq__hurai = args + (qzdfn__ohm, chwg__fjue, mdy__ntm)
        kcfkf__gezyt = builder.call(gtzpw__ugny, gvfq__hurai)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        uqpe__usxw = builder.load(chwg__fjue)
        aizgh__fqmj = cgutils.create_struct_proxy(types.pyobject_of_list_type)(
            context, builder)
        wgqj__czv = context.get_python_api(builder)
        aizgh__fqmj.meminfo = wgqj__czv.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), uqpe__usxw)
        aizgh__fqmj.pyobj = uqpe__usxw
        wgqj__czv.decref(uqpe__usxw)
        rtktp__ovop = [kcfkf__gezyt, builder.load(qzdfn__ohm), aizgh__fqmj.
            _getvalue(), builder.load(mdy__ntm)]
        return context.make_tuple(builder, zcf__fqgmx, rtktp__ovop)
    zcf__fqgmx = types.Tuple([table_type, types.int64, types.
        pyobject_of_list_type, types.int64])
    vpohp__trqmc = zcf__fqgmx(types.voidptr, types.voidptr, types.voidptr,
        types.boolean, types.int64, parquet_predicate_type,
        parquet_predicate_type, types.voidptr, types.int32, types.voidptr,
        pyarrow_schema_type, types.voidptr, types.int32, types.boolean)
    return vpohp__trqmc, codegen


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.boolean,
    pyarrow_schema_type, types.int64, types.voidptr, types.voidptr, types.
    int32, types.voidptr, types.boolean, types.boolean))
