# TODO: Need to setup CI in a way that actually has a backend to hit, right now this depends on cloud and on-prem running locally
import uuid

import pytest

from rhino_health import ApiEnvironment, SDKVersion, login
from rhino_health.lib.endpoints.aimodel.aimodel_dataclass import (
    AIModel,
    AIModelCreateInput,
    AIModelRunInput,
    AIModelTrainInput,
    ModelTypes,
)


@pytest.mark.local
class TestAIModelEndToEnd:
    def test_get_aimodel(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="ido@rhinohealth.com",
            password="3107",
            sdk_version=SDKVersion.PREVIEW,
        )
        expected = {
            "uid": "ab3d41b3-aa0c-4371-a856-6090240c0c20",
            "name": "ooooo",
            "description": "",
            "model_type": ModelTypes.GENERALIZED_COMPUTE,
            "version": 0,
            "config": {"container_image_uri": ""},
            "project_uid": "68751894-b7a3-4da4-8e7c-a48a38e2783c",
            "input_data_schema": "107330d1-29dd-4490-a2eb-52390807088d",
            "output_data_schema": "107330d1-29dd-4490-a2eb-52390807088d",
        }
        aimodel = rhino_session.aimodel.get_aimodel("ab3d41b3-aa0c-4371-a856-6090240c0c20")
        assert aimodel.uid == expected["uid"]
        assert aimodel.description == expected["description"]
        assert aimodel.model_type == expected["model_type"]
        assert aimodel.version == expected["version"]
        assert aimodel.config == expected["config"]
        assert aimodel.project_uid == expected["project_uid"]
        assert aimodel.input_data_schema == expected["input_data_schema"]
        assert aimodel.output_data_schema == expected["output_data_schema"]

    def test_create_aimodel(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="ido@rhinohealth.com",
            password="3107",
            sdk_version=SDKVersion.PREVIEW,
        )

        random_name = str(uuid.uuid4())
        run_params = AIModelCreateInput(
            session=rhino_session,
            name=random_name,
            description="test case",
            model_type=ModelTypes.GENERALIZED_COMPUTE,
            version=0,
            container_image_uri="",
            project_uid="68751894-b7a3-4da4-8e7c-a48a38e2783c",
            input_data_schema="107330d1-29dd-4490-a2eb-52390807088d",
            output_data_schema="107330d1-29dd-4490-a2eb-52390807088d",
        )
        aimodel = rhino_session.aimodel.create_aimodel(run_params)
        assert type(aimodel) == AIModel
        assert aimodel.name == random_name

    def test_run_aimodel_sync_false(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="ido@rhinohealth.com",
            password="3107",
            sdk_version=SDKVersion.PREVIEW,
        )
        run_params = AIModelRunInput(
            aimodel_uid="ab3d41b3-aa0c-4371-a856-6090240c0c20",
            input_cohort_uids=["f4c5de7a-8c52-45f8-b6fa-f5a2828332bc"],
            output_cohort_names_suffix="test",
            run_params={"code": "df['BMI'] = df.Weight / (df.Height ** 2)"},
            timeout_seconds=600,
            sync=False,
        )
        aimodel = rhino_session.aimodel.run_aimodel(run_params)
        assert aimodel.raw_response.status_code == 201

    def test_run_empty_aimodel_sync_true(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="ido@rhinohealth.com",
            password="3107",
            sdk_version=SDKVersion.PREVIEW,
        )
        run_params = AIModelRunInput(
            aimodel_uid="ab3d41b3-aa0c-4371-a856-6090240c0c20",
            input_cohort_uids=["f4c5de7a-8c52-45f8-b6fa-f5a2828332bc"],
            output_cohort_names_suffix="test",
            run_params="",
            timeout_seconds=600,
            sync=True,
        )
        aimodel = rhino_session.aimodel.run_aimodel(run_params)
        assert aimodel.raw_response.status_code == 200

    def test_train_aimodel(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="ido@rhinohealth.com",
            password="3107",
            sdk_version=SDKVersion.PREVIEW,
        )
        run_params = AIModelTrainInput(
            aimodel_uid="ab3d41b3-aa0c-4371-a856-6090240c0c20",
            input_cohort_uids=["f4c5de7a-8c52-45f8-b6fa-f5a2828332bc"],
            validation_cohort_uids=["f4c5de7a-8c52-45f8-b6fa-f5a2828332bc"],
            validation_cohorts_inference_suffix="test",
            config_fed_server="",
            config_fed_client="",
            timeout_seconds=600,
            sync=True,
        )
        aimodel = rhino_session.aimodel.train_aimodel(run_params)
        assert aimodel.raw_response.status_code == 200
