import uuid

import pytest

from rhino_health.lib.endpoints.aimodel.aimodel_dataclass import AIModelRunInput


@pytest.mark.local
class TestAIModelDataclass:
    def test_aimodel_timeout_seconds_sync(self):
        with pytest.raises(ValueError):
            AIModelRunInput(
                aimodel_uid=str(uuid.uuid4()),
                import_cohort_uids=[str(uuid.uuid4())],
                input_cohort_uids=[str(uuid.uuid4())],
                output_cohort_names_suffix="test",
                timeout_seconds=601,
                sync=True,
            )
        AIModelRunInput(
            aimodel_uid=str(uuid.uuid4()),
            import_cohort_uids=[str(uuid.uuid4())],
            input_cohort_uids=[str(uuid.uuid4())],
            output_cohort_names_suffix="test",
            timeout_seconds=601,
            sync=False,
        )
