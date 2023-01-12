import os
import datetime
import ntpath
import shutil
import textwrap
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import interp1d
import pandas as pd
import numpy as np

import yaml

from steam_sdk.data.DataModelCircuit import DataModelCircuit, Component
from steam_sdk.parsers.ParserYAML import dict_to_yaml


class ParserXYCE:
    """
        Class with methods to read/write XYCE information from/to other programs
    """

    def __init__(self, circuit_data: DataModelCircuit, path_input: Path = None, output_path: str = ''):
        """
            Initialization using a DataModelCircuit object containing circuit netlist structure
        """

        self.circuit_data: DataModelCircuit = circuit_data
        self.path_input: str = path_input
        self.output_path: str = output_path


    def read_netlist(self, full_path_file_name: str, flag_acquire_auxiliary_files: bool = False, verbose: bool = False):
        '''
        ** Reads a XYCE netlist file **

        :param full_path_file_name:
        :param flag_acquire_auxiliary_files: If True, add list of additional files to circuit_data
        :param verbose:
        :return: ModelCircuit dataclass with filled keys
        '''

        # Initialize
        self.circuit_data = DataModelCircuit()
        self.circuit_data.InitialConditions.initial_conditions = {}
        # Set flags indicating that the last read line corresponds to an item that might span to the next line
        self._set_all_flags_to_false()
        self.flag_found_title = 0

        with open(full_path_file_name) as file:
            for row, line in enumerate(file):
                if verbose: print(line.rstrip())

                line = line.replace('\t',' ').rstrip('\n')

                # If the line is empty, skip to the next
                if (not line):
                    self._set_all_flags_to_false()
                    continue

                if (type(line)==str) and (not self.flag_found_title):
                    self.circuit_data.GeneralParameters.circuit_name = line.replace(' ','')
                    self.flag_found_title = 1
                    continue

                # Reset all flags to False if the line does not contain '+' in first position (excluding whitespaces)
                # Note: When one of these flags is set to True it indicates that this line might contain additional parameters from the previous line
                if (not '+' in line) and (not line.strip(' ')[0] == '+'):
                    self._set_all_flags_to_false()

                # If the line is a comment, skip to the next
                if '*' in line and line[0] == '*':
                    continue
                # If the line is the ending command, skip to the next
                if '.END' in line:
                    continue

                # Remove spaces before and after the "=" equal sign to make the parser more robust
                line = line.replace(' =', '=')
                line = line.replace('= ', '=')

                # Read libraries
                if '.INCLUDE' in line:
                    line_split = line.split(' ')
                    value = line_split[1].strip('"')
                    self.circuit_data.Libraries.component_libraries.append(str(value))
                    continue

                # Read global parameters
                if '.PARAM' in line:  # it also covers the case where ".PARAMS" is written
                    self.flag_read_global_parameters = True
                    self.circuit_data.GlobalParameters.global_parameters = {}
                    continue
                if self.flag_read_global_parameters and '+ ' in line:
                    line_split = line.split(' ')
                    line_split = line_split[1].split('=')
                    name  = line_split[0].strip('"')
                    value = line_split[1].strip('{').strip('}')
                    self.circuit_data.GlobalParameters.global_parameters[str(name)] = str(value)
                    continue

                # Read initial conditions
                if '.IC ' in line or '.DCVOLT' in line:
                    if '.IC' in line:
                        line = line[3:]
                    if '.DCVOLT' in line:
                        line = line[7:]
                    line = line.replace('V(','').replace(')','').replace('=',' ')
                    line = line.split(' ')  # remove whitespaces at the beginning and end of the string, then divide it at the internal whitespace
                    line_split = [x for x in line if x]
                    name = 'V('+line_split[0]+')'
                    value = line_split[1]
                    self.circuit_data.InitialConditions.initial_conditions[str(name)] = str(value)
                    continue

                # Read options
                if '.OPTION' in line:  # it also covers the case where ".OPTIONS" is written
                    self.flag_read_options = True
                    self.circuit_data.Options.options_simulation = {}
                    continue
                if self.flag_read_options and '+ ' in line:
                    line_split = line.rstrip('\n').strip(' ').split(' ')
                    line_split = line_split[1].split('=')
                    name  = line_split[0].strip('"')
                    value = line_split[1].strip('{').strip('}')
                    self.circuit_data.Options.options_simulation[str(name)] = str(value)
                    continue

                # Read analysis
                if '.TRAN' in line:
                    self.circuit_data.Analysis.analysis_type = 'transient'
                    line = line.replace('s','')
                    line_split = line.split(' ')
                    self.circuit_data.Analysis.simulation_time.time_start = str(line_split[1])
                    self.circuit_data.Analysis.simulation_time.time_end = str(line_split[2])
                    if len(line_split) > 3:
                        self.circuit_data.Analysis.simulation_time.min_time_step = str(line_split[3])
                    continue
                elif '.AC' in line:
                    self.circuit_data.Analysis.analysis_type = 'frequency'
                    line_split = line.split(' ')
                    self.circuit_data.Analysis.simulation_frequency.frequency_step = str(line_split[1])
                    self.circuit_data.Analysis.simulation_frequency.frequency_points = str(line_split[2])
                    self.circuit_data.Analysis.simulation_frequency.frequency_start = str(line_split[3])
                    self.circuit_data.Analysis.simulation_frequency.frequency_end = str(line_split[4])
                    continue
                elif '.STEP' in line:
                    # TODO. Parametric analysis
                    continue

                # Read time schedule
                if 'SCHEDULE' in line:
                    self.flag_read_time_schedule = True
                    self.circuit_data.Analysis.simulation_time.time_schedule = {}
                    if not ')}' in line:
                        continue
                # If the line is the end of the time schedule section, skip to the next
                elif ('}' in line or '}' in line) and (self.flag_read_time_schedule):
                    self.flag_read_time_schedule = False
                    continue
                if self.flag_read_time_schedule and ',' in line:
                    line_split = line.split(',')
                    line_split = [x.replace('+','').replace(',','').replace(' ','') for x in line_split]
                    name = line_split[0]
                    value = line_split[1]
                    self.circuit_data.Analysis.simulation_time.time_schedule[str(name)] = str(value)
                    continue

                # Read print
                if '.PRINT' in line:
                    format = line.split('=')[1].split(' ')[0]
                    if format=='PROBE':
                        self.circuit_data.PostProcess.probe.probe_type = 'standard'
                    elif format=='CSV':
                        self.circuit_data.PostProcess.probe.probe_type = 'CSV'
                    else:
                        self.circuit_data.PostProcess.probe.probe_type = format
                        if verbose: print(f'Print type {format} not understood.')
                    self.flag_read_probe = True
                    # TODO: Known issue: If probe variables are defined in this same line, they are ignored
                    continue
                if self.flag_read_probe and '+ ' in line:
                    line_split = line.split(' ')
                    value = line_split[1]
                    self.circuit_data.PostProcess.probe.variables.append(str(value))
                    continue

                # Special case: Controlled-source component
                # E: Voltage-controlled voltage source
                # F: Current-controlled current source
                # G: Voltage-controlled current source
                # H: Current-controlled voltage source
                list_controlled_components = ['e', 'f', 'g', 'h']
                if line[0].casefold() in list_controlled_components:
                    keywords_controlled_components = ['VALUE', 'POLY', 'TABLE']
                    keyword = 'GAIN'
                    for k in range(len(keywords_controlled_components)):
                        if keywords_controlled_components[k] in line:
                            keyword = keywords_controlled_components[k]
                            break
                    if keyword != 'VALUE':
                        raise Exception('Not implemented yet.')

                    line_split = line.split(keyword)
                    value = line_split[-1].replace('{','').replace('}','').replace('=','').replace(' ','')
                    line_split = line_split[0].split(' ')
                    line_split = [x for x in line_split if x]
                    name = line_split[0]
                    nodes = line_split[1:]

                    new_Component = Component()
                    new_Component.type = 'controlled-source component'
                    new_Component.nodes = nodes
                    new_Component.value = str(value)
                    self.circuit_data.Netlist.__setattr__(name, new_Component)
                    continue

                # Special case: B component
                if line[0].casefold()=='b':
                    if 'V=' in line:
                        keyword = 'V='
                    elif 'I=' in line:
                        keyword =  'I='

                    line_split = line.split(keyword)
                    value = keyword+line_split[-1]
                    line_split = line_split[0].split(' ')
                    line_split = [x for x in line_split if x]
                    name = line_split[0]
                    nodes = line_split[1:]

                    new_Component = Component()
                    new_Component.type = 'nonlinear-dependent-source component'
                    new_Component.nodes = nodes
                    new_Component.value = str(value)
                    self.circuit_data.Netlist.__setattr__(name, new_Component)
                    continue

                # Special case: Parametrized component
                if line[0].casefold()=='x':
                    self.flag_read_parametrized_component = True
                    line = line.split(' ')

                    name = line[0]
                    value = line[-1]
                    nodes = line[1:-1]

                    self.name_last_component = name
                    new_Component = Component()
                    new_Component.type = 'parametrized component'
                    new_Component.nodes = nodes
                    new_Component.value = str(value)
                    self.circuit_data.Netlist.__setattr__(self.name_last_component, new_Component)
                    continue

                # Special case: Parameters of a parametrized component
                if self.flag_read_parametrized_component and '+ PARAM' in line:  # This line defines parameters of the component
                    # Reminder: This type of line looks like this: + PARAMS: name1={value1} name2={value2} name3={value3}
                    line_split = line.partition(':')[2]  # Take the part of the string after the first "+" char
                    line_split = line_split.split(' ')         # Split into different parameters

                    continue_Component = getattr(self.circuit_data.Netlist, self.name_last_component)
                    for par in line_split:                     # Loop through the parameters
                        par_split = par.split('=')             # Split into name and value of the parameter
                        if len(par_split) == 2:                # Only take into account entries with two elements (for example, avoid None)
                            name_par = str(par_split[0].strip(' '))
                            value_par = str(par_split[1].strip(' { } '))  # Strip spaces and bracket at the extremities
                            continue_Component.parameters[str(name_par)] = str(value_par)
                    self.circuit_data.Netlist.__setattr__(self.name_last_component, continue_Component)
                    continue
                elif self.flag_read_parametrized_component and '+' in line and line[0] == '+':  # This line defines additional parameters of the component
                    # Reminder: This type of line looks like this: + PARAMS: name1={value1} name2={value2} name3={value3}
                    line_split = line.partition('+')[2]        # Take the part of the string after the first "+" char
                    line_split = line_split.split(' ')                      # Split into different parameters
                    continue_Component = getattr(self.circuit_data.Netlist, self.name_last_component)
                    for par in line_split:                                  # Loop through the parameters
                        par_split = par.split('=')                          # Split into name and value of the parameter
                        if len(par_split) == 2:                             # Only take into account entries with two elements (for example, avoid None)
                            name_par  = str(par_split[0].strip(' '))
                            value_par = str(par_split[1].strip(' { } '))  # Strip spaces and bracket at the extremities
                            continue_Component.parameters[str(name_par)] = str(value_par)
                    self.circuit_data.Netlist.__setattr__(self.name_last_component, continue_Component)
                    continue

                # Current/Voltage source
                if line[0].casefold()=='i' or line[0].casefold()=='v':
                    list_transient_options = ['PULSE','SIN','EXP','PWL','PAT','SFFM']
                    keyword = ''
                    for k in range(len(list_transient_options)):
                        if list_transient_options[k] in line:
                            keyword = list_transient_options[k]
                            break
                    if not keyword:
                        line_split = line.split(' ')
                        value = line_split[-1].replace(' ','')
                        del line_split[-1]
                    else:
                        line_split = line.split(keyword)
                        value = line_split[-1].replace('(','').replace(')','')
                        line_split = line_split[0].split(' ')
                    if '{' in value or '}' in value:
                        value = value.replace('{','').replace('}','')
                    if ' ' == value[0]:
                        value = value[1:]

                    if 'file' in value.casefold():
                        value_split = value.split(' ')
                        source_file = value_split[-1]
                        source_file = source_file.replace('"','').replace("'",'')
                        self.circuit_data.GeneralParameters.additional_files.append(source_file)
                    line_split = [x for x in line_split if x]
                    name = line_split[0]
                    nodes = line_split[1:]

                    new_Component = Component()
                    if keyword == 'PULSE':
                        new_Component.type = 'pulsed-source component'
                    elif keyword == 'PWL':
                        new_Component.type = 'stimulus-controlled component'
                    else:
                        if keyword:
                            value = keyword + ' ' + value
                        new_Component.type = 'standard component'
                    new_Component.nodes = nodes
                    new_Component.value = str(value)
                    self.circuit_data.Netlist.__setattr__(name, new_Component)
                    continue


                # If this part of the code is reached, the line defines standard component
                line = line.split(' ')

                name = line[0]
                nodes = line[1:-1]
                value = line[-1].replace('{','').replace('}','')
                new_Component = Component()
                new_Component.type = 'standard component'
                new_Component.nodes = nodes
                new_Component.value = str(value)
                self.circuit_data.Netlist.__setattr__(name, new_Component)

        if flag_acquire_auxiliary_files:
            # Read entries of required additional files and add them to the yaml dictionary
            # Add component library files (defined with ".LIB" option)
            for file in self.circuit_data.Libraries.component_libraries:
                self.circuit_data.GeneralParameters.additional_files.append(file)
            if verbose:
                print('Option flag_acquire_auxiliary_files set to {}'.format(flag_acquire_auxiliary_files))
                for file in self.circuit_data.GeneralParameters.additional_files:
                    print('File {} added to the list of files to add to the model.'.format(file))

        return self.circuit_data


    def _set_all_flags_to_false(self):
        '''
            # Set flags indicating that the last read line corresponds to an item that might span to the next line
        '''
        self.flag_read_global_parameters = False
        self.flag_read_parametrized_component = False
        self.flag_read_options = False
        self.flag_read_autoconverge = False
        self.flag_read_time_schedule = False
        self.flag_read_probe = False
        self.name_last_component = None  # this is used to have the name of the latest added component (used to read the parameters of parametrized component over multiple rows)


    def write2XYCE(self, full_path_file_name: str, verbose: bool = False):
        '''
        ** Writes a XYCE netlist file **

        :param full_path_file_name:
        :param verbose:
        :return:
        '''
        current_path = Path(full_path_file_name).parent.resolve()

        # Title of the circuit
        row_title = [f'{self.circuit_data.GeneralParameters.circuit_name} \n']

        # Prepare header
        time_start = datetime.datetime.now()
        rows_header = [
            add_comment('XYCE Netlist Simulation File'),
            add_comment('Generated at {} at CERN using STEAM_SDK'.format(time_start)),
            add_comment('Authors: STEAM Team'),
        ]

        # Prepare libraries
        rows_libraries = []
        if self.circuit_data.Libraries.component_libraries:
            rows_libraries.append(add_comment('**** Component libraries ****'))  # Add header of this section
            for s in self.circuit_data.Libraries.component_libraries:
                rows_libraries.append(add_library(s))

        # Prepare global parameters
        rows_global_parameters = []
        if self.circuit_data.GlobalParameters.global_parameters:
            # Add comment and .PARAM command before the first entry
            rows_global_parameters.append(add_comment('**** Global parameters ****'))  # Add header of this section
            rows_global_parameters.append('.PARAM')  # Add header of this section
            # Add global parameter entries
            for name, value in self.circuit_data.GlobalParameters.global_parameters.items():
                if '#' in str(value):
                    value = value.replace('#','')
                if '#' in str(name):
                    name = name.replace('#','')
                rows_global_parameters.append(add_global_parameter(name, value))

        # Prepare initial conditions
        rows_initial_conditions = []
        if self.circuit_data.InitialConditions.initial_conditions:
            # Add comment and .PARAM command before the first entry
            rows_initial_conditions.append(add_comment('**** Initial conditions ****'))  # Add header of this section
            # Add initial condition entries
            for name, value in self.circuit_data.InitialConditions.initial_conditions.items():
                if name[0].casefold()=='i':
                    if verbose: print('Initial condition for currents not supported in XYCE. Will be ignored.')
                    continue
                rows_initial_conditions.append(add_initial_condition(name, value))

        # Prepare netlist
        rows_netlist = []
        rows_netlist.append(add_comment('**** Netlist ****'))  # Add header of this section
        for s, name in enumerate(self.circuit_data.Netlist.__dict__.keys()):
            # Read keys
            type        = getattr(getattr(self.circuit_data.Netlist, name), 'type')
            nodes       = getattr(getattr(self.circuit_data.Netlist, name), 'nodes')
            value       = getattr(getattr(self.circuit_data.Netlist, name), 'value')
            parameters  = getattr(getattr(self.circuit_data.Netlist, name), 'parameters')
            # name, nodes, value, parameters, type = component.name, component.nodes, component.value, component.parameters, component.type

            # Check inputs
            if not type:
                raise Exception('At least one netlist entry of known type must be added. Supported component types:\n' +
                                '- comment\n' +
                                '- standard component\n'
                                '- stimulus-controlled component\n'
                                '- controlled-source component\n'
                                '- pulsed-source component\n'
                                '- parametrized component\n'
                                '- transient-source component\n'
                                'Netlist cannot be generated.')

            # Add the relevant row depending on the component type
            if type == 'comment':
                if verbose: print('Netlist entry {} in position #{} is treated as a comment.'.format(name, s + 1))
                rows_netlist.append(add_comment(value))
            elif type == 'standard component':
                if name == None or nodes == None or value == None:
                    raise Exception('Netlist component in position #{} is of type {} and requires name, nodes, and value.'.format(s+1, type))
                if verbose: print('Netlist entry {} in position #{} is treated as a standard component.'.format(name, s + 1))
                rows_netlist.append(add_standard_component(name, nodes, value))
            elif type == 'stimulus-controlled component':
                if name == None or nodes == None or value == None:
                    raise Exception('Netlist component in position #{} is of type {} and requires name, nodes, and value.'.format(s+1, type))
                if verbose: print('Netlist entry {} in position #{} is treated as a stimulus-controlled component.'.format(name, s + 1))
                rows_netlist.append(add_stimulus_controlled_component(name, nodes, value, output_path = current_path))
            elif type == 'pulsed-source component':
                if name == None or nodes == None or value == None:
                    raise Exception('Netlist component in position #{} is of type {} and requires name, nodes, and value.'.format(s+1, type))
                if verbose: print('Netlist entry {} in position #{} is treated as a pulsed-source component.'.format(name, s + 1))
                rows_netlist.append(add_pulsed_source_component(name, nodes, value))
            elif type == 'controlled-source component':
                if name == None or nodes == None or value == None:
                    raise Exception('Netlist component in position #{} is of type {} and requires name, nodes, and value.'.format(s+1, type))
                if verbose: print('Netlist entry {} in position #{} is treated as a controlled-source component.'.format(name, s + 1))
                rows_netlist.append(add_controlled_source_component(name, nodes, value))
            elif type == 'nonlinear-dependent-source component':
                if name == None or nodes == None or value == None:
                    raise Exception('Netlist component in position #{} is of type {} and requires name, nodes, and value.'.format(s+1, type))
                if verbose: print('Netlist entry {} in position #{} is treated as a controlled-source component.'.format(name, s + 1))
                rows_netlist.append(add_nonlinear_source_component(name, nodes, value))
            elif type == 'transient-source component':
                if name == None or nodes == None or value == None:
                    raise Exception('Netlist component in position #{} is of type {} and requires name, nodes, and value.'.format(s+1, type))
                if verbose: print('Netlist entry {} in position #{} is treated as a transient-source component.'.format(name, s + 1))
                rows_netlist.append(add_transient_source_component(name, nodes, value))
            elif type == 'parametrized component':
                if name == None or nodes == None or value == None:
                    raise Exception('Netlist component in position #{} is of type {} and requires name, nodes, and value.'.format(s+1, type))
                if verbose: print('Netlist entry {} in position #{} is treated as a parametrized component.'.format(name, s + 1))
                rows_netlist.append(add_parametrized_component(name, nodes, value, parameters))
            else:
                raise Exception ('Netlist entry {} in position #{} has an unknown type: {}.'.format(name, s+1, type))

        # Prepare options - Simulation options
        rows_options = []
        options = self.circuit_data.Options.options_simulation

        keywords_timeInt = ['METHOD', 'RELTOL', 'ABSTOL', 'RESTARTSTEPSCALE'] # Not complete list, but most used
        keywords_NonLinSolv = ['NLSTRATEGY', 'SEARCHMETHOD', 'CONTINUATION', 'RELTOL', 'ABSTOL', 'DELTAXTOL', 'RHSTOL']
        keywords_LinSolv = ['type']

        if options:
            # Add comment and .OPTIONS command before the first entry
            rows_options.append(add_comment('**** Simulation parameters ****'))  # Add header of this section

            overlap_timeInt = [i for i in keywords_timeInt if i in list(options.keys())]
            overlap_NonLinSolv = [i for i in keywords_NonLinSolv if i in list(options.keys())]
            overlap_LinSolv = [i for i in keywords_LinSolv if i in list(options.keys())]

            if overlap_timeInt:
                rows_options.append('.OPTIONS TIMEINT')  # Add header of this section
                # Add option entries
                for name in overlap_timeInt:
                    rows_options.append(add_option(name, options[name]))
            if overlap_NonLinSolv:
                rows_options.append('.OPTIONS NONLIN')  # Add header of this section
                # Add option entries
                for name in overlap_NonLinSolv:
                    rows_options.append(add_option(name, options[name]))
            if overlap_LinSolv:
                rows_options.append('.OPTIONS LINSOL')  # Add header of this section
                # Add option entries
                for name in overlap_LinSolv:
                    rows_options.append(add_option(name, options[name]))


        # Prepare analysis settings
        rows_analysis = []
        analysis_type = self.circuit_data.Analysis.analysis_type
        if analysis_type == 'transient':
            # Unpack inputs
            time_start = self.circuit_data.Analysis.simulation_time.time_start
            time_end = self.circuit_data.Analysis.simulation_time.time_end
            min_time_step = self.circuit_data.Analysis.simulation_time.min_time_step
            time_schedule = self.circuit_data.Analysis.simulation_time.time_schedule
            # Check inputs
            if time_start == None:
                time_start = '0'
                if verbose: print('Parameter time_start set to {} by default.'.format(time_start))
            if not time_end:
                raise Exception('When "transient" analysis is selected, parameter Analysis.simulation_time.time_end must be defined.')
            if not min_time_step:
                if verbose: print('Parameter min_time_step was missing and it will not be written.')
            # Add analysis entry
            rows_analysis.append(add_transient_analysis(time_start, time_end, min_time_step))
            # If defined, add time schedule (varying minimum time stepping) entry
            if time_schedule and len(time_schedule) > 0:
                rows_analysis.append(add_transient_time_schedule(time_schedule))
        elif analysis_type == 'frequency':
            # Unpack inputs
            frequency_step = self.circuit_data.Analysis.simulation_frequency.frequency_step
            frequency_points = self.circuit_data.Analysis.simulation_frequency.frequency_points
            frequency_start = self.circuit_data.Analysis.simulation_frequency.frequency_start
            frequency_end = self.circuit_data.Analysis.simulation_frequency.frequency_end
            # Check inputs
            if frequency_step not in ['DEC','LIN','OCT']:
                raise Exception('Frequency step in AC analysis has to be one of [DEC,LIN,OCT]')
            if 'Hz' not in frequency_start:
                frequency_start = str(frequency_start)+'Hz'
                if verbose: print('No unit found in AC analysis starting frequency. Added unit Hz')
            if 'Hz' not in frequency_end:
                frequency_end = str(frequency_end)+'Hz'
                if verbose: print('No unit found in AC analysis last frequency. Added unit Hz')
            if not frequency_step or not frequency_start or not frequency_end or not frequency_points:
                raise Exception('A parameter for AC analysis is missing.')
            # Add analysis entry
            rows_analysis.append(add_AC_analysis(frequency_step, frequency_points, frequency_start, frequency_end))
        elif analysis_type == None:
            pass  # netlists can exist that do not have analysis set (for example, it could be defined in an auxiliary file)
        # TODO: DC analysis
        # TODO: parametric analysis. EXAMPLE: .STEP PARAM C_PARALLEL LIST 100n 250n 500n 750n 1u
        else:
            raise Exception('Analysis entry has an unknown type: {}.'.format(analysis_type))

        # Prepare post-processing settings
        rows_post_processing = []
        probe_type = self.circuit_data.PostProcess.probe.probe_type
        probe_variables = self.circuit_data.PostProcess.probe.variables
        if probe_type:
            rows_post_processing.append(add_probe(probe_type, probe_variables, self.circuit_data.Analysis.analysis_type,
                                                  os.path.join(current_path, self.circuit_data.GeneralParameters.circuit_name)))

        # Prepare file end
        rows_file_end = [add_end_file()]

        # Assemble all rows to write
        rows_to_write = \
            row_title + \
            rows_header + \
            rows_libraries + \
            rows_global_parameters + \
            rows_initial_conditions + \
            rows_netlist + \
            rows_options + \
            rows_analysis + \
            rows_post_processing + \
            rows_file_end

        # Write netlist file
        with open(full_path_file_name, 'w') as f:
            for row in rows_to_write:
                if verbose: print(row)
                f.write(row)
                f.write('\n')

        # Display time stamp
        time_written = datetime.datetime.now()
        if verbose:
            print(' ')
            print('Time stamp: ' + str(time_written))
            print('New file ' + full_path_file_name + ' generated.')


    def readFromYaml(self, full_path_file_name: str, verbose: bool = False):
        if isinstance(full_path_file_name, Path):
            full_path_file_name = str(full_path_file_name)
        # Load yaml keys into DataModelCircuit dataclass
        with open(full_path_file_name, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            self.circuit_data = DataModelCircuit(**dictionary_yaml)
            for key in dictionary_yaml['Netlist'].keys():
                new_Component = Component(**dictionary_yaml['Netlist'][key])
                self.circuit_data.Netlist.__setattr__(key, new_Component)
        if verbose:
            print('File ' + full_path_file_name + ' read.')


    def write2yaml(self, full_path_file_name: str, verbose: bool = False):
        '''
        ** Write netlist to yaml file **
        :param full_path_file_name:
        :param verbose:
        :return:
        '''
        # This hard-coded list defines the keys that will NOT be written in a single row in the output yaml file
        list_exceptions = [
            'additional_files',
            'files_to_include',
            'stimulus_files',
            'component_libraries',
            'variables',
            ]

        all_data_dict = {**self.circuit_data.dict()}
        dict_to_yaml(all_data_dict, full_path_file_name, list_exceptions=list_exceptions)
        if verbose:
            print('New file ' + full_path_file_name + ' generated.')


    def copy_additional_files(self, flag_translate: bool = False, verbose: bool = False):
        '''
            Copy additional files
        :return: Number of copied files
        '''
        for file_to_copy in self.circuit_data.GeneralParameters.additional_files+self.circuit_data.Stimuli.stimulus_files:
            if not os.path.isabs(file_to_copy) and self.path_input:
                # If the provided path is relative, use the path_input as the root folder (if available)
                file_to_copy_relative = os.path.join(self.path_input, file_to_copy)
                file_to_copy = file_to_copy_relative
                if verbose:
                    print('Relative path changed from {} to {}.'.format(file_to_copy, file_to_copy_relative))

            file_name = ntpath.basename(file_to_copy)
            file_to_write = os.path.join(self.output_path, file_name)
            if os.path.isfile(os.path.join(file_to_copy)):
                if verbose: print('File {} exists'.format(file_to_copy))
            else:
                if verbose: print('File {} does not exist. Skipped.'.format(file_to_copy))
                continue
            if os.path.isdir(self.output_path):
                if verbose: print('Dir {} exists'.format(self.output_path))
            else:
                if verbose: print('Dir {} does not exist. Skipped.'.format(self.output_path))
                continue
            if flag_translate and str(file_to_copy).endswith('.lib'):
                ## TODO: Temporary fix, until merged libraries!
                if 'converter' in str(file_to_copy):
                    file_to_copy = list(file_to_copy)
                    file_to_copy.insert(-4, '_XYCE')
                    file_to_copy = ''.join(file_to_copy)
                translate_library_PSPICE_2_XYCE(file_to_copy, file_to_write.replace('PSPICE','XYCE'))
            elif flag_translate and str(file_to_copy).endswith('.stl'):
                # path_stl = str(Path(file_to_write+'/..').resolve())
                path_stl = str(Path(file_to_write+'/..'+'/Stimulus').resolve())
                if not os.path.exists(path_stl):
                    os.mkdir(path_stl)
                translate_stimulus('all', file_to_copy, path_output=path_stl)
            else:
                shutil.copyfile(Path(file_to_copy), Path(file_to_write))

            if verbose:
                print('Additional file copied from {} to {}.'.format(file_to_copy, file_to_write))
        return len(self.circuit_data.GeneralParameters.additional_files)


    def resolve_paths_netlist(self, full_path_file_name: str):
        '''
        Helper function that resolves the library paths to the new, translated versions.

        :param full_path_file_name: Name of the circuit file
        :return:
        '''
        for i in range(len(self.circuit_data.Libraries.component_libraries)):
            file_name = ntpath.basename(self.circuit_data.Libraries.component_libraries[i])
            self.circuit_data.Libraries.component_libraries[i] = str(Path(os.path.join(self.output_path,file_name)).resolve())

        self.write2XYCE(full_path_file_name)

        return


#######################  Helper functions - START  #######################
def add_comment(text: str):
    ''' Format comment row '''
    if text[0] == '*':
        return text  # If the input string starts with a "*", leave it unchanged (it is already a comment)
    formatted_text = '* ' + text
    return formatted_text


def add_library(text: str):
    ''' Format library row '''
    formatted_text = '.INCLUDE \"' + text + '\"'
    return formatted_text


def add_initial_condition(name: str, value: str):
    ''' Format initial condition row '''
    formatted_text = '.IC ' + name + ' ' + str(value)
    return formatted_text


def add_global_parameter(name: str, value: str):
    ''' Format global parameters row '''
    formatted_text = '+ ' + name + '={' + str(value) + '}'
    return formatted_text


def add_standard_component(name: str, nodes: list, value: str):
    ''' Format standard component netlist row '''
    str_nodes = " ".join(nodes)  # string with space-separated nodes
    formatted_text = name + ' ' + str_nodes + ' ' + '{' + str(value) + '}'
    return formatted_text


def add_nonlinear_source_component(name: str, nodes: list, value: str):
    ''' Format nonlinear-source component netlist row '''
    str_nodes = " ".join(nodes)  # string with space-separated nodes
    formatted_text = name + ' ' + str_nodes + ' ' + str(value)
    return formatted_text


def add_controlled_source_component(name: str, nodes: list, value: str):
    ''' Format controlled-source component netlist row '''
    str_nodes = " ".join(nodes)  # string with space-separated nodes
    str_stimulus = 'VALUE ' + '{' + value + '}'
    formatted_text = name + ' ' + str_nodes + ' ' + str_stimulus
    return formatted_text


def add_stimulus_controlled_component(name: str, nodes: list, value: str, output_path = ''):
    ''' Format stimulus-controlled component netlist row '''
    str_nodes = " ".join(nodes)  # string with space-separated nodes
    if len(value.split(' '))==1:
        output_path = str(output_path).replace(os.sep, '/')
        str_stimulus = 'PWL FILE ' + output_path + '/Stimulus/' + value + '.csv'
    else:
        str_stimulus = 'PWL ' + value
    formatted_text = name + ' ' + str_nodes + ' ' + str_stimulus
    return formatted_text


def add_pulsed_source_component(name: str, nodes: list, value: str):
    ''' Format stimulus-controlled component netlist row '''
    str_nodes = " ".join(nodes)  # string with space-separated nodes
    str_stimulus = 'PULSE ' + value
    formatted_text = name + ' ' + str_nodes + ' ' + str_stimulus
    return formatted_text

def add_option(name: str, value: str):
    ''' Format option row '''
    formatted_text = '+ ' + name + '=' + value
    return formatted_text


def add_transient_source_component(name: str, nodes: list, value: str):
    ''' Format controlled-source component netlist row '''
    str_nodes = " ".join(nodes)  # string with space-separated nodes
    str_stimulus = 'AC ' + '{' + value + '}'
    formatted_text = name + ' (' + str_nodes + ') ' + str_stimulus
    return formatted_text


def add_parametrized_component(name: str, nodes: list, value: str, parameters: dict):
    ''' Format parametrized component netlist row '''
    str_nodes = " ".join(nodes)  # string with space-separated nodes
    formatted_component = name + ' ' + str_nodes + ' ' + value  # First row, which defines the component
    if parameters:
        formatted_component = formatted_component + '\n'
        formatted_parameters = '+ PARAMS:'  # First part of the string in the second row, which defines the component parameters
        for name_parameters, value_parameters in parameters.items():
            formatted_parameters = formatted_parameters + ' ' + name_parameters + '={' + value_parameters + '}'

        # Make sure the maximum number of characters in each row does not exceed 132, which is the maximum that XYCE supports
        N_MAX_CHARS_PER_ROW = 130
        formatted_parameters = textwrap.fill(formatted_parameters, N_MAX_CHARS_PER_ROW)
        formatted_parameters = formatted_parameters.replace('\n', '\n+ ')  # Add "+ " at the beginning of each new line
    else:
        formatted_parameters = ''  # If no parameters are defined, empty string

    formatted_text = formatted_component + formatted_parameters  # Concatenate the two rows
    return formatted_text


def add_transient_analysis(time_start, time_end, min_time_step = None):
    ''' Format transient analysis row '''
    formatted_text = '.TRAN ' + str(time_start) + ' ' + str(time_end)
    if not min_time_step == None:
        formatted_text = formatted_text + ' ' + str(min_time_step)
    return formatted_text


def add_AC_analysis(frequency_step, frequency_points, frequency_start, frequency_end):
    ''' Format transient analysis row '''
    formatted_text = f'.AC {frequency_step} {str(int(frequency_points))} {str(frequency_start)} {str(frequency_end)}'
    return formatted_text


def add_transient_time_schedule(time_schedule):
    ''' Format transient time schedule rows '''
    # If time_schedule is not defined, output will be None
    if time_schedule == None or len(time_schedule) == 0:
        return None

    formatted_text = '+ {SCHEDULE(\n'
    for time_window_start, time_step_in_window in time_schedule.items():
        if time_window_start == list(time_schedule.keys())[-1]:
            formatted_text = formatted_text + '+ ' + time_window_start + ', ' + time_step_in_window + '\n'  # the last entry must not have the comma
        else:
            formatted_text = formatted_text + '+ ' + time_window_start + ', ' + time_step_in_window + ',' + '\n'
    formatted_text = formatted_text + '+)}'
    return formatted_text


def add_probe(probe_type: str, probe_variables: list, analysis_type: str, csd_path: str):
    ''' Format probe row '''
    if analysis_type=='frequency':
        type = 'AC'
    elif analysis_type=='transient':
        type = 'TRAN'
    if probe_type == 'standard' or probe_type == 'CSDF':
        formatted_text = f'.PRINT {type} FORMAT=PROBE' + f' FILE={csd_path}.csd'
    else:
        raise Exception('Probe entry has an unknown or not implemented type: {}.'.format(probe_type))

    for var in probe_variables:
        var = var.replace('.',':').upper()
        formatted_text = formatted_text + '\n' + '+ ' + var
    return formatted_text


def add_end_file():
    formatted_text = '.END'
    return formatted_text


def CompareXYCEParameters(fileA, fileB):
    '''
        Compare all the variables imported from two XYCE netlists
    '''

    pp_a = ParserXYCE(None)
    pp_a.read_netlist(fileA, verbose=False)
    pp_b = ParserXYCE(None)
    pp_b.read_netlist(fileB, verbose=False)
    print("Comparing File A: ({}) and File B: ({})".format(fileA, fileB))

    flag_equal = pp_a.circuit_data == pp_b.circuit_data
    return flag_equal


def translate_library_PSPICE_2_XYCE(in_file_library: str, out_file_library: str, verbose: bool = False):
    """
    Helper function, that can translate a whole library file from PSPICE syntax to XYCE syntax

    :param in_file_library: Name of the input library
    :param out_file_library: Path to the translated, output library
    :param verbose:
    :return:
    """
    output_path = str(Path(out_file_library).parent.absolute())
    with open(in_file_library) as f:
        lines = f.readlines()
        flag_inModel = 0
        flag_inSubckt = 0
        idx_start = []
        idx_end = []
        for i in range(len(lines)):
            if lines[i].casefold().startswith('.subckt') and not flag_inSubckt and not flag_inModel:
                flag_inSubckt = 1
                idx_start_s = i
            elif flag_inSubckt and lines[i].casefold().startswith('.ends'):
                flag_inSubckt = 0
                idx_end.append(i)
                idx_start.append(idx_start_s)
            if lines[i].casefold().startswith('.model') and not flag_inModel and not flag_inSubckt:
                flag_inModel = 1
                idx_start_m = i
            elif flag_inModel and not lines[i].startswith('+'):
                flag_inModel = 0
                idx_end.append(i)
                idx_start.append(idx_start_m)
        if flag_inSubckt or flag_inModel:
            raise Exception("Couldn't find a .ends. Please check.")
        for i in range(len(idx_start)):
            test = lines[idx_start[i]:idx_end[i]+1]
            old_model = ''.join(lines[idx_start[i]:idx_end[i]+1]).replace('\t',' ')
            new_model, flag_Added = translate_model_PSPICE_2_XYCE(old_model, output_path)
            new_model = new_model.split('\n')
            new_model = [x+'\n' for x in new_model]
            lines[idx_start[i]:idx_end[i]+1+flag_Added] = new_model[:-1]

        with open(out_file_library, 'w') as f:
            for line in lines:
                f.write(line)
            if verbose: print('Library translated.')
    return


def translate_model_PSPICE_2_XYCE(model: str, output_path: str = ''):
    """
    Function that converts a PSPICE model to a XYCE model

    :param model: str, containing the whole model as a string, lines seperated by \n
    :rtype: str, the changed model as a str
    """

    model_split = model.split('\n')

    list_possible_components = ['r','l','c','x','k','d','p','o','s','w','v','i']
    list_possible_sources = ['v','i']
    list_possible_ABM = ['e','f','g','h','b']

    flag_inModel = False
    flag_Added = 0

    for i in range(len(model_split)):
        line = model_split[i].replace('\t',' ')
        if not line or line==' ':
            flag_inModel = False
            continue
        if line[0]==' ':
            p = 0
            while line[p]==' ':
                p=p+1
            line = line[p:]
        if flag_inModel and line[0]!='+':
            flag_inModel = False
        if line[0].casefold() in list_possible_sources and 'STIMULUS' in line:
            # Stimulus controlled sources are PWL controlled sources in XYCE. The line needs to be translated and
            # the stimulus needs to be imported as a csv/txt file
            line = translate_stimulus_line(line, output_path)
        elif line[0].casefold() in list_possible_sources and 'PULSE' in line:
            # If the PULSE function is defined, it needs to be enclosed in brackets in XYCE
            line_split = line.split('PULSE')
            value = line_split[-1]
            line_split = line_split[0].split(' ')
            line_split = [l.replace('(', '').replace(')', '') for l in line_split if l]
            line_split.append('PULSE'+value)
            line = ' '.join(line_split)
        elif line[0].casefold() in list_possible_ABM:
            # If the line is an ABM element, the split has to be done on the keyword, such that the brackets
            # are not removed within possible functions in the value
            if 'VALUE' in line:
                line_split = line.split('VALUE')
                value = 'VALUE'+line_split[-1]
            elif 'TABLE' in line:
                # PSPICE & XYCE difference: XYCE requires the table pairs to be seperated by commas
                # this bulky code part checks the string and inserts a ',' inbetween all pairs
                line_split = line.split('TABLE')
                value = 'TABLE' + line_split[-1][1:]
                try:
                    idx_eq = value.index('}')
                except:
                    raise Exception('Known issue! Please provide the Table function in a single row!')
                value = value[:idx_eq+1]+'='+value[idx_eq+1:]
                val_split = value.split(' ')
                str_val = val_split[0]
                for j in range(1,len(val_split)):
                    if not val_split[j-1].endswith(')') and \
                            not val_split[j-1].endswith('=') and \
                            not val_split[j-1]==',' and \
                            not val_split[j-1]=='' and val_split[j]!=')':
                        str_val = str_val + ',' + val_split[j]
                    else:
                        str_val = str_val + val_split[j]
                value = str_val
            else:
                line_split = line.split(' ')
                value = line_split[-1]
                line_split = [x+' ' for x in line_split]


            line = ''.join(line_split[:-1])
            line_split = line.split(' ')
            line_split_eff = line_split[:-1]
            line_split_eff = [l.replace('(', '').replace(')', '') for l in line_split_eff if l]
            line_split[:-1] = line_split_eff
            line = ' '.join(line_split)+' '+value
        elif line.startswith('.model') or line.startswith('.MODEL') or flag_inModel:
            # In XYCE models, the parameters are not allowed to be seperated by commas
            flag_inModel = True
            line = line.replace(',', '')
            if line.replace('\n', '').replace('\t', '').replace(' ', '')[-1].casefold() == 'd':
                # Diode models in XYCE need to be specified to be Level = 2 (PSPICE implementation)
                line = line + '\n+ LEVEL = 2'
                flag_Added = flag_Added +1
        elif line[0].casefold() in list_possible_components:
            # Nodes in XYCE are not allowed to be hold in brackets
            if '{' in line:
                line = list(line)
                p = [x.replace(' ', '') for x in line[line.index('{'):line.index('}') + 1]]
                line[line.index('{'):line.index('}') + 1] = p
                line = ''.join(line)
            line_split = line.replace('\t',' ').split(' ')
            line_split_eff = line_split[:-1]
            line_split_eff = [l.replace('(','').replace(')','') for l in line_split_eff if l]
            line_split[:-1] = line_split_eff
            line = ' '.join(line_split)
        model_split[i] = line
    model = '\n'.join(model_split)
    return model, flag_Added


def translate_stimulus_line(line: str, origin_stl: str = ''):
    '''
    Helper function that translates a stimulus controlled source component into a PWL
    :param line:
    :return:
    '''
    line_split = line.split('=')
    line_nodes = line_split[0].split(' ')
    line_nodes = [x.replace('(', '').replace(')', '') for x in line_nodes if x]
    in_line = ' '.join(line_nodes[:-1])

    if origin_stl:
        origin_stl = origin_stl.replace(os.sep, '/')+'/'+'Stimulus'+'/'+line_split[-1][1:] + '.csv'
    else:
        origin_stl = line_split[-1][1:] + '.csv'
    new_stl_line = in_line + ' PWL FILE ' + origin_stl
    return new_stl_line


def translate_stimulus(stl_name, stl_file: str, path_output: str = ''):
    '''
    Function that translates a single, list of stimuli or all stimuli in the file
    (if stl_name is only a single string, if it's a list or if the keyword 'all' is provided)
    to an each independent .csv file, which can be used by PWL controlled XYCE sources
    :param stl_name:
    :param stl_file:
    :param path_output:
    :return:
    '''
    with open(stl_file, 'r') as f:
        lines = f.readlines()

    if stl_name=='all':
        stl_name = []
        for line in lines:
            if '.STIMULUS' in line:
                line_split = line.split(' ')
                stl_name.append(line_split[1])

    if isinstance(stl_name, str):
        stl_name = [stl_name]

    for k in range(len(stl_name)):
        stl = stl_name[k]
        time = []
        value = []
        flag_inStl = False
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith(f'.STIMULUS {stl}') and not flag_inStl:
                flag_inStl = True
                continue
            if '+' in line[:10] and '(' in line[:10] and flag_inStl:
                line = line.replace(' ','').replace('s','').replace('V','').replace('A','').replace('(','').replace(')','').replace('+','').replace('\n','').replace('\t','')
                line_split = line.split(',')
                time.append(float(line_split[0]))
                value.append(float(line_split[1]))
            if (not line or line.startswith(f'.STIMULUS') or line=='\n') and (flag_inStl):
                flag_inStl = False
                break

        df_stl = pd.DataFrame.from_dict({'Time': time,'Value': value})

        if path_output:
            outputfile = os.path.join(path_output,stl+'.csv')
        else:
            outputfile =  os.path.join(os.getcwd(),stl+'.csv')
        df_stl.to_csv(outputfile, header=False, index=False )
        # print(f'{outputfile} was translated.')
    return


#######################  Helper functions - END  #######################
