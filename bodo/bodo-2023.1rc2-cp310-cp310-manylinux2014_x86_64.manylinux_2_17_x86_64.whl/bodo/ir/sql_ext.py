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
        wsqdz__drs = tuple(rgr__xrep.name for rgr__xrep in self.out_vars)
        return (
            f'{wsqdz__drs} = SQLReader(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_schema={self.pyarrow_schema}, is_merge_into={self.is_merge_into})'
            )


def parse_dbtype(con_str):
    ukef__bfr = urlparse(con_str)
    db_type = ukef__bfr.scheme
    chqqs__byax = ukef__bfr.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', chqqs__byax
    if db_type == 'mysql+pymysql':
        return 'mysql', chqqs__byax
    if con_str.startswith('iceberg+glue') or ukef__bfr.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', chqqs__byax
    return db_type, chqqs__byax


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
    jkxtv__vhf = sql_node.out_vars[0].name
    erlc__bvk = sql_node.out_vars[1].name
    svwd__iaen = sql_node.out_vars[2].name if len(sql_node.out_vars
        ) > 2 else None
    mmjaw__jywu = sql_node.out_vars[3].name if len(sql_node.out_vars
        ) > 3 else None
    if (not sql_node.has_side_effects and jkxtv__vhf not in lives and 
        erlc__bvk not in lives and svwd__iaen not in lives and mmjaw__jywu
         not in lives):
        return None
    if jkxtv__vhf not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
        sql_node.is_live_table = False
    if erlc__bvk not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    if svwd__iaen not in lives:
        sql_node.file_list_live = False
        sql_node.file_list_type = types.none
    if mmjaw__jywu not in lives:
        sql_node.snapshot_id_live = False
        sql_node.snapshot_id_type = types.none
    return sql_node


def sql_distributed_run(sql_node: SqlReader, array_dists, typemap,
    calltypes, typingctx, targetctx, is_independent=False,
    meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        ptsq__atxhl = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        zfs__aqm = []
        dict_encoded_cols = []
        for ziqgb__tdl in sql_node.out_used_cols:
            sshu__amave = sql_node.df_colnames[ziqgb__tdl]
            zfs__aqm.append(sshu__amave)
            if isinstance(sql_node.out_types[ziqgb__tdl], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(sshu__amave)
        if sql_node.index_column_name:
            zfs__aqm.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(sql_node.index_column_name)
        ragfi__wkaaq = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', ptsq__atxhl,
            ragfi__wkaaq, zfs__aqm)
        if dict_encoded_cols:
            ynczy__qbtlr = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                ynczy__qbtlr, ragfi__wkaaq, dict_encoded_cols)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        udom__fhqk = set(sql_node.unsupported_columns)
        ugny__xvva = set(sql_node.out_used_cols)
        jboib__fibpq = ugny__xvva & udom__fhqk
        if jboib__fibpq:
            jfjn__legfc = sorted(jboib__fibpq)
            skd__kfria = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            gpyh__cdb = 0
            for see__ywic in jfjn__legfc:
                while sql_node.unsupported_columns[gpyh__cdb] != see__ywic:
                    gpyh__cdb += 1
                skd__kfria.append(
                    f"Column '{sql_node.original_df_colnames[see__ywic]}' with unsupported arrow type {sql_node.unsupported_arrow_types[gpyh__cdb]}"
                    )
                gpyh__cdb += 1
            milsi__qtrav = '\n'.join(skd__kfria)
            raise BodoError(milsi__qtrav, loc=sql_node.loc)
    if sql_node.limit is None and (not meta_head_only_info or 
        meta_head_only_info[0] is None):
        limit = None
    elif sql_node.limit is None:
        limit = meta_head_only_info[0]
    elif not meta_head_only_info or meta_head_only_info[0] is None:
        limit = sql_node.limit
    else:
        limit = min(limit, meta_head_only_info[0])
    qnvjo__ursg, wuqhj__ppx = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    rzsoz__frrkh = ', '.join(qnvjo__ursg.values())
    syik__xoq = (
        f'def sql_impl(sql_request, conn, database_schema, {rzsoz__frrkh}):\n')
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        if sql_node.filters:
            rscwm__jjhed = []
            for vxlv__zkaww in sql_node.filters:
                nnunh__ohoq = []
                for ydt__iio in vxlv__zkaww:
                    ahypv__vvpoj, jnagd__couzh = ydt__iio[0], ydt__iio[2]
                    ahypv__vvpoj = convert_col_name(ahypv__vvpoj, sql_node.
                        converted_colnames)
                    ahypv__vvpoj = '\\"' + ahypv__vvpoj + '\\"'
                    ocsgq__lzd = '{' + qnvjo__ursg[ydt__iio[2].name
                        ] + '}' if isinstance(ydt__iio[2], ir.Var
                        ) else jnagd__couzh
                    if ydt__iio[1] in ('startswith', 'endswith'):
                        trm__qtuup = ['(', ydt__iio[1], '(', ahypv__vvpoj,
                            ',', ocsgq__lzd, ')', ')']
                    else:
                        trm__qtuup = ['(', ahypv__vvpoj, ydt__iio[1],
                            ocsgq__lzd, ')']
                    nnunh__ohoq.append(' '.join(trm__qtuup))
                rscwm__jjhed.append(' ( ' + ' AND '.join(nnunh__ohoq) + ' ) ')
            ygt__bgn = ' WHERE ' + ' OR '.join(rscwm__jjhed)
            for ziqgb__tdl, clt__vnmum in enumerate(qnvjo__ursg.values()):
                syik__xoq += (
                    f'    {clt__vnmum} = get_sql_literal({clt__vnmum})\n')
            syik__xoq += f'    sql_request = f"{{sql_request}} {ygt__bgn}"\n'
        if sql_node.limit != limit:
            syik__xoq += (
                f'    sql_request = f"{{sql_request}} LIMIT {limit}"\n')
    zly__fftpz = ''
    if sql_node.db_type == 'iceberg':
        zly__fftpz = rzsoz__frrkh
    syik__xoq += f"""    (total_rows, table_var, index_var, file_list, snapshot_id) = _sql_reader_py(sql_request, conn, database_schema, {zly__fftpz})
"""
    cems__mfv = {}
    exec(syik__xoq, {}, cems__mfv)
    cwtfw__cijk = cems__mfv['sql_impl']
    qymc__jlcv = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.out_used_cols, sql_node.converted_colnames, typingctx,
        targetctx, sql_node.db_type, limit, parallel, typemap, sql_node.
        filters, sql_node.pyarrow_schema, not sql_node.is_live_table,
        sql_node.is_select_query, sql_node.is_merge_into, is_independent)
    fyf__ngb = types.none if sql_node.database_schema is None else string_type
    ufji__vwix = compile_to_numba_ir(cwtfw__cijk, {'_sql_reader_py':
        qymc__jlcv, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type, fyf__ngb) +
        tuple(typemap[rgr__xrep.name] for rgr__xrep in wuqhj__ppx), typemap
        =typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        erb__gpytw = [sql_node.df_colnames[ziqgb__tdl] for ziqgb__tdl in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            erb__gpytw.append(sql_node.index_column_name)
        if len(erb__gpytw) == 0:
            fcv__szqk = 'COUNT(*)'
        else:
            fcv__szqk = escape_column_names(erb__gpytw, sql_node.db_type,
                sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            wncv__hkoi = ('SELECT ' + fcv__szqk + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            wncv__hkoi = ('SELECT ' + fcv__szqk + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        wncv__hkoi = sql_node.sql_request
    replace_arg_nodes(ufji__vwix, [ir.Const(wncv__hkoi, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + wuqhj__ppx)
    jeri__gbh = ufji__vwix.body[:-3]
    if meta_head_only_info:
        jeri__gbh[-5].target = meta_head_only_info[1]
    jeri__gbh[-4].target = sql_node.out_vars[0]
    jeri__gbh[-3].target = sql_node.out_vars[1]
    assert sql_node.has_side_effects or not (sql_node.index_column_name is
        None and not sql_node.is_live_table
        ), 'At most one of table and index should be dead if the SQL IR node is live and has no side effects'
    if sql_node.index_column_name is None:
        jeri__gbh.pop(-3)
    elif not sql_node.is_live_table:
        jeri__gbh.pop(-4)
    if sql_node.file_list_live:
        jeri__gbh[-2].target = sql_node.out_vars[2]
    else:
        jeri__gbh.pop(-2)
    if sql_node.snapshot_id_live:
        jeri__gbh[-1].target = sql_node.out_vars[3]
    else:
        jeri__gbh.pop(-1)
    return jeri__gbh


def convert_col_name(col_name: str, converted_colnames: List[str]) ->str:
    if col_name in converted_colnames:
        return col_name.upper()
    return col_name


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type == 'snowflake':
        from bodo.io.snowflake import escape_col_name
        fcv__szqk = ', '.join(escape_col_name(convert_col_name(eljod__sncmo,
            converted_colnames)) for eljod__sncmo in col_names)
    elif db_type == 'oracle':
        erb__gpytw = []
        for eljod__sncmo in col_names:
            erb__gpytw.append(convert_col_name(eljod__sncmo,
                converted_colnames))
        fcv__szqk = ', '.join([f'"{eljod__sncmo}"' for eljod__sncmo in
            erb__gpytw])
    elif db_type == 'mysql':
        fcv__szqk = ', '.join([f'`{eljod__sncmo}`' for eljod__sncmo in
            col_names])
    else:
        fcv__szqk = ', '.join([f'"{eljod__sncmo}"' for eljod__sncmo in
            col_names])
    return fcv__szqk


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    scki__oiyuh = types.unliteral(filter_value)
    if scki__oiyuh == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(scki__oiyuh, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif isinstance(scki__oiyuh, bodo.PandasTimestampType):
        if scki__oiyuh.tz is None:
            exgei__kzeg = 'TIMESTAMP_NTZ'
        else:
            exgei__kzeg = 'TIMESTAMP_TZ'

        def impl(filter_value):
            hslvy__tady = filter_value.nanosecond
            xtse__xqxua = ''
            if hslvy__tady < 10:
                xtse__xqxua = '00'
            elif hslvy__tady < 100:
                xtse__xqxua = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{xtse__xqxua}{hslvy__tady}'::{exgei__kzeg}"
                )
        return impl
    elif scki__oiyuh == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {scki__oiyuh} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float, bodo.PandasTimestampType
    cfng__gubt = bodo.datetime_date_type, types.unicode_type, types.bool_
    scki__oiyuh = types.unliteral(filter_value)
    if (isinstance(scki__oiyuh, (types.List, types.Array, bodo.
        IntegerArrayType, bodo.FloatingArrayType, bodo.DatetimeArrayType)) or
        scki__oiyuh in (bodo.string_array_type, bodo.dict_str_arr_type,
        bodo.boolean_array, bodo.datetime_date_array_type)) and (isinstance
        (scki__oiyuh.dtype, scalar_isinstance) or scki__oiyuh.dtype in
        cfng__gubt):

        def impl(filter_value):
            ntuyy__xcwrj = ', '.join([_get_snowflake_sql_literal_scalar(
                eljod__sncmo) for eljod__sncmo in filter_value])
            return f'({ntuyy__xcwrj})'
        return impl
    elif isinstance(scki__oiyuh, scalar_isinstance
        ) or scki__oiyuh in cfng__gubt:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {scki__oiyuh} used in filter pushdown.'
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
    except ImportError as rgih__dih:
        xzuz__ugqg = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(xzuz__ugqg)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as rgih__dih:
        xzuz__ugqg = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(xzuz__ugqg)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as rgih__dih:
        xzuz__ugqg = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(xzuz__ugqg)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as rgih__dih:
        xzuz__ugqg = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(xzuz__ugqg)


def req_limit(sql_request):
    import re
    wrh__gxh = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    cbexq__orx = wrh__gxh.search(sql_request)
    if cbexq__orx:
        return int(cbexq__orx.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs: List[Any],
    index_column_name: Optional[str], index_column_type, out_used_cols:
    List[int], converted_colnames: List[str], typingctx, targetctx, db_type:
    str, limit: Optional[int], parallel: bool, typemap, filters: Optional[
    Any], pyarrow_schema: Optional[pa.Schema], is_dead_table: bool,
    is_select_query: bool, is_merge_into: bool, is_independent: bool):
    otow__hlm = next_label()
    erb__gpytw = [col_names[ziqgb__tdl] for ziqgb__tdl in out_used_cols]
    bns__vkl = [col_typs[ziqgb__tdl] for ziqgb__tdl in out_used_cols]
    if index_column_name:
        erb__gpytw.append(index_column_name)
        bns__vkl.append(index_column_type)
    uhs__kgku = None
    xcyaj__qdo = None
    tdhch__tlmy = types.none if is_dead_table else TableType(tuple(col_typs))
    zly__fftpz = ''
    qnvjo__ursg = {}
    wuqhj__ppx = []
    if filters and db_type == 'iceberg':
        qnvjo__ursg, wuqhj__ppx = bodo.ir.connector.generate_filter_map(filters
            )
        zly__fftpz = ', '.join(qnvjo__ursg.values())
    syik__xoq = (
        f'def sql_reader_py(sql_request, conn, database_schema, {zly__fftpz}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from an Iceberg database'
        ihgy__yayce, cjyh__wsoz = bodo.ir.connector.generate_arrow_filters(
            filters, qnvjo__ursg, wuqhj__ppx, col_names, col_names,
            col_typs, typemap, 'iceberg')
        ouy__afst = -1
        if is_merge_into and col_names.index('_bodo_row_id') in out_used_cols:
            ouy__afst = col_names.index('_bodo_row_id')
        selected_cols: List[int] = [pyarrow_schema.get_field_index(
            col_names[ziqgb__tdl]) for ziqgb__tdl in out_used_cols if 
            ziqgb__tdl != ouy__afst]
        mzh__ueki = {eju__pif: ziqgb__tdl for ziqgb__tdl, eju__pif in
            enumerate(selected_cols)}
        nullable_cols = [int(is_nullable(col_typs[ziqgb__tdl])) for
            ziqgb__tdl in selected_cols]
        dbklr__gzd = [ziqgb__tdl for ziqgb__tdl in selected_cols if 
            col_typs[ziqgb__tdl] == bodo.dict_str_arr_type]
        rmrq__zgnn = (
            f'dict_str_cols_arr_{otow__hlm}.ctypes, np.int32({len(dbklr__gzd)})'
             if dbklr__gzd else '0, 0')
        mjt__hojrl = ',' if zly__fftpz else ''
        syik__xoq += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{ihgy__yayce}", "{cjyh__wsoz}", ({zly__fftpz}{mjt__hojrl}))
  out_table, total_rows, file_list, snapshot_id = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{otow__hlm}.ctypes,
    {len(selected_cols)},
    nullable_cols_arr_{otow__hlm}.ctypes,
    pyarrow_schema_{otow__hlm},
    {rmrq__zgnn},
    {is_merge_into},
  )
"""
        if parallel:
            syik__xoq += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            syik__xoq += f'  local_rows = total_rows\n'
        uhs__kgku = None
        if not is_dead_table:
            uhs__kgku = []
            osbq__kda = 0
            for ziqgb__tdl in range(len(col_names)):
                if osbq__kda < len(out_used_cols
                    ) and ziqgb__tdl == out_used_cols[osbq__kda]:
                    if ziqgb__tdl == ouy__afst:
                        uhs__kgku.append(len(selected_cols))
                    else:
                        uhs__kgku.append(mzh__ueki[ziqgb__tdl])
                    osbq__kda += 1
                else:
                    uhs__kgku.append(-1)
            uhs__kgku = np.array(uhs__kgku, dtype=np.int64)
        if is_dead_table:
            syik__xoq += '  table_var = None\n'
        else:
            syik__xoq += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{otow__hlm}, py_table_type_{otow__hlm})
"""
            if len(out_used_cols) == 0:
                syik__xoq += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        erlc__bvk = 'None'
        if index_column_name is not None:
            japnh__opjf = len(out_used_cols) + 1 if not is_dead_table else 0
            erlc__bvk = (
                f'info_to_array(info_from_table(out_table, {japnh__opjf}), index_col_typ)'
                )
        syik__xoq += f'  index_var = {erlc__bvk}\n'
        syik__xoq += f'  delete_table(out_table)\n'
        syik__xoq += f'  ev.finalize()\n'
        syik__xoq += (
            '  return (total_rows, table_var, index_var, file_list, snapshot_id)\n'
            )
    elif db_type == 'snowflake':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from Snowflake'
        if is_select_query:
            lgi__mlmo = []
            for col_name in erb__gpytw:
                ywjoe__ewtwc = convert_col_name(col_name, converted_colnames)
                gpyh__cdb = pyarrow_schema.get_field_index(ywjoe__ewtwc)
                if gpyh__cdb < 0:
                    raise BodoError(
                        f'SQLReader Snowflake: Column {ywjoe__ewtwc} is not in source schema'
                        )
                lgi__mlmo.append(pyarrow_schema.field(gpyh__cdb))
            pyarrow_schema = pa.schema(lgi__mlmo)
        hih__vplbw = {eju__pif: ziqgb__tdl for ziqgb__tdl, eju__pif in
            enumerate(out_used_cols)}
        nzcot__vzkl = [hih__vplbw[ziqgb__tdl] for ziqgb__tdl in
            out_used_cols if col_typs[ziqgb__tdl] == dict_str_arr_type]
        nullable_cols = [int(is_nullable(col_typs[ziqgb__tdl])) for
            ziqgb__tdl in out_used_cols]
        if index_column_name:
            nullable_cols.append(int(is_nullable(index_column_type)))
        vnqdh__vni = np.array(nzcot__vzkl, dtype=np.int32)
        aeaun__mjrrw = np.array(nullable_cols, dtype=np.int32)
        syik__xoq += f"""  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = snowflake_read(
    unicode_to_utf8(sql_request),
    unicode_to_utf8(conn),
    {parallel},
    {is_independent},
    pyarrow_schema_{otow__hlm},
    {len(aeaun__mjrrw)},
    nullable_cols_array.ctypes,
    snowflake_dict_cols_array.ctypes,
    {len(vnqdh__vni)},
    total_rows_np.ctypes,
    {is_select_query and len(erb__gpytw) == 0},
    {is_select_query},
  )
  check_and_propagate_cpp_exception()
"""
        syik__xoq += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            syik__xoq += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            syik__xoq += f'  local_rows = total_rows\n'
        if index_column_name:
            syik__xoq += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            syik__xoq += '  index_var = None\n'
        if not is_dead_table:
            gpyh__cdb = []
            osbq__kda = 0
            for ziqgb__tdl in range(len(col_names)):
                if osbq__kda < len(out_used_cols
                    ) and ziqgb__tdl == out_used_cols[osbq__kda]:
                    gpyh__cdb.append(osbq__kda)
                    osbq__kda += 1
                else:
                    gpyh__cdb.append(-1)
            uhs__kgku = np.array(gpyh__cdb, dtype=np.int64)
            syik__xoq += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{otow__hlm}, py_table_type_{otow__hlm})
"""
            if len(out_used_cols) == 0:
                if index_column_name:
                    syik__xoq += (
                        f'  table_var = set_table_len(table_var, len(index_var))\n'
                        )
                else:
                    syik__xoq += (
                        f'  table_var = set_table_len(table_var, local_rows)\n'
                        )
        else:
            syik__xoq += '  table_var = None\n'
        syik__xoq += '  delete_table(out_table)\n'
        syik__xoq += '  ev.finalize()\n'
        syik__xoq += (
            '  return (total_rows, table_var, index_var, None, None)\n')
    else:
        if not is_dead_table:
            syik__xoq += f"""  type_usecols_offsets_arr_{otow__hlm}_2 = type_usecols_offsets_arr_{otow__hlm}
"""
            xcyaj__qdo = np.array(out_used_cols, dtype=np.int64)
        syik__xoq += '  df_typeref_2 = df_typeref\n'
        syik__xoq += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            syik__xoq += '  pymysql_check()\n'
        elif db_type == 'oracle':
            syik__xoq += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            syik__xoq += '  psycopg2_check()\n'
        if parallel:
            syik__xoq += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                syik__xoq += f'  nb_row = {limit}\n'
            else:
                syik__xoq += '  with objmode(nb_row="int64"):\n'
                syik__xoq += f'     if rank == {MPI_ROOT}:\n'
                syik__xoq += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                syik__xoq += '         frame = pd.read_sql(sql_cons, conn)\n'
                syik__xoq += '         nb_row = frame.iat[0,0]\n'
                syik__xoq += '     else:\n'
                syik__xoq += '         nb_row = 0\n'
                syik__xoq += '  nb_row = bcast_scalar(nb_row)\n'
            syik__xoq += f"""  with objmode(table_var=py_table_type_{otow__hlm}, index_var=index_col_typ):
"""
            syik__xoq += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                syik__xoq += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                syik__xoq += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            syik__xoq += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            syik__xoq += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            syik__xoq += f"""  with objmode(table_var=py_table_type_{otow__hlm}, index_var=index_col_typ):
"""
            syik__xoq += '    df_ret = pd.read_sql(sql_request, conn)\n'
            syik__xoq += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            syik__xoq += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            syik__xoq += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            syik__xoq += '    index_var = None\n'
        if not is_dead_table:
            syik__xoq += f'    arrs = []\n'
            syik__xoq += f'    for i in range(df_ret.shape[1]):\n'
            syik__xoq += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            syik__xoq += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{otow__hlm}_2, {len(col_names)})
"""
        else:
            syik__xoq += '    table_var = None\n'
        syik__xoq += '  return (-1, table_var, index_var, None, None)\n'
    tlhgt__wnlg = globals()
    tlhgt__wnlg.update({'bodo': bodo, f'py_table_type_{otow__hlm}':
        tdhch__tlmy, 'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        tlhgt__wnlg.update({f'table_idx_{otow__hlm}': uhs__kgku,
            f'pyarrow_schema_{otow__hlm}': pyarrow_schema,
            'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'get_node_portion': bodo.libs.distributed_api.
            get_node_portion})
    if db_type == 'iceberg':
        tlhgt__wnlg.update({f'selected_cols_arr_{otow__hlm}': np.array(
            selected_cols, np.int32), f'nullable_cols_arr_{otow__hlm}': np.
            array(nullable_cols, np.int32),
            f'dict_str_cols_arr_{otow__hlm}': np.array(dbklr__gzd, np.int32
            ), f'py_table_type_{otow__hlm}': tdhch__tlmy,
            'get_filters_pyobject': bodo.io.parquet_pio.
            get_filters_pyobject, 'iceberg_read': _iceberg_pq_read})
    elif db_type == 'snowflake':
        tlhgt__wnlg.update({'np': np, 'snowflake_read': _snowflake_read,
            'nullable_cols_array': aeaun__mjrrw,
            'snowflake_dict_cols_array': vnqdh__vni})
    else:
        tlhgt__wnlg.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(bns__vkl), bodo.RangeIndexType(None),
            tuple(erb__gpytw)), 'Table': Table,
            f'type_usecols_offsets_arr_{otow__hlm}': xcyaj__qdo})
    cems__mfv = {}
    exec(syik__xoq, tlhgt__wnlg, cems__mfv)
    qymc__jlcv = cems__mfv['sql_reader_py']
    zejnl__vtho = numba.njit(qymc__jlcv)
    compiled_funcs.append(zejnl__vtho)
    return zejnl__vtho


parquet_predicate_type = ParquetPredicateType()
pyarrow_schema_type = PyArrowTableSchemaType()


@intrinsic
def _iceberg_pq_read(typingctx, conn_str, db_schema, sql_request_str,
    parallel, limit, dnf_filters, expr_filters, selected_cols,
    num_selected_cols, nullable_cols, pyarrow_schema, dict_encoded_cols,
    num_dict_encoded_cols, is_merge_into_cow):

    def codegen(context, builder, signature, args):
        klc__mhgtt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(1), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(64).as_pointer()])
        lzxs__eyq = cgutils.get_or_insert_function(builder.module,
            klc__mhgtt, name='iceberg_pq_read')
        uhdl__yknq = cgutils.alloca_once(builder, lir.IntType(64))
        vrp__ciamk = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        qyz__kloqo = cgutils.alloca_once(builder, lir.IntType(64))
        nxj__tkx = args + (uhdl__yknq, vrp__ciamk, qyz__kloqo)
        okpj__wehat = builder.call(lzxs__eyq, nxj__tkx)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        glid__qxvf = builder.load(vrp__ciamk)
        sgv__pisk = cgutils.create_struct_proxy(types.pyobject_of_list_type)(
            context, builder)
        isr__tjbhf = context.get_python_api(builder)
        sgv__pisk.meminfo = isr__tjbhf.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), glid__qxvf)
        sgv__pisk.pyobj = glid__qxvf
        isr__tjbhf.decref(glid__qxvf)
        lkjq__dyd = [okpj__wehat, builder.load(uhdl__yknq), sgv__pisk.
            _getvalue(), builder.load(qyz__kloqo)]
        return context.make_tuple(builder, gsxhj__lqd, lkjq__dyd)
    gsxhj__lqd = types.Tuple([table_type, types.int64, types.
        pyobject_of_list_type, types.int64])
    oyeg__sor = gsxhj__lqd(types.voidptr, types.voidptr, types.voidptr,
        types.boolean, types.int64, parquet_predicate_type,
        parquet_predicate_type, types.voidptr, types.int32, types.voidptr,
        pyarrow_schema_type, types.voidptr, types.int32, types.boolean)
    return oyeg__sor, codegen


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.boolean,
    pyarrow_schema_type, types.int64, types.voidptr, types.voidptr, types.
    int32, types.voidptr, types.boolean, types.boolean))
