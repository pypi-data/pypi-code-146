import json
from unittest.mock import ANY, MagicMock, Mock, PropertyMock, patch

from click.testing import CliRunner
from packaging.version import Version

from energinetml import PACKAGE_NAME
from energinetml.cli.model.submit import submit
from energinetml.core.model import Model
from tests.constants import COMPUTE_TARGET, VM_SIZE


class TestModelSubmit:
    def test__download_and_not_wait__should_abort(self, model_path):
        """
        :param str model_path:
        """
        runner = CliRunner()

        # Act
        result = runner.invoke(
            cli=submit, args=["--path", model_path, "--download", "--nowait"]
        )

        # Assert
        assert result.exit_code == 1
        assert result.output.startswith(
            "Can not use -d/--download together with --nowait"
        )

    @patch.object(Model, "requirements", new_callable=PropertyMock)
    def test__package_name_not_in_requirements__should_abort(
        self, model_requirements_mock, model_path
    ):
        """
        :param Mock model_requirements_mock:
        :param str model_path:
        """
        runner = CliRunner()

        model_requirements_mock.return_value = []

        # Act
        result = runner.invoke(cli=submit, args=["--path", model_path])

        # Assert
        assert result.exit_code == 1
        assert result.output.startswith(
            f"Could not find '{PACKAGE_NAME}' in the project's requirements.txt file"
        )

    @patch("energinetml.cli.model.submit.backend")
    @patch.object(Model, "requirements", new_callable=MagicMock)
    def test__required_sdk_version_less_than_current__should_echo_warning(
        self, model_requirements_mock, backend_mock, model_path, clusters_mock
    ):
        """
        :param Mock model_requirements_mock:
        :param Mock backend_mock:
        :param str model_path:
        """
        runner = CliRunner()

        model_requirements_mock.__contains__.return_value = True
        model_requirements_mock.get_version.return_value = Version("0.0.0")

        backend_mock.get_compute_clusters.return_value = clusters_mock

        # Act
        result = runner.invoke(cli=submit, args=["--path", model_path])

        # Assert
        assert result.exit_code == 0
        assert (
            (
                "WARNING: Your requirements.txt file contains a version of "
                "%s (0.0.0) which is older than your current installation"
            )
            % PACKAGE_NAME
        ) in result.output

    @patch("energinetml.cli.model.submit.backend")
    @patch.object(Model, "requirements", new_callable=MagicMock)
    def test__required_sdk_version_greater_than_current__should_echo_warning(
        self, model_requirements_mock, backend_mock, model_path, clusters_mock
    ):
        """
        :param Mock model_requirements_mock:
        :param Mock backend_mock:
        :param str model_path:
        """
        runner = CliRunner()

        model_requirements_mock.__contains__.return_value = True
        model_requirements_mock.get_version.return_value = Version("9999.9999.9999")

        backend_mock.get_compute_clusters.return_value = clusters_mock

        # Act
        result = runner.invoke(cli=submit, args=["--path", model_path])

        # Assert
        assert result.exit_code == 0
        assert (
            (
                "WARNING: Your requirements.txt file contains a version of "
                "%s (9999.9999.9999) which is newer than your current installation "
            )
            % PACKAGE_NAME
        ) in result.output

    @patch("energinetml.cli.model.submit.backend")
    @patch.object(Model, "requirements", new_callable=MagicMock)
    def test__should_submit_wait_and_download_files(
        self, model_requirements_mock, backend_mock, model_path, clusters_mock
    ):
        """
        :param Mock model_requirements_mock:
        :param Mock backend_mock:
        :param str model_path:
        """
        runner = CliRunner()

        model_requirements_mock.__contains__.return_value = True
        model_requirements_mock.get_version.return_value = Version("9999.9999.9999")

        context = Mock()

        backend_mock.submit_model.return_value = context
        backend_mock.get_compute_clusters.return_value = clusters_mock

        # Act
        result = runner.invoke(
            cli=submit,
            args=[
                "--path",
                model_path,
                "--wait",
                "--download",
                "parameter1",
                "parameter2",
            ],
        )

        # Assert
        assert result.exit_code == 0

        backend_mock.submit_model.assert_called_once_with(
            model=ANY, params=("parameter1", "parameter2")
        )

        context.wait_for_completion.assert_called_once()
        context.wait_for_completion.download_files()

    @patch("energinetml.cli.model.submit.backend")
    def test__verify_compute_cluster__should_prompt_user(
        self, backend_mock, model_path
    ):
        # Arrange
        cluster1 = Mock()
        cluster1.name = "cluster1"

        cluster2 = Mock()
        cluster2.name = "cluster2"
        cluster2.vm_size = VM_SIZE

        mock_clusters = [cluster1, cluster2]
        backend_mock.get_compute_clusters.return_value = mock_clusters

        backend_mock.get_workspace.return_value = Mock()
        backend_mock.submit_model.return_value = Mock()

        runner = CliRunner()

        # Act
        result = runner.invoke(
            cli=submit,
            args=[
                "--path",
                model_path,
            ],
            # Select cluster2 as the new cluster
            input="cluster2",
        )

        # Assert
        assert result.exit_code == 0
        assert (
            f"Could not find compute target '{COMPUTE_TARGET}' in "
            "the available compute targets: ['cluster1', 'cluster2']."
        ) in result.output

        # Check that cluster2 was selected.
        with open(f"{model_path}/{Model._CONFIG_FILE_NAME}", "r") as f:
            model_json = json.load(f)

        assert model_json["compute_target"] == "cluster2"

    @patch("energinetml.cli.model.submit.backend")
    def test__verify_compute_cluster__should_be_silent(self, backend_mock, model_path):
        # Arrange
        cluster1 = Mock()
        cluster1.name = COMPUTE_TARGET
        cluster1.vm_size = VM_SIZE

        cluster2 = Mock()
        cluster2.name = "cluster2"

        mock_clusters = [cluster1, cluster2]
        backend_mock.get_compute_clusters.return_value = mock_clusters
        backend_mock.get_workspace.return_value = Mock()
        backend_mock.submit_model.return_value = Mock()

        runner = CliRunner()

        # Act
        result = runner.invoke(
            cli=submit,
            args=[
                "--path",
                model_path,
            ],
        )

        # Assert
        assert result.exit_code == 0
        assert (
            f"Could not find compute target '{COMPUTE_TARGET}'"
        ) not in result.output

    @patch("energinetml.cli.model.submit.backend")
    def test__verify_vm_size__mismatching_vm_sizes_should_abort(
        self, backend_mock, model_path
    ):
        # Arrange
        cluster1 = Mock()
        cluster1.name = COMPUTE_TARGET
        cluster1.vm_size = "not the right vm size"
        mock_clusters = [cluster1]

        backend_mock.get_compute_clusters.return_value = mock_clusters
        backend_mock.get_workspace.return_value = Mock()
        backend_mock.submit_model.return_value = Mock()

        runner = CliRunner()

        # Act
        result = runner.invoke(
            cli=submit,
            args=[
                "--path",
                model_path,
            ],
        )

        # Assert
        assert result.exit_code == 1
        assert (
            "WARNING: The VM size (vm-size) specified in "
            f"{Model._CONFIG_FILE_NAME} does "
            "not match the actual VM size of the compute cluster "
            "(not the right vm size)."
        ) in result.output

    @patch("energinetml.cli.model.submit.backend")
    def test__verify_vm_size__matching_vm_sizes_should_be_silent(
        self, backend_mock, model_path
    ):
        # Arrange
        cluster1 = Mock()
        cluster1.name = COMPUTE_TARGET
        cluster1.vm_size = VM_SIZE
        mock_clusters = [cluster1]

        backend_mock.get_compute_clusters.return_value = mock_clusters
        backend_mock.get_workspace.return_value = Mock()
        backend_mock.submit_model.return_value = Mock()

        runner = CliRunner()

        # Act
        result = runner.invoke(
            cli=submit,
            args=[
                "--path",
                model_path,
            ],
        )

        # Assert
        assert result.exit_code == 0
        assert (
            f"WARNING: The VM size specified in {Model._CONFIG_FILE_NAME} does "
            "not match the actual VM size of the compute cluster."
        ) not in result.output
