"""
File that contains the main functionality for the Iceberg
integration within the Bodo repo. This does not contain the
main IR transformation.
"""
import os
import re
import sys
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.extending import intrinsic
import bodo
from bodo.io.fs_io import get_s3_bucket_region_njit
from bodo.io.helpers import _get_numba_typ_from_pa_typ, pyarrow_table_schema_type
from bodo.libs.array import arr_info_list_to_table, array_to_info, py_table_to_cpp_table
from bodo.libs.str_ext import unicode_to_utf8
from bodo.utils import tracing
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError


def format_iceberg_conn(conn_str: str) ->str:
    nsuic__fdtxt = urlparse(conn_str)
    if not conn_str.startswith('iceberg+glue') and nsuic__fdtxt.scheme not in (
        'iceberg', 'iceberg+file', 'iceberg+s3', 'iceberg+thrift',
        'iceberg+http', 'iceberg+https'):
        raise BodoError(
            "'con' must start with one of the following: 'iceberg://', 'iceberg+file://', 'iceberg+s3://', 'iceberg+thrift://', 'iceberg+http://', 'iceberg+https://', 'iceberg+glue'"
            )
    if sys.version_info.minor < 9:
        if conn_str.startswith('iceberg+'):
            conn_str = conn_str[len('iceberg+'):]
        if conn_str.startswith('iceberg://'):
            conn_str = conn_str[len('iceberg://'):]
    else:
        conn_str = conn_str.removeprefix('iceberg+').removeprefix('iceberg://')
    return conn_str


@numba.njit
def format_iceberg_conn_njit(conn_str):
    with numba.objmode(conn_str='unicode_type'):
        conn_str = format_iceberg_conn(conn_str)
    return conn_str


def get_iceberg_type_info(table_name: str, con: str, database_schema: str,
    is_merge_into_cow: bool=False):
    import bodo_iceberg_connector
    import numba.core
    pvbrr__fcc = None
    yaau__jsrjq = None
    txk__gxbv = None
    if bodo.get_rank() == 0:
        try:
            pvbrr__fcc, yaau__jsrjq, txk__gxbv = (bodo_iceberg_connector.
                get_iceberg_typing_schema(con, database_schema, table_name))
            if txk__gxbv is None:
                raise BodoError('No such Iceberg table found')
        except bodo_iceberg_connector.IcebergError as siwb__tfbc:
            if isinstance(siwb__tfbc, bodo_iceberg_connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                pvbrr__fcc = BodoError(
                    f'{siwb__tfbc.message}: {siwb__tfbc.java_error}')
            else:
                pvbrr__fcc = BodoError(siwb__tfbc.message)
    mfdp__fto = MPI.COMM_WORLD
    pvbrr__fcc = mfdp__fto.bcast(pvbrr__fcc)
    if isinstance(pvbrr__fcc, Exception):
        raise pvbrr__fcc
    col_names = pvbrr__fcc
    yaau__jsrjq = mfdp__fto.bcast(yaau__jsrjq)
    txk__gxbv = mfdp__fto.bcast(txk__gxbv)
    cxvo__velv = [_get_numba_typ_from_pa_typ(typ, False, True, None)[0] for
        typ in yaau__jsrjq]
    if is_merge_into_cow:
        col_names.append('_bodo_row_id')
        cxvo__velv.append(types.Array(types.int64, 1, 'C'))
    return col_names, cxvo__velv, txk__gxbv


def get_iceberg_file_list(table_name: str, conn: str, database_schema: str,
    filters) ->Tuple[List[str], List[str]]:
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_file_list should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        pxe__vqde = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as siwb__tfbc:
        if isinstance(siwb__tfbc, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{siwb__tfbc.message}:\n{siwb__tfbc.java_error}')
        else:
            raise BodoError(siwb__tfbc.message)
    return pxe__vqde


def get_iceberg_snapshot_id(table_name: str, conn: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_snapshot_id should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        snapshot_id = (bodo_iceberg_connector.
            bodo_connector_get_current_snapshot_id(conn, database_schema,
            table_name))
    except bodo_iceberg_connector.IcebergError as siwb__tfbc:
        if isinstance(siwb__tfbc, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{siwb__tfbc.message}:\n{siwb__tfbc.java_error}')
        else:
            raise BodoError(siwb__tfbc.message)
    return snapshot_id


class IcebergParquetDataset:

    def __init__(self, conn, database_schema, table_name, pa_table_schema,
        pq_file_list, snapshot_id, pq_dataset=None):
        self.pq_dataset = pq_dataset
        self.conn = conn
        self.database_schema = database_schema
        self.table_name = table_name
        self.schema = pa_table_schema
        self.file_list = pq_file_list
        self.snapshot_id = snapshot_id
        self.pieces = []
        self._bodo_total_rows = 0
        self._prefix = ''
        self.filesystem = None
        if pq_dataset is not None:
            self.pieces = pq_dataset.pieces
            self._bodo_total_rows = pq_dataset._bodo_total_rows
            self._prefix = pq_dataset._prefix
            self.filesystem = pq_dataset.filesystem


def get_iceberg_pq_dataset(conn: str, database_schema: str, table_name: str,
    typing_pa_table_schema: pa.Schema, dnf_filters=None, expr_filters=None,
    tot_rows_to_read=None, is_parallel=False, get_row_counts=True):
    izhys__oxld = get_row_counts and tracing.is_tracing()
    if izhys__oxld:
        acpt__cjob = tracing.Event('get_iceberg_pq_dataset')
    mfdp__fto = MPI.COMM_WORLD
    avozk__vqy = None
    vbzhp__rmpv = None
    jjdb__neuf = None
    if bodo.get_rank() == 0:
        if izhys__oxld:
            mkpi__ryvv = tracing.Event('get_iceberg_file_list', is_parallel
                =False)
            mkpi__ryvv.add_attribute('g_dnf_filter', str(dnf_filters))
        try:
            avozk__vqy, jjdb__neuf = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if izhys__oxld:
                ubqa__fnp = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                mkpi__ryvv.add_attribute('num_files', len(avozk__vqy))
                mkpi__ryvv.add_attribute(f'first_{ubqa__fnp}_files', ', '.
                    join(avozk__vqy[:ubqa__fnp]))
        except Exception as siwb__tfbc:
            avozk__vqy = siwb__tfbc
        if izhys__oxld:
            mkpi__ryvv.finalize()
            oog__lvf = tracing.Event('get_snapshot_id', is_parallel=False)
        try:
            vbzhp__rmpv = get_iceberg_snapshot_id(table_name, conn,
                database_schema)
        except Exception as siwb__tfbc:
            vbzhp__rmpv = siwb__tfbc
        if izhys__oxld:
            oog__lvf.finalize()
    avozk__vqy, vbzhp__rmpv, jjdb__neuf = mfdp__fto.bcast((avozk__vqy,
        vbzhp__rmpv, jjdb__neuf))
    if isinstance(avozk__vqy, Exception):
        jqyyp__vic = avozk__vqy
        raise BodoError(
            f"""Error reading Iceberg Table: {type(jqyyp__vic).__name__}: {str(jqyyp__vic)}
"""
            )
    if isinstance(vbzhp__rmpv, Exception):
        jqyyp__vic = vbzhp__rmpv
        raise BodoError(
            f"""Error reading Iceberg Table: {type(jqyyp__vic).__name__}: {str(jqyyp__vic)}
"""
            )
    iooj__pqxc: List[str] = avozk__vqy
    snapshot_id: int = vbzhp__rmpv
    if len(iooj__pqxc) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(iooj__pqxc,
                get_row_counts=get_row_counts, expr_filters=expr_filters,
                is_parallel=is_parallel, typing_pa_schema=
                typing_pa_table_schema, partitioning=None, tot_rows_to_read
                =tot_rows_to_read)
        except BodoError as siwb__tfbc:
            if re.search('Schema .* was different', str(siwb__tfbc), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{siwb__tfbc}"""
                    )
            else:
                raise
    xaq__jeog = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, jjdb__neuf, snapshot_id, pq_dataset)
    if izhys__oxld:
        acpt__cjob.finalize()
    return xaq__jeog


def are_schemas_compatible(pa_schema: pa.Schema, df_schema: pa.Schema,
    allow_downcasting: bool=False) ->bool:
    if pa_schema.equals(df_schema):
        return True
    if len(df_schema) < len(pa_schema):
        krax__vflt = []
        for ouck__zgquf in pa_schema:
            mgego__ykfpc = df_schema.field_by_name(ouck__zgquf.name)
            if not (mgego__ykfpc is None and ouck__zgquf.nullable):
                krax__vflt.append(ouck__zgquf)
        pa_schema = pa.schema(krax__vflt)
    if len(pa_schema) != len(df_schema):
        return False
    for ctkh__dmhs in range(len(df_schema)):
        mgego__ykfpc = df_schema.field(ctkh__dmhs)
        ouck__zgquf = pa_schema.field(ctkh__dmhs)
        if mgego__ykfpc.equals(ouck__zgquf):
            continue
        zvsm__sbuqc = mgego__ykfpc.type
        zqqdn__squj = ouck__zgquf.type
        if not zvsm__sbuqc.equals(zqqdn__squj) and allow_downcasting and (
            pa.types.is_signed_integer(zvsm__sbuqc) and pa.types.
            is_signed_integer(zqqdn__squj) or pa.types.is_floating(
            zvsm__sbuqc) and pa.types.is_floating(zqqdn__squj)
            ) and zvsm__sbuqc.bit_width > zqqdn__squj.bit_width:
            mgego__ykfpc = mgego__ykfpc.with_type(zqqdn__squj)
        if not mgego__ykfpc.nullable and ouck__zgquf.nullable:
            mgego__ykfpc = mgego__ykfpc.with_nullable(True)
        elif allow_downcasting and mgego__ykfpc.nullable and not ouck__zgquf.nullable:
            mgego__ykfpc = mgego__ykfpc.with_nullable(False)
        df_schema = df_schema.set(ctkh__dmhs, mgego__ykfpc)
    return df_schema.equals(pa_schema)


def get_table_details_before_write(table_name: str, conn: str,
    database_schema: str, df_schema: pa.Schema, if_exists: str,
    allow_downcasting: bool=False):
    acpt__cjob = tracing.Event('iceberg_get_table_details_before_write')
    import bodo_iceberg_connector as connector
    mfdp__fto = MPI.COMM_WORLD
    pgw__smawt = None
    iceberg_schema_id = None
    table_loc = ''
    partition_spec = []
    sort_order = []
    iceberg_schema_str = ''
    pa_schema = None
    cpdt__qkl = {uiyp__nlyo: jibf__jgwde for jibf__jgwde, uiyp__nlyo in
        enumerate(df_schema.names)}
    if mfdp__fto.Get_rank() == 0:
        try:
            (table_loc, iceberg_schema_id, pa_schema, iceberg_schema_str,
                partition_spec, sort_order) = (connector.get_typing_info(
                conn, database_schema, table_name))
            for tqaxr__rqbe, *wwce__jtxf in partition_spec:
                assert tqaxr__rqbe in cpdt__qkl, f'Iceberg Partition column {tqaxr__rqbe} not found in dataframe'
            for tqaxr__rqbe, *wwce__jtxf in sort_order:
                assert tqaxr__rqbe in cpdt__qkl, f'Iceberg Sort column {tqaxr__rqbe} not found in dataframe'
            partition_spec = [(cpdt__qkl[tqaxr__rqbe], *skcig__nxwe) for 
                tqaxr__rqbe, *skcig__nxwe in partition_spec]
            sort_order = [(cpdt__qkl[tqaxr__rqbe], *skcig__nxwe) for 
                tqaxr__rqbe, *skcig__nxwe in sort_order]
            if if_exists == 'append' and pa_schema is not None:
                if not are_schemas_compatible(pa_schema, df_schema,
                    allow_downcasting):
                    if numba.core.config.DEVELOPER_MODE:
                        raise BodoError(
                            f"""DataFrame schema needs to be an ordered subset of Iceberg table for append

Iceberg:
{pa_schema}

DataFrame:
{df_schema}
"""
                            )
                    else:
                        raise BodoError(
                            'DataFrame schema needs to be an ordered subset of Iceberg table for append'
                            )
            if iceberg_schema_id is None:
                iceberg_schema_str = connector.pyarrow_to_iceberg_schema_str(
                    df_schema)
        except connector.IcebergError as siwb__tfbc:
            if isinstance(siwb__tfbc, connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                pgw__smawt = BodoError(
                    f'{siwb__tfbc.message}: {siwb__tfbc.java_error}')
            else:
                pgw__smawt = BodoError(siwb__tfbc.message)
        except Exception as siwb__tfbc:
            pgw__smawt = siwb__tfbc
    pgw__smawt = mfdp__fto.bcast(pgw__smawt)
    if isinstance(pgw__smawt, Exception):
        raise pgw__smawt
    table_loc = mfdp__fto.bcast(table_loc)
    iceberg_schema_id = mfdp__fto.bcast(iceberg_schema_id)
    partition_spec = mfdp__fto.bcast(partition_spec)
    sort_order = mfdp__fto.bcast(sort_order)
    iceberg_schema_str = mfdp__fto.bcast(iceberg_schema_str)
    pa_schema = mfdp__fto.bcast(pa_schema)
    if iceberg_schema_id is None:
        already_exists = False
        iceberg_schema_id = -1
    else:
        already_exists = True
    acpt__cjob.finalize()
    return (already_exists, table_loc, iceberg_schema_id, partition_spec,
        sort_order, iceberg_schema_str, pa_schema if if_exists == 'append' and
        pa_schema is not None else df_schema)


def collect_file_info(iceberg_files_info) ->Tuple[List[str], List[int],
    List[int]]:
    from mpi4py import MPI
    mfdp__fto = MPI.COMM_WORLD
    kwy__eeup = [rxj__rcrzt[0] for rxj__rcrzt in iceberg_files_info]
    tcec__hbud = mfdp__fto.gather(kwy__eeup)
    fnames = [rdwh__cua for ollc__uyr in tcec__hbud for rdwh__cua in ollc__uyr
        ] if mfdp__fto.Get_rank() == 0 else None
    ptt__akp = np.array([rxj__rcrzt[1] for rxj__rcrzt in iceberg_files_info
        ], dtype=np.int64)
    zjupv__egja = np.array([rxj__rcrzt[2] for rxj__rcrzt in
        iceberg_files_info], dtype=np.int64)
    icw__ygm = bodo.gatherv(ptt__akp).tolist()
    xfq__gtkb = bodo.gatherv(zjupv__egja).tolist()
    return fnames, icw__ygm, xfq__gtkb


def register_table_write(conn_str: str, db_name: str, table_name: str,
    table_loc: str, fnames: List[str], all_metrics: Dict[str, List[Any]],
    iceberg_schema_id: int, pa_schema, partition_spec, sort_order, mode: str):
    acpt__cjob = tracing.Event('iceberg_register_table_write')
    import bodo_iceberg_connector
    mfdp__fto = MPI.COMM_WORLD
    success = False
    if mfdp__fto.Get_rank() == 0:
        etj__gldvk = None if iceberg_schema_id < 0 else iceberg_schema_id
        success = bodo_iceberg_connector.commit_write(conn_str, db_name,
            table_name, table_loc, fnames, all_metrics, etj__gldvk,
            pa_schema, partition_spec, sort_order, mode)
    success = mfdp__fto.bcast(success)
    acpt__cjob.finalize()
    return success


def register_table_merge_cow(conn_str: str, db_name: str, table_name: str,
    table_loc: str, old_fnames: List[str], new_fnames: List[str],
    all_metrics: Dict[str, List[Any]], snapshot_id: int):
    acpt__cjob = tracing.Event('iceberg_register_table_merge_cow')
    import bodo_iceberg_connector
    mfdp__fto = MPI.COMM_WORLD
    success = False
    if mfdp__fto.Get_rank() == 0:
        success = bodo_iceberg_connector.commit_merge_cow(conn_str, db_name,
            table_name, table_loc, old_fnames, new_fnames, all_metrics,
            snapshot_id)
    success: bool = mfdp__fto.bcast(success)
    acpt__cjob.finalize()
    return success


from numba.extending import NativeValue, box, models, register_model, unbox


class PythonListOfHeterogeneousTuples(types.Opaque):

    def __init__(self):
        super(PythonListOfHeterogeneousTuples, self).__init__(name=
            'PythonListOfHeterogeneousTuples')


python_list_of_heterogeneous_tuples_type = PythonListOfHeterogeneousTuples()
types.python_list_of_heterogeneous_tuples_type = (
    python_list_of_heterogeneous_tuples_type)
register_model(PythonListOfHeterogeneousTuples)(models.OpaqueModel)


@unbox(PythonListOfHeterogeneousTuples)
def unbox_python_list_of_heterogeneous_tuples_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(PythonListOfHeterogeneousTuples)
def box_python_list_of_heterogeneous_tuples_type(typ, val, c):
    c.pyapi.incref(val)
    return val


this_module = sys.modules[__name__]
PyObjectOfList = install_py_obj_class(types_name='pyobject_of_list_type',
    python_type=None, module=this_module, class_name='PyObjectOfListType',
    model_name='PyObjectOfListModel')


@numba.njit()
def iceberg_pq_write(table_loc, bodo_table, col_names, partition_spec,
    sort_order, iceberg_schema_str, is_parallel, expected_schema):
    bucket_region = get_s3_bucket_region_njit(table_loc, is_parallel)
    dbby__ygxkn = 'snappy'
    ivi__rlf = -1
    iceberg_files_info = iceberg_pq_write_table_cpp(unicode_to_utf8(
        table_loc), bodo_table, col_names, partition_spec, sort_order,
        unicode_to_utf8(dbby__ygxkn), is_parallel, unicode_to_utf8(
        bucket_region), ivi__rlf, unicode_to_utf8(iceberg_schema_str),
        expected_schema)
    return iceberg_files_info


@numba.njit()
def iceberg_write(table_name, conn, database_schema, bodo_table, col_names,
    if_exists, is_parallel, df_pyarrow_schema, allow_downcasting=False):
    acpt__cjob = tracing.Event('iceberg_write_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        iceberg_schema_id='i8', partition_spec=
        'python_list_of_heterogeneous_tuples_type', sort_order=
        'python_list_of_heterogeneous_tuples_type', iceberg_schema_str=
        'unicode_type', expected_schema='pyarrow_table_schema_type'):
        (already_exists, table_loc, iceberg_schema_id, partition_spec,
            sort_order, iceberg_schema_str, expected_schema) = (
            get_table_details_before_write(table_name, conn,
            database_schema, df_pyarrow_schema, if_exists, allow_downcasting))
    if already_exists and if_exists == 'fail':
        raise ValueError(f'Table already exists.')
    if already_exists:
        mode = if_exists
    else:
        mode = 'create'
    iceberg_files_info = iceberg_pq_write(table_loc, bodo_table, col_names,
        partition_spec, sort_order, iceberg_schema_str, is_parallel,
        expected_schema)
    with numba.objmode(success='bool_'):
        fnames, icw__ygm, xfq__gtkb = collect_file_info(iceberg_files_info)
        success = register_table_write(conn, database_schema, table_name,
            table_loc, fnames, {'size': xfq__gtkb, 'record_count': icw__ygm
            }, iceberg_schema_id, df_pyarrow_schema, partition_spec,
            sort_order, mode)
    if not success:
        raise BodoError('Iceberg write failed.')
    acpt__cjob.finalize()


@numba.generated_jit(nopython=True)
def iceberg_merge_cow_py(table_name, conn, database_schema, bodo_df,
    snapshot_id, old_fnames, is_parallel=False):
    if not is_parallel:
        raise BodoError(
            'Merge Into with Iceberg Tables are only supported on distributed DataFrames'
            )
    df_pyarrow_schema = bodo.io.helpers.numba_to_pyarrow_schema(bodo_df,
        is_iceberg=True)
    qlzp__yfvgt = pd.array(bodo_df.columns)
    if bodo_df.is_table_format:
        slm__dtk = bodo_df.table_type

        def impl(table_name, conn, database_schema, bodo_df, snapshot_id,
            old_fnames, is_parallel=False):
            iceberg_merge_cow(table_name, format_iceberg_conn_njit(conn),
                database_schema, py_table_to_cpp_table(bodo.hiframes.
                pd_dataframe_ext.get_dataframe_table(bodo_df), slm__dtk),
                snapshot_id, old_fnames, array_to_info(qlzp__yfvgt),
                df_pyarrow_schema, is_parallel)
    else:
        zqxvj__htjn = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(bodo_df, {}))'
            .format(jibf__jgwde) for jibf__jgwde in range(len(bodo_df.columns))
            )
        sjarf__qaboe = 'def impl(\n'
        sjarf__qaboe += '    table_name,\n'
        sjarf__qaboe += '    conn,\n'
        sjarf__qaboe += '    database_schema,\n'
        sjarf__qaboe += '    bodo_df,\n'
        sjarf__qaboe += '    snapshot_id,\n'
        sjarf__qaboe += '    old_fnames,\n'
        sjarf__qaboe += '    is_parallel=False,\n'
        sjarf__qaboe += '):\n'
        sjarf__qaboe += '    info_list = [{}]\n'.format(zqxvj__htjn)
        sjarf__qaboe += '    table = arr_info_list_to_table(info_list)\n'
        sjarf__qaboe += '    iceberg_merge_cow(\n'
        sjarf__qaboe += '        table_name,\n'
        sjarf__qaboe += '        format_iceberg_conn_njit(conn),\n'
        sjarf__qaboe += '        database_schema,\n'
        sjarf__qaboe += '        table,\n'
        sjarf__qaboe += '        snapshot_id,\n'
        sjarf__qaboe += '        old_fnames,\n'
        sjarf__qaboe += '        array_to_info(col_names_py),\n'
        sjarf__qaboe += '        df_pyarrow_schema,\n'
        sjarf__qaboe += '        is_parallel,\n'
        sjarf__qaboe += '    )\n'
        locals = dict()
        globals = {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'iceberg_merge_cow': iceberg_merge_cow,
            'format_iceberg_conn_njit': format_iceberg_conn_njit,
            'col_names_py': qlzp__yfvgt, 'df_pyarrow_schema': df_pyarrow_schema
            }
        exec(sjarf__qaboe, globals, locals)
        impl = locals['impl']
    return impl


@numba.njit()
def iceberg_merge_cow(table_name, conn, database_schema, bodo_table,
    snapshot_id, old_fnames, col_names, df_pyarrow_schema, is_parallel):
    acpt__cjob = tracing.Event('iceberg_merge_cow_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        partition_spec='python_list_of_heterogeneous_tuples_type',
        sort_order='python_list_of_heterogeneous_tuples_type',
        iceberg_schema_str='unicode_type', expected_schema=
        'pyarrow_table_schema_type'):
        (already_exists, table_loc, wwce__jtxf, partition_spec, sort_order,
            iceberg_schema_str, expected_schema) = (
            get_table_details_before_write(table_name, conn,
            database_schema, df_pyarrow_schema, 'append', allow_downcasting
            =True))
    if not already_exists:
        raise ValueError(f'Iceberg MERGE INTO: Table does not exist at write')
    iceberg_files_info = iceberg_pq_write(table_loc, bodo_table, col_names,
        partition_spec, sort_order, iceberg_schema_str, is_parallel,
        expected_schema)
    with numba.objmode(success='bool_'):
        fnames, icw__ygm, xfq__gtkb = collect_file_info(iceberg_files_info)
        success = register_table_merge_cow(conn, database_schema,
            table_name, table_loc, old_fnames, fnames, {'size': xfq__gtkb,
            'record_count': icw__ygm}, snapshot_id)
    if not success:
        raise BodoError('Iceberg MERGE INTO: write failed')
    acpt__cjob.finalize()


import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('iceberg_pq_write', arrow_cpp.iceberg_pq_write)


@intrinsic
def iceberg_pq_write_table_cpp(typingctx, table_data_loc_t, table_t,
    col_names_t, partition_spec_t, sort_order_t, compression_t,
    is_parallel_t, bucket_region, row_group_size, iceberg_metadata_t,
    iceberg_schema_t):

    def codegen(context, builder, sig, args):
        gpu__gut = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        nrxf__khgb = cgutils.get_or_insert_function(builder.module,
            gpu__gut, name='iceberg_pq_write')
        ydb__fday = builder.call(nrxf__khgb, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return ydb__fday
    return types.python_list_of_heterogeneous_tuples_type(types.voidptr,
        table_t, col_names_t, python_list_of_heterogeneous_tuples_type,
        python_list_of_heterogeneous_tuples_type, types.voidptr, types.
        boolean, types.voidptr, types.int64, types.voidptr,
        pyarrow_table_schema_type), codegen
