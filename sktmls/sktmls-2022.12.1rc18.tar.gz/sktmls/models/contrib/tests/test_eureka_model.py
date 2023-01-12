import numpy as np

from sktmls import MLSRuntimeENV
from sktmls.apis import MLSProfileAPIClient, MLSGraphAPIClient
from sktmls.dynamodb import DynamoDBClient
from sktmls.models.contrib import EurekaModel
from sktmls.utils import LogicConverter


class TestEurekaModel:
    def test_000_generic_context_success(self, mocker):
        mocker.patch(
            "sktmls.models.contrib.eureka_model.EurekaModel._ml_predict",
            return_value=np.array([0, 1]),
        )
        mocker.patch("sktmls.apis.MLSProfileAPIClient.get_item_profile", return_value={"test_dimension": 300})
        mocker.patch(
            "sktmls.apis.MLSGraphAPIClient.list_vertices",
            return_value=[{"id": "test001", "label": "testlabel", "properties": {"hello": "world"}}],
        )
        mocker.patch("sktmls.dynamodb.DynamoDBClient.get_item", return_value={"id": "ITEM0001", "age": 3})

        def Handler(data=None):
            if data:
                return {
                    "id": "prod_id",
                    "name": "prod_nm",
                    "type": "vas",
                    "props": {"class": "sub", "score": data["y"][1]},
                }

            else:
                return []

        handler = LogicConverter(user_defined_func=Handler).FunctionToConvert()

        automl = EurekaModel(
            model_name="test_model",
            model_version="test_version",
            features=["feature1", "feature2", "feature3", "emb_feature1", "context_feature1", "context_feature2"],
            preprocess_logic=None,
            postprocess_logic=handler,
            predict_fn="predict",
            use_logic_processer="N",
        )

        assert automl._preprocess(
            [9.0, 10.0, 2.0, 4.0, None, "Y"],
            [1],
            MLSProfileAPIClient(client_id="a", apikey="a"),
            MLSGraphAPIClient(),
            DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == [9.0, 10.0, 2.0, 4.0, None, "Y"]

        assert automl._postprocess(
            x=[9.0, 10.0, 2.0, 4.0, 8.0, "Y"],
            additional_keys=[1],
            y=[0, 3],
            pf_client=MLSProfileAPIClient(client_id="a", apikey="a"),
            graph_client=MLSGraphAPIClient(),
            dynamodb_client=DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == [{"id": "prod_id", "name": "prod_nm", "type": "vas", "props": {"class": "sub", "score": 3}}]

        assert automl.predict([9.0, 10.0, 2.0, 4.0, None, "Y"],) == {
            "items": [
                {
                    "id": "prod_id",
                    "name": "prod_nm",
                    "type": "vas",
                    "props": {"class": "sub", "score": 1},
                }
            ]
        }

    def test_001_generic_context_success(self, mocker):
        mocker.patch(
            "sktmls.models.contrib.eureka_model.EurekaModel._ml_predict",
            return_value=np.array([0, 1]),
        )
        mocker.patch("sktmls.apis.MLSProfileAPIClient.get_item_profile", return_value={"test_dimension": 300})
        mocker.patch(
            "sktmls.apis.MLSGraphAPIClient.list_vertices",
            return_value=[{"id": "test001", "label": "testlabel", "properties": {"hello": "world"}}],
        )
        mocker.patch("sktmls.dynamodb.DynamoDBClient.get_item", return_value={"id": "ITEM0001", "age": 3})

        def Handler(data=None):
            if data:
                if data["context_feature2"] < 3:
                    return {
                        "id": "prod_id",
                        "name": "prod_nm",
                        "type": "vas",
                        "props": {"class": "sub", "score": data["y"][1]},
                    }
                else:
                    return {
                        "id": "prod_id",
                        "name": "prod_nm",
                        "type": "vas",
                        "props": {"class": "sub", "score": data["y"][1]},
                    }

            else:
                return {
                    "id": "prod_id",
                    "name": "prod_nm",
                    "type": "vas",
                    "props": {"class": "sub", "score": "None"},
                }

        handler = LogicConverter(user_defined_func=Handler).FunctionToConvert()

        automl = EurekaModel(
            model_name="test_model",
            model_version="test_version",
            features=["feature1", "feature2", "feature3", "emb_feature1", "context_feature1", "context_feature2"],
            preprocess_logic=None,
            postprocess_logic=handler,
            predict_fn="predict",
            use_logic_processer="N",
        )

        assert automl._preprocess(
            [9.0, 10.0, 10.0, None, "Y", 0],
            [1],
            MLSProfileAPIClient(client_id="a", apikey="a"),
            MLSGraphAPIClient(),
            DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == [9.0, 10.0, 10.0, None, "Y", 0]

        assert automl._postprocess(
            x=[9.0, 10.0, 10.0, 2.0, "Y", 10.0],
            additional_keys=[1],
            y=[0, 3],
            pf_client=MLSProfileAPIClient(client_id="a", apikey="a"),
            graph_client=MLSGraphAPIClient(),
            dynamodb_client=DynamoDBClient(runtime_env=MLSRuntimeENV.MMS),
        ) == [
            {
                "id": "prod_id",
                "name": "prod_nm",
                "type": "vas",
                "props": {"class": "sub", "score": 3},
            }
        ]

        assert automl.predict([9.0, 10.0, 10.0, 2.0, "Y", 1.0],) == {
            "items": [
                {
                    "id": "prod_id",
                    "name": "prod_nm",
                    "type": "vas",
                    "props": {"class": "sub", "score": 1},
                }
            ]
        }
