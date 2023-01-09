import logging

from azure.core.settings import settings
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

from . import logs, traces


def configure_monitoring():
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
