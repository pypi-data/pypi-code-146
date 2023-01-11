# this fails immediately on import of ruamel.std.pathlib.blake3 if blake3 not installed


__all__ = ['blake3']

from typing import Any
from blake3 import blake3  # type: ignore

from pathlib import Path


if not hasattr(Path, 'blake3'):

    def _blake3(self: Path, size: int = -1, timeit: bool = False) -> Any:
        """blake3 hash of the contents
        if size is provided and non-negative only read that amount of bytes from
        the start of the file
        """
        with self.open(mode='rb') as f:
            data = f.read(size)
        if timeit:
            import time

            start = time.time()
            try:
                res = blake3(data, max_threads=blake3.AUTO)
            except (TypeError, AttributeError):
                res = blake3(data, multithreading=True)
            return time.time() - start, res
        try:
            res = blake3(data, max_threads=blake3.AUTO)
        except (TypeError, AttributeError):
            res = blake3(data, multithreading=True)
        return res

    Path.blake3 = _blake3  # type: ignore
