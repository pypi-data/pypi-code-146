from pydantic import BaseModel, Extra
from typing import Optional, Mapping, Literal, Any


class Metadata(BaseModel, extra=Extra.forbid):
    class Provenance(BaseModel, extra=Extra.forbid):
        type: str
        metadata: Optional[Mapping[str, Any]]

    provenance: Provenance
    version: Literal["4.1", "4.1.0", "4.1.1", "4.1.2", "4.1.3"]
    timezone: str = "localtime"
