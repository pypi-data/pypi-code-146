from typing import Iterable

from fastapi.responses import JSONResponse

from velait.velait_fastapi.api.schemas import BaseSchema


class APIResponse(JSONResponse):
    def __init__(
        self,
        content=None,
        status_code=200,
        headers=None,
        errors: Iterable['ResponseErrorItem'] = None,
        **kwargs
    ):
        if errors is not None:
            content = {
                "Errors": [error.dict() for error in errors],
            }

        super(APIResponse, self).__init__(content, status_code=status_code, headers=headers, **kwargs)


class ResponseErrorItem(BaseSchema):
    name: str
    description: str


__all__ = [
    'APIResponse',
    'ResponseErrorItem',
]
