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
    jnhrl__qrdgk = urlparse(conn_str)
    if not conn_str.startswith('iceberg+glue') and jnhrl__qrdgk.scheme not in (
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
    dpek__occ = None
    akzvq__nwdn = None
    hru__ideo = None
    if bodo.get_rank() == 0:
        try:
            dpek__occ, akzvq__nwdn, hru__ideo = (bodo_iceberg_connector.
                get_iceberg_typing_schema(con, database_schema, table_name))
            if hru__ideo is None:
                raise BodoError('No such Iceberg table found')
        except bodo_iceberg_connector.IcebergError as dpqt__odvq:
            if isinstance(dpqt__odvq, bodo_iceberg_connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                dpek__occ = BodoError(
                    f'{dpqt__odvq.message}: {dpqt__odvq.java_error}')
            else:
                dpek__occ = BodoError(dpqt__odvq.message)
    xkrb__yum = MPI.COMM_WORLD
    dpek__occ = xkrb__yum.bcast(dpek__occ)
    if isinstance(dpek__occ, Exception):
        raise dpek__occ
    col_names = dpek__occ
    akzvq__nwdn = xkrb__yum.bcast(akzvq__nwdn)
    hru__ideo = xkrb__yum.bcast(hru__ideo)
    anty__jiyt = [_get_numba_typ_from_pa_typ(typ, False, True, None)[0] for
        typ in akzvq__nwdn]
    if is_merge_into_cow:
        col_names.append('_bodo_row_id')
        anty__jiyt.append(types.Array(types.int64, 1, 'C'))
    return col_names, anty__jiyt, hru__ideo


def get_iceberg_file_list(table_name: str, conn: str, database_schema: str,
    filters) ->Tuple[List[str], List[str]]:
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_file_list should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        utd__hwzr = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as dpqt__odvq:
        if isinstance(dpqt__odvq, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{dpqt__odvq.message}:\n{dpqt__odvq.java_error}')
        else:
            raise BodoError(dpqt__odvq.message)
    return utd__hwzr


def get_iceberg_snapshot_id(table_name: str, conn: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_snapshot_id should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        snapshot_id = (bodo_iceberg_connector.
            bodo_connector_get_current_snapshot_id(conn, database_schema,
            table_name))
    except bodo_iceberg_connector.IcebergError as dpqt__odvq:
        if isinstance(dpqt__odvq, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{dpqt__odvq.message}:\n{dpqt__odvq.java_error}')
        else:
            raise BodoError(dpqt__odvq.message)
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
    vsoiz__kgsy = get_row_counts and tracing.is_tracing()
    if vsoiz__kgsy:
        djk__fbeb = tracing.Event('get_iceberg_pq_dataset')
    xkrb__yum = MPI.COMM_WORLD
    fjqwq__ljey = None
    eqaeu__kgvy = None
    mgxi__cxw = None
    if bodo.get_rank() == 0:
        if vsoiz__kgsy:
            xmazj__mgn = tracing.Event('get_iceberg_file_list', is_parallel
                =False)
            xmazj__mgn.add_attribute('g_dnf_filter', str(dnf_filters))
        try:
            fjqwq__ljey, mgxi__cxw = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if vsoiz__kgsy:
                csjs__heg = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                xmazj__mgn.add_attribute('num_files', len(fjqwq__ljey))
                xmazj__mgn.add_attribute(f'first_{csjs__heg}_files', ', '.
                    join(fjqwq__ljey[:csjs__heg]))
        except Exception as dpqt__odvq:
            fjqwq__ljey = dpqt__odvq
        if vsoiz__kgsy:
            xmazj__mgn.finalize()
            oyoiy__sedzp = tracing.Event('get_snapshot_id', is_parallel=False)
        try:
            eqaeu__kgvy = get_iceberg_snapshot_id(table_name, conn,
                database_schema)
        except Exception as dpqt__odvq:
            eqaeu__kgvy = dpqt__odvq
        if vsoiz__kgsy:
            oyoiy__sedzp.finalize()
    fjqwq__ljey, eqaeu__kgvy, mgxi__cxw = xkrb__yum.bcast((fjqwq__ljey,
        eqaeu__kgvy, mgxi__cxw))
    if isinstance(fjqwq__ljey, Exception):
        svq__qit = fjqwq__ljey
        raise BodoError(
            f'Error reading Iceberg Table: {type(svq__qit).__name__}: {str(svq__qit)}\n'
            )
    if isinstance(eqaeu__kgvy, Exception):
        svq__qit = eqaeu__kgvy
        raise BodoError(
            f'Error reading Iceberg Table: {type(svq__qit).__name__}: {str(svq__qit)}\n'
            )
    ziwf__ila: List[str] = fjqwq__ljey
    snapshot_id: int = eqaeu__kgvy
    if len(ziwf__ila) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(ziwf__ila,
                get_row_counts=get_row_counts, expr_filters=expr_filters,
                is_parallel=is_parallel, typing_pa_schema=
                typing_pa_table_schema, partitioning=None, tot_rows_to_read
                =tot_rows_to_read)
        except BodoError as dpqt__odvq:
            if re.search('Schema .* was different', str(dpqt__odvq), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{dpqt__odvq}"""
                    )
            else:
                raise
    iflv__xtci = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, mgxi__cxw, snapshot_id, pq_dataset)
    if vsoiz__kgsy:
        djk__fbeb.finalize()
    return iflv__xtci


def are_schemas_compatible(pa_schema: pa.Schema, df_schema: pa.Schema,
    allow_downcasting: bool=False) ->bool:
    if pa_schema.equals(df_schema):
        return True
    if len(df_schema) < len(pa_schema):
        pxul__fhr = []
        for jzb__juu in pa_schema:
            qcyay__faq = df_schema.field_by_name(jzb__juu.name)
            if not (qcyay__faq is None and jzb__juu.nullable):
                pxul__fhr.append(jzb__juu)
        pa_schema = pa.schema(pxul__fhr)
    if len(pa_schema) != len(df_schema):
        return False
    for silhr__yycv in range(len(df_schema)):
        qcyay__faq = df_schema.field(silhr__yycv)
        jzb__juu = pa_schema.field(silhr__yycv)
        if qcyay__faq.equals(jzb__juu):
            continue
        mqzpk__peng = qcyay__faq.type
        galrv__hcvyr = jzb__juu.type
        if not mqzpk__peng.equals(galrv__hcvyr) and allow_downcasting and (
            pa.types.is_signed_integer(mqzpk__peng) and pa.types.
            is_signed_integer(galrv__hcvyr) or pa.types.is_floating(
            mqzpk__peng) and pa.types.is_floating(galrv__hcvyr)
            ) and mqzpk__peng.bit_width > galrv__hcvyr.bit_width:
            qcyay__faq = qcyay__faq.with_type(galrv__hcvyr)
        if not qcyay__faq.nullable and jzb__juu.nullable:
            qcyay__faq = qcyay__faq.with_nullable(True)
        elif allow_downcasting and qcyay__faq.nullable and not jzb__juu.nullable:
            qcyay__faq = qcyay__faq.with_nullable(False)
        df_schema = df_schema.set(silhr__yycv, qcyay__faq)
    return df_schema.equals(pa_schema)


def get_table_details_before_write(table_name: str, conn: str,
    database_schema: str, df_schema: pa.Schema, if_exists: str,
    allow_downcasting: bool=False):
    djk__fbeb = tracing.Event('iceberg_get_table_details_before_write')
    import bodo_iceberg_connector as connector
    xkrb__yum = MPI.COMM_WORLD
    spubw__zkmz = None
    iceberg_schema_id = None
    table_loc = ''
    partition_spec = []
    sort_order = []
    iceberg_schema_str = ''
    pa_schema = None
    hon__grls = {ogf__cos: wwkd__hgmoh for wwkd__hgmoh, ogf__cos in
        enumerate(df_schema.names)}
    if xkrb__yum.Get_rank() == 0:
        try:
            (table_loc, iceberg_schema_id, pa_schema, iceberg_schema_str,
                partition_spec, sort_order) = (connector.get_typing_info(
                conn, database_schema, table_name))
            for kra__qureh, *lbmea__dyj in partition_spec:
                assert kra__qureh in hon__grls, f'Iceberg Partition column {kra__qureh} not found in dataframe'
            for kra__qureh, *lbmea__dyj in sort_order:
                assert kra__qureh in hon__grls, f'Iceberg Sort column {kra__qureh} not found in dataframe'
            partition_spec = [(hon__grls[kra__qureh], *iqo__knnvl) for 
                kra__qureh, *iqo__knnvl in partition_spec]
            sort_order = [(hon__grls[kra__qureh], *iqo__knnvl) for 
                kra__qureh, *iqo__knnvl in sort_order]
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
        except connector.IcebergError as dpqt__odvq:
            if isinstance(dpqt__odvq, connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                spubw__zkmz = BodoError(
                    f'{dpqt__odvq.message}: {dpqt__odvq.java_error}')
            else:
                spubw__zkmz = BodoError(dpqt__odvq.message)
        except Exception as dpqt__odvq:
            spubw__zkmz = dpqt__odvq
    spubw__zkmz = xkrb__yum.bcast(spubw__zkmz)
    if isinstance(spubw__zkmz, Exception):
        raise spubw__zkmz
    table_loc = xkrb__yum.bcast(table_loc)
    iceberg_schema_id = xkrb__yum.bcast(iceberg_schema_id)
    partition_spec = xkrb__yum.bcast(partition_spec)
    sort_order = xkrb__yum.bcast(sort_order)
    iceberg_schema_str = xkrb__yum.bcast(iceberg_schema_str)
    pa_schema = xkrb__yum.bcast(pa_schema)
    if iceberg_schema_id is None:
        already_exists = False
        iceberg_schema_id = -1
    else:
        already_exists = True
    djk__fbeb.finalize()
    return (already_exists, table_loc, iceberg_schema_id, partition_spec,
        sort_order, iceberg_schema_str, pa_schema if if_exists == 'append' and
        pa_schema is not None else df_schema)


def collect_file_info(iceberg_files_info) ->Tuple[List[str], List[int],
    List[int]]:
    from mpi4py import MPI
    xkrb__yum = MPI.COMM_WORLD
    ush__ozk = [zjonw__okao[0] for zjonw__okao in iceberg_files_info]
    xuv__jvyey = xkrb__yum.gather(ush__ozk)
    fnames = [orf__cnt for xfgi__agpmu in xuv__jvyey for orf__cnt in
        xfgi__agpmu] if xkrb__yum.Get_rank() == 0 else None
    taa__eual = np.array([zjonw__okao[1] for zjonw__okao in
        iceberg_files_info], dtype=np.int64)
    pyzn__ukd = np.array([zjonw__okao[2] for zjonw__okao in
        iceberg_files_info], dtype=np.int64)
    hiqh__qgyh = bodo.gatherv(taa__eual).tolist()
    lra__mpwkj = bodo.gatherv(pyzn__ukd).tolist()
    return fnames, hiqh__qgyh, lra__mpwkj


def register_table_write(conn_str: str, db_name: str, table_name: str,
    table_loc: str, fnames: List[str], all_metrics: Dict[str, List[Any]],
    iceberg_schema_id: int, pa_schema, partition_spec, sort_order, mode: str):
    djk__fbeb = tracing.Event('iceberg_register_table_write')
    import bodo_iceberg_connector
    xkrb__yum = MPI.COMM_WORLD
    success = False
    if xkrb__yum.Get_rank() == 0:
        evpj__rrk = None if iceberg_schema_id < 0 else iceberg_schema_id
        success = bodo_iceberg_connector.commit_write(conn_str, db_name,
            table_name, table_loc, fnames, all_metrics, evpj__rrk,
            pa_schema, partition_spec, sort_order, mode)
    success = xkrb__yum.bcast(success)
    djk__fbeb.finalize()
    return success


def register_table_merge_cow(conn_str: str, db_name: str, table_name: str,
    table_loc: str, old_fnames: List[str], new_fnames: List[str],
    all_metrics: Dict[str, List[Any]], snapshot_id: int):
    djk__fbeb = tracing.Event('iceberg_register_table_merge_cow')
    import bodo_iceberg_connector
    xkrb__yum = MPI.COMM_WORLD
    success = False
    if xkrb__yum.Get_rank() == 0:
        success = bodo_iceberg_connector.commit_merge_cow(conn_str, db_name,
            table_name, table_loc, old_fnames, new_fnames, all_metrics,
            snapshot_id)
    success: bool = xkrb__yum.bcast(success)
    djk__fbeb.finalize()
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
    kavo__ztu = 'snappy'
    ccjn__tdo = -1
    iceberg_files_info = iceberg_pq_write_table_cpp(unicode_to_utf8(
        table_loc), bodo_table, col_names, partition_spec, sort_order,
        unicode_to_utf8(kavo__ztu), is_parallel, unicode_to_utf8(
        bucket_region), ccjn__tdo, unicode_to_utf8(iceberg_schema_str),
        expected_schema)
    return iceberg_files_info


@numba.njit()
def iceberg_write(table_name, conn, database_schema, bodo_table, col_names,
    if_exists, is_parallel, df_pyarrow_schema, allow_downcasting=False):
    djk__fbeb = tracing.Event('iceberg_write_py', is_parallel)
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
        fnames, hiqh__qgyh, lra__mpwkj = collect_file_info(iceberg_files_info)
        success = register_table_write(conn, database_schema, table_name,
            table_loc, fnames, {'size': lra__mpwkj, 'record_count':
            hiqh__qgyh}, iceberg_schema_id, df_pyarrow_schema,
            partition_spec, sort_order, mode)
    if not success:
        raise BodoError('Iceberg write failed.')
    djk__fbeb.finalize()


@numba.generated_jit(nopython=True)
def iceberg_merge_cow_py(table_name, conn, database_schema, bodo_df,
    snapshot_id, old_fnames, is_parallel=False):
    if not is_parallel:
        raise BodoError(
            'Merge Into with Iceberg Tables are only supported on distributed DataFrames'
            )
    df_pyarrow_schema = bodo.io.helpers.numba_to_pyarrow_schema(bodo_df,
        is_iceberg=True)
    wnzi__rhrkb = pd.array(bodo_df.columns)
    if bodo_df.is_table_format:
        xui__ypgqb = bodo_df.table_type

        def impl(table_name, conn, database_schema, bodo_df, snapshot_id,
            old_fnames, is_parallel=False):
            iceberg_merge_cow(table_name, format_iceberg_conn_njit(conn),
                database_schema, py_table_to_cpp_table(bodo.hiframes.
                pd_dataframe_ext.get_dataframe_table(bodo_df), xui__ypgqb),
                snapshot_id, old_fnames, array_to_info(wnzi__rhrkb),
                df_pyarrow_schema, is_parallel)
    else:
        zix__cmfbv = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(bodo_df, {}))'
            .format(wwkd__hgmoh) for wwkd__hgmoh in range(len(bodo_df.columns))
            )
        cwv__qsw = 'def impl(\n'
        cwv__qsw += '    table_name,\n'
        cwv__qsw += '    conn,\n'
        cwv__qsw += '    database_schema,\n'
        cwv__qsw += '    bodo_df,\n'
        cwv__qsw += '    snapshot_id,\n'
        cwv__qsw += '    old_fnames,\n'
        cwv__qsw += '    is_parallel=False,\n'
        cwv__qsw += '):\n'
        cwv__qsw += '    info_list = [{}]\n'.format(zix__cmfbv)
        cwv__qsw += '    table = arr_info_list_to_table(info_list)\n'
        cwv__qsw += '    iceberg_merge_cow(\n'
        cwv__qsw += '        table_name,\n'
        cwv__qsw += '        format_iceberg_conn_njit(conn),\n'
        cwv__qsw += '        database_schema,\n'
        cwv__qsw += '        table,\n'
        cwv__qsw += '        snapshot_id,\n'
        cwv__qsw += '        old_fnames,\n'
        cwv__qsw += '        array_to_info(col_names_py),\n'
        cwv__qsw += '        df_pyarrow_schema,\n'
        cwv__qsw += '        is_parallel,\n'
        cwv__qsw += '    )\n'
        locals = dict()
        globals = {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'iceberg_merge_cow': iceberg_merge_cow,
            'format_iceberg_conn_njit': format_iceberg_conn_njit,
            'col_names_py': wnzi__rhrkb, 'df_pyarrow_schema': df_pyarrow_schema
            }
        exec(cwv__qsw, globals, locals)
        impl = locals['impl']
    return impl


@numba.njit()
def iceberg_merge_cow(table_name, conn, database_schema, bodo_table,
    snapshot_id, old_fnames, col_names, df_pyarrow_schema, is_parallel):
    djk__fbeb = tracing.Event('iceberg_merge_cow_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        partition_spec='python_list_of_heterogeneous_tuples_type',
        sort_order='python_list_of_heterogeneous_tuples_type',
        iceberg_schema_str='unicode_type', expected_schema=
        'pyarrow_table_schema_type'):
        (already_exists, table_loc, lbmea__dyj, partition_spec, sort_order,
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
        fnames, hiqh__qgyh, lra__mpwkj = collect_file_info(iceberg_files_info)
        success = register_table_merge_cow(conn, database_schema,
            table_name, table_loc, old_fnames, fnames, {'size': lra__mpwkj,
            'record_count': hiqh__qgyh}, snapshot_id)
    if not success:
        raise BodoError('Iceberg MERGE INTO: write failed')
    djk__fbeb.finalize()


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
        gwf__ayabf = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        xezh__buh = cgutils.get_or_insert_function(builder.module,
            gwf__ayabf, name='iceberg_pq_write')
        ilzgd__omq = builder.call(xezh__buh, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return ilzgd__omq
    return types.python_list_of_heterogeneous_tuples_type(types.voidptr,
        table_t, col_names_t, python_list_of_heterogeneous_tuples_type,
        python_list_of_heterogeneous_tuples_type, types.voidptr, types.
        boolean, types.voidptr, types.int64, types.voidptr,
        pyarrow_table_schema_type), codegen
