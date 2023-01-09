"""Contains PyTorch specific utility methods."""
from enum import Enum
from functools import lru_cache
import logging

import pytorch_lightning.loggers as pl_loggers
import torch

from bitfount.config import BITFOUNT_USE_MPS
from bitfount.types import _StrAnyDict

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _autodetect_gpu() -> _StrAnyDict:
    """Detects and returns GPU accelerator and device count.

    Returns:
        A dictionary with the keys 'accelerator' and 'devices' which should be passed
        to the PyTorchLightning Trainer.
    """
    mps = False
    try:
        if torch.backends.mps.is_available():  # type: ignore[attr-defined] # Reason: Older PyTorch versions don't have this attribute.  # noqa: B950
            if BITFOUNT_USE_MPS:
                mps = True
            else:
                logger.info("Metal support detected, but has been switched off.")
    except AttributeError:
        logger.debug("Pytorch version does not support MPS.")

    if mps:
        logger.info("Metal support detected. Running model on Apple GPU.")
        return {"accelerator": "mps", "devices": 1}

    else:
        # Run on GPU if available
        gpus: int = torch.cuda.device_count()
        if gpus > 0:
            gpu_0_name: str = torch.cuda.get_device_name(0)

            # Reduce to 1 GPU if multiple detected
            # TODO: [BIT-492] Add multi-GPU support.
            if gpus > 1:
                logger.warning(
                    f"Bitfount model currently only supports one GPU. "
                    f"Will use GPU 0 ({gpu_0_name})."
                )
                gpus = 1

            logger.info(f"CUDA support detected. GPU ({gpu_0_name}) will be used.")
            return {"accelerator": "gpu", "devices": 1}

    logger.info("No supported GPU detected. Running model on CPU.")
    return {"accelerator": None, "devices": None}


class LoggerType(Enum):
    """Different types of loggers for PyTorchLightning.

    With the exception of CSVLogger and TensorBoardLogger, all loggers need to have
    their corresponding python libraries installed separately.

    More information about PyTorchLightning loggers can be found here:
    https://pytorch-lightning.readthedocs.io/en/latest/common/loggers.html
    """

    CSVLogger = pl_loggers.CSVLogger
    MLFlow = pl_loggers.MLFlowLogger
    Neptune = pl_loggers.NeptuneLogger
    TensorBoard = pl_loggers.TensorBoardLogger
    WeightsAndBiases = pl_loggers.WandbLogger
