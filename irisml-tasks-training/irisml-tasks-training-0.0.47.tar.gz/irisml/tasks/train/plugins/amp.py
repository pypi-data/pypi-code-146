"""Automatic Mixed Precision plugin

Enable float16 AMP on CUDA, and bfloat16 AMP on CPU.

AMP will be applied only in the forward pass.

Gradient scaling will be used on CUDA.
"""
import logging
import torch
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class AMPOptimizer:
    def __init__(self, optimizer, scaler):
        self._optimizer = optimizer
        self._scaler = scaler

    def __getattr__(self, attr):
        return getattr(self._optimizer, attr)

    def step(self, *args, **kwargs):
        result = self._scaler.step(self._optimizer)
        self._scaler.update()
        return result


class Plugin(PluginBase):
    def on_train_start(self, trainer, model):
        self._scaler = torch.cuda.amp.GradScaler()  # Will be disabled if it's on CPU.
        self._device_type = trainer.device.type
        logger.info(f"Automatic Mixed Precision is enabled on {self._device_type}.")

    def on_train_backward_start(self, trainer, model, loss):
        return self._scaler.scale(loss) if self._scaler else loss

    def on_optimizer_step_start(self, trainer, model, optimizer):
        if self._scaler:
            self._scaler.unscale_(optimizer)
            return AMPOptimizer(optimizer, self._scaler)
        else:
            return optimizer

    def forward_context(self):
        return torch.autocast(self._device_type)
