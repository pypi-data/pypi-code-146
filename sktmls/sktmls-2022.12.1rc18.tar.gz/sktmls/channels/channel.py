from typing import List, TYPE_CHECKING

from dateutil import parser

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse, MLSClientError

if TYPE_CHECKING:
    from sktmls.experiments import Experiment

MLS_CHANNELS_API_URL = "/api/v1/channels"


class Channel:
    """
    MLS 채널 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 채널 고유 ID
            - screen_id: (str) 채널 이름
            - experiments: (list(int)) 연결된 실험 ID 리스트
            - user: (str) 채널 생성 계정명
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `sktmls.channels.Channel`
        """
        self.id = kwargs.get("id")
        self.screen_id = kwargs.get("screen_id")
        self.experiments = kwargs.get("experiments")
        self.user = kwargs.get("user")

        if kwargs.get("created_at"):
            self.created_at = parser.parse(kwargs.get("created_at"))
        if kwargs.get("updated_at"):
            self.updated_at = parser.parse(kwargs.get("updated_at"))

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ChannelClient(MLSClient):
    """
    MLS 채널 관련 기능들을 제공하는 클라이언트입니다.
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
        `sktmls.channels.ChannelClient`

        ## Example

        ```python
        channel_client = ChannelClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """

        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_channel(self, name: str, experiments: List["Experiment"]) -> Channel:
        """
        채널를 생성합니다.

        ## Args

        - name: (str) 채널 이름
        - experiments: (list(`sktmls.experiments.Experiment`)) 실험 객체 리스트

        ## Returns
        `sktmls.channels.Channel`

        - id: (int) 채널 고유 ID
        - screen_id: (str) 채널 이름
        - experiments: (list(int)) 연결된 실험 ID 리스트
        - user: (str) 채널 생성 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        experiment_1 = experiment_client.get_experiment(name="my_experiment_1")
        experiment_2 = experiment_client.get_experiment(name="my_experiment_2")

        channel = channel_client.create_channel(
            name="my_channel",
            experiments=[
                experiment_1,
                experiment_2,
            ]
        )
        ```
        """
        assert type(experiments) == list, "`experiments`는 Experiment객체를 담은 list타입이어야 합니다."
        assert len(experiments) >= 1, "최소 1개 이상의 Experiment객체가 포함되어야 합니다."

        data = {
            "screen_id": name,
            "experiments": [experiment.id for experiment in experiments],
        }

        return Channel(**self._request(method="POST", url=MLS_CHANNELS_API_URL, data=data).results)

    def list_channels(self, **kwargs) -> List[Channel]:
        """
        채널 리스트를 가져옵니다. (채널 조건 제외)

        ## Args

        - kwargs: (optional) (dict) 채널 조건
            - id: (int) 채널 고유 ID
            - name: (str) 채널 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.channels.Channel`)

        - id: (int) 채널 고유 ID
        - name: (str) 채널 이름
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        channels = channel_client.list_channels()
        ```
        """

        response = self._request(method="GET", url=f"{MLS_CHANNELS_API_URL}", params=kwargs).results

        return [Channel(**channel) for channel in response]

    def get_channel(self, id: int = None, name: str = None) -> Channel:
        """
        채널 정보를 가져옵니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (optional) (int) 채널 고유 ID
        - name: (optional) (str) 채널 이름

        ## Returns
        `sktmls.channels.Channel`

        - id: (int) 채널 고유 ID
        - screen_id: (str) 채널 이름
        - experiments: (list(int)) 연결된 실험 ID 리스트
        - user: (str) 채널 생성 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        channel_by_id = channel_client.get_channel(
            id=3
        )
        channel_by_name = channel_client.get_channel(
            name="my_channel"
        )
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        channels = self.list_channels(id=id, screen_id=name)
        if len(channels) == 0:
            raise MLSClientError(code=404, msg="채널이 없습니다.")
        elif len(channels) > 1:
            raise MLSClientError(code=409, msg="채널이 여러개 존재합니다.")
        return Channel(**self._request(method="GET", url=f"{MLS_CHANNELS_API_URL}/{channels[0].id}").results)

    def update_channel(self, channel: Channel, name: str = None, experiments: List["Experiment"] = None) -> Channel:
        """
        채널 정보를 수정합니다.

        ## Args

        - channel: (`sktmls.channels.Channel`) 채널 객체
        - name: (optional) (str) 채널 이름
        - experiments: (optional) (list(`sktmls.experiments.Experiment`)) 실험 객체 리스트

        ## Returns
        `sktmls.channels.Channel`

        - id: (int) 채널 고유 ID
        - screen_id: (str) 채널 이름
        - experiments: (list(int)) 연결된 실험 ID 리스트
        - user: (str) 채널 생성 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        experiment_new = experiment_client.get_experiment(name="my_experiment_new")

        channel = channel_clinet.get_channel(name="my_channel")
        channel = channel_client.update_channel(
            channel=channel,
            name="my_updated_channel",
            experiments=[experiment_new],
        )
        ```
        """
        assert type(channel) == Channel
        assert type(experiments) == list, "`experiments`는 Experiment객체를 담은 list타입이어야 합니다."
        assert len(experiments) >= 1, "최소 1개 이상의 Experiment객체가 포함되어야 합니다."

        data = {"screen_id": channel.screen_id, "experiments": channel.experiments}
        if name:
            data["screen_id"] = name
        if experiments:
            data["experiments"] = [experiment.id for experiment in experiments]

        channel.reset(**self._request(method="PUT", url=f"{MLS_CHANNELS_API_URL}/{channel.id}", data=data).results)
        return channel

    def delete_channel(self, channel: Channel) -> MLSResponse:
        """
        채널 삭제합니다.

        ## Args

        - channel: (`sktmls.channels.Channel`) 채널 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        channel_client.delete_channel(channel)
        ```
        """

        assert type(channel) == Channel

        return self._request(method="DELETE", url=f"{MLS_CHANNELS_API_URL}/{channel.id}")
