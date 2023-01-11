# NOTE: OpenTelemetry logging to Azure is still in EXPERIMENTAL mode!
import logging
from logging import StreamHandler

from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from opentelemetry.sdk import _logs as logs
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

logger = logging.getLogger(__name__)
logger.addHandler(StreamHandler())

LOGGING_IS_CONFIGURED = False


def configure_logging():
    global LOGGING_IS_CONFIGURED
    if LOGGING_IS_CONFIGURED:
        # logging should only be set up once
        # to avoid duplicated log handling.
        # Global variables is the pattern used
        # by opentelemetry, so we use the same
        return

    # setup azure monitor log exporter to send telemetry to App Insights
    try:
        log_exporter = AzureMonitorLogExporter()
    except ValueError:
        # if no App Insights instrumentation key is set (e.g. when running unit tests),
        # the exporter creation will fail. In this case we skip it
        logger.warning(
            "Cant set up logging to App Insights, as no instrumentation key is set."
        )
    else:
        log_record_processor = BatchLogRecordProcessor(log_exporter)
        logs.get_logger_provider().add_log_record_processor(log_record_processor)

    LOGGING_IS_CONFIGURED = True


def get_logger(name: str):
    # set up standard logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        # add OTEL handler
        handler = LoggingHandler()
        logger.addHandler(handler)

    return logger
