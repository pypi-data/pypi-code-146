"""Train with gradient caching. Useful for training a large model that requires lots of GPU memory.

Initially I tried to make a wrapper for Model without modifing the Trainer class. However, it required a backward loop in a training_step(), which is bit counterintuitive.
Also having a backward pass in training_step() will make a conflict with plugins that have callbacks for backward pass.
For example, the AMP plugin might require special implementation for gradient caching.

"""
import contextlib
import copy
import dataclasses
import logging
import irisml.core
import torch
from .train import Task as TrainTask
from .train.ddp_utils import all_gather, all_gather_object

logger = logging.getLogger(__name__)


class Task(TrainTask):
    """Train a model using gradient cache. Useful for contrastive learning with a large model.

    This trainer expects the model to return a single FloatTensor or a tuple of FloatTensors or a scalar Tensor.
    If a scalar Tensor is returned, the trainer assumes it is a fixed value in an iteration regardless of inputs.

    Config:
        sub_batch_size (int): Sub batch size for each forward/backward pass. batch_size must be divisible by sub_batch_size.
    """
    VERSION = '0.1.1'

    @dataclasses.dataclass
    class Config(TrainTask.Config):
        sub_batch_size: int = 1

    def execute(self, inputs):
        if self.config.batch_size % self.config.sub_batch_size != 0:
            raise ValueError(f"batch_size must be divisible by sub_batch_size. batch_size={self.config.batch_size}, sub_batch_size={self.config.sub_batch_size}")
        return super().execute(inputs)

    def get_trainer(self, parameters):
        parameters['sub_batch_size'] = self.config.sub_batch_size
        if self.config.num_processes == 1:
            return GradientCachingTrainer(**parameters)
        else:
            return GradientCachingDDPTrainer(num_processes=self.config.num_processes, **parameters)


class GradientCachingMixin:
    class ModelWrapper:
        def __init__(self, model, device):
            self._model = model
            self._device = device
            self._criterion = model.criterion
            self._has_multiple_features = None

        def __call__(self, inputs, rng_states=None):
            """
            Args:
                inputs (Any): inputs to the model
                rng_states (List): Random Number Generator state to use. Default: None

            Returns:
                (features, rng_states)
            """
            current_rng_states = rng_states or self._get_rng_states()
            with self._use_rng_states(rng_states):
                features = self._model(inputs)

            if self._has_multiple_features is None:
                self._has_multiple_features = isinstance(features, (list, tuple))
            if not self._has_multiple_features:
                features = [features]

            return features, current_rng_states

        def __getattr__(self, attr):
            return getattr(self._model, attr)

        def calculate_loss(self, features, targets):
            if not self._has_multiple_features:
                features = features[0]
            return self._criterion(features, targets)

        def _get_rng_states(self):
            states = [torch.get_rng_state()]
            if self._device.type == 'cuda':
                states.append(torch.cuda.get_rng_state(self._device))
            return states

        @contextlib.contextmanager
        def _use_rng_states(self, rng_states):
            if rng_states:
                devices = [self._device] if self._device.type == 'cuda' else None
                with torch.random.fork_rng(devices):
                    torch.set_rng_state(rng_states[0])
                    if len(rng_states) > 1:
                        torch.cuda.set_rng_state(rng_states[1], self._device)
                    yield
            else:
                yield

    def __init__(self, sub_batch_size, **kwargs):
        super().__init__(**kwargs)
        self._sub_batch_size = sub_batch_size
        assert self.criterion, "The model must have a criterion property to use gradient caching."

    def train_epoch(self, dataloader, epoch):
        if not self._plugins.on_train_epoch_start(self, self.model, epoch):
            return False  # Early stopping

        model = GradientCachingMixin.ModelWrapper(self.model, self.device)

        for batch_index, batch in enumerate(dataloader):
            self._optimizer.zero_grad()
            batch = self._plugins.on_train_batch_start(self, self.model, batch, batch_index)
            batch = self._to_device(batch)
            sub_batches = list(zip(self._split_tensor_or_list(batch[0]), self._split_tensor_or_list(batch[1])))

            # Run forward pass for the sub batches.
            with self._plugins.forward_context():
                with torch.no_grad():
                    results = [model(b[0]) for b in sub_batches]
                    features_local = [r[0] for r in results]
                    rng_states = [r[1] for r in results]
                    # Note that a feature vector can contain a scalar tensor. In such case, uses the first scalar value since the trainer assumes all sub_batch returns a same value.
                    features = [torch.cat(f, dim=0) if f[0].shape else f[0] for f in zip(*features_local)]

            # Set requires_grad in order to calculate gradients for features on this device.
            for f in features:
                f.requires_grad_()

            features_all = [self._all_gather(f) for f in features]
            targets_all = self._all_gather(batch[1])
            loss = model.calculate_loss(features_all, targets_all)

            # Run backward pass to calculate gradients for 'features'.
            loss = self._plugins.on_train_backward_start(self, self.model, loss)
            loss.backward()
            self._plugins.on_train_backward_end(self, self.model)

            # Copy the gradients of the feature vectors. Deep-copied so that the subsequent backward pass doesn't affect the cache
            gradient_cache = [self._split_tensor_or_list(copy.deepcopy(f.grad.detach())) for f in features]

            for i, sub_batch in enumerate(sub_batches):
                # Run forward pass again, with gradients this time.
                with self._plugins.forward_context():
                    features_local_recalculated = model(sub_batch[0], rng_states[i])[0]
                    assert len(features_local_recalculated) == len(gradient_cache)

                maybe_no_sync = self.model.no_sync if hasattr(model, 'no_sync') and i + 1 != len(sub_batches) else contextlib.nullcontext
                with maybe_no_sync():
                    # Run backward pass using the cached gradients for each features.
                    for j, f in enumerate(features_local_recalculated):
                        if not torch.allclose(f, features_local[i][j]):
                            diff = torch.max(torch.abs(f - features_local[i][j]))
                            logger.warning(f"The recalculated feature({i=}, {j=}) has different values. {diff=}")
                        gradient = gradient_cache[j][i] if f.shape else (gradient_cache[j] / len(sub_batches))
                        f.backward(gradient=gradient)

            optimizer = self._plugins.on_optimizer_step_start(self, self.model, self._optimizer)
            optimizer.step()
            self._plugins.on_train_batch_end(self, self.model, loss, batch, batch_index)
            self._lr_scheduler.step()

        self._plugins.on_train_epoch_end(self, self.model, epoch)
        return True

    def _all_gather(self, tensor_or_list):
        """Gather tensors from all devices. Keep the local tensors as they are."""
        if not torch.distributed.is_initialized():
            return tensor_or_list

        if torch.is_tensor(tensor_or_list):
            if not tensor_or_list.shape:
                return tensor_or_list  # TODO: We have an assumption that a sclar tensor is same on all devices.
            return all_gather(tensor_or_list)
        else:
            assert isinstance(tensor_or_list, list)
            return all_gather_object(tensor_or_list)

    def _split_tensor_or_list(self, tensor_or_list):
        if torch.is_tensor(tensor_or_list):
            if not tensor_or_list.shape:
                return tensor_or_list  # Returns a scalar value as-is.
            assert len(tensor_or_list) % self._sub_batch_size == 0, f"len(tensor_or_list) must be divisible by sub_batch_size. {len(tensor_or_list)}, {self._sub_batch_size}"
            return torch.split(tensor_or_list, self._sub_batch_size)
        elif torch.is_tensor(tensor_or_list[0]):
            assert all(len(t) % self._sub_batch_size == 0 for t in tensor_or_list)
            return list(zip(*[torch.split(t, self._sub_batch_size) for t in tensor_or_list]))
        else:
            assert isinstance(tensor_or_list, list)
            assert len(tensor_or_list) % self._sub_batch_size == 0, f"len(tensor_or_list) must be divisible by sub_batch_size. {len(tensor_or_list)}, {self._sub_batch_size}"
            num_chunks = self.config.batch_size // self._sub_batch_size
            bs = self._sub_batch_size
            return [tensor_or_list[i * bs: (i + 1) * bs] for i in range(num_chunks)]


class GradientCachingTrainer(GradientCachingMixin, irisml.tasks.train.Trainer):
    pass


class GradientCachingDDPTrainer(GradientCachingMixin, irisml.tasks.train.DDPTrainer):
    pass
