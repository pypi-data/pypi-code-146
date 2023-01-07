# TODO: Need to setup CI in a way that actually has a backend to hit, right now this depends on cloud and on-prem running locally
from time import sleep

import pytest

from rhino_health import ApiEnvironment, SDKVersion, login


@pytest.mark.local
class TestCase:
    def test_valid_login(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="richard@rhinohealth.com",
            password="Test123!",
            sdk_version=SDKVersion.PREVIEW,
        )
        sync_result = rhino_session.cohort.sync_cohort_info("e48ab042-1041-4861-9244-f63de78e31ec")
        assert sync_result.status_code == 200
        cohort_result = rhino_session.cohort.get_cohort("e48ab042-1041-4861-9244-f63de78e31ec")
        assert cohort_result.cohort_info is not None
        project = cohort_result.project
        assert project is not None

    def test_projects(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="richard@rhinohealth.com",
            password="Test123!",
            sdk_version=SDKVersion.PREVIEW,
        )
        sync_result = rhino_session.cohort.sync_cohort_info("e48ab042-1041-4861-9244-f63de78e31ec")
        assert sync_result.status_code == 200
        cohort_result = rhino_session.cohort.get_cohort("e48ab042-1041-4861-9244-f63de78e31ec")
        assert cohort_result.cohort_info is not None
        project = cohort_result.project
        assert project is not None

    def test_timeout(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="richard@rhinohealth.com",
            password="Test123!",
        )
        sync_result = rhino_session.cohort.sync_cohort_info("e48ab042-1041-4861-9244-f63de78e31ec")
        assert sync_result.status_code == 200
        sleep(10)
        sync_result = rhino_session.cohort.sync_cohort_info("e48ab042-1041-4861-9244-f63de78e31ec")
        assert sync_result.status_code == 200
