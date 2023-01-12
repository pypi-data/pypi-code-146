from typing import Any, Dict, List

from sktmls.models import MLSModelError, MLSRuleModel


class InfoDefectRuleModel(MLSRuleModel):
    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(self.features) != len(x):
            raise MLSModelError("The length of input is different from that of features in model.json")

        svc_scrb_period = x[0] if x[0] is not None else -1
        eqp_chg_period = x[1] if x[1] is not None else 99999

        if (svc_scrb_period <= 30) or (eqp_chg_period >= 1 and eqp_chg_period <= 30):
            return {"items": [{"id": "INF0000004", "name": "초기 불량 대처 방법 안내", "props": {}, "type": "info_defect"}]}
        else:
            return {"items": []}
