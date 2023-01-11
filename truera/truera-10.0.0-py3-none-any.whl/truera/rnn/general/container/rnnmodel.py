import os
from typing import Dict, Sequence, Tuple

import numpy as np

from truera.rnn.general.aiq.clustering import SpectralHierarchicalClusterer
from truera.rnn.general.utils.mem import MemUtil
from truera.rnn.general.utils.mem import MemUtilDeps
from truera.rnn.general.utils.time import TemporalData

from . import ArtifactsContainer
from .model import ModelProxy


class RNNModelProxy(ModelProxy):

    def __init__(self):
        super(RNNModelProxy, self).__init__()

    def get_lengths(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        input_lengths=True
    ):
        name = "lengths"
        variable_lengths = [
            l.astype("int32") for l in
            MemUtil.get(artifacts_container, name, num_records, offset=offset)
        ]
        lengths = variable_lengths
        if not input_lengths:
            max_input_timesteps = self.get_data(
                artifacts_container=artifacts_container,
                num_records=num_records,
                offset=offset
            )[0].shape[1]
            max_output_timesteps = self.get_ground_truth(
                artifacts_container=artifacts_container,
                num_records=num_records,
                offset=offset
            )[0].shape[1]
            if max_input_timesteps != max_output_timesteps:
                # do not use variable lengths in output lengths if input and output lengths do not match
                lengths = [
                    [max_output_timesteps
                     for l in batch_lengths]
                    for batch_lengths in lengths
                ]
        return lengths

    # batch x timestep x feature
    def get_data(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):
        return super(RNNModelProxy, self
                    ).get_data(artifacts_container, num_records, offset=offset)

    # batch x timestep
    def get_predictions(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):
        return super(RNNModelProxy, self).get_predictions(
            artifacts_container, num_records, offset=offset
        )

    # batch x timestep
    def get_ground_truth(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):
        return super(RNNModelProxy, self).get_ground_truth(
            artifacts_container, num_records, offset=offset
        )

    def get_correlation_matrices(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset: int = 0,
        qoi_class: int = 0,
        path_max_filter=0,
        filter_top_n: int = -1
    ) -> Tuple[np.ndarray, Dict[int, int]]:
        """Gets the correlation matrices of feature-ts to feature-ts, using the pearson correlation on the token grad paths 


        Args:
            artifacts_container (ArtifactsContainer): The metadata of the model.
            num_records (int): The number of records to get.
            offset (int, optional): An offset of record id to start from. Defaults to 0.
            qoi_class (int, optional): The qoi for the influences. Defaults to 0.
            path_max_filter (float, optional): A filter to apply to remove paths with max value in the specified bottom percentage. Defaults to 0.
            filter_top_n (int, optional): Only keeps the most interacting features by pearson correlation. Defaults to -1.

        Returns:
            Tuple[np.ndarray,Dict[int,int]]: 
                corrcoef (np.ndarray) - the correlation matrix 
                idx_mapping (Dict[int,int]) - a mapping of the correlation matrix indices to a feature-ts index. 
                            usually 1:1 unless a top_n filter was applied or a token has no influence change.

        """
        grad_path_influences, grad_path_influences_column_names = self.get_grad_path_influences(
            artifacts_container,
            num_records,
            offset=offset,
            qoi_class=qoi_class
        )
        corrcoefs, idx_mappings = SpectralHierarchicalClusterer._get_correlation_matrices(
            grad_path_influences,
            path_max_filter=path_max_filter,
            filter_top_n=filter_top_n
        )
        return corrcoefs, idx_mappings, grad_path_influences_column_names

    def get_grad_path_influences(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset: int = 0,
        qoi_class: int = 0
    ) -> Tuple[Sequence[np.ndarray], Sequence[str]]:
        """
        Get the gradients per DoI. This is used for feature influence calculations.
        This is restricted on the last timestep QoI for data reduction purposes.

        Args:
            artifacts_container (ArtifactsContainer): ArtifactsContainer for the model
            num_records (int): The number of records to take
            offset (int): The starting point of records to take
            qoi_class (int): the index of the class

        Returns:
            tuple[list[np.ndarray],list[str]: The list of np.ndarray holds gradient paths per record. The gradient paths are np.ndarray of size timestep x resolution
                The list of str holds feature-timestep feature names, which are flattened by (timesteps x feature)
        """

        name = "grad_paths_last"
        # shape: (num_records, num_timesteps_in, num_postprocessed_features, resolution, num_classes)
        grad_path_influences = MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )[0]
        lengths = self.get_lengths(
            artifacts_container, num_records, offset=offset
        )[0]

        grad_path_influences = TemporalData(
            grad_path_influences, lengths,
            self.get_forward_padded(artifacts_container)
        ).defaulted_pad_transform().get_ndarray()
        # take selected class if multiple classes are given
        # shape: (num_records, num_timesteps_in, num_postprocessed_features, resolution)
        grad_path_influences = grad_path_influences[..., qoi_class]

        all_features = self.get_feature_names(artifacts_container)

        flattened_grad_paths = []
        flattened_grad_paths_column_names = []
        for length, grad_path in zip(lengths, grad_path_influences):
            num_features = grad_path.shape[2]
            num_timesteps = length
            # resolution, num_timesteps_in, num_postprocessed_features
            grad_path = grad_path[:, :num_timesteps, :]
            grad_path = np.reshape(
                grad_path, (grad_path.shape[0], num_timesteps * num_features)
            )
            grad_path = grad_path.T

            columns_names = []
            for ts in range(num_timesteps):
                for f in range(num_features):
                    feature_ts_pair = f"{all_features[f]} - T-{length - 1 - ts}"
                    columns_names.append(feature_ts_pair)
            flattened_grad_paths.append(grad_path)
            flattened_grad_paths_column_names.append(columns_names)
        return flattened_grad_paths, flattened_grad_paths_column_names

    # batch x timestep x features x timestep (out)
    def get_influences_per_timestep(
        self,
        layer,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0
    ):
        name = "%s_attrs_per_timestep" % layer

        # influences have shape (batchsize, num_timesteps_in, num_postprocessed_features, num_timesteps_out, num_classes)
        np_arrays = MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )
        for i in range(len(np_arrays)):
            np_array = np_arrays[i]
            if layer != "outer":  # influences calculated w.r.t. input features
                feature_map = self.get_feature_transform_map(
                    artifacts_container
                )
                if feature_map:  # map influences to preprocessed features
                    np_array = np.stack(
                        [
                            np_array[:, :, fs, ...].sum(axis=2)
                            for fs in feature_map
                        ], -1
                    )  # stack adding an extra axis for num_raw_features
                    np_array = np_array.transpose(
                        0, 1, 4, 2, 3
                    )  # reshape to (batchsize, num_timesteps, num_raw_features, num_timesteps, num_classes)
            np_arrays[i] = np_array
        return np_arrays

    # batch x timestep x features
    def get_influences_last(
        self,
        layer,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0
    ):
        forward_padded = self.get_forward_padded(artifacts_container)
        lengths_list = self.get_lengths(
            artifacts_container,
            num_records,
            offset=offset,
            input_lengths=False
        )
        layer_influences_list = self.get_influences_per_timestep(
            layer, artifacts_container, num_records, offset=offset
        )
        last_influence_list = []
        for lengths, layer_influences in zip(
            lengths_list, layer_influences_list
        ):
            last_influences = TemporalData(
                layer_influences, lengths, forward_padded
            ).defaulted_pad_transform().get_ndarray()
            last_influences = np.array(
                [p[:, :, l - 1] for p, l in zip(layer_influences, lengths)]
            )
            last_influence_list.append(last_influences)
        return last_influence_list

    def get_predictions_last(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):
        predictions_list = self.get_predictions(
            artifacts_container, num_records, offset=offset
        )
        lengths_list = self.get_lengths(
            artifacts_container,
            num_records,
            offset=offset,
            input_lengths=False
        )
        return [
            np.array([p[l - 1]
                      for p, l in zip(predictions, lengths)])
            for predictions, lengths in zip(predictions_list, lengths_list)
        ]

    def get_ground_truth_last(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):
        ground_truth_list = self.get_ground_truth(
            artifacts_container, num_records, offset=offset
        )
        lengths_list = self.get_lengths(
            artifacts_container,
            num_records,
            offset=offset,
            input_lengths=False
        )
        return [
            np.array([g[l - 1]
                      for g, l in zip(ground_truth, lengths)])
            for ground_truth, lengths in zip(ground_truth_list, lengths_list)
        ]

    def get_influences_reduced_last(
        self,
        layer,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        algorithm="tsne"
    ):
        name = "%s_attrs_last_%s" % (layer, algorithm)
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )

    def get_total_records(
        self, artifacts_container: ArtifactsContainer, application: MemUtilDeps
    ):
        if (application == MemUtilDeps.INPUT_ATTRS):
            filename = "input_attrs_per_timestep_shape.npy"
        elif (application == MemUtilDeps.INTERNAL_ATTRS):
            filename = "inner_attrs_per_timestep_shape.npy"
        else:
            filename = "targets_shape.npy"

        num_records = np.load(
            os.path.join(artifacts_container.get_path(), filename)
        )[0]
        return num_records
