import glob
import os.path
import numpy as np
import pandas as pd
import random
import logging
from simAIRR.expand_repertoire_components.ImplantationHelper import ImplantationHelper
from simAIRR.util.utilities import write_yaml_file


class SignalComponentGeneration:
    def __init__(self, outdir_path, pgen_count_map_obj, desired_num_repertoires, desired_phenotype_burden, seed,
                 phenotype_pool_size=None, allow_closer_phenotype_burden=True):
        self.signal_components_path = os.path.join(outdir_path, "signal_components")
        self.pgen_file = \
        glob.glob(os.path.join(self.signal_components_path, "pgen_files", "pgen_*.tsv"), recursive=False)[0]
        self.signal_chunks_path = os.path.join(self.signal_components_path, "signal_rep_chunks")
        self.pgen_count_map_obj = pgen_count_map_obj
        self.desired_num_repertoires = desired_num_repertoires
        self.desired_phenotype_burden = desired_phenotype_burden
        self.phenotype_pool_size = phenotype_pool_size
        self.seed = seed
        self.desired_total_implantation_count = int(round(self.desired_num_repertoires * self.desired_phenotype_burden))
        self.allow_closer_phenotype_burden = allow_closer_phenotype_burden
        if not os.path.exists(self.signal_components_path):
            os.makedirs(self.signal_components_path)
        if not os.path.exists(self.signal_chunks_path):
            os.makedirs(self.signal_chunks_path)

    def generate_signal_components(self, write_signal_components=True):
        pgen_dat = pd.read_csv(self.pgen_file, header=None, index_col=None, sep='\t', names=['aa_seq', 'pgen'])
        pgen_intervals_array = ImplantationHelper.get_pgen_intervals(pgen_dat=pgen_dat,
                                                                     pgen_count_map_obj=self.pgen_count_map_obj)
        obtained_pool_size, implantation_stats = self._get_signal_seq_combination(pgen_intervals_array)
        sequence_proportion, implantation_count, implantable_seq_subset_indices = implantation_stats[0], \
                                                                                  implantation_stats[1], \
                                                                                  implantation_stats[2]
        possible_phen_burden = round(implantation_count / self.desired_num_repertoires)
        self._write_implantation_stats_to_disk(possible_phen_burden, obtained_pool_size, implantation_count)
        signal_generation_status_code = self._assess_signal_generation_feasibility(possible_phen_burden)
        if signal_generation_status_code == 0 and write_signal_components:
            self._write_signal_components(implantable_seq_subset_indices, pgen_intervals_array)
        return signal_generation_status_code

    def _assess_signal_generation_feasibility(self, possible_phen_burden):
        logging.info(
            f'Assessing the feasibility of signal implantation at the desired phenotype burden: '
            f'{self.desired_phenotype_burden}')
        if possible_phen_burden != self.desired_phenotype_burden:
            signal_generation_status_code = 1
            logging.warning('Assessed that precise match of user-desired phenotype burden not feasible.')
        else:
            signal_generation_status_code = 0
            logging.info('Assessed that user-desired phenotype burden feasible.')
        if self.allow_closer_phenotype_burden:
            if possible_phen_burden not in range(self.desired_phenotype_burden - 1, self.desired_phenotype_burden + 2):
                signal_generation_status_code = 1
                logging.warning('Feasible phenotype burden not within a closer range of user-desired phenotype burden.')
            else:
                signal_generation_status_code = 0
                logging.info('Using closest possible phenotype burden ...')
        return signal_generation_status_code

    def _write_signal_components(self, implantable_seq_subset_indices, pgen_intervals_array):
        logging.info('Generating and writing signal component chunks ...')
        original_rep_file = os.path.join(self.signal_components_path,
                                         os.path.basename(self.pgen_file).replace('pgen_', ''))
        original_seqs = pd.read_csv(original_rep_file, header=None, index_col=None, sep='\t')
        filtered_signal_pool_file = os.path.join(self.signal_components_path,
                                                 "filtered_implantable_signal_pool.tsv")
        original_seqs.loc[implantable_seq_subset_indices].to_csv(filtered_signal_pool_file, header=None,
                                                                 index=None, sep='\t')
        abs_rep_num = ImplantationHelper.get_absolute_number_of_repertoires(
            pgen_intervals_list=[pgen_intervals_array[ind] for ind in implantable_seq_subset_indices],
            pgen_count_map_obj=self.pgen_count_map_obj)
        np.savetxt(os.path.join(self.signal_components_path, "implanted_sequences_frequencies.txt"),
                   abs_rep_num, fmt="%s")
        seq_presence_indices = ImplantationHelper.get_repertoire_sequence_presence_indices(
            desired_num_repertoires=self.desired_num_repertoires, abs_num_of_reps_list=abs_rep_num)
        ImplantationHelper.write_public_repertoire_chunks(original_repertoire_file=filtered_signal_pool_file,
                                                          output_files_path=self.signal_chunks_path,
                                                          repertoire_sequence_presence_indices=seq_presence_indices,
                                                          file_type="tsv")

    def _determine_signal_sequence_combination(self, pgen_intervals_array, pool_size):
        if len(pgen_intervals_array) > pool_size:
            valid_seq_proportions = [1 - seq_proportion for seq_proportion in
                                     [0, 0.05, 0.10, 0.20, 0.40, 0.60, 0.80, 0.90, 0.95] if
                                     seq_proportion * len(pgen_intervals_array) > pool_size]
            subset_seqs_total_implant_counts = {}
            subset_seq_indices = {}
            random.seed(self.seed)
            for seq_proportion in valid_seq_proportions:
                to_subset_indices = random.sample(
                    range(int(round(len(pgen_intervals_array) * seq_proportion)), len(pgen_intervals_array)), pool_size)
                subset_pgen_array = [pgen_intervals_array[ind] for ind in to_subset_indices]
                subset_seqs_total_implant_counts[seq_proportion] = self._get_avg_total_implantation_count(
                    subset_pgen_array)
                subset_seq_indices[seq_proportion] = to_subset_indices
            condition_met = dict((k, v) for k, v in subset_seqs_total_implant_counts.items() if
                                 round(v / self.desired_num_repertoires) == self.desired_phenotype_burden)
            if condition_met:
                sequence_proportion, implantation_count = min(condition_met.items(), key=lambda x: x[0])
                implantable_seq_subset_indices = subset_seq_indices[sequence_proportion]
            else:
                sequence_proportion, implantation_count = min(subset_seqs_total_implant_counts.items(),
                                                              key=lambda k: abs(round(k[1] / self.desired_num_repertoires) - self.desired_phenotype_burden))
                implantable_seq_subset_indices = subset_seq_indices[sequence_proportion]
        else:
            implantation_count = self._get_avg_total_implantation_count(pgen_intervals_array)
            sequence_proportion = 0
            implantable_seq_subset_indices = list(range(len(pgen_intervals_array)))
        return sequence_proportion, implantation_count, implantable_seq_subset_indices

    def _get_avg_total_implantation_count(self, pgen_intervals_array):
        multi_abs_rep_num = []
        for i in range(1000):
            abs_rep_num = ImplantationHelper.get_absolute_number_of_repertoires(
                pgen_intervals_list=pgen_intervals_array,
                pgen_count_map_obj=self.pgen_count_map_obj)
            multi_abs_rep_num.append(abs_rep_num)
        abs_rep_num_sums = [sum(abs_rep_num_list) for abs_rep_num_list in multi_abs_rep_num]
        avg_total = sum(abs_rep_num_sums) / len(abs_rep_num_sums)
        return int(avg_total)

    def _get_signal_seq_combination(self, pgen_intervals_array):
        if self.phenotype_pool_size is None:
            logging.warning('No phenotype pool size is given. Will attempt to determine suitable phenotype pool size.')
            possible_pool_sizes = [round(len(pgen_intervals_array) * prop) for prop in
                                   [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                                    1.0]]  # TODO: enhance this in such a way that iteratively the pool sizes are
            # updated on the fly based on desired phenotype burden falling within a range of pool sizes.
        else:
            possible_pool_sizes = [self.phenotype_pool_size]
            logging.info(f'Using the user-defined phenotype pool size {self.phenotype_pool_size}')
        optimal_implantation_stats = {}
        for pool_size in possible_pool_sizes:
            logging.info(f"Determining signal sequence combination for pool size: ----------: {pool_size}")
            optimal_implantation_stats[pool_size] = list(
                self._determine_signal_sequence_combination(pgen_intervals_array, pool_size))
        condition_met = dict((k, v) for k, v in optimal_implantation_stats.items() if
                             round(v[1] / self.desired_num_repertoires) == self.desired_phenotype_burden)
        if condition_met:
            obtained_pool_size, implantation_stats = min(condition_met.items(), key=lambda x: x[0])
        else:
            obtained_pool_size, implantation_stats = min(optimal_implantation_stats.items(), key=lambda x: abs(
                round(x[1][1] / self.desired_num_repertoires) - self.desired_phenotype_burden))
        return obtained_pool_size, implantation_stats

    def _write_implantation_stats_to_disk(self, possible_phen_burden, obtained_pool_size, implantation_count):
        out_yaml_dict = {'a. Desired number of positive-labeled repertoires': self.desired_num_repertoires,
                         'b. Desired phenotype burden': self.desired_phenotype_burden,
                         'c. Desired implantation pool size': self.phenotype_pool_size,
                         'd. Desired total implantation count (a*b)': self.desired_total_implantation_count,
                         'e. Possible phenotype burden': possible_phen_burden,
                         'f. Possible/Chosen implantation pool size': obtained_pool_size,
                         'g. Possible total implantation count (a*e)': implantation_count}
        write_yaml_file(out_yaml_dict, os.path.join(self.signal_components_path, "signal_implantation_stats.yaml"))
