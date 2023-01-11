import os
import glob
import secrets
from multiprocessing import Pool
import pandas as pd
from simAIRR.util.utilities import makedir_if_not_exists


class RepComponentConcatenation:
    def __init__(self, components_type, super_path, n_threads, export_nt=None):
        self.components_type = components_type
        self.super_path = str(super_path).rstrip('/')
        self.n_threads = n_threads
        self.export_nt = export_nt
        self.proxy_primary_fns = None

    def _set_component_specific_paths(self):
        # super_path in case of "public_private" concatenation is baseline_repertoires_path and
        # in case of signal+baseline is output_path (to be related with attributes of workflows class)
        if self.components_type == "public_private":
            self.primary_reps_path = os.path.join(self.super_path, "corrected_public_repertoires")
            self.secondary_reps_path = os.path.join(self.super_path, "filtered_private_repertoires")
            self.concatenated_reps_path = os.path.join(os.path.dirname(self.super_path),
                                                       "corrected_baseline_repertoires")
        else:
            self.primary_reps_path = os.path.join(self.super_path, "corrected_baseline_repertoires")
            self.secondary_reps_path = os.path.join(self.super_path, "signal_components", "signal_rep_chunks",
                                                    "filtered_implantable_signal_pool")
            self.concatenated_reps_path = os.path.join(self.super_path, "simulated_repertoires")

    def concatenate_repertoire_components(self, file_number):
        rep_file_name = f"rep_{file_number}.tsv"
        if self.components_type == "baseline_and_signal":
            concat_fn = os.path.join(self.concatenated_reps_path, self.proxy_primary_fns[file_number])
        else:
            concat_fn = os.path.join(self.concatenated_reps_path, rep_file_name)
        primary_rep = os.path.join(self.primary_reps_path, rep_file_name)
        secondary_rep = os.path.join(self.secondary_reps_path, rep_file_name)
        dfs_list = []
        for rep_file in [primary_rep, secondary_rep]:
            try:
                rep_df = pd.read_csv(rep_file, header=None, index_col=None, sep='\t')
                dfs_list.append(rep_df)
            except (pd.errors.EmptyDataError, FileNotFoundError) as e:
                continue
        concatenated_df = pd.concat(dfs_list)
        if self.export_nt is False:
            concatenated_df = concatenated_df.drop(concatenated_df.columns[[0]], axis=1)
        concatenated_df.to_csv(concat_fn, header=None, index=None, sep='\t')

    def multi_concatenate_repertoire_components(self):
        self._set_component_specific_paths()
        makedir_if_not_exists(self.concatenated_reps_path, fail_if_exists=True)
        found_primary_reps = glob.glob(self.primary_reps_path + "/rep_*.tsv", recursive=False)
        found_secondary_reps = glob.glob(self.secondary_reps_path + "/rep_*.tsv", recursive=False)
        if self.components_type == "baseline_and_signal":
            primary_rep_fns = [os.path.basename(rep) for rep in found_primary_reps]
            proxy_subject_ids = [secrets.token_hex(16) for i in range(len(found_primary_reps))]
            self.proxy_primary_fns = [subject_id + ".tsv" for subject_id in proxy_subject_ids]
            secondary_rep_fns = [os.path.basename(rep) for rep in found_secondary_reps]
            metadata_dict = {'subject_id': proxy_subject_ids, 'filename': self.proxy_primary_fns,
                             'label_positive': [True if rep in secondary_rep_fns else False for rep in primary_rep_fns]}
            metadata_df = pd.DataFrame.from_dict(metadata_dict)
            metadata_df.to_csv(os.path.join(self.super_path, "metadata.csv"))
            metadata_df.to_csv(os.path.join(self.concatenated_reps_path, "metadata.csv"))
        else:
            assert len(found_primary_reps) == len(found_secondary_reps)
        pool = Pool(self.n_threads)
        pool.map(self.concatenate_repertoire_components, list(range(len(found_primary_reps))))
