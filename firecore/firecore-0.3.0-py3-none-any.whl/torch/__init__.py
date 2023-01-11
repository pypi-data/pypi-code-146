from firecore.logging import get_logger

logger = get_logger(__name__)
try:
    import torch
except ImportError:
    logger.exception("please install pytorch first")
