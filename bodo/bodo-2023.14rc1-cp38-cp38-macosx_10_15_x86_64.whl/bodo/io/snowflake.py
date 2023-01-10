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
    for col_name, tjsmm__ljrz in zip(column_names, column_datatypes):
        if isinstance(tjsmm__ljrz, bodo.DatetimeArrayType
            ) or tjsmm__ljrz == bodo.datetime_datetime_type:
            sf_schema[col_name] = 'TIMESTAMP_NTZ'
        elif tjsmm__ljrz == bodo.datetime_date_array_type:
            sf_schema[col_name] = 'DATE'
        elif isinstance(tjsmm__ljrz, bodo.TimeArrayType):
            if tjsmm__ljrz.precision in [0, 3, 6]:
                cvoso__rdk = tjsmm__ljrz.precision
            elif tjsmm__ljrz.precision == 9:
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"""to_sql(): {col_name} time precision will be lost.
Snowflake loses nano second precision when exporting parquet file using COPY INTO.
 This is due to a limitation on Parquet V1 that is currently being used in Snowflake"""
                        ))
                cvoso__rdk = 6
            else:
                raise ValueError(
                    'Unsupported Precision Found in Bodo Time Array')
            sf_schema[col_name] = f'TIME({cvoso__rdk})'
        elif isinstance(tjsmm__ljrz, types.Array):
            mkrwz__uac = tjsmm__ljrz.dtype.name
            if mkrwz__uac.startswith('datetime'):
                sf_schema[col_name] = 'DATETIME'
            if mkrwz__uac.startswith('timedelta'):
                sf_schema[col_name] = 'NUMBER(38, 0)'
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"to_sql(): {col_name} with type 'timedelta' will be written as integer values (ns frequency) to the database."
                        ))
            elif mkrwz__uac.startswith(('int', 'uint')):
                sf_schema[col_name] = 'NUMBER(38, 0)'
            elif mkrwz__uac.startswith('float'):
                sf_schema[col_name] = 'REAL'
        elif is_str_arr_type(tjsmm__ljrz):
            sf_schema[col_name] = 'TEXT'
        elif tjsmm__ljrz == bodo.binary_array_type:
            sf_schema[col_name] = 'BINARY'
        elif tjsmm__ljrz == bodo.boolean_array:
            sf_schema[col_name] = 'BOOLEAN'
        elif isinstance(tjsmm__ljrz, bodo.IntegerArrayType):
            sf_schema[col_name] = 'NUMBER(38, 0)'
        elif isinstance(tjsmm__ljrz, bodo.FloatingArrayType):
            sf_schema[col_name] = 'REAL'
        elif isinstance(tjsmm__ljrz, bodo.DecimalArrayType):
            sf_schema[col_name] = 'NUMBER(38, 18)'
        elif isinstance(tjsmm__ljrz, (ArrayItemArrayType, StructArrayType)):
            sf_schema[col_name] = 'VARIANT'
        else:
            raise BodoError(
                f'Conversion from Bodo array type {tjsmm__ljrz} to snowflake type for {col_name} not supported yet.'
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
    except snowflake.connector.errors.ProgrammingError as ppy__idmtb:
        if 'SQL execution canceled' in str(ppy__idmtb):
            return None
        else:
            raise


def escape_col_name(col_name: str) ->str:
    return '"{}"'.format(col_name.replace('"', '""'))


def snowflake_connect(conn_str: str, is_parallel: bool=False
    ) ->'SnowflakeConnection':
    zhfo__uwdz = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    azza__yxwl = urlparse(conn_str)
    ukxo__pinx = {}
    if azza__yxwl.username:
        ukxo__pinx['user'] = azza__yxwl.username
    if azza__yxwl.password:
        ukxo__pinx['password'] = azza__yxwl.password
    if azza__yxwl.hostname:
        ukxo__pinx['account'] = azza__yxwl.hostname
    if azza__yxwl.port:
        ukxo__pinx['port'] = azza__yxwl.port
    if azza__yxwl.path:
        qrb__ctvz = azza__yxwl.path
        if qrb__ctvz.startswith('/'):
            qrb__ctvz = qrb__ctvz[1:]
        ggfi__gkog = qrb__ctvz.split('/')
        if len(ggfi__gkog) == 2:
            kamc__jrerv, schema = ggfi__gkog
        elif len(ggfi__gkog) == 1:
            kamc__jrerv = ggfi__gkog[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        ukxo__pinx['database'] = kamc__jrerv
        if schema:
            ukxo__pinx['schema'] = schema
    if azza__yxwl.query:
        for qghj__rjs, mtp__qcuyh in parse_qsl(azza__yxwl.query):
            ukxo__pinx[qghj__rjs] = mtp__qcuyh
            if qghj__rjs == 'session_parameters':
                import json
                ukxo__pinx[qghj__rjs] = json.loads(mtp__qcuyh)
    ukxo__pinx['application'] = 'bodo'
    ukxo__pinx['login_timeout'] = 5
    try:
        import snowflake.connector
    except ImportError as xqlqk__kmcn:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**ukxo__pinx)
    vfeo__jdpbd = os.environ.get('BODO_PLATFORM_WORKSPACE_REGION', None)
    if vfeo__jdpbd and bodo.get_rank() == 0:
        vfeo__jdpbd = vfeo__jdpbd.lower()
        iyhnt__ttpfp = os.environ.get('BODO_PLATFORM_CLOUD_PROVIDER', None)
        if iyhnt__ttpfp is not None:
            iyhnt__ttpfp = iyhnt__ttpfp.lower()
        com__lxdf = conn.cursor()
        com__lxdf.execute('select current_region()')
        ezpky__wue: pa.Table = com__lxdf.fetch_arrow_all()
        cltmg__qga = ezpky__wue[0][0].as_py()
        com__lxdf.close()
        oknth__fwd = cltmg__qga.split('_')
        mdb__jnetu = oknth__fwd[0].lower()
        kdy__xlmw = '-'.join(oknth__fwd[1:]).lower()
        if iyhnt__ttpfp and iyhnt__ttpfp != mdb__jnetu:
            wfpi__aimlj = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are on different cloud providers. '
                 +
                f'The Snowflake warehouse is located on {mdb__jnetu}, but the Bodo cluster is located on {iyhnt__ttpfp}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(wfpi__aimlj)
        elif vfeo__jdpbd != kdy__xlmw:
            wfpi__aimlj = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are in different cloud regions. '
                 +
                f'The Snowflake warehouse is located in {kdy__xlmw}, but the Bodo cluster is located in {vfeo__jdpbd}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(wfpi__aimlj)
    zhfo__uwdz.finalize()
    return conn


def get_schema_from_metadata(cursor: 'SnowflakeCursor', sql_query: str,
    is_select_query: bool) ->Tuple[List[pa.Field], List, List[int], List[pa
    .DataType]]:
    zmon__rlwnt = cursor.describe(sql_query)
    tz: str = cursor._timezone
    xsudh__yfprx: List[pa.Field] = []
    gqk__qts: List[str] = []
    obop__rspw: List[int] = []
    for wcqdo__guo, fmoa__mpd in enumerate(zmon__rlwnt):
        rum__tkyas = TYPE_CODE_TO_ARROW_TYPE[fmoa__mpd.type_code](fmoa__mpd, tz
            )
        xsudh__yfprx.append(pa.field(fmoa__mpd.name, rum__tkyas, fmoa__mpd.
            is_nullable))
        if pa.types.is_int64(rum__tkyas):
            gqk__qts.append(fmoa__mpd.name)
            obop__rspw.append(wcqdo__guo)
    if is_select_query and len(gqk__qts) != 0:
        aqe__oftmi = 'SELECT ' + ', '.join(
            f'SYSTEM$TYPEOF({escape_col_name(x)})' for x in gqk__qts
            ) + f' FROM ({sql_query}) LIMIT 1'
        crzy__afl = execute_query(cursor, aqe__oftmi, timeout=
            SF_READ_SCHEMA_PROBE_TIMEOUT)
        if crzy__afl is not None and (xxy__eufr := crzy__afl.fetch_arrow_all()
            ) is not None:
            for wcqdo__guo, (wqyy__woaha, jol__pngd) in enumerate(xxy__eufr
                .to_pylist()[0].items()):
                rbecf__xik = gqk__qts[wcqdo__guo]
                zwzh__zwl = (
                    f'SYSTEM$TYPEOF({escape_col_name(rbecf__xik)})',
                    f'SYSTEM$TYPEOF({escape_col_name(rbecf__xik.upper())})')
                assert wqyy__woaha in zwzh__zwl, 'Output of Snowflake Schema Probe Query Uses Unexpected Column Names'
                vpuaw__bba = obop__rspw[wcqdo__guo]
                mgtpr__qacy = int(jol__pngd[-2])
                xula__wqsu = INT_BITSIZE_TO_ARROW_DATATYPE[mgtpr__qacy]
                xsudh__yfprx[vpuaw__bba] = xsudh__yfprx[vpuaw__bba].with_type(
                    xula__wqsu)
    jgw__acsz = []
    xqrpn__akk = []
    hzgz__axz = []
    for wcqdo__guo, ncana__gfk in enumerate(xsudh__yfprx):
        rum__tkyas, obl__mrbq = _get_numba_typ_from_pa_typ(ncana__gfk, 
            False, ncana__gfk.nullable, None)
        jgw__acsz.append(rum__tkyas)
        if not obl__mrbq:
            xqrpn__akk.append(wcqdo__guo)
            hzgz__axz.append(ncana__gfk.type)
    return xsudh__yfprx, jgw__acsz, xqrpn__akk, hzgz__axz


def get_schema(conn_str: str, sql_query: str, is_select_query: bool,
    _bodo_read_as_dict: Optional[List[str]]):
    conn = snowflake_connect(conn_str)
    cursor = conn.cursor()
    qxvn__wjltp, jgw__acsz, xqrpn__akk, hzgz__axz = get_schema_from_metadata(
        cursor, sql_query, is_select_query)
    mmoi__rfiug = _bodo_read_as_dict if _bodo_read_as_dict else []
    iojk__wxue = {}
    for wcqdo__guo, rkbja__etm in enumerate(jgw__acsz):
        if rkbja__etm == string_array_type:
            iojk__wxue[qxvn__wjltp[wcqdo__guo].name] = wcqdo__guo
    jsrvc__ojrqq = {(gojnb__dcj.lower() if gojnb__dcj.isupper() else
        gojnb__dcj): gojnb__dcj for gojnb__dcj in iojk__wxue.keys()}
    efmiq__iwb = mmoi__rfiug - jsrvc__ojrqq.keys()
    if len(efmiq__iwb) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {efmiq__iwb}'
                ))
    ixg__rek = jsrvc__ojrqq.keys() & mmoi__rfiug
    for gojnb__dcj in ixg__rek:
        jgw__acsz[iojk__wxue[jsrvc__ojrqq[gojnb__dcj]]] = dict_str_arr_type
    sxvg__kjf, wdkac__pqlhp = [], []
    iahg__srp = jsrvc__ojrqq.keys() - mmoi__rfiug
    for gojnb__dcj in iahg__srp:
        sxvg__kjf.append(f'count (distinct "{jsrvc__ojrqq[gojnb__dcj]}")')
        wdkac__pqlhp.append(iojk__wxue[jsrvc__ojrqq[gojnb__dcj]])
    rrxr__fhgq: Optional[Tuple[int, List[str]]] = None
    if len(sxvg__kjf) != 0 and SF_READ_AUTO_DICT_ENCODE_ENABLED:
        tkyj__oxyhf = max(SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT // len(
            sxvg__kjf), 1)
        hitez__aho = (
            f"select count(*),{', '.join(sxvg__kjf)}from ( select * from ({sql_query}) limit {tkyj__oxyhf} ) SAMPLE (1)"
            )
        joy__yqn = execute_query(cursor, hitez__aho, timeout=
            SF_READ_DICT_ENCODING_PROBE_TIMEOUT)
        if joy__yqn is None:
            rrxr__fhgq = tkyj__oxyhf, sxvg__kjf
            if SF_READ_DICT_ENCODING_IF_TIMEOUT:
                for wcqdo__guo in wdkac__pqlhp:
                    jgw__acsz[wcqdo__guo] = dict_str_arr_type
        else:
            kgqth__qtpc: pa.Table = joy__yqn.fetch_arrow_all()
            aocki__owcsf = kgqth__qtpc[0][0].as_py()
            vph__gbhei = [(kgqth__qtpc[wcqdo__guo][0].as_py() / max(
                aocki__owcsf, 1)) for wcqdo__guo in range(1, len(sxvg__kjf) +
                1)]
            ovl__miodt = filter(lambda x: x[0] <=
                SF_READ_DICT_ENCODE_CRITERION, zip(vph__gbhei, wdkac__pqlhp))
            for _, pigys__mgjb in ovl__miodt:
                jgw__acsz[pigys__mgjb] = dict_str_arr_type
    akm__eopv: List[str] = []
    hkw__hqr = set()
    for x in qxvn__wjltp:
        if x.name.isupper():
            hkw__hqr.add(x.name.lower())
            akm__eopv.append(x.name.lower())
        else:
            akm__eopv.append(x.name)
    lpqmh__royn = DataFrameType(data=tuple(jgw__acsz), columns=tuple(akm__eopv)
        )
    return lpqmh__royn, hkw__hqr, xqrpn__akk, hzgz__axz, pa.schema(qxvn__wjltp
        ), rrxr__fhgq


class SnowflakeDataset(object):

    def __init__(self, batches: List['ResultBatch'], schema, conn:
        'SnowflakeConnection'):
        self.pieces = batches
        self._bodo_total_rows = 0
        for irws__ttym in batches:
            irws__ttym._bodo_num_rows = irws__ttym.rowcount
            self._bodo_total_rows += irws__ttym._bodo_num_rows
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
        uoz__dgp = []
        for luugg__weyp in self._json_batch.create_iter():
            uoz__dgp.append({self._schema.names[wcqdo__guo]: lmb__umo for 
                wcqdo__guo, lmb__umo in enumerate(luugg__weyp)})
        buyee__uygr = pa.Table.from_pylist(uoz__dgp, schema=self._schema)
        return buyee__uygr


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
    except ImportError as xqlqk__kmcn:
        raise BodoError(
            "Snowflake Python connector packages not found. Fetching data from Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    zhfo__uwdz = tracing.Event('get_snowflake_dataset', is_parallel=is_parallel
        )
    myezm__sttdj = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    bmo__alqxa = -1
    batches = []
    if only_fetch_length and is_select_query:
        if bodo.get_rank() == 0 or is_independent:
            com__lxdf = conn.cursor()
            eea__igag = tracing.Event('execute_length_query', is_parallel=False
                )
            com__lxdf.execute(query)
            ezpky__wue = com__lxdf.fetch_arrow_all()
            bmo__alqxa = ezpky__wue[0][0].as_py()
            com__lxdf.close()
            eea__igag.finalize()
        if not is_independent:
            bmo__alqxa = myezm__sttdj.bcast(bmo__alqxa)
    else:
        if bodo.get_rank() == 0 or is_independent:
            com__lxdf = conn.cursor()
            eea__igag = tracing.Event('execute_query', is_parallel=False)
            com__lxdf = conn.cursor()
            com__lxdf.execute(query)
            eea__igag.finalize()
            bmo__alqxa: int = com__lxdf.rowcount
            batches: 'List[ResultBatch]' = com__lxdf.get_result_batches()
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
            com__lxdf.close()
        if not is_independent:
            bmo__alqxa, batches, schema = myezm__sttdj.bcast((bmo__alqxa,
                batches, schema))
    wci__jiwj = SnowflakeDataset(batches, schema, conn)
    zhfo__uwdz.finalize()
    return wci__jiwj, bmo__alqxa


def create_internal_stage(cursor: 'SnowflakeCursor', is_temporary: bool=False
    ) ->str:
    zhfo__uwdz = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as xqlqk__kmcn:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = ''
    ghxe__vyen = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                ejh__sph = 'CREATE TEMPORARY STAGE'
            else:
                ejh__sph = 'CREATE STAGE'
            imw__wpvfd = (
                f'{ejh__sph} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(imw__wpvfd, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as epcr__oqle:
            if epcr__oqle.msg is not None and epcr__oqle.msg.endswith(
                'already exists.'):
                continue
            ghxe__vyen = epcr__oqle.msg
            break
    zhfo__uwdz.finalize()
    if ghxe__vyen is not None:
        raise snowflake.connector.ProgrammingError(ghxe__vyen)
    return stage_name


def drop_internal_stage(cursor: 'SnowflakeCursor', stage_name: str):
    zhfo__uwdz = tracing.Event('drop_internal_stage', is_parallel=False)
    aijh__syg = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(aijh__syg, _is_internal=True)
    zhfo__uwdz.finalize()


def do_upload_and_cleanup(cursor: 'SnowflakeCursor', chunk_idx: int,
    chunk_path: str, stage_name: str):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        byx__fwxj = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        jhzi__xfc = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(jhzi__xfc, _is_internal=True).fetchall()
        byx__fwxj.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        xukvw__bhlua = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        xukvw__bhlua.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        xukvw__bhlua = None
    return xukvw__bhlua


def create_table_handle_exists(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str):
    zhfo__uwdz = tracing.Event('create_table_if_not_exists', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as xqlqk__kmcn:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    if if_exists == 'fail':
        clqoh__zmaxx = 'CREATE TABLE'
    elif if_exists == 'replace':
        clqoh__zmaxx = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        clqoh__zmaxx = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    tqsqd__vhkr = tracing.Event('create_table', is_parallel=False)
    ewyh__whawh = ', '.join([f'"{fgu__gbw}" {sf_schema[fgu__gbw]}' for
        fgu__gbw in sf_schema.keys()])
    chrja__hrzo = (
        f'{clqoh__zmaxx} {location} ({ewyh__whawh}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(chrja__hrzo, _is_internal=True)
    tqsqd__vhkr.finalize()
    zhfo__uwdz.finalize()


def execute_copy_into(cursor: 'SnowflakeCursor', stage_name: str, location:
    str, sf_schema):
    zhfo__uwdz = tracing.Event('execute_copy_into', is_parallel=False)
    rdldf__dece = ','.join([f'"{fgu__gbw}"' for fgu__gbw in sf_schema.keys()])
    pfbg__dmt = {fgu__gbw: ('::binary' if sf_schema[fgu__gbw] == 'BINARY' else
        '::string' if sf_schema[fgu__gbw].startswith('TIME') else '') for
        fgu__gbw in sf_schema.keys()}
    wbnzb__vupv = ','.join([f'$1:"{fgu__gbw}"{pfbg__dmt[fgu__gbw]}' for
        fgu__gbw in sf_schema.keys()])
    yfg__kjmu = (
        f'COPY INTO {location} ({rdldf__dece}) FROM (SELECT {wbnzb__vupv} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO BINARY_AS_TEXT=False) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    cxoh__kcf = cursor.execute(yfg__kjmu, _is_internal=True).fetchall()
    axv__pxzzg = sum(1 if ppy__idmtb[1] == 'LOADED' else 0 for ppy__idmtb in
        cxoh__kcf)
    hhz__tdp = len(cxoh__kcf)
    xun__ctl = sum(int(ppy__idmtb[3]) for ppy__idmtb in cxoh__kcf)
    zkzq__ymaxg = axv__pxzzg, hhz__tdp, xun__ctl, cxoh__kcf
    zhfo__uwdz.add_attribute('copy_into_nsuccess', axv__pxzzg)
    zhfo__uwdz.add_attribute('copy_into_nchunks', hhz__tdp)
    zhfo__uwdz.add_attribute('copy_into_nrows', xun__ctl)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(cxoh__kcf)}')
    zhfo__uwdz.finalize()
    return zkzq__ymaxg


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except (ImportError, AttributeError) as xqlqk__kmcn:
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
    zhfo__uwdz = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    ciujn__xbjbi = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    ciujn__xbjbi = ciujn__xbjbi.replace('\\', '\\\\').replace("'", "\\'")
    jhzi__xfc = (
        f'PUT \'file://{ciujn__xbjbi}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    jcgz__kxff = cursor._execute_helper(jhzi__xfc, is_internal=True)
    zhfo__uwdz.finalize()
    return jcgz__kxff


def connect_and_get_upload_info(conn_str: str):
    zhfo__uwdz = tracing.Event('connect_and_get_upload_info')
    myezm__sttdj = MPI.COMM_WORLD
    xxs__xpgiu = myezm__sttdj.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    joqss__qsxbs = ''
    kwkp__lecs = {}
    old_creds = {}
    old_core_site = ''
    xbw__duffl = ''
    old_sas_token = ''
    unvxi__uysm = None
    if xxs__xpgiu == 0:
        try:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                joqss__qsxbs = ''
            else:
                jcgz__kxff = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                hymv__ndsu = jcgz__kxff['data']['uploadInfo']
                tsr__vre = hymv__ndsu.get('locationType', 'UNKNOWN')
                coxd__skuk = False
                if tsr__vre == 'S3':
                    qndda__pvu, _, qrb__ctvz = hymv__ndsu['location'
                        ].partition('/')
                    qrb__ctvz = qrb__ctvz.rstrip('/')
                    joqss__qsxbs = f's3://{qndda__pvu}/{qrb__ctvz}/'
                    kwkp__lecs = {'AWS_ACCESS_KEY_ID': hymv__ndsu['creds'][
                        'AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY': hymv__ndsu[
                        'creds']['AWS_SECRET_KEY'], 'AWS_SESSION_TOKEN':
                        hymv__ndsu['creds']['AWS_TOKEN'],
                        'AWS_DEFAULT_REGION': hymv__ndsu['region']}
                elif tsr__vre == 'AZURE':
                    wgqme__fls = False
                    try:
                        import bodo_azurefs_sas_token_provider
                        wgqme__fls = True
                    except ImportError as xqlqk__kmcn:
                        pass
                    fdp__mkp = len(os.environ.get('HADOOP_HOME', '')
                        ) > 0 and len(os.environ.get('ARROW_LIBHDFS_DIR', '')
                        ) > 0 and len(os.environ.get('CLASSPATH', '')) > 0
                    if wgqme__fls and fdp__mkp:
                        tct__tyvks, _, qrb__ctvz = hymv__ndsu['location'
                            ].partition('/')
                        qrb__ctvz = qrb__ctvz.rstrip('/')
                        hgob__feg = hymv__ndsu['storageAccount']
                        xbw__duffl = hymv__ndsu['creds']['AZURE_SAS_TOKEN'
                            ].lstrip('?')
                        if len(qrb__ctvz) == 0:
                            joqss__qsxbs = (
                                f'abfs://{tct__tyvks}@{hgob__feg}.dfs.core.windows.net/'
                                )
                        else:
                            joqss__qsxbs = (
                                f'abfs://{tct__tyvks}@{hgob__feg}.dfs.core.windows.net/{qrb__ctvz}/'
                                )
                        if not 'BODO_PLATFORM_WORKSPACE_UUID' in os.environ:
                            warnings.warn(BodoWarning(
                                """Detected Azure Stage. Bodo will try to upload to the stage directly. If this fails, there might be issues with your Hadoop configuration and you may need to use the PUT method instead by setting
import bodo
bodo.io.snowflake.SF_WRITE_UPLOAD_USING_PUT = True
before calling this function."""
                                ))
                    else:
                        coxd__skuk = True
                        gmqqo__ggsh = 'Detected Azure Stage. '
                        if not wgqme__fls:
                            gmqqo__ggsh += """Required package bodo_azurefs_sas_token_provider is not installed. To use direct upload to stage in the future, install the package using: 'conda install bodo-azurefs-sas-token-provider -c bodo.ai -c conda-forge'.
"""
                        if not fdp__mkp:
                            gmqqo__ggsh += """You need to download and set up Hadoop. For more information, refer to our documentation: https://docs.bodo.ai/latest/file_io/?h=hdfs#HDFS.
"""
                        gmqqo__ggsh += (
                            'Falling back to PUT command for upload for now.')
                        warnings.warn(BodoWarning(gmqqo__ggsh))
                else:
                    coxd__skuk = True
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{tsr__vre}'. Falling back to PUT command for upload."
                        ))
                if coxd__skuk:
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as ppy__idmtb:
            unvxi__uysm = RuntimeError(str(ppy__idmtb))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, ppy__idmtb,
                    ppy__idmtb.__traceback__)))
    unvxi__uysm = myezm__sttdj.bcast(unvxi__uysm)
    if isinstance(unvxi__uysm, Exception):
        raise unvxi__uysm
    joqss__qsxbs = myezm__sttdj.bcast(joqss__qsxbs)
    azure_stage_direct_upload = joqss__qsxbs.startswith('abfs://')
    if joqss__qsxbs == '':
        jay__gdo = True
        joqss__qsxbs = tmp_folder.name + '/'
        if xxs__xpgiu != 0:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
    else:
        jay__gdo = False
        kwkp__lecs = myezm__sttdj.bcast(kwkp__lecs)
        old_creds = update_env_vars(kwkp__lecs)
        if azure_stage_direct_upload:
            import bodo_azurefs_sas_token_provider
            bodo.HDFS_CORE_SITE_LOC_DIR.initialize()
            old_core_site = update_file_contents(bodo.HDFS_CORE_SITE_LOC,
                SF_AZURE_WRITE_HDFS_CORE_SITE)
            xbw__duffl = myezm__sttdj.bcast(xbw__duffl)
            old_sas_token = update_file_contents(
                SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION, xbw__duffl)
    stage_name = myezm__sttdj.bcast(stage_name)
    zhfo__uwdz.finalize()
    return (cursor, tmp_folder, stage_name, joqss__qsxbs, jay__gdo,
        old_creds, azure_stage_direct_upload, old_core_site, old_sas_token)


def create_table_copy_into(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str, old_creds, tmp_folder:
    TemporaryDirectory, azure_stage_direct_upload: bool, old_core_site: str,
    old_sas_token: str):
    zhfo__uwdz = tracing.Event('create_table_copy_into', is_parallel=False)
    myezm__sttdj = MPI.COMM_WORLD
    xxs__xpgiu = myezm__sttdj.Get_rank()
    unvxi__uysm = None
    if xxs__xpgiu == 0:
        try:
            aievz__pcx = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(aievz__pcx)
            create_table_handle_exists(cursor, stage_name, location,
                sf_schema, if_exists)
            axv__pxzzg, hhz__tdp, xun__ctl, njzbc__rmc = execute_copy_into(
                cursor, stage_name, location, sf_schema)
            if axv__pxzzg != hhz__tdp:
                raise BodoError(
                    f'Snowflake write copy_into failed: {njzbc__rmc}')
            qtv__yegj = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(qtv__yegj)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as ppy__idmtb:
            unvxi__uysm = RuntimeError(str(ppy__idmtb))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, ppy__idmtb,
                    ppy__idmtb.__traceback__)))
    unvxi__uysm = myezm__sttdj.bcast(unvxi__uysm)
    if isinstance(unvxi__uysm, Exception):
        raise unvxi__uysm
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    if azure_stage_direct_upload:
        update_file_contents(bodo.HDFS_CORE_SITE_LOC, old_core_site)
        update_file_contents(SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION,
            old_sas_token)
    zhfo__uwdz.finalize()
