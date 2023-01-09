from typing import List

import pytest

from cinnaroll_internal import constants, environment_info

PYTORCH_REQUIREMENTS = [
    "requests-oauthlib==1.3.1",
    "rsa==4.9",
    "setuptools==65.4.0",
    "torch==1.12.1",
]

test_get_framework_version_cases = [
    (
        constants.TENSORFLOW,
        [
            "tensorboard-plugin-wit==1.8.1",
            "tensorflow-estimator==2.10.0",
            "tensorflow-macos==2.10.0",
        ],
        "2.10.0",
    ),
    (
        constants.KERAS,
        [
            "tensorboard-plugin-wit==1.8.1",
            "tensorflow-estimator==2.10.0",
            "tensorflow-macos==2.10.0",
        ],
        "2.10.0",
    ),
    (
        constants.KERAS,
        [
            "tensorflow-estimator==2.10.0",
            "tensorflow==2.10.0",
        ],
        "2.10.0",
    ),
    (constants.PYTORCH, PYTORCH_REQUIREMENTS, "1.12.1"),
]


@pytest.mark.parametrize(
    "framework, requirements, expected_framework_version",
    test_get_framework_version_cases,
)
def test_get_framework_version_when_framework_is_known(
    framework: str, requirements: List[str], expected_framework_version: str
) -> None:
    got = environment_info._get_framework_version(framework, requirements)
    assert got == expected_framework_version


def test_get_framework_version_when_framework_is_unknown() -> None:
    with pytest.raises(environment_info.UnknownFrameworkError):
        environment_info._get_framework_version(
            "definitely not a known framework", PYTORCH_REQUIREMENTS
        )


def test_get_framework_version_when_framework_package_is_not_found_in_requirements() -> None:
    with pytest.raises(environment_info.FrameworkPackageNotFoundError):
        environment_info._get_framework_version(constants.KERAS, PYTORCH_REQUIREMENTS)
