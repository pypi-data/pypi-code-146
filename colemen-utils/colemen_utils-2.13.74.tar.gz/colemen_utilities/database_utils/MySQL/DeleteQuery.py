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
# import os as _os

# import sys
# import time
# from typing import Union as _Union
# from typing import Iterable as _Iterable

from colemen_config import _db_table_type,_db_mysql_database_type

import colemen_utilities.string_utils as _csu
import colemen_utilities.list_utils as _lu
import colemen_utilities.console_utils as _con
import colemen_utilities.database_utils.MySQL.QueryBase as _QueryBase
_log = _con.log


@dataclass
class DeleteQuery(_QueryBase.QueryBase):
    
    limit:int = 1
    offset:int = None


    soft_delete:bool = True
    '''If True and the table supports it, the row's "deleted" column will be updated instead of actually deleted'''
    
    _selects = None
    _params = None
    



    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.crud_type = "delete"
        self._selects = []
        self._params = {}


    def execute(self):
        if self.database is None:
            raise Exception("Delete Query does not have a database to execute the query on")
        sql,args= self.query
        # _log(f"sql: {sql}","magenta")
        # _log(f"args: {args}","magenta")
        return self.database.run(sql,args)



    @property
    def query(self):
        '''
            Get this DeleteQuery's query

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:44:59
            `@memberOf`: DeleteQuery
            `@property`: query
        '''
        value = None
        if self.soft_delete is True and self.table.has_deleted_column is True:
            u = self.table.update_query()
            # u.add_column("deleted",)
            u.crud_type = "delete"
            u.limit = self.limit
            u.offset = None
            for where in self._wheres:
                u.add_where_from_where(**where)
            value,self._params = u.query
        else:
            value = f"DELETE FROM {self._schema_table_string}{self.where_string}"
            value = self._paginate_select_query(value)
            value = self._format_query_params(value,self._params)
        return value,self._params


if __name__ == '__main__':
    import time
    q = DeleteQuery(
        table_name="blackholes",
        schema_name="boobs",
    )
    # q.add_where("expiration",(0,time.time()),"between")
    # q.add_where("expiration",time.time(),"<=")
    q.add_where("ip_address","50.26.8.91","=")
    # q.add_select("hash_id")
    sql,args = q.query
    print(sql)
    print(args)

