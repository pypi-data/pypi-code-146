import asyncio
from typing import Type, TypeVar

import httpx

from pytailor.clients.auth import TailorAuth
from pytailor.clients.handling import (
    handle_retry,
    handle_exception,
    handle_wait_retry,
    handle_waited_for,
)
from pytailor.config import (
    API_BASE_URL,
    ASYNC_REQUEST_TIMEOUT,
    ASYNC_CONNECT_TIMEOUT,
    REQUEST_RETRY_COUNT,
    WAIT_RETRY_COUNT,
)
from pytailor.models import *

T = TypeVar("T")


class AsyncRestClient(httpx.AsyncClient):
    def __init__(self):
        timeout = httpx.Timeout(timeout=ASYNC_REQUEST_TIMEOUT, connect=ASYNC_CONNECT_TIMEOUT)
        super().__init__(base_url=API_BASE_URL, auth=TailorAuth(), timeout=timeout)

    async def __handle_request(
        self,
        method: str,
        url: str,
        request_data: Optional[BaseModel] = None,
        response_model: Optional[Type[T]] = None,
        return_none_on: Optional[List[httpx.codes]] = None,
        error_msg: str = "Error.",
        wait_for_operation: bool = False,
        **kwargs,
    ) -> Optional[Union[httpx.Response, T, List[T]]]:

        if request_data:
            kwargs["data"] = request_data.json()

        if return_none_on is None:
            return_none_on = []

        if wait_for_operation:
            pass
            # TODO: make assertion that response_model is BaseOperationResult, i.e. has fields operation_status,
            #       operation_id and msg.

        try:
            no_of_error_retries = 0
            no_of_wait_retries = 0
            while True:
                try:
                    result = await self.__make_request(method, url, response_model, **kwargs)

                    if wait_for_operation:
                        retry, no_of_wait_retries, sleep_time = handle_wait_retry(
                            result.operation_status, no_of_wait_retries
                        )
                        if retry and no_of_wait_retries < WAIT_RETRY_COUNT:
                            # set method and url for subsequent calls
                            method = "get"
                            url += f"/{result.operation_id}"
                        else:
                            return handle_waited_for(result)  # may raise BackendResponseError, which will NOT cause
                    else:  # error retry, and will hence be re-raised below
                        return result
                except Exception as exc:
                    retry, no_of_error_retries, sleep_time = handle_retry(exc, no_of_error_retries)
                    if not (retry and no_of_error_retries < REQUEST_RETRY_COUNT):
                        raise
                await asyncio.sleep(sleep_time)

        except Exception as exc:
            handle_exception(exc, return_none_on, error_msg)

    async def __make_request(
        self, method: str, url: str, response_model: Optional[Type[T]] = None, **kwargs
    ) -> Optional[Union[httpx.Response, T, List[T]]]:

        response = await self.request(method, url, **kwargs)
        if response.status_code == httpx.codes.OK:
            if response_model:
                return self.__parse_data(response, response_model)
            else:
                return response
        else:
            response.raise_for_status()

    @staticmethod
    def __parse_data(response: httpx.Response, response_model: Type[T]) -> Union[T, List[T]]:
        parsed = response.json()
        if isinstance(parsed, list):
            return [response_model.parse_obj(obj) for obj in parsed]
        else:
            return response_model.parse_obj(parsed)

    async def checkout_task(self, checkout_query: TaskCheckout) -> Optional[TaskExecutionData]:
        url = f"tasks/checkouts"
        return await self.__handle_request(
            "post",
            url,
            request_data=checkout_query,
            response_model=TaskExecutionData,
            return_none_on=[
                httpx.codes.NOT_FOUND,
                httpx.codes.INTERNAL_SERVER_ERROR  # will prevent the worker from stopping on 500 from the backend
            ],
            error_msg="Could not checkout task.",
        )
