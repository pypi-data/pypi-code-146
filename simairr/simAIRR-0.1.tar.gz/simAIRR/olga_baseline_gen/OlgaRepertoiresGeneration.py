import os
from multiprocessing import Pool
from simAIRR.util.utilities import makedir_if_not_exists


class OlgaRepertoiresGeneration:

    def __init__(self, model: str, output_file_path: str, n_seq: int, seed: int, n_reps: int, n_threads: int):
        self.model = model
        self.output_file_path = output_file_path
        self.n_seq = n_seq #TODO: use only 65% of desired n_seq to account for increased seq because of public counts
        self.seed = seed
        self.n_reps = n_reps
        self.n_threads = n_threads

    def olga_generate_multiple_repertoires(self):
        makedir_if_not_exists(self.output_file_path, fail_if_exists=True)
        pool = Pool(self.n_threads)
        number_reps = list(range(1, self.n_reps + 1))
        pool.map(self._olga_generate_repertoire, number_reps)

    def _olga_generate_repertoire(self, rep):
        out_filename = os.path.join(self.output_file_path, 'rep_' + str(rep) + '.tsv')
        rep_seed = rep + self.seed
        command = 'olga-generate_sequences --' + self.model + ' -o ' + out_filename + ' -n ' + str(
            self.n_seq) + ' --seed ' + str(rep_seed)
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError(f"Running olga tool failed:{command}.")
