import dataclasses
import logging
from typing import Optional
import torch.utils.data
import irisml.core


class Task(irisml.core.TaskBase):
    """Get a train/val split of a dataset.

    If val_dataset is not provided, then the train_dataset will be split into a train and val dataset. E.g. if train_val_split is 0.8, then 80% of the
    train_dataset will be used for training and 20% will be used for validation.

    If val_dataset is provided, then it will be used as the validation dataset and the train_dataset will be used for training as-is.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        train_val_split: float

    @dataclasses.dataclass
    class Inputs:
        train_dataset: torch.utils.data.Dataset
        val_dataset: Optional[torch.utils.data.Dataset] = None

    @dataclasses.dataclass
    class Outputs:
        train_dataset: torch.utils.data.Dataset
        val_dataset: torch.utils.data.Dataset

    def execute(self, inputs):
        if self.config.train_val_split < 0 or self.config.train_val_split > 1:
            raise ValueError("train_val_split must be between 0 and 1")

        if not inputs.val_dataset:
            num_images = len(inputs.train_dataset)
            num_train_images = int(num_images * self.config.train_val_split)
            num_val_images = num_images - num_train_images
            train_dataset, val_dataset = torch.utils.data.random_split(inputs.train_dataset, [num_train_images, num_val_images])
            logging.info(f"Split train dataset into {len(train_dataset)} train images and {len(val_dataset)} val images")
        else:
            train_dataset, val_dataset = inputs.train_dataset, inputs.val_dataset
            logging.info(f"Skip splitting - val dataset is already provided. Using {len(train_dataset)} train images and {len(val_dataset)} val images")

        return self.Outputs(train_dataset, val_dataset)

    def dry_run(self, inputs):
        return self.execute(inputs)
