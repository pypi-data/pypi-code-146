from jija_orm.executors import operators, functions, comparators, sql_object
from jija_orm import executors


table_selector = executors.Executor(
    'pg_catalog.pg_tables',
    operators.Select(name='tablename'),
    operators.Where(
        comparators.Not('schemaname', 'pg_catalog'),
        comparators.Not('schemaname', 'information_schema'),
        comparators.Not('tablename', 'jija_orm'),
        comparators.Like('tablename', sql_object.Param('app')),
    ),
    use_model=False
)

columns_selector = executors.Executor(
    'information_schema.columns',
    operators.Select(
        name='column_name', default='column_default', null='is_nullable',
        type='udt_name', max_length='character_maximum_length'
    ),
    operators.Where(table_name=sql_object.Param('table')),
    use_model=False
)

migration_id_selector = executors.Executor(
    'jija_orm',
    operators.Select(id=functions.Max('id')),
    use_model=False
)

id_setter = executors.Executor(
    'jija_orm',
    operators.Insert(id=sql_object.Param('id')),
    use_model=False
)
