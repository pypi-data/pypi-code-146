from datetime import timezone, timedelta, tzinfo
from typing import Optional
from collections import OrderedDict

import re

from tsp.time import get_utc_offset


class GtnpMetadata:
    def __init__(self, filepath):
        """A class to read GTN-P metadata files

        Parameters
        ----------
        filepath : str
            Path to GTN-P *.metadata.txt file.
        """
        self.filepath = filepath
        self.dict = OrderedDict()
        self._read()
        self._parse()

    def _read(self):
        with open(self.filepath, 'r') as f:
            self._raw = f.readlines()
    
    def _parse(self):
        lines = [line for line in self._raw]  # Make a copy in case we need to use fallback plan
        
        try:
            self.dict = OrderedDict()
            recursively_build_metadata(lines, self.dict)

        except Exception:
            print("Couldn't build nested dictionary. Fallback to simple dictionary.")
            self.dict = OrderedDict()
            self._parse_dict()
 

    def _parse_dict(self) -> None:
        pattern = re.compile(r"^([^:]+):\s*(.*)$")
        
        for line in self._raw:
            result = pattern.match(line)
            if result:
                key, value = result.groups()
                
                if value.strip() != "":
                    self.dict[key] = value.strip()

    def get_timezone(self) -> Optional[tzinfo]:
        try:
            zone = self.dict['Timezone']
        except KeyError:
            return None
        
        if zone == 'UTC':
            return timezone.utc
        elif isinstance(zone, str):
            seconds = get_utc_offset(zone.strip())
            tz = timezone(timedelta(seconds=seconds))
            return tz
    
    def get_latitude(self) -> Optional[float]:
        try:
            return float(self.dict['Latitude'])
        except KeyError:
            return None

    def get_longitude(self) -> Optional[float]:
        try:
            return float(self.dict['Longitude'])
        except KeyError:
            return None

    @property
    def values(self):
        pass


def recursively_build_metadata(lines: list, odict: OrderedDict, depth:int=0) -> None:
    """ A recursive function to build an OrderedDict from a list of lines.
    
    The function expects lines to be in the format:
    Key: Value
    Key: Value
    Key: 
        Subkey: Multi line Subvalue
                Multi line Subvalue
                Multi line Subvalue
        Subkey: Subvalue
        Subkey: 
            Subsubkey: Subsubvalue

    Parameters
    ----------
    lines : list
        A list of lines from a metadata file.
    odict : OrderedDict
        An OrderedDict to build.
    depth : int, optional
        The depth of the OrderedDict, by default 0
    
    """
    pattern = re.compile(r"^(\t*)([^:]+):\s*(.*)$")

    while lines:
        line = lines.pop(0)
        result = pattern.match(line)
        
        if result:
            tabs, key, value = result.groups()
            
            if len(tabs) < depth:  # Un-indent, return to previous level
                lines.insert(0, line)
                return

            if value.strip() != "":  # Valid key:value pair
                odict[key] = value.strip()
            
            else:  # Empty value, recurse
                odict[key] = OrderedDict()
                recursively_build_metadata(lines, odict[key], depth=depth+1)
                
        else:  # Multi-line value
            try:
                odict[next(reversed(odict))] = odict[next(reversed(odict))] + line
            except StopIteration:  # If no key:value pair has been added yet
                continue
            except TypeError:  # If the value is not a string
                continue
            continue
