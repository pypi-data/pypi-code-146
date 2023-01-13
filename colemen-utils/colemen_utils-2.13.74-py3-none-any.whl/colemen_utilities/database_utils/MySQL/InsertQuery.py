# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    A module of utility methods used for parsing and converting python types.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: type_utils
'''



from dataclasses import dataclass
import re as re
import os as _os
from re import L
import sys
import time
from typing import Union as _Union
from typing import Iterable as _Iterable

import mysql.connector
import traceback as _traceback
from mysql.connector import Error
from colorama import Fore as _Fore
from colorama import Style as _Style
from colemen_config import _db_table_type,_db_mysql_database_type
import colemen_utilities.dict_utils as _obj
import colemen_utilities.file_utils as _cfu
import colemen_utilities.directory_utils as _dirs
import colemen_utilities.string_utils as _csu
import colemen_utilities.list_utils as _lu
import colemen_utilities.console_utils as _con
import colemen_utilities.database_utils.MySQL.QueryBase as _QueryBase
_log = _con.log


@dataclass
class InsertQuery(_QueryBase.QueryBase):

    return_row:bool = True
    '''If True the execute method will return the newly inserted row, otherwise the id is returned.'''

    _columns = None
    '''A dictionary of columns with their associated values to be inserted into the table.'''






    def __init__(self,**kwargs):
        '''
            Create an insert query instance.
            ----------

            Arguments
            -------------------------
            `arg_name` {type}
                arg_description

            Keyword Arguments
            -------------------------
            `quote_char` {str}
                The character used to wrap terms in the query.

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-14-2022 10:45:26
            `memberOf`: InsertQuery
            `version`: 1.0
            `method_name`: InsertQuery
            * @TODO []: documentation for InsertQuery
        '''
        super().__init__(**kwargs)
        self._columns = {}
        self.crud_type = "create"

    def execute(self)->_Union[bool,dict,int]:
        if self.database is None:
            raise Exception("Insert Query does not have a database to execute the query on")

        sql,args= self.query
        if sql is False:
            return False
        
        # @Mstep [] execute the insert query.
        result = self.database.run(sql,args)
        # @Mstep [IF] if the query was successful.
        if result is True:
            # @Mstep [] get the id of the inserted role.
            result = self.database.last_id()
            if self.return_row is True:
                s = self.table.select_query()
                s.correlate_to_table = False
                s.add_where(self.table.primary_id.name,result,"=")
                row = s.execute()
                if isinstance(row,(list)):
                    result = row[0]
                    
        # print(f"sql: {sql}")
        # print(f"args: {args}")
        return result

    @property
    def query(self):
        '''
            Get this InsertQuery's query

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:44:59
            `@memberOf`: InsertQuery
            `@property`: query
        '''


        # @Mstep [IF] if the database instance exists and correlate_to_table is True
        if self.database is not None and self.correlate_to_table is True:
            # @Mstep [] correlate this table's columns to the table's columns
            self._columns = self.database.correlate_to_table(
                self.table_name,
                self._columns,
                crud=self.crud_type
            )
        # print(f"INSERTION COLUMNS---------------")
        # print(self._columns)
        # print(f"INSERTION COLUMNS---------------")
        data = self._columns

        if len(data.keys()) == 0:
            _log("No keys in the data dict were correlated to columns in the table.","warning")
            return False

        value_string = ','.join(['%s' for x in list(range(len(data.keys())))])

        value = f"INSERT INTO {self._schema_table_string} ({self.column_list_string}) VALUES ({value_string})"
        # return (sql,list(data.values()))


        # value = _format_query_params(value,self._params)
        return value,list(data.values())

    @property
    def column_list_string(self):
        '''
            Generate the SQL list of column names.

            This will skip columns that start with underscores.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-14-2022 10:40:39
            `@memberOf`: InsertQuery
            `@property`: column_list_string
        '''
        if len(self._columns) == 0:
            return None
        columns = self._columns.keys()
        # if isinstance(columns,(dict)):

        column_array = []
        # @Mstep [LOOP] iterate the column names.
        for name in columns:
            # @Mstep [IF] if the first char is an underscore.
            if name[0] == "_":
                # @Mstep [] go to the next indice.
                continue
            # @Mstep [] append the column name wrapped in accents to the column_array
            column_array.append(f"{self.quote_char}{name}{self.quote_char}")
        # @Mstep [] join the column_array with commas
        # @Mstep [RETURN] return column string
        return ', '.join(column_array)

    def add_column(self,column_name:_Union[str,dict],value=None):
        '''
            Add a column or multiple columns to be inserted to the table.



            Arguments
            -------------------------
            `column_name` {dict,str}
                The name of the column to add.

                This can also be a dictionary of columns and their values.

            [`value`=None] {any}
                The value to assign to the column

                If the column_name is a dictionary, this is ignored.

            Keyword Arguments
            -------------------------
            `arg_name` {type}
                arg_description

            Return {None}
            ----------------------
            returns nothing.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-14-2022 11:14:19
            `memberOf`: InsertQuery
            `version`: 1.0
            `method_name`: add_column
            * @xxx [12-14-2022 11:16:09]: documentation for add_column
        '''
        if isinstance(column_name,(dict)):
            for k,v in column_name.items():

                self._columns[k] = v
                # data = {
                #     "column_name":k,
                #     "value":v,
                # }
                # self._columns.append(data)
            return
        else:
            self._columns[column_name] = value



if __name__ == '__main__':
    import time
    q = InsertQuery(
        table_name="blackholes",
        schema_name="boobs",
    )
    # q.add_where("expiration",(0,time.time()),"between")
    # q.add_where("expiration",time.time(),"<=")
    q.add_column("ip_address","50.26.8.91")
    q.add_column("reason","I just really hate this guy")
    # q.add_select("hash_id")
    sql,args = q.query
    print(sql)
    print(args)

