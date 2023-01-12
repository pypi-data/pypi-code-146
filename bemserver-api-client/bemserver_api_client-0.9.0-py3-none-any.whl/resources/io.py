"""BEMServer API client resources

/io/ endpoints
"""
from .base import BaseResources


class IOResources(BaseResources):
    endpoint_base_uri = "/io/"
    disabled_endpoints = ["getall", "getone", "create", "update", "delete"]

    def upload_timeseries_csv(self, campaign_id, csv_files):
        """

        :param dict csv_files:
            key is the upload field name (timeseries_csv)
            value is a file stream (tempfile.SpooledTemporaryFile)
        """
        endpoint = f"{self.endpoint_base_uri}timeseries"
        q_params = {"campaign_id": campaign_id}
        return self._req.upload_files(endpoint, params=q_params, files=csv_files)

    def upload_sites_csv(self, campaign_id, csv_files):
        """

        :param dict csv_files:
            key is the upload field name (sites_csv, buildings_csv...)
            value is a file stream (tempfile.SpooledTemporaryFile)
        """
        endpoint = f"{self.endpoint_base_uri}sites"
        q_params = {"campaign_id": campaign_id}
        return self._req.upload_files(endpoint, params=q_params, files=csv_files)
