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
    xhcu__davd = urlparse(conn_str)
    if not conn_str.startswith('iceberg+glue') and xhcu__davd.scheme not in (
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
    boj__qcdyb = None
    uzajd__jslf = None
    zbf__ewgd = None
    if bodo.get_rank() == 0:
        try:
            boj__qcdyb, uzajd__jslf, zbf__ewgd = (bodo_iceberg_connector.
                get_iceberg_typing_schema(con, database_schema, table_name))
            if zbf__ewgd is None:
                raise BodoError('No such Iceberg table found')
        except bodo_iceberg_connector.IcebergError as hhbu__adrcl:
            if isinstance(hhbu__adrcl, bodo_iceberg_connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                boj__qcdyb = BodoError(
                    f'{hhbu__adrcl.message}: {hhbu__adrcl.java_error}')
            else:
                boj__qcdyb = BodoError(hhbu__adrcl.message)
    asqx__zcn = MPI.COMM_WORLD
    boj__qcdyb = asqx__zcn.bcast(boj__qcdyb)
    if isinstance(boj__qcdyb, Exception):
        raise boj__qcdyb
    col_names = boj__qcdyb
    uzajd__jslf = asqx__zcn.bcast(uzajd__jslf)
    zbf__ewgd = asqx__zcn.bcast(zbf__ewgd)
    hzuxh__bvdu = [_get_numba_typ_from_pa_typ(typ, False, True, None)[0] for
        typ in uzajd__jslf]
    if is_merge_into_cow:
        col_names.append('_bodo_row_id')
        hzuxh__bvdu.append(types.Array(types.int64, 1, 'C'))
    return col_names, hzuxh__bvdu, zbf__ewgd


def get_iceberg_file_list(table_name: str, conn: str, database_schema: str,
    filters) ->Tuple[List[str], List[str]]:
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_file_list should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        rybwq__wrkp = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as hhbu__adrcl:
        if isinstance(hhbu__adrcl, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{hhbu__adrcl.message}:\n{hhbu__adrcl.java_error}'
                )
        else:
            raise BodoError(hhbu__adrcl.message)
    return rybwq__wrkp


def get_iceberg_snapshot_id(table_name: str, conn: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_snapshot_id should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        snapshot_id = (bodo_iceberg_connector.
            bodo_connector_get_current_snapshot_id(conn, database_schema,
            table_name))
    except bodo_iceberg_connector.IcebergError as hhbu__adrcl:
        if isinstance(hhbu__adrcl, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{hhbu__adrcl.message}:\n{hhbu__adrcl.java_error}'
                )
        else:
            raise BodoError(hhbu__adrcl.message)
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
    qntrt__lfv = get_row_counts and tracing.is_tracing()
    if qntrt__lfv:
        pawtl__zmtgo = tracing.Event('get_iceberg_pq_dataset')
    asqx__zcn = MPI.COMM_WORLD
    suqf__kwnai = None
    kwg__ckik = None
    crjw__ccjl = None
    if bodo.get_rank() == 0:
        if qntrt__lfv:
            echj__opx = tracing.Event('get_iceberg_file_list', is_parallel=
                False)
            echj__opx.add_attribute('g_dnf_filter', str(dnf_filters))
        try:
            suqf__kwnai, crjw__ccjl = get_iceberg_file_list(table_name,
                conn, database_schema, dnf_filters)
            if qntrt__lfv:
                suld__mhvsz = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                echj__opx.add_attribute('num_files', len(suqf__kwnai))
                echj__opx.add_attribute(f'first_{suld__mhvsz}_files', ', '.
                    join(suqf__kwnai[:suld__mhvsz]))
        except Exception as hhbu__adrcl:
            suqf__kwnai = hhbu__adrcl
        if qntrt__lfv:
            echj__opx.finalize()
            loia__chc = tracing.Event('get_snapshot_id', is_parallel=False)
        try:
            kwg__ckik = get_iceberg_snapshot_id(table_name, conn,
                database_schema)
        except Exception as hhbu__adrcl:
            kwg__ckik = hhbu__adrcl
        if qntrt__lfv:
            loia__chc.finalize()
    suqf__kwnai, kwg__ckik, crjw__ccjl = asqx__zcn.bcast((suqf__kwnai,
        kwg__ckik, crjw__ccjl))
    if isinstance(suqf__kwnai, Exception):
        dkd__pyigw = suqf__kwnai
        raise BodoError(
            f"""Error reading Iceberg Table: {type(dkd__pyigw).__name__}: {str(dkd__pyigw)}
"""
            )
    if isinstance(kwg__ckik, Exception):
        dkd__pyigw = kwg__ckik
        raise BodoError(
            f"""Error reading Iceberg Table: {type(dkd__pyigw).__name__}: {str(dkd__pyigw)}
"""
            )
    loea__dzx: List[str] = suqf__kwnai
    snapshot_id: int = kwg__ckik
    if len(loea__dzx) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(loea__dzx,
                get_row_counts=get_row_counts, expr_filters=expr_filters,
                is_parallel=is_parallel, typing_pa_schema=
                typing_pa_table_schema, partitioning=None, tot_rows_to_read
                =tot_rows_to_read)
        except BodoError as hhbu__adrcl:
            if re.search('Schema .* was different', str(hhbu__adrcl), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{hhbu__adrcl}"""
                    )
            else:
                raise
    npybx__htps = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, crjw__ccjl, snapshot_id, pq_dataset)
    if qntrt__lfv:
        pawtl__zmtgo.finalize()
    return npybx__htps


def are_schemas_compatible(pa_schema: pa.Schema, df_schema: pa.Schema,
    allow_downcasting: bool=False) ->bool:
    if pa_schema.equals(df_schema):
        return True
    if len(df_schema) < len(pa_schema):
        draiv__rjfkd = []
        for yztzu__isab in pa_schema:
            xtqrq__plofv = df_schema.field_by_name(yztzu__isab.name)
            if not (xtqrq__plofv is None and yztzu__isab.nullable):
                draiv__rjfkd.append(yztzu__isab)
        pa_schema = pa.schema(draiv__rjfkd)
    if len(pa_schema) != len(df_schema):
        return False
    for gij__jpytj in range(len(df_schema)):
        xtqrq__plofv = df_schema.field(gij__jpytj)
        yztzu__isab = pa_schema.field(gij__jpytj)
        if xtqrq__plofv.equals(yztzu__isab):
            continue
        mpbtw__bxgcm = xtqrq__plofv.type
        mbjdf__bjvg = yztzu__isab.type
        if not mpbtw__bxgcm.equals(mbjdf__bjvg) and allow_downcasting and (
            pa.types.is_signed_integer(mpbtw__bxgcm) and pa.types.
            is_signed_integer(mbjdf__bjvg) or pa.types.is_floating(
            mpbtw__bxgcm) and pa.types.is_floating(mbjdf__bjvg)
            ) and mpbtw__bxgcm.bit_width > mbjdf__bjvg.bit_width:
            xtqrq__plofv = xtqrq__plofv.with_type(mbjdf__bjvg)
        if not xtqrq__plofv.nullable and yztzu__isab.nullable:
            xtqrq__plofv = xtqrq__plofv.with_nullable(True)
        elif allow_downcasting and xtqrq__plofv.nullable and not yztzu__isab.nullable:
            xtqrq__plofv = xtqrq__plofv.with_nullable(False)
        df_schema = df_schema.set(gij__jpytj, xtqrq__plofv)
    return df_schema.equals(pa_schema)


def get_table_details_before_write(table_name: str, conn: str,
    database_schema: str, df_schema: pa.Schema, if_exists: str,
    allow_downcasting: bool=False):
    pawtl__zmtgo = tracing.Event('iceberg_get_table_details_before_write')
    import bodo_iceberg_connector as connector
    asqx__zcn = MPI.COMM_WORLD
    pxmk__ctchg = None
    iceberg_schema_id = None
    table_loc = ''
    partition_spec = []
    sort_order = []
    iceberg_schema_str = ''
    pa_schema = None
    gluxv__yupaa = {tez__gbjp: uiu__orq for uiu__orq, tez__gbjp in
        enumerate(df_schema.names)}
    if asqx__zcn.Get_rank() == 0:
        try:
            (table_loc, iceberg_schema_id, pa_schema, iceberg_schema_str,
                partition_spec, sort_order) = (connector.get_typing_info(
                conn, database_schema, table_name))
            for uaujh__ifred, *jkmhr__yodtc in partition_spec:
                assert uaujh__ifred in gluxv__yupaa, f'Iceberg Partition column {uaujh__ifred} not found in dataframe'
            for uaujh__ifred, *jkmhr__yodtc in sort_order:
                assert uaujh__ifred in gluxv__yupaa, f'Iceberg Sort column {uaujh__ifred} not found in dataframe'
            partition_spec = [(gluxv__yupaa[uaujh__ifred], *jjc__zdpqa) for
                uaujh__ifred, *jjc__zdpqa in partition_spec]
            sort_order = [(gluxv__yupaa[uaujh__ifred], *jjc__zdpqa) for 
                uaujh__ifred, *jjc__zdpqa in sort_order]
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
        except connector.IcebergError as hhbu__adrcl:
            if isinstance(hhbu__adrcl, connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                pxmk__ctchg = BodoError(
                    f'{hhbu__adrcl.message}: {hhbu__adrcl.java_error}')
            else:
                pxmk__ctchg = BodoError(hhbu__adrcl.message)
        except Exception as hhbu__adrcl:
            pxmk__ctchg = hhbu__adrcl
    pxmk__ctchg = asqx__zcn.bcast(pxmk__ctchg)
    if isinstance(pxmk__ctchg, Exception):
        raise pxmk__ctchg
    table_loc = asqx__zcn.bcast(table_loc)
    iceberg_schema_id = asqx__zcn.bcast(iceberg_schema_id)
    partition_spec = asqx__zcn.bcast(partition_spec)
    sort_order = asqx__zcn.bcast(sort_order)
    iceberg_schema_str = asqx__zcn.bcast(iceberg_schema_str)
    pa_schema = asqx__zcn.bcast(pa_schema)
    if iceberg_schema_id is None:
        already_exists = False
        iceberg_schema_id = -1
    else:
        already_exists = True
    pawtl__zmtgo.finalize()
    return (already_exists, table_loc, iceberg_schema_id, partition_spec,
        sort_order, iceberg_schema_str, pa_schema if if_exists == 'append' and
        pa_schema is not None else df_schema)


def collect_file_info(iceberg_files_info) ->Tuple[List[str], List[int],
    List[int]]:
    from mpi4py import MPI
    asqx__zcn = MPI.COMM_WORLD
    uvt__fjty = [wgf__firp[0] for wgf__firp in iceberg_files_info]
    ghu__xsms = asqx__zcn.gather(uvt__fjty)
    fnames = [bnk__wcjvo for ctqbc__pifd in ghu__xsms for bnk__wcjvo in
        ctqbc__pifd] if asqx__zcn.Get_rank() == 0 else None
    lso__ibq = np.array([wgf__firp[1] for wgf__firp in iceberg_files_info],
        dtype=np.int64)
    sucr__qvpi = np.array([wgf__firp[2] for wgf__firp in iceberg_files_info
        ], dtype=np.int64)
    vvl__dmezy = bodo.gatherv(lso__ibq).tolist()
    hnp__hna = bodo.gatherv(sucr__qvpi).tolist()
    return fnames, vvl__dmezy, hnp__hna


def register_table_write(conn_str: str, db_name: str, table_name: str,
    table_loc: str, fnames: List[str], all_metrics: Dict[str, List[Any]],
    iceberg_schema_id: int, pa_schema, partition_spec, sort_order, mode: str):
    pawtl__zmtgo = tracing.Event('iceberg_register_table_write')
    import bodo_iceberg_connector
    asqx__zcn = MPI.COMM_WORLD
    success = False
    if asqx__zcn.Get_rank() == 0:
        mwza__xydbh = None if iceberg_schema_id < 0 else iceberg_schema_id
        success = bodo_iceberg_connector.commit_write(conn_str, db_name,
            table_name, table_loc, fnames, all_metrics, mwza__xydbh,
            pa_schema, partition_spec, sort_order, mode)
    success = asqx__zcn.bcast(success)
    pawtl__zmtgo.finalize()
    return success


def register_table_merge_cow(conn_str: str, db_name: str, table_name: str,
    table_loc: str, old_fnames: List[str], new_fnames: List[str],
    all_metrics: Dict[str, List[Any]], snapshot_id: int):
    pawtl__zmtgo = tracing.Event('iceberg_register_table_merge_cow')
    import bodo_iceberg_connector
    asqx__zcn = MPI.COMM_WORLD
    success = False
    if asqx__zcn.Get_rank() == 0:
        success = bodo_iceberg_connector.commit_merge_cow(conn_str, db_name,
            table_name, table_loc, old_fnames, new_fnames, all_metrics,
            snapshot_id)
    success: bool = asqx__zcn.bcast(success)
    pawtl__zmtgo.finalize()
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
    gzvf__lzf = 'snappy'
    znt__gjcbv = -1
    iceberg_files_info = iceberg_pq_write_table_cpp(unicode_to_utf8(
        table_loc), bodo_table, col_names, partition_spec, sort_order,
        unicode_to_utf8(gzvf__lzf), is_parallel, unicode_to_utf8(
        bucket_region), znt__gjcbv, unicode_to_utf8(iceberg_schema_str),
        expected_schema)
    return iceberg_files_info


@numba.njit()
def iceberg_write(table_name, conn, database_schema, bodo_table, col_names,
    if_exists, is_parallel, df_pyarrow_schema, allow_downcasting=False):
    pawtl__zmtgo = tracing.Event('iceberg_write_py', is_parallel)
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
        fnames, vvl__dmezy, hnp__hna = collect_file_info(iceberg_files_info)
        success = register_table_write(conn, database_schema, table_name,
            table_loc, fnames, {'size': hnp__hna, 'record_count':
            vvl__dmezy}, iceberg_schema_id, df_pyarrow_schema,
            partition_spec, sort_order, mode)
    if not success:
        raise BodoError('Iceberg write failed.')
    pawtl__zmtgo.finalize()


@numba.generated_jit(nopython=True)
def iceberg_merge_cow_py(table_name, conn, database_schema, bodo_df,
    snapshot_id, old_fnames, is_parallel=False):
    if not is_parallel:
        raise BodoError(
            'Merge Into with Iceberg Tables are only supported on distributed DataFrames'
            )
    df_pyarrow_schema = bodo.io.helpers.numba_to_pyarrow_schema(bodo_df,
        is_iceberg=True)
    xmdfw__tmlj = pd.array(bodo_df.columns)
    if bodo_df.is_table_format:
        cnvu__pcf = bodo_df.table_type

        def impl(table_name, conn, database_schema, bodo_df, snapshot_id,
            old_fnames, is_parallel=False):
            iceberg_merge_cow(table_name, format_iceberg_conn_njit(conn),
                database_schema, py_table_to_cpp_table(bodo.hiframes.
                pd_dataframe_ext.get_dataframe_table(bodo_df), cnvu__pcf),
                snapshot_id, old_fnames, array_to_info(xmdfw__tmlj),
                df_pyarrow_schema, is_parallel)
    else:
        hbc__pxgqx = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(bodo_df, {}))'
            .format(uiu__orq) for uiu__orq in range(len(bodo_df.columns)))
        nfnkt__atke = 'def impl(\n'
        nfnkt__atke += '    table_name,\n'
        nfnkt__atke += '    conn,\n'
        nfnkt__atke += '    database_schema,\n'
        nfnkt__atke += '    bodo_df,\n'
        nfnkt__atke += '    snapshot_id,\n'
        nfnkt__atke += '    old_fnames,\n'
        nfnkt__atke += '    is_parallel=False,\n'
        nfnkt__atke += '):\n'
        nfnkt__atke += '    info_list = [{}]\n'.format(hbc__pxgqx)
        nfnkt__atke += '    table = arr_info_list_to_table(info_list)\n'
        nfnkt__atke += '    iceberg_merge_cow(\n'
        nfnkt__atke += '        table_name,\n'
        nfnkt__atke += '        format_iceberg_conn_njit(conn),\n'
        nfnkt__atke += '        database_schema,\n'
        nfnkt__atke += '        table,\n'
        nfnkt__atke += '        snapshot_id,\n'
        nfnkt__atke += '        old_fnames,\n'
        nfnkt__atke += '        array_to_info(col_names_py),\n'
        nfnkt__atke += '        df_pyarrow_schema,\n'
        nfnkt__atke += '        is_parallel,\n'
        nfnkt__atke += '    )\n'
        locals = dict()
        globals = {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'iceberg_merge_cow': iceberg_merge_cow,
            'format_iceberg_conn_njit': format_iceberg_conn_njit,
            'col_names_py': xmdfw__tmlj, 'df_pyarrow_schema': df_pyarrow_schema
            }
        exec(nfnkt__atke, globals, locals)
        impl = locals['impl']
    return impl


@numba.njit()
def iceberg_merge_cow(table_name, conn, database_schema, bodo_table,
    snapshot_id, old_fnames, col_names, df_pyarrow_schema, is_parallel):
    pawtl__zmtgo = tracing.Event('iceberg_merge_cow_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        partition_spec='python_list_of_heterogeneous_tuples_type',
        sort_order='python_list_of_heterogeneous_tuples_type',
        iceberg_schema_str='unicode_type', expected_schema=
        'pyarrow_table_schema_type'):
        (already_exists, table_loc, jkmhr__yodtc, partition_spec,
            sort_order, iceberg_schema_str, expected_schema) = (
            get_table_details_before_write(table_name, conn,
            database_schema, df_pyarrow_schema, 'append', allow_downcasting
            =True))
    if not already_exists:
        raise ValueError(f'Iceberg MERGE INTO: Table does not exist at write')
    iceberg_files_info = iceberg_pq_write(table_loc, bodo_table, col_names,
        partition_spec, sort_order, iceberg_schema_str, is_parallel,
        expected_schema)
    with numba.objmode(success='bool_'):
        fnames, vvl__dmezy, hnp__hna = collect_file_info(iceberg_files_info)
        success = register_table_merge_cow(conn, database_schema,
            table_name, table_loc, old_fnames, fnames, {'size': hnp__hna,
            'record_count': vvl__dmezy}, snapshot_id)
    if not success:
        raise BodoError('Iceberg MERGE INTO: write failed')
    pawtl__zmtgo.finalize()


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
        sqovh__bkp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        syfv__mjxv = cgutils.get_or_insert_function(builder.module,
            sqovh__bkp, name='iceberg_pq_write')
        lono__ksj = builder.call(syfv__mjxv, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return lono__ksj
    return types.python_list_of_heterogeneous_tuples_type(types.voidptr,
        table_t, col_names_t, python_list_of_heterogeneous_tuples_type,
        python_list_of_heterogeneous_tuples_type, types.voidptr, types.
        boolean, types.voidptr, types.int64, types.voidptr,
        pyarrow_table_schema_type), codegen
