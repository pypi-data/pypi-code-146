import onnxruntime as ort

from ..core import Runner


class ONNXRunner(Runner):

    def __init__(self, onnx_file, **kwargs) -> None:
        self.onnx_file = onnx_file

        self.session = ort.InferenceSession(self.onnx_file, **kwargs)

    def run(self, input_dict):
        output_dict = self.session.run(None, input_dict)

        return output_dict
