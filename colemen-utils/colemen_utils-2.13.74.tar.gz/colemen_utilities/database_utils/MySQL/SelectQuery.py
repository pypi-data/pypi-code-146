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


from colemen_config import _db_mysql_database_type
import colemen_utilities.string_utils as _csu
import colemen_utilities.list_utils as _lu


import colemen_utilities.console_utils as _con
import colemen_utilities.database_utils.MySQL.QueryBase as _QueryBase
_log = _con.log

@dataclass
class SelectQuery(_QueryBase.QueryBase):

    limit:int = 100
    '''The limit of how many results are allowed to be returned.'''

    offset:int = None
    '''The offset of the result set.'''

    statement:str = None

    args = None
    _count:bool = False
    '''True if this query should return the count of rows selected'''
    _average:bool = False
    '''True if this query should return the average of rows selected'''
    _sum_:bool = False
    '''True if this query should return the sum of rows selected'''

    _deleted_where_used:bool = None
    '''If True, then the deleted column is referenced in the wheres list'''

    include_deleted:bool = False
    '''If True and the table support it, soft deleted rows are included in the query'''

    _selects = None
    _params = None



    def __init__(self,**kwargs):
        self._selects = []
        self._params = {}
        super().__init__(**kwargs)
        self.crud_type = "read"


    def execute(self,default=None):
        '''
            Execute this query's SQL and return its results.
            ----------

            Arguments
            -------------------------
            [`default`=None] {any}
                The default value to return if nothing is found.


            Return {any}
            ----------------------
            The results of the query if successful, the default value otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:12:16
            `memberOf`: SelectQuery
            `version`: 1.0
            `method_name`: execute
            * @xxx [12-13-2022 12:14:14]: documentation for execute
        '''
        if self.database is None:
            raise Exception("Select Query does not have a database to execute the query on")
        sql,args= self.query
        # print(f"sql: {sql}")
        # print(f"args: {args}")
        return self.database.run_select(sql,args,default=default)


    @property
    def query(self):
        '''
            Get the compiled and parameterized SQL query with the parameter dictionary.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:44:59
            `@memberOf`: SelectQuery
            `@property`: query
        '''

        # @Mstep [IF] if the database instance exists and correlate_to_table is True
        if self.database is not None and self.correlate_to_table is True:
            # @Mstep [] correlate this table's columns to the table's columns
            self._selects = self.database.correlate_to_table(
                self.table_name,
                self._selects,
                crud=self.crud_type
            )
            
        # @Mstep [IF] if the table instance exists.
        if self.table is not None:
            # @Mstep [IF] if the table has a deleted column
            if self.table.has_deleted_column is True:
                # @Mstep [IF] if the deleted column is not already used in the query.
                if self.deleted_where_used is False:
                    # @Mstep [IF] if the query should NOT include deleted columns
                    if self.include_deleted is False:
                        # @Mstep [] Add the deleted is null where clause.
                        self.add_where("deleted",None,"is")
            
        value = f"SELECT {self.select_string} FROM {self._schema_table_string}{self.where_string}"

        value = self._paginate_select_query(value)
        value = self._format_query_params(value,self._params)
        return value,self._params

    @property
    def deleted_where_used(self):
        '''
            Get this SelectQuery's deleted_where_used

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-14-2022 11:51:50
            `@memberOf`: SelectQuery
            `@property`: deleted_where_used
        '''
        value = self._deleted_where_used
        if value is None:
            value = False
            for where in self._wheres:
                if where['column_name'] == "deleted":
                    value = True
                    break
            self._deleted_where_used = value
        return value

    # @property
    # def where_string(self)->str:
    #     '''
    #         Get the compiled where clauses for this query.

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-09-2022 15:45:29
    #         `@memberOf`: SelectQuery
    #         `@property`: where_string
    #     '''
    #     # @Mstep [IF] if the table instance exists.
    #     if self.table is not None:
    #         # @Mstep [IF] if the table has a deleted column
    #         if self.table.has_deleted_column is True:
    #             # @Mstep [IF] if the deleted column is not already used in the query.
    #             if self.deleted_where_used is False:
    #                 # @Mstep [IF] if the query should NOT include deleted columns
    #                 if self.include_deleted is False:
    #                     # @Mstep [] Add the deleted is null where clause.
    #                     self.add_where("deleted",None,"is")



    #     value = self._wheres
    #     self._params = {}
    #     if len(self._wheres) > 0:
    #         wheres = []
    #         for where in self._wheres:
    #             if where['comparison'] in ["between"]:
    #                 min_key =f"{where['column_name']}_minimum"
    #                 max_key =f"{where['column_name']}_maximum"

    #                 single_where = f"{where['column_name']} {where['comparison'].upper()} :{min_key} AND :{max_key}"
    #                 self._params[min_key] = where['value']
    #                 self._params[max_key] = where['max_value']


    #             elif where['comparison'] in ["in"]:
    #                 in_list = []
    #                 for idx,val in enumerate(where['value']):
    #                     key = f"{where['column_name']}_{idx}"
    #                     self._params[key] = val
    #                     in_list.append(f":{key}")
    #                 in_list_string = ', '.join(in_list)
    #                 single_where = f"{where['column_name']} {where['comparison'].upper()} ({in_list_string})"



    #             elif where['comparison'] in ["is","is not"]:
    #                 single_where = f"{where['column_name']} {where['comparison'].upper()} {str(where['value'])}"
    #                 # params[where['column_name']] = where['value']
    #             else:
    #                 single_where = f"{where['column_name']} {where['comparison']} :{where['column_name']}"
    #                 self._params[where['column_name']] = where['value']

    #             wheres.append(single_where)
    #         wheres = ' AND '.join(wheres)
    #         value = f" WHERE {wheres}"
    #     else:
    #         value = ""
    #     return value

    @property
    def select_string(self)->str:
        '''
            Get the compiled select string for this query.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:56:15
            `@memberOf`: SelectQuery
            `@property`: select_string
        '''
        if len(self._selects) == 0:
            value = "*"
        else:
            selects = []
            for sel in self._selects:
                value = None
                if sel['alias'] is not None:
                    value = f"{sel['column_name']} as {sel['alias']}"
                else:
                    value = f"{sel['column_name']}"
                if value is not None:
                    selects.append(value)
            value = ', '.join(selects)
        if self.count is True:
            value = f"COUNT({value})"
        if self.average is True:
            value = f"AVG({value})"
        if self.sum_ is True:
            value = f"SUM({value})"
        return value


    # def add_where(self,column_name,value,comparison="="):
    #     '''
    #         Add a where clause to the query.

    #         ----------

    #         Arguments
    #         -------------------------
    #         `column_name` {str}
    #             The name of the column to compare.

    #         `value` {any}
    #             The value that the column should match.

    #             If the comparison is a "between", this should be a list or tuple with two values [min,max].

    #             If the comparison is an "in", this should be a list or tuple of values.

    #         [`comparison`="="] {str}
    #             The type of comparison to perform, defaults to "="

    #             Also supports:
    #             - between
    #             - in
    #             - is not
    #             - !=,<>,=,<,>,>=,<=

    #         Return {None}
    #         ----------------------
    #         nothing.

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 12-13-2022 11:55:02
    #         `memberOf`: SelectQuery
    #         `version`: 1.0
    #         `method_name`: add_where
    #         * @xxx [12-13-2022 12:04:13]: documentation for add_where
    #     '''

    #     if self.table is not None:
    #         if self.table.get_column_by_name(column_name) is None:
    #             _log(f"Column {column_name} does not exist in the table: {self.table.name}","warning")
    #             return

    #     if value is None:
    #         value = "NULL"

    #     if _csu.to_snake_case(comparison) in ["!","!=","isnt","isnot","is_not","<>"]:
    #         comparison = "is not"

    #     data = {
    #         "column_name":column_name,
    #         "comparison":comparison,
    #         "value":value,
    #         "max_value":None,
    #     }


    #     if _csu.to_snake_case(comparison) in ["between"]:
    #         if isinstance(value,(list,tuple)):
    #             data['value'] = value[0]
    #             data['max_value'] = value[1]
    #         else:
    #             data['value'] = 0
    #             data['max_value'] = value

    #     if _csu.to_snake_case(comparison) in ["in"]:
    #         value = _lu.force_list(value)
    #         if isinstance(value,(list,tuple)):
    #             items = []
    #             for idx,x in enumerate(value):
    #                 if isinstance(x,(str)):
    #                     # key = f"{column_name}_{idx}"
    #                     # items[key] = f"'{x}'"
    #                     items.append(x)


    #                 if isinstance(x,(int,float)):
    #                     # key = f"{column_name}_{idx}"
    #                     items.append(f"{x}")
    #                     # items[key] = f"{x}"

    #             # str_list = ', '.join(items)

    #             data['value'] = items

    #     self._wheres.append(data)

    def add_select(self,column_name,alias=None):
        '''
            Add a column to the selection of this query.

            By default "*" is used to select all columns if None are specified.
            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to select
            [`alias`=None] {str}
                An alias to use for this column

            Return {None}
            ----------------------
            returns nothing

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:04:31
            `memberOf`: SelectQuery
            `version`: 1.0
            `method_name`: add_select
            * @xxx [12-13-2022 12:06:00]: documentation for add_select
        '''
        if self.table is not None:
            if self.table.get_column_by_name(column_name) is None:
                _log(f"Column {column_name} does not exist in table: {self.table.name}","warning")
                return
        data = {
            "column_name":column_name,
            "alias":alias,
        }
        self._selects.append(data)

    @property
    def average(self):
        '''
            Get this SelectQuery's average

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 17:11:35
            `@memberOf`: SelectQuery
            `@property`: average
        '''
        value = self._average
        return value

    @average.setter
    def average(self,value):
        '''
            True if this query should return the average of rows selected

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 17:07:17
            `@memberOf`: SelectQuery
            `@property`: average
        '''
        if value is True:
            self._count = False
            self._sum_ = False
        self._average = True

    @property
    def sum_(self):
        '''
            Get this SelectQuery's sum

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 17:11:52
            `@memberOf`: SelectQuery
            `@property`: sum
        '''
        value = self._sum_
        return value

    @sum_.setter
    def sum_(self,value):
        '''
            True if this query should return the sum of rows selected

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 17:08:11
            `@memberOf`: SelectQuery
            `@property`: sum
        '''
        if value is True:
            self._count = False
            self._average = True
        self._sum_ = True

    @property
    def count(self):
        '''
            Get this SelectQuery's count

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 17:12:11
            `@memberOf`: SelectQuery
            `@property`: count
        '''
        value = self._count
        return value

    @count.setter
    def count(self,value):
        '''
            True if this query should return the count of rows selected

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 17:05:48
            `@memberOf`: SelectQuery
            `@property`: count
        '''
        if value is True:
            self._average = False
            self._sum_ = False
        self._count = value



if __name__ == '__main__':
    import time
    q = SelectQuery(
        table_name="blackholes",
        schema_name="boobs",
    )
    # q.add_where("expiration",(0,time.time()),"between")
    # q.add_where("expiration",time.time(),"<=")
    q.add_where("reason",["there","boobs"],"in")
    # q.add_select("hash_id")
    sql,args = q.query
    print(sql)
    print(args)

