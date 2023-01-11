import asyncio
import logging
from contextlib import contextmanager
from functools import wraps
from typing import Callable

from azure.core.settings import settings
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

from . import logs, traces

MESSAGE_PARAM_NAME = "msg"
SUBJECT_IDENTIFIER = "<Subject>"

tracer = traces.get_tracer(__name__)
logger = logs.get_logger(__name__)


def configure_monitoring():
    """
    Configure logging and tracing on Azure Function to
    - export telemetry to App Insights
    - supress spamming logs
    """
    # declare OTEL as enabled tracing plugin for Azure SDKs
    settings.tracing_implementation = OpenTelemetrySpan

    # disable logging for HTTP calls to avoid log spamming
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
        logging.WARNING
    )

    # disable logging for Service Bus underlying uAMQP library to avoid log spamming
    logging.getLogger("uamqp").setLevel(logging.WARNING)

    # configure tracer provider
    traces.configure_tracing()

    # configure logger provider
    logs.configure_logging()


@contextmanager
def setup_monitoring(kwargs):
    try:
        context = kwargs["context"]
    except KeyError:
        raise KeyError(
            "Azure Function must contain argument named `context` to use monitoring"
        )

    configure_monitoring()

    trace_context = context.trace_context
    with traces.set_trace_context(
        trace_context.trace_parent, trace_context.trace_state
    ):
        yield


def monitor(main: Callable):
    """Wrapper for running Azure Function
    with telemetry settings for exporting
    to App Insights.

    Args:
        main (Callable): Azure Function main function
    """

    # The `wraps` decorator ensures the resulting function has the same signature
    # as the original one, to avoid errors form the Azure Function worker.
    @wraps(main)
    async def wrapper_async(*args, **kwargs):
        with setup_monitoring(kwargs):
            pre_function(kwargs)
            result = await main(*args, **kwargs)
            post_function(kwargs)
            return result

    @wraps(main)
    def wrapper(*args, **kwargs):
        with setup_monitoring(kwargs):
            pre_function(kwargs)
            result = main(*args, **kwargs)
            post_function(kwargs)
            return result

    if asyncio.iscoroutinefunction(main):
        return wrapper_async
    else:
        return wrapper


def pre_function(kwargs):
    if MESSAGE_PARAM_NAME in kwargs:
        log_subject(kwargs[MESSAGE_PARAM_NAME].label)


def post_function(kwargs):
    pass


def log_subject(subject):
    logger.info(f"{SUBJECT_IDENTIFIER}{subject}")
