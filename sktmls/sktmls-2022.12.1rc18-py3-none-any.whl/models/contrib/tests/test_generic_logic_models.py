import numpy as np
import lightgbm

from sktmls import MLSRuntimeENV
from sktmls.apis import MLSProfileAPIClient, MLSGraphAPIClient
from sktmls.dynamodb import DynamoDBClient
from sktmls.models.contrib import GenericLogicModel


class TestGenericLogicModel:
    def test_000_generic_context_success(self, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.6]))
        mocker.patch("sktmls.apis.MLSProfileAPIClient.get_item_profile", return_value={"test_dimension": 300})
        mocker.patch(
            "sktmls.apis.MLSGraphAPIClient.list_vertices",
            return_value=[{"id": "test001", "label": "testlabel", "properties": {"hello": "world"}}],
        )
        mocker.patch("sktmls.dynamodb.DynamoDBClient.get_item", return_value={"id": "ITEM0001", "age": 3})

        glm = GenericLogicModel(
            model=lightgbm.basic.Booster(train_set=lightgbm.Dataset(np.array([[1, 2]]), np.array([1]))),
            model_name="test_model",
            model_version="test_version",
            features=["feature1", "feature2", "feature3", "emb_feature1", "context_feature1", "context_feature2"],
            preprocess_logic={
                "merge": [
                    {"var": ["feature1", 0.0]},
                    {"if": [{"==": [{"var": ["feature2", "N"]}, "Y"]}, 1, 0]},
                    {"float": [{"var": ["feature3", "0.0"]}]},
                    {"pick": [{"var": ["emb_feature1", [0.0] * 4]}, [1, 3]]},
                    {"first": [{"pf": ["item", "test_profile", {"var": "additional_keys.0"}, ["test_dimension"]]}, 1]},
                ]
            },
            postprocess_logic={
                "if": [
                    {">": [{"var": "y"}, 0.5]},
                    {
                        "list": [
                            {
                                "dict": [
                                    "id",
                                    "PROD001",
                                    "name",
                                    "제품1",
                                    "type",
                                    "my_type",
                                    "props",
                                    {
                                        "dict": [
                                            "test_score",
                                            {"var": "y"},
                                            "context_id",
                                            {
                                                "if": [
                                                    {"==": [{"var": ["context_feature1", "N"]}, "Y"]},
                                                    "context_feature1",
                                                    {"==": [{"var": ["context_feature2", "N"]}, "Y"]},
                                                    "context_feature2",
                                                    "context_default",
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            }
                        ]
                    },
                    {">": [{"var": "y"}, 0.3]},
                    {
                        "list": [
                            {
                                "dict": [
                                    "id",
                                    "PROD002",
                                    "name",
                                    "제품2",
                                    "type",
                                    "my_type",
                                    "props",
                                    {
                                        "dict": [
                                            "test_score",
                                            {"var": "y"},
                                            "context_id",
                                            {
                                                "if": [
                                                    {"==": [{"var": ["context_feature2", "N"]}, "Y"]},
                                                    "context_feature2",
                                                    {"==": [{"var": ["context_feature1", "N"]}, "Y"]},
                                                    "context_feature1",
                                                    "context_default",
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            }
                        ]
                    },
                    {"list": []},
                ]
            },
            predict_fn="predict",
        )

        assert glm._preprocess(
            [2.0, "Y", "4.0", [1, 2, 3, 4], "Y", "Y"],
            [1],
            MLSProfileAPIClient(client_id="a", apikey="a"),
            MLSGraphAPIClient(),
            DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == [
            2.0,
            1.0,
            4.0,
            2.0,
            4.0,
            300.0,
        ]

        assert glm.predict(
            x=[2.0, "Y", "4.0", [1, 2, 3, 4], "Y", "Y"],
            keys=[1],
            pf_client=MLSProfileAPIClient(client_id="a", apikey="a"),
            graph_client=MLSGraphAPIClient(),
            dynamodb_client=DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == {
            "items": [
                {
                    "id": "PROD001",
                    "name": "제품1",
                    "type": "my_type",
                    "props": {"context_id": "context_feature1", "test_score": 0.6},
                }
            ]
        }

    def test_001_generic_context_success(self, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.5]))
        mocker.patch("sktmls.apis.MLSProfileAPIClient.get_item_profile", return_value={"test_dimension": 300})
        mocker.patch(
            "sktmls.apis.MLSGraphAPIClient.list_vertices",
            return_value=[{"id": "test001", "label": "testlabel", "properties": {"hello": "world"}}],
        )
        mocker.patch("sktmls.dynamodb.DynamoDBClient.get_item", return_value={"id": "ITEM0001", "age": 3})

        glm = GenericLogicModel(
            model=lightgbm.basic.Booster(train_set=lightgbm.Dataset(np.array([[1, 2]]), np.array([1]))),
            model_name="test_model",
            model_version="test_version",
            features=["feature1", "feature2", "feature3", "emb_feature1", "context_feature1", "context_feature2"],
            preprocess_logic={
                "merge": [
                    {"var": ["feature1", 0.0]},
                    {"if": [{"==": [{"var": ["feature2", "N"]}, "Y"]}, 1, 0]},
                    {"float": [{"var": ["feature3", "0.0"]}]},
                    {"pick": [{"var": ["emb_feature1", [0.0] * 4]}, [1, 3]]},
                    {"first": [{"pf": ["item", "test_profile", {"var": "additional_keys.0"}, ["test_dimension"]]}, 1]},
                ]
            },
            postprocess_logic={
                "if": [
                    {">": [{"var": "y"}, 0.5]},
                    {
                        "list": [
                            {
                                "dict": [
                                    "id",
                                    "PROD001",
                                    "name",
                                    "제품1",
                                    "type",
                                    "my_type",
                                    "props",
                                    {
                                        "dict": [
                                            "test_score",
                                            {"var": "y"},
                                            "context_id",
                                            {
                                                "if": [
                                                    {"==": [{"var": ["context_feature1", "N"]}, "Y"]},
                                                    "context_feature1",
                                                    {"==": [{"var": ["context_feature2", "N"]}, "Y"]},
                                                    "context_feature2",
                                                    "context_default",
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            }
                        ]
                    },
                    {">": [{"var": "y"}, 0.3]},
                    {
                        "list": [
                            {
                                "dict": [
                                    "id",
                                    "PROD002",
                                    "name",
                                    "제품2",
                                    "type",
                                    "my_type",
                                    "props",
                                    {
                                        "dict": [
                                            "test_score",
                                            {"var": "y"},
                                            "context_id",
                                            {
                                                "if": [
                                                    {"==": [{"var": ["context_feature2", "N"]}, "Y"]},
                                                    "context_feature2",
                                                    {"==": [{"var": ["context_feature1", "N"]}, "Y"]},
                                                    "context_feature1",
                                                    "context_default",
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            }
                        ]
                    },
                    {"list": []},
                ]
            },
            predict_fn="predict",
        )

        assert glm._preprocess(
            [2.0, "Y", "4.0", [1, 2, 3, 4], "Y", "Y"],
            [1],
            MLSProfileAPIClient(client_id="a", apikey="a"),
            MLSGraphAPIClient(),
            DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == [
            2.0,
            1.0,
            4.0,
            2.0,
            4.0,
            300.0,
        ]

        assert glm.predict(
            x=[2.0, "Y", "4.0", [1, 2, 3, 4], "Y", "Y"],
            keys=[1],
            pf_client=MLSProfileAPIClient(client_id="a", apikey="a"),
            graph_client=MLSGraphAPIClient(),
            dynamodb_client=DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == {
            "items": [
                {
                    "id": "PROD002",
                    "name": "제품2",
                    "type": "my_type",
                    "props": {"context_id": "context_feature2", "test_score": 0.5},
                }
            ]
        }

    def test_002_generic_context_success(self, mocker):
        mocker.patch("lightgbm.basic.Booster.predict", return_value=np.array([0.1]))
        mocker.patch("sktmls.apis.MLSProfileAPIClient.get_item_profile", return_value={"test_dimension": 300})
        mocker.patch(
            "sktmls.apis.MLSGraphAPIClient.list_vertices",
            return_value=[{"id": "test001", "label": "testlabel", "properties": {"hello": "world"}}],
        )
        mocker.patch("sktmls.dynamodb.DynamoDBClient.get_item", return_value={"id": "ITEM0001", "age": 3})

        glm = GenericLogicModel(
            model=lightgbm.basic.Booster(train_set=lightgbm.Dataset(np.array([[1, 2]]), np.array([1]))),
            model_name="test_model",
            model_version="test_version",
            features=["feature1", "feature2", "feature3", "emb_feature1", "context_feature1", "context_feature2"],
            preprocess_logic={
                "merge": [
                    {"var": ["feature1", 0.0]},
                    {"if": [{"==": [{"var": ["feature2", "N"]}, "Y"]}, 1, 0]},
                    {"float": [{"var": ["feature3", "0.0"]}]},
                    {"pick": [{"var": ["emb_feature1", [0.0] * 4]}, [1, 3]]},
                    {"first": [{"pf": ["item", "test_profile", {"var": "additional_keys.0"}, ["test_dimension"]]}, 1]},
                ]
            },
            postprocess_logic={
                "if": [
                    {">": [{"var": "y"}, 0.5]},
                    {
                        "list": [
                            {
                                "dict": [
                                    "id",
                                    "PROD001",
                                    "name",
                                    "제품1",
                                    "type",
                                    "my_type",
                                    "props",
                                    {
                                        "dict": [
                                            "test_score",
                                            {"var": "y"},
                                            "context_id",
                                            {
                                                "if": [
                                                    {"==": [{"var": ["context_feature1", "N"]}, "Y"]},
                                                    "context_feature1",
                                                    {"==": [{"var": ["context_feature2", "N"]}, "Y"]},
                                                    "context_feature2",
                                                    "context_default",
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            }
                        ]
                    },
                    {">": [{"var": "y"}, 0.3]},
                    {
                        "list": [
                            {
                                "dict": [
                                    "id",
                                    "PROD002",
                                    "name",
                                    "제품2",
                                    "type",
                                    "my_type",
                                    "props",
                                    {
                                        "dict": [
                                            "test_score",
                                            {"var": "y"},
                                            "context_id",
                                            {
                                                "if": [
                                                    {"==": [{"var": ["context_feature2", "N"]}, "Y"]},
                                                    "context_feature2",
                                                    {"==": [{"var": ["context_feature1", "N"]}, "Y"]},
                                                    "context_feature1",
                                                    "context_default",
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            }
                        ]
                    },
                    {"list": []},
                ]
            },
            predict_fn="predict",
        )

        assert glm._preprocess(
            [2.0, "Y", "4.0", [1, 2, 3, 4], "Y", "Y"],
            [1],
            MLSProfileAPIClient(client_id="a", apikey="a"),
            MLSGraphAPIClient(),
            DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == [
            2.0,
            1.0,
            4.0,
            2.0,
            4.0,
            300.0,
        ]

        assert glm.predict(
            x=[2.0, "Y", "4.0", [1, 2, 3, 4], "Y", "Y"],
            keys=[1],
            pf_client=MLSProfileAPIClient(client_id="a", apikey="a"),
            graph_client=MLSGraphAPIClient(),
            dynamodb_client=DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == {"items": []}
