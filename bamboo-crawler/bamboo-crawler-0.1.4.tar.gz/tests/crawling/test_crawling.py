import os
import subprocess

import pytest


@pytest.fixture
def web_server_environment() -> None:  # type: ignore
    overwrite_envs = {
        "FLASK_ENV": "development",
        "WERKZEUG_RUN_MAIN": "true",
    }
    recovery_values = {
        name: os.environ.get(name) for name in overwrite_envs.keys()
    }
    os.environ.update(overwrite_envs)
    yield
    for k, v in recovery_values.items():
        if v is None:
            del os.environ[k]
        else:
            os.environ[k] = v


@pytest.fixture
def target_web_server(web_server_environment) -> None:  # type: ignore
    server = subprocess.Popen(
        [
            "python",
            "-m",
            "http.server",
            "8000",
            "--directory",
            "tests/crawling/assets",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    yield
    server.stderr.close()  # type: ignore
    server.stdout.close()  # type: ignore
    server.kill()
    server.wait()


def test_crawling(target_web_server) -> None:  # type: ignore
    c = subprocess.run(
        [
            "python",
            "-m",
            "bamboo_crawler",
            "-r",
            "tests/crawling/recipe.yml",
            "-t",
            "index_html",
        ],
        stdout=subprocess.PIPE,
    )
    assert c.returncode == 0, "success"
    assert c.stdout == b"<body>test!test!test!</body>\n", "crawling"
