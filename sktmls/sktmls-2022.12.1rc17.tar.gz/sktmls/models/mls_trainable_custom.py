from pathlib import Path
from typing import Dict, List

import pandas as pd
from autogluon.tabular import TabularPredictor, version

MLS_MODEL_DIR = Path.home().joinpath("models")


class MLSTrainableCustom:
    """
    AutoGluon을 통한 학습을 지원하는 클래스입니다.
    이 클래스는 단독으로 상속될 수 없으며 MLSModel과 함께 상속되어야 정상 동작합니다.
    `sktmls.models.contrib.EurekaModel`에서 실사용 가능합니다.
    """

    def fit(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        label: str,
        non_training_features: List[str] = [],
        eval_metric: str = "roc_auc",
        k: int = 30,
        time_limit: int = None,
        ensemble: bool = False,
        num_trials: int = 5,
        search_strategy: str = "auto",
        excluded_model_types: List[str] = [
            "FASTTEXT",
            "AG_TEXT_NN",
            "TRANSF",
            "custom",
        ],
    ) -> None:
        """
        AutoGluon을 통해 모델을 학습합니다.
        모델 학습이 완료되면 `self.models[0]`에 자동으로 할당되며, 이후 `predict` 함수에서 참조될 수 있습니다.
        ## 참고 사항
        - AutoGluon이 자동으로 분류 문제인지 회귀 문제인지 판단합니다.
        - 성능 지표를 설정할 수 있으나, 분류 문제의 경우 기본값인 `roc_auc` 사용을 권장합니다.
        - 회귀 문제에 분류 성능 지표를 세팅하거나 분류 문제에 회귀 성능 지표를 세팅하면 에러가 발생합니다.
        ## Args
        - train_data: (`pandas.DataFrame`) 학습에 사용할 데이터 프레임
        - test_data: (`pandas.DataFrame`) 모델 성능 측정을 위한 테스트 데이터 프레임
        - label: (str) train_data 내 라벨 컬럼 이름
        - non_training_features: (optional) (str) 학습에서 제외할 피쳐 이름 리스트. 후처리 전용 피쳐 등을 명세할 때 사용 가능 (기본값: [])
        - eval_metric: (optional) (str) 성능 지표 (기본값: `roc_auc`)
            - 분류 모델의 경우 가능한 값: `accuracy`|`balanced_accuracy`|`f1`|`f1_macro`|`f1_micro`|`f1_weighted`|`roc_auc`|`average_precision`|`precision`|`precision_macro`|`precision_micro`|`precision_weighted`|`recall`|`recall_macro`|`recall_micro`|`recall_weighted`|`log_loss`|`pac_score`
            - 회귀 모델의 경우 가능한 값: `root_mean_squared_error`|`mean_squared_error`|`mean_absolute_error`|`median_absolute_error`|`r2`
        - k: (optional) (int) Feature importance를 바탕으로 선택할 상위 피쳐의 개수 (기본값: 20)
        - time_limit: (optional) (int) 학습 시간 제한 시간 (단위: 초). n개의 모델을 학습하는 경우 1/n초씩 사용. None인 경우 무제한 (기본값: None)
        - ensemble: (optional) (bool) 앙상블 모델 학습 여부. 추론 시간이 길어지므로 학습 후 벤치마크 필수 (기본값: False)
        - num_trials: (optional) (int) Number of hpo trials you want to perform
        - search_strategy: (optional) (str) Search algorithm used by hpo experiment. ‘auto’: Random search. ‘random’: Random search. ‘bayes’: Bayes Optimization. Only supported by Ray Tune backend.
        - excluded_model_types: (optional) (List[str]) Banned subset of model types to avoid training during fit(), even if present in hyperparameters. Reference hyperparameters documentation for what models correspond to each value.
        ## Example
        features = [...]
        preprocess_logic = {...}
        postprocess_logic = {...}
        # 학습을 직접 할 것이므로 `model`을 `None`으로 할당합니다.
        my_model_v1 = GenericLogicModel(
            model=None,
            model_name="my_model",
            model_version="v1",
            features=features,
            preprocess_logic=preprocess_logic,
            postprocess_logic=postprocess_logic,
            predict_fn="predict_proba"
        )
        # 학습 및 테스트 데이터 준비
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=0)
        # 학습
        my_model_v1.fit(
            train_data=train_data,
            test_data=test_data,
            label="some_label"
        )
        # 성능 확인
        print(my_model_v1.performance)
        print(my_model_v1.feature_importance)
        # predict 테스트
        print(my_model_v1.predict(test_feature_values, pf_client=pf_client, graph_client=graph_client))
        # 배포
        model_registry = ModelRegistry(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE)
        model_registry.save(my_model_v1)
        """

        self.model_lib = "autogluon"
        self.model_lib_version = version.__version__
        self.metric = eval_metric
        self.label = label
        self.non_training_features = non_training_features
        self.preprocess_logic = {"merge": [{"var": f} for f in self.features if f not in non_training_features]}
        self.num_trials = num_trials
        self.search_strategy = search_strategy
        self.excluded_model_types = excluded_model_types
        feature_cnt_check = [i for i in self.features if i not in self.non_training_features]
        if len(feature_cnt_check) <= k:
            self.models[0] = self._fit(train_data, eval_metric, time_limit, ensemble)
            self.models[0].delete_models(models_to_keep="best", dry_run=False)
            best_model = self.models[0].get_model_best()
            self.feature_importance = self.get_feature_importance(test_data).to_dict()
        else:
            if time_limit is None:
                self.models[0] = self._fit(train_data, eval_metric, time_limit, False)
                self.models[0].delete_models(models_to_keep="best", dry_run=False)
                best_model = self.models[0].get_model_best()
                feature_importance = self.get_feature_importance(test_data)
                top_features = feature_importance[:k].index.tolist()
                if len(self.features) > len(top_features):
                    self.features = top_features + non_training_features
                    self.preprocess_logic = {"merge": [{"var": f} for f in top_features]}
                    self.models[0] = self._fit(train_data, eval_metric, time_limit, ensemble)
                    self.feature_importance = self.get_feature_importance(test_data).to_dict()
            else:
                self.models[0] = self._fit(train_data, eval_metric, int(time_limit / 3), False)
                self.models[0].delete_models(models_to_keep="best", dry_run=False)
                best_model = self.models[0].get_model_best()
                feature_importance = self.get_feature_importance(test_data)
                top_features = feature_importance[:k].index.tolist()
                if len(self.features) > len(top_features):
                    self.features = top_features + non_training_features
                    self.preprocess_logic = {"merge": [{"var": f} for f in top_features]}
                    self.models[0] = self._fit(train_data, eval_metric, time_limit - int(time_limit / 3), ensemble)
                    self.feature_importance = self.get_feature_importance(test_data).to_dict()
        self.performance = self.evaluate(test_data)
        self.model_info_origin = self.models[0].info()
        self.model_info = self.model_info_origin["model_info"][best_model]
        self.model_info.pop("path", None)
        self.model_info.pop("feature_metadata", None)
        self.model_info.pop("stacker_info", None)
        self.model_info.pop("bagged_info", None)
        self.model_info.pop("children_info", None)
        self.models[0].save_space(remove_data=True, remove_fit_stack=False, requires_save=False, reduce_children=False)
        self.models[0]._trainer.reset_paths = True

    def _fit(
        self,
        train_data: pd.DataFrame,
        eval_metric: str,
        time_limit: int,
        ensemble: bool,
    ):
        columns = [f for f in self.features if f not in self.non_training_features] + [self.label]
        predictor = TabularPredictor(
            label=self.label, eval_metric=eval_metric, path=MLS_MODEL_DIR.joinpath(self.model_name, self.model_version)
        )
        return predictor.fit(
            train_data=train_data[columns],
            presets="good_quality_faster_inference_only_refit" if ensemble else "medium_quality_faster_train",
            time_limit=time_limit,
            excluded_model_types=self.excluded_model_types,
        )

    def batch_prediction(self, batch_data: pd.DataFrame) -> pd.DataFrame:
        """
        AutoGluon을 통해 학습한 모델의 배치 예측을 지원합니다.
        """
        assert self.predict_fn in [
            "predict",
            "predict_proba",
        ], "배치 예측 시 `predict_fn`은 predict, predict_proba 중 하나의 값이어야 합니다."

        if self.predict_fn == "predict":
            return self.models[0].predict(batch_data)
        elif self.predict_fn == "predict_proba":
            return self.models[0].predict_proba(batch_data)

    def evaluate(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """
        AutoGluon을 통해 학습한 모델의 성능을 계산합니다.
        ## 참고 사항
        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        - `fit` 함수에서는 모델 학습 후 한 차례 본 함수를 실행하여 `self.performance`에 저장합니다.
        ## Args
        - test_data: (optional) (`pandas.DataFrame`) 모델 성능 측정을 위한 테스트 데이터 프레임 (기본값: None)
        ## Example
        # 학습 및 테스트 데이터 준비
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=0)
        # 학습
        my_model_v1.fit(
            train_data=train_data,
            test_data=test_data,
            label="some_label"
        )
        # 성능 계산
        print(my_model_v1.evaluate(test_data))
        """
        columns = [f for f in self.features if f not in self.non_training_features] + [self.label]
        return self.models[0].evaluate(test_data[columns], silent=True)

    def get_feature_importance(self, test_data: pd.DataFrame) -> pd.Series:
        """
        AutoGluon을 통해 학습한 모델의 피쳐 중요도를 계산하여 `pandas.Series` 형식으로 리턴합니다.
        ## 참고 사항
        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        - `fit` 함수에서는 모델 학습 후 한 차례 본 함수를 실행하여 `self.feature_importance`에 저장합니다.
        ## Args
        - test_data: (optional) (`pandas.DataFrame`) 모델 성능 측정을 위한 테스트 데이터 프레임 (기본값: None)
        ## Example
        # 학습 및 테스트 데이터 준비
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=0)
        # 학습
        my_model_v1.fit(
            train_data=train_data,
            test_data=test_data,
            label="some_label"
        )
        # 성능 계산
        print(my_model_v1.get_feature_importance(test_data))
        """
        columns = [f for f in self.features if f not in self.non_training_features] + [self.label]
        return self.models[0].feature_importance(test_data[columns], silent=True)["importance"]

    def set_mms_path(self) -> None:
        """
        MMS에서의 정상적인 inference를 위한 path 업데이트 함수로 내부 호출 용도입니다.
        """
        trainer = self.models[0]._trainer
        for model_name in trainer.get_model_names():
            trainer.set_model_attribute(
                model_name, "path", f"/models/{self.model_name}/{self.model_version}/models/{model_name}/"
            )

    def set_local_path(self) -> None:
        """
        로컬 환경에서의 정상적인 inference를 위한 path 업데이트 함수로 내부 호출 용도입니다.
        """
        trainer = self.models[0]._trainer
        for model_name in trainer.get_model_names():
            trainer.set_model_attribute(
                model_name, "path", f"{MLS_MODEL_DIR}/{self.model_name}/{self.model_version}/models/{model_name}/"
            )

    def persist_models(self) -> None:
        """
        모델 캐시를 위한 함수로 내부 호출 용도입니다.
        """
        self.models[0].persist_models()

    def unpersist_models(self) -> None:
        """
        모델 캐시 만료를 위한 함수로 내부 호출 용도입니다.
        """
        self.models[0].unpersist_models()

    def get_model_names_persisted(self) -> List[str]:
        """
        캐시된 모델 이름 조회를 위한 함수로 내부 호출 용도입니다.
        """
        return self.models[0].get_model_names_persisted()
