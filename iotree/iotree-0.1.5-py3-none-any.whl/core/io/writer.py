import os
import json
import yaml
import toml
import xmltodict as xtd

from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple, Callable, Iterable

from iotree.core.render.funcs import try_all

formats = ['.json', '.yaml', '.toml', 'xml'] #'.proto'

writers = [
    lambda data, path : json.dump(data, open(path, 'w+')),
    lambda data, path : yaml.safe_dump(data, open(path, 'w+')),
    lambda data, path : toml.dump(data, open(path, 'w+')),
    lambda data, path : open(path, "w+").write(xtd.unparse(data))
    #lambda data, path : write_proto(path)
    ]


def write(
    path: Union[str, Path],
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Read a file or directory of files.
    
    Supported file formats: .json, .yaml, .toml, .proto
    """
    path = Path(path)
    
    if path.is_dir():
        return write_dir(path)
    else:
        return write_file(path)
    
def write_file(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    path: Union[str, Path],
    ) -> str:
    """Read a file. Returns the file path.
    
    Accepted data types: dict, list, str, etc."""
    path = Path(path)
    
    if path.suffix == '.json':
        json.dump(data, open(path, 'w+'))
    elif path.suffix == '.yaml':
        yaml.safe_dump(data, open(path, 'w+'))
    elif path.suffix == '.toml':
        toml.dump(data, open(path, 'w+'))
    elif path.suffix == '.proto':
        write_proto(path)
    elif path.suffix == '.xml':
        open(path, "w+").write(xtd.unparse(data))
    else:
        try_all(writers, data, path)
    
def write_proto(
    path: Union[str, Path],
    ) -> Dict[str, Any]:
    """Read a proto file."""
    raise NotImplementedError('Proto file reading not implemented yet.')
  
def write_dir(
    data_array: List[Dict[str, Any]],
    path: Union[str, Path],
    prefix: Optional[str] = "file-",
    extension: Optional[str] = ".json",
    ) -> List[Dict[str, Any]]:
    """Store many files separately in a directory."""
    
    raise NotImplementedError('Directory writing not implemented yet.')