from processview.core.dataset import Dataset


class TomwerObject(Dataset):
    """Common tomwer object"""

    def __init__(self) -> None:
        super().__init__()

    def _clear_heavy_cache(self):
        """util function to clear some heavy object from the cache"""
        raise NotImplementedError()

    def clear_caches(self):
        pass
