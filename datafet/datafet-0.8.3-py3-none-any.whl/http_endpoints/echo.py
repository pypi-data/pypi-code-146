from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1/echo", tags=["echo"])


@router.get("")
def get_echo(request: Request) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(request.headers))
