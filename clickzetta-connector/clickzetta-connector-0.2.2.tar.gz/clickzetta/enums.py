import copy
import enum
import string

DEFAULT_NS = ['default', 'lh']


class AutoRowIDs(enum.Enum):
    DISABLED = enum.auto()
    GENERATE_UUID = enum.auto()


class Compression(object):
    GZIP = "GZIP"

    DEFLATE = "DEFLATE"

    SNAPPY = "SNAPPY"

    NONE = "NONE"


class DecimalTargetType:
    STRING = "STRING"


class CreateDisposition(object):
    CREATE_IF_NEEDED = "CREATE_IF_NEEDED"

    CREATE_NEVER = "CREATE_NEVER"


class DestinationFormat(object):
    CSV = "CSV"

    NEWLINE_DELIMITED_JSON = "NEWLINE_DELIMITED_JSON"

    AVRO = "AVRO"

    PARQUET = "PARQUET"


class Encoding(object):
    UTF_8 = "UTF-8"

    ISO_8859_1 = "ISO-8859-1"


class QueryPriority(object):
    INTERACTIVE = "INTERACTIVE"

    BATCH = "BATCH"


class QueryApiMethod(str, enum.Enum):
    SELECT = "SELECT"

    SHOW = "SHOW"

    DROP = "DROP"

    ALTER = "ALTER"

    CREATE = "CREATE"

    TRUNCATE = "TRUNCATE"


class JobType(object):
    SQL_JOB = "SQL_JOB"

    COMPACTION_JOB = "COMPACTION_JOB"


class JobStatus(object):
    SETUP = "SETUP"
    QUEUEING = "QUEUEING"
    RUNNING = "RUNNING"
    SUCCEED = "SUCCEED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class JobRequestMode(object):
    UNKNOWN = "UNKNOWN"
    HYBRID = "HYBRID"
    ASYNC = "ASYNC"
    SYNC = "SYNC"


class SQLJobConfig(object):
    def __init__(self, timeout, adhoc_size_limit: string, adhoc_row_limit: string, hint: map):
        self.timeout = timeout
        self.adhoc_size_limit = adhoc_size_limit
        self.adhoc_row_limit = adhoc_row_limit
        self.hint = hint
        self._properties = {'timeout': timeout, 'adhocSizeLimit': adhoc_size_limit, 'adhocRowLimit': adhoc_row_limit,
                            'hint': hint}

    def to_api_repr(self) -> dict:
        return copy.deepcopy(self._properties)


class SQLJob(object):
    def __init__(self, sql_job_config: SQLJobConfig, workspace: string, db_name: string, query):
        self.query = query
        self.default_namespace = [workspace, db_name]
        self.sql_job_config = sql_job_config

    def to_api_repr(self) -> dict:
        _properties = {'query': self.query, 'defaultNamespace': self.default_namespace,
                       'sqlConfig': self.sql_job_config.to_api_repr()}
        return copy.deepcopy(_properties)


class JobID(object):
    def __init__(self, id: string, workspace: string, instance_id: int):
        self.id = id
        self.workspace = workspace
        self.instance_id = instance_id
        self._properties = {'id': id, 'workspace': workspace, 'instanceId': instance_id}

    def to_api_repr(self) -> dict:
        return copy.deepcopy(self._properties)


class JobDesc(object):
    def __init__(self, virtual_cluster: string, job_type: JobType, job_id: JobID, job_name: string, user_id: int,
                 request_mode: JobRequestMode, hybrid_polling_timeout: int, job_config: map, sql_job: SQLJob,
                 job_timeout_ms: int, user_agent: string, priority: int):
        self.virtual_cluster = virtual_cluster
        self.job_type = job_type
        self.job_id = job_id
        self.job_name = job_name
        self.user_id = user_id
        self.request_mode = request_mode
        self.hybrid_polling_timeout = hybrid_polling_timeout
        self.job_config = job_config
        self.sql_job = sql_job
        self.job_timeout_ms = job_timeout_ms
        self.user_agent = user_agent
        self.priority = priority
        self._properties = {'virtualCluster': virtual_cluster, 'type': job_type, 'jobId': job_id.to_api_repr(),
                            'jobName': job_name,
                            'requestMode': request_mode, 'hybridPollingTimeout': hybrid_polling_timeout,
                            'jobConfig': job_config, 'sqlJob': sql_job.to_api_repr()}

    def to_api_repr(self) -> dict:
        return copy.deepcopy(self._properties)


class JobRequest(object):
    def __init__(self, job_desc: JobDesc):
        self.job_desc = job_desc
        self._properties = {"jobDesc": job_desc.to_api_repr()}

    def to_api_repr(self) -> dict:
        return copy.deepcopy(self._properties)


class LoginParams(object):
    def __init__(self, username: string, password: string, instance_name: string):
        self.username = username
        self.password = password
        self.instance_name = instance_name
        self._properties = {"username": username, "password": password, "instanceName": instance_name}

    def to_api_repr(self) -> dict:
        return copy.deepcopy(self._properties)


class ErrorStatus(object):
    Unauthorized = "UNAUTHORIZED"


class SourceFormat(object):
    CSV = "CSV"

    NEWLINE_DELIMITED_JSON = "NEWLINE_DELIMITED_JSON"

    AVRO = "AVRO"

    PARQUET = "PARQUET"

    ORC = "ORC"


class KeyResultStatementKind:
    KEY_RESULT_STATEMENT_KIND_UNSPECIFIED = "KEY_RESULT_STATEMENT_KIND_UNSPECIFIED"
    LAST = "LAST"
    FIRST_SELECT = "FIRST_SELECT"


class StandardSqlTypeNames(str, enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    TYPE_KIND_UNSPECIFIED = enum.auto()
    INT64 = enum.auto()
    BOOL = enum.auto()
    FLOAT64 = enum.auto()
    FLOAT32 = enum.auto()
    STRING = enum.auto()
    VARCHAR = enum.auto()
    CHAR = enum.auto()
    INT32 = enum.auto()
    INT16 = enum.auto()
    INT8 = enum.auto()
    TIMESTAMP = enum.auto()
    DATE = enum.auto()
    DECIMAL = enum.auto()
    BINARY = enum.auto()
    ARRAY = enum.auto()
    MAP = enum.auto()
    STRUCT = enum.auto()


class SqlTypeNames(str, enum.Enum):
    STRING = "STRING"
    BINARY = "BINARY"
    INT8 = "INT8"
    INT16 = "INT16"
    INT32 = "INT32"
    INT64 = "INT64"
    FLOAT32 = "FLOAT32"
    FLOAT64 = "FLOAT32"
    DECIMAL = "DECIMAL"
    BOOL = "BOOLEAN"
    STRUCT = "STRUCT"
    MAP = "MAP"
    ARRAY = "ARRAY"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"


class WriteDisposition(object):
    WRITE_APPEND = "WRITE_APPEND"

    WRITE_TRUNCATE = "WRITE_TRUNCATE"

    WRITE_EMPTY = "WRITE_EMPTY"
