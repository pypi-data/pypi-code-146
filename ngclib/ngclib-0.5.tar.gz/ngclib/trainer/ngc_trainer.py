"""NGC Trainer module"""
from typing import List, Dict, Callable, Optional
from pathlib import Path
from nwgraph import Edge
from pytorch_lightning import Callback

from ..models import NGC
from ..logger import logger
from ..utils import DirLinker
from ..ngcdir import NGCDir

class NGCTrainer:
    """NGC trainer for N iterations. Calls NGCIterationTrainer + DirLinker + Pseudolabels code
    TODO: do the actual implementation and tests
    """
    def __init__(self, model: NGC, ngc_dir_path: Path, num_iterations: int, train_dir: Path, train_cfg: Dict,
                 validation_dir: Optional[Path] = None, semisupervised_dirs: Optional[List[Path]] = None,
                 edge_callbacks: Dict[Edge, List[Callback]] = None, augmentation_fn: Callable = None):
        if semisupervised_dirs is None:
            semisupervised_dirs = []
        if validation_dir is None:
            logger.info("No validation dir set. Using train set as validation as well.")
            validation_dir = train_dir
        if augmentation_fn is not None:
            logger.info(f"Augmentation function getter provided: {augmentation_fn}")
        else:
            logger.info("No augmentation function getter provided")

        self.model = model.to("cpu")
        self.model_cfg = model.cfg
        self.num_iterations = num_iterations
        self.edge_callbacks = edge_callbacks
        self.augmentation_fn = augmentation_fn
        self.train_cfg = train_cfg

        # ngc_dir_path.mkdir(exist_ok=True, parents=True)
        self.ngc_dir = NGCDir(ngc_dir_path, self.model_cfg)
        self.dir_linker = DirLinker(self.ngc_dir, train_dir, validation_dir, semisupervised_dirs)

        # all_dirs = self.ngc_dir.all_data_dirs(self.num_iterations)
        # self.model_dirs, self.data_dirs = all_dirs["models"], all_dirs["data"]
        # self.validation_dir = validation_dir

    def __call__(self, start_iteration: int):
        assert 0 < start_iteration < self.num_iterations, f"Got {start_iteration} not in (0, {self.num_iterations})"
        assert False, "TODO"
