import json
import os
import os.path
import pkgutil
import shutil
import subprocess
import tempfile
from typing import Any, Dict, Optional, cast
from urllib.parse import urlparse

from chaoslib import decode_bytes
from chaoslib.exceptions import ActivityFailed, InvalidActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

__all__ = ["inject_gradual_traffic_into_endpoint"]


def inject_gradual_traffic_into_endpoint(
    endpoint: str,
    step_duration: int = 5,
    step_additional_vu: int = 1,
    vu_per_second_rate: int = 1,
    test_duration: int = 30,
    results_json_filepath: Optional[str] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Load traffic into the given `endpoint`. Uses an approach that creates an
    incremental load into the endpoint rather than swarming it. The point of
    this action is to ensure your endpoint is active while you perform another
    action. This you means you likely want to run this action in the
    `background`.

    You may set a bearer token if your application uses one to authenticate.
    Pass `test_bearer_token` as a secret key in the `secrets` payload.

    This action return a dictionary payload of the load test results.
    """
    u = urlparse(endpoint)
    if not u.scheme or not u.netloc:
        raise InvalidActivity("endpoint must be a proper url")

    script = pkgutil.get_data(
        "chaosreliably", "activities/load/scripts/step_load_test.py"
    )
    if not script:
        raise ActivityFailed("failed to locate load-test script")

    locust_path = shutil.which("locust")
    if not locust_path:
        raise ActivityFailed("missing load test dependency")

    env = {
        "RELIABLY_LOCUST_ENDPOINT": endpoint,
        "RELIABLY_LOCUST_STEP_TIME": str(step_duration),
        "RELIABLY_LOCUST_STEP_LOAD": str(step_additional_vu),
        "RELIABLY_LOCUST_SPAWN_RATE": str(vu_per_second_rate),
        "RELIABLY_LOCUST_TIME_LIMIT": str(test_duration),
    }

    secrets = secrets or {}
    test_bearer_token = secrets.get("test_bearer_token")
    if test_bearer_token:
        env["RELIABLY_LOCUST_ENDPOINT_TOKEN"] = test_bearer_token

    with tempfile.TemporaryDirectory() as d:
        locustfile_path = os.path.join(d, "locustfile.py")
        with open(locustfile_path, mode="wb") as f:
            f.write(script)

        cmd = [
            locust_path,
            "--host",
            "localhost:8089",
            "--locustfile",
            locustfile_path,
            "--json",
            "--headless",
            "--loglevel",
            "INFO",
            "--exit-code-on-error",
            "0",
        ]
        try:
            p = subprocess.run(
                cmd,
                timeout=test_duration + 5,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                shell=False,
                cwd=d,
            )
            os.remove(locustfile_path)
        except subprocess.TimeoutExpired:
            raise ActivityFailed("load test took too long to complete")

        stdout = decode_bytes(p.stdout)
        stderr = decode_bytes(p.stderr)

        logger.debug(f"locust exit code: {p.returncode}")
        logger.debug(f"locust stderr: {stderr}")

        if results_json_filepath:
            with open(results_json_filepath, "w") as f:
                f.write(stdout)

        return cast(Dict[str, Any], json.loads(stdout))
