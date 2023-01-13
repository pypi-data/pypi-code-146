"""Log information about Sciagraph jobs to OpenTelemetry."""

from opentelemetry.trace import INVALID_SPAN, get_current_span
from sciagraph.api import job_status


def record_sciagraph_job():
    """
    Record information about the current Sciagraph job as a OpenTelemetry Event
    on the current span.
    """
    span = get_current_span()
    if span == INVALID_SPAN:
        return
    status = job_status()
    span.add_event(
        "sciagraph",
        {
            "sciagraph.download_key": status.download_key,
            "sciagraph.decryption_key": status.decryption_key,
            "sciagraph.peak_memory_job": status.peak_memory_kb,
            "sciagraph.instructions": status.instructions(),
            "sciagraph.job_id": status.job_id,
        },
    )


__all__ = ["record_sciagraph_job"]
