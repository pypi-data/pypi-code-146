import os
import numpy as np
import pandas as pd
from pathlib import Path
import ruamel.yaml
import csv
from steam_sdk.parsers.ParserYAML import dict_to_yaml





def getSpecificSignalCSV(path_sim, model_name, simNumber, list_Signals):

    simulationSignalsToPlot = pd.DataFrame()

    for i in range(len(simNumber)):
        for n in range(len(list_Signals)):
            path_simulationSignals = os.path.join(path_sim + str(simNumber[i]) + '.csv')
            # Importing csv
            simulationSignals = np.genfromtxt(path_simulationSignals, dtype=str, delimiter=',', skip_header=0)
            simulationSignals = simulationSignals.tolist()
            simulationSignals = pd.DataFrame(simulationSignals)
            simulationSignals.set_index(0, inplace=True)
            simulationSignal = list(simulationSignals.loc[list_Signals[n]])
            simulationSignal.insert(0, list_Signals[n] + '_' + str(simNumber[i]))
            simulationSignal = [simulationSignal]
            temp_frame = pd.DataFrame(simulationSignal)
            temp_frame.set_index(0, inplace=True)
            simulationSignalsToPlot = simulationSignalsToPlot.append(temp_frame)

    return simulationSignalsToPlot


def get_signals_from_csv(full_name_file: str, list_signals):
    '''
    Reads a csv file and returns a dataframe with the selected signals
    :param full_name_file: full path to the csv file
    :param list_signals: list of signals to read
    :return: dataframe with the selected signals
    '''

    if type(list_signals) == str: list_signals = [list_signals]           # If only one signal is passed as an argument, make it a list

    all_signals_df = pd.read_csv(full_name_file)                          # read file into a dataframe
    all_signals_df.columns = all_signals_df.columns.str.replace(' ', '')  # eliminate whitespaces from the column names
    list_signals = [x.replace(' ', '') for x in list_signals]             # eliminate whitespaces from the signal names as well
    return all_signals_df[list_signals]


def load_global_parameters_from_csv(filename: str, circuit_name: str, steam_models_path: str, case_model: str, flag_write_file:bool=False):
    '''
        Reads a csv file and circuit name and checks that the global parameters for the circuit are consistent with the csv file. If not, changes are made in the circuit parameters
        :param filename: full path to the csv file
        :param circuit_name: circuit name eg. RCS.A12B1
        :param steam_models_path: path to steam models
        :param case_model: folder within steam models eg. circuit or magnet
        :param flag_write_file: whether changes are made or not
        :param out_file: changed yaml file

        :return: out_file
    '''
    circuit_param=[]
    param_names=[]

    circuit_param= find_by_position(filename, 0, circuit_name)
    param_names=find_column_list(filename)
    dict_circuit = {k: v for k, v in zip(param_names, circuit_param)}
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    name = circuit_name.split('.')[0]
    path_to_model_circuit_data=os.path.join(steam_models_path,case_model+"s",name,"input","modelData_"+name+".yaml")


    with open(path_to_model_circuit_data) as fp:
        data = yaml.load(fp)

        #Write the data before change to an auto.yaml file
    path_previous_record="previous_global_param_auto.yaml"
    dict_to_yaml(data, path_previous_record)

    for key, value in dict_circuit.items():
        if key in data['GlobalParameters']['global_parameters']:
            if data['GlobalParameters']['global_parameters'][key] != value:
                print(data['GlobalParameters']['global_parameters'][key], "is different from", value)
                data['GlobalParameters']['global_parameters'][key] = value
                flag_write_file=True
    output_file=os.path.join('output', 'load_parameters_from_csv','modelData_'+circuit_name+".yaml")
    with open('modelData_'+circuit_name+".yaml", 'w') as f:
        yaml.dump(data, f)
    out_file=os.path.join(os.getcwd(),'modelData_'+circuit_name+".yaml")
    #yaml.dump(data, sys.stdout)
    return out_file


###### HELPER FUNCTION #####
def find_by_position(filename, idx, value):
    with open(filename) as f:
        reader = csv.reader(f)
        row = next((item for item in reader if item[idx] == value), None)

    return row


def find_column_list(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        row1 = next(reader)
    return row1
############################


# def gettime_vectorCSV(path_sim, simNumber):
#
#     path_simulationSignals = os.path.join(path_sim + str(simNumber[0]) + '.csv')
#     # Importing csv
#     simulationSignals = np.genfromtxt(path_simulationSignals, dtype=str, delimiter=',', skip_header=0)
#     simulationSignals = simulationSignals.tolist()
#     simulationSignals = pd.DataFrame(simulationSignals)
#     simulationSignals.set_index(0, inplace=True)
#     simulationSignal = list(simulationSignals.loc['ï»¿time_vector'])
#     simulationSignal.insert(0, 'time_vector')
#     simulationSignal = [simulationSignal]
#     simulationSignalsToPlot = pd.DataFrame(simulationSignal)
#     simulationSignalsToPlot.set_index(0, inplace=True)
#     return simulationSignalsToPlot

# def writeTdmsToCsv(self, path_output: Path, dictionary: {}):
#     """
#         This function writes the signals of the signal_data dictionary of this class of a TDMS file to a specific csv file.
#         dictionary for header with names of the groups and signal that are used in the TDMS file
#         header: Groupname_signalname, ....
#     """
#     # Get signal
#     # signal_output = getspecificSignal(path_tdms, group_name, signal_name)
#     # np.savetxt(path_output, signal_output, delimiter=",")
#     # headers, units,...
#
#     header = []
#     for group in dictionary.keys():
#         for channel in dictionary[group]:
#             header.append(group + '_' + channel)
#
#     tdms_df = pd.DataFrame(self.signal_data)
#     tdms_df.to_csv(path_output, header=header, index=False)