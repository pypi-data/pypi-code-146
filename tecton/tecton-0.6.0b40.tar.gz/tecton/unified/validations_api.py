from enum import Enum
from typing import List
from typing import Tuple

from colorama import Fore
from typeguard import typechecked

from tecton import version as tecton_version
from tecton._internals import metadata_service
from tecton.unified import common as unified_common
from tecton_core import errors
from tecton_core import id_helper
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import repo_metadata_pb2
from tecton_proto.data import state_update_pb2
from tecton_proto.metadataservice import metadata_service_pb2


class ValidationMode(str, Enum):
    EXPLICIT = "explicit"
    AUTOMATIC = "auto"


# Copy of logic in engine.py - but using unified objects for notebook development.
def _get_declared_fco_args(
    objects: List[unified_common.BaseTectonObject],
) -> Tuple[List[fco_args_pb2.FcoArgs], repo_metadata_pb2.FeatureRepoSourceInfo]:
    all_args = []
    repo_source_info = repo_metadata_pb2.FeatureRepoSourceInfo()

    for fco_obj in objects:
        source_info = fco_obj._source_info
        source_info.fco_id.CopyFrom(id_helper.IdHelper.from_string(fco_obj.info.id))

        repo_source_info.source_info.append(source_info)
        all_args.append(fco_obj._build_args())

    return all_args, repo_source_info


# Copy of logic in error_utils.py - but using unified objects for notebook development.
def _format_server_errors(
    messages: List[state_update_pb2.ValidationMessage], objects: List[unified_common.BaseTectonObject]
):
    obj_by_id = {}
    for fco_obj in objects:
        obj_by_id[fco_obj.info.id] = fco_obj

    for m in messages:
        obj_id = id_helper.IdHelper.to_string(m.fco_refs[0].fco_id)
        obj = obj_by_id[obj_id]
        print(f"================ Error found in {obj.__class__.__name__} {obj.info.name} ================")
        print(Fore.RED + m.message + Fore.RESET)


@typechecked
def run_backend_validation(
    objects: List[unified_common.BaseTectonObject],
    timeout_seconds=90 * 60,
) -> bool:
    """Use the plan MDS endpoint to run validations from a notebook."""
    object_names = [obj.info.name for obj in objects]
    print(f"Performing validation for {', '.join(object_names)}.")
    fco_args, repo_source_info = _get_declared_fco_args(objects)
    workspace_name = "prod"  # Defaults to running plan endpoint on prod since the endpoint expects a valid workspace

    request_plan = metadata_service_pb2.NewStateUpdateRequest(
        blocking_dry_run_mode=True,
        request=state_update_pb2.StateUpdateRequest(
            workspace=workspace_name,
            upgrade_all=False,
            sdk_version=tecton_version.get_semantic_version() or "",
            fco_args=fco_args,
            repo_source_info=repo_source_info,
            suppress_recreates=False,
        ),
    )

    try:
        response_submit = metadata_service.instance().NewStateUpdate(request_plan)
        response_query = response_submit.eager_response
        if response_query.error:
            print("Validation has failed to run")
            print(response_query.error)
            return False
        if response_query.validation_result.errors:
            _format_server_errors(response_query.validation_result.errors, objects)
            print(f"Tecton objects: {', '.join(object_names)} have failed validation")
            return False
    except (
        errors.TectonInternalError,
        errors.TectonAPIValidationError,
    ) as e:
        print(e)
        return False

    print(f"Tecton objects: {', '.join(object_names)} have been succesfully validated!")
    return True
