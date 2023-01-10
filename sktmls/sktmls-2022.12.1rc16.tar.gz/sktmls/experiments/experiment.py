from typing import Dict, Any, List, Union

from dateutil import parser

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse, MLSClientError
from sktmls.models import ManualModel, AutoMLModel, MLModelClient
from sktmls.filters import Filter
from sktmls.channels import Channel

MLS_EXPERIMENTS_API_URL = "/api/v1/experiments"
MLS_BUCKET_MIGRATIONS_API_URL = "/api/v1/bucket_migrations"


class Experiment:
    """
    MLS 실험 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 실험 고유 ID
            - channels: (list(`sktmls.channels.Channel`)) 실험이 속한 채널 리스트
            - name: (str) 실험 이름
            - description: (str) 실험 설명
            - model_filter: (`sktmls.filters.Filter`) 적용된 필터 (필터 조건 제외)
            - bucketing_seed: (str) 버킷팅 시드
            - user: (str) 실험 소유 계정명
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `sktmls.experiments.Experiment`
        """
        self.id = kwargs.get("id")
        self.channels = kwargs.get("channels")
        self.channels = (
            [Channel(**channel) for channel in kwargs.get("channels")]
            if kwargs.get("channels") is not None
            else kwargs.get("channels")
        )
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.user = kwargs.get("user")
        self.model_filter = (
            Filter(**kwargs.get("model_filter"))
            if kwargs.get("model_filter") is not None
            else kwargs.get("model_filter")
        )
        self.bucketing_seed = kwargs.get("bucketing_seed")

        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None

        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def generate_request_body(self) -> Dict:
        body = {
            "name": self.name,
            "bucketing_seed": self.bucketing_seed,
            "model_filter_id": self.model_filter.id if self.model_filter is not None else None,
        }
        if self.description:
            body["description"] = self.description
        return body


class Bucket:
    """
    MLS 버킷 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 버킷 고유 ID
            - experiment: (int) 버킷이 속한 실험정보
            - prediction: (`sktmls.experiments.Prediction`) 해당 버킷의 Prediction 정보
            - name: (str) 버킷 이름
            - description: (str) 버킷 설명
            - bucket_range: (str) 해당 버킷의 범위
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `sktmls.experiments.Bucket`

        """
        self.id = kwargs.get("id")
        self.experiment = kwargs.get("experiment")
        self.prediction = Prediction(**kwargs.get("prediction")) if kwargs.get("prediction") else None
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.bucket_range = kwargs.get("bucket_range")

        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None

        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def generate_request_body(self) -> Dict:
        data = {
            "name": self.name,
        }

        if self.description:
            data["description"] = self.description

        model_type = self.prediction.request["type"]
        data["prediction_type"] = model_type
        if model_type == "online":
            data["online_model_id"] = self.prediction.ml_model.id
        elif model_type == "batch":
            data["batch_model_id"] = self.prediction.ml_model.id
        elif model_type == "static":
            data["static_value"] = {"items": self.prediction.request["items"]}

        return data


class Prediction:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.request = kwargs.get("request")
        self.ml_model = kwargs.get("ml_model")

    def get(self):
        return self.__dict__


class ExperimentClient(MLSClient):
    """
    MLS 실험 관련 기능들을 제공하는 클라이언트입니다.
    """

    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
        username: str = None,
        password: str = None,
    ):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        아래의 환경 변수가 정의된 경우 해당 파라미터를 생략 가능합니다.

        - $MLS_ENV: env
        - $MLS_RUNTIME_ENV: runtime_env
        - $MLS_USERNAME: username
        - $MLS_PASSWORD: password

        ## Returns
        `sktmls.experiments.ExperimentClient`

        ## Example

        ```python
        experiment_client = ExperimentClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_experiment(
        self, name: str, description: str = None, bucketing_seed: str = "", model_filter: Filter = None
    ) -> Experiment:
        """
        실험을 생성합니다.

        ## Args

        - name: (str) 생성할 실험 이름
        - description: (optional) (str) 생성할 실험 설명
        - bucketing_seed: (optional) (str) 생성할 실험의 버킷팅 시드
        - model_filter: (optional) (`sktmls.filters.Filter`) 생성할 실험의 필터 (필터 조건 제외)

        ## Returns
        `sktmls.experiments.Experiment`

        - id: (int) 실험 고유 ID
        - channels: (list(`sktmls.channels.Channel`)) 실험이 속한 채널 리스트
        - name: (str) 실험 이름
        - description: (str) 실험 설명
        - model_filter: (`sktmls.filters.Filter`) 적용된 필터 (필터 조건 제외)
        - bucketing_seed: (str) 버킷팅 시드
        - user: (str) 실험 소유 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        my_experiment = experiment_client.create_experiment(
            name="my_experiment",
            description="This is my experiment",
            filter=my_filter,
        )
        ```
        """

        data = {"name": name, "bucketing_seed": bucketing_seed}
        if description:
            data["description"] = description
        if model_filter:
            data["model_filter_id"] = model_filter.id

        return Experiment(**self._request(method="POST", url=MLS_EXPERIMENTS_API_URL, data=data).results)

    def remove_filter(self, experiment: Experiment) -> Experiment:
        """
        실험의 필터를 제거합니다.

        ## Args

        - experiment: (`sktmls.experiments.Experiment`) 필터를 제거할 실험

        ## Returns
        `sktmls.experiments.Experiment`

        - id: (int) 실험 고유 ID
        - channels: (list(`sktmls.channels.Channel`)) 실험이 속한 채널 리스트
        - name: (str) 실험 이름
        - description: (str) 실험 설명
        - model_filter: (`sktmls.filters.Filter`) 적용된 필터 (필터 조건 제외)
        - bucketing_seed: (str) 버킷팅 시드
        - user: (str) 실험 소유 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        my_experiment = experiment_client.remove_filter(
            experiment=my_experiment,
        )
        ```
        """
        assert type(experiment) == Experiment
        data = experiment.generate_request_body()
        data.pop("model_filter_id")

        self._request(method="PUT", url=f"{MLS_EXPERIMENTS_API_URL}/{experiment.id}", data=data)

        return self.get_experiment(id=experiment.id)

    def update_experiment(
        self,
        experiment: Experiment,
        name: str = None,
        description: str = None,
        bucketing_seed: str = None,
        model_filter: Filter = None,
    ) -> Experiment:
        """
        실험을 수정합니다. Optional 필드의 경우에 값을 넣지 않을시에는 기존의 값들이 유지됩니다.

        ## Args

        - experiment: (`sktmls.experiments.Experiment`) 수정할 실험
        - name: (optional) (str) 수정할 실험 이름
        - description: (optional) (str) 수정할 실험 설명
        - bucketing_seed: (optional) (str) 수정할 실험의 버킷팅 시드
        - model_filter: (optional) (`sktmls.filters.Filter`) 수정할 실험의 필터 (필터 조건 제외)

        ## Returns
        `sktmls.experiments.Experiment`

        - id: (int) 실험 고유 ID
        - channels: (list(`sktmls.channels.Channel`)) 실험이 속한 채널 리스트
        - name: (str) 실험 이름
        - description: (str) 실험 설명
        - model_filter: (`sktmls.filters.Filter`) 적용된 필터 (필터 조건 제외)
        - bucketing_seed: (str) 버킷팅 시드
        - user: (str) 실험 소유 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        my_experiment = experiment_client.update_experiment(
            experiment=my_experiment,
            description="This is updated experiment",
        )
        ```
        """
        assert type(experiment) == Experiment
        data = experiment.generate_request_body()

        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if bucketing_seed:
            data["bucketing_seed"] = bucketing_seed
        if model_filter:
            data["model_filter_id"] = model_filter.id

        self._request(method="PUT", url=f"{MLS_EXPERIMENTS_API_URL}/{experiment.id}", data=data)

        return self.get_experiment(id=experiment.id)

    def get_experiment(self, id: int = None, name: str = None) -> Experiment:
        """
        실험 정보를 조회합니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) 실험 고유 ID
        - name: (str) 실험 이름

        ## Returns
        `sktmls.experiments.Experiment`

        - id: (int) 실험 고유 ID
        - channels: (list(`sktmls.channels.Channel`)) 실험이 속한 채널 리스트
        - name: (str) 실험 이름
        - description: (str) 실험 설명
        - model_filter: (`sktmls.filters.Filter`) 적용된 필터 (필터 조건 제외)
        - bucketing_seed: (str) 버킷팅 시드
        - user: (str) 실험 소유 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        experiment_by_id = experiment_client.get_experiment(id=3)
        experiment_by_name = experiment_client.get_experiment(name="my_experiment")
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        experiments = self.list_experiments(id=id, name=name)
        if len(experiments) == 0:
            raise MLSClientError(code=404, msg="해당 실험이 없습니다")
        elif len(experiments) > 1:
            raise MLSClientError(code=409, msg="같은 이름의 실험이 여러개 존재합니다.")

        return experiments[0]

    def list_experiments(self, **kwargs) -> List[Experiment]:
        """
        실험의 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 실험 고유 ID
            - name: (str) 실험 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns

        list(`sktmls.experiments.Experiment`)
        - id: (int) 실험 고유 ID
        - channels: (list(`sktmls.channels.Channel`)) 실험이 속한 채널 리스트
        - name: (str) 실험 이름
        - description: (str) 실험 설명
        - model_filter: (`sktmls.filters.Filter`) 적용된 필터 (필터 조건 제외)
        - bucketing_seed: (str) 버킷팅 시드
        - user: (str) 실험 소유 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        experiments = experiment_client.list_experiments()
        ```
        """

        response = self._request(method="GET", url=f"{MLS_EXPERIMENTS_API_URL}", params=kwargs).results

        return [Experiment(**experiment) for experiment in response]

    def delete_experiment(self, experiment: Experiment) -> MLSResponse:
        """
        실험을 삭제합니다.

        ## Args

        - experiment: (`sktmls.experiments.Experiment`) experiment 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        experiment_client.delete_experiment(experiment)
        ```
        """
        assert type(experiment) == Experiment

        return self._request(method="DELETE", url=f"{MLS_EXPERIMENTS_API_URL}/{experiment.id}")

    def update_bucket_ratio(self, experiment: Experiment, bucket_ratio: Dict[Bucket, int]) -> List[Bucket]:
        """
        현재 실험의 버킷 비율을 수정합니다.

        ## Args

        - experiment: (`sktmls.experiments.Experiment`) 수정할 실험
        - bucket_ratio: (dict(Bucket, int)) 키가 버킷 이고 바꾸고자 하는 bucket range 가 값인 Dict

        ## Returns

        list(sktmls.experiments.Bucket)
        - id: (int) 버킷 고유 ID
        - experiment: (int) 버킷이 속한 실험정보
        - prediction: (`sktmls.experiments.Prediction`) 해당 버킷의 Prediction 정보
        - name: (str) 버킷 이름
        - description: (str) 버킷 설명
        - bucket_range: (str) 해당 버킷의 범위
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        buckets = experiment_client.list_buckets(experiment)
        bucket_ratio = {buckets[0]: 40, buckets[1]: 60}
        experiment_client.update_bucket_ratio(experiment, bucket_ratio)
        ```
        """
        assert type(experiment) == Experiment

        ratio_data = {}
        for bucket, value in bucket_ratio.items():
            assert type(bucket) == Bucket
            assert type(value) == int
            ratio_data[bucket.id] = value

        data = {"bucket_ratio": ratio_data}

        response = self._request(
            method="PUT",
            url=f"{MLS_EXPERIMENTS_API_URL}/{experiment.id}/bucket_ratio",
            data=data,
        ).results

        return [Bucket(**bucket) for bucket in response]

    def create_bucket(
        self,
        experiment: Experiment,
        name: str,
        prediction_type: str,
        model: Union[ManualModel, AutoMLModel] = None,
        description: str = None,
        static_value: Dict[str, Any] = None,
    ) -> Bucket:
        """
        버킷을 생성합니다.

        ## Args

        - experiment: (`sktmls.experiments.Experiment`) 수정할 실험
        - name: (str) 생성할 버킷 이름
        - prediction_type: 버킷의 추론 타입 (`empty`|`static`|`batch`|`online`)
        - model: (optional) (`sktmls.models.ManualModel`, `sktmls.models.AutoMLModel`) 버킷에 연결할 모델
        - static_value: (optional) (dict) (고정값일 경우) Static Value
        - description: (optional) (str) 생성할 버킷 설명

        ## Returns
        `sktmls.experiments.Bucket`

        - id: (int) 버킷 고유 ID
        - experiment: (int) 버킷이 속한 실험정보
        - prediction: (`sktmls.experiments.Prediction`) 해당 버킷의 Prediction 정보
        - name: (str) 버킷 이름
        - description: (str) 버킷 설명
        - bucket_range: (str) 해당 버킷의 범위
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        my_batch_model = model_client.get_manual_model(
            name="my_manual_model",
            version="my_manual_version",
        )
        experiment_client.create_bucket(
            experiment=my_experiment,
            name="my_bucket",
            prediction_type="batch",
            model=my_batch_model
        )
        ```
        """
        assert type(experiment) == Experiment
        assert prediction_type in ["empty", "static", "batch", "online"]

        data = {"name": name, "prediction_type": prediction_type}
        if prediction_type == "online":
            assert type(model) in [ManualModel, AutoMLModel]
            data["online_model_id"] = model.id
        elif prediction_type == "batch":
            assert type(model) in [ManualModel, AutoMLModel]
            data["batch_model_id"] = model.id
        elif prediction_type == "static":
            assert static_value
            data["static_value"] = static_value
        elif prediction_type == "automl":
            assert type(model) == AutoMLModel
            data["automl_model_id"] = model.id

        if description:
            data["description"] = description

        resp = self._request(method="POST", url=f"{MLS_EXPERIMENTS_API_URL}/{experiment.id}/buckets", data=data).results
        resp["experiment"] = experiment

        return Bucket(**resp)

    def list_buckets(self, experiment: Experiment, **kwargs) -> List[Bucket]:
        """
        특정 실험에 속한 버킷들의 정보를 조회합니다.

        ## Args

        - experiment: (sktmls.experiments.Experiment) 버킷의 실험 객체
        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 버킷 고유 ID
            - name: (str) 버킷 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.experiments.Bucket`)

        - id: (int) 버킷 고유 ID
        - experiment: (int) 버킷이 속한 실험정보
        - prediction: (`sktmls.experiments.Prediction`) 해당 버킷의 Prediction 정보
        - name: (str) 버킷 이름
        - description: (str) 버킷 설명
        - bucket_range: (str) 해당 버킷의 범위
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        buckets = experiment_client.list_buckets(experiment)
        ```
        """
        assert type(experiment) == Experiment

        resp = self._request(
            method="GET", url=f"{MLS_EXPERIMENTS_API_URL}/{experiment.id}/buckets", params=kwargs
        ).results

        ml_model_client = MLModelClient(
            env=self._MLSClient__env,
            runtime_env=self._MLSClient__runtime_env,
            username=self._MLSClient__username,
            password=self._MLSClient__password,
        )

        buckets = []
        for r in resp:
            r["experiment"] = experiment

            model_id = r.get("prediction", {}).get("ml_model")
            model_type = r.get("prediction", {}).get("request", {}).get("type")

            if model_id:
                if model_type in ["batch", "online"]:
                    model = ml_model_client.get_manual_model(id=model_id)
                elif model_type == "automl":
                    request = r.get("prediction", {}).get("request", {})
                    if request.get("username") == self._MLSClient__username:
                        model = ml_model_client.get_automl_model(id=model_id)
                    else:
                        model = AutoMLModel(
                            id=model_id, name=request.get("model_name"), version=request.get("model_version")
                        )
                else:
                    raise Exception(f"지원하지 않는 모델 타입입니다: {model_type}")
                r["prediction"]["ml_model"] = model
            buckets.append(Bucket(**r))

        return buckets

    def get_bucket(self, experiment: Experiment, id: int = None, name: str = None) -> Bucket:
        """
        버킷 정보를 가져옵니다.

        ## Args: `id` 또는 `name`중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - experiment: (sktmls.experiments.Experiment) 버킷의 실험 객체
        - id: (optional) (int) 버킷 고유 ID
        - name: (optional) (str) 버킷 이름

        ## Returns
        `sktmls.experiments.Bucket`

        - id: (int) 버킷 고유 ID
        - experiment: (int) 버킷이 속한 실험정보
        - prediction: (`sktmls.experiments.Prediction`) 해당 버킷의 Prediction 정보
        - name: (str) 버킷 이름
        - description: (str) 버킷 설명
        - bucket_range: (str) 해당 버킷의 범위
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        my_bucket_by_id = experiment_client.get_bucket(id=3)
        my_bucket_by_name = experiment_client.get_bucket(name="my_bucket")
        ```
        """
        assert type(experiment) == Experiment
        assert id or name, "One of id or name must be provided"

        buckets = self.list_buckets(experiment, id=id, name=name)
        if len(buckets) == 0:
            raise MLSClientError(code=404, msg="해당 버킷이 없습니다")
        elif len(buckets) > 1:
            raise MLSClientError(code=409, msg="같은 이름의 버킷이 여러개 존재합니다.")

        return buckets[0]

    def delete_bucket(self, bucket: Bucket) -> MLSResponse:
        """
        버킷을 삭제합니다.

        ## Args

        - bucket: (sktmls.experiments.Bucket) 삭제할 버킷

        ## Return
        `sktmls.MLSResponse`

        ## Example

        ```python
        bucket_to_delete = experiment_client.get_bucket(id=3)
        experiment_client.delete_bucket(bucket_to_delete)
        ```
        """
        assert type(bucket) == Bucket

        return self._request(
            method="DELETE", url=f"{MLS_EXPERIMENTS_API_URL}/{bucket.experiment.id}/buckets/{bucket.id}"
        )

    def update_bucket(
        self,
        bucket: Bucket,
        name: str = None,
        prediction_type: str = None,
        model: Union[ManualModel, AutoMLModel] = None,
        description: str = None,
        static_value: Dict[str, Any] = None,
    ) -> Bucket:
        """
        버킷을 수정합니다.

        ## Args

        - experiment: (`sktmls.experiments.Experiment`) 수정할 실험
        - name: (optional) (str) 수정할 버킷 이름
        - prediction_type: (optional) 수정할 버킷의 추론 타입 (`empty`|`static`|`batch`|`online`)
        - model: (optional) (`sktmls.models.ManualModel`, `sktmls.models.AutoMLModel`) 수정할 버킷에 연결할 모델
        - static_value: (optional) (dict) (고정값일 경우) Static Value
        - description: (optional) (str) 수정할 버킷 설명


        ## Returns
        `sktmls.experiments.Bucket`

        - id: (int) 버킷 고유 ID
        - experiment: (int) 버킷이 속한 실험정보
        - prediction: (`sktmls.experiments.Prediction`) 해당 버킷의 Prediction 정보
        - name: (str) 버킷 이름
        - description: (str) 버킷 설명
        - bucket_range: (str) 해당 버킷의 범위
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        my_batch_model = model_client.get_manual_model(
            name="my_manual_model",
            version="my_manual_version",
        )
        my_bucket = experiment_client.get_bucket(name="my_bucket")
        experiment_client.update_bucket(
            bucket=my_bucket,
            prediction_type="batch",
            model=my_batch_model
        )
        ```
        """
        assert type(bucket) == Bucket

        data = bucket.generate_request_body()
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if prediction_type:
            assert prediction_type in ["empty", "static", "batch", "online", "automl"]
            data["prediction_type"] = prediction_type
            if prediction_type == "online":
                assert type(model) in [ManualModel, AutoMLModel]
                data["online_model_id"] = model.id
            elif prediction_type == "batch":
                assert type(model) in [ManualModel, AutoMLModel]
                data["batch_model_id"] = model.id
            elif prediction_type == "static":
                assert static_value
                data["static_value"] = static_value
            elif prediction_type == "automl":
                assert type(model) == AutoMLModel
                data["automl_model_id"] = model.id

        resp = self._request(
            method="PUT", url=f"{MLS_EXPERIMENTS_API_URL}/{bucket.experiment.id}/buckets/{bucket.id}", data=data
        ).results
        resp["experiment"] = bucket.experiment
        resp["prediction"]["ml_model"] = model

        bucket.reset(**resp)

        return bucket

    def migrate_bucket(
        self,
        prev_model: Union[ManualModel, AutoMLModel],
        next_prediction_type: str,
        next_model: Union[ManualModel, AutoMLModel] = None,
        next_static_value: Dict[str, Any] = None,
    ) -> List[Bucket]:
        """
        `prev_model` 이 연결되어 있는 모든 버킷을 `next_model` (또는 `next_static_value`) 으로 대체합니다.

        ## Args
        - prev_model: (`sktmls.models.ManualModel`, `sktmls.models.AutoMLModel`) 기존 모델
        - next_prediction_type: (str) 변경할 모델의 추론 타입 (`empty`|`static`|`batch`|`online`|`automl`)
        - next_model: (optional) (`sktmls.models.ManualModel`, `sktmls.models.AutoMLModel`) 변경할 모델
        - next_static_value: (optional) (dict(str, any)) 변경할 모델의 Static 값

        ## Returns
        list(`sktmls.experiments.Bucket`)
        - id: (int) 버킷 고유 ID
        - experiment: (int) 버킷이 속한 실험정보
        - prediction: (`sktmls.experiments.Prediction`) 해당 버킷의 Prediction 정보
        - name: (str) 버킷 이름
        - description: (str) 버킷 설명
        - bucket_range: (str) 해당 버킷의 범위
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example
        ```python

        my_prev_model = model_client.get_automl_model(
            name="my_prev_model",
            version="my_prev_version",
        )
        my_new_model = model_client.get_automl_model(
            name="my_new_model",
            version="my_new_version",
        )

        experiment_client.migrate_bucket(
            prev_model=my_prev_model,
            next_prediction_type='automl',
            prediction_type="batch"
        )
        ```
        """
        assert next_prediction_type in ["empty", "static", "batch", "online", "automl"]

        migration_request = {
            "prediction_type": next_prediction_type,
        }

        if next_prediction_type == "online":
            assert type(next_model) in [ManualModel, AutoMLModel]
            migration_request["online_model_id"] = next_model.id
        elif next_prediction_type == "batch":
            assert type(next_model) in [ManualModel, AutoMLModel]
            migration_request["batch_model_id"] = next_model.id
        elif next_prediction_type == "static":
            assert next_static_value
            migration_request["static_value"] = next_static_value
        elif next_prediction_type == "automl":
            assert type(next_model) == AutoMLModel
            migration_request["automl_model_id"] = next_model.id

        resp = self._request(
            method="POST",
            url=MLS_BUCKET_MIGRATIONS_API_URL,
            data={
                "model_id": prev_model.id,
                "migration_request": migration_request,
            },
        ).results

        return [Bucket(**bucket) for bucket in resp]
