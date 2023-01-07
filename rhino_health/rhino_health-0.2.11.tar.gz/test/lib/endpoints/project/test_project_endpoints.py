# TODO: Need to setup CI in a way that actually has a backend to hit, right now this depends on cloud and on-prem running locally
import pytest

from rhino_health import ApiEnvironment, SDKVersion, login


@pytest.mark.local
class TestProjectEndToEnd:
    def test_get_projects(self):
        rhino_session = login(
            rhino_api_url=ApiEnvironment.LOCALHOST_API_URL,
            username="richard@rhinohealth.com",
            password="Test123!",
            sdk_version=SDKVersion.PREVIEW,
        )
        projects = rhino_session.project.get_projects()
        assert len(projects)
        project = projects[0]
        single_project = rhino_session.project.get_projects([project.uid])[0]
        assert single_project == project
        collaborators = single_project.collaborating_workgroups()
        assert not len(collaborators)
        collaborators = projects[1].collaborating_workgroups()
        assert len(collaborators)
