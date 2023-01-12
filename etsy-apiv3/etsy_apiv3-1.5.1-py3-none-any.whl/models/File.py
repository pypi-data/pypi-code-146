from __future__ import annotations
from pydantic import BaseModel

class File(BaseModel):
    listing_file_id: int
    listing_id: int
    rank: int
    filename: str
    filesize: str
    size_bytes: int
    filetype: str
    create_timestamp: int
    created_timestamp: int
    