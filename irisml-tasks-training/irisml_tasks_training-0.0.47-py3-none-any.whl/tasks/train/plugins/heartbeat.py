"""Log the current status every N minutes. Useful for large datasets that an epoch takes long time.

DEBUG level is used for logging.
"""
import logging
import time
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Plugin(PluginBase):
    def __init__(self, interval_in_minutes=5):
        self._interval_in_minutes = interval_in_minutes

    def on_train_epoch_start(self, trainer, model, epoch_index):
        self._last_update = time.time()
        return True

    def on_train_batch_end(self, trainer, model, loss, batch, batch_index):
        if time.time() > self._last_update + self._interval_in_minutes * 60:
            self._last_update = time.time()
            logger.debug(f"Batch {batch_index} is completed. loss={float(loss.item())}")
