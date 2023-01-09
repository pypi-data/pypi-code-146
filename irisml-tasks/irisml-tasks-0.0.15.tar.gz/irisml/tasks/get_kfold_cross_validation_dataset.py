import dataclasses
import logging
import random
import torch.utils.data
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Get train/test dataset for k-fold cross validation.

    Config:
        num_folds (int): K
        index (int): The index of a fold for test.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset

    @dataclasses.dataclass
    class Config:
        num_folds: int
        index: int

    @dataclasses.dataclass
    class Outputs:
        train_dataset: torch.utils.data.Dataset
        val_dataset: torch.utils.data.Dataset

    def execute(self, inputs):
        num_samples = len(inputs.dataset)

        if num_samples < self.config.num_folds:
            raise ValueError(f"There are not enough samples for k-fold cross validation. {num_samples=}, num_folds={self.config.num_folds}")

        if not 0 <= self.config.index < self.config.num_folds:
            raise ValueError(f"The index must be 0 <= index < num_folds. index={self.config.index}, num_folds={self.config.num_folds}")

        shuffled_indices = random.sample(range(num_samples), num_samples)

        fold_size = num_samples // self.config.num_folds
        remainder = num_samples % self.config.num_folds

        start_index = fold_size * self.config.index + min(self.config.index, remainder)
        end_index = start_index + fold_size + (1 if self.config.index < remainder else 0)
        assert 0 <= start_index < end_index <= num_samples

        train_indices = shuffled_indices[0:start_index] + shuffled_indices[end_index:]
        val_indices = shuffled_indices[start_index:end_index]

        assert len(train_indices) + len(val_indices) == num_samples

        train_dataset = torch.utils.data.Subset(inputs.dataset, train_indices)
        val_dataset = torch.utils.data.Subset(inputs.dataset, val_indices)
        logger.info(f"Created train/val datasets. {len(train_dataset)=}, {len(val_dataset)=}")

        return self.Outputs(train_dataset, val_dataset)

    def dry_run(self, inputs):
        return self.execute(inputs)
