





import datetime
import json
import os
import hashlib
# from typing import Union


from dataclasses import dataclass

from colemen_config import _db_column_type,_db_mysql_database_type

import colemen_utilities.dict_utils as _obj
import colemen_utilities.random_utils as _rand
import colemen_utilities.file_utils as _cfu
import colemen_utilities.directory_utils as _cdu
import colemen_utilities.console_utils as _con
_log = _con.log




@dataclass
class CacheFile:
    name:str = None
    '''The unique name to use for this cache file.'''

    # table_name:str = None
    # '''The name of the table that this susurrus represents'''

    # schema_name:str = None
    # '''The name of the schema that the table belongs to.'''

    cache_dir_path:str = f"{os.getcwd()}/cache"
    '''The file path to the cache directory.'''

    _cache_path:str = None
    '''The file path to this cache file.'''


    _file_name_deconstructed = None
    '''A dictionary of the parts of the file name'''

    _file_name:str = None
    '''The name of this cache file.'''
    _cache_failed_signature:bool = True

    # exists:bool = False
    # '''True if the cache file exists'''

    def __init__(self,database:_db_mysql_database_type,schema_name:str,table_name:str):
        self.database = database
        self.schema_name = schema_name
        self.table_name = table_name
        self.cache_dir_path = self.database.cache_path
        self._data = {}

    @property
    def data(self)->dict:
        '''
            Get the _data value.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 10:48:08
            `@memberOf`: PostArg
            `@property`: _data
        '''
        value = self._data
        return value

    @data.setter
    def data(self,value:dict):
        '''
            Set the _data value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 10:48:08
            `@memberOf`: PostArg
            `@property`: _data
        '''
        self._data = value

    def set_key(self,key,value):
        d = self.data
        if d is None:
            d = {}
        d[key] = value
        self.data = d

    def get_key(self,key,default=None,value_type=None):
        d = self.data
        if isinstance(d,(dict)) is False:
            return default

        result = _obj.get_arg(d,key,default,value_type)
        return result

    @property
    def exists(self):
        if _cfu.exists(self.cache_path) and self._cache_failed_signature is False:
            return True
        return False

    @property
    def file_name(self):
        '''
            Get this CacheFile's file_name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 10:10:08
            `@memberOf`: CacheFile
            `@property`: file_name
        '''
        if self._file_name is None:
            # datetime.datetime.today()
            date = datetime.datetime.today().strftime("%m%d%Y")
            # title = f"{self.schema_name}_{self.table_name}"
            hash_value = hashlib.md5(self.name.encode()).hexdigest()
            extension = ".json"
            self._file_name = f"{date}-{hash_value}{extension}"
            self._file_name_deconstructed = {
                "date":date,
                "hash_value":hash_value,
                "extension":extension
            }
        return self._file_name

    @property
    def name_date(self):
        '''
            Get this CacheFile's name_date

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 11:40:28
            `@memberOf`: CacheFile
            `@property`: name_date
        '''
        decon = self.file_name_deconstructed
        return decon['date']

    @property
    def name_hash(self):
        '''
            Get this CacheFile's name_hash

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 11:42:15
            `@memberOf`: CacheFile
            `@property`: name_hash
        '''
        decon = self.file_name_deconstructed
        return decon['hash_value']

    @property
    def extension(self):
        '''
            Get this CacheFile's extension

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 11:41:28
            `@memberOf`: CacheFile
            `@property`: extension
        '''
        decon = self.file_name_deconstructed
        return decon['extension']

    @property
    def file_name_deconstructed(self):
        '''
            Get this CacheFile's file_name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 10:10:08
            `@memberOf`: CacheFile
            `@property`: file_name
        '''
        value = self._file_name_deconstructed
        if value is None:
            file_name = self.file_name
            value = self._file_name_deconstructed
        return value

    @property
    def cache_path(self):
        '''
            Get the file_path to this cache file.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 10:08:14
            `@memberOf`: CacheFile
            `@property`: cache_path
        '''
        if self._cache_path is None:
            self._cache_path = f"{self.cache_dir_path}/{self.file_name}"
        return self._cache_path



    def load(self)->dict:
        '''
            Load this cache file.
            
            ----------

            Return {None,dict}
            ----------------------
            The contents of the cache file if it exists and it's signature is validated.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-05-2022 10:24:56
            `memberOf`: CacheFile
            `version`: 1.0
            `method_name`: load
            * @xxx [12-12-2022 09:01:00]: documentation for load
        '''
        result = None
        # @Mstep [IF] if the cache directory does not exist.
        if _cdu.exists(self.cache_dir_path) is False:
            # _log("Creating Susurrus Cache Directory")
            # @Mstep [] create the cache directory.
            _cdu.create(self.cache_dir_path)

        # @Mstep [] randomly purge the cache directory of old files.
        if _rand.boolean(2):
            purge_cache_files(self)
        # self.cache_path = f"{self.cache_dir_path}/{self.schema_name}_{self.table_name}.cache"
        if _cfu.exists(self.cache_path):
            _log(f"{self.name} cache file exists.","magenta")
            contents = _cfu.read.as_json(self.cache_path)
            # @Mstep [IF] if the cache file was successfully read as JSON.
            if isinstance(contents,(dict)):
                # @Mstep [IF] if the signature matches the newly generated one.
                if contents['signature'] != gen_signature(contents['cache_data']):
                    _log("Failed signature validation.","warning")
                # @Mstep [ELSE] if the signatures match.
                else:
                    self._cache_failed_signature = False
                    _log(f"Successfully loaded cache file:  {self.name}  from  {self.cache_path}","success")
                    self.data = contents['cache_data']
                    # @Mstep [] set this CacheFile's data to be the contents of the cache_data key.
                    result = self.data

        else:
            _log(f"{self.name} cache file does NOT exist.","magenta")

        return result

    def save(self):

        contents = {
            "signature":gen_signature(self._data),
            "cache_data":self._data,
        }
        _cfu.writer.to_json(self.cache_path,contents)
        _log(f"Saving cache: {self.name}  -  {self.cache_path}","green")
    # def validate(self,data):


def gen_signature(value):
    salt = "n56sgZmRrM4jK8lSzqabJ97ETSmbZqdf18u9"
    value = f"{salt}{json.dumps(value)}"
    signature = hashlib.md5(value.encode()).hexdigest()
    return signature

def purge_cache_files(cache:CacheFile,include_current=True):
    cache_path = cache.cache_dir_path
    files = _cfu.get_files(cache_path,extension=[cache.extension])
    # @Mstep [LOOP] iterate the files.
    for file in files:
        # @Mstep [IF] if the file_name contains the cache files hash.
        if cache.name_hash in file['file_name']:
            # @Mstep [IF] if the file has the current date
            if cache.name_date in file['file_name'] and include_current is False:
                # @Mstep [] skip deletion of this file.
                continue
            _log(f"purging cache file: {file['file_path']}")
            # @Mstep [] delet the file.
            _cfu.delete(file['file_path'])

