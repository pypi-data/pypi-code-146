import configparser
import importlib.resources

config = configparser.ConfigParser()
config_file = importlib.resources.read_text('dry_scraper', 'config.ini')
config.read_string(config_file)
