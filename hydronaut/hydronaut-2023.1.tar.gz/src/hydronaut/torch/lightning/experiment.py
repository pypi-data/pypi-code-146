#!/usr/bin/env python3
'''
PyTorch Lightning experiments.
'''

import logging

import mlflow.pytorch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import Callback
from omegaconf import DictConfig

from hydronaut.experiment import Experiment
from hydronaut.hydra.omegaconf import get_container
from hydronaut.types import OptimizationValue

LOGGER = logging.getLogger(__name__)


class PLExperiment(Experiment):
    '''
    Experiment class for PyTorch Lightning experiments.
    '''

    def __init__(
        self,
        config: DictConfig,
        model_cls: pl.LightningModule,
        data_module_cls: pl.LightningDataModule,
        callback_classes: list[Callback] = None
    ) -> None:
        '''
        Args:
            config:
                Same as Experiment.__init__().

            model_cls:
                A subclass of LightningModule.

            data_module_cls:
                A subclass of LightningDataModule.

            callback_classes:
                An optional list of Callback subclasses.

        model_cls, data_module_cls and all classes in callback_classes should
        all accept a single configuration object as a parameter to their
        __init__ methods.
        '''
        super().__init__(config)
        self.model = model_cls(config)
        self.data = data_module_cls(config)
        if callback_classes:
            self.callbacks = [c_cls(config) for c_cls in callback_classes]
        else:
            self.callbacks = []
        self.trainer = None

        # Results object. Currently it only restores the results of the call to
        # trainer.test.
        self.results = {}

    def get_objective_value(self) -> OptimizationValue:
        '''
        Return an objective value for the optimizer. This must be overridden in
        subclasses. It can use any of the attributes of this class such as the
        LightningModule instance or any of the optional Callback instances.

        Returns:
            A numerical value or tuple of numerical values for the optimizer.
        '''
        raise NotImplementedError(
            f'{self.__class__.__name__} does not override get_objective_value()'
        )

    def setup(self):
        '''
        Invoke the data modules setup function to download the data before the
        trainer creates multiple processes that may lead to file conflicts.
        '''
        self.data.setup()

    def __call__(self):
        config = self.config
        params = config.experiment.params

        model = self.model
        data = self.data
        trainer_kwargs = get_container(params, 'trainer', default={}, resolve=True)
        trainer_kwargs['callbacks'] = self.callbacks

        trainer = pl.Trainer(**trainer_kwargs)
        self.trainer = trainer

        # Configure MLflow logging.
        # https://github.com/mlflow/mlflow/blob/eb3588abb55032838b1ff5af1b7d660f2b826dee/examples/pytorch/MNIST/mnist_autolog_example.py
        if trainer.global_rank == 0:
            mlflow.pytorch.autolog()

        trainer.fit(model, datamodule=data)
        self.results['test'] = trainer.test(datamodule=data)

        return self.get_objective_value()
