import logging
from typing import Dict, Generator, List, Union

from requests import HTTPError, Session

from belvo import __version__
from belvo.exceptions import RequestError

logger = logging.getLogger(__name__)


class APISession:
    _secret_key_id: str
    _secret_key_password: str
    _url: str

    def __init__(self, url: str) -> None:
        self._url = url
        self._session = Session()
        self._session.headers.update({"User-Agent": f"belvo-python ({__version__})"})

    @property
    def url(self) -> Union[str, None]:
        return self._url

    @property
    def key_id(self) -> Union[str, None]:
        return self._secret_key_id

    @property
    def session(self) -> Session:
        return self._session

    @property
    def headers(self) -> Dict:
        return self.session.headers  # type: ignore

    def login(self, secret_key_id: str, secret_key_password: str, timeout: int = 5) -> bool:
        base_url = "{}/api/".format(self.url)
        self._secret_key_id = secret_key_id
        self._secret_key_password = secret_key_password
        self._session.auth = (secret_key_id, secret_key_password)

        try:
            r = self.session.get(base_url, timeout=timeout)
            r.raise_for_status()
        except HTTPError:
            return False
        return True

    def _get(self, url: str, params: Dict = None) -> Dict:
        if params is None:
            params = {}

        timeout = params.pop("timeout", 5)
        r = self.session.get(url=url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()

    def get(self, endpoint: str, id: str, params: Dict = None) -> Dict:
        url = "{}{}{}/".format(self.url, endpoint, id)
        return self._get(url=url, params=params)

    def put(
        self, endpoint: str, id: str, data: Dict, raise_exception: bool = False, **kwargs
    ) -> Union[List[Dict], Dict]:
        url = "{}{}{}/".format(self.url, endpoint, id)
        r = self.session.put(url=url, json=data, **kwargs)

        if raise_exception:
            try:
                r.raise_for_status()
            except HTTPError:
                raise RequestError(r.status_code, r.json())

        return r.json()

    def list(self, endpoint: str, params: Dict = None) -> Generator:
        url = "{}{}".format(self.url, endpoint)
        while True:
            data = self._get(url, params=params)
            for result in data["results"]:
                yield result

            if not data["next"]:
                break

            url = data["next"]
            params = None

    def post(
        self, endpoint: str, data: Dict, raise_exception: bool = False, *args, **kwargs
    ) -> Union[List, Dict]:
        url = "{}{}".format(self.url, endpoint)
        r = self.session.post(url, json=data, **kwargs)

        if raise_exception:
            try:
                r.raise_for_status()
            except HTTPError:
                raise RequestError(r.status_code, r.json())

        return r.json()

    def patch(
        self, endpoint: str, data: Dict, raise_exception: bool = False, **kwargs
    ) -> Union[List[Dict], Dict]:
        url = "{}{}".format(self.url, endpoint)
        r = self.session.patch(url=url, json=data, **kwargs)

        if raise_exception:
            try:
                r.raise_for_status()
            except HTTPError:
                raise RequestError(r.status_code, r.json())

        return r.json()

    def delete(self, endpoint: str, id: str, timeout: int = 5) -> bool:
        url = "{}{}{}/".format(self.url, endpoint, id)
        r = self.session.delete(url, timeout=timeout)
        try:
            r.raise_for_status()
        except HTTPError:
            return False
        return True
