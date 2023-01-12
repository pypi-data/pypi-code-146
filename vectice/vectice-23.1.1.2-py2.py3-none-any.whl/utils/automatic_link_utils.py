from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.api.json.iteration import (
    IterationStatus,
    IterationStepArtifact,
    IterationStepArtifactInput,
    IterationStepArtifactType,
)

if TYPE_CHECKING:
    from logging import Logger

    from vectice.models import Iteration, Phase, Project, Step
    from vectice.models.datasource.datawrapper import DataWrapper


def existing_dataset_logger(data: dict, dataset_name: str, _logger: Logger):
    if data["useExistingDataset"]:
        existing_dataset_version = f"Dataset: {dataset_name}"
        if data["useExistingVersion"]:
            existing_dataset_version += f" with Version: {data['datasetVersion']['name']}"
        _logger.info(f"{existing_dataset_version} already exists.")


def existing_model_logger(data: dict, model_name: str, _logger: Logger):
    """
    registerModel does not return useExistingVersion
    """
    if data["useExistingModel"]:
        _logger.info(f"Model: {model_name} already exists.")


def get_active_step(client, phase_id: int):
    """
    Get the current active iteration and the ordered step to continue with.
    """
    return sorted(
        [step for step in client.list_steps(phase_id) if step.completed is False],
        key=lambda x: x.index,  # type: ignore[no-any-return]
    )


def use_step_or_active_step(
    iteration: Iteration, client, phase_id, _logger, data_source, data, step: Step | None = None
):
    refresh_step = iteration.step(step.name) if step else None
    if refresh_step and refresh_step.completed is False:
        step_id, step_name = refresh_step.id, refresh_step.name
        step_artifacts = refresh_step.artifacts if refresh_step.artifacts else []
    else:
        active_steps = get_active_step(client, phase_id)
        if len(active_steps) >= 1:
            step_id, step_name = active_steps[0].id, active_steps[0].name
            step_artifacts = active_steps[0].artifacts
        else:
            _logger.warning(
                f"There are no active steps to attach the registered Dataset(name='{data_source.name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type=MODELING) to."
            )
            return
    return step_id, step_name, step_artifacts


def handle_phase_level(client, data_source: DataWrapper, data: dict, _logger: Logger, phase_id: int, iteration):
    step = iteration._current_step
    step_id, step_name, step_artifacts = use_step_or_active_step(
        iteration, client, phase_id, _logger, data_source, data, step
    )
    return step_id, step_name, step_artifacts


def handle_project_level(client, data_source: DataWrapper, data: dict, _logger: Logger, phase_id: int, iteration):
    logging.getLogger("vectice.models.project").propagate = True
    step = iteration._current_step
    step_id, step_name, step_artifacts = use_step_or_active_step(
        iteration, client, phase_id, _logger, data_source, data, step
    )
    return step_id, step_name, step_artifacts


def check_active_iteration(client, phase_id: int, _logger: Logger, iteration: Iteration | None = None):
    refresh_iteration = client.get_iteration(iteration.id) if iteration else None
    if not refresh_iteration or (
        refresh_iteration.status == IterationStatus.Abandoned or refresh_iteration.status == IterationStatus.Completed
    ):
        iterations = client.list_iterations(phase_id)
        active_iteration = None
        for item in iterations:
            if item.status == IterationStatus.NotStarted or item.status == IterationStatus.InProgress:
                active_iteration = item
        if not active_iteration:
            _logger.warning("There is no active iteration to link asset to.")
            return
        return active_iteration
    return refresh_iteration


def link_dataset_to_step(
    step_artifact: IterationStepArtifactInput,
    data_source: DataWrapper,
    data: dict,
    _logger: Logger,
    project: Project | None = None,
    phase: Phase | None = None,
):
    """
    1. We get the current phase if it exists
        - No phase results in a warning / failure (We can't assume phases are ordinal so this fails/exits)
        - We need a phase to be called at some point at the very least
    2. We get the current iteration if it exists e.g a user did phase.iteration()
        - No iteration results in us getting one/creating one.
    3. We get the current step if it exists e.g a user did iteration.step()
    3. If there is no current step
        - We check if the iteration has any steps that are not completed.
    """
    if project:
        client = project._client
        if project._phase:
            phase_id = project._phase.id
            iteration = project._phase._current_iteration
        else:
            _logger.warning("No phase has been selected in the session.")
            return
        iteration_check = check_active_iteration(client, phase_id, _logger, iteration)
        if not iteration_check:
            return
        elif not iteration:
            iteration = project._phase.iteration()
        step_id, step_name, step_artifacts = handle_project_level(
            client, data_source, data, _logger, phase_id, iteration
        )
        client = project._client
        dataset_type = "ORIGIN"
    elif phase:
        iteration, client, phase_id = phase._current_iteration, phase._client, phase.id
        iteration_check = check_active_iteration(client, phase_id, _logger, iteration)
        if not iteration_check:
            return
        elif not iteration:
            iteration = phase.iteration()
        step_id, step_name, step_artifacts = handle_phase_level(client, data_source, data, _logger, phase_id, iteration)
        dataset_type = "CLEAN"
    else:
        raise RuntimeError("Vectice Error: Failed to provision level for automatic asset link.")

    match_dataset_assets = [
        artifact
        for artifact in step_artifacts
        if artifact.type == IterationStepArtifactType.DataSetVersion and artifact.dataset_version_id == step_artifact.id
    ]
    if len(step_artifacts) == 0 or (len(step_artifacts) >= 1 and not any(match_dataset_assets)):
        step_output = client.add_iteration_step_artifact(step_id, step_artifact)
        _logger.info(
            f"Successfully added Dataset(name='{data_source.name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type={dataset_type}) to {step_output.name}"
        )
    elif len(step_artifacts) >= 1 and any(match_dataset_assets):
        _logger.info(
            f"The step {step_name} already has Dataset(name='{data_source.name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type={dataset_type}) linked."
        )
    else:
        _logger.warning(
            f"There are no active steps to attach the registered Dataset(name='{data_source.name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type={dataset_type}) to."
        )
        return


def link_assets_to_step(
    iteration: Iteration,
    step_artifact: IterationStepArtifactInput,
    name: str,
    data: dict,
    _logger: Logger,
    attachments: list[IterationStepArtifactInput] | None = None,
):
    """
    1. We get the current step if it exists e.g a user did iteration.step()
    2. If there is no current step
        - We check if the iteration has any steps that are not completed.
    """
    client, phase_id = iteration._client, iteration._phase.id
    iteration_check = check_active_iteration(client, phase_id, _logger, iteration)
    if not iteration_check:
        return
    step = iteration._current_step
    refresh_step = iteration.step(step.name) if step else None
    if refresh_step and refresh_step.completed is False:
        step_id, step_name = refresh_step.id, refresh_step.name
        refresh_step = iteration.step(step_name)
        step_artifacts = refresh_step.artifacts if refresh_step.artifacts else []
    else:
        active_steps = get_active_step(client, phase_id)
        if len(active_steps) >= 1:
            step_id, step_name = active_steps[0].id, active_steps[0].name
            step_artifacts = active_steps[0].artifacts
        else:
            _logger.warning("There are no active steps to attach the registered asset.")
            return
    if step_artifact.type == "DataSetVersion":
        _dataset_link_and_logger(client, step_artifact, step_artifacts, name, data, step_name, step_id, _logger)
    elif step_artifact.type == "ModelVersion":
        _model_link_and_logger(client, step_artifact, step_artifacts, name, data, step_name, step_id, _logger)
    else:
        raise RuntimeError("Vectice Error: The step artifact type was not set.")
    if attachments:
        _attachment_link_and_logger(client, attachments, step_artifacts, name, data, step_name, step_id, _logger)


def _dataset_link_and_logger(
    client,
    step_artifact: IterationStepArtifactInput,
    step_artifacts: list[IterationStepArtifact],
    name: str,
    data: dict,
    step_name: str,
    step_id: int,
    _logger: Logger,
):
    check_assets = [artifact for artifact in step_artifacts if artifact.type == IterationStepArtifactType.ModelVersion]
    match_dataset_assets = [
        artifact
        for artifact in step_artifacts
        if artifact.type == IterationStepArtifactType.DataSetVersion and artifact.dataset_version_id == step_artifact.id
    ]
    if (len(step_artifacts) == 0 or len(step_artifacts) == len(check_assets)) or (
        len(step_artifacts) >= 1 and not any(match_dataset_assets)
    ):
        step_output = client.add_iteration_step_artifact(step_id, step_artifact)
        _logger.info(
            f"Successfully added Dataset(name='{name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type=MODELING) to {step_output.name}"
        )
    elif len(step_artifacts) >= 1 and any(match_dataset_assets):
        _logger.info(
            f"The step {step_name} already has Dataset(name='{name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type=MODELING) linked."
        )
    else:
        raise RuntimeError("Vectice Error: The dataset link failed")


def _model_link_and_logger(
    client,
    step_artifact: IterationStepArtifactInput,
    step_artifacts: list[IterationStepArtifact],
    name: str,
    data: dict,
    step_name: str,
    step_id: int,
    _logger: Logger,
):
    check_assets = [
        artifact for artifact in step_artifacts if artifact.type == IterationStepArtifactType.DataSetVersion
    ]
    match_model_assets = [
        artifact
        for artifact in step_artifacts
        if artifact.type == IterationStepArtifactType.ModelVersion and artifact.model_version_id == step_artifact.id
    ]
    if (len(step_artifacts) == 0 or len(step_artifacts) == len(check_assets)) or (
        len(step_artifacts) >= 1 and not any(match_model_assets)
    ):
        step_output = client.add_iteration_step_artifact(step_id, step_artifact)
        _logger.info(
            f"Successfully added Model(name='{name}', version='{data['modelVersion']['name']}') to {step_output.name}"
        )
    elif len(step_artifacts) >= 1 and any(match_model_assets):
        _logger.info(
            f"The step {step_name} already has Model(name='{name}', version='{data['modelVersion']['name']}') linked."
        )
    else:
        raise RuntimeError("Vectice Error: The model link failed")


def _attachment_link_and_logger(
    client,
    attachments: list[IterationStepArtifactInput],
    step_artifacts: list[IterationStepArtifact],
    name: str,
    data: dict,
    step_name: str,
    step_id: int,
    _logger: Logger,
):
    check_assets = [artifact for artifact in step_artifacts if artifact.type == IterationStepArtifactType.EntityFile]
    for attachment in attachments:
        match_attachment_assets = [
            artifact
            for artifact in step_artifacts
            if artifact.type == IterationStepArtifactType.EntityFile
            and artifact.entity_file_id == attachment.entity_file_id
        ]
        if (len(step_artifacts) == 0 or len(step_artifacts) == len(check_assets)) or (
            len(step_artifacts) >= 1 and not any(match_attachment_assets)
        ):
            attachment.pop("entityFileId")
            step_output = client.add_iteration_step_artifact(step_id, attachment)
            _logger.info(
                f"Successfully added Attachment: {attachment.id} from Model(name='{name}', version='{data['modelVersion']['name']}') to {step_output.name}"
            )
        elif len(step_artifacts) >= 1 and any(match_attachment_assets):
            _logger.info(
                f"The step {step_name} already has Attachment: {attachment.id} from Model(name='{name}', version='{data['modelVersion']['name']}') linked."
            )
        else:
            raise RuntimeError("Vectice Error: The attachment link failed")
