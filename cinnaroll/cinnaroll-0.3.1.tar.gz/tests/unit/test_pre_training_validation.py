import pytest
from typing import Callable, Any, Optional, List

from cinnaroll_internal import pre_training_validation, rollout_config
from tests.unit import utils


class ClassWithImplementedInfer:
    # some comment
    """
    multiline comment
    """
    # some comment
    @staticmethod
    def infer(model_object: Any, input_data: Any) -> None:
        # some comment
        """
        multiline comment
        """
        # some comment
        print("some code")


class ClassWithPassInfer:
    # some comment
    """
    multiline comment
    """
    # some comment
    @staticmethod
    def infer(model_object: Any, input_data: Any) -> None:
        # some comment
        """
        multiline comment
        """
        # some comment
        pass


class ClassWithDotInfer:
    # some comment
    """
    multiline comment
    """
    # some comment
    @staticmethod
    def infer(model_object: Any, input_data: Any) -> None:
        # some comment
        """
        multiline comment
        """
        # some comment
        ...


class ClassWithSameLineDotInfer:
    # some comment
    """
    multiline comment
    """
    # some comment
    @staticmethod
    # fmt: off
    def infer(model_object: Any, input_data: Any) -> None: ...  # noqa: E704
    # fmt: on


implemented_infer = ClassWithImplementedInfer.infer
pass_infer = ClassWithPassInfer.infer
dot_infer = ClassWithDotInfer.infer
same_line_dot_infer = ClassWithSameLineDotInfer.infer


def test_verify_infer_func_is_implemented_returns_none_if_infer_is_implemented() -> None:
    err = pre_training_validation.find_infer_func_not_implemented_error(
        implemented_infer
    )
    assert err is None


@pytest.mark.parametrize("infer_func", (pass_infer, dot_infer, same_line_dot_infer))
def test_verify_infer_func_is_implemented_returns_error_if_infer_is_empty(
    infer_func: Callable[[Any, Any], Any]
) -> None:
    err: Optional[
        Exception
    ] = pre_training_validation.find_infer_func_not_implemented_error(infer_func)
    assert isinstance(err, pre_training_validation.InferFunctionNotImplementedError)
    assert err.args == ("Infer function is not implemented. Implement it.",)


class Config(rollout_config.RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> None:
        ...

    @staticmethod
    def infer(model_object: Any, input_data: Any) -> Any:
        ...


test_find_config_none_value_errors_cases = [
    (
        Config(
            project_id="something",
            model_name="something",
            model_object="something",
            infer_func_input_format="something",
            infer_func_output_format="something",
            model_input_sample="something",
            infer_func_input_sample="something",
        ),
        [],
    ),
    (
        Config(
            project_id=None,  # type: ignore
            model_name=None,
            model_object=None,
            infer_func_input_format=None,  # type: ignore
            infer_func_output_format=None,  # type: ignore
            model_input_sample=None,
            infer_func_input_sample=None,
        ),
        [
            pre_training_validation.ConfigParameterUndefinedError(
                "Required config parameter project_id is undefined (its value is None)."
            ),
            pre_training_validation.ConfigParameterUndefinedError(
                "Required config parameter model_object is undefined (its value is None)."
            ),
            pre_training_validation.ConfigParameterUndefinedError(
                "Required config parameter infer_func_input_format is undefined (its value is None)."
            ),
            pre_training_validation.ConfigParameterUndefinedError(
                "Required config parameter infer_func_output_format is undefined (its value is None)."
            ),
            pre_training_validation.ConfigParameterUndefinedError(
                "Required config parameter model_input_sample is undefined (its value is None)."
            ),
            pre_training_validation.ConfigParameterUndefinedError(
                "Required config parameter infer_func_input_sample is undefined (its value is None)."
            ),
        ],
    ),
]


@pytest.mark.parametrize(
    "config, expected_errors", test_find_config_none_value_errors_cases
)
def test_find_config_none_value_errors(
    config: rollout_config.RolloutConfig, expected_errors: List[Exception]
) -> None:
    got = pre_training_validation.find_config_none_value_errors(config)
    assert len(got) == len(expected_errors)
    utils.assert_contains_exceptions(expected_errors, got)


# PROJECT_ID = "123123123"
# test_find_project_id_error_when_response_arrives_cases = [
#     (requests.codes.ok, "", None),
#     (requests.codes.unauthorized, "", environment_check.WrongAPIKeyError()),
#     (requests.codes.forbidden, "", pre_training_validation.ProjectIDError(
#         f"Project with ID {PROJECT_ID} doesn't exist. "
#         f"Ensure you've pasted project ID correctly.")),
#     (requests.codes.not_found, "", pre_training_validation.ProjectIDError(
#         f"Project with ID {PROJECT_ID} doesn't exist. "
#         f"Ensure you've pasted project ID correctly.")),
#     (requests.codes.internal_server_error, "There was an error processing the request.",
#      pre_training_validation.ProjectIDError(
#          f"Project ID validation returned status code {requests.codes.internal_server_error} "
#          f"and message: There was an error processing the request.")),
# ]


# @mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
# @mock.patch("cinnaroll_internal.pre_training_validation.requests.get")
# @pytest.mark.parametrize("status_code, text, expected", test_find_project_id_error_when_response_arrives_cases)
# def test_find_project_id_error_when_response_arrives(
#         mock_get: mock.MagicMock, status_code: int, text: str, expected: Optional[Exception]) -> None:
#     mock_get.return_value.status_code = status_code
#     mock_get.return_value.text = text
#     got = pre_training_validation.find_project_id_error(PROJECT_ID)
#     utils.assert_optional_exception_equals(expected, got)
#
#
# @mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
# @mock.patch("cinnaroll_internal.pre_training_validation.requests.get")
# def test_find_project_id_error_when_request_errors_out(mock_get: mock.MagicMock) -> None:
#     mock_get.side_effect = requests.ConnectTimeout()
#     got = pre_training_validation.find_project_id_error(PROJECT_ID)
#     utils.assert_optional_exception_equals(requests.RequestException(), got)

# @mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
# @mock.patch("cinnaroll_internal.pre_training_validation.requests.get")
# def test_find_config_pre_training_errors_when_it_should_return_multiple_errors(mock_get: mock.MagicMock) -> None:
#     config = TestConfig(
#         project_id="abc321",
#         model_object=None,
#         infer_func_input_format="unimplemented format",
#         infer_func_output_format="unimplemented format",
#         model_input_sample=None,
#         infer_func_input_sample=None,
#         )
#
#     mock_get.return_value.status_code = requests.codes.not_found
#     got = pre_training_validation.find_config_pre_training_errors(config)
#     assert len(got)
