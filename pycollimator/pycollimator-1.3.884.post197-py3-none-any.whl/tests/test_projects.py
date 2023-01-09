import json
import os
import sys

from pycollimator import Api, global_variables
import pytest
from tests import config


def list_includes(lst, predicate):
    for item in lst:
        if predicate(item):
            return True
    return False


def test_projects_list():
    response = Api.get_projects()
    assert isinstance(response, object)

    projects = response["projects"]
    assert len(projects) > 0
    assert len(projects) == response["count"]

    project_uuid = global_variables.GlobalVariables.project_uuid()
    found = False
    for project in projects:
        assert isinstance(project, dict)
        if project["uuid"] == project_uuid:
            found = True
            break
    assert found


def test_models_list():
    response = Api.get_project()
    assert isinstance(response, dict)

    models = response["models"]
    assert len(models) > 0

    # check that we find all the expected models in this project
    expected_models = config["models"]
    assert len(expected_models) > 0
    fixtures_root = os.environ.get("FIXTURES_ROOT", "")

    for name, _modelcfg in expected_models.items():
        with open(f"{fixtures_root}tests/fixtures/{name}.json", "r") as f:
            model_data = json.loads(f.read())
        assert list_includes(models, lambda item: item["name"] == model_data["name"])


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
