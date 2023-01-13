# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    Used for generating an SQL update query to execute on a database.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: type_utils
'''



from dataclasses import dataclass
import re as re
# import os as _os

# import sys
# import time
# from typing import Union as _Union
# from typing import Iterable as _Iterable

# import mysql.connector
# import traceback as _traceback
# from mysql.connector import Error
# from colorama import Fore as _Fore
# from colorama import Style as _Style
from colemen_config import _db_mysql_database_type
import colemen_utilities.dict_utils as _obj
import colemen_utilities.file_utils as _cfu
import colemen_utilities.directory_utils as _dirs
import colemen_utilities.string_utils as _csu
import colemen_utilities.list_utils as _lu


# import colemen_utilities.database_utils.TableManager as _table_manager

# import colemen_utilities.database_utils.TableManager as _table_manager

# import colemen_utilities.database_utils as _cdb
# _TableManager = _cdb.TableManager
import colemen_utilities.console_utils as _con
import colemen_utilities.database_utils.MySQL.QueryBase as _QueryBase
_log = _con.log


@dataclass
class UpdateQuery(_QueryBase.QueryBase):
    # table_name:str = None
    # schema_name:str = None
    # database:_db_mysql_database_type = None
    
    limit:int = None
    offset:int = None
    statement:str = None
    args = None
    
    

    return_row:bool = True
    '''If True the execute method will return the updated row, otherwise the id is returned.'''

    # _count:bool = False
    # '''True if this query should return the count of rows selected'''

    # _average:bool = False
    # '''True if this query should return the average of rows selected'''

    # _sum_:bool = False
    # '''True if this query should return the sum of rows selected'''

    _updates = None
    _params = None



    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.crud_type = "update"
        self._updates = {}
        self._params = {}


    def execute(self):
        if self.database is None:
            raise Exception("Update Query does not have a database to execute the query on")

        sql,args= self.query
        if sql is False:
            return False

        print(f"sql: {sql}")
        print(f"args: {args}")
        result = self.database.run(sql,args)
        if result is True:
            if self.return_row is True and self.table is not None:
                s = self.table.select_query()
                for where in self._wheres:
                    s.add_where_from_where(**where)
                return s.execute()
        return result

    @property
    def query(self):
        '''
            Get this UpdateQuery's query

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:44:59
            `@memberOf`: UpdateQuery
            `@property`: query
        '''

        # print(self._updates)
        # @Mstep [IF] if the database instance exists and correlate_to_table is True
        if self.database is not None and self.correlate_to_table is True:
            # @Mstep [] correlate this table's columns to the table's columns
            self._updates = self.database.correlate_to_table(
                self.table,
                self._updates,
                crud=self.crud_type
            )

        # print(self._updates)

        value = f"UPDATE {self._schema_table_string} SET {self.update_string}{self.where_string}"

        value = self._paginate_select_query(value)
        value = self._format_query_params(value,self._params)
        return value,self._params

    @property
    def update_string(self):
        '''
            Get this UpdateQuery's update_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:56:15
            `@memberOf`: UpdateQuery
            `@property`: update_string
        '''
        if len(self._updates) == 0:
            return None
        else:
            selects = []
            for k,v in self._updates.items():
                value = None
                value = f"{k}=:{k}"
                self._params[k] = v
                selects.append(value)
            value = ', '.join(selects)

        return value

    def add_column(self,column_name,value):
        # if self.database is not None:
        #     tb = self.database.get_table(self.table_name)
        #     col = tb.get_column_by_name(column_name)
        #     if col.validation.update_post_args is False:

        # data = {
        #     "column_name":column_name,
        #     "value":value,
        # }
        # self._updates.append(data)
        # self.validate()
        self._updates[column_name] = value



if __name__ == '__main__':
    import time
    q = UpdateQuery(
        table_name="blackholes",
        schema_name="boobs",
    )
    # q.add_where("expiration",(0,time.time()),"between")
    q.add_where("hash_id","blackhole_RgH1OzdPnkGbj9dES593UlXc","=")
    q.add_column("reason","someShit")
    q.add_column("message","boobies")
    # q.add_select("hash_id")
    sql,args = q.query
    print(sql)
    print(args)

