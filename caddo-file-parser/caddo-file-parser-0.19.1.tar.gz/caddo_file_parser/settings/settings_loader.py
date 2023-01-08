from caddo_file_parser.settings.settings import Settings


class SettingsLoader:
    def load_settings_object(self, settings_file):
        settings_data: Settings = None
        settings_data.data_source_path = settings_file['data_source']['path']
        settings_data.data_source_separator = settings_file['data_source']['separator']
        settings_data.data_source_x_cols = settings_file['data_source']['x_columns_names']
        settings_data.data_source_y_cols = settings_file['data_source']['y_columns_names']
        settings_data.extraction_data_module = settings_file['extraction_data']['file_name_without_extension']
        settings_data.percent_of_training_data = settings_file['model']['percent_of_training_data']
        settings_data.number_of_folds = settings_file['model']['number_of_folds']
        settings_data.runs = settings_file['model']['runs']
        settings_data.output_file_name = settings_file['output']['file_name']
        settings_data.output_separator = settings_file['output']['separator']
        settings_data.folding_method = settings_file['folding']['method']
        settings_data.seeds_path = settings_file['folding']['seeds']['path']
        settings_data.seeds = settings_file['folding']['seeds']['write_directly']
        return settings_data
