"""Mixup (https://arxiv.org/abs/1710.09412)

For classification_multiclass, targets will be updated to one-hot vectors, then mixup will be applied.

For object_detection, bounding boxes are simply concatenated without changing box probabilities.
"""

import logging
import typing
import torch
from .plugin_base import PluginBase

logger = logging.getLogger(__name__)


class Delegate:
    def __init__(self, alpha, num_classes):
        self._beta_distribution = torch.distributions.beta.Beta(alpha, alpha)
        self.num_classes = num_classes

    def get_lambda(self):
        return self._beta_distribution.sample()

    def __call__(self, batch):
        inputs, targets = batch
        indices = torch.randperm(len(inputs), device=inputs.device, dtype=torch.long)
        coefficient = self.get_lambda()
        return self.mixup(batch, indices, coefficient)

    def mixup(self, batch, indices, coefficient):
        raise NotImplementedError


class ClassificationMulticlassDelegate(Delegate):
    def mixup(self, batch, indices, coefficient):
        inputs, targets = batch
        inputs = inputs * coefficient + inputs[indices] * (1 - coefficient)
        onehot_targets = torch.nn.functional.one_hot(targets, self.num_classes)
        targets = onehot_targets * coefficient + onehot_targets[indices] * (1 - coefficient)
        return inputs, targets


class ClassificationMultilabelDelegate(Delegate):
    def mixup(self, batch, indices, coefficient):
        inputs, targets = batch
        inputs = inputs * coefficient + inputs[indices] * (1 - coefficient)
        targets = targets * coefficient + targets[indices] * (1 - coefficient)
        return inputs, targets


class ObjectDetectionDelegate(Delegate):
    def mixup(self, batch, indices, coefficient):
        inputs, targets = batch
        inputs = inputs * coefficient + inputs[indices] * (1 - coefficient)
        targets = [torch.cat((t, targets[indices[i]])) for i, t in enumerate(targets)]
        return inputs, targets


class Plugin(PluginBase):
    def __init__(self, task_type: typing.Literal['classification_multiclass', 'classification_multilabel', 'object_detection'], alpha: float, num_classes: int):
        if task_type == 'classification_multiclass':
            self._delegate = ClassificationMulticlassDelegate(alpha, num_classes)
        elif task_type == 'classification_multilabel':
            self._delegate = ClassificationMultilabelDelegate(alpha, num_classes)
        elif task_type == 'object_detection':
            self._delegate = ObjectDetectionDelegate(alpha, num_classes)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")

        logger.info(f"Mixup is enabled with {alpha=}, {task_type=}, {num_classes=}")

    def on_train_batch_start(self, trainer, model, batch, batch_index):
        if len(batch[0]) == 1:
            return batch  # Do nothing if batch_size is 1.
        return self._delegate(batch)
