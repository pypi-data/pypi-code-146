from typing import Any, Dict, List, Union

import numpy as np
from pandas import DataFrame
from pytz import timezone
import torch

from sktmls import MLSRuntimeENV
from sktmls.apis import MLSProfileAPIClient, MLSGraphAPIClient
from sktmls.dynamodb import DynamoDBClient
from sktmls.models import MLSGenericModel, MLSModelError
from sktmls.utils import LogicProcessor

TZ = timezone("Asia/Seoul")

logic_processor = LogicProcessor()


class ConditionalGenericLogicModel(MLSGenericModel):
    """
    MLS 모델 레지스트리에 등록되는 다수 모델 기반의 클래스입니다.

    모델 선택 로직으로 적용할 모델을 선택한 뒤 전처리 로직과 후처리 로직을 기반으로 프로세스합니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        models: List[Any],
        preprocess_logics: List[Dict[str, List[Any]]],
        postprocess_logics: List[Dict[str, List[Any]]],
        predict_fns: List[str],
        model_selection_logic: Dict[str, List[Any]] = {"abs": 0},
        data: Dict[str, Any] = {},
    ):
        """
        `sktmls.models.contrib.GenericLogicModel`과 동작 원리는 동일하나, `models`에 여러 개의 ML 라이브러리로 학습된 모델을 저장해 두고 `model_selection_logic`을 통해 하나를 선택하여 predict를 수행합니다.

        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - features: (list(str)) 피쳐 이름 리스트
        - models: ML 라이브러리로 학습한 모델 객체 리스트
        - preprocess_logics: (list(dict)) 각 모델에 대해 전달된 피쳐 `x`로부터 ML모델의 predict 함수에 input으로 들어갈 `preprocessed_x`를 만드는 전처리 로직 리스트
        - postprocess_logics: (list(dict)) 각 ML모델의 predict 함수 결과로 얻어진 `y`로부터 리턴 body(items 리스트)를 만드는 후처리 로직 리스트
        - predict_fns: (list(str)) ML모델의 추론 함수 이름 (`predict`|`predict_proba`|`none`)
            - `none` 전달 시 ML모델 추론을 사용하지 않습니다 (룰 모델).
            - `model_lib`이 `pytorch` 인 경우 이 파라미터는 무시됩니다.
        - model_selection_logic: (dict) `models`의 모델 중 하나를 선택하는 로직 (기본값: {"abs": 0} (models[0] 모델 사용))
            - 정수 반환 시 models의 인덱스로 사용합니다.
            - list(dict) 반환 시 즉시 그 값을 리턴합니다. 이 때 유효한 response 형식이어야 합니다.
        - data: (optional) (dict) 각 모델의 `preprocess_logic`과 `postprocess_logic`에서 피쳐와 함께 "var" 참조할 추가 데이터 (기본값: {})
            - 피쳐 이름과 같은 키 존재 시 피쳐 값을 덮어쓰게 됩니다. 주의하세요!

        `models`, `preprocess_logics`, `postprocess_logics`, `predict_fns`는 `sktmls.models.contrib.GenericLogicModel`의 `model`, `preprocess_logic`, `postprocess_logic`, `predict_fn`을 리스트로 여러 개 가지고 있는 형태입니다.

        자세한 형식은 `sktmls.models.contrib.GenericLogicModel` 문서를 참조하세요.

        ## Example

        my_model_v1 = ConditionalGenericLogicModel(
            model_name="my_model",
            model_version="v1",
            features=["feature1", "feature2", "feature3", "embedding_vector", "context_feature1", "context_feature2"],
            models=[model0, model1],
            preprocess_logics=[preprocess_logic0, preprocess_logic1],
            postprocess_logics=[postprocess_logic0, postprocess_logic1],
            predict_fns=["predict", "predict_proba"],
            model_selection_logic={
                "if": [
                    {">": [{"var": "feature1"}, 3.0]},
                    0,
                    1
                ]
            },
            data={}
        )
        """
        assert isinstance(features, list), "`features`은 list 타입이어야 합니다."

        assert isinstance(model_selection_logic, dict), "`model_selection_logic`은 dict 타입이어야 합니다."
        for key in model_selection_logic.keys():
            assert key in ["var", "missing", "missing_some", "pf", "with", "for"] or key in logic_processor.operations

        assert (
            len(models) == len(preprocess_logics) == len(postprocess_logics) == len(predict_fns)
        ), "`preprocess_logics`, `postprocess_logics`, `predict_fns`의 길이는 같아야 합니다."

        assert isinstance(preprocess_logics, list), "`preprocess_logics`는 list 타입이어야 합니다."
        for preprocess_logic in preprocess_logics:
            assert isinstance(preprocess_logic, dict), "`preprocess_logic`은 dict 타입이어야 합니다."
            for key in preprocess_logic.keys():
                assert (
                    key in ["var", "missing", "missing_some", "pf", "with", "for"] or key in logic_processor.operations
                )

        assert isinstance(postprocess_logics, list), "`postprocess_logics`는 list 타입이어야 합니다."
        for postprocess_logic in postprocess_logics:
            assert isinstance(postprocess_logic, dict), "`postprocess_logic`은 dict 타입이어야 합니다."
            for key in postprocess_logic.keys():
                assert (
                    key in ["var", "missing", "missing_some", "pf", "with", "for"] or key in logic_processor.operations
                )

        assert isinstance(predict_fns, list), "`predict_fn`은 list 타입이어야 합니다."
        for predict_fn in predict_fns:
            assert predict_fn in [
                "predict",
                "predict_proba",
                "none",
            ], "`predict_fn`은 predict, predict_proba, none 중 하나의 값이어야 합니다."

        assert isinstance(data, dict), "`data`는 dict 타입이어야 합니다."

        super().__init__(models, model_name, model_version, features)

        self.preprocess_logics = preprocess_logics
        self.postprocess_logics = postprocess_logics
        self.predict_fns = predict_fns
        self.model_selection_logic = model_selection_logic
        self.data = data

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(self.features) != len(x):
            raise MLSModelError("ConditionalGenericLogicModel: `x`의 길이가 `features`의 길이와 다릅니다.")

        pf_client = kwargs.get("pf_client") or MLSProfileAPIClient(runtime_env=MLSRuntimeENV.MMS)
        graph_client = kwargs.get("graph_client") or MLSGraphAPIClient(runtime_env=MLSRuntimeENV.MMS)
        dynamodb_client = kwargs.get("dynamodb_client") or DynamoDBClient(runtime_env=MLSRuntimeENV.MMS)

        result = self._select_model(x, kwargs.get("keys", []), pf_client, graph_client, dynamodb_client)
        if isinstance(result, int):
            if result < 0 or result >= len(self.models):
                raise MLSModelError(f"ConditionalGenericLogicModel: model_index({result})가 유효하지 않습니다.")
            model_index = result
        elif isinstance(result, list):
            return {"items": result}
        else:
            raise MLSModelError("ConditionalGenericLogicModel: `model_selection_logic`이 유효하지 않습니다.")

        preprocessed_x = self._preprocess(
            model_index, x, kwargs.get("keys", []), pf_client, graph_client, dynamodb_client
        )
        y = self._ml_predict(model_index, preprocessed_x)
        items = (
            self._postprocess(model_index, x, kwargs.get("keys", []), y, pf_client, graph_client, dynamodb_client) or []
        )

        return {"items": items}

    def _select_model(
        self,
        x: List[Any],
        additional_keys: List[Any],
        pf_client: MLSProfileAPIClient,
        graph_client: MLSGraphAPIClient,
        dynamodb_client: DynamoDBClient,
    ) -> Union[int, List[Dict[str, Any]]]:
        data = {name: x[i] for i, name in enumerate(self.features) if x[i] not in [None, []]}
        data["additional_keys"] = additional_keys
        data.update(self.data)

        try:
            return logic_processor.apply(
                self.model_selection_logic,
                data=data,
                pf_client=pf_client,
                graph_client=graph_client,
                dynamodb_client=dynamodb_client,
            )
        except Exception as e:
            raise MLSModelError(f"ConditionalGenericLogicModel: 모델 선택에 실패했습니다. {e}")

    def _preprocess(
        self,
        model_index: int,
        x: List[Any],
        additional_keys: List[Any],
        pf_client: MLSProfileAPIClient,
        graph_client: MLSGraphAPIClient,
        dynamodb_client: DynamoDBClient,
    ) -> List[Any]:
        data = {name: x[i] for i, name in enumerate(self.features) if x[i] not in [None, []]}
        data["additional_keys"] = additional_keys
        data["model_index"] = model_index
        data.update(self.data)

        try:
            return logic_processor.apply(
                self.preprocess_logics[model_index],
                data=data,
                pf_client=pf_client,
                graph_client=graph_client,
                dynamodb_client=dynamodb_client,
            )
        except Exception as e:
            raise MLSModelError(f"ConditionalGenericLogicModel: 전처리에 실패했습니다. {e}")

    def _ml_predict(self, model_index: int, preprocessed_x: List[Any]) -> Union[float, List[float], str, None]:
        try:
            if self.predict_fns[model_index] == "none" and self.model_lib != "pytorch":
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
                y = self.models[model_index](input_data).detach().numpy()
            elif self.predict_fns[model_index] == "predict":
                y = self.models[model_index].predict(input_data)
            else:
                y = self.models[model_index].predict_proba(input_data)

            if len(y) == 1:
                y = y[0]

            try:
                return y.tolist()
            except AttributeError:
                return y

        except Exception as e:
            raise MLSModelError(f"ConditionalGenericLogicModel: ML Prediction에 실패했습니다. {e}")

    def _postprocess(
        self,
        model_index: int,
        x: List[Any],
        additional_keys: List[Any],
        y: Union[float, List[float], None],
        pf_client: MLSProfileAPIClient,
        graph_client: MLSGraphAPIClient,
        dynamodb_client: DynamoDBClient,
    ) -> List[Dict[str, Any]]:

        data = {name: x[i] for i, name in enumerate(self.features) if x[i] not in [None, []]}
        data["additional_keys"] = additional_keys
        data["model_index"] = model_index
        data["y"] = y
        data.update(self.data)

        try:
            return logic_processor.apply(
                self.postprocess_logics[model_index],
                data=data,
                pf_client=pf_client,
                graph_client=graph_client,
                dynamodb_client=dynamodb_client,
            )
        except Exception as e:
            raise MLSModelError(f"ConditionalGenericLogicModel: 후처리에 실패했습니다. {e}")
