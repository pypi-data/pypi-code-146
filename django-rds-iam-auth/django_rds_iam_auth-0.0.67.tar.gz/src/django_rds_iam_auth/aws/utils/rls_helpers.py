import sys

import psycopg2
from django.db.migrations.operations.base import Operation
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

RLS_EXPLICIT_TYPE_SELECT = 'SELECT'
RLS_EXPLICIT_TYPE_UPDATE = 'UPDATE'
RLS_EXPLICIT_TYPE_INSERT = 'INSERT'
RLS_EXPLICIT_TYPE_DELETE = 'DELETE'

class CreateRLSPolicyOperation(Operation):

    reversible = True
    choices = None

    def __init__(self, table_name, policy_name, useing_rule=None, with_check_rule=None):
        self.table_name = table_name
        self.policy_name = policy_name
        self.useing_rule = useing_rule
        self.with_check_rule = with_check_rule

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        settings = schema_editor.connection.settings_dict
        connection = psycopg2.connect(user=settings['USER'],
                                      password=settings['PASSWORD'],
                                      host=settings['HOST'],
                                      port=settings['PORT'],
                                      database=settings['NAME'])
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        try:
            # schema_editor.execute("drop policy %s on %s;" % (self.policy_name, self.table_name))
            cursor.execute("drop policy %s on %s;" % (self.policy_name, self.table_name))
        except Exception as ex:
            sys.stdout.write(str(ex))

        query = 'CREATE POLICY {} ON {} USING {} WITH CHECK {} ;'.format(self.policy_name, self.table_name, self.useing_rule, self.with_check_rule)
        cursor.execute(query)


    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("drop policy %s on %s;" % (self.policy_name, self.table_name))

    def describe(self):
        return "Creates policy if exists %s for table %s" % (self.policy_name, self.table_name)


class RunSimpleMigrationInIsolationMode(Operation):
    reversible = True
    choices = None

    def __init__(self, table_name, migrationSql=''):
        self.table_name = table_name
        self.sql = migrationSql

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        settings = schema_editor.connection.settings_dict
        connection = psycopg2.connect(user=settings['USER'],
                                      password=settings['PASSWORD'],
                                      host=settings['HOST'],
                                      port=settings['PORT'],
                                      database=settings['NAME'])
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        try:
            cursor.execute(self.sql)
        except Exception as ex:
            sys.stdout.write(str(ex))

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("drop policy %s on %s;" % (self.policy_name, self.table_name))

    def describe(self):
        return "Creates policy %s for table %s" % (self.policy_name, self.table_name)

class CreateRLSPolicyExplicitOperation(Operation):

    reversible = True
    choices = None

    def __init__(self, table_name, policy_name, policy_explicit_type=RLS_EXPLICIT_TYPE_SELECT, useing_rule=None, with_check_rule=None):
        self.table_name = table_name
        self.policy_name = policy_name
        self.useing_rule = useing_rule
        self.with_check_rule = with_check_rule
        self.policy_explicit_type = policy_explicit_type

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        settings = schema_editor.connection.settings_dict
        connection = psycopg2.connect(user=settings['USER'],
                                      password=settings['PASSWORD'],
                                      host=settings['HOST'],
                                      port=settings['PORT'],
                                      database=settings['NAME'])
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        try:
            # schema_editor.execute("drop policy %s on %s;" % (self.policy_name, self.table_name))
            cursor.execute("drop policy if exists %s on %s;" % (self.policy_name, self.table_name))
            t=2
        except Exception as ex:
            sys.stdout.write(str(ex))


        query = {
            RLS_EXPLICIT_TYPE_SELECT: 'CREATE POLICY {} ON {} FOR {} USING {};'.format(
                self.policy_name, self.table_name, RLS_EXPLICIT_TYPE_SELECT, self.useing_rule),
            RLS_EXPLICIT_TYPE_DELETE: 'CREATE POLICY {} ON {} FOR {} USING {};'.format(
                self.policy_name, self.table_name, RLS_EXPLICIT_TYPE_SELECT, self.useing_rule)
        }.get(self.policy_explicit_type, 'CREATE POLICY {} ON {} FOR {} WITH CHECK {} ;'.format(
            self.policy_name, self.table_name, self.policy_explicit_type, self.with_check_rule))
        cursor.execute(query)


    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("drop policy %s on %s;" % (self.policy_name, self.table_name))

    def describe(self):
        return "Creates policy %s for table %s" % (self.policy_name, self.table_name)