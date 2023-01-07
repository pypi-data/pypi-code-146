import pytest

# TODO: Need to setup CI in a way that actually has a backend to hit, right now this depends on cloud and on-prem running locally
from rhino_health import ApiEnvironment, SDKVersion, login
from rhino_health.lib.endpoints.model_result.model_result_dataclass import ModelResult


@pytest.mark.local
class TestModelResultEndToEnd:
    def test_get_model_result(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="ido@rhinohealth.com",
            password="3107",
            sdk_version=SDKVersion.PREVIEW,
        )
        expected = {
            "uid": "224aed5a-a507-42cc-8771-7a0843b2ef61",
            "action_type": "Run",
            "status": "Failed",
            "start_time": "Apr 10, 2022 08:43:02AM",
            "end_time": "Apr 10, 2022 08:48:03AM",
            "input_cohorts": ["f4c5de7a-8c52-45f8-b6fa-f5a2828332bc"],
            "output_cohorts": ["94d92023-967a-4ecb-9866-9d7a78086cc3"],
        }
        model_result = rhino_session.model_result.get_model_result(
            "01d29087-88b3-49a7-94bc-f27e009c1ae5"
        )
        assert model_result.uid == expected["uid"]
        assert model_result.action_type == expected["action_type"]
        assert model_result.status == expected["status"]
        assert model_result.start_time == expected["start_time"]
        assert model_result.input_cohorts == expected["input_cohorts"]
        assert model_result.output_cohorts == expected["output_cohorts"]
