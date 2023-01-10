from __future__ import annotations

import time

import betamax
import pytest
from click.testing import CliRunner

import itkdb
from itkdb import commandline


@pytest.fixture(scope="function")
def recorder_session(auth_user, monkeypatch):
    monkeypatch.setattr(commandline._session, "user", auth_user)
    with betamax.Betamax(
        commandline._session,
        cassette_library_dir=itkdb.settings.ITKDB_CASSETTE_LIBRARY_DIR,
    ) as recorder:
        yield recorder


def test_commandline():
    assert commandline._session
    assert commandline._session.user


def test_version():
    runner = CliRunner()
    start = time.time()
    result = runner.invoke(commandline.itkdb, ["--version"])
    end = time.time()
    elapsed = end - start
    assert result.exit_code == 0
    assert itkdb.__version__ in result.stdout
    # make sure it took less than a second
    assert elapsed < 1.0


def test_authenticate(recorder_session):
    runner = CliRunner()
    result = runner.invoke(commandline.itkdb, ["authenticate"])
    assert result.exit_code == 0
    assert "You have signed in as" in result.output


def test_stats(recorder_session):
    recorder_session.use_cassette("test_stats.test_get", record="none")
    runner = CliRunner()
    result = runner.invoke(commandline.itkdb, ["stats"])
    assert result.exit_code == 0
    assert result.output


def test_listInstitutions(recorder_session):
    recorder_session.use_cassette("test_institution.test_get", record="none")
    runner = CliRunner()
    result = runner.invoke(commandline.itkdb, ["list-institutes"])
    assert result.exit_code == 0
    assert result.output


def test_listComponentTypes(recorder_session):
    recorder_session.use_cassette("test_components.test_get", record="none")
    runner = CliRunner()
    result = runner.invoke(commandline.itkdb, ["list-component-types"])
    assert result.exit_code == 0
    assert result.output


def test_listComponents(recorder_session):
    recorder_session.use_cassette(
        "test_components.test_list_componentsv2", record="none"
    )
    runner = CliRunner()
    result = runner.invoke(commandline.itkdb, ["list-components"])
    assert result.exit_code == 0
    assert result.output

    recorder_session.use_cassette(
        "test_components.test_list_components_componentTypev2", record="none"
    )
    runner = CliRunner()
    result = runner.invoke(
        commandline.itkdb, ["list-components", "--component-type", "HYBRID"]
    )
    assert result.exit_code == 0
    assert result.output


def test_listAllAttachments(recorder_session):
    recorder_session.use_cassette(
        "test_attachments.test_list_all_attachments", record="none"
    )
    runner = CliRunner()
    result = runner.invoke(commandline.itkdb, ["list-all-attachments"])
    assert result.exit_code == 0
    assert result.output


def test_listProjects(recorder_session):
    recorder_session.use_cassette("test_projects.test_list_projects", record="none")
    runner = CliRunner()
    result = runner.invoke(commandline.itkdb, ["list-projects"])
    assert result.exit_code == 0
    assert result.output


def test_listTestTypes(recorder_session):
    recorder_session.use_cassette("test_tests.test_list_test_types", record="none")
    runner = CliRunner()
    result = runner.invoke(
        commandline.itkdb, ["list-test-types", "--component-type", "HYBRID"]
    )
    assert result.exit_code == 0
    assert result.output


def test_getComponentInfoByCode(recorder_session):
    recorder_session.use_cassette(
        "test_components.test_get_component_info_code", record="none"
    )
    runner = CliRunner()
    result = runner.invoke(
        commandline.itkdb,
        ["get-component-info", "--component", "54f134b9975bebc851c4671d0ccbb489"],
    )
    assert result.exit_code == 0
    assert result.output


def test_getComponentInfoBySerial(recorder_session):
    recorder_session.use_cassette(
        "test_components.test_get_component_info_serial", record="none"
    )
    runner = CliRunner()
    result = runner.invoke(
        commandline.itkdb, ["get-component-info", "--component", "20USE000000086"]
    )
    assert result.exit_code == 0
    assert result.output


def test_getSummary(recorder_session):
    recorder_session.use_cassette("test_summary.test_get_summary", record="none")
    runner = CliRunner()
    result = runner.invoke(commandline.itkdb, ["summary", "--project", "S"])
    assert result.exit_code == 0
    assert result.output


def test_addAttachment(recorder_session, tmp_path):
    temp = tmp_path / "test.txt"
    temp.write_text("this is a fake attachment for testing purposes")

    recorder_session.use_cassette("test_attachments.test_add_attachment", record="none")
    runner = CliRunner()
    result = runner.invoke(
        commandline.itkdb,
        [
            "add-attachment",
            "--component",
            "20USE000000086",
            "--title",
            '"this is a test attachment"',
            "-d",
            '"delete this attachment if you see it"',
            "-f",
            temp,
        ],
    )
    assert result.exit_code == 0
    assert result.output


def test_addComment(recorder_session):
    recorder_session.use_cassette("test_components.test_add_comment", record="none")
    runner = CliRunner()
    result = runner.invoke(
        commandline.itkdb,
        [
            "add-comment",
            "--component",
            "20USE000000086",
            "--message",
            '"this is a test message"',
        ],
    )

    assert result.exit_code == 0
    assert result.output
