import os
import shutil
import subprocess
from steam_nb_api.ledet.NotebookLEDET_V2 import Notebook_LEDET

from steam_nb_api.resources.ResourceReader import read_yaml

class Sim_LEDET:

    def __init__(self, circuit_name, model_no, LEDET_folder, magnet_inputs_path=''):
        self.circuit_name = circuit_name
        self.model_no = model_no
        self.LEDET_folder = LEDET_folder
        self.magnet_inputs_path = magnet_inputs_path

    @staticmethod
    def ensure_dir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def copy_move_file(dest_folder, source_folder, file, operation):
        dst_file = os.path.join(dest_folder, file)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        if operation =='copy':
            shutil.copy(os.path.join(source_folder, file), dest_folder)
        elif operation =='move':
            shutil.move(os.path.join(source_folder, file), dest_folder)
        else:
            raise Exception(f'Operation {operation} not supported.')

    def get_pre_calc_timing(self):
        initial_path = os.getcwd()
        if self.magnet_inputs_path != '':
            os.chdir(self.magnet_inputs_path)
        solenoid_data = read_yaml('circuit', self.circuit_name)
        os.chdir(initial_path)
        return solenoid_data['t_pre_calc'], solenoid_data['simul_time'][0]['step']


    def gen_LEDET_input(self, t_PC, simul_time='file', **kwargs):
        initial_path = os.getcwd()
        if self.magnet_inputs_path != '':
            os.chdir(self.magnet_inputs_path)
        if 'for_cosim' in kwargs:
            if kwargs['for_cosim']:
                self.LEDET_notebook = Notebook_LEDET(self.circuit_name, typeMagnet='solenoid', **kwargs)
        else:
            self.LEDET_notebook = Notebook_LEDET(self.circuit_name, typeMagnet='solenoid', model_no=self.model_no, **kwargs)
        self.LEDET_notebook.load_Options('solenoid')
        self.LEDET_notebook.load_VariablesToStore()
        self.LEDET_notebook.load_PlotOptions()
        if 'flag_generateReport' in kwargs:
            if kwargs['flag_generateReport']:
                self.LEDET_notebook.Magnet.Options.flag_generateReport = 1
            else:
                self.LEDET_notebook.Magnet.Options.flag_generateReport = 0
        self.LEDET_notebook.writeLEDETFile(f'{self.circuit_name}_{self.model_no}.xlsx', locals(), t_PC=t_PC, simul_time=simul_time)
        self.LEDET_notebook.write_start_bat(self.model_no)
        os.chdir(initial_path)
        self.source_folder = self.LEDET_notebook.out_dir


    def prep_LEDET_files(self, **kwargs):
        Input_folder = os.path.join(self.LEDET_folder, 'LEDET', f"{self.circuit_name}", 'Input')
        Field_maps_folder = os.path.join(self.LEDET_folder, 'Field maps', f"{self.circuit_name}")
        LEDET_xlsx = f'{self.circuit_name}_{self.model_no}.xlsx'
        LEDET_bat = f"{self.circuit_name}_{self.model_no}.bat"
        Mut_Ind = f"{self.circuit_name}_selfMutualInductanceMatrix.csv"
        field_maps = []
        for file in os.listdir(self.source_folder):
            if file.endswith(".map2d"):
                field_maps.append(file)
        folders = [*[Input_folder]*3, *[Field_maps_folder]*len(field_maps)]
        files = [LEDET_xlsx, LEDET_bat, Mut_Ind, *field_maps]
        for file, dest_folder in zip(files, folders):
            self.ensure_dir(dest_folder)
            self.copy_move_file(dest_folder, self.source_folder, file, 'copy')
        if 'copy_to_folder' in kwargs:
            ctf = kwargs['copy_to_folder']
            folders = [*[ctf]*3, *[ctf]*len(field_maps)]
            for file, dest_folder in zip(files, folders):
                self.ensure_dir(dest_folder)
                self.copy_move_file(dest_folder, self.source_folder, file, 'copy')


    def run_LEDET(self):
        #print([os.path.join(self.LEDET_folder, f"{os.path.normpath(self.LEDET_folder).split(os.sep)[-1]}.exe"), os.path.join(self.LEDET_folder, 'LEDET'), self.circuit_name, str(self.model_no)])
        subprocess.call([os.path.join(self.LEDET_folder, f"{os.path.normpath(self.LEDET_folder).split(os.sep)[-1]}.exe"), os.path.join(self.LEDET_folder, 'LEDET'), self.circuit_name, str(self.model_no)], stdout=subprocess.DEVNULL)

    def run_LEDET_bat(self):
        initial_path = os.getcwd()
        model_dir = os.path.join(self.LEDET_folder, "LEDET", self.circuit_name, "Input")
        os.chdir(model_dir)
        batch_file_path = os.path.join(model_dir, f"{self.circuit_name}_{self.model_no}.bat")
        print(f"Running {batch_file_path}")
        p = subprocess.Popen(batch_file_path, shell=False,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            excel_file_path = os.path.join(model_dir, f"{self.circuit_name}_{self.model_no}.xlsx")
            raise Exception(f"LEDET returned error while running {excel_file_path}")
        os.chdir(initial_path)

if __name__ == "__main__":
    magnet_inputs_path = r'C:\Users\mawoznia\cernbox\COSIM\steam-notebooks\steam-ledet-input\HEL'
    LEDET_folder_path = r"D:\LEDET\LEDET_v2_01_35"
    s = Sim_LEDET("RLEMx2", 1, LEDET_folder_path, magnet_inputs_path=magnet_inputs_path)
    s.gen_LEDET_input(t_PC=0.028)
    s.LEDET_notebook.plot_heat_exchange_order()

