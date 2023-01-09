import os
import sys


class DriverFiQuS:
    """
        Class to drive FiQuS models
    """
    def __init__(self, FiQuS_path='', path_folder_FiQuS=None, path_folder_FiQuS_input=None, verbose=False):
        self.FiQuS_path = FiQuS_path
        self.path_folder_FiQuS = path_folder_FiQuS
        self.path_folder_FiQuS_input = path_folder_FiQuS_input
        self.verbose = verbose
        if verbose:
            print('path_exe =          {}'.format(FiQuS_path))
            print('path_folder_FiQuS = {}'.format(path_folder_FiQuS))

        sys.path.insert(0, FiQuS_path)
        from fiqus.MainFiQuS import MainFiQuS as MF
        self.MainFiQuS = MF

    def run_FiQuS(self, sim_file_name: str, output_directory: str = 'output', verbose: bool = False):
        full_path_input = os.path.join(self.path_folder_FiQuS_input, sim_file_name + '.yaml')
        full_path_output = os.path.join(self.path_folder_FiQuS, output_directory)

        # Run model
        return self.MainFiQuS(input_file_path=full_path_input, model_folder=full_path_output).summary
        # return subprocess.call(['py', self.path_exe, model_data_path, outputDirectory])

