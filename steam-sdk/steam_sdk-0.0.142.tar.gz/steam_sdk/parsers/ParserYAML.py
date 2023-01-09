import ruamel.yaml
import numpy as np


def yaml_to_data(full_file_path, data_class=dict, with_comments=False):
    """
    Loads content of yaml file to data class. If data class not provided it loads into dictionary.
    :param full_file_path: full path to yaml file with .yaml extension
    :param data_class: data class to load yaml file to, if empty yaml is loaded as python dictionary (dict)
    :param with_comments: if set to true, comments in the yaml file are preserved - this is only a placeholder as the functionality for doing this is note yet implemented
    """

    with open(full_file_path, 'r') as stream:

        if with_comments:
            yaml = ruamel.yaml.YAML(typ='rt')
        else:
            yaml = ruamel.yaml.YAML(typ='safe', pure=True)
        yaml_str = yaml.load(stream)
    return data_class(**yaml_str)


def dict_to_yaml(data_dict, name_output_file: str, list_exceptions: list = [], with_comments=False):
    """
    Write a dictionary to yaml with pre-set format used across STEAM yaml files.
    In particular:
    - keys order is preserved
    - lists are written in a single row
    :param data_dict: python dictionary to write
    :type data_dict: dict
    :param name_output_file: Full path to yaml file to write
    :type name_output_file: str
    :param list_exceptions: List of strings defining keys that will not be written in a single row
    :type list_exceptions: list
    :param with_comments: If true, preserves comments in the yaml file on save. Needs to be used in combination with yaml_to_data_class flag with_comments=True
    :type with_comments: bool
    :return: Nothing, writes yaml file to disc
    :rtype: None
    """
    #################################################################################################
    # Helper functions
    def my_represent_none(obj, *args):
        '''
            Change data representation from empty string to "null" string
        '''
        return obj.represent_scalar('tag:yaml.org,2002:null', 'null')

    def flist(x):
        '''
            Define a commented sequence to allow writing a list in a single row
        '''
        retval = ruamel.yaml.comments.CommentedSeq(x)
        retval.fa.set_flow_style()  # fa -> format attribute
        return retval

    def list_single_row_recursively(data_dict: dict, list_exceptions: list = []):
        '''
            Write lists in a single row
            :param data_dict: Dictionary to edit
            :param list_exceptions: List of strings defining keys that will not be written in a single row
            :return:
        '''
        for key, value in data_dict.items():
            if isinstance(value, list) and (not key in list_exceptions):
                data_dict[key] = flist(value)
            elif isinstance(value, np.ndarray):
                data_dict[key] = flist(value.tolist())
            elif isinstance(value, dict):
                data_dict[key] = list_single_row_recursively(value, list_exceptions)

        return data_dict

    #################################################################################################

    # Set up ruamel.yaml settings
    if with_comments:
        ruamel_yaml = ruamel.yaml.YAML(typ='rt')
    else:
        ruamel_yaml = ruamel.yaml.YAML()
    ruamel_yaml.width = 268435456  # define the maximum number of characters in each line
    ruamel_yaml.default_flow_style = False
    ruamel_yaml.emitter.alt_null = 'Null'
    ruamel_yaml.representer.add_representer(type(None), my_represent_none)

    # Write lists in a single row
    data_dict = list_single_row_recursively(data_dict, list_exceptions=list_exceptions)

    # Write yaml file
    with open(name_output_file, 'w') as yaml_file:
        ruamel_yaml.dump(data_dict, yaml_file)
