import os
import json
import yaml
import toml
import xmltodict as xtd

from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple, Callable, Iterable

formats = ['.json', '.yaml', '.toml', '.proto']

def read(
    path: Union[str, Path],
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Read a file or directory of files.
    
    Supported file formats: .json, .yaml, .toml, .proto
    """
    path = Path(path)
    
    if path.is_dir():
        return read_dir(path)
    else:
        return read_file(path)
    
def read_file(
    path: Union[str, Path],
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Read a file."""
    path = Path(path)
    
    if path.suffix == '.json':
        return json.loads(open(path, 'r').read())
    elif path.suffix == '.yaml':
        return yaml.safe_load(open(path, 'r'))
    elif path.suffix == '.toml':
        return toml.loads(open(path, 'r').read())
    elif path.suffix == '.proto':
        return read_proto(path)
    elif path.suffix == '.xml':
        return xtd.parse(open(path, 'r').read())
    else:
        raise ValueError(f'Unsupported file format: {path.suffix}')
    
def read_proto(
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