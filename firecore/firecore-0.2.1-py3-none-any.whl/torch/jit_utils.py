from pathlib import Path
import functools
import torch
from firecore.logging import get_logger

logger = get_logger(__name__)


class AutoExporter:
    def __init__(self, path: str) -> None:
        export_dir = Path(path)

        logger.debug('make dirs', export_dir=export_dir)
        export_dir.mkdir(parents=True, exist_ok=True)

        self._export_dir = export_dir

    def trace(self, func):
        scripted_func = None
        func_name: str = func.__name__

        """
        The jitted function have no kwargs
        and must return single tensor or tuple of tensor
        """
        @functools.wraps(func)
        def f(*args):
            nonlocal scripted_func
            if scripted_func is None:
                scripted_func = torch.jit.trace(func, args)
                output_path = self._export_dir / '{}.pt'.format(func_name)
                logger.debug(
                    'save scripted funcion',
                    output_path=output_path
                )
                scripted_func.save(str(output_path))

            return scripted_func(*args)

        return f
