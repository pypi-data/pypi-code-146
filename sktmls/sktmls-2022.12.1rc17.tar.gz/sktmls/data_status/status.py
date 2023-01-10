from typing import List
from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSClientError

MLS_DATA_STATUS_API_URL = "/api/v1/data_status"


class S3Status:
    """
    MLS S3 업로드 상태를 나타내는 클래스입니다.
    """

    def __init__(self, table: str, daily_status: List[dict]):
        """
        ## Args

        - table: (str) 테이블 명
        - daily_status: (list) 최근 5일간의 상태 값 리스트

        ## Returns
        `sktmls.data_status.S3Status`
        """
        self.table = table
        self.daily_status = daily_status

    def get(self):
        return self.__dict__


class BatchStatus:
    """
    MLS Batch 작업 상태를 나타내는 클래스입니다.
    """

    def __init__(self, job_status: str, jobs: List[dict]):
        """
        ## Args

        - job_status: (str) 작업 상태 (`running`|`success`|`fail`)
        - jobs: (list) 작업 리스트

        ## Returns
        `sktmls.data_status.BatchStatus`
        """
        self.job_status = job_status
        self.jobs = jobs

    def get(self):
        return self.__dict__


class DynamoDBStatus:
    """
    MLS DynamoDB 업로드 상태를 나타내는 클래스입니다.
    """

    def __init__(self, table: str, status: List[dict]):
        """
        ## Args

        - table: (str) 테이블 명
        - status: (list) 최근 5일간의 상태값 리스트

        ## Returns
        `sktmls.data_status.DynamoDBStatus`
        """
        self.table = table
        self.status = status

    def get(self):
        return self.__dict__


class StatusClient(MLSClient):
    """
    MLS Status 관련 기능들을 제공하는 클라이언트입니다.
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
        `sktmls.data_status.StatusClient`

        ## Example

        ```python
        status_client = StatusClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def list_s3_status(self) -> List[S3Status]:
        """
        S3 상태 리스트를 가져옵니다.

        ## Returns
        list(`sktmls.data_status.S3Status`)

        - table: (str) 테이블 명
        - daily_status: (list(dict)) 최근 5일간의 상태 값 리스트

        ## Example

        ```python
        s3_status_list = status_client.list_s3_status()
        ```
        """
        return [
            S3Status(table=table, daily_status=daily_status)
            for table, daily_status in self._request(method="GET", url=f"{MLS_DATA_STATUS_API_URL}/s3")
            .results["s3"]
            .items()
        ]

    def get_s3_status(self, table: str) -> S3Status:
        """
        S3 상태 정보를 가져옵니다.

        ## Args

        - table: (str) 테이블 명

        ## Returns
        `sktmls.data_status.S3Status`

        - table: (str) 테이블 명
        - daily_status: (list(dict)) 최근 5일간의 상태 값 리스트

        ## Example

        ```python
        s3_status = status_client.get_s3_status(table="sample_table")
        ```
        """
        try:
            daily_status = self._request(method="GET", url=f"{MLS_DATA_STATUS_API_URL}/s3").results["s3"][table]
        except KeyError:
            raise MLSClientError(code=404, msg="해당 테이블에 대한 상태값이 없습니다")

        return S3Status(
            table=table,
            daily_status=daily_status,
        )

    def list_batch_status(self) -> List[BatchStatus]:
        """
        Batch 상태 리스트를 가져옵니다.

        ## Returns
        list(`sktmls.data_status.BatchStatus`)

        - job_status: (str) 작업 상태 (`running`|`success`|`fail`)
        - jobs: (list(dict)) 작업 리스트

        ## Example

        ```python
        batch_status_list = status_client.list_batch_status()
        ```
        """
        return [
            BatchStatus(job_status=job_status, jobs=jobs)
            for job_status, jobs in self._request(method="GET", url=f"{MLS_DATA_STATUS_API_URL}/batch")
            .results["batch"]
            .items()
        ]

    def get_batch_status(self, job_status: str) -> BatchStatus:
        """
        Batch 상태를 가져옵니다.

        ## Args

        - job_status: (str) 작업 상태 (`running`|`success`|`fail`)

        ## Returns
        `sktmls.data_status.BatchStatus`

        - job_status: (str) 작업 상태 (`running`|`success`|`fail`)
        - jobs: (list(dict)) 작업 리스트

        ## Example

        ```python
        batch_status = status_client.get_batch_status(job_status="success")
        ```
        """
        assert job_status in ["running", "success", "fail"], "작업의 상태는 running, success, fail 중 하나여야합니다"

        return BatchStatus(
            job_status=job_status,
            jobs=self._request(method="GET", url=f"{MLS_DATA_STATUS_API_URL}/batch").results["batch"][job_status],
        )

    def list_dynamodb_status(self) -> List[DynamoDBStatus]:
        """
        DynamoDB 상태 리스트를 가져옵니다.

        ## Returns
        list(`sktmls.data_status.DynamoDBStatus`)

        - table: (str) 테이블 명
        - status: (list(dict)) 최근 5일간의 상태값 리스트

        ## Example

        ```python
        dynamodb_status_list = status_client.list_dynamodb_status()
        ```
        """
        return [
            DynamoDBStatus(table_name, status)
            for table_name, status in self._request(method="GET", url=f"{MLS_DATA_STATUS_API_URL}/dynamodb")
            .results["dynamodb"]
            .items()
        ]

    def get_dynamodb_status(self, table: str) -> DynamoDBStatus:
        """
        DynamoDB 상태를 가져옵니다.

        ## Args

        - table: (str) 테이블 명

        ## Returns
        `sktmls.data_status.DynamoDBStatus`

        - table: (str) 테이블 명
        - status: (list(dict)) 최근 5일간의 상태값 리스트

        ## Example

        ```python
        dynamodb_status = status_client.get_dynamodb_status(table="sample_table")
        ```
        """
        try:
            status = self._request(method="GET", url=f"{MLS_DATA_STATUS_API_URL}/dynamodb").results["dynamodb"][table]
        except KeyError:
            raise MLSClientError(code=404, msg="해당 테이블에 대한 상태값이 없습니다")

        return DynamoDBStatus(table=table, status=status)
