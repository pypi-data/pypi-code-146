# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
# '''
#     Contains the general methods for manipulating files.

#     ----------

#     Meta
#     ----------
#     `author`: Colemen Atwood
#     `created`: 06-03-2022 10:22:15
#     `memberOf`: rand
#     `version`: 1.0
#     `method_name`: rand
# '''




import json
# import shutil
# import time
# import json
# import re
# from pathlib import Path
import time as _time
import json as _json
from datetime import timezone as _timezone
from datetime import datetime as _datetime
import gzip as _gzip
# import zipfile
import os as _os
import io as _io
import shutil as _shutil
import traceback as _traceback
from threading import Thread as _Thread
import logging as _logging
from pathlib import Path, PureWindowsPath

from isort import file

# import ftputil as _ftputil
# from secure_delete import secure_delete as _secure_delete
# import patoolib
# import colemen_string_utils as strUtils
# import colemen_utilities.files.dir as directory
# import _f.resources
# import colemen_utilities.files.dir as dirUtils
# from colemen_utilities.files.dir import create as create_dir
# import colemen_utilities.object_utils as obj
# import colemen_utilities.files.file_read as read
# import colemen_utilities.files.file_write as write
# import colemen_utilities.files.file_search as search
# import colemen_utilities.files.file_convert as convert
# import colemen_utilities.files.file_image as image
# import colemen_utilities.files.file_compression as compression
# import colemen_utilities.files.exiftool as exiftool
# from colemen_utilities.files.dir import get_folders_ftp
# import colemen_utilities.files.string_utils as strUtils

import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj
import colemen_utilities.file_utils as _f
import colemen_utilities.directory_utils as _directory

# from colemen_utilities.string_utils.string_format import array_in_string as _csu.array_in_string
# from colemen_utilities.string_utils.string_format import file_path as _csu.file_path
# from colemen_utilities.string_utils.string_format import extension as _csu.extension
# from colemen_utilities.string_utils.string_generation import variations as _csu.variations
# from colemen_utilities.string_utils.string_generation import to_hash as _csu.to_hash
# from colemen_utilities.dict_utils.dict_utils import get_kwarg as _obj.get_kwarg


logger = _logging.getLogger(__name__)






class File():
    def __init__(self,file_path,args:dict=None):
        self.args = {} if args is None else args
        self.data = {
            "file_path":file_path,
            "file_name":None,
            "extension":None,
            "name_no_ext":None,
            "dir_path":None,
            "access_time":None,
            "modified_time":None,
            "created_time":None,
            "size":None,
            "is_json":None,
        }
        self.settings = {}
        self.data = _obj.set_defaults(self.data,self.args)

    @property
    def to_dict(self):
        '''
            Get this File's data as a dictionary.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:48:25
            `@memberOf`: File
            `@property`: to_dict
        '''
        data = {
            "file_path":self.file_path,
            "name":self.name,
            "extension":self.extension,
            "name_no_ext":self.name_no_ext,
            "dir_path":self.dir_path,
            "access_time":self.access_time,
            "modified_time":self.modified_time,
            "created_time":self.created_time,
            "drive":self.drive,
            "size":self.size,
        }
        return data

    @property
    def file_path(self):
        '''
            Get this File's file_path

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:37:48
            `@memberOf`: File
            `@property`: file_path
        '''
        path = _obj.get_arg(self.data,['file_path'],None,(str))
        if isinstance(path,(str)):
            path = str(PureWindowsPath(Path(path)))
        return path
    path = file_path

    @property
    def name(self):
        '''
            Get this File's name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:37:33
            `@memberOf`: File
            `@property`: name
        '''
        value = _obj.get_arg(self.data,['name'],None,(str))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _os.path.basename(self.file_path)
            self.data['name'] = value
        return value
    file_name = name

    @property
    def extension(self):
        '''
            Get this File's extension

            `default`:None

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:41:26
            `@memberOf`: File
            `@property`: extension
        '''
        value = _obj.get_arg(self.data,['extension'],None,(str))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _f.get_ext(self.file_path)
            if isinstance(value,(str)):
                self.data['extension'] = value
        return value
    ext = extension

    @extension.setter
    def extension(self,value):
        '''
            Set the File's extension property

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-15-2022 09:40:40
            `@memberOf`: File
            `@property`: extension
        '''
        value = _csu.format_extension(value)
        self.data['extension'] = f".{value}"
    
    @property
    def name_no_ext(self):
        '''
            Get this File's name_no_ext

            `default`:""


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:43:19
            `@memberOf`: File
            `@property`: name_no_ext
        '''
        value = _obj.get_arg(self.data,['name_no_ext'],None,(str))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _f.get_name_no_ext(self.file_path)
            self.data['name_no_ext'] = value
        return value

    @property
    def dir_path(self):
        '''
            Get this File's dir_path

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:44:32
            `@memberOf`: File
            `@property`: dir_path
        '''
        value = _obj.get_arg(self.data,['dir_path'],None,(str))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _os.path.dirname(self.file_path)
            self.data['dir_path'] = value
        return value

    @property
    def access_time(self):
        '''
            Get this File's access_time

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:44:58
            `@memberOf`: File
            `@property`: access_time
        '''
        value = _obj.get_arg(self.data,['access_time'],None,(int))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _f.get_access_time(self.file_path)
            self.data['access_time'] = value
        return value

    @property
    def created_time(self):
        '''
            Get this File's created_time

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:45:32
            `@memberOf`: File
            `@property`: created_time
        '''
        value = _obj.get_arg(self.data,['created_time'],None,(int))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _f.get_create_time(self.file_path)
            self.data['created_time'] = value
        return value

    @property
    def modified_time(self):
        '''
            Get this File's modified_time

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:46:25
            `@memberOf`: File
            `@property`: modified_time
        '''
        value = _obj.get_arg(self.data,['modified_time'],None,(int))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _f.get_modified_time(self.file_path)
            self.data['modified_time'] = value
        return value

    @property
    def drive(self):
        '''
            Get this File's drive

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:47:02
            `@memberOf`: File
            `@property`: drive
        '''
        value = _obj.get_arg(self.data,['drive'],None,(str))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _f.get_drive(self.file_path)
            self.data['drive'] = value
        return value

    @property
    def size(self):
        '''
            Get this File's size

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:47:34
            `@memberOf`: File
            `@property`: size
        '''
        value = _obj.get_arg(self.data,['size'],None,(int))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _os.path.getsize(self.file_path)
            self.data['size'] = value
        return value

    @property
    def exists(self):
        '''
            Check if this file actually exists.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-15-2022 09:05:54
            `@memberOf`: File
            `@property`: exists
        '''
        value = _obj.get_arg(self.data,['exists'],None,(bool))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = _f.exists(self.file_path)
            self.data['exists'] = value
        return value

    @property
    def _is_json(self):
        '''
            Get this File's _is_json

            If the is_json argument was not provided, this will check the file extension.

            If the extension is not json or jsonc, it will return False.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-15-2022 09:37:53
            `@memberOf`: File
            `@property`: _is_json
        '''
        value = _obj.get_arg(self.data,['is_json'],None,(bool))
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = False
            if self.extension in ['.json','.jsonc']:
                value = True
            if self.content is not None:
                result = _f.as_json(self.content)
                if result is not False:
                    value = True
                    self.content = result
            self.data['_is_json'] = value
        return value

    @property
    def content(self):
        '''
            Get this File's content

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-15-2022 09:27:31
            `@memberOf`: File
            `@property`: content
        '''
        value = _obj.get_arg(self.data,['content'],None)
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = None
            if self.exists is True:
                value = _f.readr(self.path)
            self.data['content'] = value
        return value

    def content_to_string(self,value):
        value = self.content
        if isinstance(value,(str)) is True:
            return value
        if isinstance(value,(dict,list)):
            # TODO []: add error catching.
            value = json.encode(value)
            return value

    @content.setter
    def content(self,value='',save=True):
        '''
            Set the File's contents property

            `default`:''


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-15-2022 09:33:56
            `@memberOf`: File
            `@property`: contents
        '''
        self.data['content'] = value
        if save == True:
            _f.write(self.path,self.content)

    # def write(self,content):
    #     self.data['content'] = 


    def save(self):
        _f.write(self.path,self.contents)

    def append(self,new_contents):
        _f.append(self.path,new_contents)
        # @Mstep [IF] if the contents have already been read.
        if self.content is not None:
            # @Mstep [] set the contents to None
            self.data['content'] = None
            # @Mstep [] read the file again.
            _ = self.content

def file_from_path(file_path,**kwargs):
    
    args = {
        "is_json":_obj.get_kwarg(['is_json','json'],None,(bool),**kwargs),
    }
    return File(file_path,args)



