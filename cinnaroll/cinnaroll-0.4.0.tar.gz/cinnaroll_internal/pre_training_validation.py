from typing import Optional, Callable, Any, List

import requests

from cinnaroll_internal import constants, io_formats, model, rollout_config, utils, environment_check


class ConfigParameterUndefinedError(Exception):
    ...


class ProjectIDError(Exception):
    ...


class InferFunctionNotImplementedError(Exception):
    ...


class UnknownFrameworkError(Exception):
    ...


# todo: discuss endpoint and behavior with engineers
# fire a GET /projects/{projectID} request to backend
# 200 - everything is ok, 401 - API Key is wrong, 403 or 404 - project ID is wrong
def find_project_id_error(project_id: str) -> Optional[Exception]:
    headers = {
        constants.API_KEY_HEADER_KEY: environment_check.get_api_key()
    }
    try:
        response = requests.get(url=constants.BACKEND_BASE_URL + f"/modelUploads?projectId={project_id}",
                                headers=headers)
        if response.status_code == requests.codes.ok:
            return None
        elif response.status_code == requests.codes.unauthorized:
            return environment_check.WrongAPIKeyError()
        elif response.status_code in (requests.codes.not_found, requests.codes.forbidden):
            return ProjectIDError(f"Project with ID {project_id} doesn't exist. "
                                  f"Ensure you've pasted project ID correctly.")
        else:
            return ProjectIDError(f"Project ID validation returned status code {response.status_code} "
                                  f"and message: {response.text}")
    except requests.RequestException as e:
        return e


# it has some implementation if it isn't just pass
def find_infer_func_not_implemented_error(
    infer_func: Callable[[Any, Any], Any]
) -> Optional[Exception]:
    if not utils.is_function_implemented(infer_func):
        return InferFunctionNotImplementedError(
            "Infer function is not implemented. Implement it."
        )
    return None


# return errors if something besides metrics is missing (None)
def find_config_none_value_errors(
    config: rollout_config.RolloutConfig,
) -> List[Exception]:
    errors: List[Exception] = []

    config_parameters = {
        "project_id": config.project_id,
        "model_object": config.model_object,
        "infer_func_input_format": config.infer_func_input_format,
        "infer_func_output_format": config.infer_func_output_format,
        "model_input_sample": config.model_input_sample,
        "infer_func_input_sample": config.infer_func_input_sample,
    }
    for name, value in config_parameters.items():
        if value is None:
            errors.append(
                ConfigParameterUndefinedError(
                    f"Required config parameter {name} is undefined "
                    f"(its value is None)."
                )
            )

    return errors


def find_unknown_model_framework_error(model_object: Any) -> Optional[Exception]:
    if model.infer_framework(model_object) == constants.UNKNOWN_FRAMEWORK:
        return UnknownFrameworkError(
            f"Unknown machine learning framework used. Currently only "
            f"{constants.VALID_FRAMEWORKS} are supported."
        )
    return None


# are input_format and output_format recognizable?
# is infer func input sample in input_format?
# does infer func contain code?
def find_config_pre_training_errors(
    config: rollout_config.RolloutConfig,
) -> List[Exception]:
    errors: List[Exception] = []
    errors += find_config_none_value_errors(config)
    utils.append_if_not_none(errors, find_project_id_error(config.project_id))
    errors += io_formats.find_disallowed_io_format_errors(
        config.infer_func_input_format, config.infer_func_output_format
    )
    utils.append_if_not_none(
        errors,
        io_formats.find_infer_func_input_format_mismatch_error(
            config.infer_func_input_sample, config.infer_func_input_format
        ),
    )
    utils.append_if_not_none(
        errors, find_infer_func_not_implemented_error(config.infer)
    )

    if config.model_object:
        utils.append_if_not_none(
            errors, find_unknown_model_framework_error(config.model_object)
        )

    return errors
