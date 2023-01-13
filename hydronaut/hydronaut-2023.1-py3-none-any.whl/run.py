#!/usr/bin/env python3
'''
Run an experiment with Hydra, Optuna and MLflow.

TODO
* Explore mlflow.autolog support in PyTorch.
'''

import importlib
import inspect
import logging
import subprocess
import sys
from typing import Any

import hydra
import mlflow

from hydronaut.experiment import Experiment
from hydronaut.hydra.config import configure_hydra, configure_environment, HYDRA_VERSION_BASE
from hydronaut.hydra.omegaconf import get
from hydronaut.mlflow import MLflowRunner
from hydronaut.paths import PathManager
from hydronaut.types import Path, OptimizationValue

LOGGER = logging.getLogger(__name__)


class Runner():
    '''
    Experiment runner.
    '''

    def __init__(self, config_subpath: Path = None) -> None:
        '''
        Args:
            config_subpath:
                The subpath to the configuration file. This is
                passed through to hydronaut.paths.get_config_path
                to get the main Hydra configuration file.
        '''
        self._path_manager = PathManager()
        self.config_subpath = config_subpath
        # The Hydra configuration object, which will be set when this is run.
        self.config = None

    def get_experiment_object(self) -> Experiment:
        '''
        Get the experiment class specified by the configuration object.

        Returns:
            The experiment instance.

        Raises:
            ImportError:
                The module could not be found.

            AttributeError:
                The module does not contain the expected class name.
        '''
        config = self.config
        exp_cls_param = config.experiment.exp_class
        exp_cls_module, exp_cls_name = exp_cls_param.split(':', 1)
        importlib.import_module(exp_cls_module)
        exp_cls = getattr(sys.modules[exp_cls_module], exp_cls_name)
        LOGGER.debug('loaded experiment class: %s', exp_cls)

        if not issubclass(exp_cls, Experiment):
            LOGGER.warning(
                'Experiment class %s.%s [%s] is not a subclass of %s.%s',
                exp_cls.__module__,
                exp_cls.__qualname__,
                inspect.getfile(exp_cls),
                Experiment.__module__,
                Experiment.__qualname__
            )
        return exp_cls(config)

    def __call__(self, *args: Any, **kwargs: Any) -> OptimizationValue:
        '''
        Run the experiment and return a value for the Optuna sweeper.

        Args:
            *args, **kwargs:
                Positional and keyword arguments passed through to the
                hydra.main function.

        Returns:
            The value to optimize.
        '''
        configure_hydra()
        config_path = self._path_manager.get_config_path(subpath=self.config_subpath)
        if not config_path.exists():
            LOGGER.error(
                # One string intentionally split across several lines.
                'The expected configuration file (%s) does exist. If you wish to '
                'use a different file, set the %s environment variable to the '
                'name of the file that you wish to use. Relative paths will be '
                'interpreted relative to %s.',
                config_path,
                self._path_manager.HYDRONAUT_CONFIG_ENV_VAR,
                self._path_manager.config_dir
            )
            return 1

        @hydra.main(
            version_base=HYDRA_VERSION_BASE,
            config_path=str(config_path.parent),
            config_name=config_path.stem
        )
        def _run(config):
            '''
            Internal runner function. This is defined within this method so that
            class attributes can be used as arguments to hydra.main().

            Args:
                config:
                    The Hydra configuration object. It must contain a field
                    named "experiment.class" that points to an importable Python
                    class which is a subclass of
                    hydronaut.experiment.Experiment.
            '''
            LOGGER.info('Hydronaut configuration file: %s', config_path)
            configure_hydra()
            self.config = config

            with MLflowRunner(config):
                # Configure the environment variables so that any experiment
                # subprocesses can invoke configure_hydra(from_env=True) to
                # re-establish the Hydra configuration. This also ensures that they
                # set the right MLflow run ID.
                configure_environment()

                self._path_manager.add_python_paths(
                    get(self.config, 'experiment.python.paths')
                )

                exp = self.get_experiment_object()
                exp.setup()
                obj_val = exp()
                mlflow.log_metric("Objective Value", obj_val)
                return obj_val
        return _run(*args, **kwargs)


def main(*args: Any, **kwargs: Any) -> OptimizationValue:
    '''
    Main function to run an experiment with the Hydra configuration.

    Args:
        *args, **kwargs:
            Positional and keyword arguments passed through to the hydra.main
            function.

    Returns:
        The value returned by calling the runner.
    '''
    return Runner()(*args, **kwargs)


def script_main() -> None:
    '''
    Hydra makes some assumptions about configuration paths based on how the main
    function is called. This is a workaround for creating a script via
    pyproject.toml. It will simply invoke main() with any passed command-line
    arguments.
    '''
    cmd = (sys.executable, '-m', 'hydronaut.run', *sys.argv[1:])
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as err:
        sys.exit(err)


if __name__ == '__main__':
    main()
