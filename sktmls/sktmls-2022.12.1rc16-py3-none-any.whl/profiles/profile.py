from os.path import commonprefix
from typing import List

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse, MLSClientError

MLS_PROFILES_API_URL = "/api/v1/profile"


class Profile:
    """
    MLS 프로파일 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 프로파일 고유 ID
            - profile_id: (str) 프로파일 이름
            - tables: (list) 프로파일에 연결할 DynamoDB 테이블 이름 리스트
            - user: (str) 프로파일 소유 계정명

        ## Returns
        `sktmls.profiles.Profile`
        """
        self.id = kwargs.get("id")
        self.profile_id = kwargs.get("profile_id")
        self.tables = kwargs.get("tables")
        self.user = kwargs.get("user")

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ProfileClient(MLSClient):
    """
    MLS 프로파일 관련 기능들을 제공하는 클라이언트입니다.
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

        ## Returns
        `sktmls.profiles.ProfileClient`

        ## Example

        ```python
        profile_client = ProfileClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_profile(self, profile_id: str, tables: List[str], main_table: str = None) -> Profile:
        """
        프로파일을 생성합니다.

        ## Args

        - profile_id: (str) 프로파일 이름
        - tables: (list) 프로파일에 연결할 DynamoDB 테이블 이름 리스트
            - 테이블 간 중복 키에 대한 값 우선 순위는 왼쪽 테이블이 오른쪽 테이블보다 높습니다.
            - 연결된 모든 테이블 내에 없는 키에 대한 값은 null로 반환됩니다.
        - main_table: (optional) (str) 서비스 대상 여부를 결정하는 테이블
            - 기준 테이블에 데이터가 존재하지 않는 경우 다른 테이블에 데이터가 있다 하더라도 서비스되지 않습니다.
            - 기준 테이블에 데이터가 존재하는 경우 다른 테이블의 데이터 여부와 관계 없이 반드시 서비스됩니다.
            - 미선택 시 `tables` 파라미터에 명시된 테이블 중 첫 번째 테이블로 설정됩니다.

        ## Returns
        `sktmls.profiles.Profile`

        - id: (int) 프로파일 고유 ID
        - profile_id: (str) 프로파일 이름
        - tables: (list) 프로파일에 연결할 DynamoDB 테이블 이름 리스트
        - main_table: (str) 연결 테이블 중 기준이 되는 테이블 (추후 로직 추가 예정)
        - user: (str) 프로파일 소유 계정명

        ## Example

        ```python
        profile = profile_client.create_profile(
            profile_id="my_profile",
            tables=["user-profile", "user-profile-daily"]
        )
        ```
        """
        assert type(tables) == list
        for table_name in tables:
            assert type(table_name) == str, "`tables`는 문자열만 포함해야 합니다."
        assert commonprefix(tables).startswith(
            ("user-profile", "item-profile", "profile-")
        ), "`tables`의 테이블 이름은 반드시 user-profile,item-profile, profile- 중 하나로 시작해야 합니다. "

        data = {"profile_id": profile_id, "tables": tables}
        if main_table:
            data["main_table"] = main_table

        return Profile(**self._request(method="POST", url=f"{MLS_PROFILES_API_URL}", data=data).results)

    def list_profiles(self, **kwargs) -> List[Profile]:
        """
        프로파일 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 프로파일 고유 ID
            - profile_id: (str) 프로파일 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.profiles.Profile`)

        - id: (int) 프로파일 고유 ID
        - profile_id: (str) 프로파일 이름
        - tables: (list) 프로파일에 연결할 DynamoDB 테이블 이름 리스트
        - main_table: (str) 연결 테이블 중 기준이 되는 테이블 (추후 로직 추가 예정)
        - user: (str) 프로파일 소유 계정명

        ## Example

        ```python
        all_my_user_profiles = profile_client.list_profiles(api_type="user")
        ```
        """

        response = self._request(method="GET", url=f"{MLS_PROFILES_API_URL}", params=kwargs).results
        return [Profile(**profile) for profile in response]

    def get_profile(self, id: int = None, profile_id: str = None) -> Profile:
        """
        프로파일 정보를 가져옵니다.

        ## Args: `id` 또는 `profile_id` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - api_type: (str) 프로파일 타입 (`user`|`item`)
        - id: (int) 프로파일 고유 ID
        - profile_id: (str) 프로파일 이름

        ## Returns
        `sktmls.clients.Client`

        - id: (int) 프로파일 고유 ID
        - api_type: (str) 프로파일 타입 (`user`|`item`)
        - profile_id: (str) 프로파일 이름
        - tables: (list) 프로파일에 연결할 DynamoDB 테이블 이름 리스트
        - main_table: (str) 연결 테이블 중 기준이 되는 테이블 (추후 로직 추가 예정)
        - user: (str) 프로파일 소유 계정명

        ## Example

        ```python
        profile_by_id = profile_client.get_profile(api_type="user", id=3)
        profile_by_profile_id = profile_client.get_profile(api_type="item", profile_id="my_item_profile")
        ```
        """
        assert id or profile_id, "`id` 또는 `profile_id` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        profiles = self.list_profiles(id=id, profile_id=profile_id)
        if len(profiles) == 0:
            raise MLSClientError(code=404, msg="프로파일이 없습니다.")
        if len(profiles) > 1:
            raise MLSClientError(code=409, msg="프로파일이 여러개 존재합니다.")
        return profiles[0]

    def update_profile(
        self, profile: Profile, profile_id: str = None, tables: List[str] = None, main_table: str = None
    ) -> Profile:
        """
        프로파일 정보를 수정합니다.

        ## Args

        - profile_id: (optional) (str) 프로파일 이름
        - tables: (optional) (list) 프로파일에 연결할 DynamoDB 테이블 이름 리스트
            - 테이블 간 중복 키에 대한 값 우선 순위는 왼쪽 테이블이 오른쪽 테이블보다 높습니다.
            - 연결된 모든 테이블 내에 없는 키에 대한 값은 null로 반환됩니다.
        - main_table: (optional) (str) 서비스 대상 여부를 결정하는 테이블
            - 기준 테이블에 데이터가 존재하지 않는 경우 다른 테이블에 데이터가 있다 하더라도 서비스되지 않습니다.
            - 기준 테이블에 데이터가 존재하는 경우 다른 테이블의 데이터 여부와 관계 없이 반드시 서비스됩니다.
            - 미선택 시 `tables` 파라미터에 명시된 테이블 중 첫 번째 테이블로 설정됩니다.

        ## Returns
        `sktmls.profiles.Profile`

        - id: (int) 프로파일 고유 ID
        - profile_id: (str) 프로파일 이름
        - tables: (list) 프로파일에 연결할 DynamoDB 테이블 이름 리스트
        - main_table: (str) 연결 테이블 중 기준이 되는 테이블 (추후 로직 추가 예정)
        - user: (str) 프로파일 소유 계정명

        ## Example

        ```python
        profile = profile_client.profile_profile(
            profile=my_profile,
            profile_id="updated_profile",
            tables=["user-profile", "user-profile-daily"]
        )
        ```
        """
        assert type(profile) == Profile

        data = profile.get()
        if profile_id:
            data["profile_id"] = profile_id
        if tables:
            assert type(tables) == list
            for table_name in tables:
                assert type(table_name) == str, "`tables`는 문자열만 포함해야 합니다."
            assert commonprefix(tables).startswith(
                ("user-profile", "item-profile", "profile-")
            ), "`tables`의 테이블 이름은 반드시 user-profile,item-profile, profile- 중 하나로 시작해야 합니다. "
            data["tables"] = tables
        if main_table:
            data["main_table"] = main_table

        return profile.reset(
            **self._request(method="PUT", url=f"{MLS_PROFILES_API_URL}/{profile.id}", data=data).results
        )

    def delete_profile(self, profile: Profile) -> MLSResponse:
        """
        프로파일을 삭제합니다.

        ## Args

        - profile: (`sktmls.profiles.Profile`) 프로파일 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        profile_client.delete_profile(my_profile)
        ```
        """
        assert type(profile) == Profile

        return self._request(method="DELETE", url=f"{MLS_PROFILES_API_URL}/{profile.id}")
