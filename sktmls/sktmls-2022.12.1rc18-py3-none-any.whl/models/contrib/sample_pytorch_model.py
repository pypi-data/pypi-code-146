from typing import Any, Dict, List

import torch

from sktmls.models import MLSPyTorchModel, MLSModelError


class SamplePyTorchModel(MLSPyTorchModel):
    """
    MLS 모델 레지스트리에 등록되는 PyTorch 기반 샘플 클래스입니다.

    PyTorch로 학습한 모델을 `torch.jit.ScriptMoudle`형태로 변환 후 MLS 모델로 저장합니다.
    """

    def __init__(self, model, model_name: str, model_version: str, features: List[str]):
        """
        ## Args

        - model: PyTorch로 학습 후 `torch.jit.ScriptMoudle`형태로 변환한 객체 (`torch.jit.ScriptMoudle`로 변환 전 기존 torch 모델 device를 cpu로 변환해야 합니다.)
        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - features: (list(str)) 학습에 사용된 피쳐 리스트

        ## Example

        ```python
        model           # 학습이 완료된 PyTorch 모델 (상위 클래스 : `torch.nn.Module`)
        tensor_sample   # `model`의 input shape에 맞는 sample용 `torch.Tensor`

        script_model = torch.jit.trace(model.cpu(), tensor_sample)

        my_mls_torch_model = PytorchSampleModel(
            model=script_model,
            model_name="my_model",
            model_version="v1",
            features=["feature1", "feature2", "feature3", "feature4"],
        )

        result = my_mls_torch_model.predict(["value_1", "value_2", "value_3", "value_4"])
        ```
        """
        super().__init__(model, model_name, model_version, features)

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(self.features) != len(x):
            raise MLSModelError("`x`와 `features`의 길이가 다릅니다.")

        return {
            "items": [
                {
                    "id": "SAMPLE001",
                    "name": "PyTorch샘플모델",
                    "type": "PyTorch샘플타입",
                    "props": {"score": float(self.models[0](torch.tensor(x)).detach().numpy()[0])},
                }
            ]
        }
