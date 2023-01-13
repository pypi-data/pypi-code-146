import os
from typing import Union, List

import torch


def activate_remote_pycharm_debug(port: int = 11004):
    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=port, stdoutToServer=True, stderrToServer=True)


def to_device(data: torch.Tensor, device: torch.device) -> Union[torch.Tensor, List[torch.Tensor]]:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)


def get_cuda_test_device_id():
    return int(os.environ.get("BIE_DEVICE", "0"))


def get_cuda_test_device():
    return torch.device(f"cuda:{get_cuda_test_device_id()}")
