import re
import psycopg2
from py_postgres import QueryFactory


class PyPostgres:
    def __init__(self, db_connection, verbose=False):
        self.verbose = verbose
        if type(db_connection) == dict:
            if ['host', 'port', 'db', 'user', 'pass'] == list(db_connection.keys()):
                if re.match(r'^(\d{1,3}(\.|$)){4}', db_connection['host']):
                    if type(db_connection['port']) == int and db_connection['port'] in range(0, 65536):
                        if type(db_connection['db']) == str \
                                and type(db_connection['user']) == str \
                                and type(db_connection['pass']) == str:
                            self.connection_data = db_connection
                        else:
                            raise ValueError('db, user and pass for the db connection have to be strings')
                    else:
                        raise ValueError('the port number has to be an int between 0 and 65535')
                else:
                    raise ValueError('the field host has to be in format of an ip v4 address')
            else:
                raise ValueError(f'the dict for the db connection has to contain the following values: '
                                 f'[\'host\', \'port\', \'db\', \'user\', \'pass\']')
        else:
            raise TypeError('db connection has to be type dict. see docs for more info.')

    def select(self, select_from, select_select='*', select_where=None, select_left_join=None,
               select_order_by=None, select_order_direction=None):
        with psycopg2.connect(dbname=self.connection_data['db'], user=self.connection_data['user'],
                              password=self.connection_data['pass'], host=self.connection_data['host'],
                              port=self.connection_data['port']) as connection:
            cursor = connection.cursor()
            select_query = QueryFactory.build_select_query(select_from, select_select, select_where, select_left_join,
                                                           select_order_by, select_order_direction)
            if self.verbose is True:
                print(select_query)
            cursor.execute(select_query)

            result = cursor.fetchall()

        return result

    def insert(self, insert_into, columns, values):
        with psycopg2.connect(dbname=self.connection_data['db'], user=self.connection_data['user'],
                              password=self.connection_data['pass'], host=self.connection_data['host'],
                              port=self.connection_data['port']) as connection:
            cursor = connection.cursor()
            insert_query = QueryFactory.build_insert_query(insert_into, columns, values)
            if self.verbose is True:
                print(insert_query, values)
            for value_line in values:
                cursor.execute(insert_query, value_line)

    def update(self, table, set_fields, set_values, where='all'):
        with psycopg2.connect(dbname=self.connection_data['db'], user=self.connection_data['user'],
                              password=self.connection_data['pass'], host=self.connection_data['host'],
                              port=self.connection_data['port']) as connection:
            cursor = connection.cursor()
            update_query = QueryFactory.build_update_query(table, set_fields, set_values, where)
            if self.verbose is True:
                print(update_query)
            cursor.execute(update_query)

    def delete(self, delete_from, delete_where):
        with psycopg2.connect(dbname=self.connection_data['db'], user=self.connection_data['user'],
                              password=self.connection_data['pass'], host=self.connection_data['host'],
                              port=self.connection_data['port']) as connection:
            cursor = connection.cursor()
            update_query = QueryFactory.build_delete_query(delete_from, delete_where)
            if self.verbose is True:
                print(update_query)
            cursor.execute(update_query)
