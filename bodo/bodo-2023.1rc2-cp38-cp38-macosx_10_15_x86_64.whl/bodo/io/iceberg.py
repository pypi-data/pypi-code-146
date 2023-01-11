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
    ewolm__zfdj = urlparse(conn_str)
    if not conn_str.startswith('iceberg+glue') and ewolm__zfdj.scheme not in (
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
    dzg__ikfm = None
    jmc__cqjrj = None
    ooq__vmjq = None
    if bodo.get_rank() == 0:
        try:
            dzg__ikfm, jmc__cqjrj, ooq__vmjq = (bodo_iceberg_connector.
                get_iceberg_typing_schema(con, database_schema, table_name))
            if ooq__vmjq is None:
                raise BodoError('No such Iceberg table found')
        except bodo_iceberg_connector.IcebergError as ter__mug:
            if isinstance(ter__mug, bodo_iceberg_connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                dzg__ikfm = BodoError(
                    f'{ter__mug.message}: {ter__mug.java_error}')
            else:
                dzg__ikfm = BodoError(ter__mug.message)
    klh__zbkxl = MPI.COMM_WORLD
    dzg__ikfm = klh__zbkxl.bcast(dzg__ikfm)
    if isinstance(dzg__ikfm, Exception):
        raise dzg__ikfm
    col_names = dzg__ikfm
    jmc__cqjrj = klh__zbkxl.bcast(jmc__cqjrj)
    ooq__vmjq = klh__zbkxl.bcast(ooq__vmjq)
    eik__oilmc = [_get_numba_typ_from_pa_typ(typ, False, True, None)[0] for
        typ in jmc__cqjrj]
    if is_merge_into_cow:
        col_names.append('_bodo_row_id')
        eik__oilmc.append(types.Array(types.int64, 1, 'C'))
    return col_names, eik__oilmc, ooq__vmjq


def get_iceberg_file_list(table_name: str, conn: str, database_schema: str,
    filters) ->Tuple[List[str], List[str]]:
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_file_list should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        fzin__ngizx = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as ter__mug:
        if isinstance(ter__mug, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{ter__mug.message}:\n{ter__mug.java_error}')
        else:
            raise BodoError(ter__mug.message)
    return fzin__ngizx


def get_iceberg_snapshot_id(table_name: str, conn: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_snapshot_id should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        snapshot_id = (bodo_iceberg_connector.
            bodo_connector_get_current_snapshot_id(conn, database_schema,
            table_name))
    except bodo_iceberg_connector.IcebergError as ter__mug:
        if isinstance(ter__mug, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{ter__mug.message}:\n{ter__mug.java_error}')
        else:
            raise BodoError(ter__mug.message)
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
    fblkt__ilr = get_row_counts and tracing.is_tracing()
    if fblkt__ilr:
        fhyyh__lsqpm = tracing.Event('get_iceberg_pq_dataset')
    klh__zbkxl = MPI.COMM_WORLD
    mlgj__vqt = None
    yneow__fjpmu = None
    oiwb__uwi = None
    if bodo.get_rank() == 0:
        if fblkt__ilr:
            msuc__mdczo = tracing.Event('get_iceberg_file_list',
                is_parallel=False)
            msuc__mdczo.add_attribute('g_dnf_filter', str(dnf_filters))
        try:
            mlgj__vqt, oiwb__uwi = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if fblkt__ilr:
                dqr__sbotm = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                msuc__mdczo.add_attribute('num_files', len(mlgj__vqt))
                msuc__mdczo.add_attribute(f'first_{dqr__sbotm}_files', ', '
                    .join(mlgj__vqt[:dqr__sbotm]))
        except Exception as ter__mug:
            mlgj__vqt = ter__mug
        if fblkt__ilr:
            msuc__mdczo.finalize()
            wdxqe__kcx = tracing.Event('get_snapshot_id', is_parallel=False)
        try:
            yneow__fjpmu = get_iceberg_snapshot_id(table_name, conn,
                database_schema)
        except Exception as ter__mug:
            yneow__fjpmu = ter__mug
        if fblkt__ilr:
            wdxqe__kcx.finalize()
    mlgj__vqt, yneow__fjpmu, oiwb__uwi = klh__zbkxl.bcast((mlgj__vqt,
        yneow__fjpmu, oiwb__uwi))
    if isinstance(mlgj__vqt, Exception):
        yda__xyri = mlgj__vqt
        raise BodoError(
            f"""Error reading Iceberg Table: {type(yda__xyri).__name__}: {str(yda__xyri)}
"""
            )
    if isinstance(yneow__fjpmu, Exception):
        yda__xyri = yneow__fjpmu
        raise BodoError(
            f"""Error reading Iceberg Table: {type(yda__xyri).__name__}: {str(yda__xyri)}
"""
            )
    bkei__gpshq: List[str] = mlgj__vqt
    snapshot_id: int = yneow__fjpmu
    if len(bkei__gpshq) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(bkei__gpshq,
                get_row_counts=get_row_counts, expr_filters=expr_filters,
                is_parallel=is_parallel, typing_pa_schema=
                typing_pa_table_schema, partitioning=None, tot_rows_to_read
                =tot_rows_to_read)
        except BodoError as ter__mug:
            if re.search('Schema .* was different', str(ter__mug), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{ter__mug}"""
                    )
            else:
                raise
    txh__zwq = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, oiwb__uwi, snapshot_id, pq_dataset)
    if fblkt__ilr:
        fhyyh__lsqpm.finalize()
    return txh__zwq


def are_schemas_compatible(pa_schema: pa.Schema, df_schema: pa.Schema,
    allow_downcasting: bool=False) ->bool:
    if pa_schema.equals(df_schema):
        return True
    if len(df_schema) < len(pa_schema):
        vxgu__fut = []
        for wizz__kzq in pa_schema:
            vuf__hjcov = df_schema.field_by_name(wizz__kzq.name)
            if not (vuf__hjcov is None and wizz__kzq.nullable):
                vxgu__fut.append(wizz__kzq)
        pa_schema = pa.schema(vxgu__fut)
    if len(pa_schema) != len(df_schema):
        return False
    for dcm__nut in range(len(df_schema)):
        vuf__hjcov = df_schema.field(dcm__nut)
        wizz__kzq = pa_schema.field(dcm__nut)
        if vuf__hjcov.equals(wizz__kzq):
            continue
        hmov__koyj = vuf__hjcov.type
        tjw__oflj = wizz__kzq.type
        if not hmov__koyj.equals(tjw__oflj) and allow_downcasting and (pa.
            types.is_signed_integer(hmov__koyj) and pa.types.
            is_signed_integer(tjw__oflj) or pa.types.is_floating(hmov__koyj
            ) and pa.types.is_floating(tjw__oflj)
            ) and hmov__koyj.bit_width > tjw__oflj.bit_width:
            vuf__hjcov = vuf__hjcov.with_type(tjw__oflj)
        if not vuf__hjcov.nullable and wizz__kzq.nullable:
            vuf__hjcov = vuf__hjcov.with_nullable(True)
        elif allow_downcasting and vuf__hjcov.nullable and not wizz__kzq.nullable:
            vuf__hjcov = vuf__hjcov.with_nullable(False)
        df_schema = df_schema.set(dcm__nut, vuf__hjcov)
    return df_schema.equals(pa_schema)


def get_table_details_before_write(table_name: str, conn: str,
    database_schema: str, df_schema: pa.Schema, if_exists: str,
    allow_downcasting: bool=False):
    fhyyh__lsqpm = tracing.Event('iceberg_get_table_details_before_write')
    import bodo_iceberg_connector as connector
    klh__zbkxl = MPI.COMM_WORLD
    mqz__fldhd = None
    iceberg_schema_id = None
    table_loc = ''
    partition_spec = []
    sort_order = []
    iceberg_schema_str = ''
    pa_schema = None
    tmp__datpe = {svkzm__woay: lutzt__pfns for lutzt__pfns, svkzm__woay in
        enumerate(df_schema.names)}
    if klh__zbkxl.Get_rank() == 0:
        try:
            (table_loc, iceberg_schema_id, pa_schema, iceberg_schema_str,
                partition_spec, sort_order) = (connector.get_typing_info(
                conn, database_schema, table_name))
            for dcel__qqp, *eqw__lmtx in partition_spec:
                assert dcel__qqp in tmp__datpe, f'Iceberg Partition column {dcel__qqp} not found in dataframe'
            for dcel__qqp, *eqw__lmtx in sort_order:
                assert dcel__qqp in tmp__datpe, f'Iceberg Sort column {dcel__qqp} not found in dataframe'
            partition_spec = [(tmp__datpe[dcel__qqp], *syr__unndw) for 
                dcel__qqp, *syr__unndw in partition_spec]
            sort_order = [(tmp__datpe[dcel__qqp], *syr__unndw) for 
                dcel__qqp, *syr__unndw in sort_order]
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
        except connector.IcebergError as ter__mug:
            if isinstance(ter__mug, connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                mqz__fldhd = BodoError(
                    f'{ter__mug.message}: {ter__mug.java_error}')
            else:
                mqz__fldhd = BodoError(ter__mug.message)
        except Exception as ter__mug:
            mqz__fldhd = ter__mug
    mqz__fldhd = klh__zbkxl.bcast(mqz__fldhd)
    if isinstance(mqz__fldhd, Exception):
        raise mqz__fldhd
    table_loc = klh__zbkxl.bcast(table_loc)
    iceberg_schema_id = klh__zbkxl.bcast(iceberg_schema_id)
    partition_spec = klh__zbkxl.bcast(partition_spec)
    sort_order = klh__zbkxl.bcast(sort_order)
    iceberg_schema_str = klh__zbkxl.bcast(iceberg_schema_str)
    pa_schema = klh__zbkxl.bcast(pa_schema)
    if iceberg_schema_id is None:
        already_exists = False
        iceberg_schema_id = -1
    else:
        already_exists = True
    fhyyh__lsqpm.finalize()
    return (already_exists, table_loc, iceberg_schema_id, partition_spec,
        sort_order, iceberg_schema_str, pa_schema if if_exists == 'append' and
        pa_schema is not None else df_schema)


def collect_file_info(iceberg_files_info) ->Tuple[List[str], List[int],
    List[int]]:
    from mpi4py import MPI
    klh__zbkxl = MPI.COMM_WORLD
    uqfvb__yeweq = [cni__bclu[0] for cni__bclu in iceberg_files_info]
    dpvva__gyl = klh__zbkxl.gather(uqfvb__yeweq)
    fnames = [kuq__dmyl for jzvk__phddf in dpvva__gyl for kuq__dmyl in
        jzvk__phddf] if klh__zbkxl.Get_rank() == 0 else None
    hpl__xdmrh = np.array([cni__bclu[1] for cni__bclu in iceberg_files_info
        ], dtype=np.int64)
    qgbza__gwr = np.array([cni__bclu[2] for cni__bclu in iceberg_files_info
        ], dtype=np.int64)
    pihq__eqav = bodo.gatherv(hpl__xdmrh).tolist()
    kwetg__ctvot = bodo.gatherv(qgbza__gwr).tolist()
    return fnames, pihq__eqav, kwetg__ctvot


def register_table_write(conn_str: str, db_name: str, table_name: str,
    table_loc: str, fnames: List[str], all_metrics: Dict[str, List[Any]],
    iceberg_schema_id: int, pa_schema, partition_spec, sort_order, mode: str):
    fhyyh__lsqpm = tracing.Event('iceberg_register_table_write')
    import bodo_iceberg_connector
    klh__zbkxl = MPI.COMM_WORLD
    success = False
    if klh__zbkxl.Get_rank() == 0:
        uejyf__hkl = None if iceberg_schema_id < 0 else iceberg_schema_id
        success = bodo_iceberg_connector.commit_write(conn_str, db_name,
            table_name, table_loc, fnames, all_metrics, uejyf__hkl,
            pa_schema, partition_spec, sort_order, mode)
    success = klh__zbkxl.bcast(success)
    fhyyh__lsqpm.finalize()
    return success


def register_table_merge_cow(conn_str: str, db_name: str, table_name: str,
    table_loc: str, old_fnames: List[str], new_fnames: List[str],
    all_metrics: Dict[str, List[Any]], snapshot_id: int):
    fhyyh__lsqpm = tracing.Event('iceberg_register_table_merge_cow')
    import bodo_iceberg_connector
    klh__zbkxl = MPI.COMM_WORLD
    success = False
    if klh__zbkxl.Get_rank() == 0:
        success = bodo_iceberg_connector.commit_merge_cow(conn_str, db_name,
            table_name, table_loc, old_fnames, new_fnames, all_metrics,
            snapshot_id)
    success: bool = klh__zbkxl.bcast(success)
    fhyyh__lsqpm.finalize()
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
    psonz__qftwh = 'snappy'
    qheg__vxyb = -1
    iceberg_files_info = iceberg_pq_write_table_cpp(unicode_to_utf8(
        table_loc), bodo_table, col_names, partition_spec, sort_order,
        unicode_to_utf8(psonz__qftwh), is_parallel, unicode_to_utf8(
        bucket_region), qheg__vxyb, unicode_to_utf8(iceberg_schema_str),
        expected_schema)
    return iceberg_files_info


@numba.njit()
def iceberg_write(table_name, conn, database_schema, bodo_table, col_names,
    if_exists, is_parallel, df_pyarrow_schema, allow_downcasting=False):
    fhyyh__lsqpm = tracing.Event('iceberg_write_py', is_parallel)
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
        fnames, pihq__eqav, kwetg__ctvot = collect_file_info(iceberg_files_info
            )
        success = register_table_write(conn, database_schema, table_name,
            table_loc, fnames, {'size': kwetg__ctvot, 'record_count':
            pihq__eqav}, iceberg_schema_id, df_pyarrow_schema,
            partition_spec, sort_order, mode)
    if not success:
        raise BodoError('Iceberg write failed.')
    fhyyh__lsqpm.finalize()


@numba.generated_jit(nopython=True)
def iceberg_merge_cow_py(table_name, conn, database_schema, bodo_df,
    snapshot_id, old_fnames, is_parallel=False):
    if not is_parallel:
        raise BodoError(
            'Merge Into with Iceberg Tables are only supported on distributed DataFrames'
            )
    df_pyarrow_schema = bodo.io.helpers.numba_to_pyarrow_schema(bodo_df,
        is_iceberg=True)
    lxq__pinw = pd.array(bodo_df.columns)
    if bodo_df.is_table_format:
        qxreg__smhes = bodo_df.table_type

        def impl(table_name, conn, database_schema, bodo_df, snapshot_id,
            old_fnames, is_parallel=False):
            iceberg_merge_cow(table_name, format_iceberg_conn_njit(conn),
                database_schema, py_table_to_cpp_table(bodo.hiframes.
                pd_dataframe_ext.get_dataframe_table(bodo_df), qxreg__smhes
                ), snapshot_id, old_fnames, array_to_info(lxq__pinw),
                df_pyarrow_schema, is_parallel)
    else:
        lii__kbnh = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(bodo_df, {}))'
            .format(lutzt__pfns) for lutzt__pfns in range(len(bodo_df.columns))
            )
        lsouc__xdvim = 'def impl(\n'
        lsouc__xdvim += '    table_name,\n'
        lsouc__xdvim += '    conn,\n'
        lsouc__xdvim += '    database_schema,\n'
        lsouc__xdvim += '    bodo_df,\n'
        lsouc__xdvim += '    snapshot_id,\n'
        lsouc__xdvim += '    old_fnames,\n'
        lsouc__xdvim += '    is_parallel=False,\n'
        lsouc__xdvim += '):\n'
        lsouc__xdvim += '    info_list = [{}]\n'.format(lii__kbnh)
        lsouc__xdvim += '    table = arr_info_list_to_table(info_list)\n'
        lsouc__xdvim += '    iceberg_merge_cow(\n'
        lsouc__xdvim += '        table_name,\n'
        lsouc__xdvim += '        format_iceberg_conn_njit(conn),\n'
        lsouc__xdvim += '        database_schema,\n'
        lsouc__xdvim += '        table,\n'
        lsouc__xdvim += '        snapshot_id,\n'
        lsouc__xdvim += '        old_fnames,\n'
        lsouc__xdvim += '        array_to_info(col_names_py),\n'
        lsouc__xdvim += '        df_pyarrow_schema,\n'
        lsouc__xdvim += '        is_parallel,\n'
        lsouc__xdvim += '    )\n'
        locals = dict()
        globals = {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'iceberg_merge_cow': iceberg_merge_cow,
            'format_iceberg_conn_njit': format_iceberg_conn_njit,
            'col_names_py': lxq__pinw, 'df_pyarrow_schema': df_pyarrow_schema}
        exec(lsouc__xdvim, globals, locals)
        impl = locals['impl']
    return impl


@numba.njit()
def iceberg_merge_cow(table_name, conn, database_schema, bodo_table,
    snapshot_id, old_fnames, col_names, df_pyarrow_schema, is_parallel):
    fhyyh__lsqpm = tracing.Event('iceberg_merge_cow_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        partition_spec='python_list_of_heterogeneous_tuples_type',
        sort_order='python_list_of_heterogeneous_tuples_type',
        iceberg_schema_str='unicode_type', expected_schema=
        'pyarrow_table_schema_type'):
        (already_exists, table_loc, eqw__lmtx, partition_spec, sort_order,
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
        fnames, pihq__eqav, kwetg__ctvot = collect_file_info(iceberg_files_info
            )
        success = register_table_merge_cow(conn, database_schema,
            table_name, table_loc, old_fnames, fnames, {'size':
            kwetg__ctvot, 'record_count': pihq__eqav}, snapshot_id)
    if not success:
        raise BodoError('Iceberg MERGE INTO: write failed')
    fhyyh__lsqpm.finalize()


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
        hxg__arjm = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        sggro__lqzcz = cgutils.get_or_insert_function(builder.module,
            hxg__arjm, name='iceberg_pq_write')
        cbzpl__ktkn = builder.call(sggro__lqzcz, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return cbzpl__ktkn
    return types.python_list_of_heterogeneous_tuples_type(types.voidptr,
        table_t, col_names_t, python_list_of_heterogeneous_tuples_type,
        python_list_of_heterogeneous_tuples_type, types.voidptr, types.
        boolean, types.voidptr, types.int64, types.voidptr,
        pyarrow_table_schema_type), codegen
