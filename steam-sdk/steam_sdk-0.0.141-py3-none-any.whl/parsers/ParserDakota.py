from jinja2 import Environment, FileSystemLoader

from steam_sdk.parsers import templates
from steam_sdk.data import DataDakota


class ParserDakota:
    def __init__(self, file_base_path):
        """
        Class for generating .in templates
        :param file_base_path: this is a full path to a folder with the model and includes model name, but without extension
        """
        self.file_base_path = file_base_path

    def assemble_in_file(self, template: str = None, dakota_data: DataDakota.DataDakota = None):
        """
        Generates .in file from template
        :param template: .in template file name
        :param dakota_data: Dakota data
        :return: None. Generates .in file and saves it on disk in the model folder
        """
        loader = FileSystemLoader(templates.__path__)
        env = Environment(loader=loader, variable_start_string='<<', variable_end_string='>>',
                          trim_blocks=True, lstrip_blocks=True)
        env.globals.update(len=len)
        in_template = env.get_template(template)

        auxiliary = DataDakota.Auxiliary()
        for name, var in dakota_data.study.variables.items():
            if dakota_data.study.type == 'multidim_parameter_study':
                auxiliary.partitions.append(var.data_points - 1)
            auxiliary.lower_bounds.append(var.bounds.min)
            auxiliary.upper_bounds.append(var.bounds.max)

        output_from_parsed_template = in_template.render(dd=dakota_data, aux=auxiliary)
        with open(f"{self.file_base_path}.in", "w") as tf:
            tf.write(output_from_parsed_template)


# import os
# from pathlib import Path
#
# from steam_sdk.data.DataDakota import DataDakota
# from steam_sdk.parsers.ParserYAML import yaml_to_data
#
#
# class ParserDakota:
#     """
#         Class with methods to read/write FiQuS information from/to other programs
#     """
#
#     def __init__(self, input_Dakota_data_yaml, verbose: bool = True):
#         """
#             Initialization using a BuilderDakota object containing Dakota parameter structure
#             Read the Dakota input variables from a input_Dakota_data_yaml file and parse into the object
#
#         """
#         self.dakota_data = yaml_to_data(full_file_path=input_Dakota_data_yaml, data_class=DataDakota)
#
#         if verbose:
#             print('File {} was loaded.'.format(input_Dakota_data_yaml))
#
#     def writeDakota2in(self, output_file_full_path: str, verbose: bool = False):
#         """
#         Writes the Dakota object into a respective .in file according to the format
#         """
#
#         # If the output folder is not an empty string, and it does not exist, make it
#         output_path = os.path.dirname(output_file_full_path)
#         if verbose:
#             print('output_path: {}'.format(output_path))
#         if output_path != '' and not os.path.isdir(output_path):
#             print("Output folder {} does not exist. Making it now".format(output_path))
#             Path(output_path).mkdir(parents=True)
#
#         dict_to_in(self.dakota_data.Dakota_analysis.dict(), output_file_full_path)
#
#
# def dict_to_in(data_dict, name_output_file: str):
#     """
#     Function that converts a dictionary into a .in file for Dakota
#     :param data_dict, dict - contains all keys and values
#     :param name_output_file, str - name of the .in file
#     """
#
#     def __fill_up_level(level: int, strng: str):
#         """
#         Helper function that fills up a string with a tabular, according to the level
#         """
#         filler = ''.join(map(str, ([' ']*level*4)))
#         return filler + strng
#
#     def __flatten_list(lst: list):
#         """
#         Helper function that reduces a list to a single string, separated by one space
#         """
#         lst = ["'" + x + "'" if type(x) == str else x for x in lst]
#         return ' '.join(map(str, lst))
#
#     def __construct_string(data, key):
#         """
#         Helper function that constructs a string from data values, based on the type
#         """
#         # If data value is empty/false: ignore
#         if not data[key]:
#             return ''
#
#         # If string: fill only with data value
#         if type(data[key]) == str:
#             strng = f"{key} = '{data[key]}' \n"
#         # If list: return list flattened to a single line
#         elif type(data[key]) == list:
#             strng = f"{key} = {__flatten_list(data[key])} \n"
#         # If bool: return only key, without it's value
#         elif type(data[key]) == bool:
#             strng = f"{key} \n"
#         # All other types: return key and value
#         else:
#             strng = f"{key} = {data[key]} \n"
#         # Convention: If key is marked as a type, we ignore the key and just return the value
#         if 'type' in key:
#             strng = f"{data[key]} \n"
#         return strng
#
#     # Actual function that writes the .in file
#     with open(name_output_file, 'w') as in_file:
#         # Loop through all Dakota key words
#         for key in data_dict.keys():
#             in_file.write(f'{key} \n')
#             # Loop through all sub-keys in each category
#             for subkey in data_dict[key].keys():
#                 if type(data_dict[key][subkey]) == dict:
#                     for subsubkey in data_dict[key][subkey].keys():
#                         string = __construct_string(data_dict[key][subkey], subsubkey)
#                         if string: in_file.write(__fill_up_level(2, string))
#                 else:
#                     string = __construct_string(data_dict[key], subkey)
#                     if string: in_file.write(__fill_up_level(1, string))
