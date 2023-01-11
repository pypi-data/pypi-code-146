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
    for col_name, gtawv__jvqqx in zip(column_names, column_datatypes):
        if isinstance(gtawv__jvqqx, bodo.DatetimeArrayType
            ) or gtawv__jvqqx == bodo.datetime_datetime_type:
            sf_schema[col_name] = 'TIMESTAMP_NTZ'
        elif gtawv__jvqqx == bodo.datetime_date_array_type:
            sf_schema[col_name] = 'DATE'
        elif isinstance(gtawv__jvqqx, bodo.TimeArrayType):
            if gtawv__jvqqx.precision in [0, 3, 6]:
                mvyiy__igo = gtawv__jvqqx.precision
            elif gtawv__jvqqx.precision == 9:
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"""to_sql(): {col_name} time precision will be lost.
Snowflake loses nano second precision when exporting parquet file using COPY INTO.
 This is due to a limitation on Parquet V1 that is currently being used in Snowflake"""
                        ))
                mvyiy__igo = 6
            else:
                raise ValueError(
                    'Unsupported Precision Found in Bodo Time Array')
            sf_schema[col_name] = f'TIME({mvyiy__igo})'
        elif isinstance(gtawv__jvqqx, types.Array):
            raae__falk = gtawv__jvqqx.dtype.name
            if raae__falk.startswith('datetime'):
                sf_schema[col_name] = 'DATETIME'
            if raae__falk.startswith('timedelta'):
                sf_schema[col_name] = 'NUMBER(38, 0)'
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"to_sql(): {col_name} with type 'timedelta' will be written as integer values (ns frequency) to the database."
                        ))
            elif raae__falk.startswith(('int', 'uint')):
                sf_schema[col_name] = 'NUMBER(38, 0)'
            elif raae__falk.startswith('float'):
                sf_schema[col_name] = 'REAL'
        elif is_str_arr_type(gtawv__jvqqx):
            sf_schema[col_name] = 'TEXT'
        elif gtawv__jvqqx == bodo.binary_array_type:
            sf_schema[col_name] = 'BINARY'
        elif gtawv__jvqqx == bodo.boolean_array:
            sf_schema[col_name] = 'BOOLEAN'
        elif isinstance(gtawv__jvqqx, bodo.IntegerArrayType):
            sf_schema[col_name] = 'NUMBER(38, 0)'
        elif isinstance(gtawv__jvqqx, bodo.FloatingArrayType):
            sf_schema[col_name] = 'REAL'
        elif isinstance(gtawv__jvqqx, bodo.DecimalArrayType):
            sf_schema[col_name] = 'NUMBER(38, 18)'
        elif isinstance(gtawv__jvqqx, (ArrayItemArrayType, StructArrayType)):
            sf_schema[col_name] = 'VARIANT'
        else:
            raise BodoError(
                f'Conversion from Bodo array type {gtawv__jvqqx} to snowflake type for {col_name} not supported yet.'
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
    except snowflake.connector.errors.ProgrammingError as kfc__dexqg:
        if 'SQL execution canceled' in str(kfc__dexqg):
            return None
        else:
            raise


def escape_col_name(col_name: str) ->str:
    return '"{}"'.format(col_name.replace('"', '""'))


def snowflake_connect(conn_str: str, is_parallel: bool=False
    ) ->'SnowflakeConnection':
    ppgs__tik = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    znl__xdomq = urlparse(conn_str)
    edb__ssbay = {}
    if znl__xdomq.username:
        edb__ssbay['user'] = znl__xdomq.username
    if znl__xdomq.password:
        edb__ssbay['password'] = znl__xdomq.password
    if znl__xdomq.hostname:
        edb__ssbay['account'] = znl__xdomq.hostname
    if znl__xdomq.port:
        edb__ssbay['port'] = znl__xdomq.port
    if znl__xdomq.path:
        cnc__nha = znl__xdomq.path
        if cnc__nha.startswith('/'):
            cnc__nha = cnc__nha[1:]
        vin__jjy = cnc__nha.split('/')
        if len(vin__jjy) == 2:
            wwpun__shvtm, schema = vin__jjy
        elif len(vin__jjy) == 1:
            wwpun__shvtm = vin__jjy[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        edb__ssbay['database'] = wwpun__shvtm
        if schema:
            edb__ssbay['schema'] = schema
    if znl__xdomq.query:
        for uzm__ekap, cwbp__roiak in parse_qsl(znl__xdomq.query):
            edb__ssbay[uzm__ekap] = cwbp__roiak
            if uzm__ekap == 'session_parameters':
                import json
                edb__ssbay[uzm__ekap] = json.loads(cwbp__roiak)
    edb__ssbay['application'] = 'bodo'
    edb__ssbay['login_timeout'] = 5
    try:
        import snowflake.connector
    except ImportError as zzmb__jxq:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**edb__ssbay)
    saqkv__vrlj = os.environ.get('BODO_PLATFORM_WORKSPACE_REGION', None)
    if saqkv__vrlj and bodo.get_rank() == 0:
        saqkv__vrlj = saqkv__vrlj.lower()
        qcvu__fbv = os.environ.get('BODO_PLATFORM_CLOUD_PROVIDER', None)
        if qcvu__fbv is not None:
            qcvu__fbv = qcvu__fbv.lower()
        sayb__uadel = conn.cursor()
        sayb__uadel.execute('select current_region()')
        smov__cbths: pa.Table = sayb__uadel.fetch_arrow_all()
        bhroj__fjhv = smov__cbths[0][0].as_py()
        sayb__uadel.close()
        yxfex__iws = bhroj__fjhv.split('_')
        nvy__wdo = yxfex__iws[0].lower()
        ydpxd__pkeqd = '-'.join(yxfex__iws[1:]).lower()
        if qcvu__fbv and qcvu__fbv != nvy__wdo:
            zkr__aqoh = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are on different cloud providers. '
                 +
                f'The Snowflake warehouse is located on {nvy__wdo}, but the Bodo cluster is located on {qcvu__fbv}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(zkr__aqoh)
        elif saqkv__vrlj != ydpxd__pkeqd:
            zkr__aqoh = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are in different cloud regions. '
                 +
                f'The Snowflake warehouse is located in {ydpxd__pkeqd}, but the Bodo cluster is located in {saqkv__vrlj}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(zkr__aqoh)
    ppgs__tik.finalize()
    return conn


def get_schema_from_metadata(cursor: 'SnowflakeCursor', sql_query: str,
    is_select_query: bool) ->Tuple[List[pa.Field], List, List[int], List[pa
    .DataType]]:
    qlfdd__jlp = cursor.describe(sql_query)
    tz: str = cursor._timezone
    dtb__yqpr: List[pa.Field] = []
    blsmf__vjmxb: List[str] = []
    olk__lmzh: List[int] = []
    for mlos__hjfjs, pqdp__rzx in enumerate(qlfdd__jlp):
        jyoct__bmrzc = TYPE_CODE_TO_ARROW_TYPE[pqdp__rzx.type_code](pqdp__rzx,
            tz)
        dtb__yqpr.append(pa.field(pqdp__rzx.name, jyoct__bmrzc, pqdp__rzx.
            is_nullable))
        if pa.types.is_int64(jyoct__bmrzc):
            blsmf__vjmxb.append(pqdp__rzx.name)
            olk__lmzh.append(mlos__hjfjs)
    if is_select_query and len(blsmf__vjmxb) != 0:
        kvoz__ycmn = 'SELECT ' + ', '.join(
            f'SYSTEM$TYPEOF({escape_col_name(x)})' for x in blsmf__vjmxb
            ) + f' FROM ({sql_query}) LIMIT 1'
        lzmga__dzwt = execute_query(cursor, kvoz__ycmn, timeout=
            SF_READ_SCHEMA_PROBE_TIMEOUT)
        if lzmga__dzwt is not None and (ovo__jygwt := lzmga__dzwt.
            fetch_arrow_all()) is not None:
            for mlos__hjfjs, (tusar__qugsr, toqo__noke) in enumerate(ovo__jygwt
                .to_pylist()[0].items()):
                uapa__eec = blsmf__vjmxb[mlos__hjfjs]
                vfj__eick = (f'SYSTEM$TYPEOF({escape_col_name(uapa__eec)})',
                    f'SYSTEM$TYPEOF({escape_col_name(uapa__eec.upper())})')
                assert tusar__qugsr in vfj__eick, 'Output of Snowflake Schema Probe Query Uses Unexpected Column Names'
                ztprh__myhzv = olk__lmzh[mlos__hjfjs]
                gqiel__fntiq = int(toqo__noke[-2])
                csxjy__rxkfn = INT_BITSIZE_TO_ARROW_DATATYPE[gqiel__fntiq]
                dtb__yqpr[ztprh__myhzv] = dtb__yqpr[ztprh__myhzv].with_type(
                    csxjy__rxkfn)
    ptb__ynwdh = []
    qou__iwfz = []
    gxe__clud = []
    for mlos__hjfjs, sfbxb__dykl in enumerate(dtb__yqpr):
        jyoct__bmrzc, bqb__chidf = _get_numba_typ_from_pa_typ(sfbxb__dykl, 
            False, sfbxb__dykl.nullable, None)
        ptb__ynwdh.append(jyoct__bmrzc)
        if not bqb__chidf:
            qou__iwfz.append(mlos__hjfjs)
            gxe__clud.append(sfbxb__dykl.type)
    return dtb__yqpr, ptb__ynwdh, qou__iwfz, gxe__clud


def get_schema(conn_str: str, sql_query: str, is_select_query: bool,
    _bodo_read_as_dict: Optional[List[str]]):
    conn = snowflake_connect(conn_str)
    cursor = conn.cursor()
    bxwa__lxp, ptb__ynwdh, qou__iwfz, gxe__clud = get_schema_from_metadata(
        cursor, sql_query, is_select_query)
    pxjz__ydjv = _bodo_read_as_dict if _bodo_read_as_dict else []
    ediw__koqc = {}
    for mlos__hjfjs, scqkf__pmqx in enumerate(ptb__ynwdh):
        if scqkf__pmqx == string_array_type:
            ediw__koqc[bxwa__lxp[mlos__hjfjs].name] = mlos__hjfjs
    mkzc__gzvg = {(orev__dgb.lower() if orev__dgb.isupper() else orev__dgb):
        orev__dgb for orev__dgb in ediw__koqc.keys()}
    yttr__llzoe = pxjz__ydjv - mkzc__gzvg.keys()
    if len(yttr__llzoe) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {yttr__llzoe}'
                ))
    nuq__rgsow = mkzc__gzvg.keys() & pxjz__ydjv
    for orev__dgb in nuq__rgsow:
        ptb__ynwdh[ediw__koqc[mkzc__gzvg[orev__dgb]]] = dict_str_arr_type
    hwb__clzf, wtbio__qufp = [], []
    faa__kbo = mkzc__gzvg.keys() - pxjz__ydjv
    for orev__dgb in faa__kbo:
        hwb__clzf.append(f'count (distinct "{mkzc__gzvg[orev__dgb]}")')
        wtbio__qufp.append(ediw__koqc[mkzc__gzvg[orev__dgb]])
    wlkm__oca: Optional[Tuple[int, List[str]]] = None
    if len(hwb__clzf) != 0 and SF_READ_AUTO_DICT_ENCODE_ENABLED:
        fzc__oibh = max(SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT // len(
            hwb__clzf), 1)
        ntwyc__nlnez = (
            f"select count(*),{', '.join(hwb__clzf)}from ( select * from ({sql_query}) limit {fzc__oibh} ) SAMPLE (1)"
            )
        ntnv__qpt = execute_query(cursor, ntwyc__nlnez, timeout=
            SF_READ_DICT_ENCODING_PROBE_TIMEOUT)
        if ntnv__qpt is None:
            wlkm__oca = fzc__oibh, hwb__clzf
            if SF_READ_DICT_ENCODING_IF_TIMEOUT:
                for mlos__hjfjs in wtbio__qufp:
                    ptb__ynwdh[mlos__hjfjs] = dict_str_arr_type
        else:
            pwomf__mezy: pa.Table = ntnv__qpt.fetch_arrow_all()
            sso__inc = pwomf__mezy[0][0].as_py()
            ntdlt__lkdou = [(pwomf__mezy[mlos__hjfjs][0].as_py() / max(
                sso__inc, 1)) for mlos__hjfjs in range(1, len(hwb__clzf) + 1)]
            kwhkt__bef = filter(lambda x: x[0] <=
                SF_READ_DICT_ENCODE_CRITERION, zip(ntdlt__lkdou, wtbio__qufp))
            for _, mude__dwt in kwhkt__bef:
                ptb__ynwdh[mude__dwt] = dict_str_arr_type
    ybav__fpnx: List[str] = []
    hhzjw__zon = set()
    for x in bxwa__lxp:
        if x.name.isupper():
            hhzjw__zon.add(x.name.lower())
            ybav__fpnx.append(x.name.lower())
        else:
            ybav__fpnx.append(x.name)
    qbg__atoyf = DataFrameType(data=tuple(ptb__ynwdh), columns=tuple(
        ybav__fpnx))
    return qbg__atoyf, hhzjw__zon, qou__iwfz, gxe__clud, pa.schema(bxwa__lxp
        ), wlkm__oca


class SnowflakeDataset(object):

    def __init__(self, batches: List['ResultBatch'], schema, conn:
        'SnowflakeConnection'):
        self.pieces = batches
        self._bodo_total_rows = 0
        for mlbs__oher in batches:
            mlbs__oher._bodo_num_rows = mlbs__oher.rowcount
            self._bodo_total_rows += mlbs__oher._bodo_num_rows
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
        klbs__bvmsb = []
        for deqsz__rbnv in self._json_batch.create_iter():
            klbs__bvmsb.append({self._schema.names[mlos__hjfjs]: ruqo__hvv for
                mlos__hjfjs, ruqo__hvv in enumerate(deqsz__rbnv)})
        ncoz__jrkz = pa.Table.from_pylist(klbs__bvmsb, schema=self._schema)
        return ncoz__jrkz


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
    except ImportError as zzmb__jxq:
        raise BodoError(
            "Snowflake Python connector packages not found. Fetching data from Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    ppgs__tik = tracing.Event('get_snowflake_dataset', is_parallel=is_parallel)
    bvci__xgtw = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    ufa__esma = -1
    batches = []
    if only_fetch_length and is_select_query:
        if bodo.get_rank() == 0 or is_independent:
            sayb__uadel = conn.cursor()
            wnety__hgvdn = tracing.Event('execute_length_query',
                is_parallel=False)
            sayb__uadel.execute(query)
            smov__cbths = sayb__uadel.fetch_arrow_all()
            ufa__esma = smov__cbths[0][0].as_py()
            sayb__uadel.close()
            wnety__hgvdn.finalize()
        if not is_independent:
            ufa__esma = bvci__xgtw.bcast(ufa__esma)
    else:
        if bodo.get_rank() == 0 or is_independent:
            sayb__uadel = conn.cursor()
            wnety__hgvdn = tracing.Event('execute_query', is_parallel=False)
            sayb__uadel = conn.cursor()
            sayb__uadel.execute(query)
            wnety__hgvdn.finalize()
            ufa__esma: int = sayb__uadel.rowcount
            batches: 'List[ResultBatch]' = sayb__uadel.get_result_batches()
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
            sayb__uadel.close()
        if not is_independent:
            ufa__esma, batches, schema = bvci__xgtw.bcast((ufa__esma,
                batches, schema))
    queo__iroja = SnowflakeDataset(batches, schema, conn)
    ppgs__tik.finalize()
    return queo__iroja, ufa__esma


def create_internal_stage(cursor: 'SnowflakeCursor', is_temporary: bool=False
    ) ->str:
    ppgs__tik = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as zzmb__jxq:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = ''
    jlj__wfjoa = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                tfo__rco = 'CREATE TEMPORARY STAGE'
            else:
                tfo__rco = 'CREATE STAGE'
            ptph__upw = (
                f'{tfo__rco} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(ptph__upw, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as msp__ykit:
            if msp__ykit.msg is not None and msp__ykit.msg.endswith(
                'already exists.'):
                continue
            jlj__wfjoa = msp__ykit.msg
            break
    ppgs__tik.finalize()
    if jlj__wfjoa is not None:
        raise snowflake.connector.ProgrammingError(jlj__wfjoa)
    return stage_name


def drop_internal_stage(cursor: 'SnowflakeCursor', stage_name: str):
    ppgs__tik = tracing.Event('drop_internal_stage', is_parallel=False)
    kwd__iain = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(kwd__iain, _is_internal=True)
    ppgs__tik.finalize()


def do_upload_and_cleanup(cursor: 'SnowflakeCursor', chunk_idx: int,
    chunk_path: str, stage_name: str):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        hcz__gda = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        sytsh__fgz = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(sytsh__fgz, _is_internal=True).fetchall()
        hcz__gda.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        klov__nscj = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        klov__nscj.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        klov__nscj = None
    return klov__nscj


def create_table_handle_exists(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str):
    ppgs__tik = tracing.Event('create_table_if_not_exists', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as zzmb__jxq:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    if if_exists == 'fail':
        cnsem__prvz = 'CREATE TABLE'
    elif if_exists == 'replace':
        cnsem__prvz = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        cnsem__prvz = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    slhq__mvh = tracing.Event('create_table', is_parallel=False)
    dwxcl__mby = ', '.join([f'"{ofsv__dqr}" {sf_schema[ofsv__dqr]}' for
        ofsv__dqr in sf_schema.keys()])
    vmnha__cyq = (
        f'{cnsem__prvz} {location} ({dwxcl__mby}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(vmnha__cyq, _is_internal=True)
    slhq__mvh.finalize()
    ppgs__tik.finalize()


def execute_copy_into(cursor: 'SnowflakeCursor', stage_name: str, location:
    str, sf_schema):
    ppgs__tik = tracing.Event('execute_copy_into', is_parallel=False)
    vek__jqgu = ','.join([f'"{ofsv__dqr}"' for ofsv__dqr in sf_schema.keys()])
    iqj__vjb = {ofsv__dqr: ('::binary' if sf_schema[ofsv__dqr] == 'BINARY' else
        '::string' if sf_schema[ofsv__dqr].startswith('TIME') else '') for
        ofsv__dqr in sf_schema.keys()}
    nksn__ompw = ','.join([f'$1:"{ofsv__dqr}"{iqj__vjb[ofsv__dqr]}' for
        ofsv__dqr in sf_schema.keys()])
    huhqv__lkp = (
        f'COPY INTO {location} ({vek__jqgu}) FROM (SELECT {nksn__ompw} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO BINARY_AS_TEXT=False) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    gpyic__aing = cursor.execute(huhqv__lkp, _is_internal=True).fetchall()
    fzkqy__ynla = sum(1 if kfc__dexqg[1] == 'LOADED' else 0 for kfc__dexqg in
        gpyic__aing)
    rbpyl__ffa = len(gpyic__aing)
    ixjr__veuq = sum(int(kfc__dexqg[3]) for kfc__dexqg in gpyic__aing)
    mxxjf__ssmof = fzkqy__ynla, rbpyl__ffa, ixjr__veuq, gpyic__aing
    ppgs__tik.add_attribute('copy_into_nsuccess', fzkqy__ynla)
    ppgs__tik.add_attribute('copy_into_nchunks', rbpyl__ffa)
    ppgs__tik.add_attribute('copy_into_nrows', ixjr__veuq)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(gpyic__aing)}')
    ppgs__tik.finalize()
    return mxxjf__ssmof


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except (ImportError, AttributeError) as zzmb__jxq:
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
    ppgs__tik = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    ngzei__xwsum = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    ngzei__xwsum = ngzei__xwsum.replace('\\', '\\\\').replace("'", "\\'")
    sytsh__fgz = (
        f'PUT \'file://{ngzei__xwsum}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    cnco__mjtqo = cursor._execute_helper(sytsh__fgz, is_internal=True)
    ppgs__tik.finalize()
    return cnco__mjtqo


def connect_and_get_upload_info(conn_str: str):
    ppgs__tik = tracing.Event('connect_and_get_upload_info')
    bvci__xgtw = MPI.COMM_WORLD
    sbrpj__zzeq = bvci__xgtw.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    vyyeu__jnn = ''
    mxob__hcbby = {}
    old_creds = {}
    old_core_site = ''
    bqrz__ckd = ''
    old_sas_token = ''
    shs__isifd = None
    if sbrpj__zzeq == 0:
        try:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                vyyeu__jnn = ''
            else:
                cnco__mjtqo = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                rdlyl__iixg = cnco__mjtqo['data']['uploadInfo']
                mvomv__xni = rdlyl__iixg.get('locationType', 'UNKNOWN')
                dzll__qvkzg = False
                if mvomv__xni == 'S3':
                    lpn__cwj, _, cnc__nha = rdlyl__iixg['location'].partition(
                        '/')
                    cnc__nha = cnc__nha.rstrip('/')
                    vyyeu__jnn = f's3://{lpn__cwj}/{cnc__nha}/'
                    mxob__hcbby = {'AWS_ACCESS_KEY_ID': rdlyl__iixg['creds'
                        ]['AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY':
                        rdlyl__iixg['creds']['AWS_SECRET_KEY'],
                        'AWS_SESSION_TOKEN': rdlyl__iixg['creds'][
                        'AWS_TOKEN'], 'AWS_DEFAULT_REGION': rdlyl__iixg[
                        'region']}
                elif mvomv__xni == 'AZURE':
                    diuo__rcaz = False
                    try:
                        import bodo_azurefs_sas_token_provider
                        diuo__rcaz = True
                    except ImportError as zzmb__jxq:
                        pass
                    iydxr__bbl = len(os.environ.get('HADOOP_HOME', '')
                        ) > 0 and len(os.environ.get('ARROW_LIBHDFS_DIR', '')
                        ) > 0 and len(os.environ.get('CLASSPATH', '')) > 0
                    if diuo__rcaz and iydxr__bbl:
                        nkp__wqg, _, cnc__nha = rdlyl__iixg['location'
                            ].partition('/')
                        cnc__nha = cnc__nha.rstrip('/')
                        bcio__hourx = rdlyl__iixg['storageAccount']
                        bqrz__ckd = rdlyl__iixg['creds']['AZURE_SAS_TOKEN'
                            ].lstrip('?')
                        if len(cnc__nha) == 0:
                            vyyeu__jnn = (
                                f'abfs://{nkp__wqg}@{bcio__hourx}.dfs.core.windows.net/'
                                )
                        else:
                            vyyeu__jnn = (
                                f'abfs://{nkp__wqg}@{bcio__hourx}.dfs.core.windows.net/{cnc__nha}/'
                                )
                        if not 'BODO_PLATFORM_WORKSPACE_UUID' in os.environ:
                            warnings.warn(BodoWarning(
                                """Detected Azure Stage. Bodo will try to upload to the stage directly. If this fails, there might be issues with your Hadoop configuration and you may need to use the PUT method instead by setting
import bodo
bodo.io.snowflake.SF_WRITE_UPLOAD_USING_PUT = True
before calling this function."""
                                ))
                    else:
                        dzll__qvkzg = True
                        evfok__jze = 'Detected Azure Stage. '
                        if not diuo__rcaz:
                            evfok__jze += """Required package bodo_azurefs_sas_token_provider is not installed. To use direct upload to stage in the future, install the package using: 'conda install bodo-azurefs-sas-token-provider -c bodo.ai -c conda-forge'.
"""
                        if not iydxr__bbl:
                            evfok__jze += """You need to download and set up Hadoop. For more information, refer to our documentation: https://docs.bodo.ai/latest/file_io/?h=hdfs#HDFS.
"""
                        evfok__jze += (
                            'Falling back to PUT command for upload for now.')
                        warnings.warn(BodoWarning(evfok__jze))
                else:
                    dzll__qvkzg = True
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{mvomv__xni}'. Falling back to PUT command for upload."
                        ))
                if dzll__qvkzg:
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as kfc__dexqg:
            shs__isifd = RuntimeError(str(kfc__dexqg))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, kfc__dexqg,
                    kfc__dexqg.__traceback__)))
    shs__isifd = bvci__xgtw.bcast(shs__isifd)
    if isinstance(shs__isifd, Exception):
        raise shs__isifd
    vyyeu__jnn = bvci__xgtw.bcast(vyyeu__jnn)
    azure_stage_direct_upload = vyyeu__jnn.startswith('abfs://')
    if vyyeu__jnn == '':
        iwsxb__lvnq = True
        vyyeu__jnn = tmp_folder.name + '/'
        if sbrpj__zzeq != 0:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
    else:
        iwsxb__lvnq = False
        mxob__hcbby = bvci__xgtw.bcast(mxob__hcbby)
        old_creds = update_env_vars(mxob__hcbby)
        if azure_stage_direct_upload:
            import bodo_azurefs_sas_token_provider
            bodo.HDFS_CORE_SITE_LOC_DIR.initialize()
            old_core_site = update_file_contents(bodo.HDFS_CORE_SITE_LOC,
                SF_AZURE_WRITE_HDFS_CORE_SITE)
            bqrz__ckd = bvci__xgtw.bcast(bqrz__ckd)
            old_sas_token = update_file_contents(
                SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION, bqrz__ckd)
    stage_name = bvci__xgtw.bcast(stage_name)
    ppgs__tik.finalize()
    return (cursor, tmp_folder, stage_name, vyyeu__jnn, iwsxb__lvnq,
        old_creds, azure_stage_direct_upload, old_core_site, old_sas_token)


def create_table_copy_into(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str, old_creds, tmp_folder:
    TemporaryDirectory, azure_stage_direct_upload: bool, old_core_site: str,
    old_sas_token: str):
    ppgs__tik = tracing.Event('create_table_copy_into', is_parallel=False)
    bvci__xgtw = MPI.COMM_WORLD
    sbrpj__zzeq = bvci__xgtw.Get_rank()
    shs__isifd = None
    if sbrpj__zzeq == 0:
        try:
            hpnf__arcia = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(hpnf__arcia)
            create_table_handle_exists(cursor, stage_name, location,
                sf_schema, if_exists)
            fzkqy__ynla, rbpyl__ffa, ixjr__veuq, qza__rpilo = (
                execute_copy_into(cursor, stage_name, location, sf_schema))
            if fzkqy__ynla != rbpyl__ffa:
                raise BodoError(
                    f'Snowflake write copy_into failed: {qza__rpilo}')
            ldgk__rivg = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(ldgk__rivg)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as kfc__dexqg:
            shs__isifd = RuntimeError(str(kfc__dexqg))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, kfc__dexqg,
                    kfc__dexqg.__traceback__)))
    shs__isifd = bvci__xgtw.bcast(shs__isifd)
    if isinstance(shs__isifd, Exception):
        raise shs__isifd
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    if azure_stage_direct_upload:
        update_file_contents(bodo.HDFS_CORE_SITE_LOC, old_core_site)
        update_file_contents(SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION,
            old_sas_token)
    ppgs__tik.finalize()
