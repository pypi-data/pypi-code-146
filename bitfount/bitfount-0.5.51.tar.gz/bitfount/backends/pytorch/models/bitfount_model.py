"""Contains PyTorch implementations of the BitfountModel paradigm."""
from abc import abstractmethod
from collections import defaultdict
import logging
import os
import re
from typing import Any, Dict, List, MutableMapping, Optional, Tuple, Union, cast

import numpy as np
import pytorch_lightning as pl
from pytorch_lightning.callbacks import Callback
from pytorch_lightning.callbacks.progress import TQDMProgressBar
from pytorch_lightning.loggers import TensorBoardLogger
import torch
from torch import nn as nn
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import DataLoader as PyTorchDataLoader

from bitfount.backends.pytorch.data.dataloaders import _BasePyTorchBitfountDataLoader
from bitfount.backends.pytorch.federated.mixins import _PyTorchDistributedModelMixIn
from bitfount.backends.pytorch.models.base_models import (
    _STEP_OUTPUT,
    _TORCH_DTYPES,
    _OptimizerType,
)
from bitfount.backends.pytorch.utils import _autodetect_gpu
from bitfount.config import BITFOUNT_LOGS_DIR, BITFOUNT_OUTPUT_DIR
from bitfount.data.databunch import BitfountDataBunch
from bitfount.data.dataloaders import BitfountDataLoader
from bitfount.data.datasources.base_source import BaseSource
from bitfount.metrics import Metric
from bitfount.models.base_models import ClassifierMixIn, ModelContext
from bitfount.models.bitfount_model import BitfountModel
from bitfount.types import T_DTYPE, _StrAnyDict
from bitfount.utils import _merge_list_of_dicts, delegates
from bitfount.utils.logging_utils import filter_stderr

logger = logging.getLogger(__name__)


@delegates()
class PyTorchBitfountModel(
    _PyTorchDistributedModelMixIn, BitfountModel, pl.LightningModule
):
    """Blueprint for a pytorch custom model in the lightning format.

    This class must be subclassed in its own module. A `Path` to the module containing
    the subclass can then be passed to `BitfountModelReference` and on to your
    `Algorithm` of choice which will send the model to Bitfount Hub.

    To get started, just implement the abstract methods in this class. For more advanced
    users feel free to override or overwrite any variables/methods in your subclass.

    Take a look at the pytorch-lightning documentation on how to properly create a
    `LightningModule`:

    https://pytorch-lightning.readthedocs.io/en/stable/common/lightning_module.html

    :::caution

    Ensure you set `self.metrics` in the `__init__` method of your subclass to ensure
    they pertain appropriately to your model. If not, Bitfount will attempt to set
    these appropriately for you but there is no guarantee it will get it right.

    :::

    Args:
        batch_size: The batch size to use for training. Defaults to 32.
        epochs: The number of epochs to train for.
        steps: The number of steps to train for.
        **kwargs: Any additional arguments to pass to parent constructors.

    Attributes:
        batch_size: The batch size to use for training.
        epochs: The number of epochs to train for.
        steps: The number of steps to train for.
        preds: The predictions from the most recent test run.
        target: The targets from the most recent test run.
        val_stats: Metrics from the validation set during training.

    Raises:
        ValueError: If both `epochs` and `steps` are specified.
    """

    train_dl: _BasePyTorchBitfountDataLoader
    # Test attributes
    _test_preds: Optional[List[np.ndarray]]
    _test_targets: Optional[List[np.ndarray]]

    def __init__(
        self,
        batch_size: int = 32,
        epochs: Optional[int] = None,
        steps: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        if (steps is None and epochs is None) or (
            isinstance(steps, int) and isinstance(epochs, int)
        ):
            raise ValueError("You must specify one (and only one) of steps or epochs.")

        # Set hyperparameters
        self.batch_size = batch_size
        self.epochs: Optional[int] = epochs
        self.steps: Optional[int] = steps

        # Set training attributes
        # Override self._model with your model
        self._model: Optional[nn.Module] = None
        self._pl_trainer: pl.Trainer = self.trainer_init()  # cannot be "self.trainer"
        self.preds: List[float] = []
        self.target: List[float] = []
        self.val_stats: List[Dict[str, float]] = []
        self._trained_on_previous_batch: bool = False
        self._total_num_batches_trained: int = 0

    @staticmethod
    def _get_import_statements() -> List[str]:
        """Returns a list of import statements likely to be required for the model.

        Returns:
            A list of import statements.
        """
        return [
            "import os",
            "import torch",
            "from torch import nn as nn",
            "from torch.nn import functional as F",
            "from bitfount import *",
            "import bitfount",
        ]

    @abstractmethod
    def forward(self, x: Any) -> Any:  # type:ignore[override] # Reason: see below
        """Forward method of the model - just like a regular `torch.nn.Module` class.

        :::tip

        This will depend on your model but could be as simple as:

        ```python
        return self._model(x)
        ```

        :::

        Args:
            x: Input to the model.

        Returns:
            Output of the model.
        """
        # pl.LightningModule incompatible with our forward function.
        raise NotImplementedError

    @abstractmethod
    def configure_optimizers(
        self,
    ) -> Union[_OptimizerType, Tuple[List[_OptimizerType], List[_LRScheduler]]]:
        """Configures the optimizer(s) and scheduler(s) for backpropagation.

        Returns:
            Either the optimizer of your choice or a tuple of optimizers and learning
            rate schedulers.
        """
        raise NotImplementedError

    @abstractmethod
    def create_model(self) -> nn.Module:
        """Creates and returns the underlying pytorch model.

        Returns:
            Underlying pytorch model. This is set to `self._model`.
        """
        raise NotImplementedError

    @abstractmethod
    def training_step(self, batch: Any, batch_idx: int) -> _STEP_OUTPUT:  # type: ignore[override] # Reason: see below  # noqa: B950
        """Training step.

        :::caution

        If iterations have been specified in terms of steps, the default behaviour of
        pytorch lightning is to train on the first _n_ steps of the dataloader every
        time `fit` is called. This default behaviour is not desirable and has been dealt
        with in the built-in Bitfount models but, until this bug gets fixed by the
        pytorch lightning team, this needs to be implemented by the user for custom
        models.

        :::

        :::tip

        Take a look at the `skip_training_batch` method for one way on how to deal with
        this. It can be used as follows:

        ```python
        if self.skip_training_batch(batch_idx):
            return None
        ```

        :::

        Args:
            batch: The batch to be trained on.
            batch_idx: The index of the batch to be trained on from the train
                dataloader.

        Returns:
            The loss from this batch as a `torch.Tensor`. Or a dictionary which includes
            the key `loss` and the loss as a `torch.Tensor`.
        """
        # Override the pl.lightning method, as it requires *args
        # and **kwargs as arguments whereas we will always have
        # the batch and the batch_idx as args
        raise NotImplementedError

    @abstractmethod
    def validation_step(self, batch: Any, batch_idx: int) -> _StrAnyDict:  # type: ignore[override] # Reason: see below # noqa: B950
        """Validation step.

        Args:
            batch: The batch to be evaluated.
            batch_idx: The index of the batch to be evaluated from the validation
                dataloader.

        Returns:
            A dictionary of strings and values that should be averaged at the end of
            every epoch and logged e.g. `{"validation_loss": loss}`. These will be
            passed to the `validation_epoch_end` method.
        """
        # Override the pl.lightning method, as it requires *args
        # and **kwargs as arguments whereas we will always have
        # the batch and the batch_idx as args
        raise NotImplementedError

    @abstractmethod
    def test_step(self, batch: Any, batch_idx: int) -> _STEP_OUTPUT:  # type: ignore[override] # Reason: see below  # noqa: B950
        """Operates on a single batch of data from the test set.

        Args:
            batch: The batch to be evaluated.
            batch_idx: The index of the batch to be evaluated from the test
                dataloader.

        Returns:
            A dictionary of predictions and targets, with the dictionary
            keys being "predictions" and "targets" for each of them, respectively.
            These will be passed to the `test_epoch_end` method.
        """
        # Override the pl.lightning method, as it requires
        # *args and **kwargs as arguments whereas we will
        # always have the batch and the batch_idx as args
        raise NotImplementedError

    def tensor_precision(self) -> T_DTYPE:
        """Returns tensor dtype used by Pytorch Lightning Trainer.

        :::note

        Currently only 32-bit training is supported.

        :::

        Returns:
            Pytorch tensor dtype.
        """
        # TODO: [BIT-727] support non-32 bit training
        return cast(T_DTYPE, _TORCH_DTYPES[cast(int, self._pl_trainer.precision)])

    def initialise_model(
        self, data: Optional[BaseSource] = None, context: Optional[ModelContext] = None
    ) -> None:
        """Any initialisation of models/dataloaders to be done here.

        Initialises the dataloaders and sets `self._model` to be the output from
        `self.create_model`. Any initialisation ahead of federated or local training,
        serialization or deserialization should be done here.

        Args:
            data: The datasource for model training. Defaults to None.
            context: Indicates if the model is running as a modeller or worker.
                If None, there is no difference between modeller and worker.
        """
        self._context = context
        self._initialised = True
        if self._context == ModelContext.MODELLER:
            # In a distributed setting, the Modeller needs to first initialise its
            # own model before it can be used. The pod identifier needs to be set
            # before the model is initialised so the the relevant details can be
            # retrieved from the schema. For this we just use the first pod
            # identifier specified in the datastructure as it is assumed the the
            # schemas for all the Pods are the same.
            pod_identifiers = self.datastructure.get_pod_identifiers()
            if pod_identifiers:
                self.set_pod_identifier(pod_identifiers[0])
        if data is not None:
            if self.datastructure.query:
                table_schema = self.datastructure._override_schema(
                    pod_identifier=self.pod_identifier
                )
                self.databunch = BitfountDataBunch(
                    data_structure=self.datastructure,
                    schema=table_schema,
                    datasource=data,
                )
            elif self.datastructure.table:
                if context:
                    table_schema = self.schema.get_table_schema(
                        self.datastructure.get_table_name(self.pod_identifier)
                    )
                    self.databunch = BitfountDataBunch(
                        data_structure=self.datastructure,
                        schema=table_schema,
                        datasource=data,
                    )
                else:
                    # For local training, we can add the datasource to the schema.
                    data.load_data(table_name=self.datastructure.table)
                    self._add_datasource_to_schema(data)
                    table_schema = self.schema.get_table_schema(
                        self.datastructure.get_table_name(self.pod_identifier)
                    )

            if self._context != ModelContext.MODELLER:
                self._set_dataloaders(self.batch_size)
        else:
            if self.datastructure.query:
                table_schema = self.datastructure._override_schema(
                    pod_identifier=self.pod_identifier
                )
            else:
                table_schema = self.schema.get_table_schema(
                    self.datastructure.get_table_name(self.pod_identifier)
                )
        self.datastructure.set_training_input_size(table_schema)

        if hasattr(self, "_objective") and self._objective == "classification":
            # The casts here are to assuage mypy because it (incorrectly) asserts
            # that a subclass of both ClassifierMixIn and BitfountModel cannot exist.
            # We utilise a subclass of both in the tests to assure ourselves.
            if isinstance(cast(ClassifierMixIn, self), ClassifierMixIn):
                cast(ClassifierMixIn, self).set_number_of_classes(table_schema)
            else:
                raise TypeError(
                    "Training objective is classification but this model does not "
                    "inherit from ClassifierMixIn"
                )
        self._model = self.create_model()

    def trainer_init(self) -> pl.Trainer:
        """Initialises the Lightning Trainer for this model.

        Documentation for pytorch-lightning trainer can be found here:
        https://pytorch-lightning.readthedocs.io/en/stable/common/trainer.html

        :::tip

        Override this method to choose your own `Trainer` arguments.

        :::

        Returns:
            The pytorch lightning trainer.
        """
        callbacks: List[Callback] = [TQDMProgressBar(refresh_rate=1)]

        # torch emits warnings to stderr that are not relevant for us, so we need
        # to filter them out
        with filter_stderr(
            re.escape(
                "[W Context.cpp:70] Warning:"
                " torch.use_deterministic_algorithms is in beta"
            )
        ):
            gpu_kwargs = _autodetect_gpu()
            trainer = pl.Trainer(
                max_epochs=self.epochs or -1,
                max_steps=self.steps or -1,
                deterministic=True,
                auto_lr_find=True,
                callbacks=callbacks,
                logger=TensorBoardLogger(save_dir=str(BITFOUNT_LOGS_DIR)),
                default_root_dir=str(BITFOUNT_OUTPUT_DIR),
                **gpu_kwargs,
            )
            return trainer

    def train_dataloader(self) -> _BasePyTorchBitfountDataLoader:  # type: ignore[override] # Reason: see below # noqa: B950
        """Returns training dataloader."""
        # We override the dataloader return annotation as the LightningModule
        # expects a pytorch DataLoader, and we return out PyTorchBitfountDataLoader
        return self.train_dl

    def val_dataloader(self) -> _BasePyTorchBitfountDataLoader:  # type: ignore[override] # Reason: see below # noqa: B950
        """Returns validation dataloader."""
        # We override the dataloader return annotation as the LightningModule
        # expects a pytorch DataLoader, and we return out PyTorchBitfountDataLoader
        return cast(_BasePyTorchBitfountDataLoader, self.validation_dl)

    def test_dataloader(self) -> _BasePyTorchBitfountDataLoader:  # type: ignore[override] # Reason: see below # noqa: B950
        """Returns test dataloader."""
        # We override the dataloader return annotation as the LightningModule
        # expects a pytorch DataLoader, and we return out PyTorchBitfountDataLoader
        return cast(_BasePyTorchBitfountDataLoader, self.test_dl)

    def serialize(self, filename: Union[str, os.PathLike]) -> None:
        """Serialize model to file with provided `filename`.

        Args:
            filename: Path to file to save serialized model.
        """
        if not self._initialised:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model()
        # Model has been initialised, assuring mypy of this
        assert self._model is not None  # nosec[assert_used]
        torch.save(self._model.state_dict(), filename)

    def deserialize(self, filename: Union[str, os.PathLike], **kwargs: Any) -> None:
        """Deserialize model.

        :::danger

        This should not be used on a model file that has been received across a
        trust boundary due to underlying use of `pickle` by `torch`.

        :::

        Args:
            filename: Path to file containing serialized model.
            **kwargs: Keyword arguments provided to `torch.load` under the hood.
        """
        if not self._initialised:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model()
        # Model has been initialised, assuring mypy of this
        assert self._model is not None  # nosec[assert_used]
        self._model.load_state_dict(torch.load(filename, **kwargs))

    def skip_training_batch(self, batch_idx: int) -> bool:
        """Checks if the current batch from the training set should be skipped.

        This is a workaround for the fact that PyTorch Lightning starts the Dataloader
        iteration from the beginning every time `fit` is called. This means that if we
        are training in steps, we are always training on the same batches. So this
        method needs to be called at the beginning of every `training_step` to skip
        to the right batch index.

        Args:
            batch_idx: the index of the batch from `training_step`.

        Returns:
            True if the batch should be skipped, otherwise False.
        """
        # TODO: [BIT-1237] remove this code block and find a better way to do this that
        # doesn't involve loading every batch into memory until we get to the right one
        if self.steps:
            # If we have trained on the previous batch, we can avoid the checks because
            # it means we have already reached the target start batch.
            if not self._trained_on_previous_batch:
                if (self.steps != self._pl_trainer.max_steps) and (
                    batch_idx < (self._total_num_batches_trained % len(self.train_dl))
                ):
                    return True
                else:
                    self._trained_on_previous_batch = True

            # `_total_num_batches_trained` hasn't been incremented yet so we need to add
            # 1 here to get the correct batch number.
            if self._total_num_batches_trained + 1 == self._pl_trainer.max_steps:
                self._trained_on_previous_batch = False

        if not self._pl_trainer.sanity_checking:
            self._total_num_batches_trained += 1

        return False

    def validation_epoch_end(  # type: ignore[override] # Reason: see below
        self, outputs: List[_StrAnyDict]
    ) -> None:
        """Called at the end of the validation epoch with all validation step outputs.

        Ensures that the average metrics from a validation epoch is stored. Logs results
        and also appends to `self.val_stats`.

        Args:
            outputs: List of outputs from each validation step.
        """
        # Override the pl.lightning method, as its outputs can be
        # List[Union[Tensor, _StrAnyDict]],
        # whereas we force outputs to be a Dict
        avgs = self._compute_metric_averages(outputs)
        self.val_stats.append(avgs)

        # Also log out these averaged metrics
        for k, v in avgs.items():
            self.log(f"avg_{k}", v)

    def test_epoch_end(self, outputs: List[Dict[str, torch.Tensor]]) -> None:  # type: ignore[override] # Reason: see below # noqa: B950
        """Aggregates the predictions and targets from the test set.

        :::caution

        If you are overwriting this method, ensure you set `self._test_preds` to
        maintain compatibility with `self._predict_local` unless you are overwriting
        both of them.

        :::

        Args:
            outputs: List of outputs from each test step.
        """
        # Override the pl.lightning method, as it requires a different type for outputs.
        merged_outputs: Dict[str, List[torch.Tensor]] = _merge_list_of_dicts(outputs)
        self._test_preds = [i.cpu().numpy() for i in merged_outputs["predictions"]]
        self._test_targets = [i.cpu().numpy() for i in merged_outputs["targets"]]

    @staticmethod
    def _compute_metric_averages(outputs: List[_StrAnyDict]) -> Dict[str, float]:
        """Compute the average metrics from a list of outputs."""
        # Stack up shared dict keys into lists of entries
        stacked_dict = defaultdict(list)
        for output in outputs:
            for k, v in output.items():
                stacked_dict[k].append(v)

        # Calculate the average value of each key and convert to float
        avgs = {}
        for k, v_list in stacked_dict.items():
            avgs[k] = float(torch.stack(v_list).mean().item())
        return avgs

    def _evaluate_local(
        self, test_dl: Optional[BitfountDataLoader] = None, **kwargs: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """This method runs inference on the test dataloader.

        This is done by calling `self.test_step` under the hood. Customise this method
        as you please but it must return a list of predictions and a list of targets.

        Args:
            test_dl: Optional dataloader to run inference on which takes precedence over
                the dataloader returned by `self.test_dataloader`.

        Returns:
            A tuple of predictions and targets as numpy arrays.
        """
        # Reset test attributes to None
        self._reset_test_attrs()
        if test_dl is None:
            if isinstance(self.test_dl, _BasePyTorchBitfountDataLoader):
                test_dl = self.test_dl
            else:
                raise ValueError("No test data to evaluate the model on.")
        self._pl_trainer.test(model=self, dataloaders=cast(PyTorchDataLoader, test_dl))
        return np.asarray(self._test_preds), np.asarray(self._test_targets)

    def _reset_test_attrs(self) -> None:
        """Resets test attributes to None."""
        self._test_preds = None
        self._test_targets = None

    def _predict_local(self, data: BaseSource, **kwargs: Any) -> List[np.ndarray]:
        """This method runs inference on the test data, returns predictions.

        This is done by calling `test_step` under the hood. Customise this method as you
        please but it must return a list of predictions and a list of targets. Note that
        as this is the prediction function, only the predictions are returned.

        :::tip

        Feel free to overwrite this method just so long as you return a numpy array to
        maintain compatability with the `ModelInference` algorithm - you are not limited
        to just returning predictions.

        :::

        Returns:
            A numpy array containing the prediction values.
        """
        if data is not None:
            data.load_data()
            self._add_datasource_to_schema(data)  # Also sets `self.databunch
            test_dl = self.databunch.get_test_dataloader(self.batch_size)
            if isinstance(test_dl, BitfountDataLoader):
                logger.info(
                    f"Using test portion of dataset for inference - this has "
                    f"{len(test_dl)} record(s)."
                )
            else:
                raise ValueError("No test data to infer in the provided datasource.")

        self._pl_trainer.test(model=self, dataloaders=cast(PyTorchDataLoader, test_dl))

        if self._test_preds is not None:
            return self._test_preds

        raise ValueError("'self._test_preds' was not set by the model after inference.")

    def _fit_local(
        self,
        data: BaseSource,
        metrics: Optional[Union[str, List[str], MutableMapping[str, Metric]]] = None,
        **kwargs: Any,
    ) -> Dict[str, str]:
        """Trains the model on local data.

        Returns:
            Validation metrics for the final epoch.
        """
        if not self._initialised:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model(data)

        self._pl_trainer.fit(self)

        # Return the validation stats to be sent back
        return {k: ("%.4f" % v) for k, v in self.val_stats[-1].items()}
