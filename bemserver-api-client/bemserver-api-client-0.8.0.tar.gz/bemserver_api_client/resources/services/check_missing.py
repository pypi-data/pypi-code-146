"""BEMServer API client check missing service resources

/st_check_missings_by_campaigns/ endpoints
"""
from ..base import BaseResources


class ST_CheckMissingByCampaignResources(BaseResources):
    endpoint_base_uri = "/st_check_missings_by_campaigns/"

    def get_full(self, *, etag=None, **kwargs):
        endpoint = f"{self.endpoint_base_uri}full"
        return self._req.getall(endpoint, etag=etag, params=kwargs)
