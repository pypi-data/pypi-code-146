import collections
import dataclasses
import logging
import math
import random
from typing import Optional
import torch.utils.data
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Get a train/val split of a dataset.

    If val_dataset is not provided, then the train_dataset will be split into a train and val dataset. E.g. if train_val_split is 0.8, then 80% of the
    train_dataset will be used for training and 20% will be used for validation.

    If val_dataset is provided, then it will be used as the validation dataset and the train_dataset will be used for training as-is.

    Config:
        train_val_split (float): The ratio of the size of the train/val datasets.
        keep_class_distribution (bool): If true, tries to keep the class distribution.
    """
    VERSION = '0.2.0'

    @dataclasses.dataclass
    class Config:
        train_val_split: float
        keep_class_distribution: bool = False

    @dataclasses.dataclass
    class Inputs:
        train_dataset: torch.utils.data.Dataset
        val_dataset: Optional[torch.utils.data.Dataset] = None

    @dataclasses.dataclass
    class Outputs:
        train_dataset: torch.utils.data.Dataset
        val_dataset: torch.utils.data.Dataset

    def execute(self, inputs):
        if not 0 <= self.config.train_val_split <= 1:
            raise ValueError("train_val_split must be between 0 and 1")

        if not inputs.val_dataset:
            if self.config.keep_class_distribution:
                train_indices, val_indices = self._get_split_indices(inputs.train_dataset, self.config.train_val_split)
                assert len(train_indices) + len(val_indices) == len(inputs.train_dataset)
                train_dataset = torch.utils.data.Subset(inputs.train_dataset, train_indices)
                val_dataset = torch.utils.data.Subset(inputs.train_dataset, val_indices)
            else:
                num_images = len(inputs.train_dataset)
                num_train_images = int(num_images * self.config.train_val_split)
                num_val_images = num_images - num_train_images
                train_dataset, val_dataset = torch.utils.data.random_split(inputs.train_dataset, [num_train_images, num_val_images])
            logger.info(f"Split train dataset into {len(train_dataset)} train images and {len(val_dataset)} val images")
        else:
            train_dataset, val_dataset = inputs.train_dataset, inputs.val_dataset
            logger.info(f"Skip splitting - val dataset is already provided. Using {len(train_dataset)} train images and {len(val_dataset)} val images")

        return self.Outputs(train_dataset, val_dataset)

    def dry_run(self, inputs):
        return self.execute(inputs)

    @staticmethod
    def _get_split_indices(dataset, train_val_ratio):
        """Get train/val indices that keeps the class distribution."""
        def get_class(x):
            if torch.is_tensor(x):
                if not x.shape:
                    return [int(x)]
                elif len(x.shape) == 1:
                    return x.tolist()
                elif len(x.shape) == 2:
                    assert x.shape[1] == 5
                    return [int(y[0]) for y in x]
            elif isinstance(x, int):
                return [x]
            raise ValueError(f"Unexpected data label: {x=}, {type(x)=}")

        image_class_indices = [(i, get_class(x[1])) for i, x in enumerate(dataset)]
        random.shuffle(image_class_indices)

        train_indices = []
        val_indices = []

        # Split examples that has no class labels.
        negative_examples = [i for i, c in image_class_indices if not c]
        num_val_negative_examples = math.ceil(len(negative_examples) * (1 - train_val_ratio))
        val_indices += negative_examples[0:num_val_negative_examples]
        train_indices += negative_examples[num_val_negative_examples:]

        image_class_indices = [(i, c) for i, c in image_class_indices if c]
        train_classes_counter = collections.Counter()
        val_classes_counter = collections.Counter()
        for index, classes in image_class_indices:
            train_class_counts = [train_classes_counter[x] for x in classes]
            val_class_counts = [val_classes_counter[x] for x in classes]
            train_class_count_sum = sum(train_class_counts) * (1 - train_val_ratio) / train_val_ratio
            train_class_count_min = min(train_class_counts) * (1 - train_val_ratio) / train_val_ratio
            val_class_count_sum = sum(val_class_counts)
            val_class_count_min = min(val_class_counts)
            if val_class_count_min < train_class_count_min or (val_class_count_min == train_class_count_min and val_class_count_sum < train_class_count_sum):
                val_indices.append(index)
                val_classes_counter.update(classes)
            else:
                train_indices.append(index)
                train_classes_counter.update(classes)
        return train_indices, val_indices
