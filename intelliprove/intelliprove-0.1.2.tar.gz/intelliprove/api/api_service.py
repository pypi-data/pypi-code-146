import datetime

import requests
from requests import Response

from typing import Optional, Union, Iterable
from pathlib import Path
import urllib.parse

from intelliprove.api.models import IntelliproveApiSettings
from intelliprove.api.models.responses import BiomarkersResponse, QualityResponse
from intelliprove.api.utils import is_valid_video_path, is_valid_uuid

from intelliprove.api.exceptions import (
    ApiException, ApiForbiddenException, ApiErrorException, ApiNotFoundException,
    MediaException, InvalidUuidException)


class ApiService:
    def __init__(self, api_key: str, settings: Optional[IntelliproveApiSettings] = None):
        self.api_key = api_key
        # check if custom settings are set, if not => use default
        self.settings = settings if isinstance(settings, IntelliproveApiSettings) else IntelliproveApiSettings()

    def make_url(self, sub_url: str) -> str:
        # Returns full url for given sub url
        sub_url = "/" + sub_url if sub_url[0] != '/' else sub_url
        return self.settings.full_url + sub_url

    def get_upload_url(self) -> dict:
        # Sends request to api to get S3 upload url for video
        uri = self.make_url('/videos/upload_url')
        resp = requests.get(uri, **self.request_kwargs)
        self._check_status_code(resp)  # check response
        return resp.json()

    def check_image(self, img_path: Union[Path, str]) -> QualityResponse:
        uri = self.make_url('videos/check')
        files = {'image': open(img_path, 'rb')}
        resp = requests.post(uri, files=files, **self.request_kwargs)

        self._check_status_code(resp)  # check response
        return QualityResponse.from_json(resp.json())

    def upload_video(self, video: Union[Path, str], upload_data: dict) -> bool:
        # Uploads video using the request library
        if not is_valid_video_path(video):
            raise MediaException("Video does not exist or is invalid format.", video)

        uri = upload_data['url']
        data = upload_data['form_data_fields']
        files = {'file': open(video, 'rb')}
        headers = {
            'Accept': 'application/json'
        }

        resp = requests.post(uri, data=data, files=files, headers=headers, timeout=self.settings.upload_timeout)
        self._check_status_code(resp, 204)
        return True

    def queue_upload(self, uuid: str, performer: Optional[str] = None, patient: Optional[str] = None) -> bool:
        # Queues the uploaded video for processing by uuid

        if not is_valid_uuid(uuid):
            raise InvalidUuidException(uuid)

        uri = self.make_url(f"videos/process/{uuid}")
        query = {}
        if performer:
            if not isinstance(performer, str):
                raise ValueError(f'Invalid type for performer, expected str got: {type(performer)}.')
            query['performer-ref'] = performer
        if patient:
            if not isinstance(patient, str):
                raise ValueError(f'Invalid type for patient, expected str got: {type(patient)}.')
            query['patient-ref'] = patient

        uri = self._add_query_to_uri(uri, query)

        resp = requests.post(uri, **self.request_kwargs)
        self._check_status_code(resp)
        return True

    def get_result(self, uuid: str) -> Optional[BiomarkersResponse]:
        # Get result of processed upload by uuid
        if not is_valid_uuid(uuid):
            raise InvalidUuidException(uuid)

        uri = self.make_url(f"results/wait/{uuid}")

        resp = requests.get(uri, **self.request_kwargs)
        self._check_status_code(resp, (200, 204))
        return BiomarkersResponse.from_json(resp.json()) if resp.status_code == 200 else None

    @property
    def headers(self) -> dict:
        return {
            'x-api-key': self.api_key,
            'Accept': 'application/json'
        }

    @property
    def request_kwargs(self) -> dict:
        return {
            'headers': self.headers,
            'timeout': self.settings.send_timeout
        }

    @staticmethod
    def _check_status_code(resp: Response, expected: Union[int, Iterable] = 200):
        if resp.status_code == 403:
            raise ApiForbiddenException()

        if resp.status_code == 404:
            raise ApiNotFoundException()

        if resp.status_code >= 500:
            raise ApiErrorException(status_code=resp.status_code)

        if resp.status_code != expected if isinstance(expected, int) else resp.status_code not in expected:
            raise ApiException("Unexpected response from IntelliProve api.", resp.status_code)

    @staticmethod
    def _add_query_to_uri(uri, query: dict) -> str:
        # add dict query to uri and url encode
        return uri + "?" + urllib.parse.quote("&".join([f'{str(key)}={str(val)}' for key, val in query.items()]))
