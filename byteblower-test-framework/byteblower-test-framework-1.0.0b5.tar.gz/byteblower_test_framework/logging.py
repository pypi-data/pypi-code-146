"""Logging requirements for the ByteBlower Test Framework."""
import logging

__all__ = (
    'configure_logging',
)


def configure_logging():
    """Configure logging for the used (low-level) frameworks."""
    for framework in ('scapy.runtime', ):
        framework_logger = logging.getLogger(framework)
        framework_logger.setLevel(logging.ERROR)
