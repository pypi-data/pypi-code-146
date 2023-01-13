import dataclasses
import enum
import logging
import typing
import torch.nn
import torch.utils.data
import irisml.core
import irisml.tasks.train
import numpy as np
import onnxruntime

logger = logging.getLogger(__name__)


class OrtExecutionProvider(enum.Enum):
    CPU_ONLY = 0
    CUDA_AND_CPU = 1


class OrtPredictor:
    def __init__(self, model_bytes: bytes, execution_provider: OrtExecutionProvider):
        providers_list = ["CPUExecutionProvider"]
        if execution_provider == OrtExecutionProvider.CUDA_AND_CPU:
            providers_list = ["CUDAExecutionProvider"] + providers_list
        elif execution_provider != OrtExecutionProvider.CPU_ONLY:
            raise RuntimeError(f"Unexpected value for OrtExecutionProvider: {execution_provider}")

        session = onnxruntime.InferenceSession(model_bytes, providers=providers_list)

        model_inputs = session.get_inputs()
        if len(model_inputs) > 1:
            raise RuntimeError(f"Basic onnx prediction task only supports one input, instead found {len(model_inputs)} : {[model_input.name for model_input in model_inputs]})")
        if len(session.get_outputs()) > 1:
            raise RuntimeError(f"Basic onnx prediction task only supports one output, instead found {len(session.get_outputs())} : {[model_output.name for model_output in session.get_outputs()]})")

        self._session = session
        self._input_name = model_inputs[0].name
        self._input_shape = tuple(model_inputs[0].shape)
        self._output_names = [model_output.name for model_output in self._session.get_outputs()]

    def predict(self, dataloader: torch.utils.data.DataLoader):
        if dataloader.batch_size != 1:
            raise RuntimeError(f"Currently only batch size 1 is supported, instead found configured batch size {dataloader.batch_size}")

        results = []
        targets = []
        for inference_input, inference_target in dataloader:
            targets.append(inference_target)

            inference_input_np = inference_input.numpy()
            if inference_input_np.shape != self._input_shape:
                raise RuntimeError(f"Shape of inference input ({inference_input_np.shape}) does not match traced model input shape ({self._input_shape})")

            result = self._session.run(self._output_names, {self._input_name: inference_input_np})
            results.extend(result)

        return torch.from_numpy(np.concatenate(results)), torch.cat(targets)


class Task(irisml.core.TaskBase):
    """Predict using a given onnx model traced with the export_onnx task"""
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset
        transform: torch.nn.Module
        onnx_model_bytes: bytes

    @dataclasses.dataclass
    class Config:
        device: typing.Literal['cpu', 'cuda']

    @dataclasses.dataclass
    class Outputs:
        predictions: typing.Union[typing.List, torch.Tensor] = dataclasses.field(default_factory=list)
        targets: typing.Optional[typing.Union[typing.List, torch.Tensor]] = None

    def execute(self, inputs):
        results = self._predict(inputs)
        return self.Outputs(results[0], results[1])

    def _predict(self, inputs):
        dataloader: torch.utils.data.DataLoader \
            = irisml.tasks.train.build_dataloader.build_dataloader(inputs.dataset, inputs.transform, batch_size=1, shuffle=False, drop_last=False)
        predictor = OrtPredictor(inputs.onnx_model_bytes, self._get_execution_provider())

        results = predictor.predict(dataloader)
        if len(inputs.dataset) != len(results[0]):
            raise RuntimeError(f"Didn't get the expected number of prediction results. Expected: {len(inputs.dataset)}. Actual: {len(results[0])}")

        return results

    def _get_execution_provider(self) -> OrtExecutionProvider:
        """Get an ORT execution provider name based on the configuration."""
        if self.config.device == "cpu":
            return OrtExecutionProvider.CPU_ONLY
        elif self.config.device == "cuda":
            return OrtExecutionProvider.CUDA_AND_CPU
        else:
            raise RuntimeError(f"Unexpected value for config.device_name: {self.config.device}")
