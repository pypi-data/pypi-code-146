import os
import torch


def get_cuda_benchmark_device_id():
    return int(os.environ.get("BIE_DEVICE", "0"))


def get_cuda_benchmark_device():
    return torch.device(f"cuda:{get_cuda_benchmark_device_id()}")
