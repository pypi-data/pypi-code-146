import contextlib
import functools
import logging
import multiprocessing
import os
import socket
import torch.multiprocessing
import torch.utils.data


def recreate_dataloader_with_distributed_sampler(dataloader: torch.utils.data.DataLoader):
    if isinstance(dataloader.sampler, torch.utils.data.RandomSampler):
        shuffle = True
    elif isinstance(dataloader.sampler, torch.utils.data.SequentialSampler):
        shuffle = False
    else:
        raise RuntimeError(f"DDP Trainer doesn't support the sampler {dataloader.sampler}. Please make a pull request.")

    # Create a new sampler. If shuffle is True, the default random seed 0 will be used.
    sampler = torch.utils.data.distributed.DistributedSampler(dataloader.dataset, shuffle=shuffle)
    return recreate_dataloader_with_new_sampler(dataloader, sampler)


def recreate_dataloader_with_new_sampler(dataloader: torch.utils.data.DataLoader, sampler: torch.utils.data.Sampler):
    return torch.utils.data.DataLoader(dataloader.dataset, dataloader.batch_size, sampler=sampler, num_workers=dataloader.num_workers,
                                       collate_fn=dataloader.collate_fn, pin_memory=dataloader.pin_memory, drop_last=dataloader.drop_last, timeout=dataloader.timeout,
                                       worker_init_fn=dataloader.worker_init_fn, prefetch_factor=dataloader.prefetch_factor, multiprocessing_context=dataloader.multiprocessing_context)


class DDPWrapperModel(torch.nn.Module):
    """A wrapper model to let DDP use forward() method instead of training_step() method."""
    def __init__(self, model):
        super().__init__()
        self._model = model

    def forward(self, *args, _call_training_step=False, **kwargs):
        if _call_training_step:
            return self._model.training_step(*args, **kwargs)
        else:
            return self._model.forward(*args, **kwargs)

    def state_dict(self, *args, **kwargs):
        return self._model.state_dict(*args, **kwargs)

    def load_state_dict(self, *args, **kwargs):
        return self._model.load_state_dict(*args, **kwargs)


def create_distributed_data_parallel_model(model, device_ids):
    # TODO: we might need to set find_unused_parameters=True if there are models that require such settings.
    ddp_model = torch.nn.parallel.DistributedDataParallel(DDPWrapperModel(model), device_ids=device_ids)
    if hasattr(model, 'criterion'):
        ddp_model.criterion = model.criterion
    if hasattr(model, 'predictor'):
        ddp_model.predictor = model.predictor
    if hasattr(model, 'training_step'):
        ddp_model.training_step = functools.partial(ddp_model.forward, _call_training_step=True)
    if hasattr(model, 'prediction_step'):
        ddp_model.prediction_step = model.prediction_step

    return ddp_model


def _get_available_port():
    """Find an available port number on the localhost."""
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def _wrap_function(process_index, target_function, args, logger_info):
    logging.getLogger().setLevel(logger_info[0])
    logging.getLogger('irisml').setLevel(logger_info[1])
    old_handler_strs = [str(type(h)) for h in logging.getLogger().handlers]

    # Remove the default logging handlers. Some modules create them when imported.
    for h in logging.getLogger().handlers:
        logging.getLogger().removeHandler(h)

    for h in logger_info[2]:
        logging.getLogger().addHandler(h)

    logger = logging.getLogger(__name__)
    logger.info(f"Removed logging handlers: {','.join(old_handler_strs)}")
    logger.info(f"Set logging levels: root={logger_info[0]}, irisml={logger_info[1]}")
    logger.info(f"Started a new process. {process_index=}, {args=}")

    target_function(process_index, *args)


def spawn_processes(target_function, args, nprocs):
    """Spawn subprocesses and wait until one of them ends.

    The subprocess inherits logging handlers from the current process.

    MASTER_ADDR and MASTER_PORT environment variables will be added on this process and the child processes.

    Args:
        target_function (Callable): The first argument is the local rank.
        args (List): Arguments for the target function.
        nprocs (int): The number of processes to make.

    Returns:
        SpawnContext
    """
    # Keep using the logger if it can be serialized and deserialized in the child process.
    # The Irisml's official log handlers are serializable, but sometimes other platform such as pytest might add a new log handler.
    pickleable_log_handlers = [h for h in logging.getLogger().handlers if hasattr(h, '__getstate__')]
    logger_info = (logging.getLogger().getEffectiveLevel(), logging.getLogger('irisml').getEffectiveLevel(), pickleable_log_handlers)

    # There is a bug in file_descriptor sharing that results in "bad value(s) in fds_to_keep" exception.
    # https://github.com/pytorch/pytorch/issues/31571
    torch.multiprocessing.set_sharing_strategy('file_system')

    # Set environment variables if they are not defined. AML can set those variables if DistributedConfig was used.
    if not os.getenv('MASTER_ADDR'):
        os.environ['MASTER_ADDR'] = 'localhost'
    if not os.getenv('MASTER_PORT'):
        os.environ['MASTER_PORT'] = str(_get_available_port())

    # This method will block until all processes end or any process fails.
    return torch.multiprocessing.spawn(_wrap_function, args=(target_function, args, logger_info), nprocs=nprocs, join=False)


def spawn_and_wait(target_function, args, nprocs):
    context = spawn_processes(target_function, args, nprocs)
    sentinels = [p.sentinel for p in context.processes]

    # Wait until one of the processes is terminated.
    multiprocessing.connection.wait(sentinels)

    return context


def all_gather(tensor):
    """Gather tensors from all nodes.

    Collected tensors are concatenated at the first dimension.

    Raises a runtime error if it's not on distributed environment.
    """
    if not torch.distributed.is_initialized():
        raise RuntimeError("Distributed training is not initialized.")

    world_size = torch.distributed.get_world_size()
    rank = torch.distributed.get_rank()
    tensors = [torch.zeros_like(tensor) for _ in range(world_size)]
    torch.distributed.all_gather(tensors, tensor)

    tensors[rank] = tensor  # Make sure the local tensor keeps the gradients.
    return torch.cat(tensors, dim=0)


def all_gather_object(obj):
    """Gather python objects from all nodes.

    Raises a runtime error if it's not on distributed environment.
    """
    if not torch.distributed.is_initialized():
        raise RuntimeError("Distributed training is not initialized.")

    world_size = torch.distributed.get_world_size()
    object_list = [None] * world_size
    torch.distributed.all_gather_object(object_list, obj)
    return object_list
