import math
import os
from typing import Optional, Sequence

import numpy as np
import pandas as pd
import progressbar

from truera.rnn.general.aiq import AIQ
from truera.rnn.general.aiq import influences as Influences
from truera.rnn.general.aiq import input_inf_utils as ii_utils
from truera.rnn.general.aiq.clustering import SpectralHierarchicalClusterer
from truera.rnn.general.container import ArtifactsContainer
from truera.rnn.general.frontend.component import ComponentData
from truera.rnn.general.model_runner_proxy.general_utils import load_yaml
from truera.rnn.general.selection.interaction_selection import \
    AggregationMethod
from truera.rnn.general.selection.interaction_selection import FeatureSpace
from truera.rnn.general.selection.interaction_selection import \
    InfluenceAggregationMethod
from truera.rnn.general.selection.interaction_selection import InteractAlong
from truera.rnn.general.selection.interaction_selection import InteractionType
from truera.rnn.general.selection.interaction_selection import LocalExpSortMode
from truera.rnn.general.selection.swap_selection import SwapComparisons
from truera.rnn.general.utils.errors import FilterError
from truera.rnn.general.utils.mem import MemUtilDeps
from truera.rnn.general.utils.metrics import get_available_metric_names
from truera.rnn.general.utils.metrics import get_class_breakdowns
from truera.rnn.general.utils.metrics import get_stats
from truera.rnn.general.utils.metrics import get_threshold_from_pct
from truera.rnn.general.utils.time import TemporalData


class RnnAIQ(AIQ):

    def _get_sample_index_from_batched(
        self, data_list, sample_index, return_index=False
    ):
        batchsize = len(data_list[0])
        batch = sample_index // batchsize
        batch_index = sample_index - (batch * batchsize)
        if return_index:
            return batch, batch_index
        return data_list[batch][batch_index]

    def _align_influences_timestep(self, influence_list, timestep_list):
        # used to properly chunk batches of influences/timesteps for further analysis
        total_inf_records = sum([len(l) for l in influence_list])
        total_timestep_records = sum([len(l) for l in timestep_list])
        assert total_inf_records == total_timestep_records, "Internal error: number of timesteps does not match number of influences."
        all_timesteps = np.concatenate(timestep_list, axis=0)
        return influence_list, np.array_split(
            all_timesteps, len(influence_list)
        )

    def get_total_timesteps(
        self, artifacts_container: ArtifactsContainer, input_timesteps=True
    ):
        return self.model.get_total_timesteps(
            artifacts_container, input_timesteps=input_timesteps
        )

    def get_total_records(
        self, artifacts_container: ArtifactsContainer, application: MemUtilDeps
    ):
        return self.model.get_total_records(artifacts_container, application)

    def get_max_batchsize(
        self, artifacts_container: ArtifactsContainer, dep_level
    ):
        return self.model.get_max_batchsize(artifacts_container, dep_level)

    def get_feature_names(
        self, artifacts_container: ArtifactsContainer, internal=False
    ):
        if internal:
            num_neurons = self.model.get_num_internal_neurons(
                artifacts_container
            )
            return ["neuron {}".format(i) for i in range(num_neurons)]
        return self.model.get_feature_names(artifacts_container)

    def get_default_threshold(self, artifacts_container: ArtifactsContainer):
        artifacts_path = artifacts_container.get_path()
        run_config_path = os.path.join(artifacts_path, "run_config.yaml")
        if not os.path.exists(run_config_path):
            return 0.5
        run_args = load_yaml(run_config_path)
        if not hasattr(run_args, "default_threshold"
                      ) or not run_args.default_threshold or not isinstance(
                          run_args.default_threshold, float
                      ):
            return 0.5
        else:
            return run_args.default_threshold

    def get_nonnumeric_feature_map(
        self, artifacts_container: ArtifactsContainer
    ):
        return self.model.get_nonnumeric_feature_map(artifacts_container)

    def get_formatted_feature_descriptions(
        self, artifacts_container: ArtifactsContainer, features
    ):
        feature_descriptions = self.model.get_feature_descriptions(
            artifacts_container
        )
        formatted_descriptions = []
        for feature in features:
            desc = feature_descriptions[feature]
            if "high_level_description" in desc:
                desc = desc["high_level_description"]
            formatted_descriptions.append(desc)
        return formatted_descriptions

    def get_concatenated_feature_descriptions(
        self, artifacts_container: ArtifactsContainer, features
    ):
        feature_descs = self.get_formatted_feature_descriptions(
            artifacts_container, features
        )
        return [
            "{}: {}".format(name, desc)
            for name, desc in zip(features, feature_descs)
        ]

    def get_record_ids(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        sample_index=None
    ):
        record_ids = self.model.get_record_ids(
            artifacts_container, num_records, offset=offset
        )
        if sample_index is not None:
            return self._get_sample_index_from_batched(record_ids, sample_index)
        return np.squeeze(np.concatenate(record_ids, axis=0))

    def get_lengths(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        sample_index=None,
        input_lengths=True
    ):
        lengths_list = self.model.get_lengths(
            artifacts_container,
            num_records,
            offset=offset,
            input_lengths=input_lengths
        )
        if sample_index is not None:
            return self._get_sample_index_from_batched(
                lengths_list, sample_index
            )
        return np.concatenate(lengths_list, axis=0)

    def get_data(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        sample_index=None,
        feature_index=None
    ):
        lengths = self.model.get_lengths(
            artifacts_container, num_records, offset=offset
        )
        forward_padded = self.model.get_forward_padded(artifacts_container)
        data = self.model.get_data(
            artifacts_container, num_records, offset=offset
        )
        if feature_index is not None:
            data = [d[..., feature_index] for d in data]
        if sample_index is not None:
            batch, batch_index = self._get_sample_index_from_batched(
                data, sample_index, return_index=True
            )
            temp_data = TemporalData(
                data[batch], lengths[batch], forward_padded
            ).defaulted_pad_transform().get_ndarray()
            return temp_data[batch_index]
        lengths = np.concatenate(lengths, axis=0)
        data = np.concatenate(data, axis=0)
        data = TemporalData(data, lengths, forward_padded
                           ).defaulted_pad_transform().get_ndarray()
        return data

    def get_predictions(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        sample_index=None,
        class_index=None,
        convert_class_int: bool = False
    ):
        lengths = self.model.get_lengths(
            artifacts_container, num_records, offset=offset
        )
        forward_padded = self.model.get_forward_padded(artifacts_container)
        preds = self.model.get_predictions(
            artifacts_container, num_records, offset=offset
        )
        if sample_index is not None:
            batch, batch_index = self._get_sample_index_from_batched(
                preds, sample_index, return_index=True
            )
            temp_data = TemporalData(
                preds[batch], lengths[batch], forward_padded
            ).defaulted_pad_transform().get_ndarray()
            preds = temp_data[batch_index]
        else:
            lengths = np.concatenate(lengths, axis=0)
            preds = np.concatenate(preds, axis=0)
            preds = TemporalData(preds, lengths, forward_padded
                                ).defaulted_pad_transform().get_ndarray()
        if class_index is not None:
            preds = preds[..., class_index]
        elif convert_class_int:
            if (preds.shape[-1]) != 1:
                preds = np.argmax(preds, axis=-1)
            else:
                preds = preds[..., 0]
        return preds

    def get_predictions_last(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        sample_index=None,
        class_index=None
    ):
        preds = self.model.get_predictions_last(
            artifacts_container, num_records, offset=offset
        )
        if sample_index is not None:
            preds = self._get_sample_index_from_batched(preds, sample_index)
        else:
            preds = np.concatenate(preds, axis=0)
        if class_index is not None:
            preds = preds[..., class_index]
        return preds

    def get_ground_truth(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        sample_index=None,
        class_index=None,
        convert_class_int: bool = False
    ):
        lengths = self.model.get_lengths(
            artifacts_container, num_records, offset=offset
        )
        forward_padded = self.model.get_forward_padded(artifacts_container)
        labels = self.model.get_ground_truth(
            artifacts_container, num_records, offset=offset
        )
        labels_before_before = labels
        if sample_index is not None:
            batch, batch_index = self._get_sample_index_from_batched(
                labels, sample_index, return_index=True
            )
            temp_data = TemporalData(
                labels[batch], lengths[batch], forward_padded
            ).defaulted_pad_transform().get_ndarray()
            labels = temp_data[batch_index]
        else:
            lengths = np.concatenate(lengths, axis=0)
            labels = np.concatenate(labels, axis=0)
            labels = TemporalData(labels, lengths, forward_padded
                                 ).defaulted_pad_transform().get_ndarray()
        if class_index is not None:
            labels = labels[..., class_index]
        elif convert_class_int:
            if (labels.shape[-1]) != 1:
                labels = np.argmax(labels, axis=-1)
            else:
                labels = labels[..., 0]

        return labels

    def get_ground_truth_last(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        sample_index=None,
        class_index=None
    ):
        labels = self.model.get_ground_truth_last(
            artifacts_container, num_records, offset=offset
        )
        if sample_index is not None:
            labels = self._get_sample_index_from_batched(labels, sample_index)
        else:
            labels = np.concatenate(labels, axis=0)
        if class_index is not None:
            labels = labels[..., class_index]
        return labels

    def get_influences_per_timestep(
        self,
        layer,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        sample_index=None,
        class_index=None,
        feature_index=None
    ):
        """Returns influences matrix with shape (num_records, num_timesteps, num_features, num_timesteps, num_classes)
        Where axis 1 is indexed such that index 0 correspond to the influence for the last timestep of that particular record
        """
        forward_padded = self.model.get_forward_padded(artifacts_container)
        influences = self.model.get_influences_per_timestep(
            layer, artifacts_container, num_records, offset=offset
        )
        lengths = self.model.get_lengths(
            artifacts_container, num_records, offset=offset
        )
        influences, lengths = self._align_influences_timestep(
            influences, lengths
        )
        if feature_index is not None:
            influences = [inf[:, :, feature_index] for inf in influences]
        if sample_index is not None:
            batch, batch_index = self._get_sample_index_from_batched(
                influences, sample_index, return_index=True
            )
            temp_data = TemporalData(
                influences[batch], lengths[batch], forward_padded
            ).defaulted_pad_transform().get_ndarray()
            influences = temp_data[batch_index]
        else:
            lengths = np.concatenate(lengths, axis=0)
            influences = np.concatenate(influences, axis=0)
            influences = TemporalData(influences, lengths, forward_padded
                                     ).defaulted_pad_transform().get_ndarray()
        if class_index is not None:
            influences = influences[..., class_index]
        return influences

    def get_influences_from_qoi(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        qoi_core_class,
        qoi_compare_class,
        qoi,
        offset=0,
        qoi_timestep=0,
        pred_thresh=0.5,
        from_layer="input",
        neuron=None,
        feature_index=None
    ):
        return Influences.get_influences_from_qoi(
            self,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            artifacts_container,
            num_records,
            offset=offset,
            pred_thresh=pred_thresh,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            neuron=neuron,
            feature_index=feature_index
        )

    def get_influences_alongside_filter(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value,
        feature_index=None
    ):
        return Influences.get_influences_alongside_filter(
            self,
            artifacts_container,
            num_records,
            offset=0,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter,
            feature_index=feature_index
        )

    def get_influences_reduced(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        qoi_core_class=0,
        qoi="average",
        from_layer="internal",
        algorithm="tsne"
    ):

        if qoi == "average":
            get_influences_reduced = self.model.get_influences_reduced
        elif qoi == "last":
            get_influences_reduced = self.model.get_influences_reduced_last
        else:
            raise Exception("Precalculations for this qoi were not generated")
        influence_type_str = "outer" if from_layer == "internal" else "input"
        influences_reduced = get_influences_reduced(
            influence_type_str,
            artifacts_container,
            num_records,
            offset=offset,
            algorithm=algorithm
        )
        influences_reduced = influences_reduced[:, qoi_core_class, ...]
        if (len(influences_reduced.shape) < 2):
            raise Exception(
                "Precalculations for this qoi were not generated correctly"
            )
        return influences_reduced

    def get_global_influences(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        top_n=None,
        offset=0,
        sort: InfluenceAggregationMethod = InfluenceAggregationMethod.MEAN_ABS,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        from_layer="internal",
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        return Influences.global_influences(
            self,
            top_n,
            artifacts_container,
            num_records,
            offset=offset,
            sort=sort,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )

    def local_explanations_prediction_info(
        self,
        index,
        timestep_values,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        qoi_core_class=0,
        thresh=0.5,
        view_all_class_filter: bool = False
    ):
        if view_all_class_filter:
            qoi_core_class = None
        t_min, t_max = timestep_values
        return_df = pd.DataFrame()
        max_timesteps = self.get_total_timesteps(
            artifacts_container, input_timesteps=False
        )
        seq_length = self.get_lengths(
            artifacts_container,
            num_records,
            offset=offset,
            sample_index=index,
            input_lengths=False
        )
        return_df["predictions"] = self.get_predictions(
            artifacts_container,
            num_records,
            offset=offset,
            sample_index=index,
            class_index=qoi_core_class,
            convert_class_int=True
        )[:seq_length]
        return_df["timesteps"] = [
            "t-{}".format(seq_length - i - 1) for i in range(seq_length)
        ]
        filtered_timesteps = [
            "t-{}".format(max_timesteps - i - 1)
            for i in range(t_min, t_max + 1)
        ]
        return_df["labels"] = self.get_ground_truth(
            artifacts_container,
            num_records,
            offset=offset,
            sample_index=index,
            class_index=qoi_core_class,
            convert_class_int=True
        )[:seq_length]
        return_df["thresholds"] = thresh
        return_df = return_df[return_df["timesteps"].isin(filtered_timesteps)]
        return return_df

    def local_explanations_attribution_info(
        self,
        index,
        timestep_values,
        sort_mode,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        qoi_timestep=None,
    ):
        t_min, t_max = timestep_values
        return_df = pd.DataFrame()
        seq_length = self.get_lengths(
            artifacts_container, num_records, offset=offset, sample_index=index
        )

        # grab sample influences, data for timestep range
        influences, _, _, _, _ = self.get_influences_from_qoi(
            artifacts_container,
            num_records,
            offset=offset,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            neuron=None
        )
        influences = influences[index, :seq_length]

        # Sum the total record influence before partitioning via the timestep_values
        summed_influence = np.sum(influences)

        data = self.get_data(
            artifacts_container, num_records, offset=offset, sample_index=index
        )[:seq_length]
        return_df["feature_name"] = self.model.get_feature_names(
            artifacts_container
        )
        return_df["feature_desc"] = self.get_formatted_feature_descriptions(
            artifacts_container, return_df["feature_name"]
        )
        return_df["total_influence"] = np.sum(influences, axis=0)
        influences = influences[t_min:t_max + 1]
        data = data[t_min:t_max + 1]
        timesteps = [
            "t-{}".format(seq_length - i - 1) for i in range(seq_length)
        ][t_min:t_max + 1]

        # sort indices with desired mode
        return_df = LocalExpSortMode.get_sort_order(
            sort_mode, return_df, "total_influence"
        )
        return return_df, influences, data, timesteps, summed_influence

    def input_inf_2d_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        features,
        offset=0,
        index=None,
        thresh=None,
        thresh_le=False,
        timestep=None,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        qoi_timestep=0,
        pred_thresh=0.5,
        grouping=None,
        filter_list=[]
    ):
        all_features = self.get_feature_names(artifacts_container)
        feature_names = np.array(all_features)[features]

        # aggregate point-level metadata
        point_metadata_df = pd.DataFrame()
        point_metadata_df["record_id"] = np.squeeze(
            self.get_record_ids(
                artifacts_container, num_records, offset=offset
            )
        )
        point_metadata_df["indices"] = np.arange(len(point_metadata_df))

        # pull influences, data, grouping
        input_influences, filter_criteria, lengths, data, grouping_labels, grouping_preds = Influences.get_influences_alongside_filter(
            self,
            artifacts_container,
            num_records,
            offset=offset,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            feature_index=features
        )

        if sum(filter_criteria) == 0:
            raise FilterError
        grouping, names = ii_utils.get_grouping(
            grouping, grouping_labels, grouping_preds, lengths,
            input_influences, data, feature_names
        )

        # flatten data into 2D dataframes
        dfs = ii_utils.input_influence_2d_dfs(
            features,
            feature_names,
            input_influences,
            self.get_data(
                artifacts_container,
                num_records,
                offset=offset,
                feature_index=features
            ),
            lengths,
            index=index,
            length_thresh=thresh,
            length_thresh_le=thresh_le,
            timestep=timestep,
            grouping=grouping,
            sample_filter=filter_criteria
        )

        # join record ID and point level metadata
        for feature in dfs:
            dfs[feature] = dfs[feature].merge(point_metadata_df, on="indices")

        return dfs, grouping, names

    def get_model_thresholds_pct(
        self, artifact_containers, pct, num_records, class_name, offset=0
    ):
        thresholds = []
        for artifact_container in artifact_containers:
            pred = self.get_predictions_last(
                artifact_container,
                num_records,
                offset=offset,
                class_index=class_name
            )
            thresh = get_threshold_from_pct(pct, pred)
            thresh = round(thresh, 2)  # round for input validation
            thresholds.append(thresh)
        return thresholds

    def ensemble_analysis_info(
        self,
        artifact_containers,
        model_names,
        model_weights,
        model_thresholds,
        ensemble_threshold,
        num_records,
        class_name,
        offset=0
    ):
        table_df = pd.DataFrame()
        table_df["Metrics"] = get_available_metric_names()
        # find ground truths and sequence lengths
        label = self.get_ground_truth_last(
            artifact_containers[0],
            num_records,
            offset=offset,
            class_index=class_name
        )
        ensembled_preds = np.zeros_like(label, dtype="float32")

        # calc stats for individual models
        for model_name, model_weight, model_thresh, artifact_container in zip(
            model_names, model_weights, model_thresholds, artifact_containers
        ):
            pred = self.get_predictions_last(
                artifact_container,
                num_records,
                offset=offset,
                class_index=class_name
            )
            ensembled_preds += model_weight * pred
            table_df[model_name] = get_stats(pred, label, model_thresh)

        # calc stats for ensembled model
        best_model_per_metric = table_df.max(axis=1)
        ensembled_preds /= sum(model_weights)
        table_df["ensembled"] = get_stats(
            ensembled_preds, label, ensemble_threshold
        )
        table_df["improvement"] = table_df["ensembled"] - best_model_per_metric
        table_df["improvement"] = table_df["improvement"].apply(
            lambda x: "( {} )".format("{:+.4f}".format(x))
        )
        return table_df

    def global_metric_info(
        self,
        artifacts_containers,
        selected_models,
        selected_splits,
        num_records,
        class_name,
        model_thresholds,
        offset=0
    ):
        stats = get_available_metric_names()
        num_models = len(selected_models)
        num_splits = len(selected_splits)
        num_stats = len(stats)

        num_timesteps = None
        for artifacts_model in artifacts_containers:
            for artifacts_split in artifacts_model:
                if artifacts_split is not None and num_timesteps is None:
                    num_timesteps = self.get_total_timesteps(artifacts_split)

        all_stats = np.zeros((num_models, num_splits, num_stats))
        length_stats = np.zeros(
            (num_models, num_splits, num_timesteps, num_stats + 1)
        )  # include stat for data volume
        for model_i, (model_name, artifacts_model) in enumerate(
            zip(selected_models, artifacts_containers)
        ):
            model_thresh = model_thresholds[model_name]
            for split_i, artifacts_split in enumerate(artifacts_model):
                if artifacts_split is None:
                    all_stats[model_i, split_i] = np.nan
                    length_stats[model_i, split_i] = np.nan
                if artifacts_split is not None:
                    pred = self.get_predictions_last(
                        artifacts_split,
                        num_records,
                        offset=offset,
                        class_index=class_name
                    )
                    label = self.get_ground_truth_last(
                        artifacts_split,
                        num_records,
                        offset=offset,
                        class_index=class_name
                    )
                    seq_lengths = self.get_lengths(
                        artifacts_split, num_records, offset=offset
                    )
                    for seq_val in range(num_timesteps):
                        mask = (seq_lengths - 1) == seq_val
                        if mask.sum() == 0:
                            length_stats[model_i, split_i,
                                         seq_val] = [0, 0, 0, 0, 0]
                        else:
                            length_stats[model_i, split_i, seq_val] = get_stats(
                                pred[mask],
                                label[mask],
                                model_thresh,
                                include_data_volume=True
                            )
                    all_stats[model_i,
                              split_i] = get_stats(pred, label, model_thresh)
        return all_stats, length_stats, stats, num_timesteps

    def class_distribution_info(
        self,
        artifacts_containers,
        selected_models,
        selected_splits,
        num_records,
        class_name,
        model_thresholds,
        offset=0
    ):
        max_num_classes = 1
        model_dict = {}
        for model_idx in range(len(artifacts_containers)):
            artifacts_model = artifacts_containers[model_idx]
            model_name = selected_models[model_idx]
            model_thresh = model_thresholds[model_name]

            split_dict = {}
            for split_idx in range(len(artifacts_model)):
                artifacts_split = artifacts_model[split_idx]
                if (artifacts_split is not None):
                    split_name = selected_splits[split_idx]
                    full_pred = self.get_predictions_last(
                        artifacts_split, num_records, offset=offset
                    )
                    full_label = self.get_ground_truth_last(
                        artifacts_split, num_records, offset=offset
                    )
                    num_classes = full_label.shape[-1]
                    max_num_classes = max(max_num_classes, num_classes)
                    class_dict = {}
                    for class_idx in range(num_classes):
                        label = full_label[..., class_idx]
                        pred = full_pred[..., class_idx]
                        class_breakdown = get_class_breakdowns(
                            pred, label, model_thresh
                        )
                        class_dict[class_idx] = [
                            class_breakdown, 1 - class_breakdown
                        ]
                    split_dict[split_name] = class_dict
            model_dict[model_name] = split_dict
        return model_dict, max_num_classes

    def feature_splines_export_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset: int = 0,
        length_thresh: Optional[int] = None,
        length_thresh_le: bool = False,
        qoi_core_class: int = 0,
        qoi_compare_class: int = 0,
        qoi: str = "last",
        qoi_timestep: int = 0,
        pred_thresh: float = 0.5,
        filter_list: Optional[Sequence[ComponentData]] = None,
        artifacts_container_compare: ArtifactsContainer = None,
        pred_thresh_compare: float = 0.5,
        swap_compare_filter=SwapComparisons.NONE.value,
        poly_order: int = 3
    ) -> np.ndarray:
        """
        Calculates and returns the feature splines of input attributions.
        Args:
            artifacts_container: ArtifactsContainer,
            num_records (int or None): The number of records to return. If none, will return all.
            offset (int): The offset to start the num_records.
            length_thresh (int or None): An optional filter on record timeseries length.
            length_thresh_le (bool): A flag for the length threshold filter being less than or greater than. Defaults to False.
            qoi_core_class (int): The main class to get influences from.
            qoi_compare_class (int): A comparitive class to subtract from the main qoi_core_class. This gets a difference of classes explanation.
            qoi (str): The type of qoi. Options are ["last", "average","timestep","first default (prediction), "first default (ground truth)"]. These reference the timestep outputs.
            qoi_timestep (int): If the qoi is "timestep", this helps specify the timestep output
            pred_thresh_compare(float or None): A threshold to use for filters on a compare artifact. Defaults to 0.5
            filter_list (list of dash filter components): Filters to apply to the data.
            artifacts_container_compare (ArtifactsContainer or None): An ArtifactsContainer object that helps locate metadata of a compare artifact. 
            pred_thresh_compare(float or None): A threshold to use for filters on a compare artifact. Defaults to 0.5
            swap_compare_filter (SwapComparisons value): SwapComparisons filter to determine confusion matrix swapping from original to the compare data.
            poly_order (int): The polynomial order for splines. Defaults to 3

        Returns:
            spline_coefficients (np.ndarray): An array of spline coefficients. The dimensions will be (feature_id x timestep x polynomial order). Splines can be loaded in python with:
                spline_f = np.poly1d(spline_coefficients[feature_idx][timestep]) 
                extracted_feature += spline_f(data[feature_idx][timestep])
        """
        all_features = self.get_feature_names(artifacts_container)
        influences, filter_criteria, lengths, data, _, _ = Influences.get_influences_alongside_filter(
            self,
            artifacts_container,
            num_records,
            offset=offset,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )

        all_poly = np.zeros((len(all_features), len(data[0]), poly_order + 1))
        if sum(filter_criteria) == 0:
            raise FilterError

        progress = progressbar.ProgressBar(maxval=len(all_features))
        progress.start()
        for f_idx, feature in enumerate(all_features):
            data_3d = ii_utils.data_3d(
                influences[:, :, [f_idx]],
                data[:, :, [f_idx]],
                lengths,
                feature,
                length_thresh=length_thresh,
                length_thresh_le=length_thresh_le,
                sample_filter=filter_criteria
            )
            fitted_data = np.array(
                ii_utils.fit_poly_only(
                    data_3d,
                    self.get_total_timesteps(artifacts_container),
                    poly_order=poly_order
                )
            )
            all_poly[f_idx] = fitted_data
            progress.update(progress.currval + 1)
        progress.finish()
        return all_poly

    def feature_timesteps_export_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        aggregation_method=InfluenceAggregationMethod.MEAN_ABS,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        from_layer="internal",
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):

        temporal_data = Influences.get_all_influences(
            self,
            artifacts_container,
            num_records,
            offset=offset,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        if temporal_data is None:
            raise FilterError

        # Get all but the last timestep
        backpadding = temporal_data.forward_pad_transform().get_ndarray()
        num_features = backpadding.shape[-1]
        importances = aggregation_method.apply_aggregation(backpadding, axis=0)
        features = self.get_feature_names(
            artifacts_container, internal=(from_layer == "internal")
        )
        num_timesteps = self.get_total_timesteps(artifacts_container)
        timesteps = ["t-{}".format(i - 1) for i in range(num_timesteps, 0, -1)]
        export_df = pd.DataFrame()
        export_df["Importance"] = importances.flatten()
        export_df["Feature"] = np.tile(features, num_timesteps)
        export_df["Timestep"] = np.repeat(timesteps, num_features)
        return export_df

    def local_influences_export_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        from_layer="input",
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value,
        max_batchsize=None
    ):
        artifact_app = MemUtilDeps.INTERNAL_ATTRS if from_layer == "internal" else MemUtilDeps.INPUT_ATTRS
        if num_records is None:
            num_records = self.get_total_records(
                artifacts_container, artifact_app
            )

        export_data = []
        if max_batchsize is None:  # option to provide a max batchsize for testing pagination
            max_batchsize, _ = self.model.get_max_batchsize(
                artifacts_container, artifact_app
            )
        num_batches = math.ceil(num_records / max_batchsize)
        num_completed_records = 0
        for batch_i in range(num_batches):
            batchsize = min(num_records - num_completed_records, max_batchsize)
            temporal_data = Influences.get_all_influences(
                self,
                artifacts_container,
                batchsize,
                offset=num_completed_records,
                qoi_core_class=qoi_core_class,
                qoi_compare_class=qoi_compare_class,
                qoi=qoi,
                from_layer=from_layer,
                qoi_timestep=qoi_timestep,
                pred_thresh=pred_thresh,
                filter_list=filter_list,
                artifacts_container_compare=artifacts_container_compare,
                pred_thresh_compare=pred_thresh_compare,
                swap_compare_filter=swap_compare_filter
            )
            if temporal_data is None:
                raise FilterError
            export_data.append(temporal_data.get_ndarray())
            num_completed_records += batchsize

        return export_data

    def global_influence_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        top_n=None,
        sort: InfluenceAggregationMethod = InfluenceAggregationMethod.MEAN_ABS,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        from_layer="internal",
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value,
        aggregate_only=False,
        return_agg_seq=False
    ):
        seq, sorted_index, agg_seq = Influences.global_influences(
            self, top_n, artifacts_container, num_records, offset, sort,
            qoi_core_class, qoi_compare_class, qoi, from_layer, qoi_timestep,
            pred_thresh, filter_list, artifacts_container_compare,
            pred_thresh_compare, swap_compare_filter
        )
        if seq is None:
            raise FilterError
        if aggregate_only:
            feature_names = self.get_feature_names(
                artifacts_container, internal=(from_layer == "internal")
            )
            export_df = pd.DataFrame()
            export_df["feature_name"] = feature_names
            export_df["importance"] = agg_seq
            return export_df
        else:
            sorted_index = sorted_index[::-1]
            seq = seq[sorted_index, :]
            df = pd.DataFrame(
                data=seq,
                index=sorted_index,
                columns=["col{}".format(i) for i in range(seq.shape[1])]
            )
            if return_agg_seq:
                return df, agg_seq
            return df

    def global_timestep_influence_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        from_layer="internal",
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        feature=None,
        neuron=None
    ):

        temporal_data = Influences.get_all_influences(
            self,
            artifacts_container,
            num_records,
            offset=offset,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list
        )
        if temporal_data is None:
            raise FilterError
        influences = temporal_data.backward_pad_transform().get_ndarray()
        lengths = temporal_data.get_lengths()
        if from_layer == "input":
            feature_names = self.get_feature_names(artifacts_container)
            feature_idx = feature_names.index(feature.lower())
        elif from_layer == "internal":
            feature_idx = neuron

        seq = influences.T[feature_idx, :]
        return seq, lengths

    def internal_neuron_heatmap_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        infl_aggr="var",
        qoi="last",
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi_timestep=0,
        pred_thresh=0.5
    ):
        # get internal influences for each neuron/timestep
        influences, sample_filter, lengths, labels, preds = Influences.get_influences_from_qoi(
            self,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            artifacts_container,
            num_records,
            pred_thresh=pred_thresh,
            offset=offset,
            from_layer="internal",
            qoi_timestep=qoi_timestep
        )

        # compute feature importance with specified aggregation
        if isinstance(infl_aggr, int):
            neuron_importance = np.linalg.norm(
                influences, axis=0, ord=infl_aggr
            )

        elif isinstance(infl_aggr, str):
            neuron_importance = getattr(np, infl_aggr)(influences, axis=0)
        else:
            raise TypeError("`infl_aggr` not supported")

        # normalize for heatmap
        neuron_importance /= np.max(neuron_importance)
        return neuron_importance

    def internal_neuron_heatmap_export_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        infl_aggr="var",
        qoi="last",
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi_timestep=0,
        pred_thresh=0.5
    ):
        neuron_importance = self.internal_neuron_heatmap_info(
            artifacts_container,
            num_records,
            offset=offset,
            infl_aggr=infl_aggr,
            qoi=qoi,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh
        )
        export_df = pd.DataFrame(
            data=neuron_importance,
            index=["t-{}".format(i) for i in range(neuron_importance.shape[0])],
            columns=self.get_feature_names(artifacts_container, internal=True),
        )
        return export_df

    def feature_interaction_dendrogram_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset: int = 0,
        qoi_class: int = 0,
        path_max_filter=0,
        filter_top_n: int = -1
    ):
        """
        Takes records in the given artifact container from index offset to offset + num_records.
        Build a spectral coclustering-based binary tree of each record, and return a dataframe that contains
        (1) tree structure (parent, ancestors of each node)
        (2) link to original features (indexes in the original data)
        """
        corrs, corr_idx_mapping, feature_timestep_column_names = self.model.get_correlation_matrices(
            artifacts_container,
            num_records,
            offset=offset,
            qoi_class=qoi_class,
            path_max_filter=path_max_filter,
            filter_top_n=filter_top_n
        )
        return SpectralHierarchicalClusterer.interaction_dendrogram_info(
            corrs,
            corr_idx_mapping,
            feature_timestep_column_names,
            num_records=num_records,
            offset=offset
        )

    def gradient_landscape_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset: int = 0,
        qoi_class: int = 0,
    ) -> Sequence[pd.DataFrame]:
        """
        Returns the gradient landscape for each record, building a dataframe where
        - each column corresponds to a feature,timestep index
        - each row corresponds to a specific step number
        in the gradient attribution interpolation
        """
        # shape: (num_records, resolution, num_timesteps_in, num_postprocessed_features)
        grad_path_influences, grad_path_influences_column_names = self.model.get_grad_path_influences(
            artifacts_container,
            num_records=num_records,
            offset=offset,
            qoi_class=qoi_class
        )

        return_dfs = {}
        for idx, grad_path, column_names in zip(
            range(offset, offset + num_records), grad_path_influences,
            grad_path_influences_column_names
        ):
            return_dfs[idx] = pd.DataFrame(
                data=np.abs(grad_path.T), columns=column_names
            ), column_names
        return return_dfs

    def pairwise_interactions_info(
        self,
        pairwise_feature1: str,
        pairwise_feature2: str,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        timestep_feature1: str = "all",
        timestep_feature2: str = "all",
        qoi_core_class: int = 0,
        qoi_compare_class: int = 0,
        qoi: str = "average",
        qoi_timestep: int = 0,
        pred_thresh: float = 0.5,
        grouping_str: Optional[str] = None,
    ):
        all_features = self.get_feature_names(artifacts_container)
        features = [pairwise_feature1.lower(), pairwise_feature2.lower()]
        feature_idx = [
            all_features.index(pairwise_feature1.lower()),
            all_features.index(pairwise_feature2.lower())
        ]
        input_influences, sample_filter, lengths, grouping_labels, grouping_preds = self.get_influences_from_qoi(
            artifacts_container,
            num_records,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            feature_index=feature_idx
        )
        data = self.get_data(
            artifacts_container, num_records, feature_index=feature_idx
        )
        grouping, names = ii_utils.get_grouping(
            grouping_str, grouping_labels, grouping_preds, lengths,
            input_influences, data, features
        )
        point_data = ii_utils.pairwise_influences_3d(
            input_influences,
            data,
            lengths,
            pairwise_feature1,
            timestep_feature1=timestep_feature1,
            timestep_feature2=timestep_feature2,
            grouping=grouping
        )
        return point_data, names

    def _aggregate_from_aggr_type(self, x, aggr_type, normalize=False):
        if isinstance(aggr_type, int):
            feature_importance = np.linalg.norm(x, axis=0, ord=aggr_type)
        elif isinstance(aggr_type, str):
            feature_importance = getattr(np, aggr_type)(x, axis=0)
        else:
            raise TypeError(
                "Aggrregation type of {} not supported".format(aggr_type)
            )
        if normalize:
            feature_importance /= np.max(feature_importance)
        return feature_importance

    def feature_correlation_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        feature_space=FeatureSpace.INPUT,
        correlate_along=InteractAlong.FEATURE_DIM,
        temporal_aggr=AggregationMethod.L1,
        interaction_type=InteractionType.CORRELATION,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        qoi_timestep=0,
        pred_thresh=0.5
    ):
        feature_names = self.get_feature_names(artifacts_container)
        num_timesteps = self.get_total_timesteps(artifacts_container)
        if correlate_along == InteractAlong.ALL.value:
            feature_names = [
                "{} T-{}".format(name, ts)
                for ts in range(num_timesteps)
                for name in feature_names
            ]
        data = self.get_data(artifacts_container, num_records)
        lengths = self.get_lengths(artifacts_container, num_records)
        features = data if feature_space == FeatureSpace.INPUT.value else self.get_influences_from_qoi(
            artifacts_container,
            num_records,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            pred_thresh=pred_thresh,
            qoi_timestep=qoi_timestep
        )[0]

        temporal_data = TemporalData(features, lengths,
                                     False).forward_pad_transform()
        features = temporal_data.get_ndarray()[:, ::-1, ...]
        feature_importance = self._aggregate_from_aggr_type(
            temporal_data.mean_over_timestep(), temporal_aggr, normalize=True
        )

        MathOverflow = False
        if interaction_type == InteractionType.CORRELATION.value:
            corr, feature_names = ii_utils.linear_correlation(
                features, correlate_along
            )
        elif interaction_type == InteractionType.PARTIAL_CORRELATION.value:
            try:
                corr, feature_names, not_PSD = ii_utils.partial_correlation(
                    features, correlate_along
                )
            except:
                corr, feature_names = ii_utils.linear_correlation(
                    features, correlate_along
                )
                MathOverflow = True
        elif interaction_type == InteractionType.AUTO_CORRELATION.value:
            corr = ii_utils.auto_correlation(features)
        else:
            raise ValueError("Not a supported type.")

        corr = np.nan_to_num(corr)
        return corr, feature_names, features, feature_importance

    def internal_unit_influence_info(
        self,
        index,
        artifacts_container: ArtifactsContainer,
        num_records,
        neuron=None,
        sort=0,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        qoi_timestep=None,
        top_n_features=20,
        feature=None
    ):
        influences, _, _, _, _ = self.get_influences_from_qoi(
            artifacts_container,
            num_records,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            qoi_timestep=qoi_timestep,
            neuron=neuron
        )
        seq = influences[index]
        if neuron is not None:
            seq = seq[:, :, neuron]
        preds_all = self.get_predictions(artifacts_container, num_records)
        preds = preds_all[index, ..., qoi_core_class:qoi_core_class + 1]
        preds_high = np.max(preds_all)
        preds_low = np.min(preds_all)
        preds_df = pd.DataFrame(data=preds.T, index=["model output"])

        feature_names = self.get_feature_names(artifacts_container)

        inf_data = seq.T
        infs_df = pd.DataFrame(
            data=inf_data, index=list(range(len(feature_names)))
        )

        # Add a summed column to sort by (TODO: have customizable summing)
        max_timesteps = len(infs_df.columns)

        display_df = pd.concat(
            [infs_df, infs_df.sum(axis=1)], axis=1, sort=False
        )
        display_df.columns = pd.RangeIndex(max_timesteps + 1)
        summed_column = len(display_df.columns) - 1
        if sort < 2:
            display_df = display_df.sort_values(
                by=[summed_column], ascending=sort
            )

            # Filter by the top features, and reverse indexing so visualization shows highest values at the top
            display_df = display_df.iloc[:top_n_features]
            display_df = display_df.reindex(index=display_df.index[::-1])
        else:
            # TODO: allow a list of custom features instead of a single one?
            display_df = display_df.iloc[[feature_names.index(feature.lower())]]
        return preds_df, preds_high, preds_low, infs_df, display_df, summed_column

    def input_inf_3d_info(
        self,
        feature,
        artifacts_container: ArtifactsContainer,
        num_records,
        index=None,
        length_thresh=None,
        length_thresh_le=False,
        num_timesteps=None,
        timestep_forward=False,
        filter_mode=None,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi="average",
        qoi_timestep=0,
        pred_thresh=0.5,
        grouping=None,
        filter_list=[],
        artifacts_container_compare: ArtifactsContainer = None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        all_features = self.get_feature_names(artifacts_container)
        feature_index = [all_features.index(feature.lower())]
        influences, filter_criteria, lengths, data, grouping_labels, grouping_preds = self.get_influences_alongside_filter(
            artifacts_container,
            num_records,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter,
            feature_index=feature_index
        )
        if sum(filter_criteria) == 0:
            raise FilterError
        grouping, names = ii_utils.get_grouping(
            grouping, grouping_labels, grouping_preds, lengths, influences,
            data, [feature]
        )
        data = ii_utils.data_3d(
            influences,
            self.get_data(
                artifacts_container, num_records, feature_index=feature_index
            ),
            lengths,
            feature,
            index=index,
            length_thresh=length_thresh,
            length_thresh_le=length_thresh_le,
            num_timesteps=num_timesteps,
            grouping=grouping,
            sample_filter=filter_criteria
        )
        point_data = ii_utils.convert_data_3d_to_points(data)
        fitted_data = np.array(ii_utils.fit_data(data))
        return point_data, fitted_data, names
