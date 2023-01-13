import base64
import hashlib
import re
import string
import unicodedata
from typing import NamedTuple, Dict, List, Set, Iterable, Optional
from urllib.parse import quote_plus, urlencode

from sqlalchemy.engine import Connection, Dialect

from bach.expression import Expression, ColumnReferenceToken
from bach.sql_model import BachSqlModel
from sql_models.util import is_postgres, DatabaseNotSupportedException, is_bigquery, is_athena


class SortColumn(NamedTuple):
    expression: Expression
    asc: bool


class FeatureRange(NamedTuple):
    min: int
    max: int


class ResultSeries(NamedTuple):
    name: str
    expression: 'Expression'
    dtype: str


def get_result_series_dtype_mapping(result_series: List[ResultSeries]) -> Dict[str, str]:
    return {
        rs.name: rs.dtype
        for rs in result_series
    }


def get_merged_series_dtype(dtypes: Set[str]) -> str:
    """
    returns a final dtype when trying to combine series with different dtypes
    """
    from bach import get_series_type_from_dtype, SeriesAbstractNumeric
    if len(dtypes) == 1:
        return dtypes.pop()
    elif all(
        issubclass(get_series_type_from_dtype(dtype), SeriesAbstractNumeric)
        for dtype in dtypes
    ):
        return 'float64'

    # default casting will be as text, this way we avoid any SQL errors
    # when merging different db types into a column
    return 'string'


def escape_parameter_characters(conn: Connection, raw_sql: str) -> str:
    """
    Return a modified copy of the given sql with the query-parameter special characters escaped.
    e.g. if the connection uses '%' to mark a parameter, then all occurrences of '%' will be replaced by '%%'
    """
    # for now we'll just assume Postgres and assume the pyformat parameter style is used.
    # When we support more databases we'll need to do something smarter, see
    # https://www.python.org/dev/peps/pep-0249/#paramstyle
    return raw_sql.replace('%', '%%')


_BQ_COLUMN_NAME_RESERVED_PREFIXES = [
    # https://cloud.google.com/bigquery/docs/schemas#column_names
    '_TABLE_',
    '_FILE_',
    '_PARTITION',
    '_ROW_TIMESTAMP',
    '__ROOT__',
    '_COLIDENTIFIER'
]


def is_valid_column_name(dialect: Dialect, name: str) -> bool:
    """
    Check that the given name is a valid column name in the SQL dialect.
    """
    if is_postgres(dialect):
        # Identifiers longer than 63 characters are not necessarily wrong, but they will be truncated which
        # could lead to identifier collisions, so we just disallow it.
        # source: https://www.postgresql.org/docs/14/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
        return 0 < len(name) < 64
    if is_athena(dialect):
        # Source: https://docs.aws.amazon.com/athena/latest/ug/tables-databases-columns-names.html

        # Only allow lower-case a-z, to make sure we don't have duplicate case-insensitive column names
        regex = '^[a-z0-9_]*$'
        len_ok = 0 < len(name) <= 255
        pattern_ok = bool(re.match(pattern=regex, string=name))
        return len_ok and pattern_ok
    if is_bigquery(dialect):
        # Sources:
        #  https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#column_names
        #  https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#case_sensitivity
        #  https://cloud.google.com/bigquery/docs/schemas#column_names

        # Only allow lower-case a-z, to make sure we don't have duplicate case-insensitive column names
        regex = '^[a-z_][a-z0-9_]*$'
        len_ok = 0 < len(name) <= 300
        pattern_ok = bool(re.match(pattern=regex, string=name))
        prefix_ok = not any(name.startswith(prefix.lower()) for prefix in _BQ_COLUMN_NAME_RESERVED_PREFIXES)
        return len_ok and pattern_ok and prefix_ok
    raise DatabaseNotSupportedException(dialect)


def get_sql_column_name(dialect: Dialect, name: str) -> str:
    """
    Given the name of a series and dialect, return the sql column name.

    If the name contains no characters that require escaping, for the given dialect, then the same string is
    returned. Otherwise, a column name is that can be safely used with the given dialect. The generated name
    will be based on the given name, but with all non-allowed characters filtered out and a hash added.

    **Background**
    Each Bach Series is mapped to a column in queries. Unfortunately, some databases only supported a limited
    set of characters in column names. To work around this limitation we distinguish the Series name from the
    sql-column name. The former is the name a Bach user will see and use, the latter is the name that will
    appear in SQL queries.

    The algorithm we use to map series names to column names is deterministic, but not reversible. That is,
    the same input always yields the same output, and it might be impossible to recover the input from a
    given output.

    :raises ValueError: if name cannot be appropriately escaped or is too long for the given dialect
    :return: column name for the given series name.
    """
    if is_valid_column_name(dialect, name):
        return name

    # If name is not a valid column name in itself. Then transform it:
    # 1) Turn `name` into `cleaned_name`, which only keeps the allowed characters
    # 2) Add a hash of `name` to make the name unique again
    #
    # This process should yield a valid column name for any database, if it's not too long.

    table_upper_to_lower = str.maketrans(string.ascii_uppercase, string.ascii_lowercase)
    chars_lower = set(string.ascii_lowercase)
    chars_numbers = set('0123456789')
    chars_underscore = set('_')
    allowed_chars = chars_lower | chars_numbers | chars_underscore

    # Convert 'name' into cleaned form, in three steps:
    # 1) Normalize the name to the decomposed character form. This will split diacritics of the base
    #    character, e.g. 'ç' will be split in two characters: 'c' and ' ̧'.
    # 2) Lowercase all characters.
    # 3) Filter out all characters that are not in [a-z0-9_]. Example: 'c' would be kept, but ' ̧' would
    #    be filtered out.

    # There are probably better methods, and libraries that have more comprehensive ways of doing this.
    # But for now this works okayish, and is simple.
    # In step 2 we lowercase characters using a translation table. We could probably just do .lower(), but I
    # wasn't 100% sure that works in all locales the same, and the docs were unclear on that.

    decomposed_characters = unicodedata.normalize('NFKD', name)
    decomposed_lowered = decomposed_characters.translate(table_upper_to_lower)
    cleaned_name = ''.join(c for c in decomposed_lowered if c in allowed_chars)
    if not cleaned_name:
        cleaned_name = 'empty'

    if is_bigquery(dialect):
        # Additional rules for BigQuery:
        # 1) Must start with a character a-z or underscore, not with a number
        if cleaned_name[0] in chars_numbers:
            cleaned_name = f'_{cleaned_name}'
        # 2) Cannot start with one of the reserved prefixes:
        if any(cleaned_name.startswith(prefix.lower()) for prefix in _BQ_COLUMN_NAME_RESERVED_PREFIXES):
            cleaned_name = f'x_{cleaned_name}'

    # Add a hash of `name` to make the name unique again.
    # Ten characters of hash (50 bits) should be enough.
    hash = _get_string_hash(name)[:10]
    escaped = f'{cleaned_name}__{hash}'

    if not is_valid_column_name(dialect, escaped):
        raise ValueError(f'Column name "{name}" is not valid for SQL dialect {dialect.name}, and cannot be '
                         f'escaped. Try making the series name shorter and/or using characters [a-z] only.')
    return escaped


def _get_string_hash(input: str) -> str:
    """ Give md5 hash of the given input strings, encoded as a 26 character long base-32 string. """
    # .hexdigest() would give the md5 hash encoded with [a-e0-9], which gives 4 bits per character
    # we'd rather not spend too many characters on the hash, so we base-32 encode the bytes, which gives 5
    # bits per character. Which makes the 128-bit hash fit in 26 characters instead of 32.
    input_bytes = input.encode('utf-8')
    md5_bytes = hashlib.md5(input_bytes).digest()
    hash = base64.b32encode(md5_bytes).decode('utf-8').lower().replace('=', '')
    return hash


def get_name_to_column_mapping(dialect: Dialect, names: Iterable[str]) -> Dict[str, str]:
    """ Give a mapping of series names to sql column names. """
    return {
        name: get_sql_column_name(dialect=dialect, name=name) for name in names
    }


def validate_node_column_references_in_sorting_expressions(
    dialect: Dialect, node: BachSqlModel, order_by: List[SortColumn],
) -> None:
    """
    Validate that all ColumnReferenceTokens in order_by expressions refer columns that exist in node.
    """
    sql_column_names = set(get_sql_column_name(dialect=dialect, name=column) for column in node.series_names)
    for ob in order_by:
        invalid_column_references = [
            token.column_name
            for token in ob.expression.get_all_tokens()
            if isinstance(token, ColumnReferenceToken) and token.column_name not in sql_column_names
        ]
        if invalid_column_references:
            raise ValueError(
                (
                    'Sorting contains expressions referencing '
                    f'non-existent columns in current base node. {invalid_column_references}.'
                    ' Please call DataFrame.sort_values([]) or DataFrame.sort_index() for removing'
                    ' sorting and try again.'
                )
            )


def merge_sql_statements(dialect: Dialect, sql_statements: List[str]) -> List[str]:
    """
    Merge multiple sql statements into one statement with separating semicolons, if the dialect supports
    executing multiple statements in once call to conn.execute(). Otherwise return the original list.
    """
    if is_athena(dialect) or not sql_statements:
        return sql_statements
    combined = '; '.join(sql_statements)
    return [combined]


def athena_construct_engine_url(
    *,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    region_name: str,
    schema_name: str,
    s3_staging_dir: str,
    athena_work_group: Optional[str] = None,
    catalog_name: Optional[str] = None
) -> str:
    """
    Construct a url that can be passed to SqlAlchemy's `create_engine()` to connect to an Athena database.

    Note that the access key and secret access key are not needed for a valid url. Athena libraries will use
    the standard fallback mechanism in case credentials are missing from the url, see
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials

    For more information on

    :param aws_access_key_id: Optional, account to use
    :param aws_secret_access_key: Optional, secret key for account
    :param region_name: region where data is hosted, e.g. 'eu-west-1'
    :param schema_name: Database name
    :param s3_staging_dir: S3 path where query results should be written,
            e.g. 'S3://some_bucket/my_staging_area/'
    :param athena_work_group: Optional, workgroup under which queries will be executed.
    :param catalog_name: Optional, catalog in which table information is stored.
    """
    q_region_name = quote_plus(region_name)
    q_schema_name = quote_plus(schema_name)

    if aws_access_key_id and aws_secret_access_key:
        q_user_pass = f'{quote_plus(aws_access_key_id)}:{quote_plus(aws_secret_access_key)}@'
    elif aws_access_key_id:
        q_user_pass = f'{quote_plus(aws_access_key_id)}@'
    else:
        q_user_pass = ''

    query_string_params = {'s3_staging_dir': s3_staging_dir}
    if athena_work_group is not None:
        query_string_params['work_group'] = athena_work_group
    if catalog_name:
        query_string_params['catalog_name'] = catalog_name

    query_string = urlencode(query_string_params)

    url = (
        f'awsathena+rest://'
        f'{q_user_pass}athena.{q_region_name}.amazonaws.com:443/{q_schema_name}?{query_string}'
    )
    return url
