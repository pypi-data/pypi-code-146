from collections.abc import Sequence
from enum import Enum
from typing import Any, Iterable as IterableType, List, Optional, Tuple, Union

import numpy as np
import pydantic
from numpy.typing import ArrayLike
from pydantic import BaseModel

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.helpers.versioned_model import VersionedModel

DataList = List[List[float]]
LabelsInt = List[int]


def listify(obj: Union[IterableType, ArrayLike]) -> list:
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, Sequence) and obj and isinstance(obj[0], np.ndarray):
        return np.array(obj).tolist()
    elif isinstance(obj, list):
        return obj
    else:
        return list(obj)  # type: ignore[arg-type]


class QSVMPreferences(BaseModel):
    execution_preferences: ExecutionPreferences
    l2_norm_regularization_factor: float = 0.001


class QSVMFeatureMapEntanglement(str, Enum):
    FULL = "full"
    LINEAR = "linear"
    CIRCULAR = "circular"
    SCA = "sca"
    PAIRWISE = "pairwise"


class QSVMFeatureMapDimensional(BaseModel):
    feature_dimension: Optional[int] = None


VALID_PAULI_LETTERS = ("I", "X", "Y", "Z")


class QSVMFeatureMapPauli(QSVMFeatureMapDimensional):
    reps: int = 2
    entanglement: QSVMFeatureMapEntanglement = QSVMFeatureMapEntanglement.LINEAR
    alpha: float = 2.0
    paulis: List[str] = ["Z", "ZZ"]
    parameter_prefix: str = "x"
    name: str = "PauliFeatureMap"

    @pydantic.validator("paulis", pre=True)
    def set_paulis(cls, paulis):
        # iterate every letter in every string in the list of paulis
        for s in paulis:
            if not all(map(VALID_PAULI_LETTERS.__contains__, s.upper())):
                raise ValueError(
                    f'Invalid pauli string given: "{s}". Expecting a combination of {VALID_PAULI_LETTERS}'
                )
        return list(map(str.upper, paulis))


class QSVMFeatureMapBlochSphere(QSVMFeatureMapDimensional):
    pass


FeatureMapType = Union[QSVMFeatureMapBlochSphere, QSVMFeatureMapPauli]


def validate_array_to_list(name: str):
    return pydantic.validator(name, pre=True, allow_reuse=True)(listify)


Shape = Tuple[int, ...]


class QSVMInternalState(BaseModel):
    underscore_sparse: bool
    class_weight: list
    classes: list
    underscore_gamma: float
    underscore_base_fit: list
    support: list
    support_vectors: list
    underscore_n_support: list
    dual_coef_2: list
    intercept: list
    underscore_p_a: list
    underscore_p_b: list
    fit_status: int
    shape_fit: Shape
    underscore_intercept: list
    dual_coef: list

    class_weight__shape: Shape
    classes__shape: Shape
    underscore_base_fit__shape: Shape
    support__shape: Shape
    support_vectors__shape: Shape
    underscore_n_support__shape: Shape
    dual_coef_2__shape: Shape
    intercept__shape: Shape
    underscore_p_a__shape: Shape
    underscore_p_b__shape: Shape
    underscore_intercept__shape: Shape
    dual_coef__shape: Shape

    set_class_weight = validate_array_to_list("class_weight")
    set_classes = validate_array_to_list("classes")
    set_underscore_base_fit = validate_array_to_list("underscore_base_fit")
    set_support = validate_array_to_list("support")
    set_support_vectors = validate_array_to_list("support_vectors")
    set_underscore_n_support = validate_array_to_list("underscore_n_support")
    set_dual_coef_2 = validate_array_to_list("dual_coef_2")
    set_intercept = validate_array_to_list("intercept")
    set_underscore_p_a = validate_array_to_list("underscore_p_a")
    set_underscore_p_b = validate_array_to_list("underscore_p_b")
    set_underscore_intercept = validate_array_to_list("underscore_intercept")
    set_dual_coef = validate_array_to_list("dual_coef")


class QSVMData(BaseModel):
    data: DataList
    labels: Optional[LabelsInt] = None
    feature_map: FeatureMapType
    internal_state: Optional[QSVMInternalState] = None
    preferences: QSVMPreferences

    class Config:
        smart_union = True
        extra = "forbid"

    @pydantic.validator("data", pre=True)
    def set_data(cls, data):
        return listify(data)

    @pydantic.validator("labels", pre=True)
    def set_labels(cls, labels):
        if labels is None:
            return None
        else:
            return listify(labels)


QSVMTrainResult = QSVMInternalState
QSVMTestResult = float  # between 0 to 1
QSVMPredictResult = list  # serialized np.array


class QSVMResult(VersionedModel):
    details: Optional[Any] = None  # anything that's convertible to string
    result: Union[
        QSVMTrainResult,
        QSVMTestResult,
        QSVMPredictResult,
    ]
