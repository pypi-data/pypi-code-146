
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import json
# import importlib
from dataclasses import dataclass
from re import L
# from typing import List
from typing import Iterable, Union



# import colemen_utilities.database_utils.MySQL.Column.Column as _Column
# from colemen_utilities.database_utils.MySQL.Column.Column import Column as _Column
# from colemen_utilities.database_utils.MySQL.Column import column_utils as _u
from colemen_config import _db_table_type,_db_column_type,_db_mysql_database_type
# from colemen_utilities.database_utils.MySQL import CacheFile as _CacheFile
# import colemen_utilities.database_utils.MySQL.CacheFile as _CacheFile
import colemen_utilities.dict_utils as _obj
import colemen_utilities.random_utils as _rand
import colemen_utilities.string_utils as _csu
import colemen_utilities.console_utils as _con
_log = _con.log




@dataclass
class Relationship:
    database:_db_mysql_database_type = None
    '''The database instance that this column belongs to'''
    table:_db_table_type = None
    '''The table instance that this column belongs to'''
    column:_db_column_type = None
    '''The column instance'''


    foreign_schema:_db_mysql_database_type = None
    '''The database instance that the foreign table belongs to'''
    foreign_table:_db_table_type = None
    '''The table instance that the foreign column belongs to'''
    foreign_column:_db_column_type = None
    '''The foreign column instance'''

    # foreign_table:_db_table_type = None
    # foreign_column:_db_column_type = None


    foreign_table_schema:str = None
    '''The name of the foreign schema'''
    foreign_table_name:str = None
    '''The name of the foreign table'''
    foreign_column_name:str = None
    '''The name of the foreign column'''

    foreign_key_constraint_name:str = None
    '''The name of the foreign key constraint'''

    update_rule:str = None
    '''The value of the constraint ON UPDATE attribute. The possible values are CASCADE, SET NULL, SET DEFAULT, RESTRICT, NO ACTION.'''

    delete_rule:str = None
    '''The value of the constraint ON DELETE attribute. The possible values are CASCADE, SET NULL, SET DEFAULT, RESTRICT, NO ACTION.'''

    _parent_table_found:bool = None
    '''True if the parent table's instance has been found, False otherwise'''

    def __init__(self,database:_db_mysql_database_type,table:_db_table_type,column:_db_column_type,data:dict) -> None:
        self.database:_db_mysql_database_type = database
        self._dbm = self.database._dbm
        self.table:_db_table_type = table
        self.column:_db_column_type = column

        if isinstance(data,(dict)):
            populate_from_dict(data,self)


        # @Mstep [] register this relationship with the database.
        self.database.register(self)
        self.table.register_relationship(self)


    @property
    def summary(self):
        '''
            Get this Relationship's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 11:36:41
            `@memberOf`: Relationship
            `@property`: summary
        '''
        value = {
            "foreign_key_constraint_name":self.foreign_key_constraint_name,
            "database":self.database.name,
            "table":self.table.name,
            "column":self.column.data.column_name,
            "update_rule":self.update_rule,
            "delete_rule":self.delete_rule,
            "foreign_column_name":self.foreign_column_name,
            "foreign_table_name":self.foreign_table_name,
            "foreign_table_schema":self.foreign_table_schema,
        }
        if self.parent_table is not None:
            value["foreign_database"] = self.parent_table.database.name
            value["foreign_table"] = self.parent_table.name
            value["foreign_column"] = self.parent_column.data.column_name
        return value

    @property
    def name(self):
        '''
            Get this Relationship's name a.k.a. `foreign_key_constraint_name`

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 12:15:15
            `@memberOf`: Relationship
            `@property`: name
        '''
        value = self.foreign_key_constraint_name
        return value

    # @property
    # def update_rule(self):
    #     '''
    #         Get this Relationship's update_rule

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-16-2022 12:12:43
    #         `@memberOf`: Relationship
    #         `@property`: update_rule
    #     '''
    #     return self._update_rule
    
    # @update_rule.setter
    # def update_rule(self,value):
    #     '''
    #         Set the Relationship's update_rule property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-16-2022 13:07:41
    #         `@memberOf`: Relationship
    #         `@property`: update_rule
    #     '''
    #     print(f"setting update_rule {self.name} - {value}")
    #     self._update_rule = value
    
    # @property
    # def delete_rule(self):
    #     '''
    #         Get this Relationship's delete_rule

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-16-2022 12:12:43
    #         `@memberOf`: Relationship
    #         `@property`: delete_rule
    #     '''
    #     return self._delete_rule

    # @delete_rule.setter
    # def delete_rule(self,value):
    #     '''
    #         Set the Relationship's delete_rule property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-16-2022 13:07:51
    #         `@memberOf`: Relationship
    #         `@property`: delete_rule
    #     '''
    #     self._delete_rule = value

    @property
    def parent_table(self)->_db_table_type:
        '''
            Get this Relationship's parent_table

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 11:13:55
            `@memberOf`: Relationship
            `@property`: parent_table
        '''
        if self.foreign_table is not None:
            return self.foreign_table

        # @Mstep [IF] if the foreign table is in a different schema.
        if self.foreign_table_schema != self.database.name:
            # @Mstep [IF] if the database does not have a database manager.
            if self.database._dbm is None:
                # @Mstep [] alert the user that a table cannot be found without access to the schema.
                _log("Failed to locate parent table for relationship, the foreign table belongs to a different schema. ","warning")
            # @Mstep [ELSE] if the database does have a database manager.
            else:
                # @Mstep [] have the database maanger search across schemas to find the table.
                table = self.database._dbm.get_table(self.foreign_table_name,self.foreign_table_schema)
                # @Mstep [IF] if the table is not found.
                if table is None:
                    # @Mstep [IF] alert the user that the table could not be found.
                    
                    _log("\n")
                    _log(f"Failed to locate parent table for relationship, the manager could not locate the table {self.foreign_table_name}. ","warning")
                    _log(f"foreign table: {self.foreign_table_schema}.{self.foreign_table_name}?","warning")
                    _log(f"Have all tables been indexed by the manager?","warning")
                else:
                    self.foreign_table = table
                    self._parent_table_found = True
                    # return table
        # @Mstep [IF] if the foreign table is in the same schema.
        else:
            # @Mstep [] get the table from the database.
            table = self.database.get_table(self.foreign_table_name)
            # @Mstep [IF] if the table cannot be located.
            if table is None:
                # @Mstep [] alert the user that the table was not found in the schema.
                _log(f"Failed to locate parent table for relationship, the schema {self.database.name} could not locate the table {self.foreign_table_name}. ","warning")
                _log(f"foreign table: {self.foreign_table_schema}.{self.foreign_table_name}?","warning")
                _log(f"Have all tables been indexed by the manager?","warning")
            else:
                self.foreign_table = table
                self._parent_table_found = True
                # return table
        # value = self.foreign_table


        return self.foreign_table

    @property
    def child_table(self):
        '''
            Get this Relationship's child_table

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 11:26:34
            `@memberOf`: Relationship
            `@property`: child_table
        '''
        return self.table

    @property
    def parent_column(self):
        '''
            Get this Relationship's parent_column a.k.a. foreign_column

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 11:42:14
            `@memberOf`: Relationship
            `@property`: parent_column
        '''
        value = self.foreign_column
        if value is None:
            parent = self.parent_table
            if parent is not None:
                col = parent.get_column_by_name(self.foreign_column_name)
                if col is not None:
                    value = col
                    self.foreign_column = value
        return value

    @property
    def parent_table_found(self):
        '''
            Determine if the parent table instance has been found.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 11:51:51
            `@memberOf`: Relationship
            `@property`: parent_table_found
        '''

        if self._parent_table_found is not True:
            # @Mstep [] trigger the parent table search to update the _parent_table_found value
            pt = self.parent_table
        return self._parent_table_found


    def is_parent(self,table:Union[str,_db_table_type])->bool:
        '''
            Check if the table name provided is the parent of this relationship

            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to test against the parent of this relationship.


            Return {bool}
            ----------------------
            True if the table is the parent_table of this relationship, False otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 11:29:33
            `memberOf`: Relationship
            `version`: 1.0
            `method_name`: is_parent
            * @TODO []: documentation for is_parent
        '''
        table_name = _table_to_name(table)
        if self.foreign_table_name == table_name:
            return True
        return False

    def is_child(self,table:Union[str,_db_table_type])->bool:
        '''
            Check if the table name provided is the child of this relationship

            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to test against the child of this relationship.


            Return {bool}
            ----------------------
            True if the table is the child_table of this relationship, False otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 11:29:33
            `memberOf`: Relationship
            `version`: 1.0
            `method_name`: is_parent
            * @xxx [12-16-2022 12:04:10]: documentation for is_parent
        '''
        table_name = _table_to_name(table)
        if self.table.name == table_name:
            return True
        return False




def _table_to_name(table:Union[str,_db_table_type]):
    '''returns a table name if the table instance is provided.'''
    from colemen_utilities.database_utils.MySQL.Table import Table
    if isinstance(table,Table.Table):
        table = table.name
    return table


def populate_from_dict(data:dict,rel:Relationship):
    for k,v in data.items():
        if k in ['database','table','column',"foreign_schema","foreign_table","foreign_column"]:
            continue
        
        if k == "constraint_name":
            k = "foreign_key_constraint_name"
        # if k in ["delete_rule","update_rule"]:
        #     k = f"_{k}"

        if hasattr(rel,k):
            setattr(rel,k,v)
    if isinstance(rel.table.raw_referential_constraints,(list)):
        for ref in rel.table.raw_referential_constraints:
            if ref['CONSTRAINT_NAME'] == rel.foreign_key_constraint_name:
                rel.update_rule = ref['UPDATE_RULE']
                rel.delete_rule = ref['DELETE_RULE']
# def new(database:_db_mysql_database_type,table:_db_table_type,column:_db_column_type,data:dict):
#     Relationship()

