# Launch with: uvicorn opyrator_multiple_funcs:app --reload

from opyrator.api import create_api
from opyrator import Opyrator
from typing import Any, Dict

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from opyrator import Opyrator
from opyrator.api.fastapi_utils import patch_fastapi


class Input(BaseModel):
    inp: int


class Output(BaseModel):
    res: int


def pyd_func(input: Input) -> Output:
    result = input.inp * 2
    return Output(res=result)


def pyd_func2(input: Input) -> Output:
    result = input.inp * 3
    return Output(res=result)


def create_api(opyrator: Opyrator, opyrator2: Opyrator) -> FastAPI:

    title = opyrator.name
    if 'opyrator' not in opyrator.name.lower():
        title += ' - Opyrator'

    # TODO what about version?
    app = FastAPI(title=title, description=opyrator.description)

    patch_fastapi(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.post(
        '/call',
        operation_id='call',
        response_model=opyrator.output_type,
        # response_model_exclude_unset=True,
        summary='Execute the opyrator.',
        status_code=status.HTTP_200_OK,
    )
    def call(input: opyrator.input_type) -> Any:  # type: ignore
        """Executes this opyrator."""
        return opyrator(input)

    @app.post(
        '/call2',
        operation_id='call2',
        response_model=opyrator2.output_type,
        # response_model_exclude_unset=True,
        summary='Execute the opyrator.',
        status_code=status.HTTP_200_OK,
    )
    def call(input: opyrator2.input_type) -> Any:  # type: ignore
        """Executes this opyrator."""
        return opyrator2(input)

    @app.get(
        '/info',
        operation_id='info',
        response_model=Dict,
        # response_model_exclude_unset=True,
        summary='Get info metadata.',
        status_code=status.HTTP_200_OK,
    )
    def info() -> Any:  # type: ignore
        """Returns informational metadata about this Opyrator."""
        return {}

    # Redirect to docs
    @app.get('/', include_in_schema=False)
    def root() -> Any:
        return RedirectResponse('./docs')

    return app


op = Opyrator(pyd_func)
op2 = Opyrator(pyd_func2)
app = create_api(op, op2)
