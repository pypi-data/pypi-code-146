from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.api.json import ActivityTargetType

if TYPE_CHECKING:
    from logging import Logger

    from vectice.api import Client


def _get_last_asset(target_type: ActivityTargetType, client: Client, _logger: Logger):
    try:
        last_asset = client.get_last_assets([target_type.value], {"index": 1, "size": 1}).list[0]
        return last_asset
    except IndexError as e:
        _logger.debug(f"There were no assets with activity found. Sanity check {e}")
        return


def _formatting(longest, string):
    if longest != string:
        return " " * ((len(longest) - len(string)) // 2)
    else:
        return ""


def _get_last_used_assets_and_logging(client: Client, _logger: Logger, current_workspace: str):
    try:
        asset = _get_last_asset(ActivityTargetType.Iteration, client, _logger)
        iteration = client.get_iteration(asset["targetId"])
        last_assets = client.get_iteration_last_assets(iteration.id)
    except Exception as e:
        _logger.warning(
            "No Iteration exists with activity. When an Iteration is created, last used assets will be displayed."
        )
        _logger.debug(f"Sanity Check: No Iteration exists with activity.\n{e}")
        return
    workspace_name = last_assets.phase["parent"]["workspace"]["name"]
    if workspace_name != current_workspace:
        _logger.warning(
            "No Iteration exists with activity. When an Iteration is created, last used assets will be displayed."
        )
        return
    project_name = last_assets.phase["parent"]["name"]
    phase_name = last_assets.phase.name
    iteration_index = last_assets.index
    steps = sorted([step for step in last_assets.steps if step.completed is False], key=lambda x: x["updatedDate"])  # type: ignore[no-any-return]
    try:
        step_name = steps[0].name if steps else ""
    except IndexError:
        step_name = ""
    _logger.info("Assets with Latest Activity   Asset Type    Name")
    _logger.info(f"Assets with Latest Activity   Project       '{project_name}'")
    _logger.info(f"Assets with Latest Activity   Phase         '{phase_name}'")
    _logger.info(f"Assets with Latest Activity   Iteration      {iteration_index}")
    _logger.info(f"Assets with Latest Activity   Step          '{step_name}'")
