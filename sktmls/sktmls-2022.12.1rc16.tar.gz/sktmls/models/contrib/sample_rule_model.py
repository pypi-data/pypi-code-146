from typing import Any, Dict, List

from sktmls.models import MLSModelError, MLSRuleModel


class SampleRuleModel(MLSRuleModel):
    """
    ML 라이브러리를 사용하지 않는 Rule 기반의 샘플 모델입니다.

    세 개의 feature에 대한 조건을 체크하여 반환 여부를 결정합니다.
    """

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        age = x[0]
        app_use_traffic_youtube = x[1]
        svc_scrb_period = x[2]

        if len(self.features) != len(x):
            raise MLSModelError("The length of input is different from features on model.json")

        if svc_scrb_period < 100 or age < 19 or age > 60 or app_use_traffic_youtube < 10:
            return {"items": []}
        else:
            return {
                "items": [{"id": "NA00006538", "name": "T플랜 스페셜", "props": {"percent_rk": "0.5755"}, "type": "fee"}]
            }
