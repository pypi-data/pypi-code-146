from .util import Console
import os
from typing import Any

class File:

    _filePath = ''
    result: Any = None

    def __init__(self, filePath):
        # figure out what type of file this is

        filename, file_extension = os.path.splitext(filePath)

        do = f"_ext_{file_extension[1:]}"
  
        if hasattr(self, do) and callable(func := getattr(self, do)):
            self._filePath = self._buildFilePath(filePath)
            self.result = func()



    def _ext_json(self):
        Console.info(f'Loading json data from "{self._filePath}"')
        import json

        result = {}
        try:
            data = open(self._filePath)
            result = json.load(data)
            
            Console.ok('File opened and parsed')
        except:
            Console.error('Error when opening file')
       
        return result

    def _buildFilePath(self, filePath):
        # we take the file path passed in and do some checks to make sure it will work

        filePath = filePath.replace('/', os.path.sep)
        filePath = filePath.replace('\\', os.path.sep)

        return filePath