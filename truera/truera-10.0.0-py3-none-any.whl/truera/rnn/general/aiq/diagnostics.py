from enum import Enum
from typing import Sequence

import numpy as np
import pandas as pd

from truera.rnn.general.aiq.aiq import RnnAIQ
from truera.rnn.general.container import ArtifactsContainer
from truera.rnn.general.selection.interaction_selection import \
    GroupProfilerDiagnosticType
from truera.rnn.general.selection.interaction_selection import \
    InfluenceAggregationMethod
from truera.rnn.general.selection.interaction_selection import ModelGrouping
from truera.rnn.general.selection.swap_selection import SwapComparisons
from truera.rnn.general.utils.errors import viz_callback

from . import influences as Influences
from . import input_inf_utils as ii_utils
from .processor import OverfittingProcessor
from .processor import SplineProcessor


class DiagnosticsGenerator:

    def __init__(self, aiq: RnnAIQ):
        self.aiq = aiq

    @viz_callback
    def get_feature_importance(
        self,
        artifact_containers: Sequence[ArtifactsContainer],
        class_labels: Sequence[int],
        num_records,
        aggregation_type=InfluenceAggregationMethod.MEAN_ABS
    ):
        data_dfs = []
        feature_names = self.aiq.get_feature_names(artifact_containers[0])
        for model_class in class_labels:
            for artifacts_container in artifact_containers:
                split_name = artifacts_container.locator.split
                input_influences, _, lengths, _, _ = self.aiq.get_influences_from_qoi(
                    artifacts_container, num_records, model_class, None,
                    'average'
                )
                feature_array = np.hstack(
                    [
                        input_influences[i, 0:length, ...].T
                        for i, length in enumerate(lengths)
                    ]
                )  # make feature the first dimension
                agg_influences = aggregation_type.apply_aggregation(
                    feature_array, axis=1
                )
                data_df = pd.DataFrame(
                    {
                        'Feature': feature_names,
                        'Value': agg_influences
                    }
                )
                data_df['Class'] = model_class
                data_df['Split'] = split_name
                data_dfs.append(data_df)
        return pd.concat(data_dfs)

    def detect_overfitting(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0
    ):
        all_features = self.aiq.get_feature_names(artifacts_container)
        input_influences, _, lengths, grouping_labels, grouping_preds = self.aiq.get_influences_from_qoi(
            artifacts_container,
            num_records,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            qoi_timestep=qoi_timestep
        )
        data = self.aiq.get_data(artifacts_container, num_records)
        bucket_metadata, importance_metadata = OverfittingProcessor.rnn_overfit_metadata(
            input_influences, data, lengths, all_features,
            input_influences.shape[1]
        )
        overfitting_df = pd.DataFrame()
        overfitting_df['Feature'] = list(bucket_metadata.keys())
        overfitting_df['Overfitting Score'] = overfitting_df['Feature'].map(
            importance_metadata
        )
        overfitting_df['Overfitting Ranges'] = overfitting_df['Feature'].map(
            bucket_metadata
        )
        return overfitting_df

    @viz_callback
    def var_from_spline_diagnostic(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        offset=0,
        length_thresh=None,
        length_thresh_le=False,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='last',
        qoi_timestep=0,
        pred_thresh=0.5,
        grouping_str=None,
        filter_list=[],
        artifacts_container_compare: ArtifactsContainer = None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value,
        poly_order=3
    ):
        all_features = self.aiq.get_feature_names(artifacts_container)
        influences, filter_criteria, lengths, data, _, _ = Influences.get_influences_alongside_filter(
            self.aiq,
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
        if sum(filter_criteria) == 0:
            raise FilterError
        return SplineProcessor.var_from_spline_calculation(
            all_features,
            self.aiq.get_total_timesteps(artifacts_container),
            influences,
            data,
            lengths,
            length_thresh=length_thresh,
            length_thresh_le=length_thresh_le,
            filter_criteria=filter_criteria,
            poly_order=poly_order
        )

    def high_global_influence_concentration_diagnostic(
        self, record_ids, feature_values: np.ndarray, influences: np.ndarray,
        group_mask: np.ndarray, influence_concentration_pct: int,
        feature_cutoff: int, feature_names: Sequence[str],
        global_importance_info: pd.DataFrame
    ):
        """
        Goal: Define if the model is focusing on too few features
        Definition: Show records where the sum of the normalized influence of the global top X features account
        for over Y% of all of the record's feature normalized influence
        """
        influences_normalized, cutoff_features_indices = self._get_normalized_features_and_cutoff_features(
            influences, global_importance_info, feature_cutoff
        )
        influence_normalized_denom = np.abs(influences_normalized).sum(
            axis=(1, 2)
        )  # sum across timesteps and features to get total per record
        influence_normalized_numerator = np.abs(
            influences_normalized
        )[:, :, cutoff_features_indices].sum(
            axis=(1, 2)
        )  # sum across timesteps and top global features to get total per record

        influence_concentration = influence_normalized_numerator / influence_normalized_denom  # find influence concentration per record
        accepted_records = np.logical_and(
            np.around(100 * influence_concentration) >=
            influence_concentration_pct, group_mask
        )  # filter to records of the given group with high enough influence concentration
        data = {
            'diagnostic': 'high_global_influence_concentration',
            'records': {}
        }
        for record_idx, record_id, feature_value, influence in zip(
            np.asarray(range(len(accepted_records)))[accepted_records],
            record_ids[accepted_records], feature_values[accepted_records],
            influences_normalized[accepted_records]
        ):
            record_data = {
                'top_features': [],
                'total_influence': np.sum(influence),
                'record_idx': record_idx,
            }
            sum_top_features = influence[:, cutoff_features_indices].sum(axis=0)
            for i, feature_ix in enumerate(cutoff_features_indices):
                record_data['top_features'].append(
                    {
                        'feature': feature_names[feature_ix],
                        'normalized_influences': sum_top_features[i]
                    }
                )
            data['records'][str(record_id)] = record_data
        return data

    def _get_normalized_features_and_cutoff_features(
        self, influences: np.ndarray, global_importance_info: pd.DataFrame,
        feature_cutoff: int
    ):
        influences_normalized = influences - np.median(influences, axis=(0, 1))
        global_importance_info = global_importance_info.sort_values(
            by='importance', ascending=False
        )
        cutoff_features_indices = global_importance_info.index[
            range(feature_cutoff)]
        return influences_normalized, cutoff_features_indices

    def no_strong_influence_diagnostic(
        self,
        record_ids,
        feature_values: np.ndarray,
        influences: np.ndarray,
        lengths: np.ndarray,
        group_mask: np.ndarray,
        influence_concentration_pct: int,
        feature_cutoff: int,
        feature_names: Sequence[str],
        global_importance_info: pd.DataFrame,
        num_feature_to_beat: int = 1
    ):
        """
        Goal: Find records that the model has little opinion on.
        Definition: Show records in which 1 or fewer features has a high importance, 
        where high importance is denoted by the X%tile of the Yth most globally important feature's importance.
        """
        total_features = influences.shape[2]
        influences_normalized, cutoff_features_indices = self._get_normalized_features_and_cutoff_features(
            influences, global_importance_info, feature_cutoff
        )
        feature_cutoff_index = cutoff_features_indices[-1]
        influence_cutoff = np.percentile(
            np.abs(influences_normalized[..., feature_cutoff_index]),
            influence_concentration_pct
        )
        accepted_records = np.logical_and(
            group_mask,
            np.max(
                (np.abs(influences_normalized) >= np.abs(influence_cutoff)),
                axis=1
            ).sum(axis=1) <= 1
        )  # filter to records of the given group with at most one feature above the influence cutoff
        data = {
            'diagnostic':
                'no_strong_influence_diagnostic',
            'records': {},
            'global_important_features':
                list(
                    global_importance_info['feature_name'].
                    values[:feature_cutoff]
                )
        }
        low_inf = np.max(
            (np.abs(influences_normalized) >= np.abs(influence_cutoff)), axis=1
        ).sum(axis=1) <= num_feature_to_beat

        for record_idx, record_id, feature_value, influence, length in zip(
            np.asarray(range(len(accepted_records)))[accepted_records],
            record_ids[accepted_records], feature_values[accepted_records],
            influences_normalized[accepted_records], lengths[accepted_records]
        ):
            record_data = {
                'top_features': [],
                'total_influence': np.sum(influence),
                'record_idx': record_idx,
                'strong_influence_threshold': round(influence_cutoff, 4)
            }

            top_timesteps_in_features = np.argmax(np.abs(influence), axis=0)

            top_feature_infs = np.max(np.abs(influence), axis=0)
            top_features = np.argsort(top_feature_infs)[
                -min(total_features, num_feature_to_beat + 1):]
            for feature_ix in top_features:
                timestep_ix = top_timesteps_in_features[feature_ix]
                record_data['top_features'].append(
                    {
                        'feature':
                            feature_names[feature_ix],
                        'timestep':
                            f't-{length - timestep_ix - 1}',
                        'feature_value':
                            feature_value[timestep_ix, feature_ix],
                        'normalized_influences':
                            influence[timestep_ix, feature_ix]
                    }
                )

            data['records'][str(record_id)] = record_data
        return data

    def group_profiler_data(
        self,
        artifacts_container: ArtifactsContainer,
        group_profiler_diagnostic_type,
        grouping_str,
        feature_cutoff,
        influence_concentration_pct,
        num_records,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='last',
        qoi_timestep=0,
        pred_thresh=0.5
    ):
        all_features = self.aiq.get_feature_names(artifacts_container)
        input_influences, _, lengths, grouping_labels, grouping_preds = self.aiq.get_influences_from_qoi(
            artifacts_container,
            num_records,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh
        )
        data = self.aiq.get_data(artifacts_container, num_records)
        record_ids = self.aiq.get_record_ids(artifacts_container, num_records)
        if grouping_str is None or grouping_str == "none" or grouping_str == "all":
            grouping_str = "all"
            group_type = ModelGrouping.NONE
        else:
            group_type = ModelGrouping.CONFUSION_MATRIX
        grouping, names = ii_utils.get_grouping(
            group_type, grouping_labels, grouping_preds, lengths,
            input_influences, data, all_features
        )
        group = names.index(grouping_str)
        group_mask = (grouping == group)
        global_importances = self.aiq.global_influence_info(
            artifacts_container,
            num_records,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            sort=InfluenceAggregationMethod.MEAN_ABS,
            from_layer='input',
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            aggregate_only=True
        )
        if group_profiler_diagnostic_type == GroupProfilerDiagnosticType.INFLUENCE_CONCENTRATION:
            return self.high_global_influence_concentration_diagnostic(
                record_ids, data, input_influences, group_mask,
                influence_concentration_pct, feature_cutoff, all_features,
                global_importances
            )
        if group_profiler_diagnostic_type == GroupProfilerDiagnosticType.NO_STRONG_INFLUENCE:

            return self.no_strong_influence_diagnostic(
                record_ids, data, input_influences, lengths, group_mask,
                influence_concentration_pct, feature_cutoff, all_features,
                global_importances
            )
        raise NotImplementedError(
            f"Group profiler diagnostic {group_profiler_diagnostic_type} is not supported."
        )
