import math
import os
import re
import csv
from typing import List, Dict
import pandas as pd

# from steam_sdk.analyses.AnalysisSTEAM import AnalysisSTEAM
from steam_sdk.builders.BuilderModel import BuilderModel
from steam_sdk.data.DataAnalysis import ModifyModelMultipleVariables
from steam_sdk.data.DataEventMagnet import DataEventMagnet
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.sgetattr import rsetattr, rgetattr


class ParsimEventMagnet:
    """

    """

    def __init__(self, ref_model: BuilderModel = None, verbose: bool = True):
        """
        If verbose is set to True, additional information will be displayed
        """
        # Unpack arguments
        self.verbose: bool = verbose
        self.list_events: List[DataEventMagnet] = []
        self.dict_AnalysisStepDefinition = {}
        self.list_AnalysisStepSequence = []
        # save local reference model, so that empty field in EventData.csv can be populated with default ones
        self.ref_model = ref_model
        # TODO add a dictionary of default values?


    def read_from_input(self, path_input_file: str, flag_append: bool):
        # TODO: maybe call this function build_DataEventMagnet_from_table()
        '''
        Read a list of events from an input .csv file and assign its content to a list of DataEventMagnet() objects.
        This method is used to read and set the variables that can be expressed with one or a limited amount of values.
        More complex variables are covered by dedicated methods.

        :param path_input_file: Path to the .csv file to read
        :param flag_append: If True, merge the content of the file to the current list of events. If False, overwrite it.
        :return:
        '''

        # Read the input file
        if path_input_file.endswith('.csv'):
            df_events = pd.read_csv(path_input_file)
        elif path_input_file.endswith('.xlsx'):
            df_events = pd.read_excel(path_input_file)
        else:
            raise Exception(f'The extension of the file {path_input_file} is not supported.')

        # Assign the content to a dataclass structure
        list_events = []
        for index, event_info in df_events.iterrows():
            new_event = DataEventMagnet()

            self.__set_general_parameters(event_info, new_event)
            self.__set_powering(event_info, new_event)
            self.__set_QH(event_info, new_event)
            self.__set_CLIQ(event_info, new_event)

            list_events.append(new_event)

        # Update attribute
        if flag_append:
            self.list_events += list_events
        else:
            self.list_events = list_events


    def set_up_analysis(self, model_name: str, simulation_numbers: List[int], simulation_name: str, software : List[str], t_PC_off: float, current_polarities_CLIQ: List[int], list_QH_strips_to_units: List[List[int]], path: str):
        '''
        Make an AnalysisSTEAM object from the list of DataEventMagnet objects

        :return: List of read DataEventMagnet objects
        '''
        # check inputs
        if len(simulation_numbers) != len(self.list_events):
            raise Exception(
                f'length of input simulation numbers ({len(simulation_numbers)}) differs from length of events found in the input file ({len(self.list_events)})')

        # Go in a loop trough each element of self.list_events and save steps for analysis
        for i, event in enumerate(self.list_events):
            self.__set_analysis_powering(model_name, event, i, t_PC_off)
            self.__set_analysis_CLIQ(model_name, event, i, current_polarities_CLIQ)
            self.__set_analysis_QH(model_name, event, i, list_QH_strips_to_units)
            self.__set_analysis_general_parameters(model_name, simulation_numbers, simulation_name, software, event, i)
        # define fieldnames of all parameters
        fieldnames = ['simulation_name', 'simulation_number', 'comments',
                      'GeneralParameters.T_initial',
                      'Power_Supply.I_initial', 'Power_Supply.t_off', 'Power_Supply.R_crowbar',
                      'Power_Supply.Ud_crowbar', 'Power_Supply.t_control_LUT', 'Power_Supply.I_control_LUT',
                                                                               'Quench_Protection.CLIQ.t_trigger',
                      'Quench_Protection.CLIQ.U0', 'Quench_Protection.CLIQ.C', 'Quench_Protection.CLIQ.R',
                      'Quench_Protection.CLIQ.L', 'Quench_Protection.CLIQ.current_direction',
                                                  'Quench_Protection.Quench_Heaters.t_trigger',
                      'Quench_Protection.Quench_Heaters.U0', 'Quench_Protection.Quench_Heaters.C',
                      'Quench_Protection.Quench_Heaters.R_warm']

        # Make target folder if it is missing
        make_folder_if_not_existing(os.path.dirname(path))
        # Open the file in 'w' mode (write mode)
        with open(path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # Write the header row
            writer.writeheader()
            new_row = dict()
            for i, event in enumerate(self.list_events):
                new_row.clear()
                new_row['simulation_name'] = simulation_name  # TODO: is this the right entry?
                new_row['simulation_number'] = simulation_numbers[i]
                new_row['comments'] = 'TODO'  # TODO: where do I get it from?
                event_name = rgetattr(event, 'GeneralParameters.name')
                for step_name, step in self.dict_AnalysisStepDefinition.items():
                    if event_name in step_name:
                        new_row.update(zip(step.variables_to_change, step.variables_value))
                # check if there are columns in the csv for every variable to change
                missing_keys = [key for key in new_row.keys() if key not in fieldnames]
                if missing_keys:
                    raise ValueError(f"The following keys are missing from the list: {', '.join(missing_keys)}")
                writer.writerow(new_row)

    def set_up_viewer(self, path_viewer_csv: str, default_keys: Dict, simulation_numbers: List[int], simulation_name: str, software: str):
        '''
        Write a .csv file that can be used to run a STEAM Viewer analysis
        
        :param path_viewer_csv: 
        :param default_keys: 
        :param simulation_numbers: 
        :param simulation_name: 
        :param software: 
        :return: 
        '''
        # Unpack input dictionary with default key values
        path_config_file = default_keys['path_config_file']
        default_config = default_keys['default_config']
        if 'default_config_sim' in default_keys:
            default_config_sim = default_keys['default_config_sim']
        path_tdms_files = default_keys['path_tdms_files']
        test_campaign_name = default_keys['test_campaign_name']
        path_output_measurement_files = default_keys['path_output_measurement_files']
        path_output = default_keys['path_output']

        # Check if the measurement files exist, and either find the file names or set different configuration settings (without measurement data)
        list_default_config = []
        list_test_names = []
        for i, event in enumerate(self.list_events):
            event_name = event.GeneralParameters.name
            # Find all 10-digit sequences of integers in the string
            list_integer_sequences = re.findall(r'\d{10}', event_name)  # This will likely be a string defining the year, month, day, hour, and minute of the test

            # Look into the test campaign folder looking for a file containing the required string
            flag_file_found = False
            list_files = os.listdir(os.path.join(path_tdms_files, test_campaign_name))  # TODO allow to look into more than one subfolder by defining test_campaign_name as a list 
            for file in list_files:
                if file.endswith('.tdms') and (len(list_integer_sequences) > 0) and all([sequence in file for sequence in list_integer_sequences]):
                    flag_file_found = True
                    name_file_found = file.split('.tdms')[0]  # remove ".tdms" from the file name
            if flag_file_found:
                # If the measurement file exists, find the file name
                list_test_names.append(name_file_found)
                list_default_config.append(default_config)
            else:
                # If the measurement file does not exist, change the default configuration settings
                list_test_names.append('')
                list_default_config.append(default_config_sim)

        # Identify software-specific folder and file names 
        if software == 'LEDET':
            local_LEDET_folder = default_keys['local_LEDET_folder']
            # Identify simulation folder based on the software
            path_simulation_folder = f'{local_LEDET_folder}\{simulation_name}\Output\Mat Files'
            # Identify simulation file names based on the software
            list_simulation_names = []
            for sim in simulation_numbers:
                list_simulation_names.append(f'SimulationResults_LEDET_{sim}.mat')
        else:
            raise Exception(f'The required software ({software}) is not supported.')

        # If the parent folder is not present, make it
        make_folder_if_not_existing(os.path.dirname(path_viewer_csv))

        # Write .csv file
        f = open(path_viewer_csv, "w")
        # Write header
        f.write("Event label,Configuration file,Configuration,Measurement folder,Test campaign,Test name,flag_convert_meas_csv,path_output_measurement_files,Simulation folder,Simulation file,path_output_figures,path_output_simulation_files,Comments\n")
        # Write information for each event (one event in each row)
        for i, event in enumerate(self.list_events):
            f.write(
                f"{event.GeneralParameters.name},"
                f"{path_config_file},"
                f"{list_default_config[i]},"
                f"{path_tdms_files},"
                f"{test_campaign_name},"  #TODO consider getting this entry from the actual subfolder where the file was found
                f"{list_test_names[i]},"
                f"1,"  # hard-coded
                f"{path_output_measurement_files},"
                f"{path_simulation_folder},"
                f"{list_simulation_names[i]},"
                f"{path_output},"
                f"not_used,"  # hard-coded
                f"no comments"  # hard-coded
                f"\n")
        f.close()


    ### Helper functions ###
    def __set_analysis_general_parameters(self, model_name: str, simulation_numbers: List[int], simulation_name: str, software: List[str], event: DataEventMagnet, i: int):
        event_name = rgetattr(event, 'GeneralParameters.name')
        current_step = f'modify_general_parameters_{i+1}_{event_name}'
        self.dict_AnalysisStepDefinition[current_step] = ModifyModelMultipleVariables(type='ModifyModelMultipleVariables')
        self.dict_AnalysisStepDefinition[current_step].model_name = model_name
        self.dict_AnalysisStepDefinition[current_step].variables_to_change = []
        self.dict_AnalysisStepDefinition[current_step].variables_value = []
        self.dict_AnalysisStepDefinition[current_step].simulation_numbers = [simulation_numbers[i]]
        self.dict_AnalysisStepDefinition[current_step].simulation_name = simulation_name
        self.dict_AnalysisStepDefinition[current_step].software = software
        self.dict_AnalysisStepDefinition[current_step].new_model_name = []
        # populate steps in list of steps
        dict_param = {
            'GeneralParameters.initial_temperature': 'GeneralParameters.T_initial',
        }
        for param in dict_param:
            if rgetattr(event, param) and not math.isnan(rgetattr(event, param)):
                new_var_name = dict_param[param]
                if not math.isnan(rgetattr(event, param)):
                    new_var_value = rgetattr(event, param)
                else:
                    # get default values from reference model if entry is not a number
                    new_var_value = rgetattr(self.ref_model, f'model_data.{new_var_name}')
                self.dict_AnalysisStepDefinition[current_step].variables_to_change.append(new_var_name)
                self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_var_value])
        if len(self.dict_AnalysisStepDefinition[current_step].variables_to_change) > 0:
            self.list_AnalysisStepSequence.append(current_step)

    def __set_analysis_powering(self, model_name: str, event: DataEventMagnet, i: int, t_PC_off: float):
        if t_PC_off is None:
            raise Exception('no value for t_PC_off provided in ParsimEvent step definition')
        event_name = rgetattr(event, 'GeneralParameters.name')
        current_step = f'modify_powering_parameters_{i+1}_{event_name}'
        self.dict_AnalysisStepDefinition[current_step] = ModifyModelMultipleVariables(type='ModifyModelMultipleVariables')
        self.dict_AnalysisStepDefinition[current_step].model_name = model_name
        self.dict_AnalysisStepDefinition[current_step].variables_to_change = []
        self.dict_AnalysisStepDefinition[current_step].variables_value = []
        # populate steps in list of steps
        dict_param = {
            'Powering.PowerSupply.I_initial': 'Power_Supply.I_initial',
            # 'Powering.PowerSupply.t_off': 'Power_Supply.t_off',
            # 'Powering.PowerSupply.R_crowbar': 'Power_Supply.R_crowbar',
            # 'Powering.PowerSupply.Ud_crowbar': 'Power_Supply.Ud_crowbar',
        }
        for param in dict_param:
            if rgetattr(event, param) and not math.isnan(rgetattr(event, param)):  #TODO this won't work if rgetattr(event, param) has a value of 0!
                new_var_name = dict_param[param]
                if not math.isnan(rgetattr(event, param)):
                    new_var_value = rgetattr(event, param)
                else:
                    # get default values from reference model if entry is not a number
                    new_var_value = rgetattr(self.ref_model, f'model_data.{new_var_name}')
                self.dict_AnalysisStepDefinition[current_step].variables_to_change.append(new_var_name)
                self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_var_value])
        # Set power supply switch-off time
        self.dict_AnalysisStepDefinition[current_step].variables_to_change.append('Power_Supply.t_off')
        self.dict_AnalysisStepDefinition[current_step].variables_value.append([t_PC_off])
        # Calculate LUT for power supply
        if not math.isnan(rgetattr(event, 'Powering.PowerSupply.I_initial')):
            I_initial = rgetattr(event, 'Powering.PowerSupply.I_initial')
        else:
            raise Exception(f'Powering.PowerSupply.I_initial must be provided in the event {event_name}')
        if not math.isnan(rgetattr(event, 'Powering.max_dI_dt')):
            dI_dt = rgetattr(event, 'Powering.max_dI_dt')
            if self.verbose:
                print(f'Powering.max_dI_dt not provided and set to 0 A/s.')
        else:
            dI_dt = 0
        new_t_control_LUT = [t_PC_off-1, t_PC_off, t_PC_off+0.01]
        new_I_control_LUT = [I_initial-1*dI_dt, I_initial, 0]
        self.dict_AnalysisStepDefinition[current_step].variables_to_change.append('Power_Supply.t_control_LUT')
        self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_t_control_LUT])
        self.dict_AnalysisStepDefinition[current_step].variables_to_change.append('Power_Supply.I_control_LUT')
        self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_I_control_LUT])
        # add step if something is changed
        if len(self.dict_AnalysisStepDefinition[current_step].variables_to_change) > 0:
            self.list_AnalysisStepSequence.append(current_step)

    def __set_analysis_CLIQ(self, model_name: str, event: DataEventMagnet, i: int, current_polarities_CLIQ: List[int]):
        event_name = rgetattr(event, 'GeneralParameters.name')
        current_step = f'modify_CLIQ_parameters_{i + 1}_{event_name}'
        self.dict_AnalysisStepDefinition[current_step] = ModifyModelMultipleVariables(type='ModifyModelMultipleVariables')
        self.dict_AnalysisStepDefinition[current_step].model_name = model_name
        self.dict_AnalysisStepDefinition[current_step].variables_to_change = []
        self.dict_AnalysisStepDefinition[current_step].variables_value = []
        # populate steps in list of steps
        dict_param = {
            'QuenchProtection.CLIQ.t_trigger': 'Quench_Protection.CLIQ.t_trigger',
            'QuenchProtection.CLIQ.U0': 'Quench_Protection.CLIQ.U0',
            'QuenchProtection.CLIQ.C': 'Quench_Protection.CLIQ.C',
            'QuenchProtection.CLIQ.R': 'Quench_Protection.CLIQ.R',
            'QuenchProtection.CLIQ.L': 'Quench_Protection.CLIQ.L',
        }
        for param in dict_param:
            if rgetattr(event, param):
                new_var_name = dict_param[param]
                if not math.isnan(rgetattr(event, param)):
                    new_var_value = rgetattr(event, param)
                else:
                    # get default values from reference model if entry is not a number
                    new_var_value = rgetattr(self.ref_model, f'model_data.{new_var_name}')
                self.dict_AnalysisStepDefinition[current_step].variables_to_change.append(new_var_name)
                self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_var_value])
        # add current_polarities_CLIQ if provided
        if current_polarities_CLIQ:
            self.dict_AnalysisStepDefinition[current_step].variables_to_change.append('Quench_Protection.CLIQ.current_direction')
            self.dict_AnalysisStepDefinition[current_step].variables_value.append([current_polarities_CLIQ])
        # add step if something is changed
        if len(self.dict_AnalysisStepDefinition[current_step].variables_to_change) > 0:
            self.list_AnalysisStepSequence.append(current_step)

    def __set_analysis_QH(self, model_name: str, event: DataEventMagnet, i: int, list_QH_strips_to_units: List[List[int]]):
        if list_QH_strips_to_units is None:
            raise Exception('no values for list_QH_strips_to_units provided in ParsimEvent step definition')
        # unpack QH data from event data
        t_trigger_units = event.QuenchProtection.Quench_Heaters.t_trigger
        U0_units = event.QuenchProtection.Quench_Heaters.U0
        C_units = event.QuenchProtection.Quench_Heaters.C
        R_total_units = event.QuenchProtection.Quench_Heaters.R_total
        n_QH_units = len(U0_units)
        # check inputs
        if len(list_QH_strips_to_units) != n_QH_units:
            raise Exception(f'length of list_QH_strips_to_units should be {len(U0_units)}')  # TODO: what else should be checked?
        event_name = rgetattr(event, 'GeneralParameters.name')
        current_step = f'modify_QH_parameters_{i + 1}_{event_name}'
        self.dict_AnalysisStepDefinition[current_step] = ModifyModelMultipleVariables(type='ModifyModelMultipleVariables')
        self.dict_AnalysisStepDefinition[current_step].model_name = model_name
        self.dict_AnalysisStepDefinition[current_step].variables_to_change = []
        self.dict_AnalysisStepDefinition[current_step].variables_value = []
        # populate U0
        n_QH_strips = len(self.ref_model.model_data.Quench_Protection.Quench_Heaters.U0)
        new_list_t_trigger = [None for i in range(n_QH_strips)]
        new_list_U0 = [None for i in range(n_QH_strips)]
        new_list_C = [None for i in range(n_QH_strips)]
        new_list_R_warm = [None for i in range(n_QH_strips)]
        new_list_R_cold = self.__calculate_QH_R_cold()
        for i, list in enumerate(list_QH_strips_to_units):
            t_trigger = t_trigger_units[i]
            U0 = U0_units[i]
            C = C_units[i]
            R_total = R_total_units[i]
            n_strips_current_unit = len(list)
            for j in list:
                R_cold = new_list_R_cold[j-1]  # the resistance of the cold part of the QH strip is calculated for each strip from the reference BuilderModel
                new_list_t_trigger[j-1] = t_trigger
                new_list_U0[j-1] = U0 / n_strips_current_unit  # NOTE: assumption: the voltage is distributed equally across the strips
                new_list_C[j-1] = C * n_strips_current_unit  # NOTE: assumption: the voltage is distributed equally across the strips
                new_list_R_warm[j-1] = R_total/n_strips_current_unit - R_cold
        self.dict_AnalysisStepDefinition[current_step].variables_to_change.append('Quench_Protection.Quench_Heaters.t_trigger')
        self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_list_t_trigger])
        self.dict_AnalysisStepDefinition[current_step].variables_to_change.append('Quench_Protection.Quench_Heaters.U0')
        self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_list_U0])
        self.dict_AnalysisStepDefinition[current_step].variables_to_change.append('Quench_Protection.Quench_Heaters.C')
        self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_list_C])
        self.dict_AnalysisStepDefinition[current_step].variables_to_change.append('Quench_Protection.Quench_Heaters.R_warm')
        self.dict_AnalysisStepDefinition[current_step].variables_value.append([new_list_R_warm])
        # add step if something is changed
        if len(self.dict_AnalysisStepDefinition[current_step].variables_to_change) > 0:
            self.list_AnalysisStepSequence.append(current_step)

    def __calculate_QH_R_cold(self):  # TODO: put it in BuilderModel?
        f_SS = self.ref_model.model_data.Options_LEDET.physics.fScaling_RhoSS
        w_QH = self.ref_model.model_data.Quench_Protection.Quench_Heaters.w
        h_QH = self.ref_model.model_data.Quench_Protection.Quench_Heaters.h
        l_QH = self.ref_model.model_data.Quench_Protection.Quench_Heaters.l
        f_QH = self.ref_model.model_data.Quench_Protection.Quench_Heaters.f_cover
        rhoSS = 5.00E-07 * f_SS  # in [Ohm m]
        return [rhoSS / (w_QH[qh] * h_QH[qh]) * l_QH[qh] * f_QH[qh] for qh in range(len(w_QH))]

    def __set_general_parameters(self, event_info: pd.Series, new_event: DataEventMagnet):
        '''
        Function to set GeneralParameters keys

        :param event_info: Series of parameters
        :param new_event: DataEventMagnet object to update
        :return: new_event
        '''

        dict_params = {
            'File name': 'GeneralParameters.name', 'Test name': 'GeneralParameters.name',
            'Test Type': 'GeneralParameters.type',
            'Trigger Type': 'GeneralParameters.type_trigger',
            'Temperature [K]': 'GeneralParameters.initial_temperature',
        }

        for param in dict_params:
            if param in event_info:
                rsetattr(new_event, dict_params[param], event_info[param])

    def __set_powering(self, event_info: pd.Series, new_event: DataEventMagnet):
        '''
        Function to set Powering keys

        :param event_info: Series of parameters
        :param new_event: DataEventMagnet object to update
        :return:
        '''

        dict_params = {
            'Current [A]': 'Powering.PowerSupply.I_initial',
            'dI/dt (t < 0) [A/s]': 'Powering.max_dI_dt', 'dI/dt (t<0) [A/s]': 'Powering.max_dI_dt', 'dI/dt [A/s]': 'Powering.max_dI_dt',  # alternative spelling
            'dI/dt2 (t < 0) [A/s^2]': 'Powering.max_dI_dt2',
        }

        for param in dict_params:
            if param in event_info:
                rsetattr(new_event, dict_params[param], event_info[param])

    def __set_CLIQ(self, event_info: pd.Series, new_event: DataEventMagnet):
        '''
        Function to set CLIQ keys

        :param event_info: Series of parameters
        :param new_event: DataEventMagnet object to update
        :return:
        '''

        dict_params = {
            't CLIQ [s]': 'QuenchProtection.CLIQ.t_trigger',
            'U0 CLIQ [V]': 'QuenchProtection.CLIQ.U0',
            'C CLIQ [F]': 'QuenchProtection.CLIQ.C', 'CLIQ Capacitance [F]': 'QuenchProtection.CLIQ.C',  # alternative spelling
            'R CLIQ [Ohm]': 'QuenchProtection.CLIQ.R',
            'L CLIQ [H]': 'QuenchProtection.CLIQ.L',
        }

        for param in dict_params:
            if param in event_info:
                rsetattr(new_event, dict_params[param], event_info[param])
                
        # If these scalars are not set, try alternative reading method based on a list
        if not rgetattr(new_event, 'QuenchProtection.CLIQ.t_trigger'):
            # if pd.isna(event_info['CLIQ event Time [s]']):
            if 'CLIQ event Time [s]' in event_info:
                if event_info['CLIQ event Time [s]'] == event_info['CLIQ event Time [s]']:
                    # Take the first value of the selected column (hard-coded behavior)
                    rsetattr(new_event, 'QuenchProtection.CLIQ.t_trigger',
                             [float(num_as_str.strip(' ')) for num_as_str in event_info['CLIQ event Time [s]'].split(';')][0])
        if not rgetattr(new_event, 'QuenchProtection.CLIQ.U0'):
            if 'CLIQ event Value' in event_info:
                if event_info['CLIQ event Value'] == event_info['CLIQ event Value']:
                    # Take the first value of the selected column (hard-coded behavior)
                    rsetattr(new_event, 'QuenchProtection.CLIQ.U0',
                             [float(num_as_str.strip(' ')) for num_as_str in event_info['CLIQ event Value'].split(';')][0])

    def __set_QH(self, event_info: pd.Series, new_event: DataEventMagnet):
        '''
        Function to set QH keys

        :param event_info: Series of parameters
        :param new_event: DataEventMagnet object to update
        :return:
        '''

        dict_params = {
            'QH Start time [s]': 'QuenchProtection.Quench_Heaters.t_trigger',
            'QH Voltage [V]': 'QuenchProtection.Quench_Heaters.U0',
            'QH Capacitance [F]': 'QuenchProtection.Quench_Heaters.C',
            'QH Resistance [Ohm]': 'QuenchProtection.Quench_Heaters.R_total'
        }
        for param in dict_params:
            if param in event_info:
                if event_info[param] == event_info[param]:  # only save values when table entries are not empty
                    rsetattr(new_event, dict_params[param],
                             [float(num_as_str.strip(' ')) for num_as_str in event_info[param].split(';')])

