from logzero import logger

__all__ = ["response_time_must_be_under"]


def response_time_must_be_under(latency: float, value: float = 0.0) -> bool:
    """
    Validates the response time is under the given latency.

    Use this as the tolerance of the
    `chaosreliably.activities.http.probes.measure_response_time` probe.
    """
    logger.debug(f"Verify that response time is under: {latency}")
    return value <= latency
