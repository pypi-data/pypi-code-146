import dataclasses
import logging
import pathlib
import pickle
import uuid
import torch.utils.data
import irisml.core

logger = logging.getLogger()


class Task(irisml.core.TaskBase):
    """Save dataset cache on disk.

    Inputs:
        dataset (torch.utils.data.Dataset): The original dataset object. The return values must be serializable.

    Config:
        cache_dir (pathlib.Path): The path to the cache directory
    """
    VERSION = '0.1.1'

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset

    @dataclasses.dataclass
    class Config:
        cache_dir: pathlib.Path = pathlib.Path('.')

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset

    class CachedDataset(torch.utils.data.Dataset):
        def __init__(self, dataset, cache_dir):
            self._dataset = dataset
            self._cache_dir = cache_dir
            cache_dir.mkdir(parents=True, exist_ok=True)

        def __len__(self):
            return len(self._dataset)

        def __getitem__(self, index):
            cache_path = self._cache_dir / str(index)
            if cache_path.exists():
                try:
                    return pickle.loads(cache_path.read_bytes())
                except Exception:
                    pass
            item = self._dataset[index]
            cache_path.write_bytes(pickle.dumps(item))
            return item

        def __getstate__(self):
            return {'dataset': self._dataset, 'cache_dir': self._cache_dir}

        def __setstate__(self, state):
            self.__init__(**state)

    def execute(self, inputs):
        cache_dir = self.config.cache_dir / str(uuid.uuid4())
        logger.info(f"Saving dataset cache to {cache_dir}")
        return self.Outputs(Task.CachedDataset(inputs.dataset, cache_dir))

    def dry_run(self, inputs):
        return self.execute(inputs)
