from typing import Any, Dict, List

import numpy as np

from sktmls.models import MLSLightGBMModel


class SampleModel(MLSLightGBMModel):
    """
    단일 LightGBM을 사용하는 샘플 모델입니다.

    모델을 추론하여 y score가 0.2 이상인 경우 결과를 반환합니다.
    """

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if not self.models:
            return {"items": []}

        try:
            y = self.models[0].predict(np.array([x])).flatten().tolist()[0]
        except Exception:
            return {"items": []}

        if y < 0.2:
            return {"items": []}

        return {
            "items": [{"id": "SAMPLE001", "name": "샘플상품", "props": {"context": "샘플컨텍스트", "score": y}, "type": "샘플타입"}]
        }
