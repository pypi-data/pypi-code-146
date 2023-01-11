"""Dir linker module"""
from typing import List
from pathlib import Path
import os
from natsort import natsorted
from ngclib.logger import logger

class DirLinker:
    """Dir linker implementation"""
    def __init__(self, ngc_dir, train_dir: Path, validation_dir: Path, semisupervised_dirs: List[Path]):
        self.ngc_dir = ngc_dir
        self.train_dir = train_dir
        self.validation_dir = validation_dir
        self.semisupervised_dirs = semisupervised_dirs

    def link_train_dir(self, iteration: int):
        """
        Creates a symlink between a training directory (given supervised data) and the data directory in the ngc_dir
        """
        node_names = self.ngc_dir.nodes["names"]
        data_dir = self.ngc_dir.path / f"iter{iteration}/data"
        logger.debug(f"Linking training dir {self.train_dir} -> {data_dir}")

        for node_name in node_names:
            out_dir = data_dir / node_name
            if out_dir.exists():
                logger.debug(f"Node out dir '{out_dir}' exists. Skipping.")
                continue
            out_dir.mkdir(exist_ok=False, parents=True)
            in_dir = self.train_dir / node_name
            in_files = natsorted([str(x) for x in in_dir.glob("*.npz")])
            out_files = [out_dir / f"train_{i}.npz" for i in range(len(in_files))]
            for in_file, out_file in zip(in_files, out_files):
                os.symlink(in_file, out_file)
        logger.debug("Finished linking training dir.")

    def link_input_nodes(self, input_nodes: List[str], iteration: int, debug: bool = False):
        """Links all inpiut nodes for this iteration based on the input nodes list."""
        data_dir = self.ngc_dir.path / f"iter{iteration}/data"
        logger.debug(f"Linking semisupervised dirs ({len(self.semisupervised_dirs)}) -> {data_dir} for all "
            f"input nodes: {input_nodes}")
        data_dir = self.ngc_dir.path / f"iter{iteration}/data"
        for j, ss_dir in enumerate(self.semisupervised_dirs):
            for node_name in input_nodes:
                assert (data_dir / node_name).exists(), data_dir / node_name
                assert (ss_dir / node_name).exists(), ss_dir / node_name
                in_files = natsorted([str(x) for x in (ss_dir / node_name).glob("*.npz")])
                in_files = in_files[0 : 5] if debug else in_files
                out_files = [data_dir / node_name / f"ss{j}_{i}.npz" for i in range(len(in_files))]
                for in_file, out_file in zip(in_files, out_files):
                    if not out_file.exists():
                        os.symlink(in_file, out_file)
        logger.debug("Finished linking input nodes for semisupervised dirs.")
