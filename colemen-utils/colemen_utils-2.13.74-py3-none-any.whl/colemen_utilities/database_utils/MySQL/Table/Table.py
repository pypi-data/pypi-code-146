
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import json
# import importlib
from dataclasses import dataclass
from posixpath import split
# from typing import List
from typing import Iterable, Union



from colemen_config import _db_column_type,_db_mysql_database_type,_db_table_type,_db_relationship_type
# import colemen_utilities.database_utils.MySQL.Column.Column as _Column
from colemen_utilities.database_utils.MySQL.Column.Column import Column as _Column
# from colemen_utilities.database_utils.MySQL.Column import column_utils as _u
from colemen_utilities.database_utils.MySQL.Column.column_utils import parse_comment_yaml
from colemen_utilities.database_utils.MySQL import CacheFile as _CacheFile
import colemen_utilities.database_utils.MySQL.Relationship.Relationship as _rel
import colemen_utilities.list_utils as _lu


import colemen_utilities.dict_utils as _obj
import colemen_utilities.random_utils as _rand
import colemen_utilities.string_utils as _csu
import colemen_utilities.console_utils as _con
_log = _con.log




@dataclass
class Table:
    database:_db_mysql_database_type = None
    _cache = None

    schema:str = None
    _name:str = None
    _has_deleted_column:bool = None
    _has_timestamp_column:bool = None
    _has_modified_timestamp_column:bool = None
    _has_hash_id:bool = None
    _hash_id_prefix:str = None
    _hash_id_column:_db_column_type = None
    table_catalog = None
    table_schema = None
    table_name = None
    table_type = None
    engine = None
    version = None
    row_format = None
    table_rows = None
    avg_row_length = None
    data_length = None
    max_data_length = None
    index_length = None
    data_free = None
    auto_increment = None
    
    # ----------------------------------- ROLES ---------------------------------- #
    create_roles = None
    '''The roles allowed to insert to this table'''
    read_roles = None
    '''The roles allowed to read from this table'''
    update_roles = None
    '''The roles allowed to update this table'''
    delete_roles = None
    '''The roles allowed to delete rows in this table'''
    
    
    # create_time = None
    # update_time = None
    # check_time = None
    subject_type:str = None
    '''The type of subject this table represents [entity,relationship]'''
    table_collation = None
    checksum = None
    create_options = None
    table_comment = None
    name_ = None
    _cerberus_validations = None

    # TODO []: get all form names
    # TODO []: get columns by form name

    _hash_id = None
    _primary_id = None
    '''The column instance of this table's primary id.'''
    _Columns = []
    '''A list of column instances associated to this table.'''
    _relationships = None
    '''A dictionary of relationship instances that are associated to this table.'''


    _column_names = None
    '''Contains a list of all column names in this table.'''
    _longest_column_name = None
    '''Contains the longest column name tuple'''

    raw_fulltext_indexes= None
    '''Contains a list of dictionaries, each representing a column that has a fulltext index in this table.'''
    raw_referential_constraints= None
    '''Contains a list of dictionaries, each representing a column that has a referential constraint in this table.'''

    def __init__(self,database:_db_mysql_database_type,table_name:str,data:dict = None) -> None:
        '''
            Create a table instance.

            ----------

            Arguments
            -------------------------
            `database` {MySQLDatabase}
                A reference to the Database that this table belongs to.

            `table_name` {str}
                The name of this table.

            `data` {dict}
                A dictionary of table data.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:38:23
            `memberOf`: Table
            `version`: 1.0
            `method_name`: Table
            * @TODO []: documentation for Table
        '''
        self.database:_db_mysql_database_type = database
        self.table_name = table_name
        self._columns = []
        self._relationships = []
        self._has_deleted_column = None
        self._has_timestamp_column = None
        self._has_modified_timestamp_column = None
        self._has_hash_id = None
        self._hash_id_prefix = None
        self._hash_id_column = None
        self.name_ = _csu.Name(table_name)

        if data is None and self.database.no_caching is False:
            data = self.cache.load()
        # if data is None:
        #     data = self.database.get_table_meta_data(self.naem)
        if data is not None:
            populate_from_dict(data,self)

        self.raw_fulltext_indexes = self.database.get_fulltext_indexes_by_table(self.name)
        # if self.raw_referential_constraints is None:
        #     self.raw_referential_constraints = _lu.force_list(self.database.get_referential_constraint_by_table(self.name))
        
        # @Mstep [] register this table with the database.
        self.database.register(self)


    # ---------------------------------------------------------------------------- #
    #                                CACHE UTILITIES                               #
    # ---------------------------------------------------------------------------- #


    @property
    def cache(self):
        '''
            Get this Table's cache

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:51:44
            `@memberOf`: Table
            `@property`: cache
        '''

        value = self._cache
        if value is None:
            # print(f"table.cache - instantiating cache class")
            value = _CacheFile(self.database,self.database.database,self.table_name)
            value.name = f"{self.database.database}_{self.table_name}"
            self._cache = value
        return value

    def save_cache(self):
        '''Save this table's cache file'''
        # @Mstep [IF] if the no_caching setting is True >>> [] skip saving the cache.
        if self.database.no_caching is True:
            return
        # @Mstep [] generate this table's summary, this causes the table to compile its data for saving.
        self.summary
        # @Mstep [] save the cache file.
        # self.cache.save()




    @property
    def summary(self):
        '''
            Get the summary property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-06-2022 12:10:00
            `@memberOf`: __init__
            `@property`: summary
        '''
        # print(f"table.summary - generating summary")
        value = {
            "schema":self.database.database,
            "name":self.table_name,
            "has_deleted_column":self.has_deleted_column,
            "has_timestamp_column":self.has_timestamp_column,
            "has_modified_timestamp_column":self.has_modified_timestamp_column,
            "has_hash_id":self.has_hash_id,
            "hash_id_prefix":self.hash_id_prefix,
            "table_catalog":self.table_catalog,
            "table_schema":self.table_schema,
            "table_name":self.table_name,
            "table_type":self.table_type,
            "engine":self.engine,
            "version":self.version,
            "row_format":self.row_format,
            "table_rows":self.table_rows,
            "avg_row_length":self.avg_row_length,
            "data_length":self.data_length,
            "max_data_length":self.max_data_length,
            "index_length":self.index_length,
            "data_free":self.data_free,
            "auto_increment":self.auto_increment,
            "table_collation":self.table_collation,
            "checksum":self.checksum,
            "table_comment":self.table_comment,
            "raw_fulltext_indexes":self.raw_fulltext_indexes,
            "raw_referential_constraints":self.raw_referential_constraints,
            "create_roles":self.create_roles,
            "read_roles":self.read_roles,
            "update_roles":self.update_roles,
            "delete_roles":self.delete_roles,
            "subject_type":self.subject_type,
            # "create_options":self.create_options,
            # "create_roles":self.create_roles,
            # "read_roles":self.read_roles,
            # "update_roles":self.update_roles,
            # "delete_roles":self.delete_roles,
            # "blueprint_name":self.blueprint_name,
        }

        # value['relationships'] = [x.summary for x in self.relationships]
        self._cache.set_key("table_data",value)
        value['columns'] = [x.summary for x in self.columns]
        value['relationships'] = [x.summary for x in self._relationships]
        value['total_columns'] = len(self.columns)
        value['total_relationships'] = len(self._relationships)
        # value['total_raw_referential_constraints'] = len(self.raw_referential_constraints)
        # value['total_raw_fulltext_indexes'] = len(self.raw_fulltext_indexes)

        # self._cache.set_key("columns",value['columns'])
        # value['end_points'] = [x.summary for x in self._end_point_docs]
        self._cache.save()
        return value

    @property
    def meta_data(self)->dict:
        '''
            Get this Table's meta_data as a dictionary.
            
            This is the same as the result of "select * from INFORMATION_SCHEMA.TABLES"
            
            Keys:
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

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 08:50:03
            `@memberOf`: Table
            `@property`: meta_data
        '''
        return _meta_data(self)

    def register_column(self,column:Union[dict,_db_column_type]):
        '''
            Register a column instance with this table.

            ----------

            Arguments
            -------------------------
            `column` {Column,dict}
                The column instance or dictionary of data to register.


            Return {None}
            ----------------------
            None

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:35:18
            `memberOf`: Table
            `version`: 1.0
            `method_name`: register_column
            * @xxx [12-13-2022 12:36:52]: documentation for register_column
        '''
        if isinstance(column,(dict)):
            column = _Column(self.database,self,column)
            # rel = column.relationship
            # if rel is not None:
                # self._relationships.append(rel)
        self._columns.append(column)

    def register_relationship(self,relationship:_db_relationship_type):
        '''
            Register a relationship instance with this table.

            ----------

            Arguments
            -------------------------
            `relationsihp` {Relationship,dict}
                The relationship instance or dictionary of data to register.


            Return {None}
            ----------------------
            None

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:35:18
            `memberOf`: Table
            `version`: 1.0
            `method_name`: register_column
            * @xxx [12-13-2022 12:36:52]: documentation for register_column
        '''
        # if isinstance(relationship,(dict)):
        #     relationship = _rel.Relationship(self.database,self,relationship)
        if isinstance(relationship,_rel.Relationship):
            if self.get_relationship(relationship.name) is None:
                self._relationships.append(relationship)
            # self._relationships[relationship.name] = relationship
    def get_relationship(self,name:str)->_db_relationship_type:
        rel:_db_relationship_type
        for rel in self._relationships:
            if rel.name == name:
                return rel
        # if name in self._relationships:
        #     return self._relationships[name]
        return None

    def gen_hash_id(self):
        '''
            Generate a hash_id specific for this table, if the table supports a hash_id column.
            ----------

            Return {str,None}
            ----------------------
            The hash_id if the table supports it, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:34:03
            `memberOf`: Table
            `version`: 1.0
            `method_name`: gen_hash_id
            * @xxx [12-13-2022 12:35:06]: documentation for gen_hash_id
        '''
        if self.has_hash_id:
            if self.hash_id_prefix is not None:
                return f"{self.hash_id_prefix}_{_rand.rand((self._hash_id_column.data.character_maximum_length - len(self.hash_id_prefix)))}"


    @property
    def child_tables(self)->Iterable[_db_table_type]:
        '''
            Get all table instances that are children of this table.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-21-2022 09:49:13
            `@memberOf`: Table
            `@property`: child_tables
        '''
        value = self.database.get_table_children(self.name)
        return value

    @property
    def parent_tables(self)->Iterable[_db_table_type]:
        '''
            Get all table instances that are parents of this table.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-21-2022 09:49:13
            `@memberOf`: Table
            `@property`: child_tables
        '''
        value = self.database.get_table_parents(self.name)
        return value





    # ---------------------------------------------------------------------------- #
    #                            COLUMN SUPPORT METHODS                            #
    # ---------------------------------------------------------------------------- #


    @property
    def columns(self)->Iterable[_db_column_type]:
        '''
            Get the columns associated to this table.
            
            If None are registered with this table, it will query the database.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-06-2022 12:27:28
            `@memberOf`: __init__
            `@property`: columns
        '''
        value = self._columns
        if len(value) == 0:
            _log("table.columns - no columns associated to table, requesting data from the database.","info")
            cols = self.database.get_column_data(self.table_name)
            if isinstance(cols,(list)):
                for col in cols:
                    self.register_column(col)
                    # self.register_column(_column.Column(self.database,self,col))
        return self._columns

    @columns.setter
    def columns(self,value):
        '''
            Set the columns property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-06-2022 12:17:29
            `@memberOf`: __init__
            `@property`: columns
        '''
        self._columns = value

    @property
    def primary_id(self):
        '''
            Get this Table's primary_id column instance

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-13-2022 11:52:51
            `@memberOf`: Table
            `@property`: primary_id
        '''
        value = self._primary_id
        if value is None:
            for col in self.columns:
                if col.data.is_primary:
                    value = col
                    self._primary_id = col
                    break
        return value
    
    @property
    def primary_column_name(self):
        '''
            Get this Table's primary column name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-21-2022 08:35:46
            `@memberOf`: Table
            `@property`: primary_column_name
        '''
        value = self.primary_id.data.column_name
        return value
    
    
    @property
    def hash_id(self):
        '''
            Get this Table's hash_id column instance, if it exists.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-19-2022 11:03:27
            `@memberOf`: Table
            `@property`: hash_id
        '''
        if self.has_hash_id:
            for col in self.columns:
                if col.data.is_hash_id:
                    self._hash_id = col
                    return self._hash_id
        return None


    @property
    def foreign_keys(self)->Iterable[_db_column_type]:
        output = []
        col:_db_column_type
        for col in self.columns:
            if col.sql_data.is_foreign_key:
                output.append(col)
        return output

    def get_column_by_name(self,name)->_db_column_type:
        for col in self.columns:
            
            if col.data.column_name == name:
                return col
        return None

    @property
    def name(self)->str:
        '''
            Get this table's name.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:40:58
            `@memberOf`: PostArg
            `@property`: name
        '''
        value = self.table_name
        self._name = value

        return value

    @name.setter
    def name(self,value:str):
        '''
            Set the name value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:40:58
            `@memberOf`: PostArg
            `@property`: name
        '''
        self._name = value

    def populate_from_dict(self,data:dict):
        '''Used internally to populate the instance from caches.'''
        populate_from_dict(data,self)

    @property
    def has_deleted_column(self)->bool:
        '''
            Check if this table has a column used for denoting that a row is "deleted".

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:36:20
            `@memberOf`: PostArg
            `@property`: has_deleted_column
        '''

        for col in self.columns:
            if col.data.is_deleted is True:
                self._has_deleted_column = True

        return self._has_deleted_column

    @has_deleted_column.setter
    def has_deleted_column(self,value):
        '''
            Set the Table's has_deleted_column property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:49:47
            `@memberOf`: Table
            `@property`: has_deleted_column
        '''
        self._has_deleted_column = value

    @property
    def has_hash_id(self)->bool:
        '''
            Check if this table has a column used storing a hash_id.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:36:20
            `@memberOf`: PostArg
            `@property`: has_hash_id
        '''
        value = self._has_hash_id
        if value is None:
            value = False
            for col in self.columns:
                # print(f"col.data:{col.data.summary()}")
                if col.data.is_hash_id is True:
                    # print(f"hash_id column found: {col.data.column_name}")
                    self._hash_id_column = col
                    value = True
                    # self._has_hash_id = True
                    break
            self._has_hash_id = value
        return self._has_hash_id

    @has_hash_id.setter
    def has_hash_id(self,value):
        '''
            Set the Table's has_hash_id property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:49:28
            `@memberOf`: Table
            `@property`: has_hash_id
        '''
        self._has_hash_id = value

    @property
    def hash_id_prefix(self):
        '''
            If this table supports a hash_id column this will contain the prefix used to denote the hash_id.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:44:30
            `@memberOf`: Table
            `@property`: hash_id_prefix
        '''

        if self.has_hash_id is False:
            return None

        value = self._hash_id_column.data.hash_id_prefix
        return value

    @hash_id_prefix.setter
    def hash_id_prefix(self,value):
        '''
            Set the Table's hash_id_prefix property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:50:02
            `@memberOf`: Table
            `@property`: hash_id_prefix
        '''
        self._hash_id_prefix = value

    @property
    def has_timestamp_column(self)->bool:
        '''
            Check if this table has a column used storing a timestamp_column.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:36:20
            `@memberOf`: PostArg
            `@property`: has_timestamp_column
        '''
        value = self._has_timestamp_column
        if value is None:
            for col in self.columns:
                if col.data.is_timestamp is True:
                    value = True
            self._has_timestamp_column = value
        return value

    @has_timestamp_column.setter
    def has_timestamp_column(self,value):
        '''
            Set the Table's has_timestamp_column property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:50:31
            `@memberOf`: Table
            `@property`: has_timestamp_column
        '''
        self._has_timestamp_column = value

    @property
    def has_modified_timestamp_column(self)->bool:
        '''
            Check if this table has a column used storing a modified_timestamp_column.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:36:20
            `@memberOf`: PostArg
            `@property`: has_modified_timestamp_column
        '''
        value = self._has_modified_timestamp_column
        if value is None:
            for col in self.columns:
                if col.data.is_modified_timestamp is True:
                    value = True
            self._has_modified_timestamp_column = value
        return value

    @has_modified_timestamp_column.setter
    def has_modified_timestamp_column(self,value):
        '''
            Set the Table's has_modified_timestamp_column property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:50:41
            `@memberOf`: Table
            `@property`: has_modified_timestamp_column
        '''
        self._has_modified_timestamp_column = value

    @property
    def column_names(self):
        '''
            Get a list of this Table's column names

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-21-2022 08:38:55
            `@memberOf`: Table
            `@property`: column_names
        '''
        if self._column_names is None:
            names = []
            for col in self.columns:
                names.append(col.data.column_name)
            self._column_names = names
        return self._column_names

    @property
    def longest_column_name(self):
        '''
            Get this Table's longest column name as a tuple:

            (20,someFuckinColumnName)

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-21-2022 08:37:11
            `@memberOf`: Table
            `@property`: longest_column_name
        '''
        if self._longest_column_name is None:
            self._longest_column_name = _lu.longest_string(self.column_names)
        return self._longest_column_name



    # ---------------------------------------------------------------------------- #
    #                             QUERY SUPPORT METHODS                            #
    # ---------------------------------------------------------------------------- #


    def insert(self,data:dict,**kwargs)->Union[int,dict,bool]:
        '''
            Insert a dictionary of data into this table
            ----------

            Arguments
            -------------------------
            `data` {dict}
                The data to be inserted into this table, where the keys correspond to columns.

            Keyword Arguments
            -------------------------
            [`return_row`=True] {bool}
                If True, the entire row will be retrieved after a successful insertion and returned as a dictionary.

            Return {int,dict,bool}
            ----------------------
            The integer id of the inserted row if successful, False otherwise.

            if return_row is True, the row dictionary is returned.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 11:43:55
            `memberOf`: Table
            `version`: 1.0
            `method_name`: insert
            * @TODO []: documentation for insert
        '''
        
        from colemen_utilities.database_utils.MySQL.InsertQuery import InsertQuery
        
        InsertQuery(database=self.database,table=self)
        
        cerberus_validate = _obj.get_kwarg(['cerberus_validate'],False,(bool),**kwargs)
        return_row = _obj.get_kwarg(['return_row'],True,(bool),**kwargs)
        
        result = self.database.insert_to_table(self.table_name,data,cerberus_validate)
        if result:
            if return_row:
                s = self.select_query()
                s.add_where(self.primary_id.name,result,"=")
                result = s.execute()
        return result

    def insert_query(self):
        return self.database.insert_query(self)

    def select_query(self):
        '''Create a new select query instance for this table.'''
        return self.database.select_query(self)

    def update_query(self):
        '''Create a new update query instance for this table.'''
        return self.database.update_query(self)
        # return self.database.update_query(self.table_name)

    def delete_query(self):
        '''Create a new delete query instance for this table.'''
        return self.database.delete_query(self)
        # return self.database.delete_query(self.table_name)

    @property
    def cerberus_validation_schema(self):
        '''
            Get this Table's cerberus_validation_schema

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 13:47:07
            `@memberOf`: Table
            `@property`: cerberus_validation_schema
        '''
        value = self._cerberus_validations
        if value is None:
            value = {
                "create":[],
                "read":[],
                "update":[],
                "delete":[],
            }
            col:_db_column_type
            cols = self.columns
            for col in cols:
                value['create'].append(col.validation.cerberus_schema("create"))
                value['read'].append(col.validation.cerberus_schema("read"))
                value['update'].append(col.validation.cerberus_schema("update"))
                value['delete'].append(col.validation.cerberus_schema("delete"))


            self._cerberus_validations = value
        return value


    def create_cerberus_validation_schema(self,**kwargs):
        _obj.get_kwarg(['post_arguments'],False,)

    @property
    def comment(self)->str:
        '''
            Get this tables comment if there is one.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-20-2022 11:18:08
            `@memberOf`: PostArg
            `@property`: comment
        '''
        value = self.table_comment
        return value

    @comment.setter
    def comment(self,value:str):
        '''
            Set this tables comment.

            This will execute an ALTER query to save the comment to the table.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-20-2022 11:18:08
            `@memberOf`: PostArg
            `@property`: comment
        '''
        self.table_comment = value
        sql = f"ALTER TABLE `{self.database.name}`.`{self.name}` COMMENT = '%s';"
        args = [self.table_comment]
        return self.database.run(sql,args)








    def api_endpoint_url(self,crud_type:str=None):
        if crud_type is None or crud_type in ['create','update','delete','read_single']:
            return self.api_url_base
        if crud_type in ['read']:
            return f"/{self.name_.camel.plural}"
    @property
    def api_url_base(self):
        if self.has_hash_id:
            return f"/{self.name_.camel.singular}/{self._hash_id_column.data.flask_url_placeholder}"
        return f"/{self.name_.camel.singular}"




def populate_from_dict(data:dict,table:Table):
    columns = None
    relationships = None
    table_data = data
    # print(f"table_data: {table_data}")
    # @Mstep [IF] if table_data in the dictionary, this means the dict is from a cache file.
    if "table_data" in data:
        _log("table.populate.from_dict - table_data key located in data dictionary","info")
        table_data = data['table_data']
        if "columns" in table_data:
            _log("table.populate.from_dict -    columns key located in table_data dictionary","info")
            columns = table_data['columns']
            del table_data['columns']
        if "relationships" in table_data:
            _log("table.populate.from_dict -    relationships key located in table_data dictionary","info")
            relationships = table_data['relationships']
            del table_data['relationships']


    if columns is not None:
        _log("table.populate_from_dict -    Loading Columns from cache","info")
        for col in columns:
            table.register_column(col)

    for k,v in table_data.items():
        # @Mstep [IF] if the key is for columns skip it
        if k == "columns" and columns is not None:
            _log("table.populate.from_dict -        skipping columns key from table_data dictionary","info")
            continue
        if k == "table_name":
            setattr(table,"name",v)
            # setattr(table,"name",_name.Name(v))
            continue
        if k == "table_schema":
            setattr(table,"schema",v)
            continue

        # @Mstep [IF] if the key is table_comment
        if k == "table_comment":
            _log(f"table.populate.from_dict - table_comment found {table.name}","magenta invert")
            # @Mstep [] parse the comment as YAML
            yd = parse_comment_yaml(v)
            if isinstance(yd,(dict)):
                # print(yd)
                # @Mstep [LOOP] iterate the comments keys
                for ck,cv in yd.items():
                    # @Mstep [] assign the comment keys to the table
                    if hasattr(table,ck):
                        setattr(table,ck,cv)
            setattr(table,"table_comment",v)
            continue

        if hasattr(table,k):
            setattr(table,k,v)

    # @Mstep [IF] if there are relationships
    if relationships is not None and len(relationships) > 0:
        _log(f"table.populate_from_dict -   Loading {table.name} relationships from cache","info")
        # @Mstep [LOOP] iterate the relationships
        for rel in relationships:
            # @Mstep [] get the column this relationship references
            column = table.get_column_by_name(rel['column'])
            # @Mstep [IF] if the column is successfully located
            if isinstance(column,_Column):
                # @Mstep [] instantiate the relationship instance.
                _rel.Relationship(table.database,table,column,rel)



def _meta_data(table)->dict:
    '''
        Get this Table's meta_data as a dictionary with the keys:
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

        `default`:None


        Meta
        ----------
        `@author`: Colemen Atwood
        `@created`: 12-16-2022 08:50:03
        `@memberOf`: Table
        `@property`: meta_data
    '''
    value = {
            "table_catalog":table.table_catalog,
            "table_schema":table.table_schema,
            "table_name":table.table_name,
            "table_type":table.table_type,
            "engine":table.engine,
            "version":table.version,
            "table_rows":table.table_rows,
            "row_format":table.row_format,
            "avg_row_length":table.avg_row_length,
            "data_length":table.data_length,
            "max_data_length":table.max_data_length,
            "index_length":table.index_length,
            "data_free":table.data_free,
            "auto_increment":table.auto_increment,
            "table_collation":table.table_collation,
            "checksum":table.checksum,
            "table_comment":table.table_comment
    }
    return value


