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
dynabyte.utils

- Dynabytes utility/helper functions. 
- Also useful for general file IO.
"""

import os


def RotateLeft(x, n):
    """Circular rotate shift x left by n bits"""
    return ((x << n % 8) & 255) | ((x & 255) >> (8 - (n % 8)))


def RotateRight(x, n):
    """Circular rotate shift x right by n bits"""
    return ((x & 255) >> (n % 8)) | (x << (8 - (n % 8)) & 255)
    

def getbytearray(data):
    """Return bytearray from string, list, bytes, or int objects
    
    :rtype: bytearray
    """
    if type(data) is type(None):
        return ""
    elif type(data) is str:
        return bytearray([ord(c) for c in data])    
    elif type(data) is list or type(data) is bytes:
        return bytearray(data)
    elif type(data) is int:
        return bytearray([data])
    elif type(data) is bytearray:
        return data
    else:
        raise TypeError(data)
        

def bprint(data, style=None, delim=", "):
    """Print given bytes in given format
    
    Default: Comma-deliminated hex representation
    
    :param data: bytes or bytearray object
    :param style: C, Python, string, or None (hex bytes) array format
    :type style: str
    :param delim: Delimiter between hex values (Default: ', ')
    :type delim: str
    :rtype: None 
    """
    try:
        style = style.lower()
    except AttributeError:
        pass           
    array = delim.join(hex(byte) for byte in data)    
    if style == "c":
        array = f"unsigned char byte_array[] = {{ {array} }};"
    elif style == "list":
        array = f"byte_array = [{array}]"
    elif style == "string":
        try:
            array = self.data.decode()
        except:
            pass        
    print(array)
    

def comparefilebytes(path1, path2, verbose=True):
    """Compare the bytes of the two given files.
    
    :param path1: Path to file
    :type path1: str
    :param path2: Path to second file
    :type path2: str
    :param verbose: Print filesize message
    :type verbose: bool
    :rtype: bool
    """
    name1 = os.path.basename(path1)
    name2 = os.path.basename(path2)
    deviants = []
    offset = 0
    with open(path1, "rb") as file1, open(path2, "rb") as file2:
        chunk1 = file1.read(8192)
        chunk2 = file2.read(8192)
        while chunk1 and chunk2:
            for byte1, byte2 in zip(chunk1, chunk2):
                if byte1 != byte2:
                    deviants.append(f"Offset {hex(offset)}: {hex(byte1)} -> {hex(byte2)}")
                offset += 1
            chunk1 = file1.read(8192)
            chunk2 = file2.read(8192)
    if deviants:
        if verbose:
            print(f"{len(deviants)} errors found.")
        return deviants
    if verbose:
        print(f"No discrepancies found between {name1} and {name2}")
    return None



if __name__ == "__main__":
    pass
