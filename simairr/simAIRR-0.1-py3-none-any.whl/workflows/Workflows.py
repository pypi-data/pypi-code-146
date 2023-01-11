import logging
import os
import pandas as pd
import numpy as np
import shutil
from simAIRR.concatenate_repertoire_components.RepComponentConcatenation import RepComponentConcatenation
from simAIRR.expand_repertoire_components.PublicRepertoireGeneration import PublicRepertoireGeneration
from simAIRR.expand_repertoire_components.SignalComponentGeneration import SignalComponentGeneration
from simAIRR.olga_baseline_gen.OlgaRepertoiresGeneration import OlgaRepertoiresGeneration
from simAIRR.olga_compute_pgen.OlgaPgenComputation import OlgaPgenComputation
from simAIRR.olga_compute_pgen.UniqueSequenceFilter import UniqueSequenceFilter
from simAIRR.pgen_count_map.PgenCountMap import PgenCountMap
from simAIRR.util.utilities import makedir_if_not_exists, sort_olga_seq_by_pgen


class Workflows:
    def __init__(self, mode: str = None, olga_model: str = None, output_path: str = None, n_sequences: int = None,
                 n_repertoires: int = None, n_threads: int = None, seed: int = None,
                 public_seq_proportion: float = None, public_seq_pgen_count_mapping_file: str = None,
                 signal_pgen_count_mapping_file: str = None,
                 signal_sequences_file: str = None, positive_label_rate: float = None, phenotype_burden: int = None,
                 phenotype_pool_size: int = None, allow_closer_phenotype_burden: bool = None,
                 store_intermediate_files: bool = None, export_nt: bool = None):
        """

        :param mode: str
        :param olga_model: str
        :param output_path: str
        :param n_sequences: int
        :param n_repertoires: int
        :param n_threads: int
        :param seed: int
        :param public_seq_proportion: float
        :param public_seq_pgen_count_mapping_file: str
        :param signal_pgen_count_mapping_file: str
        :param signal_sequences_file: str
        :param positive_label_rate: float
        :param phenotype_burden: int
        :param phenotype_pool_size: int
        :param allow_closer_phenotype_burden: bool
        """
        self.mode = mode
        self.olga_model = olga_model
        self.output_path = output_path
        self.baseline_reps_path = os.path.join(self.output_path, "baseline_repertoires")
        self.filtered_public_reps_path = os.path.join(self.baseline_reps_path, "filtered_public_repertoires")
        self.n_sequences = n_sequences
        self.n_repertoires = n_repertoires
        self.n_threads = n_threads
        self.seed = seed
        self.public_seq_proportion = public_seq_proportion
        self.public_seq_pgen_count_mapping_file = public_seq_pgen_count_mapping_file
        self.signal_pgen_count_mapping_file = signal_pgen_count_mapping_file
        self.signal_sequences_file = signal_sequences_file
        self.positive_label_rate = positive_label_rate
        self.phenotype_burden = phenotype_burden
        self.phenotype_pool_size = phenotype_pool_size
        self.allow_closer_phenotype_burden = allow_closer_phenotype_burden
        self.export_nt = export_nt
        self.store_intermediate_files = store_intermediate_files

    def _baseline_repertoire_generation(self):
        olga_reps = OlgaRepertoiresGeneration(model=self.olga_model, output_file_path=self.baseline_reps_path,
                                              n_seq=self.n_sequences, seed=self.seed,
                                              n_reps=self.n_repertoires, n_threads=self.n_threads)
        logging.info(f'Generating baseline repertoires with the following parameters --- {vars(olga_reps)}')
        olga_reps.olga_generate_multiple_repertoires()

    def _public_component_correction(self):
        seq_filter = UniqueSequenceFilter(baseline_repertoires_path=self.baseline_reps_path,
                                          public_sequence_proportion=self.public_seq_proportion, seed=self.seed)
        logging.info(f'Filtering sequences to retain unique sequences and writing public, private components.')
        seq_filter.write_unique_public_and_private_repertoire_components()
        comp_pgen = OlgaPgenComputation(self.filtered_public_reps_path, n_threads=self.n_threads,
                                        model=self.olga_model)
        logging.info(f'Computing pgen of public component sequences on {self.n_threads} processes.')
        comp_pgen.multi_compute_pgen()
        pgen_count_map = PgenCountMap(number_of_repertoires=self.n_repertoires,
                                      pgen_count_map_file=self.public_seq_pgen_count_mapping_file)
        pub_rep_gen = PublicRepertoireGeneration(public_repertoires_path=self.filtered_public_reps_path,
                                                 n_threads=self.n_threads, pgen_count_map_obj=pgen_count_map,
                                                 desired_num_repertoires=self.n_repertoires)
        logging.info('Generating public repertoire components based on empirical relationship between pgen and public '
                     'sequence counts.')
        pub_rep_gen.execute()
        rep_concat = RepComponentConcatenation(components_type="public_private", super_path=self.baseline_reps_path,
                                               n_threads=self.n_threads)
        logging.info('Concatenating public and private repertoire components')
        rep_concat.multi_concatenate_repertoire_components()

    def _signal_component_generation(self):
        user_signal = self._parse_and_validate_user_signal()
        self.signal_components_path = os.path.join(self.output_path, "signal_components")
        makedir_if_not_exists(self.signal_components_path, fail_if_exists=True)
        user_signal_file = os.path.join(self.signal_components_path, "user_supplied_signal.tsv")
        user_signal_pgen_file = os.path.join(self.signal_components_path, "pgen_files", "pgen_user_supplied_signal.tsv")
        user_signal.to_csv(user_signal_file, header=None, sep='\t', index=None)
        logging.info('Read in the user-supplied signal sequences file. Starting to compute generation probability.')
        pgen_compute = OlgaPgenComputation(repertoires_path=self.signal_components_path, n_threads=1,
                                           model=self.olga_model)
        pgen_compute.compute_pgen(user_signal_file)
        sort_olga_seq_by_pgen(user_signal_file, user_signal_pgen_file)
        self.n_pos_repertoires = int(round(self.n_repertoires * self.positive_label_rate))
        signal_pgen_count_map = PgenCountMap(number_of_repertoires=self.n_pos_repertoires,
                                             pgen_count_map_file=self.signal_pgen_count_mapping_file)
        signal_gen = SignalComponentGeneration(outdir_path=self.output_path, pgen_count_map_obj=signal_pgen_count_map,
                                               desired_num_repertoires=self.n_pos_repertoires,
                                               desired_phenotype_burden=self.phenotype_burden, seed=self.seed,
                                               phenotype_pool_size=self.phenotype_pool_size,
                                               allow_closer_phenotype_burden=self.allow_closer_phenotype_burden)
        return signal_gen

    def _parse_and_validate_user_signal(self):
        user_signal = pd.read_csv(self.signal_sequences_file, header=None, sep='\t', index_col=None)
        assert user_signal.shape[1] >= 3, "The user-supplied sequence file is expected to contain at least 3 fields " \
                                          "with aa sequence, v gene and j gene information. Found less than 3 fields."
        if user_signal.shape[1] == 3:
            self.export_nt = False
            user_signal.insert(0, 'nt_seq', "NA")
        if user_signal.shape[1] == 4:
            if not user_signal.iloc[:, 0].isnull().any():
                if np.mean([len(seq) for seq in user_signal.iloc[:, 0]]) < 20:
                    self.export_nt = False
            if user_signal.iloc[:, 0].isnull().all():
                self.export_nt = False
        return user_signal

    def _simulated_repertoire_generation(self):
        rep_concat = RepComponentConcatenation(components_type="baseline_and_signal", super_path=self.output_path,
                                               n_threads=self.n_threads, export_nt=self.export_nt)
        logging.info('Concatenating the signal component and baseline repertoire component')
        rep_concat.multi_concatenate_repertoire_components()

    def workflow_generate_baseline_repertoires(self):
        self._baseline_repertoire_generation()

    def workflow_generate_public_component_corrected_repertoires(self):
        self._baseline_repertoire_generation()
        self._public_component_correction()
        if not self.store_intermediate_files:
            shutil.rmtree(self.baseline_reps_path)

    def workflow_generate_signal_implanted_repertoires(self):
        signal_gen = self._signal_component_generation()
        signal_generation_status = signal_gen.generate_signal_components()
        if signal_generation_status == 0:
            self._baseline_repertoire_generation()
            self._public_component_correction()
            self._simulated_repertoire_generation()
            if not self.store_intermediate_files:
                shutil.rmtree(self.baseline_reps_path)
                shutil.rmtree(os.path.join(self.output_path, "corrected_baseline_repertoires"))

    def workflow_assess_signal_feasibility(self):
        signal_gen = self._signal_component_generation()
        signal_gen.generate_signal_components(write_signal_components=False)

    def execute(self):
        mode_methods = {"baseline_repertoire_generation": self.workflow_generate_baseline_repertoires,
                        "public_component_correction": self.workflow_generate_public_component_corrected_repertoires,
                        "signal_implantation": self.workflow_generate_signal_implanted_repertoires,
                        "signal_feasibility_assessment": self.workflow_assess_signal_feasibility}
        logging.info(f'Starting the execution of desired workflow: {self.mode}')
        mode_methods.get(self.mode)()
