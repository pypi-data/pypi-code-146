"""Freeze parameters up to the specified module.

The order of modules are determined by running a model with forward hooks.
"""

import functools
import logging
import re
import torch
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Plugin(PluginBase):
    def __init__(self, module_name_pattern):
        """
        Args:
            module_name_pattern (str): A regular expression to find a module. If empty, this plugin does nothing.
        """
        self._module_name_pattern = module_name_pattern

    def on_train_start(self, trainer, model):
        self._freeze_targets = None

    def on_train_epoch_start(self, trainer, model, epoch_index):
        if self._freeze_targets:
            freeze_modules(model, self._freeze_targets)
        return True

    def on_train_batch_start(self, trainer, model, batch, batch_index):
        if self._freeze_targets is None:
            self._freeze_targets = get_module_names_upto(model, self._module_name_pattern, batch[0], trainer.device)
            freeze_modules(model, self._freeze_targets, verbose=True)
        return batch

    def on_train_epoch_end(self, trainer, model, epoch_index):
        model.requires_grad_(True)
        model.eval()


def get_module_names_upto(module, module_name_pattern, example_inputs, device):
    """Get a list of module names up to the module that matches the given name pattern."""
    called_modules = []

    def log_module_forward(module, inputs, outputs, module_name):
        called_modules.append(module_name)

    # Add hooks
    hooks = [m.register_forward_hook(functools.partial(log_module_forward, module_name=n)) for n, m in module.named_modules()]

    logger.debug(f"Running the model once on {device} to get the order of modules.")
    example_inputs = to_device(example_inputs, device)
    with torch.no_grad():
        # Some module parameters might be impacted by this forward pass. Might need to restore the initial state if it caused an issue.
        module(example_inputs)

    for hook in hooks:
        hook.remove()

    assert called_modules
    pattern = re.compile(module_name_pattern)
    matched_index = next((i for i, n in enumerate(called_modules) if pattern.match(n)), None)
    if matched_index is None:
        logger.error(f"Failed to get matching module names. {module_name_pattern=}, {called_modules=}")
        return []
    else:
        return called_modules[:matched_index]


def freeze_modules(module, module_names, verbose=False):
    for n, m in module.named_modules():
        if n in module_names:
            if verbose:
                logger.debug(f"Freezing module {n}")
            m.requires_grad_(False)
            m.eval()


def to_device(tensor_or_list, device):
    if hasattr(tensor_or_list, 'to'):
        return tensor_or_list.to(device)
    elif isinstance(tensor_or_list, list):
        return [to_device(x, device) for x in tensor_or_list]
    else:
        return tensor_or_list
