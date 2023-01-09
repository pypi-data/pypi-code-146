"""Tests for the workflow CLI."""

import click
import pytest
from click.testing import CliRunner

from chime_frb_api.modules.buckets import Buckets
from chime_frb_api.workflow import Work
from chime_frb_api.workflow.cli import cli

BUCKETS_KWARGS = {"debug": True, "base_url": "http://localhost:8000"}


@pytest.fixture()
def buckets():
    """Create a Buckets instance."""
    buckets = Buckets(**BUCKETS_KWARGS)
    # flush any existing Work objects
    if "workflow-tests" in buckets.pipelines():
        buckets.delete_many("workflow-tests", force=True)
    yield buckets
    buckets.delete_many("workflow-tests", force=True)


@pytest.fixture()
def work():
    """Create a Work instance."""
    return Work(pipeline="workflow-tests")


def test_workflow_import():
    """Test that the task module can be imported."""
    from chime_frb_api.workflow import pipeline  # noqa: F401


def invoke_run(func_name: str, lifetime: int = 1):
    """Invoke the run command with the given arguments."""
    return CliRunner().invoke(
        cli,
        [
            "run",
            "workflow-tests",
            "chime_frb_api.tests.test_workflow." + func_name,
            "--lifetime=%i" % lifetime,
            "--base-urls=http://localhost:8000",
            "--site=local",
            "--sleep-time=1",
            "--log-level=DEBUG",
        ],
    )


def test_success(buckets, work):
    """Test that a successful task is marked as such."""
    assert work.deposit(**BUCKETS_KWARGS)
    result = invoke_run("sleep_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["success"] == 1


def test_multi_success(buckets, work):
    """Test that a successful task is marked as such."""
    assert work.deposit()
    assert work.deposit()
    result = invoke_run("sleep_func", lifetime=2)
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["success"] == 2


def test_timeout(buckets, work):
    """Test that a task that times out is marked as such."""
    work.parameters = {"s": 2}
    work.timeout = 1
    assert work.deposit()
    result = invoke_run("sleep_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["failure"] == 1


def test_failing_func(buckets, work):
    """Test that a failing task is marked as such."""
    assert work.deposit()
    result = invoke_run("failing_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["failure"] == 1


def test_noncompliant_func(buckets, work):
    """Test that a noncompliant task is marked as such."""
    assert work.deposit()
    result = invoke_run("noncompliant_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["failure"] == 1


def test_bad_imports(buckets, work):
    """Test that a task with bad imports is marked as such."""
    assert work.deposit()
    result = invoke_run("nonexisting_func")
    assert result.exit_code == 1
    assert buckets.status("workflow-tests")["queued"] == 1


def test_click_func(buckets, work):
    """Test that a click function can be run."""
    assert work.deposit()
    result = invoke_run("click_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["success"] == 1


def test_bad_base_url():
    """Test that a bad base URL is handled correctly."""
    result = CliRunner().invoke(
        cli,
        [
            "run",
            "workflow-tests",
            "chime_frb_api.tests.test_workflow.sleep_func",
            "--lifetime=1",
            "--base-urls=http://localhost:9000",
            "--site=local",
            "--sleep-time=1",
            "--log-level=DEBUG",
        ],
    )
    assert result.exit_code == 1


def sleep_func(**kwargs):
    """Sleep for a given number of seconds."""
    from time import sleep

    sleep(kwargs.get("s", 0.1))
    return {}, [], []


def failing_func(**kwargs):
    """Raise an exception."""
    raise ValueError


def noncompliant_func(**kwargs):
    """Return a non-compliant result."""
    return True


@click.command()
@click.option("--opt", default=1)
def click_func(opt):
    """A click function."""
    return {}, [], []
