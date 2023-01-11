import os.path
from simAIRR.util.utilities import concatenate_files, makedir_if_not_exists, split_dataframe


class UniqueSequenceFilter:

    def __init__(self, baseline_repertoires_path: str, public_sequence_proportion: float, seed: int):
        self.baseline_repertoires_path = baseline_repertoires_path
        self.public_sequence_proportion = public_sequence_proportion
        self.seed = seed

    def filter_unique_sequences(self):
        concatenated_df, num_files = concatenate_files(self.baseline_repertoires_path, 'rep_*.tsv')
        concatenated_df = concatenated_df.drop_duplicates()
        return concatenated_df, num_files

    def write_unique_public_and_private_repertoire_components(self):
        concatenated_df, num_files = self.filter_unique_sequences()
        public_df = concatenated_df.sample(frac=self.public_sequence_proportion, random_state=self.seed)
        private_df = concatenated_df.drop(public_df.index)
        filtered_public_repertoires_path = os.path.join(self.baseline_repertoires_path, "filtered_public_repertoires")
        makedir_if_not_exists(filtered_public_repertoires_path, fail_if_exists=True)
        filtered_private_repertoires_path = os.path.join(self.baseline_repertoires_path, "filtered_private_repertoires")
        makedir_if_not_exists(filtered_private_repertoires_path, fail_if_exists=True)
        split_dataframe(public_df, num_files, filtered_public_repertoires_path)
        split_dataframe(private_df, num_files, filtered_private_repertoires_path)

