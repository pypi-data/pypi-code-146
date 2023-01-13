import time
import pytest
import torch
from bitorch_engine.layers.qlinear.nbit.cutlass import Q4LinearCutlass
from tests.layers.util import get_cuda_test_device

"""
    Test nbit inference layers
"""

# lower print threshold
torch.set_printoptions(threshold=100)


def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("num_input_features", [32, 64, 96, 128, 160, 192, 224, 256, 512])
@pytest.mark.parametrize("num_hidden_fc", [32, 64, 96, 128, 160, 192, 224, 256, 512])
@pytest.mark.parametrize("batch_size", [32, 64, 96, 128, 160, 192, 224, 256, 512])
def test_q4_linear_cuda(num_input_features, num_hidden_fc, batch_size):
    print("\nM:{}, N:{}, K:{}.".format(batch_size, num_hidden_fc, num_input_features))

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features), requires_grad=False)

    # to gpu
    device = get_cuda_test_device()
    input_data_cuda = to_device(input_data, device)

    nbit_linear_layer = Q4LinearCutlass(in_channels=num_input_features,
                                       out_channels=num_hidden_fc,
                                       device=device)
    nbit_linear_layer.to(device)

    start_time = time.time()
    result = nbit_linear_layer(input_data_cuda)
    torch.cuda.synchronize()
    time_engine = time.time() - start_time
    # print(result)
    print("bitorch-engine 4-bit qlinear (CUTLASS) run time: %.6f s" % time_engine)

    # use quantized weight for inference
    nbit_linear_layer.generate_quantized_weight()
    start_time = time.time()
    result_quantized_w = nbit_linear_layer(input_data_cuda)
    torch.cuda.synchronize()
    time_engine = time.time() - start_time
    print(result_quantized_w)
    print("bitorch-engine 4-bit qlinear quantized w (CUTLASS) run time: %.6f s" % time_engine)

    assert torch.equal(result, result_quantized_w)
