"""Model Exponential Moving Average (EMA)

This plugin keeps expornential moving average of the model parameter as it is training.

The EMA weights are updated as follows at the end of each epoch:
    ema_weights = decay * ema_weights + (1 - decay) * current_weights
"""
import logging
import torch
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Plugin(PluginBase):
    def __init__(self, decay: float = 0.99):
        if not (0.0 <= decay <= 1.0):
            raise ValueError(f"Decay must be in the range [0, 1]. decay={decay}")
        self._decay = decay

    def on_train_start(self, trainer, model):
        def ema_avg(averaged_model_params, model_params, num_averaged):
            return self._decay * averaged_model_params + (1 - self._decay) * model_params

        # Keep the copy on CPU memory.
        self._averaged_model = torch.optim.swa_utils.AveragedModel(model, avg_fn=ema_avg, device=torch.device('cpu'))
        logger.info(f"Model EMA is enabled with decay={self._decay}")

    def on_train_batch_end(self, trainer, model, loss, batch, batch_index):
        self._averaged_model.update_parameters(model)

    def on_train_end(self, trainer, model):
        assert len(list(self._averaged_model.parameters())) == len(list(model.parameters()))
        for avg_param, model_param in zip(self._averaged_model.parameters(), model.parameters()):
            assert avg_param.shape == model_param.shape
            model_param.detach().copy_(avg_param.to(model_param.device))
        logger.info("Updated the model with the averaged parameters.")
