import asyncio
import importlib
import os.path

from typing import Optional

from jija_orm import utils, models
from jija_orm import executors
from jija_orm import exceptions


class App:
    def __init__(
            self, *, name: str, path: str = None, models_modules: Optional[str] = None,
            migration_dir: Optional[str] = None):

        """
        :param name: App name
        :param path: App path by base path from core, if path is None it will be same as name
        :param models_modules: List of models files, if it is None it will be [models]
        :param migration_dir: Directory for app migrations, if it is None it will be "migrations.{app_name}"
        """

        self.__name = name

        self.__path = path or name
        self.__models_modules = self.__validate_models(models_modules)
        self.__migration_dir = self.__validate_migration_dir(migration_dir)

        self.__models = None

    @property
    def name(self):
        return self.__name

    @property
    def migrations_dir(self):
        return self.__migration_dir

    @property
    def models(self):
        return self.__models

    @staticmethod
    def __validate_models(models_modules):
        if models_modules is None:
            return ['models']

        if not isinstance(models_modules, (list, tuple)):
            raise exceptions.AppConfigTypeError(models_modules)

        return models_modules

    def __validate_migration_dir(self, migration_dir):
        if migration_dir:
            return migration_dir

        return f'migrations.{self.__name}'

    def check(self, base_path):
        for app_models in self.__models_modules:
            path = base_path.joinpath(self.__path.replace('.', '/'), app_models.replace('.', '/') + '.py')
            if not os.path.exists(path):
                raise exceptions.AppConfigImportError(path)

        self.__create_migrations_dir()

    def load(self):
        self.__load_models()
        asyncio.run(self.__load_migrations_table())

    async def async_load(self):
        self.__load_models()
        await self.__load_migrations_table()

    def __load_models(self):
        app_models = {}
        for model_module in self.__models_modules:
            module = importlib.import_module(f'{self.__path}.{model_module}')
            app_models.update(map(
                lambda model_class: (model_class.get_name(), model_class),
                utils.collect_subclasses(module, models.Model)
            ))

        for model_name in app_models:
            app_models[model_name].init_managers()

        self.__models = app_models

    @staticmethod
    async def __load_migrations_table():
        from jija_orm.migrator import templates
        from jija_orm.executors import operators, comparators

        executor = executors.Executor(
            'pg_catalog.pg_tables',
            operators.Select(name='tablename'),
            operators.Where(
                comparators.Not('schemaname', 'pg_catalog'),
                comparators.Not('schemaname', 'information_schema'),
                tablename='jija_orm',
            ),
            use_model=False
        )

        if len(await executor.execute()) == 0:
            migration = templates.ModelMigration(
                'jija_orm', templates.Action.CREATE,
                [
                    templates.FieldMigration(
                        'id', templates.Action.CREATE,
                        [
                            templates.AttributeMigration('pk', True),
                            templates.AttributeMigration('null', False),
                            templates.AttributeMigration('type', 'int8')
                        ]
                    )
                ],

            )

            await migration.execute()

    def __create_migrations_dir(self):
        current_path = []
        path = self.__migration_dir.split('.')
        for directory in path:
            dir_to_create = '/'.join(current_path + [directory])
            if not os.path.exists(dir_to_create):
                os.mkdir(dir_to_create)

            current_path.append(directory)

    def get_migrations(self):
        migrations = []
        for path in os.listdir(self.migrations_dir.replace('.', '/')):
            if not path.endswith('.py'):
                continue

            module_path = f'{self.__migration_dir}.{path.replace(".py", "")}'
            module = importlib.import_module(module_path)
            migrations.append(module.Migration)

        return migrations
