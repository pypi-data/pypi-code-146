''' mi_models.py
A module to that makes calles to the Infor ION API simple. This module
contains dataclasses that represents data objects from the Api.

Author: Kim Timothy Engh
Email: kim.timothy.engh@epiroc.com
Licence: GPLv3 '''

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Iterator, Any


@dataclass
class Endpoint:
    name: str
    host: str
    port: int
    usr: str
    pwd: str = field(default='')

    def __repr__(s):
        return f'Endpoint(name={s.name}, host={s.host}, port={s.port}, usr={s.usr}, pwd={"*" * len(s.pwd)})'


@dataclass
class MiRecords:
    program: str
    transaction: str
    metadata: List[Dict] = field(repr=False)
    records: List[Dict] = field(repr=False)
    
    @staticmethod
    def __numeric_to_int_float(value: str):
        try:
            return int(value.strip())
        
        except ValueError:
            pass
        
        try:
            return float(value.strip())
        
        except ValueError:
            pass
        
        if value == '':
            return None
        
        else:
            raise ValueError(f'Could not convert value {value} of type {type(value)} to int, float or None')

    @staticmethod
    def __alpha_to_str(value: str):
        return value
        
    @staticmethod
    def __date_to_int(value: str):
        try:
            return int(value.strip())

        except ValueError:
            pass
        
        if value == '':
            return None

    def converted(self, strip=False) -> Iterator[Dict]:
        """ Converts values to correct datatypes based on the metadata
        in the response from the API.
        
        [A, 6] '      '   -> '      '
        [A, 6] 'ABC   '   -> 'ABC'
        [A, 6] 'ABCDEF'   -> 'ABCDEF'
        [A, 6] ''         -> ''
        [N, 1] '1'        -> 1
        [N, 2] ' 1'       -> 1
        [N, 2] '99'       -> 99
        [N, 2] '1.2'      -> 1.2
        [N, 2] ''         -> None
        [D, 8] '20220201' -> 20220201
        [D, 8] ''         -> None
        
        If "strip" is set to "True", any whitespace is is stripped out
        of the result.
        """
        
        converters: List[Callable[[str], Any]] = []
        
        for field in self.metadata:
            if field['type'] == 'A':
                if strip:
                    converters.append(lambda x: self.__alpha_to_str(x.strip()))
                  
                else:  
                    converters.append(self.__alpha_to_str)
            
            elif field['type'] == 'N':
                converters.append(self.__numeric_to_int_float)
                
            elif field['type'] == 'D':
                converters.append(self.__date_to_int)
                
            else:
                print(f''' No converter function for type "{field['type']}" ''')
                converters.append(lambda x: x)
        
        def convert_record(record: Dict[str, str]):
            for (key, value), converter in zip(record.items(), converters):                
                try:
                    record[key] = converter(value)
                
                except:       
                    print(f"""Could not convert key "{key}" with value "{value}" from record {record} """)

            return record
    
        for record in self.records:
            yield convert_record(record)


@dataclass
class MiPrograms:
    records: List[str]


@dataclass
class MiFieldMetadata:
    name: str
    description: str
    fieldtype: str
    length: int
    mandatory: bool


@dataclass
class MiTransactionMetadata:
    program: str
    transaction: str
    description: str
    multi: str
    inputs: List[MiFieldMetadata] = field(repr=False)
    outputs: List[MiFieldMetadata] = field(repr=False)


@dataclass
class MiProgramMetadata:
    program: str
    description: str
    version: str
    transactions: List[Optional[MiTransactionMetadata]] = field(repr=False)


class MiApiError(Exception):
    """ Error class that returns exceptions raised by the the service.
    This comes handy, when incorrect paramters are entered, or if there
    are any other usage errors. """
    
    def __init__(self, code: str, desc: str, xml: str):
        self.code = code
        self.desc = desc
        self.xml = xml
        
        super(MiApiError, self).__init__(f"MiError({': '.join([code, desc])})")
        
        
