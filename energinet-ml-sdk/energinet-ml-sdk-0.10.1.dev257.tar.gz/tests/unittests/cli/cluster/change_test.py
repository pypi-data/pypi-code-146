from unittest.mock import ANY, Mock, PropertyMock, patch

from click.testing import CliRunner

from energinetml.cli.cluster.change import change
from tests.constants import WORKSPACE_NAME

# -- Tests -------------------------------------------------------------------


@patch("energinetml.cli.cluster.change.backend")
def test__change_cluster__no_clusters_exists__should_abort(backend_mock, model):
    """
    :param Mock backend_mock:
    :param Model model:
    """
    # Workaround: Can not mock property "name" of Mock object
    workspace = Mock()
    type(workspace).name = PropertyMock(return_value=WORKSPACE_NAME)

    backend_mock.get_workspace.return_value = workspace
    backend_mock.get_compute_clusters.return_value = []

    # Act
    result = CliRunner().invoke(cli=change, args=["--path", model.path])

    # Assert
    assert result.exit_code == 1


@patch("energinetml.cli.cluster.change.backend")
@patch("energinetml.cli.cluster.change.click.prompt")
def test__change_cluster__provide_a_cluster_that_does_not_exists__should_prompt_for_clister_and_update_model(  # noqa: E501
    prompt_mock, backend_mock, model_with_project
):
    """
    :param Mock prompt_mock:
    :param Mock backend_mock:
    :param Model model_with_project:
    """
    # Workaround: Can not mock property "name" of Mock object
    workspace = Mock()
    type(workspace).name = PropertyMock(return_value=WORKSPACE_NAME)

    cluster = Mock()
    cluster.vm_size = "cluster-vm-size"
    type(cluster).name = PropertyMock(return_value="an-existing-cluster")

    backend_mock.get_workspace.return_value = workspace
    backend_mock.get_compute_clusters.return_value = [cluster]

    prompt_mock.return_value = "an-existing-cluster"

    # Act
    result = CliRunner().invoke(
        cli=change,
        args=[
            "--path",
            model_with_project.path,
            "--cluster-name",
            "a-cluster-that-doesnt-exists",
        ],
    )

    # Assert
    assert result.exit_code == 0

    prompt_mock.assert_called_once_with(
        text="Please enter name of a compute cluster to use", type=ANY
    )
