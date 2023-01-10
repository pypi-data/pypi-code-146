import random
from calendar import monthrange
from datetime import datetime
from functools import reduce
from typing import Any, Dict, List

import numpy as np
from pytz import timezone

from sktmls.models import MLSGenericModel, MLSModelError
from sktmls.utils import LogicProcessor

TZ = timezone("Asia/Seoul")

logic_processor = LogicProcessor()


class GenericContextModel(MLSGenericModel):
    """
    MLS 모델 레지스트리에 등록되는 단일 모델 기반의 클래스입니다.

    y 결과에 따라 적절한 상품 정보와 context_id를 선택하여 제공해야 하는 경우 사용 가능합니다.
    """

    def __init__(
        self,
        model,
        model_name: str,
        model_version: str,
        model_features: List[str],
        default_model_feature_values: List[Any],
        default_context_value: str,
        products: Dict[str, Any],
        product_selection_logic: Dict[str, Any],
        conversion_formulas: Dict[str, Dict[str, Any]] = dict(),
        emb_features: List[str] = [],
        default_emb_feature_values: List[List[Any]] = [],
        emb_feature_indices: List[List[int]] = [],
        context_features: List[str] = [],
        context_values: List[Any] = [],
        realtime_features: List[str] = [],
        include_y: bool = False,
        y_key: str = "score",
    ):
        """
        ## Args

        - model: ML 라이브러리로 학습한 모델 객체
        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - model_features: (list(str)) 피쳐 리스트
        - default_model_feature_values: (list) 피쳐 기본값 리스트
        - default_context_value: (str) 기본 컨텍스트 값
        - products: (dict) 추천 상품 정보. 형식은 아래 Example 참조
        - product_selection_logic: (dict) 계산된 y로 추천 상품을 선택하는 로직. 형식은 아래 Example 참조
        - conversion_formulas: (optional) (dict(dict)) Feature conversion에 사용할 조건 dict. 형식은 아래 Example 참조 (기본값: {})
        - emb_features: (optional) (list(str)) 임베딩 피쳐 이름 리스트 (기본값: [])
        - default_emb_feature_values: (optional) (list(list)) 임베딩 피쳐들의 기본값 리스트 (리스트의 리스트 형식) (기본값: [])
        - emb_feature_indices: (optional) (list(list)) 각 임베딩 피쳐의 세부 사용 피쳐 인덱스 리스트 (기본값: [])
        - context_features: (optional) (list(str)) 컨텍스트 생성을 위한 피쳐 리스트 (기본값: [])
        - context_values: (optional) (list(str)) 컨텍스트 값 리스트 (기본값: [])
        - realtime_features: (optional) (list(str)) 실시간 피쳐 리스트 (포함 가능 값: `weekday`|`day_ratio`) (기본값: [])
        - include_y: (optional) (bool) props에 y값을 포함할 지 여부 (기본값: False)
        - y_key: (optional) (str) `include_y`가 True인 경우 props에서 y값을 쓰기 위해 사용할 키 (기본값: `score`)

        ## Example

        ```python
        model_features = ["feature1", "feature2", "feature3", "feature4", "feature5", "feature6"]
        emb_features = ["embedding_vector1", "embedding_vector2"]
        context_features = ["context_feature1", "context_feature2"]

        default_model_feature_values = ["D", 0.0, "N/A", 0.0, 0.0, "S"]
        default_emb_feature_values = [[1, 2, 3], [4, 5, 6]]
        emb_feature_indices = [[0, 1, 2], [0, 2]]

        # 상품 정보
        # - products: 추천 상품 정보. Key는 상품의 고유 id
        #    - name
        #    - type
        #    - context_features: 컨텍스트로 사용할 feature 리스트. None이거나 비어있으면 default_context_value가 반환됨
        #    - random_context: 유효한 컨텍스트를 랜덤하게 뽑아서 반환할 지 context_features의 순서대로 우선순위를 주어 반환할 지 여부 (기본값: False)
        products = {
            "PRODUCT001": {
                "name": "상품001",
                "type": "상품타입",
                "context_features": ["context_feature1", "context_feature2"],
                "random_context": False,
            },
            "PRODUCT002": {
                "name": "상품002",
                "type": "상품타입",
                "context_features": ["context_feature1"],
                "random_context": False,
            },
            "PRODUCT003": {
                "name": "상품002",
                "type": "상품타입",
                "context_features": ["context_feature1", "context_feature2"],
                "random_context": True,
            },
        }

        # 상품 선택 로직
        # - product_selection_logic: ML라이브러리 predict 함수 계산을 통해 얻어낸 y값을 바탕으로 실제 상품을 선택하는 로직
        # - 자세한 문법은 sktmls/utils/logic.py 참조
        product_selection_logic = {
            "if": [
                # 계산한 y가 0보다 크고
                # 25 <= feature2 < 65 이며
                # feature3 == "N" 인 경우
                # 아래 if_closest_upper 확인
                {
                    "and": [
                        {">": [{"var": "y"}, 0]},
                        {">=": [{"var": "feature2"}, 25]},
                        {"<": [{"var": "feature2"}, 65]},
                        {"==": [{"var": "feature3"}, "N"]},
                    ]
                },
                {
                    "if_closest_upper": [
                        # y * 1000 + feature4 값이 가장 가까운 것을 리턴
                        {"+": [{"*": [{"var": "y"}, 1000]}, {"var": "feature4"}]},
                        # 43000에 가장 가까운 경우
                        # "PRODUCT001"를 리턴
                        43000,
                        "PRODUCT001",
                        # 50000 가장 가까운 경우
                        # "PRODUCT002"를 리턴
                        50000,
                        "PRODUCT002",
                    ]
                },
                # 계산한 y가 0보다 크고
                # 19 <= feature2 < 25 이며
                # feature3 == "N" 인 경우
                # 아래 if_closest_upper 확인
                {
                    "and": [
                        {">": [{"var": "y"}, 0]},
                        {">=": [{"var": "feature2"}, 19]},
                        {"<": [{"var": "feature2"}, 25]},
                        {"==": [{"var": "feature3"}, "N"]},
                    ]
                },
                {
                    "if_closest_upper": [
                        # y * 1000 + feature4 값이 가장 가까운 것을 리턴
                        {"+": [{"*": [{"var": "y"}, 1000]}, {"var": "feature4"}]},
                        # 53000에 가장 가까운 경우
                        # "PRODUCT001"를 리턴
                        53000,
                        "PRODUCT001",
                        # 60000 가장 가까운 경우
                        # "PRODUCT003"를 리턴
                        60000,
                        "PRODUCT003",
                    ]
                },
                # 아무 조건에도 해당되지 않을 때 None
                None
            ]
        }

        conversion_formulas = {
            "feature1": {"map": {"D": 1, "V": 2}, "default": 0},
            "feature5": {"map": {"S": 1, "K": 2}, "default": 0},
        }

        realtime_features = ["weekday", "day_ratio"]

        my_model_v1 = GenericContextModel(
            model=model,
            model_name="my_model",
            model_version="v1",
            model_features=model_features,
            default_model_feature_values=default_model_feature_values,
            default_context_value="default_context_id",
            products=products,
            product_selection_logic=product_selection_logic,
            conversion_formulas=conversion_formulas,
            emb_features=emb_features,
            default_emb_feature_values=default_emb_feature_values,
            emb_feature_indices=emb_feature_indices,
            context_features=context_features,
            context_values=context_features,
            realtime_features=realtime_features
        )
        ```
        """
        assert len(model_features) == len(
            default_model_feature_values
        ), "`model_features`와 `default_model_feature_values`의 길이가 다릅니다."
        assert None not in default_model_feature_values, "`default_model_feature_values`에 None이 포함되어 있습니다."

        assert isinstance(emb_features, list), "`emb_features`는 리스트 형식이어야 합니다."
        assert isinstance(default_emb_feature_values, list), "`default_emb_feature_values`는 리스트 형식이어야 합니다."
        assert None not in default_emb_feature_values, "`default_emb_feature_values`에 None이 포함되어 있습니다."
        assert isinstance(emb_feature_indices, list), "`emb_feature_indices`는 리스트 형식이어야 합니다."
        assert None not in emb_feature_indices, "`emb_feature_indices`에 None이 포함되어 있습니다."
        assert (
            len(emb_features) == len(default_emb_feature_values) == len(emb_feature_indices)
        ), "`emb_features`, `default_emb_feature_values`, `emb_feature_indices`의 길이가 다릅니다."

        for i, indices in enumerate(emb_feature_indices):
            assert isinstance(indices, list), "`emb_feature_indices` 내 모든 element는 리스트 형식이어야 합니다."
            assert len(indices) <= len(
                default_emb_feature_values[i]
            ), "`emb_feature_indices` 내 element 길이가 해당 임베딩 피쳐 길이보다 깁니다."
            assert None not in default_emb_feature_values[i], "`default_emb_feature_values` 내 element에 None이 포함되어 있습니다."
            for idx in indices:
                assert isinstance(idx, int), "`emb_feature_indices` 내 모든 인덱스 값은 int 형식이어야 합니다."
                assert idx < len(default_emb_feature_values[i]), "`emb_feature_indices` 내 인덱스가 임베딩 피쳐 전체 길이보다 깁니다."

        assert isinstance(context_features, list), "`context_features`는 리스트 형식이어야 합니다."
        if context_features:
            assert context_values and isinstance(context_values, list), "`context_values`는 리스트 형식이어야 합니다."
            assert len(context_features) == len(context_values), "`context_features`와 `context_values`의 길이가 다릅니다."
        else:
            assert not context_values, "`context_features`와 `context_values`의 길이가 다릅니다."

        assert isinstance(realtime_features, list), "`realtime_features`는 리스트 형식이어야 합니다."
        assert set(realtime_features).issubset({"weekday", "day_ratio"}), "현재 지원하는 실시간 피쳐는 `weekday`와 `day_ratio` 입니다."

        assert isinstance(conversion_formulas, dict), "`conversion_formulas`는 dict 형식이어야 합니다."
        for k, v in conversion_formulas.items():
            assert isinstance(k, str), "`conversion_formulas`의 키는 문자열이어야 합니다."
            assert isinstance(v, dict), "`conversion_formulas`의 값은 dict 형식이어야 합니다."
            assert "map" in v or "conditions" in v, "`conversion_formulas`의 값에 map 또는 conditions 키가 포함되어야 합니다."
            assert "default" in v, "`conversion_formulas`의 값에 default 키가 포함되어야 합니다."

        assert isinstance(product_selection_logic, dict), "`product_selection_logic`는 dict 형식이어야 합니다."
        for key in product_selection_logic.keys():
            assert key in ["var", "missing", "missing_some", "pf", "with", "for"] or key in logic_processor.operations

        product_context_features = set()
        for p in products.values():
            product_context_features.update(p.get("context_features", []))
        assert product_context_features.issubset(
            context_features
        ), "`products`에 명세된 context_features에 `context_features` 파라미터에 없는 피쳐가 존재합니다."

        super().__init__([model], model_name, model_version, model_features + emb_features + context_features)

        self.default_model_feature_values = default_model_feature_values
        self.default_context_value = default_context_value
        self.products = products
        self.product_selection_logic = product_selection_logic
        self.conversion_formulas = conversion_formulas
        self.default_emb_feature_values = default_emb_feature_values
        self.emb_feature_indices = emb_feature_indices
        self.context_values = context_values
        self.realtime_features = realtime_features
        self.include_y = include_y
        self.y_key = y_key

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        # 1. 피쳐 전처리
        preprocessed_x = self._preprocess(x)

        # 2. Prediction
        y = self._ml_predict(preprocessed_x)

        # 3. 컨텍스트 빌드 (후처리)
        item = self._postprocess(x, y)

        return {"items": item}

    def _preprocess(self, x: List[Any]) -> List[Any]:
        if len(self.features) != len(x):
            raise MLSModelError("GenericContextModel: `x`의 길이가 `features`의 길이와 다릅니다.")

        # - 1.1. 피쳐 나누기
        emb_x = x[
            len(x) - len(self.context_values) - len(self.default_emb_feature_values) : len(x) - len(self.context_values)
        ]

        for i, emb_f in enumerate(emb_x):
            if not emb_f:
                emb_x[i] = self.default_emb_feature_values[i]
                continue
            if len(emb_f) != len(self.default_emb_feature_values[i]):
                raise MLSModelError("GenericContextModel: emb_x와 `default_emb_feature_values`의 임베딩 피쳐 길이가 다릅니다.")
            if len(emb_f) < len(self.emb_feature_indices[i]):
                raise MLSModelError("GenericContextModel: `emb_feature_indices`의 임베딩 피쳐 인덱스 길이가 emb_x 임베딩 피쳐 길이보다 큽니다.")

        # - 1.2. None 피쳐 기본값 할당 및 임베딩 피쳐 펼치기
        non_emb_x = x[: len(x) - len(self.context_values) - len(self.default_emb_feature_values)]
        non_emb_x = [f if f is not None else self.default_model_feature_values[i] for i, f in enumerate(non_emb_x)]
        emb_x = [
            [
                emb_x[i][j] if emb_x[i][j] is not None else self.default_emb_feature_values[i][j]
                for j in self.emb_feature_indices[i]
            ]
            for i in range(len(emb_x))
        ]
        emb_x = reduce(lambda a, b: a + b, emb_x, [])

        # - 1.3. conversion_formulas를 이용한 피쳐 맵핑 작업
        try:
            preprocessed_x = self._convert(non_emb_x) + emb_x
        except Exception as e:
            raise MLSModelError(f"GenericContextModel: Feature conversion에 실패했습니다. {e}")

        # - 1.4. Realtime feature 생성
        now = datetime.now(TZ)
        for realtime_feature in self.realtime_features:
            if realtime_feature == "weekday":
                preprocessed_x.append(now.weekday() + 1)
            else:
                _, ndays = monthrange(now.year, now.month)
                preprocessed_x.append(now.day / ndays)

        return preprocessed_x

    def _ml_predict(self, x: List[Any]) -> float:
        try:
            return self.models[0].predict(np.array([x], dtype=np.float32)).flatten().tolist()[0]
        except Exception as e:
            raise MLSModelError(f"GenericContextModel: Prediction에 실패했습니다. {e}")

    def _postprocess(self, x: List[Any], y: float) -> Dict[str, Any]:
        context_x = x[len(x) - len(self.context_values) :]
        non_emb_x = x[: len(x) - len(self.context_values) - len(self.default_emb_feature_values)]
        non_emb_x = [f if f is not None else self.default_model_feature_values[i] for i, f in enumerate(non_emb_x)]

        # 컨텍스트 빌드
        # - 3.1. 추천 상품 선택
        try:
            non_emb_features = self.features[
                : len(self.features) - len(self.context_values) - len(self.default_emb_feature_values)
            ]
            context_features = self.features[len(self.features) - len(self.context_values) :]

            feature_map = {name: non_emb_x[i] for i, name in enumerate(non_emb_features)}
            feature_map.update({name: context_x[i] for i, name in enumerate(context_features)})
            feature_map["y"] = y

            product_id = logic_processor.apply(self.product_selection_logic, feature_map)
            if not product_id:
                return []

            product = self.products[product_id]
        except Exception as e:
            raise MLSModelError(f"GenericContextModel: 추천 상품 선택 로직 프로세스에 실패했습니다. {e}")

        # - 3.2. context_id 선택
        try:
            product_context_features = [f for f in product.get("context_features", []) if feature_map[f] == "Y"]
            if product_context_features:
                context_map = {name: self.context_values[i] for i, name in enumerate(context_features)}
                context_ids = [context_map[f] for f in product_context_features]
                is_random = product.get("random_context", False)
                context_id = random.choice(context_ids) if is_random else context_ids[0]
            else:
                context_id = self.default_context_value
        except Exception as e:
            raise MLSModelError(f"GenericContextModel: context_id 선택에 실패했습니다. {e}")

        item = {
            "id": product_id,
            "name": product["name"],
            "type": product["type"],
            "props": {"context_id": context_id},
        }
        if self.include_y:
            item["props"][self.y_key] = round(y, 4)

        return [item]

    def _convert(self, features):
        converted_features = []
        for i, f in enumerate(features):
            feature_name = self.features[i]
            formula = self.conversion_formulas.get(feature_name)
            if formula:
                if "map" in formula:
                    converted_features.append(formula["map"].get(f, formula["default"]))
                elif "conditions" in formula:
                    conditions = formula["conditions"]
                    conditions_checked = True
                    for condition in conditions:
                        if (
                            (condition[0] == "==" and f != condition[1])
                            or (condition[0] == "!=" and f == condition[1])
                            or (condition[0] == "<" and f >= condition[1])
                            or (condition[0] == "<=" and f > condition[1])
                            or (condition[0] == ">" and f <= condition[1])
                            or (condition[0] == ">=" and f < condition[1])
                        ):
                            conditions_checked = False
                            break
                    converted_features.append(f if conditions_checked else formula["default"])
            else:
                converted_features.append({"Y": 1, "N": 0}.get(f, f))
        return converted_features
