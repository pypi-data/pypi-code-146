from datetime import datetime

from gl_parser.config.configuration import ConfigurationManager


class TestConfigurationManager:

    def test_build(self, output_folder):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        toml_filename = f'{timestamp}_config.toml'
        manager = ConfigurationManager(output_folder, toml_filename)
        configuration = manager.get_configuration()
        assert configuration is not None
        assert manager.config_file == output_folder / toml_filename
