import datetime
from typing import Optional

import aiofile

from jija_orm.migrator import selectors
from jija_orm import config, fields
from jija_orm import utils


class Action:
    CREATE = 'create'
    DROP = 'drop'
    ALTER = 'alter'


class __BaseMigrator:
    def __init__(self, name: str, action: str, childes: list):
        self.__name = name
        self.__action = action
        self.__childes = childes

    @property
    def name(self):
        return self.__name

    @property
    def action(self):
        return self.__action

    @property
    def childes(self):
        return self.__childes

    @property
    def childes_dict(self):
        return dict(map(lambda child: (child.name, child), self.__childes))

    def copy(self):
        return self.__class__(self.name, self.action, list(map(lambda child: child.copy(), self.childes)))

    @classmethod
    def sqwash(
            cls,
            oldest: Optional['__BaseMigrator'],
            newest: Optional['__BaseMigrator']
    ) -> Optional['__BaseMigrator']:

        if not newest or not oldest:
            if not newest and not oldest:
                return

            if newest and newest.action != Action.CREATE:
                raise AttributeError

            to_return = newest or oldest
            return cls(to_return.name, to_return.action, list(map(lambda child: child.copy(), to_return.childes)))

        if not type(newest) == type(oldest):
            raise TypeError(type(newest), type(oldest))

        if oldest.action == Action.CREATE:
            if newest.action == Action.DROP:
                return None

        if oldest.action == Action.DROP:
            if newest.action == Action.CREATE:
                return cls(newest.name, Action.CREATE, newest.childes.copy())

            if oldest.action == Action.DROP:
                return cls(newest.name, Action.DROP, [])

            raise AttributeError()

        if oldest.action == Action.ALTER:
            if newest.action == Action.CREATE:
                raise AttributeError()

            if newest.action == Action.DROP:
                return cls(newest.name, Action.DROP, [])

        newest_dict = newest.childes_dict
        oldest_dict = oldest.childes_dict

        childes = []
        for field_name in {*oldest_dict, *newest_dict}:
            child_class = newest_dict.get(field_name) or oldest_dict.get(field_name)

            field = child_class.sqwash(oldest_dict.get(field_name), newest_dict.get(field_name))
            if field:
                childes.append(field)

        return cls(newest.name, oldest.action, childes)

    @classmethod
    def difference(
            cls,
            newest: Optional['__BaseMigrator'],
            oldest: Optional['__BaseMigrator']
    ) -> Optional['__BaseMigrator']:
        if newest == oldest:
            return

        if not newest:
            if oldest.action == Action.DROP:
                return

            return cls(oldest.name, Action.DROP, [])

        if not oldest:
            if newest.action != Action.CREATE:
                raise AttributeError()

            return cls(newest.name, Action.CREATE, list(map(lambda child: child.copy(), newest.childes)))

        if not type(newest) == type(oldest):
            raise TypeError(type(newest), type(oldest))

        if newest.action == Action.CREATE:
            if oldest.action == Action.DROP:
                return cls(newest.name, Action.CREATE, list(map(lambda child: child.copy(), newest.childes)))

            if oldest.action == Action.ALTER:
                raise AttributeError()

        if newest.action == Action.DROP:
            if oldest.action == Action.DROP:
                return

            return cls(newest.name, Action.DROP, [])

        if newest.action == Action.ALTER:
            if oldest.action == Action.CREATE:
                raise AttributeError()

            if oldest.action == Action.DROP:
                return cls(newest.name, Action.ALTER, list(map(lambda child: child.copy(), newest.childes)))

        newest_dict = newest.childes_dict
        oldest_dict = oldest.childes_dict

        childes = []
        for field_name in {*oldest_dict, *newest_dict}:
            child_class = newest_dict.get(field_name) or oldest_dict.get(field_name)

            field = child_class.difference(newest_dict.get(field_name), oldest_dict.get(field_name))
            if field:
                childes.append(field)

        if not childes:
            return

        if oldest.action == Action.DROP:
            action = Action.CREATE
        else:
            action = Action.ALTER

        return cls(newest.name, action, childes)

    def get_constructor(self):
        childes = []
        for child in self.childes:
            childes.extend(map(lambda line: f'        {line}', child.get_constructor()))

        return [
            f'templates.{self.__class__.__name__}(',
            f'    name="{self.name}",',
            f'    action=templates.Action.{self.action.upper()},',
            f'    childes=[',
            *childes,
            f'    ]',
            '),'
        ]

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.name == other.name and \
               self.action == other.action and \
               self.__eq_childes(other)

    def __eq_childes(self, other):
        self_childes = self.childes_dict
        other_childes = other.childes_dict

        for child in self_childes:
            other_child = other_childes.pop(child, None)
            if self_childes[child] != other_child:
                return False

        if other_childes:
            return False

        return True

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.__action} {self.__name}>'

    def get_query(self, *args, **kwargs):
        raise NotImplementedError()


class AppMigration:
    def __init__(self, app, migrations):
        self.__app = app
        self.__migrations = migrations

    @property
    def app(self):
        return self.__app

    @property
    def migrations(self):
        return self.__migrations

    @property
    def migrations_dict(self):
        return dict(map(lambda child: (child.name, child), self.__migrations))

    @classmethod
    async def from_table(cls, app: str) -> Optional['AppMigration']:
        migrations = []

        for table_record in await selectors.table_selector.execute(app=app):
            migrations.append(await ModelMigration.from_table(table_record['name']))

        if not migrations:
            return

        return cls(app, migrations)

    @classmethod
    def from_models(cls, app: str, models: list) -> Optional['AppMigration']:
        migrations = []

        for model in models:
            migrations.append(ModelMigration.from_model(model))

        if not migrations:
            return

        return cls(app, migrations)

    @classmethod
    def from_migration(cls, app: str, migration: 'Migration'):
        migrations = []

        for command in migration.commands:
            migrations.append(command)

        return cls(app, migrations)

    @classmethod
    def sqwash(cls, oldest: Optional['AppMigration'], newest: Optional['AppMigration']) -> Optional['AppMigration']:
        if not oldest or not newest:
            return oldest or newest

        newest_dict = newest.migrations_dict
        oldest_dict = oldest.migrations_dict

        migrations = []
        for migration_name in {*oldest_dict, *newest_dict}:
            field = ModelMigration.sqwash(oldest_dict.get(migration_name), newest_dict.get(migration_name))
            field and migrations.append(field)

        return cls(newest.app, migrations) if migrations else None

    @classmethod
    def difference(cls, newest: Optional['AppMigration'], oldest: Optional['AppMigration']) -> Optional['AppMigration']:
        if newest == oldest:
            return

        if not newest:
            return

        if not oldest:
            return cls(newest.app, list(map(lambda migration: migration.copy(), newest.migrations)))

        newest_dict = newest.migrations_dict
        oldest_dict = oldest.migrations_dict

        differences = []
        for name in {*newest_dict, *oldest_dict}:
            difference = ModelMigration.difference(newest_dict.get(name), oldest_dict.get(name))
            difference and differences.append(difference)

        return cls(newest.app, differences) if differences else None

    async def write(self):
        migration_dir = config.JijaORM.get_migrations_dir(self.app)
        migration_id, constructor = Migration.get_constructor(self.migrations)

        path = migration_dir.replace('.', '/') + f'/{migration_id}.py'
        async with aiofile.async_open(path, 'w') as file:
            print(f'Creating migration manifest {path}')
            await file.write(constructor)

    def __repr__(self):
        return f'<AppMigration {self.app}>'


class ModelMigration(__BaseMigrator):
    @classmethod
    def from_model(cls, model):
        return cls(
            model.get_name(), Action.CREATE,
            [*cls.__get_fields(model), *cls.__get_constraints(model)]
        )

    @classmethod
    def __get_fields(cls, model):
        raw_fields = model.get_fields()
        return list(map(lambda field_name: FieldMigration.from_field(field_name, raw_fields[field_name]), raw_fields))

    @classmethod
    def __get_constraints(cls, model):
        raw_constraints = model.get_constraints()

        childes = []
        for constraint_name in raw_constraints:
            childes.append(FieldMigration.from_field(f'{constraint_name}_id', raw_constraints[constraint_name]))
            childes.append(ConstraintMigration.from_field(constraint_name, raw_constraints[constraint_name]))

        return childes

    @classmethod
    async def from_table(cls, table):
        raw_columns = await cls.__get_field_data(table)

        return cls(
            table, Action.CREATE,
            list(map(lambda column: FieldMigration.from_column(column), raw_columns))
        )

    @staticmethod
    async def __get_field_data(table):
        return await (await config.JijaORM.get_connection()).fetch(f"""
            select
                column_name as "name",
                column_default as "default",
                is_nullable as "null",
            
                (case when udt_name = 'varchar' then concat(udt_name, '(', character_maximum_length, ')')
                 else udt_name end) as type,
            
                column_name = (select pg_attribute.attname::text
                 from pg_index,
                      pg_class,
                      pg_attribute,
                      pg_namespace
                 where pg_class.oid = '{table}'::regclass
                   and indrelid = pg_class.oid
                   AND nspname = 'public'
                   AND pg_class.relnamespace = pg_namespace.oid
                   AND pg_attribute.attrelid = pg_class.oid
                   AND pg_attribute.attnum = any (pg_index.indkey)
                   AND indisprimary) as pk
            
            from information_schema.columns
            where table_name = '{table}'
                """)

    async def execute(self):
        query = self.get_query()

        connection = await config.JijaORM.get_connection()
        await connection.execute(query)

    def get_query(self):
        if self.action == Action.DROP:
            return f'drop table "{self.name}"'

        childes = self.__sort_childes()
        childes_query = ', '.join(map(lambda field: field.get_query(self.action), childes))

        if self.action == Action.CREATE:
            return f'create table "{self.name}" ({childes_query})'

        else:
            return f'alter table "{self.name}" {childes_query}'

    def __sort_childes(self) -> list:
        childes = sorted(self.childes, key=lambda _child: isinstance(_child, FieldMigration))

        if self.action == Action.CREATE:
            return childes

        constraint_indexes = {}
        field_indexes = {}
        for index, child in enumerate(childes):
            if isinstance(child, FieldMigration):
                field_indexes[child.name.replace('_id', '')] = index
            else:
                constraint_indexes[child.name] = index

        if not constraint_indexes:
            return childes

        for name in constraint_indexes:
            pair = [childes[field_indexes[name]], childes[constraint_indexes[name]]]
            if childes[constraint_indexes[name]].action == Action.DROP:
                pair = list(reversed(pair))

            for attr in pair:
                childes.remove(attr)

            childes.extend(pair)

        return childes


class FieldMigration(__BaseMigrator):
    @classmethod
    def from_field(cls, name, field):
        if isinstance(field, fields.Field):
            childes = [
                    AttributeMigration('pk', field.pk),
                    AttributeMigration('null', field.null),
                    AttributeMigration('type', field.get_type()),
                ]

            if field.default is not utils.NotSet:
                childes.append(AttributeMigration('default', field.default))

            return cls(name, Action.CREATE, childes)

        if isinstance(field, fields.RelatedField):
            return cls(
                name,
                Action.CREATE,
                [
                    AttributeMigration('null', field.null),
                    AttributeMigration('type', fields.IntegerField.SQL_TYPE),
                ]
            )

        raise TypeError(type(field))

    @classmethod
    def from_column(cls, column):
        return cls(
            column['name'],
            Action.CREATE,
            [
                AttributeMigration('pk', column['pk']),
                AttributeMigration('default', column['default']),
                AttributeMigration('null', column['null']),
                AttributeMigration('type', column['type']),
            ]
        )

    # def get_model_create_query(self):
    #     attrs = sorted(self.childes, key=lambda attr: attr.priority, reverse=True)
    #     attrs_query = ' '.join(list(filter(lambda attr: attr, map(lambda attr: attr.get_create_query(), attrs))))
    #     return f"{self.name} {attrs_query}"

    def get_query(self, model_action):
        if self.action == Action.DROP:
            return f'drop column "{self.name}"'

        elif self.action == Action.ALTER:
            return self.__get_alter_query()

        else:
            return self.__get_create_query(model_action)

    def __get_alter_query(self):
        query_lines = []
        for attr in self.childes:
            child_query = attr.get_query(Action.ALTER)
            child_query and query_lines.append(f'alter column "{self.name}" {child_query}')

        return ', '.join(query_lines)

    def __get_create_query(self, model_action):
        attrs = sorted(self.childes, key=lambda attr: attr.priority)

        attrs_query = ' '.join(
            filter(lambda attr: attr,
                   map(lambda attr: attr.get_query(self.action),
                       attrs)
                   )
        )
        query = f'"{self.name}" {attrs_query}'

        if model_action != Action.CREATE:
            query = f'add column {query}'

        return query


class ConstraintMigration(__BaseMigrator):
    @classmethod
    def from_field(cls, name, field):
        return cls(
            name, Action.CREATE,
            [
                ConstraintAttributeMigration('field', f'{name}_id'),
                ConstraintAttributeMigration('relation_to', field.relation_to),
                ConstraintAttributeMigration('on_delete', field.on_delete),
            ]
        )

    @classmethod
    def from_column(cls):
        raise NotImplementedError()

    def get_query(self, model_action):
        attrs = sorted(self.childes, key=lambda attr: attr.priority)
        attrs_query = " ".join(map(lambda attr: attr.get_query(self.action), attrs))

        query = f'constraint "{self.name}" {attrs_query}'

        if self.action == Action.CREATE:
            action_query = 'add'
        else:
            action_query = self.action

        if model_action != Action.CREATE:
            query = f'{action_query} {query}'

        return query


class __BaseAttributeMigration:
    PRIORITY: dict = NotImplemented

    def __init__(self, name, value):
        self.__name = name
        self.__value = value
        self.__priority = self.PRIORITY.get(name, 999)

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def priority(self):
        return self.__priority

    def copy(self):
        return self.__class__(self.name, self.value)

    @classmethod
    def sqwash(cls, oldest: Optional['__BaseAttributeMigration'], newest: Optional['__BaseAttributeMigration']
               ) -> '__BaseAttributeMigration':

        return newest or oldest

    @classmethod
    def difference(cls, newest: Optional['__BaseAttributeMigration'], oldest: Optional['__BaseAttributeMigration']
                   ) -> Optional['__BaseAttributeMigration']:

        if not newest:
            return

        if not oldest:
            return newest

        if not type(newest) == type(oldest):
            raise TypeError(type(newest), type(oldest))

        if newest.value == oldest.value:
            return

        return cls(newest.name, newest.value)

    def get_query(self, model_action):
        raise NotImplementedError()

    def get_constructor(self):
        return [f'templates.{self.__class__.__name__}('f'name="{self.name}", value={self.__get_constructor_value()}),']

    def __get_constructor_value(self):
        if self.value is None or isinstance(self.value, bool):
            return self.value

        if isinstance(self.value, str):
            return f'"{self.value}"'

        return self.value

    def __eq__(self, other: '__BaseAttributeMigration') -> bool:
        return isinstance(other, self.__class__) and \
               self.name == other.name and \
               self.value == other.value and \
               self.priority == other.priority

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.name} {self.value}>'


class AttributeMigration(__BaseAttributeMigration):
    PRIORITY = {'type': 0}
    ATTRS_TRANSLATOR = {
        'type': 'type {}',
        'pk': '{} primary key',
        'null': '{} not null',
        'default': '{} default'
    }

    def get_query(self, field_action):
        return getattr(self, f'_{self.__class__.__name__}__get_{self.name}')(field_action)

    def __get_type(self, field_action):
        if field_action == Action.CREATE:
            return self.value

        return f'type {self.value}'

    def __get_null(self, field_action):
        if field_action == Action.ALTER:
            return f'{"drop" if self.value else "set"} not null'

        if not self.value:
            return 'not null'

    def __get_pk(self, field_action):
        if field_action == Action.ALTER:
            return f'{"set" if self.value else "drop"} primary key'

        if self.value:
            return 'primary key generated by default as identity'

    def __get_default(self, field_action):
        if self.value is None:
            query = 'default null'
        elif isinstance(self.value, int):
            query = f'default {self.value}'
        else:
            query = f'default "{self.value}"'

        if field_action == Action.CREATE:
            return query
        return f'set {query}'


class ConstraintAttributeMigration(__BaseAttributeMigration):
    PRIORITY = {
        'field': 0,
        'relation_to': 1,
        'on_delete': 2
    }

    ATTRS_TRANSLATOR = {
        'field': 'foreign key ("{}")',
        'relation_to': 'references "{}"(id)',
        'on_delete': 'on delete {}'
    }

    def get_query(self, model_action):
        return self.ATTRS_TRANSLATOR[self.name].format(self.value)


class Migration:
    id: int = NotImplemented
    commands: tuple[ModelMigration] = NotImplemented

    @classmethod
    async def execute(cls):
        for command in cls.commands:
            await command.execute()

    @staticmethod
    def get_constructor(commands):
        commands_lines = []
        for command in commands:
            commands_lines.extend(map(lambda line: f'        {line}', command.get_constructor()))

        now = datetime.datetime.now()
        migration_id = int(datetime.datetime.now().timestamp() * 1000000)
        template = [
            f'# Created by jija-orm at {now.replace(microsecond=0)}',
            'from jija_orm.migrator import templates',
            '',
            '',
            f'class Migration(templates.Migration):',
            f'    id = {migration_id}',
            '    commands = (',
            *commands_lines,
            '    )',
            ''
        ]

        return migration_id, '\n'.join(template)
