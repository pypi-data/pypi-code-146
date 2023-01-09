from typing import Any, Dict
import inspect
from ... import settings


class Model:
    def __init__(self, name: str):
        self.name = name

        self.ready = False
        self.model_path = settings.DEFAULT_MODEL_PATH

    async def _preprocess(self, request: Any) -> Any:
        return request

    def _postprocess(self, response: Any) -> Dict:
        return response

    async def predict(self, request: Any):
        return request

    def load(self):
        self.ready = True

        return self.ready

    def _validate(self, request: Any) -> Any:
        return request

    async def __call__(self, body: dict, *args, **kwargs):
        request = (
            await self._preprocess(body)
            if inspect.iscoroutinefunction(self._preprocess)
            else self._preprocess(body)
        )
        request = self._validate(request)

        response = (
            (await self.predict(request))
            if inspect.iscoroutinefunction(self.predict)
            else self.predict(request)
        )

        return self._postprocess(response)
