from typing import Any, Dict, List

import random

from sktmls.models import MLSRuleModel


class TwRandomGreetingRuleModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    TW 그리팅 추천 모델에 특화된 모델이며, 2개의 그리팅 타입(이미지 / 텍스트) 및 1개의 그리팅 랭킹을 사용합니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        image_type_ids: List[str],
        text_type_ids: List[str],
        greeting_ids: List[str],
        greeting_ids_shuffle: bool = False,
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - image_type_ids: (list) 티월드그리팅 이미지 타입
        - text_type_ids: (list) 티월드그리팅 텍스트 타입
        - greeting_ids: (list) 티월드그리팅 랭킹
        - greeting_ids_shuffle: (bool) 티월드그리팅 랭킹 Shuffle 여부

        ## Example

        ```python
        random_greeting_rule_model_v1 = TwRandomGreetingRuleModel(
            model_name="random_greeting_rule_model",
            model_version="v1",
            image_type_ids=["A", "B"],
            text_type_ids=["A", "B", "C"],
            greeting_ids=["C1", "C2", "C3", "C4", "C5"],
            greeting_ids_shuffle=True
        )

        result = random_greeting_rule_model_v1.predict(None)
        ```
        """
        assert isinstance(image_type_ids, list) and image_type_ids, "`image_type_ids`는 list 형식이어야 합니다."
        assert isinstance(text_type_ids, list) and text_type_ids, "`text_type_ids`는 list 형식이어야 합니다."
        assert isinstance(greeting_ids, list) and greeting_ids, "`greeting_ids`는 list 형식이어야 합니다."

        super().__init__(model_name, model_version, ["user_id"])

        self.image_type_ids = image_type_ids
        self.text_type_ids = text_type_ids
        self.greeting_ids = greeting_ids
        self.greeting_ids_shuffle = greeting_ids_shuffle

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if self.greeting_ids_shuffle:
            random.shuffle(self.greeting_ids)

        return {
            "items": [
                {
                    "id": "tw_greeting_image",
                    "name": "티월드그리팅이미지타입",
                    "type": "tw_greeting",
                    "props": {"bucket": random.choice(self.image_type_ids)},
                },
                {
                    "id": "tw_greeting_text",
                    "name": "티월드그리팅텍스트타입",
                    "type": "tw_greeting",
                    "props": {"bucket": random.choice(self.text_type_ids)},
                },
                {
                    "id": "tw_greeting_ranking",
                    "name": "티월드그리팅랭킹",
                    "type": "tw_greeting",
                    "props": {"ranking": self.greeting_ids},
                },
            ]
        }
