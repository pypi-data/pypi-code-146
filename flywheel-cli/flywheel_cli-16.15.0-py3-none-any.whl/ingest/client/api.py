"""Client implementation using a hosted HTTP ingest API"""
import json
import typing
import uuid

import requests
import urllib3.util.retry

from ... import util
from ...models import FWAuth
from .. import config as C
from .. import schemas as T
from .abstract import Client


class APIClient(Client):
    """Ingest API client implementing the CRUD interface"""

    BACKOFF_FACTOR = 0.1
    STATUS_FORCELIST = {502, 503, 504}
    TOTAL_RETRIES = 5

    def __init__(self, url: str):
        super().__init__(url)
        self.session = requests.Session()
        self.session.headers["Authorization"] = util.get_api_key()
        retry = urllib3.util.retry.Retry(
            backoff_factor=self.BACKOFF_FACTOR,
            status_forcelist=self.STATUS_FORCELIST,
            total=self.TOTAL_RETRIES,
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def call_api(self, method: str, url: str, **kwargs: typing.Any):
        """
        Send HTTP request with URL prefix 'ingest_api_url' and timeouts set.
        Raise requests.HTTPError if the response status is not 2xx/OK.
        Return loaded JSON by default or the original response if 'stream=True'.
        """
        url = f"{self.url}{url}"
        kwargs.setdefault("timeout", (util.CONNECT_TIMEOUT, util.READ_TIMEOUT))
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        if kwargs.get("stream"):
            return response
        return response.json()

    def call_bound_api(self, method, url, **kwargs):
        """Use 'call_api' with ingest-bound URL prefix '/ingests/{ingest_id}'"""
        return self.call_api(method, f"/ingests/{self.ingest_id}{url}", **kwargs)

    def iter_lines(self, url: str) -> typing.Iterable[str]:
        """Use 'call_bound_api' to stream a GET response and yield decoded lines"""
        response = self.call_bound_api("GET", url, stream=True)
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                yield line.decode("utf-8") + "\n"

    # Non-ingest-bound methods

    def create_ingest(
        self,
        config: C.IngestConfig,
        strategy_config: C.StrategyConfig,
        fw_auth: typing.Optional[FWAuth] = None,
    ) -> T.IngestOutAPI:
        payload = {
            "config": config.dict(exclude_none=True),
            "strategy_config": strategy_config.dict(exclude_none=True),
        }
        ingest = T.IngestOutAPI(**self.call_api("POST", "/ingests", json=payload))
        self.bind(ingest.id)
        return ingest

    def delete_ingest(self, ingest_id: uuid.UUID) -> None:
        self.call_api("POST", f"/ingests/{ingest_id}/delete")

    def list_ingests(
        self, api_key: typing.Optional[str] = None
    ) -> typing.Iterable[T.IngestOutAPI]:
        for ingest in self.call_api("GET", "/ingests"):
            yield T.IngestOutAPI(**ingest)

    # Ingest-bound methods

    @property
    def ingest(self) -> T.IngestOutAPI:
        return T.IngestOutAPI(**self.call_bound_api("GET", ""))

    def load_subject_csv(self, subject_csv: typing.BinaryIO) -> None:
        self.call_bound_api("POST", "/subjects", files={"subject_csv": subject_csv})

    def start(self) -> T.IngestOutAPI:
        return T.IngestOutAPI(**self.call_bound_api("POST", "/start"))

    def review(self, changes: typing.Optional[T.ReviewIn] = None) -> T.IngestOutAPI:
        return T.IngestOutAPI(**self.call_bound_api("POST", "/review", json=changes))

    def abort(self) -> T.IngestOutAPI:
        return T.IngestOutAPI(**self.call_bound_api("POST", "/abort"))

    @property
    def progress(self) -> T.Progress:
        return T.Progress(**self.call_bound_api("GET", "/progress"))

    @property
    def summary(self) -> T.Summary:
        return T.Summary(**self.call_bound_api("GET", "/summary"))

    @property
    def report(self) -> T.Report:
        return T.Report(**self.call_bound_api("GET", "/report"))

    @property
    def tree(self) -> typing.Iterable[T.Container]:
        for line in self.iter_lines("/tree"):
            yield T.Container(**json.loads(line))

    @property
    def audit_logs(self) -> typing.Iterable[str]:
        return self.iter_lines("/audit")

    @property
    def deid_logs(self) -> typing.Iterable[str]:
        return self.iter_lines("/deid")

    @property
    def subjects(self) -> typing.Iterable[str]:
        return self.iter_lines("/subjects")
