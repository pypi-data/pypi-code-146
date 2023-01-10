from typing import Any, Dict, List, Union

import numpy as np
from pandas import DataFrame
from pytz import timezone
import torch

from sktmls import MLSRuntimeENV
from sktmls.apis import MLSProfileAPIClient, MLSGraphAPIClient
from sktmls.dynamodb import DynamoDBClient
from sktmls.models import MLSGenericModel, MLSModelError, MLSTrainable
from sktmls.utils import LogicProcessor

TZ = timezone("Asia/Seoul")

logic_processor = LogicProcessor()


class GenericLogicModel(MLSGenericModel, MLSTrainable):
    """
    MLS 모델 레지스트리에 등록되는 단일 모델 기반의 클래스입니다.

    전처리 로직과 후처리 로직을 json 형태로 전달하여 프로세스합니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        model=None,
        preprocess_logic: Dict[str, List[Any]] = None,
        postprocess_logic: Dict[str, List[Any]] = None,
        predict_fn: str = "predict",
        data: Dict[str, Any] = {},
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - features: (list(str)) 피쳐 이름 리스트
        - model: (optional) ML 라이브러리로 학습한 모델 객체 (기본값: None)
        - preprocess_logic: (optional) (dict) 전달된 피쳐 `x`로부터 ML모델의 predict 함수에 input으로 들어갈 `preprocessed_x`를 만드는 전처리 로직 (기본값: 아래 참조)
        - postprocess_logic: (optional) (dict) ML모델의 predict 함수 결과로 얻어진 `y`로부터 리턴 body(items 리스트)를 만드는 후처리 로직 (기본값: 아래 참조)
        - predict_fn: (optional) (str) ML모델의 추론 함수 이름 (`predict`|`predict_proba`|`none`) (기본값: `predict`)
            - `none` 전달 시 ML모델 추론을 사용하지 않습니다 (룰 모델).
            - `model_lib`이 `pytorch` 인 경우 이 파라미터는 무시됩니다.
        - data: (optional) (dict) `preprocess_logic`과 `postprocess_logic`에서 피쳐와 함께 "var" 참조할 추가 데이터 (기본값: {})
            - 피쳐 이름과 같은 키 존재 시 피쳐 값을 덮어쓰게 됩니다. 주의하세요!

        ## Example

        자세한 예제는 아래를 참조하세요.

        - https://github.com/sktaiflow/mls-samples/tree/main/GenericLogicModel


        ```python

        # 피쳐 이름
        # 유저 프로파일에 존재하는 디멘전의 이름 리스트
        features = ["feature1", "feature2", "feature3", "embedding_vector", "context_feature1", "context_feature2"]

        # 전처리 로직
        # 전달된 피쳐로부터 preprocessed_x를 만드는 로직을 정의합니다.
        # 피쳐 값은 {"var": ["피쳐이름", 기본값]} 으로 참조합니다.
        # 이해를 돕기 위한 예시이며 실제 문제와는 다를 수 있습니다. 그대로 사용하지 마시고 참고만 해 주세요.
        # 전달하지 않은 경우 x 리스트를 전처리 없이 그대로 사용합니다.
        preprocess_logic = {
            # float: 리스트의 모든 element를 float으로 캐스팅합니다.
            "float": [
                # merge: element들을 하나의 리스트에 합쳐 반환합니다.
                {"merge": [
                    {"var": ["feature1", 0]},
                    {"if": [
                        {"==": [{"var": ["feature2", "N/A"]}, "S"]},
                        1,
                        {"==": [{"var": ["feature2", "N/A"]}, "V"]},
                        2,
                        0
                    ]},
                    {"var": ["feature3", 0]},
                    # replace: 리스트 내 None을 0.0으로 교체
                    {"replace": [
                        None,
                        0.0,
                        # pick: 리스트의 특정 인덱스만 뽑아서 리턴
                        {"pick": [
                            {"var": ["embedding_vector", [0.0] * 64]},
                            [1, 2]
                        ]}
                    ]},
                    # weekday: 요일 리턴 (월요일: 1 ~ 일요일: 7)
                    {"weekday": []},
                    # day: 오늘 날짜
                    # ndays: 이번 달 마지막 날짜
                    # /: 나누기
                    {"/": [{"day": []}, {"ndays": []}]},
                    # get: 리스트 또는 딕셔너리에서 해당 인덱스 꺼내기
                    {"get": [
                        {"replace": [
                            "#",
                            "0.0",
                            {
                                # pf: 프로파일 조회
                                # - 타입: (`user`|`item`)
                                # - 프로파일ID
                                # - 조회할 user_id 또는 item_id
                                # - 조회할 키 디멘전
                                "pf": [
                                    "item",
                                    "device",
                                    # additional_keys: Recommendation API(v3 이상)으로부터 전달된 추가 키 리스트
                                    # additional_keys.0: 0번째 element
                                    {"var": ["additional_keys.0", "ABCD"]},
                                    ["sale_cnt"]
                                ]
                            }
                        ]},
                        0
                    ]}
                ]
            }]
        }

        # 후처리 로직
        # 계산된 y로부터 최종 리턴 body(items 리스트)를 만드는 로직을 정의합니다.
        # 피쳐 값은 {"var": "피쳐이름"} 으로 참조합니다.
        # y 값은 {"var": "y"} 으로 참조합니다.
        # y가 리스트인 경우 {"var": "y.0"}, {"var": "y.1"} 등으로 참조합니다.
        # 이해를 돕기 위한 예시이며 실제 문제와는 다를 수 있습니다. 그대로 사용하지 마시고 참고만 해 주세요.
        # 전달하지 않은 경우 아래 기본값이 사용됩니다.
        # [{"id": "ID", "name": "NAME", "type": "TYPE", "props": {"score": {"var": "y"}}}]
        postprocess_logic = {
            "if": [
                # if
                # 25 <= age < 65 이며
                # five_g_yn == "N" 인 경우
                {
                    "and": [
                        {">=": [{"var": ["age", 0]}, 25]},
                        {"<": [{"var": ["age", 0]}, 65]},
                        {"==": [{"var": ["five_g_yn", "N"]}, "N"]},
                    ]
                },
                # then
                {
                    "list": [
                        {
                            "dict": [
                                "id", "PRODUCT001",
                                "name", "상품001",
                                "type", "타입",
                                "props", {
                                    "dict": [
                                        "context_id", {
                                            "if": [
                                                # if context_feature1의 값이 Y이면
                                                {"==": [{"var": ["context_feature1", "N"]}, "Y"]},
                                                # "context_feature1"을 context_id로 사용
                                                "context_feature1",
                                                # else if context_feature2의 값이 Y이면
                                                {"==": [{"var": ["context_feature2", "N"]}, "Y"]},
                                                # "context_feature2"을 context_id로 사용
                                                "context_feature2",
                                                # else "default_context"를 context_id로 사용
                                                "default_context"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                # else if
                # 19 <= age < 25 이며
                # five_g_yn == "N" 인 경우
                {
                    "and": [
                        {">=": [{"var": ["age", 0]}, 19]},
                        {"<": [{"var": ["age", 0]}, 25]},
                        {"==": [{"var": ["five_g_yn", "N"]}, "N"]},
                    ]
                },
                # then
                {
                    "list": [
                        {
                            "dict": [
                                "id", "PRODUCT002",
                                "name", "상품002",
                                "type", "타입",
                                "props", {
                                    "dict": [
                                        "context_id", {
                                            "if": [
                                                # if context_feature1의 값이 Y이면
                                                {"==": [{"var": ["context_feature1", "N"]}, "Y"]},
                                                # "context_feature1"을 context_id로 사용
                                                "context_feature1",
                                                # else if context_feature2의 값이 Y이면
                                                {"==": [{"var": ["context_feature2", "N"]}, "Y"]},
                                                # "context_feature2"을 context_id로 사용
                                                "context_feature2",
                                                # else "default_context"를 context_id로 사용
                                                "default_context"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                # else
                # None을 리턴
                None
            ]
        }

        my_model_v1 = GenericLogicModel(
            model=model,
            model_name="my_model",
            model_version="v1",
            features=features,
            preprocess_logic=preprocess_logic,
            postprocess_logic=postprocess_logic,
            predict_fn="predict"
        )

        # 정확한 로깅을 위한 사용 라이브러리 명시 (권장) (`sklearn`|`lightgbm`|`xgboost`|`catboost`|`pytorch`|`rule`|`etc`)
        my_model_v1.model_lib = "lightgbm"
        my_model_v1.model_lib_version = "2.3.1"
        ```
        """
        assert isinstance(features, list), "`features`은 list 타입이어야 합니다."

        if preprocess_logic is not None:
            assert isinstance(preprocess_logic, dict), "`preprocess_logic`은 dict 타입이어야 합니다."
            for key in preprocess_logic.keys():
                assert (
                    key in ["var", "missing", "missing_some", "pf", "with", "for"] or key in logic_processor.operations
                )
        else:
            preprocess_logic = {"merge": [{"var": f} for f in features]}

        if postprocess_logic is not None:
            assert isinstance(postprocess_logic, dict), "`postprocess_logic`은 dict 타입이어야 합니다."
            for key in postprocess_logic.keys():
                assert (
                    key in ["var", "missing", "missing_some", "pf", "with", "for"] or key in logic_processor.operations
                )
        else:
            postprocess_logic = {
                "list": [
                    {"dict": ["id", "id", "name", "name", "type", "type", "props", {"dict": ["score", {"var": "y"}]}]}
                ]
            }

        assert isinstance(predict_fn, str), "`predict_fn`은 str 타입이어야 합니다."
        assert predict_fn in [
            "predict",
            "predict_proba",
            "none",
        ], "`predict_fn`은 predict, predict_proba, none 중 하나의 값이어야 합니다."

        assert isinstance(data, dict), "`data`는 dict 타입이어야 합니다."

        super().__init__([model], model_name, model_version, features)

        self.preprocess_logic = preprocess_logic
        self.postprocess_logic = postprocess_logic
        self.predict_fn = predict_fn
        self.data = data

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        pf_client = kwargs.get("pf_client") or MLSProfileAPIClient(runtime_env=MLSRuntimeENV.MMS)
        graph_client = kwargs.get("graph_client") or MLSGraphAPIClient(runtime_env=MLSRuntimeENV.MMS)
        dynamodb_client = kwargs.get("dynamodb_client") or DynamoDBClient(runtime_env=MLSRuntimeENV.MMS)

        preprocessed_x = self._preprocess(x, kwargs.get("keys", []), pf_client, graph_client, dynamodb_client)
        y = self._ml_predict(preprocessed_x)
        items = self._postprocess(x, kwargs.get("keys", []), y, pf_client, graph_client, dynamodb_client) or []

        return {"items": items}

    def _preprocess(
        self,
        x: List[Any],
        additional_keys: List[Any],
        pf_client: MLSProfileAPIClient,
        graph_client: MLSGraphAPIClient,
        dynamodb_client: DynamoDBClient,
    ) -> List[Any]:
        if len(self.features) != len(x):
            raise MLSModelError("GenericLogicModel: `x`의 길이가 `features`의 길이와 다릅니다.")

        data = {name: x[i] for i, name in enumerate(self.features) if x[i] not in [None, []]}
        data["additional_keys"] = additional_keys
        data.update(self.data)

        try:
            return logic_processor.apply(
                self.preprocess_logic,
                data=data,
                pf_client=pf_client,
                graph_client=graph_client,
                dynamodb_client=dynamodb_client,
            )
        except Exception as e:
            raise MLSModelError(f"GenericLogicModel: 전처리에 실패했습니다. {e}")

    def _ml_predict(self, preprocessed_x: List[Any]) -> Union[float, List[float], str, None]:
        try:
            if self.predict_fn == "none" and self.model_lib != "pytorch":
                return None

            if not isinstance(preprocessed_x[0], list):
                preprocessed_x = [preprocessed_x]

            if self.model_lib == "autogluon":
                input_data = DataFrame(
                    preprocessed_x, columns=[f for f in self.features if f not in self.non_training_features]
                )
            elif self.model_lib == "pytorch":
                input_data = torch.tensor(preprocessed_x, dtype=torch.float)
            else:
                input_data = np.array(preprocessed_x)

            if self.model_lib == "pytorch":
                y = self.models[0](input_data).detach().numpy()
            elif self.predict_fn == "predict":
                y = self.models[0].predict(input_data)
            else:
                y = self.models[0].predict_proba(input_data)
                if self.model_lib == "autogluon" and isinstance(y, DataFrame):
                    y = y.to_numpy()

            if len(y) == 1:
                y = y[0]

            try:
                return y.tolist()
            except AttributeError:
                return y

        except Exception as e:
            raise MLSModelError(f"GenericLogicModel: ML Prediction에 실패했습니다. {e}")

    def _postprocess(
        self,
        x: List[Any],
        additional_keys: List[Any],
        y: Union[float, List[float], None],
        pf_client: MLSProfileAPIClient,
        graph_client: MLSGraphAPIClient,
        dynamodb_client: DynamoDBClient,
    ) -> List[Dict[str, Any]]:

        data = {name: x[i] for i, name in enumerate(self.features) if x[i] not in [None, []]}
        data["additional_keys"] = additional_keys
        data["y"] = y
        data.update(self.data)

        try:
            return logic_processor.apply(
                self.postprocess_logic,
                data=data,
                pf_client=pf_client,
                graph_client=graph_client,
                dynamodb_client=dynamodb_client,
            )
        except Exception as e:
            raise MLSModelError(f"GenericLogicModel: 후처리에 실패했습니다. {e}")
