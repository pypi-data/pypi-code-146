from typing import Dict

import fire
from sqlalchemy import inspect
from sqlalchemy.sql.ddl import CreateSchema, DropSchema

from reljicd_utils.rdbms import engine, transaction

PUBLIC_SCHEMA = 'public'
BASES = []
SCHEMAS_BASES = {base.metadata.schema: base for base in BASES}

# Fix for postgres
SCHEMAS_BASES[PUBLIC_SCHEMA] = SCHEMAS_BASES[None]
del SCHEMAS_BASES[None]


@transaction
def recreate_schema(schema: str,
                    schema_bases: Dict = None) -> None:
    if schema_bases is None:
        schema_bases = SCHEMAS_BASES

    if schema not in schema_bases:
        raise AttributeError

    if schema in inspect(engine).get_schema_names():
        print(f'Dropping {schema} schema...')
        engine.execute(DropSchema(name=schema, cascade=True))

    print(f'Creating {schema} schema...')
    engine.execute(CreateSchema(name=schema))
    # inside "create the database" script, first create tables:
    schema_bases[schema].metadata.create_all(engine)
    print(f'Created {schema} schema.')

    inspector = inspect(engine)
    assert schema in inspector.get_schema_names()


if __name__ == '__main__':
    fire.Fire(recreate_schema)
