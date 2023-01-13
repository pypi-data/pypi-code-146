
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import


'''
    Module containing the MySQLDatabase class declaration.

    This is used to connect to a remote MySQL database and allows slightly abstracted
    methods for manipulating it.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-13-2022 12:42:25
    `memberOf`: MySQL
'''


import datetime
from dataclasses import dataclass
import json
import re as re
import os

import sys

from typing import Iterable, Union


import mysql.connector as _mysqlConnector
import traceback as _traceback
from mysql.connector import Error
from colemen_config import _db_column_type,_db_table_type,_db_mysql_delete_query_type,_db_mysql_select_query_type,_db_mysql_update_query_type,_db_mysql_insert_query_type,_db_relationship_type,_db_mysql_manager_type

# import colemen_utilities.file_utils as _cfu
# import colemen_utilities.directory_utils as _dirs
# import colemen_utilities.list_utils as _lu
import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj

from colemen_utilities.database_utils.MySQL.InsertQuery import InsertQuery
from colemen_utilities.database_utils.MySQL.SelectQuery import SelectQuery
from colemen_utilities.database_utils.MySQL.UpdateQuery import UpdateQuery
from colemen_utilities.database_utils.MySQL.DeleteQuery import DeleteQuery
from colemen_utilities.database_utils.MySQL.Table import Table
from colemen_utilities.database_utils.MySQL.Relationship import Relationship
from colemen_utilities.database_utils.MySQL.Column import Column


import colemen_utilities.console_utils as _con
_log = _con.log


@dataclass
class MySQLDatabase:
    database:str = None
    '''The name of the database/schema this instance represents.'''

    user:str = None
    '''The user name used to connect to the database.'''

    password:str = None
    '''The password used to connect to the database.'''

    host:str = None
    '''The host address used to connect to the database'''

    no_caching:bool = False
    '''If True, no cache files will be created, this really slows shit down..'''

    cache_path:str = None
    '''File path to the directory where table cache files are stored.

    Defaults to: {cwd}/db_cache
    '''

    get_limit:int = 100
    '''The default LIMIT applied to select queries'''

    _dbm:_db_mysql_manager_type = None
    '''The database manager instance used to manage multiple schemas'''

    _table_relationships = None
    '''A list of all table relationships retrieved from the database'''


    # ------------------------------- SUB-ENTITIES ------------------------------- #

    _tables = None
    '''A dictionary of table instances the keys correspond to the table's name for quick lookups.'''

    _relationships = None
    '''A list of relationship instances'''

    _columns = None
    '''A list of column instances'''



    def __init__(self,**kwargs):
        '''
            Create a new MySQL database connection.
            ----------


            Keyword Arguments
            -------------------------
            `database` {str}
                The name of the database/schema this instance represents.

            `user` {str}
                The user name used to connect to the database.

            `password` {str}
                The password used to connect to the database.

            `host` {str}
                The host address used to connect to the database

            `cache_path` {str}
                The path to the directory where the table cache files can be saved.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:30:55
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: MySQLDatabase
            * @xxx [12-13-2022 12:31:27]: documentation for MySQLDatabase
        '''

        self.database:str = _obj.get_kwarg(['database','name'],None,(str),**kwargs)
        self.user:str = _obj.get_kwarg(['user'],None,(str),**kwargs)
        self.password:str = _obj.get_kwarg(['password'],None,(str),**kwargs)
        self.host:str = _obj.get_kwarg(['host'],None,(str),**kwargs)
        self.cache_path:str = _obj.get_kwarg(['cache_path'],f"{os.getcwd()}/db_cache",(str),**kwargs)
        self.no_caching:bool = _obj.get_kwarg(['no_caching'],False,(bool),**kwargs)
        self._dbm:_db_mysql_manager_type = _obj.get_kwarg(['database_manager'],None,None,**kwargs)

        self._credentials:bool = None
        '''True if the credentials dictionary can be successfully compiled.'''


        self.con = None
        self.cur = None


        # initialize these attributes for later use.
        self._tables = {}
        self._relationships = []
        self._columns = []


        self.connect()
        if self._dbm is not None:
            self._dbm.register(self)


    @property
    def summary(self):
        '''
            Get the summary dictionary for this database.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:21:04
            `@memberOf`: MySQLDatabase
            `@property`: summary
        '''
        value = {
            "schema":self.database,
        }
        # print(f"self._tables:{self._tables}")
        value['tables'] = { k:v.summary for (k,v) in self._tables.items()}
        # value['tables'] = [x.summary for x in self._tables]

        return value

    # def save(self):
    #     table:_db_table_type
    #     for _,table in self._tables.items():
    #         table.cache.save()
        # _cfu.writer.to_json(f"{self.cache_path}/db_summary.json",self.summary)


    # ---------------------------------------------------------------------------- #
    #                                 GENERAL DATA                                 #
    # ---------------------------------------------------------------------------- #

    @property
    def name(self):
        '''
            Get this MySQLDatabase's name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 10:11:26
            `@memberOf`: MySQLDatabase
            `@property`: name
        '''
        return self.database



    # ---------------------------------------------------------------------------- #
    #                                  CONNECTION                                  #
    # ---------------------------------------------------------------------------- #


    @property
    def __credentials(self):
        '''
            Verify that all credentials were provided and compile the credential dictionary.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 11-28-2022 09:05:14
            `@memberOf`: __init__
            `@property`: credentials
        '''
        missing_keys = []
        if self.user is None:
            missing_keys.append('user')
        if self.password is None:
            missing_keys.append('password')
        if self.host is None:
            missing_keys.append('host')
        if self.database is None:
            missing_keys.append('database')
        if len(missing_keys) > 0:
            _log(f"MISSING CREDENTIALS: {missing_keys}","warning")
            self._credentials = False
            return False
        creds = {
            "user":self.user,
            "password":self.password,
            "host":self.host,
            "database":self.database,
        }
        self._credentials = True
        return creds

    def connect(self)->bool:
        '''
            Attempts to connect to the database.

            ----------

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 10:03:16
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __connect_to_my_sqldb
        '''
        connect_success = False
        if self.con is not None:
            return True
        creds = self.__credentials
        if self._credentials:
            self.con = None
            try:
                self.con = _mysqlConnector.connect(
                    database =self.database,
                    user =self.user,
                    password =self.password,
                    host =self.host,
                )

                self.cur = self.con.cursor(
                    buffered=True,
                    dictionary=True
                )

                if self.con.is_connected():
                    # print("Successfully connected to mysql database")
                    _log("Successfully connected to database.","success")
                    connect_success = True

            except Error as error:
                print(error)

        if connect_success is False:
            _log("Failed to connect to database.","warning")

        return connect_success

    @property
    def is_connected(self)->bool:
        '''
            Get the current status of the connection to the database.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 08:38:35
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: is_connected
            * @xxx [12-16-2022 08:39:06]: documentation for is_connected
        '''
        if self.con is not None:
            if self.con.is_connected() is True:
                return True
            # return True
        return False

    def close(self):
        '''
            Close the connection to the mySQL database.

            ----------

            Return {None}
            ----------------------
            None

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 19:19:32
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: close
            * @xxx [06-05-2022 19:20:10]: documentation for close
        '''

        self.con.close()
        self.con = None
        self.cur = None



    # ---------------------------------------------------------------------------- #
    #                                 SQL EXECUTION                                #
    # ---------------------------------------------------------------------------- #


    def run(self, sql:str, args:Union[list,dict]=False):
        '''
            Executes a query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {string}
                The sql query to execute.

            `args` {list,dict}
                A list of arguments to apply to the sql query

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            if multiple statements are provided it will return True if ALL statements execute successfully.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:07:54
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: run
        '''

        statements = sql
        # if the sql is a string, split it into a list of statements
        if isinstance(sql, (str)):
            statements = _to_statement_list(sql)



        if len(statements) > 1:
            # print(f"Multiple statements [{len(statements)}] found in sql.")
            success = True
            for statement in statements:
                # print(f"statement: {statement}")
                res = self.execute_single_statement(statement, args)
                if res is False:
                    success = False
            return success

        if len(statements) == 1:
            return self.execute_single_statement(sql, args)

    def run_select(self,sql:str,args=False,**kwargs):
        '''
            Execute a select query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {str}
                The Select query to execute.

            `args` {list,dict}
                The arguments to use in parameterized placeholders

            Keyword Arguments
            -------------------------
            [`default`=None] {any}
                The default value to return in the event of an error.

            [`limit`=None] {int}
                The maximum number of results to return

            [`offset`=None] {int}
                The index offset to apply to the query.

            Return {any}
            ----------------------
            The results of the query if successful, the default value otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 11:12:16
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: run_select
            * @xxx [12-09-2022 11:15:35]: documentation for run_select
        '''
        default = _obj.get_kwarg(['default'],None,None,**kwargs)
        limit = _obj.get_kwarg(['limit'],None,(int),**kwargs)
        offset = _obj.get_kwarg(['offset'],None,(int),**kwargs)

        sql = _paginate_select_query(sql,limit,offset)
        if isinstance(args,(dict)):
            sql = _format_query_params(sql,args)
        # print(f"sql:{sql}")
        if self.connect() is False:
            return default

        # _log(f"sql:{sql}","cyan")
        # _log(f"args:{args}","cyan")

        if self.run(sql,args):
            return self.fetchall()
        return default


    def execute_single_statement(self, sql:str, args=False,isTimeoutRetry=False):
        '''
            Executes a single SQL query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {string}
                The SQL to be executed.

            `args` {list}
                A list of arguments for parameter substitution.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2021 09:19:40
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: execute_single_statement
        '''
        success = False
        if self.cur is None or self.con is None:
            print("Not connected to a database, aborting query.")
            if self.data['credentials'] is not None:
                self.connect()
        try:
            if args is False:
                # print(f"executing sql: ",sql)
                self.cur.execute(sql)
            else:
                # args = _csu.sql.sanitize_quotes(args)
                args = _sanitize_args(args)
                if isinstance(args,(dict)):
                    sql = _format_query_params(sql,args)
                # print(f"args:{args}")
                self.cur.execute(sql, args)

                # print(f"result: ",result)

            self.con.commit()
            success = True


        except _mysqlConnector.errors.IntegrityError:
            _log(f"{_traceback.format_exc()}","error")
            _log(f"SQL: {sql}","error")

        except _mysqlConnector.errors.InterfaceError:
            if isTimeoutRetry is True:
                _log(f"{_traceback.format_exc()}","error")
                _log(f"SQL: {sql}","error")
            if isTimeoutRetry is False:
                # _log(f"CONNECTION TIMED OUT")
                self.cur = None
                self.con = None
                self.connect()
                return self.execute_single_statement(sql,args,True)

        except _mysqlConnector.errors.OperationalError:
            if isTimeoutRetry is True:
                _log(f"{_traceback.format_exc()}","error")
                _log(f"SQL: {sql}","error")
            if isTimeoutRetry is False:
                # _log(f"CONNECTION TIMED OUT")
                self.cur = None
                self.con = None
                self.connect()
                return self.execute_single_statement(sql,args,True)
        except _mysqlConnector.errors.DatabaseError:
            # print(f"ERROR: {err}", PRESET="FATAL_ERROR_INVERT")
            _log(f"{_traceback.format_exc()}","error")
            _log(f"SQL: {sql}","error")

        except AttributeError:
            _log(f"{_traceback.format_exc()}\n","error")
            _log(f"{print(sys.exc_info()[2])}\n\n","error")
            _log(f"SQL: \033[38;2;(235);(64);(52)m{sql}")
        return success

    def run_from_list(self, query_list,**kwargs):
        '''
            Execute SQL statements from a list.

            ----------

            Arguments
            -------------------------
            `query_list` {list}
                A list of query statements to execute.

            Keyword Arguments
            -------------------------
            [`disable_restraints`=True] {bool}
                If True, temporarily disable foreign_key_checks while executing the queries

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 16:32:58
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: run_from_list
            * @xxx [06-05-2022 16:36:56]: documentation for run_from_list
        '''

        disable_foreign_key_restraints = _obj.get_kwarg(['disable key restraints','disable restraints'],True,(bool),**kwargs)
        # disable_foreign_key_restraints = True
        # if 'DISABLE_KEY_RESTRAINTS' in kwargs:
        #     if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
        #         disable_foreign_key_restraints = False
        if disable_foreign_key_restraints is True:
            self.run("SET foreign_key_checks = 0;")

        success = True
        for idx,que in enumerate(query_list):
            print(f"{idx}/{len(query_list)}",end="\r",flush=True)
            success = self.run(que)
            if success is False:
                break

        if disable_foreign_key_restraints is True:
            self.run("SET foreign_key_checks = 1;")
        return success

    def run_multi(self, sql:str, args):
        sql = sql.replace(";", ";STATEMENT_END")
        statements = sql.split('STATEMENT_END')
        for s in statements:
            if len(s) > 0:
                # print(f"query: {s}")
                self.run(s, args)

    def fetchall(self):
        '''
            Executes the fetchall method on the database and converts the result to a dictionary.

            ----------


            Return {dict|list}
            ----------------------
            If there is more than one result, it returns a list of dicts.
            If there is only one result, it returns a single dictionary.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 13:58:55
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: fetchall
            * @xxx [06-02-2022 13:59:37]: documentation for fetchall
        '''
        return self._to_dict(self.cur.fetchall())

    def fetchone(self):
        '''
            Executes the fetchone method on the database.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 08:41:39
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: fetchone
            * @xxx [12-16-2022 08:42:00]: documentation for fetchone
        '''

        r = self.cur.fetchone()
        return r

    def execute_sql_from_file(self, filePath:str, **kwargs):
        '''
            Executes queries stored in a file.

            ----------

            Arguments
            -------------------------
            `file_path` {str}
                The filePath to the sql file

            Keyword Arguments
            -------------------------
            `DISABLE_KEY_RESTRAINTS` {bool}
                If True, temporarily disable foreign_key_checks while executing the queries

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 16:29:39
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: execute_sql_from_file
            * @xxx [06-05-2022 16:41:53]: documentation for execute_sql_from_file
        '''

        with open(filePath, 'r', encoding='utf-8') as file:
            sql = file.read()
            # print(f"filePath:{filePath}")
            statements = [str(x) for x in _csu.sql.get_statements(sql)]
            # sql = _csu.strip_sql_comments(sql)
            # _re.sub(r";")
            # sql = sql.replace(";", ";STATEMENT_END")
            # statements = sql.split('STATEMENT_END')

        # self.run("SET foreign_key_checks=0;")
        # "SOURCE /backups/mydump.sql;" -- restore your backup within THIS session
        # statements = getSQLStatementsFromFile(filePath)
        # print(f"total statements: {len(statements)}")
        disable_foreign_key_restraints = True
        if 'DISABLE_KEY_RESTRAINTS' in kwargs:
            if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
                disable_foreign_key_restraints = False
        return self.run_from_list(statements, DISABLE_KEY_RESTRAINTS=disable_foreign_key_restraints)
        # self.run("SET foreign_key_checks=1;")


    # ---------------------------------------------------------------------------- #
    #                               QUERY GENERATION                               #
    # ---------------------------------------------------------------------------- #


    def insert_query(self,table:Union[str,_db_table_type])->_db_mysql_insert_query_type:
        '''Create a new insert query instance for the table provided.'''
        if isinstance(table,(str)):
            return InsertQuery(database=self,table_name=table)
        else:
            return InsertQuery(database=self,table=table)

    def select_query(self,table:Union[str,_db_table_type])->_db_mysql_select_query_type:
        '''Create a new select query instance'''
        if isinstance(table,(str)):
            return SelectQuery(database=self,table_name=table)
        else:
            return SelectQuery(database=self,table=table)

    def update_query(self,table:Union[str,_db_table_type])->_db_mysql_update_query_type:
        '''Create a new update query instance'''
        if isinstance(table,(str)):
            return UpdateQuery(database=self,table_name=table)
        else:
            return UpdateQuery(database=self,table=table)

    def delete_query(self,table:Union[str,_db_table_type])->_db_mysql_delete_query_type:
        '''Create a new delete query instance'''
        if isinstance(table,(str)):
            return DeleteQuery(database=self,table_name=table)
        else:
            return DeleteQuery(database=self,table=table)



    # ---------------------------------------------------------------------------- #
    #                                SUPPORT QUERIES                               #
    # ---------------------------------------------------------------------------- #


    def list_schemas(self)->list:
        '''
            List all schemas in this database.

            ----------

            Return {list}
            ----------------------
            The list of schemas in this database.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 19:17:41
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: list_schemas
            * @xxx [06-05-2022 19:19:02]: documentation for list_schemas
        '''

        schemas = []
        if self.settings['setup_complete'] is False:
            return False
        # master = _cfu.read.as_json(f"{_os.getcwd()}{_os_divider}modules{_os_divider}equari{_os_divider}parse_master_sql.json")
        print(f"\n{_csu.gen.title_divider('Equari Database Schemas')}\n\n")
        total_tables = 0
        for schema in self.data['schemas']:
            print(f"    {schema['name']}")
            schemas.append(schema['name'])
            total_tables += len(schema['tables'])

        print(f"Total Schemas: {len(self.data['schemas'])}")
        print(f"Total Tables: {total_tables}")
        print(f"\n\n{_csu.gen.title_divider('Equari Database Schemas')}\n\n")
        return schemas

    def insert_to_table(self,table_name:str,data:dict,cerberus_validate:bool=False):
        '''
            Insert a dictionary of data into the table specified
            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to insert the data into.
            `data` {dict}
                A dictionary of data to insert, the keys corresponding to columns in the table.

            Return {int,bool}
            ----------------------
            The integer id of the inserted row if successful, False otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 11:44:48
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: insert_to_table
            * @xxx [12-13-2022 11:46:06]: documentation for insert_to_table
        '''
        # tb = self.get_table(table_name)
        data = self.correlate_to_table(table_name,data,crud="create",cerberus_validate=cerberus_validate)
        from colemen_utilities.sql_utils import insert_from_dict
        if len(data.keys()) == 0:
            _log("No keys in the data dict were correlated to columns in the table.","warning")
            return False
        sql,args = insert_from_dict(data,table_name,self.database)
        # print(f"sql: {sql}")
        # print(f"args: {args}")
        result = self.run(sql,args)
        if result is True:
            return self.last_id()
        _log("Failed to execute SQL.","warning")
        return False

    def last_id(self)->int:
        '''
            Retrieve the last insert id committed to the database.
            ----------

            Return {int}
            ----------------------
            The primary id of the last inserted row.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 08:43:06
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: last_id
            * @xxx [12-16-2022 08:44:37]: documentation for last_id
        '''
        sql = 'SELECT LAST_INSERT_ID();'
        result = self.run_select(sql)
        if isinstance(result,(list)):
            result = result[0]['LAST_INSERT_ID()']
        return result


    # ---------------------------------------------------------------------------- #
    #                                TABLE UTILITIES                               #
    # ---------------------------------------------------------------------------- #

    def get_table_data(self,table_name:str):
        '''
            Retrieve the Table's meta data and
            ----------

            Arguments
            -------------------------
            `arg_name` {type}
                arg_description

            Keyword Arguments
            -------------------------
            `arg_name` {type}
                arg_description

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-12-2022 09:02:38
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_table_data
            * @TODO []: documentation for get_table_data
        '''
        # if table_name in self._tables:
        #     return self._tables[table_name]
        keys = self.get_foreign_keys(table_name)
        columns = self.get_column_data(table_name)
        output = []
        # TODO []: modify this method to use the Column class
        for col in columns:
            for key in keys:
                if col['COLUMN_NAME'] == key['COLUMN_NAME']:
                    col['constraint'] = key
            output.append(col)
        # self._tables[table_name] = output
        return output

    def get_table(self,table_name:str,**kwargs)->_db_table_type:
        '''
            Retrieve a table from this database by its name.


            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to retrieve


            Keyword Arguments
            -------------------------
            `no_caching` {bool}
                If True, the table will not be loaded from its cache file, if it exists.
                This defaults to the database setting "no_caching"

            `force_regen` {bool}
                If True, the table instance is recreated.

            Return {Table}
            ----------------------
            The MySQL Table instance if the table exists, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:17:47
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_table
            * @xxx [12-13-2022 12:19:06]: documentation for get_table
        '''

        no_caching = _obj.get_kwarg(["no_caching"],self.no_caching,(bool),**kwargs)
        force_regen = _obj.get_kwarg(["force_regen"],False,(bool),**kwargs)


        # @Mstep [IF] if the table already exists in the _tables dictionary.
        if table_name in self._tables and force_regen is False:
            # @Mstep [RETURN] return table
            return self._tables[table_name]

        # @Mstep [IF] if we fail to connect to the database
        if self.connect() is False:
            # @Mstep [RETURN] return False
            return False

        output = None
        # @Mstep [] instantiate the table
        tb = Table.Table(self,table_name)

        # @Mstep [IF] if we should not use cache files.
        if no_caching is True:
            result = self._table_apply_meta_data(tb)
            success:bool = result[0]
            tb:_db_table_type = result[1]
            # @Mstep [IF] if the table meta data was successfully applied
            if success is True:
                output = tb
        else:
            # @Mstep [IF] if the table cannot be loaded from a cache file.
            if tb.cache.exists is False:
                _log("database.get_table - Failed to get table from cache.","info")
                result = self._table_apply_meta_data(tb)
                success:bool = result[0]
                tb:_db_table_type = result[1]
                # @Mstep [IF] if the table meta data was successfully applied
                if success is True:
                    # @Mstep [] have the table save its cache file.
                    tb.save_cache()
                    output = tb
                # # @Mstep [] retrieve the tables data from the database.
                # result = self.get_table_meta_data(table_name)
                # # @Mstep [IF] if the data is successfully retrieved
                # if isinstance(result,(list)):
                #     # @Mstep [LOOP] iterate the results (there should only ever be ONE)
                #     for table_data in result:
                #         # @Mstep [] have the table populate using the result data.
                #         tb.populate_from_dict(table_data)
                #         # @Mstep [] add the table to self._tables[table_name]
                #         self._tables[table_name] = tb
                #         tb.save_cache()
                #         output = tb
            # @Mstep [ELSE] if the table was loaded from the cache file.
            else:
                self._tables[table_name] = tb
                output = tb

        if output is None:
            _log(f"Could not find table: {table_name}","warning")
        return output

    def _table_apply_meta_data(self,table:_db_table_type)->tuple:
        '''
            Used by get_table to retrieve the meta data for a table and apply the results to a table instance.

            ----------

            Arguments
            -------------------------
            `table` {Table}
                The table instance to retrieve meta data for.

            Return {tuple}
            ----------------------
            (success,Table)

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 09:10:33
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: _table_apply_meta_data
            * @TODO []: documentation for _table_apply_meta_data
        '''
        result = False
        # @Mstep [] retrieve the tables data from the database.
        meta_data = self.get_table_meta_data(table.name)
        # @Mstep [IF] if the data is successfully retrieved
        if isinstance(meta_data,(list)):
            # @Mstep [LOOP] iterate the results (there should only ever be ONE)
            for table_data in meta_data:
                # @Mstep [] have the table populate using the meta_data data.
                table.populate_from_dict(table_data)
                # # @Mstep [] add the table to self._tables[table_name]
                # self._tables[table.name] = table
                result = True
        return (result,table)

    def get_table_meta_data(self,table_name:str,default=None)->dict:
        '''
            Get meta data for the table provided.
            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to retrieve column data about.

            [`default`=None] {any}
                The value to return if no data is found.

            Return {type}
            ----------------------
            If successful, this will return a dictionary of table meta data with the keys:
            - table_catalog
            - table_schema
            - table_name
            - table_type
            - engine
            - version
            - row_format
            - table_rows
            - avg_row_length
            - data_length
            - max_data_length
            - index_length
            - data_free
            - auto_increment
            - create_time
            - update_time
            - check_time
            - table_collation
            - checksum
            - create_options
            - table_comment

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 08:45:43
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_table_meta_data
            * @TODO []: documentation for get_table_meta_data
        '''
        sql = f"""select *
            from INFORMATION_SCHEMA.TABLES
            where table_type = 'BASE TABLE'
                    and table_schema = '{self.database}'
                    and table_name = '{table_name}'"""
        result = self.run_select(sql)
        output = []
        for table in result:
            if isinstance(table,(dict)):
                table = _obj.keys_to_snake_case(table)
                output.append(table)

        if len(output) == 0:
            output = default
        return output

    def get_all_tables(self)->Iterable[_db_table_type]:
        '''
            Retrieve all tables from this database.

            ----------


            Return {list}
            ----------------------
            A list of table instances.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-15-2022 13:27:01
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_all_tables
            * @xxx [12-15-2022 13:30:59]: documentation for get_all_tables
        '''
        sql = f"""select TABLE_NAME
            from INFORMATION_SCHEMA.TABLES
            where table_type = 'BASE TABLE'
                    and table_schema = '{self.database}'"""
        result = self.run_select(sql)
        output = []
        for table in result:
            print(f"\n")
            table = _obj.keys_to_snake_case(table)
            table = self.get_table(table['table_name'])
            output.append(table)
        return output



    # ---------------------------------------------------------------------------- #
    #                               COLUMN UTILITIES                               #
    # ---------------------------------------------------------------------------- #

    def get_column_data(self,table_name:str,default=None)->Iterable[_db_column_type]:
        '''
            Retrieve the column meta data for all columns in the table provided.

            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to retrieve column data about.

            [`default`=None] {any}
                The value to return if no columns are found.


            Return {list}
            ----------------------
            A list of column instances if successful, the default otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 11:18:41
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_column_data
            * @xxx [12-09-2022 11:19:52]: documentation for get_column_data
        '''
        # if table_name in self._tables:
        #     return self._tables[table_name]['columns']

        if self.connect() is False:
            return False
        # @Mstep [] get the INFORMATION_SCHEMA.COLUMNS data from the database.
        sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=$schema_name AND TABLE_NAME=$table_name"
        args = {
            "schema_name":self.database,
            "table_name":table_name,
        }
        result = self.run_select(sql, args)

        if isinstance(result,(list)) is False:
            return default

        keys = self.get_foreign_keys(table_name)


        columns = []
        for col in result:
            for key in keys:
                if col['COLUMN_NAME'] == key['COLUMN_NAME']:
                    col['constraint'] = key
            columns.append(col)


        # import colemen_utilities.database_utils.MySQL.Column.Column as _col
        output = columns
        # output = []
        # for col in columns:
            # output.append(_col.Column(col))
            # output.append(_col.Column(col))
        if len(columns) == 0:
            output = default
        return output

    def get_referential_constraint_by_name(self,name:str,table_name:str):
        if self.connect() is False:
            return False
        sql = f'''
            SELECT
                *
            FROM
                INFORMATION_SCHEMA.referential_constraints
            WHERE
                TABLE_NAME = $table_name AND
                CONSTRAINT_NAME = $name
        '''
        args = {
            "table_name":table_name,
            "name":name,
        }
        _log(f"MySQLDatabase.get_referential_constraint_by_name - {name}","magenta")
        result = self.run_select(sql,args)
        if isinstance(result,(list)) is False:
            result = []
        else:
            if len(result) > 0:
                result = result[0]
        return result

    def get_referential_constraint_by_table(self,table_name:str):
        if self.connect() is False:
            return False
        sql = f'''
            SELECT
                *
            FROM
                INFORMATION_SCHEMA.referential_constraints
            WHERE
                TABLE_NAME = $table_name;'''
        args = {
            # "schema_name":self.database,
            "table_name":table_name,
        }
        result = self.run_select(sql,args)
        if isinstance(result,(list)) is False:
            result = []

        return result

    def get_fulltext_indexes_by_table(self,table_name):
        '''Retrieve all fulltext indexes on the table provided'''
        sql = f'''
            SELECT
            `INDEX_NAME` as index_name,
            `COLUMN_NAME` as column_name,
            `NULLABLE` as nullable,
            `INDEX_COMMENT` as index_comment,
            `INDEX_TYPE` as index_type
            FROM INFORMATION_SCHEMA.STATISTICS 
            WHERE
            `INDEX_TYPE`='FULLTEXT' AND
            `table_name`=$table_name AND
            `table_schema` = $schema_name;'''
        args = {
            "schema_name":self.database,
            "table_name":table_name,
        }
        result = self.run_select(sql,args)
        if isinstance(result,(list)) is False:
            result = []
        # self._tables[table_name]
        # self._tables[table_name]['foreign_keys'] = result
        return result

    def get_foreign_keys(self,table_name:str):
        '''
            Retrieve a list of columns that are foreign keys in the table provided.
            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to query.


            Return {list}
            ----------------------
            A list of foreign key columns, the list is empty if there are None.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 11:24:42
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_foreign_keys
            * @xxx [12-09-2022 11:26:26]: documentation for get_foreign_keys
        '''
        # if table_name in self._tables:
        #     return self._tables[[table_name]]['foreign_keys']
        if self.connect() is False:
            return False
        sql = f'''
            SELECT
                TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME,REFERENCED_TABLE_SCHEMA
            FROM
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
                TABLE_NAME = $table_name AND
                TABLE_SCHEMA = $schema_name AND
                REFERENCED_TABLE_NAME IS NOT NULL;
        '''
        args = {
            "schema_name":self.database,
            "table_name":table_name,
        }
        result = self.run_select(sql,args)
        if isinstance(result,(list)) is False:
            result = []
        # self._tables[table_name]
        # self._tables[table_name]['foreign_keys'] = result
        return result



    # ---------------------------------------------------------------------------- #
    #                                 RELATIONSHIPS                                #
    # ---------------------------------------------------------------------------- #


    @property
    def get_table_relationships(self):
        '''
            Query the database to retrieve all relationships between tables in this schema specifically

            Relationships from other schemas ares filtered out.
            This will include relationships to a different schema.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:21:04
            `@memberOf`: DatabaseManager
            `@property`: summary
        '''
        if self._table_relationships is not None:
            print(f"table relationships already populated")
            return self._table_relationships
        
        if self._dbm is not None:
            result = self._dbm.get_table_relationships
        else:
            sql = '''
                SELECT
                `REFERENCED_TABLE_NAME` as 'parent_table_name',                 -- Origin key table
                `REFERENCED_TABLE_SCHEMA` as 'parent_table_schema',               -- Origin key schema
                `REFERENCED_COLUMN_NAME` as 'parent_column_name',                 -- Origin key column
                `TABLE_NAME` as 'child_table_name',                            -- Foreign key table
                `TABLE_SCHEMA` as 'child_table_schema',                          -- Foreign key schema
                `COLUMN_NAME` as 'child_column_name'
                FROM
                `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`  -- Will fail if user don't have privilege
                WHERE
                `REFERENCED_TABLE_NAME` IS NOT NULL -- Only tables with foreign keys
                ORDER BY REFERENCED_TABLE_NAME
                ;'''
            result = self._default_schema.run_select(sql)
        print(f"result: {result}")
        output = []
        for r in result:
            if r['parent_table_schema'] not in [self.name] and r['child_table_schema'] not in [self.name]:
                continue
            output.append(r)
        self._table_relationships = output
        return output


    def get_table_children(self,table:Union[str,_db_table_type])->Iterable[_db_table_type]:
        '''
            Retrieve a list of tables that have a foreign key constraint referencing the table provided.

            Essentially retrieving all tables that are children of the table provided

            ----------

            Arguments
            -------------------------
            `table` {str,Table}
                The name of the parent table or the Table instance.


            Return {list}
            ----------------------
            A list of tables associated as children to the table provided.

            If None are found, the list is empty.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 11:56:16
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: get_table_children
            * @xxx [12-16-2022 12:01:52]: documentation for get_table_children
        '''
        table_name = _table_to_name(table)
        if self._dbm is not None:
            return self._dbm.get_table_children(table_name)
        else:
            table = self.get_table(table_name)
            if table is not None:
                tables = []
                rels = self.get_table_relationships
                for rel in rels:
                    if rel['parent_table_name'] == table_name:
                        self.database.get_table(rel['child_table_schema'])
                        if table is not None:
                            tables.append(table)
                return tables


    def get_table_parents(self,table:Union[str,_db_table_type])->Iterable[_db_table_type]:
        '''
            Retrieve a list of tables that have a foreign key constraint referencing the table provided.

            Essentially retrieving all tables that are children of the table provided

            ----------

            Arguments
            -------------------------
            `table` {str,Table}
                The name of the parent table or the Table instance.


            Return {list}
            ----------------------
            A list of tables associated as children to the table provided.

            If None are found, the list is empty.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 11:56:16
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: get_table_children
            * @xxx [12-16-2022 12:01:52]: documentation for get_table_children
        '''
        table_name = _table_to_name(table)
        if self._dbm is not None:
            return self._dbm.get_table_parents(table_name)
        else:
            table = self.get_table(table_name)
            if table is not None:
                tables = []
                rels = self.get_table_relationships
                for rel in rels:
                    if rel['child_table_name'] == table_name:
                        self.database.get_table(rel['parent_table_name'])
                        if table is not None:
                            tables.append(table)
                return tables

    def get_all_relationships(self)->Iterable[_db_relationship_type]:
        table:_db_table_type
        for _,table in self._tables.items():
            for col in table.columns:
                if col.data.is_foreign_key:
                    # _log("Column.relationship --- Relationship Found","magenta")
                    value = Relationship.Relationship(
                        self,
                        col.table,
                        col,
                        col.data.foreign_key_data
                    )
                    self._relationship = value
                    if self.no_caching is False:
                        col.table.save_cache()



    # def get_from_table(self,table_name:str,data:dict,**kwargs):
    #     limit = _obj.get_kwarg(['limit'],self.get_limit,(int),**kwargs)
    #     offset = _obj.get_kwarg(['offset'],None,(int),**kwargs)
    #     select = _obj.get_kwarg(['select'],None,(list,dict),**kwargs)
    #     data = self.correlate_to_table(table_name,data,crud="read",cerberus_validate=True)
    #     from colemen_utilities.sql_utils import select_from_dict
    #     if len(data.keys()) == 0:
    #         return False

    #     sql,args = select_from_dict(
    #         data,
    #         table_name,
    #         schema_name=self.database,
    #         select = select,
    #     )

    #     sql = _paginate_select_query(sql,limit,offset)
    #     sql = _format_query_params(sql,data)

    #     # TODO []: COMMENTED FOR TESTING
    #     # result = self.run_select(sql,args)
    #     # TODO []: COMMENTED FOR TESTING
    #     print(f"result:{(sql,args)}")

    def _to_dict(self, result):
        # print(f"_to_dict: resultType: {type(result)}")
        if isinstance(result, list):
            new_data = []
            for row in result:
                tmp = {}
                for col in row.keys():
                    tmp[col] = row[col]
                new_data.append(tmp)
            return new_data
        # if isinstance(result, sqlite3.Row):
        #     new_data = {}
        #     for col in result.keys():
        #         new_data[col] = result[col]
        #     return new_data

    # def get_column_data(self,table_name:str,default=None)->Iterable[_db_column_type]:
    #     '''
    #         Retrieve the column meta data for all columns in the table provided.

    #         ----------

    #         Arguments
    #         -------------------------
    #         `table_name` {str}
    #             The name of the table to retrieve column data about.

    #         [`default`=None] {any}
    #             The value to return if no columns are found.


    #         Return {list}
    #         ----------------------
    #         A list of column instances if successful, the default otherwise.

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 12-09-2022 11:18:41
    #         `memberOf`: MySQLDatabase
    #         `version`: 1.0
    #         `method_name`: get_column_data
    #         * @xxx [12-09-2022 11:19:52]: documentation for get_column_data
    #     '''
    #     # if table_name in self._tables:
    #     #     return self._tables[table_name]['columns']

    #     if self.connect() is False:
    #         return False
    #     # @Mstep [] get the INFORMATION_SCHEMA.COLUMNS data from the database.
    #     sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=$schema_name AND TABLE_NAME=$table_name"
    #     args = {
    #         "schema_name":self.database,
    #         "table_name":table_name,
    #     }
    #     result = self.run_select(sql, args)
    #     # _cfu.writer.to_json("tmp.json",result)
    #     if isinstance(result,(list)) is False:
    #         result = []
    #     import colemen_utilities.database_utils.MySQL.Column.Column as _col
    #     output = []
    #     for col in result:
    #         output.append(_col.Column(col))
    #     if len(output) == 0:
    #         output = default
    #     return output

    def get_cerberus_schema(self,table_name,crud_type=None,to_json=False):
        tb = self.get_table(table_name)
        result = []
        if tb is not None:
            result = tb.columns
        # result = self.get_column_data(table_name)

        # col:colemen_config._db_column_type = result[0]


        cerb = {}
        for x in result:
            valid = x.validation.cerberus_schema(crud_type)
            if valid is not None:
                data = {}
                for k,v in valid.items():
                    if to_json is True:
                        if k in ["check_with",'coerce']:
                            v = v.__name__
                    data[k] = v
                cerb[x.name] = data
        if to_json is True:
            return json.dumps(cerb,indent=4)
        return cerb


    # def get_table_meta_data(self):


    #     sql = f"""select *
    #         from INFORMATION_SCHEMA.TABLES
    #         where table_type = 'BASE TABLE'
    #                 and table_schema = '{self.database}'"""
    #     result = self.run_select(sql)
    #     output = []
    #     for table in result:
    #         if isinstance(table,(dict)):
    #             table = _obj.keys_to_snake_case(table)
    #             tb = Table.Table(self,table['table_name'],table)
    #             cols:Iterable[_db_column_type] = self.get_column_data(table['table_name'])
    #             for col in cols:
    #                 tb.add_column(col)
    #         # if isinstance(table,(dict)):
    #             # table['create_time'] = table['create_time'].timestamp()
    #             output.append(table)
    #     return output

    # def validate_to_table(self,table_name:str,data:dict):
    #     cerberus_validate = _obj.get_kwarg(['cerberus_validate'],False,(bool),**kwargs)
    #     crud_type = _obj.get_kwarg(['crud','crud_type'],None,(str),**kwargs)
    #     default_on_fail = _obj.get_kwarg(['default_on_failure'],False,(bool),**kwargs)

    def __assign_default_meta_cols(self,tb:_db_table_type,crud_type):
        output = {}
        if crud_type in ['create']:
            if tb.has_timestamp_column:
                output['timestamp'] = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

            if tb.has_modified_timestamp_column:
                output['modified_timestamp'] = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

            if tb.has_hash_id:
                output['hash_id'] = tb.gen_hash_id()

        if crud_type in ['update']:
            if tb.has_modified_timestamp_column:
                output['modified_timestamp'] = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

        if crud_type in ['delete']:
            if tb.has_modified_timestamp_column:
                output['modified_timestamp'] = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

            if tb.has_deleted_column:
                output['deleted'] = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())


        return output


    # ---------------------------------------------------------------------------- #
    #                                DATA VALIDATION                               #
    # ---------------------------------------------------------------------------- #


    def correlate_to_table(self,table_name:str,data:dict,**kwargs):
        '''
            Correlate a dictionary of data to the columns of the table.

            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to compare the dictionary to.

            `data` {dict}
                The dictionary to compare.

            Keyword Arguments
            -------------------------
            `arg_name` {type}
                arg_description

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 14:02:34
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: correlate_to_table
            * @TODO []: documentation for correlate_to_table
        '''
        # cerberus_validate = _obj.get_kwarg(['cerberus_validate'],False,(bool),**kwargs)
        crud_type = _obj.get_kwarg(['crud','crud_type'],None,(str),**kwargs)
        default_on_fail = _obj.get_kwarg(['default_on_failure'],False,(bool),**kwargs)
        validate_types = _obj.get_kwarg(['validate_types'],True,(bool),**kwargs)
        if isinstance(table_name,(str)):
            tb = self.get_table(table_name)
        else:
            tb = table_name

        cols = tb.columns
        # cols = self.get_column_data(table_name)
        col:_db_column_type

        output = self.__assign_default_meta_cols(tb,crud_type)
        
        for col in cols:
            name = col.data.column_name
            if name in data:
                value = data[name]
                result = self.correlate_single_column(
                    col,
                    value,
                    default_on_fail=default_on_fail
                    )
                if isinstance(result,(dict)):
                    for key,value in result.items():
                        output[key] = value
                    continue
        # _log(f"\nMySQLDatabase.correlate_to_table: {output}","magenta")
        return output

    def correlate_single_column(self,column:_db_column_type,value,**kwargs):
        output = {}



        default_on_fail = _obj.get_kwarg(["default_on_fail"],False,(bool),**kwargs)
        name = column.data.column_name
        value_type = type(value).__name__


        # @Mstep [IF] if the value_type matches the column's supported data type (or its python equivalent)
        if value_type in column.data.py_data_type:
            # @Mstep [] add the key value to the output
            output[name] = value
        # @Mstep [ELSE] if the value_type does not match the column's supported data type
        else:

            # @Mstep [IF] if the column contains a boolean value and the value is an int or string.
            if column.validation.is_boolean is True and value_type in ['string','int']:
                # @Mstep [] convert the value to a boolean.
                from colemen_utilities.type_utils import to_bool
                # @Mstep [] add the key value to the output
                output[name] = to_bool(to_bool)
                return output

            # @Mstep [IF] if the value is None and the column is nullable
            if value is None and column.data.is_nullable is True:
                # @Mstep [] add the key value to the output
                output[name] = value
                return output
            
            # @Mstep [IF] if the value is an int or float and the column only supports strings
            if column.data.py_data_type in ['integer'] and isinstance(value,datetime.datetime):
                output[name] = int(value.timestamp())
                return output
            if column.data.py_data_type in ['string'] and isinstance(value,(int,float)):
                # @Mstep [] convert the value to a string
                # @Mstep [] add the key value to the output
                output[name] = str(value)
                return output


            # else:
            if default_on_fail is True:
                output[name] = column.data.default
            else:
                _log(f"Value for {name} expected: {column.validation.py_data_type} --- found: {value_type}","warning")
                output = False
        return output



    # ---------------------------------------------------------------------------- #
    #                                    SUPPORT                                   #
    # ---------------------------------------------------------------------------- #

    def register(self,entity):
        '''
            Used INTERNALLY to register table, column & relationship entities with this database.

            ----------

            Arguments
            -------------------------
            `entity` {any}
                The entity to register with this database.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 10:01:12
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: register
            * @TODO []: documentation for register
        '''

        if isinstance(entity,Table.Table):
            table:_db_table_type = entity
            self._tables[table.name] = table

        if isinstance(entity,Relationship.Relationship):
            rel:_db_relationship_type = entity
            self._relationships.append(rel)

        if isinstance(entity,Column):
            col:_db_column_type = entity
            self._columns.append(col)

        # @Mstep [IF] if there is a manager associated to this database
        if self._dbm is not None:
            # @Mstep [] register there entity with the manager as well.
            self._dbm.register(entity)






def _to_statement_list(sql):
    sql = sql.replace(";", ";STATEMENT_END")
    statements = sql.split('STATEMENT_END')
    output = [x.strip() for x in statements if len(x.strip()) > 0]
    return output

def _format_query_params(sql:str,args:dict)->str:
    '''
        Format an SQL query's parameters to use the python named template format.

        This will only replace matches that have a corresponding key in the args dictionary.

        Parameters can begin with a dollar sign or colon.


        SELECT * from blackholes WHERE hash_id=$hash_id

        SELECT * from blackholes WHERE hash_id=%(hash_id)s

        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql string to format.

        `args` {dict}
            The dictionary of parameter values.


        Return {str}
        ----------------------
        The sql statement with parameters replaced.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2022 10:39:24
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: _format_query_params
        * @xxx [12-09-2022 10:43:23]: documentation for _format_query_params
    '''
    if isinstance(args,(dict)) is False:
        return sql
    # args = sorted(args.items(), key=lambda x: x[1], reverse=True)
    arg_keys = list(args.keys())
    arg_keys.sort(key=len, reverse=True)
    for k in arg_keys:
    # for k,v in args.items():
        sql = re.sub(fr'[$:]{k}',f"%({k})s",sql)

    # matches = re.findall(r'[$:]([a-z_0-9]*)',sql,re.IGNORECASE)
    # if isinstance(matches,(list)):
    #     for match in matches:
    #         if match in args:
    #             sql = sql.replace(f"${match}",f"%({match})s")

    return sql


def _paginate_select_query(sql:str,limit:int=None,offset:int=None)->str:
    '''
        Apply a limit and offset value to a select query statement.
        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql statement to modify

        [`limit`=None] {int}
            The limit to apply to the results.

        [`offset`=None] {int}
            The offset to apply to the results.


        Return {str}
        ----------------------
        The sql statement with a limit and offset value applied.

        If the limit/offset if invalid no pagination is added.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2022 11:09:53
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: _paginate_select_query
        * @xxx [12-09-2022 11:11:52]: documentation for _paginate_select_query
    '''
    if limit is None and offset is None:
        return sql
    if isinstance(limit,(str)):
        limit = re.sub(r'[^0-9]',"",limit)
        if len(limit) == 0:
            return sql
        limit = int(limit)

    if isinstance(offset,(str)):
        offset = re.sub(r'[^0-9]',"",offset)
        if len(offset) == 0:
            offset = None
        else:
            offset = int(offset)

    if limit == 0:
        limit = 1

    if offset is not None:
        if offset < 1:
            offset = None

    sql = _csu.strip(sql,[";"],"right")
    sql = re.sub(r'limit\s*[0-9]*\s*(,|offset)\s*(:?[0-9\s]*)?',"",sql,re.MULTILINE | re.IGNORECASE)

    limit_string = f"LIMIT {limit}"
    offset_string = ""
    if offset is not None:
        offset_string = f"OFFSET {offset}"
    paginate = f"{limit_string} {offset_string}"
    sql = f"{sql} {paginate}"
    return sql

def _sanitize_args(args):
    if isinstance(args,(dict)):
        output = {}
        for k,v in args.items():
            output[k] = _csu.sanitize_quotes(v)
        return output
    if isinstance(args,(list)):
        output = []
        for v in args:
            output.append(_csu.sanitize_quotes(v))
        return output


def new(**kwargs)->MySQLDatabase:
    '''
        Create a new MySQL database connection.

        ----------


        Keyword Arguments
        -------------------------

        `database` {str}
            The name of the database/schema this instance represents.

        `user` {str}
            The user name used to connect to the database.

        `password` {str}
            The password used to connect to the database.

        `host` {str}
            The host address used to connect to the database

        [`cache_path`=None] {str}
            The path to the directory where the table cache files can be saved.

        [`database_manager`=None] {DatabaseManager}
            A reference to the database manager

        Return {MySQLDatabase}
        ----------------------
        The MySQLDatabase instance.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-13-2022 12:27:05
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: new
        * @xxx [12-13-2022 12:29:29]: documentation for new
    '''
    return MySQLDatabase(**kwargs)








def _table_to_name(table:Union[str,_db_table_type]):
    '''returns a table name if the table instance is provided.'''
    from colemen_utilities.database_utils.MySQL.Table import Table
    if isinstance(table,Table.Table):
        table = table.name
    return table


