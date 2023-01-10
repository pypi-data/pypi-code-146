import math
import os
import platform
import time
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from loguru import logger

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
import torchvision

try:
    import thop  # for FLOPs computation
except ImportError:
    thop = None


@contextmanager
def wait_for_the_master(local_rank=-1):
    """
    Make all processes waiting for the master to do some task.
    """
    if local_rank > 0:
        dist.barrier()
    yield
    if local_rank == 0:
        if not dist.is_available():
            return
        if not dist.is_initialized():
            return
        else:
            dist.barrier()


def load_ckpt(model, weights, device=0, is_state_dict=True, load_keys=None):
    """
    load ckpt to model
    Args:
        model: torch model
        weights (str): weights path
        device (int | List | torch.device): device num
        is_stat_dict (bool): False: model.load_state_dict(ckpt.state_dict())
                             True : model.load_state_dict(ckpt)
        load_keys (dict key): weights to be loaded
    Returns:
        model
    """
    assert os.path.exists(weights), "weights path is not existe"
    logger.info("loading checkpoint from {}".format(weights))

    map_location = select_device(device)
    ckpt = torch.load(weights, map_location=map_location)

    state_dict = ckpt
    if is_state_dict:
        if load_keys is not None:
            state_dict = ckpt[load_keys]
    else:
        state_dict = ckpt.state_dict()

    model_state_dict = model.state_dict()
    load_dict = {}
    for key_model, v in model_state_dict.items():
        if key_model not in state_dict:
            print(
                "{} is not in the ckpt. Please double check and see if this is desired.".format(
                    key_model
                )
            )
            continue
        v_ckpt = state_dict[key_model]
        if v.shape != v_ckpt.shape:
            print(
                "Shape of {} in checkpoint is {}, while shape of {} in model is {}.".format(
                    key_model, v_ckpt.shape, key_model, v.shape
                )
            )
            continue
        load_dict[key_model] = v_ckpt

    model.load_state_dict(load_dict, strict=False)
    logger.info("loaded checkpoint done.")


def select_device(device=0):
    """

    Args:
        device (int | str | torch.device | list):
    Returns:
        torch.device
    """
    cpu = False
    gpu_id = 0
    if isinstance(device, int):
        cpu = device == -1 or not torch.cuda.is_available()
        gpu_id = device
        device = torch.device(f'cuda:{gpu_id}' if not cpu else 'cpu')
    elif isinstance(device, torch.device):
        if device.type == 'cuda':
            gpu_id = device.index
            assert torch.cuda.is_available() and gpu_id < torch.cuda.device_count()
        else:
            cpu = True
    elif isinstance(device, str):
        cpu = device.startswith('cpu')
        gpu_id = int(device[-1])
        device = torch.device(f'cuda:{gpu_id}' if not cpu else 'cpu')
    elif isinstance(device, list):
        device_id = device[0] if len(device) else 0
        cpu = device_id == -1 and not torch.cuda.is_available()
        gpu_id = device
        device = torch.device(f'cuda:{gpu_id}' if not cpu else 'cpu')
    else:
        raise Exception('device type is error')

    if cpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # force torch.cuda.is_available() = False
    else:  # non-cpu device requested
        os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)  # set environment variable
        assert torch.cuda.is_available(), f'CUDA unavailable, invalid device {device} requested'  # check availability

    return device


def profile(input, ops, n=10, device=None):
    """ YOLOv5 speed/memory/FLOPs profiler
    Usage:
        input = torch.randn(16, 3, 640, 640)
        m1 = lambda x: x * torch.sigmoid(x)
        m2 = nn.SiLU()
        profile(input, [m1, m2], n=100)  # profile over 100 iterations
    """
    results = []
    if not isinstance(device, torch.device):
        device = select_device(device)
    print(f"{'Params':>12s}{'GFLOPs':>12s}{'GPU_mem (GB)':>14s}{'forward (ms)':>14s}{'backward (ms)':>14s}"
          f"{'input':>24s}{'output':>24s}")

    for x in input if isinstance(input, list) else [input]:
        x = x.to(device)
        x.requires_grad = True
        for m in ops if isinstance(ops, list) else [ops]:
            m = m.to(device) if hasattr(m, 'to') else m  # device
            m = m.half() if hasattr(m, 'half') and isinstance(x, torch.Tensor) and x.dtype is torch.float16 else m
            tf, tb, t = 0, 0, [0, 0, 0]  # dt forward, backward
            try:
                flops = thop.profile(m, inputs=(x,), verbose=False)[0] / 1E9 * 2  # GFLOPs
            except Exception:
                flops = 0

            try:
                for _ in range(n):
                    t[0] = time_synchronized()
                    y = m(x)
                    t[1] = time_synchronized()
                    try:
                        _ = (sum(yi.sum() for yi in y) if isinstance(y, list) else y).sum().backward()
                        t[2] = time_synchronized()
                    except Exception:  # no backward method
                        # print(e)  # for debug
                        t[2] = float('nan')
                    tf += (t[1] - t[0]) * 1000 / n  # ms per op forward
                    tb += (t[2] - t[1]) * 1000 / n  # ms per op backward
                mem = torch.cuda.memory_reserved() / 1E9 if torch.cuda.is_available() else 0  # (GB)
                s_in, s_out = (tuple(x.shape) if isinstance(x, torch.Tensor) else 'list' for x in (x, y))  # shapes
                p = sum(x.numel() for x in m.parameters()) if isinstance(m, nn.Module) else 0  # parameters
                print(f'{p:12}{flops:12.4g}{mem:>14.3f}{tf:14.4g}{tb:14.4g}{str(s_in):>24s}{str(s_out):>24s}')
                results.append([p, flops, mem, tf, tb, s_in, s_out])
            except Exception as e:
                print(e)
                results.append(None)
            torch.cuda.empty_cache()
    return results


def time_synchronized():
    # pytorch-accurate time
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    return time.time()


def scale_img(img, ratio=1.0, same_shape=False, gs=32):  # img(16,3,256,416)
    # scales img(bs,3,y,x) by ratio constrained to gs-multiple
    if ratio == 1.0:
        return img
    else:
        h, w = img.shape[2:]
        s = (int(h * ratio), int(w * ratio))  # new size
        img = F.interpolate(img, size=s, mode='bilinear', align_corners=False)  # resize
        if not same_shape:  # pad/crop img
            h, w = (math.ceil(x * ratio / gs) * gs for x in (h, w))
        return F.pad(img, [0, w - s[1], 0, h - s[0]], value=0.447)  # value = imagenet mean


def is_parallel(model):
    """
    check if model is in parallel mode.
    Returns True if model is of type DP or DDP
    """
    parallel_type = (
        nn.parallel.DataParallel,
        nn.parallel.DistributedDataParallel,
    )
    return isinstance(model, parallel_type)


class ModelEMA:
    """
    Model Exponential Moving Average from https://github.com/rwightman/pytorch-image-models
    Keep a moving average of everything in the model state_dict (parameters and buffers).
    This is intended to allow functionality like
    https://www.tensorflow.org/api_docs/python/tf/train/ExponentialMovingAverage
    A smoothed version of the weights is necessary for some training schemes to perform well.
    This class is sensitive where it is initialized in the sequence of model init,
    GPU assignment and distributed training wrappers.
    """

    def __init__(self, model, decay=0.9999, updates=0):
        """
        Args:
            model (nn.Module): model to apply EMA.
            decay (float): ema decay reate.
            updates (int): counter of EMA updates.
        """
        # Create EMA(FP32)
        self.ema = deepcopy(model.module if is_parallel(model) else model).eval()
        self.updates = updates
        # decay exponential ramp (to help early epochs)
        self.decay = lambda x: decay * (1 - math.exp(-x / 2000))
        for p in self.ema.parameters():
            p.requires_grad_(False)

    def update(self, model):
        # Update EMA parameters
        with torch.no_grad():
            self.updates += 1
            d = self.decay(self.updates)

            msd = model.module.state_dict() if is_parallel(model) else model.state_dict()  # model state_dict
            for k, v in self.ema.state_dict().items():
                if v.dtype.is_floating_point:
                    v *= d
                    v += (1.0 - d) * msd[k].detach()

    def update_attr(self, model, include=(), exclude=('process_group', 'reducer')):
        # Update EMA attributes
        # Copy attributes from b to a, options to only include [...] and to exclude [...]
        for k, v in model.__dict__.items():
            if (len(include) and k not in include) or k.startswith('_') or k in exclude:
                continue
            else:
                setattr(self.ema, k, v)


class EarlyStopping:
    # simple early stopper
    def __init__(self, patience=30, early_stop=True):
        self.best_fitness = 0.0  # i.e. mAP
        self.best_epoch = 1
        self.patience = patience or float('inf')  # num of eval epoch to wait after fitness stops improving to stop
        self.possible_stop = False  # possible stop may occur next epoch
        self.up_down = True
        self.early_stop = early_stop

    def __call__(self, epoch, fitness):
        if self.up_down:
            if fitness >= self.best_fitness:  # >= 0 to allow for early zero-fitness stage of training
                self.best_epoch = epoch
                self.best_fitness = fitness
        else:
            if fitness <= self.best_fitness:  # >= 0 to allow for early zero-fitness stage of training
                self.best_epoch = epoch
                self.best_fitness = fitness

        delta = epoch - self.best_epoch  # epochs without improvement
        self.possible_stop = delta >= (self.patience - 1)  # possible stop may occur next epoch
        stop = delta >= self.patience and self.early_stop  # stop training if patience exceeded
        if stop:
            logger.info(f'Stopping training early as no improvement observed in last {self.patience} epochs. '
                        f'Best results observed at epoch {self.best_epoch}, best model saved as best.pth.')
        return stop