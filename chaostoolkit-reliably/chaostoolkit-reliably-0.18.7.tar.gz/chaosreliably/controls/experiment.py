import json
import os
from typing import Any, Dict, Optional, cast

from chaoslib.run import EventHandlerRegistry, RunEventHandler
from chaoslib.types import (
    Configuration,
    Experiment,
    Journal,
    Schedule,
    Secrets,
    Settings,
)
from logzero import logger

from chaosreliably import RELIABLY_HOST, get_session

__all__ = ["configure_control"]


class ReliablyHandler(RunEventHandler):  # type: ignore
    def __init__(
        self,
        org_id: str,
        exp_id: str,
    ) -> None:
        RunEventHandler.__init__(self)
        self.org_id = org_id
        self.exp_id = exp_id
        self.exec_id = None

    def running(
        self,
        experiment: Experiment,
        journal: Journal,
        configuration: Configuration,
        secrets: Secrets,
        schedule: Schedule,
        settings: Settings,
    ) -> None:
        self.configuration = configuration
        self.secrets = secrets

        try:
            result = create_run(
                self.org_id,
                self.exp_id,
                experiment,
                journal,
                self.configuration,
                self.secrets,
            )

            if result:
                payload = result
                extension = get_reliably_extension_from_journal(journal)

                self.exec_id = payload["id"]
                logger.debug(f"Reliably execution: {self.exec_id}")

                host = self.secrets.get(
                    "host", os.getenv("RELIABLY_HOST", RELIABLY_HOST)
                )

                url = f"https://{host}/executions/view/?id={self.exec_id}&exp={self.exp_id}"  # noqa
                extension["execution_url"] = url

                add_runtime_extra(extension)
                set_plan_status(
                    self.org_id,
                    "running",
                    None,
                    self.configuration,
                    self.secrets,
                )
        except Exception as ex:
            set_plan_status(
                self.org_id, "error", str(ex), self.configuration, self.secrets
            )

    def finish(self, journal: Journal) -> None:
        try:
            complete_run(
                self.org_id,
                self.exp_id,
                self.exec_id,
                journal,
                self.configuration,
                self.secrets,
            )
            set_plan_status(
                self.org_id,
                "completed",
                None,
                self.configuration,
                self.secrets,
            )
        except Exception as ex:
            set_plan_status(
                self.org_id, "error", str(ex), self.configuration, self.secrets
            )


def configure_control(
    experiment: Experiment,
    event_registry: EventHandlerRegistry,
    exp_id: str,
    org_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    logger.debug("Configure Reliably's experiment control")
    event_registry.register(ReliablyHandler(org_id, exp_id))


###############################################################################
# Private functions
###############################################################################
def create_run(
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


def complete_run(
    org_id: str,
    exp_id: str,
    execution_id: Optional[str],
    state: Journal,
    configuration: Configuration,
    secrets: Secrets,
) -> Optional[Dict[str, Any]]:
    with get_session(configuration, secrets) as session:
        resp = session.put(
            f"/{org_id}/experiments/{exp_id}/executions/{execution_id}/results",
            json={"result": json.dumps(state)},
        )
        if resp.status_code != 200:
            logger.error("Failed to update results on server")
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
