import logging
import typing
import json
import numpy as np
from fastapi.responses import JSONResponse as _JSONResponse
from .models.commons.exceptions import ServingHttpError


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class JSONResponse(_JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=NpEncoder
        ).encode("utf-8")


def __mk_response_body(code, message, data):
    return {"code": code, "message": message, "data": data}


def _mk_json_response(code, message, data, status_code):
    return JSONResponse(
        __mk_response_body(
            code,
            message,
            data,
        ),
        status_code=status_code,
    )


def success_response(body: dict, status_code: int = 200):
    if not isinstance(body, dict):
        raise ValueError("body must be a dict!")
    return _mk_json_response(0, "Success", body, status_code)


def failed_response(body: dict = None, message: str = None, status_code: int = 400):
    if body is None:
        body = {}
    if not isinstance(body, dict):
        raise ValueError("body must be a dict!")
    return _mk_json_response(-1, message if message else "Failed", body, status_code)


def failed_response_with_break(
        body: dict = None, message: str = None, status_code: int = 400
):
    if body is None:
        body = {}
    if not isinstance(body, dict):
        raise ValueError("body must be a dict!")

    raise ServingHttpError(
        status_code=status_code,
        detail=__mk_response_body(-1, message if message else "Failed", body),
    )


def get_logger(name, level) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger


__all__ = ["success_response", "failed_response", "failed_response_with_break"]
