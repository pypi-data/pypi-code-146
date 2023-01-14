from typing import List

import fire

from reljicd_utils.logger.logger import get_logger
from reljicd_utils.rdbms.set_sequences import SCHEMAS
from reljicd_utils.rdbms.utils import execute_statement, schema_tables

LOGGER = get_logger(__name__)


def reindex_schemas(schemas: List = SCHEMAS) -> None:
    for schema in schemas:
        for table in schema_tables(schema):
            reindex_schema_table(schema, table)


def reindex_schema_table(schema: str, table: str) -> None:
    LOGGER.info(f'REINDEX TABLE {schema}.{table} ...')
    execute_statement(f'REINDEX TABLE {schema}.{table}')
    LOGGER.info(f'REINDEX TABLE {schema}.{table} done')


if __name__ == '__main__':
    fire.Fire(reindex_schemas)
