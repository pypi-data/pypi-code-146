from logzero import logger

__all__ = ["ratio_under", "ratio_above"]


def ratio_under(target: float, value: float = 0.0) -> bool:
    """
    Validates the ratio returned by a probe is strictly below the `target`.
    """
    logger.debug(f"Verify that ratio is below: {target}")
    return value < target


def ratio_above(target: float, value: float = 0.0) -> bool:
    """
    Validates the ratio returned by a probe is strictly greater than the
    `target`.
    """
    logger.debug(f"Verify that ratio is above: {target}")
    return value > target
