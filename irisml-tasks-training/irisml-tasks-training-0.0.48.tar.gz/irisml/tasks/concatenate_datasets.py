import copy
import dataclasses
import logging
import typing
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Concatenate the given two datasets together.

    If Config.use_same_classspace is False, class_names0 and class_names1 must be provided. The class ids will be mapped so that the new class_names will not have duplicated names.

    Config:
        task_type ('classifictaion_multiclass' or 'object_detection'): The dataset type.
        use_same_classspace (bool): If False, the class ids of the dataset1 will be mapped to new class ids.
    """
    VERSION = '0.1.1'

    @dataclasses.dataclass
    class Inputs:
        dataset0: torch.utils.data.Dataset
        dataset1: typing.Optional[torch.utils.data.Dataset] = None
        class_names0: typing.Optional[typing.List[str]] = None
        class_names1: typing.Optional[typing.List[str]] = None

    @dataclasses.dataclass
    class Config:
        task_type: typing.Literal['classification_multiclass', 'object_detection'] = 'classification_multiclass'
        use_same_classspace: bool = True

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset
        class_names: typing.Optional[typing.List[str]] = None
        num_classes: typing.Optional[int] = None

    def execute(self, inputs):
        if not inputs.dataset1:
            logger.info("dataset1 is None. Returning dataset0 without concatenation.")
            return self.Outputs(inputs.dataset0, inputs.class_names0)

        if not self.config.use_same_classspace:
            if inputs.class_names0 and inputs.class_names1:
                class_mappings = [list(range(len(inputs.class_names0))), []]
                new_class_names = copy.deepcopy(inputs.class_names0)
                for c in inputs.class_names1:
                    try:
                        existing_class_id = new_class_names.index(c)
                        class_mappings[1].append(existing_class_id)
                    except ValueError:
                        class_mappings[1].append(len(new_class_names))
                        new_class_names.append(c)
            else:
                raise RuntimeError("When use_same_classspace is False, both class_names0 and class_names1 must be provided.")
            num_classes = len(new_class_names)
            logger.info(f"The number of new classes is {num_classes}")
        else:
            class_mappings = None
            new_class_names = None
            num_classes = None

        dataset = ConcatDataset(inputs.dataset0, inputs.dataset1, class_mappings, self.config.task_type)
        return self.Outputs(dataset, new_class_names, num_classes)

    def dry_run(self, inputs):
        return self.execute(inputs)


class ConcatDataset(torch.utils.data.Dataset):
    def __init__(self, dataset0, dataset1, class_mappings: typing.List[typing.List[int]], task_type):
        assert class_mappings is None or len(class_mappings) == 2
        assert task_type in ['classification_multiclass', 'object_detection']
        self._datasets = [dataset0, dataset1]
        self._first_dataset_size = len(dataset0)
        self._class_mappings = class_mappings
        self._task_type = task_type

    def __len__(self):
        return len(self._datasets[0]) + len(self._datasets[1])

    def __getitem__(self, index):
        if index < self._first_dataset_size:
            dataset_index = 0
            sample_index = index
        else:
            dataset_index = 1
            sample_index = index - self._first_dataset_size

        inputs, targets = self._datasets[dataset_index][sample_index]

        if self._class_mappings:
            if self._task_type == 'classification_multiclass':
                if isinstance(targets, list) and len(targets) == 1:
                    targets = targets[0]
                targets = torch.tensor([self._class_mappings[dataset_index][int(targets)]])
            elif self._task_type == 'object_detection':
                targets = torch.tensor([[self._class_mappings[dataset_index][int(t[0])], *t[1:]] for t in targets])

        return inputs, targets
