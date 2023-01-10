from typing import List, Any, Dict, Union

import re
from functools import reduce

import numpy as np
from pandas import DataFrame

from sktmls.models import MLSCatBoostModel, MLSModelError
from sktmls.meta_tables import MetaTable


class CatboostDeviceModel(MLSCatBoostModel):
    """
    MLS 모델 레지스트리에 등록되는 CatBoost 기반 클래스입니다.

    주어진 `features`리스트를 이용해 prediction 후 스코어 상위 3개 단말그룹으로 필터링 합니다.
    이후 `id`, `name`, `score`, `props`, `type`을 반환하는 모델입니다.
    """

    def __init__(
        self,
        model,
        model_name: str,
        model_version: str,
        model_features: List[str],
        default_model_feature_values: List[Any],
        target_prod_id: List[str],
        products_meta: Dict[str, Any],
        products: Dict[str, Any],
        context_meta: DataFrame,
        device_meta: MetaTable,
        conversion_formulas: Dict[str, Dict[str, Any]] = {},
        emb_features: List[str] = [],
        default_emb_feature_values: List[List[Any]] = [],
        emb_feature_indices: List[List] = [],
        default_context_value: str = "context_default",
        num_pick: int = 3,
    ):
        """
        ## Args

        - model: Catboost로 학습한 모델 객체
        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - model_features: (list(str)) non-embedding 피쳐 리스트(필수 피쳐: `eqp_mdl_cd`, `age`)
        - default_model_feature_values: (list) 피쳐 기본값 리스트
        - target_prod_id: (list) 타겟 상품 ID 리스트
        - products: (dict) 상품 컨텍스트 값
        - products_meta: (dict) 상품 메타 정보
        - context_meta: (DataFrame) 컨텍스트 메타 정보
        - device_meta: (`sktmls.meta_tables.MetaTable`) 단말코드그룹 값
        - conversion_formulas: (optional) (dict(dict)) Feature conversion에 사용할 조건 dict. 형식은 아래 Example 참조 (기본값: {})
        - emb_features: (optional) (list(str)) 임베딩 피쳐 이름 리스트 (기본값: [])
        - default_emb_feature_values: (optional) (list(list)) 임베딩 피쳐들의 기본값 리스트 (리스트의 리스트 형식) (기본값: [])
        - emb_feature_indices: (optional) (list(list)) 각 임베딩 피쳐의 세부 사용 피쳐 인덱스 리스트 (기본값: [])
        - default_context_value: (optional) (str) 기본 컨텍스트 값 (기본값: "context_default")

        ## Example

        ```python
        model_features = ["feature1", "feature2", "feature3"]
        default_model_feature_values = [
            dimension_client.get_dimension(dimension_type="user", name=feature).default for feature in model_features
        ]

        device_meta = metatable_client.get_meta_table(name="test_meta_table")
        context_meta = metatable_client.get_meta_table_dataframe(name="test_context_table")

        products_meta={
            "test_prod_id": {"product_grp_nm": "test_product_grp_nm", "mfact_nm": "test_mfact_nm", "eqp_mdl_ntwk": "4G"},
        }

        products = {
            "test_prod_id": {
                "name": "test_prod_name",
                "type": "device",
                "context_features": ["context_default"],
                "random_context": False,
            }
        }

        my_model_v1 = CatboostDeviceModel(
            model=catboost_model,
            model_name="my_model",
            model_version="v1",
            model_features=["eqp_mdl_cd", "age"] + model_features,
            default_model_feature_values=default_model_feature_values,
            products_meta=products_meta,
            products = products,
            target_prod_id = ["prod_1", "prod_2"],
            context_meta=context_meta,
            device_meta=device_meta,
            emb_features=["embedding_vector"],
            default_emb_feature_values=[[0.0] * 64],
            emb_feature_indices=[[0, 1]],
        )

        result = my_model_v1.predict(["eqp_mdl_cd", "value_1", "value_2", "value_3"])
        """

        assert isinstance(model_features, list), "`model_features`는 list타입이어야 합니다."
        assert model_features[0] == "eqp_mdl_cd" and model_features[1] == "age", "`eqp_mdl_cd`, `age`는 필수 피쳐 입니다."
        assert isinstance(default_model_feature_values, list), "`default_model_feature_values`는 list타입이어야 합니다."
        assert len(model_features) - 2 == len(
            default_model_feature_values
        ), "`model_features`(필수 피쳐제외)와 `default_model_feature_values`의 길이가 다릅니다."
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
            assert isinstance(indices, list) and isinstance(
                default_emb_feature_values[i], list
            ), "`emb_feature_indices`와 `default_emb_feature_values` 내 모든 element는 리스트 형식이어야 합니다."
            assert len(indices) <= len(
                default_emb_feature_values[i]
            ), "`emb_feature_indices` 내 element 길이가 해당 임베딩 피쳐 길이보다 깁니다."
            assert None not in default_emb_feature_values[i], "`default_emb_feature_values` 내 element에 None이 포함되어 있습니다."
            for idx in indices:
                assert isinstance(idx, int), "`emb_feature_indices` 내 모든 인덱스 값은 int 형식이어야 합니다."
                assert idx < len(default_emb_feature_values[i]), "`emb_feature_indices` 내 인덱스가 임베딩 피쳐 전체 길이보다 깁니다."

        assert isinstance(target_prod_id, list) and len(target_prod_id) > 0, "`target_prod_id`는 리스트 형식이어야 하며 필수 입력값입니다."
        assert isinstance(products_meta, dict) and len(products_meta) > 0, "`products_meta`는 딕셔너리 형식이어야 하며 필수 입력값입니다."
        assert isinstance(products, dict) and len(products) > 0, "`products`는 딕셔너리 형식이어야 하며 필수 입력값입니다."
        assert isinstance(context_meta, DataFrame) and len(context_meta) > 0, "`context_meta`는 필수 입력 값 입니다."
        for column in ["ContextId", "ItemNm", "Text ID", "T world text"]:
            assert column in context_meta.columns, "`context_meta`의 필수 컬럼이 누락되어 있습니다"
        assert isinstance(device_meta, MetaTable) and len(device_meta.items) > 0, "`device_meta`는 필수 입력 값 입니다."

        assert isinstance(conversion_formulas, dict), "`conversion_formulas`는 dict 형식이어야 합니다."
        for k, v in conversion_formulas.items():
            assert isinstance(k, str), "`conversion_formulas`의 키는 문자열이어야 합니다."
            assert isinstance(v, dict), "`conversion_formulas`의 값은 dict 형식이어야 합니다."
            assert "map" in v or "conditions" in v, "`conversion_formulas`의 값에 map 또는 conditions 키가 포함되어야 합니다."
            assert "default" in v, "`conversion_formulas`의 값에 default 키가 포함되어야 합니다."

        for device_meta_item in device_meta.items:
            device_meta_item_name = device_meta_item.get("name")
            device_meta_item_value = device_meta_item.get("values")

            assert (
                device_meta_item_value and device_meta_item_name
            ), "`device_meta`의 `item` 항목 중 `name`과 `values`는 필수입니다."
            assert isinstance(device_meta_item_name, str), "`device_meta.item`의 `name`은 str 타입이어야 합니다."
            assert isinstance(device_meta_item_value, dict), "`device_meta.item`의 `values`은 dict 타입이어야 합니다."
            assert {
                "product_grp_id",
                "product_grp_nm",
                "mfact_nm",
            } <= device_meta_item_value.keys(), (
                "`device_meta.item`의 `values`는 `product_grp_id`, `product_grp_nm`, `mfact_nm` 키를 포함하여야 합니다."
            )

        super().__init__(model, model_name, model_version, model_features + emb_features)
        self.default_model_feature_values = default_model_feature_values
        self.target_prod_id = target_prod_id
        self.device_meta = {meta["name"]: meta["values"] for meta in device_meta.items}
        self.context_meta = context_meta[context_meta["ItemNm"] == "device nm"]
        self.conversion_formulas = conversion_formulas
        self.products_meta = products_meta
        self.products = products
        self.default_emb_feature_values = default_emb_feature_values
        self.emb_feature_indices = emb_feature_indices
        self.default_context_value = default_context_value
        self.num_pick = num_pick

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        # 1. 전처리
        model_x = self._preprocess(x[2:])

        # 2. ML Prediction
        y = self._ml_predict(model_x)

        # 3. 후처리
        items = self._postprocess(y, x[0], x[1]) or []
        return {"items": items}

    def _preprocess(self, x: List[Any]) -> List[Any]:
        # 1. 전처리
        try:
            if len(self.features) - 2 != len(x):
                raise MLSModelError("CatboostDeviceModel: `x`와 `features`의 길이가 다릅니다.")

            # - 1.1 피쳐 나누기
            emb_x = x[len(x) - len(self.default_emb_feature_values) :]
            for i, emb_f in enumerate(emb_x):
                if not emb_f:
                    emb_x[i] = self.default_emb_feature_values[i]
                    continue
                if not isinstance(emb_f, list):
                    raise MLSModelError("CatboostDeviceModel: emb_x는 list 타입이어야 합니다.")
                if len(emb_f) != len(self.default_emb_feature_values[i]):
                    raise MLSModelError("CatboostDeviceModel: emb_x와 `default_emb_feature_values`의 임베딩 피쳐 길이가 다릅니다.")
                if len(emb_f) < len(self.emb_feature_indices[i]):
                    raise MLSModelError(
                        "CatboostDeviceModel: `emb_feature_indices`의 임베딩 피쳐 인덱스 길이가 emb_x 임베딩 피쳐 길이보다 큽니다."
                    )

            # - 1.2. None 피쳐 기본값 할당 및 임베딩 피쳐 펼치기
            non_emb_x = x[: len(x) - len(self.default_emb_feature_values)]
            non_emb_x = [f if f is not None else self.default_model_feature_values[i] for i, f in enumerate(non_emb_x)]
            emb_x = [
                [
                    emb_x[i][j] if emb_x[i][j] is not None else self.default_emb_feature_values[i][j]
                    for j in self.emb_feature_indices[i]
                ]
                for i in range(len(emb_x))
            ]
            emb_x = reduce(lambda a, b: a + b, emb_x, [])

            return self._convert(non_emb_x) + emb_x
        except Exception as e:
            raise MLSModelError(f"CatboostDeviceModel: 전처리에 실패했습니다. {e}")

    def _ml_predict(self, x: List[Any]) -> List[float]:
        try:
            y = self.models[0].predict_proba(np.array([x]))
            if len(y) == 1:
                y = y[0]
            try:
                return y.tolist()
            except AttributeError:
                return y
        except Exception as e:
            raise MLSModelError(f"CatboostDeviceModel: ML Prediction에 실패했습니다. {e}")

    def _postprocess(self, y: Union[List[float], None], user_eqp_mdl_cd: str, user_age: int) -> List[Dict[str, Any]]:
        try:
            user_meta = self.device_meta.get(user_eqp_mdl_cd, {})
            user_product_grp_id = user_meta.get("product_grp_id", "")
            user_mfact_nm = user_meta.get("mfact_nm", "")

            if user_product_grp_id in self.target_prod_id:
                y[self.target_prod_id.index(user_product_grp_id)] = 0

            sort_labels = np.argsort(y)[::-1].tolist()
            top_prod_ids = [self.target_prod_id[label] for label in sort_labels[: min(self.num_pick, len(y))]]

            top_mfacts = [self.products_meta[prod_id]["mfact_nm"] for prod_id in top_prod_ids]

            if user_mfact_nm == "Apple" and "Apple" in top_mfacts:
                apple_idx = [i for i, mfact in enumerate(top_mfacts) if mfact == "Apple"]
                none_apple_idx = [i for i, mfact in enumerate(top_mfacts) if mfact != "Apple"]

                top_prod_ids = [top_prod_ids[i] for i in apple_idx + none_apple_idx]

            items = []
            for prod_id in top_prod_ids:
                context_features = self.products.get(prod_id, {}).get("context_features", [])
                context_id = self.default_context_value
                if context_features:
                    for context_feature in context_features:
                        if re.match("^context_age[0-9]{2}", context_feature):
                            try:
                                age_bin = int(context_feature.split("_")[1][3:5])
                                if int(user_age) // 10 * 10 == age_bin:
                                    context_id = context_feature
                                    break
                            except Exception:
                                break
                        else:
                            context_id = context_feature
                            break

                context_meta = self.context_meta[self.context_meta["ContextId"] == context_id]
                text_id = context_meta["Text ID"].values[0] if len(context_meta) > 0 else ""
                text_value = context_meta["T world text"].values[0] if len(context_meta) > 0 else ""

                items.append(
                    {
                        "id": prod_id,
                        "name": self.products_meta[prod_id]["product_grp_nm"],
                        "props": {
                            "text_id": text_id,
                            "text_value": text_value,
                            "network_type": self.products_meta[prod_id]["eqp_mdl_ntwk"],
                        },
                        "type": "tds_device",
                    }
                )

            return items
        except Exception as e:
            raise MLSModelError(f"CatboostDeviceModel: 후처리에 실패했습니다. {e}")

    def _convert(self, features):
        feature_names = self.features[2 : len(self.features) - len(self.default_emb_feature_values)]
        converted_features = []
        for i, f in enumerate(features):
            feature_name = feature_names[i]
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
                try:
                    converted_feature = float({"Y": 1, "N": 0}.get(f, f))
                except Exception:
                    converted_feature = {"Y": 1, "N": 0}.get(f, f)

                converted_features.append(converted_feature)
        return converted_features
