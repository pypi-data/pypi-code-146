from typing import Optional

import sqlalchemy as sa
import sqlalchemy.engine as sa_engine
import sqlalchemy.schema as sa_schema

import sqlalchemize.features as features
import sqlalchemize.exceptions as ex


def drop_table(
    table: sa.Table | str,
    engine: Optional[sa_engine.Engine] = None,
    if_exists: bool = True,
    schema: Optional[str] = None
) -> None:
    if isinstance(table, str):
        if table not in sa.inspect(engine).get_table_names(schema=schema):
            if if_exists:
                return
        if engine is None:
            raise ValueError('Must pass engine if table is str.')
        table = features.get_table(table, engine, schema=schema)
    sql = sa_schema.DropTable(table, if_exists=if_exists)
    engine = ex.check_for_engine(table, engine)
    engine.execute(sql)