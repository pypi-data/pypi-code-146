from typing import Any, Dict, List

import re
from functools import reduce

import numpy as np

from sktmls.models import MLSLightGBMModel, MLSModelError
from sktmls.meta_tables import MetaTable


class LightGBMDeviceModel(MLSLightGBMModel):
    """
    MLS 모델 레지스트리에 등록되는 LightGBM 기반 클래스입니다.

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
        label_indices: Dict[str, int],
        product_classes: Dict[str, Any],
        products: Dict[str, Any],
        device_meta: MetaTable,
        conversion_formulas: Dict[str, Dict[str, Any]] = dict(),
        emb_features: List[str] = [],
        default_emb_feature_values: List[List[Any]] = [],
        emb_feature_indices: Dict[str, List[int]] = [],
        default_context_value: str = "context_default",
        num_pick: int = 3,
        high_rank_word: List[str] = ["Plus", "플러스", "울트라", "Ultra", "Max", "맥스", "Pro", "프로"],
    ):
        """
        ## Args

        - model: LightGBM으로 학습한 모델 객체
        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - model_features: (list(str)) non-embedding 피쳐 리스트(필수피쳐: "eqp_mdl_cd", "age")
        - default_model_feature_values: (list) 피쳐 기본값 리스트
        - label_indices: (dict) 라벨 인덱스 값
        - product_classes: (dict) 상품 클래스 값
        - products: (dict) 컨텍스트 값
        - device_meta: (`sktmls.meta_tables.MetaTable`) 단말코드그룹 값
        - conversion_formulas: (optional) (dict(dict)) Feature conversion에 사용할 조건 dict. 형식은 아래 Example 참조 (기본값: {})
        - emb_features: (optional) (list(str)) 임베딩 피쳐 이름 리스트 (기본값: [])
        - default_emb_feature_values: (optional) (list(list)) 임베딩 피쳐들의 기본값 리스트 (리스트의 리스트 형식) (기본값: [])
        - emb_feature_indices: (optional) (list(list)) 각 임베딩 피쳐의 세부 사용 피쳐 인덱스 리스트 (기본값: [])
        - default_context_value: (optional) (str) 기본 컨텍스트 값 (기본값: "context_default")
        - num_pick: (optional) (int) 스코어 상위 N개 추출
        - high_rank_word: (optional) (list(str)) 플래그쉽 모델 명칭 (기본값 : ["Plus", "플러스", "울트라", "Ultra", "Max", "맥스", "Pro", "프로"])

        ## Example

        ```python
        model_features = ["feature1", "feature2", "feature3"]
        default_model_feature_values = [
            dimension_client.get_dimension(dimension_type="user", name=feature).default for feature in model_features
        ]

        label_indices = {
            "삼성전자_120만원": 0,
            "삼성전자_160만원": 1,
            "삼성전자_60만원": 2,
            "Apple_120만원": 3,
            "Apple_160만원": 4,
            "Apple_60만원": 5,
            "LG전자_120만원": 6,
            "LG전자_160만원": 7,
            "LG전자_60만원": 8,
            "기타_120만원": 9,
            "기타_160만원": 10,
            "기타_60만원": 11,
        }

        product_classes = {
            "Apple_120만원": [
                {
                    "product_grp_id": "000004352",
                    "product_grp_nm": "iPhone SE (2020)",
                    "mfact_nm": "Apple",
                    "eqp_mdl_cd": "A23F",
                    "rep_eqp_mdl_cd": "A23F",
                    "rep_eqp_yn": "Y",
                    "color_hex": "1F2120",
                    "color_nm": "블랙",
                    "network_type": "4G",
                    "device_weight": 0.02356698,
                },
                {
                    "product_grp_id": "000003972",
                    "product_grp_nm": "iPhone 11",
                    "mfact_nm": "Apple",
                    "eqp_mdl_cd": "A1G6",
                    "rep_eqp_mdl_cd": "A1G6",
                    "rep_eqp_yn": "Y",
                    "color_hex": "1F2120",
                    "color_nm": "블랙",
                    "network_type": "4G",
                    "device_weight": 0.01638297,
                },
            ],
            "Apple_160만원": [
                {
                    "product_grp_id": "000003973",
                    "product_grp_nm": "iPhone 11 Pro",
                    "mfact_nm": "Apple",
                    "eqp_mdl_cd": "A1GR",
                    "rep_eqp_mdl_cd": "A1GR",
                    "rep_eqp_yn": "Y",
                    "color_hex": "52514F",
                    "color_nm": "스페이스 그레이",
                    "network_type": "4G",
                    "device_weight": 0.00767129,
                }
            ],
        }

        products = {
            "000000332": {
                "name": "iPhone 6",
                "type": "device",
                "context_features": ["context_default"],
                "random_context": False,
            },
            "000000952": {
                "name": "iPhone 6s",
                "type": "device",
                "context_features": ["context_default"],
                "random_context": False,
            },
            "000001153": {
                "name": "갤럭시 S7 엣지",
                "type": "device",
                "context_features": ["context_popular_apple_device"],
                "random_context": False,
            },
            "000001572": {
                "name": "BlackBerry PRIV",
                "type": "device",
                "context_features": ["context_default"],
                "random_context": False,
            },
            "000001613": {"name": "준3", "type": "device", "context_features": ["context_default"], "random_context": False},
            "000001672": {
                "name": "iPhone 7",
                "type": "device",
                "context_features": ["context_popular_apple_device"],
                "random_context": False,
            },
        }

        device_meta = metatable_client.get_meta_table(name="eqp_mdl_cd_meta")

        conversion_formulas = {
            "additional_svc_allcare_scrb_type": {"map": {"free": 1, "paid": 2, "N/A": 0}, "default": 0},
            "additional_svc_ansim_option_scrb_type": {"map": {"free": 1, "paid": 2, "N/A": 0}, "default": 0},
            "additional_svc_flo_scrb_type": {"map": {"free": 1, "paid": 2, "N/A": 0}, "default": 0},
            "additional_svc_melon_scrb_type": {"map": {"free": 1, "paid": 2, "N/A": 0}, "default": 0},
            "additional_svc_oksusu_scrb_type": {"map": {"free": 1, "paid": 2, "N/A": 0}, "default": 0},
            "additional_svc_pooq_scrb_type": {"map": {"free": 1, "paid": 2, "N/A": 0}, "default": 0},
            "age_band": {"map": {"kids": 1, "ting": 2, "young": 3, "tplan": 4, "senior": 5}, "default": 4},
            "channel": {"map": {"T월드": 1, "고객센터": 2, "오프라인": 3}, "default": 0},
            "family_comb_type": {"map": {"wire": 1, "wless": 2}, "default": 0},
            "main_channel_eqp_buy": {"map": {"D": 1, "S": 2}, "default": 0},
            "mbr_card_gr_cd": {"map": {"S": 1, "G": 2, "V": 3}, "default": 0},
            "mng_nice_cb_grd": {
                "map": {"01": 1, "02": 2, "03": 3, "04": 4, "05": 5, "06": 6, "07": 7, "08": 8, "09": 9, "10": 10},
                "default": -1,
            },
            "prefer_device_price": {"map": {"M": 1, "H": 2}, "default": 0},
            "prefer_latest_device": {"map": {"M": 1, "H": 2, "R": 3}, "default": 0},
            "prefer_device_manufacturer": {"map": {"lg": 1, "apple": 2, "samsung": 3}, "default": 0},
            "tmap_freq_dest_residence": {"map": {"apart": 1, "complex_redisence": 2, "villa": 3, "officetel": 4}, "default": 0},
        }

        my_model_v1 = LightGBMDeviceModel(
            model=lightgbm_model,
            model_name="my_model",
            model_version="v1",
            model_features=["eqp_mdl_cd", "age"] + model_features,
            default_model_feature_values=default_model_feature_values,
            label_indices=label_indices,
            product_classes=product_classes,
            products=products,
            device_meta=device_meta,
            conversion_formulas=conversion_formulas,
            emb_features=["embedding_vector"],
            default_emb_feature_values=[[0.0] * 64],
            emb_feature_indices=[[0, 1]],
        )

        result = my_model_v1.predict(["eqp_mdl_cd", "value_1", "value_2", "value_3", [[0.1, 0.2]]])

        ```
        """

        feature_indices_non_emb = [i for i, feature in enumerate(model.feature_name()) if not feature.startswith("emb")]
        feature_indices_emb = [i for i, feature in enumerate(model.feature_name()) if feature.startswith("emb")]
        if feature_indices_emb:
            assert (
                feature_indices_non_emb[-1] < feature_indices_emb[0]
            ), "`model`학습에 사용된 feature 중 embedding 피쳐는 반드시 non-embedding 피쳐 뒤에 있어야 합니다."

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

        assert isinstance(label_indices, dict) and len(label_indices) > 0, "`label_indices`는 필수 입력 값 입니다."
        assert isinstance(product_classes, dict) and len(product_classes) > 0, "`product_classes`는 필수 입력 값 입니다."
        assert isinstance(products, dict) and len(products) > 0, "`products`는 필수 입력 값 입니다."
        assert isinstance(high_rank_word, list), "`high_rank_word`리스트 타입이어야 합니다."

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
                "`device_meta.item`의 `values`는 `product_grp_id`, `product_grp_nm`, `mfact_nm`키를 포함하여야 합니다."
            )

        super().__init__(model, model_name, model_version, model_features + emb_features)

        self.default_model_feature_values = default_model_feature_values
        self.index_labels = {v: k for k, v in label_indices.items() if k in product_classes}
        self.product_classes = product_classes
        self.products = products
        self.device_meta = {meta["name"]: meta["values"] for meta in device_meta.items}
        self.conversion_formulas = conversion_formulas
        self.default_emb_feature_values = default_emb_feature_values
        self.emb_feature_indices = emb_feature_indices
        self.default_context_value = default_context_value
        self.num_pick = num_pick
        self.high_rank_word = high_rank_word

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        # 1. 전처리
        model_x = self._preprocess(x[2:])

        # 2. ML Prediction
        y = self._ml_predict(model_x)

        # 3. 후처리
        items = self._postprocess(y, x[0], x[1])

        return {"items": items}

    def _preprocess(self, x: List[Any]) -> List[Any]:
        if len(self.features) - 2 != len(x):
            raise MLSModelError("`x`와 `features`(첫 두개(`eqp_mdl_cd`, `age`)제외)의 길이가 다릅니다.")

        # - 1.1 피쳐 나누기
        emb_x = x[len(x) - len(self.default_emb_feature_values) :]
        for i, emb_f in enumerate(emb_x):
            if not emb_f:
                emb_x[i] = self.default_emb_feature_values[i]
                continue
            if not isinstance(emb_f, list):
                raise MLSModelError("LightGBMDeviceModel: emb_x는 list 타입이어야 합니다.")
            if len(emb_f) != len(self.default_emb_feature_values[i]):
                raise MLSModelError("LightGBMDeviceModel: emb_x와 `default_emb_feature_values`의 임베딩 피쳐 길이가 다릅니다.")
            if len(emb_f) < len(self.emb_feature_indices[i]):
                raise MLSModelError("LightGBMDeviceModel: `emb_feature_indices`의 임베딩 피쳐 인덱스 길이가 emb_x 임베딩 피쳐 길이보다 큽니다.")

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

    def _ml_predict(self, x: List[Any]) -> List[float]:
        return self.models[0].predict(np.array([x]))[0].tolist()

    def _postprocess(self, y: List[float], user_mdl_cd: str, user_age: int) -> List[Dict[str, Any]]:
        user_device_info = self.device_meta.get(user_mdl_cd, {})

        user_grp_id = user_device_info.get("product_grp_id", "")
        user_grp_nm = user_device_info.get("product_grp_nm", "")
        user_mfact_nm = user_device_info.get("mfact_nm", "")

        results = []
        for label_index, label in self.index_labels.items():
            try:
                prod_list = self.product_classes[label]
                for prod in prod_list:
                    prod.update({"score": y[label_index]})
                    results.append(prod)
            except Exception:
                raise MLSModelError("`label`이 product_classes에 존재하지 않습니다.")

        items = []
        for result in results:
            rec_grp_nm = re.sub("5G|Re", "", result["product_grp_nm"])
            high_rank_eqp_nm_list = [(rec_grp_nm + " " + word).replace("  ", " ") for word in self.high_rank_word]

            # 본인 단말기 제외
            if result["product_grp_id"] == user_grp_id:
                score = 0
            # 애플 고객에게는 아이폰만 추천
            elif user_mfact_nm == "Apple" and result["mfact_nm"] == "Apple":
                score = 50 * result["device_weight"]
            # 현재 단말기가 울트라, pro 등 상위 단말기일 경우 제외
            elif user_grp_nm in high_rank_eqp_nm_list:
                score = 0
            else:
                score = result["score"] * result["device_weight"]

            # 컨텍스트 빌드
            context_features = self.products.get(result["product_grp_id"], {}).get("context_features", [])
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

            items.append(
                {
                    "id": result["product_grp_id"],
                    "name": result["product_grp_nm"],
                    "score": score,
                    "props": {"context_id": context_id},
                    "type": "device",
                }
            )

        items = sorted(items, key=lambda x: x["score"], reverse=True)[: min(self.num_pick, len(items))]
        return [{k: v for k, v in d.items() if k != "score"} for d in items]

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
