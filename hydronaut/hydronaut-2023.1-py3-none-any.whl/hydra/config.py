#!/usr/bin/env python3
'''
Structured configs for Hydra and associated helper functions.
'''

import logging
import os
import pathlib
import platform
from dataclasses import dataclass, field
from typing import Optional, Any

from omegaconf import DictConfig, OmegaConf
import hydra
from hydra.utils import to_absolute_path
from hydra.types import RunMode
from hydra.core.config_store import ConfigStore
from hydra.core.global_hydra import GlobalHydra
from hydra.core.hydra_config import HydraConfig
import mlflow

from hydronaut.file import save_config
from hydronaut.hydra.resolvers import reregister


HYDRA_VERSION_BASE = '1.2'
LOGGER = logging.getLogger(__name__)


# This is not supported so use Any.
# DefaultsType = list[dict[str, str] | str]
DefaultsType = list[Any]


# In Python 3.10+ this can be a static method within HydronautConfig but for
# earlier versions this must be scoped outside of the class definition for the
# call to field().
def _get_hydronaut_defaults():
    '''
    Factory for defaults list.
    '''
    return [
        {'override /hydra/job_logging@_global_.hydra.job_logging': 'colorlog'},
        {'override /hydra/hydra_logging@_global_.hydra.hydra_logging': 'colorlog'}
    ]


@dataclass
class MLflowRunConfig:
    '''
    Parameters for mlflow.start_run(), except for experiment_id which is set
    from the experiment name. For details, see
    https://mlflow.org/docs/latest/python_api/mlflow.html
    '''
    #  experiment_id: Optional[str] = None
    run_id: Optional[str] = None
    run_name: Optional[str] = None
    nested: bool = False
    tags: Optional[dict[str, str]] = None
    description: Optional[str] = '${experiment.description}-run_${hydra:job.name}_${hydra:job.num}'


@dataclass
class MLflowConfig:
    '''
    MLflow configuration.
    '''
    run: Optional[MLflowRunConfig] = None
    tracking_uri: Optional[str] = 'file://{wd}/mlruns'
    artifact_uri: Optional[str] = None
    registry_uri: Optional[str] = None


@dataclass
class PythonConfig:
    '''
    Pyton configuration.
    '''
    # Paths to prepend to the system path list.
    paths: Optional[list[str]] = field(default_factory=list)


@dataclass
class ExperimentConfig:
    '''
    Experiment configuration.
    '''
    name: str
    description: str
    exp_class: str
    params: Optional[dict[str, Any]]
    python: Optional[PythonConfig] = None
    mlflow: Optional[MLflowConfig] = None
    defaults: Optional[DefaultsType] = field(default_factory=_get_hydronaut_defaults)


def _get_hydronaut_defaults():
    '''
    Factory for defaults list.
    '''
    return ['experiment/hf_experiment']


@dataclass
class HydronautConfig:
    '''
    Common Hydronaut configuration.
    '''
    defaults: Optional[DefaultsType] = field(default_factory=_get_hydronaut_defaults)
    #  experiment: ExperimentConfig


def _get_unique_identifier() -> str:
    '''
    Get a unique process identifier.

    Returns:
        A string with the format "<node>:<pid>".
    '''
    return f'{platform.node()}:{os.getpid()}'


def _reinitialize_from_environment() -> DictConfig:
    '''
    Re-initialize the Hydra configuration in a subprocess from environment
    variables if uninitialized.

    Returns:
        A Hydra config object.
    '''
    LOGGER.debug('Attempting to re-initialize Hydra from environment variables.')

    if GlobalHydra().is_initialized():
        LOGGER.debug('Aborting re-initialization of Hydra: already initialized.')
        return

    my_uid = _get_unique_identifier()
    main_uid = os.getenv('HF_MAIN_UID')
    if my_uid == main_uid:
        LOGGER.debug('Aborting re-initialization of Hydra: current process is the main process.')
        return

    working_dir = os.getenv('HF_WORKING_DIR')
    os.chdir(working_dir)

    GlobalHydra.instance().clear()
    hydra.initialize_config_dir(
        version_base=HYDRA_VERSION_BASE,
        config_dir=os.getenv('HF_CONFIG_DIR'),
        job_name=os.getenv('HF_JOB_NAME')
    )
    cfg = hydra.compose(config_name='config', return_hydra_config=True)
    HydraConfig().set_config(cfg)


def configure_hydra(from_env: bool = False) -> None:
    '''
    Configure the config store, resolvers and global configs as necessary.

    Args:
        from_env:
            If True, re-initialize the Hydra configuration object from
            environment variables set configure_environment().
    '''
    store = ConfigStore.instance()
    store.store(name='hf_experiment', group='experiment', node=ExperimentConfig)
    store.store(name='hf_config', node=HydronautConfig)
    reregister()
    if from_env:
        _reinitialize_from_environment()


def _safe_resolve_hydra_conf(hydra_conf: DictConfig, conf: DictConfig) -> DictConfig:
    '''
    Safely resolve a Hydra configuration object. This is required for simple
    runs due to a bug in Hydra's default configuration file.

    Args:
        hydra_conf:
            The Hydra configuration object.

        conf:
            The main configuration object, required for resolving interpolations.

    Returns:
        The resolved configuration object except unresolvable interpolations
        will be left in place.
    '''
    # Create a copy to ensure that the original is not modified.
    conf = OmegaConf.create(OmegaConf.to_container(conf, resolve=False))

    # Replace the erroneous "hydra." interpolations with the "hydra:" resolver.
    text = OmegaConf.to_yaml(hydra_conf)
    text = text.replace('${hydra.', '${hydra:')
    hydra_conf = OmegaConf.create(text)

    # Integrate the configuration objects to ensure full resolution.
    conf.hydra = hydra_conf
    OmegaConf.resolve(conf)

    # Extract the Hydra configuration and return it.
    hydra_conf = conf.hydra
    OmegaConf.set_readonly(hydra_conf, True)
    return hydra_conf


def configure_environment() -> None:
    '''
    Save the current Hydra configuration to fully resolved OmegaConf files and
    set environment variables for subprocesses to re-initialize the current
    configuration.
    '''
    if not HydraConfig.initialized():
        LOGGER.error('Unable to configure environment: Hydra is not initalized')
        return

    hydra_conf = HydraConfig.get()
    job = hydra_conf.job
    if hydra_conf.mode == RunMode.MULTIRUN:
        config_dir = pathlib.Path(hydra_conf.sweep.dir) / str(job.num)
    else:
        config_dir = hydra_conf.run.dir
    config_dir = pathlib.Path(to_absolute_path(config_dir)).resolve()

    hydra_dir = config_dir / hydra_conf.output_subdir
    conf = OmegaConf.load(hydra_dir / 'config.yaml')

    # Configure MLflow
    if conf.experiment.get('mlflow') is None:
        conf.experiment.mlflow = OmegaConf.create(MLflowConfig())
    conf.experiment.mlflow.tracking_uri = mlflow.get_tracking_uri()
    conf.experiment.mlflow.artifact_uri = mlflow.get_artifact_uri()
    conf.experiment.mlflow.registry_uri = mlflow.get_registry_uri()

    active_run = mlflow.active_run()
    if active_run is not None:
        os.environ['MLFLOW_RUN_ID'] = str(active_run.info.run_id)
    else:
        LOGGER.error('no active MLflow run')

    # Save resolved versions of the current configs for subprocesses.
    config_dir /= '.hydronaut'
    config_dir.mkdir(parents=True, exist_ok=True)
    save_config(
        _safe_resolve_hydra_conf(hydra_conf, conf),
        config_dir / 'hydra.yaml',
        resolve=False,
        overwrite=False
    )
    save_config(
        conf,
        config_dir / 'config.yaml',
        resolve=True,
        overwrite=False
    )
    #  save_config(GlobalHydra().get(), config_dir / 'config.yaml', resolve=True)

    # Log Hydra configuration files.
    for hydra_config in (config_dir.parent / hydra_conf.output_subdir).glob('*'):
        mlflow.log_artifact(hydra_config, artifact_path='hydra')

    os.environ['HF_CONFIG_DIR'] = str(config_dir)
    os.environ['HF_JOB_NAME'] = str(job.name)
    os.environ['HF_WORKING_DIR'] = str(pathlib.Path.cwd())
    main_uid = os.getenv('HF_MAIN_UID')
    if main_uid is None:
        os.environ['HF_MAIN_UID'] = _get_unique_identifier()
