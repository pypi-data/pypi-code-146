from enum import Enum
from typing import List


class MLSENV(Enum):
    DEV = "dev"
    STG = "stg"
    PRD = "prd"
    LOCAL = "local"

    @classmethod
    def list_items(cls) -> List["MLSENV"]:
        """
        모든 MLS 환경을 리스트로 반환합니다.
        """
        return [t for t in cls]

    @classmethod
    def list_values(cls) -> List[str]:
        """
        모든 MLS 환경 이름을 리스트로 반환합니다.
        """
        return [t.value for t in cls]


class MLSRuntimeENV(Enum):
    YE = "YE"
    EDD = "EDD"
    MMS = "MMS"
    LOCAL = "LOCAL"

    @classmethod
    def list_items(cls) -> List["MLSRuntimeENV"]:
        """
        모든 MLSRuntimeENV 환경을 리스트로 반환합니다.
        """
        return [t for t in cls]

    @classmethod
    def list_values(cls) -> List[str]:
        """
        모든 MLSRuntimeENV 환경 이름을 리스트로 반환합니다.
        """
        return [t.value for t in cls]
