"""Use PyTorch Autograd's anomaly detection.

Useful for debugging a training issue. Note that this plugin is not recommended for production. It will slow down your training.
"""
import logging
import torch.autograd
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Plugin(PluginBase):
    def __init__(self):
        logger.info("Anomaly Detection is enabled. It will slow down the training.")

    def on_train_start(self, trainer, model):
        torch.autograd.set_detect_anomaly(True)

    def on_train_end(self, trainer, model):
        torch.autograd.set_detect_anomaly(False)
