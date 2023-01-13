import pytest
import torch
from bitorch import RuntimeMode
from bitorch.layers import QLinear, convert
from torch.nn import Parameter

from bitorch_engine import initialize
from bitorch_engine.layers.qlinear import QLinearInf
from bitorch_engine.layers.qlinear.binary.cpp import BinaryLinearCPP
from tests.layers.util import to_device, activate_remote_pycharm_debug, get_cuda_test_device

initialize()

# activate_remote_pycharm_debug()


MODES_TO_TEST = [
    (RuntimeMode.INFERENCE_AUTO, QLinearInf),
    (RuntimeMode.CPU, BinaryLinearCPP),
]
if torch.cuda.is_available():
    from bitorch_engine.layers.qlinear.binary.cuda import BinaryLinearCuda
    MODES_TO_TEST.append((RuntimeMode.GPU, BinaryLinearCuda))


@pytest.mark.parametrize("num_input_features", [64, 512, 1024])
@pytest.mark.parametrize("num_hidden_fc", [20, 128])
@pytest.mark.parametrize("batch_size", [1, 64, 128])
@pytest.mark.parametrize("mode, class_", MODES_TO_TEST)
@pytest.mark.parametrize("kwargs", [
    {"bias": False, "weight_quantization": "sign", "input_quantization": "sign"},
])
def test_q_linear_integration(num_input_features, num_hidden_fc, batch_size, mode, class_, kwargs):
    # creating test data
    input_data = torch.normal(0, 1, size=(batch_size, num_input_features))
    weight = torch.normal(0, 1, size=(num_hidden_fc, num_input_features))

    # get QLinear output
    q_linear = QLinear(num_input_features, num_hidden_fc, **kwargs)
    q_linear.weight = Parameter(weight)
    y_dot = q_linear(input_data)

    device = None
    if (mode == RuntimeMode.GPU) or (mode == RuntimeMode.INFERENCE_AUTO and torch.cuda.is_available()):
        # these are the cases where we use CUDA, so we need to pass a device
        device = get_cuda_test_device()
        input_data = to_device(input_data, device=device)

    convert(q_linear, mode, device=device, verbose=True)

    assert input_data.device == q_linear.weight.device
    assert isinstance(q_linear, class_)

    y_dot_2 = q_linear(input_data)
    y_dot_2_cpu = y_dot_2.to(device=torch.device("cpu"))
    assert torch.equal(y_dot, y_dot_2_cpu)
