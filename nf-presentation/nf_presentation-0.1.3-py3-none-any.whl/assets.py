import importlib.resources as pkg_resources
from .settings import RFS_LOGO_FILE_NAME

def get_rfs_logo():
    return pkg_resources.open_binary(__package__, RFS_LOGO_FILE_NAME)

def get_test_data(short=True) -> dict:
    resource_path= 'test_data_short.json' if short else 'test_data.json'
    return pkg_resources.open_text(__package__, resource_path,encoding='utf8')

