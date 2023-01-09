import json
from pathlib import Path
from typing import List, Optional, Union
from unittest import mock

import PIL.Image
import pytest

from cinnaroll_internal.io_formats import (
    ALLOWED_INFER_FUNC_INPUT_FORMATS,
    ALLOWED_INFER_FUNC_OUTPUT_FORMATS,
    IMG,
    JSON,
    DisallowedInferFuncInputFormatError,
    DisallowedInferFuncOutputFormatError,
    InferFuncInputFormatMismatchError,
    InferFuncOutputFormatMismatchError,
    find_disallowed_io_format_errors,
    find_infer_func_input_format_mismatch_error,
    find_infer_func_output_format_mismatch_error,
)
from tests.unit import utils


class Inputs:
    def __init__(self) -> None:
        self.valid_json = [{"zaba": 5, "pies": 3, "kot": -1}, {"orzel": 15, "nosorozec": 10}]
        self.invalid_json = "not a valid JSON string"

        img_file = Path(__file__).parent / "test_data" / "cifar-example.jpg"
        self.img = PIL.Image.open(img_file)


class TestIOFormats:
    test_find_disallowed_io_format_cases = [
        ("file", "json", []),
        ("json", "img",
            [
                DisallowedInferFuncOutputFormatError(
                    f"img is not an allowed infer func output format. "
                    f"You can choose from one of: {ALLOWED_INFER_FUNC_OUTPUT_FORMATS}"
                )
            ],
         ),
        (
            "foo",
            "json",
            [
                DisallowedInferFuncInputFormatError(
                    f"foo is not an allowed infer func input format. "
                    f"You can choose from one of: {ALLOWED_INFER_FUNC_INPUT_FORMATS}"
                )
            ],
        ),
        (
            "file",
            "baz",
            [
                DisallowedInferFuncOutputFormatError(
                    f"baz is not an allowed infer func output format. "
                    f"You can choose from one of: {ALLOWED_INFER_FUNC_OUTPUT_FORMATS}"
                )
            ],
        ),
        (
            "foo",
            "baz",
            [
                DisallowedInferFuncInputFormatError(
                    f"foo is not an allowed infer func input format. "
                    f"You can choose from one of: {ALLOWED_INFER_FUNC_INPUT_FORMATS}"
                ),
                DisallowedInferFuncOutputFormatError(
                    f"baz is not an allowed infer func output format. "
                    f"You can choose from one of: {ALLOWED_INFER_FUNC_OUTPUT_FORMATS}"
                ),
            ],
        ),
    ]

    @pytest.mark.parametrize(
        "infer_func_input_format, infer_func_output_format, expected",
        test_find_disallowed_io_format_cases,
    )
    def test_find_disallowed_io_format_errors(
        self,
        infer_func_input_format: str,
        infer_func_output_format: str,
        expected: List[Exception],
    ) -> None:
        got = find_disallowed_io_format_errors(
            infer_func_input_format, infer_func_output_format
        )
        assert len(expected) == len(got)
        if len(expected):
            utils.assert_contains_exceptions(expected, got)

    test_find_infer_func_input_format_mismatch_error_when_input_is_json_cases = [
        (json.dumps({"number": 3}), None),
        (
            "invalid json",
            InferFuncInputFormatMismatchError(
                "Input in json format needs to be a string containing valid JSON "
                "that can be decoded with json.loads(). Here is the error encountered "
                "while trying to json.loads() provided input: "
            ),
        ),
    ]

    @pytest.mark.parametrize(
        "input_sample, expected",
        test_find_infer_func_input_format_mismatch_error_when_input_is_json_cases,
    )
    def test_find_infer_func_input_format_mismatch_error_when_input_is_json(
        self, input_sample: str, expected: Optional[Exception]
    ) -> None:
        got = find_infer_func_input_format_mismatch_error(input_sample, "json")
        utils.assert_optional_exception_like(expected, got)

    test_find_infer_func_input_format_mismatch_error_when_input_is_file_type_cases = [
        ("file", None, None),
        ("img", None, None),
        (
            "file",
            PermissionError(),
            InferFuncInputFormatMismatchError(
                "Input in file format needs to be path to a file that can be opened. "
                "Here is the error encountered while trying to open provided file: "
            ),
        ),
        (
            "img",
            PermissionError(),
            InferFuncInputFormatMismatchError(
                "Input in img format needs to be path to a file that can be opened. "
                "Here is the error encountered while trying to open provided file: "
            ),
        ),
    ]

    @pytest.mark.parametrize(
        "input_format, side_effect, expected",
        test_find_infer_func_input_format_mismatch_error_when_input_is_file_type_cases,
    )
    def test_find_infer_func_input_format_mismatch_error_when_input_is_file_type(
        self,
        input_format: str,
        side_effect: Optional[Exception],
        expected: Optional[Exception],
    ) -> None:
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            mock_file.side_effect = side_effect
            got = find_infer_func_input_format_mismatch_error(
                "somefile.png", input_format
            )
            utils.assert_optional_exception_like(expected, got)

    @pytest.mark.parametrize(
        "inp, format, expected_outcome",
        [
            ("valid_json", JSON, None),
            ("invalid_json", JSON, InferFuncOutputFormatMismatchError()),
            ("img", IMG, None),
            ("valid_json", IMG, InferFuncOutputFormatMismatchError()),
        ],
    )
    def test_find_infer_func_output_format_mismatch_error(
        self,
        inp: Union[str, PIL.Image.Image],
        format: str,
        expected_outcome: Optional[Exception],
    ) -> None:
        test_inputs = Inputs()

        outcome = find_infer_func_output_format_mismatch_error(
            getattr(test_inputs, inp), format
        )

        if outcome is None:
            assert True
        else:
            assert isinstance(outcome, type(expected_outcome))
