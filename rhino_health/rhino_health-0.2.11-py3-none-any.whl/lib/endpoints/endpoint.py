import os
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import Extra

FORBID_EXTRA_RESULT_FIELDS = os.environ.get("RHINO_SDK_FORBID_EXTRA_RESULT_FIELDS", "").lower() in {
    "1",
    "on",
    "true",
}

RESULT_DATACLASS_EXTRA = Extra.forbid if FORBID_EXTRA_RESULT_FIELDS else Extra.ignore


class NameFilterMode(Enum):
    EXACT = "iexact"
    CONTAINS = "icontains"


class VersionMode(str, Enum):
    LATEST = "latest"
    ALL = "all"


class Endpoint:
    def __init__(self, session):
        self.session = session

    def _get_filter_query_params(
        self, direct_arguments: Dict[str, Any], name_filter_mode: Optional[NameFilterMode] = None
    ):
        query_params = {k: v for k, v in direct_arguments.items() if v is not None}
        if name_filter_mode is not None and query_params:
            query_params["name_filter_mode"] = name_filter_mode.value
        return query_params
