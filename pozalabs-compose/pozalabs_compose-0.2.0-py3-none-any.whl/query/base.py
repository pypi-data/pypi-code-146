from typing import Any

from .. import container


class Query(container.BaseModel):
    def to_query(self) -> Any:
        ...
