class InvalidMetricsObject(Exception):
    """Custom exception class for invalid metrics."""
    pass


class MetricsCollectionFailure(Exception):
    """Custom exception class for metrics collection failure."""
    pass


class InvalidMetricsSetup(Exception):
    """Custom exception class for metrics collection failure."""
    pass


class InvalidHookAccess(Exception):
    """Custom exception class for invalid metrics."""
    pass


class ExternalHostException(Exception):
    """Custom exception class for external hosts trying to use internal mongo metrics client."""
    pass
