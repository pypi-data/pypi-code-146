import copy
import dataclasses
import logging
import typing
import torch
import irisml.core

from .build_dataloader import build_dataloader
from .build_lr_scheduler import LrSchedulerFactory, LrSchedulerConfig
from .build_optimizer import OptimizerFactory
from .ddp_trainer import DDPTrainer
from .plugin_loader import load_plugin
from .trainer import Trainer

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Train a pytorch model.

    This is a simple training baseline.

    Config:
        num_epochs (int): The number of epochs.
        batch_size (int): Batch size.
        base_lr (float): Base learning rate.
        device ('cpu' or 'cuda'): Device for training.
        lr_scheduler (LrSchedulerConfig): Learning rate scheduler config.
        momentum (float): Momentum parameter for optimizer.
        val_check_interval(float or int): Validation phase interval.
        weight_decay (float): Weight decay.
        num_processes (int): The number of processes to use. Default: 1.
        no_weight_decay_param_names (Optional[List[str]]): A regex pattern for parameter names to disable weight_decay
        no_weight_decay_module_class_names (Optional[List[str]]): A regex pattern for module class names to disable weight_decay
        lr_scale_param_names (Optional[List[Tuple[str, float]]]): Learning rate scaling for matched parameters.
        plugins: List[str]: Plugins to use for training. Each plugin can have constant values as arguments. e.g. "clip_max_norm(10)".
    """
    VERSION = '0.2.5'

    @dataclasses.dataclass
    class Config:
        num_epochs: int
        batch_size: int = 1
        base_lr: float = 1e-5
        device: typing.Optional[typing.Literal['cpu', 'cuda']] = None
        lr_scheduler: typing.Optional[LrSchedulerConfig] = None
        momentum: float = 0
        optimizer: typing.Literal['sgd', 'adam', 'amsgrad', 'adamw', 'adamw_amsgrad', 'rmsprop', 'zero_adam', 'zero_amsgrad', 'zero_adamw', 'zero_adamw_amsgrad'] = 'sgd'
        val_check_interval: typing.Optional[typing.Union[int, float]] = None
        weight_decay: float = 0
        num_processes: int = 1
        no_weight_decay_param_names: typing.Optional[typing.List[str]] = None
        no_weight_decay_module_class_names: typing.Optional[typing.List[str]] = None
        lr_scale_param_names: typing.Optional[typing.List[typing.Tuple[str, float]]] = None
        plugins: typing.List[str] = dataclasses.field(default_factory=list)

    @dataclasses.dataclass
    class Inputs:
        model: torch.nn.Module
        train_dataset: torch.utils.data.Dataset
        train_transform: typing.Callable
        val_dataset: torch.utils.data.Dataset = None
        val_transform: typing.Callable = None

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module = None

    def execute(self, inputs):
        model = self.train(inputs)
        return self.Outputs(model)

    def dry_run(self, inputs):
        model = self.train(inputs, dry_run=True)
        return self.Outputs(model)

    def train(self, inputs, dry_run=False) -> torch.nn.Module:
        plugins = [load_plugin(p, self.context) for p in self.config.plugins]
        if dry_run:
            train_dataloader = val_dataloader = None
        else:
            train_dataloader = build_dataloader(inputs.train_dataset, inputs.train_transform, batch_size=self.config.batch_size)
            val_dataloader = inputs.val_dataset and build_dataloader(inputs.val_dataset, inputs.val_transform, batch_size=self.config.batch_size, shuffle=False, drop_last=False)
        device = self._get_device()
        model = copy.deepcopy(inputs.model) if not dry_run else inputs.model  # Save CPU memory on dry run

        optimizer_factory = OptimizerFactory(self.config.optimizer, self.config.base_lr, self.config.weight_decay, self.config.momentum,
                                             self.config.no_weight_decay_param_names, self.config.no_weight_decay_module_class_names,
                                             self.config.lr_scale_param_names)
        lr_scheduler_factory = LrSchedulerFactory(self.config.lr_scheduler, self.config.num_epochs, len(train_dataloader) if train_dataloader else 1)

        trainer_parameters = {'model': model, 'lr_scheduler_factory': lr_scheduler_factory, 'optimizer_factory': optimizer_factory, 'plugins': plugins,
                              'device': device, 'val_check_interval': self.config.val_check_interval}

        trainer = self.get_trainer(trainer_parameters)

        if not dry_run:
            trainer.train(train_dataloader, val_dataloader, num_epochs=self.config.num_epochs)

        return trainer.model

    def get_trainer(self, parameters):
        """Get a trainer instance. This method may be overridden by a subclass."""
        if self.config.num_processes == 1:
            return Trainer(**parameters)
        else:
            return DDPTrainer(num_processes=self.config.num_processes, **parameters)

    def _get_device(self) -> torch.device:
        """Get a torch device based on the configuration. If not specified explicitly, it uses cuda if available."""
        if self.config.device:
            device_name = self.config.device
        else:
            device_name = 'cuda' if torch.cuda.is_available() else 'cpu'
            logger.info(f"Training device is selected automatically: {device_name}. To specify the device manually, please set Config.device.")

        return torch.device(device_name)
