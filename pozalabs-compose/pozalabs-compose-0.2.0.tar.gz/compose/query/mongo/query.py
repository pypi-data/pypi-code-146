from typing import Any, Optional

from pydantic import conint

from .. import base


class MongoQuery(base.Query):
    def to_query(self) -> list[dict[str, Any]]:
        ...


class MongoFilterQuery(MongoQuery):
    page: Optional[conint(ge=1)] = None
    per_page: Optional[conint(ge=1)] = None

    @property
    def can_paginate(self) -> bool:
        return self.page is not None and self.per_page is not None
