import fire
from sqlalchemy.exc import ProgrammingError

from reljicd_utils.rdbms.scoped_session import engine

SCHEMAS = ['public']


def set_all_sequences() -> None:
    for schema in SCHEMAS:
        tables = [row[0] for row in engine.execute(
            f"SELECT table_name FROM information_schema.tables "
            f"WHERE table_schema = '{schema}'")]

        for table in tables:
            try:
                set_sequence(schema, table)
            except ProgrammingError:
                print(f'[Table: {table}] skipped')


def set_sequence(schema: str, table: str) -> None:
    engine.execute(
        f"SELECT pg_catalog.setval(pg_get_serial_sequence("
        f"'{schema}.{table}', 'id'), "
        f"MAX(id)) FROM {schema}.{table}")


if __name__ == '__main__':
    fire.Fire(set_all_sequences)
