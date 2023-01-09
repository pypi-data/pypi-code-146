from typing import Any, Callable

from fastapi.types import DecoratedCallable
from fastapi import APIRouter as FastAPIRouter
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from .model import Model
from .exceptions import ServingHttpError
from ...settings import KUBEFLOW_USER_ID, METAAI_APP
import uvicorn


def authn(user_id):
    if not METAAI_APP:
        return True
    if not user_id or user_id != KUBEFLOW_USER_ID:
        return False

    return True


class APIRouter(FastAPIRouter):
    def api_route(
            self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]

        add_path = super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )

        alternate_path = path + "/"
        add_alternate_path = super().api_route(
            alternate_path, include_in_schema=False, **kwargs
        )

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            add_alternate_path(func)
            return add_path(func)

        return decorator


class ModelServer:
    @classmethod
    def create_application(cls) -> FastAPI:
        # return APIRouter(redirect_slashes=True)
        return FastAPI(redoc_url=None, openapi_url=None)

    @classmethod
    def _add_error_handler(cls, app: FastAPI):
        @app.exception_handler(ServingHttpError)
        async def serving_error_handler(request, exc: ServingHttpError):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @classmethod
    def _include_api_route(cls, app: FastAPI, model: Model):
        api = APIRouter(redirect_slashes=False)

        @api.post("/predict")
        async def predict(body: dict, kubeflow_userid: str = Header(default=None)):
            if not authn(kubeflow_userid):
                return JSONResponse(
                    status_code=401,
                    content={
                        "code": 401,
                        "message": f"access info not found in our records!",
                    },
                )

            return await model(body=body)

        app.include_router(api)

    @classmethod
    def start(cls, model: Model):

        if not isinstance(model, Model):
            raise ValueError(
                "Please inherit 'metaai.serving.models.Model' for custom model service class"
            )
        try:
            model.load()
        except Exception as load_e:
            raise RuntimeError(
                f"loading model file were error ! error msg {load_e}"
            ) from load_e

        if not model.ready:
            raise RuntimeError(
                "ModelService load model not ready! check you class,please!}"
            )
        app = cls.create_application()

        @app.get("/")
        async def health():
            return {"status": "Alive"}

        cls._include_api_route(app, model)
        cls._add_error_handler(app)
        # 使用命令行运行服务，可能会出现的问题
        # 加载模型的时候，一些类，需要在uvicorn文件上显式的声明 这显然不友好

        # 使用当前方法 目前看来和命令行启动并没有太多的不一样
        uvicorn.run(app, host="0.0.0.0", port=8089, proxy_headers=True, forwarded_allow_ips="*")
