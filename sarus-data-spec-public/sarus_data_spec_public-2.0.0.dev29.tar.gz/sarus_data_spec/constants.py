from enum import Enum

DATA = 'data'
USER_COLUMN = 'sarus_protected_entity'
WEIGHTS = 'sarus_weights'
PUBLIC = 'sarus_is_public'

# constants used in protection stored in each struct
NON_EMPTY_PROTECTED_PATHS = 'non_zero_protected_values'
STRUCT_KIND = 'merge_paths'
TO_MERGE = 'fks_for_merging'

# protection constants for paths in types
LIST_VALUES = 'sarus_list_values'
ARRAY_VALUES = 'sarus_array_values'
OPTIONAL_VALUE = 'sarus_optional_value'


class StructKind(Enum):
    HAS_PE = '0'
    NO_PE = '1'
    TO_MERGE = '2'


# constants for type properties
TEXT_MIN_LENGTH = 'min_length'
TEXT_MAX_LENGTH = 'max_length'
TEXT_CHARSET = 'text_char_set'
TEXT_EXACT_CHARSET = 'FullUserInput'
TEXT_ALPHABET_NAME = 'text_alphabet_name'
SQL_MAPPING = 'sql_mapping'
FLOAT_DISTRIBUTION = 'distribution_model'
FLOAT_DIST_PARAMS = 'parameters'
MAX_MAX_MULT = 'max_max_multiplicity'

# name of the dataset
DATASET_SLUGNAME = 'slugname'

# names when transforming datetime type in struct
DATETIME_YEAR = 'year'
DATETIME_MONTH = 'month'
DATETIME_DAY = 'day'
DATETIME_HOUR = 'hour'
DATETIME_MINUTES = 'minutes'
DATETIME_SECONDS = 'seconds'


# Statuses constants
TO_SQL_TASK = "sql_preparation"

# Big Data Status
BIG_DATA_TASK = 'big_data_dataset'
BIG_DATA_THRESHOLD = 'threshold'
IS_BIG_DATA = 'is_big_data'
DATASET_N_LINES = 'dataset_n_lines'
DATASET_N_BYTES = 'dataset_n_bytes'
THRESHOLD_TYPE = "threshold_type"

# Caching Status
TO_PARQUET_TASK = 'to_parquet'
CACHE = TO_PARQUET_TASK
CACHE_PATH = 'path'
COMPUTATION_QUEUED = 'computation_queued'

# Caching infos for scalar
CACHE_TYPE = 'cache_type'
CACHE_PROTO = 'cache_proto'
SCALAR_TASK = 'scalar_value'


class ScalarCaching(Enum):
    PICKLE = 'pickle'
    PROTO = 'protobuf'


# Attributes Status
SCHEMA_TASK = 'schema'
SIZE_TASK = 'size'
BOUNDS_TASK = 'bounds'
MARGINALS_TASK = 'marginals'
ARROW_TASK = 'arrow'
PROTECTION_TASK = 'protection_task'
USER_SETTINGS_TASK = 'user_settings_task'
PUBLIC_TASK = 'public_task'
CACHE_SCALAR_TASK = 'cache_scalar'
QB_TASK = 'query_builder'
LINKS_TASK = 'links_statistics'
SYNTHETIC_TASK = 'synthetic'

# Privacy
PEP_TOKEN = "pep_token"
PRIVACY_LIMIT = "privacy_limit"

# QUERYBUILDER
QUERIES = 'queries'

# Attributes names
PRIVATE_QUERY = "private_query"
IS_REMOTE = "is_remote"
VARIANT_UUID = "variant_uuid"


# SYNTHETIC DATA
class SyntheticDataSettings:
    """Namespace for SD generation settings"""

    BATCH_SIZE = 64
    EPOCHS = 10
