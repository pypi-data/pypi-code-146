import json
from datetime import datetime, timezone
from urllib.parse import parse_qs

from loguru import logger
from pydantic import AnyHttpUrl, parse_obj_as
from pytest import mark, raises

from saxo_apy.models import OpenAPIAppConfig
from saxo_apy.utils import (
    configure_logger,
    construct_auth_url,
    decode_streaming_message,
    make_default_session_headers,
    unix_seconds_to_datetime,
    validate_redirect_url,
)
from saxo_apy.version import VERSION

from .fixtures.models import DUMMY_LIVE_CONFIG, DUMMY_SIM_CONFIG


def test_logger_setup() -> None:
    configure_logger(log_sink="log.txt", log_level="DEBUG")
    logger_config = str(logger)
    assert "id=1" in logger_config
    assert "level=10" in logger_config
    assert "sink='log.txt" in logger_config


def test_make_default_session_headers() -> None:
    headers = make_default_session_headers()

    expected_headers = {
        "accept-encoding": "gzip",
        "user-agent": f"saxo-apy/{VERSION}",
        "connection": "keep-alive",
        "cache-control": "no-cache",
        "accept": "application/json; charset=utf-8",
    }
    for header, value in headers.items():
        assert value == expected_headers[header]


@mark.parametrize(
    "unix, datetime",
    [
        (1, datetime(1970, 1, 1, 0, 0, 1, tzinfo=timezone.utc)),
        (2, datetime(1970, 1, 1, 0, 0, 2, tzinfo=timezone.utc)),
        (2657175467, datetime(2054, 3, 15, 8, 17, 47, tzinfo=timezone.utc)),
    ],
)
def test_unix_seconds_to_datetime(unix: int, datetime: datetime) -> None:
    assert datetime == unix_seconds_to_datetime(unix)


def test_validate_redirect_url() -> None:
    config = parse_obj_as(OpenAPIAppConfig, DUMMY_SIM_CONFIG)

    # test default to first localhost if None provided
    assert "http://localhost:12321/redirect1" == validate_redirect_url(config, None)

    # test selecting a valid redirect_url from config
    assert "http://example.net:12321/redirect" == validate_redirect_url(
        config, config.redirect_urls[2]
    )

    # test selecting invalid redirect_url
    with raises(AssertionError, match="not available in app config"):
        validate_redirect_url(
            config,
            parse_obj_as(AnyHttpUrl, "http://example.net:12321/invalid-redirect"),
        )


@mark.parametrize(
    "config",
    [
        (DUMMY_SIM_CONFIG),
        (DUMMY_LIVE_CONFIG),
    ],
)
def test_construct_auth_url(config: dict) -> None:
    _config = parse_obj_as(OpenAPIAppConfig, config)
    auth_url = construct_auth_url(_config, _config.redirect_urls[0], "state123")
    querystring = parse_qs(auth_url.query)
    assert querystring["response_type"][0] == _config.grant_type.value.lower()
    assert querystring["client_id"][0] == _config.client_id
    assert querystring["state"][0] == "state123"
    assert querystring["redirect_uri"][0] == _config.redirect_urls[0]


def test_decode_streaming_message() -> None:
    msg_bytes = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06refids\x00\x9f\x00\x00\x00{"LastUpdated":"2022-11-16T09:18:53.349000Z","MarketDepth":{"Ask":[1.04199,1.042],"Bid":[1.04169,1.04168]},"Quote":{"Ask":1.04199,"Bid":1.04169,"Mid":1.04184}}'  # noqa

    msg = decode_streaming_message(msg_bytes)
    assert msg.msg_id == 1
    assert msg.ref_id == "refids"
    assert msg.ts
    assert type(msg.ts) == datetime
    assert msg.data == json.loads(
        '{"LastUpdated":"2022-11-16T09:18:53.349000Z","MarketDepth":{"Ask":[1.04199,1.042],"Bid":[1.04169,1.04168]},"Quote":{"Ask":1.04199,"Bid":1.04169,"Mid":1.04184}}'  # noqa
    )

    msg_bytes_bad = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06refids\x01\x9f\x00\x00\x00{"LastUpdated":"2022-11-16T09:18:53.349000Z","MarketDepth":{"Ask":[1.04199,1.042],"Bid":[1.04169,1.04168]},"Quote":{"Ask":1.04199,"Bid":1.04169,"Mid":1.04184}}'  # noqa
    with raises(RuntimeError):
        decode_streaming_message(msg_bytes_bad)
