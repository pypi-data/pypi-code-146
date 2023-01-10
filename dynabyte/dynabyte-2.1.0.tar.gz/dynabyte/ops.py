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
dynabyte.ops

- Bit-wise operations that can be used independently
    of dynabyte objects
"""
import os
import hashlib
from dynabyte import utils

def ROL(data, value=0, *, count=1):
    """Circular rotate shift 'data' left by 'value' bits
    
    :param data: Data to perform operation on (str, list, bytes, bytearray, int)
    :param value: Number of bits to rotate
    :type value: int
    :param count: Number of times to perform function
    :type count: int
    :rtype: bytes
    """
    data = utils.getbytearray(data)
    for _ in range(count):
        for offset, byte in enumerate(data):
            data[offset] = ((((byte << value % 8) & 255) | ((byte & 255) >> (8 - (value % 8)))) & 0xff)        
    return bytes(data)


def ROR(data, value=0, *, count=1):
    """Circular rotate shift 'data' right by 'value' bits
    
    :param data: Data to perform operation on (str, list, bytes, bytearray, int)
    :param value: Number of bits to rotate
    :type value: int
    :param count: Number of times to perform function
    :type count: int
    :rtype: bytes
    """
    data = utils.getbytearray(data)
    for _ in range(count):
        for offset, byte in enumerate(data):
            data[offset] = ((((byte & 255) >> (value % 8)) | (byte << (8 - (value % 8)) & 255)) & 0xff)        
    return bytes(data)
    

def XOR(data, value=0, *, count=1):
    """XOR 'data' against 'value', 'count' times
    
    If value is anything other than int, data will be XOR'd against
    the value sequentially (like a key).
     
    :param data: Data to perform operation on (str, list, bytes, bytearray, int)
    :param value: Value to XOR array against (str, list, bytes, bytearray, int)
    :param count: Number of times to perform function
    :type count: int
    :rtype: bytes
    """
    data = utils.getbytearray(data)
    value = utils.getbytearray(value)
    for _ in range(count):
        for offset, byte in enumerate(data):
            data[offset] = ((byte ^ value[offset % len(value)]) & 0xff)
    return bytes(data)


def SUB(data, value=0, *, count=1):
    """Subtract 'value' from each byte in 'data', 'count' times
     
    :param data: Data to perform operation on (str, list, bytes, bytearray, int)
    :param value: Value to subtract
    :type value: int
    :param count: Number of times to perform function
    :type count: int
    :rtype: bytes
    """
    data = utils.getbytearray(data)
    for _ in range(count):
        for offset, byte in enumerate(data):
            data[offset] = ((byte - value) & 0xff)
    return bytes(data)


def ADD(data, value=0, *, count=1):
    """Add 'value' to each byte in 'data', 'count' times
     
    :param data: Data to perform operation on (str, list, bytes, bytearray, int)
    :param value: Value to add
    :type value: int
    :param count: Number of times to perform function
    :type count: int
    :rtype: bytes
    """
    data = utils.getbytearray(data)
    for _ in range(count):
        for offset, byte in enumerate(data):
            data[offset] = ((byte + value) & 0xff)
    return bytes(data)