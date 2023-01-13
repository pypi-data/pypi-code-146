
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import json
import re
from typing import Iterable
# import importlib
# from dataclasses import dataclass
# from posixpath import split
# from typing import List
# from typing import Iterable, Union



# import colemen_utilities.database_utils.MySQL.Column.Column as _Column
# from colemen_utilities.database_utils.MySQL.Column.Column import Column as _Column
# import colemen_utilities.dict_utils as _obj
import colemen_utilities.string_utils as _csu
# from colemen_utilities.database_utils.MySQL.Column import column_utils as _u
# from colemen_config import _db_column_type,_db_mysql_database_type
# from colemen_utilities.database_utils.MySQL import CacheFile as _CacheFile
# import colemen_utilities.database_utils.MySQL.CacheFile as _CacheFile
# import colemen_utilities.random_utils as _rand
import colemen_utilities.console_utils as _con
_log = _con.log
import inflect




class Name:
    def __init__(self,name:str=None):
        self.names = []
        '''A list of all variations of the name'''
        self.name = name
        '''The unmodified name'''
        self.private = f"_{name}"
        '''The name with a single leading underscore'''
        self.pascal = self.__Pascal(self,name)
        self.snake = self.__Snake(self,name)
        self.camel = self.__Camel(self,name)
        self.title = _csu.to_title_case(name)
        '''The name converted to title case'''
        self.singular:str = None
        '''The name converted to a singular'''
        _,self.singular,self.plural = gen_plurality(self.name)
        self.names.append(self.name)
        self.names.append(self.title)
        # self.names.append(self.pascal.name)
        # self.names.append(self.pascal.singular)
        # self.names.append(self.pascal.plural)
        # self.names.append(self.camel.name)
        # self.names.append(self.camel.singular)
        # self.names.append(self.camel.plural)
        # self.names.append(self.snake.name)
        # self.names.append(self.snake.singular)
        # self.names.append(self.snake.plural)
        # self.settings = {}
        # self.data = {}

    class __Camel:
        name:str = None
        '''The name converted to camel'''
        singular:str = None
        '''The camel name coerced to a singular'''
        plural:str = None
        '''The camel name coerced to a plural'''

        def __init__(self,main,name:str):
            self.main = main
            self.name = _csu.to_camel_case(name)
            self.name,self.singular,self.plural = gen_plurality(self.name)
            self.main.names.append(self.name)
            self.main.names.append(self.singular)
            self.main.names.append(self.plural)            

    class __Pascal:
        name:str = None
        '''The name converted to pascal'''
        singular:str = None
        '''The pascal name coerced to a singular'''
        plural:str = None
        '''The pascal name coerced to a plural'''

        def __init__(self,main,name:str):
            self.main = main
            self.name = _csu.to_pascal_case(name)
            self.name,self.singular,self.plural = gen_plurality(self.name)
            self.main.names.append(self.name)
            self.main.names.append(self.singular)
            self.main.names.append(self.plural)            

    class __Snake:
        name:str = None
        '''The name converted to snake'''

        singular:str = None
        '''The snake name coerced to a singular'''

        plural:str = None
        '''The snake name coerced to a plural'''

        def __init__(self,main,name:str):
            self.main = main
            self.name = _csu.to_snake_case(name)
            self.name,self.singular,self.plural = gen_plurality(self.name)
            self.main.names.append(self.name)
            self.main.names.append(self.singular)
            self.main.names.append(self.plural)

            self._misspellings:Iterable[str] = None


    @property
    def misspellings(self)->list:
        '''
            Get the misspellings value.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 16:31:05
            `@memberOf`: PostArg
            `@property`: misspellings
        '''
        if self._misspellings is not None:
            return self._misspellings
        value = _csu.variations(self.name.name,)
        return value

    @misspellings.setter
    def misspellings(self,value:str):
        '''
            Set the misspellings value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 16:31:05
            `@memberOf`: PostArg
            `@property`: misspellings
        '''
        self._misspellings = value



def gen_plurality(value):
    p = inflect.engine()
    value = _csu.strip(value," ")

    if "_" not in value:
        value = re.sub(r'([idID]{2})$',lambda x: x.group(1).upper(),value)

    singular = p.singular_noun(value)
    if singular is False:
        singular = value

    plural = p.plural_noun(value)
    if plural.endswith("seses"):
        plural = plural.replace("seses","ses")
    if plural.endswith("ieses"):
        plural = plural.replace("ieses","ies")
    if plural.endswith("eses"):
        plural = plural.replace("eses","es")

    if plural.endswith("ss"):
        plural = re.sub(r"ss$","s",plural,re.IGNORECASE)

    return (value,singular,plural)







