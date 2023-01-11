import functools
import sys
from typing import Callable
from uuid import UUID, uuid4

import pytest
from _pytest.monkeypatch import MonkeyPatch
from click.testing import CliRunner

from sym.shared.cli.helpers import os as sym_os
from sym.shared.cli.tests.helpers.capture import CaptureCommand


@pytest.fixture(autouse=True)
def patch_execvp(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sym_os, "execvp", lambda client, args: client.exec(*args))


@pytest.fixture
def uuid() -> UUID:
    return uuid4()


@pytest.fixture
def uuid_factory() -> Callable[[], UUID]:
    return uuid4


@pytest.fixture
def capture_command(monkeypatch: MonkeyPatch) -> CaptureCommand:
    return CaptureCommand(monkeypatch)


@pytest.fixture
def wrapped_cli_runner():
    """Yield a click.testing.CliRunner to invoke the CLI."""
    class_ = CliRunner

    def invoke_wrapper(f):
        """Augment CliRunner.invoke to emit its output to stdout.

        This enables pytest to show the output in its logs on test
        failures. Otherwise, the isolated environment swallows everything.

        Seen here: https://github.com/pallets/click/issues/737

        Example:
            def command_login_tester_with_echo(click_setup):
                with click_setup() as runner:
                    result = runner.invoke(click_command, args, echo=True)
        """

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            echo = kwargs.pop("echo", False)
            result = f(*args, **kwargs)

            if echo is True:
                sys.stdout.write(result.output)

            return result

        return wrapper

    class_.invoke = invoke_wrapper(class_.invoke)
    cli_runner = class_()

    yield cli_runner


def _env_str(creds):
    return "\n".join([f"{k}={v}" for k, v in creds.items()]) + "\n"


@pytest.fixture
def creds_env():
    return {
        "AWS_REGION": "us-east-2",
        "AWS_ACCESS_KEY_ID": "ASIA4GNNUMIHHBPSAQC3",
        "AWS_SECRET_ACCESS_KEY": "xxx",
        "AWS_SESSION_TOKEN": "xxx",
        "AWS_OKTA_SESSION_EXPIRATION": "1600494616",
    }


@pytest.fixture
def creds_env_str(creds_env):
    return _env_str(creds_env)


@pytest.fixture
def env_creds(creds_env_str, capture_command: CaptureCommand):
    """Include this fixture to automatically stub the subprocess
    that retrieves credentials from the environment.

    Will only work when subprocess is executed with capture_command
    context. For example:

    def test_with_creds(env_creds, capture_command):
        with capture_command():
            execute thing that gets creds

    will successfully use this stub. However this will not:

    def test_with_creds(env_creds):
        execute thing that gets creds
    """
    capture_command.register_output(r"env", creds_env_str)


@pytest.fixture
def fake_creds_env():
    return {
        "AWS_REGION": "foobar",
        "AWS_FOOBAR": "baz",
        "AWS_OKTA_SESSION_EXPIRATION": "1600494616",
    }


@pytest.fixture
def fake_creds_env_str(fake_creds_env):
    return _env_str(fake_creds_env)
