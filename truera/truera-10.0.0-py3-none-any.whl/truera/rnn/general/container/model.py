import json
import os
from typing import Sequence

import numpy as np
import pandas as pd

from truera.rnn.general.model_runner_proxy.general_utils import load_yaml
from truera.rnn.general.utils.mem import MemUtil
from truera.rnn.general.utils.mem import MemUtilDeps

from .artifacts import ArtifactsContainer


class ModelProxy(object):

    def __init__(self):
        self.feature_names = {}
        self.feature_descriptions = {}
        self.feature_transform_map = {}
        self.nonnumeric_feature_map = {}
        self.forward_padded = {}
        self.data_dtype = {}
        self.input_influences = None
        self.outer_influences = None
        self.outer_influences_reduced = {'tsne': None, 'pca': None}
        self.input_influences_reduced = {'tsne': None, 'pca': None}
        self.inner_influences = None
        self.x_data = None
        self.predictions = None
        self.ground_truth = None
        self.record_ids = None

    def get_forward_padded(self, artifacts_container: ArtifactsContainer):
        artifacts_path = artifacts_container.get_path()
        if artifacts_path not in self.forward_padded:
            self.forward_padded[artifacts_path] = MemUtil.get_forward_padded(
                artifacts_container
            )
        return self.forward_padded[artifacts_path]

    def get_data_dtype(self, artifacts_container: ArtifactsContainer):
        artifacts_path = artifacts_container.get_path()
        if artifacts_path not in self.data_dtype:
            self.data_dtype[artifacts_path] = MemUtil.get_data_dtype(
                artifacts_container
            )
        return self.data_dtype[artifacts_path]

    def get_feature_names(self, artifacts_container: ArtifactsContainer):
        artifacts_path = artifacts_container.get_path()
        if (artifacts_path in self.feature_names):
            return self.feature_names[artifacts_path]

        feature_df = pd.read_csv(
            os.path.join(artifacts_path, 'feature_names.csv')
        )
        features = []
        for f in feature_df.columns.str.lower():
            features.append(f)
        self.feature_names[artifacts_path] = features
        return self.feature_names[artifacts_path]

    def get_feature_descriptions(self, artifacts_container: ArtifactsContainer):
        artifacts_path = artifacts_container.get_path()
        if (artifacts_path in self.feature_descriptions):
            return self.feature_descriptions[artifacts_path]

        json_canonical = json.loads('{}')
        with open(
            os.path.join(artifacts_path, 'feature_dict.json'), 'r'
        ) as json_file:
            json_load = json.load(json_file)

        for key in json_load:
            json_canonical[key.lower()] = json_load[key]

        self.feature_descriptions[artifacts_path] = json_canonical
        return self.feature_descriptions[artifacts_path]

    def get_feature_transform_map(
        self, artifacts_container: ArtifactsContainer
    ):
        artifacts_path = artifacts_container.get_path()
        if (artifacts_path in self.feature_transform_map):
            return self.feature_transform_map[artifacts_path]

        feature_names = self.get_feature_names(artifacts_container)
        feature_transform_path = os.path.join(
            artifacts_path, 'feature_transform_map.json'
        )
        if not os.path.exists(feature_transform_path):
            feature_map = []
        else:
            with open(feature_transform_path, 'r') as json_file:
                raw_feature_map = json.load(json_file)
            # maps preprocessed col index -> list of postprocessed col indices
            feature_map = []
            postprocessed_cols = 0
            for f in feature_names:
                num_cols = raw_feature_map.get(f, 1)
                feature_map.append(
                    list(
                        range(
                            postprocessed_cols, postprocessed_cols + num_cols
                        )
                    )
                )
                postprocessed_cols += num_cols

        self.feature_transform_map[artifacts_path] = feature_map
        return self.feature_transform_map[artifacts_path]

    def get_nonnumeric_feature_map(
        self, artifacts_container: ArtifactsContainer
    ):
        artifacts_path = artifacts_container.get_path()
        if (artifacts_path in self.nonnumeric_feature_map):
            return self.nonnumeric_feature_map[artifacts_path]
        map_path = os.path.join(artifacts_path, 'feature_nonnumeric_map.json')
        nonnumeric_feature_map = {}

        # initialize feature map from file
        if os.path.exists(map_path):
            with open(map_path, 'r') as h:
                nonnumeric_feature_map = json.load(h)
        for feature_name, feature_vals in nonnumeric_feature_map.items():
            if all([val.isdigit() for val in feature_vals]):
                nonnumeric_feature_map[feature_name] = {
                    int(k): v for k, v in feature_vals.items()
                }

        # grab data slice to supplement map
        num_records = min(
            self.get_total_records(artifacts_container, MemUtilDeps.NO_ATTRS),
            1000
        )
        feature_names = self.get_feature_names(artifacts_container)
        features = self.get_data(artifacts_container, num_records)[0]
        features = features.reshape(
            features.shape[0] * features.shape[1], features.shape[-1]
        )
        for i, feature_name in enumerate(feature_names):
            if feature_name in nonnumeric_feature_map:
                continue
            feature_vals = features[:, i]
            is_numeric = np.issubdtype(feature_vals.dtype, np.number)
            unique_feature_vals = np.unique(feature_vals)
            if len(unique_feature_vals) <= 10 or not is_numeric:
                nonnumeric_feature_map[feature_name] = {
                    v: v for v in unique_feature_vals
                }
        self.nonnumeric_feature_map[artifacts_path] = nonnumeric_feature_map
        return nonnumeric_feature_map

    def get_data(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset: int = 0
    ) -> Sequence[np.memmap]:
        name = 'data'
        dtype = MemUtil.get_data_dtype(artifacts_container)
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset, dtype=dtype
        )

    def get_influences_reduced(
        self,
        layer,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        algorithm='tsne'
    ):
        name = '%s_attrs_%s' % (layer, algorithm)
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )

    def get_predictions(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):
        name = 'preds'
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )

    def get_ground_truth(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):

        name = 'targets'
        return [
            x.astype('float32') for x in
            MemUtil.get(artifacts_container, name, num_records, offset=offset)
        ]

    def get_record_ids(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):
        name = 'keys'
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset, dtype='U32'
        )

    def get_max_batchsize(
        self, artifacts_container: ArtifactsContainer, dep_level
    ):
        return MemUtil.get_max_batchsize(artifacts_container, dep_level)

    def get_total_timesteps(
        self, artifacts_container: ArtifactsContainer, input_timesteps=True
    ):
        return MemUtil.get_total_timesteps(
            artifacts_container, input_timesteps=input_timesteps
        )

    def get_num_internal_neurons(self, artifacts_container: ArtifactsContainer):
        return MemUtil.get_num_internal_neurons(artifacts_container)

    def get_total_records(
        self, artifacts_container: ArtifactsContainer, application: MemUtilDeps
    ):
        raise NotImplementedError
