#
# Copyright (C) 2023 LLCZ00
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.  
#

"""
dynabyte.core

- Classes providing the core functionality of Dynabyte
"""

from dynabyte import utils


__all__ = ["Array", "File"]


class DynabyteBase:
    """Base class for dynabyte objects
    
    Provides bit-wise operations, and default buffersize and encoding class attributes
    """
    buffersize = 8192
    encoding="utf-8" # https://docs.python.org/3/library/codecs.html#standard-encodings
        
    def run(self, callback, *, output=None, count=1):
        """Execute operations defined in a callback function upon data. Gives access to offset.
        
        Must be overriden by subclass
        
        :param callback: Callback function: func(byte, offset) -> byte
        :param output: Output file path (optional)
        :type output: str
        :param count: Number of times to run array though callback function
        :type count: int
        """
        raise NotImplementedError
    
    def XOR(self, value=0, *, count=1):
        """XOR each byte of the current instance against 'value', 'count' times
        
        If value is anything other than int, data will be XOR'd against
        the value sequentially (like a key).
        
        :param value: Value to XOR array against (int, str, list, bytes, or bytearray)
        :param count: Number of times to XOR array against value
        :type count: int
        """
        key = utils.getbytearray(value)
        return self.run(callback=lambda x, y: x ^ key[y % len(key)], count=count)
        
    def __xor__(self, value):
        return self.XOR(value)
        
    def SUB(self, value=0, *, count=1):
        """Subtract 'value' from each byte of the current instance, 'count' times
         
        :param value: Value to subtract from each byte of array
        :type value: int
        :param count: Number of times to subtract value from array
        :type count: int
        """
        return self.run(callback=lambda x, y: x - value, count=count)
        
    def __sub__(self, value):
        return self.SUB(value)
        
    def ADD(self, value=0, *, count=1):
        """"Add 'value' to each byte of the current instance, 'count' times
        
        :param value: Value to add to each byte of array
        :type value: int
        :param count: Number of times to add value to array
        :type count: int
        """
        return self.run(callback=lambda x, y: x + value, count=count)
        
    def __add__(self, value):
        return self.ADD(value)
        
    def ROL(self, value=0, *, count=1):
        """Circular rotate shift left each byte of the current instance by 'value' bits, 'count' times
        
        :param value: Number of places to shift array
        :type value: int
        :param count: Number of times to run ROL
        :type count: int
        """
        return self.run(callback=lambda x, y: ((x << value % 8) & 255) | ((x & 255) >> (8 - (value % 8))), count=count)
        
    def __lshift__(self, value):
        return self.ROL(value)
        
    def ROR(self, value=0, *, count=1):
        """Circular rotate shift right each byte of the current instance by 'value' bits, 'count' times
        
        :param value: Number of places to shift array
        :type value: int
        :param count: Number of times to run ROR
        :type count: int
        """
        return self.run(callback=lambda x, y: ((x & 255) >> (value % 8)) | (x << (8 - (value % 8)) & 255), count=count)
        
    def __rshift__(self, value):
        return self.ROR(value)


class Array(DynabyteBase):
    """Dynabyte class for interacting with arrays
    
    For use with string/list/byte/bytearray objects
    """
    def __init__(self, data):
        if type(data) is type(self): # For accepting data from dynabyte.core.Array objects
            self.data = data.data
        else:
            self.data = utils.getbytearray(data)
    
    def __str__(self):
        return self.format(style="string")
        
    def format(self, style=None, delim= ", "):
        """Return string of instance's array data in given format.
        
        C-style array, Python list, delimited hex values,
        or string (default) formats.
        
        :param style: C, list, string, or None (hex bytes) array format
        :type style: str
        :param delim: Delimiter between hex values (Default: ', ')
        :type delim: str        
        :rtype: str 
        """       
        try:
            style = style.lower()
        except AttributeError:
            pass           
        array = delim.join(hex(byte) for byte in self.data)    
        if style == "c":
            array = f"unsigned char byte_array[] = {{ {array} }};"
        elif style == "list":
            array = f"byte_array = [{array}]"
        elif style == "string":
            array = self.data.decode(self.encoding, errors='ignore')
        return array
        
    def bytes(self):
        """Return bytes-object from instance's data
        """
        return bytes(self.data)
                
    def run(self, callback, *, output=None, count=1):
        """Execute operations defined in a callback function upon data. 
        
        Gives access to offset.
        
        :param callback: Callback function: func(byte, offset) -> byte
        :param output: Output file path (optional)
        :type output: str
        :param count: Number of times to run array though callback function
        :type count: int
        """
        for _ in range(count):
            self.data = DynabyteCallback(callback)(self.data)
        if output:
            with open(output, 'wb') as file:
                file.write(self.data)
        self.data = bytearray(self.data)
        return self
        

class File(DynabyteBase):
    """Dynabyte class for interacting with files"""
    def __init__(self, path):
        self.path = path
        
    def __str__(self):
        return self.path
        
    def getsize(self, verbose=False):
        """Return size of current instance file in bytes
        
        :param verbose: Print filesize message
        :type verbose: bool
        """
        size = os.stat(self.path).st_size
        if verbose:
            print(f"{os.path.basename(self.path)}: {size:,} bytes")
        return size

    def gethash(self, hash="sha256", verbose=False):
        """Return hash of current instance file
        
        :param hash: Hash type (Default: sha256)
        :type hash: str
        :param verbose: Print filesize message
        :type verbose: bool
        :rtype: str
        """
        hash_obj = hashlib.new(hash)
        try:
            with open(self.path, "rb") as reader:
                chunk = reader.read(8192)
                while chunk:
                    hash_obj.update(chunk)
                    chunk = reader.read(8192)
        except FileNotFoundError:
            if verbose:
                print(f"File not found: '{self.path}'")
            return None
            
        if verbose:
            print(f"{os.path.basename(self.path)} - {hash}: {hash_obj.hexdigest()}")
        return hash_obj.hexdigest()
        
    def delete(self):
        """Delete input file"""
        if os.path.exists(self.path):
            os.remove(self.path)
        
    def getfilebytes(self, buffer=-1):
        """Return all bytes from file in dynabyte Array
        
        Beware hella large files
        
        :param buffer: Number of bytes to read from file (Default: all)
        :type buffer: int
        :returns Array: Array object initialized with file bytes
        :rtype dynabyte.core.Array:
        """
        data = None
        try:
            with open(self.path, "rb") as fileobj:
                data = Array(file.read(buffer))
        except FileNotFoundError:
            pass
        return data 
        
    def run(
        self,
        callback: "Callback function: func(byte, offset) -> byte",
        *,
        output: "Optional output file path" = None,
        count: "Number of times to run array though callback function" = 1) -> object:
        """Execute operations defined in a callback function upon data within given file. 
        
        Gives access to offset, returns self, or instance created from output file
        
        :param callback: Callback function: func(byte, offset) -> byte
        :param output: Output file path (optional)
        :type output: str
        :param count: Number of times to run file though callback function
        :type count: int
        """       
        input = self.path # Running count > 1 and outputting a file at the same time breaks if I don't do this
        for _ in range(count):
            callback_function = DynabyteCallback(callback)
            with DynabyteFileManager(input, output, self.buffersize) as file_manager:
                for chunk in file_manager: 
                    file_manager.write(callback_function(chunk))
            if output:
                input = output # On the 2nd cycle it'll continue reading from the original (not up to date) file
                output = None
        return self
    

class DynabyteFileManager:
    """Context manager for file objects, can be iterated over to retrieve buffer of file bytes.
    
    Handles the input/output of one or two files.
    If no output path is given, the input will be overwritten
    """
    start_position = 0    
    def __init__(self, input: str, output: str, buffersize: int): 
        self.input_file = input
        self.output_file = output
        self.buffersize = buffersize
        self.last_position = self.start_position      

    def write(self, chunk: bytes) -> None:
        """Write bytes to file"""
        self.writer.seek(self.last_position)
        self.writer.write(chunk)

    def __enter__(self):
        if self.output_file is None:
            self.reader = self.writer = open(self.input_file, "rb+")  # reader/writer will use the same file handle if no output given
        else:
            self.reader = open(self.input_file, "rb")
            self.writer = open(self.output_file, "wb")
        return self

    def __exit__(self, type, val, traceback):
        self.reader.close()
        self.writer.close()
           
    def __iter__(self):
        return self

    def __next__(self) -> bytes:
        self.last_position = self.reader.tell() 
        chunk = self.reader.read(self.buffersize)
        if self.reader is None or chunk == b"":
            raise StopIteration
        else:
            return chunk


class DynabyteCallback:
    """Callback function handler, runs bytes through given function."""
    def __init__(self, function):
        self.callback = function
        self.global_offset = 0
        
    def __call__(self, chunk: bytes) -> bytes:
        """Returns bytes after being processed through callback function"""
        buffer = bytearray(len(chunk))
        for chunk_offset, byte in enumerate(chunk):
            buffer[chunk_offset] = (self.callback(byte, self.global_offset) & 0xff)
            self.global_offset += 1
        return bytes(buffer)
        

if __name__ == "__main__":
    pass
