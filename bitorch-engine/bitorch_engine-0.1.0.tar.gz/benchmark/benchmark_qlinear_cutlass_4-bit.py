import torch
from bitorch.layers import QLinear
from torch.nn import Parameter
from torch.profiler import profile, record_function, ProfilerActivity

import os, sys

from benchmark.util import get_cuda_benchmark_device

sys.path.insert(0, os.getcwd())
from bitorch_engine.layers.qlinear.nbit.cutlass import Q4LinearCutlass
from bitorch_engine.utils.quant_operators import nv_tensor_quant


def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)


def cuda_kernel_bentchmarking(num_input_features, num_hidden_fc, batch_size):
    # pass if not cuda ready
    if not torch.cuda.is_available(): return
    print("\nM:{}, N:{}, K:{}.".format(batch_size, num_hidden_fc, num_input_features))

    # setup data
    bits_binary_word = 32
    num_runs = 100

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features), requires_grad=False)
    weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features), requires_grad=False)

    # to gpu
    device = get_cuda_benchmark_device()
    input_data_cuda = to_device(input_data, device)
    weight_cuda = to_device(weight, device)

    # get QLinear output
    qlayer = QLinear(num_input_features, num_hidden_fc, bias=False, weight_quantization="sign", input_quantization="sign")
    qlayer.to(device)
    qlayer.weight = Parameter(weight_cuda, requires_grad=False)
    # warm up
    for i in range(num_runs):
        y_dot = qlayer(input_data_cuda)

    stream = torch.cuda.current_stream(device=device)
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    start.record(stream=stream)
    # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    for i in range(num_runs):
        y_dot = qlayer(input_data_cuda)
    # print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    end.record(stream=stream)
    torch.cuda.synchronize()
    dot_time = start.elapsed_time(end)/1000/num_runs
    print("Dot run time:\t%.6f s" % (dot_time))


    # 4-bit linear using cutlass kernel
    nbit_linear_layer = Q4LinearCutlass(in_channels=num_input_features, out_channels=num_hidden_fc, device=device)
    nbit_linear_layer.to(device)
    nbit_linear_layer.generate_quantized_weight()

    start.record(stream=stream)
    for i in range(num_runs):
        result = nbit_linear_layer(input_data_cuda, quantize_act=True)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("NV-quant for activation & 4-bit qlinear (cutlass) run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))

    input_data_cuda_cp = nv_tensor_quant(input_data_cuda, num_bits=4)[0].to(torch.int8).clone()
    start.record(stream=stream)
    # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    for i in range(num_runs):
        result_quantized_w = nbit_linear_layer(input_data_cuda_cp)
    # print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    # print(result_quantized_w)
    print("4-bit qlinear (cutlass) run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))



# M,K,N
CONFIG_DATA = [
    [32, 256, 256],
    [32, 512, 512],
    [32, 1024, 1024],
    [32, 2048, 2048],
    [64, 128, 128],
    [64, 256, 256],
    [64, 512, 512],
    [64, 1024, 1024],
    [64, 2048, 2048],
    [128, 128, 128],
    [128, 256, 256],
    [128, 512, 512],
    [128, 1024, 1024],
    [128, 2048, 2048],
    [256, 128, 128],
    [256, 256, 256],
    [256, 512, 512],
    [256, 1024, 1024],
    [256, 2048, 2048],
    [512, 128, 128],
    [512, 256, 256],
    [512, 512, 512],
    [512, 1024, 1024],
    [512, 2048, 2048],
    [1024, 128, 128],
    [1024, 256, 256],
    [1024, 512, 512],
    [1024, 1024, 1024],
    [1024, 2048, 2048],
    [1024, 4096, 4096],
    [2048, 2048, 2048],
    [2048, 4096, 4096],
    [4096, 256, 256],
    [4096, 512, 512],
    [4096, 1024, 1024],
    [4096, 2048, 2048],
    [4096, 4096, 4096],
    [4096, 1024, 4096],
    [4096, 4096, 1024],
]

if __name__ == '__main__':
    for config in CONFIG_DATA:
        cuda_kernel_bentchmarking(config[2], config[1], config[0])
