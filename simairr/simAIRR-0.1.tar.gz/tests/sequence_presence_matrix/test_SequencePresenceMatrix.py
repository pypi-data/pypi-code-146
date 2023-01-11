import numpy as np
from simAIRR.sequence_presence_matrix.SequencePresenceMatrix import SequencePresenceMatrix


def test_get_repertoire_sequence_presence_indices():
    count_list = [2, 1, 1, 4, 2, 6, 1, 3, 9]
    test_mat = SequencePresenceMatrix(number_of_repertoires=10, presence_counts_list=count_list)
    rep_presence_list = test_mat.get_repertoire_sequence_presence_indices()
    assert len(rep_presence_list) == 10, f"Number of sequence presence arrays does not match " \
                                         f"the desired number of repertoires"
    assert len(np.concatenate(rep_presence_list)) == sum(count_list), f"Sum of presence count list does not match " \
                                                                      f"the length of implantable indices list"
