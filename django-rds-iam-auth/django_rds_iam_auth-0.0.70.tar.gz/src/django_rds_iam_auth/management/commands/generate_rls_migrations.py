import sys

from django.conf import settings
from django.core.management.base import (
    BaseCommand, CommandError, no_translations,
)
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.core.management.commands import makemigrations
from django.db import connections, DEFAULT_DB_ALIAS, router
from django.db.migrations import Migration
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.questioner import NonInteractiveMigrationQuestioner
from django.db.migrations.state import ProjectState

from django_rds_iam_auth.aws.utils.rls_helpers import CreateRLSPolicyOperation


class Command(makemigrations.Command):


    def add_arguments(self, parser):
        parser.add_argument('-a', '--app_name', type=str, help='Add app name for model retrival', )
        parser.add_argument('-ex', '--exclude', type=str, help='List of models to exclude (eg: User,Tenant,Other)')
        parser.add_argument(
            '--dry-run', action='store_true',
            help="Just show what migrations would be made; don't actually write them.",
        )


    def _filter_models(self, models):
        models_to_process = []
        exclude_models = []

        for model in models:
            if model._meta.db_table not in exclude_models:
                models_to_process.append(model)
            # self.stdout.write(self.style.SUCCESS('policy for table "%s"' % model._meta.db_table))
        # remaing_models = list(filter(lambda model: len(list(filter(lambda field: hasattr(field,'c'), model.fields))) > 0, mulist))
        return list(filter(lambda mod: len(list(filter(
            lambda field: hasattr(field, 'column') and (field.column == 'owner_id' or field.column == 'tenant_id'),
            mod._meta.fields))) >= 2, models_to_process))


    def handle(self, *app_labels, **options):
        self.verbosity = options['verbosity']
        self.dry_run = options['dry_run']
        self.interactive = None
        self.merge = None
        self.empty = None
        self.include_header = None
        self.migration_name = ''
        # if self.migration_name and not self.migration_name.isidentifier():
        #     raise CommandError('The migration name must be a valid Python identifier.')

        # Make sure the app they asked for exists
        app_labels = set(options['app_name'].split(','))
        has_bad_labels = False
        for app_label in app_labels:
            try:
                apps.get_app_config(app_label)
            except LookupError as err:
                self.stderr.write(str(err))
                has_bad_labels = True
        if has_bad_labels:
            sys.exit(2)

        # Load the current graph state. Pass in None for the connection so
        # the loader doesn't try to resolve replaced migrations from DB.
        loader = MigrationLoader(None, ignore_no_migrations=True)

        questioner = NonInteractiveMigrationQuestioner(specified_apps=app_labels, dry_run=self.dry_run)
        # Set up autodetector
        autodetector = MigrationAutodetector(
            loader.project_state(),
            ProjectState.from_apps(apps),
            questioner,
        )
        last_migration = None
        app_models = apps.get_app_config(options['app_name']).get_models()
        for item in self._filter_models(app_models):
            self.stdout.write(self.style.SUCCESS('policy for table "%s"' % item._meta.db_table))
        # If they want to make an empty migration, make one for each app
            if not app_labels:
                raise CommandError("You must supply at least one app label when using --empty.")
            # Make a fake changes() result we can pass to arrange_for_graph
            changes = {
                app: [Migration("custom", app)] for app in app_labels
            }
            for app_name, list_of_changes in changes.items():
                for single_chane in list_of_changes:
                    single_chane.operations.append(
                        CreateRLSPolicyOperation(
                            item._meta.db_table,
                            item._meta.db_table +'_table_policy',
                            """(ibrag_is_super_admin(current_user) or (ibrag_user_has_role('tenant_admin') and ibrag_user_has_tenant(tenant_id)) or ibrag_priviliged_is_owner_of_user(owner_id, current_user))""",
                            """(ibrag_is_super_admin(current_user)  or (ibrag_user_has_role('tenant_admin') and ibrag_user_has_tenant(tenant_id)) or ibrag_priviliged_is_owner_of_user(owner_id, current_user))"""
                        )
                    )
                    if last_migration:
                        single_chane.dependencies = [(app_name, last_migration)]

                changes = autodetector.arrange_for_graph(
                    changes=changes,
                    graph=loader.graph,
                    migration_name=str(item._meta.db_table) + '_rls_generated',
                )

                for app_name, soerted_changes in changes.items():
                    for sorted_change in soerted_changes:
                        last_migration = sorted_change.name

                self.write_migration_files(changes)
        self.stdout.write(self.style.SUCCESS('Successfully created rls policies for "%s"' % options['app_name']))
        return


        #############


