"""
# Settings

Set project name, name of logger and chunk size.
"""
from dataclasses import dataclass, field


@dataclass
class Settings:
    """
    Default settings that can be set when starting the app.
    """
    chunk_size: int = field(default=2000)

    @classmethod
    def set_chunk_size(cls, chunk_size):
        cls.chunk_size = chunk_size
