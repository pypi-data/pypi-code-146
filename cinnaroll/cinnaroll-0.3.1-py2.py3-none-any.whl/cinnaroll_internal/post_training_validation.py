from typing import Any, Dict, List, Optional, Callable

from cinnaroll_internal import io_formats, model, rollout_config, utils

DATASET_KEY_NAME = "dataset"


class InferFunctionError(Exception):
    ...


class MetricsError(Exception):
    ...


def verify_infer_func_call_with_input_sample_infer_func(
    infer_func: Callable[[Any, Any], Any],
    model_object: Any,
    infer_func_input_sample: Any,
) -> Any:
    try:
        output = infer_func(model_object, infer_func_input_sample)
    except Exception as e:
        raise InferFunctionError(
            f"Passing infer_func_input_sample to infer_func yielded the following error. "
            f"Please correct the sample and/or infer_func. \n {e}"
        )
    return output


# this function needs to be refactored to comply with the current error handling policy
def find_config_post_training_errors(
    *, cinnaroll_model: model.CinnarollModel, config: rollout_config.RolloutConfig
) -> List[Exception]:
    errors: List[Exception] = []
    utils.append_if_not_none(
        errors, cinnaroll_model.find_model_input_sample_error(config.model_input_sample)
    )

    try:
        infer_func_output = verify_infer_func_call_with_input_sample_infer_func(
            config.infer, cinnaroll_model.model_object, config.infer_func_input_sample
        )
        utils.append_if_not_none(
            errors,
            io_formats.find_infer_func_output_format_mismatch_error(
                infer_func_output, config.infer_func_output_format
            ),
        )
    except InferFunctionError as e:
        errors.append(e)
    errors += find_metrics_post_training_errors(config.metrics)
    return errors


# metrics declaration should look like this:
# metrics = {
#   "dataset": "mnist_extended",
#   "f1": f1_val,
#   "accuracy": accuracy
# }
def find_metrics_post_training_errors(
    metrics: Optional[Dict[str, Any]]
) -> List[Exception]:
    errors: List[Exception] = []
    if metrics is None:
        return errors

    if isinstance(metrics, dict):
        if not all([isinstance(key, str) for key in metrics.keys()]):
            errors.append(
                MetricsError("All keys in the metrics dictionary must be strings.")
            )

        wrong_value_present = False
        for key, value in metrics.items():
            if key != DATASET_KEY_NAME and not isinstance(value, float):
                wrong_value_present = True
            if key == DATASET_KEY_NAME and not isinstance(value, str):
                wrong_value_present = False
        if wrong_value_present:
            errors.append(
                MetricsError(
                    "All values in the metrics dictionary must be floats, "
                    "except for optional 'dataset' key value which must be string."
                )
            )

        if any([x is None for x in metrics.values()]):
            errors.append(
                MetricsError(
                    "Values in the metrics dictionary cannot be None."
                )
            )
    else:
        errors.append(MetricsError("Object passed as metrics must be a dictionary."))

    return errors
