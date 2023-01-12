import csv
import sys
import ntpath
import os
import shutil
import importlib
import importlib.util
import pandas as pd
import pickle
from copy import deepcopy
from pathlib import Path
from typing import Union

from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.builders.BuilderModel import BuilderModel
from steam_sdk.data.DataAnalysis import DataAnalysis, ModifyModel
from steam_sdk.drivers.DriverFiQuS import DriverFiQuS
from steam_sdk.drivers.DriverLEDET import DriverLEDET
from steam_sdk.drivers.DriverPSPICE import DriverPSPICE
from steam_sdk.drivers.DriverPyBBQ import DriverPyBBQ
from steam_sdk.drivers.DriverXYCE import DriverXYCE
from steam_sdk.parsers.ParserYAML import dict_to_yaml, yaml_to_data
from steam_sdk.parsims.ParsimEventMagnet import ParsimEventMagnet
from steam_sdk.parsims.ParsimSweep import ParsimSweep
from steam_sdk.postprocs.PostprocsMetrics import PostprocsMetrics
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.rgetattr import rgetattr
from steam_sdk.utils.sgetattr import rsetattr
from steam_sdk.utils.rhasattr import rhasattr
from steam_sdk.viewers.Viewer import Viewer
from steam_sdk.parsers.ParserPSPICE import writeStimuliFromInterpolation, writeStimuliFromInterpolation_general


class AnalysisSTEAM:
    """
        Class to run analysis based on STEAM_SDK
    """

    def __init__(self,
                 file_name_analysis: str = None,
                 file_path_list_models: str = '',
                 relative_path_settings: str = '',
                 verbose: bool = False):
        """
        Analysis based on STEAM_SDK
        :param file_name_analysis: full path to analysis.yaml input file  # object containing the information read from the analysis input file
        :param relative_path_settings: relative path to settings.xxx.yaml file
        :param verbose: if true, more information is printed to the console
        """

        # Initialize
        self.settings = DataSettings()  # object containing the settings acquired during initialization
        self.library_path = None
        self.output_path = None
        self.temp_path = None
        if file_path_list_models:
            with open(file_path_list_models, 'rb') as input_dict:
                self.list_models = pickle.load(input_dict)
        else:
            self.list_models = {}  # this dictionary will be populated with BuilderModel objects and their names

        self.list_sims = []  # this list will be populated with integers indicating simulations to run
        self.list_viewers = {}  # this dictionary will be populated with Viewer objects and their names
        self.list_metrics = {}  # this dictionary will be populated with calculated metrics
        self.verbose = verbose
        self.summary = None  # float representing the overall outcome of a simulation for parsims

        if file_name_analysis:
            self.data_analysis = yaml_to_data(file_name_analysis, DataAnalysis)  # Load yaml keys into DataAnalysis dataclass
            # Read working folders and set them up
            self._set_up_working_folders()
            # Read analysis settings
            self._load_and_write_settings(relative_path_settings)
        else:
            self.data_analysis = DataAnalysis()
            if verbose: print('Empty AnalysisSTEAM() object generated.')


    def setAttribute(self, dataclassSTEAM, attribute: str, value):
        try:
            setattr(dataclassSTEAM, attribute, value)
        except:
            setattr(getattr(self, dataclassSTEAM), attribute, value)

    def getAttribute(self, dataclassSTEAM, attribute):
        try:
            return getattr(dataclassSTEAM, attribute)
        except:
            return getattr(getattr(self, dataclassSTEAM), attribute)

    def _set_up_working_folders(self):
        """
            ** Read working folders and set them up **
            This method performs the following tasks:
             - Check all folder paths are defined. If not, raise an exception.
             - Check if model library folder is present. If not, raise an exception.
             - Check if output folder is present. If not, make it.
             - Check if temporary folder is present. If so, delete it.
        """

        # Raise exceptions if folders are not defined.
        if not self.data_analysis.WorkingFolders.library_path:
            raise Exception('Model library path must be defined. Key to provide: WorkingFolders.library_path')
        if not self.data_analysis.WorkingFolders.output_path:
            raise Exception('Output folder path must be defined. Key to provide: WorkingFolders.output_path')
        if not self.data_analysis.WorkingFolders.temp_path:
            raise Exception('Temporary folder path must be defined. Key to provide: WorkingFolders.temp_path')

        # Resolve all paths and re-assign them to the self variables

        self.library_path = Path(self.data_analysis.WorkingFolders.library_path).resolve()
        self.output_path = Path(self.data_analysis.WorkingFolders.output_path).resolve()
        self.temp_path = Path(self.data_analysis.WorkingFolders.temp_path).resolve()

        if self.verbose:
            print('Model library path:    {}'.format(self.library_path))
            print('Output folder path:    {}'.format(self.output_path))
            print('Temporary folder path: {}'.format(self.temp_path))

        # Check if model library folder is present. If not, raise an exception.
        if not os.path.isdir(self.library_path):
            raise Exception(f'Model library path refers to a not-existing folder: {self.library_path}. Key to change: WorkingFolders.library_path')

        # Check if output folder is present. If not, make it.
        make_folder_if_not_existing(self.output_path, verbose=self.verbose)

        # Check if temporary folder is present. If so, delete it.
        if os.path.isdir(self.temp_path):
            shutil.rmtree(self.temp_path)
            if self.verbose: print('Folder {} already existed. It was removed.'.format(self.temp_path))

    def _load_and_write_settings(self, relative_path_settings: str):
        """
            ** Read analysis settings **
            They will be read either form a local settings file (if flag_permanent_settings=False)
            or from the keys in the input analysis file (if flag_permanent_settings=True)
            :param relative_path_settings: only used if flag_permanent_settings=False and allows to specify folder containing settings.user_name.yaml
            :rtype: nothing, saves temporary settings.user_name.yaml on disk
        """

        verbose = self.verbose
        user_name = os.getlogin()
        settings_file = f"settings.{user_name}.yaml"

        if self.data_analysis.GeneralParameters.flag_permanent_settings:
            # Read settings from analysis input file (yaml file)
            if verbose:
                print('flag_permanent_settings is set to True')
            settings_dict = self.data_analysis.PermanentSettings.__dict__
        else:
            # Read settings from local settings file (yaml file)
            full_path_file_settings = os.path.join(Path(relative_path_settings).resolve(), settings_file)
            if verbose:
                print('flag_permanent_settings is set to False')
                print('user_name:               {}'.format(user_name))
                print('relative_path_settings:  {}'.format(relative_path_settings))
                print('full_path_file_settings: {}'.format(full_path_file_settings))
            if not os.path.isfile(full_path_file_settings):
                raise Exception('Local setting file {} not found. This file must be provided when flag_permanent_settings is set to False.'.format(full_path_file_settings))
            settings_dict = yaml_to_data(full_path_file_settings)

        # Assign the keys read either from permanent-settings or local-settings
        for name, _ in self.settings.__dict__.items():
            if name in settings_dict:
                value = settings_dict[name]
                self.setAttribute(self.settings, name, value)
                if verbose: print('{} : {}. Added.'.format(name, value))
            else:
                if verbose: print('{}: not found in the settings. Skipped.'.format(name))

        # Dump read keys to temporary settings file locally
        path_temp_file_settings = Path(os.path.join('', settings_file)).resolve()
        dict_to_yaml(settings_dict, path_temp_file_settings)
        if verbose: print('File {} was saved locally.'.format(path_temp_file_settings))

    def store_model_objects(self, path_output_file: str):
        """
        ** Stores the dictionary of BuilderModel objects in a pickle file at the specified path **
        This can be helpful to load the list of models instead of generating it at every iteration of a co-simulation.
        :param path_output_file: string to the file to write
        :return: None
        """
        # Make sure the target folder exists
        make_folder_if_not_existing(os.path.dirname(path_output_file), verbose=self.verbose)

        # Store the objects as pickle file
        with open(path_output_file, 'wb') as output:
            pickle.dump(self.list_models, output, pickle.HIGHEST_PROTOCOL)

        if self.verbose: print(f'File {path_output_file} saved.')

    def write_analysis_file(self, path_output_file: str):
        """
        ** Write the analysis data in the target file **
        This can be helpful to keep track of the final state of the DataAnalysis object before running it, especially if it was modified programmatically.
        :param path_output_file: string to the file to write
        :return: None
        """

        # Make sure the target folder exists
        make_folder_if_not_existing(os.path.dirname(path_output_file), verbose=self.verbose)

        # Write the STEAM analysis data to a yaml file
        dict_to_yaml({**self.data_analysis.dict()}, path_output_file, list_exceptions=['AnalysisStepSequence', 'variables_to_change'])
        if self.verbose: print(f'File {path_output_file} saved.')

    def run_analysis(self, verbose: bool = None):
        """
            ** Run the analysis **
        """

        # Unpack and assign default values
        step_definitions = self.data_analysis.AnalysisStepDefinition
        if not verbose:
            verbose = self.verbose

        # Print the selected analysis steps
        if verbose:
            print('Defined analysis steps (not in sequential order):')
            for def_step in step_definitions:
                print(f'{def_step}')

        # Print analysis sequence
        if verbose: print('Defined sequence of analysis steps:')
        for s, seq_step in enumerate(self.data_analysis.AnalysisStepSequence):
            if verbose: print('Step {}/{}: {}'.format(s + 1, len(self.data_analysis.AnalysisStepSequence), seq_step))

        # Run analysis (and re-print analysis steps)
        if verbose: print('Analysis started.')
        for s, seq_step in enumerate(self.data_analysis.AnalysisStepSequence):
            if verbose: print('Step {}/{}: {}'.format(s + 1, len(self.data_analysis.AnalysisStepSequence), seq_step))
            step = step_definitions[seq_step]  # this is the object containing the information about the current step
            if step.type == 'MakeModel':
                self.step_make_model(step, verbose=verbose)
            elif step.type == 'ModifyModel':
                self.step_modify_model(step, verbose=verbose)
            elif step.type == 'ModifyModelMultipleVariables':
                self.step_modify_model_multiple_variables(step, verbose=verbose)
            elif step.type == 'RunSimulation':
                self.step_run_simulation(step, verbose=verbose)
            elif step.type == 'PostProcess':
                self.step_postprocess(step, verbose=verbose)
            elif step.type == 'SetUpFolder':
                self.step_setup_folder(step, verbose=verbose)
            elif step.type == 'AddAuxiliaryFile':
                self.add_auxiliary_file(step, verbose=verbose)
            elif step.type == 'CopyFile':
                self.copy_file_to_target(step, verbose=verbose)
            elif step.type == 'RunCustomPyFunction':
                self.run_custom_py_function(step, verbose=verbose)
            elif step.type == 'RunViewer':
                self.run_viewer(step, verbose=verbose)
            elif step.type == 'CalculateMetrics':
                self.calculate_metrics(step, verbose=verbose)
            elif step.type == 'LoadCircuitParameters':
                self.load_circuit_parameters(step, verbose=verbose)
            elif step.type == 'WriteStimulusFile':
                self.write_stimuli_from_interpolation(step, verbose=verbose)
            elif step.type == 'ParsimEvent':
                self.run_parsim_event(step, verbose=verbose)
            elif step.type == 'ParametricSweep':
                self.run_parsim_sweep(step, verbose=verbose)
            else:
                raise Exception('Unknown type of analysis step: {}'.format(step.type))

    def step_make_model(self, step, verbose: bool = False):
        if verbose:
            print('Making model object named {}'.format(str(step.model_name)))
        ## Assuming the steam-models directory structure if 'steam-models' or model_library found at the end of library path.
        # Else assuming library path directs straight to the model
        if (str(self.library_path).endswith('steam_models')) or (str(self.library_path).endswith('steam-models')) or (str(self.library_path).endswith('model_library')):
            file_model_data = os.path.join(self.library_path, step.case_model + 's', step.file_model_data, 'input', 'modelData_' + step.file_model_data + '.yaml')
        else:
            file_model_data = os.path.join(self.library_path, 'modelData_' + step.file_model_data + '.yaml')

        case_model = step.case_model
        software = step.software  # remember this is a list, not a string
        verbose_of_step = step.verbose
        flag_build = step.flag_build
        flag_dump_all = step.flag_dump_all
        flag_plot_all = step.flag_plot_all
        flag_json = step.flag_json
        output_folder = self.output_path
        relative_path_settings = ''

        # Build the model
        BM = BuilderModel(file_model_data=file_model_data, case_model=case_model, software=software,
                          verbose=verbose_of_step, flag_build=flag_build, flag_dump_all=flag_dump_all,
                          flag_plot_all=flag_plot_all, flag_json=flag_json, output_path=output_folder,
                          relative_path_settings=relative_path_settings)

        # Build simulation file
        if step.simulation_number:
            if 'FiQuS' in step.software:
                self.setup_sim_FiQuS(simulation_name=step.simulation_name, sim_number=step.simulation_number, magnet_type=BM.model_data.GeneralParameters.magnet_type)
                # note above magnet_type is specified only for the step_make_model to make setup_sim_FiQuS copy additional files needed for the multipole magnet
            if 'LEDET' in step.software:
                flag_yaml = True  # Hard-coded for the moment
                self.setup_sim_LEDET(simulation_name=step.simulation_name, sim_number=step.simulation_number, flag_yaml=flag_yaml, flag_json=flag_json)
            if 'PyBBQ' in step.software:
                self.setup_sim_PyBBQ(simulation_name=step.simulation_name, sim_number=step.simulation_number)
            if 'PSPICE' in step.software:
                self.setup_sim_PSPICE(simulation_name=step.simulation_name, sim_number=step.simulation_number)
            if 'XYCE' in step.software:
                self.setup_sim_XYCE(simulation_name=step.simulation_name, sim_number=step.simulation_number)

        # Add the reference to the model in the dictionary
        self.list_models[step.model_name] = BM

    def step_modify_model(self, step, verbose: bool = False):
        if verbose:
            print('Modifying model object named {}'.format(str(step.model_name)))

        # Check inputs
        if step.model_name not in self.list_models:
            raise Exception('Name of the model to modify ({}) does not correspond to any of the defined models.'.format(step.model_name))
        len_variable_value = len(step.variable_value)
        len_simulation_numbers = len(step.simulation_numbers)
        len_new_model_name = len(step.new_model_name)
        if len_new_model_name > 0 and not len_new_model_name == len_variable_value:
            raise Exception('The length of new_model_name and variable_value must be the same, but they are {} and {} instead.'.format(len_new_model_name, len_variable_value))
        if len_simulation_numbers > 0 and not len_simulation_numbers == len_variable_value:
            raise Exception('The length of simulation_numbers and variable_value must be the same, but they are {} and {} instead.'.format(len_simulation_numbers, len_variable_value))

        # Change the value of the selected variable
        for v, value in enumerate(step.variable_value):
            BM = self.list_models[step.model_name]  # original BuilderModel object
            case_model = BM.case_model  # model case (magnet, conductor, circuit)

            if 'Conductors[' in step.variable_to_change:  # Special case when the variable to change is the Conductors key
                if verbose:
                    idx_conductor = int(step.variable_to_change.split('Conductors[')[1].split(']')[0])
                    conductor_variable_to_change = step.variable_to_change.split('].')[1]
                    print('Variable {} is treated as a Conductors key. Conductor index: #{}. Conductor variable to change: {}.'.format(step.variable_to_change, idx_conductor, conductor_variable_to_change))

                    old_value = self.get_attribute_model(case_model, BM, conductor_variable_to_change, idx_conductor)
                    print('Variable {} changed from {} to {}.'.format(conductor_variable_to_change, old_value, value))

                if len_new_model_name > 0:  # Make a new copy of the BuilderModel object, and change it
                    self.list_models[step.new_model_name[v]] = deepcopy(BM)
                    BM = self.list_models[step.new_model_name[v]]

                    if case_model == 'conductor':
                        rsetattr(BM.conductor_data.Conductors[idx_conductor], conductor_variable_to_change, value)
                    else:
                        rsetattr(BM.model_data.Conductors[idx_conductor], conductor_variable_to_change, value)

                    if verbose:
                        print('Model {} copied to model {}.'.format(step.model_name, step.new_model_name[v]))
                else:  # Change the original BuilderModel object

                    if case_model == 'conductor':
                        rsetattr(BM.conductor_data.Conductors[idx_conductor], conductor_variable_to_change, value)
                    else:
                        rsetattr(BM.model_data.Conductors[idx_conductor], conductor_variable_to_change, value)

            else:  # Standard case when the variable to change is not the Conductors key
                if verbose:
                    old_value = self.get_attribute_model(case_model, BM, step.variable_to_change)
                    print('Variable {} changed from {} to {}.'.format(step.variable_to_change, old_value, value))

                if len_new_model_name > 0:  # Make a new copy of the BuilderModel object, and change it
                    self.list_models[step.new_model_name[v]] = deepcopy(BM)
                    BM = self.list_models[step.new_model_name[v]]
                    self.set_attribute_model(case_model, BM, step.variable_to_change, value)
                    if verbose:
                        print('Model {} copied to model {}.'.format(step.model_name, step.new_model_name[v]))

                else:  # Change the original BuilderModel object
                    self.set_attribute_model(case_model, BM, step.variable_to_change, value)

            # Special case: If the sub-keys of "Source" are changed, a resetting of the input paths is triggered
            if step.variable_to_change.startswith('Sources.'):
                BM.set_input_paths()

            # Build simulation file
            if len_simulation_numbers > 0:
                simulation_number = step.simulation_numbers[v]
                if 'FiQuS' in step.software:
                    BM.buildFiQuS(simulation_name=f'{step.simulation_name}')
                    self.setup_sim_FiQuS(simulation_name=step.simulation_name, sim_number=simulation_number,
                                         magnet_type=BM.model_data.GeneralParameters.magnet_type if not step.variable_to_change.startswith('Options_FiQuS.') else None)
                if 'LEDET' in step.software:
                    flag_json = BM.flag_json
                    flag_yaml = True  # Hard-coded for the moment
                    BM.buildLEDET()
                    self.setup_sim_LEDET(simulation_name=step.simulation_name, sim_number=simulation_number, flag_yaml=flag_yaml, flag_json=flag_json)
                if 'PyBBQ' in step.software:
                    BM.buildPyBBQ()
                    self.setup_sim_PyBBQ(simulation_name=step.simulation_name, sim_number=simulation_number)
                if 'PSPICE' in step.software:
                    BM.buildPSPICE()
                    self.setup_sim_PSPICE(simulation_name=step.simulation_name, sim_number=simulation_number)
                if 'XYCE' in step.software:
                    BM.buildXYCE()
                    self.setup_sim_XYCE(simulation_name=step.simulation_name, sim_number=simulation_number)

    def get_attribute_model(self, case_model: str, builder_model: BuilderModel, name_variable: str, idx_conductor: int = None):
        """
        Helper function used to get an attribute from a key of the model data.
        Depending on the model type (circuit, magnet, conductor), the data structure to access is different.
        Also, there is a special case when the variable to read is a sub-key of the Conductors key. In such a case, an additional parameter idx_conductor must be defined (see below).
        :param case_model: Model type
        :param builder_model: BuilderModel object to access
        :param name_variable: Name of the variable to read
        :param idx_conductor: When defined, a sub-key form the Conductors key is read. The index of the conductor to read is defined by idx_conductor
        :return: Value of the variable to get
        """

        if case_model == 'magnet':
            if idx_conductor is None:  # Standard case when the variable to change is not the Conductors key
                value = rgetattr(builder_model.model_data, name_variable)
            else:
                value = rgetattr(builder_model.model_data.Conductors[idx_conductor], name_variable)
        elif case_model == 'conductor':
            if idx_conductor is None:  # Standard case when the variable to change is not the Conductors key
                value = rgetattr(builder_model.conductor_data, name_variable)
            else:
                value = rgetattr(builder_model.conductor_data.Conductors[idx_conductor], name_variable)
        elif case_model == 'circuit':
            value = rgetattr(builder_model.circuit_data, name_variable)
        else:
            raise Exception(f'Model type not supported: case_model={case_model}')
        return value

    def set_attribute_model(self, case_model: str, builder_model: BuilderModel, name_variable: str, value_variable: Union[int, float, str], idx_conductor: int = None):
        """
        Helper function used to set a key of the model data to a certain value.
        Depending on the model type (circuit, magnet, conductor), the data structure to access is different.
        Also, there is a special case when the variable to change is a sub-key of the Conductors key. In such a case, an additional parameter idx_conductor must be defined (see below).
        :param case_model: Model type
        :param builder_model: BuilderModel object to access
        :param name_variable: Name of the variable to change
        :param value_variable: New value of the variable of the variable
        :param idx_conductor: When defined, a sub-key form the Conductors key is read. The index of the conductor to read is defined by idx_conductor
        :return: Value of the variable to get
        """

        if case_model == 'magnet':
            if idx_conductor is None:  # Standard case when the variable to change is not the Conductors key
                rsetattr(builder_model.model_data, name_variable, value_variable)
            else:
                rsetattr(builder_model.model_data.Conductors[idx_conductor], name_variable, value_variable)
        elif case_model == 'conductor':
            if idx_conductor is None:  # Standard case when the variable to change is not the Conductors key
                rsetattr(builder_model.conductor_data, name_variable, value_variable)
            else:
                rsetattr(builder_model.conductor_data.Conductors[idx_conductor], name_variable, value_variable)
        elif case_model == 'circuit':
            rsetattr(builder_model.circuit_data, name_variable, value_variable)
        else:
            raise Exception(f'Model type not supported: case_model={case_model}')

    def step_modify_model_multiple_variables(self, step, verbose: bool = False):
        if verbose:
            print('Modifying model object named {}'.format(str(step.model_name)))

        # Check inputs
        if step.model_name not in self.list_models:
            raise Exception(f'Name of the model to modify ({step.model_name}) does not correspond to any of the defined models.'.format(step.model_name))
        len_variables_to_change = len(step.variables_to_change)
        len_variables_value = len(step.variables_value)
        if not len_variables_to_change == len_variables_value:
            raise Exception('The length of variables_to_change and variables_value must be the same, but they are {} and {} instead.'.format(len_variables_to_change, len_variables_value))

        # Loop through the list of variables to change
        for v, variable_to_change in enumerate(step.variables_to_change):
            # For each variable to change, make an instance of an ModifyModel step and call the step_modify_model() method
            next_step = ModifyModel(type='ModifyModel')
            next_step.model_name = step.model_name
            next_step.variable_to_change = variable_to_change
            next_step.variable_value = step.variables_value[v]
            if v + 1 == len_variables_to_change:  # If this is the last variable to change, import new_model_name and simulation_numbers from the step
                next_step.new_model_name = step.new_model_name
                next_step.simulation_numbers = step.simulation_numbers
            else:  # else, set new_model_name and simulation_numbers to empty lists to avoid making models/simulations for intermediate changes
                next_step.new_model_name = []
                next_step.simulation_numbers = []
            next_step.simulation_name = step.simulation_name
            next_step.software = step.software
            self.step_modify_model(next_step, verbose=verbose)
        if verbose:
            print('All variables of step {} were changed.'.format(step))

    def step_run_simulation(self, step, verbose: bool = False):
        software = step.software
        simulation_name = step.simulation_name
        simFileType = step.simFileType
        for sim_number in step.simulation_numbers:
            if verbose:
                print('Running simulation of model {} #{} using {}.'.format(simulation_name, sim_number, software))
            # Run simulation
            self.run_sim(software, simulation_name, sim_number, simFileType, verbose)

    def step_postprocess(self, step, verbose: bool = False):
        if verbose: print('postprocessing')
        print('Not implemented yet.')
        pass

    def step_setup_folder(self, step, verbose: bool = False):
        """
        Set up simulation working folder.
        The function applies a different logic for each simulation software.
        """
        list_software = step.software
        simulation_name = step.simulation_name

        for software in list_software:
            if verbose:
                print('Set up folder of model {} for {}.'.format(simulation_name, software))


            if 'FiQuS' in software:
                # make top level output folder
                make_folder_if_not_existing(self.settings.local_FiQuS_folder, verbose=verbose)

                # make simulation name folder inside top level folder
                make_folder_if_not_existing(os.path.join(self.settings.local_FiQuS_folder, step.simulation_name))

            elif 'LEDET' in software:
                local_LEDET_folder = Path(self.settings.local_LEDET_folder)
                # Make magnet input folder and its subfolders
                make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input').resolve(), verbose=verbose)
                make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'Control current input').resolve(), verbose=verbose)
                make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'Initialize variables').resolve(), verbose=verbose)
                make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'InitializationFiles').resolve(), verbose=verbose)

                # Copy csv files from the output folder
                list_csv_files = [entry for entry in os.listdir(self.output_path) if (simulation_name in entry) and ('.csv' in entry)]
                for csv_file in list_csv_files:
                    file_to_copy = os.path.join(self.output_path, csv_file)
                    file_copied = os.path.join(Path(local_LEDET_folder / simulation_name / 'Input').resolve(), csv_file)
                    shutil.copyfile(file_to_copy, file_copied)
                    if verbose: print('Csv file {} copied to {}.'.format(file_to_copy, file_copied))

                # Make magnet field-map folder
                field_maps_folder = Path(local_LEDET_folder / '..' / 'Field maps' / simulation_name).resolve()
                make_folder_if_not_existing(field_maps_folder, verbose=verbose)

                # Copy field-map files from the output folder
                list_field_maps = [entry for entry in os.listdir(self.output_path) if (simulation_name in entry) and ('.map2d' in entry)]
                for field_map in list_field_maps:
                    file_to_copy = os.path.join(self.output_path, field_map)
                    file_copied = os.path.join(field_maps_folder, field_map)
                    shutil.copyfile(file_to_copy, file_copied)
                    if verbose: ('Field map file {} copied to {}.'.format(file_to_copy, file_copied))

            elif 'PSPICE' in software:
                local_PSPICE_folder = Path(self.settings.local_PSPICE_folder)
                local_model_folder = Path(local_PSPICE_folder / simulation_name).resolve()
                # Make magnet input folder
                make_folder_if_not_existing(local_model_folder, verbose=verbose)

                # Copy lib files from the output folder
                list_lib_files = [entry for entry in os.listdir(self.output_path) if (simulation_name in entry) and ('.lib' in entry)]
                for lib_file in list_lib_files:
                    file_to_copy = os.path.join(self.output_path, lib_file)
                    file_copied = os.path.join(local_model_folder, lib_file)
                    shutil.copyfile(file_to_copy, file_copied)
                    if verbose: print('Lib file {} copied to {}.'.format(file_to_copy, file_copied))

                # Copy stl files from the output folder
                list_stl_files = [entry for entry in os.listdir(self.output_path) if (simulation_name in entry) and ('.stl' in entry)]
                for stl_file in list_stl_files:
                    file_to_copy = os.path.join(self.output_path, stl_file)
                    file_copied = os.path.join(local_model_folder, stl_file)
                    shutil.copyfile(file_to_copy, file_copied)
                    if verbose: print('Stl file {} copied to {}.'.format(file_to_copy, file_copied))

            elif 'XYCE' in software:
                local_XYCE_folder = Path(self.settings.local_XYCE_folder)
                local_model_folder = str(Path(local_XYCE_folder / simulation_name).resolve())
                # Make circuit input folder
                make_folder_if_not_existing(local_model_folder, verbose=verbose)

                # Copy lib files from the output folder
                list_lib_files = [entry for entry in os.listdir(self.output_path) if
                                  (simulation_name in entry) and ('.lib' in entry)]
                for lib_file in list_lib_files:
                    file_to_copy = os.path.join(self.output_path, lib_file)
                    file_copied = os.path.join(local_model_folder, lib_file)
                    shutil.copyfile(file_to_copy, file_copied)
                    if verbose: print('Lib file {} copied to {}.'.format(file_to_copy, file_copied))

                # Copy stl files from the output folder
                stl_path = os.path.join(self.output_path, 'Stimulus')
                list_stl_files = [entry for entry in os.listdir(stl_path) if
                                  (simulation_name in entry) and ('.csv' in entry)]
                stl_path_new = os.path.join(local_model_folder, 'Stimulus')
                if os.path.exists(stl_path_new):
                    shutil.rmtree(stl_path_new)
                os.mkdir(stl_path_new)

                for stl_file in list_stl_files:
                    file_to_copy = os.path.join(self.output_path, stl_file)
                    file_copied = os.path.join(stl_path_new, stl_file)
                    shutil.copyfile(file_to_copy, file_copied)
                    if verbose: print('Stl file {} copied to {}.'.format(file_to_copy, file_copied))

            else:
                raise Exception(f'Software {software} not supported for automated folder setup.')

    def add_auxiliary_file(self, step, verbose: bool = False):
        """
        Copy the desired auxiliary file to the output folder
        """
        # Unpack
        full_path_aux_file = Path(step.full_path_aux_file).resolve()
        new_file_name = step.new_file_name
        output_path = self.output_path

        # If no new name is provided, use the old file name
        if new_file_name == None:
            new_file_name = ntpath.basename(full_path_aux_file)

        # Copy auxiliary file to the output folder
        full_path_output_file = os.path.join(output_path, new_file_name)
        shutil.copyfile(full_path_aux_file, full_path_output_file)
        if verbose: print(f'File {full_path_aux_file} was copied to {full_path_output_file}.')

        # Build simulation file
        len_simulation_numbers = len(step.simulation_numbers)
        if len_simulation_numbers > 0:
            for simulation_number in step.simulation_numbers:
                if 'FiQuS' in step.software:
                    self.setup_sim_FiQuS(simulation_name=step.simulation_name, sim_number=simulation_number)
                if 'LEDET' in step.software:
                    flag_yaml = True  # Hard-coded for the moment
                    flag_json = False  # Hard-coded for the moment
                    self.setup_sim_LEDET(simulation_name=step.simulation_name, sim_number=simulation_number, flag_yaml=flag_yaml, flag_json=flag_json)
                if 'PyBBQ' in step.software:
                    self.setup_sim_PyBBQ(simulation_name=step.simulation_name, sim_number=simulation_number)
                if 'PSPICE' in step.software:
                    self.setup_sim_PSPICE(simulation_name=step.simulation_name, sim_number=simulation_number)
                if 'PSPICE' in step.software:
                    self.setup_sim_XYCE(simulation_name=step.simulation_name, sim_number=simulation_number)

    def copy_file_to_target(self, step, verbose: bool = False):
        """
            Copy one file from a location to another (the destination folder can be different from the analysis output folder)
        """
        # Unpack
        full_path_file_to_copy = Path(step.full_path_file_to_copy).resolve()
        full_path_file_target = Path(step.full_path_file_target).resolve()

        # Make sure the target folder exists
        make_folder_if_not_existing(os.path.dirname(full_path_file_target), verbose=verbose)

        # Copy file
        shutil.copyfile(full_path_file_to_copy, full_path_file_target)
        if verbose: print(f'File {full_path_file_to_copy} was copied to {full_path_file_target}.')

    def run_custom_py_function(self, step, verbose: bool = False):
        """
            Run a custom Python function with given arguments
        """
        # If the step is not enabled, the function will not be run
        if not step.flag_enable:
            if verbose: print(f'flag_enable set to False. Custom function {step.function_name} will not be run.')
            return

        # Unpack variables
        function_name = step.function_name
        function_arguments = step.function_arguments
        if step.path_module:
            # Import the custom function from a specified location different from the default location
            # This Python magic comes from: https://stackoverflow.com/questions/67631/how-do-i-import-a-module-given-the-full-path
            path_module = os.path.join(Path(step.path_module).resolve())
            custom_module = importlib.util.spec_from_file_location('custom_module', os.path.join(path_module, function_name + '.py'))
            custom_function_to_load = importlib.util.module_from_spec(custom_module)
            sys.modules['custom_module'] = custom_function_to_load
            custom_module.loader.exec_module(custom_function_to_load)
            custom_function = getattr(custom_function_to_load, function_name)
        else:
            # Import the custom function from the default location
            path_module = f'steam_sdk.analyses.custom_analyses.{function_name}.{function_name}'
            custom_module = importlib.import_module(path_module)
            custom_function = getattr(custom_module, function_name)

        # Run custom function with the given argument
        if verbose: print(f'Custom function {function_name} from module {path_module} will be run with arguments: {function_arguments}.')
        output = custom_function(function_arguments)
        return output

    def run_viewer(self, step, verbose: bool = False):
        """
            Make a steam_sdk.viewers.Viewer.Viewer() object and run its analysis
        """

        # Unpack variables
        viewer_name = step.viewer_name

        if verbose: print(f'Making Viewer object named {viewer_name}.')

        # Make a steam_sdk.viewers.Viewer.Viewer() object and run its analysis
        V = Viewer(file_name_transients=step.file_name_transients,
                   list_events=step.list_events,
                   flag_analyze=step.flag_analyze,
                   flag_display=step.flag_display,
                   flag_save_figures=step.flag_save_figures,
                   path_output_html_report=step.path_output_html_report,
                   figure_types=step.figure_types,
                   verbose=step.verbose)

        # Add the reference to the Viewer object in the dictionary
        self.list_viewers[viewer_name] = V

    def calculate_metrics(self, step, verbose: bool = False):
        """
        Calculate metrics (usually to compare two or more measured and/or simulated signals)
        :param step: STEAM analysis step of type CalculateMetrics, which has attributes:
        - viewer_name: the name of the Viewer object containing the data to analyze
        - metrics_to_calculate: list that defines the type of calculation to perform for each metric.
        - variables_to_analyze: list
        :param verbose:
        :return:
        """
        """
            
            The metrics to calculate are indicated in the list metrics_to_calculate, which defines the type of calculation of each metric.

        """
        if verbose: print(f'Calculate metrics.')

        # Unpack variables
        viewer_name = step.viewer_name
        metrics_name = step.metrics_name
        metrics_to_calculate = step.metrics_to_calculate
        variables_to_analyze = step.variables_to_analyze
        # Note: Avoid unpacking "list_viewers = self.list_viewers" since the variable usually has large size

        # Check input
        if not viewer_name in self.list_viewers:
            raise Exception(f'The selected Viewer object named {viewer_name} is not present in the current Viewer list: {self.list_viewers}. Add an analysis step of type RunViewer to define a Viewer object.')
        # if len(metrics_to_calculate) != len(variables_to_analyze):
        #     raise Exception(f'The lengths of the lists metrics_to_calculate and variables_to_analyze must match, but are {len(metrics_to_calculate)} and {len(variables_to_analyze)} instead.')

        # If the Analysis object contains a metrics set with the selected metrics_name, retrieve it: the new metrics entries will be appended to it
        if metrics_name in self.list_metrics:
            current_list_output_metrics = self.list_metrics[metrics_name]
        else:
            # If not, make a new metrics set
            current_list_output_metrics = {}

        # Loop through all events listed in the selected Viewer object
        for event_id in self.list_viewers[viewer_name].list_events:
            event_label = self.list_viewers[viewer_name].dict_events['Event label'][event_id - 1]
            if verbose: print(f'Event #{event_id}: "{event_label}".')
            current_list_output_metrics[event_label] = {}

            # For each selected pair of variables to analyze, calculate metrics
            for pair_var in variables_to_analyze:
                var_to_analyze = pair_var[0]
                var_reference = pair_var[1]

                # Check that the selected signal to analyze and its reference signal (if they are defined) exist in the current event
                if len(var_to_analyze) > 0:
                    if var_to_analyze in self.list_viewers[viewer_name].dict_data[event_label]:
                        if 'x_sim' in self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze]:  # usually the variable to analyze is a simulated signal
                            x_var_to_analyze = self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze]['x_sim']
                            y_var_to_analyze = self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze]['y_sim']
                        elif 'x_meas' in self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze]:  # but a measured signal is also supported
                            x_var_to_analyze = self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze]['x_meas']
                            y_var_to_analyze = self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze]['y_meas']
                        else:
                            print(f'WARNING: Viewer {viewer_name}: Event "{event_label}": Signal label "{var_to_analyze}" not found. Signal skipped.')
                            continue
                    else:
                        print(f'WARNING: Viewer "{viewer_name}": Event "{event_label}": Signal label "{var_to_analyze}" not found. Signal skipped.')
                        continue
                else:
                    raise Exception(f'Viewer "{viewer_name}": Event "{event_label}": The first value of each pair in variables_to_analyze cannot be left empty, but {pair_var} was found.')

                if len(var_reference) > 0:  # if the string is empty, skip this check (it is possible to run the metrics calculation on one variable only)
                    if var_reference in self.list_viewers[viewer_name].dict_data[event_label]:
                        if 'x_meas' in self.list_viewers[viewer_name].dict_data[event_label][var_reference]:  # usually the variable to analyze is a measured signal
                            x_var_reference = self.list_viewers[viewer_name].dict_data[event_label][var_reference]['x_meas']
                            y_var_reference = self.list_viewers[viewer_name].dict_data[event_label][var_reference]['y_meas']
                        elif 'x_sim' in self.list_viewers[viewer_name].dict_data[event_label][var_reference]:  # but a simulated signal is also supported
                            x_var_reference = self.list_viewers[viewer_name].dict_data[event_label][var_reference]['x_sim']
                            y_var_reference = self.list_viewers[viewer_name].dict_data[event_label][var_reference]['y_sim']
                        else:
                            print(f'WARNING: Viewer "{viewer_name}": Event "{event_label}": Signal label "{var_reference}" not found. Signal skipped.')
                            continue
                    else:
                        print(f'WARNING: Viewer "{viewer_name}": Event "{event_label}": Signal label "{var_reference}" not found. Signal skipped.')
                        continue
                else:  # It is possible to run the metrics calculation on one variable only, without a reference signal
                    x_var_reference = None
                    y_var_reference = None

                # Perform the metrics calculation
                if verbose: print(f'Viewer "{viewer_name}": Event "{event_label}": Metrics calculated using signals "{var_to_analyze}" and "{var_reference}".')

                # Calculate the metrics
                # output_metric = PostprocsMetrics(
                #     metrics_to_calculate=metrics_to_calculate,
                #     x_value=x_var_to_analyze,
                #     y_value=y_var_to_analyze,
                #     x_ref=x_var_reference,
                #     y_ref=y_var_reference,
                #     flag_run=True)
                output_metric = PostprocsMetrics(metrics_to_do=metrics_to_calculate, var_to_interpolate=y_var_to_analyze,
                                                 var_to_interpolate_ref=y_var_reference, time_vector=x_var_to_analyze,
                                                 time_vector_ref=x_var_reference)
                current_list_output_metrics[event_label][var_to_analyze] = output_metric.metrics_result

        # Add the reference to the Viewer object in the dictionary
        self.list_metrics[metrics_name] = current_list_output_metrics

        return current_list_output_metrics

    def load_circuit_parameters(self, step, verbose: bool = False):
        """
        Load global circuit parameters from a .csv file into an existing BuilderModel circuit model
        :param step: STEAM analysis step of type LoadCircuitParameters, which has attributes:
        - model_name: BuilderModel object to edit - THIS MUST BE OF TYPE CIRCUIT
        - path_file_circuit_parameters: the name of the .csv file containing the circuit parameters
        - selected_circuit_name: name of the circuit name whose parameters will be loaded
        :param verbose: display additional logging info
        :return:
        """
        if verbose: print(f'Load circuit parameters.')

        # Unpack variables
        model_name = step.model_name
        path_file_circuit_parameters = step.path_file_circuit_parameters
        selected_circuit_name = step.selected_circuit_name

        BM = self.list_models[model_name]

        # Call function to load the parameters into the object
        BM.load_circuit_parameters_from_csv(input_file_name=path_file_circuit_parameters, selected_circuit_name=selected_circuit_name)

        # Update the BuilderModel object
        self.list_models[model_name] = BM

        return


    def setup_sim_FiQuS(self, simulation_name, sim_number, magnet_type=None):
        """
        Set up a FiQuS simulation by copying the last file generated by BuilderModel to the output folder and to the
        local FiQuS working folder.
        The original file is then deleted.
        """

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Make simulation folder
        local_model_folder = os.path.join(self.settings.local_FiQuS_folder, f'{simulation_name}_{str(sim_number)}')
        make_folder_if_not_existing(local_model_folder)

        # Copy simulation file
        file_name_temp = os.path.join(self.output_path, f'{simulation_name}')
        yaml_temp = os.path.join(file_name_temp + '_FiQuS.yaml')
        file_name_local = os.path.join(local_model_folder, f'{simulation_name}')
        yaml_local = os.path.join(file_name_local + '.yaml')
        shutil.copyfile(yaml_temp, yaml_local)

        if magnet_type == 'multipole':
            geo_temp = os.path.join(file_name_temp + '_FiQuS.geom')
            set_temp = os.path.join(file_name_temp + '_FiQuS.set')
            geo_local = os.path.join(file_name_local + '.geom')
            set_local = os.path.join(file_name_local + '.set')
            shutil.copyfile(geo_temp, geo_local)
            shutil.copyfile(set_temp, set_local)

        if self.verbose: print('Simulation files {} generated.'.format(file_name_temp))
        if self.verbose: print('Simulation files {} copied.'.format(file_name_local))

    def setup_sim_LEDET(self, simulation_name, sim_number, flag_yaml=True, flag_json=False):
        """
        Set up a LEDET simulation by copying the last file generated by BuilderModel to the output folder and to the
        local LEDET working folder. The original file is then deleted.
        If flag_yaml=True, the model is set up to be run using a yaml input file.
        If flag_json=True, the model is set up to be run using a json input file.
        """

        # Unpack
        output_folder = self.output_path
        local_LEDET_folder = self.settings.local_LEDET_folder

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Copy simulation file
        list_suffix = ['.xlsx']
        if flag_yaml == True:
            list_suffix.append('.yaml')
        if flag_json == True:
            list_suffix.append('.json')

        for suffix in list_suffix:
            file_name_temp = os.path.join(output_folder, simulation_name + suffix)
            file_name_output = os.path.join(output_folder, simulation_name + '_' + str(sim_number) + suffix)
            file_name_local = os.path.join(local_LEDET_folder, simulation_name, 'Input', simulation_name + '_' + str(sim_number) + suffix)

            shutil.copyfile(file_name_temp, file_name_output)
            if self.verbose: print('Simulation file {} generated.'.format(file_name_output))

            shutil.copyfile(file_name_temp, file_name_local)
            if self.verbose: print('Simulation file {} copied.'.format(file_name_local))

            # os.remove(file_name_temp)
            # print('Temporary file {} deleted.'.format(file_name_temp))

    def setup_sim_PSPICE(self, simulation_name, sim_number):
        """
        Set up a PSPICE simulation by copying the last file generated by BuilderModel to the output folder and to the
        local PSPICE working folder.
        The simulation netlist and auxiliary files are copied in a new numbered subfoldered.
        The original file is then deleted.
        """

        # Unpack
        output_folder = self.output_path
        local_PSPICE_folder = Path(self.settings.local_PSPICE_folder)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Make simulation folder
        local_model_folder = os.path.join(local_PSPICE_folder, simulation_name, str(sim_number))
        make_folder_if_not_existing(local_model_folder)

        # Copy simulation file
        file_name_temp = os.path.join(output_folder, simulation_name + '.cir')
        file_name_local = os.path.join(local_model_folder, simulation_name + '.cir')
        if self.verbose: print('Simulation file {} generated.'.format(file_name_temp))

        shutil.copyfile(file_name_temp, file_name_local)
        if self.verbose: print('Simulation file {} copied.'.format(file_name_local))

        # os.remove(file_name_temp)
        # print('Temporary file {} deleted.'.format(file_name_temp))

        # Copy lib files from the output folder
        list_lib_files = [entry for entry in os.listdir(output_folder) if (simulation_name in entry) and ('.lib' in entry)]
        for lib_file in list_lib_files:
            file_to_copy = os.path.join(output_folder, lib_file)
            file_copied = os.path.join(local_model_folder, lib_file)
            shutil.copyfile(file_to_copy, file_copied)
            if self.verbose: print('Lib file {} copied to {}.'.format(file_to_copy, file_copied))

        # Copy stl files from the output folder
        list_stl_files = [entry for entry in os.listdir(output_folder) if (simulation_name in entry) and ('.stl' in entry)]
        for stl_file in list_stl_files:
            file_to_copy = os.path.join(output_folder, stl_file)
            file_copied = os.path.join(local_model_folder, stl_file)
            shutil.copyfile(file_to_copy, file_copied)
            if self.verbose: print('Stl file {} copied to {}.'.format(file_to_copy, file_copied))

        # # Copy Conf.cir file from the output folder
        # list_cir_files = [entry for entry in os.listdir(output_folder) if ("Conf" in entry) and ('.cir' in entry)]
        # for cir_file in list_cir_files:
        #     file_to_copy = os.path.join(output_folder, cir_file)
        #     file_copied = os.path.join(local_model_folder, cir_file)
        #     shutil.copyfile(file_to_copy, file_copied)
        #     if self.verbose: print('Cir file {} copied to {}.'.format(file_to_copy, file_copied))

        # Special case: Copy coil_resistances.stl file from the output folder
        file_coil_resistances_to_copy = os.path.join(output_folder, 'coil_resistances.stl')
        file_coil_resistances_copied = os.path.join(local_model_folder, 'coil_resistances.stl')
        if os.path.isfile(file_coil_resistances_to_copy):
            shutil.copyfile(file_coil_resistances_to_copy, file_coil_resistances_copied)
            if self.verbose: print('Stl file {} copied to {}.'.format(file_coil_resistances_to_copy, file_coil_resistances_copied))

    def setup_sim_XYCE(self, simulation_name, sim_number):
        """
        Set up a PSPICE simulation by copying the last file generated by BuilderModel to the output folder and to the
        local PSPICE working folder.
        The simulation netlist and auxiliary files are copied in a new numbered subfoldered.
        The original file is then deleted.
        """

        # Unpack
        output_folder = self.output_path
        local_XYCE_folder = Path(self.settings.local_XYCE_folder)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Make simulation folder
        local_model_folder = os.path.join(local_XYCE_folder, simulation_name, str(sim_number))
        make_folder_if_not_existing(local_model_folder)

        # Copy simulation file
        file_name_temp = os.path.join(output_folder, simulation_name + '.cir')
        file_name_local = os.path.join(local_model_folder, simulation_name + '.cir')
        if self.verbose: print('Simulation file {} generated.'.format(file_name_temp))

        self.copy_XYCE_cir(file_name_temp, file_name_local)
        if self.verbose: print('Simulation file {} copied.'.format(file_name_local))

        # os.remove(file_name_temp)
        # print('Temporary file {} deleted.'.format(file_name_temp))

        local_XYCE_folder = Path(self.settings.local_XYCE_folder)
        local_model_folder = str(Path(local_XYCE_folder / simulation_name/ str(sim_number)).resolve())
        # Make circuit input folder
        make_folder_if_not_existing(local_model_folder, verbose=self.verbose)

        # Copy lib files from the output folder
        list_lib_files = [entry for entry in os.listdir(self.output_path) if
                          (simulation_name in entry) and ('.lib' in entry)]
        for lib_file in list_lib_files:
            file_to_copy = os.path.join(self.output_path, lib_file)
            file_copied = os.path.join(local_model_folder, lib_file)
            shutil.copyfile(file_to_copy, file_copied)
            if self.verbose: print('Lib file {} copied to {}.'.format(file_to_copy, file_copied))

        # Copy csv files from the output folder
        csv_path = os.path.join(self.output_path, 'Stimulus')
        csv_path_new = os.path.join(local_model_folder, 'Stimulus')
        if os.path.exists(csv_path_new):
            shutil.rmtree(csv_path_new)
        os.mkdir(csv_path_new)

        list_csv_files = [entry for entry in os.listdir(csv_path) if (simulation_name in entry) and ('.csv' in entry)]
        for csv_file in list_csv_files:
            file_to_copy = os.path.join(csv_path, csv_file) #self.output_path was first argument; changed it to stl_path
            file_copied = os.path.join(csv_path_new, csv_file)
            shutil.copyfile(file_to_copy, file_copied)
            if self.verbose: print('Csv file {} copied to {}.'.format(file_to_copy, file_copied))

        # Special case: Copy coil_resistances.csv file from the output folder
        file_coil_resistances_to_copy = os.path.join(output_folder, 'coil_resistances.csv')
        file_coil_resistances_copied = os.path.join(local_model_folder, 'coil_resistances.csv')
        if os.path.isfile(file_coil_resistances_to_copy):
            shutil.copyfile(file_coil_resistances_to_copy, file_coil_resistances_copied)
            if self.verbose: print('Csv file {} copied to {}.'.format(file_coil_resistances_to_copy, file_coil_resistances_copied))

    def copy_XYCE_cir(self, file_name_temp, file_name_local):
        '''
            Function that copies the XYCE circuit file from 'file_name_temp' to 'file_name_local' and changes the
            respective output path for the csd
        :param file_name_temp: Original circuit file
        :param file_name_local: Final circuit file
        :return:
        '''

        with open(file_name_temp) as f:
            contents = f.readlines()
        for k in range(len(contents)):
            if contents[k].casefold().startswith('.print'):
                if 'csd' in contents[k]: type_output = 'csd'
                elif 'csv' in contents[k]: type_output = 'csv'
                elif 'txt' in contents[k]: type_output = 'txt'
                else:
                    raise Exception("Don't understand output type.")
                print_line = contents[k].split('FILE=')
                print_line[-1] = f'FILE={file_name_local[:-4]}.{type_output} \n'
                contents[k] = ''.join(print_line)
                break

        contents = ''.join(contents)
        new_file = open(file_name_local, 'w')
        new_file.write(contents)
        new_file.close()


    def setup_sim_PyBBQ(self, simulation_name, sim_number):
        """
        Set up a PyBBQ simulation by copying the last file generated by BuilderModel to the output folder and to the
        local PyBBQ working folder.
        The original file is then deleted.
        """

        # Unpack
        output_folder = self.output_path
        local_PyBBQ_folder = Path(self.settings.local_PyBBQ_folder)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Make simulation folder
        local_model_folder = os.path.join(local_PyBBQ_folder, simulation_name, str(sim_number))
        make_folder_if_not_existing(local_model_folder)

        # Copy simulation file
        file_name_temp = os.path.join(output_folder, simulation_name + '.yaml')
        file_name_local = os.path.join(local_model_folder, simulation_name + '.yaml')
        if self.verbose: print('Simulation file {} generated.'.format(file_name_temp))

        shutil.copyfile(file_name_temp, file_name_local)
        if self.verbose: print('Simulation file {} copied.'.format(file_name_local))

        # os.remove(file_name_temp)
        # print('Temporary file {} deleted.'.format(file_name_temp))


    def run_sim(self, software: str, simulation_name: str, sim_number: int, simFileType: str = None, verbose: bool = False):
        """
        Run selected simulation.
        The function applies a different logic for each simulation software.
        """
        if software == 'FiQuS':
            local_analysis_folder = simulation_name + '_' + str(sim_number)
            dFiQuS = DriverFiQuS(FiQuS_path=self.settings.FiQuS_path, path_folder_FiQuS=self.settings.local_FiQuS_folder,
                                 path_folder_FiQuS_input=os.path.join(self.settings.local_FiQuS_folder, local_analysis_folder), verbose=verbose)
            self.summary = dFiQuS.run_FiQuS(sim_file_name=simulation_name, output_directory=local_analysis_folder)
        elif software == 'LEDET':
            dLEDET = DriverLEDET(path_exe=self.settings.LEDET_path, path_folder_LEDET=self.settings.local_LEDET_folder, verbose=verbose)
            dLEDET.run_LEDET(simulation_name, str(sim_number), simFileType=simFileType)
        elif software == 'PyBBQ':
            local_model_folder_input = os.path.join(self.settings.local_PyBBQ_folder, simulation_name, str(sim_number))
            relative_folder_output = os.path.join(simulation_name, str(sim_number))
            dPyBBQ = DriverPyBBQ(path_exe=self.settings.PyBBQ_path, path_folder_PyBBQ=self.settings.local_PyBBQ_folder, path_folder_PyBBQ_input=local_model_folder_input, verbose=verbose)
            dPyBBQ.run_PyBBQ(simulation_name, outputDirectory=relative_folder_output)
        elif software == 'PSPICE':
            local_model_folder = Path(Path(self.settings.local_PSPICE_folder) / simulation_name / str(sim_number)).resolve()
            dPSPICE = DriverPSPICE(path_exe=self.settings.PSPICE_path, path_folder_PSPICE=local_model_folder, verbose=verbose)
            dPSPICE.run_PSPICE(simulation_name, suffix='')
        elif software == 'XYCE':
            local_model_folder = Path(Path(self.settings.local_XYCE_folder) / simulation_name / str(sim_number)).resolve()
            dXYCE = DriverXYCE(path_exe=self.settings.XYCE_path, path_folder_XYCE=local_model_folder, verbose=verbose)
            dXYCE.run_XYCE(simulation_name, suffix='')
        else:
            raise Exception(f'Software {software} not supported for automated running.')


    def write_stimuli_from_interpolation(self, step, verbose: bool = False):
        '''
        Function to write a resistance stimuli for n apertures of a magnet for any current level. Resistance will be interpolated
        from pre-calculated values (see InterpolateResistance for closer explanation). Stimuli is then written in a .stl file for PSPICE

        :param current_level: list, all current level that shall be used for interpolation (each magnet has 1 current level)
        :param n_total_magnets: int, Number of total magnets in the circuit (A stimuli will be written for each, non-quenching = 0)
        :param n_apertures: int, Number of apertures per magnet. A stimuli will be written for each aperture for each magnet
        :param magnets: list, magnet numbers for which the stimuli shall be written
        :param tShift: list, time shift that needs to be applied to each stimuli
        (e.g. if magnet 1 quenches at 0.05s, magnet 2 at 1s etc.), so that the stimuli are applied at the correct time in the simulation
        :param Outputfile: str, name of the stimuli-file
        :param path_resources: str, path to the file with pre-calculated values
        :param InterpolationType: str, either Linear or Spline, type of interpolation
        :param type_stl: str, how to write the stimuli file (either 'a' (append) or 'w' (write))
        :param sparseTimeStepping: int, every x-th time value only a stimuli point is written (to reduce size of stimuli)
        :return:
        '''
        # Unpack inputs
        current_level      = step.current_level
        n_total_magnets    = step.n_total_magnets
        n_apertures        = step.n_apertures
        magnets            = step.magnets
        tShift             = step.t_offset
        Outputfile         = step.output_file
        path_resources     = step.path_interpolation_file
        InterpolationType  = step.interpolation_type
        type_stl           = step.type_file_writing
        sparseTimeStepping = step.n_sampling
        magnet_type        = step.magnet_types
        # Set default values for selected missing inputs
        if not InterpolationType:
            InterpolationType = 'Linear'
        if not type_stl:
            type_stl = 'w'
        if not sparseTimeStepping:
            sparseTimeStepping = 1  # Note: This will ovrewrite the default value of 100 used in the writeStimuliFromInterpolation_general() function

        # Call coil-resistance interpolation function
        writeStimuliFromInterpolation_general(current_level, n_total_magnets, n_apertures, magnets, tShift, Outputfile, path_resources, InterpolationType, type_stl, sparseTimeStepping, magnet_type)

        if verbose:
            print(f'Output stimulus file {Outputfile} written.')


    def run_parsim_event(self, step, verbose: bool = False):
        '''
        Function to generate steps based on list of events from external file

        :param step:
        :param verbose: if true displays more information
        :return:
        '''
        input_file              = step.input_file
        simulation_numbers      = step.simulation_numbers
        model_name              = step.model_name
        case_model              = step.case_model
        simulation_name         = step.simulation_name
        software                = step.software
        t_PC_off                = step.t_PC_off
        current_polarities_CLIQ = step.current_polarities_CLIQ
        list_QH_strips_to_units = step.list_QH_strips_to_units
        flag_set_up_viewer      = step.flag_set_up_viewer
        path_viewer_csv         = step.path_viewer_csv
        default_keys            = step.default_keys

        # Check inputs
        if type(path_viewer_csv) == str:
            path_viewer_csv = [path_viewer_csv]  # Make sure this variable is always a list
        if path_viewer_csv and (len(path_viewer_csv) != len(software)):
            raise Exception(f'The length of path_viewer_csv ({len(path_viewer_csv)}) differs from the length of software({len(software)}). This is not allowed.')

        # path to ideal Quench dict
        outputfile_event_csv = os.path.join(os.getcwd(), 'output', 'run_parsim_event', 'events.csv')  # TODO avoid hard-coding this file name?
        # Read input file and run the ParsimEvent analysis
        if case_model == 'magnet':
            pem = ParsimEventMagnet(ref_model=self.list_models[model_name], verbose=verbose)
            pem.read_from_input(path_input_file=input_file, flag_append=False)
            pem.set_up_analysis(model_name=model_name, simulation_name=simulation_name,
                                simulation_numbers=simulation_numbers, software=software,
                                t_PC_off=t_PC_off,
                                current_polarities_CLIQ=current_polarities_CLIQ,
                                list_QH_strips_to_units=list_QH_strips_to_units,
                                path=outputfile_event_csv)
            for step_name in pem.list_AnalysisStepSequence:
                step = pem.dict_AnalysisStepDefinition[step_name]
                self.step_modify_model_multiple_variables(step, verbose=verbose)
            # TODO: merge list and dict into self.data_analysis
            # pem.list_AnalysisStepSequence
            # pem.dict_AnalysisStepDefinition
            # TODO: add flag_show_parsim_output ?
            # TODO: add flag to write yaml analysis with all steps

            # Optionally, write a .csv file that can be used to run a STEAM Viewer analysis
            if flag_set_up_viewer:
                for current_software, current_path_viewer_csv in zip(software, path_viewer_csv):
                    pem.set_up_viewer(current_path_viewer_csv, default_keys, simulation_numbers, simulation_name, current_software)
                    if verbose: print(f'File {current_path_viewer_csv} written. It can be used to run a STEAM Viewer analysis.')
        else:
            raise Exception(f'case_model {case_model} not supported by ParsimEvent.')

        if verbose:
            print(f'ParsimEvent called using input file {input_file}.')


    def run_parsim_sweep_OLD(self, step, verbose: bool = False):
        '''
        Function to generate steps based on list of events from external file

        :param step:
        :param verbose: if true displays more information
        :return:
        '''
        input_sweep_file = step.input_sweep_file
        model_name = step.model_name
        case_model = step.case_model
        software = step.software
        flag_build = step.flag_build  # TODO: wozu dieser flag?
        verbose = step.verbose

        # path to ideal Quench dict
        input_sweep_file_abs = os.path.join(os.getcwd(), input_sweep_file)
        # Read input file and run the ParsimEvent analysis
        if case_model == 'magnet':
            ps = ParsimSweep(ref_model=self.list_models[model_name], verbose=verbose)
            ps.read_from_input(file_path=input_sweep_file_abs, flag_append=False)
            # ps.set_up_analysis(...)
            for step_name in pem.list_AnalysisStepSequence:
                step = pem.dict_AnalysisStepDefinition[step_name]
                self.step_modify_model_multiple_variables(step, verbose=verbose)
        else:
            raise Exception(f'case_model {case_model} not supported by parsim events')

        if verbose:
            print(f'Parsim Event called using input file {input_sweep_file}.')


    def run_parsim_sweep(self, step, verbose: bool = False):
        '''
        Function to generate steps based on list of models read from external file
        :param step:
        :param verbose: if true displays more information
        :return:
        '''
        # Unpack inputs
        input_sweep_file = step.input_sweep_file
        model_name = step.model_name
        case_model = step.case_model
        software = step.software
        verbose = step.verbose

        input_parsim_sweep_df = pd.read_csv(input_sweep_file)
        for i, row in input_parsim_sweep_df.iterrows():
            simulation_number = row['simulation_number']
            simulation_name = row['simulation_name']
            if verbose: print(f'changing these fields row # {i + 1}: {row}')
            
            if case_model == 'magnet':
                model_data = self.list_models[model_name].model_data
            elif case_model == 'circuit':
                model_data = self.list_models[model_name].circuit_data
            elif case_model == 'conductor':
                model_data = self.list_models[model_name].conductor_data
            else:
                raise Exception(f'case_model {case_model} not supported by ParsimSweep.')

            # Iterate through the keys and values in the data dictionary
            for var_name, var_value in row.items():
                # Check if the current variable is present in the model data structure
                if rhasattr(model_data, var_name):
                    # For each variable to change, make an instance of an ModifyModel step and call the step_modify_model() method
                    next_step = ModifyModel(type='ModifyModel')
                    next_step.model_name = model_name
                    next_step.variable_to_change = var_name
                    next_step.variable_value = [var_value]
                    next_step.simulation_numbers = [simulation_number]
                    next_step.simulation_name = simulation_name
                    next_step.software = software
                    self.step_modify_model(next_step, verbose=verbose)
            #TODO handle the case where the value from the csv file is empty
            #TODO handle the case where no variable to change is found in the csv file
        
        # # Open the CSV file
        # with open(input_sweep_file, 'r') as csv_file:
        #     # Generate a CSV reader
        #     reader = csv.DictReader(csv_file)
        #     # Iterate through the rows (parametric simulations to set up)
        #     for i, row in enumerate(reader):
        #         simulation_number = row['simulation_number']
        #         simulation_name = row['simulation_name']
        #         if verbose: print(f'changing these fields row # {i+1}: {row}')
        #
        #         if case_model == 'magnet':
        #             model_data = self.list_models[model_name].model_data
        #         else:
        #             raise Exception(f'case_model {case_model} not supported by ParsimSweep.')
        #
        #         # Iterate through the keys and values in the data dictionary
        #         for var_name, var_value in row.items():
        #             # Check if the current variable is present in the model data structure
        #             if rhasattr(model_data, var_name):
        #                 # For each variable to change, make an instance of an ModifyModel step and call the step_modify_model() method
        #                 next_step                    = ModifyModel(type='ModifyModel')
        #                 next_step.model_name         = model_name
        #                 next_step.variable_to_change = var_name
        #                 next_step.variable_value     = [var_value]
        #                 next_step.simulation_numbers = [simulation_number]
        #                 next_step.simulation_name    = simulation_name
        #                 next_step.software           = software
        #                 self.step_modify_model(next_step, verbose=verbose)

        #
        #
        #
        #
        #             # Set the class variable using the key and value
        #             try:
        #                 rsetattr(new_BM, key, value)
        #             except:
        #                 try:
        #                     rsetattr(new_BM.model_data, key, value)
        #                 except:
        #                     print(f'Skipped column {key} - no corresponding entry in BuilderModel found.')
        #         # Append the row as a dictionary to the list
        #         self.dict_BuilderModels[self.simulation_numbers[i]] = new_BM
        # if verbose:
        #     print('csv file read.')
        #
        # # Read input file and run the ParsimEvent analysis
        # if case_model == 'magnet':
        #
        #     # Loop through the list of variables to change
        #     for v, variable_to_change in enumerate(step.variables_to_change):
        #         # For each variable to change, make an instance of an ModifyModel step and call the step_modify_model() method
        #         next_step = ModifyModel(type='ModifyModel')
        #         next_step.model_name = step.model_name
        #         next_step.variable_to_change = variable_to_change
        #         next_step.variable_value = step.variables_value[v]
        #         if v + 1 == len_variables_to_change:  # If this is the last variable to change, import new_model_name and simulation_numbers from the step
        #             next_step.new_model_name = step.new_model_name
        #             next_step.simulation_numbers = step.simulation_numbers
        #         else:  # else, set new_model_name and simulation_numbers to empty lists to avoid making models/simulations for intermediate changes
        #             next_step.new_model_name = []
        #             next_step.simulation_numbers = []
        #         next_step.simulation_name = step.simulation_name
        #         next_step.software = step.software
        #         self.step_modify_model(next_step, verbose=verbose)
        #     if verbose:
        #         print('All variables of step {} were changed.'.format(step))
        #
        #
        #
        #     ps = ParsimSweep(ref_model=self.list_models[model_name], verbose=verbose)
        #     ps.read_from_input(file_path=input_sweep_file, flag_append=False)
        #     # ps.set_up_analysis(...)
        #     for step_name in pem.list_AnalysisStepSequence:
        #         step = pem.dict_AnalysisStepDefinition[step_name]
        #         self.step_modify_model_multiple_variables(step, verbose=verbose)
        # else:
        #     raise Exception(f'case_model {case_model} not supported by ParsimSweep.')

        if verbose:
            print(f'Parsim Event called using input file {input_sweep_file}.')
