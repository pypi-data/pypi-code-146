import glob
import os
import pandas as pd
from multiprocessing import Pool
from simAIRR.expand_repertoire_components.ImplantationHelper import ImplantationHelper


class PublicRepertoireGeneration:
    def __init__(self, public_repertoires_path, n_threads, pgen_count_map_obj, desired_num_repertoires):
        self.public_repertoires_path = public_repertoires_path
        self.pgen_files_path = os.path.join(self.public_repertoires_path, "pgen_files")
        self.tmp_chunks_path = os.path.join(self.public_repertoires_path, "tmp_chunks")
        self.corrected_public_repertoires_path = os.path.join(os.path.dirname(self.public_repertoires_path),
                                                              "corrected_public_repertoires")
        self.n_threads = n_threads
        self.pgen_count_map_obj = pgen_count_map_obj
        self.desired_num_repertoires = desired_num_repertoires
        if not os.path.exists(self.corrected_public_repertoires_path):
            os.makedirs(self.corrected_public_repertoires_path)

    def generate_public_repertoires(self, pgen_file):
        original_rep_file = os.path.join(self.public_repertoires_path, os.path.basename(pgen_file).replace('pgen_', ''))
        pgen_dat = pd.read_csv(pgen_file, header=None, index_col=None, sep='\t', names=['aa_seq', 'pgen'])
        pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                     pgen_count_map_obj=self.pgen_count_map_obj)
        abs_rep_num = ImplantationHelper.get_absolute_number_of_repertoires(pgen_intervals_list=pgen_intervals_array,
                                                                            pgen_count_map_obj=self.pgen_count_map_obj)
        seq_presence_indices = ImplantationHelper.get_repertoire_sequence_presence_indices(
            desired_num_repertoires=self.desired_num_repertoires, abs_num_of_reps_list=abs_rep_num)
        ImplantationHelper.write_public_repertoire_chunks(original_repertoire_file=original_rep_file,
                                                          output_files_path=self.tmp_chunks_path,
                                                          repertoire_sequence_presence_indices=seq_presence_indices,
                                                          file_type="pickle")

    def multi_generate_public_repertoires(self):
        found_pgen_files = glob.glob(self.pgen_files_path + "/pgen_*.tsv", recursive=False)
        pool = Pool(self.n_threads)
        pool.map(self.generate_public_repertoires, found_pgen_files)

    def concatenate_public_repertoire_chunks(self, pgen_file_chunks_list):
        concat_fn = os.path.join(self.corrected_public_repertoires_path,
                                 os.path.basename(pgen_file_chunks_list[0]).replace(".pkl", ".tsv"))
        chunk_dfs_list = []
        for file_chunk in pgen_file_chunks_list:
            chunk_df = pd.read_pickle(file_chunk)
            chunk_dfs_list.append(chunk_df)
        concatenated_df = pd.concat(chunk_dfs_list)
        concatenated_df.to_csv(concat_fn, header=None, index=None, sep='\t')

    def multi_concatenate_public_repertoire_chunks(self):
        found_pgen_file_chunks = []
        for i in range(self.desired_num_repertoires):
            found_pgen_files = glob.glob(self.tmp_chunks_path + f"/*/rep_{i}.pkl", recursive=True)
            found_pgen_file_chunks.append(found_pgen_files)
        pool = Pool(self.n_threads)
        pool.map(self.concatenate_public_repertoire_chunks, found_pgen_file_chunks)

    def execute(self):
        self.multi_generate_public_repertoires()
        self.multi_concatenate_public_repertoire_chunks()
