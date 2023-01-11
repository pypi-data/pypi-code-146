import numpy as np


class SequencePresenceMatrix:
    def __init__(self, number_of_repertoires, presence_counts_list):
        self.number_of_repertoires = number_of_repertoires
        self.null_matrix = np.zeros((len(presence_counts_list), self.number_of_repertoires), dtype=int)
        self.presence_counts_list = presence_counts_list

    def _get_random_presence_indices(self, presence_count):
        try:
            assert presence_count <= self.number_of_repertoires, "Unusual sequence presence count > desired number of repertoires returned"
            return np.random.choice(self.number_of_repertoires, presence_count, replace=False)
        except ValueError as e:
            print(e)

    def _update_seq_presence_matrix(self, presence_count, row_index):
        col_indices = self._get_random_presence_indices(presence_count)
        self.null_matrix[row_index, col_indices] = 1

    def _map_update_seq_presence_matrix(self):
        for i, presence_count in enumerate(self.presence_counts_list):
            self._update_seq_presence_matrix(presence_count=presence_count, row_index=i)

    def get_repertoire_sequence_presence_indices(self):
        self._map_update_seq_presence_matrix()
        nonzero_seq_indices = [np.where(self.null_matrix[:, i] > 0) for i in range(self.number_of_repertoires)]
        return [item for sublist in nonzero_seq_indices for item in sublist]
