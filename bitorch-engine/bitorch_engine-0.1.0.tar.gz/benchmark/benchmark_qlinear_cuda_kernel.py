import torch
from bitorch.layers import QLinear
from torch.nn import Parameter
from torch.profiler import profile, record_function, ProfilerActivity

import os, sys

from benchmark.util import get_cuda_benchmark_device, get_cuda_benchmark_device_id

sys.path.insert(0, os.getcwd())
from bitorch_engine.layers.qlinear.binary.cuda import BinaryLinearCuda as BinaryLinearCuda, BMM

VERBOSE = False

def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)


def cuda_kernel_benchmarking(num_input_features, num_hidden_fc, batch_size):
    # pass if not cuda ready
    if not torch.cuda.is_available(): return
    print("\nM:{}, N:{}, K:{}.".format(batch_size, num_hidden_fc, num_input_features))

    # setup data
    bits_binary_word = 32
    num_runs = 10

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
    qlayer.weight = Parameter(weight_cuda)

    # warm-up
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
    y_dot = y_dot.clone()
    dot_time = start.elapsed_time(end)/1000/num_runs
    print("Dot run time:\t%.6f s" % (dot_time))
    if VERBOSE:
        print("CUDA QLinear out: {}".format(y_dot))

    ##########################################
    ## Test uppacked weights and activation ##
    ##########################################
    ## run CUDA xor inference
    ## Init
    binary_layer_cuda = BinaryLinearCuda(num_input_features//bits_binary_word, num_hidden_fc, device=device)
    binary_layer_cuda.set_weight_data(weight_cuda)
    binary_layer_cuda.to(device)


    # BSTC-32
    start.record(stream=stream)
    for i in range(num_runs):
        output_bstc = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BSTC32, verbose=False)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("BSTC-32 run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))
    if VERBOSE:
        print("CUDA BSTC-32 out: {}".format(output_bstc))


    ## BTC
    start.record(stream=stream)
    # with torch.autograd.profiler.profile(use_cuda=True) as prof:
    for i in range(num_runs):
        output_tensorcore = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BTC32, verbose=False)
    # print(prof)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("BTC run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))
    if VERBOSE:
        print("CUDA BTC out: {}".format(output_tensorcore))

    # # COMBINED
    # start.record(stream=stream)
    # for i in range(num_runs):
    #     output_combined = binary_layer_cuda(input_data_cuda, bmm_type=BMM.COMBINED, verbose=False)
    # end.record(stream=stream)
    # torch.cuda.synchronize()
    # rt = start.elapsed_time(end)/1000/num_runs
    # print("Combined time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))
    # if VERBOSE:
    #     print("Combined out: {}".format(output_combined))


    ############################
    ## Test binarized weight  ##
    ############################

    # BSTC-32
    packed_w_bstc = BinaryLinearCuda.w_pack(weight_cuda,
                                          num_hidden_fc,
                                          num_input_features,
                                          bmm_type=BMM.BSTC32,
                                          device_id=get_cuda_benchmark_device_id(),
                                          verbose=False)
    binary_layer_cuda.set_quantized_weight_data(packed_w_bstc)
    start.record(stream=stream)
    for i in range(num_runs):
        output = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BSTC32, verbose=False)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("BSTC-32 packed:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))
    if VERBOSE:
        print("BSTC-32 packed out: {}".format(output))


    ## BTC
    packed_w_btc = BinaryLinearCuda.w_pack(weight_cuda,
                                          num_hidden_fc,
                                          num_input_features,
                                          bmm_type=BMM.BTC32,
                                          device_id=get_cuda_benchmark_device_id(),
                                          verbose=False)
    binary_layer_cuda.set_quantized_weight_data(packed_w_btc)
    start.record(stream=stream)
    # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    for i in range(num_runs):
        output = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BTC32, verbose=False)
    # print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("BTC packed:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))
    if VERBOSE:
        print("BTC packed out: {}".format(output))

    # # COMBINED
    # packed_w_comb = BinaryLinearCuda.w_pack(weight_cuda,
    #                                       num_hidden_fc,
    #                                       num_input_features,
    #                                       bmm_type=BMM.COMBINED,
    #                                       device_id=get_cuda_benchmark_device_id(),
    #                                       verbose=False)
    # start.record(stream=stream)
    # for i in range(num_runs):
    #     output = binary_layer_cuda(input_data_cuda, packed_w_comb, bmm_type=BMM.COMBINED, verbose=False)
    # end.record(stream=stream)
    # torch.cuda.synchronize()
    # rt = start.elapsed_time(end)/1000/num_runs
    # print("Comb packed:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))
    # if VERBOSE:
    #     print("Comb packed out: {}".format(output))

# M,K,N
CONFIG_DATA = [
    [8, 128, 128],
    [8, 256, 256],
    [8, 512, 512],
    [8, 1024, 1024],
    [8, 2048, 2048],
    [16, 128, 128],
    [16, 256, 256],
    [16, 512, 512],
    [16, 1024, 1024],
    [16, 2048, 2048],
    [32, 128, 128],
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
    [256, 256, 256],
    [256, 512, 512],
    [256, 1024, 1024],
    [256, 2048, 2048],
    [512, 256, 256],
    [512, 512, 512],
    [512, 1024, 1024],
    [512, 2048, 2048],
    [1024, 2048, 2048],
    [2048, 2048, 2048],
    [4096, 4096, 4096],
]

if __name__ == '__main__':
    for config in CONFIG_DATA:
        cuda_kernel_benchmarking(config[2], config[1], config[0])
