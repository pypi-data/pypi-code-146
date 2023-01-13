"""An easy way to get pretrained auto models."""

import importlib
import json
import os
import requests
import sys
from zipfile import ZipFile

from .. import logger
from .auto_model import AutoModel, MandatoryConfig
from .exceptions import AutoModelError, ConfigError


def from_pretrained(resource_dir: str,
                    name: str = None,  # TODO remove me
                    version: int = 1,  # TODO remove me
                    download: bool = False,
                    **kwargs) -> AutoModel:
    """Initiate an AutoModel instance from pretrained models.

    Args:
        resource_dir:
            The root dir of the resource for setup process, i.e. parameter files.
        name:
            The name of the pretrained model.
        version:
            The version of the pretrained model.
        kwargs:
            Other keyword arguments.
    """
    if not resource_dir or not isinstance(resource_dir, str):
        raise ConfigError(f'Invalid pretrained model resource directory: {resource_dir}.')
    logger.info(f'Loading resouce from: `{resource_dir}`.')

    if download and not _is_resource_ready(resource_dir):
        _download_resource(name=name, resource_dir=resource_dir, version=version)

    if not _is_resource_ready(resource_dir):
        raise ConfigError('Failed to setup model because of incomplete context.')

    return _load_model_obj(resource_dir=resource_dir)


def _is_resource_ready(resource_dir: str) -> bool:
    """Validate if resource are ready for loading model.

    Args:
        resouce_dir:
            The directory where the resource locates.
    """
    config_file = os.path.join(resource_dir, 'config.json')
    if not os.path.isfile(config_file):
        logger.warn(f'Config file `{config_file}` is not found.')
        return False
    try:
        with open(config_file, 'r') as f:
            config_json = json.load(f)
    except json.JSONDecodeError as err:
        logger.warn('Config content is not in valid JSON format.')
        logger.exception(err)
        return False

    try:
        config = MandatoryConfig(**config_json)
    except TypeError as err:
        logger.warn('Invalid config content.')
        logger.exception(err)
        return False
    try:
        config.validate_files(resource_dir)
    except ConfigError as err:
        logger.warn('Mandatory files are missing.')
        logger.exception(err)
        return False

    return True


def _download_resource(name: str, resource_dir: str, version: int = 1):
    """Download auto model resource from model zoo.

    Args:
        name:
            The name of auto model.
        resource_dir:
            The directory where to store the resource downloaded.
        version:
            The version of auto model.
    """
    # TODO 请求 model zoo 接口，下载压缩包
    logger.info('Begin to download model resource.')
    os.makedirs(resource_dir, exist_ok=True)

    _MAP = {  # TODO use model zoo API
        ('breast_density_classification', 1): 'https://dev-sapce-1309103037.cos.ap-nanjing.myqcloud.com/tmp/breast_density_classification/res_local.zip',  # noqa
        ('skin_lesion_diagnosis', 1): 'https://dev-sapce-1309103037.cos.ap-nanjing.myqcloud.com/tmp/skin_lesion_diagnosis/res_local.zip',  # noqa
        ('endoscopic_inbody_classification', 1): 'https://dev-sapce-1309103037.cos.ap-nanjing.myqcloud.com/tmp/endoscopic_inbody_classification/res_local.zip',  # noqa
        ('breast_density_classification_fed_avg', 1): 'https://dev-sapce-1309103037.cos.ap-nanjing.myqcloud.com/tmp/breast_density_classification/res_fed_avg.zip',  # noqa
        ('skin_lesion_diagnosis_fed_avg', 1): 'https://dev-sapce-1309103037.cos.ap-nanjing.myqcloud.com/tmp/skin_lesion_diagnosis/res_fed_avg.zip',  # noqa
        ('endoscopic_inbody_classification_fed_avg', 1): 'https://dev-sapce-1309103037.cos.ap-nanjing.myqcloud.com/tmp/endoscopic_inbody_classification/res_fed_avg.zip',  # noqa
    }
    url = _MAP.get((name, version))
    if not url:
        raise AutoModelError(f'Model resource not found: `{(name, version)}`.')
    download_resp = requests.get(url, allow_redirects=True)
    package = os.path.join(resource_dir, 'res_local.zip')
    with open(package, 'wb') as f:
        f.write(download_resp.content)

    with ZipFile(package) as zf:
        zf.extractall(resource_dir)

    os.remove(package)
    logger.info('Downloading model resource complete.')


def _load_model_obj(resource_dir: str) -> AutoModel:
    """Try to load and initialize an auto model instance.

    Args:
        config:
            Auto model configuration.
        resouce_dir:
            The directory where the resource locates.
    """
    config_file = os.path.join(resource_dir, 'config.json')
    with open(config_file, 'r') as f:
        config_json = json.load(f)
    config = MandatoryConfig(**config_json)

    sys.path.insert(0, resource_dir)
    if config.entry_module:
        module_path = os.path.join(resource_dir, config.entry_module)
        logger.debug(f'{config.entry_module=}')
        logger.debug(f'{module_path=}')
        module = importlib.import_module(config.entry_module, module_path)
    else:
        model_file = os.path.join(resource_dir, config.entry_file)
        logger.debug(f'{config.entry_file=}')
        logger.debug(f'{model_file=}')
        module = importlib.import_module(config.entry_file[:-3], model_file)
    logger.debug(f'{module=}')
    model_class = getattr(module, config.entry_class)
    logger.debug(f'{model_class=}')
    model = model_class(resource_dir=resource_dir)
    logger.info('Loading pretrained model complete.')

    # remove module from sys.modules in case module name confliction
    sys.modules.pop(module.__name__)
    return model
