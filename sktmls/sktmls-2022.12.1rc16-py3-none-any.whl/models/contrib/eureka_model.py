from typing import Any, Dict, List, Union

import numpy as np
from pandas import DataFrame
from pytz import timezone
import torch

from sktmls import MLSRuntimeENV
from sktmls.apis import MLSProfileAPIClient, MLSGraphAPIClient
from sktmls.dynamodb import DynamoDBClient
from sktmls.models import MLSGenericModel, MLSModelError, MLSTrainableCustom
from sktmls.utils import LogicProcessor, LogicConverter

TZ = timezone("Asia/Seoul")

logic_processor = LogicProcessor()


class EurekaModel(MLSGenericModel, MLSTrainableCustom):
    """
    MLS 모델 레지스트리에 등록되는 단일 모델 기반의 클래스입니다.
    전처리 로직은 json 형태로 후처리 로직은 별도로 정의한 함수를 전달하여 프로세스합니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: List[str],
        model=None,
        preprocess_logic: Dict[str, List[Any]] = None,
        postprocess_logic=None,
        predict_fn: str = "predict",
        data: Dict[str, Any] = {},
        postprocessing_user_profile: Dict[str, Any] = {},
        postprocessing_item_profile: Dict[str, Any] = {},
        use_logic_processer: str = "Y",
    ):
        assert isinstance(features, list), "`features`은 list 타입이어야 합니다."

        if preprocess_logic is not None:
            assert isinstance(preprocess_logic, dict), "`preprocess_logic`은 dict 타입이어야 합니다."
            for key in preprocess_logic.keys():
                assert (
                    key in ["var", "missing", "missing_some", "pf", "with", "for"] or key in logic_processor.operations
                )
        else:
            preprocess_logic = {"merge": [{"var": f} for f in features]}

        assert isinstance(use_logic_processer, str), "`use_logic_processer`은 str 타입이어야 합니다."

        if use_logic_processer == "N":
            # logic processer 를 사용하지 않을 경우 후처리 로직
            if postprocess_logic is not None:
                assert isinstance(postprocess_logic, bytes), "`postprocess_logic`은 bytes 타입이어야 합니다."
            self.postprocess_logic = postprocess_logic
        else:
            # logic processer 를 사용할 경우 후처리 로직
            if postprocess_logic is not None:
                assert isinstance(postprocess_logic, dict), "`postprocess_logic`은 dict 타입이어야 합니다."
                for key in postprocess_logic.keys():
                    assert (
                        key in ["var", "missing", "missing_some", "pf", "with", "for"]
                        or key in logic_processor.operations
                    )
            else:
                postprocess_logic = {
                    "list": [
                        {
                            "dict": [
                                "id",
                                "id",
                                "name",
                                "name",
                                "type",
                                "type",
                                "props",
                                {"dict": ["score", {"var": "y"}]},
                            ]
                        }
                    ]
                }
            self.postprocess_logic = postprocess_logic

        assert isinstance(predict_fn, str), "`predict_fn`은 str 타입이어야 합니다."
        assert predict_fn in [
            "predict",
            "predict_proba",
            "none",
        ], "`predict_fn`은 predict, predict_proba, none 중 하나의 값이어야 합니다."

        assert isinstance(data, dict), "`data`는 dict 타입이어야 합니다."
        assert isinstance(postprocessing_user_profile, dict), "`postprocessing_user_profile`는 dict 타입이어야 합니다."
        for i in postprocessing_user_profile:
            assert isinstance(i, str), f"호출 하고자 하는 유저 프로파일명 `{i}`은(는) str 타입이어야 합니다."
            assert isinstance(postprocessing_user_profile[i], list), f"유저 프로파일 `{i}`에서 호출하려는 값들은 list 타입이어야 합니다."
            for j in postprocessing_user_profile[i]:
                assert isinstance(j, str), f"유저 프로파일 {i} 에서 호출하려고 하는 변수명 `{j}`은(는) str 타입이어야 합니다."

        assert isinstance(postprocessing_item_profile, dict), "`postprocessing_item_profile`는 dict 타입이어야 합니다."
        for item_profile in postprocessing_item_profile:
            assert isinstance(item_profile, str), f"호출 하고자 하는 아이템 프로파일명`{item_profile}`은(는) str 타입이어야 합니다."
            for item_id, key in postprocessing_item_profile.get(item_profile).items():
                assert isinstance(item_id, str), f"호출 하고자 하는 아이템 프로파일의 ID `{item_id}`은(는) str 타입이어야 합니다."
                assert isinstance(key, list), f"아이템 프로파일 `{key}`에서 호출하려는 값들은 list 타입이어야 합니다."

        super().__init__([model], model_name, model_version, features)

        self.preprocess_logic = preprocess_logic
        self.predict_fn = predict_fn
        self.data = data
        self.postprocessing_user_profile = postprocessing_user_profile
        self.postprocessing_item_profile = postprocessing_item_profile
        self.use_logic_processer = use_logic_processer

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
            raise MLSModelError("EurekaModel: `x`의 길이가 `features`의 길이와 다릅니다.")

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
            raise MLSModelError(f"EurekaModel: 전처리에 실패했습니다. {e}")

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
            raise MLSModelError(f"EurekaModel: ML Prediction에 실패했습니다. {e}")

    def _get_var(self, data, postprocessing_item_profile):
        for item_profile, key in postprocessing_item_profile.items():
            for key in list(postprocessing_item_profile.get(item_profile)):
                if "." in key:
                    assert (
                        key.split(".")[1] in data.keys()
                    ), f"후처리 시 item profile에서 참조하려고 하는 유저의 변수 {key.split('.')[1]}의 값은 사용되는 유저 프로파일에 있어야 합니다."
                    get_user_item = data[key.split(".")[1]]
                    postprocessing_item_profile[item_profile][get_user_item] = postprocessing_item_profile[
                        item_profile
                    ].pop(key)
        return postprocessing_item_profile

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
            if self.postprocessing_user_profile:
                for user_profile in self.postprocessing_user_profile:
                    user_values = pf_client.get_user_profile(
                        profile_id=user_profile,
                        user_id=data["user_id"],
                        keys=self.postprocessing_user_profile[user_profile],
                    )
                    assert (
                        None not in user_values.values()
                    ), f"후처리 시 사용되는 `user profile` 변수의 값은 사용되는 `{user_profile}`에 있어야 합니다."
                    data.update(user_values)

            postprocessing_item_profile_preprocessed = self._get_var(
                data=data, postprocessing_item_profile=self.postprocessing_item_profile
            )

            if postprocessing_item_profile_preprocessed:
                for item_profile in postprocessing_item_profile_preprocessed:
                    for item_id, keys in postprocessing_item_profile_preprocessed[item_profile].items():
                        item_values = pf_client.get_item_profile(profile_id=item_profile, item_id=item_id, keys=keys)
                        data.update(item_values)
                        assert (
                            None not in user_values.values()
                        ), f"후처리 시 사용되는 `item profile` 변수의 값은 사용되는 `{item_profile}`에 있어야 합니다."
        except Exception as e:
            raise MLSModelError(f"EurekaModel: profile 후처리에 실패했습니다. {e}")
        if self.use_logic_processer == "N":
            try:
                handler = LogicConverter(user_converted_logic=self.postprocess_logic).ConvertToFunction(
                    name=f"{self.model_name}_{self.model_version}_Handler"
                )
                assert hasattr(handler, "__call__") is True, "후처리 로직은 함수이어야 합니다."
                result = handler(data)
                for i in ["id", "name", "type", "props"]:
                    assert i in result.keys(), f"후처리 로직 결과에 {i}가 포함되어 있지 않습니다."
                for j in result.keys():
                    assert j in ["id", "name", "type", "props"], f"후처리 로직 결과에 반환되어서는 안되는 {j}가 포함되어 있습니다."
                return [result]
            except Exception as e:
                raise MLSModelError(f"EurekaModel: Logic Converter 후처리에 실패했습니다. {e}")
        else:
            try:
                return logic_processor.apply(
                    self.postprocess_logic,
                    data=data,
                    pf_client=pf_client,
                    graph_client=graph_client,
                    dynamodb_client=dynamodb_client,
                )
            except Exception as e:
                raise MLSModelError(f"EurekaModel: Logic Processor 후처리에 실패했습니다. {e}")
