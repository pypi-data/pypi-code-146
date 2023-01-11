import json
import os
from typing import Any, Dict, Optional, cast

from chaoslib.types import Configuration, Experiment, Journal, Secrets
from logzero import logger

from chaosreliably import RELIABLY_HOST, get_session

__all__ = ["after_experiment_control", "before_experiment_control"]


def before_experiment_control(
    context: Experiment,
    exp_id: str,
    org_id: str,
    state: Journal,
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    set_plan_status(org_id, "running", None, configuration, secrets)


def after_experiment_control(
    context: Experiment,
    exp_id: str,
    org_id: str,
    state: Journal,
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    try:
        result = complete_run(
            org_id, exp_id, context, state, configuration, secrets
        )

        if result:
            payload = result
            extension = get_reliably_extension_from_journal(state)

            exec_id = payload["id"]

            host = secrets.get(
                "host", os.getenv("RELIABLY_HOST", RELIABLY_HOST)
            )

            url = f"https://{host}/executions/view/?id={exec_id}&exp={exp_id}"
            extension["execution_url"] = url

            add_runtime_extra(extension)
            set_plan_status(org_id, "completed", None, configuration, secrets)
    except Exception as ex:
        set_plan_status(org_id, "error", str(ex), configuration, secrets)


###############################################################################
# Private functions
###############################################################################
def complete_run(
    org_id: str,
    exp_id: str,
    experiment: Experiment,
    state: Journal,
    configuration: Configuration,
    secrets: Secrets,
) -> Optional[Dict[str, Any]]:
    with get_session(configuration, secrets) as session:
        resp = session.post(
            f"/{org_id}/experiments/{exp_id}/executions",
            json={"result": json.dumps(state)},
        )
        if resp.status_code == 201:
            return cast(Dict[str, Any], resp.json())
    return None


def get_reliably_extension_from_journal(journal: Journal) -> Dict[str, Any]:
    experiment = journal.get("experiment")
    extensions = experiment.setdefault("extensions", [])
    for extension in extensions:
        if extension["name"] == "reliably":
            return cast(Dict[str, Any], extension)

    extension = {"name": "reliably"}
    extensions.append(extension)
    return cast(Dict[str, Any], extension)


def add_runtime_extra(extension: Dict[str, Any]) -> None:
    extra = os.getenv("RELIABLY_EXECUTION_EXTRA")
    if not extra:
        return

    try:
        extension["extra"] = json.loads(extra)
    except Exception:
        pass


def set_plan_status(
    org_id: str,
    status: str,
    message: Optional[str],
    configuration: Configuration,
    secrets: Secrets,
) -> None:
    plan_id = os.getenv("RELIABLY_PLAN_ID")
    if not plan_id:
        return None

    with get_session(configuration, secrets) as session:
        r = session.put(
            f"/{org_id}/plans/{plan_id}/status",
            json={"status": status, "error": message},
        )
        if r.status_code > 399:
            logger.debug(
                f"Failed to set plan status: {r.status_code}: {r.json()}"
            )
