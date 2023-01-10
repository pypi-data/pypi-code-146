import json
import logging
from typing import Dict, Iterable, Optional, Set

import httpx
import pydantic

from classiq.interface.jobs import JobDescription, JobID, JSONObject

from classiq._internals.async_utils import poll_for
from classiq._internals.client import Client, client, refresh_token_on_failure
from classiq._internals.config import SDKMode
from classiq.exceptions import ClassiqAPIError

_URL_PATH_SEP = "/"
GeneralJobDescription = JobDescription[JSONObject]
_logger = logging.getLogger(__name__)


def _join_url_path(*parts: str) -> str:
    if not parts:
        return ""
    prepend_slash = parts[0].startswith(_URL_PATH_SEP)
    append_slash = parts[-1].endswith(_URL_PATH_SEP)
    joined = _URL_PATH_SEP.join(part.strip(_URL_PATH_SEP) for part in parts)

    return "".join(
        [
            ("/" if prepend_slash else ""),
            joined,
            ("/" if append_slash else ""),
        ]
    )


class JobPoller:
    INITIAL_INTERVAL_SEC = 5
    INTERVAL_FACTOR = 2
    FINAL_INTERVAL_SEC = INITIAL_INTERVAL_SEC * INTERVAL_FACTOR**3  # 40 secs
    DEV_INTERVAL = 0.05

    def __init__(self, base_url: str, required_headers: Optional[Set[str]] = None):
        self._required_headers = required_headers or set()
        client_instance = client()
        self._base_url = client_instance.make_versioned_url(base_url)
        self._async_client = client_instance.async_client()
        self._mode = client_instance.config.mode

    def _make_poll_url(self, response: httpx.Response) -> str:
        job_id: JobID = JobID.parse_obj(response.json())
        return _join_url_path(self._base_url, job_id.job_id)

    @staticmethod
    def _make_cancel_url(poll_url: str) -> str:
        return _join_url_path(poll_url, "cancel")

    def _update_headers(self, response: httpx.Response) -> None:
        for header in self._required_headers:
            try:
                self._async_client.headers[header] = response.headers[header]
            except KeyError as exc:
                raise ClassiqAPIError(
                    f"Response to {self._base_url} is missing header {header}"
                ) from exc

    @refresh_token_on_failure
    async def _request(self, http_method: str, url: str, body: Optional[Dict] = None):
        # Update authorization header in case it expires
        self._async_client.headers.update(client()._get_authorization_header())
        response = await self._async_client.request(
            method=http_method, url=url, json=body
        )
        if response.is_error:
            Client.handle_error(response)
        return response

    async def _submit(self, body: Dict) -> httpx.Response:
        return await self._request(http_method="POST", url=self._base_url, body=body)

    def _interval_sec(self) -> Iterable[float]:
        if self._mode == SDKMode.DEV:
            while True:
                yield self.DEV_INTERVAL
        else:
            i = self.INITIAL_INTERVAL_SEC
            while True:
                yield i
                i = min(i * self.INTERVAL_FACTOR, self.FINAL_INTERVAL_SEC)

    async def _poll(
        self, poll_url: str, timeout_sec: Optional[float]
    ) -> GeneralJobDescription:
        async def poller():
            nonlocal self, poll_url
            raw_response = await self._request(http_method="GET", url=poll_url)
            return raw_response.json()

        async for json_response in poll_for(
            poller, timeout_sec=timeout_sec, interval_sec=self._interval_sec()
        ):
            job_description: GeneralJobDescription = GeneralJobDescription.parse_obj(
                json_response
            )
            if job_description.status.is_final():
                return job_description
        raise ClassiqAPIError("API request timed out")

    async def _cancel(self, poll_url: str) -> None:
        _logger.info("Cancelling job %s", poll_url, exc_info=True)
        cancel_url = self._make_cancel_url(poll_url)
        await self._request(http_method="PUT", url=cancel_url)

    async def run(
        self, body: Dict, timeout_sec: Optional[float]
    ) -> GeneralJobDescription:
        async with self._async_client:
            submit_response = await self._submit(body=body)
            poll_url = self._make_poll_url(response=submit_response)
            self._update_headers(response=submit_response)
            try:
                return await self._poll(poll_url=poll_url, timeout_sec=timeout_sec)
            except Exception:
                await self._cancel(poll_url=poll_url)
                raise

    async def run_pydantic(
        self, model: pydantic.BaseModel, timeout_sec: Optional[float]
    ) -> GeneralJobDescription:
        # TODO: we can't use model.dict() - it doesn't serialize complex class.
        # This was added because JSON serializer doesn't serialize complex type, and pydantic does.
        # We should add support for smarter json serialization.
        body = json.loads(model.json())
        return await self.run(body, timeout_sec)
