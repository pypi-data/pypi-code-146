import glob
import os
from multiprocessing import Pool


class OlgaPgenComputation:
    def __init__(self, repertoires_path: str, n_threads: int, model: str):
        self.repertoires_path = str(repertoires_path)
        self.n_threads = n_threads
        self.model = model
        self.pgen_files_base_path = os.path.join(self.repertoires_path, "pgen_files")
        if not os.path.exists(self.pgen_files_base_path):
            os.makedirs(self.pgen_files_base_path)

    def compute_pgen(self, repertoire_file_path):
        pgen_file_path = os.path.join(self.pgen_files_base_path, 'pgen_' + os.path.basename(repertoire_file_path))
        command = 'olga-compute_pgen --' + self.model + ' -i ' + repertoire_file_path + ' -o ' + pgen_file_path \
                  + ' --seq_type_out aaseq --seq_in 1 --v_in 2 --j_in 3 --display_off'
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError(f"Running olga tool failed:{command}.")

    def multi_compute_pgen(self):
        found_files = glob.glob(self.repertoires_path + "/rep_*.tsv", recursive=False)
        pool = Pool(self.n_threads)
        pool.map(self.compute_pgen, found_files)
