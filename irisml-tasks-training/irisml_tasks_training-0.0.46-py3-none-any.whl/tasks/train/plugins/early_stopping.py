"""Early stopping for training.

To use this plugin, validation steps must be included in the training.
"""
import logging
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Plugin(PluginBase):
    def __init__(self, patience=2, min_delta=0.0):
        """
        Args:
            patience (int): Number of validation epochs with no improvement after which training will be stopped.
            min_delta (float): Minimum change in the loss to qualify as improvement
        """
        self._patience = patience
        self._min_delta = min_delta
        logger.info(f"Early stopping is enabled with {patience=}, {min_delta=}")

    def on_train_start(self, trainer, model):
        self._counter = 0
        self._early_stop = False
        self._best_loss = None

    def on_train_end(self, trainer, model):
        if self._best_loss is None:
            logger.warning("Early stopping was enabled but validation step was never called. Please enable validation to use early stopping.")

    def on_train_epoch_start(self, trainer, model, epoch_index):
        return not self._early_stop

    def on_validation_start(self, trainer, model):
        self._validation_sum_loss = 0
        self._validation_num_samples = 0

    def on_validation_batch_end(self, trainer, model, loss, batch, batch_index):
        self._validation_sum_loss += float(loss.item()) * len(batch[0])
        self._validation_num_samples += len(batch[0])

    def on_validation_end(self, trainer, model):
        if self._validation_num_samples == 0:
            logger.warning("Validation set doesn't have any samples. Please double check your dataset settings.")
            return

        mean_validation_loss = self._validation_sum_loss / self._validation_num_samples
        if self._best_loss is None or mean_validation_loss < self._best_loss - self._min_delta:
            self._best_loss = mean_validation_loss
            self._counter = 0
        else:
            self._counter += 1

        if self._counter > self._patience:
            logger.info(f"The validation loss has not improved for {self._counter} times. Stopping the training.")
            self._early_stop = True
