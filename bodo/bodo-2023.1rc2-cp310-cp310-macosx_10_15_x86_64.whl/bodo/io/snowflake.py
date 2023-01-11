import os
import sys
import traceback
import warnings
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Callable, Dict, List, Literal, Optional, Tuple
from urllib.parse import parse_qsl, urlparse
from uuid import uuid4
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.io.helpers import ExceptionPropagatingThread, _get_numba_typ_from_pa_typ, update_env_vars, update_file_contents
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError, BodoWarning, is_str_arr_type
if TYPE_CHECKING:
    from snowflake.connector import SnowflakeConnection
    from snowflake.connector.cursor import ResultMetadata, SnowflakeCursor
    from snowflake.connector.result_batch import JSONResultBatch, ResultBatch
SF_READ_SCHEMA_PROBE_TIMEOUT = 5
SF_READ_AUTO_DICT_ENCODE_ENABLED = True
SF_READ_DICT_ENCODE_CRITERION = 0.5
SF_READ_DICT_ENCODING_PROBE_TIMEOUT = 5
SF_READ_DICT_ENCODING_IF_TIMEOUT = False
SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT = 100000000
SCALE_TO_UNIT_PRECISION: Dict[int, Literal['s', 'ms', 'us', 'ns']] = {(0):
    's', (3): 'ms', (6): 'us', (9): 'ns'}
TYPE_CODE_TO_ARROW_TYPE: List[Callable[['ResultMetadata', str], pa.DataType]
    ] = [lambda m, _: pa.int64() if m.scale == 0 else pa.float64() if m.
    scale < 18 else pa.decimal128(m.precision, m.scale), lambda _, __: pa.
    float64(), lambda _, __: pa.string(), lambda _, __: pa.date32(), lambda
    _, __: pa.time64('ns'), lambda _, __: pa.string(), lambda m, tz: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale], tz=tz), lambda m, tz: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale], tz=tz), lambda m, _: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale]), lambda _, __: pa.string(),
    lambda _, __: pa.string(), lambda _, __: pa.binary(), lambda m, _: {(0):
    pa.time32('s'), (3): pa.time32('ms'), (6): pa.time64('us'), (9): pa.
    time64('ns')}[m.scale], lambda _, __: pa.bool_(), lambda _, __: pa.string()
    ]
INT_BITSIZE_TO_ARROW_DATATYPE = {(1): pa.int8(), (2): pa.int16(), (4): pa.
    int32(), (8): pa.int64()}


def gen_snowflake_schema(column_names, column_datatypes):
    sf_schema = {}
    for col_name, wsrw__owv in zip(column_names, column_datatypes):
        if isinstance(wsrw__owv, bodo.DatetimeArrayType
            ) or wsrw__owv == bodo.datetime_datetime_type:
            sf_schema[col_name] = 'TIMESTAMP_NTZ'
        elif wsrw__owv == bodo.datetime_date_array_type:
            sf_schema[col_name] = 'DATE'
        elif isinstance(wsrw__owv, bodo.TimeArrayType):
            if wsrw__owv.precision in [0, 3, 6]:
                bjed__zahr = wsrw__owv.precision
            elif wsrw__owv.precision == 9:
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"""to_sql(): {col_name} time precision will be lost.
Snowflake loses nano second precision when exporting parquet file using COPY INTO.
 This is due to a limitation on Parquet V1 that is currently being used in Snowflake"""
                        ))
                bjed__zahr = 6
            else:
                raise ValueError(
                    'Unsupported Precision Found in Bodo Time Array')
            sf_schema[col_name] = f'TIME({bjed__zahr})'
        elif isinstance(wsrw__owv, types.Array):
            wnv__mnlxd = wsrw__owv.dtype.name
            if wnv__mnlxd.startswith('datetime'):
                sf_schema[col_name] = 'DATETIME'
            if wnv__mnlxd.startswith('timedelta'):
                sf_schema[col_name] = 'NUMBER(38, 0)'
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"to_sql(): {col_name} with type 'timedelta' will be written as integer values (ns frequency) to the database."
                        ))
            elif wnv__mnlxd.startswith(('int', 'uint')):
                sf_schema[col_name] = 'NUMBER(38, 0)'
            elif wnv__mnlxd.startswith('float'):
                sf_schema[col_name] = 'REAL'
        elif is_str_arr_type(wsrw__owv):
            sf_schema[col_name] = 'TEXT'
        elif wsrw__owv == bodo.binary_array_type:
            sf_schema[col_name] = 'BINARY'
        elif wsrw__owv == bodo.boolean_array:
            sf_schema[col_name] = 'BOOLEAN'
        elif isinstance(wsrw__owv, bodo.IntegerArrayType):
            sf_schema[col_name] = 'NUMBER(38, 0)'
        elif isinstance(wsrw__owv, bodo.FloatingArrayType):
            sf_schema[col_name] = 'REAL'
        elif isinstance(wsrw__owv, bodo.DecimalArrayType):
            sf_schema[col_name] = 'NUMBER(38, 18)'
        elif isinstance(wsrw__owv, (ArrayItemArrayType, StructArrayType)):
            sf_schema[col_name] = 'VARIANT'
        else:
            raise BodoError(
                f'Conversion from Bodo array type {wsrw__owv} to snowflake type for {col_name} not supported yet.'
                )
    return sf_schema


SF_WRITE_COPY_INTO_ON_ERROR = 'abort_statement'
SF_WRITE_OVERLAP_UPLOAD = True
SF_WRITE_PARQUET_CHUNK_SIZE = int(256000000.0)
SF_WRITE_PARQUET_COMPRESSION = 'snappy'
SF_WRITE_UPLOAD_USING_PUT = False
SF_AZURE_WRITE_HDFS_CORE_SITE = """<configuration>
  <property>
    <name>fs.azure.account.auth.type</name>
    <value>SAS</value>
  </property>
  <property>
    <name>fs.azure.sas.token.provider.type</name>
    <value>org.bodo.azurefs.sas.BodoSASTokenProvider</value>
  </property>
  <property>
    <name>fs.abfs.impl</name>
    <value>org.apache.hadoop.fs.azurebfs.AzureBlobFileSystem</value>
  </property>
</configuration>
"""
SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION = os.path.join(bodo.
    HDFS_CORE_SITE_LOC_DIR.name, 'sas_token.txt')


def execute_query(cursor: 'SnowflakeCursor', query: str, timeout: Optional[int]
    ) ->Optional['SnowflakeCursor']:
    try:
        return cursor.execute(query, timeout=timeout)
    except snowflake.connector.errors.ProgrammingError as rbguh__ykx:
        if 'SQL execution canceled' in str(rbguh__ykx):
            return None
        else:
            raise


def escape_col_name(col_name: str) ->str:
    return '"{}"'.format(col_name.replace('"', '""'))


def snowflake_connect(conn_str: str, is_parallel: bool=False
    ) ->'SnowflakeConnection':
    gcm__eetn = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    kik__rjasc = urlparse(conn_str)
    craxc__feesq = {}
    if kik__rjasc.username:
        craxc__feesq['user'] = kik__rjasc.username
    if kik__rjasc.password:
        craxc__feesq['password'] = kik__rjasc.password
    if kik__rjasc.hostname:
        craxc__feesq['account'] = kik__rjasc.hostname
    if kik__rjasc.port:
        craxc__feesq['port'] = kik__rjasc.port
    if kik__rjasc.path:
        lec__zqtge = kik__rjasc.path
        if lec__zqtge.startswith('/'):
            lec__zqtge = lec__zqtge[1:]
        wwbsk__cmm = lec__zqtge.split('/')
        if len(wwbsk__cmm) == 2:
            dimc__hyzm, schema = wwbsk__cmm
        elif len(wwbsk__cmm) == 1:
            dimc__hyzm = wwbsk__cmm[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        craxc__feesq['database'] = dimc__hyzm
        if schema:
            craxc__feesq['schema'] = schema
    if kik__rjasc.query:
        for qitrs__uvy, qgh__affwt in parse_qsl(kik__rjasc.query):
            craxc__feesq[qitrs__uvy] = qgh__affwt
            if qitrs__uvy == 'session_parameters':
                import json
                craxc__feesq[qitrs__uvy] = json.loads(qgh__affwt)
    craxc__feesq['application'] = 'bodo'
    craxc__feesq['login_timeout'] = 5
    try:
        import snowflake.connector
    except ImportError as efm__rdwa:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**craxc__feesq)
    hqt__ehl = os.environ.get('BODO_PLATFORM_WORKSPACE_REGION', None)
    if hqt__ehl and bodo.get_rank() == 0:
        hqt__ehl = hqt__ehl.lower()
        engtz__lvahp = os.environ.get('BODO_PLATFORM_CLOUD_PROVIDER', None)
        if engtz__lvahp is not None:
            engtz__lvahp = engtz__lvahp.lower()
        qvc__hlm = conn.cursor()
        qvc__hlm.execute('select current_region()')
        bmmsm__gxjuz: pa.Table = qvc__hlm.fetch_arrow_all()
        nuvy__crhm = bmmsm__gxjuz[0][0].as_py()
        qvc__hlm.close()
        fbs__iqvf = nuvy__crhm.split('_')
        xcirh__oafan = fbs__iqvf[0].lower()
        nvcx__vusib = '-'.join(fbs__iqvf[1:]).lower()
        if engtz__lvahp and engtz__lvahp != xcirh__oafan:
            zosa__bqlt = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are on different cloud providers. '
                 +
                f'The Snowflake warehouse is located on {xcirh__oafan}, but the Bodo cluster is located on {engtz__lvahp}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(zosa__bqlt)
        elif hqt__ehl != nvcx__vusib:
            zosa__bqlt = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are in different cloud regions. '
                 +
                f'The Snowflake warehouse is located in {nvcx__vusib}, but the Bodo cluster is located in {hqt__ehl}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(zosa__bqlt)
    gcm__eetn.finalize()
    return conn


def get_schema_from_metadata(cursor: 'SnowflakeCursor', sql_query: str,
    is_select_query: bool) ->Tuple[List[pa.Field], List, List[int], List[pa
    .DataType]]:
    lkkv__srkr = cursor.describe(sql_query)
    tz: str = cursor._timezone
    xpo__wun: List[pa.Field] = []
    klc__zbip: List[str] = []
    utxtk__fnd: List[int] = []
    for mno__zrcu, iol__yhx in enumerate(lkkv__srkr):
        zwl__rbd = TYPE_CODE_TO_ARROW_TYPE[iol__yhx.type_code](iol__yhx, tz)
        xpo__wun.append(pa.field(iol__yhx.name, zwl__rbd, iol__yhx.is_nullable)
            )
        if pa.types.is_int64(zwl__rbd):
            klc__zbip.append(iol__yhx.name)
            utxtk__fnd.append(mno__zrcu)
    if is_select_query and len(klc__zbip) != 0:
        aws__igxu = 'SELECT ' + ', '.join(
            f'SYSTEM$TYPEOF({escape_col_name(x)})' for x in klc__zbip
            ) + f' FROM ({sql_query}) LIMIT 1'
        rrr__zdt = execute_query(cursor, aws__igxu, timeout=
            SF_READ_SCHEMA_PROBE_TIMEOUT)
        if rrr__zdt is not None and (swr__qeyo := rrr__zdt.fetch_arrow_all()
            ) is not None:
            for mno__zrcu, (kqjjb__myzzh, isi__xstx) in enumerate(swr__qeyo
                .to_pylist()[0].items()):
                zzypc__jap = klc__zbip[mno__zrcu]
                scyy__gdjfm = (
                    f'SYSTEM$TYPEOF({escape_col_name(zzypc__jap)})',
                    f'SYSTEM$TYPEOF({escape_col_name(zzypc__jap.upper())})')
                assert kqjjb__myzzh in scyy__gdjfm, 'Output of Snowflake Schema Probe Query Uses Unexpected Column Names'
                qwr__yrss = utxtk__fnd[mno__zrcu]
                ywfe__azd = int(isi__xstx[-2])
                xamy__ybqlo = INT_BITSIZE_TO_ARROW_DATATYPE[ywfe__azd]
                xpo__wun[qwr__yrss] = xpo__wun[qwr__yrss].with_type(xamy__ybqlo
                    )
    unsm__wqgwy = []
    vnd__xzd = []
    lmwxq__zltn = []
    for mno__zrcu, mrcf__xjg in enumerate(xpo__wun):
        zwl__rbd, fyt__gbcxs = _get_numba_typ_from_pa_typ(mrcf__xjg, False,
            mrcf__xjg.nullable, None)
        unsm__wqgwy.append(zwl__rbd)
        if not fyt__gbcxs:
            vnd__xzd.append(mno__zrcu)
            lmwxq__zltn.append(mrcf__xjg.type)
    return xpo__wun, unsm__wqgwy, vnd__xzd, lmwxq__zltn


def get_schema(conn_str: str, sql_query: str, is_select_query: bool,
    _bodo_read_as_dict: Optional[List[str]]):
    conn = snowflake_connect(conn_str)
    cursor = conn.cursor()
    vtzu__ezxs, unsm__wqgwy, vnd__xzd, lmwxq__zltn = get_schema_from_metadata(
        cursor, sql_query, is_select_query)
    vpf__rusln = _bodo_read_as_dict if _bodo_read_as_dict else []
    yenrg__vjtn = {}
    for mno__zrcu, icrtd__lnfct in enumerate(unsm__wqgwy):
        if icrtd__lnfct == string_array_type:
            yenrg__vjtn[vtzu__ezxs[mno__zrcu].name] = mno__zrcu
    xiusy__vpcts = {(urst__xrsk.lower() if urst__xrsk.isupper() else
        urst__xrsk): urst__xrsk for urst__xrsk in yenrg__vjtn.keys()}
    jacg__fxnpf = vpf__rusln - xiusy__vpcts.keys()
    if len(jacg__fxnpf) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {jacg__fxnpf}'
                ))
    dqs__ryb = xiusy__vpcts.keys() & vpf__rusln
    for urst__xrsk in dqs__ryb:
        unsm__wqgwy[yenrg__vjtn[xiusy__vpcts[urst__xrsk]]] = dict_str_arr_type
    vjlpj__qzo, kxe__rxcuy = [], []
    tjy__vphpp = xiusy__vpcts.keys() - vpf__rusln
    for urst__xrsk in tjy__vphpp:
        vjlpj__qzo.append(f'count (distinct "{xiusy__vpcts[urst__xrsk]}")')
        kxe__rxcuy.append(yenrg__vjtn[xiusy__vpcts[urst__xrsk]])
    amm__tzqkl: Optional[Tuple[int, List[str]]] = None
    if len(vjlpj__qzo) != 0 and SF_READ_AUTO_DICT_ENCODE_ENABLED:
        cuh__rtb = max(SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT // len(
            vjlpj__qzo), 1)
        burfz__ncug = (
            f"select count(*),{', '.join(vjlpj__qzo)}from ( select * from ({sql_query}) limit {cuh__rtb} ) SAMPLE (1)"
            )
        bwa__zcw = execute_query(cursor, burfz__ncug, timeout=
            SF_READ_DICT_ENCODING_PROBE_TIMEOUT)
        if bwa__zcw is None:
            amm__tzqkl = cuh__rtb, vjlpj__qzo
            if SF_READ_DICT_ENCODING_IF_TIMEOUT:
                for mno__zrcu in kxe__rxcuy:
                    unsm__wqgwy[mno__zrcu] = dict_str_arr_type
        else:
            drtx__fhj: pa.Table = bwa__zcw.fetch_arrow_all()
            qidz__cmpw = drtx__fhj[0][0].as_py()
            vcapx__hwi = [(drtx__fhj[mno__zrcu][0].as_py() / max(qidz__cmpw,
                1)) for mno__zrcu in range(1, len(vjlpj__qzo) + 1)]
            zvrk__iwcin = filter(lambda x: x[0] <=
                SF_READ_DICT_ENCODE_CRITERION, zip(vcapx__hwi, kxe__rxcuy))
            for _, grint__qfc in zvrk__iwcin:
                unsm__wqgwy[grint__qfc] = dict_str_arr_type
    sdlt__zsc: List[str] = []
    wwuo__hbikg = set()
    for x in vtzu__ezxs:
        if x.name.isupper():
            wwuo__hbikg.add(x.name.lower())
            sdlt__zsc.append(x.name.lower())
        else:
            sdlt__zsc.append(x.name)
    wzm__dvs = DataFrameType(data=tuple(unsm__wqgwy), columns=tuple(sdlt__zsc))
    return wzm__dvs, wwuo__hbikg, vnd__xzd, lmwxq__zltn, pa.schema(vtzu__ezxs
        ), amm__tzqkl


class SnowflakeDataset(object):

    def __init__(self, batches: List['ResultBatch'], schema, conn:
        'SnowflakeConnection'):
        self.pieces = batches
        self._bodo_total_rows = 0
        for xvijd__pzdtb in batches:
            xvijd__pzdtb._bodo_num_rows = xvijd__pzdtb.rowcount
            self._bodo_total_rows += xvijd__pzdtb._bodo_num_rows
        self.schema = schema
        self.conn = conn


class FakeArrowJSONResultBatch:

    def __init__(self, json_batch: 'JSONResultBatch', schema: pa.Schema
        ) ->None:
        self._json_batch = json_batch
        self._schema = schema

    @property
    def rowcount(self):
        return self._json_batch.rowcount

    def to_arrow(self, _: Optional['SnowflakeConnection']=None) ->pa.Table:
        bxr__tzcw = []
        for zij__zhy in self._json_batch.create_iter():
            bxr__tzcw.append({self._schema.names[mno__zrcu]: mtojt__tbe for
                mno__zrcu, mtojt__tbe in enumerate(zij__zhy)})
        gzvh__kaid = pa.Table.from_pylist(bxr__tzcw, schema=self._schema)
        return gzvh__kaid


def get_dataset(query: str, conn_str: str, schema: pa.Schema,
    only_fetch_length: bool=False, is_select_query: bool=True, is_parallel:
    bool=True, is_independent: bool=False) ->Tuple[SnowflakeDataset, int]:
    assert not (only_fetch_length and not is_select_query
        ), 'The only length optimization can only be run with select queries'
    assert not (is_parallel and is_independent
        ), 'Snowflake get_dataset: is_parallel and is_independent cannot be True at the same time'
    try:
        import snowflake.connector
        from snowflake.connector.result_batch import ArrowResultBatch, JSONResultBatch
    except ImportError as efm__rdwa:
        raise BodoError(
            "Snowflake Python connector packages not found. Fetching data from Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    gcm__eetn = tracing.Event('get_snowflake_dataset', is_parallel=is_parallel)
    vvvqw__lawb = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    ttqqj__qian = -1
    batches = []
    if only_fetch_length and is_select_query:
        if bodo.get_rank() == 0 or is_independent:
            qvc__hlm = conn.cursor()
            faywh__xif = tracing.Event('execute_length_query', is_parallel=
                False)
            qvc__hlm.execute(query)
            bmmsm__gxjuz = qvc__hlm.fetch_arrow_all()
            ttqqj__qian = bmmsm__gxjuz[0][0].as_py()
            qvc__hlm.close()
            faywh__xif.finalize()
        if not is_independent:
            ttqqj__qian = vvvqw__lawb.bcast(ttqqj__qian)
    else:
        if bodo.get_rank() == 0 or is_independent:
            qvc__hlm = conn.cursor()
            faywh__xif = tracing.Event('execute_query', is_parallel=False)
            qvc__hlm = conn.cursor()
            qvc__hlm.execute(query)
            faywh__xif.finalize()
            ttqqj__qian: int = qvc__hlm.rowcount
            batches: 'List[ResultBatch]' = qvc__hlm.get_result_batches()
            if len(batches) > 0 and not isinstance(batches[0], ArrowResultBatch
                ):
                if not is_select_query and len(batches) == 1 and isinstance(
                    batches[0], JSONResultBatch):
                    batches = [FakeArrowJSONResultBatch(x, schema) for x in
                        batches]
                else:
                    raise BodoError(
                        f"Batches returns from Snowflake don't match the expected format. Expected Arrow batches but got {type(batches[0])}"
                        )
            qvc__hlm.close()
        if not is_independent:
            ttqqj__qian, batches, schema = vvvqw__lawb.bcast((ttqqj__qian,
                batches, schema))
    sbc__dtcj = SnowflakeDataset(batches, schema, conn)
    gcm__eetn.finalize()
    return sbc__dtcj, ttqqj__qian


def create_internal_stage(cursor: 'SnowflakeCursor', is_temporary: bool=False
    ) ->str:
    gcm__eetn = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as efm__rdwa:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = ''
    fpn__upou = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                vprm__nusj = 'CREATE TEMPORARY STAGE'
            else:
                vprm__nusj = 'CREATE STAGE'
            okgh__pdq = (
                f'{vprm__nusj} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(okgh__pdq, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as xxg__rtpto:
            if xxg__rtpto.msg is not None and xxg__rtpto.msg.endswith(
                'already exists.'):
                continue
            fpn__upou = xxg__rtpto.msg
            break
    gcm__eetn.finalize()
    if fpn__upou is not None:
        raise snowflake.connector.ProgrammingError(fpn__upou)
    return stage_name


def drop_internal_stage(cursor: 'SnowflakeCursor', stage_name: str):
    gcm__eetn = tracing.Event('drop_internal_stage', is_parallel=False)
    rivrv__mnk = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(rivrv__mnk, _is_internal=True)
    gcm__eetn.finalize()


def do_upload_and_cleanup(cursor: 'SnowflakeCursor', chunk_idx: int,
    chunk_path: str, stage_name: str):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        vakq__mzdr = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        vdzso__pexn = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(vdzso__pexn, _is_internal=True).fetchall()
        vakq__mzdr.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        wvi__lplig = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        wvi__lplig.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        wvi__lplig = None
    return wvi__lplig


def create_table_handle_exists(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str):
    gcm__eetn = tracing.Event('create_table_if_not_exists', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as efm__rdwa:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    if if_exists == 'fail':
        hetoa__gczc = 'CREATE TABLE'
    elif if_exists == 'replace':
        hetoa__gczc = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        hetoa__gczc = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    ikwi__rhf = tracing.Event('create_table', is_parallel=False)
    czgzr__csi = ', '.join([f'"{bvyb__dqc}" {sf_schema[bvyb__dqc]}' for
        bvyb__dqc in sf_schema.keys()])
    kvcrm__zwoqs = (
        f'{hetoa__gczc} {location} ({czgzr__csi}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(kvcrm__zwoqs, _is_internal=True)
    ikwi__rhf.finalize()
    gcm__eetn.finalize()


def execute_copy_into(cursor: 'SnowflakeCursor', stage_name: str, location:
    str, sf_schema):
    gcm__eetn = tracing.Event('execute_copy_into', is_parallel=False)
    avbc__ocmyw = ','.join([f'"{bvyb__dqc}"' for bvyb__dqc in sf_schema.keys()]
        )
    bon__lfc = {bvyb__dqc: ('::binary' if sf_schema[bvyb__dqc] == 'BINARY' else
        '::string' if sf_schema[bvyb__dqc].startswith('TIME') else '') for
        bvyb__dqc in sf_schema.keys()}
    uaz__hzxog = ','.join([f'$1:"{bvyb__dqc}"{bon__lfc[bvyb__dqc]}' for
        bvyb__dqc in sf_schema.keys()])
    pfyxr__vxhr = (
        f'COPY INTO {location} ({avbc__ocmyw}) FROM (SELECT {uaz__hzxog} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO BINARY_AS_TEXT=False) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    qkt__eya = cursor.execute(pfyxr__vxhr, _is_internal=True).fetchall()
    rcrqc__osu = sum(1 if rbguh__ykx[1] == 'LOADED' else 0 for rbguh__ykx in
        qkt__eya)
    jhsz__qxbzr = len(qkt__eya)
    nwn__nkwor = sum(int(rbguh__ykx[3]) for rbguh__ykx in qkt__eya)
    veb__blphw = rcrqc__osu, jhsz__qxbzr, nwn__nkwor, qkt__eya
    gcm__eetn.add_attribute('copy_into_nsuccess', rcrqc__osu)
    gcm__eetn.add_attribute('copy_into_nchunks', jhsz__qxbzr)
    gcm__eetn.add_attribute('copy_into_nrows', nwn__nkwor)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(qkt__eya)}')
    gcm__eetn.finalize()
    return veb__blphw


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except (ImportError, AttributeError) as efm__rdwa:
    snowflake_connector_cursor_python_type = None
SnowflakeConnectorCursorType = install_py_obj_class(types_name=
    'snowflake_connector_cursor_type', python_type=
    snowflake_connector_cursor_python_type, module=sys.modules[__name__],
    class_name='SnowflakeConnectorCursorType', model_name=
    'SnowflakeConnectorCursorModel')
TemporaryDirectoryType = install_py_obj_class(types_name=
    'temporary_directory_type', python_type=TemporaryDirectory, module=sys.
    modules[__name__], class_name='TemporaryDirectoryType', model_name=
    'TemporaryDirectoryModel')


def get_snowflake_stage_info(cursor: 'SnowflakeCursor', stage_name: str,
    tmp_folder: TemporaryDirectory) ->Dict:
    gcm__eetn = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    qsxqx__ich = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    qsxqx__ich = qsxqx__ich.replace('\\', '\\\\').replace("'", "\\'")
    vdzso__pexn = (
        f'PUT \'file://{qsxqx__ich}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    akqec__qsenr = cursor._execute_helper(vdzso__pexn, is_internal=True)
    gcm__eetn.finalize()
    return akqec__qsenr


def connect_and_get_upload_info(conn_str: str):
    gcm__eetn = tracing.Event('connect_and_get_upload_info')
    vvvqw__lawb = MPI.COMM_WORLD
    rzkad__oulks = vvvqw__lawb.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    gscz__qzxuv = ''
    drg__fcepe = {}
    old_creds = {}
    old_core_site = ''
    whvq__ylbrj = ''
    old_sas_token = ''
    pul__oblsh = None
    if rzkad__oulks == 0:
        try:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                gscz__qzxuv = ''
            else:
                akqec__qsenr = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                gxi__wzxbj = akqec__qsenr['data']['uploadInfo']
                gip__ccu = gxi__wzxbj.get('locationType', 'UNKNOWN')
                gnh__xop = False
                if gip__ccu == 'S3':
                    hwn__mojsd, _, lec__zqtge = gxi__wzxbj['location'
                        ].partition('/')
                    lec__zqtge = lec__zqtge.rstrip('/')
                    gscz__qzxuv = f's3://{hwn__mojsd}/{lec__zqtge}/'
                    drg__fcepe = {'AWS_ACCESS_KEY_ID': gxi__wzxbj['creds'][
                        'AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY': gxi__wzxbj[
                        'creds']['AWS_SECRET_KEY'], 'AWS_SESSION_TOKEN':
                        gxi__wzxbj['creds']['AWS_TOKEN'],
                        'AWS_DEFAULT_REGION': gxi__wzxbj['region']}
                elif gip__ccu == 'AZURE':
                    jsrkr__qipf = False
                    try:
                        import bodo_azurefs_sas_token_provider
                        jsrkr__qipf = True
                    except ImportError as efm__rdwa:
                        pass
                    azkp__jba = len(os.environ.get('HADOOP_HOME', '')
                        ) > 0 and len(os.environ.get('ARROW_LIBHDFS_DIR', '')
                        ) > 0 and len(os.environ.get('CLASSPATH', '')) > 0
                    if jsrkr__qipf and azkp__jba:
                        mnp__srfkx, _, lec__zqtge = gxi__wzxbj['location'
                            ].partition('/')
                        lec__zqtge = lec__zqtge.rstrip('/')
                        zoy__qci = gxi__wzxbj['storageAccount']
                        whvq__ylbrj = gxi__wzxbj['creds']['AZURE_SAS_TOKEN'
                            ].lstrip('?')
                        if len(lec__zqtge) == 0:
                            gscz__qzxuv = (
                                f'abfs://{mnp__srfkx}@{zoy__qci}.dfs.core.windows.net/'
                                )
                        else:
                            gscz__qzxuv = (
                                f'abfs://{mnp__srfkx}@{zoy__qci}.dfs.core.windows.net/{lec__zqtge}/'
                                )
                        if not 'BODO_PLATFORM_WORKSPACE_UUID' in os.environ:
                            warnings.warn(BodoWarning(
                                """Detected Azure Stage. Bodo will try to upload to the stage directly. If this fails, there might be issues with your Hadoop configuration and you may need to use the PUT method instead by setting
import bodo
bodo.io.snowflake.SF_WRITE_UPLOAD_USING_PUT = True
before calling this function."""
                                ))
                    else:
                        gnh__xop = True
                        jpw__wbd = 'Detected Azure Stage. '
                        if not jsrkr__qipf:
                            jpw__wbd += """Required package bodo_azurefs_sas_token_provider is not installed. To use direct upload to stage in the future, install the package using: 'conda install bodo-azurefs-sas-token-provider -c bodo.ai -c conda-forge'.
"""
                        if not azkp__jba:
                            jpw__wbd += """You need to download and set up Hadoop. For more information, refer to our documentation: https://docs.bodo.ai/latest/file_io/?h=hdfs#HDFS.
"""
                        jpw__wbd += (
                            'Falling back to PUT command for upload for now.')
                        warnings.warn(BodoWarning(jpw__wbd))
                else:
                    gnh__xop = True
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{gip__ccu}'. Falling back to PUT command for upload."
                        ))
                if gnh__xop:
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as rbguh__ykx:
            pul__oblsh = RuntimeError(str(rbguh__ykx))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, rbguh__ykx,
                    rbguh__ykx.__traceback__)))
    pul__oblsh = vvvqw__lawb.bcast(pul__oblsh)
    if isinstance(pul__oblsh, Exception):
        raise pul__oblsh
    gscz__qzxuv = vvvqw__lawb.bcast(gscz__qzxuv)
    azure_stage_direct_upload = gscz__qzxuv.startswith('abfs://')
    if gscz__qzxuv == '':
        mrhjy__zvjf = True
        gscz__qzxuv = tmp_folder.name + '/'
        if rzkad__oulks != 0:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
    else:
        mrhjy__zvjf = False
        drg__fcepe = vvvqw__lawb.bcast(drg__fcepe)
        old_creds = update_env_vars(drg__fcepe)
        if azure_stage_direct_upload:
            import bodo_azurefs_sas_token_provider
            bodo.HDFS_CORE_SITE_LOC_DIR.initialize()
            old_core_site = update_file_contents(bodo.HDFS_CORE_SITE_LOC,
                SF_AZURE_WRITE_HDFS_CORE_SITE)
            whvq__ylbrj = vvvqw__lawb.bcast(whvq__ylbrj)
            old_sas_token = update_file_contents(
                SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION, whvq__ylbrj)
    stage_name = vvvqw__lawb.bcast(stage_name)
    gcm__eetn.finalize()
    return (cursor, tmp_folder, stage_name, gscz__qzxuv, mrhjy__zvjf,
        old_creds, azure_stage_direct_upload, old_core_site, old_sas_token)


def create_table_copy_into(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str, old_creds, tmp_folder:
    TemporaryDirectory, azure_stage_direct_upload: bool, old_core_site: str,
    old_sas_token: str):
    gcm__eetn = tracing.Event('create_table_copy_into', is_parallel=False)
    vvvqw__lawb = MPI.COMM_WORLD
    rzkad__oulks = vvvqw__lawb.Get_rank()
    pul__oblsh = None
    if rzkad__oulks == 0:
        try:
            cuj__nvzy = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(cuj__nvzy)
            create_table_handle_exists(cursor, stage_name, location,
                sf_schema, if_exists)
            rcrqc__osu, jhsz__qxbzr, nwn__nkwor, bqwlu__aoskp = (
                execute_copy_into(cursor, stage_name, location, sf_schema))
            if rcrqc__osu != jhsz__qxbzr:
                raise BodoError(
                    f'Snowflake write copy_into failed: {bqwlu__aoskp}')
            zbq__bju = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(zbq__bju)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as rbguh__ykx:
            pul__oblsh = RuntimeError(str(rbguh__ykx))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, rbguh__ykx,
                    rbguh__ykx.__traceback__)))
    pul__oblsh = vvvqw__lawb.bcast(pul__oblsh)
    if isinstance(pul__oblsh, Exception):
        raise pul__oblsh
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    if azure_stage_direct_upload:
        update_file_contents(bodo.HDFS_CORE_SITE_LOC, old_core_site)
        update_file_contents(SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION,
            old_sas_token)
    gcm__eetn.finalize()
