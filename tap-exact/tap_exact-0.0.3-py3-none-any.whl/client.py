"""REST client handling, including ExactOnlineStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import Stream

from exactonline.api import ExactApi
from exactonline.storage.ini import IniStorage
from exactonline.storage.base import ExactOnlineConfig 
from singer_sdk.tap_base import Tap


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ExactOnlineStream(Stream):
    """ExactOnline stream class."""
    def __init__(self, tap: Tap) -> None:
        super().__init__(tap)
        storage = IniStorage(self.config.get("config_file_location"))
        self.division = storage.get_division()
        self.conn = ExactApi(storage=storage)

