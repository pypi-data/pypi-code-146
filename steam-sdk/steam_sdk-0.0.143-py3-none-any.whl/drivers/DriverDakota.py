import os
import shutil
import subprocess
from steam_sdk.analyses.AnalysisSTEAM import AnalysisSTEAM


class DriverDakota:

    def __init__(self, dakota_path, analysis_yaml_path=None, settings_path: str = None, iterable_steps=None, dakota_input_folder=None):

        # Define settings file
        self.dakota_path = dakota_path
        self.analysis_yaml_path = analysis_yaml_path
        self.settings_path = settings_path
        self.iterable_steps = iterable_steps
        self.dakota_input_folder = dakota_input_folder

        self.analysis_yaml_local_path = None
        self.builder_model_obj_path = os.path.join(self.dakota_input_folder, 'temp.pkl')

    def prepare(self):
        analysis = AnalysisSTEAM(file_name_analysis=self.analysis_yaml_path, relative_path_settings=self.settings_path, verbose=True)
        analysis.run_analysis()
        analysis.store_model_objects(self.builder_model_obj_path)

        analysis_yaml_local_path = os.path.join(self.dakota_input_folder, os.path.basename(self.analysis_yaml_path))
        shutil.copyfile(self.analysis_yaml_path, analysis_yaml_local_path)
        self.analysis_yaml_local_path = analysis_yaml_local_path

    def run(self, input_file_path):
        """
        Runs dakota.exe with the input file specified
        :param input_file_path: full path to the input file, with its name and .in
        :return: None, runs dakota
        """
        # os.chdir(self.dakota_output_folder)

        # with open(r"C:\Users\avitrano\PycharmProjects\steam_sdk\tests\parsims\FiQuS_run\summary.dat", 'w') as file:
        #     file.write("mesh_coil.SizeMin mesh_coil.SizeMax mesh_iron.SizeMin mesh_iron.SizeMax solution_time overall_error weighted_sum SJ SICN SIGE Gamma nodes minimum_diff maximum_diff\n")

        print(f'`Changed working directory to: {self.dakota_input_folder}')
        path_to_driver_link = os.path.join(self.dakota_input_folder, 'driver_link.py')
        with open(path_to_driver_link, 'w') as f:
            f.write('from steam_sdk.drivers.DriverAnalysis import DriverAnalysis')
            f.write(f'\nda = DriverAnalysis(analysis_yaml_path=r"{self.analysis_yaml_local_path}", settings_path=r"{self.settings_path}", analysis_models_path=r"{self.builder_model_obj_path}", iterable_steps={self.iterable_steps})')
            f.write('\nda.drive()')
        print('DriverDakota.run called')
        subprocess.call([self.dakota_path, '-i', input_file_path])

        # p = Popen([self.dakota_path, '-i', input_file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # output, err = p.communicate()
        # rc = p.returncode
        # print(output)
        # print(err)
