import pytest
import torch
import numpy as np

from tests.layers.util import get_cuda_test_device

if torch.cuda.is_available():
    from bitorch_engine.layers.qconv.nbit.cutlass import Q4Conv2dCutlass


"""
    Test nbit inference layers
"""

# lower print threshold
torch.set_printoptions(threshold=100)


def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)

TEST_BATCH_SIZE = [1, 32, 64, 128, 256, 512]
# Input shape: (batch size, num of input channels, h, w)
TEST_INPUT_DATA = [
    ((32, 56, 56), [32, 32],
     {"kernel_size": 1, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((64, 56, 56), [64, 256],
        {"kernel_size": 1, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
         "stride": 1, "dilation": 1}),
    ((64, 56, 56), [64, 64],
     {"kernel_size": 3, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((256, 56, 56), [256, 64],
     {"kernel_size": 1, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((256, 56, 56), [256, 512],
     {"kernel_size": 1, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((256, 56, 56), [256, 128],
     {"kernel_size": 1, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((128, 28, 28), [128, 128],
     {"kernel_size": 3, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((128, 28, 28), [128, 512],
     {"kernel_size": 1, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((256, 14, 14), [256, 256],
     {"kernel_size": 3, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
    ((512, 7, 7), [512, 512],
     {"kernel_size": 3, "weight_quantization": "nv_quant", "input_quantization": "dorefa", "padding": 0,
      "stride": 1, "dilation": 1}),
]


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("input_shape, args, kwargs", TEST_INPUT_DATA)
@pytest.mark.parametrize("BS", TEST_BATCH_SIZE)
def test_q4_conv_cuda(input_shape, args, kwargs, BS):
    print("\n")
    print("input_shape:{}, intput/output nums:{}, other args:{}".format(input_shape, args, kwargs))
    input_shape = (BS, input_shape[0], input_shape[1], input_shape[2])
    input = np.random.uniform(-1, 1, input_shape)
    input_tensor = torch.tensor(input).float()

    # to gpu
    device = get_cuda_test_device()
    input_tensor_cuda = to_device(input_tensor, device)

    padding = kwargs["padding"]
    kernel_size = kwargs["kernel_size"]
    stride = kwargs["stride"]
    dilation = kwargs["dilation"]

    nbit_conv_layer = Q4Conv2dCutlass(in_channels=int(args[0]),
                                     out_channels=args[1],
                                     kernel_size=kernel_size,
                                     stride=stride,
                                     padding=padding,
                                     dilation=dilation,
                                     device=device)
    nbit_conv_layer.to(device)


    result = nbit_conv_layer(input_tensor_cuda)
    # print(result)

    # use quantized weight for inference
    nbit_conv_layer.generate_quantized_weight()
    result_quantized_w = nbit_conv_layer(input_tensor_cuda, quantize_act=True)
    print(result_quantized_w)

    # assert torch.equal(result, result_quantized_w)
