from enum import Enum
import math
import os
from pathlib import Path
import pickle as pkl
from typing import Any, Iterable, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import yaml

from truera.nlp.general.model_runner_proxy.mem_utils import load_text_data
from truera.rnn.general.container.artifacts import ArtifactsContainer


class TorchUtils(object):
    import gc
    import sys

    import humanize
    import torch

    @staticmethod
    def tensor_memory_usage(tensors: Iterable[torch.Tensor]) -> Tuple[int, int]:
        """Given a list of tensors, return how many basic elements they contain and how much memory (bytes) they represent.
        """

        # https://gist.github.com/Stonesjtu/368ddf5d9eb56669269ecdf9b0d21cbe

        visited = set()

        total_memory = 0
        total_memory_sys = 0
        total_elements = 0

        for tensor in tensors:
            if tensor.is_sparse:
                continue

            data_ptr = tensor.storage().data_ptr()

            if data_ptr in visited:
                continue

            visited.add(data_ptr)

            number_elements = tensor.storage().size()
            total_elements += number_elements

            element_size = tensor.storage().element_size()
            memory = number_elements * element_size

            memory_sys = TorchUtils.sys.getsizeof(tensor.storage())

            total_memory += memory
            total_memory_sys += memory_sys

        return total_elements, total_memory, total_memory_sys

    @staticmethod
    def tensor_memory_report() -> None:
        """"Print out tensor memory usage information. Make sure to call this in a context where your tensors cannot be
        yet be garbage collected.
        """
        # https://gist.github.com/Stonesjtu/368ddf5d9eb56669269ecdf9b0d21cbe

        objects = TorchUtils.gc.get_objects()
        tensors = [obj for obj in objects if TorchUtils.torch.is_tensor(obj)]
        cuda_tensors = [t for t in tensors if t.is_cuda]
        host_tensors = [t for t in tensors if not t.is_cuda]

        def gnusize(n):
            return TorchUtils.humanize.naturalsize(n, gnu=True)

        cuda_usage = TorchUtils.tensor_memory_usage(cuda_tensors)
        print(
            "cuda", TorchUtils.humanize.intcomma(cuda_usage[0]),
            gnusize(cuda_usage[1]), gnusize(cuda_usage[2])
        )

        stats = TorchUtils.torch.cuda.memory_stats()
        peak_alloc = stats["allocated_bytes.all.peak"]
        total_alloc = stats["allocated_bytes.all.allocated"]

        batch_inefficiency = float(total_alloc) / float(peak_alloc)

        print(
            f"cuda memory allocated: "
            f"peak={gnusize(peak_alloc)}, "
            f"total={gnusize(total_alloc)}, "
            f"total/peak={batch_inefficiency:0.3f}"
        )

        print(TorchUtils.torch.cuda.memory_summary())

        host_usage = TorchUtils.tensor_memory_usage(host_tensors)
        print(
            "host", TorchUtils.humanize.intcomma(host_usage[0]),
            gnusize(host_usage[1]), gnusize(cuda_usage[2])
        )


class MemUtilDeps(Enum):
    """
    Levels of MemUtil dependencies based on application. 
    """
    NO_DEPS = []
    NO_ATTRS = ["preds", "targets", "token_ids"]
    INPUT_ATTRS = NO_ATTRS + ["max_class_token_attrs"]
    ALL_ATTRS = list(set(INPUT_ATTRS))

    def get_names(self):
        return self.value

    @classmethod
    def get_dep_level(cls, name):
        if name in cls.NO_ATTRS.value:
            return cls.NO_ATTRS
        elif name in cls.INPUT_ATTRS.value:
            return cls.INPUT_ATTRS
        return cls.NO_DEPS


class MemUtil():
    file_pointers = {}
    # Only allow up to 2GB to be loaded into memory per datastructure
    MAX_BYTES_ALLOWED = pow(1024, 3) * 2
    # 32 bit floats are 4 bytes
    MAX_ELEMENTS_ALLOWED = MAX_BYTES_ALLOWED / 4
    MAX_DATAPOINTS_UI = 20000  # ballparked from Dash/Plotly forums

    @staticmethod
    def _get_artifact_config(artifacts_container):
        config_path = os.path.join(
            artifacts_container.get_path(), "artifact_config.yaml"
        )
        if not os.path.exists(config_path):
            return {}
        with open(config_path, "r") as h:
            cfg = yaml.safe_load(h)
        return cfg

    @staticmethod
    def get_forward_padded(artifacts_container: ArtifactsContainer) -> bool:
        """
        Returns whether model is forward padded, defaulting to False.
        """
        config = MemUtil._get_artifact_config(artifacts_container)
        return config.get("forward_padded", False)

    @staticmethod
    def get_data_dtype(artifacts_container: ArtifactsContainer) -> str:
        """
        Returns dtype with which to load preprocessed model input
        """
        config = MemUtil._get_artifact_config(artifacts_container)
        return config.get("token_ids_dtype", "float32")

    @staticmethod
    def _get_total_records(
        artifacts_container: ArtifactsContainer,
        influences: bool = False
    ) -> int:
        """Get the total number of records generated. This will be based off the number of records for metrics.
        If influences is True, this will be based off the number of records for influences.

        Args:
            artifacts_container (ArtifactsContainer): The artifact metadata.
            influences (bool, optional): Whether to use metrics or influences counts. Defaults to False.

        Returns:
            int: The number of records.
        """
        path = artifacts_container.get_path()
        if influences:
            name = "class_token_attrs_shape.npy"
        else:
            name = "token_ids_shape.npy"
        data_shape = np.load(os.path.join(path, name))
        return data_shape[0]

    @staticmethod
    def get_total_timesteps(artifacts_container: ArtifactsContainer) -> int:
        """
        Returns total number of records for given project/model/data collection/split.
        """
        path = artifacts_container.get_path()
        name = "token_ids_shape.npy"
        data_shape = np.load(os.path.join(path, name))
        return data_shape[1]

    @staticmethod
    def get_num_internal_neurons(
        artifacts_container: ArtifactsContainer
    ) -> int:
        path = artifacts_container.get_path()
        name = "outer_attrs_per_timestep_shape.npy"
        data_shape = np.load(os.path.join(path, name))
        return data_shape[2]

    @staticmethod
    def get_max_batchsize(
        artifacts_container: ArtifactsContainer,
        dep_level: MemUtilDeps,
        dtype: Union[str, np.dtype] = "float32"
    ) -> int:
        """
        Returns maximum batchsize allowed given memory constraints of page, 
        as well as the maximum batchsize ignoring memory constraints (total number of records) 
        """
        total_records = MemUtil._get_total_records(artifacts_container)
        batch_sizes = [total_records]
        for name in dep_level.get_names():
            path = artifacts_container.get_path()
            MemUtil.free(path, name)
            try:
                fp = MemUtil.load(path, name, dtype=dtype)
            except:
                fp = MemUtil.load(path, name)
            data_shape = np.asarray(fp.shape)
            data_shape[0] = 1  # assume batch size is 1
            max_batchsize = MemUtil.MAX_ELEMENTS_ALLOWED // np.prod(
                data_shape
            )  # max memory-constrained batchsize
            MemUtil.free(path, name)
            batch_sizes.append(max_batchsize)
        return int(np.min(batch_sizes)), total_records

    @staticmethod
    def _get_singlebatch(
        path: str,
        name: str,
        batch: int,
        batch_size: int,
        offset: int = 0,
        dtype: Union[str, np.dtype] = "float32"
    ) -> np.memmap:
        batch = int(batch)
        batch_size = int(batch_size)
        MemUtil.free(path, name)
        try:
            fp = MemUtil.load(path, name, dtype=dtype)
        except:
            if name == "keys":
                fp = MemUtil.load(
                    path, name, dtype="int32"
                )  # try to decode keys as ints first
            else:
                fp = MemUtil.load(path, name)

        data_shape = np.asarray(fp.shape)
        data_shape[0] = min(batch_size, data_shape[0] - batch * batch_size)
        num_elements = np.prod(data_shape)
        if (num_elements > MemUtil.MAX_ELEMENTS_ALLOWED):
            raise Exception(
                "Trying to load more " +
                "{0:.2f}".format(num_elements / MemUtil.MAX_ELEMENTS_ALLOWED) +
                " times more data than is safe. Please reduce batch size."
            )
        start = (batch * batch_size) + offset
        end = ((batch + 1) * batch_size) + offset
        mem_loaded_fp = fp[start:end]
        if (len(mem_loaded_fp) <= 0):
            raise Exception("No more samples to batch.")
        MemUtil.free(path, name)
        try:
            round_mem_loaded_fp = np.memmap.round(mem_loaded_fp, decimals=5)
            return round_mem_loaded_fp
        except:
            return mem_loaded_fp

    @staticmethod
    def get_pickle(
        artifacts_container: ArtifactsContainer,
        name: str,
        num_records: Optional[int] = None,
        offset: int = 0
    ) -> Any:
        path = artifacts_container.get_path()
        pkl_path = os.path.join(path, "{}.pkl".format(name))

        if not os.path.exists(pkl_path):
            raise FileNotFoundError(
                f"Missing path in MemUtil.get_pickle() for name {name}: {pkl_path}"
            )

        with open(pkl_path, "rb") as f:
            pickle_object = pkl.load(f)
        if num_records == None:
            return pickle_object
        return pickle_object[offset:num_records + offset]

    @staticmethod
    def get_df_from_csv(
        artifacts_container: ArtifactsContainer, name: str
    ) -> pd.DataFrame:
        path = artifacts_container.get_path()
        df = pd.read_csv(
            os.path.join(path, "{}.csv".format(name)),
            encoding="L1",
            index_col=0
        )
        return df

    @staticmethod
    def get_text(
        artifacts_container: ArtifactsContainer,
        name: str,
        num_records: int,
        offset: int = 0
    ) -> Sequence[str]:
        # TODO: use Paths upstream from here
        path = Path(artifacts_container.get_path())

        list = load_text_data(path, name)

        return list[offset:num_records + offset]

    @staticmethod
    def get(
        artifacts_container: ArtifactsContainer,
        name: str,
        num_records: int,
        offset: int = 0,
        dtype: Union[str, np.dtype] = "float32"
    ) -> Sequence[np.memmap]:
        """
        Returns a list of np.memmap items corresponding to the type specified by name.
        The return type is list so that memmaps are broken up into properly sized memory chunks which
        are calculated by MemUtil.get_max_batchsize.

        Args:
            name (str): The name of the backing files saved in artifact generation
            num_records (int): The total number of records to return
            offset (int): An offset to the start of the records to return
            dtype (str): The dtype of the underlying memmap

        Returns:
            Sequence[np.memmap]: Returns a list of np.memmap items. list items are memmaps that 
            are broken up into properly sized memory chunks which calculated by MemUtil.get_max_batchsize.
        """
        path = artifacts_container.get_path()
        max_batchsize, _ = MemUtil.get_max_batchsize(
            artifacts_container, MemUtilDeps.get_dep_level(name), dtype=dtype
        )

        num_records = min(
            num_records,
            MemUtil.load(path, name, dtype=dtype, force_reload=True).shape[0]
        )

        num_batches = math.ceil(num_records / max_batchsize)
        remaining_records = num_records
        data = []
        for batch in range(num_batches):
            batchsize = min(max_batchsize, remaining_records)
            data.append(
                MemUtil._get_singlebatch(
                    path, name, batch, batchsize, offset=offset, dtype=dtype
                )
            )
            remaining_records -= batchsize
        return data

    @staticmethod
    def load(
        path: str,
        name: str,
        dtype: Union[str, np.dtype] = "float32",
        force_reload: bool = False
    ) -> np.memmap:
        key = os.path.join(path, name)
        if force_reload or key not in MemUtil.file_pointers:
            shape = np.load(key + "_shape.npy")
            fp = np.memmap(
                key + ".dat", dtype=dtype, mode="r", shape=tuple(shape)
            )
            MemUtil.file_pointers[key] = fp
        return MemUtil.file_pointers[key]

    @staticmethod
    def free(path: str, name: str) -> None:
        key = path + name
        if key in MemUtil.file_pointers:
            fp = MemUtil.file_pointers[key]
            del fp
            del MemUtil.file_pointers[key]
