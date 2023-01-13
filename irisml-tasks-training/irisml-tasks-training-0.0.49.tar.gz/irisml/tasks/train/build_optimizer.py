import collections
import logging
import re
import torch.distributed.optim
import torch.optim

logger = logging.getLogger(__name__)


def build_optimizer(name: str, parameters, base_lr, weight_decay, momentum):
    if name == 'sgd':
        return torch.optim.SGD(parameters, lr=base_lr, weight_decay=weight_decay, momentum=momentum)
    elif name == 'adam':
        return torch.optim.Adam(parameters, lr=base_lr, weight_decay=weight_decay)
    elif name == 'amsgrad':
        return torch.optim.Adam(parameters, lr=base_lr, weight_decay=weight_decay, amsgrad=True)
    elif name == 'adamw':
        return torch.optim.AdamW(parameters, lr=base_lr, weight_decay=weight_decay)
    elif name == 'adamw_amsgrad':
        return torch.optim.AdamW(parameters, lr=base_lr, weight_decay=weight_decay, amsgrad=True)
    elif name == 'rmsprop':
        return torch.optim.RMSprop(parameters, lr=base_lr, weight_decay=weight_decay, momentum=momentum)
    elif name == 'zero_adam':
        return torch.distributed.optim.ZeroRedundancyOptimizer(parameters, optimizer_class=torch.optim.Adam, lr=base_lr, weight_decay=weight_decay)
    elif name == 'zero_amsgrad':
        return torch.distributed.optim.ZeroRedundancyOptimizer(parameters, optimizer_class=torch.optim.Adam, lr=base_lr, weight_decay=weight_decay, amsgrad=True)
    elif name == 'zero_adamw':
        return torch.distributed.optim.ZeroRedundancyOptimizer(parameters, optimizer_class=torch.optim.AdamW, lr=base_lr, weight_decay=weight_decay)
    elif name == 'zero_adamw_amsgrad':
        return torch.distributed.optim.ZeroRedundancyOptimizer(parameters, optimizer_class=torch.optim.AdamW, lr=base_lr, weight_decay=weight_decay, amsgrad=True)
    else:
        raise ValueError(f"Unsupported optimizer: {name}")


class OptimizerFactory:
    def __init__(self, name: str, base_lr, weight_decay=0, momentum=0, no_weight_decay_param_names=None, no_weight_decay_module_class_names=None, lr_scale_param_names=None):
        self._name = name
        self._base_lr = base_lr
        self._weight_decay = weight_decay
        self._momentum = momentum
        self._no_weight_decay_param_name_patterns = [re.compile(p) for p in (no_weight_decay_param_names or [])]
        self._no_weight_decay_module_class_name_patterns = [re.compile(p) for p in (no_weight_decay_module_class_names or [])]
        self._lr_scale_param_name_patterns = [(re.compile(k), v) for k, v in (lr_scale_param_names or [])]

    def __call__(self, model):
        params = []
        no_weight_decay_params = set()

        for name, module in model.named_modules():
            if any(p.match(type(module).__name__) for p in self._no_weight_decay_module_class_name_patterns):
                logger.debug(f"Disabling weight_decay for module {name}")
                no_weight_decay_params.update(module.parameters())

        param_groups_dict = collections.defaultdict(list)
        for name, param in model.named_parameters():
            weight_decay = None
            lr = None

            if param in no_weight_decay_params:
                weight_decay = 0.0

            if weight_decay is None and any(p.match(name) for p in self._no_weight_decay_param_name_patterns):
                logger.debug(f"Disabling weight_decay for param {name}")
                weight_decay = 0.0

            lr_scale_entry = next((p for p in self._lr_scale_param_name_patterns if p[0].match(name)), None)
            if lr_scale_entry:
                logger.debug(f"Scaling lr for param {name} with {lr_scale_entry[1]}")
                lr = self._base_lr * lr_scale_entry[1]

            param_groups_dict[(weight_decay, lr)].append(param)

        assert len(list(model.parameters())) == sum(len(p) for p in param_groups_dict.values())

        # Construct param_groups parameter.
        param_groups = []
        for (weight_decay, lr), params in param_groups_dict.items():
            group = {'params': params}
            if weight_decay is not None:
                group['weight_decay'] = weight_decay
            if lr is not None:
                group['lr'] = lr
            param_groups.append(group)

        return build_optimizer(self._name, param_groups, self._base_lr, self._weight_decay, self._momentum)
