import json
from assertpy import assert_that

LOG_TYPE_IMAGE = "image"
LOG_TYPE_MEDIA = "media"
LOG_TYPE_TABLE = "table"

class Media:

    def __init__(self, log_type: str=LOG_TYPE_MEDIA, path: str="") -> None:
        # 서버로 로깅되는 타입("media" 로 고정)
        self.log_type = log_type

        # 파일이 저장된 위치
        self.path = path

    # 서버로 전송될 파일 지정
    # 상속받는 자식 객체에서 공통적으로 사용할 함수
    def set_file(self) -> None:
        pass

    def to_json(self, key_name: str) -> str:
        assert_that(key_name).is_not_none()

        value_type = __class__.__name__
        return json.dumps({
            "log_type" : self.log_type,
            "hash" : "",
            "size" : 0,
            "path" : self.get_path(key_name, value_type),
        })

    # json으로 구성된 메타데이터 전송
    # 상속받는 자식 객체에서 공통적으로 사용할 함수
    def upload(self) -> None:
        pass

    # 실제 파일 서버로 전송
    # 상속받는 자식 객체에서 공통적으로 사용할 함수
    def upload_file(self) -> None:
        pass

    def get_path(self, key_name: str, value_type: str) -> str:
        return f"{key_name}.{value_type}.json"
