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
    for col_name, eyx__mgwiv in zip(column_names, column_datatypes):
        if isinstance(eyx__mgwiv, bodo.DatetimeArrayType
            ) or eyx__mgwiv == bodo.datetime_datetime_type:
            sf_schema[col_name] = 'TIMESTAMP_NTZ'
        elif eyx__mgwiv == bodo.datetime_date_array_type:
            sf_schema[col_name] = 'DATE'
        elif isinstance(eyx__mgwiv, bodo.TimeArrayType):
            if eyx__mgwiv.precision in [0, 3, 6]:
                tznm__mkywi = eyx__mgwiv.precision
            elif eyx__mgwiv.precision == 9:
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"""to_sql(): {col_name} time precision will be lost.
Snowflake loses nano second precision when exporting parquet file using COPY INTO.
 This is due to a limitation on Parquet V1 that is currently being used in Snowflake"""
                        ))
                tznm__mkywi = 6
            else:
                raise ValueError(
                    'Unsupported Precision Found in Bodo Time Array')
            sf_schema[col_name] = f'TIME({tznm__mkywi})'
        elif isinstance(eyx__mgwiv, types.Array):
            asqps__bkh = eyx__mgwiv.dtype.name
            if asqps__bkh.startswith('datetime'):
                sf_schema[col_name] = 'DATETIME'
            if asqps__bkh.startswith('timedelta'):
                sf_schema[col_name] = 'NUMBER(38, 0)'
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"to_sql(): {col_name} with type 'timedelta' will be written as integer values (ns frequency) to the database."
                        ))
            elif asqps__bkh.startswith(('int', 'uint')):
                sf_schema[col_name] = 'NUMBER(38, 0)'
            elif asqps__bkh.startswith('float'):
                sf_schema[col_name] = 'REAL'
        elif is_str_arr_type(eyx__mgwiv):
            sf_schema[col_name] = 'TEXT'
        elif eyx__mgwiv == bodo.binary_array_type:
            sf_schema[col_name] = 'BINARY'
        elif eyx__mgwiv == bodo.boolean_array:
            sf_schema[col_name] = 'BOOLEAN'
        elif isinstance(eyx__mgwiv, bodo.IntegerArrayType):
            sf_schema[col_name] = 'NUMBER(38, 0)'
        elif isinstance(eyx__mgwiv, bodo.FloatingArrayType):
            sf_schema[col_name] = 'REAL'
        elif isinstance(eyx__mgwiv, bodo.DecimalArrayType):
            sf_schema[col_name] = 'NUMBER(38, 18)'
        elif isinstance(eyx__mgwiv, (ArrayItemArrayType, StructArrayType)):
            sf_schema[col_name] = 'VARIANT'
        else:
            raise BodoError(
                f'Conversion from Bodo array type {eyx__mgwiv} to snowflake type for {col_name} not supported yet.'
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
    except snowflake.connector.errors.ProgrammingError as ozp__oufg:
        if 'SQL execution canceled' in str(ozp__oufg):
            return None
        else:
            raise


def escape_col_name(col_name: str) ->str:
    return '"{}"'.format(col_name.replace('"', '""'))


def snowflake_connect(conn_str: str, is_parallel: bool=False
    ) ->'SnowflakeConnection':
    kdvzt__tve = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    zntsy__ktie = urlparse(conn_str)
    ovesz__fxjk = {}
    if zntsy__ktie.username:
        ovesz__fxjk['user'] = zntsy__ktie.username
    if zntsy__ktie.password:
        ovesz__fxjk['password'] = zntsy__ktie.password
    if zntsy__ktie.hostname:
        ovesz__fxjk['account'] = zntsy__ktie.hostname
    if zntsy__ktie.port:
        ovesz__fxjk['port'] = zntsy__ktie.port
    if zntsy__ktie.path:
        qjn__kwgn = zntsy__ktie.path
        if qjn__kwgn.startswith('/'):
            qjn__kwgn = qjn__kwgn[1:]
        wor__emlzh = qjn__kwgn.split('/')
        if len(wor__emlzh) == 2:
            krvr__bbg, schema = wor__emlzh
        elif len(wor__emlzh) == 1:
            krvr__bbg = wor__emlzh[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        ovesz__fxjk['database'] = krvr__bbg
        if schema:
            ovesz__fxjk['schema'] = schema
    if zntsy__ktie.query:
        for ojzhd__cna, whaqf__urhf in parse_qsl(zntsy__ktie.query):
            ovesz__fxjk[ojzhd__cna] = whaqf__urhf
            if ojzhd__cna == 'session_parameters':
                import json
                ovesz__fxjk[ojzhd__cna] = json.loads(whaqf__urhf)
    ovesz__fxjk['application'] = 'bodo'
    ovesz__fxjk['login_timeout'] = 5
    try:
        import snowflake.connector
    except ImportError as vdwh__tmk:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**ovesz__fxjk)
    asgms__ekkof = os.environ.get('BODO_PLATFORM_WORKSPACE_REGION', None)
    if asgms__ekkof and bodo.get_rank() == 0:
        asgms__ekkof = asgms__ekkof.lower()
        dyox__powr = os.environ.get('BODO_PLATFORM_CLOUD_PROVIDER', None)
        if dyox__powr is not None:
            dyox__powr = dyox__powr.lower()
        oay__hxg = conn.cursor()
        oay__hxg.execute('select current_region()')
        gml__dzbng: pa.Table = oay__hxg.fetch_arrow_all()
        dhwxs__ngn = gml__dzbng[0][0].as_py()
        oay__hxg.close()
        xioxb__mdwv = dhwxs__ngn.split('_')
        rttx__nlv = xioxb__mdwv[0].lower()
        lzbam__bef = '-'.join(xioxb__mdwv[1:]).lower()
        if dyox__powr and dyox__powr != rttx__nlv:
            yrmk__hexz = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are on different cloud providers. '
                 +
                f'The Snowflake warehouse is located on {rttx__nlv}, but the Bodo cluster is located on {dyox__powr}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(yrmk__hexz)
        elif asgms__ekkof != lzbam__bef:
            yrmk__hexz = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are in different cloud regions. '
                 +
                f'The Snowflake warehouse is located in {lzbam__bef}, but the Bodo cluster is located in {asgms__ekkof}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(yrmk__hexz)
    kdvzt__tve.finalize()
    return conn


def get_schema_from_metadata(cursor: 'SnowflakeCursor', sql_query: str,
    is_select_query: bool) ->Tuple[List[pa.Field], List, List[int], List[pa
    .DataType]]:
    jqkp__wok = cursor.describe(sql_query)
    tz: str = cursor._timezone
    come__gwl: List[pa.Field] = []
    hivq__oip: List[str] = []
    ofn__rizbn: List[int] = []
    for dgpb__wunt, hyh__efqpb in enumerate(jqkp__wok):
        nkw__pvjqm = TYPE_CODE_TO_ARROW_TYPE[hyh__efqpb.type_code](hyh__efqpb,
            tz)
        come__gwl.append(pa.field(hyh__efqpb.name, nkw__pvjqm, hyh__efqpb.
            is_nullable))
        if pa.types.is_int64(nkw__pvjqm):
            hivq__oip.append(hyh__efqpb.name)
            ofn__rizbn.append(dgpb__wunt)
    if is_select_query and len(hivq__oip) != 0:
        mpnfw__zfu = 'SELECT ' + ', '.join(
            f'SYSTEM$TYPEOF({escape_col_name(x)})' for x in hivq__oip
            ) + f' FROM ({sql_query}) LIMIT 1'
        ril__cvnff = execute_query(cursor, mpnfw__zfu, timeout=
            SF_READ_SCHEMA_PROBE_TIMEOUT)
        if ril__cvnff is not None and (pghme__ekkn := ril__cvnff.
            fetch_arrow_all()) is not None:
            for dgpb__wunt, (upg__uqbeu, nkpm__bmwwp) in enumerate(pghme__ekkn
                .to_pylist()[0].items()):
                trb__oggb = hivq__oip[dgpb__wunt]
                acyis__sdyo = (
                    f'SYSTEM$TYPEOF({escape_col_name(trb__oggb)})',
                    f'SYSTEM$TYPEOF({escape_col_name(trb__oggb.upper())})')
                assert upg__uqbeu in acyis__sdyo, 'Output of Snowflake Schema Probe Query Uses Unexpected Column Names'
                dry__sypme = ofn__rizbn[dgpb__wunt]
                ihfh__eci = int(nkpm__bmwwp[-2])
                xzosv__jml = INT_BITSIZE_TO_ARROW_DATATYPE[ihfh__eci]
                come__gwl[dry__sypme] = come__gwl[dry__sypme].with_type(
                    xzosv__jml)
    nmf__rxn = []
    zit__oyyv = []
    yvg__pljy = []
    for dgpb__wunt, fevwy__pxhi in enumerate(come__gwl):
        nkw__pvjqm, xyj__ndj = _get_numba_typ_from_pa_typ(fevwy__pxhi, 
            False, fevwy__pxhi.nullable, None)
        nmf__rxn.append(nkw__pvjqm)
        if not xyj__ndj:
            zit__oyyv.append(dgpb__wunt)
            yvg__pljy.append(fevwy__pxhi.type)
    return come__gwl, nmf__rxn, zit__oyyv, yvg__pljy


def get_schema(conn_str: str, sql_query: str, is_select_query: bool,
    _bodo_read_as_dict: Optional[List[str]]):
    conn = snowflake_connect(conn_str)
    cursor = conn.cursor()
    wpdxz__mxf, nmf__rxn, zit__oyyv, yvg__pljy = get_schema_from_metadata(
        cursor, sql_query, is_select_query)
    gnn__yqr = _bodo_read_as_dict if _bodo_read_as_dict else []
    jivis__ggpug = {}
    for dgpb__wunt, kapro__juk in enumerate(nmf__rxn):
        if kapro__juk == string_array_type:
            jivis__ggpug[wpdxz__mxf[dgpb__wunt].name] = dgpb__wunt
    pwa__xiy = {(bjzst__cib.lower() if bjzst__cib.isupper() else bjzst__cib
        ): bjzst__cib for bjzst__cib in jivis__ggpug.keys()}
    zjrn__lxnls = gnn__yqr - pwa__xiy.keys()
    if len(zjrn__lxnls) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {zjrn__lxnls}'
                ))
    jvybl__itjj = pwa__xiy.keys() & gnn__yqr
    for bjzst__cib in jvybl__itjj:
        nmf__rxn[jivis__ggpug[pwa__xiy[bjzst__cib]]] = dict_str_arr_type
    hvrti__fwnj, acugg__izo = [], []
    vcww__bnu = pwa__xiy.keys() - gnn__yqr
    for bjzst__cib in vcww__bnu:
        hvrti__fwnj.append(f'count (distinct "{pwa__xiy[bjzst__cib]}")')
        acugg__izo.append(jivis__ggpug[pwa__xiy[bjzst__cib]])
    crldb__xcqh: Optional[Tuple[int, List[str]]] = None
    if len(hvrti__fwnj) != 0 and SF_READ_AUTO_DICT_ENCODE_ENABLED:
        vjjfe__beuje = max(SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT // len(
            hvrti__fwnj), 1)
        ftkyv__tqw = (
            f"select count(*),{', '.join(hvrti__fwnj)}from ( select * from ({sql_query}) limit {vjjfe__beuje} ) SAMPLE (1)"
            )
        lvmv__snzz = execute_query(cursor, ftkyv__tqw, timeout=
            SF_READ_DICT_ENCODING_PROBE_TIMEOUT)
        if lvmv__snzz is None:
            crldb__xcqh = vjjfe__beuje, hvrti__fwnj
            if SF_READ_DICT_ENCODING_IF_TIMEOUT:
                for dgpb__wunt in acugg__izo:
                    nmf__rxn[dgpb__wunt] = dict_str_arr_type
        else:
            jxauf__pgt: pa.Table = lvmv__snzz.fetch_arrow_all()
            oczr__cft = jxauf__pgt[0][0].as_py()
            yrg__lpw = [(jxauf__pgt[dgpb__wunt][0].as_py() / max(oczr__cft,
                1)) for dgpb__wunt in range(1, len(hvrti__fwnj) + 1)]
            rehnn__jdxt = filter(lambda x: x[0] <=
                SF_READ_DICT_ENCODE_CRITERION, zip(yrg__lpw, acugg__izo))
            for _, cveq__rgd in rehnn__jdxt:
                nmf__rxn[cveq__rgd] = dict_str_arr_type
    xuzj__tgjv: List[str] = []
    ivj__kfgn = set()
    for x in wpdxz__mxf:
        if x.name.isupper():
            ivj__kfgn.add(x.name.lower())
            xuzj__tgjv.append(x.name.lower())
        else:
            xuzj__tgjv.append(x.name)
    nik__kxpz = DataFrameType(data=tuple(nmf__rxn), columns=tuple(xuzj__tgjv))
    return nik__kxpz, ivj__kfgn, zit__oyyv, yvg__pljy, pa.schema(wpdxz__mxf
        ), crldb__xcqh


class SnowflakeDataset(object):

    def __init__(self, batches: List['ResultBatch'], schema, conn:
        'SnowflakeConnection'):
        self.pieces = batches
        self._bodo_total_rows = 0
        for cbfu__npm in batches:
            cbfu__npm._bodo_num_rows = cbfu__npm.rowcount
            self._bodo_total_rows += cbfu__npm._bodo_num_rows
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
        vmw__mfk = []
        for kjc__sjnxf in self._json_batch.create_iter():
            vmw__mfk.append({self._schema.names[dgpb__wunt]: idlj__dtm for 
                dgpb__wunt, idlj__dtm in enumerate(kjc__sjnxf)})
        ieat__tlhv = pa.Table.from_pylist(vmw__mfk, schema=self._schema)
        return ieat__tlhv


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
    except ImportError as vdwh__tmk:
        raise BodoError(
            "Snowflake Python connector packages not found. Fetching data from Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    kdvzt__tve = tracing.Event('get_snowflake_dataset', is_parallel=is_parallel
        )
    lrjb__iohg = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    tqhjl__fxbsx = -1
    batches = []
    if only_fetch_length and is_select_query:
        if bodo.get_rank() == 0 or is_independent:
            oay__hxg = conn.cursor()
            ahuf__cgnj = tracing.Event('execute_length_query', is_parallel=
                False)
            oay__hxg.execute(query)
            gml__dzbng = oay__hxg.fetch_arrow_all()
            tqhjl__fxbsx = gml__dzbng[0][0].as_py()
            oay__hxg.close()
            ahuf__cgnj.finalize()
        if not is_independent:
            tqhjl__fxbsx = lrjb__iohg.bcast(tqhjl__fxbsx)
    else:
        if bodo.get_rank() == 0 or is_independent:
            oay__hxg = conn.cursor()
            ahuf__cgnj = tracing.Event('execute_query', is_parallel=False)
            oay__hxg = conn.cursor()
            oay__hxg.execute(query)
            ahuf__cgnj.finalize()
            tqhjl__fxbsx: int = oay__hxg.rowcount
            batches: 'List[ResultBatch]' = oay__hxg.get_result_batches()
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
            oay__hxg.close()
        if not is_independent:
            tqhjl__fxbsx, batches, schema = lrjb__iohg.bcast((tqhjl__fxbsx,
                batches, schema))
    jpu__wozoh = SnowflakeDataset(batches, schema, conn)
    kdvzt__tve.finalize()
    return jpu__wozoh, tqhjl__fxbsx


def create_internal_stage(cursor: 'SnowflakeCursor', is_temporary: bool=False
    ) ->str:
    kdvzt__tve = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as vdwh__tmk:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = ''
    hddn__joifr = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                iuz__xwcye = 'CREATE TEMPORARY STAGE'
            else:
                iuz__xwcye = 'CREATE STAGE'
            gbck__slopn = (
                f'{iuz__xwcye} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(gbck__slopn, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as krj__cmk:
            if krj__cmk.msg is not None and krj__cmk.msg.endswith(
                'already exists.'):
                continue
            hddn__joifr = krj__cmk.msg
            break
    kdvzt__tve.finalize()
    if hddn__joifr is not None:
        raise snowflake.connector.ProgrammingError(hddn__joifr)
    return stage_name


def drop_internal_stage(cursor: 'SnowflakeCursor', stage_name: str):
    kdvzt__tve = tracing.Event('drop_internal_stage', is_parallel=False)
    cujvl__ljx = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(cujvl__ljx, _is_internal=True)
    kdvzt__tve.finalize()


def do_upload_and_cleanup(cursor: 'SnowflakeCursor', chunk_idx: int,
    chunk_path: str, stage_name: str):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        yuq__jllaw = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        wetkm__mev = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(wetkm__mev, _is_internal=True).fetchall()
        yuq__jllaw.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        ytj__ewfpj = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        ytj__ewfpj.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        ytj__ewfpj = None
    return ytj__ewfpj


def create_table_handle_exists(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str):
    kdvzt__tve = tracing.Event('create_table_if_not_exists', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as vdwh__tmk:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    if if_exists == 'fail':
        huu__ximn = 'CREATE TABLE'
    elif if_exists == 'replace':
        huu__ximn = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        huu__ximn = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    tfuz__ykmj = tracing.Event('create_table', is_parallel=False)
    cov__lgy = ', '.join([f'"{pxb__tjn}" {sf_schema[pxb__tjn]}' for
        pxb__tjn in sf_schema.keys()])
    esoih__uol = (
        f'{huu__ximn} {location} ({cov__lgy}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(esoih__uol, _is_internal=True)
    tfuz__ykmj.finalize()
    kdvzt__tve.finalize()


def execute_copy_into(cursor: 'SnowflakeCursor', stage_name: str, location:
    str, sf_schema):
    kdvzt__tve = tracing.Event('execute_copy_into', is_parallel=False)
    zxu__wqdix = ','.join([f'"{pxb__tjn}"' for pxb__tjn in sf_schema.keys()])
    pmeyb__sqbiq = {pxb__tjn: ('::binary' if sf_schema[pxb__tjn] ==
        'BINARY' else '::string' if sf_schema[pxb__tjn].startswith('TIME') else
        '') for pxb__tjn in sf_schema.keys()}
    afai__wct = ','.join([f'$1:"{pxb__tjn}"{pmeyb__sqbiq[pxb__tjn]}' for
        pxb__tjn in sf_schema.keys()])
    ysffv__zbs = (
        f'COPY INTO {location} ({zxu__wqdix}) FROM (SELECT {afai__wct} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO BINARY_AS_TEXT=False) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    vadj__wkaw = cursor.execute(ysffv__zbs, _is_internal=True).fetchall()
    rbk__cyliw = sum(1 if ozp__oufg[1] == 'LOADED' else 0 for ozp__oufg in
        vadj__wkaw)
    kgrw__ccaq = len(vadj__wkaw)
    fjen__zguyc = sum(int(ozp__oufg[3]) for ozp__oufg in vadj__wkaw)
    hjvst__xgpn = rbk__cyliw, kgrw__ccaq, fjen__zguyc, vadj__wkaw
    kdvzt__tve.add_attribute('copy_into_nsuccess', rbk__cyliw)
    kdvzt__tve.add_attribute('copy_into_nchunks', kgrw__ccaq)
    kdvzt__tve.add_attribute('copy_into_nrows', fjen__zguyc)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(vadj__wkaw)}')
    kdvzt__tve.finalize()
    return hjvst__xgpn


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except (ImportError, AttributeError) as vdwh__tmk:
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
    kdvzt__tve = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    kmc__fbqo = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    kmc__fbqo = kmc__fbqo.replace('\\', '\\\\').replace("'", "\\'")
    wetkm__mev = (
        f'PUT \'file://{kmc__fbqo}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    dwhfg__jyx = cursor._execute_helper(wetkm__mev, is_internal=True)
    kdvzt__tve.finalize()
    return dwhfg__jyx


def connect_and_get_upload_info(conn_str: str):
    kdvzt__tve = tracing.Event('connect_and_get_upload_info')
    lrjb__iohg = MPI.COMM_WORLD
    iqv__ldf = lrjb__iohg.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    zme__xse = ''
    iszn__jxjl = {}
    old_creds = {}
    old_core_site = ''
    psulk__fxyh = ''
    old_sas_token = ''
    tloxs__ipas = None
    if iqv__ldf == 0:
        try:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                zme__xse = ''
            else:
                dwhfg__jyx = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                zcvle__kfmef = dwhfg__jyx['data']['uploadInfo']
                kke__ohx = zcvle__kfmef.get('locationType', 'UNKNOWN')
                zrc__smom = False
                if kke__ohx == 'S3':
                    yeej__fgpor, _, qjn__kwgn = zcvle__kfmef['location'
                        ].partition('/')
                    qjn__kwgn = qjn__kwgn.rstrip('/')
                    zme__xse = f's3://{yeej__fgpor}/{qjn__kwgn}/'
                    iszn__jxjl = {'AWS_ACCESS_KEY_ID': zcvle__kfmef['creds'
                        ]['AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY':
                        zcvle__kfmef['creds']['AWS_SECRET_KEY'],
                        'AWS_SESSION_TOKEN': zcvle__kfmef['creds'][
                        'AWS_TOKEN'], 'AWS_DEFAULT_REGION': zcvle__kfmef[
                        'region']}
                elif kke__ohx == 'AZURE':
                    lqb__wpu = False
                    try:
                        import bodo_azurefs_sas_token_provider
                        lqb__wpu = True
                    except ImportError as vdwh__tmk:
                        pass
                    qey__rfne = len(os.environ.get('HADOOP_HOME', '')
                        ) > 0 and len(os.environ.get('ARROW_LIBHDFS_DIR', '')
                        ) > 0 and len(os.environ.get('CLASSPATH', '')) > 0
                    if lqb__wpu and qey__rfne:
                        grhhx__utkx, _, qjn__kwgn = zcvle__kfmef['location'
                            ].partition('/')
                        qjn__kwgn = qjn__kwgn.rstrip('/')
                        eah__qwv = zcvle__kfmef['storageAccount']
                        psulk__fxyh = zcvle__kfmef['creds']['AZURE_SAS_TOKEN'
                            ].lstrip('?')
                        if len(qjn__kwgn) == 0:
                            zme__xse = (
                                f'abfs://{grhhx__utkx}@{eah__qwv}.dfs.core.windows.net/'
                                )
                        else:
                            zme__xse = (
                                f'abfs://{grhhx__utkx}@{eah__qwv}.dfs.core.windows.net/{qjn__kwgn}/'
                                )
                        if not 'BODO_PLATFORM_WORKSPACE_UUID' in os.environ:
                            warnings.warn(BodoWarning(
                                """Detected Azure Stage. Bodo will try to upload to the stage directly. If this fails, there might be issues with your Hadoop configuration and you may need to use the PUT method instead by setting
import bodo
bodo.io.snowflake.SF_WRITE_UPLOAD_USING_PUT = True
before calling this function."""
                                ))
                    else:
                        zrc__smom = True
                        roppb__ruba = 'Detected Azure Stage. '
                        if not lqb__wpu:
                            roppb__ruba += """Required package bodo_azurefs_sas_token_provider is not installed. To use direct upload to stage in the future, install the package using: 'conda install bodo-azurefs-sas-token-provider -c bodo.ai -c conda-forge'.
"""
                        if not qey__rfne:
                            roppb__ruba += """You need to download and set up Hadoop. For more information, refer to our documentation: https://docs.bodo.ai/latest/file_io/?h=hdfs#HDFS.
"""
                        roppb__ruba += (
                            'Falling back to PUT command for upload for now.')
                        warnings.warn(BodoWarning(roppb__ruba))
                else:
                    zrc__smom = True
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{kke__ohx}'. Falling back to PUT command for upload."
                        ))
                if zrc__smom:
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as ozp__oufg:
            tloxs__ipas = RuntimeError(str(ozp__oufg))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, ozp__oufg,
                    ozp__oufg.__traceback__)))
    tloxs__ipas = lrjb__iohg.bcast(tloxs__ipas)
    if isinstance(tloxs__ipas, Exception):
        raise tloxs__ipas
    zme__xse = lrjb__iohg.bcast(zme__xse)
    azure_stage_direct_upload = zme__xse.startswith('abfs://')
    if zme__xse == '':
        ahu__mgeg = True
        zme__xse = tmp_folder.name + '/'
        if iqv__ldf != 0:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
    else:
        ahu__mgeg = False
        iszn__jxjl = lrjb__iohg.bcast(iszn__jxjl)
        old_creds = update_env_vars(iszn__jxjl)
        if azure_stage_direct_upload:
            import bodo_azurefs_sas_token_provider
            bodo.HDFS_CORE_SITE_LOC_DIR.initialize()
            old_core_site = update_file_contents(bodo.HDFS_CORE_SITE_LOC,
                SF_AZURE_WRITE_HDFS_CORE_SITE)
            psulk__fxyh = lrjb__iohg.bcast(psulk__fxyh)
            old_sas_token = update_file_contents(
                SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION, psulk__fxyh)
    stage_name = lrjb__iohg.bcast(stage_name)
    kdvzt__tve.finalize()
    return (cursor, tmp_folder, stage_name, zme__xse, ahu__mgeg, old_creds,
        azure_stage_direct_upload, old_core_site, old_sas_token)


def create_table_copy_into(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str, old_creds, tmp_folder:
    TemporaryDirectory, azure_stage_direct_upload: bool, old_core_site: str,
    old_sas_token: str):
    kdvzt__tve = tracing.Event('create_table_copy_into', is_parallel=False)
    lrjb__iohg = MPI.COMM_WORLD
    iqv__ldf = lrjb__iohg.Get_rank()
    tloxs__ipas = None
    if iqv__ldf == 0:
        try:
            zfj__rwi = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(zfj__rwi)
            create_table_handle_exists(cursor, stage_name, location,
                sf_schema, if_exists)
            rbk__cyliw, kgrw__ccaq, fjen__zguyc, nczt__rey = execute_copy_into(
                cursor, stage_name, location, sf_schema)
            if rbk__cyliw != kgrw__ccaq:
                raise BodoError(
                    f'Snowflake write copy_into failed: {nczt__rey}')
            vhqa__aopgk = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(vhqa__aopgk)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as ozp__oufg:
            tloxs__ipas = RuntimeError(str(ozp__oufg))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, ozp__oufg,
                    ozp__oufg.__traceback__)))
    tloxs__ipas = lrjb__iohg.bcast(tloxs__ipas)
    if isinstance(tloxs__ipas, Exception):
        raise tloxs__ipas
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    if azure_stage_direct_upload:
        update_file_contents(bodo.HDFS_CORE_SITE_LOC, old_core_site)
        update_file_contents(SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION,
            old_sas_token)
    kdvzt__tve.finalize()
