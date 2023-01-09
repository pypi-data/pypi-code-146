import logging
from logging import StreamHandler

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logger = logging.getLogger(__name__)
logger.addHandler(StreamHandler())

TRACING_IS_CONFIGURED = False


def configure_tracing():
    global TRACING_IS_CONFIGURED
    if TRACING_IS_CONFIGURED:
        # tracing should only be set up once
        # to avoid duplicated trace handling.
        # Global variables is the pattern used
        # by opentelemetry, so we use the same
        return

    # setup OTEL tracing provider.
    # any call to to the tracer provider
    # prior to this line, will reference
    # a "proxy" trace provider
    trace.set_tracer_provider(TracerProvider())

    # setup azure monitor trace exporter to send telemetry to appinsights
    try:
        trace_exporter = AzureMonitorTraceExporter()
    except ValueError:
        # if no appinsights instrumentation key is set (e.g. when running unit tests),
        # the exporter creation will fail. In this case we skip it
        logger.warning(
            "Cant set up tracing to App Insights, as no instrumentation key is set."
        )
    else:
        span_processor = BatchSpanProcessor(trace_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

    TRACING_IS_CONFIGURED = True


def get_tracer(name: str):
    tracer = trace.get_tracer(name)
    return tracer
