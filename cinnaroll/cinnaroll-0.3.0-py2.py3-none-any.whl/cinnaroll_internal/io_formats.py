import json
from pathlib import Path
from typing import Any, List, Optional

import PIL.Image

# currently json string is assumed
JSON = "json"
FILE = "file"
IMG = "img"

ALLOWED_INFER_FUNC_INPUT_FORMATS = [JSON, FILE]
ALLOWED_INFER_FUNC_INPUT_EXTENSIONS = (".json", ".txt", ".jpg", ".jpeg", ".png")
ALLOWED_INFER_FUNC_OUTPUT_FORMATS = [JSON]

CHECK_ALLOWED_INFER_FUNC_INPUT_EXTENSIONS = False


class DisallowedInferFuncInputFormatError(Exception):
    ...


class DisallowedInferFuncOutputFormatError(Exception):
    ...


class InferFuncInputFormatMismatchError(Exception):
    ...


class InferFuncOutputFormatMismatchError(Exception):
    ...


def find_disallowed_io_format_errors(
    infer_func_input_format: str, infer_func_output_format: str
) -> List[Exception]:
    errors: List[Exception] = []
    if infer_func_input_format not in ALLOWED_INFER_FUNC_INPUT_FORMATS:
        errors.append(
            DisallowedInferFuncInputFormatError(
                f"{infer_func_input_format} is not an allowed infer func input format. "
                f"You can choose from one of: {ALLOWED_INFER_FUNC_INPUT_FORMATS}"
            )
        )
    if infer_func_output_format not in ALLOWED_INFER_FUNC_OUTPUT_FORMATS:
        errors.append(
            DisallowedInferFuncOutputFormatError(
                f"{infer_func_output_format} is not an allowed infer func output format. "
                f"You can choose from one of: {ALLOWED_INFER_FUNC_OUTPUT_FORMATS}"
            )
        )
    return errors


def find_infer_func_input_format_mismatch_error(
    infer_func_input_sample: Any, input_format: str
) -> Optional[Exception]:
    if input_format == JSON:
        try:
            _ = json.loads(infer_func_input_sample)
        except json.JSONDecodeError as e:
            return InferFuncInputFormatMismatchError(
                f"Input in {input_format} format needs to be a string containing valid JSON "
                f"that can be decoded with json.loads(). Here is the error encountered "
                f"while trying to json.loads() provided input: "
                f"{repr(e)}"
            )
    if input_format in (FILE, IMG):
        if not isinstance(infer_func_input_sample, str):
            return InferFuncInputFormatMismatchError(
                f"Input in {input_format} must be a string containing path to a file."
            )

        if (
            CHECK_ALLOWED_INFER_FUNC_INPUT_EXTENSIONS
            and Path(infer_func_input_sample).suffix
            not in ALLOWED_INFER_FUNC_INPUT_EXTENSIONS
        ):
            return InferFuncInputFormatMismatchError(
                f"We currently support files with the following extensions: {ALLOWED_INFER_FUNC_INPUT_EXTENSIONS}"
            )
        else:
            try:
                f = open(infer_func_input_sample, "r")
                f.close()
            except IOError as e:
                return InferFuncInputFormatMismatchError(
                    f"Input in {input_format} format needs to be path to a file that can be opened. "
                    f"Here is the error encountered while trying to open provided file: "
                    f"{repr(e)}"
                )
    return None


def find_infer_func_output_format_mismatch_error(
    infer_func_output: Any, output_format: str
) -> Optional[Exception]:
    if output_format == JSON:
        if not isinstance(infer_func_output, dict) and not isinstance(infer_func_output, list):
            return InferFuncOutputFormatMismatchError(
                f"When output_format is set to {JSON} infer function must return a JSON serializable "
                f"dictionary or list, that you can pass to json.dumps(). "
                f"Currently infer function returns an object of type {type(infer_func_output)}."
            )
        try:
            _ = json.dumps(infer_func_output)
        except json.JSONDecodeError as e:
            return InferFuncOutputFormatMismatchError(
                f"When output_format is set to {JSON} infer function must return a JSON serializable "
                f"dictionary or list, that you can pass to json.dumps(). Here is the error encountered "
                f"while trying to json.dumps() provided output: "
                f"{repr(e)}"
            )
    elif output_format == IMG:
        if not isinstance(infer_func_output, PIL.Image.Image):
            return InferFuncOutputFormatMismatchError(
                f"Output in {JSON} format needs to be an instance of PIL.Image.Image."
            )
    return None
