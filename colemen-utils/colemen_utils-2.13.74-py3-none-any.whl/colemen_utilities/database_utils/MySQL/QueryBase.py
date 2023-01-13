# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    Used as the base for generating an SQL query to execute on a database.

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
from colemen_config import _db_mysql_database_type,_db_table_type
import colemen_utilities.dict_utils as _obj
# import colemen_utilities.file_utils as _cfu
# import colemen_utilities.directory_utils as _dirs
import colemen_utilities.string_utils as _csu
import colemen_utilities.list_utils as _lu


# import colemen_utilities.database_utils.TableManager as _table_manager

# import colemen_utilities.database_utils.TableManager as _table_manager

# import colemen_utilities.database_utils as _cdb
# _TableManager = _cdb.TableManager
import colemen_utilities.console_utils as _con
_log = _con.log


@dataclass
class QueryBase:

    table_name:str = None
    '''The name of the table this query will execute on.'''

    table:_db_table_type = None
    '''The table instance this query is related to.'''

    schema_name:str = None
    '''The name of the schema/database that the table belongs to.'''

    database:_db_mysql_database_type = None
    '''The schema/database instance'''

    # limit:int = None
    # offset:int = None
    # statement:str = None
    # args = None
    crud_type:str = None
    '''The CRUD operation that this query performs'''
    correlate_to_table:bool = True
    '''If True the data will be filtered by the columns in the table.'''


    _quote_char:str = "`"
    '''The character used for quotations in the query.'''
    
    _wheres = None
    '''A list of where clause dictionaries.'''

    def __init__(self,**kwargs):
        self._wheres = []
        # @Mstep [LOOP] iterate the keyword arguments.
        for k,v in kwargs.items():
            # @Mstep [IF] if the key matches a property on this instance.
            if hasattr(self,k):
                # @Mstep [] set the value to the property.
                setattr(self,k,v)

        # @Mstep [IF] if the database instance was provided.
        if self.database is not None:
            self.schema_name = self.database.database
            self.limit = self.database.get_limit

            # @Mstep [IF] if the table name is provided.
            if self.table is None and self.table_name is not None:
                # @Mstep [] search for the table instance by its name.
                self.table = self.database.get_table(self.table_name)
            # @Mstep [IF] if the table name is not provided
            if self.table is not None and self.table_name is None:
                # @Mstep [] get the table_name from the table instance.
                self.table_name = self.table.name


    @property
    def _schema_table_string(self):
        '''
            The name of the table used in the query.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 10:47:15
            `@memberOf`: Query
            `@property`: __schema_table_string
        '''
        q = self.quote_char
        value = f"{q}{self.table_name}{q}"
        if self.schema_name is not None:
            value = f"{q}{self.schema_name}{q}.{value}"
        return value

    @property
    def quote_char(self)->str:
        '''
            The character used for quotation in the query.

            `default`:"`"


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-14-2022 10:42:47
            `@memberOf`: PostArg
            `@property`: quote_char
        '''
        value = self._quote_char
        return value

    @quote_char.setter
    def quote_char(self,value:str):
        '''
            Set the quote_char value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-14-2022 10:42:47
            `@memberOf`: PostArg
            `@property`: quote_char
        '''
        valid_chars =["`","'",'"']
        if value not in valid_chars:
            _log(f"Invalid Quote character: {value}. Allowed Values: [{''.join(valid_chars)}]","warning")
            value = "`"
        self._quote_char = value

    def add_where_from_where(self,**kwargs):
        column_name = _obj.get_kwarg(["column_name"],None,(str),**kwargs)
        value = _obj.get_kwarg(["value"],None,None,**kwargs)
        max_value = _obj.get_kwarg(["max_value"],None,None,**kwargs)
        comparison = _obj.get_kwarg(["comparison"],None,None,**kwargs)

        if max_value is not None:
            value = [value,max_value]
            
        self.add_where(column_name,value,comparison)
        
        
        
    def add_where(self,column_name,value,comparison="="):

    

        if self.table is not None and self.correlate_to_table is True:
            col = self.table.get_column_by_name(column_name)
            if col is None:
                _log(f"Column {column_name} does not exist in table: {self.table.name}","warning")
                return

            else:
                # @Mstep [IF] if the column is the primary key of the table
                if col.data.is_primary is True:
                    # @Mstep [IF] if the value is a string and the table has a hash_id column
                    if isinstance(value,(int)) is False and self.table.has_hash_id:
                        if self.table.hash_id_prefix not in value:
                            value = f"{self.table.hash_id_prefix}_{value}"
                        # @Mstep [] set the column to be the hash_id column instead.
                        column_name = "hash_id"
                        col = self.table.get_column_by_name("hash_id")
                    else:
                        return
                # @Mstep [] correlate the value to the column
                result = self.database.correlate_single_column(col,value)
                if isinstance(result,(dict)):
                    value = result[col.data.column_name]

        
        if value is None:
            value = "NULL"

        if _csu.to_snake_case(comparison) in ["!","!=","isnt","isnot","is_not","<>"]:
            comparison = "is not"

        data = {
            "column_name":column_name,
            "comparison":comparison,
            "value":value,
            "max_value":None,
        }
        if _csu.to_snake_case(comparison) in ["between"]:
            if isinstance(value,(list,tuple)):
                data['value'] = value[0]
                data['max_value'] = value[1]
            else:
                data['value'] = 0
                data['max_value'] = value

        if _csu.to_snake_case(comparison) in ["in"]:
            value = _lu.force_list(value)
            if isinstance(value,(list,tuple)):
                items = []
                for idx,x in enumerate(value):
                    if isinstance(x,(str)):
                        # key = f"{column_name}_{idx}"
                        # items[key] = f"'{x}'"
                        items.append(x)


                    if isinstance(x,(int,float)):
                        # key = f"{column_name}_{idx}"
                        items.append(f"{x}")
                        # items[key] = f"{x}"

                # str_list = ', '.join(items)

                data['value'] = items

        self._wheres.append(data)

    @property
    def where_string(self):
        '''
            Get this UpdateQuery's where_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:45:29
            `@memberOf`: UpdateQuery
            `@property`: where_string
        '''
        value = self._wheres
        # self._params = {}
        if len(self._wheres) > 0:
            wheres = []
            for where in self._wheres:
                if where['comparison'] in ["between"]:
                    min_key =f"{where['column_name']}_minimum"
                    max_key =f"{where['column_name']}_maximum"

                    single_where = f"{where['column_name']} {where['comparison'].upper()} :{min_key} AND :{max_key}"
                    self._params[min_key] = where['value']
                    self._params[max_key] = where['max_value']


                elif where['comparison'] in ["in"]:
                    in_list = []
                    for idx,val in enumerate(where['value']):
                        key = f"{where['column_name']}_{idx}"
                        self._params[key] = val
                        in_list.append(f":{key}")
                    in_list_string = ', '.join(in_list)
                    single_where = f"{where['column_name']} {where['comparison'].upper()} ({in_list_string})"



                elif where['comparison'] in ["is","is not"]:
                    single_where = f"{where['column_name']} {where['comparison'].upper()} {str(where['value'])}"
                    # params[where['column_name']] = where['value']
                else:
                    single_where = f"{where['column_name']} {where['comparison']} :{where['column_name']}"
                    self._params[where['column_name']] = where['value']
                wheres.append(single_where)
            wheres = ' AND '.join(wheres)
            value = f" WHERE {wheres}"
        else:
            value = ""
        return value





    def _format_query_params(self,sql:str,args:dict)->str:
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
        return _format_query_params(sql,args)

    def _paginate_select_query(self,sql)->str:
        '''
            Apply a limit and offset value to a select query statement.


            Arguments
            -------------------------
            `sql` {str}
                The sql statement to modify

            Return {str}
            ----------------------
            The sql statement with a limit and offset value applied.

            If the limit/offset if invalid no pagination is added.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-14-2022 11:45:47
            `memberOf`: QueryBase
            `version`: 1.0
            `method_name`: __paginate_select_query
            * @xxx [12-14-2022 11:46:12]: documentation for __paginate_select_query
        '''
        return _paginate_select_query(sql,self.limit,self.offset)



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
























