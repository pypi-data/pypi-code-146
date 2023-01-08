def sample_to_dbfs(sample: int, bits: int = 16) -> float:
    import numpy as np

    return 20 * np.log10(abs(sample) / (2 ** (bits - 1)))


def dbfs_to_sample(dbfs: float, bits: int = 16) -> int:
    return int((10 ** (dbfs / 20)) * (2 ** (bits - 1)))
