from csv import Dialect
import os
from pathlib import Path
import types

import numpy as np
from scipy import stats
from tqdm import tqdm

from truera.client.nn.client_configs import Dimension
from truera.client.nn.wrappers.timeseries import Wrappers as Timeseries
from truera.rnn.general.model_runner_proxy.dimension_utils import \
    reverse_transpose_back_to_original_dimensions
from truera.rnn.general.model_runner_proxy.dimension_utils import \
    transpose_to_standard_dimensions
from truera.rnn.general.model_runner_proxy.explain_helpers import \
    baseline_minimizer
from truera.rnn.general.utils import log
from truera.utils.file_utils import as_path


class BaselineConstructor():

    def __init__(
        self, baseline_ds, baseline_split_path, model, data_wrapper,
        model_wrapper, model_args, batch_size
    ):
        self.baseline_split_path: Path = as_path(baseline_split_path, warn=True)
        self.baseline_ds = baseline_ds
        self.model = model
        self.n_time_step_input = model_args.n_time_step_input
        self.batch_size = batch_size
        self.data_wrapper = data_wrapper
        self.model_wrapper = model_wrapper
        self.input_dimension_order = model_args.input_dimension_order
        self.standard_input_dimension_order = (
            Dimension.BATCH, Dimension.TIMESTEP, Dimension.FEATURE
        )

    def create_batched_baseline(self, timestep_input, batches):
        '''
        batches together inputs. At this point; the dimensions expected are (batch x timestep x feature)
        '''
        return (
            np.tile(timestep_input, (batches, self.n_time_step_input, 1)),
            np.asarray([self.n_time_step_input] * batches)
        )

    def get_special_baseline_values(self):
        '''
        The special values baseline defines special values per feature in which the influence should be 0.
        If a special value is the baseline, it will have 0 influence.

        Note: This method will transpose the input feature dimensions to (batch x timestep x feature)

        Special value classes currently supported:
        - Missing values given by the user.
        - Categorical variables where the data is significantly skewed towards a single mode.
          It is undesirable to have most common categorical variable with high variance so we choose it
          to be the baseline to lower variance by having 0 influence
        '''
        # keep randomness consistent between runs
        np.random.seed(0)

        special_baseline_indices = []

        if isinstance(self.data_wrapper.get_missing_values, types.FunctionType):
            features_missing = self.data_wrapper.get_missing_values(
                self.baseline_split_path
            )
            feature_names = self.data_wrapper.get_feature_names(
                self.baseline_split_path
            )
        else:
            features_missing = self.data_wrapper.get_missing_values()
            feature_names = self.data_wrapper.get_feature_names()

        if isinstance(
            self.model_wrapper, Timeseries.ModelRunWrapper.WithOneHot
        ):
            encoded_features = self.model_wrapper.get_one_hot_sizes()
        else:
            encoded_features = dict()

        # if features_missing is a list or set, then it means that feature contains missing values, but we might not know what the specific value is
        # we will naively find the modes and set the mode value as the missing value.
        special_baseline_indices = []
        encoded_indices = []
        curr_index = 0
        non_encoded_feature_indices = {}
        for f in feature_names:
            if f in encoded_features:
                encoded_indices.extend(
                    list(range(curr_index, curr_index + encoded_features[f]))
                )
                curr_index = curr_index + encoded_features[f]
            else:
                # A list implies we know the feature has missing values, but we don't know what it is beforehand
                if isinstance(features_missing, list) and f in features_missing:
                    special_baseline_indices.append(curr_index)
                non_encoded_feature_indices[f] = curr_index
                curr_index += 1

        special_baseline_indices = set(special_baseline_indices)
        special_value_samples = []

        for batch, ds_batch in enumerate(tqdm(self.baseline_ds)):
            tru_batch: Timeseries.Types.TruBatch = self.model_wrapper.trubatch_of_databatch(
                ds_batch, self.model
            )

            # Transpose so that ordering is (batch x timestep x feature)
            np_num_sequences = transpose_to_standard_dimensions(
                tru_batch.features,
                self.standard_input_dimension_order,
                data_dimension_order=self.input_dimension_order
            )
            batch_len = len(np_num_sequences)

            # Take one random timestep so as not to dilute/confuse with non changing values
            rand_index = (
                np.random.uniform(low=0.0, high=1.0, size=batch_len) *
                tru_batch.lengths
            ).astype(int)
            random_step = np_num_sequences[range(batch_len), rand_index]
            special_value_samples.append(random_step)

        repeated_random_timestep_samples = np.vstack(special_value_samples).T
        baseline_record = np.average(repeated_random_timestep_samples, axis=1)
        # Set encoded indices baseline to 0
        baseline_record[encoded_indices] = 0.0

        # find the mode value of each feature
        modes_val = {}
        for index in range(len(repeated_random_timestep_samples)):
            if index not in encoded_indices:
                (vals, counts) = np.unique(
                    repeated_random_timestep_samples[index], return_counts=True
                )

                tops = np.argsort(counts)[::-1]
                modes_val[index] = vals[tops[0]]
                if len(counts) > 1:
                    # Simple heuristic, if the first mode is 50% more than the 2nd mode, then classify it as a special value
                    simple_heuristic_first_to_second_ratio = 1.5
                    if (
                        counts[tops[0]] / counts[tops[1]] >
                        simple_heuristic_first_to_second_ratio
                    ):
                        special_baseline_indices.add(index)
        # Set the modes val to the missing val if it was specified in the features_missing_dict
        if (isinstance(features_missing, dict)):
            for f in features_missing:
                modes_val[non_encoded_feature_indices[f]] = features_missing[f]

        return baseline_record, special_baseline_indices, modes_val

    def construct_avg_baseline(self):
        '''
        Merge average baseline with special values baseline.
        See construct_simple_avg_baseline.
        See get_special_baseline
        '''
        #if (os.path.exists(self.baseline_split_path + "avg_baseline.npy")):
        #    return np.load(self.baseline_split_path + "avg_baseline.npy")

        baseline_record, special_baseline_indices, modes_val = \
            self.get_special_baseline_values()

        for special_baseline_index in special_baseline_indices:
            special_baseline_val = modes_val[special_baseline_index]
            baseline_record[special_baseline_index] = special_baseline_val

        baseline, baseline_lengths = self.create_batched_baseline(
            baseline_record, self.batch_size
        )

        os.makedirs(self.baseline_split_path, exist_ok=True)
        np.save(self.baseline_split_path / "avg_baseline.npy", baseline)
        log.info('average baseline constructed')

        # reverse transpose order back to original input dimensions, as it will need to be used in trulens in the original input dimensions
        baseline = reverse_transpose_back_to_original_dimensions(
            baseline,
            self.standard_input_dimension_order,
            data_dimension_order=self.input_dimension_order
        )

        return baseline