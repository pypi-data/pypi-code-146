from enum import Enum
import math
import os

import numpy as np
import yaml

from truera.rnn.general.container import ArtifactsContainer


class MemUtilDeps(Enum):
    '''
    Levels of MemUtil dependencies based on application. 
    '''
    NO_DEPS = []
    NO_ATTRS = ['preds', 'targets', 'keys', 'data']
    INPUT_ATTRS = NO_ATTRS + ['input_attrs_per_timestep']
    INTERNAL_ATTRS = NO_ATTRS + [
        'outer_attrs_per_timestep', 'inner_attrs_per_timestep'
    ]
    ALL_ATTRS = list(set(INPUT_ATTRS + INTERNAL_ATTRS))

    def get_names(self):
        return self.value

    @classmethod
    def get_dep_level(cls, name):
        if name in cls.NO_ATTRS.value:
            return cls.NO_ATTRS
        elif name in cls.INPUT_ATTRS.value:
            return cls.INPUT_ATTRS
        elif name in cls.INTERNAL_ATTRS.value:
            return cls.INTERNAL_ATTRS
        return cls.NO_DEPS


class MemUtil():
    file_pointers = {}
    GBS_PER_BATCH = 0.5
    # Only allow up to 0.5 GB to be loaded into memory per datastructure
    # Some good machines can go 2-4GB, but keeping low in case deployed machine has memory limits
    MAX_BYTES_ALLOWED = pow(1024, 3) * GBS_PER_BATCH
    # 32 bit floats are 4 bytes
    MAX_ELEMENTS_ALLOWED = MAX_BYTES_ALLOWED / 4
    MAX_DATAPOINTS_UI = 20000  # ballparked from Dash/Plotly forums

    @staticmethod
    def _get_artifact_config(artifacts_container):
        config_path = os.path.join(
            artifacts_container.get_path(), 'artifact_config.yaml'
        )
        if not os.path.exists(config_path):
            return {}
        with open(config_path, 'r') as h:
            cfg = yaml.safe_load(h)
        return cfg

    @staticmethod
    def get_forward_padded(artifacts_container: ArtifactsContainer):
        '''
        Returns whether model is forward padded, defaulting to False.
        '''
        config = MemUtil._get_artifact_config(artifacts_container)
        return config.get('forward_padded', False)

    @staticmethod
    def get_data_dtype(artifacts_container: ArtifactsContainer):
        '''
        Returns dtype with which to load preprocessed model input
        '''
        config = MemUtil._get_artifact_config(artifacts_container)
        return config.get('data_dtype', 'float32')

    @staticmethod
    def _get_total_records(artifacts_container: ArtifactsContainer):
        '''
        Returns total number of records for given project/model/data collection/split.
        '''
        path = artifacts_container.get_path()
        name = 'data_shape.npy'
        data_shape = np.load(os.path.join(path, name))
        return data_shape[0]

    @staticmethod
    def get_total_timesteps(
        artifacts_container: ArtifactsContainer, input_timesteps=True
    ):
        '''
        Returns total number of records for given project/model/data collection/split.
        '''
        path = artifacts_container.get_path()
        name = 'input_attrs_per_timestep_shape.npy'
        data_shape = np.load(os.path.join(path, name))
        if input_timesteps:
            return data_shape[1]
        else:
            return data_shape[3]

    @staticmethod
    def get_num_internal_neurons(artifacts_container: ArtifactsContainer):
        path = artifacts_container.get_path()
        name = 'outer_attrs_per_timestep_shape.npy'
        data_shape = np.load(os.path.join(path, name))
        return data_shape[2]

    @staticmethod
    def get_max_batchsize(
        artifacts_container: ArtifactsContainer, dep_level, dtype='float32'
    ):
        '''
        Returns maximum batchsize allowed given memory constraints of page, 
        as well as the maximum batchsize ignoring memory constraints (total number of records) 
        '''
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
        path, name, batch, batch_size, offset=0, dtype='float32'
    ):
        batch = int(batch)
        batch_size = int(batch_size)
        MemUtil.free(path, name)
        try:
            fp = MemUtil.load(path, name, dtype=dtype)
        except:
            if name == 'keys':
                fp = MemUtil.load(
                    path, name, dtype='int32'
                )  # try to decode keys as ints first
            else:
                fp = MemUtil.load(path, name)

        data_shape = np.asarray(fp.shape)
        data_shape[0] = min(batch_size, data_shape[0] - batch * batch_size)
        num_elements = np.prod(data_shape)
        if (num_elements > MemUtil.MAX_ELEMENTS_ALLOWED):
            raise Exception(
                "Trying to load more " +
                '{0:.2f}'.format(num_elements / MemUtil.MAX_ELEMENTS_ALLOWED) +
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
    def get(
        artifacts_container: ArtifactsContainer,
        name,
        num_records,
        offset=0,
        dtype='float32'
    ):
        path = artifacts_container.get_path()
        max_batchsize, _ = MemUtil.get_max_batchsize(
            artifacts_container, MemUtilDeps.get_dep_level(name), dtype=dtype
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
    def load(path, name, dtype=None):
        key = os.path.join(path, name)
        if not dtype:
            dtype_file = f'{key}_dtype.txt'
            if os.path.exists(dtype_file):
                dtype = open(os.path.join(dtype_file)).read().strip()
            else:
                dtype = 'float32'

        if key not in MemUtil.file_pointers:
            shape = np.load(key + "_shape.npy")
            fp = np.memmap(
                key + ".dat", dtype=dtype, mode='r', shape=tuple(shape)
            )
            MemUtil.file_pointers[key] = fp
        return MemUtil.file_pointers[key]

    @staticmethod
    def free(path, name):
        key = os.path.join(path, name)
        if key in MemUtil.file_pointers:
            fp = MemUtil.file_pointers[key]
            del fp
            del MemUtil.file_pointers[key]
