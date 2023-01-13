import os
import sys

import numpy as np
import torch
from bitorch.layers import QConv2d

from benchmark.util import get_cuda_benchmark_device

sys.path.insert(0, os.getcwd())
from bitorch_engine.layers.qconv.nbit.cutlass import Q4Conv2dCutlass
from bitorch_engine.utils.quant_operators import nv_tensor_quant

TEST_BATCH_SIZE = [1, 32, 64, 128, 256]

# Input shape: (batch size, num of input channels, h, w)
TEST_INPUT_DATA = [
    ((32, 56, 56), [32, 32],
     {"kernel_size": 1, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((64, 56, 56), [64, 256],
        {"kernel_size": 1, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
         "stride": 1, "dilation": 1}),
    ((64, 56, 56), [64, 64],
     {"kernel_size": 3, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((256, 56, 56), [256, 64],
     {"kernel_size": 1, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((256, 56, 56), [256, 512],
     {"kernel_size": 1, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((256, 56, 56), [256, 128],
     {"kernel_size": 1, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((128, 28, 28), [128, 128],
     {"kernel_size": 3, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((128, 28, 28), [128, 512],
     {"kernel_size": 1, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((256, 14, 14), [256, 256],
     {"kernel_size": 3, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((512, 7, 7), [512, 512],
     {"kernel_size": 3, "weight_quantization": "weightdorefa", "input_quantization": "inputdorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
]

def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)


def bit_conv_kernel_bentchmarking(input_shape, args, kwargs):
    # pass if not cuda ready
    if not torch.cuda.is_available(): return

    device = get_cuda_benchmark_device()
    stream = torch.cuda.current_stream(device=device)
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    num_runs = 100
    for BS in TEST_BATCH_SIZE:
        in_shape = (BS, input_shape[0], input_shape[1], input_shape[2])
        print("input_shape:{}, intput/output nums:{}, other args:{}".format(in_shape, args, kwargs))
        input = np.random.uniform(-1, 1, in_shape)
        input_tensor = torch.tensor(input).float()

        # to gpu
        input_tensor_cuda = to_device(input_tensor, device)
        padding = kwargs["padding"]
        kernel_size = kwargs["kernel_size"]
        stride = kwargs["stride"]
        dilation = kwargs["dilation"]

        # bitorch qconv2d
        qconv2d_layer = QConv2d(*args, **kwargs)
        qconv2d_layer.to(device)

        # warm up
        for i in range(num_runs):
            result_bitorch = qconv2d_layer(input_tensor_cuda)

        start.record(stream=stream)
        # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
        for i in range(num_runs):
            result_bitorch = qconv2d_layer(input_tensor_cuda)
        # print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
        end.record(stream=stream)
        torch.cuda.synchronize()
        dot_time = start.elapsed_time(end) / 1000 / num_runs
        # print(result_bitorch)
        print("QConv run time:\t%.6f s" % (dot_time))

        # 4-bit cutlass conv
        nbit_conv_layer = Q4Conv2dCutlass(in_channels=int(args[0]),
                                         out_channels=args[1],
                                         kernel_size=kernel_size,
                                         stride=stride,
                                         padding=padding,
                                         dilation=dilation,
                                         device=device)
        nbit_conv_layer.to(device)
        nbit_conv_layer.generate_quantized_weight()

        start.record(stream=stream)
        # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
        for i in range(num_runs):
            result = nbit_conv_layer(input_tensor_cuda, quantize_act=True)
        end.record(stream=stream)
        torch.cuda.synchronize()
        rt = start.elapsed_time(end) / 1000 / num_runs
        print("NV-quant for activation & 4-bit qconv (cutlass) run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time / rt))

        start.record(stream=stream)
        # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
        for i in range(num_runs):
            result = nbit_conv_layer(input_tensor_cuda)
        end.record(stream=stream)
        torch.cuda.synchronize()
        rt = start.elapsed_time(end) / 1000 / num_runs
        print("Ang-quant for activation & 4-bit qconv (cutlass) run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time / rt))


        input_tensor_cuda_cp = nv_tensor_quant(input_tensor_cuda, num_bits=4)[0].to(torch.int8).clone()
        start.record(stream=stream)
        # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
        for i in range(num_runs):
            result_quantized_w = nbit_conv_layer(input_tensor_cuda_cp, no_quant=True)
        end.record(stream=stream)
        torch.cuda.synchronize()
        rt = start.elapsed_time(end) / 1000 / num_runs
        result_quantized_w = result_quantized_w.view(result_quantized_w.size(0), result_quantized_w.size(3),
                                                     result_quantized_w.size(1), result_quantized_w.size(2))
        # print(result_quantized_w)
        print("4-bit qconv (cutlass) run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time / rt))


if __name__ == '__main__':
    for config in TEST_INPUT_DATA:
        bit_conv_kernel_bentchmarking(config[0], config[1], config[2])
