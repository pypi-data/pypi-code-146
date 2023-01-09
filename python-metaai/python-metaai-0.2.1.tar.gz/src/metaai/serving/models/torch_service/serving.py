from typing import Dict, Any
import warnings

try:
    import torch
except ImportError as ipt_e:
    warnings.warn(
        "import torch were error, please install this pkg manually or use command: pip install 'python-metaai[torch]'"
    )
    raise ipt_e

from metaai.serving import Model
from metaai.serving.utils import failed_response_with_break, success_response

PYTORCH_FILE = "model.pt"


class PyTorchModel(Model):
    def __init__(self, name: str, model_class):
        super().__init__(name)
        self.model = None
        self.model_cls = model_class
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def load(self) -> bool:

        self.model = self.model_cls.load_state_dict(
            torch.load(self.model_path, map_location=self.device)
        )
        #        self.model = torch.load(self.model_path, map_location=self.device)

        self.model.to(self.device)

        self.model.eval()
        self.ready = True
        return self.ready

    async def predict(self, request: Dict) -> Dict:
        inputs = []
        with torch.no_grad():
            try:
                inputs = torch.tensor(request["instances"]).to(self.device)
            except Exception as e:
                raise TypeError(
                    "Failed to initialize Torch Tensor from inputs: %s, %s"
                    % (e, inputs)
                )
            try:
                res = await self.model(inputs).tolist()
                return {"predictions": res}
            except Exception as e:
                failed_response_with_break(message="Failed to predict %s" % e)

    def _postprocess(self, response: Any) -> Dict:
        return success_response(response)
