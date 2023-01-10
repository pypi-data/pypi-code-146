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
    for col_name, hivtw__lmhll in zip(column_names, column_datatypes):
        if isinstance(hivtw__lmhll, bodo.DatetimeArrayType
            ) or hivtw__lmhll == bodo.datetime_datetime_type:
            sf_schema[col_name] = 'TIMESTAMP_NTZ'
        elif hivtw__lmhll == bodo.datetime_date_array_type:
            sf_schema[col_name] = 'DATE'
        elif isinstance(hivtw__lmhll, bodo.TimeArrayType):
            if hivtw__lmhll.precision in [0, 3, 6]:
                mzdke__legmk = hivtw__lmhll.precision
            elif hivtw__lmhll.precision == 9:
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"""to_sql(): {col_name} time precision will be lost.
Snowflake loses nano second precision when exporting parquet file using COPY INTO.
 This is due to a limitation on Parquet V1 that is currently being used in Snowflake"""
                        ))
                mzdke__legmk = 6
            else:
                raise ValueError(
                    'Unsupported Precision Found in Bodo Time Array')
            sf_schema[col_name] = f'TIME({mzdke__legmk})'
        elif isinstance(hivtw__lmhll, types.Array):
            tlw__tkg = hivtw__lmhll.dtype.name
            if tlw__tkg.startswith('datetime'):
                sf_schema[col_name] = 'DATETIME'
            if tlw__tkg.startswith('timedelta'):
                sf_schema[col_name] = 'NUMBER(38, 0)'
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"to_sql(): {col_name} with type 'timedelta' will be written as integer values (ns frequency) to the database."
                        ))
            elif tlw__tkg.startswith(('int', 'uint')):
                sf_schema[col_name] = 'NUMBER(38, 0)'
            elif tlw__tkg.startswith('float'):
                sf_schema[col_name] = 'REAL'
        elif is_str_arr_type(hivtw__lmhll):
            sf_schema[col_name] = 'TEXT'
        elif hivtw__lmhll == bodo.binary_array_type:
            sf_schema[col_name] = 'BINARY'
        elif hivtw__lmhll == bodo.boolean_array:
            sf_schema[col_name] = 'BOOLEAN'
        elif isinstance(hivtw__lmhll, bodo.IntegerArrayType):
            sf_schema[col_name] = 'NUMBER(38, 0)'
        elif isinstance(hivtw__lmhll, bodo.FloatingArrayType):
            sf_schema[col_name] = 'REAL'
        elif isinstance(hivtw__lmhll, bodo.DecimalArrayType):
            sf_schema[col_name] = 'NUMBER(38, 18)'
        elif isinstance(hivtw__lmhll, (ArrayItemArrayType, StructArrayType)):
            sf_schema[col_name] = 'VARIANT'
        else:
            raise BodoError(
                f'Conversion from Bodo array type {hivtw__lmhll} to snowflake type for {col_name} not supported yet.'
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
    except snowflake.connector.errors.ProgrammingError as yas__ooiek:
        if 'SQL execution canceled' in str(yas__ooiek):
            return None
        else:
            raise


def escape_col_name(col_name: str) ->str:
    return '"{}"'.format(col_name.replace('"', '""'))


def snowflake_connect(conn_str: str, is_parallel: bool=False
    ) ->'SnowflakeConnection':
    dnyxb__qjqz = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    iekag__mhqae = urlparse(conn_str)
    jfpr__tzfs = {}
    if iekag__mhqae.username:
        jfpr__tzfs['user'] = iekag__mhqae.username
    if iekag__mhqae.password:
        jfpr__tzfs['password'] = iekag__mhqae.password
    if iekag__mhqae.hostname:
        jfpr__tzfs['account'] = iekag__mhqae.hostname
    if iekag__mhqae.port:
        jfpr__tzfs['port'] = iekag__mhqae.port
    if iekag__mhqae.path:
        hol__apz = iekag__mhqae.path
        if hol__apz.startswith('/'):
            hol__apz = hol__apz[1:]
        bgyhd__nrnb = hol__apz.split('/')
        if len(bgyhd__nrnb) == 2:
            iegs__xev, schema = bgyhd__nrnb
        elif len(bgyhd__nrnb) == 1:
            iegs__xev = bgyhd__nrnb[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        jfpr__tzfs['database'] = iegs__xev
        if schema:
            jfpr__tzfs['schema'] = schema
    if iekag__mhqae.query:
        for wob__ukha, biw__vhct in parse_qsl(iekag__mhqae.query):
            jfpr__tzfs[wob__ukha] = biw__vhct
            if wob__ukha == 'session_parameters':
                import json
                jfpr__tzfs[wob__ukha] = json.loads(biw__vhct)
    jfpr__tzfs['application'] = 'bodo'
    jfpr__tzfs['login_timeout'] = 5
    try:
        import snowflake.connector
    except ImportError as upli__rll:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**jfpr__tzfs)
    tsa__vow = os.environ.get('BODO_PLATFORM_WORKSPACE_REGION', None)
    if tsa__vow and bodo.get_rank() == 0:
        tsa__vow = tsa__vow.lower()
        gfoc__fubkn = os.environ.get('BODO_PLATFORM_CLOUD_PROVIDER', None)
        if gfoc__fubkn is not None:
            gfoc__fubkn = gfoc__fubkn.lower()
        mqg__dla = conn.cursor()
        mqg__dla.execute('select current_region()')
        mhd__jip: pa.Table = mqg__dla.fetch_arrow_all()
        bpd__pcwz = mhd__jip[0][0].as_py()
        mqg__dla.close()
        ifzgh__sob = bpd__pcwz.split('_')
        ixjym__prios = ifzgh__sob[0].lower()
        jvs__rckvu = '-'.join(ifzgh__sob[1:]).lower()
        if gfoc__fubkn and gfoc__fubkn != ixjym__prios:
            kkfjk__qjn = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are on different cloud providers. '
                 +
                f'The Snowflake warehouse is located on {ixjym__prios}, but the Bodo cluster is located on {gfoc__fubkn}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(kkfjk__qjn)
        elif tsa__vow != jvs__rckvu:
            kkfjk__qjn = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are in different cloud regions. '
                 +
                f'The Snowflake warehouse is located in {jvs__rckvu}, but the Bodo cluster is located in {tsa__vow}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(kkfjk__qjn)
    dnyxb__qjqz.finalize()
    return conn


def get_schema_from_metadata(cursor: 'SnowflakeCursor', sql_query: str,
    is_select_query: bool) ->Tuple[List[pa.Field], List, List[int], List[pa
    .DataType]]:
    hdx__ymtj = cursor.describe(sql_query)
    tz: str = cursor._timezone
    nbbf__nut: List[pa.Field] = []
    qtegn__ptxqp: List[str] = []
    jpmxr__wxcc: List[int] = []
    for hcgd__jre, bxtz__drm in enumerate(hdx__ymtj):
        gfpg__afs = TYPE_CODE_TO_ARROW_TYPE[bxtz__drm.type_code](bxtz__drm, tz)
        nbbf__nut.append(pa.field(bxtz__drm.name, gfpg__afs, bxtz__drm.
            is_nullable))
        if pa.types.is_int64(gfpg__afs):
            qtegn__ptxqp.append(bxtz__drm.name)
            jpmxr__wxcc.append(hcgd__jre)
    if is_select_query and len(qtegn__ptxqp) != 0:
        ojw__rdtjv = 'SELECT ' + ', '.join(
            f'SYSTEM$TYPEOF({escape_col_name(x)})' for x in qtegn__ptxqp
            ) + f' FROM ({sql_query}) LIMIT 1'
        mkj__ptso = execute_query(cursor, ojw__rdtjv, timeout=
            SF_READ_SCHEMA_PROBE_TIMEOUT)
        if mkj__ptso is not None and (ihq__olgzd := mkj__ptso.fetch_arrow_all()
            ) is not None:
            for hcgd__jre, (dnlpy__xcp, dkgc__nklbx) in enumerate(ihq__olgzd
                .to_pylist()[0].items()):
                mgq__tnufa = qtegn__ptxqp[hcgd__jre]
                kjdi__cmz = (
                    f'SYSTEM$TYPEOF({escape_col_name(mgq__tnufa)})',
                    f'SYSTEM$TYPEOF({escape_col_name(mgq__tnufa.upper())})')
                assert dnlpy__xcp in kjdi__cmz, 'Output of Snowflake Schema Probe Query Uses Unexpected Column Names'
                pbuc__rlz = jpmxr__wxcc[hcgd__jre]
                uhls__abjha = int(dkgc__nklbx[-2])
                jzra__kkj = INT_BITSIZE_TO_ARROW_DATATYPE[uhls__abjha]
                nbbf__nut[pbuc__rlz] = nbbf__nut[pbuc__rlz].with_type(jzra__kkj
                    )
    ccd__zgsxu = []
    kfk__vxleh = []
    lzexy__gqtpc = []
    for hcgd__jre, egl__lwom in enumerate(nbbf__nut):
        gfpg__afs, gga__tjre = _get_numba_typ_from_pa_typ(egl__lwom, False,
            egl__lwom.nullable, None)
        ccd__zgsxu.append(gfpg__afs)
        if not gga__tjre:
            kfk__vxleh.append(hcgd__jre)
            lzexy__gqtpc.append(egl__lwom.type)
    return nbbf__nut, ccd__zgsxu, kfk__vxleh, lzexy__gqtpc


def get_schema(conn_str: str, sql_query: str, is_select_query: bool,
    _bodo_read_as_dict: Optional[List[str]]):
    conn = snowflake_connect(conn_str)
    cursor = conn.cursor()
    evog__uzr, ccd__zgsxu, kfk__vxleh, lzexy__gqtpc = get_schema_from_metadata(
        cursor, sql_query, is_select_query)
    jkm__ayh = _bodo_read_as_dict if _bodo_read_as_dict else []
    aycq__bfzz = {}
    for hcgd__jre, qmurq__xtri in enumerate(ccd__zgsxu):
        if qmurq__xtri == string_array_type:
            aycq__bfzz[evog__uzr[hcgd__jre].name] = hcgd__jre
    pcnid__omhnt = {(igc__zecc.lower() if igc__zecc.isupper() else
        igc__zecc): igc__zecc for igc__zecc in aycq__bfzz.keys()}
    yipps__xefev = jkm__ayh - pcnid__omhnt.keys()
    if len(yipps__xefev) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {yipps__xefev}'
                ))
    iru__mmxn = pcnid__omhnt.keys() & jkm__ayh
    for igc__zecc in iru__mmxn:
        ccd__zgsxu[aycq__bfzz[pcnid__omhnt[igc__zecc]]] = dict_str_arr_type
    vsnze__uauvs, okj__zbpne = [], []
    idkmp__eiso = pcnid__omhnt.keys() - jkm__ayh
    for igc__zecc in idkmp__eiso:
        vsnze__uauvs.append(f'count (distinct "{pcnid__omhnt[igc__zecc]}")')
        okj__zbpne.append(aycq__bfzz[pcnid__omhnt[igc__zecc]])
    hub__rvrbk: Optional[Tuple[int, List[str]]] = None
    if len(vsnze__uauvs) != 0 and SF_READ_AUTO_DICT_ENCODE_ENABLED:
        vbg__ebp = max(SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT // len(
            vsnze__uauvs), 1)
        tipge__woq = (
            f"select count(*),{', '.join(vsnze__uauvs)}from ( select * from ({sql_query}) limit {vbg__ebp} ) SAMPLE (1)"
            )
        ibv__veuro = execute_query(cursor, tipge__woq, timeout=
            SF_READ_DICT_ENCODING_PROBE_TIMEOUT)
        if ibv__veuro is None:
            hub__rvrbk = vbg__ebp, vsnze__uauvs
            if SF_READ_DICT_ENCODING_IF_TIMEOUT:
                for hcgd__jre in okj__zbpne:
                    ccd__zgsxu[hcgd__jre] = dict_str_arr_type
        else:
            lfepd__ojhx: pa.Table = ibv__veuro.fetch_arrow_all()
            uym__nvj = lfepd__ojhx[0][0].as_py()
            xeuqd__qyzwx = [(lfepd__ojhx[hcgd__jre][0].as_py() / max(
                uym__nvj, 1)) for hcgd__jre in range(1, len(vsnze__uauvs) + 1)]
            lib__rts = filter(lambda x: x[0] <=
                SF_READ_DICT_ENCODE_CRITERION, zip(xeuqd__qyzwx, okj__zbpne))
            for _, vna__dfnus in lib__rts:
                ccd__zgsxu[vna__dfnus] = dict_str_arr_type
    tbu__lsma: List[str] = []
    aei__reph = set()
    for x in evog__uzr:
        if x.name.isupper():
            aei__reph.add(x.name.lower())
            tbu__lsma.append(x.name.lower())
        else:
            tbu__lsma.append(x.name)
    ugi__lkion = DataFrameType(data=tuple(ccd__zgsxu), columns=tuple(tbu__lsma)
        )
    return ugi__lkion, aei__reph, kfk__vxleh, lzexy__gqtpc, pa.schema(evog__uzr
        ), hub__rvrbk


class SnowflakeDataset(object):

    def __init__(self, batches: List['ResultBatch'], schema, conn:
        'SnowflakeConnection'):
        self.pieces = batches
        self._bodo_total_rows = 0
        for rejw__jecxm in batches:
            rejw__jecxm._bodo_num_rows = rejw__jecxm.rowcount
            self._bodo_total_rows += rejw__jecxm._bodo_num_rows
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
        zxtw__gqdpf = []
        for vvn__snf in self._json_batch.create_iter():
            zxtw__gqdpf.append({self._schema.names[hcgd__jre]: rpkv__nit for
                hcgd__jre, rpkv__nit in enumerate(vvn__snf)})
        pzds__ucfh = pa.Table.from_pylist(zxtw__gqdpf, schema=self._schema)
        return pzds__ucfh


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
    except ImportError as upli__rll:
        raise BodoError(
            "Snowflake Python connector packages not found. Fetching data from Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    dnyxb__qjqz = tracing.Event('get_snowflake_dataset', is_parallel=
        is_parallel)
    rqvl__csxyx = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    ffgt__qfcbq = -1
    batches = []
    if only_fetch_length and is_select_query:
        if bodo.get_rank() == 0 or is_independent:
            mqg__dla = conn.cursor()
            rdbot__mlx = tracing.Event('execute_length_query', is_parallel=
                False)
            mqg__dla.execute(query)
            mhd__jip = mqg__dla.fetch_arrow_all()
            ffgt__qfcbq = mhd__jip[0][0].as_py()
            mqg__dla.close()
            rdbot__mlx.finalize()
        if not is_independent:
            ffgt__qfcbq = rqvl__csxyx.bcast(ffgt__qfcbq)
    else:
        if bodo.get_rank() == 0 or is_independent:
            mqg__dla = conn.cursor()
            rdbot__mlx = tracing.Event('execute_query', is_parallel=False)
            mqg__dla = conn.cursor()
            mqg__dla.execute(query)
            rdbot__mlx.finalize()
            ffgt__qfcbq: int = mqg__dla.rowcount
            batches: 'List[ResultBatch]' = mqg__dla.get_result_batches()
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
            mqg__dla.close()
        if not is_independent:
            ffgt__qfcbq, batches, schema = rqvl__csxyx.bcast((ffgt__qfcbq,
                batches, schema))
    loasm__yyy = SnowflakeDataset(batches, schema, conn)
    dnyxb__qjqz.finalize()
    return loasm__yyy, ffgt__qfcbq


def create_internal_stage(cursor: 'SnowflakeCursor', is_temporary: bool=False
    ) ->str:
    dnyxb__qjqz = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as upli__rll:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = ''
    ljp__trnw = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                elb__bvj = 'CREATE TEMPORARY STAGE'
            else:
                elb__bvj = 'CREATE STAGE'
            owlc__yolrm = (
                f'{elb__bvj} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(owlc__yolrm, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as fqphj__oopdo:
            if fqphj__oopdo.msg is not None and fqphj__oopdo.msg.endswith(
                'already exists.'):
                continue
            ljp__trnw = fqphj__oopdo.msg
            break
    dnyxb__qjqz.finalize()
    if ljp__trnw is not None:
        raise snowflake.connector.ProgrammingError(ljp__trnw)
    return stage_name


def drop_internal_stage(cursor: 'SnowflakeCursor', stage_name: str):
    dnyxb__qjqz = tracing.Event('drop_internal_stage', is_parallel=False)
    nag__vhn = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(nag__vhn, _is_internal=True)
    dnyxb__qjqz.finalize()


def do_upload_and_cleanup(cursor: 'SnowflakeCursor', chunk_idx: int,
    chunk_path: str, stage_name: str):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        hjth__zqj = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        skatf__vtxlw = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(skatf__vtxlw, _is_internal=True).fetchall()
        hjth__zqj.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        tfp__vva = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        tfp__vva.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        tfp__vva = None
    return tfp__vva


def create_table_handle_exists(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str):
    dnyxb__qjqz = tracing.Event('create_table_if_not_exists', is_parallel=False
        )
    try:
        import snowflake.connector
    except ImportError as upli__rll:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    if if_exists == 'fail':
        iaxx__lyhel = 'CREATE TABLE'
    elif if_exists == 'replace':
        iaxx__lyhel = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        iaxx__lyhel = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    uey__ajho = tracing.Event('create_table', is_parallel=False)
    dilw__rat = ', '.join([f'"{fde__wpm}" {sf_schema[fde__wpm]}' for
        fde__wpm in sf_schema.keys()])
    otlld__diery = (
        f'{iaxx__lyhel} {location} ({dilw__rat}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(otlld__diery, _is_internal=True)
    uey__ajho.finalize()
    dnyxb__qjqz.finalize()


def execute_copy_into(cursor: 'SnowflakeCursor', stage_name: str, location:
    str, sf_schema):
    dnyxb__qjqz = tracing.Event('execute_copy_into', is_parallel=False)
    rqzf__ejb = ','.join([f'"{fde__wpm}"' for fde__wpm in sf_schema.keys()])
    liidp__dhpz = {fde__wpm: ('::binary' if sf_schema[fde__wpm] == 'BINARY'
         else '::string' if sf_schema[fde__wpm].startswith('TIME') else '') for
        fde__wpm in sf_schema.keys()}
    xwga__vqivf = ','.join([f'$1:"{fde__wpm}"{liidp__dhpz[fde__wpm]}' for
        fde__wpm in sf_schema.keys()])
    npe__mlny = (
        f'COPY INTO {location} ({rqzf__ejb}) FROM (SELECT {xwga__vqivf} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO BINARY_AS_TEXT=False) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    suiu__fwngi = cursor.execute(npe__mlny, _is_internal=True).fetchall()
    oooii__jyv = sum(1 if yas__ooiek[1] == 'LOADED' else 0 for yas__ooiek in
        suiu__fwngi)
    zwd__mbb = len(suiu__fwngi)
    nag__srqt = sum(int(yas__ooiek[3]) for yas__ooiek in suiu__fwngi)
    qalhi__zgo = oooii__jyv, zwd__mbb, nag__srqt, suiu__fwngi
    dnyxb__qjqz.add_attribute('copy_into_nsuccess', oooii__jyv)
    dnyxb__qjqz.add_attribute('copy_into_nchunks', zwd__mbb)
    dnyxb__qjqz.add_attribute('copy_into_nrows', nag__srqt)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(suiu__fwngi)}')
    dnyxb__qjqz.finalize()
    return qalhi__zgo


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except (ImportError, AttributeError) as upli__rll:
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
    dnyxb__qjqz = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    hlbnw__xxl = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    hlbnw__xxl = hlbnw__xxl.replace('\\', '\\\\').replace("'", "\\'")
    skatf__vtxlw = (
        f'PUT \'file://{hlbnw__xxl}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    skhgb__vrkb = cursor._execute_helper(skatf__vtxlw, is_internal=True)
    dnyxb__qjqz.finalize()
    return skhgb__vrkb


def connect_and_get_upload_info(conn_str: str):
    dnyxb__qjqz = tracing.Event('connect_and_get_upload_info')
    rqvl__csxyx = MPI.COMM_WORLD
    tol__biumq = rqvl__csxyx.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    oamfg__ruve = ''
    ucd__zkcrf = {}
    old_creds = {}
    old_core_site = ''
    vdrla__aucw = ''
    old_sas_token = ''
    xeeve__mwhh = None
    if tol__biumq == 0:
        try:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                oamfg__ruve = ''
            else:
                skhgb__vrkb = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                alku__baf = skhgb__vrkb['data']['uploadInfo']
                fjl__ebeh = alku__baf.get('locationType', 'UNKNOWN')
                idfq__abft = False
                if fjl__ebeh == 'S3':
                    vjll__uwui, _, hol__apz = alku__baf['location'].partition(
                        '/')
                    hol__apz = hol__apz.rstrip('/')
                    oamfg__ruve = f's3://{vjll__uwui}/{hol__apz}/'
                    ucd__zkcrf = {'AWS_ACCESS_KEY_ID': alku__baf['creds'][
                        'AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY': alku__baf[
                        'creds']['AWS_SECRET_KEY'], 'AWS_SESSION_TOKEN':
                        alku__baf['creds']['AWS_TOKEN'],
                        'AWS_DEFAULT_REGION': alku__baf['region']}
                elif fjl__ebeh == 'AZURE':
                    wmnxg__gpun = False
                    try:
                        import bodo_azurefs_sas_token_provider
                        wmnxg__gpun = True
                    except ImportError as upli__rll:
                        pass
                    yqkg__clpc = len(os.environ.get('HADOOP_HOME', '')
                        ) > 0 and len(os.environ.get('ARROW_LIBHDFS_DIR', '')
                        ) > 0 and len(os.environ.get('CLASSPATH', '')) > 0
                    if wmnxg__gpun and yqkg__clpc:
                        asic__jgwd, _, hol__apz = alku__baf['location'
                            ].partition('/')
                        hol__apz = hol__apz.rstrip('/')
                        bik__mjfe = alku__baf['storageAccount']
                        vdrla__aucw = alku__baf['creds']['AZURE_SAS_TOKEN'
                            ].lstrip('?')
                        if len(hol__apz) == 0:
                            oamfg__ruve = (
                                f'abfs://{asic__jgwd}@{bik__mjfe}.dfs.core.windows.net/'
                                )
                        else:
                            oamfg__ruve = (
                                f'abfs://{asic__jgwd}@{bik__mjfe}.dfs.core.windows.net/{hol__apz}/'
                                )
                        if not 'BODO_PLATFORM_WORKSPACE_UUID' in os.environ:
                            warnings.warn(BodoWarning(
                                """Detected Azure Stage. Bodo will try to upload to the stage directly. If this fails, there might be issues with your Hadoop configuration and you may need to use the PUT method instead by setting
import bodo
bodo.io.snowflake.SF_WRITE_UPLOAD_USING_PUT = True
before calling this function."""
                                ))
                    else:
                        idfq__abft = True
                        vntni__mltvp = 'Detected Azure Stage. '
                        if not wmnxg__gpun:
                            vntni__mltvp += """Required package bodo_azurefs_sas_token_provider is not installed. To use direct upload to stage in the future, install the package using: 'conda install bodo-azurefs-sas-token-provider -c bodo.ai -c conda-forge'.
"""
                        if not yqkg__clpc:
                            vntni__mltvp += """You need to download and set up Hadoop. For more information, refer to our documentation: https://docs.bodo.ai/latest/file_io/?h=hdfs#HDFS.
"""
                        vntni__mltvp += (
                            'Falling back to PUT command for upload for now.')
                        warnings.warn(BodoWarning(vntni__mltvp))
                else:
                    idfq__abft = True
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{fjl__ebeh}'. Falling back to PUT command for upload."
                        ))
                if idfq__abft:
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as yas__ooiek:
            xeeve__mwhh = RuntimeError(str(yas__ooiek))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, yas__ooiek,
                    yas__ooiek.__traceback__)))
    xeeve__mwhh = rqvl__csxyx.bcast(xeeve__mwhh)
    if isinstance(xeeve__mwhh, Exception):
        raise xeeve__mwhh
    oamfg__ruve = rqvl__csxyx.bcast(oamfg__ruve)
    azure_stage_direct_upload = oamfg__ruve.startswith('abfs://')
    if oamfg__ruve == '':
        eam__blkb = True
        oamfg__ruve = tmp_folder.name + '/'
        if tol__biumq != 0:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
    else:
        eam__blkb = False
        ucd__zkcrf = rqvl__csxyx.bcast(ucd__zkcrf)
        old_creds = update_env_vars(ucd__zkcrf)
        if azure_stage_direct_upload:
            import bodo_azurefs_sas_token_provider
            bodo.HDFS_CORE_SITE_LOC_DIR.initialize()
            old_core_site = update_file_contents(bodo.HDFS_CORE_SITE_LOC,
                SF_AZURE_WRITE_HDFS_CORE_SITE)
            vdrla__aucw = rqvl__csxyx.bcast(vdrla__aucw)
            old_sas_token = update_file_contents(
                SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION, vdrla__aucw)
    stage_name = rqvl__csxyx.bcast(stage_name)
    dnyxb__qjqz.finalize()
    return (cursor, tmp_folder, stage_name, oamfg__ruve, eam__blkb,
        old_creds, azure_stage_direct_upload, old_core_site, old_sas_token)


def create_table_copy_into(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str, old_creds, tmp_folder:
    TemporaryDirectory, azure_stage_direct_upload: bool, old_core_site: str,
    old_sas_token: str):
    dnyxb__qjqz = tracing.Event('create_table_copy_into', is_parallel=False)
    rqvl__csxyx = MPI.COMM_WORLD
    tol__biumq = rqvl__csxyx.Get_rank()
    xeeve__mwhh = None
    if tol__biumq == 0:
        try:
            wgfh__wpfqz = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(wgfh__wpfqz)
            create_table_handle_exists(cursor, stage_name, location,
                sf_schema, if_exists)
            oooii__jyv, zwd__mbb, nag__srqt, ebyky__wzc = execute_copy_into(
                cursor, stage_name, location, sf_schema)
            if oooii__jyv != zwd__mbb:
                raise BodoError(
                    f'Snowflake write copy_into failed: {ebyky__wzc}')
            ezvst__oprpb = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(ezvst__oprpb)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as yas__ooiek:
            xeeve__mwhh = RuntimeError(str(yas__ooiek))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, yas__ooiek,
                    yas__ooiek.__traceback__)))
    xeeve__mwhh = rqvl__csxyx.bcast(xeeve__mwhh)
    if isinstance(xeeve__mwhh, Exception):
        raise xeeve__mwhh
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    if azure_stage_direct_upload:
        update_file_contents(bodo.HDFS_CORE_SITE_LOC, old_core_site)
        update_file_contents(SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION,
            old_sas_token)
    dnyxb__qjqz.finalize()
