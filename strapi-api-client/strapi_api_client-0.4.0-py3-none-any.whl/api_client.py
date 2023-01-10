from .resources.community import CommunityResource
from .resources.group import GroupResource
from .resources.subgroup import SubgroupResource
from .version import __version__
from .requestor import Requestor


class ApiClient(object):
    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        self._api_url = api_url
        self._api_key = f"Bearer {api_key}"
        self._timeout = timeout
        self._requestor = Requestor(api_url=self._api_url, api_key=self._api_key, timeout=self._timeout)
        self._community = CommunityResource(api_url=self._api_url, requestor=self._requestor)
        self._group = GroupResource(api_url=self._api_url, requestor=self._requestor)
        self._subgroup = SubgroupResource(api_url=self._api_url, requestor=self._requestor)

    @property
    def version(self) -> str:
        return __version__

    @property
    def api_url(self) -> str:
        return self._api_url

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def community(self) -> CommunityResource:
        return self._community

    @property
    def group(self) -> GroupResource:
        return self._group

    @property
    def subgroup(self) -> SubgroupResource:
        return self._subgroup

    def __str__(self) -> str:
        return f"{self._api_url}"
