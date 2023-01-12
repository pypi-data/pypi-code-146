"""Multiple the loss value by the specified value."""

import logging
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Plugin(PluginBase):
    def __init__(self, scale):
        super().__init__()
        self._scale = scale

    def on_train_start(self, trainer, model):
        logger.info(f"Loss scaling is enabled. scale={self._scale}")

    def on_train_backward_start(self, trainer, model, loss):
        return loss * self._scale
