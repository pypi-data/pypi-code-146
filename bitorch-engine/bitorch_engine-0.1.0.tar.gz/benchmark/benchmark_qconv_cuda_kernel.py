import os
import sys

import numpy as np
import torch
from bitorch.layers import QConv2d

from benchmark.util import get_cuda_benchmark_device
from torch._utils import _get_device_index as _torch_get_device_index

sys.path.insert(0, os.getcwd())
from bitorch_engine.layers.qconv.binary.cuda import BinaryConv2dCuda as BinaryConv2dCuda
from bitorch_engine.layers.qconv.binary.cuda import BCNV


def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)


def cuda_kernel_bentchmarking(input_shape, args, kwargs):
    # pass if not cuda ready
    if not torch.cuda.is_available(): return
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))

    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    dilation = kwargs["dilation"]
    bits_binary_word = 32
    num_runs = 100

    output_edge = int((input_shape[2] - kernel_size + 2 * padding) / stride + 1)
    n = output_edge * output_edge
    m = args[1]
    k = args[0] * kernel_size * kernel_size
    print("M:{}, N:{}, K:{}.".format(m, n, k))

    input = np.random.uniform(-1, 1, input_shape)
    input_tensor = torch.tensor(input).float()

    # to gpu
    print("Using gpu: {}".format(get_cuda_benchmark_device()))
    device = get_cuda_benchmark_device()
    input_tensor_cuda = to_device(input_tensor, device)
    qconv2d_layer = QConv2d(*args, **kwargs)
    qconv2d_layer.to(device)
    weight_cuda = qconv2d_layer.weight

    # warm up
    for i in range(num_runs):
        result_bitorch = qconv2d_layer(input_tensor_cuda)

    stream = torch.cuda.current_stream(device=device)
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    start.record(stream=stream)
    # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    for i in range(num_runs):
        result_bitorch = qconv2d_layer(input_tensor_cuda)
    # print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    end.record(stream=stream)
    torch.cuda.synchronize()
    dot_time = start.elapsed_time(end)/1000/num_runs
    print("QConv run time:\t%.6f s" % (dot_time))


    ##########################################
    ## Test uppacked weights and activation ##
    ##########################################
    ## run CUDA xor inference
    ## Init
    binary_conv_layer = BinaryConv2dCuda(in_channels=int(args[0]/bits_binary_word),
                                        out_channels=args[1],
                                        kernel_size=kernel_size,
                                        stride=stride,
                                        padding=padding,
                                        dilation=dilation,
                                        device=device)
    binary_conv_layer.set_weight_data(weight_cuda)
    # binary_conv_layer.to(device)

    # BSTC-32
    start.record(stream=stream)
    for i in range(num_runs):
        result_bitorch_engine_BSTC = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BSTC32, verbose=False)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("BSTC run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))


    ## BTC
    start.record(stream=stream)
    # with torch.autograd.profiler.profile(use_cuda=True) as prof:
    for i in range(num_runs):
        result_bitorch_engine = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BTC32, verbose=False)
    # print(prof)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("BTC run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))
    # print(result_bitorch)
    # print(result_bitorch_engine)
    # assert torch.equal(result_bitorch, result_bitorch_engine)


    ############################
    ## Test binarized weight  ##
    ############################

    # BSTC-32
    packed_w_bstc = BinaryConv2dCuda.w_pack(weight_cuda,
                                           m,
                                           k,
                                           bcnv_type=BCNV.BMM_BSTC32,
                                           device_id=_torch_get_device_index(device),
                                           verbose=False)
    binary_conv_layer.set_quantized_weight_data(packed_w_bstc)

    start.record(stream=stream)
    for i in range(num_runs):
        result_bstc_packed = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BSTC32, verbose=False)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("BSTC PACKED:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))


    ## BTC
    packed_w_btc = BinaryConv2dCuda.w_pack(weight_cuda,
                                              m,
                                              k,
                                              bcnv_type=BCNV.BMM_BTC32,
                                              device_id=_torch_get_device_index(device),
                                              verbose=False)
    binary_conv_layer.set_quantized_weight_data(packed_w_btc)

    start.record(stream=stream)
    # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    for i in range(num_runs):
        result_btc_packed = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BTC32, verbose=False)
    # print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("BTC PACKED:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))


    ## bconv-32

    binary_conv_layer.quantized_weight = None
    start.record(stream=stream)
    # with torch.autograd.profiler.profile(use_cuda=True) as prof:
    for i in range(num_runs):
        result_bitorch_engine = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BCNV_32, verbose=False)
    # print(prof)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("Bconv-32 run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))

    ## bconv-64
    binary_conv_layer.quantized_weight = None
    start.record(stream=stream)
    # with torch.autograd.profiler.profile(use_cuda=True) as prof:
    for i in range(num_runs):
        result_bitorch_engine = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BCNV_64, verbose=False)
    # print(prof)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end) / 1000 / num_runs
    print("Bconv-64 run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time / rt))

    ## bconv-BMMA-fmt
    binary_conv_layer.quantized_weight = None
    start.record(stream=stream)
    # with torch.autograd.profiler.profile(use_cuda=True) as prof:
    for i in range(num_runs):
        result_bitorch_engine = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BCNV_BMMA_FMT, verbose=False)
    # print(prof)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end) / 1000 / num_runs
    print("Bconv-BMMA-fmt run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time / rt))

        


TEST_INPUT_DATA_BTC = [
    ((8, 128, 128, 128), [128, 64],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((16, 1024, 128, 128), [1024, 64],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((64, 128, 64, 64), [128, 256],
     {"kernel_size": 3, "weight_quantization": "sign", "input_quantization": "sign", "padding": 1,
      "stride": 1, "dilation": 1}),
    ((128, 512, 64, 64), [512, 128],
     {"kernel_size": 3, "weight_quantization": "sign", "input_quantization": "sign", "padding": 1,
      "stride": 1, "dilation": 1}),
    ((32, 128, 64, 64), [128, 64],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 2,
      "stride": 1, "dilation": 1}),
    ((16, 512, 32, 32), [512, 256],
     {"kernel_size": 3, "weight_quantization": "sign", "input_quantization": "sign", "padding": 1,
      "stride": 2, "dilation": 1}),
    ((16, 128, 8, 8), [128, 256],
     {"kernel_size": 5, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 1, "dilation": 1}),
]


if __name__ == '__main__':
    for config in TEST_INPUT_DATA_BTC:
        cuda_kernel_bentchmarking(config[0], config[1], config[2])
