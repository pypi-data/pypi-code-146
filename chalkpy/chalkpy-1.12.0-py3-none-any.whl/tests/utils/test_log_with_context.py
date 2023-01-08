import concurrent.futures
import logging
from typing import Any, List, cast

import pytest

from chalk.utils.log_with_context import add_logging_context, get_logger


@pytest.fixture
def logger(caplog: pytest.LogCaptureFixture):
    with caplog.at_level(logging.INFO, "test_logger"):
        yield get_logger("test_logger")


def test_add_logging_context(logger: logging.Logger, caplog: pytest.LogCaptureFixture):
    """Test that :py:class:`add_logging_context` works."""
    logger.info("1")
    records = cast(List[Any], caplog.records)
    assert records[-1].message == "1"

    with add_logging_context(a=1, k={"hello": "world"}):
        logger.info("2")
        assert records[-1].message == "2"
        assert records[-1].a == 1
        assert records[-1].k == {"hello": "world"}

        with add_logging_context(b=2, k={"foo": "bar"}):
            logger.info("3")
            assert records[-1].message == "3"
            assert records[-1].a == 1
            assert records[-1].b == 2
            assert records[-1].k == {"hello": "world", "foo": "bar"}

            with add_logging_context(a=4, c=3, k={"hello": "world2", "biz": "baz"}):
                logger.info("4")
                assert records[-1].message == "4"
                assert records[-1].a == 4
                assert records[-1].b == 2
                assert records[-1].c == 3
                assert records[-1].k == {"hello": "world2", "foo": "bar", "biz": "baz"}

            logger.info("5")
            assert records[-1].message == "5"
            assert records[-1].a == 1
            assert records[-1].b == 2
            assert records[-1].k == {"hello": "world", "foo": "bar"}
            assert not hasattr(records[-1], "c")

        logger.info("6")
        assert records[-1].message == "6"
        assert records[-1].a == 1
        assert records[-1].k == {"hello": "world"}
        assert not hasattr(records[-1], "b")
        assert not hasattr(records[-1], "c")

    logger.info("7")
    assert records[-1].message == "7"
    assert not hasattr(records[-1], "a")
    assert not hasattr(records[-1], "b")
    assert not hasattr(records[-1], "c")


def test_inline_extra(logger: logging.Logger, caplog: pytest.LogCaptureFixture):
    """Test that we can add one-off additions to our context."""
    logger.info("message", extra={"hello": "world"})
    records = cast(List[Any], caplog.records)
    assert records[-1].message == "message"
    assert records[-1].hello == "world"

    with add_logging_context(foo="bar"):
        logger.info("message", extra={"hello": "world"})
        assert records[-1].message == "message"
        assert records[-1].hello == "world"
        assert records[-1].foo == "bar"


def test_thread_local(logger: logging.Logger, caplog: pytest.LogCaptureFixture):
    """Test that our logging context is indeed thread-local."""

    def thread_worker(val: int):
        records = cast(List[Any], caplog.records)
        logger.info("1")
        assert records[-1].message == "1"
        assert not hasattr(records[-1], "a")

        with add_logging_context(a=2, b=val):
            logger.info("2")
            assert records[-1].message == "2"
            assert records[-1].a == 2
            assert records[-1].b == val

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as exc:
        with add_logging_context(a=1):
            list(exc.map(thread_worker, [1, 2]))
