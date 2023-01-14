from jija_orm import config
from jija_orm.migrator import selectors
from jija_orm.migrator import templates


class Migrator:
    @classmethod
    async def migrate(cls):
        # tables_migrations = await cls.__get_tables_migrations()
        # print(tables_migrations) # TODO

        models_migrations = cls.__get_models_migrations()
        exist_migrations = cls.__get_exist_migrations()
        migrations_by_migrations = cls.__get_differences(models_migrations, exist_migrations)
        await cls.__write_migrations(migrations_by_migrations)

    @classmethod
    async def __get_tables_migrations(cls):
        apps = config.JijaORM.get_apps_names()

        migrations = []
        for app in apps:
            migration = await templates.AppMigration.from_table(app)
            migration and migrations.append(migration)

        return migrations

    @classmethod
    def __get_models_migrations(cls):
        apps_models = config.JijaORM.get_models()

        migrations = []
        for app_name in apps_models:
            migration = templates.AppMigration.from_models(app_name, apps_models[app_name])
            migration and migrations.append(migration)

        return migrations

    @classmethod
    def __get_exist_migrations(cls):
        raw_app_migrations = config.JijaORM.get_migrations()

        migrations = []
        for app_name in raw_app_migrations:
            app_migration = None
            for raw_migration in raw_app_migrations[app_name]:
                migration = templates.AppMigration.from_migration(app_name, raw_migration)
                app_migration = templates.AppMigration.sqwash(app_migration, migration)

            app_migration and migrations.append(app_migration)

        return migrations

    @staticmethod
    def __get_differences(one, two):
        one_dict = dict(map(lambda mig: (mig.app, mig), one))
        two_dict = dict(map(lambda mig: (mig.app, mig), two))

        differences = []
        for name in {*one_dict, *two_dict}:
            difference = templates.AppMigration.difference(one_dict.get(name), two_dict.get(name))
            if difference:
                differences.append(difference)

        return differences

    @staticmethod
    async def __write_migrations(migrations: list[templates.AppMigration]):
        for migration in migrations:
            await migration.write()

    @classmethod
    async def __get_migrations_to_execute(cls) -> list[templates.Migration]:
        executed_id = (await selectors.migration_id_selector.execute())[0]['id']
        exist_migrations = config.JijaORM.get_migrations()

        migrations = []
        for app_name in exist_migrations:
            for app_migration in exist_migrations[app_name]:
                if executed_id and app_migration.id <= executed_id:
                    continue

                migrations.append(app_migration)

        return sorted(migrations, key=lambda migration: migration.id)

    @classmethod
    async def update(cls):
        migrations = await cls.__get_migrations_to_execute()

        for migration in migrations:
            await migration.execute()
            await selectors.id_setter.execute(id=migration.id)
