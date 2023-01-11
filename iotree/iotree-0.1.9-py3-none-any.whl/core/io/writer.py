import os
import json
import yaml
import toml
import xmltodict as xtd

from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple, Callable, Iterable

from .internals import format_dict

def write(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    path: Union[str, Path],
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Write a file to path in multiple formats.
    
    Supported file formats: .json, .yaml, .toml, .proto
    """
    path = Path(path)
    
    if path.is_dir():
        return write_dir(data, path)
    else:
        return write_file(data, path)
    
def write_file(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    path: Union[str, Path],
    ) -> str:
    """Read a file. Returns the file path.
    
    Accepted data types: dict, list, str, etc."""
    path = Path(path)
    suffix = path.suffix
    writer = format_dict["writers_compact"].get(suffix, None)
    
    if writer is not None:
        return writer(data, path)
    else:
        call_any(format_dict["writers"], data, path)
    
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