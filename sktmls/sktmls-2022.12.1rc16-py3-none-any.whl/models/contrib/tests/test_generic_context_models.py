import pytest

import numpy as np

import lightgbm

from sktmls.models.contrib import GenericContextModel


class TestGenericContextModels:
    @pytest.fixture(scope="class")
    def param(self):
        return {
            "model": GenericContextModel(
                model=lightgbm.basic.Booster(train_set=lightgbm.Dataset(np.array([[1, 2]]), np.array([1]))),
                model_name="test_model",
                model_version="test_version",
                model_features=["feature1", "feature2", "feature3", "feature4"],
                default_model_feature_values=[0.0, "N", 10.0, "S"],
                default_context_value="default_context",
                products={
                    "PROD001": {
                        "name": "제품1",
                        "type": "my_type",
                        "context_features": ["cx_feat1", "cx_feat2"],
                        "random_context": False,
                    },
                    "PROD002": {
                        "name": "제품2",
                        "type": "my_type",
                        "context_features": ["cx_feat1"],
                        "random_context": False,
                    },
                },
                product_selection_logic={
                    "if": [
                        {"and": [{">": [{"var": "y"}, 0.5]}, {"<=": [{"var": "feature3"}, 5]}]},
                        "PROD001",
                        {"<=": [{"var": "y"}, 0.5]},
                        "PROD002",
                        None,
                    ]
                },
                conversion_formulas={"feature4": {"map": {"S": 0, "L": 1}, "default": -1}},
                emb_features=["emb1", "emb2"],
                default_emb_feature_values=[[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0]],
                emb_feature_indices=[[0, 1], [0, 2, 3]],
                context_features=["cx_feat1", "cx_feat2", "cx_feat3"],
                context_values=["cx_value1", "cx_value2", "cx_value3"],
                realtime_features=[],
                include_y=True,
                y_key="test_score",
            )
        }

    def test_000_generic_context_success(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.6]))
        assert param.get("model").predict([2.0, "Y", 4.0, "S", [1, 2, 3, 4], [10, 9, 8, 7], "Y", "Y", "Y"]) == {
            "items": [
                {
                    "id": "PROD001",
                    "name": "제품1",
                    "type": "my_type",
                    "props": {"context_id": "cx_value1", "test_score": 0.6},
                }
            ]
        }

    def test_001_generic_context_success(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.4]))
        assert param.get("model").predict([2.0, "Y", 4.0, "S", [1, 2, 3, 4], [10, 9, 8, 7], "N", "Y", "Y"]) == {
            "items": [
                {
                    "id": "PROD002",
                    "name": "제품2",
                    "type": "my_type",
                    "props": {"context_id": "default_context", "test_score": 0.4},
                }
            ]
        }

    def test_002_generic_context_selection_none(self, param, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.7]))
        assert param.get("model").predict([2.0, "Y", 10.0, "S", [1, 2, 3, 4], [10, 9, 8, 7], "Y", "Y", "Y"]) == {
            "items": []
        }
