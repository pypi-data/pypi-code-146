from typing import Any, Dict, List

import numpy as np

from sktmls.models import MLSGenericModel


class SampleGenericModel(MLSGenericModel):
    """
    샘플 제네릭 모델입니다.

    같은 `features`를 사용하는 모델을 여러 개 추론하여 y score의 합이 1.0이 넘는 경우 결과를 반환합니다.
    """

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if not self.models:
            return {"items": []}

        try:
            y0 = self.models[0].predict(np.array([x])).flatten().tolist()[0]
            y1 = self.models[1].predict(np.array([x])).flatten().tolist()[0]
            y = y0 + y1
        except Exception:
            return {"items": []}

        if y < 1.0:
            return {"items": []}

        return {
            "items": [{"id": "SAMPLE001", "name": "샘플상품", "props": {"context": "샘플컨텍스트", "score": y}, "type": "샘플타입"}]
        }
