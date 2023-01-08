import yaml
from yaml import SafeLoader
from caddo_file_parser.settings.settings import Settings


class SettingsLoader:
    def __init__(self, settings_path=''):
        self.settings_path = settings_path

    def load(self):
        print("LOADING SETTINGS")
        self.load_settings_object()
        print()

    def read_settings_file(self):
        with open(self.settings_path) as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data

    def load_settings_object(self):
        settings_file = self.read_settings_file()
        print("Settings:")
        print(yaml.dump(settings_file, default_style=False))
        Settings.data_source_path = settings_file['data_source']['path']
        Settings.data_source_separator = settings_file['data_source']['separator']
        Settings.data_source_x_cols = settings_file['data_source']['x_columns_names']
        Settings.data_source_y_cols = settings_file['data_source']['y_columns_names']
        Settings.extraction_data_module = settings_file['extraction_data']['file_name_without_extension']
        Settings.percent_of_training_data = settings_file['model']['percent_of_training_data']
        Settings.number_of_folds = settings_file['model']['number_of_folds']
        Settings.runs = settings_file['model']['runs']
        Settings.output_file_name = settings_file['output']['file_name']
        Settings.output_separator = settings_file['output']['separator']
        Settings.folding_method = settings_file['folding']['method']
        Settings.seeds_path = settings_file['folding']['seeds']['path']
        Settings.seeds = settings_file['folding']['seeds']['write_directly']
