from typing import List

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.exc import ProgrammingError

from reljicd_utils.logger import get_logger
from reljicd_utils.rdbms import engine

LOGGER = get_logger(__name__)


def schema_tables(schema: str) -> List[str]:
    return [row[0] for row in engine.execute(
        f"SELECT table_name FROM information_schema.tables "
        f"WHERE table_schema = '{schema}'")]


def execute_statement(statement: str) -> None:
    try:
        connection = engine.raw_connection()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(statement)
        cursor.close()
    except ProgrammingError:
        LOGGER.error(f'Failed execution of: "{statement}"')
