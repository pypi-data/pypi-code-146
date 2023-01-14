import os

from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple, Callable, Iterable

from .internals import read_any, format_dict

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
    
    suffix = path.suffix
    reader = format_dict["readers_compact"].get(suffix, None)
    
    if reader is not None:
        return reader(path)
    else:
        return read_any(format_dict["readers"], path, msg=f'File format {suffix} not supported.')
        
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
        if any(file.endswith(ext) for ext in format_dict["formats"]):
            readfiles.append(read_file(file))
            
    return readfiles