import collections
import dataclasses
import logging
import math
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Make an oversampled dataset.

    Config:
        min_num_samples (int): The minimum number of samples in the oversampled dataset.
        oversampling_rate (float): The rate of oversampling. Actual rate can be bigger than this value because of the effect of min_num_samples.
        balance (bool): If True, oversample from the minority classes.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset

    @dataclasses.dataclass
    class Config:
        min_num_samples: int
        oversampling_rate: float = 1.0
        balance: bool = False
        balance_weights_max: float = 5.0
        balance_weights_min: float = 0.2

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset

    def execute(self, inputs):
        num_samples = len(inputs.dataset)
        num_new_samples = max(0, self.config.min_num_samples - num_samples, int((self.config.oversampling_rate - 1) * num_samples))

        if num_new_samples > 0:
            logger.info(f"Oversampling the dataset. The current number of samples: {num_samples}. New: {num_samples+num_new_samples}")
            if self.config.balance:
                weights = self._calculcate_weights(inputs.dataset, self.config.balance_weights_max, self.config.balance_weights_min)
                new_samples = torch.multinomial(torch.tensor(weights), num_new_samples, replacement=True)
            else:
                new_samples = torch.randint(high=num_samples, size=(num_new_samples,), dtype=torch.int64)

            index_map = torch.cat([torch.arange(num_samples, dtype=torch.int64), new_samples]).tolist()
            dataset = OversampledDataset(inputs.dataset, index_map)
        else:  # No oversampling
            dataset = inputs.dataset
            if self.config.balance:
                logger.warning("Dataset balancing is not performed. Please change oversampling_rate to a higher value.")

        assert len(dataset) == num_samples + num_new_samples
        return self.Outputs(dataset)

    def dry_run(self, inputs):
        return self.Outputs(inputs.dataset)

    @staticmethod
    def _calculcate_weights(dataset, balance_weights_max, balance_weights_min):
        # Get the number of annotations per class.
        class_ids = [Task._get_class_id(x) for x in dataset]
        class_counter = collections.Counter()
        for ids in class_ids:
            class_counter.update(ids)

        mean_num_tags = sum(class_counter.values()) / len(class_counter)
        weights_per_class = {c: mean_num_tags / n for c, n in class_counter.items()}

        # Make soft target
        weights_per_class = {c: math.sqrt(w) for c, w in weights_per_class.items()}

        # Clamp the weights
        weights_per_class = {c: max(min(w, balance_weights_max), balance_weights_min) for c, w in weights_per_class.items()}

        weights_per_sample = [math.prod(weights_per_class[t] for t in tags) for tags in class_ids]
        weights_per_sample = [min(w, balance_weights_max) for w in weights_per_sample]

        return weights_per_sample

    @staticmethod
    def _get_class_id(sample):
        """Get a list of class ids from the target.
        Supported target formats:
            int
            float
            List[]
            List[int]
            List[float]
            List[List[float]]
            LongTensor(,)
            LongTensor(N,)
            FloatTensor(N,)
            FloatTensor(N, 5)
        """
        targets = sample[1]
        if isinstance(targets, int):
            return [targets]
        elif isinstance(targets, float):
            return []
        elif isinstance(targets, list):
            if not targets or isinstance(targets[0], float):
                return []
            elif isinstance(targets[0], int):
                return list(set(targets))
            elif isinstance(targets[0], list):
                return list(set(x[0] for x in targets)) if targets[0] else []
        elif isinstance(targets, torch.Tensor):
            if not targets.shape:
                return [int(targets)] if not targets.is_floating_point() else []
            elif len(targets.shape) == 1:
                return list(set(targets.tolist())) if not targets.is_floating_point() else []
            elif len(targets.shape) == 2:
                return list(set(targets[:, 0].flatten().tolist()))
        raise TypeError(f"Unsupported target type is detected: {targets} ({type(targets)})")


class OversampledDataset(torch.utils.data.Dataset):
    def __init__(self, dataset, index_map):
        self._dataset = dataset
        self._index_map = index_map

    def __len__(self):
        return len(self._index_map)

    def __getitem__(self, index):
        new_index = self._index_map[index]
        assert isinstance(new_index, int)
        return self._dataset[new_index]
