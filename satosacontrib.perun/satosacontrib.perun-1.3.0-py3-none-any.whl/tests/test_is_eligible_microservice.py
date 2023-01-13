import copy
import logging
from datetime import datetime
from unittest.mock import patch, MagicMock

from dateutil.relativedelta import relativedelta
from freezegun import freeze_time
from satosa.context import Context
from satosa.internal import InternalData
from satosa.micro_services.base import MicroService

from satosacontrib.perun.micro_services.is_eligible_microservice import (
    IsEligible,
)
from tests.test_microservice_loader import Loader

DATE_NOW = datetime.fromisoformat("2022-01-30 12:00:00")

ONE_HOUR_OLD_TIMESTAMP = int(datetime.timestamp(DATE_NOW - relativedelta(hours=1)))
ONE_DAY_OLD_TIMESTAMP = int(datetime.timestamp(DATE_NOW - relativedelta(days=1)))
THIRTY_ONE_DAYS_OLD_TIMESTAMP = int(
    datetime.timestamp(DATE_NOW - relativedelta(days=31))
)
TWO_DAYS_OLD_TIMESTAMP = int(datetime.timestamp(DATE_NOW - relativedelta(days=2)))
SIX_MONTHS_OLD_TIMESTAMP = int(datetime.timestamp(DATE_NOW - relativedelta(months=6)))
TWO_YEARS_OLD_TIMESTAMP = int(datetime.timestamp(DATE_NOW - relativedelta(years=2)))

SUPPORTED_ELIGIBILITY_TYPE_1 = "eligibility_type_1"
SUPPORTED_ELIGIBILITY_TYPE_2 = "eligibility_type_2"
SUPPORTED_ELIGIBILITY_TYPE_3 = "eligibility_type_3"
SUPPORTED_ELIGIBILITY_TYPE_4 = "eligibility_type_4"
SUPPORTED_ELIGIBILITY_TYPE_5 = "eligibility_type_5"
SUPPORTED_ELIGIBILITY_TYPE_6 = "eligibility_type_6"
UNSUPPORTED_ELIGIBILITY_TYPE = "unsupported_eligibility_type"

PREFIX_1_A = "example_prefix_1_a"
PREFIX_1_B = "example_prefix_1_b"
PREFIX_2 = "example_prefix_2"
PREFIX_3_A = "example_prefix_3_a"
PREFIX_3_B = "example_prefix_3_b"
PREFIX_3_C = "example_prefix_3_b"
PREFIX_4 = "example_prefix_4"
PREFIX_5 = "example_prefix_5"
PREFIX_6 = "example_prefix_6"

TARGET_ATTRIBUTES = ["example_target_1", "example_target_2"]
DEFAULT_TARGET_ATTRIBUTE = "eduPersonAssurance"

ELIGIBILITY_TIMESTAMPS_DICT = {
    SUPPORTED_ELIGIBILITY_TYPE_1: ONE_HOUR_OLD_TIMESTAMP,
    SUPPORTED_ELIGIBILITY_TYPE_2: TWO_DAYS_OLD_TIMESTAMP,
    SUPPORTED_ELIGIBILITY_TYPE_3: SIX_MONTHS_OLD_TIMESTAMP,
    SUPPORTED_ELIGIBILITY_TYPE_4: TWO_YEARS_OLD_TIMESTAMP,
    SUPPORTED_ELIGIBILITY_TYPE_5: ONE_DAY_OLD_TIMESTAMP,
    SUPPORTED_ELIGIBILITY_TYPE_6: THIRTY_ONE_DAYS_OLD_TIMESTAMP,
    UNSUPPORTED_ELIGIBILITY_TYPE: ONE_HOUR_OLD_TIMESTAMP,
}
ELIGIBILITY_TIMESTAMPS_DICT_ATTR_NAME = "eligibility_timestamps_dict_attr"
NO_TARGET_ATTRS_CONFIGURED_INFO_MESSAGE = (
    "No target attributes configured. "
    "Calculated eligibility can't be "
    "stored. Skipping this service. "
    "You can try configuring "
    "<target_attributes> in "
    "microservice config."
)
NO_TIMESTAMPS_DICT_ATTR_INFO_MESSAGE = "No eligibility timestamps found. Skipping this service. Attribute {self.__eligibility_timestamps_dict_attribute} might be missing in provided data"

MICROSERVICE_CONFIG = {
    "target_attributes": TARGET_ATTRIBUTES,
    "eligibility_timestamps_dict_attribute": ELIGIBILITY_TIMESTAMPS_DICT_ATTR_NAME,
    "supported_eligibility_types": {
        SUPPORTED_ELIGIBILITY_TYPE_1: {
            "prefixes": [PREFIX_1_A, PREFIX_1_B],
            "suffixes": {"1d": 1, "1m": 31, "1y": 365},
        },
        SUPPORTED_ELIGIBILITY_TYPE_2: {
            "prefixes": [PREFIX_2],
            "suffixes": {"1d": 1, "1m": 31, "1y": 365},
        },
        SUPPORTED_ELIGIBILITY_TYPE_3: {
            "prefixes": [PREFIX_3_A, PREFIX_3_B, PREFIX_3_C],
            "suffixes": {"1d": 1, "1m": 31, "1y": 365},
        },
        SUPPORTED_ELIGIBILITY_TYPE_4: {
            "prefixes": [PREFIX_4],
            "suffixes": {
                "1d": 1,
                "1m": 31,
                "1y": 365,
            },
        },
        SUPPORTED_ELIGIBILITY_TYPE_5: {
            "prefixes": [PREFIX_5],
            "suffixes": {
                "1d": 1,
                "1m": 31,
                "1y": 365,
            },
        },
        SUPPORTED_ELIGIBILITY_TYPE_6: {
            "prefixes": [PREFIX_6],
            "suffixes": {
                "1m": 31,
                "1y": 365,
            },
        },
    },
}
EXPECTED_ELIGIBILITY_DATA = {
    SUPPORTED_ELIGIBILITY_TYPE_1: [
        f"{PREFIX_1_A}-1d",
        f"{PREFIX_1_B}-1d",
        f"{PREFIX_1_A}-1m",
        f"{PREFIX_1_B}-1m",
        f"{PREFIX_1_A}-1y",
        f"{PREFIX_1_B}-1y",
    ],
    SUPPORTED_ELIGIBILITY_TYPE_2: [f"{PREFIX_2}-1m", f"{PREFIX_2}-1y"],
    SUPPORTED_ELIGIBILITY_TYPE_3: [
        f"{PREFIX_3_A}-1y",
        f"{PREFIX_3_B}-1y",
        f"{PREFIX_3_C}-1y",
    ],
    SUPPORTED_ELIGIBILITY_TYPE_5: [
        f"{PREFIX_5}-1d",
        f"{PREFIX_5}-1m",
        f"{PREFIX_5}-1y",
    ],
    SUPPORTED_ELIGIBILITY_TYPE_6: [f"{PREFIX_6}-1m", f"{PREFIX_6}-1y"],
}

MICROSERVICE = Loader(MICROSERVICE_CONFIG, IsEligible.__name__).create_mocked_instance()


def test_process_data_with_empty_attrs(caplog):
    data_without_attrs = InternalData()
    data_without_attrs.attributes = {}

    with caplog.at_level(logging.INFO):
        MICROSERVICE.process(Context(), data_without_attrs)

        assert NO_TIMESTAMPS_DICT_ATTR_INFO_MESSAGE in caplog.text


def test_process_data_with_empty_timestamps_dict_attr(caplog):
    data_without_timestamps_dict_attrs = InternalData()
    data_without_timestamps_dict_attrs.attributes = {
        ELIGIBILITY_TIMESTAMPS_DICT_ATTR_NAME: {}
    }

    with caplog.at_level(logging.INFO):
        MICROSERVICE.process(Context(), data_without_timestamps_dict_attrs)

        assert NO_TIMESTAMPS_DICT_ATTR_INFO_MESSAGE in caplog.text


@freeze_time(DATE_NOW)
@patch("satosa.micro_services.base.MicroService.process")
def test_process_data_with_empty_target_attrs(mock_request_1):
    data_without_target_attrs = InternalData()
    data_without_target_attrs.attributes = {
        ELIGIBILITY_TIMESTAMPS_DICT_ATTR_NAME: ELIGIBILITY_TIMESTAMPS_DICT
    }

    config_without_target_attrs = copy.deepcopy(MICROSERVICE_CONFIG)
    config_without_target_attrs["target_attributes"] = []
    microservice = Loader(
        config_without_target_attrs, IsEligible.__name__
    ).create_mocked_instance()

    # Extract modified attributes passed to a mocked parent class
    MicroService.process = MagicMock(side_effect=lambda context, data: data.attributes)
    result = microservice.process(Context(), data_without_target_attrs)
    computed_eligibility_data = result.get(DEFAULT_TARGET_ATTRIBUTE)
    print("Computed result", computed_eligibility_data)

    MicroService.process.assert_called()
    assert computed_eligibility_data == EXPECTED_ELIGIBILITY_DATA


@freeze_time(DATE_NOW)
@patch("satosa.micro_services.base.MicroService.process")
def test_compute_valid_eligibilities(mock_request_1):
    data_with_multiple_eligibility_types = InternalData()
    data_with_multiple_eligibility_types.attributes = {
        ELIGIBILITY_TIMESTAMPS_DICT_ATTR_NAME: ELIGIBILITY_TIMESTAMPS_DICT
    }

    # Extract modified attributes passed to a mocked parent class
    MicroService.process = MagicMock(side_effect=lambda context, data: data.attributes)

    result = MICROSERVICE.process(Context(), data_with_multiple_eligibility_types)

    MicroService.process.assert_called()
    for target_attr in TARGET_ATTRIBUTES:
        computed_eligibility_data = result.get(target_attr)
        assert computed_eligibility_data is not None
        assert UNSUPPORTED_ELIGIBILITY_TYPE not in computed_eligibility_data.keys()
        assert SUPPORTED_ELIGIBILITY_TYPE_4 not in computed_eligibility_data.keys()
        assert computed_eligibility_data == EXPECTED_ELIGIBILITY_DATA
