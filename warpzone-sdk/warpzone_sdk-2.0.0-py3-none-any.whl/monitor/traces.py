import logging
from contextlib import contextmanager
from logging import StreamHandler

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import context, trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ALWAYS_ON
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

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
    # NOTE: We use the ALWAYS ON sampler since otherwise,
    # spans will not be recording upon creation
    # (https://anecdotes.dev/opentelemetry-on-google-cloud-unraveling-the-mystery-f61f044c18be)
    trace.set_tracer_provider(TracerProvider(sampler=ALWAYS_ON))

    # setup azure monitor trace exporter to send telemetry to App Insights
    try:
        trace_exporter = AzureMonitorTraceExporter()
    except ValueError:
        # if no App Insights instrumentation key is set (e.g. when running unit tests),
        # the exporter creation will fail. In this case we skip it
        logger.warning(
            "Cant set up tracing to App Insights, as no instrumentation key is set."
        )
    else:
        span_processor = BatchSpanProcessor(trace_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

    TRACING_IS_CONFIGURED = True


@contextmanager
def set_trace_context(trace_parent: str, trace_state: str = ""):
    """Context manager for setting the trace context

    Args:
        trace_parent (str): Trace parent ID
        trace_state (str, optional): Trace state. Defaults to "".
    """
    carrier = {"traceparent": trace_parent, "tracestate": trace_state}
    ctx = TraceContextTextMapPropagator().extract(carrier=carrier)

    token = context.attach(ctx)  # attach context before run
    try:
        yield
    finally:
        context.detach(token)  # detach context after run


def get_tracer(name: str):
    tracer = trace.get_tracer(name)
    return tracer
