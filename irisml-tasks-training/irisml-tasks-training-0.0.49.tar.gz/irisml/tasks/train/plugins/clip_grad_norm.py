"""Clips gradient norm of model parameters."""
import logging
import torch
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Plugin(PluginBase):
    def __init__(self, max_norm: float = 1.0):
        self._max_norm = max_norm
        logger.info(f"Enabled gradient clipping. max_norm={max_norm}")

    def on_optimizer_step_start(self, trainer, model, optimizer):
        total_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), self._max_norm)
        if total_norm > self._max_norm:
            logger.debug(f"Clipping the gradients. norm={total_norm}")
        return optimizer
