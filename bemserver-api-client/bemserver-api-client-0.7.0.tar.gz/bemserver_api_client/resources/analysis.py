"""BEMServer API client resources

/analysis/ endpoints
"""
from .base import BaseResources
from ..enums import BucketWidthUnit
from ..exceptions import BEMServerAPIClientValueError


class AnalysisResources(BaseResources):
    endpoint_base_uri = "/analysis/"
    disabled_endpoints = ["getall", "getone", "create", "update", "delete"]

    def get_completeness(
        self,
        start_time,
        end_time,
        timeseries,
        data_state,
        bucket_width_value,
        bucket_width_unit,
        timezone="UTC",
        *,
        etag=None,
    ):
        if bucket_width_unit not in BucketWidthUnit:
            raise BEMServerAPIClientValueError(
                f"Invalid bucket width unit: {bucket_width_unit}"
            )

        endpoint = f"{self.endpoint_base_uri}completeness"
        q_params = {
            "start_time": start_time,
            "end_time": end_time,
            "timeseries": timeseries,
            "data_state": data_state,
            "bucket_width_value": bucket_width_value,
            "bucket_width_unit": bucket_width_unit.value,
            "timezone": timezone,
        }
        return self._req.getall(endpoint, etag=etag, params=q_params)

    def get_energy_consumption_breakdown(
        self,
        structural_element_type,
        structural_element_id,
        start_time,
        end_time,
        bucket_width_value,
        bucket_width_unit,
        timezone="UTC",
        *,
        etag=None,
    ):
        if bucket_width_unit not in BucketWidthUnit:
            raise BEMServerAPIClientValueError(
                f"Invalid bucket width unit: {bucket_width_unit}"
            )

        endpoint = (
            f"{self.endpoint_base_uri}energy_consumption/"
            f"{structural_element_type}/{structural_element_id}"
        )
        q_params = {
            "start_time": start_time,
            "end_time": end_time,
            "bucket_width_value": bucket_width_value,
            "bucket_width_unit": bucket_width_unit.value,
            "timezone": timezone,
        }
        return self._req.getall(endpoint, etag=etag, params=q_params)
