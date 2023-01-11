import pandas as pd
import numpy as np
from operator import attrgetter
import os
import re
from simAIRR.sequence_presence_matrix.SequencePresenceMatrix import SequencePresenceMatrix


class ImplantationHelper:

    @staticmethod
    def get_pgen_intervals(pgen_dat, pgen_count_map_obj):
        pgen_dat['pgen'] = pgen_dat['pgen'].replace([0], 1.0e-50)
        pgen_dat['pgen_bins'] = pd.cut(np.log10(pgen_dat['pgen']), bins=pgen_count_map_obj.get_pgen_breaks(),
                                       include_lowest=True)
        pgen_dat['pgen_left'] = pgen_dat['pgen_bins'].map(attrgetter('left'))
        pgen_dat['pgen_right'] = pgen_dat['pgen_bins'].map(attrgetter('right'))
        pgen_dat['pgen_interval'] = pgen_dat[['pgen_left', 'pgen_right']].apply(tuple, axis=1)
        pgen_intervals_list = pgen_dat['pgen_interval'].to_list()
        return [(int(x), int(y)) for x, y in pgen_intervals_list]

    @staticmethod
    def get_absolute_number_of_repertoires(pgen_intervals_list, pgen_count_map_obj):
        return [pgen_count_map_obj.get_absolute_number_of_repertoires(interval_bin) for interval_bin in
                pgen_intervals_list]

    @staticmethod
    def get_repertoire_sequence_presence_indices(desired_num_repertoires, abs_num_of_reps_list):
        return SequencePresenceMatrix(number_of_repertoires=desired_num_repertoires,
                                      presence_counts_list=abs_num_of_reps_list).get_repertoire_sequence_presence_indices()

    @staticmethod
    def write_public_repertoire_chunks(original_repertoire_file, output_files_path,
                                       repertoire_sequence_presence_indices, file_type="pickle"):
        original_file = pd.read_csv(original_repertoire_file, header=None, index_col=None, sep='\t')
        original_file_chunk_name = re.sub(r"\..*", "", os.path.basename(original_repertoire_file)).replace("rep", "chunk")
        chunk_path = os.path.join(output_files_path, original_file_chunk_name)
        if not os.path.exists(chunk_path):
            os.makedirs(chunk_path)
        if file_type == "pickle":
            for i, indices in enumerate(repertoire_sequence_presence_indices):
                original_file.loc[indices].to_pickle(os.path.join(chunk_path, f"rep_{i}.pkl"))
        else:
            for i, indices in enumerate(repertoire_sequence_presence_indices):
                original_file.loc[indices].to_csv(os.path.join(chunk_path, f"rep_{i}.tsv"), header=None, index=None, sep='\t')