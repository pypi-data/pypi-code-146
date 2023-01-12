from sktmls.apis import MLSProfileAPIClient
from typing import Dict, List, Any
from sktmls import MLSENV, MLSRuntimeENV
from sktmls.utils import LogicConverter
from sktmls.models import MLSModelError
import hvac
import time
import numpy as np


class EurekaModelTest(MLSProfileAPIClient):
    def __init__(
        self,
        profile_id: str,
        model,
        client_id: str = "netcrm",
        apikey: str = "DGHIIVU4PS4FI9ECJJ7QWHKN9OS8OHVGR1S961YC",
        env: str = "stg",
        runtime_env: str = "ye",
        additional_keys: str = None,
    ):
        """
        AutoGluon을 통해 학습한 모델의 테스트를 지원합니다.
        ## Example
        # 기학습 모델 준비
        model_test = EurekaModelTest(
            profile_id='user_profile_smp_result',
            model = kyu_test_model,
            client_id = "netcrm",
            apikey = "DGHIIVU4PS4FI9ECJJ7QWHKN9OS8OHVGR1S961YC",
            env = "stg",
            runtime_env = "ye",
        )
        # prediction & 후처리 테스트 Example
        result = model_test.test_logic(user_id = user_id)
        print(result)
        [{'id': 'prod_id', 'name': 'prod_nm', 'type': 'vas', 'props': {'class': 'sub', 'fee_prod_id': 'NA00006402', 'score': 0.4414701759815216}}]

        #전처리 결과
        user_profile_dict, preprocessed_features = model_test._preprocess_logic_test(user_id = user_id)
        #예측 결과
        predictions = model_test._ml_prediction_test(preprocessed_features = preprocessed_features)
        #후처리 결과
        result = model_test._postprocess_logic_test(user_profile_dict = user_profile_dict
                                                   , user_id = user_id
                                                   , additional_keys = None
                                                   , predictions = predictions)
        print(result)

        user_profile_dict, preprocessed_features, predictions = model_test._ml_predict(user_id=user_id)
        print(predictions)
        [0.7659122347831726, 0.2340877503156662]
        # 후처리 테스트
        results= model_test._postprocess_logic_test(user_profile_dict = user_profile_dict, user_id = user_id, predictions = predictions)
        print(results)
        [{'id': 'prod_id', 'name': 'prod_nm', 'type': 'vas', 'props': {'class': 'sub', 'fee_prod_id': 'NA00006402', 'score': 0.4414701759815216}}]
        """
        assert type(env) is str, "테스트 환경 값은 String 이어야 합니다.(stg, dev, prd)"
        assert type(runtime_env) is str, "runtime_env 값은 String 이어야 합니다.(ye, mms etc)"
        assert type(profile_id) is str, "profile_id 값은 String 이어야 합니다.(user_profile_smp_result etc)"
        assert type(client_id) is str, "client_id 값은 String 이어야 합니다.(netcrm etc)"
        assert type(apikey) is str, "apikey 값은 String 이어야 합니다. "
        self.env = env
        self.profile_id = profile_id
        self.model = model
        self.pf_client = MLSProfileAPIClient(
            env=MLSENV.PRD if env == "prd" else MLSENV.STG,
            runtime_env=MLSRuntimeENV.MMS if runtime_env == "mms" else MLSRuntimeENV.YE,
            client_id=client_id,
            apikey=apikey,
        )
        self.additional_keys = additional_keys

    def _preprocess_logic_test(
        self,
        user_id: str,
    ) -> List[Any]:
        assert type(user_id) is str, "테스트하고자 하는 유저 ID 값은 str 이어야 합니다."

        user_profile_dict = self.pf_client.get_user_profile(
            profile_id=self.profile_id,
            user_id=user_id,
            keys=self.model.features,
        )

        # features 순서에 맞게 리스트로 정리
        feature_values = [user_profile_dict[feature_name] for feature_name in self.model.features]
        # Preprocessing
        preprocessed_features = self.model._preprocess(
            x=feature_values,
            additional_keys=self.additional_keys,
            pf_client=self.pf_client,
            dynamodb_client=None,
            graph_client=None,
        )
        return user_profile_dict, preprocessed_features

    def _ml_prediction_test(
        self,
        preprocessed_features,
    ) -> List[Any]:
        """
        AutoGluon을 통해 학습한 모델의 전처리 및 예측 결과를 반환합니다.
        ## Example
        # 학습 및 테스트 데이터 준비
        model_test = MLSModelTest(
            profile_id=profile_id,
            model = model_name,
            client_id = client_id,
            apikey = apikey,
            env = "stg",
            runtime_env = "ye",
        )
        # prediction Example
        user_profile_dict, preprocessed_features, predictions = model_test._ml_predict(user_id=user_id)
        print(predictions)
        [0.7659122347831726, 0.2340877503156662]
        """
        # ML Prediction
        predictions = self.model._ml_predict(preprocessed_x=preprocessed_features)

        return predictions

    def _postprocess_logic_test(
        self, user_profile_dict: Dict[str, Any], user_id: str, additional_keys: str, predictions: Dict[str, Any] = None
    ):
        """
        AutoGluon을 통해 학습한 모델의 후처리 결과를 반환합니다.
        ## 참고 사항
        - `postprocess_logic_func` 함수를 통해 동작하므로 postprocess_logic_func 는 함수여야 합니다.
        ## 후처리 Example
        results= model_test._postprocess_logic_test(user_profile_dict = user_profile_dict, user_id = user_id, predictions = predictions)
        print(results)
        [{'id': 'prod_id', 'name': 'prod_nm', 'type': 'vas', 'props': {'class': 'sub', 'fee_prod_id': 'NA00006402', 'score': 0.4414701759815216}}]
        """
        assert isinstance(user_profile_dict, dict), "`user_profile_dict`는 dict 타입이어야 합니다."
        assert type(user_id) is str, "테스트하고자 하는 유저 ID 값은 str 이어야 합니다."
        assert type(predictions) is list, "테스트하고자 하는 predictions 값은 list 이어야 합니다."
        data = user_profile_dict
        data["additional_keys"] = self.additional_keys
        data["y"] = predictions
        data["user_id"] = user_id

        postprocessing_user_profile = self.model.postprocessing_user_profile
        if postprocessing_user_profile:
            for user_profile in postprocessing_user_profile:
                user_values = self.pf_client.get_user_profile(
                    profile_id=user_profile, user_id=data["user_id"], keys=postprocessing_user_profile[user_profile]
                )
                assert (
                    None not in user_values.values()
                ), "후처리 시 사용되는 `user profile` 변수의 값은 사용되는 `user profile`에 있어야 합니다."
                data.update(user_values)

        postprocessing_item_profile_preprocessed = self.model._get_var(
            data=data, postprocessing_item_profile=self.model.postprocessing_item_profile
        )

        if postprocessing_item_profile_preprocessed:
            for item_profile in postprocessing_item_profile_preprocessed:
                for item_id, keys in postprocessing_item_profile_preprocessed[item_profile].items():
                    item_values = self.pf_client.get_item_profile(profile_id=item_profile, item_id=item_id, keys=keys)
                    data.update(item_values)
                    assert (
                        None not in user_values.values()
                    ), "후처리 시 사용되는 `item profile` 변수의 값은 사용되는 `item profile`에 있어야 합니다."
        try:
            if self.model.postprocess_logic is not None:
                assert isinstance(
                    self.model.postprocess_logic, bytes
                ), "`postprocess_logic`은 Logic Converter를 통해 변환된 타입이어야 합니다."
                Handler = LogicConverter(user_converted_logic=self.model.postprocess_logic).ConvertToFunction(
                    name=f"{self.model.model_name}_{self.model.model_version}_Handler"
                )
                assert hasattr(Handler, "__call__") is True, "후처리 로직은 함수이어야 합니다."
                return Handler(data)
        except Exception as e:
            raise MLSModelError(f"EurekaModel: 후처리에 실패했습니다. {e}")

    def test_logic(
        self,
        user_id: str,
    ) -> Any:
        """
        AutoGluon을 통해 학습한 모델의 테스트를 지원합니다.
        # prediction & 후처리 테스트 Example
        result = model_test.test_logic(user_id = user_id)
        print(result)
        [{'id': 'prod_id', 'name': 'prod_nm', 'type': 'vas', 'props': {'class': 'sub', 'fee_prod_id': 'NA00006402', 'score': 0.4414701759815216}}]
        """

        user_profile_dict, preprocessed_features = self._preprocess_logic_test(user_id=user_id)
        predictions = self._ml_prediction_test(preprocessed_features=preprocessed_features)
        return self.model._postprocess(
            x=preprocessed_features + [user_id],
            additional_keys=self.additional_keys,
            y=predictions,
            pf_client=self.pf_client,
            graph_client=None,
            dynamodb_client=None,
        )


def get_secrets(path, parse_data=True):
    vault_client = hvac.Client()
    data = vault_client.secrets.kv.v2.read_secret_version(path=path)
    if parse_data:
        data = data["data"]["data"]
    return data


def generate_configs(env, user):
    import pkg_resources
    from packaging import version
    from sktmls import MLSENV

    mlsenv = MLSENV.STG
    if env == "prd":
        mlsenv = MLSENV.PRD
    secrets = get_secrets(path="mls")
    config = dict(
        env=mlsenv,
        username=secrets.get(f"{user}_id"),
        password=secrets.get(f"{user}_pass"),
    )

    # sktmls version upgrade 후 수정
    mls_v = pkg_resources.get_distribution("sktmls").version
    if version.parse(mls_v) > version.parse("2020.8.29"):
        from sktmls import MLSRuntimeENV

        return [{**config, "runtime_env": r} for r in MLSRuntimeENV.list_items() if r != MLSRuntimeENV.EDD]

    return [config]


def get_mls_config(env, user):
    import concurrent.futures

    configs = generate_configs(env=env, user=user)
    e = concurrent.futures.ThreadPoolExecutor(max_workers=len(configs) + 1)
    fs = [e.submit(check_client_config, conf) for conf in configs]
    for f in concurrent.futures.as_completed(fs):
        if f.exception() is None:
            config = f.result()
            break
    e.shutdown(wait=False)
    return config


def check_client_config(config):
    from sktmls.meta_tables.meta_table import MetaTableClient

    client = MetaTableClient(**config)
    client.list_meta_tables()
    return config


def get_mls_ml_model_client(env="stg", user="aa2"):
    from sktmls.models import MLModelClient

    config = get_mls_config(env, user)
    return MLModelClient(**config)


def get_mls_experiment_client(env="stg", user="aa2"):
    from sktmls.experiments import ExperimentClient

    config = get_mls_config(env, user)
    return ExperimentClient(**config)


def get_mls_profile_api_client(env="stg", user="aa2"):
    from sktmls.apis.profile_api import MLSProfileAPIClient

    config = dict({conf for conf in get_mls_config(env, user).items() if conf[0] in ["env", "runtime_env"]})
    return MLSProfileAPIClient(**config, **get_secrets("mls").get("reco_api"))


def get_mls_recommendation_api_client(env="stg", user="aa2"):
    from sktmls.apis.recommendation_api import MLSRecommendationAPIClient

    config = dict({conf for conf in get_mls_config(env, user).items() if conf[0] in ["env", "runtime_env"]})
    return MLSRecommendationAPIClient(**config, **get_secrets("mls").get("reco_api"))


class EurekaExpModelTest:
    def __init__(
        self,
        env: str = "stg",
        user: str = "aa2",
        model_name: str = "kyu_auto_test_model",
        model_version: str = "v1",
        test_experiment: str = "kyu_test_model",
        test_channel: str = "kyu_test_model",
        bucket_name: str = "A",
    ):
        """
        AutoGluon을 통해 학습한 모델의 실제 MLS 연결 테스트를 지원합니다.
        ## Example
        exp_test = EurekaExpModelTest(env= "stg",
            user= "aa2",
            model_name = "kyu_auto_test_model",
            model_version = "v1",
            test_experiment = "kyu_test_model",
            test_channel = "kyu_test_model",
            bucket_name = "A"
        )

        # 실제 실험 연결 및 테스트
        test_info, success_svc, error_svc, running_time = exp_test.model_test_real_experiments(user_ids= user_ids, prediction_type='online')
        print(test_info)
        {'NUMBER_OF_NO_USER_PROFILE': 34, 'NUMBER_OF_SUCCESS': 65, 'NUMBER_OF_EMPTY_RESPONSE': 0, 'NUMBER_OF_ERROR': 0, 'RUNNING_TIME_AVG': 0.2112327428964468}

        #실제 실험 연결
        profile_api_client, recommendation_api_client = exp_test.test_model_connect_experiment(prediction_type = "online")
        """
        assert type(env) is str, "테스트 환경 값은 String 이어야 합니다.(stg, prd)"
        assert type(user) is str, "user 값은 String 이어야 합니다.(aa2 etc)"
        assert type(model_name) is str, "model_name 값은 String 이어야 합니다.(kyu_auto_test_model etc)"
        assert type(model_version) is str, "model_version 값은 String 이어야 합니다.(v1 etc)"
        assert type(test_experiment) is str, "test_experiment 값은 String 이어야 합니다.(kyu_test_model etc)"
        assert type(test_channel) is str, "test_channel 값은 String 이어야 합니다.(kyu_test_model etc)"
        assert type(bucket_name) is str, "bucket_name 값은 String 이어야 합니다.(A etc)"
        self.env = env
        self.user = user
        self.model_name = model_name
        self.model_version = model_version
        self.test_experiment = test_experiment
        self.test_channel = test_channel
        self.bucket_name = bucket_name

    def test_model_connect_experiment(self, prediction_type="online"):
        model_client = get_mls_ml_model_client(env=self.env, user=self.user)
        model = model_client.get_manual_model(name=self.model_name, version=self.model_version)

        experiment_client = get_mls_experiment_client(env=self.env, user=self.user)
        my_experiment = experiment_client.get_experiment(name=self.test_experiment)

        my_bucket = experiment_client.get_bucket(experiment=my_experiment, name=self.bucket_name)

        experiment_client.update_bucket(bucket=my_bucket, prediction_type=prediction_type, model=model)

        recommendation_api_client = get_mls_recommendation_api_client(env=self.env, user=self.user)
        profile_api_client = get_mls_profile_api_client(env=self.env, user=self.user)
        return profile_api_client, recommendation_api_client

    def model_test_real_experiments(self, user_ids: List[str], prediction_type: str = "online") -> List[Any]:
        assert isinstance(user_ids, list), "`user_id`은 list 타입이어야 합니다."
        assert type(prediction_type) is str, "`prediction_type`은 str 타입이어야 합니다."

        profile_api_client, recommendation_api_client = self.test_model_connect_experiment(
            prediction_type=prediction_type
        )

        no_user_profile_cnt = 0
        success_cnt = 0
        empty_reponse_cnt = 0
        error_cnt = 0

        error_svc = []
        success_svc = []

        running_time = []

        for i in range(0, len(user_ids)):
            try:
                profile_api_client.get_user_profile(profile_id="user_default", user_id=user_ids[i], keys=["user_id"])[
                    "user_id"
                ]
                try:
                    start_time = time.time()
                    response = recommendation_api_client.predict(
                        api_type="user",
                        target_id=user_ids[i],
                        channel_ids=[self.test_channel],
                    )[self.test_channel]
                    end_time = time.time()
                    running_time.append(end_time - start_time)
                    if len(response) < 1:
                        empty_reponse_cnt = empty_reponse_cnt + 1
                    else:
                        success_svc.append(user_ids[i])
                        success_cnt = success_cnt + 1
                except Exception as e:
                    error_svc.append(user_ids[i])
                    print(f"error svc: {user_ids[i]}")
                    print(e)
                    error_cnt = error_cnt + 1
            except Exception:
                no_user_profile_cnt = no_user_profile_cnt + 1

        test_info = {
            "NUMBER_OF_NO_USER_PROFILE": no_user_profile_cnt,
            "NUMBER_OF_SUCCESS": success_cnt,
            "NUMBER_OF_EMPTY_RESPONSE": empty_reponse_cnt,
            "NUMBER_OF_ERROR": error_cnt,
            "RUNNING_TIME_AVG": np.mean(running_time),
        }
        return test_info, success_svc, error_svc, running_time
