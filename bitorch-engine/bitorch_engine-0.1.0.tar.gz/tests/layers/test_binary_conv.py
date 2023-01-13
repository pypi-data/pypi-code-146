import pytest
import torch
import numpy as np
import time
from bitorch.layers import QConv2d
from torch.nn import Parameter
from bitorch_engine.utils.quant_operators import get_binary_row, get_binary_col
from bitorch_engine.layers.qconv.binary.cpp import BinaryConv2dCPP as BinaryConv2dCPP
from tests.layers.util import get_cuda_test_device, get_cuda_test_device_id

if torch.cuda.is_available():
    from bitorch_engine.layers.qconv.binary.cuda import BinaryConv2dCuda as BinaryConv2dCuda
    from bitorch_engine.layers.qconv.binary.cuda import BCNV
#     from bitorch_engine.layers.qconv.binary.cutlass import BinaryConv2d as BinaryConv2dCutlass

"""
    Test binary inference layers
"""

# lower print threshold
torch.set_printoptions(threshold=10)


def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)

# Input shape: (batch size, num of input channels, h, w)
TEST_INPUT_DATA = [
    ((8, 128, 128, 128), [128, 64],
        {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
         "stride": 1, "dilation": 1}),
    ((1, 32, 64, 64), [32, 10],
     {"kernel_size": 3, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 2, "dilation": 1}),
    ((2, 32, 64, 64), [32, 64],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 3,
      "stride": 1, "dilation": 2}),
    ((8, 64, 16, 16), [64, 128],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((16, 128, 8, 8), [128, 256],
     {"kernel_size": 5, "weight_quantization": "sign", "input_quantization": "sign", "padding": 1,
      "stride": 2, "dilation": 1})
]

TEST_INPUT_DATA_BTC = [
    ((8, 128, 128, 128), [128, 64],
    {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
         "stride": 1, "dilation": 1}),
    ((8, 128, 64, 64), [128, 64],
     {"kernel_size": 3, "weight_quantization": "sign", "input_quantization": "sign", "padding": 1,
      "stride": 1, "dilation": 1}),
    ((1, 128, 64, 64), [128, 64],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 2,
      "stride": 1, "dilation": 2}),
    ((16, 128, 8, 8), [128, 256],
     {"kernel_size": 5, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 1, "dilation": 1})
]

TEST_INPUT_DATA_BCNV_32 = [
    ((8, 128, 64, 64), [128, 64],
     {"kernel_size": 3, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 1}),
    ((8, 128, 64, 64), [128, 64],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 1,
      "stride": 1})
]

TEST_INPUT_DATA_BCNV_64 = [
    ((8, 128, 64, 64), [128, 64],
     {"kernel_size": 3, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 1}),
    ((8, 128, 64, 64), [128, 64],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 1,
      "stride": 1})
]

TEST_INPUT_DATA_BCNV_BMMA_FMT = [
    ((8, 128, 64, 64), [128, 64],
     {"kernel_size": 3, "weight_quantization": "sign", "input_quantization": "sign", "padding": 0,
      "stride": 1}),
    ((8, 128, 64, 64), [128, 8],
     {"kernel_size": 1, "weight_quantization": "sign", "input_quantization": "sign", "padding": 1,
      "stride": 1})
]



@pytest.mark.parametrize("input_shape, args, kwargs", TEST_INPUT_DATA)
def test_binary_conv_inference_cpu(input_shape, args, kwargs):
    print("\n")
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))
    bits_binary_word = 32
    input = np.random.uniform(-1, 1, input_shape)
    layer = QConv2d(*args, **kwargs)
    input_tensor = torch.tensor(input).float()

    result_bitorch = layer(input_tensor)

    weight = layer.weight.clone()
    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    dilation = kwargs["dilation"]

    binary_conv_layer = BinaryConv2dCPP(in_channels=int(args[0]//bits_binary_word),
                                        out_channels=args[1],
                                        kernel_size=kernel_size,
                                        stride=stride,
                                        padding=padding,
                                        dilation=dilation)
    binary_conv_layer.set_weight_data(weight)
    result_bitorch_engine = binary_conv_layer(input_tensor, False)

    # NOTE: we don't do this anymore
    # convert [-1,+1] to [0,1] results
    # scale_range = input_shape[1] * kernel_size * kernel_size
    # result_bitorch = (scale_range - result_bitorch) / 2

    # test binarized weights
    size_binary = int(weight.nelement()//bits_binary_word)
    binarized_row = torch.zeros(size_binary, dtype=torch.int64)
    binarized_row = get_binary_row(weight.reshape(-1, ), binarized_row, weight.nelement(), bits_binary_word)
    binary_conv_layer.quantized_weight = binarized_row
    result_bitorch_engine_binarized_weight = binary_conv_layer(input_tensor, False)
    assert torch.equal(result_bitorch, result_bitorch_engine)
    assert torch.equal(result_bitorch_engine, result_bitorch_engine_binarized_weight)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("input_shape, args, kwargs", TEST_INPUT_DATA_BTC)
def test_binary_conv_inference_cuda_BTC(input_shape, args, kwargs):
    print("\n")
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))
    bits_binary_word = 32
    input = np.random.uniform(-1, 1, input_shape)
    input_tensor = torch.tensor(input).float()

    # to gpu
    device = get_cuda_test_device()
    input_tensor_cuda = to_device(input_tensor, device)
    layer = QConv2d(*args, **kwargs)
    layer.to(device)
    weight_cuda = layer.weight.clone()
    result_bitorch = layer(input_tensor_cuda)
    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    dilation = kwargs["dilation"]


    binary_conv_layer = BinaryConv2dCuda(in_channels=int(args[0]//bits_binary_word),
                                        out_channels=args[1],
                                        kernel_size=kernel_size,
                                        stride=stride,
                                        padding=padding,
                                        dilation=dilation,
                                        device=device)
    binary_conv_layer.to(device)
    binary_conv_layer.set_weight_data(weight_cuda)
    result_bitorch_engine = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BTC32, verbose=False)
    assert torch.equal(result_bitorch, result_bitorch_engine)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("input_shape, args, kwargs", TEST_INPUT_DATA)
def test_binary_conv_inference_cuda_BSTC(input_shape, args, kwargs):
    print("\n")
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))
    bits_binary_word = 32
    input = np.random.uniform(-1, 1, input_shape)
    input_tensor = torch.tensor(input).float()

    # to gpu
    device = get_cuda_test_device()
    input_tensor_cuda = to_device(input_tensor, device)
    layer = QConv2d(*args, **kwargs)
    layer.to(device)
    weight_cuda = layer.weight.clone()

    result_bitorch = layer(input_tensor_cuda)

    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    dilation = kwargs["dilation"]

    binary_conv_layer = BinaryConv2dCuda(in_channels=int(args[0]//bits_binary_word),
                                        out_channels=args[1],
                                        kernel_size=kernel_size,
                                        stride=stride,
                                        padding=padding,
                                        dilation=dilation,
                                        device=device)
    binary_conv_layer.to(device)
    binary_conv_layer.set_weight_data(weight_cuda)
    result_bitorch_engine_BSTC = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BSTC32, verbose=False)
    assert torch.equal(result_bitorch, result_bitorch_engine_BSTC)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("input_shape, args, kwargs", TEST_INPUT_DATA_BCNV_32)
def test_binary_conv_inference_cuda_BCNV_32(input_shape, args, kwargs):
    print("\n")
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))
    bits_binary_word = 32
    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    input = np.random.uniform(-1, 1, input_shape)
    input_tensor = torch.tensor(input).float()

    # to gpu
    device = get_cuda_test_device()
    input_tensor_cuda = to_device(input_tensor, device)
    layer = QConv2d(*args, **kwargs)
    layer.to(device)

    result_bitorch = layer(input_tensor_cuda)

    weight_cuda = layer.weight.clone()
    binary_conv_layer = BinaryConv2dCuda(in_channels=int(args[0]//bits_binary_word),
                                        out_channels=args[1],
                                        kernel_size=kernel_size,
                                        stride=stride,
                                        padding=padding,
                                        device=device)
    binary_conv_layer.to(device)
    binary_conv_layer.set_weight_data(weight_cuda)
    result_bitorch_engine = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BCNV_32, verbose=False)
    print(result_bitorch_engine.shape)
    assert torch.equal(result_bitorch, result_bitorch_engine)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("input_shape, args, kwargs", TEST_INPUT_DATA_BCNV_64)
def test_binary_conv_inference_cuda_BCNV_64(input_shape, args, kwargs):
    print("\n")
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))
    bits_binary_word = 32
    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    input = np.random.uniform(-1, 1, input_shape)
    input_tensor = torch.tensor(input).float()

    # to gpu
    device = get_cuda_test_device()
    input_tensor_cuda = to_device(input_tensor, device)
    layer = QConv2d(*args, **kwargs)
    layer.to(device)

    result_bitorch = layer(input_tensor_cuda)

    weight_cuda = layer.weight.clone()
    binary_conv_layer = BinaryConv2dCuda(in_channels=int(args[0]//bits_binary_word),
                                        out_channels=args[1],
                                        kernel_size=kernel_size,
                                        stride=stride,
                                        padding=padding,
                                        device=device)
    binary_conv_layer.to(device)
    binary_conv_layer.set_weight_data(weight_cuda)
    result_bitorch_engine = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BCNV_64, verbose=False)
    print(result_bitorch_engine.shape)
    assert torch.equal(result_bitorch, result_bitorch_engine)




@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("input_shape, args, kwargs", TEST_INPUT_DATA_BCNV_BMMA_FMT)
def test_binary_conv_inference_cuda_BCNV_BMMA_FMT(input_shape, args, kwargs):
    print("\n")
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))
    bits_binary_word = 32
    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    input = np.random.uniform(-1, 1, input_shape)
    input_tensor = torch.tensor(input).float()

    # to gpu
    device = get_cuda_test_device()
    input_tensor_cuda = to_device(input_tensor, device)
    layer = QConv2d(*args, **kwargs)
    layer.to(device)

    result_bitorch = layer(input_tensor_cuda)

    weight_cuda = layer.weight.clone()
    binary_conv_layer = BinaryConv2dCuda(in_channels=int(args[0]//bits_binary_word),
                                        out_channels=args[1],
                                        kernel_size=kernel_size,
                                        stride=stride,
                                        padding=padding,
                                        device=device)
    binary_conv_layer.to(device)
    binary_conv_layer.set_weight_data(weight_cuda)
    result_bitorch_engine = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BCNV_BMMA_FMT, verbose=False)
    print(result_bitorch_engine.shape)
    assert torch.equal(result_bitorch, result_bitorch_engine)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("input_shape, args, kwargs", TEST_INPUT_DATA_BTC)
def test_binary_conv_weight_packing(input_shape, args, kwargs):
    print("\n")
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))
    bits_binary_word = 32
    input = np.random.uniform(-1, 1, input_shape)
    input_tensor = torch.tensor(input).float()

    # to gpu
    device = get_cuda_test_device()
    input_tensor_cuda = to_device(input_tensor, device)
    layer = QConv2d(*args, **kwargs)
    layer.to(device)
    weight_cuda = layer.weight.clone()
    result_bitorch = layer(input_tensor_cuda)
    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    dilation = kwargs["dilation"]

    binary_conv_layer = BinaryConv2dCuda(in_channels=int(args[0]//bits_binary_word),
                                        out_channels=args[1],
                                        kernel_size=kernel_size,
                                        stride=stride,
                                        padding=padding,
                                        dilation=dilation,
                                        device=device)
    binary_conv_layer.to(device)

    # BTC
    binary_conv_layer.set_weight_data(weight_cuda)
    result_btc_unpacked = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BTC32, verbose=False)
    binary_conv_layer.generate_quantized_weight()
    result_btc_packed = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BTC32, verbose=False)
    assert torch.equal(result_bitorch, result_btc_packed)
    assert torch.equal(result_btc_unpacked, result_btc_packed)

    # BSTC
    packed_w_bstc = BinaryConv2dCuda.w_pack(weight_cuda,
                                           args[1],  # m
                                           args[0] * kernel_size * kernel_size,  # k
                                           bcnv_type=BCNV.BMM_BSTC32,
                                           device_id=get_cuda_test_device_id(),
                                           verbose=False)
    binary_conv_layer.quantized_weight = None
    result_bstc_unpacked = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BSTC32, verbose=False)
    binary_conv_layer.set_quantized_weight_data(packed_w_bstc)
    result_bstc_packed = binary_conv_layer(input_tensor_cuda, bcnv_type=BCNV.BMM_BSTC32, verbose=False)
    assert torch.equal(result_bitorch, result_bstc_packed)
    assert torch.equal(result_bstc_unpacked, result_bstc_packed)
