from enum import Enum

from aiohttp import FormData
from pydantic import BaseModel

from wonda.api.request_validator.abc import ABCRequestValidator
from wonda.api.utils.file_util import File
from wonda.modules import json


class TranslateFriendlyTypesRequestValidator(ABCRequestValidator):
    async def validate(self, request: dict) -> dict:
        data = FormData(quote_fields=False)

        for k, v in request.items():
            if isinstance(v, str) or isinstance(v, int):
                data.add_field(k, str(v))
            elif isinstance(v, bool):
                data.add_field(k, int(v))
            elif isinstance(v, list):
                data.add_field(k, ",".join(str(e) for e in v))
            elif isinstance(v, dict):
                data.add_field(k, json.dumps(await self.validate(v)))
            elif isinstance(v, BaseModel):
                data.add_field(k, v.json(exclude_none=True, encoder=json.dumps))
            elif isinstance(v, File):
                data.add_field(k, v.content, filename=v.name)
            elif isinstance(v, Enum):
                data.add_field(k, v.value)
            elif v is None:
                pass

        return data
