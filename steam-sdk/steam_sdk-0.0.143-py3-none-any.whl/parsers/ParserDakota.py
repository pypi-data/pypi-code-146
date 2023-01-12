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
