"""Export pseudolabels module.
    TODO: Refactor into a nice class
"""
from typing import List, Callable
from pathlib import Path
import torch as tr
from ..logger import logger

def export_pseudolabels(model: "NGC", semisupervised_dirs: List[Path], next_data_dir: Path,
                        export_one_dir_fn: Callable, debug: bool):
    """Assuming a pretrained model, we'll copy/link the labels of the training directory and then, for all
    semisupervised directories, pass the data through the NGC model and save the results.
    """
    logger.debug(f"Exporting the trainDir and {len(semisupervised_dirs)} semisupervised dirs")
    logger.debug(f"Next data directory: '{next_data_dir}'")

    # Export pseudolabels for all semisupervised dirs (while copying the input nodes)
    logger.info("Exporting pseudolabels")
    model.eval()
    # Because some voting functions, like median, are not supported with determnisitic algorithms.
    prev = tr.are_deterministic_algorithms_enabled()
    tr.use_deterministic_algorithms(False)
    for i in range(len(semisupervised_dirs)):
        ss_dir = semisupervised_dirs[i]
        logger.debug2(f"Exporting for directory '{ss_dir}'")
        export_one_dir_fn(model, next_data_dir, ss_dir, postfix=i, debug=debug)
    tr.use_deterministic_algorithms(prev)
