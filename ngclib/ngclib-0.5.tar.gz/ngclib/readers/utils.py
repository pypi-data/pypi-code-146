"""Readers utils module"""
from typing import Dict
import torch as tr
from torch.utils.data import DataLoader, Subset
from .ngc_npz_reader import NGCNpzReader
from ..logger import logger

def reader_to_data_loader(reader: NGCNpzReader, train_cfg: Dict, shuffle: bool = False,
                          debug: bool = False) -> DataLoader:
    """Creates a dataloader from ngc npz reader, but also applies determinism and others if needed."""
    if train_cfg is None or "loader_params" not in train_cfg:
        logger.debug("No train cfg or loader params provided, defaulting to an empty dict")
        train_cfg = {"loader_params": {}}

    loader_params = train_cfg["loader_params"]
    if "shuffle" in loader_params:
        logger.warning(f"shuffle in loader params, but is being overriden by parameter '{shuffle}'")
    if debug:
        logger.info("Debug mode. Yielding a subset of 10, num_workers 0 and no shuffle")
        loader_params["num_workers"] = 0
        shuffle = False
        reader = Subset(reader, range(10))
        reader.collate_fn = reader.dataset.collate_fn

    loader_params["collate_fn"] = reader.collate_fn
    loader_params["num_workers"] = loader_params["num_workers"] if "num_workers" in loader_params else 0
    loader_params["shuffle"] = shuffle

    loader_params["generator"] = None
    if "seed" in train_cfg and train_cfg["seed"] is not None:
        generator = tr.Generator()
        generator.manual_seed(train_cfg["seed"])
        loader_params["generator"] = generator
    logger.debug(f"Creating dataloader: {loader_params}")
    loader = DataLoader(reader, **loader_params)
    return loader
