
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import


'''
    Module containing the DatabaseManager class declaration.

    This is used to connect to a remote MySQL database and allows slightly abstracted
    methods for manipulating it.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-13-2022 12:42:25
    `memberOf`: MySQL
    # TODO []: purge table cache files that are not associated to an existing table.
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
from colemen_config import _db_column_type,_db_table_type,_db_mysql_database_type,_db_relationship_type

# import colemen_utilities.file_utils as _cfu
# import colemen_utilities.directory_utils as _dirs
import colemen_utilities.list_utils as _lu
import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj


import colemen_utilities.database_utils.MySQL.MySQLDatabase as _mySQLDatabase
from colemen_utilities.database_utils.MySQL.Relationship import Relationship as _relationship
from colemen_utilities.database_utils.MySQL.Table import Table as _table


import colemen_utilities.console_utils as _con
_log = _con.log


@dataclass
class DatabaseManager:

    database:str = None
    '''The name of the database/schema this instance represents.'''

    user:str = None
    '''The user name used to connect to the database.'''

    password:str = None
    '''The password used to connect to the database.'''

    host:str = None
    '''The host address used to connect to the database'''

    _tables = None
    '''A dictionary of table instances the keys correspond to the table's name for quick lookups.'''


    no_caching:bool = False
    '''If True, no cache files will be created, this really slows shit down..'''

    cache_path:str = f"{os.getcwd()}/cache"
    '''File path to the directory where table cache files are stored.

    Defaults to: {cwd}/cache
    '''

    get_limit:int = 100
    '''The default LIMIT applied to select queries'''

    _relationships = None
    '''A list of relationship instances'''

    _table_relationships = None
    '''A list of all table relationships retrieved from the database'''

    _default_schema:_db_mysql_database_type = None

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
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: DatabaseManager
            * @xxx [12-13-2022 12:31:27]: documentation for DatabaseManager
        '''

        self._schemas = {}


        # initialize these attributes for later use.
        self._tables = {}
        self._relationships = []
        self._columns = []


    @property
    def summary(self):
        '''
            Get the summary dictionary for all databases associated to this .

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:21:04
            `@memberOf`: DatabaseManager
            `@property`: summary
        '''
        value = {
            "schemas":{},
        }
        for name,s in self._schemas.items():
            value['schemas'][name] = s.summary
        return value

    def master_index(self):
        '''
            All schemas will retrieve their associated tables, columns and relationships.

            This typically only needs to be called after all schemas are added.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 10:34:20
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: master_index
            * @xxx [01-12-2023 09:20:26]: documentation for master_index
        '''
        # @Mstep [LOOP] iterate all schemas
        schema:_db_mysql_database_type
        for name,schema in self._schemas.items():
            print(f"\n")
            _log(f"Indexing all tables in schema {name} {' '*150}","info invert")
            # @Mstep [] get all tables from the schema
            schema.get_all_tables()
        for name,schema in self._schemas.items():
            schema.get_all_relationships()

    def register(self,entity):
        '''
            Used INTERNALLY to register database entities with this manager.

            ----------

            Arguments
            -------------------------
            `entity` {any}
                The entity to register with this manager.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 10:01:12
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: register
            * @xxx [12-16-2022 10:43:14]: documentation for register
        '''
        from colemen_utilities.database_utils.MySQL.Table import Table
        from colemen_utilities.database_utils.MySQL.Relationship import Relationship
        from colemen_utilities.database_utils.MySQL.Column import Column

        if isinstance(entity,_mySQLDatabase.MySQLDatabase):
            db:_db_mysql_database_type = entity
            self._schemas[db.name] = db

        if isinstance(entity,Table.Table):
            table:_db_table_type = entity
            self._tables[table.name] = table

        if isinstance(entity,Relationship.Relationship):
            rel:_db_relationship_type = entity
            self._relationships.append(rel)

        if isinstance(entity,Column):
            col:_db_column_type = entity
            self._columns.append(col)



    # ---------------------------------------------------------------------------- #
    #                               SCHEMA UTILITIES                               #
    # ---------------------------------------------------------------------------- #


    def add_schema(self,**credentials):
        if 'name' in credentials:
            credentials['database'] = credentials['name']
        credentials['database_manager'] = self
        schema = _mySQLDatabase.new(**credentials)
        schema.no_caching = self.no_caching
        schema.cache_path = self.cache_path
        if self._default_schema is None:
            self._default_schema = schema
        self._schemas[credentials['database']] = schema


    def get_schema(self,schema_name:str)->_db_mysql_database_type:
        '''Retrieve a schema[database] instance by its name'''
        if schema_name in self._schemas:
            return self._schemas[schema_name]
        return None



    # ---------------------------------------------------------------------------- #
    #                                TABLE UTILITIES                               #
    # ---------------------------------------------------------------------------- #

    def get_table(self,table_name:str,schema_name:str=None)->_db_table_type:
        '''
            Get a table instance from the databases
            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to search for

            [`schema_name`=None] {str}
                The name of the schema the table must belong to.

            Return {_db_table_type,None}
            ----------------------
            The table instance, if it can be found, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 10:43:22
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: get_table
            * @xxx [12-16-2022 10:44:51]: documentation for get_table
        '''
        if table_name in self._tables:
            return self._tables[table_name]

        if schema_name is not None:
            schema = self.get_schema(schema_name)
            from colemen_utilities.database_utils.MySQL.Table import Table
            if isinstance(schema,_mySQLDatabase.MySQLDatabase):
                return schema.get_table(table_name)

        _log(f"Failed to locate table {table_name}, have all the schemas been indexed? call master_index","warning")

    @property
    def tables(self)->Iterable[_db_table_type]:
        '''
            Get all tables being managed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 15:36:52
            `@memberOf`: DatabaseManager
            `@property`: tables
        '''
        value = self._tables.values()
        return value

    @property
    def table_names(self)->Iterable[str]:
        '''
            Get a list of all table names associated to this manager.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 10:54:20
            `@memberOf`: DatabaseManager
            `@property`: table_names
        '''

        return list(self._tables.keys())

    @property
    def longest_table_name(self):
        '''
            find the table with the longest name.

            returns a tuple containing the length and name.

            (13,'someTableName')

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-20-2022 10:19:37
            `@memberOf`: DatabaseManager
            `@property`: longest_table_name
        '''
        value = _lu.longest_string(self.table_names)
        return value


    # ---------------------------------------------------------------------------- #
    #                                 RELATIONSHIPS                                #
    # ---------------------------------------------------------------------------- #

    @property
    def relationships(self)->Iterable[_db_relationship_type]:
        '''
            Get this DatabaseManager's relationships

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 11:01:56
            `@memberOf`: DatabaseManager
            `@property`: relationships
        '''
        if self._relationships is not None:
            return self._relationships
        relationships = []
        if self._relationships is None:
            rels = self.get_table_relationships
            for rel in rels:
                child_table = self.get_table(rel['child_table_name'],rel['child_table_schema'])
                parent_table = self.get_table(rel['parent_table_name'],rel['parent_table_schema'])
                from colemen_utilities.database_utils.MySQL.Table import Table
                from colemen_utilities.database_utils.MySQL.Column import Column
                # child_schema = self.get_schema(rel['child_table_schema'])
                if isinstance(child_table,Table) and isinstance(parent_table,Table):
                    parent_column = parent_table.get_column_by_name(rel['parent_column_name'])
                    child_column = child_table.get_column_by_name(rel['child_column_name'])
                    if isinstance(child_column,Column):
                        relationship = _relationship.Relationship(
                            child_table.database,
                            child_table,
                            child_column,
                            {
                                "foreign_key_constraint_name":rel['constraint_name']
                            }
                        )
                        relationship.foreign_schema = parent_table.database
                        relationship.foreign_table = parent_table
                        relationship.foreign_column = parent_column
                        relationships.append(relationship)


        if isinstance(relationships,(list)):
            if len(relationships) == 0:
                relationships = None

        self._relationships = relationships
        return self._relationships

    @property
    def get_table_relationships(self)->Iterable[dict]:
        '''
            Query the database to retrieve all relationships between tables.

            Relationships from Schemas that are not being managed by this instance are removed from the results.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:21:04
            `@memberOf`: DatabaseManager
            `@property`: summary
        '''
        if self._table_relationships is not None:
            return self._table_relationships

        sql = '''
            SELECT
            `REFERENCED_TABLE_NAME` as 'parent_table_name',                 -- Origin key table
            `REFERENCED_TABLE_SCHEMA` as 'parent_table_schema',               -- Origin key schema
            `REFERENCED_COLUMN_NAME` as 'parent_column_name',                 -- Origin key column
            `TABLE_NAME` as 'child_table_name',                            -- Foreign key table
            `TABLE_SCHEMA` as 'child_table_schema',                          -- Foreign key schema
            `COLUMN_NAME` as 'child_column_name',
            `CONSTRAINT_NAME` as 'constraint_name'                        -- Foreign key column
            FROM
            `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`  -- Will fail if user don't have privilege
            WHERE
            `REFERENCED_TABLE_NAME` IS NOT NULL -- Only tables with foreign keys
            ORDER BY REFERENCED_TABLE_NAME
            ;'''
        result = self._default_schema.run_select(sql)
        schema_names = self._schemas.keys()
        output = []
        for r in result:
            if r['parent_table_schema'] not in schema_names or r['child_table_schema']not in schema_names:
                continue
            output.append(r)
        return output

    def get_table_children(self,table:Union[str,_db_table_type])->Iterable[_db_table_type]:
        '''
            Retrieve a list of tables that have a foreign key constraint referencing the table provided.

            Essentially retrieving all tables that are children of the table provided

            Unlike the MySQLDatabase method, this can retrieve tables across schemas.

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
        parent_table = _table_to_name(table)
        tables = []
        rels = self.get_table_relationships
        for rel in rels:
            if rel['parent_table_name'] == parent_table:
                schema = self.get_schema(rel['child_table_schema'])
                if schema is not None:
                    table = schema.get_table(rel['child_table_name'])
                    if table is not None:
                        tables.append(table)
        return tables

    def get_table_parents(self,table:Union[str,_db_table_type])->Iterable[_db_table_type]:
        '''
            Retrieve a list of tables that the table provided is a child of.

            This means that it has a foreign key constraint referencing the tables returned.

            ----------

            Arguments
            -------------------------
            `table_name` {str,Table}
                The name of the parent table or the Table instance.


            Return {list}
            ----------------------
            A list of tables associated as parents to the table provided.

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
        tables = []
        rels = self.get_table_relationships
        for rel in rels:
            if rel['child_table_name'] == table_name:
                schema = self.get_schema(rel['parent_table_schema'])
                if schema is not None:
                    table = schema.get_table(rel['parent_table_name'])
                    if table is not None:
                        tables.append(table)
        return tables

    def get_table_relationships_by_child_count(self):
        # if self._table_relationships is not None:
        #     return self._table_relationships

        sql = '''
            SELECT 
                count(1) total_relationships ,
            `REFERENCED_TABLE_NAME` as 'parent_table_name',                 -- Origin key table
            `REFERENCED_TABLE_SCHEMA` as 'parent_table_schema',               -- Origin key schema
            `REFERENCED_COLUMN_NAME` as 'parent_column_name',                 -- Origin key column
            `TABLE_NAME` as 'child_table_name',                            -- Foreign key table
            `TABLE_SCHEMA` as 'child_table_schema',                          -- Foreign key schema
            `COLUMN_NAME` as 'child_column_name'                        -- Foreign key column
            FROM
            `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`  -- Will fail if user don't have privilege
            WHERE
            `REFERENCED_TABLE_NAME` IS NOT NULL -- Only tables with foreign keys
            GROUP BY REFERENCED_TABLE_NAME
            ORDER BY total_relationships desc
            ;'''
        result = self._default_schema.run_select(sql)

        return result



    @property
    def api_endpoints(self):
        ordered_relationships = self.get_table_relationships_by_child_count()
        end_points = self._gen_api_endpoints("api/1/",None,ordered_relationships,0)
        return end_points

    def _gen_api_endpoints(self,prefix:str=None,parent_url:str=None,ordered_relationships=None,depth=0,depth_limit=20):
        end_points = []
        depth += 1
        if depth > depth_limit:
            return end_points

        crud_types = ['create','read','read_single','update','delete']
        # if ordered_relationships is None:
        #     ordered_relationships = self.get_table_relationships_by_child_count()

        data = {
            "crud":None,
            "url":None
        }
        for relData in ordered_relationships:
            parent_table = relData
            if isinstance(relData,(dict)):
                parent_table = self.get_table(relData['parent_table_name'])
            if isinstance(parent_table,_table.Table) is False:
                continue
            parent_url = parent_table.api_url_base
            
            if prefix is not None:
                prefix = f"{prefix}"
            url = f"{prefix}{parent_url}"
            end_points.append(url)

            children = self.get_table_children(parent_table)
            for child in children:
                # children = self.get_table_children(parent_table)
                # url = f"{prefix}/{child.api_endpoint_url()}"
                # end_points.append(url)
                # grandChildren = self.get_table_children(child)
                eps = self._gen_api_endpoints(prefix,url,self.get_table_children(child),depth,depth_limit)
                end_points = end_points + eps

                print(f"url: {url}")
        return end_points



    # def get_table_parents(self,table:Union[str,_db_table_type])->Iterable[_db_table_type]:
    #     '''
    #         Retrieve a list of tables that the table provided is a child of.

    #         This means that it has a foreign key constraint referencing the tables returned.

    #         ----------

    #         Arguments
    #         -------------------------
    #         `table` {str,Table}
    #             The name of the parent table or the Table instance.


    #         Return {list}
    #         ----------------------
    #         A list of tables associated as parents to the table provided.

    #         If None are found, the list is empty.

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 12-16-2022 11:56:16
    #         `memberOf`: DatabaseManager
    #         `version`: 1.0
    #         `method_name`: get_table_children
    #         * @xxx [12-16-2022 12:01:52]: documentation for get_table_children
    #     '''
    #     table_name = _table_to_name(table)
    #     tables = []
    #     rel:_db_relationship_type
    #     for rel in self._relationships:
    #         if rel.is_child(table_name):
    #             if rel.parent_table_found:
    #                 tables.append(rel.parent_table)
    #     return tables



def _table_to_name(table:Union[str,_db_table_type]):
    '''returns a table name if the table instance is provided.'''
    from colemen_utilities.database_utils.MySQL.Table import Table
    if isinstance(table,Table.Table):
        table = table.name
    return table


def new(**kwargs)->DatabaseManager:
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

        Return {DatabaseManager}
        ----------------------
        The DatabaseManager instance.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-13-2022 12:27:05
        `memberOf`: DatabaseManager
        `version`: 1.0
        `method_name`: new
        * @xxx [12-13-2022 12:29:29]: documentation for new
    '''
    return DatabaseManager(**kwargs)










