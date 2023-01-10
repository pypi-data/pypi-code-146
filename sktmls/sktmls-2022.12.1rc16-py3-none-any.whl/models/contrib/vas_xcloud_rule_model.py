from typing import Any, Dict, List

from sktmls.models import MLSModelError, MLSRuleModel


class VasXcloudRuleModel(MLSRuleModel):
    """
    ## Args

    - model_name: (str) 모델 이름
    - model_version: (str) 모델 버전
    - features: (list(str)) 피쳐 리스트

    ## Example

    ```python
    my_model = VasXcloudRuleModel(
        model_name="vas_xloud_rule_model",
        model_version="v1",
        features=[
            "age",
            "real_arpu_bf_m1",
            "app_use_traffic_game",
            "app_use_days_video_median_yn",
            "data_use_night_ratio_median_yn",
        ],
    )

    result = my_model.predict([20, 55000, 10000, "Y", "Y"])

    ```
    """

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(self.features) != len(x):
            raise MLSModelError("The length of input is different from that of features in model.json")

        age = x[0] if x[0] is not None else 0
        real_arpu_bf_m1 = x[1] if x[1] is not None else 0
        app_use_traffic_game = x[2] if x[2] is not None else 0
        app_use_days_video_median_yn = x[3] or "N"
        data_use_night_ratio_median_yn = x[4] or "N"

        if (
            (age >= 19 and age <= 55)
            and real_arpu_bf_m1 >= 30000
            and (
                app_use_traffic_game > 0 or app_use_days_video_median_yn == "Y" or data_use_night_ratio_median_yn == "Y"
            )
        ):
            return {
                "items": [
                    {
                        "id": "NA00007114",
                        "name": "게임패스 얼티밋",
                        "type": "vas_xcloud",
                        "props": {"context_id": "context_default"},
                    }
                ]
            }
        else:
            return {"items": []}
