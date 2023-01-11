import re
from datetime import datetime, tzinfo

from typing import Union


def get_utc_offset(offset: "Union[str,int]") -> int:
    """Get the UTC offset in seconds from a string or integer"""

    if isinstance(offset, str):
        if offset.lower() == "utc" or (offset.lower() == "z"):
            return 0
        
        pattern = re.compile(r"([+-]?)(\d{2}):(\d{2})")
        match = pattern.match(offset)
        
        if not match:
            raise ValueError("Offset must be a string in the format '+HH:MM' or '-HH:MM'")
        
        sign = match.group(1)
        hours = int(match.group(2))
        minutes = int(match.group(3))
        utc_offset = (hours*60 + minutes)*60
        if sign == "-":
            utc_offset *= -1

    elif isinstance(offset, int):
        utc_offset = offset

    else:
        raise ValueError("Offset must be a string in the format '+HH:MM' or '-HH:MM' or an integer in seconds")

    return utc_offset


def format_utc_offset(offset: tzinfo) -> str:
    """Format a UTC offset as a string in the format '+HH:MM' or '-HH:MM'"""
    utc_offset = offset.utcoffset(datetime.now()).total_seconds()
    sign = "-" if utc_offset < 0 else "+"
    hours = int(abs(utc_offset)//3600)
    minutes = int(abs(utc_offset)%3600/60)
    
    if hours == 0 and minutes == 0:
        return "UTC"

    return f"{sign}{hours:02d}:{minutes:02d}"