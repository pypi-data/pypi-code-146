from typing import Any, Dict, List

from sktmls.models import MLSLightGBMModel, MLSXGBoostModel, MLSCatBoostModel, MLSGenericModel


class DefaultLightGBMModel(MLSLightGBMModel):
    """
    MLS 모델 레지스트리에 등록되는 LightGBM 기본 클래스입니다.

    온라인 추론 없이 MLS 모델 레지스트리에 바이너리만을 등록하고자 할 때 사용합니다.
    """

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        """
        본 클래스의 predict 함수는 아무런 일을 하지 않습니다.
        """
        return {"items": []}


class DefaultXGBoostModel(MLSXGBoostModel):
    """
    MLS 모델 레지스트리에 등록되는 XGBoost 기본 클래스입니다.

    온라인 추론 없이 MLS 모델 레지스트리에 바이너리만을 등록하고자 할 때 사용합니다.
    """

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        """
        본 클래스의 predict 함수는 아무런 일을 하지 않습니다.
        """
        return {"items": []}


class DefaultCatBoostModel(MLSCatBoostModel):
    """
    MLS 모델 레지스트리에 등록되는 CatBoost 기본 클래스입니다.

    온라인 추론 없이 MLS 모델 레지스트리에 바이너리만을 등록하고자 할 때 사용합니다.
    """

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        """
        본 클래스의 predict 함수는 아무런 일을 하지 않습니다.
        """
        return {"items": []}


class DefaultGenericModel(MLSGenericModel):
    """
    MLS 모델 레지스트리에 등록되는 일반모델 기본 클래스입니다.

    온라인 추론 없이 MLS 모델 레지스트리에 바이너리만을 등록하고자 할 때 사용합니다.
    models는 list 타입으로 모델이 한 개만 저장되는 경우에도 list 형태로 전달하여야 합니다.
    """

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        """
        본 클래스의 predict 함수는 아무런 일을 하지 않습니다.
        """
        return {"items": []}
