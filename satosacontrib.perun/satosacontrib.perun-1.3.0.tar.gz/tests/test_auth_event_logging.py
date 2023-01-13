import satosacontrib.perun.micro_services.auth_event_logging_microservice as ms
from unittest.mock import patch, MagicMock
from satosa.context import Context
from satosa.internal import InternalData
from satosa.micro_services.base import MicroService
from satosacontrib.perun.micro_services.auth_event_logging_microservice import (
    AuthEventLogging,
)
from tests.test_microservice_loader import Loader


MICROSERVICE_CONFIG = {
    "user_identifier": "user_id",
    "logging_db": "wholeconnectionstring",
    "path_to_geolite2_city": "path",
    "ip_address_header": "REMOTE_ADDR",
}

TEST_INTERNAL_RESPONSE = {
    "auth_info": {"issuer": "issuer", "auth_class_ref": "auth_class_ref"},
    "requester": "requester",
    "requester_name": [{"text": "name"}],
    "subject_id": "id",
}

TEST_CONTEXT_DATA = {
    "http_headers": {"User-Agent": "user_agent", "REMOTE_ADDR": "ip_addr"},
    "state": {"none": "none"},
}


class TestContext(Context):
    __test__ = False
    KEY_AUTHN_CONTEXT_CLASS_REF = "None"

    def __init__(self, state, http_headers):
        super().__init__()
        self.state = state
        self.http_headers = http_headers


class TestData(InternalData):
    __test__ = False

    def __init__(self, requester, requester_name, subject_id):
        super().__init__()
        self.auth_info = None
        self.requester = requester
        self.requester_name = requester_name
        self.subject_id = subject_id


class TestEngine:
    __test__ = False

    @staticmethod
    def connect():
        return TestCnxn()


class TestMetadata:
    __test__ = False

    bind = None


class TestCnxn:
    __test__ = False

    @staticmethod
    def execute(a):
        return a


TEST_DATA = TestData(
    TEST_INTERNAL_RESPONSE["requester"],
    TEST_INTERNAL_RESPONSE["requester_name"],
    TEST_INTERNAL_RESPONSE["subject_id"],
)
TEST_DATA.auth_info = TEST_INTERNAL_RESPONSE["auth_info"]

TEST_CONTEXT = TestContext(
    TEST_CONTEXT_DATA["state"], TEST_CONTEXT_DATA["http_headers"]
)

MICROSERVICE = Loader(
    MICROSERVICE_CONFIG, AuthEventLogging.__name__
).create_mocked_instance()


@patch(
    "satosacontrib.perun.micro_services.auth_event_logging_microservice."
    "AuthEventLogging._AuthEventLogging__get_id_from_foreign_table"
)
@patch(
    "satosacontrib.perun.micro_services.auth_event_logging_microservice."
    "AuthEventLogging._AuthEventLogging__get_id_from_identifier"
)
@patch(
    "satosacontrib.perun.micro_services.auth_event_logging_microservice."
    "AuthEventLogging._AuthEventLogging__get_location"
)
@patch("sqlalchemy.create_engine")
@patch("satosacontrib.perun.utils.AuthEventLoggingDbModels.Base")
@patch("satosa.micro_services.base.MicroService.process")
def test_microservice(
    mock_request_1,
    mock_request_2,
    mock_request_3,
    mock_request_4,
    mock_request_5,
    mock_request_6,
):
    AuthEventLogging._AuthEventLogging__get_id_from_foreign_table = MagicMock(
        side_effect=[1, 2, 3, 4, 5, 6, 7]
    )
    AuthEventLogging._AuthEventLogging__get_id_from_identifier = MagicMock(
        side_effect=[1, 2]
    )
    AuthEventLogging._AuthEventLogging__get_location = MagicMock(
        return_value={"city": "city", "country": "country"}
    )
    ms.create_engine = MagicMock(return_value=TestEngine())
    ms.Base.metadata = MagicMock(return_value=TestMetadata())
    MicroService.process = MagicMock(return_value=None)

    result = MICROSERVICE.process(TEST_CONTEXT, TEST_DATA)
    assert result is None
