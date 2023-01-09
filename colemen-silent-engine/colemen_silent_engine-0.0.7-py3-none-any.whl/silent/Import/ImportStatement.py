# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import



import ast
from dataclasses import dataclass
from string import Template
from typing import Iterable, Union
import silent.EntityBase as _eb

import colemen_utils as c

# from silent.EntityBase import EntityBase as _eb
# import agod.TypeDeclaration as _type_dec
# from config import column_type,_relationship_type,endpointdoc_type,route_type,root_directory,susurrus_type
import silent.se_config as config
log = c.con.log

_STANDARD_LIBRARY_NAMES =["string","re","difflib","textwrap","unicodedata","stringprep","readline","rlcompleter","struct","codecs","datetime","zoneinfo","calendar","collections","collections.abc","heapq","bisect","array","weakref","types","copy","pprint","reprlib","enum","graphlib","numbers","math","cmath","decimal","fractions","random","statistics","itertools","functools","operator","pathlib","os.path","fileinput","stat","filecmp","tempfile","glob","fnmatch","linecache","shutil","pickle","copyreg","shelve","marshal","dbm","sqlite3","zlib","gzip","bz2","lzma","zipfile","tarfile","csv","configparser","tomllib","netrc","plistlib","hashlib","hmac","secrets","os","io","time","argparse","getopt","logging","logging.config","logging.handlers","getpass","curses","curses.textpad","curses.ascii","curses.panel","platform","errno","ctypes","threading","multiprocessing","multiprocessing.shared_memory","concurrent.futures","subprocess","sched","queue","contextvars","_thread","asyncio","socket","ssl","select","selectors","signal","mmap","email","json","mailbox","mimetypes","base64","binascii","quopri","html","html.parser","html.entities","xml.etree.ElementTree","xml.dom","xml.dom.minidom","xml.dom.pulldom","xml.sax","xml.sax.handler","xml.sax.saxutils","xml.sax.xmlreader","xml.parsers.expat","webbrowser","wsgiref","urllib","urllib.request","urllib.response","urllib.parse","urllib.error","urllib.robotparser","http","http.client","ftplib","poplib","imaplib","smtplib","uuid","socketserver","http.server","http.cookies","http.cookiejar","xmlrpc","xmlrpc.client","xmlrpc.server","ipaddress","wave","colorsys","gettext","locale","turtle","cmd","shlex","tkinter","tkinter.colorchooser","tkinter.font","tkinter.messagebox","tkinter.scrolledtext","tkinter.dnd","tkinter.ttk","tkinter.tix","typing","pydoc","doctest","unittest","unittest.mock","unittest.mock","2to3","test","test.support","test.support.socket_helper","test.support.script_helper","test.support.bytecode_helper","test.support.threading_helper","test.support.os_helper","test.support.import_helper","test.support.warnings_helper","bdb","faulthandler","pdb","timeit","trace","tracemalloc","distutils","ensurepip","venv","zipapp","sys","sysconfig","builtins","__main__","warnings","dataclasses","contextlib","abc","atexit","traceback","__future__","gc","inspect","site","code","codeop","zipimport","pkgutil","modulefinder","runpy","importlib","ast","symtable","token","keyword","tokenize","tabnanny","pyclbr","py_compile","compileall","dis","pickletools","msvcrt","winreg","winsound","posix","pwd","grp","termios","tty","pty","fcntl","resource","syslog","aifc","asynchat","asyncore","audioop","cgi","cgitb","chunk","crypt","imghdr","imp","mailcap","msilib","nis","nntplib","optparse","ossaudiodev","pipes","smtpd","sndhdr","spwd","sunau","telnetlib","uu","xdrlib"]

@dataclass
class ImportStatement(_eb.EntityBase):

    import_path:str = None
    '''The import path'''

    alias:str = None
    '''The alias to use for this import'''

    _subjects:Iterable[str] = None
    '''The named subjects to be imported'''

    is_standard_library:bool = False
    '''True if this is importing from the python standard library'''

    is_third_party:bool = False
    '''True if this is importing from a third party library'''



    def __init__(self,**kwargs) -> None:
        '''
            Represents an import statement.

            ----------

            Keyword Arguments
            ----------
            [`import_path`=None] {str}
                The import path where the imported value is located.

            [`alias`=None] {str}
                The alias to use for this import

            [`subjects`=None] {list,str}
                The subject or list of subjects to import

            [`is_standard_library`=False] {bool}
                True if this import is from the python standard library.

            [`is_third_party`=False] {bool}
                True if this is importing from a third party library.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-26-2022 08:35:16
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: Table
            * @xxx [12-26-2022 08:36:08]: documentation for Table
        '''
        super().__init__(**kwargs)
        self._subjects = []









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
        value = {
            "subjects":self.subjects,
            "import_path":self.import_path,
            "alias":self.alias,
            "is_standard_library":self.is_standard_library,
            "is_third_party":self.is_third_party,
            # "schema":self.table.database.database,
        }

        return value

    def add_subject(self,name):
        '''
            Add a subject to import.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:11:34
            `@memberOf`: ImportStatement
            `@property`: add_subject
        '''
        self._subjects.append(name)
        self._subjects = c.arr.remove_duplicates(self.subjects)

    @property
    def subjects(self)->Iterable[str]:
        '''
            Get this ImportStatement's subjects

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 10:52:48
            `@memberOf`: ImportStatement
            `@property`: subjects
        '''
        value = list(self._subjects)
        return value

    @subjects.setter
    def subjects(self,value:Union[str,list]):
        '''
            Set the ImportStatement's subjects property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 10:55:27
            `@memberOf`: ImportStatement
            `@property`: subjects
        '''
        self._subjects = []
        if isinstance(value,(str)):
            value = value.split(",")
        value = c.arr.force_list(value)
        self._subjects = value

    # @property
    # def _subject_names(self):
    #     '''
    #         Get this ImportStatement's _subject_names

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 10:08:17
    #         `@memberOf`: ImportStatement
    #         `@property`: _subject_names
    #     '''
    #     subjects = c.arr.force_list(self.subjects)
    #     value = ""
    #     if len(subjects) > 0:
    #         value = ','.join(subjects)
    #     return value

    # @property
    # def _alias(self):
    #     '''
    #         Get this ImportStatement's _alias

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 10:10:10
    #         `@memberOf`: ImportStatement
    #         `@property`: _alias
    #     '''
    #     value = ""
    #     if len(self.subjects) == 1:
    #         value = f"as {self.alias}"
    #     return value

    def __gen_ast_names(self):
        output = []
        for name in self.subjects:
            alias = ast.alias(name=name)
            if self.alias is not None:
                alias.asname=self.alias
            output.append(alias)
            # print(ast.dump(alias,indent=4))
        return output

    @property
    def ast(self)->Union[ast.Import,ast.ImportFrom]:
        '''
            Get this ImportStatement's ast object.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 10:57:49
            `@memberOf`: ImportStatement
            `@property`: ast
        '''
        imp = None
        if self.import_path is not None:
            imp = ast.ImportFrom()
            imp.module=self.import_path
            imp.level=0
            imp.names = self.__gen_ast_names()
        else:
            imp = ast.Import()
            imp.names = self.__gen_ast_names()
        imp = ast.fix_missing_locations(imp)
        return imp

    @property
    def result(self):
        '''
            Get the python source code of this import statement.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 09:17:47
            `@memberOf`: Property
            `@property`: declaration
        '''
        # imp = None
        # if self.import_path is not None:
        #     imp = ast.ImportFrom()
        #     imp.module=self.import_path
        #     imp.level=0
        #     imp.names = self.__gen_ast_names()
        # else:
        #     imp = ast.Import()
        #     imp.names = self.__gen_ast_names()
        # imp = ast.fix_missing_locations(imp)
        # # print(ast.dump(imp,indent=4))
        return ast.unparse(self.ast)

