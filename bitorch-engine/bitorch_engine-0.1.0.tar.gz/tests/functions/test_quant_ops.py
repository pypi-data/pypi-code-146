import pytest
import torch
from tests.layers.util import get_cuda_test_device
from bitorch_engine.utils.quant_operators import nv_tensor_quant

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
def test_fp32toint4_cuda(num_input_features, num_hidden_fc, batch_size):
    from bitorch_engine.functions.cuda import fp32toint4
    print("\nM:{}, N:{}, K:{}.".format(batch_size, num_hidden_fc, num_input_features))

    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features), requires_grad=False)

    # to gpu
    device = get_cuda_test_device()
    input_data_cuda = to_device(input_data, device)
    num_runs = 100

    # warm up
    for i in range(num_runs):
        output_nv_int4 = nv_tensor_quant(input_data_cuda, num_bits=4)[0]

    stream = torch.cuda.current_stream(device=device)
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    start.record(stream=stream)
    for i in range(num_runs):
        output_nv_int4 = nv_tensor_quant(input_data_cuda, num_bits=4)[0]
    end.record(stream=stream)
    torch.cuda.synchronize()
    nv_q4_time = start.elapsed_time(end)/1000/num_runs
    # print("nv_q4 function run time:\t%.6f s" % (nv_q4_time))
    print(output_nv_int4)

    # nv quant function
    start.record(stream=stream)
    for i in range(num_runs):
        output_int4 = fp32toint4(input_data_cuda, device)
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end) / 1000 / num_runs
    # print("BE fp32tpint4 function run time:\t{:.6f} s, {:.2f} times speedup".format(rt, nv_q4_time / rt))
    print(output_int4)

    # assert torch.equal(result, result_quantized_w)
