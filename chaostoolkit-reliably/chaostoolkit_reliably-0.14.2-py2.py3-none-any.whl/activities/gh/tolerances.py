from logzero import logger

__all__ = ["ratio_under"]


def ratio_under(target: float, value: float = 0.0) -> bool:
    """
    Validates the ratio returned by a probe is strictly below the `target`.
    """
    logger.debug(f"Verify that ratio is below: {target}")
    return value < target
