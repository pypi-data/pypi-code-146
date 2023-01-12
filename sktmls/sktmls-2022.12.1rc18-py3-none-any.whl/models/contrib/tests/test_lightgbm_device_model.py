import pytest

import numpy as np

import lightgbm

from sktmls.meta_tables import MetaTable
from sktmls.models.contrib import LightGBMDeviceModel


class TestLightGBMDeviceModels:
    @pytest.fixture(scope="class")
    def param(self):
        return {
            "model": LightGBMDeviceModel(
                model=lightgbm.basic.Booster(train_set=lightgbm.Dataset(np.array([[1, 2]]), np.array([1]))),
                model_name="test_model",
                model_version="test_version",
                model_features=["eqp_mdl_cd", "age"] + ["feature1", "feature2", "feature3", "feature4"],
                default_model_feature_values=[0.0, "N", 10.0, "S"],
                label_indices={
                    "삼성전자_120만원": 0,
                    "삼성전자_160만원": 1,
                    "Apple_120만원": 2,
                    "Apple_160만원": 3,
                    "기타_120만원": 4,
                    "기타_160만원": 5,
                },
                product_classes={
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
                    "삼성전자_120만원": [
                        {
                            "product_grp_id": "000004552",
                            "product_grp_nm": "갤럭시 노트20 5G",
                            "mfact_nm": "삼성전자",
                            "eqp_mdl_cd": "A26X",
                            "rep_eqp_mdl_cd": "A26X",
                            "rep_eqp_yn": "Y",
                            "color_hex": "4A4A4A",
                            "color_nm": "미스틱 그레이",
                            "network_type": "5G",
                            "device_weight": 0.22045896,
                        },
                        {
                            "product_grp_id": "000004432",
                            "product_grp_nm": "갤럭시 A 퀀텀",
                            "mfact_nm": "삼성전자",
                            "eqp_mdl_cd": "A1XG",
                            "rep_eqp_mdl_cd": "A1XG",
                            "rep_eqp_yn": "Y",
                            "color_hex": "191C25",
                            "color_nm": "프리즘 큐브 블랙",
                            "network_type": "5G",
                            "device_weight": 0.07969578,
                        },
                        {
                            "product_grp_id": "000003132",
                            "product_grp_nm": "갤럭시 노트9 (재출시)",
                            "mfact_nm": "삼성전자",
                            "eqp_mdl_cd": "A0M0",
                            "rep_eqp_mdl_cd": "A0M0",
                            "rep_eqp_yn": "Y",
                            "color_hex": "000000",
                            "color_nm": "미드나잇블랙",
                            "network_type": "4G",
                            "device_weight": 0.04440128,
                        },
                    ],
                    "삼성전자_160만원": [
                        {
                            "product_grp_id": "000004553",
                            "product_grp_nm": "갤럭시 노트20 Ultra 5G",
                            "mfact_nm": "삼성전자",
                            "eqp_mdl_cd": "A26Y",
                            "rep_eqp_mdl_cd": "A26Y",
                            "rep_eqp_yn": "Y",
                            "color_hex": "1F1F1F",
                            "color_nm": "미스틱 블랙",
                            "network_type": "5G",
                            "device_weight": 0.14155994,
                        },
                    ],
                },
                products={
                    "000001153": {
                        "name": "갤럭시 S7 엣지",
                        "type": "device",
                        "context_features": ["context_popular_apple_device"],
                        "random_context": False,
                    },
                    "000001672": {
                        "name": "iPhone 7",
                        "type": "device",
                        "context_features": ["context_popular_apple_device"],
                        "random_context": False,
                    },
                    "000004352": {
                        "name": "iPhone SE 2020",
                        "type": "device",
                        "context_features": [
                            "context_age10",
                            "context_age20",
                            "context_age30",
                            "context_default",
                            "context_popular_apple_device",
                        ],
                        "random_context": False,
                    },
                    "000003972": {
                        "name": "iPhone 11",
                        "type": "device",
                        "context_features": ["context_popular_apple_device"],
                        "random_context": False,
                    },
                    "000004552": {
                        "name": "갤럭시 노트20 5G",
                        "type": "device",
                        "context_features": [
                            "context_popular_device",
                            "context_popular_samsung_device",
                            "context_age20",
                            "context_age10",
                            "context_age50",
                            "context_age40",
                            "context_age60plus",
                            "context_age30",
                        ],
                        "random_context": False,
                    },
                    "000004553": {
                        "name": "갤럭시 노트20 Ultra 5G",
                        "type": "device",
                        "context_features": [
                            "context_popular_samsung_device",
                            "context_age20",
                            "context_age50",
                            "context_age40",
                            "context_age30",
                        ],
                        "random_context": False,
                    },
                },
                device_meta=MetaTable(
                    **{
                        "id": 1,
                        "name": "name",
                        "description": "desc",
                        "schema": {},
                        "items": [
                            {
                                "name": "A1GW",
                                "values": {
                                    "color_nm": "실버",
                                    "mfact_nm": "Apple",
                                    "color_hex": "EBEBE3",
                                    "rep_eqp_yn": "N",
                                    "network_type": "4G",
                                    "product_grp_id": "000003973",
                                    "product_grp_nm": "iPhone 11 Pro",
                                    "rep_eqp_mdl_cd": "A1GV",
                                },
                            },
                            {
                                "name": "A26Y",
                                "values": {
                                    "color_nm": "미스틱 블랙",
                                    "mfact_nm": "삼성전자",
                                    "color_hex": "1F1F1F",
                                    "rep_eqp_yn": "Y",
                                    "network_type": "5G",
                                    "product_grp_id": "000004553",
                                    "product_grp_nm": "갤럭시 노트20 Ultra 5G",
                                    "rep_eqp_mdl_cd": "A26Y",
                                },
                            },
                        ],
                        "user": "user",
                        "created_at": "1",
                        "updated_at": "1",
                    }
                ),
                num_pick=3,
            )
        }

    def test_000_generic_context_apple(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([[0.1, 0.2, 0.3, 0.4]]))
        assert len(param.get("model").predict(["A1GW", 25] + [0.0, "N", 10.0, "S"]).get("items")) == 3
        assert param.get("model").predict(["A1GW", 25] + [0.0, "N", 10.0, "S"]) == {
            "items": [
                {
                    "id": "000004352",
                    "name": "iPhone SE (2020)",
                    "props": {"context_id": "context_age20"},
                    "type": "device",
                },
                {
                    "id": "000003972",
                    "name": "iPhone 11",
                    "props": {"context_id": "context_popular_apple_device"},
                    "type": "device",
                },
                {
                    "id": "000004553",
                    "name": "갤럭시 노트20 Ultra 5G",
                    "props": {"context_id": "context_popular_samsung_device"},
                    "type": "device",
                },
            ]
        }

    def test_001_generic_context_samsung(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([[0.1, 0.2, 0.3, 0.4]]))
        assert len(param.get("model").predict(["A26Y", 32] + [0.0, "N", 9.0, "S"]).get("items")) == 3
        assert param.get("model").predict(["A26Y", 32] + [0.0, "N", 9.0, "S"]) == {
            "items": [
                {
                    "id": "000004552",
                    "name": "갤럭시 노트20 5G",
                    "props": {"context_id": "context_popular_device"},
                    "type": "device",
                },
                {"id": "000004432", "name": "갤럭시 A 퀀텀", "props": {"context_id": "context_default"}, "type": "device"},
                {
                    "id": "000004352",
                    "name": "iPhone SE (2020)",
                    "props": {"context_id": "context_age30"},
                    "type": "device",
                },
            ]
        }
