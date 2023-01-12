import enum
from datomizer.protos.autodiscoveryservice_pb2 import ColumnDTO
from datomizer.utils.schema import Roles
from datomizer.utils.messages import EML_TARGET_INVALID_ROLE, EML_TARGET_INVALID_UNIQUE_COUNT


class Algorithms(enum.Enum):
    ADABOOST = "ADABOOST"
    BGG = "BGG"
    CATBOOST = "CATBOOST"
    DECISION_TREE = "DECISION_TREE"
    EXTRA_TREE = "EXTRA_TREE"
    GBM = "GBM"
    KNN = "KNN"
    LINEAR_SVM = "LINEAR_SVM"
    LR = "LR"
    LGBM = "LGBM"
    NB = "NB"
    NN = "NN"
    POLY_SVM = "POLY_SVM"
    RANDOM_FOREST = "RANDOM_FOREST"
    SVM = "SVM"
    XGBOOST = "XGBOOST"


class Metrics(enum.Enum):
    ACC = "ACC"
    AUC = "AUC"
    BALANCED_ACC = "BALANCED_ACC"
    F1 = "F1"
    MAE = "MAE"
    MSE = "MSE"
    PRECISION = "PRECISION"
    RECALL = "RECALL"
    RMSE = "RMSE"
    ROC_AUC = "ROC_AUC"
    PR_AUC = "PR_AUC"


def map_enum_list(enum_list: []):
    return [obj.value for obj in enum_list]


def assert_column_valid_for_eml(column: ColumnDTO) -> bool:
    assert column.role == Roles.LABEL.value, EML_TARGET_INVALID_ROLE
    assert 2 <= column.uniqueCount <= 10, EML_TARGET_INVALID_UNIQUE_COUNT
