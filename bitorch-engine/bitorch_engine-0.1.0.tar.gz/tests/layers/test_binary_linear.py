import pytest
import torch
import time
from bitorch.layers import QLinear

from torch.nn import Parameter
from bitorch_engine.utils.quant_operators import get_binary_row, get_binary_col
from bitorch_engine.layers.qlinear.binary.cpp import BinaryLinearCPP as BinaryLinearCPP
from tests.layers.util import to_device, get_cuda_test_device, get_cuda_test_device_id

if torch.cuda.is_available():
    from bitorch_engine.layers.qlinear.binary.cuda import BinaryLinearCuda as BinaryLinearCuda, BMM

"""
    Test binary inference layers
"""

# lower print threshold
torch.set_printoptions(threshold=100)


@pytest.mark.parametrize("num_input_features", [64, 512, 1024])
@pytest.mark.parametrize("num_hidden_fc", [20, 128])
@pytest.mark.parametrize("batch_size", [1, 64, 128])
def test_cpu_kernel(num_input_features, num_hidden_fc, batch_size):
    # setup data
    bits_binary_word = 32
    print("num_input_features:{}, num_hidden:{}, batch_size:{}".format(num_input_features, num_hidden_fc, batch_size))

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features))
    weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features))

    # get QLinear output
    qlayer = QLinear(num_input_features, num_hidden_fc, bias=False, weight_quantization="sign", input_quantization="sign")
    qlayer.weight = Parameter(weight)
    y_dot = qlayer(input_data)
    # print("QLinear out:")
    # print(y_dot)

    # dot output to xor output: dot_ouput = scale_range - 2 * xor_output
    # y_dot2xor = (num_input_features - y_dot)/2
    # print("QLinear -> XOR out:")
    # print(y_dot2xor)

    # run python version of "get_binary_row(...)"
    # We run both python and c++ on binary row and binary col generation
    # so that we could briefly compare them.
    size_binary = int(num_input_features//bits_binary_word)
    binary_row = torch.zeros((batch_size*size_binary), dtype=torch.int64)
    assert input_data.nelement() == num_input_features*batch_size, "incorrect input dim"
    binary_row = get_binary_row(input_data.reshape(-1,), binary_row, input_data.nelement(), bits_binary_word)
    # print("Binary row (Python):")
    # print(binary_row)

    # run python version of "get_binary_col(...)"
    binary_col = torch.zeros((num_hidden_fc*size_binary), dtype=torch.int64)
    binary_col = get_binary_col(weight.transpose(0,1).reshape(-1,), binary_col, num_input_features, num_hidden_fc, bits_binary_word)
    # print("Binary col (Python):")
    # print(binary_col)

    ## run c++ xor inference
    binary_layer = BinaryLinearCPP(num_input_features // bits_binary_word, num_hidden_fc)
    binary_layer.weight = Parameter(weight)
    xor_output = binary_layer(input_data, verbose=False)
    # print("C++ XOR out:")
    # print(xor_output)

    assert torch.equal(y_dot, xor_output)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("num_input_features", [128, 256, 384, 512, 640, 896, 1024, 2048])
@pytest.mark.parametrize("num_hidden_fc", [8, 16, 24, 32, 40, 128, 256, 384, 512, 1024, 2048])
@pytest.mark.parametrize("batch_size", [8, 16, 24, 32, 40, 128, 256, 384, 512, 1024, 2048])
def test_combined_cuda_kernel_output(num_input_features, num_hidden_fc, batch_size):
    print("\nM:{}, N:{}, K:{}.".format(batch_size, num_hidden_fc, num_input_features))
    # setup data
    bits_binary_word = 32

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features), requires_grad=False)
    weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features), requires_grad=False)

    # to gpu
    device = get_cuda_test_device()
    input_data_cuda = to_device(input_data, device)
    weight_cuda = to_device(weight, device)

    # get QLinear output
    qlayer = QLinear(num_input_features, num_hidden_fc, bias=False, weight_quantization="sign", input_quantization="sign")
    qlayer.to(device)
    qlayer.weight = Parameter(weight_cuda)
    y_dot = qlayer(input_data_cuda)
    y_dot = y_dot.clone()
    # print("CUDA QLinear out:")
    # print(y_dot)

    binary_layer_cuda = BinaryLinearCuda(num_input_features//bits_binary_word, num_hidden_fc, device=device)
    binary_layer_cuda.set_weight_data(weight_cuda)
    binary_layer_cuda.to(device)
    output_combined = binary_layer_cuda(input_data_cuda, bmm_type=BMM.ADAPTIVE, verbose=False)
    output_combined = output_combined.clone()
    # print("CUDA combined kernel out:")
    # print(output_combined)
    assert torch.equal(y_dot, output_combined)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("num_input_features", [128, 256, 384, 512, 640, 896, 1024, 2048])
@pytest.mark.parametrize("num_hidden_fc", [8, 16, 24, 32, 40, 128, 256, 384, 512, 1024, 2048])
@pytest.mark.parametrize("batch_size", [8, 16, 24, 32, 40, 128, 256, 384, 512, 1024, 2048])
def test_cuda_btc_output(num_input_features, num_hidden_fc, batch_size):
    print("\nM:{}, N:{}, K:{}.".format(batch_size, num_hidden_fc, num_input_features))
    # setup data
    bits_binary_word = 32

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features), requires_grad=False)
    weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features), requires_grad=False)

    # to gpu
    device = get_cuda_test_device()
    input_data_cuda = to_device(input_data, device)
    weight_cuda = to_device(weight, device)

    # get QLinear output
    qlayer = QLinear(num_input_features, num_hidden_fc, bias=False, weight_quantization="sign", input_quantization="sign")
    qlayer.to(device)
    qlayer.weight = Parameter(weight_cuda)
    y_dot = qlayer(input_data_cuda)
    y_dot = y_dot.clone()
    # print("CUDA QLinear out:")
    # print(y_dot)

    binary_layer_cuda = BinaryLinearCuda(num_input_features//bits_binary_word, num_hidden_fc, device=device)
    binary_layer_cuda.set_weight_data(weight_cuda)
    binary_layer_cuda.to(device)
    output_tensorcore = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BTC32, verbose=False)
    # print("CUDA BTC out:")
    # print(output_tensorcore)
    assert torch.equal(y_dot, output_tensorcore)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("num_input_features", [128, 256, 384, 512, 640, 896, 1024, 2048, 4096])
@pytest.mark.parametrize("num_hidden_fc", [8, 16, 24, 32, 40, 128, 256, 384, 512, 1024, 2048, 4096])
@pytest.mark.parametrize("batch_size", [8, 16, 24, 32, 40, 128, 256, 384, 512, 1024, 2048, 4096])
def test_cuda_BSTC_output(num_input_features, num_hidden_fc, batch_size):
    print("\nM:{}, N:{}, K:{}.".format(batch_size, num_hidden_fc, num_input_features))
    # setup data
    bits_binary_word = 32
    num_runs = 100

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features), requires_grad=False)
    weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features), requires_grad=False)

    # to gpu
    device = get_cuda_test_device()
    input_data_cuda = to_device(input_data, device)
    weight_cuda = to_device(weight, device)

    # get QLinear output
    qlayer = QLinear(num_input_features, num_hidden_fc, bias=False, weight_quantization="sign", input_quantization="sign")
    qlayer.to(device)
    qlayer.weight = Parameter(weight_cuda)

    for i in range(num_runs):
        y_dot = qlayer(input_data_cuda)
    y_dot = y_dot.clone()
    torch.cuda.synchronize()
    # print("CUDA QLinear out:")
    # print(y_dot)

    binary_layer_cuda = BinaryLinearCuda(num_input_features//bits_binary_word, num_hidden_fc, device=device)
    binary_layer_cuda.set_weight_data(weight_cuda)
    binary_layer_cuda.to(device)

    for i in range(num_runs):
        output_bstc32 = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BSTC32, verbose=False)
    torch.cuda.synchronize()
    # print("CUDA BSTC out:")
    # print(output_bstc32)

    assert torch.equal(y_dot, output_bstc32)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("num_input_features", [512])
@pytest.mark.parametrize("num_hidden_fc", [512])
@pytest.mark.parametrize("batch_size", [32])
def test_cuda_weight_packing(num_input_features, num_hidden_fc, batch_size):
    print("\nM:{}, N:{}, K:{}.".format(batch_size, num_hidden_fc, num_input_features))
    # setup data
    bits_binary_word = 32

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features), requires_grad=False)
    weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features), requires_grad=False)

    # to gpu
    device = get_cuda_test_device()
    input_data_cuda = to_device(input_data, device)
    weight_cuda = to_device(weight, device)

    # weight packing test
    binary_layer_cuda = BinaryLinearCuda(num_input_features // bits_binary_word, num_hidden_fc, device=device)
    binary_layer_cuda.set_weight_data(weight_cuda)
    binary_layer_cuda.to(device)

    # BTC
    packed_w_btc = BinaryLinearCuda.w_pack(weight_cuda,
                                              num_hidden_fc,
                                              num_input_features,
                                              bmm_type=BMM.BTC32,
                                              device_id=get_cuda_test_device_id(),
                                              verbose=False)

    output_btc_unpacked = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BTC32, verbose=False)
    binary_layer_cuda.set_quantized_weight_data(packed_w_btc)
    output_btc_packed = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BTC32, verbose=False)
    assert torch.equal(output_btc_unpacked, output_btc_packed)

    # BSTC32
    binary_layer_cuda.quantized_weight = None
    packed_w_bstc = BinaryLinearCuda.w_pack(weight_cuda,
                                              num_hidden_fc,
                                              num_input_features,
                                              bmm_type=BMM.BSTC32,
                                              device_id=get_cuda_test_device_id(),
                                              verbose=False)
    output_bstc_unpacked = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BSTC32, verbose=False)
    binary_layer_cuda.set_quantized_weight_data(packed_w_bstc)
    output_bstc_packed = binary_layer_cuda(input_data_cuda, bmm_type=BMM.BSTC32, verbose=False)
    assert torch.equal(output_bstc_unpacked, output_bstc_packed)


    ## run python version of "get_binary_row(...)"
    ## We run both python and c++ on binary row and binary col generation
    ## so that we could briefly compare them.
    # size_binary = int(num_input_features//bits_binary_word)
    # binary_row = torch.zeros((batch_size*size_binary), dtype=torch.int64)
    # assert input_data.nelement() == num_input_features*batch_size, "incorrect input dim"
    # binary_row = get_binary_row(input_data.reshape(-1,), binary_row, input_data.nelement(), bits_binary_word)
    # print("Binary row (Python):")
    # print(binary_row)
    ## run python version of "get_binary_col(...)"
    # size_binary = int(num_input_features//bits_binary_word)
    # binary_col = torch.zeros((num_hidden_fc*size_binary), dtype=torch.int64)
    # binary_col = get_binary_col(weight.transpose(0,1).reshape(-1,), binary_col, num_input_features, num_hidden_fc, bits_binary_word)
    # binary_col_cuda = to_device(binary_col, device)


@pytest.mark.parametrize("num_input_features", [64, 512, 1024])
@pytest.mark.parametrize("num_hidden_fc", [512, 1000])
@pytest.mark.parametrize("batch_size", [1, 32, 128, 512])
def test_cpu_weight_packing(num_input_features, num_hidden_fc, batch_size):
    # setup data
    bits_binary_word = 32

    print("num_input_features:{}, num_hidden:{}, batch_size:{}".format(num_input_features, num_hidden_fc, batch_size))

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features))
    weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features))

    # get QLinear output
    qlayer = QLinear(num_input_features, num_hidden_fc, bias=False, weight_quantization="sign", input_quantization="sign")
    qlayer.weight = Parameter(weight)
    start_time = time.time()
    y_dot = qlayer(input_data)
    # time_dot = time.time() - start_time
    # print("1-bit dot run time: %.6f s" % time_dot)

    ## run python version of "get_binary_col(...)"
    size_binary = int(num_input_features//bits_binary_word)
    binary_col = torch.zeros((num_hidden_fc * size_binary), dtype=torch.int64)
    binary_col = get_binary_col(weight.transpose(0, 1).reshape(-1,), binary_col, num_input_features, num_hidden_fc, bits_binary_word)

    ## run c++ xor inference
    binary_layer = BinaryLinearCPP(num_input_features // bits_binary_word, num_hidden_fc)
    binary_layer.set_weight_data(weight)
    assert torch.equal(binary_layer.opt_weight, weight)
    # start_time = time.time()
    xor_output = binary_layer(input_data, verbose=False)
    # time_xor = time.time() - start_time
    # print("C++ XOR unpacked weight run time: %.6f s" % time_xor)
    # using bit-packed weights
    # start_time = time.time()
    binary_layer.set_quantized_weight_data(binary_col)
    assert torch.equal(binary_layer.opt_weight, binary_col)
    xor_output_binarized_weights = binary_layer(input_data, verbose=False)
    # time_xor_binarized = time.time() - start_time
    # print("C++ XOR binarized weight run time: %.6f s" % time_xor_binarized)

    assert torch.equal(y_dot, xor_output)
    assert torch.equal(xor_output_binarized_weights, xor_output)


# @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
# @pytest.mark.parametrize("num_input_features", [128])
# @pytest.mark.parametrize("num_hidden_fc", [128])
# @pytest.mark.parametrize("batch_size", [128])
# def test_cutlass(num_input_features, num_hidden_fc, batch_size):
#     # setup data
#     bits_binary_word = 32
#     print("num_input_features:{}, num_hidden:{}, batch_size:{}".format(num_input_features, num_hidden_fc, batch_size))
#
#     # creating test data
#     input_data = torch.normal(0, 1, size=(batch_size, num_input_features))
#     weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features))
#
#     ## run python version of "get_binary_col(...)"
#     size_binary = int(num_input_features//bits_binary_word)
#     binary_col = torch.zeros((num_hidden_fc*size_binary), dtype=torch.int64)
#     binary_col = get_binary_col(weight.transpose(0,1).reshape(-1,), binary_col, num_input_features, num_hidden_fc, bits_binary_word)
#
#     # to gpu
#     device = get_cuda_test_device()
#     input_data_cuda = to_device(input_data, device)
#     weight_cuda = to_device(weight, device)
#
#     # get QLinear output
#     qlayer = QLinear(num_input_features, num_hidden_fc, bias=False, weight_quantization="sign",
#                      input_quantization="sign")
#     qlayer.to(device)
#     qlayer.weight = Parameter(weight_cuda)
#
#     start_time = time.time()
#     y_dot = qlayer(input_data_cuda)
#     torch.cuda.synchronize()
#     time_cuda_dot = time.time() - start_time
#     # dot output to xor output: dot_ouput = scale_range - 2 * xor_output
#     y_dot2xor = (num_input_features - y_dot)/2
#     print(y_dot2xor)
#     print("CUDA 1-bit-Dot run time: %.6f s" % time_cuda_dot)
#
#     # run CUTLASS xor inference
#     binary_layer_cutlass = BinaryLinearCutlass(num_input_features//bits_binary_word, num_hidden_fc)
#     binary_layer_cutlass.to(device)
#     start_time = time.time()
#     xor_output_cutlass = binary_layer_cutlass(input_data_cuda, weight_cuda, verbose=True)
#     torch.cuda.synchronize()
#     time_cutlass_xor = time.time() - start_time
#     print("CUDA XOR W-unpacked run time: %.6f s" % time_cutlass_xor)
#     print(xor_output_cutlass)
#
#     assert torch.equal(y_dot2xor, xor_output_cutlass)
