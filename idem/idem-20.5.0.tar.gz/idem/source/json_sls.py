"""
This module is used to retrieve files from a json source
"""
import json
from typing import ByteString
from typing import Tuple

__virtualname__ = "json"


async def cache(
    hub, ctx, protocol: str, source: str, location: str
) -> Tuple[str, ByteString]:
    """
    Take a file from a location definition and cache it in memory
    """
    data = json.loads(source)

    key = hash(str(source))

    if location in data:
        zip_loc_data = data[location]
        data_cache = json.dumps(zip_loc_data).encode("utf-8")
        # use <source>/<sls file> as the unique sls_ref
        return f"{key}/{location}", data_cache
