import os
import json
import yaml
import toml
import xmltodict as xtd

from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple, Callable, Iterable

formats = ['.json', '.yaml', '.toml', '.proto']

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
        return json.dump(data, open(path, 'w+'))
    elif path.suffix == '.yaml':
        return yaml.safe_dump(data, open(path, 'w+'))
    elif path.suffix == '.toml':
        return toml.dump(data, open(path, 'w+'))
    elif path.suffix == '.proto':
        return write_proto(path)
    elif path.suffix == '.xml':
        with open(path, "w+") as f:
            f.write(xtd.unparse(data))
            
        return path
    else:
        raise ValueError(f'Unsupported file format: {path.suffix}')
    
def write_proto(
    path: Union[str, Path],
    ) -> Dict[str, Any]:
    """Read a proto file."""
    raise NotImplementedError('Proto file reading not implemented yet.')
  
def read_dir(
    path: Union[str, Path],
    ) -> List[Dict[str, Any]]:
    """Read a directory of files."""
    readfiles = []
    for file in os.listdir(path):
        if any(file.endswith(ext) for ext in formats):
            readfiles.append(read_file(file))
            
    return readfiles